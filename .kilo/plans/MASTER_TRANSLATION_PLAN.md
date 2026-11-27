# EXECUTION PLAN — FIX FOREIGN LANGUAGE REMNANTS & COMPLETE 13 CHAPTERS (V1-C01 to V1-C13)

## 1. CURRENT STATE (verified by reading source files)

### 1.1 Project structure
- **Project root:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project`
- **Source PDF:** `books/The_Cambridge_History_of_the_Vietnam_War.pdf` (1866 pages, text layer)
- **Extracted text:** `02_extracted_text/v1/ch01.txt` … `ch21.txt` (V1, 21 chapters)
- **Translation files:** `04_translation/v1/ch01/` … `ch15/` (each has `v1_chXX_src.txt` + `v1_chXX_vi.txt`)
- **Scripts:** `99_scripts/` (workspace root), `.kilo/scripts/common/` (shared)
- **Standards:** `07_style_guide/STYLE_GUIDE_PHAN_B.md` (v2.3), `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` (v2.1), `03_terminology/` (glossary, lexicon, sources)
- **DOCX:** `09_docx/` (partial — some chapters have DOCX, some don't)
- **QA reports:** `05_qa/` (AUDIT_REPORT_CH01-06.md, BUG_REGISTER_V1-C11.md, REVIEW_AUDIT_CH14.md, etc.)

### 1.2 Chapter status (verified)

| Chapter | src exists | vi exists | Content type | Known issues |
|---------|-----------|-----------|--------------|--------------|
| V1-C01 | ✅ | ✅ | **Arendt content** (Antisemitism) — WRONG PROJECT | ISSUE-01: cross-contamination, must re-translate |
| V1-C02 | ✅ | ✅ | **Arendt content** (Jews, nation-state) — WRONG PROJECT | ISSUE-01: cross-contamination, must re-translate |
| V1-C03 | ✅ | ✅ | Vietnam War (Hồ Chí Minh & VCP) | ISSUE-06: alignment + VNCH terms (222 fixes) |
| V1-C04 | ✅ | ✅ | Vietnam War (Indochina WWII) | ISSUE-06: alignment + VNCH terms |
| V1-C05 | ✅ | ✅ | Vietnam War (August Revolution 1945) | ISSUE-06: alignment + VNCH terms |
| V1-C06 | ✅ | ✅ | Vietnam War (Birth of DRVN) | ISSUE-06: alignment + VNCH terms |
| V1-C07 | ✅ | ✅ | Vietnam War (France's Indochina War) | VNCH calque, foreign remnants |
| V1-C08 | ✅ | ✅ | Vietnam War (China & French Indochina War) | ISSUE-05: "nässig" → "này" (28×, fixed) |
| V1-C09 | ✅ | ✅ | Vietnam War (French Indochina War in Central Highlands) | Footnote markers missing (14×) |
| V1-C10 | ✅ | ✅ | Vietnam War (French Indochina War in Northern Vietnam) | Only P001-P011 translated, P012+ missing |
| V1-C11 | ✅ | ✅ | Vietnam War (Battle of Điện Biên Phủ) | ISSUE-02: missing 21 footnotes (BUG-008) |
| V1-C12 | ✅ | ✅ | Vietnam War (Geneva Conference 1954) | ISSUE-03: missing 42 markers, duplicate [20] (BUG-001, BUG-003, BUG-009) |
| V1-C13 | ✅ | ✅ | Vietnam War (Eisenhower and Vietnam) | Calque errors, foreign remnants |

### 1.3 Known issues from prior work

| Issue | Chapters | Severity | Source |
|-------|----------|----------|--------|
| ISSUE-01: Cross-contamination (Arendt content in V1-C01, V1-C02) | C01, C02 | CRITICAL | Direct file inspection |
| ISSUE-02: Missing 21 footnotes | C11 | CRITICAL | BUG_REGISTER_V1-C11.md |
| ISSUE-03: Missing 42 footnote markers, duplicate [20] | C12 | CRITICAL | BUG-001, BUG-003, BUG-009 |
| ISSUE-04: Was machine translation placeholder, rewritten | C14 | MAJOR | REVIEW_AUDIT_CH14.md |
| ISSUE-05: "nässig" used 28× as "này" | C08 | MAJOR | LANGUAGE_PURITY_REVIEW_V1-C08.md |
| ISSUE-06: Alignment + VNCH term errors (222 fixes) | C01-C06 | MAJOR | AUDIT_REPORT_CH01-06.md |
| ISSUE-07: progress.json references Arendt book | All | CRITICAL | progress.json inspection |
| ISSUE-08: Foreign language remnants (EN/FR/DE/etc.) in vi files | All | MAJOR | User report |
| ISSUE-09: Duplicate chapter titles, running headers in body | All | MAJOR | User report |
| ISSUE-10: Missing paragraphs (P012+ in C10) | C10 | CRITICAL | SKILL.md §11 |
| ISSUE-11: Footnote markers missing (14× in C09) | C09 | MAJOR | SKILL.md §8A.2 |

### 1.4 Foreign language remnants (verified by reading vi files)

From direct inspection of `v1_ch02_vi.txt`:
- German "Böhmisch" mixed into Vietnamese: "giomot", "đằng sau", "đằng sau", "Müller", "Müller"
- Korean characters: "봉 phong" (fengjian) instead of "phong kiến"
- French/English terms: "múltiples", "múlti", "doubt", "giomot"
- Calque errors: "Việt Nam Nam" (instead of "Nam Việt Nam"), "Châu Á" (instead of "Á Châu"), "Châu Âu" (instead of "Âu Châu")
- Machine translation artifacts: "giomot", "Müller", "Müller", "dobrovol'", " dobровol'"

From direct inspection of `v1_ch13_vi.txt`:
- "Việt Nam Nam" appears (should be "Nam Việt Nam" or "Việt Nam Cộng Hòa")
- "Hàn Quốc Nam" (should be "Nam Hàn")
- "Châu Á" (should be "Á Châu")
- "Châu Âu" (should be "Âu Châu")
- "Chiến tranh thế giới thứ hai" (should be "Thế Chiến thứ Hai")
- "Cộng Hòa Dân Chủ Việt Nam" (should be "Việt Nam Dân Chủ Cộng Hòa")

### 1.5 Pipeline issues identified

| Pipeline stage | Issue | Root cause | Fix approach |
|---------------|-------|------------|--------------|
| OCR extraction | Running headers and page numbers mixed into body text | No layout-based detection | Add header/footer pattern detection to `extract_chapters.py` |
| Paragraph reconstruction | Paragraphs split across pages not properly joined | Simple line-based joining | Improve reconstruction with page-break detection |
| Source classification | Headings, subheadings, footnotes not distinguished from body | No type classification | Add paragraph type tags (heading/subheading/body/footnote) |
| Translation | Foreign language remnants, calque errors, missing paragraphs | Machine translation artifacts, manual errors | Re-translate affected paragraphs, apply VNCH fixes |
| DOCX builder | Duplicate titles, running headers in body, footnote placement | No deduplication, no header/footer filtering | Fix `build_chapter_docx.py` to filter headers/footers and deduplicate titles |
| Quality gate | Only checks counts, not placement or content quality | Insufficient checks | Enhance `audit_chapter.py` with placement and content checks |

---

## 2. GAP ANALYSIS

### 2.1 What is broken

1. **Cross-contamination (C01-C02):** V1-C01 and V1-C02 contain Arendt content (The Origins of Totalitarianism) instead of Vietnam War content. These must be completely re-translated from `02_extracted_text/v1/ch01.txt` and `ch02.txt`.

2. **Foreign language remnants (C01-C13):** Multiple languages mixed into Vietnamese text:
   - German: "giomot", "dobrovol'", "Müller", "Böhmisch"
   - Korean: "봉 phong" (fengjian)
   - French: "múltiples", "múlti"
   - English: untranslated sentences, calque errors
   - Chinese: Pinyin names not converted to Hán-Việt

3. **Calque errors (C01-C13):** Machine translation artifacts:
   - "Việt Nam Nam" → "Nam Việt Nam" or "Việt Nam Cộng Hòa"
   - "Hàn Quốc Nam" → "Nam Hàn"
   - "Châu Á" → "Á Châu"
   - "Châu Âu" → "Âu Châu"
   - "Chiến tranh thế giới thứ hai" → "Thế Chiến thứ Hai"
   - "Cộng Hòa Dân Chủ Việt Nam" → "Việt Nam Dân Chủ Cộng Hòa"

4. **Missing paragraphs (C10):** Only P001-P011 translated, P012+ missing entirely.

5. **Missing footnotes (C09, C11, C12):**
   - C09: 14 footnote markers missing from body text
   - C11: 21 footnotes missing from notes block
   - C12: 42 footnote markers missing, duplicate [20]

6. **Duplicate titles / running headers (all):** Chapter titles and running headers from PDF pages appear in body text.

7. **Paragraph structure issues (all):** Headings, subheadings, footnotes not properly classified.

8. **DOCX issues (all):** Duplicate titles, running headers in body, footnote placement errors.

### 2.2 What is working

1. **Source extraction:** `02_extracted_text/v1/ch01.txt` … `ch21.txt` exist and contain complete text.
2. **Translation files for C03-C13:** Exist with Vietnam War content (except C01-C02 which have Arendt content).
3. **Style Guide + Grammar Engine:** Complete and verified (v2.3, v2.1).
4. **Terminology:** Glossary, lexicon, sources all present.
5. **Scripts:** `audit_chapter.py`, `build_chapter_docx.py`, `check_footnote_markers.py`, `chapter_workflow.py` all exist.
6. **QA reports:** AUDIT_REPORT_CH01-06.md, BUG_REGISTER_V1-C11.md, REVIEW_AUDIT_CH14.md document known issues.

### 2.3 What needs to be fixed vs. kept

| Component | Status | Action |
|-----------|--------|--------|
| Source extraction (02_extracted_text/v1/) | ✅ Keep | Already complete for C01-C21 |
| Translation src files (v1_chXX_src.txt) | ✅ Keep | Already complete |
| Translation vi files (v1_chXX_vi.txt) | ⚠️ Fix | C01-C02: re-translate; C03-C13: fix foreign remnants, calques, missing paragraphs |
| Style Guide + Grammar Engine | ✅ Keep | Already complete |
| Terminology | ✅ Keep | Already complete |
| audit_chapter.py | ✅ Keep | Already has 5 checks |
| build_chapter_docx.py | ⚠️ Fix | Filter headers/footers, deduplicate titles |
| check_footnote_markers.py | ✅ Keep | Already complete |
| progress.json | ❌ Fix | Currently references Arendt book, must replace |

---

## 3. EXECUTION PHASES

### PHASE 0 — DIAGNOSIS (read-only, no file changes)

**Goal:** Scan all 13 chapters to identify every foreign language remnant, paragraph issue, and DOCX issue.

| Task ID | Task | Scope | Deliverable | Dependency |
|---------|------|-------|-------------|------------|
| P0-01 | Run `audit_chapter.py` on all 13 chapters | C01-C13 | Audit report per chapter (JSON) | None |
| P0-02 | Scan vi files for foreign language remnants (EN/FR/DE/KO/ZH/etc.) | C01-C13 | Foreign remnant report per chapter | None |
| P0-03 | Verify paragraph alignment (src vs vi count) for all 13 chapters | C01-C13 | Alignment report per chapter | None |
| P0-04 | Check footnote markers (missing/duplicate/orphan) for all 13 chapters | C01-C13 | Footnote marker report per chapter | None |
| P0-05 | Check DOCX files for duplicate titles, running headers, footnote placement | C01-C13 | DOCX audit report per chapter | None |
| P0-06 | Verify `02_extracted_text/v1/chXX.txt` matches PDF for all 13 chapters | C01-C13 | Source verification report | None |

**Phase 0 exit criteria:** Complete diagnosis report for all 13 chapters. Every issue documented with location, cause, and fix approach.

---

### PHASE 1 — FIX PIPELINE (source extraction + paragraph reconstruction)

**Goal:** Fix the pipeline so that source text is clean, properly segmented, and classified before translation.

| Task ID | Task | Scope | Deliverable | Dependency |
|---------|------|-------|-------------|------------|
| P1-01 | Add header/footer pattern detection to `extract_chapters.py` | `extract_chapters.py` | Updated script with layout-based header/footer removal | P0 done |
| P1-02 | Add paragraph type classification (heading/subheading/body/footnote) to source reconstruction | `ocr_reconstruct.py` or new script | Classified source files with type tags | P1-01 |
| P1-03 | Fix paragraph reconstruction for cross-page paragraphs | `ocr_reconstruct.py` or new script | Properly joined paragraphs across page breaks | P1-02 |
| P1-04 | Re-extract source for C01-C13 with fixed pipeline | C01-C13 | Clean source files with proper segmentation | P1-03 |
| P1-05 | Verify re-extracted source matches PDF (page provenance, completeness) | C01-C13 | Source verification report | P1-04 |

**Phase 1 exit criteria:** All 13 chapters have clean, properly segmented source text with paragraph type classification and page provenance.

---

### PHASE 2 — TRANSLATE / FIX TRANSLATIONS

**Goal:** Ensure all 13 chapters have complete, accurate Vietnamese translations with no foreign language remnants.

| Task ID | Task | Scope | Deliverable | Dependency |
|---------|------|-------|-------------|------------|
| P2-01 | Re-translate V1-C01 from `02_extracted_text/v1/ch01.txt` (Vietnam War content) | C01 | New `v1_ch01_src.txt` + `v1_ch01_vi.txt` | P1-05 |
| P2-02 | Re-translate V1-C02 from `02_extracted_text/v1/ch02.txt` (Vietnam War content) | C02 | New `v1_ch02_src.txt` + `v1_ch02_vi.txt` | P2-01 |
| P2-03 | Fix foreign language remnants in V1-C03 | C03 | Fixed `v1_ch03_vi.txt` | P1-05 |
| P2-04 | Fix foreign language remnants in V1-C04 | C04 | Fixed `v1_ch04_vi.txt` | P1-05 |
| P2-05 | Fix foreign language remnants in V1-C05 | C05 | Fixed `v1_ch05_vi.txt` | P1-05 |
| P2-06 | Fix foreign language remnants in V1-C06 | C06 | Fixed `v1_ch06_vi.txt` | P1-05 |
| P2-07 | Fix foreign language remnants + VNCH calque in V1-C07 | C07 | Fixed `v1_ch07_vi.txt` | P1-05 |
| P2-08 | Fix foreign language remnants in V1-C08 (verify "nässig" fix) | C08 | Fixed `v1_ch08_vi.txt` | P1-05 |
| P2-09 | Fix missing footnote markers (14×) in V1-C09 | C09 | Fixed `v1_ch09_vi.txt` | P1-05 |
| P2-10 | Translate missing paragraphs (P012+) in V1-C10 | C10 | Complete `v1_ch10_vi.txt` | P1-05 |
| P2-11 | Fix missing 21 footnotes in V1-C11 | C11 | Fixed `v1_ch11_vi.txt` with footnote block | P1-05 |
| P2-12 | Fix missing 42 footnote markers + duplicate [20] in V1-C12 | C12 | Fixed `v1_ch12_vi.txt` | P1-05 |
| P2-13 | Fix foreign language remnants + calque errors in V1-C13 | C13 | Fixed `v1_ch13_vi.txt` | P1-05 |

**Phase 2 exit criteria:** All 13 chapters have complete Vietnamese translations with no foreign language remnants (except proper nouns, quotes, and terms that must be kept in original language).

---

### PHASE 3 — EDITORIAL REVIEW

**Goal:** Apply VNCH orthography rules, fix calque errors, standardize terminology.

| Task ID | Task | Scope | Deliverable | Dependency |
|---------|------|-------|-------------|------------|
| P3-01 | Run `vnch_orthography.py` on all 13 chapters, fix all CRITICAL/MAJOR issues | C01-C13 | Fixed files | P2 done |
| P3-02 | Fix VNCH calque errors (Việt Nam Nam, Hàn Quốc Nam, Châu Á, Châu Âu, etc.) | C01-C13 | Fixed files | P3-01 |
| P3-03 | Standardize terminology across all 13 chapters (check glossary consistency) | C01-C13 | Terminology consistency report | P3-02 |
| P3-04 | Apply VLP-01 (Vietnamese-first translation) sentence-level check | C01-C13 | VLP-01 compliance report | P3-03 |
| P3-05 | Convert Pinyin Chinese names to Hán-Việt (§13 of SKILL) | C01-C13 | Fixed files | P3-04 |

**Phase 3 exit criteria:** All 13 chapters pass VNCH orthography check, VLP-01 sentence-level check, and terminology consistency check.

---

### PHASE 4 — SOURCE COMPARISON

**Goal:** Verify every translation paragraph matches the source paragraph (1:1 alignment, no missing/added content).

| Task ID | Task | Scope | Deliverable | Dependency |
|---------|------|-------|-------------|------------|
| P4-01 | Run `document_comparator.py` on all 13 chapters | C01-C13 | Alignment reports | P3 done |
| P4-02 | Fix any alignment issues (missing/extra paragraphs) | C01-C13 | Fixed files | P4-01 |
| P4-03 | Run `audit_chapter.py` on all 13 chapters | C01-C13 | Audit reports (0 errors) | P4-02 |
| P4-04 | Run `quality_gate.py` on all 13 chapters | C01-C13 | Quality gate reports (8/8 PASS) | P4-03 |

**Phase 4 exit criteria:** All 13 chapters pass `audit_chapter.py` (exit 0) and `quality_gate.py` (8/8 criteria PASS).

---

### PHASE 5 — DOCX GENERATION

**Goal:** Build DOCX files for all 13 chapters with proper formatting and Word native footnotes.

| Task ID | Task | Scope | Deliverable | Dependency |
|---------|------|-------|-------------|------------|
| P5-01 | Fix `build_chapter_docx.py` to filter running headers and deduplicate titles | `build_chapter_docx.py` | Updated script | P4 done |
| P5-02 | Run `extract_images.py` for all 13 chapters | C01-C13 | Image manifest + extracted images | P5-01 |
| P5-03 | Build DOCX for all 13 chapters | C01-C13 | 13 DOCX files in `09_docx/` | P5-02 |
| P5-04 | Run `audit_docx_format.py` on all 13 DOCX files | C01-C13 | DOCX audit reports (PASS) | P5-03 |
| P5-05 | Word COM verify Footnotes.Count for all 13 chapters | C01-C13 | Validation reports | P5-04 |

**Phase 5 exit criteria:** All 13 chapters have DOCX files that pass `audit_docx_format.py` and Word COM footnote verification.

---

### PHASE 6 — REGRESSION TESTING

**Goal:** Run comprehensive regression tests on all 13 chapters and Master DOCX.

| Task ID | Task | Scope | Deliverable | Dependency |
|---------|------|-------|-------------|------------|
| P6-01 | Run `test_regression.py` on C01-C13 | C01-C13 | Regression test results | P5 done |
| P6-02 | Verify no foreign language remnants remain in any vi file | C01-C13 | Foreign remnant scan report (0 findings) | P6-01 |
| P6-03 | Verify no duplicate titles or running headers in any DOCX | C01-C13 | DOCX structure report | P6-02 |
| P6-04 | Verify footnote placement (each footnote at correct paragraph) | C01-C13 | Footnote placement report | P6-03 |
| P6-05 | Update `progress.json` with correct statuses for all 13 chapters | All | Updated progress.json | P6-04 |
| P6-06 | Build Master DOCX (if applicable) | All | Master DOCX | P6-05 |

**Phase 6 exit criteria:** All 13 chapters pass regression tests. `progress.json` reflects actual state. Master DOCX passes quality gate.

---

## 4. CHAPTER WORK PLAN

### V1-C01: Memory, Tradition, and the History of "Vietnam" (Liam C. Kelley)

| Field | Value |
|-------|-------|
| Status | needs_full_redo (contains Arendt content) |
| Source | `02_extracted_text/v1/ch01.txt` (PDF 43-59, in 27-43) |
| Action | Re-translate from source |
| Foreign remnants | All (entire file is wrong content) |
| Footnotes | TBD (verify from source) |
| Images | 0 |
| Est. paragraphs | ~49 |

### V1-C02: The Origins of the Vietnamese Revolution (Christopher E. Goscha)

| Field | Value |
|-------|-------|
| Status | needs_full_redo (contains Arendt content) |
| Source | `02_extracted_text/v1/ch02.txt` (PDF 60-81, in 44-65) |
| Action | Re-translate from source |
| Foreign remnants | All (entire file is wrong content) |
| Footnotes | TBD (verify from source) |
| Images | 2 (Hình 2.1, 2.2) |
| Est. paragraphs | ~40 |

### V1-C03: Hồ Chí Minh and the Rise of the Vietnamese Communist Party (Pierre Brocheux)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch03.txt` (PDF 82-99, in 66-83) |
| Action | Fix foreign remnants, calques, alignment |
| Foreign remnants | EN/FR terms, calque errors |
| Footnotes | 51 |
| Images | 1 (Hình 3.1) |
| Est. paragraphs | ~62 |

### V1-C04: Indochina during World War II (Stein Tønnesson)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch04.txt` (PDF 100-121, in 84-105) |
| Action | Fix foreign remnants, calques, alignment |
| Foreign remnants | EN/FR terms, calque errors |
| Footnotes | 71 |
| Images | 2 (Hình 4.1, 4.2) |
| Est. paragraphs | ~48 |

### V1-C05: The August Revolution of 1945 (Stein Tønnesson)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch05.txt` (PDF 122-142, in 106-124) |
| Action | Fix foreign remnants, calques, alignment |
| Foreign remnants | EN/FR terms, calque errors |
| Footnotes | 26 |
| Images | 2 (Hình 5.1, 5.2) |
| Est. paragraphs | ~15 |

### V1-C06: The Birth of the Democratic Republic of Vietnam (Stein Tønnesson)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch06.txt` (PDF 143-169, in 127-152) |
| Action | Fix foreign remnants, calques, alignment |
| Foreign remnants | EN/FR terms, calque errors |
| Footnotes | 43 |
| Images | 1 (Hình 6.1) |
| Est. paragraphs | ~81 |

### V1-C07: France's Indochina War (Fredrik Logevall)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch07.txt` (PDF 170-188, in 154-172) |
| Action | Fix foreign remnants, VNCH calque, alignment |
| Foreign remnants | EN/FR terms, calque errors |
| Footnotes | TBD |
| Images | TBD |
| Est. paragraphs | TBD |

### V1-C08: China and the French Indochina War (Chen Jian)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch08.txt` (PDF 189-210, in 173-196) |
| Action | Fix foreign remnants, verify "nässig" fix, alignment |
| Foreign remnants | EN/FR terms (nässig fixed) |
| Footnotes | 68 |
| Images | TBD |
| Est. paragraphs | 36 |

### V1-C09: The French Indochina War in the Central Highlands (Andrew J. Gawthorpe)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch09.txt` (PDF 211-233, in 195-217) |
| Action | Fix missing 14 footnote markers, foreign remnants |
| Foreign remnants | EN/FR terms |
| Footnotes | 51 |
| Images | 3 (Hình 9.1, 9.2, Bản đồ 9.1) |
| Est. paragraphs | TBD |

### V1-C10: The French Indochina War in Northern Vietnam (Christopher Goscha)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch10.txt` (PDF 234-253, in 218-237) |
| Action | Translate missing P012+, fix foreign remnants |
| Foreign remnants | EN/FR terms |
| Footnotes | 0 (only P001-P011 translated) |
| Images | 2 (Hình 10.1, Bản đồ 10.1) |
| Est. paragraphs | 20 (only 11 translated) |

### V1-C11: The Battle of Điện Biên Phủ (Christopher Goscha)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch11.txt` (PDF 254-276, in 238-260) |
| Action | Fix missing 21 footnotes (BUG-008), foreign remnants |
| Foreign remnants | EN/FR terms |
| Footnotes | 21 missing |
| Images | TBD |
| Est. paragraphs | 56 |

### V1-C12: The Geneva Conference of 1954 (Fredrik Logevall)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch12.txt` (PDF 277-297, in 261-281) |
| Action | Fix missing 42 markers, duplicate [20], foreign remnants |
| Foreign remnants | EN/FR terms |
| Footnotes | 42 missing, duplicate [20] |
| Images | TBD |
| Est. paragraphs | TBD |

### V1-C13: Eisenhower and Vietnam (David L. Anderson)

| Field | Value |
|-------|-------|
| Status | needs_qa (translated, needs fixes) |
| Source | `02_extracted_text/v1/ch13.txt` (PDF 298-317, in 282-301) |
| Action | Fix foreign remnants, calque errors (Việt Nam Nam, Châu Á, Châu Âu, etc.) |
| Foreign remnants | EN/FR terms, calque errors |
| Footnotes | TBD |
| Images | TBD |
| Est. paragraphs | 254 lines |

---

## 5. QUALITY GATES

### Per-chapter Quality Gate (8 criteria — ALL must PASS)

| # | Criterion | Standard | Check Method |
|---|-----------|----------|--------------|
| C1 | Encoding | UTF-8, NFC, no BOM, LF | `encoding_checker.py` |
| C2 | Orthography | 0× non-VNCH terms (CRITICAL/MAJOR) | `vnch_orthography.py` |
| C3 | Paragraph alignment | src paragraphs = vi paragraphs | `document_comparator.py` |
| C4 | Footnote alignment | src footnotes = vi footnotes | `quality_gate.py` |
| C5 | No fabricate | No added/omitted information | Sentence-by-sentence review |
| C6 | VNCH style | Natural VNCH, no word-for-word | Independent read-through |
| C7 | DOCX exists | DOCX in `09_docx/` | `build_chapter_docx.py` |
| C8 | DOCX footnotes | Word native footnotes (OOXML) | Word COM verification |

### Per-phase Quality Gate

| Phase | Exit Criteria |
|-------|---------------|
| Phase 0 | Complete diagnosis report for all 13 chapters |
| Phase 1 | Clean source text with proper segmentation and type classification |
| Phase 2 | Complete Vietnamese translations with no foreign remnants |
| Phase 3 | All 13 chapters pass VNCH orthography + VLP-01 + terminology consistency |
| Phase 4 | All 13 chapters pass audit_chapter.py (exit 0) + quality_gate.py (8/8) |
| Phase 5 | All 13 chapters have DOCX files passing audit_docx_format.py |
| Phase 6 | All 13 chapters pass regression tests, progress.json updated |

---

## 6. CHECKPOINT & RECOVERY

### 6.1 Checkpoint format

After each task, update `00_plan/progress.json` with:
- Chapter status (pending/translating/translating_done/qa_pending/qa_done/docx_built/HOAN_TAT)
- Paragraphs translated
- Footnotes count
- Known issues
- Last updated timestamp

### 6.2 Recovery procedure

If interrupted:
1. Read `00_plan/progress.json` to identify last completed task
2. Read the chapter's `v1_chXX_vi.txt` to verify current state
3. Resume from the next uncompleted task
4. Re-run quality checks on the last completed chapter to verify

### 6.3 File backup

Before modifying any vi file:
1. Create backup in `99_scripts/backup/` with timestamp
2. Never overwrite original source files
3. Keep all intermediate versions until final QA passes

---

## 7. DELIVERABLES

| Deliverable | Location |
|-------------|----------|
| Fixed translation files | `04_translation/v1/chXX/v1_chXX_vi.txt` |
| Fixed source files (if re-extracted) | `02_extracted_text/v1/chXX.txt` |
| DOCX files | `09_docx/V1-CXX_<slug>.docx` |
| QA reports | `05_qa/` |
| Audit reports | `05_qa/audit_chXX.json` |
| Foreign remnant reports | `05_qa/foreign_remnant_chXX.md` |
| Updated progress.json | `00_plan/progress.json` |
| Scripts (if new) | `99_scripts/` |

---

## 8. DEPENDENCIES & RISKS

### 8.1 Dependencies

| Dependency | Status | Risk |
|------------|--------|------|
| Source PDF (text layer) | ✅ Available | Low |
| Extracted text (v1) | ✅ Available (C01-C21) | Low |
| Style Guide Phan B v2.3 | ✅ Available | Low |
| Grammar Engine v2.1 | ✅ Available | Low |
| Master Lexicon (321+ terms) | ✅ Available | Low |
| Glossary (nam/bac compare) | ✅ Available | Low |
| audit_chapter.py | ✅ Available | Low |
| build_chapter_docx.py | ✅ Available | Medium (needs fixes) |
| check_footnote_markers.py | ✅ Available | Low |
| chapter_workflow.py | ✅ Available | Low |

### 8.2 Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| C01-C02 entirely wrong content (Arendt) | High | Re-translate from source (P2-01, P2-02) |
| Foreign language remnants in C03-C13 | High | Systematic scan + fix (P0-02, P2-03..P2-13) |
| Missing paragraphs in C10 | High | Translate P012+ (P2-10) |
| Missing footnotes in C09, C11, C12 | High | Extract from source, translate, add markers |
| Duplicate titles / running headers in DOCX | Medium | Fix build_chapter_docx.py (P5-01) |
| Calque errors (Việt Nam Nam, etc.) | Medium | Apply VNCH fixes (P3-02) |
| Pinyin names not converted to Hán-Việt | Medium | Apply §13 rules (P3-05) |
| Pipeline issues (OCR, segmentation) | High | Fix pipeline (P1-01..P1-05) |

---

## 9. COMPLETION CRITERIA

All of the following must be true for the project to be considered complete:

1. **Source verification:** All 13 chapters' source text matches PDF (page provenance, completeness, no missing content).
2. **Translation completeness:** All 13 chapters have complete Vietnamese translations (no missing paragraphs).
3. **Foreign language scan:** 0 foreign language remnants in any vi file (except proper nouns, quotes, and terms that must be kept in original language).
4. **VNCH orthography:** 0 CRITICAL/MAJOR orthography violations in any chapter.
5. **VLP-01 compliance:** All sentences pass Vietnamese-first translation check.
6. **Paragraph alignment:** src paragraphs = vi paragraphs for all 13 chapters (1:1 mapping).
7. **Footnote alignment:** src footnotes = vi footnotes for all 13 chapters (sequential 1..N).
8. **audit_chapter.py:** Exit 0 for all 13 chapters.
9. **quality_gate.py:** 8/8 PASS for all 13 chapters.
10. **DOCX:** All 13 chapters have DOCX files passing `audit_docx_format.py`.
11. **Word COM:** Footnotes.Count matches progress.json for all 13 chapters.
12. **Regression tests:** `test_regression.py` passes for all 13 chapters.
13. **progress.json:** Updated with correct statuses, paragraphs, footnotes for all 13 chapters.

---

## 10. CURRENT PROJECT STATUS

- **Phase:** 0 (diagnosis not yet started)
- **Chapters with translations:** 15 (C01-C15)
- **Chapters needing full re-translation:** 2 (C01, C02 — Arendt content)
- **Chapters needing fixes:** 11 (C03-C13 — foreign remnants, calques, missing paragraphs/footnotes)
- **Chapters with DOCX:** ~1 (C14 only, based on available reports)
- **Chapters HOAN_TAT:** 1 (C14)
- **Critical blockers:** C01-C02 cross-contamination, C10 missing paragraphs, C11/C12 missing footnotes

## 11. RECOMMENDED FIRST TASK

**P0-01: Run `audit_chapter.py` on all 13 chapters** to get a baseline diagnosis of every issue.

This is the first step because:
- It provides a quantitative baseline (how many foreign remnants, missing footnotes, calque errors per chapter)
- It identifies which chapters need the most work
- It's read-only (no file changes)
- It informs the scope of subsequent phases

Command: `for i in $(seq 1 13); do python 99_scripts/audit_chapter.py $i; done`

## 12. CRITICAL BLOCKERS

1. **C01-C02 contain wrong content** (Arendt instead of Vietnam War) — must re-translate from source before any fixes can be applied.
2. **C10 only has P001-P011 translated** — P012+ must be translated before QA.
3. **C11 missing 21 footnotes** — must extract from source and translate.
4. **C12 missing 42 footnote markers + duplicate [20]** — must fix markers before DOCX build.
5. **progress.json references Arendt book** — must replace with correct project data.

## 13. EXPECTED DELIVERABLES

1. 13 complete Vietnamese translation files (`v1_ch01_vi.txt` … `v1_ch13_vi.txt`) with no foreign language remnants.
2. 13 DOCX files in `09_docx/` passing format audit.
3. 13 QA reports in `05_qa/` (audit + quality gate results).
4. Updated `progress.json` reflecting actual state of all 13 chapters.
5. Fixed pipeline scripts (if needed) in `99_scripts/`.
6. Foreign remnant scan reports for all 13 chapters.

## 14. APPROVAL REQUIRED

This plan requires user approval before execution. The plan is divided into 6 phases (P0-P6) with 30 tasks. Phases must be executed in order. No translation or file modification should begin until Phase 0 diagnosis is complete and reviewed.

**Estimated scope:** 13 chapters, ~110,000 words of source text, 30 tasks across 6 phases.
**Estimated foreign remnants:** TBD (to be determined in Phase 0).

---

*D (Dừng sau khi hoàn thành plan và chờ phê duyệt)*
