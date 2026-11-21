#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiem tra alignment src vs vi va encoding.
Ghi ket qua ra file de tranh loi encoding console.
"""
import re
import unicodedata
from pathlib import Path

SRC = Path("translation-project/04_translation/v1/ch01/v1_ch01_src.txt")
VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

def read_file(p):
    raw = p.read_bytes()
    text = raw.decode("utf-8")
    text = unicodedata.normalize("NFC", text)
    return text, raw

src_text, src_raw = read_file(SRC)
vi_text, vi_raw = read_file(VI)

# Kiem tra encoding
src_bom = src_raw[:3] == b'\xef\xbb\xbf'
vi_bom = vi_raw[:3] == b'\xef\xbb\xbf'
src_crlf = b'\r\n' in src_raw
vi_crlf = b'\r\n' in vi_raw
src_lf = b'\n' in src_raw and b'\r' not in src_raw
vi_lf = b'\n' in vi_raw and b'\r' not in vi_raw

# Kiem tra NFC
src_nfc = src_text == unicodedata.normalize("NFC", src_text)
vi_nfc = vi_text == unicodedata.normalize("NFC", vi_text)

# Dem so doan Pxxx
src_paras = re.findall(r'--- \[V1C01-P(\d+)\]', src_text)
vi_paras = re.findall(r'--- \[V1C01-P(\d+)\]', vi_text)

out = []
out.append("=== KIEM TRA ALIGNMENT VA ENCODING ===")
out.append("")
out.append(f"SRC file: {SRC.name}")
out.append(f"VI file: {VI.name}")
out.append("")
out.append("--- Encoding ---")
out.append(f"SRC BOM: {src_bom}, VI BOM: {vi_bom}")
out.append(f"SRC CRLF: {src_crlf}, VI CRLF: {vi_crlf}")
out.append(f"SRC LF-only: {src_lf}, VI LF-only: {vi_lf}")
out.append(f"SRC NFC: {src_nfc}, VI NFC: {vi_nfc}")
out.append("")
out.append("--- Alignment ---")
out.append(f"SRC so doan: {len(src_paras)}")
out.append(f"VI so doan: {len(vi_paras)}")
out.append(f"SRC cac so: {src_paras[:5]} ... {src_paras[-5:]}")
out.append(f"VI cac so: {vi_paras[:5]} ... {vi_paras[-5:]}")
out.append(f"Marker khop 1-1: {src_paras == vi_paras}")
out.append("")
out.append("--- Ket thuc ===")

Path("99_scripts/alignment_check.txt").write_text("\n".join(out), encoding="utf-8", newline="\n")
print("Da ghi ket qua kiem tra vao 99_scripts/alignment_check.txt")
