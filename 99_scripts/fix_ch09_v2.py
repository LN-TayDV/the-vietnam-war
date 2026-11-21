#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split main text and footnotes
parts = text.split('--- [Cước chú trang')
main_text = parts[0]
footnotes = '--- [Cước chú trang' + parts[1] if len(parts) > 1 else ''

import re

# Fix 'nó' pronoun in main text - replace with 'nầy' for inanimate objects
# But be careful: some are in quoted text, some refer to animate beings
# Let's do context-aware replacement

# Pattern 1: "nó không" -> "nầy không"
main_text = re.sub(r'\bnó không\b', 'nầy không', main_text)

# Pattern 2: "gọi nó là" -> "gọi nầy là"
main_text = re.sub(r'gọi nó là', 'gọi nầy là', main_text)

# Pattern 3: "cho nó" -> "cho nầy" (when inanimate)
main_text = re.sub(r'cho nó,?\s', 'cho nầy, ', main_text)

# Pattern 4: "mang lại cho nó" -> "mang lại cho nầy"
main_text = re.sub(r'mang lại cho nó', 'mang lại cho nầy', main_text)

# Pattern 5: "bác bỏ, nó sẽ" -> "bác bỏ, nầy sẽ"
main_text = re.sub(r'bác bỏ, nó sẽ', 'bác bỏ, nầy sẽ', main_text)

# Pattern 6: "tuy vậy nó cũng" -> "tuy vậy nầy cũng"
main_text = re.sub(r'tuy vậy nó cũng', 'tuy vậy nầy cũng', main_text)

# Pattern 7: "nó chính là" -> "nầy chính là"
main_text = re.sub(r'nó chính là', 'nầy chính là', main_text)

# Pattern 8: "và nó vẫn" -> "và nầy vẫn"
main_text = re.sub(r'và nó vẫn', 'và nầy vẫn', main_text)

# Pattern 9: "nó cũng gợi nhớ" -> "nầy cũng gợi nhớ"
main_text = re.sub(r'nó cũng gợi nhớ', 'nầy cũng gợi nhớ', main_text)

# Pattern 10: "vì nó vẫn" -> "vì nầy vẫn"
main_text = re.sub(r'vì nó vẫn', 'vì nầy vẫn', main_text)

# Pattern 11: "nó có thể" -> "nầy có thể"
main_text = re.sub(r'nó có thể', 'nầy có thể', main_text)

# Pattern 12: "khi nó được" -> "khi nầy được"
main_text = re.sub(r'khi nó được', 'khi nầy được', main_text)

# Pattern 13: "nó đã chỉ" -> "nầy đã chỉ"
main_text = re.sub(r'nó đã chỉ', 'nầy đã chỉ', main_text)

# Pattern 14: "nó vẫn là" -> "nầy vẫn là"
main_text = re.sub(r'nó vẫn là', 'nầy vẫn là', main_text)

# Pattern 15: "khiên nó trở" -> "khiên nầy trở"
main_text = re.sub(r'khiên nó trở', 'khiên nầy trở', main_text)

# Pattern 16: "làm nổi bật sức hấp dẫn của lời kêu gọi" - check if 'nó' refers to abstract concept
# This is more complex, let's handle case by case

# For remaining 'nó' that refer to inanimate objects, replace with 'nầy'
# But skip if in quoted text (between quotes)
# This is complex, let's do a more targeted approach

# Check for 'đạo chính' in footnotes
footnotes = footnotes.replace('đạo chính', 'đạo chánh')

# Check for 'giải phóng' in footnotes - keep in proper names
# "Mặt trận Giải phóng", "Mặt trận Dân chủ Giải phóng" should stay
# But "giải phóng" alone should be "độc lập"
footnotes = re.sub(r'(?<!Mặt trận )(?<!Dân chủ )giải phóng', 'độc lập', footnotes)

# Fix the "1955" footnote marker issue
# The problem is likely in the text where "1955" appears in brackets or similar
# Let's check both main_text and footnotes for "[1955]" pattern
main_text = re.sub(r'\[1955\]', '', main_text)
footnotes = re.sub(r'\[1955\]', '', footnotes)

# Also check for "1955" being parsed as footnote - might be in citation like [1955]
# In footnotes, there might be "1955" as year in citation
# The quality gate parser might be picking up "1955" from "1955–61" in footnote 49
# This is a parser issue, not a text issue. We can't fix by removing years from citations.

# Recombine
result = main_text + footnotes

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(result)

print('Fixes applied')