with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Check P009 ends with [3]
idx_p009 = text.find('--- [V1C10-P009]')
idx_pimg1 = text.find('--- [PIMG1]')
p009_content = text[idx_p009:idx_pimg1]

# Check P010 starts without [3]
idx_p010 = text.find('--- [V1C10-P010]')
idx_p011 = text.find('--- [V1C10-P011]')
p010_content = text[idx_p010:idx_p011]

with open('footnote_check.txt', 'w', encoding='utf-8') as f:
    f.write('P009 end:\n')
    f.write(repr(p009_content[-150:]))
    f.write('\n\nP010 start:\n')
    f.write(repr(p010_content[:200]))