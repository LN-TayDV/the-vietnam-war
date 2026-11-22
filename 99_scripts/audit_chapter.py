# -*- coding: utf-8 -*-
"""
audit_chapter.py — Cổng kiểm soát chất lượng (QA gate) bắt buộc trước khi build DOCX.

Tổng hợp các phép kiểm tra từng bị bỏ sót trong các chương trước, gói thành một
công cụ duy nhất để ngăn lỗi tái diễn:

  1. FOOTNOTE MARKERS   — đủ [N], không thiếu/trùng/thừa (giống check_footnote_markers.py)
  2. ENGLISH REMNANT    — câu/đoạn tiếng Anh còn sót trong THÂN BÀI (dịch chưa xong)
  3. FOOTNOTE LEAK      — trích dẫn cước chú (tên tác giả, "Ibid", "FRUS", số trang,
                          tên sách/báo) bị dịch/để lọt vào THÂN BÀI
  4. VNCH CALQUE        — lỗi dịch máy từng từ: "Việt Nam Nam", "Hàn Quốc Nam",
                          "Châu Á", "Châu Âu", "Chiến tranh thế giới thứ hai"...
  5. OMISSION (khối lượng) — so số từ thân bài VN với thân bài EN (đã bỏ cước chú);
                          cảnh báo nếu bản dịch ngắn bất thường (bỏ sót nội dung)

Nguyên tắc: cước chú / trích dẫn thư mục GIỮ NGUYÊN tiếng Anh trong khối
"--- [Cước chú ...] ---"; phần THÂN BÀI phải là tiếng Việt hoàn chỉnh.

Usage:
    python 99_scripts/audit_chapter.py 13
    python 99_scripts/audit_chapter.py 13 --json

Exit code: 0 = PASS, 1 = FAIL (có lỗi nghiêm trọng), 2 = WARN (chỉ cảnh báo).
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJECT = Path(__file__).resolve().parents[1]
TP = PROJECT / "translation-project"
SRC_DIR = TP / "04_translation" / "v1"
EN_DIR = TP / "02_extracted_text" / "v1"

NOTE_BLOCK_HEADER = re.compile(r"^--- \[Cước chú (.+?)\] ---\s*$")
NOTE_ENTRY = re.compile(r"^\[(\d{1,3})\]\s+(.+)$")
INLINE_MARKER = re.compile(r"\[(\d{1,3})\]")
SEG_HEADER = re.compile(r"^--- \[V\dC\d+-P\d+\]")

# --- (2) English function words: >=3 trong một câu latin dài => câu chưa dịch ---
EN_STOP = set(
    """the of and to in that it was for on with as by at from this be are is were an or
    its his their which had has have not but would could should can may might must do
    does did he she they we you i him them us our your my me who whom whose what when
    where why how all any some no more most other such than then there these those
    about into over under between during before after above below up down out off again
    further once here also because while if although though since until unless upon
    within without across against among around through toward towards per via""".split()
)

# --- (3) Footnote-citation leak markers (xuất hiện trong THÂN BÀI là đáng ngờ) ---
FN_LEAK = [
    "Ibid", "ibid", "FRUS", "Foreign Relations of the United States",
    "Public Papers", "interview with author", "Cong.", "sess.",
    "Washington, DC", "New York,", "Cambridge,", "Princeton,",
    " box ", "vol. ", "no. ", "pp.", "University Press",
    "National Security Council Minutes", "Department of State, Bulletin",
]

# --- (4) VNCH calque blacklist (lỗi dịch máy từng từ) ---
CALQUES = {
    "Việt Nam Nam": "Nam Việt Nam / miền Nam Việt Nam / Việt Nam Cộng Hòa",
    "Hàn Quốc Nam": "Nam Hàn / Hàn Quốc",
    "Châu Á": "Á Châu",
    "Châu Âu": "Âu Châu",
    "Chiến tranh thế giới thứ hai": "Thế Chiến thứ Hai / Thế chiến II",
    "Chiến tranh thế giới thứ nhất": "Thế Chiến thứ Nhất / Thế chiến I",
    "Cộng Hòa Dân Chủ Việt Nam": "Việt Nam Dân Chủ Cộng Hòa (DRVN)",
    "thế giới thứ ba": "Thế giới thứ ba",
}


def find_files(num: str):
    vi = SRC_DIR / f"ch{num}" / f"v1_ch{num}_vi.txt"
    if not vi.exists():
        for m in SRC_DIR.glob(f"ch*/v1_ch*_vi.txt"):
            if m.parent.name[-2:].zfill(2) == num.zfill(2):
                vi = m
                break
    en = EN_DIR / f"ch{num}.txt"
    return vi, en


def split_body_notes(text: str):
    """Trả về (body_text, notes_block_text)."""
    idx = text.find("--- [Cước chú")
    if idx == -1:
        return text, ""
    return text[:idx], text[idx:]


def strip_notes_from_text(text: str) -> str:
    body, _ = split_body_notes(text)
    return body


def parse_notes(notes_block: str) -> dict:
    notes = {}
    for line in notes_block.split("\n"):
        m = NOTE_ENTRY.match(line.strip())
        if m:
            notes.setdefault(int(m.group(1)), m.group(2).strip())
    return notes


def parse_body_markers(body: str) -> list:
    return [int(m.group(1)) for m in INLINE_MARKER.finditer(body)]


def clean_english_body(en_text: str) -> str:
    """Bỏ khối trích dẫn cước chú (dòng bắt đầu bằng space+số+TAB) khỏi nguồn EN."""
    out, in_fn = [], False
    for ln in en_text.split("\n"):
        if re.match(r"^\s+\d+\t", ln):
            in_fn = True
            continue
        if in_fn:
            if ln.strip() == "":
                in_fn = False
            continue
        if re.fullmatch(r"\s*\d{1,3}\s*", ln):
            continue
        out.append(ln)
    txt = "\n".join(out)
    # bỏ các segment header ---
    txt = re.sub(r"^--- \[.*?\](?: \([^)]*\))?(?: — .*?)? ---$", "", txt, flags=re.M)
    return txt


def count_words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def scan_english_remnant(body: str):
    """Trả về list (seg_label, snippet) các đoạn latin có >=3 stop-word EN."""
    hits = []
    # tách theo segment header để định vị
    parts = re.split(r"(--- \[V\dC\d+-P\d+\][^\n]*---)", body)
    i = 1
    while i < len(parts):
        header, content = parts[i], parts[i + 1] if i + 1 < len(parts) else ""
        num = re.search(r"P(\d+)", header)
        label = f"P{num.group(1)}" if num else "?"
        c = re.sub(r"\[\d+\]", "", content)
        # tìm các run latin >=6 từ
        for run in re.findall(
            r"[A-Za-z][A-Za-zÀ-ỹ'\-]*(?:\s+[A-Za-z][A-Za-zÀ-ỹ'\-]*){5,}", c
        ):
            toks = run.split()
            fn = sum(1 for t in toks if t.lower() in EN_STOP)
            if fn >= 3:
                hits.append((label, run[:120]))
        i += 2
    return hits


def scan_footnote_leak(body: str):
    hits = []
    for marker in FN_LEAK:
        if marker in body:
            idx = body.find(marker)
            hits.append((marker, body[max(0, idx - 40): idx + 60].replace("\n", " ")))
    return hits


def scan_calques(body: str):
    return [(c, body.count(c)) for c in CALQUES if c in body]


def main():
    ap = argparse.ArgumentParser(description="QA gate audit cho chương dịch")
    ap.add_argument("chapter", type=int)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    num = f"{args.chapter:02d}"

    vi_path, en_path = find_files(num)
    if not vi_path or not vi_path.exists():
        print(f"FAIL: không tìm thấy file bản dịch chương {num}")
        return 1

    text = vi_path.read_text(encoding="utf-8-sig")
    body, notes_block = split_body_notes(text)
    notes = parse_notes(notes_block)
    body_markers = parse_body_markers(body)

    errors, warns = [], []

    # 1. markers
    note_nums, body_nums = set(notes), set(body_markers)
    missing = sorted(note_nums - body_nums)
    dup = sorted(n for n in body_nums if body_markers.count(n) > 1)
    orphan = sorted(body_nums - note_nums)
    if missing:
        errors.append(f"FOOTNOTE MARKERS: thiếu {missing}")
    if dup:
        errors.append(f"FOOTNOTE MARKERS: trùng {dup}")
    if orphan:
        errors.append(f"FOOTNOTE MARKERS: thừa {orphan}")

    # 2. English remnant
    eng = scan_english_remnant(body)
    if eng:
        errors.append(f"ENGLISH REMNANT: {len(eng)} đoạn tiếng Anh trong thân bài")
    # 3. footnote leak
    leak = scan_footnote_leak(body)
    if leak:
        errors.append(f"FOOTNOTE LEAK: {len(leak)} dấu vết trích dẫn trong thân bài")
    # 4. calques
    cal = scan_calques(body)
    if cal:
        warns.append(f"VNCH CALQUE: {cal}")
    # 5. omission (word-count ratio)
    ratio_info = None
    if en_path and en_path.exists():
        en_body = clean_english_body(en_path.read_text(encoding="utf-8-sig"))
        en_w, vi_w = count_words(en_body), count_words(body)
        ratio = vi_w / max(en_w, 1)
        ratio_info = (en_w, vi_w, round(ratio, 2))
        # VN thường 1.0–1.6× EN; < 0.9 => nghi bỏ sót
        if ratio < 0.9:
            errors.append(
                f"OMISSION: thân bài VN ({vi_w} từ) chỉ bằng {ratio:.0%} "
                f"nguồn EN ({en_w} từ) — nghi bỏ sót nội dung"
            )

    result = {
        "chapter": f"V1-C{args.chapter:02d}",
        "vi_file": str(vi_path),
        "total_notes": len(notes),
        "total_body_markers": len(body_markers),
        "english_remnant_count": len(eng),
        "footnote_leak_count": len(leak),
        "calques": cal,
        "word_ratio": ratio_info,
        "errors": errors,
        "warnings": warns,
        "pass": len(errors) == 0,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== AUDIT CHAPTER {result['chapter']} ===")
        print(f"File: {vi_path}")
        print(f"Notes: {len(notes)} · body markers: {len(body_markers)}")
        if ratio_info:
            print(f"Từ (EN→VN): {ratio_info[0]} → {ratio_info[1]} (tỉ lệ {ratio_info[2]})")
        print()
        if eng:
            print(f"[ENGLISH REMNANT] {len(eng)} đoạn:")
            for lbl, sn in eng[:20]:
                print(f"  {lbl}: {sn}")
            print()
        if leak:
            print(f"[FOOTNOTE LEAK] {len(leak)} dấu vết:")
            for mk, sn in leak[:20]:
                print(f"  «{mk}» …{sn}…")
            print()
        if errors:
            print("ERRORS:")
            for e in errors:
                print("  -", e)
        if warns:
            print("WARNINGS:")
            for w in warns:
                print("  -", w)
        print()
        if result["pass"] and not warns:
            print("RESULT: PASS")
        elif result["pass"]:
            print("RESULT: PASS (có cảnh báo — nên rà lại)")
        else:
            print("RESULT: FAIL — khắc phục trước khi build DOCX.")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())