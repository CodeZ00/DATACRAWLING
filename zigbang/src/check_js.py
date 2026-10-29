# -*- coding: utf-8 -*-
with open("zigbang/dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# let allItems = rawData.items; 등을 찾기
lines = text.split("\n")
for idx, line in enumerate(lines):
    if "allItems = rawData.items" in line or "initMap" in line or "DOMContentLoaded" in line:
        print(f"Line {idx+1}: {line}")
