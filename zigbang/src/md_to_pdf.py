# -*- coding: utf-8 -*-
"""
EDA_Report.md -> 고품질 출판물급 PDF 변환기
- markdown 라이브러리로 HTML 파싱 (테이블, 코드블록 지원)
- 이미지 상대경로를 file:// 절대경로로 자동 변환
- 보고서 전용 CSS (Pretendard/Malgun Gothic 폰트, 다크네이비 헤더 테이블, 콜아웃, 차트 캡션)
- Playwright (msedge headless) 기반 A4 고해상도 PDF 렌더링
- 출력 파일: zigbang/reports/EDA_Report.pdf
"""

import sys
import os
import re
import asyncio
from pathlib import Path
import markdown
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
IMAGES_DIR = BASE_DIR / "images"
MD_FILE = REPORTS_DIR / "EDA_Report.md"
PDF_FILE = REPORTS_DIR / "EDA_Report.pdf"
HTML_TEMP = REPORTS_DIR / "EDA_Report_print.html"


def convert_md_to_html():
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 이미지 경로를 절대 file:/// 경로로 변환하여 렌더링 보장
    def replace_img_path(match):
        alt = match.group(1)
        rel_path = match.group(2)
        # ../images/xxx.png -> IMAGES_DIR / xxx.png
        img_name = Path(rel_path).name
        full_img_path = (IMAGES_DIR / img_name).resolve()
        return f'![{alt}](file:///{full_img_path.as_posix()})'

    md_text_fixed = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img_path, md_text)

    # Markdown -> HTML 변환 (테이블, 펜스코드, 메타데이터 확장)
    html_body = markdown.markdown(
        md_text_fixed,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"]
    )

    # 전문 보고서 스타일시트
    css = """
    @page {
        size: A4 portrait;
        margin: 18mm 15mm 20mm 15mm;
    }
    
    * {
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Pretendard', 'Malgun Gothic', 'Apple SD Gothic Neo', -apple-system, sans-serif;
        font-size: 10pt;
        line-height: 1.65;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
        word-break: keep-all;
    }
    
    /* 제목 스타일 */
    h1 {
        font-size: 19pt;
        font-weight: 800;
        color: #0f172a;
        margin-top: 0;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 2.5px solid #2563eb;
        line-height: 1.3;
        page-break-after: avoid;
    }
    
    h2 {
        font-size: 14pt;
        font-weight: 700;
        color: #1e3a8a;
        margin-top: 24px;
        margin-bottom: 10px;
        padding-bottom: 4px;
        border-bottom: 1.5px solid #cbd5e1;
        page-break-after: avoid;
    }
    
    h3 {
        font-size: 11.5pt;
        font-weight: 700;
        color: #334155;
        margin-top: 16px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }
    
    h4 {
        font-size: 10.5pt;
        font-weight: 600;
        color: #475569;
        margin-top: 12px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }
    
    p {
        margin-top: 0;
        margin-bottom: 10px;
        text-align: justify;
    }
    
    /* 인용구 및 콜아웃 블록 */
    blockquote {
        margin: 12px 0;
        padding: 10px 16px;
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        border-radius: 0 8px 8px 0;
        color: #334155;
        font-size: 9.5pt;
        line-height: 1.6;
        page-break-inside: avoid;
    }
    
    blockquote p {
        margin: 4px 0;
    }
    
    /* 리스트 스타일 */
    ul, ol {
        margin-top: 4px;
        margin-bottom: 12px;
        padding-left: 22px;
    }
    
    li {
        margin-bottom: 4px;
        line-height: 1.6;
    }
    
    li strong {
        color: #0f172a;
    }
    
    /* 표 스타일 */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 9pt;
        line-height: 1.45;
        page-break-inside: avoid;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    th {
        background-color: #1e293b;
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        padding: 8px 10px;
        border: 1px solid #334155;
        white-space: nowrap;
    }
    
    td {
        padding: 7px 10px;
        border: 1px solid #e2e8f0;
        color: #334155;
    }
    
    tr:nth-child(even) td {
        background-color: #f8fafc;
    }
    
    /* 수치형 정렬 */
    td:nth-child(n+3) {
        text-align: right;
    }
    td:nth-child(1), td:nth-child(2) {
        text-align: left;
    }
    
    /* 이미지 스타일 */
    img {
        display: block;
        max-width: 96%;
        height: auto;
        margin: 16px auto 8px auto;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
        page-break-inside: avoid;
    }
    
    /* 구분선 */
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 20px 0;
    }
    
    /* 코드 및 강조 */
    code {
        font-family: Consolas, 'Courier New', monospace;
        background-color: #f1f5f9;
        color: #0f766e;
        padding: 2px 5px;
        border-radius: 4px;
        font-size: 8.5pt;
    }
    
    strong {
        color: #0f172a;
        font-weight: 700;
    }
    
    em {
        color: #64748b;
    }
    """

    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>직방 오창읍 원룸·빌라 월세 심층 EDA 보고서</title>
    <style>
{css}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

    with open(HTML_TEMP, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[+] 인쇄용 HTML 변환 완료: {HTML_TEMP}")
    return HTML_TEMP


async def render_pdf():
    html_path = convert_md_to_html()
    file_url = f"file:///{html_path.resolve().as_posix()}"
    print(f"[*] Playwright 브라우저로 PDF 렌더링 시작: {file_url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_timeout(1500)  # 이미지 로드 대기

        # PDF 생성 옵션
        header_template = """
        <div style="font-family: 'Malgun Gothic', sans-serif; font-size: 8pt; color: #94a3b8; width: 100%; text-align: right; padding-right: 15mm;">
            직방 충북 청주시 오창읍 원룸·빌라 월세 시장 데이터 인텔리전스 리포트
        </div>
        """

        footer_template = """
        <div style="font-family: 'Malgun Gothic', sans-serif; font-size: 8pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding-left: 15mm; padding-right: 15mm;">
            <span>CONFIDENTIAL & PROPRIETARY — 2026 ZIGBANG RESEARCH</span>
            <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
        </div>
        """

        await page.pdf(
            path=str(PDF_FILE),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={
                "top": "20mm",
                "bottom": "20mm",
                "left": "15mm",
                "right": "15mm"
            }
        )

        await browser.close()

    print(f"[+] PDF 생성 성공! 파일 경로: {PDF_FILE}")
    if PDF_FILE.exists():
        size_kb = round(PDF_FILE.stat().st_size / 1024, 1)
        print(f"[+] PDF 파일 크기: {size_kb} KB")


if __name__ == "__main__":
    asyncio.run(render_pdf())
