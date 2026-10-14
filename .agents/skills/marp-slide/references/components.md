# Marp UI 컴포넌트 마크업 가이드 (모던 화이트 에디션)

순백색 배경(`background: #FFFFFF`)을 기준으로 글자 넘침을 방지하고 시각적 가독성을 극대화한 표준 컴포넌트 코드 조각입니다.

---

## 1. 차트 2분할 레이아웃 (Grid-2: Image + Table + Highlight)

```html
<div class="grid-2">
  <div>
    <img src="../images/차트_파일명.png" alt="차트 설명" style="width: 100%;">
  </div>
  <div>
    <div class="card" style="margin-bottom: 6px;">
      <div class="card-title">📊 핵심 통계 지표</div>
      <table>
        <tr><th>지표 항목</th><th>측정 수치</th><th>비즈니스 의미</th></tr>
        <tr><td><strong>표본 수</strong></td><td>285건</td><td>전수 조사 완료</td></tr>
        <tr><td><strong>평균값</strong></td><td>27,247원</td><td>전문가 가격 프리미엄</td></tr>
        <tr><td><strong>중앙값</strong></td><td>26,000원</td><td>안정적 중심 가격대</td></tr>
      </table>
    </div>
    <div class="highlight">
      <strong>핵심 인사이트:</strong> 2만 원대 중후반에 집중 분포하며 일반 대중서 대비 1만 원 높은 지불 의사가 형성되어 있습니다.
    </div>
  </div>
</div>
```

---

## 2. 2열 비교 카드 (Grid-2 Cards)

```html
<div class="grid-2">
  <div class="card">
    <div class="card-title">📌 현상 및 원인 분석</div>
    <ul>
      <li><strong>자기 선택 편향:</strong> 목차와 기술 스택을 면밀히 검토 후 구매</li>
      <li><strong>초기 서평단 집중:</strong> 출간 직후 10점 만점 리뷰 형성 (중앙값 9.8점)</li>
    </ul>
  </div>
  <div class="card">
    <div class="card-title">🎯 전략적 대응 방안</div>
    <div class="highlight">
      <strong>최적 권장 정가: 26,000원 ~ 28,000원</strong>
    </div>
    <p style="font-size: 0.78rem; color: #475569; margin-top: 6px;">
      무리한 저가 정책은 기술서로서의 신뢰도를 저하시킬 수 있으므로 2만 원대 중반의 스위트 스팟 유지가 필수적입니다.
    </p>
  </div>
</div>
```

---

## 3. 3열 카드 레이아웃 (Grid-3 Cards)

```html
<div class="grid-3">
  <div class="card">
    <div class="card-title">1. 시의성</div>
    <p>최신 생성형 AI 모델 및 툴링 버전 반영 여부</p>
    <span class="badge badge-blue">가장 강력한 구매 동인</span>
  </div>
  <div class="card">
    <div class="card-title">2. 학습 리소스</div>
    <p>GitHub 소스코드 완성도 및 동영상 강의 무료 연계</p>
    <span class="badge badge-green">독자 락인 (Lock-in)</span>
  </div>
  <div class="card">
    <div class="card-title">3. 독점 굿즈</div>
    <p>치트시트 데스크패드, 단축키 스티커 결합 프로모션</p>
    <span class="badge badge-orange">구매 전환율 28% 상승</span>
  </div>
</div>
```

---

## 4. 챕터 간지 (Section Divider Slide)

```html
<!-- Slide: 간지 -->
<!-- _class: divider -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

<div style="max-width: 780px; margin: 0 auto;">
  <span class="badge badge-dark" style="font-size: 0.88rem; padding: 4px 16px;">SECTION 02</span>
  <h1 style="font-size: 2.2rem; color: #FFFFFF; margin-top: 14px; margin-bottom: 8px;">PART 2. 심층 EDA & 시장 구조 분석</h1>
  <p style="font-size: 1.05rem; color: #93C5FD; margin-bottom: 22px;">가격 저항선, 도서정가제 한계, 평점 왜곡, 멱법칙(파레토) 집중도 규명</p>
  <div class="highlight-dark">
    ✓ 가격 비탄력성 (r = +0.01) &nbsp;|&nbsp; ✓ 상위 5%의 43.8% 독점 &nbsp;|&nbsp; ✓ TOP 10 감쇠 절벽 (3.4배 격차)
  </div>
</div>
```

---

## 5. 분석가 총평 카드 (Colored Left Borders)

```html
<div class="card" style="margin-bottom: 8px; border-left: 4px solid #2563EB;">
  <strong style="color: #1E40AF; font-size: 0.90rem;">1. 완벽한 파이프라인과 데이터 신뢰성</strong>
  <p style="margin: 3px 0 0 0; font-size: 0.78rem;">
    285건 전수 데이터는 10대 무결성 검증을 100% 통과하여 결측·역전 없는 프로덕션 품질을 유지함.
  </p>
</div>

<div class="card" style="margin-bottom: 8px; border-left: 4px solid #10B981;">
  <strong style="color: #166534; font-size: 0.90rem;">2. 멱법칙 파레토 지배와 TOP 10 쏠림</strong>
  <p style="margin: 3px 0 0 0; font-size: 0.78rem;">
    상위 5% 도서가 판매지수의 43.8%를 독점하고 TOP 10이 하위권 대비 3.4~10.4배의 판매력을 창출함.
  </p>
</div>
```
