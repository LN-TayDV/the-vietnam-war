#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventory all _p1.txt, _p2.txt part files in 04_translation/v1/ for footnote provenance.
Output: audit/part_files_inventory.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V1_DIR = ROOT / "04_translation" / "v1"
AUDIT_DIR = ROOT / "audit"

def inventory_part_files():
    results = {}
    
    for chapter_dir in sorted(V1_DIR.iterdir()):
        if chapter_dir.is_dir() and chapter_dir.name.startswith("ch"):
            part_files = list(chapter_dir.glob("*.txt"))
            chapter_data = {}
            
            for pf in part_files:
                try:
                    text = pf.read_text(encoding="utf-8")
                    lines = text.split("\n")
                    chapter_data[pf.name] = {
                        "size_bytes": pf.stat().st_size,
                        "line_count": len(lines),
                        "first_200_chars": text[:200],
                        "has_footnotes": "footnote" in text.lower() or "cước chú" in text.lower(),
                    }
                except Exception as e:
                    chapter_data[pf.name] = {"error": str(e)}
            
            results[chapter_dir.name] = chapter_data
    
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIT_DIR / "part_files_inventory.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved to {out_path}")
    return results

def main():
    results = inventory_part_files()
    for chapter, files in results.items():
        print(f"{chapter}: {len(files)} part files")
        for fname, info in files.items():
            if "error" not in info:
                print(f"  {fname}: {info['line_count']} lines, {info['size_bytes']} bytes, footnotes: {info['has_footnotes']}")
            else:
                print(f"  {fname}: ERROR - {info['error']}")

if __name__ == "__main__":
    main()