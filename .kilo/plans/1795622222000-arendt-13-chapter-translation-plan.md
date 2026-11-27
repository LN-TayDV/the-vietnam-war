# Arendt Translation Plan — 13 Chapters from Meridian 1962 v7 Source

## Goal
Produce 13 complete, error-free DOCX files (Vietnamese, VNCH pre-1975 Southern) from Meridian 1962 v7 Source TXT, following the translation-workflow SKILL.md workflow. All 8 Quality Gate criteria must PASS per chapter before DOCX build.

## Project Context
- **Book**: The Origins of Totalitarianism — Hannah Arendt
- **Source PDF**: `books/hannah-arendt-the-origins-of-totalitarianism-meridian-1962.pdf` (552 pages)
- **Source TXT**: `02_extracted_text/v7/v2_*_src.txt` (14 files: front_matter + ch01-ch13)
- **Format**: `[V7-CH-PNNN] (trang Y) [chapter_heading|body|footnote]` — UTF-8, NFC, LF
- **Target**: Vietnamese (VNCH pre-1975 Southern), 13 chapter DOCX + MASTER DOCX
- **Reference skill**: `.kilo/skills/translation-workflow/SKILL.md`
- **Style guide**: `translation-project-arendt/08_southern_vietnamese_library/07_style_guide/STYLE_GUIDE_PHAN_B.md`
- **Terminology**: `translation-project-arendt/03_terminology/ARENDT_TERMINOLOGY.md`

## Current State (as of v7 extraction)
| Item | Status |
|------|--------|
| v7 Source extraction (all 13 chapters + front_matter) | COMPLETE — 2,265 paragraphs |
| Quality Gate extraction (8 criteria) | 7/8 PASS (criterion 2 = source OCR artifacts, not extraction bugs) |
| Translation files | NEED TO BE CREATED from v7 source |
| Existing translations (1973 HBJ-based) | `04_translation/v2/chXX/v1_chXX_vi.txt` — NOT compatible with v7 page numbering |
| DOCX files | Exist in `09_docx/` but progress.json shows `docx_status: pending` |
| progress.json | All chapters at `structure_verified`, checkpoint 1 |

## Critical Issue — Source Mismatch
- v7 source uses Meridian 1962 page numbers (ch01: p23-30, ch02: p31-74, etc.)
- Existing translation files use HBJ 1973 page numbers (ch01: p48-55, ch02: p56-98, etc.)
- v7 paragraph IDs: `[V7-CH-PNNN]`; existing translation IDs: `[V1Cxx-PNNN]`
- **Decision**: Use v7 source as source of truth. Existing HBJ translations cannot be directly mapped due to page/ID mismatch. All 13 chapters need translation from v7 source.

## Plan — 4 Phases

### Phase 0: Preparation (one-time)
1. Read `STYLE_GUIDE_PHAN_B.md` (v2.3, 29 rules) — required before any translation
2. Read `ARENDT_TERMINOLOGY.md` — core terminology source of truth
3. Read `TRANSLATION_GRAMMAR_ENGINE.md` — 7-step translation process
4. Set up output directory structure: `04_translation/v2/chXX/` for each chapter
5. Verify all 14 v7 source TXT files are readable and UTF-8/NFC/LF

### Phase 1: Translation (per chapter, chapters 01-13 + front_matter)
For each chapter, execute the 7-step Grammar Engine process:

1. **Read source** — Open `02_extracted_text/v7/v2_chXX_src.txt`, note paragraph count, pages, footnote count
2. **Parse paragraphs** — Extract `[V7-CH-PNNN] (trang Y) [type]` blocks; separate body, footnote, chapter_heading
3. **Translate each paragraph** (7 steps):
   - Step 1: Phân tích ngữ pháp nguyên tác (chủ thể, vị ngữ, đối tượng, quan hệ logic)
   - Step 2: Xác định chủ thể, vị ngữ, đối tượng; chuyển bị động → chủ động
   - Step 3: Phân tích quan hệ logic; dùng từ nối VNCH (dầu, trái lại, tuy vậy, bởi thế, vả)
   - Step 4: Xác định thuật ngữ theo ARENDT_TERMINOLOGY.md + VNCH Grammar Database
   - Step 5: Tái cấu trúc câu tiếng Việt tự nhiên (VNCH), không dịch từng từ
   - Step 6: Đối chiếu lại nguyên tác (số câu, thông tin, thuật ngữ, cước chú)
   - Step 7: Kiểm tra dễ hiểu (hiểu ngay lần đầu)
4. **VLP-01 (Tiếng Việt trước)** — Dịch nghĩa sang tiếng Việt trước; giữ ngoại ngữ chỉ khi có lý do ngôn học rõ ràng (nhóm A/B/C/D)
5. **Create files**:
   - `04_translation/v2/chXX/v1_chXX_src.txt` — source copy with v7 paragraph IDs
   - `04_translation/v2/chXX/v1_chXX_vi.txt` — translated text with same paragraph markers
6. **Footnotes** — Add `=== FOOTNOTES ===` block with footnote definitions; ensure inline markers match footnote numbers 1..N

### Phase 2: Quality Gate (8 criteria, per chapter — ALL MUST PASS)
Run in sequence for each chapter:

| # | Criteria | Script/Method | PASS Condition |
|---|----------|---------------|----------------|
| 1 | Encoding | `encoding_checker.py` | UTF-8, NFC, no BOM, LF |
| 2 | Orthography | `vnch_orthography.py` | 0 critical/major VNCH violations |
| 3 | Paragraph alignment | `document_comparator.py` | src paragraphs = vi paragraphs (1-1 marker match) |
| 4 | Footnote alignment | `check_footnote_markers.py` | 0 missing, 0 duplicate, 0 orphan |
| 5 | No fabricate | Manual review + `translation_validator.py` | All claims traceable to source |
| 6 | Natural VNCH style | Deep Translation Review (S1-S20, P1-P10) | No word-for-word, no foreign-language calques |
| 7 | DOCX exists | `docx_builder.py` build | File exists in `09_docx/` |
| 8 | DOCX footnotes | Word COM: `Footnotes.Count` = notes count | N/N match, 9pt, hanging indent 0.4cm, placement correct |

If any criterion FAILs → fix source TXT → re-run all 8 criteria from start.

### Phase 3: DOCX Build (per chapter)
1. Run `99_scripts/build_chapter_docx.py chXX` (Arendt-specific builder)
2. Verify output: `09_docx/V2-XX_<slug>.docx` exists
3. Run Word COM verification: `Footnotes.Count` matches progress.json notes count
4. Run `audit_docx_format.py XX` — validate heading/body/quote/footnote formatting
5. If FAIL → fix TXT → rebuild

### Phase 4: Finalization
1. Update `progress.json`: set each chapter `status: "HOAN_TAT"`, `docx_status: "DONE"`
2. Build MASTER DOCX: `99_scripts/build_master_docx_v2.py` (combine all 13 chapters)
3. Verify MASTER DOCX: all 13 chapters present, footnotes continuous
4. Final progress report: 13/13 chapters HOAN_TAT

## File Paths

| Purpose | Path |
|---------|------|
| v7 Source TXT | `translation-project-arendt/02_extracted_text/v7/v2_chXX_src.txt` |
| Translation source | `translation-project-arendt/04_translation/v2/chXX/v1_chXX_src.txt` |
| Translation Vietnamese | `translation-project-arendt/04_translation/v2/chXX/v1_chXX_vi.txt` |
| Output DOCX | `translation-project-arendt/09_docx/V2-XX_<slug>.docx` |
| Progress checkpoint | `translation-project-arendt/00_plan/progress.json` |
| Style guide | `translation-project-arendt/08_southern_vietnamese_library/07_style_guide/STYLE_GUIDE_PHAN_B.md` |
| Terminology | `translation-project-arendt/03_terminology/ARENDT_TERMINOLOGY.md` |
| Build script | `translation-project-arendt/99_scripts/build_chapter_docx.py` |
| Common scripts | `.kilo/scripts/common/` (encoding_checker, vnch_orthography, document_comparator, quality_gate, docx_builder) |

## Chapter Order (recommended)
Start with shorter chapters to validate the pipeline, then proceed to longer ones:

1. front_matter (pages 1-7, ~74 paragraphs)
2. ch01 (pages 23-30, ~37 paragraphs)
3. ch06 (pages 179-204, ~110 paragraphs)
4. ch04 (pages 109-141, ~155 paragraphs)
5. ch09 (pages 287-323, ~142 paragraphs)
6. ch02 (pages 31-74, ~181 paragraphs)
7. ch03 (pages 75-108, ~165 paragraphs)
8. ch05 (pages 143-178, ~177 paragraphs)
9. ch07 (pages 205-242, ~177 paragraphs)
10. ch08 (pages 243-286, ~188 paragraphs)
11. ch10 (pages 325-360, ~148 paragraphs)
12. ch13 (pages 481-552, ~246 paragraphs)
13. ch12 (pages 409-480, ~279 paragraphs — longest)

## Validation Checklist (per chapter)
- [ ] Source TXT readable, UTF-8/NFC/LF
- [ ] Translation file created with matching paragraph markers
- [ ] VLP-01 applied (no unnecessary foreign words)
- [ ] Encoding check PASS
- [ ] Orthography check PASS
- [ ] Paragraph alignment PASS (src = vi)
- [ ] Footnote alignment PASS (0 missing/duplicate/orphan)
- [ ] No fabricate PASS
- [ ] Natural VNCH style PASS (Deep Review)
- [ ] DOCX built successfully
- [ ] Word COM Footnotes.Count = notes count
- [ ] `audit_docx_format.py` PASS
- [ ] progress.json updated to HOAN_TAT

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| v7 source has OCR artifacts (equaHty, poHtical, etc.) | Fix common patterns in extraction (U→l between lowercase); remaining artifacts noted for translator awareness |
| Page numbering mismatch (Meridian 1962 vs HBJ 1973) | Use v7 page numbers exclusively; do not attempt to map to HBJ translations |
| Footnote markers missing in translation | Run `check_footnote_markers.py` before DOCX build; fix TXT if FAIL |
| Builder incompatibility (v7 format vs build script expectations) | Ensure translation file uses `[V1Cxx-PNNN] (trang Y)` format expected by `build_chapter_docx.py` |
| Chapter 12 is longest (~279 paragraphs) | Schedule last; allocate extra time |

## Success Criteria
- [ ] 13/13 chapters translated from v7 Source TXT
- [ ] 13/13 chapters pass all 8 Quality Gate criteria
- [ ] 13/13 DOCX files built in `09_docx/`
- [ ] Word COM Footnotes.Count matches progress.json for each chapter
- [ ] MASTER DOCX built with all 13 chapters
- [ ] progress.json: all chapters `status: "HOAN_TAT"`, `docx_status: "DONE"`