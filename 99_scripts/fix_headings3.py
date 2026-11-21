#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sua 5 heading tieng Anh thanh tieng Viet VNCH.
Tim dong header chua 'Pxxx]' va 'muc', dong tiep theo la heading tieng Anh.
UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

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
i = 0
while i < len(lines):
    ln = lines[i]
    # Kiem tra dong header: chua 'P005]' hoac 'P017]' ... va chua 'muc'
    is_header = False
    pid_found = None
    for pid in replacements:
        if f"[{pid}]" in ln and "mục" in ln:
            is_header = True
            pid_found = pid
            break
    if is_header:
        new_lines.append(ln)
        i += 1
        # Dong tiep theo la heading tieng Anh
        if i < len(lines):
            new_lines.append(replacements[pid_found])
            fixed += 1
            i += 1
            continue
    new_lines.append(ln)
    i += 1

new_raw = "\n".join(new_lines)
new_raw = unicodedata.normalize("NFC", new_raw)
VI.write_text(new_raw, encoding="utf-8", newline="\n")
print(f"Da sua {fixed} heading thanh tieng Viet VNCH vao {VI.name}")
