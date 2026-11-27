# EXECUTION PLAN — FINAL TRANSLATION QA & REPAIR

**Dự án:** Dịch The Cambridge History of the Vietnam War sang tiếng Việt miền Nam (VNCH pre-1975)  
**Thư mục:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project`  
**Skill tham chiếu:** `.kilo/skills/translation-workflow/SKILL.md`  
**Chế độ:** PLAN MODE — chỉ đọc, phân tích, lập kế hoạch. KHÔNG sửa bản dịch, KHÔNG thay đổi file.

---

## 1. WORKSPACE INVENTORY & SOURCE OF TRUTH

### 1.1 Cấu trúc thư mục thực tế (đã khảo sát)

| Thư mục | Mô tả | Trạng thái |
|---|---|---|
| `00_plan/` | progress.json, MASTER_PLAN.md, chapter_inventory.csv, manifest.json, image_manifest.json, chapter_boundaries.json, registry_ch15.json, bug_register.md | Có |
| `01_source_pdf/` | Nơi chứa PDF gốc | **TRỐNG** — không có file PDF |
| `02_extracted_text/v1/` | ch01_src.txt … ch21.txt (text đã trích, UTF-8 NFC, đã xoá watermark) | Có, 21 chương đã trích |
| `02_extracted_text/v2/`, `v3/` | Text trích tập 2, tập 3 | Có (chưa kiểm tra chi tiết) |
| `03_terminology/` | glossary_nam_bac_compare.tsv, POLITICAL_ECONOMIC_GLOSSARY.md/.csv, SOURCES.md, uncertain_terms.md | Có |
| `04_translation/v1/ch01-15/` | Mỗi chương: `v1_chXX_src.txt` + `v1_chXX_vi.txt` (KHÔNG có `_meta.json` như skill khuyến khích) | Có, 15 chương |
| `04_translation/v1/ch15/` | Ngoài ra có `ch15_en_raw.txt`, `v1_ch15_src.txt`, `v1_ch15_vi.txt` | Có |
| `04_translation/v1/images/` | Ảnh raster trích từ PDF | Có |
| `05_qa/` | AUDIT_REPORT_CH01-06.md, AUDIT_REPORT_CH10.md, FINAL_PILOT_QUALITY_GATE.md, GIAO_DOAN_3_REPORT.md, GIAO_DOAN_4_ACCEPTANCE.md, REVIEW_AUDIT_CH14.md, LANGUAGE_PURITY_REVIEW_V1-C08.md, BUG_REGISTER_V1-C11.md, ch06_lessons_learned.md, v1_ch01_pilot_review.md | Có, 10 file |
| `06_reports/` | **TRỐNG** | Không có file |
| `06_temp/` | Có (không kiểm tra chi tiết) | Có |
| `07_style_guide/` | STYLE_GUIDE.md, STYLE_GUIDE_PHAN_B.md, TRANSLATION_GRAMMAR_ENGINE.md | Có |
| `08_southern_vietnamese_library/` | MASTER_LEXICON.csv, TERMINOLOGY_DATABASE.csv, ORTHOGRAPHY_DATABASE.csv, SOURCE_REGISTRY.csv, library_progress.json | Có |
| `09_docx/` | V1-C01 … V1-C15 DOCX (17 file, bao gồm cả V1_Tap-I_Nguon-Coi.docx) | Có, 15 chương đã build DOCX |
| `chinese_check.txt` | File ở gốc translation-project | Có |

### 1.2 XUNG ĐẤT NGUỒN CHẤN THẬP (CRITICAL FINDING)

**Hai dự án khác nhau đang trộn lẫn trong cùng `translation-project/`:**

| Hiệu lực | Nội dung |
|---|---|
| **Dự án A (theo skill + MASTER_PLAN + manifest + extracted_text + src files)** | *The Cambridge History of the Vietnam War*, Cambridge University Press, 3 tập, 77 chương, ~1866 trang PDF, SHA-256 `338BC8B8…`. Chương 1 = Liam C. Kelley "Memory, Tradition…", Chương 2 = Christopher E. Goscha "The Origins of the Vietnamese Revolution". |
| **Dự án B (theo progress.json)** | *The Origins of Totalitarianism — Hannah Arendt*, Harcourt Brace & Jovanovich 1973, 574 trang. |

**Rằng rễ nội dung file dịch:**

| File dịch | Header trong file | Nội dung thực tế | Khớp src? |
|---|---|---|---|
| `v1_ch01_vi.txt` | `V1-C01 · Antisemitism as an Outrage to Common Sense · Hannah Arendt` | Nội dung Hannah Arendt (chủ nghĩa chống người Do Thái, Nazi, người Do Thái) | ❌ KHÔNG — src là Cambridge History Ch1 (Liam C. Kelley) |
| `v1_ch02_vi.txt` | `V1-C02 · The Jews, the Nation-State, and the Birth of Antisemitism · Hannah Arendt` | Nội dung Hannah Arendt | ❌ KHÔNG — src là Cambridge History Ch2 (Goscha) |
| `v1_ch12_vi.txt` | `V1-C12 · Hội nghị Geneva năm 1954 · Martin Thomas` | Nội dung Cambridge History Ch12 | ✅ |
| `v1_ch13_vi.txt` | `V1-C13 · Eisenhower and Vietnam · David L. Anderson` | Nội dung Cambridge History Ch13 | ✅ |
| `v1_ch15_vi.txt` | `15 Xây dựng Quốc gia ở Nam Việt Nam sau Geneva` | Nội dung Cambridge History Ch15 | ✅ |

**Kết luận:** `ch01` và `ch02` bản dịch là nội dung Hannah Arendt, không phải dịch của Cambridge History Ch1/Ch2. Đây là sự oan lẫn dữ liệu nghiêm trọng phải được giải quyết trước khi QA.

### 1.3 progress.json — OUT OF DATE

`00_plan/progress.json` chỉ theo dõi **2 chương** (Ch01 status=translated, Ch02 status=in_progress) và ghi rõ dự án là Hannah Arendt. Tuy nhiên:
- Có 15 chương đã có file dịch trong `04_translation/v1/`
- Có 15 file DOCX trong `09_docx/` (V1-C01 … V1-C15)
- `02_extracted_text/v1/` đã trích đủ 21 chương

**progress.json không phải source of truth cho tiến độ thực tế.**

### 1.4 Source of truth đề xuất (chưa chốt, cần user phê duyệt)

| Loại | File đề xuất làm source of truth | Lý do |
|---|---|---|
| Sách gốc | `The_Cambridge_History_of_the_Vietnam_War.pdf` (SHA-256 trong manifest.json) | Skill, MASTER_PLAN, manifest, extracted_text, src files đều nhất quán quyển này |
| Text nguồn đã trích | `02_extracted_text/v1/chNN.txt` | Đã trích, UTF-8 NFC, đã xoá watermark |
| Bản dịch tham chiếu | `04_translation/v1/chNN/v1_chNN_vi.txt` (ch03-ch15) | Nội dung Cambridge History, khớp src |
| Bản dịch cần kiểm tra lại hoàn toàn | `ch01`, `ch02` | Nội dung Hannah Arendt, không khớp src |
| Tiến độ | Chưa có — progress.json cũ, không phản hồi thực tế | Cần xây dựng lại từ thực tế file hệ thống |
| Đã build DOCX | `09_docx/V1-C01 … V1-C15` | 15 chương đã có DOCX |

### 1.5 Phạm vi chưa hoàn thành / thiếu dữ liệu

- `01_source_pdf/` trống → **không thể đối chiếu PDF gốc trực tiếp** trong giai đoạn này
- `06_reports/` trống → chưa có báo cáo tổng hợp
- Không có `_meta.json` cho bất kỳ chương nào (skill khuyến khích)
- `progress.json` cần xây dựng lại dựa trên thực tế
- Ch01, ch02 bản dịch không khớp src → cần xác định: dịch lại hay thay bằng bản dịch đúng quyển
- Ch11: BUG-008 ghi là 0/0 footnotes, thiếu 21 chú thích → CRITICAL known issue
- Ch10: progress ghi là EXTRACTION_COMPLETE, dịch dở P012+ → chưa hoàn tất

---

## 2. EXISTING SKILL COMPLIANCE REVIEW

Skill `translation-workflow` (SKILL.md) đã định nghĩa quy trình end-to-end với các công cụ và cổng QA. Kế hoạch này **tận dụng sẵn** các thành phần sau, KHÔNG phát minh quy trình mới:

| Thành phần skill | Vị trí | Vai trò trong kế hoạch |
|---|---|---|
| STYLE_GUIDE_PHAN_B.md (v2.3, 29 quy tắc) | `07_style_guide/` | Tiêu chuẩn văn phong VNCH cho Language Quality Audit |
| TRANSLATION_GRAMMAR_ENGINE.md (v2.1) | `07_style_guide/` | 7 bước dịch + Checklist S1-S20, P1-P10, C1-C10 |
| MASTER_LEXICON.csv (321 mục) | `08_southern_vietnamese_library/10_LEXICAL_DATABASE/` | Tra cứu thuật ngữ Nam |
| POLITICAL_ECONOMIC_GLOSSARY.md | `03_terminology/` | 110+ thuật ngữ chính trị-kinh tế-tư tưởng |
| uncertain_terms.md | `03_terminology/` | Hàng đợi thuật ngữ chưa chốt |
| AUDIT_REPORT_CH01-06.md | `05_qa/` | Bài học 222 lỗi đã fix, 6 chương đầu |
| check_footnote_markers.py | `translation-project/99_scripts/` | Kiểm tra missing/duplicate/orphan marker trước build |
| audit_chapter.py | `translation-project/99_scripts/` | Cổng QA bắt buộc: English remnant / footnote leak / VNCH calque / omission / markers |
| document_comparator.py | `.kilo/scripts/common/` | Đối chiếu src↔vi: số đoạn, số câu, cấu trúc, alignment |
| quality_gate.py | `.kilo/scripts/common/` | 8 tiêu chí Quality Gate, output JSON |
| vnch_orthography.py | `.kilo/scripts/common/` | 120+ quy tắc VNCH chính tả |
| encoding_checker.py | `.kilo/scripts/common/` | UTF-8, NFC, no BOM, LF |
| docx_builder.py | `.kilo/scripts/common/` | Build DOCX với real Word footnotes |
| build_chapter_docx.py | `translation-project/99_scripts/` | Script chuẩn xuất DOCX (bố cục sách + footnote chân trang) |
| audit_docx_format.py | `translation-project/99_scripts/` | Validator định dạng DOCX |
| bug_register.md | `00_plan/` | 9 bug đã xác định (BUG-001 … BUG-009) + 4 rủi ro |

**Các bước skill đã xử lý tốt, KHÔNG cần lặp lại trong kế hoạch này:**
- Encoding check (UTF-8/NFC/no BOM/LF)
- Orthography VNCH (chính trị→chánh trị, này→nầy, etc.)
- Footnote marker validation trước build (check_footnote_markers.py)
- DOCX format audit (audit_docx_format.py)
- Word COM Footnotes.Count verification

**Các bước cần bổ sung cho kế hoạch QA & Repair này (skill chưa xử lý):**
- Đối chiếu 3 lớp: PDF gốc ↔ extracted text ↔ bản dịch cuối (cần file PDF, hiện chưa có)
- Phát hiện footnote content bị chèn nhầm vào body (không chỉ missing marker)
- Phát hiện đoạn văn bị chia qua page break (paragraph continuity)
- Kiểm tra tính liên tục đoạn văn toàn bộ 77 chương, không chỉ mẫu
- Language Quality Audit toàn bộ phạm vi (văn phong, từ vựng, ngữ pháp) theo tiêu chuẩn skill

---

## 3. FOOTNOTE AUDIT METHODOLOGY

### 3.1 Mục tiêu
Xác định và phân loại toàn bộ lỗi footnote trong bản dịch cuối, đảm bảo:
- Không còn nội dung footnote bị nhân đôi trong body
- Không mất footnote gốc
- Không mất marker
- Không sai liên kết giữa marker và content

### 3.2 Phương pháp đối chiếu 3 lớp (khi có PDF)
1. **Lớp 1 (PDF gốc):** Xem cấu trúc footnote thực tế trên mỗi trang — vị trí, số thứ tự, nội dung chú thích, cách đánh dấu trong trang in.
2. **Lớp 2 (extracted text):** `02_extracted_text/v1/chNN.txt` — xem footnote đã được trích xuất ra thế nào, có biệt được marker và content không.
3. **Lớp 3 (bản dịch cuối):** `04_translation/v1/chNN/v1_chNN_vi.txt` — xem footnote đã dịch thế nào, marker `[N]` có ở đâu, nội dung chú thích nằm ở đâu.

**Không được mặc định mọi nội dung nằm cuối trang đều là footnote.** Phải đối chiếu với PDF gốc để xác nhận.

### 3.3 Phân loại lỗi footnote

| Mã | Loại lỗi | Định nghĩa | Cách phát hiện |
|---|---|---|---|
| FN-01 | Footnote hợp lệ | Marker `[N]` trong body + nội dung chú thích `[N]` trong notes block, liên kết đúng, không trùng | check_footnote_markers.py PASS + đối chiếu src |
| FN-02 | Footnote bị lặp | Nội dung chú thích xuất hiện cả trong body và trong notes block | Grep nội dung notes block trong body text |
| FN-03 | Footnote content chèn vào body | Đoạn chú thích được dịch thành thân bài thay vì giữ trong khối cước chú | So sánh notes block src vs vi, tìm đoạn src chỉ là footnote nhưng xuất hiện trong body vi |
| FN-04 | Footnote marker bị mất | Có notes block `[N]` nhưng không có marker `[N]` trong body | check_footnote_markers.py (missing) |
| FN-05 | Marker orphan | Có marker `[N]` trong body nhưng không có notes block tương ứng | check_footnote_markers.py (orphan) |
| FN-06 | Marker trùng | Marker `[N]` xuất hiện >1 lần trong body | check_footnote_markers.py (duplicate) |
| FN-07 | Footnote liên kết sai | Marker `[N]` trong body trỏ tới notes block sai nội dung | Đối chiếu vị trí marker trong src và vi |
| FN-08 | Footnote không thể xác minh | Không đủ bằng chứng (thiếu PDF, thiếu src) | Đánh dấu UNVERIFIED |

### 3.4 Quy trình thực hiện

1. Chạy `check_footnote_markers.py --chapter NN` cho tất cả chương có bản dịch (ch01-ch15)
2. Đối chiếu notes block giữa `v1_chNN_src.txt` và `v1_chNN_vi.txt` — tìm nội dung chú thích src nào chưa có trong vi
3. Grep toàn bộ `v1_chNN_vi.txt` tìm các đoạn văn trùng khớp với nội dung notes block (phát hiện FN-02, FN-03)
4. Đối chiếu với PDF gốc (nếu có) để xác nhận cấu trúc footnote thực tế
5. Ghi từng lỗi vào Footnote Audit Register

### 3.5 Đầu ra
- Footnote Audit Register (theo bảng mục 8.1)
- Thống kê số lượng lỗi theo loại và chương
- Danh sách chương cần repair (ưu tiên FN-02, FN-03, FN-04, FN-06)

---

## 4. PARAGRAPH CONTINUITY AUDIT METHODOLOGY

### 4.1 Mục tiêu
Đảm bảo tất cả đoạn văn bị chia giữa hai hoặc nhiều trang trong bản gốc đã được nối đúng thành một đoạn hoàn chỉnh trong bản dịch, không mất câu, không mất cụm từ, không sai thứ tự, không ghép nhầm đoạn.

### 4.2 Phát hiện đoạn văn bị chia tại page break

**Dấu hiệu trong extracted text (`02_extracted_text/v1/chNN.txt`):**
- Đoạn kết thúc bằng trang in X, đoạn tiếp theo bắt đầu bằng trang in X+1
- Nội dung cuối trang X dứt giữa câu (không có dấu chấm hết)
- Nội dung đầu trang X+1 bắt đầu giữa câu hoặc là phần tiếp theo của câu

**Phương pháp:**
1. Lấy danh sách tất cả ranh giới trang trong extracted text (dựa trên marker `[V1CNN-PIDX] (trang Z)`)
2. Đối chiếu từng ranh giới: đoạn cuối trang Z vs đoạn đầu trang Z+1
3. Xác định câu cuối trang Z có kết thúc đầy đủ không (dấu chấm, chấm hỏi, chấm than, gạch ngang kết thúc đoạn)
4. Xác định câu đầu trang Z+1 có phải là tiếp nối hay là câu mới

### 4.3 Đối chiếu 3 lớp

| Lớp | File | Nhiệm vụ |
|---|---|---|
| PDF gốc | `The_Cambridge_History_of_the_Vietnam_War.pdf` | Xác nhận ranh giới trang in, câu cuối trang / đầu trang tiếp theo |
| Extracted text | `02_extracted_text/v1/chNN.txt` | Xem đoạn đã được tách thế nào tại page break |
| Bản dịch cuối | `04_translation/v1/chNN/v1_chNN_vi.txt` | Xem đoạn đã được nối đúng hay chưa |

### 4.4 Phân loại lỗi paragraph continuity

| Mã | Loại lỗi | Định nghĩa |
|---|---|---|
| PC-01 | Đoạn bị chia qua trang nhưng đã nối đúng | Nguồn chia 2 trang, bản dịch gộp thành 1 đoạn hoàn chỉnh |
| PC-02 | Đoạn bị tách sai | Nguồn là 1 đoạn, bản dịch tách thành 2 đoạn tại vị trí không phải page break |
| PC-03 | Đoạn bị ghép nhầm | 2 đoạn khác nhau trong nguồn được gộp thành 1 đoạn trong bản dịch |
| PC-04 | Mất câu tại ranh giới trang | Câu cuối trang X bị cắt, không xuất hiện đầy đủ trong bản dịch |
| PC-05 | Mất cụm từ tại ranh giới trang | Một phần câu bị mất khi chuyển sang trang tiếp theo |
| PC-06 | Nội dung đảo thứ tự | Đoạn A trước đoạn B trong nguồn, nhưng bản dịch đảo ngược |
| PC-07 | Đoạn độc lập bị gộp | 2 đoạn độc lập trong nguồn bị gộp thành 1 trong bản dịch |

### 4.5 Quy trình thực hiện (toàn bộ phạm vi, không lấy mẫu)

1. Lấy danh sách tất cả đoạn trong `v1_chNN_src.txt` và `v1_chNN_vi.txt` (dựa trên ID đoạn `[V1CNN-PIDX]`)
2. So sánh số lượng đoạn: src_count == vi_count? Nếu không → nghi có PC-02, PC-03, PC-07
3. Đối chiếu từng đoạn theo ID: nội dung src ↔ nội dung vi, phát hiện sự khác biệt về cấu trúc câu
4. Xác định tất cả ranh giới trang trong src, kiểm tra mỗi ranh giới xem có chia câu không
5. Đối chiếu với extracted text để xác nhận ranh giới trang thực tế
6. Đối chiếu với PDF gốc (nếu có) để xác nhận câu cuối trang / đầu trang tiếp theo
7. Ghi từng lỗi vào Paragraph Continuity Register

### 4.6 Đầu ra
- Paragraph Continuity Register (theo bảng mục 8.2)
- Danh sách ranh giới trang cần kiểm tra (tất cả ranh giới trong tất cả chương)
- Danh sách chương cần repair (ưu tiên PC-04, PC-05, PC-06)

---

## 5. LANGUAGE QUALITY AUDIT METHODOLOGY

### 5.1 Mục tiêu
Áp dụng đúng tiêu chuẩn trong skill `translation-workflow` (STYLE_GUIDE_PHAN_B.md v2.3, TRANSLATION_GRAMMAR_ENGINE.md v2.1, VLP-01) để đánh giá văn phong, từ vựng, ngữ pháp trên toàn bộ bản dịch.

### 5.2 Hệ thống phân loại lỗi

| Mã | Nhóm lỗi | Định nghĩa | Mức độ |
|---|---|---|---|
| LQ-01 | Văn phong cứng | Dịch sát cấu trúc tiếng Anh, câu cứng, khó hiểu | MAJOR |
| LQ-02 | Dịch từng từ | Dịch máy, ghép kị câu, không tự nhiên | CRITICAL |
| LQ-03 | Dùng từ sai ngữ cảnh | Từ không đúng nghĩa trong ngữ cảnh đó | MAJOR |
| LQ-04 | Thuật ngữ không nhất quán | Cùng thuật ngữ Anh được dịch khác nhau giữa các chương | MAJOR |
| LQ-05 | Lỗi ngữ pháp | Chủ ngữ, vị ngữ, đại từ, từ chỉ định, trật tự từ | MAJOR |
| LQ-06 | Câu khó hiểu | Câu quá dài, nhiều mệnh đề, thiếu liên kết | MAJOR |
| LQ-07 | Lỗi dấu câu | Dấu câu không đúng chuẩn tiếng Việt | MINOR |
| LQ-08 | Lặp từ, diễn đạt thừa | Lặp ý, từ thừa, không súc tích | MINOR |
| LQ-09 | Sai sắc thái, lệch ý tác giả | Thay đổi lập luận, hedging, quan hệ nhân quả | CRITICAL |
| LQ-10 | Phrase/domain mix | Trộn lẫn thuật ngữ miền Bắc và miền Nam | MAJOR |
| LQ-11 | VLP-01 vi phạm | Giữ ngoại ngữ có thể dịch, phiên âm thay nghĩa, cấu trúc dịch máy | CRITICAL |

### 5.3 Tiêu chí mức độ nghiêm trọng

| Mức | Định nghĩa | Hành động |
|---|---|---|
| CRITICAL | Làm sai lệch ý nghĩa, mất thông tin, hoặc không đọc được | Sửa ngay, chặn HOAN_TAT |
| MAJOR | Làm giảm rõ rệt chất lượng, khó hiểu, không nhất quán | Sửa trước khi HOAN_TAT |
| MINOR | Lỗi nhỏ, không ảnh hưởng nhiều đến hiểu biết | Sửa nếu có thời gian, không chặn HOAN_TAT |

### 5.4 Quy trình thực hiện

**Bước 1: Kiểm tra tự động (tận dụng common scripts)**
- `encoding_checker.py --chapter NN` → UTF-8, NFC, no BOM, LF
- `vnch_orthography.py --chapter NN` → 0 lỗi CRITICAL/MAJOR (chính trị→chánh trị, này→nầy, etc.)
- `document_comparator.py --chapter NN` → số đoạn src == số đoạn vi, alignment check
- `translation_validator.py --chapter NN` → quét từ Anh còn sót, thuật ngữ không nhất quán, nội dung rỗng
- `grep "tuy nhiên"` → 0 kết quả (tuy nhiên là từ miền Bắc, phải dùng "tuy vậy", "dẫu", "trái lại")
- `grep "chính trị\|chính phủ\|tài chính\|đại biểu\|đảo chính"` → 0 kết quả (phải dùng từ VNCH)

**Bước 2: Đọc hiệu đính thực sự (bắt buộc, không tự động hóa được)**
- Đọc toàn bộ `v1_chNN_vi.txt` không nhìn nguyên tác, đánh giá:
  - Câu văn có tự nhiên không?
  - Giọng văn có thống nhất không?
  - Lập luận tác giả có rõ ràng không?
- Đối chiếu ngược với nguyên tác (back-translation mẫu) cho các đoạn khó
- Kiểm tra VLP-01: không còn ngoại ngữ có thể dịch, không phiên âm thay nghĩa

**Bước 3: Đối chiếu thuật ngữ**
- Tra cứu MASTER_LEXICON.csv, POLITICAL_ECONOMIC_GLOSSARY.md
- Kiểm tra nhất quán giữa các chương
- Ghi thuật ngữ chưa có vào uncertain_terms.md

### 5.5 Phạm vi
Toàn bộ 15 chương đã có bản dịch (ch01-ch15), không chỉ lấy mẫu.

### 5.6 Đầu ra
- Language QA Register (theo bảng mục 8.3)
- Thống kê lỗi theo nhóm và mức độ
- Danh sách chương cần repair (ưu tiên CRITICAL, MAJOR)

---

## 6. BATCH-BY-BATCH EXECUTION PLAN

**Nguyên tắc thứ tự:** Xác định source of truth → Kiểm tra cấu trúc và footnote → Khôi phục tính liên tục đoạn văn → Audit ngôn ngữ → Sửa lỗi theo batch → Kiểm tra hồi quy → Final acceptance.

### Batch 0 — Xác định Source of Truth và Khai báo (trước khi sửa)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Xác định chính xác source of truth, phân biệt hai dự án trộn lẫn, quyết định cách xử lý ch01/ch02 |
| Phạm vi | Toàn bộ `translation-project/`, đặc biệt `04_translation/v1/ch01/`, `ch02/`, `00_plan/progress.json` |
| Đầu vào | Tất cả file đã khảo sát ở mục 1 |
| Các bước | 1. Xác nhận sách gốc là Cambridge History of the Vietnam War (theo manifest, MASTER_PLAN, skill) 2. Xác nhận ch01/ch02 bản dịch là Hannah Arendt (không khớp src) 3. Quyết định: dịch lại ch01/ch02 theo Cambridge History, hay giữ bản dịch Hannah Arendt và tách ra dự án riêng 4. Xây dựng lại progress.json dựa trên thực tế file hệ thống (ch01-ch15 đã có dịch, ch16-ch21 chỉ có extracted text) |
| Phương pháp kiểm tra | Đối chiếu header file dịch vs nội dung src, đối chiếu với manifest.json và MASTER_PLAN.md |
| Đầu ra | Source of truth được chốt, progress.json được xây dựng lại, quyết định xử lý ch01/ch02 |
| Điều kiện nghiệm thu | User phê duyệt source of truth và quyết định ch01/ch02 |
| Rủi ro | Nếu không chốt source of truth, mọi bước QA sau sẽ chạy trên dữ liệu oan lẫn |
| Phòng ngừa | Không sửa bất kỳ file dịch nào trước khi Batch 0 xong |
| Checkpoint | Lưu progress.json phiên bản mới (chưa sửa nội dung dịch) |

### Batch 1 — Footnote Audit (toàn bộ ch01-ch15)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Phát hiện và phân loại tất cả lỗi footnote (FN-01 đến FN-08) |
| Phạm vi | `04_translation/v1/ch01-15/v1_chNN_vi.txt` + `v1_chNN_src.txt` |
| Đầu vào | File dịch, file src, check_footnote_markers.py, bug_register.md (BUG-001, BUG-002, BUG-003, BUG-006, BUG-007, BUG-008, BUG-009) |
| Các bước | 1. Chạy `check_footnote_markers.py --chapter NN` cho ch01-ch15 2. Đối chiếu notes block src↔vi, tìm chú thích src chưa có trong vi 3. Grep nội dung notes block trong body text (phát hiện FN-02, FN-03) 4. Kiểm tra marker trùng (FN-06), marker orphan (FN-05), marker thiếu (FN-04) 5. Đối chiếu với PDF gốc nếu có sẵn (nếu không, đánh dấu UNVERIFIED) 6. Ghi từng lỗi vào Footnote Audit Register |
| Phương pháp kiểm tra | Script tự động + đọc thủ công notes block |
| Đầu ra | Footnote Audit Register đầy đủ, thống kê lỗi theo loại |
| Điều kiện nghiệm thu | Tất cả chương ch01-ch15 đã được chạy check_footnote_markers.py, tất cả lỗi đã được ghi vào register |
| Rủi ro | Không có PDF gốc → không thể xác nhận 100% cấu trúc footnote, đánh dấu UNVERIFIED |
| Phòng ngừa | Chỉ ghi nhận lỗi, KHÔNG sửa file dịch trong Batch 1 |
| Checkpoint | Lưu Footnote Audit Register |

### Batch 2 — Paragraph Continuity Audit (toàn bộ ch01-ch15)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Phát hiện tất cả lỗi liên tục đoạn văn (PC-01 đến PC-07) |
| Phạm vi | `04_translation/v1/ch01-15/` + `02_extracted_text/v1/chNN.txt` |
| Đầu vào | File dịch, file src, extracted text, document_comparator.py |
| Các bước | 1. Lấy danh sách tất cả đoạn theo ID `[V1CNN-PIDX]` trong src và vi 2. So sánh số lượng đoạn (src_count == vi_count?) 3. Đối chiếu từng đoạn theo ID, phát hiện sự khác biệt cấu trúc 4. Xác định tất cả ranh giới trang, kiểm tra chia câu 5. Đối chiếu với extracted text xác nhận ranh giới trang thực tế 6. Đối chiếu với PDF gốc nếu có (nếu không, UNVERIFIED) 7. Ghi từng lỗi vào Paragraph Continuity Register |
| Phương pháp kiểm tra | Script so sánh số đoạn + đọc thủ công từng ranh giới trang |
| Đầu ra | Paragraph Continuity Register đầy đủ |
| Điều kiện nghiệm thu | Tất cả ranh giới trang trong tất cả chương đã được kiểm tra |
| Rủi ro | Không có PDF gốc → không thể xác nhận câu cuối trang / đầu trang tiếp theo với 100% độ tin cậy |
| Phòng ngừa | Chỉ ghi nhận, KHÔNG sửa |
| Checkpoint | Lưu Paragraph Continuity Register |

### Batch 3 — Language Quality Audit (toàn bộ ch01-ch15)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Đánh giá văn phong, từ vựng, ngữ pháp theo tiêu chuẩn skill |
| Phạm vi | `04_translation/v1/ch01-15/v1_chNN_vi.txt` |
| Đầu vào | STYLE_GUIDE_PHAN_B.md, TRANSLATION_GRAMMAR_ENGINE.md, MASTER_LEXICON.csv, POLITICAL_ECONOMIC_GLOSSARY.md, common scripts |
| Các bước | 1. Chạy encoding_checker.py, vnch_orthography.py, document_comparator.py, translation_validator.py cho tất cả chương 2. Grep các từ cấm: "tuy nhiên", "chính trị", "chính phủ", "tài chính", "đại biểu", "đảo chính" 3. Đọc hiệu đính thực sự toàn bộ bản dịch (không nhìn nguyên tác) 4. Đối chiếu ngẫu nhiên 2 đoạn dài + 1 đoạn khó/chương (back-translation) 5. Kiểm tra thuật ngữ nhất quán giữa các chương 6. Kiểm tra VLP-01 (không giữ ngoại ngữ có thể dịch, không phiên âm) 7. Ghi từng lỗi vào Language QA Register |
| Phương pháp kiểm tra | Script tự động + đọc thủ công |
| Đầu ra | Language QA Register đầy đủ, thống kê lỗi theo nhóm và mức độ |
| Điều kiện nghiệm thu | Tất cả 15 chương đã được đọc và review, tất cả lỗi đã được ghi |
| Rủi ro | Đọc hiệu đính 15 chương cần thời gian, không thể rush |
| Phòng ngừa | Chỉ ghi nhận, KHÔNG sửa |
| Checkpoint | Lưu Language QA Register |

### Batch 4 — Ưu tiên sửa lỗi CRITICAL và MAJOR

| Mục | Nội dung |
|---|---|
| Mục tiêu | Sửa tất cả lỗi CRITICAL và MAJOR đã được ghi trong các register |
| Phạm vi | Chương có lỗi CRITICAL/MAJOR trong Footnote, Paragraph Continuity, Language QA registers |
| Đầu vào | Các register từ Batch 1-3, bug_register.md |
| Các bước | 1. Sắp xếp lỗi theo mức độ (CRITICAL trước, MAJOR sau) 2. Sửa lỗi footnote: khôi phục marker thiếu, xóa marker trùng, tách nội dung footnote ra khỏi body, thêm notes block thiếu 3. Sửa lỗi paragraph continuity: nối đoạn bị tách, tách đoạn bị ghép, khôi phục câu bị mất 4. Sửa lỗi ngôn ngữ: viết lại câu cứng, chuẩn hóa thuật ngữ, sửa VLP-01 vi phạm 5. Sau mỗi lần sửa, chạy lại các script kiểm tra liên quan |
| Phương pháp kiểm tra | Chạy lại check_footnote_markers.py, document_comparator.py, encoding_checker.py, vnch_orthography.py sau mỗi sửa |
| Đầu ra | Các file vi.txt đã được sửa, register cập nhật status = FIXED |
| Điều kiện nghiệm thu | Không còn lỗi CRITICAL/MAJOR chưa xử lý trong các register |
| Rủi ro | Sửa sai có thể gây ra lỗi mới → cần kiểm tra hồi quy |
| Phòng ngừa | Backup file trước khi sửa, chạy lại toàn bộ kiểm tra sau mỗi sửa |
| Checkpoint | Cập nhật progress.json sau mỗi chương sửa xong |

### Batch 5 — Kiểm tra hồi quy (Regression)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Đảm bảo việc sửa lỗi không gây ra lỗi mới |
| Phạm vi | Tất cả chương đã sửa trong Batch 4 |
| Đầu vào | Các register, các script kiểm tra |
| Các bước | 1. Chạy lại toàn bộ kiểm tra tự động (encoding, orthography, document_comparator, translation_validator, check_footnote_markers) 2. Chạy `audit_chapter.py --chapter NN` cho từng chương đã sửa 3. Chạy `audit_docx_format.py --chapter NN` nếu có DOCX 4. Đọc lại các đoạn đã sửa để đảm bảo không làm mất nghĩa |
| Phương pháp kiểm tra | Script tự động + đọc thủ công các đoạn đã sửa |
| Đầu ra | Kết quả kiểm tra hồi quy, tất cả PASS |
| Điều kiện nghiệm thu | Tất cả script kiểm tra PASS, audit_chapter.py PASS cho tất cả chương đã sửa |
| Rủi ro | Một số lỗi có thể chỉ phát hiện được khi đọc toàn bộ, không chỉ đoạn đã sửa |
| Phòng ngừa | Đọc lại toàn bộ chương sau khi sửa, không chỉ đoạn bị lỗi |
| Checkpoint | Cập nhật progress.json qa_status = passed cho từng chương |

### Batch 6 — Final Acceptance

| Mục | Nội dung |
|---|---|
| Mục tiêu | Nghiệm thu cuối cùng, đánh dấu chương HOAN_TAT |
| Phạm vi | Tất cả 15 chương (ch01-ch15) |
| Đầu vào | Tất cả register, kết quả kiểm tra hồi quy |
| Các bước | 1. Xem lại toàn bộ Footnote Audit Register: không còn FN-02, FN-03, FN-04, FN-05, FN-06, FN-07 chưa xử lý 2. Xem lại toàn bộ Paragraph Continuity Register: không còn PC-04, PC-05, PC-06 chưa xử lý 3. Xem lại toàn bộ Language QA Register: không còn lỗi CRITICAL/MAJOR 4. Cập nhật progress.json: tất cả chương status = HOAN_TAT, qa_status = passed 5. Tổng hợp báo cáo cuối |
| Phương pháp kiểm tra | Review tất cả register, xác nhận status |
| Đầu ra | Báo cáo nghiệm thu cuối, progress.json cập nhật |
| Điều kiện nghiệm thu | Tất cả lỗi CRITICAL/MAJOR đã FIXED, tất cả chương HOAN_TAT |
| Rủi ro | Một số lỗi có thể bị bỏ sót nếu không đọc kỹ |
| Phòng ngừa | Cross-check giữa các register, đảm bảo không có lỗi nào bị bỏ qua |
| Checkpoint | progress.json final version |

---

## 7. CHECKPOINT & RECOVERY STRATEGY

### 7.1 Checkpoint cần lưu

| Checkpoint | File | Nội dung | Khi lưu |
|---|---|---|---|
| CP-0 | `00_plan/progress.json` (phiên bản mới) | Source of truth chốt, tiến độ thực tế ch01-ch15 | Sau Batch 0 |
| CP-1 | `99_scripts/footnote_audit_register.json` | Footnote Audit Register | Sau Batch 1 |
| CP-2 | `99_scripts/paragraph_continuity_register.json` | Paragraph Continuity Register | Sau Batch 2 |
| CP-3 | `99_scripts/language_qa_register.json` | Language QA Register | Sau Batch 3 |
| CP-4 | `00_plan/progress.json` (cập nhật) | Trạng thái sau mỗi chương sửa xong | Sau mỗi chương trong Batch 4 |
| CP-5 | `00_plan/progress.json` (final) | Tất cả chương HOAN_TAT, qa_status = passed | Sau Batch 6 |

### 7.2 Phương án khôi phục

| Tình huống | Phương án khôi復 |
|---|---|
| Sửa sai file vi.txt, gây lỗi mới | Sao lưu file trước khi sửa (copy sang `99_scripts/backup/` kèm timestamp). Nếu lỗi, khôi phục từ backup. |
| progress.json bị hỏng | Khôi phục từ CP-0 (phiên bản sau Batch 0) hoặc git commit trước đó. |
| Register bị mất | Tái chạy Batch 1-3 (script có thể tái tạo từ file dịch). |
| Xác nhận sau này là source of truth sai | Tái chạy Batch 0, điều chỉnh progress.json và registers. |

**Quy tắc:** Luôn backup file `v1_chNN_vi.txt` trước khi sửa, lưu tại `99_scripts/backup/v1_chNN_vi.txt.<timestamp>`.

---

## 8. QA REGISTERS AND REPORTING STRUCTURE

Tất cả register lưu dưới dạng JSON UTF-8 tại `99_scripts/` (theo quy tắc skill section 7B).

### 8.1 Footnote Audit Register

| Field | Ý nghĩa |
|---|---|
| chapter | Chương (V1-C01 … V1-C15) |
| page | Trang in (từ marker trong file) |
| footnote_id | Mã chú thích [N] |
| issue_type | FN-01 … FN-08 |
| source_reference | Vị trí trong src (dòng, ID đoạn) |
| translation_reference | Vị trí trong bản dịch (dòng, ID đoạn) |
| severity | CRITICAL / MAJOR / MINOR |
| status | UNVERIFIED / VERIFIED / FIXED / NOT_APPLICABLE |
| verification | Bằng chứng xác minh (script output, trích dẫn PDF, etc.) |

### 8.2 Paragraph Continuity Register

| Field | Ý nghĩa |
|---|---|
| chapter | Chương |
| start_page | Trang bắt đầu đoạn |
| end_page | Trang kết thúc đoạn |
| source_paragraph | ID đoạn trong src `[V1CNN-PIDX]` |
| extracted_segments | Các phần trong extracted text tại ranh giới trang |
| translated_segments | Các phần trong bản dịch tại ranh giới trang |
| continuity_status | PC-01 … PC-07 |
| severity | CRITICAL / MAJOR / MINOR |
| status | UNVERIFIED / VERIFIED / FIXED / NOT_APPLICABLE |
| repair_status | Chưa xử lý / Đã sửa / Đã kiểm tra lại |

### 8.3 Language QA Register

| Field | Ý nghĩa |
|---|---|
| chapter | Chương |
| page | Trang in |
| paragraph_id | ID đoạn `[V1CNN-PIDX]` |
| issue_category | LQ-01 … LQ-11 |
| severity | CRITICAL / MAJOR / MINOR |
| original_context | Ngữ cảnh nguyên tác (trích dẫn src) |
| current_translation | Bản dịch hiện tại (trích dẫn vi) |
| proposed_resolution | Hướng xử lý đề xuất |
| status | UNVERIFIED / VERIFIED / FIXED / NOT_APPLICABLE |

### 8.4 Evidence Status (áp dụng cho tất cả register)

| Giá trị | Ý nghĩa |
|---|---|
| VERIFIED | Đã đối chiếu và xác nhận |
| FIXED | Đã sửa và kiểm tra lại |
| UNVERIFIED | Chưa đủ bằng chứng (ví dụ: thiếu PDF gốc) |
| CONTEXT_GAP | Thiếu ngữ cảnh hoặc tài liệu |
| NOT_APPLICABLE | Không áp dụng |

**Không được thiết kế tiêu chuẩn PASS cho phép bỏ qua lỗi nghiêm trọng chưa xử lý.** Tất cả CRITICAL và MAJOR phải có status = FIXED trước khi chương được đánh dấu HOAN_TAT.

---

## 9. ACCEPTANCE CRITERIA

### 9.1 Footnote
- [ ] Không còn nội dung footnote bị nhân đôi trong body (FN-02, FN-03 = 0)
- [ ] Không mất footnote gốc (mọi notes block trong src có tương ứng trong vi)
- [ ] Không mất marker (mọi notes block có marker trong body)
- [ ] Không sai liên kết giữa marker và content (FN-07 = 0)
- [ ] Không có marker trùng (FN-06 = 0)
- [ ] `check_footnote_markers.py --chapter NN` PASS cho tất cả chương

### 9.2 Paragraph Continuity
- [ ] Tất cả ranh giới trang đã được kiểm tra (tất cả chương, không chỉ mẫu)
- [ ] Đoạn tiếp nối được nối đúng (PC-01)
- [ ] Đoạn độc lập không bị ghép nhầm (PC-03, PC-07 = 0)
- [ ] Không mất câu, không mất cụm từ (PC-04, PC-05 = 0)
- [ ] Không đảo nội dung (PC-06 = 0)
- [ ] `document_comparator.py` số đoạn src == số đoạn vi cho tất cả chương

### 9.3 Language Quality
- [ ] Toàn bộ 15 chương đã được đọc và review
- [ ] Không còn lỗi CRITICAL chưa xử lý
- [ ] Không còn lỗi MAJOR chưa xử lý
- [ ] Thuật ngữ nhất quán giữa các chương (tra cứu MASTER_LEXICON, POLITICAL_ECONOMIC_GLOSSARY)
- [ ] Văn phong tự nhiên, dễ hiểu, dễ thấm (đọc độc lập hiểu được ý chính)
- [ ] Không làm sai lệch giọng văn và lập luận nguyên tác
- [ ] VLP-01: không giữ ngoại ngữ có thể dịch, không phiên âm thay nghĩa
- [ ] Encoding: UTF-8, NFC, no BOM, LF (0 lỗi)
- [ ] Orthography: 0 lỗi CRITICAL/MAJOR (chính trị→chánh trị, này→nầy, etc.)

### 9.4 Evidence Status
- [ ] Mỗi vấn đề trong các register đã được đánh dấu status
- [ ] Không có lỗi CRITICAL/MAJOR với status = UNVERIFIED (trừ những thứ thực sự không thể xác minh do thiếu PDF, phải đánh dấu CONTEXT_GAP và báo cáo rõ ràng)

---

## 10. RISKS, DEPENDENCIES AND UNVERIFIED AREAS

### 10.1 Risks

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Hai dự án trộn lẫn (Cambridge History vs Hannah Arendt) | CRITICAL | Batch 0 phải chốt source of truth trước khi làm gì khác |
| Không có file PDF gốc (`01_source_pdf/` trống) | HIGH | Không thể đối chiếu PDF trực tiếp, đánh dấu UNVERIFIED/CONTEXT_GAP cho các vấn đề cần PDF |
| progress.json cũ, không phản hồi thực tế | HIGH | Xây dựng lại progress.json từ thực tế file hệ thống trong Batch 0 |
| ch01/ch02 bản dịch là Hannah Arendt, không khớp src | CRITICAL | Cần user quyết định: dịch lại hay tách ra dự án riêng |
| Sửa lỗi có thể gây ra lỗi mới | MEDIUM | Backup trước khi sửa, chạy lại toàn bộ kiểm tra sau mỗi chương |
| Đọc hiệu đính 15 chương cần thời gian | MEDIUM | Không rush, đọc từng chương một |

### 10.2 Dependencies

| Phụ thuộc | Trạng thái | Ghi chú |
|---|---|---|
| File PDF gốc (`The_Cambridge_History_of_the_Vietnam_War.pdf`) | ❌ Không có | Cần để đối chiếu footnote và paragraph continuity với 100% độ tin cậy |
| check_footnote_markers.py | ✅ Có | Trong `translation-project/99_scripts/` |
| document_comparator.py | ✅ Có | Trong `.kilo/scripts/common/` |
| quality_gate.py | ✅ Có | Trong `.kilo/scripts/common/` |
| vnch_orthography.py | ✅ Có | Trong `.kilo/scripts/common/` |
| encoding_checker.py | ✅ Có | Trong `.kilo/scripts/common/` |
| STYLE_GUIDE_PHAN_B.md | ✅ Có | Trong `07_style_guide/` |
| TRANSLATION_GRAMMAR_ENGINE.md | ✅ Có | Trong `07_style_guide/` |
| MASTER_LEXICON.csv | ✅ Có | Trong `08_southern_vietnamese_library/` |
| bug_register.md | ✅ Có | Trong `00_plan/` (9 bug đã biết) |

### 10.3 Unverified Areas (cần user xác nhận)

1. **Source of truth:** Xác nhận sách gốc là Cambridge History of the Vietnam War (không phải Hannah Arendt). progress.json hiện ghi Hannah Arendt — cần điều chỉnh.
2. **Xử lý ch01/ch02:** Bản dịch hiện là nội dung Hannah Arendt, không khớp src Cambridge History. User cần quyết định: dịch lại theo Cambridge History, hay giữ và tách ra dự án riêng.
3. **File PDF:** `01_source_pdf/` trống. User cần cung cấp PDF hoặc xác nhận sẽ không dùng PDF trong giai đoạn này (đánh dấu UNVERIFIED/CONTEXT_GAP cho các vấn đề cần PDF).
4. **progress.json:** Cần xây dựng lại từ thực tế (ch01-ch15 đã có dịch, ch16-ch21 chỉ có extracted text).
5. **DOCX cho ch01-ch02:** Nếu ch01/ch02 được dịch lại, DOCX cũ trong `09_docx/` cần rebuild.

---

## 11. QUYẾT ĐỊNH CẦN USER PHÊ DUYỆT

| # | Vấn đề | Lựa chọn đề xuất | Ảnh hưởng |
|---|---|---|---|
| 1 | **Source of truth** | Chốt là *The Cambridge History of the Vietnam War* (theo manifest, MASTER_PLAN, skill, extracted_text, src files) | Xác định toàn bộ kế hoạch QA chạy trên quyển nào |
| 2 | **Xử lý ch01/ch02** | Dịch lại theo Cambridge History Ch1/Ch2 (bản dịch hiện tại là Hannah Arendt, không khớp src) | Ch01, ch02 cần dịch lại hoàn toàn, DOCX cần rebuild |
| 3 | **File PDF** | Không có PDF trong giai đoạn này → đánh dấu UNVERIFIED/CONTEXT_GAP cho các vấn đề cần PDF | Không thể đối chiếu PDF trực tiếp, chỉ đối chiếu extracted text ↔ bản dịch |
| 4 | **progress.json** | Xây dựng lại từ thực tế file hệ thống (ch01-ch15 đã có dịch) | Cập nhật checkpoint cho toàn bộ kế hoạch |

---

## 12. TỔNG KẾT PHÁT HIỆN THỰC TẾ

| Vấn đề | Đã xác minh | Chưa xác minh |
|---|---|---|
| Hai dự án trộn lẫn (Cambridge History vs Hannah Arendt) | ✅ (header file dịch ch01/ch02 vs src) | — |
| ch01/ch02 bản dịch là Hannah Arendt, không khớp src | ✅ (đọc file) | — |
| progress.json cũ (chỉ 2 chương, ghi Hannah Arendt) | ✅ (đọc file) | — |
| `01_source_pdf/` trống | ✅ (kiểm tra thư mục) | — |
| 15 chương đã có bản dịch (ch01-ch15) | ✅ (kiểm tra thư mục) | — |
| 15 chương đã có DOCX (V1-C01 … V1-C15) | ✅ (kiểm tra thư mục) | — |
| Ch11 thiếu 21 footnotes (BUG-008) | ✅ (bug_register.md) | — |
| Ch12: 42 markers đã bị mất, đã khôi phục thủ công | ✅ (bug_register.md BUG-001) | — |
| Ch12: duplicate marker [20] (BUG-009) | ✅ (bug_register.md) | — |
| Footnote content bị chèn vào body (FN-02, FN-03) | Chưa quét hệ thống | Cần chạy Batch 1 |
| Paragraph continuity lỗi (PC-01 … PC-07) | Chưa quét hệ thống | Cần chạy Batch 2 |
| Lỗi ngôn ngữ toàn bộ 15 chương | Chưa quét hệ thống | Cần chạy Batch 3 |

**File bản dịch cuối sẽ được xử lý:** `04_translation/v1/ch01/v1_ch01_vi.txt` … `ch15/v1_ch15_vi.txt` (15 file), với ưu tiên ch01, ch02 (cần xác định source of truth trước), rồi ch11 (BUG-008 CRITICAL), rồi các chương còn lại.

**Thứ tự thực hiện:** Batch 0 → Batch 1 → Batch 2 → Batch 3 → Batch 4 → Batch 5 → Batch 6.

**KHÔNG được tự động chuyển sang Execution Mode.** Kế hoạch này cần user phê duyệt trước khi bắt đầu thực thi.
