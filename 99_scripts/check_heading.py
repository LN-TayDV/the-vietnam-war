#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import unicodedata

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")
raw = VI.read_text(encoding="utf-8").replace("\r\n", "\n")
raw = unicodedata.normalize("NFC", raw)

out = []
for i, ln in enumerate(raw.split("\n"), 1):
    if "mục" in ln or "de muc" in ln.lower() or "P005]" in ln or "P017]" in ln or "P023]" in ln or "P028]" in ln or "P039]" in ln:
        out.append(f"{i}: {repr(ln)}")

Path("99_scripts/heading_check.txt").write_text("\n".join(out), encoding="utf-8", newline="\n")
print("Da ghi vao 99_scripts/heading_check.txt")
