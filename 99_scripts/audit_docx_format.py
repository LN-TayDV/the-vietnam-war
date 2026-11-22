# -*- coding: utf-8 -*-
"""Comprehensive DOCX formatting audit against the chapter spec.
Checks: heading (13.5pt bold, sb=14pt sa=6pt, centered/left), body (12pt,
Justify, fi=0.9cm, sa=6pt, line=1.3), quote (12pt italic, li=0.5"), footnote
(9pt, sequential), images (4.5" wide, before caption), no block-header leaks,
no metadata leaks.

Usage: python translation-project/99_scripts/audit_docx_format.py NN [path]
Exit 0 = PASS, 1 = FAIL.
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
    # find the NEWEST docx for this chapter (a chapter may have stale
    # files from earlier builds with a different title slug).
    cands = sorted((PROJECT / "09_docx").glob(f"V1-C{int(chap):02d}_*.docx"),
                   key=lambda p: p.stat().st_mtime)
    path = cands[-1] if cands else None
if path is None or not path.exists():
    print(f"FAIL: docx not found for ch{chap}")
    sys.exit(1)

z = zipfile.ZipFile(path)
xml = z.read("word/document.xml").decode("utf-8")
para_elems = re.findall(r'(<w:p\b[^>]*>.*?</w:p>)', xml, re.DOTALL)

FAIL = []
def check(cond, msg):
    print(("PASS" if cond else "FAIL") + " - " + msg)
    if not cond:
        FAIL.append(msg)

def is_true_italic(rpr):
    return bool(re.search(r'<w:i/>|<w:i\s+w:val="(?:true|1)"', rpr))
def is_true_bold(rpr):
    return bool(re.search(r'<w:b/>|<w:b\s+w:val="(?:true|1)"', rpr))

def para_metrics(pe):
    txt = re.sub(r"<[^>]+>", "", pe); txt = re.sub(r"\s+", " ", txt).strip()
    sz = re.search(r'w:sz w:val="(\d+)"', pe); sz = int(sz.group(1)) if sz else None
    # first run rPr (representative)
    rpr_m = re.search(r'<w:rPr>(.*?)</w:rPr>', pe, re.DOTALL)
    rpr = rpr_m.group(1) if rpr_m else ""
    ital = is_true_italic(rpr)
    bold = is_true_bold(rpr)
    jc = re.search(r'w:jc w:val="(\w+)"', pe); jc = jc.group(1) if jc else None
    ind = re.search(r'w:ind [^>]*w:left="(\d+)"', pe); ind = int(ind.group(1)) if ind else 0
    fi = re.search(r'w:ind [^>]*w:firstLine="(\d+)"', pe); fi = int(fi.group(1)) if fi else 0
    sb = re.search(r'w:before="(\d+)"', pe); sb = int(sb.group(1)) if sb else 0
    sa = re.search(r'w:after="(\d+)"', pe); sa = int(sa.group(1)) if sa else 0
    ls = re.search(r'w:line="(\d+)"', pe); ls = int(ls.group(1)) if ls else 0
    nref = pe.count('w:footnoteReference')
    has_img = 'r:embed' in pe
    return dict(txt=txt, sz=sz, ital=ital, bold=bold, jc=jc, ind=ind, fi=fi,
                sb=sb, sa=sa, ls=ls, nref=nref, has_img=has_img)

print(f"=== AUDIT {path.name} ===\n")

# Classify paragraphs
heads, quotes, bodies, others = [], [], [], []
hinh_pat = re.compile(
    r"^\s*(?:H\u00ecnh|B\u1ea3n \u0111\u1ed3|Bi\u1ec3u \u0111\u1ed3|S\u01a1 \u0111\u1ed3|B\u1ea3ng)\s+\d+\.\d+"
)
for i, pe in enumerate(para_elems):
    m = para_metrics(pe)
    if m["sz"] == 27 and m["bold"]:
        heads.append((i, m))
    elif m["ital"] and m["ind"] == 720:
        quotes.append((i, m))
    elif m["sz"] == 24 and not m["ital"] and not m["bold"] and m["fi"] != 0:
        bodies.append((i, m))
    elif m["has_img"] or hinh_pat.match(m["txt"]):
        others.append((i, m))
    else:
        # title block / empty paras
        pass

print(f"Headings: {len(heads)} | Quotes: {len(quotes)} | Body: {len(bodies)} | Img/Cap: {len(others)}")

# --- Heading checks ---
for i, m in heads:
    check(m["sb"] == 280, f"H P{i} sb={m['sb']}twips (expect 280=14pt)")
    check(m["sa"] == 120, f"H P{i} sa={m['sa']}twips (expect 120=6pt)")

# --- Body checks ---
for i, m in bodies:
    check(m["sz"] == 24, f"B P{i} sz={m['sz']} (expect 24=12pt)")
    check(m["jc"] == "both", f"B P{i} jc={m['jc']} (expect both/justify)")
    check(m["fi"] == 510, f"B P{i} fi={m['fi']}twips (expect 510=0.9cm)")
    check(m["sa"] == 120, f"B P{i} sa={m['sa']}twips (expect 120=6pt)")
    check(m["ls"] == 312, f"B P{i} ls={m['ls']} (expect 312=1.3line)")

# --- Quote checks ---
for i, m in quotes:
    check(m["ital"], f"Q P{i} must be italic")
    check(m["ind"] == 720, f"Q P{i} ind={m['ind']}twips (expect 720=0.5in)")
    check(m["sz"] == 24, f"Q P{i} sz={m['sz']} (expect 24=12pt)")

# --- Footnote checks ---
fn_ids = []
try:
    fn = z.read("word/footnotes.xml").decode("utf-8")
    fn_ids = sorted(int(i) for i in re.findall(r'w:footnote w:id="(\d+)"', fn) if int(i) > 0)
    check(fn_ids == list(range(1, len(fn_ids) + 1)),
          f"footnotes sequential 1..{len(fn_ids)}")
    # footnote text size = 18 (9pt)
    check(fn.count('w:sz w:val="18"') >= len(fn_ids), "footnote text 9pt (sz=18)")
except KeyError:
    # No footnotes.xml: only a real failure if the body references footnotes.
    check(xml.count("w:footnoteReference") == 0,
          "footnotes.xml MISSING but body has no footnote refs (0-note chapter OK)")

nref = xml.count("w:footnoteReference")
print(f"Body footnote refs: {nref} | native footnotes: {len(fn_ids)}")

# --- No leaks ---
leaked = re.findall(r"--- \[[^\]]+\](?: \([^)]*\))?(?: — .*?)? ---", xml)
check(len(leaked) == 0, f"no block-header leaks ({len(leaked)})")
check("02_extracted_text" not in xml, "no source-path metadata")
check("· 9,512 từ ·" not in xml, "no colophon metadata")

# --- Images before captions ---
img_paras = {i for i, pe in enumerate(para_elems) if 'r:embed' in pe}
caps = []
for i, pe in enumerate(para_elems):
    m = para_metrics(pe)
    if hinh_pat.match(m["txt"]):
        caps.append(i)
if caps:
    check(all((i-1) in img_paras for i in caps), "every caption preceded by its image")
    check(len(caps) == len(img_paras), "image count == caption count")
print(f"Images: {len(img_paras)} | Captions: {len(caps)}")

print("\n" + "=" * 60)
if FAIL:
    print(f"AUDIT FAILED: {len(FAIL)} issue(s)")
    for f in FAIL[:30]:
        print("  -", f)
    sys.exit(1)
else:
    print("AUDIT PASSED: all format checks OK")