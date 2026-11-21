#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ghep cac dong cuoc chu bi cat tu file 02_extracted_text/v1/ch01.txt.
Pattern bat dau: \t{N}\t (tab + so + tab)
Cac dong tiep theo khong co pattern nay la phan tiep theo cua cuoc chu hien tai.
Ghi ket qua ra file.
"""
import re
from pathlib import Path

SRC = Path("translation-project/02_extracted_text/v1/ch01.txt")
OUT = Path("99_scripts/footnotes_full.txt")

raw = SRC.read_text(encoding="utf-8").replace("\r\n", "\n")
lines = raw.split("\n")

fn_start = re.compile(r"^\t(\d+)\t(.+)$")
current_num = None
current_text = None
notes = []

for ln in lines:
    m = fn_start.match(ln)
    if m:
        # Luu cuoc chu cu (neu co)
        if current_num is not None:
            notes.append((current_num, current_text))
        current_num = int(m.group(1))
        current_text = m.group(2).strip()
    else:
        # Dong tiep theo (khong co pattern \tN\t) -> phan tiep theo cua cuoc chu hien tai
        if current_num is not None and ln.strip():
            # Chi noi neu dong khong la trang so hoac header/footer
            s = ln.strip()
            if not re.fullmatch(r"\d{1,3}", s) and s != "Liam C. Kelley" and not s.startswith("Memory, Tradition"):
                current_text += " " + s

# Luu cuoc chu cuoi cung
if current_num is not None:
    notes.append((current_num, current_text))

# Sap xep theo so
notes.sort(key=lambda x: x[0])

out_lines = []
out_lines.append(f"Tong so cuoc chu: {len(notes)}")
for num, txt in notes:
    out_lines.append(f"[{num}] {txt}")

OUT.write_text("\n".join(out_lines), encoding="utf-8", newline="\n")
print(f"Da ghi {len(notes)} cuoc chu day du vao {OUT.name}")
