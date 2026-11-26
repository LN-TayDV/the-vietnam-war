import sys
sys.path.insert(0, '99_scripts')

from docx_builder_v2.parser import parse

chapters = ['ch03', 'ch05', 'ch06', 'ch07', 'ch10', 'ch11']

for ch in chapters:
    try:
        with open(f'04_translation/v2/{ch}/v1_{ch}_vi.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        model = parse(text, chapter_label=ch, vi_title=ch)
        
        # Check duplicate issues
        if 'duplicate_issues' in model.metadata:
            issues = model.metadata['duplicate_issues']
            print(f'{ch}: duplicate_issues={len(issues)}')
            for issue in issues:
                print(f'  {issue}')
        else:
            print(f'{ch}: duplicate_issues=0')
                
    except Exception as e:
        print(f'{ch}: ERROR - {e}')