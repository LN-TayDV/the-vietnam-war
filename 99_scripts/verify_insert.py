# -*- coding: utf-8 -*-
"""Verify .new vs original:
   - notes block (from '--- [Cước chú') must be byte-identical
   - body (before notes): after stripping inserted [N] and undoing P014 fix,
     must equal the original body
"""
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

orig = Path(sys.argv[1]).read_text(encoding="utf-8-sig")
new = Path(sys.argv[2]).read_text(encoding="utf-8-sig")

MARK = "--- [Cước chú"
oi = orig.find(MARK)
ni = new.find(MARK)
assert oi != -1 and ni != -1, "notes block not found"

orig_body, orig_notes = orig[:oi], orig[oi:]
new_body, new_notes = new[:ni], new[ni:]

# 1) notes identical
if orig_notes == new_notes:
    print("OK: notes block is byte-identical.")
else:
    print("FAIL: notes block changed!")

# 2) body: strip [N] and undo P014 fix
nb = new_body.replace("[20][21]", "20 21")
nb = re.sub(r"\[(\d{1,3})\]", "", nb)
if orig_body == nb:
    print("OK: body differs ONLY by inserted [N] markers + P014 fix.")
else:
    print("FAIL: body has unexpected differences.")
    import difflib
    for line in difflib.unified_diff(orig_body.split("\n"), nb.split("\n"),
                                     "orig_body", "new_body_stripped", lineterm="", n=1):
        print(line)