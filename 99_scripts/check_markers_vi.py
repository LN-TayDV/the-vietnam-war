# -*- coding: utf-8 -*-
import re
from pathlib import Path

root = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war")
vi = (root/"translation-project/04_translation/v1/ch13/v1_ch13_vi.txt").read_text(encoding="utf-8")

idx = vi.find("--- [C\u01b0\u1edbc ch\u00fa")
body = vi[:idx]
notes = vi[idx:]

# parse vi body segments
parts = re.split(r"(--- \[V1C13-P\d+\][^\n]*---)", body)
i = 1
print("=== vi BODY: footnote markers per segment ===")
vi_markers = []
while i < len(parts):
    header = parts[i]
    content = parts[i+1] if i+1 < len(parts) else ""
    num = re.search(r"V1C13-P(\d+)", header).group(1)
    marks = re.findall(r"\[(\d+)\]", content)
    if marks:
        print(f"P{num}: {marks}")
        for m in marks:
            vi_markers.append(int(m))
    i += 2

# notes block markers
note_marks = [int(x) for x in re.findall(r"\[(\d+)\]", notes)]
print("\n=== NOTES block: note numbers present ===")
print(sorted(note_marks))
print("count notes:", len(note_marks))

print("\n=== vi body markers (in order) ===")
print(vi_markers)
print("count body markers:", len(vi_markers))
print("unique body markers:", sorted(set(vi_markers)))
missing = [n for n in range(1,62) if n not in set(vi_markers)]
print("MISSING in body:", missing)
from collections import Counter
dup = [k for k,v in Counter(vi_markers).items() if v>1]
print("DUPLICATE in body:", dup)