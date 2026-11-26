import zipfile
import re
import os
from collections import Counter

# Final validation of all V2 DOCX files
chapters = ['V2-01', 'V2-02', 'V2-03', 'V2-04', 'V2-05', 'V2-06', 'V2-07', 'V2-08', 'V2-09', 'V2-10', 'V2-11', 'V2-12', 'V2-13']

total_footnotes = 0
total_body = 0
total_block = 0
for ch in chapters:
    docx_files = [f for f in os.listdir('09_docx') if f.startswith(ch)]
    if docx_files:
        fname = docx_files[0]
        with zipfile.ZipFile(f'09_docx/{fname}') as z:
            if 'word/footnotes.xml' in z.namelist():
                fn_content = z.read('word/footnotes.xml').decode('utf-8', 'replace')
                fn_count = len(re.findall(r'<w:footnote w:id=', fn_content))
                total_footnotes += fn_count
            doc_content = z.read('word/document.xml').decode('utf-8', 'replace')
            styles = re.findall(r'<w:pStyle w:val="([^"]+)"/>', doc_content)
            cnt = Counter(styles)
            total_body += cnt.get('BodyText', 0)
            total_block += cnt.get('BlockQuote', 0)
            if cnt.get('ArendtBookTitle'):
                print(f'{ch}: HAS TITLE BLOCK')
            if cnt.get('ChapterNumber'):
                print(f'{ch}: HAS CHAPTER NUMBER')
            if cnt.get('ChapterTitle'):
                print(f'{ch}: HAS CHAPTER TITLE')
            if cnt.get('Author'):
                print(f'{ch}: HAS AUTHOR')

print(f'\nTOTAL: footnotes={total_footnotes}, body={total_body}, block={total_block}')