import re

# Read source and translation
with open('translation-project/04_translation/v1/ch01/v1_ch01_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()
with open('translation-project/04_translation/v1/ch01/v1_ch01_vi.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

# Split by paragraph markers
src_paras = re.split(r'--- \[V1C01-P\d+\]', src)
vi_paras = re.split(r'--- \[V1C01-P\d+\]', vi)

src_paras = [p.strip() for p in src_paras[1:] if p.strip()]
vi_paras = [p.strip() for p in vi_paras[1:] if p.strip()]

# Clean paragraph content
def clean_para(p):
    p = re.sub(r'\(trang \d+\)\s*---', '', p)
    p = re.sub(r'\(trang \d+-\d+\)\s*---', '', p)
    p = re.sub(r'— đề mục\s*---', '', p)
    p = re.sub(r'heading\s*---', '', p)
    p = re.sub(r'--- \[Cước chú.*?---', '', p, flags=re.DOTALL)
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

# Distribute translation sentences across paragraphs
# For first 38 paragraphs, we have 179 sentences for 160 needed
# For last 11 paragraphs, we need 44 sentences but have 0

# Strategy: Use proportional distribution for first 38 paragraphs
# Each paragraph gets ceil(count * 179/160) sentences, but capped at available
total_main_src = sum(src_sent_counts[:38])
total_main_vi = len(vi_all_sents)  # 179
ratio = total_main_vi / total_main_src  # ~1.12

new_vi_paras = []
vi_idx = 0

for i, count in enumerate(src_sent_counts):
    if i < 38:
        # Main section - allocate proportionally
        allocated = int(round(count * ratio))
        allocated = max(1, allocated)  # at least 1 sentence
        end_idx = min(vi_idx + allocated, len(vi_all_sents))
    else:
        # Missing section - mark for translation
        new_vi_paras.append('[CẦN DỊCH - MISSING]')
        continue
    
    para_sents = vi_all_sents[vi_idx:end_idx]
    new_vi_paras.append(' '.join(para_sents) if para_sents else '[EMPTY]')
    vi_idx = end_idx

print(f'Used {vi_idx} of {len(vi_all_sents)} sentences')
print(f'Generated {len(new_vi_paras)} paragraphs')

# Check distribution
for i in range(49):
    if i < 38:
        allocated = len(split_sentences(new_vi_paras[i])) if new_vi_paras[i] not in ['[CẦN DỊCH - MISSING]', '[EMPTY]'] else 0
        print(f'PARA {i+1}: src={src_sent_counts[i]}, vi={allocated}, ratio={allocated/src_sent_counts[i] if src_sent_counts[i]>0 else 0:.2f}')
    else:
        print(f'PARA {i+1}: src={src_sent_counts[i]}, vi=MISSING')

# Save the main section realigned translation
output = '===== V1-C01 · Trí nhớ, Truyền thống và Sử học về "Việt Nam" · Liam C. Kelley =====\n'
output += 'Nguồn: 02_extracted_text/v1/ch01.txt · PDF 43-59 · trang in 27-43\n\n'

for i, src_para in enumerate(src_paras):
    # Extract page/heading marker from source
    marker_match = re.search(r'(\(trang [\d\-]+\)\s*---.*?)(?=\n)', src_para)
    if marker_match:
        marker = marker_match.group(1)
    else:
        marker = '(trang ???) ---'
    
    is_heading = '— đề mục' in src_para or 'heading' in src_para.lower()
    if is_heading:
        marker = marker.replace('---', '— đề mục ---')
    
    vi_para = new_vi_paras[i] if i < len(new_vi_paras) else '[MISSING]'
    output += f'--- [V1C01-P{i+1:03d}] {marker}\n{vi_para}\n\n'

# Add footnotes from original translation
# Extract footnotes from original vi
footnote_blocks = re.findall(r'--- \[Cước chú.*?---', vi, re.DOTALL)
if footnote_blocks:
    output += '\n'.join(footnote_blocks)

with open('translation-project/04_translation/v1/ch01/v1_ch01_vi_fixed.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(output)

print('\nSaved to v1_ch01_vi_fixed.txt')