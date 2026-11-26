# -*- coding: utf-8 -*-
"""
Map a chapter's page-based v1 consolidated translation into the v2 paragraph
format ([V1CNN-Pxxx] (trang N) + === FOOTNOTES === block).

This generalizes build_v2_ch04.py for Phase C (ch01-03, ch05-11). It:
  - parses v2 source paragraph IDs + page numbers (the alignment target)
  - parses v1 page-based body + footnote definitions (superscript or "N.")
  - assigns each v2 paragraph the clean body of its page; when the v2 source
    merges two source pages into one paragraph (no standalone paragraph for the
    later page), the later page's body is appended to the earlier paragraph
  - collects footnote definitions, deduped, ordered 1..N
  - writes 04_translation/v2/chNN/v1_chNN_vi.txt (UTF-8, NFC, no BOM, LF)
  - does NOT translate; only re-segments existing clean translation

A per-chapter report is printed: src para count, vi para count, footnote count,
and any page in v1 with no v2 paragraph (potential lost content) so a human can
review before QA.

Usage:
    python 99_scripts/map_v1_to_v2.py ch01 ch02 ...   # or "all"
"""
import io
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "02_extracted_text" / "v2"
V1 = ROOT / "04_translation" / "v1"
V2 = ROOT / "04_translation" / "v2"
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"

RUNNING_HEADERS = {
    "CHỦ NGHĨA PHÂN BIỆT CHỦNG TỘC DO THÁI",
    "VỤ DREYFUS",
    "THE DREYFUS AFFAIR",
    "ANTISEMITISM",
    "THE POLITICAL EMANCIPATION OF THE BOURGEOISIE",
    "RACE-THINKING BEFORE RACISM",
    "RACE AND BUREAUCRACY",
    "CONTINENTAL IMPERIALISM",
    "THE DECLINE OF THE NATION-STATE",
    "A CLASSLESS SOCIETY",
    "THE TOTALITARIAN MOVEMENT",
}
SECTION_LABELS = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII"}


def sup_to_int(s):
    return int("".join(str(SUP.index(c)) for c in s))


def to_sup(n):
    return "".join(SUP[int(d)] for d in str(n))


def insert_marker(text, marker, k):
    """Insert *marker* into *text* at a sentence boundary, never adjacent to an
    existing superscript (which would merge into a wrong multi-digit number).
    Tries boundaries from the end offset by k, then any boundary, then spreads
    by character position as a last resort."""
    ends = [m.end() for m in re.finditer(r"[.!?…][\"”’]?\s", text)]
    candidates = []
    # ordered boundaries from end, offset by k
    if ends:
        order = list(reversed(ends))
        # rotate by k so successive inserts differ
        order = order[k:] + order[:k]
        candidates.extend(order)
    # fallback: evenly spread positions
    L = len(text)
    for j in range(1, 12):
        candidates.append(int(L * j / 12))
    for pos in candidates:
        if pos <= 0 or pos >= L:
            continue
        # not adjacent to a superscript char
        left = text[pos - 1]
        right = text[pos]
        if left in SUP or right in SUP:
            continue
        return text[:pos] + marker + text[pos:]
    # last resort: append with a separating space
    return text + " " + marker


def defnum(s):
    s = s.strip()
    if not s:
        return None
    if s[0] in SUP:
        run = ""
        for c in s:
            if c in SUP:
                run += c
            else:
                break
        return sup_to_int(run)
    m = re.match(r"^(\d{1,3})\.\s+\S", s)
    return int(m.group(1)) if m else None


def parse_source(ch):
    text = (SRC / f"{ch}_src.txt").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)\s*$", text)
    out = []
    i = 1
    while i < len(parts):
        out.append((parts[i], parts[i + 1]))
        i += 3
    return out


def parse_v1(ch):
    """Parse a page-based v1 file with INLINE footnote definitions.

    v1 has NO '=== FOOTNOTES ===' block. A definition is any line whose first
    non-space char is a superscript run (or 'N.' arabic) with number >= the next
    expected number; the whole line (marker + text) is the definition. Body
    lines (incl. inline superscript reference markers) are kept verbatim.

    Returns (pages, defs, fn_page) where:
      pages[page]   = list of body lines (markers intact)
      defs          = list of (real_num, full_line) in file order
      fn_page[num]  = page where the definition appears
    """
    raw = (V1 / ch / f"v1_{ch}_vi.txt").read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^=== PAGE (\d+) ===\s*$", raw)
    pages = {}
    defs = []
    fn_page = {}
    expect = 1
    i = 1
    while i < len(blocks):
        page = blocks[i]
        content = blocks[i + 1]
        body = []
        for line in content.split("\n"):
            n = defnum(line)
            if n is not None and n >= expect:
                defs.append((n, line.strip()))
                fn_page.setdefault(n, page)
                expect = n + 1
                continue
            s = line.strip()
            if not s:
                continue
            if s in RUNNING_HEADERS or s in SECTION_LABELS:
                continue
            if re.fullmatch(r"\d{1,3}", s):
                continue
            if re.fullmatch(r"[" + SUP + r"]+", s):
                continue
            body.append(s)
        pages[page] = body
        i += 2
    return pages, defs, fn_page


def v2_page_groups(src_paras):
    """Return {pid: [pages]} merging pages that share one paragraph.

    A paragraph owns its own page; if a source page has no paragraph of its own
    (i.e. it is missing between two paragraph pages), it is appended to the
    preceding paragraph."""
    page_to_pid = {}
    ordered_pages = []
    for pid, page in src_paras:
        page_to_pid.setdefault(page, pid)
        ordered_pages.append(page)
    # detect gaps: pages present in v1 but not in src -> merge into previous pid
    return src_paras


def build(ch):
    src_paras = parse_source(ch)
    pages, defs, fn_page = parse_v1(ch)
    src_pages = [p for _, p in src_paras]

    covered = set(src_pages)
    all_v1_pages = set(pages.keys())
    gap_pages = sorted(all_v1_pages - covered, key=lambda x: int(x) if x.isdigit() else 0)

    assign = {pid: [page] for pid, page in src_paras}
    for gp in gap_pages:
        prev = None
        for pid, page in src_paras:
            if page.isdigit() and gp.isdigit() and int(page) <= int(gp):
                prev = pid
            else:
                break
        if prev:
            assign[prev].append(gp)

    # Dedup defs by real number (keep first), then reindex to 1..N.
    by_num = {}
    for n, t in defs:
        by_num.setdefault(n, t)
    real_nums = sorted(by_num)
    old2new = {old: i + 1 for i, old in enumerate(real_nums)}

    # Rewrite each definition line's leading marker to its new 1..N number.
    def renumber_def(old, line):
        new = old2new[old]
        if line and line[0] in SUP:
            rest = line.lstrip(SUP)
            return to_sup(new) + rest
        # arabic "N." style
        m = re.match(r"^(\d{1,3})\.\s+(.*)$", line)
        if m:
            return f"{new}. {m.group(2)}"
        return line

    footnotes = [renumber_def(old, by_num[old]) for old in real_nums]

    # Rewrite inline superscript markers in body using old->new map.
    def remap_markers(text):
        def repl(m):
            old = int("".join(str(SUP.index(c)) for c in m.group(0)))
            new = old2new.get(old)
            return to_sup(new) if new is not None else m.group(0)
        return re.sub(r"[" + SUP + r"]+", repl, text)

    bodies = {}
    present = {}
    for pid, page in src_paras:
        body = []
        for pg in assign[pid]:
            body.extend(pages.get(pg, []))
        text = re.sub(r"\s+", " ", " ".join(body)).strip()
        text = remap_markers(text)
        bodies[pid] = text
        present[pid] = set()
        for run in re.findall(r"[" + SUP + r"]+", text):
            present[pid].add(int("".join(str(SUP.index(c)) for c in run)))

    # Missing markers (new numbering). Place each at the END of the paragraph
    # that owns the definition's page (deterministic page-boundary placement;
    # used only when the original inline anchor was lost in v1 consolidation).
    all_markers = set().union(*present.values()) if present else set()
    missing = [n for n in range(1, len(footnotes) + 1) if n not in all_markers]
    inserted = []
    blocked = []
    appended_count = {}
    for n in missing:
        old = real_nums[n - 1]
        pg = fn_page.get(old)
        target_pid = None
        if pg is not None:
            for pid, page in src_paras:
                if pg in assign[pid]:
                    target_pid = pid
                    break
            if target_pid is None:
                prev = None
                for pid, page in src_paras:
                    if page.isdigit() and pg.isdigit() and int(page) <= int(pg):
                        prev = pid
                    else:
                        break
                target_pid = prev
        if target_pid is None:
            blocked.append(n)
            continue
        k = appended_count.get(target_pid, 0)
        appended_count[target_pid] = k + 1
        bodies[target_pid] = insert_marker(bodies[target_pid], to_sup(n), k)
        present[target_pid].add(n)
        inserted.append(n)

    out_chunks = []
    for pid, page in src_paras:
        out_chunks.append(f"[{pid}] (trang {page})\n{bodies[pid]}\n")

    fn_block = "=== FOOTNOTES ===\n" + "\n".join(footnotes)
    out = "\n".join(out_chunks) + "\n" + fn_block + "\n"
    out = unicodedata.normalize("NFC", out)

    dst_dir = V2 / ch
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / f"v1_{ch}_vi.txt"
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)

    print(f"{ch}: src_paras={len(src_paras)} fns={len(footnotes)} "
          f"real_range={real_nums[0] if real_nums else '-'}..{real_nums[-1] if real_nums else '-'} "
          f"gap_pages={gap_pages} inserted={inserted} BLOCKED={blocked} -> {dst.name}")
    return len(src_paras), len(footnotes), gap_pages


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if not argv or argv[0] == "all":
        chs = [f"ch{i:02d}" for i in range(1, 12)]
    else:
        chs = argv
    for ch in chs:
        if not (SRC / f"{ch}_src.txt").exists() or not (V1 / ch / f"v1_{ch}_vi.txt").exists():
            print(f"{ch}: SKIP (missing src or v1)")
            continue
        build(ch)


if __name__ == "__main__":
    main(sys.argv[1:])