# -*- coding: utf-8 -*-
"""
rebuild_paragraph_registry.py — Xây dựng lại Paragraph Registry từ PDF trực tiếp.

Quy tắc tuân thủ:
  1. Không chia một đoạn thành nhiều đoạn (gộp cross-page paragraphs).
  2. Không ghép các đoạn độc lập (mỗi paragraph là một block riêng).
  3. Xử lý chính xác câu tiếp nối qua trang, tiêu đề, trích dẫn, hình ảnh, chú thích.
  4. Mỗi footnote = một block duy nhất (không chia, không ghép).
  5. Mỗi block có ID (V1C15-PNNN) và vị trí trang (trang in).
  6. Chỉ tiếp tục dịch khi cấu trúc đoạn nguồn đã được xác minh chính xác.

Input : PDF nguồn (books/The_Cambridge_History_of_the_Vietnam_War.pdf)
Output: translation-project/04_translation/v1/ch15/v1_ch15_src_registry.txt

Usage:  python 99_scripts/rebuild_paragraph_registry.py <chap> [--volume v1]
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pymupdf

PDF_PATH = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\books\The_Cambridge_History_of_the_Vietnam_War.pdf'
ROOT = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project'

WATERMARK_RE = re.compile(r'https?://doi\.org/\S+.*$', re.IGNORECASE)
PAGE_NUM_RE = re.compile(r'^\s*(\d{1,4})\s*$')
FN_START_RE = re.compile(r'^(\d+)\s(.*)$', re.DOTALL)  # footnote: number + whitespace + text
SENTENCE_END = re.compile(r'[.!?…]["”’]?$')


def printed_label(page) -> int | None:
    for line in page.get_text("text").split("\n")[:4]:
        m = PAGE_NUM_RE.match(line)
        if m:
            return int(m.group(1))
    return None


def is_skip_block(text: str, y0: float, chap_title: str, author: str) -> bool:
    """Xác định block là header/footer/watermark/page-number (loại bỏ khỏi registry)."""
    t = text.strip()
    if not t:
        return True
    # Page number only
    if PAGE_NUM_RE.fullmatch(t):
        return True
    # Watermark
    if WATERMARK_RE.search(t):
        return True
    # Chapter title / author running header
    if chap_title and t == chap_title:
        return True
    if author and t == author:
        return True
    return False


def split_footnotes(text: str, first_num: int | None = None) -> list[tuple[int, str]]:
    """Tách một block chứa nhiều footnote thành danh sách (num, text).
    
    first_num: số footnote đầu tiên đã được tách khỏi text bởi FN_START_RE.
    Nếu text bắt đầu bằng nội dung của first_num (trước pattern \d+\t đầu tiên),
    nó sẽ được gán cho first_num.
    """
    results = []
    parts = re.split(r'(\d+\t)', text)
    current_num = first_num
    current_text = parts[0] if parts[0].strip() else ""
    for part in parts[1:]:
        m = re.match(r'^(\d+)\t$', part)
        if m:
            if current_num is not None:
                results.append((current_num, current_text.strip()))
            current_num = int(m.group(1))
            current_text = ""
        else:
            if current_num is not None:
                current_text += part
    if current_num is not None:
        results.append((current_num, current_text.strip()))
    return results


def looks_like_subheading(text: str, chap_title: str, author: str) -> bool:
    """Heuristic: dòng ngắn, không kết thúc bằng dấu câu, không phải title/author."""
    t = text.strip()
    if not t:
        return False
    if t == chap_title or t == author:
        return False
    if len(t) > 90:
        return False
    if SENTENCE_END.search(t):
        return False
    if re.fullmatch(r'\d+', t):
        return False
    return True


def is_figure_caption(text: str) -> bool:
    t = text.strip()
    return bool(re.match(r'^(Figure|Map|Table|Diagram|Chart|Hình|Bản đồ|Biểu đồ|Sơ đồ|Bảng)\s+\d+\.\d+', t, re.IGNORECASE))


def build_registry(chap: int, volume: str = "V1",
                   pdf_start: int | None = None,
                   pdf_end: int | None = None,
                   chap_title: str = "",
                   author: str = "") -> list[dict]:
    """Đọc PDF và xây dựng registry cho một chương."""
    doc = pymupdf.open(PDF_PATH)

    if pdf_start is None or pdf_end is None:
        manifest_path = Path(ROOT) / "00_plan" / "manifest.json"
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
        for ch in manifest.get("chapters", []):
            if ch["volume"] == volume.upper() and ch["chapter"] == chap:
                pdf_start = ch["pdf_start"]
                pdf_end = ch["pdf_end"]
                chap_title = chap_title or ch.get("title_en", "")
                author = author or ch.get("author", "")
                break

    if pdf_start is None or pdf_end is None:
        raise ValueError(f"Không tìm thấy dải trang cho {volume}-Ch{chap:02d} trong manifest.json")

    # Bước 1: Trích xuất tất cả block theo trang, giữ nguyên thứ tự y0
    raw_blocks = []  # list of dict
    for pdf_page in range(pdf_start, pdf_end + 1):
        page = doc[pdf_page - 1]
        printed = printed_label(page)
        blocks = page.get_text("blocks")
        blocks_sorted = sorted(blocks, key=lambda b: (b[1], b[0]))
        for b in blocks_sorted:
            x0, y0, x1, y1, text, bno, btype = b
            t = text.strip()
            if not t:
                continue
            raw_blocks.append({
                "pdf_page": pdf_page,
                "printed": printed,
                "y0": y0,
                "text": t,
            })

    doc.close()

    # Bước 2: Phân loại từng block
    # Loại bỏ skip blocks (header, footer, page number, watermark, title, author)
    # Phân loại remaining: footnote_start, body, subheading, caption
    classified = []
    i = 0
    while i < len(raw_blocks):
        rb = raw_blocks[i]
        t = rb["text"]
        y0 = rb["y0"]

        if is_skip_block(t, y0, chap_title, author):
            i += 1
            continue

        # Footnote start: bắt đầu bằng "num\s" và nằm ở vùng dưới trang (y0 > 350)
        # để tránh nhầm lẫn với chapter title (ví dụ: "15 Nation-Building..." ở y0=90)
        fnm = FN_START_RE.match(t)
        if fnm and y0 > 350:
            fn_num = int(fnm.group(1))
            fn_text = fnm.group(2).strip()
            # Thu thập continuation của footnote này: các block tiếp theo ở cùng
            # trang, y0 gần nhau (khoảng cách < 200 điểm), không phải skip block,
            # không phải footnote start mới, không phải caption/subheading.
            j = i + 1
            while j < len(raw_blocks):
                nxt = raw_blocks[j]
                if is_skip_block(nxt["text"], nxt["y0"], chap_title, author):
                    j += 1
                    continue
                if FN_START_RE.match(nxt["text"]):
                    break  # footnote mới bắt đầu
                if is_figure_caption(nxt["text"]):
                    break
                if looks_like_subheading(nxt["text"], chap_title, author):
                    break
                # Continuation nếu cùng trang và khoảng cách y0 hợp lý
                if nxt["pdf_page"] == rb["pdf_page"] and (nxt["y0"] - y0) < 200:
                    fn_text = fn_text + " " + nxt["text"].strip()
                    y0 = nxt["y0"]  # cập nhật y0 cho continuation kế tiếp
                    j += 1
                    continue
                break
            # TÁCH TỪNG FOOTNOTE RIÊNG: fn_text có thể chứa nhiều footnote
            # cách nhau bởi "\t" (ví dụ: "2	... 	3	... 	4	...")
            fns = split_footnotes(fn_text, first_num=fn_num)
            if not fns:
                # Chỉ có một footnote trong block này (fn_num đã tách khỏi fn_text)
                fns = [(fn_num, fn_text)]
            for f_num, f_text in fns:
                classified.append({
                    "kind": "footnote",
                    "pdf_page": rb["pdf_page"],
                    "printed": rb["printed"],
                    "text": f"{f_num}\t{f_text}",
                    "fn_num": f_num,
                })
            i = j
            continue

        # Figure caption
        if is_figure_caption(t):
            classified.append({
                "kind": "caption",
                "pdf_page": rb["pdf_page"],
                "printed": rb["printed"],
                "text": t,
            })
            i += 1
            continue

        # Subheading
        if looks_like_subheading(t, chap_title, author):
            classified.append({
                "kind": "subheading",
                "pdf_page": rb["pdf_page"],
                "printed": rb["printed"],
                "text": t,
            })
            i += 1
            continue

        # Body paragraph
        classified.append({
            "kind": "body",
            "pdf_page": rb["pdf_page"],
            "printed": rb["printed"],
            "text": t,
        })
        i += 1

    # Bước 3: Gộp cross-page body paragraphs
    # Chỉ gộp khi: block hiện tại là body, không kết thúc bằng dấu câu,
    #               block tiếp theo là body, bắt đầu bằng chữ thường,
    #               và không có block khác (footnote, caption, subheading) xen giữa.
    merged = []
    i = 0
    while i < len(classified):
        blk = classified[i]
        if blk["kind"] != "body":
            merged.append(blk)
            i += 1
            continue

        combined_text = blk["text"]
        combined_printed = blk["printed"]
        combined_pdf = blk["pdf_page"]
        j = i + 1
        while j < len(classified):
            nxt = classified[j]
            if nxt["kind"] != "body":
                break
            if not SENTENCE_END.search(combined_text):
                if nxt["text"] and nxt["text"][0].islower():
                    combined_text = combined_text + " " + nxt["text"]
                    combined_printed = nxt["printed"]
                    combined_pdf = nxt["pdf_page"]
                    j += 1
                    continue
            break

        merged.append({
            "kind": "body",
            "pdf_page": combined_pdf,
            "printed": combined_printed,
            "text": combined_text,
        })
        i = j

    # Bước 4: Tách multi-footnote block thành từng footnote riêng
    final = []
    for blk in merged:
        if blk["kind"] == "footnote":
            # Đã là single footnote
            final.append(blk)
        else:
            final.append(blk)

    # Bước 5: Gán ID tuần tự
    vol_prefix = "V1" if volume.lower() == "v1" else volume.upper()
    chap_id = f"{vol_prefix}-C{chap:02d}"
    for idx, blk in enumerate(final, start=1):
        blk["id"] = f"{chap_id}-P{idx:03d}"
        blk["chap_id"] = chap_id

    return final


def write_registry(registry: list[dict], out_path: Path,
                   chap_id: str, title: str, author: str,
                   pages_range: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append(f"===== {chap_id} · {title} · {author} =====")
    lines.append(f"Nguồn: PDF trực tiếp · {pages_range}")
    lines.append("")
    for blk in registry:
        bid = blk["id"]
        page = blk["printed"]
        kind = blk["kind"]
        text = blk["text"]

        if kind == "footnote":
            m = re.match(r'^(\d+)\s(.*)$', text, re.DOTALL)
            if m:
                label = f"cước chú {m.group(1)}"
                fn_text = m.group(2)
            else:
                label = "cước chú"
                fn_text = text
            lines.append(f"--- [{bid}] (trang {page}) — {label} ---")
            lines.append(fn_text)
        elif kind == "caption":
            lines.append(f"--- [{bid}] (trang {page}) — PIMG ---")
            lines.append(text)
        elif kind == "subheading":
            lines.append(f"--- [{bid}] (trang {page}) — đề mục ---")
            lines.append(text)
        else:
            lines.append(f"--- [{bid}] (trang {page}) — P ---")
            lines.append(text)
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Đã ghi {len(registry)} block vào {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Xây dựng lại Paragraph Registry từ PDF trực tiếp")
    parser.add_argument("chapter", type=int, help="Số chương (ví dụ: 15)")
    parser.add_argument("--volume", default="v1", help="Tập (mặc định: v1)")
    args = parser.parse_args()

    chap = args.chapter
    volume = args.volume

    manifest_path = Path(ROOT) / "00_plan" / "manifest.json"
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    chap_meta = None
    for ch in manifest.get("chapters", []):
        if ch["volume"] == volume.upper() and ch["chapter"] == chap:
            chap_meta = ch
            break

    if chap_meta is None:
        print(f"ERROR: Không tìm thấy {volume}-Ch{chap:02d} trong manifest.json")
        sys.exit(1)

    vol_prefix = "V1" if volume.lower() == "v1" else volume.upper()
    chap_id = f"{vol_prefix}-C{chap:02d}"
    title_en = chap_meta.get("title_en", "")
    title_vi = ""
    prog_path = Path(ROOT) / "00_plan" / "progress.json"
    if prog_path.exists():
        with open(prog_path, encoding="utf-8") as f:
            prog = json.load(f)
        ch_prog = prog.get("chapters", {}).get(chap_id, {})
        title_vi = ch_prog.get("title_vi", "")

    display_title = title_vi or title_en
    author = chap_meta.get("author", "")
    first_printed = chap_meta["pages"][0].get("printed", "?")
    last_printed = chap_meta["pages"][-1].get("printed", "?")
    pages_range = f"trang in {first_printed}-{last_printed}"

    registry = build_registry(
        chap=chap,
        volume=volume,
        pdf_start=chap_meta["pdf_start"],
        pdf_end=chap_meta["pdf_end"],
        chap_title=title_en,
        author=author,
    )

    kind_counts = Counter(b["kind"] for b in registry)
    print(f"\n=== Thống kê {chap_id} ===")
    print(f"Tổng block: {len(registry)}")
    for k, v in sorted(kind_counts.items()):
        print(f"  {k}: {v}")
    if registry:
        print(f"Trang in: {registry[0]['printed']} → {registry[-1]['printed']}")

    out_path = Path(ROOT) / "04_translation" / volume.lower() / f"ch{chap:02d}" / f"v1_ch{chap:02d}_src_registry.txt"
    write_registry(registry, out_path, chap_id, display_title, author, pages_range)

    json_path = Path(ROOT) / "00_plan" / f"registry_ch{chap:02d}.json"
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "chap_id": chap_id,
            "title": display_title,
            "author": author,
            "pages_range": pages_range,
            "pdf_start": chap_meta["pdf_start"],
            "pdf_end": chap_meta["pdf_end"],
            "blocks": registry,
        }, f, ensure_ascii=False, indent=2)
    print(f"Đã ghi JSON metadata vào {json_path}")


if __name__ == "__main__":
    main()
