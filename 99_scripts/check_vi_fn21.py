#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

# Find footnote 21 in VI
for m in re.finditer(r'\[21\].*?(?=\[22\]|$)', vi, re.DOTALL):
    with open('vi_fn21.txt', 'w', encoding='utf-8') as f:
        f.write(m.group()[:1000])

# Find the citation for Le Thanh Khoi
for m in re.finditer(r'Lê Thành Khôi.*?1955', vi):
    start = max(0, m.start()-100)
    end = min(len(vi), m.end()+100)
    with open('vi_citation.txt', 'w', encoding='utf-8') as f:
        f.write(vi[start:end])