# -*- coding: utf-8 -*-
"""Check whether the bare markers skipped by the guard were real footnotes.
Compares old behavior (no guard) vs new (with guard) for a chapter."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "translation-project" / "99_scripts"))
import build_chapter_docx as bd

chap = sys.argv[1] if len(sys.argv) > 1 else "09"
ch = bd.parse_chapter(bd.SRC_DIR / f"ch{chap}" / f"v1_ch{chap}_vi.txt")

# OLD behavior: no warn, no year/page guard
old_items, old_marks, old_mode = bd.plan_footnotes(ch)[:3], None, None
# re-run with the guard disabled by monkeypatching
import re
# Temporarily test: what numbers exist as bare markers and their context
items = ch["items"]
notes = ch["notes"]
MARKER = bd.MARKER
ND_SPAN = bd.ND_SPAN
print(f"Chapter {chap}: {len(notes)} notes, {len(items)} items")
print("\n--- All bare (non-[N]) number markers found in body ---")
for idx, it in enumerate(items):
    if it["kind"] not in ("para", "quote"):
        continue
    text = it["text"]
    masked = ND_SPAN.sub(lambda m: " " * len(m.group(0)), text)
    for m in MARKER.finditer(masked):
        if m.group(1) is not None:
            continue  # [N] inline, skip
        num = int(m.group(2))
        ctx = text[max(0, m.start() - 30):m.start()] + "<<" + m.group(2) + ">>" + text[m.end():m.end() + 10]
        print(f"  [P{idx}] num={num} ctx=...{ctx!r}")