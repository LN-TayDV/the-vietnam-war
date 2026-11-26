# DOCX_PUBLISHING_SPEC.md — QUY CHUẨN DOCX XUẤT BẢN

**Dự án:** The Origins of Totalitarianism — Hannah Arendt (VNCH rebuild)  
**File:** `.kilo/plans/DOCX_PUBLISHING_SPEC.md`  
**Phiên bản:** 1.0

---

## 1. CẤU TRÚC DOCX TỪNG CHƯƠNG

Mỗi chương được build thành một file DOCX riêng tại `09_docx/V2-NN_chNN.docx`.

### 1.1 Heading Hierarchy

| Cấp | Style | Mục đích | Ví dụ |
|-----|-------|----------|-------|
| 1 | Heading 1 / ChapterTitle | Tiêu đề chương | "CHƯƠNG MỘT: ..." |
| 2 | Heading 2 / SectionH1 | Mục chính trong chương | "I. ..." |
| 3 | Heading 3 / SectionH2 | Mục phụ | "A. ..." |
| 4 | Heading 4 / SectionH3 | Mục tiểu phụ (nếu có) | "1. ..." |

**Quy tắc:**
- Mỗi chapter có đúng 1 Heading 1 (tiêu đề chương)
- Không lặp Heading 1 trong cùng một chapter
- Heading phải có `keep_with_next = true` để không bị tách trang

### 1.2 Body Text Styles

| Style | Mục đích | Định dạng |
|-------|----------|-----------|
| Body Text | Đoạn văn thường | Times New Roman 12pt, khoảng cách dòng 1.5, căn lề hai bên, đầu đoạn thụt lề 0.5" |
| Block Quotation | Trích dẫn dài (>4 dòng) | Times New Roman 12pt, thụt lề trái và phải 0.5", khoảng cách dòng 1.5, italic (tùy ngữ cảnh) |
| Footnote | Chú thích chân trang | Times New Roman 9pt, đánh số 1..N, xuất hiện ở cuối trang |

### 1.3 Chapter Structure trong DOCX

```
[Heading 1] Chương X: Tiêu đề chương
[Body Text] Đoạn P001
[Body Text] Đoạn P002
...
[Footnote markers] ¹ ² ³ (liên kết với footnote tại bottom of page)
=== FOOTNOTES === (xuất hiện ở bottom of page, không ở cuối chương)
```

**Quy tắc:**
- Không lặp tiêu đề chương ở đầu nội dung body
- Không để tiêu đề chạy đầu trang (running header) lọt vào body
- Chú thích đúng vị trí, liên kết với footnote marker trong body
- Footnote đánh số 1..N (có thể có gaps nếu số nguyên bản không liên tục)

---

## 2. CẤU TRÚC DOCX TỔNG HỢP (MASTER)

File: `09_docx/V2-Origins-of-Totalitarianism-MASTER.docx`

### 2.1 Thứ tự nội dung

1. Trang bìa (Title Page): Tên tác phẩm, tác giả, nhà xuất bản, năm
2. Mục lục tự động (TOC field): `TOC \o "1-3" \h \z \u`
3. Phần mở đầu (front matter): 6 thành phần
4. Chương 1–13: mỗi chương bắt đầu trên trang mới (section break)
5. Chú thích liên tục xuyên suốt toàn bộ tác phẩm (continuous numbering)

### 2.2 Footnote Strategy (Continuous Numbering)

- Mỗi chapter có local footnote numbers (1..N_local)
- Khi build master, local numbers được remap thành global numbers
- Global numbering không restart giữa các chapter
- Body superscript markers được rewrite thành «globalnum» tokens

### 2.3 Navigation Pane

- Tất cả Heading 1 (chapter titles) xuất hiện trong Navigation Pane
- Heading 2 và Heading 3 cũng xuất hiện nếu được cấu hình
- Người dùng có thể nhảy trực tiếp đến chương bất kỳ qua Navigation Pane

### 2.4 Mục lục tự động

- TOC field được chèn sau trang bìa
- TOC hiển thị Heading 1–3
- Placeholder text: "Nhấn F9 để cập nhật mục lục."

---

## 3. FILE NAMING CONVENTION

| Loại | Pattern | Ví dụ |
|------|---------|-------|
| Từng chương | `V2-NN_chNN.docx` | `V2-01_ch01.docx`, `V2-12_ch12.docx` |
| Phần mở đầu | `V2-{section}.docx` | `V2-Front-Matter.docx`, `V2-Preface-1.docx` |
| Tổng hợp | `V2-Origins-of-Totalitarianism-MASTER.docx` | `V2-Origins-of-Totalitarianism-MASTER.docx` |

---

## 4. BUILD SCRIPTS

| Script | Vị trí | Mục đích |
|--------|--------|----------|
| `build_chapter_docx_v2.py` | `99_scripts/` | Build DOCX từng chương từ file translation |
| `build_master_docx_v2.py` | `99_scripts/` | Build DOCX tổng hợp 13 chương + phần mở đầu |
| `docx_builder_v2/` | `99_scripts/` | Thư viện core: models, parser, styles, layout, renderer |

### 4.1 Style Registry

File: `99_scripts/styles/spec.yaml`

Định nghĩa tất cả Word Styles sử dụng trong DOCX:
- Heading 1, Heading 2, Heading 3, Heading 4
- Body Text, Block Quotation
- Footnote
- TOCHeading

### 4.2 Renderer

File: `99_scripts/docx_builder_v2/renderer.py`

Chuyển đổi DocumentModel thành python-docx Document:
- Áp dụng Style Registry
- Render footnote như Word native footnotes (OOXML)
- Chèn TOC field vào master DOCX

---

## 5. VALIDATION CHECKLIST (TRƯỚC KHI HOAN_TAT)

| # | Kiểm tra | Phương pháp | Pass condition |
|---|----------|-------------|----------------|
| D1 | File mở được trong Word | `python-docx Document()` mở thành công | Không lỗi |
| D2 | Heading 1 tồn tại và duy nhất | Kiểm tra Styles pane trong Word | Đúng 1 Heading 1 per chapter |
| D3 | Footnote Count khớp | Word `Footnotes.Count` = số footnote trong progress.json | OK N/N |
| D4 | TOC field tồn tại | Master DOCX có TOC field | Có TOC field |
| D5 | Navigation Pane hoạt động | Mở DOCX, kiểm tra Navigation Pane | Có danh sách chapter |
| D6 | Không lặp tiêu đề chương | Kiểm tra body text không có tiêu đề chapter lặp | 0 lần lặp |
| D7 | Không header chạy vào body | Kiểm tra body text không bắt đầu bằng running header | 0 header trong body |
| D8 | Encoding file nguồn | UTF-8, NFC, no BOM, LF | Tất cả file nguồn chuẩn |

---

## 6. OUTPUT DIRECTORY

| Thư mục | Mục đích |
|---------|----------|
| `09_docx/` | Tất cả file DOCX output |
| `09_docx/V2-NN_chNN.docx` | DOCX từng chương |
| `09_docx/V2-Origins-of-Totalitarianism-MASTER.docx` | DOCX tổng hợp |
