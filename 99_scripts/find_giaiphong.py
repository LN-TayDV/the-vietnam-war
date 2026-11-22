with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'giải phóng', text):
    start = max(0, m.start()-80)
    end = min(len(text), m.end()+80)
    context = text[start:end].replace('\n', ' ')
    with open('giaiphong_find.txt', 'a', encoding='utf-8') as f:
        f.write(f'Position {m.start()}: ...{context}...\n\n')