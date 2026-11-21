src = open('translation-project/99_scripts/build_chapter_docx.py', encoding='utf-8').read()
lines = src.split(chr(10))
out = []
for i, line in enumerate(lines):
    if 'trích dẫn' in line:
        out.append(str(i+1) + ': ' + line.strip())
open('C:/Users/PC/AppData/Local/Temp/kilo/td_lines.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')