#!/usr/bin/env python3
"""
Realignment script v3: Sequence-based alignment using paragraph order.
Since pagination schemes differ, match by content order with dynamic programming.
"""

import re
import json
from pathlib import Path

def parse_paragraphs(text: str):
    """Parse paragraphs with [ID] (trang N) format."""
    paragraphs = []
    pattern = r'(\[V1[^\]]+\]\s*\(trang\s+\d+\))'
    parts = re.split(pattern, text)
    
    current_id = None
    current_page = None
    current_text = ""
    
    for part in parts:
        if re.match(pattern, part.strip()):
            if current_id and current_text.strip():
                paragraphs.append({
                    "id": current_id,
                    "page": current_page,
                    "text": current_text.strip()
                })
            match = re.match(r'\[(V1[^\]]+)\]\s*\(trang\s+(\d+)\)', part.strip())
            if match:
                current_id = match.group(1)
                current_page = int(match.group(2))
                current_text = ""
        else:
            current_text += part
    
    if current_id and current_text.strip():
        paragraphs.append({
            "id": current_id,
            "page": current_page,
            "text": current_text.strip()
        })
    
    return paragraphs

def extract_footnotes(text: str):
    """Extract footnotes from === FOOTNOTES === section."""
    if "=== FOOTNOTES ===" not in text:
        return {}
    fn_section = text.split("=== FOOTNOTES ===")[1]
    footnotes = {}
    for match in re.finditer(r'\[(\d+)\]\s*(.+?)(?=\n\[\d+\]|\n*$)', fn_section, re.DOTALL):
        num = match.group(1)
        content = match.group(2).strip()
        footnotes[num] = content
    return footnotes

def simple_similarity(a: str, b: str) -> float:
    """Cross-language similarity using numbers, proper nouns, punctuation patterns."""
    # Extract numbers
    a_nums = set(re.findall(r'\b\d+\b', a))
    b_nums = set(re.findall(r'\b\d+\b', b))
    num_score = len(a_nums & b_nums) * 3
    
    # Extract proper nouns (capitalized, 2+ chars)
    a_proper = set(re.findall(r'\b[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĐ][a-zàáâãèéêìíòóôõùúỹđ]{2,}', a))
    b_proper = set(re.findall(r'\b[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĐ][a-zàáâãèéêìíòóôõùúỹđ]{2,}', b))
    proper_score = len(a_proper & b_proper) * 5
    
    # Extract words with length > 3 (might be cognates or same proper nouns)
    a_words = set(w.lower() for w in re.findall(r'\b\w{4,}\b', a))
    b_words = set(w.lower() for w in re.findall(r'\b\w{4,}\b', b))
    word_score = len(a_words & b_words)
    
    # Punctuation pattern similarity
    a_punct = re.sub(r'[^\.,;:!?\-\(\)\[\]"\']', '', a)
    b_punct = re.sub(r'[^\.,;:!?\-\(\)\[\]"\']', '', b)
    punct_score = len(set(a_punct) & set(b_punct))
    
    return num_score + proper_score + word_score + punct_score

def align_sequences(en_paras, vi_paras):
    """
    Align two sequences using dynamic programming (Needleman-Wunsch style).
    Allows 1:1, 1:2, 2:1 matches.
    """
    n, m = len(en_paras), len(vi_paras)
    
    # DP table: dp[i][j] = best score for en[:i] and vi[:j]
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    trace = [[None] * (m + 1) for _ in range(n + 1)]
    
    # Gap penalty
    gap_penalty = -5.0
    
    # Initialize
    for i in range(1, n + 1):
        dp[i][0] = dp[i-1][0] + gap_penalty
        trace[i][0] = ('gap_en', i-1, 0)
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j-1] + gap_penalty
        trace[0][j] = ('gap_vi', 0, j-1)
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # 1:1 match
            score_11 = simple_similarity(en_paras[i-1]['text'], vi_paras[j-1]['text'])
            best = dp[i-1][j-1] + score_11
            move = ('match_11', i-1, j-1)
            
            # 1:2 match (en[i] matches vi[j-1] + vi[j])
            if j >= 2:
                combined_vi = vi_paras[j-2]['text'] + " " + vi_paras[j-1]['text']
                score_12 = simple_similarity(en_paras[i-1]['text'], combined_vi)
                val = dp[i-1][j-2] + score_12
                if val > best:
                    best = val
                    move = ('match_12', i-1, j-2)
            
            # 2:1 match (en[i-1] + en[i] matches vi[j])
            if i >= 2:
                combined_en = en_paras[i-2]['text'] + " " + en_paras[i-1]['text']
                score_21 = simple_similarity(combined_en, vi_paras[j-1]['text'])
                val = dp[i-2][j-1] + score_21
                if val > best:
                    best = val
                    move = ('match_21', i-2, j-1)
            
            # Gap in EN
            val_gap_en = dp[i-1][j] + gap_penalty
            if val_gap_en > best:
                best = val_gap_en
                move = ('gap_en', i-1, j)
            
            # Gap in VI
            val_gap_vi = dp[i][j-1] + gap_penalty
            if val_gap_vi > best:
                best = val_gap_vi
                move = ('gap_vi', i, j-1)
            
            dp[i][j] = best
            trace[i][j] = move
    
    # Traceback
    alignment = []
    i, j = n, m
    while i > 0 or j > 0:
        move = trace[i][j]
        if move[0] == 'match_11':
            alignment.append(('match_11', i-1, j-1))
            i, j = move[1], move[2]
        elif move[0] == 'match_12':
            alignment.append(('match_12', i-1, j-2, j-1))
            i, j = move[1], move[2]
        elif move[0] == 'match_21':
            alignment.append(('match_21', i-2, i-1, j-1))
            i, j = move[1], move[2]
        elif move[0] == 'gap_en':
            alignment.append(('gap_en', i-1))
            i, j = move[1], move[2]
        elif move[0] == 'gap_vi':
            alignment.append(('gap_vi', j-1))
            i, j = move[1], move[2]
    
    alignment.reverse()
    return alignment

def realign_chapter(chapter: int, volume: str = "v2"):
    """Realign Vietnamese paragraphs to English paragraph structure."""
    root = Path("/workspaces/the-vietnam-war/translation-project-arendt")
    
    # Load English source
    en_file = root / f"02_extracted_text/{volume}/{volume}_ch{chapter:02d}_src.txt"
    en_text = en_file.read_text(encoding='utf-8')
    en_paras = parse_paragraphs(en_text)
    
    # Load Vietnamese translation
    vi_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi.txt"
    vi_text = vi_file.read_text(encoding='utf-8')
    vi_paras = parse_paragraphs(vi_text)
    
    # Extract footnotes
    vi_footnotes = extract_footnotes(vi_text)
    
    print(f"Chapter {chapter}: EN={len(en_paras)} paras, VI={len(vi_paras)} paras")
    print(f"  VI footnotes: {len(vi_footnotes)}")
    
    # Align sequences
    alignment = align_sequences(en_paras, vi_paras)
    
    # Build realigned output
    realigned = []
    vi_used = set()
    
    for item in alignment:
        if item[0] == 'match_11':
            _, en_idx, vi_idx = item
            realigned.append({
                "en_id": en_paras[en_idx]['id'],
                "en_page": en_paras[en_idx]['page'],
                "vi_id": vi_paras[vi_idx]['id'],
                "vi_page": vi_paras[vi_idx]['page'],
                "type": "1:1",
                "vi_text": vi_paras[vi_idx]['text']
            })
            vi_used.add(vi_idx)
        elif item[0] == 'match_12':
            _, en_idx, vi_idx1, vi_idx2 = item
            combined = vi_paras[vi_idx1]['text'] + "\n\n" + vi_paras[vi_idx2]['text']
            realigned.append({
                "en_id": en_paras[en_idx]['id'],
                "en_page": en_paras[en_idx]['page'],
                "vi_id": f"{vi_paras[vi_idx1]['id']}+{vi_paras[vi_idx2]['id']}",
                "vi_page": f"{vi_paras[vi_idx1]['page']}-{vi_paras[vi_idx2]['page']}",
                "type": "1:2",
                "vi_text": combined
            })
            vi_used.add(vi_idx1)
            vi_used.add(vi_idx2)
        elif item[0] == 'match_21':
            _, en_idx1, en_idx2, vi_idx = item
            # Assign to first EN paragraph, note the merge
            realigned.append({
                "en_id": f"{en_paras[en_idx1]['id']}+{en_paras[en_idx2]['id']}",
                "en_page": f"{en_paras[en_idx1]['page']}-{en_paras[en_idx2]['page']}",
                "vi_id": vi_paras[vi_idx]['id'],
                "vi_page": vi_paras[vi_idx]['page'],
                "type": "2:1",
                "vi_text": vi_paras[vi_idx]['text']
            })
            vi_used.add(vi_idx)
        elif item[0] == 'gap_en':
            _, en_idx = item
            realigned.append({
                "en_id": en_paras[en_idx]['id'],
                "en_page": en_paras[en_idx]['page'],
                "vi_id": None,
                "vi_page": None,
                "type": "gap_en",
                "vi_text": "[MISSING - NO VIETNAMESE MATCH]"
            })
        elif item[0] == 'gap_vi':
            _, vi_idx = item
            realigned.append({
                "en_id": f"EXTRA_{vi_paras[vi_idx]['id']}",
                "en_page": None,
                "vi_id": vi_paras[vi_idx]['id'],
                "vi_page": vi_paras[vi_idx]['page'],
                "type": "extra_vi",
                "vi_text": vi_paras[vi_idx]['text']
            })
            vi_used.add(vi_idx)
    
    # Output realigned Vietnamese with English IDs
    output_lines = []
    for item in realigned:
        if item['vi_id']:
            output_lines.append(f"[{item['en_id']}] (trang {item['en_page'] if item['en_page'] else '?'})")
            output_lines.append(item['vi_text'])
            output_lines.append("")
        else:
            output_lines.append(f"[{item['en_id']}] (trang {item['en_page']})")
            output_lines.append(item['vi_text'])
            output_lines.append("")
    
    # Add footnotes
    if vi_footnotes:
        output_lines.append("=== FOOTNOTES ===")
        for num in sorted(vi_footnotes.keys(), key=int):
            output_lines.append(f"[{num}] {vi_footnotes[num]}")
    
    output_text = "\n".join(output_lines).strip() + "\n"
    
    # Save realigned file
    out_file = root / f"04_translation/{volume}/ch{chapter:02d}/{volume}_ch{chapter:02d}_vi_realigned.txt"
    out_file.write_text(output_text, encoding='utf-8')
    
    # Stats
    matched_11 = sum(1 for r in realigned if r['type'] == '1:1')
    matched_12 = sum(1 for r in realigned if r['type'] == '1:2')
    matched_21 = sum(1 for r in realigned if r['type'] == '2:1')
    gaps_en = sum(1 for r in realigned if r['type'] == 'gap_en')
    extra_vi = sum(1 for r in realigned if r['type'] == 'extra_vi')
    
    print(f"  1:1 matches: {matched_11}, 1:2: {matched_12}, 2:1: {matched_21}")
    print(f"  Gaps EN: {gaps_en}, Extra VI: {extra_vi}")
    print(f"  Saved: {out_file}")
    
    # Save alignment report
    report_file = root / f"04_translation/{volume}/ch{chapter:02d}/alignment_report_ch{chapter:02d}.json"
    report = {
        "chapter": chapter,
        "en_paragraphs": len(en_paras),
        "vi_paragraphs": len(vi_paras),
        "matched_11": matched_11,
        "matched_12": matched_12,
        "matched_21": matched_21,
        "gaps_en": gaps_en,
        "extra_vi": extra_vi,
        "alignment": alignment,
        "details": realigned
    }
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"  Report: {report_file}")
    
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        chapter = int(sys.argv[1])
        realign_chapter(chapter)
    else:
        for ch in range(1, 14):
            realign_chapter(ch)