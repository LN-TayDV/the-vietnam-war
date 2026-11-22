from docx import Document
from pathlib import Path
import json

docx_dir = Path("C:/Users/PC/Documents/AI_project/the-vietnam-war/translation-project/09_docx")

files = [
    "V1-C01_Tri-nho-Truyen-thong-va-Su-hoc-ve-Viet-Nam.docx",
    "V1-C02_The-Origins-of-the-Vietnamese-Revolution.docx",
    "V1-C03_Ho-Chi-Minh-va-Su-Noi-Len-cua-Dang-Cong-San-Viet-Nam.docx",
    "V1-C04_Dong-Duong-trong-Chien-tranh-The-gioi-Thu-hai.docx",
    "V1-C05_Cach-mang-Thang-Tam-nam-1945.docx",
    "V1-C06_The-Birth-of-the-Democratic-Republic-of-Vietnam.docx",
    "V1-C07_Chien-tranh-Dong-Duong-cua-Phap.docx",
    "V1-C08_Trung-Quoc-va-Chien-tranh-Dong-Duong.docx",
    "V1-C09_The-French-Indochina-War-in-the-Central-Highlands.docx",
    "V1-C10_The-French-Indochina-War-Dong-Duong-in-Northern-Vietnam.docx",
]

results = []

for fname in files:
    path = docx_dir / fname
    doc = Document(path)
    
    chapter_title = ""
    chapter_num = ""
    for p in doc.paragraphs:
        text = p.text.strip()
        if text.startswith("CHƯƠNG"):
            chapter_num = text
        elif chapter_num and text and not text.startswith("THE CAMBRIDGE") and not text.startswith("TẬP I") and not text.startswith("Christopher") and not text.startswith("Chen") and not text.startswith("Pierre") and not text.startswith("Edward") and not text.startswith("Peng") and not text.startswith("Goscha"):
            chapter_title = text
            break
    
    results.append({
        "file": fname,
        "chapter_num": chapter_num,
        "title": chapter_title
    })

with open("C:/Users/PC/Documents/AI_project/the-vietnam-war/docx_titles_check.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done - saved to docx_titles_check.json")