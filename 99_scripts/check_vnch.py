#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, r'.kilo/scripts/common')
from vnch_orthography import check_vnch_rules

result = check_vnch_rules('translation-project/04_translation/v1/ch09/v1_ch09_vi.txt')

with open('vnch_details.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total issues: {len(result)}\n')
    for issue in result:
        f.write(f'[{issue["severity"]}] {issue["rule_id"]}: {issue["found"]} -> {issue["expected"]}\n')
        f.write(f'  Context: {issue["context"]}\n\n')