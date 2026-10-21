"""대시보드 계획서를 GitHub 이슈로 등록하는 스크립트."""

import json
from pathlib import Path
import urllib.request

TOKEN = "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"
REPO = "CodeZ00/DATACRAWLING"
URL = f"https://api.github.com/repos/{REPO}/issues"

plan_path = Path(
    r"C:\Users\user\.gemini\antigravity-cli\brain\1b236998-bba7-4d00-b669-c0e1706a6c08\dashboard_implementation_plan.md"
)
plan_content = plan_path.read_text(encoding="utf-8")

payload = {
    "title": "[FEAT] 교보문고 IT 베스트셀러 글래스모피즘 웹 대시보드 (Chart.js) 구축",
    "body": plan_content,
    "labels": ["enhancement"],
}

req = urllib.request.Request(
    URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Antigravity-Agent",
    },
    method="POST",
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    issue_num = res["number"]
    issue_url = res["html_url"]
    print(f"Issue Created: #{issue_num} - {issue_url}")
