# 📚 직방 세종 오피스텔 프로젝트 공식 문서 보관소 (Documentation Hub)

본 디렉터리는 세종특별자치시 정부청사 생활권(어진동·나성동·도담동) 오피스텔 데이터 수집, 심층 EDA, 비즈니스 리포트 및 웹 대시보드 구축과 관련된 모든 공식 문서를 영구 보존하는 아카이브입니다.

---

## 📑 보관 문서 목차

| 파일명 | 문서 구분 | 주요 내용 요약 |
| :--- | :--- | :--- |
| **[api_specification.md](api_specification.md)** | 기술 명세서 | 직방 Gateway REST API 엔드포인트, 헤더, 페이로드 및 응답 JSON 스키마 |
| **[collection_plan.md](collection_plan.md)** | 수집 기획서 | 어진동·나성동·도담동 공간적 범위 설정 및 무결성 기준 |
| **[implementation_plan.md](implementation_plan.md)** | 구현 설계서 | 스크래퍼, 10종 차트 심층 EDA, 앰버 글래스모피즘 대시보드 엔드투엔드 설계서 |
| **[walkthrough.md](walkthrough.md)** | 결과 보고서 | 전체 파이프라인 수행 결과, 산출물 목록 및 검증 Walkthrough |
| **[subagent_workflow_and_audits.md](subagent_workflow_and_audits.md)** | 서브에이전트 감사서 | 4종 서브에이전트(빌더 2종+리뷰어 2종) 협업 워크플로우 및 정밀 감사 보고서 전문 |
| **[subagents/docx-builder.md](subagents/docx-builder.md)** | 에이전트 명세서 | Word 보고서 자동 생성 서브에이전트 역할 및 시스템 프롬프트 명세 |
| **[subagents/pptx-builder.md](subagents/pptx-builder.md)** | 에이전트 명세서 | 16:9 와이드 PPTX 슬라이드 생성 서브에이전트 역할 및 시스템 프롬프트 명세 |
| **[subagents/docx-reviewer.md](subagents/docx-reviewer.md)** | 에이전트 명세서 | Word 보고서 품질 감사 및 무결성 검증 서브에이전트 역할 명세 |
| **[subagents/pptx-reviewer.md](subagents/pptx-reviewer.md)** | 에이전트 명세서 | PPTX 디자인 및 발표 대본 검증 서브에이전트 역할 명세 |
| **[../reports/Sejong_Officetel_Report.docx](../reports/Sejong_Officetel_Report.docx)** | 공식 Word 보고서 | 10대 차트 전수 수록 및 4,500자 이상 비즈니스 제언 포함 완성본 (.docx) |
| **[../reports/Sejong_Officetel_Presentation.pptx](../reports/Sejong_Officetel_Presentation.pptx)** | 공식 발표 자료 | 16:9 와이드 13장 슬라이드 및 13장 전수 발표자 노트 완비본 (.pptx) |
| **[../reports/EDA_Report.md](../reports/EDA_Report.md)** | 분석 보고서 | 10대 핵심 차트 해석 및 2,000자 이상 실거주/가성비 비즈니스 종합 리포트 |
| **[../reports/EDA_Report.pdf](../reports/EDA_Report.pdf)** | 공식 인쇄본 | Print-CSS 기반 고해상도 A4 PDF 인쇄용 보고서 |

---

## 💡 문서 활용 가이드
- **개발 및 API 스펙 확인 시**: `api_specification.md` 참조
- **수집 및 정제 기준 확인 시**: `collection_plan.md` 및 `implementation_plan.md` 참조
- **실거주 상권 분석 및 비즈니스 의사결정 시**: `../reports/EDA_Report.md` 참조
- **인터랙티브 웹 대시보드 실행 시**: `../dashboard.html` 직접 실행
