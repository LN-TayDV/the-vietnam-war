#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, r'.kilo/scripts/common')
from quality_gate import (
    check_encoding, check_orthography, check_alignment, 
    check_footnotes_alignment, check_fabricate, check_writing_style,
    check_docx_exists, check_docx_footnotes, find_root
)
from pathlib import Path

project_root = find_root()
volume = 'v1'
chapter = 9

results = {}

# 1. Encoding
results['encoding'] = check_encoding(project_root, volume, chapter)

# 2. Orthography
results['orthography'] = check_orthography(project_root, volume, chapter)

# 3. Alignment
results['alignment'] = check_alignment(project_root, volume, chapter)

# 4. Footnotes alignment
results['footnotes'] = check_footnotes_alignment(project_root, volume, chapter)

# 5. Fabricate
results['fabricate'] = check_fabricate(project_root, volume, chapter)

# 6. Writing style
results['style'] = check_writing_style(project_root, volume, chapter)

# 7. DOCX exists
results['docx_exists'] = check_docx_exists(project_root, volume, chapter)

# 8. DOCX footnotes
results['docx_footnotes'] = check_docx_footnotes(project_root, volume, chapter)

with open('qg_results.txt', 'w', encoding='utf-8') as f:
    for key, value in results.items():
        f.write(f'{key}: {value}\n')