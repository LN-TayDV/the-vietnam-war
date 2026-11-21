src = open('translation-project/99_scripts/build_chapter_docx.py', encoding='utf-8').read()
lines = src.split(chr(10))
out = []
for i in range(238, 258):
    out.append(str(i+1) + ': ' + lines[i])
open('C:/Users/PC/AppData/Local/Temp/kilo/td_ctx.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')