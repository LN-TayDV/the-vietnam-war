# -*- coding: utf-8 -*-
import win32com.client
from pathlib import Path
w = win32com.client.Dispatch("Word.Application")
w.Visible = False
f = sorted(Path("09_docx").glob("V1-C05*.docx"))[0]
print("path:", f.resolve())
d = w.Documents.Open(str(f.resolve()), False, True)
print("opened footnotes=" + str(d.Footnotes.Count))
print("last-page=" + str(d.Range(d.Content.End-1, d.Content.End-1).Information(3)))
d.Close(0)
w.Quit()