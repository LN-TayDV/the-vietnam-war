import re
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all instances of 'chính phủ' case insensitive
for m in re.finditer(r'chính phủ', text, re.IGNORECASE):
    start = max(0, m.start()-100)
    end = min(len(text), m.end()+100)
    print(f'Position {m.start()}: ...{text[start:end]}...')
    print()