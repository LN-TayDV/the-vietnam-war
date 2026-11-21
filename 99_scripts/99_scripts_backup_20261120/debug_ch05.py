# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_chapter_docx as b

ch = b.parse_chapter(Path("04_translation/v1/ch05/v1_ch05_vi.txt"))
items, placements, mode = b.plan_footnotes(ch)
out = []
out.append("mode=%s notes=%d keys=%s" % (mode, len(ch["notes"]), sorted(ch["notes"].keys())))
out.append("items=%d placements=%d" % (len(items), sum(len(v) for v in placements.values())))
for idx, it in enumerate(items):
    out.append("%d %s page=%s marks=%s %r" % (idx, it["kind"], it.get("page"), sorted(placements.get(idx, [])), it["text"][:70]))
Path("debug_out2.txt", encoding="utf-8").write_text("\n".join(out), encoding="utf-8")