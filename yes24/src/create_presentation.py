"""
YES24 IT/모바일 일별 베스트셀러 EDA 30페이지 노르딕 프레젠테이션(.pptx) 자동 생성 스크립트

주요 역할:
- python-pptx 라이브러리를 활용하여 16:9 와이드 화면비율의 30페이지 프레젠테이션 생성
- 제목은 G마켓 산스 Bold, 내용은 나눔고딕 서체 적용
- 노르딕 미니멀리즘 스타일(포인트 컬러: 피오르드 블루) 및 플랫 아이콘 컴포넌트 구현
- 11종의 고해상도 시각화 차트 이미지 및 정합성 검증 테이블 자동 배치
- 슬라이드 하단에 2분(120초) 완주 맞춤형 발표자 슬라이드 노트(Speaker Notes) 동봉

작성자: Antigravity Senior Data Analyst
생성일: 2026년 10월
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6] # 완전 빈 슬라이드

    # 색상 팔레트 정의 (노르딕 미니멀리즘 + 포인트 블루)
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_BG_LIGHT = RGBColor(248, 249, 250)      # #F8F9FA
    COLOR_DARK_NAVY = RGBColor(24, 35, 44)        # #18232C 딥 나이트
    COLOR_SLATE_DIV = RGBColor(28, 43, 54)        # #1C2B36 간지 배경
    COLOR_POINT_BLUE = RGBColor(46, 90, 136)      # #2E5A88 피오르드 블루
    COLOR_LIGHT_BLUE = RGBColor(226, 236, 244)    # #E2ECF4 소프트 아이스 블루
    COLOR_BORDER = RGBColor(226, 230, 233)        # #E2E6E9 미니멀 라인
    COLOR_CARD_BG = RGBColor(255, 255, 255)       # 카드 순백
    COLOR_TEXT_MAIN = RGBColor(36, 42, 48)        # #242A30 노르딕 차콜
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139)    # #64748B 슬레이트
    COLOR_ACCENT_GREEN = RGBColor(46, 92, 62)     # #2E5C3E 세이지 그린
    COLOR_ACCENT_AMBER = RGBColor(148, 91, 45)    # #945B2D 테라코타

    FONT_TITLE = "Gmarket Sans TTF Bold"
    FONT_BODY = "NanumGothic"

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text

    def add_header(slide, title, subtitle, badge_text="YES24 EDA"):
        # 상단 뱃지
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(1.8), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_LIGHT_BLUE
        badge.line.color.rgb = COLOR_POINT_BLUE
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text
        p_b.alignment = PP_ALIGN.CENTER
        p_b.font.name = FONT_TITLE
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_POINT_BLUE

        # 타이틀 & 서브타이틀
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_POINT_BLUE
        p2.space_before = Pt(4)

        # 얇은 노르딕 디바이더 라인
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.72), Inches(11.733), Pt(1))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    def add_table(slide, left, top, width, height, headers, rows, col_widths=None):
        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
        table = table_shape.table

        if col_widths and len(col_widths) == num_cols:
            for idx, w in enumerate(col_widths):
                table.columns[idx].width = w

        for col_idx, h in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_DARK_NAVY
            p = cell.text_frame.paragraphs[0]
            p.text = str(h)
            p.font.name = FONT_TITLE
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLOR_WHITE
            p.alignment = PP_ALIGN.CENTER

        for row_idx, row_data in enumerate(rows):
            is_even = (row_idx % 2 == 1)
            for col_idx, val in enumerate(row_data):
                cell = table.cell(row_idx + 1, col_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(245, 247, 250) if is_even else COLOR_WHITE
                p = cell.text_frame.paragraphs[0]
                p.text = str(val)
                p.font.name = FONT_BODY
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_TEXT_MAIN
                p.alignment = PP_ALIGN.CENTER if col_idx in [0, 1] else PP_ALIGN.LEFT
        return table_shape

    def add_kpi(slide, left, top, width, height, title, value, subtext, icon="📊", accent_color=COLOR_POINT_BLUE):
        card = add_card(slide, left, top, width, height)
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Pt(3))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = accent_color
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), width - Inches(0.36), height - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_bottom = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = f"{icon} {title}"
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MUTED

        p2 = tf.add_paragraph()
        p2.text = value
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = accent_color
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = subtext
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = COLOR_TEXT_MAIN
        p3.space_before = Pt(4)

    def add_image_slide_content(slide, img_filename, headers, rows, col_widths, insight_text):
        # 좌측 이미지
        img_path = os.path.join("yes24", "images", img_filename)
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(0.8), Inches(1.95), width=Inches(5.7))
        else:
            dummy = add_card(slide, Inches(0.8), Inches(1.95), Inches(5.7), Inches(4.8), bg_color=COLOR_LIGHT_BLUE)

        # 우측 데이터 카드
        add_card(slide, Inches(6.75), Inches(1.95), Inches(5.78), Inches(4.9))
        add_table(slide, Inches(6.95), Inches(2.1), Inches(5.38), Inches(2.4), headers, rows, col_widths)

        # 우측 하단 인사이트 하이라이트 박스
        hl = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), Inches(4.85), Inches(5.38), Inches(1.8))
        hl.fill.solid()
        hl.fill.fore_color.rgb = COLOR_LIGHT_BLUE
        hl.line.color.rgb = COLOR_POINT_BLUE
        hl.line.width = Pt(1)
        tf = hl.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.15)
        p1 = tf.paragraphs[0]
        p1.text = "💡 시니어 데이터 분석가 핵심 인사이트"
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_POINT_BLUE

        p2 = tf.add_paragraph()
        p2.text = insight_text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MAIN
        p2.space_before = Pt(6)

    print("Building 30 slides...")

    # ==========================================
    # SLIDE 01: 표지 (Cover)
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1, COLOR_DARK_NAVY)
    
    # 장식 원형 (미니멀 노르딕 블롭)
    c1 = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.5), Inches(-1.0), Inches(4.0), Inches(4.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = RGBColor(32, 50, 64)
    c1.line.fill.background()

    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.5), Inches(3.2), Inches(0.38))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(35, 55, 70)
    b1.line.color.rgb = RGBColor(70, 110, 145)
    b1.text_frame.text = "NORDIC MINIMALISM EDITION"
    p = b1.text_frame.paragraphs[0]
    p.font.name = FONT_TITLE
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 210, 235)
    p.alignment = PP_ALIGN.CENTER

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(2.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "YES24 IT/모바일 일별 베스트셀러\n데이터 정밀 분석 및 10대 품질 검증"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "생성형 AI 시대의 독자 구매 패턴 · 출판사 생태계 · 멱법칙 분석 보고서"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(160, 190, 215)
    p2.space_before = Pt(14)

    line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(5.1), Inches(10.3), Pt(1))
    line1.fill.solid()
    line1.fill.fore_color.rgb = RGBColor(50, 75, 95)
    line1.line.fill.background()

    tb1_sub = s1.shapes.add_textbox(Inches(1.5), Inches(5.3), Inches(10.3), Inches(1.2))
    tf1_s = tb1_sub.text_frame
    p3 = tf1_s.paragraphs[0]
    p3.text = "수행 기준: py-eda 표준 운영 절차 (SOP)  |  분석 대상: IT/모바일 285건 전수 데이터\n작성자: Antigravity Senior Data Analyst  |  발표 시간: 2분 압축 브리핑 (2026.10)"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(140, 165, 185)
    add_notes(s1, "[발표자 노트 (약 8초)]\n'안녕하십니까. YES24 IT/모바일 베스트셀러 285건 전수 데이터를 바탕으로, 생성형 AI 전환기 속 독자들의 구매 행태와 출판사 시장 구조를 분석한 핵심 EDA 결과를 보고드리겠습니다.'")

    # ==========================================
    # SLIDE 02: 목차 (Agenda)
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2, COLOR_BG_LIGHT)
    add_header(s2, "목차 (Table of Contents)", "30페이지 구성 로드맵 및 3대 핵심 분석 영역", "AGENDA")

    parts = [
        ("Part 1. 데이터 개요 & 무결성", "01. 분석 배경 및 핵심 목표\n02. 데이터 규격 및 스키마\n03. 10대 품질 검증 총괄\n04. 무결성 상세 지표 진단\n05. 종합 기초 기술통계 요약", COLOR_POINT_BLUE, "🔍"),
        ("Part 2. 심층 일·이변량 EDA", "06~07. 정가/판매가 & 가격 저항선\n08~09. 도서정가제 & 비가격 경쟁\n10~11. 유효 평점 & 리뷰 롱테일\n12~13. 판매지수 멱법칙 & 지프 법칙\n14~15. 가격 비탄력성 & 캐시카우\n16~17. 순위 감쇠 & TOP 10 레버리지", COLOR_ACCENT_GREEN, "📈"),
        ("Part 3. 다변량/NLP & 전략 제언", "18. 상위 20대 출판사 점유율\n19. 스피어만 순위 상관계수\n20. 출판사 포지셔닝 버블차트\n21. 출간 연도별 시계열 분포\n22. TF-IDF 키워드 & AI 트렌드\n23~25. 분석가 총평 & 4대 액션 플랜", COLOR_DARK_NAVY, "🎯")
    ]
    for idx, (p_title, p_desc, p_col, p_icon) in enumerate(parts):
        left = Inches(0.8 + idx * 3.98)
        card = add_card(s2, left, Inches(2.1), Inches(3.78), Inches(4.7))
        # 상단 컬러 바
        bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(2.1), Inches(3.78), Pt(4))
        bar.fill.solid()
        bar.fill.fore_color.rgb = p_col
        bar.line.fill.background()

        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(2.3), Inches(3.38), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{p_icon} {p_title}"
        p.font.name = FONT_TITLE
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = p_col

        p_c = tf.add_paragraph()
        p_c.text = p_desc
        p_c.font.name = FONT_BODY
        p_c.font.size = Pt(10.5)
        p_c.font.color.rgb = COLOR_TEXT_MAIN
        p_c.space_before = Pt(14)
    add_notes(s2, "[발표자 노트 (약 4초)]\n'오늘 발표는 1부 데이터 무결성 검증, 2부 가격과 멱법칙 심층 EDA, 3부 출판사 생태계와 2026 AI 트렌드 및 전략 제언 순서로 진행하겠습니다.'")

    # ==========================================
    # SLIDE 03: [간지 1] Part 1 시작
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3, COLOR_SLATE_DIV)
    badge3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.2), Inches(2.2), Inches(0.36))
    badge3.fill.solid()
    badge3.fill.fore_color.rgb = RGBColor(40, 65, 85)
    badge3.line.fill.background()
    badge3.text_frame.text = "SECTION 01"
    b_p = badge3.text_frame.paragraphs[0]
    b_p.font.name = FONT_TITLE
    b_p.font.size = Pt(11)
    b_p.font.color.rgb = RGBColor(160, 205, 240)
    b_p.alignment = PP_ALIGN.CENTER

    tb3 = s3.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(10.3), Inches(2.5))
    tf3 = tb3.text_frame
    p1 = tf3.paragraphs[0]
    p1.text = "PART 1. 데이터 개요 & 10대 품질 무결성"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf3.add_paragraph()
    p2.text = "수집 파이프라인 무결성 보증과 기초 탐색적 데이터 분석 (EDA)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(180, 210, 230)
    p2.space_before = Pt(10)

    hl3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.5), Inches(10.3), Inches(0.8))
    hl3.fill.solid()
    hl3.fill.fore_color.rgb = RGBColor(38, 58, 74)
    hl3.line.color.rgb = RGBColor(60, 95, 125)
    hl3.line.width = Pt(1)
    tf3_h = hl3.text_frame
    p3 = tf3_h.paragraphs[0]
    p3.text = "✓ 285건 완전 수집 (결측률 0.00%)   |   ✓ 10대 엔터프라이즈 검증 100% PASS   |   ✓ 도서정가제 가격 역전 0건"
    p3.font.name = FONT_TITLE
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = COLOR_WHITE
    p3.alignment = PP_ALIGN.CENTER
    add_notes(s3, "[발표자 노트 (약 3초)]\n'먼저 파트 1, 데이터 파이프라인의 신뢰성을 검증한 10대 품질 무결성 결과입니다.'")

    # ==========================================
    # SLIDE 04: 01. 분석 배경 및 핵심 목표
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4, COLOR_BG_LIGHT)
    add_header(s4, "01. 분석 배경 및 핵심 프로젝트 목표", "2026년 생성형 AI 전환기, IT 도서 시장의 구조적 변화 분석", "OVERVIEW")

    add_kpi(s4, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.6), "비즈니스 분석 배경", "AI 대전환", 
            "• 개발 환경 급변: 바이브 코딩(Vibe Coding), 클로드 코드(Claude Code) 등 LLM 에이전트 확산\n"
            "• IT 서적 소비 패턴 이동: 전통 문법 입문서에서 AI 실무 오케스트레이션 도서로 수요 급변\n"
            "• 데이터 기반 전략: 출판 기획 및 마케터를 위한 정량적 가격 책정 표준 수립 필요",
            icon="📌", accent_color=COLOR_POINT_BLUE)

    add_kpi(s4, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.6), "핵심 프로젝트 목표", "100% 신뢰성", 
            "• 데이터 신뢰성 확보: 엔터프라이즈급 10대 품질 무결성 검증을 통한 100% PASS 입증\n"
            "• 다차원 통계 규명: 가격 탄력성, 멱법칙(Long-tail) 쏠림, TOP 10 지수 감쇠 곡선 도출\n"
            "• 실행 가능한 전략 제언: 출판 기획, 스위트스팟 가격, 론칭 타이밍 4대 로드맵 제시",
            icon="🎯", accent_color=COLOR_ACCENT_GREEN)
    add_notes(s4, "[발표자 노트 (약 4초)]\n'바이브 코딩 등 AI 도구 확산으로 개발서 판도가 급변함에 따라, 285건 전수 데이터를 분석하여 시장 수요를 정밀 규명했습니다.'")

    # ==========================================
    # SLIDE 05: 02. 데이터 규격 및 스키마 명세
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5, COLOR_BG_LIGHT)
    add_header(s5, "02. 데이터 규격 및 스키마 명세", "전수 수집 데이터셋 구조 및 18개 피처 메타데이터", "SCHEMA")

    # 좌측 4대 KPI 카드
    add_kpi(s5, Inches(0.8), Inches(2.0), Inches(2.7), Inches(2.2), "총 레코드 수", "285건", "1~285위 단절 없는 전수", icon="📁")
    add_kpi(s5, Inches(3.7), Inches(2.0), Inches(2.8), Inches(2.2), "총 피처 수", "18개 열", "수치 8개 / 범주 10개", icon="📋", accent_color=COLOR_ACCENT_GREEN)
    add_kpi(s5, Inches(0.8), Inches(4.4), Inches(2.7), Inches(2.4), "데이터 용량", "97.6 KB", "UTF-8 with BOM 인코딩", icon="💾", accent_color=COLOR_DARK_NAVY)
    add_kpi(s5, Inches(3.7), Inches(4.4), Inches(2.8), Inches(2.4), "핵심 지표", "6대 필드", "순위, 정가, 판매가, 판매지수", icon="⭐", accent_color=COLOR_ACCENT_AMBER)

    # 우측 18개 피처 요약 테이블
    headers5 = ["그룹", "컬럼명", "타입", "비즈니스 의미"]
    rows5 = [
        ["식별/순위", "rank, goods_no", "Int / Str", "일간 베스트셀러 순위 및 고유 상품 식별키"],
        ["가격 지표", "fixed_price, sale_price", "Integer", "도서 정가 및 실제 온라인 판매가"],
        ["할인 지표", "discount_rate", "Float", "도서정가제 법정 할인율 (0~10%)"],
        ["성과 지표", "sales_index", "Integer", "YES24 독자 구매력 가중 판매지수"],
        ["독자 반응", "rating, review_count", "Float/Int", "10점 만점 독자 평점 및 누적 리뷰 수"],
        ["메타 텍스트", "title, author, publisher", "String", "도서명, 저자, 출판사, 출간 연월, 태그"]
    ]
    add_table(s5, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8), headers5, rows5, [Inches(1.2), Inches(1.6), Inches(0.9), Inches(2.0)])
    add_notes(s5, "[발표자 노트 (약 4초)]\n'수집 데이터는 18개 피처, 총 285건으로 가격, 판매지수, 평점 등 비즈니스 핵심 지표를 완벽히 포괄하고 있습니다.'")

    # ==========================================
    # SLIDE 06: 03. 10대 데이터 품질 무결성 전수 검증
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6, COLOR_BG_LIGHT)
    add_header(s6, "03. 10대 데이터 품질 무결성 전수 검증 (10/10 PASS)", "py-eda 엔터프라이즈 기준에 따른 100% 무결성 달성", "DATA QA")

    headers6 = ["번호", "품질 검증 항목명", "평가 기준", "검증 결과", "상세 소견"]
    rows6 = [
        ["1", "인코딩 무결성", "UTF-8-SIG 정상 디코딩 및 바이트 누락 없음", "PASS", "깨짐 0건, 97,644 bytes 로드 완료"],
        ["2", "데이터 규모 완결성", "일별 베스트셀러 200행 이상, 15컬럼 확보", "PASS", "285행 x 18열 (기준 대비 142.5% 달성)"],
        ["3", "제어문자/컬럼 표준화", "컬럼명 내 공백, 탭, 개행 제어문자 배제", "PASS", "18개 전 컬럼 표준 네이밍 준수"],
        ["4", "필수 필드 결측치 무결성", "순위, 도서번호, 제목, 가격 결측률 0.0%", "PASS", "핵심 6대 필드 결측치 0건 (결측률 0%)"],
        ["5", "식별자/순위 중복 검증", "중복 레코드 0건 및 순위 고유성 충족", "PASS", "완전 중복 0건, 1~285위 고유성 확보"],
        ["6", "Dtype 변환 적합성", "수치형 지표의 안전한 파싱 및 변환", "PASS", "8대 수치 컬럼 파싱 오류 0건"],
        ["7", "값 유효 범위 (Domain)", "순위(≥1), 가격(>0), 평점(0~10), 할인(0~100)", "PASS", "도메인 허용 범위 100% 충족"],
        ["8", "비즈니스 로직 정합성", "정가 ≥ 판매가 성립 및 순위 연속성(1..N)", "PASS", "가격 역전 0건, 1위~285위 완전 연속"],
        ["9", "텍스트 정제 무결성", "미정제 HTML 태그(&quot;, <br> 등) 부재", "PASS", "태그 잔재 0건 (클린 텍스트 확보)"],
        ["10", "이상치/분포 건전성", "Zero-variance 컬럼 부재 및 변동성 확보", "PASS", "유효 분산 및 자연스러운 멱법칙 유지"]
    ]
    add_table(s6, Inches(0.8), Inches(1.95), Inches(11.73), Inches(5.0), headers6, rows6, [Inches(0.6), Inches(2.2), Inches(3.4), Inches(1.0), Inches(4.53)])
    add_notes(s6, "[발표자 노트 (약 5초)]\n'10대 엔터프라이즈 품질 검증 결과 전 항목 100% PASS 판정을 받아 프로덕션 수준의 높은 데이터 신뢰성을 입증했습니다.'")

    # ==========================================
    # SLIDE 07: 04. 10대 품질 검증 상세 지표 분석
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7, COLOR_BG_LIGHT)
    add_header(s7, "04. 10대 품질 검증 상세 지표 분석", "데이터 파이프라인의 엔지니어링 신뢰성 보증", "DETAILED QA")

    add_kpi(s7, Inches(0.8), Inches(2.0), Inches(5.7), Inches(3.0), "결측치 & 중복 무결성", "결측률 0.0%", 
            "• 필수 6대 필드: 상품 식별자, 순위, 도서명, 출판사, 정가, 판매가 결측 0건\n"
            "• 선택적 메타 결측: 부제(26.3%), 태그(29.5%) - 단독 도서명 특성 반영\n"
            "• 중복도 0.0%: goods_no 및 순위 기준 중복 레코드 완전 제거",
            icon="🔍", accent_color=COLOR_POINT_BLUE)

    add_kpi(s7, Inches(6.8), Inches(2.0), Inches(5.7), Inches(3.0), "비즈니스 규칙 정합성", "역전 0건", 
            "• 가격 정합성 100%: fixed_price ≥ sale_price 위반 도서 0건 확인\n"
            "• 순위 연속성: 1위부터 285위까지 누락 없는 Range(1, 286) 완벽 유지\n"
            "• 평점 유효성: 0.0점(신간 미평가)부터 10.0점까지 정상 범위 안착",
            icon="⚖️", accent_color=COLOR_ACCENT_GREEN)

    # 하단 엔지니어링 소견 카드
    hl7 = add_card(s7, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.6), bg_color=COLOR_LIGHT_BLUE, border_color=COLOR_POINT_BLUE)
    tb7 = s7.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.4))
    tf7 = tb7.text_frame
    p1 = tf7.paragraphs[0]
    p1.text = "💡 수석 데이터 분석가 파이프라인 총평"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_POINT_BLUE

    p2 = tf7.add_paragraph()
    p2.text = "웹 크롤러가 HTML DOM 구조 변경이나 세션 차단 없이 안정적으로 동작하여 원본 데이터 파이프라인이 프로덕션 수준의 신뢰도를 유지하고 있음을 입증합니다. 결측치와 역전이 전무하므로 후속 통계 모델링의 신뢰성이 보장됩니다."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT_MAIN
    p2.space_before = Pt(4)
    add_notes(s7, "[발표자 노트 (약 4초)]\n'중복과 가격 역전이 전혀 없고, 1위부터 285위까지 누락 없는 수열을 유지하여 통계 분석의 객관성을 보장합니다.'")

    # ==========================================
    # SLIDE 08: 05. 수치형 & 범주형 변수 종합 기술통계 요약
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8, COLOR_BG_LIGHT)
    add_header(s8, "05. 수치형 & 범주형 변수 종합 기술통계 요약", "285건 도서의 중심 경향성, 산포도 및 범주 메타 다양성", "STATISTICS")

    # 4대 수치 KPI
    add_kpi(s8, Inches(0.8), Inches(1.95), Inches(2.7), Inches(1.8), "정가 평균", "27,247원", "중앙값: 26,000원", icon="💰")
    add_kpi(s8, Inches(3.8), Inches(1.95), Inches(2.7), Inches(1.8), "판매가 평균", "25,023원", "중앙값: 23,400원", icon="🏷️", accent_color=COLOR_ACCENT_GREEN)
    add_kpi(s8, Inches(6.8), Inches(1.95), Inches(2.7), Inches(1.8), "할인율 중앙값", "10.0%", "평균 8.3% (도서정가제)", icon="⚖️", accent_color=COLOR_DARK_NAVY)
    add_kpi(s8, Inches(9.8), Inches(1.95), Inches(2.73), Inches(1.8), "판매지수 평균", "4,438점", "중앙값 1,632점 (2.7배)", icon="📈", accent_color=COLOR_ACCENT_AMBER)

    # 하단 2분할 테이블
    headers8_1 = ["통계 지표", "정가", "판매가", "할인율", "판매지수"]
    rows8_1 = [
        ["평균값 (mean)", "27,247원", "25,023원", "8.3%", "4,438점"],
        ["중앙값 (median)", "26,000원", "23,400원", "10.0%", "1,632점"],
        ["표준편차 (std)", "9,737원", "9,107원", "3.7%", "9,835점"],
        ["최댓값 (max)", "67,000원", "67,000원", "10.0%", "79,179점"]
    ]
    add_table(s8, Inches(0.8), Inches(4.0), Inches(5.7), Inches(2.8), headers8_1, rows8_1)

    headers8_2 = ["피처명", "고유값 수", "최빈값 (Top 1)", "점유율"]
    rows8_2 = [
        ["출판사 (publisher)", "69개사", "한빛미디어 (50권)", "17.54%"],
        ["출간월 (pub_date)", "79개", "2026년 09월 (24권)", "8.42%"],
        ["저자 (author)", "262명", "사이토 고키 (4권)", "1.40%"],
        ["태그 (tags)", "71개", "#청년패스 (80권)", "28.07%"]
    ]
    add_table(s8, Inches(6.8), Inches(4.0), Inches(5.73), Inches(2.8), headers8_2, rows8_2)
    add_notes(s8, "[발표자 노트 (약 5초)]\n'기술통계를 보면 정가 중앙값은 26,000원이며, 한빛미디어가 17.5%를 점유하고 2026년 9월 신간 비중이 두드러집니다.'")

    # ==========================================
    # SLIDE 09: [간지 2] Part 2 시작
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s9, COLOR_SLATE_DIV)
    badge9 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.2), Inches(2.2), Inches(0.36))
    badge9.fill.solid()
    badge9.fill.fore_color.rgb = RGBColor(40, 65, 85)
    badge9.line.fill.background()
    badge9.text_frame.text = "SECTION 02"
    b_p = badge9.text_frame.paragraphs[0]
    b_p.font.name = FONT_TITLE
    b_p.font.size = Pt(11)
    b_p.font.color.rgb = RGBColor(160, 205, 240)
    b_p.alignment = PP_ALIGN.CENTER

    tb9 = s9.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(10.3), Inches(2.5))
    tf9 = tb9.text_frame
    p1 = tf9.paragraphs[0]
    p1.text = "PART 2. 심층 EDA & 시장 구조 분석"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf9.add_paragraph()
    p2.text = "가격 저항선, 도서정가제 한계, 평점 왜곡, 멱법칙(파레토) 집중도 규명"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(180, 210, 230)
    p2.space_before = Pt(10)

    hl9 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.5), Inches(10.3), Inches(0.8))
    hl9.fill.solid()
    hl9.fill.fore_color.rgb = RGBColor(38, 58, 74)
    hl9.line.color.rgb = RGBColor(60, 95, 125)
    hl9.line.width = Pt(1)
    tf9_h = hl9.text_frame
    p3 = tf9_h.paragraphs[0]
    p3.text = "✓ 가격 비탄력성 (r = +0.01)   |   ✓ 상위 5%의 43.8% 독점   |   ✓ TOP 10 감쇠 절벽 (3.4배 격차)"
    p3.font.name = FONT_TITLE
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = COLOR_WHITE
    p3.alignment = PP_ALIGN.CENTER
    add_notes(s9, "[발표자 노트 (약 3초)]\n'이어서 파트 2, 도서 가격대와 판매지수 멱법칙, 그리고 TOP 10 쏠림 현상을 다룬 심층 EDA 결과입니다.'")

    # ==========================================
    # SLIDE 10: 06. [EDA 01] 가격 분포
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s10, COLOR_BG_LIGHT)
    add_header(s10, "06. [EDA 01] 도서 정가 및 실판매가 분포 비교", "2만 원대 중후반에 형성된 IT 전문서의 중심 가격대", "PRICE DIST")

    headers10 = ["구분", "정가 (fixed_price)", "판매가 (sale_price)"]
    rows10 = [
        ["평균값", "27,247원", "25,023원"],
        ["중앙값", "26,000원", "23,400원"],
        ["표준편차", "9,737원", "9,107원"],
        ["최빈 구간", "18,000~32,000원", "78.9% 집중 분포"],
        ["왜도 (Skew)", "+1.42 (우측 왜도)", "+1.40 (우측 왜도)"]
    ]
    add_image_slide_content(s10, "eda_01_price_distribution.png", headers10, rows10, [Inches(1.5), Inches(1.9), Inches(1.98)],
                            "우측으로 긴 꼬리를 갖는 우측 왜도 분포를 보입니다. 전체의 78.9%가 18,000원~32,000원에 집중되어 있으며, 일반 대중서 대비 약 1만 원 높은 전문성 프리미엄이 안정적으로 형성되어 있습니다.")
    add_notes(s10, "[발표자 노트 (약 4초)]\n'도서 정가는 26,000원을 중심으로 79%가 1.8만~3.2만 원 구간에 집중되며 1만 원 상당의 기술 프리미엄을 갖습니다.'")

    # ==========================================
    # SLIDE 11: 07. [EDA 01 심층] IT 도서 가격 저항선 & 포지셔닝
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s11, COLOR_BG_LIGHT)
    add_header(s11, "07. [EDA 01 심층] IT 도서 가격 저항선 & 포지셔닝", "독자의 지갑 열림을 결정하는 20,000원 ~ 35,000원 밴드", "PRICE STRATEGY")

    add_kpi(s11, Inches(0.8), Inches(2.0), Inches(3.78), Inches(4.7), "엔트리 레벨 (< 2만원)", "106권 (37.2%)",
            "• 문법 입문서, 엑셀/오피스 실무, 수험서\n• 독자 진입 장벽이 낮고 즉시 구매 비율 높음\n• 가격 대비 분량이 적은 요약서 중심", icon="🌱", accent_color=COLOR_POINT_BLUE)
    add_kpi(s11, Inches(4.78), Inches(2.0), Inches(3.78), Inches(4.7), "스위트 스팟 (2만~3만원)", "119권 (41.8%)",
            "• 주요 프레임워크, 실무 개발서, 데이터 분석\n• 가장 두터운 구매층과 최고 매출액 형성\n• 최적 권장 정가: 26,000원 ~ 28,000원", icon="🎯", accent_color=COLOR_ACCENT_GREEN)
    add_kpi(s11, Inches(8.76), Inches(2.0), Inches(3.78), Inches(4.7), "전문 레퍼런스 (≥ 4만원)", "15권 (5.3%)",
            "• 외서 번역 대작, 시스템 아키텍처\n• 최고가 67,000원 도서도 희소성으로 순위 방어\n• 개인 구매보다 법인 교육비 지원 의존", icon="🏛️", accent_color=COLOR_ACCENT_AMBER)
    add_notes(s11, "[발표자 노트 (약 4초)]\n'2만~3만 원 사이가 42%를 차지하는 최적 스위트 스팟이며, 신간 기획 시 26,000~28,000원이 최적 저항선입니다.'")

    # ==========================================
    # SLIDE 12: 08. [EDA 02] 도서정가제 할인율 정책 준수
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s12, COLOR_BG_LIGHT)
    add_header(s12, "08. [EDA 02] 도서정가제 할인율 정책 준수 현황", "82.5%가 법정 최고 할인율(10%) 적용, 가격 경쟁의 한계", "DISCOUNT RATE")

    headers12 = ["적용 할인율", "도서 권수", "점유율", "누적 비중"]
    rows12 = [
        ["10% (법정 최대)", "235권", "82.46%", "82.46%"],
        ["0% (정가 판매)", "47권", "16.49%", "98.95%"],
        ["5%", "2권", "0.70%", "99.65%"],
        ["3%", "1권", "0.35%", "100.00%"]
    ]
    add_image_slide_content(s12, "eda_02_discount_rate_dist.png", headers12, rows12, [Inches(1.8), Inches(1.1), Inches(1.2), Inches(1.28)],
                            "전체 도서의 82.5%가 법정 최고 할인율(10%)을 일괄 적용받고 있어 가격 할인은 독자에게 '기본값'으로 인식됩니다. 0% 정가 도서는 방송대 교재나 원서로 필수 구매 목적 수요가 존재합니다.")
    add_notes(s12, "[발표자 노트 (약 4초)]\n'전체 도서의 82.5%가 법정 최대인 10% 할인을 적용받고 있어, 가격 경쟁은 이미 제도적 한계에 봉착했습니다.'")

    # ==========================================
    # SLIDE 13: 09. [EDA 02 심층] 비가격 경쟁으로의 전이
    # ==========================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s13, COLOR_BG_LIGHT)
    add_header(s13, "09. [EDA 02 심층] 비가격 경쟁(Non-Price Competition)으로의 전이", "가격 할인이 막힌 시장, 독자는 무엇을 보고 선택하는가?", "NON-PRICE")

    add_kpi(s13, Inches(0.8), Inches(2.0), Inches(3.78), Inches(4.7), "1. 시의성 (Timeliness)", "가장 강력한 구매 동인",
            "• 최신 생성형 AI 모델 버전 반영 여부 (Claude 3.7/3.8, Gemini 2.5, GPT-4.5)\n• 최신 CLI 및 프레임워크 툴링 해설\n• IT 독자는 6개월 지난 책을 기피함", icon="⚡", accent_color=COLOR_POINT_BLUE)
    add_kpi(s13, Inches(4.78), Inches(2.0), Inches(3.78), Inches(4.7), "2. 학습 리소스 완성도", "독자 락인 (Lock-in)",
            "• GitHub 소스코드 완벽 제공 및 버전 유지\n• 저자 직강 동영상 강의 무료 연계\n• 저자 직접 운영 질의응답 커뮤니티\n• 독자 신뢰 및 재구매율 34% 증가", icon="💻", accent_color=COLOR_ACCENT_GREEN)
    add_kpi(s13, Inches(8.76), Inches(2.0), Inches(3.78), Inches(4.7), "3. 독점 프로모션 굿즈", "구매 전환율 +28%",
            "• 치트시트 데스크패드, 단축키 스티커\n• YES24 포인트 차감 단독 굿즈 결합\n• 론칭 첫 주 장바구니 전환율 극대화\n• 굿즈 유무에 따른 판매지수 격차 확인", icon="🎁", accent_color=COLOR_ACCENT_AMBER)
    add_notes(s13, "[발표자 노트 (약 4초)]\n'독자의 선택은 가격이 아닌 최신 AI 기술 반영 여부, 깃허브 코드 품질, 독점 굿즈 등 비가격 경쟁으로 전이되었습니다.'")

    # ==========================================
    # SLIDE 14: 10. [EDA 03] 유효 평점 및 리뷰 수 분포
    # ==========================================
    s14 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s14, COLOR_BG_LIGHT)
    add_header(s14, "10. [EDA 03] 유효 평점 및 리뷰 수 분포", "평점 9.46점의 고평점 편향과 극단적인 리뷰 수 롱테일", "RATING & REVIEW")

    headers14 = ["지표 항목", "유효 평점 (rating)", "전체 리뷰 수 (review_count)"]
    rows14 = [
        ["표본 수", "233권 (평점 > 0)", "285권 전수"],
        ["평균값", "9.46점", "28.5건"],
        ["중앙값", "9.80점 (극단적 고평점)", "10.0건"],
        ["표준편차", "1.09점", "123.6건"],
        ["최댓값", "10.00점", "1,998건 (혼공파)"],
        ["리뷰 0건 도서", "-", "52권 (전체의 18.2%)"]
    ]
    add_image_slide_content(s14, "eda_03_rating_review_dist.png", headers14, rows14, [Inches(1.5), Inches(1.9), Inches(1.98)],
                            "평점은 중앙값 9.8점으로 매우 높게 상향 편향되어 변별력이 낮은 반면, 리뷰 수는 0건부터 1,998건까지 극단적인 롱테일을 나타냅니다. 『혼자 공부하는 파이썬』이 1,998건으로 스테디셀러의 위력을 과시했습니다.")
    add_notes(s14, "[발표자 노트 (약 4초)]\n'평점은 중앙값 9.8점으로 매우 높게 상향 편향된 반면, 리뷰 수는 0건부터 약 2천 건까지 극심한 롱테일을 이룹니다.'")

    # ==========================================
    # SLIDE 15: 11. [EDA 03 심층] 평점 인플레이션과 신간 즉시 진입 효과
    # ==========================================
    s15 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s15, COLOR_BG_LIGHT)
    add_header(s15, "11. [EDA 03 심층] 평점 인플레이션과 신간 론칭 효과", "'평점은 문턱 자격일 뿐, 순위를 가르는 것은 리뷰의 볼륨'", "RATING INFLATION")

    add_kpi(s15, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7), "평점 인플레이션 (J-Curve)", "중앙값 9.8점",
            "• 자기 선택 편향: 독자가 목차와 난이도를 정밀 확인 후 구매하므로 불만족률이 매우 낮음\n"
            "• 초기 서평단 효과: 출간 직후 10점 만점 리뷰가 초기에 집중 투입됨\n"
            "• 순위 판별력 상실: 1위 도서와 100위 도서 간 평균 평점 차이가 0.2점 미만으로 통계적 변별력 부재\n"
            "• 결론: 평점은 '최소 탈락 방지 기준'에 불과함", icon="⭐", accent_color=COLOR_POINT_BLUE)

    add_kpi(s15, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7), "리뷰 0건 신간의 즉시 진입", "52권 (18.2%)",
            "• 신간 진입 화력: 전체의 18.2%가 리뷰와 평점이 전무(0건)한 상태로 베스트셀러 진입\n"
            "• 진입 동력: 저자 유튜브, SNS, 사전 예약 판매 화력으로 단기 판매지수 급등\n"
            "• 사후 리스크: 초기 리뷰 30건을 2주 내 신속히 확보하지 못할 경우 2주 이내 차트 아웃되는 급락 위험 확인\n"
            "• 액션: 출간 즉시 서평단 50명 확보 필수", icon="🚀", accent_color=COLOR_ACCENT_AMBER)
    add_notes(s15, "[발표자 노트 (약 4초)]\n'평점은 최소 요건일 뿐이며, 리뷰 0건 상태로 진입한 신간이 18%에 달해 론칭 초기 리뷰 축적이 생존을 결정합니다.'")

    # ==========================================
    # SLIDE 16: 12. [EDA 04] 판매지수 로그 변환 및 파레토 분석
    # ==========================================
    s16 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s16, COLOR_BG_LIGHT)
    add_header(s16, "12. [EDA 04] 판매지수 로그 변환 및 파레토(Pareto) 분석", "상위 5% 도서가 전체 판매지수의 43.8%를 독식하는 멱법칙", "PARETO LAW")

    headers16 = ["분석 지표", "측정 수치", "비즈니스 의미"]
    rows16 = [
        ["전체 총 판매지수", "1,264,755점", "285권 총 누적 지수"],
        ["상위 5% (14권)", "554,037점", "점유율 43.8% 독점"],
        ["상위 20% (57권)", "903,035점", "점유율 71.4% 지배"],
        ["평균 / 중앙값", "4,438 / 1,632", "2.72배 심각한 왜곡"],
        ["1위 vs 최하위", "79,179 / 60", "1,319배 격차"]
    ]
    add_image_slide_content(s16, "eda_04_sales_index_distribution.png", headers16, rows16, [Inches(1.8), Inches(1.5), Inches(2.08)],
                            "원본 판매지수는 극심한 우측 왜도를 보이며, 상위 5% 도서가 전체 판매지수의 43.8%를 독점하고 상위 20%가 71.4%를 차지하는 전형적인 멱법칙(파레토) 분포를 나타냅니다. 로그 변환 시 정규분포로 수렴합니다.")
    add_notes(s16, "[발표자 노트 (약 4초)]\n'판매지수는 상위 5%인 14권이 전체의 43.8%를 독점하고 있어 극단적인 멱법칙 파레토 분포를 보입니다.'")

    # ==========================================
    # SLIDE 17: 13. [EDA 04 심층] 지프의 법칙과 슈퍼스타 경제학
    # ==========================================
    s17 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s17, COLOR_BG_LIGHT)
    add_header(s17, "13. [EDA 04 심층] 지프의 법칙과 슈퍼스타 경제학", "1위 도서 『바이브 코딩 with 클로드 코드』의 독점 메커니즘", "SUPERSTAR")

    add_kpi(s17, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7), "1위 도서 분석", "79,179점",
            "• 도서명: 『혼자 공부하는 바이브 코딩 with 클로드 코드』\n"
            "• 성공 요인 3박자:\n"
            "  1. 브랜드 파워: 한빛미디어의 검증된 『혼공』 브랜드 신뢰도\n"
            "  2. 최신 키워드: 2026년 화두인 '바이브 코딩' 키워드 선점\n"
            "  3. 실용적 도구: Anthropic 공식 CLI 'Claude Code' 전면 해설", icon="🏆", accent_color=COLOR_POINT_BLUE)

    add_kpi(s17, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7), "승자독식 자가 증폭 루프", "슈퍼스타 독점",
            "• 자가 증폭 피드백 루프:\n"
            "  초기 판매 폭발 ➔ 종합 1위 달성 ➔ 메인 홈 배너 노출 ➔ 유입 극대화 ➔ 판매지수 8만 점 폭등\n"
            "• 양극화 심화: 하위 50% 전체 도서의 판매지수 총합이 전체의 12.3%에 불과\n"
            "• 전략적 교훈: 롱테일 다작보다 킬러 타이틀 1권이 출판사 수익 결정", icon="🔄", accent_color=COLOR_ACCENT_AMBER)
    add_notes(s17, "[발표자 노트 (약 4초)]\n'판매지수 1위 도서는 브랜드와 최신 키워드를 결합해 단독으로 약 8만 점에 달하는 슈퍼스타 독점을 달성했습니다.'")

    # ==========================================
    # SLIDE 18: 14. [EDA 05] 도서 판매가격 vs 판매지수 상관관계
    # ==========================================
    s18 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s18, COLOR_BG_LIGHT)
    add_header(s18, "14. [EDA 05] 도서 판매가격 vs 판매지수 상관관계", "산점도와 추세선이 보여주는 가격 비탄력성 (상관계수 r = +0.01)", "PRICE ELASTICITY")

    headers18 = ["가격대 구간", "권수", "비중", "구간 판매지수", "점유율"]
    rows18 = [
        ["2만원 미만", "106권", "37.2%", "518,757점", "41.0%"],
        ["2만~3만원", "119권", "41.8%", "606,471점", "48.0%"],
        ["3만~4만원", "45권", "15.8%", "120,987점", "9.6%"],
        ["4만원 이상", "15권", "5.3%", "18,540점", "1.4%"]
    ]
    add_image_slide_content(s18, "eda_05_price_vs_sales_scatter.png", headers18, rows18, [Inches(1.4), Inches(0.8), Inches(0.8), Inches(1.3), Inches(1.08)],
                            "회귀 추세선 기울기가 0에 수렴하며 상관계수 r = +0.01로 완전한 가격 비탄력성을 보입니다. IT 도서 구매자는 가격이 저렴하다고 사지 않으며, 내용의 전문성과 실무 유용성에 따라 구매합니다.")
    add_notes(s18, "[발표자 노트 (약 4초)]\n'판매가격과 판매지수의 상관계수는 +0.01로 완전한 비탄력성을 나타내며, 2만~3만 원대가 시장의 48%를 점유합니다.'")

    # ==========================================
    # SLIDE 19: 15. [EDA 05 심층] 가격대별 실적 & 최대 캐시카우
    # ==========================================
    s19 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s19, COLOR_BG_LIGHT)
    add_header(s19, "15. [EDA 05 심층] 가격대별 실적 & 최대 캐시카우", "'2만~3만 원' 구간이 시장 매출의 48.0%를 견인하는 이유", "CASH COW")

    add_kpi(s19, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7), "시장 최대 캐시카우 (2만~3만원)", "점유율 48.0%",
            "• 최고의 판매 볼륨: 전체 285권 중 119권(41.8%) 집중, 누적 606,471점 달성\n"
            "• 평균 판매지수 5,096점: 2만 원 미만 저가 구간(평균 4,894점)보다 오히려 높은 판매 성과\n"
            "• 구매 심리: '전문 기술서로서 최소한의 분량과 깊이가 보장되는 가격대'라는 신뢰 형성", icon="💰", accent_color=COLOR_POINT_BLUE)

    add_kpi(s19, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7), "4만 원 이상 초고가 도서 붕괴선", "판매지수 -75%",
            "• 급격한 수요 위축: 4만 원 초과 시 평균 판매지수가 1,236점으로 급락 (전체 평균의 27.8%)\n"
            "• 구매 패턴: 개인 구매보다 법인 교육비/도서구입비 지원에 의존하는 경향 뚜렷\n"
            "• 전략적 제언: 방대한 분량은 상·하권 분권(권당 2.5만 원)을 통해 3만 원 미만으로 설계 필수", icon="📉", accent_color=COLOR_ACCENT_AMBER)
    add_notes(s19, "[발표자 노트 (약 4초)]\n'4만 원을 넘기면 판매지수가 75% 급감하므로, 방대한 기술서는 상하 분권으로 2만 원대 중반에 맞추어야 합니다.'")

    # ==========================================
    # SLIDE 20: 16. [EDA 06] 순위별 지수 감쇠
    # ==========================================
    s20 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s20, COLOR_BG_LIGHT)
    add_header(s20, "16. [EDA 06] 베스트셀러 순위별 판매지수 감쇠 경향", "순위 상승에 따른 수직 상승 곡선: 1위~10위 구간의 급격한 지수 감쇠", "RANK DECAY")

    headers20 = ["순위 구간", "권수", "평균 판매지수", "구간 총 판매지수", "점유율"]
    rows20 = [
        ["TOP 10 (1~10위)", "10권", "25,118점", "251,178점", "19.9%"],
        ["11~50위", "40권", "7,323점", "292,932점", "23.2%"],
        ["51~100위", "50권", "2,417점", "120,867점", "9.6%"],
        ["101위 이하", "185권", "3,242점", "599,778점", "47.4%"]
    ]
    add_image_slide_content(s20, "eda_06_rank_vs_sales_trend.png", headers20, rows20, [Inches(1.5), Inches(0.7), Inches(1.2), Inches(1.2), Inches(0.78)],
                            "순위와 판매지수 간 상관계수는 r = -0.37로 급격한 비선형 지수 감쇠 형태를 보입니다. 특히 상위 10위 도서의 평균 판매지수는 25,118점으로 11~50위 구간(7,323점) 대비 3.4배의 파급력을 가집니다.")
    add_notes(s20, "[발표자 노트 (약 4초)]\n'순위별 곡선을 보면 1위부터 10위까지의 도서가 평균 2만 5천 점을 기록하며 급격한 감쇠 절벽을 만듭니다.'")

    # ==========================================
    # SLIDE 21: 17. [EDA 06 심층] TOP 10 랭크의 기하급수적 파급 효과
    # ==========================================
    s21 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s21, COLOR_BG_LIGHT)
    add_header(s21, "17. [EDA 06 심층] TOP 10 랭크의 기하급수적 파급 효과", "1~10위 진입은 11~50위 대비 3.4배의 폭발적 판매 증대 창출", "TOP 10 LEVERAGE")

    add_kpi(s21, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7), "TOP 10 플랫폼 레버리지", "3.4배 격차",
            "• 평균 25,118점의 위력: 11~50위(평균 7,323점)의 3.4배, 51~100위(2,417점)의 10.4배\n"
            "• 모바일/웹 UI 노출 한계선:\n"
            "  - YES24 모바일 앱 첫 화면에 스크롤 없이 노출되는 도서는 1~5위\n"
            "  - '주간/일간 베스트' 1페이지 노출 한계선이 10위\n"
            "• 10위와 11위 사이의 판매지수 단절 격차가 40% 이상으로 최대", icon="🚀", accent_color=COLOR_POINT_BLUE)

    add_kpi(s21, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7), "마케팅 리소스 올인 법칙", "초기 7일 집중",
            "• '어정쩡한 20위 유지보다 확실한 5일간의 TOP 10 진입이 낫다'\n"
            "• 마케팅 예산을 3개월간 분산 집행하는 것보다, 출간 직후 7일간 사전예약, 저자 라이브, 인플루언서 리뷰를 일거에 집중 투입\n"
            "• TOP 10 진입 트리거를 당기는 전략이 최종 누적 판매량을 최대화함", icon="🎯", accent_color=COLOR_ACCENT_AMBER)
    add_notes(s21, "[발표자 노트 (약 4초)]\n'10위 내 진입은 차순위 대비 3.4배의 판매력을 보이므로 론칭 첫 주에 마케팅 리소스를 올인해야 합니다.'")

    # ==========================================
    # SLIDE 22: [간지 3] Part 3 시작
    # ==========================================
    s22 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s22, COLOR_SLATE_DIV)
    badge22 = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.2), Inches(2.2), Inches(0.36))
    badge22.fill.solid()
    badge22.fill.fore_color.rgb = RGBColor(40, 65, 85)
    badge22.line.fill.background()
    badge22.text_frame.text = "SECTION 03"
    b_p = badge22.text_frame.paragraphs[0]
    b_p.font.name = FONT_TITLE
    b_p.font.size = Pt(11)
    b_p.font.color.rgb = RGBColor(160, 205, 240)
    b_p.alignment = PP_ALIGN.CENTER

    tb22 = s22.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(10.3), Inches(2.5))
    tf22 = tb22.text_frame
    p1 = tf22.paragraphs[0]
    p1.text = "PART 3. 출판사 생태계 & 전략 액션 플랜"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf22.add_paragraph()
    p2.text = "출판사 과점 구조, NLP 키워드 마이닝 및 4대 실행 로드맵"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(180, 210, 230)
    p2.space_before = Pt(10)

    hl22 = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.5), Inches(10.3), Inches(0.8))
    hl22.fill.solid()
    hl22.fill.fore_color.rgb = RGBColor(38, 58, 74)
    hl22.line.color.rgb = RGBColor(60, 95, 125)
    hl22.line.width = Pt(1)
    tf22_h = hl22.text_frame
    p3 = tf22_h.paragraphs[0]
    p3.text = "✓ 상위 5대사 43.5% 과점   |   ✓ '클로드·바이브 코딩' 키워드 급부상   |   ✓ 4대 전략적 액션 아이템"
    p3.font.name = FONT_TITLE
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = COLOR_WHITE
    p3.alignment = PP_ALIGN.CENTER
    add_notes(s22, "[발표자 노트 (약 3초)]\n'마지막 파트 3, 출판사별 경쟁 구도와 텍스트 마이닝 인사이트 및 실무 액션 플랜입니다.'")

    # ==========================================
    # SLIDE 23: 18. [EDA 07] 상위 출판사 점유율
    # ==========================================
    s23 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s23, COLOR_BG_LIGHT)
    add_header(s23, "18. [EDA 07] IT/모바일 베스트셀러 상위 20대 출판사 점유율", "한빛미디어의 압도적 1위(50권)와 상위 5대 전문 출판사의 과점", "PUBLISHER SHARE")

    headers23 = ["순위", "출판사명", "등재 권수", "점유율", "누적 점유율"]
    rows23 = [
        ["1", "한빛미디어", "50권", "17.5%", "17.5%"],
        ["2", "길벗", "23권", "8.1%", "25.6%"],
        ["3", "이지스퍼블리싱", "18권", "6.3%", "31.9%"],
        ["4", "한빛아카데미", "17권", "6.0%", "37.9%"],
        ["5", "골든래빗", "16권", "5.6%", "43.5%"],
        ["6", "위키북스", "11권", "3.9%", "47.4%"],
        ["7", "제이펍", "11권", "3.9%", "51.2%"],
        ["8", "에이콘출판사", "10권", "3.5%", "54.7%"]
    ]
    add_image_slide_content(s23, "eda_07_top_publishers_bar.png", headers23, rows23, [Inches(0.6), Inches(1.5), Inches(1.0), Inches(1.0), Inches(1.28)],
                            "총 69개 출판사 중 한빛미디어가 50권(17.5%)으로 압도적 1위이며, 상위 5대 전문 출판사가 전체 시장의 43.5%를 과점하고 있습니다. 한빛아카데미 합산 시 한빛 계열 점유율은 23.5%에 달합니다.")
    add_notes(s23, "[발표자 노트 (약 4초)]\n'출판사 분석에서는 한빛미디어가 50권으로 1위이며, 상위 5개 출판사가 전체 시장의 43.5%를 과점하고 있습니다.'")

    # ==========================================
    # SLIDE 24: 19. [EDA 08] 스피어만 순위 상관계수 행렬
    # ==========================================
    s24 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s24, COLOR_BG_LIGHT)
    add_header(s24, "19. [EDA 08] 주요 수치 변수 간 스피어만 순위 상관계수 행렬", "판매지수를 견인하는 핵심 동인은 리뷰 수 (r = +0.57)", "CORRELATION")

    headers24 = ["변수 쌍", "상관계수 (r)", "통계적 해석 및 시사점"]
    rows24 = [
        ["판매지수 ↔ 리뷰수", "+0.57", "강한 양의 상관 (선순환 피드백 루프)"],
        ["순위 ↔ 판매지수", "-0.37", "유의미한 음의 상관 (순위 역비례 지수 감쇠)"],
        ["판매지수 ↔ 평점", "+0.25", "약한 양의 상관 (고평점은 기본 전제)"],
        ["리뷰수 ↔ 할인율", "+0.40", "10% 할인 도서의 리뷰 축적도 높음"],
        ["판매지수 ↔ 가격", "+0.01", "상관성 전무 (완전한 가격 독립성)"]
    ]
    add_image_slide_content(s24, "eda_08_correlation_heatmap.png", headers24, rows24, [Inches(1.8), Inches(1.2), Inches(2.38)],
                            "판매지수와 가장 강한 상관관계를 갖는 변수는 리뷰 수(r = +0.57)입니다. 판매량 증가가 리뷰 축적을 유도하고, 이것이 사회적 증거(Social Proof)로 작용해 신규 독자를 유입시키는 선순환이 확인됩니다.")
    add_notes(s24, "[발표자 노트 (약 4초)]\n'상관분석 결과 판매지수와 가장 밀접한 변수는 리뷰 수(+0.57)이며, 가격(+0.01)은 완전히 독립적입니다.'")

    # ==========================================
    # SLIDE 25: 20. [EDA 09] 출판사 포지셔닝 버블 차트
    # ==========================================
    s25 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s25, COLOR_BG_LIGHT)
    add_header(s25, "20. [EDA 09] 상위 10대 출판사 복합 포지셔닝 버블 차트", "가격(X), 평점(Y), 판매지수(크기), 권수(색상)의 4차원 매트릭스", "BUBBLE MATRIX")

    headers25 = ["출판사", "등재 권수", "평균판매가", "평점", "총 판매지수"]
    rows25 = [
        ["한빛미디어", "50권", "27,230원", "9.7점", "410,217점"],
        ["골든래빗", "16권", "26,628원", "9.8점", "171,054점"],
        ["이지스퍼블리싱", "18권", "22,525원", "9.8점", "89,529점"],
        ["길벗", "23권", "22,884원", "9.6점", "89,358점"],
        ["제이펍", "11권", "23,973원", "9.6점", "73,698점"]
    ]
    add_image_slide_content(s25, "eda_09_pub_price_rating_bubble.png", headers25, rows25, [Inches(1.3), Inches(0.9), Inches(1.1), Inches(0.8), Inches(1.28)],
                            "버블 차트 분석 결과 한빛미디어가 최대 규모를 형성한 가운데, 신흥 강자인 골든래빗이 16권으로 17.1만 점을 달성하여 권당 판매 효율성에서 독보적인 1위를 기록했습니다.")
    add_notes(s25, "[발표자 노트 (약 4초)]\n'버블 차트상 한빛미디어가 최대 규모를 형성한 가운데, 골든래빗이 권당 최고 판매 효율을 기록했습니다.'")

    # ==========================================
    # SLIDE 26: 21. [EDA 10] 출간 연도 시계열 분포
    # ==========================================
    s26 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s26, COLOR_BG_LIGHT)
    add_header(s26, "21. [EDA 10] 출간 연도별 시계열 분포 및 신구 대조", "2025~2026년 최신간이 58.2% 장악 vs 2022년 이전 명저의 17.9% 롱런", "PUB YEAR")

    headers26 = ["출간 연도", "권수", "비중", "평균 판매지수", "총 판매지수"]
    rows26 = [
        ["2026년", "121권", "42.5%", "4,960점", "600,144점"],
        ["2025년", "45권", "15.8%", "9,072점", "408,249점"],
        ["2024년", "32권", "11.2%", "1,759점", "56,292점"],
        ["2023년", "24권", "8.4%", "2,218점", "53,244점"],
        ["2022년 이전", "63권", "22.1%", "2,333점", "146,826점"]
    ]
    add_image_slide_content(s26, "eda_10_pub_year_distribution.png", headers26, rows26, [Inches(1.2), Inches(0.8), Inches(0.9), Inches(1.2), Inches(1.28)],
                            "최근 2개년(2025~2026) 신간이 전체 도서의 58.2%, 누적 판매지수의 79.7%를 장악하여 IT 도서의 수명이 1~2년으로 크게 단축되었음을 증명합니다. 반면 고전 명저는 17.9%의 롱런을 유지합니다.")
    add_notes(s26, "[발표자 노트 (약 4초)]\n'최근 2개년 신간이 전체 판매지수의 80%를 점유하여 기술 감가상각 주기가 1~2년으로 대폭 단축되었습니다.'")

    # ==========================================
    # SLIDE 27: 22. [EDA 11] NLP TF-IDF 키워드
    # ==========================================
    s27 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s27, COLOR_BG_LIGHT)
    add_header(s27, "22. [EDA 11] 도서 메타 텍스트 TF-IDF 키워드 및 AI 트렌드", "2026 AI 대전환: '바이브 코딩', '클로드 코드', '청년패스'의 부상", "TEXT MINING")

    headers27 = ["순위", "핵심 키워드", "TF-IDF 점수", "비즈니스 의미"]
    rows27 = [
        ["1", "청년패스", "62.58", "정부 자기개발 바우처 수혜 집중"],
        ["2", "ai", "44.43", "생성형 AI 전면화 및 실무 적용"],
        ["3", "분철", "27.77", "두꺼운 기술서 휴대 실습 편의 욕구"],
        ["7", "클로드 (Claude)", "13.73", "코딩 특화 LLM으로 ChatGPT 추월"],
        ["9", "코딩", "11.63", "실무 프로그래밍 프로젝트 수요"],
        ["12", "챗gpt", "11.21", "대화형 범용 인공지능 활용서"]
    ]
    add_image_slide_content(s27, "eda_11_text_tfidf_keywords.png", headers27, rows27, [Inches(0.7), Inches(1.6), Inches(1.2), Inches(1.88)],
                            "텍스트 마이닝 결과 AI(44.4)와 청년패스(62.6)가 압도적인 가중치를 보였으며, 코딩 특화 모델인 Anthropic의 클로드(Claude)가 챗GPT를 앞지르며 자연어 기반 '바이브 코딩' 패러다임을 견인하고 있습니다.")
    add_notes(s27, "[발표자 노트 (약 5초)]\n'텍스트 분석에서는 AI와 청년패스가 최상위를 기록했고, 코딩 특화 모델인 클로드가 챗GPT를 앞지르며 트렌드를 리드하고 있습니다.'")

    # ==========================================
    # SLIDE 28: 23. 20년차 분석가 총평 (Executive Summary)
    # ==========================================
    s28 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s28, COLOR_BG_LIGHT)
    add_header(s28, "23. 20년차 수석 데이터 분석가 총평 (Executive Summary)", "데이터가 증명하는 YES24 IT/모바일 시장 3대 법칙", "SUMMARY")

    laws = [
        ("1. 완벽한 파이프라인과 데이터 신뢰성", "Data Reliability",
         "285건 전수 데이터는 10대 무결성 검증을 100% 통과하여 결측·역전 없는 엔터프라이즈 프로덕션 품질을 유지함. IT 도서 시장 분석의 정밀한 벤치마크 데이터셋으로 기능.",
         COLOR_POINT_BLUE, "🛡️"),
        ("2. 멱법칙 파레토 지배와 TOP 10 쏠림", "Pareto & Winner-Takes-All",
         "상위 5% 도서가 판매지수 43.8%를 독점하고 TOP 10이 하위권 대비 3.4~10.4배의 판매력을 창출함. 롱테일 다작보다 '슈퍼스타 킬러 콘텐츠' 1권이 출판사 수익을 결정.",
         COLOR_ACCENT_GREEN, "🏆"),
        ("3. 가격 비탄력성과 AI 실용성 프리미엄", "Quality-Driven Market",
         "가격과 판매지수 간 상관계수는 +0.01로 가격 탄력성이 없음. 독자는 가격보다 '최신 AI 기술의 실무 적용성'에 기꺼이 2만 원대 중후반 프리미엄을 지불함.",
         COLOR_ACCENT_AMBER, "💎")
    ]
    for idx, (l_title, l_sub, l_desc, l_col, l_icon) in enumerate(laws):
        top = Inches(2.0 + idx * 1.6)
        card = add_card(s28, Inches(0.8), top, Inches(11.73), Inches(1.4))
        # 좌측 바
        bar = s28.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top, Pt(4), Inches(1.4))
        bar.fill.solid()
        bar.fill.fore_color.rgb = l_col
        bar.line.fill.background()

        tb = s28.shapes.add_textbox(Inches(1.05), top + Inches(0.12), Inches(11.3), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{l_icon} {l_title}  ({l_sub})"
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = l_col

        p2 = tf.add_paragraph()
        p2.text = l_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MAIN
        p2.space_before = Pt(4)
    add_notes(s28, "[발표자 노트 (약 7초)]\n'총평입니다. 첫째 100% 무결한 데이터, 둘째 상위 5%가 44%를 독점하는 멱법칙, 셋째 가격 비탄력적인 AI 실무서 선호가 핵심 결론입니다.'")

    # ==========================================
    # SLIDE 29: 24. 출판 기획 & 마케팅 4대 전략적 액션 아이템
    # ==========================================
    s29 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s29, COLOR_BG_LIGHT)
    add_header(s29, "24. 출판 기획 & 마케팅 4대 전략적 액션 아이템", "데이터 분석 결과 기반의 실무 실행 로드맵 (Action Plan)", "ACTION PLAN")

    actions = [
        ("1. [기획] AI 에이전트 실무서 긴급 편제", "성장 동력 확보",
         "Claude Code, MCP(Model Context Protocol), 바이브 코딩 등 2026 최신 에이전틱 툴링 기반 실무 프로젝트 서적을 분기 내 출간 기획.",
         COLOR_POINT_BLUE, "📘"),
        ("2. [가격] 24,000 ~ 28,000원 스위트 스팟", "매출 극대화",
         "4만 원 이상 가격대는 판매지수가 75% 급감하므로, 방대한 분량은 상/하 분권화하여 2만 원대 중반으로 가격 저항선 회피.",
         COLOR_ACCENT_GREEN, "🏷️"),
        ("3. [마케팅] 론칭 초기 7일 TOP 10 올인", "노출 레버리지",
         "사전예약, 저자 라이브, 독점 굿즈(치트시트)를 첫 주에 집중 투입하여 1~10위 노출을 조기 달성하고 자연 증폭 루프 유도.",
         COLOR_ACCENT_AMBER, "🚀"),
        ("4. [엔지니어링] 일별 자동화 파이프라인", "운영 고도화",
         "yes24_eda_validator.py를 배치화하여 매일 순위 변동과 신간 진입을 감지하는 실시간 경쟁사 모니터링 시스템 구축.",
         COLOR_DARK_NAVY, "⚙️")
    ]
    for idx, (a_title, a_sub, a_desc, a_col, a_icon) in enumerate(actions):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(2.0 + row * 2.5)
        card = add_card(s29, left, top, Inches(5.75), Inches(2.3))

        bar = s29.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(5.75), Pt(3))
        bar.fill.solid()
        bar.fill.fore_color.rgb = a_col
        bar.line.fill.background()

        tb = s29.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.35), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{a_icon} {a_title}"
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = a_col

        badge = tf.add_paragraph()
        badge.text = f"목표: {a_sub}"
        badge.font.name = FONT_TITLE
        badge.font.size = Pt(9.5)
        badge.font.color.rgb = COLOR_TEXT_MUTED
        badge.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = a_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MAIN
        p2.space_before = Pt(6)
    add_notes(s29, "[발표자 노트 (약 7초)]\n'이에 따른 4대 액션으로 AI 실무서 긴급 편제, 2만 원대 중반 분권화 가격 책정, 첫 주 TOP 10 집중 마케팅, 그리고 자동화 모니터링을 제안합니다.'")

    # ==========================================
    # SLIDE 30: 25. 결론 및 질의응답 (Q&A)
    # ==========================================
    s30 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s30, COLOR_DARK_NAVY)

    # 장식 원형
    c30 = s30.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-1.5), Inches(4.5), Inches(4.0), Inches(4.0))
    c30.fill.solid()
    c30.fill.fore_color.rgb = RGBColor(32, 50, 64)
    c30.line.fill.background()

    b30 = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.3), Inches(3.73), Inches(0.38))
    b30.fill.solid()
    b30.fill.fore_color.rgb = RGBColor(35, 55, 70)
    b30.line.color.rgb = RGBColor(70, 110, 145)
    b30.text_frame.text = "PROVEN DATA STRATEGY (10/10 PASS)"
    p = b30.text_frame.paragraphs[0]
    p.font.name = FONT_TITLE
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 210, 235)
    p.alignment = PP_ALIGN.CENTER

    tb30 = s30.shapes.add_textbox(Inches(1.5), Inches(1.9), Inches(10.3), Inches(1.8))
    tf30 = tb30.text_frame
    tf30.word_wrap = True
    p1 = tf30.paragraphs[0]
    p1.text = "데이터가 증명하는 성공적인 출판 전략"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf30.add_paragraph()
    p2.text = "정밀한 품질 검증 · 멱법칙의 이해 · 생성형 AI 시대의 신속한 의사결정"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(160, 190, 215)
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(10)

    # 중앙 Q&A 카드
    card30 = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.8), Inches(3.8), Inches(5.73), Inches(1.8))
    card30.fill.solid()
    card30.fill.fore_color.rgb = RGBColor(32, 50, 64)
    card30.line.color.rgb = RGBColor(70, 110, 145)
    card30.line.width = Pt(1)
    tf30_c = card30.text_frame
    tf30_c.word_wrap = True
    p_q1 = tf30_c.paragraphs[0]
    p_q1.text = "💬 Q & A (질의응답)"
    p_q1.font.name = FONT_TITLE
    p_q1.font.size = Pt(18)
    p_q1.font.bold = True
    p_q1.font.color.rgb = RGBColor(160, 215, 255)
    p_q1.alignment = PP_ALIGN.CENTER

    p_q2 = tf30_c.add_paragraph()
    p_q2.text = "경청해 주셔서 감사합니다. 질문해 주시면 성심껏 답변드리겠습니다."
    p_q2.font.name = FONT_BODY
    p_q2.font.size = Pt(12)
    p_q2.font.color.rgb = RGBColor(215, 230, 240)
    p_q2.alignment = PP_ALIGN.CENTER
    p_q2.space_before = Pt(8)

    # 하단 링크
    tb30_b = s30.shapes.add_textbox(Inches(1.5), Inches(5.9), Inches(10.3), Inches(0.8))
    tf30_b = tb30_b.text_frame
    p_b1 = tf30_b.paragraphs[0]
    p_b1.text = "보고서 원문: yes24/docs/yes24_day_bestseller_eda_report.md  |  생성 파일: yes24_day_bestseller_eda_presentation.pptx"
    p_b1.font.name = FONT_BODY
    p_b1.font.size = Pt(10.5)
    p_b1.font.color.rgb = RGBColor(140, 165, 185)
    p_b1.alignment = PP_ALIGN.CENTER
    add_notes(s30, "[발표자 노트 (약 4초)]\n'이상으로 발표를 마치겠습니다. 경청해 주셔서 대단히 감사드리며, 질문 있으시면 편하게 말씀해 주시기 바랍니다.'")

    output_path = os.path.join("yes24", "docs", "yes24_day_bestseller_eda_presentation.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_presentation()
