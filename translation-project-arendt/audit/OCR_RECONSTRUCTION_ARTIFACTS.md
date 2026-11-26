# OCR / Paragraph Reconstruction Artifacts Document

Based on `reconstruction_report.json` and analysis of v1 vs v2 source files.

## Reconstruction Report Summary

The `reconstruction_report.json` documents the paragraph count per chapter in the v2 clean source extraction:

| Chapter | Paragraphs | Pages | Footnotes (in report) |
|---------|-----------|-------|----------------------|
| front_matter | 5 | 7 | 0 |
| preface_first_edition | 2 | 3 | 0 |
| preface_part_one | 4 | 6 | 0 |
| preface_part_two | 4 | 6 | 0 |
| preface_part_three | 13 | 19 | 0 |
| part_one_intro | 4 | 6 | 0 |
| ch01 | 5 | 8 | 0 |
| ch02 | 40 | 43 | 0 |
| ch03 | 35 | 35 | 0 |
| ch04 | 34 | 34 | 0 |
| ch05 | 37 | 35 | 0 |
| ch06 | 29 | 27 | 0 |
| ch07 | 39 | 37 | 0 |
| ch08 | 44 | 45 | 0 |
| ch09 | 36 | 38 | 0 |
| ch10 | 37 | 38 | 0 |
| ch11 | 43 | 46 | 0 |
| ch12 | 71 | 71 | 0 |
| ch13 | 61 | 70 | 0 |

## Key Observations

### 1. Front Matter & Prefaces (No v2 Translation Files)
- The reconstruction report shows paragraph counts for front matter and 4 prefaces, but these don't have corresponding v2 translation files in `04_translation/v2/`
- This explains why `debug_align.py` skipped them
- These need v2 translation files created for full audit coverage

### 2. Chapter Paragraph Alignment
- All 13 chapters (ch01-ch13) show **perfect paragraph alignment** between v2 source and v2 translation
- Each chapter's v2 translation has exactly the same paragraph IDs and count as the v2 source
- This confirms Rule 18 (source paragraph count == VI paragraph count) is satisfied for all chapters

### 3. OCR Artifacts in ch12 (Critical)
From the plan and direct inspection of `v1_ch12_vi.txt`:

**Embedded Page Header Artifacts:**
- Lines like `=== PAGE 435 === 390 TOÀN TRỊ CHỦ NGHĨA` appear merged into footnote definitions (line 615 in footnotes block)
- Lines like `=== PAGE 438 === TOTALITARIANISM IN POWER 393` similarly embedded
- These are OCR artifacts from PDF page headers that survived into the translation

**Inline Footnote Definitions in Body:**
- Lines 9-11 show footnote ¹ and ² definitions appearing as standalone body paragraphs
- The parser must handle both inline defs and marker-only refs

**Duplicate Body Content:**
- Lines 86-88 and 118-120 are verbatim duplicates (same text about Nazi office duplication)
- This is a text integrity issue the audit must catch

**Untranslated English Fragments in ch12:**
- `preceded`, `giuramento`, `stakes`, `circumscribe`, `counter`, `fantastique`, `altogether`, `autonomous`, `turns out`
- These need VNCH orthography audit flags

**Cyrillic/Latin Artifacts in ch12 Footnotes:**
- `строго speaking` (Cyrillic `строго`) on footnote line 615
- OCR artifacts survived translation

### 4. Footnote Recovery Status per Chapter

| Chapter | Total Footnotes | Recovery Notes |
|---------|-----------------|----------------|
| ch01 | 0 | No footnotes |
| ch02 | 21 | Reindexed from 40..61 → 1..21 |
| ch03 | 79 | ALL 79 inline body markers dropped in v1; placed deterministically at owning-page paragraph ends via fn_page |
| ch04 | 100 | Recovered missing fn 35-39; inserted dropped inline markers 7,8 (p136) and 70 (p154) |
| ch05 | 60 | Auto-inserted 3 missing body markers (1,7,9) at sentence boundaries |
| ch06 | 65 | All markers present |
| ch07 | 103 | All markers present |
| ch08 | 98 | 7 missing body markers placed at owning-page paragraph ends |
| ch09 | 54 | Auto-inserted 2 missing body markers (27,38) |
| ch10 | 65 | Auto-inserted 1 missing body marker (26) |
| ch11 | 103 | Reindexed 5..107 → 1..103; 5 missing body markers placed |
| ch12 | 139 | 63 translated from _p1/_p2, 37 recovered from OCR, 39 placeholders for unrecoverable OCR; fns 72,154,158 lack body anchors |
| ch13 | 5 | 5 footnotes sequential 1..5 |

### 5. Part Files for Footnote Provenance

Key chapters with `_p1.txt`, `_p2.txt` etc. that contain footnote translations:

- **ch04**: 5 part files (_p1 through _p5) - used for recovering missing fn 35-39
- **ch05**: 3 part files (_p1, _p2, _p3) - _p3 has footnotes
- **ch07**: 9 part files (_p1 through _p9)
- **ch08**: 4 part files (_p1 through _p4) - _p4 has footnotes
- **ch10**: 10 part files (_p1 through _p9, plus _p4b)
- **ch11**: 9 part files (_p1 through _p8, plus _p6b) - _p6/_p6b gap for fn 75
- **ch12**: 2 part files (_p1, _p2) - used for fns 1-63 and 64-158 recovery

### 6. VNCH Orthography Issues (Systematic)

The translation inventory shows widespread patterns needing review:

1. **`chính phủ` → `chánh phủ`** (ch07: 1 occurrence, others may have)
2. **`quốc gia`** - context dependent, appears frequently (5-106 per chapter)
3. **`được` passive overuse** - 51-212 per chapter (Northern pattern)
4. **`cái` classifier overuse** - 2-155 per chapter (Northern pattern)
5. **`rất` vs `quá`** - 5-27 per chapter (Northern prefers `rất`)
6. **`thứ trưởng` → `bộ trưởng`** (ch08: 1 occurrence)

### 7. Cross-Page Continuity Issues

From the plan, the cross-page merge heuristic needs to handle:
- Lowercase start of paragraph + no terminal punctuation on previous = likely continuation
- Hyphenated word at page end = likely split word
- Roman/Arabic numeral at page start = likely heading (keep separate)
- Capitalized sentence start + previous ended with period = likely new paragraph

### 8. Heading Detection Gaps

Current parser only detects:
- Roman numerals (I-VI) → Heading 2
- Arabic numerals (1, 2, 3...) standalone → Heading 3
- ALL-CAPS short titles (≤60 chars) → Heading 4

Missing:
- Chapter title detection (first paragraph after book title)
- Part heading detection
- Lower-level subsections (a, b, c / 1.1, 1.2...)
- Block quote detection (indented + citation)
- Bibliography/Index detection (ch13)

---

## Next Steps for Phase 1 Audit

1. **Source Quality Audit**: Compare v1 OCR source vs v2 clean source per chapter
2. **Paragraph Reconstruction Audit**: Verify 1:1 mapping, detect splits/merges
3. **Chapter Structure & Heading Audit**: Apply full heading hierarchy validation
4. **Paragraph Structure & Cross-Page Continuity Audit**: Check all page boundaries
5. **Full Text Integrity Audit**: Detect duplicates, missing, reversed paragraphs
6. **Translation Alignment Audit**: Already PASS for all 13 chapters
7. **VNCH Quality Audit**: Apply STYLE_GUIDE_PHAN_B.md rules systematically
8. **Footnote & Citation Audit**: Verify all markers have defs, sequential numbering
9. **Structural Element Detection**: Find block quotes, bibliography, index, tables