import re

# Read the extracted text
with open('translation-project/02_extracted_text/v1/ch05.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove page numbers, headers, footers, figure captions
lines = text.split('\n')
cleaned = []
for line in lines:
    line_stripped = line.strip()
    # Skip page numbers (lines with just digits)
    if re.match(r'^\d+$', line_stripped):
        continue
    # Skip repeated headers
    if line_stripped in ['The August Revolution of 1945', 'Stein Tønnesson']:
        continue
    # Skip figure captions
    if line_stripped.startswith('Figure 5.') or line_stripped.startswith('Source:'):
        continue
    # Skip footnote markers like "1  David G. Marr..."
    if re.match(r'^\d+ ', line_stripped):
        continue
    # Skip footnote continuations like "2  Jack A. Goldstone..."
    if re.match(r'^\d+\s', line_stripped) and len(line_stripped) > 20:
        continue
    cleaned.append(line)

text = '\n'.join(cleaned)

# Now we need to reconstruct paragraphs. The text has single newlines within paragraphs
# and double newlines between paragraphs. But page breaks broke this.
# Let's join lines that don't end with sentence-ending punctuation followed by capital letter
# Actually, let's use a simpler approach: split by double newline first
paras = re.split(r'\n\s*\n', text)

# Merge short fragments that are likely continuations
merged = []
for p in paras:
    p = p.strip()
    if not p:
        continue
    # If previous paragraph doesn't end with sentence end and this starts with lowercase,
    # or if this is very short (< 50 chars), merge with previous
    if merged and (len(p) < 80 or (not re.search(r'[.!?]["\']?\s*$', merged[-1]) and p[0].islower())):
        merged[-1] += ' ' + p
    else:
        merged.append(p)

# Identify headings
headings = [
    'The August Revolution of 1945',
    'What Is Revolution?',
    'Hồ Chí Minh and Trường Chinh',
    'The Concept of "August Revolution"',
    'The Global Context and the Role of the United States',
    'A Divided Nation',
    'Revolution and War',
    'Part II'
]

output = '===== V1-C05 · The August Revolution of 1945 · Stein Tønnesson =====\n'
output += 'Nguồn: 02_extracted_text/v1/ch05.txt · PDF 106-124 · trang in 106-124\n\n'

para_num = 1
for p in merged:
    is_heading = any(p.startswith(h) for h in headings)
    if is_heading:
        output += f'--- [V1C05-P{para_num:03d}] (trang ???) — đề mục ---\n{p}\n\n'
    else:
        output += f'--- [V1C05-P{para_num:03d}] (trang ???) ---\n{p}\n\n'
    para_num += 1

with open('translation-project/04_translation/v1/ch05/v1_ch05_src.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(output)

print(f'Created source file with {para_num-1} paragraphs')
for i, p in enumerate(merged, 1):
    is_heading = any(p.startswith(h) for h in headings)
    print(f'P{i:03d} {"[HEADING]" if is_heading else ""}: {p[:100]}...')