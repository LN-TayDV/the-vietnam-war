#!/usr/bin/env python3
"""
Update realigned files: Replace placeholder footnotes with context-rich markers for human translation.
"""

import re
from pathlib import Path

def update_placeholder_footnotes(chapter: int, volume: str = "v2"):
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_realigned.txt"
    
    with open(file, encoding='utf-8') as f:
        text = f.read()
    
    if '=== FOOTNOTES ===' not in text:
        print(f"Ch{chapter}: No footnotes section")
        return
    
    body, fn_section = text.split('=== FOOTNOTES ===', 1)
    fn_lines = fn_section.strip().split('\n')
    
    updated = []
    for line in fn_lines:
        if 'cước chú' in line and 'tham chiếu' in line:
            # Extract list number and reference number
            match = re.match(r'\[(\d+)\]\s*\[cước chú\s+(\d+)', line)
            if match:
                list_num = match.group(1)
                ref_num = match.group(2)
                # Replace with context marker
                updated.append(f"[{list_num}] [CẦN DỊCH — cước chú {ref_num} từ bản gốc; tham chiếu tại cước chú {ref_num} trong thân bài]")
            else:
                updated.append(line)
        else:
            updated.append(line)
    
    new_text = body.rstrip() + "\n\n=== FOOTNOTES ===\n" + "\n".join(updated) + "\n"
    file.write_text(new_text, encoding='utf-8')
    print(f"Ch{chapter}: Updated placeholder footnotes")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        chapter = int(sys.argv[1])
        update_placeholder_footnotes(chapter)
    else:
        for ch in [2, 3, 5, 12, 13]:
            update_placeholder_footnotes(ch)