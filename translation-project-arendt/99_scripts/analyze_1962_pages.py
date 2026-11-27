# -*- coding: utf-8 -*-
"""
analyze_1962_pages.py — Tìm cấu trúc chương của PDF Meridian 1962.
"""

import fitz
import re

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

doc = fitz.open(PDF_PATH)

# Scan all pages for chapter-like headings
chapter_patterns = [
    r'PART\s+[IVXLC]+',
    r'CHAPTER\s+[IVXLC]+',
    r'C\s+H\s+A\s+P\s+T\s+E\s+R',
    r'P\s+A\s+R\s+T',
    r'PREFACE',
    r'INTRODUCTION',
    r'CONTENTS',
]

print("Scanning for structural headings across all 552 pages...\n")

for pnum in range(doc.page_count):
    page = doc[pnum]
    d = page.get_text("dict")
    
    page_texts = []
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
            sz = round(sum(s["size"] * len(s["text"]) for s in spans) / max(len(text), 1), 1)
            page_texts.append((y0, sz, text))
    
    # Sort by y position
    page_texts.sort(key=lambda x: x[0])
    
    for y0, sz, text in page_texts:
        compact = re.sub(r'\s+', '', text)
        # Check for chapter/part patterns
        if re.match(r'PART\s+[IVXLC]+', compact, re.I) or re.match(r'CHAPTER', compact, re.I):
            print(f"  Page {pnum+1:3d} y={y0:6.1f} sz={sz:5.1f} | {text[:80]}")
        elif sz >= 16.0 and len(text) < 80 and y0 < 150:
            print(f"  Page {pnum+1:3d} y={y0:6.1f} sz={sz:5.1f} (LARGE) | {text[:80]}")

doc.close()
