with open(r'.kilo\skills\translation-workflow\SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the exact 99_scripts section
idx = content.find('99_scripts/')
if idx >= 0:
    # Print 20 lines after
    lines = content[idx:idx+500].split('\n')
    with open('debug_output.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(lines[:15]):
            out.write(f'{i}: {repr(line)}\n')

print("Done")