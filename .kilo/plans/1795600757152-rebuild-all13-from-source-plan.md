# PLAN: XÂY DỰNG LẠI TOÀN BỘ 13 CHƯƠNG — THE ORIGINS OF TOTALITARIANISM (VNCH)

**Dự án:** The Origins of Totalitarianism — Hannah Arendt (dịch VNCH trước 1975)  
**Root:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\`  
**File kế hoạch:** `.kilo/plans/1795600757152-rebuild-all13-from-source-plan.md`  
**Trạng thái:** Sẵn sàng triển khai (implementation-ready)

---

## 0. RÀNG BUỘC QUYỀN HẠN (Plan Mode)

Tôi đang chạy ở Plan Mode. Chỉ được tạo/sửa file kế hoạch. Không được:
- Sửa file nguồn (PDF, TXT, DOCX)
- Chạy lệnh mutating (python script, git, etc.)
- Dịch bản dịch trực tiếp

Sau khi `plan_exit`, một agent có quyền triển khai sẽ thực hiện các task dưới đây.

---

## 1. TỔNG QUAN CÔNG VIỆC

Xây dựng lại toàn bộ 13 chương từ nguyên bản, theo luồng:

**PDF gốc → trích xuất/OCR → tái lập cấu trúc → Source TXT → dịch mới → hiệu đính → đối chiếu → QA → DOCX**

Không dùng bản dịch cũ làm nguồn dịch. Chỉ dùng làm tài liệu tham khảo khi truy nguyên lỗi.

### Phạm vi
- 6 phần mở đầu (front_matter, preface x4, part_one_intro): trang 1–47
- 13 chương chính (ch01–ch13): trang 48–574
- Tổng cộng 19 thành phần, mỗi thành phần xử lý tuần tự

---

## 2. NGUỒN TÀI LIỆU VÀ CÔNG CỤ HIỆN CÓ

| Vị trí | Mô tả |
|--------|-------|
| `books/Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf` | PDF gốc (nguyên bản) |
| `02_extracted_text/v1/{name}.txt` | Văn bản trích xuất từ PDF theo trang (các script đã có) |
| `02_extracted_text/v2/{name}_src.txt` | Văn bản đã tái lập cấu trúc (các script đã có) |
| `04_translation/v2/chNN/v1_chNN_vi.txt` | Bản dịch v2 hiện tại (CHỈ dùng làm tham khảo, KHÔNG làm nguồn) |
| `99_scripts/extract_chapters.py` | Trích xuất PDF → TXT theo trang (PyMuPDF/fitz) |
| `99_scripts/ocr_reconstruct.py` | Tái lập đoạn văn, gộp đoạn ngắt trang, gán mã `[V1CNN-PNNN]` |
| `99_scripts/build_chapter_docx_v2.py` + `docx_builder_v2/` | Xây dựng DOCX chương với Word Styles |
| `99_scripts/build_master_docx_v2.py` | Xây dựng DOCX tổng hợp 13 chương + phần mở đầu |
| `99_scripts/debug_align.py` | Kiểm tra ánh xạ source–translation 1:1 |
| `00_plan/progress.json` | Theo dõi trạng thái từng chương |
| `dashboard.html` | GOAL Dashboard (cần cập nhật trạng thái thực tế) |

---

## 3. CÁC QUY TRÌNH CHUẨN (THEO 7 YÊU CẦU CỦA NGƯỜI DÙNG)

### Quy trình A: Trích xuất và tái lập cấu trúc (mỗi thành phần)

1. Chạy `extract_chapters.py` để trích xuất PDF → `02_extracted_text/v1/{name}.txt` theo trang
2. Chạy `ocr_reconstruct.py` để:
   - Tách đoạn văn, gộp đoạn bị ngắt qua ranh giới trang (dấu `-` kết thúc dòng hoặc đoạn bắt đầu bằng chữ thường)
   - Phân biệt body text, footnote (dấu ngõ trên đầu dòng)
   - Gán mã đoạn `[V1CNN-PNNN] (trang N)`
   - Xuất `02_extracted_text/v2/{name}_src.txt`
3. Kiểm tra: mỗi trang có đoạn được đánh dấu, không bỏ sót nội dung

### Quy trình B: Dịch mới (mỗi chương)

1. Đọc Source TXT (`v2/{name}_src.txt`) đoạn demi đoạn
2. Dịch sang tiếng Việt theo STYLE_GUIDE_PHAN_B.md và ARENDT_TERMINOLOGY.md
3. Xuất Translation TXT (`04_translation/v2/chNN/v1_chNN_vi.txt`) với cùng số đoạn, cùng mã `[V1CNN-PNNN]`
4. Ánh xạ 1:1: Source P001 ↔ Translation P001, Source P002 ↔ Translation P002, ...
5. **Không** tự ý gộp/tách đoạn
6. **Không** để đoạn trống giả
7. **Không** để đoạn ghép từ nhiều trang không đúng ranh giới
8. Dịch toàn bộ ngoại ngữ (Anh, Pháp, Đức, Latin) trong nội dung
9. Giữ tên riêng, địa danh, nhan đề bằng nguyên ngữ khi cần; kèm nghĩa tiếng Việt
10. **Không** xóa nguyên văn ngoại ngữ bằng bộ lọc
11. **Không** tự suy diễn, thêm ý, lược bỏ, thay đổi lập luận của Arendt

### Quy trình C: Hiệu đính và chuẩn hóa (mỗi chương)

1. Sửa lỗi ngữ pháp, câu tối nghĩa, lặp từ, sai dấu câu, dịch sát chữ
2. Chuẩn hóa văn phong miền Nam Việt Nam trước 1975 (tránh từ miền Bắc)
3. Thống nhất thuật ngữ triết học, chính trị, lịch sử, xã hội học
4. Giữ nguyên sắc thái và văn phong học thuật của tác giả

### Quy trình D: Đối chiếu (mỗi chương)

1. Source TXT và Translation TXT phải có cùng số đoạn
2. Mỗi đoạn dich phải tương ứng đúng nội dung đoạn source
3. Không thiếu, không thừa, không sai nghĩa, không sai ngữ cảnh

### Quy trình E: Xây dựng DOCX (mỗi chương + toàn bộ)

1. Chạy `build_chapter_docx_v2.py` cho từng chương
2. Heading 1/2/3 đúng cấp
3. Body, quotation, footnote, bibliography có Word Styles riêng
4. Không lặp tiêu đề chương ở đầu nội dung
5. Không để tiêu đề chạy đầu trang lọt vào body
6. Chú thích đúng vị trí và liên kết
7. Hỗ trợ Navigation Pane và mục lục tự động
8. Chạy `build_master_docx_v2.py` để xây dựng DOCX tổng hợp

### Quy trình F: Kiểm định (mỗi chương + toàn bộ 13 chương)

10 mục kiểm tra bắt buộc:
1. Source–Translation paragraph mapping 1:1
2. Nội dung dịch thiếu, thừa, sai nghĩa, sai ngữ cảnh
3. Ngoại ngữ còn sót trong thân bài
4. Đoạn trống, đoạn trùng, đoạn ghép sai
5. Tiêu đề chương và subheading bị lặp
6. Nối đoạn qua trang
7. Chú thích và trích dẫn
8. Thuật ngữ và văn phong
9. Cấu trúc DOCX và Word Styles
10. Tính toàn vẹn của nội dung so với nguyên bản

Mỗi lỗi phải có: vị trí, nguyên nhân, cách sửa, kết quả kiểm chứng.

---

## 4. DANH SÁCH TASK (THEO THỰ TỰ)

### Giai đoạn 1: Chuẩn bị và trích xuất

| Task | Mô tả | Input | Output |
|------|-------|-------|--------|
| T1.1 | Kiểm tra PDF gốc tồn tại và có thể mở | `books/*.pdf` | Xác nhận PDF hợp lệ |
| T1.2 | Chạy `extract_chapters.py` cho tất cả 19 thành phần | PDF gốc | `02_extracted_text/v1/{name}.txt` (19 file) |
| T1.3 | Chạy `ocr_reconstruct.py` cho tất cả 19 thành phần | `v1/*.txt` | `v2/{name}_src.txt` (19 file) |
| T1.4 | Kiểm tra số đoạn mỗi thành phần trong v2 | `v2/*_src.txt` | Báo cáo số đoạn mỗi thành phần |

### Giai đoạn 2: Dịch mới (13 chương chính, tuần tự)

| Task | Mô tả | Input | Output |
|------|-------|-------|--------|
| T2.1 | Dịch ch01 (trang 48–55) | `v2/ch01_src.txt` | `04_translation/v2/ch01/v1_ch01_vi.txt` |
| T2.2 | Dịch ch02 (trang 56–98) | `v2/ch02_src.txt` | `04_translation/v2/ch02/v1_ch02_vi.txt` |
| T2.3 | Dịch ch03 (trang 99–133) | `v2/ch03_src.txt` | `04_translation/v2/ch03/v1_ch03_vi.txt` |
| T2.4 | Dịch ch04 (trang 134–167) | `v2/ch04_src.txt` | `04_translation/v2/ch04/v1_ch04_vi.txt` |
| T2.5 | Dịch ch05 (trang 168–202) | `v2/ch05_src.txt` | `04_translation/v2/ch05/v1_ch05_vi.txt` |
| T2.6 | Dịch ch06 (trang 203–229) | `v2/ch06_src.txt` | `04_translation/v2/ch06/v1_ch06_vi.txt` |
| T2.7 | Dịch ch07 (trang 230–266) | `v2/ch07_src.txt` | `04_translation/v2/ch07/v1_ch07_vi.txt` |
| T2.8 | Dịch ch08 (trang 267–311) | `v2/ch08_src.txt` | `04_translation/v2/ch08/v1_ch08_vi.txt` |
| T2.9 | Dịch ch09 (trang 312–349) | `v2/ch09_src.txt` | `04_translation/v2/ch09/v1_ch09_vi.txt` |
| T2.10 | Dịch ch10 (trang 350–387) | `v2/ch10_src.txt` | `04_translation/v2/ch10/v1_ch10_vi.txt` |
| T2.11 | Dịch ch11 (trang 388–433) | `v2/ch11_src.txt` | `04_translation/v2/ch11/v1_ch11_vi.txt` |
| T2.12 | Dịch ch12 (trang 434–504) | `v2/ch12_src.txt` | `04_translation/v2/ch12/v1_ch12_vi.txt` |
| T2.13 | Dịch ch13 (trang 505–574) | `v2/ch13_src.txt` | `04_translation/v2/ch13/v1_ch13_vi.txt` |

### Giai đoạn 3: Phần mở đầu (6 thành phần)

| Task | Mô tả | Input | Output |
|------|-------|-------|--------|
| T3.1 | Dịch front_matter (trang 1–7) | `v2/front_matter_src.txt` | `04_translation/v2/front_matter/...` |
| T3.2 | Dịch preface_first_edition (trang 8–10) | `v2/preface_first_edition_src.txt` | ... |
| T3.3 | Dịch preface_part_one (trang 11–16) | `v2/preface_part_one_src.txt` | ... |
| T3.4 | Dịch preface_part_two (trang 17–22) | `v2/preface_part_two_src.txt` | ... |
| T3.5 | Dịch preface_part_three (trang 23–41) | `v2/preface_part_three_src.txt` | ... |
| T3.6 | Dịch part_one_intro (trang 42–47) | `v2/part_one_intro_src.txt` | ... |

### Giai đoạn 4: Hiệu đính và chuẩn hóa (tất cả 19 thành phần)

| Task | Mô tả |
|------|-------|
| T4.1 | Hiệu đính ch01–ch13 (ngữ pháp, câu tối nghĩa, thuật ngữ, văn phong VNCH) |
| T4.2 | Hiệu đính 6 thành phần mở đầu |
| T4.3 | Chuẩn hóa UTF-8, NFC, no BOM, LF cho tất cả file TXT |

### Giai đoạn 5: Đối chiếu (tất cả 19 thành phần)

| Task | Mô tả |
|------|-------|
| T5.1 | Kiểm tra ánh xạ 1:1 source↔translation cho mỗi chương |
| T5.2 | Kiểm tra không thiếu, không thừa đoạn |
| T5.3 | Kiểm tra nội dung dịch khớp source (không sai nghĩa, sai ngữ cảnh) |

### Giai đoạn 6: Xây dựng DOCX

| Task | Mô tả |
|------|-------|
| T6.1 | Xây dựng DOCX từng chương (ch01–ch13) với Word Styles |
| T6.2 | Xây dựng DOCX phần mở đầu (6 thành phần) |
| T6.3 | Xây dựng DOCX tổng hợp (master) với TOC tự động, Navigation Pane |
| T6.4 | Kiểm tra cấu trúc DOCX: Heading 1/2/3, Styles, footnote liên kết |

### Giai đoạn 7: Kiểm định QA (tất cả 19 thành phần + tổng hợp)

| Task | Mô tả |
|------|-------|
| T7.1 | Chạy `debug_align.py` cho tất cả 13 chương (src=vi alignment) |
| T7.2 | Kiểm tra 10 mục QA cho mỗi chương |
| T7.3 | Kiểm tra 10 mục QA cho toàn bộ 13 chương |
| T7.4 | Ghi nhận mọi lỗi: vị trí, nguyên nhân, cách sửa, kết quả kiểm chứng |
| T7.5 | Cập nhật `progress.json` và `dashboard.html` với trạng thái thực tế |

---

## 5. QUY TẮC THỰC THI (THEO YÊU CẦU)

1. Đọc lại workflow/skill và toàn bộ quy định dự án trước khi thực hiện
2. Làm trực tiếp, không tạo kế hoạch mới thay cho công việc
3. Chạy lần lượt 13 chương, có checkpoint và khả năng tiếp tục khi gián đoạn
4. Không ghi đè nguyên bản hoặc xóa dữ liệu nguồn
5. UTF-8 bắt buộc cho toàn bộ file văn bản
6. Mọi script và file text mới phải lưu trong `99_scripts`
7. Cập nhật progress và GOAL Dashboard bằng trạng thái thực tế
8. Chỉ đánh dấu PASS khi đã đối chiếu và chạy kiểm tra thành công

---

## 6. TIÊU CHÍ KẾT QUẢ CUỐI CÙNG (ĐỦ ĐIỀU KIỆN ĐỂ ĐÁNH DẤU HOAN_TAT)

- [ ] Tất cả 13 chương được dịch lại đầy đủ từ nguyên bản
- [ ] Source TXT và Translation TXT có cùng số đoạn, ánh xạ 1:1
- [ ] Không còn đoạn ngoại ngữ chưa dịch trong thân bài (ngoại trừ tên riêng, địa danh, nhan đề cần giữ nguyên ngữ)
- [ ] Không còn đoạn trống, đoạn trùng, đoạn ghép sai
- [ ] Không còn tiêu đề chương lặp lại ở đầu nội dung
- [ ] Không còn tiêu đề chạy đầu trang lọt vào body
- [ ] Văn phong miền Nam Việt Nam trước 1975, thống nhất thuật ngữ
- [ ] DOCX từng chương và DOCX tổng hợp được xây dựng với Word Styles đúng cấp
- [ ] Hỗ trợ Navigation Pane và mục lục tự động
- [ ] Tất cả 10 mục QAPASS cho từng chương và toàn bộ
- [ ] Mọi lỗi đã được ghi nhận: vị trí, nguyên nhân, cách sửa, kết quả kiểm chứng

---

## 7. FILE CẦN TẠO / CẬP NHẬT (TRONG 99_SCSRIPTS HOẶC PLAN)

| File | Mục đích |
|------|----------|
| `99_scripts/qa_checklist.py` | Script chạy 10 mục QA cho một chương hoặc toàn bộ |
| `00_plan/progress.json` | Cập nhật trạng thái từng chương (dịch/xong/QA/PASS) |
| `dashboard.html` | Cập nhật GOAL Dashboard với trạng thái thực tế |

---

## 8. CÂU HỎI MỞ (CẦN XÁC NHẬN TRƯỚC KHI TRIỂN KHAI)

Nếu bạn muốn tôi điều chỉnh kế hoạch, hãy trả lời:

1. **Bibliography ch13 (P016–P061):** Giữ nguyên ngữ tiếng Anh cho các mục錄 sách theo quy ước học thuật, hay dịch sang tiếng Việt? [Khuyên: Giữ nguyên ngữ]
2. **Đoạn trống (ch02 P001–P026, ch10 P007–P008):** Nếu bản PDF gốc không có nội dung ở những trang này, đánh dấu `[TRONG]` + UNVERIFIED, hay để trống? [Khuyên: Đánh dấu UNVERIFIED]
3. **Chú thích không thể khôi phục (ch12, 39 mục):** Giữ đánh dấu `[CHƯA KHÔ PHỤC]`, hay loại bỏ? [Khuyên: Giữ đánh dấu]
4. **Phần mở đầu (6 thành phần):** Cũng dịch hoàn toàn theo quy trình rebuild, hay chỉ dịch 13 chương chính? [Khuyên: Dịch đầy đủ 19 thành phần]

Nếu bạn xác nhận các mặc định trên, kế hoạch đã sẵn sàng triển khai. Gọi `plan_exit` để chuyển sang giai đoạn thực thi.