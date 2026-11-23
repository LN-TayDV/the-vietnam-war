# -*- coding: utf-8 -*-
import re
from pathlib import Path

root = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war")
src = (root/"translation-project/04_translation/v1/ch13/v1_ch13_src.txt").read_text(encoding="utf-8")

lines = src.split("\n")
# Identify footnote citation lines: pattern ^\s+\d+\t  (space(s) + digits + TAB)
fn_start = re.compile(r"^\s+\d+\t")
# Print lines that look like footnote starts to understand structure
print("=== Lines matching footnote-citation start (space+digits+TAB) ===")
for i, ln in enumerate(lines, 1):
    if fn_start.match(ln):
        print(i, repr(ln[:90]))
print("\n=== Lines that are pure tab/whitespace ===")
for i, ln in enumerate(lines,1):
    if ln.strip()=="" and ln!="":
        print(i, repr(ln))