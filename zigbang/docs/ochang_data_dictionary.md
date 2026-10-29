# 📖 [데이터 사전] 오창읍 원룸·빌라 월세 데이터셋 스키마 명세

> **파일명**: `zigbang_daily_ochang_monthly_rent_20261029.csv`  
> **총 관측치**: 603행  
> **총 변수**: 26개 열  
> **인코딩**: UTF-8-SIG  
> **결측률**: 0.0% (결측치 0건)  

---

## 변수별 상세 명세 (26개 필드)

| No | 컬럼명 | 데이터 타입 | 설명 | 예시값 | 산출 공식 및 로직 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `item_id` | Integer | 직방 고유 매물 식별자 (PK) | `50855368` | 직방 시스템 원천 식별 번호 |
| 2 | `region_gu` | String | 상위 자치구 명칭 | `청주시 청원구` | 행정구역 분류 |
| 3 | `region_dong` | String | 읍/면/동 명칭 | `오창읍` | 법정동 기준 |
| 4 | `sub_dong` | String | 오창읍 세부 권역(리) | `양청리`, `구룡리` | 주소 및 텍스트 파싱 매핑 |
| 5 | `sales_type` | String | 거래 유형 | `월세` | 사용자 요구사항 필터링 (월세 100%) |
| 6 | `structure_type` | String | 방 구조 유형 | `원룸`, `투룸` | 원룸, 1.5룸, 투룸, 쓰리룸+, 복층 등 |
| 7 | `deposit_manwon` | Integer | 보증금 (단위: 만원) | `300` | 원천 매물 보증금 |
| 8 | `rent_manwon` | Integer | 순수 월세 (단위: 만원) | `35` | 원천 매물 월 임대료 |
| 9 | `manage_cost_manwon` | Float | 월 관리비 (단위: 만원) | `10.0` | 원천 원 단위를 만원 단위로 정규화 |
| 10 | `total_monthly_cost` | Float | 실질 총 주거비용 (단위: 만원) | `45.0` | `rent_manwon + manage_cost_manwon` |
| 11 | `size_m2` | Float | 전용면적 (단위: ㎡) | `33.0` | 실거주 전용면적 |
| 12 | `size_pyeong` | Float | 전용면적 (단위: 평) | `10.0` | `round(size_m2 / 3.30578, 1)` |
| 13 | `cost_per_pyeong` | Float | 평당 실질 주거비 (가성비 지수) | `4.5` | `round(total_monthly_cost / size_pyeong, 1)` |
| 14 | `current_floor` | Integer | 해당 매물 해당층 | `3` | 정수형 정제 (저/중/고 수치 변환) |
| 15 | `max_floor` | Integer | 건물의 총 층수 | `4` | 정수형 정제 |
| 16 | `floor_category` | String | 층수 구간 카테고리 | `중층` | 층수 비율(저층 <=0.33, 중층 <=0.66, 고층) |
| 17 | `has_full_option` | Integer | 풀옵션 여부 (0/1) | `1` | 필수 가전 4종 이상 보유 여부 |
| 18 | `option_score` | Integer | 옵션 보유 개수 점수 | `7` | 에어컨, 세탁기, 냉장고, TV 등 매칭 개수 |
| 19 | `has_elevator` | Integer | 승강기(엘리베이터) 여부 | `0` | 엘리베이터 키워드 탐지 |
| 20 | `parking_available` | Integer | 주차 가능 여부 (0/1) | `1` | 주차 키워드 탐지 |
| 21 | `latitude` | Float | 매물 위도 (Latitude) | `36.7125` | WGS84 좌표 |
| 22 | `longitude` | Float | 매물 경도 (Longitude) | `127.4281` | WGS84 좌표 |
| 23 | `title` | String | 직방 매물 홍보 제목 | `양청리 풀옵션 원룸` | 개행 및 특수문자 정제 |
| 24 | `address_full` | String | 매물 상세 소재지 지번 | `충북 청주시 청원구 오창읍...` | 직방 지번 주소 |
| 25 | `reg_date` | String | 매물 등록 일자 | `2026-10-25` | YYYY-MM-DD 포맷 |
| 26 | `thumbnail_url` | String | 대표 이미지 썸네일 URL | `https://ic.zigbang.com/...` | 직방 이미지 CDN 링크 |
