from docx import Document
doc = Document('translation-project/09_docx/V1-C03_Ho-Chi-Minh-va-Su-Noi-Len-cua-Dang-Cong-San-Viet-Nam.docx')
out = []
for p in doc.paragraphs[-8:]:
    out.append(repr(p.text[:80]))
open('C:/Users/PC/AppData/Local/Temp/kilo/end_check.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')