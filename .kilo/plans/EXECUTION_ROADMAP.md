# EXECUTION ROADMAP — THE CAMBRIDGE HISTORY OF THE VIETNAM WAR (3 VOLUMES)

## PHASE 1 — AUDIT & FIX EXISTING WORK (Volume 1, ch01-ch15)

**Goal:** Fix all known issues before any new translation. Do not start new translations until Phase 1 is complete.

| Step | Action | Chapter(s) | Deliverable | Dependency |
|------|--------|------------|-------------|------------|
| 1.1 | Verify `v1_ch01_src.txt` matches `02_extracted_text/v1/ch01.txt` | Ch01 | Source verification report | None |
| 1.2 | Delete contaminated `v1_ch01_vi.txt` (contains Arendt content) | Ch01 | Clean slate | 1.1 |
| 1.3 | Re-translate Ch01 from `02_extracted_text/v1/ch01.txt` | Ch01 | New `v1_ch01_vi.txt` | 1.2 |
| 1.4 | Extract 21 missing footnotes from `ch11.txt`, translate, add to `v1_ch11_vi.txt` | Ch11 | Footnote block added | None |
| 1.5 | Fix footnote markers, remove duplicate [20], re-align Ch12 | Ch12 | Fixed markers, alignment restored | None |
| 1.6 | Confirm rewritten Ch14 translation is final version | Ch14 | Confirmation note | None |
| 1.7 | Verify VNCH orthography fixes applied to Ch01-C06 | Ch01-C06 | Verification report | None |
| 1.8 | Create `progress.json` with correct chapter statuses (not Arendt) | All | `progress.json` | 1.1-1.7 |

**Phase 1 exit criteria:** All ISSUE-01 to ISSUE-07 resolved. `progress.json` reflects actual state. No chapter has contaminated or placeholder content.

---

## PHASE 2 — COMPLETE VOLUME 1 TRANSLATIONS (ch16-ch21)

**Goal:** Translate the 6 chapters that have source text but no translation.

| Step | Action | Chapter(s) | Deliverable | Dependency |
|------|--------|------------|-------------|------------|
| 2.1 | Translate Ch16 from `02_extracted_text/v1/ch16.txt` | Ch16 | `v1_ch16_src.txt` + `v1_ch16_vi.txt` | Phase 1 done |
| 2.2 | Translate Ch17 from `02_extracted_text/v1/ch17.txt` | Ch17 | `v1_ch17_src.txt` + `v1_ch17_vi.txt` | 2.1 |
| 2.3 | Translate Ch18 from `02_extracted_text/v1/ch18.txt` | Ch18 | `v1_ch18_src.txt` + `v1_ch18_vi.txt` | 2.2 |
| 2.4 | Translate Ch19 from `02_extracted_text/v1/ch19.txt` | Ch19 | `v1_ch19_src.txt` + `v1_ch19_vi.txt` | 2.3 |
| 2.5 | Translate Ch20 from `02_extracted_text/v1/ch20.txt` | Ch20 | `v1_ch20_src.txt` + `v1_ch20_vi.txt` | 2.4 |
| 2.6 | Translate Ch21 from `02_extracted_text/v1/ch21.txt` | Ch21 | `v1_ch21_src.txt` + `v1_ch21_vi.txt` | 2.5 |

**Phase 2 exit criteria:** All ch16-ch21 have `v1_chXX_src.txt` and `v1_chXX_vi.txt` with 1:1 paragraph alignment.

---

## PHASE 3 — VOLUME 1 QA + DOCX (ch01-ch21)

**Goal:** QA all Volume 1 chapters and build DOCX files.

| Step | Action | Chapter(s) | Deliverable | Dependency |
|------|--------|------------|-------------|------------|
| 3.1 | Run paragraph alignment check (src=vi paragraph count) | Ch01-Ch21 | Alignment reports | Phase 2 done |
| 3.2 | Run VNCH orthography check (Style Guide Phan B) | Ch01-Ch21 | Orthography reports | 3.1 |
| 3.3 | Run footnote alignment check (src count = vi count) | Ch01-Ch21 | Footnote reports | 3.2 |
| 3.4 | Fix any alignment/orthography/footnote issues found | Ch01-Ch21 | Fixed files | 3.3 |
| 3.5 | Build DOCX for each chapter with Word native footnotes | Ch01-Ch21 | 21 DOCX files in `09_docx/` | 3.4 |
| 3.6 | Word COM verify Footnotes.Count matches progress.json | Ch01-Ch21 | Validation reports | 3.5 |
| 3.7 | Mark all Volume 1 chapters HOAN_TAT | Ch01-Ch21 | Updated `progress.json` | 3.6 |

**Phase 3 exit criteria:** All 21 Volume 1 chapters HOAN_TAT. 21 DOCX files in `09_docx/`.

---

## PHASE 4 — VOLUME 2 TRANSLATIONS

**Goal:** Translate all Volume 2 chapters from v2 source.

| Step | Action | Chapter(s) | Deliverable | Dependency |
|------|--------|------------|-------------|------------|
| 4.1 | Confirm Volume 2 chapter boundaries (which chapters belong to V2) | All | Boundary confirmation | Phase 3 done |
| 4.2 | Verify v2 source for each chapter against PDF | All | Source verification reports | 4.1 |
| 4.3 | Translate chapters sequentially from v2 source | All | `v2_chXX_src.txt` + `v2_chXX_vi.txt` | 4.2 |
| 4.4 | Apply VNCH orthography + Style Guide rules | All | Fixed translations | 4.3 |
| 4.5 | Add footnotes from source | All | Footnote blocks in vi files | 4.4 |

**Phase 4 exit criteria:** All Volume 2 chapters translated with footnotes.

---

## PHASE 5 — VOLUME 3 TRANSLATIONS

**Goal:** Translate all Volume 3 chapters from v3 source.

| Step | Action | Chapter(s) | Deliverable | Dependency |
|------|--------|------------|-------------|------------|
| 5.1 | Confirm Volume 3 chapter boundaries (which chapters belong to V3) | All | Boundary confirmation | Phase 4 done |
| 5.2 | Verify v3 source for each chapter against PDF | All | Source verification reports | 5.1 |
| 5.3 | Translate chapters sequentially from v3 source | All | `v3_chXX_src.txt` + `v3_chXX_vi.txt` | 5.2 |
| 5.4 | Apply VNCH orthography + Style Guide rules | All | Fixed translations | 5.3 |
| 5.5 | Add footnotes from source | All | Footnote blocks in vi files | 5.4 |

**Phase 5 exit criteria:** All Volume 3 chapters translated with footnotes.

---

## PHASE 6 — VOLUME 2 & VOLUME 3 QA + DOCX

**Goal:** QA and build DOCX for all remaining chapters.

| Step | Action | Volume(s) | Deliverable | Dependency |
|------|--------|-----------|-------------|------------|
| 6.1 | Run paragraph alignment check (src=vi) | V2, V3 | Alignment reports | Phase 5 done |
| 6.2 | Run VNCH orthography check | V2, V3 | Orthography reports | 6.1 |
| 6.3 | Run footnote alignment check | V2, V3 | Footnote reports | 6.2 |
| 6.4 | Fix any issues found | V2, V3 | Fixed files | 6.3 |
| 6.5 | Build DOCX for each chapter | V2, V3 | DOCX files in `09_docx/` | 6.4 |
| 6.6 | Word COM verify Footnotes.Count | V2, V3 | Validation reports | 6.5 |
| 6.7 | Mark all Volume 2 and 3 chapters HOAN_TAT | V2, V3 | Updated `progress.json` | 6.6 |

**Phase 6 exit criteria:** All 77 chapters HOAN_TAT. All DOCX files in `09_docx/`.

---

## PHASE 7 — FINAL VALIDATION + MASTER DOCX

**Goal:** Final validation and master DOCX for the complete 3-volume work.

| Step | Action | Deliverable | Dependency |
|------|--------|-------------|------------|
| 7.1 | Verify all 77 chapters HOAN_TAT in `progress.json` | Final progress.json | Phase 6 done |
| 7.2 | Build master DOCX (complete 3-volume book) | Master DOCX in `09_docx/` | 7.1 |
| 7.3 | Run final quality gate on master DOCX | Quality gate report | 7.2 |
| 7.4 | Archive and backup | Backup directory | 7.3 |

**Phase 7 exit criteria:** All chapters HOAN_TAT. Master DOCX passes quality gate.

---

## SEQUENCING RULES

1. Phases must be executed in order: 1 → 2 → 3 → 4 → 5 → 6 → 7
2. No new translation until Phase 1 audit is complete
3. No QA until translation is complete for that chapter
4. No DOCX until QA passes for that chapter
5. No HOAN_TAT until all 8 quality gate criteria PASS
6. Chapters within a phase are done sequentially (no parallel translation)
7. `progress.json` is the source of truth — update after each step

---

## DEPENDENCIES & RISKS

| Risk | Impact | Mitigation |
|------|--------|------------|
| Volume boundaries unknown (v1/v2/v3 all start at ch01) | High | Confirm during Phase 1 before Phase 4 |
| Page ranges unknown for most chapters | Medium | Verify from extracted text during QA |
| Ch01 source may also be contaminated | High | Verify against PDF in Step 1.1 |
| ch16-ch21 have no translation directory | Medium | Create from scratch in Phase 2 |
| No existing v2/v3 translation to reference | High | All translations from scratch |
