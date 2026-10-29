# -*- coding: utf-8 -*-
import asyncio
import json
from playwright.async_api import async_playwright

async def inspect_zigbang_network():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    captured_requests = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        async def on_request(request):
            url = request.url
            if "apis.zigbang.com" in url or "zigbang.com/api" in url:
                post_data = request.post_data
                captured_requests.append({
                    "method": request.method,
                    "url": url,
                    "post_data": post_data[:200] if post_data else None,
                    "headers": dict(request.headers)
                })

        page.on("request", on_request)

        print("[*] 직방 빌라 지도 페이지 로딩...")
        await page.goto("https://www.zigbang.com/home/villa/map?lat=36.715&lng=127.43&zoom=15", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # 검색창에 '오창읍' 입력 시도
        try:
            search_input = page.locator("input[placeholder*='검색']").first
            if await search_input.is_visible():
                await search_input.click()
                await search_input.fill("오창읍")
                await page.wait_for_timeout(1500)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(4000)
        except Exception as e:
            print("검색 입력 예외:", e)

        await browser.close()

    print(f"[*] 캡처된 API 요청 수: {len(captured_requests)}")
    with open("zigbang/src/captured_api_requests.json", "w", encoding="utf-8") as f:
        json.dump(captured_requests, f, ensure_ascii=False, indent=2)

    for req in captured_requests:
        if any(keyword in req["url"] for keyword in ["items", "item", "villa", "oneroom", "article"]):
            print(f"-> {req['method']} {req['url'][:120]}")

if __name__ == "__main__":
    asyncio.run(inspect_zigbang_network())
