import re
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all instances of 'này' (as whole word)
matches = list(re.finditer(r'\bnày\b', text))
print(f"Total instances found: {len(matches)}")

# The exception is at position 40390: "sau này"
# We need to change all others to "nầy"

# Build new text by replacing from end to start to preserve positions
new_text = text
changes = 0
for m in reversed(matches):
    pos = m.start()
    # Check if this is the exception "sau này"
    # Look at context before
    context_before = text[max(0, pos-10):pos]
    if context_before.strip().endswith('sau'):
        print(f"SKIP (exception 'sau này'): position {pos}")
        continue
    
    # Replace this instance
    new_text = new_text[:pos] + 'nầy' + new_text[pos+len('này'):]
    changes += 1

print(f"Changes made: {changes}")

# Write back
with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_text)

print("Done!")