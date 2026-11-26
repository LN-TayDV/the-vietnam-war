# -*- coding: utf-8 -*-
"""
Test hồi quy: running header dán liền body (trường hợp trang 99–100, chương 3).

Chạy:  python 99_scripts/test_header_strip.py
Yêu cầu: 100% PASS. Không sửa file gốc.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # translation-project-arendt
sys.path.insert(0, str(ROOT / "99_scripts"))
sys.stdout.reconfigure(encoding="utf-8")

from docx_builder_v2.parser import parse  # noqa: E402

V2 = ROOT / "04_translation" / "v2"

TITLE = "DÂN TỘC QUỐC GIA, SỰ RA ĐỜI CHỦ NGHĨA PHÂN BIỆT CHỦNG TỘC DO THÁI"

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))


def body_texts(model):
    return [n.text for n in model.nodes if n.type in ("body", "block_quote")]


def main():
    f = V2 / "ch03" / "v1_ch03_vi.txt"
    text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
    model = parse(text, chapter_label="Chương Ba", vi_title="Dân Tộc Do Thái và Xã Hội")

    bodies = body_texts(model)
    joined = "\n".join(bodies)

    # 1) Running header KHÔNG được xuất hiện trong body.
    check("Không còn tiêu đề chương trong body", TITLE not in joined,
          "TITLE vẫn còn trong body")
    # 1b) OCR variant BIỂT cũng không còn.
    check("Không còn biến thể OCR 'BIỂT CHỦNG TỘC' trong body",
          "BIỂT CHỦNG TỘC" not in joined)

    # 2) Trang 99: body bắt đầu bằng 'Niềm tin mê tín' (không phải tiêu đề).
    p99 = [b for b in bodies if b.startswith("Niềm tin mê tín")]
    check("Trang 99 body bắt đầu 'Niềm tin mê tín'", len(p99) >= 1,
          "không tìm thấy body bắt đầu 'Niềm tin mê tín'")

    # 3) Trang 100: body bắt đầu bằng 'kém quan tâm' (nối tiếp, không lặp tiêu đề).
    p100 = [b for b in bodies if b.startswith("kém quan tâm")]
    check("Trang 100 body bắt đầu 'kém quan tâm'", len(p100) >= 1,
          "không tìm thấy body bắt đầu 'kém quan tâm'")

    # 4) Không có đoạn body nào bắt đầu bằng cụm caps dài (dấu hiệu header còn sót).
    import re
    leftover = [b for b in bodies if re.match(r"^[A-ZÀ-Ỹ]{2,}(\s+[A-ZÀ-Ỹ]{2,}){3,}\s", b)]
    check("Không còn body mở đầu bằng cụm ALL-CAPS dài", len(leftover) == 0,
          f"{len(leftover)} đoạn còn cụm caps: {leftover[:1]}")

    # 5) Footnote markers vẫn được bảo toàn (không mất nội dung).
    #    Trang 99 có ³ ² ¹; trang 100 có ⁷ ⁶ ⁵ ⁴.
    check("Footnote ³/²/¹ (trang 99) còn trong body",
          "³" in joined and "²" in joined and "¹" in joined)
    check("Footnote ⁷/⁶/⁵/⁴ (trang 100) còn trong body",
          all(m in joined for m in "⁷⁶⁵⁴"))

    # 6) Không mất chữ: body trang 99 phải chứa 'mê tín', 'huyết thống', 'Disraeli'.
    check("Nội dung trang 99 còn đủ (huyết thống/Disraeli)",
          "huyết thống" in joined and "Disraeli" in joined)
    # 7) Nội dung trang 100 còn đủ.
    check("Nội dung trang 100 còn đủ (hội bí mật/Rothschild)",
          "hội bí mật" in joined and "Rothschild" in joined)

    # 8) Header strip log phải ghi nhận việc cắt ở trang 99 và 100.
    log = model.metadata.get("header_strip_log", [])
    pages = {e["page"] for e in log}
    check("Log ghi nhận cắt header ở trang 99", 99 in pages, f"pages={sorted(pages)}")
    check("Log ghi nhận cắt header ở trang 100", 100 in pages, f"pages={sorted(pages)}")

    # 9) Số footnote không đổi (không mất định nghĩa).
    check("Số footnote định nghĩa > 0", len(model.footnotes) > 0,
          f"footnotes={len(model.footnotes)}")

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"\n{'='*60}\n{passed}/{total} PASS")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())