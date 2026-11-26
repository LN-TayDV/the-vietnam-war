# Arendt Translation Workflow Rebuild Plan

**Project**: The Origins of Totalitarianism — Hannah Arendt
**Directory**: `translation-project-arendt/`
**Goal**: Rebuild entire translation pipeline while preserving ch01–ch11 translations

---

## Design Decisions (Confirmed)

| Decision | Choice |
|----------|--------|
| Source format | Paragraph IDs + page refs: `[V1CNN-PXXX] (trang N)` |
| Footnotes | Separate section with `[FN:N]` inline markers |
| Existing translation mapping | Sentence-level alignment |
| DOCX output | Book layout, Word native footnotes at bottom of page |

---

## Phase 0: Audit & Backup (Week 0)

### 0.1 Inventory & Backup
- [ ] Copy `translation-project-arendt/` → `translation-project-arendt.backup_$(date +%Y%m%d)/`
- [ ] Catalog all existing files: source, translation parts, consolidated, progress.json
- [ ] Verify encoding (UTF-8/NFC/no-BOM/LF) on all files
- [ ] Document current chapter statuses from progress.json

### 0.2 Baseline Metrics
- [ ] Count paragraphs per chapter in `02_extracted_text/v1/`
- [ ] Count paragraphs per chapter in `04_translation/v1/ch*/v1_ch*_vi.txt`
- [ ] Count footnotes per chapter (inline markers + definitions)
- [ ] Record page ranges per chapter

---

## Phase 1: OCR Reconstruction Pipeline (Week 1)

### 1.1 New OCR Script (`99_scripts/ocr_reconstruct.py`)
```python
# Input: PDF → per-page text (already done in extract_chapters.py)
# Output: 02_extracted_text/v2/chNN_src.txt with:
#   - Paragraph detection (blank line + indentation heuristics)
#   - Cross-page paragraph merging (detect continued paragraphs)
#   - Unique paragraph IDs: [V1C01-P001] (trang 48)
#   - Footnote extraction → separate section at end of file
#   - Heading detection (CHAPTER, Section I/II/III, etc.)
```

### 1.2 Paragraph Reconstruction Rules
- **Paragraph boundary**: Blank line OR significant indentation change
- **Cross-page merge**: If paragraph ends mid-sentence (no period, lowercase start next page) → merge
- **Footnote detection**: Lines starting with superscript digits (¹²³⁴⁵⁶⁷⁸⁹) or `[1]` pattern
- **Heading preservation**: Keep "— đề mục —" markers for chapter/section headings

### 1.3 Output Format (chNN_src.txt)
```
=== CHAPTER 1: Antisemitism as an Outrage to Common Sense ===
[V1C01-P001] (trang 48)
MANY STILL consider it an accident that Nazi ideology centered around antisemitism...

[V1C01-P002] (trang 48)
Only the horror of the final catastrophe...

...

=== FOOTNOTES ===
[FN:1] (trang 48) Source text...
[FN:2] (trang 49) Source text...
```

### 1.4 Validation
- [ ] Run on ch01 (known good), compare paragraph count vs old
- [ ] Run on ch04 (cross-page paragraphs), verify merges
- [ ] Run on ch07 (103 footnotes), verify extraction
- [ ] Generate `reconstruction_report.json` with stats per chapter

---

## Phase 2: Source File Generation (Week 1-2)

### 2.1 Build All Chapter Sources
- [ ] Run `ocr_reconstruct.py` for all 18 sections (front_matter → ch13)
- [ ] Output to `02_extracted_text/v2/`
- [ ] Verify: paragraph IDs sequential, page refs correct, footnotes extracted

### 2.2 Quality Checks
- [ ] No duplicate/missing paragraph IDs
- [ ] Page refs match PDF page numbers
- [ ] Footnote count matches progress.json `notes` field
- [ ] Cross-page paragraphs properly merged (no artificial splits)

---

## Phase 3: Translation Mapping (Week 2)

### 3.1 Alignment Tool (`99_scripts/align_translations.py`)
```python
# For each chapter ch01–ch11:
#   1. Load old source (v1) + old translation (v1)
#   2. Load new source (v2) with paragraph IDs
#   3. Sentence-split both old source and old translation
#   4. Align sentences (fuzzy match + position)
#   5. Map each old sentence → new paragraph ID
#   6. Reconstruct translation in new paragraph structure
#   7. Output: 04_translation/v2/chNN/v1_chNN_vi.txt
```

### 3.2 Mapping Strategy
- **Exact match**: Identical sentences → direct mapping
- **Fuzzy match**: Levenshtein distance < 0.2 → review needed
- **Unmatched**: Flag for human review (likely split/merged differently)

### 3.3 Output Format (v2 translation)
```
=== CHAPTER 1 ===
[V1C01-P001] (trang 48)
NHIỀU NGƯỜI VẪN coi đó là một sự việc ngẫu nhiên...

[V1C01-P002] (trang 48)
Chỉ có kinh hoàng của thảm họa cuối cùng...

...

=== FOOTNOTES ===
[FN:1] (trang 48) Nội dung chú thích đã dịch...
[FN:2] (trang 49) Nội dung chú thích đã dịch...
```

### 3.4 Verification
- [ ] Paragraph count: new source = new translation (Rule 18)
- [ ] Footnote count: source = translation
- [ ] No missing content (sentence count match)
- [ ] Generate `mapping_report_chNN.json` per chapter

---

## Phase 4: Translation Workflow Redesign (Week 2-3)

### 4.1 New Translation Script (`99_scripts/translate_chapter.py`)
```python
# Features:
# - Resume from checkpoint (last completed paragraph ID)
# - Batch processing (N paragraphs per run)
# - Auto-save after each batch
# - Progress tracking in progress.json
# - VNCH terminology enforcement (from MASTER_LEXICON.csv)
# - Grammar Engine integration (7-step process)
```

### 4.2 Checkpoint Format (`04_translation/v2/chNN/checkpoint.json`)
```json
{
  "chapter": "ch12",
  "last_paragraph": "V1C12-P045",
  "last_batch": 3,
  "completed_paragraphs": 45,
  "total_paragraphs": 120,
  "footnotes_done": 12,
  "total_footnotes": 65,
  "updated": "2026-11-25T15:33:54Z"
}
```

### 4.3 Translation Loop
```
while not done:
  load checkpoint
  get next batch (10 paragraphs)
  for each paragraph:
    apply 7-step Grammar Engine
    enforce VNCH rules (Style Guide 29 rules)
    save immediately
  update checkpoint
  run quick QA (alignment + encoding)
```

---

## Phase 5: QA Pipeline (Week 3)

### 5.1 QA Script (`99_scripts/qa_chapter.py`)
```python
# Checks (per Style Guide Quy tắc 29 - Quality Gate 8 criteria):
# 1. Encoding: UTF-8/NFC/no-BOM/LF
# 2. Orthography: 0× non-VNCH terms (apply_vnch_fixes.py)
# 3. Paragraph alignment: src count == vi count (Rule 18)
# 4. Footnote alignment: src count == vi count, markers match
# 5. No fabricate: no invented page refs, citations
# 6. Natural style: run word-for-word detection
# 7. DOCX buildable: build_chapter_docx.py succeeds
# 8. Word Footnotes.Count == progress.json notes
```

### 5.2 Auto-Fix Script (`99_scripts/apply_vnch_fixes.py`)
- Apply 30 VNCH grammar rules from Grammar Engine §1.3-1.8
- Preserve proper nouns, titles, French quotes (Rule 15 false positive list)
- Output diff for review

### 5.3 Realignment Script (`99_scripts/realign_chapter.py`)
- Sentence-level realignment when paragraph counts differ
- Used only when QA fails on alignment

---

## Phase 6: DOCX Builder Redesign (Week 3-4)

### 6.1 Requirements
- **Book layout**: Mirror margins, page size matching PDF (B5/A5)
- **Headings**: Chapter title (Heading 1), Section I/II/III (Heading 2)
- **Paragraphs**: Normal style, first-line indent, 1.15 line spacing
- **Footnotes**: Word native, bottom of page, 9pt, continuous numbering 1..N per chapter
- **Page breaks**: Match PDF page boundaries (optional: `[V1CNN-PXXX] (trang N)` → page break)
- **Quotations**: Block quote style for indented passages
- **Unicode**: Full Vietnamese support (NFC)

### 6.2 Build Script (`99_scripts/build_chapter_docx.py`)
```python
# Input: v2 source + v2 translation
# Process:
# 1. Create Document()
# 2. Add chapter heading
# 3. For each paragraph:
#    - Add paragraph with style
#    - Insert footnote reference (superscript)
#    - Add footnote content at bottom of page
# 4. Handle page breaks from source markers
# 5. Save to 09_docx/V1-CNN_<slug>.docx
# 6. Verify via python-docx + Word COM (if available)
```

### 6.3 Verification
- [ ] `docx.footnotes.count == progress.json['chapters'][ch]['notes']`
- [ ] Open in Word/LibreOffice → no corruption
- [ ] Footnote references link to correct content
- [ ] Page count reasonable (not 1 giant page)

---

## Phase 7: Test & Validation (Week 4)

### 7.1 Test Chapters
| Chapter | Reason |
|---------|--------|
| ch04 | Many cross-page paragraphs, 70+ footnotes |
| ch07 | 103 footnotes, complex section structure |
| ch10 | Page label drift, _p4b partial, 65 footnotes |
| ch12 | Next to translate (pending), 71 pages, many footnotes |

### 7.2 Test Procedure per Chapter
1. Reconstruct source (v2)
2. Map existing translation (ch01–ch11) OR translate new (ch12+)
3. Run QA pipeline → all 8 gates PASS
4. Build DOCX → verify in Word
5. Update progress.json with full metadata

### 7.3 Acceptance Criteria
- [ ] All 8 Quality Gate criteria PASS
- [ ] DOCX opens in Word + LibreOffice without errors
- [ ] Footnotes.Count matches exactly
- [ ] No paragraph loss/duplication
- [ ] Unicode Vietnamese renders correctly

---

## Phase 8: Full Rollout & Documentation (Week 4-5)

### 8.1 Update Documentation
- [ ] `MASTER_TRANSLATION_PLAN.md` — new workflow, file locations, commands
- [ ] `TRANSLATION_WORKFLOW.md` — step-by-step for translators
- [ ] `SKILL.md` — updated for v2 pipeline
- [ ] `progress.json` — add v2 fields (paragraphs, footnotes, docx_status)

### 8.2 Apply to Remaining Chapters (ch12, ch13)
- [ ] Run full pipeline on ch12
- [ ] Run full pipeline on ch13
- [ ] Mark `HOAN_TAT` when all gates pass

### 8.3 Cleanup
- [ ] Archive v1 folders (`v1_archive/`)
- [ ] Remove temp files (`tmp_*`, `debug_*`)
- [ ] Final progress.json with complete book status

---

## File Structure After Rebuild

```
translation-project-arendt/
├── 00_plan/
│   ├── progress.json          # Updated with v2 metadata
│   ├── MASTER_TRANSLATION_PLAN.md
│   └── TRANSLATION_WORKFLOW.md
├── 02_extracted_text/
│   ├── v1/                    # Archived (read-only)
│   └── v2/                    # NEW: chNN_src.txt with para IDs + footnotes
├── 03_terminology/
│   └── ARENDT_TERMINOLOGY.md
├── 04_translation/
│   ├── v1/                    # Archived
│   └── v2/
│       ├── ch01/
│       │   ├── v1_ch01_vi.txt        # Mapped translation
│       │   └── checkpoint.json
│       ├── ch02/
│       │   └── ...
│       └── ch12/                    # New translations start here
│           ├── v1_ch12_vi.txt
│           └── checkpoint.json
├── 05_qa/
│   └── reports/               # QA reports per chapter
├── 07_style_guide/
│   ├── STYLE_GUIDE_PHAN_B.md  # v2.3 (keep)
│   ├── TRANSLATION_GRAMMAR_ENGINE.md  # v2.1 (keep)
│   └── ...
├── 08_southern_vietnamese_library/
├── 09_docx/
│   ├── V1-C01_antisemitism-outrage.docx
│   ├── V1-C02_...
│   └── ...
└── 99_scripts/
    ├── ocr_reconstruct.py
    ├── align_translations.py
    ├── translate_chapter.py
    ├── qa_chapter.py
    ├── apply_vnch_fixes.py
    ├── realign_chapter.py
    ├── build_chapter_docx.py
    └── verify_docx.py
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Paragraph mapping loses content | Sentence-level alignment + human review of diffs |
| Footnote misalignment | Extract footnotes separately, match by page + sequence |
| DOCX footnote corruption | Dual verification: python-docx + Word COM automation |
| Encoding issues | Enforce UTF-8/NFC/LF in all scripts; reject non-compliant |
| Regression on ch01–ch11 | Full backup + automated comparison v1 vs v2 output |

---

## Commands Summary

```bash
# Phase 1: Reconstruct sources
python 99_scripts/ocr_reconstruct.py --all

# Phase 3: Map existing translations (ch01-ch11)
python 99_scripts/align_translations.py --chapter ch01
# ... repeat for ch02-ch11

# Phase 4: Translate new chapters (ch12+)
python 99_scripts/translate_chapter.py --chapter ch12 --resume

# Phase 5: QA
python 99_scripts/qa_chapter.py --chapter ch12

# Phase 6: Build DOCX
python 99_scripts/build_chapter_docx.py --chapter ch12

# Phase 7: Verify DOCX
python 99_scripts/verify_docx.py --chapter ch12
```

---

## Open Questions for Implementation

1. **Word COM availability**: Is `win32com.client` available for Footnotes.Count verification? If not, use python-docx only.
2. **PDF page size**: What exact page dimensions (B5, A5, custom)? Needed for DOCX page setup.
3. **Footnote numbering**: Continuous 1..N per chapter, or continuous across book? (Assume per chapter based on progress.json)
4. **Heading hierarchy**: Confirm Section I/II/III → Heading 2, subsections → Heading 3?
5. **Batch size for translation**: 10 paragraphs per checkpoint? Adjustable?

---

## Success Criteria

- [ ] All 18 sections have v2 source files with paragraph IDs
- [ ] ch01–ch11 translations mapped to v2 structure, QA PASS
- [ ] ch12, ch13 translated from scratch using new workflow
- [ ] All 18 DOCX files built, verified in Word/LibreOffice
- [ ] progress.json shows `HOAN_TAT` for all sections
- [ ] Zero data loss from existing translations
- [ ] Pipeline documented and reproducible