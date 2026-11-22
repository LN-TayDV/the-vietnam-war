---
name: deep-translation-review
description: Đối chiếu và kiểm tra bản dịch ở cấp câu, đoạn và chương. Phát hiện lỗi sai ý, thiếu ý, thừa ý, sai quan hệ logic, câu tối nghĩa, tiếng Anh còn sót. Dựa trên Grammar Engine checklist S1-S20, P1-P10, C1-C10 và bài học từ Audit 6 chương đầu.
---

# Skill: Deep Translation Review — Đối Chiếu Sâu Bản Dịch

## 1. MỤC ĐÍCH
Đảm bảo bản dịch đạt **ba điều kiện cốt lõi** (Grammar Engine §0):
1. **Đúng nghĩa nguyên tác** — không thêm, không bớt, không đổi nghĩa.
2. **Đúng ngữ pháp tiếng Việt** — câu đúng cấu trúc VN, không bê nguyên cấu trúc ngoại ngữ.
3. **Truyền đạt rõ ràng ý tưởng tác giả** — người đọc hiểu ngay lần đầu, không phải đọc lại để giải mã.

## 2. KHI NÀO KÍCH HOẠT
- **Bắt buộc** sau khi dịch xong mỗi chương (Grammar Engine Bước 6-7).
- Khi audit chương đã hoàn tất (Deep Review).
- Khi user yêu cầu re-review/re-audit (như task hiện tại).
- **KHÔNG** mặc nhiên tin kết quả review cũ — phải đối chiếu độc lập.

## 3. CÔNG CỤ & TÀI LIỆU THAM CHIẾU
| File | Mục đích |
|---|---|
| `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` | Checklist S1-S20, P1-P10, C1-C10; Error Taxonomy E01-E16 |
| `07_style_guide/STYLE_GUIDE_PHAN_B.md` | 29 quy tắc VNCH (v2.3) |
| `05_qa/AUDIT_REPORT_CH01-06.md` | Bài học 6 chương đầu (alignment, word-for-word, VNCH terminology) |
| `04_translation/v1/chXX/v1_chXX_src.txt` | Nguyên tác tiếng Anh |
| `04_translation/v1/chXX/v1_chXX_vi.txt` | Bản dịch tiếng Việt chính thức |
| `02_extracted_text/v1/chXX.txt` | Text gốc PDF (cho cước chú, hình ảnh) |
| **Common Scripts** | `.kilo/scripts/common/` — `document_comparator.py`, `vnch_orthography.py`, `encoding_checker.py`, `translation_validator.py`, `quality_gate.py` |

## 4. QUY TRÌNH ĐỐI CHIẾU (3 CẤP)

### 4.1 CẤP SENTENCE (Câu) — 20 Mục (S1-S20)
**Thực hiện cho MỖI CÂU trong chương:**

| Mã | Kiểm tra | Nếu FAIL |
|---|---|---|
| S1 | Chủ ngữ rõ ràng? | Xác định lại chủ thể |
| S2 | Vị ngữ đúng hành động? | Kiểm tra lại động từ |
| S3 | Đối tượng rõ ràng? | Xác định lại tân ngữ |
| S4 | Đại từ có quy chiếu rõ? | Thay bằng *người ấy/ông ấy/bà ấy* hoặc danh từ cụ thể |
| S5 | Mệnh đề phụ gắn đúng đối tượng? | Sắp xếp lại mệnh đề |
| S6 | Quan hệ nhân quả đúng chiều? | Sửa liên từ theo §1.8 (dầu, trái lại, tuy vậy, bởi thế, vả) |
| S7 | Hiểu ngay lần đọc đầu? | Viết lại ngắn gọn hơn |
| S8 | Từ Hán Việt dùng đúng nghĩa? | Tra từ điển, sửa |
| S9 | Có cấu trúc ngoại ngữ bê nguyên? | Tái cấu trúc theo VN + VNCH Grammar |
| S10 | Có thêm nghĩa không có trong nguyên tác? | Bỏ phần thêm |
| S11 | Có bớt nghĩa có trong nguyên tác? | Thêm lại phần thiếu (Quy tắc 16) |
| S12 | Thuật ngữ có trong lexicon/VNCH Grammar? | Tra lexicon + VNCH Grammar Database, hoặc đánh dấu |
| S13 | Có dùng từ miền Bắc? | Thay bằng dạng Nam Bộ (Rule 2) |
| S14 | Có dùng từ hiện đại áp đặt? | Thay bằng dạng VNCH (Rule 12) |
| **S15** | **Chỉ định danh từ đúng Nam Bộ?** | Sửa theo §1.3 (cuốn/cái/con/cây/cục/bài) |
| **S16** | **Trạng từ dùng nầy/đó/kia?** | Sửa theo §1.4 (Rule 22) |
| **S17** | **Thể khía đầy đủ?** | Sửa theo §1.5 (Rule 23) |
| **S18** | **Bị động đã chủ động hóa?** | Áp dụng §1.6 (Rule 26) |
| **S19** | **Đại từ nhân xưng trang trọng?** | Sửa theo §1.7 (Rule 24) |
| **S20** | **Từ nối logic Nam Bộ?** | Sửa theo §1.8 (Rule 25) |

**Lưu ý**: S15-S20 là các mục mới từ VNCH Grammar Database (Audit 6 chương).

### 4.2 CẤP PARAGRAPH (Đoạn) — 10 Mục (P1-P10)
**Thực hiện cho MỖI ĐOẠN:**

| Mã | Kiểm tra | Nếu FAIL |
|---|---|---|
| P1 | Ý chính rõ ràng? | Xác định lại topic sentence |
| P2 | Các câu liên kết logic? | Sắp xếp lại, thêm từ nối §1.8 |
| P3 | Có câu lặp ý hoặc thừa? | Gộp hoặc bỏ |
| **P4** | **Kết thúc bằng dấu chấm?** | Hoàn tất câu cuối (Quy tắc 16) |
| **P5** | **Số câu = gốc?** | Kiểm tra alignment (Quy tắc 18) |
| **P6** | **Marker cước chú `[N]`/`N` đúng vị trí, thứ tự?** | Điều chỉnh marker. **BẮT BUỘC**: chạy `python 99_scripts/check_footnote_markers.py --chapter NN` để xác nhận không missing, không duplicate, không orphan. |
| **P7** | **Heading có marker "— đề mục —"?** | Khôi phục marker |
| P8 | Thuật ngữ nhất quán trong đoạn? | Thống nhất theo lexicon |
| P9 | Văn phong tự nhiên, mượt mà? | Viết lại câu cứng |
| P10 | Không fabricate? | Xóa phần bịa (Quy tắc 27) |

**P4, P5, P6, P7 là CRITICAL** — liên quan trực tiếp đến Quality Gate.

### 4.3 CẤP CHAPTER (Chương) — 10 Mục (C1-C10)
**Thực hiện cho TOÀN CHƯƠNG:**

| Mã | Kiểm tra | Nếu FAIL |
|---|---|---|
| C1 | Giữ nguyên hệ thống lập luận tác giả? | Xác định lại cấu trúc chương |
| **C2** | **Số đoạn src = số đoạn vi?** | Chạy `debug_align.py`, realign (Quy tắc 18) |
| **C3** | **Số cước chú src = số cước chú vi?** | Kiểm tra marker, build DOCX verify |
| C4 | Thuật ngữ xuyên suốt nhất quán? | Thống nhất theo lexicon |
| C5 | Văn phong VNCH đồng nhất? | Chạy `apply_vnch_fixes.py` |
| **C6** | **Encoding UTF-8/NFC/no BOM/LF?** | Check encoding (Quy tắc 28) |
| **C7** | **DOCX build "OK N/N"?** | Fix input, rebuild |
| **C8** | **Word Footnotes.Count = notes trong progress.json?** | Fix marker/neo cước chú |
| **C9** | **Footnote chân trang 9pt, đánh số 1..N?** | Check build script |
| **C10** | **Quality Gate 8 tiêu chí PASS?** | Chỉ HOAN_TAT khi PASS hết (Quy tắc 29) |

## 5. PHÁT HIỆN LỖI THƯỜNG GẶP (Error Taxonomy E01-E16)

| Mã | Tên lỗi | Mức độ | Cấp độ | Ví dụ thực tế (Audit 6 chương) | Quy tắc sửa |
|---|---|---|---|---|---|
| **E01** | Thiếu đoạn giữa câu | CRITICAL | Sentence | Ch1 P012: "Thuật ngữ này —" (bỏ lửng 3 câu) | Quy tắc 16, S11 |
| **E02** | Alignment lệch đoạn | CRITICAL | Chapter | Ch1: 49 src vs 50 vi (lệch từ P008); Ch5: 15 src vs 9 vi | Quy tắc 18, C2 |
| **E03** | Dịch từng từ ghép lại | CRITICAL | Sentence | *chính phủ, giải phóng, đồng chí, Annam* | Quy tắc 19, S9 |
| **E04** | Sai thuật ngữ VNCH core | CRITICAL | Sentence | *chính trị* → *chánh trị* (69 lần) | Quy tắc 1, 4, 12 |
| **E05** | Sai từ miền Bắc | MAJOR | Sentence | *này, giải phóng, đồng chí, chính phủ* | Quy tắc 2, 8, 12, 22, 24 |
| **E06** | Sai từ hiện đại áp đặt | MAJOR | Sentence | *tài chính, đại biểu, lương hưu* | Quy tắc 3, 4, 12 |
| **E07** | Sai tên thuộc địa | MAJOR | Sentence | *Annam, Tonkin* (giữ tên Pháp) | Quy tắc 15 |
| E08 | Bê nguyên cấu trúc bị động | MINOR | Sentence | "được ký bởi" | Quy tắc 26, S18 |
| E09 | Thiếu chỉ định danh từ | MINOR | Sentence | *một sách* (thiếu *cuốn/cái*) | Quy tắc 21, S15 |
| E10 | Sai trạng từ *này/nầy* | MINOR | Sentence | *năm này* | Quy tắc 22, S16 |
| E11 | Sai thể khía *đang* | MINOR | Sentence | *đang ký kết* | Quy tắc 23, S17 |
| E12 | Sai từ nối *tuy nhiên* | MINOR | Sentence | *Tuy nhiên, kết quả...* | Quy tắc 25, S20 |
| E13 | Sai đại từ nhân xưng | MINOR | Sentence | *hắn, nó* chỉ người | Quy tắc 24, S19 |
| **E14** | Fabricate thông tin | CRITICAL | Paragraph | Bịa số trang, trích dẫn | Quy tắc 27, P10 |
| **E15** | Encoding sai | CRITICAL | Chapter | cp1252, BOM, CRLF | Quy tắc 28, C6 |
| **E16** | Quality Gate không PASS | CRITICAL | Chapter | Chưa đủ 8 tiêu chí | Quy tắc 29, C10 |

## 6. QUY TRÌNH REVIEW ĐỘC LẬP (KHÔNG DỰA VÀO AUDIT CŨ)

### 6.1 Nguyên tắc
- **KHÔNG** chỉ đọc báo cáo audit cũ và xác nhận.
- **PHẢI** đối chiếu trực tiếp: câu gốc ↔ câu dịch ↔ ngữ cảnh đoạn.
- **PHẢI** kiểm tra lại các lỗi audit cũ đã sửa (có thể sửa chưa đúng).
- **PHẢI** chủ động tìm lỗi audit cũ bỏ sót (alignment, word-for-word, từ/câu khó).

### 6.2 Quy trình thực tế (cho task re-review hiện tại)
1. **Đọc nguyên tác** (src.txt) — hiểu nội dung, lập luận, cấu trúc.
2. **Đọc bản dịch** (vi.txt) — đánh dấu chỗ nghi ngờ.
3. **Đối chiếu từng câu** — S1-S20.
4. **Đối chiếu từng đoạn** — P1-P10 (đặc biệt P4, P5, P6, P7).
5. **Kiểm tra toàn vẹn footnote markers** — chạy `python 99_scripts/check_footnote_markers.py NN` (P6, C3). Nếu FAIL → sửa TXT trước khi tiếp tục.
6. **Kiểm tra alignment** — chạy `python .kilo/scripts/common/document_comparator.py NN` (C2).
6. **Kiểm tra thuật ngữ VNCH** — chạy `python .kilo/scripts/common/vnch_orthography.py --check-only NN` (C5).
7. **Kiểm tra encoding** — `python .kilo/scripts/common/encoding_checker.py --chapter NN` (C6).
8. **Build DOCX verify** — dùng `docx_builder.py` (Common) → `OK N/N` (C7).
9. **Word COM check** — Footnotes.Count (C8), footnote format (C9).
10. **Quality Gate** — 8 tiêu chí PASS (C10).

### 6.3 Sửa trực tiếp bản dịch chính thức
- Nếu nhiệm vụ cho phép: sửa **trực tiếp** `v1_chXX_vi.txt`.
- **KHÔNG** tạo file `_FINAL.txt`, `_REALIGNED.txt`, bản nháp.
- **Giữ nguyên** tên file, cấu trúc thư mục.
- Sau sửa: đọc lại toàn đoạn/chương để bảo đảm mạch lạc.

## 7. CÁC LỖI NGHIÊM TRỌNG AUDIT 6 CHƯƠNG BỎ SÓT (CẦN KIỂM TRA THÊM)

| Lỗi | Mô tả | Chương liên quan |
|---|---|---|
| **Heading mismatch** | 3 heading bị mất marker "— đề mục —" | Ch4 (3 heading), Ch6 (3 heading) |
| **Sentence count mismatch** | Nhiều đoạn lệch 1-2 câu so với gốc | Ch2 (P001, P027, P035, P040), Ch3 (P021, P025, P060, P062), Ch4 (10+ đoạn), Ch6 (P051, P058, P073, P078, P080) |
| **Footnote marker missing** | Thiếu marker `[N]` trong thân bài so với notes block | Ch12 (42 markers bị mất: [15], [16], [24]-[26], [35]-[76]); Ch11 (0/0 footnotes, xem Bug Register BUG-008) |
| **Footnote marker duplicate** | Marker `[N]` xuất hiện >1 lần trong thân bài | Ch12 ([20] xuất hiện 2 lần) |
| **VNCH false positive** | 43 "lỗi" trong tên sách/trích dẫn/tổ chức tiếng Pháp — KHÔNG SỬA | Toàn bộ |
| **Từ tiếng Anh còn sót** | *nation, pays, supposedly transient, staffing, greatly, severely, staging, meant to be, agitation, coolie, trump mere patriotism, voie royale, Five Dragons, Front populaire, grafting, teleology, ultima avis, glass ceiling, allegory, brinkmanship, en même temps, en route, gouvernement de fait, essentialism, fascism, autarky, ersatz, phalanx, exacted a dreadful toll, Improvisation, deus ex machina* | Ch2, Ch3, Ch4 |

## 8. LIÊN KẾT SKILLS
- **historical-book-translation**: Bước 3.6, Bước 7.
- **contextual-translation**: Kiểm tra ngữ cảnh, lập luận.
- **southern-vietnamese-editorial-style**: Kiểm tra văn phong VNCH (S13-S20).
- **historical-terminology-research**: Kiểm tra thuật ngữ (S12).
- **translation-error-detection**: Phát hiện lỗi theo Taxonomy E01-E16.
- **translation-quality-gate**: Chạy Quality Gate 8 tiêu chí.
- **translation-error-kb**: Tra cứu lỗi thực tế đã gặp.

---

*Cập nhật: 2026-11-20 — Dựa trên Grammar Engine v2.1 §3-7, Audit 6 chương §2-3, Task re-review 2026-11-20.*