# [Implementation Plan] 스타벅스 매장 데이터 수집 및 엔드투엔드 파이프라인 구축

스타벅스 코리아 공식 웹사이트([store_map.do](https://www.starbucks.co.kr/store/store_map.do))의 내부 REST API를 분석하여 서울 매장 1차 검증 후 전국 전수 수집(약 2,210개)을 완료하고, 심층 EDA 분석(10종 시각화, TF-IDF 키워드) 및 글래스모피즘 인터랙티브 웹 대시보드를 구축하는 엔드투엔드 파이프라인 계획입니다.

---

## 1. Goal Description
- **배경**: 스타벅스 매장 찾기 페이지(`store_map.do`)는 내부적으로 `https://www.starbucks.co.kr/store/getStore.do` 비동기 POST 엔드포인트를 호출하여 매장 정보를 수신합니다.
- **수집 전략**:
  - **Phase 1 (서울 검증)**: 서울 지역(`p_sido_cd=01`) 매장 약 710여 개를 우선 수집하여 데이터 필드 정합성, 결측치율(0%), 좌표 유효성을 검증합니다.
  - **Phase 2 (전국 전수 수집)**: 서울 데이터 검증 통과 시 전국 17개 시도 전체 매장 약 2,210여 개를 일괄 수집하여 `UTF-8-SIG` CSV로 저장합니다.
- **분석 및 대시보드**:
  - 10종 이상의 고해상도 차트와 2,000자 이상 비즈니스 인사이트를 담은 종합 EDA 리포트(`starbucks/reports/EDA_Report.md`) 발행
  - Chart.js v4 기반의 단일 파일(Single File HTML) 글래스모피즘 인터랙티브 웹 대시보드(`starbucks/dashboard.html`) 제작

---

## 2. User Review Required
> [!IMPORTANT]
> - **1차(서울) 검증 후 자동/수동 전환**: 1차 서울 수집 후 결측치 0%, 좌표 정상 범위(33~39, 124~132) 등 무결성 검증을 통과하면 즉시 전국 2차 수집으로 이어지도록 설계됩니다.
> - **의존성 패키지**: 공통 가상환경(`.venv`)에 `pandas`, `koreanize-matplotlib`, `matplotlib`, `scikit-learn`이 필요하며, 누락된 경우 `uv add`로 추가 설치합니다.

---

## 3. Open Questions
- 현재 질문 분기가 모두 해결되었으며, 사용자의 요청대로 모든 계획 문서는 `starbucks/docs/`에도 함께 보관됩니다.

---

## 4. Proposed Changes

### Component 1: 데이터 수집 및 무결성 검증 모듈 (`starbucks/src/scraper.py`)

#### [NEW] `starbucks/src/scraper.py`
- 스타벅스 공식 Gateway API(`https://www.starbucks.co.kr/store/getStore.do`) 연동
- 헤더 설정: `User-Agent`, `Content-Type: application/x-www-form-urlencoded; charset=UTF-8`, `X-Requested-With: XMLHttpRequest`
- 페이로드 제어:
  - Phase 1 (서울): `p_sido_cd=01`, `iend=1000`
  - Phase 2 (전국): `p_sido_cd=`, `iend=3000`
- 데이터 파싱 및 파생 변수 생성:
  - `store_code`, `store_name`, `sido_code`, `sido_name`, `gugun_code`, `gugun_name`
  - `doro_address`, `jibun_address`, `latitude`, `longitude`, `tel`, `open_date`
  - `business_years` (개점일 기준 운영 연수)
  - `is_new`, `is_drive_thru` (DT), `is_reserve` (리저브), `is_delivers` (딜리버스)
  - `default_image`
- 자동 무결성 검증 함수 (`validate_dataset`):
  - 건수 체크 (서울 >= 650, 전국 >= 2,000)
  - 결측치율 체크 (필수 5대 필드 결측치 0.0%)
  - 좌표 범위 체크 (위도 33.0~39.0, 경도 124.0~132.0)
  - 매장코드 고유성 검증 (중복 0건)
- 파일 저장:
  - 서울: `starbucks/data/starbucks_seoul_{YYYYMMDD}.csv` (`utf-8-sig`)
  - 전국: `starbucks/data/starbucks_national_{YYYYMMDD}.csv` (`utf-8-sig`)

---

### Component 2: 심층 탐색적 데이터 분석 모듈 (`starbucks/src/eda_analysis.py`)

#### [NEW] `starbucks/src/eda_analysis.py`
- `universal-pipeline.md` 및 `py-eda` 규칙을 준수한 자동 분석 스크립트
- `koreanize_matplotlib` 적용 (한글 폰트 완벽 지원, `sns.set_theme()` 사용 금지)
- 10종 이상의 고해상도(DPI 150) 차트 생성 (`starbucks/images/` 저장):
  1. `01_sido_store_distribution.png`: 전국 17개 시도별 매장 수 분포 (가로 막대)
  2. `02_seoul_gu_store_density.png`: 서울 25개 자치구별 매장 집중도 비교
  3. `03_specialty_store_ratio.png`: 특화 매장(DT, 리저브, 딜리버스) 구성 비율
  4. `04_sido_dt_ratio_comparison.png`: 시도별 DT(드라이브스루) 입점 비율 비교
  5. `05_annual_opening_trend.png`: 연도별 신규 개점 매장 수 추이 (1999년 이대 1호점 ~ 현재)
  6. `06_business_years_distribution.png`: 전국 매장 업력(운영 연수) 분포 히스토그램 & KDE
  7. `07_store_geo_scatter.png`: 전국 매장 위경도 공간 산점도 (지역별 색상 코딩)
  8. `08_seoul_hotspot_scatter.png`: 서울 중심권/강남권 매장 밀집 공간 분포도
  9. `09_tfidf_top30_keywords.png`: 매장명 및 주소 기반 TF-IDF 상위 30대 핵심 입지 키워드
  10. `10_sido_specialty_cluster_heatmap.png`: 시도별 일반/DT/리저브 매장 구성비 히트맵
- 각 차트별 요약 통계 및 200자 이상 비즈니스 인사이트 작성
- 전체 기술통계표 및 2,000자 이상의 시장 구조·입지 전략 심층 리포트 생성 (`starbucks/reports/EDA_Report.md`)

---

### Component 3: 글래스모피즘 인터랙티브 웹 대시보드 (`starbucks/src/build_dashboard.py` & `starbucks/dashboard.html`)

#### [NEW] `starbucks/src/build_dashboard.py` & `starbucks/dashboard.html`
- 단일 파일 HTML (로컬 `file://` 실행 지원, CORS 이슈 원천 차단)
- 전수 데이터를 JSON 형태로 인라인 임베드
- UI 스타일: **오로라 앰비언트 글로우 & 반투명 블러 글래스모피즘 테마**
- Chart.js v4 기반 6대 인터랙티브 반응형 차트:
  1. 시도별 매장 수 랭킹 (Horizontal Bar Chart)
  2. 특화 서비스 매장 비중 (Doughnut Chart: 일반, DT, 리저브, 딜리버스)
  3. 연도별 개점 추이 (Area Line Chart)
  4. 시도별 DT 비율 비교 (Bar Chart)
  5. 업력 구간별 매장 수 (Polar Area / Bar Chart)
  6. 서울 구별 매장 수 TOP 10 (Bar Chart)
- 실시간 데이터 탐색기:
  - 매장명, 주소 실시간 텍스트 검색
  - 시도 선택, DT 여부, 리저브 여부, 신규 매장 필터링
  - 컬럼 클릭 시 오름차순/내림차순 정렬
  - 반응형 페이지네이션 (페이지당 15/30/50개 보기)
  - 매장 클릭 시 상세 모달 (주소, 전화번호, 개점일, 이미지, 특화 태그)
  - 필터링된 결과 즉시 CSV 다운로드 기능

---

### Component 4: 프로젝트 문서화 (`starbucks/docs/`)

#### [NEW] `starbucks/docs/implementation_plan.md`
- 본 구현 계획서 복사본 보관

#### [NEW] `starbucks/docs/api_specification.md`
- 스타벅스 Gateway API 엔드포인트 명세서, 요청 헤더, 페이로드 구조 및 응답 JSON 스키마 상세 문서

---

## 5. Verification Plan

### Automated Tests
1. **가상환경 패키지 확인 및 설치**:
   ```powershell
   uv add pandas matplotlib koreanize-matplotlib scikit-learn
   ```
2. **Phase 1 서울 수집 및 무결성 검증 실행**:
   ```powershell
   uv run python starbucks/src/scraper.py --phase seoul
   ```
   - 예상 결과: 서울 매장 710개 이상 수집 완료, 결측치 0%, `starbucks/data/starbucks_seoul_{YYYYMMDD}.csv` 생성.
3. **Phase 2 전국 전수 수집 실행**:
   ```powershell
   uv run python starbucks/src/scraper.py --phase national
   ```
   - 예상 결과: 전국 매장 2,210개 이상 수집 완료, `starbucks/data/starbucks_national_{YYYYMMDD}.csv` 생성.
4. **심층 EDA 분석 실행**:
   ```powershell
   uv run python starbucks/src/eda_analysis.py
   ```
   - 예상 결과: `starbucks/images/`에 10종 차트 생성 완료, `starbucks/reports/EDA_Report.md` 발행 완료.
5. **대시보드 빌드 실행**:
   ```powershell
   uv run python starbucks/src/build_dashboard.py
   ```
   - 예상 결과: `starbucks/dashboard.html` 생성 완료.

### Manual Verification
- 브라우저를 통해 `starbucks/dashboard.html` 열기
- 검색창에 '강남' 또는 '제주' 입력 시 필터링 동작 확인
- DT/리저브 필터 토글 동작 확인
- 차트 호버 툴팁 및 다크/라이트 글래스모피즘 테마 가독성 확인
- CSV 다운로드 버튼 클릭 시 정제된 데이터 정상 다운로드 확인
