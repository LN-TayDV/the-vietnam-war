#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trich xuat cuoc chu tu PDF trang 27-43 (PDF index 42-58).
Tim pattern '[N] ' hoac '\tN\t' o cuoi moi trang.
Ghi ket qua ra file.
"""
import fitz
import re
from pathlib import Path

PDF = Path("books/The_Cambridge_History_of_the_Vietnam_War.pdf")
OUT = Path("99_scripts/footnotes_from_pdf_v2.txt")

doc = fitz.open(PDF)

page_map = {27: 42}
for p in range(28, 44):
    page_map[p] = 42 + (p - 27)

all_notes = {}
for pageno, idx in page_map.items():
    page = doc[idx]
    text = page.get_text()
    lines = text.split("\n")
    notes_on_page = []
    for ln in lines:
        s = ln.strip()
        # Pattern [N] text hoac \tN\t text
        m = re.match(r"^\[(\d+)\]\s+(.+)$", s)
        if not m:
            m = re.match(r"^\t(\d+)\t(.+)$", s)
        if m:
            num = int(m.group(1))
            txt = m.group(2).strip()
            notes_on_page.append((num, txt))
    if notes_on_page:
        all_notes[pageno] = notes_on_page

out_lines = []
out_lines.append(f"Tong so trang co cuoc chu: {len(all_notes)}")
total = 0
for pageno in sorted(all_notes):
    out_lines.append(f"--- Trang {pageno} ---")
    for num, txt in all_notes[pageno]:
        out_lines.append(f"  [{num}] {txt}")
        total += 1
out_lines.append(f"Tong so cuoc chu: {total}")

OUT.write_text("\n".join(out_lines), encoding="utf-8", newline="\n")
print(f"Da ghi {total} cuoc chu tu {len(all_notes)} trang vao {OUT.name}")
