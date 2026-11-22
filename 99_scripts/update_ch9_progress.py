#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update V1-C09 progress entry: now 3 images (Map 9.1 added)."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

pj = Path("translation-project/00_plan/progress.json")
p = json.loads(pj.read_text(encoding="utf-8"))
c9 = p["chapters"]["V1-C09"]

c9["g2_progress"] = c9.get("g2_progress", "") + " | UPDATE 2026-11-21: Map 9.1 (p231/215, vector→rasterized 113 drawings) nay da trich xuat & nhung (ch09_p231_img2.png); DOCX co 3 hinh (Figure 9.1, 9.2, Map 9.1). Pipeline vector-figure fix ap dung chung cho ca ch9 & ch10."
c9["docx_status"] = "DONE (rebuilt 2026-11-21 with 3 IMAGES; 9,621 từ, 51/51 cước chú inline; HÌNH ẢNH: Figure 9.1 (p213/197), Figure 9.2 (p226/210), Map 9.1 (p231/215, vector rasterized 113 drawings); audit_docx_format.py PASS — Images 3 | Captions 3, every caption preceded by image)"
c9["format_audit"] = "PASS (2026-11-21): audit_docx_format.py ch09 — 3 hình ảnh nhúng (image1/2/3.png), every caption preceded by image, image count == caption count; footnotes 51/51; heading/quote/body OK"
c9["images_note"] = "3 images: v1-C09-IMG001 (Figure 9.1 raster), v1-C09-IMG002 (Figure 9.2 raster), v1-C09-IMG003 (Map 9.1 vector_figure_rasterized). Previously Map 9.1 was VECTOR_ONLY (never embedded) — fixed by extract_images.py render_vector_figure()."

p["updated"] = "2026-11-21 (V1-C09 them Map 9.1; V1-C10 EXTRACTION_COMPLETE 2 hinh; sua workflow vector map dung chung)"
pj.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
print("V1-C09 updated: 3 images (Map 9.1 added)")