from docx import Document
from pathlib import Path
import json

docx_dir = Path("C:/Users/PC/Documents/AI_project/the-vietnam-war/translation-project/09_docx")

updates = {
    "V1-C03_Ho-Chi-Minh-va-Su-Noi-Len-cua-Dang-Cong-San-Viet-Nam.docx": 
        "Hồ Chí Minh và Sự Nổi Dậy của Đảng Cộng sản Việt Nam",
    "V1-C06_The-Birth-of-the-Democratic-Republic-of-Vietnam.docx": 
        "Sự Ra Đời của Cộng hòa Dân chủ Việt Nam",
    "V1-C09_The-French-Indochina-War-in-the-Central-Highlands.docx": 
        "Chiến tranh Đông Dương của Pháp ở Cao nguyên Trung phần",
    "V1-C10_The-French-Indochina-War-Dong-Duong-in-Northern-Vietnam.docx": 
        "Chiến tranh Đông Dương của Pháp ở Bắc Việt Nam",
}

already_vi = [
    "V1-C01_Tri-nho-Truyen-thong-va-Su-hoc-ve-Viet-Nam.docx",
    "V1-C02_The-Origins-of-the-Vietnamese-Revolution.docx",
    "V1-C04_Dong-Duong-trong-Chien-tranh-The-gioi-Thu-hai.docx",
    "V1-C05_Cach-mang-Thang-Tam-nam-1945.docx",
    "V1-C07_Chien-tranh-Dong-Duong-cua-Phap.docx",
    "V1-C08_Trung-Quoc-va-Chien-tranh-Dong-Duong.docx",
]

results = []

for fname, new_title in updates.items():
    path = docx_dir / fname
    doc = Document(path)
    
    old_title = ""
    chapter_num = ""
    title_para_idx = -1
    
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text.startswith("CHƯƠNG"):
            chapter_num = text
        elif chapter_num and text and not text.startswith("THE CAMBRIDGE") and not text.startswith("TẬP I") and not text.startswith("Christopher") and not text.startswith("Chen") and not text.startswith("Pierre") and not text.startswith("Edward") and not text.startswith("Peng") and not text.startswith("Goscha"):
            old_title = text
            title_para_idx = i
            break
    
    if title_para_idx >= 0:
        p = doc.paragraphs[title_para_idx]
        for run in p.runs:
            run.text = ""
        if p.runs:
            p.runs[0].text = new_title
        else:
            run = p.add_run(new_title)
        doc.save(path)
        status = "Đã cập nhật"
    else:
        status = "Không tìm thấy tiêu đề"
    
    results.append({
        "file": fname,
        "old_title": old_title,
        "new_title": new_title,
        "status": status
    })

for fname in already_vi:
    path = docx_dir / fname
    doc = Document(path)
    old_title = ""
    chapter_num = ""
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text.startswith("CHƯƠNG"):
            chapter_num = text
        elif chapter_num and text and not text.startswith("THE CAMBRIDGE") and not text.startswith("TẬP I") and not text.startswith("Christopher") and not text.startswith("Chen") and not text.startswith("Pierre") and not text.startswith("Edward") and not text.startswith("Peng") and not text.startswith("Goscha"):
            old_title = text
            break
    results.append({
        "file": fname,
        "old_title": old_title,
        "new_title": old_title,
        "status": "Đã là tiếng Việt, giữ nguyên"
    })

with open("C:/Users/PC/Documents/AI_project/the-vietnam-war/title_update_report.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done")