import sys
sys.path.insert(0, '99_scripts')

from docx_builder_v2.parser import parse

with open('04_translation/v2/ch12/v1_ch12_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

model = parse(text, chapter_label='Chương Mười Hai', vi_title='Toàn Trị Tại Quyền')
print(f'Nodes: {len(model.nodes)}')
print(f'Footnotes: {len(model.footnotes)}')
print(f'Footnote numbers: {sorted(model.footnotes.keys())}')

if 'inline_footnote_issues' in model.metadata:
    issues = model.metadata['inline_footnote_issues']
    print(f'Inline footnote issues: {len(issues)}')
    for issue in issues:
        print(f'  {issue}')
else:
    print('No inline footnote issues key in metadata')