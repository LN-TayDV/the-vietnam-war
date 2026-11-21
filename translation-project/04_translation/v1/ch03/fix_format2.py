from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

docx_path = 'translation-project/09_docx/V1-C03_Ho-Chi-Minh-va-Su-Noi-Len-cua-Dang-Cong-San-Viet-Nam.docx'
img_path = 'translation-project/04_translation/v1/images/ch03_p72_img0.png'

doc = Document(docx_path)

for i, p in enumerate(doc.paragraphs):
    if 'Hình 3.1' in p.text:
        for run in p.runs:
            run.font.size = Pt(10)
            run.italic = True
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        new_p = doc.add_paragraph()
        new_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = new_p.add_run()
        run.add_picture(img_path, width=Inches(4.5))
        p._element.addnext(new_p._element)
        break  # Only insert once
    
    if 'Hồ Chí Minh luôn là một kẻ hữu phái' in p.text:
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(0)
        for run in p.runs:
            run.italic = True
            run.font.size = Pt(12)

doc.save(docx_path)
print('done')