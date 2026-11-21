#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common Script: Encoding Checker
Kiểm tra UTF-8, NFC, no BOM, LF.
Dùng cho translation-quality-gate, translation-error-detection.
"""

import os
import sys
import json
import argparse
import unicodedata
from pathlib import Path


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project").is_dir():
            return parent
    return Path.cwd()


def check_file_encoding(filepath: Path) -> dict:
    """Kiểm tra chi tiết encoding của một file."""
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
    except Exception as e:
        return {
            "file": str(filepath),
            "error": str(e),
            "pass": False
        }
    
    # Check BOM
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    has_utf16_be = raw.startswith(b'\xfe\xff')
    has_utf16_le = raw.startswith(b'\xff\xfe')
    
    # Try decode UTF-8
    utf8_ok = False
    text = ""
    try:
        text = raw.decode('utf-8')
        utf8_ok = True
    except UnicodeDecodeError as e:
        # Try to detect actual encoding
        import chardet
        detected = chardet.detect(raw)
        return {
            "file": str(filepath),
            "pass": False,
            "encoding": detected.get('encoding'),
            "confidence": detected.get('confidence'),
            "utf8_ok": False,
            "has_bom": has_bom,
            "error": f"Not valid UTF-8: {e}"
        }
    
    # Check NFC normalization
    nfc_ok = text == unicodedata.normalize('NFC', text)
    if not nfc_ok:
        # Find non-NFC characters
        non_nfc_chars = []
        for i, ch in enumerate(text):
            if ch != unicodedata.normalize('NFC', ch):
                non_nfc_chars.append({"char": ch, "codepoint": f"U+{ord(ch):04X}", "position": i})
                if len(non_nfc_chars) > 10:
                    break
    else:
        non_nfc_chars = []
    
    # Check line endings
    has_crlf = b'\r\n' in raw
    has_lf = b'\n' in raw
    has_cr_only = b'\r' in raw and not has_crlf
    
    # Check for control characters (except normal ones)
    control_chars = []
    for i, ch in enumerate(text):
        if ord(ch) < 32 and ch not in '\n\r\t':
            control_chars.append({"char": repr(ch), "codepoint": f"U+{ord(ch):04X}", "position": i})
            if len(control_chars) > 10:
                break
    
    return {
        "file": str(filepath),
        "size_bytes": len(raw),
        "pass": utf8_ok and nfc_ok and not has_bom and not has_crlf and not has_utf16_be and not has_utf16_le and not control_chars,
        "utf8_ok": utf8_ok,
        "nfc_ok": nfc_ok,
        "no_bom": not has_bom,
        "no_utf16_bom": not has_utf16_be and not has_utf16_le,
        "lf_only": has_lf and not has_crlf,
        "has_crlf": has_crlf,
        "has_cr_only": has_cr_only,
        "non_nfc_chars": non_nfc_chars[:10],
        "control_chars": control_chars[:10],
        "line_count": text.count('\n') + 1
    }


def check_directory(root: Path, volume: str = "v1") -> dict:
    """Kiểm tra tất cả file .txt trong thư mục dịch."""
    trans_dir = root / "translation-project" / "04_translation" / volume.lower()
    
    if not trans_dir.exists():
        return {"error": f"Directory not found: {trans_dir}"}
    
    results = []
    all_pass = True
    
    for txt_file in trans_dir.rglob("*.txt"):
        result = check_file_encoding(txt_file)
        results.append(result)
        if not result.get("pass", False):
            all_pass = False
    
    return {
        "volume": volume,
        "files_checked": len(results),
        "all_pass": all_pass,
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Encoding Checker - UTF-8, NFC, no BOM, LF")
    parser.add_argument("--file", help="Specific file to check")
    parser.add_argument("--chapter", type=int, help="Chapter number")
    parser.add_argument("--volume", default="v1", help="Volume")
    parser.add_argument("--all", action="store_true", help="Check all chapters in volume")
    parser.add_argument("--root", default=None, help="Project root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    root = Path(args.root) if args.root else find_root()
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = root / file_path
        result = check_file_encoding(file_path)
    elif args.all:
        result = check_directory(root, args.volume)
    elif args.chapter:
        ch_dir = root / "translation-project" / "04_translation" / args.volume.lower() / f"ch{args.chapter:02d}"
        # Check both src and vi files
        results = []
        for pattern in ["*_src.txt", "*_vi.txt"]:
            for f in ch_dir.glob(pattern):
                results.append(check_file_encoding(f))
        result = {
            "chapter": args.chapter,
            "volume": args.volume,
            "files_checked": len(results),
            "all_pass": all(r.get("pass", False) for r in results),
            "results": results
        }
    else:
        print("ERROR: Specify --file, --chapter, or --all", file=sys.stderr)
        sys.exit(1)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Print summary
        if "files_checked" in result:
            print(f"Encoding Check: {result['volume']} - {result['files_checked']} files")
            print(f"  All PASS: {result['all_pass']}")
            for r in result.get("results", []):
                status = "PASS" if r.get("pass") else "FAIL"
                fname = Path(r["file"]).name
                print(f"  {fname}: {status}")
                if not r.get("pass"):
                    if not r.get("utf8_ok"): print(f"    - Not valid UTF-8")
                    if not r.get("nfc_ok"): print(f"    - Not NFC normalized ({len(r.get('non_nfc_chars', []))} chars)")
                    if not r.get("no_bom"): print(f"    - Has BOM")
                    if r.get("has_crlf"): print(f"    - Has CRLF line endings")
                    if r.get("control_chars"): print(f"    - Has control chars ({len(r['control_chars'])})")
        else:
            r = result
            status = "PASS" if r.get("pass") else "FAIL"
            print(f"{Path(r['file']).name}: {status}")
            if not r.get("pass"):
                if not r.get("utf8_ok"): print(f"  - Not valid UTF-8: {r.get('error')}")
                if not r.get("nfc_ok"): print(f"  - Not NFC normalized ({len(r.get('non_nfc_chars', []))} chars)")
                if not r.get("no_bom"): print(f"  - Has BOM")
                if r.get("has_crlf"): print(f"  - Has CRLF line endings")
                if r.get("control_chars"): print(f"  - Has control chars ({len(r['control_chars'])})")
    
    sys.exit(0 if result.get("all_pass", result.get("pass", False)) else 1)


if __name__ == "__main__":
    main()