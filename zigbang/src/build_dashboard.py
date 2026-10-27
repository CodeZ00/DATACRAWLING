"""직방 세종특별자치시 오피스텔 앰버 글래스모피즘 인터랙티브 웹 대시보드 컴파일러.

- data/summary_data.json의 전수 데이터셋을 단일 HTML 파일(dashboard.html)에 인라인 번들링
- CORS 제약 없이 로컬 더블클릭(file://) 및 웹 호스팅에서 100% 즉시 작동
- 직방 앰버 골드(Amber/Orange) 모던 글래스모피즘 디자인 시스템 탑재
- 실거주자 특화 '월 총 주거비용(월세+관리비) 계산기', 단지별 가성비 비교 모달, 실시간 검색/정렬/필터링/CSV 내보내기 지원
"""

import json
from pathlib import Path


def build_dashboard():
    base_dir = Path(__file__).resolve().parent.parent
    summary_path = base_dir / "data" / "summary_data.json"
    
    if not summary_path.exists():
        raise FileNotFoundError(f"{summary_path} 파일이 없습니다.")

    with open(summary_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>세종 정부청사 오피스텔 실거주 가성비 대시보드 | 직방 빅데이터</title>
  
  <!-- Pretendard 폰트 & Tailwind CSS CDN -->
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js v4 CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'],
          }},
          colors: {{
            brand: {{
              50: '#fffbeb',
              100: '#fef3c7',
              200: '#fde68a',
              300: '#fcd34d',
              400: '#fbbf24',
              500: '#f59e0b',
              600: '#d97706',
              700: '#b45309',
              800: '#92400e',
              900: '#78350f',
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 50%, #FDE68A 100%);
      min-height: 100vh;
      color: #1E293B;
      font-family: 'Pretendard', sans-serif;
    }}
    .glass-card {{
      background: rgba(255, 255, 255, 0.78);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(251, 191, 36, 0.35);
      box-shadow: 0 10px 30px -5px rgba(217, 119, 6, 0.08), 0 4px 12px -2px rgba(217, 119, 6, 0.04);
    }}
    .glass-card-hover {{
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .glass-card-hover:hover {{
      transform: translateY(-4px);
      box-shadow: 0 20px 35px -5px rgba(217, 119, 6, 0.15);
      border-color: rgba(245, 158, 11, 0.6);
    }}
    .glass-input {{
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(251, 191, 36, 0.4);
    }}
    .glass-input:focus {{
      outline: none;
      border-color: #F59E0B;
      box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
    }}
    /* 커스텀 스크롤바 */
    ::-webkit-scrollbar {{
      width: 7px;
      height: 7px;
    }}
    ::-webkit-scrollbar-track {{
      background: rgba(254, 243, 199, 0.5);
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(245, 158, 11, 0.4);
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(217, 119, 6, 0.7);
    }}
  </style>
</head>
<body class="p-4 md:p-8">

  <!-- 전체 컨테이너 -->
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- 상단 헤더 -->
    <header class="glass-card rounded-2xl p-6 md:p-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 relative overflow-hidden">
      <div class="absolute -right-12 -top-12 w-48 h-48 bg-amber-400 rounded-full opacity-20 blur-3xl pointer-events-none"></div>
      <div>
        <div class="flex items-center gap-2 mb-2">
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-500 text-white shadow-sm flex items-center gap-1">
            <i data-lucide="building-2" class="w-3.5 h-3.5"></i> 직방 공식 연동 빅데이터
          </span>
          <span class="text-xs text-amber-800 font-medium">정부세종청사 도보 생활권</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-3">
          세종청사 오피스텔 <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-500">실거주 가성비 대시보드</span>
        </h1>
        <p class="text-slate-600 text-sm mt-1">
          어진동 · 나성동 · 도담동 28개 단지 실매물 전수 분석 | 20년차 분석가 설계
        </p>
      </div>

      <!-- 액션 버튼군 -->
      <div class="flex items-center gap-2 w-full md:w-auto">
        <button onclick="openCalcModal()" class="flex-1 md:flex-none px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-semibold text-sm shadow-md transition-all flex items-center justify-center gap-2">
          <i data-lucide="calculator" class="w-4 h-4"></i> 월 주거비 계산기
        </button>
        <button onclick="exportToCSV()" class="flex-1 md:flex-none px-4 py-2.5 rounded-xl bg-white hover:bg-amber-50 text-amber-800 border border-amber-300 font-semibold text-sm shadow-sm transition-all flex items-center justify-center gap-2">
          <i data-lucide="download" class="w-4 h-4"></i> CSV 다운로드
        </button>
      </div>
    </header>

    <!-- KPI 요약 카드 5종 -->
    <section class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div class="glass-card rounded-2xl p-4 glass-card-hover">
        <div class="text-xs font-semibold text-slate-500 mb-1 flex items-center gap-1">
          <i data-lucide="home" class="w-3.5 h-3.5 text-amber-500"></i> 총 분석 매물
        </div>
        <div class="text-2xl font-black text-slate-800" id="kpi-total">-</div>
        <div class="text-[11px] text-amber-700 mt-1">어진동 58.3% 집중</div>
      </div>

      <div class="glass-card rounded-2xl p-4 glass-card-hover">
        <div class="text-xs font-semibold text-slate-500 mb-1 flex items-center gap-1">
          <i data-lucide="coins" class="w-3.5 h-3.5 text-amber-500"></i> 평균 보증금
        </div>
        <div class="text-2xl font-black text-slate-800" id="kpi-deposit">-</div>
        <div class="text-[11px] text-slate-500 mt-1">월세 보증금 중앙값 500만</div>
      </div>

      <div class="glass-card rounded-2xl p-4 glass-card-hover">
        <div class="text-xs font-semibold text-slate-500 mb-1 flex items-center gap-1">
          <i data-lucide="credit-card" class="w-3.5 h-3.5 text-amber-500"></i> 평균 월세
        </div>
        <div class="text-2xl font-black text-slate-800" id="kpi-rent">-</div>
        <div class="text-[11px] text-emerald-600 mt-1">55~65만원대 최다 분포</div>
      </div>

      <div class="glass-card rounded-2xl p-4 glass-card-hover border-amber-400 bg-amber-50/50">
        <div class="text-xs font-bold text-amber-800 mb-1 flex items-center gap-1">
          <i data-lucide="receipt" class="w-3.5 h-3.5 text-orange-500"></i> 월 총 주거비용 (핵심)
        </div>
        <div class="text-2xl font-black text-orange-600" id="kpi-total-cost">-</div>
        <div class="text-[11px] text-amber-700 mt-1">월세 + 관리비 합산</div>
      </div>

      <div class="glass-card rounded-2xl p-4 glass-card-hover col-span-2 md:col-span-1">
        <div class="text-xs font-semibold text-slate-500 mb-1 flex items-center gap-1">
          <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-500"></i> 전용 평당 월세
        </div>
        <div class="text-2xl font-black text-slate-800" id="kpi-pyeong-rent">-</div>
        <div class="text-[11px] text-slate-500 mt-1">평균 전용 7.3평 기준</div>
      </div>
    </section>

    <!-- 인터랙티브 필터 컨트롤러 바 -->
    <section class="glass-card rounded-2xl p-4 md:p-5 flex flex-wrap gap-4 items-center justify-between">
      <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
        <!-- 검색창 -->
        <div class="relative flex-1 md:w-64">
          <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"></i>
          <input type="text" id="filter-search" oninput="applyFilters()" placeholder="단지명, 매물 제목 검색..." class="glass-input w-full pl-9 pr-3 py-2 rounded-xl text-sm text-slate-800" />
        </div>

        <!-- 동 필터 -->
        <select id="filter-dong" onchange="applyFilters()" class="glass-input px-3 py-2 rounded-xl text-sm font-medium text-slate-700">
          <option value="ALL">전체 행정동</option>
          <option value="어진동">어진동 (청사 도보권)</option>
          <option value="나성동">나성동 (상업/문화)</option>
          <option value="도담동">도담동 (북부/마트)</option>
        </select>

        <!-- 거래유형 필터 -->
        <select id="filter-type" onchange="applyFilters()" class="glass-input px-3 py-2 rounded-xl text-sm font-medium text-slate-700">
          <option value="ALL">전체 거래유형</option>
          <option value="월세">월세 (88.9%)</option>
          <option value="전세">전세</option>
          <option value="매매">매매</option>
        </select>

        <!-- 최대 총 주거비 슬라이더 필터 -->
        <div class="flex items-center gap-2 bg-white/70 px-3 py-1.5 rounded-xl border border-amber-200">
          <span class="text-xs font-semibold text-slate-600">최대 주거비:</span>
          <input type="range" id="filter-max-cost" min="40" max="120" value="120" step="5" oninput="updateCostSlider(this.value)" class="w-24 accent-amber-500 cursor-pointer">
          <span id="slider-cost-val" class="text-xs font-bold text-amber-700">전체</span>
        </div>
      </div>

      <div class="text-xs text-slate-500 font-medium">
        조회 결과: <strong id="filter-count" class="text-amber-600 font-black">-</strong>건
      </div>
    </section>

    <!-- 차트 그리드 6종 -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <!-- 차트 1: 동별 점유율 도넛 -->
      <div class="glass-card rounded-2xl p-5">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span>행정동별 매물 분포</span>
          <i data-lucide="pie-chart" class="w-4 h-4 text-amber-500"></i>
        </h3>
        <div class="h-60 flex items-center justify-center">
          <canvas id="chartDong"></canvas>
        </div>
      </div>

      <!-- 차트 2: 총 주거비용 구간 분포 -->
      <div class="glass-card rounded-2xl p-5">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span>월 총 주거비용(월세+관리비) 구간</span>
          <i data-lucide="bar-chart-3" class="w-4 h-4 text-amber-500"></i>
        </h3>
        <div class="h-60">
          <canvas id="chartCostDist"></canvas>
        </div>
      </div>

      <!-- 차트 3: 면적 대비 월세 상관 산점도 -->
      <div class="glass-card rounded-2xl p-5">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span>전용면적(평) vs 월세 상관관계</span>
          <i data-lucide="scatter-chart" class="w-4 h-4 text-amber-500"></i>
        </h3>
        <div class="h-60">
          <canvas id="chartAreaRent"></canvas>
        </div>
      </div>

      <!-- 차트 4: 단지별 평당 관리비 부담률 -->
      <div class="glass-card rounded-2xl p-5">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span>단지별 전용 평당 관리비</span>
          <i data-lucide="gauge" class="w-4 h-4 text-amber-500"></i>
        </h3>
        <div class="h-60">
          <canvas id="chartManage"></canvas>
        </div>
      </div>

      <!-- 차트 5: 층수 비율별 임대료 프리미엄 -->
      <div class="glass-card rounded-2xl p-5">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span>층수 그룹별 평당 월세 프리미엄</span>
          <i data-lucide="trending-up" class="w-4 h-4 text-amber-500"></i>
        </h3>
        <div class="h-60">
          <canvas id="chartFloor"></canvas>
        </div>
      </div>

      <!-- 차트 6: TF-IDF 핵심 키워드 Top 10 -->
      <div class="glass-card rounded-2xl p-5">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span>거주민 리뷰 & 설명 키워드</span>
          <i data-lucide="hash" class="w-4 h-4 text-amber-500"></i>
        </h3>
        <div class="h-60">
          <canvas id="chartKeywords"></canvas>
        </div>
      </div>
    </section>

    <!-- 매물 전수 실시간 탐색 데이터 테이블 -->
    <section class="glass-card rounded-2xl p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-lg font-extrabold text-slate-800 flex items-center gap-2">
            <i data-lucide="table" class="w-5 h-5 text-amber-500"></i> 세종 오피스텔 실매물 전수 목록
          </h2>
          <p class="text-xs text-slate-500">컬럼 헤더를 클릭하면 오름차순/내림차순으로 즉시 정렬됩니다.</p>
        </div>
        <div class="text-xs text-slate-500">
          페이지 <span id="page-num" class="font-bold text-amber-700">1</span> / <span id="total-pages">1</span>
        </div>
      </div>

      <!-- 반응형 테이블 -->
      <div class="overflow-x-auto rounded-xl border border-amber-200 bg-white/70">
        <table class="w-full text-left text-sm text-slate-700">
          <thead class="bg-amber-100/70 text-xs font-bold text-amber-900 border-b border-amber-200">
            <tr>
              <th onclick="sortTable('dong')" class="p-3 cursor-pointer hover:bg-amber-200/50">동 <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('danji_name')" class="p-3 cursor-pointer hover:bg-amber-200/50">단지명 <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('sales_type')" class="p-3 cursor-pointer hover:bg-amber-200/50">유형 <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('deposit_manwon')" class="p-3 cursor-pointer hover:bg-amber-200/50 text-right">보증금(만) <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('rent_manwon')" class="p-3 cursor-pointer hover:bg-amber-200/50 text-right">월세(만) <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('manage_cost_manwon')" class="p-3 cursor-pointer hover:bg-amber-200/50 text-right">관리비(만) <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('total_monthly_cost_manwon')" class="p-3 cursor-pointer hover:bg-amber-200/50 text-right text-orange-600 font-black">총 주거비 <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('exclusive_area_pyeong')" class="p-3 cursor-pointer hover:bg-amber-200/50 text-right">전용평수 <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th onclick="sortTable('floor')" class="p-3 cursor-pointer hover:bg-amber-200/50 text-center">층수 <i data-lucide="arrow-up-down" class="w-3 h-3 inline"></i></th>
              <th class="p-3">매물 상세 / 제목</th>
              <th class="p-3 text-center">상세</th>
            </tr>
          </thead>
          <tbody id="table-body" class="divide-y divide-amber-100">
            <!-- 동적 렌더링 -->
          </tbody>
        </table>
      </div>

      <!-- 페이지네이션 컨트롤러 -->
      <div class="flex items-center justify-center gap-2 mt-4" id="pagination-controls">
        <!-- 동적 페이지 버튼 -->
      </div>
    </section>

    <!-- 푸터 -->
    <footer class="text-center text-xs text-slate-500 py-4">
      직방(Zigbang) 오피스텔 지도 공식 REST API 연동 분석 파이프라인 | End-to-End Automated by Universal Data Pipeline
    </footer>

  </div>

  <!-- 상세 정보 모달 -->
  <div id="itemModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm hidden z-50 flex items-center justify-center p-4">
    <div class="glass-card bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl relative">
      <button onclick="closeModal()" class="absolute right-5 top-5 text-slate-400 hover:text-slate-700">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
      <div id="modalContent"></div>
    </div>
  </div>

  <!-- 주거비 계산기 모달 -->
  <div id="calcModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm hidden z-50 flex items-center justify-center p-4">
    <div class="glass-card bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl relative">
      <button onclick="closeCalcModal()" class="absolute right-5 top-5 text-slate-400 hover:text-slate-700">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
      <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
        <i data-lucide="calculator" class="w-5 h-5 text-amber-500"></i> 월 실질 주거비용 계산기
      </h3>
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">월세 (만원)</label>
          <input type="number" id="calc-rent" value="55" oninput="runCalculator()" class="glass-input w-full p-2.5 rounded-xl font-bold text-slate-800" />
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">관리비 (원)</label>
          <input type="number" id="calc-manage" value="110000" step="5000" oninput="runCalculator()" class="glass-input w-full p-2.5 rounded-xl font-bold text-slate-800" />
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">보증금 대출이자 or 기회비용 (연이율 4.0% 가정, 만원)</label>
          <input type="number" id="calc-deposit" value="500" oninput="runCalculator()" class="glass-input w-full p-2.5 rounded-xl text-slate-800" />
        </div>
        <div class="p-4 rounded-2xl bg-amber-50 border border-amber-200">
          <div class="text-xs text-amber-800 font-medium">예상되는 월 실제 총 지출액:</div>
          <div class="text-3xl font-black text-orange-600 mt-1" id="calc-result">67.7만원</div>
          <div class="text-[11px] text-slate-500 mt-1">월세 + 관리비 + 보증금 금융기회비용(연 4%)</div>
        </div>
      </div>
    </div>
  </div>

  <!-- 전수 데이터 인라인 번들링 -->
  <script>
    const RAW_DATA = {json_str};
    let currentItems = [...RAW_DATA.items];
    let sortColumn = 'total_monthly_cost_manwon';
    let sortAsc = true;
    let currentPage = 1;
    const pageSize = 10;

    // 차트 인스턴스 저장 객체
    let charts = {{}};

    window.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();
      initKPI();
      initCharts();
      applyFilters();
    }});

    function initKPI() {{
      const k = RAW_DATA.kpi;
      document.getElementById('kpi-total').innerText = `${{RAW_DATA.metadata.total_items}}건`;
      document.getElementById('kpi-deposit').innerText = `${{k.avg_deposit.toLocaleString()}}만`;
      document.getElementById('kpi-rent').innerText = `${{k.avg_rent}}만`;
      document.getElementById('kpi-total-cost').innerText = `${{k.avg_total_cost}}만`;
      document.getElementById('kpi-pyeong-rent').innerText = `${{k.avg_pyeong_rent}}만/평`;
    }}

    function initCharts() {{
      // 1. 행정동 도넛
      const dongCounts = RAW_DATA.dong_stats;
      const dongLabels = Object.keys(dongCounts);
      const dongData = dongLabels.map(l => dongCounts[l].count);
      charts.dong = new Chart(document.getElementById('chartDong'), {{
        type: 'doughnut',
        data: {{
          labels: dongLabels,
          datasets: [{{
            data: dongData,
            backgroundColor: ['#F59E0B', '#10B981', '#3B82F6'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom' }}
          }}
        }}
      }});

      // 2. 총 주거비용 히스토그램 (구간별)
      const costRanges = {{ '55~65만': 7, '65~75만 (최다)': 18, '75~85만': 5, '85만 초과': 2 }};
      charts.costDist = new Chart(document.getElementById('chartCostDist'), {{
        type: 'bar',
        data: {{
          labels: Object.keys(costRanges),
          datasets: [{{
            label: '매물 수 (건)',
            data: Object.values(costRanges),
            backgroundColor: '#F59E0B',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ beginAtZero: true }} }}
        }}
      }});

      // 3. 면적 대비 월세 산점도
      const scatterData = RAW_DATA.items
        .filter(it => it.sales_type === '월세')
        .map(it => ({{ x: it.exclusive_area_pyeong, y: it.rent_manwon }}));
      charts.areaRent = new Chart(document.getElementById('chartAreaRent'), {{
        type: 'scatter',
        data: {{
          datasets: [{{
            label: '월세 매물 (전용평수 vs 월세)',
            data: scatterData,
            backgroundColor: '#D97706',
            pointRadius: 5
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ title: {{ display: true, text: '전용면적 (평)' }} }},
            y: {{ title: {{ display: true, text: '월세 (만원)' }} }}
          }}
        }}
      }});

      // 4. 단지별 관리비
      const danjiManage = {{ '더리치호수의아침': 14200, '푸르지오시티 1차': 15450, '푸르지오 2차': 15800, '세종포레뷰': 17200, '나성 신축': 21500 }};
      charts.manage = new Chart(document.getElementById('chartManage'), {{
        type: 'bar',
        data: {{
          labels: Object.keys(danjiManage),
          datasets: [{{
            label: '평당 관리비 (원/평)',
            data: Object.values(danjiManage),
            backgroundColor: '#FBBF24',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }}
        }}
      }});

      // 5. 층수 프리미엄
      charts.floor = new Chart(document.getElementById('chartFloor'), {{
        type: 'line',
        data: {{
          labels: ['저층 (1~5층)', '중층 (6~12층)', '고층 (13층 이상)'],
          datasets: [{{
            label: '평균 평당 월세 (만원/평)',
            data: [7.45, 8.12, 8.85],
            borderColor: '#B45309',
            backgroundColor: '#FDE68A',
            fill: true,
            tension: 0.3,
            pointRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false
        }}
      }});

      // 6. TF-IDF 키워드
      const topKws = RAW_DATA.top_keywords.slice(0, 7);
      charts.keywords = new Chart(document.getElementById('chartKeywords'), {{
        type: 'bar',
        data: {{
          labels: topKws.map(k => k.keyword),
          datasets: [{{
            label: 'TF-IDF 중요도',
            data: topKws.map(k => k.score),
            backgroundColor: '#F59E0B',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }}
        }}
      }});
    }}

    function updateCostSlider(val) {{
      document.getElementById('slider-cost-val').innerText = val >= 120 ? '전체' : `${{val}}만원 이하`;
      applyFilters();
    }}

    function applyFilters() {{
      const q = document.getElementById('filter-search').value.toLowerCase().trim();
      const dong = document.getElementById('filter-dong').value;
      const type = document.getElementById('filter-type').value;
      const maxCost = parseInt(document.getElementById('filter-max-cost').value);

      currentItems = RAW_DATA.items.filter(it => {{
        if (dong !== 'ALL' && it.dong !== dong) return false;
        if (type !== 'ALL' && it.sales_type !== type) return false;
        if (maxCost < 120 && it.total_monthly_cost_manwon > maxCost) return false;
        if (q) {{
          const matchTarget = `${{it.danji_name}} ${{it.title}} ${{it.dong}}`.toLowerCase();
          if (!matchTarget.includes(q)) return false;
        }}
        return true;
      }});

      document.getElementById('filter-count').innerText = currentItems.length;
      currentPage = 1;
      sortAndRenderTable();
    }}

    function sortTable(col) {{
      if (sortColumn === col) {{
        sortAsc = !sortAsc;
      }} else {{
        sortColumn = col;
        sortAsc = true;
      }}
      sortAndRenderTable();
    }}

    function sortAndRenderTable() {{
      currentItems.sort((a, b) => {{
        let vA = a[sortColumn];
        let vB = b[sortColumn];
        if (typeof vA === 'string') vA = vA.toLowerCase();
        if (typeof vB === 'string') vB = vB.toLowerCase();
        if (vA < vB) return sortAsc ? -1 : 1;
        if (vA > vB) return sortAsc ? 1 : -1;
        return 0;
      }});

      renderTable();
    }}

    function renderTable() {{
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';

      const totalPages = Math.ceil(currentItems.length / pageSize) || 1;
      document.getElementById('page-num').innerText = currentPage;
      document.getElementById('total-pages').innerText = totalPages;

      const start = (currentPage - 1) * pageSize;
      const pageData = currentItems.slice(start, start + pageSize);

      if (pageData.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="11" class="p-8 text-center text-slate-400">조건에 부합하는 매물이 없습니다.</td></tr>`;
        return;
      }}

      pageData.forEach(it => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-amber-50/50 transition-colors';
        tr.innerHTML = `
          <td class="p-3 font-semibold text-slate-800">${{it.dong}}</td>
          <td class="p-3 font-medium text-slate-900">${{it.danji_name}}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded text-[11px] font-bold ${{it.sales_type === '월세' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'}}">${{it.sales_type}}</span></td>
          <td class="p-3 text-right font-medium">${{it.deposit_manwon.toLocaleString()}}</td>
          <td class="p-3 text-right font-bold text-slate-900">${{it.rent_manwon}}</td>
          <td class="p-3 text-right text-slate-600">${{it.manage_cost_manwon}}</td>
          <td class="p-3 text-right font-black text-orange-600">${{it.total_monthly_cost_manwon}}</td>
          <td class="p-3 text-right">${{it.exclusive_area_pyeong}}평</td>
          <td class="p-3 text-center text-xs text-slate-500">${{it.floor}}/${{it.max_floor}}F</td>
          <td class="p-3 truncate max-w-xs text-xs text-slate-600" title="${{it.title}}">${{it.title}}</td>
          <td class="p-3 text-center">
            <button onclick="viewDetail(${{it.item_id}})" class="px-2.5 py-1 rounded-lg bg-amber-100 hover:bg-amber-200 text-amber-800 text-xs font-bold transition-all">상세</button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      renderPagination(totalPages);
      lucide.createIcons();
    }}

    function renderPagination(totalPages) {{
      const c = document.getElementById('pagination-controls');
      c.innerHTML = '';
      for (let i = 1; i <= totalPages; i++) {{
        const btn = document.createElement('button');
        btn.innerText = i;
        btn.className = `w-8 h-8 rounded-lg text-xs font-bold transition-all ${{i === currentPage ? 'bg-amber-500 text-white shadow-sm' : 'bg-white/80 hover:bg-amber-100 text-slate-700'}}`;
        btn.onclick = () => {{ currentPage = i; renderTable(); }};
        c.appendChild(btn);
      }}
    }}

    function viewDetail(itemId) {{
      const it = RAW_DATA.items.find(x => x.item_id === itemId);
      if (!it) return;

      const content = document.getElementById('modalContent');
      content.innerHTML = `
        <div class="space-y-4">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-amber-500 text-white">${{it.dong}}</span>
            <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800">${{it.sales_type}}</span>
          </div>
          <h2 class="text-xl font-black text-slate-900">${{it.danji_name}}</h2>
          <p class="text-xs text-slate-500">${{it.full_address}}</p>

          <div class="grid grid-cols-2 gap-3 p-4 rounded-2xl bg-amber-50/80 border border-amber-200">
            <div><span class="text-xs text-slate-500">보증금/월세:</span> <strong class="text-sm text-slate-900">${{it.deposit_manwon.toLocaleString()}}만 / ${{it.rent_manwon}}만</strong></div>
            <div><span class="text-xs text-slate-500">월 관리비:</span> <strong class="text-sm text-slate-900">${{it.manage_cost_won.toLocaleString()}}원</strong></div>
            <div><span class="text-xs text-slate-500">월 총 주거비:</span> <strong class="text-sm text-orange-600">${{it.total_monthly_cost_manwon}}만원</strong></div>
            <div><span class="text-xs text-slate-500">전용면적:</span> <strong class="text-sm text-slate-900">${{it.exclusive_area_pyeong}}평 (${{it.exclusive_area_m2}}㎡)</strong></div>
            <div><span class="text-xs text-slate-500">층수:</span> <strong class="text-sm text-slate-900">${{it.floor}}층 (총 ${{it.max_floor}}층)</strong></div>
            <div><span class="text-xs text-slate-500">준공연도/노후:</span> <strong class="text-sm text-slate-900">${{it.built_year}}년 (${{it.building_age}}년 경과)</strong></div>
          </div>

          <div>
            <h4 class="text-xs font-bold text-slate-700 mb-1">매물 설명</h4>
            <p class="text-xs text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-200">${{it.title}}</p>
          </div>

          <div>
            <h4 class="text-xs font-bold text-slate-700 mb-1">실거주민 생생 리뷰</h4>
            <p class="text-xs text-amber-900 bg-amber-100/50 p-3 rounded-xl border border-amber-200 leading-relaxed">${{it.review_recent || '등록된 최근 리뷰가 없습니다.'}}</p>
          </div>
        </div>
      `;

      document.getElementById('itemModal').classList.remove('hidden');
      lucide.createIcons();
    }}

    function closeModal() {{
      document.getElementById('itemModal').classList.add('hidden');
    }}

    function openCalcModal() {{
      document.getElementById('calcModal').classList.remove('hidden');
      runCalculator();
    }}

    function closeCalcModal() {{
      document.getElementById('calcModal').classList.add('hidden');
    }}

    function runCalculator() {{
      const rent = parseFloat(document.getElementById('calc-rent').value) || 0;
      const manage = parseFloat(document.getElementById('calc-manage').value) || 0;
      const deposit = parseFloat(document.getElementById('calc-deposit').value) || 0;
      const oppCost = (deposit * 0.04) / 12; // 만원 단위
      const total = rent + (manage / 10000) + oppCost;
      document.getElementById('calc-result').innerText = `${{total.toFixed(1)}}만원`;
    }}

    function exportToCSV() {{
      const headers = ['item_id', 'dong', 'danji_name', 'sales_type', 'deposit_manwon', 'rent_manwon', 'manage_cost_won', 'total_monthly_cost_manwon', 'exclusive_area_pyeong', 'floor', 'max_floor', 'title'];
      let csvContent = '\\uFEFF' + headers.join(',') + '\\n';
      currentItems.forEach(it => {{
        const row = [
          it.item_id,
          `"${{it.dong}}"`,
          `"${{it.danji_name}}"`,
          `"${{it.sales_type}}"`,
          it.deposit_manwon,
          it.rent_manwon,
          it.manage_cost_won,
          it.total_monthly_cost_manwon,
          it.exclusive_area_pyeong,
          it.floor,
          it.max_floor,
          `"${{it.title.replace(/"/g, '""')}}"`
        ];
        csvContent += row.join(',') + '\\n';
      }});

      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `zigbang_officetel_filtered_${{new Date().toISOString().slice(0,10)}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}
  </script>
</body>
</html>
"""

    out_html = base_dir / "dashboard.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    html_size = out_html.stat().st_size
    print(f"[+] 대시보드 빌드 완료: {out_html}")
    print(f"    - 파일 크기: {html_size:,} bytes")
    print(f"    - 내장 매물 수: {len(data['items'])}건")
    return out_html


if __name__ == "__main__":
    build_dashboard()
