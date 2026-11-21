src = open('translation-project/99_scripts/build_chapter_docx.py', encoding='utf-8').read()
import re
out = []
for m in re.finditer(r'.{0,60}đề mục.{0,60}', src):
    out.append(m.group())
open('C:/Users/PC/AppData/Local/Temp/kilo/hd.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')