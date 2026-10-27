import asyncio
import json
import os
from playwright.async_api import async_playwright

async def collect_all_sejong_officetels():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    all_collected_items = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        async def on_response(response):
            if "items/list" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    items = data.get('items', [])
                    for item in items:
                        item_id = item.get('item_id')
                        all_collected_items[item_id] = item
                except Exception:
                    pass
        
        page.on("response", on_response)
        
        await page.goto("https://www.zigbang.com/home/officetel/map", wait_until="commit")
        await page.wait_for_timeout(3000)
        
        # 정부청사 생활권 세부 지역 검색
        search_targets = [
            "세종특별자치시 어진동",
            "세종특별자치시 나성동",
            "세종특별자치시 도담동",
            "세종푸르지오시티",
            "세종 1차 푸르지오시티",
            "세종 2차 푸르지오시티",
            "세종포레뷰",
            "더리치호수의아침",
            "모닝시티"
        ]
        
        for query in search_targets:
            print(f"[*] 검색 진행: '{query}'")
            try:
                search_box = page.locator("input[type='text'], input[placeholder*='검색']").first
                await search_box.click()
                await search_box.fill(query)
                await page.wait_for_timeout(1000)
                
                # 자동완성 추천 클릭
                suggestions = await page.locator("li, div[role='button'], div[class*='item']").all()
                clicked = False
                for s in suggestions:
                    try:
                        text = await s.inner_text()
                        if any(w in text for w in ["세종", "어진", "나성", "도담", "푸르지오", "호수"]):
                            await s.click()
                            clicked = True
                            print(f"    -> 선택: {text.strip()[:35]}")
                            break
                    except Exception:
                        pass
                
                if not clicked:
                    await page.keyboard.press("Enter")
                
                await page.wait_for_timeout(3000)
                
                # 좌측 매물 리스트 패널 스크롤 (마우스 휠 5회)
                # 마우스 좌표를 좌측 패널(x=200, y=500)에 두고 휠
                await page.mouse.move(200, 500)
                for _ in range(8):
                    await page.mouse.wheel(0, 1500)
                    await page.wait_for_timeout(800)
                
            except Exception as e:
                print(f"    [!] 검색 에러 ({query}): {e}")
        
        await browser.close()
        
    print(f"\n[+] 총 수집된 원천 매물 수: {len(all_collected_items)}건")
    
    # 세종특별자치시 관련 매물 필터링
    sejong_items = {}
    for iid, it in all_collected_items.items():
        addr = it.get('addressOrigin', {})
        full_text = addr.get('fullText', '') or it.get('address', '')
        title = it.get('title', '')
        desc = it.get('desc', '')
        if '세종' in full_text or '어진' in full_text or '나성' in full_text or '도담' in full_text:
            sejong_items[iid] = it
        elif any(k in title for k in ['세종', '어진', '나성', '도담', '푸르지오시티', '호수의아침', '포레뷰']):
            sejong_items[iid] = it
    
    print(f"[+] 세종시 정부청사 생활권 확정 매물: {len(sejong_items)}건")
    
    # JSON 파일로 영구 저장
    os.makedirs("zigbang/data", exist_ok=True)
    out_path = "zigbang/data/sejong_officetels_full.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(list(sejong_items.values()), f, ensure_ascii=False, indent=2)
    print(f"[+] 전수 데이터 저장 완료: {out_path}")

if __name__ == "__main__":
    asyncio.run(collect_all_sejong_officetels())
