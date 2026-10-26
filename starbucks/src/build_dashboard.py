"""
스타벅스 전국 매장 글래스모피즘 인터랙티브 웹 대시보드 빌더
- Single File HTML (CORS 없이 file:// 로컬 즉시 실행)
- 전수 2,213개 매장 데이터 JSON 인라인 임베딩
- 오로라 앰비언트 글로우 & 반투명 블러 글래스모피즘 UI
- Chart.js v4 기반 6대 인터랙티브 반응형 차트
- 실시간 다중 필터, 검색, 정렬, 페이지네이션, 모달 팝업, CSV 다운로드
"""

import datetime
import json
import os
import pandas as pd


def generate_dashboard():
    csv_path = "starbucks/data/starbucks_national_latest.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} 데이터 파일이 없습니다.")

    df = pd.read_csv(csv_path)
    total_stores = len(df)
    seoul_cnt = int((df["sido_name"] == "서울").sum())
    dt_cnt = int(df["is_drive_thru"].sum())
    reserve_cnt = int(df["is_reserve"].sum())
    delivers_cnt = int(df["is_delivers"].sum())
    new_cnt = int(df["is_new"].sum())

    # JSON 직렬화용 레코드 생성
    stores_data = []
    for _, row in df.iterrows():
        stores_data.append({
            "code": str(row["store_code"]),
            "name": str(row["store_name"]),
            "type": str(row["store_type"]),
            "sido": str(row["sido_name"]),
            "gugun": str(row["gugun_name"]),
            "addr": str(row["doro_address"]),
            "jibun": str(row["jibun_address"]),
            "lat": float(row["latitude"]) if pd.notnull(row["latitude"]) else 0.0,
            "lon": float(row["longitude"]) if pd.notnull(row["longitude"]) else 0.0,
            "tel": str(row["tel"]) if pd.notnull(row["tel"]) else "",
            "open": str(row["open_date"]) if pd.notnull(row["open_date"]) else "",
            "year": str(row["open_year"]) if pd.notnull(row["open_year"]) else "",
            "years": float(row["business_years"]) if pd.notnull(row["business_years"]) else 0.0,
            "is_dt": bool(row["is_drive_thru"]),
            "is_res": bool(row["is_reserve"]),
            "is_del": bool(row["is_delivers"]),
            "is_new": bool(row["is_new"]),
            "img": str(row["default_image"]) if pd.notnull(row["default_image"]) else "",
        })

    stores_json = json.dumps(stores_data, ensure_ascii=False)

    # HTML 템플릿 작성
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>스타벅스 전국 매장 인터랙티브 인텔리전스 대시보드</title>
  <!-- Chart.js v4 -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <!-- Lucide Icons -->
  <script src="https://cdn.jsdelivr.net/npm/lucide@0.344.0/dist/umd/lucide.min.js"></script>
  <style>
    :root {{
      --bg-gradient: radial-gradient(circle at 15% 20%, #0d2b1d 0%, #06150e 45%, #020705 100%);
      --card-bg: rgba(18, 38, 28, 0.55);
      --card-border: rgba(255, 255, 255, 0.12);
      --card-hover: rgba(24, 52, 38, 0.7);
      --text-main: #f0fdf4;
      --text-muted: #86efac;
      --accent-green: #008744;
      --accent-gold: #cba258;
      --accent-dt: #f87171;
      --accent-blue: #38bdf8;
      --glow-1: rgba(0, 135, 68, 0.28);
      --glow-2: rgba(203, 162, 88, 0.18);
    }}

    [data-theme="light"] {{
      --bg-gradient: radial-gradient(circle at 15% 20%, #e8f5e9 0%, #f1f8f5 45%, #ffffff 100%);
      --card-bg: rgba(255, 255, 255, 0.75);
      --card-border: rgba(0, 112, 74, 0.18);
      --card-hover: rgba(255, 255, 255, 0.95);
      --text-main: #143823;
      --text-muted: #2d6a4f;
      --accent-green: #00704a;
      --accent-gold: #9d7827;
      --accent-dt: #dc2626;
      --accent-blue: #0284c7;
      --glow-1: rgba(0, 112, 74, 0.12);
      --glow-2: rgba(203, 162, 88, 0.15);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Segoe UI", Roboto, sans-serif;
    }}

    body {{
      background: var(--bg-gradient);
      color: var(--text-main);
      min-height: 100vh;
      overflow-x: hidden;
      padding: 24px;
      transition: background 0.3s ease, color 0.3s ease;
      position: relative;
    }}

    /* Ambient Background Glows */
    .ambient-glow {{
      position: fixed;
      border-radius: 50%;
      filter: blur(120px);
      z-index: -1;
      pointer-events: none;
      animation: float 14s infinite alternate ease-in-out;
    }}
    .glow-top-left {{
      width: 480px;
      height: 480px;
      background: var(--glow-1);
      top: -100px;
      left: -100px;
    }}
    .glow-bottom-right {{
      width: 520px;
      height: 520px;
      background: var(--glow-2);
      bottom: -150px;
      right: -100px;
      animation-duration: 18s;
    }}

    @keyframes float {{
      0% {{ transform: translate(0, 0) scale(1); }}
      100% {{ transform: translate(50px, 40px) scale(1.1); }}
    }}

    .container {{
      max-width: 1480px;
      margin: 0 auto;
    }}

    /* Glassmorphism Panel */
    .glass-panel {{
      background: var(--card-bg);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.25);
      padding: 24px;
      transition: all 0.25s ease;
    }}

    .glass-panel:hover {{
      border-color: rgba(255, 255, 255, 0.24);
    }}

    /* Header */
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .logo-badge {{
      width: 56px;
      height: 56px;
      background: linear-gradient(135deg, #00704a, #004d34);
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 6px 16px rgba(0, 112, 74, 0.4);
      color: white;
    }}

    h1 {{
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
    }}

    .sub-title {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn {{
      background: var(--card-bg);
      color: var(--text-main);
      border: 1px solid var(--card-border);
      padding: 10px 18px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }}

    .btn:hover {{
      background: var(--card-hover);
      border-color: var(--accent-green);
      transform: translateY(-1px);
    }}

    .btn-primary {{
      background: linear-gradient(135deg, #00704a, #008744);
      color: white;
      border: none;
    }}
    .btn-primary:hover {{
      background: linear-gradient(135deg, #008744, #00a854);
    }}

    /* KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      padding: 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      position: relative;
      overflow: hidden;
    }}

    .kpi-card::after {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--accent-green);
    }}

    .kpi-card.kpi-gold::after {{ background: var(--accent-gold); }}
    .kpi-card.kpi-dt::after {{ background: var(--accent-dt); }}
    .kpi-card.kpi-blue::after {{ background: var(--accent-blue); }}

    .kpi-icon {{
      width: 48px;
      height: 48px;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}

    .kpi-val {{
      font-size: 26px;
      font-weight: 800;
      line-height: 1.1;
    }}

    .kpi-label {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 3px;
    }}

    /* Charts Grid */
    .charts-grid {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 20px;
      margin-bottom: 24px;
    }}

    .col-4 {{ grid-column: span 4; }}
    .col-6 {{ grid-column: span 6; }}
    .col-8 {{ grid-column: span 8; }}
    .col-12 {{ grid-column: span 12; }}

    @media (max-width: 1024px) {{
      .col-4, .col-6, .col-8 {{ grid-column: span 12; }}
    }}

    .chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}

    .chart-title {{
      font-size: 16px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .chart-box {{
      position: relative;
      height: 300px;
      width: 100%;
    }}

    /* Filters Bar */
    .filters-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      margin-bottom: 16px;
    }}

    .search-box {{
      position: relative;
      flex: 1;
      min-width: 260px;
    }}

    .search-input {{
      width: 100%;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px 16px 10px 40px;
      color: var(--text-main);
      font-size: 14px;
      outline: none;
      transition: all 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--accent-green);
      background: rgba(0, 0, 0, 0.35);
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }}

    .select-filter {{
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px 14px;
      color: var(--text-main);
      font-size: 13px;
      outline: none;
      cursor: pointer;
    }}
    .select-filter option {{
      background: #0f241a;
      color: #fff;
    }}

    .badge-filter {{
      padding: 8px 14px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--card-border);
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-main);
      transition: all 0.2s;
    }}
    .badge-filter.active {{
      background: var(--accent-green);
      color: white;
      border-color: var(--accent-green);
    }}

    /* Data Table */
    .table-container {{
      overflow-x: auto;
      border-radius: 14px;
      margin-top: 12px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    th {{
      background: rgba(0, 0, 0, 0.3);
      padding: 12px 16px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
      user-select: none;
      transition: background 0.2s;
    }}
    th:hover {{
      background: rgba(0, 0, 0, 0.45);
      color: var(--text-main);
    }}

    td {{
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      white-space: nowrap;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.04);
      cursor: pointer;
    }}

    .tag {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }}
    .tag-dt {{ background: rgba(248, 113, 113, 0.2); color: #fca5a5; border: 1px solid rgba(248, 113, 113, 0.4); }}
    .tag-res {{ background: rgba(203, 162, 88, 0.2); color: #fde047; border: 1px solid rgba(203, 162, 88, 0.4); }}
    .tag-del {{ background: rgba(56, 189, 248, 0.2); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.4); }}
    .tag-gen {{ background: rgba(255, 255, 255, 0.1); color: #cbd5e1; }}
    .tag-new {{ background: rgba(34, 197, 94, 0.2); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); }}

    /* Pagination */
    .pagination {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 16px;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 13px;
    }}

    .page-controls {{
      display: flex;
      gap: 6px;
    }}

    .page-btn {{
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid var(--card-border);
      background: var(--card-bg);
      color: var(--text-main);
      cursor: pointer;
      font-size: 12px;
    }}
    .page-btn.active {{
      background: var(--accent-green);
      color: white;
      border-color: var(--accent-green);
    }}
    .page-btn:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}

    /* Modal */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }}
    .modal-overlay.active {{ display: flex; }}

    .modal-card {{
      background: var(--card-bg);
      backdrop-filter: blur(25px);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      max-width: 580px;
      width: 100%;
      overflow: hidden;
      animation: popIn 0.25s ease-out;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    @keyframes popIn {{
      0% {{ transform: scale(0.92); opacity: 0; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}

    .modal-hero {{
      height: 200px;
      background-size: cover;
      background-position: center;
      position: relative;
      background-color: #0d2b1d;
    }}

    .modal-close {{
      position: absolute;
      top: 16px;
      right: 16px;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.6);
      color: white;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .modal-body {{
      padding: 24px;
    }}

    .modal-title {{
      font-size: 22px;
      font-weight: 800;
      margin-bottom: 8px;
    }}

    .modal-tags {{
      display: flex;
      gap: 6px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}

    .modal-info-row {{
      display: flex;
      margin-bottom: 12px;
      font-size: 13.5px;
      line-height: 1.5;
    }}
    .modal-info-label {{
      width: 90px;
      color: var(--text-muted);
      font-weight: 600;
      flex-shrink: 0;
    }}
  </style>
</head>
<body>

  <div class="ambient-glow glow-top-left"></div>
  <div class="ambient-glow glow-bottom-right"></div>

  <div class="container">
    <!-- Header -->
    <header class="glass-panel">
      <div class="header-left">
        <div class="logo-badge">
          <i data-lucide="coffee" style="width: 28px; height: 28px;"></i>
        </div>
        <div>
          <h1>스타벅스 전국 매장 인텔리전스 대시보드</h1>
          <div class="sub-title">공식 Gateway REST API 역공학 전수 수집 및 심층 분석 시스템 | {datetime.date.today().strftime('%Y-%m-%d')} 기준</div>
        </div>
      </div>
      <div class="header-actions">
        <button class="btn" id="themeToggleBtn" onclick="toggleTheme()">
          <i data-lucide="sun-moon" style="width: 16px; height: 16px;"></i> 테마 전환
        </button>
        <button class="btn btn-primary" onclick="exportFilteredCSV()">
          <i data-lucide="download" style="width: 16px; height: 16px;"></i> CSV 내보내기
        </button>
      </div>
    </header>

    <!-- KPI Summary Cards -->
    <div class="kpi-grid">
      <div class="glass-panel kpi-card">
        <div class="kpi-icon"><i data-lucide="map-pin" style="color: var(--accent-green); width: 24px; height: 24px;"></i></div>
        <div>
          <div class="kpi-val" id="kpiTotal">{total_stores:,}</div>
          <div class="kpi-label">전국 총 매장 수</div>
        </div>
      </div>

      <div class="glass-panel kpi-card">
        <div class="kpi-icon"><i data-lucide="building-2" style="color: var(--accent-blue); width: 24px; height: 24px;"></i></div>
        <div>
          <div class="kpi-val" id="kpiSeoul">{seoul_cnt:,}</div>
          <div class="kpi-label">서울 매장 수 ({round(seoul_cnt/total_stores*100, 1)}%)</div>
        </div>
      </div>

      <div class="glass-panel kpi-card kpi-dt">
        <div class="kpi-icon"><i data-lucide="car" style="color: var(--accent-dt); width: 24px; height: 24px;"></i></div>
        <div>
          <div class="kpi-val" id="kpiDT">{dt_cnt:,}</div>
          <div class="kpi-label">드라이브스루 (DT) ({round(dt_cnt/total_stores*100, 1)}%)</div>
        </div>
      </div>

      <div class="glass-panel kpi-card kpi-gold">
        <div class="kpi-icon"><i data-lucide="sparkles" style="color: var(--accent-gold); width: 24px; height: 24px;"></i></div>
        <div>
          <div class="kpi-val" id="kpiReserve">{reserve_cnt:,}</div>
          <div class="kpi-label">스타벅스 리저브 ({round(reserve_cnt/total_stores*100, 1)}%)</div>
        </div>
      </div>

      <div class="glass-panel kpi-card kpi-blue">
        <div class="kpi-icon"><i data-lucide="truck" style="color: #38bdf8; width: 24px; height: 24px;"></i></div>
        <div>
          <div class="kpi-val" id="kpiDelivers">{delivers_cnt:,}</div>
          <div class="kpi-label">딜리버스 매장 ({round(delivers_cnt/total_stores*100, 1)}%)</div>
        </div>
      </div>
    </div>

    <!-- 6대 핵심 차트 그리드 -->
    <div class="charts-grid">
      <!-- Chart 1: 시도별 매장 수 -->
      <div class="glass-panel col-6">
        <div class="chart-header">
          <div class="chart-title"><i data-lucide="bar-chart-2" style="width: 18px; height: 18px; color: var(--accent-green);"></i> 시도별 매장 수 랭킹</div>
        </div>
        <div class="chart-box">
          <canvas id="chartSido"></canvas>
        </div>
      </div>

      <!-- Chart 2: 매장 유형별 점유율 -->
      <div class="glass-panel col-6">
        <div class="chart-header">
          <div class="chart-title"><i data-lucide="pie-chart" style="width: 18px; height: 18px; color: var(--accent-gold);"></i> 매장 유형별 구성비</div>
        </div>
        <div class="chart-box">
          <canvas id="chartType"></canvas>
        </div>
      </div>

      <!-- Chart 3: 연도별 신규 출점 추이 -->
      <div class="glass-panel col-8">
        <div class="chart-header">
          <div class="chart-title"><i data-lucide="trending-up" style="width: 18px; height: 18px; color: #38bdf8;"></i> 연도별 신규 개점 추이 (1999~현재)</div>
        </div>
        <div class="chart-box">
          <canvas id="chartTrend"></canvas>
        </div>
      </div>

      <!-- Chart 4: 시도별 DT 비율 -->
      <div class="glass-panel col-4">
        <div class="chart-header">
          <div class="chart-title"><i data-lucide="car" style="width: 18px; height: 18px; color: var(--accent-dt);"></i> 시도별 DT 비중 (%)</div>
        </div>
        <div class="chart-box">
          <canvas id="chartDTRatio"></canvas>
        </div>
      </div>

      <!-- Chart 5: 서울 구별 TOP 10 -->
      <div class="glass-panel col-6">
        <div class="chart-header">
          <div class="chart-title"><i data-lucide="landmark" style="width: 18px; height: 18px; color: #a78bfa;"></i> 서울 자치구별 매장 수 TOP 10</div>
        </div>
        <div class="chart-box">
          <canvas id="chartSeoulGu"></canvas>
        </div>
      </div>

      <!-- Chart 6: 업력 구간별 매장 수 -->
      <div class="glass-panel col-6">
        <div class="chart-header">
          <div class="chart-title"><i data-lucide="clock" style="width: 18px; height: 18px; color: #f59e0b;"></i> 매장 운영 연수(업력) 구간 분포</div>
        </div>
        <div class="chart-box">
          <canvas id="chartYears"></canvas>
        </div>
      </div>
    </div>

    <!-- 실시간 데이터 탐색기 -->
    <div class="glass-panel">
      <div class="chart-header">
        <div class="chart-title"><i data-lucide="search" style="width: 18px; height: 18px; color: var(--accent-green);"></i> 실시간 전국 매장 탐색기</div>
        <div style="font-size: 13px; color: var(--text-muted);" id="filteredCountText">전체 {total_stores:,}개 매장 중 {total_stores:,}개 표시</div>
      </div>

      <div class="filters-bar">
        <div class="search-box">
          <i data-lucide="search" class="search-icon" style="width: 16px; height: 16px;"></i>
          <input type="text" id="searchInput" class="search-input" placeholder="매장명, 도로명, 지번 주소 검색 (예: 강남, 제주, 테헤란로)" oninput="handleSearch()">
        </div>

        <select id="sidoSelect" class="select-filter" onchange="handleFilterChange()">
          <option value="ALL">전국 시/도 전체</option>
        </select>

        <div class="badge-filter active" data-filter="ALL" onclick="setSpecialFilter('ALL')">전체</div>
        <div class="badge-filter" data-filter="DT" onclick="setSpecialFilter('DT')">🚗 드라이브스루(DT)</div>
        <div class="badge-filter" data-filter="RES" onclick="setSpecialFilter('RES')">⭐ 리저브</div>
        <div class="badge-filter" data-filter="DEL" onclick="setSpecialFilter('DEL')">🛵 딜리버스</div>
        <div class="badge-filter" data-filter="NEW" onclick="setSpecialFilter('NEW')">✨ 신규 매장</div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th onclick="sortTable('name')">매장명 ⇕</th>
              <th onclick="sortTable('type')">매장 유형 ⇕</th>
              <th onclick="sortTable('sido')">시/도 ⇕</th>
              <th onclick="sortTable('gugun')">구/군 ⇕</th>
              <th onclick="sortTable('addr')">도로명 주소 ⇕</th>
              <th onclick="sortTable('tel')">전화번호</th>
              <th onclick="sortTable('open')">개점일 ⇕</th>
              <th onclick="sortTable('years')">업력(년) ⇕</th>
            </tr>
          </thead>
          <tbody id="storeTableBody"></tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <div style="color: var(--text-muted);">
          페이지당 행 수: 
          <select id="pageSizeSelect" class="select-filter" style="padding: 4px 8px;" onchange="handlePageSizeChange()">
            <option value="15">15개</option>
            <option value="30" selected>30개</option>
            <option value="50">50개</option>
            <option value="100">100개</option>
          </select>
        </div>
        <div class="page-controls" id="pageControls"></div>
      </div>
    </div>
  </div>

  <!-- Detail Modal -->
  <div class="modal-overlay" id="detailModal" onclick="closeModalOnOverlay(event)">
    <div class="modal-card">
      <div class="modal-hero" id="modalHero">
        <button class="modal-close" onclick="closeModal()"><i data-lucide="x" style="width: 20px; height: 20px;"></i></button>
      </div>
      <div class="modal-body">
        <div class="modal-title" id="modalTitle">매장명</div>
        <div class="modal-tags" id="modalTags"></div>
        <div class="modal-info-row"><div class="modal-info-label">도로명주소</div><div id="modalAddr">-</div></div>
        <div class="modal-info-row"><div class="modal-info-label">지번주소</div><div id="modalJibun">-</div></div>
        <div class="modal-info-row"><div class="modal-info-label">대표전화</div><div id="modalTel">-</div></div>
        <div class="modal-info-row"><div class="modal-info-label">개점일자</div><div id="modalOpen">-</div></div>
        <div class="modal-info-row"><div class="modal-info-label">운영업력</div><div id="modalYears">-</div></div>
        <div class="modal-info-row"><div class="modal-info-label">위도/경도</div><div id="modalCoord">-</div></div>
      </div>
    </div>
  </div>

  <script>
    // 2,213개 전체 매장 데이터 인라인 임베드
    const RAW_STORES = {stores_json};

    let filteredStores = [...RAW_STORES];
    let currentPage = 1;
    let pageSize = 30;
    let currentSpecialFilter = 'ALL';
    let currentSort = {{ column: 'open', ascending: false }};

    // Lucide Icons 초기화
    lucide.createIcons();

    // 초기 시도 드롭다운 구성
    function initSidoSelect() {{
      const sidoSet = new Set();
      RAW_STORES.forEach(s => {{ if (s.sido) sidoSet.add(s.sido); }});
      const sidoSelect = document.getElementById('sidoSelect');
      Array.from(sidoSet).sort().forEach(sido => {{
        const opt = document.createElement('option');
        opt.value = sido;
        opt.textContent = sido;
        sidoSelect.appendChild(opt);
      }});
    }}

    // 차트 인스턴스 보관
    let chartInstances = {{}};

    function initCharts() {{
      // 1. 시도별 매장 수
      const sidoCounts = {{}};
      RAW_STORES.forEach(s => {{ sidoCounts[s.sido] = (sidoCounts[s.sido] || 0) + 1; }});
      const sortedSido = Object.entries(sidoCounts).sort((a,b) => b[1] - a[1]);

      chartInstances.sido = new Chart(document.getElementById('chartSido'), {{
        type: 'bar',
        data: {{
          labels: sortedSido.map(x => x[0]),
          datasets: [{{
            label: '매장 수',
            data: sortedSido.map(x => x[1]),
            backgroundColor: '#008744',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 2. 매장 유형별 구성비
      const typeCounts = {{}};
      RAW_STORES.forEach(s => {{ typeCounts[s.type] = (typeCounts[s.type] || 0) + 1; }});
      chartInstances.type = new Chart(document.getElementById('chartType'), {{
        type: 'doughnut',
        data: {{
          labels: Object.keys(typeCounts),
          datasets: [{{
            data: Object.values(typeCounts),
            backgroundColor: ['#00704A', '#F87171', '#CBA258', '#38BDF8'],
            borderColor: 'transparent'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'right', labels: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 3. 연도별 출점 추이
      const yearCounts = {{}};
      RAW_STORES.forEach(s => {{
        if (s.year && Number(s.year) >= 1999) {{
          yearCounts[s.year] = (yearCounts[s.year] || 0) + 1;
        }}
      }});
      const sortedYears = Object.entries(yearCounts).sort((a,b) => Number(a[0]) - Number(b[0]));
      chartInstances.trend = new Chart(document.getElementById('chartTrend'), {{
        type: 'line',
        data: {{
          labels: sortedYears.map(x => x[0] + '년'),
          datasets: [{{
            label: '신규 개점 매장 수',
            data: sortedYears.map(x => x[1]),
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.15)',
            fill: true,
            tension: 0.35,
            pointRadius: 3
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 4. 시도별 DT 비중
      const sidoDT = {{}};
      const sidoTotal = {{}};
      RAW_STORES.forEach(s => {{
        sidoTotal[s.sido] = (sidoTotal[s.sido] || 0) + 1;
        if (s.is_dt) sidoDT[s.sido] = (sidoDT[s.sido] || 0) + 1;
      }});
      const dtRatios = Object.keys(sidoTotal).map(sido => ({{
        sido,
        ratio: Math.round(((sidoDT[sido] || 0) / sidoTotal[sido]) * 1000) / 10
      }})).sort((a,b) => b.ratio - a.ratio);

      chartInstances.dt = new Chart(document.getElementById('chartDTRatio'), {{
        type: 'bar',
        data: {{
          labels: dtRatios.map(x => x.sido),
          datasets: [{{
            label: 'DT 비율 (%)',
            data: dtRatios.map(x => x.ratio),
            backgroundColor: '#f87171',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 5. 서울 구별 TOP 10
      const seoulGuCounts = {{}};
      RAW_STORES.filter(s => s.sido === '서울').forEach(s => {{
        seoulGuCounts[s.gugun] = (seoulGuCounts[s.gugun] || 0) + 1;
      }});
      const sortedGu = Object.entries(seoulGuCounts).sort((a,b) => b[1] - a[1]).slice(0, 10);
      chartInstances.gu = new Chart(document.getElementById('chartSeoulGu'), {{
        type: 'bar',
        data: {{
          labels: sortedGu.map(x => x[0]),
          datasets: [{{
            label: '매장 수',
            data: sortedGu.map(x => x[1]),
            backgroundColor: '#a78bfa',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 6. 업력 구간 분포
      const yearBuckets = {{ '1년 미만': 0, '1~3년': 0, '3~5년': 0, '5~10년': 0, '10년 이상': 0 }};
      RAW_STORES.forEach(s => {{
        const y = s.years;
        if (y < 1) yearBuckets['1년 미만']++;
        else if (y < 3) yearBuckets['1~3년']++;
        else if (y < 5) yearBuckets['3~5년']++;
        else if (y < 10) yearBuckets['5~10년']++;
        else yearBuckets['10년 이상']++;
      }});

      chartInstances.years = new Chart(document.getElementById('chartYears'), {{
        type: 'bar',
        data: {{
          labels: Object.keys(yearBuckets),
          datasets: [{{
            label: '매장 수',
            data: Object.values(yearBuckets),
            backgroundColor: '#f59e0b',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});
    }}

    // 필터링 및 렌더링
    function applyFilters() {{
      const query = document.getElementById('searchInput').value.trim().toLowerCase();
      const selectedSido = document.getElementById('sidoSelect').value;

      filteredStores = RAW_STORES.filter(s => {{
        if (selectedSido !== 'ALL' && s.sido !== selectedSido) return false;

        if (currentSpecialFilter === 'DT' && !s.is_dt) return false;
        if (currentSpecialFilter === 'RES' && !s.is_res) return false;
        if (currentSpecialFilter === 'DEL' && !s.is_del) return false;
        if (currentSpecialFilter === 'NEW' && !s.is_new) return false;

        if (query) {{
          const match = s.name.toLowerCase().includes(query) ||
                        s.addr.toLowerCase().includes(query) ||
                        s.jibun.toLowerCase().includes(query) ||
                        s.gugun.toLowerCase().includes(query);
          if (!match) return false;
        }}
        return true;
      }});

      // 정렬 적용
      filteredStores.sort((a, b) => {{
        let valA = a[currentSort.column];
        let valB = b[currentSort.column];
        if (typeof valA === 'string') {{
          return currentSort.ascending ? valA.localeCompare(valB) : valB.localeCompare(valA);
        }}
        return currentSort.ascending ? valA - valB : valB - valA;
      }});

      currentPage = 1;
      renderTable();
      renderPagination();
      document.getElementById('filteredCountText').textContent = 
        `전체 ${{RAW_STORES.length.toLocaleString()}}개 매장 중 ${{filteredStores.length.toLocaleString()}}개 표시`;
    }}

    function renderTable() {{
      const tbody = document.getElementById('storeTableBody');
      tbody.innerHTML = '';

      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      const pageData = filteredStores.slice(start, end);

      if (pageData.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 40px; color: var(--text-muted);">조건에 부합하는 매장이 없습니다.</td></tr>';
        return;
      }}

      pageData.forEach(store => {{
        const tr = document.createElement('tr');
        tr.onclick = () => openModal(store);

        let typeBadge = '';
        if (store.is_res) typeBadge += '<span class="tag tag-res">리저브</span> ';
        if (store.is_dt) typeBadge += '<span class="tag tag-dt">DT</span> ';
        if (store.is_del) typeBadge += '<span class="tag tag-del">딜리버스</span> ';
        if (store.is_new) typeBadge += '<span class="tag tag-new">신규</span> ';
        if (!typeBadge) typeBadge = '<span class="tag tag-gen">일반</span>';

        tr.innerHTML = `
          <td style="font-weight: 600;">${{store.name}}</td>
          <td>${{typeBadge}}</td>
          <td>${{store.sido}}</td>
          <td>${{store.gugun}}</td>
          <td style="max-width: 320px; overflow: hidden; text-overflow: ellipsis;">${{store.addr}}</td>
          <td>${{store.tel}}</td>
          <td>${{store.open}}</td>
          <td>${{store.years}}년</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderPagination() {{
      const controls = document.getElementById('pageControls');
      controls.innerHTML = '';
      const totalPages = Math.ceil(filteredStores.length / pageSize) || 1;

      const prevBtn = document.createElement('button');
      prevBtn.className = 'page-btn';
      prevBtn.textContent = '이전';
      prevBtn.disabled = currentPage === 1;
      prevBtn.onclick = () => {{ currentPage--; renderTable(); renderPagination(); }};
      controls.appendChild(prevBtn);

      const maxButtons = 5;
      let startP = Math.max(1, currentPage - 2);
      let endP = Math.min(totalPages, startP + maxButtons - 1);
      if (endP - startP < maxButtons - 1) {{
        startP = Math.max(1, endP - maxButtons + 1);
      }}

      for (let p = startP; p <= endP; p++) {{
        const btn = document.createElement('button');
        btn.className = 'page-btn' + (p === currentPage ? ' active' : '');
        btn.textContent = p;
        btn.onclick = () => {{ currentPage = p; renderTable(); renderPagination(); }};
        controls.appendChild(btn);
      }}

      const nextBtn = document.createElement('button');
      nextBtn.className = 'page-btn';
      nextBtn.textContent = '다음';
      nextBtn.disabled = currentPage === totalPages;
      nextBtn.onclick = () => {{ currentPage++; renderTable(); renderPagination(); }};
      controls.appendChild(nextBtn);
    }}

    function handleSearch() {{ applyFilters(); }}
    function handleFilterChange() {{ applyFilters(); }}
    function handlePageSizeChange() {{
      pageSize = Number(document.getElementById('pageSizeSelect').value);
      applyFilters();
    }}

    function setSpecialFilter(type) {{
      currentSpecialFilter = type;
      document.querySelectorAll('.badge-filter').forEach(b => {{
        b.classList.toggle('active', b.dataset.filter === type);
      }});
      applyFilters();
    }}

    function sortTable(column) {{
      if (currentSort.column === column) {{
        currentSort.ascending = !currentSort.ascending;
      }} else {{
        currentSort.column = column;
        currentSort.ascending = true;
      }}
      applyFilters();
    }}

    // Modal Details
    function openModal(store) {{
      document.getElementById('modalTitle').textContent = store.name;
      const hero = document.getElementById('modalHero');
      if (store.img) {{
        hero.style.backgroundImage = `url('${{store.img}}')`;
      }} else {{
        hero.style.backgroundImage = 'none';
      }}

      let tagsHtml = '';
      if (store.is_res) tagsHtml += '<span class="tag tag-res">리저브(Reserve)</span> ';
      if (store.is_dt) tagsHtml += '<span class="tag tag-dt">드라이브스루(DT)</span> ';
      if (store.is_del) tagsHtml += '<span class="tag tag-del">딜리버스(Delivers)</span> ';
      if (store.is_new) tagsHtml += '<span class="tag tag-new">신규 매장</span> ';
      document.getElementById('modalTags').innerHTML = tagsHtml || '<span class="tag tag-gen">일반 매장</span>';

      document.getElementById('modalAddr').textContent = store.addr || '-';
      document.getElementById('modalJibun').textContent = store.jibun || '-';
      document.getElementById('modalTel').textContent = store.tel || '-';
      document.getElementById('modalOpen').textContent = store.open || '-';
      document.getElementById('modalYears').textContent = store.years ? store.years + '년' : '-';
      document.getElementById('modalCoord').textContent = `${{store.lat}}, ${{store.lon}}`;

      document.getElementById('detailModal').classList.add('active');
    }}

    function closeModal() {{
      document.getElementById('detailModal').classList.remove('active');
    }}

    function closeModalOnOverlay(e) {{
      if (e.target.id === 'detailModal') closeModal();
    }}

    // 테마 토글
    function toggleTheme() {{
      const body = document.body;
      const isLight = body.getAttribute('data-theme') === 'light';
      body.setAttribute('data-theme', isLight ? 'dark' : 'light');
    }}

    // CSV 내보내기
    function exportFilteredCSV() {{
      if (filteredStores.length === 0) {{
        alert('내보낼 데이터가 없습니다.');
        return;
      }}

      const headers = ['매장코드', '매장명', '매장유형', '시도', '구군', '도로명주소', '지번주소', '전화번호', '개점일', '업력(년)', '위도', '경도', 'DT여부', '리저브여부', '딜리버스여부', '신규여부'];
      const rows = filteredStores.map(s => [
        `"${{s.code}}"`,
        `"${{s.name}}"`,
        `"${{s.type}}"`,
        `"${{s.sido}}"`,
        `"${{s.gugun}}"`,
        `"${{s.addr}}"`,
        `"${{s.jibun}}"`,
        `"${{s.tel}}"`,
        `"${{s.open}}"`,
        s.years,
        s.lat,
        s.lon,
        s.is_dt ? 'Y' : 'N',
        s.is_res ? 'Y' : 'N',
        s.is_del ? 'Y' : 'N',
        s.is_new ? 'Y' : 'N'
      ]);

      const csvContent = '\\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `starbucks_filtered_${{new Date().toISOString().slice(0,10)}}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    }}

    // 초기 실행
    window.addEventListener('DOMContentLoaded', () => {{
      initSidoSelect();
      initCharts();
      applyFilters();
    }});
  </script>
</body>
</html>
"""

    output_path = "starbucks/dashboard.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] 글래스모피즘 인터랙티브 웹 대시보드 빌드 완료: {output_path} (크기: {len(html_content):,}자)")
    return output_path


if __name__ == "__main__":
    generate_dashboard()
