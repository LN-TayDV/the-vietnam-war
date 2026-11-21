#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()

# Find inline markers in source
markers_bracket = re.findall(r'\[(\d+)\]', src)
print('Source [n] markers:', sorted(set(int(x) for x in markers_bracket))[:20], '...')

# Check first 5000 chars
sample = src[:5000]
for m in re.finditer(r'\[(\d+)\]', sample):
    print(f'Pos {m.start()}: ...{sample[max(0,m.start()-30):m.end()+30]}...')