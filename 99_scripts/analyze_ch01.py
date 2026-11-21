#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phân tích nguyên bản ch01.txt để xác định các đoạn (paragraph).
Ghi ket qua ra file de tranh loi encoding console.
"""
import re
from pathlib import Path

SRC = Path("translation-project/02_extracted_text/v1/ch01.txt")
raw = SRC.read_text(encoding="utf-8").replace("\r\n", "\n")
lines = raw.split("\n")

blocks = []
cur = []
for ln in lines:
    s = ln.strip()
    if s == "":
        if cur:
            blocks.append("\n".join(cur))
            cur = []
    else:
        cur.append(s)
if cur:
    blocks.append("\n".join(cur))

filtered = []
for b in blocks:
    bs = b.strip()
    if re.fullmatch(r"\d{1,3}", bs):
        continue
    if bs == "Liam C. Kelley":
        continue
    if bs.startswith("Memory, Tradition"):
        continue
    filtered.append(b)

out_lines = []
out_lines.append(f"Tong so block sau khi loc: {len(filtered)}")
out_lines.append("=" * 60)
for i, b in enumerate(filtered, 1):
    first = b.replace("\n", " ")[:100]
    m = re.search(r"\b(2[7-9]|3[0-9]|4[0-3])\b", b)
    page = m.group(1) if m else "?"
    bs = b.strip()
    is_heading = bool(re.match(r"^(Introduction|From Traditional|Historical Writings|Historical Scholarship|Anglophone Histories)", bs))
    marker = " [HEADING]" if is_heading else ""
    out_lines.append(f"P{i:02d} (trang {page}){marker}: {first}...")
out_lines.append("=" * 60)

Path("99_scripts/ch01_blocks_analysis.txt").write_text("\n".join(out_lines), encoding="utf-8", newline="\n")
print("Da ghi ket qua vao 99_scripts/ch01_blocks_analysis.txt")
