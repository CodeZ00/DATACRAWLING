"""
YES24 베스트셀러 종합 EDA 마크다운 보고서의 고품질 PDF 변환 스크립트

이 모듈은 'yes24/docs/yes24_day_bestseller_eda_report.md' 마크다운 보고서를 파싱하여
인쇄용 고품질 CSS 스타일(A4 규격, 한글 맑은 고딕 폰트, 표 스타일, 이미지 최적화)이 적용된 HTML로 렌더링한 후,
헤드리스 브라우저 엔진(Chrome / Edge)을 통해 출판물 수준의 PDF 문서로 자동 변환합니다.

주요 기능:
1. 마크다운 표(Table), 인용구(Blockquote), 제목 태그의 HTML 파싱 (Python-Markdown 확장)
2. 이미지 상대경로를 Base64 인라인 데이터로 자동 변환하여 외부 의존성 없는 완결형 문서 생성
3. A4 인쇄 최적화 CSS 적용 (페이지 나눔 방지, 여백, 고해상도 테이블)
4. Chrome/Edge 헤드리스 PDF 렌더링 파이프라인 구동

작성일자: 2026-10-12
작성자: Antigravity 시니어 데이터 분석 에이전트
"""

import os
import re
import base64
import subprocess
import markdown

MD_PATH = os.path.join("yes24", "docs", "yes24_day_bestseller_eda_report.md")
HTML_PATH = os.path.join("yes24", "docs", "yes24_day_bestseller_eda_report.html")
PDF_PATH = os.path.join("yes24", "docs", "yes24_day_bestseller_eda_report.pdf")


def embed_images_as_base64(html_content: str, base_dir: str) -> str:
    """HTML 내의 로컬 이미지 상대경로를 Base64 인라인 데이터로 치환합니다."""
    def replacer(match):
        img_src = match.group(1)
        # 상대경로 결합
        if img_src.startswith("http://") or img_src.startswith("https://"):
            return match.group(0)
        
        full_img_path = os.path.normpath(os.path.join(base_dir, img_src))
        if os.path.exists(full_img_path):
            with open(full_img_path, "rb") as img_file:
                b64_str = base64.b64encode(img_file.read()).decode("utf-8")
                ext = os.path.splitext(full_img_path)[1].lower().replace(".", "")
                mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
                return f'<img src="data:image/{mime};base64,{b64_str}"'
        return match.group(0)

    return re.sub(r'<img\s+src="([^"]+)"', replacer, html_content)


def convert_md_to_pdf():
    print("=" * 70)
    print(" [PDF 변환 파이프라인] 마크다운 종합 보고서 -> 고품질 PDF 변환")
    print("=" * 70)

    if not os.path.exists(MD_PATH):
        print(f"[ERROR] 원본 마크다운 파일을 찾을 수 없습니다: {MD_PATH}")
        return

    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 1. 마크다운 -> HTML 변환 (테이블 및 펜스드 코드 블록 확장 활성화)
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"]
    )

    # 2. 이미지 Base64 임베딩
    docs_dir = os.path.dirname(MD_PATH)
    html_body_embedded = embed_images_as_base64(html_body, docs_dir)

    # 3. 인쇄용 프리미엄 CSS 스타일 정의
    css_style = """
    @page {
        size: A4;
        margin: 18mm 16mm 18mm 16mm;
        @bottom-right {
            content: counter(page);
        }
    }
    body {
        font-family: 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 10pt;
        line-height: 1.65;
        color: #222222;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }
    h1 {
        font-size: 20pt;
        font-weight: 800;
        color: #1a365d;
        border-bottom: 3px solid #2b5c8f;
        padding-bottom: 8px;
        margin-top: 0;
        margin-bottom: 14px;
    }
    h2 {
        font-size: 14pt;
        font-weight: 700;
        color: #2b5c8f;
        border-bottom: 1.5px solid #cbd5e1;
        padding-bottom: 5px;
        margin-top: 24px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }
    h3 {
        font-size: 12pt;
        font-weight: 700;
        color: #2d3748;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }
    h4 {
        font-size: 10.5pt;
        font-weight: 600;
        color: #4a5568;
        margin-top: 14px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }
    p {
        margin-top: 0;
        margin-bottom: 10px;
        text-align: justify;
    }
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 20px 0;
    }
    blockquote {
        margin: 10px 0 16px 0;
        padding: 10px 14px;
        background-color: #f8fafc;
        border-left: 4px solid #2b5c8f;
        color: #334155;
        font-size: 9.5pt;
        border-radius: 0 4px 4px 0;
        page-break-inside: avoid;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 16px 0;
        font-size: 8.5pt;
        page-break-inside: avoid;
    }
    th, td {
        border: 1px solid #cbd5e1;
        padding: 6px 8px;
        text-align: left;
    }
    th {
        background-color: #f1f5f9;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
    }
    tr:nth-child(even) {
        background-color: #f8fafc;
    }
    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 12px auto;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        page-break-inside: avoid;
    }
    strong {
        color: #0f172a;
    }
    ul, ol {
        margin-top: 0;
        margin-bottom: 10px;
        padding-left: 22px;
    }
    li {
        margin-bottom: 4px;
    }
    code {
        font-family: Consolas, monospace;
        font-size: 9pt;
        background-color: #f1f5f9;
        padding: 2px 4px;
        border-radius: 3px;
        color: #0f172a;
    }
    """

    complete_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>YES24 베스트셀러 EDA 종합 분석 보고서</title>
    <style>
{css_style}
    </style>
</head>
<body>
{html_body_embedded}
</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(complete_html)

    print(f"[*] 임베디드 HTML 문서 생성 완료: {HTML_PATH}")

    # 4. 헤드리스 브라우저 탐색 및 PDF 렌더링
    browser_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]

    browser_bin = None
    for cand in browser_candidates:
        if os.path.exists(cand):
            browser_bin = cand
            break

    if not browser_bin:
        print("[ERROR] Chrome 또는 Edge 브라우저를 찾을 수 없습니다.")
        return

    print(f"[*] 사용할 렌더링 엔진: {browser_bin}")

    abs_html = os.path.abspath(HTML_PATH)
    abs_pdf = os.path.abspath(PDF_PATH)

    cmd = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={abs_pdf}",
        "--no-pdf-header-footer",
        abs_html
    ]

    print("[*] 헤드리스 인쇄 엔진 구동 중...")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if os.path.exists(PDF_PATH):
            pdf_size = os.path.getsize(PDF_PATH)
            print("=" * 70)
            print(f"[SUCCESS] PDF 보고서 변환 완료!")
            print(f"[*] 생성된 파일 경로: {PDF_PATH}")
            print(f"[*] 파일 크기: {pdf_size:,} bytes")
            print("=" * 70)
        else:
            print("[ERROR] PDF 파일이 생성되지 않았습니다.")
    except Exception as e:
        print(f"[ERROR] PDF 렌더링 중 오류 발생: {e}")


if __name__ == "__main__":
    convert_md_to_pdf()
