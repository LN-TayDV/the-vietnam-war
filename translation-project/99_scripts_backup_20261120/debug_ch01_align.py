import re

# Read source and translation
with open('translation-project/04_translation/v1/ch01/v1_ch01_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()
with open('translation-project/04_translation/v1/ch01/v1_ch01_vi.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

# Split by paragraph markers
src_paras = re.split(r'--- \[V1C01-P\d+\]', src)
vi_paras = re.split(r'--- \[V1C01-P\d+\]', vi)

# Remove first empty element
src_paras = [p.strip() for p in src_paras[1:] if p.strip()]
vi_paras = [p.strip() for p in vi_paras[1:] if p.strip()]

print(f'Source: {len(src_paras)} paragraphs')
print(f'Translation: {len(vi_paras)} paragraphs')

# Let's look at the content more carefully to understand the shift
# The translation seems to have the heading as a separate paragraph (P005)
# Let's check which paragraphs are headings
src_headings = []
vi_headings = []
for i, p in enumerate(src_paras):
    if '— đề mục' in p or p.strip().startswith('From Traditional'):
        src_headings.append(i)
        print(f'SRC Heading at {i}: {p[:80]}')
for i, p in enumerate(vi_paras):
    if '— đề mục' in p or p.strip().startswith('Từ Sử Học'):
        vi_headings.append(i)
        print(f'VI Heading at {i}: {p[:80]}')

# The issue: translation has extra paragraph at the beginning (the title line)
# Let's check the first few paragraphs
print('\n--- FIRST 10 SRC ---')
for i in range(min(10, len(src_paras))):
    print(f'SRC[{i}]: {src_paras[i][:100]}...')

print('\n--- FIRST 10 VI ---')
for i in range(min(10, len(vi_paras))):
    print(f'VI[{i}]: {vi_paras[i][:100]}...')