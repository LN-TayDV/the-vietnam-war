#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common Script: File Integrity Checker
Kiểm tra cấu trúc 2 file/chương, encoding UTF-8, tên file, cấu trúc thư mục.
Dùng chung cho tất cả skills.
"""

import os
import sys
import json
import argparse
from pathlib import Path


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project").is_dir():
            return parent
    return Path.cwd()


def check_encoding(filepath: Path) -> dict:
    """Kiểm tra encoding UTF-8, NFC, no BOM, LF."""
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
        
        # Check BOM
        has_bom = raw.startswith(b'\xef\xbb\xbf')
        
        # Try decode UTF-8
        try:
            text = raw.decode('utf-8')
            utf8_ok = True
        except UnicodeDecodeError:
            utf8_ok = False
            text = raw.decode('utf-8', errors='replace')
        
        # Check NFC
        import unicodedata
        nfc_ok = text == unicodedata.normalize('NFC', text)
        
        # Check line endings
        has_crlf = b'\r\n' in raw
        has_lf = b'\n' in raw and not has_crlf
        
        return {
            "file": str(filepath),
            "utf8_ok": utf8_ok,
            "nfc_ok": nfc_ok,
            "no_bom": not has_bom,
            "lf_only": has_lf and not has_crlf,
            "encoding_pass": utf8_ok and nfc_ok and not has_bom and has_lf and not has_crlf
        }
    except Exception as e:
        return {
            "file": str(filepath),
            "error": str(e),
            "encoding_pass": False
        }


def check_chapter_structure(chapter_dir: Path) -> dict:
    """Kiểm tra cấu trúc 2 file trong thư mục chương."""
    src_file = chapter_dir / f"{chapter_dir.parent.name}_ch{chapter_dir.name[-2:]}_src.txt"
    vi_file = chapter_dir / f"{chapter_dir.parent.name}_ch{chapter_dir.name[-2:]}_vi.txt"
    
    # Find actual files
    src_files = list(chapter_dir.glob("*_src.txt"))
    vi_files = list(chapter_dir.glob("*_vi.txt"))
    
    result = {
        "chapter_dir": str(chapter_dir),
        "src_files": [str(f) for f in src_files],
        "vi_files": [str(f) for f in vi_files],
        "has_src": len(src_files) > 0,
        "has_vi": len(vi_files) > 0,
        "extra_files": [],
        "structure_pass": False
    }
    
    # Check for extra files (not src, vi, or .gitkeep)
    all_files = list(chapter_dir.glob("*"))
    allowed_suffixes = {'.txt', '.gitkeep'}
    for f in all_files:
        if f.is_file() and f.suffix not in allowed_suffixes:
            result["extra_files"].append(str(f))
    
    # Structure pass: exactly 1 src and 1 vi (or at least 1 each)
    result["structure_pass"] = (len(src_files) >= 1 and len(vi_files) >= 1 and len(result["extra_files"]) == 0)
    
    return result


def check_chapter_files(chapter_dir: Path) -> dict:
    """Kiểm tra chi tiết file src và vi: số đoạn, encoding."""
    src_files = list(chapter_dir.glob("*_src.txt"))
    vi_files = list(chapter_dir.glob("*_vi.txt"))
    
    if not src_files or not vi_files:
        return {"error": "Missing src or vi file"}
    
    src_file = src_files[0]
    vi_file = vi_files[0]
    
    # Count paragraphs
    def count_paragraphs(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            import re
            paras = re.findall(r'--- \[V\d+C\d{2}-P\d{3}\]', content)
            return len(paras)
        except:
            return 0
    
    src_paras = count_paragraphs(src_file)
    vi_paras = count_paragraphs(vi_file)
    
    src_enc = check_encoding(src_file)
    vi_enc = check_encoding(vi_file)
    
    return {
        "src_file": str(src_file),
        "vi_file": str(vi_file),
        "src_paragraphs": src_paras,
        "vi_paragraphs": vi_paras,
        "paragraphs_match": src_paras == vi_paras and src_paras > 0,
        "src_encoding": src_enc,
        "vi_encoding": vi_enc
    }


def main():
    parser = argparse.ArgumentParser(description="File Integrity Checker for translation project")
    parser.add_argument("--chapter", type=int, help="Chapter number (e.g., 7)")
    parser.add_argument("--volume", default="v1", help="Volume (v1, v2, v3)")
    parser.add_argument("--all", action="store_true", help="Check all chapters")
    parser.add_argument("--root", default=None, help="Project root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    root = Path(args.root) if args.root else find_root()
    trans_dir = root / "translation-project" / "04_translation" / args.volume.lower()
    
    if not trans_dir.exists():
        print(f"ERROR: Translation directory not found: {trans_dir}", file=sys.stderr)
        sys.exit(1)
    
    chapters = []
    if args.all:
        for d in sorted(trans_dir.iterdir()):
            if d.is_dir() and d.name.startswith("ch"):
                try:
                    ch_num = int(d.name[2:])
                    chapters.append((ch_num, d))
                except:
                    pass
    elif args.chapter:
        ch_dir = trans_dir / f"ch{args.chapter:02d}"
        if ch_dir.exists():
            chapters.append((args.chapter, ch_dir))
        else:
            print(f"ERROR: Chapter directory not found: {ch_dir}", file=sys.stderr)
            sys.exit(1)
    else:
        print("ERROR: Specify --chapter N or --all", file=sys.stderr)
        sys.exit(1)
    
    results = []
    all_pass = True
    
    for ch_num, ch_dir in chapters:
        struct = check_chapter_structure(ch_dir)
        files = check_chapter_files(ch_dir)
        
        ch_result = {
            "chapter": ch_num,
            "structure": struct,
            "files": files,
            "overall_pass": struct.get("structure_pass", False) and files.get("paragraphs_match", False) and files.get("src_encoding", {}).get("encoding_pass", False) and files.get("vi_encoding", {}).get("encoding_pass", False)
        }
        
        if not ch_result["overall_pass"]:
            all_pass = False
        
        results.append(ch_result)
    
    summary = {
        "volume": args.volume,
        "chapters_checked": len(results),
        "all_pass": all_pass,
        "results": results
    }
    
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        for r in results:
            status = "PASS" if r["overall_pass"] else "FAIL"
            print(f"Ch{r['chapter']:02d}: {status}")
            if not r["overall_pass"]:
                if not r["structure"].get("structure_pass"):
                    print(f"  Structure: FAIL - src={len(r['structure']['src_files'])}, vi={len(r['structure']['vi_files'])}, extra={len(r['structure']['extra_files'])}")
                if not r["files"].get("paragraphs_match"):
                    print(f"  Paragraphs: FAIL - src={r['files'].get('src_paragraphs')}, vi={r['files'].get('vi_paragraphs')}")
                if not r["files"].get("src_encoding", {}).get("encoding_pass"):
                    print(f"  Src Encoding: FAIL - {r['files'].get('src_encoding')}")
                if not r["files"].get("vi_encoding", {}).get("encoding_pass"):
                    print(f"  Vi Encoding: FAIL - {r['files'].get('vi_encoding')}")
    
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()