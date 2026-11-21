import re

# VNCH terminology checks
CHECKS = [
    # (pattern, replacement, description, severity)
    (r'\bchính trị\b', 'chánh trị', 'Political terminology', 'CRITICAL'),
    (r'\bchính phủ\b', 'chánh phủ', 'Government terminology', 'CRITICAL'),
    (r'\bchính đảng\b', 'chánh đảng', 'Party terminology', 'CRITICAL'),
    (r'\bđảo chính\b', 'đảo chánh', 'Coup terminology', 'CRITICAL'),
    (r'\btài chính\b', 'tài chánh', 'Finance terminology', 'CRITICAL'),
    (r'\blương hưu\b', 'hưu bổng', 'Pension terminology', 'CRITICAL'),
    (r'\bbất động sản\b', 'địa ốc', 'Real estate terminology', 'CRITICAL'),
    (r'\bngân sách\b(?!.*(?:quốc gia|tỉnh|huyện|xã))', 'ngân khố', 'Treasury vs budget', 'MAJOR'),
    (r'\bđại biểu\b(?!.*Quốc hội)', 'dân biểu', 'Representative terminology', 'CRITICAL'),
    (r'\bgiải phóng\b', 'độc lập/kháng cự', 'Liberation terminology', 'MAJOR'),
    (r'\bđồng chí\b', 'người đồng chí/đồng đạo', 'Comrade terminology', 'MAJOR'),
    (r'\bnày\b(?!.*(?:trong|ngoài|trước|sau))', 'nầy', 'Demonstrative pronoun', 'CRITICAL'),
    (r'\bmà\b(?=\s+(?:không|chẳng|đâu))', 'chớ', 'Contrastive conjunction', 'MAJOR'),
    (r'\bmặc dù\b', 'dầu/dẫu', 'Concessive conjunction', 'MAJOR'),
    (r'\btuy nhiên\b', 'tuy vậy/đã vậy', 'Adversative conjunction', 'MAJOR'),
    (r'\bvì vậy\b', 'bởi thế/do đó', 'Consequential conjunction', 'MAJOR'),
    (r'\bhơn nữa\b', 'vả/lại', 'Additive conjunction', 'MAJOR'),
    (r'\bngười ấy\b', 'người ấy/ông ấy/bà ấy', 'Third person pronoun', 'MINOR'),
    (r'\bhắn\b', 'người ấy/ông ấy', 'Third person pronoun (avoid)', 'MINOR'),
    (r'\bAnnam\b', 'Trung Kỳ (Annam)', 'Colonial name', 'MAJOR'),
    (r'\bTonkin\b', 'Bắc Kỳ (Tonkin)', 'Colonial name', 'MAJOR'),
    (r'\bCochinchina\b', 'Nam Kỳ (Cochinchina)', 'Colonial name', 'MAJOR'),
    (r'\bCochinchine\b', 'Nam Kỳ (Cochinchine)', 'Colonial name', 'MAJOR'),
    (r'\bIndochine\b', 'Đông Dương (Indochine)', 'Colonial name', 'MAJOR'),
    (r'\bquốc gia\b(?!.*VNCH)', 'quốc gia/dân tộc', 'Nation terminology', 'MINOR'),
]

def audit_file(filepath, label):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = []
    for pattern, replacement, desc, severity in CHECKS:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            for m in matches[:10]:  # Limit to first 10 per pattern
                start = max(0, m.start() - 50)
                end = min(len(content), m.end() + 50)
                context = content[start:end].replace('\n', ' ')
                results.append({
                    'file': label,
                    'pattern': pattern,
                    'found': m.group(),
                    'replacement': replacement,
                    'description': desc,
                    'severity': severity,
                    'context': context
                })
    return results

# Audit all translation files
all_results = []
for ch in ['ch01', 'ch02', 'ch03', 'ch04', 'ch05', 'ch06']:
    filepath = f'translation-project/04_translation/v1/{ch}/v1_{ch}_vi.txt'
    try:
        results = audit_file(filepath, ch)
        all_results.extend(results)
        print(f'{ch}: {len(results)} issues found')
    except Exception as e:
        print(f'{ch}: ERROR - {e}')

# Write report
with open('C:\\Users\\PC\\AppData\\Local\\Temp\\kilo\\vnch_audit_report.txt', 'w', encoding='utf-8') as f:
    f.write('VNCH TERMINOLOGY AUDIT REPORT\n')
    f.write('='*60 + '\n\n')
    
    # Group by severity
    for severity in ['CRITICAL', 'MAJOR', 'MINOR']:
        sev_results = [r for r in all_results if r['severity'] == severity]
        f.write(f'\n{severity} ISSUES ({len(sev_results)}):\n')
        f.write('-'*60 + '\n')
        for r in sev_results:
            f.write(f"File: {r['file']}\n")
            f.write(f"  Pattern: {r['pattern']} -> {r['replacement']}\n")
            f.write(f"  Found: '{r['found']}'\n")
            f.write(f"  Description: {r['description']}\n")
            f.write(f"  Context: ...{r['context']}...\n\n")

print(f'\nTotal issues: {len(all_results)}')
print('Report written to C:\\Users\\PC\\AppData\\Local\\Temp\\kilo\\vnch_audit_report.txt')