# 스타벅스 전국 매장 데이터 수집 및 엔드투엔드 파이프라인 구축 계획서

## 1. 개요 및 수집 목표
- **대상 사이트**: 스타벅스 코리아 공식 매장 찾기 ([https://www.starbucks.co.kr/store/store_map.do](https://www.starbucks.co.kr/store/store_map.do))
- **수집 방식**: 웹 브라우저 대신 초고속 내부 Gateway API(`https://www.starbucks.co.kr/store/getStore.do`) 직접 호출 (REST API 역공학)
- **전략**: 
  1. **Phase 1 (1차 검증)**: 서울 지역 매장(약 710여 개) 우선 수집 및 데이터 무결성 검증
  2. **Phase 2 (2차 본수집)**: 검증 통과 후 전국 17개 시도 전체 매장(약 2,210여 개) 일괄 전수 수집
- **최종 산출물**:
  - `starbucks/data/starbucks_seoul_{YYYYMMDD}.csv` (1차 서울 검증 데이터, UTF-8-SIG)
  - `starbucks/data/starbucks_national_{YYYYMMDD}.csv` (2차 전국 통합 데이터, UTF-8-SIG)
  - `starbucks/src/scraper.py` (API 크롤러 및 자동 검증 스크립트)
  - `starbucks/reports/EDA_Report.md` 및 `starbucks/images/*.png` (10종 차트 심층 EDA 분석)
  - `starbucks/dashboard.html` (글래스모피즘 인터랙티브 웹 대시보드)

---

## 2. API 기술 명세 및 파라미터 구조

### 2.1 엔드포인트 사양
- **URL**: `https://www.starbucks.co.kr/store/getStore.do?r=2G30D88Z8X`
- **HTTP Method**: `POST`
- **Request Headers**:
  ```http
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
  Content-Type: application/x-www-form-urlencoded; charset=UTF-8
  X-Requested-With: XMLHttpRequest
  ```

### 2.2 요청 페이로드 (Form-encoded)
| 파라미터 | 서울 수집값 (Phase 1) | 전국 수집값 (Phase 2) | 설명 |
| :--- | :--- | :--- | :--- |
| `p_sido_cd` | `01` | *(빈 문자열)* | 시도 코드 (`01`=서울, 비워두면 전국 전체 조회) |
| `p_gugun_cd` | *(빈 문자열)* | *(빈 문자열)* | 구군 코드 |
| `iend` | `1000` | `3000` | 조회 최대 건수 (전국 매장 수용용) |
| `search_type` | `C` | `C` | 지역/검색 구분 |
| `in_biz_cds` | `0` | `0` | 비즈니스 코드 |
| `in_scodes` | `0` | `0` | 매장 코드 |
| `ins_lat` | `37.56682` | `37.56682` | 기준 위도 |
| `ins_lng` | `126.97865` | `126.97865` | 기준 경도 |

---

## 3. 정제 스키마 및 가공 사양 (총 18개 핵심 필드)

API의 약 30개 원천 JSON 필드 중 분석 및 서비스에 필수적인 항목을 정제·파생 변수화합니다.

| 표준 컬럼명 | 원천 필드 | 데이터 타입 | 설명 및 정제/파생 로직 |
| :--- | :--- | :--- | :--- |
| `store_code` | `s_code` | string | 고유 매장 식별 코드 |
| `store_name` | `s_name` | string | 매장명 (공백 및 특수문자 정제) |
| `sido_code` | `sido_code` | string | 시/도 행정구역 코드 (예: `01`, `02`) |
| `sido_name` | `sido_name` | string | 시/도 명칭 (예: `서울`, `경기`, `부산`) |
| `gugun_code` | `gugun_code` | string | 구/군 행정구역 코드 (예: `0101`) |
| `gugun_name` | `gugun_name` | string | 구/군 명칭 (예: `강남구`, `종로구`) |
| `doro_address` | `doro_address` | string | 도로명 기본 주소 |
| `jibun_address` | `addr` | string | 지번 기본 주소 |
| `latitude` | `lat` | float | 위도 (WGS84, 33.0 ~ 39.0 검증) |
| `longitude` | `lot` | float | 경도 (WGS84, 124.0 ~ 132.0 검증) |
| `tel` | `tel` | string | 매장 대표 전화번호 |
| `open_date` | `open_dt` | string | 개점일자 (`YYYYMMDD` -> `YYYY-MM-DD`) |
| `business_years` | *(파생)* | float | 개점일 기준 운영 연수 (`round((현재 - 개점일)/365.25, 1)`) |
| `is_new` | `new_state` | boolean | 신규 매장 여부 (`Y`=True, `N`=False) |
| `is_drive_thru` | `theme_state` | boolean | 드라이브 스루(DT) 매장 여부 (`T01` 등 DT 코드 포함 여부) |
| `is_reserve` | `theme_state` | boolean | 스타벅스 리저브(Reserve) 매장 여부 (`T03` 등 포함) |
| `is_delivers` | `theme_state` | boolean | 딜리버스(배달 서비스) 매장 여부 (`T43` 등 포함) |
| `default_image` | `defaultimage` | string | 매장 대표 이미지 절대 URL 경로 |

---

## 4. 데이터 무결성 검증 기준 (Automated Validation)

수집 직후 스크립트 내에서 다음 항목을 엄격히 자동 검증합니다:
1. **건수 정합성**:
   - 서울: 최소 650개 이상 (현재 기준 약 710여 개)
   - 전국: 최소 2,000개 이상 (현재 기준 약 2,210여 개)
2. **결측치 검증**: 핵심 식별자(`store_code`, `store_name`, `latitude`, `longitude`, `doro_address`) 결측치율 **0.0%**
3. **좌표 유효성**:
   - 대한민국 위도 범위(`33.0 <= lat <= 39.0`) 이내
   - 대한민국 경도 범위(`124.0 <= lon <= 132.0`) 이내
4. **중복 검증**: `store_code` 기준 고유성 100% (중복 0건)
5. **인코딩 검증**: 엑셀 한글 깨짐 방지를 위한 **UTF-8-SIG (BOM)** 인코딩 적용

---

## 5. 단계별 실행 로드맵 (Action Steps)

- **Step 1**: `starbucks/src/scraper.py` 모듈 개발 (서울 수집 모드 및 전국 수집 모드)
- **Step 2**: 1차 서울 매장 데이터 수집 실행 -> `starbucks/data/starbucks_seoul_{YYYYMMDD}.csv` 생성 및 무결성 검증 보고서 출력
- **Step 3**: 1차 검증 확인 후 전국 17개 시도 전수 수집 실행 -> `starbucks/data/starbucks_national_{YYYYMMDD}.csv` 생성
- **Step 4**: `starbucks/reports/` 폴더 생성 및 10종 고해상도 시각화 차트(`starbucks/images/`)와 심층 EDA 리포트(`starbucks/reports/EDA_Report.md`) 작성
- **Step 5**: Single File HTML 기반 글래스모피즘 인터랙티브 대시보드(`starbucks/dashboard.html`) 제작 (전국 매장 지도, 지역별/타입별 통계, 실시간 필터/검색)
