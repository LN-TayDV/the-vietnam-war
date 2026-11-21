#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix footnote 21: add [1955] after 1969
text = text.replace('(München, 1969 ), 433.', '(München, 1969 [1955]), 433.')

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print('Fixed footnote 21')