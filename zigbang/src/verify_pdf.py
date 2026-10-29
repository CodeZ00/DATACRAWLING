# -*- coding: utf-8 -*-
import json
from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "reports" / "EDA_Report.pdf"

def verify():
    reader = PdfReader(str(PDF_PATH))
    total_pages = len(reader.pages)

    full_text = []
    page_stats = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        full_text.append(text)
        page_stats.append({
            "page": i + 1,
            "char_count": len(text)
        })

    all_text = " ".join(full_text)

    keywords = [
        "오창읍", "원룸", "빌라", "1인 가구", "RIR", "양청택지로", "124-32",
        "은하빌라", "보증금", "실질 총 주거비용", "호수공원", "TF-IDF"
    ]

    kw_res = {kw: all_text.count(kw) for kw in keywords}

    res = {
        "total_pages": total_pages,
        "total_chars": len(all_text),
        "file_size_bytes": PDF_PATH.stat().st_size,
        "keywords": kw_res,
        "page_stats": page_stats
    }

    with open(BASE_DIR / "reports" / "pdf_verification_result.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Total {total_pages} pages, {len(all_text)} chars, size: {PDF_PATH.stat().st_size} bytes")

if __name__ == "__main__":
    verify()
