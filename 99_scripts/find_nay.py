import re
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all instances of 'này' (as whole word)
for m in re.finditer(r'\bnày\b', text):
    start = max(0, m.start()-80)
    end = min(len(text), m.end()+80)
    context = text[start:end].replace('\n', ' ')
    print(f'Position {m.start()}: ...{context}...')
    print()