import sys
sys.path.insert(0, '99_scripts')

from docx_builder_v2.parser import parse

chapters = ['ch04', 'ch12', 'ch13']

for ch in chapters:
    try:
        with open(f'04_translation/v2/{ch}/v1_{ch}_vi.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        model = parse(text, chapter_label=ch, vi_title=ch)
        
        # Check cross-page issues
        if 'cross_page_issues' in model.metadata:
            issues = model.metadata['cross_page_issues']
            print(f'{ch}: cross_page_issues={len(issues)}')
            for issue in issues[:5]:
                print(f'  {issue}')
        
        # Check duplicate issues
        if 'duplicate_issues' in model.metadata:
            issues = model.metadata['duplicate_issues']
            print(f'{ch}: duplicate_issues={len(issues)}')
            for issue in issues:
                print(f'  {issue}')
                
    except Exception as e:
        print(f'{ch}: ERROR - {e}')