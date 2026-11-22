#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify ch10 DOCX: embedded images + caption pairing (independent of footnotes)."""
import sys, zipfile, re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
sys.stdout.reconfigure(encoding="utf-8")

docx = sorted(Path("translation-project/09_docx").glob("V1-C10*.docx"))[-1]
print("DOCX:", docx.name)

# 1. media files embedded
z = zipfile.ZipFile(docx)
media = [n for n in z.namelist() if n.startswith("word/media/")]
print("Embedded media files:", media)
for m in media:
    print("  ", m, z.getinfo(m).file_size, "bytes")

# 2. walk paragraphs: image runs + caption paragraphs
doc = Document(str(docx))
cap_re = re.compile(r"^\s*(?:Hình|Bản đồ|Biểu đồ|Sơ đồ|Bảng)\s+\d+\.\d+")
paras = doc.paragraphs
img_para_idx = []
cap_para_idx = []
for i, p in enumerate(paras):
    has_img = bool(p._p.findall(".//" + qn("w:drawing")))
    if has_img:
        img_para_idx.append(i)
    if cap_re.match(p.text):
        cap_para_idx.append(i)

print("\nImage paragraphs (idx):", img_para_idx)
print("Caption paragraphs (idx):", cap_para_idx)
for i in cap_para_idx:
    print("  caption[%d]: %s" % (i, paras[i].text[:90]))
for i in img_para_idx:
    prev_cap = (i - 1) in cap_para_idx
    print("  image[%d] preceded by caption? %s" % (i, (i-1) in cap_para_idx))

# 3. checks
print("\n--- CHECKS ---")
n_img = len(img_para_idx)
n_cap = len(cap_para_idx)
print("image count == caption count:", n_img == n_cap, "(%d vs %d)" % (n_img, n_cap))
each_cap_after_img = all((i-1) in img_para_idx for i in cap_para_idx)
print("every caption preceded by image:", each_cap_after_img)
# order: Hình 10.1 caption should map to ch10_p239 (photo), Bản đồ 10.1 to ch10_p245 (map)
print("captions in order:", [paras[i].text[:12] for i in cap_para_idx])

ok = (n_img == 2 and n_cap == 2 and each_cap_after_img and len(media) >= 2)
print("\nRESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)