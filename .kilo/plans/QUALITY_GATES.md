# QUALITY GATES — THE CAMBRIDGE HISTORY OF THE VIETNAM WAR (3 VOLUMES)

## 1. EIGHT QUALITY CRITERIA (ALL MUST PASS BEFORE HOAN_TAT)

| # | Criterion | Standard | Pass Condition | Check Method |
|---|-----------|----------|----------------|--------------|
| C1 | Encoding | UTF-8, NFC, no BOM, LF | Both src and vi files | `encoding_checker.py` |
| C2 | Orthography | 0× non-VNCH terms (CRITICAL/MAJOR) | No `chính trị`, `chính phủ`, `này`, etc. in VNCH context | `apply_vnch_fixes.py` + manual review |
| C3 | Paragraph alignment | src paragraphs = vi paragraphs | Same count, same order, same IDs | `document_comparator.py` |
| C4 | Footnote alignment | src footnotes = vi footnotes | Same count, sequential 1..N | Manual + `quality_gate.py` |
| C5 | No fabricate | No added/omitted information | Every vi paragraph maps to src paragraph | Sentence-by-sentence review |
| C6 | VNCH style | Natural VNCH, no word-for-word | Passes Style Guide Phan B + Grammar Engine | Independent read-through |
| C7 | DOCX exists | DOCX in `09_docx/` | File opens in Word without errors | `build_chapter_docx.py` |
| C8 | DOCX footnotes | Word native footnotes (OOXML) | `Footnotes.Count` = notes in `progress.json` | Word COM verification |

## 2. PER-CRITERION DETAILS

### C1 — Encoding
- File encoding: UTF-8
- Unicode normalization: NFC
- BOM: Not allowed
- Line endings: LF only (not CRLF)
- Applies to: both `v1_chXX_src.txt` and `v1_chXX_vi.txt`

### C2 — Orthography (VNCH terms)
From Style Guide Phan B v2.3:
- `chính trị` → `chánh trị`
- `chính phủ` → `chánh phủ`
- `chính đảng` → `chánh đảng`
- `đảo chính` → `đảo chánh`
- `tài chính` → `tài chánh`
- `này` → `nầy` (in VNCH context)
- `Tuy nhiên` → `Tuy vậy`
- `ngược lại` → `trái lại`
- False positives allowed: names, titles, direct quotations, French terms in brackets

### C3 — Paragraph alignment
- Every `[V1CNN-Pxxx]` marker in src must have corresponding marker in vi
- Paragraph count must match exactly
- Paragraph order must match exactly
- No paragraph may be split or merged without documentation

### C4 — Footnote alignment
- Every footnote marker `[N]` in src must appear in vi
- Footnote count must match between src and vi
- Footnotes must be sequential 1..N with no gaps or duplicates
- Footnote content must be translated (not left in English/French)

### C5 — No fabricate
- No information added that is not in the source
- No information omitted from the source
- No meaning changed during translation
- Direct quotations must be accurate

### C6 — VNCH style
- Vocabulary from VNCH pre-1975 sources (Lê Văn Đức, Bách Khoa, Hiến pháp 1967)
- Connectives: `chớ`, `nầy`, `gởi`, `thơ`, `chừng nấy`
- No Northern terms: `đồng chí`, `ta/địch`, `giải phóng` (in inappropriate contexts)
- No modern terms: `chính phủ`, `đại biểu`, `tài chính`
- Grammar Engine 7-step process applied

### C7 — DOCX
- File exists in `09_docx/`
- Opens in Microsoft Word without errors
- All content present (no missing paragraphs)
- Headings formatted correctly
- Images and captions present (if applicable)

### C8 — DOCX footnotes
- Word native footnotes via OOXML (not simulated)
- `Footnotes.Count` in Word equals number of footnotes in `progress.json`
- Footnote markers `[N]` in body text match footnote numbers
- Footnote text appears at bottom of page (not end of chapter)

## 3. QUALITY GATE PROCESS

```
For each chapter:
  1. Run C1 (encoding check) → PASS/FAIL
  2. Run C2 (orthography check) → PASS/FAIL
  3. Run C3 (paragraph alignment) → PASS/FAIL
  4. Run C4 (footnote alignment) → PASS/FAIL
  5. Run C5 (no fabricate review) → PASS/FAIL
  6. Run C6 (VNCH style review) → PASS/FAIL
  7. Run C7 (DOCX build) → PASS/FAIL
  8. Run C8 (Word COM footnote verify) → PASS/FAIL
  If all 8 PASS → mark HOAN_TAT
  If any FAIL → fix and re-run from step 1
```

## 4. SCRIPTS FOR QUALITY GATE

| Script | Location | Purpose |
|--------|----------|---------|
| `encoding_checker.py` | `99_scripts/common/` | C1 — UTF-8/NFC/no-BOM/LF |
| `vnch_orthography.py` | `99_scripts/common/` | C2 — VNCH term violations |
| `document_comparator.py` | `99_scripts/common/` | C3 — Paragraph alignment |
| `quality_gate.py` | `99_scripts/common/` | C4 — Footnote alignment |
| `translation_validator.py` | `99_scripts/common/` | C5/C6 — No fabricate + VNCH style |
| `docx_builder.py` | `99_scripts/common/` | C7 — DOCX build |
| `audit_docx_format.py` | `99_scripts/` | C7/C8 — DOCX format audit |

## 5. FAILURE HANDLING

| Failure | Action |
|---------|--------|
| C1 FAIL | Re-encode file with UTF-8/NFC/LF |
| C2 FAIL | Apply `vnch_orthography.py` fixes, manual review for false positives |
| C3 FAIL | Re-align paragraphs, re-translate split/merged paragraphs |
| C4 FAIL | Add missing footnotes, fix duplicate markers |
| C5 FAIL | Re-translate affected paragraphs |
| C6 FAIL | Rewrite sentences for natural VNCH style |
| C7 FAIL | Fix DOCX build script, rebuild |
| C8 FAIL | Add missing footnote blocks, rebuild DOCX, re-verify |

## 6. SIGN-OFF

| Role | Responsibility |
|------|----------------|
| Translator | Ensures C1-C6 before submitting for QA |
| QA Reviewer | Runs C1-C8, confirms all PASS |
| Project Lead | Approves HOAN_TAT status, updates `progress.json` |
