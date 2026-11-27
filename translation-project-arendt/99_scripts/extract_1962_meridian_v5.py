# -*- coding: utf-8 -*-
"""
extract_1962_meridian_v5.py — Trích xuất văn bản từ PDF Meridian 1962 (552 trang).

Phương pháp:
- Trích xuất text blocks từ mỗi trang với toa do
- Phân chia block vao cot trai/phai theo x0 (nguong x=170)
- Sap xep block trong moi cot theo y0
- Doc cot trai truoc, cot phai sau (thu tu doc dung cua sach hai cot)
- Xay dung doan van, gop chéo trang qua dau gach ngang
- Xac dinh chuong theo pattern "CHAPTER one:" (in hoa, co dau hai cham)
- Xuat file v2_*_src.txt chuan: UTF-8, NFC, LF
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


def is_chapter_heading(text):
    """Kiem tra xem co phai chuong cua sach khong.
    
    Chi nhan:
    - "CHAPTER one:" / "CHAPTER TWO" / "CHAPTER FIVE:" (in hoa, co so sau)
    - Khong nhan "CHAPTER VIII," (dau phay = footnote)
    - Khong nhan "chapter" (thuong) trong noi dung
    """
    t = text.strip()
    if not re.match(r'^CHAPTER\s', t, re.I):
        return False
    after = t[len("CHAPTER"):].strip()
    # Loai tru "CHAPTER VIII," (dau phay = footnote reference)
    if re.match(r'^[IVXLC]+\s*[,:]', after, re.I):
        return False
    # Phai co it nhat mot ky tu so hoac chu sau CHAPTER
    if not after or not re.search(r'[\wIVXLC]', after):
        return False
    return True


def extract_page_columns(doc, pnum):
    """Trich xuat block text cua trang, phan chia vao cot trai/phai, sap xep theo y."""
    page = doc[pnum]
    page_num = pnum + 1
    blocks = page.get_text("blocks")

    left_blocks = []
    right_blocks = []

    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        if block_type != 0:
            continue
        text = text.strip()
        if not text:
            continue
        block_info = {
            "text": text,
            "x0": x0,
            "y0": y0,
            "x1": x1,
            "y1": y1,
            "page": page_num,
        }
        # Phan chia cot theo x0
        if x0 < COLUMN_SPLIT_X:
            left_blocks.append(block_info)
        else:
            right_blocks.append(block_info)

    # Sap xep trong moi cot theo y0
    left_blocks.sort(key=lambda b: b["y0"])
    right_blocks.sort(key=lambda b: b["y0"])

    return left_blocks, right_blocks


def build_page_reading_order(left_blocks, right_blocks, page_num):
    """Ghep cot trai va cot phai thanh danh sach block theo thu tu doc dung."""
    ordered = []
    for b in left_blocks:
        ordered.append(b)
    for b in right_blocks:
        ordered.append(b)
    return ordered


def build_paragraphs_from_ordered_blocks(ordered_blocks):
    """Xay dung doan van tu cac block da sap xep thu tu doc.
    
    Quy tắc:
    - Mỗi block là một đoạn text
    - Nếu block tiếp theo bắt đầu bằng chữ thường VÀ block trước KHÔNG kết thúc bằng dấu câu → gộp
    - Nếu block tiếp theo bắt đầu bằng chữ in hoa → đoạn mới
    """
    if not ordered_blocks:
        return []

    paragraphs = []
    current_text = ordered_blocks[0]["text"]
    current_page = ordered_blocks[0]["page"]

    for i in range(1, len(ordered_blocks)):
        block = ordered_blocks[i]
        text = block["text"]

        if starts_with_lowercase(text) and not ends_sentence(current_text):
            current_text = current_text + " " + text
        else:
            paragraphs.append({
                "text": current_text,
                "page": current_page,
            })
            current_text = text
            current_page = block["page"]

    paragraphs.append({
        "text": current_text,
        "page": current_page,
    })

    return paragraphs


def generate_src_txt(name, paragraphs, start_page, end_page):
    """Tao file v2_*_src.txt tu danh sach paragraph."""
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

    all_paragraphs = []

    for pnum in range(doc.page_count):
        page_num = pnum + 1
        left_blocks, right_blocks = extract_page_columns(doc, pnum)

        if not left_blocks and not right_blocks:
            continue

        # Luu raw text
        raw_path = os.path.join(RAW_DIR, f"page_{page_num:03d}.txt")
        with open(raw_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("=== LEFT COLUMN ===\n")
            for b in left_blocks:
                f.write(f"[{b['y0']:7.1f},{b['x0']:6.1f}] {b['text']}\n")
            f.write("\n=== RIGHT COLUMN ===\n")
            for b in right_blocks:
                f.write(f"[{b['y0']:7.1f},{b['x0']:6.1f}] {b['text']}\n")

        # Ghep theo thu tu doc: cot trai truoc, cot phai sau
        ordered = build_page_reading_order(left_blocks, right_blocks, page_num)

        # Xay dung doan van
        page_paragraphs = build_paragraphs_from_ordered_blocks(ordered)
        all_paragraphs.extend(page_paragraphs)

    print(f"Extracted {len(all_paragraphs)} paragraphs from {doc.page_count} pages")

    # === Gop doan van chéo trang ===
    merged_paragraphs = []
    i = 0
    while i < len(all_paragraphs):
        cur = dict(all_paragraphs[i])
        j = i + 1
        while j < len(all_paragraphs):
            nxt = all_paragraphs[j]
            if nxt["page"] == cur["page"] + 1:
                if ends_with_hyphen(cur["text"]) and starts_with_lowercase(nxt["text"]):
                    cur["text"] = cur["text"].rstrip("-").rstrip() + " " + nxt["text"].lstrip()
                    cur["page"] = nxt["page"]
                    j += 1
                    continue
            break
        merged_paragraphs.append(cur)
        i = j if j > i + 1 else i + 1

    print(f"After cross-page merge: {len(merged_paragraphs)} paragraphs")

    # === Xac dinh ranh gioi chuong (13 chuong co san, xac dinh tu toc muc trang 17-18) ===
    chapter_boundaries = [
        {"chapter": "front_matter", "page": 1, "text": "Front matter"},
        {"chapter": "ch01", "page": 23, "text": "CHAPTER one: Antisemitism as an Outrage to Common Sense"},
        {"chapter": "ch02", "page": 31, "text": "CHAPTER two: The Jews, the Nation-State, and the Birth of Antisemitism"},
        {"chapter": "ch03", "page": 75, "text": "CHAPTER three: The Jews and Society"},
        {"chapter": "ch04", "page": 109, "text": "CHAPTER FOUR: The Dreyfus Affair"},
        {"chapter": "ch05", "page": 143, "text": "CHAPTER five: The Political Emancipation of the Bourgeoisie"},
        {"chapter": "ch06", "page": 179, "text": "CHAPTER six: Race-Thinking Before Racism"},
        {"chapter": "ch07", "page": 205, "text": "CHAPTER SEVEN: Race and Bureaucracy"},
        {"chapter": "ch08", "page": 243, "text": "CHAPTER eight: Continental Imperialism: The Pan-Movements"},
        {"chapter": "ch09", "page": 287, "text": "CHAPTER nine: The Decline of the Nation-State and the End of the Rights of Man"},
        {"chapter": "ch10", "page": 325, "text": "CHAPTER TEN: A Classless Society"},
        {"chapter": "ch11", "page": 361, "text": "CHAPTER ELEVEN: The Totalitarian Movement"},
        {"chapter": "ch12", "page": 409, "text": "CHAPTER TWELVE: Totalitarianism in Power"},
        {"chapter": "ch13", "page": 481, "text": "CHAPTER THIRTEEN: Ideology and Terror"},
    ]

    chapter_names = [cb["chapter"] for cb in chapter_boundaries]

    print(f"Chapters ({len(chapter_boundaries)}):")
    for cb in chapter_boundaries:
        print(f"  {cb['chapter']}: page {cb['page']} - {cb['text'][:60]}")

    # Gan chapter cho moi paragraph
    for p in merged_paragraphs:
        p["chapter"] = None
        for cb in chapter_boundaries:
            if p["page"] >= cb["page"]:
                p["chapter"] = cb["chapter"]
            else:
                break
        if p["chapter"] is None:
            p["chapter"] = "front_matter"

    chapter_names = [cb["chapter"] for cb in chapter_boundaries]

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
