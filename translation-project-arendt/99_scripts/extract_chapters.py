import fitz
import os

doc = fitz.open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\books\Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf')

output_dir = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\02_extracted_text\v1"
os.makedirs(output_dir, exist_ok=True)

# Chapter page ranges (1-indexed page numbers)
chapters = [
    ("front_matter", 1, 7),
    ("preface_first_edition", 8, 10),
    ("preface_part_one", 11, 16),
    ("preface_part_two", 17, 22),
    ("preface_part_three", 23, 41),
    ("part_one_intro", 42, 47),
    ("ch01", 48, 55),
    ("ch02", 56, 98),
    ("ch03", 99, 133),
    ("ch04", 134, 167),
    ("ch05", 168, 202),
    ("ch06", 203, 229),
    ("ch07", 230, 266),
    ("ch08", 267, 311),
    ("ch09", 312, 349),
    ("ch10", 350, 387),
    ("ch11", 388, 433),
    ("ch12", 434, 504),
    ("ch13", 505, 574),
]

for name, start, end in chapters:
    text_parts = []
    for i in range(start - 1, min(end, doc.page_count)):
        text = doc[i].get_text()
        text_parts.append(f"=== PAGE {i+1} ===\n{text}")
    
    full_text = "\n\n".join(text_parts)
    output_path = os.path.join(output_dir, f"{name}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Saved {name}: pages {start}-{end} ({len(full_text)} chars)")

print("Extraction complete!")