# -*- coding: utf-8 -*-
"""
extract_1962_meridian_v2.py — Trích xuất văn bản từ PDF Meridian 1962 với xử lý cột hai cột.

Cải tiến từ phiên bản trước:
- Phân biệt cột trái và cột phải dựa trên x0 (ngưỡng cột chia khoảng x=170)
- Sắp xếp dòng theo (cột, y0) thay vì chỉ y0 để tránh xen kẽ hai cột
- Gộp đoạn văn chéo trang đúng cách
"""

import fitz
import os
import re
import json
import unicodedata
import statistics
from collections import Counter

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
RAW_DIR = os.path.join(BASE, "01_raw_text", "meridian_1962")
V2_DIR = os.path.join(BASE, "02_extracted_text", "v2")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(V2_DIR, exist_ok=True)

SUP_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
COLUMN_SPLIT_X = 170.0  # Ngưỡng chia cột trái / cột phải


def norm(s):
    return unicodedata.normalize("NFC", s)


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


def is_section_number(text, body_size):
    t = text.strip()
    if re.match(r'^[IVX]+:\s*$', t, re.I):
        return True
    if re.match(r'^\d{1,3}\s*:', t):
        return True
    return False


def is_artifact(text, size, y0, page_height, body_size):
    t = text.strip()
    rel_y = y0 / page_height
    if rel_y < 0.05:
        if re.match(r'^\d+$', t):
            return False
        upper_ratio = sum(1 for c in t if c.isupper()) / max(len(t), 1)
        if upper_ratio > 0.7 and len(t) >= 3 and size <= 8.5:
            return False
        if re.match(r'^[A-Z]\s*\d+', t) and size > body_size + 1.0:
            return True
        if size > body_size + 2.0 and len(t) <= 10:
            return True
    return False


def clean_text(t):
    t = t.replace("\u200b", "")
    t = re.sub(r'(\w)\u00ad\s+(\w)', r'\1\2', t)
    t = t.replace("\u00ad", "")
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def extract_page_lines(doc, pnum):
    page = doc[pnum]
    pnum_1 = pnum + 1
    ph = page.rect.height
    pw = page.rect.width
    d = page.get_text("dict")

    lines = []
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
            # Xác định cột: trái (x0 < COLUMN_SPLIT_X) hoặc phải (x0 >= COLUMN_SPLIT_X)
            column = "left" if min_x < COLUMN_SPLIT_X else "right"
            lines.append({
                "text": line_text,
                "size": dom_sz,
                "max_size": max(round(s["size"], 1) for s in spans),
                "x0": min_x,
                "y0": min_y,
                "x1": max_x,
                "page": pnum_1,
                "ph": ph,
                "pw": pw,
                "column": column,
                "spans": spans,
            })
    return lines


def detect_body_size_and_margin(all_lines):
    page_info = {}
    for line in all_lines:
        page_info.setdefault(line["page"], []).append(line)

    page_body_sizes = {}
    margin_candidates = Counter()

    for page_num, plines in page_info.items():
        ph = plines[0]["ph"]
        for line in plines:
            rel_y = line["y0"] / ph
            if 0.25 <= rel_y <= 0.80:
                margin_candidates[round(line["x0"], 0)] += 1

        page_middle = Counter()
        for line in plines:
            rel_y = line["y0"] / ph
            if 0.25 <= rel_y <= 0.80:
                sz = line["size"]
                if 6.0 <= sz <= 11.0:
                    page_middle[sz] += len(line["text"])
        if page_middle:
            most_common_sz, most_common_cnt = page_middle.most_common(1)[0]
            total_chars = sum(page_middle.values())
            if most_common_cnt / total_chars > 0.35:
                page_body_sizes[page_num] = round(most_common_sz, 1)
            else:
                page_body_sizes[page_num] = round(statistics.median(list(page_middle.elements())), 1)

    body_size = round(statistics.median(list(page_body_sizes.values())), 1) if page_body_sizes else 6.6
    left_margin = margin_candidates.most_common(1)[0][0] if margin_candidates else 19.0

    return body_size, left_margin, page_body_sizes


def classify_lines(all_lines, body_size, left_margin, page_body_sizes):
    classified = []
    heading_counter = 0

    for line in all_lines:
        ph = line["ph"]
        pw = line["pw"]
        rel_y = line["y0"] / ph
        text = line["text"]
        size = line["size"]
        y0 = line["y0"]
        x0 = line["x0"]
        compact = re.sub(r'\s+', '', text)

        # 1. Page number
        if re.match(r'^\d+$', text) and 6.0 <= size <= 10.0 and rel_y < 0.10:
            if x0 < 60 or x0 > pw - 90:
                classified.append({
                    "type": "page_number", "text": text, "size": size,
                    "y": y0, "x": x0, "page": line["page"],
                })
                continue

        # 2. Part divider
        if re.match(r'P\s*A\s*R\s*T\s*[O|T|H|R|E|E]', compact, re.I) and size >= 10.0:
            heading_counter += 1
            classified.append({
                "type": "part_divider", "text": text, "size": size,
                "y": y0, "x": x0, "page": line["page"],
                "heading_id": f"V1-H{heading_counter:03d}",
                "level": 1,
            })
            continue

        # 3. Chapter title
        if re.match(r'CHAPTER|Chapter', compact, re.I) and size >= 10.0:
            heading_counter += 1
            classified.append({
                "type": "chapter_title", "text": text, "size": size,
                "y": y0, "x": x0, "page": line["page"],
                "heading_id": f"V1-H{heading_counter:03d}",
                "level": 1,
            })
            continue

        # 4. Part title
        if size >= body_size + 12.0 and len(text.strip()) > 1:
            heading_counter += 1
            classified.append({
                "type": "part_title", "text": text, "size": size,
                "y": y0, "x": x0, "page": line["page"],
                "heading_id": f"V1-H{heading_counter:03d}",
                "level": 1,
            })
            continue

        # 5. Section number
        if is_section_number(text, body_size):
            heading_counter += 1
            classified.append({
                "type": "section_number", "text": text, "size": size,
                "y": y0, "x": x0, "page": line["page"],
                "heading_id": f"V1-HS{heading_counter:03d}",
                "level": 2,
            })
            continue

        # 6. Drop cap
        if len(text.strip()) == 1 and size >= body_size + 9.0 and rel_y < 0.10:
            pass

        # 7. Heading
        if size >= body_size + 4.0 and len(text.strip()) > 1:
            level = 1 if size >= body_size + 9.0 else (2 if size >= body_size + 6.0 else 3)
            heading_counter += 1
            classified.append({
                "type": "heading", "text": text, "size": size,
                "y": y0, "x": x0, "page": line["page"],
                "heading_id": f"V1-H{heading_counter:03d}",
                "level": level,
            })
            continue

        # 8. Footnote
        page_bs = page_body_sizes.get(line["page"], body_size)
        t = text.lstrip()
        is_fn = False

        if size < page_bs - 0.5:
            if t and t[0] in SUP_DIGITS:
                is_fn = True
            elif re.match(r'^\[\d+\]', t):
                is_fn = True
            elif re.match(r'^\d{1,3}\s', t):
                is_fn = True
            elif rel_y > 0.85:
                is_fn = True
            elif re.search(r'(op\. cit\.|loc\. cit\.|ibid\.|pp?\.\s*\d)', t, re.I):
                is_fn = True

        if is_fn:
            classified.append({
                "type": "footnote", "text": text, "size": size, "y": y0,
                "page": line["page"],
            })
            continue

        # 9. Body paragraph line
        inline_refs = []
        for s in line["spans"]:
            st = s["text"].strip()
            sz = round(s["size"], 1)
            if re.match(r'^\d{1,3}$', st) and sz < size - 0.5:
                inline_refs.append(int(st))
        classified.append({
            "type": "body", "text": text, "size": size,
            "x0": x0, "y0": y0, "page": line["page"],
            "column": line["column"],
            "inline_fn_refs": inline_refs,
        })

    return classified, heading_counter


def build_paragraphs(classified, body_size, left_margin):
    """Gộp body lines thành paragraph, xử lý theo cột rồi chéo trang."""
    body_lines = [c for c in classified if c["type"] == "body"]
    # Sắp xếp theo trang trước, sau đó cột (trái trước phải sau), rồi y0
    column_order = {"left": 0, "right": 1}
    body_lines.sort(key=lambda c: (c["page"], column_order.get(c.get("column", "left"), 0), c["y0"]))

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
                "para_id": f"V1-P{para_counter:03d}",
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
            same_column = line.get("column", "left") == current_para.get("column", "left")
            vertical_gap = line["y0"] - current_para["y_end"]
            is_indented = line["x0"] > left_margin + indent_threshold
            prev_ends_sentence = ends_sentence(current_para["lines"][-1])
            prev_ends_hyphen = ends_with_hyphen(current_para["lines"][-1])

            is_new_para = False

            if same_page and same_column:
                # Cùng trang, cùng cột: điều kiện thông thường
                if vertical_gap > para_gap_threshold:
                    is_new_para = True
                elif is_indented and prev_ends_sentence and vertical_gap > line_height * 0.8:
                    is_new_para = True
            elif same_page and not same_column:
                # Đổi cột trên cùng trang (trái→phải): LUONLÀ đoạn mới, không gộp qua cột
                is_new_para = True
            else:
                # Đổi trang (phải trang N → trái trang N+1): kiểm tra hyphen continuation
                if prev_ends_hyphen and starts_with_lowercase(line["text"]):
                    is_new_para = False  # Gộp: dấu gạch ngang nối dòng chéo trang
                else:
                    is_new_para = True  # Đoạn mới

            if is_new_para:
                paragraphs.append(current_para)
                para_counter += 1
                current_para = {
                    "para_id": f"V1-P{para_counter:03d}",
                    "text": line["text"],
                    "page_start": line["page"],
                    "page_end": line["page"],
                    "y_start": line["y0"],
                    "y_end": line["y0"],
                    "x0": line["x0"],
                    "size": line["size"],
                    "lines": [line["text"]],
                    "pages": [line["page"]],
                    "column": line.get("column", "left"),
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

    # Gộp paragraph bị chia bởi dấu gạch ngang (chỉ chéo trang, cùng cột)
    merged = []
    i = 0
    while i < len(paragraphs):
        cur = dict(paragraphs[i])
        j = i + 1
        while j < len(paragraphs):
            nxt = paragraphs[j]
            if ends_with_hyphen(cur["text"]) and starts_with_lowercase(nxt["text"]):
                if nxt["page_start"] == cur["page_end"] + 1 and cur.get("column") == nxt.get("column"):
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

    return merged


def generate_src_txt(name, paragraphs, start_page, end_page):
    lines = []
    title = name.replace("_", " ").title()
    lines.append(f"# {title}")
    lines.append(f"# Source structure rebuilt from original PDF (Meridian 1962)")
    lines.append(f"# Pages: {start_page}-{end_page}")
    lines.append("# Encoding: UTF-8, NFC, LF")
    lines.append("")

    for p in paragraphs:
        pid = p["para_id"]
        page = p["page_start"]
        text = p["text"].strip()
        if not text:
            continue
        lines.append(f"[{pid}] (trang {page})")
        lines.append(text)
        lines.append("")

    content = "\n".join(lines)
    content = unicodedata.normalize("NFC", content)
    return content


def main():
    doc = fitz.open(PDF_PATH)
    print(f"PDF: {doc.page_count} pages")

    # Pass 1: Trích xuất tất cả lines
    all_lines = []
    for pnum in range(doc.page_count):
        page_lines = extract_page_lines(doc, pnum)
        all_lines.extend(page_lines)

    # Lưu raw text từng trang
    page_info = {}
    for line in all_lines:
        page_info.setdefault(line["page"], []).append(line)

    for pnum in range(1, doc.page_count + 1):
        if pnum not in page_info:
            continue
        plines = sorted(page_info[pnum], key=lambda l: (l["column"], l["y0"]))
        raw_lines = []
        for line in plines:
            raw_lines.append(f"[{line['y0']:7.1f},{line['x0']:6.1f},{line['size']:5.1f},{line['column']}] {line['text']}")
        raw_path = os.path.join(RAW_DIR, f"page_{pnum:03d}.txt")
        with open(raw_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(raw_lines))

    print(f"Raw text extracted for {len(page_info)} pages")

    # Pass 2: body_size và left_margin
    body_size, left_margin, page_body_sizes = detect_body_size_and_margin(all_lines)
    print(f"Body size: {body_size}, Left margin: {left_margin}")

    # Pass 3: Phân loại từng line
    classified, heading_counter = classify_lines(all_lines, body_size, left_margin, page_body_sizes)
    type_counts = Counter(c["type"] for c in classified)
    print(f"Line classification: {dict(type_counts)}")

    # Pass 4: Gộp body lines thành paragraph
    paragraphs = build_paragraphs(classified, body_size, left_margin)
    print(f"Total paragraphs: {len(paragraphs)}")

    # Pass 5: Phân chia theo chương và xuất file
    chapter_boundaries = []
    current_chapter = None
    chapter_counter = 0

    for item in classified:
        if item["type"] == "chapter_title":
            chapter_counter += 1
            ch_name = f"ch{chapter_counter:02d}"
            chapter_boundaries.append({
                "chapter": ch_name,
                "page": item["page"],
                "y": item["y"],
                "text": item["text"],
            })
            current_chapter = ch_name

    print(f"Chapters detected: {chapter_boundaries}")

    for p in paragraphs:
        p["chapter"] = None
        for cb in chapter_boundaries:
            if p["page_start"] >= cb["page"]:
                p["chapter"] = cb["chapter"]
            else:
                break
        if p["chapter"] is None:
            p["chapter"] = "front_matter"

    chapter_names = ["front_matter"] + [cb["chapter"] for cb in chapter_boundaries]

    for ch_name in chapter_names:
        ch_paras = [p for p in paragraphs if p["chapter"] == ch_name]
        if not ch_paras:
            continue

        pages = [p["page_start"] for p in ch_paras]
        start_page = min(pages)
        end_page = max(pages)

        content = generate_src_txt(ch_name, ch_paras, start_page, end_page)
        out_path = os.path.join(V2_DIR, f"v2_{ch_name}_src.txt")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"  {ch_name}: {len(ch_paras)} paragraphs, pages {start_page}-{end_page}")

    meta_path = os.path.join(V2_DIR, "chapter_boundaries.json")
    with open(meta_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(chapter_boundaries, f, ensure_ascii=False, indent=2)

    doc.close()
    print("\nDone!")


if __name__ == "__main__":
    main()
