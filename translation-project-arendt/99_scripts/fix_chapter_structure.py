# -*- coding: utf-8 -*-
"""
Structural fixes for all 13 v2 chapter files.
- Separate chapter title from body (ch01, ch12)
- Remove running header text prepended to body paragraphs
- Remove page numbers leaked into body
- Mark empty paragraphs with [TRONG] placeholder
- Remove duplicate paragraphs (keep first)
- Extract inline footnote definitions from body to FOOTNOTES block (ch12)
- Remove standalone orphaned numbers (ch12 "1:")
- Preserve === FOOTNOTES === block intact
- Idempotent; outputs a change report
"""
import re
import sys
import unicodedata
from pathlib import Path
from typing import List, Tuple, Dict, Any

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "04_translation" / "v2"

# ============================================================
# Running header patterns (VNCH and English) — these are page-level
# artifacts that got prepended to body paragraphs during OCR/segmentation.
# ============================================================
VNCH_RUNNING_HEADERS = [
    "DÂN TỘC QUỐC GIA, SỰ RA ĐỜI CHỦ NGHĨA PHÂN BIỆT CHỦNG TỘC DO THÁI",
    "CHỦ NGHĨA ĐẾ QUỐC",
    "TƯ DUY VỀ CHỦNG TỘC TRƯỚC CHỦ NGHĨA PHÂN BIỆT CHỦNG TỘC",
    "CHỦ NGHĨA TOÀN TRỊ",
    "CHỦ NGHĨA PHÂN BIỆT CHỦNG TỘC DO THÁI",
    "VỤ DREYFUS",
    "GIẢI PHÓP CHÍNH TRỊ CỦA TIỂU SẢN",
    "CHỦNG TỘC VÀ QUAN LIÊU",
    "CHỦ NGHĨA ĐẾ QUỐC LỤC ĐỊA: CÁC PHONG TRÀO PAN",
    "SỰ SUY TÀN CỦA QUỐC GIA QUỐC DÂN VÀ HẾT HẠN QUYỀN CON NGƯỜI",
    "XÃ HỘI KHÔNG GIAI CẤP",
    "PHONG TRÀO TOÀN TRỊ",
    "Ý THỨC HỆ VÀ KHỦNG BỐ",
    "TOÀN TRỊ TẠI QUYỀN",
]

EN_RUNNING_HEADERS = [
    "THE NATION-STATE; THE BIRTH OF ANTISEMITISM",
    "TOTALITARIANISM IN POWER",
    "ANTISEMITISM",
    "IMPERIALISM",
    "THE DREYFUS AFFAIR",
    "RACE THINKING BEFORE RACE IDEOLOGY",
    "THE DECLINE OF THE NATION STATE",
    "A CLASSLESS SOCIETY",
    "THE TOTALITARIAN MOVEMENT",
    "IDEOLOGY AND TERROR",
]

# All running headers for detection (case-insensitive)
ALL_RUNNING_HEADERS = VNCH_RUNNING_HEADERS + EN_RUNNING_HEADERS

# Page numbers leaked into body text (as standalone lines)
LEAKED_PAGE_NUMBERS = {"390", "391", "392", "393", "394"}

# Chapters with empty paragraphs to mark
EMPTY_PARAGRAPHS = {
    "ch01": ["P004", "P005"],
    "ch02": [f"P{str(i).zfill(3)}" for i in range(1, 27)],  # P001-P026
    "ch10": ["P007", "P008"],
}

# Duplicate paragraphs to remove (keep first occurrence)
DUPLICATE_PARAGRAPHS = {
    "ch09": ["P009"],  # P009 is duplicate of P008
    "ch10": ["P004"],  # P004 is duplicate of P003
    "ch13": ["P010"],  # P010 is duplicate of P009
}

# Chapter title separation: chapters where P001 has title merged with body
CHAPTER_TITLE_MERGED = {
    "ch01": {
        "title": "CHƯƠNG NHẤT: CHỦ NGHĨA PHÂN BIỆT CHỦNG TỘC DO THÁI LÀ MỘT SỰ QUÁ ĐÁNG ĐỐI VỚI LẺ THƯỜNG",
        "title_id": "P000",
    },
    "ch12": {
        "title": "C H A P T E R T W E L V E :\nCHỦ NGHĨA TOÀN TRỊ TRONG QUYỀN LỰC",
        "title_id": "P000",
    },
}

# Inline footnote definitions to extract from body (ch12 P001-P005)
# These are lines starting with superscript digits followed by footnote text
CH12_INLINE_FOOTNOTES = {
    # Will be detected dynamically: lines starting with ¹²³⁴⁵ in P001-P005
}

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def sup_to_int(run: str) -> int:
    return int("".join(str(SUP.index(c)) for c in run))


def parse_paras(text: str) -> List[Tuple[str, str, str]]:
    """Parse text into list of (para_id, page, body_text)."""
    pattern = re.compile(r"(?m)^\[(V1\w*C\d+-P\d{3})\] \(trang (\d+)\)\s*$")
    matches = list(pattern.finditer(text))
    blocks = []
    for j, m in enumerate(matches):
        pid = m.group(1)
        page = m.group(2)
        start = m.end()
        end = matches[j + 1].start() if j + 1 < len(matches) else len(text)
        body = text[start:end]
        blocks.append((pid, page, body))
    return blocks


def serialize_paras(blocks: List[Tuple[str, str, str]]) -> str:
    """Serialize paragraph blocks back to text format."""
    out = []
    for pid, page, body in blocks:
        out.append(f"[{pid}] (trang {page})")
        out.append(body.rstrip())
        out.append("")  # blank line between paragraphs
    return "\n".join(out).strip() + "\n"


def remove_running_header_from_body(body: str) -> Tuple[str, bool]:
    """Remove running header text prepended to body. Returns (cleaned_body, changed)."""
    lines = body.split("\n")
    if not lines:
        return body, False

    # Skip leading empty lines
    first_non_empty_idx = 0
    while first_non_empty_idx < len(lines) and not lines[first_non_empty_idx].strip():
        first_non_empty_idx += 1
    
    if first_non_empty_idx >= len(lines):
        return body, False

    first_line = lines[first_non_empty_idx].strip()
    # Check if first line starts with a running header
    for header in ALL_RUNNING_HEADERS:
        if first_line.upper().startswith(header.upper()):
            # Remove the header portion
            # The header might be followed by space or directly by text
            remainder = first_line[len(header):].lstrip(" .,;:")
            if remainder:
                lines[first_non_empty_idx] = remainder
            else:
                lines.pop(first_non_empty_idx)
            return "\n".join(lines), True

    return body, False


def remove_leaked_page_numbers(body: str) -> Tuple[str, bool]:
    """Remove standalone page numbers from body. Returns (cleaned_body, changed)."""
    lines = body.split("\n")
    new_lines = []
    changed = False
    for line in lines:
        stripped = line.strip()
        if stripped in LEAKED_PAGE_NUMBERS:
            changed = True
            continue
        new_lines.append(line)
    return "\n".join(new_lines), changed


def mark_empty_paragraphs(blocks: List[Tuple[str, str, str]], ch: str) -> Tuple[List[Tuple[str, str, str]], List[str]]:
    """Mark empty paragraphs with [TRONG] placeholder. Returns (new_blocks, changes)."""
    changes = []
    empty_pids = set(EMPTY_PARAGRAPHS.get(ch, []))
    new_blocks = []
    for pid, page, body in blocks:
        short_pid = pid.split("-")[-1]  # e.g., "P004"
        if short_pid in empty_pids and not body.strip():
            placeholder = f"[TRONG] (UNVERIFIED - {short_pid} Paragraph trống, cần kiểm tra bản gốc)"
            new_blocks.append((pid, page, placeholder))
            changes.append(f"{ch}: {pid} marked as [TRONG]")
        else:
            new_blocks.append((pid, page, body))
    return new_blocks, changes


def remove_duplicate_paragraphs(blocks: List[Tuple[str, str, str]], ch: str) -> Tuple[List[Tuple[str, str, str]], List[str]]:
    """Remove duplicate paragraphs (keep first occurrence). Returns (new_blocks, changes)."""
    changes = []
    duplicate_pids = set(DUPLICATE_PARAGRAPHS.get(ch, []))
    new_blocks = []
    seen_bodies = {}
    for pid, page, body in blocks:
        short_pid = pid.split("-")[-1]
        if short_pid in duplicate_pids:
            # Check if body matches a previous paragraph
            norm_body = re.sub(r"\s+", " ", body.strip())
            if norm_body in seen_bodies:
                changes.append(f"{ch}: {pid} removed (duplicate of {seen_bodies[norm_body]})")
                continue  # skip this duplicate
            else:
                seen_bodies[norm_body] = pid
        else:
            norm_body = re.sub(r"\s+", " ", body.strip())
            if norm_body and len(norm_body) > 50:
                seen_bodies[norm_body] = pid
        new_blocks.append((pid, page, body))
    return new_blocks, changes


def separate_chapter_title(blocks: List[Tuple[str, str, str]], ch: str) -> Tuple[List[Tuple[str, str, str]], List[str]]:
    """Separate chapter title from first body paragraph. Returns (new_blocks, changes)."""
    changes = []
    if ch not in CHAPTER_TITLE_MERGED:
        return blocks, changes

    title_info = CHAPTER_TITLE_MERGED[ch]
    title_text = title_info["title"]
    title_id = f"[V1C{ch[2:4].upper()}-{title_info['title_id']}]"

    # Find P001 block
    new_blocks = []
    for i, (pid, page, body) in enumerate(blocks):
        short_pid = pid.split("-")[-1]
        if short_pid == "P001":
            # Check if body starts with the title
            if body.strip().startswith(title_text.strip().split("\n")[0].strip()[:50]):
                # Remove title from body
                body_without_title = body.replace(title_text, "", 1).lstrip("\n ")
                # Insert title as separate block before P001
                new_blocks.append((title_id, page, title_text))
                new_blocks.append((pid, page, body_without_title))
                changes.append(f"{ch}: Separated chapter title from {pid} -> {title_id}")
            else:
                new_blocks.append((pid, page, body))
        else:
            new_blocks.append((pid, page, body))
    return new_blocks, changes


def remove_orphaned_numbers(body: str) -> Tuple[str, bool]:
    """Remove standalone orphaned numbers like '1:' from body. Returns (cleaned_body, changed)."""
    lines = body.split("\n")
    new_lines = []
    changed = False
    for line in lines:
        stripped = line.strip()
        # Match standalone "1:" or "1" at start of line (orphaned section numbers)
        if re.match(r"^\d{1,3}\s*:?\s*$", stripped):
            changed = True
            continue
        new_lines.append(line)
    return "\n".join(new_lines), changed


def extract_ch12_inline_footnotes(blocks: List[Tuple[str, str, str]]) -> Tuple[List[Tuple[str, str, str]], Dict[int, str], List[str]]:
    """Extract inline footnote definitions (¹-⁵) from ch12 P001-P005 body text.
    Returns (cleaned_blocks, extracted_footnotes, changes)."""
    changes = []
    extracted = {}
    new_blocks = []

    # Pattern for inline footnote definition at start of line
    inline_fn_re = re.compile(rf"^([{SUP}]+)\s*(.+)$")

    for pid, page, body in blocks:
        short_pid = pid.split("-")[-1]
        if short_pid in ["P001", "P002", "P003", "P004", "P005"]:
            lines = body.split("\n")
            body_lines = []
            for line in lines:
                m = inline_fn_re.match(line.strip())
                if m:
                    run = m.group(1)
                    fn_text = m.group(2).strip()
                    if fn_text:
                        num = sup_to_int(run)
                        if num not in extracted:
                            extracted[num] = fn_text
                            changes.append(f"ch12: Extracted inline footnote {num} from {pid}: {fn_text[:60]}...")
                            continue  # remove from body
                body_lines.append(line)
            new_body = "\n".join(body_lines)
            new_blocks.append((pid, page, new_body))
        else:
            new_blocks.append((pid, page, body))

    return new_blocks, extracted, changes


def integrate_footnotes(fn_block: str, extracted: Dict[int, str]) -> Tuple[str, List[str]]:
    """Integrate extracted footnotes into the FOOTNOTES block. Returns (new_fn_block, changes)."""
    changes = []
    if not extracted:
        return fn_block, changes

    lines = fn_block.split("\n")
    existing_nums = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line[0] in SUP:
            run = ""
            for c in line:
                if c in SUP:
                    run += c
                else:
                    break
            if run:
                existing_nums.add(sup_to_int(run))
        else:
            m = re.match(r"^(\d{1,3})\.\s", line)
            if m:
                existing_nums.add(int(m.group(1)))

    # Add missing footnotes
    for num in sorted(extracted.keys()):
        if num not in existing_nums:
            sup = "".join(SUP[int(d)] for d in str(num))
            lines.append(f"{sup} {extracted[num]}")
            changes.append(f"ch12: Added footnote {num} to FOOTNOTES block")

    return "\n".join(lines), changes


def process_chapter(ch: str) -> List[str]:
    """Process a single chapter file. Returns list of changes made."""
    path = V2 / ch / f"v1_{ch}_vi.txt"
    if not path.exists():
        return [f"SKIP {ch}: file not found"]

    raw = path.read_text(encoding="utf-8")
    raw = raw.replace("\r\n", "\n")

    # Partition body and footnotes
    body_part, sep, fn_part = raw.partition("=== FOOTNOTES ===")
    if not sep:
        return [f"SKIP {ch}: no FOOTNOTES block"]

    all_changes = []

    # Parse body paragraphs
    blocks = parse_paras(body_part)

    # 1. Separate chapter title from body (ch01, ch12)
    blocks, changes = separate_chapter_title(blocks, ch)
    all_changes.extend(changes)

    # 2. Remove running headers from body paragraphs
    for i, (pid, page, body) in enumerate(blocks):
        cleaned, changed = remove_running_header_from_body(body)
        if changed:
            blocks[i] = (pid, page, cleaned)
            all_changes.append(f"{ch}: {pid} removed running header")

    # 3. Remove leaked page numbers
    for i, (pid, page, body) in enumerate(blocks):
        cleaned, changed = remove_leaked_page_numbers(body)
        if changed:
            blocks[i] = (pid, page, cleaned)
            all_changes.append(f"{ch}: {pid} removed leaked page number")

    # 4. Remove orphaned numbers (ch12 "1:")
    for i, (pid, page, body) in enumerate(blocks):
        cleaned, changed = remove_orphaned_numbers(body)
        if changed:
            blocks[i] = (pid, page, cleaned)
            all_changes.append(f"{ch}: {pid} removed orphaned number")

    # 5. Mark empty paragraphs
    blocks, changes = mark_empty_paragraphs(blocks, ch)
    all_changes.extend(changes)

    # 6. Remove duplicate paragraphs
    blocks, changes = remove_duplicate_paragraphs(blocks, ch)
    all_changes.extend(changes)

    # 7. Extract ch12 inline footnotes
    extracted_fns = {}
    if ch == "ch12":
        blocks, extracted_fns, changes = extract_ch12_inline_footnotes(blocks)
        all_changes.extend(changes)

    # Rebuild body part
    new_body = serialize_paras(blocks)

    # 8. Integrate extracted footnotes into FOOTNOTES block
    new_fn_part = fn_part
    if extracted_fns:
        new_fn_part, changes = integrate_footnotes(fn_part, extracted_fns)
        all_changes.extend(changes)

    # Reconstruct full text
    new_text = new_body + "\n" + sep + "\n" + new_fn_part.strip() + "\n"
    new_text = unicodedata.normalize("NFC", new_text)

    if new_text != raw:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        all_changes.append(f"{ch}: FILE UPDATED")
    else:
        all_changes.append(f"{ch}: no changes")

    return all_changes


def main():
    chapters = [f"ch{i:02d}" for i in range(1, 14)]
    all_changes = []

    for ch in chapters:
        changes = process_chapter(ch)
        all_changes.extend(changes)
        for c in changes:
            print(c)

    # Write report
    report_path = ROOT / "STRUCTURE_FIX_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Structure Fix Report\n\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().isoformat()}\n\n")
        for c in all_changes:
            f.write(f"- {c}\n")

    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    main()