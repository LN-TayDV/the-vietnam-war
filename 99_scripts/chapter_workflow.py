#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chapter_workflow.py — Workflow thống nhất cho MỌI CHƯƠNG MỚI
Thay thế việc tạo script riêng cho từng chương (fix_ch11_*, check_ch11_*, etc.)

Usage:
    python 99_scripts/chapter_workflow.py 11 --volume v1 --step all

Steps:
    extract       - Trích xuất hình ảnh từ PDF (bắt buộc trước khi dịch)
    check_markers - Kiểm tra toàn vẹn footnote inline markers (BẮT BUỘC trước build)
    build         - Build DOCX từ bản dịch
    audit         - Kiểm tra định dạng DOCX
    compare       - Đối chiếu src vs vi (alignment)
    quality       - Chạy Quality Gate
    all           - Chạy toàn bộ pipeline (extract → check_markers → build → audit → compare → quality)

Các script chuyên dụng (chỉ dùng khi cần thiết):
    - build_chapter_docx.py: Build DOCX
    - extract_images.py: Trích xuất ảnh
    - audit_docx_format.py: Kiểm tra format
    - document_comparator.py (common): Đối chiếu
    - quality_gate.py (common): Quality Gate
    - vnch_orthography.py (common): Kiểm tra chính tả VNCH
    - encoding_checker.py (common): Kiểm tra encoding
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "translation-project").is_dir():
            return parent
    return Path.cwd()


def run_cmd(cmd: list[str], cwd: Path, description: str) -> int:
    """Chạy lệnh và trả về exit code."""
    print(f"\n{'='*60}")
    print(f"[TOOL] {description}")
    print(f"DIR: {cwd}")
    print(f"CMD: {' '.join(cmd)}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode == 0:
        print(f"[OK] {description} - PASS")
    else:
        print(f"[FAIL] {description} - FAIL (exit code: {result.returncode})")
    return result.returncode


def step_extract(root: Path, chapter: int, volume: str) -> int:
    """Bước 1: Trích xuất hình ảnh từ PDF."""
    return run_cmd([
        sys.executable, "99_scripts/extract_images.py",
        str(chapter), "--volume", volume
    ], root, f"Extract images for {volume.upper()}-Ch{chapter:02d}")


def step_check_markers(root: Path, chapter: int) -> int:
    """Bước 1.5: Kiểm tra toàn vẹn footnote inline markers trước khi build DOCX.
    
    BẮT BUỘC chạy trước `build`. Nếu thiếu marker, duplicate, hoặc orphan
    → exit 1, chặn build DOCX.
    """
    return run_cmd([
        sys.executable, "99_scripts/check_footnote_markers.py",
        str(chapter)
    ], root, f"Check footnote markers for Chapter {chapter:02d}")


def check_file_locked(filepath: Path) -> bool:
    """Kiểm tra file có bị lock bởi process khác không."""
    if not filepath.exists():
        return False
    try:
        with open(filepath, 'a'):
            pass
        return False
    except PermissionError:
        return True


def step_build(root: Path, chapter: int) -> int:
    """Bước 2: Build DOCX từ bản dịch."""
    # Kiểm tra file output có bị lock không
    out_dir = root / "translation-project" / "09_docx"
    possible_files = list(out_dir.glob(f"V1-C{chapter:02d}_*.docx"))
    if possible_files:
        for f in possible_files:
            if check_file_locked(f):
                print(f"[WARN] File {f.name} dang bi mo trong Word/preview.")
                print(f"       Hay dong Word roi chay lai.")
                return 1
    return run_cmd([
        sys.executable, "99_scripts/build_chapter_docx.py",
        str(chapter)
    ], root, f"Build DOCX for Chapter {chapter:02d}")


def step_audit(root: Path, chapter: int) -> int:
    """Bước 3: Audit định dạng DOCX."""
    return run_cmd([
        sys.executable, "99_scripts/audit_docx_format.py",
        str(chapter)
    ], root, f"Audit DOCX format for Chapter {chapter:02d}")


def step_compare(root: Path, chapter: int) -> int:
    """Bước 4: Đối chiếu src vs vi (alignment)."""
    return run_cmd([
        sys.executable, ".kilo/scripts/common/document_comparator.py",
        "--chapter", str(chapter)
    ], root, f"Compare src vs vi for Chapter {chapter:02d}")


def step_quality(root: Path, chapter: int) -> int:
    """Bước 5: Quality Gate."""
    return run_cmd([
        sys.executable, ".kilo/scripts/common/quality_gate.py",
        "--chapter", str(chapter)
    ], root, f"Quality Gate for Chapter {chapter:02d}")


def step_orthography(root: Path, chapter: int) -> int:
    """Kiểm tra chính tả VNCH (bổ sung)."""
    return run_cmd([
        sys.executable, ".kilo/scripts/common/vnch_orthography.py",
        "--chapter", str(chapter)
    ], root, f"VNCH Orthography check for Chapter {chapter:02d}")


def step_encoding(root: Path, chapter: int) -> int:
    """Kiểm tra encoding (bổ sung)."""
    return run_cmd([
        sys.executable, ".kilo/scripts/common/encoding_checker.py",
        "--chapter", str(chapter)
    ], root, f"Encoding check for Chapter {chapter:02d}")


def main():
    parser = argparse.ArgumentParser(
        description="Workflow thống nhất cho mọi chương dịch thuật",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Vi du:
  python 99_scripts/chapter_workflow.py 11 --volume v1 --step all
  python 99_scripts/chapter_workflow.py 12 --volume v1 --step extract check_markers build audit
  python 99_scripts/chapter_workflow.py 09 --volume v1 --step compare quality

Quy trinh chuan (theo SKILL.md):
  1. extract_images.py    -> Trich xuat anh tu PDF
  2. check_footnote_markers.py -> Kiem tra toan van footnote markers (BAT BUOC)
  3. Dich ban dich (tu dong/hand)
  4. build_chapter_docx.py -> Build DOCX
  5. audit_docx_format.py  -> Kiem tra format
  6. document_comparator.py -> Doi chieu src vs vi
  7. quality_gate.py       -> Quality Gate 8 tieu chi
  8. vnch_orthography.py   -> Kiem tra chinh ta VNCH
  9. encoding_checker.py   -> Kiem tra UTF-8/NFC/no BOM/LF
        """
    )
    parser.add_argument("chapter", type=int, help="Số chương (ví dụ: 11)")
    parser.add_argument("--volume", default="v1", help="Tập (mặc định: v1)")
    parser.add_argument(
        "--step", nargs="+", choices=[
            "extract", "check_markers", "build", "audit", "compare", "quality",
            "orthography", "encoding", "all"
        ], default=["all"], help="Các bước cần chạy"
    )
    args = parser.parse_args()

    root = find_root()
    chapter = args.chapter
    volume = args.volume

    steps = args.step
    if "all" in steps:
        steps = ["extract", "check_markers", "build", "audit", "compare",
                 "quality", "orthography", "encoding"]

    print(f"\n{'#'*60}")
    print(f"# WORKFLOW CHUONG {chapter:02d} - {volume.upper()}")
    print(f"# Cac buoc: {', '.join(steps)}")
    print(f"{'#'*60}")

    exit_codes = {}
    for step in steps:
        if step == "extract":
            exit_codes[step] = step_extract(root, chapter, volume)
        elif step == "check_markers":
            exit_codes[step] = step_check_markers(root, chapter)
        elif step == "build":
            exit_codes[step] = step_build(root, chapter)
        elif step == "audit":
            exit_codes[step] = step_audit(root, chapter)
        elif step == "compare":
            exit_codes[step] = step_compare(root, chapter)
        elif step == "quality":
            exit_codes[step] = step_quality(root, chapter)
        elif step == "orthography":
            exit_codes[step] = step_orthography(root, chapter)
        elif step == "encoding":
            exit_codes[step] = step_encoding(root, chapter)

    # Tổng kết
    print(f"\n{'#'*60}")
    print(f"# TONG KET CHUONG {chapter:02d}")
    print(f"{'#'*60}")
    all_pass = True
    for step, code in exit_codes.items():
        status = "PASS" if code == 0 else "FAIL"
        print(f"  {step:15s}: {status}")
        if code != 0:
            all_pass = False

    if all_pass:
        print(f"\nTAT CA CAC BUOC PASS - Chuong {chapter:02d} SAN SANG BAN GIAO")
        return 0
    else:
        print(f"\nCO BUOC FAIL - CAN KIEM TRA LAI")
        return 1


if __name__ == "__main__":
    sys.exit(main())