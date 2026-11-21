#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split main text and footnotes
parts = text.split('--- [Cước chú trang')
main_text = parts[0]
footnotes = '--- [Cước chú trang' + parts[1] if len(parts) > 1 else ''

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\find_issues_out.txt', 'w', encoding='utf-8') as out:
    out.write("=== FOOTNOTES: 'đạo chính' occurrences ===\n")
    for m in re.finditer(r'đạo chính', footnotes):
        start = max(0, m.start()-50)
        end = min(len(footnotes), m.end()+50)
        out.write(f'Pos {m.start()}: ...{footnotes[start:end]}...\n')

    out.write("\n=== FOOTNOTES: 'giải phóng' occurrences ===\n")
    for m in re.finditer(r'giải phóng', footnotes):
        start = max(0, m.start()-50)
        end = min(len(footnotes), m.end()+50)
        out.write(f'Pos {m.start()}: ...{footnotes[start:end]}...\n')

    out.write("\n=== MAIN TEXT: 'nó' pronoun (first 10) ===\n")
    count = 0
    for m in re.finditer(r'\bnó\b', main_text):
        if count >= 10:
            break
        start = max(0, m.start()-50)
        end = min(len(main_text), m.end()+50)
        out.write(f'Pos {m.start()}: ...{main_text[start:end]}...\n')
        count += 1