import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

def build_docx(chapter_num, chapter_title, author, src_file, vi_file, output_file):
    """Build DOCX from translation file."""
    
    # Read translation
    with open(vi_file, 'r', encoding='utf-8') as f:
        vi_content = f.read()
    
    # Read source for metadata
    with open(src_file, 'r', encoding='utf-8') as f:
        src_content = f.read()
    
    # Split translation into paragraphs
    vi_paras = re.split(r'--- \[V1C\d\d-P\d+\]', vi_content)
    vi_paras = [p.strip() for p in vi_paras[1:] if p.strip()]
    
    # Create document
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.space_before = Pt(0)
    
    # Title page
    for _ in range(4):
        doc.add_paragraph('')
    
    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_para.add_run(f'The Cambridge History of the Vietnam War')
    run.bold = True
    run.font.size = Pt(24)
    run.font.name = 'Times New Roman'
    
    doc.add_paragraph('')
    
    vol_para = doc.add_paragraph()
    vol_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = vol_para.add_run(f'Volume I')
    run.bold = True
    run.font.size = Pt(18)
    run.font.name = 'Times New Roman'
    
    doc.add_paragraph('')
    
    ch_para = doc.add_paragraph()
    ch_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = ch_para.add_run(f'Chương {chapter_num}: {chapter_title}')
    run.bold = True
    run.font.size = Pt(16)
    run.font.name = 'Times New Roman'
    
    doc.add_paragraph('')
    
    auth_para = doc.add_paragraph()
    auth_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = auth_para.add_run(f'Tác giả: {author}')
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    
    doc.add_paragraph('')
    doc.add_paragraph('')
    
    trans_para = doc.add_paragraph()
    trans_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = trans_para.add_run('Bản dịch tiếng Việt (Văn phong VNCH)')
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    run.italic = True
    
    doc.add_page_break()
    
    # Chapter content
    for i, para in enumerate(vi_paras):
        # Skip if it's just footnotes
        if para.startswith('--- [Cước chú'):
            break
        
        # Extract marker and content
        lines = para.split('\n', 1)
        if len(lines) < 2:
            continue
        
        marker = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ''
        
        # Check if heading
        is_heading = '— đề mục' in marker
        
        if is_heading:
            # Heading paragraph
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(content)
            run.bold = True
            run.font.size = Pt(13)
            run.font.name = 'Times New Roman'
        else:
            # Body paragraph
            if content and content != '[CẦN DỊCH - MISSING]' and content != '[MISSING]':
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Inches(0.5)
                run = p.add_run(content)
                run.font.size = Pt(12)
                run.font.name = 'Times New Roman'
    
    # Add footnotes
    footnote_blocks = re.findall(r'--- \[Cước chú.*?---', vi_content, re.DOTALL)
    if footnote_blocks:
        doc.add_page_break()
        fn_heading = doc.add_paragraph()
        fn_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = fn_heading.add_run('CƯỚC CHÚ')
        run.bold = True
        run.font.size = Pt(14)
        run.font.name = 'Times New Roman'
        
        for block in footnote_blocks:
            # Parse footnote block
            lines = block.strip().split('\n')
            for line in lines[1:]:  # Skip the "--- [Cước chú..." line
                line = line.strip()
                if line and not line.startswith('---'):
                    p = doc.add_paragraph()
                    p.paragraph_format.space_after = Pt(2)
                    run = p.add_run(line)
                    run.font.size = Pt(10)
                    run.font.name = 'Times New Roman'
    
    # Save
    doc.save(output_file)
    print(f'Saved: {output_file}')

# Build all 6 chapters
chapters = [
    (1, 'Trí nhớ, Truyền thống và Sử học về "Việt Nam"', 'Liam C. Kelley',
     'translation-project/04_translation/v1/ch01/v1_ch01_src.txt',
     'translation-project/04_translation/v1/ch01/v1_ch01_vi_FINAL.txt',
     'translation-project/04_translation/v1/ch01/Ch01_VNCH.docx'),
    (2, 'Cách mạng và Chiến tranh: Việt Nam 1930–1945', 'Christopher E. Goscha',
     'translation-project/04_translation/v1/ch02/v1_ch02_src.txt',
     'translation-project/04_translation/v1/ch02/v1_ch02_vi_FINAL.txt',
     'translation-project/04_translation/v1/ch02/Ch02_VNCH.docx'),
    (3, 'Hồ Chí Minh và Trường Chinh: Nhận định lại Quan hệ của họ', 'Pierre Brocheux',
     'translation-project/04_translation/v1/ch03/v1_ch03_src.txt',
     'translation-project/04_translation/v1/ch03/v1_ch03_vi_FINAL.txt',
     'translation-project/04_translation/v1/ch03/Ch03_VNCH.docx'),
    (4, 'Chiến tranh Thái Bình Dương và Đông Dương: 1940–1945', 'Stein Tønnesson',
     'translation-project/04_translation/v1/ch04/v1_ch04_src.txt',
     'translation-project/04_translation/v1/ch04/v1_ch04_vi_FINAL.txt',
     'translation-project/04_translation/v1/ch04/Ch04_VNCH.docx'),
    (5, 'Cách mạng Tháng Tám năm 1945', 'Stein Tønnesson',
     'translation-project/04_translation/v1/ch05/v1_ch05_src.txt',
     'translation-project/04_translation/v1/ch05/v1_ch05_vi_FINAL.txt',
     'translation-project/04_translation/v1/ch05/Ch05_VNCH.docx'),
    (6, 'Cách mạng Tháng Tám và Khởi đầu Chiến tranh Đông Dương', 'Stein Tønnesson',
     'translation-project/04_translation/v1/ch06/v1_ch06_src.txt',
     'translation-project/04_translation/v1/ch06/v1_ch06_vi_FINAL.txt',
     'translation-project/04_translation/v1/ch06/Ch06_VNCH.docx'),
]

for ch in chapters:
    try:
        build_docx(*ch)
    except Exception as e:
        print(f'Error building {ch[0]}: {e}')

print('\nAll DOCX files built.')