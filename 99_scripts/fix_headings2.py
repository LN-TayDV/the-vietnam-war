#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sua 5 heading (de muc) tieng Anh thanh tieng Viet theo van phong VNCH.
Pattern: dong header chua 'de muc', dong tiep theo la heading tieng Anh.
Giu nguyen marker va trang. UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata
import re

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

# Map: PID -> heading VNCH moi
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
    # Kiem tra dong header co chua 'de muc' va mot PID
    m = re.search(r"--- \[(V1C01-P\d+)\] \(trang ([^)]+)\)[^—]*—[^—]*—", ln)
    if m:
        pid = m.group(1)
        page = m.group(2)
        if pid in replacements:
            # Giu dong header nguyen van (bao ca dau gach ngang)
            new_lines.append(ln)
            i += 1
            # Dong tiep theo la heading tieng Anh -> thay bang tieng Viet
            if i < len(lines):
                old_head = lines[i].strip()
                new_head = replacements[pid]
                new_lines.append(new_head)
                fixed += 1
                i += 1
                continue
    new_lines.append(ln)
    i += 1

new_raw = "\n".join(new_lines)
new_raw = unicodedata.normalize("NFC", new_raw)
VI.write_text(new_raw, encoding="utf-8", newline="\n")
print(f"Da sua {fixed} heading thanh tieng Viet VNCH vao {VI.name}")
