---
name: marp-slide
description: Marp 슬라이드, 마크다운 프레젠테이션, 발표 자료, PPT 슬라이드 생성, 슬라이드 리팩토링, 발표자 노트(Speaker Notes) 작성이 필요한 모든 상황에서 반드시 활성화해야 하는 전문 프레젠테이션 디자인 스킬입니다. 사용자가 "Marp", "슬라이드", "발표자료", "발표 대본", "프레젠테이션", "보고서를 슬라이드로", "간지 슬라이드", "발표자 노트", "16:9 슬라이드" 등을 언급하거나 분석 보고서/문서를 슬라이드로 변환해 달라고 요청할 때 예외 없이 무조건 이 스킬을 최우선으로 적용하십시오.
---

# 엔터프라이즈 Marp 프레젠테이션 디자인 스킬 (marp-slide)

이 스킬은 데이터 분석 보고서, 기획서, 기술 문서 등을 바탕으로 시각적 완성도가 뛰어난 **16:9 와이드 화면 비율의 모던 화이트 미니멀 Marp 슬라이드(`slides.md`)**를 제작하는 전문 운영 절차(SOP)입니다.

---

## 1. 핵심 철학 및 디자인 원칙

1. **순백색 바탕의 모던 미니멀리즘 (Clean White Modern Design)**:
   - 슬라이드 기본 배경을 **순백색(`#FFFFFF`)**으로 설정하여 높은 시인성과 산뜻한 모던 감성을 제공합니다.
   - 표지와 챕터 간지는 **다크 슬레이트/딥 네이비 그라디언트**를 적용하여 시각적 전환감을 극대화합니다.
2. **화면 넘침 방지 컴팩트 타이포그래피 (Zero Overflow)**:
   - 표(Table)나 카드가 슬라이드 밖으로 넘치거나 텍스트가 잘리지 않도록 **컴팩트한 폰트 스케일(제목 1.45rem, 본문 0.80rem, 표 0.68rem)**과 최적의 패딩을 적용합니다.
   - 테이블 셀에 `word-break: break-all;` 및 `overflow-wrap: anywhere;`를 적용하여 긴 텍스트와 다열(6~8열) 구조에서도 완벽한 가독성을 보장합니다.
3. **데이터 스토리텔링 & 7대 완결 구조**:
   - **표지 → 목차 → 챕터별 다크 간지(Section Divider) → 차트 2분할/심층 카드 본문 → 총평(3대 핵심 법칙) → 4대 액션 플랜 → Q&A 클로징**의 완결된 스토리라인을 구축합니다.
4. **완벽한 발표자 노트(Speaker Notes) 동봉**:
   - Marp 표준 주석 문법(`<!-- [발표자 노트 (약 N초)] "..." -->`)을 사용하여 전 슬라이드에 구어체 대본을 배치합니다. (기본 2분/120초 완주 호흡)
5. **언어 및 경로 규칙**:
   - 모든 슬라이드 내용, 코드 주석, 발표자 대본은 **한국어로만 작성**합니다.
   - 워크스페이스 내부 경로는 반드시 **상대경로**(`../images/차트.png`, `docs/문서.md`)를 준수합니다.

---

## 2. Marp 슬라이드 표준 스키마 & Frontmatter

슬라이드 파일 시작 부분에 아래 확장 인라인 스타일시트와 설정을 포함합니다.

```yaml
---
marp: true
theme: gaia
_class: lead
paginate: true
size: 16:9
header: "[프로젝트명 또는 메인 타이틀]"
footer: "[프로젝트명] Analytics Report | [연월]"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
  @font-face {
    font-family: 'GmarketSansBold';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansBold.woff') format('woff');
    font-weight: 700;
    font-style: normal;
  }
  
  /* 기본 슬라이드: 깨끗한 순백색 바탕과 컴팩트 폰트 */
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
```

---

## 3. 표준 슬라이드 7대 구조

1. **표지 (Cover Slide)**: `_class: lead`, 헤더/푸터 숨김, 타이틀, 부제목, 메타데이터
2. **목차 (Table of Contents)**: `grid-3` 카드 레이아웃으로 전체 발표 흐름 구조화
3. **챕터 간지 (Section Divider Slide)**: 파트 전환마다 1장씩 삽입 (`_class: divider`, `highlight-dark`)
4. **데이터 시각화 & 심층 분석 본문 슬라이드**:
   - 차트 슬라이드: `grid-2` (좌측 `img`, 우측 `card` 내 `table` + `highlight`)
   - 심층/이론 슬라이드: `grid-2` 또는 `grid-3` 카드 컴포넌트
   - 모든 슬라이드 상단에 주제 번호(`h1`)와 한 줄 결론(`h2`) 배치
5. **분석가 총평 (Executive Summary)**: 좌측 컬러 보더(`border-left: 4px solid ...`) 3대 핵심 시장 법칙
6. **전략적 4대 액션 플랜 (Action Plan)**: 기획, 가격, 마케팅, 엔지니어링 4대 실행 과제
7. **클로징 & Q&A**: `_class: lead`, 질의응답 안내 및 관련 파일 링크

---

## 4. 발표자 노트(Speaker Notes) 작성 가이드라인

- **표준 문법:**
  ```markdown
  <!--
  [발표자 노트 (약 N초)]
  "안녕하십니까. ...를 보고드리겠습니다."
  -->
  ```
- **기본 2분(120초) 완주 호흡:**
  - 표지 & 목차: 10~12초
  - 간지 슬라이드: 각 3초
  - 차트/분석 슬라이드: 각 4~5초 (수치 강조와 핵심 결론)
  - 총평 & 액션 플랜: 각 7~8초
  - 클로징: 4초
