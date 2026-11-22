with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find all block headers
for m in re.finditer(r'--- \[([^\]]+)\]', text):
    print(m.group(1))