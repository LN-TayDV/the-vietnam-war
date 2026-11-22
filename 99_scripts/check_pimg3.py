with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find all PIMG blocks
for m in re.finditer(r'--- \[PIMG(\d+)\]', text):
    num = m.group(1)
    start = m.end()
    next_block = text.find('--- [', start)
    if next_block == -1:
        next_block = len(text)
    block = text[start:next_block].strip()
    with open(f'pimg{num}_content.txt', 'w', encoding='utf-8') as f:
        f.write(repr(block[:500]))