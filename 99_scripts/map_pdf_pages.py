#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quet toan bo PDF de tim trang in 27-43 va lay text cua tung trang.
Ghi ket qua ra file.
"""
import fitz
import re
from pathlib import Path

PDF = Path("books/The_Cambridge_History_of_the_Vietnam_War.pdf")
OUT = Path("99_scripts/pdf_page_map.txt")

doc = fitz.open(PDF)
out_lines = []
out_lines.append(f"Tong so trang PDF: {doc.page_count}")
out_lines.append("=" * 60)

page_map = {}
for i in range(doc.page_count):
    page = doc[i]
    text = page.get_text()
    # Tim so trang in (mot so 2 chu so o dau trang hoac o cuoi trang)
    # Quet tat ca dong de tim so trang
    for ln in text.split("\n"):
        m = re.match(r"^(2[7-9]|3[0-9]|4[0-3])$", ln.strip())
        if m:
            pageno = int(m.group(1))
            page_map[pageno] = i
            break

for pageno in sorted(page_map):
    idx = page_map[pageno]
    out_lines.append(f"Trang in {pageno} = PDF index {idx}")

OUT.write_text("\n".join(out_lines), encoding="utf-8", newline="\n")
print(f"Da tim {len(page_map)} trang, ghi vao {OUT.name}")
