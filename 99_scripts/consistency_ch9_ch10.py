#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consistency check: Ch9 vs Ch10 extraction pipeline."""
import json, re, sys, zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("CH9 vs CH10 CONSISTENCY CHECK")
print("=" * 60)

# 1. Manifest structure
mani = json.loads(Path("translation-project/00_plan/image_manifest.json").read_text(encoding="utf-8"))
c9 = [e for e in mani["images"] if e["chapter"] == 9]
c10 = [e for e in mani["images"] if e["chapter"] == 10]
print("\n[1] Manifest entries: ch9=%d, ch10=%d" % (len(c9), len(c10)))
keys9 = set(c9[0].keys()) if c9 else set()
keys10 = set(c10[0].keys()) if c10 else set()
print("    ch9 keys :", sorted(keys9))
print("    ch10 keys:", sorted(keys10))
print("    same core schema:", {"image_id","source_pdf","volume","chapter","pdf_page","printed_page","filename","image_type","caption","extraction_status"}.issubset(keys9) and {"image_id","source_pdf","volume","chapter","pdf_page","printed_page","filename","image_type","caption","extraction_status"}.issubset(keys10))

# 2. Naming convention
print("\n[2] Filename convention ch<NN>_p<PPP>_img<I>.png:")
for e in c9 + c10:
    print("    %-14s ch%d -> %s" % (e["image_id"], e["chapter"], e["filename"] or "(vector-only)"))

# 3. extraction_status values
print("\n[3] extraction_status:")
for e in c9 + c10:
    print("    %-14s %s [%s]" % (e["image_id"], e["image_type"], e["extraction_status"]))

# 4. Placeholder convention in vi.txt
print("\n[4] Placeholder blocks in vi.txt:")
for ch in ("ch09", "ch10"):
    p = Path("translation-project/04_translation/v1/%s/v1_%s_vi.txt" % (ch, ch))
    txt = p.read_text(encoding="utf-8")
    ph = re.findall(r"---\s*\[(V1C\d+-PIMG\d+)\]\s*\(trang ([^)]+)\)", txt)
    caps = re.findall(r"(?m)^\s*((?:Hình|Bản đồ)\s+\d+\.\d+)", txt)
    print("    %s: PIMG blocks=%s | captions=%s" % (ch, ph, caps))

# 5. DOCX embedded image count
print("\n[5] DOCX embedded images:")
for pat, label in (("V1-C09*.docx", "ch9"), ("V1-C10*.docx", "ch10")):
    fs = sorted(Path("translation-project/09_docx").glob(pat))
    if fs:
        z = zipfile.ZipFile(fs[-1])
        media = [n for n in z.namelist() if n.startswith("word/media/")]
        print("    %s: %d media (%s)" % (label, len(media), [Path(m).name for m in media]))
    else:
        print("    %s: NO DOCX" % label)

print("\n" + "=" * 60)
v9 = [e for e in c9 if e["extraction_status"].startswith("VECTOR_ONLY")]
v10 = [e for e in c10 if e["extraction_status"].startswith("VECTOR_ONLY")]
if not v9 and not v10:
    print("CONSISTENT: both chapters fully rasterized (no VECTOR_ONLY left)")
else:
    print("INCONSISTENT: VECTOR_ONLY remains -> ch9=%d ch10=%d" % (len(v9), len(v10)))
print("=" * 60)