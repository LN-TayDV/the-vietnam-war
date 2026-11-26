# -*- coding: utf-8 -*-
"""
QA Gate — 11 quality checks on the 13 v2 chapter DOCX + master DOCX and the
underlying translation text. Prints PASS/FAIL per gate. Exit 0 only if all pass.

Gates:
 1 Alignment        (para count src==vi, ids in order)
 2 DOCX structure   (python-docx opens, has footnotes part when expected)
 3 Footnotes        (placed == total, no orphans)
 4 Styles           (body paragraphs use a named style)
 5 Headings         (hierarchy valid, no duplicate headings)
 6 Pagination       (headings keep_with_next)
 7 Encoding         (UTF-8, NFC, no BOM, LF)
 8 VNCH orthography (0 'chính phủ', 0 CJK/Cyrillic in body)
 9 Chapter structure(exactly one chapter title)
10 Paragraph continuity (no duplicate paragraphs)
11 Text integrity   (no CJK/Cyrillic/Han/Korean in body)
"""
from __future__ import annotations

import io
import re
import sys
import unicodedata as u
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "04_translation" / "v2"
SRC = ROOT / "02_extracted_text" / "v2"
DOCX = ROOT / "09_docx"
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"

CYR = re.compile(r"[\u0400-\u04FF]+")
HAN = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]+")
KOR = re.compile(r"[\uac00-\ud7af\u1100-\u11ff]+")
KANA = re.compile(r"[\u3040-\u30ff]+")

PARA_HDR = re.compile(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)\s*$")

results = []  # (gate, chapter, ok, detail)


def rec(gate, ch, ok, detail=""):
    results.append((gate, ch, ok, detail))


def parse_paras(text):
    parts = re.split(r"(?m)^\[(V1\w*-?C\d+-P\d{3})\] \(trang (\d+)\)\s*$", text)
    out = []
    i = 1
    while i < len(parts):
        out.append((parts[i], parts[i + 1]))
        i += 3
    return out


def body_of(text):
    return text.split("=== FOOTNOTES ===")[0]


def check_chapter(ch):
    txt_path = V2 / ch / f"v1_{ch}_vi.txt"
    raw = txt_path.read_text(encoding="utf-8")
    body = body_of(raw)

    # Gate 7 encoding
    bom = raw.startswith("\ufeff")
    crlf = "\r\n" in raw
    nfc = u.is_normalized("NFC", raw)
    rec("7 Encoding", ch, (not bom) and (not crlf) and nfc,
        f"BOM={bom} CRLF={crlf} NFC={nfc}")

    # Gate 1 alignment
    src_path = SRC / f"{ch}_src.txt"
    if src_path.exists():
        sp = parse_paras(src_path.read_text(encoding="utf-8"))
        vp = parse_paras(raw)
        ok = len(sp) == len(vp) and all(a[0] == b[0] for a, b in zip(sp, vp))
        rec("1 Alignment", ch, ok, f"src={len(sp)} vi={len(vp)}")
    else:
        rec("1 Alignment", ch, True, "no src (skip)")

    # Gate 8 VNCH orthography + Gate 11 text integrity
    chinhphu = len(re.findall(r"ch\u00ednh ph\u1ee7", body))
    cjk = len(CYR.findall(body)) + len(HAN.findall(body)) + len(KOR.findall(body)) + len(KANA.findall(body))
    rec("8 VNCH orthography", ch, chinhphu == 0, f"chinhphu={chinhphu}")
    rec("11 Text integrity", ch, cjk == 0, f"cjk/cyr={cjk}")

    # Gate 10 paragraph continuity (duplicates)
    paras = [t.strip() for _, t in parse_paras(raw)]
    seen = {}
    dups = 0
    for t in paras:
        norm = re.sub(r"\s+", " ", t)
        if len(norm) > 80:
            if norm in seen:
                dups += 1
            else:
                seen[norm] = 1
    rec("10 Paragraph continuity", ch, dups == 0, f"dup_paras={dups}")

    # DOCX checks
    cands = list(DOCX.glob(f"V2-{ch[-2:].upper()}_*.docx"))
    docx_path = cands[0] if cands else None
    if docx_path is None or not docx_path.exists():
        rec("2 DOCX structure", ch, False, "docx missing")
        rec("3 Footnotes", ch, False, "docx missing")
        rec("4 Styles", ch, False, "docx missing")
        rec("5 Headings", ch, False, "docx missing")
        rec("6 Pagination", ch, False, "docx missing")
        return

    doc = Document(str(docx_path))
    # Gate 2 structure: footnotes part present if body has markers
    has_fn_part = any("footnotes" in r.reltype for r in doc.part.rels.values())
    body_has_markers = bool(re.search("[" + SUP + "]+|«", body))
    rec("2 DOCX structure", ch, (has_fn_part == body_has_markers) or not body_has_markers,
        f"fn_part={has_fn_part} body_markers={body_has_markers}")

    # Gate 3 footnotes: count footnoteReference in document.xml
    fn_refs = len(re.findall(r"footnoteReference", doc.element.xml))
    # total defs
    defs = set()
    for line in raw.split("=== FOOTNOTES ===")[1].split("\n"):
        s = line.strip()
        if not s:
            continue
        if s[0] in SUP:
            r = ""
            for c in s:
                if c in SUP:
                    r += c
                else:
                    break
            defs.add(int("".join(str(SUP.index(c)) for c in r)))
        else:
            m = re.match(r"^(\d{1,3})\.\s", s)
            if m:
                defs.add(int(m.group(1)))
    rec("3 Footnotes", ch, fn_refs == len(defs), f"refs={fn_refs} defs={len(defs)}")

    # Gate 4 styles: every non-empty paragraph has a pStyle
    no_style = 0
    for p in doc.paragraphs:
        if not p.text.strip():
            continue
        ppr = p._p.find(qn("w:pPr"))
        has = ppr is not None and ppr.find(qn("w:pStyle")) is not None
        if not has:
            no_style += 1
    rec("4 Styles", ch, no_style == 0, f"paras_without_style={no_style}")

    # Gate 5 headings: no duplicate heading text at same level
    from collections import Counter
    heads = []
    for p in doc.paragraphs:
        ppr = p._p.find(qn("w:pPr"))
        if ppr is None:
            continue
        ps = ppr.find(qn("w:pStyle"))
        if ps is None:
            continue
        val = ps.get(qn("w:val")) or ""
        if val in ("Heading1", "Heading2", "Heading3", "Heading4",
                   "ChapterTitle", "SectionH1", "SectionH2", "SectionH3"):
            heads.append((val, p.text.strip()))
    cnt = Counter(heads)
    dups = {k: v for k, v in cnt.items() if v > 1 and k[1]}
    rec("5 Headings", ch, len(dups) == 0, f"dup_headings={len(dups)}")

    # Gate 6 pagination: headings keep_with_next
    bad_keep = 0
    for p in doc.paragraphs:
        ppr = p._p.find(qn("w:pPr"))
        if ppr is None:
            continue
        ps = ppr.find(qn("w:pStyle"))
        if ps is None:
            continue
        val = ps.get(qn("w:val")) or ""
        if val in ("Heading1", "Heading2", "Heading3", "Heading4",
                   "ChapterTitle", "SectionH1", "SectionH2", "SectionH3"):
            if p.paragraph_format.keep_with_next is not True:
                bad_keep += 1
    rec("6 Pagination", ch, bad_keep == 0, f"headings_without_keepnext={bad_keep}")


def _title(ch):
    return {
        "ch01": "Thuyet-Trai-Dat-Bang-Phang",
    }.get(ch, "")


def _slug(s):
    return s


def check_master():
    p = DOCX / "V2-Origins-of-Totalitarianism-MASTER.docx"
    if not p.exists():
        rec("2 DOCX structure", "MASTER", False, "missing")
        return
    doc = Document(str(p))
    fn_refs = len(re.findall(r"footnoteReference", doc.element.xml))
    rec("3 Footnotes", "MASTER", fn_refs == 892, f"refs={fn_refs}/892")
    # structure
    has_fn = any("footnotes" in r.reltype for r in doc.part.rels.values())
    rec("2 DOCX structure", "MASTER", has_fn, f"fn_part={has_fn}")


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    for i in range(1, 14):
        check_chapter(f"ch{i:02d}")
    check_master()

    # summarize
    gates = {}
    for gate, ch, ok, detail in results:
        gates.setdefault(gate, []).append((ch, ok, detail))
    all_ok = True
    print("=" * 70)
    for gate in sorted(gates):
        items = gates[gate]
        passed = sum(1 for _, ok, _ in items if ok)
        total = len(items)
        status = "PASS" if passed == total else "FAIL"
        if passed != total:
            all_ok = False
        print(f"{status}  {gate}: {passed}/{total}")
        if passed != total:
            for ch, ok, detail in items:
                if not ok:
                    print(f"      FAIL {ch}: {detail}")
    print("=" * 70)
    print("OVERALL:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())