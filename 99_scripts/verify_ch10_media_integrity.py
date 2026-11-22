#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrity: DOCX embedded media bytes == source PNG bytes (ch10)."""
import sys, zipfile, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

docx = sorted(Path("translation-project/09_docx").glob("V1-C10*.docx"))[-1]
z = zipfile.ZipFile(docx)
media = sorted(n for n in z.namelist() if n.startswith("word/media/"))

src_map = {
    "word/media/image1.png": "translation-project/04_translation/v1/images/ch10_p239_img0.png",
    "word/media/image2.png": "translation-project/04_translation/v1/images/ch10_p245_img1.png",
}

def sha(b): return hashlib.sha256(b).hexdigest()[:16]

print("DOCX:", docx.name)
ok = True
for m in media:
    docx_bytes = z.read(m)
    src_path = src_map.get(m)
    if not src_path or not Path(src_path).exists():
        print("  ", m, "-> NO source mapping", sha(docx_bytes))
        ok = False
        continue
    src_bytes = Path(src_path).read_bytes()
    match = sha(docx_bytes) == sha(src_bytes)
    print("  %s == %s : %s (%d bytes, sha %s)" % (
        m, Path(src_path).name, "MATCH" if match else "DIFFER",
        len(docx_bytes), sha(docx_bytes)))
    ok = ok and match

print("\nINTEGRITY:", "PASS (embedded media identical to source renders)" if ok else "FAIL")
sys.exit(0 if ok else 1)