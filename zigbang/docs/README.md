# 📚 직방 부동산 데이터 인텔리전스 프로젝트 문서 보관소 (Documentation Hub)

본 디렉터리는 직방(Zigbang) 플랫폼 기반 부동산 데이터 수집, 심층 EDA, 비즈니스 리포트 및 웹 대시보드 구축과 관련된 모든 공식 기술 문서 및 산출물 아티팩트를 영구 보존하는 아카이브입니다.

---

## 📑 [최신 프로젝트] 충북 청주시 청원구 오창읍 원룸·빌라 월세 파이프라인 (2026-10-29)

### 1. 공식 비즈니스 보고서 & 프레젠테이션 (.docx / .pptx)
| 파일명 | 산출물 구분 | 주요 내용 요약 |
| :--- | :--- | :--- |
| **[../reports/Ochang_Villa_Rent_Report.docx](../reports/Ochang_Villa_Rent_Report.docx)** | **공식 Word 종합 보고서 (.docx)** | 603개 실매물 데이터, 11대 시각화 차트 및 4,000자 이상 심층 비즈니스 제언 수록 프리미엄 리포트 |
| **[../reports/Ochang_Villa_Rent_Presentation.pptx](../reports/Ochang_Villa_Rent_Presentation.pptx)** | **공식 PPTX 발표 슬라이드 (.pptx)** | 16:9 와이드스크린 규격, Bento Grid 모던 디자인 시스템, 14장 전 슬라이드 200자 이상 발표자 노트 완비 |
| **[../reports/EDA_Report.md](../reports/EDA_Report.md)** | **마크다운 종합 분석 리포트** | 20년차 수석 데이터 분석가 작성 2,000자 이상 비즈니스 인사이트 및 11종 차트 전문 |

### 2. 인터랙티브 웹 대시보드
| 파일명 | 산출물 구분 | 주요 내용 요약 |
| :--- | :--- | :--- |
| **[../dashboard.html](../../dashboard.html)** (또는 `../dashboard.html`) | **인터랙티브 웹 대시보드** | 더블클릭(`file://`) 즉시 실행, 화이트 글래스모피즘 테마, Leaflet.js 오창읍 매물 지도, 6대 핵심 차트, 다중 필터 |

### 3. 프로젝트 기술 문서 & 데이터셋
| 파일명 | 문서 구분 | 주요 내용 요약 |
| :--- | :--- | :--- |
| **[ochang_collection_plan.md](ochang_collection_plan.md)** | 기술 명세서 / 수집 계획서 | 직방 Gateway REST API(POST /items/list 15개 배치), 지오해시 클러스터링 및 오창읍 바운딩 박스 명세 |
| **[ochang_data_dictionary.md](ochang_data_dictionary.md)** | 데이터 딕셔너리 | 수집 및 파생변수 26개 필드(보증금, 월세, 관리비, 가성비 지수, 옵션점수 등) 스키마 정의서 |
| **[ochang_dashboard_guide.md](ochang_dashboard_guide.md)** | 대시보드 가이드 | 화이트 글래스모피즘 Single File HTML, Leaflet.js 인터랙티브 지도 퀵 네비게이션 및 기능 가이드 |
| **[ochang_eda_summary.md](ochang_eda_summary.md)** | EDA 요약서 | 603건 표본 기술통계, 권역별(양청/구룡/주성) 비교표, Scikit-learn TF-IDF Top 10 요약 |
| **[../data/zigbang_daily_ochang_monthly_rent_20261029.csv](../data/zigbang_daily_ochang_monthly_rent_20261029.csv)** | 원천 데이터셋 | UTF-8-SIG 인코딩, 결측치 0.0% 무결성 검증 완료 전수 데이터셋 (603행, 26열) |

---

## 🏛️ [기존 프로젝트] 세종특별자치시 정부청사 생활권 오피스텔 파이프라인
- `api_specification.md`, `collection_plan.md`, `implementation_plan.md`, `walkthrough.md`, `subagent_workflow_and_audits.md`
