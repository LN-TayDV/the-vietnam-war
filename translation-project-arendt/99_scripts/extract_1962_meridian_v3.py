# -*- coding: utf-8 -*-
"""
extract_1962_meridian_v3.py — Trích xuất văn bản từ PDF Meridian 1962 bằng cách cắt cột.

Phương pháp:
- Mỗi trang được chia thành 2 cột (trái, phải) dựa trên x좌표
- Trích xuất text từ mỗi cột riêng biệt bằng page.get_text("text", clip=rect)
- Xử lý từng cột độc lập: tách paragraph, gộp chéo trang
- Xuất file v2_*_src.txt chuẩn: UTF-8, NFC, LF
"""

import fitz
import os
import re
import json
import unicodedata

PDF_PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\books\hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
RAW_DIR = os.path.join(BASE, "01_raw_text", "meridian_1962")
V2_DIR = os.path.join(BASE, "02_extracted_text", "v2")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(V2_DIR, exist_ok=True)

# Ngưỡng chia cột (được xác định từ phân tích: x < 170 là trái, x >= 170 là phải)
COLUMN_SPLIT_X = 170.0


def norm(s):
    return unicodedata.normalize("NFC", s)


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


def clean_text(t):
    t = t.replace("\u200b", "")
    t = re.sub(r'(\w)\u00ad\s+(\w)', r'\1\2', t)
    t = t.replace("\u00ad", "")
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def extract_column_text(doc, pnum, x0, y0, x1, y1, column_name):
    """Trích xuất text từ một vùng chữ (column) của trang."""
    page = doc[pnum]
    clip = fitz.Rect(x0, y0, x1, y1)
    text = page.get_text("text", clip=clip)
    return text


def parse_column_paragraphs(text, page_num, column_name):
    """Phân tách text của một cột thành các paragraph.
    
    Quy tắc:
    - Mỗi paragraph là một块 text liên tiếp, tách bởi dòng trắng hoặc khoảng cách dọc lớn
    - Xử lý dấu gạch ngang ở cuối dòng (nối từ)
    """
    if not text or not text.strip():
        return []

    # Chuẩn hóa: NFC, LF
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Tách thành dòng
    raw_lines = text.split("\n")

    # Lọc bỏ dòng trắng và giữ lại dòng có nội dung
    lines = []
    for line in raw_lines:
        line = line.strip()
        if line:
            lines.append(line)

    if not lines:
        return []

    # Gộp các dòng thành paragraph
    # Quy tắc: nếu dòng kết thúc bằng gạch ngang và dòng tiếp theo bắt đầu bằng chữ thường → gộp
    paragraphs = []
    current = lines[0]

    for i in range(1, len(lines)):
        next_line = lines[i]
        if ends_with_hyphen(current) and starts_with_lowercase(next_line):
            # Nối: bỏ gạch ngang, thêm khoảng trắng
            current = current.rstrip("-").rstrip() + " " + next_line
        else:
            paragraphs.append({
                "para_id": None,  # Sẽ gán sau
                "text": current,
                "page": page_num,
                "column": column_name,
            })
            current = next_line

    paragraphs.append({
        "para_id": None,
        "text": current,
        "page": page_num,
        "column": column_name,
    })

    return paragraphs


def generate_src_txt(name, paragraphs, start_page, end_page):
    """Tạo file v2_*_src.txt từ danh sách paragraph."""
    lines = []
    title = name.replace("_", " ").title()
    lines.append(f"# {title}")
    lines.append(f"# Source structure rebuilt from original PDF (Meridian 1962)")
    lines.append(f"# Pages: {start_page}-{end_page}")
    lines.append("# Encoding: UTF-8, NFC, LF")
    lines.append("")

    para_counter = 0
    for p in paragraphs:
        para_counter += 1
        pid = f"V1-{name[:2].upper()}-P{para_counter:03d}"
        page = p["page"]
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

    # Lấy kích thước trang từ trang đầu tiên có nội dung
    page_width = None
    page_height = None
    for pnum in range(doc.page_count):
        page = doc[pnum]
        if page_width is None:
            page_width = page.rect.width
            page_height = page.rect.height
        break

    print(f"Page size: {page_width:.1f} x {page_height:.1f}")

    # Xác định ranh giới cột
    left_x0 = 0
    left_x1 = COLUMN_SPLIT_X
    right_x0 = COLUMN_SPLIT_X
    right_x1 = page_width

    # Vùng nội dung (loại bỏ header/footer, margin)
    content_top = 40.0   # Bỏ qua header/top margin
    content_bottom = page_height - 50.0  # Bỏ qua footer/bottom margin

    # Trích xuất từng trang, từng cột
    all_paragraphs = []
    page_info = {}

    for pnum in range(doc.page_count):
        page = doc[pnum]
        page_text = page.get_text().strip()
        if not page_text:
            continue

        page_num = pnum + 1
        page_info[page_num] = {"width": page_width, "height": page_height}

        # Trích xuất cột trái
        left_text = extract_column_text(doc, pnum, left_x0, content_top, left_x1, content_bottom, "left")
        left_paras = parse_column_paragraphs(left_text, page_num, "left")

        # Trích xuất cột phải
        right_text = extract_column_text(doc, pnum, right_x0, content_top, right_x1, content_bottom, "right")
        right_paras = parse_column_paragraphs(right_text, page_num, "right")

        # Lưu raw text
        raw_path = os.path.join(RAW_DIR, f"page_{page_num:03d}.txt")
        with open(raw_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"=== LEFT COLUMN ===\n{left_text}\n\n=== RIGHT COLUMN ===\n{right_text}\n")

        # Thêm vào danh sách (trái trước, phải sau - đúng thứ tự đọc)
        all_paragraphs.extend(left_paras)
        all_paragraphs.extend(right_paras)

    print(f"Extracted paragraphs from {len(page_info)} pages")

    # === Gộp paragraph chéo trang (cùng cột) ===
    # Sắp xếp theo cột (trái trước phải sau), rồi theo trang
    column_order = {"left": 0, "right": 1}
    all_paragraphs.sort(key=lambda p: (column_order.get(p["column"], 0), p["page"]))

    merged_paragraphs = []
    i = 0
    while i < len(all_paragraphs):
        cur = dict(all_paragraphs[i])
        j = i + 1
        while j < len(all_paragraphs):
            nxt = all_paragraphs[j]
            # Chỉ gộp nếu: cùng cột, trang liền nhau, dòng trước kết thúc bằng gạch ngang, dòng mới bắt đầu chữ thường
            if cur["column"] == nxt["column"] and nxt["page"] == cur["page"] + 1:
                if ends_with_hyphen(cur["text"]) and starts_with_lowercase(nxt["text"]):
                    cur["text"] = cur["text"].rstrip("-").rstrip() + " " + nxt["text"].lstrip()
                    cur["page"] = nxt["page"]
                    j += 1
                    continue
            break
        merged_paragraphs.append(cur)
        i = j if j > i + 1 else i + 1

    print(f"After cross-page merge: {len(merged_paragraphs)} paragraphs")

    # === Phân chia theo chương và xuất file ===
    # Xác định chương từ text của paragraph đầu tiên trên mỗi trang
    chapter_boundaries = []
    chapter_counter = 0

    for p in merged_paragraphs:
        text = p["text"]
        if re.match(r'CHAPTER|Chapter', text, re.I):
            chapter_counter += 1
            ch_name = f"ch{chapter_counter:02d}"
            chapter_boundaries.append({
                "chapter": ch_name,
                "page": p["page"],
                "text": text[:80],
            })

    print(f"Chapters detected: {chapter_boundaries}")

    # Gán chapter cho mỗi paragraph
    for p in merged_paragraphs:
        p["chapter"] = None
        for cb in chapter_boundaries:
            if p["page"] >= cb["page"]:
                p["chapter"] = cb["chapter"]
            else:
                break
        if p["chapter"] is None:
            p["chapter"] = "front_matter"

    chapter_names = ["front_matter"] + [cb["chapter"] for cb in chapter_boundaries]

    for ch_name in chapter_names:
        ch_paras = [p for p in merged_paragraphs if p["chapter"] == ch_name]
        if not ch_paras:
            continue

        pages = [p["page"] for p in ch_paras]
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
