#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug alignment: kiem tra so doan src vs vi, so cau moi doan.
Dung truoc khi build DOCX de dam bao alignment 1-1 (Quy tac 18).

Usage:
    python 99_scripts/debug_align.py 01
    python 99_scripts/debug_align.py 01 02 03
"""

import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT / "04_translation" / "v1"
VI_DIR = PROJECT / "04_translation" / "v1"

P_HDR = re.compile(r"^--- \[([A-Za-z0-9]+-P\d+)\]")

def split_paragraphs(content):
    """Split by paragraph markers, return list of (header, text)."""
    blocks = re.split(r'--- \[([A-Za-z0-9]+-P\d+)\]', content)
    result = []
    for i in range(1, len(blocks), 2):
        header = blocks[i].strip()
        text = blocks[i+1].strip() if i+1 < len(blocks) else ""
        result.append((header, text))
    return result

def count_sentences(text):
    """Count sentences in text (rough)."""
    if not text:
        return 0
    # Simple sentence splitter
    sents = re.split(r'(?<=[.!?])\s+(?=[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲÝỴỶỸĐ])', text)
    return len([s for s in sents if s.strip()])

def check_chapter(chap_no):
    """Check alignment for one chapter."""
    chap_no = chap_no.zfill(2)
    
    src_file = SRC_DIR / f"ch{chap_no}" / f"v1_ch{chap_no}_src.txt"
    vi_file = VI_DIR / f"ch{chap_no}" / f"v1_ch{chap_no}_vi_FINAL.txt"
    
    if not src_file.exists():
        print(f"Ch{chap_no}: SRC NOT FOUND: {src_file}")
        return False
    if not vi_file.exists():
        print(f"Ch{chap_no}: VI NOT FOUND: {vi_file}")
        return False
    
    src_content = src_file.read_text(encoding="utf-8")
    vi_content = vi_file.read_text(encoding="utf-8")
    
    src_paras = split_paragraphs(src_content)
    vi_paras = split_paragraphs(vi_content)
    
    print(f"\n=== Ch{chap_no} ===")
    print(f"  Source paragraphs: {len(src_paras)}")
    print(f"  Translation paragraphs: {len(vi_paras)}")
    
    if len(src_paras) != len(vi_paras):
        print(f"  [FAIL] MISMATCH: src={len(src_paras)} vs vi={len(vi_paras)}")
        return False
    
    # Check sentence counts per paragraph
    mismatches = []
    for i, ((src_h, src_t), (vi_h, vi_t)) in enumerate(zip(src_paras, vi_paras)):
        src_sents = count_sentences(src_t)
        vi_sents = count_sentences(vi_t)
        
        if src_sents != vi_sents:
            mismatches.append((i+1, src_h, src_sents, vi_sents))
    
    if mismatches:
        print(f"  [WARN] Sentence count mismatches in {len(mismatches)} paragraphs:")
        for idx, h, src_s, vi_s in mismatches[:10]:
            print(f"    P{idx:03d} ({h}): src={src_s} sents, vi={vi_s} sents")
        if len(mismatches) > 10:
            print(f"    ... and {len(mismatches)-10} more")
        return False
    
    print(f"  [PASS] {len(src_paras)} paragraphs, all sentence counts match")
    return True

def main():
    if len(sys.argv) < 2:
        # Check all chapters
        chapters = sorted([d.name[-2:] for d in SRC_DIR.glob("ch*") if d.is_dir()])
    else:
        chapters = [c.zfill(2) for c in sys.argv[1:]]
    
    print(f"Checking alignment for chapters: {', '.join(chapters)}")
    
    all_pass = True
    for chap in chapters:
        if not check_chapter(chap):
            all_pass = False
    
    print(f"\n{'='*50}")
    if all_pass:
        print("[PASS] ALL CHAPTERS PASS alignment check")
        return 0
    else:
        print("[FAIL] SOME CHAPTERS FAIL alignment check")
        return 1

if __name__ == "__main__":
    sys.exit(main())