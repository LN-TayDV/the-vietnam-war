"""
Consolidate Chapter 4 translation parts (_p1.._p5) into v1_ch04_vi.txt.

Correctly handles:
- _p1 (134-140), _p2 (141-146), _p3 (147-149): use as-is
- _p4: re-segment into source pages 150-156 with correct page labels AND footnote distribution
- _p5 (157-167): use as-is

_p4 footnote redistribution (by superscript number prefix):
  _p4 PAGE 151 footnotes 59-63 -> split: 59-60 to page 151, 61-63 to page 152
  _p4 PAGE 153 footnotes 70-73 -> split: 70-71 to page 154, 72-73 to page 155
  _p4 PAGE 154 footnotes 74-77 -> split: 74 to page 155, 75-77 to page 156
"""
import re
import os

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v1\ch04"

def read_part(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return f.read()

p1 = read_part("_p1.txt")
p2 = read_part("_p2.txt")
p3 = read_part("_p3.txt")
p4 = read_part("_p4.txt")
p5 = read_part("_p5.txt")

# --- Split text into page blocks ---
def split_pages(text):
    pattern = re.compile(r'^=== PAGE (\d+) ===\s*$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    blocks = {}
    for i, m in enumerate(matches):
        page_num = int(m.group(1))
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = text[start:end].strip()
        blocks[page_num] = body
    return blocks

p4_blocks = split_pages(p4)

# --- Separate body from footnotes in a block ---
# Footnotes start with superscript digits: ⁰¹²³⁴⁵⁶⁷⁸⁹
SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹'
fn_line_re = re.compile(r'^[⁰¹²³⁴⁵⁶⁷⁸⁹]')

def split_body_footnotes(block):
    """Return (body_text, footnotes_dict) where footnotes_dict maps number->text."""
    lines = block.split('\n')
    body_lines = []
    footnotes = {}
    in_footnotes = False
    for line in lines:
        if fn_line_re.match(line):
            in_footnotes = True
            # Extract footnote number from superscript prefix
            sup = ''
            rest = line
            for ch in line:
                if ch in SUP:
                    sup += ch
                else:
                    rest = line[len(sup):]
                    break
            # Convert superscript to int
            sup_map = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
            num = int(''.join(sup_map[c] for c in sup))
            footnotes[num] = rest.strip()
        else:
            if not in_footnotes:
                body_lines.append(line)
            # Skip footnote continuation lines (already captured)
    body = '\n'.join(body_lines).strip()
    return body, footnotes

# Extract body + footnotes for each _p4 block
b150_body, fn150 = split_body_footnotes(p4_blocks[150])
b151_body, fn151 = split_body_footnotes(p4_blocks[151])
b152_body, fn152 = split_body_footnotes(p4_blocks[152])
b153_body, fn153 = split_body_footnotes(p4_blocks[153])
b154_body, fn154 = split_body_footnotes(p4_blocks[154])

# --- Split body texts at source page boundaries ---
# PAGE 151 -> 151 + 152
split_151 = "phải theo dõi tiếng nói ấy một cách xảo quyệt."
idx = b151_body.find(split_151)
assert idx != -1, "split_151 not found"
end = idx + len(split_151)
body_151 = b151_body[:end].strip()
body_152 = b151_body[end:].strip()

# PAGE 153 -> 154 + 155
split_153 = "làm tròn bổn phận hằng ngày."
idx = b153_body.find(split_153)
assert idx != -1, "split_153 not found"
end = idx + len(split_153)
body_154 = b153_body[:end].strip()
body_155 = b153_body[end:].strip()

# PAGE 154 -> 155(rest) + 156
split_154 = "Dấu vết dẫn thẳng từ"
idx = b154_body.find(split_154)
assert idx != -1, "split_154 not found"
end = idx + len(split_154)
body_155_rest = b154_body[:end].strip()
body_156 = b154_body[end:].strip()

# Combine 155
body_155_full = body_155 + " " + body_155_rest

# Fix text marker: Brogan footnote is marked ⁷⁰ in _p4 but should be ⁶⁹
# (source: "sleepless night on their account.69")
body_154 = body_154.replace("mất một giấc ngủ vì họ.⁷⁰", "mất một giấc ngủ vì họ.⁶⁹")

# --- Redistribute footnotes ---
# fn151 has 59-63: 59-60 -> page 151, 61-63 -> page 152
fn_151 = {k:v for k,v in fn151.items() if k <= 60}
fn_152 = {k:v for k,v in fn151.items() if k >= 61}

# fn153 has 70-73 (but _p4 numbering is off by 2 for 70,71):
#   _p4 70 (Scheurer-Kestner) -> source 68
#   _p4 71 (Brogan)           -> source 69
#   _p4 72 (Barrès)           -> source 72 (correct)
#   _p4 73 (Yves Simon)       -> source 73 (correct)
# Renumber 70->68, 71->69; add missing 70 (Picquart/Tunis) and 71 (Peguy group)
fn_154 = {}
if 70 in fn153:
    fn_154[68] = fn153[70]  # Scheurer-Kestner
if 71 in fn153:
    fn_154[69] = fn153[71]  # Brogan
fn_155a = {}
if 72 in fn153:
    fn_155a[72] = fn153[72]  # Barrès
if 73 in fn153:
    fn_155a[73] = fn153[73]  # Yves Simon

# fn154 has 74-77: 74 -> page 155, 75-77 -> page 156
fn_155b = {}
if 74 in fn154:
    fn_155b[74] = fn154[74]  # Rennes University
fn_156 = {k:v for k,v in fn154.items() if k >= 75}

# Add missing footnotes from source:
# Source p.154 fn 70 (Picquart/Tunis)
fn_154[70] = ("Ngay sau khi đã có những phát hiện của mình, Picquart bị đày đến "
    "một chức vụ nguy hiểm tại Tunisia. Sau đó ông đã làm di chúc, phơi bày "
    "toàn bộ câu chuyện, và gửi một bản sao tài liệu cho luật sư của mình. "
    "Vài tháng sau, khi người ta phát hiện ra rằng ông vẫn còn sống, một "
    "trận mưa thư tín bí ẩn đã trút xuống, liên lụy đến ông và buộc tội ông "
    "đồng lõa với 'kẻ phản bội' Dreyfus. Ông bị đối xử như một tên côn đồ "
    "đã dọa 'méc lẻo.' Khi tất cả những điều nầy đều không hiệu quả, ông bị "
    "bắt giữ, bị đuổi khỏi quân đội, và bị tước hết huân chương, tất cả "
    "những điều nầy ông đều chịu đựng với sự điềm tĩnh.")
# Source p.155 fn 71 (Peguy group)
fn_155a[71] = ("Nhóm nầy, do Charles Péguy cầm đầu, bao gồm những người trẻ "
    "Romain Rolland, Suarez, Georges Sorel, Daniel Halévy, và Bernard Lazare.")

# Combine page 155 footnotes
fn_155 = {**fn_155a, **fn_155b}

# --- Format page blocks ---
def format_footnotes(fn_dict):
    if not fn_dict:
        return ''
    lines = []
    for num in sorted(fn_dict.keys()):
        lines.append(f'{num}. {fn_dict[num]}')
    return '\n'.join(lines)

def page_block(label, book_page, body, footnotes):
    fn_text = format_footnotes(footnotes)
    parts = [f'=== PAGE {label} ===', str(book_page), body]
    if fn_text:
        parts.append(fn_text)
    return '\n'.join(parts)

p4_reassembled = '\n\n'.join([
    page_block(150, 105, b150_body, fn150),
    page_block(151, 106, body_151, fn_151),
    page_block(152, 107, body_152, fn_152),
    page_block(153, 108, b152_body, fn152),
    page_block(154, 109, body_154, fn_154),
    page_block(155, 110, body_155_full, fn_155),
    page_block(156, 111, body_156, fn_156),
])

# --- Build consolidated file ---
def ensure_trailing(s):
    return s.rstrip() + '\n'

consolidated = '\n\n'.join([
    ensure_trailing(p1),
    ensure_trailing(p2),
    ensure_trailing(p3),
    p4_reassembled.rstrip() + '\n',
    ensure_trailing(p5),
])

out_path = os.path.join(BASE, 'v1_ch04_vi.txt')
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(consolidated)

# --- Report ---
pages_found = re.findall(r'=== PAGE (\d+) ===', consolidated)
print(f'Written: {out_path}')
print(f'Total pages: {len(pages_found)}')
print(f'Page range: {pages_found[0]}..{pages_found[-1]}')
from collections import Counter
dupes = {k: v for k, v in Counter(pages_found).items() if v > 1}
if dupes:
    print(f'DUPLICATE PAGES: {dupes}')
else:
    print('No duplicate pages.')
expected = [str(i) for i in range(134, 168)]
missing = [p for p in expected if p not in pages_found]
if missing:
    print(f'MISSING PAGES: {missing}')
else:
    print('All pages 134-167 present.')

# Report footnote distribution for pages 150-156
print('\nFootnote distribution (pages 150-156):')
for pg in [150,151,152,153,154,155,156]:
    m = re.search(rf'=== PAGE {pg} ===.*?(?==== PAGE|\Z)', consolidated, re.DOTALL)
    if m:
        block = m.group()
        fns = re.findall(r'^(\d+)\.', block, re.MULTILINE)
        print(f'  PAGE {pg}: footnotes {fns}')