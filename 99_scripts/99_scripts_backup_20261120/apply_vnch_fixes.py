import re

# VNCH Terminology Fixes
VNCH_FIXES = [
    # CRITICAL: Political terminology
    (r'\bchính trị\b', 'chánh trị'),
    (r'\bChính trị\b', 'Chánh trị'),
    (r'\bCHÍNH TRỊ\b', 'CHÁNH TRỊ'),
    (r'\bchính phủ\b', 'chánh phủ'),
    (r'\bChính phủ\b', 'Chánh phủ'),
    (r'\bCHÍNH PHỦ\b', 'CHÁNH PHỦ'),
    (r'\bchính đảng\b', 'chánh đảng'),
    (r'\bChính đảng\b', 'Chánh đảng'),
    (r'\bđảo chính\b', 'đảo chánh'),
    (r'\bĐảo chính\b', 'Đảo chánh'),
    
    # CRITICAL: Demonstrative pronouns
    (r'\bnày\b(?!(?:\s+(?:trong|ngoài|trước|sau|này|kia|đó|ấy|đây|nấy)))', 'nầy'),
    (r'\bNày\b(?!(?:\s+(?:trong|ngoài|trước|sau|này|kia|đó|ấy|đây|nấy)))', 'Nầy'),
    
    # CRITICAL: Finance terminology
    (r'\btài chính\b', 'tài chánh'),
    (r'\bTài chính\b', 'Tài chánh'),
    (r'\bTÀI CHÍNH\b', 'TÁI CHÁNH'),
    (r'\blương hưu\b', 'hưu bổng'),
    (r'\bLương hưu\b', 'Hưu bổng'),
    (r'\bbất động sản\b', 'địa ốc'),
    (r'\bBất động sản\b', 'Địa ốc'),
    
    # MAJOR: Conjunctions
    (r'\bmặc dù\b', 'dầu'),
    (r'\bMặc dù\b', 'Dầu'),
    (r'\btuy nhiên\b', 'tuy vậy'),
    (r'\bTuy nhiên\b', 'Tuy vậy'),
    (r'\bvì vậy\b', 'bởi thế'),
    (r'\bVì vậy\b', 'Bởi thế'),
    (r'\bhơn nữa\b', 'vả'),
    (r'\bHơn nữa\b', 'Vả'),
    (r'\bmà\b(?=\s+(?:không|chẳng|đâu))', 'chớ'),
    (r'\bMà\b(?=\s+(?:không|chẳng|đâu))', 'Chớ'),
    
    # MAJOR: Colonial names (keep original in parentheses per Style Guide Rule 15)
    (r'\bAnnam\b(?!\s*\([^)]*\))', 'Trung Kỳ (Annam)'),
    (r'\bTonkin\b(?!\s*\([^)]*\))', 'Bắc Kỳ (Tonkin)'),
    (r'\bCochinchina\b(?!\s*\([^)]*\))', 'Nam Kỳ (Cochinchina)'),
    (r'\bCochinchine\b(?!\s*\([^)]*\))', 'Nam Kỳ (Cochinchine)'),
    (r'\bIndochine\b(?!\s*\([^)]*\))', 'Đông Dương (Indochine)'),
    
    # MAJOR: Liberation terminology
    (r'\bgiải phóng\b', 'độc lập'),
    (r'\bGiải phóng\b', 'Độc lập'),
    (r'\bGIẢI PHÓNG\b', 'ĐỘC LẬP'),
    
    # MAJOR: Comrade terminology
    (r'\bđồng chí\b', 'đồng đạo'),
    (r'\bĐồng chí\b', 'Đồng đạo'),
    (r'\bĐỒNG CHÍ\b', 'ĐỒNG ĐẠO'),
    
    # MINOR: Representative terminology
    (r'\bđại biểu\b(?!\s+Quốc hội)', 'dân biểu'),
    (r'\bĐại biểu\b(?!\s+Quốc hội)', 'Dân biểu'),
    
    # MINOR: Nation terminology
    (r'\bquốc gia\b(?!\s+VNCH)', 'quốc gia/dân tộc'),
    (r'\bQuốc gia\b(?!\s+VNCH)', 'Quốc gia/Dân tộc'),
]

def apply_vnch_fixes(text):
    """Apply VNCH terminology fixes to text."""
    for pattern, replacement in VNCH_FIXES:
        text = re.sub(pattern, replacement, text)
    return text

def fix_paragraph_formatting(text):
    """Fix duplicate markers and formatting issues."""
    # Remove duplicate page markers in content
    text = re.sub(r'\(trang \d+\)\s*---\s*(?=\n)', '', text)
    text = re.sub(r'\(trang \d+-\d+\)\s*---\s*(?=\n)', '', text)
    text = re.sub(r'— đề mục\s*---\s*(?=\n)', '', text)
    # Fix heading markers that got into content
    text = re.sub(r'^\(trang \?\?\?\)\s*---\s*', '', text, flags=re.MULTILINE)
    # Remove footnote blocks that leaked into body
    text = re.sub(r'--- \[Cước chú.*?---', '', text, flags=re.DOTALL)
    # Clean up multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

# Process all chapter translation files
chapters = ['ch01', 'ch02', 'ch03', 'ch04', 'ch05', 'ch06']

for ch in chapters:
    # Determine the correct translation file
    if ch == 'ch01':
        # Use the complete fixed version
        vi_file = f'translation-project/04_translation/v1/{ch}/v1_{ch}_vi_complete.txt'
    else:
        vi_file = f'translation-project/04_translation/v1/{ch}/v1_{ch}_vi.txt'
    
    try:
        with open(vi_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        content = fix_paragraph_formatting(content)
        content = apply_vnch_fixes(content)
        
        # Save fixed version
        out_file = f'translation-project/04_translation/v1/{ch}/v1_{ch}_vi_FINAL.txt'
        with open(out_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        
        print(f'{ch}: Fixed and saved to {out_file}')
    except FileNotFoundError:
        print(f'{ch}: File not found - {vi_file}')
    except Exception as e:
        print(f'{ch}: Error - {e}')

print('\nVNCH terminology fixes applied to all chapters.')