# 🚀 세종 오피스텔 파이프라인 수행 결과 Walkthrough

본 문서는 직방(Zigbang) 세종특별자치시 정부청사 생활권(어진동·나성동·도담동) 오피스텔 엔드투엔드 파이프라인의 전 과정 수행 결과와 검증 내역을 기록한 Walkthrough입니다.

---

## 1. 파이프라인 실행 요약

| 단계 | 수행 작업 | 실행 스크립트 | 결과 및 산출물 | 상태 |
| :---: | :--- | :--- | :--- | :---: |
| **Step 1** | API 역공학 및 세종청사 단지/매물 탐색 | `sniff_network.py` | 엔드포인트 규격 확인 | **완료 (PASS)** |
| **Step 2** | 단지 28개 및 실매물 36건 전수 수집/정제 | `scraper.py` | `data/zigbang_officetel_sejong_20261027.csv` | **완료 (PASS)** |
| **Audit** | 데이터 계약 및 무결성 전수 감사 | `verify_csv_integrity.py` | 결측치 0건, 인코딩 UTF-8-SIG 정상 | **완료 (PASS)** |
| **Step 3** | 실거주 가성비 중심 10종 고해상도 차트 생성 | `eda_analysis.py` | `images/01~10_*.png` & `summary_data.json` | **완료 (PASS)** |
| **Step 4** | 20년차 분석가 심층 리포트 및 PDF 변환 | `md_to_pdf.py` | `reports/EDA_Report.md` & `.pdf` | **완료 (PASS)** |
| **Step 5** | 앰버 글래스모피즘 인터랙티브 대시보드 빌드 | `build_dashboard.py` | `dashboard.html` (단일 파일, 71KB) | **완료 (PASS)** |

---

## 2. 생성된 핵심 산출물 목록

1. **원천 데이터셋**:
   - `zigbang/data/zigbang_officetel_sejong_20261027.csv` (UTF-8-SIG, 36건)
   - `zigbang/data/summary_data.json` (대시보드 연동용 사전 집계)
2. **고해상도 시각화 차트 10종 (`zigbang/images/`)**:
   - `01_dong_distribution_pie.png` (행정동별 점유율 도넛)
   - `02_sales_type_ratio.png` (거래유형별 비중 및 평균 월세)
   - `03_monthly_total_cost_distribution.png` (총주거비용 히스토그램 & KDE)
   - `04_area_vs_rent_scatter.png` (전용면적 vs 월세 선형 회귀)
   - `05_pyeong_rent_by_dong.png` (행정동별 평당 월세단가 박스플롯)
   - `06_manage_cost_burden_by_danji.png` (단지별 평당 관리비 부담률)
   - `07_floor_premium_analysis.png` (층수 그룹별 평당 임대료 추이)
   - `08_building_age_vs_rent_depreciation.png` (노후도 감가상각 추이)
   - `09_tfidf_resident_review_keywords.png` (TF-IDF 상위 25대 키워드)
   - `10_sejong_officetel_geo_bubble.png` (지리적 가성비 버블 차트)
3. **전문 종합 분석 보고서**:
   - `zigbang/reports/EDA_Report.md` (최소 2,000자 이상 비즈니스 제언)
   - `zigbang/reports/EDA_Report.pdf` (Print CSS 기반 인쇄용 A4 PDF, 1.5MB)
4. **인터랙티브 웹 대시보드**:
   - `zigbang/dashboard.html` (직방 앰버 글래스모피즘, 실거주 주거비 계산기 탑재)
