# YES24 베스트셀러 EDA 수행 결과 (Walkthrough)

## 1. 작업 개요 (Changes Made)
[`artifacts/plan_eda_yes24_bestseller.md`](file:///C:/FTC_downloads/Antigravity_project/myfirst_project/DATACRAWLING/artifacts/plan_eda_yes24_bestseller.md) 계획에 따라, YES24 IT/모바일 일별 베스트셀러 데이터셋([`yes24_day_bestseller.csv`](file:///C:/FTC_downloads/Antigravity_project/myfirst_project/DATACRAWLING/yes24/data/yes24_day_bestseller.csv))의 탐색적 데이터 분석(EDA)을 성공적으로 완료하였습니다.

### 주요 생성 및 변경 내역
1. **분석 환경 구축**:
   - `uv pip install --system-certs pandas numpy matplotlib seaborn` 설치 완료
2. **EDA 분석 스크립트 작성**:
   - 파일: [`yes24/src/yes24_eda_analysis.py`](file:///C:/FTC_downloads/Antigravity_project/myfirst_project/DATACRAWLING/yes24/src/yes24_eda_analysis.py)
   - 파이썬 코드 작성 규칙에 맞추어 최상단 모듈 Docstring 및 함수별 상세 Docstring을 한국어로 구현
3. **6종의 고해상도 시각화 차트 생성**:
   - 위치: [`yes24/images/`](file:///C:/FTC_downloads/Antigravity_project/myfirst_project/DATACRAWLING/yes24/images)
   - `eda_01_price_distribution.png`: 가격 분포 및 도서정가제(10%) 할인율 현황
   - `eda_02_correlation_heatmap.png`: 순위, 판매지수, 평점, 리뷰 수 간 스피어만 상관계수 히트맵
   - `eda_03_sales_vs_reviews.png`: 판매지수 vs 리뷰 수 관계 및 핵심 인기 도서 라벨링
   - `eda_04_top_publishers.png`: 베스트셀러 상위 10대 출판사 도서 점유율 및 누적 판매지수
   - `eda_05_keyword_frequency.png`: 태그 및 도서명 핵심 IT 키워드 TOP 20 빈도
   - `eda_06_pub_year_trend.png`: 출간 연도별 도서 수 및 신간(58.2%) vs 스테디셀러(41.8%) 비중
4. **종합 EDA 분석 보고서 작성**:
   - 파일: [`yes24/docs/yes24_day_bestseller_eda_report.md`](file:///C:/FTC_downloads/Antigravity_project/myfirst_project/DATACRAWLING/yes24/docs/yes24_day_bestseller_eda_report.md)
   - 5대 분석 영역별 심층 해석 및 비즈니스 전략 인사이트 수록

---

## 2. 검증 결과 (Validation Results)

### 스크립트 실행 및 산출물 검증
* `uv run python yes24/src/yes24_eda_analysis.py` 무결점 실행 완료 (`exit code 0`).
* [`yes24/images/`](file:///C:/FTC_downloads/Antigravity_project/myfirst_project/DATACRAWLING/yes24/images) 내 6종 이미지 생성 확인 (한글 폰트 정상 반영).
* 워크스페이스 아티팩트 관리 규칙에 따라 [`artifacts/walkthrough.md`](file:///C:/FTC_downloads/Antigravity_project/myfirst_project/DATACRAWLING/artifacts/walkthrough.md)에 동기화 완료.

---

## 3. 핵심 발견점 (Key Insights)
* **가격 정책**: 평균 판매가 25,023원, 전체 도서의 92.3%가 10% 정형화된 할인율 적용.
* **상관관계 및 집중도**: 순위와 판매지수 간 강한 음의 상관(-0.62), 판매지수와 리뷰 수 간 높은 양의 상관(+0.68) 확인.
* **출판사 생태계**: 한빛미디어(17.5%), 길벗(8.1%), 위키북스(6.3%) 등 상위 6개 출판사가 시장의 49.1%를 과점.
* **기술 트렌드**: AI, 클로드, 챗GPT, 바이브 코딩 등 생성형 AI 실무 활용서가 시장 수요를 주도.
* **도서 라이프사이클**: 2025~2026년 최신간이 58.2%로 과반수를 차지하나, 기초 CS 및 개발 명저는 2020~2023년 스테디셀러로 41.8%의 탄탄한 생존율을 유지.
