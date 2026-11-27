import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\02_extracted_text\v2\ch04_structure_REBUILT.json', encoding='utf-8') as f:
    data = json.load(f)

print('=== Paragraphs spanning multiple pages ===')
for p in data['paragraphs']:
    if p.get('page_start') != p.get('page_end'):
        print(f"  [{p['para_id']}] p{p['page_start']}-{p['page_end']}: {p['text'][:100]}")

print()
print('=== Paragraphs starting on problem pages ===')
for p in data['paragraphs']:
    if p['page_start'] in [138, 139, 155, 156, 157, 158, 159, 160, 162, 163]:
        print(f"  [{p['para_id']}] p{p['page_start']}-{p['page_end']}: {p['text'][:100]}")

print()
print('=== Artifacts ===')
for a in data.get('artifacts', []):
    print(f"  p{a['page']} y={a['y']:.1f} x={a['x']:.1f} sz={a['size']}: '{a['text']}'")

print()
print('=== Section numbers ===')
for sn in data.get('section_numbers', []):
    print(f"  p{sn['page']} y={sn['y']:.1f} x={sn['x']:.1f} sz={sn['size']}: '{sn['text']}'")

print()
print('=== Headings ===')
for h in data['headings']:
    print(f"  [{h['id']}] {h['type']} L{h['level']} (p{h['page']}, sz={h['size']}): {h['text'][:80]}")
