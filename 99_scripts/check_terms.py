with open('translation-project/04_translation/v1/ch11/v1_ch11_vi.txt', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    'chánh phủ',
    'đảo chánh',
    'chánh trị',
    'tài chánh',
    'dân biểu',
    'độc lập',
    'ngôn ngữ lưỡng lự',
    'Trung ương Đảng',
    'căn cứ kiên cố',
    'Thái',
    'Sư 1 Xích lô',
    'người',
    'chính quyền cộng sản',
    'nêu ra',
    'đồng bằng',
    'dầu',
    'tuy vậy',
    'chớ không',
]

results = []
for term in checks:
    if term in content:
        results.append('OK: ' + term)
    else:
        results.append('MISSING: ' + term)

with open('check_results.txt', 'w', encoding='utf-8') as f:
    for r in results:
        f.write(r + '\n')

import re
paras = len(re.findall(r'--- \[V1C11-P\d+\]', content))
with open('check_results.txt', 'a', encoding='utf-8') as f:
    f.write('Paragraphs: ' + str(paras) + '\n')