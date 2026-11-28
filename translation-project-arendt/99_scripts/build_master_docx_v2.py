# -*- coding: utf-8 -*-
"""
Master DOCX Builder v2 — combine all 13 chapters + front matter/prefaces into
one book with continuous footnote numbering, a title page, and an auto TOC.

Footnote strategy: continuous numbering across the whole book. Each chapter's
local footnote numbers are remapped to a global offset; body superscript markers
are rewritten to «globalnum» tokens that split_markers understands.

Usage:
    python 99_scripts/build_master_docx_v2.py
"""
from __future__ import annotations

import io
import re
import sys
import unicodedata
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

from docx_builder_v2.models import DocumentModel, DocNode
from docx_builder_v2.parser import parse, sup_to_int, SUP
from docx_builder_v2.styles import StyleRegistry
from docx_builder_v2.layout import PageLayout
from docx_builder_v2.renderer import Renderer, STYLE_NAMES

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "04_translation" / "v2"
V1 = ROOT / "04_translation" / "v1"
OUT_DIR = ROOT / "09_docx"
STYLES_PATH = ROOT / "99_scripts" / "styles" / "spec.yaml"

BOOK_TITLE = "The Origins of Totalitarianism"
AUTHOR = "Hannah Arendt"

CHAPTERS = [f"ch{i:02d}" for i in range(1, 14)]

TITLES = {
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

FRONT = [
    ("front_matter", "Phần Mở Đầu", "Trang Bìa và Thông Tin Xuất Bản"),
    ("preface_first_edition", "Lời Nói Đầu Bản Dựng Lần Thứ Nhất", ""),
    ("preface_part_one", "Lời Nói Đầu Phần Một", ""),
    ("preface_part_two", "Lời Nói Đầu Phần Hai", ""),
    ("preface_part_three", "Lời Nói Đầu Phần Ba", ""),
    ("part_one_intro", "Phần Một: Chủ Nghĩa Phân Biệt Chủng Tộc", "Giới Thiệu"),
]

SUP_RUN = re.compile(r"[" + SUP + r"]+")
SUP_OR_GLOBAL = re.compile(r"(?:[" + SUP + r"]+|«\d+»)")


def normalize_for_dedup(text: str) -> str:
    """Normalize text for deduplication by removing footnote markers."""
    return SUP_OR_GLOBAL.sub("", text)


def remap_superscripts(text: str, offset: int) -> str:
    """Replace superscript footnote runs with «globalnum» tokens."""
    def repl(m):
        local = sup_to_int(m.group(0))
        return f"«{local + offset}»"
    return SUP_RUN.sub(repl, text)


def load_front_matter():
    """Load v1 front matter/preface text files as body nodes using the parser."""
    nodes = []
    for key, label, title in FRONT:
        path = V1 / key / f"v1_{key}_vi.txt"
        if not path.exists():
            continue
        # Use the parser to properly handle metadata headers and footnotes
        raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        model = parse(raw, chapter_label="", vi_title="")
        # Add section heading
        nodes.append(DocNode(type="chapter", text=label, level=1,
                             metadata={"section": key}))
        if title:
            nodes.append(DocNode(type="section_h3", text=title, level=4,
                                 metadata={"section": key}))
        # Add parsed nodes (they already have proper types from parser)
        nodes.extend(model.nodes)
    return nodes


def build_master() -> tuple:
    registry = StyleRegistry.from_yaml(STYLES_PATH)
    layout = PageLayout()

    master = DocumentModel()
    master.title = "Nguồn Gốc Của Chủ Nghĩa Toàn Trị"  # Vietnamese book title
    master.chapter_label = "PHẦN MỞ ĐẦU"  # Will be overridden per section
    global_footnotes: dict = {}
    offset = 0

    # Front matter first
    master.nodes.extend(load_front_matter())

    seen_body_texts = set()

    for ch in CHAPTERS:
        src = V2 / ch / f"v1_{ch}_vi.txt"
        text = src.read_text(encoding="utf-8").replace("\r\n", "\n")
        model = parse(text, chapter_label="", vi_title="")
        # Insert an explicit chapter heading node (from TITLES) so the master
        # has a proper Heading-1 chapter title for every chapter.
        chap_label, vi_title = TITLES.get(ch, (ch, ch))
        master.nodes.append(DocNode(type="chapter_number", text=chap_label,
                                    level=1, metadata={"chapter": ch}))
        master.nodes.append(DocNode(type="chapter", text=vi_title,
                                    level=1, metadata={"chapter": ch}))
        # remap footnotes to global
        local_notes = dict(model.footnotes)
        for num, txt in local_notes.items():
            global_footnotes[num + offset] = txt
        # remap body markers and filter out duplicate chapter title nodes from parser
        for node in model.nodes:
            if node.type in ("body", "block_quote"):
                # Check if paragraph has footnote markers
                has_fn_markers = bool(SUP_RUN.search(node.text))
                # Deduplicate: skip if normalized text already added AND no footnote markers
                norm_text = normalize_for_dedup(node.text)
                if norm_text in seen_body_texts and not has_fn_markers:
                    continue
                seen_body_texts.add(norm_text)
                node.text = remap_superscripts(node.text, offset)
            # Skip chapter/part title nodes from parser - we add explicit ones above
            if node.type in ("chapter", "chapter_number", "part", "book_title", "author"):
                continue
            master.nodes.extend([node])
        offset += (max(local_notes.keys()) if local_notes else 0)

    master.footnotes = global_footnotes
    master.restart_footnotes = False

    # Render
    doc, fn_placed = Renderer(registry, layout).render(master)

    # Insert TOC after the title block (find first section break)
    _insert_toc(doc)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "V2-Origins-of-Totalitarianism-MASTER.docx"
    tmp = OUT_DIR / ".tmp_master_v2.docx"
    if tmp.exists():
        tmp.unlink()
    doc.save(tmp)
    if out.exists():
        out.unlink()
    tmp.rename(out)
    words = sum(len(n.text.split()) for n in master.nodes if n.type in ("body", "block_quote"))
    return out, words, fn_placed, len(global_footnotes)


def _insert_toc(doc):
    """Insert a TOC field at the start of the body section."""
    # Find the paragraph that starts the body section (after title block).
    # We insert TOC right before the first body node paragraph.
    body = doc.element.body
    # Create TOC paragraph
    p = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    pstyle = OxmlElement("w:pStyle")
    pstyle.set(qn("w:val"), "TOCHeading")
    ppr.append(pstyle)
    p.append(ppr)
    # TOC field
    def fld(char_type, instr=None):
        r = OxmlElement("w:r")
        if char_type == "begin":
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin")
            r.append(fc)
        elif char_type == "instr":
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
            it.text = instr
            r.append(it)
        elif char_type == "separate":
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "separate")
            r.append(fc)
        elif char_type == "end":
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "end")
            r.append(fc)
        return r
    p.append(fld("begin"))
    p.append(fld("instr", ' TOC \\o "1-3" \\h \\z \\u '))
    p.append(fld("separate"))
    # placeholder text
    r = OxmlElement("w:r"); t = OxmlElement("w:t")
    t.text = "Nhấn F9 để cập nhật mục lục."
    r.append(t); p.append(r)
    p.append(fld("end"))

    # Insert after the last title-block paragraph (before first section's body).
    # Heuristic: insert as first child after the first sectPr's preceding content.
    # We insert right after the title block's rule paragraph.
    # Find first paragraph with a section break (w:sectPr in pPr) -> insert before it.
    inserted = False
    for child in list(body):
        if child.tag == qn("w:p"):
            ppr = child.find(qn("w:pPr"))
            if ppr is not None and ppr.find(qn("w:sectPr")) is not None:
                child.addprevious(p)
                inserted = True
                break
    if not inserted:
        body.insert(0, p)


def main(argv) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    out, words, used, total = build_master()
    flag = "OK " if used == total else "WARN"
    print(f"{flag} MASTER -> {out.name} ({words:,} từ, {used}/{total} cước chú liên tục)")
    return 0 if used == total else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))