# -*- coding: utf-8 -*-
"""
Build a print-ready DOCX for each completed chapter translation.

Input : 04_translation/v1/chNN/v1_chNN_vi.txt   (translation, source of truth)
        02_extracted_text/v1/chNN.txt           (English source, footnote anchoring)
Output: 09_docx/V1-CNN_<slug>.docx

Footnotes are real Word footnotes: they flow to the bottom of the page on
which their reference appears, 9 pt, with a hanging number, like a printed book.

Usage:
    python 99_scripts/build_chapter_docx.py                # all chapters
    python 99_scripts/build_chapter_docx.py 01 03          # selected chapters
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from xml.sax.saxutils import escape

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor

PROJECT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT / "04_translation" / "v1"
EN_DIR = PROJECT / "02_extracted_text" / "v1"
OUT_DIR = PROJECT / "09_docx"

BOOK_TITLE = "The Cambridge History of the Vietnam War"
VOLUME_LABEL = "TẬP I — ORIGINS · NGUỒN CỘI"

VOLUME_EN_TITLES = {
    "V1-C01": "Memory, Tradition, and the History of “Vietnam”",
    "V1-C02": "The Origins of the Vietnamese Revolution",
    "V1-C03": "Hồ Chí Minh and the Rise of the Vietnamese Communist Party",
    "V1-C04": "Indochina during World War II",
}

VI_TITLES = {
    "V1-C02": "Nguồn cội của Cách mạng Việt Nam",
}

SECTION_VI = {
    ("V1-C04", "Watersheds"): "Những Bước Ngoặt",
}

SERIF = "Times New Roman"
INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x55, 0x55, 0x55)
RULE = "BFBFBF"

P_HDR = re.compile(r"^--- \[([A-Za-z0-9]+-P\d+)\] \(trang ([^)]+)\)(?: — (.*?))? ---$")
N_HDR = re.compile(r"^--- \[Cước chú (.*?)\] ---$")
FN_BRACKET = re.compile(r"^\[(\d+)\]\s*(.*)$")
FN_BARE = re.compile(r"^(\d+)\s+(?=\S)(.*)$")

ND_SPAN = re.compile(r"\[ND:[^\]]*\]")
INLINE = re.compile(
    r"(\[ND:[^\]]*\])"          # translator note
    r"|(\[[0-9]{1,3}\])"        # footnote reference (fallback)
    r"|(_[^_\n]+_)"             # _italic_
    r"|(\*[^*\n]+\*)"           # *italic*
)
# Footnote markers still embedded in the translation body:
#   [12]   (ch01 style)   or   12 appended to a word (ch02 style)
MARKER = re.compile(r"\[(\d{1,3})\]|(?<=[^\s\d])(\d{1,3})(?=\s|$)")


# ---------------------------------------------------------------- helpers
def set_run_font(run, size=None, bold=None, italic=None, color=None,
                 caps=False, spacing=None):
    run.font.name = SERIF
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), SERIF)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    if caps:
        run.font.all_caps = True
    if spacing is not None:  # character spacing in twentieths of a point
        el = OxmlElement("w:spacing")
        el.set(qn("w:val"), str(spacing))
        rpr.append(el)


def add_rule(paragraph, size=6, color=RULE, space=6):
    ppr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), str(space))
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    ppr.append(borders)


def add_text_runs(paragraph, text, size=12.0, color=INK, markup=True):
    """Render inline markers: [ND: ...], _/_*_ italics, leftover refs."""
    if not markup:
        run = paragraph.add_run(text)
        set_run_font(run, size=size, color=color)
        return
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            run = paragraph.add_run(text[pos:m.start()])
            set_run_font(run, size=size, color=color)
        if m.group(1):                        # [ND: ...]
            run = paragraph.add_run(m.group(0))
            set_run_font(run, size=size - 1, italic=True, color=MUTED)
        elif m.group(2):                      # stray [12] -> superscript
            run = paragraph.add_run(m.group(2)[1:-1])
            set_run_font(run, size=size - 2, color=MUTED)
            run.font.superscript = True
        else:                                 # italics
            run = paragraph.add_run(m.group(0)[1:-1])
            set_run_font(run, size=size, italic=True, color=color)
        pos = m.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        set_run_font(run, size=size, color=color)


def para_fmt(p, first_indent=0.0, space_before=0, space_after=6,
             line=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, keep_next=False,
             keep_together=False):
    pf = p.paragraph_format
    pf.first_line_indent = Cm(first_indent)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    pf.alignment = align
    pf.keep_with_next = keep_next
    pf.keep_together = keep_together
    pf.widow_control = True
    return p


def add_field(paragraph, instr):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar"); begin.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = instr
    sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t"); txt.text = "1"
    end = OxmlElement("w:fldChar"); end.set(qn("w:fldCharType"), "end")
    for el in (begin, it, sep, txt, end):
        run._r.append(el)
    set_run_font(run, size=9, color=MUTED)


def slugify(text, limit=70):
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "D")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")
    return text[:limit].rstrip("-")


# ---------------------------------------------------------------- parse
def parse_chapter(path):
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    lines = raw.split("\n")

    header = lines[0].strip().strip("=").strip()
    parts = [p.strip() for p in header.split("·")]
    chap_id, title = parts[0], parts[1]
    author = parts[2] if len(parts) > 2 else ""

    meta, i = [], 1
    while i < len(lines) and not lines[i].startswith("--- ["):
        s = lines[i].strip()
        if s and not s.startswith("Sửa Giai đoạn"):
            meta.append(s)
        i += 1

    blocks, cur = [], None
    for line in lines[i:]:
        if line.startswith("--- ["):
            cur = {"header": line.strip(), "lines": []}
            blocks.append(cur)
        elif cur is not None:
            cur["lines"].append(line)

    notes, items = {}, []
    for b in blocks:
        h = b["header"]
        if N_HDR.match(h):
            for line in b["lines"]:
                s = line.strip()
                if not s:
                    continue
                m = FN_BRACKET.match(s) or FN_BARE.match(s)
                if m:
                    num = int(m.group(1))
                    text = m.group(2).strip()
                    notes.setdefault(num, text)   # drop exact duplicates
                else:
                    # wrapped continuation of the previous note
                    if notes:
                        last = max(notes)
                        if notes[last]:
                            notes[last] += " " + s
            continue

        m = P_HDR.match(h)
        if not m:
            continue
        label = (m.group(3) or "").strip()
        page = int(re.match(r"\d+", m.group(2)).group())
        chunks, buf = [], []
        for line in b["lines"]:
            if line.strip():
                buf.append(line.strip())
            elif buf:
                chunks.append(" ".join(buf))
                buf = []
        if buf:
            chunks.append(" ".join(buf))
        if label.lower() == "đề mục" and chunks:
            items.append({"kind": "heading", "text": chunks.pop(0)})
            label = ""
        elif label:
            if label.lower().startswith("phần introduction"):
                label = "Dẫn nhập"
            label = SECTION_VI.get((chap_id, label), label)
            items.append({"kind": "heading", "text": label})
        for text in chunks:
            items.append({"kind": "para", "text": text, "page": page})

    return {"id": chap_id, "title": title, "author": author,
            "meta": meta, "items": items, "notes": notes}


# ------------------------------------------------- footnote placement (A)
def extract_inline_markers(items, notes):
    """Use markers already present in the translation body. Returns
    {item_index: [(offset, note_number), ...]} and cleaned texts, or None."""
    target = max(notes) if notes else 0
    expect, marks = 1, {}
    texts = {}
    for idx, it in enumerate(items):
        if it["kind"] != "para":
            continue
        text = it["text"]
        masked = ND_SPAN.sub(lambda m: " " * len(m.group(0)), text)
        out, last, local = [], 0, []
        for m in MARKER.finditer(masked):
            num = int(m.group(1) or m.group(2))
            if num != expect:
                continue
            out.append(text[last:m.start()])
            local.append((sum(len(x) for x in out), num))
            last = m.end()
            expect += 1
        if local:
            out.append(text[last:])
            texts[idx] = "".join(out)
            marks[idx] = local
    if expect - 1 != target:
        return None
    cleaned = [dict(it) for it in items]
    for idx, t in texts.items():
        cleaned[idx]["text"] = t
    return cleaned, marks


# ------------------------------------------------- footnote placement (B)
FN_LINE = re.compile(r"^\s*(\d{1,3})\s*\t\s*(.*)$")
PAGE_NO = re.compile(r"^\s*(\d{1,3})\s*$")


def _join_lines(body_lines, title, author):
    keep = []
    for l in body_lines:
        s = l.strip()
        if s in (title, author) or re.fullmatch(r"\d{1,3}", s):
            continue
        keep.append(s)
    if not keep:
        return ""
    out = keep[0]
    for l in keep[1:]:
        if out.endswith("-") and l[:1].islower():
            out = out[:-1] + l
        else:
            out += " " + l
    return out


def source_path(chap_id):
    """V1-C05 -> 02_extracted_text/v1/ch05.txt (same rule for V2/V3)."""
    vol, no = chap_id[1], chap_id[-2:]
    path = PROJECT / "02_extracted_text" / f"v{vol}" / f"ch{no}.txt"
    return path if path.exists() else None


def parse_source_pages(chap_id, first, last, title, author):
    path = source_path(chap_id)
    if path is None:
        return None
    lines = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")
    starts = {}
    for i, l in enumerate(lines):
        m = PAGE_NO.match(l)
        if m and first <= int(m.group(1)) <= last:
            starts.setdefault(int(m.group(1)), i)
    if not starts:
        return None
    pages = []
    for page, i in sorted(starts.items()):
        body, notes, cur, in_notes, j = [], {}, None, False, i + 1
        while j < len(lines):
            l = lines[j]
            m = PAGE_NO.match(l)
            if m and j > i + 1 and int(m.group(1)) in starts:
                break
            fm = FN_LINE.match(l)
            if fm and (not in_notes or int(fm.group(1)) == (max(notes) + 1 if notes else 1)):
                in_notes, cur = True, int(fm.group(1))
                notes[cur] = fm.group(2).strip()
                j += 1
                continue
            if in_notes:
                s = l.strip()
                if not s:
                    j += 1
                    continue
                if s in (title, author):
                    break
                if cur is not None:
                    notes[cur] = (notes[cur] + " " + s).strip()
                j += 1
                continue
            body.append(l)
            j += 1
        pages.append({"page": page,
                      "text": _join_lines(body, title, author),
                      "notes": notes})
    return pages


def source_page_markers(pages, total):
    """Sequential footnote markers inside the English body, as page ratios."""
    expect, out = 1, []
    for p in pages:
        text = p["text"]
        if not text:
            continue
        for m in re.finditer(r"(?<=[^\s\d])(\d{1,3})(?=\s|$)", text):
            num = int(m.group(1))
            if num != expect:
                continue
            out.append({"num": num, "page": p["page"],
                        "ratio": m.start() / max(len(text), 1)})
            expect += 1
    return out if expect - 1 == total else None


def _sentence_positions(text):
    # insert right after the punctuation (and closing quote), not after the
    # following space, so the reference sits tight against the sentence.
    return [m.start() + len(m.group(0).rstrip())
            for m in re.finditer(r'[.!?…]["”’]?\s', text)]


def _adjust_offset(text, off, prev=0):
    """Snap to a safe insertion point: outside markup and words."""
    off = max(prev, min(off, len(text)))
    for m in INLINE.finditer(text):
        if m.start() < off < m.end():
            off = m.end()
    if 0 < off < len(text) and text[off - 1].isalnum() and text[off].isalnum():
        nxt = re.search(r"[\s]", text[off:])
        off = off + nxt.start() if nxt else len(text)
    return off


def snap_to_sentence(text, off, prev=0):
    off = _adjust_offset(text, off, prev)
    positions = [x for x in _sentence_positions(text) if x >= prev]
    if not positions:
        return off
    near = min(positions, key=lambda x: abs(x - off))
    return near if abs(near - off) <= 160 else off


def source_placements(items, chap, notes):
    pages_src = parse_source_pages(chap["id"],
                                   min(p["page"] for p in items if p["kind"] == "para"),
                                   max(p["page"] for p in items if p["kind"] == "para"),
                                   chap["title"], chap["author"])
    if not pages_src:
        return None
    mark_list = source_page_markers(pages_src, max(notes))
    if not mark_list:
        return None

    # Group translation paragraphs by the page they start on.
    by_page, order = {}, []
    for idx, it in enumerate(items):
        if it["kind"] != "para":
            continue
        by_page.setdefault(it["page"], []).append(idx)
        order.append(idx)

    marks, prev_by_para = {}, {}
    for mk in mark_list:
        group = by_page.get(mk["page"])
        if not group:
            earlier = [p for p in by_page if p < mk["page"]]
            group = by_page[max(earlier)] if earlier else [order[-1]]
        total_len = sum(len(items[i]["text"]) for i in group)
        target = mk["ratio"] * max(total_len - 1, 0)
        acc, chosen, local = 0, group[-1], 0
        for i in group:
            L = len(items[i]["text"])
            if target <= acc + L or i == group[-1]:
                chosen, local = i, int(round(target - acc))
                break
            acc += L
        text = items[chosen]["text"]
        off = snap_to_sentence(text, local, prev_by_para.get(chosen, 0))
        marks.setdefault(chosen, []).append((off, mk["num"]))
        prev_by_para[chosen] = off
    if sum(len(v) for v in marks.values()) != max(notes):
        return None
    # De-duplicate: two markers landing on the same offset inside one paragraph
    # would overlap in the DOCX.  Push later markers forward to the next safe
    # sentence boundary so every footnote reference stays visually separate.
    for idx, lst in marks.items():
        lst.sort()
        text = items[idx]["text"]
        prev = 0
        for i, (off, num) in enumerate(lst):
            if off <= prev:
                off = snap_to_sentence(text, prev + 1, prev)
            lst[i] = (off, num)
            prev = off
    return marks


def plan_footnotes(chap):
    notes = chap["notes"]
    inline = extract_inline_markers(chap["items"], notes)
    if inline:
        items, marks = inline
        return items, marks, "inline"
    marks = source_placements(chap["items"], chap, notes)
    if marks:
        return chap["items"], marks, "source"
    return chap["items"], {}, "none"


# ---------------------------------------------------------------- docx core
def setup_document():
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = SERIF
    normal.font.size = Pt(12)
    normal.font.color.rgb = INK
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), SERIF)
    lang = OxmlElement("w:lang")
    lang.set(qn("w:val"), "vi-VN")
    lang.set(qn("w:eastAsia"), "vi-VN")
    rpr.append(lang)

    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.9)
    section.bottom_margin = Cm(1.8)
    section.left_margin = Cm(2.1)
    section.right_margin = Cm(1.8)
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.0)
    return doc


def start_body_section(doc):
    section = doc.add_section(WD_SECTION.NEW_PAGE)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.9)
    section.bottom_margin = Cm(1.8)
    section.left_margin = Cm(2.1)
    section.right_margin = Cm(1.8)
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.0)

    section.header.is_linked_to_previous = False
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run(f"{BOOK_TITLE} · Tập I")
    set_run_font(run, size=8.5, color=MUTED, italic=True)
    add_rule(header, size=4, space=4)

    section.footer.is_linked_to_previous = False
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run("Trang ")
    set_run_font(run, size=9, color=MUTED)
    add_field(footer, "PAGE")

    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:start"), "1")
    section._sectPr.append(pg)
    return section


def add_title_block(doc, ch):
    eyebrow = doc.add_paragraph()
    para_fmt(eyebrow, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=42,
             space_after=4, line=1.0)
    run = eyebrow.add_run(BOOK_TITLE.upper())
    set_run_font(run, size=10.5, color=MUTED, caps=True, spacing=10)

    vol = doc.add_paragraph()
    para_fmt(vol, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=30, line=1.0)
    run = vol.add_run(VOLUME_LABEL)
    set_run_font(run, size=10.5, italic=True, color=MUTED, caps=True, spacing=20)

    num = doc.add_paragraph()
    para_fmt(num, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10, line=1.0)
    m = re.search(r"(\d+)$", ch["id"])
    run = num.add_run(f"CHƯƠNG {int(m.group(1)) if m else ''}")
    set_run_font(run, size=13, bold=True, color=MUTED, spacing=40)

    vi_title = VI_TITLES.get(ch["id"], ch["title"])
    t = doc.add_paragraph()
    para_fmt(t, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6, line=1.15)
    run = t.add_run(vi_title)
    tsize = 24 if len(vi_title) <= 38 else (21 if len(vi_title) <= 52 else 19)
    set_run_font(run, size=tsize, bold=True, spacing=6)

    en = VOLUME_EN_TITLES.get(ch["id"])
    if en and en.strip().lower() != vi_title.strip().lower():
        sub = doc.add_paragraph()
        para_fmt(sub, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, line=1.1)
        run = sub.add_run(en)
        set_run_font(run, size=12, italic=True, color=MUTED)

    if ch["author"]:
        a = doc.add_paragraph()
        para_fmt(a, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10, line=1.0)
        run = a.add_run(ch["author"])
        set_run_font(run, size=12, italic=True, color=RGBColor(0x33, 0x33, 0x33))

    rule = doc.add_paragraph()
    para_fmt(rule, space_before=6, space_after=12, line=1.0)
    add_rule(rule, size=8, space=1)

    for line in ch["meta"]:
        p = doc.add_paragraph()
        para_fmt(p, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, line=1.1)
        add_text_runs(p, line, size=9, color=MUTED, markup=False)

    start_body_section(doc)


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    para_fmt(p, space_before=14, space_after=6, line=1.15,
             align=WD_ALIGN_PARAGRAPH.LEFT, keep_next=True)
    run = p.add_run(text)
    set_run_font(run, size=13.5, bold=True, color=INK)


def add_footnote_ref(paragraph, fid):
    run = paragraph.add_run()
    rpr = run._r.get_or_add_rPr()
    style = OxmlElement("w:rStyle")
    style.set(qn("w:val"), "FootnoteReference")
    rpr.append(style)
    valign = OxmlElement("w:vertAlign")
    valign.set(qn("w:val"), "superscript")
    rpr.append(valign)
    ref = OxmlElement("w:footnoteReference")
    ref.set(qn("w:id"), str(fid))
    run._r.append(ref)


def add_body_paragraph(doc, text, marks):
    p = doc.add_paragraph()
    para_fmt(p, first_indent=0.9, space_after=6, line=1.3)
    pos = 0
    for off, fid in marks:
        if off > pos:
            add_text_runs(p, text[pos:off], size=12)
        add_footnote_ref(p, fid)
        pos = off
    if pos < len(text):
        add_text_runs(p, text[pos:], size=12)


def add_colophon(doc, ch, words, nparas, nnotes):
    p = doc.add_paragraph()
    para_fmt(p, space_before=22, space_after=4, line=1.0,
             align=WD_ALIGN_PARAGRAPH.CENTER)
    add_rule(p, size=4, space=6)
    num = ch["id"].split("-")[-1]
    run = p.add_run(
        f"Bản dịch tiếng Việt · {ch['id']} · {words:,} từ · {nparas} đoạn · "
        f"{nnotes} cước chú · nguồn: 04_translation/v1/ch{num}/v1_ch{num}_vi.txt"
    )
    set_run_font(run, size=8.5, italic=True, color=MUTED)


# --------------------------------------------------------- Word footnotes
FOOTNOTES_CT = ("application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.footnotes+xml")

STYLE_FOOTNOTE_TEXT = f"""
<w:style {nsdecls('w')} w:type="paragraph" w:styleId="FootnoteText">
  <w:name w:val="footnote text"/>
  <w:basedOn w:val="Normal"/>
  <w:uiPriority w:val="99"/>
  <w:unhideWhenUsed/>
  <w:pPr>
    <w:spacing w:before="0" w:after="0" w:line="230" w:lineRule="auto"/>
    <w:ind w:left="227" w:hanging="227"/>
    <w:jc w:val="both"/>
  </w:pPr>
  <w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
</w:style>
"""

STYLE_FOOTNOTE_REF = f"""
<w:style {nsdecls('w')} w:type="character" w:styleId="FootnoteReference">
  <w:name w:val="footnote reference"/>
  <w:uiPriority w:val="99"/>
  <w:unhideWhenUsed/>
  <w:rPr><w:vertAlign w:val="superscript"/></w:rPr>
</w:style>
"""


def ensure_footnote_styles(doc):
    styles = doc.styles.element
    ids = {s.get(qn("w:styleId")) for s in styles.findall(qn("w:style"))}
    for style_id, xml in (("FootnoteText", STYLE_FOOTNOTE_TEXT),
                          ("FootnoteReference", STYLE_FOOTNOTE_REF)):
        if style_id not in ids:
            styles.append(parse_xml(xml))


def _fn_runs(text):
    """Footnote body runs: 9 pt; *italics* and [ND: ...] in italic grey."""
    base = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    ital = ('<w:rPr><w:i/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>')
    nd = ('<w:rPr><w:i/><w:color w:val="555555"/>'
          '<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>')
    pat = re.compile(r"(\[ND:[^\]]*\])|(_[^_\n]+_)|(\*[^*\n]+\*)")
    out, pos = [], 0

    def run(rpr, txt):
        return (f'<w:r>{rpr}<w:t xml:space="preserve">{escape(txt)}</w:t></w:r>')

    for m in pat.finditer(text):
        if m.start() > pos:
            out.append(run(base, text[pos:m.start()]))
        if m.group(1):
            out.append(run(nd, m.group(1)))
        else:
            out.append(run(ital, m.group(0)[1:-1]))
        pos = m.end()
    if pos < len(text):
        out.append(run(base, text[pos:]))
    return "".join(out)


def install_footnotes(doc, entries):
    """entries: [(word_id, text)] in document order."""
    parts = [
        f'<w:footnotes {nsdecls("w")}>',
        '<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr>'
        '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:r><w:separator/></w:r></w:p></w:footnote>',
        '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr>'
        '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:r><w:continuationSeparator/></w:r></w:p></w:footnote>',
    ]
    for fid, text in entries:
        parts.append(
            f'<w:footnote w:id="{fid}"><w:p>'
            '<w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>'
            '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr>'
            '<w:footnoteRef/></w:r>'
            '<w:r><w:t xml:space="preserve"> </w:t></w:r>'
            + _fn_runs(text) +
            '</w:p></w:footnote>'
        )
    parts.append("</w:footnotes>")
    blob = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            + "".join(parts)).encode("utf-8")
    part = Part(PackURI("/word/footnotes.xml"), FOOTNOTES_CT, blob,
                doc.part.package)
    doc.part.relate_to(part, RT.FOOTNOTES)


# ------------------------------------------------------------------ build
def build(ch_path):
    ch = parse_chapter(ch_path)
    items, placements, mode = plan_footnotes(ch)
    notes = ch["notes"]

    doc = setup_document()
    add_title_block(doc, ch)
    ensure_footnote_styles(doc)

    next_id, entries, words, nparas = 1, [], 0, 0
    for idx, it in enumerate(items):
        if it["kind"] == "heading":
            add_section_heading(doc, it["text"])
            continue
        marks = []
        for off, num in sorted(placements.get(idx, [])):
            if num in notes:
                marks.append((off, next_id))
                entries.append((next_id, notes[num]))
                next_id += 1
        add_body_paragraph(doc, it["text"], marks)
        words += len(it["text"].split())
        nparas += 1

    add_colophon(doc, ch, words, nparas, len(entries))
    if entries:
        install_footnotes(doc, entries)

    props = doc.core_properties
    props.title = f"{ch['id']} — {VI_TITLES.get(ch['id'], ch['title'])}"
    props.subject = BOOK_TITLE
    props.author = ch["author"] or "Bản dịch tiếng Việt"
    props.language = "vi-VN"
    props.comments = "Bản dịch tiếng Việt (chuẩn ngôn ngữ miền Nam)"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{ch['id']}_{slugify(ch['title'])}.docx"
    tmp = OUT_DIR / f".tmp_{ch['id']}_{slugify(ch['title'])}.docx"
    if tmp.exists():
        tmp.unlink()
    doc.save(tmp)
    if out.exists():
        out.unlink()
    tmp.rename(out)
    return out, words, len(entries), mode, len(notes)


def main(argv):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    wanted = {a.zfill(2) for a in argv if a.strip().isdigit()}
    paths = sorted(SRC_DIR.glob("ch*/v1_ch*_vi.txt"))
    if wanted:
        paths = [p for p in paths if p.parent.name[-2:].zfill(2) in wanted]
    if not paths:
        print("Không tìm thấy chương nào.")
        return 1
    for p in paths:
        out, words, used, mode, total = build(p)
        flag = "OK " if used == total else "WARN"
        print(f"{flag} {p.parent.name} -> {out.name}  "
              f"({words:,} từ, {used}/{total} cước chú, nguồn: {mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
