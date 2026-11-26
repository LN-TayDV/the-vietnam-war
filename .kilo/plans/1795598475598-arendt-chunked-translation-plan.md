# Arendt Translation Plan — Chunked for Goal-Driven Execution

## Goal
Complete translation of remaining chapters (4-13) into Southern Vietnamese (VNCH) in small, resumable chunks, with QA and DOCX build per chapter. Each goal turn completes one chunk and checkpoints progress.

## Key Principle
Work is divided into atomic chunks of ~10 paragraphs (or 1 footnote batch). Each chunk: translate → append to v2 translation file → update checkpoint.json → stop. The Goal loop resumes from checkpoint next turn. Never attempt a full chapter in one turn.

## Chunk Definition
- **Paragraph chunk**: 10 consecutive untranslated paragraphs from a chapter's v2 source.
- **Footnote chunk**: 10 consecutive footnotes.
- **QA chunk**: run QA on one completed chapter.
- **DOCX chunk**: build DOCX for one completed chapter.

## Checkpoint Schema (`04_translation/v2/chNN/checkpoint.json`)
```json
{"chapter":"ch04","next_para":"V1C04-P014","next_fn":1,"paras_done":13,"fns_done":0,"status":"translating"}
```

## Execution Order
1. ch04 (P014-P034, then footnotes) → QA → DOCX
2. ch05 → ... → ch13

## Per-Turn Algorithm
1. Read checkpoint.json (or create if missing, starting P001).
2. Read next 10 paragraphs from chNN_src.txt.
3. Translate each per Grammar Engine 7-step + VNCH rules.
4. Append to v1_chNN_vi.txt in v2 structure.
5. Update checkpoint (next_para, paras_done).
6. If paragraphs remain, stop (goal continues next turn). Else move to footnotes, then QA, then DOCX, then next chapter.

## Validation Per Chunk
- Encoding UTF-8/NFC, no BOM, LF.
- Paragraph ID present and sequential.
- No placeholder text left.

## Blockers (genuine only)
- Missing source file.
- Encoding corruption.

## Files
- Source: `02_extracted_text/v2/chNN_src.txt`
- Output: `04_translation/v2/chNN/v1_chNN_vi.txt`
- Checkpoint: `04_translation/v2/chNN/checkpoint.json`
- Progress: `00_plan/progress.json`

## Notes
- Do not translate an entire chapter in one session.
- Footnote extraction from v1 OCR is incomplete; footnotes will be translated from v1 translation files when encountered.
- Chapters 4-13 only; 1-3 and prefaces already done.
