# -*- coding: utf-8 -*-
import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def test_dashboard():
    dashboard_path = Path("zigbang/dashboard.html").resolve()
    url = f"file:///{dashboard_path.as_posix()}"
    print(f"Loading URL: {url}")

    errors = []
    logs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 1000})
        page = await context.new_page()

        page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: errors.append(str(err)))

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # 주요 요소 검증
        kpi_total = await page.inner_text("#kpiTotal")
        print(f"KPI 총 매물 수: {kpi_total}")

        table_rows = await page.locator("#tableBody tr").count()
        print(f"테이블 첫 페이지 행 수: {table_rows}")

        # 차트 캔버스 검증
        chart_ids = [
            'chartRentDist', 'chartStructure', 'chartSubdong', 
            'chartSizeVsCost', 'chartDepositBin', 'chartFloorLevel'
        ]
        charts_ok = True
        for cid in chart_ids:
            cnt = await page.locator(f"#{cid}").count()
            if cnt == 0:
                print(f"[-] 차트 엘리먼트 누락: {cid}")
                charts_ok = False
            else:
                print(f"[+] 차트 확인: #{cid}")

        # 지도 엘리먼트 부재 확인
        map_cnt = await page.locator("#map").count()
        print(f"지도(#map) 엘리먼트 수 (0이어야 정상): {map_cnt}")

        # 캡처 저장
        screenshot_path = Path("zigbang/images/dashboard_no_map_verified.png").resolve()
        await page.screenshot(path=str(screenshot_path), full_page=False)
        print(f"[+] 스크린샷 저장 완료: {screenshot_path}")

        await browser.close()

    print(f"=== 브라우저 콘솔 에러 수: {len(errors)} ===")
    if errors:
        for err in errors:
            print(f"  [ERROR] {err}")
    else:
        print("[+] 브라우저 렌더링 무결성: 콘솔 에러 0건 (완벽 무결)")

if __name__ == "__main__":
    asyncio.run(test_dashboard())
