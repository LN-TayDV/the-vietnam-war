from docx import Document
doc = Document('translation-project/09_docx/V1-C03_Ho-Chi-Minh-va-Su-Noi-Len-cua-Dang-Cong-San-Viet-Nam.docx')
out = []
for p in doc.paragraphs:
    if 'H' in p.text and 'Ch' in p.text and 'Minh' in p.text and 'h' in p.text and 'ph' in p.text:
        out.append('runs: ' + str(len(p.runs)))
        for r in p.runs:
            out.append('  text: ' + repr(r.text[:40]) + ' italic: ' + str(r.italic) + ' size: ' + str(r.font.size))
open('C:/Users/PC/AppData/Local/Temp/kilo/qr.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')