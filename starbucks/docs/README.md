# 📚 스타벅스 프로젝트 공식 문서 저장소 (Documentation Hub)

본 디렉터리는 스타벅스 전국 매장 수집 및 데이터 파이프라인과 관련된 모든 계획서, 기술 명세서, 분석 보고서 아티팩트를 영구 보존하는 공식 문서 보관소입니다.

---

## 📑 보관 문서 목차

| 파일명 | 문서 구분 | 주요 내용 요약 |
| :--- | :--- | :--- |
| **[api_specification.md](api_specification.md)** | 기술 명세서 | 스타벅스 Gateway REST API(`getStore.do`) 엔드포인트, 헤더, 페이로드 및 응답 JSON 스키마 |
| **[starbucks_collection_plan.md](starbucks_collection_plan.md)** | 수집 기획서 | 1차 서울 검증(712개) ➔ 2차 전국 전수 수집(2,213개) 2단계 수집 전략 및 무결성 기준 |
| **[implementation_plan.md](implementation_plan.md)** | 구현 계획서 | 스크래퍼, 10종 차트 심층 EDA, 글래스모피즘 인터랙티브 대시보드 엔드투엔드 구현 설계서 |
| **[artifact_storage_plan.md](artifact_storage_plan.md)** | 운영 계획서 | 모든 아티팩트의 `docs/` 전수 보존 및 영구 동기화 관리 체계 |
| **[walkthrough.md](walkthrough.md)** | 결과 보고서 | 전체 수집, 검증(PASS), 10종 시각화, 웹 대시보드 완성 Walkthrough |
| **[../reports/EDA_Report.md](../reports/EDA_Report.md)** | 분석 보고서 | 10대 핵심 차트 해석 및 2,000자 이상 비즈니스 심층 인사이트 종합 보고서 |

---

## 💡 문서 활용 가이드
- **API 연동 및 크롤링 개발 시**: `api_specification.md` 참조
- **수집 및 검증 절차 확인 시**: `implementation_plan.md` 및 `walkthrough.md` 참조
- **상권 분석 및 비즈니스 의사결정 시**: `../reports/EDA_Report.md` 참조
- **웹 대시보드 열람 시**: `../dashboard.html` 직접 실행
