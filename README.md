# 📚 DATACRAWLING: 국내 주요 서점 베스트셀러 데이터 수집 & 심층 분석 플랫폼

[![GitHub Pages](https://img.shields.io/badge/Live_Dashboard-GitHub_Pages-blue?style=for-the-badge&logo=github)](https://codez00.github.io/DATACRAWLING/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/Package_Manager-uv-DE5FE9?style=for-the-badge)](https://github.com/astral-sh/uv)
[![Chart.js](https://img.shields.io/badge/Visualization-Chart.js_v4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

교보문고와 예스24 등 국내 대표 온라인 서점의 IT/컴퓨터 분야 일간 베스트셀러 데이터를 공식 REST API 및 웹 스크래핑을 통해 안정적으로 수집하고, 데이터 사이언스 기반의 심층 탐색적 데이터 분석(EDA)과 모던 인터랙티브 웹 대시보드를 구축하는 엔드투엔드(End-to-End) 데이터 엔지니어링 & 분석 플랫폼입니다.

---

## 🌐 인터랙티브 웹앱 라이브 대시보드

교보문고 IT 베스트셀러 전수 데이터를 브라우저에서 실시간으로 시각화하고 탐색할 수 있는 웹 애플리케이션입니다.

👉 **[라이브 대시보드 바로가기 (클릭)](https://codez00.github.io/DATACRAWLING/)**

```
https://codez00.github.io/DATACRAWLING/
```

### 🎨 대시보드 주요 특징
- **화이트 톤 글래스모피즘(White Glassmorphism)**: 은은한 파스텔 앰비언트 글로우 배경과 프로스티드 글래스 패널의 감각적인 UI
- **Chart.js 6대 인터랙티브 차트**: 가격대 구간별 분포, 상위 10대 출판사 점유율, 연도별 신간 추이, 순위별 리뷰 수, 평점 분포, TF-IDF 핵심 키워드
- **실시간 탐색기**: 도서명/저자/출판사 실시간 검색, 다중 조건 필터링, 컬럼별 정렬, 페이징 테이블
- **상세 모달 & CSV 다운로드**: 도서 클릭 시 전체 줄거리/소개글 및 스펙 확인, 필터링 결과 엑셀 호환 CSV 즉시 내보내기

---

## 📂 프로젝트 구조

```text
DATACRAWLING/
├── README.md                      # 전체 프로젝트 통합 가이드
├── kyobo/                         # 교보문고 베스트셀러 프로젝트
│   ├── data/                      # 수집된 데이터셋 (CSV, UTF-8-SIG)
│   │   ├── kyobo_daily_it_bestseller_20261020.csv  # 1차 수집 (658건)
│   │   └── kyobo_daily_it_bestseller_20261021.csv  # 2차 수집 (593건, 1~593위)
│   ├── docs/                      # 수집 계획서 및 아티팩트 문서
│   │   ├── dashboard_implementation_plan.md       # 대시보드 구축 계획서
│   │   ├── dashboard_walkthrough.md               # 구축 완료 워크스루 보고서
│   │   ├── kyobo_scraping_plan.md                 # 데이터 수집 계획서
│   │   └── scraping_promt.md                      # REST API 규격 명세서
│   ├── images/                    # EDA 시각화 차트 이미지 (11종 고해상도 PNG)
│   ├── reports/                   # 전문 데이터 분석 보고서
│   │   └── EDA_Report.md                          # 20년차 데이터 분석가 가이드라인 보고서
│   └── src/                       # 핵심 소스 코드
│       ├── build_dashboard.py                     # 대시보드 번들러 & 컴파일러
│       ├── dashboard.html                         # 독립형 화이트 글래스모피즘 웹 대시보드
│       ├── generate_tables.py                     # 통계 요약표 생성기
│       ├── github_workflow.py                     # GitHub Issue/PR 자동화 스크립트
│       ├── kyobo_bestseller_scraper.py            # 교보문고 REST Gateway API 스크래퍼
│       └── kyobo_eda_analysis.py                  # 11종 차트 생성 심층 EDA 스크립트
├── starbucks/                     # 스타벅스 전국 매장 전수 수집 & 상권 심층 분석 프로젝트
│   ├── dashboard.html             # 독립형 에메랄드 글래스모피즘 웹 대시보드
│   ├── docs/                      # API 규격서, 수집 계획서, 구현 계획서, 워크스루
│   ├── images/                    # 10종 고해상도 EDA 시각화 차트 (PNG)
│   ├── reports/                   # 20년차 데이터 분석가 심층 분석 종합 보고서 (Markdown)
│   └── src/                       # 스크래퍼, EDA 분석기, 대시보드 빌더, PDF 변환기
└── yes24/                         # 예스24 베스트셀러 프로젝트
    ├── docs/                      # 예스24 스크래핑 명세 및 슬라이드 프롬프트
    ├── images/                    # 예스24 EDA 분석 차트 이미지
    └── src/                       # 예스24 스크래퍼 및 Marp 발표 자료 생성기
```

---

## 🔍 주요 프로젝트 상세

### 1. 교보문고 (kyobo)
- **API 연동 스크래퍼**: 교보문고 프론트엔드가 사용하는 내부 REST Gateway API(`https://store.kyobobook.co.kr/api/gw/best/best-seller/online`)를 직접 호출하여 차단 위험 없이 고속 수집
- **자동 페이징 & 무결성 보장**: GZIP 응답 압축 해제, HTML 태그 자동 정제, 1위부터 593위까지 결측치 0건 전수 수집
- **심층 EDA 분석 (11개 차트)**:
  - 수치형/범주형 기술통계 및 각 2,000자 이상의 심층 비즈니스 인사이트 도출
  - Scikit-Learn `TfidfVectorizer` 기반 도서 소개 형태소 배제 텍스트 마이닝
  - 가격 형성 메커니즘, 도서정가제 10% 획일화, 출판사 3사 과점(한빛미디어, 길벗, 영진닷컴) 실증 분석
- **독립형 웹앱 대시보드**: 별도 백엔드 실행 없이 로컬 `file://` 또는 GitHub Pages로 즉시 서빙

### 2. 예스24 (yes24)
- 예스24 일간 베스트셀러 웹 스크래핑 및 정제
- 도서 판매지수, 가격, 리뷰, 출판사별 EDA 시각화
- Marp 기반 프리젠테이션 슬라이드 및 엑셀 대시보드 자동화

### 3. 스타벅스 (starbucks)
- **전국 매장 전수 수집**: 스타벅스 Gateway REST API(`getStore.do`) 연동으로 17개 시도 2,213개 전 매장 무결점 전수 수집
- **지리/상권 심층 EDA (10개 차트)**: 서울 구별 밀집도, 드라이브스루(DT) 권역 비교, 개점 연도별 확장 추이, 텍스트 마이닝(TF-IDF) 등 20년차 분석가 수준의 비즈니스 리포트 도출
- **에메랄드 글래스모피즘 웹 대시보드**: 독립형 단일 HTML 파일로 전국 매장 실시간 검색, 시도/유형 필터링, Chart.js 동적 시각화 및 CSV 즉시 내보내기 지원

---

## 🛠 기술 스택

| 영역 | 기술 및 도구 |
| :--- | :--- |
| **Language & Runtime** | Python 3.12+, HTML5, Vanilla JavaScript (ES6+) |
| **Package Management** | `uv` (Astral) |
| **Data Engineering** | `urllib`, `gzip`, `json`, `csv`, `re` |
| **Data Analysis & ML** | `pandas`, `numpy`, `scikit-learn` (TF-IDF) |
| **Data Visualization** | `matplotlib`, `seaborn`, `koreanize-matplotlib`, `Chart.js v4` |
| **UI Framework** | Tailwind CSS (CDN), Lucide Icons, Pretendard Font |
| **Deployment & CI/CD** | GitHub Pages (`gh-pages`), Git & GitHub REST API |

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1. 저장소 클론 및 가상환경 활성화
```bash
git clone https://github.com/CodeZ00/DATACRAWLING.git
cd DATACRAWLING
```

> [!NOTE]
> 본 프로젝트는 초고속 패키지 관리자인 **`uv`**를 표준으로 사용하며, 워크스페이스 루트의 단일 `.venv` 환경을 공유합니다.

### 2. 패키지 설치
```bash
uv pip install -r requirements.txt
# 또는 주요 패키지 직접 설치
uv pip install pandas matplotlib seaborn koreanize-matplotlib scikit-learn
```

### 3. 교보문고 베스트셀러 데이터 수집 실행
```bash
uv run python kyobo/src/kyobo_bestseller_scraper.py
```
- 실행 완료 시 `kyobo/data/kyobo_daily_it_bestseller_{YYYYMMDD}.csv` 파일이 생성됩니다.

### 4. 심층 EDA 분석 및 시각화 차트 생성
```bash
uv run python kyobo/src/kyobo_eda_analysis.py
```
- 11종의 고해상도 시각화 차트가 `kyobo/images/` 폴더에 생성됩니다.

### 5. 웹 대시보드 빌드 및 로컬 실행
```bash
uv run python kyobo/src/build_dashboard.py
```
- 최신 수집 데이터를 감지하여 `kyobo/src/dashboard.html`이 빌드됩니다.
- 생성된 `dashboard.html` 파일을 더블클릭하거나 브라우저로 열면 즉시 대시보드가 구동됩니다.

---

## 🤖 범용 웹 수집·EDA·대시보드 자동화 에이전트 프레임워크 (`.agents/`)

교보문고와 예스24 프로젝트에서 실증된 파이프라인을 완전히 표준화하여, **어떠한 신규 웹사이트(이커머스, 채용, 포털, 미디어 등)**라도 일관된 품질로 수집부터 웹 대시보드 배포까지 완수할 수 있는 5대 핵심 커스터마이징 자산을 저장소에 일체형으로 탑재했습니다:

```text
.agents/
├── rules/
│   └── universal-pipeline.md        # 5대 표준 디렉터리 강제 및 운영 규칙
├── skills/
│   └── universal-data-pipeline/     # 범용 파이프라인 실행 스킬
│       ├── SKILL.md                 # 6단계 엔드투엔드 실행 지침
│       └── templates/               # 재사용 가능한 코드 템플릿 4종
│           ├── scraper_template.py      # REST API/정적 스크래퍼 베이스
│           ├── eda_template.py          # 10종 차트 & Scikit-learn TF-IDF 분석기
│           ├── dashboard_template.html  # 화이트 글래스모피즘 웹 대시보드
│           └── report_template.md       # 20년차 데이터 분석가 종합 리포트 서식
├── hooks/
│   ├── hooks.json                   # PostToolUse 파일 저장 감지 훅
│   └── verify_csv_integrity.py      # UTF-8-SIG 인코딩, 결측치 0% 감사기
└── agents/
    └── definitions.json             # 4대 전문 서브에이전트 역할 정의
        ├── site-crawler             # REST API 역공학 및 전수 수집
        ├── eda-analyst              # 10종 차트 생성 및 심층 리포트 작성
        ├── dashboard-architect      # Chart.js 웹 대시보드 UI/UX 구축
        └── pipeline-orchestrator    # PR 머지 및 GitHub Pages 라이브 배포 총괄
```

### ⚡ 새로운 사이트 적용 방법
1. **사이트 지정 및 요청**:
   - 사용자가 *"알라딘 베스트셀러 수집해서 대시보드까지 만들어줘"*와 같이 요청합니다.
2. **에이전트 파이프라인 자동 구동**:
   - `.agents/rules/universal-pipeline.md`에 따라 프로젝트 폴더 생성(`data/`, `src/`, `images/`, `docs/`, `reports/`)
   - `site-crawler`가 API 트래픽 역공학 후 `scraper.py`를 실행하여 UTF-8-SIG CSV 생성
   - `.agents/hooks/verify_csv_integrity.py`가 데이터셋의 무결성(결측률, 인코딩, 연속성)을 자동 검증
   - `eda-analyst`가 10종 고해상도 차트와 2,000자 이상의 심층 마크다운 보고서(`reports/EDA_Report.md`) 작성
   - `dashboard-architect`가 Chart.js 기반 글래스모피즘 웹 대시보드(`src/dashboard.html`) 완성
   - `pipeline-orchestrator`가 GitHub Pages에 라이브 배포

---

## 📄 라이선스 및 문의
- 본 프로젝트는 교육 및 연구 목적으로 제작되었습니다.
- 문의 사항은 저장소 [Issues](https://github.com/CodeZ00/DATACRAWLING/issues) 탭을 이용해 주시기 바랍니다.
