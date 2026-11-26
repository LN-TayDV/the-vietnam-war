#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract DOCX structure from chapter DOCXs and master DOCX.
Output: audit/docx_structure_baseline.json
"""
import json
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "09_docx"
AUDIT_DIR = ROOT / "audit"

DOCX_FILES = {
    "front_matter": None,  # not in 09_docx
    "preface_first_edition": None,
    "preface_part_one": None,
    "preface_part_two": None,
    "preface_part_three": None,
    "part_one_intro": None,
    "ch01": "V1-01_ch01.docx",
    "ch02": "V1-02_ch02.docx",
    "ch03": "V1-03_ch03.docx",
    "ch04": "V1-04_Vu-Dreyfus.docx",
    "ch05": "V1-05_ch05.docx",
    "ch06": "V1-06_ch06.docx",
    "ch07": "V1-07_ch07.docx",
    "ch08": "V1-08_ch08.docx",
    "ch09": "V1-09_ch09.docx",
    "ch10": "V1-10_ch10.docx",
    "ch11": "V1-11_ch11.docx",
    "ch12": "V1-12_Toan-Tri-Tai-Quyen.docx",
    "ch13": "V1-13_Y-thuc-he-va-Khung-bo-Mot-Hinh-thuc-Chinh-phu-Moi.docx",
    "master": "V1-Origins-of-Totalitarianism.docx",
}

def extract_styles(doc):
    """Extract all paragraph styles used in the document."""
    styles = {}
    for style in doc.styles:
        if style.type == 1:  # WD_STYLE_TYPE.PARAGRAPH
            styles[style.style_id] = {
                "name": style.name,
                "based_on": style.base_style.style_id if style.base_style else None,
                "font": style.font.name,
                "size_pt": style.font.size.pt if style.font.size else None,
                "bold": style.font.bold,
                "italic": style.font.italic,
            }
    return styles

def extract_paragraphs(doc):
    """Extract all paragraphs with their style and text."""
    paras = []
    for i, p in enumerate(doc.paragraphs):
        paras.append({
            "index": i,
            "style_id": p.style.style_id,
            "style_name": p.style.name,
            "text": p.text[:200],  # truncate for readability
            "runs_count": len(p.runs),
            "alignment": str(p.alignment) if p.alignment else None,
            "first_line_indent_cm": p.paragraph_format.first_line_indent.cm if p.paragraph_format.first_line_indent else None,
            "space_before_pt": p.paragraph_format.space_before.pt if p.paragraph_format.space_before else None,
            "space_after_pt": p.paragraph_format.space_after.pt if p.paragraph_format.space_after else None,
            "line_spacing": p.paragraph_format.line_spacing,
            "keep_with_next": p.paragraph_format.keep_with_next,
        })
    return paras

def extract_headings(doc):
    """Extract heading paragraphs (Heading 1-4 styles)."""
    headings = []
    for p in doc.paragraphs:
        if p.style.style_id.startswith("Heading") or "Heading" in p.style.name:
            headings.append({
                "level": int(p.style.style_id[-1]) if p.style.style_id[-1].isdigit() else None,
                "style_id": p.style.style_id,
                "text": p.text,
            })
    return headings

def extract_footnotes(doc):
    """Extract footnote count and basic info."""
    fn_count = 0
    if hasattr(doc.part, 'footnotes') and doc.part.footnotes:
        fn_count = len(doc.part.footnotes._footnotes)
    return {"count": fn_count}

def extract_sections(doc):
    """Extract section properties."""
    sections = []
    for s in doc.sections:
        sections.append({
            "page_width_cm": s.page_width.cm,
            "page_height_cm": s.page_height.cm,
            "top_margin_cm": s.top_margin.cm,
            "bottom_margin_cm": s.bottom_margin.cm,
            "left_margin_cm": s.left_margin.cm,
            "right_margin_cm": s.right_margin.cm,
            "header_distance_cm": s.header_distance.cm,
            "footer_distance_cm": s.footer_distance.cm,
            "start_type": str(s.start_type),
        })
    return sections

def extract_toc(doc):
    """Check for TOC field codes."""
    toc_fields = []
    for p in doc.paragraphs:
        for run in p.runs:
            for child in run._r:
                if child.tag.endswith('}instrText') and 'TOC' in (child.text or ''):
                    toc_fields.append(child.text)
    return toc_fields

def process_docx(chapter, filename):
    path = OUT_DIR / filename
    if not path.exists():
        return {"chapter": chapter, "status": "MISSING", "file": str(path)}
    
    doc = Document(path)
    
    return {
        "chapter": chapter,
        "file": str(path),
        "status": "OK",
        "paragraphs_count": len(doc.paragraphs),
        "styles": extract_styles(doc),
        "paragraphs_sample": extract_paragraphs(doc)[:50],  # first 50
        "headings": extract_headings(doc),
        "footnotes": extract_footnotes(doc),
        "sections": extract_sections(doc),
        "toc_fields": extract_toc(doc),
        "core_properties": {
            "title": doc.core_properties.title,
            "author": doc.core_properties.author,
            "subject": doc.core_properties.subject,
            "language": doc.core_properties.language,
        }
    }

def main():
    results = {}
    for chapter, filename in DOCX_FILES.items():
        if filename:
            print(f"Processing {chapter}...")
            results[chapter] = process_docx(chapter, filename)
        else:
            results[chapter] = {"chapter": chapter, "status": "NO_DOCX"}
    
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIT_DIR / "docx_structure_baseline.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    main()