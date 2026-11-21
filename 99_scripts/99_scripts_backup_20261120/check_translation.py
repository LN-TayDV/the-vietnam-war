import sys
import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch06\v1_ch06_vi.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Check forbidden terms
forbidden = ['chính trị', 'chính phủ', 'đại biểu Quốc hội', 'đại biểu', 'tài chính', 'bất động sản', 'lương hưu', 'ngân sách', 'đảo chính', 'giải phóng', 'đồng chí']
found = []
for term in forbidden:
    if term in content:
        found.append(term)

# Check required terms
required = ['chánh trị', 'chánh phủ', 'dân biểu', 'nghị sĩ', 'tài chánh', 'địa ốc', 'hưu bổng', 'ngân khố', 'đảo chánh', 'Nam Kỳ', 'Trung Kỳ', 'Bắc Kỳ']
req_counts = {}
for term in required:
    count = content.count(term)
    if count > 0:
        req_counts[term] = count

# Count paragraphs properly
paras = re.findall(r'--- \[V1C06-P\d+\] \(trang \d+\) ---', content)

# Write results to file
with open(r'C:\Users\PC\AppData\Local\Temp\kilo\check_results.txt', 'w', encoding='utf-8') as f:
    f.write(f'Forbidden terms found: {found}\n')
    f.write(f'Required term counts: {req_counts}\n')
    f.write(f'Paragraphs: {len(paras)}\n')
    for p in paras:
        f.write(f'  {p}\n')