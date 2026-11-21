# -*- coding: utf-8 -*-
import re
text = open("04_translation/v1/ch05/v1_ch05_vi.txt", encoding="utf-8").read()
for m in re.finditer(r"(?<=[^\s\d])(\d{1,3})(?=\s|$)", text):
    print(m.group(1), repr(text[max(0, m.start()-50):m.start()]))