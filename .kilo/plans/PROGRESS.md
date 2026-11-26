# PROGRESS TRACKING — THE CAMBRIDGE HISTORY OF THE VIETNAM WAR (3 VOLUMES)

## PROJECT INFO

| Field | Value |
|-------|-------|
| Project | The Cambridge History of the Vietnam War |
| Source PDF | `books/The_Cambridge_History_of_the_Vietnam_War.pdf` |
| Total pages | 1866 |
| Total chapters | 77 |
| Encoding | UTF-8/NFC/no-BOM/LF |
| Language | Vietnamese (Southern, VNCH pre-1975) |
| Created | 2026-11-25 |
| Last updated | 2026-11-25 |
| Execution phase | 1 |

## STATUS VALUES

`pending` → `translating` → `translating_done` → `qa_pending` → `qa_done` → `docx_built` → `HOAN_TAT`
Additional: `needs_full_redo` (must be re-translated from source)

## VOLUME SUMMARY

| Volume | Chapters | Src Done | Trans Done | QA Done | DOCX Done | HOAN_TAT |
|--------|----------|----------|------------|---------|-----------|----------|
| Volume 1 | ch01-ch21 | 21 | 15 | 1 | 1 | 1 |
| Volume 2 | ch01-ch30 (v2) | 30 | 0 | 0 | 0 | 0 |
| Volume 3 | ch01-ch26 (v3) | 26 | 0 | 0 | 0 | 0 |
| **Total** | **77** | **77** | **15** | **1** | **1** | **1** |

## CHAPTER-LEVEL STATUS

| Chapter | Status | Issue | Footnotes |
|---------|--------|-------|-----------|
| V1-C01 | needs_full_redo | ISSUE-01: Arendt cross-contamination | TBD |
| V1-C02 | needs_qa | ISSUE-06: alignment + VNCH terms | TBD |
| V1-C03 | needs_qa | ISSUE-06: alignment + VNCH terms | TBD |
| V1-C04 | needs_qa | ISSUE-06: alignment + VNCH terms | TBD |
| V1-C05 | needs_qa | ISSUE-06: alignment + VNCH terms | TBD |
| V1-C06 | needs_qa | ISSUE-06: alignment + VNCH terms | TBD |
| V1-C07 | needs_qa | none | TBD |
| V1-C08 | needs_qa | ISSUE-05: nässig→này (fixed) | TBD |
| V1-C09 | needs_qa | none | TBD |
| V1-C10 | needs_qa | none | TBD |
| V1-C11 | needs_qa | ISSUE-02: missing 21 footnotes (BUG-008) | 21 missing |
| V1-C12 | needs_qa | ISSUE-03: missing 42 markers, dup [20] (BUG-001, BUG-003, BUG-009) | 42 missing |
| V1-C13 | needs_qa | none | TBD |
| V1-C14 | HOAN_TAT | ISSUE-04: was machine translation, rewritten | 76 |
| V1-C15 | needs_qa | none | TBD |
| V1-C16 | not_started | no translation directory | TBD |
| V1-C17 | not_started | no translation directory | TBD |
| V1-C18 | not_started | no translation directory | TBD |
| V1-C19 | not_started | no translation directory | TBD |
| V1-C20 | not_started | no translation directory | TBD |
| V1-C21 | not_started | no translation directory | TBD |
| V2-C01 through V2-C30 | not_started | Volume boundary TBD | TBD |
| V3-C01 through V3-C26 | not_started | Volume boundary TBD | TBD |

## KNOWN ISSUES

| ID | Description |
|----|-------------|
| ISSUE-01 | V1-C01: `v1_ch01_vi.txt` contains Arendt content — must re-translate from source |
| ISSUE-02 | V1-C11: Missing 21 footnotes (BUG-008) |
| ISSUE-03 | V1-C12: Missing 42 footnote markers, duplicate [20] (BUG-001, BUG-003, BUG-009) |
| ISSUE-04 | V1-C14: Was machine translation placeholder, already rewritten |
| ISSUE-05 | V1-C08: 'nässig' used 28 times — fixed (LANGUAGE_PURITY_REVIEW_V1-C08.md) |
| ISSUE-06 | V1-C01..C06: Alignment + VNCH term errors (222 fixes from AUDIT_REPORT_CH01-06.md) |
| ISSUE-07 | Old progress.json referenced Arendt book — replaced by this file |

## NEXT ACTIONS (Phase 1)

1. Verify V1-C01 source against extracted text
2. Delete contaminated V1-C01 translation
3. Re-translate V1-C01 from source
4. Fix V1-C11 missing 21 footnotes
5. Fix V1-C12 footnote markers
6. Confirm V1-C14 rewritten version is final
7. Verify VNCH orthography fixes applied to V1-C01..C06
8. Update this progress tracking after each step

## QUALITY GATE CRITERIA (ALL 8 MUST PASS BEFORE HOAN_TAT)

C1: Encoding (UTF-8/NFC/no-BOM/LF) | C2: Orthography (VNCH terms) | C3: Paragraph alignment (src=vi)
C4: Footnote alignment (src=vi) | C5: No fabricate | C6: VNCH style | C7: DOCX exists | C8: Word COM Footnotes.Count
