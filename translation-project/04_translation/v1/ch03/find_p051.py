vi = open('translation-project/04_translation/v1/ch03/v1_ch03_vi.txt', encoding='utf-8').read()
import re
m = re.search(r'--- \[V1C03-P051\].*?--- \[V1C03-P052\]', vi, re.DOTALL)
if m:
    open('C:/Users/PC/AppData/Local/Temp/kilo/p051.txt','w',encoding='utf-8').write(m.group())
print('done')