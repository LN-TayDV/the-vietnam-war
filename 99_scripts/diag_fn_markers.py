# -*- coding: utf-8 -*-
"""Diagnose footnote marker placement for a chapter (uses build script logic)."""
import sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "translation-project" / "99_scripts"))
import build_chapter_docx as B

vi_path = Path(sys.argv[1])
ch = B.parse_chapter(vi_path)
items = ch["items"]
notes = ch["notes"]

# Replicate extract_inline_markers but verbose
expect = 1
found = []
for idx, it in enumerate(items):
    if it["kind"] not in ("para", "quote"):
        continue
    text = it["text"]
    masked = B.ND_SPAN.sub(lambda m: " " * len(m.group(0)), text)
    for m in B.MARKER.finditer(masked):
        num = int(m.group(1) or m.group(2))
        is_inline = m.group(1) is not None
        if is_inline:
            if num < expect:
                continue
        else:
            if num != expect:
                continue
        found.append((idx, num, "inline" if is_inline else "bare", text[max(0,m.start()-20):m.end()+5]))
        expect = num + 1

print(f"Total notes defined: {len(notes)} (keys: {min(notes)}..{max(notes)})")
print(f"Markers FOUND inline (sequential from 1): {len(found)}")
for idx, num, kind, ctx in found:
    print(f"  item#{idx} note#{num} [{kind}] ...{ctx}...")
missing = [n for n in sorted(notes) if n not in {f[1] for f in found}]
print(f"MARKERS NOT placed inline ({len(missing)}): {missing}")