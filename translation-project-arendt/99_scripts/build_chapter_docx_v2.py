#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI wrapper for DOCX Builder v2.

Usage:
    python 99_scripts/build_chapter_docx_v2.py ch04 [ch05 ...]
    python 99_scripts/build_chapter_docx_v2.py --all
"""
from docx_builder_v2.builder import main

if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
