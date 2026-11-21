#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Check footnote block
idx = text.find('--- [Cước chú trang')
if idx >= 0:
    with open('fn_block.txt', 'w', encoding='utf-8') as f:
        f.write(text[idx:idx+500])
    print('Found footnote block')
else:
    print('Footnote block NOT found')