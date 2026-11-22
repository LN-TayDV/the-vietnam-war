with open('translation-project/04_translation/v1/ch11/v1_ch11_vi.txt', 'r', encoding='utf-8') as f:
    content = f.read()

import re
for term in ['đảo chính', 'tài chính', 'đại biểu', 'đảo chánh', 'tài chánh', 'dân biểu']:
    matches = [(m.start(), content[max(0,m.start()-30):m.end()+30]) for m in re.finditer(term, content)]
    if matches:
        with open('find_results.txt', 'a', encoding='utf-8') as out:
            for pos, ctx in matches:
                out.write('FOUND "' + term + '" at ' + str(pos) + ': ...' + ctx + '...\n')
    else:
        with open('find_results.txt', 'a', encoding='utf-8') as out:
            out.write('NOT FOUND: ' + term + '\n')