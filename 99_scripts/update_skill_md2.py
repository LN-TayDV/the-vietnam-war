import re

with open(r'.kilo\skills\translation-workflow\SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the PROJECT SCRIPTS table (section 7)
old_section7 = """| Script | Chức năng |
|---|---|
| `build_chapter_docx.py` | **Script chuẩn xuất DOCX** (bố cục sách + footnote chân trang). KHÔNG thay thế. |
| `extract_chapters.py` | One-time PDF → text extraction (pymupdf) |
| `extract_images.py` | **BẮT BUỘC**: trích xuất ảnh raster + **rasterize bản đồ/sơ đồ vector** (render_vector_figure, 300 DPI) từ PDF theo chapter, tạo image manifest. Chạy trước `build_chapter_docx.py`. |
| `build_volume_docx.py` | Legacy volume DOCX builder (backward compat) |
| `build_lexicon.py` | Lexicon management: `build`, `update`, `verify`, `stats` |
| `write_translation.py` | AI translation writer (79KB, specialized) |
| `build_corpus.py` | Corpus building for research |
| `audit_docx_format.py` | **Validator định dạng DOCX** (heading/body/quote/footnote/image). Chạy sau mỗi build. |
| `test_regression.py` | Regression test ch01-06 (metadata/image/footnote) |
| `verify_final.py` | Báo cáo kiểm tra từng chương ch01-06 |
| `analyze_docx.py` | Phân tích chi tiết từng đoạn DOCX (debug) |

*Script phụ trợ tại workspace `99_scripts/` (ngoài translation-project): `inspect_docx_ch09.py`, `check_italic.py`, `check_keepnext.py`, `check_bare_markers.py`, `debug_meta.py` — dùng để debug, không phải script build.*

*Đã xóa: 42 script cũ/debug/chapter-specific/tmp (xem consolidation report).*"""

new_section7 = """| Script | Chức năng |
|---|---|
| `chapter_workflow.py` | **Workflow chính** cho mọi chương: extract → build → audit → compare → quality. **Dùng cho mọi chương mới.** |
| `build_chapter_docx.py` | **Script chuẩn xuất DOCX** (bố cục sách + footnote chân trang). KHÔNG thay thế. |
| `extract_images.py` | **BẮT BUỘC**: trích xuất ảnh raster + **rasterize bản đồ/sơ đồ vector** (render_vector_figure, 300 DPI) từ PDF theo chapter, tạo image manifest. Chạy trước `build_chapter_docx.py`. |
| `audit_docx_format.py` | **Validator định dạng DOCX** (heading/body/quote/footnote/image). Chạy sau mỗi build. |
| `build_volume_docx.py` | Legacy volume DOCX builder (backward compat) |
| `build_lexicon.py` | Lexicon management: `build`, `update`, `verify`, `stats` |
| `extract_chapters.py` | One-time PDF → text extraction (pymupdf) |
| `test_regression.py` | Regression test ch01-06 (metadata/image/footnote) |
| `verify_final.py` | Báo cáo kiểm tra từng chương ch01-06 |

*Đã xóa: 100+ script cũ/debug/chapter-specific/tmp (xem consolidation report). Chỉ giữ 9 scripts cốt lõi.*"""

content = content.replace(old_section7, new_section7)

with open(r'.kilo\skills\translation-workflow\SKILL.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Done section 7")