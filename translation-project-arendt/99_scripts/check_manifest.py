import json
with open('02_extracted_text/v7/manifest_continuity.json', 'r', encoding='utf-8') as f:
    m = json.load(f)
gaps = [t for t in m['page_transitions'] if not t['is_consecutive']]
print('Total transitions:', len(m['page_transitions']))
print('Non-consecutive (gaps):', len(gaps))
for g in gaps:
    print(f'  Page {g["from_page"]} -> {g["to_page"]} (gap of {g["to_page"] - g["from_page"] - 1} missing page(s))')
merged = [t for t in m['page_transitions'] if t['merged']]
print('Merged transitions:', len(merged))
