# -*- coding: utf-8 -*-
"""Phân tích cấu trúc src ch15.txt: tách block, phân loại thân/chú thích/hình/đề mục."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
import re

SRC = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch15\v1_ch15_src.txt")
raw = SRC.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
lines = raw.split("\n")

# Tách block theo header: --- [V1C15-PNNN] (trang Z) — label ---
BLOCK_HDR = re.compile(r"^\[(V1C15-P\d+)\] \(trang ([^)]+)\)(?: — (.*?))? ---$")

blocks = []
cur = None
buf = []
for ln in lines:
    m = BLOCK_HDR.match(ln)
    if m:
        if cur is not None:
            cur["body"] = "\n".join(buf)
            blocks.append(cur)
        cur = {"id": m.group(1), "page": m.group(2), "label": (m.group(3) or "").strip(), "buf": []}
        buf = []
    else:
        buf.append(ln)
if cur is not None:
    cur["body"] = "\n".join(buf)
    blocks.append(cur)

print(f"Tổng số block: {len(blocks)}")
from collections import Counter
labels = Counter(b["label"] for b in blocks)
print("Phân bố label:", dict(labels))

for i, b in enumerate(blocks):
    first = " ".join(b["body"].split())[:90]
    print(f"{i+1:3d} {b['id']:12s} trang={b['page']:>4s} label={b['label']:<18s} | {first}")
