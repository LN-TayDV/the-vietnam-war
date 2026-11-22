import re

with open(r'.kilo\skills\translation-workflow\SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the 99_scripts section in Cấu trúc thư mục
old_scripts = """## 99_scripts/
    extract_chapters.py
    extract_images.py          # **BẮT BUỘC**: trích xuất ảnh raster từ PDF theo chapter
    build_chapter_docx.py      # Script chuẩn xuất DOCX (bố cục sách + footnote chân trang)
    apply_vnch_fixes.py        # Áp dụng quy tắc VNCH (30 quy tắc)
    ch01_realign.py            # Căn lại đoạn chương 1
    ch05_realign.py            # Căn lại đoạn chương 5
    build_docx_final.py        # Script build DOCX cuối cùng
    debug_align.py             # Kiểm tra alignment src vs vi
    check_encoding.py          # Kiểm tra encoding UTF-8/NFC/no BOM/LF"""

new_scripts = """## 99_scripts/
    chapter_workflow.py       # **Workflow chính** cho mọi chương (extract→build→audit→compare→quality)
    build_chapter_docx.py     # Script chuẩn xuất DOCX (bố cục sách + footnote chân trang)
    extract_images.py         # **BẮT BUỘC**: trích xuất ảnh raster + rasterize vector map từ PDF theo chapter
    audit_docx_format.py      # Validator định dạng DOCX (heading/body/quote/footnote/image)
    build_volume_docx.py      # Legacy volume DOCX builder (backward compat)
    build_lexicon.py          # Lexicon management: build, update, verify, stats
    extract_chapters.py       # One-time PDF → text extraction (pymupdf)
    test_regression.py        # Regression test ch01-06 (metadata/image/footnote)
    verify_final.py           # Báo cáo kiểm tra từng chương ch01-06"""

content = content.replace(old_scripts, new_scripts)

with open(r'.kilo\skills\translation-workflow\SKILL.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Done")