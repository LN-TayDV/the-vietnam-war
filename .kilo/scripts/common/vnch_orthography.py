#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common Script: VNCH Orthography Checker
Kiểm tra 30 quy tắc VNCH từ apply_vnch_fixes.py logic.
Dùng cho southern-vietnamese-editorial-style, translation-error-detection.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project-arendt").is_dir():
            return parent
    return Path.cwd()


# 30 quy tắc VNCH từ audit 6 chương + Style Guide
VNCH_RULES = [
    # Core political terms (CRITICAL)
    {"id": "VNCH-01", "category": "core", "pattern": r"\bchính trị\b", "replacement": "chánh trị", "severity": "CRITICAL"},
    {"id": "VNCH-02", "category": "core", "pattern": r"\bchính phủ\b", "replacement": "chánh phủ", "severity": "CRITICAL"},
    {"id": "VNCH-03", "category": "core", "pattern": r"\bchính đảng\b", "replacement": "chánh đảng", "severity": "CRITICAL"},
    {"id": "VNCH-04", "category": "core", "pattern": r"\bđảo chính\b", "replacement": "đảo chánh", "severity": "CRITICAL"},
    {"id": "VNCH-05", "category": "core", "pattern": r"\btài chính\b", "replacement": "tài chánh", "severity": "CRITICAL"},
    {"id": "VNCH-06", "category": "core", "pattern": r"\blương hưu\b", "replacement": "hưu bổng", "severity": "CRITICAL"},
    {"id": "VNCH-07", "category": "core", "pattern": r"\bbất động sản\b", "replacement": "địa ốc", "severity": "CRITICAL"},
    {"id": "VNCH-08", "category": "core", "pattern": r"\bđại biểu\b", "replacement": "dân biểu", "severity": "CRITICAL"},
    {"id": "VNCH-09", "category": "core", "pattern": r"\bngân sách\b(?=\s*(cơ quan|ngân khố|ngân hàng))", "replacement": "ngân khố", "severity": "CRITICAL"},
    
    # Bắc/Nam terms (MAJOR)
    {"id": "VNCH-10", "category": "north_south", "pattern": r"\bgiải phóng\b", "replacement": "độc lập/kháng cự", "severity": "MAJOR", "exceptions": ["cờ giải phóng", "quân giải phóng", "mặt trận giải phóng"]},
    {"id": "VNCH-11", "category": "north_south", "pattern": r"\bđồng chí\b", "replacement": "đồng đạo", "severity": "MAJOR", "exceptions": ["thanh niên cách mạng đồng chí hội", "đồng chí hội"]},
    {"id": "VNCH-12", "category": "north_south", "pattern": r"\bnày\b(?!.*(?:trong|ngoài|trước|sau)\s+nầy)", "replacement": "nầy", "severity": "CRITICAL"},
    {"id": "VNCH-13", "category": "north_south", "pattern": r"\bmặc dù\b", "replacement": "dầu/dẫu", "severity": "MAJOR"},
    {"id": "VNCH-14", "category": "north_south", "pattern": r"\btuy nhiên\b", "replacement": "tuy vậy/đã vậy", "severity": "MAJOR"},
    {"id": "VNCH-15", "category": "north_south", "pattern": r"\bvì vậy\b", "replacement": "bởi thế/do đó", "severity": "MAJOR"},
    {"id": "VNCH-16", "category": "north_south", "pattern": r"\bhơn nữa\b", "replacement": "vả/lại", "severity": "MAJOR"},
    {"id": "VNCH-17", "category": "north_south", "pattern": r"\bngược lại\b", "replacement": "trái lại", "severity": "MAJOR"},
    {"id": "VNCH-18", "category": "north_south", "pattern": r"\bmà không\b", "replacement": "chớ không", "severity": "MAJOR"},
    {"id": "VNCH-19", "category": "north_south", "pattern": r"\bmà chẳng\b", "replacement": "chớ chẳng", "severity": "MAJOR"},
    {"id": "VNCH-20", "category": "north_south", "pattern": r"\bmà đâu\b", "replacement": "chớ đâu", "severity": "MAJOR"},
    
    # Colonial names - Rule 15 (MAJOR)
    {"id": "VNCH-21", "category": "colonial", "pattern": r"\bAnnam\b", "replacement": "Trung Kỳ (Annam)", "severity": "MAJOR"},
    {"id": "VNCH-22", "category": "colonial", "pattern": r"\bTonkin\b", "replacement": "Bắc Kỳ (Tonkin)", "severity": "MAJOR"},
    {"id": "VNCH-23", "category": "colonial", "pattern": r"\bCochinchina\b", "replacement": "Nam Kỳ (Cochinchina)", "severity": "MAJOR"},
    {"id": "VNCH-24", "category": "colonial", "pattern": r"\bCochinchine\b", "replacement": "Nam Kỳ (Cochinchine)", "severity": "MAJOR"},
    {"id": "VNCH-25", "category": "colonial", "pattern": r"\bIndochine\b", "replacement": "Đông Dương (Indochine)", "severity": "MAJOR"},
    {"id": "VNCH-26", "category": "colonial", "pattern": r"\bIndochina\b", "replacement": "Đông Dương (Indochina)", "severity": "MAJOR"},
    
    # Grammar rules (from VNCH Grammar Database)
    {"id": "VNCH-27", "category": "grammar", "pattern": r"\bmột\s+(sách|ký|người|ngày|năm|cái|cuốn|bài)\b(?! (cuốn|cái|con|người|ngài|cây|cục|bài))", "replacement": "một [classifier] + noun", "severity": "MINOR", "note": "Missing classifier (Rule 21)"},
    {"id": "VNCH-28", "category": "grammar", "pattern": r"\b(năm|ngày|trước|sau)\s+này\b(?! (trong|ngoài|trước|sau)\s+nầy)", "replacement": "nầy", "severity": "MINOR", "note": "Wrong demonstrative (Rule 22)"},
    {"id": "VNCH-29", "category": "grammar", "pattern": r"\bđang\s+\w+(?!\s+(xong|tiến hành|đang))", "replacement": "đang... xong/tiến hành", "severity": "MINOR", "note": "Incomplete aspect (Rule 23)"},
    {"id": "VNCH-30", "category": "grammar", "pattern": r"\b(hắn|y|nó)\b.*?(?:lập luận|nói|cho rằng|tin rằng|là)", "replacement": "người ấy/ông ấy/bà ấy", "severity": "MINOR", "note": "Wrong pronoun (Rule 24)"},
]


def check_vnch_rules(text: str) -> list:
    """Kiểm tra tất cả 30 quy tắc VNCH."""
    issues = []
    
    for rule in VNCH_RULES:
        pattern = re.compile(rule["pattern"], re.IGNORECASE)
        matches = list(pattern.finditer(text))
        
        for match in matches:
            # Check exceptions
            skip = False
            if "exceptions" in rule:
                context = text[max(0, match.start()-50):match.end()+50].lower()
                for exc in rule["exceptions"]:
                    if exc.lower() in context:
                        skip = True
                        break
            
            if skip:
                continue
            
            # Get context
            start = max(0, match.start() - 80)
            end = min(len(text), match.end() + 80)
            context = text[start:end].strip()
            
            # For colonial names, check if VNCH equivalent in parentheses
            if rule["category"] == "colonial":
                context_lower = context.lower()
                vnch_forms = {
                    "annam": "trung kỳ",
                    "tonkin": "bắc kỳ",
                    "cochinchina": "nam kỳ",
                    "cochinchine": "nam kỳ",
                    "indochine": "đông dương",
                    "indochina": "đông dương",
                }
                term_lower = match.group().lower()
                if term_lower in vnch_forms:
                    vnch_form = vnch_forms[term_lower]
                    if vnch_form in context_lower and "(" in context:
                        # VNCH equivalent in parentheses nearby - OK
                        continue
            
            issues.append({
                "rule_id": rule["id"],
                "category": rule["category"],
                "severity": rule["severity"],
                "found": match.group(),
                "expected": rule["replacement"],
                "position": match.start(),
                "context": context[:200],
                "note": rule.get("note", "")
            })
    
    return issues


def fix_vnch_rules(text: str) -> tuple:
    """Tự động sửa lỗi VNCH. Trả về (fixed_text, fix_count)."""
    fixed_text = text
    fix_count = 0
    
    # Process rules in order of specificity (longer patterns first)
    for rule in VNCH_RULES:
        pattern = re.compile(rule["pattern"], re.IGNORECASE)
        matches = list(pattern.finditer(fixed_text))
        
        # Process from end to start to maintain positions
        for match in reversed(matches):
            # Check exceptions
            skip = False
            if "exceptions" in rule:
                context = fixed_text[max(0, match.start()-50):match.end()+50].lower()
                for exc in rule["exceptions"]:
                    if exc.lower() in context:
                        skip = True
                        break
            
            if skip:
                continue
            
            # For colonial names, check if VNCH equivalent already in parentheses
            if rule["category"] == "colonial":
                context = fixed_text[max(0, match.start()-100):match.end()+100].lower()
                vnch_forms = {
                    "annam": "trung kỳ",
                    "tonkin": "bắc kỳ",
                    "cochinchina": "nam kỳ",
                    "cochinchine": "nam kỳ",
                    "indochine": "đông dương",
                    "indochina": "đông dương",
                }
                term_lower = match.group().lower()
                if term_lower in vnch_forms:
                    vnch_form = vnch_forms[term_lower]
                    if vnch_form in context and "(" in context:
                        continue
            
            # Apply fix
            found = match.group()
            expected = rule["replacement"]
            
            # Preserve case for the replacement
            if found.isupper():
                expected = expected.upper()
            elif found[0].isupper():
                expected = expected[0].upper() + expected[1:]
            
            fixed_text = fixed_text[:match.start()] + expected + fixed_text[match.end():]
            fix_count += 1
    
    return fixed_text, fix_count


def main():
    parser = argparse.ArgumentParser(description="VNCH Orthography Checker (30 rules)")
    parser.add_argument("--chapter", type=int, help="Chapter number")
    parser.add_argument("--volume", default="v1", help="Volume")
    parser.add_argument("--file", help="Specific file to check")
    parser.add_argument("--root", default=None, help="Project root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--fix", action="store_true", help="Auto-fix VNCH terminology")
    
    args = parser.parse_args()
    root = Path(args.root) if args.root else find_root()
    
    if args.file:
        file_path = Path(args.file)
    else:
        ch_dir = root / "translation-project-arendt" / "04_translation" / args.volume.lower() / f"ch{args.chapter:02d}"
        file_path = ch_dir / f"{args.volume.lower()}_ch{args.chapter:02d}_vi.txt"
    
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if args.fix:
        # Auto-fix mode
        fixed_text, fix_count = fix_vnch_rules(text)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(fixed_text)
        
        # Check remaining issues
        issues = check_vnch_rules(fixed_text)
        by_severity = {"CRITICAL": [], "MAJOR": [], "MINOR": []}
        for issue in issues:
            by_severity[issue["severity"]].append(issue)
        
        result = {
            "file": str(file_path),
            "fixed_count": fix_count,
            "remaining_issues": len(issues),
            "by_severity": {k: len(v) for k, v in by_severity.items()},
            "issues": issues
        }
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"VNCH Orthography Fix: {file_path.name}")
            print(f"  Fixed: {fix_count}")
            print(f"  Remaining issues: {len(issues)}")
            print(f"  CRITICAL: {len(by_severity['CRITICAL'])}")
            print(f"  MAJOR: {len(by_severity['MAJOR'])}")
            print(f"  MINOR: {len(by_severity['MINOR'])}")
    else:
        # Check only mode
        issues = check_vnch_rules(text)
        
        # Group by severity
        by_severity = {"CRITICAL": [], "MAJOR": [], "MINOR": []}
        for issue in issues:
            by_severity[issue["severity"]].append(issue)
        
        result = {
            "file": str(file_path),
            "total_issues": len(issues),
            "by_severity": {k: len(v) for k, v in by_severity.items()},
            "issues": issues
        }
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"VNCH Orthography Check: {file_path.name}")
            print(f"  Total issues: {len(issues)}")
            print(f"  CRITICAL: {len(by_severity['CRITICAL'])}")
            print(f"  MAJOR: {len(by_severity['MAJOR'])}")
            print(f"  MINOR: {len(by_severity['MINOR'])}")
            
            if issues:
                print("\nDetails (first 30):")
                for issue in issues[:30]:
                    print(f"  [{issue['severity']}] {issue['rule_id']}: '{issue['found']}' -> '{issue['expected']}'")
                    print(f"    Context: ...{issue['context'][:100]}...")
    
    sys.exit(0 if len(issues) == 0 else 1)


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project-arendt").is_dir():
            return parent
    return Path.cwd()


if __name__ == "__main__":
    main()