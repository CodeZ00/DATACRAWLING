# -*- coding: utf-8 -*-
with open("zigbang/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

print("Original length:", len(content))

# 1. Leaflet CDN 확인
has_leaflet = "leaflet@1.9.4" in content
print("Has Leaflet CDN:", has_leaflet)

# 2. 지도 카드 HTML 섹션 확인
has_map_card = "오창읍 실시간 매물 지리 인터랙티브 맵" in content
print("Has Map Card:", has_map_card)

# 3. JS 함수 확인
has_initMap = "function initMap()" in content
has_updateMapMarkers = "function updateMapMarkers()" in content
print("Has initMap:", has_initMap, "Has updateMapMarkers:", has_updateMapMarkers)
