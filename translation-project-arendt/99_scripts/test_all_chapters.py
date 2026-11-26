import sys
sys.path.insert(0, '99_scripts')

from docx_builder_v2.parser import parse
from collections import Counter

chapters = ['ch01', 'ch02', 'ch03', 'ch04', 'ch05', 'ch06', 'ch07', 'ch08', 'ch09', 'ch10', 'ch11', 'ch12', 'ch13']

for ch in chapters:
    try:
        with open(f'04_translation/v2/{ch}/v1_{ch}_vi.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        model = parse(text, chapter_label=ch, vi_title=ch)
        types = Counter(n.type for n in model.nodes)
        headings = [n for n in model.nodes if n.type in ('section_h1', 'section_h2', 'section_h3', 'chapter', 'part')]
        print(f'{ch}: nodes={len(model.nodes)}, footnotes={len(model.footnotes)}, types={dict(types)}, headings={len(headings)}')
        if headings:
            for h in headings:
                print(f'  {h.type}: {h.text[:60]} (para: {h.metadata.get("para_id")}, page: {h.metadata.get("page")})')
    except Exception as e:
        print(f'{ch}: ERROR - {e}')