# -*- coding: utf-8 -*-
"""
SURGICAL insert of the MISSING footnote reference markers into the vi body.
Existing bare markers (already correctly placed) are left untouched. Only the
truly-missing notes are inserted as inline [N] at ratio-mapped, sentence-snapped
positions derived from the paragraph-aligned English source.

Special cases:
  - P034: note 48 belongs to the SECOND body line -> appended there.
  - P014: the run "20 21" (note 21 space-separated) -> rewritten "[20][21]".

Writes to <vi>.new and prints every insertion for review. Does NOT overwrite.
"""
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BLOCK = re.compile(r"--- \[(V1C09-P\d+)\] \([^)]*\)(?: — [^-]+)? ---")
MARKER = re.compile(r"(?<=[^\s\d])(\d{1,3})(?=\s|$)")
HEADING_P = {"V1C09-P001", "V1C09-P005", "V1C09-P013",
             "V1C09-P023", "V1C09-P028", "V1C09-P036"}


def parse_blocks(path):
    raw = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    lines = raw.split("\n")
    blocks = []
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


def body_text(content, pnum):
    lines = [l.strip() for l in content if l.strip()]
    if pnum in HEADING_P and lines:
        lines = lines[1:]
    return " ".join(lines)


def snap_sentence(text, pos):
    if pos <= 0:
        return 0
    if pos >= len(text):
        return len(text)
    bounds = [m.start() + len(m.group(0).rstrip())
              for m in re.finditer(r'[.!?…]["\u201d\u2019]?\s', text)]
    bounds.append(len(text))
    near = min(bounds, key=lambda x: abs(x - pos))
    return near if abs(near - pos) <= 220 else pos


def main():
    src_path = Path(sys.argv[1])
    vi_path = Path(sys.argv[2])

    # --- src ratios ---
    src_blocks = parse_blocks(src_path)
    src_order = [p for p, _, _ in src_blocks]
    src_body = {p: body_text(c, p) for p, _, c in src_blocks}
    expect = 1
    src_marks = {}  # pnum -> list[(ratio, num)]
    for p in src_order:
        text = src_body[p]
        if not text:
            continue
        for m in MARKER.finditer(text):
            num = int(m.group(1))
            if num != expect:
                continue
            src_marks.setdefault(p, []).append((m.start() / max(len(text), 1), num))
            expect = num + 1
    all_nums = [n for lst in src_marks.values() for _, n in lst]
    assert all_nums == list(range(1, 52)), f"src markers not 1..51: {all_nums}"

    # --- vi blocks + present markers ---
    vi_blocks = parse_blocks(vi_path)
    vi_body = {p: body_text(c, p) for p, _, c in vi_blocks}
    present = set()
    for p in vi_body:
        for m in MARKER.finditer(vi_body[p]):
            present.add(int(m.group(1)))

    missing = [n for n in range(1, 52) if n not in present and n != 21]
    print(f"Missing to insert: {missing}")

    # group missing markers by block
    ins_by_block = {}
    for p, lst in src_marks.items():
        for r, n in lst:
            if n in missing:
                ins_by_block.setdefault(p, []).append((r, n))

    # Build new content
    out = []
    inserted = []
    for p, header, content in vi_blocks:
        # Fix P014 run "20 21" -> "[20][21]"
        if p == "V1C09-P014":
            new_content = []
            for l in content:
                if "20 21" in l:
                    l = l.replace("20 21", "[20][21]")
                new_content.append(l)
            out.append(header)
            out.extend(new_content)
            continue

        marks = sorted(ins_by_block.get(p, []))
        if not marks:
            out.append(header)
            out.extend(content)
            continue

        # Identify body line indices (exclude heading)
        nonempty = [i for i, l in enumerate(content) if l.strip()]
        if p in HEADING_P and nonempty:
            body_idx = nonempty[1:]
        else:
            body_idx = nonempty

        if p == "V1C09-P034":
            # note 48 -> end of last body line
            last = body_idx[-1]
            line = content[last]
            pieces = [line, "[48]"]
            inserted.append((p, 48, line[-30:]))
            content = list(content)
            content[last] = "".join(pieces)
            out.append(header)
            out.extend(content)
            continue

        # single body line expected
        assert len(body_idx) == 1, f"{p} has {len(body_idx)} body lines"
        bi = body_idx[0]
        line = content[bi]
        vtext = vi_body[p]
        # compute absolute insertion offsets, right-to-left
        offs = []
        prev = 0
        for r, n in marks:
            pos = int(round(r * len(vtext)))
            pos = snap_sentence(vtext, pos)
            if pos < prev:
                pos = snap_sentence(vtext, prev + 1)
            offs.append((pos, n))
            prev = pos
        # insert right-to-left into the line
        newline = line
        for pos, n in sorted(offs, key=lambda x: -x[0]):
            newline = newline[:pos] + f"[{n}]" + newline[pos:]
            inserted.append((p, n, line[max(0, pos-28):pos]))
        content = list(content)
        content[bi] = newline
        out.append(header)
        out.extend(content)

    # reassemble
    raw = vi_path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    first_block = raw.find("--- [")
    prefix = raw[:first_block]
    notes_idx = raw.find("--- [Cước chú")
    suffix = raw[notes_idx:] if notes_idx != -1 else ""
    new_text = prefix + "\n".join(out) + "\n\n" + suffix
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)

    out_path = vi_path.with_suffix(".txt.new")
    out_path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"\nInserted {len(inserted)} markers (+P014 fix) -> {out_path}")
    for p, n, ctx in inserted:
        print(f"  {p} [{n}] ...{ctx}...")


if __name__ == "__main__":
    main()