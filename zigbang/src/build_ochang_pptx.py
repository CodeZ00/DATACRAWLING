# -*- coding: utf-8 -*-
"""
충북 청주시 청원구 오창읍 원룸·빌라 월세 심층 분석 프레젠테이션 (.pptx) 자동 생성기
- 1인 가구 주거 인텔리전스 및 양청택지로 124-32(은하빌라B) 정밀 감정평가 슬라이드 수록
- 16:9 와이드스크린 규격 (13.333 x 7.5 인치)
- Bento Grid 모던 디자인 시스템 및 직방 브랜드 테마
- 15장 슬라이드 전수에 11종 고해상도 차트 및 200자 이상 발표자 노트(Speaker Notes) 완비
- 출력 파일: zigbang/reports/Ochang_Villa_Rent_Presentation.pptx
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PPTX = REPORTS_DIR / "Ochang_Villa_Rent_Presentation.pptx"

# 컬러 팔레트 (다크 테마 & 앰버/블루 하이라이트)
BG_DARK = RGBColor(15, 23, 42)          # 다크 슬레이트 (#0F172A)
CARD_DARK = RGBColor(30, 41, 59)        # 카드 다크 슬레이트 (#1E293B)
BORDER_DARK = RGBColor(51, 65, 85)      # 테두리 (#334155)

PRIMARY_BLUE = RGBColor(59, 130, 246)   # 로얄 블루 (#3B82F6)
PRIMARY_AMBER = RGBColor(245, 158, 11)  # 직방 앰버 골드 (#F59E0B)
ACCENT_ORANGE = RGBColor(234, 88, 12)   # 웜 오렌지 (#EA580C)
ACCENT_ROSE = RGBColor(244, 63, 94)     # 로즈 레드 (#F43F5E)
ACCENT_TEAL = RGBColor(20, 184, 166)    # 에메랄드 틸 (#14B8A6)

TEXT_LIGHT = RGBColor(248, 250, 252)    # 밝은 본문 (#F8FAFC)
TEXT_MUTED = RGBColor(148, 163, 184)    # 밝은 뮤트 (#94A3B8)
TEXT_DARK = RGBColor(15, 23, 42)

FONT_HEADING = "Malgun Gothic"
FONT_BODY = "Malgun Gothic"


def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rounded_card(slide, left, top, width, height, fill_color, border_color=None, border_width=1):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape


def add_header(slide, tag_text, title_text, subtitle_text):
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.2), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CARD_DARK
    badge.line.color.rgb = BORDER_DARK
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    r_b = p_b.add_run()
    r_b.text = f"• {tag_text}"
    r_b.font.name = FONT_HEADING
    r_b.font.size = Pt(9.5)
    r_b.font.bold = True
    r_b.font.color.rgb = PRIMARY_AMBER

    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title_text
    r_t.font.name = FONT_HEADING
    r_t.font.size = Pt(20)
    r_t.font.bold = True
    r_t.font.color.rgb = TEXT_LIGHT

    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.5), Inches(0.35))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    r_s = p_s.add_run()
    r_s.text = subtitle_text
    r_s.font.name = FONT_BODY
    r_s.font.size = Pt(11)
    r_s.font.color.rgb = TEXT_MUTED


def set_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text


def build_pptx():
    print("[*] 16:9 와이드 PPTX 슬라이드 생성 시작 (15장 전수 빌드)...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # Slide 1: 표지
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_DARK)
    add_rounded_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), CARD_DARK, BORDER_DARK, 1)

    t_box = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(3.0))
    tf = t_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "ZIGBANG REAL ESTATE BIG DATA INTELLIGENCE"
    r0.font.name = FONT_HEADING
    r0.font.size = Pt(12)
    r0.font.bold = True
    r0.font.color.rgb = PRIMARY_AMBER

    p1 = tf.add_paragraph()
    p1.space_before = Pt(14)
    r1 = p1.add_run()
    r1.text = "오창읍 원룸·빌라 월세 시장 데이터 분석 리포트"
    r1.font.name = FONT_HEADING
    r1.font.size = Pt(28)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.space_before = Pt(8)
    r2 = p2.add_run()
    r2.text = "오창산단 배후 603개 매물 전수 분석, 청년 1인 가구 가이드 및 양청택지로 124-32 감정평가"
    r2.font.name = FONT_BODY
    r2.font.size = Pt(14)
    r2.font.color.rgb = TEXT_MUTED

    p3 = tf.add_paragraph()
    p3.space_before = Pt(28)
    r3 = p3.add_run()
    r3.text = "발행일자: 2026년 10월 29일 | 수집 출처: 직방(Zigbang) 공식 Gateway API 전수 수집"
    r3.font.name = FONT_BODY
    r3.font.size = Pt(10)
    r3.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s1,
        "안녕하십니까. 오늘 발표드릴 내용은 충북 청주시 청원구 오창읍 일대의 원룸 및 빌라 월세 시장을 심층 분석한 데이터 인텔리전스 리포트입니다. "
        "오창읍은 이차전지와 반도체 소부장 특화단지, 방사광가속기 유치로 청년 연구원과 엔지니어의 유입이 매우 활발한 첨단 산업의 핵심 거점입니다. "
        "본 보고서는 직방 게이트웨이 API를 통해 오창읍 전역의 실매물 603건을 전수 수집하여 결측률 0%로 검증된 데이터를 바탕으로, "
        "가격 형성 원리와 관리비 착시 현상, 청년 1인 가구 특화 분석, 그리고 양청택지로 124-32 은하빌라B에 대한 정밀 입지 감정평가를 수학적으로 규명하였습니다."
    )

    # ==========================================
    # Slide 2: Executive Summary
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, BG_DARK)
    add_header(s2, "EXECUTIVE SUMMARY", "경영 요약: 오창읍 월세 시장의 3대 핵심 구조적 특성", "603건 전수 조사로 규명된 가격 앵커링, 관리비 전가 및 투룸의 가성비 역전")

    cards_s2 = [
        ("01", "가격 앵커링 & 저보증금 구조", "월세 36만 / 보증금 300만 집중", 
         "오창읍 월세의 중위수는 36.0만 원(평균 40.8만), 보증금 중위수는 300만 원으로 전체의 61.2%가 300만 원 이하 저보증금에 포진하여 1인 가구 진입 장벽이 매우 낮습니다.", PRIMARY_AMBER),
        ("02", "관리비 착시와 실질 주거비", "평균 관리비 10.4만 원 전가", 
         "임대인들이 표면 월세 저항선을 회피하기 위해 관리비 항목으로 주거비를 전가하여, 실질 총 주거비용 중위수는 46.0만 원, 평균은 51.2만 원에 달합니다.", ACCENT_ROSE),
        ("03", "투룸의 평당 가성비 역전", "투룸 4.0만 vs 원룸 5.4만/평", 
         "단독 원룸(72%)이 시장을 과점하고 있으나, 평당 실질비용은 투룸(4.0만 원/평)이 원룸(5.4만 원/평) 대비 25.9% 저렴하여 규모의 경제가 발생합니다.", PRIMARY_BLUE)
    ]

    for idx, (num, title, sub, body, color) in enumerate(cards_s2):
        left = Inches(0.8 + idx * 3.95)
        add_rounded_card(s2, left, Inches(1.8), Inches(3.75), Inches(5.0), CARD_DARK, BORDER_DARK, 1)

        tbox = s2.shapes.add_textbox(left + Inches(0.25), Inches(2.0), Inches(3.25), Inches(4.5))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        r_num = p_num.add_run()
        r_num.text = num
        r_num.font.name = FONT_HEADING
        r_num.font.size = Pt(24)
        r_num.font.bold = True
        r_num.font.color.rgb = color

        p_t = tf.add_paragraph()
        p_t.space_before = Pt(8)
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = FONT_HEADING
        r_t.font.size = Pt(14)
        r_t.font.bold = True
        r_t.font.color.rgb = TEXT_LIGHT

        p_sub = tf.add_paragraph()
        p_sub.space_before = Pt(4)
        r_sub = p_sub.add_run()
        r_sub.text = sub
        r_sub.font.name = FONT_BODY
        r_sub.font.size = Pt(11)
        r_sub.font.bold = True
        r_sub.font.color.rgb = color

        p_b = tf.add_paragraph()
        p_b.space_before = Pt(12)
        r_b = p_b.add_run()
        r_b.text = body
        r_b.font.name = FONT_BODY
        r_b.font.size = Pt(10)
        r_b.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s2,
        "오창읍 월세 시장의 3대 핵심 발견점을 요약해 드리겠습니다. 첫째, 오창읍은 보증금 300만 원, 월세 36만 원 선에 60% 이상의 매물이 집중되는 전형적인 가성비 앵커링 구조를 보입니다. "
        "둘째, 표면 월세 뒤에 숨겨진 평균 10.4만 원의 관리비로 인해 실질 월 주거비는 46만 원에서 51만 원 수준에 형성됩니다. "
        "셋째, 원룸이 72%를 차지하고 있으나 평당 단가 기준으로는 투룸이 약 26% 저렴하여, 넓은 공간을 원하는 임차인에게 투룸이 매우 매력적인 대안임을 밝혀냈습니다."
    )

    # ==========================================
    # Slide 3: [특집 1] 청년 1인 가구 정밀 주거 분석
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, BG_DARK)
    add_header(s3, "FOCUS 01", "[특집 1] 청년 1인 가구를 위한 정밀 주거 인텔리전스", "소득 대비 주거비 부담률(RIR) 13~16%, 최적 룸타입 매트릭스 및 풀옵션 경제성")

    cards_s3 = [
        ("소득 대비 RIR 분석", "월 소득의 13~16% 건강한 지출 구조", [
            "• 산단 초임 세후 소득: 약 280만~350만 원",
            "• 실질 주거비 중위수: 46.0만 원",
            "• RIR 13.1%~16.4%: 수도권(30%대) 대비 절반 수준으로 초기 자산 모으기에 최적"
        ], PRIMARY_BLUE),
        ("1인 가구 룸타입 매트릭스", "가성비 순위: 투룸 > 1.5룸 > 원룸", [
            "• 투룸 (16.1평): 평당 4.0만 원 (최고 공간 효율)",
            "• 1.5룸 (7.8평): 실질 월 42.3만 원 (최저 지출형)",
            "• 단독 원룸 (9.5평): 평당 5.4만 원 (기본 숙식형)",
            "• 투룸 임차 시 서재/침실 분리로 거주 만족도 극대화"
        ], PRIMARY_AMBER),
        ("풀옵션 7대 스펙 경제성", "가전 구매비 250만 원 이상 절감", [
            "• 필수 7종: 에어컨, 세탁기, 냉장고, 인덕션, 전자레인지, 도어락, 붙박이장",
            "• 풀옵션 매물(42.3만) vs 일반(40.4만) 차이는 월 1.9만 원에 불과",
            "• 가전 구입 대비 2년 거주 기준 최소 150만 원 순이득"
        ], ACCENT_TEAL)
    ]

    for idx, (title, sub, bullets, color) in enumerate(cards_s3):
        left = Inches(0.8 + idx * 3.95)
        add_rounded_card(s3, left, Inches(1.8), Inches(3.75), Inches(5.0), CARD_DARK, BORDER_DARK, 1)

        tbox = s3.shapes.add_textbox(left + Inches(0.25), Inches(2.0), Inches(3.25), Inches(4.5))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = FONT_HEADING
        r_t.font.size = Pt(14)
        r_t.font.bold = True
        r_t.font.color.rgb = color

        p_sub = tf.add_paragraph()
        p_sub.space_before = Pt(4)
        r_sub = p_sub.add_run()
        r_sub.text = sub
        r_sub.font.name = FONT_BODY
        r_sub.font.size = Pt(11)
        r_sub.font.bold = True
        r_sub.font.color.rgb = TEXT_LIGHT

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(8)
            r_b = p_b.add_run()
            r_b.text = b
            r_b.font.name = FONT_BODY
            r_b.font.size = Pt(9.5)
            r_b.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s3,
        "오창읍 입주자의 대다수를 차지하는 청년 1인 가구 분석입니다. 오창 산단 초임 엔지니어의 소득 대비 실질 주거비 부담률은 13~16%로, "
        "수도권 1인 가구(30% 안팎)와 비교하면 주거비 부담이 절반에 불과하여 자산 형성에 매우 유리합니다. "
        "룸타입은 평당 4.0만 원인 투룸이 가장 우수한 가성비를 보이며, 풀옵션 가구는 개별 가전 구매 대비 최소 150만 원 이상의 실질 절감 효과를 제공합니다."
    )

    # ==========================================
    # Slide 4: [특집 2] 양청택지로 124-32 정밀 감정평가
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, BG_DARK)
    add_header(s4, "FOCUS 02", "[특집 2] 특정 번지 정밀 감정평가: 양청택지로 124-32 (은하빌라B)", "오창호수공원 남측 중심상권 도보 5분 주거-상업 완충지 및 시세 감정 결과")

    cards_s4 = [
        ("물건지 개요 & 입지 환경", "도보 상권과 주거 쾌적성의 황금 밸런스", [
            "• 소재지: 청원구 오창읍 양청택지로 124-32 (양청리 731-4)",
            "• 건물명: 은하빌라B (다가구/다세대 주택)",
            "• 호수공원 남측 도보 5~7분, 메가박스/중심상가 도보 3분",
            "• 상가 소음을 한 블록 비껴서 조용하면서도 인프라 향유 최적"
        ], PRIMARY_AMBER),
        ("반경 300m 주변 시세 벤치마크", "평당 3.8만 원의 강력한 공간 가성비", [
            "• 반경 300m 평균 보증금: 300만 원 (안정적)",
            "• 반경 300m 평균 순수월세: 50.0만 원 (14.5평 기준)",
            "• 평당 실질 주거비: 3.8만 원/평",
            "• 오창읍 전체 평균(5.2만 원) 대비 약 27% 우수한 가성비"
        ], ACCENT_ROSE),
        ("적정 임대료 감정가 & 체크포인트", "실거주자를 위한 현장 가이드", [
            "• 원룸 적정 임대료: 보증금 200~300만 / 월세 30~35만",
            "• 투룸 적정 임대료: 보증금 300~500만 / 월세 45~52만",
            "• 빌라 특성상 승강기 부재 가능성 (2~3층 로열층 선호)",
            "• 관리비 포함 항목(수도/인터넷) 및 주차 공간 사전 확인"
        ], PRIMARY_BLUE)
    ]

    for idx, (title, sub, bullets, color) in enumerate(cards_s4):
        left = Inches(0.8 + idx * 3.95)
        add_rounded_card(s4, left, Inches(1.8), Inches(3.75), Inches(5.0), CARD_DARK, BORDER_DARK, 1)

        tbox = s4.shapes.add_textbox(left + Inches(0.25), Inches(2.0), Inches(3.25), Inches(4.5))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = FONT_HEADING
        r_t.font.size = Pt(14)
        r_t.font.bold = True
        r_t.font.color.rgb = color

        p_sub = tf.add_paragraph()
        p_sub.space_before = Pt(4)
        r_sub = p_sub.add_run()
        r_sub.text = sub
        r_sub.font.name = FONT_BODY
        r_sub.font.size = Pt(11)
        r_sub.font.bold = True
        r_sub.font.color.rgb = TEXT_LIGHT

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(8)
            r_b = p_b.add_run()
            r_b.text = b
            r_b.font.name = FONT_BODY
            r_b.font.size = Pt(9.5)
            r_b.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s4,
        "특정 번지인 양청택지로 124-32, 은하빌라B에 대한 정밀 감정평가 결과입니다. 본 물건지는 오창호수공원과 중심상업지구에 도보 3~5분 내에 접근 가능한 핵심 주거지입니다. "
        "반경 300m 이내 실거래 시세를 분석한 결과 평당 실질 주거비는 3.8만 원으로 오창읍 평균(5.2만 원) 대비 27% 우수한 가성비를 보유하고 있습니다. "
        "원룸 기준 보증금 300에 월 30~35만 원, 투룸 기준 보증금 500에 월 45~50만 원이 가장 적정한 시세로 평가됩니다."
    )

    # 차트 슬라이드 목록 (Slide 5 ~ 15)
    chart_slides = [
        ("chart01_monthly_rent_dist.png", "CHART 01", "월세 및 실질 총 주거비용 분포 (히스토그램 & KDE)", 
         "순수 월세와 실질 비용의 분포 차이 및 관리비 전가 현상",
         ["• 순수 월세 중위수: 36.0만 원 (평균 40.8만 원, 최빈 구간 30~35만 원)",
          "• 실질 총 주거비용 중위수: 46.0만 원 (평균 51.2만 원, 최빈 구간 40~45만 원)",
          "• 관리비 약 10만 원이 가산되며 확률밀도곡선(KDE) 전체가 우측으로 평행 이동",
          "• 80만 원 이상의 고액 월세는 오창 2산단 및 신축 쓰리룸 매물로 상위 3% 미만"]),
        
        ("chart02_structure_composition.png", "CHART 02", "방 구조 유형별 매물 점유 비율", 
         "단독 원룸 72% 과점 구조와 1.5룸/투룸 공급 불균형",
         ["• 단독 원룸: 434건 (72.0%) - 단위 면적당 수익률 극대화 산물",
          "• 투룸 (빌라/다가구): 94건 (15.6%) - 평균 면적 16.1평의 쾌적 공간",
          "• 1.5룸 / 분리형: 48건 (8.0%) - 실속형 1인 가구 타깃",
          "• 쓰리룸+: 19건 (3.2%) - 2인 이상 가구 및 임원급 숙소용"]),
        
        ("chart03_subdong_rent_boxplot.png", "CHART 03", "세부 권역(리)별 월세 분포 및 이상치 비교", 
         "양청리(중심상업) vs 구룡리(구시가지) vs 주성리(2산단 신흥)",
         ["• 양청리 (221건, 36.7%): 평균 37.0만 / 중위 31.0만 (호수공원 인접 핵심 선호지)",
          "• 구룡리 (91건, 15.1%): 평균 33.1만 / 중위 30.0만 (오창 내 최저가 가성비 원룸촌)",
          "• 주성리 (13건): 평균 51.5만 / 중위 58.0만 (2산단 신축 다가구 밀집 최고가 형성)",
          "• 오창읍 기타 (272건): 각리 및 외곽 산단 배후 주거벨트 (평균 45.8만)"]),
        
        ("chart04_rent_vs_size_scatter.png", "CHART 04", "전용면적(평) 대비 실질 총주거비 산점도 및 추세선", 
         "공간 면적 증가에 따른 실질 주거비의 체감 증가율",
         ["• 면적과 총주거비는 뚜렷한 양의 선형 관계 (피어슨 r = +0.63)",
          "• 7~10평 표준 원룸: 평균 실질비용 월 46.8만 원 (평당 5.4만 원)",
          "• 15평 이상 중대형: 평균 실질비용 월 74.6만 원 (평당 3.9만 원)",
          "• 빨간 점선은 선형 추세선, 분홍색 면적은 95% 신뢰구간을 의미"]),
        
        ("chart05_deposit_rent_tradeoff.png", "CHART 05", "보증금 구간별 평균 월세 수준 및 매물 분포", 
         "300만 원 이하 저보증금 구조와 고액 보증금의 신축 편중",
         ["• 보증금 200만 이하(204건) 및 201~300만(165건)이 전체의 61.2% 차지",
          "• 보증금 300만 이하 구간의 평균 월세는 34~36만 원 선으로 매우 안정적",
          "• 1,000만 원 초과 고보증금 구간은 평균 월세 68.4만 원으로 동반 상승",
          "• 금융 전환이 아닌 주택 평형과 연식 차이가 보증금과 월세를 동시 견인"]),
        
        ("chart06_cost_per_pyeong_rank.png", "CHART 06", "방 구조 유형별 평당 실질 주거비용 (가성비 지수)", 
         "복층형(3.9만) 및 투룸(4.0만)의 압도적 공간 가성비 우위",
         ["• 1위 (최고 효율): 복층형 원룸 - 평당 3.9만 원 (공간 활용 극대화)",
          "• 2위: 투룸 - 평당 4.0만 원 (16.1평의 넓은 공간을 월 64만 원에 향유)",
          "• 4위: 단독 원룸 - 평당 5.4만 원 (소형화 시공비용으로 단가 상승)",
          "• 5위: 1.5룸/분리형 - 평당 5.5만 원 (분리벽 시공에 따른 평당 프리미엄)"]),
        
        ("chart07_floor_level_analysis.png", "CHART 07", "층수 카테고리별 평균 월세 및 전용면적 비교", 
         "저층(1층)의 할인 효과(월 6.3만 원)와 중·고층 선호도",
         ["• 중층 (2~4층, 370건): 평균 월세 42.0만 원 (시장 주력 선호층)",
          "• 저층 (1층, 80건): 평균 월세 35.7만 원 (중층 대비 월 6.3만 원 저렴)",
          "• 1층 매물은 연간 약 75만 원의 실질 주거비 절감 혜택 제공",
          "• 고층 (5층 이상, 153건): 평균 월세 40.4만 원 (승강기 완비 신축 중심)"]),
        
        ("chart08_option_score_effect.png", "CHART 08", "승강기 유무 및 풀옵션 여부별 월세 프리미엄", 
         "승강기 완비 건물의 월 +9.7만 원 압도적 프리미엄 규명",
         ["• 승강기(엘리베이터) 보유 비율: 오창 전체의 1.7% (10건)에 불과",
          "• 엘리베이터 보유 시 평균 월세 50.3만 원 vs 미보유 시 40.6만 원 (+9.7만 원 차이)",
          "• 풀옵션 완료 시 평균 월세 42.3만 원 vs 일반 40.4만 원 (+1.9만 원 차이)",
          "• 가전 옵션은 기본재화된 반면 이동 편의시설(승강기)이 결정적 차별화 요인"]),
        
        ("chart09_spatial_cluster_kde.png", "CHART 09", "오창읍 매물 지리적 공간 분포 및 클러스터", 
         "양청리 호수공원 상권과 구룡리 원룸촌의 2대 지리적 중심축",
         ["• 제1축: 양청리 호수공원 상업지구 (Lat 36.712, Lng 127.428) - 221건 집중",
          "• 제2축: 구룡리 먹자골목 원룸단지 (Lat 36.715, Lng 127.417) - 91건 집중",
          "• 제3축: 오창 2산단 주성리 신흥 주거지 (Lat 36.728, Lng 127.445) - 13건",
          "• 도보 상권 선호자는 양청리, 저렴한 주거비 선호자는 구룡리로 명확히 분기"]),
        
        ("chart10_tfidf_keywords_top30.png", "CHART 10", "Scikit-learn TF-IDF 핵심 키워드 Top 30", 
         "양청리, 풀옵션, 신축, 호수공원, 분리형, 주차의 6대 핵심 소구점",
         ["• 지역 브랜드 1위: '양청리' (38.4) 및 '구룡리' (24.8)",
          "• 상품 필수 속성: '풀옵션' (35.1), '신축' (22.3), '분리형' (18.2)",
          "• 생활 인프라 및 여가: '호수공원' (19.7), '주차' (16.5), '엘리베이터' (14.8)",
          "• 산단 교대근무 및 자차 출퇴근 특성으로 '주차'와 '채광'이 핵심 결정 요인"]),
        
        ("chart11_correlation_matrix.png", "CHART 11", "주요 수치형 변수 간 피어슨 상관계수 매트릭스", 
         "월세-총비용의 완전 선형성(+0.98) 및 면적-평당비용의 음의 상관(-0.48)",
         ["• 순수월세 ↔ 실질총주거비: r = +0.98 (실질 비용의 96%는 월세로 결정)",
          "• 전용면적 ↔ 순수월세: r = +0.64 (면적 1평 증가 시 정비례 월세 상승)",
          "• 전용면적 ↔ 평당비용: r = -0.48 (면적이 커질수록 평당 단가가 떨어지는 규모의 경제)",
          "• 보증금 ↔ 순수월세: r = +0.41 (고가 주택일수록 보증금과 월세가 동반 상승)"])
    ]

    for img_name, tag, title, sub, bullets in chart_slides:
        s = prs.slides.add_slide(blank_layout)
        set_slide_background(s, BG_DARK)
        add_header(s, tag, title, sub)

        add_rounded_card(s, Inches(0.8), Inches(1.8), Inches(7.4), Inches(5.1), CARD_DARK, BORDER_DARK, 1)
        img_path = IMAGES_DIR / img_name
        if img_path.exists():
            s.shapes.add_picture(str(img_path), Inches(0.95), Inches(1.95), width=Inches(7.1))

        add_rounded_card(s, Inches(8.4), Inches(1.8), Inches(4.133), Inches(5.1), CARD_DARK, BORDER_DARK, 1)
        tbox = s.shapes.add_textbox(Inches(8.65), Inches(2.0), Inches(3.65), Inches(4.7))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        r_h = p_h.add_run()
        r_h.text = "📊 핵심 분석 요약"
        r_h.font.name = FONT_HEADING
        r_h.font.size = Pt(13)
        r_h.font.bold = True
        r_h.font.color.rgb = PRIMARY_AMBER

        for b_text in bullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(10)
            r_b = p_b.add_run()
            r_b.text = b_text
            r_b.font.name = FONT_BODY
            r_b.font.size = Pt(10)
            r_b.font.color.rgb = TEXT_LIGHT

        speaker_script = (
            f"본 슬라이드는 {title}에 대한 분석 결과입니다. {sub}. "
            f"{' '.join(bullets[:2])} "
            "이러한 분석 결과는 오창읍 임대차 시장에서 가격과 면적, 옵션 간의 실질적인 상관관계를 증명하며, "
            "실수요자에게 합리적인 주거 선택의 기준을 제공합니다."
        )
        set_speaker_notes(s, speaker_script)

    # ==========================================
    # Slide 16: 종합 결론 및 실행 로드맵
    # ==========================================
    s_end = prs.slides.add_slide(blank_layout)
    set_slide_background(s_end, BG_DARK)
    add_header(s_end, "STRATEGIC RECOMMENDATIONS", "종합 결론: 이해관계자별 실행 로드맵", "청년 임차인, 임대인 자산관리자, 지자체 정책 입안자를 위한 데이터 기반 제언")

    recs_cards = [
        ("청년 임차인 / 연구원", "가성비 극대화 및 지출 방어", [
            "• 평당 4.0만 원 선의 투룸을 임차하여 드레스룸/서재 분리 활용",
            "• 도보 상권 선호 시 양청리, 최저 주거비 추구 시 구룡리 선택",
            "• 표면 월세보다 '월세+관리비' 합산 실질 총주거비 기준 계약"
        ], PRIMARY_BLUE),
        ("임대인 / 자산관리자", "공실률 제로 및 수익률 제고", [
            "• 승강기 설치 및 전용 주차 공간 확충으로 월 +9.7만 원 프리미엄 확보",
            "• 노후 단독 원룸 리모델링 시 슬라이딩 도어 적용 1.5룸화 전환",
            "• 단순 풀옵션을 넘어 전자레인지, 건조기 등 차별화 옵션 완비"
        ], PRIMARY_AMBER),
        ("지자체 / 정책 입안자", "산단 청년 정착 주거 지원", [
            "• 청년 주거비 지원 기준을 관리비 포함 실질 45~50만 원 선으로 현실화",
            "• 원룸 밀집 구시가지(구룡리) 공용 안심 주차장 및 방범 인프라 확충",
            "• 2차전지·반도체 첨단 R&D 인력 유치를 위한 소형 공공임대 확대"
        ], ACCENT_TEAL)
    ]

    for idx, (title, sub, items, color) in enumerate(recs_cards):
        left = Inches(0.8 + idx * 3.95)
        add_rounded_card(s_end, left, Inches(1.8), Inches(3.75), Inches(5.0), CARD_DARK, BORDER_DARK, 1)

        tbox = s_end.shapes.add_textbox(left + Inches(0.25), Inches(2.0), Inches(3.25), Inches(4.5))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = FONT_HEADING
        r_t.font.size = Pt(14)
        r_t.font.bold = True
        r_t.font.color.rgb = color

        p_sub = tf.add_paragraph()
        p_sub.space_before = Pt(4)
        r_sub = p_sub.add_run()
        r_sub.text = sub
        r_sub.font.name = FONT_BODY
        r_sub.font.size = Pt(11)
        r_sub.font.bold = True
        r_sub.font.color.rgb = TEXT_LIGHT

        for it in items:
            p_it = tf.add_paragraph()
            p_it.space_before = Pt(10)
            r_it = p_it.add_run()
            r_it.text = it
            r_it.font.name = FONT_BODY
            r_it.font.size = Pt(9.5)
            r_it.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s_end,
        "마지막으로 오창읍 원룸·빌라 월세 시장에 대한 이해관계자별 종합 전략을 말씀드리겠습니다. "
        "청년 임차인은 평당 가성비가 26% 뛰어난 투룸 매물을 적극 고려하고 관리비 합산 금액으로 예산을 통제해야 합니다. "
        "임대인은 단순 풀옵션 경쟁을 지양하고 승강기나 주차, 1.5룸 구조 리모델링을 통해 차별화된 프리미엄을 창출해야 합니다. "
        "지자체는 오창 첨단산단의 우수 청년 인재들이 안정적으로 정주할 수 있도록 실질 주거비 수준에 맞춘 지원책을 펼쳐야 합니다. 경청해 주셔서 대단히 감사합니다."
    )

    prs.save(str(OUTPUT_PPTX))
    print(f"[+] 공식 PPTX 프레젠테이션 생성 완료 (총 16장): {OUTPUT_PPTX}")


if __name__ == "__main__":
    build_pptx()
