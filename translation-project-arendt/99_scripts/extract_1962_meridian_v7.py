# -*- coding: utf-8 -*-
"""
extract_1962_meridian_v7.py — Trích xuất văn bản từ PDF Meridian 1962 (552 trang).

Tuân thủ NGUYÊN TẮC TRÍCH XUẤT QUAN TRỌNG 5 BƯỚC:
  Bước 1: Trích xuất cấp trang (loại bỏ running header/số trang, tách body/footnote, giữ thứ tự đọc)
  Bước 2: Phục hồi sự liên tục đoạn văn chéo trang
  Bước 3: Xây dựng cấu trúc chương (CHAPTER → HEADING → SUBHEADING → PARAGRAPH)
  Bước 4: Tạo Source TXT sạch (không header, không số trang, mỗi đoạn một dòng)
  Bước 5: Tạo manifest xác minh liên tục cho mọi chuyển tiếp trang

Đầu vào:  01_raw_text/meridian_1962/page_XXX.txt (đã trích xuất bởi PyMuPDF)
Đầu ra:   02_extracted_text/v7/v2_*_src.txt (Source TXT cho mỗi chương)
          02_extracted_text/v7/manifest_continuity.json (manifest liên tục)
          02_extracted_text/v7/chapter_boundaries.json (ranh giới chương)

Mã hóa: UTF-8, NFC, LF
"""

import fitz
import os
import re
import json
import unicodedata
import sys
from collections import OrderedDict

sys.stdout.reconfigure(encoding="utf-8")

PDF_PATH = "/workspaces/the-vietnam-war/books/hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf"

BASE = "/workspaces/the-vietnam-war/translation-project-arendt"
RAW_DIR = os.path.join(BASE, "01_raw_text", "meridian_1962")
V7_DIR = os.path.join(BASE, "02_extracted_text", "v7")
os.makedirs(V7_DIR, exist_ok=True)

# ── Cấu hình ngưỡng vị trí (từ phân tích header trên 552 trang) ──
HEADER_Y_THRESHOLD = 60.0      # y0 < 60: vùng header (trên cùng trang)
FOOTNOTE_Y_THRESHOLD = 450.0   # y0 > 450: vùng chân trang (có thể là footnote)
PAGE_HEIGHT = 792.0            # Chiều cao trang PDF (giá trị chuẩn letter)

# ── Ran h gioi chuong (13 chuong, xac dinh tu toc muc Meridian 1962) ──
CHAPTER_BOUNDARIES = [
    {"chapter": "front_matter", "page": 1,  "text": "Front matter"},
    {"chapter": "ch01",         "page": 23, "text": "CHAPTER one: Antisemitism as an Outrage to Common Sense"},
    {"chapter": "ch02",         "page": 31, "text": "CHAPTER two: The Jews, the Nation-State, and the Birth of Antisemitism"},
    {"chapter": "ch03",         "page": 75, "text": "CHAPTER three: The Jews and Society"},
    {"chapter": "ch04",         "page": 109,"text": "CHAPTER FOUR: The Dreyfus Affair"},
    {"chapter": "ch05",         "page": 143,"text": "CHAPTER five: The Political Emancipation of the Bourgeoisie"},
    {"chapter": "ch06",         "page": 179,"text": "CHAPTER six: Race-Thinking Before Racism"},
    {"chapter": "ch07",         "page": 205,"text": "CHAPTER SEVEN: Race and Bureaucracy"},
    {"chapter": "ch08",         "page": 243,"text": "CHAPTER eight: Continental Imperialism: The Pan-Movements"},
    {"chapter": "ch09",         "page": 287,"text": "CHAPTER nine: The Decline of the Nation-State and the End of the Rights of Man"},
    {"chapter": "ch10",         "page": 325,"text": "CHAPTER TEN: A Classless Society"},
    {"chapter": "ch11",         "page": 361,"text": "CHAPTER ELEVEN: The Totalitarian Movement"},
    {"chapter": "ch12",         "page": 409,"text": "CHAPTER TWELVE: Totalitarianism in Power"},
    {"chapter": "ch13",         "page": 481,"text": "CHAPTER THIRTEEN: Ideology and Terror"},
]

CHAPTER_START_PAGES = [cb["page"] for cb in CHAPTER_BOUNDARIES]
CHAPTER_NAMES = [cb["chapter"] for cb in CHAPTER_BOUNDARIES]


def norm(s):
    """Chuẩn hóa Unicode NFC."""
    return unicodedata.normalize("NFC", s)


def clean_text(t):
    """Làm sạch văn bản: xóa zero-width space, nối từ bị gạch nối mềm, chuẩn hóa khoảng trắng."""
    t = t.replace("\u200b", "")
    # Nối từ bị tách bởi gạch nối mềm (soft hyphen ­) ở cuối dòng
    t = re.sub(r'(\w)\u00ad\s+(\w)', r'\1\2', t)
    t = t.replace("\u00ad", "")
    # Xóa các ký tự OCR rác phổ biến
    t = re.sub(r'[£„„]', '', t)  # ký tự OCR sai
    # Sửa lỗi OCR phổ biến: chữ hoa U giữa 2 chữ thường -> chữ thường l (ví dụ: equaUty→equality, poUtical→political)
    t = re.sub(r'([a-z])U([a-z])', r'\1l\2', t)
    # Chuẩn hóa khoảng trắng
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def is_chapter_heading(text):
    """Kiểm tra xem có phảiHeading chương (chứa 'CHAPTER') hay không."""
    return bool(re.search(r'CHAPTER', text, re.IGNORECASE))


def is_running_header(text, y0):
    """
    Kiểm tra xem block có phải là running header (can xoa) hay khong.
    
    Running header:
    - o dau trang (y0 < HEADER_Y_THRESHOLD)
    - KHONG chua tu 'CHAPTER' (vi do la heading cua chuong, can giu)
    - La van degan ngunga (nhu 'ANTISEMITISM', 'IMPERIALISM', 'TOTALITARIANISM')
    """
    if y0 >= HEADER_Y_THRESHOLD:
        return False
    if is_chapter_heading(text):
        return False
    # Xoa neu la van degan ngunga (nhung chu viet hoa, ngan)
    t = text.strip()
    if not t:
        return False
    # Neu chi co 1-2 tu viet hoa va khong co dau cau ket thuc => header
    words = t.split()
    if len(words) <= 4 and all(w.isupper() or re.match(r'^[A-Z]', w) for w in words):
        if not re.search(r'[.!?]$', t):
            return True
    # Neu chua cac tu khoa header biet
    header_keywords = ['ANTISEMITISM', 'IMPERIALISM', 'TOTALITARIANISM',
                       'INDEX', 'MERIDIAN', 'JEWS AND SOCIETY',
                       'CONTINENTAL IMPERIALISM', 'IDEOLOGY AND TERROR',
                       'THE TOTALITARIAN MOVEMENT', 'RACE AND BUREAUCRACY']
    for kw in header_keywords:
        if kw in t.upper():
            return True
    return False


def is_footnote(text, y0, page_height=PAGE_HEIGHT):
    """
    Kiem tra xem block co phai footnote hay khong.
    
    Footnote:
    - o duoi trang (y0 > FOOTNOTE_Y_THRESHOLD), HOAC
    - Bat dau boi chu so + khoang trang (vi du: '1 J. A. Hobson...')
    """
    t = text.strip()
    if not t:
        return False
    # Vi tri o duoi trang
    if y0 > FOOTNOTE_Y_THRESHOLD:
        return True
    # Bat dau boi chu so + khoang trang + ten tac gia / cuon sach
    if re.match(r'^\d+\s+[A-Z]', t):
        return True
    return False


def is_page_number(text):
    """Kiem tra xem block co phai so trang doc lap hay khong."""
    t = text.strip()
    if not t:
        return False
    # So trang doc lap (1-3 chu so)
    if re.match(r'^\d{1,3}$', t):
        return True
    return False


def parse_raw_page(filepath):
    """
    Doc file raw text cua mot trang, tra ve danh sach block co toa do.
    
    Dinh dang file:
      === LEFT COLUMN ===
      [   y0,  x0] text
      === RIGHT COLUMN ===
      [   y0,  x0] text
    
    Tra ve: danh sach dict {text, y0, x0, column, page}
    """
    blocks = []
    if not os.path.exists(filepath):
        return blocks

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    current_column = None
    page_num = None

    # Lay so trang tu ten file
    basename = os.path.basename(filepath)
    m = re.search(r'page_(\d+)\.txt', basename)
    if m:
        page_num = int(m.group(1))

    for line in content.split('\n'):
        line = line.rstrip('\n')
        if line.strip() == '=== LEFT COLUMN ===':
            current_column = 'left'
            continue
        if line.strip() == '=== RIGHT COLUMN ===':
            current_column = 'right'
            continue
        if not line.strip():
            continue

        # Parse: [   y0,  x0] text
        m = re.match(r'\[\s*([\d.]+)\s*,\s*([\d.]+)\]\s(.*)', line)
        if m:
            y0 = float(m.group(1))
            x0 = float(m.group(2))
            text = m.group(3)
            blocks.append({
                "text": text,
                "y0": y0,
                "x0": x0,
                "column": current_column,
                "page": page_num,
            })

    return blocks


def classify_blocks(blocks):
    """
    Phan loai cac block vao: header (xoa), chapter_heading (giu), footnote (tach), body (giu), page_number (xoa).
    
    Footnote detection co 2 buoc:
    1. Nhan dang cac block dau tien cua footnote (y > ngưỡng hoac bat dau boi chu so + khoang trang)
    2. Trang lai: khi da vao che do footnote trong mot cot, tat ca cac block sau (cao hon) cung cot cung trang cung duoc dan la footnote.
    
    Tra ve: dict co 5 loai block.
    """
    classified = {
        "headers": [],
        "chapter_headings": [],
        "footnotes": [],
        "body": [],
        "page_numbers": [],
    }

    # Buoc 1: phan loai ban dau (footnote chi duoc luu tam vao preliminary, phan loai chinh xac o buoc 2)
    preliminary = []
    for b in blocks:
        text = b["text"].strip()
        y0 = b["y0"]

        if is_page_number(text):
            classified["page_numbers"].append(b)
        elif is_running_header(text, y0):
            classified["headers"].append(b)
        elif is_chapter_heading(text):
            classified["chapter_headings"].append(b)
        elif is_footnote(text, y0):
            # Chua them vao classified, se xu ly o buoc 2
            preliminary.append((b, "footnote"))
        else:
            preliminary.append((b, "body"))

    # Buoc 2: cascade footnote - khi da gap footnote, tat ca block sau cung cot/trang cung la footnote
    # Nhom theo (page, column), sap xep theo y0
    from collections import defaultdict
    groups = defaultdict(list)
    for b, label in preliminary:
        key = (b["page"], b["column"])
        groups[key].append((b, label))

    for key, items in groups.items():
        items.sort(key=lambda x: x[0]["y0"])
        in_footnote = False
        for b, label in items:
            if label == "footnote":
                in_footnote = True
                classified["footnotes"].append(b)
            elif in_footnote:
                # Block sau footnote cung cot cung trang cung duoc xem la footnote
                classified["footnotes"].append(b)
            else:
                classified["body"].append(b)

    return classified


def reconstruct_paragraphs(blocks_with_classification):
    """
    Xay dung doan van tu cac block da phan loai.

    QUY TAC NOI CHUNG:
    - Cung trang, cung cung, cung loai: noi neu khong ket thuc boi dau cau
    - Chapter heading: LUON bat dau doan moi, khong bao giờ noi voi body
    - Cheo trang (cung cot, cung loai): noi neu dau gach ngang + chu thuong
    - Doi cot (trai -> phai): bat dau doan moi
    - Running headers da bo loc truoc nen khong xuat hien o day.
    """
    if not blocks_with_classification:
        return []

    # Sap xep block: theo trang, cot (left truoc, right sau), y0
    def sort_key(b):
        page_order = b["page"] if b["page"] is not None else 9999
        col_order = 0 if b["column"] == "left" else 1
        return (page_order, col_order, b["y0"])

    sorted_blocks = sorted(blocks_with_classification, key=sort_key)

    paragraphs = []
    current_text = None
    current_page = None
    current_column = None
    current_type = None  # 'body' or 'footnote' or 'chapter_heading'

    for b in sorted_blocks:
        text = clean_text(b["text"])
        if not text:
            continue

        block_page = b["page"] if b["page"] is not None else 0
        block_column = b["column"] if b["column"] else "left"
        block_type = b.get("type", "body")

        # Chapter heading: LUON bat dau doan moi, khong noi voi gi ca
        if block_type == "chapter_heading":
            if current_text is not None:
                paragraphs.append({
                    "text": current_text,
                    "page": current_page,
                    "type": current_type,
                })
            current_text = text
            current_page = block_page
            current_column = block_column
            current_type = block_type
            continue

        # Footnote: noi chung nhu body nhung chi trong cung loai footnote
        if block_type == "footnote":
            if current_text is not None and current_type == "footnote":
                same_page = (block_page == current_page)
                same_column = (block_column == current_column)

                is_continuation = False
                if same_page and same_column:
                    if not ends_sentence(current_text):
                        is_continuation = True
                elif not same_page and same_column:
                    if ends_with_hyphen(current_text) and starts_with_lowercase(text):
                        is_continuation = True

                if is_continuation:
                    if ends_with_hyphen(current_text):
                        current_text = current_text.rstrip("-").rstrip() + " " + text.lstrip()
                    else:
                        current_text = current_text + " " + text.lstrip()
                    continue

            # Ket thuc doan truoc (neu co) va bat dau doan footnote moi
            if current_text is not None:
                paragraphs.append({
                    "text": current_text,
                    "page": current_page,
                    "type": current_type,
                })
            current_text = text
            current_page = block_page
            current_column = block_column
            current_type = block_type
            continue

        # block_type == 'body'
        if current_text is None:
            current_text = text
            current_page = block_page
            current_column = block_column
            current_type = block_type
            continue

        same_page = (block_page == current_page)
        same_column = (block_column == current_column)

        # Xet co phai tiep tuc doan hien tai khong
        is_continuation = False

        if same_page and same_column and current_type == "body":
            # Cung trang, cung cot, cung loai body: noi neu khong ket thuc boi dau cau
            if not ends_sentence(current_text):
                is_continuation = True
        elif not same_page and same_column and current_type == "body":
            # Cung cot, cheo trang: noi neu dau gach ngang + chu thuong
            if ends_with_hyphen(current_text) and starts_with_lowercase(text):
                is_continuation = True
        # Doi cot (trai -> phai) cung trang: luon bat dau doan moi

        if is_continuation:
            # Noi chung: bo dau gach ngang neu co
            if ends_with_hyphen(current_text):
                current_text = current_text.rstrip("-").rstrip() + " " + text.lstrip()
            else:
                current_text = current_text + " " + text.lstrip()
        else:
            paragraphs.append({
                "text": current_text,
                "page": current_page,
                "type": current_type,
            })
            current_text = text
            current_page = block_page
            current_column = block_column
            current_type = block_type

    # Them doan cuoi cung
    if current_text is not None:
        paragraphs.append({
            "text": current_text,
            "page": current_page,
            "type": current_type,
        })

    return paragraphs


def ends_with_hyphen(text):
    return text.rstrip().endswith("-") or text.rstrip().endswith("\u00ad")


def starts_with_lowercase(text):
    t = text.lstrip()
    return bool(t) and t[0].islower()


def ends_sentence(text):
    t = text.rstrip()
    if not t:
        return False
    # Khong xet la ket thuc cau neu ket thuc boi dau cham ba (ellipsis) . . .
    if re.search(r'\.\s*\.\s*\.?\s*$', t):
        return False
    return t[-1] in ".!?…\"'”’"


def merge_cross_page(paragraphs):
    """
    Gop doan van cheo trang: tim doan body cuoi cung cua trang N va doan body dau tien
    cua trang N+1. Neu doan cuoi khong ket thuc boi dau cau va doan dau bat dau boi
    chu thuong (hoac co dau gach ngang) => noi chung.
    
    Xuat hien footnote o giua khong chong gan gan noi chung.
    """
    from collections import defaultdict

    # Nhom doan theo trang
    pages = defaultdict(list)
    for p in paragraphs:
        pages[p["page"]].append(p)

    page_nums = sorted(pages.keys())

    # Danh dau cac doan da bi gom vao doan trang truoc (bo qua khi xay dung ket qua)
    merged_into_prev = set()

    result = []

    for i in range(len(page_nums)):
        curr_page = page_nums[i]
        curr_paras = pages[curr_page]

        # Tim doan body cuoi cung chua duoc gop
        last_body_idx = None
        for j in range(len(curr_paras) - 1, -1, -1):
            pj = curr_paras[j]
            if pj["type"] == "body" and id(pj) not in merged_into_prev:
                last_body_idx = j
                break

        # Neu co trang tiep theo, thu gop doan body cuoi trang nay voi doan body dau trang tiep
        if i + 1 < len(page_nums):
            next_page = page_nums[i + 1]
            next_paras = pages[next_page]

            # Tim doan body dau tien chua duoc gop
            first_body_idx = None
            for j in range(len(next_paras)):
                pj = next_paras[j]
                if pj["type"] == "body" and id(pj) not in merged_into_prev:
                    first_body_idx = j
                    break

            if last_body_idx is not None and first_body_idx is not None:
                last_body = curr_paras[last_body_idx]
                first_body = next_paras[first_body_idx]

                should_merge = False
                if ends_with_hyphen(last_body["text"]) and starts_with_lowercase(first_body["text"]):
                    should_merge = True
                elif not ends_sentence(last_body["text"]) and starts_with_lowercase(first_body["text"]):
                    should_merge = True

                if should_merge:
                    if ends_with_hyphen(last_body["text"]):
                        last_body["text"] = last_body["text"].rstrip("-").rstrip() + " " + first_body["text"].lstrip()
                    else:
                        last_body["text"] = last_body["text"].rstrip() + " " + first_body["text"].lstrip()
                    last_body["page"] = next_page
                    merged_into_prev.add(id(first_body))

        # Them cac doan cua trang nay vao ket qua (bo qua doan da duoc gop)
        for p in curr_paras:
            if id(p) not in merged_into_prev:
                result.append(p)

    return result


def assign_chapters(paragraphs):
    """
    Gan chuong cho moi doan dua tren so trang.
    """
    for p in paragraphs:
        page = p["page"] if p["page"] is not None else 0
        chapter = "front_matter"
        for cb in CHAPTER_BOUNDARIES:
            if page >= cb["page"]:
                chapter = cb["chapter"]
            else:
                break
        p["chapter"] = chapter
    return paragraphs


def generate_src_txt(chapter_name, paragraphs, start_page, end_page):
    """Tao noi dung Source TXT cho mot chuong."""
    lines = []
    title = chapter_name.replace("_", " ").title()
    lines.append(f"# {title}")
    lines.append(f"# Source structure rebuilt from original PDF (Meridian 1962)")
    lines.append(f"# Pages: {start_page}-{end_page}")
    lines.append("# Encoding: UTF-8, NFC, LF")
    lines.append("# Structure: CHAPTER → HEADING → SUBHEADING → PARAGRAPH → FOOTNOTE")
    lines.append("")

    para_counter = 0
    for p in paragraphs:
        text = p["text"].strip()
        if not text:
            continue
        para_counter += 1
        pid = f"V7-{chapter_name[:2].upper()}-P{para_counter:03d}"
        page = p["page"] if p["page"] is not None else 0
        ptype = p.get("type", "body")
        lines.append(f"[{pid}] (trang {page}) [{ptype}]")
        lines.append(text)
        lines.append("")

    content = "\n".join(lines)
    content = norm(content)
    return content


def build_manifest(all_paragraphs, missing_pages):
    """Xay dựng manifest xác minh liên tục cho mọi chuyển tiếp trang."""
    manifest = {
        "total_pages_in_pdf": 552,
        "pages_extracted": len([p for p in all_paragraphs if p["page"] is not None]),
        "missing_pages": missing_pages,
        "page_transitions": [],
    }

    # Lay danh sach trang co du lieu, sap xep
    pages_with_data = sorted(set(
        p["page"] for p in all_paragraphs if p["page"] is not None
    ))

    for i in range(len(pages_with_data) - 1):
        curr_page = pages_with_data[i]
        next_page = pages_with_data[i + 1]

        curr_paras = [p for p in all_paragraphs if p["page"] == curr_page]
        next_paras = [p for p in all_paragraphs if p["page"] == next_page]

        # Kiem tra xem co doan bi cat o cuoi trang curr khong
        last_body = None
        for p in reversed(curr_paras):
            if p.get("type") == "body":
                last_body = p
                break

        first_body = None
        for p in next_paras:
            if p.get("type") == "body":
                first_body = p
                break

        transition = {
            "from_page": curr_page,
            "to_page": next_page,
            "is_consecutive": (next_page == curr_page + 1),
            "last_body_ends_hyphen": bool(last_body and ends_with_hyphen(last_body["text"])),
            "last_body_no_sentence_end": bool(last_body and not ends_sentence(last_body["text"])),
            "first_body_starts_lowercase": bool(first_body and starts_with_lowercase(first_body["text"])),
            "merged": False,
        }

        if transition["is_consecutive"] and transition["first_body_starts_lowercase"]:
            if transition["last_body_ends_hyphen"] or transition["last_body_no_sentence_end"]:
                transition["merged"] = True

        manifest["page_transitions"].append(transition)

    return manifest


def main():
    doc = fitz.open(PDF_PATH)
    total_pages = doc.page_count
    print(f"PDF: {total_pages} pages")

    # Kiem tra cac trang thieu trong raw directory
    missing_pages = []
    for pnum in range(1, total_pages + 1):
        filepath = os.path.join(RAW_DIR, f"page_{pnum:03d}.txt")
        if not os.path.exists(filepath):
            missing_pages.append(pnum)
    print(f"Missing raw pages: {len(missing_pages)} -> {missing_pages[:20]}...")

    all_paragraphs = []
    pages_processed = 0

    for pnum in range(total_pages):
        page_num = pnum + 1
        filepath = os.path.join(RAW_DIR, f"page_{page_num:03d}.txt")

        if not os.path.exists(filepath):
            continue

        # BƯỚC 1: Doc raw page va phan loai block
        blocks = parse_raw_page(filepath)
        if not blocks:
            continue

        classified = classify_blocks(blocks)

        # Tao danh sach block kieu type de xu ly
        # RUNNING HEADERS DUOC BO LOC HOAN TOAN - khong xuat hien trong dau ra
        blocks_with_type = []
        for b in classified["chapter_headings"]:
            b2 = dict(b); b2["type"] = "chapter_heading"; blocks_with_type.append(b2)
        for b in classified["body"]:
            b2 = dict(b); b2["type"] = "body"; blocks_with_type.append(b2)
        for b in classified["footnotes"]:
            b2 = dict(b); b2["type"] = "footnote"; blocks_with_type.append(b2)
        # classified["headers"] va classified["page_numbers"] bo qua (da xoa)

        # BƯỚC 2: Phuc hoi doan van
        page_paragraphs = reconstruct_paragraphs(blocks_with_type)
        all_paragraphs.extend(page_paragraphs)
        pages_processed += 1

    print(f"Pages processed: {pages_processed}")
    print(f"Raw paragraphs: {len(all_paragraphs)}")

    # Gop doan cheo trang
    merged_paragraphs = merge_cross_page(all_paragraphs)
    print(f"After cross-page merge: {len(merged_paragraphs)} paragraphs")

    # Gan chuong
    merged_paragraphs = assign_chapters(merged_paragraphs)

    # Map ten chuong -> text heading tu boundaries (de them synthetic heading neu can)
    chapter_heading_text = {cb["chapter"]: cb["text"] for cb in CHAPTER_BOUNDARIES}

    # Xuat Source TXT cho tung chuong
    chapter_stats = {}
    for ch_name in CHAPTER_NAMES:
        ch_paras = [p for p in merged_paragraphs if p["chapter"] == ch_name]
        if not ch_paras:
            print(f"  {ch_name}: 0 paragraphs (skipped)")
            continue

        pages = [p["page"] for p in ch_paras if p["page"] is not None]
        start_page = min(pages) if pages else 0
        end_page = max(pages) if pages else 0

        # Neu doan dau tien khong phai chapter_heading, them synthetic heading
        # (bo qua front_matter vi khong co "CHAPTER" heading)
        output_paras = list(ch_paras)
        if ch_name != "front_matter" and output_paras and output_paras[0].get("type") != "chapter_heading":
            synthetic_heading = {
                "text": chapter_heading_text.get(ch_name, ch_name.replace("_", " ").title()),
                "page": start_page,
                "type": "chapter_heading",
            }
            output_paras.insert(0, synthetic_heading)
            print(f"  [SYNTHETIC] Added chapter heading for {ch_name} at page {start_page}")

        content = generate_src_txt(ch_name, output_paras, start_page, end_page)
        out_path = os.path.join(V7_DIR, f"v2_{ch_name}_src.txt")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

        n_body = len([p for p in output_paras if p.get("type") == "body"])
        n_fn = len([p for p in output_paras if p.get("type") == "footnote"])
        n_ch = len([p for p in output_paras if p.get("type") == "chapter_heading"])
        chapter_stats[ch_name] = {
            "paragraphs": len(output_paras),
            "body": n_body,
            "footnote": n_fn,
            "chapter_heading": n_ch,
            "start_page": start_page,
            "end_page": end_page,
        }
        print(f"  {ch_name}: {len(output_paras)} paragraphs (body:{n_body}, footnote:{n_fn}, heading:{n_ch}), pages {start_page}-{end_page}")

    # BƯỚC 5: Xuat manifest lien continuity
    manifest = build_manifest(all_paragraphs, missing_pages)
    manifest_path = os.path.join(V7_DIR, "manifest_continuity.json")
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nManifest saved to: {manifest_path}")

    # Xuat chapter boundaries
    cb_path = os.path.join(V7_DIR, "chapter_boundaries.json")
    with open(cb_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(CHAPTER_BOUNDARIES, f, ensure_ascii=False, indent=2)

    # Xuat thong ke chuong
    stats_path = os.path.join(V7_DIR, "chapter_stats.json")
    with open(stats_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(chapter_stats, f, ensure_ascii=False, indent=2)

    doc.close()
    print("\nDone!")


if __name__ == "__main__":
    main()