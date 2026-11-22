with open('translation-project/04_translation/v1/ch10/v1_ch10_vi.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    with open('title_check.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(lines[:15]):
            out.write(f"{i}: {line.rstrip()}\n")