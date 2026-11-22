# -*- coding: utf-8 -*-
"""
check_footnote_markers.py — Kiểm tra toàn vẹn footnote inline markers trước khi build DOCX.

So sánh các footnote markers trong:
  (a) Khối "--- [Cước chú trang X-Y] ---" của file bản dịch (notes block) → đây là danh sách "mong đợi"
  (b) Các marker inline [N] trong thân bài bản dịch (body text)

Báo cáo:
  - Missing markers: có trong notes block nhưng không có trong body
  - Duplicate markers: xuất hiện >1 lần trong body
  - Orphan markers: có trong body nhưng không có trong notes block

Usage:
    python 99_scripts/check_footnote_markers.py 12          # kiểm tra chương 12
    python 99_scripts/check_footnote_markers.py 12 --json   # xuất JSON kết quả

Exit code:
    0 = PASS (không có missing, duplicate, orphan)
    1 = FAIL (có lỗi)
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

# Đảm bảo stdout UTF-8 để tránh lỗi UnicodeEncodeError trên Windows PowerShell (cp1252)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJECT = Path(__file__).resolve().parents[1]
TP = PROJECT / "translation-project"
SRC_DIR = TP / "04_translation" / "v1"

# Marker inline [N] trong thân bài
INLINE_MARKER = re.compile(r"\[(\d{1,3})\]")

# Header khối cước chú: --- [Cước chú trang X-Y] ---
NOTE_BLOCK_HEADER = re.compile(r"^--- \[Cước chú (.+?)\] ---\s*$")

# Mỗi entry cước chú: [N] text...
NOTE_ENTRY = re.compile(r"^\[(\d{1,3})\]\s+(.+)$")


def find_vi_file(chap_id: str) -> Path:
    """Tìm file v1_chNN_vi.txt cho chương."""
    vol = chap_id[1]  # '1' từ 'V1-C12'
    num = chap_id[-2:]  # '12' từ 'V1-C12'
    path = SRC_DIR / f"ch{num}" / f"v1_ch{num}_vi.txt"
    if not path.exists():
        # Thử tìm linh hoạt
        matches = list(SRC_DIR.glob(f"ch*/v1_ch*_vi.txt"))
        for m in matches:
            if m.parent.name[-2:].zfill(2) == num.zfill(2):
                return m
        raise FileNotFoundError(f"Không tìm thấy file bản dịch cho {chap_id}")
    return path


def parse_notes_block(text: str) -> dict[int, str]:
    """Trích xuất tất cả footnote entries từ khối '--- [Cước chú ...] ---'."""
    lines = text.split("\n")
    in_notes = False
    notes: dict[int, str] = {}
    for line in lines:
        s = line.strip()
        if NOTE_BLOCK_HEADER.match(s):
            in_notes = True
            continue
        if in_notes:
            if s.startswith("--- [") and not NOTE_BLOCK_HEADER.match(s):
                # Đã ra khỏi khối notes (khối block khác bắt đầu)
                break
            m = NOTE_ENTRY.match(s)
            if m:
                num = int(m.group(1))
                note_text = m.group(2).strip()
                notes.setdefault(num, note_text)  # drop exact duplicates
            elif s and not s.startswith("--- ["):
                # Continuation line của note trước
                if notes:
                    last = max(notes)
                    if notes[last]:
                        notes[last] += " " + s
    return notes


def parse_inline_markers(text: str) -> list[int]:
    """Trích xuất tất cả marker [N] từ thân bài (loại trừ khối notes)."""
    # Loại trừ khối notes block trước khi tìm markers
    lines = text.split("\n")
    in_notes = False
    body_lines: list[str] = []
    for line in lines:
        s = line.strip()
        if NOTE_BLOCK_HEADER.match(s):
            in_notes = True
            continue
        if in_notes:
            if s.startswith("--- [") and not NOTE_BLOCK_HEADER.match(s):
                in_notes = False
                body_lines.append(line)
                continue
            # Trong khối notes: bỏ qua
            continue
        body_lines.append(line)

    body_text = "\n".join(body_lines)
    markers: list[int] = []
    for m in INLINE_MARKER.finditer(body_text):
        markers.append(int(m.group(1)))
    return markers


def check_markers(chap_id: str, json_output: bool = False) -> int:
    """Chạy kiểm tra. Trả về exit code (0=PASS, 1=FAIL)."""
    vi_path = find_vi_file(chap_id)
    text = vi_path.read_text(encoding="utf-8-sig")

    notes = parse_notes_block(text)
    body_markers = parse_inline_markers(text)

    note_nums = set(notes.keys())
    body_nums = set(body_markers)

    missing = sorted(note_nums - body_nums)  # có trong notes, không có trong body
    duplicates = sorted([n for n in body_nums if body_markers.count(n) > 1])
    orphans = sorted(body_nums - note_nums)  # có trong body, không có trong notes

    result = {
        "chapter": chap_id,
        "vi_file": str(vi_path),
        "total_notes": len(notes),
        "total_body_markers": len(body_markers),
        "unique_body_markers": len(body_nums),
        "missing": missing,
        "duplicate": duplicates,
        "orphan": orphans,
        "pass": len(missing) == 0 and len(duplicates) == 0 and len(orphans) == 0,
    }

    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== CHECK FOOTNOTE MARKERS — {chap_id} ===")
        print(f"File: {vi_path}")
        print(f"Total notes block: {result['total_notes']}")
        print(f"Total markers in body: {result['total_body_markers']}")
        print(f"Unique markers in body: {result['unique_body_markers']}")
        print()

        if missing:
            print(f"[MISSING] {len(missing)} markers in notes but NOT in body:")
            for n in missing:
                preview = notes[n][:80].replace("…", "...")
                print(f"  [{n}] {preview}")
            print()
        if duplicates:
            print(f"[DUPLICATE] {len(duplicates)} markers appearing >1 time in body:")
            for n in duplicates:
                count = body_markers.count(n)
                print(f"  [{n}] appears {count} times")
            print()
        if orphans:
            print(f"[ORPHAN] {len(orphans)} markers in body but NOT in notes:")
            for n in orphans:
                print(f"  [{n}]")
            print()

        if result["pass"]:
            print("RESULT: PASS — All markers match, no missing, no duplicate, no orphan.")
        else:
            print("RESULT: FAIL — Marker errors found. Do NOT build DOCX until fixed.")

    return 0 if result["pass"] else 1


def main():
    parser = argparse.ArgumentParser(
        description="Kiểm tra toàn vẹn footnote inline markers trước khi build DOCX"
    )
    parser.add_argument("chapter", type=int, help="Số chương (ví dụ: 12)")
    parser.add_argument(
        "--json", action="store_true", help="Xuất kết quả dạng JSON"
    )
    args = parser.parse_args()

    chap_id = f"V1-{args.chapter:02d}"
    # Thử v2, v3 nếu v1 không tồn tại
    for vol in ("v1", "v2", "v3"):
        test_path = SRC_DIR / f"ch{args.chapter:02d}" / f"v1_ch{args.chapter:02d}_vi.txt"
        # find_vi_file sẽ xử lý
        break

    exit_code = check_markers(chap_id, args.json)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
