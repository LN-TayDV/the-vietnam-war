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

# Clean paragraph content (remove page/heading markers)
def clean_para(p):
    p = re.sub(r'\(trang \d+\)\s*---', '', p)
    p = re.sub(r'\(trang \d+-\d+\)\s*---', '', p)
    p = re.sub(r'— đề mục\s*---', '', p)
    p = re.sub(r'heading\s*---', '', p)
    return p.strip()

src_clean = [clean_para(p) for p in src_paras]
vi_clean = [clean_para(p) for p in vi_paras]

# Count sentences in each source paragraph
def count_sentences(text):
    return len(re.findall(r'(?<=[.!?])\s+(?=[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲÝỴỶỸĐ])', text)) + (1 if text.strip() and not text.strip().endswith(('.', '!', '?')) else 0)

# Actually better: split sentences
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲÝỴỶỸĐ])', text)
    return [s.strip() for s in sentences if s.strip()]

# Get sentence counts per source paragraph
src_sent_counts = []
src_sents_list = []
for p in src_clean:
    sents = split_sentences(p)
    src_sent_counts.append(len(sents))
    src_sents_list.append(sents)

# Get all translation sentences in order
vi_full = ' '.join(vi_clean)
vi_all_sents = split_sentences(vi_full)

print(f'Total source sentences: {sum(src_sent_counts)}')
print(f'Total translation sentences: {len(vi_all_sents)}')
print(f'Source paragraph sentence counts: {src_sent_counts}')

# Now rebuild translation paragraphs by taking sentences from vi_all_sents
# according to src_sent_counts
new_vi_paras = []
vi_idx = 0
for i, count in enumerate(src_sent_counts):
    if vi_idx >= len(vi_all_sents):
        # No more translation sentences - this paragraph missing
        new_vi_paras.append('[MISSING TRANSLATION]')
        continue
    # Take 'count' sentences
    end_idx = min(vi_idx + count, len(vi_all_sents))
    para_sents = vi_all_sents[vi_idx:end_idx]
    new_vi_paras.append(' '.join(para_sents))
    vi_idx = end_idx

# Check if we used all translation sentences
print(f'Used {vi_idx} of {len(vi_all_sents)} translation sentences')
if vi_idx < len(vi_all_sents):
    print(f'Remaining translation sentences: {len(vi_all_sents) - vi_idx}')
    for s in vi_all_sents[vi_idx:]:
        print(f'  REMAINING: {s[:100]}')

# Now rebuild the full translation file with proper markers
# We need to preserve the original page/heading markers from source
output = '===== V1-C01 · Trí nhớ, Truyền thống và Sử học về "Việt Nam" · Liam C. Kelley =====\n'
output += 'Nguồn: 02_extracted_text/v1/ch01.txt · PDF 43-59 · trang in 27-43\n\n'

for i, (src_para, vi_para) in enumerate(zip(src_paras, new_vi_paras)):
    # Extract page/heading marker from source
    marker_match = re.search(r'(\(trang [\d\-]+\)\s*---.*?)(?=\n)', src_para)
    if marker_match:
        marker = marker_match.group(1)
    else:
        marker = '(trang ???) ---'
    
    # Check if heading
    is_heading = '— đề mục' in src_para or 'heading' in src_para.lower()
    if is_heading:
        marker = marker.replace('---', '— đề mục ---')
    
    output += f'--- [V1C01-P{i+1:03d}] {marker}\n{vi_para}\n\n'

# Save
with open('translation-project/04_translation/v1/ch01/v1_ch01_vi_realigned.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(output)

print(f'Rebuilt translation with {len(new_vi_paras)} paragraphs')
print('Saved to v1_ch01_vi_realigned.txt')