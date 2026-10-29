# -*- coding: utf-8 -*-
import re
import shutil

src_file = "zigbang/dashboard.html"
bak_file = "zigbang/dashboard.html.bak"

# 1. 백업 생성
shutil.copy2(src_file, bak_file)
print(f"[+] 백업 파일 생성: {bak_file}")

with open(src_file, "r", encoding="utf-8") as f:
    html = f.read()

# 2. Leaflet CDN 제거
cdn_target = """  <!-- Leaflet CSS & JS CDN (인터랙티브 맵) -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <!-- Leaflet MarkerCluster -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>"""

if cdn_target in html:
    html = html.replace(cdn_target, "")
    print("[+] Leaflet CDN 링크 제거 성공")
else:
    # 정규식 대체
    html = re.sub(r'\s*<!-- Leaflet.*?leaflet\.markercluster\.js"></script>', '', html, flags=re.DOTALL)
    print("[+] Leaflet CDN 링크 (정규식) 처리")

# 3. CSS 스타일 제거 (#map, .quick-btn, .leaflet-popup-...)
css_pattern = r'\s*#map\s*\{[^}]+\}\s*\.quick-btn\s*\{[^}]+\}\s*\.quick-btn:hover\s*\{[^}]+\}\s*\.leaflet-popup-content-wrapper\s*\{[^}]+\}\s*\.leaflet-popup-tip\s*\{[^}]+\}'
html = re.sub(css_pattern, '', html)
print("[+] Leaflet & 지도 관련 CSS 스타일 제거")

# 4. 헤더 설명문 문구 수정
html = html.replace(
    "오창산단·2산단 일대 직방 실시간 시세, 6대 지표 분석 및 지리 인터랙티브 맵 탐색",
    "오창산단·2산단 일대 직방 실시간 시세 및 6대 핵심 지표 심층 분석"
)

# 5. 본문 지도 카드 UI 섹션 제거
map_card_pattern = r'\s*<!-- 인터랙티브 지도 섹션 \(Leaflet & 고도화\) -->\s*<div class="glass-card p-6">.*?<div id="map"></div>\s*</div>'
match = re.search(map_card_pattern, html, flags=re.DOTALL)
if match:
    html = html[:match.start()] + html[match.end():]
    print("[+] '오창읍 실시간 매물 지리 인터랙티브 맵' 카드 UI 섹션 삭제 성공")
else:
    print("[-] 지도 카드 UI 패턴을 찾지 못함. 직접 탐색 시도.")
    # 대체 방식
    start_str = '<!-- 인터랙티브 지도 섹션'
    end_str = '<div id="map"></div>\n    </div>'
    if start_str in html and end_str in html:
        idx1 = html.find(start_str)
        idx2 = html.find(end_str) + len(end_str)
        html = html[:idx1] + html[idx2:]
        print("[+] '오창읍 실시간 매물 지리 인터랙티브 맵' 카드 UI 섹션 (수동 인덱스) 삭제 성공")

# 6. JavaScript 내 map 관련 변수 제거
html = re.sub(r'\s*let map = null;\s*let markersCluster = null;', '', html)

# 7. DOMContentLoaded 내 initMap() 및 setTimeout 지도 리사이즈 제거
html = html.replace("      initMap();\n", "")
resize_block_pattern = r'\s*// \S+ Ÿ.*?setTimeout\(\(\) => \{\s*if \(map\) \{.*?fitMapToFilteredMarkers\(\);\s*\}\s*\}, 300\);'
html = re.sub(r'\s*// [^\n]*\s*setTimeout\(\(\) => \{\s*if \(map\) \{.*?\}, 300\);', '', html, flags=re.DOTALL)

# 8. btnResetFilters 내 flyToRegion 제거
html = html.replace("        flyToRegion('ALL');\n", "")

# 9. applyFilters 내 updateMapMarkers() 호출 제거
html = html.replace("      updateMapMarkers();\n", "")

# 10. 지도 관련 함수 전체(initMap, fitMapToFilteredMarkers, flyToRegion, updateMapMarkers) 삭제
# 함수 시작부터 initCharts 직전까지
funcs_pattern = r'\s*// Leaflet 인터랙티브 맵 초기화.*?function updateMapMarkers\(\) \{.*?\n    \}\n\n    // Chart\.js 6종 차트 초기화'
match_funcs = re.search(funcs_pattern, html, flags=re.DOTALL)
if match_funcs:
    html = html[:match_funcs.start()] + "\n\n    // Chart.js 6종 차트 초기화" + html[match_funcs.end() - len("    // Chart.js 6종 차트 초기화"):]
    print("[+] 지도 관련 JS 함수들 (initMap, fitMapToFilteredMarkers, flyToRegion, updateMapMarkers) 삭제 성공")
else:
    print("[-] JS 함수 패턴 매칭 실패, 대체 패턴 적용 시도")
    start_f = "// Leaflet 인터랙티브 맵 초기화"
    end_f = "// Chart.js 6종 차트 초기화"
    if start_f in html and end_f in html:
        idx_f1 = html.find(start_f)
        idx_f2 = html.find(end_f)
        html = html[:idx_f1] + html[idx_f2:]
        print("[+] 지도 관련 JS 함수들 (수동 인덱스) 삭제 성공")

# 11. 결과 저장
with open(src_file, "w", encoding="utf-8") as f:
    f.write(html)
print(f"[+] 수정된 {src_file} 저장 완료 (새 길이: {len(html)})")

# 루트에도 동일하게 동기화 (만약 사용자가 루트 파일 접근 시 대비)
shutil.copy2(src_file, "dashboard.html")
print("[+] 루트 dashboard.html 동기화 완료")
