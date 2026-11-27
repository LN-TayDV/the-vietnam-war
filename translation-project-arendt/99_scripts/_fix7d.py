# -*- coding: utf-8 -*-
import io, re
p = r"04_translation\v2\ch07\v1_ch07_vi.txt"
s = io.open(p, encoding="utf-8").read()
s = re.sub(r"l\u00e0 facilitating s\u1ef1", "l\u00e0 thu\u1eadn ti\u1ec7n cho s\u1ef1", s)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("facilitating" in s, "thu\u1eadn ti\u1ec7n cho" in s)
