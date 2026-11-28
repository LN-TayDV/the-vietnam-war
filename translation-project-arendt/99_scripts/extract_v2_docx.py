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
            # Get footnote text
            texts = []
            for t in fn.findall('.//w:t', ns):
                if t.text:
                    texts.append(t.text)
            fn_text = ''.join(texts).strip()
            # Remove the footnote reference number at start
            fn_text = re.sub(r'^\d+\s*', '', fn_text)
            fn_defs[int(fid)] = fn_text
    
    # Extract body paragraphs with inline footnote markers
    body_paras = []
    in_body = False
    para_buffer = []
    
    for p in root.findall('.//w:p', ns):
        # Get paragraph text with footnote markers
        runs = p.findall('.//w:r', ns)
        para_text = ""
        fn_markers = []
        
        for r in runs:
            # Check for footnote reference
            fn_ref = r.find('.//w:footnoteReference', ns)
            if fn_ref is not None:
                fid = fn_ref.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                if fid:
                    fn_markers.append(int(fid))
                    # Add superscript marker
                    para_text += to_sup(fid)
                continue
            
            # Regular text
            t = r.find('.//w:t', ns)
            if t is not None and t.text:
                para_text += t.text
        
        para_text = para_text.strip()
        if not para_text:
            continue
        
        # Detect chapter title block (first few paragraphs)
        if not in_body:
            if "CHƯƠNG" in para_text.upper() or "CHƯƠNG" in para_text:
                in_body = True
            elif "CHỦ NGHĨA" in para_text.upper() and len(para_text) < 100:
                in_body = True
            elif para_text.startswith("[V1C"):
                in_body = True
            else:
                continue
        
        if in_body:
            body_paras.append((para_text, fn_markers))
    
    # Now we need to reconstruct the source format
    # The format is: [V1CXX-P###] (trang N)\n<body text with superscript markers>
    # Then === FOOTNOTES ===\n¹ def\n² def...
    
    # For now, let's just output the extracted text for analysis
    return body_paras, fn_defs

def to_sup(num):
    SUP_MAP = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    return ''.join(SUP_MAP[d] for d in str(num))

# Test on ch01
docx_path = DOCX_DIR / "V2-01_Chu-Nghia-Chong-Do-Thai-Mot-Su-Lang-Ma-Doi-Voi-Le-Thuong.docx"
body_paras, fn_defs = extract_chapter(docx_path, 1)

print(f"Body paragraphs: {len(body_paras)}")
print(f"Footnote definitions: {len(fn_defs)}")
print("\nFirst 10 body paragraphs:")
for i, (text, markers) in enumerate(body_paras[:10]):
    print(f"  {i}: {text[:100]} {'[FNs:' + ','.join(map(str,markers)) + ']' if markers else ''}")

print("\nFootnote definitions:")
for fid, text in sorted(fn_defs.items())[:10]:
    print(f"  {fid}: {text[:100]}")

PYEOF