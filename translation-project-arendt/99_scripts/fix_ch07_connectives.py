"""
Apply Rule 25 connective replacements to ch07 parts, then re-consolidate.
  - ngược lại -> trái lại (tương phản)
  - tuy nhiên -> tuy vậy (chuyển ý)
  - hơn nữa -> vả lại (bổ sung)
All contexts reviewed; replacements are safe.
"""
import re
import os

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v1\ch07"
PARTS = ["_p1.txt", "_p2.txt", "_p3.txt", "_p4.txt", "_p5.txt",
         "_p6.txt", "_p7.txt", "_p8.txt", "_p9.txt"]

REPL = [
    (r'ng\u01b0\u1ee3c l\u1ea1i', 'tr\u00e1i l\u1ea1i'),   # ngược lại -> trái lại
    (r'tuy nhi\u00ean', 'tuy v\u1eady'),                   # tuy nhiên -> tuy vậy
    (r'h\u01a1n n\u1eefa', 'v\u1ea3 l\u1ea1i'),           # hơn nữa -> vả lại
]

for name in PARTS:
    path = os.path.join(BASE, name)
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    orig = txt
    counts = {}
    for pat, rep in REPL:
        txt, n = re.subn(pat, rep, txt)
        if n:
            counts[pat] = n
    if txt != orig:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
        print(f'{name}: {counts}')
print('Done.')