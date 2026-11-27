# -*- coding: utf-8 -*-
"""
Main build entry point for DOCX Builder v2.

Usage:
    python 99_scripts/build_chapter_docx_v2.py ch04 [ch05 ...]
    python 99_scripts/build_chapter_docx_v2.py --all

Reads 04_translation/v2/chNN/v1_chNN_vi.txt and writes
09_docx/V1-<NN>_<slug>.docx using Word styles, native footnotes, and the
shared style system from styles/spec.yaml.
"""
from __future__ import annotations

import io
import re
import sys
import unicodedata
from pathlib import Path

from docx_builder_v2.models import DocumentModel
from docx_builder_v2.parser import parse, strip_page_artifacts
from docx_builder_v2.styles import StyleRegistry
from docx_builder_v2.layout import PageLayout
from docx_builder_v2.renderer import Renderer

ROOT = Path(__file__).resolve().parent.parent.parent
V2 = ROOT / "04_translation" / "v2"
OUT_DIR = ROOT / "09_docx"
STYLES_PATH = ROOT / "99_scripts" / "styles" / "spec.yaml"

BOOK_TITLE = "The Origins of Totalitarianism"
AUTHOR = "Hannah Arendt"

TITLES = {
    "front_matter": ("Phần Mở Đầu", "Trang Bìa và Thông Tin Xuất Bản"),
    "preface_first_edition": ("Lời Nói Đầu Bản Dựng Lần Thứ Nhất", ""),
    "preface_part_one": ("Lời Nói Đầu Phần Một", ""),
    "preface_part_two": ("Lời Nói Đầu Phần Hai", ""),
    "preface_part_three": ("Lời Nói Đầu Phần Ba", ""),
    "part_one_intro": ("Phần Một: Chủ Nghĩa Phân Biệt Chủng Tộc", "Giới Thiệu"),
    "ch01": ("Chương Một", "Chủ Nghĩa Chống Do Thái — Một Sự Lăng Mạ Đối Với Lẽ Thường"),
    "ch02": ("Chương Hai", "Chủ Nghĩa Phân Biệt Chủng Tộc Trước Chủ Nghĩa Quốc Gia"),
    "ch03": ("Chương Ba", "Người Do Thái Và Xã Hội"),
    "ch04": ("Chương Bốn", "Vụ Dreyfus"),
    "ch05": ("Chương Năm", "Giải Phóng Chánh Trị Của Giai Cấp Thị Dân"),
    "ch06": ("Chương Sáu", "Tư Duy Chủng Tộc Trước Chủ Nghĩa Phân Biệt Chủng Tộc"),
    "ch07": ("Chương Bảy", "Chủng Tộc và Quan Liêu"),
    "ch08": ("Chương Tám", "Chủ Nghĩa Đế Quốc Lục Địa: Các Phong Trào Pan"),
    "ch09": ("Chương Chín", "Sự Suy Tàn Của Quốc Gia Quốc Dân và Hết Hạn Quyền Con Người"),
    "ch10": ("Chương Mười", "Xã Hội Không Giai Cấp"),
    "ch11": ("Chương Mười Một", "Phong Trào Toàn Trị"),
    "ch12": ("Chương Mười Hai", "Toàn Trị Tại Quyền"),
    "ch13": ("Chương Mười Ba", "Ý Thức Hệ và Khủng Bố · Một Hình Thức Chánh Phủ Mới"),
}


def slugify(text: str, limit=70) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "D")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")
    return text[:limit].rstrip("-")


def _safe_unlink(path, required=True) -> None:
    import time
    if not path.exists():
        return
    last = None
    for _ in range(10):
        try:
            path.unlink()
            return
        except PermissionError as exc:
            last = exc
            import time as _t
            _t.sleep(0.3)
    if required:
        raise PermissionError(
            f"Không thể ghi đè '{path.name}'. Hãy đóng Word rồi chạy lại.\nChi tiết: {last}")


def build(ch: str, registry: StyleRegistry, layout: PageLayout) -> tuple:
    """
    Build one chapter DOCX.  Returns (output_path, word_count, fn_used, fn_total).
    """
    src_path = V2 / ch / f"v1_{ch}_vi.txt"
    if not src_path.exists():
        raise FileNotFoundError(f"Source not found: {src_path}")

    text = src_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    chap_label, vi_title = TITLES.get(ch, (ch, ch))

    model = parse(text, chapter_label=chap_label, vi_title=vi_title)

    doc_obj, fn_placed = Renderer(registry, layout).render(model)

    # Word count of body text
    words = sum(len(n.text.split()) for n in model.nodes if n.type in ("body", "block_quote"))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"V2-{ch[-2:].upper()}_{slugify(vi_title)}.docx"
    tmp = OUT_DIR / f".tmp_v2_{ch}.docx"
    if tmp.exists():
        _safe_unlink(tmp, required=True)
    doc_obj.save(tmp)
    if out.exists():
        _safe_unlink(out, required=True)
    tmp.rename(out)

    fn_used = fn_placed
    fn_total = len(model.footnotes)
    return out, words, fn_used, fn_total


def main(argv) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    wanted = [a for a in argv if a.strip() and a != "--all"]
    if "--all" in argv:
        wanted = sorted(d.name for d in V2.iterdir() if d.is_dir() and (d / f"v1_{d.name}_vi.txt").exists())
    if not wanted:
        print("Usage: python 99_scripts/build_chapter_docx_v2.py ch04 [ch05 ...]")
        print("       python 99_scripts/build_chapter_docx_v2.py --all")
        return 1

    registry = StyleRegistry.from_yaml(STYLES_PATH)
    layout = PageLayout()

    rc = 0
    results = []
    for ch in wanted:
        try:
            out, words, used, total = build(ch, registry, layout)
            flag = "OK " if used == total else "WARN"
            if used != total:
                rc = 1
            print(f"{flag} {ch} -> {out.name} ({words:,} từ, {used}/{total} cước chú)")
            results.append((ch, out.name, words, used, total, True))
        except Exception as exc:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            print(f"FAIL {ch}: {exc}")
            rc = 1
            results.append((ch, "", 0, 0, 0, False))
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
