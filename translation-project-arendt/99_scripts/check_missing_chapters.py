import fitz

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

doc = fitz.open(PDF_PATH)

# Check pages where chapters might be missing
for pnum in [79, 80, 140, 141, 218, 219, 492, 493, 108, 142]:
    page = doc[pnum]
    page_num = pnum + 1
    blocks = page.get_text("blocks")
    
    print(f"\n===== PAGE {page_num} =====")
    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        if block_type != 0:
            continue
        text = text.strip()
        if not text:
            continue
        print(f"  y={y0:7.1f} x={x0:6.1f} | {text[:100]}")

doc.close()
