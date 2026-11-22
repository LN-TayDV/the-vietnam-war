with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\.kilo\skills\translation-workflow\SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the exact 99_scripts section and replace it
start = content.find('99_scripts/')
end = content.find('```', start)

# New content
new_scripts_section = """99_scripts/
    chapter_workflow.py       # **Workflow chính** cho mọi chương (extract→build→audit→compare→quality)
    build_chapter_docx.py     # Script chuẩn xuất DOCX (bố cục sách + footnote chân trang)
    extract_images.py         # **BẮT BUỘC**: trích xuất ảnh raster + rasterize vector map từ PDF theo chapter
    audit_docx_format.py      # Validator định dạng DOCX (heading/body/quote/footnote/image)
    build_volume_docx.py      # Legacy volume DOCX builder (backward compat)
    build_lexicon.py          # Lexicon management: build, update, verify, stats
    extract_chapters.py       # One-time PDF → text extraction (pymupdf)
    test_regression.py        # Regression test ch01-06 (metadata/image/footnote)
    verify_final.py           # Báo cáo kiểm tra từng chương ch01-06"""

content = content[:start] + new_scripts_section + content[end:]

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\.kilo\skills\translation-workflow\SKILL.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Done")