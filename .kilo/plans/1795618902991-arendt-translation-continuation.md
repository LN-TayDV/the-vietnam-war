# Arendt Translation Project - Continuation Plan

## Project Overview
- **Book**: The Origins of Totalitarianism by Hannah Arendt (1973 edition, 574 pages)
- **Target**: Vietnamese (VNCH pre-1975 Southern standard)
- **Current State**: 12/13 chapters completed (HOAN_TAT), Chapter 12 BLOCKED on footnotes 63-162
- **Project Directory**: `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt`

## Current Progress (from progress.json)

| Chapter | Status | Notes |
|---------|--------|-------|
| Front Matter | HOAN_TAT | 0 footnotes |
| Preface 1-4 | HOAN_TAT | 0 footnotes |
| Part One Intro | HOAN_TAT | 0 footnotes |
| Ch01-Ch11 | HOAN_TAT | All footnotes sequential, DOCX built |
| **Ch12** | **BLOCKED** | **Body: 71 paras translated. Footnotes 1-62 OK. Footnotes 63-162 MISSING (OCR-degraded, only ~35/100 recoverable)** |
| Ch13 | HOAN_TAT | 5 footnotes, DOCX built |
| **Master DOCX** | **BUILT** | 12 of 13 chapters combined |

## Key Issues to Resolve

### 1. Chapter 12 Footnote Blockage (CRITICAL)
- **Problem**: Footnotes 63-162 exist only as severely OCR-degraded inline fragments in English source
- **Impact**: Cannot build DOCX without all footnotes (docx_builder raises ValueError on orphan footnotes)
- **Body Translation**: Complete (71 paragraphs P001-P071, VNCH style, src=vi aligned)
- **Recovery Options**:
  - Re-extract from PDF with better OCR for pages 480-504
  - Manual reconstruction from context
  - Mark as [CẦN BỔ SUNG] with placeholder and proceed

### 2. DOCX Builder Issues
- Two implementations exist:
  - `99_scripts/build_chapter_docx.py` (project-specific, uses superscript digits ⁰¹²³⁴⁵⁶⁷⁸⁹)
  - `.kilo/scripts/common/docx_builder.py` (common library, uses [N] bracket markers)
- **Incompatibility**: Different marker formats, different parsing logic
- **Need**: Unified approach, fix for Chapter 12 footnote placement

### 3. GOAL Button - Workflow Management Interface
- No existing web interface found
- Need to create a simple HTML/JS dashboard showing:
  - Overall project goal
  - Current chapter goal
  - Actual progress vs targets
  - Next work items & missing Quality Gates
  - Quick links to MASTER_PLAN, progress.json, checkpoints

## Implementation Plan

### Phase 1: Fix Chapter 12 Footnotes (Priority 1)
1. **Re-extract source text** for Chapter 12 pages 480-504 with better OCR
2. **Recover missing footnotes** 63-162 from re-extracted text
3. **Integrate recovered footnotes** into `v1_ch12_vi.txt` with proper FOOTNOTES block
4. **Verify alignment** and run quality checks

### Phase 2: DOCX Builder Unification & Fixes (Priority 1)
1. **Audit both builders** for compatibility with Chapter 12 format
2. **Fix footnote placement logic** for chapters with missing inline markers
3. **Ensure consistent marker format** (prefer [N] bracket style as per common library)
4. **Test build** for Chapter 12 and verify Word Footnotes.Count

### Phase 3: Workflow Management Dashboard with GOAL Button (Priority 2)
1. **Create HTML dashboard** at `translation-project-arendt/dashboard.html`
2. **Implement GOAL button** with modal showing:
   - Project overview (total chapters, completed, blocked)
   - Current chapter status with detailed metrics
   - Progress bars vs targets
   - Next actionable steps
   - Quality Gate checklist status
   - Links to key files (MASTER_PLAN, progress.json, TRANSLATION_PLAN.md)
3. **Auto-refresh** from progress.json

### Phase 4: Quality Gates & Finalization (Priority 2)
1. Run all quality checks on Chapter 12:
   - `encoding_checker.py`
   - `vnch_orthography.py`
   - `document_comparator.py`
   - `quality_gate.py`
   - `audit_chapter.py` (if exists for Arendt project)
2. Build Chapter 12 DOCX
3. Rebuild Master DOCX with all 13 chapters
4. Update progress.json with final status

## Detailed Task Breakdown

### Task 1.1: Re-extract Chapter 12 Source (Pages 480-504)
- Use `extract_chapters.py` or `ocr_reconstruct.py` with improved settings
- Focus on footnote areas (bottom of pages)
- Save to `02_extracted_text/v2/ch12_recover.txt`

### Task 1.2: Recover Footnotes 63-162
- Parse recovered text for footnote definitions
- Translate recovered footnotes to VNCH Vietnamese
- Map to correct paragraph positions using page numbers

### Task 1.3: Update v1_ch12_vi.txt
- Add `=== FOOTNOTES ===` block with all 162 footnotes
- Ensure inline markers (⁰¹²³⁴⁵⁶⁷⁸⁹ or [N]) match footnote numbers
- Verify paragraph count = 71 (src=vi alignment)

### Task 2.1: Analyze Builder Differences
| Feature | build_chapter_docx.py | docx_builder.py |
|---------|----------------------|-----------------|
| Markers | Superscript digits (¹²³) | [N] brackets |
| Parsing | Custom regex | P_HDR, FN_BRACKET, FN_BARE |
| Footnotes | Real Word footnotes | Real Word footnotes |
| Sections | SECTION_RE (I..VI) | "đề mục" label in header |
| Images | Not handled | _insert_chapter_images |

### Task 2.2: Choose Strategy
**Recommendation**: Use common `docx_builder.py` as primary, adapt Chapter 12 format to match expected [N] bracket markers. The common library is more robust and used by the Vietnam War project.

### Task 3.1: Create Dashboard HTML
- Single-file HTML with embedded CSS/JS
- Read `progress.json` via fetch
- GOAL button triggers modal with detailed view
- Responsive, works offline

### Task 4.1: Quality Gate Execution
Run in sequence:
1. `python .kilo/scripts/common/encoding_checker.py --chapter 12`
2. `python .kilo/scripts/common/vnch_orthography.py --chapter 12`
3. `python .kilo/scripts/common/document_comparator.py --chapter 12`
4. `python .kilo/scripts/common/quality_gate.py --chapter 12`
5. `python 99_scripts/build_chapter_docx.py ch12` (or common builder)

## File Paths Reference

| Purpose | Path |
|---------|------|
| Progress checkpoint | `translation-project-arendt/00_plan/progress.json` |
| Master plan | `translation-project-arendt/00_plan/TRANSLATION_PLAN.md` |
| Chapter 12 translation | `translation-project-arendt/04_translation/v2/ch12/v1_ch12_vi.txt` |
| Chapter 12 source | `translation-project-arendt/02_extracted_text/v2/ch12_src.txt` |
| Project scripts | `translation-project-arendt/99_scripts/` |
| Common scripts | `.kilo/scripts/common/` |
| Output DOCX | `translation-project-arendt/09_docx/` |
| Dashboard (new) | `translation-project-arendt/dashboard.html` |

## Success Criteria

1. ✅ Chapter 12: All 162 footnotes recovered and integrated
2. ✅ Chapter 12: DOCX builds successfully with `OK 162/162`
3. ✅ Master DOCX: Rebuilt with all 13 chapters
4. ✅ Quality Gates: All 8 criteria PASS for Chapter 12
5. ✅ Dashboard: GOAL button functional, shows accurate progress
6. ✅ progress.json: Updated with `ch12.status = "HOAN_TAT"`

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Footnotes 63-162 unrecoverable | Use [CẦN BỔ SUNG] placeholders with English source reference, mark in progress.json |
| Builder incompatibility | Write adapter to convert v1_ch12_vi.txt format to common builder expectations |
| OCR quality insufficient | Manual reconstruction from context + PDF visual inspection |
| Time overrun | Prioritize Chapter 12 completion; dashboard can be minimal viable first |

## Next Immediate Actions

1. **Start Task 1.1**: Run improved OCR extraction on Chapter 12 pages 480-504
2. **Parallel**: Analyze Chapter 12 translation file format vs common builder expectations
3. **Then**: Recover and translate missing footnotes
4. **Finally**: Build DOCX, run quality gates, create dashboard