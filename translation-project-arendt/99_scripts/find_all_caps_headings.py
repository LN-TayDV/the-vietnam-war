import fitz
import re

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

doc = fitz.open(PDF_PATH)

print("Searching for all-caps headings at top of pages (potential chapter starts)...\n")

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
        # Only look at blocks near top of page (y < 60)
        if y0 > 60:
            continue
        # All caps heading (mostly uppercase, short)
        compact = re.sub(r'\s+', '', text)
        if len(compact) > 3 and len(compact) < 60:
            upper_ratio = sum(1 for c in compact if c.isupper()) / max(len(compact), 1)
            if upper_ratio > 0.8 and not re.match(r'^CHAPTER', compact, re.I):
                print(f"  Page {page_num:3d} y={y0:6.1f} x={x0:6.1f} | {text[:80]}")

doc.close()
