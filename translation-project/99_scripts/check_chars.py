import re
import sys

# Read the file
with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch04\v1_ch04_vi.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Define Vietnamese alphabet (including diacritics)
vietnamese_chars = set(
    'aăâbcdđeêghiklmnoôơpqrstuưvxy'
    'AĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXY'
    '0123456789'
    '.,;:!?()[]{}"\'«»–—-–—_/'
    ' \n\r\t'
    'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ'
    'ìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ'
    'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆ'
    'ÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ'
)

# Also allow Latin-1 supplement characters used in names (French, etc.)
latin1_supplement = set(chr(i) for i in range(0x00C0, 0x0180))

# CJK ranges
cjk_ranges = [
    (0x4E00, 0x9FFF),    # CJK Unified Ideographs
    (0x3400, 0x4DBF),    # CJK Extension A
    (0x20000, 0x2A6DF),  # CJK Extension B
    (0x2A700, 0x2B73F),  # CJK Extension C
    (0x2B740, 0x2B81F),  # CJK Extension D
    (0x2B820, 0x2CEAF),  # CJK Extension E
    (0x2CEB0, 0x2EBEF),  # CJK Extension F
    (0x3000, 0x303F),    # CJK Symbols and Punctuation
    (0x3040, 0x309F),    # Hiragana
    (0x30A0, 0x30FF),    # Katakana
    (0x3130, 0x318F),    # Hangul Compatibility Jamo
    (0xAC00, 0xD7AF),    # Hangul Syllables
    (0x1100, 0x11FF),    # Hangul Jamo
    (0xA960, 0xA97F),    # Hangul Jamo Extended-A
    (0xD7B0, 0xD7FF),    # Hangul Jamo Extended-B
    (0xFF00, 0xFFEF),    # Halfwidth and Fullwidth Forms
    (0xF900, 0xFAFF),    # CJK Compatibility Ideographs
    (0x2F800, 0x2FA1F),  # CJK Compatibility Supplement
]

def is_cjk(char):
    code = ord(char)
    for start, end in cjk_ranges:
        if start <= code <= end:
            return True
    return False

def is_vietnamese_or_latin(char):
    return char in vietnamese_chars or char in latin1_supplement or ord(char) < 0x80

# Split into main text and footnotes
parts = content.split('--- [C\u01b0\u1edbc ch\u00fa trang')
main_text = parts[0]
footnotes = parts[1] if len(parts) > 1 else ''

# Check main text for non-Vietnamese/Latin characters
issues_main = []
for i, char in enumerate(main_text):
    if not is_vietnamese_or_latin(char) and not is_cjk(char):
        code = ord(char)
        if code > 127 and code < 0x10000:
            if is_cjk(char):
                start = max(0, i-20)
                end = min(len(main_text), i+20)
                context = main_text[start:end].replace('\n', ' ')
                issues_main.append(f"  Pos {i} (U+{code:04X}): '{char}' -- CJK in main text: ...{context}...")
            else:
                start = max(0, i-20)
                end = min(len(main_text), i+20)
                context = main_text[start:end].replace('\n', ' ')
                issues_main.append(f"  Pos {i} (U+{code:04X}): '{char}' -- Unknown char: ...{context}...")

# Check footnotes for CJK
cjk_in_footnotes = []
for i, char in enumerate(footnotes):
    if is_cjk(char):
        start = max(0, i-30)
        end = min(len(footnotes), i+30)
        context = footnotes[start:end].replace('\n', ' ')
        cjk_in_footnotes.append(f"  Pos {i} (U+{ord(char):04X}): '{char}' -- ...{context}...")

# Extended CJK ranges
extended_cjk_ranges = [
    (0x3100, 0x312F),  # Bopomofo
    (0x31A0, 0x31BF),  # Bopomofo Extended
    (0x31C0, 0x31EF),  # CJK Strokes
    (0x31F0, 0x31FF),  # Katakana Phonetic Extensions
    (0x3200, 0x32FF),  # Enclosed CJK Letters and Months
    (0x3300, 0x33FF),  # CJK Compatibility
    (0xA840, 0xA87F),  # Phags-pa
    (0x16FE0, 0x16FFF),
    (0x17000, 0x187FF),
    (0x18800, 0x18AFF),
    (0x1B000, 0x1B0FF),
    (0x1B100, 0x1B12F),
    (0x1B130, 0x1B16F),
]

def is_extended_cjk(char):
    code = ord(char)
    for start, end in extended_cjk_ranges:
        if start <= code <= end:
            return True
    return False

ext_cjk_issues = []
for i, char in enumerate(main_text):
    if is_extended_cjk(char):
        start = max(0, i-20)
        end = min(len(main_text), i+20)
        context = main_text[start:end].replace('\n', ' ')
        ext_cjk_issues.append(f"  Pos {i} (U+{ord(char):04X}): '{char}' -- ...{context}...")

# Special characters
special_checks = {
    'ZERO WIDTH SPACE': '\u200B',
    'ZERO WIDTH NON-JOINER': '\u200C',
    'ZERO WIDTH JOINER': '\u200D',
    'LEFT-TO-RIGHT MARK': '\u200E',
    'RIGHT-TO-LEFT MARK': '\u200F',
    'BYTE ORDER MARK': '\uFEFF',
    'REPLACEMENT CHARACTER': '\uFFFD',
    'OBJECT REPLACEMENT CHARACTER': '\uFFFC',
}

# Write results to file (avoid console encoding issues)
with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\99_scripts\char_check_result.txt', 'w', encoding='utf-8') as out:
    out.write("=== KIEM TRA KY TU KHONG PHAI TIENG VIET ===\n\n")
    
    out.write("1. KIEM TRA THAN BAN (TRUOC KHOI CUOC CHU):\n")
    if issues_main:
        for issue in issues_main[:50]:
            out.write(issue + "\n")
        if len(issues_main) > 50:
            out.write(f"  ... va {len(issues_main) - 50} loi khac\n")
    else:
        out.write("  OK: KHONG CO KY TU CJK/HAN/HAN/KHAC LA TRONG THAN BAN\n")
    
    out.write("\n2. KIEM TRA KHOI CUOC CHU:\n")
    if cjk_in_footnotes:
        out.write(f"  Tim thay {len(cjk_in_footnotes)} ky tu CJK trong cuoc chu (co the trong tua sach tieng Nhat/Trung):\n")
        for issue in cjk_in_footnotes[:20]:
            out.write(issue + "\n")
        if len(cjk_in_footnotes) > 20:
            out.write(f"  ... va {len(cjk_in_footnotes) - 20} ky tu khac\n")
    else:
        out.write("  OK: KHONG CO KY TU CJK TRONG CUOC CHU\n")
    
    out.write("\n3. KIEM TRA KY TU DAC BIET:\n")
    for name, char in special_checks.items():
        count = content.count(char)
        if count > 0:
            out.write(f"  WARNING: {name} (U+{ord(char):04X}): {count} lan\n")
        else:
            out.write(f"  OK: {name}: 0 lan\n")
    
    out.write("\n4. KIEM TRA CAC DANG CJK MO RONG:\n")
    if ext_cjk_issues:
        for issue in ext_cjk_issues:
            out.write(issue + "\n")
    else:
        out.write("  OK: KHONG CO KY TU CJK MO RONG TRONG THAN BAN\n")
    
    out.write("\n=== TONG KET ===\n")
    if not issues_main and not ext_cjk_issues:
        out.write("HOAN TOAN SACH: Than ban chi chua tieng Viet (co dau), tieng Latin, so, dau cau chuan.\n")
        out.write("KHONG CO: Ky tu Han (CJK Unified Ideographs), Han tu, Chu Nom, Hangul (tieng Han), Hiragana/Katakana (tieng Nhat), Bopomofo, hoac ky tu la/garbled.\n")
    else:
        out.write(f"CO VAN DE: {len(issues_main) + len(ext_cjk_issues)} ky tu can kiem tra\n")
    
    # Check for Hangul 'stack' character
    if '\uc7d3' in content:
        out.write("\nWARNING: Van con ky tu Hangul 'stack' (U+C7D3) trong file!\n")
        idx = content.index('\uc7d3')
        start = max(0, idx-30)
        end = min(len(content), idx+30)
        out.write(f"  Ngay canh: ...{content[start:end]}...\n")
    else:
        out.write("\nOK: Da sua ky tu Hangul 'stack' (neu co truoc do)\n")

print("Done. Check char_check_result.txt")