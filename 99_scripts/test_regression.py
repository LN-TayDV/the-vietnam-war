# -*- coding: utf-8 -*-
"""Regression tests for build_chapter_docx.py (chapters 1-6).
Includes footnote marker completeness checks (BUG-001, BUG-002, BUG-003, BUG-006)."""
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent / "99_scripts"))
import build_chapter_docx as bd

PROJECT = Path(__file__).resolve().parents[1]  # translation-project, same as build_chapter_docx.py
OUT = PROJECT / "09_docx"

FAILURES = []

def check(cond, msg):
    print(("PASS" if cond else "FAIL"), "-", msg)
    if not cond:
        FAILURES.append(msg)

def read_docx(path):
    return zipfile.ZipFile(path)

def strip_tags(xml):
    t = re.sub(r"<[^>]+>", " ", xml)
    t = re.sub(r"\s+", " ", t)
    return t

INLINE_MARKER = re.compile(r"\[(\d{1,3})\]")
NOTE_BLOCK_HEADER = re.compile(r"^--- \[Cước chú (.+?)\] ---\s*$")
NOTE_ENTRY = re.compile(r"^\[(\d{1,3})\]\s+(.+)$")

def parse_notes_and_body_markers(text):
    """Trả về (notes_dict, body_markers_list) từ nội dung TXT."""
    lines = text.split("\n")
    in_notes = False
    notes = {}
    body_lines = []
    for line in lines:
        s = line.strip()
        if NOTE_BLOCK_HEADER.match(s):
            in_notes = True
            continue
        if in_notes:
            if s.startswith("--- [") and not NOTE_BLOCK_HEADER.match(s):
                in_notes = False
                body_lines.append(line)
                continue
            m = NOTE_ENTRY.match(s)
            if m:
                num = int(m.group(1))
                note_text = m.group(2).strip()
                notes.setdefault(num, note_text)
            elif s and not s.startswith("--- ["):
                if notes:
                    last = max(notes)
                    if notes[last]:
                        notes[last] += " " + s
            continue
        body_lines.append(line)

    body_text = "\n".join(body_lines)
    markers = [int(m.group(1)) for m in INLINE_MARKER.finditer(body_text)]
    return notes, markers

def test_footnote_markers(chap_id):
    """Kiểm tra toàn vẹn footnote markers: không missing, không duplicate, không orphan."""
    print(f"\n----- {chap_id} footnote markers -----")
    src = bd.SRC_DIR / f"ch{chap_id}" / f"v1_ch{chap_id}_vi.txt"
    text = src.read_text(encoding="utf-8-sig")
    notes, markers = parse_notes_and_body_markers(text)

    note_nums = set(notes.keys())
    body_nums = set(markers)

    missing = sorted(note_nums - body_nums)
    duplicates = sorted([n for n in body_nums if markers.count(n) > 1])
    orphans = sorted(body_nums - note_nums)

    check(len(missing) == 0, f"{chap_id}: no missing footnote markers (missing: {missing})")
    check(len(duplicates) == 0, f"{chap_id}: no duplicate footnote markers (duplicates: {duplicates})")
    check(len(orphans) == 0, f"{chap_id}: no orphan footnote markers (orphans: {orphans})")
    check(len(notes) == len(markers) and len(notes) == len(body_nums),
          f"{chap_id}: notes count ({len(notes)}) == unique body markers ({len(body_nums)}) == total body markers ({len(markers)})")

    if missing:
        print(f"  MISSING markers: {missing}")
    if duplicates:
        print(f"  DUPLICATE markers: {duplicates}")
    if orphans:
        print(f"  ORPHAN markers: {orphans}")
    if not missing and not duplicates and not orphans:
        print(f"  All {len(notes)} footnote markers match correctly.")

def test_chapter(chap_id, expected_images, expected_notes):
    print(f"\n===== {chap_id} =====")
    src = bd.SRC_DIR / f"ch{chap_id}" / f"v1_ch{chap_id}_vi.txt"
    ch = bd.parse_chapter(src)

    out, words, used, mode_ret, total = bd.build(src)
    z = read_docx(out)
    xml = z.read("word/document.xml").decode("utf-8")

    # 1. Metadata must NOT be in body
    check("02_extracted_text" not in xml, f"{chap_id}: no source-path metadata")
    check("trang in" not in xml, f"{chap_id}: no 'trang in' metadata")
    check("*Bản dịch tiếng Việt ·" not in xml, f"{chap_id}: no colophon metadata")

    # 2. Block headers must not leak into body
    leaked = re.findall(r"--- \[[^\]]+\] \([^)]*\)(?: — [^—]*?)? ---", xml)
    check(len(leaked) == 0, f"{chap_id}: no block-header leaks ({len(leaked)})")

    # 3. Images embedded
    actual_img = xml.count("r:embed")
    check(actual_img == expected_images,
          f"{chap_id}: images embedded ({actual_img}/{expected_images})")

    # 4. Images & captions.
    hinh_pat = re.compile(r"^\s*H\u00ecnh\s+\d+\.\d+")
    para_elems = re.findall(r'(<w:p[^>]*>.*?</w:p>)', xml, re.DOTALL)
    captions = []
    image_paras = set()
    for i, pe in enumerate(para_elems):
        if 'r:embed' in pe:
            image_paras.add(i)
        txt = re.sub(r"<[^>]+>", "", pe)
        txt = re.sub(r"\s+", " ", txt).strip()
        if hinh_pat.match(txt):
            captions.append((i, txt))

    check(actual_img == len(image_paras),
          f"{chap_id}: r:embed count ({actual_img}) == image paragraphs ({len(image_paras)})")
    check(actual_img == expected_images,
          f"{chap_id}: images embedded ({actual_img}/{expected_images})")

    if captions:
        check(len(captions) > 0, f"{chap_id}: at least one true caption")
        for _, c in captions:
            check(not re.search(r"\.png|\.jpg|img\d", c, re.I),
                  f"{chap_id}: caption has no filename: {c[:60]}")
        print(f"   true captions ({len(captions)}):")
        for _, c in captions:
            print("     ", c[:90])
        all_ok = True
        for idx, _ in captions:
            if (idx - 1) not in image_paras:
                all_ok = False
        check(all_ok, f"{chap_id}: every caption immediately preceded by its image")
        check(actual_img == len(captions),
              f"{chap_id}: image count ({actual_img}) == caption count ({len(captions)})")
    else:
        print(f"   true captions: 0 (none in source; images appended at end)")

    # 5. Footnotes native
    try:
        fn = z.read("word/footnotes.xml").decode("utf-8")
        fn_ids = [int(i) for i in re.findall(r'w:footnote w:id="(\d+)"', fn) if int(i) > 0]
        check(len(fn_ids) == expected_notes,
              f"{chap_id}: native footnotes ({len(fn_ids)}/{expected_notes})")
    except KeyError:
        check(False, f"{chap_id}: footnotes.xml MISSING")

    nref = xml.count("w:footnoteReference")
    print(f"   body footnote refs: {nref}, source notes: {expected_notes}")
    return out, xml

def main():
    cases = {}
    for chap in ["01", "02", "03", "04", "05", "06"]:
        img_dir = PROJECT / "04_translation" / "v1" / "images"
        n_img = len(list(img_dir.glob(f"ch{chap}_p*_img*.png")))
        src = bd.SRC_DIR / f"ch{chap}" / f"v1_ch{chap}_vi.txt"
        ch = bd.parse_chapter(src)
        cases[chap] = (n_img, len(ch["notes"]))
        print(f"[case] {chap}: images={n_img}, notes={len(ch['notes'])}")

    # --- Test footnote markers FIRST (BUG-001, BUG-002, BUG-003, BUG-006) ---
    for chap in ["01", "02", "03", "04", "05", "06"]:
        test_footnote_markers(chap)

    # --- Build DOCX tests ---
    for chap in ["01", "02", "03", "04", "05", "06"]:
        n_img, n_notes = cases[chap]
        test_chapter(chap, n_img, n_notes)

    print("\n================ RESULT ================")
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S):")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    else:
        print("ALL TESTS PASSED")

if __name__ == "__main__":
    main()
