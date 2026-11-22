# -*- coding: utf-8 -*-
"""Inspect parsed chapter structure. Usage: python translation-project/99_scripts/dump_parse.py NN"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_chapter_docx as bd

chap = sys.argv[1] if len(sys.argv) > 1 else "09"
src = bd.SRC_DIR / f"ch{chap}" / f"v1_ch{chap}_vi.txt"
ch = bd.parse_chapter(src)
print("id:", ch["id"])
print("title:", ch["title"])
print("author:", ch["author"])
print("notes:", len(ch["notes"]), "range", min(ch["notes"]), "-", max(ch["notes"]))
print("items:", len(ch["items"]))
for i, it in enumerate(ch["items"]):
    t = it["text"][:55]
    print(f'  [{i}] kind={it["kind"]} text={t!r}')