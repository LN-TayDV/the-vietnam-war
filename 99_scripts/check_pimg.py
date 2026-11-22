with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find PIMG blocks
for m in re.finditer(r'--- \[V1C10-PIMG\d+\]', text):
    start = m.end()
    # Find next block start or end
    next_block = text.find('--- [', start)
    if next_block == -1:
        next_block = len(text)
    block = text[start:next_block].strip()
    print(repr(block[:200]))
    print()