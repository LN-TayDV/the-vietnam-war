#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse all v2 translation files to create translation inventory.
Output: audit/translation_inventory.json
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V2_DIR = ROOT / "04_translation" / "v2"
SRC_DIR = ROOT / "02_extracted_text" / "v2"
AUDIT_DIR = ROOT / "audit"

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
PARA_HDR = re.compile(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)\s*$")
SECTION_RE = re.compile(r"^(I|II|III|IV|V|VI)$")
ARABIC_SECTION_RE = re.compile(r"^(\d{1,3})\s*:?\s*$")
ALLCAPS_SECTION_RE = re.compile(
    r"^[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ]"
    r"[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ\s\d\.,;:'\"()\-–—]+$"
)

def sup_to_int(run):
    return int("".join(str(SUP.index(c)) for c in run))

def parse_paras(text):
    """Parse paragraphs by [V1C##-P###] (trang N) headers."""
    parts = re.split(r"(?m)^\[(V1\w*-?C\d+-P\d{3})\] \(trang (\d+)\)\s*$", text)
    out = []
    i = 1
    while i < len(parts):
        out.append((parts[i], parts[i + 1]))
        i += 3
    return out

def detect_headings(text):
    """Detect heading lines in text."""
    headings = []
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    for ln in lines:
        if SECTION_RE.match(ln):
            headings.append({"type": "roman", "text": ln, "level": 2})
        elif ARABIC_SECTION_RE.match(ln) and len(ln) <= 10:
            headings.append({"type": "arabic", "text": ln.rstrip(":"), "level": 3})
        elif ALLCAPS_SECTION_RE.match(ln) and len(ln) <= 60:
            headings.append({"type": "allcaps", "text": ln, "level": 4})
    return headings

def count_footnote_markers(text):
    """Count inline footnote markers in body text."""
    markers = []
    for run in re.finditer(r"[" + SUP + r"]+", text):
        markers.append(sup_to_int(run.group(0)))
    return markers

def parse_footnotes(fn_part):
    """Parse footnote definitions."""
    notes = {}
    for line in fn_part.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s[0] in SUP:
            run = ""
            for c in s:
                if c in SUP:
                    run += c
                else:
                    break
            num = sup_to_int(run)
            text = s[len(run):].strip()
        else:
            m = re.match(r"^(\d{1,3})\.\s+(.*)$", s)
            if not m:
                continue
            num = int(m.group(1))
            text = m.group(2).strip()
        if num not in notes:
            notes[num] = text
    return notes

def check_vnch_orthography(text):
    """Check for common VNCH orthography issues (Northern terms)."""
    # Common Northern terms that should be VNCH
    northern_terms = {
        r"\bchính phủ\b": "chánh phủ",
        r"\bquốc gia\b": "quốc gia",  # context dependent
        r"\bđược\b": "[passive overuse]",  # flag for review
        r"\bcái\b": "[classifier]",  # flag for review
        r"\brất\b": "quá",  # context dependent
        r"\bchủ tịch nước\b": "tổng thống",
        r"\bthứ trưởng\b": "bộ trưởng",
    }
    issues = []
    for pattern, suggestion in northern_terms.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            issues.append({
                "pattern": pattern,
                "suggestion": suggestion,
                "count": len(matches),
                "positions": [m.start() for m in matches[:5]]  # first 5
            })
    return issues

def process_chapter(chapter_dir):
    """Process one chapter's v2 translation file."""
    vi_files = list(chapter_dir.glob("*.txt"))
    if not vi_files:
        return {"status": "NO_VI_FILE"}
    
    vi_path = vi_files[0]
    vi_text = vi_path.read_text(encoding="utf-8")
    
    # Split body and footnotes
    if "=== FOOTNOTES ===" in vi_text:
        body_part, _, fn_part = vi_text.partition("=== FOOTNOTES ===")
    else:
        body_part = vi_text
        fn_part = ""
    
    # Parse paragraphs
    paras = parse_paras(body_part)
    
    # Count footnote markers in body
    body_markers = count_footnote_markers(body_part)
    
    # Parse footnote definitions
    fn_defs = parse_footnotes(fn_part) if fn_part else {}
    
    # Detect headings in body
    headings = detect_headings(body_part)
    
    # Check VNCH orthography
    vnch_issues = check_vnch_orthography(body_part)
    
    # Check source file
    chapter_name = chapter_dir.name
    src_path = SRC_DIR / f"{chapter_name}_src.txt"
    src_paras = []
    if src_path.exists():
        src_text = src_path.read_text(encoding="utf-8")
        src_paras = parse_paras(src_text)
    
    # Check for English fragments (basic heuristic)
    english_words = re.findall(r'\b[a-zA-Z]{3,}\b', body_part)
    english_fragments = [w for w in english_words if w.lower() not in 
                         {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'has', 'had', 'was', 'were', 'his', 'her', 'its', 'our', 'their', 'this', 'that', 'with', 'from', 'they', 'will', 'would', 'could', 'should', 'about', 'into', 'over', 'after', 'before', 'under', 'again', 'between', 'through', 'during', 'without', 'within', 'along', 'across', 'among', 'around', 'behind', 'below', 'beneath', 'beside', 'beyond', 'inside', 'outside', 'toward', 'towards', 'until', 'upon', 'within'}]
    
    return {
        "file": str(vi_path),
        "paragraphs": len(paras),
        "paragraph_ids": [p[0] for p in paras],
        "src_paragraphs": len(src_paras),
        "src_paragraph_ids": [p[0] for p in src_paras],
        "aligned": len(paras) == len(src_paras) and all(p[0] == s[0] for p, s in zip(paras, src_paras)) if src_paras else None,
        "footnote_markers_in_body": sorted(set(body_markers)),
        "footnote_defs": {str(k): v[:100] for k, v in list(fn_defs.items())[:10]},  # sample
        "footnote_defs_count": len(fn_defs),
        "footnote_defs_range": f"{min(fn_defs.keys())}-{max(fn_defs.keys())}" if fn_defs else "0-0",
        "headings": headings,
        "vnch_orthography_issues": vnch_issues,
        "english_fragments_sample": list(set(english_fragments))[:20],
        "encoding_check": {
            "has_bom": vi_text.startswith('\ufeff'),
            "has_crlf": '\r\n' in vi_text,
            "is_nfc": vi_text == unicodedata.normalize('NFC', vi_text),
        }
    }

def main():
    results = {}
    for chapter_dir in sorted(V2_DIR.iterdir()):
        if chapter_dir.is_dir() and chapter_dir.name.startswith("ch"):
            print(f"Processing {chapter_dir.name}...")
            results[chapter_dir.name] = process_chapter(chapter_dir)
    
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIT_DIR / "translation_inventory.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    main()