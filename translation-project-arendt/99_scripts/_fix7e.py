# -*- coding: utf-8 -*-
import io, re
p = r"04_translation\v2\ch07\v1_ch07_vi.txt"
s = io.open(p, encoding="utf-8").read()
# remove junk parenthesized-letter prefixes at start of footnote-content body paras
s = re.sub(r"\n\ affirmed", "\n", s)  # noop guard
s = re.sub(r"\n\u207d[\u1d43\u1d47\u02e2\u1d49\u02e3\u1d58\u1d57\u02b0\u2071\u02b2\u2093\u1d2c\u1d31\u1d3f\u1d40\u1d43\u02e0\u1d47\u1d48\u1d49\u1d56\u1d57\u02b3\u1d58\u1d5b\u02b0\u1d38\u1d39\u1d3a\u1d3b\u1d3c\u1d3d\u1d3e\u1d3f\u1d40\u1d41\u02bc\u02bb\u02bd\u02be\u02bf\u02ba\u02bb\u02bc\u02bd\u02be\u02bf\u02ba\u02bb\u02bc\u02bd\u02be\u02bf\u02ba\u02bb\u02bc\u02bd\u02be\u02bf\u02ba\u1d43\u1d47\u02e2\u1d49\u02e3\u1d58\u1d57\u02b0\u2071\u02b2\u2093\u1d2c\u1d31\u1d3f\u1d40\u1d43\u02e0\u1d47\u1d48\u1d49\u1d56\u1d57\u02b3\u1d58\u1d5b\u02b0\u1d38\u1d39\u1d3a\u1d3b\u1d3c\u1d3d\u1d3e\u1d3f\u1d40\u1d41]+\u207e\s*", "\n", s)
# simpler: strip the exact junk tokens used
for tok in ["\u207d\u1d43\u207e ", "\u207d\u1d47\u207e ", "\u207d\u02e2\u207e ", "\u207d\u1d49\u207e ", "\u207d\u02e3\u207e "]:
    s = s.replace(tok, "")
# English remnants
s = s.replace(" definitely ", " ch\u1eafc ch\u1eafn ")
s = s.replace(" \u0111\u00e3 steadily gi\u1ea3m s\u00fat", " \u0111\u00e3 \u0111\u1ec1u \u0111\u1ec1u gi\u1ea3m s\u00fat")
s = s.replace("steadily gi\u1ea3m s\u00fat", "\u0111\u1ec1u \u0111\u1ec1u gi\u1ea3m s\u00fat")
io.open(p,"w",encoding="utf-8",newline="\n").write(s)
print("definitely" in s, "steadily" in s)
import re as r2
print("junk paren remaining:", bool(r2.search(r"\u207d", s)))
