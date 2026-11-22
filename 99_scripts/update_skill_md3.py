import re

with open(r'.kilo\skills\translation-workflow\SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace section 8A.4 - audit command
old_audit = """Sau khi build, CHẠY validator:
```bash
python translation-project/99_scripts/audit_docx_format.py NN
```"""

new_audit = """Sau khi build, CHẠY validator:
```bash
python 99_scripts/audit_docx_format.py NN
```"""

content = content.replace(old_audit, new_audit)

# Replace section 10 checklist - add chapter_workflow.py reference
old_checklist = """## 10. CHECKLIST BẮT BUỘC MỖI SESSION MỚI (MỞ RỘNG)

1. **Kiểm tra rác workspace** → xóa file lệch.
2. Đọc `progress.json` → chương tiếp theo.
3. Đọc `STYLE_GUIDE_PHAN_B.md` + `TRANSLATION_GRAMMAR_ENGINE.md`.
4. Đọc `MASTER_LEXICON.csv` + `AUDIT_REPORT_CH01-06.md`.
5. **Kích hoạt skills**: `historical-book-translation`, `contextual-translation`, `southern-vietnamese-editorial-style`.
6. **Áp dụng VLP-01**: nhận diện từ ngoại ngữ trong nguồn trước khi dịch (§9.1-9.2).
7. **Áp dụng quy tắc Hán Việt**: chuẩn hóa tên nhân vật Trung Quốc theo bảng Hán Việt đã thiết lập (xem §13), không giữ Pinyin hoặc phiên âm tiếng Anh nếu đã có tên Hán-Việt.
8. Dịch theo 8 bước (bao gồm kiểm tra cấp câu VLP-01 ở bước 5b).
9. Chạy `vnch_orthography.py` + **VLP-01 sentence-level check** (§9.3) + quét tên Pinyin còn sót (§13.4) → `document_comparator.py` → `quality_gate.py` → `build_chapter_docx.py`.
10. **Chạy `audit_docx_format.py NN`** (§8A.4) → PASS (exit 0). Nếu FAIL, sửa TXT (heading/quote/marker) rồi build lại.
11. Quality Gate 8 tiêu chí + **VLP-01 criterion 6b** + **Hán Việt name check** + **DOCX format audit** PASS → cập nhật `progress.json` HOAN_TAT.
12. **Dọn dẹp file tạm** (tmp_*, debug_*, *.bak, file DOCX cũ cùng chương có slug khác)."""

new_checklist = """## 10. CHECKLIST BẮT BUỘC MỖI SESSION MỚI (MỞ RỘNG)

1. **Kiểm tra rác workspace** → xóa file lệch.
2. Đọc `progress.json` → chương tiếp theo.
3. Đọc `STYLE_GUIDE_PHAN_B.md` + `TRANSLATION_GRAMMAR_ENGINE.md`.
4. Đọc `MASTER_LEXICON.csv` + `AUDIT_REPORT_CH01-06.md`.
5. **Kích hoạt skills**: `historical-book-translation`, `contextual-translation`, `southern-vietnamese-editorial-style`.
6. **Áp dụng VLP-01**: nhận diện từ ngoại ngữ trong nguồn trước khi dịch (§9.1-9.2).
7. **Áp dụng quy tắc Hán Việt**: chuẩn hóa tên nhân vật Trung Quốc theo bảng Hán Việt đã thiết lập (xem §13), không giữ Pinyin hoặc phiên âm tiếng Anh nếu đã có tên Hán-Việt.
8. Dịch theo 8 bước (bao gồm kiểm tra cấp câu VLP-01 ở bước 5b).
9. Chạy `vnch_orthography.py` + **VLP-01 sentence-level check** (§9.3) + quét tên Pinyin còn sót (§13.4) → `document_comparator.py` → `quality_gate.py` → `build_chapter_docx.py`.
10. **Chạy `audit_docx_format.py NN`** (§8A.4) → PASS (exit 0). Nếu FAIL, sửa TXT (heading/quote/marker) rồi build lại.
11. Quality Gate 8 tiêu chí + **VLP-01 criterion 6b** + **Hán Việt name check** + **DOCX format audit** PASS → cập nhật `progress.json` HOAN_TAT.
12. **Dọn dẹp file tạm** (tmp_*, debug_*, *.bak, file DOCX cũ cùng chương có slug khác).

**Workflow thống nhất (khuyên dùng):**
```bash
python 99_scripts/chapter_workflow.py NN --volume v1 --step all
```
Tự động chạy: extract → build → audit → compare → quality → orthography → encoding."""

content = content.replace(old_checklist, new_checklist)

# Also update section 8 - step 8 to reference build_chapter_docx.py directly
old_step8 = """### BƯỚC 8: XUẤT DOCX + QUALITY GATE (8 TIÊU CHÍ)
1. `python -c "from docx_builder import DocxBuilder; from pathlib import Path; b=DocxBuilder(Path('.')); r=b.build_chapter(Path('translation-project/04_translation/v1/chNN/v1_chNN_vi.txt'), Path('translation-project/09_docx/V1-CNN_<slug>.docx')); print(r)"` → `OK N/N`.
2. **Kiểm tra hình ảnh trong DOCX**: Chạy `python translation-project/99_scripts/audit_docx_format.py NN` → phải PASS với `Images: N | Captions: N` (N = số ảnh trong image manifest). Mỗi caption phải đứng sau ảnh tương ứng (`every caption preceded by its image`, `image count == caption count`).
3. Word COM: `Footnotes.Count` = `notes` trong progress.json."""

new_step8 = """### BƯỚC 8: XUẤT DOCX + QUALITY GATE (8 TIÊU CHÍ)
1. `python 99_scripts/build_chapter_docx.py NN` → `OK N/N`.
2. **Kiểm tra hình ảnh trong DOCX**: Chạy `python 99_scripts/audit_docx_format.py NN` → phải PASS với `Images: N | Captions: N` (N = số ảnh trong image manifest). Mỗi caption phải đứng sau ảnh tương ứng (`every caption preceded by its image`, `image count == caption count`).
3. Word COM: `Footnotes.Count` = `notes` trong progress.json."""

content = content.replace(old_step8, new_step8)

# Update step 0 (extract_images.py path)
old_step0 = """6. **Kiểm tra hình ảnh trước khi dịch**: Chạy `99_scripts/extract_images.py --chapter XX --volume v1` để kiểm kê ảnh của chương. Nếu có ảnh chưa trích xuất → trích xuất trước khi tiếp tục. Nếu không thể trích xuất → ghi nhận lỗi vào `00_plan/image_manifest.json` và đánh trạng thái chương là BLOCKED."""

new_step0 = """6. **Kiểm tra hình ảnh trước khi dịch**: Chạy `python 99_scripts/extract_images.py --chapter XX --volume v1` để kiểm kê ảnh của chương. Nếu có ảnh chưa trích xuất → trích xuất trước khi tiếp tục. Nếu không thể trích xuất → ghi nhận lỗi vào `00_plan/image_manifest.json` và đánh trạng thái chương là BLOCKED."""

content = content.replace(old_step0, new_step0)

with open(r'.kilo\skills\translation-workflow\SKILL.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Done checklist updates")