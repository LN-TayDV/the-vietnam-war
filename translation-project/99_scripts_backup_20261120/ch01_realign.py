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

# Remove page markers and heading markers from content for alignment
def clean_para(p):
    # Remove page/heading markers
    p = re.sub(r'\(trang \d+\)\s*---', '', p)
    p = re.sub(r'\(trang \d+-\d+\)\s*---', '', p)
    p = re.sub(r'— đề mục\s*---', '', p)
    p = re.sub(r'heading\s*---', '', p)
    return p.strip()

src_clean = [clean_para(p) for p in src_paras]
vi_clean = [clean_para(p) for p in vi_paras]

# Join all text
src_full = ' '.join(src_clean)
vi_full = ' '.join(vi_clean)

# Split into sentences
def split_sentences(text):
    # Simple sentence splitter
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲÝỴỶỸĐ])', text)
    return [s.strip() for s in sentences if s.strip()]

src_sents = split_sentences(src_full)
vi_sents = split_sentences(vi_full)

print(f'Source sentences: {len(src_sents)}')
print(f'Translation sentences: {len(vi_sents)}')

# Check first 10 sentences
for i in range(min(10, len(src_sents))):
    print(f'SRC[{i}]: {src_sents[i][:100]}')
for i in range(min(10, len(vi_sents))):
    print(f'VI[{i}]: {vi_sents[i][:100]}')