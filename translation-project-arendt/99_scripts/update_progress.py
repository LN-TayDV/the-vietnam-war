import json

path = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\00_plan\progress.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['chapters']['ch13']['notes'] = ("Phase E + Structural Cleanup: BODY FULLY TRANSLATED — 15 paras P001-P015 (pp505-524) + 46 back-matter paras P016-P061 (Bibliography/Index pp526-574) preserved verbatim for alignment = 61 paras src=vi. 5 footnotes sequential 1..5. Duplicate paragraph P010 removed. Bibliography headers translated: 'Bibliography'→'Tài Liệu Tham Khảo', 'Part One: Antisemitism'→'Phần Một: Chủ Nghĩa Bài Do Thái', etc. Latin 'Initium ut esset homo creatus est', 'consensus iuris' translated. DOCX built 5/5 footnotes. Master DOCX 892/892 continuous footnotes. QA PASS 11/11.")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated ch13 notes")