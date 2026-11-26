# -*- coding: utf-8 -*-
"""Dump cac dong dai (>1800 ky tu) trong v1_ch15_src.txt de doc day du, khong bi truncate."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

SRC = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch15\v1_ch15_src.txt")
OUT = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war\99_scripts\ch15_long_lines.txt")
raw = SRC.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
lines = raw.split("\n")

out = []
for i, ln in enumerate(lines, 1):
    if len(ln) > 1800:
        out.append(f"\n===== DONG {i} (do dai {len(ln)}) =====")
        out.append(ln)
        out.append(f"\n===== HET DONG {i} =====\n")

OUT.write_text("\n".join(out), encoding="utf-8")
print(f"Da dump {sum(1 for ln in lines if len(ln)>1800)} dong dai vao {OUT}")
