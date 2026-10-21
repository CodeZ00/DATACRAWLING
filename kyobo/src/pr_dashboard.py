"""대시보드 구현 커밋, 원격 푸시 및 Pull Request 생성을 수행하는 스크립트."""

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


def git_commit_and_push():
    branch_name = "feat/kyobo-glassmorphism-dashboard"
    print(">>> 파일 스테이징 중...")
    subprocess.run(["git", "add", "kyobo/"], check=True)

    commit_msg = (
        "feat: 교보문고 IT 베스트셀러 글래스모피즘 웹 대시보드 구축 (#3)\n\n"
        "- Chart.js 기반 6대 인터랙티브 차트 구현\n"
        "- 앰비언트 글로우 및 블러 효과의 글래스모피즘 UI 스타일링\n"
        "- 658건 전수 실시간 검색, 다중 필터, 동적 정렬, 페이징 테이블 및 도서 상세 모달\n"
        "- 독립형 단일 파일(dashboard.html) 번들링으로 로컬 즉시 구동 지원"
    )
    print(">>> 커밋 수행 중...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print(f">>> 원격 푸시 중: origin {branch_name}")
    subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)


def create_pull_request():
    url = f"https://api.github.com/repos/{REPO}/pulls"
    payload = {
        "title": "[FEAT] 교보문고 IT 베스트셀러 글래스모피즘 웹 대시보드 (Chart.js) 구축 (#3)",
        "head": "feat/kyobo-glassmorphism-dashboard",
        "base": "main",
        "body": """## 🎨 Pull Request 개요
이슈 #3에 계획된 교보문고 컴퓨터/IT 베스트셀러 658건 대상 **글래스모피즘(Glassmorphism) 기반 Chart.js 웹 대시보드** 구현을 완료하여 메인 브랜치에 반영합니다.

## ✨ 주요 구현 사항
1. **글래스모피즘(Glassmorphism) UI & 디자인**:
   - 앰비언트 글로우(Ambient Glow) 오로라 원형 배경 블러 애니메이션
   - 반투명 글래스 카드(`backdrop-blur-md`, `border-white/10`, `bg-slate-900/55`)
   - 네온 시안/블루/에메랄드/퍼플 액센트 컬러 시스템 적용

2. **핵심 메트릭 KPI 카드 (4종)**:
   - 총 도서 수 (`658권`)
   - 평균 실구매가 (`24,955원`, 중앙값 23,400원)
   - 평균 리뷰 평점 (`8.13점` / 10점 만점)
   - 최다 리뷰 도서 (`469건`, 진짜 쓰는 실무 엑셀)

3. **Chart.js 6대 인터랙티브 차트 그리드**:
   - `차트 1`: 가격대 구간별 도서 분포 (Bar Chart)
   - `차트 2`: 상위 10대 출판사 시장 점유율 (Doughnut Chart)
   - `차트 3`: 출간 연도별 신간 진입 추이 (Line & Area Chart)
   - `차트 4`: 순위 구간별 평균 리뷰 수 (Bar Chart)
   - `차트 5`: 평점 구간별 도서 분포 현황 (Polar Area Chart)
   - `차트 6`: TF-IDF 상위 핵심 키워드 Top 15 (Horizontal Bar Chart)

4. **실시간 데이터 탐색기 & 모달 인터랙션**:
   - 실시간 텍스트 검색 (도서명, 저자, 출판사)
   - 출판사 드롭다운, 가격대별, 최소 평점별 다중 복합 필터링
   - 테이블 헤더 클릭 기반 실시간 동적 정렬 (순위, 판매가, 리뷰수, 평점)
   - 15/30/50개 단위 반응형 페이지네이션
   - 행 클릭 시 도서 소개글(`intro`), ISBN, 상세 가격을 보여주는 글래스 모달 팝업
   - 필터링된 결과 즉시 CSV 다운로드 기능

5. **완전 독립형 배포**:
   - 658건 전수 데이터 인라인 임베드로 별도 웹서버 없이 로컬 브라우저(`file:///.../dashboard.html`) 더블클릭만으로 즉시 구동

## 📁 주요 변경 파일
- `kyobo/src/dashboard.html`: 완성된 독립형 글래스모피즘 웹 대시보드
- `kyobo/src/build_dashboard.py`: 대시보드 컴파일 및 번들러 스크립트
- `kyobo/docs/dashboard_implementation_plan.md`: 세부 구축 계획서

Closes #3
""",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=HEADERS,
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        pr_number = res["number"]
        pr_url = res["html_url"]
        print(f">>> Pull Request 생성 완료: #{pr_number} - {pr_url}")
        return pr_number, pr_url


if __name__ == "__main__":
    git_commit_and_push()
    pr_num, pr_url = create_pull_request()
    print("\n" + "=" * 60)
    print(f"PR 생성 완료: {pr_url}")
    print("=" * 60)
