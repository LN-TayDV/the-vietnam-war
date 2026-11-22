from docx import Document
from pathlib import Path

docx_path = Path("C:/Users/PC/Documents/AI_project/the-vietnam-war/translation-project/09_docx/V1-C10_The-French-Indochina-War-Dong-Duong-in-Northern-Vietnam.docx")
doc = Document(docx_path)

with open("C:/Users/PC/Documents/AI_project/the-vietnam-war/ch10_docx_structure.txt", "w", encoding="utf-8") as out:
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        style = p.style.name if p.style else "None"
        size = None
        bold = None
        italic = None
        for run in p.runs:
            if run.font.size:
                size = run.font.size.pt
            if run.font.bold is not None:
                bold = run.font.bold
            if run.font.italic is not None:
                italic = run.font.italic
            break
        out.write(f"P{i:3d} | {style:20s} | sz={str(size):5s} | b={str(bold):5s} | i={str(italic):5s} | {text[:120]}\n")
    
    out.write(f"\n=== IMAGES ===\n")
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            out.write(f"  {rel.target_ref}\n")

print("Done")