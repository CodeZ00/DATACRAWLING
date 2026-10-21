"""GitHub Issue 생성, 커밋, 푸시 및 Pull Request 생성을 수행하는 스크립트."""

import json
import subprocess
import urllib.request

TOKEN = "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"
REPO = "CodeZ00/DATACRAWLING"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Antigravity-Agent",
}


def create_issue():
    url = f"https://api.github.com/repos/{REPO}/issues"
    data = {
        "title": "[FEAT] 교보문고 컴퓨터/IT 베스트셀러 데이터 수집 및 심층 EDA 분석 구축",
        "body": """## 📌 작업 개요
교보문고 컴퓨터/IT 분야 일간 베스트셀러 전체(658건) 목록을 공식 REST Gateway API를 통해 안정적으로 수집하고, 데이터의 통계적 특성과 출판 시장 트렌드를 파악하기 위한 심층 탐색적 데이터 분석(EDA) 및 리포트를 구축합니다.

## 🛠 세부 작업 내역
1. **수집 명세서 및 계획서 작성**:
   - `kyobo/docs/scraping_promt.md` (HTTP 요청 정보, 15개 스키마 컬럼 정의)
   - `kyobo/docs/kyobo_scraping_plan.md` (수집 단계별 검증 계획)
2. **REST API 스크래퍼 개발**:
   - `kyobo/src/kyobo_bestseller_scraper.py`
   - GZIP 압축 해제, HTML 태그 정제, 요청 간 0.5초 딜레이 적용
3. **데이터 수집 및 무결성 검증**:
   - `kyobo/data/kyobo_daily_it_bestseller_20261020.csv`
   - 658건 전수 수집(1위~658위 연속), 결측치 0건, UTF-8-SIG 인코딩
4. **심층 EDA 분석 및 시각화**:
   - `kyobo/src/kyobo_eda_analysis.py` (11개 일변량/이변량/다변량 차트 생성)
   - `kyobo/images/` (고해상도 시각화 차트 이미지 11종 저장)
5. **전문가 분석 리포트 발행**:
   - `kyobo/reports/EDA_Report.md` (20년차 데이터 분석가 가이드라인 준수, 기술통계 심층 해석 포함)
""",
        "labels": ["enhancement"],
    }

    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=HEADERS, method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f">>> GitHub Issue 생성 완료: #{res['number']} ({res['html_url']})")
        return res["number"], res["html_url"]


def run_git_commands(issue_number):
    branch_name = "feat/kyobo-scraping-and-eda"
    print(f">>> Git 브랜치 생성 및 전환: {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)

    print(">>> 파일 스테이징: kyobo/ 폴더")
    subprocess.run(["git", "add", "kyobo/"], check=True)

    commit_msg = f"feat: 교보문고 컴퓨터/IT 베스트셀러 스크래퍼 및 심층 EDA 리포트 추가 (#{issue_number})\n\n- 교보문고 REST API 기반 658건 데이터 수집\n- 11개 고해상도 시각화 차트 및 TF-IDF 키워드 분석\n- 전문 EDA 분석 보고서(EDA_Report.md) 작성"
    print(f">>> 커밋 수행: {commit_msg.splitlines()[0]}")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print(f">>> 원격 저장소 푸시: origin {branch_name}")
    subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)


def create_pull_request(issue_number):
    url = f"https://api.github.com/repos/{REPO}/pulls"
    data = {
        "title": f"[FEAT] 교보문고 컴퓨터/IT 베스트셀러 데이터 수집 및 심층 EDA 분석 구축 (#{issue_number})",
        "head": "feat/kyobo-scraping-and-eda",
        "base": "main",
        "body": f"""## 🎯 Pull Request 개요
이슈 #{issue_number} 작업을 완료하여 교보문고 컴퓨터/IT 베스트셀러 전수 수집 및 전문 EDA 분석 리포트를 메인 브랜치에 반영합니다.

## 📦 주요 변경 사항
- **데이터 수집 모듈**:
  - `kyobo/src/kyobo_bestseller_scraper.py`: 교보문고 REST Gateway API 연동 스크래퍼
  - `kyobo/data/kyobo_daily_it_bestseller_20261020.csv`: 수집된 658건 정제 데이터셋 (UTF-8-SIG)
- **명세서 및 계획서**:
  - `kyobo/docs/scraping_promt.md`: API 명세 및 15개 스키마 컬럼 정의
  - `kyobo/docs/kyobo_scraping_plan.md`: 데이터 수집 프로세스 및 검증 계획
- **EDA 분석 및 시각화**:
  - `kyobo/src/kyobo_eda_analysis.py`: 11종 차트 시각화 및 통계 산출 스크립트
  - `kyobo/src/generate_tables.py`: 요약 통계 테이블 생성
  - `kyobo/images/`: 11개 시각화 차트 이미지 저장 (가격 분포, 평점, 출판사 점유율, TF-IDF 등)
  - `kyobo/reports/EDA_Report.md`: 20년차 데이터 분석가 가이드라인에 따른 종합 보고서

Closes #{issue_number}
""",
    }

    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=HEADERS, method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f">>> Pull Request 생성 완료: #{res['number']} ({res['html_url']})")
        return res["number"], res["html_url"]


if __name__ == "__main__":
    issue_num, issue_url = create_issue()
    run_git_commands(issue_num)
    pr_num, pr_url = create_pull_request(issue_num)
    print("\n" + "=" * 60)
    print("깃헙 이슈 생성, 커밋, 푸시, PR 생성 전체 프로세스 완료!")
    print(f"이슈 링크: {issue_url}")
    print(f"PR 링크: {pr_url}")
    print("=" * 60)
