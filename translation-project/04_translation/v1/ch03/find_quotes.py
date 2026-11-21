vi = open('translation-project/04_translation/v1/ch03/v1_ch03_vi.txt', encoding='utf-8').read()
import re
out = []
for m in re.finditer(r'--- \[V1C03-P(\d+)\].*?--- \[V1C03-P', vi, re.DOTALL):
    para = m.group()
    if '"' in para or '— trích dẫn —' in para:
        num = re.search(r'P(\d+)', para).group(1)
        out.append('P' + num)
open('C:/Users/PC/AppData/Local/Temp/kilo/quotes.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')