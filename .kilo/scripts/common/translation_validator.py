#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common Script: Translation Validator
Quét từ tiếng Anh còn sót, thuật ngữ dịch không nhất quán, nội dung rỗng/bất thường.
Dùng chung cho translation-error-detection, translation-quality-gate.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from collections import Counter


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project").is_dir():
            return parent
    return Path.cwd()


def load_lexicon(lexicon_path: Path) -> dict:
    """Load MASTER_LEXICON.csv into dict for term checking."""
    terms = {}
    try:
        import csv
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                term = row.get('tu_chuan', '').strip()
                if term:
                    terms[term.lower()] = row
    except Exception as e:
        print(f"WARN: Could not load lexicon: {e}", file=sys.stderr)
    return terms


# Từ khóa VNCH sai thường gặp (từ audit 6 chương)
VNCH_TERM_MAPPING = {
    # Core political terms
    'chính trị': 'chánh trị',
    'chính phủ': 'chánh phủ',
    'chính đảng': 'chánh đảng',
    'đảo chính': 'đảo chánh',
    'tài chính': 'tài chánh',
    'lương hưu': 'hưu bổng',
    'bất động sản': 'địa ốc',
    'đại biểu': 'dân biểu',
    'ngân sách': 'ngân khố',  # when referring to agency
    
    # Bắc/Nam terms
    'giải phóng': 'độc lập/kháng cự',
    'đồng chí': 'đồng đạo',
    'này': 'nầy',
    'mặc dù': 'dầu/dẫu',
    'tuy nhiên': 'tuy vậy/đã vậy',
    'vì vậy': 'bởi thế/do đó',
    'hơn nữa': 'vả/lại',
    'ngược lại': 'trái lại',
    
    # Colonial names (Rule 15)
    'annam': 'Trung Kỳ (Annam)',
    'tonkin': 'Bắc Kỳ (Tonkin)',
    'cochinchina': 'Nam Kỳ (Cochinchina)',
    'cochinchine': 'Nam Kỳ (Cochinchine)',
    'indochine': 'Đông Dương (Indochine)',
    'indochina': 'Đông Dương (Indochine)',
    
    # English terms often left untranslated (from audit)
    'nation': 'quốc gia/dân tộc',
    'pays': 'khu vực',
    'supposedly transient': 'người tạm trú',
    'staffing': 'bổ nhiệm nhân sự',
    'greatly': 'mạnh mẽ',
    'severely': 'rất',
    'staging': 'tổ chức/biểu diễn',
    'meant to be': 'dự định là',
    'agitation': 'xuyên tạc/khuyến khích',
    'coolie': 'lao công thuê',
    'trump mere patriotism': 'đè bẹp lòng yêu nước thuần túy',
    'voie royale': 'con đường vương giả',
    'five dragons': 'Ngũ Long',
    'front populaire': 'Mặt trận Phổ thông',
    'grafting': 'ghép cắm',
    'teleology': 'xác định trước',
    'ultima avis': 'thông báo cuối cùng',
    'glass ceiling': 'trần kính',
    'allegory': 'ẩn dụ',
    'brinkmanship': 'đe dọa hạt nhân',
    'en même temps': 'cùng lúc',
    'en route': 'đang trên đường',
    'gouvernement de fait': 'chánh phủ thực tế',
    'essentialism': 'bản chất chủ nghĩa',
    'fascism': 'fa-xít',
    'autarky': 'tự cung tự túc',
    'ersatz': 'vật thay thế',
    'phalanx': 'đoàn người',
    'exacted a dreadful toll': 'gặt hái cái giá khủng khiếp',
    'improvisation': 'sự ứng biến',
    'deus ex machina': 'thần cơ vả vỡ',
    'modus vivendi': 'thỏa thuận sống cùng nhau',
    'enclave': 'miền lãnh thổ tách biệt',
    'tonkinois': 'người Bắc Kỳ',
}


def check_english_remaining(text: str) -> list:
    """Quét từ tiếng Anh còn sót trong bản dịch."""
    issues = []
    
    # Pattern: English words in Vietnamese text (simple heuristic)
    # Look for words that are clearly English and not proper names
    english_pattern = re.compile(r'\b[a-zA-Z]{3,}\b')
    
    # Known Vietnamese words that might match (exclude)
    vietnamese_common = {
        'và', 'của', 'trong', 'người', 'năm', 'tháng', 'ngày', 'là', 'có', 'được',
        'cho', 'với', 'tại', 'từ', 'đến', 'về', 'như', 'khi', 'nếu', 'thì',
        'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười',
        'các', 'những', 'mọi', 'toàn', 'quốc', 'gia', 'dân', 'tộc', 'nước',
        'chánh', 'trị', 'phủ', 'đảng', 'đảo', 'tài', 'chánh', 'lương', 'hưu',
        'bất', 'động', 'sản', 'địa', 'ốc', 'ngân', 'khố', 'sách', 'học', 'văn',
        'hóa', 'lịch', 'sử', 'chiến', 'tranh', 'cách', 'mạng', 'độc', 'lập',
        'kháng', 'cự', 'bình', 'dân', 'cộng', 'hòa', 'quân', 'sự', 'vụ', 'việc',
        'người', 'ta', 'họ', 'này', 'nầy', 'đó', 'kia', 'trước', 'sau', 'ngoài',
        'trong', 'ngoài', 'trên', 'dưới', 'bên', 'giữa', 'gần', 'xa', 'lớn', 'nhỏ'
    }
    
    words = english_pattern.findall(text)
    for word in words:
        lower = word.lower()
        if lower not in vietnamese_common and lower not in VNCH_TERM_MAPPING:
            # Check if it looks like English (has common English patterns)
            if re.search(r'(tion|ing|ment|ness|able|ible|ous|ive|ful|less|ly|ed)$', lower):
                issues.append({
                    "type": "english_remaining",
                    "word": word,
                    "context": "English suffix detected"
                })
    
    return issues


def check_vnch_terminology(text: str, lexicon: dict) -> list:
    """Kiểm tra thuật ngữ VNCH sai."""
    issues = []
    text_lower = text.lower()
    
    for wrong, correct in VNCH_TERM_MAPPING.items():
        # Skip if it's in a citation context (has parentheses with original)
        pattern = re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE)
        matches = list(pattern.finditer(text))
        
        for match in matches:
            # Get context around match
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context = text[start:end]
            
            # Check if it's in a citation (has original in parentheses nearby)
            in_citation = False
            if '(' in context and ')' in context:
                # Check if the original term is in parentheses
                if wrong.lower() in context and ('(' in context[context.lower().find(wrong.lower()):]):
                    in_citation = True
            
            # Also check for false positives in book titles, org names
            false_positive_contexts = [
                'tên sách', 'tựa sách', 'trích dẫn', 'nguyên tác', 'nguồn',
                'bibliography', 'references', 'citation', 'quoted'
            ]
            is_false_positive = any(fp in context.lower() for fp in false_positive_contexts)
            
            if not in_citation and not is_false_positive:
                issues.append({
                    "type": "vnch_terminology",
                    "wrong": wrong,
                    "correct": correct,
                    "position": match.start(),
                    "context": context[:200]
                })
    
    return issues


def check_paragraph_consistency(src_path: Path, vi_path: Path) -> list:
    """Kiểm tra nhất quán số đoạn, số câu giữa src và vi."""
    issues = []
    
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            src_text = f.read()
        with open(vi_path, 'r', encoding='utf-8') as f:
            vi_text = f.read()
    except Exception as e:
        return [{"type": "file_error", "error": str(e)}]
    
    # Count paragraphs
    src_paras = re.findall(r'--- \[V\d+C\d{2}-P\d{3}\]', src_text)
    vi_paras = re.findall(r'--- \[V\d+C\d{2}-P\d{3}\]', vi_text)
    
    if len(src_paras) != len(vi_paras):
        issues.append({
            "type": "paragraph_count_mismatch",
            "src_count": len(src_paras),
            "vi_count": len(vi_paras),
            "difference": len(vi_paras) - len(src_paras)
        })
    
    # Check sentence count per paragraph (rough)
    src_sentences = re.split(r'[.!?]+', src_text)
    vi_sentences = re.split(r'[.!?]+', vi_text)
    src_sent_count = len([s for s in src_sentences if s.strip()])
    vi_sent_count = len([s for s in vi_sentences if s.strip()])
    
    if abs(src_sent_count - vi_sent_count) > max(3, src_sent_count * 0.1):
        issues.append({
            "type": "sentence_count_mismatch",
            "src_sentences": src_sent_count,
            "vi_sentences": vi_sent_count,
            "difference": vi_sent_count - src_sent_count
        })
    
    return issues


def check_empty_content(vi_path: Path) -> list:
    """Kiểm tra nội dung rỗng hoặc bất thường."""
    issues = []
    
    try:
        with open(vi_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return [{"type": "file_error", "error": str(e)}]
    
    # Check for empty paragraphs
    paras = re.split(r'--- \[V\d+C\d{2}-P\d{3}\]', text)
    for i, para in enumerate(paras[1:], 1):  # Skip header
        if not para.strip():
            issues.append({
                "type": "empty_paragraph",
                "paragraph": i
            })
        # Check for very short content (might be incomplete)
        elif len(para.strip()) < 20 and '— đề mục' not in para:
            issues.append({
                "type": "very_short_paragraph",
                "paragraph": i,
                "length": len(para.strip()),
                "content": para.strip()[:100]
            })
    
    # Check for untranslated English sentences (long sequences)
    english_sentences = re.findall(r'[A-Z][a-zA-Z\s,]{20,}[.!?]', text)
    for sent in english_sentences:
        if len(sent) > 50:
            issues.append({
                "type": "long_english_sequence",
                "content": sent[:200]
            })
    
    return issues


def main():
    parser = argparse.ArgumentParser(description="Translation Validator")
    parser.add_argument("--chapter", type=int, required=True, help="Chapter number")
    parser.add_argument("--volume", default="v1", help="Volume")
    parser.add_argument("--root", default=None, help="Project root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--lexicon", default=None, help="Path to MASTER_LEXICON.csv")
    
    args = parser.parse_args()
    root = Path(args.root) if args.root else find_root()
    
    ch_dir = root / "translation-project" / "04_translation" / args.volume.lower() / f"ch{args.chapter:02d}"
    vi_file = ch_dir / f"{args.volume.lower()}_ch{args.chapter:02d}_vi.txt"
    src_file = ch_dir / f"{args.volume.lower()}_ch{args.chapter:02d}_src.txt"
    
    if not vi_file.exists():
        print(f"ERROR: VI file not found: {vi_file}", file=sys.stderr)
        sys.exit(1)
    if not src_file.exists():
        print(f"ERROR: SRC file not found: {src_file}", file=sys.stderr)
        sys.exit(1)
    
    # Load lexicon
    lexicon_path = Path(args.lexicon) if args.lexicon else root / "translation-project" / "08_southern_vietnamese_library" / "10_LEXICAL_DATABASE" / "MASTER_LEXICON.csv"
    lexicon = load_lexicon(lexicon_path)
    
    # Read files
    with open(vi_file, 'r', encoding='utf-8') as f:
        vi_text = f.read()
    with open(src_file, 'r', encoding='utf-8') as f:
        src_text = f.read()
    
    all_issues = []
    
    # Run checks
    all_issues.extend(check_english_remaining(vi_text))
    all_issues.extend(check_vnch_terminology(vi_text, lexicon))
    all_issues.extend(check_paragraph_consistency(src_file, vi_file))
    all_issues.extend(check_empty_content(vi_file))
    
    # Summary
    result = {
        "chapter": args.chapter,
        "volume": args.volume,
        "total_issues": len(all_issues),
        "issues_by_type": {},
        "issues": all_issues
    }
    
    for issue in all_issues:
        itype = issue.get("type", "unknown")
        if itype not in result["issues_by_type"]:
            result["issues_by_type"][itype] = 0
        result["issues_by_type"][itype] += 1
    
    # Output
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Chapter {args.chapter} Validation Results:")
        print(f"  Total issues: {len(all_issues)}")
        for itype, count in result["issues_by_type"].items():
            print(f"  {itype}: {count}")
        if all_issues and not args.json:
            print("\nDetails:")
            for issue in all_issues[:20]:  # Limit output
                print(f"  - {issue}")
    
    sys.exit(0 if len(all_issues) == 0 else 1)


if __name__ == "__main__":
    main()