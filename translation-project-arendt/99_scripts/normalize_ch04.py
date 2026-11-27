# -*- coding: utf-8 -*-
"""
normalize_ch04.py — Đảm bảo UTF-8/NFC/LF cho ch04_structure.json và ch04_src.txt
"""

import json
import os
import unicodedata

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
V2 = os.path.join(BASE, "02_extracted_text", "v2")

def normalize_obj(obj):
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, dict):
        return {k: normalize_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize_obj(v) for v in obj]
    return obj

# Fix structure JSON
struct_path = os.path.join(V2, "ch04_structure.json")
with open(struct_path, encoding="utf-8") as f:
    struct = json.load(f)
struct_norm = normalize_obj(struct)
with open(struct_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(struct_norm, f, ensure_ascii=False, indent=2)
print(f"Normalized: {struct_path}")

# Fix src TXT
src_path = os.path.join(V2, "ch04_src.txt")
with open(src_path, encoding="utf-8") as f:
    content = f.read()
content_norm = unicodedata.normalize("NFC", content)
with open(src_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content_norm)
print(f"Normalized: {src_path}")

print("Done!")
