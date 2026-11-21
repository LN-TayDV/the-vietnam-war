#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split main text and footnotes
parts = text.split('--- [Cước chú trang')
main_text = parts[0]

# Find all inline markers in main text (both [n] and n at end of sentences)
markers_bracket = re.findall(r'\[(\d+)\]', main_text)
print('Main text [n] markers:', sorted(set(int(x) for x in markers_bracket)))

# Check for bare numbers at end of sentences (footnote references)
markers_bare = re.findall(r'\.(\d{1,2})\s+[A-ZĂÂĐÊÔƠƯ]', main_text)
print('Main text bare markers:', sorted(set(int(x) for x in markers_bare)))

# Check first 5000 chars for footnote references
sample = main_text[:5000]
for m in re.finditer(r'\.(\d{1,2})\s', sample):
    print(f'Pos {m.start()}: ...{sample[max(0,m.start()-30):m.end()+30]}...')