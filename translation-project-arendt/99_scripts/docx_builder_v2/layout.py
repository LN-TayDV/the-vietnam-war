# -*- coding: utf-8 -*-
"""
Page layout and section management for DOCX Builder v2.

A4 page, margins, header/footer with page numbers, per-chapter section breaks.
"""
from __future__ import annotations

from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SERIF = "Times New Roman"
INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x55, 0x55, 0x55)

BOOK_TITLE = "The Origins of Totalitarianism"
AUTHOR = "Hannah Arendt"


class PageLayout:
    """Holds page layout configuration."""

    def __init__(self) -> None:
        self.page_width_cm = 21.0
        self.page_height_cm = 29.7
        self.top_margin_cm = 1.9
        self.bottom_margin_cm = 1.8
        self.left_margin_cm = 2.1
        self.right_margin_cm = 1.8
        self.header_distance_cm = 1.0
        self.footer_distance_cm = 1.0
        self.restart_page_numbering = True


def apply_layout(section, layout: PageLayout) -> None:
    """Apply page layout to a section."""
    section.page_width = Cm(layout.page_width_cm)
    section.page_height = Cm(layout.page_height_cm)
    section.top_margin = Cm(layout.top_margin_cm)
    section.bottom_margin = Cm(layout.bottom_margin_cm)
    section.left_margin = Cm(layout.left_margin_cm)
    section.right_margin = Cm(layout.right_margin_cm)
    section.header_distance = Cm(layout.header_distance_cm)
    section.footer_distance = Cm(layout.footer_distance_cm)


def add_header_footer(section, layout: PageLayout, chapter_label: str = "") -> None:
    """Add header (book title, right aligned) and footer (page number, centered)."""
    section.header.is_linked_to_previous = False
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run(f"{BOOK_TITLE} · {AUTHOR}")
    _fmt_run(run, size=8.5, color=MUTED, italic=True)
    _add_rule(header, size=4, space=4)

    section.footer.is_linked_to_previous = False
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run("Trang ")
    _fmt_run(run, size=9, color=MUTED)
    _add_field(footer, "PAGE")

    if layout.restart_page_numbering:
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:start"), "1")
        section._sectPr.append(pg)


def _fmt_run(run, size=None, bold=None, italic=None, color=None, caps=False) -> None:
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


def _add_rule(paragraph, size=6, color="BFBFBF", space=6) -> None:
    ppr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), str(space))
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    ppr.append(borders)


def _add_field(paragraph, instr: str) -> None:
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for el in (begin, it, sep, txt, end):
        run._r.append(el)
    _fmt_run(run, size=9, color=MUTED)


def new_section(doc, layout: PageLayout) -> None:
    """Add a new page section with layout applied."""
    doc.add_section(WD_SECTION.NEW_PAGE)
    section = doc.sections[-1]
    apply_layout(section, layout)
