#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Realign Vietnamese translation to match English source paragraph structure.
Uses content similarity (SequenceMatcher) to match paragraphs.
"""
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "02_extracted_text" / "v2"
VI_DIR = ROOT / "04_translation" / "v2"

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def extract_paragraphs(text: str) -> list:
    """Extract paragraphs with markers."""
    pattern = r'(\[V1[^\]]+\] \(trang \d+\))\n(.*?)(?=\n\[V1[^\]]+\] \(trang \d+\)|\n=== FOOTNOTES ===|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    paragraphs = []
    for i, (marker, content) in enumerate(matches):
        para_id_match = re.search(r'\[(V1[^\]]+)\]', marker)
        pid = para_id_match.group(1) if para_id_match else f"P{i+1:03d}"
        content = content.strip()
        paragraphs.append({
            "id": pid,
            "marker": marker.strip(),
            "content": content,
            "char_count": len(content),
            "sentence_count": len([s for s in re.split(r'[.!?]+', content) if s.strip()])
        })
    return paragraphs


def extract_footnotes(text: str) -> list:
    """Extract footnotes from === FOOTNOTES === section."""
    fn_match = re.search(r'=== FOOTNOTES ===\n(.*)', text, re.DOTALL)
    if not fn_match:
        return []
    fn_text = fn_match.group(1)
    fn_pattern = r'(?:^|\n)([' + SUP + r']+|\d+)\.?\s*(.*?)(?=\n[' + SUP + r']+|\n\d+\.?\s|\Z)'
    matches = re.findall(fn_pattern, fn_text, re.DOTALL)
    footnotes = []
    for num, text in matches:
        if num[0] in SUP:
            n = ""
            for c in num:
                if c in SUP:
                    n += str(SUP.index(c))
            num = n
        footnotes.append({"number": num.strip(), "text": text.strip()})
    return footnotes


def similarity(a: str, b: str) -> float:
    """Calculate similarity between two texts."""
    return SequenceMatcher(None, a, b).ratio()


def match_paragraphs(src_paras: list, vi_paras: list, threshold: float = 0.3) -> list:
    """Match Vietnamese paragraphs to English source paragraphs by content similarity.
    Returns list of (src_idx, vi_idx, similarity) tuples."""
    matches = []
    used_vi = set()
    
    for src_idx, src_para in enumerate(src_paras):
        best_match = None
        best_score = 0
        
        for vi_idx, vi_para in enumerate(vi_paras):
            if vi_idx in used_vi:
                continue
            score = similarity(src_para["content"], vi_para["content"])
            if score > best_score and score >= threshold:
                best_score = score
                best_match = vi_idx
        
        if best_match is not None:
            matches.append((src_idx, best_match, best_score))
            used_vi.add(best_match)
        else:
            matches.append((src_idx, None, 0))
    
    return matches


def realign_chapter(chapter: int):
    """Realign a single chapter."""
    src_file = SRC_DIR / f"v2_ch{chapter:02d}_src.txt"
    vi_file = VI_DIR / f"ch{chapter:02d}" / f"v2_ch{chapter:02d}_vi.txt"
    
    if not src_file.exists() or not vi_file.exists():
        print(f"Files not found for chapter {chapter}")
        return False
    
    src_text = src_file.read_text(encoding="utf-8")
    vi_text = vi_file.read_text(encoding="utf-8")
    
    src_paras = extract_paragraphs(src_text)
    vi_paras = extract_paragraphs(vi_text)
    vi_fns = extract_footnotes(vi_text)
    
    print(f"\nChapter {chapter}:")
    print(f"  English paragraphs: {len(src_paras)}")
    print(f"  Vietnamese paragraphs: {len(vi_paras)}")
    print(f"  Vietnamese footnotes: {len(vi_fns)}")
    
    # Match paragraphs
    matches = match_paragraphs(src_paras, vi_paras, threshold=0.25)
    
    matched = sum(1 for m in matches if m[1] is not None)
    print(f"  Matched: {matched}/{len(src_paras)}")
    
    # Show unmatched source paragraphs
    for src_idx, vi_idx, score in matches:
        if vi_idx is None:
            print(f"    UNMATCHED src[{src_idx}]={src_paras[src_idx]['id']}: {src_paras[src_idx]['content'][:80]}...")
        elif score < 0.5:
            print(f"    LOW MATCH src[{src_idx}]={src_paras[src_idx]['id']} <-> vi[{vi_idx}]={vi_paras[vi_idx]['id']} (score={score:.2f})")
    
    # Show unused Vietnamese paragraphs
    used_vi = {m[1] for m in matches if m[1] is not None}
    for vi_idx, vi_para in enumerate(vi_paras):
        if vi_idx not in used_vi:
            print(f"    UNUSED vi[{vi_idx}]={vi_para['id']}: {vi_para['content'][:80]}...")
    
    return matches


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python realign_chapter.py <chapter_num> [chapter_num...]")
        sys.exit(1)
    
    for arg in sys.argv[1:]:
        ch = int(arg)
        realign_chapter(ch)