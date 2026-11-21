#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, r'.kilo/scripts/common')
from quality_gate import find_root
from pathlib import Path

root = find_root()
print(f'Root: {root}')
print(f'translation-project exists: {(root / "translation-project").is_dir()}')