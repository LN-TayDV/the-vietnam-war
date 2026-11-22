from docx import Document
from pathlib import Path

docx_dir = Path("C:/Users/PC/Documents/AI_project/the-vietnam-war/translation-project/09_docx")

files_to_check = [
    "V1-C03_Ho-Chi-Minh-va-Su-Noi-Len-cua-Dang-Cong-San-Viet-Nam.docx",
    "V1-C06_The-Birth-of-the-Democratic-Republic-of-Vietnam.docx",
    "V1-C09_The-French-Indochina-War-in-the-Central-Highlands.docx",
    "V1-C10_The-French-Indochina-War-Dong-Duong-in-Northern-Vietnam.docx",
]

with open("C:/Users/PC/Documents/AI_project/the-vietnam-war/format_check.txt", "w", encoding="utf-8") as out:
    for fname in files_to_check:
        path = docx_dir / fname
        doc = Document(path)
        
        out.write(f"\n=== {fname} ===\n")
        for i, p in enumerate(doc.paragraphs[:15]):
            text = p.text.strip()[:80]
            style = p.style.name if p.style else "None"
            size = None
            bold = None
            italic = None
            align = p.alignment
            for run in p.runs:
                if run.font.size:
                    size = run.font.size.pt
                if run.font.bold is not None:
                    bold = run.font.bold
                if run.font.italic is not None:
                    italic = run.font.italic
                break
            out.write(f"  P{i:2d} | {style:15s} | sz={size} | b={bold} | i={italic} | al={str(align):5s} | {text}\n")

print("Format check saved to format_check.txt")