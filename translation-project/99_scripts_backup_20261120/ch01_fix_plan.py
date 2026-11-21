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

# Clean paragraph content (remove page/heading markers, footnotes)
def clean_para(p):
    p = re.sub(r'\(trang \d+\)\s*---', '', p)
    p = re.sub(r'\(trang \d+-\d+\)\s*---', '', p)
    p = re.sub(r'— đề mục\s*---', '', p)
    p = re.sub(r'heading\s*---', '', p)
    # Remove footnote blocks
    p = re.sub(r'--- \[Cước chú.*?---', '', p, flags=re.DOTALL)
    return p.strip()

src_clean = [clean_para(p) for p in src_paras]
vi_clean = [clean_para(p) for p in vi_paras]

# Join all translation body text (excluding footnotes)
vi_body = ' '.join(vi_clean)

# Split into sentences
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲÝỴỶỸĐ])', text)
    return [s.strip() for s in sentences if s.strip()]

vi_all_sents = split_sentences(vi_body)

# Count sentences per source paragraph
def count_sents(text):
    return len(split_sentences(text))

src_sent_counts = [count_sents(p) for p in src_clean]

print(f'Total translation sentences available: {len(vi_all_sents)}')
print(f'Total source sentences needed: {sum(src_sent_counts)}')
print(f'Source paragraph sentence counts: {src_sent_counts}')

# The missing section is paragraphs 39-49 (indices 38-48) - Anglophone Histories
# Let's check how many sentences those have
missing_start = 38  # 0-indexed, paragraph 39
missing_sents = sum(src_sent_counts[missing_start:])
print(f'Missing section (paras 39-49) sentences: {missing_sents}')

# Available sentences for paras 1-38
available_for_main = len(vi_all_sents)
needed_for_main = sum(src_sent_counts[:missing_start])
print(f'Main section (paras 1-38) needs: {needed_for_main}, available: {available_for_main}')

# We have 179 sentences, need ~179 for first 38 paragraphs (roughly matches)
# Let's distribute proportionally
# Actually, let's just take sentences sequentially for each paragraph

# Rebuild translation paragraphs
new_vi_paras = []
vi_idx = 0

for i, count in enumerate(src_sent_counts):
    if vi_idx >= len(vi_all_sents):
        # No more translation - mark as missing
        new_vi_paras.append('[CẦN DỊCH - MISSING TRANSLATION]')
        continue
    
    end_idx = min(vi_idx + count, len(vi_all_sents))
    para_sents = vi_all_sents[vi_idx:end_idx]
    new_vi_paras.append(' '.join(para_sents))
    vi_idx = end_idx

print(f'Used {vi_idx} of {len(vi_all_sents)} sentences')
print(f'Generated {len(new_vi_paras)} paragraphs')

# Check last few paragraphs
for i in range(38, 49):
    p = new_vi_paras[i]
    print(f'PARA {i+1} ({src_sent_counts[i]} src sents): {p[:150]}...')

# Now we need to translate the missing paragraphs (39-49)
# Let's extract the source text for those paragraphs
print('\n--- MISSING SOURCE PARAGRAPHS (need translation) ---')
for i in range(38, 49):
    print(f'SRC PARA {i+1}: {src_clean[i][:200]}...')