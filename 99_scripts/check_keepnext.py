# -*- coding: utf-8 -*-
"""Verify keep_with_next on image paragraphs in a DOCX."""
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
path = Path(sys.argv[1])
z = zipfile.ZipFile(path)
xml = z.read("word/document.xml").decode("utf-8")
paras = re.findall(r'(<w:p\b[^>]*>.*?</w:p>)', xml, re.DOTALL)
imgs = [p for p in paras if "r:embed" in p]
print(f"File: {path.name}")
print(f"Image paragraphs: {len(imgs)}")
for i, p in enumerate(imgs):
    keep = "w:keepNext" in p
    sz_m = re.search(r'w:sz w:val="(\d+)"', p)
    sz = sz_m.group(1) if sz_m else None
    print(f"  img{i}: keep_with_next={keep} sz={sz}")
    if not keep:
        print("    FAIL: image paragraph missing keep_with_next")