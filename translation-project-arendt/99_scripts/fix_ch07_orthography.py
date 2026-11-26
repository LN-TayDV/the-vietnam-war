"""
Apply VNCH orthography fixes to ch07 part files, then re-consolidate.
Fixes per STYLE_GUIDE_PHAN_B.md:
  - chính phủ -> chánh phủ (Hiến pháp 1967)
  - Mặc dù / mặc dù -> Mặc dầu / mặc dầu (Rule 25: dầu/dẫu thay mặc dù)
  - standalone dù (conjunction) -> dầu (Rule 25)
  - hành chính -> hành chánh (VNCH administrative spelling)
"""
import re
import os

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v1\ch07"
PARTS = ["_p1.txt", "_p2.txt", "_p3.txt", "_p4.txt", "_p5.txt",
         "_p6.txt", "_p7.txt", "_p8.txt", "_p9.txt"]

# \b works in Python 3 re for Unicode (Vietnamese diacritics are word chars)
du_re = re.compile(r'\bd\u00f9\b')

total_changes = {}
for name in PARTS:
    path = os.path.join(BASE, name)
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    orig = txt
    c = {}
    # 1. Mặc dù -> Mặc dầu (do before standalone dù)
    txt, n = re.subn(r'M\u1eb7c d\u00f9', 'M\u1eb7c d\u1ea7u', txt); c['Mặc dù'] = n
    txt, n = re.subn(r'm\u1eb7c d\u00f9', 'm\u1eb7c d\u1ea7u', txt); c['mặc dù'] = n
    # 2. chính phủ -> chánh phủ
    txt, n = re.subn(r'ch\u00ednh ph\u1ee7', 'ch\u00e1nh ph\u1ee7', txt); c['chính phủ'] = n
    # 3. hành chính -> hành chánh
    txt, n = re.subn(r'h\u00e0nh ch\u00ednh', 'h\u00e0nh ch\u00e1nh', txt); c['hành chính'] = n
    # 4. standalone dù -> dầu (remaining conjunctions)
    txt, n = du_re.subn('d\u1ea7u', txt); c['dù'] = n
    if txt != orig:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
    total_changes[name] = {k: v for k, v in c.items() if v}

for name, ch in total_changes.items():
    if ch:
        print(f'{name}: {ch}')
print('\nDone. Re-consolidating...')