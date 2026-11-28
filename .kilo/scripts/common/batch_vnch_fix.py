#!/usr/bin/env python3
"""
Safe VNCH batch fix: Apply CRITICAL rules to all occurrences (case-insensitive).
"""

import re
from pathlib import Path

# CRITICAL VNCH rules (safe to auto-apply) - case insensitive
CRITICAL_RULES = [
    # Core political terms
    {"id": "VNCH-01", "pattern": r"(?i)\bchính trị\b", "replacement": "chánh trị"},
    {"id": "VNCH-02", "pattern": r"(?i)\bchính phủ\b", "replacement": "chánh phủ"},
    {"id": "VNCH-03", "pattern": r"(?i)\bchính đảng\b", "replacement": "chánh đảng"},
    {"id": "VNCH-04", "pattern": r"(?i)\bđảo chính\b", "replacement": "đảo chánh"},
    {"id": "VNCH-05", "pattern": r"(?i)\btài chính\b", "replacement": "tài chánh"},
    {"id": "VNCH-06", "pattern": r"(?i)\blương hưu\b", "replacement": "hưu bổng"},
    {"id": "VNCH-07", "pattern": r"(?i)\bbất động sản\b", "replacement": "địa ốc"},
    {"id": "VNCH-08", "pattern": r"(?i)\bđại biểu\b", "replacement": "dân biểu"},
    {"id": "VNCH-09", "pattern": r"(?i)\bngân sách\b(?=\s*(?:cơ quan|ngân khố|ngân hàng))", "replacement": "ngân khố"},
    
    # Bắc/Nam terms - CRITICAL
    {"id": "VNCH-12", "pattern": r"(?i)\bnày\b(?!.*(?:trong|ngoài|trước|sau)\s+nầy)", "replacement": "nầy"},
    
    # Colonial names
    {"id": "VNCH-21", "pattern": r"\bAnnam\b", "replacement": "Trung Kỳ (Annam)"},
    {"id": "VNCH-22", "pattern": r"\bTonkin\b", "replacement": "Bắc Kỳ (Tonkin)"},
    {"id": "VNCH-23", "pattern": r"\bCochinchina\b", "replacement": "Nam Kỳ (Cochinchina)"},
]

# MAJOR VNCH rules (need review, apply with --major flag)
MAJOR_RULES = [
    {"id": "VNCH-10", "pattern": r"(?i)\bgiải phóng\b", "replacement": "độc lập/kháng cự", "exceptions": ["cờ giải phóng", "quân giải phóng", "mặt trận giải phóng"]},
    {"id": "VNCH-11", "pattern": r"(?i)\bđồng chí\b", "replacement": "đồng đạo", "exceptions": ["thanh niên cách mạng đồng chí hội", "đồng chí hội"]},
    {"id": "VNCH-13", "pattern": r"(?i)\bmặc dù\b", "replacement": "dầu/dẫu"},
    {"id": "VNCH-14", "pattern": r"(?i)\btuy nhiên\b", "replacement": "tuy vậy/đã vậy"},
    {"id": "VNCH-15", "pattern": r"(?i)\bvì vậy\b", "replacement": "bởi thế/do đó"},
    {"id": "VNCH-16", "pattern": r"(?i)\bhơn nữa\b", "replacement": "vả/lại"},
    {"id": "VNCH-17", "pattern": r"(?i)\bngược lại\b", "replacement": "trái lại"},
    {"id": "VNCH-18", "pattern": r"(?i)\bmà không\b", "replacement": "chớ không"},
    {"id": "VNCH-19", "pattern": r"(?i)\bmà chẳng\b", "replacement": "chớ chẳng"},
    {"id": "VNCH-20", "pattern": r"(?i)\bmà đâu\b", "replacement": "chớ đâu"},
]

def apply_rules_all(text: str, rules: list):
    """Apply replacement rules to ALL occurrences."""
    changes = []
    result = text
    
    for rule in rules:
        pattern = rule["pattern"]
        replacement = rule["replacement"]
        rule_id = rule["id"]
        
        # Find all matches and replace
        matches = list(re.finditer(pattern, result))
        if not matches:
            continue
        
        # Apply from end to start to preserve positions
        for match in reversed(matches):
            start, end = match.span()
            # Preserve case for first letter if original was capitalized
            original = match.group()
            if original[0].isupper():
                replacement_adj = replacement[0].upper() + replacement[1:]
            else:
                replacement_adj = replacement
            result = result[:start] + replacement_adj + result[end:]
            changes.append({
                "rule_id": rule_id,
                "original": original,
                "replacement": replacement_adj,
                "position": start
            })
    
    return result, changes

def fix_chapter(chapter: int, volume: str = "v2", apply_major: bool = False):
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    file_path = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_realigned.txt"
    
    text = file_path.read_text(encoding='utf-8')
    
    # Apply CRITICAL rules
    fixed_text, critical_changes = apply_rules_all(text, CRITICAL_RULES)
    
    # Apply MAJOR rules if requested
    major_changes = []
    if apply_major:
        fixed_text, major_changes = apply_rules_all(fixed_text, MAJOR_RULES)
    
    all_changes = critical_changes + major_changes
    
    # Save fixed version
    fixed_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_fixed.txt"
    fixed_file.write_text(fixed_text, encoding='utf-8')
    
    # Count by rule
    by_rule = {}
    for c in all_changes:
        by_rule[c['rule_id']] = by_rule.get(c['rule_id'], 0) + 1
    
    print(f"Chapter {chapter}: CRITICAL={len(critical_changes)}, MAJOR={len(major_changes)} - {by_rule}")
    
    return len(critical_changes), len(major_changes)

if __name__ == "__main__":
    import sys
    apply_major = "--major" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--major"]
    
    if args:
        chapter = int(args[0])
        fix_chapter(chapter, apply_major=apply_major)
    else:
        total_critical = 0
        total_major = 0
        for ch in range(1, 14):
            c, m = fix_chapter(ch, apply_major=apply_major)
            total_critical += c
            total_major += m
        print(f"\nTotal: CRITICAL={total_critical}, MAJOR={total_major}")