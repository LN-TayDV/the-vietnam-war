# -*- coding: utf-8 -*-
"""
Parser: v2 translation text → DocumentModel.

Input format (04_translation/v2/chNN/v1_chNN_vi.txt):
    [V1C04-P001] (trang 134)
    <body text with superscript footnote markers ¹²³…>
    ...
    === FOOTNOTES ===
    ¹ <definition>                    (superscript prefix, fns 1-52)
    53. <definition>                  (arabic prefix, fns 53+)
    ...

The parser:
  1. Splits on === FOOTNOTES === → body + footnotes
  2. Parses paragraphs by [V1C##-P###] (trang N) headers
  3. Filters out running headers (page-level artifacts like "TOTALITARIANISM IN POWER 391")
  4. Resolves cross-page continuity (merges continuations, joins hyphenated splits)
  5. Splits each paragraph block into lines; classifies each line:
     - Book title / Author / Part / Chapter → book_title, author, part, chapter
     - Roman numeral alone (I-VI)      → section_h1  (Heading 2)
     - Arabic numeral alone (1:, 1, 2) → section_h2  (Heading 3)
     - ALL-CAPS short title (non-running-header) → section_h3  (Heading 4)
     - Block quote (indented + citation) → block_quote
     - Bibliography / index pattern    → bibliography / index_entry
     - Default                         → body
  6. Extracts inline superscript markers as footnote references
  7. Parses footnote definitions (superscript or arabic prefix)
  8. Validates heading hierarchy, detects duplicates, flags UNVERIFIED merges

Translation text is preserved byte-for-byte; only structural metadata is added.
"""
from __future__ import annotations

import re
from typing import Optional, Tuple, List, Dict, Any, Set
from pathlib import Path

from .models import DocNode, DocumentModel, NodeType
from .headers import strip_running_headers

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"

PARA_HDR = re.compile(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)\s*$")
SECTION_RE = re.compile(r"^(I|II|III|IV|V|VI)$")
ARABIC_SECTION_RE = re.compile(r"^(\d{1,3})\s*:?\s*$")
# ALL-CAPS section title: short (<=60 chars), but EXCLUDE running headers
# Running headers are page-level artifacts that repeat across pages (e.g., "TOTALITARIANISM IN POWER 391")
ALLCAPS_SECTION_RE = re.compile(
    r"^[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ]"
    r"[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ\s\d\.,;:'\"()\-–—]+$"
)
PAGE_ARTIFACT_RE = re.compile(r"===\s*PAGE\s+\d+\s*===\s*[\d\wÀ-ỹ\s]*")
FOOTNOTE_SUP_RE = re.compile(r"[" + SUP + r"]+")
FOOTNOTE_ARABIC_RE = re.compile(r"^(\d{1,3})\.\s+(.*)$", re.MULTILINE)

# Known running header patterns (from Arendt's book) - these are page-level artifacts, NOT structural headings
RUNNING_HEADER_PATTERNS = [
    # English running headers
    re.compile(r"^TOTALITARIANISM\s+IN\s+POWER\s*\d*$", re.IGNORECASE),
    re.compile(r"^ANTISEMITISM\s*\d*$", re.IGNORECASE),
    re.compile(r"^IMPERIALISM\s*\d*$", re.IGNORECASE),
    re.compile(r"^THE\s+DREYFUS\s+AFFAIR\s*\d*$", re.IGNORECASE),
    re.compile(r"^RACE\s+THINKING\s+BEFORE\s+RACE\s+IDEOLOGY\s*\d*$", re.IGNORECASE),
    re.compile(r"^THE\s+DECLINE\s+OF\s+THE\s+NATION\s+STATE\s*\d*$", re.IGNORECASE),
    re.compile(r"^A\s+CLASSLESS\s+SOCIETY\s*\d*$", re.IGNORECASE),
    re.compile(r"^THE\s+TOTALITARIAN\s+MOVEMENT\s*\d*$", re.IGNORECASE),
    re.compile(r"^TOTALITARIANISM\s+IN\s+POWER\s*\d*$", re.IGNORECASE),
    re.compile(r"^IDEOLOGY\s+AND\s+TERROR\s*\d*$", re.IGNORECASE),
    # Vietnamese running headers (translated)
    re.compile(r"^TOÀN\s+TRỊ\s+CHỦ\s+NGHĨA\s*\d*$", re.IGNORECASE),
    re.compile(r"^CHỦ\s+NGHĨA\s+PHÂN\s+BIỆT\s+CHỦNG\s+TỘC\s*\d*$", re.IGNORECASE),
    re.compile(r"^CHỦ\s+NGHĨA\s+ĐẾ\s+QUỐC\s*\d*$", re.IGNORECASE),
    re.compile(r"^VỤ\s+DREYFUS\s*\d*$", re.IGNORECASE),
    re.compile(r"^TƯ\s+DUY\s+VỀ\s+CHỦNG\s+TỘC\s*\d*$", re.IGNORECASE),
    re.compile(r"^SỰ\s+SUY\s+TÀN\s+CỦA\s+QUỐC\s+GIA\s*\d*$", re.IGNORECASE),
    re.compile(r"^XÃ\s+HỘI\s+PHI\s+GIAI\s+CẤP\s*\d*$", re.IGNORECASE),
    re.compile(r"^PHONG\s+TRÀO\s+TOÀN\s+TRỊ\s*\d*$", re.IGNORECASE),
    re.compile(r"^Ý\s+THỨC\s+HỆ\s+VÀ\s+KHỦNG\s+BỐ\s*\d*$", re.IGNORECASE),
    # Generic: ALL-CAPS + page number pattern (e.g., "TITLE 391")
    re.compile(r"^[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ\s]+\d{1,3}$"),
]

def is_running_header(text: str) -> bool:
    """Check if a line is a running header (page-level artifact, not structural heading)."""
    t = text.strip()
    if not t:
        return False
    for pat in RUNNING_HEADER_PATTERNS:
        if pat.match(t):
            return True
    return False

# Chapter title patterns (first paragraph after book/author)
CHAPTER_TITLE_PATTERNS = [
    re.compile(r"^(CHƯƠNG|Chương)\s+[IVXLCĐM]+", re.IGNORECASE),
    re.compile(r"^(PHẦN|Phần)\s+[IVXLCĐM]+", re.IGNORECASE),
    re.compile(r"^LỜI NÓI ĐẦU", re.IGNORECASE),
    re.compile(r"^TRANG BÌA", re.IGNORECASE),
]

# Block quote detection: indented text with citation-like ending
BLOCK_QUOTE_RE = re.compile(r"^.{50,}.*[.!?]\s*[—–-]\s*[A-Z][a-z]+.*\d{4}$")

# Bibliography entry pattern
BIBLIOGRAPHY_RE = re.compile(
    r"^[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỵỄ][a-zàáảãạăằẳẵặâầẩẫậđèéẻẽẹêề�ỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỵỄ\s\-']+"
    r",\s*[A-Z][a-zàáảãạăằẳẵặâầẩẫậđèéẻẽẹêề�ỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỵỄ\s\.,]+"
    r",\s*\d{4}"
)

# Index entry pattern
INDEX_ENTRY_RE = re.compile(r"^.+,\s*\d{1,3}(?:[-–]\d{1,3})?(?:,\s*\d{1,3}(?:[-–]\d{1,3})?)*\s*$")


def sup_to_int(run: str) -> int:
    """Convert a superscript digit run (e.g. ⁵³) to an int."""
    return int("".join(str(SUP.index(c)) for c in run))


def strip_page_artifacts(text: str) -> str:
    """Remove embedded === PAGE N === OCR header artifacts."""
    text = PAGE_ARTIFACT_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def classify_line(text: str) -> Tuple[Optional[NodeType], str]:
    """
    Classify a single line of text. Returns (node_type, display_text).
    display_text is the text to render (may be cleaned for headings).
    """
    t = text.strip()
    if not t:
        return None, ""

    # Skip running headers - they are page artifacts, not structural headings
    if is_running_header(t):
        return None, t  # Treat as body text (will be filtered out later)

    # Roman numeral section heading (I, II, III, IV, V, VI)
    if SECTION_RE.match(t):
        return "section_h1", t

    # Arabic numeral section heading (1:, 1, 2, ...)
    m = ARABIC_SECTION_RE.match(t)
    if m and len(t) <= 10:
        return "section_h2", t.rstrip(":").strip()

    # ALL-CAPS section title (short, e.g. "TOÀN TRỊ CHỦ NGHĨA")
    # But exclude running headers (already checked above)
    if ALLCAPS_SECTION_RE.match(t) and len(t) <= 60:
        return "section_h3", t

    return None, t


def is_chapter_title_line(text: str) -> bool:
    """Check if a line looks like a chapter/part title.

    A real title is short. If the line is long, the title is merged with body
    prose on the same line (OCR artifact) -> do NOT treat as a standalone title
    (that would swallow the body and its footnote markers).
    """
    t = text.strip()
    if not t or len(t) < 5:
        return False
    if len(t) > 90:
        return False
    for pat in CHAPTER_TITLE_PATTERNS:
        if pat.search(t):
            return True
    return False


def is_block_quote(text: str) -> bool:
    """Heuristic: long indented paragraph with citation."""
    t = text.strip()
    if len(t) < 80:
        return False
    # Check for citation-like ending (— Author, Year)
    if re.search(r"[—–-]\s*[A-Z][a-zàáảãạăằẳẵặâầẩẫậđèéẻẽẹêềểễệìíỉịỏõọôồốổỗộơờởỡợủűũụýỳỷỵỄ]+\s*,?\s*\d{4}", t):
        return True
    return False


def split_markers(text: str):
    """
    Split body text into [(text, None) | (None, num)] segments by superscript
    footnote marker runs. Preserves the original text between markers.

    Also recognizes global footnote tokens of the form «N» (guillemets around an
    integer), used by the master builder for continuous cross-chapter numbering.
    """
    segs = []
    pos = 0
    # Combined pattern: superscript runs OR «N» global tokens
    pat = re.compile(r"[" + SUP + r"]+|«(\d+)»")
    for m in pat.finditer(text):
        if m.start() > pos:
            segs.append((text[pos:m.start()], None))
        if m.group(1) is not None:
            segs.append((None, int(m.group(1))))
        else:
            segs.append((None, sup_to_int(m.group(0))))
        pos = m.end()
    if pos < len(text):
        segs.append((text[pos:], None))
    return segs


def parse_footnotes(fn_part: str) -> dict:
    """
    Parse the footnote block into {number: text}.
    Handles both superscript prefix (¹ def) and arabic prefix (53. def).
    Strips PAGE artifacts. Preserves _italic_ and *bold* markdown.
    """
    notes = {}
    for line in fn_part.split("\n"):
        s = strip_page_artifacts(line)
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
            m = FOOTNOTE_ARABIC_RE.match(s)
            if not m:
                continue
            num = int(m.group(1))
            text = m.group(2).strip()
        if num not in notes:
            notes[num] = text
    return notes


def parse_body_blocks(body_part: str) -> list:
    """
    Split the body part into paragraph blocks delimited by [V1C##-P###] (trang N).
    Returns list of (para_id, page, raw_text).
    """
    matches = list(PARA_HDR.finditer(body_part))
    blocks = []
    for j, m in enumerate(matches):
        pid = m.group(1)
        page = int(m.group(2))
        start = m.end()
        end = matches[j + 1].start() if j + 1 < len(matches) else len(body_part)
        text = body_part[start:end]
        blocks.append((pid, page, text))
    return blocks


def extract_inline_footnotes(blocks: list, existing_footnotes: dict) -> tuple:
    """
    Extract inline footnote definitions from body blocks.

    Inline footnote definitions appear as lines starting with superscript digits
    (e.g., "¹ Bọn Nazi nhận thức...", "¹³ Xem Deutscher...").

    SAFETY: A leading superscript that is a legitimate footnote *marker* at the
    start of a body paragraph (e.g. "⁶⁰ Cả hai quan...") must NOT be removed.
    We NEVER delete body lines here (no content loss). We only *copy* genuinely
    new inline definitions into the footnotes map; duplicated inline definitions
    are logged as issues but the line is kept in the body so its marker survives.

    Returns (cleaned_blocks, extracted_footnotes, issues)
    """
    extracted = {}
    issues = []

    # Pattern for inline footnote definition: superscript run at start of line
    inline_fn_re = re.compile(r"^(\s*)([" + SUP + r"]+)(\s*)(.*)$")

    def _matches_existing(num: int, fn_text: str) -> bool:
        """True if fn_text is (a prefix of) the existing definition for num."""
        if num not in existing_footnotes:
            return False
        ex = existing_footnotes[num].strip()
        ft = fn_text.strip()
        if not ex or not ft:
            return False
        k = 40
        return ex[:k] == ft[:k] or ft.startswith(ex[:k]) or ex.startswith(ft[:k])

    cleaned_blocks = []
    for pid, page, text in blocks:
        lines = text.split("\n")
        body_lines = []
        for ln in lines:
            m = inline_fn_re.match(ln)
            if m:
                run = m.group(2)
                fn_text = m.group(4).strip()
                num = sup_to_int(run)
                if fn_text and num not in existing_footnotes and num not in extracted:
                    # genuinely new inline definition not in the footnotes block
                    extracted[num] = fn_text
                    body_lines.append(ln)
                elif fn_text and _matches_existing(num, fn_text):
                    # duplicated inline definition -> log but KEEP line in body
                    # (preserves the footnote marker; no content deletion)
                    issues.append({
                        "type": "duplicate_inline_footnote",
                        "footnote_num": num,
                        "para_id": pid,
                        "page": page,
                    })
                    body_lines.append(ln)
                else:
                    # leading superscript is a body marker -> keep
                    body_lines.append(ln)
            else:
                body_lines.append(ln)

        cleaned_text = "\n".join(body_lines)
        cleaned_blocks.append((pid, page, cleaned_text))

    return cleaned_blocks, extracted, issues


def detect_special_block(text: str) -> Optional[NodeType]:
    """
    Detect bibliography or index entry patterns in a block of text.
    """
    t = text.strip()
    if not t:
        return None
    low = t.lower()
    if low.startswith("bibliography") or "bibliography" in low[:20]:
        return "bibliography"
    if INDEX_ENTRY_RE.match(t):
        return "index_entry"
    if BIBLIOGRAPHY_RE.match(t):
        return "bibliography"
    return None


def resolve_cross_page_continuity(blocks: list) -> tuple:
    """
    Resolve cross-page paragraph continuity.
    
    Heuristics:
    - If paragraph ends without terminal punctuation (., !, ?) AND next starts lowercase → MERGE (continuation)
    - If paragraph ends with hyphenated word AND next starts with word fragment → JOIN (split word)
    - If paragraph is Roman numeral heading AND next is body → KEEP SEPARATE
    - If paragraph is Arabic numeral heading AND next is body → KEEP SEPARATE
    - Else if both body and no merge signals → KEEP SEPARATE (new paragraph)
    
    Returns (merged_blocks, continuity_issues)
    """
    if not blocks:
        return [], []
    
    merged = []
    issues = []
    i = 0
    while i < len(blocks):
        pid, page, text = blocks[i]
        text = strip_page_artifacts(text)
        
        # Look ahead to next block
        if i + 1 < len(blocks):
            next_pid, next_page, next_text = blocks[i + 1]
            next_text = strip_page_artifacts(next_text)
            
            # Check if current page != next page (page boundary)
            if page != next_page:
                curr_end = text.rstrip()
                next_start = next_text.lstrip()
                
                # Check for heading at next start (excluding running headers)
                next_is_heading = False
                for ln in next_start.split("\n"):
                    ln = ln.strip()
                    if ln:
                        nt, _ = classify_line(ln)
                        # Running headers return None from classify_line, so they won't be treated as headings
                        if nt:
                            next_is_heading = True
                        break
                
                # Check for continuation signals
                has_terminal = bool(re.search(r"[.!?]\s*$", curr_end))
                next_starts_lower = next_start[:1].islower() if next_start else False
                curr_ends_hyphen = curr_end.endswith("-") or curr_end.endswith("–")
                
                if not has_terminal and next_starts_lower and not next_is_heading:
                    # MERGE: continuation across page boundary
                    merged_text = curr_end + " " + next_start
                    issues.append({
                        "type": "merged_continuation",
                        "page_boundary": f"{page}→{next_page}",
                        "para_ids": f"{pid} + {next_pid}",
                        "status": "MERGED",
                        "unverified": True,  # Flag as UNVERIFIED without source PDF
                    })
                    merged.append((pid, page, merged_text))
                    i += 2
                    continue
                elif curr_ends_hyphen and not next_is_heading:
                    # JOIN: hyphenated word split across pages
                    # Remove hyphen and join
                    word_part = curr_end.rstrip("-–").split()[-1] if curr_end.split() else ""
                    next_word = next_start.split()[0] if next_start.split() else ""
                    joined = curr_end.rstrip("-–") + next_word
                    rest = " ".join(next_start.split()[1:]) if len(next_start.split()) > 1 else ""
                    merged_text = joined + (" " + rest if rest else "")
                    issues.append({
                        "type": "joined_hyphenated",
                        "page_boundary": f"{page}→{next_page}",
                        "para_ids": f"{pid} + {next_pid}",
                        "status": "JOINED",
                        "unverified": True,
                    })
                    merged.append((pid, page, merged_text))
                    i += 2
                    continue
                elif next_is_heading:
                    # KEEP SEPARATE: heading at page start
                    issues.append({
                        "type": "heading_at_page_start",
                        "page_boundary": f"{page}→{next_page}",
                        "para_ids": f"{pid} → {next_pid}",
                        "status": "KEPT_SEPARATE",
                    })
        
        merged.append((pid, page, text))
        i += 1
    
    return merged, issues


def parse(text: str, chapter_label: str = "", vi_title: str = "") -> DocumentModel:
    """
    Parse a v2 translation file's full text into a DocumentModel.
    """
    model = DocumentModel()
    model.chapter_label = chapter_label
    model.title = vi_title or chapter_label

    if "=== FOOTNOTES ===" in text:
        body_part, _, fn_part = text.partition("=== FOOTNOTES ===")
        model.footnotes = parse_footnotes(fn_part)
    else:
        body_part = text
        model.footnotes = {}

    # Parse raw blocks
    raw_blocks = parse_body_blocks(body_part)

    # Strip running headers / chapter titles glued onto body text (segmentation fix).
    # MUST run before inline-footnote extraction and cross-page continuity so that
    # continuation detection sees real body text, not page artifacts.
    raw_blocks, header_strip_log = strip_running_headers(raw_blocks, vi_title=vi_title)
    model.metadata = getattr(model, "metadata", {})
    model.metadata["header_strip_log"] = header_strip_log

    # Extract inline footnote definitions from body blocks
    raw_blocks, inline_footnotes, inline_fn_issues = extract_inline_footnotes(raw_blocks, model.footnotes)
    model.footnotes.update(inline_footnotes)
    model.metadata = getattr(model, 'metadata', {})
    model.metadata["inline_footnote_issues"] = inline_fn_issues
    
    # Extract a chapter/part title that sits on its OWN raw line in the first
    # block (e.g. ch13 "CHƯƠNG MƯỜI BA: Ý thức hệ..."). Must run BEFORE
    # resolve_cross_page_continuity, which collapses newlines and would merge
    # the title into the body. The title is emitted as a chapter node; the body
    # below is parsed normally.
    pre_title = None
    if raw_blocks:
        _rs = raw_blocks[0][2].lstrip("\n")
        _rf = _rs.split("\n", 1)[0].strip()
        if _rf and is_chapter_title_line(_rf):
            pre_title = (_rf, raw_blocks[0][0], raw_blocks[0][1])
            _nl = _rs.find("\n")
            raw_blocks[0] = (raw_blocks[0][0], raw_blocks[0][1],
                             _rs[_nl:] if _nl >= 0 else "")

    # Resolve cross-page continuity
    blocks, continuity_issues = resolve_cross_page_continuity(raw_blocks)
    model.metadata = getattr(model, 'metadata', {})
    model.metadata["cross_page_issues"] = continuity_issues

    # Track first body paragraph for chapter title detection
    first_body_seen = False
    chapter_title_node = None
    part_heading_node = None

    if pre_title is not None:
        _t, _pid, _pg = pre_title
        model.nodes.append(DocNode(
            type="chapter" if ("CHƯƠNG" in _t.upper() or "PHẦN" in _t.upper()) else "part",
            text=_t, level=1, metadata={"para_id": _pid, "page": _pg},
        ))
    
    for pid, page, raw_text in blocks:
        text = strip_page_artifacts(raw_text)
        if not text:
            continue

        # Split block into lines for fine-grained heading detection.
        lines = [ln for ln in text.split("\n") if ln.strip()]
        
        # Filter out running headers and standalone page numbers from lines
        # These are page-level artifacts, not structural content
        filtered_lines = []
        for ln in lines:
            ln_stripped = ln.strip()
            # Skip running headers
            if is_running_header(ln_stripped):
                continue
            # Skip standalone page numbers (1-3 digits, possibly with spaces)
            if re.match(r"^\s*\d{1,3}\s*$", ln_stripped):
                continue
            filtered_lines.append(ln)
        
        lines = filtered_lines
        if not lines:
            continue
        
        # Check for chapter/part title in first few lines of first block
        if not first_body_seen and lines:
            first_line = lines[0].strip()
            if is_chapter_title_line(first_line):
                # This is a chapter/part title
                node = DocNode(
                    type="chapter" if "CHƯƠNG" in first_line.upper() or "PHẦN" in first_line.upper() else "part",
                    text=first_line,
                    level=1,
                    metadata={"para_id": pid, "page": page}
                )
                model.nodes.append(node)
                lines = lines[1:]  # Remove title line from processing
                if not lines:
                    continue

        # Re-join: consecutive non-heading lines form one body paragraph.
        i = 0
        while i < len(lines):
            ln = lines[i].strip()
            node_type, display = classify_line(ln)
            if node_type is not None:
                # Standalone heading line
                node = DocNode(type=node_type, text=display, level={
                    "section_h1": 2,
                    "section_h2": 3,
                    "section_h3": 4,
                }[node_type], metadata={"para_id": pid, "page": page})
                model.nodes.append(node)
                i += 1
            else:
                # Collect consecutive body lines
                body_lines = []
                while i < len(lines):
                    ln2 = lines[i].strip()
                    nt2, _ = classify_line(ln2)
                    if nt2 is not None:
                        break
                    body_lines.append(ln2)
                    i += 1
                body_text = " ".join(body_lines)
                body_text = re.sub(r"\s+", " ", body_text).strip()
                if body_text:
                    # Check for special block types
                    special = detect_special_block(body_text)
                    if special is None and is_block_quote(body_text):
                        special = "block_quote"
                    
                    node = DocNode(
                        type=special if special else "body",
                        text=body_text,
                        level=1 if special else 0,
                        metadata={"para_id": pid, "page": page},
                    )
                    model.nodes.append(node)
                    first_body_seen = True

    # Post-process: Validate heading hierarchy
    validate_heading_hierarchy(model)
    
    # Detect duplicate paragraphs
    detect_duplicate_paragraphs(model)
    
    return model


def validate_heading_hierarchy(model: DocumentModel) -> None:
    """Validate heading hierarchy and flag issues."""
    issues = []
    headings = [n for n in model.nodes if n.type in ("section_h1", "section_h2", "section_h3", "chapter", "part")]
    
    # Check for duplicate headings at same level within chapter
    heading_texts = {}
    for h in headings:
        key = (h.type, h.text)
        if key not in heading_texts:
            heading_texts[key] = []
        heading_texts[key].append(h)
    
    for (h_type, h_text), nodes in heading_texts.items():
        if len(nodes) > 1:
            issues.append({
                "type": "duplicate_heading",
                "level": h_type,
                "text": h_text,
                "locations": [f"{n.metadata.get('para_id')} (trang {n.metadata.get('page')})" for n in nodes]
            })
    
    # Check for skipped heading levels
    levels_seen = set()
    level_map = {"part": 1, "chapter": 1, "section_h1": 2, "section_h2": 3, "section_h3": 4}
    for h in headings:
        levels_seen.add(level_map.get(h.type, 0))
    
    sorted_levels = sorted(levels_seen)
    for i in range(len(sorted_levels) - 1):
        if sorted_levels[i+1] - sorted_levels[i] > 1:
            issues.append({
                "type": "heading_level_skip",
                "from_level": sorted_levels[i],
                "to_level": sorted_levels[i+1],
            })
    
    # Check for false positives: sentences misclassified as headings
    # (e.g., "Khi một phong trào..." is body text, not a heading)
    for h in headings:
        if h.type in ("section_h1", "section_h2", "section_h3"):
            # ALL-CAPS headings that are actually sentences (contain lowercase-like structure)
            if h.type == "section_h3" and len(h.text) > 60:
                issues.append({
                    "type": "possible_false_positive_heading",
                    "level": h.type,
                    "text": h.text[:100],
                    "para_id": h.metadata.get("para_id"),
                    "page": h.metadata.get("page"),
                })
    
    model.metadata = getattr(model, 'metadata', {})
    model.metadata["heading_issues"] = issues


def detect_duplicate_paragraphs(model: DocumentModel) -> None:
    """Detect duplicate or near-duplicate body paragraphs."""
    body_nodes = [n for n in model.nodes if n.type in ("body", "block_quote")]
    text_map = {}
    
    for n in body_nodes:
        # Normalize for comparison
        norm = re.sub(r"\s+", " ", n.text).strip()
        if norm and len(norm) > 50:  # Only check substantial paragraphs
            if norm not in text_map:
                text_map[norm] = []
            text_map[norm].append(n)
    
    duplicates = {text: nodes for text, nodes in text_map.items() if len(nodes) > 1}
    
    issues = []
    for text, nodes in duplicates.items():
        issues.append({
            "type": "duplicate_paragraph",
            "text_preview": text[:200],
            "locations": [f"{n.metadata.get('para_id')} (trang {n.metadata.get('page')})" for n in nodes],
            "count": len(nodes),
        })
    
    model.metadata = getattr(model, 'metadata', {})
    model.metadata["duplicate_issues"] = issues


def audit_vnch_orthography(text: str) -> list:
    """Check VNCH orthography rules in text."""
    issues = []
    
    # Specific term replacements
    term_replacements = [
        ("chính phủ", "chánh phủ"),
        ("thứ trưởng", "bộ trưởng"),
        ("chủ tịch nước", "tổng thống"),
    ]
    
    for wrong, correct in term_replacements:
        matches = list(re.finditer(rf"\b{re.escape(wrong)}\b", text))
        if matches:
            issues.append({
                "rule": f"{wrong} → {correct}",
                "type": "orthography",
                "count": len(matches),
                "positions": [m.start() for m in matches[:10]],
            })
    
    # Northern patterns (flag for review)
    patterns = [
        (r"\bđược\s+\w{3,}", "được passive overuse (Northern pattern)", "grammar_northern"),
        (r"\bcái\s+\w{3,}", "cái classifier overuse (Northern pattern)", "grammar_northern"),
        (r"\brất\s+\w{3,}", "rất vs quá (Northern prefers rất, VNCH prefers quá)", "vocabulary_northern"),
    ]
    
    for pattern, desc, typ in patterns:
        matches = list(re.finditer(pattern, text))
        if matches:
            issues.append({
                "rule": desc,
                "type": typ,
                "count": len(matches),
                "positions": [m.start() for m in matches[:10]],
            })
    
    return issues