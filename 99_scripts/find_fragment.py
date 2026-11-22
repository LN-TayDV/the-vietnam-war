with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the problematic area
idx = text.find('Bản đồ 10.1)')
with open('fragment_check.txt', 'w', encoding='utf-8') as f:
    f.write(text[max(0,idx-50):idx+150])