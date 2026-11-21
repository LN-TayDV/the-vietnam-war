# -*- coding: utf-8 -*-
"""Verify footnote TEXT in the DOCX matches the source notes for a few key ids."""
import re
import sys
import io
import zipfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

docx = Path(sys.argv[1])
with zipfile.ZipFile(docx) as z:
    xml = z.read("word/footnotes.xml").decode("utf-8")

# extract footnote id -> text
fns = re.findall(r'<w:footnote w:id="(\d+)"[^>]*>(.*?)</w:footnote>', xml, re.S)
texts = {}
for fid, body in fns:
    if int(fid) <= 0:
        continue
    txt = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', body, re.S))
    txt = txt.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    texts[int(fid)] = txt.strip()

print(f"Total footnotes: {len(texts)} (ids {min(texts)}..{max(texts)})")
# check contiguity
ids = sorted(texts)
gaps = [i for i in range(1, 52) if i not in texts]
print(f"Missing ids: {gaps}")
for n in (1, 20, 28, 47, 48, 51):
    print(f"\nFN #{n}: {texts.get(n, '<MISSING>')[:140]}")