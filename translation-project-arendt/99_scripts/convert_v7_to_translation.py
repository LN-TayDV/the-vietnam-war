# -*- coding: utf-8 -*-
"""
convert_v7_to_translation.py — Chuyển đổi v7 Source TXT sang định dạng dịch thuật.

Đầu vào:  02_extracted_text/v7/v2_*_src.txt (v7 format: [V7-CH-PNNN] (trang Y) [type])
Đầu ra:   04_translation/v2/chXX/v1_chXX_src.txt  (source copy, định dạng build_chapter_docx.py)
          04_translation/v2/chXX/v1_chXX_vi.txt   (translation template, có === FOOTNOTES ===)

Quy tắc chuyển đổi:
- ID: V7-CH-PNNN → V1Cxx-PNNN  (ch01→V1C01, ..., ch13→V1C13, front_matter→V1C00)
- Footnote paragraphs tách ra thành block === FOOTNOTES ===, đánh số 1..N
- Dấu hiệu chú thích trênь:text (superscript ¹²³...) được thêm vào cuối đoạn body
  trước đoạn footnote tương ứng
- Mã hóa: UTF-8, NFC, LF
"""

import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
V7_DIR = os.path.join(BASE, "02_extracted_text", "v7")
TRANS_DIR = os.path.join(BASE, "04_translation", "v2")

# Map v7 chapter name → translation chapter prefix (V1Cxx)
CHAPTER_MAP = {
    "front_matter": "V1C00",
    "ch01": "V1C01",
    "ch02": "V1C02",
    "ch03": "V1C03",
    "ch04": "V1C04",
    "ch05": "V1C05",
    "ch06": "V1C06",
    "ch07": "V1C07",
    "ch08": "V1C08",
    "ch09": "V1C09",
    "ch10": "V1C10",
    "ch11": "V1C11",
    "ch12": "V1C12",
    "ch13": "V1C13",
}

# Superscript digits for footnote markers
SUP_DIGITS = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "¹⁰", "¹¹", "¹²", "¹³",
              "¹⁴", "¹⁵", "¹⁶", "¹⁷", "¹⁸", "¹⁹", "²⁰", "²¹", "²²", "²³", "²⁴", "²⁵",
              "²⁶", "²⁷", "²⁸", "²⁹", "³⁰", "³¹", "³²", "³³", "³⁴", "³⁵", "³⁶", "³⁷",
              "³⁸", "³⁹", "⁴⁰", "⁴¹", "⁴²", "⁴³", "⁴⁴", "⁴⁵", "⁴⁶", "⁴⁷", "⁴⁸", "⁴⁹",
              "⁵⁰", "⁵¹", "⁵²", "⁵³", "⁵⁴", "⁵⁵", "⁵⁶", "⁵⁷", "⁵⁸", "⁵⁹", "⁶⁰", "⁶¹",
              "⁶²", "⁶³", "⁶⁴", "⁶⁵", "⁶⁶", "⁶⁷", "⁶⁸", "⁶⁹", "⁷⁰", "⁷¹", "⁷²", "⁷³",
              "⁷⁴", "⁷⁵", "⁷⁶", "⁷⁷", "⁷⁸", "⁷⁹", "⁸⁰", "⁸¹", "⁸²", "⁸³", "⁸⁴", "⁸⁵",
              "⁸⁶", "⁸⁷", "⁸⁸", "⁸⁹", "⁹⁰", "⁹¹", "⁹²", "⁹³", "⁹⁴", "⁹⁵", "⁹⁶", "⁹⁷",
              "⁹⁸", "⁹⁹", "¹⁰⁰", "¹⁰¹", "¹⁰²", "¹⁰³", "¹⁰⁴", "¹⁰⁵", "¹⁰⁶", "¹⁰⁷",
              "¹⁰⁸", "¹⁰⁹", "¹¹⁰", "¹¹¹", "¹¹²", "¹¹³", "¹¹⁴", "¹¹⁵", "¹¹⁶", "¹¹⁷",
              "¹¹⁸", "¹¹⁹", "¹²⁰", "¹²¹", "¹²²", "¹²³", "¹²⁴", "¹²⁵", "¹²⁶", "¹²⁷",
              "¹²⁸", "¹²⁹", "¹³⁰", "¹³¹", "¹³²", "¹³³", "¹³⁴", "¹³⁵", "¹³⁶", "¹³⁷",
              "¹³⁸", "¹³⁹", "¹⁴⁰", "¹⁴¹", "¹⁴²", "¹⁴³", "¹⁴⁴", "¹⁴⁵", "¹⁴⁶", "¹⁴⁷",
              "¹⁴⁸", "¹⁴⁹", "¹⁵⁰", "¹⁵¹", "¹⁵²", "¹⁵³", "¹⁵⁴", "¹⁵⁵", "¹⁵⁶", "¹⁵⁷",
              "¹⁵⁸", "¹⁵⁹", "¹⁶⁰", "¹⁶¹", "¹⁶²", "¹⁶³", "¹⁶⁴", "¹⁶⁵", "¹⁶⁶", "¹⁶⁷",
              "¹⁶⁸", "¹⁶⁹", "¹⁷⁰", "¹⁷¹", "¹⁷²", "¹⁷³", "¹⁷⁴", "¹⁷⁵", "¹⁷⁶", "¹⁷⁷",
              "¹⁷⁸", "¹⁷⁹", "¹⁸⁰", "¹⁸¹", "¹⁸²", "¹⁸³", "¹⁸⁴", "¹⁸⁵", "¹⁸⁶", "¹⁸⁷",
              "¹⁸⁸", "¹⁸⁹", "¹⁹⁰", "¹⁹¹", "¹⁹²", "¹⁹³", "¹⁹⁴", "¹⁹⁵", "¹⁹⁶", "¹⁹⁷",
              "¹⁹⁸", "¹⁹⁹", "²⁰⁰"]


def parse_v7_source(filepath):
    """
    Đọc file v7 source TXT, trả về danh sách paragraph dict.
    
    Mỗi paragraph: {v7_id, page, type, text}
    """
    paragraphs = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    para_pattern = re.compile(
        r"^\[V7-[A-Z]{2}-P\d{3}\]\s\(trang \d+\)\s\[(body|footnote|chapter_heading)\]$"
    )

    i = 0
    while i < len(lines):
        m = para_pattern.match(lines[i])
        if m:
            ptype = m.group(1)
            # Lấy văn bản (dòng sau header)
            text = ""
            if i + 1 < len(lines):
                text = lines[i + 1].strip()

            # Trích xuất ID, trang từ header
            id_match = re.match(
                r"^\[(V7-[A-Z]{2}-P\d{3})\]\s\(trang (\d+)\)\s\[.*\]$", lines[i]
            )
            if id_match:
                v7_id = id_match.group(1)
                page = int(id_match.group(2))
            else:
                v7_id = ""
                page = 0

            paragraphs.append({
                "v7_id": v7_id,
                "page": page,
                "type": ptype,
                "text": text,
            })
            i += 3  # Skip header, text, empty line
        else:
            i += 1

    return paragraphs


def convert_chapter(ch_name, v7_paras):
    """
    Chuyển đổi danh sách paragraph v7 sang định dạng dịch thuật.
    
    Trả về: (src_content, vi_content, footnote_count)
    """
    prefix = CHAPTER_MAP[ch_name]

    # Tách body/chapter_heading và footnote
    body_paras = [p for p in v7_paras if p["type"] in ("body", "chapter_heading")]
    footnote_paras = [p for p in v7_paras if p["type"] == "footnote"]

    # Xây dựng src content
    src_lines = []
    vi_lines = []

    # Header metadata
    v7_file = f"v2_{ch_name}_src.txt"
    pages = [p["page"] for p in v7_paras if p["page"] > 0]
    start_page = min(pages) if pages else 0
    end_page = max(pages) if pages else 0

    src_lines.append(f"# {ch_name}")
    src_lines.append(f"# Source structure rebuilt from original PDF (Meridian 1962)")
    src_lines.append(f"# Pages: {start_page}-{end_page}")
    src_lines.append(f"# Encoding: UTF-8, NFC, LF")
    src_lines.append(f"# Structure: CHAPTER → HEADING → SUBHEADING → PARAGRAPH → FOOTNOTE")
    src_lines.append("")

    vi_lines.append(f"# {ch_name}")
    vi_lines.append(f"# Translation target: Vietnamese (VNCH pre-1975 Southern)")
    vi_lines.append(f"# Source: {v7_file} (Meridian 1962)")
    vi_lines.append(f"# Pages: {start_page}-{end_page}")
    vi_lines.append(f"# Encoding: UTF-8, NFC, LF")
    vi_lines.append("")

    para_counter = 0
    footnote_counter = 0
    fn_texts = {}  # footnote number → text

    for idx, p in enumerate(v7_paras):
        if p["type"] == "footnote":
            continue  # Xử lý footnote sau

        # Body hoặc chapter_heading
        para_counter += 1
        # Map ID: V7-CH-PNNN → V1Cxx-PNNN
        nnn = p["v7_id"].split("-P")[1]
        new_id = f"{prefix}-P{nnn}"
        page = p["page"]
        text = p["text"]

        # Kiểm tra xem đoạn tiếp theo có phải footnote không
        has_followup_fn = False
        if idx + 1 < len(v7_paras) and v7_paras[idx + 1]["type"] == "footnote":
            has_followup_fn = True

        # Thêm dấu hiệu chú thích nếu có footnote sau
        if has_followup_fn:
            footnote_counter += 1
            fn_num = footnote_counter
            sup = SUP_DIGITS[fn_num - 1] if fn_num <= len(SUP_DIGITS) else f"[{fn_num}]"
            text_with_marker = text + sup
            fn_texts[fn_num] = v7_paras[idx + 1]["text"]
        else:
            text_with_marker = text

        # Src content
        src_lines.append(f"[{new_id}] (trang {page})")
        src_lines.append(text_with_marker)
        src_lines.append("")

        # Vi content (translation template - empty for now)
        vi_lines.append(f"[{new_id}] (trang {page})")
        vi_lines.append("")  # Translation to be filled in
        vi_lines.append("")

    # Thêm block footnotes
    if fn_texts:
        src_lines.append("=== FOOTNOTES ===")
        vi_lines.append("=== FOOTNOTES ===")
        for fn_num in sorted(fn_texts.keys()):
            sup = SUP_DIGITS[fn_num - 1] if fn_num <= len(SUP_DIGITS) else f"[{fn_num}]"
            src_lines.append(f"{sup}{fn_texts[fn_num]}")
            vi_lines.append(f"{sup}")  # Translation to be filled in

    return "\n".join(src_lines), "\n".join(vi_lines), footnote_counter


def main():
    # Tìm tất cả file v7 source
    v7_files = sorted([f for f in os.listdir(V7_DIR) if f.endswith("_src.txt")])

    stats = {}
    for v7_file in v7_files:
        # Trích xuất tên chương từ tên file: v2_ch01_src.txt → ch01
        m = re.match(r"v2_(.+)_src\.txt", v7_file)
        if not m:
            continue
        ch_name = m.group(1)

        if ch_name not in CHAPTER_MAP:
            print(f"  SKIP {ch_name}: not in CHAPTER_MAP")
            continue

        v7_path = os.path.join(V7_DIR, v7_file)
        v7_paras = parse_v7_source(v7_path)

        src_content, vi_content, fn_count = convert_chapter(ch_name, v7_paras)

        # Tạo thư mục đầu ra
        ch_dir = os.path.join(TRANS_DIR, ch_name)
        os.makedirs(ch_dir, exist_ok=True)

        # Ghi file src
        src_path = os.path.join(ch_dir, f"v1_{ch_name}_src.txt")
        with open(src_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(src_content)

        # Ghi file vi (template)
        vi_path = os.path.join(ch_dir, f"v1_{ch_name}_vi.txt")
        with open(vi_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(vi_content)

        n_body = len([p for p in v7_paras if p["type"] in ("body", "chapter_heading")])
        n_fn = len([p for p in v7_paras if p["type"] == "footnote"])
        stats[ch_name] = {
            "body": n_body,
            "footnote": n_fn,
            "mapped_fn": fn_count,
            "pages": f"{min(p['page'] for p in v7_paras if p['page'] > 0)}-{max(p['page'] for p in v7_paras if p['page'] > 0)}",
        }
        print(f"  {ch_name}: {n_body} body, {n_fn} footnotes ({fn_count} mapped), pages {stats[ch_name]['pages']}")

    print(f"\nTotal chapters converted: {len(stats)}")


if __name__ == "__main__":
    main()
