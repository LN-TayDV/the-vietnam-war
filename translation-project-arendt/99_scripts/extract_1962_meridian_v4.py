# -*- coding: utf-8 -*-
"""
extract_1962_meridian_v4.py — Trích xuất văn bản từ PDF Meridian 1962.

Phương pháp:
- Sử dụng page.get_text("text", sort=True) để lấy text theo thứ tự đọc (y, rồi x)
- Xử lý từng trang: tách thành các dòng, nhận diện đoạn văn
- Gộp đoạn văn chéo trang qua dấu gạch ngang
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
    
    Chi nhan cac heading co dang:
    - "CHAPTER one:" (in hoa, co dau hai chot)
    - "CHAPTER TWO" (toan bo in hoa)
    - "CHAPTER FIVE:" (in hoa)
    - Khong nhan "Chapter VIII," o dau trang chu (footnote) hoac "chapter" (thuong) trong noi dung
    """
    t = text.strip()
    # Phai bat dau boi "CHAPTER" (in hoa) hoac "Chapter " (dau viet hoa)
    if not re.match(r'^CHAPTER\s', t, re.I):
        return False
    # Sau "CHAPTER" phai co so La ma hoac so (one, two, three... hoac I, II, III...)
    after_chapter = t[len("CHAPTER"):].strip()
    # Loai tru "CHAPTER VIII," (dau phay = footnote reference)
    if re.match(r'^[IVXLC]+\s*[,:]', after_chapter, re.I):
        return False
    # Chap phai co it nhat mot ky tu sau CHAPTER (so hoac chu)
    if not after_chapter:
        return False
    return True


def is_part_divider(text):
    """Kiem tra xem co phai phan chia phan khong."""
    t = text.strip()
    compact = re.sub(r'\s+', '', t)
    return bool(re.match(r'P\s*A\s*R\s*T\s*[O|T|H|R|E|E]', compact, re.I)) and len(t) < 60


def extract_page_blocks(doc, pnum):
    """Trich xuat cac block text tu mot trang, sap xep theo thu tu doc (y, x)."""
    page = doc[pnum]
    page_num = pnum + 1
    
    # Lay text theo block, sap xep theo toa do
    blocks = page.get_text("blocks")
    
    page_blocks = []
    for block in blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        if block_type != 0:  # Chi lay text block
            continue
        text = text.strip()
        if not text:
            continue
        page_blocks.append({
            "text": text,
            "x0": x0,
            "y0": y0,
            "x1": x1,
            "y1": y1,
            "page": page_num,
        })
    
    # Sap xep theo y, sau do x
    page_blocks.sort(key=lambda b: (b["y0"], b["x0"]))
    return page_blocks


def build_paragraphs_from_blocks(page_blocks):
    """Xay dung doan van tu cac block text.
    
    Quy tắc:
    - Moi block la mot doan van (hoặc mot phần của doan)
    - Neu block ke tiep bat dau bang chu thuong va block truoc khong ket thuc boi dau cau => gop
    - Neu block ke tiep bat dau bang chu in hoa => doan moi
    """
    if not page_blocks:
        return []

    paragraphs = []
    current_text = page_blocks[0]["text"]
    current_page = page_blocks[0]["page"]

    for i in range(1, len(page_blocks)):
        block = page_blocks[i]
        text = block["text"]
        
        # Kiem tra co phai tiep tuc doan truoc khong
        if starts_with_lowercase(text) and not ends_sentence(current_text):
            # Noi chung: them khoang trang
            current_text = current_text + " " + text
        else:
            # Ket thuc doan hien tai, bat dau doan moi
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
        page_blocks = extract_page_blocks(doc, pnum)
        
        if not page_blocks:
            continue

        # Luu raw text
        raw_path = os.path.join(RAW_DIR, f"page_{page_num:03d}.txt")
        with open(raw_path, "w", encoding="utf-8", newline="\n") as f:
            for block in page_blocks:
                f.write(f"[{block['y0']:7.1f},{block['x0']:6.1f}] {block['text']}\n")

        # Xay dung doan van tu cac block cua trang nay
        page_paragraphs = build_paragraphs_from_blocks(page_blocks)
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
            # Chỉ gop neu: trang lien nhau, cua truu ket thuc boi dau gach ngang, moi bat dau bang chu thuong
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

    # === Xac dinh ranh gioi chuong ===
    chapter_boundaries = []
    chapter_counter = 0

    for p in merged_paragraphs:
        text = p["text"].strip()
        if is_chapter_heading(text):
            chapter_counter += 1
            ch_name = f"ch{chapter_counter:02d}"
            chapter_boundaries.append({
                "chapter": ch_name,
                "page": p["page"],
                "text": text[:80],
            })

    print(f"Chapters detected: {chapter_boundaries}")

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
