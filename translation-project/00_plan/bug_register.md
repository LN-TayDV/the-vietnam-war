# BUG REGISTER — Dự án Dịch The Cambridge History of the Vietnam War

**Tập trung tất cả lỗi đã xác định, nghi ngờ và rủi ro tiềm ẩn trong toàn bộ quy trình dịch.**
**File này là single source of truth. Mọi lỗi mới phát hiện phải được ghi vào đây kèm bằng chứng.**

---

## 1. TỔNG QUAN

| Thống kê | Số lượng |
|----------|----------|
| Tổng số bug đã xác nhận | 9 |
| Đã khắc phục (tạm thời/thủ công) | 3 |
| Đã khắc phục (tự động/toàn hệ thống) | 0 |
| Chưa xử lý | 6 |
| Rủi ro tiềm ẩn (risk) | 4 |
| Nguyên nhân gốc đã xác minh | 5 |

---

## 2. DANH SÁCH BUG ĐÃ XÁC NHẬN

### BUG-001 — Footnote markers bị mất khi dịch EN→VI (CRITICAL)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-001 |
| **Tên lỗi** | Footnote inline markers [N] bị mất trong bản dịch tiếng Việt |
| **Mức độ** | CRITICAL (chặn HOAN_TAT, làm sai toàn bộ footnotes trong DOCX) |
| **Giai đoạn phát sinh** | Bước 3: Dịch thuật (EN→VI) |
| **Nguyên nhân gốc** | Dịch giả coi inline marker `[N]` là artifacts định dạng, không phải nội dung ngữ nghĩa → bỏ qua khi dịch. Marker không phải từ tiếng Việt tự nhiên nên dễ bị loại bỏ vô ý thức. |
| **Bằng chứng** | Chương 12: 42 marker bị mất: [15], [16], [24], [25], [26], [35]-[69], [70]-[76]. Source text `02_extracted_text/v1/ch12.txt` có đầy đủ 76 markers. Bản dịch `v1_ch12_vi.txt` ban đầu chỉ có 34 marker. |
| **Phạm vi ảnh hưởng** | Tất cả chương có footnote (ch01-ch12, và mọi chương sau). Ch11 đã Known Issue (0/0 footnotes). |
| **Phương án khắc phục** | 1. Thêm script `check_footnote_markers.py` so sánh markers source vs translation trước khi build. 2. Buộc phải rebuild TXT (không fix trực tiếp DOCX). 3. Thêm bước pre-build vào `chapter_workflow.py`. |
| **Regression test** | `check_footnote_markers.py --chapter 12` phải báo 0 missing, 0 duplicate. |
| **Điều kiện nghiệm thu** | Mọi chương mới build phải chạy `check_footnote_markers.py` vàPASS (exit 0) trước khi `build_chapter_docx.py`. |
| **Trạng thái** | **Đã khắc phục thủ công cho Ch12** (markers [15],[16],[24]-[26],[35]-[76] đã khôi phục). **Chưa có tự động hóa phòng ngừa cho chương sau.** |
| **Kỹ năng chịu trách nhiệm** | `translation-workflow`, `translation-quality-gate`, `deep-translation-review`, `historical-book-translation` |

---

### BUG-002 — Không có kiểm tra toàn vẹn footnote markers trước build DOCX (CRITICAL)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-002 |
| **Tên lỗi** | `build_chapter_docx.py` không validate rằng tất cả source footnote markers có trong translation |
| **Mức độ** | CRITICAL |
| **Giai đoạn phát sinh** | Bước 8: Xuất DOCX |
| **Nguyên nhân gốc** | `plan_footnotes()` trong `build_chapter_docx.py` chỉ trích xuất markers đã có trong TXT. Nếu marker đã bị mất ở bước dịch, script sẽ không phát hiện → build thành công nhưng footnotes thiếu. Fallback `source_placements()` cố gắng tự động đặt markers nhưng không tin cậy. |
| **Bằng chứng** | Ch12: 42 markers bị mất nhưng `build_chapter_docx.py 12` vẫn báo `OK` (vì nó dùng fallback source_placements hoặc chỉ báo count khớp notes block, không kiểm tra body markers). |
| **Phạm vi ảnh hưởng** | Mọi chương build DOCX sau này |
| **Phương án khắc phục** | Tạo script `check_footnote_markers.py` chạy TRƯỚC `build_chapter_docx.py`. Nếu thiếu marker → exit 1, chặn build. |
| **Regression test** | Chạy script trên Ch12 sau khi fix → phải PASS. Chạy trên TXT giả tạo thiếu marker → phải FAIL. |
| **Điều kiện nghiệm thu** | Script tồn tại, được gọi trong `chapter_workflow.py` bước `all` trước `build`. |
| **Trạng thái** | **Chưa xử lý** |
| **Kỹ năng chịu trách nhiệm** | `translation-workflow`, `translation-quality-gate` |

---

### BUG-003 — Duplicate footnote marker không được phát hiện (MAJOR)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-003 |
| **Tên lỗi** | Marker trùng lặp trong body text không được báo lỗi |
| **Mức độ** | MAJOR |
| **Giai đoạn phát sinh** | Bước 3: Dịch thuật |
| **Nguyên nhân gốc** | `extract_inline_markers()` trong `build_chapter_docx.py` chấp nhận marker `[N]` bất kỳ, không kiểm tra trùng lặp. Nếu `[23]` xuất hiện 2 lần, script chỉ nhận lần đầu, lần thứ hai bị bỏ qua hoặc gây xung đột. |
| **Bằng chứng** | Ch12: marker `[23]` bị trùng ở cuối P023. Đã bị xóa thủ công. |
| **Phạm vi ảnh hưởng** | Mọi chương có footnote |
| **Phương án khắc phục** | `check_footnote_markers.py` phát hiện duplicate và báo lỗi. |
| **Regression test** | TXT giả tạo có marker trùng → script báo FAIL. |
| **Điều kiện nghiệm thu** | Script kiểm tra duplicate, exit 1 nếu có trùng. |
| **Trạng thái** | **Đã khắc phục thủ công cho Ch12** (xóa [23] trùng). **Chưa có tự động hóa.** |
| **Kỹ năng chịu trách nhiệm** | `translation-quality-gate`, `deep-translation-review` |

---

### BUG-004 — Header/footer artifacts được strip theo cách hardcode per-chapter (MAJOR)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-004 |
| **Tên lỗi** | `is_header_footer_line()` trong `build_chapter_docx.py` chỉ kiểm tra hardcoded `CHAPTER_TITLE_VI`, `CHAPTER_TITLE_EN`, `AUTHOR_NAME`, `CONTINUATION` cho Ch12 |
| **Mức độ** | MAJOR |
| **Giai đoạn phát sinh** | Bước 8: Xuất DOCX |
| **Nguyên nhân gốc** | Hàm `is_header_footer_line()` chỉ biết nhận diện artifacts của Ch12. Các chương khác có header/footer khác nhau (tác giả khác, tên chương khác) sẽ không được strip → artifacts lọt vào DOCX body. |
| **Bằng chứng** | Ch12: 47 artifact lines đã strip (bao gồm "Martin Thomas", "Hội nghị Geneva năm 1954"). Chương khác (ví dụ Ch08 có tác giả "Chen Jian") sẽ không được strip tên tác giả nếu nó xuất hiện trong body. |
| **Phạm vi ảnh hưởng** | Tất cả chương khác Ch12 |
| **Phương án khắc phục** | Thay hardcode bằng pattern matching generics: dòng chỉ chứa số trang, dòng trùng tên tác giả trong progress.json, dòng trùng tiêu đề chương. Hoặc cho phép config per-chapter trong progress.json. |
| **Regression test** | Tạo TXT test với header artifact giả lập → script phải strip. |
| **Điều kiện nghiệm thu** | `is_header_footer_line()` hoạt động cho bất kỳ chương nào mà không cần hardcode tên tác giả/tiêu đề. |
| **Trạng thái** | **Chưa xử lý** |
| **Kỹ năng chịu trách nhiệm** | `translation-workflow`, `historical-book-translation` |

---

### BUG-005 — Subheading detection dùng heuristic, không phải marker rõ ràng (MAJOR)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-005 |
| **Tên lỗi** | `looks_like_subheading()` dùng heuristic (dưới 90 ký tự, không có dấu câu kết câu) thay vì marker rõ ràng |
| **Mức độ** | MAJOR |
| **Giai đoạn phát sinh** | Bước 2: Phân đoạn / Bước 8: Build DOCX |
| **Nguyên nhân gốc** | Hàm `looks_like_subheading()` heuristic có thể misclassify: đoạn văn ngắn có thể được nhận nhầm thành heading; heading dài (>90 ký tự) có thể bị bỏ qua. Cần `KNOWN_SUBHEADINGS` fallback cho Ch12. |
| **Bằng chứng** | Ch12: 5 subheadings cần KNOWN_SUBHEADINGS dict để detect đúng. |
| **Phạm vi ảnh hưởng** | Mọi chương có subheading |
| **Phương án khắc phục** | Buộc phải dùng marker `— đề mục —` trong block header cho mọi subheading (theo quy tắc 8A.3 của translation-workflow SKILL.md). Script chỉ nhận subheading khi có marker này. |
| **Regression test** | TXT có block `--- [...] (trang Z) — đề mục ---` → được tạo thành Heading 2. TXT không có marker → không được tạo heading. |
| **Điều kiện nghiệm thu** | Không còn dùng `KNOWN_SUBHEADINGS` hardcode. Mọi subheading phải có marker rõ ràng trong TXT. |
| **Trạng thái** | **Chưa xử lý** |
| **Kỹ năng chịu trách nhiệm** | `translation-workflow`, `historical-book-translation` |

---

### BUG-006 — Orphaned footnotes bị dump vô âm vào paragraph cuối (CRITICAL)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-006 |
| **Tên lỗi** | `build()` trong `build_chapter_docx.py` dump footnotes không có body reference vào paragraph cuối |
| **Mức độ** | CRITICAL (mask lỗi thay vì phát hiện) |
| **Giai đoạn phát sinh** | Bước 8: Xuất DOCX |
| **Nguyên nhân gốc** | Lines 909-917 của `build_chapter_docx.py`: nếu có note trong `notes` block nhưng không có body marker, script thêm footnote ref vào paragraph cuối cùng. Điều này làm che chứa lỗi marker thiếu. |
| **Bằng chứng** | Trước khi fix Ch12, footnotes 35-69 bị gom vào paragraph cuối (P046 "Kết luận"). |
| **Phạm vi ảnh hưởng** | Mọi chương có footnote |
| **Phương án khắc phục** | Xóa fallback dump. Nếu có orphan notes → raise error, chặn build, báo rõ ràng哪些 note bị thiếu marker. |
| **Regression test** | TXT có note block nhưng không có marker trong body → build phải FAIL với thông báo lỗi. |
| **Điều kiện nghiệm thu** | Không còn dump orphan footnotes vào paragraph cuối. |
| **Trạng thái** | **Chưa xử lý** |
| **Kỹ năng chịu trách nhiệm** | `translation-workflow`, `translation-quality-gate` |

---

### BUG-007 — Quality Gate criterion 4 chỉ kiểm tra count, không kiểm tra placement (MAJOR)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-007 |
| **Tên lỗi** | Quality Gate tiêu chí 4 (`Đồng bộ cước chú`) chỉ kiểm tra số lượng `OK N/N` và `Word COM Footnotes.Count`, không kiểm tra từng footnote đặt ở paragraph đúng |
| **Mức độ** | MAJOR |
| **Giai đoạn phát sinh** | Bước 8: Quality Gate |
| **Nguyên nhân gốc** | `quality_gate.py` và `translation-quality-gate` skill chỉ kiểm tra count khớp, không kiểm tra vị trí placement của từng footnote tương ứng với source marker. |
| **Bằng chứng** | Ch12: 76/76 footnotes đều có trong DOCX nhưng một số bị đặt sai paragraph (gom vào paragraph cuối) trước khi fix. Quality Gate vẫn PASS vì count khớp. |
| **Phạm vi ảnh hưởng** | Mọi chương build DOCX |
| **Phương án khắc phục** | Thêm kiểm tra: mỗi footnote marker `[N]` trong body phải tương ứng với footnote `[N]` trong notes block, và placement phải đúng paragraph so với source (dựa trên `document_comparator.py` hoặc marker position). |
| **Regression test** | TXT có markers đặt sai vị trí so với source → Quality Gate phải FAIL. |
| **Điều kiện nghiệm thu** | Quality Gate kiểm tra placement, không chỉ count. |
| **Trạng thái** | **Chưa xử lý** |
| **Kỹ năng chịu trách nhiệm** | `translation-quality-gate`, `deep-translation-review` |

---

### BUG-008 — Chương 11 thiếu toàn bộ footnotes (CRITICAL - Known Issue)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-008 |
| **Tên lỗi** | Chương 11 có 0/0 footnotes, chưa dịch 21 chú thích |
| **Mức độ** | CRITICAL |
| **Giai đoạn phát sinh** | Bước 5: Thêm cước chú |
| **Nguyên nhân gốc** | Khối 'Cước chú' chưa được thêm vào TXT vì chú thích nguồn trộn lẫn với nội dung trích xuất PDF, không trích xuất được tin cậy. Các dấu mốc footnote trong bản dịch đã bị xóa khi build. |
| **Bằng chứng** | `progress.json` V1-C11: `footnotes: 0`, `status: HOAN_TAT pipeline (build + audit PASS)`, notes: "BUG-001: thiếu 21 cước chú译文 chưa được thêm vào TXT". |
| **Phạm vi ảnh hưởng** | Chương 11 |
| **Phương án khắc phục** | Dịch 21 chú thích từ nguồn, thêm khối `--- [Cước chú ...] ---` vào TXT, thêm inline markers vào body, rebuild DOCX. |
| **Regression test** | Sau khi fix: Ch11 phải có 21 footnotes, `check_footnote_markers.py` PASS. |
| **Điều kiện nghiệm thu** | Ch11 có đầy đủ 21 footnotes, DOCX rebuild, Quality Gate PASS. |
| **Trạng thái** | **MỞ RỘNG (đã biết, đang theo dõi trong progress.json)** |
| **Kỹ năng chịu trách nhiệm** | `historical-book-translation`, `translation-workflow` |

---

### BUG-009 — Duplicate marker [20] trong body Chương 12 (MAJOR)

| Trường | Nội dung |
|--------|----------|
| **Mã lỗi** | BUG-009 |
| **Tên lỗi** | Duplicate marker [20] trong body Chương 12 |
| **Mức độ** | MAJOR |
| **Giai đoạn phát sinh** | Bước 3: Dịch thuật |
| **Nguyên nhân gốc** | Marker [20] xuất hiện 2 lần trong body (P018 và P019). Một trong hai có thể là lỗi khi dịch, hoặc cần là marker khác. |
| **Bằng chứng** | Script `check_footnote_markers.py --chapter 12` báo: "[20] appears 2 times". |
| **Phạm vi ảnh hưởng** | Chương 12 |
| **Phương án khắc phục** | Đối chiếu với source text để xác định marker đúng tại mỗi vị trí. Một trong hai [20] có thể cần đổi thành marker khác hoặc xóa. |
| **Regression test** | `check_footnote_markers.py --chapter 12` phải báo 0 duplicate. |
| **Điều kiện nghiệm thu** | Không còn marker trùng trong body Ch12. |
| **Trạng thái** | **MỞ RỘNG** (đã phát hiện bởi script mới, chưa sửa nội dung dịch) |
| **Kỹ năng chịu trách nhiệm** | `deep-translation-review`, `translation-error-detection` |

---

## 3. RỦI RO TẦM TẦM (RISK — Chưa xác nhận là lỗi nhưng có nguy cơ cao)

### RISK-001: Không có script so sánh footnote markers source vs translation

- **Mô tả**: Không có công cụ tự động so sánh markers giữa file src và file vi. Phải dùng manual forensic audit (như đã làm cho Ch12).
- **Nguyên nhân**: Chưa ai viết script này.
- **Phương án phòng ngừa**: Viết `check_footnote_markers.py` (xem BUG-002).

### RISK-002: Header/footer artifacts khác chương khác không được strip

- **Mô tả**: Chương khác có tên tác giả, tiêu đề khác nhau → `is_header_footer_line()` không nhận diện → artifacts lọt vào DOCX.
- **Nguyên nhân**: Hardcode per-chapter (xem BUG-004).
- **Phương án phòng ngừa**: Generic pattern matching (xem BUG-004).

### RISK-003: Subheading được misclassify ở chương sau

- **Mô tả**: Heuristic `looks_like_subheading()` có thể nhận nhầm đoạn ngắn thành heading hoặc bỏ qua heading dài.
- **Nguyên nhân**: Không có marker rõ ràng (xem BUG-005).
- **Phương án phòng ngừa**: Buộc marker `— đề mục —` (xem BUG-005).

### RISK-004: Fallback `source_placements()` đặt marker sai vị trí

- **Mô tả**: Nếu inline markers thiếu, `source_placements()` cố gắng tự động đặt dựa trên page ratio, nhưng không tin cậy và có thể đặt sai.
- **Nguyên nhân**: Không có validation bắt buộc markers phải có trong TXT trước khi build.
- **Phương án phòng ngừa**: Chặn build nếu thiếu marker (xem BUG-002, BUG-006).

---

## 4. NGUYÊN NHẠN GỐC ĐÃ XÁC MINH

| # | Nguyên nhân gốc | Bug liên quan | Bằng chứng |
|---|----------------|---------------|------------|
| RC-001 | Inline footnote markers `[N]` không phải nội dung ngữ nghĩa → dịch giả bỏ qua khi dịch EN→VI | BUG-001, BUG-002 | Ch12 thiếu 42 markers; source text có đầy đủ 76 |
| RC-002 | Không có script validate markers trước build DOCX | BUG-002 | `build_chapter_docx.py` chỉ trích xuất markers đã có, không kiểm tra tính đầy đủ |
| RC-003 | `build()` dump orphan footnotes vào paragraph cuối thay vì báo lỗi | BUG-006 | Lines 909-917 `build_chapter_docx.py` |
| RC-004 | `is_header_footer_line()` hardcode per-chapter | BUG-004 | Chỉ biết artifacts Ch12 (Martin Thomas, Hội nghị Geneva năm 1954) |
| RC-005 | `looks_like_subheading()` dùng heuristic không marker rõ ràng | BUG-005 | Cần `KNOWN_SUBHEADINGS` dict cho Ch12 |

---

## 5. QUY TRÌNH BỔ SUNG BUG MỚI

Khi phát hiện lỗi mới:

1. Ghi vào file này với mã lỗi `BUG-XXX` (tăng dần từ BUG-009).
2. Điền đầy đủ: Mã, Tên, Mức độ, Giai đoạn, Nguyên nhân, Bằng chứng, Phạm vi, Phương án khắc phục, Regression test, Điều kiện nghiệm thu, Kỹ năng chịu trách nhiệm, Trạng thái.
3. Nếu là rủi ro tiềm ẩn → ghi vào mục 3 (RISK).
4. Nếu xác định được nguyên nhân gốc mới → ghi vào mục 4 (RC-XXX).
5. Cập nhật mục 1 (Tổng quan) sau mỗi lần thêm/sửa.

---

## 6. LIÊN KẾT KỸ NĂNG

| Kỹ năng | Bug chịu trách nhiệm |
|---------|---------------------|
| `translation-workflow` | BUG-001, BUG-002, BUG-004, BUG-005, BUG-006, BUG-008 |
| `translation-quality-gate` | BUG-002, BUG-003, BUG-006, BUG-007 |
| `deep-translation-review` | BUG-001, BUG-003, BUG-007, BUG-009 |
| `historical-book-translation` | BUG-004, BUG-005, BUG-008 |
| `translation-error-detection` | BUG-001, BUG-003, BUG-009 (phát hiện qua script/grep) |

---

*Cập nhật: 2026-11-22 — Tạo ban đầu dựa trên sự cố footnote Chương 12 (42 markers bị mất, đã khôi phục). BUG-009 phát hiện bởi script check_footnote_markers.py mới (duplicate [20] trong Ch12).*
