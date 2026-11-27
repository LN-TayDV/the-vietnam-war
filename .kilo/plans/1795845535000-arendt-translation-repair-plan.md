# EXECUTION PLAN — ARENDT TRANSLATION REPAIR (13 CHAPTERS + FOOTNOTES + DOCX)

**Dự án:** `C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt`  
**Sách:** *The Origins of Totalitarianism* — Hannah Arendt (Meridian 1962, 574 trang)  
**Ngôn ngữ mục tiêu:** Tiếng Việt miền Nam (VNCH trước 1975)  
**Skill tham chiếu:** `.kilo/skills/translation-workflow/SKILL.md`  
**Chế độ:** PLAN MODE — chỉ đọc, phân tích, lập kế hoạch. KHÔNG sửa bản dịch, KHÔNG thay đổi file, KHÔNG triển khai.

---

## 1. CURRENT-STATE FINDINGS

### 1.1 Cấu trúc dự án (đã khảo sát)

| Thư mục | Mô tả | Trạng thái |
|---|---|---|
| `00_plan/` | progress.json, TRANSLATION_PLAN.md | Có |
| `01_raw_text/` | meridian_1962/, meridian_1962_analysis/ | Có |
| `02_extracted_text/` | v7/ | Có |
| `03_terminology/` | ARENDT_TERMINOLOGY.md | Có |
| `04_translation/v2/ch01-13/` | Mỗi chương: `v1_chNN_src.txt` + `v1_chNN_vi.txt` | Có, 13 chương |
| `04_translation/v2/front_matter/` | Có | Có |
| `05_qa/` | **TRỐNG** | Không có file |
| `08_southern_vietnamese_library/` | Có | Có |
| `09_docx/` | 10 file DOCX (V2-01 … V2-13, trừ V2-03, V2-05, V2-07, V2-08, V2-09) | Có, 10/13 |
| `99_scripts/` | 85 file script (build_chapter_docx.py, build_chapter_docx_v2.py, build_master_docx_v2.py, validate_docx.py, phase1_full_audit.py, test_continuity.py, test_duplicates.py, v.v.) | Có |
| `audit/` | CHAPTER_AUDIT_MATRIX.md, FULL_13_CHAPTER_AUDIT.md, full_chapter_audit.json, translation_inventory.json, alignment_baseline.json, docx_structure_baseline.json, OCR_RECONSTRUCTION_ARTIFACTS.md, part_files_inventory.json | Có |

### 1.2 Tìmings thực tế quan trọng (CRITICAL FINDINGS)

#### A. Footnote content bị chèn vào body text (CRITICAL — NGUYÊN NHẬN GỐC)

Trong các file `v1_chNN_vi.txt`, nội dung footnote xuất hiện CÙNG LÚC ở cả body text VÀ trong block `=== FOOTNOTES ===`. Điều này gây trùng lặp nội dung.

**Bằng chứng cụ thể (ch01):**

| Vị trí | Nội dung body | Footnote ID | Nội dung footnote trong `=== FOOTNOTES ===` | Trùng? |
|---|---|---|---|---|
| P008 (trang 25) | "...sự bách hại và tiêu diệt của Nazi có thể trông giống ²" | ² | "...như một sự gia tốc vô nghĩa của một tiến trình mà có lẽ dù sao cũng đã diễn ra. Điều nầy cũng đúng với hầu hết mọi nước Tây Âu..." | ✅ TRÙNG với P009 |
| P009 (trang 24) | "...như một sự gia tốc vô nghĩa của một tiến trình mà có lẽ dù sao cũng đã diễn ra..." | — | (nội dung footnote ²) | ✅ NỘI DUNG FOOTNOTE ² Ở TRONG BODY |
| P017 (trang 27) | "...khủng bố chỉ trong trường hợp cuối cùng của sự phát triển của nó mới là ³" | ³ | "...một hình thức chính quyền thuần túy. Để thiết lập một chế độ toàn trị..." | ✅ TRÙNG với P010 |
| P010 (trang 24) | "...một hình thức chính quyền thuần túy. Để thiết lập một chế độ toàn trị..." | — | (nội dung footnote ³) | ✅ NỘI DUNG FOOTNOTE ³ Ở TRONG BODY |
| P019 (trang 27) | "...đã là trung tâm của hệ tư tưởng Nazi. ⁴" | ⁴ | "Điểm mấu chốt đối với sử gia là người Do Thái..." | ✅ TRÙNG với P019 body |
| P019 (trang 27) | "...đã là trung tâm của hệ tư tưởng Nazi. ⁴ Điểm mấu chốt đối với sử gia..." | — | (nội dung footnote ⁴) | ✅ NỘI DUNG FOOTNOTE ⁴ Ở TRONG BODY |

**Tác động:** Khi `build_chapter_docx.py` xử lý, nội dung footnote được render làm body paragraph THÊM SAU ĐÓ còn được tạo thành Word native footnote → nội dung chú thích xuất hiện hai lần trong DOCX.

#### B. Chương tiêu đề nằm trong body paragraph

| File | Đoạn | Vấn đề |
|---|---|---|
| ch01 | P001 | "Chương Một: Chủ nghĩa chống Do Thái — Một sự lăng mạ đối với lẽ thường" nằm trong body paragraph |
| ch02 | P001 | "Chương Hai: NHỮNG NGƯỜI DO THÁI, NHÀ NƯỚC DÂN TỘC, VÀ SỰ RA ĐỜI CỦA CHỦ NGHĨA CHỐNG DO THÁI" nằm trong body paragraph |
| ch04 | P001 | "Chương Bốn: Vụ Dreyfus" nằm trong body paragraph |
| ch12 | P001 | "CHƯƠNG MƯỜI HAI / Chủ nghĩa Toàn trị trong Quyền lực" nằm trong body paragraph |
| ch12 | P015 | "II. NHÀ NƯỚC TOÀN TRỊ HUYỀN THOẠI" (section heading) nằm trong body paragraph |

#### C. Inline footnote definitions bị lặp (ch12, CRITICAL)

Theo `ROOT_CAUSE_REPAIR_REPORT.md` và `FULL_13_CHAPTER_AUDIT.md`:
- ch12: 12 inline footnote issues, cùng footnote definitions (¹³-²²) lặp lại trên 3 trang khác nhau
- ch12: 39 placeholder footnotes, footnotes 72/154/158 thiếu body anchor
- ch12: embedded PAGE artifacts trong footnote definitions

#### D. Văn bản bị chia ngang trang không được nối đúng

Theo `FULL_13_CHAPTER_AUDIT.md`:
- ch04: 8 cross-page issues (severity HIGH)
- ch12: 14 cross-page issues, 9 severity HIGH
- ch13: 28 cross-page issues, severity HIGH
- ch02: 1 cross-page issue (84→85, HIGH)

#### E. VNCH orthography lỗi hệ thống (tất cả chương)

Theo `CHAPTER_AUDIT_Matrix.md` và `FULL_13_CHAPTER_AUDIT.md`:
- `được` passive overuse: 42-222x/chương
- `cái` classifier overuse: 2-155x/chương
- `rất` vs `quá`: 1-29x/chương
- `chính phủ` → `chánh phủ`: 38-48x (ch07, ch12, ch13)

#### F. Foreign language fragments còn sót

Theo `TRANSLATION_REPORT.md` và `FULL_13_CHAPTER_AUDIT.md`:
- Tất cả 13 chương đều có ~30 English fragments còn sót
- ch03: French, Latin fragments
- ch04: French fragments
- ch05: French, Latin, English fragments
- ch06: French, Latin, English fragments
- ch08: OCR artifacts (Pan-Xlaven→Pan-Xlavơ, Pan-Duc→Pan-Dức)
- ch12: English fragments (preceded, giuramento, stakes, circumscribe, counter, fantastique, altogether, autonomous, turns out), Cyrillic artifact (`строго speaking`)

#### G. Missing translations (front matter + 4 prefaces + part intro)

Theo `progress.json` và `CHAPTER_AUDIT_MATRIX.md`:
- front_matter: 5 paras, 0 vi paras
- preface_first_edition: 2 paras, 0 vi paras
- preface_part_one: 4 paras, 0 vi paras
- preface_part_two: 4 paras, 0 vi paras
- preface_part_three: 13 paras, 0 vi paras
- part_one_intro: 4 paras, 0 vi paras

#### H. DOCX build status

Theo `ROOT_CAUSE_REPAIR_REPORT.md`:
- ch01: 0/0 footnotes, OK
- ch02: 21/21, OK
- ch03: 79/79, OK
- ch04: 96/100, WARN (4 missing definitions)
- ch05: 60/60, OK
- ch06: 65/65, OK
- ch07: 103/103, OK
- ch08: 98/98, OK
- ch09: 54/54, OK
- ch10: 61/65, WARN (4 missing definitions)
- ch11: 103/103, OK
- ch12: 135/139, WARN (4 missing body anchors: fns 72, 154, 158 + 1 more)
- ch13: 5/5, OK

#### I. Heading detection

Theo `CHAPTER_AUDIT_MATRIX.md`:
- Tất cả chương: 0 headings detected (trừ ch12 có 45 false positives từ running headers)
- Chương tiêu đề không được detect thành Heading 1
- Section headings (I, II, … VI) không được detect

### 1.3 Source of truth

| Loại | File | Lý do |
|---|---|---|
| Sách gốc | `books/Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf` (theo progress.json) | Source PDF gốc |
| Text nguồn | `04_translation/v2/chNN/v1_chNN_src.txt` | Đã trích, UTF-8 NFC, LF |
| Bản dịch | `04_translation/v2/chNN/v1_chNN_vi.txt` | Bản dịch hiện tại, cần repair |
| Terminology | `03_terminology/ARENDT_TERMINOLOGY.md` | Source of truth cho thuật ngữ Arendt |
| Style guide | `07_style_guide/STYLE_GUIDE_PHAN_B.md` | 29 quy tắc VNCH |
| Grammar Engine | `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` | 7 bước dịch + Checklist |
| Builder | `99_scripts/build_chapter_docx.py` | Script xuất DOCX hiện tại |

---

## 2. ROOT-CAUSE ANALYSIS

### 2.1 Nguyên nhân gốc 1: Footnote content bị chèn vào body text (CRITICAL)

**Vị trí:** `04_translation/v2/chNN/v1_chNN_vi.txt` (tất cả chương có footnote)

**Mô tả:** Khi dịch, người dịch đã chèn toàn bộ nội dung footnote vào thân bài dưới dạng đoạn văn tiếp theo, thay vì chỉ giữ marker (¹²³…) tại vị trí tham chiếu và để toàn bộ nội dung chú thích trong block `=== FOOTNOTES ===`. Điều này làm nội dung chú thích xuất hiện hai lần: một lần trong body, một lần trong footnotes block.

**Ví dụ (ch01):**
- P008 kết thúc bằng marker ², sau đó P009 bắt đầu bằng nội dung của footnote ²
- P017 kết thúc bằng marker ³, sau đó P010 bắt đầu bằng nội dung của footnote ³

**Tác động:** DOCX build sẽ render nội dung footnote làm body text PLUS tạo Word native footnote → trùng lặp.

**Sửa chữa:** Xóa toàn bộ nội dung footnote đã bị chèn vào body, giữ lại chỉ marker tại vị trí tham chiếu. Đảm bảo toàn bộ nội dung chú thích chỉ nằm trong block `=== FOOTNOTES ===`.

### 2.2 Nguyên nhân gốc 2: Chương tiêu đề và section heading nằm trong body paragraph

**Vị trí:** `04_translation/v2/chNN/v1_chNN_vi.txt` (ch01, ch02, ch04, ch12, và các chương khác)

**Mô tả:** Tiêu đề chương và section heading (I, II, … VI) được đánh là body paragraph thay vì heading structure. Khi `build_chapter_docx.py` xử lý, chúng được render làm body text thường thay vì heading.

**Sửa chữa:** Tách tiêu đề chương và section heading ra khỏi body paragraph, đánh dấu đúng heading level (Chapter title → H1, Section → H2/H3).

### 2.3 Nguyên nhân gốc 3: Inline footnote definitions bị lặp (ch12)

**Vị trí:** `04_translation/v2/ch12/v1_ch12_vi.txt`

**Mô tả:** Cùng một footnote definition (¹³-²²) xuất hiện nhiều lần trên các trang khác nhau. Khi builder xử lý, chỉ lấy lần đầu, các lần sau bị bỏ qua hoặc gây xung đột.

**Sửa chữa:** Giữ lại chỉ lần đầu tiên của mỗi footnote ID, xóa các bản lặp sau.

### 2.4 Nguyên nhân gốc 4: Paragraph bị chia ngang trang không được nối đúng

**Vị trí:** `04_translation/v2/chNN/v1_chNN_vi.txt` + `02_extracted_text/v7/`

**Mô tả:** Đoạn văn bị cắt ở cuối trang PDF, phần tiếp theo nằm ở đầu trang tiếp theo. Bản dịch hiện tại chưa nối đúng các đoạn này, gây mất câu hoặc đoạn bị tách thành hai phần không liên lạc.

**Sửa chữa:** Đối chiếu src vs vi tại mỗi ranh giới trang, nối các đoạn bị chia ngang trang thành một đoạn hoàn chỉnh.

### 2.5 Nguyên nhân gốc 5: Running headers và OCR artifacts không được lọc

**Vị trí:** `04_translation/v2/chNN/v1_chNN_vi.txt`

**Mô tả:** Running headers (ví dụ: "TOÀN TRỊ CHỦ NGHĨA 391"), số trang đơn lẻ, và OCR artifacts còn sót trong body text. Theo `ROOT_CAUSE_REPAIR_REPORT.md`, các running header ALL-CAPS bị misclassify thành structural headings.

**Sửa chữa:** Lọc bỏ running headers, số trang đơn lẻ, và OCR artifacts khỏi body text trước khi build.

### 2.6 Nguyên nhân gốc 6: VNCH orthography lỗi hệ thống

**Vị trí:** `04_translation/v2/chNN/v1_chNN_vi.txt` (tất cả 13 chương)

**Mô tả:** `được` passive overuse, `cái` classifier overuse, `rất` vs `quá`, `chính phủ` → `chánh phủ` — các lỗi VNCH systematically xuất hiện ở mọi chương.

**Sửa chữa:** Áp dụng `vnch_orthography.py` và batch normalize theo `STYLE_GUIDE_PHAN_B.md`.

### 2.7 Nguyên nhân gốc 7: Foreign language fragments còn sót

**Vị trí:** `04_translation/v2/chNN/v1_chNN_vi.txt` (tất cả 13 chương)

**Mô tả:** English, French, German, Latin fragments chưa được dịch hoặc chưa được xử lý đúng theo VLP-01 (tiếng Việt trước).

**Sửa chữa:** Áp dụng VLP-01: dịch nghĩa sang tiếng Việt, chỉ giữ ngoại ngữ khi có lý do ngôn học rõ ràng.

### 2.8 Nguyên nhân gốc 8: Missing translations (front matter, prefaces, part intro)

**Vị trí:** `04_translation/v2/front_matter/`, `preface_*/`, `part_one_intro/`

**Mô tả:** 6 section không có file bản dịch v2.

**Sửa chữa:** Dịch các section này (phần này nằm ngoài phạm vi repair plan nếu user chỉ muốn repair 13 chapter — cần xác nhận).

---

## 3. ALL AFFECTED FILES AND COMPONENTS

### 3.1 Translation files (cần sửa nội dung)

| File | Vấn đề chính |
|---|---|
| `04_translation/v2/ch01/v1_ch01_vi.txt` | Footnote content duplicated in body (², ³, ⁴), chapter title in P001 |
| `04_translation/v2/ch02/v1_ch02_vi.txt` | Chapter title in P001, footnote content in body |
| `04_translation/v2/ch03/v1_ch03_vi.txt` | Duplicate paragraphs (P014/P035), VNCH orthography |
| `04_translation/v2/ch04/v1_ch04_vi.txt` | Chapter title in P001, 4 missing footnote definitions, cross-page issues |
| `04_translation/v2/ch05/v1_ch05_vi.txt` | 3 duplicate paragraph pairs, VNCH orthography |
| `04_translation/v2/ch06/v1_ch06_vi.txt` | 2 duplicate paragraph pairs, VNCH orthography |
| `04_translation/v2/ch07/v1_ch07_vi.txt` | 2 duplicate paragraph pairs, `chính phủ`→`chánh phủ` (1x) |
| `04_translation/v2/ch08/v1_ch08_v1.txt` | OCR artifacts (Pan-Xlaven, Pan-Duc), VNCH orthography |
| `04_translation/v2/ch09/v1_ch09_vi.txt` | VNCH orthography |
| `04_translation/v2/ch10/v1_ch10_vi.txt` | 1 duplicate paragraph pair, 4 missing footnote definitions |
| `04_translation/v2/ch11/v1_ch11_vi.txt` | 1 duplicate paragraph pair, VNCH orthography |
| `04_translation/v2/ch12/v1_ch12_vi.txt` | **CRITICAL**: inline fn defs duplicated (¹³-²²), 39 placeholder fns, fns 72/154/158 missing anchors, PAGE artifacts, Cyrillic artifacts, English fragments, chapter title in P001, section heading in P015 |
| `04_translation/v2/ch13/v1_ch13_vi.txt` | Cross-page issues (28), VNCH orthography, part files (_p001_006.txt, etc.) |

### 3.2 Builder files (cần sửa logic)

| File | Vấn đề |
|---|---|
| `99_scripts/build_chapter_docx.py` | Không detect footnote content leaked into body; không validate footnote content uniqueness; không tách chapter title/section heading khỏi body |
| `99_scripts/build_chapter_docx_v2.py` | Cần kiểm tra (phiên bản v2) |
| `99_scripts/build_master_docx_v2.py` | Cần kiểm tra |
| `99_scripts/validate_docx.py` | Chỉ kiểm tra count, không kiểm tra footnote content trong body |

### 3.3 Supporting files (tham khảo)

| File | Vai trò |
|---|---|
| `audit/FULL_13_CHAPTER_AUDIT.md` | Chi tiết lỗi từng chương |
| `audit/CHAPTER_AUDIT_MATRIX.md` | Ma trận audit |
| `audit/full_chapter_audit.json` | Dữ liệu audit có cấu trúc |
| `audit/translation_inventory.json` | Inventory từng chapter |
| `99_scripts/ROOT_CAUSE_REPAIR_REPORT.md` | Root cause analysis đã làm |
| `99_scripts/TRANSLATION_REPORT.md` | Foreign language remnants |
| `00_plan/progress.json` | Tiến độ từng chương |
| `03_terminology/ARENDT_TERMINOLOGY.md` | Terminology source of truth |

---

## 4. REPAIR TASKS IN EXECUTION ORDER

**Nguyên tắc:** Sửa engine trước, rồi sửa dữ liệu, rồi rebuild. KHÔNG sửa tay DOCX.

### Phase 0 — Xác định Source of Truth và Scope (chưa sửa file)

1. Xác nhận sách gốc: *The Origins of Totalitarianism*, Hannah Arendt, Meridian 1962 (theo progress.json)
2. Xác nhận 13 chương cần repair (ch01-ch13)
3. Quyết định: front_matter, prefaces, part_one_intro có nằm trong scope repair không (hiện chưa có file dịch v2)
4. Tạo progress.json phiên bản mới đánh dấu trạng thái thực tế của 13 chương

### Phase 1 — Repair builder engine (fix underlying defects)

1. **Sửa `build_chapter_docx.py`**: Thêm hàm detect footnote content leaked into body — quét body paragraphs để tìm nội dung trùng khớp với footnote definitions trong block `=== FOOTNOTES ===`, báo lỗi nếu phát hiện
2. **Sửa `build_chapter_docx.py`**: Thêm validate rằng mỗi footnote definition chỉ được reference một lần trong body (không trùng marker)
3. **Sửa `build_chapter_docx.py`**: Thêm detect chapter title và section heading trong body paragraph, tách ra thành heading structure
4. **Sửa `build_chapter_docx.py`**: Thêm lọc running headers, số trang đơn lẻ, OCR artifacts khỏi body text trước khi render
5. **Sửa `build_chapter_docx.py`**: Thêm validate footnote numbering sequential (1..N) và không có gap
6. **Tái build tất cả 13 chapter** sau khi dữ liệu đã được repair

### Phase 2 — Repair translation data (tất cả 13 chapter)

7. **ch01**: Xóa footnote content duplicated trong body (P009 là nội dung fn ², P010 là nội dung fn ³); tách chapter title từ P001
8. **ch02**: Xóa footnote content duplicated trong body; tách chapter title từ P001
9. **ch03**: Xóa duplicate paragraph (P014/P035); chuẩn hóa VNCH orthography
10. **ch04**: Xóa chapter title từ P001; thêm 4 missing footnote definitions; sửa cross-page issues
11. **ch05**: Xóa 3 duplicate paragraph pairs (P006/P007, P019/P020, P024/P025); chuẩn hóa VNCH
12. **ch06**: Xóa 2 duplicate paragraph pairs (P007/P008, P025/P026); chuẩn hóa VNCH
13. **ch07**: Xóa 2 duplicate paragraph pairs (P016/P017, P024/P025); sửa `chính phủ`→`chánh phủ`; chuẩn hóa VNCH
14. **ch08**: Sửa OCR artifacts (Pan-Xlaven→Pan-Xlavơ, Pan-Duc→Pan-Dức); chuẩn hóa VNCH
15. **ch09**: Chuẩn hóa VNCH orthography
16. **ch10**: Xóa duplicate paragraph pair (P005/P006); thêm 4 missing footnote definitions; chuẩn hóa VNCH
17. **ch11**: Xóa duplicate paragraph pair (P011/P012); chuẩn hóa VNCH
18. **ch12**: **CRITICAL** — Xóa inline footnote definitions duplicated (giữ chỉ lần đầu ¹³-²²); xóa 39 placeholder footnotes hoặc đánh dấu UNVERIFIED; thêm body anchors cho fns 72/154/158; xóa PAGE artifacts khỏi footnote definitions; sửa Cyrillic artifact (`строго speaking`); xóa chapter title từ P001; tách section heading từ P015; dịch English fragments còn sót
19. **ch13**: Sửa cross-page issues (28); chuẩn hóa VNCH orthography

### Phase 3 — VNCH orthography & foreign language fragments (tất cả chapter)

20. Chạy `vnch_orthography.py` cho tất cả 13 chapter → 0 lỗi CRITICAL/MAJOR
21. Áp dụng VLP-01: dịch các English/French/German/Latin fragments còn sót, chỉ giữ nguyên khi có lý do ngôn học
22. Chuẩn hóa `được` passive, `cái` classifier, `rất`→`quá` theo STYLE_GUIDE_PHAN_B.md

### Phase 4 — Rebuild DOCX và validation

23. Rebuild tất cả 13 chapter DOCX bằng `build_chapter_docx.py` đã sửa
24. Chạy `audit_docx_format.py` cho từng chapter → PASS
25. Kiểm tra Word `Footnotes.Count` = số footnotes trong progress.json
26. Validate không có footnote content trong body text của DOCX
27. Validate footnote numbering 1..N đúng thứ tự

### Phase 5 — Quality gates và acceptance

28. Chạy Quality Gate 8 tiêu chí cho tất cả 13 chapter
29. Xác nhận tất cả chapter đạt PASS
30. Tổng hợp báo cáo repair cuối cùng

---

## 5. CHAPTER-BY-CHAPTER REPAIR MATRIX (ALL 13 CHAPTERS)

| Chương | Source integrity | Paragraph reconstruction | Heading/subheading errors | Body contamination (footnote leaked) | Footnote marker/content errors | Duplicate/missing content | Foreign fragments | DOCX errors | Severity | Affected files |
|---|---|---|---|---|---|---|---|---|---|---|
| ch01 | OK | OK | Chapter title in P001 | fn ²,³,⁴ content in body (P009,P010,P019) | Markers ²,³,⁴ correctly placed but content duplicated | 0 | ~30 English | OK | CRITICAL | `v1_ch01_vi.txt` |
| ch02 | OK | OK | Chapter title in P001 | Footnote content in body | ~21 markers, content may duplicate | 0 | ~30 English | OK | CRITICAL | `v1_ch02_vi.txt` |
| ch03 | OK | OK | 0 | 0 | 79 markers OK | 1 duplicate pair (P014/P035) | ~30 English | OK | MAJOR | `v1_ch03_vi.txt` |
| ch04 | OK | OK | Chapter title in P001 | 0 | 100 defs, 4 missing definitions | 0 | ~30 French | WARN (96/100) | CRITICAL | `v1_ch04_vi.txt` |
| ch05 | OK | OK | 0 | 0 | 60 markers OK | 3 duplicate pairs | ~30 French/Latin/English | OK | MAJOR | `v1_ch05_vi.txt` |
| ch06 | OK | OK | 0 | 0 | 65 markers OK | 2 duplicate pairs | ~30 French/Latin/English | OK | MAJOR | `v1_ch06_vi.txt` |
| ch07 | OK | OK | 0 | 0 | 103 markers OK | 2 duplicate pairs | ~30 English | OK | MAJOR | `v1_ch07_vi.txt` |
| ch08 | OK | OK | 0 | 0 | 98 markers OK | 0 | OCR artifacts (Pan-Xlaven, Pan-Duc) | OK | MAJOR | `v1_ch08_vi.txt` |
| ch09 | OK | OK | 0 | 0 | 54 markers OK | 0 | ~30 English | OK | MAJOR | `v1_ch09_vi.txt` |
| ch10 | OK | OK | 0 | 0 | 65 defs, 4 missing | 1 duplicate pair | ~30 German | WARN (61/65) | CRITICAL | `v1_ch10_vi.txt` |
| ch11 | OK | OK | 0 | 0 | 103 markers OK | 1 duplicate pair | ~30 German | OK | MAJOR | `v1_ch11_vi.txt` |
| ch12 | OK | OK | Chapter title in P001; section heading in P015 | Inline fn defs (¹³-²²) in body | 139 defs, fns 72/154/158 missing anchors, 39 placeholders | 12 inline FN duplicates | English + Cyrillic (`строго speaking`) | WARN (135/139) | CRITICAL | `v1_ch12_vi.txt` |
| ch13 | OK | Cross-page (28 issues) | 0 | 0 | 5 defs OK | 0 | ~30 English | OK | MAJOR | `v1_ch13_vi.txt` |

---

## 6. DOCX BUILDER REPAIR TASKS

**File mục tiêu:** `99_scripts/build_chapter_docx.py` (không thay thế bằng builder mới)

### 6.1 Footnote-specific repairs

| Task | Mô tả | Vị trí trong code |
|---|---|---|
| 6.1.1 | Thêm hàm `detect_footnote_content_in_body(body_items, notes)` — quét mỗi body paragraph để tìm nội dung trùng khớp với footnote definitions, báo lỗi nếu phát hiện | Sau `parse()`, trước `build()` |
| 6.1.2 | Thêm validate: mỗi footnote ID trong `notes` phải có đúng một marker tương ứng trong body (không trùng, không thiếu) | Trong `build()`, trước `install_footnotes()` |
| 6.1.3 | Thêm validate: footnote numbering sequential 1..N, không có gap | Trong `build()` |
| 6.1.4 | Thêm validate: không có orphan footnote (note def không có body marker) — raise error thay vì dump vào paragraph cuối | Hiện tại đã có (lines 491-495), cần giữ |

### 6.2 Structure repairs

| Task | Mô tả | Vị trí trong code |
|---|---|---|
| 6.2.1 | Thêm detect chapter title trong body paragraph (dòng đầu chứa "Chương X:" hoặc "CHƯƠNG X") → tách thành title block | Trong `parse()` hoặc `build()` |
| 6.2.2 | Thêm detect section heading (Roman I-VI, Arabic "1:", ALL-CAPS) trong body → tách thành Heading 2/3 | Hiện tại có `SECTION_RE`, `ARABIC_SECTION_RE`, `ALLCAPS_SECTION_RE` nhưng chỉ nhận standalone lines |
| 6.2.3 | Thêm lọc running headers (ALL-CAPS page headers) khỏi body text | Trong `parse()`, dùng `PAGE_ARTIFACT_RE` hoặc pattern mới |

### 6.3 Build flow repairs

| Task | Mô tả |
|---|---|
| 6.3.1 | Thêm pre-build validation: nếu `detect_footnote_content_in_body` báo lỗi → raise ValueError, chặn build |
| 6.3.2 | Thêm post-build validation: kiểm tra DOCX output không chứa footnote content trong body paragraphs |
| 6.3.3 | Giữ nguyên OOXML footnote structures (`w:footnoteReference`, `w:footnote`, `FootnoteText`, `FootnoteReference` styles) — đã đúng, không cần đổi |

---

## 7. FOOTNOTE-SPECIFIC IMPLEMENTATION AND VALIDATION STRATEGY

### 7.1 Phát hiện footnote content leaked vào body

**Algorithm:**
1. Parse file `v1_chNN_vi.txt` → lấy `body_items` (danh sách paragraph) và `notes` (dict footnote ID → content)
2. Cho mỗi body paragraph, chuẩn hóa text (xóa whitespace, xóa markers ¹²³…)
3. Cho mỗi footnote definition, chuẩn hóa text tương tự
4. Nếu body paragraph text chứa footnote definition text (hoặc ngược lại) → báo lỗTE: `FOOTNOTE_CONTENT_IN_BODY`
5. Báo cáo: chapter, paragraph ID, footnote ID, vị trí

### 7.2 Xác định marker và footnote ID mapping

**Algorithm:**
1. Parse body paragraphs, dùng `split_markers()` để lấy các superscript runs → footnote numbers
2. Parse `=== FOOTNOTES ===` block → lấy footnote ID và content
3. Mapping: footnote number trong body ↔ footnote ID trong notes block (theo thứ tự xuất hiện)
4. Validate: số lượng markers trong body == số lượng notes definitions
5. Validate: không có marker trùng lặp
6. Validate: không có note orphan (note def không có body marker)

### 7.3 Validation gates

| Gate | Mô tả | PASS condition |
|---|---|---|
| G1 | Footnote content không nằm trong body | 0 paragraph trùng với footnote definition |
| G2 | Mọi note def có body marker | 0 orphan notes |
| G3 | Mọi body marker có note def | 0 orphan markers |
| G4 | Không có marker trùng | 0 duplicate markers |
| G5 | Footnote numbering sequential | 1..N, không gap |
| G6 | Word `Footnotes.Count` == notes count | Exit 0 từ builder |
| G7 | DOCX body không chứa footnote text | 0 footnote content in body paragraphs |

---

## 8. QUALITY GATES AND ACCEPTANCE CRITERIA

### 8.1 Measurable PASS/FAIL gates

| # | Gate | PASS condition | FAIL condition |
|---|---|---|---|
| QG1 | All 13 chapters accounted for | Tất cả ch01-ch13 có file dịch và DOCX | Bất kỳ chapter nào thiếu |
| QG2 | Chapter and subheading hierarchy correct | Chapter title là H1, section là H2/H3, không có heading trong body | Heading nằm trong body paragraph |
| QG3 | No duplicated headings | Không có heading trùng lặp (trừ intentional source duplicates) | Duplicate heading phát hiện |
| QG4 | No incorrectly split/merged paragraphs | Paragraph count src == vi, cross-page joins đúng | Cross-page issues còn sót |
| QG5 | No footnote content inside body text | 0 footnote definition trùng với body paragraph | Footnote content trong body |
| QG6 | All footnote references linked to native Word footnotes | `Footnotes.Count` == notes count, mỗi marker có footnote | Orphan marker/note |
| QG7 | No missing, duplicated, or orphaned footnotes | 0 missing, 0 duplicate, 0 orphan | Bất kỳ lỗi nào |
| QG8 | No stray OCR artifacts (standalone P, etc.) | 0 OCR artifact lines trong body | OCR artifacts còn sót |
| QG9 | No unintended foreign-language fragments | 0 English/French/German fragments có thể dịch | Fragments còn sót |
| QG10 | Images, captions, tables preserved | Image count == caption count, đúng vị trí | Ảnh/caption bị mất hoặc sai vị trí |
| QG11 | DOCX generated by repaired builder | Tất cả 13 DOCX build bởi `build_chapter_docx.py` đã sửa | Build thất bại hoặc WARN |

**Quan trọng:** Không đánh dấu chapter PASS chỉ vì DOCX đã được generate. Phải pass tất cả QG1-QG11.

### 8.2 Acceptance criteria per chapter

| Chương | QG1 | QG2 | QG3 | QG4 | QG5 | QG6 | QG7 | QG8 | QG9 | QG10 | QG11 | Overall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ch01 | ✅ | ❌ (title in P001) | ✅ | ✅ | ❌ (fn leaked) | ❌ | ❌ | ✅ | ❌ | N/A | ❌ | FAIL |
| ch02 | ✅ | ❌ (title in P001) | ✅ | ✅ | ❌ (fn leaked) | ❌ | ❌ | ✅ | ❌ | N/A | ❌ | FAIL |
| ch03 | ✅ | ✅ | ✅ | ❌ (dup) | ✅ | ✅ | ✅ | ✅ | ❌ | N/A | ✅ | FAIL |
| ch04 | ✅ | ❌ (title in P001) | ✅ | ✅ | ✅ | ❌ (4 missing) | ❌ | ❌ | ❌ | N/A | ❌ | FAIL |
| ch05 | ✅ | ✅ | ✅ | ❌ (3 dup) | ✅ | ✅ | ✅ | ✅ | ❌ | N/A | ✅ | FAIL |
| ch06 | ✅ | ✅ | ✅ | ❌ (2 dup) | ✅ | ✅ | ✅ | ✅ | ❌ | N/A | ✅ | FAIL |
| ch07 | ✅ | ✅ | ✅ | ❌ (2 dup) | ✅ | ✅ | ✅ | ✅ | ❌ | N/A | ✅ | FAIL |
| ch08 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ (OCR) | ❌ | N/A | ✅ | FAIL |
| ch09 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | N/A | ✅ | FAIL |
| ch10 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ (4 missing) | ❌ | ❌ | ❌ | N/A | ❌ | FAIL |
| ch11 | ✅ | ✅ | ✅ | ❌ (1 dup) | ✅ | ✅ | ✅ | ✅ | ❌ | N/A | ✅ | FAIL |
| ch12 | ✅ | ❌ (title+heading) | ❌ | ❌ | ❌ (inline fn) | ❌ (39 placeholder) | ❌ | ❌ | ❌ | N/A | ❌ | FAIL |
| ch13 | ✅ | ✅ | ✅ | ❌ (28 cross-page) | ✅ | ✅ | ✅ | ✅ | ❌ | N/A | ✅ | FAIL |

---

## 9. DEPENDENCIES AND EXECUTION SEQUENCE

### 9.1 Dependencies

| Dependency | Trạng thái | Ghi chú |
|---|---|---|
| `build_chapter_docx.py` | ✅ Có | Cần sửa logic footnote detection |
| `vnch_orthography.py` | ✅ Có | Trong `.kilo/scripts/common/` |
| `document_comparator.py` | ✅ Có | Trong `.kilo/scripts/common/` |
| `audit_docx_format.py` | ✅ Có | Trong `99_scripts/` |
| `STYLE_GUIDE_PHAN_B.md` | ✅ Có | Trong `07_style_guide/` |
| `ARENDT_TERMINOLOGY.md` | ✅ Có | Trong `03_terminology/` |
| Source PDF | ❓ Không rõ | progress.json ghi `books/Hannah-Arendt-...pdf`, cần xác nhận có file không |
| front_matter/prefaces/part intro translations | ❌ Chưa có | 6 section chưa có file dịch v2 |

### 9.2 Execution sequence (thứ tự ưu tiên)

```
Phase 0: Xác định scope và source of truth
  └─ Phải hoàn thành trước mọi sửa chữa

Phase 1: Sửa builder engine (build_chapter_docx.py)
  └─ Phải hoàn thành trước khi rebuild DOCX

Phase 2: Sửa dữ liệu translation (ch01-ch13, theo thứ tự ưu tiên)
  1. ch12 (CRITICAL - nhiều lỗi nhất)
  2. ch01, ch02 (CRITICAL - footnote content trong body)
  3. ch04, ch10 (CRITICAL - missing footnotes)
  4. ch03, ch05, ch06, ch07, ch11 (MAJOR - duplicate paragraphs)
  5. ch08 (MAJOR - OCR artifacts)
  6. ch09, ch13 (MAJOR - VNCH orthography, cross-page)

Phase 3: VNCH orthography & foreign fragments (tất cả chapter)

Phase 4: Rebuild DOCX + validation (tất cả chapter)

Phase 5: Quality gates + acceptance (tất cả chapter)
```

### 9.3 Checkpoint và rollback

| Checkpoint | File | Nội dung |
|---|---|---|
| CP-0 | `00_plan/progress.json` | Trạng thái thực tế trước khi sửa |
| CP-1 | `99_scripts/build_chapter_docx.py` (backup) | Builder trước khi sửa |
| CP-2 | Mỗi file `v1_chNN_vi.txt` trước khi sửa | Backup tại `99_scripts/backup/` |
| CP-3 | `00_plan/progress.json` sau mỗi chapter sửa | Trạng thái sau mỗi chapter |

**Quy tắc rollback:** Nếu sửa file vi.txt gây lỗi mới, khôi phục từ backup tại `99_scripts/backup/v1_chNN_vi.txt.<timestamp>`.

---

## 10. FINAL DELIVERABLES

| Deliverable | Mô tả | Trạng thái mục tiêu |
|---|---|---|
| 13 file DOCX | `09_docx/V2-01_*.docx` … `V2-13_*.docx` | Tất cả build bởi repaired builder |
| 13 file vi.txt repaired | `04_translation/v2/chNN/v1_chNN_vi.txt` | Không có footnote content trong body |
| progress.json updated | `00_plan/progress.json` | Tất cả chapter status = HOAN_TAT |
| Repair report | Báo cáo tổng kết lỗi đã sửa, còn sót | Lưu tại `99_scripts/` hoặc `05_qa/` |
| Quality gate results | Kết quả QG1-QG11 cho từng chapter | Tất cả PASS |

---

## 11. QUYẾT ĐỊNH CẦN USER PHÊ DUYỆT

| # | Vấn đề | Lựa chọn đề xuất | Ảnh hưởng |
|---|---|---|---|
| 1 | **Scope repair** | Chỉ repair 13 chapter (ch01-ch13), không bao gồm front_matter/prefaces/part intro (chưa có file dịch) | 6 section không được dịch trong giai đoạn này |
| 2 | **Footnote content in ch12** | Xóa 39 placeholder footnotes hoặc đánh dấu UNVERIFIED trong report | Nếu xóa, có thể mất thông tin; nếu giữ, đánh dấu UNVERIFIED |
| 3 | **Footnotes 72/154/158 missing anchors** (ch12) | Thêm body marker hoặc dokument là UNVERIFIED (không fabricate) | Cần user xác nhận source |
| 4 | **Builder changes** | Sửa `build_chapter_docx.py` hiện tại, không tạo builder mới | Tái sử dụng existing architecture |

---

## 12. TÓM TẮT PHÁT HIỆN THỰC TẾ

| Vấn đề | Đã xác minh | Chưa xác minh |
|---|---|---|
| Footnote content duplicated in body (ch01, ch02, ch12) | ✅ (đọc file trực tiếp) | — |
| Chapter title in body paragraph (ch01, ch02, ch04, ch12) | ✅ (đọc file trực tiếp) | — |
| Inline footnote duplicates (ch12, ¹³-²²) | ✅ (ROOT_CAUSE_REPAIR_REPORT.md) | — |
| Missing footnote definitions (ch04: 4, ch10: 4, ch12: fns 72/154/158) | ✅ (ROOT_CAUSE_REPAIR_REPORT.md) | — |
| Cross-page continuity issues (ch04: 8, ch12: 14, ch13: 28) | ✅ (FULL_13_CHAPTER_AUDIT.md) | — |
| Duplicate paragraphs (ch03, ch05, ch06, ch07, ch10, ch11) | ✅ (CHAPTER_AUDIT_MATRIX.md) | — |
| VNCH orthography errors (tất cả 13 chapter) | ✅ (CHAPTER_AUDIT_MATRIX.md) | — |
| Foreign language fragments (tất cả 13 chapter) | ✅ (TRANSLATION_REPORT.md) | — |
| Missing translations (front_matter, 4 prefaces, part intro) | ✅ (progress.json, CHAPTER_AUDIT_MATRIX.md) | — |
| Running headers misclassified as headings | ✅ (ROOT_CAUSE_REPAIR_REPORT.md) | — |

**File bản dịch cuối sẽ được xử lý:** `04_translation/v2/ch01/v1_ch01_vi.txt` … `ch13/v1_ch13_vi.txt` (13 file), với ưu tiên ch12, ch01, ch02, ch04, ch10.

**Builder sẽ được sửa:** `99_scripts/build_chapter_docx.py`.

**KHÔNG được tự động chuyển sang Execution Mode.** Kế hoạch này cần user phê duyệt trước khi bắt đầu thực thi.
