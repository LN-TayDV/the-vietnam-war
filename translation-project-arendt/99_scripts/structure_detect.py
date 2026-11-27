#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
structure_detect.py — Phát hiện cấu trúc chương từ PDF gốc (line-based, indentation-aware).

Quy trình:
1. Trích xuất tất cả text lines với spans chi tiết (size, text, vị trí).
2. Với mỗi line, tính dominant_size = size có nhiều ký tự nhất.
3. Xác định body_size = mode dominant_size ở vùng giữa trang.
4. Xác định left_margin = x0 phổ biến nhất của các line body.
5. Phân loại từng line: running_header / page_number / chapter_title /
   heading / footnote / body.
6. Gộp các line body thành paragraph:
   - Ngắt paragraph khi khoảng cách dọc lớn
   - Hoặc khi dòng có indentation (x0 > left_margin + ngưỡng) và dòng trước kết thúc bằng dấu câu
7. Gộp paragraph bị chia bởi dấu gạch ngang.
8. Đánh dấu running header để loại khỏi body.

Output: 02_extracted_text/v2/{name}_structure.json
"""

import fitz
import os
import re
import json
import unicodedata
import statistics
from collections import Counter
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf"
V2 = os.path.join(BASE, "02_extracted_text", "v2")
os.makedirs(V2, exist_ok=True)

SUP_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"

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


def dominant_size(spans):
    """Trả về size có nhiều ký tự nhất trong danh sách spans."""
    char_counts = Counter()
    for s in spans:
        t = s["text"]
        if t.strip():
            char_counts[round(s["size"], 1)] += len(t.strip())
    if not char_counts:
        return 0
    return char_counts.most_common(1)[0][0]


def is_footnote_marker(text):
    """Kiểm tra text bắt đầu bằng số mũ footnote hoặc [n]."""
    t = text.lstrip()
    if not t:
        return False
    if t[0] in SUP_DIGITS:
        return True
    if re.match(r"^\[\d+\]", t):
        return True
    return False


def extract_footnote_markers(text):
    """Trích xuất các số mũ footnote (¹, ², ...) từ trong text.
    Trả về list các số footnote (int) được tìm thấy."""
    markers = []
    i = 0
    while i < len(text):
        if text[i] in SUP_DIGITS:
            # Ghép các chữ số mũ liền nhau
            num_str = ""
            while i < len(text) and text[i] in SUP_DIGITS:
                num_str += str(SUP_DIGITS.index(text[i]))
                i += 1
            if num_str:
                markers.append(int(num_str))
        else:
            i += 1
    return markers


def ends_with_hyphen(text):
    return text.rstrip().endswith("-") or text.rstrip().endswith("\u00ad")


def starts_with_lowercase(text):
    t = text.lstrip()
    return bool(t) and t[0].islower()


def ends_sentence(text):
    t = text.rstrip()
    if not t:
        return False
    return t[-1] in ".!?…\"'”’"


def id_prefix(name):
    if name.startswith("ch"):
        return f"V1C{name[2:].zfill(2)}"
    # Front matter components all use V1C00 in _src.txt
    return "V1C00"


def detect_structure(name, start_page, end_page, doc):
    result = {
        "name": name,
        "pdf_pages": f"{start_page}-{end_page}",
        "body_size": None,
        "left_margin": None,
        "headings": [],
        "paragraphs": [],
        "running_headers": [],
        "page_numbers": [],
        "footnotes": [],
        "issues": [],
    }

    # === Pass 1: Trích xuất tất cả lines với spans chi tiết ===
    all_lines = []
    page_info = {}

    for pnum in range(start_page - 1, min(end_page, doc.page_count)):
        page = doc[pnum]
        pnum_1 = pnum + 1
        page_info[pnum_1] = (page.rect.height, page.rect.width)
        d = page.get_text("dict")

        for block in d["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                if not spans:
                    continue
                line_text = "".join(s["text"] for s in spans).strip()
                if not line_text:
                    continue
                dom_sz = dominant_size(spans)
                min_y = min(s["bbox"][1] for s in spans)
                min_x = min(s["bbox"][0] for s in spans)
                max_x = max(s["bbox"][2] for s in spans)

                all_lines.append({
                    "text": line_text,
                    "size": dom_sz,
                    "max_size": max(round(s["size"], 1) for s in spans),
                    "x0": min_x,
                    "y0": min_y,
                    "x1": max_x,
                    "page": pnum_1,
                    "spans": spans,
                })

    if not all_lines:
        result["issues"].append("No text found on pages")
        return result

    # === Pass 2: Xác định body_size và left_margin (per-page) ===
    # Dùng dominant_size của các line ở vùng giữa trang (25-80% chiều cao)
    page_body_sizes = {}
    margin_candidates = Counter()

    for line in all_lines:
        ph, pw = page_info[line["page"]]
        rel_y = line["y0"] / ph
        # Thu thập x0 để xác định left margin (dùng các line ở vùng giữa)
        if 0.25 <= rel_y <= 0.80:
            margin_candidates[round(line["x0"], 0)] += 1

    # Tính body_size cho mỗi trang riêng biệt
    for pnum in range(start_page, min(end_page + 1, doc.page_count + 1)):
        ph, pw = page_info[pnum]
        page_middle = Counter()
        for line in all_lines:
            if line["page"] != pnum:
                continue
            rel_y = line["y0"] / ph
            if 0.25 <= rel_y <= 0.80:
                sz = line["size"]
                if 6.5 <= sz <= 10.0:  # Loại footnote quá nhỏ và heading quá lớn
                    page_middle[sz] += len(line["text"])
        if page_middle:
            most_common_sz, most_common_cnt = page_middle.most_common(1)[0]
            total_chars = sum(page_middle.values())
            if most_common_cnt / total_chars > 0.35:
                page_body_sizes[pnum] = round(most_common_sz, 1)
            else:
                page_body_sizes[pnum] = round(statistics.median(list(page_middle.elements())), 1)

    if page_body_sizes:
        # Body size chapter-level = median of per-page sizes (robust to mixed pages)
        all_page_sizes = list(page_body_sizes.values())
        result["body_size"] = round(statistics.median(all_page_sizes), 1)
        result["page_body_sizes"] = page_body_sizes
    else:
        all_dom = [l["size"] for l in all_lines if 6.0 <= l["size"] <= 11.0]
        result["body_size"] = round(statistics.median(all_dom), 1) if all_dom else 7.4
        result["page_body_sizes"] = {}

    body_size = result["body_size"]

    # Left margin = x0 phổ biến nhất (làm tròn về số nguyên)
    if margin_candidates:
        result["left_margin"] = margin_candidates.most_common(1)[0][0]
    else:
        result["left_margin"] = 10.0

    left_margin = result["left_margin"]

    # === Pass 3: Phân loại từng line ===
    classified = []

    for line in all_lines:
        ph, pw = page_info[line["page"]]
        rel_y = line["y0"] / ph
        text = line["text"]
        size = line["size"]
        max_sz = line["max_size"]
        y0 = line["y0"]
        x0 = line["x0"]

        # 1. Page number: số đơn lẻ ở góc trên
        if re.match(r'^\d+$', text) and 6.0 <= size <= 10.0 and rel_y < 0.10:
            if x0 < 60 or x0 > pw - 90:
                result["page_numbers"].append({
                    "page": line["page"], "text": text, "size": size, "y": y0, "x": x0,
                })
                continue

        # 2. Running header: chữ in hoa, cỡ nhỏ, ở đầu trang (rel_y < 0.10)
        if rel_y < 0.10:
            upper_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
            if upper_ratio > 0.7 and len(text) >= 3 and size <= 8.5:
                result["running_headers"].append({
                    "page": line["page"], "text": text, "size": size, "y": y0, "x": x0,
                })
                continue

        # 3. Chapter title: chứa "CHAPTER" ở ĐẦU dòng (loại bỏ khoảng cách giữa các chữ)
        compact = re.sub(r'\s+', '', text)
        if re.match(r'CHAPTER', compact, re.I) and rel_y < 0.30 and len(compact) < 60:
            heading_counter = len(result["headings"]) + 1
            result["headings"].append({
                "id": f"{id_prefix(name)}-H{heading_counter:03d}",
                "type": "chapter_title",
                "text": text,
                "page": line["page"], "y": y0, "x": x0,
                "size": size, "level": 1,
            })
            continue

        # 4. Drop cap: dòng có max_size rất lớn nhưng dominant_size bình thường
        # → đây là dòng body có chữ cái đầu to lẹ, không phải heading
        # (không làm gì cả, sẽ được xử lý làm body ở bước 7)

        # 5. Heading: dominant_size đáng kể lớn hơn body (>= body_size + 4)
        if size >= body_size + 4.0:
            heading_counter = len(result["headings"]) + 1
            if size >= body_size + 9.0:
                level = 1
            elif size >= body_size + 6.0:
                level = 2
            else:
                level = 3
            result["headings"].append({
                "id": f"{id_prefix(name)}-H{heading_counter:03d}",
                "type": f"heading_l{level}",
                "text": text,
                "page": line["page"], "y": y0, "x": x0,
                "size": size, "level": level,
            })
            continue

        # 6. Footnote text ở dưới trang (rel_y > 0.88) với font nhỏ hơn body (dùng per-page body_size)
        page_bs = page_body_sizes.get(line["page"], body_size)
        if rel_y > 0.88 and size < page_bs - 0.5:
            result["footnotes"].append({
                "page": line["page"], "text": text, "size": size, "y": y0,
            })
            continue

        # 7. Mặc định: body paragraph line
        # Kiểm tra các span có chữ số nhỏ (footnote reference trong dòng body)
        inline_refs = []
        for s in spans:
            st = s["text"].strip()
            sz = round(s["size"], 1)
            if re.match(r'^\d{1,3}$', st) and sz < size - 0.5:
                inline_refs.append(int(st))
        classified.append({
            "type": "body",
            "text": text,
            "size": size,
            "x0": x0,
            "y0": y0,
            "page": line["page"],
            "inline_fn_refs": inline_refs,
        })

    # === Pass 4: Gộp các line body thành paragraph ===
    # Dùng cả khoảng cách dọc VÀ indentation để phát hiện ranh giới paragraph
    body_lines = [c for c in classified if c["type"] == "body"]
    body_lines.sort(key=lambda c: (c["page"], c["y0"]))

    paragraphs = []
    para_counter = 0
    current_para = None

    # Ngưỡng indentation: dòng được coi là "indented" nếu x0 > left_margin + 3
    indent_threshold = 3.0
    line_height = body_size * 1.2
    para_gap_threshold = line_height * 1.5

    for line in body_lines:
        if current_para is None:
            para_counter += 1
            current_para = {
                "para_id": f"{id_prefix(name)}-P{para_counter:03d}",
                "text": line["text"],
                "page": line["page"],
                "y_start": line["y0"],
                "y_end": line["y0"],
                "x0": line["x0"],
                "size": line["size"],
                "lines": [line["text"]],
                "footnote_refs": extract_footnote_markers(line["text"]) + line.get("inline_fn_refs", []),
                "is_indented_start": line["x0"] > left_margin + indent_threshold,
            }
        else:
            same_page = line["page"] == current_para["page"]
            vertical_gap = line["y0"] - current_para["y_end"]
            is_indented = line["x0"] > left_margin + indent_threshold
            prev_ends_sentence = ends_sentence(current_para["lines"][-1])

            is_new_para = False

            if not same_page:
                is_new_para = True
            elif vertical_gap > para_gap_threshold:
                is_new_para = True
            elif is_indented and prev_ends_sentence and vertical_gap > line_height * 0.8:
                # Dòng mới có indentation và dòng trước kết thúc bằng dấu câu
                # → đây là paragraph mới (dù khoảng cách dọc không lớn)
                is_new_para = True

            if is_new_para:
                paragraphs.append(current_para)
                para_counter += 1
                current_para = {
                    "para_id": f"{id_prefix(name)}-P{para_counter:03d}",
                    "text": line["text"],
                    "page": line["page"],
                    "y_start": line["y0"],
                    "y_end": line["y0"],
                    "x0": line["x0"],
                    "size": line["size"],
                    "lines": [line["text"]],
                    "footnote_refs": extract_footnote_markers(line["text"]) + line.get("inline_fn_refs", []),
                    "is_indented_start": is_indented,
                }
            else:
                current_para["text"] += " " + line["text"]
                current_para["y_end"] = line["y0"]
                current_para["lines"].append(line["text"])
                current_para["footnote_refs"].extend(
                    extract_footnote_markers(line["text"]) + line.get("inline_fn_refs", [])
                )

    if current_para is not None:
        paragraphs.append(current_para)

    # === Pass 5: Gộp paragraph bị chia bởi dấu gạch ngang ===
    merged = []
    i = 0
    while i < len(paragraphs):
        cur = dict(paragraphs[i])
        j = i + 1
        while j < len(paragraphs):
            nxt = paragraphs[j]
            if ends_with_hyphen(cur["text"]) and starts_with_lowercase(nxt["text"]):
                if nxt["page"] == cur["page"] or nxt["page"] == cur["page"] + 1:
                    cur["text"] = cur["text"].rstrip("-").rstrip() + " " + nxt["text"].lstrip()
                    cur.setdefault("merged_from", []).append(nxt["para_id"])
                    cur["page"] = nxt["page"]
                    cur["footnote_refs"].extend(nxt.get("footnote_refs", []))
                    cur["y_end"] = nxt["y_end"]
                    j += 1
                    continue
            break
        merged.append(cur)
        i = j if j > i + 1 else i + 1

    result["paragraphs"] = merged
    result["total_paragraphs"] = len(merged)
    result["total_headings"] = len(result["headings"])
    result["total_footnotes"] = len(result["footnotes"])
    result["total_running_headers"] = len(result["running_headers"])

    return result


if __name__ == "__main__":
    doc = fitz.open(PDF_PATH)
    print(f"PDF: {doc.page_count} pages")

    for name, start, end in CHAPTERS:
        print(f"\n=== {name} (pages {start}-{end}) ===")
        r = detect_structure(name, start, end, doc)
        print(f"  Body size: {r.get('body_size')}, Left margin: {r.get('left_margin')}")
        print(f"  Headings: {r['total_headings']}, Paragraphs: {r['total_paragraphs']}")
        print(f"  Footnotes: {r['total_footnotes']}, Running headers: {r['total_running_headers']}")
        print(f"  Page numbers: {len(r['page_numbers'])}")
        if r["issues"]:
            print(f"  Issues: {r['issues']}")

        # In headings
        for h in r["headings"][:8]:
            print(f"    [{h['id']}] {h['type']} L{h['level']} (p{h['page']}, sz={h['size']}): {h['text'][:70]}")

        # In paragraphs đầu
        for p in r["paragraphs"][:3]:
            print(f"    [{p['para_id']}] (p{p['page']}): {p['text'][:70]}")

        # Lưu file — normalize NFC và dùng LF newline
        def normalize_obj(obj):
            if isinstance(obj, str):
                return unicodedata.normalize("NFC", obj)
            if isinstance(obj, dict):
                return {k: normalize_obj(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [normalize_obj(v) for v in obj]
            return obj

        r_norm = normalize_obj(r)
        out_path = os.path.join(V2, f"{name}_structure.json")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(r_norm, f, ensure_ascii=False, indent=2)
        print(f"  Saved: {out_path}")

    doc.close()
    print("\nDone!")
