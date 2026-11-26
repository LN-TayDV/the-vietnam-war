# -*- coding: utf-8 -*-
"""
Document model for DOCX Builder v2.

Intermediate representation (IR) that the parser produces and the renderer
consumes.  Translation text is preserved byte-for-byte; only structural and
formatting information is added here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, List, Optional

NodeType = Literal[
    "book_title",
    "author",
    "part",
    "chapter",
    "chapter_number",
    "section_h1",   # Roman numeral section (Heading 2)
    "section_h2",   # Arabic numeral subsection (Heading 3)
    "section_h3",   # Lower subsection / ALL-CAPS title (Heading 4)
    "body",         # Body paragraph
    "block_quote",  # Indented block quote
    "footnote",     # Footnote definition
    "bibliography", # Bibliography entry (ch13 back-matter)
    "index_entry",  # Index entry (ch13 back-matter)
    "page_break",
]


@dataclass
class DocNode:
    """A single node in the document model."""
    type: NodeType
    text: str
    level: int = 0
    metadata: dict = field(default_factory=dict)
    children: List["DocNode"] = field(default_factory=list)

    def add_child(self, node: "DocNode") -> "DocNode":
        self.children.append(node)
        return node


@dataclass
class DocumentModel:
    """Top-level document model for one chapter (or the master book)."""
    nodes: List[DocNode] = field(default_factory=list)
    title: str = ""
    author: str = "Hannah Arendt"
    language: str = "vi-VN"
    chapter_label: str = ""
    source_file: Optional[str] = None
    # Footnote definitions: number -> text
    footnotes: dict = field(default_factory=dict)
    # Whether footnote numbering should restart (per-chapter) or be continuous
    restart_footnotes: bool = True
    # Metadata for audit issues
    metadata: dict = field(default_factory=dict)
