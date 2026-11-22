from docx import Document

doc = Document("translation-project/09_docx/V1-C10_The-French-Indochina-War-Dong-Duong-in-Northern-Vietnam.docx")

with open("docx_check.txt", "w", encoding="utf-8") as f:
    f.write("=== ALL PARAGRAPHS ===\n")
    for i, p in enumerate(doc.paragraphs):
        text = p.text[:150]
        style = p.style.name if p.style else "None"
        align = p.alignment
        size = None
        italic = None
        for run in p.runs:
            if run.font.size:
                size = run.font.size.pt
            if run.font.italic is not None:
                italic = run.font.italic
                break
        has_img = any('blip' in run._element.xml for run in p.runs)
        f.write(f"P{i:3d} | {style:15s} | sz={size} | it={str(italic):5s} | al={str(align):5s} | img={has_img} | {text}\n")