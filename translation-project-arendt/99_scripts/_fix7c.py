# -*- coding: utf-8 -*-
import io, re
p = r"04_translation\v2\ch07\v1_ch07_vi.txt"
s = io.open(p, encoding="utf-8").read()
s2 = re.sub(r"\s*hardly\s+", " ", s)
io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
print("hardly" in s2, "facilitating" in s2, "somehow" in s2)
print(any('\u4e00'<=c<='\u9fff' for c in s2))
