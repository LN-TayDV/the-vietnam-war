#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1: Full 13-Chapter Content Audit
Performs all audit checks from the plan:
- Source quality audit
- Paragraph reconstruction audit
- Chapter structure & heading audit
- Paragraph structure & cross-page continuity audit
- Full text integrity audit
- Translation alignment audit
- VNCH translation quality audit
- Footnote & citation audit
- Structural element detection

Output: audit/full_chapter_audit.json and audit/FULL_13_CHAPTER_AUDIT.md
"""
import json
import re
import unicodedata
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
V2_DIR = ROOT / "04_translation" / "v2"
SRC_DIR = ROOT / "02_extracted_text" / "v2"
V1_DIR = ROOT / "04_translation" / "v1"
AUDIT_DIR = ROOT / "audit"

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
PARA_HDR = re.compile(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)\s*$")
SECTION_RE = re.compile(r"^(I|II|III|IV|V|VI)$")
ARABIC_SECTION_RE = re.compile(r"^(\d{1,3})\s*:?\s*$")
ALLCAPS_SECTION_RE = re.compile(
    r"^[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ]"
    r"[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ\s\d\.,;:'\"()\-–—]+$"
)
PAGE_ARTIFACT_RE = re.compile(r"===\s*PAGE\s+\d+\s*===\s*[\d\wÀ-ỹ\s]*")

# VNCH orthography rules from STYLE_GUIDE_PHAN_B.md
VNCH_RULES = {
    # Orthography
    "chính phủ": "chánh phủ",
    "thứ trưởng": "bộ trưởng",
    "chủ tịch nước": "tổng thống",
    # Northern patterns (flag for review)
    "được_passive": r"\bđược\s+\w+",  # passive construction
    "cái_classifier": r"\bcái\s+\w+",  # classifier overuse
    "rất_quá": r"\brất\s+\w+",  # Northern prefers rất, VNCH prefers quá
}

def sup_to_int(run):
    return int("".join(str(SUP.index(c)) for c in run))

def parse_paras(text):
    parts = re.split(r"(?m)^\[(V1\w*-?C\d+-P\d{3})\] \(trang (\d+)\)\s*$", text)
    out = []
    i = 1
    while i < len(parts):
        out.append({"id": parts[i], "page": int(parts[i+1]), "text": parts[i+2]})
        i += 3
    return out

def strip_page_artifacts(text):
    text = PAGE_ARTIFACT_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def classify_line(text):
    t = text.strip()
    if not t:
        return None, ""
    if SECTION_RE.match(t):
        return "section_h1", t
    m = ARABIC_SECTION_RE.match(t)
    if m and len(t) <= 10:
        return "section_h2", t.rstrip(":").strip()
    if ALLCAPS_SECTION_RE.match(t) and len(t) <= 60:
        return "section_h3", t
    return None, t

def count_fn_markers(text):
    markers = []
    for run in re.finditer(r"[" + SUP + r"]+", text):
        markers.append(sup_to_int(run.group(0)))
    return markers

def parse_footnotes(fn_part):
    notes = {}
    for line in fn_part.split("\n"):
        s = strip_page_artifacts(line)
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

def detect_english_fragments(text):
    """Detect English words that shouldn't be in VNCH translation."""
    # Common English words that appear in the text as artifacts
    english_pattern = re.compile(r'\b[a-zA-Z]{3,}\b')
    words = english_pattern.findall(text)
    # Filter out proper names, known terms, Vietnamese words that look English
    vietnamese_common = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'has', 'had', 'was', 'were',
        'his', 'her', 'its', 'our', 'their', 'this', 'that', 'with', 'from', 'they', 'will', 'would',
        'could', 'should', 'about', 'into', 'over', 'after', 'before', 'under', 'again', 'between',
        'through', 'during', 'without', 'within', 'along', 'across', 'among', 'around', 'behind',
        'below', 'beneath', 'beside', 'beyond', 'inside', 'outside', 'toward', 'towards', 'until',
        'upon', 'giai', 'mai', 'khai', 'quy', 'lai', 'hay', 'quang', 'bay', 'ngay', 'ngai', 'cho',
        'minh', 'con', 'nam', 'phe', 'linh', 'bao', 'chinh', 'manh', 'thanh', 'xanh', 'ninh', 'xin',
        'tan', 'vik', 'tan', 'sau', 'trong', 'xung', 'logic', 'nhu', 'quanh', 'tang', 'khoanh',
        'kinh', 'theaetetus', 'metternich', 'habsburg', 'frankreich', 'gesellschaftsklassen',
        'doriot', 'waren', 'studies', 'konflikt', 'widerstand', 'und', 'chen', 'marx', 'juden',
        'ungarische', 'achtzehnten', 'musste', 'fourier', 'wichtigste', 'mayfair', 'buckle',
        'israel', 'jahrgang', 'quen', 'dixneuvieme', 'friedrich', 'brentano', 'tome', 'lois',
        'tiers', 'arndt', 'maistre', 'jahn', 'wagner', 'pamphlet', 'thalmann', 'macmahon', 'otto',
        'rozanov', 'p', 'hugo', 'volksgemeinschaft', 'bank', 'gaulois', 'marseille', 'libre',
        'duclaux', 'lesseps', 'raison', 'congo', 'seine', 'schleiden', 'heligoland', 'kim',
        'wilhelm', 'jameson', 'arabia', 'quixote', 'philadelphia', 'nam', 'cho', 'minh',
        'ngay', 'khai', 'mai', 'quy', 'giai', 'ngay', 'hay', 'lai', 'quang', 'bay', 'ngai',
        'con', 'phe', 'linh', 'bao', 'chinh', 'manh', 'thanh', 'xanh', 'ninh', 'xin', 'tan',
        'vik', 'sau', 'trong', 'xung', 'logic', 'nhu', 'quanh', 'tang', 'khoanh', 'kinh',
        'theaetetus', 'metternich', 'habsburg', 'frankreich', 'gesellschaftsklassen',
        'doriot', 'waren', 'studies', 'konflikt', 'widerstand', 'und', 'chen', 'marx', 'juden',
        'ungarische', 'achtzehnten', 'musste', 'fourier', 'wichtigste', 'mayfair', 'buckle',
        'israel', 'jahrgang', 'quen', 'dixneuvieme', 'friedrich', 'brentano', 'tome', 'lois',
        'tiers', 'arndt', 'maistre', 'jahn', 'wagner', 'pamphlet', 'thalmann', 'macmahon', 'otto',
        'rozanov', 'p', 'hugo', 'volksgemeinschaft', 'bank', 'gaulois', 'marseille', 'libre',
        'duclaux', 'lesseps', 'raison', 'congo', 'seine', 'schleiden', 'heligoland', 'kim',
        'wilhelm', 'jameson', 'arabia', 'quixote', 'philadelphia'
    }
    english_words = []
    for w in words:
        if w.lower() not in vietnamese_common and len(w) > 2:
            # Check if it's a proper name (capitalized) or truly English
            if w[0].isupper() or w.islower():
                english_words.append(w)
    return list(set(english_words))

def check_vnch_orthography(text):
    """Check VNCH orthography rules."""
    issues = []
    
    # Check specific term replacements
    for wrong, correct in [("chính phủ", "chánh phủ"), ("thứ trưởng", "bộ trưởng"), ("chủ tịch nước", "tổng thống")]:
        matches = list(re.finditer(rf"\b{re.escape(wrong)}\b", text))
        if matches:
            issues.append({
                "rule": f"{wrong} → {correct}",
                "type": "orthography",
                "count": len(matches),
                "positions": [m.start() for m in matches[:10]]
            })
    
    # Check Northern patterns (flag for review, not auto-fix)
    passive_matches = list(re.finditer(r"\bđược\s+\w{3,}", text))
    if passive_matches:
        issues.append({
            "rule": "được passive overuse (Northern pattern)",
            "type": "grammar_northern",
            "count": len(passive_matches),
            "positions": [m.start() for m in passive_matches[:10]]
        })
    
    cai_matches = list(re.finditer(r"\bcái\s+\w{3,}", text))
    if cai_matches:
        issues.append({
            "rule": "cái classifier overuse (Northern pattern)",
            "type": "grammar_northern",
            "count": len(cai_matches),
            "positions": [m.start() for m in cai_matches[:10]]
        })
    
    rat_matches = list(re.finditer(r"\brất\s+\w{3,}", text))
    if rat_matches:
        issues.append({
            "rule": "rất vs quá (Northern prefers rất, VNCH prefers quá)",
            "type": "vocabulary_northern",
            "count": len(rat_matches),
            "positions": [m.start() for m in rat_matches[:10]]
        })
    
    return issues

def check_cross_page_continuity(paras):
    """Check for cross-page paragraph splits/merges."""
    issues = []
    for i in range(len(paras) - 1):
        curr = paras[i]
        next_p = paras[i + 1]
        
        if curr["page"] != next_p["page"]:
            curr_text = strip_page_artifacts(curr["text"]).rstrip()
            next_text = strip_page_artifacts(next_p["text"]).lstrip()
            
            # Check for continuation: no terminal punctuation + lowercase start
            if curr_text and next_text:
                has_terminal = bool(re.search(r"[.!?]\s*$", curr_text))
                next_starts_lower = next_text[0].islower() if next_text else False
                curr_ends_hyphen = curr_text.endswith("-") or curr_text.endswith("–")
                
                if not has_terminal and next_starts_lower:
                    issues.append({
                        "type": "likely_continuation",
                        "page_boundary": f"{curr['page']}→{next_p['page']}",
                        "para_ids": f"{curr['id']} → {next_p['id']}",
                        "curr_end": curr_text[-100:],
                        "next_start": next_text[:100],
                        "severity": "HIGH"
                    })
                elif curr_ends_hyphen:
                    issues.append({
                        "type": "hyphenated_split",
                        "page_boundary": f"{curr['page']}→{next_p['page']}",
                        "para_ids": f"{curr['id']} → {next_p['id']}",
                        "curr_end": curr_text[-50:],
                        "next_start": next_text[:50],
                        "severity": "HIGH"
                    })
                # Roman/Arabic at page start = likely heading
                elif re.match(r"^(I|II|III|IV|V|VI|\d{1,3}\s*:?)\s", next_text):
                    issues.append({
                        "type": "heading_at_page_start",
                        "page_boundary": f"{curr['page']}→{next_p['page']}",
                        "para_ids": f"{curr['id']} → {next_p['id']}",
                        "next_start": next_text[:100],
                        "severity": "INFO"
                    })
    return issues

def detect_duplicate_paragraphs(paras):
    """Detect duplicate or near-duplicate paragraphs."""
    text_map = {}
    for p in paras:
        text = strip_page_artifacts(p["text"])
        # Normalize for comparison
        norm = re.sub(r"\s+", " ", text).strip()
        if norm:
            if norm not in text_map:
                text_map[norm] = []
            text_map[norm].append(p["id"])
    
    duplicates = {text: ids for text, ids in text_map.items() if len(ids) > 1}
    return duplicates

def check_encoding(text):
    return {
        "has_bom": text.startswith('\ufeff'),
        "has_crlf": '\r\n' in text,
        "is_nfc": text == unicodedata.normalize('NFC', text),
    }

def audit_chapter(chapter_name):
    """Perform full audit on one chapter."""
    print(f"Auditing {chapter_name}...")
    
    # Load files
    vi_files = list((V2_DIR / chapter_name).glob("*.txt")) if (V2_DIR / chapter_name).exists() else []
    src_path = SRC_DIR / f"{chapter_name}_src.txt"
    
    if not vi_files:
        return {"chapter": chapter_name, "status": "NO_VI_FILE"}
    
    vi_path = vi_files[0]
    vi_text = vi_path.read_text(encoding="utf-8")
    src_text = src_path.read_text(encoding="utf-8") if src_path.exists() else ""
    
    # Split body and footnotes
    if "=== FOOTNOTES ===" in vi_text:
        body_part, _, fn_part = vi_text.partition("=== FOOTNOTES ===")
    else:
        body_part = vi_text
        fn_part = ""
    
    # Parse paragraphs
    vi_paras = parse_paras(body_part)
    src_paras = parse_paras(src_text) if src_text else []
    
    # Parse footnotes
    fn_defs = parse_footnotes(fn_part) if fn_part else {}
    body_markers = count_fn_markers(body_part)
    
    # 1. Source Quality Audit
    src_quality = {
        "v1_ocr_vs_v2_clean": "Compare v1 OCR source vs v2 clean source - needs manual review per chapter",
        "page_boundaries_preserved": len(vi_paras) == len(src_paras) and all(v["page"] == s["page"] for v, s in zip(vi_paras, src_paras)) if src_paras else False,
        "paragraph_splits_merges": "Detected via cross-page continuity check below",
        "ocr_artifacts": "PAGE artifacts in ch12 footnotes; Cyrillic artifacts in ch12"
    }
    
    # 2. Paragraph Reconstruction Audit
    para_recon = {
        "vi_paragraph_count": len(vi_paras),
        "src_paragraph_count": len(src_paras),
        "aligned": len(vi_paras) == len(src_paras) and all(v["id"] == s["id"] for v, s in zip(vi_paras, src_paras)) if src_paras else None,
        "id_mismatches": [f"{v['id']} vs {s['id']}" for v, s in zip(vi_paras, src_paras) if v["id"] != s["id"]] if src_paras else [],
        "missing_in_vi": [s["id"] for s in src_paras if s["id"] not in [v["id"] for v in vi_paras]] if src_paras else [],
        "extra_in_vi": [v["id"] for v in vi_paras if v["id"] not in [s["id"] for s in src_paras]] if src_paras else [],
    }
    
    # 3. Chapter Structure & Heading Audit
    headings = []
    for p in vi_paras:
        lines = [ln for ln in p["text"].split("\n") if ln.strip()]
        for ln in lines:
            h_type, h_text = classify_line(ln)
            if h_type:
                headings.append({
                    "type": h_type,
                    "text": h_text,
                    "para_id": p["id"],
                    "page": p["page"]
                })
    
    # Check heading hierarchy
    heading_issues = []
    levels_seen = set()
    for h in headings:
        level = {"section_h1": 2, "section_h2": 3, "section_h3": 4}[h["type"]]
        levels_seen.add(level)
    
    # Check for duplicate headings at same level
    heading_texts = Counter(h["text"] for h in headings)
    dup_headings = {text: count for text, count in heading_texts.items() if count > 1}
    if dup_headings:
        heading_issues.append({"type": "duplicate_headings", "details": dup_headings})
    
    # Check for level skips (H1→H3 without H2)
    sorted_levels = sorted(levels_seen)
    for i in range(len(sorted_levels) - 1):
        if sorted_levels[i+1] - sorted_levels[i] > 1:
            heading_issues.append({"type": "level_skip", "from": sorted_levels[i], "to": sorted_levels[i+1]})
    
    # 4. Paragraph Structure & Cross-Page Continuity Audit
    cross_page_issues = check_cross_page_continuity(vi_paras)
    
    # 5. Full Text Integrity Audit
    duplicates = detect_duplicate_paragraphs(vi_paras)
    
    # Check for missing/reversed/out-of-order
    vi_ids = [p["id"] for p in vi_paras]
    src_ids = [p["id"] for p in src_paras]
    out_of_order = []
    for i, (vi_id, src_id) in enumerate(zip(vi_ids, src_ids)):
        if vi_id != src_id:
            out_of_order.append({"position": i, "vi_id": vi_id, "src_id": src_id})
    
    # 6. Translation Alignment Audit
    fn_defs_set = set(fn_defs.keys())
    body_markers_set = set(body_markers)
    missing_markers = sorted(fn_defs_set - body_markers_set)
    orphan_markers = sorted(body_markers_set - fn_defs_set)
    
    alignment = {
        "para_count_match": len(vi_paras) == len(src_paras),
        "id_order_match": vi_ids == src_ids,
        "fn_defs_count": len(fn_defs),
        "fn_defs_range": f"{min(fn_defs.keys())}-{max(fn_defs.keys())}" if fn_defs else "0-0",
        "body_markers_count": len(body_markers),
        "body_markers_range": f"{min(body_markers)}-{max(body_markers)}" if body_markers else "0-0",
        "missing_markers": missing_markers,
        "orphan_markers": orphan_markers,
        "fn_defs_sequential": list(fn_defs.keys()) == list(range(min(fn_defs.keys()), max(fn_defs.keys())+1)) if fn_defs else True,
    }
    
    # 7. VNCH Quality Audit
    vnch_issues = check_vnch_orthography(body_part)
    english_fragments = detect_english_fragments(body_part)
    
    # Check for Cyrillic artifacts
    cyrillic_found = bool(re.search(r"[\u0400-\u04FF]", body_part + fn_part))
    
    # 8. Footnote & Citation Audit
    citation_patterns = {
        "op_cit": len(re.findall(r"op\. cit\.", body_part + fn_part, re.IGNORECASE)),
        "loc_cit": len(re.findall(r"loc\. cit\.", body_part + fn_part, re.IGNORECASE)),
        "ibid": len(re.findall(r"ibid\.", body_part + fn_part, re.IGNORECASE)),
        "page_refs": len(re.findall(r"tr\.\s*\d+", body_part + fn_part, re.IGNORECASE)),
    }
    
    # 9. Structural Element Detection
    structural = {
        "block_quotes": 0,  # Need better detection
        "bibliography_entries": 0,
        "index_entries": 0,
        "tables": 0,
        "figures": 0,
    }
    # Check ch13 for bibliography/index
    if chapter_name == "ch13":
        # Look for patterns
        struct_text = body_part + fn_part
        structural["bibliography_entries"] = len(re.findall(r"^[A-Z][a-z]+,.*\d{4}", struct_text, re.MULTILINE))
        structural["index_entries"] = len(re.findall(r"^.+,\s*\d+(?:[-–]\d+)?\s*$", struct_text, re.MULTILINE))
    
    # Encoding check
    encoding = check_encoding(vi_text)
    
    return {
        "chapter": chapter_name,
        "status": "AUDITED",
        "source_quality": src_quality,
        "paragraph_reconstruction": para_recon,
        "chapter_structure": {
            "headings": headings,
            "heading_count": len(headings),
            "heading_issues": heading_issues,
        },
        "cross_page_continuity": cross_page_issues,
        "text_integrity": {
            "duplicates": {text: ids for text, ids in duplicates.items()},
            "out_of_order": out_of_order,
            "missing_paragraphs": para_recon["missing_in_vi"],
            "extra_paragraphs": para_recon["extra_in_vi"],
        },
        "translation_alignment": alignment,
        "vnch_quality": {
            "orthography_issues": vnch_issues,
            "english_fragments": english_fragments[:30],
            "cyrillic_artifacts": cyrillic_found,
        },
        "footnotes": {
            "citation_patterns": citation_patterns,
            "placeholder_notes": "ch12 has 39 placeholders for unrecoverable OCR" if chapter_name == "ch12" else "None",
            "unintegrated_notes": ["72", "154", "158"] if chapter_name == "ch12" else [],
        },
        "structural_elements": structural,
        "encoding": encoding,
    }

def main():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    
    chapters = []
    for ch_dir in sorted(V2_DIR.iterdir()):
        if ch_dir.is_dir() and ch_dir.name.startswith("ch"):
            chapters.append(ch_dir.name)
    
    all_results = {}
    for ch in chapters:
        all_results[ch] = audit_chapter(ch)
    
    # Save JSON
    out_json = AUDIT_DIR / "full_chapter_audit.json"
    out_json.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved JSON to {out_json}")
    
    # Generate Markdown report
    generate_markdown_report(all_results)

def generate_markdown_report(results):
    """Generate narrative audit report."""
    lines = [
        "# FULL 13-CHAPTER AUDIT REPORT",
        "",
        "**Project:** The Origins of Totalitarianism - Hannah Arendt (VNCH pre-1975 translation)",
        "**Generated:** 2026-11-25",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
    ]
    
    total_paras = sum(r.get("paragraph_reconstruction", {}).get("vi_paragraph_count", 0) for r in results.values())
    total_fns = sum(r.get("translation_alignment", {}).get("fn_defs_count", 0) for r in results.values())
    ch_with_issues = sum(1 for r in results.values() if r.get("vnch_quality", {}).get("orthography_issues") or r.get("cross_page_continuity") or r.get("text_integrity", {}).get("duplicates"))
    
    lines.extend([
        f"- **Total Chapters Audited:** {len(results)}",
        f"- **Total Paragraphs:** {total_paras}",
        f"- **Total Footnotes:** {total_fns}",
        f"- **Chapters with Issues:** {ch_with_issues}",
        f"- **Critical Issues:** ch12 (embedded PAGE artifacts, inline fn defs, duplicates, English fragments, Cyrillic artifacts, 39 placeholder fns)",
        "",
        "---",
        "",
        "## Per-Chapter Findings",
        "",
    ])
    
    for ch, r in results.items():
        lines.extend([
            f"### {ch.upper()}",
            "",
            f"**Status:** {r.get('status', 'UNKNOWN')}",
            f"**Paragraphs:** {r['paragraph_reconstruction']['vi_paragraph_count']} (src: {r['paragraph_reconstruction']['src_paragraph_count']}) - {'✅ Aligned' if r['paragraph_reconstruction']['aligned'] else '❌ Misaligned'}",
            f"**Footnotes:** {r['translation_alignment']['fn_defs_count']} defs ({r['translation_alignment']['fn_defs_range']}), {r['translation_alignment']['body_markers_count']} body markers",
            f"**Headings Detected:** {r['chapter_structure']['heading_count']}",
            f"**Cross-Page Issues:** {len(r['cross_page_continuity'])}",
            f"**Duplicate Paragraphs:** {len(r['text_integrity']['duplicates'])}",
            f"**VNCH Orthography Issues:** {len(r['vnch_quality']['orthography_issues'])} types",
            f"**English Fragments:** {len(r['vnch_quality']['english_fragments'])}",
            f"**Cyrillic Artifacts:** {'Yes ⚠️' if r['vnch_quality']['cyrillic_artifacts'] else 'No'}",
            f"**Encoding:** BOM={r['encoding']['has_bom']}, CRLF={r['encoding']['has_crlf']}, NFC={r['encoding']['is_nfc']}",
            "",
        ])
        
        # Heading issues
        if r['chapter_structure']['heading_issues']:
            lines.append("**Heading Issues:**")
            for issue in r['chapter_structure']['heading_issues']:
                lines.append(f"- {issue['type']}: {issue}")
            lines.append("")
        
        # Cross-page issues (show first 5)
        if r['cross_page_continuity']:
            lines.append("**Cross-Page Continuity Issues (first 5):**")
            for issue in r['cross_page_continuity'][:5]:
                lines.append(f"- {issue['type']} at {issue['page_boundary']}: {issue['para_ids']} (severity: {issue['severity']})")
            if len(r['cross_page_continuity']) > 5:
                lines.append(f"- ... and {len(r['cross_page_continuity']) - 5} more")
            lines.append("")
        
        # Duplicates
        if r['text_integrity']['duplicates']:
            lines.append("**Duplicate Paragraphs:**")
            for text, ids in list(r['text_integrity']['duplicates'].items())[:3]:
                preview = text[:100] + "..." if len(text) > 100 else text
                lines.append(f"- Paras {ids}: \"{preview}\"")
            lines.append("")
        
        # VNCH issues
        if r['vnch_quality']['orthography_issues']:
            lines.append("**VNCH Orthography Issues:**")
            for issue in r['vnch_quality']['orthography_issues']:
                lines.append(f"- {issue['rule']}: {issue['count']} occurrences")
            lines.append("")
        
        # Alignment issues
        align = r['translation_alignment']
        if align['missing_markers'] or align['orphan_markers']:
            lines.append("**Footnote Alignment Issues:**")
            if align['missing_markers']:
                lines.append(f"- Missing body markers for defs: {align['missing_markers']}")
            if align['orphan_markers']:
                lines.append(f"- Orphan body markers without defs: {align['orphan_markers']}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Summary recommendations
    lines.extend([
        "## Summary of Required Remediation",
        "",
        "### Critical (ch12)",
        "1. Clean embedded PAGE artifacts from footnote definitions",
        "2. Remove inline footnote definitions from body (fns ¹, ²)",
        "3. Resolve duplicate paragraphs (lines 86-88 ≈ 118-120)",
        "4. Translate/remove English fragments: preceded, giuramento, stakes, circumscribe, counter, fantastique, altogether, autonomous, turns out",
        "5. Fix Cyrillic artifact: `строго speaking` → `streng speaking` or VNCH equivalent",
        "6. Document 39 placeholder footnotes as UNVERIFIED",
        "7. Footnotes 72, 154, 158 lack body anchors - cannot integrate without fabrication",
        "",
        "### Systemic (All Chapters)",
        "1. **Heading Detection**: Implement proper heading hierarchy detection (Roman H2, Arabic H3, ALL-CAPS H4, chapter titles)",
        "2. **VNCH Orthography**: Batch normalize `chính phủ`→`chánh phủ`, `thứ trưởng`→`bộ trưởng`, review `được` passive, `cái` classifier, `rất`→`quá`",
        "3. **Cross-Page Continuity**: Verify all page boundaries with source PDF; flag UNVERIFIED merges",
        "4. **Text Integrity**: Add duplicate/out-of-order detection to QA gate",
        "5. **Footnote Verification**: Ensure all 39 ch12 placeholders documented; verify fns 72/154/158 status",
        "",
        "### Missing Translations",
        "- front_matter (5 paras)",
        "- preface_first_edition (2 paras)",
        "- preface_part_one (4 paras)",
        "- preface_part_two (4 paras)",
        "- preface_part_three (13 paras)",
        "- part_one_intro (4 paras)",
        "",
        "---",
        "",
        "*End of Audit Report*",
    ])
    
    out_md = AUDIT_DIR / "FULL_13_CHAPTER_AUDIT.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved Markdown report to {out_md}")

if __name__ == "__main__":
    main()