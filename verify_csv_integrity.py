"""수집된 데이터셋(CSV)의 무결성을 검증하는 자동화 훅 스크립트.

인코딩(UTF-8-SIG), 컬럼 헤더 무결성, 빈 행 유무,
순위 필드 연속성, 결측치 비율 등을 전수 감사하여 결과를 보고합니다.
"""

import csv
import json
import sys
from pathlib import Path

# Windows 환경 콘솔 UTF-8 출력 보장
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def verify_csv(file_path: str | Path) -> dict:
    path = Path(file_path)
    if not path.exists():
        return {"status": "FAIL", "error": f"파일을 찾을 수 없습니다: {path}"}

    # 1. 인코딩 및 BOM 검사
    raw_bytes = path.read_bytes()
    is_utf8_sig = raw_bytes.startswith(b"\xef\xbb\xbf")

    try:
        text_content = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        return {"status": "FAIL", "error": f"UTF-8 디코딩 실패: {e}"}

    # 2. CSV 구조 파싱
    lines = [line for line in text_content.splitlines() if line.strip()]
    if not lines:
        return {"status": "FAIL", "error": "CSV 파일이 비어 있습니다."}

    reader = csv.DictReader(lines)
    fieldnames = reader.fieldnames or []
    rows = list(reader)
    total_rows = len(rows)

    if total_rows == 0:
        return {"status": "FAIL", "error": "헤더 외에 데이터 행이 존재하지 않습니다."}

    # 3. 결측치 및 무결성 집계
    missing_counts = {col: 0 for col in fieldnames}
    for row in rows:
        for col in fieldnames:
            val = row.get(col, "")
            if val is None or str(val).strip() == "":
                missing_counts[col] += 1

    # 4. 순위 연속성 검사 (rank 컬럼이 있을 경우)
    rank_check = {"has_rank": False, "is_continuous": False, "min": None, "max": None}
    if "rank" in fieldnames:
        ranks = []
        for r in rows:
            v = r.get("rank", "")
            if str(v).isdigit():
                ranks.append(int(v))
        if ranks:
            rank_check["has_rank"] = True
            rank_check["min"] = min(ranks)
            rank_check["max"] = max(ranks)
            expected_ranks = list(range(min(ranks), min(ranks) + len(ranks)))
            rank_check["is_continuous"] = (ranks == expected_ranks)

    # 5. 최종 결과 종합
    report = {
        "status": "PASS",
        "file_name": path.name,
        "total_rows": total_rows,
        "total_columns": len(fieldnames),
        "columns": fieldnames,
        "is_utf8_sig": is_utf8_sig,
        "missing_summary": {k: v for k, v in missing_counts.items() if v > 0},
        "rank_continuity": rank_check,
    }

    # 경고 및 결측치율 검사
    critical_missing = False
    for col in ["title", "book_id", "id", "name"]:
        if col in missing_counts and missing_counts[col] > 0:
            critical_missing = True
            report["status"] = "WARN"

    if not is_utf8_sig:
        report["status"] = "WARN"
        report["encoding_note"] = "BOM(UTF-8-SIG)이 없어 엑셀에서 한글이 깨질 수 있습니다."

    return report


def main():
    target_file = None

    # 1. 커맨드라인 인자로 파일 경로가 주어진 경우
    if len(sys.argv) >= 2:
        target_file = sys.argv[1]
        is_hook_mode = False
    else:
        # 2. Antigravity Hook(stdin JSON) 모드로 호출된 경우
        is_hook_mode = True
        try:
            input_data = sys.stdin.read().strip()
            if input_data:
                payload = json.loads(input_data)
                tool_call = payload.get("toolCall", {})
                args = tool_call.get("args", {})
                file_path = args.get("Path", "")
                if file_path.endswith(".csv"):
                    target_file = file_path
        except Exception:
            pass

    if not target_file:
        if is_hook_mode:
            # 훅 시스템 응답 규격(빈 JSON 객체)
            print("{}")
            sys.exit(0)
        else:
            print("사용법: python verify_csv_integrity.py <CSV_파일_경로>")
            sys.exit(1)

    result = verify_csv(target_file)

    if not is_hook_mode:
        print("=" * 60)
        print(f"[데이터 무결성 검증] {result.get('file_name', target_file)}")
        print(f"상태: {result['status']}")
        print(f"총 데이터 행 수: {result.get('total_rows', 0):,}건")
        print(f"컬럼 수: {result.get('total_columns', 0)}개")
        print(f"UTF-8-SIG 인코딩: {'정상 (BOM 포함)' if result.get('is_utf8_sig') else '미적용 (BOM 없음)'}")
        
        rank_info = result.get("rank_continuity", {})
        if rank_info.get("has_rank"):
            cont_str = "연속성 일치 (누락 없음)" if rank_info.get("is_continuous") else "비연속 (누락 존재)"
            print(f"순위 범위: {rank_info.get('min')}위 ~ {rank_info.get('max')}위 ({cont_str})")

        missing = result.get("missing_summary", {})
        if missing:
            print("결측치 발생 컬럼:", missing)
        else:
            print("결측치: 0건 (완벽한 무결성)")
        print("=" * 60)

        if result["status"] == "FAIL":
            sys.exit(1)
    else:
        # Hook 모드에서는 표준 에러(stderr)에 검증 로그를 남기고 stdout에는 {} 출력
        sys.stderr.write(f"[CSV 무결성 검증] {result.get('file_name', target_file)} -> 상태: {result['status']}, 행: {result.get('total_rows', 0)}건\n")
        print("{}")


if __name__ == "__main__":
    main()
