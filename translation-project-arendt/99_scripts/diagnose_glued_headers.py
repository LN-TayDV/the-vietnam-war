# -*- coding: utf-8 -*-
"""
Chẩn đoán: tiêu đề chương / section heading / running header bị DÁN LIỀN vào
body text (không có newline phân tách) — lỗi segmentation/OCR.

Phát hiện:
  - Dòng mở đầu bằng >=3 từ ALL-CAPS liên tiếp (ứng viên tiêu đề/running header)
    rồi CHUYỂN SANG từ thường (body) trên CÙNG dòng.
  - Dòng ALL-CAPS kèm số trang ở cuối (running header).
  - Tiêu đề chương lặp ở đầu nhiều trang (running header).

Không sửa file gốc. Chỉ báo cáo. UTF-8.
"""
from __future__ import annotations
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 99_scripts/ -> translation-project-arendt
V2 = ROOT / "04_translation" / "v2"
CHAPTERS = [f"ch{i:02d}" for i in range(1, 14)]

UPPER = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
def is_upper_word(w: str) -> bool:
    letters = [c for c in w if c.isalpha()]
    if not letters:
        return False
    return all(c.isupper() for c in letters)

def leading_caps_run(line: str):
    """Trả về (số từ ALL-CAPS ở đầu, từ đầu tiên không phải caps, index kết thúc caps)."""
    words = line.split(" ")
    n = 0
    i = 0
    while i < len(words):
        w = words[i].strip(".,;:'\"()[]")
        if w and is_upper_word(w):
            n += 1
            i += 1
        else:
            break
    return n, (words[i] if i < len(words) else ""), i

PARA_HDR = re.compile(r"\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)")

def diag_chapter(ch: str):
    f = V2 / ch / f"v1_{ch}_vi.txt"
    if not f.exists():
        return []
    t = f.read_text(encoding="utf-8").replace("\r\n", "\n")
    # body only
    body = t.split("=== FOOTNOTES ===")[0]
    matches = list(PARA_HDR.finditer(body))
    findings = []
    for j, m in enumerate(matches):
        pid = m.group(1); page = int(m.group(2))
        start = m.end()
        end = matches[j+1].start() if j+1 < len(matches) else len(body)
        block = body[start:end].strip("\n")
        if not block.strip():
            continue
        first_line = block.split("\n", 1)[0].strip()
        n_caps, next_word, idx = leading_caps_run(first_line)
        # glued title: >=3 caps words then a lowercase/mixed body word on same line
        if n_caps >= 3 and next_word and not is_upper_word(next_word) and len(first_line) > 60:
            findings.append({
                "pid": pid, "page": page, "n_caps": n_caps,
                "caps": " ".join(first_line.split(" ")[:n_caps]),
                "body_start": next_word,
                "line_len": len(first_line),
            })
    return findings

def main():
    total = 0
    for ch in CHAPTERS:
        fs = diag_chapter(ch)
        if fs:
            print(f"\n=== {ch}: {len(fs)} dòng tiêu đề/header dán liền body ===")
            for x in fs:
                total += 1
                print(f"  [{x['pid']} trang {x['page']}] caps={x['n_caps']} từ | "
                      f"{x['caps'][:55]!r} -> body {x['body_start']!r} (len={x['line_len']})")
    print(f"\nTỔNG: {total} trường hợp trên {len(CHAPTERS)} chương")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()