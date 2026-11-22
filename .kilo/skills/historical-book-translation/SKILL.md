---
name: historical-book-translation
description: Quy trình dịch một tác phẩm lịch sử học thuật từ đầu đến cuối. Dùng cho dự án dịch The Cambridge History of the Vietnam War (77 chương, 3 tập). Bao gồm: chuẩn bị, phân đoạn, dịch thuật, đối chiếu, xuất bản DOCX, quản lý tiến độ.
---

# Skill: Historical Book Translation — Dịch Sách Lịch Sử Học Thuật

## 1. MỤC ĐÍCH
Cung cấp quy trình chuẩn end-to-end cho việc dịch một cuốn sách lịch sử học thuật tiếng Anh sang tiếng Việt miền Nam (VNCH pre-1975). Áp dụng cho **The Cambridge History of the Vietnam War** (77 chương, ~698.500 từ).

## 2. KHI NÀO KÍCH HOẠT
- Bắt đầu dịch chương mới (bất kỳ chương nào trong 77 chương).
- Tiếp tục dự án dịch sau khi nghỉ session.
- Cần xuất bản một chương đã dịch xong (build DOCX).

## 3. ĐẦU VÀO CẦN ĐỌC TRƯỚC KHI BẮT ĐẦU

### 3.1 Bắt buộc (mỗi session mới)
| File | Mục đích |
|---|---|
| `00_plan/progress.json` | Trạng thái hiện tại, chương tiếp theo, số đoạn/cước chú |
| `07_style_guide/STYLE_GUIDE_PHAN_B.md` | 29 quy tắc VNCH (v2.3) — **Đọc kỹ trước khi dịch** |
| `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` | 7 bước dịch + VNCH Grammar Database + Checklist S1-S20, P1-P10, C1-C10 |
| `08_southern_vietnamese_library/10_LEXICAL_DATABASE/MASTER_LEXICON.csv` | 321 mục từ điển Nam có nguồn |
| `05_qa/AUDIT_REPORT_CH01-06.md` | Bài học từ 6 chương đầu (alignment, thuật ngữ, word-for-word, từ/câu khó) |

### 3.2 Tra cứu khi cần
| File | Mục đích |
|---|---|
| `03_terminology/glossary_nam_bac_compare.tsv` | Tra cứu từ Bắc/Nam |
| `03_terminology/SOURCES.md` | Nguồn ngôn ngữ miền Nam |
| `03_terminology/uncertain_terms.md` | Hàng đợi nghiên cứu (KHÔNG tự ý chốt) |

## 4. QUY TRÌNH DỊCH MỘT CHƯƠNG (8 BƯỚC)

### BƯỚC 1: ĐỌC NGUYÊN TÁC
- Mở `02_extracted_text/v1/chXX.txt` (XX = số chương 2 chữ số: 01, 02, ...).
- Ghi nhận: số trang PDF, số đoạn ước lượng, số cước chú.
- Hiểu nội dung chính, lập luận tác giả, cấu trúc chương.

### BƯỚC 2: PHÂN ĐOẠN (Paragraph Segmentation)
- Mỗi đoạn đánh số `[V1CXX-PYYY] (trang Z)` ở đầu.
- Tạo 2 file trong `04_translation/v1/chXX/`:
  - `v1_chXX_src.txt`: Nguyên tác tiếng Anh (có sẵn, copy từ extracted text).
  - `v1_chXX_vi.txt`: Bản dịch tiếng Việt (file chính thức, duy nhất).
- **QUAN TRỌNG**: Mỗi đoạn trong src và vi phải tương ứng **1-1** (cùng số lượng, cùng thứ tự).

### BƯỚC 3: DỊCH THEO STYLE GUIDE V2.3 + GRAMMAR ENGINE V2.1
Áp dụng quy trình **7 bước** cho MỖI ĐOẠN:

#### 3.1 Bước 1: Phân tích ngữ pháp nguyên tác
- Xác định: chủ thể, vị ngữ, đối tượng, mệnh đề phụ.
- Phân tích quan hệ logic: nhân quả, tương phản, nhượng bộ, mục đích, điều kiện, liệt kê.
- Chú ý cấu trúc bị động, thể khía, mệnh đề quan hệ.

#### 3.2 Bước 2: Xác định chủ thể, vị ngữ, đối tượng
- Ai/thứ gì thực hiện hành động? (Chủ thể)
- Hành động/tình trạng gì? (Vị ngữ)
- Ai/thứ gì chịu tác động? (Đối tượng)
- Nếu bị động tiếng Anh: Xác định tác nhân (by...) để chuyển sang chủ động tiếng Việt.

#### 3.3 Bước 3: Phân tích quan hệ logic giữa các mệnh đề
Sử dụng **bảng từ nối logic Nam Bộ** (Grammar Engine §1.8):
- Nhượng bộ: *dầu, dẫu* (thay *mặc dù*)
- Tương phản: *trái lại* (thay *ngược lại*)
- Chuyển ý: *tuy vậy, đã vậy, song* (thay *tuy nhiên*)
- Nhân quả: *bởi thế, do đó, cho nên* (thay *vì vậy*)
- Bổ sung: *vả, lại, cũng* (thay *hơn nữa*)

#### 3.4 Bước 4: Xác định nghĩa thuật ngữ theo ngữ cảnh
**Thứ tự tra cứu BẮT BUỘC:**
1. `MASTER_LEXICON.csv` (321 mục) → nếu có → dùng dạng trong lexicon, ghi nguồn.
2. `VNCH Grammar Database` (Grammar Engine §1.2-1.8) cho từ chức năng (chỉ định, trạng từ, đại từ, thể, từ nối).
3. Nguồn VNCH sơ cấp: Lê Văn Đức 1970, Hiến pháp VNCH 1967, Bách Khoa 405.
4. Nếu vẫn không có → **giữ nguyên thuật ngữ gốc** (in nghiêng) + giải nghĩa lần đầu + đánh dấu `[CẦN BỔ SUNG LEXICON]`.
5. **TUYỆT ĐỐI KHÔNG** tự dịch một từ mới không có nguồn.

**KHI GẶP TỪ/CÂU KHÓ** (Quy tắc 20 — Grammar Engine):
1. Mở rộng phân tích sang toàn bộ đoạn văn, đoạn trước/sau, chương, phần liên quan.
2. Xác định chủ đề, lập luận, sự kiện, nhân vật, ý đồ tác giả.
3. Tra cứu từ điển, tài liệu chuyên ngành, nguồn lịch sử.
4. Đối chiếu cách dùng từ trong các phần khác của sách.
5. Tái dựng ý nghĩa tác giả → diễn đạt tiếng Việt tự nhiên theo văn phong VNCH.
**Ghi nhận căn cứ bắt buộc**: căn cứ văn bản, ngữ cảnh, nguồn tra cứu, lập luận; phân biệt nghĩa nguyên văn / ngữ cảnh / diễn đạt; mức độ chắc chắn + lý do.

#### 3.5 Bước 5: Tái cấu trúc thành câu tiếng Việt tự nhiên (VNCH)
**Áp dụng VNCH Grammar Database (§1.3-1.8) + Quy tắc 19 (Cấm dịch từng từ) + Quy tắc 20:**
- **Chủ động hóa** câu bị động tiếng Anh (Quy tắc 26) — **QUY TẮC VÀNG**.
- **Dùng chỉ định đúng** (§1.3): *một cuốn sách, một cái bài, một con người, một cây bút, một cục đá, một thời kỳ nầy*.
- **Dùng trạng từ không gian/thời gian Nam Bộ** (§1.4): *nầy, đó, kia, trong, ngoài, trước, sau, ngày nầy, năm nầy, trước nầy, sau nầy*.
- **Dùng thể khía đúng** (§1.5): *đã... rùi/hẵng, đang... xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa... mới/mới... xong, chưa... bao giờ/vẫn chưa*.
- **Dùng đại từ nhân xưng trang trọng** (§1.7): *người ấy, ông ấy, bà ấy, họ* — **CẤM** *hắn, y, nó* chỉ người; *ta, tui, mình* (người 1); *mày, tao, cậu* (người 2).
- **Dùng từ nối logic Nam Bộ** (§1.8): *dầu, dẫu, trái lại, tuy vậy, đã vậy, song, bởi thế, do đó, vả, lại, một là... hai là...*.
- **CẤM KỊ (Quy tắc 19)**: **KHÔNG dịch từng từ rồi ghép lại**. Phải đọc toàn câu, đoạn, ngữ cảnh → tái cấu trúc.
- **KHÔNG** giữ nguyên cấu trúc câu ngoại ngữ nếu làm tiếng Việt khó hiểu.
- **KHÔNG** dùng từ Hán Việt chỉ để tạo vẻ học thuật.
- **KHÔNG** rút gọn những đoạn có nội dung lý luận.
- **KHÔNG** tự diễn giải vượt quá ý tác giả.
- **KHÔNG** fabricate (Quy tắc 27): không bịa số trang, trích dẫn, ví dụ.

#### 3.6 Bước 6: Đối chiếu lại nguyên tác
- Số câu: bản dịch phải có đúng số câu như nguyên tác (không thêm, không bớt) — S11.
- Thông tin: không mất ý chính, không thêm ý không có — S10, S11.
- Thuật ngữ: đúng lexicon, đúng VNCH Grammar — S12, S13, S14, S15, S16, S17, S18, S19, S20.
- Cước chú: marker `[N]`/`N` ở đúng vị trí, đúng thứ tự 1..N — P6.
- **Alignment**: số đoạn src = số đoạn vi (**Quy tắc 18**, C2).

#### 3.7 Bước 7: Kiểm tra tính dễ hiểu
- Đọc to câu dịch: có hiểu ngay lần đầu không? (S7)
- Có từ nào gây nhầm lẫn, câu nào rối logic không?
- Có từ miền Bắc, từ hiện đại áp đặt không?
- Có cấu trúc ngoại ngữ bê nguyên không?

### BƯỚC 4: KIỂM TRA ORTHOGRAPHY (Style Guide)
- 0× "chính trị" (phải là "chánh trị").
- 0× từ miền Bắc không phù hợp.
- Từ hiện đại chỉ dùng khi là thuật ngữ chuyên ngành (tài chính → tài chánh, đại biểu → dân biểu).

### BƯỚC 5: THÊM CỤC CHÚ (Footnotes)
- Trích xuất footnotes từ file extracted text (`02_extracted_text/v1/chXX.txt`).
- Đặt trong khối `--- [Cước chú trang X-Y] ---`; có thể gom ở cuối chương (ch03/ch04) hoặc đặt theo cụm trang (ch01/ch02).
- Mỗi footnote đánh số `[N] ` hoặc `N ` (ch03/ch04 dùng dạng trần `1 Jean Decoux…`); phải đủ và đúng thứ tự 1..N.
- Giữ nguyên tên tác giả, tựa sách, nhà xuất bản (tiếng Anh/Pháp); dịch phần giải nghĩa trong ngoặc vuông.
- **QUAN TRỌNG**: Giữ marker `[N]`/`N` ngay trong thân bài bản dịch → script neo chính xác.

### BƯỚC 6: KIỂM TRA ENCODING
- UTF-8, NFC, không BOM, LF (không CRLF).
- Python: `encoding="utf-8", newline="\n"`.
- PowerShell: **KHÔNG** dùng heredoc cho tiếng Việt (cp1252 issue) — dùng Python script.
- Kiểm tra: `python -c "import sys; f=open('file.txt','rb'); b=f.read(); ..."` hoặc script check.

### BƯỚC 7: CẬP NHẬT PROGRESS.JSON
- Thêm/cập nhật entry `V1-CXX` với: status, paragraphs, footnotes, pages.
- Cập nhật `volumes.V1.status`.

### BƯỚC 8: XUẤT DOCX CHUẨN (BẮT BUỘC)

**Trước khi build, BẮT BUỘC chạy kiểm tra footnote markers:**
1. `python 99_scripts/check_footnote_markers.py NN` → phải PASS (0 missing, 0 duplicate, 0 orphan). Nếu FAIL → sửa TXT, không được build DOCX.
2. Chạy script: `python translation-project/99_scripts/build_chapter_docx.py NN` (NN = số chương).
3. Xác nhận dòng `OK ... (N/N cước chú, nguồn: inline|source)`; nếu `WARN` → sửa input, build lại.
4. Mở bằng Word COM, kiểm tra `Footnotes.Count` = `notes` trong `progress.json`.
5. Cập nhật `docx`, `docx_status` trong `progress.json`.

## 5. QUALITY GATE (8 TIÊU CHÍ — Quy tắc 29)
Chương chỉ được đánh dấu `HOAN_TAT` khi **TẤT CẢ PASS**:

| # | Tiêu chí | Cách kiểm tra |
|---|---|---|
| 1 | Encoding UTF-8, NFC, no BOM, LF | `encoding_checker.py` (Common) |
| 2 | Orthography: 0× "chính trị", 0× từ miền Bắc | `vnch_orthography.py` (Common) |
| 3 | Đồng bộ đoạn: src = vi | `document_comparator.py` (Common) |
| 4 | Đồng bộ cước chú: src = vi | `docx_builder.py` (Common) build verify |
| 5 | Không fabricate | Manual review |
| 6 | Văn phong tự nhiên, không dịch từng từ | Checklist S1-S20, P1-P10; `translation_validator.py` (Common) |
| 7 | DOCX tồn tại 09_docx/, sinh bởi `docx_builder.py` (Common) | File exists |
| 8 | DOCX cước chú: `OK N/N`, Word `Footnotes.Count` = `notes`, footnote chân trang 9pt, đánh số 1..N | Word COM check |

## 6. QUY TẮC QUẢN LÝ FILE (BẮT BUỘC)

### 6.1 Chỉ 2 file trong thư mục chương
Mỗi `04_translation/v1/chXX/` chỉ duy trì **2 file**:
1. `v1_chXX_src.txt` — Nguyên tác tiếng Anh.
2. `v1_chXX_vi.txt` — Bản dịch tiếng Việt chính thức.

**KHÔNG** tạo: file `_FINAL.txt`, `_REALIGNED.txt`, `.docx`, `.json`, `.md` trong thư mục chương.

### 6.2 Vị trí file chuẩn
| Loại file | Thư mục đích |
|---|---|
| Bản dịch + nguồn | `04_translation/v1/chXX/` |
| DOCX xuất bản | `09_docx/` |
| Script tạm / debug | `99_scripts/` hoặc `C:\Users\PC\AppData\Local\Temp\kilo\` |
| QA / ghi chú | `05_qa/` |
| Thuật ngữ / tra cứu | `03_terminology/` |
| Style guide | `07_style_guide/` |

### 6.3 Dọn dẹp sau mỗi session
Trước khi kết thúc: xóa file tạm (`tmp_*`, `debug_*`, `*.bak`, `*_old`) ở workspace gốc.

## 7. LIÊN KẾT SKILLS LIÊN QUAN
- **contextual-translation**: Phân tích ngữ cảnh, lập luận trước khi dịch (Bước 1-3).
- **southern-vietnamese-editorial-style**: Chuẩn hóa văn phong VNCH (Bước 3.5, Bước 4).
- **historical-terminology-research**: Nghiên cứu thuật ngữ (Bước 3.4).
- **deep-translation-review**: Đối chiếu bản dịch (Bước 3.6, Bước 7).
- **translation-error-detection**: Phát hiện lỗi thường gặp (alignment, word-for-word, VNCH terminology).
- **translation-quality-gate**: Kiểm định 8 tiêu chí trước HOAN_TAT.
- **translation-error-kb**: Tra cứu lỗi thực tế đã gặp để phòng ngừa.

## 8. TRẠNG THÁI HIỆN TẠI (2026-11-20)
- **V1-Ch1 đến V1-Ch6**: HOAN_TAT (đã audit, đã xuất DOCX, có hình ảnh).
- **V1-Ch7 đến V1-Ch21**: Chưa bắt đầu.
- **Volume 2, 3**: Chưa bắt đầu.

---

*Cập nhật: 2026-11-20 — Tích hợp bài học từ audit 6 chương đầu, Common Scripts, PDF Đối Chiếu, Grammar Guide.*