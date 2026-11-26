import zipfile
import re
import os

chapters = ['V2-01', 'V2-02', 'V2-03', 'V2-04', 'V2-05', 'V2-06', 'V2-07', 'V2-08', 'V2-09', 'V2-10', 'V2-11', 'V2-12', 'V2-13']

for ch in chapters:
    docx_files = [f for f in os.listdir('09_docx') if f.startswith(ch)]
    if docx_files:
        fname = docx_files[0]
        with zipfile.ZipFile(f'09_docx/{fname}') as z:
            # Check footnotes
            if 'word/footnotes.xml' in z.namelist():
                fn_content = z.read('word/footnotes.xml').decode('utf-8', 'replace')
                fn_count = len(re.findall(r'<w:footnote w:id=', fn_content))
            else:
                fn_count = 0
            
            # Check document.xml for structure
            doc_content = z.read('word/document.xml').decode('utf-8', 'replace')
            body_count = len(re.findall(r'<w:pStyle w:val="BodyText"/>', doc_content))
            block_count = len(re.findall(r'<w:pStyle w:val="BlockQuote"/>', doc_content))
            heading1 = len(re.findall(r'<w:pStyle w:val="Heading1"/>', doc_content))
            heading2 = len(re.findall(r'<w:pStyle w:val="Heading2"/>', doc_content))
            heading3 = len(re.findall(r'<w:pStyle w:val="Heading3"/>', doc_content))
            
            print(f'{ch}: footnotes={fn_count}, body={body_count}, block={block_count}, H1={heading1}, H2={heading2}, H3={heading3}')