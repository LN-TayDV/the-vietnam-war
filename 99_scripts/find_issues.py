#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\find_issues_out.txt', 'w', encoding='utf-8') as out:
    out.write("=== 'đạo chính' occurrences ===\n")
    for m in re.finditer(r'đạo chính', text):
        start = max(0, m.start()-50)
        end = min(len(text), m.end()+50)
        out.write(f'Pos {m.start()}: ...{text[start:end]}...\n')

    out.write("\n=== 'nó' as standalone pronoun ===\n")
    for m in re.finditer(r'\bnó\b', text):
        start = max(0, m.start()-50)
        end = min(len(text), m.end()+50)
        out.write(f'Pos {m.start()}: ...{text[start:end]}...\n')

    out.write("\n=== 'giải phóng' occurrences ===\n")
    for m in re.finditer(r'giải phóng', text):
        start = max(0, m.start()-50)
        end = min(len(text), m.end()+50)
        out.write(f'Pos {m.start()}: ...{text[start:end]}...\n')