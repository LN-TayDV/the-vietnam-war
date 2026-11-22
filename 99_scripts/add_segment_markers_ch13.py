#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tự động phân đoạn ch13.txt thành các đoạn văn bản với markers [V1C13-PYYY] (trang Z).
Heuristics: paragraph mới bắt đầu khi dòng trước là dòng trống, số trang, header,
tác giả, hoặc dòng cuối của footnote block; HOẶC dòng hiện không indentation,
bắt đầu bằng chữ hoa, và dòng trước kết thúc bằng dấu chấm/ngoặc.
"""
from pathlib import Path
import re

SRC = Path("translation-project/02_extracted_text/v1/ch13.txt")
OUT = Path("translation-project/04_translation/v1/ch13/v1_ch13_src.txt")

lines = SRC.read_text(encoding="utf-8").split("\n")

PAGE_RE = re.compile(r"^\s*(\d{1,3})\s*$")
FN_RE = re.compile(r"^\t\d+\t")
CHAPTER_HEADER_RE = re.compile(r"^Eisenhower and Vietnam\s*$")
AUTHOR_RE = re.compile(r"^David L\. Anderson\s*$")

# Bước 1: Lọc bỏ dòng số trang, header chapter, tác giả; gán page
filtered = []  # (line_text, page_or_None, is_boundary)
current_page = None
prev_ended_sentence = False  # dòng trước kết thúc bằng dấu chấm/ngoặc

for line in lines:
    s = line.strip()
    m = PAGE_RE.match(s)
    if m:
        num = int(m.group(1))
        if 282 <= num <= 301:
            current_page = num
            continue  # bỏ dòng số trang, nhưng nó là boundary ngầm
    if CHAPTER_HEADER_RE.match(s) or AUTHOR_RE.match(s):
        continue
    filtered.append((line, current_page))

# Bước 2: Phát hiện paragraph boundaries
# Một paragraph mới bắt đầu khi:
# - Dòng trước là dòng trống
# - Dòng trước là dòng cuối của footnote block (dòng không bắt đầu bằng tab sau các dòng footnote)
# - Dòng hiện không có indentation, bắt đầu bằng chữ hoa, và dòng trước kết thúc bằng dấu chấm/ngoặc
output = []
para_num = 0
current_page = None
in_fn_block = False
prev_line_ended_sentence = False
prev_line_blank = False
prev_line_was_fn_end = False

for i, (line, pg) in enumerate(filtered):
    s = line.strip()
    
    # Cập nhật trang
    # (page đã được gán trong filtered, nhưng chúng ta cần theo dõi)
    # Tìm page từ dòng số trang gần nhất trước dòng này
    # Dùng cách khác: quét lại
    
    # Dòng trống
    if not s:
        output.append("")
        prev_line_blank = True
        prev_line_ended_sentence = False
        prev_line_was_fn_end = False
        in_fn_block = False
        continue
    
    # Footnote line
    if FN_RE.match(s):
        if not in_fn_block:
            # Bắt đầu block footnote
            in_fn_block = True
        output.append(line)
        prev_line_blank = False
        prev_line_ended_sentence = False
        prev_line_was_fn_end = False
        continue
    
    # Dòng không phải footnote sau block footnote → kết thúc footnote block
    if in_fn_block and not FN_RE.match(s):
        in_fn_block = False
        prev_line_was_fn_end = True
    
    # Xác định có phải đầu paragraph mới không
    is_new_para = False
    
    if prev_line_blank or prev_line_was_fn_end:
        is_new_para = True
    elif not s.startswith((" ", "\t")) and s and s[0].isalpha() and prev_line_ended_sentence:
        is_new_para = True
    
    if is_new_para:
        para_num += 1
        marker = f"--- [V1C13-P{para_num:03d}] (trang {pg if pg else '?'}) ---"
        output.append(marker)
        output.append(line)
    else:
        output.append(line)
    
    # Cập nhật trạng thái dòng trước
    prev_line_blank = False
    prev_line_ended_sentence = s.endswith((".", "!", "?", "”", "”", "’")) or s.endswith('"')
    prev_line_was_fn_end = False

OUT.write_text("\n".join(output), encoding="utf-8", newline="\n")
print(f"Created {OUT}: {para_num} segments")
