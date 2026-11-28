#!/usr/bin/env python3
"""
Add extracted Vietnamese footnotes to realigned files (from original VI).
"""

import re
from pathlib import Path

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUP_MAP = {c: str(i) for i, c in enumerate(SUP)}

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
    paragraphs = parse_paragraphs(text)
    all_footnotes = {}
    
    for para in paragraphs:
        text = para['text']
        fn_pattern = r'([' + SUP + r']+)'
        matches = list(re.finditer(fn_pattern, text))
        
        if not matches:
            continue
        
        for i, m in enumerate(matches):
            sup = m.group()
            num = ''.join(SUP_MAP[c] for c in sup)
            fn_start = m.end()
            fn_end = matches[i+1].start() if i+1 < len(matches) else len(text)
            fn_content = text[fn_start:fn_end].strip()
            fn_content = re.sub(r'^[\s\.\,\;\:]+', '', fn_content)
            fn_content = re.sub(r'[\s\.\,\;\:]+$', '', fn_content)
            
            if fn_content and num not in all_footnotes:
                all_footnotes[num] = fn_content
    
    return all_footnotes

def add_footnotes_to_realigned(chapter: int, volume: str = "v2"):
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    
    # Load ORIGINAL VI text to extract footnotes
    vi_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi.txt"
    vi_text = vi_file.read_text(encoding='utf-8')
    footnotes = extract_vi_footnotes(vi_text)
    
    # Load realigned file
    realigned_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_realigned.txt"
    realigned_text = realigned_file.read_text(encoding='utf-8')
    
    # Remove any existing footnotes section
    if "=== FOOTNOTES ===" in realigned_text:
        realigned_text = realigned_text.split("=== FOOTNOTES ===")[0].rstrip()
    
    # Add footnotes section
    if footnotes:
        realigned_text += "\n\n=== FOOTNOTES ===\n"
        for num in sorted(footnotes.keys(), key=int):
            realigned_text += f"[{num}] {footnotes[num]}\n"
    
    # Save updated realigned file
    realigned_file.write_text(realigned_text + "\n", encoding='utf-8')
    
    print(f"Chapter {chapter}: Added {len(footnotes)} footnotes to realigned file")
    
    return footnotes

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        chapter = int(sys.argv[1])
        add_footnotes_to_realigned(chapter)
    else:
        for ch in range(1, 14):
            add_footnotes_to_realigned(ch)