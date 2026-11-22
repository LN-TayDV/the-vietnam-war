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

# A page with at least this many vector drawings AND a Figure/Map caption is
# treated as a vector figure (map/diagram) and rasterized as a single image,
# instead of being recorded as VECTOR_ONLY (the Ch9 defect that left maps
# un-embedded).  Raster photos (e.g. Figure 10.1) sit on pages with 0 drawings
# and continue to use the normal per-image raster path.
VECTOR_FIGURE_MIN_DRAWINGS = 20

# Captions that introduce a rasterizable figure/map/diagram.
_CAP_RE = re.compile(r"^\s*(Figure|Map|Table|Diagram|Chart)\s+\d+\.\d+", re.I)
# Vietnamese equivalents (for already-localised text, if ever run on _vi files).
_CAP_VI_RE = re.compile(r"^\s*(Hình|Bản đồ|Biểu đồ|Sơ đồ|Bảng)\s+\d+\.\d+", re.I)


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project").is_dir():
            return parent
    return Path.cwd()


def find_caption(page) -> tuple[str, str] | tuple[None, None]:
    """Return (kind, caption_text) for the first Figure/Map/Table caption on the
    page, or (None, None) if the page has no such caption.

    kind is one of: 'figure', 'map', 'table', 'diagram', 'chart' (English) or
    the Vietnamese label lowercased.  Used to decide whether a vector-heavy page
    is a real map/diagram that must be rasterized and embedded.
    """
    for line in page.get_text("text").split("\n"):
        s = line.strip()
        m = _CAP_RE.match(s)
        if m:
            return m.group(1).lower(), s
        m = _CAP_VI_RE.match(s)
        if m:
            return m.group(1).lower(), s
    return None, None


def figure_bbox(page) -> tuple[float, float, float, float] | None:
    """Bounding box (x0, y0, x1, y1) covering all vector drawings + caption text
    on the page, excluding the running header/footer.  Returns None if the page
    has no drawings."""
    drs = page.get_drawings()
    if not drs:
        return None
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for dr in drs:
        r = dr["rect"]
        x0 = min(x0, r.x0)
        y0 = min(y0, r.y0)
        x1 = max(x1, r.x1)
        y1 = max(y1, r.y1)
    return x0, y0, x1, y1


def render_vector_figure(
    doc, page, pdf_page: int, images_dir: Path, chapter: int, img_index: int
) -> dict:
    """Rasterize a vector map/diagram page (drawings + labels + caption) into a
    single PNG at 300 DPI, cropped to the figure area (header/footer excluded).

    Returns a manifest entry dict.  Fixes the Ch9 defect where vector maps were
    recorded as VECTOR_ONLY and never embedded.
    """
    bbox = figure_bbox(page)
    if bbox is None:
        return {}
    x0, y0, x1, y1 = bbox
    rect = page.rect
    # Locate the caption line to extend the crop to include it (the caption sits
    # just below the drawing block).  Fall back to the drawing bbox.
    cap_kind, cap_text = find_caption(page)
    cap_rect = None
    if cap_text:
        for b in page.get_text("blocks"):
            if cap_text[:30] in b[4]:
                cap_rect = pymupdf.Rect(b[:4])
                break
    cx0, cy0, cx1, cy1 = x0, y0, x1, y1
    if cap_rect is not None:
        cx0 = min(cx0, cap_rect.x0)
        cy0 = min(cy0, cap_rect.y0)
        cx1 = max(cx1, cap_rect.x1)
        cy1 = max(cy1, cap_rect.y1)
    # Clamp to page, add small padding.
    pad = 4.0
    clip = pymupdf.Rect(
        max(rect.x0, cx0 - pad),
        max(rect.y0, cy0 - pad),
        min(rect.x1, cx1 + pad),
        min(rect.y1, cy1 + pad),
    )
    zoom = 300 / 72.0  # 300 DPI
    mat = pymupdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    filename = f"ch{chapter:02d}_p{pdf_page:03d}_img{img_index}.png"
    out_path = images_dir / filename
    pix.save(str(out_path))
    return {
        "filename": filename,
        "image_type": "vector_figure_rasterized",
        "width": pix.width,
        "height": pix.height,
        "caption": cap_text or "",
        "caption_kind": cap_kind or "",
    }


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

        drawings = page.get_drawings()
        cap_kind, cap_text = find_caption(page)
        is_vector_figure = (
            len(drawings) >= VECTOR_FIGURE_MIN_DRAWINGS and cap_text is not None
        )

        if is_vector_figure:
            # --- Vector map/diagram: rasterize whole figure as ONE image ---
            # (fixes Ch9 defect: maps recorded VECTOR_ONLY were never embedded).
            try:
                if not dry_run:
                    info = render_vector_figure(
                        doc, page, pdf_page, images_dir, chapter, img_counter
                    )
                else:
                    info = {
                        "filename": f"ch{chapter:02d}_p{pdf_page:03d}_img{img_counter}.png",
                        "image_type": "vector_figure_rasterized",
                        "width": 0,
                        "height": 0,
                        "caption": cap_text,
                        "caption_kind": cap_kind,
                    }
                entries.append({
                    "image_id": f"{volume.lower()}-C{chapter:02d}-IMG{img_counter+1:03d}",
                    "source_pdf": pdf_path,
                    "volume": volume,
                    "chapter": chapter,
                    "pdf_page": pdf_page,
                    "printed_page": printed,
                    "filename": info["filename"],
                    "image_type": "vector_figure_rasterized",
                    "width": info["width"],
                    "height": info["height"],
                    "caption": info.get("caption", ""),
                    "caption_kind": info.get("caption_kind", ""),
                    "source_drawings": len(drawings),
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
                    "filename": "",
                    "image_type": "vector_figure_rasterized",
                    "width": 0,
                    "height": 0,
                    "caption": cap_text or "",
                    "source_drawings": len(drawings),
                    "extraction_status": f"FAIL: {e}",
                })
                img_counter += 1
            # Skip the per-raster path for this page: the tiny rasters here
            # (compass rose / scale bar) are part of the map and are already
            # captured in the rendered figure.
            continue

        # --- Raster images (photos / charts on non-vector pages) ---
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

        # --- Residual vector drawings (no caption → decorative rules etc.) ---
        if drawings and not is_vector_figure:
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
    n_raster = sum(1 for e in entries if e['image_type'] == 'raster' and e['extraction_status'] == 'OK')
    n_vecfig = sum(1 for e in entries if e['image_type'] == 'vector_figure_rasterized' and e['extraction_status'] == 'OK')
    n_embed = sum(1 for e in entries if e['image_type'] in ('raster', 'vector_figure_rasterized') and e['extraction_status'] == 'OK' and e['filename'])
    print(f"Raster images: {n_raster}")
    print(f"Vector figures rasterized (maps/diagrams): {n_vecfig}")
    print(f"Total embeddable images: {n_embed}")
    print(f"Vector-only (decorative, no caption): {sum(1 for e in entries if e['image_type'] == 'vector_drawings')}")
    print(f"Failures: {sum(1 for e in entries if e['extraction_status'].startswith('FAIL'))}")
    for e in entries:
        print(f"  {e['image_id']}: {e['image_type']} p{e['pdf_page']} (printed {e['printed_page']}) -> {e['filename']} [{e['extraction_status']}]")

    if not args.dry_run:
        print(f"\nImage manifest saved: {image_manifest_path}")
        print(f"Images dir: {images_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
