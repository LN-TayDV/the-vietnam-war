# -*- coding: utf-8 -*-
"""
Fix ch08 Vietnamese source: convert inline digits to superscript, add footnote definitions.
"""
import re

SUP_MAP = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}

def to_sup(num_str):
    return ''.join(SUP_MAP[d] for d in num_str)

# Read Vietnamese source
vi_path = "/workspaces/the-vietnam-war/translation-project-arendt/04_translation/v2/ch08/v1_ch08_vi.txt"
vi_text = open(vi_path, encoding="utf-8").read()

vi_body = vi_text.split("=== FOOTNOTES ===")[0]

# Find all real footnote markers in body (digits at sentence boundaries)
# Pattern: after . ! ? " followed by space and digit(s) then space/punctuation
# We'll convert these to superscript

# First, let's identify the marker positions more carefully
# The markers appear as: "text. 3 " or 'text." 3 ' or "text. 12 "

# Strategy: Replace digit markers at sentence boundaries with superscript
# But we need to be careful not to replace page numbers, years, etc.

# Pattern for footnote markers: preceded by sentence end punctuation, followed by space
# and not part of a citation like "[18]71" or "1936"
# Use capturing group approach instead of lookbehind
fn_pattern = re.compile(r'([.!?]["\']?\s)(\d{1,2})(?=\s)')

# Also: after quote at end of sentence: '" 3 '
fn_pattern2 = re.compile(r'("\s)(\d{1,2})(?=\s)')

# Also: after quote mid-sentence: '." 3 '
fn_pattern3 = re.compile(r'([.!?]"\s)(\d{1,2})(?=\s)')

# Apply replacements
def replace_fn_markers(text):
    # Replace in order of specificity - keep the punctuation, replace the digit
    text = fn_pattern3.sub(lambda m: m.group(1) + to_sup(m.group(2)), text)
    text = fn_pattern2.sub(lambda m: m.group(1) + to_sup(m.group(2)), text)
    text = fn_pattern.sub(lambda m: m.group(1) + to_sup(m.group(2)), text)
    return text

new_body = replace_fn_markers(vi_body)

# Verify changes
sup = "⁰¹²³⁴⁵⁶⁷⁸⁹"
old_sup = set(re.findall(r'[' + sup + ']+', vi_body))
new_sup = set(re.findall(r'[' + sup + ']+', new_body))
print(f"Old superscript in body: {old_sup}")
print(f"New superscript in body: {new_sup}")

# Count markers
fn_pattern_count = re.compile(r'([.!?]["\']?\s)(\d{1,2})(?=\s)')
old_digits = len(fn_pattern_count.findall(vi_body))
new_markers = len(re.findall(r'[' + sup + ']+', new_body))
print(f"Old digit markers at sentence boundaries: {old_digits}")
print(f"New superscript markers: {new_markers}")

# Show sample changes
print("\n--- Sample changes ---")
for i, (old, new) in enumerate(zip(vi_body.split('\n\n'), new_body.split('\n\n'))):
    if old != new:
        print(f"Para {i}:")
        print(f"  OLD: {old[-150:]}")
        print(f"  NEW: {new[-150:]}")
        if i > 5:
            break

# Write back (keep empty footnotes section for now)
new_text = new_body + "\n\n=== FOOTNOTES ===\n\n"
# TODO: Add footnote definitions from English source

# Save to test file
test_path = "/workspaces/the-vietnam-war/translation-project-arendt/04_translation/v2/ch08/v1_ch08_vi_fixed.txt"
with open(test_path, "w", encoding="utf-8") as f:
    f.write(new_text)
print(f"\nSaved to {test_path}")

PYEOF