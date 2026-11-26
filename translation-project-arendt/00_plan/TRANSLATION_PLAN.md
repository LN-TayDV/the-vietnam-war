# TRANSLATION PLAN - THE ORIGINS OF TOTALITARIANISM

## Book Information
- **Title**: The Origins of Totalitarianism
- **Author**: Hannah Arendt
- **Edition**: New Edition with Added Prefaces (1973), Harcourt Brace Jovanovich
- **Pages**: 574 pages (PDF)
- **Chapters**: 13 chapters + 4 prefaces + front matter
- **Target Language**: Vietnamese (Southern, VNCH pre-1975 standard)

## Chapter Structure & Page Mapping

| # | Section | PDF Pages | Est. Words | Status |
|---|---------|-----------|------------|--------|
| 0 | Front Matter (Title, Copyright, Dedication) | 1-7 | ~1,000 | Pending |
| 1 | Preface to the First Edition | 8-10 | ~7,000 | Pending |
| 2 | Preface to Part One: Antisemitism | 11-16 | ~17,000 | Pending |
| 3 | Preface to Part Two: Imperialism | 17-22 | ~19,000 | Pending |
| 4 | Preface to Part Three: Totalitarianism | 23-41 | ~55,000 | Pending |
| 5 | Part One Intro: Antisemitism | 42-47 | ~2,800 | Pending |
| 6 | Chapter 1: Antisemitism as an Outrage to Common Sense | 48-55 | ~24,500 | **In Progress** |
| 7 | Chapter 2: The Jews, the Nation-State, and the Birth of Antisemitism | 56-98 | ~144,700 | Pending |
| 8 | Chapter 3: The Jews and Society | 99-133 | ~114,000 | Pending |
| 9 | Chapter 4: The Dreyfus Affair | 134-167 | ~109,800 | Pending |
| 10 | Chapter 5: The Political Emancipation of the Bourgeoisie | 168-202 | ~120,400 | Pending |
| 11 | Chapter 6: Race-Thinking Before Racism | 203-229 | ~88,700 | Pending |
| 12 | Chapter 7: Race and Bureaucracy | 230-266 | ~124,300 | Pending |
| 13 | Chapter 8: Continental Imperialism: the Pan-Movements | 267-311 | ~155,000 | Pending |
| 14 | Chapter 9: The Decline of the Nation-State and the End of the Rights of Man | 312-349 | ~127,900 | Pending |
| 15 | Chapter 10: A Classless Society | 350-387 | ~133,700 | Pending |
| 16 | Chapter 11: The Totalitarian Movement | 388-433 | ~164,800 | Pending |
| 17 | Chapter 12: Totalitarianism in Power | 434-504 | ~255,400 | Pending |
| 18 | Chapter 13: Ideology and Terror | 505-574 | ~212,400 | Pending |

**Total estimated words**: ~1,950,000 words

## Translation Workflow (per SKILL.md & STYLE_GUIDE_PHAN_B.md)

### Phase 1: Preparation (per chapter)
1. Read extracted text, mark paragraph boundaries with `[V1CNN-Pxxx] (trang X)`
2. Identify key terminology, names, concepts
3. Check against ARENDT_TERMINOLOGY.md and STYLE_GUIDE_PHAN_B.md

### Phase 2: Translation (per paragraph)
1. Apply 7-step Grammar Engine process:
   - Step 1: Phân tích ngữ pháp nguyên tác
   - Step 2: Xác định chủ thể, vị ngữ, đối tượng
   - Step 3: Phân tích quan hệ logic
   - Step 4: Xác định thuật ngữ theo ngữ cảnh
   - Step 5: Tái cấu trúc câu tiếng Việt tự nhiên (VNCH)
   - Step 6: Đối chiếu lại nguyên tác
   - Step 7: Kiểm tra tính dễ hiểu
2. Enforce VNCH rules: chớ/nầy/dầu/vả/trái lại/tuy vậy/bởi thế, thể khía đầy đủ, chủ động hóa, chỉ định danh từ, người ấy/ông ấy/bà ấy

### Phase 3: Quality Check (per chapter)
1. Paragraph alignment: src paragraphs == vi paragraphs
2. Sentence count match
3. No fabricate check
4. Orthography check (VNCH terms)
5. Encoding check (UTF-8, NFC, no BOM, LF)

### Phase 4: DOCX Build
1. Run build script to generate DOCX with footnotes at bottom of page
2. Verify Word Footnotes.Count matches progress.json

## Progress Tracking

Progress file: `00_plan/progress.json`

Status values: `pending` | `translating` | `translating_done` | `qa_pending` | `qa_done` | `docx_built` | `HOAN_TAT`

## Quality Gate (8 criteria - all must PASS)
1. Encoding: UTF-8/NFC/no BOM/LF
2. Orthography: 0× non-VNCH terms
3. Paragraph alignment: src = vi
4. Footnote alignment: src = vi
5. No fabricate
6. Natural VNCH style, no word-for-word
7. DOCX exists in 09_docx/
8. DOCX footnotes: OK N/N, Word Footnotes.Count = notes in progress.json

## Schedule
- Start: 2026-11-23
- Target: Complete all 18 sections
- Continuous translation without stopping between chapters

## Notes
- All work in `translation-project-arendt/` only
- Do not modify `translation-project/` (Vietnam War project)
- Use `99_scripts/` for book-specific scripts
- Terminology source of truth: `03_terminology/ARENDT_TERMINOLOGY.md`
- Style guide source of truth: `07_style_guide/STYLE_GUIDE_PHAN_B.md`