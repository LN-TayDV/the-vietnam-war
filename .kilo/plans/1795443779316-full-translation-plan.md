# FULL TRANSLATION PLAN - THE ORIGINS OF TOTALITARIANISM

## Book Information
- **Title**: The Origins of Totalitarianism
- **Author**: Hannah Arendt
- **Edition**: New Edition with Added Prefaces (1973), Harcourt Brace Jovanovich
- **Pages**: 574 pages (PDF)
- **Chapters**: 13 chapters + 4 prefaces + front matter
- **Target Language**: Vietnamese (Southern, VNCH pre-1975 standard)

## Current Progress

| # | Section | PDF Pages | Status |
|---|---------|-----------|--------|
| 1 | Front Matter | 1-7 | ✅ DONE |
| 2 | Preface to First Edition | 8-10 | ✅ DONE |
| 3 | Preface to Part One | 11-16 | ✅ DONE |
| 4 | Preface to Part Two | 17-22 | ✅ DONE |
| 5 | Preface to Part Three | 23-41 | ✅ DONE |
| 6 | Part One Intro | 42-47 | ✅ DONE |
| 7 | Chapter 1 | 48-55 | ✅ DONE |
| 8 | Chapter 2 | 56-98 | ✅ DONE |
| 9 | **Chapter 3** | 99-133 | ✅ DONE |
| 10 | **Chapter 4: The Dreyfus Affair** | 134-167 | ⏳ PENDING |
| 11 | **Chapter 5: Political Emancipation of the Bourgeoisie** | 168-202 | ⏳ PENDING |
| 12 | **Chapter 6: Race-Thinking Before Racism** | 203-229 | ⏳ PENDING |
| 13 | **Chapter 7: Race and Bureaucracy** | 230-266 | ⏳ PENDING |
| 14 | **Chapter 8: Continental Imperialism: the Pan-Movements** | 267-311 | ⏳ PENDING |
| 15 | **Chapter 9: Decline of the Nation-State** | 312-349 | ⏳ PENDING |
| 16 | **Chapter 10: A Classless Society** | 350-387 | ⏳ PENDING |
| 17 | **Chapter 11: The Totalitarian Movement** | 388-433 | ⏳ PENDING |
| 18 | **Chapter 12: Totalitarianism in Power** | 434-504 | ⏳ PENDING |
| 19 | **Chapter 13: Ideology and Terror** | 505-574 | ⏳ PENDING |

## Remaining Work: 10 sections (Chapters 4-13) = ~1,236,000 words

## Translation Workflow (per translation-workflow SKILL.md)

### Phase 1: Preparation (per chapter)
1. Read extracted text from `02_extracted_text/v1/chXX.txt`
2. Mark paragraph boundaries with `[V1CNN-Pxxx] (trang X)`
3. Identify key terminology, names, concepts
4. Check against `03_terminology/ARENDT_TERMINOLOGY.md` and `07_style_guide/STYLE_GUIDE_PHAN_B.md`

### Phase 2: Translation (per paragraph)
1. Apply 7-step Grammar Engine process:
   - Step 1: Phân tích ngữ pháp nguyên tác
   - Step 2: Xác định chủ thể, vị ngữ, đối tượng
   - Step 3: Phân tích quan hệ logic
   - Step 4: Xác định thuật ngữ theo ngữ cảnh
   - Step 5: Tái cấu trúc câu tiếng Việt tự nhiên (VNCH)
   - Step 6: Đối chiếu lại nguyên tác
   - Step 7: Kiểm tra tính dễ hiểu
2. Enforce VNCH rules:
   - Connectives: chớ/nầy/dầu/vả/trái lại/tuy vậy/bởi thế
   - Complete aspects (thể khía)
   - Active voice (chủ động hóa)
   - Noun determiners (chỉ định danh từ)
   - Proper pronouns: người ấy/ông ấy/bà ấy

### Phase 3: Quality Check (per chapter)
1. Paragraph alignment: src paragraphs == vi paragraphs
2. Sentence count match
3. No fabricate check
4. Orthography check (VNCH terms per STYLE_GUIDE_PHAN_B.md)
5. Encoding check (UTF-8, NFC, no BOM, LF)

### Phase 4: DOCX Build (per chapter)
1. Run build script to generate DOCX with footnotes at bottom of page
2. Verify Word Footnotes.Count matches progress.json

## Execution Order
Translate sequentially: Chapter 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13
No stopping between chapters - continuous translation as per user directive.

## File Structure
- Source: `02_extracted_text/v1/chXX.txt`
- Output: `04_translation/v1/chXX/v1_chXX_vi.txt`
- Terminology: `03_terminology/ARENDT_TERMINOLOGY.md` (source of truth)
- Style: `07_style_guide/STYLE_GUIDE_PHAN_B.md` (source of truth)

## Quality Gate (8 criteria - all must PASS)
1. Encoding: UTF-8/NFC/no BOM/LF
2. Orthography: 0× non-VNCH terms
3. Paragraph alignment: src = vi
4. Footnote alignment: src = vi
5. No fabricate
6. Natural VNCH style, no word-for-word
7. DOCX exists in 09_docx/
8. DOCX footnotes: OK N/N, Word Footnotes.Count = notes in progress.json

## Progress Tracking
- File: `00_plan/progress.json`
- Status values: `pending` → `translating` → `translating_done` → `qa_pending` → `qa_done` → `docx_built` → `HOAN_TAT`

## Notes
- All work in `translation-project-arendt/` only
- Do not modify `translation-project/` (Vietnam War project)
- Use `99_scripts/` for book-specific scripts
- Continuous translation without stopping between chapters
- Update `ARENDT_TERMINOLOGY.md` with new terms as encountered