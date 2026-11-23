# -*- coding: utf-8 -*-
"""Dump DOCX paragraphs + footnote markers for Ch14 audit."""
import sys
from docx import Document
from docx.oxml.ns import qn

path = r"translation-project\09_docx\V1-C14_Ngo-Dinh-Diem-va-Su-Ra-Doi-cua-Cong-hoa-Viet-Nam.docx"
doc = Document(path)

out = []
out.append("=== PARAGRAPHS (%d) ===" % len(doc.paragraphs))
for i, p in enumerate(doc.paragraphs):
    txt = p.text
    style = p.style.name if p.style else "?"
    out.append("[P%03d][%s] %s" % (i, style, txt))

# footnotes via raw xml
try:
    fn_part = doc.part.part_related_by(
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes")
    from lxml import etree
    root = etree.fromstring(fn_part.blob)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    fns = root.findall('.//w:footnote', ns)
    out.append("\n=== FOOTNOTES (%d footnote elements incl separators) ===" % len(fns))
    for fn in fns:
        fid = fn.get(qn('w:id'))
        texts = fn.findall('.//w:t', ns)
        t = ''.join(x.text or '' for x in texts)
        out.append("[FN id=%s] %s" % (fid, t))
except Exception as e:
    out.append("FOOTNOTE EXTRACT ERROR: %r" % e)

with open("99_scripts/_ch14_docx_dump.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))
print("WROTE 99_scripts/_ch14_docx_dump.txt")
print("paragraphs:", len(doc.paragraphs))