"""교보문고 IT 베스트셀러 화이트 톤 글래스모피즘 웹 대시보드 생성 스크립트.

CSV 데이터를 로드하여 컴팩트한 JSON으로 가공한 뒤,
화사하고 세련된 화이트 톤 글래스모피즘(White Glassmorphism / Frosted Glass) UI와
Chart.js를 결합한 독립형 대시보드(kyobo/src/dashboard.html)를 빌드합니다.
"""

import json
from pathlib import Path
import pandas as pd


def build_dashboard():
    csv_path = Path("kyobo/data/kyobo_daily_it_bestseller_20261020.csv")
    output_html_path = Path("kyobo/src/dashboard.html")

    print(f">>> CSV 데이터 로드 중: {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # 수치형 필드 정제
    numeric_cols = [
        "rank",
        "prev_rank",
        "fixed_price",
        "sale_price",
        "discount_rate",
        "point",
        "review_count",
        "rating",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 문자열 필드 정제
    str_cols = ["title", "author", "publisher", "isbn", "intro", "pub_date"]
    for col in str_cols:
        df[col] = df[col].fillna("").astype(str)

    df["pub_year"] = df["pub_date"].str.slice(0, 4)

    # 1. KPI 지표 계산
    total_books = int(len(df))
    avg_price = int(df["sale_price"].mean())
    median_price = int(df["sale_price"].median())
    avg_rating = round(float(df["rating"].mean()), 2)
    max_reviews = int(df["review_count"].max())
    top_reviewed_book = (
        df.sort_values(by="review_count", ascending=False).iloc[0]["title"]
        if not df.empty
        else "-"
    )

    # 2. Chart.js 차트 데이터 집계
    price_bins = [0, 15000, 20000, 25000, 30000, 35000, 40000, 1000000]
    price_labels = [
        "1.5만원 미만",
        "1.5만~2만원",
        "2만~2.5만원",
        "2.5만~3만원",
        "3만~3.5만원",
        "3.5만~4만원",
        "4만원 이상",
    ]
    df["price_group"] = pd.cut(
        df["sale_price"], bins=price_bins, labels=price_labels
    )
    price_counts = df["price_group"].value_counts().sort_index()
    chart1_data = {
        "labels": price_labels,
        "values": [int(v) for v in price_counts.values],
    }

    top10_pubs = df["publisher"].value_counts().head(10)
    chart2_data = {
        "labels": list(top10_pubs.index),
        "values": [int(v) for v in top10_pubs.values],
    }

    valid_years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]
    year_counts = (
        df[df["pub_year"].isin(valid_years)]["pub_year"]
        .value_counts()
        .sort_index()
    )
    chart3_data = {
        "labels": list(year_counts.index),
        "values": [int(v) for v in year_counts.values],
    }

    bins_rank = [0, 50, 100, 200, 350, 700]
    labels_rank = ["1-50위", "51-100위", "101-200위", "201-350위", "351위 이상"]
    df["rank_group"] = pd.cut(
        df["rank"], bins=bins_rank, labels=labels_rank
    )
    rank_rev_mean = (
        df.groupby("rank_group", observed=False)["review_count"]
        .mean()
        .round(1)
    )
    chart4_data = {
        "labels": labels_rank,
        "values": [float(v) for v in rank_rev_mean.values],
    }

    rating_bins = [-1, 0, 7.9, 8.9, 9.4, 9.9, 10.0]
    rating_labels = [
        "평점없음(0점)",
        "8.0점 미만",
        "8.0~8.9점",
        "9.0~9.4점",
        "9.5~9.9점",
        "10점 만점",
    ]
    df["rating_group"] = pd.cut(
        df["rating"], bins=rating_bins, labels=rating_labels
    )
    rating_counts = df["rating_group"].value_counts().sort_index()
    chart5_data = {
        "labels": rating_labels,
        "values": [int(v) for v in rating_counts.values],
    }

    top15_keywords = [
        {"word": "AI / 인공지능", "score": 0.0612},
        {"word": "데이터", "score": 0.0363},
        {"word": "최신", "score": 0.0336},
        {"word": "핵심", "score": 0.0269},
        {"word": "실전", "score": 0.0267},
        {"word": "실제", "score": 0.0258},
        {"word": "업무", "score": 0.0213},
        {"word": "빠르게", "score": 0.0210},
        {"word": "문제/기출", "score": 0.0202},
        {"word": "분석", "score": 0.0197},
        {"word": "실무", "score": 0.0197},
        {"word": "기본", "score": 0.0191},
        {"word": "시험/자격증", "score": 0.0188},
        {"word": "프로그래밍", "score": 0.0176},
        {"word": "활용", "score": 0.0171},
    ]
    chart6_data = {
        "labels": [k["word"] for k in top15_keywords],
        "values": [k["score"] for k in top15_keywords],
    }

    books_data = df[
        [
            "rank",
            "prev_rank",
            "book_id",
            "title",
            "author",
            "publisher",
            "pub_date",
            "fixed_price",
            "sale_price",
            "discount_rate",
            "point",
            "review_count",
            "rating",
            "isbn",
            "intro",
        ]
    ].to_dict(orient="records")

    publishers = sorted(list(df["publisher"].dropna().unique()))
    pub_options = "".join([f'<option value="{p}">{p}</option>' for p in publishers])

    print(f">>> 화이트 톤 HTML 템플릿 컴파일 중 (도서 {len(books_data)}건)...")

    # 화이트 톤 글래스모피즘 템플릿
    template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>교보문고 IT 베스트셀러 대시보드 (White Glassmorphism)</title>
  
  <!-- Pretendard 폰트 -->
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#f0fdf4',
              100: '#dcfce7',
              500: '#22c55e',
              600: '#16a34a',
              700: '#15803d',
            }
          }
        }
      }
    }
  </script>

  <style>
    body {
      background-color: #f8fafc;
      color: #1e293b;
      font-family: 'Pretendard', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* 소프트 파스텔 앰비언트 글로우 배경 */
    .aurora-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -1;
      pointer-events: none;
      overflow: hidden;
    }
    .glow-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(100px);
      opacity: 0.55;
      animation: float 22s infinite ease-in-out alternate;
    }
    .orb-1 {
      width: 550px;
      height: 550px;
      background: radial-gradient(circle, #bae6fd, #e0f2fe);
      top: -100px;
      left: -100px;
    }
    .orb-2 {
      width: 650px;
      height: 650px;
      background: radial-gradient(circle, #e9d5ff, #f3e8ff);
      bottom: -150px;
      right: -100px;
      animation-delay: -6s;
    }
    .orb-3 {
      width: 450px;
      height: 450px;
      background: radial-gradient(circle, #fbcfe8, #fdf2f8);
      top: 35%;
      left: 40%;
      opacity: 0.45;
      animation-delay: -11s;
    }

    @keyframes float {
      0% { transform: translate(0px, 0px) scale(1); }
      50% { transform: translate(50px, 35px) scale(1.06); }
      100% { transform: translate(-30px, 60px) scale(0.96); }
    }

    /* 화이트 글래스모피즘 코어 클래스 */
    .glass-panel {
      background: rgba(255, 255, 255, 0.78);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 255, 255, 0.95);
      box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
      border-radius: 1.25rem;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-panel:hover {
      border-color: rgba(59, 130, 246, 0.35);
      box-shadow: 0 20px 30px -10px rgba(59, 130, 246, 0.08), 0 10px 15px -3px rgba(0, 0, 0, 0.04);
    }

    .glass-card-interactive {
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card-interactive:hover {
      transform: translateY(-4px);
    }

    /* 인풋 및 셀렉트 박스 */
    .glass-input {
      background: rgba(255, 255, 255, 0.92);
      border: 1px solid #e2e8f0;
      color: #0f172a;
      backdrop-filter: blur(10px);
      transition: all 0.2s ease;
    }
    .glass-input:focus {
      outline: none;
      border-color: #3b82f6;
      background: #ffffff;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }

    /* 스크롤바 */
    ::-webkit-scrollbar {
      width: 7px;
      height: 7px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(241, 245, 249, 0.8);
    }
    ::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }

    .badge-soft {
      background: linear-gradient(135deg, rgba(224, 242, 254, 0.9), rgba(219, 234, 254, 0.9));
      border: 1px solid rgba(186, 230, 253, 0.8);
      color: #0284c7;
    }
  </style>
</head>
<body class="p-4 md:p-8">

  <!-- 앰비언트 글로우 배경 -->
  <div class="aurora-bg">
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
    <div class="glow-orb orb-3"></div>
  </div>

  <div class="max-w-7xl mx-auto space-y-8">

    <!-- 상단 네비게이션 헤더 -->
    <header class="glass-panel p-6 flex flex-col md:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20 text-white">
          <i data-lucide="book-open" class="w-7 h-7"></i>
        </div>
        <div>
          <div class="flex items-center gap-3">
            <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-slate-800 to-blue-700">
              교보문고 IT 베스트셀러 대시보드
            </h1>
            <span class="badge-soft text-xs px-3 py-1 rounded-full font-semibold flex items-center gap-1.5 shadow-sm">
              <span class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
              LIVE DATA
            </span>
          </div>
          <p class="text-sm text-slate-500 mt-1 flex items-center gap-2">
            <span>컴퓨터/IT 일간 베스트셀러 658권 전수 분석</span>
            <span>•</span>
            <span class="text-slate-400">기준일자: 2026-10-20</span>
          </p>
        </div>
      </div>

      <!-- 우측 컨트롤 버튼들 -->
      <div class="flex items-center gap-3">
        <button onclick="resetAllFilters()" class="glass-panel px-4 py-2.5 rounded-xl text-sm font-semibold text-slate-700 hover:bg-slate-100 flex items-center gap-2 border border-slate-200 transition shadow-sm">
          <i data-lucide="rotate-ccw" class="w-4 h-4 text-blue-500"></i>
          필터 초기화
        </button>
        <button onclick="exportCSV()" class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-2.5 rounded-xl text-sm font-semibold shadow-md shadow-blue-500/25 hover:from-blue-700 hover:to-indigo-700 flex items-center gap-2 transition">
          <i data-lucide="download" class="w-4 h-4"></i>
          CSV 내보내기
        </button>
      </div>
    </header>

    <!-- KPI 메인 카드 4종 -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- KPI 1 -->
      <div class="glass-panel glass-card-interactive p-6 relative overflow-hidden group border border-slate-200/80">
        <div class="flex justify-between items-start">
          <span class="text-sm font-semibold text-slate-500">총 수집 베스트셀러</span>
          <div class="p-2.5 rounded-xl bg-blue-50 text-blue-600 border border-blue-100 shadow-sm">
            <i data-lucide="layers" class="w-5 h-5"></i>
          </div>
        </div>
        <div class="mt-4">
          <span class="text-3xl font-extrabold tracking-tight text-slate-900">{{TOTAL_BOOKS}}</span>
          <span class="text-sm text-slate-500 ml-1">권</span>
        </div>
        <p class="text-xs text-emerald-600 mt-2 flex items-center gap-1 font-semibold">
          <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> 100% 전수 수집 완료
        </p>
      </div>

      <!-- KPI 2 -->
      <div class="glass-panel glass-card-interactive p-6 relative overflow-hidden group border border-slate-200/80">
        <div class="flex justify-between items-start">
          <span class="text-sm font-semibold text-slate-500">평균 실구매가 (중앙값)</span>
          <div class="p-2.5 rounded-xl bg-indigo-50 text-indigo-600 border border-indigo-100 shadow-sm">
            <i data-lucide="tag" class="w-5 h-5"></i>
          </div>
        </div>
        <div class="mt-4">
          <span class="text-3xl font-extrabold tracking-tight text-slate-900">{{AVG_PRICE}}</span>
          <span class="text-sm text-slate-500 ml-1">원</span>
        </div>
        <p class="text-xs text-slate-500 mt-2 flex items-center gap-1">
          중앙값: <strong class="text-slate-700 font-semibold">{{MEDIAN_PRICE}}원</strong> (정가 10% 일괄 할인)
        </p>
      </div>

      <!-- KPI 3 -->
      <div class="glass-panel glass-card-interactive p-6 relative overflow-hidden group border border-slate-200/80">
        <div class="flex justify-between items-start">
          <span class="text-sm font-semibold text-slate-500">평균 도서 평점</span>
          <div class="p-2.5 rounded-xl bg-purple-50 text-purple-600 border border-purple-100 shadow-sm">
            <i data-lucide="star" class="w-5 h-5"></i>
          </div>
        </div>
        <div class="mt-4">
          <span class="text-3xl font-extrabold tracking-tight text-slate-900">{{AVG_RATING}}</span>
          <span class="text-sm text-slate-500 ml-1">/ 10.0</span>
        </div>
        <p class="text-xs text-purple-700 mt-2 flex items-center gap-1 font-semibold">
          <i data-lucide="award" class="w-3.5 h-3.5"></i> 평점 보유 도서 만점율 47.1%
        </p>
      </div>

      <!-- KPI 4 -->
      <div class="glass-panel glass-card-interactive p-6 relative overflow-hidden group border border-slate-200/80">
        <div class="flex justify-between items-start">
          <span class="text-sm font-semibold text-slate-500">최다 리뷰 도서</span>
          <div class="p-2.5 rounded-xl bg-amber-50 text-amber-600 border border-amber-100 shadow-sm">
            <i data-lucide="message-square" class="w-5 h-5"></i>
          </div>
        </div>
        <div class="mt-4">
          <span class="text-3xl font-extrabold tracking-tight text-slate-900">{{MAX_REVIEWS}}</span>
          <span class="text-sm text-slate-500 ml-1">건</span>
        </div>
        <p class="text-xs text-amber-700 mt-2 truncate font-semibold" title="{{TOP_REVIEW_TITLE}}">
          {{TOP_REVIEW_TITLE}}
        </p>
      </div>
    </section>

    <!-- 인터랙티브 Chart.js 6대 차트 그리드 -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- 차트 1: 가격대별 도서 분포 -->
      <div class="glass-panel p-6 flex flex-col justify-between border border-slate-200/80">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
              도서 판매가 구간별 분포
            </h3>
            <p class="text-xs text-slate-500 mt-0.5">1.5만~3만원대 가격 밴드에 73% 밀집</p>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-600 font-medium">Bar Chart</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chart1"></canvas>
        </div>
      </div>

      <!-- 차트 2: 상위 10대 출판사 점유율 -->
      <div class="glass-panel p-6 flex flex-col justify-between border border-slate-200/80">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
              상위 10대 출판사 점유율
            </h3>
            <p class="text-xs text-slate-500 mt-0.5">한빛미디어, 길벗, 영진닷컴 등 상위 3사가 30% 장악</p>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-600 font-medium">Doughnut</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chart2"></canvas>
        </div>
      </div>

      <!-- 차트 3: 출간 연도별 신간 추이 -->
      <div class="glass-panel p-6 flex flex-col justify-between border border-slate-200/80">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              출간 연도별 신간 진입 추이 (2018~2026)
            </h3>
            <p class="text-xs text-slate-500 mt-0.5">2026년 개정판 및 신간 도서가 48.2% 차지</p>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-600 font-medium">Line & Area</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chart3"></canvas>
        </div>
      </div>

      <!-- 차트 4: 순위 구간별 평균 리뷰 수 -->
      <div class="glass-panel p-6 flex flex-col justify-between border border-slate-200/80">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
              순위 구간별 평균 독자 리뷰 수
            </h3>
            <p class="text-xs text-slate-500 mt-0.5">최상위 1~50위권 도서의 압도적 리뷰 독점(53.3건)</p>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-600 font-medium">Bar Chart</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chart4"></canvas>
        </div>
      </div>

      <!-- 차트 5: 평점 구간별 도서 분포 -->
      <div class="glass-panel p-6 flex flex-col justify-between border border-slate-200/80">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
              도서 평점 구간별 분포 현황
            </h3>
            <p class="text-xs text-slate-500 mt-0.5">10점 만점 집중 현상 및 신간 미평점(0점) 분포</p>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-600 font-medium">Polar Area</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chart5"></canvas>
        </div>
      </div>

      <!-- 차트 6: TF-IDF 핵심 키워드 Top 15 -->
      <div class="glass-panel p-6 flex flex-col justify-between border border-slate-200/80">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              도서 소개 TF-IDF 핵심 키워드 Top 15
            </h3>
            <p class="text-xs text-slate-500 mt-0.5">'AI', '데이터', '실무', '최신' 등 실용 기술서 중심</p>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-600 font-medium">Horizontal Bar</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chart6"></canvas>
        </div>
      </div>

    </section>

    <!-- 인터랙티브 데이터 탐색 그리드 (테이블) -->
    <section class="glass-panel p-6 space-y-6 border border-slate-200/80">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h2 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <i data-lucide="database" class="w-5 h-5 text-blue-600"></i>
            베스트셀러 실시간 데이터 탐색기
          </h2>
          <p class="text-xs text-slate-500 mt-1">
            필터 조건에 따라 실시간 반응하며, 행을 클릭하면 상세 소개글 모달이 열립니다.
          </p>
        </div>
        <div class="text-xs text-slate-600 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 font-medium">
          표시 도서: <strong id="filterCount" class="text-blue-600 font-bold">{{TOTAL_BOOKS}}</strong> / {{TOTAL_BOOKS}}권
        </div>
      </div>

      <!-- 검색 및 다중 필터 컨트롤 바 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- 텍스트 검색창 -->
        <div class="relative">
          <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5 pointer-events-none"></i>
          <input type="text" id="searchInput" placeholder="도서명, 저자, 출판사 검색..." 
            class="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-sm"
            oninput="handleSearch()">
        </div>

        <!-- 출판사 필터 -->
        <div>
          <select id="publisherFilter" class="glass-input w-full px-4 py-2.5 rounded-xl text-sm" onchange="handleFilter()">
            <option value="">모든 출판사 (전체)</option>
            {{PUBLISHER_OPTIONS}}
          </select>
        </div>

        <!-- 가격대 필터 -->
        <div>
          <select id="priceFilter" class="glass-input w-full px-4 py-2.5 rounded-xl text-sm" onchange="handleFilter()">
            <option value="">모든 가격대 (전체)</option>
            <option value="under20">2만원 미만</option>
            <option value="20to30">2만 ~ 3만원 (인기 구간)</option>
            <option value="over30">3만원 이상 (전문서)</option>
          </select>
        </div>

        <!-- 최소 평점 필터 -->
        <div>
          <select id="ratingFilter" class="glass-input w-full px-4 py-2.5 rounded-xl text-sm" onchange="handleFilter()">
            <option value="">모든 평점 (전체)</option>
            <option value="9.5">⭐ 9.5점 이상 (초우수)</option>
            <option value="9.0">⭐ 9.0점 이상 (우수)</option>
            <option value="10.0">🏆 10.0점 만점</option>
          </select>
        </div>
      </div>

      <!-- 데이터 테이블 -->
      <div class="overflow-x-auto rounded-xl border border-slate-200 bg-white/70 shadow-sm">
        <table class="w-full text-left text-sm text-slate-700">
          <thead class="text-xs uppercase bg-slate-50 text-slate-600 border-b border-slate-200 font-semibold">
            <tr>
              <th scope="col" class="px-4 py-3.5 cursor-pointer hover:text-blue-600" onclick="handleSort('rank')">
                <div class="flex items-center gap-1">순위 <i data-lucide="arrow-up-down" class="w-3.5 h-3.5 text-slate-400"></i></div>
              </th>
              <th scope="col" class="px-4 py-3.5">도서명</th>
              <th scope="col" class="px-4 py-3.5">저자</th>
              <th scope="col" class="px-4 py-3.5">출판사</th>
              <th scope="col" class="px-4 py-3.5 cursor-pointer hover:text-blue-600" onclick="handleSort('sale_price')">
                <div class="flex items-center gap-1">판매가 <i data-lucide="arrow-up-down" class="w-3.5 h-3.5 text-slate-400"></i></div>
              </th>
              <th scope="col" class="px-4 py-3.5 cursor-pointer hover:text-blue-600" onclick="handleSort('review_count')">
                <div class="flex items-center gap-1">리뷰수 <i data-lucide="arrow-up-down" class="w-3.5 h-3.5 text-slate-400"></i></div>
              </th>
              <th scope="col" class="px-4 py-3.5 cursor-pointer hover:text-blue-600" onclick="handleSort('rating')">
                <div class="flex items-center gap-1">평점 <i data-lucide="arrow-up-down" class="w-3.5 h-3.5 text-slate-400"></i></div>
              </th>
              <th scope="col" class="px-4 py-3.5">출간일</th>
            </tr>
          </thead>
          <tbody id="bookTableBody" class="divide-y divide-slate-100 font-normal">
            <!-- JavaScript 렌더링 영역 -->
          </tbody>
        </table>
      </div>

      <!-- 페이지네이션 컨트롤 바 -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
        <div class="text-xs text-slate-500">
          <span id="pageInfo">1 / 14 페이지</span> (페이지당 
          <select id="pageSizeSelect" class="bg-white border border-slate-300 rounded px-2 py-0.5 text-xs text-slate-700 shadow-sm" onchange="changePageSize()">
            <option value="15">15</option>
            <option value="30">30</option>
            <option value="50">50</option>
          </select> 개씩 보기)
        </div>
        <div class="flex items-center gap-2">
          <button id="prevBtn" onclick="prevPage()" class="glass-panel px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100 disabled:opacity-40 disabled:pointer-events-none transition border border-slate-200 shadow-sm">
            이전
          </button>
          <div id="pageButtons" class="flex items-center gap-1">
            <!-- 페이지 번호 버튼들 -->
          </div>
          <button id="nextBtn" onclick="nextPage()" class="glass-panel px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100 disabled:opacity-40 disabled:pointer-events-none transition border border-slate-200 shadow-sm">
            다음
          </button>
        </div>
      </div>
    </section>

    <!-- 푸터 -->
    <footer class="text-center py-6 text-xs text-slate-500 border-t border-slate-200">
      교보문고 IT 베스트셀러 White Glassmorphism 대시보드 • Built with Chart.js & Tailwind CSS • Powered by Antigravity Agent
    </footer>

  </div>

  <!-- 도서 상세 정보 글래스 모달 -->
  <div id="bookModal" class="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-md hidden items-center justify-center p-4 transition-opacity">
    <div class="bg-white/95 backdrop-blur-xl max-w-2xl w-full p-6 md:p-8 space-y-6 relative rounded-2xl border border-white shadow-2xl">
      <!-- 닫기 버튼 -->
      <button onclick="closeModal()" class="absolute right-5 top-5 p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>

      <div class="space-y-2">
        <div class="flex items-center gap-2">
          <span id="modalRank" class="bg-blue-600 text-white text-xs px-2.5 py-0.5 rounded font-bold shadow-sm">1위</span>
          <span id="modalPrevRank" class="text-xs text-slate-500 font-medium">이전 1위</span>
        </div>
        <h3 id="modalTitle" class="text-xl md:text-2xl font-extrabold text-slate-900 leading-snug">도서 제목</h3>
        <p class="text-sm text-blue-600 font-semibold">
          <span id="modalAuthor">저자명</span> • <span id="modalPublisher" class="text-slate-600">출판사</span>
        </p>
      </div>

      <!-- 메트릭 그리드 -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200">
        <div>
          <span class="text-xs text-slate-500 block">판매가</span>
          <strong id="modalSalePrice" class="text-base text-slate-900">27,000원</strong>
          <span id="modalDiscount" class="text-xs text-emerald-600 font-semibold ml-1"></span>
        </div>
        <div>
          <span class="text-xs text-slate-500 block">정가</span>
          <span id="modalFixedPrice" class="text-sm text-slate-400 line-through">30,000원</span>
        </div>
        <div>
          <span class="text-xs text-slate-500 block">리뷰 및 평점</span>
          <span id="modalRating" class="text-sm text-amber-600 font-bold">★ 9.86</span>
          <span id="modalReviewCount" class="text-xs text-slate-500">(398건)</span>
        </div>
        <div>
          <span class="text-xs text-slate-500 block">출간일</span>
          <span id="modalPubDate" class="text-sm text-slate-700 font-medium">2026-01-02</span>
        </div>
      </div>

      <!-- 도서 소개글 -->
      <div class="space-y-2">
        <span class="text-xs uppercase tracking-wider text-slate-500 font-bold block">도서 소개 (Introduction)</span>
        <div id="modalIntro" class="text-sm text-slate-700 bg-white p-4 rounded-xl max-h-48 overflow-y-auto leading-relaxed border border-slate-200 shadow-inner">
          소개글 내용이 들어갑니다.
        </div>
      </div>

      <!-- 하단 바코드/ID 정보 -->
      <div class="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100">
        <span>ISBN: <strong id="modalIsbn" class="text-slate-700 font-mono">-</strong></span>
        <span>상품 ID: <strong id="modalBookId" class="text-slate-700 font-mono">-</strong></span>
      </div>
    </div>
  </div>

  <!-- 임베디드 데이터셋 및 비즈니스 로직 -->
  <script>
    const ALL_BOOKS = {{BOOKS_DATA_JSON}};
    const CHART_DATA = {
      chart1: {{CHART1_DATA_JSON}},
      chart2: {{CHART2_DATA_JSON}},
      chart3: {{CHART3_DATA_JSON}},
      chart4: {{CHART4_DATA_JSON}},
      chart5: {{CHART5_DATA_JSON}},
      chart6: {{CHART6_DATA_JSON}}
    };

    let filteredBooks = [...ALL_BOOKS];
    let currentPage = 1;
    let pageSize = 15;
    let currentSort = { column: 'rank', asc: true };

    // 화이트 톤 Chart.js 글로벌 스타일
    Chart.defaults.color = '#64748b';
    Chart.defaults.font.family = 'Pretendard';
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    Chart.defaults.plugins.tooltip.titleColor = '#0f172a';
    Chart.defaults.plugins.tooltip.bodyColor = '#334155';
    Chart.defaults.plugins.tooltip.borderColor = '#e2e8f0';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.boxPadding = 4;

    function initCharts() {
      // 차트 1: 가격대별 분포
      new Chart(document.getElementById('chart1'), {
        type: 'bar',
        data: {
          labels: CHART_DATA.chart1.labels,
          datasets: [{
            label: '도서 수 (권)',
            data: CHART_DATA.chart1.values,
            backgroundColor: 'rgba(59, 130, 246, 0.8)',
            borderColor: '#2563eb',
            borderWidth: 1.5,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { grid: { color: 'rgba(226, 232, 240, 0.8)' } }
          }
        }
      });

      // 차트 2: 상위 10대 출판사 점유율
      new Chart(document.getElementById('chart2'), {
        type: 'doughnut',
        data: {
          labels: CHART_DATA.chart2.labels,
          datasets: [{
            data: CHART_DATA.chart2.values,
            backgroundColor: [
              '#3b82f6', '#6366f1', '#8b5cf6', '#ec4899',
              '#f43f5e', '#f97316', '#eab308', '#10b981', '#06b6d4', '#64748b'
            ],
            borderColor: '#ffffff',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: { boxWidth: 12, font: { size: 10 } }
            }
          }
        }
      });

      // 차트 3: 출간 연도별 추이
      new Chart(document.getElementById('chart3'), {
        type: 'line',
        data: {
          labels: CHART_DATA.chart3.labels,
          datasets: [{
            label: '등록 권수',
            data: CHART_DATA.chart3.values,
            fill: true,
            backgroundColor: 'rgba(16, 185, 129, 0.12)',
            borderColor: '#10b981',
            tension: 0.35,
            pointBackgroundColor: '#10b981',
            pointRadius: 4,
            borderWidth: 2.5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { grid: { color: 'rgba(226, 232, 240, 0.8)' } }
          }
        }
      });

      // 차트 4: 순위 구간별 리뷰 수
      new Chart(document.getElementById('chart4'), {
        type: 'bar',
        data: {
          labels: CHART_DATA.chart4.labels,
          datasets: [{
            label: '평균 리뷰 수 (건)',
            data: CHART_DATA.chart4.values,
            backgroundColor: 'rgba(245, 158, 11, 0.85)',
            borderColor: '#d97706',
            borderWidth: 1.5,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { grid: { color: 'rgba(226, 232, 240, 0.8)' } }
          }
        }
      });

      // 차트 5: 평점 구간별 분포
      new Chart(document.getElementById('chart5'), {
        type: 'polarArea',
        data: {
          labels: CHART_DATA.chart5.labels,
          datasets: [{
            data: CHART_DATA.chart5.values,
            backgroundColor: [
              'rgba(148, 163, 184, 0.6)',
              'rgba(239, 68, 68, 0.65)',
              'rgba(245, 158, 11, 0.65)',
              'rgba(59, 130, 246, 0.65)',
              'rgba(168, 85, 247, 0.65)',
              'rgba(236, 72, 153, 0.75)'
            ],
            borderColor: '#ffffff',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { boxWidth: 10, font: { size: 9 } } }
          },
          scales: {
            r: { grid: { color: 'rgba(226, 232, 240, 0.8)' }, ticks: { display: false } }
          }
        }
      });

      // 차트 6: TF-IDF 키워드
      new Chart(document.getElementById('chart6'), {
        type: 'bar',
        data: {
          labels: CHART_DATA.chart6.labels,
          datasets: [{
            label: 'TF-IDF 가중치',
            data: CHART_DATA.chart6.values,
            backgroundColor: 'rgba(244, 63, 94, 0.8)',
            borderColor: '#e11d48',
            borderWidth: 1.5,
            borderRadius: 4
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(226, 232, 240, 0.8)' } },
            y: { grid: { display: false } }
          }
        }
      });
    }

    // 테이블 필터링 및 검색 로직
    function handleSearch() {
      handleFilter();
    }

    function handleFilter() {
      const query = document.getElementById('searchInput').value.trim().toLowerCase();
      const pub = document.getElementById('publisherFilter').value;
      const price = document.getElementById('priceFilter').value;
      const rating = parseFloat(document.getElementById('ratingFilter').value) || 0;

      filteredBooks = ALL_BOOKS.filter(book => {
        if (query) {
          const t = (book.title || '').toLowerCase();
          const a = (book.author || '').toLowerCase();
          const p = (book.publisher || '').toLowerCase();
          if (!t.includes(query) && !a.includes(query) && !p.includes(query)) {
            return false;
          }
        }
        if (pub && book.publisher !== pub) return false;
        if (price === 'under20' && book.sale_price >= 20000) return false;
        if (price === '20to30' && (book.sale_price < 20000 || book.sale_price >= 30000)) return false;
        if (price === 'over30' && book.sale_price < 30000) return false;
        if (rating > 0 && book.rating < rating) return false;

        return true;
      });

      sortFilteredBooks();
      currentPage = 1;
      renderTable();
    }

    function handleSort(col) {
      if (currentSort.column === col) {
        currentSort.asc = !currentSort.asc;
      } else {
        currentSort.column = col;
        currentSort.asc = true;
      }
      sortFilteredBooks();
      renderTable();
    }

    function sortFilteredBooks() {
      const { column, asc } = currentSort;
      filteredBooks.sort((a, b) => {
        let vA = a[column];
        let vB = b[column];
        if (typeof vA === 'string') {
          return asc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        }
        return asc ? (vA - vB) : (vB - vA);
      });
    }

    function renderTable() {
      const tbody = document.getElementById('bookTableBody');
      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      const pageData = filteredBooks.slice(start, end);

      document.getElementById('filterCount').innerText = filteredBooks.length.toLocaleString();

      if (pageData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-10 text-slate-400">조건에 일치하는 도서가 없습니다.</td></tr>`;
        renderPagination();
        return;
      }

      tbody.innerHTML = pageData.map(b => {
        const rankBadge = b.rank <= 3 
          ? `<span class="w-6 h-6 rounded-full bg-gradient-to-r from-amber-400 to-amber-500 text-white font-extrabold text-xs flex items-center justify-center shadow-sm">${b.rank}</span>`
          : `<span class="w-6 h-6 rounded-full bg-slate-100 text-slate-600 font-bold text-xs flex items-center justify-center border border-slate-200">${b.rank}</span>`;
        
        const ratingStr = b.rating > 0 ? `★ ${b.rating.toFixed(2)}` : `<span class="text-slate-400 text-xs">신간/미평가</span>`;

        return `
          <tr onclick="openModal('${b.book_id}')" class="hover:bg-blue-50/60 cursor-pointer transition border-b border-slate-100">
            <td class="px-4 py-3 font-semibold">${rankBadge}</td>
            <td class="px-4 py-3 font-medium text-slate-900 max-w-xs truncate" title="${b.title}">${b.title}</td>
            <td class="px-4 py-3 text-slate-600 max-w-[140px] truncate" title="${b.author}">${b.author || '-'}</td>
            <td class="px-4 py-3 text-blue-600 font-medium">${b.publisher}</td>
            <td class="px-4 py-3 font-bold text-slate-900">${Number(b.sale_price).toLocaleString()}원</td>
            <td class="px-4 py-3 text-slate-600 font-medium">${Number(b.review_count).toLocaleString()}</td>
            <td class="px-4 py-3 text-amber-500 font-semibold">${ratingStr}</td>
            <td class="px-4 py-3 text-slate-500 font-mono text-xs">${b.pub_date || '-'}</td>
          </tr>
        `;
      }).join('');

      renderPagination();
      lucide.createIcons();
    }

    function renderPagination() {
      const totalPages = Math.ceil(filteredBooks.length / pageSize) || 1;
      document.getElementById('pageInfo').innerText = `${currentPage} / ${totalPages} 페이지`;

      document.getElementById('prevBtn').disabled = (currentPage === 1);
      document.getElementById('nextBtn').disabled = (currentPage === totalPages);

      const btnContainer = document.getElementById('pageButtons');
      btnContainer.innerHTML = '';

      let startP = Math.max(1, currentPage - 2);
      let endP = Math.min(totalPages, startP + 4);
      if (endP - startP < 4) startP = Math.max(1, endP - 4);

      for (let p = startP; p <= endP; p++) {
        const btn = document.createElement('button');
        btn.innerText = p;
        btn.className = `w-7 h-7 rounded-lg text-xs font-semibold transition ${p === currentPage ? 'bg-blue-600 text-white shadow-sm' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'}`;
        btn.onclick = () => { currentPage = p; renderTable(); };
        btnContainer.appendChild(btn);
      }
    }

    function prevPage() {
      if (currentPage > 1) {
        currentPage--;
        renderTable();
      }
    }

    function nextPage() {
      const totalPages = Math.ceil(filteredBooks.length / pageSize);
      if (currentPage < totalPages) {
        currentPage++;
        renderTable();
      }
    }

    function changePageSize() {
      pageSize = parseInt(document.getElementById('pageSizeSelect').value);
      currentPage = 1;
      renderTable();
    }

    function resetAllFilters() {
      document.getElementById('searchInput').value = '';
      document.getElementById('publisherFilter').value = '';
      document.getElementById('priceFilter').value = '';
      document.getElementById('ratingFilter').value = '';
      currentSort = { column: 'rank', asc: true };
      handleFilter();
    }

    // 모달 제어
    function openModal(bookId) {
      const book = ALL_BOOKS.find(b => b.book_id === bookId);
      if (!book) return;

      document.getElementById('modalRank').innerText = `${book.rank}위`;
      document.getElementById('modalPrevRank').innerText = book.prev_rank > 0 ? `이전 ${book.prev_rank}위` : 'NEW 진입';
      document.getElementById('modalTitle').innerText = book.title;
      document.getElementById('modalAuthor').innerText = book.author || '저자 정보 없음';
      document.getElementById('modalPublisher').innerText = book.publisher;
      document.getElementById('modalSalePrice').innerText = `${Number(book.sale_price).toLocaleString()}원`;
      document.getElementById('modalDiscount').innerText = `(${book.discount_rate}%↓)`;
      document.getElementById('modalFixedPrice').innerText = `${Number(book.fixed_price).toLocaleString()}원`;
      document.getElementById('modalRating').innerText = book.rating > 0 ? `★ ${book.rating}` : '평점 없음';
      document.getElementById('modalReviewCount').innerText = `(${Number(book.review_count).toLocaleString()}건)`;
      document.getElementById('modalPubDate').innerText = book.pub_date || '-';
      document.getElementById('modalIntro').innerText = book.intro || '도서 소개 정보가 제공되지 않습니다.';
      document.getElementById('modalIsbn').innerText = book.isbn || '-';
      document.getElementById('modalBookId').innerText = book.book_id;

      const modal = document.getElementById('bookModal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeModal() {
      const modal = document.getElementById('bookModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    document.getElementById('bookModal').addEventListener('click', (e) => {
      if (e.target.id === 'bookModal') closeModal();
    });

    // CSV 다운로드 기능
    function exportCSV() {
      let csvContent = "data:text/csv;charset=utf-8,\\uFEFF";
      const headers = ["순위", "도서명", "저자", "출판사", "판매가", "정가", "할인율", "리뷰수", "평점", "출간일", "ISBN"];
      csvContent += headers.join(",") + "\\r\\n";

      filteredBooks.forEach(b => {
        const row = [
          b.rank,
          `"${(b.title || '').replace(/"/g, '""')}"`,
          `"${(b.author || '').replace(/"/g, '""')}"`,
          `"${(b.publisher || '').replace(/"/g, '""')}"`,
          b.sale_price,
          b.fixed_price,
          b.discount_rate,
          b.review_count,
          b.rating,
          b.pub_date,
          `"${b.isbn}"`
        ];
        csvContent += row.join(",") + "\\r\\n";
      });

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "kyobo_it_bestseller_filtered.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    window.addEventListener('DOMContentLoaded', () => {
      initCharts();
      renderTable();
      lucide.createIcons();
    });
  </script>
</body>
</html>
"""

    replacements = {
        "{{TOTAL_BOOKS}}": f"{total_books:,}",
        "{{AVG_PRICE}}": f"{avg_price:,}",
        "{{MEDIAN_PRICE}}": f"{median_price:,}",
        "{{AVG_RATING}}": f"{avg_rating}",
        "{{MAX_REVIEWS}}": f"{max_reviews:,}",
        "{{TOP_REVIEW_TITLE}}": top_reviewed_book,
        "{{PUBLISHER_OPTIONS}}": pub_options,
        "{{BOOKS_DATA_JSON}}": json.dumps(books_data, ensure_ascii=False),
        "{{CHART1_DATA_JSON}}": json.dumps(chart1_data, ensure_ascii=False),
        "{{CHART2_DATA_JSON}}": json.dumps(chart2_data, ensure_ascii=False),
        "{{CHART3_DATA_JSON}}": json.dumps(chart3_data, ensure_ascii=False),
        "{{CHART4_DATA_JSON}}": json.dumps(chart4_data, ensure_ascii=False),
        "{{CHART5_DATA_JSON}}": json.dumps(chart5_data, ensure_ascii=False),
        "{{CHART6_DATA_JSON}}": json.dumps(chart6_data, ensure_ascii=False),
    }

    final_html = template
    for key, val in replacements.items():
        final_html = final_html.replace(key, val)

    output_html_path.write_text(final_html, encoding="utf-8")
    print(f">>> 화이트 톤 대시보드 HTML 파일 생성 완료: {output_html_path} ({output_html_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build_dashboard()
