# -*- coding: utf-8 -*-
import io
p = r"04_translation\v2\ch07\v1_ch07_vi.txt"
s = io.open(p, encoding="utf-8").read()
# Fix Chinese artifact + garbled "triun h" before "phuong tien"
import re
s = re.sub(r"vi\u1ec7c \u0111\u01b0a triun h[\u4e00-\u9fff]+ ph\u01b0\u01a1ng ti\u1ec7n", "vi\u1ec7c \u0111\u01b0a nh\u1ee1ng ph\u01b0\u01a1ng ti\u1ec7n", s)
# facilitating -> thuan tien cho
s = s.replace("m\u1ee5c \u0111\u00edch duy nh\u1ea5t l\u00e0 facilitating s\u1ef1 trao \u0111\u1ed5i", "m\u1ee5c \u0111\u00edch duy nh\u1ea5t l\u00e0 thu\u1eadn ti\u1ec7n cho s\u1ef1 trao \u0111\u1ed5i")
# "hardly mot dau vet" -> "mot dau vet"
s = s.replace("đ\u1ec3 l\u00e0i hardly m\u1ed9t d\u1ea5u v\u1ebft", "X")  # placeholder, will fix below
s = s.replace("đ\u1ec3 l\u00e0i X m\u1ed9t d\u1ea5u v\u1ebft", "\u0111\u1ec3 l\u00e0i m\u1ed9t d\u1ea5u v\u1ebft")
# "somehow ho da khong" -> "duong nhu ho da khong"
s = s.replace("th\u00ec somehow h\u1ecd \u0111\u00e3 kh\u00f4ng nh\u1eadn th\u1ee9c", "th\u00ec d\u01b0\u1eddng nh\u01b0 h\u1ecd \u0111\u00e3 kh\u00f4ng nh\u1eadn th\u1ee9c")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done")
