# -*- coding: utf-8 -*-
"""Update progress.json V1-C09 entry: docx path, word count, docx_status."""
import json
from pathlib import Path

pp = Path("translation-project/00_plan/progress.json")
data = json.loads(pp.read_text(encoding="utf-8"))

# find V1-C09 entry (top-level or under chapters)
def find_entry(d, key):
    if key in d:
        return d, key
    for container in ("chapters", "progress", "items"):
        if container in d and key in d[container]:
            return d[container], key
    return None, None

entry, key = find_entry(data, "V1-C09")
if entry is None:
    print("V1-C09 not found in progress.json")
    raise SystemExit(1)

entry[key]["docx"] = "09_docx/V1-C09_The-French-Indochina-War-in-the-Central-Highlands.docx"
entry[key]["docx_status"] = (
    "DONE (rebuilt 2026-11-21; 9,512 từ, 51/51 cước chú inline; "
    "audit_docx_format.py PASS; heading 13.5pt bold sb=14 sa=6; "
    "body 12pt Justify fi=0.9cm sa=6 line=1.3; quote 12pt italic li=0.5in; "
    "footnote 9pt tuần tự 1..51; 6 heading, 2 quote, 36 body)"
)
entry[key]["format_audit"] = (
    "PASS (2026-11-21): audit_docx_format.py ch09 — heading/quote/body/"
    "footnote/image/metadata/block-leak tất cả OK"
)
entry[key]["paragraphs"] = 37
entry[key]["footnotes"] = 51

pp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Updated {key}: docx={entry[key]['docx']}")
print(f"  docx_status={entry[key]['docx_status'][:80]}...")