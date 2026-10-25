# [Harness] 범용 웹 수집·EDA·대시보드 자동화 프레임워크 아키텍처 (Hardened v2.0)

본 문서는 신규 웹사이트(이커머스, 포털, 채용, 커뮤니티 등)를 대상으로 데이터 수집부터 20년차 분석가 수준의 심층 EDA, 마크다운 종합 리포트, 글래스모피즘 인터랙티브 웹 대시보드 빌드 및 CI/CD 라이브 배포까지 전 과정을 표준화하여 완수하는 **Harness (범용 자동화 프레임워크)**의 고도화된 아키텍처와 실행 흐름을 정의합니다.

---

## 1. Harness 전체 아키텍처 및 파이프라인 흐름

Harness는 사용자의 신규 프로젝트 요청 시 **5대 핵심 자산(Rule, Skill, Hook, Subagents, Plan)과 5대 보완 체계(체크포인트, 데이터 계약, 매니페스트, 비동기 요약 데이터, CI/CD)**가 유기적으로 연계되어 결함 없는 엔드투엔드 파이프라인을 완수합니다.

```mermaid
flowchart TD
    subgraph Trigger["1. 사용자 트리거"]
        User["사용자 요청\n(신규 사이트 X 수집 및 대시보드 제작)"]
    end

    subgraph Framework["2. Harness 통합 환경 (.agents/)"]
        direction TB
        R["Rule: universal-pipeline.md\n(표준 5대 폴더, uv 가상환경, UTF-8-SIG 원칙 강제)"]
        S["Skill: universal-data-pipeline\n(수집기, Pydantic 스키마, EDA, 대시보드, CI/CD 템플릿)"]
        H["Hook: hooks.json & verify_csv_integrity.py\n(파일 저장 시 데이터 무결성 및 Pydantic 계약 검증)"]
    end

    subgraph Orchestration["3. 중앙 상태 및 데이터 계약"]
        Manifest["pipeline_manifest.json\n(단계별 상태 추적 & 산출물 핸드오프)"]
        Checkpoint["data/checkpoint.json\n(수집 중단 시 이어받기 상태 기록)"]
        Summary["data/summary_data.json\n(대시보드용 경량 집계 데이터)"]
    end

    subgraph Agents["4. 4대 전문 서브에이전트 분업 파이프라인"]
        direction TB
        Crawler["site-crawler\n(API 역공학, 체크포인트 이어받기, Pydantic 검증)"]
        Analyst["eda-analyst\n(데이터 정제, 10종 차트, summary_data.json, 리포트)"]
        Architect["dashboard-architect\n(글래스모피즘 비동기 Fetch & 가상스크롤 대시보드)"]
        Orchestrator["pipeline-orchestrator\n(전체 조율, Git 브랜치, PR 및 배포 총괄)"]
    end

    subgraph Deliverables["5. 표준 산출물 및 배포"]
        DataDir["data/*.csv\n(BOM UTF-8, Pydantic 계약 통과)"]
        ImagesDir["images/*.png\n(10종 고해상도 시각화 차트)"]
        ReportsDir["reports/EDA_Report.md\n(2,000자 이상 심층 비즈니스 인사이트)"]
        SrcDir["src/dashboard.html\n(반응형 비동기 웹 대시보드)"]
        DeployTarget[".github/workflows/deploy.yml\n(GitHub Pages 무중단 자동 배포)"]
    end

    User --> R
    R --> S
    S --> Orchestrator
    Orchestrator --> Manifest
    Manifest --> Crawler
    Crawler <--> Checkpoint
    Crawler --> DataDir
    DataDir --> H
    H --> Analyst
    Analyst --> Summary
    Analyst --> ImagesDir
    Analyst --> ReportsDir
    Analyst --> Architect
    Architect --> SrcDir
    SrcDir --> Orchestrator
    Orchestrator --> DeployTarget
```

---

## 2. 단계별 실행 시퀀스 (Lifecycle)

작업이 시작되면 중앙 상태 파일(`pipeline_manifest.json`)을 기반으로 각 에이전트와 도구가 순차적으로 상호작용하며 자동 검증과 복원력을 제공합니다.

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant Orch as 오케스트레이터 (pipeline-orchestrator)
    participant Manifest as 상태 관리 (pipeline_manifest.json)
    participant Crawler as 수집기 (site-crawler)
    participant Hook as 무결성 훅 (verify_csv_integrity.py)
    participant Analyst as 데이터 분석가 (eda-analyst)
    participant Architect as 대시보드 빌더 (dashboard-architect)
    participant CI as 배포 자동화 (GitHub Actions)

    User->>Orch: "신규 사이트 데이터 수집 및 분석 대시보드 제작 요청"
    Orch->>Orch: 5대 표준 디렉터리 생성 (data, src, images, docs, reports)
    Orch->>Manifest: 초기 상태 및 파이프라인 메타데이터 기록
    Orch->>Crawler: 사이트 통신 분석 및 스크래핑 위임
    
    critical 수집 및 복원력 루프
        Crawler->>Crawler: data/checkpoint.json 확인 후 마지막 인덱스부터 이어받기
        Crawler->>Crawler: 지수 백오프 및 세션 갱신 처리
        Crawler->>Crawler: Pydantic Data Contract 스키마 검증
    end
    
    Crawler->>Hook: data/*.csv 파일 저장 (PostToolUse 트리거)
    Hook-->>Crawler: UTF-8-SIG 인코딩, 빈 행 및 결측률 자동 검증 완료
    Crawler->>Manifest: 수집 완료 상태 및 CSV 경로 업데이트
    Crawler->>Orch: 수집 완료 보고
    
    Orch->>Analyst: 20년차 데이터 분석가 지침 기반 심층 EDA 지시
    Analyst->>Analyst: 10종 고해상도 차트 생성 및 data/summary_data.json 사전 집계
    Analyst->>Analyst: Scikit-learn TF-IDF 분석 및 EDA_Report.md 발행
    Analyst->>Manifest: 분석 완료 상태 및 차트/리포트 경로 업데이트
    Analyst->>Orch: 종합 분석 보고서 작성 완료 보고
    
    Orch->>Architect: 글래스모피즘 인터랙티브 웹 대시보드 구축 위임
    Architect->>Architect: summary_data.json 비동기 Fetch & 가상 스크롤 dashboard.html 빌드
    Architect->>Manifest: 대시보드 빌드 완료 상태 업데이트
    Architect->>Orch: 웹 대시보드 빌드 완료 보고
    
    Orch->>CI: Git 브랜치/PR 생성 및 .github/workflows/deploy.yml 트리거
    CI->>User: GitHub Pages 라이브 배포 완료
```

---

## 3. Harness 핵심 컴포넌트 명세

| 컴포넌트 | 경로 / 식별자 | 주요 역할 및 특징 |
|---|---|---|
| **Rule** | `.agents/rules/universal-pipeline.md` | 표준 5대 폴더, `uv`(`.venv`), UTF-8-SIG, Pydantic 데이터 계약 준수 등 필수 규칙 강제 |
| **Skill** | `.agents/skills/universal-data-pipeline/SKILL.md` | 수집 템플릿, Pydantic 스키마 정의, 10종 시각화, `summary_data.json` 집계, 글래스모피즘 대시보드, CI 워크플로우 제공 |
| **Hook** | `.agents/hooks/verify_csv_integrity.py` | CSV 저장 시 BOM UTF-8, 빈 행, 결측률 검증 및 Pydantic 기반 스키마 이상치 차단 |
| **Subagents** | `site-crawler`, `eda-analyst`, `dashboard-architect`, `pipeline-orchestrator` | 컨텍스트 오염을 방지하고 각 영역별(수집/EDA/프론트엔드/배포) 독립 및 병렬 작업 수행 |
| **State Tracker** | `pipeline_manifest.json` | 에이전트 간 산출물 경로, 단계별 진행 상태(PENDING/IN_PROGRESS/COMPLETED), 오류 발생 시 롤백 정보 중앙 관리 |
| **Resilience State** | `data/checkpoint.json` | 네트워크 단절 및 레이트 리밋 발생 시 수집 재개를 위한 페이지/인덱스 체크포인트 |
| **Pre-aggregated Data**| `data/summary_data.json` | 대용량 데이터 시각화 렉을 방지하기 위한 대시보드 전용 경량 사전 집계 데이터 |
| **CI/CD Workflow** | `.github/workflows/deploy.yml` | PR 머지 기반 GitHub Pages 무중단 자동 배포 파이프라인 |

---

## 4. 6대 표준 실행 단계 상세

1. **Step 1: 사이트 구조 및 통신 프로토콜 정밀 분석**
   - 개발자 도구 네트워크 탭 분석 및 REST/GraphQL API 역공학 우선 탐색
   - User-Agent, 동적 세션 토큰 및 쿠키 자동 갱신 전략 수립
2. **Step 2: 복원력 높은 스크래퍼 구동 및 Pydantic 데이터 계약 검증**
   - `data/checkpoint.json` 상태 기반 수집 이어받기 지원
   - 지수 백오프(Exponential Backoff with Jitter) 및 429/403 방어
   - Pydantic 모델을 통한 타입, 필수값, 범위 유효성 검사 후 `data/*.csv` UTF-8-SIG 저장
3. **Step 3: 20년차 데이터 분석가 지침 기반 심층 EDA & 사전 집계**
   - 10종 이상 고해상도(300 DPI) 시각화 차트 생성 (`images/`)
   - Scikit-learn TF-IDF 키워드/바이그램 마이닝 및 통계적 이상치 검정
   - 대시보드 성능 보장을 위한 `data/summary_data.json` 경량 집계 데이터 사전 생성
4. **Step 4: 고품질 마크다운 종합 리포트 발행**
   - `reports/EDA_Report.md`에 2,000자 이상의 심층 비즈니스 인사이트 및 실행 전략 기술
5. **Step 5: 글래스모피즘 Chart.js 비동기 웹 대시보드 빌드**
   - `src/dashboard.html`에서 `summary_data.json`을 비동기 `fetch()`로 로딩
   - 상세 원천 데이터 테이블은 가상 스크롤(Virtualization) 또는 페이징 처리로 대용량 데이터 렉 차단
   - 화이트/다크 글래스모피즘 테마 및 반응형 UI 완비
6. **Step 6: Git 워크플로우 및 GitHub Actions CI/CD 라이브 배포**
   - `pipeline_manifest.json` 최종 완료 마킹
   - Git 이슈, 브랜치, PR 자동 생성 및 CI 무결성 통과 후 GitHub Pages 무중단 자동 배포
