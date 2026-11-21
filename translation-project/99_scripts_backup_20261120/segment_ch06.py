#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segment V1-Ch6 extracted text into paragraphs with [V1C06-Pxxx] (trang X) markers.
Create v1_ch06_src.txt with paragraph structure.
"""

import re

# Read the extracted text
with open(r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\02_extracted_text\v1\ch06.txt", "r", encoding="utf-8") as f:
    text = f.read()

# The text has page numbers embedded (127, 128, 129, etc.) and footnotes
# We need to split into paragraphs and track page numbers

# First, let's clean up and identify page markers
# Page numbers appear as standalone lines like "127", "128", etc.
# Also "David G. Marr 128" etc. indicates page continuation

lines = text.split('\n')

# Process to identify paragraphs and pages
paragraphs = []
current_page = 127
current_para = ""
para_num = 0

# Footnote pattern: starts with number + tab or space, or [N]
footnote_pattern = re.compile(r'^(\d+)\s+')

# We'll do a simpler approach: split by double newlines and identify page numbers
# But the extracted text is messy. Let me use a more careful approach.

# Join and split by paragraph breaks (double newline or clear breaks)
# The text has page numbers on separate lines

# Strategy: iterate through lines, build paragraphs, detect page numbers
# Page numbers are lines that are just digits (127, 128, 129...)
# "David G. Marr 128" means page 128 header

in_footnotes = False
footnotes = []

for line in lines:
    line_stripped = line.strip()
    
    # Detect page number lines
    if re.match(r'^\d{3}$', line_stripped):  # 127, 128, etc.
        current_page = int(line_stripped)
        continue
    elif re.match(r'^David G\. Marr\s+\d{3}$', line_stripped):
        # "David G. Marr 128" - page header
        match = re.search(r'(\d{3})$', line_stripped)
        if match:
            current_page = int(match.group(1))
        continue
    elif line_stripped == "The Birth of the Democratic Republic of\u00a0Vietnam":
        # Chapter title - start of content
        continue
    elif line_stripped == "David G. Marr":
        # Author name
        continue
    elif line_stripped.startswith("Figure 6.1"):
        # Figure caption - part of paragraph
        if current_para:
            current_para += " " + line_stripped
        else:
            current_para = line_stripped
        continue
    elif line_stripped.startswith("Source: "):
        # Figure source - part of paragraph
        if current_para:
            current_para += " " + line_stripped
        else:
            current_para = line_stripped
        continue
    
    # Check for footnote markers in the text body (like "1 " at start of footnote content)
    # The footnotes in the extracted text appear after the main content
    # They start with number + tab/space and are at the end
    
    # Empty line = paragraph break
    if not line_stripped:
        if current_para:
            para_num += 1
            paragraphs.append({
                'num': para_num,
                'page': current_page,
                'text': current_para.strip()
            })
            current_para = ""
        continue
    
    # Add line to current paragraph
    if current_para:
        current_para += " " + line_stripped
    else:
        current_para = line_stripped

# Don't forget last paragraph
if current_para:
    para_num += 1
    paragraphs.append({
        'num': para_num,
        'page': current_page,
        'text': current_para.strip()
    })

# Now extract footnotes from the text
# Footnotes are at the end, starting with numbers
# Let's find them in the original text
footnote_text = ""
in_fn = False
for line in lines:
    if re.match(r'^\d+\s+', line.strip()) and len(line.strip()) > 5:
        # Likely a footnote
        in_fn = True
    if in_fn:
        footnote_text += line + "\n"

# Print summary
print(f"Found {len(paragraphs)} paragraphs")
print(f"Pages covered: {min(p['page'] for p in paragraphs)} - {max(p['page'] for p in paragraphs)}")

# Write source file
output = []
output.append("===== V1-C06 · The Birth of the Democratic Republic of Vietnam · David G. Marr =====")
output.append("Nguon goc tieng Anh tu PDF (trich xuat).")
output.append("")

for p in paragraphs:
    marker = f"--- [V1C06-P{p['num']:03d}] (trang {p['page']}) ---"
    output.append(marker)
    output.append(p['text'])
    output.append("")

# Add footnotes section
output.append("--- [Cước chú trang 127-153] ---")
output.append(footnote_text.strip())

with open(r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch06\v1_ch06_src.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(output))

print("Source file written.")