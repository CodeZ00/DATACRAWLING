# -*- coding: utf-8 -*-
with open("zigbang/dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
canvases = re.findall(r'<canvas[^>]*id=["\']([^"\']+)["\']', text)
print("Canvas IDs in dashboard.html:", canvases)
