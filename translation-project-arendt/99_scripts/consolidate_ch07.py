"""
Consolidate Chapter 7 translation parts (_p1.._p9) into v1_ch07_vi.txt and run QA.

Parts already split at correct source page boundaries (230-266) with per-page
footnotes. This script concatenates them, normalizes to NFC/LF/no-BOM, and
verifies:
  - All source pages 230-266 present, no duplicates
  - Footnotes 1-103 present, sequential, no dupes/gaps
  - No forbidden U+2071 (superscript i) used as marker
"""
import re
import os
import unicodedata

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v1\ch07"
PARTS = ["_p1.txt", "_p2.txt", "_p3.txt", "_p4.txt", "_p5.txt",
         "_p6.txt", "_p7.txt", "_p8.txt", "_p9.txt"]

SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹'
SUP_MAP = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
fn_line_re = re.compile(r'^[' + SUP + r']')


def sup_to_int(s):
    return int(''.join(SUP_MAP[c] for c in s))


def read_part(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return f.read()


# --- Concatenate parts ---
chunks = []
for name in PARTS:
    txt = read_part(name)
    # normalize newlines to LF
    txt = txt.replace('\r\n', '\n').replace('\r', '\n')
    chunks.append(txt.rstrip('\n'))
consolidated = '\n\n'.join(chunks) + '\n'

# --- Normalize to NFC ---
consolidated = unicodedata.normalize('NFC', consolidated)

# --- QA: pages ---
pages = [int(x) for x in re.findall(r'=== PAGE (\d+) ===', consolidated)]
from collections import Counter
page_counts = Counter(pages)
dupes = {k: v for k, v in page_counts.items() if v > 1}
expected_pages = list(range(230, 267))
missing_pages = [p for p in expected_pages if p not in page_counts]
extra_pages = [p for p in page_counts if p not in expected_pages]

print("=== PAGE QA ===")
print(f"Total page markers: {len(pages)}")
print(f"Range: {min(pages)}..{max(pages)}")
print(f"Duplicates: {dupes if dupes else 'none'}")
print(f"Missing: {missing_pages if missing_pages else 'none'}")
print(f"Extra: {extra_pages if extra_pages else 'none'}")

# --- QA: footnotes (definitions = lines starting with superscript) ---
fn_defs = []
for line in consolidated.split('\n'):
    m = fn_line_re.match(line)
    if m:
        sup = ''
        for ch in line:
            if ch in SUP:
                sup += ch
            else:
                break
        try:
            fn_defs.append(sup_to_int(sup))
        except ValueError:
            pass

fn_counts = Counter(fn_defs)
fn_dupes = {k: v for k, v in fn_counts.items() if v > 1}
expected_fn = list(range(1, 104))
missing_fn = [n for n in expected_fn if n not in fn_counts]
extra_fn = [n for n in fn_counts if n not in expected_fn]

print("\n=== FOOTNOTE QA ===")
print(f"Total footnote definitions found: {len(fn_defs)}")
print(f"Sequence: {fn_defs[:5]} ... {fn_defs[-5:]}")
print(f"Duplicates: {fn_dupes if fn_dupes else 'none'}")
print(f"Missing (1-103): {missing_fn if missing_fn else 'none'}")
print(f"Extra (>103 or <1): {extra_fn if extra_fn else 'none'}")
print(f"Sequential in order: {fn_defs == list(range(1, 104))}")

# --- QA: forbidden U+2071 superscript i ---
bad_i = consolidated.count('\u2071')
print("\n=== ENCODING QA ===")
print(f"U+2071 (superscript i) count: {bad_i} (should be 0)")

# Check for BOM / CRLF
has_bom = consolidated.startswith('\ufeff')
has_cr = '\r' in consolidated
print(f"BOM present: {has_bom}")
print(f"CR present: {has_cr}")

# NFC check
print(f"Is NFC: {unicodedata.is_normalized('NFC', consolidated)}")

# --- Write consolidated file ---
out_path = os.path.join(BASE, 'v1_ch07_vi.txt')
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(consolidated)
print(f"\nWritten: {out_path}")
print(f"Size: {len(consolidated)} chars")