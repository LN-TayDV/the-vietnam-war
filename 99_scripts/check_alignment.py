import re
from pathlib import Path

root = Path('.')
src_file = root / 'translation-project' / '04_translation' / 'v1' / 'ch10' / 'v1_ch10_src.txt'
vi_file = root / 'translation-project' / '04_translation' / 'v1' / 'ch10' / 'v1_ch10_vi.txt'

with open(src_file, 'r', encoding='utf-8') as f:
    src_text = f.read()
with open(vi_file, 'r', encoding='utf-8') as f:
    vi_text = f.read()

# Split by markers
src_paras = re.split(r'--- \[V1C10-P\d+\]', src_text)
vi_paras = re.split(r'--- \[V1C10-P\d+\]', vi_text)

# Get markers
src_markers = re.findall(r'--- \[(V1C10-P\d+)\]', src_text)
vi_markers = re.findall(r'--- \[(V1C10-P\d+)\]', vi_text)

# Check all paragraphs for sentence count
with open('alignment_check.txt', 'w', encoding='utf-8') as out:
    for i, (marker, src_p, vi_p) in enumerate(zip(src_markers, src_paras[1:], vi_paras[1:])):
        src_sentences = len(re.findall(r'[.!?]+(?:\s|$)', src_p))
        vi_sentences = len(re.findall(r'[.!?]+(?:\s|$)', vi_p))
        diff = vi_sentences - src_sentences
        out.write(f'{marker}: src={src_sentences}, vi={vi_sentences}, diff={diff}\n')
        if abs(diff) > 2:
            out.write(f'  *** MISMATCH ***\n')
            out.write(f'  SRC: {src_p[:300]}\n')
            out.write(f'  VI:  {vi_p[:300]}\n')
        out.write('\n')

print("Done. Check alignment_check.txt")