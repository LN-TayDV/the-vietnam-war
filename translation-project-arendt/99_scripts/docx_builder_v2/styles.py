# -*- coding: utf-8 -*-
"""
Style system for DOCX Builder v2.

Loads style definitions from styles/spec.yaml and registers them as Word
styles in a python-docx Document.  All paragraphs use named Word styles;
no direct run formatting is applied (except for footnote reference runs
which require the FootnoteReference character style).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional
from pathlib import Path

import yaml

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn


@dataclass
class StyleSpec:
    style_id: str
    name: str
    type: str = "paragraph"          # "paragraph" or "character"
    based_on: Optional[str] = None
    font: str = "Times New Roman"
    size: Optional[float] = None
    bold: bool = False
    italic: bool = False
    color: Optional[str] = None      # hex RRGGBB
    align: Optional[str] = None      # "left", "center", "right", "justify"
    first_indent_cm: float = 0.0
    left_indent_cm: float = 0.0
    hanging_cm: float = 0.0
    space_before_pt: int = 0
    space_after_pt: int = 6
    line_spacing: float = 1.3
    keep_with_next: bool = False
    keep_together: bool = False
    widow_control: bool = True
    ui_priority: int = 99
    unhide_when_used: bool = True


@dataclass
class StyleRegistry:
    styles: Dict[str, StyleSpec] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "StyleRegistry":
        p = Path(path)
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        reg = cls()
        for item in data.get("styles", []):
            spec = StyleSpec(
                style_id=item["id"],
                name=item["name"],
                type=item.get("type", "paragraph"),
                based_on=item.get("based_on"),
                font=item.get("font", "Times New Roman"),
                size=item.get("size"),
                bold=item.get("bold", False),
                italic=item.get("italic", False),
                color=item.get("color"),
                align=item.get("align"),
                first_indent_cm=item.get("first_indent_cm", 0.0),
                left_indent_cm=item.get("left_indent_cm", 0.0),
                hanging_cm=item.get("hanging_cm", 0.0),
                space_before_pt=item.get("space_before_pt", 0),
                space_after_pt=item.get("space_after_pt", 6),
                line_spacing=item.get("line_spacing", 1.3),
                keep_with_next=item.get("keep_with_next", False),
                keep_together=item.get("keep_together", False),
                widow_control=item.get("widow_control", True),
                ui_priority=item.get("ui_priority", 99),
                unhide_when_used=item.get("unhide_when_used", True),
            )
            reg.styles[spec.style_id] = spec
        return reg

    def apply_to_document(self, doc: Document) -> None:
        """Register all styles into the python-docx document."""
        from docx.oxml import parse_xml
        styles_element = doc.styles.element
        existing = {
            s.get(qn("w:styleId")) for s in styles_element.findall(qn("w:style"))
        }

        # Order matters: base styles must exist before derived ones.
        ordered = sorted(self.styles.values(), key=lambda s: (s.based_on is not None, s.style_id))

        for spec in ordered:
            if spec.style_id in existing:
                continue
            xml_str = self._style_xml(spec)
            xml_el = parse_xml(xml_str)
            styles_element.append(xml_el)

    @staticmethod
    def _style_xml(spec: StyleSpec) -> str:
        from docx.oxml.ns import nsdecls

        nsprefix = nsdecls("w")
        color_xml = f'<w:color w:val="{spec.color}"/>' if spec.color else ""
        base_xml = f'<w:basedOn w:val="{spec.based_on}"/>' if spec.based_on else ""

        # Alignment
        align_map = {
            "left": "start",
            "center": "center",
            "right": "end",
            "justify": "both",
        }
        jc_val = align_map.get(spec.align, "both" if spec.type == "paragraph" else "start")
        jc_xml = f'<w:jc w:val="{jc_val}"/>' if spec.align else ""

        # Indentation
        indent_parts = []
        if spec.first_indent_cm:
            indent_parts.append(f'<w:firstLine w:val="{int(spec.first_indent_cm * 567)}"/>')
        if spec.left_indent_cm:
            indent_parts.append(f'<w:left w:val="{int(spec.left_indent_cm * 567)}"/>')
        if spec.hanging_cm:
            indent_parts.append(f'<w:hanging w:val="{int(spec.hanging_cm * 567)}"/>')
        indent_xml = f"<w:ind>{''.join(indent_parts)}</w:ind>" if indent_parts else ""

        # Spacing
        line_twips = int(spec.line_spacing * 240)
        spacing_xml = (
            f'<w:spacing w:before="{spec.space_before_pt * 20}" '
            f'w:after="{spec.space_after_pt * 20}" '
            f'w:line="{line_twips}" w:lineRule="auto"/>'
        )

        # Run properties
        rpr_parts = []
        rpr_parts.append(f'<w:rFonts w:ascii="{spec.font}" w:hAnsi="{spec.font}" w:cs="{spec.font}" w:eastAsia="{spec.font}"/>')
        if spec.size is not None:
            sz_half = int(spec.size * 2)
            rpr_parts.append(f'<w:sz w:val="{sz_half}"/><w:szCs w:val="{sz_half}"/>')
        if spec.bold:
            rpr_parts.append("<w:b/>")
        if spec.italic:
            rpr_parts.append("<w:i/>")
        if color_xml:
            rpr_parts.append(color_xml)
        rpr_xml = f"<w:rPr>{''.join(rpr_parts)}</w:rPr>"

        # Paragraph properties
        ppr_parts = []
        if indent_xml:
            ppr_parts.append(indent_xml)
        ppr_parts.append(spacing_xml)
        if jc_xml:
            ppr_parts.append(jc_xml)
        if spec.keep_with_next:
            ppr_parts.append("<w:keepNext/>")
        if spec.keep_together:
            ppr_parts.append("<w:keepLines/>")
        if spec.widow_control:
            ppr_parts.append("<w:widowControl/>")
        ppr_xml = f"<w:pPr>{''.join(ppr_parts)}</w:pPr>" if ppr_parts else ""

        ui_priority = f'<w:uiPriority w:val="{spec.ui_priority}"/>' if spec.ui_priority is not None else ""
        unhide = '<w:unhideWhenUsed/>' if spec.unhide_when_used else ""

        if spec.type == "character":
            return (
                f'<w:style {nsprefix} w:type="character" w:styleId="{spec.style_id}">'
                f'<w:name w:val="{spec.name}"/>'
                f'{base_xml}{ui_priority}{unhide}{rpr_xml}'
                f"</w:style>"
            )
        else:
            return (
                f'<w:style {nsprefix} w:type="paragraph" w:styleId="{spec.style_id}">'
                f'<w:name w:val="{spec.name}"/>'
                f'{base_xml}{ui_priority}{unhide}{ppr_xml}{rpr_xml}'
                f"</w:style>"
            )

    def get(self, style_id: str) -> Optional[StyleSpec]:
        return self.styles.get(style_id)


def apply_paragraph_format(paragraph, spec: StyleSpec) -> None:
    """Apply a StyleSpec's paragraph formatting to an existing paragraph (idempotent)."""
    pf = paragraph.paragraph_format
    pf.first_line_indent = Cm(spec.first_indent_cm) if spec.first_indent_cm else None
    pf.left_indent = Cm(spec.left_indent_cm) if spec.left_indent_cm else None
    pf.space_before = Pt(spec.space_before_pt)
    pf.space_after = Pt(spec.space_after_pt)
    pf.line_spacing = spec.line_spacing
    if spec.align == "left":
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif spec.align == "center":
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif spec.align == "right":
        pf.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    else:
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.keep_with_next = spec.keep_with_next
    pf.keep_together = spec.keep_together
    pf.widow_control = spec.widow_control


def set_run_font(run, spec: StyleSpec, override_size: Optional[float] = None,
                 override_bold: Optional[bool] = None,
                 override_italic: Optional[bool] = None,
                 override_color: Optional[str] = None) -> None:
    """Apply font properties from a StyleSpec to a run."""
    run.font.name = spec.font
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), spec.font)
    size = override_size if override_size is not None else spec.size
    if size is not None:
        run.font.size = Pt(size)
    bold = spec.bold if override_bold is None else override_bold
    if bold is not None:
        run.font.bold = bold
    italic = spec.italic if override_italic is None else override_italic
    if italic is not None:
        run.font.italic = italic
    color = override_color if override_color is not None else spec.color
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
