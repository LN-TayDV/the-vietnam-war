# -*- coding: utf-8 -*-
"""Deep inspection of a built DOCX: heading/quote/body/footnote/image layout.
Reusable regression harness.  Usage:
    python translation-project/99_scripts/inspect_docx_ch09.py [NN]
"""
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "translation-project" / "99_scripts"))
import build_chapter_docx as bd

PROJECT = Path(__file__).resolve().parents[1] / "translation-project"
chap = sys.argv[1] if len(sys.argv) > 1 else "09"

src = bd.SRC_DIR / f"ch{chap}" / f"v1_ch{chap}_vi.txt"
ch = bd.parse_chapter(src)
out, words, used, mode, total = bd.build(src)
z = zipfile.ZipFile(out)
xml = z.read("word/document.xml").decode("utf-8")

para_elems = re.findall(r'(<w:p[^>]*>.*?</w:p>)', xml, re.DOTALL)
print(f"=== {ch['id']}  ({out.name}) ===")
print(f"Words: {words:,} | notes src={total} docx_used={used} mode={mode}")
print(f"Total paragraphs in docx body: {len(para_elems)}\n")

# Style detection per paragraph
def para_info(pe):
    txt = re.sub(r"<[^>]+>", "", pe)
    txt = re.sub(r"\s+", " ", txt).strip()
    has_img = "r:embed" in pe
    sz = re.search(r'w:sz w:val="(\d+)"', pe)
    sz = int(sz.group(1)) if sz else None
    ital = "<w:i/>" in pe or "<w:i " in pe
    bold = "<w:b/>" in pe or "<w:b " in pe
    jc = re.search(r'w:jc w:val="(\w+)"', pe)
    jc = jc.group(1) if jc else None
    ind = re.search(r'w:ind [^>]*w:left="(\d+)"', pe)
    ind = int(ind.group(1)) if ind else 0
    sb = re.search(r'w:spacing [^>]*w:before="(\d+)"', pe)
    sb = int(sb.group(1)) if sb else None
    return txt, has_img, sz, ital, bold, jc, ind, sb

heading_count = 0
quote_count = 0
body_count = 0
image_count = 0
cap_count = 0
hinh_pat = re.compile(r"^\s*H\u00ecnh\s+\d+\.\d+")
issues = []

for i, pe in enumerate(para_elems):
    txt, has_img, sz, ital, bold, jc, ind, sb = para_info(pe)
    if has_img:
        image_count += 1
    if hinh_pat.match(txt):
        cap_count += 1
    # heading: sz 27 (13.5pt) bold
    if sz == 27 and bold:
        heading_count += 1
        if sb != 14:
            issues.append(f"[P{i}] HEADING sb={sb} (expect 14): {txt[:50]}")
    # quote: italic with left indent 720 twips (0.5 inch) or 0.5"=720
    if ital and ind == 720:
        quote_count += 1
    if txt and not has_img and sz == 24 and not ital and not bold:
        body_count += 1

print(f"Headings (13.5pt bold, sb=14): {heading_count}")
print(f"Quotes (italic, left-indent 720twips): {quote_count}")
print(f"Body paragraphs (12pt): {body_count}")
print(f"Images (r:embed): {image_count}")
print(f"Captions (Hinh X.Y): {cap_count}")

# footnote refs in body
nref = xml.count("w:footnoteReference")
print(f"Body footnote refs: {nref}")

# footnotes
try:
    fn = z.read("word/footnotes.xml").decode("utf-8")
    fn_ids = [int(i) for i in re.findall(r'w:footnote w:id="(\d+)"', fn) if int(i) > 0]
    print(f"Native footnotes: {len(fn_ids)}  ids range {min(fn_ids)}..{max(fn_ids)}")
    if fn_ids != list(range(1, len(fn_ids) + 1)):
        issues.append(f"footnote ids not sequential: {fn_ids}")
except KeyError:
    issues.append("footnotes.xml MISSING")

# Check for marker leaks (bare numbers that should have been footnotes)
leaked_markers = re.findall(r"\s(\d{1,2})\s(?=[A-ZÁÀẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ])", xml)
# This regex is too broad; just report count
print(f"\n--- ISSUES ({len(issues)}) ---")
for it in issues:
    print("  ", it)
if not issues:
    print("  (none)")