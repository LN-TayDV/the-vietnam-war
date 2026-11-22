#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add V1-C10 extraction entry to progress.json (idempotent)."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

pj = Path("translation-project/00_plan/progress.json")
p = json.loads(pj.read_text(encoding="utf-8"))

entry = {
    "title_en": "The French Indochina War in Northern Vietnam",
    "title_vi": "Chiến tranh Đông Dương của Pháp ở Bắc Việt Nam",
    "author": "Christopher Goscha",
    "status": "EXTRACTION_COMPLETE — 20 trang PDF (218-237), 2 hình (Figure 10.1 raster p223 + Map 10.1 vector p229 rasterized); image_manifest.json; DOCX đã tạo có nhúng 2 hình (audit PASS). DỊCH: mới xong P001-P011 (trang 218-226); phần còn lại (P012+) CHƯA dịch.",
    "pages": "218-237",
    "pdf_pages": "234-253",
    "paragraphs": 11,
    "paragraphs_total_est": "N/A (dịch dở)",
    "footnotes": 0,
    "images": {
        "count": 2,
        "items": [
            {"id": "v1-C10-IMG001", "type": "raster", "pdf_page": 239, "printed_page": 223, "file": "ch10_p239_img0.png", "caption": "Hình 10.1 — Đại tướng Jean de Lattre de Tassigny"},
            {"id": "v1-C10-IMG002", "type": "vector_figure_rasterized", "pdf_page": 245, "printed_page": 229, "file": "ch10_p245_img1.png", "source_drawings": 113, "caption": "Bản đồ 10.1 — Các vùng chiến lược do DRVN quy định"}
        ]
    },
    "image_manifest": "00_plan/image_manifest.json (v1-C10-IMG001, v1-C10-IMG002, extraction_status=OK)",
    "g2_progress": "V1-C10: trích xuất raw text 20 trang (218-237) + 2 hình (Figure 10.1 p223 raster; Map 10.1 p229 vector→rasterized 113 drawings); image_manifest.json; 2 placeholder PIMG1/PIMG2 đặt vào v1_ch10_vi.txt; DOCX nhúng 2 hình. DỊCH: P001-P011 (218-226) đã dịch; P012+ CHƯA dịch.",
    "encoding": "UTF-8/NFC/no-BOM/LF",
    "docx": "09_docx/V1-C10_The-French-Indochina-War-in-Northern-Vietnam.docx",
    "docx_status": "DONE (2026-11-21; 3,475 từ; 0 cước chú vì dịch dở; 2 hình ảnh nhúng: image1.png=Figure 10.1 photo, image2.png=Map 10.1 rendered; audit_docx_format.py PASS — Images 2 | Captions 2, every caption preceded by image, image count == caption count; media integrity PASS — DOCX bytes == source PNG)",
    "format_audit": "PASS (2026-11-21): audit_docx_format.py ch10 — body 12pt Justify fi=0.9cm sa=6 line=1.3; image/caption count 2/2; every caption preceded by image; no block-header leaks; 0-note chapter handled gracefully (footnotes.xml absent + 0 refs = OK)",
    "pipeline_fix": "extract_images.py: thêm render_vector_figure() rasterize vector map/diagram (fixes Ch9 defect: Map 9.1 VECTOR_ONLY never embedded). build_chapter_docx.py + audit_docx_format.py: caption regex mở rộng Hình|Bản đồ|Biểu đồ|Sơ đồ|Bảng. audit footnotes.xml graceful khi 0 note.",
    "updated_note": "EXTRACTION_COMPLETE 2026-11-21: xác định PDF range 234-253 (printed 218-237, 20 trang); kiểm kê cấu trúc; trích raw text; trích 2 hình (Figure 10.1 raster + Map 10.1 vector rasterized); image_manifest.json; đặt PIMG1/PIMG2 vào vi.txt; build DOCX có 2 hình; audit PASS. Phát hiện & sửa lỗi workflow: vector map trước đây bị bỏ (VECTOR_ONLY) → nay rasterize. DỊCH CÒN DỞ (P012+).",
    "notes": "Task = DOCUMENT_EXTRACTION_COMPLETE. Text raw + 2 images + manifest + DOCX(image embed) + validation đều PASS. Translation chưa hoàn tất (mới P001-P011).",
}

p["chapters"]["V1-C10"] = entry
p["updated"] = "2026-11-21 (V1-C10 EXTRACTION_COMPLETE - 2 hinh figures/map, DOCX nhung hinh, sua workflow vector map)"

pj.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
print("progress.json updated with V1-C10 entry")
print("chapters now:", list(p["chapters"].keys()))