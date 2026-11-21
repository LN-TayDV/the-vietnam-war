#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    vi = f.read()

# Find all footnote markers [number]
src_markers = re.findall(r'\[(\d+)\]', src)
vi_markers = re.findall(r'\[(\d+)\]', vi)

with open('marker_check.txt', 'w', encoding='utf-8') as out:
    out.write('Source markers: ' + str(sorted(set(int(x) for x in src_markers))) + '\n')
    out.write('VI markers: ' + str(sorted(set(int(x) for x in vi_markers))) + '\n')

    # Check for 'đạo chính' in both
    out.write('\n=== Source: đạo chính ===\n')
    for m in re.finditer(r'đạo chính', src):
        out.write(f'Pos {m.start()}: ...{src[max(0,m.start()-30):m.end()+30]}...\n')

    out.write('\n=== VI: đạo chính ===\n')
    for m in re.finditer(r'đạo chính', vi):
        out.write(f'Pos {m.start()}: ...{vi[max(0,m.start()-30):m.end()+30]}...\n')

    # Check for 'giải phóng' in VI
    out.write('\n=== VI: giải phóng ===\n')
    for m in re.finditer(r'giải phóng', vi):
        out.write(f'Pos {m.start()}: ...{vi[max(0,m.start()-30):m.end()+30]}...\n')

    # Check for 'chính' in 'chính sách' etc in VI
    out.write('\n=== VI: chính sách ===\n')
    for m in re.finditer(r'chính sách', vi):
        out.write(f'Pos {m.start()}: ...{vi[max(0,m.start()-30):m.end()+30]}...\n')

    out.write('\n=== VI: chính quyền ===\n')
    for m in re.finditer(r'chính quyền', vi):
        out.write(f'Pos {m.start()}: ...{vi[max(0,m.start()-30):m.end()+30]}...\n')

    out.write('\n=== VI: chính thể ===\n')
    for m in re.finditer(r'chính thể', vi):
        out.write(f'Pos {m.start()}: ...{vi[max(0,m.start()-30):m.end()+30]}...\n')

    out.write('\n=== VI: chính quy ===\n')
    for m in re.finditer(r'chính quy', vi):
        out.write(f'Pos {m.start()}: ...{vi[max(0,m.start()-30):m.end()+30]}...\n')