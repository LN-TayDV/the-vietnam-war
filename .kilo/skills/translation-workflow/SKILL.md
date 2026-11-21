---
name: translation-workflow
description: Workflow chuẩn cho dự án dịch The Cambridge History of the Vietnam War sang tiếng Việt miền Nam (VNCH pre-1975). Capture toàn bộ quy trình, cấu trúc file, kiểm tra chất lượng, theo dõi tiến độ và xuất DOCX chuẩn (bố cục sách, footnote chân trang) sau mỗi chương. Dùng khi bắt đầu dịch chương mới, tiếp tục dự án dịch, hoặc xuất bản một chương đã dịch xong.
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
| `build_chapter_docx.py` | Legacy chapter DOCX builder (backward compat) |
| `build_volume_docx.py` | Legacy volume DOCX builder (backward compat) |
| `extract_chapters.py` | One-time PDF → text extraction (pymupdf) |
| `build_lexicon.py` | Lexicon management: `build`, `update`, `verify`, `stats` |
| `write_translation.py` | AI translation writer (79KB, specialized) |
| `build_corpus.py` | Corpus building for research |

*Đã xóa: 42 script cũ/debug/chapter-specific/tmp (xem consolidation report).*

## 8. QUY TRÌNH DỊCH MỘT CHƯƠNG (8 BƯỚC + QUALITY GATE)

### BƯỚC 0: KHỞI ĐỘNG SESSION MỚI (BẮT BUỘC)
1. Kiểm tra rác workspace (xóa file lệch thư mục).
2. Đọc `00_plan/progress.json` → xác định chương tiếp theo.
3. Đọc `STYLE_GUIDE_PHAN_B.md` + `TRANSLATION_GRAMMAR_ENGINE.md`.
4. Đọc `MASTER_LEXICON.csv` + `AUDIT_REPORT_CH01-06.md`.
5. **Kích hoạt skill**: `historical-book-translation` + `contextual-translation` + `southern-vietnamese-editorial-style`.

### BƯỚC 1: ĐỌC NGUYÊN TÁC
- Mở `02_extracted_text/v1/chXX.txt`. Ghi nhận: trang PDF, số đoạn, số cước chú.

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
| 4 | Xác định thuật ngữ (tra Lexicon → VNCH Grammar → Nguồn VNCH → giữ gốc + ghi chú) | `historical-terminology-research` |
| 5 | Tái cấu trúc VNCH: chủ động hóa, chỉ định, trạng từ nầy/đó/kia, thể khía, đại từ, từ nối, CẤM dịch từng từ | `southern-vietnamese-editorial-style` |
| 6 | Đối chiếu: số câu, thông tin, thuật ngữ, cước chú, alignment (src=vi) | `deep-translation-review` |
| 7 | Kiểm tra dễ hiểu (hiểu ngay lần đầu) | `deep-translation-review` |

### BƯỚC 4: KIỂM TRA ORTHOGRAPHY
- Chạy `python .kilo/scripts/common/vnch_orthography.py --check-only NN` → 0 lỗi CRITICAL/MAJOR.

### BƯỚC 5: THÊM CỤC CHÚ
- Giữ marker `[N]`/`N` trong thân bài. Khối `--- [Cước chú trang X-Y] ---`.

### BƯỚC 6: KIỂM TRA ENCODING
- UTF-8, NFC, no BOM, LF. Python: `encoding="utf-8", newline="\n"`.

### BƯỚC 7: CẬP NHẬT PROGRESS.JSON
- Thêm entry `V1-CXX` với status, paragraphs, footnotes, pages.

### BƯỚC 8: XUẤT DOCX + QUALITY GATE (8 TIÊU CHÍ)
1. `python -c "from docx_builder import DocxBuilder; from pathlib import Path; b=DocxBuilder(Path('.')); r=b.build_chapter(Path('translation-project/04_translation/v1/chNN/v1_chNN_vi.txt'), Path('translation-project/09_docx/V1-CNN_<slug>.docx')); print(r)"` → `OK N/N`.
2. Word COM: `Footnotes.Count` = `notes` trong progress.json.
3. **Quality Gate 8 tiêu chí** (translation-quality-gate skill):
   - [ ] 1. Encoding UTF-8/NFC/no BOM/LF (`encoding_checker.py`)
   - [ ] 2. Orthography: 0× "chính trị", 0× từ miền Bắc (`vnch_orthography.py`)
   - [ ] 3. Đồng bộ đoạn: src = vi (`document_comparator.py`)
   - [ ] 4. Đồng bộ cước chú: src = vi (`docx_builder.py` → `OK N/N`)
   - [ ] 5. Không fabricate
   - [ ] 6. Văn phong tự nhiên (S1-S20, P1-P10)
   - [ ] 7. DOCX tồn tại 09_docx/, sinh bởi `docx_builder.py`
   - [ ] 8. DOCX cước chú: `OK N/N`, Word `Footnotes.Count` = `notes`, footnote chân trang 9pt, 1..N
4. Cập nhật `progress.json`: `status: "HOAN_TAT"`, `docx`, `docx_status`.

## 9. CHECKLIST BẮT BUỘC MỖI SESSION MỚI (MỞ RỘNG)

1. **Kiểm tra rác workspace** → xóa file lệch.
2. Đọc `progress.json` → chương tiếp theo.
3. Đọc `STYLE_GUIDE_PHAN_B.md` + `TRANSLATION_GRAMMAR_ENGINE.md`.
4. Đọc `MASTER_LEXICON.csv` + `AUDIT_REPORT_CH01-06.md`.
5. **Kích hoạt skills**: `historical-book-translation`, `contextual-translation`, `southern-vietnamese-editorial-style`.
6. Dịch theo 8 bước.
7. Chạy `vnch_orthography.py` → `document_comparator.py` → `quality_gate.py` → `docx_builder.py`.
8. Quality Gate 8 tiêu chí PASS → cập nhật `progress.json` HOAN_TAT.
9. **Dọn dẹp file tạm** (tmp_*, debug_*, *.bak).

## 10. TRẠNG THÁI HIỆN TẠI (2026-11-20)

| Chương | Trạng thái | Từ | Cước chú | DOCX | Hình ảnh |
|---|---|---|---|---|---|
| V1-Ch1 | HOAN_TAT | 7,533 | 35 | 13 trang | 0 |
| V1-Ch2 | HOAN_TAT | 10,205 | 31 | 16 trang | 2 (Hình 2.1, 2.2) |
| V1-Ch3 | HOAN_TAT | 8,913 | 51 | 15 trang | 1 (Hình 3.1) |
| V1-Ch4 | HOAN_TAT | 8,942 | 71 | 17 trang | 2 (Hình 4.1, 4.2) |
| V1-Ch5 | HOAN_TAT | 9,124 | 26 | 14 trang | 2 (Hình 5.1, 5.2) |
| V1-Ch6 | HOAN_TAT | 11,731 | 43 | 18 trang | 1 (Hình 6.1) |
| **Tổng V1 (1-6)** | **HOAN_TAT** | **56,448** | **257** | **93 trang** | **8** |

**V1-Ch7 đến V1-Ch21**: Chưa bắt đầu. **Volume 2, 3**: Chưa bắt đầu.

## 11. LIÊN KẾT TÀI LIỆU QUAN TRỌNG

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

---

*Cập nhật: 2026-11-20 — Tích hợp 9 skills chuyên biệt, Grammar Engine v2.1, Style Guide v2.3, Audit 6 chương, Quality Gate 8 tiêu chí.*