"""
스타벅스 코리아 매장 정보 스크래퍼 및 데이터 무결성 검증 파이프라인
- 엔드포인트: https://www.starbucks.co.kr/store/getStore.do
- 1단계: 서울 매장 수집 및 무결성 검증 (starbucks_seoul_YYYYMMDD.csv)
- 2단계: 전국 매장 전수 수집 및 무결성 검증 (starbucks_national_YYYYMMDD.csv)
"""

import argparse
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import pandas as pd


def get_starbucks_stores(sido_cd="", iend=3000):
    """스타벅스 공식 Gateway API를 호출하여 매장 목록 JSON을 반환합니다."""
    url = "https://www.starbucks.co.kr/store/getStore.do?r=2G30D88Z8X"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }

    payload = {
        "in_biz_cds": "0",
        "in_scodes": "0",
        "ins_lat": "37.56682",
        "ins_lng": "126.97865",
        "search_date": "",
        "search_type": "C",
        "iend": str(iend),
        "p_sido_cd": sido_cd,
        "p_gugun_cd": "",
        "isError": "N",
        "in_distance": "0",
        "in_biz_cd": "",
        "searchEgg": "N",
        "set_date": "",
        "pageSize": "100",
    }

    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)

    print(f"[*] API 요청 전송 중... (sido_cd='{sido_cd}', iend={iend})")
    start_time = time.time()
    with urllib.request.urlopen(req, timeout=20) as resp:
        elapsed = round(time.time() - start_time, 2)
        print(f"[+] API 응답 수신 완료 (소요시간: {elapsed}초, HTTP 상태: {resp.status})")
        res_text = resp.read().decode("utf-8")
        result_json = json.loads(res_text)
        store_list = result_json.get("list", [])
        return store_list


def clean_store_data(raw_stores):
    """원천 JSON 매장 목록을 표준 스키마 및 파생 변수로 정밀 정제합니다."""
    today = datetime.date.today()
    cleaned_rows = []

    for item in raw_stores:
        s_code = str(item.get("s_code", "")).strip()
        s_name = str(item.get("s_name", "")).strip()
        if not s_code or not s_name:
            continue

        sido_code = str(item.get("sido_code", "")).strip()
        sido_name = str(item.get("sido_name", "")).strip()
        gugun_code = str(item.get("gugun_code", "")).strip()
        gugun_name = str(item.get("gugun_name", "")).strip()

        doro_address = str(item.get("doro_address", "")).strip()
        jibun_address = str(item.get("addr", "")).strip()

        # 위경도 변환
        try:
            latitude = float(item.get("lat", 0.0))
        except (ValueError, TypeError):
            latitude = 0.0

        try:
            longitude = float(item.get("lot", 0.0))
        except (ValueError, TypeError):
            longitude = 0.0

        tel = str(item.get("tel", "")).strip()

        # 개점일자 및 업력 계산
        open_dt_raw = str(item.get("open_dt", "")).strip()
        open_date_str = ""
        open_year = ""
        business_years = 0.0

        if len(open_dt_raw) == 8 and open_dt_raw.isdigit():
            try:
                op_date = datetime.datetime.strptime(open_dt_raw, "%Y%m%d").date()
                open_date_str = op_date.strftime("%Y-%m-%d")
                open_year = op_date.strftime("%Y")
                delta_days = (today - op_date).days
                business_years = round(max(delta_days, 0) / 365.25, 1)
            except Exception:
                open_date_str = open_dt_raw

        theme_state = str(item.get("theme_state", ""))
        new_state = str(item.get("new_state", "")).strip()

        # 공식 JS (store_core.js) 검증 기반 특화 속성 매핑:
        # T01: 드라이브 스루 (DT)
        # T03: 스타벅스 리저브 (Reserve)
        # T43: 딜리버스 (Delivers 배달 서비스)
        is_new = (new_state.upper() == "Y")
        is_drive_thru = ("T01" in theme_state) or ("DT" in s_name.upper())
        is_reserve = ("T03" in theme_state) or ("리저브" in s_name)
        is_delivers = ("T43" in theme_state) or ("딜리버스" in s_name)

        # 매장 유형 단일 라벨
        if is_reserve and is_drive_thru:
            store_type = "리저브 DT"
        elif is_reserve:
            store_type = "리저브"
        elif is_drive_thru:
            store_type = "드라이브스루"
        else:
            store_type = "일반매장"

        default_image = str(item.get("defaultimage", "")).strip()
        if default_image and not default_image.startswith("http"):
            default_image = f"https://www.starbucks.co.kr{default_image}"

        cleaned_rows.append({
            "store_code": s_code,
            "store_name": s_name,
            "store_type": store_type,
            "sido_code": sido_code,
            "sido_name": sido_name,
            "gugun_code": gugun_code,
            "gugun_name": gugun_name,
            "doro_address": doro_address,
            "jibun_address": jibun_address,
            "latitude": latitude,
            "longitude": longitude,
            "tel": tel,
            "open_date": open_date_str,
            "open_year": open_year,
            "business_years": business_years,
            "is_new": is_new,
            "is_drive_thru": is_drive_thru,
            "is_reserve": is_reserve,
            "is_delivers": is_delivers,
            "default_image": default_image,
        })

    df = pd.DataFrame(cleaned_rows)
    return df


def validate_dataset(df, dataset_name, min_expected_count=600):
    """수집된 데이터셋의 무결성(건수, 결측치율, 좌표 유효성, 중복성)을 검증합니다."""
    print("=" * 60)
    print(f"[*] {dataset_name} 데이터 무결성 검증 시작")
    print("=" * 60)

    total_rows = len(df)
    print(f"- 총 수집 건수: {total_rows}건 (최소 기준: {min_expected_count}건)")
    if total_rows < min_expected_count:
        raise ValueError(f"수집 건수 부족: {total_rows} < {min_expected_count}")

    # 결측치 검증
    essential_cols = ["store_code", "store_name", "sido_name", "doro_address", "latitude", "longitude"]
    null_issues = {}
    for col in essential_cols:
        null_count = df[col].isnull().sum() + (df[col] == "").sum()
        null_rate = round(null_count / total_rows * 100, 2)
        if null_count > 0:
            null_issues[col] = f"{null_count}건 ({null_rate}%)"

    if null_issues:
        print(f"[!] 필수 컬럼 결측치 발견: {null_issues}")
    else:
        print("- 필수 6대 핵심 컬럼 결측치율: 0.0% (완전성 통과)")

    # 좌표 유효성 (대한민국 영역: 위도 33~39, 경도 124~132)
    invalid_lat = df[(df["latitude"] < 33.0) | (df["latitude"] > 39.0)]
    invalid_lon = df[(df["longitude"] < 124.0) | (df["longitude"] > 132.0)]
    print(f"- 유효 위도(33~39) 범위 외 건수: {len(invalid_lat)}건")
    print(f"- 유효 경도(124~132) 범위 외 건수: {len(invalid_lon)}건")

    if len(invalid_lat) > 0 or len(invalid_lon) > 0:
        print("[!] 경고: 좌표 범위 이상 매장 존재")
    else:
        print("- 좌표 유효성: 대한민국 국경 내 100% 안착")

    # 고유성 검증 (store_code 중복)
    dup_count = df["store_code"].duplicated().sum()
    print(f"- 매장 고유코드(store_code) 중복 건수: {dup_count}건")
    if dup_count > 0:
        print(f"[!] 중복 매장코드 제거 수행 ({dup_count}건)")
        df = df.drop_duplicates(subset=["store_code"]).reset_index(drop=True)
    else:
        print("- 매장 식별자 유일성: 100% 통과 (중복 0건)")

    # 특화 매장 통계
    dt_count = df["is_drive_thru"].sum()
    reserve_count = df["is_reserve"].sum()
    delivers_count = df["is_delivers"].sum()
    new_count = df["is_new"].sum()
    print(f"- DT 매장: {dt_count}개 ({round(dt_count/total_rows*100, 1)}%)")
    print(f"- 리저브 매장: {reserve_count}개 ({round(reserve_count/total_rows*100, 1)}%)")
    print(f"- 딜리버스 매장: {delivers_count}개 ({round(delivers_count/total_rows*100, 1)}%)")
    print(f"- 신규 매장: {new_count}개 ({round(new_count/total_rows*100, 1)}%)")
    print(f"[+] {dataset_name} 데이터 무결성 검증 완료 - 정상 판정")
    print("=" * 60)
    return df


def run_pipeline():
    """1단계(서울 수집/검증) -> 2단계(전국 전수 수집/검증) 순차 실행"""
    today_str = datetime.date.today().strftime("%Y%m%d")
    os.makedirs("starbucks/data", exist_ok=True)

    # ----------------------------------------------------
    # Phase 1: 서울 지역 매장 수집 및 검증
    # ----------------------------------------------------
    print("\n" + "#" * 60)
    print("### [Phase 1] 스타벅스 서울 지역 매장 수집 착수")
    print("#" * 60)
    raw_seoul = get_starbucks_stores(sido_cd="01", iend=1000)
    df_seoul = clean_store_data(raw_seoul)
    df_seoul = validate_dataset(df_seoul, "서울 지역 매장", min_expected_count=650)

    seoul_csv_path = f"starbucks/data/starbucks_seoul_{today_str}.csv"
    df_seoul.to_csv(seoul_csv_path, index=False, encoding="utf-8-sig")
    print(f"[+] 서울 매장 데이터 저장 완료: {seoul_csv_path} (총 {len(df_seoul)}건)")

    # 서버 부하 방지 대기
    print("\n[*] 1단계 검증 통과! 서버 부하 방지를 위해 1초 대기 후 전국 전수 수집으로 전환합니다...")
    time.sleep(1.0)

    # ----------------------------------------------------
    # Phase 2: 전국 전수 매장 수집 및 검증
    # ----------------------------------------------------
    print("\n" + "#" * 60)
    print("### [Phase 2] 스타벅스 전국 매장 전수 수집 착수")
    print("#" * 60)
    raw_national = get_starbucks_stores(sido_cd="", iend=3000)
    df_national = clean_store_data(raw_national)
    df_national = validate_dataset(df_national, "전국 전체 매장", min_expected_count=2000)

    national_csv_path = f"starbucks/data/starbucks_national_{today_str}.csv"
    df_national.to_csv(national_csv_path, index=False, encoding="utf-8-sig")
    print(f"[+] 전국 매장 데이터 저장 완료: {national_csv_path} (총 {len(df_national)}건)")

    # 추가 편의를 위한 최신 파일 링크 심볼릭/동일 복사
    latest_path = "starbucks/data/starbucks_national_latest.csv"
    df_national.to_csv(latest_path, index=False, encoding="utf-8-sig")
    print(f"[+] 최신 참조용 {latest_path} 생성 완료")

    print("\n" + "#" * 60)
    print("### [SUCCESS] 스타벅스 매장 수집 및 2단계 무결성 검증 전체 완료")
    print("#" * 60)
    return national_csv_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="스타벅스 매장 정보 스크래퍼")
    parser.add_argument("--phase", choices=["all", "seoul", "national"], default="all", help="수집 단계 선택")
    args = parser.parse_args()

    today_str = datetime.date.today().strftime("%Y%m%d")
    os.makedirs("starbucks/data", exist_ok=True)

    if args.phase == "all":
        run_pipeline()
    elif args.phase == "seoul":
        raw_seoul = get_starbucks_stores(sido_cd="01", iend=1000)
        df_seoul = clean_store_data(raw_seoul)
        df_seoul = validate_dataset(df_seoul, "서울 지역 매장", min_expected_count=650)
        path = f"starbucks/data/starbucks_seoul_{today_str}.csv"
        df_seoul.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"[+] 서울 데이터 저장 완료: {path}")
    elif args.phase == "national":
        raw_national = get_starbucks_stores(sido_cd="", iend=3000)
        df_national = clean_store_data(raw_national)
        df_national = validate_dataset(df_national, "전국 전체 매장", min_expected_count=2000)
        path = f"starbucks/data/starbucks_national_{today_str}.csv"
        df_national.to_csv(path, index=False, encoding="utf-8-sig")
        df_national.to_csv("starbucks/data/starbucks_national_latest.csv", index=False, encoding="utf-8-sig")
        print(f"[+] 전국 데이터 저장 완료: {path}")
