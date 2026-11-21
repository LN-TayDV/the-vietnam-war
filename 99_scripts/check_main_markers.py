#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split main text and footnotes
parts = text.split('--- [Cước chú trang')
main_text = parts[0]

# Find all inline markers in main text
markers = re.findall(r'\[(\d+)\]', main_text)
print('Main text markers:', sorted(set(int(x) for x in markers)))

# Check for [1955] in main text
for m in re.finditer(r'\[1955\]', main_text):
    start = max(0, m.start()-50)
    end = min(len(main_text), m.end()+50)
    print(f'Main text [1955] at {m.start()}: ...{main_text[start:end]}...')

# Check footnote block for [1955]
footnotes = parts[1] if len(parts) > 1 else ''
for m in re.finditer(r'\[1955\]', footnotes):
    start = max(0, m.start()-50)
    end = min(len(footnotes), m.end()+50)
    print(f'Footnote block [1955] at {m.start()}: ...{footnotes[start:end]}...')