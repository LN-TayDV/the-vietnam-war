#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

# Split into paragraphs
src_paras = re.split(r'(--- \[V1C09-P\d{3}\] \(trang [^)]+\) ---)', src)
vi_paras = re.split(r'(--- \[V1C09-P\d{3}\] \(trang [^)]+\) ---)', vi)

# src_paras and vi_paras will have: [before_first, marker1, content1, marker2, content2, ...]
# Let's process them

print(f'Source para segments: {len(src_paras)}')
print(f'VI para segments: {len(vi_paras)}')

# Extract markers per paragraph for source
src_para_markers = []
for i in range(1, len(src_paras), 2):
    if i + 1 < len(src_paras):
        marker = src_paras[i]
        content = src_paras[i+1]
        markers = re.findall(r'\[(\d+)\]', content)
        src_para_markers.append((marker, markers))

# Extract markers per paragraph for VI
vi_para_markers = []
for i in range(1, len(vi_paras), 2):
    if i + 1 < len(vi_paras):
        marker = vi_paras[i]
        content = vi_paras[i+1]
        # Both bracketed and bare
        markers_bracket = re.findall(r'\[(\d+)\]', content)
        markers_bare = re.findall(r'\.(\d{1,2})\s+[A-ZĂÂĐÊÔƠƯ]', content)
        vi_para_markers.append((marker, markers_bracket, markers_bare))

print('\nSource paragraph markers:')
for marker, markers in src_para_markers:
    print(f'  {marker.strip()}: {markers}')

print('\nVI paragraph markers:')
for marker, mbracket, mbare in vi_para_markers:
    print(f'  {marker.strip()}: bracket={mbracket}, bare={mbare}')