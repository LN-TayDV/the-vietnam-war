import sys
sys.path.insert(0, "translation-project/99_scripts")
from build_chapter_docx import parse_chapter
from pathlib import Path

ch_path = Path("translation-project/04_translation/v1/ch10/v1_ch10_vi.txt")
ch = parse_chapter(ch_path)

with open("debug_parse.txt", "w", encoding="utf-8") as f:
    for idx, it in enumerate(ch["items"]):
        kind = it.get("kind", "?")
        text = it.get("text", "")[:80]
        page = it.get("page", "?")
        f.write(f"{idx:3d} | {kind:10s} | p{page} | {text}\n")