# -*- coding: utf-8 -*-
"""Detailed per-paragraph DOCX analysis for a chapter. Reusable regression tool.
Usage: python translation-project/99_scripts/analyze_docx.py NN [path]
"""
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
chap = sys.argv[1] if len(sys.argv) > 1 else "09"
PROJECT = Path(__file__).resolve().parents[1]

if len(sys.argv) > 2:
    path = Path(sys.argv[2])
else:
    path = PROJECT / "09_docx" / "V1-C09_The-French-Indochina-War-in-the-Central-Highlands.docx"

z = zipfile.ZipFile(path)
xml = z.read("word/document.xml").decode("utf-8")
para_elems = re.findall(r'(<w:p[^>]*>.*?</w:p>)', xml, re.DOTALL)
print(f"File: {path.name}")
print(f"Total body paragraphs: {len(para_elems)}\n")

for i, pe in enumerate(para_elems):
    txt = re.sub(r'<[^>]+>', '', pe); txt = re.sub(r'\s+', ' ', txt).strip()
    sz = re.search(r'w:sz w:val="(\d+)"', pe); sz = int(sz.group(1)) if sz else None
    ital = '<w:i/>' in pe or '<w:i ' in pe
    bold = '<w:b/>' in pe or '<w:b ' in pe
    jc = re.search(r'w:jc w:val="(\w+)"', pe); jc = jc.group(1) if jc else None
    ind = re.search(r'w:ind [^>]*w:left="(\d+)"', pe); ind = int(ind.group(1)) if ind else 0
    fi = re.search(r'w:ind [^>]*w:firstLine="(\d+)"', pe); fi = int(fi.group(1)) if fi else 0
    sb = re.search(r'w:before="(\d+)"', pe); sb = int(sb.group(1)) if sb else 0
    sa = re.search(r'w:after="(\d+)"', pe); sa = int(sa.group(1)) if sa else 0
    ls = re.search(r'w:line="(\d+)"', pe); ls = int(ls.group(1)) if ls else 0
    nref = pe.count('w:footnoteReference')
    if sz == 27 and bold:
        kind = 'HEAD'
    elif ital and ind == 720:
        kind = 'QUOTE'
    elif sz == 24 and not ital and not bold and fi != 0:
        kind = 'BODY'
    else:
        kind = 'OTHER'
    print(f"P{i:2d} {kind:5s} sz={sz} ital={ital} bold={bold} jc={jc} ind={ind} fi={fi} sb={sb} sa={sa} ls={ls} fnref={nref} | {txt[:45]}")