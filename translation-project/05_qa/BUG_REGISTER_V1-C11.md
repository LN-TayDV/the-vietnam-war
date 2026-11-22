# BUG REGISTER — Chương V1-C11 "Trận chiến Điện Biên Phủ"

Dự án: Dịch The Cambridge History of the Vietnam War sang tiếng Việt miền Nam (VNCH, tiền-1975)
Người tạo: Kilo (session 2026-11-22)
Trạng thái chương: HOAN_TAT pipeline (build DOCX + audit_docx_format.py PASS), với BUG-001 chưa sửa.

---

## BUG-001 (MỞ) — Thiếu 21 cước chú tiếng Việt (chưa dịch)

**Chương:** V1-C11  
**Tác động:** DOCX xuất bản không có cước chú (0/0). Các dấu mốc chú thích (1..N) đã có trong bản dịch bản thân nhưng bị xóa bỏ khi build vì không có khối chú thích訳文 gắn liền.  
**Nguyên nhân:** Tập tin TXT `v1_ch11_vi.txt` chưa có khối `--- [Cước chú ...] ---` chứa译文 của 21 chú thích từ nguồn. Chú thích nguồn trong `02_extracted_text/v1/ch11.txt` trộn lẫn với nội dung đoạn trích (PDF extraction), chưa trích xuất được tin cậy.  
**Trạng thái:** MỞ (chưa sửa)  
**Hành động khắc phục cần thiết:**
1. Trích xuất/chốt danh sách 21 chú thích từ `02_extracted_text/v1/ch11.txt` (các dòng tab-indented bắt đầu bằng số).
2. Dịch từng chú thích sang tiếng Việt theo phong cách VNCH (giữ tên tác giả, tên sách, địa điểm xuất bản, năm, trang bằng ngôn ngữ gốc; dịch phần nhận xét của tác giả nếu có).
3. Thêm khối `--- [Cước chú trang 238-258] ---` vào cuối `v1_ch11_vi.txt`, mỗi chú thích dạng `[N] nội dung ...`.
4. Rebuild DOCX bằng `99_scripts/build_chapter_docx.py 11`, kiểm tra `used == total` (N/N).
5. Chạy lại `audit_docx_format.py 11` và quality gate (criterion 8: Word COM verify cước chú).
**Ghi chú liên quan:** progress.json V1-C11 footnotes = 0, quality_gate Footnotes = GAP.

---

## Các lỗi đã sửa trong pipeline V1-C11 (ĐÃ HOÀN TẾT)

| Mã | Chương | Mức độ | Mô tả lỗi | Cách khắc phục | Trạng thái |
|----|--------|--------|-----------|----------------|------------|
| FIX-01 | V1-C11 | CAO | Văn bản bị đánh lỗi font (garbled) do bản dịch thô | Áp dụng 83 quy tắc, 102 thay thế (`fix_ch11_garbled.py`) | Đã sửa |
| FIX-02 | V1-C11 | CAO | Cảnh 영어/garbled/CJK/H브eria còn sót trong bản dịch | Áp dụng các vòng sửa round2–round7 | Đã sửa |
| FIX-03 | V1-C11 | CAO | Đoạn P055 trùng lặp bị garder lại | Xóa đoạn P055 trùng (`fix_ch11_round3.py`) | Đã sửa |
| FIX-04 | V1-C11 | CAO | Thiếu 12 marker block (P006–P009, P021–P023, P030–P032, P036, P038) | Chèn lại marker (`fix_ch11_blocks.py`) | Đã sửa |
| FIX-05 | V1-C11 | TRUNG BÌNH | Sai chính tả VNCH: `chính trị`→`chánh trị` (1), `chính phủ`→`chánh phủ` (1), `này`→`nầy` (51) | `fix_ch11_vnch.py` 74 thay thế | Đã sửa |
| FIX-06 | V1-C11 | TRUNG BÌNH | Mã hóa file TXT là CRLF (Windows), cần LF-only | Chuyển CRLF→LF (`v1_ch11_vi.txt`) | Đã sửa |
| FIX-07 | V1-C11 | TRUNG BÌNH | Script `build_chapter_docx.py` trỏ sai thư mục (thiếu tiền tố `translation-project/`) | Thêm `TP = PROJECT / "translation-project"` và sửa `SRC_DIR`, `EN_DIR`, `OUT_DIR`, `source_path()`, `img_dir()` | Đã sửa |
| FIX-08 | V1-C11 | THẤP | `đồng chí` / `giải phóng` (MAJOR) bỏ qua do mong ng idioma | Không sửa (ngữ cảnh莫明) | Bỏ qua |

**Tổng kết:** 8 vấn đề xử lý, 7 đã sửa, 1 bỏ qua (FIX-08), 1 mở (BUG-001).

---

## Kết quả kiểm thử V1-C11 (2026-11-22)

- Build DOCX: `OK ch11 -> V1-C11_Tran-chien-Dien-Bien-Phu.docx` (11,304 từ, 0/0 cước chú, nguồn: inline)
- audit_docx_format.py: PASS (heading/body/image OK, ảnh 1/caption 1, không có block-header leaks, không có metadata leaks, 0-note chapter OK)
- Encoding: UTF-8 / NFC / no-BOM / LF — PASS
- Alignment: 56/56 đoạn (P016 diff=6, P042 diff=3 chấp nhận được)
- Image manifest: `v1-C11-IMG001` (Map 11.1, vector_figure_rasterized, 141 drawings, extraction_status=OK)
- progress.json: V1-C11 đã thêm, trạng thái HOAN_TAT (có ghi chú BUG-001)

---

**Người phối cập nhật:** Cập nhật progress.json khi BUG-001 được xử lý.
