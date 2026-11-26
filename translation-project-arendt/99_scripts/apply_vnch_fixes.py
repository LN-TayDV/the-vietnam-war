# -*- coding: utf-8 -*-
"""
Apply VNCH orthography/connective normalization (STYLE_GUIDE_PHAN_B v2.3)
to a chapter's v2 Vietnamese file, preserving UTF-8/NFC/no-BOM/LF.

Usage:
    python 99_scripts/apply_vnch_fixes.py ch04 [ch05 ...]

Only body text is touched; the === FOOTNOTES === block is left intact.
Connective rules (Rule 25) are applied only to genuine connective usage;
comparative-degree "hơn nữa" (= "even more") is intentionally preserved.
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "04_translation" / "v2"

# Unambiguous orthography replacements (whole-word, case-sensitive for proper forms).
ORTHO = [
    (r"\bchính phủ\b", "chánh phủ"),
    (r"\bChính phủ\b", "Chánh phủ"),
    (r"\bchính trị\b", "chánh trị"),
    (r"\bChính trị\b", "Chánh trị"),
    (r"\btài chính\b", "tài chánh"),
    (r"\bTài chính\b", "Tài chánh"),
    (r"\bmặc dù\b", "mặc dầu"),
    (r"\bMặc dù\b", "Mặc dầu"),
    (r"\bngược lại\b", "trái lại"),
    (r"\bNgược lại\b", "Trái lại"),
    (r"\btuy nhiên\b", "tuy vậy"),
    (r"\bTuy nhiên\b", "Tuy vậy"),
    (r"\bgửi\b", "gởi"),
    (r"\bGửi\b", "Gởi"),
]

# Connective "hơn nữa" -> "vả lại" ONLY when used as sentence-initial connective
# (followed by a comma and a clause), never as comparative degree.
CONNECTIVE = [
    (r"(?m)(^|[.!?]\s+)hơn nữa,\s*", r"\1vả lại, "),
]


def fix_text(t: str) -> str:
    body, sep, fn = t.partition("=== FOOTNOTES ===")
    for pat, rep in ORTHO:
        body = re.sub(pat, rep, body)
    for pat, rep in CONNECTIVE:
        body = re.sub(pat, rep, body)
    return body + sep + fn


def process(ch: str):
    p = V2 / ch / "v1_ch04_vi.txt" if ch == "ch04" else V2 / ch / f"v1_{ch}_vi.txt"
    if not p.exists():
        # fallback naming
        cand = list((V2 / ch).glob("*.txt"))
        if not cand:
            print(f"SKIP {ch}: no file")
            return
        p = cand[0]
    raw = p.read_text(encoding="utf-8")
    before = raw
    after = unicodedata.normalize("NFC", fix_text(raw))
    if after != before:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(after)
        print(f"FIXED {p} ({sum(1 for a,b in zip(before,after) if a!=b)} char diffs)")
    else:
        print(f"OK {p} (no change)")


if __name__ == "__main__":
    for ch in sys.argv[1:]:
        process(ch)