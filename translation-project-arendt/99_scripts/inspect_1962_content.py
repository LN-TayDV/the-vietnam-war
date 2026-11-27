# -*- coding: utf-8 -*-
"""
inspect_1962_content.py — Kiểm tra layout trang nội dung của Meridian 1962.
"""

import fitz

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

doc = fitz.open(PDF_PATH)

# Check pages around chapter starts
for pnum in [16, 20, 22, 140, 142, 322, 324]:
    page = doc[pnum]
    d = page.get_text("dict")
    print(f"\n===== PAGE {pnum+1} =====")
    for block in d["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            spans = line["spans"]
            if not spans:
                continue
            text = "".join(s["text"] for s in spans).strip()
            if not text:
                continue
            y0 = min(s["bbox"][1] for s in spans)
            x0 = min(s["bbox"][0] for s in spans)
            sz = round(sum(s["size"] * len(s["text"]) for s in spans) / max(len(text), 1), 1)
            print(f"  y={y0:7.1f} x={x0:6.1f} sz={sz:5.1f} | {text[:100]}")

doc.close()
