import json
import sys
import re
from pathlib import Path

root = Path('.')
ch_dir = root / 'translation-project' / '04_translation' / 'v1' / 'ch10'
file_path = ch_dir / 'v1_ch10_vi.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

VNCH_RULES = [
    {'id': 'VNCH-01', 'category': 'core', 'pattern': r'\bchính trị\b', 'replacement': 'chánh trị', 'severity': 'CRITICAL'},
    {'id': 'VNCH-02', 'category': 'core', 'pattern': r'\bchính phủ\b', 'replacement': 'chánh phủ', 'severity': 'CRITICAL'},
    {'id': 'VNCH-03', 'category': 'core', 'pattern': r'\bchính đảng\b', 'replacement': 'chánh đảng', 'severity': 'CRITICAL'},
    {'id': 'VNCH-04', 'category': 'core', 'pattern': r'\bđảo chính\b', 'replacement': 'đảo chánh', 'severity': 'CRITICAL'},
    {'id': 'VNCH-05', 'category': 'core', 'pattern': r'\btài chính\b', 'replacement': 'tài chánh', 'severity': 'CRITICAL'},
    {'id': 'VNCH-06', 'category': 'core', 'pattern': r'\blương hưu\b', 'replacement': 'hưu bổng', 'severity': 'CRITICAL'},
    {'id': 'VNCH-07', 'category': 'core', 'pattern': r'\bbất động sản\b', 'replacement': 'địa ốc', 'severity': 'CRITICAL'},
    {'id': 'VNCH-08', 'category': 'core', 'pattern': r'\bđại biểu\b', 'replacement': 'dân biểu', 'severity': 'CRITICAL'},
    {'id': 'VNCH-09', 'category': 'core', 'pattern': r'\bngân sách\b(?=\s*(cơ quan|ngân khố|ngân hàng))', 'replacement': 'ngân khố', 'severity': 'CRITICAL'},
    {'id': 'VNCH-10', 'category': 'north_south', 'pattern': r'\bgiải phóng\b', 'replacement': 'độc lập/kháng cự', 'severity': 'MAJOR', 'exceptions': ['cờ giải phóng', 'quân giải phóng', 'mặt trận giải phóng']},
    {'id': 'VNCH-11', 'category': 'north_south', 'pattern': r'\bđồng chí\b', 'replacement': 'đồng đạo', 'severity': 'MAJOR', 'exceptions': ['thanh niên cách mạng đồng chí hội', 'đồng chí hội']},
    {'id': 'VNCH-12', 'category': 'north_south', 'pattern': r'\bnày\b(?!.*(?:trong|ngoài|trước|sau)\s+nầy)', 'replacement': 'nầy', 'severity': 'CRITICAL'},
    {'id': 'VNCH-13', 'category': 'north_south', 'pattern': r'\bmặc dù\b', 'replacement': 'dầu/dẫu', 'severity': 'MAJOR'},
    {'id': 'VNCH-14', 'category': 'north_south', 'pattern': r'\btuy nhiên\b', 'replacement': 'tuy vậy/đã vậy', 'severity': 'MAJOR'},
    {'id': 'VNCH-15', 'category': 'north_south', 'pattern': r'\bvì vậy\b', 'replacement': 'bởi thế/do đó', 'severity': 'MAJOR'},
    {'id': 'VNCH-16', 'category': 'north_south', 'pattern': r'\bhơn nữa\b', 'replacement': 'vả/lại', 'severity': 'MAJOR'},
    {'id': 'VNCH-17', 'category': 'north_south', 'pattern': r'\bngược lại\b', 'replacement': 'trái lại', 'severity': 'MAJOR'},
    {'id': 'VNCH-18', 'category': 'north_south', 'pattern': r'\bmà không\b', 'replacement': 'chớ không', 'severity': 'MAJOR'},
    {'id': 'VNCH-19', 'category': 'north_south', 'pattern': r'\bmà chẳng\b', 'replacement': 'chớ chẳng', 'severity': 'MAJOR'},
    {'id': 'VNCH-20', 'category': 'north_south', 'pattern': r'\bmà đâu\b', 'replacement': 'chớ đâu', 'severity': 'MAJOR'},
    {'id': 'VNCH-21', 'category': 'colonial', 'pattern': r'\bAnnam\b', 'replacement': 'Trung Kỳ (Annam)', 'severity': 'MAJOR'},
    {'id': 'VNCH-22', 'category': 'colonial', 'pattern': r'\bTonkin\b', 'replacement': 'Bắc Kỳ (Tonkin)', 'severity': 'MAJOR'},
    {'id': 'VNCH-23', 'category': 'colonial', 'pattern': r'\bCochinchina\b', 'replacement': 'Nam Kỳ (Cochinchina)', 'severity': 'MAJOR'},
    {'id': 'VNCH-24', 'category': 'colonial', 'pattern': r'\bCochinchine\b', 'replacement': 'Nam Kỳ (Cochinchine)', 'severity': 'MAJOR'},
    {'id': 'VNCH-25', 'category': 'colonial', 'pattern': r'\bIndochine\b', 'replacement': 'Đông Dương (Indochine)', 'severity': 'MAJOR'},
    {'id': 'VNCH-26', 'category': 'colonial', 'pattern': r'\bIndochina\b', 'replacement': 'Đông Dương (Indochina)', 'severity': 'MAJOR'},
    {'id': 'VNCH-27', 'category': 'grammar', 'pattern': r'\bmột\s+(sách|ký|người|ngày|năm|cái|cuốn|bài)\b(?! (cuốn|cái|con|người|ngài|cây|cục|bài))', 'replacement': 'một [classifier] + noun', 'severity': 'MINOR'},
    {'id': 'VNCH-28', 'category': 'grammar', 'pattern': r'\b(năm|ngày|trước|sau)\s+này\b(?! (trong|ngoài|trước|sau)\s+nầy)', 'replacement': 'nầy', 'severity': 'MINOR'},
    {'id': 'VNCH-29', 'category': 'grammar', 'pattern': r'\bđang\s+\w+(?!\s+(xong|tiến hành|đang))', 'replacement': 'đang... xong/tiến hành', 'severity': 'MINOR'},
    {'id': 'VNCH-30', 'category': 'grammar', 'pattern': r'\b(hắn|y|nó)\b.*?(?:lập luận|nói|cho rằng|tin rằng|là)', 'replacement': 'người ấy/ông ấy/bà ấy', 'severity': 'MINOR'},
]

issues = []
for rule in VNCH_RULES:
    pattern = re.compile(rule['pattern'], re.IGNORECASE)
    matches = list(pattern.finditer(text))
    for match in matches:
        skip = False
        if 'exceptions' in rule:
            context = text[max(0, match.start()-50):match.end()+50].lower()
            for exc in rule['exceptions']:
                if exc.lower() in context:
                    skip = True
                    break
        if skip:
            continue
        if rule.get('category') == 'colonial':
            context_lower = text[max(0, match.start()-100):match.end()+100].lower()
            vnch_forms = {
                'annam': 'trung kỳ', 'tonkin': 'bắc kỳ', 'cochinchina': 'nam kỳ',
                'cochinchine': 'nam kỳ', 'indochine': 'đông dương', 'indochina': 'đông dương'
            }
            term_lower = match.group().lower()
            if term_lower in vnch_forms:
                vnch_form = vnch_forms[term_lower]
                if vnch_form in context_lower and '(' in context_lower:
                    continue
        start = max(0, match.start() - 80)
        end = min(len(text), match.end() + 80)
        context = text[start:end].strip()
        issues.append({
            'rule_id': rule['id'],
            'category': rule.get('category', ''),
            'severity': rule['severity'],
            'found': match.group(),
            'expected': rule['replacement'],
            'position': match.start(),
            'context': context[:200],
        })

by_severity = {'CRITICAL': [], 'MAJOR': [], 'MINOR': []}
for issue in issues:
    by_severity[issue['severity']].append(issue)

# Write to file to avoid encoding issues
with open('vnch_issues_detail.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total issues: {len(issues)}\n')
    f.write(f'CRITICAL: {len(by_severity["CRITICAL"])}\n')
    f.write(f'MAJOR: {len(by_severity["MAJOR"])}\n')
    f.write(f'MINOR: {len(by_severity["MINOR"])}\n\n')
    for issue in issues:
        f.write(f'[{issue["severity"]}] {issue["rule_id"]}: "{issue["found"]}" -> "{issue["expected"]}"\n')
        f.write(f'  Category: {issue["category"]}\n')
        f.write(f'  Position: {issue["position"]}\n')
        f.write(f'  Context: ...{issue["context"][:200]}...\n\n')

print(f'Total issues: {len(issues)}')
print(f'CRITICAL: {len(by_severity["CRITICAL"])}')
print(f'MAJOR: {len(by_severity["MAJOR"])}')
print(f'MINOR: {len(by_severity["MINOR"])}')
print('Details written to vnch_issues_detail.txt')