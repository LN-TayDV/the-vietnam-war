# -*- coding: utf-8 -*-
"""
fix_ch04_structure.py — Chỉnh sửa cấu trúc ch04 từ PDF gốc.

Các vấn đề đã biết cần sửa:
1. Cross-page footnote-body merges: footnote văn bản ở giữa trang bị gộp vào body paragraph.
2. "J 00" artifact trên p145: chưa được phát hiện làm section number / artifact.
3. Thiếu ch04_src_REBUILT.txt.

Quy trình:
1. Trích xuất tất cả lines từ PDF pages 134-167 với spans chi tiết.
2. Xác định body_size, left_margin per-page.
3. Phân loại từng line: running_header / page_number / section_number /
   section_heading / chapter_title / part_title / part_divider / footnote / body / artifact.
4. Gộp body lines thành paragraph, xử lý cross-page continuation (dấu gạch ngang).
5. Tách footnote khỏi body text.
6. Xuất ch04_structure_REBUILT.json và ch04_src_REBUILT.txt.
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

NAME = "ch04"
START_PAGE = 134
END_PAGE = 167

# Nếu có tham số dòng lệnh: python fix_ch04_structure.py <name> <start> <end>
if len(sys.argv) >= 4:
    NAME = sys.argv[1]
    START_PAGE = int(sys.argv[2])
    END_PAGE = int(sys.argv[3])
    print(f"Chạy cho {NAME} (trang {START_PAGE}-{END_PAGE})")

SUP_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def norm(s):
    return unicodedata.normalize("NFC", s)


def id_prefix(name):
    if name.startswith("ch"):
        return f"V1C{name[2:].zfill(2)}"
    return "V1C00"


def dominant_size(spans):
    char_counts = Counter()
    for s in spans:
        t = s["text"]
        if t.strip():
            char_counts[round(s["size"], 1)] += len(t.strip())
    if not char_counts:
        return 0
    return char_counts.most_common(1)[0][0]


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


def extract_footnote_markers(text):
    markers = []
    i = 0
    while i < len(text):
        if text[i] in SUP_DIGITS:
            num_str = ""
            while i < len(text) and text[i] in SUP_DIGITS:
                num_str += str(SUP_DIGITS.index(text[i]))
                i += 1
            if num_str:
                markers.append(int(num_str))
        else:
            i += 1
    return markers


def is_section_number(text, size, body_size):
    """Phân tích xem text có phải section number (I:, II:, III:, ...) hay không."""
    t = text.strip()
    # Roman numeral pattern: I:, II:, III:, IV:, V:, VI:, VII:, VIII:, IX:, X:, ...
    roman_pattern = r'^[IVX]+:\s*$'
    if re.match(roman_pattern, t, re.I):
        return True
    # Also "1 :", "11:" patterns from OCR (1-3 digits only, exclude 4-digit years)
    if re.match(r'^\d{1,3}\s*:', t):
        return True
    return False


def is_artifact(text, size, y0, page_height, body_size):
    """Phân tích xem text có phải artifact ở đầu trang không (ví dụ "J 00")."""
    t = text.strip()
    rel_y = y0 / page_height
    # Artifact: ở đầu trang (rel_y < 0.05), không phải running header, không phải page number
    if rel_y < 0.05:
        # Loại page number (số đơn lẻ)
        if re.match(r'^\d+$', t):
            return False
        # Loại running header (chữ in hoa, cỡ nhỏ)
        upper_ratio = sum(1 for c in t if c.isupper()) / max(len(t), 1)
        if upper_ratio > 0.7 and len(t) >= 3 and size <= 8.5:
            return False
        # "J 00" pattern: chữ cái + số, cỡ lớn hơn body
        if re.match(r'^[A-Z]\s*\d+', t) and size > body_size + 1.0:
            return True
        # Các artifact khác ở đầu trang với cỡ lẻ
        if size > body_size + 2.0 and len(t) <= 10:
            return True
    return False


def detect_structure(name, start_page, end_page, doc):
    result = {
        "name": name,
        "pdf_pages": f"{start_page}-{end_page}",
        "body_size": None,
        "page_body_sizes": {},
        "left_margin": None,
        "headings": [],
        "paragraphs": [],
        "running_headers": [],
        "page_numbers": [],
        "footnotes": [],
        "section_numbers": [],
        "artifacts": [],
        "issues": [],
    }

    # === Pass 1: Trích xuất tất cả lines ===
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

    # === Pass 2: Xác định body_size và left_margin per-page ===
    page_body_sizes = {}
    margin_candidates = Counter()

    for line in all_lines:
        ph, pw = page_info[line["page"]]
        rel_y = line["y0"] / ph
        if 0.25 <= rel_y <= 0.80:
            margin_candidates[round(line["x0"], 0)] += 1

    for pnum in range(start_page, min(end_page + 1, doc.page_count + 1)):
        ph, pw = page_info[pnum]
        page_middle = Counter()
        for line in all_lines:
            if line["page"] != pnum:
                continue
            rel_y = line["y0"] / ph
            if 0.25 <= rel_y <= 0.80:
                sz = line["size"]
                if 6.5 <= sz <= 10.0:
                    page_middle[sz] += len(line["text"])
        if page_middle:
            most_common_sz, most_common_cnt = page_middle.most_common(1)[0]
            total_chars = sum(page_middle.values())
            if most_common_cnt / total_chars > 0.35:
                page_body_sizes[pnum] = round(most_common_sz, 1)
            else:
                page_body_sizes[pnum] = round(statistics.median(list(page_middle.elements())), 1)

    if page_body_sizes:
        result["body_size"] = round(statistics.median(list(page_body_sizes.values())), 1)
        result["page_body_sizes"] = page_body_sizes
    else:
        all_dom = [l["size"] for l in all_lines if 6.0 <= l["size"] <= 11.0]
        result["body_size"] = round(statistics.median(all_dom), 1) if all_dom else 7.4
        result["page_body_sizes"] = {}

    body_size = result["body_size"]

    if margin_candidates:
        result["left_margin"] = margin_candidates.most_common(1)[0][0]
    else:
        result["left_margin"] = 10.0

    left_margin = result["left_margin"]

    # === Pass 3: Phân loại từng line ===
    classified = []
    heading_counter = 0

    for line in all_lines:
        ph, pw = page_info[line["page"]]
        rel_y = line["y0"] / ph
        text = line["text"]
        size = line["size"]
        max_sz = line["max_size"]
        y0 = line["y0"]
        x0 = line["x0"]
        compact = re.sub(r'\s+', '', text)

        # 0. Artifact: "J 00" pattern ở đầu trang
        if is_artifact(text, size, y0, ph, body_size):
            result["artifacts"].append({
                "page": line["page"], "text": text, "size": size, "y": y0, "x": x0,
            })
            continue

        # 1. Page number: số đơn lẻ ở góc trên
        if re.match(r'^\d+$', text) and 6.0 <= size <= 10.0 and rel_y < 0.10:
            if x0 < 60 or x0 > pw - 90:
                result["page_numbers"].append({
                    "page": line["page"], "text": text, "size": size, "y": y0, "x": x0,
                })
                continue

        # 2. Running header: chữ in hoa, cỡ nhỏ, ở đầu trang
        if rel_y < 0.10:
            upper_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
            if upper_ratio > 0.7 and len(text) >= 3 and size <= 8.5:
                result["running_headers"].append({
                    "page": line["page"], "text": text, "size": size, "y": y0, "x": x0,
                })
                continue

        # 3. Chapter title: chứa "CHAPTER" ở đầu dòng
        if re.match(r'CHAPTER', compact, re.I) and rel_y < 0.30 and len(compact) < 60:
            heading_counter += 1
            result["headings"].append({
                "id": f"{id_prefix(name)}-H{heading_counter:03d}",
                "type": "chapter_title",
                "level": 1,
                "text": text,
                "page": line["page"], "y": y0, "x": x0,
                "size": size,
            })
            continue

        # 4. Part divider: "P A R T T W O" pattern
        if re.match(r'P\s*A\s*R\s*T\s*T\s*W\s*O', compact, re.I) and size >= 8.0:
            heading_counter += 1
            result["headings"].append({
                "id": f"{id_prefix(name)}-H{heading_counter:03d}",
                "type": "part_divider",
                "level": 1,
                "text": text,
                "page": line["page"], "y": y0, "x": x0,
                "size": size,
            })
            continue

        # 5. Part title: cỡ rất lớn (>= body_size + 15), nhưng loại trừ drop cap (1-2 ký tự)
        if size >= body_size + 15.0 and len(text.strip()) > 2:
            heading_counter += 1
            result["headings"].append({
                "id": f"{id_prefix(name)}-H{heading_counter:03d}",
                "type": "part_title",
                "level": 1,
                "text": text,
                "page": line["page"], "y": y0, "x": x0,
                "size": size,
            })
            continue

        # 6. Section number: Roman numeral hoặc số theo sau bằng dấu hai chấm
        if is_section_number(text, size, body_size):
            result["section_numbers"].append({
                "page": line["page"], "text": text, "size": size, "y": y0, "x": x0,
            })
            # Section number cũng là heading
            heading_counter += 1
            result["headings"].append({
                "id": f"{id_prefix(name)}-HS{heading_counter:03d}",
                "type": "section_number",
                "level": 2,
                "text": text,
                "page": line["page"], "y": y0, "x": x0,
                "size": size,
            })
            continue

        # 6.5. Drop cap: 1 ký tự, cỡ rất lớn, ở đầu trang → không classify làm heading, để rơi xuống body
        if len(text.strip()) == 1 and size >= body_size + 9.0 and rel_y < 0.10:
            pass  # Rơi xuống bước 9 (body classification)

        # 7. Heading: dominant_size đáng kể lớn hơn body (>= body_size + 4), loại trừ drop cap (1 ký tự)
        if size >= body_size + 4.0 and len(text.strip()) > 1:
            level = 1 if size >= body_size + 9.0 else (2 if size >= body_size + 6.0 else 3)
            heading_counter += 1
            result["headings"].append({
                "id": f"{id_prefix(name)}-H{heading_counter:03d}",
                "type": f"heading_l{level}",
                "level": level,
                "text": text,
                "page": line["page"], "y": y0, "x": x0,
                "size": size,
            })
            continue

        # 8. Footnote: font nhỏ hơn body (dùng per-page body_size), bất kỳ vị trí nào trên trang
        page_bs = page_body_sizes.get(line["page"], body_size)
        if size < page_bs - 0.5:
            # Kiểm tra có phải footnote marker không (bắt đầu bằng số mũ hoặc số)
            t = text.lstrip()
            is_fn = False
            if t and t[0] in SUP_DIGITS:
                is_fn = True
            elif re.match(r'^\[\d+\]', t):
                is_fn = True
            elif re.match(r'^\d{1,3}\s', t):
                is_fn = True
            # Hoặc: văn bản ở vùng dưới trang (rel_y > 0.85) với cỡ nhỏ
            elif rel_y > 0.85:
                is_fn = True
            # Hoặc: văn bản có dạng trích dẫn chuyên mục (tác giả, năm, trang)
            elif re.search(r'(op\. cit\.|loc\. cit\.|ibid\.|pp?\.\s*\d)', t, re.I):
                is_fn = True

            if is_fn:
                result["footnotes"].append({
                    "page": line["page"], "text": text, "size": size, "y": y0,
                })
                continue

        # 9. Mặc định: body paragraph line
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

    # === Pass 4: Gộp body lines thành paragraph ===
    body_lines = [c for c in classified if c["type"] == "body"]
    body_lines.sort(key=lambda c: (c["page"], c["y0"]))

    paragraphs = []
    para_counter = 0
    current_para = None

    indent_threshold = 3.0
    line_height = body_size * 1.2
    para_gap_threshold = line_height * 1.5

    for line in body_lines:
        if current_para is None:
            para_counter += 1
            current_para = {
                "para_id": f"{id_prefix(name)}-P{para_counter:03d}",
                "text": line["text"],
                "page_start": line["page"],
                "page_end": line["page"],
                "y_start": line["y0"],
                "y_end": line["y0"],
                "x0": line["x0"],
                "size": line["size"],
                "lines": [line["text"]],
                "pages": [line["page"]],
                "footnote_refs": extract_footnote_markers(line["text"]) + line.get("inline_fn_refs", []),
                "is_indented_start": line["x0"] > left_margin + indent_threshold,
            }
        else:
            same_page = line["page"] == current_para["page_start"]
            vertical_gap = line["y0"] - current_para["y_end"]
            is_indented = line["x0"] > left_margin + indent_threshold
            prev_ends_sentence = ends_sentence(current_para["lines"][-1])
            prev_ends_hyphen = ends_with_hyphen(current_para["lines"][-1])

            is_new_para = False

            if not same_page:
                # Trang mới: chỉ bắt đầu paragraph mới nếu dòng trước KHÔNG kết thúc bằng gạch ngang
                # Nếu dòng trước kết thúc bằng gạch ngang → đây là continuation của paragraph cùng
                if not prev_ends_hyphen:
                    is_new_para = True
                # Nếu dòng trước kết thúc bằng gạch ngang và dòng mới bắt đầu bằng chữ thường → gộp
                elif prev_ends_hyphen and starts_with_lowercase(line["text"]):
                    is_new_para = False
                else:
                    is_new_para = True
            elif vertical_gap > para_gap_threshold:
                is_new_para = True
            elif is_indented and prev_ends_sentence and vertical_gap > line_height * 0.8:
                is_new_para = True

            if is_new_para:
                paragraphs.append(current_para)
                para_counter += 1
                current_para = {
                    "para_id": f"{id_prefix(name)}-P{para_counter:03d}",
                    "text": line["text"],
                    "page_start": line["page"],
                    "page_end": line["page"],
                    "y_start": line["y0"],
                    "y_end": line["y0"],
                    "x0": line["x0"],
                    "size": line["size"],
                    "lines": [line["text"]],
                    "pages": [line["page"]],
                    "footnote_refs": extract_footnote_markers(line["text"]) + line.get("inline_fn_refs", []),
                    "is_indented_start": is_indented,
                }
            else:
                current_para["text"] += " " + line["text"]
                current_para["page_end"] = line["page"]
                current_para["y_end"] = line["y0"]
                current_para["lines"].append(line["text"])
                current_para["pages"].append(line["page"])
                current_para["footnote_refs"].extend(
                    extract_footnote_markers(line["text"]) + line.get("inline_fn_refs", [])
                )

    if current_para is not None:
        paragraphs.append(current_para)

    # === Pass 5: Gộp paragraph bị chia bởi dấu gạch ngang (cross-page hyphen) ===
    merged = []
    i = 0
    while i < len(paragraphs):
        cur = dict(paragraphs[i])
        j = i + 1
        while j < len(paragraphs):
            nxt = paragraphs[j]
            if ends_with_hyphen(cur["text"]) and starts_with_lowercase(nxt["text"]):
                if nxt["page_start"] == cur["page_start"] or nxt["page_start"] == cur["page_end"] + 1:
                    cur["text"] = cur["text"].rstrip("-").rstrip() + " " + nxt["text"].lstrip()
                    cur.setdefault("merged_from", []).append(nxt["para_id"])
                    cur["page_end"] = nxt["page_end"]
                    cur["y_end"] = nxt["y_end"]
                    cur["footnote_refs"].extend(nxt.get("footnote_refs", []))
                    cur["lines"].extend(nxt["lines"])
                    cur["pages"].extend(nxt["pages"])
                    j += 1
                    continue
            break
        merged.append(cur)
        i = j if j > i + 1 else i + 1

    # === Pass 5.5: Gộp drop cap (đoạn 1 ký tự ở đầu trang) với paragraph kế tiếp ===
    drop_cap_merged = []
    i = 0
    while i < len(merged):
        cur = dict(merged[i])
        # Kiểm tra drop cap: đúng 1 ký tự, ở đầu trang (y_start < 40), paragraph kế tiếp cùng trang
        is_drop_cap = (
            len(cur["text"].strip()) == 1
            and cur["y_start"] < 40
            and i + 1 < len(merged)
            and merged[i + 1]["page_start"] == cur["page_start"]
        )
        if is_drop_cap:
            nxt = merged[i + 1]
            cur["text"] = cur["text"].strip() + " " + nxt["text"].lstrip()
            cur.setdefault("merged_from", []).append(nxt["para_id"])
            cur["page_end"] = nxt["page_end"]
            cur["y_end"] = nxt["y_end"]
            cur["footnote_refs"].extend(nxt.get("footnote_refs", []))
            cur["lines"].extend(nxt["lines"])
            cur["pages"].extend(nxt["pages"])
            i += 2  # Bỏ qua cả drop cap và paragraph đã gộp
        else:
            drop_cap_merged.append(cur)
            i += 1

    result["paragraphs"] = drop_cap_merged
    result["total_paragraphs"] = len(drop_cap_merged)
    result["total_headings"] = len(result["headings"])
    result["total_footnotes"] = len(result["footnotes"])
    result["total_running_headers"] = len(result["running_headers"])
    result["total_section_numbers"] = len(result["section_numbers"])
    result["total_artifacts"] = len(result["artifacts"])

    # === Pass 6: Phát hiện artifact ngắn ở đầu trang bị classify nhầm làm body ===
    # Các đoạn ngắn (< 10 ký tự), ở vùng đầu trang (y_start < 40), không phải heading/footnote
    artifact_para_ids = []
    clean_paragraphs = []
    for p in drop_cap_merged:
        is_short_artifact = (
            len(p["text"].strip()) < 10
            and p["y_start"] < 40
            and not any(h["id"] == p["para_id"] for h in result["headings"])
        )
        if is_short_artifact:
            result["artifacts"].append({
                "page": p["page_start"],
                "text": p["text"],
                "size": p["size"],
                "y": p["y_start"],
                "x": p["x0"],
            })
            artifact_para_ids.append(p["para_id"])
        else:
            clean_paragraphs.append(p)

    # Re-index paragraph IDs sau khi loại artifact
    new_paragraphs = []
    para_counter = 0
    id_map = {}
    for p in clean_paragraphs:
        para_counter += 1
        new_id = f"{id_prefix(name)}-P{para_counter:03d}"
        id_map[p["para_id"]] = new_id
        p["para_id"] = new_id
        # Thêm trường page cho tương thích với validation script
        p["page"] = p["page_start"]
        # Cập nhật merged_from references
        if "merged_from" in p:
            p["merged_from"] = [id_map.get(m, m) for m in p["merged_from"]]
        new_paragraphs.append(p)

    result["paragraphs"] = new_paragraphs
    result["total_paragraphs"] = len(new_paragraphs)
    result["total_artifacts"] = len(result["artifacts"])

    return result


def normalize_obj(obj):
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, dict):
        return {k: normalize_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize_obj(v) for v in obj]
    return obj


def generate_src_txt(struct, name, start_page, end_page):
    """Tạo file ch04_src_REBUILT.txt từ structure."""
    lines = []
    lines.append(f"# {name.upper()} — {start_page}-{end_page}")
    lines.append(f"# Source structure rebuilt from original PDF")
    lines.append(f"# Encoding: UTF-8, NFC, LF")
    lines.append("")

    for p in struct["paragraphs"]:
        pid = p["para_id"]
        page = p["page_start"]
        text = p["text"].strip()
        if not text:
            continue
        lines.append(f"[{pid}] (trang {page})")
        lines.append(text)
        lines.append("")

    return "\n".join(lines)


def main():
    doc = fitz.open(PDF_PATH)
    print(f"PDF: {doc.page_count} pages")

    r = detect_structure(NAME, START_PAGE, END_PAGE, doc)

    print(f"\n=== {NAME} (pages {START_PAGE}-{END_PAGE}) ===")
    print(f"  Body size: {r.get('body_size')}, Left margin: {r.get('left_margin')}")
    print(f"  Headings: {r['total_headings']}, Paragraphs: {r['total_paragraphs']}")
    print(f"  Footnotes: {r['total_footnotes']}, Section numbers: {r['total_section_numbers']}")
    print(f"  Running headers: {r['total_running_headers']}, Page numbers: {len(r['page_numbers'])}")
    print(f"  Artifacts: {r['total_artifacts']}")
    if r["issues"]:
        print(f"  Issues: {r['issues']}")

    # In artifacts
    if r["artifacts"]:
        print(f"\n  Artifacts detected:")
        for a in r["artifacts"]:
            print(f"    p{a['page']} y={a['y']:.1f} x={a['x']:.1f} sz={a['size']}: '{a['text']}'")

    # In section numbers
    if r["section_numbers"]:
        print(f"\n  Section numbers detected:")
        for sn in r["section_numbers"]:
            print(f"    p{sn['page']} y={sn['y']:.1f} x={sn['x']:.1f} sz={sn['size']}: '{sn['text']}'")

    # In headings
    print(f"\n  Headings:")
    for h in r["headings"]:
        print(f"    [{h['id']}] {h['type']} L{h['level']} (p{h['page']}, sz={h['size']}): {h['text'][:80]}")

    # In paragraphs đầu
    print(f"\n  First 5 paragraphs:")
    for p in r["paragraphs"][:5]:
        print(f"    [{p['para_id']}] (p{p['page_start']}-{p['page_end']}): {p['text'][:80]}")

    # Lưu structure JSON — normalize NFC và dùng LF newline
    r_norm = normalize_obj(r)
    struct_path = os.path.join(V2, f"{NAME}_structure_REBUILT.json")
    with open(struct_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(r_norm, f, ensure_ascii=False, indent=2)
    print(f"\n  Saved: {struct_path}")

    # Tạo và lưu src TXT (chuẩn hóa NFC)
    src_content = generate_src_txt(r, NAME, START_PAGE, END_PAGE)
    src_content = unicodedata.normalize("NFC", src_content)
    src_path = os.path.join(V2, f"{NAME}_src_REBUILT.txt")
    with open(src_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src_content)
    print(f"  Saved: {src_path}")

    doc.close()
    print("\nDone!")


if __name__ == "__main__":
    main()