import os, re, json, unicodedata

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
V1 = os.path.join(BASE, "02_extracted_text", "v1")
V2 = os.path.join(BASE, "02_extracted_text", "v2")
os.makedirs(V2, exist_ok=True)

SUP_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
CHAPTERS = [
    ("front_matter", 1, 7), ("preface_first_edition", 8, 10), ("preface_part_one", 11, 16),
    ("preface_part_two", 17, 22), ("preface_part_three", 23, 41), ("part_one_intro", 42, 47),
    ("ch01", 48, 55), ("ch02", 56, 98), ("ch03", 99, 133), ("ch04", 134, 167),
    ("ch05", 168, 202), ("ch06", 203, 229), ("ch07", 230, 266), ("ch08", 267, 311),
    ("ch09", 312, 349), ("ch10", 350, 387), ("ch11", 388, 433), ("ch12", 434, 504),
    ("ch13", 505, 574),
]

def norm(s): return unicodedata.normalize("NFC", s)

def parse_pages(text):
    pages = []
    for m in re.finditer(r"=== PAGE (\d+) ===\n(.*?)(?=\n=== PAGE \d+ ===|\Z)", text, re.S):
        pages.append((int(m.group(1)), m.group(2)))
    return pages

def is_footnote_line(line):
    s = line.lstrip()
    if not s: return False
    if s[0] in SUP_DIGITS: return True
    if re.match(r"^\[\d+\]", s): return True
    return False

def split_paragraphs(body_text):
    paras = []
    cur = []
    for line in body_text.splitlines():
        if line.strip() == "":
            if cur:
                paras.append(" ".join(cur).strip())
                cur = []
        else:
            cur.append(line.strip())
    if cur:
        paras.append(" ".join(cur).strip())
    return [p for p in paras if p]

def ends_sentence(p):
    p = p.rstrip()
    if p.endswith("-") or p.endswith("­"): return False
    if p and p[-1] in ".!?…\"'”’": return True
    return False

report = {}
for name, start, end in CHAPTERS:
    path = os.path.join(V1, f"{name}.txt")
    with open(path, encoding="utf-8") as f:
        text = norm(f.read())
    pages = parse_pages(text)
    # collect body paragraphs per page + footnotes
    page_paras = []  # list of (page_num, [paras])
    footnotes = []   # list of (page_num, text)
    for pnum, ptext in pages:
        body_lines = []
        for line in ptext.splitlines():
            if is_footnote_line(line):
                footnotes.append((pnum, line.strip()))
            else:
                body_lines.append(line)
        body = "\n".join(body_lines)
        paras = split_paragraphs(body)
        page_paras.append((pnum, paras))

    # merge across pages
    merged = []  # list of (page_num, text)
    for pnum, paras in page_paras:
        for para in paras:
            if merged:
                prev_pnum, prev_text = merged[-1]
                merge = False
                if prev_text.endswith("-") or prev_text.endswith("­"):
                    merge = True
                elif para and para[0].islower():
                    merge = True
                if merge:
                    if prev_text.endswith("-") or prev_text.endswith("­"):
                        prev_text = prev_text.rstrip("-­").rstrip()
                    merged[-1] = (prev_pnum, (prev_text + " " + para).strip())
                    continue
            merged.append((pnum, para))

    # assign IDs
    prefix = name.upper().replace("CH", "C").replace("FRONT_MATTER","FM").replace("PREFACE_FIRST_EDITION","PFE").replace("PREFACE_PART_ONE","PPO").replace("PREFACE_PART_TWO","PPT").replace("PREFACE_PART_THREE","PPT3").replace("PART_ONE_INTRO","POI")
    # use plan's V1CNN style for chapters; for others keep name
    if name.startswith("ch"):
        num = name[2:].zfill(2)
        idprefix = f"V1C{num}"
    else:
        idprefix = name.upper().replace("_","")[:6]

    out_lines = []
    # heading
    out_lines.append(f"=== {name} ===")
    for i, (pnum, para) in enumerate(merged, 1):
        pid = f"{idprefix}-P{i:03d}"
        out_lines.append(f"[{pid}] (trang {pnum})")
        out_lines.append(para)
        out_lines.append("")

    out_lines.append("=== FOOTNOTES ===")
    for i, (pnum, fntext) in enumerate(footnotes, 1):
        fid = f"FN:{i}"
        out_lines.append(f"[{fid}] (trang {pnum}) {fntext}")

    outpath = os.path.join(V2, f"{name}_src.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    report[name] = {
        "paragraphs": len(merged),
        "footnotes": len(footnotes),
        "pages": len(pages),
    }
    print(f"{name}: {len(merged)} paras, {len(footnotes)} fns, {len(pages)} pages")

with open(os.path.join(V2, "reconstruction_report.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("Done")
