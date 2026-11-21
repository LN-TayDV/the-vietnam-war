# -*- coding: utf-8 -*-
"""Check run-level italic flags in body paragraphs of a DOCX (accurate)."""
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("translation-project/09_docx/V1-C09_The-French-Indochina-War-in-the-Central-Highlands.docx")
z = zipfile.ZipFile(path)
xml = z.read("word/document.xml").decode("utf-8")

paras = re.findall(r'(<w:p\b[^>]*>.*?</w:p>)', xml, re.DOTALL)
body = [p for p in paras if 'w:firstLine="510"' in p]
print(f"Body paragraphs: {len(body)}")
print("\n--- First body paragraph, run-level rPr (accurate) ---")
pe = body[0]
runs = re.findall(r'(<w:r\b[^>]*>.*?</w:r>)', pe, re.DOTALL)
for ri, run in enumerate(runs):
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', run, re.DOTALL)
    t = re.search(r'<w:t[^>]*>(.*?)</w:t>', run, re.DOTALL)
    txt = t.group(1)[:40] if t else ''
    rpr_str = rpr.group(0) if rpr else '(none)'
    # TRUE italic: <w:i/> or <w:i w:val="true"/> or <w:i w:val="1"/>
    # NOT italic: <w:i w:val="0"/> or <w:i w:val="false"/> or absent
    true_italic = bool(re.search(r'<w:i/>|<w:i\s+w:val="(?:true|1)"', rpr_str))
    false_italic = bool(re.search(r'<w:i\s+w:val="(?:false|0)"', rpr_str))
    print(f"  run{ri}: TRUE_italic={true_italic} FALSE_flag={false_italic} | txt='{txt}'")
    print(f"        rPr={rpr_str}")