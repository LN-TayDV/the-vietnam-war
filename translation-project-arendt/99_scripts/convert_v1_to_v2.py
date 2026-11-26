#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert v1 extracted text (raw PDF dump with === PAGE N === markers) to v2
source format with [V1CNN-PNNN] (trang N) paragraph headers.

Usage:
    python 99_scripts/convert_v1_to_v2.py [ch01 ch02 ...]
    python 99_scripts/convert_v1_to_v2.py --all

Input:  02_extracted_text/v1/<ch>.txt
Output: 02_extracted_text/v2/<ch>_src.txt

Cleaning steps:
  1. Remove === PAGE N === markers
  2. Remove running header lines (page number + section title repeats)
  3. Dehyphenate words split across line breaks (- at EOL)
  4. Join lines within a paragraph (single \n -> space)
  5. Split paragraphs on blank lines (\n\n)
  6. Add [V1CNN-PNN] (trang N) header per paragraph
  7. Track page number per paragraph from surrounding PAGE markers
"""

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V1 = ROOT / "02_extracted_text" / "v1"
V2 = ROOT / "02_extracted_text" / "v2"

# Running header patterns (English, from Arendt's book)
RUNNING_HEADER_RE = re.compile(
    r"^(?:ANTISEMITISM\s+AS\s+AN\s+OUTRAGE\s+TO\s+COMMON\s+SENSE|"
    r"ANTISEMITISM\s+(?:AS\s+AN\s+OUTRAGE\s+TO\s+COMMON\s+SENSE\s*)?\d*$|"
    r"IMPERIALISM\s*\d*$|"
    r"THE\s+DREYFUS\s+AFFAIR\s*\d*$|"
    r"RACE\s+THINKING\s+BEFORE\s+RACE\s+IDEOLOGY\s*\d*$|"
    r"THE\s+DECLINE\s+OF\s+THE\s+NATION\s+STATE\s*\d*$|"
    r"A\s+CLASSLESS\s+SOCIETY\s*\d*$|"
    r"THE\s+TOTALITARIAN\s+MOVEMENT\s*\d*$|"
    r"IDEOLOGY\s+AND\s+TERROR\s*\d*$|"
    r"TOTALITARIANISM\s+IN\s+POWER\s*\d*$|"
    r"\d+\s+ANTISEMITISM\s*$|"
    r"^\d+\s*$)"  # standalone page number
    , re.IGNORECASE
)

PAGE_MARKER_RE = re.compile(r"===\s*PAGE\s+(\d+)\s*===")

CHAPTER_MAP = {
    "front_matter": "C00",
    "preface_first_edition": "C00",
    "preface_part_one": "C00",
    "preface_part_two": "C00",
    "preface_part_three": "C00",
    "part_one_intro": "C00",
    "ch01": "C01",
    "ch02": "C02",
    "ch03": "C03",
    "ch04": "C04",
    "ch05": "C05",
    "ch06": "C06",
    "ch07": "C07",
    "ch08": "C08",
    "ch09": "C09",
    "ch10": "C10",
    "ch11": "C11",
    "ch12": "C12",
    "ch13": "C13",
}


def clean_text(raw: str) -> list[tuple[str, int]]:
    """
    Return list of (paragraph_text, page_number) tuples.
    """
    lines = raw.split("\n")
    paragraphs = []
    current_para_lines = []
    current_page = None
    para_buf = []

    def flush_para():
        nonlocal para_buf, current_page
        if para_buf:
            text = " ".join(para_buf).strip()
            # Collapse multiple spaces
            text = re.sub(r"\s+", " ", text)
            if text:
                paragraphs.append((text, current_page or 0))
        para_buf = []

    for line in lines:
        stripped = line.strip()

        # Check for page marker
        m = PAGE_MARKER_RE.match(stripped)
        if m:
            flush_para()
            current_page = int(m.group(1))
            continue

        # Skip running headers
        if RUNNING_HEADER_RE.match(stripped):
            continue

        # Skip empty lines -> paragraph break
        if not stripped:
            flush_para()
            continue

        # Dehyphenate: if line ends with -, join with next (no space)
        if stripped.endswith("-"):
            para_buf.append(stripped[:-1])
        else:
            para_buf.append(stripped)

    flush_para()
    return paragraphs


def convert(ch_name: str):
    src_v1 = V1 / f"{ch_name}.txt"
    if not src_v1.exists():
        print(f"SKIP {ch_name}: v1 source not found: {src_v1}")
        return

    raw = src_v1.read_text(encoding="utf-8")
    paras = clean_text(raw)

    ch_code = CHAPTER_MAP.get(ch_name, ch_name.upper())
    V2.mkdir(parents=True, exist_ok=True)
    out_path = V2 / f"{ch_name}_src.txt"

    lines_out = []
    for i, (text, page) in enumerate(paras, 1):
        pid = f"V1{ch_code}-P{i:03d}"
        lines_out.append(f"[{pid}] (trang {page})")
        lines_out.append(text)
        lines_out.append("")

    out_text = "\n".join(lines_out).rstrip() + "\n"
    out_path.write_text(out_text, encoding="utf-8", newline="\n")
    print(f"OK {ch_name}: {len(paras)} paragraphs -> {out_path}")


def main():
    wanted = [a for a in sys.argv[1:] if a.strip() and a != "--all"]
    if "--all" in sys.argv:
        wanted = sorted(p.stem for p in V1.glob("*.txt"))
    if not wanted:
        print("Usage: python 99_scripts/convert_v1_to_v2.py ch01 [ch02 ...]")
        print("       python 99_scripts/convert_v1_to_v2.py --all")
        return 1
    for ch in wanted:
        convert(ch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
