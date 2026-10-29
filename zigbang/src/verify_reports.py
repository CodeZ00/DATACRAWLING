# -*- coding: utf-8 -*-
"""
DOCX 및 PPTX 산출물 무결성 정밀 검증 스크립트
- Ochang_Villa_Rent_Report.docx
- Ochang_Villa_Rent_Presentation.pptx
검증 항목:
1. 파일 존재 및 용량
2. 1인 가구 분석 내용 포함 여부
3. 양청택지로 124-32(은하빌라B) 평가 수록 여부
4. 11종 차트 이미지 삽입 및 배치
5. 슬라이드 수(16장) 및 16:9 규격 확인
6. 전 슬라이드 발표자 노트(Speaker Notes) 글자수 및 정합성
7. 표 및 텍스트 블록 통계
"""

import sys
import json
from pathlib import Path
from docx import Document
from pptx import Presentation

BASE_DIR = Path(__file__).resolve().parent.parent
DOCX_PATH = BASE_DIR / "reports" / "Ochang_Villa_Rent_Report.docx"
PPTX_PATH = BASE_DIR / "reports" / "Ochang_Villa_Rent_Presentation.pptx"

def verify_docx(path):
    result = {
        "file_exists": path.exists(),
        "file_size_bytes": path.stat().st_size if path.exists() else 0,
        "paragraphs_count": 0,
        "tables_count": 0,
        "images_count": 0,
        "keywords_found": {},
        "target_keywords": [
            "1인 가구", "RIR", "슈바베", "양청택지로", "124-32", "은하빌라", 
            "관리비 전가", "호수공원", "복층형", "TF-IDF"
        ],
        "headings": []
    }
    
    if not path.exists():
        return result

    doc = Document(str(path))
    result["paragraphs_count"] = len(doc.paragraphs)
    result["tables_count"] = len(doc.tables)

    full_text = []
    for p in doc.paragraphs:
        if p.style.name.startswith("Heading"):
            result["headings"].append((p.style.name, p.text.strip()))
        if p.text:
            full_text.append(p.text)

    # 테이블 텍스트도 취합
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                full_text.append(cell.text)

    joined_text = " ".join(full_text)
    for kw in result["target_keywords"]:
        result["keywords_found"][kw] = joined_text.count(kw)

    # 이미지 카운트 (inline_shapes & XML blip 확인)
    image_count = 0
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_count += 1
    result["images_count"] = image_count

    return result


def verify_pptx(path):
    result = {
        "file_exists": path.exists(),
        "file_size_bytes": path.stat().st_size if path.exists() else 0,
        "slides_count": 0,
        "slide_width_inches": 0,
        "slide_height_inches": 0,
        "is_16_9": False,
        "slides_detail": [],
        "target_keywords": [
            "1인 가구", "양청택지로 124-32", "은하빌라", "3.8만 원", "RIR", "KDE", "TF-IDF"
        ],
        "keywords_found": {}
    }

    if not path.exists():
        return result

    prs = Presentation(str(path))
    result["slides_count"] = len(prs.slides)
    w_in = round(prs.slide_width.inches, 3)
    h_in = round(prs.slide_height.inches, 3)
    result["slide_width_inches"] = w_in
    result["slide_height_inches"] = h_in
    result["is_16_9"] = (abs(w_in - 13.333) < 0.05 and abs(h_in - 7.5) < 0.05)

    all_slide_text = []

    for idx, slide in enumerate(prs.slides, start=1):
        slide_info = {
            "slide_num": idx,
            "shapes_count": len(slide.shapes),
            "images_count": 0,
            "title": "",
            "speaker_notes": "",
            "notes_char_count": 0
        }

        # 텍스트 및 이미지 추출
        for shape in slide.shapes:
            if shape.has_text_frame:
                txt = shape.text_frame.text.strip()
                if not slide_info["title"] and txt:
                    lines = [l.strip() for l in txt.split("\n") if l.strip()]
                    if lines:
                        slide_info["title"] = lines[0]
                all_slide_text.append(txt)
            if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
                slide_info["images_count"] += 1

        # 발표자 노트 추출
        if slide.has_notes_slide:
            notes_tf = slide.notes_slide.notes_text_frame
            notes_text = notes_tf.text.strip()
            slide_info["speaker_notes"] = notes_text
            slide_info["notes_char_count"] = len(notes_text)
            all_slide_text.append(notes_text)

        result["slides_detail"].append(slide_info)

    joined_pptx_text = " ".join(all_slide_text)
    for kw in result["target_keywords"]:
        result["keywords_found"][kw] = joined_pptx_text.count(kw)

    return result


if __name__ == "__main__":
    print("[*] DOCX 및 PPTX 정밀 검증 시작...")
    docx_res = verify_docx(DOCX_PATH)
    pptx_res = verify_pptx(PPTX_PATH)

    output = {
        "docx_verification": docx_res,
        "pptx_verification": pptx_res
    }

    with open(BASE_DIR / "reports" / "verification_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"[+] DOCX 검증 결과: 단락 {docx_res['paragraphs_count']}개, 표 {docx_res['tables_count']}개, 이미지 {docx_res['images_count']}개, 양청택지로 키워드 {docx_res['keywords_found'].get('양청택지로', 0)}회")
    print(f"[+] PPTX 검증 결과: 슬라이드 {pptx_res['slides_count']}장, 16:9 와이드 여부 {pptx_res['is_16_9']}, 양청택지로 키워드 {pptx_res['keywords_found'].get('양청택지로 124-32', 0)}회")
    print("[+] 검증 결과가 verification_result.json 에 저장되었습니다.")
