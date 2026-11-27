import os, re
V2 = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\02_extracted_text\v2"
files = [f for f in os.listdir(V2) if f.endswith("_src.txt")]
total_issues = 0
for f in sorted(files):
    path = os.path.join(V2, f)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    lines = content.split("\n")
    issues = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"\[V1-", line):
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip() == "" or re.match(r"\[V1-", next_line) or next_line.startswith("#"):
                    issues += 1
                    print(f"  {f}: line {i+1} header followed by empty/non-text: \"{next_line[:50]}\"")
            i += 1
        else:
            i += 1
    if issues > 0:
        total_issues += issues
        print(f"{f}: {issues} issues")
    else:
        print(f"{f}: OK - all paragraphs on single line")
print(f"\nTotal issues: {total_issues}")
