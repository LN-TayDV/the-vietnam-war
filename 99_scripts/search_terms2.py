with open('translation-project/04_translation/v1/ch11/v1_ch11_vi.txt', 'r', encoding='utf-8') as f:
    content = f.read()

import re
with open('search_results2.txt', 'w', encoding='utf-8') as out:
    for term in ['chánh phủ', 'chánh trị', 'tài chánh', 'dân biểu', 'đảo chánh']:
        matches = [(m.start(), content[max(0,m.start()-40):m.end()+40]) for m in re.finditer(term, content)]
        if matches:
            for pos, ctx in matches[:3]:
                out.write('FOUND: ' + term + ' at ' + str(pos) + ': ' + ctx + '\n')
        else:
            out.write('NOT FOUND: ' + term + '\n')