import json
import re
import unicodedata
import os

V2 = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\02_extracted_text\v2"
JSON_ARCHIVE = V2 + r"\json_archive"

def ends_sentence(t):
    """Kiem tra xem co ket thuc boi dau cau khong."""
    t = t.rstrip()
    if not t:
        return False
    return t[-1] in ".!?…\u2019\u201d\""

def starts_capital(t):
    """Kiem tra xem co bat dau boi chu in hoa khong."""
    t = t.lstrip()
    return bool(t) and t[0].isupper()

def starts_lowercase(t):
    """Kiem tra xem co bat dau boi chu thuong khong."""
    t = t.lstrip()
    return bool(t) and t[0].islower()

def clean_text(t):
    t = t.replace("\u200b", "")
    t = re.sub(r'(\w)\u00ad\s+(\w)', r'\1\2', t)
    t = t.replace("\u00ad", "")
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def merge_paragraphs(paras):
    """
    Gop cac doan van lai theo logic:
    - Mot doan van hop le bat dau boi chu in hoa va ket thuc boi dau cau.
    - Neu doan hien tai KHONG ket thuc boi dau cau VA doan tiep theo bat dau boi chu thuong
      -> gop hai doan thanh mot (vi la mot cau bi cat ngang dong/trang).
    - Ap dung cung cung trang va ngang trang.
    """
    merged = []
    i = 0
    while i < len(paras):
        cur = dict(paras[i])
        cur["text"] = clean_text(cur["text"])
        j = i + 1
        while j < len(paras):
            nxt = paras[j]
            nxt_text = clean_text(nxt["text"])
            # Dieu kien gop: doan hien tai chua ket thuc cau VA doan tiep bat dau bang chu thuong
            if cur["text"] and not ends_sentence(cur["text"]):
                if nxt_text and starts_lowercase(nxt_text):
                    cur["text"] = cur["text"] + " " + nxt_text
                    j += 1
                    continue
            break
        merged.append(cur)
        i = j if j > i + 1 else i + 1
    return merged

def generate_txt(name, paras):
    lines = []
    title = name.replace("_", " ").title()
    lines.append(f"# {title}")
    lines.append("# Source structure rebuilt from original PDF")
    lines.append("# Encoding: UTF-8, NFC, LF")
    lines.append("")

    for p in paras:
        pid = p["para_id"]
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

chapter_map = {
    "front_matter": "front_matter_structure.json",
    "preface_first_edition": "preface_first_edition_structure.json",
    "preface_part_one": "preface_part_one_structure.json",
    "preface_part_two": "preface_part_two_structure.json",
    "preface_part_three": "preface_part_three_structure.json",
    "part_one_intro": "part_one_intro_structure.json",
    "ch01": "ch01_structure.json",
    "ch02": "ch02_structure.json",
    "ch03": "ch03_structure.json",
    "ch04": "ch04_structure.json",
    "ch05": "ch05_structure.json",
    "ch06": "ch06_structure.json",
    "ch07": "ch07_structure.json",
    "ch08": "ch08_structure.json",
    "ch09": "ch09_structure.json",
    "ch10": "ch10_structure.json",
    "ch11": "ch11_structure.json",
    "ch12": "ch12_structure.json",
    "ch13": "ch13_structure.json",
}

total_chars = 0
total_paras = 0

for name, json_file in chapter_map.items():
    json_path = os.path.join(JSON_ARCHIVE, json_file)
    if not os.path.exists(json_path):
        print(f"SKIP (no json): {name}")
        continue

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    paras = data.get("paragraphs", [])
    merged = merge_paragraphs(paras)
    content = generate_txt(name, merged)

    out_path = os.path.join(V2, f"v2_{name}_src.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    total_chars += len(content)
    total_paras += len(merged)
    print(f"OK: {name} -> {len(merged)} doan, {len(content):,} ky tu")

print()
print(f"Tong cong: {total_paras} doan, {total_chars:,} ky tu")
print(f"Json files luu tai: {JSON_ARCHIVE}")
print(f"Txt files tao tai: {V2}")
