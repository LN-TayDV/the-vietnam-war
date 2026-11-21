vi = open('translation-project/04_translation/v1/ch03/v1_ch03_vi.txt', encoding='utf-8').read()
parts = vi.split('--- [Cước chú')
body = parts[0]
import re
lines = body.split(chr(10))
out = []
for i, line in enumerate(lines):
    if '---' in line or '=====' in line or 'Source:' in line:
        continue
    eng = re.findall(r'[A-Za-z]{6,}', line)
    if eng:
        out.append(str(i+1) + ': ' + line[:80])
        out.append('   EN: ' + str(eng))
open('C:/Users/PC/AppData/Local/Temp/kilo/body_eng2.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')