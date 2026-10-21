"""[범용 스크래퍼 템플릿] Universal Scraper Template

새로운 사이트의 REST API 또는 정적 HTML을 안전하고 빠르게 전수 수집할 수 있는
표준 뼈대 코드입니다. GZIP 응답 압축 해제, 재시도 로직, 서버 부하 방지 대기,
UTF-8-SIG 인코딩 저장 및 수집 검증 기능이 내장되어 있습니다.
"""

import csv
import gzip
import html
import io
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path


class UniversalScraper:
    def __init__(self, site_name: str, base_url: str, output_dir: str = "data"):
        self.site_name = site_name
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 기본 헤더 설정 (필요에 따라 대상 사이트에 맞게 수정)
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": base_url,
        }

    def fetch_api(self, url: str, params: dict = None, max_retries: int = 3) -> dict | list:
        """GET 요청을 보내고 GZIP 압축 해제 및 JSON을 파싱하여 반환합니다."""
        if params:
            query_string = urllib.parse.urlencode(params)
            sep = "&" if "?" in url else "?"
            full_url = f"{url}{sep}{query_string}"
        else:
            full_url = url

        req = urllib.request.Request(full_url, headers=self.headers)

        for attempt in range(1, max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=15) as response:
                    raw_data = response.read()

                    # GZIP 매직 넘버(0x1f, 0x8b) 확인 및 압축 해제
                    if raw_data.startswith(b"\x1f\x8b"):
                        decompressed = gzip.decompress(raw_data)
                        text = decompressed.decode("utf-8", errors="replace")
                    else:
                        text = raw_data.decode("utf-8", errors="replace")

                    return json.loads(text)

            except Exception as e:
                print(f"[경고] 요청 실패 (시도 {attempt}/{max_retries}) URL: {full_url} - 원인: {e}")
                if attempt < max_retries:
                    time.sleep(2**attempt)
                else:
                    raise

    @staticmethod
    def clean_text(text: str) -> str:
        """HTML 태그 제거 및 특수 엔티티 정제 유틸리티"""
        if not text:
            return ""
        # HTML 태그 제거
        clean = re.sub(r"<[^>]+>", "", str(text))
        # HTML 엔티티 언이스케이프 (&amp; -> &, &lt; -> < 등)
        clean = html.unescape(clean)
        # 연속된 공백 정리
        return re.sub(r"\s+", " ", clean).strip()

    def scrape_all(self, total_pages: int = 10, page_size: int = 20) -> list[dict]:
        """대상 사이트의 페이지들을 순회하며 전수 수집을 수행합니다.
        
        * 사이트별 응답 구조에 맞게 커스텀 추출 로직을 수정하십시오.
        """
        all_records = []
        current_rank = 1

        print(f"[{self.site_name}] 데이터 수집 시작 (총 {total_pages}페이지 예정)...")

        for page in range(1, total_pages + 1):
            print(f" -> {page}/{total_pages} 페이지 요청 중...")
            
            # 파라미터 구성 예시
            params = {
                "page": page,
                "size": page_size,
            }

            try:
                response_json = self.fetch_api(self.base_url, params=params)
                
                # TODO: 응답 JSON 구조에 따라 아이템 목록 접근 경로를 수정하세요.
                # 예: items = response_json.get("data", {}).get("items", [])
                items = response_json.get("items", [])
                if not items and isinstance(response_json, list):
                    items = response_json

                if not items:
                    print(f" -> {page}페이지에서 더 이상 데이터가 없습니다. 수집 종료.")
                    break

                for item in items:
                    # TODO: 사이트의 고유 데이터 필드를 추출 및 정제하여 딕셔너리로 구성하세요.
                    record = {
                        "rank": current_rank,
                        "item_id": item.get("id") or item.get("code") or "",
                        "title": self.clean_text(item.get("title") or item.get("name") or ""),
                        "category": self.clean_text(item.get("category") or "일반"),
                        "price": int(item.get("price") or 0),
                        "sale_price": int(item.get("sale_price") or item.get("price") or 0),
                        "review_count": int(item.get("review_count") or 0),
                        "rating": float(item.get("rating") or 0.0),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    all_records.append(record)
                    current_rank += 1

                # 서버 부하 방지를 위한 필수 대기 (최소 0.5초)
                time.sleep(0.5)

            except Exception as e:
                print(f"[오류] {page}페이지 수집 중 에러 발생: {e}")
                break

        print(f"[{self.site_name}] 수집 완료: 총 {len(all_records)}건 수집됨.")
        return all_records

    def save_to_csv(self, records: list[dict], category_name: str = "all") -> Path:
        """수집된 레코드를 엑셀 호환 UTF-8-SIG 인코딩의 CSV 파일로 저장합니다."""
        if not records:
            raise ValueError("저장할 데이터가 비어 있습니다.")

        date_str = datetime.now().strftime("%Y%m%d")
        file_path = self.output_dir / f"{self.site_name}_daily_{category_name}_{date_str}.csv"

        fieldnames = list(records[0].keys())

        with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        print(f"💾 데이터 파일 저장 완료: {file_path} (총 {len(records)}행)")
        return file_path


def main():
    # 사용 예시
    scraper = UniversalScraper(
        site_name="example_site",
        base_url="https://api.example.com/v1/items",
        output_dir="data",
    )
    # records = scraper.scrape_all(total_pages=5)
    # scraper.save_to_csv(records, category_name="general")


if __name__ == "__main__":
    main()
