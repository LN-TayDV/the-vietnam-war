# -*- coding: utf-8 -*-
import win32com.client
from pathlib import Path
w = win32com.client.Dispatch("Word.Application")
w.Visible = False
f = sorted(Path("09_docx").glob("V1-C05*.docx"))[0]
try:
    d = w.Documents.Open(str(f), False, True)
    print("opened footnotes=" + str(d.Footnotes.Count))
    d.Close(0)
except Exception as e:
    print("open failed:", e)
w.Quit()