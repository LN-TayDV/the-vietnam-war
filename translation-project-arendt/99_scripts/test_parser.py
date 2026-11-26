from docx_builder_v2.parser import parse

with open('04_translation/v2/ch12/v1_ch12_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

model = parse(text, chapter_label='Chương Mười Hai', vi_title='Toàn Trị Tại Quyền')
print(f'Nodes: {len(model.nodes)}')
print(f'Footnotes: {len(model.footnotes)}')

# Count node types
from collections import Counter
types = Counter(n.type for n in model.nodes)
print(f'Node types: {dict(types)}')

# Check for section headings
headings = [n for n in model.nodes if n.type in ('section_h1', 'section_h2', 'section_h3', 'chapter', 'part')]
print(f'Headings: {len(headings)}')
for h in headings:
    meta = h.metadata
    para_id = meta.get('para_id')
    page = meta.get('page')
    print(f'  {h.type}: {h.text[:80]} (para: {para_id}, page: {page})')

# Check for duplicate headings
from docx_builder_v2.parser import validate_heading_hierarchy
validate_heading_hierarchy(model)
if 'heading_issues' in model.metadata:
    for issue in model.metadata['heading_issues']:
        print(f'Issue: {issue}')