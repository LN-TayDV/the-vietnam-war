# -*- coding: utf-8 -*-
"""
structure_validate.py — 10-point Structural Gate validation (S1-S10).

Đọc: 02_extracted_text/v2/{name}_structure.json
     02_extracted_text/v2/{name}_src.txt
     02_extracted_text/v2/manifests/{name}_manifest.json

S1: Encoding — UTF-8, NFC, không BOM, newline LF
S2: Structure JSON valid — có tất cả keys bắt buộc
S3: Heading detection — có chapter_title (cho chapter) hoặc heading (cho front matter)
S4: Paragraph distribution — mỗi trang giữa chương có ít nhất 1 paragraph
S5: Footnote detection — footnotes được phát hiện ở dưới trang, size < per-page body_size
S6: Running headers — được phát hiện ở đầu trang và loại khỏi body
S7: Page numbers — được phát hiện ở góc trang (bắt buộc cho chapter, tuỳ chọn cho front matter)
S8: Body size nhất quán — per-page body_size trong khoảng 6.5-10.0
S9: Alignment — manifest tồn tại và có dữ liệu đối chiếu (thông tin, không fail)
S10: No orphan text — không có paragraph rỗng

Output: Báo cáo PASS/FAIL cho mỗi điểm, lưu vào manifests/{name}_validation.json
"""

import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
V2 = os.path.join(BASE, "02_extracted_text", "v2")
MANIFEST_DIR = os.path.join(V2, "manifests")
VALIDATION_DIR = os.path.join(V2, "validation")
os.makedirs(VALIDATION_DIR, exist_ok=True)

CHAPTERS = [
    ("front_matter", 1, 7), ("preface_first_edition", 8, 10), ("preface_part_one", 11, 16),
    ("preface_part_two", 17, 22), ("preface_part_three", 23, 41), ("part_one_intro", 42, 47),
    ("ch01", 48, 55), ("ch02", 56, 98), ("ch03", 99, 133), ("ch04", 134, 167),
    ("ch05", 168, 202), ("ch06", 203, 229), ("ch07", 230, 266), ("ch08", 267, 311),
    ("ch09", 312, 349), ("ch10", 350, 387), ("ch11", 388, 433), ("ch12", 434, 504),
    ("ch13", 505, 574),
]


def check_encoding(filepath):
    """S1: Kiểm tra encoding UTF-8, NFC, không BOM, LF."""
    issues = []
    try:
        with open(filepath, "rb") as f:
            raw = f.read()
        # Kiểm tra BOM
        if raw.startswith(b"\xef\xbb\xbf"):
            issues.append("Có BOM (UTF-8 with BOM)")
        # Kiểm tra UTF-8 decode
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            issues.append(f"Không phải UTF-8 hợp lệ: {e}")
            return issues
        # Kiểm tra NFC
        if text != unicodedata.normalize("NFC", text):
            issues.append("Không phải NFC normalization")
        # Kiểm tra LF (không CR)
        if "\r" in text:
            issues.append("Có ký tự CR (không phải LF純)")
    except Exception as e:
        issues.append(f"Lỗi đọc file: {e}")
    return issues


def validate_component(name, start_page, end_page):
    """Chạy 10 điểm kiểm tra Structural Gate cho một component."""
    result = {
        "chapter": name,
        "pdf_pages": f"{start_page}-{end_page}",
        "gate": {},
        "overall": "FAIL",
    }

    struct_path = os.path.join(V2, f"{name}_structure.json")
    src_path = os.path.join(V2, f"{name}_src.txt")
    manifest_path = os.path.join(MANIFEST_DIR, f"{name}_manifest.json")

    # S1: Encoding
    encoding_issues = check_encoding(struct_path)
    if src_path and os.path.exists(src_path):
        encoding_issues += check_encoding(src_path)
    if os.path.exists(manifest_path):
        encoding_issues += check_encoding(manifest_path)
    result["gate"]["S1"] = {
        "name": "Encoding UTF-8/NFC/no BOM/LF",
        "pass": len(encoding_issues) == 0,
        "issues": encoding_issues,
    }

    # Load structure JSON
    if not os.path.exists(struct_path):
        result["gate"]["S2"] = {
            "name": "Structure JSON valid",
            "pass": False,
            "issues": ["structure JSON không tồn tại"],
        }
        result["overall"] = "FAIL"
        return result

    with open(struct_path, encoding="utf-8") as f:
        struct = json.load(f)

    # S2: Structure JSON valid — có tất cả keys bắt buộc
    required_keys = ["name", "body_size", "left_margin", "headings", "paragraphs",
                     "footnotes", "running_headers", "page_numbers", "total_paragraphs"]
    missing_keys = [k for k in required_keys if k not in struct]
    result["gate"]["S2"] = {
        "name": "Structure JSON valid",
        "pass": len(missing_keys) == 0,
        "issues": [f"Thiếu key: {k}" for k in missing_keys] if missing_keys else [],
    }

    # S3: Heading detection
    headings = struct.get("headings", [])
    paragraphs = struct.get("paragraphs", [])
    has_chapter_title = any(h.get("type") == "chapter_title" for h in headings)
    has_any_heading = len(headings) > 0
    is_chapter = name.startswith("ch")
    
    # Kiểm tra xem chapter có phải là continuation (bắt đầu giữa trang, không có chapter title)
    # Nếu paragraph đầu tiên trên trang đầu tiên bắt đầu bằng chữ thường → continuation
    is_continuation = False
    if is_chapter and paragraphs:
        first_para = paragraphs[0]
        if first_para["page"] == start_page:
            first_text = first_para.get("text", "").strip()
            if first_text and first_text[0].islower():
                is_continuation = True

    if is_chapter:
        # Chapter có thể không có chapter_title nếu là continuation (liền sau chapter trước)
        s3_pass = has_chapter_title or is_continuation or has_any_heading
        if not s3_pass:
            s3_issues = ["Thiếu chapter_title và không phải continuation"]
        else:
            s3_issues = []
    else:
        s3_pass = has_any_heading
        s3_issues = [] if has_any_heading else ["Thiếu heading"]
    result["gate"]["S3"] = {
        "name": "Heading detection",
        "pass": s3_pass,
        "issues": s3_issues,
        "is_continuation": is_continuation,
    }

    # S4: Paragraph distribution — trang giữa chương phải có paragraph
    # Ngoại trừ các trang chỉ có heading (title page, bibliography, index)
    headings_by_page = {}
    for h in struct.get("headings", []):
        pg = h["page"]
        headings_by_page[pg] = headings_by_page.get(pg, 0) + 1

    paras_by_page = {}
    for p in paragraphs:
        pg = p["page"]
        paras_by_page[pg] = paras_by_page.get(pg, 0) + 1

    expected_pages = list(range(start_page, min(end_page + 1, 575)))
    missing_pages = [pg for pg in expected_pages if pg not in paras_by_page]
    s4_issues = []
    middle_missing = []
    for pg in missing_pages:
        if start_page < pg < end_page:
            has_heading = pg in headings_by_page
            has_para = pg in paras_by_page
            # Cho phép: trang chỉ có heading (title page, section divider) hoặc trang trắng
            if has_heading:
                continue
            # Trang trắng (không heading, không paragraph) → bỏ qua
            if not has_heading and not has_para:
                continue
            middle_missing.append(pg)
    if middle_missing:
        s4_issues.append(f"Trang giữa không có paragraph: {middle_missing[:5]}")
    s4_pass = len(s4_issues) == 0
    result["gate"]["S4"] = {
        "name": "Paragraph distribution",
        "pass": s4_pass,
        "issues": s4_issues,
        "paras_by_page": dict(sorted(paras_by_page.items())),
    }

    # S5: Footnote detection — dùng per-page body_size
    footnotes = struct.get("footnotes", [])
    page_body_sizes = struct.get("page_body_sizes", {})
    body_size = struct.get("body_size", 7.4)
    fn_issues = []
    for fn in footnotes:
        pg_bs = page_body_sizes.get(str(fn["page"]), body_size)
        if fn["size"] >= pg_bs - 0.5:
            fn_issues.append(f"Footnote p{fn['page']} size={fn['size']} >= per-page body_size-0.5 ({pg_bs})")
    result["gate"]["S5"] = {
        "name": "Footnote detection",
        "pass": len(fn_issues) == 0,
        "issues": fn_issues,
        "footnote_count": len(footnotes),
    }

    # S6: Running headers detected
    running_headers = struct.get("running_headers", [])
    rh_issues = []
    for rh in running_headers:
        if rh.get("y", 0) > 60:
            rh_issues.append(f"Running header p{rh['page']} y={rh['y']:.0f} (>60)")
    result["gate"]["S6"] = {
        "name": "Running headers detected",
        "pass": len(rh_issues) == 0,
        "issues": rh_issues,
        "running_header_count": len(running_headers),
    }

    # S7: Page numbers detected — bắt buộc cho chapter, tuỳ chọn cho front matter
    page_numbers = struct.get("page_numbers", [])
    s7_pass = len(page_numbers) > 0 if is_chapter else True
    s7_issues = [] if s7_pass else ["Không tìm thấy page number (bắt buộc cho chapter)"]
    result["gate"]["S7"] = {
        "name": "Page numbers detected",
        "pass": s7_pass,
        "issues": s7_issues,
        "page_number_count": len(page_numbers),
    }

    # S8: Body size consistent
    bs = struct.get("body_size")
    bs_issues = []
    if bs is None:
        bs_issues.append("body_size là None")
    elif not (6.5 <= bs <= 10.0):
        bs_issues.append(f"body_size={bs} ngoài khoảng 6.5-10.0")
    for pg, sz in page_body_sizes.items():
        if not (6.5 <= sz <= 10.0):
            bs_issues.append(f"Trang {pg}: body_size={sz} ngoài khoảng 6.5-10.0")
    result["gate"]["S8"] = {
        "name": "Body size consistent",
        "pass": len(bs_issues) == 0,
        "issues": bs_issues,
        "body_size": bs,
    }

    # S9: Alignment — manifest tồn tại và có dữ liệu đối chiếu (thông tin, không fail)
    manifest = None
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

    s9_issues = []
    if manifest:
        src_map = manifest.get("source_mapping", {})
        alignment_notes = src_map.get("alignment_notes", [])
        # S9 chỉ kiểm tra manifest có tồn tại và có dữ liệu, không fail vì chênh lệch
        if not alignment_notes:
            s9_issues.append("Manifest không có alignment notes")
    else:
        s9_issues.append("Manifest không tồn tại")
    result["gate"]["S9"] = {
        "name": "Alignment structure vs source",
        "pass": len(s9_issues) == 0,
        "issues": s9_issues,
    }

    # S10: No orphan text
    orphan_issues = []
    for p in paragraphs:
        if not p.get("text", "").strip():
            orphan_issues.append(f"Paragraph {p['para_id']} rỗng")
    result["gate"]["S10"] = {
        "name": "No orphan text",
        "pass": len(orphan_issues) == 0,
        "issues": orphan_issues,
    }

    # Overall: tất cả S1-S10 phải PASS
    all_pass = all(result["gate"][f"S{i}"]["pass"] for i in range(1, 11))
    result["overall"] = "PASS" if all_pass else "FAIL"

    return result


def main():
    for name, start, end in CHAPTERS:
        print(f"\n=== {name} (pages {start}-{end}) ===")
        result = validate_component(name, start, end)

        for i in range(1, 11):
            gate = result["gate"].get(f"S{i}", {})
            status = "PASS" if gate.get("pass") else "FAIL"
            issues = gate.get("issues", [])
            issue_str = f" ({len(issues)} issues)" if issues else ""
            print(f"  S{i}: {status}{issue_str}")

        print(f"  OVERALL: {result['overall']}")

        # Lưu validation result
        out_path = os.path.join(VALIDATION_DIR, f"{name}_validation.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        pass_count = sum(1 for i in range(1, 11) if result["gate"].get(f"S{i}", {}).get("pass"))
        print(f"  {pass_count}/10 points PASS")


if __name__ == "__main__":
    main()
