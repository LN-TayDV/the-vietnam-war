# -*- coding: utf-8 -*-
"""List ALL bare-number candidates in the vi body per paragraph (no sequential filter),
so we can see which footnote markers exist and which are missing."""
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BLOCK = re.compile(r"--- \[(V1C09-P\d+)\] \([^)]*\)(?: — [^-]+)? ---")
MARKER = re.compile(r"(?<=[^\s\d])(\d{1,3})(?=\s|$)")
HEADING_P = {"V1C09-P001", "V1C09-P005", "V1C09-P013",
             "V1C09-P023", "V1C09-P028", "V1C09-P036"}


def parse_blocks(path):
    raw = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    lines = raw.split("\n")
    blocks = []
    cur = None
    for ln in lines:
        m = BLOCK.search(ln)
        if m:
            if cur:
                blocks.append(cur)
            cur = [m.group(1), []]
        elif cur is not None:
            if ln.strip().startswith("--- [Cước chú"):
                blocks.append(cur)
                cur = None
            else:
                cur[1].append(ln)
    if cur:
        blocks.append(cur)
    return blocks


def body_text(content, pnum):
    lines = [l.strip() for l in content if l.strip()]
    if pnum in HEADING_P and lines:
        lines = lines[1:]
    return " ".join(lines)


vi = Path(sys.argv[1])
blocks = parse_blocks(vi)
allnums = []
for p, content in blocks:
    text = body_text(content, p)
    cands = [(int(m.group(1)), text[max(0, m.start()-22):m.end()+3]) for m in MARKER.finditer(text)]
    if cands:
        print(f"{p}:")
        for n, ctx in cands:
            print(f"    {n:>3}  ...{ctx}...")
            allnums.append(n)

print(f"\nAll candidate numbers found: {sorted(set(allnums))}")
# Footnote numbers are 1..51; flag which are NOT present as any bare candidate
missing = [n for n in range(1, 52) if n not in allnums]
print(f"Footnote numbers 1..51 NOT appearing as bare candidate: {missing}")