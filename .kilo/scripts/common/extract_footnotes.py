#!/usr/bin/env python3
"""
Extract footnotes from all Vietnamese chapters and English PDF.
"""

import re
from pathlib import Path
import fitz

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUP_MAP = {c: str(i) for i, c in enumerate(SUP)}

CHAPTER_START_PAGES = {
    1: 23, 2: 31, 3: 75, 4: 109, 5: 143, 6: 179, 7: 205,
    8: 243, 9: 287, 10: 325, 11: 361, 12: 409, 13: 481
}

def parse_paragraphs(text: str):
    pattern = r'(\[V1[^\]]+\]\s*\(trang\s+\d+\))'
    parts = re.split(pattern, text)
    paragraphs = []
    current_id = None
    current_page = None
    current_text = ""
    
    for part in parts:
        if re.match(pattern, part.strip()):
            if current_id and current_text.strip():
                paragraphs.append({
                    "id": current_id,
                    "page": current_page,
                    "text": current_text.strip()
                })
            match = re.match(r'\[(V1[^\]]+)\]\s*\(trang\s+(\d+)\)', part.strip())
            if match:
                current_id = match.group(1)
                current_page = int(match.group(2))
                current_text = ""
        else:
            current_text += part
    
    if current_id and current_text.strip():
        paragraphs.append({
            "id": current_id,
            "page": current_page,
            "text": current_text.strip()
        })
    return paragraphs

def extract_vi_footnotes(text: str):
    """Extract footnotes from Vietnamese inline superscript format."""
    paragraphs = parse_paragraphs(text)
    all_footnotes = {}
    clean_paragraphs = []
    
    for para in paragraphs:
        text = para['text']
        fn_pattern = r'([' + SUP + r']+)'
        matches = list(re.finditer(fn_pattern, text))
        
        if not matches:
            clean_paragraphs.append(para)
            continue
        
        last_end = 0
        clean_text = ""
        for i, m in enumerate(matches):
            sup = m.group()
            num = ''.join(SUP_MAP[c] for c in sup)
            fn_start = m.end()
            fn_end = matches[i+1].start() if i+1 < len(matches) else len(text)
            fn_content = text[fn_start:fn_end].strip()
            fn_content = re.sub(r'^[\s\.\,\;\:]+', '', fn_content)
            fn_content = re.sub(r'[\s\.\,\;\:]+$', '', fn_content)
            
            clean_text += text[last_end:m.start()]
            clean_text += sup
            
            if fn_content and num not in all_footnotes:
                all_footnotes[num] = fn_content
            
            last_end = fn_end
        
        clean_text += text[last_end:]
        para['text'] = clean_text.strip()
        clean_paragraphs.append(para)
    
    # Rebuild text
    output = []
    for para in clean_paragraphs:
        output.append(f"[{para['id']}] (trang {para['page']})")
        output.append(para['text'])
        output.append("")
    
    return "\n".join(output).strip() + "\n", all_footnotes

def extract_en_footnotes_from_pdf(chapter: int):
    """Extract footnotes from PDF for a chapter."""
    pdf_path = Path("books/hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf")
    doc = fitz.open(pdf_path)
    start_page = CHAPTER_START_PAGES[chapter] - 1  # 0-indexed
    end_page = CHAPTER_START_PAGES.get(chapter + 1, doc.page_count) - 1
    
    footnotes = {}
    fn_pattern = re.compile(r'\^\^(\d+)\^\^\s*(.+?)(?=\^\^\d+\^\^|$)')
    
    for page_num in range(start_page, min(end_page + 1, doc.page_count)):
        page = doc[page_num]
        text = page.get_text()
        # Look for ^^N^^ footnote markers
        for match in fn_pattern.finditer(text):
            num = match.group(1)
            content = match.group(2).strip()
            if content and num not in footnotes:
                footnotes[num] = content
    
    doc.close()
    return footnotes

def process_chapter(chapter: int, volume: str = "v2"):
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    
    # Process Vietnamese
    vi_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi.txt"
    vi_text = vi_file.read_text(encoding='utf-8')
    clean_text, vi_footnotes = extract_vi_footnotes(vi_text)
    
    # Save clean VI text
    clean_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_clean.txt"
    clean_file.write_text(clean_text, encoding='utf-8')
    
    # Extract English footnotes from PDF
    en_footnotes = extract_en_footnotes_from_pdf(chapter)
    
    print(f"Chapter {chapter}: VI footnotes={len(vi_footnotes)}, EN footnotes={len(en_footnotes)}")
    
    return vi_footnotes, en_footnotes

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        chapter = int(sys.argv[1])
        process_chapter(chapter)
    else:
        for ch in range(1, 14):
            process_chapter(ch)