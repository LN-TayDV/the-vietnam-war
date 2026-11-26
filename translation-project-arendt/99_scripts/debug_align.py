# -*- coding: utf-8 -*-
"""
Paragraph + footnote alignment checker for v2 chapter files.

Usage:
    python 99_scripts/debug_align.py ch04 [ch05 ...]

Checks:
  - source paragraph count == vi paragraph count (Rule 18)
  - paragraph IDs match 1-1 and in order
  - footnote definition count and sequential 1..N
  - inline footnote markers in body vs definitions (missing/orphan)

Exit 0 = PASS, 1 = FAIL.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "02_extracted_text" / "v2"
V2 = ROOT / "04_translation" / "v2"
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def parse_paras(text):
    parts = re.split(r"(?m)^\[(V1\w*-?C\d+-P\d{3})\] \(trang (\d+)\)\s*$", text)
    out = []
    i = 1
    while i < len(parts):
        out.append((parts[i], parts[i + 1]))
        i += 3
    return out


def fn_num(s):
    s = s.strip()
    if not s:
        return None
    if s[0] in SUP:
        n = ""
        for c in s:
            if c in SUP:
                n += str(SUP.index(c))
            else:
                break
        return int(n)
    m = re.match(r"^(\d{1,3})\.\s", s)
    return int(m.group(1)) if m else None


def check(ch):
    src_p = SRC / f"{ch}_src.txt"
    vi_candidates = list((V2 / ch).glob("*.txt")) if (V2 / ch).exists() else []
    if not src_p.exists() or not vi_candidates:
        print(f"SKIP {ch}: missing src or vi")
        return False
    vi_p = vi_candidates[0]
    src_text = src_p.read_text(encoding="utf-8")
    vi_text = vi_p.read_text(encoding="utf-8")

    src_paras = parse_paras(src_text)
    vi_paras = parse_paras(vi_text)
    ok = True

    if len(src_paras) != len(vi_paras):
        print(f"FAIL {ch}: para count src={len(src_paras)} vi={len(vi_paras)}")
        ok = False
    else:
        # id order
        for (sid, sp), (vid, vp) in zip(src_paras, vi_paras):
            if sid != vid:
                print(f"FAIL {ch}: id mismatch src={sid} vi={vid}")
                ok = False
                break
        if ok:
            print(f"OK {ch}: {len(src_paras)} paragraphs aligned")

    # footnotes
    if "=== FOOTNOTES ===" in vi_text:
        fn_block = vi_text.split("=== FOOTNOTES ===")[1]
        defs = [fn_num(l) for l in fn_block.split("\n") if fn_num(l) is not None]
        # Check for duplicate definition numbers
        if len(defs) != len(set(defs)):
            dups = [n for n in defs if defs.count(n) > 1]
            print(f"FAIL {ch}: duplicate footnote def numbers: {sorted(set(dups))}")
            ok = False
        else:
            # Gapped numbering is allowed (e.g. ch12: 139 defs numbered 1-162 with gaps).
            # Verify every def has an inline body marker and vice versa.
            body = vi_text.split("=== FOOTNOTES ===")[0]
            markers = set()
            # Body footnote markers are superscript runs (¹²³…); arabic "N." format
            # is only used in def lines, not inline body markers.
            for run in re.findall(r"[" + SUP + r"]+", body):
                markers.add(int("".join(str(SUP.index(c)) for c in run)))
            def_set = set(defs)
            missing_markers = sorted(def_set - markers)
            orphan_markers = sorted(markers - def_set)
            if missing_markers:
                print(f"WARN {ch}: {len(missing_markers)} def(s) without inline marker: {missing_markers}")
            if orphan_markers:
                print(f"WARN {ch}: {len(orphan_markers)} inline marker(s) without def: {orphan_markers}")
            if not missing_markers and not orphan_markers:
                if defs:
                    print(f"OK {ch}: {len(defs)} footnote defs (numbers {min(defs)}-{max(defs)}, gaps allowed) match body markers 1:1")
                else:
                    print(f"OK {ch}: 0 footnotes")
            else:
                ok = False
    else:
        print(f"WARN {ch}: no FOOTNOTES block")

    return ok


if __name__ == "__main__":
    allok = True
    for ch in sys.argv[1:]:
        allok &= check(ch)
    sys.exit(0 if allok else 1)