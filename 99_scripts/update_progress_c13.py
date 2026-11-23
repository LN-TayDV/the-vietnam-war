# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path("translation-project/00_plan/progress.json")
d = json.loads(p.read_text(encoding="utf-8"))
c = d["chapters"]["V1-C13"]

c["paragraphs"] = "64 đoạn nội dung (P001-P064) + 8 đề mục Heading 2 (gồm Dẫn nhập), trang 282-301"
c["footnotes"] = "61 cước chú [1]-[61]"
c["status"] = (
    "HOAN_TAT — 64 đoạn nội dung (P001-P064) + Dẫn nhập, trang 282-301, "
    "61 cước chú [1]-[61]; DOCX đã tạo (9,290 từ, 61/61 cước chú, nguồn: inline); "
    "audit_chapter.py PASS (English remnant=0, footnote leak=0, VNCH calque=0, tỉ lệ từ VN/EN=1.43); "
    "đã sửa: bổ sung Dẫn nhập (trước P001), thêm câu Logic của chế độ kìm chặn [60], "
    "thêm câu Once France had acceded [61], xóa trích dẫn cước chú bị lọt vào thân bài (P039, P058), "
    "chuẩn hóa VNCH (Nam Việt Nam, Nam Hàn, Á Châu, Âu Châu); alignment 64/64; UTF-8/NFC/no-BOM/LF; "
    "DOCX: V1-C13_Eisenhower-and-Vietnam.docx (9,290 từ, 61/61 cước chú, 1 hình ảnh Figure 13.1)."
)
c["g2_progress"] = (
    "V1-C13: 64 đoạn nội dung + 8 đề mục (Dẫn nhập: Việt Nam – quân domino trong Chiến Tranh Lạnh; "
    "Chế độ kìm chặn: Điểm mù của chiến lược lớn; Di sản của chủ nghĩa thực dân và đế quốc; Hợp tác 1953–5; "
    "Chủ nghĩa đơn phương 1956–7; Tự hài lòng và tự mãn 1957–61; Kết luận: Cam kết mà thiếu sáng tạo) "
    "+ 1 hình ảnh (Figure 13.1) + 61 cước chú [1]-[61], trang 282-301 — HOÀN TAT (văn phong miền Nam VNCH, "
    "Style Guide v2.3 + Grammar Engine v2.1, audit_chapter.py PASS)."
)
d["updated"] = (
    "2026-11-22 (V1-C13 HOÀN TAT sau audit–sửa: 64 đoạn + 8 đề mục + 61 cước chú, DOCX 9,290 từ 61/61; "
    "audit_chapter.py PASS; V1-C12 HOAN_TAT: 42 đoạn + 5 đề mục + 76 cước chú, DOCX 9,748 từ 76/76)"
)

p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("updated progress.json")
print("status:", c["status"][:130])