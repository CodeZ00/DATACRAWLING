# -*- coding: utf-8 -*-
with open("zigbang/dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

checks = {
    "Leaflet CDN presence": "leaflet@1.9.4" in text,
    "MarkerCluster CDN presence": "leaflet.markercluster" in text,
    "Map card title presence": "오창읍 실시간 매물 지리 인터랙티브 맵" in text,
    "id='map' or id='map' div": 'id="map"' in text or "id='map'" in text,
    "initMap call or def": "initMap" in text,
    "updateMapMarkers call or def": "updateMapMarkers" in text,
    "flyToRegion call or def": "flyToRegion" in text,
    "fitMapToFilteredMarkers call or def": "fitMapToFilteredMarkers" in text,
    "Chart.js presence (should be True)": "chart.js" in text or "Chart(" in text,
    "Table presence (should be True)": "tableItemsBody" in text,
    "KPI elements presence (should be True)": "kpiTotal" in text
}

print("=== 정적 검증 결과 ===")
for k, v in checks.items():
    status = "정상" if (("presence (should be True)" in k and v) or ("presence (should be True)" not in k and not v)) else "주의필요"
    print(f"[{status}] {k}: {v}")
