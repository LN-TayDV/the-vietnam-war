#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fitz
from pathlib import Path

PDF = Path("books/The_Cambridge_History_of_the_Vietnam_War.pdf")
OUT = Path("99_scripts/page27_v2_text.txt")

doc = fitz.open(PDF)
page = doc[42]  # Trang in 27
text = page.get_text()
OUT.write_text(text, encoding="utf-8", newline="\n")
print(f"Da ghi text trang 27 ({len(text)} ky tu) vao {OUT.name}")
lines = text.split("\n")
print(f"So dong: {len(lines)}")
print("--- 40 dong cuoi ---")
for ln in lines[-40:]:
    print(repr(ln))
