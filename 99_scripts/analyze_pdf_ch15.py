# -*- coding: utf-8 -*-
"""
analyze_pdf_ch15.py — Phân tích cấu trúc PDF chương 15 trực tiếp.
Mục tiêu: nhận diện đoạn văn, footnote, tiêu đề, hình ảnh trên mỗi trang,
để so sánh với phân đoạn hiện tại và xây dựng lại Paragraph Registry.
"""
import pymupdf, re, json, sys
from pathlib import Path

PDF = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\books\The_Cambridge_History_of_the_Vietnam_War.pdf'
OUT = r'C:\Users\PC\AppData\Local\Temp\kilo\ch15_analysis.json'

doc = pymupdf.open(PDF)

# Chương 15: PDF pages 342-362 (1-indexed)
results = []
for pdf_page in range(342, 363):
    page = doc[pdf_page - 1]
    printed = None
    for line in page.get_text("text").split("\n")[:4]:
        m = re.fullmatch(r'\s*(\d{1,4})\s*', line)
        if m:
            printed = int(m.group(1))
            break

    blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, block_type)
    blocks_sorted = sorted(blocks, key=lambda b: (b[1], b[0]))  # sort by top, then left

    page_info = {
        "pdf_page": pdf_page,
        "printed": printed,
        "blocks": []
    }

    for b in blocks_sorted:
        x0, y0, x1, y1, text, bno, btype = b
        text_clean = text.strip().replace('\n', ' ')
        if not text_clean:
            continue
        # Heuristic: footnote block = at bottom of page, small font, starts with tab+number
        is_footnote = bool(re.match(r'^\s*\d+\s', text_clean)) and y0 > 700
        is_header = y0 < 100
        is_footer = y0 > 750 and not is_footnote
        page_info["blocks"].append({
            "bbox": [round(x0,1), round(y0,1), round(x1,1), round(y1,1)],
            "text": text_clean[:200] + ("..." if len(text_clean) > 200 else ""),
            "full_len": len(text_clean),
            "is_footnote": is_footnote,
            "is_header": is_header,
            "is_footer": is_footer,
            "block_type": btype,
        })

    results.append(page_info)

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Analysis written to {OUT}")
print(f"Pages analyzed: {len(results)}")
for p in results:
    fns = [b for b in p['blocks'] if b['is_footnote']]
    print(f"PDF p{p['pdf_page']} (printed {p['printed']}): {len(p['blocks'])} blocks, {len(fns)} footnotes")

doc.close()
