"""Antigravity 에이전트 라이프사이클 훅: 변경사항 자동 Git 커밋 스크립트.

파일 쓰기(write_file), 편집(edit_file) 및 턴 종료(Stop) 시점에 호출되어,
작업 디렉토리의 변경사항을 감지하고 의미 있는 커밋 메시지로 자동 git add 및 git commit을 수행합니다.
"""

import json
import os
import subprocess
import sys
from datetime import datetime

# Windows 환경 콘솔 UTF-8 출력 보장
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_git_command(args: list[str]) -> tuple[int, str, str]:
    """Git 명령어를 실행하고 리턴코드, stdout, stderr를 반환합니다."""
    try:
        process = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=(sys.platform == "win32")
        )
        return process.returncode, process.stdout.strip(), process.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def get_changed_files() -> list[tuple[str, str]]:
    """현재 작업 트리의 변경/추가/삭제된 파일 목록을 반환합니다."""
    code, stdout, _ = run_git_command(["status", "--porcelain"])
    if code != 0 or not stdout:
        return []

    changes = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        status = line[:2].strip()
        filepath = line[3:].strip().strip('"')
        changes.append((status, filepath))
    return changes


def generate_commit_message(changes: list[tuple[str, str]], context: dict) -> str:
    """변경 내역과 훅 컨텍스트를 분석하여 적절한 커밋 메시지를 생성합니다."""
    tool_call = context.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    tool_args = tool_call.get("args", {})
    target_path = tool_args.get("Path", "")

    # 1. 특정 단일 파일이 toolCall에 의해 변경된 경우
    if target_path:
        base_name = os.path.basename(target_path)
        return f"auto: {tool_name} 호출로 인한 {base_name} 변경사항 자동 커밋"

    # 2. 파일 목록 기반 메시지 생성
    file_names = [os.path.basename(f) for _, f in changes]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if len(file_names) == 1:
        return f"auto: {file_names[0]} 변경사항 자동 커밋 ({now_str})"
    elif len(file_names) <= 3:
        summary = ", ".join(file_names)
        return f"auto: {summary} 등 변경사항 자동 커밋 ({now_str})"
    else:
        dirs = {os.path.dirname(f).split(os.sep)[0] or "root" for _, f in changes}
        dir_summary = "/".join(sorted(dirs)[:3])
        return f"auto: {dir_summary} 영역 {len(changes)}개 파일 변경사항 자동 커밋 ({now_str})"


def auto_commit(context: dict) -> bool:
    """Git 변경사항을 감지하고 자동 커밋을 수행합니다."""
    # 1. Git 저장소 여부 확인
    code, _, _ = run_git_command(["rev-parse", "--is-inside-work-tree"])
    if code != 0:
        return False

    # 2. 변경된 파일 확인
    changes = get_changed_files()
    if not changes:
        return False

    # 3. 변경사항 스테이징 (git add -A)
    # .gitignore 규칙이 자동으로 적용됩니다.
    add_code, _, add_err = run_git_command(["add", "-A"])
    if add_code != 0:
        sys.stderr.write(f"[Auto-Commit] git add 실패: {add_err}\n")
        return False

    # 스테이징 후 다시 커밋 대상이 있는지 확인
    diff_code, diff_out, _ = run_git_command(["diff", "--cached", "--name-only"])
    if diff_code != 0 or not diff_out:
        return False

    # 4. 커밋 메시지 생성
    commit_msg = generate_commit_message(changes, context)

    # 5. 커밋 실행
    commit_code, commit_out, commit_err = run_git_command(["commit", "-m", commit_msg])
    if commit_code == 0:
        sys.stderr.write(f"[Auto-Commit] [성공] {commit_msg}\n")
        return True
    else:
        sys.stderr.write(f"[Auto-Commit] [실패] git commit 에러: {commit_err or commit_out}\n")
        return False


def main():
    context = {}
    is_hook = "--hook" in sys.argv

    if is_hook:
        # 훅 모드일 때만 stdin 읽기 시도
        try:
            raw_input = sys.stdin.read().strip()
            if raw_input:
                context = json.loads(raw_input)
        except Exception:
            pass

    # 자동 커밋 수행
    auto_commit(context)

    # Antigravity 훅 표준 응답 출력 (PostToolUse / Stop 공통 빈 객체)
    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
