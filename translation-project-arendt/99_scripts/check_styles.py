import zipfile
import re
from collections import Counter

with zipfile.ZipFile('09_docx/V2-04_Vu-Dreyfus.docx') as z:
    doc_content = z.read('word/document.xml').decode('utf-8', 'replace')
    styles = re.findall(r'<w:pStyle w:val="([^"]+)"/>', doc_content)
    cnt = Counter(styles)
    for k, v in sorted(cnt.items()):
        print(f'  {k}: {v}')