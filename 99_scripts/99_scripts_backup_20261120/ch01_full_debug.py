import re

with open('translation-project/04_translation/v1/ch01/v1_ch01_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()
with open('translation-project/04_translation/v1/ch01/v1_ch01_vi.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

src_paras = re.split(r'--- \[V1C01-P\d+\]', src)
vi_paras = re.split(r'--- \[V1C01-P\d+\]', vi)

src_paras = [p.strip() for p in src_paras[1:] if p.strip()]
vi_paras = [p.strip() for p in vi_paras[1:] if p.strip()]

with open('C:\\Users\\PC\\AppData\\Local\\Temp\\kilo\\ch01_full_debug.txt', 'w', encoding='utf-8') as out:
    for i in range(len(src_paras)):
        src_sents = len(re.findall(r'\.[\s\n]', src_paras[i]))
        vi_sents = len(re.findall(r'\.[\s\n]', vi_paras[i])) if i < len(vi_paras) else 0
        out.write('PARA {}: SRC={} sentences, VI={} sentences\n'.format(i+1, src_sents, vi_sents))
        if src_sents != vi_sents:
            out.write('  SRC: {}...\n'.format(src_paras[i][:120]))
            vi_text = vi_paras[i][:120] if i < len(vi_paras) else 'MISSING'
            out.write('  VI: {}...\n'.format(vi_text))
        out.write('\n')