# -*- coding: utf-8 -*-
"""
Insert missing footnote reference markers [N] into the Vietnamese body text,
using the paragraph-aligned English source (v1_chNN_src.txt) to locate each
note. Markers 1..3 already exist as bare numbers in the body; this script
adds [4]..[51] as inline markers at ratio-mapped, sentence-snapped positions.

Paragraph correspondence is 1-1 by P-number. Heading lines (blocks whose
header we tagged) are excluded from the ratio base on both sides.

Writes the modified text to a .new file and prints each insertion for review.
It does NOT overwrite the original.
"""
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BLOCK = re.compile(r"--- \[(V1C09-P\d+)\] \([^)]*\)(?: — [^-]+)? ---")
MARKER = re.compile(r"(?<=[^\s\d])(\d{1,3})(?=\s|$)")

# P-numbers whose block begins with a section heading line
HEADING_P = {"V1C09-P001", "V1C09-P005", "V1C09-P013",
             "V1C09-P023", "V1C09-P028", "V1C09-P036"}


def parse_blocks(path):
    raw = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    lines = raw.split("\n")
    blocks = []  # (pnum, header_line, [content lines])
    cur = None
    for ln in lines:
        m = BLOCK.search(ln)
        if m:
            if cur:
                blocks.append(cur)
            cur = [m.group(1), ln.strip(), []]
        elif cur is not None:
            if ln.strip().startswith("--- [Cước chú"):
                blocks.append(cur)
                cur = None
            else:
                cur[2].append(ln)
    if cur:
        blocks.append(cur)
    return blocks


def body_text(content_lines, pnum):
    """Join non-empty lines into one string; drop heading line if applicable."""
    lines = [l.strip() for l in content_lines if l.strip()]
    if pnum in HEADING_P and lines:
        lines = lines[1:]  # drop heading line
    return " ".join(lines)


def snap_sentence(text, pos):
    """Snap position to just after the nearest sentence-ending punctuation."""
    if pos <= 0:
        return 0
    if pos >= len(text):
        return len(text)
    # find sentence boundaries
    bounds = [m.start() + len(m.group(0).rstrip())
              for m in re.finditer(r'[.!?…]["\u201d\u2019]?\s', text)]
    bounds.append(len(text))
    near = min(bounds, key=lambda x: abs(x - pos))
    return near if abs(near - pos) <= 220 else pos


def main():
    src_path = Path(sys.argv[1])
    vi_path = Path(sys.argv[2])

    src_blocks = parse_blocks(src_path)
    vi_blocks = parse_blocks(vi_path)

    src_body = {p: body_text(c, p) for p, _, c in src_blocks}
    src_order = [p for p, _, _ in src_blocks]

    # Sequential extraction of markers 1..51 from src bodies
    expect = 1
    placements = {}  # pnum -> list of (ratio, num)
    for p in src_order:
        text = src_body[p]
        if not text:
            continue
        for m in MARKER.finditer(text):
            num = int(m.group(1))
            if num != expect:
                continue
            ratio = m.start() / max(len(text), 1)
            placements.setdefault(p, []).append((ratio, num))
            expect = num + 1
    found = [n for lst in placements.values() for _, n in lst]
    print(f"Sequential markers found in src: {len(found)} (1..{expect-1})")
    missing = [n for n in range(1, 52) if n not in found]
    if missing:
        print(f"  MISSING in src: {missing}")

    # Build new vi content with inserted [N] for N >= 4
    out_lines = []
    vi_body_map = {p: body_text(c, p) for p, _, c in vi_blocks}
    inserted = []
    for p, header, content in vi_blocks:
        marks = sorted(placements.get(p, []))
        # only insert markers not already present as bare (1,2,3 are bare in body)
        to_insert = [(r, n) for r, n in marks if n >= 4]
        if not to_insert:
            out_lines.append(header)
            out_lines.extend(content)
            continue
        vtext = vi_body_map[p]
        # compute insertion offsets
        offs = []
        prev = 0
        for r, n in to_insert:
            pos = int(round(r * len(vtext)))
            pos = snap_sentence(vtext, pos)
            if pos < prev:
                pos = snap_sentence(vtext, prev + 1)
            offs.append((pos, n))
            prev = pos
        # rebuild content: locate the body line(s) and inject
        # vi body is typically a single non-empty line after heading
        # rebuild by replacing the body line
        new_content = []
        body_done = False
        # find index of first body line (after heading if applicable)
        non_empty_idx = [i for i, l in enumerate(content) if l.strip()]
        if p in HEADING_P and non_empty_idx:
            body_start = non_empty_idx[1] if len(non_empty_idx) > 1 else None
        else:
            body_start = non_empty_idx[0] if non_empty_idx else None

        if body_start is None:
            out_lines.append(header)
            out_lines.extend(content)
            continue

        # assume single body line at body_start; inject markers into it
        line = content[body_start]
        # build new line
        pieces = []
        last = 0
        for pos, n in offs:
            pieces.append(line[last:pos])
            pieces.append(f"[{n}]")
            inserted.append((p, n, line[max(0,pos-25):pos]))
            last = pos
        pieces.append(line[last:])
        newline = "".join(pieces)

        for i, l in enumerate(content):
            if i == body_start:
                new_content.append(newline)
            else:
                new_content.append(l)
        out_lines.append(header)
        out_lines.extend(new_content)

    # Reassemble file: everything before first block (title/meta) + blocks + notes
    raw = vi_path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    # preserve the original header/meta lines (before first block)
    first_block = raw.find("--- [")
    prefix = raw[:first_block]
    # notes block: find from "--- [Cước chú" to end
    notes_idx = raw.find("--- [Cước chú")
    suffix = raw[notes_idx:] if notes_idx != -1 else ""

    new_text = prefix + "\n".join(out_lines) + "\n\n" + suffix
    # normalize excessive blank lines (max 1 blank between blocks)
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)

    out_path = vi_path.with_suffix(".txt.new")
    out_path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"\nInserted {len(inserted)} markers. Output -> {out_path}")
    for p, n, ctx in inserted:
        print(f"  {p} [{n}] ...{ctx}...")


if __name__ == "__main__":
    main()