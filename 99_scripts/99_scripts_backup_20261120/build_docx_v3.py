import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_docx(chapter_num, chapter_title, author, src_file, vi_file, output_file):
    """Build DOCX from translation file using source for markers."""
    
    # Read translation
    with open(vi_file, 'r', encoding='utf-8') as f:
        vi_content = f.read()
    
    # Read source for markers
    with open(src_file, 'r', encoding='utf-8') as f:
        src_content = f.read()
    
    # Split translation by paragraph markers
    vi_paras = re.split(r'--- \[V1C\d\d-P\d+\]', vi_content)
    vi_paras = [p.strip() for p in vi_paras[1:] if p.strip()]
    
    # Split source by paragraph markers
    src_paras = re.split(r'--- \[V1C\d\d-P\d+\]', src_content)
    src_paras = [p.strip() for p in src_paras[1:] if p.strip()]
    
    print(f'Chapter {chapter_num}: {len(src_paras)} source paras, {len(vi_paras)} translation paras')
    
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
    
    # Process each paragraph pair
    footnote_mode = False
    footnotes = []
    
    for i, (src_para, vi_para) in enumerate(zip(src_paras, vi_paras)):
        if footnote_mode or vi_para.startswith('--- [Cước chú'):
            footnote_mode = True
            footnotes.append(vi_para)
            continue
        
        # Extract marker info from source
        marker_match = re.search(r'(\(trang [\d\-]+\)\s*---.*?)(?=\n)', src_para)
        if marker_match:
            marker = marker_match.group(1)
        else:
            marker = '(trang ???) ---'
        
        is_heading = '— đề mục' in src_para or 'heading' in src_para.lower()
        if is_heading:
            marker = marker.replace('---', '— đề mục ---')
        
        # Extract content from source (to verify alignment)
        src_content = src_para
        if marker_match:
            src_content = src_para[marker_match.end():].strip()
        
        # Use translation content
        vi_content = vi_para.strip()
        
        if is_heading and vi_content:
            # Heading paragraph
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(vi_content)
            run.bold = True
            run.font.size = Pt(13)
            run.font.name = 'Times New Roman'
        elif vi_content and vi_content not in ['[CẦN DỊCH - MISSING]', '[MISSING]', '[EMPTY]']:
            # Body paragraph
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Inches(0.5)
            run = p.add_run(vi_content)
            run.font.size = Pt(12)
            run.font.name = 'Times New Roman'
    
    # Add footnotes
    if footnotes:
        doc.add_page_break()
        fn_heading = doc.add_paragraph()
        fn_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = fn_heading.add_run('CƯỚC CHÚ')
        run.bold = True
        run.font.size = Pt(14)
        run.font.name = 'Times New Roman'
        
        for block in footnotes:
            lines = block.strip().split('\n')
            for line in lines[1:]:
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