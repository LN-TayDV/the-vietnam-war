#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common Script: Document Comparator
Đối chiếu src vs vi: số đoạn, số câu, cấu trúc, alignment.
Dùng chung cho deep-translation-review, translation-error-detection.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from difflib import SequenceMatcher


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project-arendt").is_dir():
            return parent
    return Path.cwd()


def extract_paragraphs(text: str) -> list:
    """Trích xuất các đoạn với marker và nội dung."""
    # Format: [V1C01-P001] (trang 1)\ncontent\n\n[V1C01-P002] (trang 2)\ncontent
    # Or English: [V1-CH-P001] (trang 23)\ncontent\n\n[V1-CH-P002] (trang 23)\ncontent
    # Match any [V1...] (trang ...) pattern
    pattern = r'(\[V1[^\]]+\] \(trang \d+\))\n(.*?)(?=\n\[V1[^\]]+\] \(trang \d+\)|\n=== FOOTNOTES ===|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    
    paragraphs = []
    for i, (marker, content) in enumerate(matches):
        # Extract paragraph ID from marker
        para_id_match = re.search(r'\[(V1[^\]]+)\]', marker)
        if para_id_match:
            pid = para_id_match.group(1)
        else:
            pid = f"P{i+1:03d}"
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
    """Trích xuất cước chú."""
    # Find footnote section
    fn_match = re.search(r'=== FOOTNOTES ===\n(.*)', text, re.DOTALL)
    if not fn_match:
        return []
    
    fn_text = fn_match.group(1)
    # Pattern: superscript numbers like ¹, ², ³ or [1], 1., etc.
    SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    fn_pattern = r'(?:^|\n)([' + SUP + r']+|\d+)\.?\s*(.*?)(?=\n[' + SUP + r']+|\n\d+\.?\s|\Z)'
    matches = re.findall(fn_pattern, fn_text, re.DOTALL)
    
    footnotes = []
    for num, text in matches:
        # Convert superscript to number
        if num[0] in SUP:
            n = ""
            for c in num:
                if c in SUP:
                    n += str(SUP.index(c))
            num = n
        footnotes.append({
            "number": num.strip(),
            "text": text.strip()
        })
    return footnotes


def compare_paragraphs(src_paras: list, vi_paras: list) -> dict:
    """So sánh chi tiết từng đoạn."""
    results = {
        "total_src": len(src_paras),
        "total_vi": len(vi_paras),
        "matching_ids": 0,
        "missing_in_vi": [],
        "missing_in_src": [],
        "sentence_mismatches": [],
        "char_ratio_mismatches": [],
        "details": []
    }
    
    # Create lookup
    src_by_id = {p["id"]: p for p in src_paras}
    vi_by_id = {p["id"]: p for p in vi_paras}
    
    all_ids = set(src_by_id.keys()) | set(vi_by_id.keys())
    
    # Loại bỏ paragraph IMAGE (caption riêng) khỏi so sánh alignment
    # vì chúng được thêm để trình bày hình ảnh trong DOCX, không phải nội dung dịch.
    all_ids = {pid for pid in all_ids if "-IMG" not in pid}
    
    for pid in sorted(all_ids):
        src = src_by_id.get(pid)
        vi = vi_by_id.get(pid)
        
        if src and vi:
            results["matching_ids"] += 1
            src_sents = src["sentence_count"]
            vi_sents = vi["sentence_count"]
            
            if src_sents != vi_sents:
                results["sentence_mismatches"].append({
                    "id": pid,
                    "src_sentences": src_sents,
                    "vi_sentences": vi_sents,
                    "diff": vi_sents - src_sents
                })
            
            # Character ratio check (should be roughly similar for translation)
            if src["char_count"] > 0:
                ratio = vi["char_count"] / src["char_count"]
                if ratio < 0.5 or ratio > 2.0:
                    results["char_ratio_mismatches"].append({
                        "id": pid,
                        "src_chars": src["char_count"],
                        "vi_chars": vi["char_count"],
                        "ratio": round(ratio, 2)
                    })
            
            results["details"].append({
                "id": pid,
                "src_chars": src["char_count"],
                "vi_chars": vi["char_count"],
                "src_sents": src["sentence_count"],
                "vi_sents": vi["sentence_count"],
                "match": True
            })
        elif src and not vi:
            results["missing_in_vi"].append(pid)
        elif vi and not src:
            results["missing_in_src"].append(pid)
    
    return results


def compare_footnotes(src_fns: list, vi_fns: list) -> dict:
    """So sánh cước chú."""
    src_nums = {fn["number"]: fn for fn in src_fns}
    vi_nums = {fn["number"]: fn for fn in vi_fns}
    
    all_nums = set(src_nums.keys()) | set(vi_nums.keys())
    
    return {
        "total_src": len(src_fns),
        "total_vi": len(vi_fns),
        "matching_count": len(set(src_nums.keys()) & set(vi_nums.keys())),
        "missing_in_vi": sorted(set(src_nums.keys()) - set(vi_nums.keys())),
        "extra_in_vi": sorted(set(vi_nums.keys()) - set(src_nums.keys())),
        "sequence_check": {
            "src_sequence": [int(n) for n in src_nums.keys() if n.isdigit()],
            "vi_sequence": [int(n) for n in vi_nums.keys() if n.isdigit()],
            "src_continuous": all(int(n) == i+1 for i, n in enumerate(sorted([int(x) for x in src_nums.keys() if x.isdigit()]))),
            "vi_continuous": all(int(n) == i+1 for i, n in enumerate(sorted([int(x) for x in vi_nums.keys() if x.isdigit()]))),
        }
    }


def check_markers_inline(vi_text: str) -> dict:
    """Kiểm tra marker cước chú [N] hoặc superscript trong thân bài."""
    SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    # Only search body text (before === FOOTNOTES ===)
    body = vi_text.split("=== FOOTNOTES ===")[0]
    # Find all [N] patterns in text
    bracket_markers = re.findall(r'\[(\d+)\]', body)
    # Find all superscript runs
    sup_runs = re.findall(r'[' + SUP + r']+', body)
    sup_markers = []
    for run in sup_runs:
        n = ""
        for c in run:
            if c in SUP:
                n += str(SUP.index(c))
        if n:
            sup_markers.append(int(n))
    
    bracket_nums = [int(m) for m in bracket_markers]
    all_markers = bracket_nums + sup_markers
    
    return {
        "total_markers": len(all_markers),
        "unique_markers": len(set(all_markers)),
        "sequence": all_markers,
        "has_duplicates": len(all_markers) != len(set(all_markers)),
        "max_marker": max(all_markers) if all_markers else 0
    }


def calculate_similarity(text1: str, text2: str) -> float:
    """Tính độ tương đồng giữa hai văn bản."""
    return SequenceMatcher(None, text1, text2).ratio()


def main():
    parser = argparse.ArgumentParser(description="Document Comparator for src vs vi")
    parser.add_argument("--chapter", type=int, required=True, help="Chapter number")
    parser.add_argument("--volume", default="v1", help="Volume")
    parser.add_argument("--root", default=None, help="Project root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    root = Path(args.root) if args.root else find_root()
    
    ch_dir = root / "translation-project-arendt" / "04_translation" / args.volume.lower() / f"ch{args.chapter:02d}"
    vi_file = ch_dir / f"{args.volume.lower()}_ch{args.chapter:02d}_vi.txt"
    src_file = ch_dir / f"{args.volume.lower()}_ch{args.chapter:02d}_src.txt"
    
    if not vi_file.exists() or not src_file.exists():
        print(f"ERROR: Files not found for chapter {args.chapter}", file=sys.stderr)
        sys.exit(1)
    
    with open(src_file, 'r', encoding='utf-8') as f:
        src_text = f.read()
    with open(vi_file, 'r', encoding='utf-8') as f:
        vi_text = f.read()
    
    # Extract components
    src_paras = extract_paragraphs(src_text)
    vi_paras = extract_paragraphs(vi_text)
    src_fns = extract_footnotes(src_text)
    vi_fns = extract_footnotes(vi_text)
    
    # Compare
    para_comparison = compare_paragraphs(src_paras, vi_paras)
    fn_comparison = compare_footnotes(src_fns, vi_fns)
    marker_check = check_markers_inline(vi_text)
    
    # Overall similarity
    overall_similarity = calculate_similarity(
        " ".join(p["content"] for p in src_paras),
        " ".join(p["content"] for p in vi_paras)
    )
    
    result = {
        "chapter": args.chapter,
        "volume": args.volume,
        "paragraphs": para_comparison,
        "footnotes": fn_comparison,
        "inline_markers": marker_check,
        "overall_similarity": round(overall_similarity, 4),
        "alignment_pass": (
            para_comparison["total_src"] == para_comparison["total_vi"] and
            len(para_comparison["missing_in_vi"]) == 0 and
            len(para_comparison["missing_in_src"]) == 0 and
            len(para_comparison["sentence_mismatches"]) == 0
        )
    }
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Chapter {args.chapter} Document Comparison:")
        print(f"  Paragraphs: src={para_comparison['total_src']}, vi={para_comparison['total_vi']}, matching={para_comparison['matching_ids']}")
        print(f"  Alignment: {'PASS' if result['alignment_pass'] else 'FAIL'}")
        
        if para_comparison["missing_in_vi"]:
            print(f"  Missing in VI: {para_comparison['missing_in_vi']}")
        if para_comparison["missing_in_src"]:
            print(f"  Missing in SRC: {para_comparison['missing_in_src']}")
        if para_comparison["sentence_mismatches"]:
            print(f"  Sentence mismatches: {len(para_comparison['sentence_mismatches'])}")
            for m in para_comparison["sentence_mismatches"][:5]:
                print(f"    {m['id']}: src={m['src_sentences']}, vi={m['vi_sentences']} (diff={m['diff']})")
        
        print(f"  Footnotes: src={fn_comparison['total_src']}, vi={fn_comparison['total_vi']}, matching={fn_comparison['matching_count']}")
        if fn_comparison["missing_in_vi"]:
            print(f"  Missing footnotes in VI: {fn_comparison['missing_in_vi']}")
        if fn_comparison["extra_in_vi"]:
            print(f"  Extra footnotes in VI: {fn_comparison['extra_in_vi']}")
        
        print(f"  Inline markers: {marker_check['total_markers']} total, {marker_check['unique_markers']} unique")
        if marker_check['has_duplicates']:
            print(f"  WARNING: Duplicate markers detected!")
        
        print(f"  Overall similarity: {overall_similarity:.2%}")
    
    sys.exit(0 if result["alignment_pass"] else 1)


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project-arendt").is_dir():
            return parent
    return Path.cwd()


if __name__ == "__main__":
    main()