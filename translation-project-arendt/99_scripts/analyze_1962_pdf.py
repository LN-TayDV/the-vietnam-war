# -*- coding: utf-8 -*-
"""
analyze_1962_pdf.py — Phân tích cấu trúc PDF Meridian 1962 trước khi trích xuất toàn bộ.
"""

import fitz
import os
import json
import unicodedata

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

doc = fitz.open(PDF_PATH)
print(f"PDF: {doc.page_count} pages")
print(f"Metadata: {doc.metadata}")
print()

# Sample first 10 pages to understand structure
for pnum in range(min(10, doc.page_count)):
    page = doc[pnum]
    d = page.get_text("dict")
    print(f"\n===== PAGE {pnum+1} (index {pnum}) =====")
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
