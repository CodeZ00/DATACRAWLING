# -*- coding: utf-8 -*-
with open("zigbang/dashboard.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if any(k in line for k in ["실시간 매물 지리 인터랙티브 맵", "id=\"map\"", "id='map'", "L.map", "leaflet", "map-container"]):
        print(f"Line {i+1}: {line.strip()[:100]}")
