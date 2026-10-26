"""
스타벅스 심층 EDA 종합 분석 보고서 Markdown -> PDF 고품질 변환기
- markdown 라이브러리 및 고급 확장(tables, fenced_code 등) 파싱
- 이미지 Base64 데이터 URI 인라인 임베딩 (이미지 누락 원천 차단)
- 스타벅스 프리미엄 비주얼 인쇄용(Print CSS) 디자인 시스템 적용
- Chromium/Edge 헤드리스 엔진 기반 완벽한 A4 PDF 출력
"""

import base64
import os
import re
import subprocess
import sys
import markdown


def convert_images_to_base64(html_content, base_dir):
    """HTML 내의 로컬 이미지 경로를 Base64 Data URI로 치환하여 인라인 임베딩합니다."""
    def replacer(match):
        img_src = match.group(1)
        # 상대경로 결합
        if img_src.startswith("http://") or img_src.startswith("https://") or img_src.startswith("data:"):
            return match.group(0)

        # ../images/xxx or images/xxx 처리
        clean_path = img_src.replace("../", "")
        img_path = os.path.join(base_dir, clean_path)
        if not os.path.exists(img_path):
            # starbucks 루트 기준 탐색
            img_path = os.path.join("starbucks", clean_path)

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
    md_path = "starbucks/reports/EDA_Report.md"
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"{md_path} 파일이 없습니다.")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Markdown -> HTML 변환
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"]
    )

    # 이미지 Base64 임베딩
    html_body = convert_images_to_base64(html_body, "starbucks/reports")

    # 전문 리포트용 CSS 스타일링
    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>스타벅스 전국 매장 심층 EDA 종합 분석 보고서</title>
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    @page {{
      size: A4 portrait;
      margin: 18mm 15mm 20mm 15mm;
    }}

    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    body {{
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", sans-serif;
      font-size: 10pt;
      line-height: 1.75;
      color: #1f2937;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
    }}

    /* Title & Headers */
    h1 {{
      font-size: 20pt;
      font-weight: 800;
      color: #004f32;
      border-bottom: 2.5pt solid #cba258;
      padding-bottom: 8pt;
      margin-top: 0;
      margin-bottom: 12pt;
      letter-spacing: -0.5px;
    }}

    h2 {{
      font-size: 14pt;
      font-weight: 700;
      color: #004f32;
      border-left: 4pt solid #00704a;
      padding-left: 8pt;
      margin-top: 22pt;
      margin-bottom: 10pt;
      page-break-after: avoid;
    }}

    h3 {{
      font-size: 11.5pt;
      font-weight: 700;
      color: #1f2937;
      margin-top: 16pt;
      margin-bottom: 8pt;
      page-break-after: avoid;
    }}

    h4 {{
      font-size: 10pt;
      font-weight: 700;
      color: #4b5563;
      margin-top: 10pt;
      margin-bottom: 4pt;
    }}

    p {{
      margin-top: 0;
      margin-bottom: 8pt;
      text-align: justify;
    }}

    hr {{
      border: none;
      border-top: 1px solid #e5e7eb;
      margin: 16pt 0;
    }}

    /* Lists */
    ul, ol {{
      margin-top: 4pt;
      margin-bottom: 10pt;
      padding-left: 18pt;
    }}

    li {{
      margin-bottom: 4pt;
    }}

    /* Tables */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 12pt 0;
      font-size: 8.5pt;
      line-height: 1.5;
      page-break-inside: avoid;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}

    th {{
      background-color: #004f32;
      color: #ffffff;
      font-weight: 700;
      text-align: center;
      padding: 6pt 8pt;
      border: 1px solid #003a24;
    }}

    td {{
      padding: 5pt 8pt;
      border: 1px solid #e5e7eb;
      color: #374151;
    }}

    tr:nth-child(even) {{
      background-color: #f8faf9;
    }}

    /* Chart & Images */
    img {{
      max-width: 95%;
      height: auto;
      display: block;
      margin: 12pt auto;
      border-radius: 8pt;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      border: 1px solid #e5e7eb;
      page-break-inside: avoid;
    }}

    /* Highlights & Badges */
    strong {{
      color: #004f32;
      font-weight: 700;
    }}

    code {{
      background-color: #f3f4f6;
      color: #b91c1c;
      padding: 1.5pt 4pt;
      border-radius: 3pt;
      font-size: 8.5pt;
    }}

    /* Callout & Footer */
    .report-badge {{
      display: inline-block;
      background: #e6f4ea;
      color: #00704a;
      padding: 3pt 8pt;
      border-radius: 4pt;
      font-size: 8.5pt;
      font-weight: bold;
      margin-bottom: 8pt;
    }}
  </style>
</head>
<body>
  {html_body}
</body>
</html>
"""

    temp_html_path = "starbucks/reports/temp_report.html"
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[*] 임시 HTML 렌더링 완료: {temp_html_path}")

    # Edge 헤드리스 호출
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    output_pdf_path = os.path.abspath("starbucks/reports/EDA_Report.pdf")
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
    
    # 임시 파일 정리
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
        pdf_size = os.path.getsize(output_pdf_path)
        print(f"[+] PDF 생성 성공: {output_pdf_path} (크기: {pdf_size:,} bytes)")
        return output_pdf_path
    else:
        raise RuntimeError(f"PDF 생성 실패: {result.stderr}")


if __name__ == "__main__":
    generate_pdf()
