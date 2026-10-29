# -*- coding: utf-8 -*-
"""
충북 청주시 청원구 오창읍 원룸 및 빌라 월세 매물 전수 수집 스크립트 (개선판)
- 배치 크기: 정확히 15개 (직방 API 최대 한도 15개 완벽 준수)
- 오창 1산단, 2산단, 중심상업지구, 구시가지 등 10대 거점 정밀 스캔
- 월세 매물 전수 수집 및 종합 주거 가성비 파생변수 산출
- UTF-8-SIG CSV 및 원천 JSON 저장
"""

import asyncio
import csv
import json
import os
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 오창읍 바운딩 박스 (위도 36.660 ~ 36.775, 경도 127.370 ~ 127.495)
OCHANG_LAT_MIN = 36.660
OCHANG_LAT_MAX = 36.775
OCHANG_LNG_MIN = 127.370
OCHANG_LNG_MAX = 127.495

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def clean_int(val, default=0):
    if val is None or val == "":
        return default
    try:
        if isinstance(val, (int, float)):
            return int(val)
        val_str = re.sub(r"[^\d\-]", "", str(val))
        return int(val_str) if val_str else default
    except Exception:
        return default


def clean_float(val, default=0.0):
    if val is None or val == "":
        return default
    try:
        if isinstance(val, (int, float)):
            return float(val)
        val_str = re.sub(r"[^\d\.\-]", "", str(val))
        return float(val_str) if val_str else default
    except Exception:
        return default


def fetch_detailed_items_batch(item_ids, batch_size=15):
    """POST /house/property/v1/items/list 배치 호출 (직방 최대 한도 15개 완벽 준수)"""
    url = "https://apis.zigbang.com/house/property/v1/items/list"
    all_details = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.zigbang.com",
        "Referer": "https://www.zigbang.com/"
    }

    total_chunks = (len(item_ids) + batch_size - 1) // batch_size
    print(f"[*] 총 {len(item_ids)}개 매물 상세 정보 수집 시작 ({total_chunks}개 배치, 배치당 {batch_size}개)...")

    for idx, i in enumerate(range(0, len(item_ids), batch_size), start=1):
        chunk = item_ids[i:i + batch_size]
        payload = json.dumps({"itemIds": chunk}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=headers)
        
        for retry in range(3):
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    items = res_data.get("items", [])
                    all_details.extend(items)
                    break
            except Exception as e:
                time.sleep(1.0 + retry)

        if idx % 5 == 0 or idx == total_chunks:
            print(f"    - [{idx}/{total_chunks} 배치 완료] 현재까지 수집된 상세 매물: {len(all_details)}건")

        time.sleep(0.3)

    return all_details


async def collect_ochang_item_ids():
    """Playwright로 직방 빌라 및 원룸 지도에서 오창읍 매물 ID 전수 탐색"""
    collected_id_map = {}  # {item_id: {'lat': ..., 'lng': ...}}

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=EDGE_PATH, headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        async def on_response(response):
            url = response.url
            if response.status == 200 and any(k in url for k in ["items/villas?", "items/onerooms?"]):
                try:
                    data = await response.json()
                    items = data.get("items", [])
                    for it in items:
                        iid = it.get("id")
                        lat = it.get("lat")
                        lng = it.get("lng")
                        if iid and lat and lng:
                            # 오창읍 바운딩 박스 내 매물만 등록
                            if (OCHANG_LAT_MIN <= lat <= OCHANG_LAT_MAX) and (OCHANG_LNG_MIN <= lng <= OCHANG_LNG_MAX):
                                collected_id_map[iid] = {"lat": lat, "lng": lng}
                except Exception:
                    pass

        page.on("response", on_response)

        # 오창읍 10대 거점 좌표 목록
        target_centers = [
            ("오창 1산단 양청리 호수공원 상권", 36.7119, 127.428, 15),
            ("오창 1산단 양청리 북부 주거단지", 36.7180, 127.432, 16),
            ("오창 구룡리 구시가지 중심상권", 36.7145, 127.417, 16),
            ("오창 구룡리 남부 원룸단지", 36.7090, 127.415, 16),
            ("오창 각리 과학산업단지 배후", 36.7080, 127.435, 16),
            ("오창 각리 주거단지 남부", 36.7020, 127.438, 16),
            ("오창 2산단 주성리 신흥 주거단지", 36.7280, 127.445, 16),
            ("오창 2산단 송대리/창리 산업벨트", 36.7380, 127.440, 15),
            ("오창 읍사무소/창리 일대", 36.7350, 127.450, 15),
            ("오창읍 전체 광역 뷰", 36.7150, 127.430, 13),
        ]

        # 1. 빌라/다세대/다가구 맵 탐색
        print("\n=== [1단계] 빌라/다세대/다가구 지도 정밀 스캔 ===")
        for name, lat, lng, zoom in target_centers:
            url = f"https://www.zigbang.com/home/villa/map?lat={lat}&lng={lng}&zoom={zoom}"
            try:
                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)
                await page.mouse.move(800, 500)
                for _ in range(4):
                    await page.mouse.wheel(0, 800)
                    await page.wait_for_timeout(300)
                print(f"  - [{name}] 누적 오창읍 매물 ID: {len(collected_id_map)}개")
            except Exception as e:
                print(f"  [!] 빌라 맵 에러 ({name}): {e}")

        # 2. 원룸 맵 탐색
        print("\n=== [2단계] 원룸 지도 정밀 스캔 ===")
        for name, lat, lng, zoom in target_centers:
            url = f"https://www.zigbang.com/home/oneroom/map?lat={lat}&lng={lng}&zoom={zoom}"
            try:
                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)
                await page.mouse.move(800, 500)
                for _ in range(4):
                    await page.mouse.wheel(0, 800)
                    await page.wait_for_timeout(300)
                print(f"  - [{name}] 누적 오창읍 매물 ID: {len(collected_id_map)}개")
            except Exception as e:
                print(f"  [!] 원룸 맵 에러 ({name}): {e}")

        # 3. 검색창을 통한 추가 매물 누락 방지
        for term in ["오창읍", "오창 양청리", "오창 구룡리", "오창 각리", "오창 2산단"]:
            try:
                search_input = page.locator("input[placeholder*='검색']").first
                if await search_input.is_visible():
                    await search_input.click()
                    await search_input.fill(term)
                    await page.wait_for_timeout(800)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(2500)
                    await page.mouse.move(400, 500)
                    for _ in range(3):
                        await page.mouse.wheel(0, 1000)
                        await page.wait_for_timeout(400)
            except Exception:
                pass

        await browser.close()

    print(f"\n[+] 오창읍 바운딩 박스 내 최종 발굴된 고유 매물 ID: {len(collected_id_map)}개")
    return list(collected_id_map.keys()), collected_id_map


def process_and_save_data(detailed_items, id_coord_map):
    """상세 매물 데이터를 월세 중심으로 필터링 및 파생변수 생성 후 UTF-8-SIG CSV로 저장"""
    today_str = datetime.now().strftime("%Y%m%d")
    out_csv = DATA_DIR / f"zigbang_daily_ochang_monthly_rent_{today_str}.csv"
    out_json = DATA_DIR / f"zigbang_ochang_raw_{today_str}.json"

    # 원천 JSON 저장
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(detailed_items, f, ensure_ascii=False, indent=2)

    rows = []
    skipped_not_rent = 0
    skipped_not_ochang = 0

    for item in detailed_items:
        sales_type = item.get("sales_type") or item.get("salesType") or ""
        # 1. 월세 매물만 엄격 필터링 (사용자 의사결정)
        if sales_type != "월세":
            skipped_not_rent += 1
            continue

        addr_info = item.get("addressOrigin") or {}
        local1 = addr_info.get("local1", "")
        local2 = addr_info.get("local2", "")
        local3 = addr_info.get("local3", "")
        full_text = addr_info.get("fullText", "") or item.get("address", "") or item.get("address1", "")
        title = item.get("title", "")
        desc = item.get("desc", "") or ""

        # 2. 오창읍 지리 검증
        loc = item.get("location") or item.get("random_location") or {}
        lat = clean_float(loc.get("lat") or id_coord_map.get(item.get("item_id"), {}).get("lat"))
        lng = clean_float(loc.get("lng") or id_coord_map.get(item.get("item_id"), {}).get("lng"))

        is_ochang_text = any(k in f"{local1} {local2} {local3} {full_text} {title}" for k in ["오창", "양청", "구룡", "각리", "창리", "주성리", "송대리", "괴정", "성산", "탑리", "복현"])
        is_ochang_coord = (OCHANG_LAT_MIN <= lat <= OCHANG_LAT_MAX) and (OCHANG_LNG_MIN <= lng <= OCHANG_LNG_MAX)

        if not (is_ochang_text or is_ochang_coord):
            skipped_not_ochang += 1
            continue

        # 세부 리(동) 구분
        sub_dong = "오창읍 기타"
        for candidate in ["양청리", "구룡리", "각리", "창리", "주성리", "송대리", "괴정리", "성산리", "탑리", "복현리"]:
            if candidate in f"{local3} {full_text} {title}":
                sub_dong = candidate
                break

        # 기본 수치 변수
        deposit = clean_int(item.get("deposit"), 0)          # 보증금 (만원)
        rent = clean_int(item.get("rent"), 0)                # 월세 (만원)
        manage_cost = clean_int(item.get("manage_cost"), 0)  # 관리비 (원 또는 만원)
        
        # 관리비 단위 정규화 (원 -> 만원)
        if manage_cost >= 1000:
            manage_cost_manwon = round(manage_cost / 10000, 1)
        else:
            manage_cost_manwon = float(manage_cost)

        # 실질 총 주거비용 (월세 + 관리비)
        total_monthly_cost = round(rent + manage_cost_manwon, 1)

        # 면적 (m2, 평)
        size_m2 = clean_float(item.get("size_m2"), 0.0)
        if size_m2 <= 0:
            size_dict = item.get("전용면적") or item.get("공급면적") or {}
            size_m2 = clean_float(size_dict.get("m2"), 0.0)
        size_pyeong = round(size_m2 / 3.30578, 1) if size_m2 > 0 else 0.0

        # 전용면적(평)당 실질 월 주거비용 (가성비 지수)
        cost_per_pyeong = round(total_monthly_cost / size_pyeong, 1) if size_pyeong > 0 else 0.0

        # 층수 정보
        floor_str = str(item.get("floor") or item.get("floor_string") or "")
        building_floor_str = str(item.get("building_floor") or "")
        current_floor = clean_int(floor_str, 0)
        max_floor = clean_int(building_floor_str, 0)

        # 층수 비율
        if max_floor > 0 and current_floor > 0:
            floor_ratio = round(current_floor / max_floor, 2)
            if floor_ratio <= 0.33:
                floor_category = "저층"
            elif floor_ratio <= 0.66:
                floor_category = "중층"
            else:
                floor_category = "고층"
        else:
            floor_ratio = 0.5
            floor_category = "중층"

        # 방 구조 및 룸 타입
        room_type = str(item.get("room_type") or item.get("room_type_title") or "")
        
        # 구조 정제
        structure_type = "원룸"
        if any(k in f"{title} {desc} {room_type}" for k in ["투룸", "2룸", "두룸"]):
            structure_type = "투룸"
        elif any(k in f"{title} {desc} {room_type}" for k in ["쓰리룸", "3룸", "세룸", "포룸"]):
            structure_type = "쓰리룸+"
        elif any(k in f"{title} {desc} {room_type}" for k in ["복층"]):
            structure_type = "복층형 원룸"
        elif any(k in f"{title} {desc} {room_type}" for k in ["분리형", "1.5룸", "주방분리"]):
            structure_type = "1.5룸/분리형"
        elif any(k in f"{title} {desc} {room_type}" for k in ["오픈형"]):
            structure_type = "오픈형 원룸"

        # 풀옵션 스코어
        option_keywords = ["에어컨", "세탁기", "냉장고", "인덕션", "가스레인지", "전자레인지", "침대", "TV", "옷장", "붙박이장", "신발장", "도어락"]
        tags = item.get("tags") or []
        text_for_options = f"{title} {desc} {' '.join(tags)}"
        option_count = sum(1 for kw in option_keywords if kw in text_for_options)
        has_full_option = 1 if option_count >= 4 or "풀옵션" in text_for_options else 0

        # 엘리베이터 여부
        has_elevator = 1 if "엘리베이터" in text_for_options or "승강기" in text_for_options else 0
        # 주차 가능 여부
        parking = 1 if "주차" in text_for_options else 0

        # 등록일
        reg_date = str(item.get("reg_date") or "")[:10]

        row = {
            "item_id": item.get("item_id"),
            "region_gu": "청주시 청원구",
            "region_dong": "오창읍",
            "sub_dong": sub_dong,
            "sales_type": "월세",
            "structure_type": structure_type,
            "deposit_manwon": deposit,
            "rent_manwon": rent,
            "manage_cost_manwon": manage_cost_manwon,
            "total_monthly_cost": total_monthly_cost,
            "size_m2": size_m2,
            "size_pyeong": size_pyeong,
            "cost_per_pyeong": cost_per_pyeong,
            "current_floor": current_floor,
            "max_floor": max_floor,
            "floor_category": floor_category,
            "has_full_option": has_full_option,
            "option_score": option_count,
            "has_elevator": has_elevator,
            "parking_available": parking,
            "latitude": lat,
            "longitude": lng,
            "title": title.strip().replace("\n", " "),
            "address_full": full_text.strip(),
            "reg_date": reg_date,
            "thumbnail_url": item.get("images_thumbnail") or ""
        }
        rows.append(row)

    # 중복 제거 (item_id 기준)
    unique_rows = {}
    for r in rows:
        unique_rows[r["item_id"]] = r
    final_rows = list(unique_rows.values())

    # CSV 저장 (UTF-8-SIG)
    if final_rows:
        fieldnames = list(final_rows[0].keys())
        with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_rows)

    print(f"\n==========================================")
    print(f"[+] 수집 결과 요약:")
    print(f"    - 수신된 상세 매물 총수: {len(detailed_items)}건")
    print(f"    - 비월세(전세/매매) 제외: {skipped_not_rent}건")
    print(f"    - 오창읍 외 지역 제외: {skipped_not_ochang}건")
    print(f"    - 최종 정제된 오창읍 월세 매물수: {len(final_rows)}건")
    print(f"    - CSV 저장 경로: {out_csv}")
    print(f"==========================================\n")

    return out_csv, len(final_rows)


async def main():
    print("[*] 오창읍 원룸/빌라 월세 데이터 수집 파이프라인 가동...")
    item_ids, id_coord_map = await collect_ochang_item_ids()
    if not item_ids:
        print("[!] 발굴된 매물 ID가 없습니다.")
        return

    detailed_items = fetch_detailed_items_batch(item_ids, batch_size=15)
    process_and_save_data(detailed_items, id_coord_map)


if __name__ == "__main__":
    asyncio.run(main())
