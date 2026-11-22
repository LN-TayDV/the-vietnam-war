import re
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Verify changes - check for remaining 'này'
matches = list(re.finditer(r'\bnày\b', text))
print(f"Remaining 'này' instances: {len(matches)}")
for m in matches:
    start = max(0, m.start()-40)
    end = min(len(text), m.end()+40)
    context = text[start:end].replace('\n', ' ')
    print(f"  Position {m.start()}: ...{context}...")

# Check 'nầy' count
nay_matches = list(re.finditer(r'\bnầy\b', text))
print(f"\n'nầy' instances: {len(nay_matches)}")