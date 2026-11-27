# -*- coding: utf-8 -*-
import io
p = r"04_translation\v2\ch07\v1_ch07_vi.txt"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\u0111\u1ec3 l\u00e0i hardly m\u1ed9t d\u1ea5u v\u1ebft", "\u0111\u1ec3 l\u00e0i m\u1ed9t d\u1ea5u v\u1ebft")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("hardly" in s)
