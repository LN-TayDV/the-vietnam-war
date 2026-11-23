# -*- coding: utf-8 -*-
import re
from pathlib import Path

root = Path(r"C:\Users\PC\Documents\AI_project\the-vietnam-war")
src = (root/"translation-project/04_translation/v1/ch13/v1_ch13_src.txt").read_text(encoding="utf-8")
lines = src.split("\n")

fn_start = re.compile(r"^\s+\d+\t")
header_re = re.compile(r"^--- \[V1C13-P\d+\]")

out = []
in_fn = False
for ln in lines:
    if header_re.match(ln):
        in_fn = False
        out.append(ln)
        continue
    if fn_start.match(ln):
        in_fn = True
        continue
    if in_fn:
        # footnote continuation until blank line
        if ln.strip() == "":
            in_fn = False
            continue
        else:
            continue  # skip continuation
    # skip lone page-number lines (e.g., "13")
    if re.fullmatch(r"\s*\d{1,3}\s*", ln):
        continue
    out.append(ln)

clean = "\n".join(out)
# collapse multiple blank lines
clean = re.sub(r"\n{3,}", "\n\n", clean)
(root/"99_scripts/ch13_src_clean.txt").write_text(clean, encoding="utf-8")
print("written clean, lines:", len(clean.split(chr(10))))
print("chars:", len(clean))