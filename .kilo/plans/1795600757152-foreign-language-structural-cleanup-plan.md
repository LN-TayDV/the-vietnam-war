# IMPLEMENTATION PLAN: Foreign Language & Structural Cleanup — All 13 Chapters

**Project:** The Origins of Totalitarianism (VNCH translation)  
**Root:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\`  
**Plan file:** `.kilo/plans/1795600757152-foreign-language-structural-cleanup-plan.md`

---

## CURRENT STATE (verified)

- All 13 chapters: status `HOAN_TAT` in `00_plan/progress.json`
- Individual chapter DOCXs built; master DOCX `V2-Origins-of-Totalitarianism-MASTER.docx` built (892/892 footnotes)
- QA gate: 11/11 PASS (alignment, encoding, footnotes, styles)
- Existing fix scripts in `99_scripts/`: `clean_foreign_fragments.py` (CJK/Cyrillic only), `clean_english_ch12.py` (EN fragments ch12/ch13 only), `apply_vnch_fixes.py` (VNCH orthography only)
- **Remaining issues NOT covered by existing scripts:**

| # | Issue | Chapters | Verified in file |
|---|-------|----------|-----------------|
| 1 | Empty paragraphs | ch01 P004/P005; ch02 P001-P026 (26); ch10 P007/P008 | ch01:v1_ch01_vi.txt:10-15, ch02:v1_ch02_vi.txt:2-78, ch10:v1_ch10_vi.txt:19-20 |
| 2 | Chapter title merged with body | ch01 P001, ch12 P001 | ch01:v1_ch01_vi.txt:1-2, ch12:v1_ch12_vi.txt:1-4 |
| 3 | Running header text prepended to body paragraphs | ch02 P033 (EN); ch03-ch11 most paragraphs (VNCH header text) | ch02:v1_ch02_vi.txt:97-98, ch03:v1_ch03_vi.txt:1-30, ch06:v1_ch06_vi.txt:1-20 |
| 4 | German text untranslated | ch02 P029 | ch02:v1_ch02_vi.txt:86 |
| 5 | French phrases untranslated | ch03-ch08 | ch03:v1_ch03_vi.txt:14 ("la capitale..."), ch06:v1_ch06_vi.txt:14 ("La raison est...") |
| 6 | Latin phrases untranslated | ch03-ch06 | ch03:v1_ch03_vi.txt:17 ("apologia pro vita sua"), ch06:v1_ch06_vi.txt:14 ("primus inter pares") |
| 7 | English words/phrases untranslated | ch01-ch13 | ch01:v1_ch01_vi.txt:5 ("con substitutions"), ch12:v1_ch12_vi.txt:5 ("totalitarian") |
| 8 | Duplicate paragraphs | ch09 P008=P009, ch10 P003=P004, ch13 P009=P010 | ch09:v1_ch09_vi.txt, ch10:v1_ch10_vi.txt:8-11 |
| 9 | Footnote content inline in body | ch12 P001-P005 | ch12:v1_ch12_vi.txt:9-28 |
| 10 | "totalitarian" instead of "toàn trị" | ch12 throughout | ch12:v1_ch12_vi.txt:5,37 |

---

## DECISIONS (recommended defaults — confirm if you disagree)

| Question | Recommended Answer | Rationale |
|----------|-------------------|-----------|
| Bibliography ch13 P016-P061 (English entries) | Keep original language | Academic convention: bibliographic citations stay in source language |
| Proper noun transliteration | VNCH convention: Hit-lê, Sta-lin, Na-xi | Consistent with existing VNCH style in ch10/ch11 |
| Empty paragraphs (ch02 P001-P026, ch10 P007-P008) | Mark `[TRONG]` placeholder + `UNVERIFIED` note | Source PDF not available to confirm content existed; do not fabricate |
| Footnote placeholders (ch12, 39 unrecoverable) | Keep as `[CHƯA KHÔ PHỤC]` placeholders | Do not fabricate footnote definitions |
| Duplicate paragraphs | Remove duplicate (keep first occurrence) | Exact duplicates are segmentation artifacts |
| Running header text in body | Remove entirely; use as chapter/section heading only | Header text is not body content |

---

## TASKS (in order)

### Task 1: Create `99_scripts/fix_chapter_structure.py`
Purpose: Structural fixes only — no translation.

Actions:
- Parse each v2 chapter file (`04_translation/v2/chNN/v1_chNN_vi.txt`)
- Separate chapter title line from body paragraph (ch01 P001, ch12 P001) → output chapter title as standalone `[V1CNN-P000]` title node, body starts at P001
- Remove running header text prepended to body paragraphs (VNCH header text like "DÂN TỘC QUỐC GIA, SỰ RA ĐỜI...", "CHỦ NGHĨA ĐẾ QUỐC", "TƯ DUY VỀ CHỦNG TỘC TRƯỚC...", "CHỦ NGHĨA TOÀN TRỊ", etc.)
- Remove English running header "THE NATION-STATE; THE BIRTH OF ANTISEMITISM" from ch02 P033
- Remove page numbers leaked into body (ch04 "390", "392"; ch12 "390", "391", "392")
- Mark empty paragraphs: replace empty body with `[TRONG] (UNVERIFIED - n Paragraph trống, cần kiểm tra bản gốc)`
- Remove duplicate paragraphs (keep first occurrence): ch09 P009, ch10 P004, ch13 P010
- Move inline footnote content (ch12 P001-P005: ¹-⁵) out of body into FOOTNOTES block
- Remove standalone orphaned numbers (ch12 "1:" at P003)
- Preserve `=== FOOTNOTES ===` block intact
- Idempotent; output a change report

### Task 2: Create `99_scripts/translate_foreign_remnants.py`
Purpose: Translate foreign language phrases to VNCH pre-1975 style.

Actions:
- German phrases → VNCH (ch02 P029 extensive German; "Partei und Staat", "Gottfried Neesse" ch10; "Fuehrer", "Völkischer Beobachter" ch11)
- French phrases → VNCH (ch03-ch08: "la capitale du dixneuvieme siecle", "bordereau", "Tiers Etat", "fortune des armes", etc.)
- Latin phrases → VNCH (ch03-ch06: "apologia pro vita sua", "primus inter pares", "ius", "imperium", "consensus iuris", "Initium ut esset homo creatus est")
- English words/phrases → VNCH (ch01 "con substitutions"; ch12 "totalitarian"→"toàn trị"; ch13 "Bibliography"→"Tài Liệu Tham Khảo", "Part One: Antisemitism"→"Phần Một: Chủ Nghĩa Bài Do Thái")
- Keep proper nouns in original language with italic formatting: book titles ("Remembrance of Things Past", "Heart of Darkness", "Leviathan"), person names, place names, newspaper names ("Action Française", "Libre Parole", "La Voix du Nord")
- Keep OCR artifacts fixed: "Pan-Xlaven"→"Pan-Slav"→VNCH "Pan-Xlavơ", "Pan-Duc"→"Pan-Dức"
- Idempotent; output a change report listing each translation with chapter/paragraph

### Task 3: Run existing clean scripts (idempotent, already partially applied)
- `python 99_scripts/clean_foreign_fragments.py` — CJK/Cyrillic cleanup
- `python 99_scripts/clean_english_ch12.py` — EN fragments ch12/ch13
- `python 99_scripts/apply_vnch_fixes.py ch01 ch02 ... ch13` — VNCH orthography

### Task 4: Rebuild DOCX files
- `python 99_scripts/build_chapter_docx_v2.py --all` — rebuild all 13 chapter DOCXs
- `python 99_scripts/build_master_docx_v2.py` — rebuild master DOCX

### Task 5: Run regression QA
- `python 99_scripts/debug_align.py` on all 13 chapters — verify src=vi alignment
- Verify no foreign language remnants remain (except proper nouns/book titles)
- Verify no empty paragraphs (except `[TRONG]` marked)
- Verify no duplicate paragraphs
- Verify footnote markers match FOOTNOTES block definitions
- Verify chapter titles are separate from body

---

## VALIDATION CRITERIA (all must PASS)

1. **Alignment:** `debug_align.py` reports src=vi for all 13 chapters
2. **No empty body paragraphs:** Every `[V1CNN-PNNN]` has non-empty body text (except `[TRONG]` marked)
3. **No running headers in body:** No paragraph starts with VNCH chapter/section header text
4. **No duplicate paragraphs:** No two paragraphs have identical body text
5. **No foreign language body text:** No German/French/Latin/English phrases in body except proper nouns and book titles
6. **Chapter titles separated:** Chapter title is its own node, not merged with first body paragraph
7. **Footnotes matched:** Every superscript marker in body has a corresponding FOOTNOTES definition
8. **DOCX builds:** All 13 chapter DOCXs + master DOCX build without errors
9. **Encoding:** UTF-8, NFC, no BOM, LF line endings

---

## DELIVERABLES

1. `99_scripts/fix_chapter_structure.py` — structural fix script
2. `99_scripts/translate_foreign_remnants.py` — VNCH translation script
3. `FOREIGN_LANGUAGE_AUDIT_FINDINGS.md` — detailed findings (already written at `.kilo/plans/FOREIGN_LANGUAGE_AUDIT_FINDINGS.md`)
4. `STRUCTURE_FIX_REPORT.md` — report of structural changes made by Task 1
5. `TRANSLATION_REPORT.md` — report of foreign language translations made by Task 2
6. Updated `00_plan/progress.json` — fix status per chapter
7. Rebuilt DOCX files for all 13 chapters + master

---

## OPEN QUESTIONS (for user confirmation)

1. **Bibliography ch13 P016-P061:** Keep English bibliographic citations in original language (academic convention)? [Recommended: YES]
2. **Empty paragraphs:** Mark `[TRONG]` + UNVERIFIED rather than fabricating content? [Recommended: YES]
3. **Footnote placeholders:** Keep `[CHƯA KHÔ PHỤC]` placeholders rather than fabricate definitions? [Recommended: YES]
4. **Proper noun transliteration:** Use VNCH convention (Hit-lê, Sta-lin, Na-xi)? [Recommended: YES]

If you confirm these defaults, the plan is implementation-ready. Otherwise, reply with your preferences and I'll update the plan before calling plan_exit.