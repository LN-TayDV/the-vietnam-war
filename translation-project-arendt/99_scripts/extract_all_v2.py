# -*- coding: utf-8 -*-
"""
Extract Vietnamese text from V2 chapter DOCX preserving footnote markers.
Output format matches v2 source format with === FOOTNOTES === section.
"""
import zipfile
import xml.etree.ElementTree as ET
import re
from pathlib import Path

DOCX_DIR = Path("/workspaces/the-vietnam-war/translation-project-arendt/09_docx")
OUT_DIR = Path("/workspaces/the-vietnam-war/translation-project-arendt/04_translation/v2")

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"

SUP_MAP = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}

def to_sup(num):
    return ''.join(SUP_MAP[d] for d in str(num))

def extract_chapter(docx_path, chapter_num):
    with zipfile.ZipFile(docx_path, 'r') as z:
        content = z.read('word/document.xml').decode('utf-8')
        fn_content = z.read('word/footnotes.xml').decode('utf-8') if 'word/footnotes.xml' in z.namelist() else None
    
    root = ET.fromstring(content)
    
    # Extract footnote definitions from footnotes.xml
    fn_defs = {}
    if fn_content:
        fn_root = ET.fromstring(fn_content)
        for fn in fn_root.findall('.//w:footnote', ns):
            fid = fn.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
            if fid in ('-1', '0'):  # separator, continuation separator
                continue
            texts = []
            for t in fn.findall('.//w:t', ns):
                if t.text:
                    texts.append(t.text)
            fn_text = ''.join(texts).strip()
            fn_text = re.sub(r'^\d+\s*', '', fn_text)
            fn_defs[int(fid)] = fn_text
    
    # Extract body paragraphs with inline footnote markers
    body_paras = []
    in_body = False
    title_block_done = False
    
    for p in root.findall('.//w:p', ns):
        runs = p.findall('.//w:r', ns)
        para_text = ""
        fn_markers = []
        
        for r in runs:
            fn_ref = r.find('.//w:footnoteReference', ns)
            if fn_ref is not None:
                fid = fn_ref.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                if fid:
                    fn_markers.append(int(fid))
                    para_text += to_sup(fid)
                continue
            
            t = r.find('.//w:t', ns)
            if t is not None and t.text:
                para_text += t.text
        
        para_text = para_text.strip()
        if not para_text:
            continue
        
        # Detect start of body: after title block (THE ORIGINS..., CHƯƠNG..., title, author, rule)
        # The first real body paragraph is typically the chapter title line or first content paragraph
        if not in_body:
            # Skip title block elements
            if para_text in ("THE ORIGINS OF TOTALITARIANISM", "Hannah Arendt"):
                continue
            # Skip CHƯƠNG X lines (chapter number in Vietnamese words)
            if re.match(r'^CHƯƠNG\s+(MỘT|HAI|BA|BỐN|NĂM|SÁU|BẢY|TÁM|CHÍN|MƯỜI|MƯỜI\s+MỘT|MƯỜI\s+HAI|MƯỜI\s+BA)$', para_text, re.IGNORECASE):
                continue
            # Skip Vietnamese chapter title (short, no colon)
            if re.match(r'^[A-ZÀÁẢÃẠĂẰẲẴẶÂẦẨẪẬĐÈÉẺẼẸÊỀỂỄỆÌÍỈỊỎÕỌÔỒỐỔỖỘƠỜỞỠỢỦỰŨỤÝỲỶỴỄ\s\.\-–—]{5,80}$', para_text) and ':' not in para_text and 'CHƯƠNG' not in para_text.upper():
                continue
            # Detect chapter title line with colon (e.g., "Chương Một: ..." or "CHƯƠNG MỘT: ...")
            if re.match(r'^CHƯƠNG\s+.+:.+', para_text, re.IGNORECASE):
                in_body = True
                continue
            # Detect first content paragraph (long text, not a title)
            if len(para_text) > 100 and not para_text.startswith("Chương") and "CHƯƠNG" not in para_text[:10]:
                in_body = True
            continue
        
        if in_body:
            body_paras.append((para_text, fn_markers))
    
    return body_paras, fn_defs

def write_source_file(chapter_num, body_paras, fn_defs, output_path):
    """Write v2 source format file."""
    lines = []
    
    # We need to assign paragraph IDs and page numbers
    # For now, use sequential numbering
    for i, (text, markers) in enumerate(body_paras):
        para_id = f"V1C{chapter_num:02d}-P{i+1:03d}"
        page_num = i + 1  # approximate
        lines.append(f"[{para_id}] (trang {page_num})")
        lines.append(text)
        lines.append("")  # blank line between paragraphs
    
    # Footnotes section
    lines.append("=== FOOTNOTES ===")
    lines.append("")
    for fid in sorted(fn_defs.keys()):
        sup = to_sup(fid)
        lines.append(f"{sup} {fn_defs[fid]}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Written: {output_path} ({len(body_paras)} paras, {len(fn_defs)} footnotes)")

# Process all chapters
CHAPTER_FILES = {
    1: "V2-01_Chu-Nghia-Chong-Do-Thai-Mot-Su-Lang-Ma-Doi-Voi-Le-Thuong.docx",
    2: "V2-02_Chu-Nghia-Phan-Biet-Chung-Toc-Truoc-Chu-Nghia-Quoc-Gia.docx",
    3: "V2-03_Nguoi-Do-Thai-Va-Xa-Hoi.docx",
    4: "V2-04_Vu-Dreyfus.docx",
    5: "V2-05_Giai-Phong-Chanh-Tri-Cua-Giai-Cap-Thi-Dan.docx",
    6: "V2-06_Tu-Duy-Chung-Toc-Truoc-Chu-Nghia-Phan-Biet-Chung-Toc.docx",
    7: "V2-07_Chung-Toc-va-Quan-Lieu.docx",
    8: "V2-08_Chu-Nghia-De-Quoc-Luc-Dia-Cac-Phong-Trao-Pan.docx",
    9: "V2-09_Su-Suy-Tan-Cua-Quoc-Gia-Quoc-Dan-va-Het-Han-Quyen-Con-Nguoi.docx",
    10: "V2-10_Xa-Hoi-Khong-Giai-Cap.docx",
    11: "V2-11_Phong-Trao-Toan-Tri.docx",
    12: "V2-12_Toan-Tri-Tai-Quyen.docx",
    13: "V2-13_Y-Thuc-He-va-Khung-Bo-Mot-Hinh-Thuc-Chanh-Phu-Moi.docx",
}

for ch_num, filename in CHAPTER_FILES.items():
    docx_path = DOCX_DIR / filename
    if not docx_path.exists():
        print(f"Missing: {filename}")
        continue
    
    body_paras, fn_defs = extract_chapter(docx_path, ch_num)
    out_path = OUT_DIR / f"ch{ch_num:02d}" / f"v1_ch{ch_num:02d}_vi.txt"
    write_source_file(ch_num, body_paras, fn_defs, out_path)

print("\nDone!")

PYEOF