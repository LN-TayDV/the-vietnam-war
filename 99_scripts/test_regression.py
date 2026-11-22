# -*- coding: utf-8 -*-
"""Regression tests for build_chapter_docx.py (chapters 1-6)."""
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
    #    Parse paragraphs in document order.  A "true caption" is a paragraph
    #    whose text STARTS with "Hinh X.Y" (anchored).  Inline refs like
    #    "(Hinh 1.1)" inside body text are NOT captions.
    hinh_pat = re.compile(r"^\s*H\u00ecnh\s+\d+\.\d+")
    # split document.xml into paragraph elements in order
    para_elems = re.findall(r'(<w:p[^>]*>.*?</w:p>)', xml, re.DOTALL)
    captions = []   # (index in para_elems, text)
    image_paras = set()  # indexes of paragraphs containing r:embed
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
        # each caption must not leak filename/ID
        for _, c in captions:
            check(not re.search(r"\.png|\.jpg|img\d", c, re.I),
                  f"{chap_id}: caption has no filename: {c[:60]}")
        print(f"   true captions ({len(captions)}):")
        for _, c in captions:
            print("     ", c[:90])
        # every caption paragraph must be immediately preceded by an image paragraph
        all_ok = True
        for idx, _ in captions:
            if (idx - 1) not in image_paras:
                all_ok = False
        check(all_ok, f"{chap_id}: every caption immediately preceded by its image")
        # image count should match caption count (1 image per caption)
        check(actual_img == len(captions),
              f"{chap_id}: image count ({actual_img}) == caption count ({len(captions)})")
    else:
        print(f"   true captions: 0 (none in source; images appended at end)")
        # images still embedded (handled above)

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
