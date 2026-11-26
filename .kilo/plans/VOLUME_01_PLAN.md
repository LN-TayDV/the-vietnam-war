# VOLUME 1 PLAN — THE CAMBRIDGE HISTORY OF THE VIETNAM WAR

## 1. VOLUME METADATA

| Field | Value |
|-------|-------|
| Volume | Volume 1 |
| Source PDF | `books/The_Cambridge_History_of_the_Vietnam_War.pdf` |
| Chapters | ch01-ch21 (extracted text v1 covers ch01-ch21) |
| PDF page range | TBD — verify from extracted text |
| In-book page range | TBD — verify from extracted text |
| Translation status | ch01-ch15: translated (needs fixes); ch16-ch21: not started |

## 2. CHAPTER LIST WITH STATUS

| # | Chapter | PDF Pages | In Pages | Src Done | Trans Done | QA Done | DOCX Done | Status | Known Issues |
|---|---------|-----------|----------|----------|------------|---------|-----------|--------|--------------|
| 1 | Ch01 | TBD | TBD | ✅ | ❌ (Arendt content) | ❌ | ❌ | needs_full_redo | ISSUE-01: cross-contamination with Arendt |
| 2 | Ch02 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-06: alignment + VNCH terms |
| 3 | Ch03 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-06: alignment + VNCH terms |
| 4 | Ch04 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-06: alignment + VNCH terms |
| 5 | Ch05 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-06: alignment + VNCH terms |
| 6 | Ch06 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-06: alignment + VNCH terms |
| 7 | Ch07 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | — |
| 8 | Ch08 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-05: "nässig" → "này" (28×, fixed) |
| 9 | Ch09 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | — |
| 10 | Ch10 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | — |
| 11 | Ch11 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-02: missing 21 footnotes (BUG-008) |
| 12 | Ch12 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | ISSUE-03: missing 42 markers, duplicate [20] |
| 13 | Ch13 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | — |
| 14 | Ch14 | TBD | TBD | ✅ | ✅ | ✅ | ✅ | qa_passed | ISSUE-04: was machine translation, rewritten |
| 15 | Ch15 | TBD | TBD | ✅ | ✅ | ❌ | ❌ | needs_qa | — |
| 16 | Ch16 | TBD | TBD | ✅ | ❌ | ❌ | ❌ | not_started | No translation directory |
| 17 | Ch17 | TBD | TBD | ✅ | ❌ | ❌ | ❌ | not_started | No translation directory |
| 18 | Ch18 | TBD | TBD | ✅ | ❌ | ❌ | ❌ | not_started | No translation directory |
| 19 | Ch19 | TBD | TBD | ✅ | ❌ | ❌ | ❌ | not_started | No translation directory |
| 20 | Ch20 | TBD | TBD | ✅ | ❌ | ❌ | ❌ | not_started | No translation directory |
| 21 | Ch21 | TBD | TBD | ✅ | ❌ | ❌ | ❌ | not_started | No translation directory |

**Legend:** ✅ = done, ❌ = not started, needs_qa = translated but needs QA, needs_full_redo = must be re-translated

## 3. FRONT MATTER (Volume 1)

| Section | Status | Notes |
|---------|--------|-------|
| GI (General Introduction) | TBD | Check extracted text |
| Other front matter | TBD | Check extracted text |

## 4. PHASE 1 ACTIONS (Volume 1)

| Step | Action | Chapter(s) | Deliverable |
|------|--------|------------|-------------|
| 1.1 | Verify `v1_ch01_src.txt` matches `02_extracted_text/v1/ch01.txt` | Ch01 | Source verification report |
| 1.2 | Delete contaminated `v1_ch01_vi.txt`, re-translate from source | Ch01 | Clean `v1_ch01_vi.txt` |
| 1.3 | Extract 21 missing footnotes from `ch11.txt`, translate, add to `v1_ch11_vi.txt` | Ch11 | Footnote block added |
| 1.4 | Fix footnote markers, remove duplicate [20], re-align | Ch12 | Fixed markers, alignment restored |
| 1.5 | Confirm rewritten Ch14 translation is final version | Ch14 | Confirmation note |
| 1.6 | Verify VNCH orthography fixes applied to Ch01-C06 | Ch01-C06 | Verification report |
| 1.7 | Create `progress.json` with correct chapter statuses | All | `progress.json` |

## 5. PHASE 2 ACTIONS (Volume 1 — new translations)

| Step | Action | Chapter(s) | Deliverable |
|------|--------|------------|-------------|
| 2.1 | Translate Ch16 from `02_extracted_text/v1/ch16.txt` | Ch16 | `v1_ch16_src.txt` + `v1_ch16_vi.txt` |
| 2.2 | Translate Ch17 from `02_extracted_text/v1/ch17.txt` | Ch17 | `v1_ch17_src.txt` + `v1_ch17_vi.txt` |
| 2.3 | Translate Ch18 from `02_extracted_text/v1/ch18.txt` | Ch18 | `v1_ch18_src.txt` + `v1_ch18_vi.txt` |
| 2.4 | Translate Ch19 from `02_extracted_text/v1/ch19.txt` | Ch19 | `v1_ch19_src.txt` + `v1_ch19_vi.txt` |
| 2.5 | Translate Ch20 from `02_extracted_text/v1/ch20.txt` | Ch20 | `v1_ch20_src.txt` + `v1_ch20_vi.txt` |
| 2.6 | Translate Ch21 from `02_extracted_text/v1/ch21.txt` | Ch21 | `v1_ch21_src.txt` + `v1_ch21_vi.txt` |

## 6. PHASE 3 ACTIONS (Volume 1 — QA + DOCX)

| Step | Action | Chapter(s) | Deliverable |
|------|--------|------------|-------------|
| 3.1 | Run paragraph alignment check (src=vi) | Ch01-Ch21 | Alignment reports |
| 3.2 | Run VNCH orthography check | Ch01-Ch21 | Orthography reports |
| 3.3 | Run footnote alignment check | Ch01-Ch21 | Footnote reports |
| 3.4 | Build DOCX for each chapter | Ch01-Ch21 | 21 DOCX files in `09_docx/` |
| 3.5 | Word COM verify Footnotes.Count | Ch01-Ch21 | Validation reports |
| 3.6 | Mark all Volume 1 chapters HOAN_TAT | Ch01-Ch21 | Updated `progress.json` |

## 7. RISKS

- Page ranges unknown — must verify from extracted text before QA
- Volume boundary between V1/V2/V3 unclear — v1/v2/v3 all start at ch01
- Ch01 source may also be contaminated — verify against PDF
- ch16-ch21 have extracted text but no src/vi translation files — must create from scratch
