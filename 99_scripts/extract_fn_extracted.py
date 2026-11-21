#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trich xuat cuoc chu tu file 02_extracted_text/v1/ch01.txt.
Pattern: \t{N}\t text (tab + so + tab + text).
Ghi ket qua ra file.
"""
import re
from pathlib import Path

SRC = Path("translation-project/02_extracted_text/v1/ch01.txt")
OUT = Path("99_scripts/footnotes_from_extracted.txt")

raw = SRC.read_text(encoding="utf-8").replace("\r\n", "\n")
lines = raw.split("\n")

notes = []
for ln in lines:
    m = re.match(r"^\t(\d+)\t(.+)$", ln)
    if m:
        num = int(m.group(1))
        txt = m.group(2).strip()
        notes.append((num, txt))

out_lines = []
out_lines.append(f"Tong so cuoc chu tim thay: {len(notes)}")
for num, txt in notes:
    out_lines.append(f"[{num}] {txt}")

OUT.write_text("\n".join(out_lines), encoding="utf-8", newline="\n")
print(f"Da ghi {len(notes)} cuoc chu vao {OUT.name}")
