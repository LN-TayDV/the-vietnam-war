import re

# Read the extracted text
with open('translation-project/02_extracted_text/v1/ch05.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean up page numbers and headers/footers
lines = text.split('\n')
cleaned = []
for line in lines:
    # Skip page numbers (lines with just digits)
    if re.match(r'^\d+$', line.strip()):
        continue
    # Skip 'The August Revolution of 1945' and 'Stein Tønnesson' repeated headers
    if line.strip() in ['The August Revolution of 1945', 'Stein Tønnesson']:
        continue
    # Skip figure captions like 'Figure 5.1  Public gathering...'
    if line.strip().startswith('Figure 5.') or line.strip().startswith('Source:'):
        continue
    cleaned.append(line)

text = '\n'.join(cleaned)

# Now split into paragraphs by double newlines
paras = re.split(r'\n\s*\n', text)

# Format with paragraph markers
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
for p in paras:
    p = p.strip()
    if not p:
        continue
    # Check if it's a heading
    is_heading = False
    for h in headings:
        if p.startswith(h):
            is_heading = True
            break
    
    if is_heading:
        output += f'--- [V1C05-P{para_num:03d}] (trang ???) — đề mục ---\n{p}\n\n'
    else:
        output += f'--- [V1C05-P{para_num:03d}] (trang ???) ---\n{p}\n\n'
    para_num += 1

with open('translation-project/04_translation/v1/ch05/v1_ch05_src.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(output)

print(f'Created source file with {para_num-1} paragraphs')