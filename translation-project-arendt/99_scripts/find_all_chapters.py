import fitz
import re

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

doc = fitz.open(PDF_PATH)

print("Searching for all CHAPTER headings across 552 pages...\n")

for pnum in range(doc.page_count):
    page = doc[pnum]
    page_num = pnum + 1
    blocks = page.get_text("blocks")
    
    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        if block_type != 0:
            continue
        text = text.strip()
        if not text:
            continue
        # Check if block starts with CHAPTER
        if re.match(r'^CHAPTER\s', text, re.I):
            print(f"  Page {page_num:3d} y={y0:6.1f} x={x0:6.1f} | {text[:80]}")

doc.close()
