#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fitz
from pathlib import Path

PDF = Path("books/The_Cambridge_History_of_the_Vietnam_War.pdf")
OUT = Path("99_scripts/page27_text.txt")

doc = fitz.open(PDF)
page = doc[1262]  # Trang in 27
text = page.get_text()
OUT.write_text(text, encoding="utf-8", newline="\n")
print(f"Da ghi text trang 27 ({len(text)} ky tu) vao {OUT.name}")
print("--- 30 dong cuoi ---")
lines = text.split("\n")
for ln in lines[-30:]:
    print(repr(ln))
