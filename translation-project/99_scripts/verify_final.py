# -*- coding: utf-8 -*-
"""Final per-chapter verification report for chapters 1-6 (clean)."""
import re, sys, zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "99_scripts"))
import build_chapter_docx as bd

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "09_docx"

def footnote_texts(z):
    try:
        fn = z.read("word/footnotes.xml").decode("utf-8")
    except KeyError:
        return {}
    out = {}
    for fid, inner in re.findall(r'<w:footnote w:id="(\d+)"><w:p>(.*?)</w:p></w:footnote>', fn, re.DOTALL):
        t = re.sub(r"<[^>]+>", "", inner)
        t = re.sub(r"\s+", " ", t).strip()
        out[int(fid)] = t
    return out

report = []
for chap in ["01","02","03","04","05","06"]:
    src = bd.SRC_DIR / f"ch{chap}" / f"v1_ch{chap}_vi.txt"
    ch = bd.parse_chapter(src)
    out, words, used, mode, total = bd.build(src)
    z = zipfile.ZipFile(out)
    xml = z.read("word/document.xml").decode("utf-8")

    # images
    n_img_xml = xml.count("r:embed")
    img_dir = PROJECT / "04_translation" / "v1" / "images"
    n_img_src = len(list(img_dir.glob(f"ch{chap}_p*_img*.png")))
    # captions (true, anchored start)
    hinh_pat = re.compile(r"^\s*H\u00ecnh\s+\d+\.\d+")
    cap_texts = []
    for m in re.finditer(r'(<w:p[^>]*>.*?</w:p>)', xml, re.DOTALL):
        t = re.sub(r"<[^>]+>", "", m.group(1))
        t = re.sub(r"\s+", " ", t).strip()
        if hinh_pat.match(t):
            cap_texts.append(t)
    n_cap = len(cap_texts)
    # footnotes
    n_note_src = len(ch["notes"])
    fn_texts = footnote_texts(z)
    n_fn_docx = len(fn_texts)
    # mapping: every source note text present in some docx footnote
    mapping_ok = all(
        any(re.sub(r"\s+"," ",s).strip() in dt for dt in fn_texts.values())
        for s in ch["notes"].values()
    )
    # metadata
    has_src_meta = "02_extracted_text" in xml
    has_colophon = "*Bản dịch tiếng Việt ·" in xml
    # block leak
    n_leak = len(re.findall(r"--- \[[^\]]+\] \([^)]*\)(?: — [^—]*?)? ---", xml))
    # image-before-caption (for chapters with captions)
    img_before_cap = True
    if cap_texts:
        para_elems = re.findall(r'(<w:p[^>]*>.*?</w:p>)', xml, re.DOTALL)
        image_idx = {i for i, pe in enumerate(para_elems) if 'r:embed' in pe}
        cap_idx = []
        for i, pe in enumerate(para_elems):
            t = re.sub(r"<[^>]+>", "", pe)
            t = re.sub(r"\s+", " ", t).strip()
            if hinh_pat.match(t):
                cap_idx.append(i)
        img_before_cap = all((i-1) in image_idx for i in cap_idx)

    report.append(dict(chap=chap, out=out, words=words, n_img_src=n_img_src,
        n_img_xml=n_img_xml, n_cap=n_cap, cap_texts=cap_texts,
        n_note_src=n_note_src, n_fn_docx=n_fn_docx, mapping_ok=mapping_ok,
        has_src_meta=has_src_meta, has_colophon=has_colophon, n_leak=n_leak,
        img_before_cap=img_before_cap))

print("="*100)
print("BAO CAO KIEM TRA TUNG CHUONG (V1-C01 den V1-C06)")
print("="*100)
ok_all = True
for r in report:
    ok = (r['n_img_src']==r['n_img_xml'] and                    # tat ca anh duoc nhung
          r['n_note_src']==r['n_fn_docx'] and r['mapping_ok'] and
          not r['has_src_meta'] and not r['has_colophon'] and r['n_leak']==0 and
          (not r['cap_texts'] or (r['n_cap']==r['n_img_xml'] and r['img_before_cap'])))
    ok_all = ok_all and ok
    print(f"\n----- V1-C{r['chap']} -----")
    print(f"  DOCX: {r['out'].name}")
    print(f"  Tu: {r['words']:,}")
    print(f"  Hinh: src={r['n_img_src']} / docx={r['n_img_xml']} -> {'OK' if r['n_img_src']==r['n_img_xml'] else 'SAI'}")
    print(f"  Caption: {r['n_cap']} doan (khong ro rang ten file/ID) -> {'OK' if (not r['cap_texts'] or r['n_cap']==r['n_img_xml']) else 'SAI'}")
    for c in r['cap_texts']:
        print(f"      - {c[:110]}")
    if r['cap_texts']:
        print(f"  Anh truoc moi caption: {'OK' if r['img_before_cap'] else 'SAI'}")
    print(f"  Footnote: src(notes)={r['n_note_src']} / docx(native)={r['n_fn_docx']} -> {'OK' if r['n_note_src']==r['n_fn_docx'] else 'SAI'}")
    print(f"  Mapping noi dung footnote: {'OK' if r['mapping_ok'] else 'SAI'}")
    print(f"  Metadata dau chuong (02_extracted_text): {'CON LAI' if r['has_src_meta'] else 'DA BO'}")
    print(f"  Colophon cuoi chuong (*Ban dich tieng Viet): {'CON LAI' if r['has_colophon'] else 'DA BO'}")
    print(f"  Block header loi vao noi dung: {r['n_leak']} -> {'OK' if r['n_leak']==0 else 'SAI'}")
    print(f"  CHUONG {r['chap']}: {'PASS' if ok else 'FAIL'}")

print("\n" + "="*100)
print("TONG KET:", "TAT CA 6 CHUONG PASS" if ok_all else "CO CHUONG FAIL")
