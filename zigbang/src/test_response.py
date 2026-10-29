# -*- coding: utf-8 -*-
import asyncio
import json
from playwright.async_api import async_playwright

async def inspect_response_body():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    sample_items = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        async def on_response(response):
            url = response.url
            if ("items/list" in url or "items/villas" in url or "items/oneroom" in url) and response.status == 200:
                try:
                    data = await response.json()
                    print(f"[Response] {url[:80]} -> keys: {list(data.keys()) if isinstance(data, dict) else len(data)}")
                    if "items" in data:
                        items = data["items"]
                        print(f"  found {len(items)} items")
                        if items and len(sample_items) < 3:
                            sample_items.extend(items[:3])
                except Exception as e:
                    pass

        page.on("response", on_response)

        # 오창읍 중심 좌표: lat=36.7119, lng=127.428 (오창 중심상업지구)
        print("[*] 오창읍 좌표로 빌라 맵 접속...")
        await page.goto("https://www.zigbang.com/home/villa/map?lat=36.7119&lng=127.428&zoom=15", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # 스크롤 동작
        await page.mouse.move(250, 400)
        for _ in range(5):
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(500)

        # 원룸 맵도 접속해보기
        print("[*] 오창읍 좌표로 원룸 맵 접속...")
        await page.goto("https://www.zigbang.com/home/oneroom/map?lat=36.7119&lng=127.428&zoom=15", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        await page.mouse.move(250, 400)
        for _ in range(5):
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(500)

        await browser.close()

    if sample_items:
        with open("zigbang/src/sample_item.json", "w", encoding="utf-8") as f:
            json.dump(sample_items[0], f, ensure_ascii=False, indent=2)
        print("[+] sample_item.json 저장 완료! 첫 번째 아이템 키:")
        print(list(sample_items[0].keys()))

if __name__ == "__main__":
    asyncio.run(inspect_response_body())
