#!/usr/bin/env python3
"""
Convert realigned Vietnamese files to builder-expected format (V1C##-P###).
The builder expects paragraph IDs like [V1C02-P001] (trang N) with single page number.
"""

import re
from pathlib import Path

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"

def int_to_sup(n: int) -> str:
    return "".join(SUP[int(d)] for d in str(n))

def sup_to_int(s: str) -> int:
    return int("".join(str(SUP.index(c)) for c in s))

def convert_realigned_to_builder(chapter: int, volume: str = "v2"):
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    # Use FIXED file (with CRITICAL + MAJOR VNCH fixes) instead of realigned
    fixed_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_fixed.txt"
    if not fixed_file.exists():
        fixed_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_realigned.txt"
    builder_file = root / f"04_translation/{volume}/ch{chapter:02d}/v1_ch{chapter:02d}_vi.txt"
    
    text = fixed_file.read_text(encoding='utf-8')
    
    # Split into body and footnotes
    if "=== FOOTNOTES ===" in text:
        body_part, fn_part = text.split("=== FOOTNOTES ===", 1)
    else:
        body_part = text
        fn_part = ""
    
    # Find all superscript markers in body
    body_superscripts = set()
    for m in re.finditer(r'[' + SUP + ']+', body_part):
        sup = m.group()
        num = sup_to_int(sup)
        body_superscripts.add(num)
    
    print(f"  Body superscript markers: {sorted(body_superscripts)} (count: {len(body_superscripts)})")
    
    # Convert body paragraph IDs to V1C##-P### (builder expected format)
    # Use single page number (first of range)
    para_count = 0
    def convert_body_id(match):
        nonlocal para_count
        para_count += 1
        ids_part = match.group(1)
        page_part = match.group(2)
        ids = ids_part.split('+')
        first_id = ids[0]
        
        # Extract paragraph number
        num = None
        if first_id.startswith('V1-CH-P'):
            num = first_id[7:]
        elif first_id.startswith('V1C'):
            p_match = re.search(r'-P(\d+)', first_id)
            if p_match:
                num = p_match.group(1)
        elif first_id.startswith('EXTRA_'):
            num = f"{para_count:03d}"
        
        if num is None:
            num = f"{para_count:03d}"
        
        # Use single page number (first of range if dash format)
        single_page = page_part.split('-')[0]
        
        # Builder expects V1C##-P### format with single page
        new_id = f"V1C{chapter:02d}-P{int(num):03d}"
        return f"[{new_id}] (trang {single_page})"
    
    body_part = re.sub(r'\[(V1[^\]]+)\]\s*\(trang\s+([\d\-]+)\)', convert_body_id, body_part)
    
    # Convert footnotes section - keep original numbering matching body markers
    if fn_part:
        fn_lines = fn_part.strip().split('\n')
        new_fn_lines = []
        
        for line in fn_lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(r'\[(\d+)\]\s*(.*)', line)
            if match:
                orig_num = int(match.group(1))
                fn_text = match.group(2).strip()
                
                # Skip if this footnote number doesn't have a body marker
                if orig_num not in body_superscripts:
                    print(f"  Skipping orphan footnote {orig_num}: {fn_text[:60]}...")
                    continue
                
                # Keep original number for builder matching
                sup = int_to_sup(orig_num)
                new_fn_lines.append(f"{sup} {fn_text}")
            else:
                continue
        
        new_fn_part = "\n".join(new_fn_lines)
        new_text = body_part.rstrip() + "\n\n=== FOOTNOTES ===\n" + new_fn_part + "\n"
    else:
        new_text = body_part.rstrip() + "\n"
    
    builder_file = root / f"04_translation/v2/ch{chapter:02d}/v1_ch{chapter:02d}_vi.txt"
    builder_file.write_text(new_text, encoding='utf-8')
    print(f"Ch{chapter}: Converted ({para_count} paragraphs, {len(body_superscripts)} footnotes) -> {builder_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        chapter = int(sys.argv[1])
        convert_realigned_to_builder(chapter)
    else:
        for ch in range(1, 14):
            convert_realigned_to_builder(ch)