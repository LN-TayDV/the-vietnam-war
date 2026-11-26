import zipfile
import re
import os
from collections import Counter

# Check if V2 master docx exists
for f in os.listdir('09_docx'):
    if 'Origins' in f and 'V2' in f:
        print(f'Found V2 master: {f}')
        with zipfile.ZipFile(f'09_docx/{f}') as z:
            doc_content = z.read('word/document.xml').decode('utf-8', 'replace')
            styles = re.findall(r'<w:pStyle w:val="([^"]+)"/>', doc_content)
            cnt = Counter(styles)
            for k, v in sorted(cnt.items()):
                print(f'  {k}: {v}')