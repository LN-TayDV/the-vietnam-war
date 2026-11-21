#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_images.py — Trích xuất hình ảnh raster từ PDF theo chương, tạo image manifest.

Công đoạn bắt buộc trong pipeline extraction:
  PDF SOURCE → PDF STRUCTURE INSPECTION → PAGE INVENTORY → TEXT EXTRACTION
  → IMAGE EXTRACTION → IMAGE MANIFEST → RAW TEXT WITH IMAGE REFERENCES
  → DOCX GENERATION → DOCX IMAGE VALIDATION → CHAPTER COMPLETENESS REPORT

Usage:
    python 99_scripts/extract_images.py <chapter> [--volume v1] [--dry-run]

Ví dụ:
    python 99_scripts/extract_images.py 09 --volume v1

Output:
  - Ảnh raster được lưu tại:
      translation-project/04_translation/v<vol>/images/ch<NN>_p<PDF_PAGE>_img<IDX>.png
  - Image manifest được lưu tại:
      translation-project/00_plan/image_manifest.json
    Mỗi entry: image_id, source_pdf, volume, chapter, pdf_page, printed_page,
               filename, image_type, width, height, caption, extraction_status
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import pymupdf


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project").is_dir():
            return parent
    return Path.cwd()


def printed_label(page) -> int | None:
    """Lấy số trang in (printed page label) từ 4 dòng đầu của trang."""
    for line in page.get_text("text").split("\n")[:4]:
        m = re.fullmatch(r"\s*(\d{1,4})\s*", line)
        if m:
            return int(m.group(1))
    return None


def find_chapter_range(manifest: dict, volume: str, chapter: int) -> dict | None:
    """Tìm entry chapter trong manifest.json."""
    for ch in manifest.get("chapters", []):
        if ch["volume"] == volume and ch["chapter"] == chapter:
            return ch
    return None


def extract_images_for_chapter(
    pdf_path: str,
    volume: str,
    chapter: int,
    manifest: dict,
    images_dir: Path,
    dry_run: bool = False,
) -> list[dict]:
    """Trích xuất tất cả ảnh raster từ các trang của một chương."""
    ch_entry = find_chapter_range(manifest, volume.upper(), chapter)
    if ch_entry is None:
        print(f"ERROR: Không tìm thấy chương {volume}-{chapter} trong manifest.json")
        return []

    pdf_start = ch_entry["pdf_start"]
    pdf_end = ch_entry["pdf_end"]
    images_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    entries: list[dict] = []
    img_counter = 0

    for pi in range(pdf_start - 1, pdf_end):  # 0-indexed
        page = doc[pi]
        pdf_page = pi + 1
        printed = printed_label(page)

        # --- Raster images ---
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                pix = pymupdf.Pixmap(doc, xref)
                if pix.n - pix.alpha > 3:
                    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                filename = f"ch{chapter:02d}_p{pdf_page:03d}_img{img_index}.png"
                out_path = images_dir / filename
                if not dry_run:
                    pix.save(str(out_path))
                entries.append({
                    "image_id": f"{volume.lower()}-C{chapter:02d}-IMG{img_counter+1:03d}",
                    "source_pdf": pdf_path,
                    "volume": volume,
                    "chapter": chapter,
                    "pdf_page": pdf_page,
                    "printed_page": printed,
                    "filename": filename,
                    "image_type": "raster",
                    "width": pix.width,
                    "height": pix.height,
                    "caption": "",
                    "extraction_status": "OK" if not dry_run else "DRY_RUN",
                })
                img_counter += 1
            except Exception as e:
                entries.append({
                    "image_id": f"{volume.lower()}-C{chapter:02d}-IMG{img_counter+1:03d}",
                    "source_pdf": pdf_path,
                    "volume": volume,
                    "chapter": chapter,
                    "pdf_page": pdf_page,
                    "printed_page": printed,
                    "filename": f"ch{chapter:02d}_p{pdf_page:03d}_img{img_index}",
                    "image_type": "raster",
                    "width": 0,
                    "height": 0,
                    "caption": "",
                    "extraction_status": f"FAIL: {e}",
                })
                img_counter += 1

        # --- Vector drawings (count only, do not extract as image) ---
        drawings = page.get_drawings()
        if drawings:
            entries.append({
                "image_id": f"{volume.lower()}-C{chapter:02d}-VEC{img_counter+1:03d}",
                "source_pdf": pdf_path,
                "volume": volume,
                "chapter": chapter,
                "pdf_page": pdf_page,
                "printed_page": printed,
                "filename": "",
                "image_type": "vector_drawings",
                "width": 0,
                "height": 0,
                "caption": "",
                "extraction_status": f"VECTOR_ONLY_{len(drawings)}_drawings",
            })

    doc.close()
    return entries


def load_or_create_manifest(manifest_path: Path) -> dict:
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"images": []}


def save_manifest(manifest_path: Path, data: dict) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Trích xuất ảnh raster từ PDF theo chương")
    parser.add_argument("chapter", type=int, help="Số chương (ví dụ: 9)")
    parser.add_argument("--volume", default="v1", help="Tập (mặc định: v1)")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ kiểm tra, không lưu file")
    args = parser.parse_args()

    root = find_root()
    pdf_path = root / "books" / "The_Cambridge_History_of_the_Vietnam_War.pdf"
    if not pdf_path.exists():
        # Thử đường dẫn thay thế
        alt = root / "The_Cambridge_History_of_the_Vietnam_War.pdf"
        if alt.exists():
            pdf_path = alt
        else:
            print(f"ERROR: Không tìm thấy PDF nguồn tại {pdf_path}")
            return 1

    manifest_path = root / "translation-project" / "00_plan" / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        chapter_manifest = json.load(f)

    images_dir = root / "translation-project" / "04_translation" / args.volume.lower() / "images"
    image_manifest_path = root / "translation-project" / "00_plan" / "image_manifest.json"

    vol_up = args.volume.upper()
    entries = extract_images_for_chapter(
        str(pdf_path), vol_up, args.chapter, chapter_manifest, images_dir, dry_run=args.dry_run
    )

    # Cập nhật image manifest (thay thế entry cũ của cùng chapter)
    image_manifest = load_or_create_manifest(image_manifest_path)
    existing = image_manifest.get("images", [])
    # Xóa entry cũ của chapter này
    existing = [e for e in existing if not (e["volume"] == vol_up and e["chapter"] == args.chapter)]
    existing.extend(entries)
    image_manifest["images"] = existing

    if not args.dry_run:
        save_manifest(image_manifest_path, image_manifest)

    print(f"=== Image extraction: {args.volume.upper()}-Ch{args.chapter:02d} ===")
    ch_entry = find_chapter_range(chapter_manifest, args.volume.upper(), args.chapter)
    print(f"PDF range: pages {ch_entry['pdf_start']}-{ch_entry['pdf_end']}")
    print(f"Images extracted: {sum(1 for e in entries if e['image_type'] == 'raster' and e['extraction_status'] == 'OK')}")
    print(f"Vector pages: {sum(1 for e in entries if e['image_type'] == 'vector_drawings')}")
    print(f"Failures: {sum(1 for e in entries if e['extraction_status'].startswith('FAIL'))}")
    for e in entries:
        print(f"  {e['image_id']}: {e['image_type']} p{e['pdf_page']} (printed {e['printed_page']}) -> {e['filename']} [{e['extraction_status']}]")

    if not args.dry_run:
        print(f"\nImage manifest saved: {image_manifest_path}")
        print(f"Images dir: {images_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
