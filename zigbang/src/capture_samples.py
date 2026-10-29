# -*- coding: utf-8 -*-
import asyncio
import json
from playwright.async_api import async_playwright

async def capture_samples():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    villa_items = []
    detailed_items = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        async def on_response(response):
            url = response.url
            if response.status == 200:
                if ("items/villas?" in url or "items/onerooms?" in url) and not villa_items:
                    try:
                        data = await response.json()
                        if "items" in data:
                            villa_items.extend(data["items"][:10])
                    except Exception:
                        pass
                elif "items/list" in url and not detailed_items:
                    try:
                        data = await response.json()
                        if "items" in data:
                            detailed_items.extend(data["items"][:5])
                    except Exception:
                        pass

        page.on("response", on_response)

        try:
            # 오창읍 중심
            await page.goto("https://www.zigbang.com/home/villa/map?lat=36.7119&lng=127.428&zoom=15", wait_until="domcontentloaded")
            await page.wait_for_timeout(4000)
            await page.mouse.move(250, 400)
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(3000)
        except Exception as e:
            print("Navigation error:", e)

        await browser.close()

    if villa_items:
        with open("zigbang/src/sample_cluster_items.json", "w", encoding="utf-8") as f:
            json.dump(villa_items, f, ensure_ascii=False, indent=2)
        print(f"[+] sample_cluster_items.json 저장: {len(villa_items)}건")

    if detailed_items:
        with open("zigbang/src/sample_detailed_items.json", "w", encoding="utf-8") as f:
            json.dump(detailed_items, f, ensure_ascii=False, indent=2)
        print(f"[+] sample_detailed_items.json 저장: {len(detailed_items)}건")

if __name__ == "__main__":
    asyncio.run(capture_samples())
