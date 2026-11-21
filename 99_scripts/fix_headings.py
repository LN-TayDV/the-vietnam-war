#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sua 5 heading (de muc) tieng Anh thanh tieng Viet theo van phong VNCH.
Giu nguyen marker va trang. UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

# Map: (Pxxx, old_heading) -> new_heading VNCH
replacements = {
    "V1C01-P005": "Từ Sử Truyền Thống Đến Sử Hiện Đại",
    "V1C01-P017": "Sử Học Thập Niên 1940",
    "V1C01-P023": "Sử Học Ở Nam Việt Nam",
    "V1C01-P028": "Sử Học Ở Bắc Việt Nam",
    "V1C01-P039": "Sử Lịch Sử Việt Nam Bằng Tiếng Anh",
}

raw = VI.read_text(encoding="utf-8").replace("\r\n", "\n")
raw = unicodedata.normalize("NFC", raw)
lines = raw.split("\n")

new_lines = []
fixed = 0
for ln in lines:
    m = None
    for pid, new_head in replacements.items():
        # Match: --- [PID] (trang X) — đề mục ---
        if ln.startswith(f"--- [{pid}]") and "— đề mục —" in ln:
            m = (pid, new_head)
            break
    if m:
        pid, new_head = m
        # Tao lai dong header voi heading moi
        # Lay trang tu dong cu
        import re as _re
        tm = _re.search(r"\(trang ([^)]+)\)", ln)
        page = tm.group(1) if tm else "?"
        new_lines.append(f"--- [{pid}] (trang {page}) — đề mục ---")
        new_lines.append(new_head)
        fixed += 1
    else:
        new_lines.append(ln)

new_raw = "\n".join(new_lines)
new_raw = unicodedata.normalize("NFC", new_raw)
VI.write_text(new_raw, encoding="utf-8", newline="\n")
print(f"Da sua {fixed} heading thanh tieng Viet VNCH vao {VI.name}")
