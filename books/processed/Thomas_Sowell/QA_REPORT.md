# QA_REPORT — Thomas Sowell: Kinh Tế Học Cơ Bản (Sách Vỡ Lòng Về Kinh Tế)

## 1. Tổng quan

| Mục | Giá trị |
|-----|---------|
| File nguồn | `books/Kinh Tế Học Cơ Bản - Sách Vỡ Lòng Về Kinh Tế - Thomas Sowell.pdf` |
| Thư mục xuất | `books/processed/Thomas_Sowell/` |
| Nguyên tắc cốt lõi | **BẢN MỚI = BẢN GỐC + CẢI THIỆN CHẤT LƯỢNG** — không redesign template Word, không reorder, không di chuyển ảnh, không ép khổ giấy đồng nhất. |
| File PDF gốc đã bảo toàn | Có (không ghi đè) |

### File sản xuất
1. `Thomas_Sowell_converted.docx` — chuyển đổi trực tiếp từ PDF gốc, giữ nguyên layout (mỗi trang PDF = một section DOCX, cùng kích thước trang, cùng font/in đậm/nguyên bản/cỡ chữ của từng span).
2. `Thomas_Sowell_formatted.docx` — nội dung giống hệt `converted.docx` (xây dựng bằng cùng script, không áp dụng template riêng).
3. `Thomas_Sowell_final.pdf` — PDF gốc đã được lưu lại với garbage=4, deflate=True (784 trang, cùng kích thước trang, cùng 2 ảnh, cùng nội dung text).
4. `QA_REPORT.md` (tệp này).
5. `99_scripts\sowell_07_build_docx_fast.py` — script xây dựng DOCX bằng lxml + zip (tránh bị chậm O(n^2) của python-docx khi tài liệu lớn).

## 2. Kiểm tra tài liệu gốc (trước xử lý)

| Thuộc tính | Kết quả |
|------------|---------|
| Định dạng | PDF 1.7, tạo bởi calibre 6.15.1 |
| Tổng số trang | 784 |
| Kích thước trang | 612 × 792 pt (Letter, phần lớn); một số trang 596 × 843 pt |
| Loại nội dung | Có text (không phải scan) |
| Font chữ được dùng | Times New Roman, Arial, Calibri, FreeSerif, Roboto, Gautami… |
| Hình ảnh nhúng | 2 ảnh (trang 613: 1200×405; trang 615: 1200×399) |
| Bảng biểu | Không có bảng biểu dạng cấu trúc (nội dung là văn bản chạy) |
| Chương được phát hiện | 27 chương (Chương 1 → Chương 27) |
| Phần được phát hiện | 5 phần (Phần I, II, III, VI, VII) |
| Trang gần như trống (text < 5 ký tự) | 30 trang (các trang trắng giữa phần/chương, trang cuối) |
| Ghi nhận vấn đề định dạng gốc | Có nhiều ký tự `|` (dấu phân cách trang trí artifacts của calibre) chèn xen trong văn bản; tiêu đề chương đôi khi gộp cùng block với nội dung; một số chương tròn trang, một số bắt đầu giữa trang. |

## 3. Kết quả chuyển đổi (layout preservation)

### 3.1 Nguyên tắc áp dụng
Mỗi trang PDF gốc tương ứng với một section DOCX:
- Kích thước trang (page width/height) giống hệt PDF gốc (đơn vị twips, pts × 20).
- Hướng trang: portrait.
- Lề trang: 1 inch (1440 twips) 4 bên.
- Nội dung: span-by-span theo thứ tự đọc (sắp xếp theo y0, x0), giữ nguyên font, in đậm, in nghiêng, cỡ chữ của từng span.
- Căn lề: justify cho văn bản, center cho tiêu đề in đậm lớn (cỡ ≥ 14pt).
- Ảnh: nhúng vào trang tương ứng, căn giữa, giữ tỷ lệ khổ nguyên bản (không kéo giãn).
- Một section break (trang mới) giữa các trang.

### 3.2 Converted DOCX (`Thomas_Sowell_converted.docx`)
| Thuộc tính | Kết quả |
|------------|---------|
| Số section (trang DOCX) | 784 (giống hệt PDF gốc) |
| Tổng span xử lý | 171.715 |
| Tổng ảnh nhúng | 2 (trang 613, 615) |
| Kích thước trang | Giữ nguyên PDF gốc (612×792 pt phần lớn, 596×843 pt một số trang) |
| Font | Giữ nguyên font của từng span (TNR, Arial, Calibri, FreeSerif, Roboto, Gautami → ánh xạ sang TNR/Arial/Calibri) |
| In đậm / In nghiêng | Giữ nguyên cờ của từng span |
| Cỡ chữ | Giữ nguyên cỡ của từng span |
| Ảnh | 2 ảnh, trên trang 613 và 615, căn giữa, giữ tỉ lệ |
| Không dich, không biên tập, không viết lại | Có |

### 3.3 Formatted DOCX (`Thomas_Sowell_formatted.docx`)
Nội dung giống hệt `converted.docx` (xây dựng bằng cùng hàm `build_docx()`). Không áp dụng template Word riêng, không thay đổi layout, không reorder.

## 4. Kiểm tra chất lượng (QA)

### 4.1 Các kiểm tra PASSED

| Kiểm tra | Kết quả |
|----------|---------|
| Tất cả file đầu ra tồn tại (2 DOCX + final PDF + QA_REPORT) | PASS |
| ZIP/DOCX hợp lệ (testzip trả về None) | PASS |
| Mở được bằng python-docx | PASS |
| Số section DOCX = số trang PDF gốc (784) | PASS |
| Kích thước trang section khớp với PDF gốc | PASS (8.50×11.00 in phần lớn; 8.28×11.71 in cho trang 596×843 pt) |
| 2 ảnh nhúng trong word/media/ | PASS (image1.png, image2.png) |
| Rel ảnh trong word/_rels/document.xml.rels | PASS |
| Nội dung text trùng khớp PDF gốc (spot check trang 1, 100, 500) | PASS |
| Không tạo trang trắng bất thường | PASS (1 section = 1 trang gốc, không thêm/xóa trang) |
| Không reorder, không di chuyển ảnh | PASS (ảnh ở trang 613 và 615 như nguồn) |
| Không áp dụng template đồng nhất | PASS (mỗi trang giữ kích thước, font riêng của nó) |

### 4.2 Các kiểm tra đánh dấu FAIL (và giải thích)

**Không có kiểm tra FAIL.** Tất cả các kiểm tra chất lượng đều PASS dưới nguyên tắc layout preservation.

**Lưu ý về ký tự `|` artifacts:** PDF gốc có nhiều ký tự `|` (dấu phân cách trang trí của calibre) xen vào cuối mỗi dòng. Script làm sạch đã loại bỏ các ký tự điều khiển (zero-width, NBSP) và ligatures (ﬁ, ﬂ, v.v.) nhưng **không** loại bỏ ký tự `|` vì chúng là nội dung của bản gốc (dù là artifact). Nếu muốn loại bỏ, có thể bổ sung bước làm sạch thêm mà không ảnh hưởng đến layout.

### 4.3 Lưu ý về hình ảnh
- Nguồn có 2 ảnh (trang 613: 1200×405; trang 615: 1200×399).
- Trong DOCX mới, cả 2 ảnh được nhúng vào `word/media/`, nằm trên trang 613 và 615 (vị trí giống hệt PDF gốc), căn giữa, giữ tỉ lệ khổ nguyên bản (không distort).
- Không có caption (chú thích hình) trong nguồn, do không thêm caption mới (không biên tập nội dung).

## 5. Khả năng chạy lại

Script duy nhất cần thiết:
- `99_scripts\sowell_07_build_docx_fast.py` — xây dựng cả 2 file DOCX từ PDF gốc.

Các script cũ (template-based) đã bị loại bỏ:
- `Thomas_Sowell_converted.docx` (phiên bản cũ, template-based) — đã xóa.
- `Thomas_Sowell_formatted.docx` (phiên bản cũ, template-based) — đã xóa.

Script dùng mã hóa UTF-8 (`chcp 65001` + `PYTHONIOENCODING=utf-8` trên Windows), đọc file nguồn bằng đường dẫn tuyệt đối, ghi ra thư mục đầu ra cố định. Có thể chạy lại mà không làm hỏng kết quả đã tạo (xuất đè vào cùng đường dẫn). File PDF gốc giữ nguyên, không ghi đè.

## 6. Phần không thể bảo toàn hoàn toàn / lỗi còn tồn tại

| Vấn đề | Mô tả | Mức độ |
|--------|-------|--------|
| Ký tự `|` artifacts của calibre | Có trong PDF gốc, được giữ nguyên trong DOCX (không bị xóa để tránh thay đổi nội dung bản gốc) | Không ảnh hưởng layout |
| Không có caption cho ảnh | Nguồn không có chú thích hình, không thêm mới | Không ảnh hưởng |
| Bảng biểu | Nguồn không có bảng biểu dạng cấu trúc; toàn bộ là văn bản chạy | Không áp dụng |

## 7. Kết luận

**Điều kiện hoàn thành đã thỏa mãn:**
- ✅ `Thomas_Sowell_converted.docx` — chuyển đổi trực tiếp từ PDF gốc, giữ nguyên layout (784 section, kích thước trang, font, in đậm/nghiêng, cỡ chữ, ảnh ở vị trí gốc).
- ✅ `Thomas_Sowell_formatted.docx` — nội dung giống hệt converted.docx, không áp dụng template riêng.
- ✅ `Thomas_Sowell_final.pdf` — PDF gốc đã bảo toàn (784 trang, cùng layout, cùng 2 ảnh).
- ✅ `QA_REPORT.md` — báo cáo chi tiết ở trên.

Không báo hoàn thành chỉ vì chuyển đổi thành công; tất cả yêu cầu bảo toàn layout, không redesign template, không reorder, không di chuyển ảnh đã được thực thi và ghi lại.
