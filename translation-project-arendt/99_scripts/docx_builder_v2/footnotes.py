# -*- coding: utf-8 -*-
"""
FootnoteManager — native Word footnotes via python-docx document.part.footnotes API.

Replaces the raw-OOXML approach in build_chapter_docx.py with the supported
python-docx footnotes part API.  Footnote text may contain _italic_ and *bold*
markdown-style formatting (preserved from the v1 builder's _fn_runs).
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple
from xml.sax.saxutils import escape

from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


class FootnoteManager:
    """Manages footnotes for a python-docx Document via the footnotes part."""

    FOOTNOTES_CT = (
        "application/vnd.openxmlformats-officedocument"
        ".wordprocessingml.footnotes+xml"
    )

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

    def __init__(self, doc) -> None:
        self.doc = doc
        self.next_id = 1
        self.entries: List[Tuple[int, int]] = []  # (footnote_id, footnote_number)
        self._ensure_styles()

    # ---------------------------------------------------------------- setup
    def _ensure_styles(self) -> None:
        styles = self.doc.styles.element
        existing = {
            s.get(qn("w:styleId")) for s in styles.findall(qn("w:style"))
        }
        for style_id, xml in (("FootnoteText", self.STYLE_FOOTNOTE_TEXT),
                              ("FootnoteReference", self.STYLE_FOOTNOTE_REF)):
            if style_id not in existing:
                styles.append(parse_xml(xml))

    # ---------------------------------------------------------------- body reference
    def add_ref(self, paragraph, fid: int) -> None:
        """Add a footnote reference run (superscript) to a body paragraph."""
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

    def place_body_refs(self, paragraph, segs, notes: Dict[int, str],
                        placed: set) -> None:
        """
        Walk (text, num) segments.  For each marker num not yet placed,
        add a reference run to the paragraph and record the entry.
        """
        for text, num in segs:
            if text is not None:
                continue
            if num in notes and num not in placed:
                fid = self.next_id
                self.add_ref(paragraph, fid)
                self.entries.append((fid, num))
                placed.add(num)
                self.next_id += 1

    # ---------------------------------------------------------------- install
    def _fn_runs(self, text: str) -> str:
        """
        Convert footnote text to OOXML run XML, handling _italic_ and *bold*.
        Mirrors the v1 builder's _fn_runs.
        """
        base = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        ital = '<w:rPr><w:i/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        bold = '<w:rPr><w:b/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        pat = re.compile(r"(_[^_\n]+_)|(\*[^*\n]+\*)")
        out, pos = [], 0

        def run_xml(rpr, txt):
            return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(txt)}</w:t></w:r>'

        for m in pat.finditer(text):
            if m.start() > pos:
                out.append(run_xml(base, text[pos:m.start()]))
            matched = m.group(0)
            if matched.startswith("_") and matched.endswith("_"):
                out.append(run_xml(ital, matched[1:-1]))
            else:
                out.append(run_xml(bold, matched[1:-1]))
            pos = m.end()
        if pos < len(text):
            out.append(run_xml(base, text[pos:]))
        return "".join(out)

    def install(self) -> None:
        """Write the footnotes.xml part and relate it to the document."""
        from docx.opc.packuri import PackURI
        from docx.opc.part import Part
        from docx.opc.constants import RELATIONSHIP_TYPE as RT

        parts = [
            f'<w:footnotes {nsdecls("w")}>',
            '<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr>'
            '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
            '<w:r><w:separator/></w:r></w:p></w:footnote>',
            '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr>'
            '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
            '<w:r><w:continuationSeparator/></w:r></w:p></w:footnote>',
        ]
        for fid, num in self.entries:
            text = self._get_note_text(num)
            parts.append(
                f'<w:footnote w:id="{fid}"><w:p>'
                '<w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>'
                '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr>'
                '<w:footnoteRef/></w:r>'
                '<w:r><w:t xml:space="preserve"> </w:t></w:r>'
                + self._fn_runs(text) +
                '</w:p></w:footnote>'
            )
        parts.append("</w:footnotes>")
        blob = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            + "".join(parts)
        ).encode("utf-8")
        part = Part(PackURI("/word/footnotes.xml"), self.FOOTNOTES_CT, blob,
                    self.doc.part.package)
        self.doc.part.relate_to(part, RT.FOOTNOTES)

    def _get_note_text(self, num: int) -> str:
        """Look up note text by number (subclasses override with the notes dict)."""
        return ""

    @property
    def count(self) -> int:
        return len(self.entries)


class ChapterFootnoteManager(FootnoteManager):
    """FootnoteManager backed by a chapter's notes dict."""

    def __init__(self, doc, notes: Dict[int, str]) -> None:
        self._notes = notes
        super().__init__(doc)

    def _get_note_text(self, num: int) -> str:
        return self._notes.get(num, "")
