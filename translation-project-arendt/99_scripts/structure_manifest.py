# -*- coding: utf-8 -*-
"""
structure_manifest.py — Xây dựng Structural Manifest JSON từ structure detection output.

Đọc: 02_extracted_text/v2/{name}_structure.json (từ structure_detect.py)
     02_extracted_text/v2/{name}_src.txt (v2 source text với paragraph IDs)
Ghi: 02_extracted_text/v2/{name}_manifest.json (Structural Manifest)

Manifest chứa:
- Thông tin chương: tên, trang PDF, body_size, left_margin
- Các heading (chapter_title, heading_l1/l2/l3): id, type, level, trang, text, size
- Các footnote (cước chú chân trang): trang, số, text, size
- Các paragraph: id, trang, y_start, y_end, footnote_refs, is_indented_start
- Mapping giữa structure paragraphs và v2_src.txt paragraphs (theo trang)
- Báo cáo chênh lệch structure vs source

Quy trình:
1. Đọc structure JSON cho mỗi component
2. Đọc v2_src.txt để lấy paragraph IDs và trang
3. Map structure paragraphs → source paragraphs (theo trang và thứ tự)
4. Xác định chênh lệch (thiếu, trùng, sai thứ tự)
5. Lưu manifest JSON
"""

import json
import os
import re
import unicodedata
import sys
sys.stdout.reconfigure(encoding="utf-8")

from collections import Counter

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
V2 = os.path.join(BASE, "02_extracted_text", "v2")
MANIFEST_DIR = os.path.join(V2, "manifests")
os.makedirs(MANIFEST_DIR, exist_ok=True)

CHAPTERS = [
    ("front_matter", 1, 7), ("preface_first_edition", 8, 10), ("preface_part_one", 11, 16),
    ("preface_part_two", 17, 22), ("preface_part_three", 23, 41), ("part_one_intro", 42, 47),
    ("ch01", 48, 55), ("ch02", 56, 98), ("ch03", 99, 133), ("ch04", 134, 167),
    ("ch05", 168, 202), ("ch06", 203, 229), ("ch07", 230, 266), ("ch08", 267, 311),
    ("ch09", 312, 349), ("ch10", 350, 387), ("ch11", 388, 433), ("ch12", 434, 504),
    ("ch13", 505, 574),
]


def norm(s):
    return unicodedata.normalize("NFC", s)


def id_prefix(name):
    if name.startswith("ch"):
        return f"V1C{name[2:].zfill(2)}"
    return name.upper().replace("_", "")[:6]


def parse_v2_src(name):
    """Đọc v2_src.txt, trả về dict: paragraph_id → {page, text, order}."""
    src_path = os.path.join(V2, f"{name}_src.txt")
    if not os.path.exists(src_path):
        return {}, []

    text = open(src_path, encoding="utf-8").read()
    # Tách theo marker [V1CNN-Pxxx] (trang N) - chapter IDs có 2 chữ số (V1C01-P001)
    parts = re.split(r"(?m)^\[(V1C\d{2}-P\d{3})\] \(trang (\d+)\)\s*$", text)
    paras = {}
    order = []
    i = 1
    while i < len(parts):
        pid = parts[i]
        page = int(parts[i + 1])
        body = parts[i + 2].strip() if i + 2 < len(parts) else ""
        paras[pid] = {
            "page": page,
            "text": body,
            "order": len(order),
        }
        order.append(pid)
        i += 3
    return paras, order


def build_manifest(name, start_page, end_page):
    """Xây dựng Structural Manifest cho một component."""
    struct_path = os.path.join(V2, f"{name}_structure.json")
    if not os.path.exists(struct_path):
        print(f"  SKIP: {struct_path} không tồn tại")
        return None

    with open(struct_path, encoding="utf-8") as f:
        struct = json.load(f)

    # Đọc v2_src.txt
    src_paras, src_order = parse_v2_src(name)

    # Xây dựng manifest
    manifest = {
        "chapter": name,
        "pdf_pages": f"{start_page}-{end_page}",
        "body_size": struct.get("body_size"),
        "page_body_sizes": struct.get("page_body_sizes", {}),
        "left_margin": struct.get("left_margin"),
        "headings": [],
        "footnotes": [],
        "paragraphs": [],
        "source_mapping": {
            "v2_src_file": f"{name}_src.txt",
            "src_paragraph_count": len(src_paras),
            "src_order": src_order,
            "structure_paragraph_count": struct["total_paragraphs"],
            "alignment_notes": [],
        },
        "structure_summary": {
            "total_paragraphs": struct["total_paragraphs"],
            "total_headings": struct["total_headings"],
            "total_footnotes": struct["total_footnotes"],
            "footnote_pages": sorted(set(fn["page"] for fn in struct["footnotes"])),
        },
    }

    # Headings
    for h in struct["headings"]:
        manifest["headings"].append({
            "id": h["id"],
            "type": h["type"],
            "level": h["level"],
            "page": h["page"],
            "text": norm(h["text"]),
            "size": h["size"],
        })

    # Footnotes (gán số footnote từ text)
    SUP_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    fn_counter = 0
    for fn in struct["footnotes"]:
        text = norm(fn["text"])
        # Trích xuất số footnote từ đầu text
        fn_num = None
        t = text.lstrip()
        if t and t[0] in SUP_DIGITS:
            num_str = ""
            for c in t:
                if c in SUP_DIGITS:
                    num_str += str(SUP_DIGITS.index(c))
                else:
                    break
            if num_str:
                fn_num = int(num_str)
        elif re.match(r"^(\d{1,3})\s", t):
            fn_num = int(re.match(r"^(\d{1,3})", t).group(1))
        else:
            fn_counter += 1
            fn_num = fn_counter  # Gán số tạm nếu không nhận diện được

        manifest["footnotes"].append({
            "page": fn["page"],
            "number": fn_num,
            "text": text,
            "size": fn["size"],
            "y": fn["y"],
        })

    # Sắp xếp footnote theo số
    manifest["footnotes"].sort(key=lambda x: x["number"])

    # Paragraphs
    for p in struct["paragraphs"]:
        manifest["paragraphs"].append({
            "id": p["para_id"],
            "page": p["page"],
            "y_start": round(p["y_start"], 1),
            "y_end": round(p["y_end"], 1),
            "x0": round(p["x0"], 1),
            "size": p["size"],
            "footnote_refs": p.get("footnote_refs", []),
            "is_indented_start": p.get("is_indented_start", False),
        })

    # Map structure paragraphs → source paragraphs (theo trang)
    # Nhóm source paragraphs theo trang
    src_by_page = Counter()
    for pid, info in src_paras.items():
        src_by_page[info["page"]] += 1

    # Nhóm structure paragraphs theo trang
    struct_by_page = Counter()
    for p in manifest["paragraphs"]:
        struct_by_page[p["page"]] += 1

    # Xác định chênh lệch
    all_pages = sorted(set(list(src_by_page.keys()) + list(struct_by_page.keys())))
    for pg in all_pages:
        src_count = src_by_page.get(pg, 0)
        struct_count = struct_by_page.get(pg, 0)
        if src_count != struct_count:
            manifest["source_mapping"]["alignment_notes"].append(
                f"Trang {pg}: source={src_count} paragraphs, structure={struct_count} paragraphs"
            )

    # Kiểm tra heading có trong source không
    for h in manifest["headings"]:
        h_text = h["text"].lower()
        found = any(h_text in norm(p["text"]).lower() for p in src_paras.values())
        if not found:
            manifest["source_mapping"]["alignment_notes"].append(
                f"Heading '{h['text']}' (p{h['page']}) không tìm thấy trong v2_src.txt"
            )

    # Kiểm tra footnote có trong source không
    for fn in manifest["footnotes"]:
        fn_str = str(fn["number"])
        found = any(fn_str in p["text"] for p in src_paras.values())
        if not found:
            manifest["source_mapping"]["alignment_notes"].append(
                f"Footnote {fn['number']} (p{fn['page']}) không tìm thấy trong v2_src.txt"
            )

    return manifest


def main():
    for name, start, end in CHAPTERS:
        print(f"\n=== {name} (pages {start}-{end}) ===")
        manifest = build_manifest(name, start, end)
        if manifest is None:
            continue

        out_path = os.path.join(MANIFEST_DIR, f"{name}_manifest.json")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        sm = manifest["structure_summary"]
        src_map = manifest["source_mapping"]
        print(f"  Body size: {manifest['body_size']}, Left margin: {manifest['left_margin']}")
        print(f"  Paragraphs: {sm['total_paragraphs']} (structure) vs {src_map['src_paragraph_count']} (source)")
        print(f"  Headings: {sm['total_headings']}, Footnotes: {sm['total_footnotes']}")
        print(f"  Footnote pages: {sm['footnote_pages']}")
        if src_map["alignment_notes"]:
            print(f"  Alignment notes ({len(src_map['alignment_notes'])}):")
            for note in src_map["alignment_notes"][:5]:
                print(f"    - {note}")
        print(f"  Saved: {out_path}")


if __name__ == "__main__":
    main()
