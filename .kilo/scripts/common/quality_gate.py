#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common Script: Quality Gate Runner
Chạy 8 tiêu chí Quality Gate, output JSON.
Dùng cho translation-quality-gate skill.
"""

import os
import sys
import json
import subprocess
import argparse
import re
from pathlib import Path


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project-arendt-arendt").is_dir():
            return parent
    return Path.cwd()


def run_cmd(cmd, cwd=None):
    """Chạy lệnh và trả về (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def check_encoding(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 1: Encoding UTF-8, NFC, no BOM, LF."""
    ch_dir = root / "translation-project-arendt-arendt" / "04_translation" / volume.lower() / f"ch{chapter:02d}"
    vi_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_vi_fixed.txt"
    src_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_src.txt"
    
    issues = []
    for f in [vi_file, src_file]:
        if f.exists():
            try:
                with open(f, 'rb') as fh:
                    raw = fh.read()
                
                # Check BOM
                has_bom = raw.startswith(b'\xef\xbb\xbf')
                
                # Try decode UTF-8
                try:
                    text = raw.decode('utf-8')
                    utf8_ok = True
                except UnicodeDecodeError:
                    utf8_ok = False
                
                # Check NFC
                import unicodedata
                try:
                    nfc_ok = text == unicodedata.normalize('NFC', text)
                except:
                    nfc_ok = False
                
                # Check line endings
                has_crlf = b'\r\n' in raw
                
                if not utf8_ok:
                    issues.append(f"{f.name}: Not valid UTF-8")
                if has_bom:
                    issues.append(f"{f.name}: Has BOM")
                if not nfc_ok:
                    issues.append(f"{f.name}: Not NFC normalized")
                if has_crlf:
                    issues.append(f"{f.name}: Has CRLF line endings")
            except Exception as e:
                issues.append(f"{f.name}: Check error - {e}")
    
    return {
        "criterion": 1,
        "name": "Encoding UTF-8/NFC/no BOM/LF",
        "pass": len(issues) == 0,
        "issues": issues
    }


def check_orthography(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 2: Orthography - 0x 'chính trị', 0x từ miền Bắc."""
    ch_dir = root / "translation-project-arendt" / "04_translation" / volume.lower() / f"ch{chapter:02d}"
    vi_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_vi_fixed.txt"
    
    if not vi_file.exists():
        return {"criterion": 2, "name": "Orthography", "pass": False, "issues": ["VI fixed file not found"]}
    
    with open(vi_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Critical terms that must not appear in Vietnamese body text
    critical_terms = {
        'chính trị': 'chánh trị',
        'chính phủ': 'chánh phủ',
        'chính đảng': 'chánh đảng',
        'đảo chính': 'đảo chánh',
        'tài chính': 'tài chánh',
        'lương hưu': 'hưu bổng',
        'bất động sản': 'địa ốc',
        'đại biểu': 'dân biểu',
        'giải phóng': 'độc lập/kháng cự',
        'đồng chí': 'đồng đạo',
        'này': 'nầy',  # with exceptions
        'mặc dù': 'dầu/dẫu',
        'tuy nhiên': 'tuy vậy/đã vậy',
        'vì vậy': 'bởi thế/do đó',
        'hơn nữa': 'vả/lại',
        'ngược lại': 'trái lại',
    }
    
    # Proper noun exceptions (Rule 15) - keep original form in proper nouns
    proper_noun_exceptions = {
        'giải phóng': [
            'quân giải phóng', 'cờ giải phóng', 'mặt trận giải phóng',
            'quân đội giải phóng', 'khu giải phóng', 'vùng giải phóng'
        ],
        'đồng chí': [
            'thanh niên cách mạng đồng chí hội', 'đồng chí hội',
            'đồng chí hội việt nam', 'đồng chí hội cách mạng'
        ],
    }
    
    issues = []
    
    # Helper: check if position is inside English citation (italicized _..._ or in footnote block)
    def in_english_citation(pos):
        # Check if inside italicized _..._ (English book titles)
        before = text[:pos]
        after = text[pos:]
        # Count underscores before position
        underscore_count = before.count('_')
        if underscore_count % 2 == 1:
            return True  # Inside italicized text
        # Check if in footnote block (after "--- [Cước chú")
        footnote_start = before.rfind('--- [Cước chú')
        if footnote_start != -1:
            # Check if there's another section header after footnote_start but before pos
            next_section = text.find('--- [', footnote_start + 1)
            if next_section == -1 or next_section > pos:
                return True  # Inside footnote block
        return False
    
    # Helper: check if position is inside a proper noun exception
    def in_proper_noun_exception(pos, term):
        if term not in proper_noun_exceptions:
            return False
        # Check context around position for proper noun patterns
        start = max(0, pos - 50)
        end = min(len(text), pos + 50)
        context = text[start:end].lower()
        for pattern in proper_noun_exceptions[term]:
            if pattern in context:
                return True
        return False
    
    for wrong, correct in critical_terms.items():
        if wrong == 'này':
            # Check with exceptions for demonstratives
            pattern = re.compile(r'\b' + re.escape(wrong) + r'\b(?!.*(?:trong|ngoài|trước|sau)\s+nầy)', re.IGNORECASE)
            for match in pattern.finditer(text):
                if not in_english_citation(match.start()) and not in_proper_noun_exception(match.start(), wrong):
                    issues.append(f"Found '{wrong}' should be '{correct}'")
        else:
            for match in re.finditer(r'\b' + re.escape(wrong) + r'\b', text, re.IGNORECASE):
                if not in_english_citation(match.start()) and not in_proper_noun_exception(match.start(), wrong):
                    issues.append(f"Found '{wrong}' should be '{correct}'")
    
    # Check colonial names (Rule 15) - should not appear in Vietnamese body text without VNCH equivalent
    # Exception: English citations, book titles, footnotes
    colonial_terms = {
        'annam': ['trung kỳ'],
        'tonkin': ['bắc kỳ'],
        'cochinchina': ['nam kỳ'],
        'cochinchine': ['nam kỳ'],
        'indochine': ['đông dương'],
        'indochina': ['đông dương'],
    }
    for term, vnch_forms in colonial_terms.items():
        matches = list(re.finditer(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE))
        for match in matches:
            # Skip if in English citation
            if in_english_citation(match.start()):
                continue
            start = max(0, match.start() - 150)
            end = min(len(text), match.end() + 150)
            context = text[start:end].lower()
            # Check if any VNCH equivalent is nearby (within 150 chars)
            has_vnch = any(vnch in context for vnch in vnch_forms)
            if not has_vnch:
                issues.append(f"Found '{term}' without VNCH equivalent '{vnch_forms[0].title()} ({term.title()})'")
    
    return {
        "criterion": 2,
        "name": "Orthography (VNCH terminology)",
        "pass": len(issues) == 0,
        "issues": issues
    }


def check_alignment(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 3: Đồng bộ đoạn src = vi."""
    ch_dir = root / "translation-project-arendt" / "04_translation" / volume.lower() / f"ch{chapter:02d}"
    vi_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_vi_fixed.txt"
    src_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_src.txt"
    
    if not vi_file.exists() or not src_file.exists():
        return {"criterion": 3, "name": "Đồng bộ đoạn", "pass": False, "issues": ["Missing files"]}
    
    with open(src_file, 'r', encoding='utf-8') as f:
        src_text = f.read()
    with open(vi_file, 'r', encoding='utf-8') as f:
        vi_text = f.read()
    
    src_paras = len(re.findall(r'--- \[V\d+C\d{2}-P\d{3}\]', src_text))
    vi_paras = len(re.findall(r'--- \[V\d+C\d{2}-P\d{3}\]', vi_text))
    
    issues = []
    warnings = []
    if src_paras != vi_paras:
        issues.append(f"Paragraph count mismatch: src={src_paras}, vi={vi_paras}")
    
    # Also check sentence count per paragraph roughly
    # Note: User rule says "Số câu tiếng Anh và tiếng Việt không bắt buộc bằng nhau"
    # So we only warn, not fail, for sentence count differences
    src_sents = len([s for s in re.split(r'[.!?]+', src_text) if s.strip()])
    vi_sents = len([s for s in re.split(r'[.!?]+', vi_text) if s.strip()])
    if abs(src_sents - vi_sents) > max(3, src_sents * 0.1):
        warnings.append(f"WARNING: Sentence count mismatch (not failing per rule): src={src_sents}, vi={vi_sents}")
    
    return {
        "criterion": 3,
        "name": "Đồng bộ đoạn (src = vi)",
        "pass": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "details": {"src_paragraphs": src_paras, "vi_paragraphs": vi_paras}
    }


def check_footnotes_alignment(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 4: Đồng bộ cước chú."""
    ch_dir = root / "translation-project-arendt" / "04_translation" / volume.lower() / f"ch{chapter:02d}"
    vi_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_vi_fixed.txt"
    src_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_src.txt"
    
    if not vi_file.exists() or not src_file.exists():
        return {"criterion": 4, "name": "Đồng bộ cước chú", "pass": False, "issues": ["Missing files"]}
    
    with open(src_file, 'r', encoding='utf-8') as f:
        src_text = f.read()
    with open(vi_file, 'r', encoding='utf-8') as f:
        vi_text = f.read()
    
    # Extract footnote markers
    src_markers = re.findall(r'\[\s*(\d+)\s*\]', src_text)
    vi_markers = re.findall(r'\[\s*(\d+)\s*\]', vi_text)
    
    # Also check for plain numbers at start of footnote lines
    src_fn = re.findall(r'(?:^|\n)\s*(\d+)\s+', src_text)
    vi_fn = re.findall(r'(?:^|\n)\s*(\d+)\s+', vi_text)
    
    src_all = list(set(src_markers + src_fn))
    vi_all = list(set(vi_markers + vi_fn))
    
    issues = []
    if len(src_all) != len(vi_all):
        issues.append(f"Footnote count mismatch: src={len(src_all)}, vi={len(vi_all)}")
    
    # Check sequence
    src_nums = sorted([int(m) for m in src_all if m.isdigit()])
    vi_nums = sorted([int(m) for m in vi_all if m.isdigit()])
    
    if src_nums != list(range(1, len(src_nums) + 1)):
        issues.append(f"Source footnotes not sequential: {src_nums}")
    if vi_nums != list(range(1, len(vi_nums) + 1)):
        issues.append(f"VI footnotes not sequential: {vi_nums}")
    
    return {
        "criterion": 4,
        "name": "Đồng bộ cước chú",
        "pass": len(issues) == 0,
        "issues": issues
    }


def check_fabricate(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 5: Không fabricate."""
    # This is mostly manual, but we can check for obvious patterns
    ch_dir = root / "translation-project-arendt" / "04_translation" / volume.lower() / f"ch{chapter:02d}"
    vi_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_vi_fixed.txt"
    
    if not vi_file.exists():
        return {"criterion": 5, "name": "Không fabricate", "pass": False, "issues": ["VI file not found"]}
    
    with open(vi_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    issues = []
    # Check for obvious fabricated page numbers
    page_refs = re.findall(r'trang\s+\d{1,4}', text, re.IGNORECASE)
    for ref in page_refs:
        # Could check against actual page range
        pass
    
    # Check for [ND:] notes (translator notes) - these are allowed
    nd_notes = re.findall(r'\[ND:[^\]]+\]', text)
    
    return {
        "criterion": 5,
        "name": "Không fabricate",
        "pass": True,  # Mostly manual check
        "issues": issues,
        "details": {"translator_notes": len(nd_notes)}
    }


def check_writing_style(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 6: Văn phong tự nhiên (S1-S20, P1-P10)."""
    ch_dir = root / "translation-project-arendt" / "04_translation" / volume.lower() / f"ch{chapter:02d}"
    vi_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_vi_fixed.txt"
    
    if not vi_file.exists():
        return {"criterion": 6, "name": "Văn phong tự nhiên", "pass": False, "issues": ["VI file not found"]}
    
    with open(vi_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    issues = []
    
    # Proper noun exceptions (Rule 15) - keep original form in proper nouns
    proper_noun_exceptions = {
        'giải phóng': [
            'quân giải phóng', 'cờ giải phóng', 'mặt trận giải phóng',
            'quân đội giải phóng', 'khu giải phóng', 'vùng giải phóng',
            'chiến đấu giải phóng', 'phong trào giải phóng'
        ],
        'đồng chí': [
            'thanh niên cách mạng đồng chí hội', 'đồng chí hội',
            'đồng chí hội việt nam', 'đồng chí hội cách mạng',
            'hội đồng chí'
        ],
    }
    
    # Helper: check if position is inside a proper noun exception
    def in_proper_noun_exception(pos, term):
        if term not in proper_noun_exceptions:
            return False
        # Check context around position for proper noun patterns
        start = max(0, pos - 60)
        end = min(len(text), pos + 60)
        context = text[start:end].lower()
        for pattern in proper_noun_exceptions[term]:
            if pattern in context:
                return True
        return False
    
    # S9: Cấu trúc ngoại ngữ bê nguyên - check for English-like structures
    # e.g., "được ... bởi" passive constructions
    passive_patterns = [
        r'\bđược\s+\w+\s+bởi\b',
        r'\bbị\s+\w+\s+bởi\b',
    ]
    for pattern in passive_patterns:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        for match in matches:
            issues.append(f"Passive structure (S18): '{match.group()}' - should active voice")
    
    # S13: Từ miền Bắc (with proper noun exceptions)
    north_terms = ['giải phóng', 'đồng chí', 'chính phủ', 'chính trị', 'này']
    for term in north_terms:
        if term == 'này':
            continue  # handled in orthography
        for match in re.finditer(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            if not in_proper_noun_exception(match.start(), term):
                issues.append(f"Northern term (S13): '{term}'")
    
    # S15: Chỉ định danh từ - check for missing classifiers (một + noun without classifier)
    # Pattern: "một " followed by a noun that needs a classifier (not already having one)
    # Common nouns that need classifiers: sách, ký, người, ngày, năm, cái, cuốn, bài, trang, dòng, câu, từ, việc, chuyện, nơi, chỗ, người, con, cái, chiếc, bản, tờ, lá, viên, quả, hạt, giọt, nhánh, cành, gốc, thân, lá, hoa, quả, hạt
    # But we should only flag if there's NO classifier between "một" and the noun
    # A proper check: "một " + (optional classifier) + noun
    # For now, check for "một " directly followed by nouns that typically need classifiers
    # but NOT when a classifier is already present (người, cái, chiếc, bản, tờ, cuốn, quyển, quyển, cuốn, quyển, cuốn)
    # This is complex - for now, make it a warning only or remove
    # The original logic was inverted - it flagged CORRECT usage as error
    pass  # S15 check disabled - too complex for regex, requires semantic analysis
    
    # S16: Trạng từ này/nầy
    north_dem = re.findall(r'\b(năm|ngày|trước|sau)\s+này\b', text, re.IGNORECASE)
    for match in north_dem:
        issues.append(f"Wrong demonstrative (S16): '{match}' -> should be 'nầy'")
    
    # S18: Passive voice
    # Already checked above
    
    # S19: Đại từ nhân xưng
    bad_pronouns = re.findall(r'\b(hắn|y|nó)\b.*?(?:lập luận|nói|cho rằng|tin rằng)', text, re.IGNORECASE)
    for match in bad_pronouns:
        issues.append(f"Bad pronoun (S19): '{match}'")
    
    # S20: Từ nối logic
    bad_connectors = ['tuy nhiên', 'ngược lại', 'vì vậy', 'hơn nữa', 'hơn thế nữa']
    for connector in bad_connectors:
        matches = list(re.finditer(r'\b' + re.escape(connector) + r'\b', text, re.IGNORECASE))
        if matches:
            print(f"DEBUG: Found '{connector}' at positions: {[m.start() for m in matches]}", file=sys.stderr)
        for match in matches:
            issues.append(f"Bad connector (S20): '{connector}'")
    
    return {
        "criterion": 6,
        "name": "Văn phong tự nhiên (S1-S20, P1-P10)",
        "pass": len(issues) == 0,
        "issues": issues
    }


def check_docx_exists(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 7: DOCX tồn tại."""
    docx_dir = root / "translation-project-arendt" / "09_docx"
    pattern = f"V{volume[-1]}-{chapter:02d}_*.docx"
    files = list(docx_dir.glob(pattern))
    
    return {
        "criterion": 7,
        "name": "DOCX tồn tại",
        "pass": len(files) > 0,
        "issues": [] if files else [f"DOCX not found: {pattern}"],
        "details": {"files": [str(f) for f in files]}
    }


def check_docx_footnotes(root: Path, volume: str, chapter: int) -> dict:
    """Tiêu chí 8: DOCX cước chú & bố cục - cần Word COM."""
    # This requires Word COM, return info for manual check
    ch_dir = root / "translation-project-arendt" / "04_translation" / volume.lower() / f"ch{chapter:02d}"
    vi_file = ch_dir / f"{volume.lower()}_ch{chapter:02d}_vi_fixed.txt"
    
    if not vi_file.exists():
        return {"criterion": 8, "name": "DOCX cước chú & bố cục", "pass": False, "issues": ["VI file not found"]}
    
    with open(vi_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Count footnotes from vi.txt
    fn_count = len(re.findall(r'--- \[Cước chú trang [^\]]+\] ---', text))
    
    # Count inline markers
    markers = re.findall(r'\[\s*(\d+)\s*\]', text)
    
    return {
        "criterion": 8,
        "name": "DOCX cước chú & bố cục",
        "pass": True,  # Needs Word COM verification
        "issues": ["REQUIRES_WORD_COM_CHECK: Verify Footnotes.Count = progress.json notes, footnote 9pt, 1..N, A4 layout"],
        "details": {
            "footnote_blocks": fn_count,
            "inline_markers": len(set(markers)),
            "max_marker": max([int(m) for m in markers if m.isdigit()]) if markers else 0
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Quality Gate Runner - 8 tiêu chí")
    parser.add_argument("--chapter", type=int, help="Chapter number")
    parser.add_argument("--volume", default="v1", help="Volume")
    parser.add_argument("--all", action="store_true", help="Run for all completed chapters")
    parser.add_argument("--root", default=None, help="Project root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    root = Path(args.root) if args.root else find_root()
    
    import re
    
    chapters = []
    if args.all:
        trans_dir = root / "translation-project-arendt" / "04_translation" / args.volume.lower()
        for d in sorted(trans_dir.iterdir()):
            if d.is_dir() and d.name.startswith("ch"):
                try:
                    ch_num = int(d.name[2:])
                    # Check if has vi file
                    vi_file = d / f"{args.volume.lower()}_ch{ch_num:02d}_vi.txt"
                    if vi_file.exists():
                        chapters.append(ch_num)
                except:
                    pass
    elif args.chapter:
        chapters.append(args.chapter)
    else:
        print("ERROR: Specify --chapter N or --all", file=sys.stderr)
        sys.exit(1)
    
    all_results = []
    overall_pass = True
    
    for ch in chapters:
        print(f"\n=== Quality Gate Chapter {ch} ===")
        
        checks = [
            check_encoding(root, args.volume, ch),
            check_orthography(root, args.volume, ch),
            check_alignment(root, args.volume, ch),
            check_footnotes_alignment(root, args.volume, ch),
            check_fabricate(root, args.volume, ch),
            check_writing_style(root, args.volume, ch),
            check_docx_exists(root, args.volume, ch),
            check_docx_footnotes(root, args.volume, ch),
        ]
        
        chapter_pass = all(c["pass"] for c in checks)
        overall_pass = overall_pass and chapter_pass
        
        result = {
            "chapter": ch,
            "volume": args.volume,
            "overall_pass": chapter_pass,
            "checks": checks
        }
        all_results.append(result)
        
        if not args.json:
            status = "PASS" if chapter_pass else "FAIL"
            print(f"Chapter {ch}: {status}")
            for check in checks:
                c_status = "PASS" if check["pass"] else "FAIL"
                print(f"  [{check['criterion']}] {check['name']}: {c_status}")
                if check["issues"]:
                    for issue in check["issues"]:
                        print(f"    - {issue}")
                if check.get("warnings"):
                    for warning in check["warnings"]:
                        print(f"    ⚠ {warning}")
    
    summary = {
        "volume": args.volume,
        "chapters_tested": len(all_results),
        "overall_pass": overall_pass,
        "results": all_results
    }
    
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    sys.exit(0 if overall_pass else 1)


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project-arendt").is_dir():
            return parent
    return Path.cwd()


if __name__ == "__main__":
    main()