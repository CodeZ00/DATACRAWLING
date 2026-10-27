"""직방 세종 오피스텔 종합 분석 보고서 Markdown -> PDF 고품질 변환기.

- markdown 라이브러리 파싱
- 이미지 Base64 인라인 임베딩 (이미지 누락 원천 차단)
- 직방 앰버 골드 테마 인쇄용(Print CSS) 디자인 시스템 적용
- Edge 헤드리스 엔진 기반 완벽한 A4 PDF 출력
"""

import base64
import os
import re
import subprocess
import sys
import markdown


def convert_images_to_base64(html_content, base_dir):
    """HTML 내 로컬 이미지 경로를 Base64 Data URI로 치환"""
    def replacer(match):
        img_src = match.group(1)
        if img_src.startswith("http://") or img_src.startswith("https://") or img_src.startswith("data:"):
            return match.group(0)

        clean_path = img_src.replace("../", "")
        img_path = os.path.join(base_dir, clean_path)
        if not os.path.exists(img_path):
            img_path = os.path.join("zigbang", clean_path)

        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(img_path)[1].lower().replace(".", "")
            if ext == "jpg":
                ext = "jpeg"
            return f'src="data:image/{ext};base64,{encoded}"'
        return match.group(0)

    pattern = r'src=["\']([^"\']+)["\']'
    return re.sub(pattern, replacer, html_content)


def generate_pdf():
    md_path = "zigbang/reports/EDA_Report.md"
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"{md_path} 파일이 없습니다.")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Markdown 변환
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "toc"]
    )

    base_dir = "zigbang"
    html_body = convert_images_to_base64(html_body, base_dir)

    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>세종특별자치시 정부청사 생활권 오피스텔 심층 EDA 종합 분석 보고서</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 15mm 18mm 15mm;
        @bottom-right {{
            content: counter(page);
            font-size: 9pt;
            color: #64748B;
        }}
    }}
    body {{
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Malgun Gothic", sans-serif;
        color: #1E293B;
        line-height: 1.65;
        font-size: 10.5pt;
        background: #FFFFFF;
        margin: 0;
        padding: 0;
    }}
    h1 {{
        color: #D97706;
        font-size: 20pt;
        font-weight: 800;
        border-bottom: 3px solid #F59E0B;
        padding-bottom: 8px;
        margin-top: 0;
        margin-bottom: 16px;
    }}
    h2 {{
        color: #B45309;
        font-size: 14pt;
        font-weight: 700;
        border-bottom: 1.5px solid #FDE68A;
        padding-bottom: 5px;
        margin-top: 24px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }}
    h3 {{
        color: #92400E;
        font-size: 12pt;
        font-weight: 600;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    p {{
        margin-top: 0;
        margin-bottom: 10px;
        text-align: justify;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 9.5pt;
        page-break-inside: avoid;
    }}
    th {{
        background-color: #FEF3C7;
        color: #92400E;
        font-weight: 700;
        border: 1px solid #FCD34D;
        padding: 7px 10px;
        text-align: center;
    }}
    td {{
        border: 1px solid #E2E8F0;
        padding: 6px 10px;
        color: #334155;
    }}
    tr:nth-child(even) {{
        background-color: #FFFDF5;
    }}
    img {{
        max-width: 95%;
        height: auto;
        display: block;
        margin: 12px auto;
        border-radius: 6px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        page-break-inside: avoid;
    }}
    blockquote {{
        border-left: 4px solid #F59E0B;
        background: #FFFBEB;
        margin: 14px 0;
        padding: 10px 14px;
        color: #78350F;
        border-radius: 0 6px 6px 0;
        page-break-inside: avoid;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    temp_html_path = "zigbang/reports/temp_report.html"
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    output_pdf_path = os.path.abspath("zigbang/reports/EDA_Report.pdf")
    input_html_abs = os.path.abspath(temp_html_path)

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf_path}",
        input_html_abs
    ]

    print(f"[*] Edge 헤드리스 PDF 변환 실행 중...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
        pdf_size = os.path.getsize(output_pdf_path)
        print(f"[+] PDF 생성 성공: {output_pdf_path} (크기: {pdf_size:,} bytes)")
        return output_pdf_path
    else:
        print(f"[!] PDF 변환 스킵 또는 실패: {result.stderr}")
        return None


if __name__ == "__main__":
    generate_pdf()
