import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\02_extracted_text\v2\ch04_structure_REBUILT.json', encoding='utf-8') as f:
    data = json.load(f)

print('=== All paragraphs on page 145 ===')
for p in data['paragraphs']:
    if p['page_start'] == 145:
        print(f"  [{p['para_id']}] p{p['page_start']}-{p['page_end']}: {p['text'][:150]}")

print()
print('=== Short/suspicious paragraphs (len < 30 chars) ===')
for p in data['paragraphs']:
    if len(p['text'].strip()) < 30:
        print(f"  [{p['para_id']}] p{p['page_start']}-{p['page_end']} len={len(p['text'].strip())}: '{p['text'].strip()}'")

print()
print('=== Total paragraphs:', len(data['paragraphs']))
