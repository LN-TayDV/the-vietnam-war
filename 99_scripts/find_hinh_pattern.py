with open('translation-project/99_scripts/build_chapter_docx.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'hinh_pattern', text):
    start = max(0, m.start()-50)
    end = min(len(text), m.end()+200)
    print(text[start:end])
    print('---')