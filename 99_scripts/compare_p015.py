import re
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

with open('translation-project/04_translation/v1/ch10/v1_ch10_src.txt', 'r', encoding='utf-8') as f:
    src_text = f.read()

with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    vi_text = f.read()

src_paras = re.split(r'--- \[V1C10-P\d+\]', src_text)
vi_paras = re.split(r'--- \[V1C10-P\d+\]', vi_text)

src_markers = re.findall(r'--- \[(V1C10-P\d+)\]', src_text)
vi_markers = re.findall(r'--- \[(V1C10-P\d+)\]', vi_text)

# Find P015
p015_idx = src_markers.index('V1C10-P015')
src_p015 = src_paras[p015_idx + 1]
vi_p015 = vi_paras[p015_idx + 1]

print("=== SOURCE P015 ===")
src_sentences = re.split(r'(?<=[.!?])\s+', src_p015.strip())
for i, s in enumerate(src_sentences):
    print(f"  {i+1}. {s.strip()}")

print(f"\nTotal source sentences: {len(src_sentences)}")

print("\n=== VI P015 ===")
vi_sentences = re.split(r'(?<=[.!?])\s+', vi_p015.strip())
for i, s in enumerate(vi_sentences):
    print(f"  {i+1}. {s.strip()}")

print(f"\nTotal VI sentences: {len(vi_sentences)}")