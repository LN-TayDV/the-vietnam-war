#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

# Find footnote 21 in both
for m in re.finditer(r'\[21\].*?1955', src, re.DOTALL):
    start = max(0, m.start()-50)
    end = min(len(src), m.end()+50)
    print(f'Source [21]: ...{src[start:end]}...')

print()

for m in re.finditer(r'\[21\].*?1955', vi, re.DOTALL):
    start = max(0, m.start()-50)
    end = min(len(vi), m.end()+50)
    print(f'VI [21]: ...{vi[start:end]}...')

print()

# Find the exact citation in source
for m in re.finditer(r'Lê Thành Khôi.*?1955', src):
    start = max(0, m.start()-100)
    end = min(len(src), m.end()+100)
    print(f'Source citation: ...{src[start:end]}...')

print()

for m in re.finditer(r'Lê Thành Khôi.*?1955', vi):
    start = max(0, m.start()-100)
    end = min(len(vi), m.end()+100)
    print(f'VI citation: ...{vi[start:end]}...')