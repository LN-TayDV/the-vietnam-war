import zipfile
import re
import os
from collections import Counter

chapters = ['V2-01', 'V2-02', 'V2-03', 'V2-04', 'V2-05', 'V2-06', 'V2-07', 'V2-08', 'V2-09', 'V2-10', 'V2-11', 'V2-12', 'V2-13']

for ch in chapters:
    docx_files = [f for f in os.listdir('09_docx') if f.startswith(ch)]
    if docx_files:
        fname = docx_files[0]
        with zipfile.ZipFile(f'09_docx/{fname}') as z:
            doc_content = z.read('word/document.xml').decode('utf-8', 'replace')
            styles = re.findall(r'<w:pStyle w:val="([^"]+)"/>', doc_content)
            cnt = Counter(styles)
            # Check for key styles
            has_title = 'ArendtBookTitle' in cnt
            has_chap_num = 'ChapterNumber' in cnt
            has_chap_title = 'ChapterTitle' in cnt
            has_author = 'Author' in cnt
            body_count = cnt.get('BodyText', 0)
            fn_count = 0
            if 'word/footnotes.xml' in z.namelist():
                fn_content = z.read('word/footnotes.xml').decode('utf-8', 'replace')
                fn_count = len(re.findall(r'<w:footnote w:id=', fn_content))
            print(f'{ch}: title={has_title}, chap_num={has_chap_num}, chap_title={has_chap_title}, author={has_author}, body={body_count}, footnotes={fn_count}')