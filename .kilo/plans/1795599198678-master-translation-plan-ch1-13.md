# MASTER TRANSLATION PLAN — THE ORIGINS OF TOTALITARIANISM (CH1–13)

## 1. PROJECT OVERVIEW

| Field | Value |
|-------|-------|
| Book | The Origins of Totalitarianism — Hannah Arendt |
| Edition | New Edition with Added Prefaces (1973), Harcourt Brace Jovanovich |
| Source PDF | books/Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf |
| Total pages | 574 |
| Sections | 18 (front matter + 4 prefaces + part one intro + 13 chapters) |
| Target language | Vietnamese (Southern, VNCH pre-1975 standard) |
| Working root | translation-project-arendt/ |
| Encoding | UTF-8, NFC, no BOM, LF |

## 2. MANDATORY 5-STEP WORKFLOW (ORDER ENFORCED)

**Bước 1 — OCR:** OCR mỗi trang PDF → lưu `02_extracted_text/v1/chXX.txt` với marker `=== PAGE N ===`.
**Bước 2 — Paragraph Reconstruction:** Ghép đoạn chia trang, khôi phục câu ngắt, xóa header/footer/số trang → `02_extracted_text/v2/chXX_src.txt` với ID `[V1CNN-Pxxx] (trang X)`.
**Bước 3 — Tạo Chapter SRC:** Xác minh source với PDF (không thiếu, trùng, sai thứ tự).
**Bước 4 — Translation:** Chỉ dịch khi source đã xác minh và status = TRANSLATION_READY. Dịch theo paragraph hoàn chỉnh. Tuân thủ Style Guide Phan B v2.3 + Grammar Engine v2.1 (7 bước, S1-S20, P1-P10, C1-C10). Checkpoint lưu tiến độ.
**Bước 5 — QA và DOCX:** Đối chiếu source ↔ translation. Chạy Quality Gate 8 tiêu chí. Xuất DOCX có footnote chân trang.

**Nguyên cấm:**
- Không được dịch khi source chưa hoàn chỉnh.
- Không dịch khi chưa có checkpoint.
- Không dịch song song nhiều chương.
- **Tuyệt đối không dịch trực tiếp văn bản OCR theo từng trang PDF.**
- **Không sửa hoặc ghi đè bản dịch hiện tại khi chưa có backup và mapping sang source v2.**

## 3. CRITICAL RULE — PARAGRAPH RECONSTRUCTION BEFORE TRANSLATION

Mỗi paragraph có thể bắt đầu ở cuối trang trước và kết thúc ở trang sau. Phải nhận diện và nối tất cả các phần thuộc cùng paragraph thành một đoạn hoàn chỉnh trước khi dịch.

### 3.1 Cách nối đoạn

1. Đọc nội dung OCR của các trang liên tiếp.
2. Xác định paragraph tiếp tục từ trang trước sang trang sau.
3. Nối đúng vị trí, giữ nguyên thứ tự câu và nội dung.
4. Khôi phục từ bị ngắt ở cuối dòng hoặc cuối trang.
5. Phân biệt dấu ngắt dòng với dấu kết thúc paragraph.
6. Không nối hai paragraph khác nhau.
7. Không tự thêm, xóa hoặc viết lại nội dung nguyên tác.
8. Giữ lại page reference để truy xuất nguồn gốc.

### 3.2 Reconstruction status

Mỗi chương phải có hai trạng thái độc lập:

| Status | Ý nghĩa |
|--------|---------|
| `RECONSTRUCTION_PENDING` | Chưa ricostruzione hoặc chưa hoàn thành |
| `RECONSTRUCTION_VERIFIED` | Toàn bộ source đã qua kiểm tra, không thiếu, trùng, sai thứ tự |
| `TRANSLATION_READY` | Được phép bắt đầu dịch |

Chỉ khi toàn bộ source đã qua kiểm tra mới được chuyển sang `TRANSLATION_READY`. Các trường hợp không chắc chắn phải đánh dấu `REVIEW_REQUIRED`.

### 3.3 Quality Gate trước khi dịch (7 tiêu chí — tất cả phải PASS)

1. Paragraph xuyên trang đã được nối đúng.
2. Không còn paragraph bị chia thành các mảnh OCR độc lập.
3. Không nối nhầm hai paragraph.
4. Không mất hoặc trùng câu.
5. Thứ tự nội dung khớp PDF.
6. Footnote và heading được nhận diện riêng.
7. Có thể truy xuất từng paragraph về trang PDF gốc.

### 3.4 Báo cáo trước khi dịch

Trước khi bắt đầu dịch từng chương, bắt buộc tạo báo cáo:

- Các đoạn đã nối (page→page, paragraph ID)
- Các đoạn cần kiểm tra (REVIEW_REQUIRED)
- Kết quả đối chiếu source với PDF

Báo cáo lưu tại: `05_qa/chXX_reconstruction_report.md`

**Quy trình thực thi:** OCR → RECONSTRUCT → VERIFY → FREEZE SOURCE → TRANSLATE. Không được vừa OCR vừa dịch. Không được dịch khi reconstruction chưa hoàn thành. Không được bỏ qua bước xác minh chỉ để tăng tốc tiến độ.

## 4. CHAPTER STATUS MATRIX

| # | Section | PDF Pages | Src v1 | Src v2 | Reconstruction | Trans v1 | Trans v2 | QA | DOCX | Status |
|---|---------|-----------|--------|--------|----------------|----------|----------|----|------|--------|
| 0 | Front Matter | 1-7 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | HOAN_TAT |
| 1 | Preface First Edition | 8-10 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | HOAN_TAT |
| 2 | Preface Part One | 11-16 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | HOAN_TAT |
| 3 | Preface Part Two | 17-22 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | HOAN_TAT |
| 4 | Preface Part Three | 23-41 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | HOAN_TAT |
| 5 | Part One Intro | 42-47 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | HOAN_TAT |
| 6 | Ch01 | 48-55 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | needs_reprocess |
| 7 | Ch02 | 56-98 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | needs_reprocess |
| 8 | Ch03 | 99-133 | ✅ | ✅ | VERIFIED | ✅ | — | ❌ | ❌ | needs_reprocess |
| 9 | Ch04 | 134-167 | ✅ | ✅ (34P) | VERIFIED | ✅ (consolidated) | 🔄 P001-P023 done, P024-P034 pending | ❌ | ❌ | translating |
| 10 | Ch05 | 168-202 | ✅ | ✅ (37P) | VERIFIED | ✅ (consolidated) | — | ❌ | ❌ | needs_reprocess |
| 11 | Ch06 | 203-229 | ✅ | ✅ (29P) | VERIFIED | ✅ (consolidated) | — | ❌ | ❌ | needs_reprocess |
| 12 | Ch07 | 230-266 | ✅ | ✅ (39P) | VERIFIED | ✅ (consolidated) | — | ❌ | ❌ | needs_reprocess |
| 13 | Ch08 | 267-311 | ✅ | ✅ (44P) | VERIFIED | ✅ (consolidated) | — | ❌ | ❌ | needs_reprocess |
| 14 | Ch09 | 312-349 | ✅ | ✅ (36P) | VERIFIED | ✅ (consolidated) | — | ❌ | ❌ | needs_reprocess |
| 15 | Ch10 | 350-387 | ✅ | ✅ (37P) | VERIFIED | ✅ (consolidated) | — | ❌ | ❌ | needs_reprocess |
| 16 | Ch11 | 388-433 | ✅ | ✅ (43P) | VERIFIED | ✅ (consolidated) | — | ❌ | ❌ | needs_reprocess |
| 17 | Ch12 | 434-504 | ✅ | ✅ (71P) | VERIFIED | ⚠️ _p1,_p2 only | — | ❌ | ❌ | pending |
| 18 | Ch13 | 505-574 | ✅ | ✅ (61P) | VERIFIED | ❌ none | — | ❌ | ❌ | pending |

**Legend:** ✅ = done, ⚠️ = partial, ❌ = not started, — = not applicable, 🔄 = in progress, needs_reprocess = đã dịch nhưng cần xử lý lại cắt đoạn + mapping sang v2

## 5. EXECUTION ROADMAP

### Phase A — Audit & Map Existing Work (ch01–ch11)

| Step | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| A1 | Verify v2 src files exist for all chapters (ch01–ch13) | Plan agent | reconstruction_report.json already exists |
| A2 | Map v1 translation parts → v2 src paragraph IDs for ch01–ch11 | Plan agent | Mapping table (no file changes) |
| A3 | Verify v1 consolidated files exist: ch04–ch11 v1_chXX_vi.txt | Plan agent | File listing confirmed |
| A4 | Identify gaps: ch12 only _p1,_p2; ch13 no translation dir | Plan agent | Gap report |

### Phase B — Complete Ch04 v2 (currently in progress)

| Step | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| B1 | Extract src P024-P034 from `02_extracted_text/v2/ch04_src.txt` | Implementation agent | Source text P024-P034 |
| B2 | Translate P024-P034 (VNCH + Grammar Engine 7-step) | Implementation agent | Updated v1_ch04_vi.txt |
| B3 | Update checkpoint.json after each paragraph | Implementation agent | checkpoint.json |
| B4 | Port footnotes for P024-P034 (from v1 translation) | Implementation agent | Footnote definitions |
| B5 | Run QA: paragraph alignment (src=vi), footnote alignment, orthography, encoding | Implementation agent | QA report |
| B6 | Build DOCX for ch04 | Implementation agent | `09_docx/V1-C04_dreyfus-affair.docx` |
| B7 | Mark ch04 HOAN_TAT in progress.json | Implementation agent | progress.json |

### Phase C — Re-process Already-Translated Chapters (ch01–ch03, ch05–ch11)

**Mục tiêu:** Xem xét lại cắt đoạn paragraph của các chương đã dịch v1, mapping sang source v2, xử lý lại phần cắt đoạn và bản dịch nếu lệch. Không ghi đè bản dịch hiện tại trước khi đã backup và mapping.

| Step | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| C1 | Create backup of all v1 translation files (ch01-ch03, ch05-ch11) | Implementation agent | `backup_$(date)/` |
| C2 | For each chapter: compare v1 paragraph segmentation vs v2 src paragraph IDs | Implementation agent | Segmentation diff report per chapter |
| C3 | Map each v1 translated paragraph → v2 src paragraph ID (1-to-1 where possible) | Implementation agent | Mapping table per chapter |
| C4 | Identify paragraphs where v1 segmentation ≠ v2 segmentation (split/merge) | Implementation agent | List of REVIEW_REQUIRED paragraphs |
| C5 | Re-align translation: re-segment v1 translation to match v2 paragraph boundaries | Implementation agent | Re-aligned v1 translation files |
| C6 | Re-translate any paragraphs that were split/merged and lost alignment | Implementation agent | Updated translation segments |
| C7 | Verify paragraph count: src count = vi count for each chapter | Implementation agent | Alignment verification report |
| C8 | Update status: needs_reprocess → translating_done | Implementation agent | progress.json |

### Phase D — Complete Ch12 (pending, partial parts exist)

| Step | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| D1 | Verify v2 src ch12: 71 paragraphs, pages 434-504 | Plan agent | Already in reconstruction_report.json |
| D2 | Translate remaining parts (_p3-_p8, _p6b) using v2 src as reference | Implementation agent | v1 translation parts |
| D3 | Consolidate ch12 parts into v1_ch12_vi.txt | Implementation agent | Consolidated file |
| D4 | Run QA (alignment, footnotes, orthography, encoding) | Implementation agent | QA report |
| D5 | Build DOCX for ch12 | Implementation agent | `09_docx/V1-C12_totalitarianism-in-power.docx` |
| D6 | Mark ch12 HOAN_TAT in progress.json | Implementation agent | progress.json |

### Phase E — Complete Ch13 (pending, no translation exists)

| Step | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| E1 | Verify v2 src ch13: 61 paragraphs, pages 505-574 | Plan agent | Already in reconstruction_report.json |
| E2 | Translate all 61 paragraphs (VNCH + Grammar Engine 7-step) | Implementation agent | v1 translation parts + consolidated |
| E3 | Port/create footnotes for ch13 | Implementation agent | Footnote definitions |
| E4 | Run QA (alignment, footnotes, orthography, encoding) | Implementation agent | QA report |
| E5 | Build DOCX for ch13 | Implementation agent | `09_docx/V1-C13_ideology-and-terror.docx` |
| E6 | Mark ch13 HOAN_TAT in progress.json | Implementation agent | progress.json |

### Phase F — QA & DOCX for All Chapters (ch01–ch13)

| Step | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| F1 | For each chapter ch01-ch13: run debug_align.py (src=vi paragraph count) | Implementation agent | Alignment report |
| F2 | Fix any alignment issues found | Implementation agent | Realigned files |
| F3 | Run apply_vnch_fixes.py (VNCH orthography normalization) | Implementation agent | Fixed files |
| F4 | Verify footnotes: src count = vi count, sequential 1..N | Implementation agent | Footnote report |
| F5 | Build DOCX for each chapter (ch01-ch13) | Implementation agent | 13 DOCX files in 09_docx/ |
| F6 | Word COM check: Footnotes.Count = progress.json notes | Implementation agent | Verification report |
| F7 | Quality Gate 8 tiêu chí PASS → mark HOAN_TAT | Implementation agent | progress.json updated |

### Phase G — Final Consolidation

| Step | Action | Owner | Deliverable |
|------|--------|-------|-------------|
| G1 | Verify all 18 sections HOAN_TAT | Plan agent | Final progress.json |
| G2 | Generate master DOCX (full book) | Implementation agent | `09_docx/V1-Origins-of-Totalitarianism.docx` |
| G3 | Archive and backup | Implementation agent | Backup directory |

## 6. FILE STRUCTURE CONVENTIONS

```
translation-project-arendt/
├── 00_plan/
│   ├── progress.json              # Progress tracker (source of truth)
│   └── TRANSLATION_PLAN.md        # High-level plan
├── 02_extracted_text/
│   ├── v1/                        # Raw OCR by page: chXX.txt
│   └── v2/                        # Reconstructed source: chXX_src.txt + reconstruction_report.json
├── 03_terminology/
│   └── ARENDT_TERMINOLOGY.md      # Terminology source of truth
├── 04_translation/
│   ├── v1/                        # Consolidated translations: chXX/v1_chXX_vi.txt + _pN.txt parts
│   └── v2/                        # In-progress translations: ch04/v1_ch04_vi.txt + checkpoint.json
├── 05_qa/                         # QA reports + per-chapter reconstruction reports
│   └── chXX_reconstruction_report.md  # Báo cáo nối đoạn trước khi dịch
├── 07_style_guide/
│   ├── STYLE_GUIDE_PHAN_B.md      # 29 rules v2.3
│   ├── STYLE_GUIDE.md
│   ├── TERMINOLOGY_TABLE_BY_DOMAIN.md
│   └── TRANSLATION_GRAMMAR_ENGINE.md  # 7-step process, S1-S20, P1-P10, C1-C10
├── 08_southern_vietnamese_library/ # Empty - reserved
├── 09_docx/                       # Empty - DOCX output (to be filled)
└── 99_scripts/
    ├── ocr_reconstruct.py         # V1→V2 reconstruction
    ├── extract_chapters.py        # PDF extraction
    ├── consolidate_ch04.py        # Ch04 consolidation
    ├── consolidate_ch07.py        # Ch07 consolidation + QA
    ├── fix_ch07_orthography.py    # VNCH orthography fixes
    ├── fix_ch07_connectives.py    # VNCH connective fixes
    └── verify_ch07.py             # Footnote + English leftover QA
```

**Missing scripts (need to be created):**
- `debug_align.py` — paragraph alignment check (src=vi)
- `apply_vnch_fixes.py` — VNCH orthography normalization
- `build_chapter_docx.py` — DOCX builder with footnotes
- `map_v1_to_v2.py` — Map v1 translation paragraphs → v2 src paragraph IDs

## 7. QUALITY STANDARDS

### VNCH Rules (Style Guide Phan B v2.3, 29 rules)
- Rule 1-17: Vocabulary, orthography, terminology
- Rule 18: Alignment (src paragraphs = vi paragraphs) — BẮT BUỘC
- Rule 19: Cấm dịch từng từ (word-for-word) — CẤM KỊ
- Rule 20: Xử lý từ/câu khó — 5 bước bắt buộc
- Rule 21-26: VNCH Grammar (chỉ định, trạng từ, thể, đại từ, từ nối, chủ động hóa)
- Rule 27: Chống fabricate
- Rule 28: Encoding (UTF-8, NFC, no BOM, LF)
- Rule 29: Quality Gate 8 tiêu chí

### Quality Gate (8 criteria — all must PASS before HOAN_TAT)
1. Encoding: UTF-8/NFC/no BOM/LF
2. Orthography: 0× non-VNCH terms (chính trị→chánh trị, này→nầy, etc.)
3. Paragraph alignment: src = vi
4. Footnote alignment: src = vi
5. No fabricate
6. Natural VNCH style, no word-for-word
7. DOCX exists in 09_docx/
8. DOCX footnotes: OK N/N, Word Footnotes.Count = notes in progress.json

### Grammar Engine 7-Step Process
1. Phân tích ngữ pháp nguyên tác
2. Xác định chủ thể, vị ngữ, đối tượng
3. Phân tích quan hệ logic
4. Xác định thuật ngữ theo ngữ cảnh
5. Tái cấu trúc câu tiếng Việt tự nhiên (VNCH)
6. Đối chiếu lại nguyên tác
7. Kiểm tra tính dễ hiểu

## 8. PROGRESS TRACKING (progress.json)

Status values: `pending` → `translating` → `translating_done` → `qa_pending` → `qa_done` → `docx_built` → `HOAN_TAT`
Additional: `needs_reprocess` (đã dịch nhưng cần xử lý lại cắt đoạn + mapping sang v2)

Reconstruction status values: `RECONSTRUCTION_PENDING` → `RECONSTRUCTION_VERIFIED` → `TRANSLATION_READY`

The `progress.json` at `00_plan/progress.json` is the source of truth. It must be updated after:
- Each paragraph translated (checkpoint.json for in-progress chapter)
- Each chapter re-processed (mapping + alignment)
- Each chapter QA passed
- Each chapter DOCX built
- Each chapter marked HOAN_TAT

## 9. SEQUENCING RULES

1. **Chapters must be done sequentially:** ch04 → ch05 → ... → ch13 (no skipping for new translation)
2. **No translation without verified source:** Bước 3 must complete before Bước 4; reconstruction status must be `RECONSTRUCTION_VERIFIED` before translation
3. **No QA without complete translation:** All paragraphs must be translated before QA
4. **No DOCX without QA pass:** Quality Gate must pass before DOCX build
5. **No HOAN_TAT without all 8 Quality Gate criteria PASS**
6. **Existing translations (ch01-ch11 v1) must not be modified without backup and mapping to v2 source**
7. **ch04 v2 is the active translation — continue from checkpoint.json (next_para=V1C04-P024)**
8. **Báo cáo nối đoạn phải tạo trước khi dịch mỗi chương** (`05_qa/chXX_reconstruction_report.md`)
9. **Re-process phase (C) must complete before QA phase (F) for ch01-ch03, ch05-ch11**

## 10. RISKS & MITIGATION

| Risk | Mitigation |
|------|------------|
| ch12 only has _p1,_p2 parts (incomplete) | Translate remaining parts using v2 src as reference, then consolidate |
| ch13 has no translation at all | Full pipeline: translate all 61 paragraphs from v2 src |
| v1 segmentation ≠ v2 segmentation for ch01-ch11 | Phase C: re-align using mapping table, re-translate split/merged paragraphs |
| No DOCX build script exists | Create `build_chapter_docx.py` before Phase F |
| No debug_align.py exists | Create `debug_align.py` for paragraph alignment verification |
| Footnotes missing for ch04 P024-P034 | Port from v1 translation parts |
| Alignment drift between v1 and v2 | Run debug_align.py before QA, realign if needed |
| Encoding issues on Windows (PowerShell heredoc) | Use Python scripts for file I/O with encoding="utf-8", newline="\n" |
| Accidental overwrite of v1 translation without backup | Phase C1: mandatory backup before any modification |

## 11. DELIVERABLES

| File | Location | Description |
|------|----------|-------------|
| MASTER_TRANSLATION_PLAN | `.kilo/plans/1795599198678-master-translation-plan-ch1-13.md` | This file |
| CHAPTER_STATUS_MATRIX | Section 4 of this plan | Status of all 18 sections |
| EXECUTION_ROADMAP | Section 5 of this plan | Step-by-step execution order |
| progress.json | `00_plan/progress.json` | Progress tracker (updated during execution) |
| QA reports | `05_qa/` | Per-chapter QA reports |
| Reconstruction reports | `05_qa/chXX_reconstruction_report.md` | Báo cáo nối đoạn trước khi dịch |
| Mapping tables | `05_qa/chXX_v1_to_v2_mapping.md` | Mapping v1 translation → v2 src paragraph IDs |
| Backup | `backup_$(date)/` | Backup of all v1 translation files before re-process |
| DOCX files | `09_docx/` | Per-chapter DOCX with footnotes |

## 12. IMMEDIATE NEXT STEPS

1. **Complete ch04 v2:** Translate P024-P034 from `02_extracted_text/v2/ch04_src.txt`, update checkpoint.json, port footnotes
2. **Create missing scripts:** `debug_align.py`, `apply_vnch_fixes.py`, `build_chapter_docx.py`, `map_v1_to_v2.py`
3. **Phase C — Re-process ch01-ch03, ch05-ch11:** Backup v1 files, audit segmentation vs v2, map v1→v2 paragraph IDs, re-align, re-translate split/merged paragraphs
4. **Complete ch12:** Translate remaining parts, consolidate, QA, DOCX
5. **Complete ch13:** Full translation pipeline, QA, DOCX
6. **Phase F — QA + DOCX for all chapters:** Alignment check, VNCH fixes, footnote verify, DOCX build
7. **Final:** Mark all chapters HOAN_TAT, generate master DOCX
