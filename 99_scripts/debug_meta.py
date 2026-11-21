# -*- coding: utf-8 -*-
"""Debug: show meta and first items for a chapter."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "translation-project" / "99_scripts"))
import build_chapter_docx as bd

chap = sys.argv[1] if len(sys.argv) > 1 else "03"
ch = bd.parse_chapter(bd.SRC_DIR / f"ch{chap}" / f"v1_ch{chap}_vi.txt")
print("=== META ===")
for m in ch["meta"]:
    print(f"  {m!r}")
print("\n=== FIRST 5 ITEMS ===")
for i, it in enumerate(ch["items"][:5]):
    print(f"  [{i}] kind={it['kind']} text={it['text'][:70]!r}")