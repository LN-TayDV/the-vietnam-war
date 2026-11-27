# -*- coding: utf-8 -*-
"""
analyze_running_headers.py — Phân tích running headers và page furniture trên 552 trang PDF Meridian 1962.
"""

import fitz
import os
import re
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
OUT_DIR = os.path.join(BASE, "01_raw_text", "meridian_1962_analysis")
os.makedirs(OUT_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)
total_pages = doc.page_count
print(f"PDF: {total_pages} pages")

from collections import Counter
header_candidates = Counter()
page_number_candidates = Counter()
all_page_data = []

for pnum in range(total_pages):
    page = doc[pnum]
    page_num = pnum + 1
    blocks = page.get_text("blocks")
    ph = page.rect.height
    pw = page.rect.width

    page_info = {
        "page": page_num,
        "header_lines": [],
        "footer_lines": [],
        "body_lines": [],
        "footnote_lines": [],
        "page_number": None,
    }

    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        if block_type != 0:
            continue
        text = text.strip()
        if not text:
            continue
        text = re.sub(r'\s+', ' ', text)

        if y0 < 60:
            page_info["header_lines"].append({"y": round(y0,1), "x": round(x0,1), "text": text})
            header_candidates[text] += 1
        elif y0 > ph - 60:
            page_info["footer_lines"].append({"y": round(y0,1), "x": round(x0,1), "text": text})
        else:
            if re.match(r'^\d+$', text) and (x0 < 60 or x0 > pw - 90):
                page_info["page_number"] = text
                page_number_candidates[text] += 1
            else:
                page_info["body_lines"].append({"y": round(y0,1), "x": round(x0,1), "text": text})

    all_page_data.append(page_info)

doc.close()

print("\n=== HEADER CANDIDATES (appearing >= 3 times) ===")
for text, count in header_candidates.most_common(30):
    print(f"  {count:3d}x | {text[:100]}")

print(f"\n=== TOTAL UNIQUE HEADER LINES: {len(header_candidates)} ===")

analysis = {
    "total_pages": total_pages,
    "header_candidates": {k: v for k, v in header_candidates.most_common()},
    "page_number_candidates": dict(page_number_candidates),
    "page_data": all_page_data,
}

with open(os.path.join(OUT_DIR, "header_analysis.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

print(f"\nSaved analysis to: {OUT_DIR}/header_analysis.json")

doc2 = fitz.open(PDF_PATH)
print("\n=== DETAIL SAMPLE PAGES ===")
for pnum in [0, 22, 30, 108, 142, 204, 286, 324, 360, 408, 480]:
    page = doc2[pnum]
    page_num = pnum + 1
    blocks = page.get_text("blocks")
    ph = page.rect.height
    print(f"\n--- PAGE {page_num} ---")
    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        if block_type != 0:
            continue
        text = text.strip()
        if not text:
            continue
        text = re.sub(r'\s+', ' ', text)
        marker = "HEADER" if y0 < 60 else ("FOOTER" if y0 > ph - 60 else "BODY")
        print(f"  {marker:8s} y={y0:6.1f} x={x0:6.1f} | {text[:90]}")
doc2.close()
