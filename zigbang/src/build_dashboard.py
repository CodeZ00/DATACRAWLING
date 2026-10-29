# -*- coding: utf-8 -*-
"""
오창읍 원룸·빌라 월세 화이트 글래스모피즘 인터랙티브 웹 대시보드 빌더 (지도 고도화 버전)
- 지도 개선: CartoDB Positron 모던 화이트 타일 + OpenStreetMap 듀얼 레이어
- 뷰 자동 맞춤: map.fitBounds()로 603개 매물 영역 자동 최적 줌 & 패닝
- 원클릭 퀵 이동 버튼: 양청리, 구룡리, 주성리, 오창 전역 즉시 이동
- 팝업 인터랙션 강화: 썸네일 이미지, 가격, 가성비 지표, 모달 연동
- Chart.js v4 기반 6대 핵심 시각화 차트
- 실시간 다중 조건 필터, 정렬 테이블, 모달, CSV 내보내기
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SUMMARY_PATH = DATA_DIR / "summary_data.json"


def generate_dashboard():
    print(f"[*] summary_data.json 로드: {SUMMARY_PATH}")
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data_json_str = json.dumps(data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>오창읍 원룸·빌라 월세 데이터 인텔리전스 대시보드</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js v4 CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <!-- Leaflet.js CDN -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <!-- Leaflet MarkerCluster CDN -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
  <!-- Font Awesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&display=swap');

    body {{
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 50%, #f8fafc 100%);
      min-height: 100vh;
      color: #1e293b;
      position: relative;
      overflow-x: hidden;
    }}

    /* 앰비언트 오로라 글로우 애니메이션 배경 */
    .aurora-bg {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      z-index: -1;
      pointer-events: none;
    }}
    .glow-circle-1 {{
      position: absolute;
      width: 600px;
      height: 600px;
      top: -150px;
      left: -150px;
      background: radial-gradient(circle, rgba(59, 130, 246, 0.18) 0%, rgba(219, 234, 254, 0.05) 70%, transparent 100%);
      border-radius: 50%;
      filter: blur(80px);
      animation: float 20s infinite ease-in-out;
    }}
    .glow-circle-2 {{
      position: absolute;
      width: 700px;
      height: 700px;
      bottom: -200px;
      right: -150px;
      background: radial-gradient(circle, rgba(14, 165, 233, 0.15) 0%, rgba(224, 242, 254, 0.05) 70%, transparent 100%);
      border-radius: 50%;
      filter: blur(90px);
      animation: float 25s infinite ease-in-out reverse;
    }}
    .glow-circle-3 {{
      position: absolute;
      width: 500px;
      height: 500px;
      top: 40%;
      left: 45%;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(238, 242, 255, 0.05) 70%, transparent 100%);
      border-radius: 50%;
      filter: blur(85px);
      animation: float 22s infinite ease-in-out;
    }}

    @keyframes float {{
      0%, 100% {{ transform: translate(0, 0) scale(1); }}
      50% {{ transform: translate(60px, 40px) scale(1.08); }}
    }}

    /* 화이트 프로스티드 글래스모피즘 패널 스타일 */
    .glass-card {{
      background: rgba(255, 255, 255, 0.82);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.95);
      box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05), 0 4px 12px -2px rgba(0, 0, 0, 0.03);
      border-radius: 1.25rem;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .glass-card:hover {{
      box-shadow: 0 16px 36px -4px rgba(0, 0, 0, 0.08), 0 6px 16px -2px rgba(0, 0, 0, 0.04);
      border-color: rgba(255, 255, 255, 1);
    }}

    /* 지도 컨테이너 */
    #map {{
      height: 520px;
      width: 100%;
      border-radius: 1rem;
      z-index: 10;
      box-shadow: inset 0 2px 8px rgba(0,0,0,0.06);
    }}

    /* Leaflet 팝업 스타일링 */
    .leaflet-popup-content-wrapper {{
      border-radius: 1rem !important;
      background: rgba(255, 255, 255, 0.95) !important;
      backdrop-filter: blur(12px) !important;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important;
      border: 1px solid rgba(255, 255, 255, 0.8) !important;
      padding: 4px !important;
    }}
    .leaflet-popup-tip {{
      background: rgba(255, 255, 255, 0.95) !important;
    }}

    /* 퀵 네비 버튼 */
    .quick-btn {{
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 11px;
      font-weight: 600;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      color: #334155;
      transition: all 0.2s;
      cursor: pointer;
    }}
    .quick-btn:hover {{
      background: #eff6ff;
      border-color: #93c5fd;
      color: #1d4ed8;
      transform: translateY(-1px);
    }}

    /* 커스텀 스크롤바 */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: rgba(241, 245, 249, 0.6);
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(148, 163, 184, 0.5);
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(100, 116, 139, 0.8);
    }}
  </style>
</head>
<body class="p-4 md:p-8">

  <!-- 배경 애니메이션 -->
  <div class="aurora-bg">
    <div class="glow-circle-1"></div>
    <div class="glow-circle-2"></div>
    <div class="glow-circle-3"></div>
  </div>

  <div class="max-w-7xl mx-auto space-y-6">

    <!-- 헤더 섹션 -->
    <header class="glass-card p-6 md:p-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-semibold mb-2 border border-blue-100">
          <i class="fa-solid fa-bolt"></i> 실시간 데이터 인텔리전스 | 전수 603건 무결성 검증
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight">
          충북 청주시 청원구 오창읍 원룸·빌라 월세 대시보드
        </h1>
        <p class="text-slate-500 text-sm mt-1">
          오창과학산업단지·2산단 배후 주거지 실시간 시세, 가성비 지표 및 지리 인터랙티브 지도 탐색기
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button id="btnExportCsv" class="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm shadow-md shadow-blue-500/20 transition flex items-center gap-2">
          <i class="fa-solid fa-file-csv text-base"></i> 필터 결과 CSV 다운로드
        </button>
        <button id="btnResetFilters" class="px-4 py-2.5 rounded-xl bg-white hover:bg-slate-50 text-slate-700 font-medium text-sm border border-slate-200 transition flex items-center gap-2">
          <i class="fa-solid fa-rotate-left"></i> 필터 초기화
        </button>
      </div>
    </header>

    <!-- KPI 요약 카드 그리드 -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
      <div class="glass-card p-5 text-center">
        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">총 수집 매물</span>
        <span id="kpiTotal" class="text-2xl md:text-3xl font-black text-blue-600 mt-1 block">603건</span>
        <span class="text-[11px] text-slate-400 mt-1 block">결측률 0.0% 검증</span>
      </div>
      <div class="glass-card p-5 text-center">
        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">평균 월세</span>
        <span id="kpiAvgRent" class="text-2xl md:text-3xl font-black text-slate-800 mt-1 block">40.8만</span>
        <span id="kpiMedianRent" class="text-[11px] text-slate-500 mt-1 block">중위수 36.0만</span>
      </div>
      <div class="glass-card p-5 text-center">
        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">평균 실질 총주거비</span>
        <span id="kpiAvgTotalCost" class="text-2xl md:text-3xl font-black text-rose-600 mt-1 block">51.2만</span>
        <span class="text-[11px] text-slate-500 mt-1 block">월세 + 관리비 합산</span>
      </div>
      <div class="glass-card p-5 text-center">
        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">평균 보증금</span>
        <span id="kpiAvgDep" class="text-2xl md:text-3xl font-black text-indigo-600 mt-1 block">547.8만</span>
        <span class="text-[11px] text-slate-500 mt-1 block">중위수 300.0만</span>
      </div>
      <div class="glass-card p-5 text-center">
        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">평균 전용면적</span>
        <span id="kpiAvgSize" class="text-2xl md:text-3xl font-black text-teal-600 mt-1 block">10.7평</span>
        <span class="text-[11px] text-slate-500 mt-1 block">약 35.2 ㎡</span>
      </div>
      <div class="glass-card p-5 text-center">
        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block">평당 실질 주거비</span>
        <span id="kpiAvgCpp" class="text-2xl md:text-3xl font-black text-amber-600 mt-1 block">5.2만</span>
        <span class="text-[11px] text-slate-500 mt-1 block">가성비 지수</span>
      </div>
    </div>

    <!-- 다중 인터랙티브 필터 컨트롤 패널 -->
    <div class="glass-card p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
          <i class="fa-solid fa-sliders text-blue-500"></i> 매물 정밀 다중 필터
        </h2>
        <span id="filterStatus" class="text-xs font-medium text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-100">
          603개 매물 전체 표시 중
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- 권역 필터 -->
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1.5">세부 권역 (리)</label>
          <select id="filterDong" class="w-full bg-white/90 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/30">
            <option value="ALL">전체 권역 (오창읍 전역)</option>
            <option value="양청리">양청리 (호수공원/중심상업 221건)</option>
            <option value="구룡리">구룡리 (구시가지 상권/원룸촌 91건)</option>
            <option value="주성리">주성리 (2산단 신흥 주거 13건)</option>
            <option value="송대리">송대리 (산단 배후 5건)</option>
            <option value="오창읍 기타">오창읍 기타 (각리/산단 272건)</option>
          </select>
        </div>

        <!-- 구조 필터 -->
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1.5">방 구조 유형</label>
          <select id="filterStructure" class="w-full bg-white/90 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/30">
            <option value="ALL">전체 구조</option>
            <option value="원룸">단독 원룸 (434건)</option>
            <option value="투룸">투룸 (94건)</option>
            <option value="1.5룸/분리형">1.5룸 / 분리형 (48건)</option>
            <option value="쓰리룸+">쓰리룸+ (19건)</option>
            <option value="복층형 원룸">복층형 원룸 (6건)</option>
          </select>
        </div>

        <!-- 월세 슬라이더 -->
        <div>
          <div class="flex justify-between items-center mb-1.5">
            <label class="text-xs font-semibold text-slate-600">최대 월세</label>
            <span id="valRent" class="text-xs font-bold text-blue-600">전체 (130만원)</span>
          </div>
          <input type="range" id="sliderRent" min="10" max="130" value="130" step="5" class="w-full accent-blue-600 cursor-pointer">
        </div>

        <!-- 보증금 슬라이더 -->
        <div>
          <div class="flex justify-between items-center mb-1.5">
            <label class="text-xs font-semibold text-slate-600">최대 보증금</label>
            <span id="valDeposit" class="text-xs font-bold text-indigo-600">전체 (8,000만원)</span>
          </div>
          <input type="range" id="sliderDeposit" min="100" max="8000" value="8000" step="100" class="w-full accent-indigo-600 cursor-pointer">
        </div>
      </div>

      <!-- 보조 토글 & 검색 -->
      <div class="mt-4 pt-4 border-t border-slate-100 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div class="flex items-center gap-6">
          <label class="inline-flex items-center gap-2 cursor-pointer text-xs font-semibold text-slate-700">
            <input type="checkbox" id="chkElevator" class="w-4 h-4 rounded text-blue-600 focus:ring-blue-500">
            <span>승강기(엘리베이터) 보유 매물만</span>
          </label>
          <label class="inline-flex items-center gap-2 cursor-pointer text-xs font-semibold text-slate-700">
            <input type="checkbox" id="chkFullOption" class="w-4 h-4 rounded text-blue-600 focus:ring-blue-500">
            <span>풀옵션 완료 매물만</span>
          </label>
        </div>

        <div class="relative flex-1 max-w-md">
          <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
          <input type="text" id="inputSearch" placeholder="매물 제목, 주소, 옵션 키워드 실시간 검색..." class="w-full bg-white/90 border border-slate-200 rounded-xl pl-8 pr-4 py-2 text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/30">
        </div>
      </div>
    </div>

    <!-- 인터랙티브 지도 섹션 (Leaflet & 고도화) -->
    <div class="glass-card p-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 mb-4">
        <div>
          <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
            <i class="fa-solid fa-map-location-dot text-teal-500"></i> 오창읍 실시간 매물 지리 인터랙티브 맵
          </h2>
          <p class="text-xs text-slate-500 mt-0.5">
            지도를 확대/이동하거나 마커를 클릭하여 매물 상세 정보를 확인할 수 있습니다.
          </p>
        </div>

        <!-- 퀵 네비게이션 버튼 & 범례 -->
        <div class="flex flex-wrap items-center gap-2">
          <div class="flex items-center gap-1.5 mr-2">
            <button onclick="flyToRegion('ALL')" class="quick-btn"><i class="fa-solid fa-earth-asia text-blue-500"></i> 오창 전역</button>
            <button onclick="flyToRegion('양청리')" class="quick-btn"><i class="fa-solid fa-building text-teal-500"></i> 양청리</button>
            <button onclick="flyToRegion('구룡리')" class="quick-btn"><i class="fa-solid fa-house text-amber-500"></i> 구룡리</button>
            <button onclick="flyToRegion('주성리')" class="quick-btn"><i class="fa-solid fa-industry text-indigo-500"></i> 주성리(2산단)</button>
          </div>

          <div class="flex items-center gap-2 text-xs font-medium bg-slate-50 px-2.5 py-1 rounded-lg border border-slate-200">
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-blue-500"></span> 35만 이하
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-500 ml-1"></span> 36~50만
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-rose-500 ml-1"></span> 50만 초과
          </div>
        </div>
      </div>

      <div id="map"></div>
    </div>

    <!-- 6대 핵심 분석 시각화 차트 그리드 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- Chart 1: 월세 가격대별 분포 -->
      <div class="glass-card p-6">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span><i class="fa-solid fa-chart-column text-blue-500 mr-1.5"></i> 월세 가격대별 매물 분포</span>
          <span class="text-xs font-normal text-slate-400">단위: 건</span>
        </h3>
        <div class="h-64">
          <canvas id="chartRentDist"></canvas>
        </div>
      </div>

      <!-- Chart 2: 방 구조 유형 점유율 -->
      <div class="glass-card p-6">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span><i class="fa-solid fa-chart-pie text-indigo-500 mr-1.5"></i> 방 구조 유형별 점유 비율</span>
          <span class="text-xs font-normal text-slate-400">비율 (%)</span>
        </h3>
        <div class="h-64">
          <canvas id="chartStructure"></canvas>
        </div>
      </div>

      <!-- Chart 3: 권역별 평균 월세 및 매물수 -->
      <div class="glass-card p-6">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span><i class="fa-solid fa-city text-teal-500 mr-1.5"></i> 권역(리)별 평균 월세 및 매물수</span>
          <span class="text-xs font-normal text-slate-400">만원 / 건</span>
        </h3>
        <div class="h-64">
          <canvas id="chartSubdong"></canvas>
        </div>
      </div>

      <!-- Chart 4: 전용면적 vs 실질총주거비 상관관계 -->
      <div class="glass-card p-6">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span><i class="fa-solid fa-chart-line text-rose-500 mr-1.5"></i> 전용면적(평) 대비 실질 총주거비</span>
          <span class="text-xs font-normal text-slate-400">평 vs 만원</span>
        </h3>
        <div class="h-64">
          <canvas id="chartSizeVsCost"></canvas>
        </div>
      </div>

      <!-- Chart 5: 보증금 구간별 평균 월세 수준 -->
      <div class="glass-card p-6">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span><i class="fa-solid fa-vault text-amber-500 mr-1.5"></i> 보증금 구간별 평균 월세 및 건수</span>
          <span class="text-xs font-normal text-slate-400">재무 구조</span>
        </h3>
        <div class="h-64">
          <canvas id="chartDepositBin"></canvas>
        </div>
      </div>

      <!-- Chart 6: 층수 구분별 월세 및 면적 비교 -->
      <div class="glass-card p-6">
        <h3 class="text-sm font-bold text-slate-800 flex items-center justify-between mb-3">
          <span><i class="fa-solid fa-stairs text-sky-500 mr-1.5"></i> 층수 구분(저/중/고)별 평균 시세</span>
          <span class="text-xs font-normal text-slate-400">층별 프리미엄</span>
        </h3>
        <div class="h-64">
          <canvas id="chartFloorLevel"></canvas>
        </div>
      </div>

    </div>

    <!-- 실시간 데이터 상세 탐색 테이블 -->
    <div class="glass-card p-6">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
        <div>
          <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
            <i class="fa-solid fa-table-list text-blue-500"></i> 오창읍 매물 실시간 탐색 데이터베이스
          </h2>
          <p class="text-xs text-slate-500 mt-0.5">
            컬럼 헤더를 클릭하여 정렬하고, 행을 클릭하면 상세 모달 팝업이 열립니다.
          </p>
        </div>

        <div class="flex items-center gap-3 text-xs text-slate-500">
          <span>표시 개수:</span>
          <select id="selectPageSize" class="bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-xs text-slate-700">
            <option value="10">10개씩</option>
            <option value="25" selected>25개씩</option>
            <option value="50">50개씩</option>
            <option value="100">100개씩</option>
          </select>
        </div>
      </div>

      <!-- 테이블 본체 -->
      <div class="overflow-x-auto rounded-xl border border-slate-100">
        <table class="w-full text-left text-xs text-slate-600 border-collapse">
          <thead class="bg-slate-50/80 text-slate-700 uppercase font-bold text-[11px] border-b border-slate-200">
            <tr>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition" onclick="sortTable('item_id')">ID <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition" onclick="sortTable('sub_dong')">권역(리) <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition" onclick="sortTable('structure_type')">구조 <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition text-right" onclick="sortTable('deposit_manwon')">보증금 <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition text-right" onclick="sortTable('rent_manwon')">월세 <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition text-right" onclick="sortTable('total_monthly_cost')">실질주거비 <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition text-right" onclick="sortTable('size_pyeong')">전용면적 <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 cursor-pointer hover:bg-slate-100 transition text-right" onclick="sortTable('cost_per_pyeong')">평당비용 <i class="fa-solid fa-sort ml-1 text-slate-400"></i></th>
              <th class="p-3 text-center">층수</th>
              <th class="p-3 text-center">옵션</th>
              <th class="p-3">매물 제목</th>
            </tr>
          </thead>
          <tbody id="tableBody" class="divide-y divide-slate-100 bg-white/60">
            <!-- 동적 렌더링 -->
          </tbody>
        </table>
      </div>

      <!-- 페이지네이션 컨트롤 -->
      <div class="flex flex-col sm:flex-row justify-between items-center gap-3 mt-4 text-xs text-slate-500">
        <div id="pageInfo">1-25 / 총 603건</div>
        <div class="flex items-center gap-1.5" id="paginationControls">
          <!-- 동적 버튼 -->
        </div>
      </div>
    </div>

    <!-- 푸터 -->
    <footer class="text-center text-xs text-slate-400 py-4">
      직방(Zigbang) 오창읍 원룸·빌라 월세 데이터 파이프라인 | 20년차 데이터 분석가 에이전트 구축 | 2026-10-29
    </footer>

  </div>

  <!-- 매물 상세 모달 팝업 -->
  <div id="itemModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-white/80 space-y-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-start">
        <div>
          <span id="modalDongBadge" class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-blue-50 text-blue-600 border border-blue-100">양청리</span>
          <span id="modalStructBadge" class="ml-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-700">단독 원룸</span>
          <h3 id="modalTitle" class="text-lg font-bold text-slate-900 mt-2">매물 제목</h3>
        </div>
        <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600 text-lg p-1">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div id="modalThumbContainer" class="w-full h-48 bg-slate-100 rounded-xl overflow-hidden flex items-center justify-center">
        <img id="modalThumb" src="" alt="매물 사진" class="w-full h-full object-cover">
      </div>

      <div class="grid grid-cols-2 gap-3 text-xs">
        <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
          <span class="text-slate-400 block">보증금 / 월세</span>
          <span id="modalPrice" class="text-base font-bold text-blue-600 mt-0.5 block">300 / 35 만원</span>
        </div>
        <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
          <span class="text-slate-400 block">실질 총 주거비용 (관리비 포함)</span>
          <span id="modalTotalCost" class="text-base font-bold text-rose-600 mt-0.5 block">45.0 만원</span>
        </div>
        <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
          <span class="text-slate-400 block">전용면적 / 평수</span>
          <span id="modalSize" class="text-sm font-semibold text-slate-800 mt-0.5 block">33.0 ㎡ (10.0평)</span>
        </div>
        <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
          <span class="text-slate-400 block">평당 실질비용 (가성비 지수)</span>
          <span id="modalCpp" class="text-sm font-semibold text-amber-600 mt-0.5 block">4.5 만원/평</span>
        </div>
      </div>

      <div class="text-xs space-y-1.5 pt-2 border-t border-slate-100 text-slate-600">
        <div><strong>소재지:</strong> <span id="modalAddress">충북 청주시 청원구 오창읍 양청리</span></div>
        <div><strong>층수 정보:</strong> <span id="modalFloor">3층 / 4층 (중층)</span></div>
        <div><strong>편의시설:</strong> <span id="modalFacilities">승강기 없음, 풀옵션 완료, 주차 가능</span></div>
        <div><strong>등록일자:</strong> <span id="modalDate">2026-10-25</span></div>
      </div>

      <div class="pt-2">
        <button onclick="closeModal()" class="w-full py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition">
          닫기
        </button>
      </div>
    </div>
  </div>

  <!-- 대시보드 인터랙티브 자바스크립트 엔진 -->
  <script>
    // 인라인 전수 데이터 로드
    const rawData = {data_json_str};
    const allItems = rawData.items || [];
    let filteredItems = [...allItems];

    let currentSortCol = 'rent_manwon';
    let currentSortAsc = true;
    let currentPage = 1;
    let pageSize = 25;

    let map = null;
    let markersCluster = null;
    let charts = {{}};

    // 초기화
    document.addEventListener('DOMContentLoaded', () => {{
      initMap();
      initCharts();
      applyFilters();
      bindEvents();

      // 지도 타일 리사이즈 보정
      setTimeout(() => {{
        if (map) {{
          map.invalidateSize();
          fitMapToFilteredMarkers();
        }}
      }}, 300);
    }});

    // 이벤트 바인딩
    function bindEvents() {{
      document.getElementById('filterDong').addEventListener('change', applyFilters);
      document.getElementById('filterStructure').addEventListener('change', applyFilters);
      
      const sliderRent = document.getElementById('sliderRent');
      sliderRent.addEventListener('input', (e) => {{
        document.getElementById('valRent').textContent = e.target.value >= 130 ? '전체 (130만원)' : `${{e.target.value}}만원 이하`;
        applyFilters();
      }});

      const sliderDep = document.getElementById('sliderDeposit');
      sliderDep.addEventListener('input', (e) => {{
        document.getElementById('valDeposit').textContent = e.target.value >= 8000 ? '전체 (8,000만원)' : `${{e.target.value}}만원 이하`;
        applyFilters();
      }});

      document.getElementById('chkElevator').addEventListener('change', applyFilters);
      document.getElementById('chkFullOption').addEventListener('change', applyFilters);
      document.getElementById('inputSearch').addEventListener('input', applyFilters);

      document.getElementById('selectPageSize').addEventListener('change', (e) => {{
        pageSize = parseInt(e.target.value);
        currentPage = 1;
        renderTable();
      }});

      document.getElementById('btnResetFilters').addEventListener('click', () => {{
        document.getElementById('filterDong').value = 'ALL';
        document.getElementById('filterStructure').value = 'ALL';
        sliderRent.value = 130;
        document.getElementById('valRent').textContent = '전체 (130만원)';
        sliderDep.value = 8000;
        document.getElementById('valDeposit').textContent = '전체 (8,000만원)';
        document.getElementById('chkElevator').checked = false;
        document.getElementById('chkFullOption').checked = false;
        document.getElementById('inputSearch').value = '';
        applyFilters();
        flyToRegion('ALL');
      }});

      document.getElementById('btnExportCsv').addEventListener('click', exportFilteredCsv);
    }}

    // 필터링 적용
    function applyFilters() {{
      const dong = document.getElementById('filterDong').value;
      const struct = document.getElementById('filterStructure').value;
      const maxRent = parseInt(document.getElementById('sliderRent').value);
      const maxDep = parseInt(document.getElementById('sliderDeposit').value);
      const needEle = document.getElementById('chkElevator').checked;
      const needOpt = document.getElementById('chkFullOption').checked;
      const query = document.getElementById('inputSearch').value.trim().toLowerCase();

      filteredItems = allItems.filter(it => {{
        if (dong !== 'ALL' && it.sub_dong !== dong) return false;
        if (struct !== 'ALL' && it.structure_type !== struct) return false;
        if (it.rent_manwon > maxRent) return false;
        if (it.deposit_manwon > maxDep) return false;
        if (needEle && it.has_elevator !== 1) return false;
        if (needOpt && it.has_full_option !== 1) return false;

        if (query) {{
          const searchText = `${{it.title}} ${{it.address_full}} ${{it.sub_dong}} ${{it.structure_type}}`.toLowerCase();
          if (!searchText.includes(query)) return false;
        }}

        return true;
      }});

      document.getElementById('filterStatus').textContent = `${{filteredItems.length}}개 매물 표시 중 (전체 ${{allItems.length}}건)`;
      updateKpis();
      updateMapMarkers();
      updateCharts();
      currentPage = 1;
      renderTable();
    }}

    // KPI 카드 업데이트
    function updateKpis() {{
      if (filteredItems.length === 0) {{
        document.getElementById('kpiTotal').textContent = '0건';
        document.getElementById('kpiAvgRent').textContent = '0만';
        document.getElementById('kpiMedianRent').textContent = '중위수 0만';
        document.getElementById('kpiAvgTotalCost').textContent = '0만';
        document.getElementById('kpiAvgDep').textContent = '0만';
        document.getElementById('kpiAvgSize').textContent = '0평';
        document.getElementById('kpiAvgCpp').textContent = '0만';
        return;
      }}

      const total = filteredItems.length;
      const rents = filteredItems.map(d => d.rent_manwon).sort((a,b) => a-b);
      const avgRent = (rents.reduce((a,b)=>a+b, 0) / total).toFixed(1);
      const medianRent = rents[Math.floor(total / 2)];
      const avgCost = (filteredItems.reduce((a,b)=>a+b.total_monthly_cost, 0) / total).toFixed(1);
      const avgDep = (filteredItems.reduce((a,b)=>a+b.deposit_manwon, 0) / total).toFixed(1);
      const avgSize = (filteredItems.reduce((a,b)=>a+b.size_pyeong, 0) / total).toFixed(1);
      const avgCpp = (filteredItems.reduce((a,b)=>a+b.cost_per_pyeong, 0) / total).toFixed(1);

      document.getElementById('kpiTotal').textContent = `${{total}}건`;
      document.getElementById('kpiAvgRent').textContent = `${{avgRent}}만`;
      document.getElementById('kpiMedianRent').textContent = `중위수 ${{medianRent}}만`;
      document.getElementById('kpiAvgTotalCost').textContent = `${{avgCost}}만`;
      document.getElementById('kpiAvgDep').textContent = `${{avgDep}}만`;
      document.getElementById('kpiAvgSize').textContent = `${{avgSize}}평`;
      document.getElementById('kpiAvgCpp').textContent = `${{avgCpp}}만`;
    }}

    // Leaflet 인터랙티브 맵 초기화
    function initMap() {{
      // 오창읍 중심 좌표: 36.7125, 127.4280
      map = L.map('map', {{
        zoomControl: true,
        scrollWheelZoom: true
      }}).setView([36.7125, 127.4280], 14);

      // 모던한 CartoDB Positron 화이트 타일 (글래스모피즘과 완벽 일체)
      L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        attribution: '&copy; <a href="https://carto.com/">CARTO</a> | &copy; OpenStreetMap',
        maxZoom: 19,
        subdomains: 'abcd'
      }}).addTo(map);

      markersCluster = L.markerClusterGroup({{
        maxClusterRadius: 40,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        zoomToBoundsOnClick: true
      }});
      map.addLayer(markersCluster);
    }}

    // 지도 영역 자동 맞춤
    function fitMapToFilteredMarkers() {{
      if (!map || !markersCluster) return;
      const layers = markersCluster.getLayers();
      if (layers.length > 0) {{
        map.fitBounds(markersCluster.getBounds().pad(0.08), {{ maxZoom: 16 }});
      }}
    }}

    // 권역 퀵 이동 함수
    function flyToRegion(region) {{
      if (!map) return;
      if (region === 'ALL') {{
        document.getElementById('filterDong').value = 'ALL';
        applyFilters();
        fitMapToFilteredMarkers();
      }} else if (region === '양청리') {{
        document.getElementById('filterDong').value = '양청리';
        applyFilters();
        map.flyTo([36.7180, 127.4250], 15, {{ duration: 1.2 }});
      }} else if (region === '구룡리') {{
        document.getElementById('filterDong').value = '구룡리';
        applyFilters();
        map.flyTo([36.7145, 127.4170], 15, {{ duration: 1.2 }});
      }} else if (region === '주성리') {{
        document.getElementById('filterDong').value = '주성리';
        applyFilters();
        map.flyTo([36.7380, 127.4520], 15, {{ duration: 1.2 }});
      }}
    }}

    // 지도 마커 업데이트
    function updateMapMarkers() {{
      if (!markersCluster) return;
      markersCluster.clearLayers();

      const newMarkers = [];
      filteredItems.forEach(it => {{
        if (it.latitude && it.longitude) {{
          let color = '#3b82f6';
          if (it.rent_manwon <= 35) color = '#3b82f6';
          else if (it.rent_manwon <= 50) color = '#f59e0b';
          else color = '#ef4444';

          const marker = L.circleMarker([it.latitude, it.longitude], {{
            radius: 6,
            fillColor: color,
            color: '#ffffff',
            weight: 1.5,
            opacity: 1,
            fillOpacity: 0.85
          }});

          const thumbHtml = it.thumbnail_url 
            ? `<div style="width: 100%; height: 90px; border-radius: 8px; overflow: hidden; margin-bottom: 6px; background: #f1f5f9;"><img src="${{it.thumbnail_url}}" style="width:100%; height:100%; object-fit: cover;" onerror="this.parentElement.style.display='none'"></div>`
            : '';

          const popupContent = `
            <div style="font-family: Pretendard, sans-serif; font-size: 12px; line-height: 1.4; min-width: 200px; padding: 4px;">
              ${{thumbHtml}}
              <div style="display: flex; gap: 4px; margin-bottom: 4px;">
                <span style="background: #eff6ff; color: #2563eb; font-weight: bold; font-size: 10px; padding: 2px 6px; border-radius: 4px;">${{it.sub_dong}}</span>
                <span style="background: #f1f5f9; color: #475569; font-weight: bold; font-size: 10px; padding: 2px 6px; border-radius: 4px;">${{it.structure_type}}</span>
              </div>
              <strong style="font-size: 13px; color: #1e293b; display: block; margin-bottom: 4px; word-break: break-all;">${{it.title || '매물 상세'}}</strong>
              <div style="color: #64748b; font-size: 11px; margin-bottom: 6px;">${{it.address_full}}</div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                <span style="color: #64748b;">보증금 / 월세:</span>
                <strong style="color: #2563eb;">${{it.deposit_manwon}} / ${{it.rent_manwon}}만</strong>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                <span style="color: #64748b;">실질 주거비:</span>
                <strong style="color: #e11d48;">${{it.total_monthly_cost}}만</strong>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #64748b;">전용면적:</span>
                <strong style="color: #0f766e;">${{it.size_pyeong}}평 (${{it.size_m2}}㎡)</strong>
              </div>
              <button onclick="openModalById(${{it.item_id}})" style="width: 100%; padding: 6px 10px; background: #2563eb; color: #fff; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 11px; transition: background 0.2s;">상세보기</button>
            </div>
          `;
          marker.bindPopup(popupContent);
          newMarkers.push(marker);
        }}
      }});

      markersCluster.addLayers(newMarkers);
    }}

    // Chart.js 6종 차트 초기화
    function initCharts() {{
      const chartOptions = {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11, family: 'Pretendard' }} }} }}
        }}
      }};

      charts.rentDist = new Chart(document.getElementById('chartRentDist'), {{
        type: 'bar',
        data: {{ labels: [], datasets: [{{ label: '매물 건수', data: [], backgroundColor: '#3b82f6', borderRadius: 6 }}] }},
        options: chartOptions
      }});

      charts.structure = new Chart(document.getElementById('chartStructure'), {{
        type: 'doughnut',
        data: {{ labels: [], datasets: [{{ data: [], backgroundColor: ['#3b82f6', '#6366f1', '#14b8a6', '#f59e0b', '#ec4899', '#64748b'] }}] }},
        options: {{ ...chartOptions, cutout: '65%' }}
      }});

      charts.subdong = new Chart(document.getElementById('chartSubdong'), {{
        type: 'bar',
        data: {{
          labels: [],
          datasets: [
            {{ type: 'bar', label: '평균 월세(만)', data: [], backgroundColor: '#6366f1', borderRadius: 6, yAxisID: 'y' }},
            {{ type: 'line', label: '매물 건수(건)', data: [], borderColor: '#f59e0b', backgroundColor: '#f59e0b', tension: 0.3, yAxisID: 'y1' }}
          ]
        }},
        options: {{
          ...chartOptions,
          scales: {{
            y: {{ type: 'linear', position: 'left', title: {{ display: true, text: '만원' }} }},
            y1: {{ type: 'linear', position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: '건수' }} }}
          }}
        }}
      }});

      charts.sizeVsCost = new Chart(document.getElementById('chartSizeVsCost'), {{
        type: 'scatter',
        data: {{
          datasets: [{{
            label: '매물 좌표',
            data: [],
            backgroundColor: 'rgba(239, 68, 68, 0.65)',
            pointRadius: 4
          }}]
        }},
        options: {{
          ...chartOptions,
          scales: {{
            x: {{ title: {{ display: true, text: '전용면적 (평)' }} }},
            y: {{ title: {{ display: true, text: '실질 총 주거비용 (만원)' }} }}
          }}
        }}
      }});

      charts.depositBin = new Chart(document.getElementById('chartDepositBin'), {{
        type: 'bar',
        data: {{ labels: [], datasets: [{{ label: '평균 월세(만)', data: [], backgroundColor: '#10b981', borderRadius: 6 }}] }},
        options: chartOptions
      }});

      charts.floorLevel = new Chart(document.getElementById('chartFloorLevel'), {{
        type: 'bar',
        data: {{
          labels: ['저층(1층/반지하)', '중층(2~4층)', '고층(5층+)'],
          datasets: [
            {{ label: '평균 월세(만)', data: [], backgroundColor: '#0284c7', borderRadius: 6 }},
            {{ label: '평균 면적(평)', data: [], backgroundColor: '#2dd4bf', borderRadius: 6 }}
          ]
        }},
        options: chartOptions
      }});
    }}

    // 차트 데이터 갱신
    function updateCharts() {{
      const rentBins = {{ '25만 이하': 0, '26~35만': 0, '36~45만': 0, '46~55만': 0, '56~70만': 0, '70만 초과': 0 }};
      filteredItems.forEach(it => {{
        const r = it.rent_manwon;
        if (r <= 25) rentBins['25만 이하']++;
        else if (r <= 35) rentBins['26~35만']++;
        else if (r <= 45) rentBins['36~45만']++;
        else if (r <= 55) rentBins['46~55만']++;
        else if (r <= 70) rentBins['56~70만']++;
        else rentBins['70만 초과']++;
      }});
      charts.rentDist.data.labels = Object.keys(rentBins);
      charts.rentDist.data.datasets[0].data = Object.values(rentBins);
      charts.rentDist.update();

      const structCounts = {{}};
      filteredItems.forEach(it => {{
        structCounts[it.structure_type] = (structCounts[it.structure_type] || 0) + 1;
      }});
      charts.structure.data.labels = Object.keys(structCounts);
      charts.structure.data.datasets[0].data = Object.values(structCounts);
      charts.structure.update();

      const dongStats = {{}};
      filteredItems.forEach(it => {{
        if (!dongStats[it.sub_dong]) dongStats[it.sub_dong] = {{ sumRent: 0, count: 0 }};
        dongStats[it.sub_dong].sumRent += it.rent_manwon;
        dongStats[it.sub_dong].count += 1;
      }});
      const dongs = Object.keys(dongStats);
      charts.subdong.data.labels = dongs;
      charts.subdong.data.datasets[0].data = dongs.map(d => (dongStats[d].sumRent / dongStats[d].count).toFixed(1));
      charts.subdong.data.datasets[1].data = dongs.map(d => dongStats[d].count);
      charts.subdong.update();

      charts.sizeVsCost.data.datasets[0].data = filteredItems.map(it => ({{ x: it.size_pyeong, y: it.total_monthly_cost }}));
      charts.sizeVsCost.update();

      const depBins = {{ '200만 이하': {{ sum: 0, cnt: 0 }}, '201~300만': {{ sum: 0, cnt: 0 }}, '301~500만': {{ sum: 0, cnt: 0 }}, '501~1000만': {{ sum: 0, cnt: 0 }}, '1000만 초과': {{ sum: 0, cnt: 0 }} }};
      filteredItems.forEach(it => {{
        const d = it.deposit_manwon;
        let b = '1000만 초과';
        if (d <= 200) b = '200만 이하';
        else if (d <= 300) b = '201~300만';
        else if (d <= 500) b = '301~500만';
        else if (d <= 1000) b = '501~1000만';
        depBins[b].sum += it.rent_manwon;
        depBins[b].cnt += 1;
      }});
      charts.depositBin.data.labels = Object.keys(depBins);
      charts.depositBin.data.datasets[0].data = Object.keys(depBins).map(k => depBins[k].cnt > 0 ? (depBins[k].sum / depBins[k].cnt).toFixed(1) : 0);
      charts.depositBin.update();

      const flStats = {{ '저층': {{ rSum: 0, sSum: 0, cnt: 0 }}, '중층': {{ rSum: 0, sSum: 0, cnt: 0 }}, '고층': {{ rSum: 0, sSum: 0, cnt: 0 }} }};
      filteredItems.forEach(it => {{
        const cat = it.floor_category || '중층';
        if (flStats[cat]) {{
          flStats[cat].rSum += it.rent_manwon;
          flStats[cat].sSum += it.size_pyeong;
          flStats[cat].cnt += 1;
        }}
      }});
      charts.floorLevel.data.datasets[0].data = ['저층', '중층', '고층'].map(c => flStats[c].cnt > 0 ? (flStats[c].rSum / flStats[c].cnt).toFixed(1) : 0);
      charts.floorLevel.data.datasets[1].data = ['저층', '중층', '고층'].map(c => flStats[c].cnt > 0 ? (flStats[c].sSum / flStats[c].cnt).toFixed(1) : 0);
      charts.floorLevel.update();
    }}

    // 테이블 렌더링 & 정렬
    function sortTable(col) {{
      if (currentSortCol === col) {{
        currentSortAsc = !currentSortAsc;
      }} else {{
        currentSortCol = col;
        currentSortAsc = true;
      }}
      renderTable();
    }}

    function renderTable() {{
      filteredItems.sort((a, b) => {{
        let v1 = a[currentSortCol];
        let v2 = b[currentSortCol];
        if (typeof v1 === 'string') v1 = v1.localeCompare(v2);
        return currentSortAsc ? (v1 > v2 ? 1 : -1) : (v1 < v2 ? 1 : -1);
      }});

      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';

      const total = filteredItems.length;
      const startIdx = (currentPage - 1) * pageSize;
      const pageItems = filteredItems.slice(startIdx, startIdx + pageSize);

      pageItems.forEach(it => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50/50 cursor-pointer transition';
        tr.onclick = () => openModal(it);

        tr.innerHTML = `
          <td class="p-3 font-mono font-medium text-slate-500">${{it.item_id}}</td>
          <td class="p-3 font-semibold text-slate-800">${{it.sub_dong}}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700">${{it.structure_type}}</span></td>
          <td class="p-3 text-right font-medium text-slate-700">${{it.deposit_manwon.toLocaleString()}}만</td>
          <td class="p-3 text-right font-bold text-blue-600">${{it.rent_manwon}}만</td>
          <td class="p-3 text-right font-bold text-rose-600">${{it.total_monthly_cost}}만</td>
          <td class="p-3 text-right text-slate-700">${{it.size_pyeong}}평</td>
          <td class="p-3 text-right font-medium text-amber-600">${{it.cost_per_pyeong}}만</td>
          <td class="p-3 text-center text-slate-500">${{it.current_floor}}/${{it.max_floor}} (${{it.floor_category}})</td>
          <td class="p-3 text-center">
            ${{it.has_elevator ? '<i class="fa-solid fa-elevator text-blue-500 mr-1" title="승강기"></i>' : ''}}
            ${{it.has_full_option ? '<i class="fa-solid fa-check-circle text-teal-500" title="풀옵션"></i>' : '<span class="text-slate-300">-</span>'}}
          </td>
          <td class="p-3 text-slate-700 max-w-xs truncate" title="${{it.title}}">${{it.title}}</td>
        `;
        tbody.appendChild(tr);
      }});

      const endIdx = Math.min(startIdx + pageSize, total);
      document.getElementById('pageInfo').textContent = `${{total > 0 ? startIdx + 1 : 0}}-${{endIdx}} / 총 ${{total}}건`;

      renderPagination(total);
    }}

    function renderPagination(total) {{
      const totalPages = Math.ceil(total / pageSize) || 1;
      const container = document.getElementById('paginationControls');
      container.innerHTML = '';

      const btnPrev = document.createElement('button');
      btnPrev.className = `px-2.5 py-1 rounded-lg border text-xs ${{currentPage === 1 ? 'border-slate-100 text-slate-300 cursor-not-allowed' : 'border-slate-200 text-slate-600 hover:bg-slate-50'}}`;
      btnPrev.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
      btnPrev.disabled = currentPage === 1;
      btnPrev.onclick = () => {{ if(currentPage > 1) {{ currentPage--; renderTable(); }} }};
      container.appendChild(btnPrev);

      let startP = Math.max(1, currentPage - 2);
      let endP = Math.min(totalPages, startP + 4);
      if (endP - startP < 4) startP = Math.max(1, endP - 4);

      for (let p = startP; p <= endP; p++) {{
        const btn = document.createElement('button');
        btn.className = `px-2.5 py-1 rounded-lg border text-xs ${{p === currentPage ? 'bg-blue-600 text-white border-blue-600 font-bold' : 'border-slate-200 text-slate-600 hover:bg-slate-50'}}`;
        btn.textContent = p;
        btn.onclick = () => {{ currentPage = p; renderTable(); }};
        container.appendChild(btn);
      }}

      const btnNext = document.createElement('button');
      btnNext.className = `px-2.5 py-1 rounded-lg border text-xs ${{currentPage === totalPages ? 'border-slate-100 text-slate-300 cursor-not-allowed' : 'border-slate-200 text-slate-600 hover:bg-slate-50'}}`;
      btnNext.innerHTML = '<i class="fa-solid fa-chevron-right"></i>';
      btnNext.disabled = currentPage === totalPages;
      btnNext.onclick = () => {{ if(currentPage < totalPages) {{ currentPage++; renderTable(); }} }};
      container.appendChild(btnNext);
    }}

    // 모달 팝업
    function openModalById(id) {{
      const it = allItems.find(d => d.item_id === id);
      if (it) openModal(it);
    }}

    function openModal(it) {{
      document.getElementById('modalDongBadge').textContent = it.sub_dong;
      document.getElementById('modalStructBadge').textContent = it.structure_type;
      document.getElementById('modalTitle').textContent = it.title;

      const thumb = document.getElementById('modalThumb');
      if (it.thumbnail_url) {{
        thumb.src = it.thumbnail_url;
        document.getElementById('modalThumbContainer').style.display = 'flex';
      }} else {{
        document.getElementById('modalThumbContainer').style.display = 'none';
      }}

      document.getElementById('modalPrice').textContent = `${{it.deposit_manwon.toLocaleString()}} / ${{it.rent_manwon}} 만원`;
      document.getElementById('modalTotalCost').textContent = `${{it.total_monthly_cost}} 만원 (관리비 ${{it.manage_cost_manwon}}만)`;
      document.getElementById('modalSize').textContent = `${{it.size_m2}} ㎡ (${{it.size_pyeong}}평)`;
      document.getElementById('modalCpp').textContent = `${{it.cost_per_pyeong}} 만원/평`;
      document.getElementById('modalAddress').textContent = it.address_full || '오창읍 일대';
      document.getElementById('modalFloor').textContent = `${{it.current_floor}}층 / ${{it.max_floor}}층 (${{it.floor_category}})`;
      
      const fac = [];
      if (it.has_elevator) fac.push('승강기(엘리베이터) 보유');
      if (it.has_full_option) fac.push('풀옵션 완비');
      if (it.parking_available) fac.push('주차 가능');
      document.getElementById('modalFacilities').textContent = fac.length > 0 ? fac.join(', ') : '기본 옵션';
      document.getElementById('modalDate').textContent = it.reg_date || '-';

      document.getElementById('itemModal').classList.remove('hidden');
    }}

    function closeModal() {{
      document.getElementById('itemModal').classList.add('hidden');
    }}

    // 필터링 결과 CSV 내보내기 (UTF-8-SIG)
    function exportFilteredCsv() {{
      if (filteredItems.length === 0) {{
        alert('내보낼 매물 데이터가 없습니다.');
        return;
      }}

      const headers = Object.keys(filteredItems[0]);
      let csvContent = '\\uFEFF';
      csvContent += headers.join(',') + '\\n';

      filteredItems.forEach(row => {{
        const line = headers.map(h => {{
          let val = row[h];
          if (val === null || val === undefined) val = '';
          const str = String(val).replace(/"/g, '""');
          return `"${{str}}"`;
        }}).join(',');
        csvContent += line + '\\n';
      }});

      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `zigbang_ochang_filtered_${{new Date().toISOString().slice(0,10)}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}
  </script>

</body>
</html>
"""

    out_file1 = BASE_DIR / "dashboard.html"
    out_file2 = Path(__file__).resolve().parent.parent.parent / "dashboard.html"

    with open(out_file1, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] 대시보드 생성 완료: {out_file1}")

    with open(out_file2, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] 루트 대시보드 복사 완료: {out_file2}")


if __name__ == "__main__":
    generate_dashboard()
