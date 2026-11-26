# QA_ACCEPTANCE_CRITERIA.md — TIÊU CHÍ NGHIỆM THU

**Dự án:** The Origins of Totalitarianism — Hannah Arendt (VNCH rebuild)  
**File:** `.kilo/plans/QA_ACCEPTANCE_CRITERIA.md`  
**Phiên bản:** 1.0

---

## 1. 10 MỤC KIỂM TRA BẮT BUỘC (TỪNG THÀNH PHẦN)

Mỗi thành phần (19 thành phần: 6 phần mở đầu + 13 chương) phải pass tất cả 10 mục kiểm tra dưới đây trước khi được đánh dấu HOAN_TAT.

| # | Mục kiểm tra | Tiêu chí PASS | Phương pháp kiểm tra | Vị trí lỗi ghi nhận |
|---|-------------|---------------|----------------------|---------------------|
| Q1 | Source–Translation mapping 1:1 | Số đoạn src = số đoạn vi; ID và thứ tự khớp chính xác | `debug_align.py` + kiểm tra thủ công | Chapter ID, paragraph ID |
| Q2 | Nội dung dịch thiếu, thừa, sai nghĩa, sai ngữ cảnh | Mỗi đoạn dịch tương ứng đúng đoạn source; không thiếu, không thừa thông tin | Đối chiếu từng đoạn src↔vi | Chapter ID, paragraph ID, nội dung sai |
| Q3 | Ngoại ngữ còn sót trong thân bài | Không còn câu/đoạn tiếng Anh, Pháp, Đức, Latin chưa dịch (ngoại trừ tên riêng, địa danh, nhan đề cần giữ nguyên ngữ) | Quét regex từ khóa ngoại ngữ + đọc thủ công | Chapter ID, paragraph ID, đoạn ngoại ngữ |
| Q4 | Đoạn trống, đoạn trùng, đoạn ghép sai | Không đoạn trống giả (trừ `[TRONG]` UNVERIFIED); không đoạn trùng; không đoạn ghép từ nhiều trang không đúng ranh giới | Kiểm tra thủ công + regex | Chapter ID, paragraph ID |
| Q5 | Tiêu đề chương và subheading bị lặp | Tiêu đề chương xuất hiện 1 lần (heading riêng, không merged với body); không subheading trùng | Kiểm tra cấu trúc file TXT + DOCX | Chapter ID, heading text |
| Q6 | Nối đoạn qua trang | Câu bị ngắt qua trang được gộp lại chính xác; không đoạn verlانی hoặc thiếu câu | Kiểm tra `ocr_reconstruct.py` output + đọc thủ công | Chapter ID, trang PDF, vị trí ngắt |
| Q7 | Chú thích và trích dẫn | Mỗi footnote marker trong body có định nghĩa trong FOOTNOTES block; số lượng khớp | `debug_align.py` footnote check | Chapter ID, footnote number |
| Q8 | Thuật ngữ và văn phong | Dùng thuật ngữ VNCH theo ARENDT_TERMINOLOGY.md + STYLE_GUIDE_PHAN_B.md; không hiện đại hóa (chánh phủ ≠ chính phủ, v.v.) | `apply_vnch_fixes.py` + đọc thủ công | Chapter ID, từ sai, thuật ngữ đúng |
| Q9 | Cấu trúc DOCX và Word Styles | Heading 1/2/3 đúng cấp; Body, quotation, footnote, bibliography có Styles riêng; không lặp tiêu đề; không header chạy vào body | Mở DOCX trong Word, kiểm tra Styles pane | Chapter ID, style name, vấn đề |
| Q10 | Tính toàn vẹn của nội dung so với nguyên bản | Không bịa thêm, không lược bỏ, không thay đổi lập luận của Arendt | Đối chiếu toàn bộ nội dung src↔vi | Chapter ID, nội dung bị thay đổi |

---

## 2. CHI TIẾT TỪNG MỤC KIỂM TRA

### Q1 — Source–Translation mapping 1:1

**Tiêu chí:**
- File source (`02_extracted_text/v2/{name}_src.txt`) và file translation (`04_translation/v2/chNN/v1_chNN_vi.txt`) phải có cùng số đoạn
- Mỗi đoạn phải có ID `[V1CNN-PNNN]` khớp nhau
- Thứ tự đoạn phải giống nhau

**Phương pháp:**
- Chạy `python 99_scripts/debug_align.py chNN` — kiểm tra số đoạn và ID
- Nếu `src_count != vi_count` → FAIL

**Ghi nhận lỗi:**
- Chapter ID, paragraph ID src, paragraph ID vi, số đoạn src, số đoạn vi

### Q2 — Nội dung dịch thiếu, thừa, sai nghĩa, sai ngữ cảnh

**Tiêu chí:**
- Mỗi đoạn dịch phải truyền đạt đầy đủ ý nghĩa của đoạn source
- Không được lược bỏ câu nào, không được thêm câu không có trong source
- Không được dịch sai nghĩa hoặc sai ngữ cảnh

**Phương pháp:**
- Đọc từng đoạn src và đoạn vi tương ứng, đối chiếu ý nghĩa
- Kiểm tra câu cuối cùng của mỗi đoạn phải kết thúc bằng dấu chấm hết (Quy tắc 16 Style Guide)

**Ghi nhận lỗi:**
- Chapter ID, paragraph ID, loại lỗi (thiếu/thừa/sai nghĩa/sai ngữ cảnh), nội dung nguồn, nội dung dịch

### Q3 — Ngoại ngữ còn sót trong thân bài

**Tiêu chí:**
- Không còn câu hoặc đoạn tiếng Anh, Pháp, Đức, Latin chưa dịch trong thân bài
- Ngoại ngữ chỉ được giữ lại khi là tên riêng, địa danh, nhan đề sách/báo cần giữ nguyên ngữ
- Khi giữ nguyên ngữ, phải cung cấp nghĩa tiếng Việt phù hợp (trong ngoặc hoặc cước chú)

**Phương pháp:**
- Quét file translation bằng regex để tìm từ khóa ngoại ngữ (ví dụ: "totalitarian", "apologia pro vita sua", "Tiers Etat", v.v.)
- Đọc thủ công từng đoạn có thể chứa ngoại ngữ

**Ghi nhận lỗi:**
- Chapter ID, paragraph ID, đoạn ngoại ngữ chưa dịch, ngữ nguyên ngữ

### Q4 — Đoạn trống, đoạn trùng, đoạn ghép sai

**Tiêu chí:**
- Không có đoạn trống giả (trừ `[TRONG]` đã đánh dấu UNVERIFIED)
- Không có hai đoạn có nội dung giống hệt nhau
- Không có đoạn ghép từ nhiều trang mà không đúng ranh giới trang

**Phương pháp:**
- Kiểm tra từng đoạn trong file translation có nội dung trống không
- So sánh mỗi cặp đoạn để tìm đoạn trùng
- Kiểm tra ranh giới trang trong đoạn

**Ghi nhận lỗi:**
- Chapter ID, paragraph ID, loại lỗi (trống/trùng/ghép sai), trang PDF liên quan

### Q5 — Tiêu đề chương và subheading bị lặp

**Tiêu chí:**
- Tiêu đề chương xuất hiện duy nhất 1 lần, dưới dạng heading riêng (không merged với body paragraph đầu tiên)
- Không có subheading trùng lặp cùng cấp
- Tiêu đề chạy đầu trang không được lọt vào body

**Phương pháp:**
- Kiểm tra P001 của mỗi chapter có phải tiêu đề chapter merged với body không
- Kiểm tra các heading trong DOCX có trùng không
- Kiểm tra running header text có được prepended vào body không

**Ghi nhận lỗi:**
- Chapter ID, heading text bị lặp, vị trí lặp

### Q6 — Nối đoạn qua trang

**Tiêu chí:**
- Câu bị ngắt qua ranh giới trang phải được gộp lại thành một câu hoàn chỉnh
- Không có đoạn verlاني (bị cắt giữa câu)
- Số trang trong mã `[V1CNN-PNNN] (trang N)` phải chính xác

**Phương pháp:**
- Kiểm tra output của `ocr_reconstruct.py` — đoạn bị ngắt qua trang có được gộp không
- Đọc đoạn ở ranh giới trang để xác nhận câu hoàn chỉnh

**Ghi nhận lỗi:**
- Chapter ID, paragraph ID, trang PDF, nội dung bị cắt

### Q7 — Chú thích và trích dẫn

**Tiêu chí:**
- Mỗi footnote marker (superscript) trong body phải có định nghĩa tương ứng trong FOOTNOTES block
- Số lượng footnote trong body và FOOTNOTES block phải khớp
- Footnote content phải được dịch sang tiếng Việt

**Phương pháp:**
- Chạy `debug_align.py chNN` — kiểm tra footnote defs vs body markers
- Kiểm tra không có orphan marker (có marker trong body nhưng không có def) và không có orphan def (có def nhưng không có marker)

**Ghi nhận lỗi:**
- Chapter ID, footnote number, loại lỗi (missing marker / orphan marker / orphan def)

### Q8 — Thuật ngữ và văn phong

**Tiêu chí:**
- Dùng thuật ngữ VNCH theo ARENDT_TERMINOLOGY.md (ví dụ: chánh phủ, chánh trị, dân biểu, tài chánh, v.v.)
- Không hiện đại hóa từ VNCH (không dùng "chính phủ", "đại biểu", "tài chính" trong ngữ cảnh VNCH)
- Văn phong miền Nam VNCH trước 1975: `chớ`, `nầy`, `dầu/dẫu`, `vả`, `trái lại`, `tuy vậy`, `bởi thế`, thể khía đầy đủ, chủ động hóa, chỉ định danh từ
- Không dịch word-for-word (Quy tắc 19 Style Guide — CẤM KỊ)

**Phương pháp:**
- Chạy `apply_vnch_fixes.py` để phát hiện từ vi phạm VNCH orthography
- Đọc thủ công từng đoạn để kiểm tra văn phong

**Ghi nhận lỗi:**
- Chapter ID, paragraph ID, từ sai, thuật ngữ đúng theo VNCH

### Q9 — Cấu trúc DOCX và Word Styles

**Tiêu chí:**
- Heading 1/2/3 đúng cấp (Heading 1 cho chapter title, Heading 2 cho section, Heading 3 cho subsection)
- Body Text, Block Quotation, Footnote, Bibliography có Word Styles riêng
- Không lặp tiêu đề chương ở đầu nội dung DOCX
- Không để tiêu đề chạy đầu trang lọt vào body DOCX
- Chú thích đúng vị trí và liên kết với footnote marker
- Hỗ trợ Navigation Pane và mục lục tự động (TOC field)

**Phương pháp:**
- Mở DOCX trong Microsoft Word, kiểm tra Styles pane
- Chạy `validate_docx.py` hoặc `check_master.py` để kiểm tra cấu trúc
- Kiểm tra `Footnotes.Count` trong Word khớp với số footnote trong progress.json

**Ghi nhận lỗi:**
- Chapter ID, style name, vấn đề cấu trúc, footnote count mismatch

### Q10 — Tính toàn vẹn của nội dung so với nguyên bản

**Tiêu chí:**
- Không bịa thêm thông tin không có trong nguyên bản (Quy tắc 27 Style Guide — Chống fabricate)
- Không lược bỏ nội dung từ nguyên bản
- Không thay đổi lập luận của Hannah Arendt
- Trích dẫn phải chính xác

**Phương pháp:**
- Đọc toàn bộ src và vi, đối chiếu nghĩa
- Kiểm tra không có thông tin được thêm vào từ bên ngoài

**Ghi nhận lỗi:**
- Chapter ID, paragraph ID, nội dung bịa/lược bỏ/thay đổi, nguồn gốc

---

## 3. BẢNG GHI NHẬN LỖI (ERROR LOG FORMAT)

Mỗi lỗi được ghi nhận theo format sau:

```
[ERROR-{chapter}-{paragraph_id}-{Q#}]
Chapter: {chapter_id}
Paragraph ID: {paragraph_id}
QA Criterion: Q{1-10}
Category: {thiếu/thừa/sai nghĩa/sai ngữ cảnh/ngoại ngữ/trống/trùng/ghép sai/vi phạm thuật ngữ/vi phạm cấu trúc/fabricate}
Root Cause: {nguyên nhân}
Required Correction: {cách sửa}
Verification: {phương pháp kiểm chứng}
Status: {OPEN/FIXED/VERIFIED}
```

**Ví dụ:**
```
[ERROR-ch02-P029-Q3]
Chapter: ch02
Paragraph ID: P029
QA Criterion: Q3
Category: Ngoại ngữ chưa dịch (German)
Root Cause: Đoạn văn tiếng Đức về người Do Thái tại Áo chưa được dịch
Required Correction: Dịch toàn bộ đoạn tiếng Đức sang tiếng Việt theo Style Guide
Verification: Đọc đoạn dịch và so sánh với nguồn tiếng Đức
Status: FIXED
```

---

## 4. TIÊU CHÍ HOAN_TAT

Một thành phần chỉ được đánh dấu `HOAN_TAT` khi:

1. Tất cả 10 mục QA (Q1-Q10) PASS
2. Tất cả lỗi trong Error Log có status `VERIFIED`
3. File translation tồn tại tại `04_translation/v2/chNN/v1_chNN_vi.txt`
4. File DOCX tồn tại tại `09_docx/V2-NN_chNN.docx`
5. `progress.json` đã được cập nhật với trạng thái HOAN_TAT

---

## 5. QA CHO TOÀN BỘ TÁC PHẨM (SAU ĐỦ 13 CHƯƠNG)

Sau khi đủ 13 chương đã HOAN_TAT, chạy QA toàn bộ tác phẩm:

| # | Mục kiểm tra | Tiêu chí PASS |
|---|-------------|---------------|
| Q11 | Nhất quán thuật ngữ xuyên suốt 13 chương | Thuật ngữ được dùng nhất quán (ví dụ: "toàn trị" không thay thế bằng "tổng thể chủ nghĩa" ở chương nào) |
| Q12 | Cấu trúc DOCX tổng hợp (MASTER) | TOC tự động, Navigation Pane, continuous footnotes 892+, Heading 1/2/3 đúng cấp |
| Q13 | Không content loss giữa các chapter | Tổng số đoạn trong 13 chapter DOCX = tổng số đoạn trong source |
| Q14 | Encoding toàn bộ file | Tất cả file TXT và DOCX UTF-8/NFC/no BOM/LF |

---

## 6. SCRIPTS DÙNG CHO QA

| Script | Vị trí | Mục đích |
|--------|--------|----------|
| `debug_align.py` | `99_scripts/` | Kiểm tra alignment src=vi, footnote markers |
| `qa_gate.py` | `99_scripts/` | Chạy 11 quality gate trên DOCX |
| `validate_docx.py` | `99_scripts/` | Kiểm tra cấu trúc DOCX |
| `check_master.py` | `99_scripts/` | Kiểm tra master DOCX |
| `apply_vnch_fixes.py` | `99_scripts/` | Phát hiện vi phạm VNCH orthography |
| `clean_foreign_fragments.py` | `99_scripts/` | Phát hiện CJK/Cyrillic contamination |
| `clean_english_ch12.py` | `99_scripts/` | Phát hiện English fragments |
