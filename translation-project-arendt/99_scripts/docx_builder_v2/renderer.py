# -*- coding: utf-8 -*-
"""
Renderer: DocumentModel → python-docx Document.

Applies Word styles exclusively (no direct paragraph formatting), builds the
title block, body paragraphs with footnote references, headings, block quotes,
bibliography/index entries, and installs native Word footnotes via the
footnotes part API.
"""
from __future__ import annotations

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

from .models import DocumentModel, DocNode, NodeType
from .parser import split_markers
from .styles import StyleRegistry, apply_paragraph_format, set_run_font
from .layout import PageLayout, apply_layout, add_header_footer, new_section
from .footnotes import ChapterFootnoteManager

INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x55, 0x55, 0x55)
SERIF = "Times New Roman"

# Map node types to style IDs
NODE_STYLE = {
    "book_title": "ArendtBookTitle",
    "author": "Author",
    "part": "PartHeading",
    "chapter": "ChapterTitle",
    "chapter_number": "ChapterNumber",
    "section_h1": "SectionH1",
    "section_h2": "SectionH2",
    "section_h3": "SectionH3",
    "body": "BodyText",
    "block_quote": "BlockQuote",
    "bibliography": "Bibliography",
    "index_entry": "IndexEntry",
}

# Style names for doc.styles[] lookup (to avoid deprecation warnings)
STYLE_NAMES = {
    "ArendtBookTitle": "Arendt Book Title",
    "ChapterNumber": "Chapter Number",
    "ChapterTitle": "Chapter Title",
    "Author": "Author",
    "PartHeading": "Part Heading",
    "SectionH1": "Section H1",
    "SectionH2": "Section H2",
    "SectionH3": "Section H3",
    "BodyText": "Body Text",
    "BodyTextFirst": "Body First Para",
    "BlockQuote": "Block Quote",
    "FootnoteText": "Footnote Text",
    "Bibliography": "Bibliography",
    "IndexEntry": "Index Entry",
    "TOC1": "TOC Level 1",
    "TOC2": "TOC Level 2",
}


class Renderer:
    def __init__(self, registry: StyleRegistry, layout: PageLayout) -> None:
        self.registry = registry
        self.layout = layout

    def render(self, model: DocumentModel) -> Document:
        doc = Document()
        self.registry.apply_to_document(doc)

        # Core properties
        cp = doc.core_properties
        cp.title = model.title or model.chapter_label
        cp.subject = "The Origins of Totalitarianism"
        cp.author = model.author
        cp.language = model.language

        # Base Normal style
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

        # First section: title page
        section = doc.sections[0]
        apply_layout(section, self.layout)
        section.header.is_linked_to_previous = True
        section.footer.is_linked_to_previous = True

        self._build_title_block(doc, model)
        new_section(doc, self.layout)
        add_header_footer(doc.sections[-1], self.layout, model.chapter_label)

        footnote_mgr = ChapterFootnoteManager(doc, model.footnotes)
        placed = set()

        # Track first body paragraph (no first-line indent)
        first_body = True

        for node in model.nodes:
            self._render_node(doc, node, footnote_mgr, placed, first_body)
            if node.type == "body":
                first_body = False

        footnote_mgr.install()
        return doc, len(placed)

    def _build_title_block(self, doc, model: DocumentModel) -> None:
        """Build the title page block with book title, chapter label, chapter title, author."""
        BOOK_TITLE = "The Origins of Totalitarianism"
        AUTHOR = "Hannah Arendt"
        
        # Book title (eyebrow)
        eyebrow = doc.add_paragraph()
        eyebrow.style = doc.styles[STYLE_NAMES["ArendtBookTitle"]]
        apply_paragraph_format(eyebrow, self.registry.get("ArendtBookTitle"))
        run = eyebrow.add_run(BOOK_TITLE.upper())
        set_run_font(run, self.registry.get("ArendtBookTitle"), override_size=10.5, override_color="555555")
        # Apply small caps and spacing via run properties
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        rpr = run._element.get_or_add_rPr()
        small_caps = OxmlElement("w:smallCaps")
        rpr.append(small_caps)
        spacing = OxmlElement("w:spacing")
        spacing.set(qn("w:val"), "20")  # 1pt = 20 twips, so 10pt = 200 twips... let me check
        rpr.append(spacing)

        # Chapter number
        num = doc.add_paragraph()
        num.style = doc.styles[STYLE_NAMES["ChapterNumber"]]
        apply_paragraph_format(num, self.registry.get("ChapterNumber"))
        run = num.add_run(model.chapter_label.upper())
        set_run_font(run, self.registry.get("ChapterNumber"), override_size=13, override_bold=True, override_color="555555")

        # Chapter title
        t = doc.add_paragraph()
        t.style = doc.styles[STYLE_NAMES["ChapterTitle"]]
        apply_paragraph_format(t, self.registry.get("ChapterTitle"))
        run = t.add_run(model.title)
        set_run_font(run, self.registry.get("ChapterTitle"), override_size=24, override_bold=True)

        # Author
        a = doc.add_paragraph()
        a.style = doc.styles[STYLE_NAMES["Author"]]
        apply_paragraph_format(a, self.registry.get("Author"))
        run = a.add_run(AUTHOR)
        set_run_font(run, self.registry.get("Author"), override_size=12, override_italic=True, override_color="333333")

        # Rule
        rule = doc.add_paragraph()
        apply_paragraph_format(rule, self.registry.get("Author"))
        self._add_rule(rule, size=8, space=1)

    def _add_rule(self, paragraph, size=6, color="BFBFBF", space=6) -> None:
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        ppr = paragraph._p.get_or_add_pPr()
        borders = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), str(size))
        bottom.set(qn("w:space"), str(space))
        bottom.set(qn("w:color"), color)
        borders.append(bottom)
        ppr.append(borders)

    # ---------------------------------------------------------------- nodes
    def _render_node(self, doc, node: DocNode, footnote_mgr, placed, first_body) -> None:
        style_id = NODE_STYLE.get(node.type, "BodyText")
        style_name = STYLE_NAMES.get(style_id, style_id)
        spec = self.registry.get(style_id)

        if node.type == "book_title":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec, override_size=24)
            return

        if node.type == "author":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec, override_size=12)
            return

        if node.type == "chapter_number":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec, override_size=13)
            return

        if node.type == "part":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec, override_size=18, override_bold=True)
            return

        if node.type == "chapter":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec, override_size=22, override_bold=True)
            return

        if node.type in ("section_h1", "section_h2", "section_h3"):
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec, override_size=spec.size or 12, override_bold=True)
            return

        if node.type == "body":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            if first_body:
                p.paragraph_format.first_line_indent = 0  # no indent on first body para
            self._add_body_runs(p, node.text, footnote_mgr, placed)
            return

        if node.type == "block_quote":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            self._add_body_runs(p, node.text, footnote_mgr, placed)
            return

        if node.type == "bibliography":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec)
            return

        if node.type == "index_entry":
            p = doc.add_paragraph()
            p.style = doc.styles[style_name]
            apply_paragraph_format(p, spec)
            run = p.add_run(node.text)
            set_run_font(run, spec)
            return

        # Fallback: body
        p = doc.add_paragraph()
        p.style = doc.styles[STYLE_NAMES["BodyText"]]
        apply_paragraph_format(p, self.registry.get("BodyText"))
        self._add_body_runs(p, node.text, footnote_mgr, placed)

    # ---------------------------------------------------------------- body runs
    def _add_body_runs(self, paragraph, text: str, footnote_mgr, placed) -> None:
        """Split text by superscript markers, add text runs + footnote refs."""
        segs = split_markers(text)
        for text_seg, num in segs:
            if text_seg is not None:
                run = paragraph.add_run(text_seg)
                set_run_font(run, self.registry.get("BodyText"))
            else:
                if num in footnote_mgr._notes and num not in placed:
                    fid = footnote_mgr.next_id
                    footnote_mgr.add_ref(paragraph, fid)
                    footnote_mgr.entries.append((fid, num))
                    placed.add(num)
                    footnote_mgr.next_id += 1
