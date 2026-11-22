# BÁO CÁO KIỂM TRA CUỐI CÙNG — CHƯƠNG 10
*The Cambridge History of the Vietnam War* — Tiếng Việt (tiên chuẩn miền Nam VNCH)

## 1. TỔNG QUAN

| Mục | Chi tiết |
|-----|----------|
| Chương | V1-C10: The French Indochina War in Northern Vietnam |
| Tác giả | Christopher Goscha |
| Trang in | 218–237 |
| Đoạn văn | 33 (P001–P033) |
| Cước chú | 19 ([1]–[19]) |
| Hình ảnh | 2 (Figure 10.1, Map 10.1) |
| Heading blocks | 3 (P003, P016, P032) |
| File bản dịch | `translation-project/04_translation/v1/ch10/v1_ch10_vi.txt` |
| File DOCX | `translation-project/09_docx/V1-C10_The-French-Indochina-War-in-Northern-Vietnam.docx` |
| Ngày hoàn thành | 2026-11-21 |

## 2. NGUYÊN TẮC ĐÃ ÁP DỤNG

Tuân thủ nghiêm ngặt `translation-workflow` skill (SKILL.md) và toàn bộ rules/references:

1. **Style Guide Phan B v2.3** — 29 quy tắc văn phong miền Nam VNCH (chánh phủ, chánh trị, dân biểu, trái lại, vả, tuy vậy, bởi thế, nầy, ...)
2. **Translation Grammar Engine v2.1** — 7 bước dịch, S1–S20, P1–P10, C1–C10 checklists
3. **MASTER_LEXICON.csv** — 77 mục thuật ngữ VNCH
4. **AUDIT_REPORT_CH01-06.md** — bài học từ Ch1–6
5. **VLP-01 (Tiếng Việt trước)** — áp dụng từ câu đầu tiên
6. **Không tạo workflow mới, không sửa skill/rules**

## 3. NỘI DUNG ĐÃ XÁC MINH (VERIFIED)

### 3.1 Encoding và định dạng file
- UTF-8, NFC, không BOM, LF-only (không CRLF): **PASS**
- File không chứa ký tự controllo hoặc artifact encoding: **PASS**

### 3.2 Alignment (đoạn src ↔ đoạn vi)
- 33/33 đoạn có marker `--- [V1C10-Pxxx] (trang Z) ---` khớp 1-1: **PASS**
- Số đoạn src = số đoạn vi = 33: **PASS**
- 3 heading block (P003, P016, P032) có marker `— đề mục —` / `— trích dẫn —`: **PASS**

### 3.3 Cước chú
- 19 cước chú [1]–[19] xuất hiện đầy đủ trong bản dịch (inline + khối chú thích cuối trang): **PASS**
- Nội dung cước chú giữ nguyên trích dẫn gốc (tác giả, năm, trang, URL): **PASS**

### 3.4 Hình ảnh
- 2 hình ảnh nhúng trong DOCX: Figure 10.1 (p223), Map 10.1 (p229): **PASS**
- Mỗi caption được đặt trước bởi hình ảnh (keep_with_next): **PASS**
- Media integrity: DOCX bytes == source PNG: **PASS**

### 3.5 Định dạng DOCX (audit_docx_format.py)
Tất cả kiểm tra định dạng PASSED:
- Heading: 13.5pt bold, sb=14pt, sa=6pt: **PASS (2 heading)**
- Body: 12pt, Justify, fi=0.9cm, sa=6pt, line=1.3: **PASS (30 body paragraphs)**
- Quote: 12pt italic, indent 0.5": **PASS (1 quote block)**
- Footnote: 9pt, sequential 1..19: **PASS**
- Images: 4.5" wide, before caption: **PASS (2 images)**
- Không có block-header leak: **PASS**
- Không có metadata leak (source path, colophon): **PASS**

### 3.6 Thuật ngữ VNCH (Style Guide v2.3 + MASTER_LEXICON.csv)
Tất cả thuật ngữ đã được chuẩn hóa:
| Từ gốc | Bản dịch VNCH |
|--------|--------------|
| chính phủ | chánh phủ |
| chính trị | chánh trị |
| đại biểu | dân biểu |
| ngược lại | trái lại |
| hơn nữa | vả |
| tuy nhiên | tuy vậy |
| vì vậy | bởi thế |
| này | nầy |
| Annam | Trung Kỳ |
| Tonkin | Bắc Kỳ |
| Cochinchina | Nam Kỳ |
| giải phóng | độc lập |
| đồng chí | đồng đạo |
| classifiers (cuốn/cái/con/cây/cục/bài) | đã áp dụng |

### 3.7 Tính chất ngôn ngữ (Language Purity)
- Không còn từ Đức, Anh, Pháp, Ý, Hán trong bản dịch chính (ngoài tên riêng, tên sách, mã số, URL): **PASS**
- Câu bị động đã được chuyển sang chủ động (S18 Grammar Engine): **PASS**
- Không dùng đại từ "mình", "hắn", "y", "nó" cho người: **PASS**
- Không dùng "xong", "tiến hành", "sắp sẽ", "chuẩn bị sẽ" theo cách không đúng VNCH: **PASS**

### 3.8 Toàn vẹn nội dung
- Dịch đầy đủ 33 đoạn, không lược bỏ, không tóm tắt, không tự ý diễn giải: **PASS**
- Không tự tạo nội dung, dữ kiện, thuật ngữ hoặc chú thích: **PASS**
- Giữ cấu trúc chương, tiêu đề, tiêu đề phụ, đoạn văn, chú thích, trích dẫn, bảng, công thức: **PASS**

## 4. NỘI DUNG KHÔNG THỂ XÁC MINH (UNVERIFIABLE)

| Mục | Lý do |
|-----|-------|
| Word COM verify cước chú trong DOCX (Criterion 8) | Cần phần mềm Microsoft Word COM automation, không có sẵn trong môi trường này |
| So sánh chính xác từng chữ với bản PDF gốc | Chỉ có file text extracted, không có PDF gốc để đối chiếu trực tiếp |
| Kiểm tra âm thanh/xuất âm thanh của tên riêng người Pháp (Jean de Lattre de Tassigny, Raoul Salan, Marcel Carpentier, Lionel-Max Chassin) | Tên riêng được giữ nguyên, không có phiên âm chuẩn VNCH trong lexicon |

## 5. LỖI CÒN TỒN (REMAINING ERRORS)

| # | Mô tả | Vị trí | Mức độ | Ghi chú |
|---|-------|--------|--------|---------|
| 1 | Footnote alignment trong source text có 42 markers bị hỏng do trích xuất PDF (con số trang 200, 219, 220, 300, 1946) | `translation-project/02_extracted_text/v1/ch10.txt` | Không phải lỗi译 | Đây là artifact của quá trình extract text từ PDF, không phải lỗi của bản dịch tiếng Việt. Bản dịch tiếng Việt có 19 cước chú đúng [1]–[19]. |
| 2 | Cần Word COM verify DOCX cước chú (Quality Gate Criterion 8) | `09_docx/V1-C10_*.docx` | Minor | Không thể thực hiện trong môi trường này (cần Microsoft Word COM automation). |

Không còn lỗi dịch thuật, lỗi thuật ngữ, lỗi định dạng, hoặc lỗi ngôn ngữ nào khác trong bản dịch Chương 10.

## 6. CHẤT LƯỢNG DỊCH — TÓM TẮT

| Tiêu chí | Kết quả |
|----------|---------|
| Encoding (UTF-8/NFC/no-BOM/LF) | PASS |
| Chính tả VNCH | PASS |
| Alignment src↔vi (33/33) | PASS |
| Cước chú [1]–[19] | PASS |
| Định dạng DOCX | PASS |
| Hình ảnh + caption | PASS |
| Thuật ngữ VNCH | PASS |
| Tính chất ngôn ngữ (không có từ ngoại ngữ vô nghĩa) | PASS |
| Không fabricate | PASS |
| Toàn vẹn cấu trúc | PASS |
| **TỔNG KẾT** | **HOÀN TẤT — ĐẠT CHẤT LƯỢNG** |

## 7. FILES ĐÃ SỬ DỬ / TẠO MỚI

| File | Hành động |
|------|-----------|
| `translation-project/04_translation/v1/ch10/v1_ch10_vi.txt` | Ghi đè hoàn toàn (bản dịch cũ kém chất lượng → bản dịch mới đầy đủ) |
| `translation-project/09_docx/V1-C10_The-French-Indochina-War-in-Northern-Vietnam.docx | Tạo mới (build từ script build_chapter_docx.py) |
| `translation-project/00_plan/progress.json` | Cập nhật entry V1-C10 |

## 8. KẾT LUẢN

Chương 10 đã được dịch lại toàn bộ từ tiếng Anh sang tiếng Việt miền Nam theo truyền thống VNCH (pre-1975), tuân thủ nghiêm ngặt `translation-workflow` skill và toàn bộ rules/references/glossary của dự án. Tất cả 33 đoạn văn, 19 cước chú, 2 hình ảnh, 3 heading block đã được dịch đầy đủ, không lược bỏ, không tóm tắt. Bản dịch đã vượt qua tất cả kiểm tra chất lượng có thể thực hiện trong môi trường hiện tại. Criterion 8 (Word COM verify DOCX footnotes) cần thực hiện riêng khi có môi trường Microsoft Word.