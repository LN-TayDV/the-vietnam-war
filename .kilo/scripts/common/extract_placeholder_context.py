#!/usr/bin/env python3
"""
Extract Vietnamese body context for placeholder footnotes to aid translation.
"""

import re
from pathlib import Path

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUP_MAP = {c: str(i) for i, c in enumerate(SUP)}
# Double superscripts
DOUBLE_SUP = {
    '¹⁰': '10', '¹¹': '11', '¹²': '12', '¹³': '13', '¹⁴': '14',
    '¹⁵': '15', '¹⁶': '16', '¹⁷': '17', '¹⁸': '18', '¹⁹': '19',
    '²⁰': '20', '²¹': '21', '²²': '22', '²³': '23', '²⁴': '24',
    '²⁵': '25', '²⁶': '26', '²⁷': '27', '²⁸': '28', '²⁹': '29',
    '³⁰': '30', '³¹': '31', '³²': '32', '³³': '33', '³⁴': '34',
    '³⁵': '35', '³⁶': '36', '³⁷': '37', '³⁸': '38', '³⁹': '39',
    '⁴⁰': '40', '⁴¹': '41', '⁴²': '42', '⁴³': '43', '⁴⁴': '44',
    '⁴⁵': '45', '⁴⁶': '46', '⁴⁷': '47', '⁴⁸': '48', '⁴⁹': '49',
    '⁵⁰': '50',
}

def parse_vi_paragraphs(text: str):
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

def find_footnote_contexts(chapter: int, volume: str = "v2"):
    """Find Vietnamese body context for each footnote number."""
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    vi_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi.txt"
    vi_text = vi_file.read_text(encoding='utf-8')
    
    # Parse paragraphs
    paragraphs = parse_vi_paragraphs(vi_text)
    
    # Find all superscript markers with their context
    footnote_contexts = {}
    
    for para in paragraphs:
        text = para['text']
        
        # Single superscripts
        for m in re.finditer(r'[' + SUP + r']', text):
            sup = m.group()
            num = SUP_MAP[sup]
            start = max(0, m.start() - 150)
            end = min(len(text), m.end() + 150)
            context = text[start:end].strip()
            if num not in footnote_contexts:
                footnote_contexts[num] = []
            footnote_contexts[num].append({
                "para_id": para['id'],
                "page": para['page'],
                "context": context
            })
        
        # Double superscripts
        for ds, num in DOUBLE_SUP.items():
            for m in re.finditer(re.escape(ds), text):
                start = max(0, m.start() - 150)
                end = min(len(text), m.end() + 150)
                context = text[start:end].strip()
                if num not in footnote_contexts:
                    footnote_contexts[num] = []
                footnote_contexts[num].append({
                    "para_id": para['id'],
                    "page": para['page'],
                    "context": context
                })
        
        # Bracket format [N]
        for m in re.finditer(r'\[(\d+)\]', text):
            num = m.group(1)
            start = max(0, m.start() - 150)
            end = min(len(text), m.end() + 150)
            context = text[start:end].strip()
            if num not in footnote_contexts:
                footnote_contexts[num] = []
            footnote_contexts[num].append({
                "para_id": para['id'],
                "page": para['page'],
                "context": context
            })
    
    return footnote_contexts

def get_placeholder_numbers(chapter: int, volume: str = "v2"):
    """Get placeholder footnote numbers from realigned file."""
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_realigned.txt"
    with open(file) as f:
        text = f.read()
    
    if '=== FOOTNOTES ===' not in text:
        return []
    
    fn_section = text.split('=== FOOTNOTES ===')[1]
    placeholders = []
    for line in fn_section.strip().split('\n'):
        if 'cước chú' in line and 'tham chiếu' in line:
            # Extract footnote number from [N] [cước chú M...]
            match = re.match(r'\[(\d+)\]\s*\[cước chú\s+(\d+)', line)
            if match:
                placeholders.append((int(match.group(1)), int(match.group(2))))
    return placeholders

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        chapters = [int(sys.argv[1])]
    else:
        chapters = [2, 3, 5, 12, 13]
    
    for ch in chapters:
        print(f"\n=== Chapter {ch} ===")
        placeholders = get_placeholder_numbers(ch)
        contexts = find_footnote_contexts(ch)
        
        for list_num, ref_num in placeholders:
            print(f"\n  Placeholder [{list_num}] -> references footnote {ref_num}")
            if str(ref_num) in contexts:
                for ctx in contexts[str(ref_num)][:1]:  # First context
                    print(f"    Body context (para {ctx['para_id']}, page {ctx['page']}):")
                    print(f"      ...{ctx['context']}...")
            else:
                print(f"    NO BODY CONTEXT FOUND for footnote {ref_num}")