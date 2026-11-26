# -*- coding: utf-8 -*-
"""
Recover missing inline footnote markers in a Phase C v2 file using the original
per-part translation files (backup_.../chNN/_p*.txt), which still carry the
markers that the v1 consolidation dropped.

v2 body uses NEW 1..N numbering; part files use REAL numbering. This script:
  - reads the v2 file's FOOTNOTES block to recover the real->new map
    (real number = the original superscript on each def line is already
    renumbered, so we instead recompute the map from the part files' real set)
  - for each missing NEW marker, finds the REAL marker in the part file,
    grabs a normalized anchor (text before the marker), locates that anchor in
    the v2 body, and inserts the NEW superscript marker right after the anchor.
  - reports matched / unmatched so nothing is fabricated silently.

Usage: python 99_scripts/recover_markers.py ch08 ch11
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "04_translation" / "v2"
V1 = ROOT / "04_translation" / "v1"
BACKUP = ROOT / "backup_20261125_171239"
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def to_sup(n):
    return "".join(SUP[int(d)] for d in str(n))


def sup_runs(text):
    out = []
    for m in re.finditer(r"[" + SUP + r"]+", text):
        out.append(int("".join(str(SUP.index(c)) for c in m.group(0))))
    return out


def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def norm_to_raw_index(raw, nidx):
    """Map an index in norm(raw) back to an index in raw."""
    count = 0
    prev_space = False
    started = False
    for i, c in enumerate(raw):
        if c.isspace():
            if started and not prev_space:
                if count == nidx:
                    return i
                count += 1
                prev_space = True
            continue
        prev_space = False
        started = True
        if count == nidx:
            return i
        count += 1
    return len(raw)


def real_def_numbers(ch):
    """Real footnote numbers as parsed from the v1 file's inline definition
    lines (same logic/order map_v1_to_v2.py used to reindex to 1..N)."""
    raw = (V1 / ch / f"v1_{ch}_vi.txt").read_text(encoding="utf-8")
    SUP_SET = set(SUP)
    def defnum(s):
        s = s.strip()
        if not s:
            return None
        if s[0] in SUP_SET:
            r = ""
            for c in s:
                if c in SUP_SET:
                    r += c
                else:
                    break
            return int("".join(str(SUP.index(c)) for c in r))
        m = re.match(r"^(\d{1,3})\.\s+\S", s)
        return int(m.group(1)) if m else None
    defs = []
    expect = 1
    for line in raw.split("\n"):
        n = defnum(line)
        if n is not None and n >= expect:
            defs.append(n)
            expect = n + 1
    # dedup keep order, then ascending = reindex order
    seen = {}
    for n in defs:
        seen.setdefault(n, None)
    return sorted(seen.keys())


def collect_real_markers(ch):
    """Return dict real_num -> list of candidate anchor strings (normalized).
    A marker may sit mid-paragraph (anchor = text before) or at a paragraph
    start right after a definition line (anchor = text after). We capture both
    before- and after-context so the matcher can try each."""
    anchors = {}
    for f in sorted((BACKUP / ch).glob("_p*.txt")):
        t = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"[" + SUP + r"]+", t):
            real = int("".join(str(SUP.index(c)) for c in m.group(0)))
            before = norm(t[max(0, m.start() - 80):m.start()])
            after = norm(t[m.end():m.end() + 80])
            cand = []
            if before:
                cand.append(before)
            if after:
                cand.append(after)
            anchors.setdefault(real, [])
            for c in cand:
                if c not in anchors[real]:
                    anchors[real].append(c)
    return anchors


def build_real_order(ch, v2_text):
    return real_def_numbers(ch)


def recover(ch):
    v2_path = V2 / ch / f"v1_{ch}_vi.txt"
    text = v2_path.read_text(encoding="utf-8")
    body, sep, fnblock = text.partition("=== FOOTNOTES ===")
    if not sep:
        print(f"{ch}: NO FOOTNOTES BLOCK")
        return

    # new markers present in body
    present = set(sup_runs(body))
    n_new = len(re.findall(r"(?m)^[" + SUP + r"]+", fnblock)) or len(fnblock.strip().splitlines())
    missing_new = [n for n in range(1, n_new + 1) if n not in present]
    if not missing_new:
        print(f"{ch}: no missing markers")
        return

    anchors = collect_real_markers(ch)
    real_order = real_def_numbers(ch)
    r2n = {real: i + 1 for i, real in enumerate(real_order)}

    matched, unmatched = [], []
    para_re = re.compile(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang \d+\)\n(.*)$")
    new_body = body
    for nn in missing_new:
        real = next((r for r, nw in r2n.items() if nw == nn), None)
        if real is None or real not in anchors:
            unmatched.append(nn)
            continue
        marker = to_sup(nn)
        placed = False
        # candidates alternate: [before, after, before, after, ...] per marker
        for ci, anchor in enumerate(anchors[real]):
            anchor = norm(anchor)
            key = anchor[-50:] if len(anchor) > 50 else anchor
            insert_after = (ci % 2 == 0)  # even index = before-context
            for pm in para_re.finditer(new_body):
                seg = pm.group(2)
                if marker in seg:
                    placed = True
                    break
                idx = seg.find(key)
                if idx < 0:
                    nseg = norm(seg)
                    nidx = nseg.find(key)
                    if nidx < 0:
                        continue
                    raw_pos = norm_to_raw_index(seg, nidx + (len(key) if insert_after else 0))
                else:
                    raw_pos = idx + (len(key) if insert_after else 0)
                new_seg = seg[:raw_pos] + marker + seg[raw_pos:]
                new_body = new_body[:pm.start(2)] + new_seg + new_body[pm.end(2):]
                placed = True
                matched.append(nn)
                break
            if placed:
                break
        if not placed:
            unmatched.append(nn)

    out = new_body + sep + fnblock
    out = unicodedata.normalize("NFC", out)
    with open(v2_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"{ch}: recovered={matched} UNMATCHED={unmatched}")


if __name__ == "__main__":
    for ch in sys.argv[1:]:
        recover(ch)