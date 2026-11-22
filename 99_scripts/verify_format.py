with open('translation-project/04_translation/v1/ch11/v1_ch11_vi.txt', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Check heading format
headings = re.findall(r'--- \[V1C11-P\d+\] \(trang [\d\-]+\) — đề mục ---', content)
with open('verify_results.txt', 'w', encoding='utf-8') as out:
    out.write('Headings (— đề mục): ' + str(len(headings)) + '\n')
    for h in headings:
        out.write('  ' + h[:80] + '\n')

    # Check image markers
    images = re.findall(r'--- \[PIMG\d+\] \(trang \d+\) ---', content)
    out.write('Image markers: ' + str(len(images)) + '\n')
    for i in images:
        out.write('  ' + i + '\n')

    # Check footnote block
    fn = content.count('--- [Cước chú trang')
    out.write('Footnote blocks: ' + str(fn) + '\n')

    # Check for metadata leaks
    leaks = ['Source:', '02_extracted_text', 'V1C11-']
    for leak in leaks:
        count = content.count(leak)
        if count > 0 and leak != 'V1C11-':
            out.write('POTENTIAL LEAK: ' + leak + ' count: ' + str(count) + '\n')

    out.write('Verification complete\n')