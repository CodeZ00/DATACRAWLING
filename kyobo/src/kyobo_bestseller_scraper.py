"""교보문고 컴퓨터/IT 베스트셀러 데이터 수집 스크립트.

교보문고 내부 REST Gateway API를 직접 호출하여
컴퓨터/IT 일간 베스트셀러 전체 목록(마지막 순위 593위)을 수집하고 CSV로 저장합니다.
"""

import csv
import datetime
import gzip
import json
import math
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


def clean_html(text: str) -> str:
    """HTML 태그 제거 및 불필요한 연속 공백 정제."""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def fetch_kyobo_page(page: int = 1, per: int = 50) -> dict:
    """교보문고 베스트셀러 특정 페이지의 JSON 데이터를 요청하여 반환합니다.

    Args:
        page (int): 요청할 페이지 번호 (기본 1)
        per (int): 페이지당 도서 수 (기본 50)

    Returns:
        dict: 파싱된 JSON 응답 딕셔너리
    """
    base_url = "https://store.kyobobook.co.kr/api/gw/best/best-seller/online"
    params = {
        "page": str(page),
        "per": str(per),
        "period": "001",
        "dsplDvsnCode": "001",
        "dsplTrgtDvsnCode": "004",
        "saleCmdtClstCode": "33",  # 컴퓨터/IT
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://store.kyobobook.co.kr/bestseller/online/daily/domestic/33?page=1",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
    }

    req = urllib.request.Request(url, headers=headers, method="GET")

    with urllib.request.urlopen(req, timeout=15) as resp:
        content_encoding = resp.headers.get("Content-Encoding", "").lower()
        raw_data = resp.read()

        if "gzip" in content_encoding or raw_data.startswith(b"\x1f\x8b"):
            decompressed = gzip.decompress(raw_data)
            return json.loads(decompressed.decode("utf-8"))
        else:
            return json.loads(raw_data.decode("utf-8"))


def parse_book_item(item: dict) -> dict:
    """API 응답 항목에서 15개 명세 컬럼을 추출하여 반환합니다."""
    return {
        "rank": item.get("prstRnkn"),
        "prev_rank": item.get("frmrRnkn"),
        "book_id": item.get("saleCmdtid"),
        "title": item.get("cmdtName"),
        "author": item.get("chrcName"),
        "publisher": item.get("pbcmName"),
        "pub_date": item.get("rlseDate"),
        "fixed_price": item.get("price"),
        "sale_price": item.get("sapr"),
        "discount_rate": item.get("dscnRate"),
        "point": item.get("upntAcmlAmnt"),
        "review_count": item.get("buyRevwNumc"),
        "rating": item.get("buyRevwRvgr"),
        "isbn": item.get("cmdtCode"),
        "intro": clean_html(item.get("inbukCntt") or ""),
    }


def scrape_all_kyobo_bestsellers(max_rank: int = 593) -> list[dict]:
    """전체 베스트셀러 목록을 페이징하여 수집합니다 (최대 순위 제한 지원)."""
    print(">>> 1페이지 조회 시작 (전체 도서 수 확인)...")
    first_res = fetch_kyobo_page(page=1, per=50)

    data_section = first_res.get("data", {})
    total_count = data_section.get("total", 0)
    best_sellers = data_section.get("bestSeller", [])

    print(f">>> API 반환 전체 등록 도서 수: {total_count}건, 수집 제한 순위: {max_rank}위")

    all_books = []
    for item in best_sellers:
        parsed = parse_book_item(item)
        if parsed["rank"] and int(parsed["rank"]) <= max_rank:
            all_books.append(parsed)

    per = 50
    target_count = min(total_count, max_rank)
    total_pages = math.ceil(target_count / per)
    print(f">>> 총 수집 대상 페이지: {total_pages}페이지 (1페이지 {len(all_books)}건 수집 완료)")

    for page in range(2, total_pages + 1):
        print(f">>> {page}/{total_pages} 페이지 수집 중...")
        time.sleep(0.5)  # 서버 부하 방지용 지연
        try:
            res = fetch_kyobo_page(page=page, per=per)
            items = res.get("data", {}).get("bestSeller", [])
            if not items:
                print(f"    {page}페이지에 더 이상 데이터가 없습니다.")
                break
            
            added_count = 0
            for item in items:
                parsed = parse_book_item(item)
                if parsed["rank"] and int(parsed["rank"]) <= max_rank:
                    all_books.append(parsed)
                    added_count += 1
            
            print(f"    {page}페이지 수집 완료: +{added_count}건 (누적: {len(all_books)}건)")
            
            # 마지막 순위 도달 시 조기 종료
            if all_books and int(all_books[-1]["rank"]) >= max_rank:
                print(f">>> 지정한 마지막 순위({max_rank}위)에 도달하여 수집을 종료합니다.")
                break
        except Exception as e:
            print(f"    [오류] {page}페이지 수집 중 에러 발생: {e}")

    # 최종 순위 기준 정렬 및 중복 제거
    seen_ids = set()
    unique_books = []
    for b in all_books:
        if b["book_id"] not in seen_ids:
            seen_ids.add(b["book_id"])
            unique_books.append(b)

    unique_books.sort(key=lambda x: int(x["rank"]) if x["rank"] else 9999)
    return unique_books


def save_to_csv(books: list[dict], output_path: Path):
    """도서 목록 데이터를 CSV 파일로 저장합니다."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "rank",
        "prev_rank",
        "book_id",
        "title",
        "author",
        "publisher",
        "pub_date",
        "fixed_price",
        "sale_price",
        "discount_rate",
        "point",
        "review_count",
        "rating",
        "isbn",
        "intro",
    ]

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    print(f">>> CSV 저장 완료: {output_path} (총 {len(books)}건)")


def main():
    """메인 실행 함수."""
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    output_path = Path("kyobo") / "data" / f"kyobo_daily_it_bestseller_{today_str}.csv"

    print("=" * 60)
    print("교보문고 컴퓨터/IT 베스트셀러 데이터 재수집 시작")
    print(f"목표 마지막 순위: 593위")
    print(f"저장 예정 경로: {output_path}")
    print("=" * 60)

    books = scrape_all_kyobo_bestsellers(max_rank=593)
    save_to_csv(books, output_path)

    print("=" * 60)
    print(f"수집 완료! (총 {len(books)}건, 1위 ~ {books[-1]['rank'] if books else 0}위)")
    print("=" * 60)


if __name__ == "__main__":
    main()
