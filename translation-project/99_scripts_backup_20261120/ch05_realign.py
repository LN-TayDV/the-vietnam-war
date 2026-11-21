import re

# Read source and translation
with open('translation-project/04_translation/v1/ch05/v1_ch05_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()
with open('translation-project/04_translation/v1/ch05/v1_ch05_vi_FINAL.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

# Split source
src_paras = re.split(r'--- \[V1C05-P\d+\]', src)
src_paras = [p.strip() for p in src_paras[1:] if p.strip()]

# Split translation
vi_paras = re.split(r'--- \[V1C05-P\d+\]', vi)
vi_paras = [p.strip() for p in vi_paras[1:] if p.strip()]

# Clean paragraphs
def clean_para(p):
    p = re.sub(r'\(trang \d+\)\s*---', '', p)
    p = re.sub(r'\(trang \d+-\d+\)\s*---', '', p)
    p = re.sub(r'— đề mục\s*---', '', p)
    p = re.sub(r'heading\s*---', '', p)
    return p.strip()

src_clean = [clean_para(p) for p in src_paras]
vi_clean = [clean_para(p) for p in vi_paras]

# Split translation into sentences
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲÝỴỶỸĐ])', text)
    return [s.strip() for s in sentences if s.strip()]

vi_body = ' '.join(vi_clean)
vi_all_sents = split_sentences(vi_body)

# Count sentences per source paragraph
def count_sents(text):
    return len(split_sentences(text))

src_sent_counts = [count_sents(p) for p in src_clean]

print(f'Total translation sentences: {len(vi_all_sents)}')
print(f'Total source sentences needed: {sum(src_sent_counts)}')
print(f'Source paragraph sentence counts: {src_sent_counts}')

# Identify headings
headings = []
for i, p in enumerate(src_paras):
    if '— đề mục' in p or 'heading' in p.lower():
        headings.append(i)
        print(f'Heading at para {i+1}: {src_clean[i][:80]}')

# Distribute sentences proportionally
total_src_sents = sum(src_sent_counts)
ratio = len(vi_all_sents) / total_src_sents
print(f'Ratio: {ratio:.2f}')

new_vi_paras = []
vi_idx = 0

for i, count in enumerate(src_sent_counts):
    if i in headings:
        # Heading - use the heading text from translation
        # Find corresponding heading in vi_clean
        allocated = 1
    else:
        allocated = max(1, int(round(count * ratio)))
    
    end_idx = min(vi_idx + allocated, len(vi_all_sents))
    para_sents = vi_all_sents[vi_idx:end_idx]
    new_vi_paras.append(' '.join(para_sents) if para_sents else '[EMPTY]')
    vi_idx = end_idx

print(f'Used {vi_idx} of {len(vi_all_sents)} sentences')
print(f'Generated {len(new_vi_paras)} paragraphs')

# Check distribution
for i in range(len(new_vi_paras)):
    allocated = len(split_sentences(new_vi_paras[i])) if new_vi_paras[i] not in ['[EMPTY]'] else 0
    is_heading = 'heading' in src_paras[i].lower() or '— đề mục' in src_paras[i]
    print(f'PARA {i+1}: src={src_sent_counts[i]}, vi={allocated}, heading={is_heading}')

# Save realigned translation
output = '===== V1-C05 · The August Revolution of 1945 · Stein Tønnesson =====\n'
output += 'Nguồn: 02_extracted_text/v1/ch05.txt · PDF 106-124 · trang in 106-124\n\n'

for i, src_para in enumerate(src_paras):
    marker_match = re.search(r'(\(trang [\d\-]+\)\s*---.*?)(?=\n)', src_para)
    if marker_match:
        marker = marker_match.group(1)
    else:
        marker = '(trang ???) ---'
    
    is_heading = '— đề mục' in src_para or 'heading' in src_para.lower()
    if is_heading:
        marker = marker.replace('---', '— đề mục ---')
    
    vi_para = new_vi_paras[i] if i < len(new_vi_paras) else '[MISSING]'
    output += f'--- [V1C05-P{i+1:03d}] {marker}\n{vi_para}\n\n'

with open('translation-project/04_translation/v1/ch05/v1_ch05_vi_REALIGNED.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(output)

print('\nSaved realigned Chapter 5 translation')