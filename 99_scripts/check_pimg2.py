with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find PIMG blocks
for m in re.finditer(r'--- \[PIMG\d+\]', text):
    start = m.end()
    next_block = text.find('--- [', start)
    if next_block == -1:
        next_block = len(text)
    block = text[start:next_block].strip()
    with open('pimg_content.txt', 'w', encoding='utf-8') as f:
        f.write(repr(block[:300]))