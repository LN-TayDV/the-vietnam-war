# -*- coding: utf-8 -*-
"""
Rebuild v2 ch04 Vietnamese file from the clean page-based v1 consolidated,
re-segmented to the 34 v2 source paragraph IDs ([V1C04-P001]..[V1C04-P034]).

- Source of truth for paragraph boundaries: 02_extracted_text/v2/ch04_src.txt
- Source of truth for clean VNCH translation + footnotes: 04_translation/v1/ch04/v1_ch04_vi.txt
- Output: 04_translation/v2/ch04/v1_ch04_vi.txt  (UTF-8, NFC, no BOM, LF)

Strategy: v1 is page-aligned; v2 paragraphs are essentially page-aligned
(34 paragraphs over pages 134-166). Each v2 paragraph is assigned the clean
body text of its page. Pages that host two v2 paragraphs (152 -> P019+P020,
160 -> P027+P028) get their footnote-continuation paragraph (P020/P028) filled
from the matching footnote definition. Running headers, page numbers, section
markers and footnote definitions are stripped from the body and the footnote
definitions are collected into a single === FOOTNOTES === block (kept 1..100).
"""
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "02_extracted_text" / "v2" / "ch04_src.txt"
V1 = ROOT / "04_translation" / "v1" / "ch04" / "v1_ch04_vi.txt"
OUT = ROOT / "04_translation" / "v2" / "ch04" / "v1_ch04_vi.txt"

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
RUNNING_HEADERS = {
    "CHỦ NGHĨA PHÂN BIỆT CHỦNG TỘC DO THÁI",
    "VỤ DREYFUS",
    "THE DREYFUS AFFAIR",
    "ANTISEMITISM",
}
SECTION_LABELS = {"I", "II", "III", "IV", "V", "VI"}
PART_TWO = {"PHẦN HAI", "Chủ nghĩa Đế quốc", "CECIL RHODES"}


def defnum(s: str):
    s = s.strip()
    if not s:
        return None
    if s[0] in SUP:
        n = ""
        for c in s:
            if c in SUP:
                n += SUP.index(c).__str__()
            else:
                break
        return int(n)
    m = re.match(r"^(\d{1,3})\.\s+\S", s)
    if m:
        return int(m.group(1))
    return None


def is_footnote_def(line: str) -> bool:
    return defnum(line) is not None


# Footnotes 35-39 were lost during the original v1 consolidation (pre-existing
# gap). Recovered from the English OCR (02_extracted_text/v1/ch04.txt, p.146)
# and translated to VNCH here.
RECOVERED_FOOTNOTES = {
    35: '³⁵ Vụ tai tiếng Panama đã được đi trước bởi cái gọi là "vụ Wilson." Con rể của Tổng thống đã bị phát hiện đang tiến hành một đường dây buôn bán công khai các danh dự và tước hiệu.',
    36: "³⁶ Xem Cha Edouard Lecanuet, Les Signes avant-coureurs de la séparation, 1894-1910, Paris, 1930.",
    37: "³⁷ Xem Bruno Weil, L'Affaire Dreyfus, Paris, 1930, tr. 169.",
    38: '³⁸ Cf. Clemenceau, "La Croisade," op. cit.: "Tây Ban Nha đang quằn quại dưới ách của Giáo hội Rô-ma. Nước Ý có vẻ đã khuất phục. Những xứ còn lại chỉ là nước Áo Công giáo, đã trong cơn giãy chết, và nước Pháp của Cách mạng, mà giờ đây các đạo binh giáo hoàng đang dàn trận chống lại."',
    39: '³⁹ Cf. Bernanos, op. cit., tr. 152: "Không thể nhấn mạnh đủ điều nầy: những kẻ hưởng lợi thật sự của phong trào phản động nối theo sau sự sụp đổ của đế chế và thất bại chính là hàng giáo sĩ. Nhờ họ mà chủ nghĩa phản động dân tộc đã khoác lấy, sau năm 1873, tính chất của một cuộc phục hưng tôn giáo."',
}


def is_running_header(line: str) -> bool:
    s = line.strip()
    return s in RUNNING_HEADERS


def is_page_number(line: str) -> bool:
    s = line.strip()
    return bool(re.fullmatch(r"\d{1,3}", s))


def is_section(line: str) -> bool:
    s = line.strip()
    return s in SECTION_LABELS or s in PART_TWO


def parse_source():
    text = SRC.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^\[(V1C04-P\d{3})\] \(trang (\d+)\)\s*$", text)
    paras = []
    i = 1
    while i < len(parts):
        pid = parts[i]
        page = parts[i + 1]
        body = parts[i + 2].strip()
        paras.append((pid, page, body))
        i += 3
    return paras


def parse_v1():
    """Return (pages, footnotes) where pages[page] = list of body lines (clean),
    footnotes = list of footnote definition strings in order 1..N.

    A line is a real footnote definition only when its number is >= the next
    expected number (forward jumps allowed to bridge the 35-39 gap); this keeps
    body paragraphs that merely begin with a superscript reference marker
    (e.g. page 152, 160) in the body instead of misclassifying them."""
    raw = V1.read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^=== PAGE (\d+) ===\s*$", raw)
    pages = {}
    footnotes = []  # (num, text)
    expect = 1
    i = 1
    while i < len(blocks):
        page = blocks[i]
        content = blocks[i + 1]
        body_lines = []
        for line in content.split("\n"):
            n = defnum(line)
            if n is not None and n >= expect:
                footnotes.append((n, line.strip()))
                expect = n + 1
                continue
            if is_running_header(line) or is_page_number(line) or is_section(line):
                continue
            if line.strip() == "":
                continue
            # Drop a line that is only a superscript/number marker with no text.
            stripped = line.strip()
            if re.fullmatch(r"[" + SUP + r"]+", stripped):
                continue
            body_lines.append(stripped)
        pages[page] = body_lines
        i += 2

    # Merge recovered 35-39 and sort by number, dedupe keeping first.
    by_num = {}
    for n, txt in footnotes:
        if n not in by_num:
            by_num[n] = txt
    for n, txt in RECOVERED_FOOTNOTES.items():
        by_num.setdefault(n, txt)
    ordered = [by_num[n] for n in sorted(by_num)]
    return pages, ordered


def main():
    src_paras = parse_source()
    pages, footnotes = parse_v1()

    # The v2 source merged source page 154 into P021 (no standalone paragraph
    # for p.154), so P021's body must combine v1 pages 153 + 154.
    page_group = {
        "V1C04-P021": ["153", "154"],
    }

    out_chunks = []
    for pid, page, _srcbody in src_paras:
        if pid in page_group:
            body = []
            for pg in page_group[pid]:
                body.extend(pages.get(pg, []))
        else:
            body = pages.get(page, [])
        # Special handling for split pages: P020 and P028 are footnote-continuation
        # paragraphs whose content lives in the footnote definitions.
        if pid == "V1C04-P020":
            body = ['(Đoạn nầy là phần tiếp nối cước chú 61 và 62, xem khối Cước chú ở cuối chương.)']
        elif pid == "V1C04-P028":
            body = ['(Đoạn nầy là phần tiếp nối cước chú 85 và 86, xem khối Cước chú ở cuối chương.)']
        text = " ".join(body).strip()
        text = re.sub(r"\s+", " ", text)
        out_chunks.append(f"[{pid}] (trang {page})\n{text}\n")

    fn_block = "=== FOOTNOTES ===\n" + "\n".join(footnotes)
    out = "\n".join(out_chunks) + "\n" + fn_block + "\n"

    # Insert inline markers that the v1 consolidation dropped (pre-existing gap).
    # Each entry: (paragraph_id, anchor_substring, marker) -> marker placed right
    # after the anchor substring within that paragraph.
    MARKER_INSERTIONS = [
        ("V1C04-P003", "tố cáo Pháp là dã man", "⁷"),
        ("V1C04-P003", "báo chí cấp tiến của thập niên 1930 mới sánh được", "⁸"),
        ("V1C04-P021", "như khi ông làm tròn bổn phận hằng ngày", "⁷⁰"),
    ]
    for pid, anchor, marker in MARKER_INSERTIONS:
        pat = re.compile(r"(\[" + re.escape(pid) + r"\] \(trang \d+\)\n)(.*?)(\n)", re.S)
        mm = pat.search(out)
        if not mm:
            continue
        seg = mm.group(2)
        if marker in seg:
            continue
        idx = seg.find(anchor)
        if idx < 0:
            continue
        pos = idx + len(anchor)
        seg = seg[:pos] + marker + seg[pos:]
        out = out[: mm.start(2)] + seg + out[mm.end(2):]

    out = unicodedata.normalize("NFC", out)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)

    # Report
    n_paras = len(src_paras)
    print(f"Wrote {OUT}")
    print(f"Paragraphs: {n_paras}")
    print(f"Footnotes: {len(footnotes)}")
    print(f"Bytes: {len(out.encode('utf-8'))}")


if __name__ == "__main__":
    main()