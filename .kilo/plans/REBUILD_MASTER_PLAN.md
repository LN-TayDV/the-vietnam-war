# REBUILD_MASTER_PLAN.md — THE ORIGINS OF TOTALITARIANISM (13 CHAPTERS, VNCH)

**Dự án:** The Origins of Totalitarianism — Hannah Arendt (dịch VNCH trước 1975)  
**Root:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\`  
**File:** `.kilo/plans/REBUILD_MASTER_PLAN.md`  
**Phiên bản:** 2.0 (STRUCTURE FIRST)  
**Ngày:** 2026-11-26

---

## 1. NGUYÊN TẮC CỐT LÕI

1. **Không bắt đầu bằng việc sửa bản dịch hiện tại.** Tất cả chapter cũ đã đánh `HOAN_TAT` KHÔNG được xem là bằng chứng chất lượng.
2. **STRUCTURE FIRST → SOURCE VALIDATION → TRANSLATION REBUILD → PUBLICATION.** Chỉ khi cấu trúc chương, heading, subheading, paragraph và footnote được đối chiếu với PDF và đạt yêu cầu mới được chuyển sang dịch thuật.
3. **Không dịch hoặc hiệu đính bản dịch trước khi Source Structure PASS.**
4. **Không xem việc xuất được TXT là bằng chứng cấu trúc chính xác.**
5. **Không xem số paragraph bằng nhau là bằng chứng nội dung khớp.**
6. UTF-8, NFC, không BOM, LF cho toàn bộ file văn bản.
7. Mọi script và file text mới lưu trong `99_scripts`.
8. Không ghi đè nguyên bản hoặc xóa dữ liệu nguồn.

---

## 2. CÂU HỎI VÀ ĐÁP ÁN (8 CÂU HỎI CỦA NGƯỜI DÙNG)

### Câu 1: PDF hiện tại được tổ chức và trích xuất như thế nào?

**PDF gốc:** `books/Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf` (574 trang)

**Công cụ trích xuất:** `99_scripts/extract_chapters.py` (PyMuPDF/fitz)

**Cách tổ chức:**
- Mỗi trang PDF được trích xuất riêng với đánh dấu `=== PAGE N ===`
- 19 thành phần được xác định bằng phạm vi trang (xem bảng dưới)
- Raw text từ `get_text()` có thể chứa running header, page number, footnote inline cùng body

**Phạm vi trang 19 thành phần:**

| # | Thành phần | Trang PDF | Loại |
|---|------------|-----------|------|
| 1 | front_matter | 1–7 | Phần mở đầu |
| 2 | preface_first_edition | 8–10 | Lời nói đầu bản dựng lần thứ nhất |
| 3 | preface_part_one | 11–16 | Lời nói đầu phần một |
| 4 | preface_part_two | 17–22 | Lời nói đầu phần hai |
| 5 | preface_part_three | 23–41 | Lời nói đầu phần ba |
| 6 | part_one_intro | 42–47 | Giới thiệu phần một |
| 7 | ch01 | 48–55 | Chương một |
| 8 | ch02 | 56–98 | Chương hai |
| 9 | ch03 | 99–133 | Chương ba |
| 10 | ch04 | 134–167 | Chương bốn |
| 11 | ch05 | 168–202 | Chương năm |
| 12 | ch06 | 203–229 | Chương sáu |
| 13 | ch07 | 230–266 | Chương bảy |
| 14 | ch08 | 267–311 | Chương tám |
| 15 | ch09 | 312–349 | Chương chín |
| 16 | ch10 | 350–387 | Chương mười |
| 17 | ch11 | 388–433 | Chương mười một |
| 18 | ch12 | 434–504 | Chương mười hai |
| 19 | ch13 | 505–574 | Chương mười ba |

---

### Câu 2: Công cụ nào có thể xác định heading và paragraph đáng tin cậy?

**Công cụ hiện có:**

| Công cụ | Vị trí | Chức năng | Hạn chế |
|---------|--------|-----------|---------|
| `extract_chapters.py` | `99_scripts/` | Trích xuất PDF → TXT theo trang | Không nhận diện heading, chỉ tách theo trang |
| `ocr_reconstruct.py` | `99_scripts/` | Tách đoạn, gộp đoạn ngắt trang, gán ID `[V1CNN-PNNN]` | Không nhận diện heading/subheading, không phát hiện OCR sai |

**Công cụ cần thêm (Phase 1):**

| Công cụ | Mục đích |
|---------|----------|
| `99_scripts/structure_detect.py` | Nhận diện chapter title, section heading, subheading từ font size, styling, indentation, casing |
| `99_scripts/structure_manifest.py` | Tạo Structural Manifest (Chapter → Section → Subheading → Paragraph → Footnote) |
| `99_scripts/structure_validate.py` | Đối chiếu Structural Manifest với PDF, kiểm tra missing/duplicate/merged/split |

**Phương pháp nhận diện heading:**
- Font size lớn hơn body text
- Font weight bold
- Casing khác (ALL CAPS hoặc Title Case)
- Indentation khác (không thụt đầu dòng)
- Có thể kết thúc bằng dấu chấm hoặc không (khác với body text thường kết thúc bằng dấu chấm)
- Vị trí đầu trang hoặc sau section break

---

### Câu 3: Làm thế nào phân biệt paragraph continuation qua trang?

**Quy tắc gộp (đã có trong `ocr_reconstruct.py`):**

1. Nếu đoạn trước kết thúc bằng dấu gạch ngang `-` (hyphen) → gộp với đoạn sau, xóa dấu `-`
2. Nếu đoạn sau bắt đầu bằng chữ thường (lowercase) → khả năng cao là continuation, gộp với đoạn trước
3. Nếu đoạn trước kết thúc bằng dấu chấm, chấm hỏi, chấm 느낌, dấu ngoặc đóng → đoạn sau là paragraph mới

**Công cụ cần cải thiện:**

| Vấn đề | Cách xử lý |
|--------|------------|
| Đoạn bị cắt giữa câu không có dấu `-` | Kiểm tra câu chưa hoàn chỉnh (thiếu chủ ngữ, vị ngữ, không kết thúc bằng dấu kết thúc câu) |
| Running header bị gộp vào paragraph đầu trang | Phát hiện running header bằng pattern known headers, tách ra trước khi gộp |
| Page number lẻ lẻ trong paragraph | Phát hiện số trang độc lập, loại bỏ |
| Đoạn trống giữa hai trang | Không gộp, giữ nguyên ranh giới |

**Output:** Mỗi paragraph gán `[V1CNN-PNNN] (trang N)` với trang bắt đầu và trang kết thúc (nếu ngắt qua trang).

---

### Câu 4: Làm thế nào tạo Structural Manifest có thể kiểm chứng?

**Cấu trúc manifest (JSON):**

```json
{
  "chapter": "ch05",
  "pdf_pages": "168-202",
  "structure_tree": [
    {
      "type": "chapter_title",
      "text": "CHƯƠNG NĂM: ...",
      "page": 168,
      "level": 1
    },
    {
      "type": "section_heading",
      "text": "I. ...",
      "page": 168,
      "level": 2,
      "paragraphs": ["P001", "P002"]
    },
    {
      "type": "subheading",
      "text": "A. ...",
      "page": 170,
      "level": 3,
      "paragraphs": ["P003"]
    },
    {
      "type": "paragraph",
      "id": "V1C05-P001",
      "text": "...",
      "page_start": 168,
      "page_end": 168,
      "parent_heading": "I. ..."
    }
  ],
  "footnotes": [
    {"number": 1, "page": 169, "text": "..."}
  ],
  "validation": {
    "total_paragraphs": 37,
    "total_footnotes": 60,
    "missing_content": [],
    "duplicate_paragraphs": [],
    "ocr_errors": []
  }
}
```

**Cơ chế kiểm chứng:**
- Mỗi node trong manifest phải có `page_start` và `page_end` trỏ về PDF
- Tổng số paragraph trong manifest phải khớp với số paragraph trong Raw Source TXT
- Mỗi footnote trong manifest phải có số và nội dung tương ứng trong PDF
- Không có paragraph nào bị bỏ sót (mỗi trang PDF có ít nhất 1 paragraph hoặc được giải thích tại sao trống)

**File đầu ra:** `02_extracted_text/v2/{name}_manifest.json`

---

### Câu 5: Làm thế nào bảo đảm Raw Source TXT phản ánh chính xác PDF?

**Quy trình đối chiếu 3 lớp:**

| Lớp | Đối chiếu | Phương pháp |
|-----|-----------|-------------|
| L1 | PDF ↔ Structural Manifest | Mỗi node manifest có page_start/page_end, kiểm tra không bỏ sót trang |
| L2 | Structural Manifest ↔ Raw Source TXT | Số paragraph, ID, thứ tự khớp chính xác |
| L3 | Raw Source TXT ↔ PDF (đọc lại) | Đọc ngẫu nhiên 10% trang PDF, so sánh nội dung với TXT |

**Công cụ:** `99_scripts/structure_validate.py`

**Tiêu chí PASS:**
- Mỗi trang PDF được biểu diễn trong manifest (hoặc có lý do合法 tại sao trống)
- Số paragraph manifest = số paragraph Source TXT
- ID paragraph theo định dạng `[V1CNN-PNNN]`, thứ tự 1..N không bị bỏ
- Không có paragraph trùng nội dung
- Không có đoạn ghép sai (paragraph chứa nội dung từ 2 heading khác nhau)

---

### Câu 6: Làm thế nào phát hiện OCR sai, heading sai và paragraph segmentation sai?

**OCR sai:**
- Phát hiện từ không tồn tại trong từ điển tiếng Anh/Pháp/Đức (nếu là phần ngoại ngữ)
- Phát hiện ký tự lạ (ví dụ: "Pan-Xlaven" thay vì "Pan-Slavism", "Pan-Duc" thay vì "Pan-Deutsch")
- Phát hiện từ bị ghép hoặc tách sai (ví dụ: "đoạnvăn" thay vì "đoạn văn")
- Công cụ: quét regex từ khóa OCR-known-errors, so sánh với ARENDT_TERMINOLOGY.md

**Heading sai:**
- Phát hiện văn bản có font size lớn nhưng được gán làm body paragraph
- Phát hiện body text có format heading (ALL CAPS, bold) nhưng không được gán heading ID
- Công cụ: so sánh cấu trúc manifest với heading thực tế trong PDF

**Paragraph segmentation sai:**
- Phát hiện paragraph quá dài (khả năng được gộp từ nhiều paragraph)
- Phát hiện paragraph quá ngắn (khả năng bị tách từ 1 paragraph)
- Phát hiện paragraph không có câu hoàn chỉnh (thiếu dấu kết thúc)
- Phát hiện 2 paragraph có nội dung giống hệt nhau (duplicate)
- Công cụ: phân tích độ dài, dấu kết thúc câu, so sánh nội dung

---

### Câu 7: Làm thế nào nghiệm thu cấu trúc từng chương trước khi dịch?

**STRUCTURAL GATE (bắt buộc PASS trước khi dịch):**

| # | Mục kiểm tra | Tiêu chí PASS | Phương pháp |
|---|-------------|---------------|-------------|
| S1 | Chapter boundary | Mỗi chapter có phạm vi trang đúng, không chồng chéo | So sánh manifest với PDF page ranges |
| S2 | Chapter title | Có đúng 1 chapter title, không merged với body | Kiểm tra manifest node type=chapter_title |
| S3 | Section/subheading | Tất cả heading được nhận diện, đúng thứ tự | Kiểm tra manifest nodes type=section_heading, subheading |
| S4 | Paragraph completeness | Mỗi paragraph có nội dung, không bị cắt giữa câu | Kiểm tra dấu kết thúc câu, page_start/page_end |
| S5 | No duplicate paragraph | Không 2 paragraph có nội dung giống hệt | So sánh nội dung paragraph 2 theo 2 |
| S6 | No missing content | Mỗi trang PDF có ít nhất 1 paragraph hoặc lý do trống | Kiểm tra từng trang trong manifest |
| S7 | Footnote completeness | Mỗi footnote marker trong body có định nghĩa | So sánh body markers với footnote definitions |
| S8 | ID stability | ID paragraph `[V1CNN-PNNN]` thứ tự 1..N không bị bỏ | Kiểm tra ID sequence |
| S9 | Source TXT integrity | Source TXT được sinh từ manifest, không nối thô OCR | Kiểm tra file nguồn của Source TXT |
| S10 | Cross-reference | Manifest ↔ Source TXT ↔ PDF khớp 3 lớp | Chạy `structure_validate.py` |

**Nếu bất kỳ mục S1–S10 FAIL:** Không được chuyển sang Phase 3 (dịch). Phải sửa manifest và Source TXT lại.

---

### Câu 8: Làm thế nào duy trì mapping ổn định cho toàn bộ 13 chương?

**ID Format:** `[V1CNN-PNNN]` (ví dụ: `[V1C05-P012]`)

**Quy tắc mapping:**
- Mỗi paragraph trong Source TXT có ID duy nhất, không thay đổi trong suốt vòng đời
- Translation TXT phải có cùng ID, cùng thứ tự, cùng số lượng
- Mỗi footnote marker trong body phải trỏ đến footnote definition có cùng số
- Heading-parent mapping được lưu trong manifest, không bị thay đổi khi dịch

**Công cụ kiểm tra:** `99_scripts/debug_align.py` (kiểm tra src=vi paragraph count và ID order)

---

## 3. PHASE 1 — ORIGINAL STRUCTURAL RECONSTRUCTION

**Mục tiêu:** Tái lập chính xác cấu trúc của nguyên bản PDF cho từng chương.

### Bước 1.1: Xác định cấu trúc chương (mỗi thành phần)

| Task | Thành phần | Công việc | Output | Checkpoint |
|------|------------|-----------|--------|------------|
| 1.1.1 | front_matter | Xác định chapter boundary, title, section, subheading | `v2/front_matter_structure.json` | CP-1 |
| 1.1.2 | preface_first_edition | Tương tự | `v2/preface_first_edition_structure.json` | CP-1 |
| 1.1.3 | preface_part_one | Tương tự | `v2/preface_part_one_structure.json` | CP-1 |
| 1.1.4 | preface_part_two | Tương tự | `v2/preface_part_two_structure.json` | CP-1 |
| 1.1.5 | preface_part_three | Tương tự | `v2/preface_part_three_structure.json` | CP-1 |
| 1.1.6 | part_one_intro | Tương tự | `v2/part_one_intro_structure.json` | CP-1 |
| 1.1.7 | ch01 | Tương tự | `v2/ch01_structure.json` | CP-1 |
| 1.1.8 | ch02 | Tương tự | `v2/ch02_structure.json` | CP-1 |
| 1.1.9 | ch03 | Tương tự | `v2/ch03_structure.json` | CP-1 |
| 1.1.10 | ch04 | Tương tự | `v2/ch04_structure.json` | CP-1 |
| 1.1.11 | ch05 | Tương tự | `v2/ch05_structure.json` | CP-1 |
| 1.1.12 | ch06 | Tương tự | `v2/ch06_structure.json` | CP-1 |
| 1.1.13 | ch07 | Tương tự | `v2/ch07_structure.json` | CP-1 |
| 1.1.14 | ch08 | Tương tự | `v2/ch08_structure.json` | CP-1 |
| 1.1.15 | ch09 | Tương tự | `v2/ch09_structure.json` | CP-1 |
| 1.1.16 | ch10 | Tương tự | `v2/ch10_structure.json` | CP-1 |
| 1.1.17 | ch11 | Tương tự | `v2/ch11_structure.json` | CP-1 |
| 1.1.18 | ch12 | Tương tự | `v2/ch12_structure.json` | CP-1 |
| 1.1.19 | ch13 | Tương tự | `v2/ch13_structure.json` | CP-1 |

### Bước 1.2: Tái lập paragraph structure (mỗi thành phần)

- Gán Paragraph ID duy nhất `[V1CNN-PNNN]`
- Xác định parent heading ID cho mỗi paragraph
- Ghi thứ tự xuất hiện, nội dung nguyên bản, trang bắt đầu/kết thúc
- Trạng thái reconstruction (OK / NEEDS_REVIEW / OCR_ERROR)

### Bước 1.3: Phục hồi cấu trúc PDF

- Nối đoạn văn bị ngắt qua trang (quy tắc hyphen + lowercase đầu dòng)
- Loại running headers và page numbers khỏi body
- Nhận diện quotation, footnotes, citations, bibliography
- Phát hiện tiêu đề bị OCR nhầm thành body
- Phát hiện nhiều đoạn bị nối thành một
- Phát hiện một đoạn bị chia sai thành nhiều đoạn

### Bước 1.4: Tạo Structural Manifest

- Sinh file `{name}_manifest.json` cho từng thành phần
- Cây cấu trúc: Chapter → Section → Subheading → Paragraph → Footnote/Quotation
- Manifest là cơ sở để sinh Raw Source TXT

**Điều kiện chuyển sang Phase 2:** Tất cả 19 file `*_structure.json` và `*_manifest.json` đã tồn tại.

---

## 4. PHASE 2 — SOURCE TXT REBUILD AND VALIDATION

**Mục tiêu:** Sinh Raw Source TXT từ Structural Manifest, đảm bảo chính xác trước khi dịch.

### Bước 2.1: Sinh Raw Source TXT (mỗi thành phần)

- Sinh từ manifest (không nối thô kết quả OCR)
- Bảo toàn thứ tự heading và paragraph
- Gắn ID ổn định `[V1CNN-PNNN]`
- Đảm bảo paragraph body không bị gộp hoặc tách sai

**Output:** `02_extracted_text/v2/{name}_src.txt`

### Bước 2.2: Đối chiếu với PDF nguyên bản

- Đối chiếu từng phần với PDF
- Kiểm tra không thiếu hoặc trùng nội dung
- Kiểm tra footnote marker khớp với footnote definition

### Bước 2.3: Tạo báo cáo Structural QA

- Mỗi chapter có báo cáo Structural QA riêng
- Ghi nhận mọi lỗi cấu trúc đã tìm thấy và đã sửa

### STRUCTURAL GATE (bắt buộc PASS)

| # | Mục | Tiêu chí | Phương pháp |
|---|-----|----------|-------------|
| S1 | Chapter boundary | Phạm vi trang đúng, không chồng chéo | So sánh manifest với PDF |
| S2 | Chapter title | Đúng 1 title, không merged với body | Kiểm tra manifest |
| S3 | Section/subheading | Tất cả heading nhận diện đúng thứ tự | Kiểm tra manifest nodes |
| S4 | Paragraph completeness | Mỗi paragraph có nội dung, không bị cắt | Kiểm tra dấu kết thúc câu |
| S5 | No duplicate | Không 2 paragraph nội dung giống hệt | So sánh 2 theo 2 |
| S6 | No missing content | Mỗi trang có ít nhất 1 paragraph hoặc lý do trống | Kiểm tra từng trang |
| S7 | Footnote completeness | Mỗi marker có định nghĩa | So sánh markers với definitions |
| S8 | ID stability | ID thứ tự 1..N không bị bỏ | Kiểm tra sequence |
| S9 | Source TXT integrity | Sinh từ manifest, không nối thô OCR | Kiểm tra nguồn file |
| S10 | Cross-reference | Manifest ↔ Source TXT ↔ PDF khớp | `structure_validate.py` |

**Nếu bất kỳ mục FAIL:** Không được chuyển sang Phase 3. Phải sửa manifest và Source TXT lại.

---

## 5. PHASE 3–6 (TÓM TẮT, CHI TIẾT SẼ ĐƯỢC Lập SAU KHI PHASE 1–2 HOÀN TẤT)

| Phase | Mục tiêu | Điều kiện bắt đầu |
|-------|----------|-------------------|
| Phase 3 | Fresh Translation (dịch mới từ validated source) | Structural Gate PASS |
| Phase 4 | Vietnamese Editing and Alignment | Translation complete |
| Phase 5 | DOCX Reconstruction | Editing complete |
| Phase 6 | Final QA (full chain validation) | DOCX built |

---

## 6. FILES CẦN TẠO (TRONG 99_SCSRIPTS)

| File | Mục đích |
|------|----------|
| `99_scripts/structure_detect.py` | Nhận diện heading, subheading từ font/styling/indentation |
| `99_scripts/structure_manifest.py` | Tạo Structural Manifest JSON |
| `99_scripts/structure_validate.py` | Đối chiếu Manifest ↔ Source TXT ↔ PDF |
| `99_scripts/ocr_error_detect.py` | Phát hiện OCR sai, heading sai, segmentation sai |
| `02_extracted_text/v2/{name}_structure.json` | Cấu trúc chi tiết từng thành phần |
| `02_extracted_text/v2/{name}_manifest.json` | Structural Manifest từng thành phần |

---

## 7. PROGRESS TRACKING

Cập nhật `00_plan/progress.json` với trạng thái thực tế:

| Status | Ý nghĩa |
|--------|---------|
| `not_started` | Chưa bắt đầu |
| `structure_detecting` | Đang nhận diện cấu trúc |
| `structure_done` | Cấu trúc đã xác định |
| `manifest_done` | Manifest đã tạo |
| `source_validated` | Source TXT đã đối chiếu xong |
| `structural_gate_pass` | Structural Gate PASS (sẵn sàng dịch) |
| `translating` | Đang dịch |
| `editing` | Đang hiệu đính |
| `qa_pending` | Chưa chạy QA |
| `qa_done` | QA đã chạy |
| `docx_built` | DOCX đã build |
| `HOAN_TAT` | Hoàn tất tất cả 10 mục QA + DOCX |

---

## 8. CÁCH TIẾP TUYẾN KHI GIẢN ĐOẠN

1. Kiểm tra `progress.json` để xem thành phần cuối cùng đã hoàn tất Structural Gate
2. Tiếp tục từ thành phần tiếp theo (không bắt đầu lại từ đầu)
3. Không ghi đè file đã structural_gate_pass
4. Cập nhật `progress.json` sau mỗi checkpoint

---

## 9. RÚU RO VÀ PHƯƠNG ÁN XỬ LÝ

| Rủi ro | Mức độ | Phương án xử lý |
|--------|--------|-----------------|
| PDF gốc không thể mở | Cao | Kiểm tra `extract_chapters.py` có thể mở PDF trước khi bắt đầu |
| Heading không được nhận diện chính xác | Cao | Sử dụng nhiều tín hiệu (font size, weight, casing, indentation) kết hợp |
| Paragraph bị gộp sai qua trang | Trung bình | Áp dụng quy tắc hyphen + lowercase, sau đó đọc thủ công xác nhận |
| Footnote bị mất hoặc neo sai | Cao | Đối chiếu 1:1 giữa body marker và footnote definition trước Structural Gate |
| OCR sai gây hiểu nhầm heading | Trung bình | Quét regex từ khóa OCR-known-errors, so sánh với terminology |

---

## 10. ĐIỀU KIỆN KẾT THÚC PHASE 1–2

- [ ] Tất cả 19 thành phần có file `*_structure.json`
- [ ] Tất cả 19 thành phần có file `*_manifest.json`
- [ ] Tất cả 19 thành phần có Raw Source TXT (`*_src.txt`)
- [ ] Structural Gate PASS cho tất cả 19 thành phần
- [ ] `progress.json` cập nhật trạng thái `structural_gate_pass` cho từng thành phần
- [ ] Mọi lỗi cấu trúc đã được ghi nhận và xử lý

**Chỉ sau khi đủ 10 điều kiện trên mới được chuyển sang Phase 3 (dịch thuật).**
