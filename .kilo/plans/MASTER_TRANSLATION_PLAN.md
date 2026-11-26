# MASTER TRANSLATION PLAN — THE CAMBRIDGE HISTORY OF THE VIETNAM WAR (3 VOLUMES)

## 1. PROJECT OVERVIEW

| Field | Value |
|-------|-------|
| Book | The Cambridge History of the Vietnam War (3 volumes) |
| Source PDF | `books/The_Cambridge_History_of_the_Vietnam_War.pdf` — 1866 pages |
| Total chapters | 77 chapters + 6 front/back matter sections (GI, IN, etc.) |
| Total words | ~698,500 |
| Target language | Vietnamese (Southern, VNCH pre-1975 standard) |
| Project root | `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project/` |
| Encoding | UTF-8, NFC, no BOM, LF |
| Plan files | MASTER_TRANSLATION_PLAN.md, VOLUME_01_PLAN.md, VOLUME_02_PLAN.md, VOLUME_03_PLAN.md, CHAPTER_STATUS_MATRIX.md, EXECUTION_ROADMAP.md, QUALITY_GATES.md, progress.json |

## 2. SOURCE INVENTORY (verified)

| Directory | Content | Chapters | Status |
|-----------|---------|----------|--------|
| `01_source_pdf/` | Source PDF | All | Present (1866 pages, text layer) |
| `02_extracted_text/v1/` | Extracted text pass 1 | ch01-ch21 | Done |
| `02_extracted_text/v2/` | Extracted text pass 2 | ch01-ch30 | Done |
| `02_extracted_text/v3/` | Extracted text pass 3 | ch01-ch26 | Done |
| `04_translation/v1/chXX/` | Translation (src + vi) | ch01-ch15 | Done |
| `04_translation/v1/chXX/` | Translation directory missing | ch16-ch21 | Not started |
| `04_translation/v2/` | Translation volume 2 | — | Not started |
| `04_translation/v3/` | Translation volume 3 | — | Not started |
| `09_docx/` | DOCX output | ch01-ch15 (partial) | Partial |
| `03_terminology/` | Glossary, lexicon, sources | — | Done |
| `07_style_guide/` | Style Guide Phan B v2.3, Grammar Engine v2.1 | — | Done |
| `05_qa/` | QA reports, audit reports | ch01-ch15 (partial) | Partial |
| `99_scripts/` | Build, QA, fix scripts | — | Present |

## 3. TRANSLATION STANDARDS (mandatory)

- **Language:** Vietnamese miền Nam, truyền thống VNCH trước 1975
- **Style Guide:** `07_style_guide/STYLE_GUIDE_PHAN_B.md` (29 quy tắc, v2.3)
- **Grammar Engine:** `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` (7 bước, S1-S20, P1-P10, C1-C10)
- **Terminology:** `03_terminology/glossary_nam_bac_compare.tsv`, `MASTER_LEXICON.csv` (321+ mục)
- **Sources:** `03_terminology/SOURCES.md`, `uncertain_terms.md`
- **Encoding:** UTF-8, NFC, no BOM, LF — cả src và vi
- **Alignment:** 1:1 paragraph mapping (src paragraphs = vi paragraphs), cùng ID và thứ tự
- **Footnotes:** Word native footnotes qua OOXML, không giả lập bằng superscript/văn bản cuối chương
- **Quy trình:** TEXT RECONSTRUCTION → SOURCE → TRANSLATION → EDITING → QA → DOCX → VALIDATION
- **Cấm:** Dịch word-for-word, tự thêm ý, lược bỏ nội dung, sáng tạo thuật ngữ, dịch trực tiếp OCR theo từng trang

## 4. KNOWN ISSUES (must be addressed in Phase 1)

| ID | Chapter | Issue | Severity | Action |
|----|---------|-------|----------|--------|
| ISSUE-01 | V1-C01 | `v1_ch01_vi.txt` chứa nội dung Arendt (Antisemitism) — chéo dữ liệu từ dự án khác | CRITICAL | Xóa toàn bộ, dịch lại từ `02_extracted_text/v1/ch01.txt` |
| ISSUE-02 | V1-C11 | Thiếu 21 cước chú tiếng Việt (BUG-008) | CRITICAL | Trích xuất từ `02_extracted_text/v1/ch11.txt`, dịch, thêm khối cước chú |
| ISSUE-03 | V1-C12 | Thiếu 42 footnote markers, marker trùng [20] (BUG-001, BUG-003, BUG-009) | CRITICAL | Sửa markers, re-align, rebuild DOCX |
| ISSUE-04 | V1-C14 | Bản dịch đầu là machine translation placeholder — đã viết lại (REVIEW_AUDIT_CH14.md) | MAJOR | Xác nhận bản đã sửa là bản cuối |
| ISSUE-05 | V1-C08 | Từ Đức "nässig" dùng nhầm làm "nässig" (28 lần) — đã sửa (LANGUAGE_PURITY_REVIEW_V1-C08.md) | MAJOR | Xác nhận đã sửa |
| ISSUE-06 | V1-C01..C06 | Lỗi alignment, thuật ngữ VNCH sai (222 lỗi đã fix qua AUDIT_REPORT_CH01-06.md) | MAJOR | Xác nhận đã áp dụng `apply_vnch_fixes.py` |
| ISSUE-07 | All | `progress.json` tham chiếu sách Arendt, không phải The Cambridge History of the Vietnam War | CRITICAL | Tạo `progress.json` mới cho dự án này |

## 5. FILE STRUCTURE CONVENTIONS

```
translation-project/
├── 01_source_pdf/              # Source PDF
├── 02_extracted_text/
│   ├── v1/                     # Extraction pass 1 (ch01-ch21)
│   ├── v2/                     # Extraction pass 2 (ch01-ch30)
│   └── v3/                     # Extraction pass 3 (ch01-ch26)
├── 03_terminology/
│   ├── glossary_nam_bac_compare.tsv
│   ├── MASTER_LEXICON.csv
│   ├── SOURCES.md
│   └── uncertain_terms.md
├── 04_translation/
│   ├── v1/chXX/                # v1_chXX_src.txt + v1_chXX_vi.txt (ch01-ch15 done)
│   ├── v2/chXX/                # (to be created)
│   └── v3/chXX/                # (to be created)
├── 05_qa/                      # QA reports per chapter
├── 06_reports/                 # Audit, review, bug reports
├── 06_temp/                    # Temp files
├── 07_style_guide/
│   ├── STYLE_GUIDE_PHAN_B.md
│   ├── STYLE_GUIDE.md
│   ├── TERMINOLOGY_TABLE_BY_DOMAIN.md
│   └── TRANSLATION_GRAMMAR_ENGINE.md
├── 08_southern_vietnamese_library/
│   └── 10_LEXICAL_DATABASE/
│       └── MASTER_LEXICON.csv
├── 09_docx/                    # DOCX output
├── 00_plan/                    # Master plan files
├── chinese_check.txt           # Hán character check
└── 99_scripts/                 # Build, QA, fix scripts (centralized)
```

## 6. VOLUME DEFINITION (TBD — verify from extracted text)

| Volume | Chapters | Page range (PDF) | Page range (in-book) | Status |
|--------|----------|-------------------|----------------------|--------|
| Volume 1 | ch01-ch?? | TBD | TBD | Extraction done (v1: ch01-ch21) |
| Volume 2 | ch??-ch?? | TBD | TBD | Extraction done (v2: ch01-ch30) |
| Volume 3 | ch??-ch?? | TBD | TBD | Extraction done (v3: ch01-ch26) |

**Note:** v1/v2/v3 extraction directories all start at ch01 — need to verify whether these are different volumes or different extraction passes. Volume boundaries to be confirmed during Phase 1 audit.

## 7. WORKFLOW PIPELINE (per chapter)

**Bước 1 — Source verification:** Xác minh `02_extracted_text/vN/chXX.txt` có đủ nội dung, đúng trang, không thiếu.
**Bước 2 — Paragraph reconstruction:** Ghép đoạn chia trang, khôi phục câu ngắt, xóa header/footer/số trang. Có ID `[V1CNN-Pxxx] (trang X)`.
**Bước 3 — Translation:** Chỉ dịch khi source đã xác minh. Dịch theo paragraph hoàn chỉnh. Tuân thủ Style Guide + Grammar Engine. Checkpoint lưu tiến độ.
**Bước 4 — Editing:** Sửa lỗi alignment, VNCH orthography, câu dịch máy.
**Bước 5 — QA:** 8 tiêu chí QUALITY_GATES.md. Tất cả phải PASS.
**Bước 6 — DOCX:** Build DOCX với Word native footnotes (OOXML).
**Bước 7 — Validation:** Word COM verify Footnotes.Count, audit_docx_format.py.

## 8. EXECUTION PHASES

| Phase | Scope | Deliverable |
|-------|-------|-------------|
| Phase 1 | Audit & fix existing work (ISSUE-01 to ISSUE-07) | Fixed ch01-ch15, corrected progress.json |
| Phase 2 | Complete V1 translations (ch16-ch21) | v1_chXX_vi.txt for ch16-ch21 |
| Phase 3 | QA + DOCX for V1 (ch01-ch21) | QA reports + 21 DOCX files |
| Phase 4 | Translate V2 (ch01-ch30) | v2 translations |
| Phase 5 | Translate V3 (ch01-ch26) | v3 translations |
| Phase 6 | QA + DOCX for V2, V3 | QA reports + DOCX files |
| Phase 7 | Final validation + master DOCX | All 77 chapters HOAN_TAT |

## 9. DELIVERABLES

| File | Location |
|------|----------|
| MASTER_TRANSLATION_PLAN.md | `.kilo/plans/` |
| VOLUME_01_PLAN.md | `.kilo/plans/` |
| VOLUME_02_PLAN.md | `.kilo/plans/` |
| VOLUME_03_PLAN.md | `.kilo/plans/` |
| CHAPTER_STATUS_MATRIX.md | `.kilo/plans/` |
| EXECUTION_ROADMAP.md | `.kilo/plans/` |
| QUALITY_GATES.md | `.kilo/plans/` |
| progress.json | `00_plan/` within translation-project |

## 10. RULES

- Không bắt đầu dịch ngay trước khi Phase 1 audit hoàn tất.
- Không xóa hoặc ghi đè dữ liệu gốc.
- Không bỏ qua bất kỳ tài liệu nào trong project.
- Không tự tạo nội dung hoặc dữ liệu chưa được xác minh.
- Mọi file văn bản sử dụng UTF-8.
- Scripts lưu tập trung tại `99_scripts/`.
- Phải có checkpoint, log và khả năng tiếp tục giữa các session.
