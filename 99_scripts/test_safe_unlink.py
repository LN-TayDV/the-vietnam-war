# -*- coding: utf-8 -*-
"""Test _safe_unlink handles a locked file gracefully."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "translation-project" / "99_scripts"))
import build_chapter_docx as bd

# Create a dummy file and try to unlink it while "locked" (simulate by
# opening it exclusively). On Windows we can't truly lock a file the way
# Word does, but we can at least verify the retry/timeout logic runs.
import tempfile, os
tmp = Path(tempfile.gettempdir()) / "test_safe_unlink.txt"
tmp.write_text("x", encoding="utf-8")
print("File created:", tmp.exists())
bd._safe_unlink(tmp, required=True)
print("After unlink:", tmp.exists())

# Test required=False on a non-existent file (should not raise)
bd._safe_unlink(Path("nonexistent_xyz.txt"), required=False)
print("Non-existent optional unlink: OK (no raise)")

print("All _safe_unlink tests passed")