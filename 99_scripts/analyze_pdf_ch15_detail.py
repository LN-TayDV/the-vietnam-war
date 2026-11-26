# -*- coding: utf-8 -*-
"""
analyze_pdf_ch15_detail.py — In chi tiết các block của mỗi trang chương 15.
Ghi ra file UTF-8 để tránh lỗi console encoding.
"""
import pymupdf, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PDF = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\books\The_Cambridge_History_of_the_Vietnam_War.pdf'

doc = pymupdf.open(PDF)

out = open(r'C:\Users\PC\AppData\Local\Temp\kilo\ch15_detail.txt', 'w', encoding='utf-8')

for pdf_page in range(342, 363):
    page = doc[pdf_page - 1]
    printed = None
    for line in page.get_text("text").split("\n")[:4]:
        m = re.fullmatch(r'\s*(\d{1,4})\s*', line)
        if m:
            printed = int(m.group(1))
            break

    blocks = page.get_text("blocks")
    blocks_sorted = sorted(blocks, key=lambda b: (b[1], b[0]))

    out.write(f"\n{'='*80}\n")
    out.write(f"PDF p{pdf_page} (printed {printed}) - {len(blocks_sorted)} blocks\n")
    out.write(f"{'='*80}\n")

    for i, b in enumerate(blocks_sorted):
        x0, y0, x1, y1, text, bno, btype = b
        text_clean = text.strip().replace('\n', ' | ')
        if len(text_clean) > 200:
            text_clean = text_clean[:200] + "..."
        fn_marker = ""
        m = re.match(r'^(\d+)\t', text.strip())
        if m:
            fn_marker = f" [FN*{m.group(1)}*]"
        pos = ""
        if y0 < 100:
            pos = " [HEADER]"
        elif y0 > 700:
            pos = " [BOTTOM]"
        out.write(f"  [{i}] y0={y0:7.1f} y1={y1:7.1f} x0={x0:7.1f} type={btype}{fn_marker}{pos}: {text_clean}\n")

out.close()
doc.close()
print("Done - wrote to ch15_detail.txt")
