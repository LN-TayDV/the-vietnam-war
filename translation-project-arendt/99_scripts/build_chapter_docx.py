# -*- coding: utf-8 -*-
"""
Build a print-ready DOCX for an Arendt chapter (v2 paragraph format).

Input : 04_translation/v2/chNN/v1_chNN_vi.txt
        Format:
          [V1C04-P001] (trang 134)
          <body text with superscript footnote markers ¹²³…>
          ...
          === FOOTNOTES ===
          ¹ <definition>
          ² <definition>
          ...
Output: 09_docx/V1-CNN_<slug>.docx

Footnotes are real Word footnotes (bottom of page, 9 pt, hanging number).
Section headings (I, II, … VI) and the chapter title block are detected from
the body. UTF-8 / NFC assumed (verified by debug_align.py).

Usage:
    python 99_scripts/build_chapter_docx.py ch04 [ch05 ...]
"""
import io
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
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "04_translation" / "v2"
OUT_DIR = ROOT / "09_docx"

BOOK_TITLE = "The Origins of Totalitarianism"
AUTHOR = "Hannah Arendt"
SERIF = "Times New Roman"
INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x55, 0x55, 0x55)
RULE = "BFBFBF"

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
PARA_HDR = re.compile(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)\s*$")
SECTION_RE = re.compile(r"^(I|II|III|IV|V|VI)$")
# Arabic numeral section headings (e.g. "1:", "1", "2:", ...) — standalone number
ARABIC_SECTION_RE = re.compile(r"^(\d{1,3})\s*:?\s*$")
# ALL-CAPS section title (e.g. "TOÀN TRỊ CHỦ NGHĨA", "TOTALITARIANISM IN POWER")
ALLCAPS_SECTION_RE = re.compile(r"^[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ][A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ\s\d\.,;:'\"()\-–—]+$")
# Embedded page-header OCR artifact, e.g. "=== PAGE 435 === 390 TOÀN TRỊ CHỦ NGHĨA"
PAGE_ARTIFACT_RE = re.compile(r"===\s*PAGE\s+\d+\s*===\s*[\d\wÀ-ỹ\s]*")

TITLES = {
    "front_matter": ("Phần Mở Đầu", "Trang Bìa và Thông Tin Xuất Bản"),
    "preface_first_edition": ("Lời Nói Đầu Bản Dựng Lần Thứ Nhất", ""),
    "preface_part_one": ("Lời Nói Đầu Phần Một", ""),
    "preface_part_two": ("Lời Nói Đầu Phần Hai", ""),
    "preface_part_three": ("Lời Nói Đầu Phần Ba", ""),
    "part_one_intro": ("Phần Một: Chủ Nghĩa Phân Biệt Chủng Tộc", "Giới Thiệu"),
    "ch01": ("Chương Một", "Thuyết Trái Đất Bằng Phẳng"),
    "ch02": ("Chương Hai", "Chủ Nghĩa Phân Biệt Chủng Tộc Trước Chủ Nghĩa Quốc Gia"),
    "ch03": ("Chương Ba", "Dân Tộc Do Thái và Xã Hội"),
    "ch04": ("Chương Bốn", "Vụ Dreyfus"),
    "ch05": ("Chương Năm", "Giải Phóng Chính Trị Của Tiểu Sản"),
    "ch06": ("Chương Sáu", "Tư Duy Chủng Tộc Trước Chủ Nghĩa Phân Biệt Chủng Tộc"),
    "ch07": ("Chương Bảy", "Chủng Tộc và Quan Liêu"),
    "ch08": ("Chương Tám", "Chủ Nghĩa Đế Quốc Lục Địa: Các Phong Trào Pan"),
    "ch09": ("Chương Chín", "Sự Suy Tàn Của Quốc Gia Quốc Dân và Hết Hạn Quyền Con Người"),
    "ch10": ("Chương Mười", "Xã Hội Không Giai Cấp"),
    "ch11": ("Chương Mười Một", "Phong Trào Toàn Trị"),
    "ch12": ("Chương Mười Hai", "Toàn Trị Tại Quyền"),
    "ch13": ("Chương Mười Ba", "Ý Thức Hệ và Khủng Bố · Một Hình Thức Chính Phủ Mới"),
}


def sup_to_int(s):
    return int("".join(str(SUP.index(c)) for c in s))


# ---------------------------------------------------------------- helpers
def set_run_font(run, size=None, bold=None, italic=None, color=None, caps=False, spacing=None):
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
    if spacing is not None:
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


def para_fmt(p, first_indent=0.0, space_before=0, space_after=6, line=1.3,
             align=WD_ALIGN_PARAGRAPH.JUSTIFY, keep_next=False, keep_together=False):
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
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
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
def parse(path):
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    body_part, _, fn_part = raw.partition("=== FOOTNOTES ===")

    # footnotes: lines beginning with a superscript run OR "N." arabic style
    notes = {}
    for line in fn_part.split("\n"):
        s = line.strip()
        if not s:
            continue
        # Strip embedded page-header OCR artifacts (e.g. "=== PAGE 435 === 390 ...")
        s = PAGE_ARTIFACT_RE.sub("", s).strip()
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

    # body paragraphs
    matches = list(PARA_HDR.finditer(body_part))
    items = []
    for j, m in enumerate(matches):
        pid = m.group(1)
        start = m.end()
        end = matches[j + 1].start() if j + 1 < len(matches) else len(body_part)
        text = body_part[start:end].strip()
        text = re.sub(r"\s+", " ", text)
        # Strip embedded page-header OCR artifacts from body text
        text = PAGE_ARTIFACT_RE.sub("", text).strip()
        text = re.sub(r"\s+", " ", text)
        items.append({"id": pid, "text": text})
    return items, notes


def split_markers(text):
    """Split body text into [(text, None) | (None, num)] segments by superscript runs."""
    segs = []
    pos = 0
    for m in re.finditer(r"[" + SUP + r"]+", text):
        if m.start() > pos:
            segs.append((text[pos:m.start()], None))
        segs.append((None, sup_to_int(m.group(0))))
        pos = m.end()
    if pos < len(text):
        segs.append((text[pos:], None))
    return segs


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
    run = header.add_run(f"{BOOK_TITLE} · {AUTHOR}")
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


def add_title_block(doc, chap_label, vi_title):
    eyebrow = doc.add_paragraph()
    para_fmt(eyebrow, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=42, space_after=4, line=1.0)
    run = eyebrow.add_run(BOOK_TITLE.upper())
    set_run_font(run, size=10.5, color=MUTED, caps=True, spacing=10)

    num = doc.add_paragraph()
    para_fmt(num, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10, line=1.0)
    run = num.add_run(chap_label.upper())
    set_run_font(run, size=13, bold=True, color=MUTED, spacing=40)

    t = doc.add_paragraph()
    t.style = doc.styles["Heading 1"]
    para_fmt(t, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6, line=1.15)
    run = t.add_run(vi_title)
    set_run_font(run, size=24, bold=True, spacing=6)

    a = doc.add_paragraph()
    para_fmt(a, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10, line=1.0)
    run = a.add_run(AUTHOR)
    set_run_font(run, size=12, italic=True, color=RGBColor(0x33, 0x33, 0x33))

    rule = doc.add_paragraph()
    para_fmt(rule, space_before=6, space_after=12, line=1.0)
    add_rule(rule, size=8, space=1)

    start_body_section(doc)


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 2"]
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


def add_runs_with_refs(paragraph, segs, next_id, entries, placed, size=12, italic=False):
    for text, num in segs:
        if text is not None:
            run = paragraph.add_run(text)
            set_run_font(run, size=size, italic=italic, color=INK)
        else:
            if num in NOTES_GLOBAL and num not in placed:  # place each note once
                add_footnote_ref(paragraph, next_id[0])
                entries.append((next_id[0], num))
                placed.add(num)
                next_id[0] += 1


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
    base = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    ital = '<w:rPr><w:i/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    pat = re.compile(r"(_[^_\n]+_)|(\*[^*\n]+\*)")
    out, pos = [], 0

    def run(rpr, txt):
        return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(txt)}</w:t></w:r>'

    for m in pat.finditer(text):
        if m.start() > pos:
            out.append(run(base, text[pos:m.start()]))
        out.append(run(ital, m.group(0)[1:-1]))
        pos = m.end()
    if pos < len(text):
        out.append(run(base, text[pos:]))
    return "".join(out)


def install_footnotes(doc, entries):
    parts = [
        f'<w:footnotes {nsdecls("w")}>',
        '<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr>'
        '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:r><w:separator/></w:r></w:p></w:footnote>',
        '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr>'
        '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:r><w:continuationSeparator/></w:r></w:p></w:footnote>',
    ]
    for fid, num in entries:
        parts.append(
            f'<w:footnote w:id="{fid}"><w:p>'
            '<w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>'
            '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr>'
            '<w:footnoteRef/></w:r>'
            '<w:r><w:t xml:space="preserve"> </w:t></w:r>'
            + _fn_runs(NOTES_GLOBAL[num]) +
            '</w:p></w:footnote>'
        )
    parts.append("</w:footnotes>")
    blob = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            + "".join(parts)).encode("utf-8")
    part = Part(PackURI("/word/footnotes.xml"), FOOTNOTES_CT, blob, doc.part.package)
    doc.part.relate_to(part, RT.FOOTNOTES)


def _safe_unlink(path, required=True):
    import time
    if not path.exists():
        return
    last = None
    for _ in range(10):
        try:
            path.unlink()
            return
        except PermissionError as exc:
            last = exc
            time.sleep(0.3)
    if required:
        raise PermissionError(
            f"Không thể ghi đè '{path.name}'. Hãy đóng Word rồi chạy lại.\nChi tiết: {last}")


# ------------------------------------------------------------------ build
NOTES_GLOBAL = {}


def build(ch):
    global NOTES_GLOBAL
    items, notes = parse(V2 / ch / f"v1_{ch}_vi.txt")
    NOTES_GLOBAL = notes
    chap_label, vi_title = TITLES.get(ch, (ch, ch))

    doc = setup_document()
    add_title_block(doc, chap_label, vi_title)
    ensure_footnote_styles(doc)

    next_id = [1]
    entries = []
    placed = set()
    words = 0

    for it in items:
        text = it["text"]
        # Standalone section heading: Roman numerals (I..VI) → Heading 2
        if SECTION_RE.match(text):
            add_section_heading(doc, text)
            continue
        # Standalone Arabic numeral section (e.g. "1:", "1", "2") → Heading 3
        m = ARABIC_SECTION_RE.match(text)
        if m and len(text) <= 10:
            add_section_heading(doc, text.rstrip(":"))
            continue
        # Standalone ALL-CAPS section title (short) → Heading 3
        if ALLCAPS_SECTION_RE.match(text) and len(text) <= 60 and text.strip():
            add_section_heading(doc, text)
            continue
        segs = split_markers(text)
        p = doc.add_paragraph()
        para_fmt(p, first_indent=0.9, space_after=6, line=1.3)
        add_runs_with_refs(p, segs, next_id, entries, placed)
        words += len(text.split())

    unplaced = [n for n in sorted(notes) if n not in placed]
    if unplaced:
        raise ValueError(
            f"FOOTNOTE ORPHAN trong {ch}: {len(unplaced)} cước chú không có marker "
            f"inline: {unplaced}. Thêm marker vào body rồi rebuild.")

    if entries:
        install_footnotes(doc, entries)

    props = doc.core_properties
    props.title = f"{chap_label} — {vi_title}"
    props.subject = BOOK_TITLE
    props.author = AUTHOR
    props.language = "vi-VN"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"V1-{ch[-2:].upper()}_{slugify(vi_title)}.docx"
    tmp = OUT_DIR / f".tmp_{ch}.docx"
    if tmp.exists():
        _safe_unlink(tmp, required=True)
    doc.save(tmp)
    if out.exists():
        _safe_unlink(out, required=True)
    tmp.rename(out)
    return out, words, len(entries), len(notes)


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    wanted = [a for a in argv if a.strip()]
    if not wanted:
        print("Usage: python 99_scripts/build_chapter_docx.py ch04 [ch05 ...]")
        return 1
    rc = 0
    for ch in wanted:
        out, words, used, total = build(ch)
        flag = "OK " if used == total else "WARN"
        if used != total:
            rc = 1
        print(f"{flag} {ch} -> {out.name} ({words:,} từ, {used}/{total} cước chú)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))