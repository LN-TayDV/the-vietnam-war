import re
import unicodedata

path = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v2\ch12\v1_ch12_vi.txt'
raw = open(path, encoding='utf-8').read()
raw = raw.replace('\r\n', '\n')
body, sep, fn = raw.partition('=== FOOTNOTES ===')

# Fix P001: Add ¹ after 'hình thức chính quyền tuyệt đối'
body = body.replace(
    'hình thức chính quyền tuyệt đối, và mặt khác',
    'hình thức chính quyền tuyệt đối¹, và mặt khác'
)

# Fix P002: Add ⁵ after 'giai đoạn kế tiếp của cách mạng.'
body = body.replace(
    'giai đoạn kế tiếp của cách mạng."',
    'giai đoạn kế tiếp của cách mạng."⁵'
)

new_text = body + sep + fn
new_text = unicodedata.normalize('NFC', new_text)

if new_text != raw:
    open(path, 'w', encoding='utf-8', newline='\n').write(new_text)
    print('FIXED: Added missing inline markers 1 and 5')
else:
    print('No changes')

# Verify
raw2 = open(path, encoding='utf-8').read()
body2, sep2, fn2 = raw2.partition('=== FOOTNOTES ===')
SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹'
markers = re.findall(r'[' + SUP + ']+', body2)
marker_nums = sorted(set(int(''.join(str(SUP.index(c)) for c in m)) for m in markers))
print('Body markers now:', marker_nums[:20], '...')
print('Has 1:', 1 in marker_nums)
print('Has 5:', 5 in marker_nums)