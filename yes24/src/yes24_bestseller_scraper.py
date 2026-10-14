"""
YES24 일별 베스트셀러 전 페이지 데이터 수집기

이 스크립트는 YES24 도서 쇼핑몰의 IT/모바일 분야 일별 베스트셀러 비동기 웹 페이지를
순차적으로 크롤링하여 도서 상세 정보(순위, 상품번호, 도서명, 저자, 출판사, 가격, 
평점, 리뷰 수, 판매지수 등 18개 필드)를 파싱하고 CSV 파일로 저장하는 데이터 수집 프로그램입니다.

[주요 기능]
1. 비동기 엔드포인트(BestSellerContents) HTTP GET 요청 및 HTML 응답 수신
2. 페이징 네비게이션 분석을 통한 전체 페이지 수 자동 감지
3. HTML 및 JSON 옵션 블록(ORD_GOODS_OPT) 정규식 기반 18개 도서 메타데이터 파싱
4. 기존 CSV 파일 데이터 분석을 통한 중복 제거 및 중단 지점 이어받기(Append) 수집 지원
5. 서버 부하 방지를 위한 페이지 간 랜덤 지연 시간(0.1 ~ 0.5초) 적용
6. 마지막 페이지 도달 및 페이지 순환 루프 자동 감지 및 안전 종료

[파일 정보]
- 작성 모듈: yes24/src/yes24_bestseller_scraper.py
- 생성 일자: 2026-10-06
- 최종 수정: 2026-10-07
- 저장 대상: yes24/data/yes24_day_bestseller.csv
"""

import os
import csv
import ssl
import json
import re
import html
import time
import random
import urllib.request
import urllib.parse
from datetime import datetime

# ==============================================================================
# CSV 파일 헤더 컬럼 정의 (총 18개 메타데이터 필드)
# ==============================================================================
CSV_HEADERS = [
    "rank",          # 순위
    "goods_no",      # 상품 고유 번호
    "title",         # 도서명
    "subtitle",      # 부제 및 부가 설명
    "author",        # 저자 및 번역자
    "publisher",     # 출판사
    "pub_date",      # 출간일 (예: 2026년 08월)
    "category",      # 카테고리 (예: IT 모바일)
    "fixed_price",   # 정가 (원)
    "sale_price",    # 판매가 (원)
    "discount_rate", # 할인율 (%)
    "point",         # 적립 포인트 (원)
    "rating",        # 회원 평점 (10점 만점)
    "review_count",  # 회원 리뷰 수
    "sales_index",   # 판매지수
    "tags",          # 태그 목록 (쉼표 구분)
    "url",           # 상품 상세 페이지 URL
    "image_url"      # 도서 표지 이미지 URL
]


def clean_text(text: str) -> str:
    """
    HTML 텍스트에서 불필요한 태그를 제거하고 HTML 엔티티를 일반 텍스트로 변환합니다.

    연속된 공백, 탭, 줄바꿈 문자를 하나의 공백으로 압축하고 앞뒤 공백을 제거합니다.
    HTML 엔티티가 이중 인코딩된 경우(&amp;amp; 등)를 고려하여 2회 연속 디코딩을 수행합니다.

    Args:
        text (str): 정제할 원본 문자열.

    Returns:
        str: HTML 태그와 엔티티가 정리된 순수 문자열. 빈 입력일 경우 빈 문자열 반환.
    """
    if not text:
        return ""
    # HTML 태그 (<tag>...</tag>) 제거
    cleaned = re.sub(r"<[^>]+>", "", text)
    # HTML 엔티티 디코딩 (이중 인코딩 대비 2회 변환: &#183;, &amp; 등)
    cleaned = html.unescape(html.unescape(cleaned))
    # 연속 공백 문자(\s+)를 단일 공백으로 치환
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def fetch_bestseller_html(page_number: int = 1, page_size: int = 24) -> str:
    """
    YES24 베스트셀러 비동기 콘텐츠 엔드포인트에 HTTP GET 요청을 보내 HTML 소스를 가져옵니다.

    브라우저와 동일한 User-Agent 및 헤더를 전송하여 차단을 방지하며,
    SSL 인증서 검증 우회 컨텍스트를 적용하여 네트워크 환경 이슈를 방지합니다.

    Args:
        page_number (int, optional): 조회할 베스트셀러 페이지 번호 (기본값: 1).
        page_size (int, optional): 한 페이지당 출력할 도서 수 (기본값: 24).

    Returns:
        str: 수신된 웹 페이지의 UTF-8 디코딩 HTML 문자열.

    Raises:
        RuntimeError: HTTP 응답 코드가 200(성공)이 아닐 경우 발생.
        urllib.error.URLError: 네트워크 연결 또는 타임아웃 오류 발생 시.
    """
    base_url = "https://www.yes24.com/product/category/BestSellerContents"
    
    # YES24 IT/모바일 일별 베스트셀러 쿼리 파라미터 구성
    params = {
        "categoryNumber": "001001003",  # 카테고리: IT 모바일
        "sumGb": "06",
        "sex": "A",
        "age": "255",
        "goodsTp": "0",
        "addOptionTp": "0",
        "excludeTp": "2",
        "pageNumber": str(page_number),
        "pageSize": str(page_size),
        "goodsStatGb": "06",
        "eBookTp": "0",
        "bestType": "DAY_BESTSELLER",   # 일별 베스트셀러
        "type": "day",
        "saleYear": "0",
        "saleMonth": "0",
        "weekNo": "0",
        "saleDts": "",
        "viewMode": "",
        "freeYn": ""
    }
    
    query_string = urllib.parse.urlencode(params)
    request_url = f"{base_url}?{query_string}"
    
    # 일반 브라우저 환경을 모사하기 위한 요청 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
        "Referer": f"https://www.yes24.com/product/category/daybestseller?pageNumber={page_number}&pageSize={page_size}&categoryNumber=001001003&type=day",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }
    
    req = urllib.request.Request(request_url, headers=headers, method="GET")
    
    # SSL 컨텍스트 설정 (자체 서명 인증서 및 검증 오류 방지)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    with urllib.request.urlopen(req, context=ctx, timeout=20) as response:
        if response.getcode() != 200:
            raise RuntimeError(f"HTTP 요청 실패 (상태 코드: {response.getcode()})")
        raw_bytes = response.read()
        return raw_bytes.decode("utf-8", errors="replace")


def extract_last_page_number(html_text: str) -> int:
    """
    수신된 HTML의 페이징 네비게이션 영역을 분석하여 전체 마지막 페이지 번호를 추출합니다.

    다음 3단계 우선순위에 따라 마지막 페이지 번호를 탐색합니다:
    1. '끝' 페이지 바로가기 버튼의 title 속성값 (class="...end..." title="N")
    2. 페이징 자바스크립트 함수 changeBestSellerParam(this, N)의 전달 인자 중 최댓값
    3. 일반 페이지 번호 태그(<a class="num" title="N">) 중 최댓값

    Args:
        html_text (str): 1페이지 또는 페이징 영역이 포함된 HTML 소스 코드.

    Returns:
        int: 추출된 마지막 페이지 번호. 페이징 정보를 찾을 수 없는 경우 기본값 1 반환.
    """
    # 1. '끝' 버튼에서 추출: class="...end..." title="12"
    end_m = re.search(r'class="[^"]*end[^"]*"[^>]*title="(\d+)"', html_text)
    if end_m:
        return int(end_m.group(1))
        
    # 2. changeBestSellerParam 함수 호출 인자 중 최대 번호 추출
    nums = re.findall(r'changeBestSellerParam\(this,\s*(\d+)\)', html_text)
    if nums:
        return max(map(int, nums))
        
    # 3. title 속성의 페이지 번호들 중 최대값
    page_titles = re.findall(r'<a[^>]*class="num"[^>]*title="(\d+)"', html_text)
    if page_titles:
        return max(map(int, page_titles))
        
    return 1


def parse_bestseller_books(html_text: str) -> list[dict]:
    """
    수신된 HTML 응답 문자열에서 도서별 상세 정보 블록을 파싱하여 딕셔너리 리스트로 반환합니다.

    각 도서 항목(`<li>` 태그) 내의 정규식 패턴 매칭 및 내부 JSON 옵션 객체(`ORD_GOODS_OPT`)를
    결합 분석하여 다음 18개 메타데이터 항목을 추출합니다:
    - 순위(rank), 상품번호(goods_no), 제목(title), 부제(subtitle)
    - 저자(author), 출판사(publisher), 출간일(pub_date), 카테고리(category)
    - 정가(fixed_price), 판매가(sale_price), 할인율(discount_rate), 포인트(point)
    - 별점(rating), 리뷰수(review_count), 판매지수(sales_index), 태그(tags)
    - 상세 URL(url), 표지 이미지 URL(image_url)

    Args:
        html_text (str): 비동기 엔드포인트로부터 수신된 HTML 소스.

    Returns:
        list[dict]: 각 도서의 메타데이터가 담긴 딕셔너리 리스트.
    """
    # 각 도서 아이템 블록 분리 (<li ... data-goods-no="..."> 단위)
    blocks = re.split(r'(?=<li[^>]*data-goods-no="\d+")', html_text)
    book_blocks = [b for b in blocks if re.search(r'^<li[^>]*data-goods-no="\d+"', b.strip())]
    
    books = []
    
    for idx, block in enumerate(book_blocks, start=1):
        # 1. 상품 번호 (goods_no)
        goods_no_m = re.search(r'data-goods-no="(\d+)"', block)
        goods_no = goods_no_m.group(1) if goods_no_m else ""
        
        # 2. ORD_GOODS_OPT JSON 옵션 데이터 추출 (상세 가격, 도서명, 카테고리 등이 포함됨)
        json_data = {}
        opt_m = re.search(r'name="ORD_GOODS_OPT"[^>]*value="([^"]+)"', block)
        if not opt_m and goods_no:
            opt_m = re.search(r'id="ordOpt_' + goods_no + r'"[^>]*value="([^"]+)"', block)
            
        if opt_m:
            try:
                raw_opt = html.unescape(opt_m.group(1))
                json_data = json.loads(raw_opt)
            except Exception:
                pass
                
        # 3. 순위 (rank)
        rank_m = re.search(r'<em class="ico rank">(\d+)</em>', block)
        rank = int(rank_m.group(1)) if rank_m else idx
        
        # 4. 도서명 (title)
        raw_title = json_data.get("goods_name", "")
        if not raw_title:
            title_m = re.search(r'<a class="gd_name"[^>]*>(.*?)</a>', block, re.DOTALL)
            raw_title = title_m.group(1) if title_m else ""
        title = clean_text(raw_title)
        
        # 5. 부제/도서설명 (subtitle)
        subtitle_m = re.search(r'<span class="gd_nameE">(.*?)</span>', block, re.DOTALL)
        subtitle = clean_text(subtitle_m.group(1)) if subtitle_m else ""
        
        # 6. 저자 (author)
        auth_m = re.search(r'<span class="authPub info_auth"[^>]*>(.*?)</span>', block, re.DOTALL)
        if auth_m:
            author = clean_text(auth_m.group(1))
        else:
            raw_auth = json_data.get("goodsAuth", "")
            author = clean_text(re.sub(r"[<>]", "", raw_auth))
            
        # 7. 출판사 (publisher)
        pub_m = re.search(r'<span class="authPub info_pub"[^>]*>(.*?)</span>', block, re.DOTALL)
        publisher = clean_text(pub_m.group(1)) if pub_m else ""
        
        # 8. 출판일 (pub_date)
        date_m = re.search(r'<span class="authPub info_date">(.*?)</span>', block, re.DOTALL)
        pub_date = clean_text(date_m.group(1)) if date_m else ""
        
        # 9. 카테고리 (category)
        category = clean_text(json_data.get("goodsSortNm", ""))
        
        # 10. 가격 정보
        # 정가 (fixed_price)
        if "shopPrice" in json_data and json_data["shopPrice"] is not None:
            fixed_price = int(float(json_data["shopPrice"]))
        else:
            fixed_m = re.search(r'<span class="txt_num dash"><em class="yes_m">([\d,]+)</em>원</span>', block)
            fixed_price = int(fixed_m.group(1).replace(",", "")) if fixed_m else 0
            
        # 판매가 (sale_price)
        if "salePrice" in json_data and json_data["salePrice"] is not None:
            sale_price = int(float(json_data["salePrice"]))
        else:
            sale_m = re.search(r'<strong class="txt_num"><em class="yes_b">([\d,]+)</em>원</strong>', block)
            sale_price = int(sale_m.group(1).replace(",", "")) if sale_m else 0
            
        # 할인율 (discount_rate)
        disc_m = re.search(r'<span class="txt_sale"><em class="num">(\d+)</em>%</span>', block)
        discount_rate = int(disc_m.group(1)) if disc_m else 0
        if discount_rate == 0 and fixed_price > 0 and sale_price > 0 and fixed_price > sale_price:
            discount_rate = round((fixed_price - sale_price) / fixed_price * 100)
            
        # 포인트 적립액 (point)
        point_m = re.search(r'<span class="yPoint">.*?포인트적립</em>\s*([\d,]+)\s*원', block, re.DOTALL)
        point = int(point_m.group(1).replace(",", "")) if point_m else 0
        
        # 11. 평점 (rating)
        rating_m = re.search(r'<span class="rating_grade">.*?<em class="yes_b">([\d.]+)</em>', block, re.DOTALL)
        rating = float(rating_m.group(1)) if rating_m else 0.0
        
        # 12. 리뷰 수 (review_count)
        review_m = re.search(r'<span class="rating_rvCount">.*?<em class="txC_blue">([\d,]+)</em>', block, re.DOTALL)
        review_count = int(review_m.group(1).replace(",", "")) if review_m else 0
        
        # 13. 판매지수 (sales_index)
        sales_m = re.search(r'class="saleNum"[^>]*>[\s\S]*?판매지수\s*([\d,]+)', block)
        sales_index = int(sales_m.group(1).replace(",", "")) if sales_m else 0
        
        # 14. 태그 (tags)
        tag_items = re.findall(r'<span class="tag">\s*<a[^>]*>(#[^<]+)</a>', block)
        tags = ", ".join(tag_items)
        
        # 15. 도서 상세 페이지 URL
        goods_url = f"https://www.yes24.com/product/goods/{goods_no}" if goods_no else ""
        
        # 16. 도서 표지 이미지 URL (지연 로딩 data-original 및 일반 src 대응)
        img_m = re.search(r'<img[^>]*class="lazy"[^>]*data-original="([^"]+)"', block)
        if not img_m:
            img_m = re.search(r'<img[^>]*data-original="([^"]+)"', block)
        if not img_m:
            img_m = re.search(r'<img[^>]*src="([^"]+)"', block)
        image_url = img_m.group(1) if img_m else ""
        
        book = {
            "rank": rank,
            "goods_no": goods_no,
            "title": title,
            "subtitle": subtitle,
            "author": author,
            "publisher": publisher,
            "pub_date": pub_date,
            "category": category,
            "fixed_price": fixed_price,
            "sale_price": sale_price,
            "discount_rate": discount_rate,
            "point": point,
            "rating": rating,
            "review_count": review_count,
            "sales_index": sales_index,
            "tags": tags,
            "url": goods_url,
            "image_url": image_url
        }
        books.append(book)
        
    return books


def load_existing_goods_nos(csv_filepath: str) -> set[str]:
    """
    지정된 CSV 파일에서 이미 수집된 도서의 상품 번호(goods_no) 집합(Set)을 로드합니다.

    수집 작업 재개 시 중복 요청 및 중복 저장을 방지하기 위해 사용됩니다.
    파일이 존재하지 않는 경우 빈 집합을 반환합니다.

    Args:
        csv_filepath (str): 확인할 대상 CSV 파일 경로.

    Returns:
        set[str]: 기수집된 goods_no 문자열들의 집합.
    """
    existing_ids = set()
    if not os.path.exists(csv_filepath):
        return existing_ids
        
    try:
        with open(csv_filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                g_no = row.get("goods_no")
                if g_no:
                    existing_ids.add(g_no.strip())
    except Exception as e:
        print(f"[알림] 기존 CSV 파일 읽기 중 참고: {e}")
        
    return existing_ids


def append_books_to_csv(books: list[dict], output_filepath: str) -> int:
    """
    수집된 도서 딕셔너리 리스트를 CSV 파일 끝에 추가(Append) 저장합니다.

    파일이 존재하지 않거나 비어있는 경우 디렉토리를 생성하고 CSV 헤더(BOM UTF-8)를 자동 작성합니다.
    기존 데이터가 있을 경우 헤더 없이 데이터 레코드만 추가합니다.

    Args:
        books (list[dict]): 저장할 도서 정보 딕셔너리 리스트.
        output_filepath (str): 저장할 대상 CSV 파일 경로.

    Returns:
        int: CSV 파일에 성공적으로 추가된 도서 수.
    """
    if not books:
        return 0
        
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    file_exists = os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 0
    
    with open(output_filepath, "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerows(books)
        
    return len(books)


def scrape_all_pages(output_csv: str = os.path.join("yes24", "data", "yes24_day_bestseller.csv")) -> None:
    """
    1페이지부터 마지막 페이지까지 순차적으로 베스트셀러를 크롤링하고 CSV에 저장합니다.

    [상세 동작 흐름]
    1. 대상 CSV 파일에서 이미 저장된 도서(goods_no) 목록을 조회합니다.
    2. 1페이지를 먼저 요청하여 전체 페이지 수를 파악하고, 시작 페이지 번호를 결정합니다.
    3. 각 페이지마다 0.1~0.5초 사이의 랜덤 지연 시간(Sleep)을 두어 서버 과부하를 방지합니다.
    4. 페이지를 요청하여 파싱한 뒤, 기존 목록에 없는 신규 도서만 필터링하여 CSV에 추가합니다.
    5. 마지막 페이지 도달 또는 순환 현상(1위 도서 재등장) 감지 시 자동으로 크롤링을 종료합니다.

    Args:
        output_csv (str, optional): 수집 결과를 저장할 CSV 상대 경로
            (기본값: 'yes24/data/yes24_day_bestseller.csv').
    """
    print("=" * 70)
    print("yes24 일별 베스트셀러 전 페이지 수집 시작")
    print(f"시작 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 1. 기존 CSV 파일에 저장된 도서 확인
    existing_goods_nos = load_existing_goods_nos(output_csv)
    initial_count = len(existing_goods_nos)
    print(f"[기존 데이터] 현재 CSV에 저장된 도서 수: {initial_count}권")
    
    # 2. 1페이지를 먼저 조회하여 전체 마지막 페이지 번호 파악
    print("\n[페이지 1 정보 확인]")
    p1_html = fetch_bestseller_html(page_number=1, page_size=24)
    total_pages = extract_last_page_number(p1_html)
    print(f"[페이징 감지] 전체 페이지 수: {total_pages} 페이지")
    
    # 만약 기존 파일이 비어있다면 1페이지 데이터도 저장 필요
    start_page = 1
    if initial_count >= 24:
        # 이미 1페이지 이상이 수집되어 있으므로 누적 수량 기준 시작 페이지 계산
        start_page = (initial_count // 24) + 1
        print(f"[이어서 수집] 기존에 {initial_count}권이 수집되어 있어 {start_page}페이지부터 수집을 시작합니다.")
    else:
        # 기존 1페이지가 불완전하거나 없으면 1페이지부터 수집
        p1_books = parse_bestseller_books(p1_html)
        # 중복 제외 필터링
        new_p1_books = [b for b in p1_books if b["goods_no"] not in existing_goods_nos]
        if new_p1_books:
            append_books_to_csv(new_p1_books, output_csv)
            for b in new_p1_books:
                existing_goods_nos.add(b["goods_no"])
            print(f"[1페이지 저장] 1페이지 {len(new_p1_books)}권 추가 완료")
        start_page = 2
        
    total_newly_collected = 0
    
    # 3. 2페이지부터 마지막 페이지까지 순회 수집
    for current_page in range(start_page, total_pages + 1):
        # 0.1 ~ 0.5초 사이 랜덤 딜레이 적용 (서버 부하 및 차단 방지)
        sleep_sec = round(random.uniform(0.1, 0.5), 3)
        time.sleep(sleep_sec)
        
        print(f"\n[페이지 {current_page}/{total_pages}] 요청 중... (이전 대기: {sleep_sec}초)")
        
        try:
            page_html = fetch_bestseller_html(page_number=current_page, page_size=24)
            page_books = parse_bestseller_books(page_html)
        except Exception as e:
            print(f"[오류 발생] {current_page}페이지 수집 중 에러: {e}")
            continue
            
        if not page_books:
            print(f"[수집 종료] {current_page}페이지에 더 이상 도서가 없습니다.")
            break
            
        # 순환 방지 체크: 첫 번째 도서의 순위가 1위로 되돌아가는 경우 마지막 페이지 초과임
        if current_page > 1 and page_books[0]["rank"] == 1:
            print(f"[순환 감지] {current_page}페이지에서 다시 1위로 돌아와 수집을 종료합니다.")
            break
            
        # 기존에 없는 도서만 필터링 (중복 방지)
        new_books = [b for b in page_books if b["goods_no"] not in existing_goods_nos]
        
        if new_books:
            added_cnt = append_books_to_csv(new_books, output_csv)
            for b in new_books:
                existing_goods_nos.add(b["goods_no"])
            total_newly_collected += added_cnt
            print(f"  -> {added_cnt}권 추가 완료! (순위: {new_books[0]['rank']}위 ~ {new_books[-1]['rank']}위 | 누적: {len(existing_goods_nos)}권)")
        else:
            print(f"  -> {current_page}페이지의 모든 도서가 이미 수집되어 있습니다.")
            
    print("\n" + "=" * 70)
    print("전체 베스트셀러 수집 작업 완료")
    print(f"새로 수집된 도서: {total_newly_collected}권")
    print(f"최종 CSV 도서 수: {len(existing_goods_nos)}권")
    print(f"저장 파일: {output_csv}")
    print(f"완료 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


if __name__ == "__main__":
    scrape_all_pages()
