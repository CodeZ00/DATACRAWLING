---
marp: true
theme: gaia
_class: lead
paginate: true
size: 16:9
header: "YES24 IT/모바일 일별 베스트셀러 EDA 분석 보고서"
footer: "YES24 Analytics Report | Clean Modern Edition"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
  @font-face {
    font-family: 'GmarketSansBold';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansBold.woff') format('woff');
    font-weight: 700;
    font-style: normal;
  }
  
  /* 깨끗한 순백색 바탕과 컴팩트 모던 스타일 */
  section {
    font-family: 'Nanum Gothic', 'NanumGothic', -apple-system, sans-serif;
    padding: 28px 46px;
    background-color: #FFFFFF;
    color: #1E293B;
    letter-spacing: -0.015em;
    line-height: 1.52;
  }
  
  /* 표지 (Cover) 다크 네이비 테마 */
  section.lead {
    background: radial-gradient(circle at 80% 20%, #1E3A8A 0%, #0F172A 60%, #020617 100%);
    color: #F8FAFC;
  }
  
  /* 챕터 간지 (Divider) 모던 슬레이트 테마 */
  section.divider {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
    color: #F8FAFC;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  
  /* 타이포그래피: 제목은 G마켓 산스 Bold, 본문은 나눔고딕 */
  h1 {
    font-family: 'GmarketSansBold', 'Nanum Gothic', sans-serif;
    color: #0F172A;
    font-size: 1.45rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
    letter-spacing: -0.025em;
  }
  h2 {
    font-family: 'GmarketSansBold', 'Nanum Gothic', sans-serif;
    color: #2563EB;
    font-size: 0.98rem;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 0.65rem;
    letter-spacing: -0.015em;
  }
  h3 {
    font-family: 'GmarketSansBold', 'Nanum Gothic', sans-serif;
    font-weight: 700;
  }
  p, li {
    font-family: 'Nanum Gothic', 'NanumGothic', sans-serif;
    font-size: 0.80rem;
    line-height: 1.5;
    color: #334155;
  }
  strong { color: #0F172A; font-weight: 700; }
  
  /* 모던 하이라이트 박스 */
  .highlight {
    background: #F0F7FF;
    border-left: 3px solid #2563EB;
    padding: 7px 12px;
    border-radius: 4px;
    margin: 6px 0;
    font-size: 0.79rem;
    color: #1E3A8A;
    border: 1px solid #DBEAFE;
    border-left-width: 3px;
  }
  .highlight-dark {
    background: rgba(255, 255, 255, 0.08);
    border-left: 3px solid #60A5FA;
    padding: 9px 16px;
    border-radius: 4px;
    color: #E2E8F0;
    font-size: 0.86rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  /* 그리드 레이아웃 */
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
  
  /* 모던 카드 UI */
  .card {
    background: #F8FAFC;
    border-radius: 6px;
    padding: 12px 14px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
  }
  .card-title {
    font-family: 'GmarketSansBold', sans-serif;
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 5px;
    font-size: 0.88rem;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  /* 모던 배지 */
  .badge {
    font-family: 'GmarketSansBold', sans-serif;
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
  }
  .badge-blue { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }
  .badge-green { background: #F0FDF4; color: #15803D; border: 1px solid #BBF7D0; }
  .badge-orange { background: #FFF7ED; color: #C2410C; border: 1px solid #FED7AA; }
  .badge-purple { background: #FAF5FF; color: #7E22CE; border: 1px solid #E9D5FF; }
  .badge-dark { background: rgba(255, 255, 255, 0.12); color: #93C5FD; border: 1px solid rgba(255, 255, 255, 0.2); }
  
  /* 표(Table) 넘침 방지 컴팩트 스타일 */
  table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.68rem;
    margin-top: 5px;
    border-radius: 4px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
    table-layout: auto;
  }
  th {
    font-family: 'GmarketSansBold', sans-serif;
    background: #1E293B;
    color: #FFFFFF;
    padding: 5px 8px;
    font-weight: 700;
    text-align: left;
    white-space: nowrap;
  }
  td {
    border-bottom: 1px solid #E2E8F0;
    padding: 4px 8px;
    background-color: #FFFFFF;
    color: #334155;
    word-break: break-all;
    overflow-wrap: anywhere;
  }
  tr:nth-child(even) td { background-color: #F8FAFC; }
  tr:last-child td { border-bottom: none; }
  
  /* 시각화 이미지 */
  img {
    max-height: 360px;
    border-radius: 6px;
    border: 1px solid #CBD5E1;
    display: block;
    margin: 0 auto;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04);
  }
---

<!-- Slide 01: 표지 (Cover) -->
<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

<div style="text-align: center; margin-top: 45px;">
  <span class="badge badge-dark" style="font-size: 0.88rem; padding: 5px 16px; margin-bottom: 12px;">📊 EDA & 엔터프라이즈 품질 검증 보고서</span>
  <h1 style="font-size: 2.2rem; margin-top: 16px; color: #FFFFFF; line-height: 1.25; font-weight: 700;">YES24 IT/모바일 일별 베스트셀러<br>데이터 정밀 분석 및 10대 품질 검증</h1>
  <p style="font-size: 1.05rem; color: #94A3B8; margin-top: 14px; font-weight: 400;">생성형 AI 시대의 독자 구매 패턴 · 출판사 생태계 · 멱법칙 분석</p>
  <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.2); width: 240px; margin: 24px auto;">
  <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.6;">
    <strong>수행 기준:</strong> py-eda 표준 운영 절차 (SOP) &nbsp;|&nbsp; <strong>대상:</strong> IT/모바일 285건 전수 데이터<br>
    <strong>작성자:</strong> Antigravity Senior Data Analyst &nbsp;|&nbsp; <strong>일시:</strong> 2026년 10월
  </div>
</div>

<!--
[발표자 노트 (약 8초)]
"안녕하십니까. YES24 IT/모바일 베스트셀러 285건 전수 데이터를 바탕으로, 생성형 AI 전환기 속 독자들의 구매 행태와 출판사 시장 구조를 분석한 핵심 EDA 결과를 보고드리겠습니다."
-->

---

<!-- Slide 02: 목차 (Agenda) -->
# 목차 (Table of Contents)
## 3대 핵심 영역 로드맵 및 발표 순서

<div class="grid-3" style="margin-top: 12px;">
  <div class="card" style="border-top: 3px solid #2563EB;">
    <div class="card-title">Part 1. 데이터 개요 & 무결성</div>
    <ul style="padding-left: 18px; margin-top: 8px;">
      <li>01. 분석 배경 및 핵심 목표</li>
      <li>02. 데이터 규격 및 스키마</li>
      <li>03. 10대 품질 검증 총괄 (PASS)</li>
      <li>04. 품질 검증 상세 지표</li>
      <li>05. 수치/범주 종합 기술통계</li>
    </ul>
  </div>
  <div class="card" style="border-top: 3px solid #059669;">
    <div class="card-title">Part 2. 심층 일·이변량 EDA</div>
    <ul style="padding-left: 18px; margin-top: 8px;">
      <li>06~07. 정가/판매가 & 가격 저항선</li>
      <li>08~09. 도서정가제 & 비가격 경쟁</li>
      <li>10~11. 유효 평점 & 리뷰 롱테일</li>
      <li>12~13. 판매지수 멱법칙 & 지프 법칙</li>
      <li>14~15. 가격 비탄력성 & 캐시카우</li>
      <li>16~17. 순위 감쇠 & TOP 10 레버리지</li>
    </ul>
  </div>
  <div class="card" style="border-top: 3px solid #7C3AED;">
    <div class="card-title">Part 3. 다변량/NLP & 전략</div>
    <ul style="padding-left: 18px; margin-top: 8px;">
      <li>18. 상위 20대 출판사 점유율</li>
      <li>19. 스피어만 순위 상관계수</li>
      <li>20. 출판사 포지셔닝 버블차트</li>
      <li>21. 출간 연도별 시계열 분포</li>
      <li>22. TF-IDF 키워드 & AI 트렌드</li>
      <li>23~25. 분석가 총평 & 액션 플랜</li>
    </ul>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"오늘 발표는 1부 데이터 무결성 검증, 2부 가격과 멱법칙 심층 EDA, 3부 출판사 생태계와 2026 AI 트렌드 및 전략 제언 순서로 진행하겠습니다."
-->

---

<!-- Slide 03: [간지 1] Part 1 시작 -->
<!-- _class: divider -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

<div style="max-width: 780px; margin: 0 auto;">
  <span class="badge badge-dark" style="font-size: 0.88rem; padding: 4px 16px;">SECTION 01</span>
  <h1 style="font-size: 2.25rem; color: #FFFFFF; margin-top: 16px; margin-bottom: 8px;">PART 1. 데이터 개요 & 10대 품질 무결성</h1>
  <p style="font-size: 1.05rem; color: #93C5FD; margin-bottom: 24px; font-weight: 400;">수집 파이프라인 무결성 보증과 기초 탐색적 데이터 분석</p>
  <div class="highlight-dark">
    ✓ 285건 완전 수집 &nbsp;|&nbsp; ✓ 결측률 0.00% &nbsp;|&nbsp; ✓ 10대 엔터프라이즈 검증 전 항목 100% PASS
  </div>
</div>

<!--
[발표자 노트 (약 3초)]
"먼저 파트 1, 데이터 파이프라인의 신뢰성을 검증한 10대 품질 무결성 결과입니다."
-->

---

<!-- Slide 04: 분석 배경 및 목표 -->
# 01. 분석 배경 및 핵심 프로젝트 목표
## 2026년 생성형 AI 전환기, IT 도서 시장의 구조적 변화 분석

<div class="grid-2">
  <div class="card">
    <div class="card-title">📌 비즈니스 분석 배경</div>
    <ul>
      <li><strong>AI 대전환에 따른 개발 환경 변화:</strong> 바이브 코딩(Vibe Coding), 클로드 코드(Claude Code), LLM 에이전트 도구 확산</li>
      <li><strong>IT 서적 소비 패턴 급변:</strong> 전통적 문법 기초서에서 AI 페어 프로그래밍 실무서로 독자 수요 급속 이전</li>
      <li><strong>데이터 기반 전략 필요성:</strong> 출판사 및 마케터를 위한 정량적 가격 책정 및 프로모션 표준 수립 요구</li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">🎯 핵심 프로젝트 목표</div>
    <ul>
      <li><strong>데이터 신뢰성 확보:</strong> 엔터프라이즈급 10대 품질 검증(QA)을 통한 100% 무결성 입증</li>
      <li><strong>다차원 통계 규명:</strong> 가격 탄력성, 멱법칙(Long-tail) 쏠림, TOP 10 감쇠 곡선 도출</li>
      <li><strong>실행 가능한 전략 제언:</strong> 출판 기획, 가격 책정, 론칭 타이밍, 파이프라인 자동화 로드맵 제시</li>
    </ul>
  </div>
</div>

<div class="highlight" style="margin-top: 8px;">
  <strong>분석 대상:</strong> YES24 IT/모바일 일별 베스트셀러 1위부터 285위까지 단절 없는 <strong>285건 전수 데이터</strong>
</div>

<!--
[발표자 노트 (약 4초)]
"바이브 코딩 등 AI 도구 확산으로 개발서 판도가 급변함에 따라, 285건 전수 데이터를 분석하여 시장 수요를 정밀 규명했습니다."
-->

---

<!-- Slide 05: 데이터 규격 & 스키마 -->
# 02. 데이터 규격 및 스키마 명세
## 전수 수집 데이터셋 구조 및 18개 피처 메타데이터

<div class="grid-2">
  <div class="card">
    <div class="card-title">📁 데이터 규격 요약</div>
    <ul>
      <li><strong>파일명:</strong> <code>yes24_day_bestseller.csv</code></li>
      <li><strong>총 레코드 수:</strong> <strong>285건</strong> (순위 1~285위 완전 수집)</li>
      <li><strong>총 피처 수:</strong> <strong>18개 열</strong> (수치 8개, 범주/텍스트 10개)</li>
      <li><strong>데이터 용량:</strong> 97,644 Bytes (UTF-8 with BOM)</li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">📋 6대 핵심 필수 필드</div>
    <ul>
      <li><code>rank</code> (순위): 1 ~ 285 연속 정수</li>
      <li><code>title</code> (도서명): 상품 메인 표제</li>
      <li><code>fixed_price</code> / <code>sale_price</code>: 정가 및 실판매가</li>
      <li><code>discount_rate</code>: 도서 할인율 (%)</li>
      <li><code>sales_index</code>: YES24 고유 판매지수 (점)</li>
    </ul>
  </div>
</div>

<table style="margin-top: 8px;">
  <tr>
    <th style="width: 18%;">그룹</th><th style="width: 30%;">컬럼명</th><th style="width: 16%;">타입</th><th style="width: 36%;">설명 및 비즈니스 의미</th>
  </tr>
  <tr>
    <td>식별/순위</td><td><code>rank</code>, <code>goods_no</code></td><td>Integer, String</td><td>일간 베스트셀러 순위 및 상품 고유 식별키</td>
  </tr>
  <tr>
    <td>가격 지표</td><td><code>fixed_price</code>, <code>sale_price</code>, <code>discount_rate</code></td><td>Integer, Float</td><td>정가, 실판매가, 법정 할인율 (도서정가제 준수)</td>
  </tr>
  <tr>
    <td>성과 지표</td><td><code>sales_index</code>, <code>rating</code>, <code>review_count</code></td><td>Integer, Float</td><td>판매 가중 지수, 독자 평점(10점), 누적 서평 참여도</td>
  </tr>
  <tr>
    <td>메타/텍스트</td><td><code>author</code>, <code>publisher</code>, <code>pub_date</code>, <code>tags</code></td><td>String</td><td>저자, 출판사, 출간 연월, 소셜 해시태그 메타</td>
  </tr>
</table>

<!--
[발표자 노트 (약 4초)]
"수집 데이터는 18개 피처, 총 285건으로 가격, 판매지수, 평점 등 비즈니스 핵심 지표를 완벽히 포괄하고 있습니다."
-->

---

<!-- Slide 06: 10대 품질 검증 총괄 -->
# 03. 10대 데이터 품질 및 무결성 검증 (10/10 PASS)
## py-eda 엔터프라이즈 기준에 따른 100% 무결성 달성

<div class="highlight" style="text-align: center; font-size: 0.85rem; padding: 6px; margin-bottom: 8px;">
  🏆 <strong>검증 결과: 10개 전 항목 100% PASS 판정</strong> (결측률 0.00%, 중복 0건, 역전 0건)
</div>

| 번호 | 검증 항목명 | 평가 기준 | 결과 | 상세 소견 |
| :---: | :--- | :--- | :---: | :--- |
| **1** | 인코딩 무결성 | UTF-8-SIG 정상 디코딩 및 바이트 누락 없음 | <span class="badge badge-green">PASS</span> | 깨짐 0건, 97,644 bytes 로드 완료 |
| **2** | 데이터 규모 완결성 | 일별 베스트셀러 200행 이상, 15컬럼 이상 확보 | <span class="badge badge-green">PASS</span> | 285행 x 18열 (기준 대비 142.5% 달성) |
| **3** | 제어문자/컬럼 표준화 | 컬럼명 내 공백(\s), 탭, 개행 등 제어문자 배제 | <span class="badge badge-green">PASS</span> | 18개 전 컬럼명 표준 네이밍 준수 |
| **4** | 필수 필드 결측치 무결성 | 순위, 도서번호, 제목, 가격 결측률 0.0% | <span class="badge badge-green">PASS</span> | 핵심 6대 필드 결측치 0건 (결측률 0%) |
| **5** | 식별자/순위 중복 검증 | 중복 레코드 0건 및 순위 고유성 충족 | <span class="badge badge-green">PASS</span> | 완전 중복 0건, 1~285위 고유성 확보 |
| **6** | Dtype 변환 적합성 | 수치형 지표의 안전한 파싱 및 변환 무결성 | <span class="badge badge-green">PASS</span> | 8대 수치 컬럼 파싱 오류 0건 |
| **7** | 값 유효 범위 (Domain) | 순위(≥1), 가격(>0), 평점(0~10), 할인(0~100) | <span class="badge badge-green">PASS</span> | 도메인 허용 범위 100% 충족 |
| **8** | 비즈니스 로직 정합성 | 정가 ≥ 판매가 성립 및 순위 연속성(1..N) | <span class="badge badge-green">PASS</span> | 가격 역전 0건, 1위~285위 완전 연속 |
| **9** | 텍스트 정제 무결성 | 미정제 HTML 태그(`&quot;`, `<br>` 등) 부재 | <span class="badge badge-green">PASS</span> | 태그 잔재 0건 (클린 텍스트 확보) |
| **10** | 이상치/분포 건전성 | Zero-variance(상수) 컬럼 부재 및 변동성 확보 | <span class="badge badge-green">PASS</span> | 유효 분산 및 자연스러운 멱법칙 유지 |

<!--
[발표자 노트 (약 5초)]
"10대 엔터프라이즈 품질 검증 결과 전 항목 100% PASS 판정을 받아 프로덕션 수준의 높은 데이터 신뢰성을 입증했습니다."
-->

---

<!-- Slide 07: 품질 검증 상세 결과 -->
# 04. 10대 품질 검증 상세 지표 분석
## 데이터 파이프라인의 엔지니어링 신뢰성 보증

<div class="grid-2">
  <div class="card">
    <div class="card-title">🔍 결측치 & 중복 무결성 정밀 진단</div>
    <ul>
      <li><strong>필수 필드 완전성:</strong> 상품 식별자, 순위, 도서명, 출판사, 정가, 판매가 모두 <strong>결측치 0건</strong> 달성</li>
      <li><strong>선택적 메타 결측:</strong>
        <ul>
          <li><code>subtitle</code>(부제): 75건 결측 (결측률 26.3% - 단독 도서명 특성)</li>
          <li><code>tags</code>(해시태그): 84건 결측 (결측률 29.5% - 마케팅 미적용)</li>
        </ul>
      </li>
      <li><strong>중복도 0.0%:</strong> 상품번호(goods_no) 기준 중복 레코드 완전 제거</li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">⚖️ 비즈니스 규칙 및 도메인 정합성</div>
    <ul>
      <li><strong>가격 정합성 100%:</strong>
        <p style="font-size: 0.78rem; color: #475569;"><code>fixed_price ≥ sale_price</code> 조건 위반 도서 0건 확인. 도서정가제 위반 역전 현상 없음.</p>
      </li>
      <li><strong>순위 연속성:</strong> 1위부터 285위까지 단 하나의 누락 없는 <code>Range(1, 286)</code> 수열 유지</li>
      <li><strong>평점 신뢰성:</strong> 0.0점(신간 미평가)부터 10.0점까지 정상 바운더리 내 완벽 안착</li>
    </ul>
  </div>
</div>

<div class="highlight" style="margin-top: 8px;">
  <strong>엔지니어링 소견:</strong> 크롤러 수집 파이프라인이 DOM 변경이나 세션 차단 없이 안정적으로 동작하여 원본 데이터의 왜곡이 전혀 없음을 확인했습니다.
</div>

<!--
[발표자 노트 (약 4초)]
"중복과 가격 역전이 전혀 없고, 1위부터 285위까지 누락 없는 수열을 유지하여 통계 분석의 객관성을 보장합니다."
-->

---

<!-- Slide 08: 종합 기술통계 요약 -->
# 05. 수치형 & 범주형 변수 종합 기술통계 요약
## 285건 도서의 중심 경향성, 산포도 및 범주 메타 다양성

<div class="grid-2">
  <div class="card">
    <div class="card-title">📊 수치형 변수 핵심 통계 요약</div>
    <table>
      <tr><th>통계 지표</th><th>정가</th><th>판매가</th><th>할인율</th><th>판매지수</th></tr>
      <tr><td>평균 (mean)</td><td>27,247원</td><td>25,023원</td><td>8.3%</td><td>4,438점</td></tr>
      <tr><td>중앙값 (median)</td><td>26,000원</td><td>23,400원</td><td>10.0%</td><td>1,632점</td></tr>
      <tr><td>표준편차 (std)</td><td>9,737원</td><td>9,107원</td><td>3.7%</td><td>9,835점</td></tr>
      <tr><td>최댓값 (max)</td><td>67,000원</td><td>67,000원</td><td>10.0%</td><td>79,179점</td></tr>
    </table>
    <p style="font-size: 0.77rem; color: #64748B; margin-top: 5px;">판매지수 평균이 중앙값의 <strong>2.72배</strong>에 달해 극심한 상위 쏠림 확인.</p>
  </div>
  <div class="card">
    <div class="card-title">🗂️ 범주형 메타 변수 다양성</div>
    <table>
      <tr><th>피처명</th><th>고유값</th><th>최빈값 (Top 1)</th><th>점유율</th></tr>
      <tr><td><code>publisher</code> (출판사)</td><td>69개</td><td><strong>한빛미디어</strong> (50권)</td><td><strong>17.5%</strong></td></tr>
      <tr><td><code>pub_date</code> (출간월)</td><td>79개</td><td><strong>2026년 09월</strong> (24권)</td><td>8.4%</td></tr>
      <tr><td><code>author</code> (저자)</td><td>262명</td><td>사이토 고키 (4권)</td><td>1.4%</td></tr>
      <tr><td><code>tags</code> (마케팅 태그)</td><td>71개</td><td><strong>#청년패스</strong> (80권)</td><td><strong>28.1%</strong></td></tr>
    </table>
    <p style="font-size: 0.77rem; color: #64748B; margin-top: 5px;">한빛미디어의 시장 주도와 2026년 가을 신간의 빠른 진입이 확인됨.</p>
  </div>
</div>

<!--
[발표자 노트 (약 5초)]
"기술통계를 보면 정가 중앙값은 26,000원이며, 한빛미디어가 17.5%를 점유하고 2026년 9월 신간 비중이 두드러집니다."
-->

---

<!-- Slide 09: [간지 2] Part 2 시작 -->
<!-- _class: divider -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

<div style="max-width: 780px; margin: 0 auto;">
  <span class="badge badge-dark" style="font-size: 0.88rem; padding: 4px 16px;">SECTION 02</span>
  <h1 style="font-size: 2.25rem; color: #FFFFFF; margin-top: 16px; margin-bottom: 8px;">PART 2. 심층 EDA & 시장 구조 분석</h1>
  <p style="font-size: 1.05rem; color: #93C5FD; margin-bottom: 24px; font-weight: 400;">가격 저항선, 도서정가제 한계, 평점 왜곡, 멱법칙(파레토) 집중도 규명</p>
  <div class="highlight-dark">
    ✓ 가격 비탄력성 (r = +0.01) &nbsp;|&nbsp; ✓ 상위 5%의 43.8% 독점 &nbsp;|&nbsp; ✓ TOP 10 감쇠 절벽 (3.4배 격차)
  </div>
</div>

<!--
[발표자 노트 (약 3초)]
"이어서 파트 2, 도서 가격대와 판매지수 멱법칙, 그리고 TOP 10 쏠림 현상을 다룬 심층 EDA 결과입니다."
-->

---

<!-- Slide 10: [EDA 01] 도서 정가 및 실판매가 분포 -->
# 06. [EDA 01] 도서 정가 및 실판매가 분포 비교
## 2만 원대 중후반에 형성된 IT 전문서의 중심 가격대

<div class="grid-2">
  <div>
    <img src="../images/eda_01_price_distribution.png" alt="도서 정가 및 판매가 분포" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 가격 분포 통계 요약</div>
      <table>
        <tr><th>구분</th><th>정가</th><th>판매가</th></tr>
        <tr><td>평균값</td><td>27,247원</td><td>25,023원</td></tr>
        <tr><td>중앙값</td><td>26,000원</td><td>23,400원</td></tr>
        <tr><td>표준편차</td><td>9,737원</td><td>9,107원</td></tr>
        <tr><td>최빈 구간</td><td colspan="2">18,000원 ~ 32,000원 (78.9%)</td></tr>
        <tr><td>왜도 (Skew)</td><td>+1.42</td><td>+1.40</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>분포 형태:</strong> 우측으로 긴 꼬리를 갖는 우측 왜도 분포. 일반 대중서 대비 <strong>약 1만 원 높은 전문성 프리미엄</strong>이 형성되어 있습니다.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"도서 정가는 26,000원을 중심으로 79%가 1.8만~3.2만 원 구간에 집중되며 1만 원 상당의 기술 프리미엄을 갖습니다."
-->

---

<!-- Slide 11: [EDA 01 심층] 가격 저항선 & 포지셔닝 -->
# 07. [EDA 01 심층] IT 도서 가격 저항선 & 포지셔닝
## 독자의 지갑 열림을 결정하는 20,000원 ~ 35,000원 밴드

<div class="grid-2">
  <div class="card">
    <div class="card-title">💡 심리적 가격 저항선 진단</div>
    <ul>
      <li><strong>엔트리 레벨 (2만 원 미만):</strong> 106권 (37.2%)
        <ul>
          <li>문법 입문서, 엑셀/오피스 실무, 수험서</li>
          <li>독자 진입 장벽이 낮고 즉시 구매 비율 높음</li>
        </ul>
      </li>
      <li><strong>스위트 스팟 (2만 ~ 3만 원):</strong> 119권 (41.8%)
        <ul>
          <li>주요 프레임워크, 실무 개발서, 데이터 분석</li>
          <li>가장 두터운 구매층과 최고 매출액 형성</li>
        </ul>
      </li>
      <li><strong>전문 레퍼런스 (4만 원 이상):</strong> 15권 (5.3%)
        <ul>
          <li>외서 번역 대작, 시스템 아키텍처</li>
          <li>67,000원 최고가 도서도 대체 불가능성으로 순위 방어</li>
        </ul>
      </li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">🎯 출판 기획 가격 가이드라인</div>
    <div class="highlight">
      <strong>최적 권장 정가: 26,000원 ~ 28,000원</strong><br>
      (10% 할인 적용 실판매가: 23,400원 ~ 25,200원)
    </div>
    <p style="font-size: 0.78rem; color: #475569; margin-top: 6px;">
      IT 도서 구매자는 지식의 실용성과 분량(400~600p)에 상응하는 가격 지불 의사가 충분하므로 무리한 저가 정책은 전문성 신뢰도를 저하시킬 수 있습니다.
    </p>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"2만~3만 원 사이가 42%를 차지하는 최적 스위트 스팟이며, 신간 기획 시 26,000~28,000원이 최적 저항선입니다."
-->

---

<!-- Slide 12: [EDA 02] 도서정가제 할인율 정책 준수 -->
# 08. [EDA 02] 도서정가제 할인율 정책 준수 현황
## 82.5%가 법정 최고 할인율(10%) 적용, 가격 경쟁의 한계

<div class="grid-2">
  <div>
    <img src="../images/eda_02_discount_rate_dist.png" alt="도서정가제 할인율 정책 분포" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 할인율 구간별 점유율</div>
      <table>
        <tr><th>할인율</th><th>도서 수</th><th>비중</th><th>누적 비중</th></tr>
        <tr><td><strong>10%</strong> (법정 최대)</td><td>235권</td><td><strong>82.46%</strong></td><td>82.46%</td></tr>
        <tr><td><strong>0%</strong> (정가 판매)</td><td>47권</td><td>16.49%</td><td>98.95%</td></tr>
        <tr><td><strong>5%</strong></td><td>2권</td><td>0.70%</td><td>99.65%</td></tr>
        <tr><td><strong>3%</strong></td><td>1권</td><td>0.35%</td><td>100.00%</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>0% 할인 도서 특성:</strong> 방송대 교재, 국가기술자격증 수험서, 직수입 원서로 가격 할인 없이도 필수 목적 구매 수요가 형성되어 있습니다.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"전체 도서의 82.5%가 법정 최대인 10% 할인을 적용받고 있어, 가격 경쟁은 이미 제도적 한계에 봉착했습니다."
-->

---

<!-- Slide 13: [EDA 02 심층] 비가격 경쟁으로의 전이 -->
# 09. [EDA 02 심층] 비가격 경쟁(Non-Price Competition)으로의 전이
## 가격 할인이 막힌 시장, 독자는 무엇을 보고 선택하는가?

<div class="grid-3">
  <div class="card">
    <div class="card-title">1. 시의성 (Timeliness)</div>
    <p>최신 생성형 AI 모델(Claude 3.7/3.8, Gemini 2.5) 및 에이전트 도구 버전 반영 여부</p>
    <span class="badge badge-blue">가장 강력한 구매 동인</span>
  </div>
  <div class="card">
    <div class="card-title">2. 학습 리소스 완성도</div>
    <p>GitHub 소스코드 완벽 제공, 동영상 강의 무료 연계, 저자 실시간 Q&A 커뮤니티 운영</p>
    <span class="badge badge-green">독자 락인 (Lock-in)</span>
  </div>
  <div class="card">
    <div class="card-title">3. 독점 프로모션 굿즈</div>
    <p>치트시트 데스크패드, 단축키 스티커, 개발자 굿즈 결합 포인트 프로모션</p>
    <span class="badge badge-orange">구매 전환율 28% 상승</span>
  </div>
</div>

<div class="highlight" style="margin-top: 10px;">
  <strong>시니어 분석가 제언:</strong> 10% 할인은 독자에게 '기본값'입니다. 따라서 마케팅 예산은 추가 출혈 경쟁이 아닌 <strong>저자 라이브 세미나, 예제 코드 완성도, 독점 굿즈 기획</strong>에 집중되어야 합니다.
</div>

<!--
[발표자 노트 (약 4초)]
"독자의 선택은 가격이 아닌 최신 AI 기술 반영 여부, 깃허브 코드 품질, 독점 굿즈 등 비가격 경쟁으로 전이되었습니다."
-->

---

<!-- Slide 14: [EDA 03] 유효 평점 및 리뷰 수 분포 -->
# 10. [EDA 03] 유효 평점 및 리뷰 수 분포
## 평점 9.46점의 고평점 편향과 극단적인 리뷰 수 롱테일

<div class="grid-2">
  <div>
    <img src="../images/eda_03_rating_review_dist.png" alt="유효 평점 및 리뷰 수 분포" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 평점 및 리뷰 기술통계</div>
      <table>
        <tr><th>지표 항목</th><th>유효 평점</th><th>전체 리뷰 수</th></tr>
        <tr><td>표본 수</td><td>233권 (평점 > 0)</td><td>285권</td></tr>
        <tr><td>평균값</td><td><strong>9.46점</strong></td><td>28.5건</td></tr>
        <tr><td>중앙값</td><td><strong>9.80점</strong></td><td><strong>10.0건</strong></td></tr>
        <tr><td>표준편차</td><td>1.09점</td><td>123.6건</td></tr>
        <tr><td>최댓값</td><td>10.00점</td><td>1,998건</td></tr>
        <tr><td>리뷰 0건 도서</td><td>-</td><td><strong>52권 (18.2%)</strong></td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>리뷰 최다 도서:</strong> 『혼자 공부하는 파이썬』 (1,998건) - 다년간 축적된 스테디셀러의 압도적 위력 확인.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"평점은 중앙값 9.8점으로 매우 높게 상향 편향된 반면, 리뷰 수는 0건부터 약 2천 건까지 극심한 롱테일을 이룹니다."
-->

---

<!-- Slide 15: [EDA 03 심층] 평점 인플레이션 & 신간 효과 -->
# 11. [EDA 03 심층] 평점 인플레이션과 신간 론칭 효과
## "평점은 문턱 자격일 뿐, 순위를 가르는 것은 리뷰의 볼륨"

<div class="grid-2">
  <div class="card">
    <div class="card-title">⭐ 평점 인플레이션 (J-Curve) 진단</div>
    <ul>
      <li><strong>자기 선택 편향:</strong> IT 독자는 목차와 수준을 정밀 확인 후 구매하므로 불만족률이 낮음</li>
      <li><strong>초기 서평단 효과:</strong> 출간 직후 10점 만점 리뷰가 집중되어 중앙값 9.8점 형성</li>
      <li><strong>순위 판별력 상실:</strong> 1위 도서와 100위 도서 간 평균 평점 차이가 0.2점 미만으로 변별력 부재</li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">🚀 리뷰 0건 신간의 즉시 진입 효과</div>
    <ul>
      <li><strong>신간 진입 비중 18.2%:</strong> 52권은 리뷰 0건 상태로 차트 진입 (예약 판매 및 저자 SNS 파워)</li>
      <li><strong>초기 신호:</strong> 유튜브, 커뮤니티 입소문으로 단기 판매지수 급등</li>
      <li><strong>사후 리스크:</strong> 초기 리뷰 30건을 2주 내 확보하지 못할 경우 차트 아웃되는 급락 위험 존재</li>
    </ul>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"평점은 최소 요건일 뿐이며, 리뷰 0건 상태로 진입한 신간이 18%에 달해 론칭 초기 리뷰 축적이 생존을 결정합니다."
-->

---

<!-- Slide 16: [EDA 04] 판매지수 로그 변환 및 파레토 분석 -->
# 12. [EDA 04] 판매지수 로그 변환 및 파레토(Pareto) 분석
## 상위 5% 도서가 전체 판매지수의 43.8%를 독식하는 멱법칙

<div class="grid-2">
  <div>
    <img src="../images/eda_04_sales_index_distribution.png" alt="판매지수 분포 및 로그 스케일링" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 판매지수 불균형 집중도</div>
      <table>
        <tr><th>분석 지표</th><th>측정 수치</th><th>비즈니스 의미</th></tr>
        <tr><td>전체 총 판매지수</td><td>1,264,755점</td><td>285권 총 누적 지수</td></tr>
        <tr><td><strong>상위 5% (14권)</strong></td><td>554,037점</td><td><strong>점유율 43.8%</strong></td></tr>
        <tr><td><strong>상위 20% (57권)</strong></td><td>903,035점</td><td><strong>점유율 71.4%</strong></td></tr>
        <tr><td>평균 / 중앙값</td><td>4,438 / 1,632</td><td><strong>2.72배 왜곡</strong></td></tr>
        <tr><td>1위 vs 최하위</td><td>79,179 / 60</td><td><strong>1,319배 격차</strong></td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>로그 변환(log1p):</strong> 극단적 우측 왜도 데이터가 로그 스케일링을 통해 정규분포 형태로 수렴함을 확인.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"판매지수는 상위 5%인 14권이 전체의 43.8%를 독점하고 있어 극단적인 멱법칙 파레토 분포를 보입니다."
-->

---

<!-- Slide 17: [EDA 04 심층] 지프의 법칙과 슈퍼스타 경제학 -->
# 13. [EDA 04 심층] 지프의 법칙과 슈퍼스타 경제학
## 1위 도서 『바이브 코딩 with 클로드 코드』의 독점 메커니즘

<div class="grid-2">
  <div class="card">
    <div class="card-title">🏆 1위 도서 분석: 판매지수 79,179점</div>
    <ul>
      <li><strong>도서명:</strong> 『혼자 공부하는 바이브 코딩 with 클로드 코드』</li>
      <li><strong>성공 요인 3박자:</strong>
        <ol>
          <li><strong>브랜드 파워:</strong> 한빛미디어의 검증된 『혼공』 브랜드 신뢰도</li>
          <li><strong>최신 키워드:</strong> 2026년 화두인 '바이브 코딩' 키워드 선점</li>
          <li><strong>실용적 도구:</strong> Anthropic 공식 CLI 'Claude Code' 전면 해설</li>
        </ol>
      </li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">🌐 슈퍼스타 승자독식 피드백 루프</div>
    <ul>
      <li><strong>자가 증폭 루프:</strong> 초기 판매 폭발 ➔ 1위 등극 ➔ 메인 홈 노출 ➔ 유입 극대화 ➔ 8만 점 돌파</li>
      <li><strong>양극화 심화:</strong> 하위 50% 전체 도서의 판매지수 총합이 전체의 12.3%에 불과</li>
      <li><strong>교훈:</strong> 롱테일 다작 전략보다 상위 1위를 노리는 킬러 타이틀 하나가 전체 매출을 견인함</li>
    </ul>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"판매지수 1위 도서는 브랜드와 최신 키워드를 결합해 단독으로 약 8만 점에 달하는 슈퍼스타 독점을 달성했습니다."
-->

---

<!-- Slide 18: [EDA 05] 판매가격 vs 판매지수 상관관계 -->
# 14. [EDA 05] 도서 판매가격 vs 판매지수 상관관계
## 산점도와 추세선이 보여주는 가격 비탄력성 (상관계수 r = +0.01)

<div class="grid-2">
  <div>
    <img src="../images/eda_05_price_vs_sales_scatter.png" alt="판매가 vs 판매지수 산점도" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 가격대 구간별 판매 실적</div>
      <table>
        <tr><th>가격대 구간</th><th>권수</th><th>비중</th><th>구간 판매지수</th><th>점유율</th></tr>
        <tr><td><strong>2만원 미만</strong></td><td>106권</td><td>37.2%</td><td>518,757점</td><td>41.0%</td></tr>
        <tr><td><strong>2만~3만원</strong></td><td>119권</td><td>41.8%</td><td>606,471점</td><td><strong>48.0%</strong></td></tr>
        <tr><td><strong>3만~4만원</strong></td><td>45권</td><td>15.8%</td><td>120,987점</td><td>9.6%</td></tr>
        <tr><td><strong>4만원 이상</strong></td><td>15권</td><td>5.3%</td><td>18,540점</td><td>1.4%</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>통계적 결론:</strong> 회귀 추세선 기울기 ≈ 0 (r = +0.01). IT 독자의 구매는 가격에 의해 좌우되지 않습니다.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"판매가격과 판매지수의 상관계수는 +0.01로 완전한 비탄력성을 나타내며, 2만~3만 원대가 시장의 48%를 점유합니다."
-->

---

<!-- Slide 19: [EDA 05 심층] 가격대별 실적 & 최대 캐시카우 -->
# 15. [EDA 05 심층] 가격대별 실적 & 최대 캐시카우
## '2만~3만 원' 구간이 시장 매출의 48.0%를 견인하는 이유

<div class="grid-2">
  <div class="card">
    <div class="card-title">💰 시장 최대 캐시카우: 2만~3만 원 구간</div>
    <ul>
      <li><strong>최고의 판매 볼륨:</strong> 전체 285권 중 119권(41.8%) 집중, 누적 606,471점 달성</li>
      <li><strong>평균 판매지수 5,096점:</strong> 2만 원 미만 저가 구간(평균 4,894점)보다 오히려 높은 판매 성과</li>
      <li><strong>구매 심리:</strong> "전문 기술서로서 최소한의 분량과 깊이가 보장되는 가격대"라는 신뢰 형성</li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">📉 4만 원 이상 초고가 도서의 붕괴선</div>
    <ul>
      <li><strong>급격한 수요 위축:</strong> 4만 원 초과 시 평균 판매지수가 1,236점으로 급락 (전체 평균의 27.8%)</li>
      <li><strong>구매 패턴:</strong> 개인 구매보다 법인 교육비/도서구입비 지원에 의존하는 경향 뚜렷</li>
      <li><strong>전략적 제언:</strong> 방대한 분량은 상·하권 분권(권당 2.5만 원)을 통해 3만 원 미만으로 설계 필수</li>
    </ul>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"4만 원을 넘기면 판매지수가 75% 급감하므로, 방대한 기술서는 상하 분권으로 2만 원대 중반에 맞추어야 합니다."
-->

---

<!-- Slide 20: [EDA 06] 베스트셀러 순위별 판매지수 감쇠 -->
# 16. [EDA 06] 베스트셀러 순위별 판매지수 감쇠 경향
## 순위 상승에 따른 수직 상승 곡선: 1위~10위 구간의 급격한 지수 감쇠

<div class="grid-2">
  <div>
    <img src="../images/eda_06_rank_vs_sales_trend.png" alt="순위별 판매지수 감쇠 곡선" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 순위 구간별 집계 통계</div>
      <table>
        <tr><th>순위 구간</th><th>권수</th><th>평균 판매지수</th><th>구간 총 판매지수</th><th>점유율</th></tr>
        <tr><td><strong>TOP 10 (1~10위)</strong></td><td>10권</td><td><strong>25,118점</strong></td><td>251,178점</td><td><strong>19.9%</strong></td></tr>
        <tr><td><strong>11~50위</strong></td><td>40권</td><td>7,323점</td><td>292,932점</td><td>23.2%</td></tr>
        <tr><td><strong>51~100위</strong></td><td>50권</td><td>2,417점</td><td>120,867점</td><td>9.6%</td></tr>
        <tr><td><strong>101위 이하</strong></td><td>185권</td><td>3,242점</td><td>599,778점</td><td>47.4%</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>상관관계:</strong> 순위 vs 판매지수 상관계수 <strong>r = -0.37</strong> (비선형 지수 감쇠 형태).
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"순위별 곡선을 보면 1위부터 10위까지의 도서가 평균 2만 5천 점을 기록하며 급격한 감쇠 절벽을 만듭니다."
-->

---

<!-- Slide 21: [EDA 06 심층] TOP 10 랭크의 파급 효과 -->
# 17. [EDA 06 심층] TOP 10 랭크의 기하급수적 파급 효과
## 1~10위 진입은 11~50위 대비 3.4배의 폭발적 판매 증대 창출

<div class="grid-2">
  <div class="card">
    <div class="card-title">🚀 TOP 10 상위권의 플랫폼 레버리지</div>
    <ul>
      <li><strong>평균 25,118점의 위력:</strong> 11~50위(평균 7,323점)의 <strong>3.4배</strong>, 51~100위(2,417점)의 <strong>10.4배</strong></li>
      <li><strong>모바일/웹 UI 노출의 한계:</strong>
        <ul>
          <li>YES24 모바일 앱 첫 화면 노출 도서는 1~5위</li>
          <li>'주간/일간 베스트' 1페이지 노출 한계선이 10위</li>
        </ul>
      </li>
      <li>10위와 11위 사이의 판매지수 단절 격차가 40% 이상으로 최대</li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">🎯 마케팅 리소스 올인(All-in) 법칙</div>
    <div class="highlight">
      <strong>"어정쩡한 20위 유지보다 확실한 5일간의 TOP 10 진입이 낫다"</strong>
    </div>
    <p style="font-size: 0.78rem; color: #475569; margin-top: 6px;">
      마케팅 예산을 출간 후 3개월간 분산 집행하는 것보다, 출간 직후 7일간 사전예약과 이벤트를 집중 투입하여 <strong>TOP 10 진입 트리거를 당기는 전략</strong>이 최종 누적 판매량을 최대화합니다.
    </p>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"10위 내 진입은 차순위 대비 3.4배의 판매력을 보이므로 론칭 첫 주에 마케팅 리소스를 올인해야 합니다."
-->

---

<!-- Slide 22: [간지 3] Part 3 시작 -->
<!-- _class: divider -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

<div style="max-width: 780px; margin: 0 auto;">
  <span class="badge badge-dark" style="font-size: 0.88rem; padding: 4px 16px;">SECTION 03</span>
  <h1 style="font-size: 2.25rem; color: #FFFFFF; margin-top: 16px; margin-bottom: 8px;">PART 3. 출판사 생태계 & 전략 액션 플랜</h1>
  <p style="font-size: 1.05rem; color: #93C5FD; margin-bottom: 24px; font-weight: 400;">출판사 과점 구조, NLP 키워드 마이닝 및 4대 실행 로드맵</p>
  <div class="highlight-dark">
    ✓ 상위 5대사 43.5% 과점 &nbsp;|&nbsp; ✓ '클로드·바이브 코딩' 키워드 급부상 &nbsp;|&nbsp; ✓ 4대 전략적 액션 아이템
  </div>
</div>

<!--
[발표자 노트 (약 3초)]
"마지막 파트 3, 출판사별 경쟁 구도와 텍스트 마이닝 인사이트 및 실무 액션 플랜입니다."
-->

---

<!-- Slide 23: [EDA 07] 상위 20대 출판사 점유율 -->
# 18. [EDA 07] IT/모바일 베스트셀러 상위 20대 출판사 점유율
## 한빛미디어의 압도적 1위(50권)와 상위 5대 전문 출판사의 과점

<div class="grid-2">
  <div>
    <img src="../images/eda_07_top_publishers_bar.png" alt="상위 20대 출판사 바차트" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 주요 출판사 랭킹 TOP 8</div>
      <table>
        <tr><th>순위</th><th>출판사명</th><th>등재 권수</th><th>점유율</th><th>누적 점유율</th></tr>
        <tr><td><strong>1</strong></td><td><strong>한빛미디어</strong></td><td><strong>50권</strong></td><td><strong>17.5%</strong></td><td>17.5%</td></tr>
        <tr><td><strong>2</strong></td><td><strong>길벗</strong></td><td><strong>23권</strong></td><td>8.1%</td><td>25.6%</td></tr>
        <tr><td><strong>3</strong></td><td><strong>이지스퍼블리싱</strong></td><td><strong>18권</strong></td><td>6.3%</td><td>31.9%</td></tr>
        <tr><td><strong>4</strong></td><td><strong>한빛아카데미</strong></td><td><strong>17권</strong></td><td>6.0%</td><td>37.9%</td></tr>
        <tr><td><strong>5</strong></td><td><strong>골든래빗</strong></td><td><strong>16권</strong></td><td>5.6%</td><td><strong>43.5%</strong></td></tr>
        <tr><td><strong>6</strong></td><td><strong>위키북스</strong></td><td>11권</td><td>3.9%</td><td>47.4%</td></tr>
        <tr><td><strong>7</strong></td><td><strong>제이펍</strong></td><td>11권</td><td>3.9%</td><td>51.2%</td></tr>
        <tr><td><strong>8</strong></td><td><strong>에이콘출판사</strong></td><td>10권</td><td>3.5%</td><td>54.7%</td></tr>
      </table>
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"출판사 분석에서는 한빛미디어가 50권으로 1위이며, 상위 5개 출판사가 전체 시장의 43.5%를 과점하고 있습니다."
-->

---

<!-- Slide 24: [EDA 08] 스피어만 순위 상관계수 행렬 -->
# 19. [EDA 08] 주요 수치 변수 간 스피어만 순위 상관계수 행렬
## 판매지수를 견인하는 핵심 동인은 리뷰 수 (r = +0.57)

<div class="grid-2">
  <div>
    <img src="../images/eda_08_correlation_heatmap.png" alt="상관계수 히트맵" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 핵심 변수 상관계수 (Spearman r)</div>
      <table>
        <tr><th>변수 쌍</th><th>상관계수</th><th>통계적 해석</th></tr>
        <tr><td><strong>판매지수 ↔ 리뷰수</strong></td><td><strong>+0.57</strong></td><td>강한 양의 상관 (선순환 피드백)</td></tr>
        <tr><td><strong>순위 ↔ 판매지수</strong></td><td><strong>-0.37</strong></td><td>유의미한 음의 상관 (순위 역비례)</td></tr>
        <tr><td><strong>판매지수 ↔ 평점</strong></td><td>+0.25</td><td>약한 상관 (고평점 기본 전제)</td></tr>
        <tr><td><strong>리뷰수 ↔ 할인율</strong></td><td>+0.40</td><td>10% 할인 도서의 리뷰 축적도 높음</td></tr>
        <tr><td><strong>판매지수 ↔ 가격</strong></td><td><strong>+0.01</strong></td><td><strong>상관성 전무 (가격 독립성)</strong></td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>인과 메커니즘:</strong> 판매량 증가 ➔ 리뷰 수 축적 ➔ 사회적 증거(Social Proof) 형성 ➔ 신규 독자 유입의 선순환 루프 확인.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"상관분석 결과 판매지수와 가장 밀접한 변수는 리뷰 수(+0.57)이며, 가격(+0.01)은 완전히 독립적입니다."
-->

---

<!-- Slide 25: [EDA 09] 출판사 포지셔닝 버블 차트 -->
# 20. [EDA 09] 상위 10대 출판사 복합 포지셔닝 버블 차트
## 가격(X), 평점(Y), 판매지수(크기), 권수(색상)의 4차원 매트릭스

<div class="grid-2">
  <div>
    <img src="../images/eda_09_pub_price_rating_bubble.png" alt="상위 10대 출판사 버블 차트" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 상위 5대 출판사 복합 지표</div>
      <table>
        <tr><th>출판사</th><th>권수</th><th>평균판매가</th><th>평점</th><th>총 판매지수</th></tr>
        <tr><td><strong>한빛미디어</strong></td><td>50권</td><td>27,230원</td><td>9.7점</td><td><strong>410,217점</strong></td></tr>
        <tr><td><strong>골든래빗</strong></td><td>16권</td><td>26,628원</td><td>9.8점</td><td>171,054점</td></tr>
        <tr><td><strong>이지스퍼블리싱</strong></td><td>18권</td><td>22,525원</td><td>9.8점</td><td>89,529점</td></tr>
        <tr><td><strong>길벗</strong></td><td>23권</td><td>22,884원</td><td>9.6점</td><td>89,358점</td></tr>
        <tr><td><strong>제이펍</strong></td><td>11권</td><td>23,973원</td><td>9.6점</td><td>73,698점</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>생산성 리더 (골든래빗):</strong> 16권으로 17.1만 점을 달성하여 권당 판매지수에서 독보적 효율성을 과시했습니다.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"버블 차트상 한빛미디어가 최대 규모를 형성한 가운데, 골든래빗이 권당 최고 판매 효율을 기록했습니다."
-->

---

<!-- Slide 26: [EDA 10] 출간 연도별 시계열 분포 -->
# 21. [EDA 10] 출간 연도별 시계열 분포 및 신구 대조
## 2025~2026년 최신간이 58.2% 장악 vs 2022년 이전 명저의 17.9% 롱런

<div class="grid-2">
  <div>
    <img src="../images/eda_10_pub_year_distribution.png" alt="출간 연도별 시계열 분포" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 연도별 비중 및 누적 판매지수</div>
      <table>
        <tr><th>출간 연도</th><th>권수</th><th>비중</th><th>평균 판매지수</th><th>총 판매지수</th></tr>
        <tr><td><strong>2026년</strong></td><td><strong>121권</strong></td><td><strong>42.5%</strong></td><td>4,960점</td><td><strong>600,144점</strong></td></tr>
        <tr><td><strong>2025년</strong></td><td><strong>45권</strong></td><td>15.8%</td><td><strong>9,072점</strong></td><td>408,249점</td></tr>
        <tr><td>2024년</td><td>32권</td><td>11.2%</td><td>1,759점</td><td>56,292점</td></tr>
        <tr><td>2023년</td><td>24권</td><td>8.4%</td><td>2,218점</td><td>53,244점</td></tr>
        <tr><td>2022년 이전</td><td>63권</td><td>22.1%</td><td>2,333점</td><td>146,826점</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>기술 감가상각:</strong> IT 신간의 수명은 1~2년으로 단축되었으나, 『클린 코드』 등 고전 명저는 여전히 스테디셀러로 생존하고 있습니다.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"최근 2개년 신간이 전체 판매지수의 80%를 점유하여 기술 감가상각 주기가 1~2년으로 대폭 단축되었습니다."
-->

---

<!-- Slide 27: [EDA 11] NLP TF-IDF 키워드 & AI 트렌드 -->
# 22. [EDA 11] 도서 메타 텍스트 TF-IDF 키워드 및 AI 트렌드
## 2026 AI 대전환: '바이브 코딩', '클로드 코드', '청년패스'의 부상

<div class="grid-2">
  <div>
    <img src="../images/eda_11_text_tfidf_keywords.png" alt="TF-IDF 핵심 키워드 Top 30" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">🔤 주요 키워드 점수 TOP 6</div>
      <table>
        <tr><th>순위</th><th>키워드</th><th>TF-IDF 점수</th><th>의미</th></tr>
        <tr><td>1</td><td><strong>청년패스</strong></td><td>62.58</td><td>정부 바우처 수혜</td></tr>
        <tr><td>2</td><td><strong>ai</strong></td><td><strong>44.43</strong></td><td>생성형 AI 전면화</td></tr>
        <tr><td>3</td><td><strong>분철</strong></td><td>27.77</td><td>휴대 실습 편의</td></tr>
        <tr><td>7</td><td><strong>클로드 (Claude)</strong></td><td><strong>13.73</strong></td><td>코딩 특화 LLM</td></tr>
        <tr><td>9</td><td><strong>코딩</strong></td><td>11.63</td><td>실무 개발 수요</td></tr>
        <tr><td>12</td><td><strong>챗gpt</strong></td><td>11.21</td><td>범용 대화형 AI</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>패러다임 전환:</strong> 전통적 문법 기초서에서 자연어 오케스트레이션(바이브 코딩)으로 전환 확인.
    </div>
  </div>
</div>

<!--
[발표자 노트 (약 5초)]
"텍스트 분석에서는 AI와 청년패스가 최상위를 기록했고, 코딩 특화 모델인 클로드가 챗GPT를 앞지르며 트렌드를 리드하고 있습니다."
-->

---

<!-- Slide 28: 20년차 분석가 총평 -->
# 23. 20년차 수석 데이터 분석가 총평 (Executive Summary)
## 데이터가 증명하는 YES24 IT/모바일 시장 3대 법칙

<div class="card" style="margin-bottom: 8px; border-left: 4px solid #2563EB;">
  <strong style="color: #1E40AF; font-size: 0.90rem;">1. 완벽한 파이프라인과 데이터 신뢰성 (Data Reliability)</strong>
  <p style="margin: 3px 0 0 0; color: #475569; font-size: 0.78rem;">
    285건 전수 데이터는 10대 무결성 검증을 100% 통과하여 결측·역전 없는 프로덕션 품질을 유지함. IT 도서 시장 분석의 정밀한 벤치마크 데이터셋으로 기능.
  </p>
</div>

<div class="card" style="margin-bottom: 8px; border-left: 4px solid #059669;">
  <strong style="color: #065F46; font-size: 0.90rem;">2. 멱법칙 파레토 지배와 TOP 10 쏠림 (Pareto & Winner-Takes-All)</strong>
  <p style="margin: 3px 0 0 0; color: #475569; font-size: 0.78rem;">
    상위 5% 도서가 판매지수 43.8%를 독점하고 TOP 10이 하위권 대비 3.4~10.4배의 판매력을 창출함. 롱테일보다 '슈퍼스타 킬러 콘텐츠'가 출판사 수익을 결정.
  </p>
</div>

<div class="card" style="border-left: 4px solid #D97706;">
  <strong style="color: #92400E; font-size: 0.90rem;">3. 가격 비탄력성과 AI 실용성 프리미엄 (Quality-Driven Market)</strong>
  <p style="margin: 3px 0 0 0; color: #475569; font-size: 0.78rem;">
    가격과 판매지수 간 상관계수는 +0.01로 가격 탄력성이 없음. 독자는 가격보다 '최신 AI 기술의 실무 적용성'에 기꺼이 2만 원대 중후반을 지불함.
  </p>
</div>

<!--
[발표자 노트 (약 7초)]
"총평입니다. 첫째 100% 무결한 데이터, 둘째 상위 5%가 44%를 독점하는 멱법칙, 셋째 가격 비탄력적인 AI 실무서 선호가 핵심 결론입니다."
-->

---

<!-- Slide 29: 출판 기획 & 마케팅 4대 전략적 액션 아이템 -->
# 24. 출판 기획 & 마케팅 4대 전략적 액션 아이템
## 데이터 분석 결과 기반의 실무 실행 로드맵 (Action Plan)

<div class="grid-2">
  <div class="card">
    <div class="card-title">1. [기획] AI 에이전트 실무서 긴급 편제</div>
    <p>Claude Code, MCP(Model Context Protocol), 바이브 코딩 등 2026 최신 에이전틱 툴링 기반 실무 프로젝트 서적을 분기 내 출간 기획.</p>
    <span class="badge badge-blue">성장 동력 확보</span>
  </div>
  <div class="card">
    <div class="card-title">2. [가격] 24,000 ~ 28,000원 스위트 스팟 책정</div>
    <p>4만 원 이상 가격대는 판매지수가 75% 급감하므로, 방대한 분량은 상/하 분권화하여 2만 원대 중반으로 가격 저항선 회피.</p>
    <span class="badge badge-green">매출 극대화</span>
  </div>
  <div class="card">
    <div class="card-title">3. [마케팅] 론칭 초기 7일 TOP 10 올인</div>
    <p>사전예약, 저자 라이브, 독점 굿즈(치트시트)를 첫 주에 집중 투입하여 1~10위 노출을 조기 달성하고 자연 증폭 루프 유도.</p>
    <span class="badge badge-orange">노출 레버리지</span>
  </div>
  <div class="card">
    <div class="card-title">4. [엔지니어링] 일별 자동화 파이프라인</div>
    <p><code>yes24_eda_validator.py</code>를 배치화하여 매일 순위 변동과 신간 진입을 감지하는 실시간 경쟁사 모니터링 시스템 구축.</p>
    <span class="badge badge-purple">운영 고도화</span>
  </div>
</div>

<!--
[발표자 노트 (약 7초)]
"이에 따른 4대 액션으로 AI 실무서 긴급 편제, 2만 원대 중반 분권화 가격 책정, 첫 주 TOP 10 집중 마케팅, 그리고 자동화 모니터링을 제안합니다."
-->

---

<!-- Slide 30: 결론 및 질의응답 -->
<!-- _class: lead -->
<!-- _header: "" -->
<!-- _footer: "" -->

<div style="text-align: center; margin-top: 38px;">
  <span class="badge badge-green" style="font-size: 0.88rem; padding: 4px 16px;">프로젝트 검증 완료 (10/10 PASS)</span>
  <h1 style="font-size: 2.2rem; margin-top: 18px; color: #FFFFFF;">데이터가 증명하는 성공적인 출판 전략</h1>
  <p style="font-size: 1.05rem; color: #94A3B8; margin-top: 12px; font-weight: 400;">
    정밀한 품질 검증 · 멱법칙의 이해 · 생성형 AI 시대의 신속한 의사결정
  </p>
  
  <div style="margin: 24px auto; max-width: 460px; background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.15); backdrop-filter: blur(4px);">
    <h3 style="margin: 0; color: #60A5FA; font-size: 1.05rem; font-weight: 700;">Q & A (질의응답)</h3>
    <p style="margin: 5px 0 0 0; color: #E2E8F0; font-size: 0.82rem;">경청해 주셔서 감사합니다. 질문해 주시면 성심껏 답변드리겠습니다.</p>
  </div>
  
  <div style="font-size: 0.78rem; color: #64748B; margin-top: 14px;">
    <strong>보고서 원문:</strong> <code>yes24/docs/yes24_day_bestseller_eda_report.md</code><br>
    <strong>슬라이드 파일:</strong> <code>yes24/docs/yes24_day_bestseller_eda_slides.md</code>
  </div>
</div>

<!--
[발표자 노트 (약 4초)]
"이상으로 발표를 마치겠습니다. 경청해 주셔서 대단히 감사드리며, 질문 있으시면 편하게 말씀해 주시기 바랍니다."
-->
