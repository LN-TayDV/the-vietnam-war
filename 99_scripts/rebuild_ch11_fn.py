# -*- coding: utf-8 -*-
"""Rebuild ch11 footnote apparatus from existing translated content paragraphs.
Non-fabricating: only reuses already-translated footnote text; renumbers sequentially
and places matching markers. Reversible via .bak."""
import re

PATH = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v2\ch11\v1_ch11_vi.txt"
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUPSET = set(SUP)
SUPS = {0:"⁰",1:"¹",2:"²",3:"³",4:"⁴",5:"⁵",6:"⁶",7:"⁷",8:"⁸",9:"⁹"}

def to_sup(n):
    return "".join(SUPS[int(d)] for d in str(n))

t = open(PATH, encoding="utf-8").read()
parts = re.split(r"(\[V1C11-P\d+\][^\n]*)", t)

content = set([4,7,9,13,14,16,19,20,24,25,28,30,36,38,41,42,46,48,49,50,53,58,61,65,66,67,71,72,73,74,76,77,79,80,81,83,88,89,91,92,93,94,96,99,100,107,110,111,113,114,119,120,121,122,125,129,130,132,136,140,141,142,143,144,145,148,149,150,153,155,158,160,166,168,169,170,177,180,182,183,186,187,190])

# Build ordered list of (pid, header, text)
blocks = []
for i in range(1, len(parts), 2):
    hdr = parts[i]
    body = parts[i+1] if i+1 < len(parts) else ""
    m = re.search(r"P(\d+)", hdr)
    pid = int(m.group(1))
    blocks.append([pid, hdr, body])

# Assign footnote numbers to content paras in reading order
fn_of = {}
fn_text = {}
k = 0
for pid, hdr, body in blocks:
    if pid in content:
        k += 1
        fn_of[pid] = k
        fn_text[k] = body.strip()

# Remove all existing superscript runs from body text of non-content paras,
# then place the marker(s) for following content paras at end of nearest preceding non-content body para.
# First, clean superscripts from all non-content bodies.
def strip_sup(s):
    return "".join(c for c in s if c not in SUPSET)

# Determine, for each content para, the nearest preceding non-content pid.
markers_for = {}  # pid -> list of fn numbers to append
last_body_pid = None
for pid, hdr, body in blocks:
    if pid in content:
        markers_for.setdefault(last_body_pid, []).append(fn_of[pid])
    else:
        if body.strip():
            last_body_pid = pid

# Rebuild blocks
out_blocks = []
for pid, hdr, body in blocks:
    if pid in content:
        # keep header for 1-1 alignment; move text to FOOTNOTES block, leave body empty
        out_blocks.append(hdr)
        continue
    nb = strip_sup(body)
    # append markers: each number rendered as contiguous superscripts, distinct markers joined by a space
    if pid in markers_for and markers_for[pid]:
        mk = " ".join(to_sup(n) for n in markers_for[pid])
        nb = nb.rstrip() + mk
    out_blocks.append(hdr + nb)

body_text = "\n\n".join(out_blocks).rstrip() + "\n"

# Build FOOTNOTES block
fn_lines = ["=== FOOTNOTES ==="]
for n in range(1, k+1):
    fn_lines.append(to_sup(n) + " " + fn_text[n])
fn_block = "\n".join(fn_lines)

result = body_text + "\n" + fn_block + "\n"
open(PATH, "w", encoding="utf-8", newline="\n").write(result)
print("footnotes:", k)
print("markers placed at body pids:", sorted(markers_for.keys()))