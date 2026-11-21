# -*- coding: utf-8 -*-
"""
Inspect a chapter DOCX for formatting compliance (diagnostic only).
Reports page setup, per-paragraph formatting, run fonts, footnotes, images.

Usage: python inspect_docx.py <path-to-docx>
"""
import sys
import io
from docx import Document
from docx.shared import Pt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def fmt_run(r):
    sz = r.font.size.pt if r.font.size else None
    parts = []
    parts.append(f"sz={sz}" if sz else "sz=-")
    if r.font.bold:
        parts.append("B")
    if r.font.italic:
        parts.append("I")
    if r.font.superscript:
        parts.append("SUP")
    if r.font.name:
        parts.append(r.font.name)
    return ",".join(parts)


def main(path):
    doc = Document(path)

    # Page setup
    for si, sec in enumerate(doc.sections):
        print(f"[SECTION {si}] page={sec.page_width.cm:.1f}x{sec.page_height.cm:.1f}cm "
              f"margins T{sec.top_margin.cm:.2f} B{sec.bottom_margin.cm:.2f} "
              f"L{sec.left_margin.cm:.2f} R{sec.right_margin.cm:.2f} "
              f"start={sec.start_type}")

    # Footnotes (read via zip for reliability)
    import zipfile
    import re as _re
    fn_count = 0
    fn_texts = []
    with zipfile.ZipFile(path) as z:
        if 'word/footnotes.xml' in z.namelist():
            xml = z.read('word/footnotes.xml').decode('utf-8')
            ids = _re.findall(r'<w:footnote w:id="(\d+)"', xml)
            ids = [i for i in ids if int(i) > 0]
            fn_count = len(ids)
            # extract first 2 footnote texts
            fns = _re.findall(r'<w:footnote w:id="(\d+)"[^>]*>(.*?)</w:footnote>', xml, _re.S)
            for fid, body in fns[:2]:
                txt = ''.join(_re.findall(r'<w:t[^>]*>(.*?)</w:t>', body, _re.S))
                if txt.strip():
                    fn_texts.append((fid, txt[:50]))
    print(f"[FOOTNOTES] count={fn_count} (ids>0)")
    for fid, t in fn_texts:
        print(f"    FN#{fid}: {t}")

    # Images
    from docx.oxml.ns import qn
    imgs = doc.element.body.findall('.//' + qn('w:drawing'))
    print(f"[IMAGES] inline_drawings={len(imgs)}")

    # Paragraphs
    print(f"[PARAGRAPHS] total={len(doc.paragraphs)}")
    for i, p in enumerate(doc.paragraphs):
        pf = p.paragraph_format
        fi = pf.first_line_indent.cm if pf.first_line_indent else 0.0
        li = pf.left_indent.cm if pf.left_indent else 0.0
        sb = pf.space_before.pt if pf.space_before else 0.0
        sa = pf.space_after.pt if pf.space_after else 0.0
        ls = pf.line_spacing if pf.line_spacing else '-'
        align = str(pf.alignment).split('.')[-1].split(' ')[0] if pf.alignment else '-'
        style = p.style.name if p.style else '-'
        runs_info = "; ".join(fmt_run(r) for r in p.runs[:3])
        txt = p.text.strip().replace("\n", " ")
        # Mark short lines that look like headings (title case, no ending period, short)
        flag = ""
        if txt and len(txt) < 90 and not txt.endswith(('.', ',', ';', ':')) and p.style.name == 'Normal':
            flag = " <<< POSSIBLE HEADING (styled Normal)"
        # footnote ref ids in this paragraph
        refids = []
        for r in p.runs:
            for fr in r._r.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnoteReference'):
                refids.append(fr.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id'))
        fnmark = f" FNREFS={refids}" if refids else ""
        print(f"P{i:02d} [{style}] al={align} fi={fi:.2f} li={li:.2f} sb={sb:.0f} sa={sa:.0f} ls={ls} | runs[{runs_info}]{fnmark}")
        print(f"     TEXT: {txt[:95]}{flag}")


if __name__ == "__main__":
    main(sys.argv[1])