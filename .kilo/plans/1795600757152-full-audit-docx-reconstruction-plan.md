# Full 13-Chapter Audit & DOCX Builder Reconstruction Plan

**Project:** The Origins of Totalitarianism - Hannah Arendt (VNCH pre-1975 translation)
**Root:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\`

---

## Executive Summary

All 13 chapters are marked **HOAN_TAT** with DOCX files built. However, the current DOCX builder (`build_chapter_docx.py`) has critical structural deficiencies:

1. **No Word Style system** — manual inline formatting per paragraph
2. **No heading hierarchy** — cannot generate Navigation Pane or auto TOC
3. **Footnotes via raw OOXML** — fragile, bypasses python-docx API
4. **No unified style template** — each chapter builds independently
5. **No section/heading detection beyond Roman numerals** — misses subsections
6. **Widow/orphan control missing** — headings can strand at page bottom
7. **No automated quality gates** — alignment check only, no DOCX structural validation
8. **No chapter structure validation** — duplicate headings, broken paragraph continuity, cross-page splits not verified

This plan defines a **complete audit** of all 13 chapters and a **ground-up DOCX Builder v2** with a shared style system, proper document model, and automated validation — including mandatory chapter structure, heading hierarchy, and cross-page continuity controls.

---

## Phase 0: Inventory & Baseline (Read-Only)

### 0.1 Collect Current State
- [ ] Run `debug_align.py` on all 13 chapters → `audit/alignment_baseline.json`
- [ ] Extract DOCX structure from all 13 chapter DOCXs + master → `audit/docx_structure_baseline.json`
- [ ] Parse all v2 translation files → `audit/translation_inventory.json` (para count, fn count, headings detected, special elements)
- [ ] Document all OCR/paragraph reconstruction artifacts from `reconstruction_report.json`
- [ ] Inventory all `_p1.txt`, `_p2.txt` part files in `04_translation/v1/` for footnote provenance

### 0.2 Define Audit Criteria Matrix
Create `CHAPTER_AUDIT_MATRIX.md` with columns:
| Chapter | Pages | Paras (src) | Paras (vi) | Aligned? | Footnotes | Sequential? | Orphans? | Headings L1 | Headings L2 | Block Quotes | Tables/Images | VNCH Issues | **Chapter Title OK?** | **Heading Dupes?** | **Level Skips?** | **Para Splits?** | **Para Merges?** | **Cross-Page Joins?** | **Text Integrity** | Notes |
|---------|-------|-------------|------------|----------|-----------|-------------|----------|-------------|-------------|--------------|---------------|-------------|---------------------|------------------|----------------|----------------|----------------|-------------------|------------------|-------|

---

## Phase 1: Full 13-Chapter Content Audit

### 1.1 Source Quality Audit (per chapter)
For each chapter, compare:
- **v1 OCR source** (`02_extracted_text/v1/chNN.txt`) vs **v2 clean source** (`02_extracted_text/v2/chNN_src.txt`)
- Document: page boundaries, paragraph splits/merges, OCR artifacts, missing text, hyphenation errors
- Cross-reference with `reconstruction_report.json` (if available)

### 1.2 Paragraph Reconstruction Audit
- Verify every v2 paragraph has 1:1 mapping to v2 source paragraph (ID + page)
- Detect: split paragraphs across pages, merged paragraphs, missing paragraphs
- Flag: paragraphs with `[V1C##-P###] (trang N)` headers that don't match source

### 1.3 Chapter Structure & Heading Audit (NEW)
**Chapter Title Control:**
- Each chapter has exactly ONE official chapter title (from TITLES dict)
- No duplicate chapter titles in body text
- Chapter title not repeated at page tops/bottoms unless intentional running header

**Heading Hierarchy Validation:**
- Scan for Roman numerals (I, II, III, IV, V, VI) → must be Heading 2 (SectionH1)
- Scan for Arabic numerals (1, 2, 3...) at paragraph start → must be Heading 3 (SectionH2) or Heading 4 (SectionH3)
- Detect: duplicate headings at same level within chapter
- Detect: skipped heading levels (e.g., H1 → H3 without H2)
- Detect: false positives — regular sentences misclassified as headings (e.g., "Khi một phong trào..." is body text, not a heading)
- Verify heading hierarchy forms valid tree: Part → Chapter → Section (Roman) → Subsection (Arabic) → Sub-subsection

**Cross-Reference:**
- Heading text in translation must match source heading text (or valid VNCH translation)
- No heading created from mid-paragraph sentence

### 1.4 Paragraph Structure & Cross-Page Continuity Audit (NEW)
**Paragraph Integrity:**
- Paragraphs split at semantic boundaries, not PDF line breaks
- No two independent paragraphs merged into one
- No single paragraph artificially split across page boundary
- Sentence order, punctuation, logical flow preserved

**Cross-Page Continuity Check:**
For each page boundary (from `[V1C##-P###] (trang N)` headers):
- If paragraph P### ends mid-sentence and P###+1 continues same sentence → MERGE REQUIRED
- If last word of page N is hyphenated → join with first word of page N+1
- If page N ends with heading and page N+1 starts body → VALID (heading kept separate)
- If page N ends body and page N+1 starts body → CHECK if same logical paragraph (merge) or new paragraph (keep)
- Flag: UNVERIFIED if source PDF not available to confirm

**Automated Detection Heuristics:**
- Lowercase start of paragraph + no terminal punctuation on previous → likely continuation
- Hyphenated word at page end → likely split word
- Roman/Arabic numeral at page start → likely heading (keep separate)
- Capitalized sentence start + previous ended with period → likely new paragraph

### 1.5 Full Text Integrity Audit (NEW)
- Detect duplicate paragraphs within chapter and across chapters
- Detect missing paragraphs (source has, translation lacks)
- Detect reversed/out-of-order paragraphs
- Detect content loss (paragraph significantly shorter than source without footnote explanation)
- Cross-reference with source PDF for UNVERIFIED cases — do NOT auto-assume

### 1.6 Translation Alignment Audit
- Source paragraph count == VI paragraph count (Rule 18)
- Paragraph IDs match exactly and in order
- No fabricated/omitted content
- Footnote markers in body match definitions 1:1

### 1.7 Translation Quality Audit (VNCH)
Apply **STYLE_GUIDE_PHAN_B.md** (29 rules) + **TRANSLATION_GRAMMAR_ENGINE.md**:
- Orthography: `chính phủ` → `chánh phủ`, `quốc gia` → `quốc gia`, proper nouns
- Vocabulary: VNCH terms (e.g., `tổng thống` not `chủ tịch nước`, `bộ trưởng` not `thứ trưởng`)
- Grammar: aspect markers, classifiers, pronouns (`ngài`, `quyến`, `ta` vs `tôi`)
- Connectives: `và`, `mà`, `nhưng`, `tuy`, `dù`, `bởi vì`, `do đó` usage
- No Northern terms (`được` passive overuse, `cái` classifier, `rất` vs `quá`)
- No modern anachronisms (post-1975 vocabulary)

### 1.8 Footnote & Citation Audit
- Every inline marker has a definition; every definition has an inline marker
- Sequential numbering 1..N (except known gaps documented in progress.json)
- Citation formatting consistency: `op. cit.`, `loc. cit.`, `ibid.`, page refs
- Foreign text preservation: German, French, Latin quotes in original
- Placeholder footnotes documented (ch12: 39 placeholders for unrecoverable OCR)

### 1.9 Structural Element Detection
Scan each chapter for:
- **Part/Chapter titles** (already in TITLES dict)
- **Roman numeral sections** (I, II, III, IV, V, VI) → Heading 2
- **Arabic numeral subsections** (1, 2, 3...) → Heading 3
- **Block quotes** (indented, often with citation) → Block Quote style
- **Bibliography/Index entries** (ch13 back-matter) → Reference style
- **Tables/Figures** (if any) → Caption style

---

## Phase 2: DOCX Builder v2 — Architecture

### 2.1 Document Structure Model (Intermediate Representation)
```python
@dataclass
class DocNode:
    type: Literal["book_title", "part", "chapter", "section_h1", "section_h2", 
                  "section_h3", "body", "block_quote", "footnote", "bibliography",
                  "index_entry", "table", "figure", "toc", "page_break"]
    text: str
    level: int = 0
    metadata: dict = field(default_factory=dict)  # page, para_id, fn_refs, etc.
    children: List['DocNode'] = field(default_factory=list)
```

### 2.2 Style System (Word Styles)
Define in `styles/spec.yaml`:
| Style ID | Name | Base | Font | Size | Bold | Italic | Indent | Spacing | Keep With Next |
|----------|------|------|------|------|------|--------|--------|---------|----------------|
| `BookTitle` | Book Title | Normal | Times New Roman | 24pt | ✓ | | Center | Before: 72pt, After: 6pt | |
| `Author` | Author | Normal | Times New Roman | 14pt | | ✓ | Center | After: 24pt | |
| `PartHeading` | Part Heading | Heading 1 | Times New Roman | 18pt | ✓ | | Center | Before: 48pt, After: 12pt | ✓ |
| `ChapterNumber` | Chapter Number | Normal | Times New Roman | 14pt | ✓ | ✓ | Center | After: 6pt | ✓ |
| `ChapterTitle` | Chapter Title | Heading 1 | Times New Roman | 22pt | ✓ | | Center | After: 6pt | ✓ |
| `SectionH1` | Section H1 | Heading 2 | Times New Roman | 14pt | ✓ | | Left | Before: 18pt, After: 6pt | ✓ |
| `SectionH2` | Section H2 | Heading 3 | Times New Roman | 12.5pt | ✓ | | Left | Before: 12pt, After: 6pt | ✓ |
| `SectionH3` | Section H3 | Heading 4 | Times New Roman | 12pt | | ✓ | Left | Before: 6pt, After: 6pt | ✓ |
| `BodyText` | Body Text | Normal | Times New Roman | 12pt | | | First: 1.27cm | After: 6pt, Line: 1.3 | |
| `BodyTextFirst` | Body First Para | BodyText | | | | | First: 0cm | | |
| `BlockQuote` | Block Quote | Normal | Times New Roman | 11pt | | | Left: 1.5cm, Right: 1.5cm | Before: 6pt, After: 6pt, Line: 1.2 | |
| `FootnoteText` | Footnote Text | Normal | Times New Roman | 9pt | | | Left: 0.63cm, Hanging: 0.63cm | Before: 0, After: 0, Line: 1.15 | |
| `FootnoteRef` | Footnote Ref | Default Paragraph Font | | 9pt | | ✓ | Superscript | | |
| `Bibliography` | Bibliography | Normal | Times New Roman | 11pt | | | Hanging: 1.27cm | Before: 0, After: 3pt, Line: 1.15 | |
| `IndexEntry` | Index Entry | Normal | Times New Roman | 10pt | | | Hanging: 1cm | Before: 0, After: 2pt, Line: 1.1 | |
| `TOC1` | TOC Level 1 | | | | | | | | |
| `TOC2` | TOC Level 2 | | | | | | | | |

### 2.3 Page Layout (Section Properties)
- Page: A4 (21.0 × 29.7 cm)
- Margins: Top 1.9cm, Bottom 1.8cm, Left 2.1cm, Right 1.8cm
- Header: 1.0cm, Footer: 1.0cm
- Header: Right-aligned "THE ORIGINS OF TOTALITARIANISM · Hannah Arendt" (8.5pt, italic, muted)
- Footer: Centered page number "Trang N" (9pt, muted)
- Section break: New page for each chapter
- Page numbering: Restart at 1 per chapter (or continuous for master)

### 2.4 Footnote System
- Use python-docx `document.part.footnotes` API (not raw OOXML)
- Style: `FootnoteText` + `FootnoteReference` character style
- Auto-numbering: Restart each chapter (or continuous for master)
- Superscript reference in body, hanging number in footnote area

### 2.5 Heading Hierarchy & Navigation
- Heading 1: Part / Chapter Title (for TOC Level 1)
- Heading 2: Roman numeral sections (I, II, III...) (TOC Level 2)
- Heading 3: Arabic subsections (1, 2, 3...) (TOC Level 3)
- Heading 4: Lower subsections (a, b, c... or 1.1, 1.2...) (TOC Level 4)
- All headings: `keep_with_next = True` (prevent widow headings)
- Body paragraphs: `widow_control = True`

---

## Phase 3: DOCX Builder v2 — Implementation

### 3.1 Core Modules
```
99_scripts/
├── docx_builder_v2/
│   ├── __init__.py
│   ├── models.py           # DocNode, DocumentModel
│   ├── parser.py           # Parse v2 text → DocumentModel
│   ├── styles.py           # StyleSpec, StyleRegistry
│   ├── renderer.py         # DocumentModel → python-docx Document
│   ├── footnotes.py        # FootnoteManager
│   ├── layout.py           # PageLayout, SectionManager
│   └── builder.py          # Main build() entry point
├── styles/
│   ├── spec.yaml           # Style definitions
│   └── registry.py         # Load/apply styles
└── build_chapter_docx_v2.py  # CLI wrapper
```

### 3.2 Parser Logic (v2 text → DocumentModel)
1. Split by `=== FOOTNOTES ===` → body + footnotes
2. Parse paragraphs by `[V1C##-P###] (trang N)` headers
3. **Cross-page continuity resolution** (NEW):
   - For each adjacent paragraph pair (P###, P###+1):
     - If P### ends without terminal punctuation (., !, ?) AND P###+1 starts lowercase → MERGE (continuation)
     - If P### ends with hyphenated word AND P###+1 starts with word fragment → JOIN (split word)
     - If P### is Roman numeral heading AND P###+1 is body → KEEP SEPARATE
     - If P### is Arabic numeral heading AND P###+1 is body → KEEP SEPARATE
     - Else if both body and no merge signals → KEEP SEPARATE (new paragraph)
   - Flag UNVERIFIED merges where source PDF not available for confirmation
4. Classify each paragraph:
   - Book title / author / part / chapter → from TITLES + first paras
   - Roman numeral alone on line → `section_h1` (Heading 2)
   - Arabic numeral + text at start → `section_h2` (Heading 3) or `section_h3` (Heading 4) (context-dependent)
   - Indented + citation-like → `block_quote`
   - Bibliography pattern (author, title, publisher, year) → `bibliography`
   - Index pattern (term, page refs) → `index_entry`
   - Default → `body`
5. **Heading validation** (NEW):
   - Ensure exactly ONE chapter title per chapter (from TITLES)
   - Detect duplicate headings at same level within chapter
   - Detect skipped heading levels (H1→H3 without H2)
   - Flag false positives (sentences misclassified as headings)
6. Extract inline superscript markers → footnote references
7. Parse footnote definitions → FootnoteManager

### 3.3 Renderer Logic (DocumentModel → DOCX)
1. Create Document, register all styles from `spec.yaml`
2. Configure section layout (margins, header, footer, page numbering)
3. Build title page (Book Title, Author, Translation note)
4. Build TOC (field code `\o "1-3" \h \z \u`)
5. For each DocNode in order:
   - Apply appropriate paragraph style
   - For body: split by footnote markers, insert `FootnoteReference` runs
   - For footnotes: add to footnotes part via API
6. Set core properties (title, author, language=vi-VN)
7. Save with atomic write (tmp → rename)

### 3.4 Master DOCX Builder
- Single document combining all 18 sections
- Continuous page numbering (or per-chapter with section breaks)
- Single TOC for entire book
- Shared footnote numbering (continuous) or per-chapter (configurable)
- Bibliography/Index at end (from ch13 back-matter)

---

## Phase 4: Quality Gates & Automated Tests

### 4.1 Test Suite (`tests/`)
```
tests/
├── test_parser.py              # Parser output matches expected DocNode tree
├── test_styles.py              # All styles registered, inherit correctly
├── test_renderer.py            # Round-trip: model → docx → model (structure)
├── test_footnotes.py           # Footnote refs match defs, sequential, no orphans
├── test_alignment.py           # Para count, ID order, fn markers = defs
├── test_pagination.py          # No widow headings, widows/orphans controlled
├── test_master.py              # Master DOCX structure valid
├── test_vnch_orthography.py    # Spot-check VNCH terms in output
├── test_chapter_structure.py   # One chapter title, no dupes, hierarchy valid
├── test_paragraph_continuity.py # No artificial splits/merges, cross-page joins
└── test_text_integrity.py      # No duplicate/missing/reversed paragraphs
```

### 4.2 Quality Gate Script (`99_scripts/qa_gate.py`)
Run after every build:
1. **Alignment**: `debug_align.py` PASS
2. **DOCX Structure**: `docx-validate` (python-docx + lxml schema check)
3. **Footnotes**: Count match, all refs resolve, no orphans
4. **Styles**: All paragraphs have named style (no direct formatting)
5. **Headings**: Hierarchy valid (H1→H2→H3, no skips, no duplicates at same level)
6. **Pagination**: No heading at page end (heuristic: heading not last para before break)
7. **Encoding**: UTF-8, NFC, no BOM, LF only
8. **VNCH**: Zero Northern term flags (configurable list)
9. **Chapter Structure**: Exactly one chapter title per chapter; no duplicate chapter titles in body
10. **Paragraph Continuity**: No merged independent paragraphs; no artificial splits at page boundaries; cross-page merges validated against source
11. **Text Integrity**: No duplicate/missing/reversed paragraphs vs source; UNVERIFIED cases documented

### 4.3 CI Integration
- Add `pytest` config
- Pre-build: run alignment check
- Post-build: run QA gate
- Fail build on any gate failure

---

## Phase 5: Remediation & Rebuild

### 5.1 Fix Translation Issues (from Audit)
For each chapter, apply targeted fixes:
- VNCH orthography normalization (batch via `apply_vnch_fixes.py` enhanced)
- Missing/extra paragraph markers
- Footnote marker/definition mismatches
- Heading detection improvements

### 5.2 Rebuild All Chapter DOCXs
```bash
python 99_scripts/build_chapter_docx_v2.py ch01 ch02 ... ch13
```

### 5.3 Rebuild Master DOCX
```bash
python 99_scripts/build_master_docx_v2.py
```

### 5.4 Full Regression Test
- Run QA gate on all 13 + master
- Visual spot-check 3 chapters in Word
- Verify Navigation Pane, TOC, footnotes work

---

## Phase 6: Deliverables

### 6.1 Audit Reports
| File | Description |
|------|-------------|
| `FULL_13_CHAPTER_AUDIT.md` | Narrative audit findings per chapter |
| `CHAPTER_AUDIT_MATRIX.md` | Tabular matrix (see Phase 0.2) |
| `TRANSLATION_ERROR_REGISTER.md` | Every error found: location, type, severity, fix status |
| `DOCX_BUILDER_AUDIT.md` | Current builder deficiencies, v2 design decisions |
| `DOCX_STYLE_SPECIFICATION.md` | Complete style spec (table + rationale) |
| `DOCX_RECONSTRUCTION_PLAN.md` | Step-by-step rebuild plan with dependencies |
| `REMEDIATION_ROADMAP.md` | Prioritized fixes, effort, owner, timeline |
| `STRUCTURE_VALIDATION_REPORT.md` | **Chapter title, heading hierarchy, paragraph continuity, cross-page joins, text integrity** per chapter (NEW) |

### 6.2 Code Deliverables
- `99_scripts/docx_builder_v2/` — Complete v2 builder package
- `99_scripts/styles/spec.yaml` — Style definitions
- `tests/` — Full test suite
- `99_scripts/qa_gate.py` — Quality gate runner
- Updated `progress.json` with v2 DOCX paths and QA status

### 6.3 Dashboard/GOAL Button
- Update `dashboard.html` with:
  - Audit progress per chapter (checklist)
  - Error register summary (count by severity)
  - DOCX status per chapter (v1 vs v2, QA gate PASS/FAIL)
  - Quality gate dashboard (11 gates, green/red)
  - **Structure validation status**: Chapter title ✓, Heading hierarchy ✓, Paragraph continuity ✓, Cross-page joins ✓, Text integrity ✓
  - Next actions list
  - Links to all report files

---

## Dependencies & Order

```
Phase 0 (Inventory) 
    → Phase 1 (Content Audit) 
    → Phase 2 (Architecture Design) 
    → Phase 3 (Implementation) 
    → Phase 4 (Tests & Gates)
    → Phase 5 (Remediation & Rebuild) 
    → Phase 6 (Deliverables)
```

**Parallelizable:**
- Phase 1 audit across 13 chapters (independent)
- Phase 4 test writing (can start during Phase 3)
- Phase 6 report writing (starts after Phase 1 findings)

---

## Open Questions for User

1. **Footnote numbering in Master DOCX:** Continuous (1..N across book) or restart per chapter?
2. **Page numbering in Master DOCX:** Continuous or restart per chapter?
3. **Back-matter (ch13 Bibliography/Index):** Include in master? Separate section? Omit?
4. **Heading detection depth:** Only Roman (H2) + Arabic (H3), or also detect lower levels (a, b, c / 1.1, 1.2)?
5. **Block quote detection:** Heuristic (indentation + citation) or explicit marker in source?
6. **VNCH term list:** Use existing `TERMINOLOGY_TABLE_BY_DOMAIN.md` + `STYLE_GUIDE_PHAN_B.md` as authority, or maintain separate glossary?
7. **Dashboard GOAL button:** Simple HTML modal (current) or integrate with a project management tool?
8. **CI/CD:** Run tests locally only, or set up GitHub Actions?
9. **Cross-page merge policy:** Auto-merge on heuristic (lowercase start, hyphen, no terminal punctuation) + flag UNVERIFIED, or require manual review for every page boundary?
10. **Source PDF access:** Is the original PDF (`books/Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf`) available for verifying UNVERIFIED cross-page joins?

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| v2 parser misses heading types | Start with conservative detection (Roman + Arabic only), extend iteratively |
| Footnote ref/def mismatch in ch12 | Document 39 placeholders explicitly; don't auto-fix without verification |
| Style inheritance conflicts | Test style registry thoroughly; use `basedOn` chain explicitly |
| Master DOCX size/complexity | Build incrementally; validate after each section added |
| Regression in translation quality | Never auto-modify translation text; only fix via reviewed patches |

---

## Success Criteria

1. **All 13 chapters + master pass QA gate** (11/11 green)
2. **DOCX uses Word Styles exclusively** (zero direct formatting runs)
3. **Navigation Pane shows full hierarchy** (Part → Chapter → Section → Subsection)
4. **TOC auto-generates** from heading styles
5. **Footnotes are native Word footnotes** (editable, renumbering works)
6. **No widow headings** (all headings `keep_with_next`)
7. **VNCH orthography clean** (zero Northern term flags in spot-check)
8. **Chapter structure valid**: exactly one chapter title per chapter; no duplicate headings; hierarchy intact
9. **Paragraph continuity verified**: no artificial splits/merges; cross-page joins validated
10. **Text integrity confirmed**: no duplicate/missing/reversed paragraphs; UNVERIFIED cases documented
11. **All deliverables produced** (7 reports + v2 builder + tests + updated dashboard)