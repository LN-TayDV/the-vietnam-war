---
name: translation-workflow
description: Workflow chuẩn cho dự án dịch The Cambridge History of the Vietnam War sang tiếng Việt miền Nam (VNCH pre-1975). Bao gồm quy tắc VLP-01 (Tiếng Việt trước) bắt buộc áp dụng ngay từ câu đầu tiên. Capture toàn bộ quy trình, cấu trúc file, kiểm tra chất lượng, theo dõi tiến độ và xuất DOCX chuẩn (bố cục sách, footnote chân trang) sau mỗi chương. Dùng khi bắt đầu dịch chương mới, tiếp tục dự án dịch, hoặc xuất bản một chương đã dịch xong.
---

# Translation Workflow — The Cambridge History of the Vietnam War

## 1. Tổng quan dự án

- **Nguồn:** The Cambridge History of the Vietnam War (3 tập, 77 chương, ~698.500 từ), PDF 1866 trang.
- **Đích:** Tiếng Việt miền Nam theo chuẩn VNCH trước 1975.
- **Phiên bản dịch hiện hành:** G3 — viết lại tự nhiên, không cưỡng ép thuật ngữ VNCH vào nơi không cần thiết.
- **Thư mục dự án:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project`
- **Workspace (kilo):** `C:\Users\PC\Documents\AI_project\the-vietnam-war`

## 2. Cấu trúc thư mục

```
translation-project/
├── 00_plan/
│   ├── progress.json              # Checkpoint — trạng thái từng chương (ĐỌC TRƯỚC KHI BẮT ĐẦU)
│   ├── MASTER_PLAN.md            # Kế hoạch tổng 11 mục
│   └── chapter_inventory.csv     # Inventory 77 chương (volume, chapter, title, pages, words)
├── 02_extracted_text/
│   ├── v1/ch01.txt ... ch21.txt   # Text gốc trích từ PDF (V1, 21 chương)
│   ├── v2/ch01.txt ... ch30.txt   # Text gốc V2
│   └── v3/ch01.txt ... ch26.txt   # Text gốc V3
├── 02_extracted_text/v1/images/   # Ảnh raster trích từ PDF (chNN_pPPP_imgI.png)
│   ├── ch01_p33_img0.png
│   └── ch09_p213_img0.png, ch09_p226_img0.png (ví dụ Chương 9)
├── 03_terminology/
│   ├── glossary_nam_bac_compare.tsv  # Đánh dấu từ Bắc/Nam (KHÔNG tự ý kết luận nếu chưa có nguồn)
│   ├── SOURCES.md                 # Nguồn tham chiếu ngôn ngữ miền Nam (ưu tiên cao)
│   └── uncertain_terms.md         # Hàng đợi nghiên cứu (không tự ý chốt)
├── 04_translation/
│   └── v1/
│       ├── ch01/
│       │   ├── v1_ch01_src.txt   # Nguyên tác tiếng Anh (có sẵn)
│       │   └── v1_ch01_vi.txt    # Bản dịch tiếng Việt
│       ├── ch02/ ... ch21/       # Mỗi chương 1 cặp src + vi
├── 05_qa/
│   ├── FINAL_PILOT_QUALITY_GATE.md
│   ├── GIAO_DOAN_3_REPORT.md
│   ├── GIAO_DOAN_4_ACCEPTANCE.md
│   └── AUDIT_REPORT_CH01-06.md   # Báo cáo audit 6 chương đầu
├── 07_style_guide/
│   ├── STYLE_GUIDE.md            # v2.0, Phần B chuẩn miền Nam
│   ├── STYLE_GUIDE_PHAN_B.md     # v2.3, 29 quy tắc (đã phê duyệt — ĐỌC TRƯỚC KHI DỊCH)
│   └── TRANSLATION_GRAMMAR_ENGINE.md  # v2.1, 7 bước + 3 cấp kiểm soát + VNCH Grammar Database
├── 08_southern_vietnamese_library/
│   ├── 10_LEXICAL_DATABASE/MASTER_LEXICON.csv  # 321 mục, 16 cột (từ điển Nam)
│   ├── 08_SPECIALIZED_TERMINOLOGY/TERMINOLOGY_DATABASE.csv  # 25 mục
│   ├── 02_ORTHOGRAPHY/ORTHOGRAPHY_DATABASE.csv  # 20 quy tắc chính tả
│   ├── 12_SOURCE_REGISTRY/SOURCE_REGISTRY.csv  # 23 nguồn
│   └── 00_LIBRARY_MASTER_PLAN/library_progress.json
├── 09_docx/                       # DOCX xuất bản — do script sinh, KHÔNG sửa tay
│   └── V1-CNN_<slug>.docx         # 1 file / chương HOAN_TAT
└── 99_scripts/
    ├── extract_chapters.py
    ├── extract_images.py          # **BẮT BUỘC**: trích xuất ảnh raster từ PDF theo chapter
    ├── build_chapter_docx.py      # Script chuẩn xuất DOCX (bố cục sách + footnote chân trang)
    ├── apply_vnch_fixes.py        # Áp dụng quy tắc VNCH (30 quy tắc)
    ├── ch01_realign.py            # Căn lại đoạn chương 1
    ├── ch05_realign.py            # Căn lại đoạn chương 5
    ├── build_docx_final.py        # Script build DOCX cuối cùng
    ├── debug_align.py             # Kiểm tra alignment src vs vi
    └── check_encoding.py          # Kiểm tra encoding UTF-8/NFC/no BOM/LF
```

## 3. HỆ THỐNG SKILLS CHUYÊN BIỆT (`.kilo/skills/`)

Dự án hiện có **9 skills chuyên biệt** trong `.kilo/skills/`. Mỗi skill chịu trách nhiệm một khía cạnh cụ thể. Khi làm việc, hãy kích hoạt skill phù hợp.

| Skill | Mô tả | Khi nào kích hoạt |
|---|---|---|
| **translation-workflow** (này) | Workflow chính end-to-end | Bắt đầu session mới, dịch chương mới, xuất DOCX |
| **historical-book-translation** | Quy trình dịch sách lịch sử end-to-end | Dịch chương mới (bổ sung chi tiết cho workflow này) |
| **contextual-translation** | Phân tích ngữ cảnh, lập luận trước khi dịch | Mỗi câu/đoạn dịch (Grammar Engine Bước 1-3) |
| **southern-vietnamese-editorial-style** | Chuẩn hóa văn phong VNCH (29 quy tắc) | Mỗi câu dịch (Bước 5), chạy `apply_vnch_fixes.py`, review |
| **historical-terminology-research** | Nghiên cứu thuật ngữ lịch sử/chính trị/quân sự | Bước 4 (thuật ngữ), gặp từ/câu khó |
| **deep-translation-review** | Đối chiếu sâu cấp câu/đoạn/chương | Sau dịch xong chương, audit, re-review |
| **translation-error-detection** | Phát hiện lỗi E01-E16 (taxonomy) | Chạy scripts, deep review, audit |
| **translation-quality-gate** | Quality Gate 8 tiêu chí | Trước HOAN_TAT, sau build DOCX |
| **translation-error-kb** | Cơ sở tri thức lỗi thực tế (E01-E16) | Tra cứu lỗi đã gặp, phòng ngừa tái diễn |

**Quy tắc**: Luôn đọc skill `translation-workflow` trước, sau đó kích hoạt skill chuyên biệt theo nhu cầu.

## 4. TÀI LIỆU CỐT LÕI (ĐÃ SẴN SÀNG — KHÔNG CẦN ĐỌC LẠI TỪ ĐẦU)

| File | Dùng để | Lưu ý |
|---|---|---|
| `07_style_guide/STYLE_GUIDE_PHAN_B.md` | 29 quy tắc VNCH (v2.3) | **Bắt buộc đọc trước mỗi chương** |
| `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` | 7 bước dịch + VNCH Grammar Database + Checklist S1-S20, P1-P10, C1-C10 | **Bắt buộc đọc trước mỗi chương** |
| `03_terminology/glossary_nam_bac_compare.tsv` | Tra cứu từ Bắc/Nam | Nếu từ chưa có → ghi vào `uncertain_terms.md`, KHÔNG tự ý chốt |
| `03_terminology/SOURCES.md` | Nguồn ngôn ngữ miền Nam | Chỉ dùng để xác định từ, không đổi nội dung nguyên tác |
| `08_southern_vietnamese_library/10_LEXICAL_DATABASE/MASTER_LEXICON.csv` | 321+ mục từ điển Nam | Tra cứu nhanh thuật ngữ |
| `05_qa/AUDIT_REPORT_CH01-06.md` | Bài học từ 6 chương đầu | **Đọc trước khi dịch chương mới** |
| `books/doi-chieu-tieng-viet.pdf` | Bảng đối chiếu VNCH-VC (~120 cặp từ) | Tham chiếu khi chọn từ |
| `books/Tom_luoc_ngu_phap_va_hanh_van_Tieng_Viet_mien_Nam.md` | Ngữ pháp & hành văn miền Nam | Quy tắc câu, đoạn, văn phong |

## 5. HỆ THỐNG SKILLS CHUYÊN BIỆT (`.kilo/skills/`)

Dự án hiện có **10 skills chuyên biệt** trong `.kilo/skills/`. Mỗi skill chịu trách nhiệm một khía cạnh cụ thể. Khi làm việc, hãy kích hoạt skill phù hợp.

| Skill | Mô tả | Khi nào kích hoạt |
|---|---|---|
| **translation-workflow** (này) | Workflow chính end-to-end | Bắt đầu session mới, dịch chương mới, xuất DOCX |
| **historical-book-translation** | Quy trình dịch sách lịch sử end-to-end | Dịch chương mới (bổ sung chi tiết cho workflow này) |
| **contextual-translation** | Phân tích ngữ cảnh, lập luận trước khi dịch | Mỗi câu/đoạn dịch (Grammar Engine Bước 1-3) |
| **southern-vietnamese-editorial-style** | Chuẩn hóa văn phong VNCH (29 quy tắc + PDF) | Mỗi câu dịch (Bước 5), chạy `vnch_orthography.py`, review |
| **historical-terminology-research** | Nghiên cứu thuật ngữ lịch sử/chính trị/quân sự | Bước 4 (thuật ngữ), gặp từ/câu khó |
| **deep-translation-review** | Đối chiếu sâu cấp câu/đoạn/chương | Sau dịch xong chương, audit, re-review |
| **translation-error-detection** | Phát hiện lỗi E01-E16 (taxonomy) | Chạy scripts, deep review, audit |
| **translation-quality-gate** | Quality Gate 8 tiêu chí | Trước HOAN_TAT, sau build DOCX |
| **translation-error-kb** | Cơ sở tri thức lỗi thực tế (E01-E16) | Tra cứu lỗi đã gặp, phòng ngừa tái diễn |
| **skills-index** | Danh mục & ma trận kích hoạt | Xem trước khi bắt đầu session mới |

**Quy tắc**: Luôn đọc skill `translation-workflow` trước, sau đó kích hoạt skill chuyên biệt theo nhu cầu.

## 6. COMMON SCRIPTS (THƯ VIỆN DÙNG CHUNG) — `.kilo/scripts/common/`

**Một chức năng chỉ có một implementation.** Skills **phải gọi Common Scripts** thay vì tự triển khai logic.

| Script | Chức năng | Skills sử dụng |
|---|---|---|
| `file_integrity.py` | Kiểm tra cấu trúc 2 file/chương, encoding, tên file | Tất cả |
| `translation_validator.py` | Quét từ Anh còn sót, thuật ngữ không nhất quán, nội dung rỗng | `translation-error-detection`, `translation-quality-gate` |
| `document_comparator.py` | Đối chiếu src vs vi: số đoạn, số câu, cấu trúc, alignment | `deep-translation-review`, `translation-error-detection` |
| `quality_gate.py` | Chạy 8 tiêu chí Quality Gate, output JSON | `translation-quality-gate` |
| `vnch_orthography.py` | Kiểm tra 120+ quy tắc VNCH (Style Guide + PDF + Grammar Engine) | `southern-vietnamese-editorial-style`, `translation-error-detection` |
| `encoding_checker.py` | Kiểm tra UTF-8, NFC, no BOM, LF | `translation-quality-gate`, `translation-error-detection` |
| `docx_builder.py` | Build DOCX chapter/volume với real Word footnotes, A4 layout | `historical-book-translation`, `translation-quality-gate` |

### 6.1 Chạy Common Scripts
```bash
# Tất cả scripts đều có interface: --chapter NN [--volume v1] [--json]
# Exit code: 0=PASS, 1=FAIL

# Kiểm tra encoding
python .kilo/scripts/common/encoding_checker.py --chapter NN

# Kiểm tra orthography VNCH
python .kilo/scripts/common/vnch_orthography.py --chapter NN

# Đối chiếu alignment
python .kilo/scripts/common/document_comparator.py --chapter NN

# Quality Gate tổng hợp
python .kilo/scripts/common/quality_gate.py --chapter NN

# Build DOCX (Common)
python -c "from docx_builder import DocxBuilder; from pathlib import Path; b=DocxBuilder(Path('.')); r=b.build_chapter(Path('translation-project/04_translation/v1/chNN/v1_chNN_vi.txt'), Path('translation-project/09_docx/V1-CNN_<slug>.docx')); print(r)"
```

## 7. PROJECT SCRIPTS (translation-project/99_scripts/)
*Specialized scripts không dùng chung, chỉ cho tác vụ đặc thù:*

| Script | Chức năng |
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

*Đã xóa: 42 script cũ/debug/chapter-specific/tmp (xem consolidation report).*

## 7A. QUY TRÌNH XỬ LÝ HÌNH ẢNH (BẮT BUỘC — MỌI CHƯƠNG)

Trước khi trích xuất text từ PDF, phải kiểm tra và trích xuất hình ảnh theo pipeline thống nhất:

```
PDF SOURCE
→ PDF STRUCTURE INSPECTION
→ PAGE INVENTORY (kiếm kê hình theo trang)
→ TEXT EXTRACTION (extract_chapters.py)
→ IMAGE EXTRACTION (extract_images.py)
→ IMAGE MANIFEST (00_plan/image_manifest.json)
→ RAW TEXT WITH IMAGE REFERENCES (thêm paragraph "Hình X.Y" vào TXT)
→ DOCX GENERATION (build_chapter_docx.py)
→ DOCX IMAGE VALIDATION (audit_docx_format.py)
→ CHAPTER COMPLETENESS REPORT
```

### 7A.1 Quy định bắt buộc

1. **Trước khi trích xuất text** phải kiểm tra cấu trúc PDF (số trang, có ảnh hay không).
2. **Phải kiểm kê hình ảnh theo từng trang** của chương (raster images và vector drawings).
3. **Phải trích xuất hình ảnh độc lập** với text extraction, dùng script `99_scripts/extract_images.py` (workspace root).
4. **Phải lưu hình ảnh** vào thư mục `translation-project/0<vol>/v1/images/` với tên `ch<NN>_p<PDF_PAGE>_img<IDX>.png`.
5. **Phải tạo image manifest** tại `translation-project/00_plan/image_manifest.json` ghi nhận: image_id, source_pdf, volume, chapter, pdf_page, printed_page, filename, image_type, width, height, caption, extraction_status.
6. **Text raw phải giữ placeholder tham chiếu** đến hình ảnh tại đúng vị trí tương ứng (thêm block `--- [V1CXX-PIMGN] (trang Z) ---` với nội dung "Hình X.Y ..." vào file `_vi.txt`).
7. **DOCX phải nhúng hình ảnh** và caption theo đúng thứ tự trong tài liệu nguồn. Script `build_chapter_docx.py` tự động chèn ảnh trước paragraph bắt đầu bằng "Hình X.Y", "Bản đồ X.Y", "Biểu đồ X.Y", "Sơ đồ X.Y", hoặc "Bảng X.Y".
8. **Không được coi một chương đã extraction thành công** nếu hình ảnh chưa được kiểm tra.
9. **Không được tự ý bỏ qua** hình, biểu đồ, bản đồ hoặc sơ đồ. Nếu không thể trích xuất một hình, phải ghi nhận lỗi rõ ràng trong manifest thay vì âm thầm bỏ qua.
10. **Không được tự tạo hình ảnh thay thế** không có trong PDF nguồn.
11. **Bản đồ/sơ đồ dạng VECTOR (drawings) PHẢI được rasterize và nhúng**, không được ghi nhận `VECTOR_ONLY` rồi bỏ. Script `extract_images.py` (hàm `render_vector_figure()`) tự động phát hiện trang có ≥20 vector drawings + caption "Map/Figure/Bản đồ/..." và render thành 1 ảnh PNG (300 DPI, crop theo vùng hình + caption). Đây là bài học từ Chương 9: Map 9.1 (p231) trước đây bị bỏ vì chỉ ghi `VECTOR_ONLY_113_drawings` — nay đã sửa và áp dụng chung cho mọi chương.
12. **Trang có bản đồ vector thường có vài raster nhỏ** (la bàn, thước tỉ lệ) — KHÔNG trích xuất riêng chúng; bản đồ được render trọn vẹn thành một ảnh duy nhất.

## 8. QUY TRÌNH DỊCH MỘT CHƯƠNG (8 BƯỚC + QUALITY GATE)

### BƯỚC 0: KHỞI ĐỘNG SESSION MỚI (BẮT BUỘC)
1. Kiểm tra rác workspace (xóa file lệch thư mục).
2. Đọc `00_plan/progress.json` → xác định chương tiếp theo.
3. Đọc `STYLE_GUIDE_PHAN_B.md` + `TRANSLATION_GRAMMAR_ENGINE.md`.
4. Đọc `MASTER_LEXICON.csv` + `AUDIT_REPORT_CH01-06.md`.
5. **Kích hoạt skill**: `historical-book-translation` + `contextual-translation` + `southern-vietnamese-editorial-style`.
6. **Kiểm tra hình ảnh trước khi dịch**: Chạy `99_scripts/extract_images.py --chapter XX --volume v1` để kiểm kê ảnh của chương. Nếu có ảnh chưa trích xuất → trích xuất trước khi tiếp tục. Nếu không thể trích xuất → ghi nhận lỗi vào `00_plan/image_manifest.json` và đánh trạng thái chương là BLOCKED.

### BƯỚC 1: ĐỌC NGUYÊN TÁC
- Mở `02_extracted_text/v1/chXX.txt`. Ghi nhận: trang PDF, số đoạn, số cước chú, **số hình ảnh theo từng trang** (từ image manifest).

### BƯỚC 2: PHÂN ĐOẠN
- Mỗi đoạn: `[V1CXX-PYYY] (trang Z)`.
- Tạo `04_translation/v1/chXX/v1_chXX_src.txt` và `v1_chXX_vi.txt` (1-1 mapping).

### BƯỚC 3: DỊCH THEO 7 BƯỚC GRAMMAR ENGINE + VNCH GRAMMAR
**Kích hoạt**: `contextual-translation` (Bước 1-3) + `historical-terminology-research` (Bước 4) + `southern-vietnamese-editorial-style` (Bước 5).

| Bước | Nội dung | Skill hỗ trợ |
|---|---|---|
| 1 | Phân tích ngữ pháp nguyên tác (chủ thể, vị ngữ, đối tượng, quan hệ logic) | `contextual-translation` |
| 2 | Xác định chủ thể, vị ngữ, đối tượng; passive → chủ động | `contextual-translation` |
| 3 | Phân tích quan hệ logic (dùng từ nối Nam Bộ: dầu, trái lại, tuy vậy, bởi thế, vả) | `contextual-translation` |
| 4 | Xác định thuật ngữ (tra Lexicon → VNCH Grammar → Nguồn VNCH → giữ gốc + ghi chú) + **VLP-01: nhận diện từ/cụm ngoại ngữ trong nguồn, phân loại A/B/C/D trước khi dịch** | `historical-terminology-research` |
| 5 | Tái cấu trúc VNCH: chủ động hóa, chỉ định, trạng từ nầy/đó/kia, thể khía, đại từ, từ nối, CẤM dịch từng từ + **VLP-01: dịch nghĩa sang tiếng Việt trước, chỉ giữ ngoại ngữ khi có lý do ngôn học/nội dung rõ ràng** | `southern-vietnamese-editorial-style` |
| 5b | **Kiểm tra cấp câu VLP-01**: không còn ngoại ngữ có thể dịch nhưng bị giữ nguyên, không dùng phiên âm thay nghĩa, không cấu trúc dịch máy/ngoại ngữ, tự nhiên với độc giả VNCH trước 1975 | `translation-error-detection` |
| 6 | Đối chiếu: số câu, thông tin, thuật ngữ, cước chú, alignment (src=vi) | `deep-translation-review` |
| 7 | Kiểm tra dễ hiểu (hiểu ngay lần đầu) | `deep-translation-review` |

### BƯỚC 4: KIỂM TRA ORTHOGRAPHY + VLP-01
- Chạy `python .kilo/scripts/common/vnch_orthography.py --check-only NN` → 0 lỗi CRITICAL/MAJOR.
- **VLP-01 sentence-level check**: Mỗi câu đã được kiểm tra không còn ngoại ngữ có thể dịch, không phiên âm thay nghĩa, không cấu trúc dịch máy, tự nhiên với độc giả VNCH trước 1975.

### BƯỚC 5: THÊM CỤC CHÚ
- Giữ marker `[N]`/`N` trong thân bài. Khối `--- [Cước chú trang X-Y] ---`.

### BƯỚC 6: KIỂM TRA ENCODING
- UTF-8, NFC, no BOM, LF. Python: `encoding="utf-8", newline="\n"`.

### BƯỚC 7: CẬP NHẬT PROGRESS.JSON
- Thêm entry `V1-CXX` với status, paragraphs, footnotes, pages.

### BƯỚC 8: XUẤT DOCX + QUALITY GATE (8 TIÊU CHÍ)
1. `python -c "from docx_builder import DocxBuilder; from pathlib import Path; b=DocxBuilder(Path('.')); r=b.build_chapter(Path('translation-project/04_translation/v1/chNN/v1_chNN_vi.txt'), Path('translation-project/09_docx/V1-CNN_<slug>.docx')); print(r)"` → `OK N/N`.
2. **Kiểm tra hình ảnh trong DOCX**: Chạy `python translation-project/99_scripts/audit_docx_format.py NN` → phải PASS với `Images: N | Captions: N` (N = số ảnh trong image manifest). Mỗi caption phải đứng sau ảnh tương ứng (`every caption preceded by its image`, `image count == caption count`).
3. Word COM: `Footnotes.Count` = `notes` trong progress.json.
4. **Quality Gate 8 tiêu chí** (translation-quality-gate skill):
   - [ ] 1. Encoding UTF-8/NFC/no BOM/LF (`encoding_checker.py`)
   - [ ] 2. Orthography: 0× "chính trị", 0× từ miền Bắc (`vnch_orthography.py`)
   - [ ] 3. Đồng bộ đoạn: src = vi (`document_comparator.py`)
   - [ ] 4. Đồng bộ cước chú: src = vi (`docx_builder.py` → `OK N/N`)
   - [ ] 5. Không fabricate
   - [ ] 6. Văn phong tự nhiên (S1-S20, P1-P10)
   - [ ] 6b. **VLP-01 Tiếng Việt trước**: không còn từ/cụm ngoại ngữ có thể dịch nhưng bị giữ nguyên, không dùng phiên âm thay nghĩa, không cấu trúc dịch máy/ngoại ngữ, phù hợp văn phong miền Nam trước 1975
   - [ ] 7. DOCX tồn tại 09_docx/, sinh bởi `docx_builder.py`
   - [ ] 8. DOCX cước chú: `OK N/N`, Word `Footnotes.Count` = `notes`, footnote chân trang 9pt, 1..N
5. Cập nhật `progress.json`: `status: "HOAN_TAT"`, `docx`, `docx_status`.

## 8A. QUY TẮC ĐỊNH DẠNG DOCX (BẮT BUỘC — TỪ BÀI HỌC CHƯƠNG 9)

> **Áp dụng cho MỌI chương.** Các quy tắc dưới đây được rút ra từ lỗi thực tế khi hiệu chỉnh Chương 9 (V1-C09). Mọi session PHẢI đọc mục này trước khi xuất DOCX. Script chuẩn `translation-project/99_scripts/build_chapter_docx.py` đã tự động áp dụng các quy tắc này; session KHÔNG được tự viết script build thay thế.

### 8A.1 Định dạng chuẩn (không tự thiết kế)

| Thành phần | Font | Cỡ | Canh lề | Khoảng cách | Ghi chú |
|---|---|---|---|---|---|
| **Tiêu đề chương (title block)** | Times New Roman | 24pt bold | Canh giữa | — | Tự sinh, không sửa |
| **Đề mục (heading)** | Times New Roman | 13.5pt bold | Canh trái | sb=14pt, sa=6pt, line=1.15 | `keep_with_next=True` (không tách khỏi đoạn sau) |
| **Thân bài (body)** | Times New Roman | 12pt (không nghiêng) | Justify (both) | fi=0.9cm, sa=6pt, line=1.3 | `widow_control=True` |
| **Trích dẫn (quote)** | Times New Roman | 12pt **nghiêng** | Justify (both) | li=0.5" (720 twips), sa=6pt, line=1.3 | Không thụt đầu dòng |
| **Chú thích hình (caption "Hình X.Y")** | Times New Roman | 10pt nghiêng | Canh giữa | — | `keep_together=True` |
| **Ảnh (image)** | — | rộng 4.5" | Canh giữa | sb=6pt, sa=2pt | `keep_with_next=True` (dính liền caption) |
| **Cước chú (footnote)** | Times New Roman | 9pt (sz=18) | Justify | — | Đánh số tự động 1..N, chân trang |
| **A4, lề** | — | — | — | — | Trên 1.9cm, dưới 1.8cm, trái 2.1cm, phải 1.8cm |

### 8A.2 Lỗi thực tế từ Chương 9 và cách phòng ngừa

| # | Lỗi thực tế | Nguyên nhân | Cách phòng ngừa (đã tích hợp vào script) |
|---|---|---|---|
| 1 | **14 cước chú thiếu marker** (4,5,37,39-42,44,45,47-51) → footnote bị dồn cuối chương | TXT thân bài thiếu marker `[N]` ở 14 vị trí; marker 21 ở dạng "20 21" (số trần liền nhau) | Trước khi build, chạy `list_vi_markers.py` để liệt kê marker thiếu. Chèn marker `[N]` đúng vị trí (theo tỷ lệ src). Marker dạng "20 21" phải sửa thành "[20][21]". |
| 2 | **Trích dẫn không được trích xuất footnote** | `extract_inline_markers` chỉ nhận `kind=="para"`, bỏ qua `kind=="quote"` | ĐÃ SỬA: điều kiện thành `kind in ("para", "quote")`. Không cần làm gì thêm. |
| 3 | **Heading không đúng định dạng** (sai cỡ/sai khoảng cách) | TXT không có nhãn `đề mục`; build không nhận diện heading | TXT phải ghi `--- [V1CXX-PYYY] (trang Z) — đề mục ---` cho mỗi đề mục. Script tự chuyển thành heading 13.5pt bold. |
| 4 | **Trích dẫn không được định dạng** | TXT không có nhãn `trích dẫn` | TXT phải ghi `--- [V1CXX-PYYY] (trang Z) — trích dẫn ---`. Script tự chuyển thành quote (nghiêng, li=0.5"). |
| 5 | **Ảnh và caption bị tách trang** | Đoạn ảnh không có `keep_with_next` | ĐÃ SỬA: ảnh giờ có `keep_with_next=True`, caption có `keep_together=True`. |
| 6 | **Build crash khi Word đang mở file** | `out.unlink()` raises PermissionError (WinError 32) | ĐÃ SỬA: `_safe_unlink()` retry 10 lần (0.3s mỗi lần), báo lỗi rõ ràng "hãy đóng Word". |
| 7 | **File DOCX cũ (slug khác) gây nhầm lẫn** | Build cũ dùng slug tiếng Việt, build mới dùng slug tiếng Anh → 2 file cùng chương | `audit_docx_format.py` chọn file MỚI NHẤT. Session nên xóa file DOCX cũ cùng chương trước khi build lại. |
| 8 | **Bare marker (số trần) false positive** | Số trong thân bài (năm, số trang) trùng `expect` → bị nuốt làm footnote | Script chỉ nhận bare marker khi `num == expect` (chuỗi tuần tự). Chương dùng marker `[N]` an toàn hơn bare marker. |

### 8A.3 Quy tắc chuẩn bị TXT trước khi build

1. **Đề mục (heading):** Mỗi đề mục phải ở dòng riêng với header `--- [V1CXX-PYYY] (trang Z) — đề mục ---`, nội dung đề mục ở dòng kế tiếp.
2. **Trích dẫn (quote):** Mỗi trích dẫn phải có header `--- [V1CXX-PYYY] (trang Z) — trích dẫn ---`, nội dung trích dẫn ở các dòng kế tiếp.
3. **Marker cước chú:** Ưu tiên `[N]` (dạng ngoặc vuông) hơn số trần. Nếu dùng số trần, phải đảm bảo tuần tự 1..N và không có số lạc (năm, số trang) trùng `expect`.
4. **Marker liền nhau:** "20 21" phải sửa thành "[20][21]" để script nhận diện đúng 2 footnote riêng biệt.
5. **Không để metadata lọt vào thân bài:** Dòng "Source: ..." phải nằm trong khối meta (trước `--- [` đầu tiên), không nằm trong thân đoạn.

### 8A.4 Kiểm tra hồi quy bắt buộc trước khi bàn giao

Sau khi build, CHẠY validator:
```bash
python translation-project/99_scripts/audit_docx_format.py NN
```
Validator kiểm tra TỰ ĐỘNG:
- Heading: 13.5pt bold, sb=14pt sa=6pt
- Body: 12pt, Justify, fi=0.9cm, sa=6pt, line=1.3
- Quote: 12pt nghiêng, li=0.5"
- Footnote: 9pt, tuần tự 1..N, không dồn cuối
- Không leak metadata (Source:, 02_extracted_text)
- Không leak block-header (`--- [...] ---`)
- Ảnh đặt trước caption (nếu có)
- Image/caption count khớp

Exit code 0 = PASS, 1 = FAIL. **Không bàn giao DOCX nếu validator FAIL.**

### 8A.5 Cấm

- KHÔNG tự viết script build thay thế `build_chapter_docx.py`.
- KHÔNG sửa template DOCX thủ công.
- KHÔNG dùng bản OCR raw (`*_text_ocr.txt`, `*_text_p1.txt`) làm nguồn build — chỉ dùng `v1_chXX_vi.txt`.
- KHÔNG bỏ qua cảnh báo `WARN` (footnote không đủ N/N) trong output build.

## 9. QUY TẶC VLP-01 — TIẾNG VIỆT TRƯỚC (VIETNAMESE-FIRST TRANSLATION)

**Quy tắc bắt đầu:** Dịch nghĩa sang tiếng Việt trước, chỉ giữ nguyên ngoại ngữ khi có lý do ngôn ngữ học hoặc nội dung rõ ràng.

Áp dụng ngay từ câu đầu tiên, không đợi đến vòng audit sau này.

### 9.1 Quy trình xử lý từng câu

Với từng câu nguồn, người dịch phải thực hiện theo thứ tự:

1. **Nhận diện** các từ, cụm từ, thành ngữ và thuật ngữ có nguồn gốc ngoại ngữ (Nhật, Hán ngữ, Trung Hoa, Đức, Pháp, Anh hoặc ngôn ngữ khác).
2. **Xác định nghĩa chính xác** trong ngữ cảnh, không dịch dựa trên mặt chữ hoặc phiên âm.
3. **Tìm cách diễn đạt tương đương** bằng tiếng Việt tự nhiên, phù hợp văn phong miền Nam trước năm 1975.
4. **Không tự động giữ nguyên** từ ngoại ngữ chỉ vì từ đó xuất hiện trong nguyên tác.
5. **Không sử dụng phiên âm** ngoại ngữ thay cho việc dịch nghĩa.
6. **Không tạo từ mới** hoặc cách ghép từ gượng ép để mô phỏng cấu trúc ngôn ngữ nguồn.

### 9.2 Phân loại từ trước khi quyết định giữ lại

Mỗi từ ngoại ngữ phải được xử lý theo một trong bốn nhóm:

| Nhóm | Định nghĩa | Quyết định |
|---|---|---|
| **A. Từ đã Việt hóa** | Từ Hán Việt đã trở thành vốn thông dụng; từ vay mượn dùng ổn định trong tiếng Việt; thuật ngữ quen thuộc trong sách báo miền Nam trước 1975. | Được phép sử dụng nếu đúng nghĩa, đúng văn cảnh, phù hợp văn phong. |
| **B. Từ ngoại quốc có thể dịch** | Có cách diễn đạt tương đương rõ ràng bằng tiếng Việt. | **Phải dịch sang tiếng Việt**. Không giữ nguyên chỉ vì nguyên tác viết bằng ngoại ngữ. |
| **C. Tên riêng và thuật ngữ cần giữ nguyên** | Tên người, địa danh, tổ chức, nhan đề, danh xưng hoặc thuật ngữ chuyên biệt mà việc dịch sẽ làm sai lệch nội dung. | Có thể giữ nguyên, nhưng phải phân biệt tên riêng với phần mô tả có thể dịch được. |
| **D. Từ ngoại quốc chưa có cách dịch tương đương rõ ràng** | Chưa xác định được cách dịch tương đương rõ ràng. | Tra cứu glossary và tài liệu tham chiếu. Nếu vẫn chưa xác định, đánh dấu `UNRESOLVED_TERM`, ghi rõ ngữ cảnh, **KHÔNG** tự ý phiên âm hoặc sáng tạo cách dịch. |

### 9.3 Kiểm tra ngay trong từng câu (Sentence-level Check)

Trước khi chuyển sang câu tiếp theo, phải tự hỏi và trả lời có/không cho từng câu hỏi:

- Câu này có còn từ ngoại quốc chưa được dịch không?
- Có chữ Hán hoặc cách viết theo ngôn ngữ Trung Hoa không cần thiết không?
- Có từ Nhật, Đức, Pháp hoặc Anh bị giữ lại do thói quen không?
- Có từ được phiên âm nhưng thực chất có thể dịch nghĩa không?
- Có cách diễn đạt tiếng Việt miền Nam tự nhiên hơn không?
- Cấu trúc câu có bị ảnh hưởng bởi ngữ pháp ngoại ngữ không?
- Một độc giả Việt Nam trước năm 1975 có thể đọc câu này tự nhiên mà không cần biết ngoại ngữ không?

Nếu câu trả lời là "có" cho bất kỳ câu hỏi nào → phải sửa ngay trước khi hoàn tất đoạn.

### 9.4 Phân biệt tiếng Việt gốc Hán và Hán ngữ

Không được hiểu quy tắc thuần Việt là cấm toàn bộ từ Hán Việt. Phải phân biệt:

- **Từ Hán Việt đã Việt hóa**: dùng tự nhiên trong tiếng Việt (ví dụ: chính trị, quốc gia, chiến tranh, dân tộc…) → được phép.
- **Hán ngữ hiện đại**: giữ nguyên hoặc dịch bám theo tiếng Trung → KHÔNG được phép nếu đã có cách diễn đạt tiếng Việt tự nhiên.
- **Cách dùng từ, trật tự từ, cấu trúc câu chịu ảnh hưởng trực tiếp từ tiếng Trung** → phải tái cấu trúc theo tiếng Việt.
- **Từ Hán Việt không phù hợp văn cảnh hoặc không thuộc cách dùng tự nhiên trong văn phong miền Nam** → phải thay bằng từ thay thế thích hợp.

Ưu tiên cách diễn đạt đã được sử dụng trong sách báo, văn liệu và học thuật miền Nam trước năm 1975 khi có căn cứ.

### 9.5 Cơ chế kiểm tra tích hợp vào quy trình dịch

| Giai đoạn | Hành động VLP-01 |
|---|---|
| **Before Translation** | Nhận diện thuật ngữ ngoại ngữ trong nguồn; phân loại A/B/C/D |
| **During Translation** | Dịch nghĩa sang tiếng Việt; áp dụng cách dùng tiếng Việt phù hợp |
| **Sentence-level Check** | Kiểm tra từng câu ngay sau khi dịch (xem §9.3) |
| **Paragraph-level Check** | Đọc lại toàn đoạn để bảo đảm câu văn tự nhiên, thống nhất |
| **Exception Register** | Ghi nhận những từ ngoại quốc thực sự cần giữ lại và lý do |

Chỉ chuyển sang đoạn tiếp theo khi đoạn hiện tại đạt yêu cầu VLP-01.

Không cần tạo báo cáo dài cho từng câu đạt chuẩn. Chỉ ghi nhận những trường hợp ngoại lệ, thuật ngữ chưa giải quyết được và lỗi đã phát hiện.

### 9.6 Điều kiện PASS của một câu

Một câu chỉ được xem là đạt VLP-01 khi:

- [ ] Đã chuyển nghĩa đầy đủ sang tiếng Việt.
- [ ] Không còn ngoại ngữ có thể dịch nhưng bị giữ nguyên.
- [ ] Không dùng phiên âm thay cho dịch nghĩa.
- [ ] Không có cấu trúc dịch máy hoặc cấu trúc ngoại ngữ.
- [ ] Từ ngữ phù hợp văn phong miền Nam trước năm 1975.
- [ ] Không làm sai lệch nghĩa, sắc thái và lập luận của nguyên tác.

---

## 10. CHECKLIST BẮT BUỘC MỖI SESSION MỚI (MỞ RỘNG)

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

## 11. TRẠNG THÁI HIỆN TẠI (2026-11-21)

| Chương | Trạng thái | Từ | Cước chú | DOCX | Hình ảnh |
|---|---|---|---|---|---|
| V1-Ch1 | HOAN_TAT | 7,533 | 35 | 13 trang | 0 |
| V1-Ch2 | HOAN_TAT | 10,205 | 31 | 16 trang | 2 (Hình 2.1, 2.2) |
| V1-Ch3 | HOAN_TAT | 8,913 | 51 | 15 trang | 1 (Hình 3.1) |
| V1-Ch4 | HOAN_TAT | 8,942 | 71 | 17 trang | 2 (Hình 4.1, 4.2) |
| V1-Ch5 | HOAN_TAT | 9,124 | 26 | 14 trang | 2 (Hình 5.1, 5.2) |
| V1-Ch6 | HOAN_TAT | 11,731 | 43 | 18 trang | 1 (Hình 6.1) |
| V1-Ch7 | HOAN_TAT | — | — | — | — |
| V1-Ch8 | HOAN_TAT | — | — | — | — |
| V1-Ch9 | HOAN_TAT | 9,621 | 51 | 3 hình | 3 (Hình 9.1, 9.2, Bản đồ 9.1) |
| V1-Ch10 | EXTRACTION_COMPLETE (dịch dở P012+) | 3,475 | 0 | 2 hình | 2 (Hình 10.1 p223, Bản đồ 10.1 p229) |
| **Tổng V1 (1-10)** | — | — | — | — | — |

**V1-Ch10**: DOCUMENT_EXTRACTION_COMPLETE — 20 trang PDF (218-237), raw text + 2 hình (Figure 10.1 raster + Map 10.1 vector rasterized) + image_manifest.json + DOCX (audit PASS, 2 hình nhúng). DỊCH mới xong P001-P011; P012+ CHƯA dịch.
**V1-Ch11 đến V1-Ch21**: Chưa bắt đầu. **Volume 2, 3**: Chưa bắt đầu.

## 12. LIÊN KẾT TÀI LIỆU QUAN TRỌNG

| Tài liệu | Vị trí | Mục đích |
|---|---|---|
| MASTER_PLAN | `00_plan/MASTER_PLAN.md` | Kế hoạch tổng 11 mục |
| Chapter Inventory | `00_plan/chapter_inventory.csv` | 77 chương (volume, title, pages, words) |
| Style Guide v2.3 | `07_style_guide/STYLE_GUIDE_PHAN_B.md` | 29 quy tắc VNCH |
| Grammar Engine v2.1 | `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` | 7 bước + VNCH Grammar + Checklist |
| Master Lexicon | `08_southern_vietnamese_library/10_LEXICAL_DATABASE/MASTER_LEXICON.csv` | 321 mục từ điển Nam |
| Audit Report | `05_qa/AUDIT_REPORT_CH01-06.md` | 222 lỗi đã fix, bài học 6 chương |
| Quality Gate | `05_qa/FINAL_PILOT_QUALITY_GATE.md` | 8 tiêu chí PASS |
| Progress | `00_plan/progress.json` | Checkpoint trạng thái |

## 13. QUY TẶC HÁN VIỆT — TÊN NHÂN VẬT TRUNG QUỐC (ESTABLISHED SINO-VIETNAMESE NAMES)

**Mục tiêu:** Bảo đảm tên các lãnh tụ, chính khách, tướng lĩnh và nhân vật lịch sử Trung Quốc được dịch theo cách gọi Hán-Việt đã định hình trong truyền thống sách báo và sử liệu tiếng Việt, thay vì giữ nguyên Pinyin hoặc phiên âm tiếng Anh.

### 13.1 Quy tắc ưu tiên

Khi gặp tên nhân vật Trung Quốc:

1. **Ưu tiên tên Hán-Việt đã được xác lập** và sử dụng phổ biến trong tiếng Việt.
2. **Không giữ Pinyin** hoặc cách viết tiếng Anh nếu đã có tên Hán-Việt tương ứng.
3. **Không tự sáng tạo cách phiên âm.**
4. **Không chuyển đổi tên một cách máy móc** nếu chưa xác minh được chữ Hán và cách đọc.
5. **Giữ nguyên cách viết tên đã thống nhất** trong toàn bộ bản dịch.

### 13.2 Bảng tên chuẩn (khởi đầu, không phải danh mục đóng)

| Pinyin / English | Tên tiếng Việt phải dùng |
|---|---|
| Zhou Enlai / Chou En-lai | Chu Ân Lai |
| Mao Zedong / Mao Tse-tung | Mao Trạch Đông |
| Deng Xiaoping | Đặng Tiểu Bình |
| Liu Shaoqi | Lưu Thiếu Kỳ |
| Zhu De | Chu Đức |
| Lin Biao | Lâm Bưu |
| Hua Guofeng | Hoa Quốc Phong |
| Chen Yun | Trần Vân |
| Ye Jianying | Diệp Kiếm Anh |
| Kang Sheng | Khang Sinh |
| Wang Hongwen | Vương Hồng Văn |
| Zhang Chunqiao | Trương Xuân Kiều |
| Jiang Qing | Giang Thanh |
| Peng Dehuai | Bành Đức Hoài |
| Zhou Yongkang | Chu Vĩnh Khang |
| Xi Jinping | Tập Cận Bình |
| Hu Jintao | Hồ Cẩm Đào |
| Jiang Zemin | Giang Trạch Dân |

### 13.3 Xử lý khi dịch

**Ví dụ đúng:**

- Source: Zhou En-lai met Mao Tse-tung in Beijing.
- Dịch: Chu Ân Lai gặp Mao Trạch Đông tại Bắc Kinh.

**Ví dụ sai:**

- Dịch: Zhou En-lai gặp Mao Tse-tung tại Bắc Kinh. (Giữ Pinyin, không đạt)

### 13.4 Kiểm tra tự động trước khi hoàn thành chương

- Quét toàn bộ bản dịch để phát hiện tên Pinyin còn sót.
- Đối chiếu với bảng tên chuẩn trong §13.2.
- Kiểm tra tính nhất quán giữa nội dung chính, chú thích và chú giải.
- Nếu phát hiện tên chưa có trong bảng, tra cứu và xác minh trước khi quyết định cách viết.
- Không tự động chuyển đổi tên nếu chưa xác định chắc chắn danh tính nhân vật.

### 13.5 Nguyên tắc văn phong

Sử dụng tên Hán-Việt theo truyền thống văn bản lịch sử tiếng Việt, phù hợp với văn phong Việt Nam Cộng Hòa mà dự án đang theo đuổi. Không pha trộn tùy tiện giữa Pinyin, cách phiên âm tiếng Anh và tên Hán-Việt trong cùng một bản dịch.

---

*Cập nhật: 2026-11-21 — Tích hợp VLP-01 (Tiếng Việt trước) làm quy tắc bắt buộc trong quy trình dịch, Quality Gate criterion 6b, và checklist session; thêm quy tắc Hán Việt (Section 13) chuẩn hóa tên nhân vật Trung Quốc; **thêm Section 8A: Quy tắc định dạng DOCX từ bài học Chương 9** (heading/quote/footnote/image/font/spacing/pagination/layout + validator `audit_docx_format.py`); Grammar Engine v2.1, Style Guide v2.3, Audit 6 chương.*
