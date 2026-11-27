import io, re
src = '02_extracted_text/v7/v2_ch03_src.txt'
s = io.open(src, encoding='utf-8').read()
parts = re.split(r'(?=\[V7-CH-P\d+\])', s)
out = []
for p in parts:
    m = re.match(r'\[V7-CH-(P\d+)\] \(\u0074rang (\d+)\) \[(\w+)\]', p)
    if m:
        body = p.split(']', 2)[-1].strip()
        out.append('### %s p%s [%s]' % (m.group(1), m.group(2), m.group(3)))
        out.append(body)
        out.append('')
io.open('99_scripts/_ch03full.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written', len(out))