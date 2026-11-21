# Common Scripts for The Cambridge History of the Vietnam War Translation Project

## Overview
This directory contains reusable scripts for translation validation, quality assurance, and document processing. 

**Principle:** One function = one implementation. Skills call these scripts instead of reimplementing logic.

## Scripts

| Script | Purpose | Skills |
|--------|---------|--------|
| `file_integrity.py` | Check 2-file structure, encoding, paragraph counts | All |
| `translation_validator.py` | Scan English remaining, term consistency, empty content | translation-error-detection, quality-gate |
| `document_comparator.py` | Align src vs vi: paragraphs, sentences, footnotes | deep-review, error-detection |
| `quality_gate.py` | Run 8 Quality Gate criteria | quality-gate |
| `vnch_orthography.py` | Check 30 VNCH rules | editorial-style, error-detection |
| `encoding_checker.py` | UTF-8, NFC, no BOM, LF | quality-gate, error-detection |

## Usage

### From Python (Skills)
```python
from pathlib import Path
import subprocess

# Run quality gate
result = subprocess.run([
    "python", ".kilo/scripts/common/quality_gate.py",
    "--chapter", "7", "--json"
], capture_output=True, text=True, cwd=PROJECT_ROOT)
```

### From Command Line
```bash
# Check file integrity for chapter 7
python .kilo/scripts/common/file_integrity.py --chapter 7

# Validate translation for chapter 7
python .kilo/scripts/common/translation_validator.py --chapter 7

# Compare src vs vi for chapter 7
python .kilo/scripts/common/document_comparator.py --chapter 7

# Run full quality gate for chapter 7
python .kilo/scripts/common/quality_gate.py --chapter 7

# Check VNCH orthography for chapter 7
python .kilo/scripts/common/vnch_orthography.py --chapter 7

# Check encoding for chapter 7
python .kilo/scripts/common/encoding_checker.py --chapter 7
```

## Design Principles

1. **Single Implementation**: Each function has exactly one implementation here.
2. **JSON Output**: All scripts support `--json` for programmatic use.
3. **Exit Codes**: 0 = PASS, 1 = FAIL (for automation).
4. **No Side Effects**: Scripts only read, never write to project files.
5. **Common Interface**: `--chapter`, `--volume`, `--root`, `--json` standard args.

## Integration with Skills

Each skill document specifies which common scripts to call:
- `historical-book-translation` → `file_integrity.py`, `quality_gate.py`
- `contextual-translation` → `translation_validator.py`
- `southern-vietnamese-editorial-style` → `vnch_orthography.py`
- `deep-translation-review` → `document_comparator.py`, `translation_validator.py`
- `translation-error-detection` → all validators
- `translation-quality-gate` → `quality_gate.py` (orchestrates all)

## Adding New Scripts

1. Place in `.kilo/scripts/common/`
2. Follow interface: `--chapter`, `--volume`, `--root`, `--json`
3. Exit 0 on PASS, 1 on FAIL
4. Support `--json` for structured output
5. Update this README
6. Update relevant skill documents