# -*- coding: utf-8 -*-
"""
Xác minh sau khi sửa: parse cả 13 chương, kiểm tra
  - body không còn mở đầu bằng cụm ALL-CAPS dài (header dán liền còn sót)
  - số từ bị cắt (header) nhỏ so với tổng (không mất nội dung)
  - tiêu đề chương không lọt vào body
  - footnote markers bảo toàn
Không sửa file. UTF-8.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "99_scripts"))
sys.stdout.reconfigure(encoding="utf-8")

from docx_builder_v2.parser import parse  # noqa: E402
from docx_builder_v2.builder import TITLES  # noqa: E402

V2 = ROOT / "04_translation" / "v2"
CHAPTERS = [f"ch{i:02d}" for i in range(1, 14)]
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"

def body_nodes(model):
    return [n for n in model.nodes if n.type in ("body", "block_quote")]

def main():
    grand_removed = 0
    grand_total = 0
    problems = 0
    for ch in CHAPTERS:
        f = V2 / ch / f"v1_{ch}_vi.txt"
        text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        chap_label, vi_title = TITLES.get(ch, (ch, ch))
        model = parse(text, chapter_label=chap_label, vi_title=vi_title)
        bodies = body_nodes(model)
        joined = "\n".join(n.text for n in bodies)

        # total words (body) after strip
        total_words = sum(len(n.text.split()) for n in bodies)
        # removed words from log
        log = model.metadata.get("header_strip_log", [])
        removed = sum(len(e["removed"].split()) for e in log if e.get("removed"))

        grand_removed += removed
        grand_total += total_words

        # leftover glued caps at body start (>=4 caps words then lowercase)
        leftover = []
        for n in bodies:
            if re.match(r"^[A-ZÀ-Ỹ]{2,}(\s+[A-ZÀ-Ỹ]{2,}){3,}\s+[a-zà-ỹ]", n.text):
                leftover.append(n.text[:60])

        # chapter title leak: chỉ flag nếu body MỞ ĐẦU bằng tiêu đề (dán liền),
        # không flag khi tiêu đề xuất hiện hợp lệ giữa body.
        import unicodedata
        def norm(s):
            s = unicodedata.normalize("NFD", s.upper())
            s = "".join(c for c in s if unicodedata.category(c) != "Mn")
            return re.sub(r"[^A-Z0-9]+", " ", s).strip()
        tn = norm(vi_title) if vi_title else ""
        tl = len(tn.split()) if tn else 0
        title_leak = False
        if tn and tl >= 2:
            for n in bodies:
                head = " ".join(norm(n.text).split(" ")[:tl])
                if head == tn:
                    title_leak = True
                    break

        # footnote markers preserved count
        fn_markers = sum(joined.count(m) for m in SUP)

        status = "OK"
        if leftover or title_leak:
            status = "FAIL"
            problems += 1
        print(f"{status} {ch}: body_words={total_words:,} removed={removed} "
              f"strips={len(log)} leftover_caps={len(leftover)} title_leak={title_leak} fn_markers={fn_markers}")
        if leftover:
            for l in leftover[:2]:
                print(f"      leftover: {l!r}")

    print(f"\nTỔNG: removed={grand_removed:,} / body={grand_total:,} "
          f"({100*grand_removed/max(grand_total,1):.2f}%)  problems={problems}")
    return 0 if problems == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())