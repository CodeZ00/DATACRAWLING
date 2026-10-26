# ☕ 스타벅스 전국 매장 수집 및 엔드투엔드 파이프라인 구축 완료 Walkthrough

스타벅스 코리아 공식 웹사이트([store_map.do](https://www.starbucks.co.kr/store/store_map.do))의 내부 REST Gateway API(`getStore.do`)를 역공학하여 서울 1차 검증(712개) 및 전국 전수 수집(2,213개), 10종 고해상도 시각화 심층 EDA, 단일 파일 글래스모피즘 인터랙티브 대시보드까지 전 과정을 성공적으로 구축했습니다.

---

## 1. 수행 결과 요약

| 구분 | 주요 결과 | 비고 |
| :--- | :--- | :--- |
| **Phase 1 (서울)** | 총 712개 매장 수집 (결측치 0.0%, 좌표 유효율 100%) | `starbucks/data/starbucks_seoul_20261026.csv` |
| **Phase 2 (전국)** | 총 2,213개 매장 전수 수집 (결측치 0.0%, 중복 0건) | `starbucks/data/starbucks_national_latest.csv` |
| **무결성 감사** | `verify_csv_integrity.py` 전수 검증 **PASS** | UTF-8-SIG (BOM 포함) 엑셀 호환 보장 |
| **특화 매장 분석** | DT: 515개 (23.3%), 리저브: 61개 (2.8%), 딜리버스: 1,621개 (73.2%) | 공식 JS `store_core.js` 태그 분석 정밀 매핑 |
| **심층 EDA 분석** | 10종 고해상도(DPI 150) 차트 + 2,000자 이상 비즈니스 리포트 | `starbucks/reports/EDA_Report.md` (17KB) |
| **인터랙티브 웹 대시보드** | Single File HTML 글래스모피즘 웹 대시보드 (Chart.js v4) | `starbucks/dashboard.html` (1.2MB, 로컬 즉시 실행) |

---

## 2. 생성 및 수정된 파일 구조

```
starbucks/
├── dashboard.html                       # 글래스모피즘 인터랙티브 웹 대시보드 (Single File HTML)
├── data/
│   ├── starbucks_seoul_20261026.csv     # Phase 1: 서울 지역 712개 매장 정제 데이터
│   ├── starbucks_national_20261026.csv  # Phase 2: 전국 17개 시도 2,213개 매장 전수 데이터
│   └── starbucks_national_latest.csv    # 전국 매장 최신 참조용 심볼릭 데이터
├── docs/
│   ├── api_specification.md            # 스타벅스 Gateway REST API 기술 명세서
│   ├── implementation_plan.md          # 엔드투엔드 파이프라인 구현 계획서
│   └── walkthrough.md                  # 최종 완료 결과 보고서 (Walkthrough)
├── images/                              # 10종 고해상도(DPI 150) EDA 시각화 차트
│   ├── 01_sido_store_distribution.png   # 17개 시도별 매장 수 분포
│   ├── 02_seoul_gu_store_density.png    # 서울 25개 자치구별 매장 집중도
│   ├── 03_store_type_ratio.png          # 매장 유형별(일반/DT/리저브) 구성비
│   ├── 04_sido_dt_ratio_comparison.png  # 시도별 DT 비율 비교
│   ├── 05_annual_opening_trend.png      # 1999년~2026년 연도별 개점 추이
│   ├── 06_business_years_distribution.png # 매장 운영 연수(업력) 분포
│   ├── 07_store_geo_scatter.png         # 전국 매장 지리적 공간 분포
│   ├── 08_seoul_hotspot_scatter.png     # 서울 도심/강남 핫스팟 분포
│   ├── 09_tfidf_top30_keywords.png      # TF-IDF 상위 30대 입지 키워드
│   └── 10_sido_specialty_cluster_heatmap.png # 특화 매장 구성비 교차 히트맵
├── reports/
│   └── EDA_Report.md                    # 2,000자 이상 비즈니스 인사이트 종합 분석 보고서
└── src/
    ├── scraper.py                       # 2단계 수집 및 자동 무결성 검증 스크립트
    ├── eda_analysis.py                  # 10종 차트 생성 및 리포트 자동 발행 스크립트
    └── build_dashboard.py               # 대시보드 HTML 자동 빌더
```

---

## 3. 세부 검증 결과

### 3.1 `verify_csv_integrity.py` 실행 결과
```text
============================================================
[데이터 무결성 검증] starbucks_national_latest.csv
상태: PASS
총 데이터 행 수: 2,213건
컬럼 수: 20개
UTF-8-SIG 인코딩: 정상 (BOM 포함)
결측치: 0건 (완벽한 무결성)
============================================================
```

### 3.2 핵심 비즈니스 발견점
1. **수도권 과밀과 강남 3구 독점 현상**: 전국 매장의 57% 이상(1,260여 개)이 수도권에 집중되어 있으며, 서울 자치구 중 강남구(90개 이상), 중구, 서초구가 서울 전체의 30% 이상을 차지합니다.
2. **지역별 출점 전략 차별화**: 서울의 DT 비율은 3.4%에 불과한 반면, 경기도 외곽 및 지방 광역도(제주, 경남, 전남)에서는 DT 비율이 40~60%에 달하여 자가용 생활권에 특화된 교외형 매장이 주류입니다.
3. **딜리버스(Delivers) MFC 인프라화**: 전국 매장의 73.2%(1,621개)에서 딜리버스 배달 서비스를 제공하며, 매장이 자체 도심 물류 거점으로 기능하고 있습니다.

---

## 4. 확인 방법 (Manual Verification)
1. **대시보드 실행**: 브라우저에서 `starbucks/dashboard.html`을 더블 클릭하거나 열면 네트워크 서버 없이 즉시 대시보드가 로드됩니다.
2. **실시간 검색 및 필터**: '강남' 또는 '제주' 입력 시 테이블 및 KPI 카드가 반응하며, '🚗 드라이브스루' 또는 '⭐ 리저브' 버튼 클릭 시 즉시 필터링됩니다.
3. **CSV 내보내기**: 상단 'CSV 내보내기' 버튼 클릭 시 필터링된 결과가 한글 깨짐 없는 UTF-8-SIG CSV로 다운로드됩니다.
