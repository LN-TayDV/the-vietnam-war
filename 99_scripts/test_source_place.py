# -*- coding: utf-8 -*-
"""Test whether source_placements can place all footnotes for a chapter."""
import sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "translation-project" / "99_scripts"))
import build_chapter_docx as B

vi_path = Path(sys.argv[1])
ch = B.parse_chapter(vi_path)
notes = ch["notes"]
items = ch["items"]

# Test source page parsing
pages = B.parse_source_pages(ch["id"],
                             min(p["page"] for p in items if p["kind"] in ("para", "quote")),
                             max(p["page"] for p in items if p["kind"] in ("para", "quote")),
                             ch["title"], ch["author"])
if not pages:
    print("parse_source_pages -> None")
    sys.exit()
print(f"Parsed source pages: {len(pages)} pages, pages={[p['page'] for p in pages]}")
for p in pages:
    print(f"  page {p['page']}: {len(p['text'])} chars, notes={sorted(p['notes'].keys())}")

mark_list = B.source_page_markers(pages, max(notes)) if pages else None
if not mark_list:
    print(f"source_page_markers -> None (could not find {max(notes)} sequential markers)")
    # diagnose: count raw sequential markers
    expect, cnt = 1, 0
    for p in pages:
        import re
        for m in re.finditer(r"(?<=[^\s\d])(\d{1,3})(?=\s|$)", p["text"]):
            if int(m.group(1)) == expect:
                cnt += 1; expect += 1
    print(f"  raw sequential markers found: {cnt}")
else:
    print(f"source_page_markers -> {len(mark_list)} markers")

marks = B.source_placements(items, ch, notes)
if marks:
    total = sum(len(v) for v in marks.values())
    print(f"source_placements -> {total} placements across {len(marks)} paragraphs")
    # check for collisions/overlaps
    for idx, lst in sorted(marks.items()):
        offs = [o for o, n in lst]
        if len(offs) != len(set(offs)):
            print(f"  OVERLAP in item#{idx}: {lst}")
else:
    print("source_placements -> None")