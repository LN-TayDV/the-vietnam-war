"""
Deep QA for ch07 consolidated file:
1. Cross-check footnote markers (inline superscripts) vs definitions (line-start superscripts).
   Every footnote 1-103 must have exactly one definition AND at least one inline marker.
2. Scan for leftover English prose (common English function words) outside of
   proper nouns / titles / quoted foreign terms.
3. Report any body superscript number not in 1..103.
"""
import re
import os

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v1\ch07"
PATH = os.path.join(BASE, 'v1_ch07_vi.txt')

SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹'
SUP_MAP = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
sup_re = re.compile('[' + SUP + ']+')

def sup_to_int(s):
    return int(''.join(SUP_MAP[c] for c in s))

with open(PATH, 'r', encoding='utf-8') as f:
    text = f.read()

# --- 1. Footnote markers vs definitions ---
defs = []       # line-start superscripts
markers = []    # inline superscripts
for line in text.split('\n'):
    m = re.match('^([' + SUP + ']+)', line)
    if m:
        defs.append(sup_to_int(m.group(1)))
        # remainder of line may contain more superscripts? unlikely for def lines
    # collect all inline superscripts in the line
    for mm in sup_re.finditer(line):
        markers.append(sup_to_int(mm.group(0)))

# Remove the definition-leading occurrence from markers count for accuracy:
# A line that starts with a superscript def should not count that leading token as a marker.
markers2 = []
for line in text.split('\n'):
    stripped = line
    m = re.match('^([' + SUP + ']+)', line)
    if m:
        stripped = line[m.end():]
    for mm in sup_re.finditer(stripped):
        markers2.append(sup_to_int(mm.group(0)))

from collections import Counter
def_counts = Counter(defs)
mark_counts = Counter(markers2)

print("=== DEFINITION CHECK ===")
print(f"Definitions: {len(defs)} total, unique {len(def_counts)}")
print(f"Missing definitions: {[n for n in range(1,104) if n not in def_counts]}")
print(f"Duplicate definitions: { {k:v for k,v in def_counts.items() if v>1} }")

print("\n=== MARKER CHECK ===")
print(f"Inline markers: {len(markers2)} total")
missing_markers = [n for n in range(1, 104) if n not in mark_counts]
print(f"Footnotes with NO inline marker: {missing_markers}")
bad_markers = sorted(set(n for n in mark_counts if n < 1 or n > 103))
print(f"Out-of-range markers: {bad_markers if bad_markers else 'none'}")
multi = {k:v for k,v in mark_counts.items() if v > 2}
print(f"Footnotes marked >2 times (may indicate stray): {multi if multi else 'none'}")

# --- 2. English leftover scan ---
# Common English function words that should NOT appear as prose (Vietnamese translation).
# Proper nouns / book titles / quoted foreign phrases are allowed, so this is advisory.
eng_words = [' the ', ' and ', ' of ', ' to ', ' in ', ' that ', ' with ', ' for ',
             ' was ', ' were ', ' which ', ' from ', ' this ', ' have ', ' had ',
             ' they ', ' their ', ' there ', ' when ', ' what ', ' who ', ' how ',
             ' not ', ' but ', ' are ', ' his ', ' her ', ' its ', ' our ', ' you ']
# Work on lowercased copy but keep positions
low = text.lower()
hits = {}
for w in eng_words:
    c = low.count(w)
    if c:
        hits[w.strip()] = c
print("\n=== ENGLISH FUNCTION-WORD SCAN (advisory) ===")
if hits:
    for w, c in sorted(hits.items(), key=lambda x: -x[1]):
        print(f"  '{w}': {c}")
else:
    print("  No common English function words found.")

# Show context for a few to judge if they are proper nouns
def show_context(word, n=3):
    pat = re.compile(r'.{0,40}' + re.escape(word) + r'.{0,40}', re.IGNORECASE)
    for i, m in enumerate(pat.finditer(text)):
        if i >= n: break
        print("    ..." + m.group(0).replace('\n',' ') + "...")

print("\n=== SAMPLE CONTEXTS (first 8 English hits) ===")
shown = 0
for w in hits:
    if shown >= 8: break
    print(f"[{w}]")
    show_context(w, 2)
    shown += 1