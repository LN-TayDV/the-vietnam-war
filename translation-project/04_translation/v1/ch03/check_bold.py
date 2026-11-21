from docx import Document
doc = Document('translation-project/09_docx/V1-C03_Ho-Chi-Minh-va-Su-Noi-Len-cua-Dang-Cong-San-Viet-Nam.docx')
out = []
for p in doc.paragraphs:
    is_bold = False
    if p.runs:
        is_bold = p.runs[0].bold
    if is_bold:
        out.append('BOLD: ' + p.text[:60])
open('C:/Users/PC/AppData/Local/Temp/kilo/bold_check.txt','w',encoding='utf-8').write(chr(10).join(out))
print('done')