# -*- coding: utf-8 -*-
"""In phan tail (ky tu 2000+) cua cac dong dai trong v1_ch15_src.txt."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

SRC = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch15\v1_ch15_src.txt")
OUT = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war\99_scripts\ch15_line_tails.txt")
raw = SRC.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
lines = raw.split("\n")

out = []
count = 0
for i, ln in enumerate(lines, 1):
    if len(ln) > 2000:
        count += 1
        out.append(f"\n===== DONG {i} (do dai {len(ln)}) TAIL tu ky tu 2000 =====")
        out.append(ln[2000:])
        out.append(f"\n===== HET DONG {i} TAIL =====\n")

OUT.write_text("\n".join(out), encoding="utf-8")
print(f"Da dump tail cua {count} dong dai vao {OUT}")
