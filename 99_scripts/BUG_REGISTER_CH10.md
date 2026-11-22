# BUG REGISTER — CHƯƠNG 10: THE FRENCH INDOCHINA WAR IN NORTHERN VIETNAM
**Tác giả:** Christopher Goscha  
**Trang PDF:** 218-237 (PDF pages 234-253)  
**Ngày rà soát:** 2026-11-22  
**Phiên bản bản dịch:** v1_ch10_vi.txt (rebuild 2026-11-21)  
**Trạng thái:** CẦN SỬA — Chưa đạt Quality Gate  

---

## TỔNG QUAN LỖI

| Nhóm lỗi | Tổng số | CRITICAL | MAJOR | MINOR | Trạng thái |
|---|---|---|---|---|---|
| 1. Trích xuất/Nội dung | 4 | 2 | 1 | 1 | Chưa sửa |
| 2. Dịch thuật (Alignment) | 6 | 2 | 2 | 2 | Chưa sửa |
| 3. Thuật ngữ VNCH (Orthography) | 128 | 68 | 7 | 53 | Chưa sửa |
| 4. Cước chú/Tham chiếu | 3 | 1 | 1 | 1 | Chưa sửa |
| 5. Hình ảnh/Bản đồ | 2 | 1 | 1 | 0 | Chưa sửa |
| 6. Định dạng DOCX | 1 | 0 | 1 | 0 | Chưa sửa |
| **TỔNG CỘNG** | **144** | **74** | **13** | **57** | |

---

## CHI TIẾT LỖI THEO NHÓM

### NHÓM 1: LỖI TRÍCH XUẤT NỘI DUNG (Content Extraction)

| ID | Vị trí | Mô tả | Bằng chứng | Mức độ | Nguồn phát hiện |
|---|---|---|---|---|---|
| **CE-01** | P009 | Caption "Hình 10.1" bị nhúng trong paragraph P009 thay vì tách thành block PIMG1 riêng | Source P009 chứa caption "Figure 10.1..." cuối đoạn; VI đã tách thành PIMG1 (line 32) nhưng P009 vẫn còn chứa text dẫn dắt | CAO | User feedback trước + audit workflow §7A.7 |
| **CE-02** | P017 | Bản đồ Map 10.1: Source chứa toàn bộ labels map (70+ dòng) trong P017; VI chỉ dịch caption, không dịch labels (đúng) nhưng P017 VI có 0 câu | Source P017: 4 "sentences" (thực chất là labels); VI P017: 0 câu - alignment diff=-4 | TRUNG BÌNH | document_comparator |
| **CE-03** | P016/P016b | Source có 2 markers riêng (P016 heading + P016b content); VI cũng có 2 nhưng sentence count khác (src=2, vi=5) | P016 src="Of Rice and War" (0 câu); P016b src=2 câu. VI P016 heading + P016b=3 câu. Diff do heading được đếm. | THẤP | Alignment check |
| **CE-04** | P003 | Chapter title: Source có "Christopher Goscha" dưới title; VI đã bỏ tên tác giả (đúng theo workflow - không để tên tác giả lặp) | Source P003: "The French Indochina War in Northern Vietnam\nChristopher Goscha"; VI P003: chỉ "Chiến tranh Đông Dương của Pháp ở Bắc Việt Nam" | THẤP | Workflow §8A.5 |

---

### NHÓM 2: LỖI DỊCH THUẬT VÀ ALIGNMENT (Translation & Alignment)

| ID | Vị trí | Mô tả | Bằng chứng | Mức độ | Nguồn phát hiện |
|---|---|---|---|---|---|
| **TA-01** | P010 | **Thiếu 3 câu** (src=20, vi=17, diff=-3). Đoạn mở đầu trang 224: "a second Vietnamese army..." đến "he improved existing air bases..." | So sánh: Source có 20 câu bao gồm: VNA formation, fortifications, pacification, troop transfers, naval surveillance, air bases, barbed wire, US aid (artillery, shells, napalm, bombers, tanks, trucks, fuel, landing craft, radios), VNA financing, DRVN transformation, Giáp's plan, Vĩnh Yên attack. VI chỉ 17 câu - có thể gộp câu hoặc lược bỏ chi tiết. | **CRITICAL** | document_comparator |
| **TA-02** | P015 | **Thiếu 7 câu** (src=18, vi=11, diff=-7). Phân tích bài học Hòa Bình (4 lessons) | Source: 18 câu bao gồm 4 bài học chi tiết (French won't give up delta; rice supply concern; party control; terrain advantage + multiple options). VI: 11 câu - có thể đã gộp/ lược bỏ bài học thứ 3-4. | **CRITICAL** | document_comparator |
| **TA-03** | P019 | Thiếu 1 câu (src=10, vi=9, diff=-1). "Economic war"/"rice war" systematization | Source: 10 câu; VI: 9 câu. Có thể gộp "la bataille du riz" vào câu trước. | TRUNG BÌNH | Alignment check |
| **TA-04** | P025 | Thiếu 2 câu (src=14, vi=12, diff=-2). Phase 3 economic offensive | Source: 14 câu; VI: 12 câu. | TRUNG BÌNH | Alignment check |
| **TA-05** | P031 | Thiếu 1 câu (src=10, vi=9, diff=-1). French economic war high gear, hydraulic systems bombing | Source: 10 câu; VI: 9 câu. | TRUNG BÌNH | Alignment check |
| **TA-06** | P005 | Thừa 1 câu (src=7, vi=8, diff=+1). "Christopher Goscha 220" header được dịch thành câu? | Source có header "Christopher Goscha\n220" - không phải câu. VI có thể đã dịch header thành câu. | THẤP | Alignment check |

---

### NHÓM 3: LỖI THUẬT NGỮ VNCH (VNCH Orthography) — 128 lỗi từ `vnch_orthography.py`

#### 3.1 CRITICAL (68 lỗi) — Phải sửa trước khi HOAN_TAT

| Rule | Từ sai → Đúng | Số lượng | Ví dụ vị trí | Ghi chú |
|---|---|---|---|---|
| **VNCH-02** | chính phủ → chánh phủ | 3 | P008, P012, P013 | Core term |
| **VNCH-12** | này → nầy | 64 | Toàn bộ chương | **NHIỀU FALSE POSITIVE** - rule regex không loại trừ "trong này", "ngoài này", "trước này", "sau này" đúng cách. Cần review thủ công từng trường hợp. |
| **VNCH-26** | Indochina → Đông Dương (Indochina) | 1 | Header line 1 | Header metadata - không nên dịch |

**⚠️ PHÂN TÍCH VNCH-12:** 64 instance của "này" → "nầy" được flag. Tuy nhiên theo Style Guide Rule 4: "này" chỉ giữ trong cấu trúc "trong này", "ngoài này", "trước này", "sau này". Regex hiện tại `(?!.*(?:trong|ngoài|trước|sau)\s+nầy)` chỉ lookahead, không kiểm tra từ LIỀN TRƯỚC. Nhiều instance là "cái này", "việc này", "điều này" → đúng phải thành "nầy". Nhưng "trong này" (line 29), "từ thời điểm này" (line 33) - "từ thời điểm" không trong exception list. Cần kiểm tra từng case.

#### 3.2 MAJOR (7 lỗi)

| Rule | Từ sai → Đúng | Số lượng | Vị trí | Ghi chú |
|---|---|---|---|---|
| **VNCH-10** | giải phóng → độc lập/kháng cự | 1 | P006 (trong trích dẫn "giải phóng miền nam Pháp năm 1944") | **Trong trích dẫn tiếng Pháp** - Rule 15: trích dẫn giữ nguyên |
| **VNCH-16** | hơn nữa → vả/lại | 1 | P019 footnote area | "trở nên tồi tệ hơn nữa" |
| **VNCH-25** | Indochine → Đông Dương (Indochine) | 4 | Footnotes [13], [6], [7], [8] | **Trong tên sách/trích dẫn Pháp** - Rule 15: giữ nguyên, thêm VNCH trong ngoặc |

#### 3.3 MINOR (53 lỗi) — Grammar Engine Rules

| Rule | Mô tả | Số lượng | Ghi chú |
|---|---|---|---|
| **VNCH-27** | Thiếu classifier ("một năm", "một người") | 7 | "một năm 1946", "một năm 1951", "một người" - Style Guide Rule 21 |
| **VNCH-28** | "sau này" → "sau nầy" | 1 | Position 40386 |
| **VNCH-29** | Thể khía "đang..." không hoàn chỉnh | 13 | "đang diễn ra", "đang làm", "đang sống", "đang mở rộng", "đang đợi", "đang nhảy", "đang mở rộng", "đang kín", "đang đến", "đang đi", "đang ở", "đang tăng", "đang chuyển" - Style Guide Rule 23 |
| **VNCH-30** | Đại từ "nó" chỉ vật/sự việc | 19 | "Nó không phải là", "nó ám chỉ", "Nó gia nhập", "Nó cũng đã biến đổi", "mục tiêu chính của nó", "của nó", "nó phải sẵn sàng", "nó gây ra", "nó một khu rừng", "nó sẽ sống sót", "nó với thủ đô", "nó là" (x2), "nó cũng là", "nó. Các sĩ quan", "nó với các nỗ lực", "nó. Kích thích", "nó. Cuối cùng", "biến nó thành", "Nó đã trở thành", "người là" (false positive), "nó, xem Hew Strachan" (false positive) |

---

### NHÓM 4: LỖI CỤC CHÚ VÀ THAM CHIẾU (Footnotes & References)

| ID | Vị trí | Mô tả | Bằng chứng | Mức độ |
|---|---|---|---|---|
| **FN-01** | P009/P010 | Footnote [3] referenced tại cuối P009 source ("Americans.[3]") nhưng VI P009 không có marker [3], chuyển sang P010 | Source P009 ends with "[3]"; VI P009 không có "[3]", VI P010 bắt đầu với "[3]" | CAO |
| **FN-02** | Footnotes section | 4 instance "Indochine" trong footnotes [6], [7], [8], [13] bị flag VNCH-25 | Footnotes chứa "Histoire de la guerre d'Indochine" - tên sách tiếng Pháp, Rule 15: giữ nguyên | TRUNG BÌNH |
| **FN-03** | P032 | Trích dẫn Chassin: French text "Il faut faire crever les gens de faim" được giữ nguyên (đúng), nhưng footnote [19] URL có "general-chassin-pdf-edit.pdf" | Footnote [19] format OK | THẤP |

---

### NHÓM 5: HÌNH ẢNH VÀ BẢN ĐỒ (Images & Maps)

| ID | Vị trí | Mô tả | Bằng chứng | Mức độ |
|---|---|---|---|---|
| **IMG-01** | PIMG1 (Figure 10.1) | VI có block PIMG1 riêng (line 32) - **ĐÚNG** theo workflow §7A.7. Source không có PIMG1 riêng (caption nhúng trong P009). | image_manifest.json: v1-C10-IMG001 (raster, pdf_page 239, printed 223). DOCX audit: "Images: 2 | Captions: 0" - caption count 0 là do script audit không nhận diện caption format. | TRUNG BÌNH |
| **IMG-02** | PIMG2 (Map 10.1) | VI có block PIMG2 riêng (line 60) - **ĐÚNG**. Source P017 chứa toàn bộ map labels (không tách caption). | image_manifest.json: v1-C10-IMG002 (vector_figure_rasterized, pdf_page 245, printed 229, 113 drawings). Map labels KHÔNG dịch (đúng), chỉ dịch caption. | TRUNG BÌNH |

**Lưu ý:** `audit_docx_format.py` báo "Images: 2 | Captions: 0" - script audit chỉ đếm caption nếu paragraph bắt đầu bằng "Hình X.Y" hoặc "Bản đồ X.Y". PIMG1/PIMG2 trong VI format là "Hình 10.1 — ..." và "Bản đồ 10.1 — ..." nên nên được nhận. Cần kiểm tra script audit.

---

### NHÓM 6: DEFIN FORMAT DOCX (DOCX Formatting)

| ID | Vị trí | Mô tả | Bằng chứng | Mức độ |
|---|---|---|---|---|
| **DF-01** | Toàn bộ DOCX | `audit_docx_format.py` PASS tất cả format checks, nhưng **Caption count = 0** (Images: 2 | Captions: 0). Script `build_chapter_docx.py` hinh_pattern có thể không khớp caption format "Hình 10.1 — ..." (em dash vs hyphen). | TRUNG BÌNH |

---

## PHÂN LOẠI THEO NGUỒN PHÁT HIỆN

### A. LỖI USER ĐÃ PHẢN ÁNH (TỪ SESSION TRƯỚC) — ĐÃ SỬA NHƯNG CẦN KIỂM TRA LẠI

| ID | Lỗi gốc | Trạng thái sau sửa | Cần verify |
|---|---|---|---|
| U-01 | P004 thiếu label "đề mục" | ✅ Đã thêm "— đề mục ---" | Kiểm tra DOCX heading render |
| U-02 | P009 caption nhúng trong paragraph | ✅ Đã tách PIMG1 | Kiểm tra DOCX image+caption position |
| U-03 | P028 thiếu đoạn (source P028: air force attack buffalo/markets/transport) | ✅ Đã bổ sung P028 | Kiểm tra alignment P028-P033 |
| U-04 | P030: "than r" garbled, Chassin quote nhúng, "vật nặng" | ✅ Đã sửa: "kinh hoàng", tách quote, "trâu bò" | Verify quote block P032 |
| U-05 | P023: "quan lý" → "quản lý" | ✅ Đã sửa | OK |
| U-06 | P015: "chiến lược đánh giá cao" → "được tính toán cẩn thận", "đưa ra" → "triển khai" | ✅ Đã sửa | OK |
| U-07 | P026: "linh hồn" → "người", "chu lip" → "không để lời lửng" | ✅ Đã sửa | OK |
| U-08 | P029: "đê, đê" → "đê, đamb" | ✅ Đã sửa | OK |
| U-09 | P032: "đẻ" → "đê" (2 lần) | ✅ Đã sửa | OK |

### B. LỖI MỚI PHÁT HIỆN TRONG RÀ SOÁT NÀY

| ID | Nhóm | Mô tả | Mức độ |
|---|---|---|---|
| **NEW-01** | TA | P010 thiếu 3 câu (alignment diff=-3) | **CRITICAL** |
| **NEW-02** | TA | P015 thiếu 7 câu (alignment diff=-7) | **CRITICAL** |
| **NEW-03** | VNCH | 64 instance "này" → "nầy" (VNCH-12) - cần review false positive | **CRITICAL** |
| **NEW-04** | VNCH | 3 instance "chính phủ" → "chánh phủ" (VNCH-02) | **CRITICAL** |
| **NEW-05** | VNCH | 7 instance thiếu classifier "một năm", "một người" (VNCH-27) | MINOR |
| **NEW-06** | VNCH | 13 instance thể khía "đang..." không hoàn chỉnh (VNCH-29) | MINOR |
| **NEW-07** | VNCH | 19 instance đại từ "nó" (VNCH-30) - nhiều false positive | MINOR |
| **NEW-08** | FN | Footnote [3] position shift từ P009 sang P010 | CAO |
| **NEW-09** | IMG | Caption count = 0 trong audit (script hinh_pattern issue) | TRUNG BÌNH |
| **NEW-10** | TA | P019, P025, P031 minor sentence mismatch | TRUNG BÌNH |

---

## NGUYÊN NHÂN GỐC (Root Cause Analysis)

### 1. VNCH Orthography Rules (vnch_orthography.py) - FALSE POSITIVE CAO
- **VNCH-12 (này→nầy)**: Regex lookahead `(?!.*(?:trong|ngoài|trước|sau)\s+nầy)` chỉ kiểm tra xuất hiện SAU, không kiểm tra từ LIỀN TRƯỚC. "trong này" match vì "trong" xuất hiện trước "này" trong lookahead. Cần sửa regex thành negative lookbehind hoặc kiểm tra word boundary trước "này".
- **VNCH-29 (đang...)**: Pattern `\bđang\s+\w+(?!\s+(xong|tiến hành|đang))` quá rộng - bắt tất cả "đang + động từ" trừ 3 từ. VNCH cho phép "đang" đơn độc cho thể khía tiến hành. Cần refine rule.
- **VNCH-30 (nó)**: Pattern `\b(hắn|y|nó)\b.*?(?:lập luận|nói|cho rằng|tin rằng|là)` match quá xa (.*? greedy). "nó" làm chủ ngữ chỉ vật ("nó không phải là", "mục tiêu của nó") bị false positive. Cần giới hạn distance.

### 2. Translation Process - ALIGNMENT LOSS
- **P010, P015**: Sentence count diff lớn (-3, -7) cho thấy dịch gộp câu hoặc lược bỏ thông tin. Grammar Engine Bước 6 (đối chiếu số câu) không được thực hiện kỹ.
- **Root cause**: Không chạy `document_comparator.py` sau khi dịch xong mỗi chương. Workflow §8 Bước 6 yêu cầu đối chiếu alignment.

### 3. Image Caption Handling
- **Source**: Caption nhúng trong paragraph (P009, P017)
- **VI**: Tách ra thành PIMG1, PIMG2 - **ĐÚNG** theo workflow §7A.7
- **Issue**: `audit_docx_format.py` không đếm caption do pattern mismatch. Script `build_chapter_docx.py` dùng `hinh_pattern` có thể không khớp "Hình 10.1 —" (em dash).

### 4. Footnote Marker Drift
- **FN-01**: Marker [3] ở cuối P009 source, nhưng VI chuyển sang đầu P010. Do source P009 kết thúc bằng "[3]" sau "Americans.", nhưng VI P009 tách caption ra PIMG1 khiến marker [3] bị đẩy. Cần neo marker [3] đúng vị trí trong P009 VI.

---

## KẾ HOẠCH SỬA CHỮA (Remediation Plan)

### Phase 1: CRITICAL - Phải sửa trước Quality Gate
1. **Fix VNCH-02**: Thay "chính phủ" → "chánh phủ" (3 chỗ) - Dùng `apply_vnch_fixes.py` hoặc sửa thủ công
2. **Fix VNCH-12**: Review 64 instance "này" → "nầy" thủ công, chỉ sửa khi KHÔNG phải "trong này/ngoài này/trước này/sau này". Cập nhật regex trong vnch_orthography.py.
3. **Fix Alignment P010**: So sánh câu-by-câu, bổ sung 3 câu thiếu.
4. **Fix Alignment P015**: So sánh câu-by-câu, bổ sung 7 câu thiếu (4 bài học Hòa Bình).
5. **Fix FN-01**: Di chuyển marker [3] từ đầu P010 về cuối P009 VI.

### Phase 2: MAJOR - Sửa trước HOAN_TAT
6. **Fix VNCH-16**: "hơn nữa" → "vả" (1 chỗ P019)
7. **Fix VNCH-25/26**: Footnotes "Indochine"/"Indochina" - thêm "(Indochine)" sau "Đông Dương" hoặc giữ nguyên theo Rule 15
8. **Fix VNCH-10**: "giải phóng" trong trích dẫn - giữ nguyên, thêm ghi chú
9. **Fix IMG-01/02**: Kiểm tra `build_chapter_docx.py` hinh_pattern, đảm bảo caption render đúng vị trí.

### Phase 3: MINOR - Polish
10. **VNCH-27**: Thêm classifier cho "một năm" → "một năm đó/năm ấy" hoặc "một năm 1946" (đã có năm) - review each
11. **VNCH-28**: "sau này" → "sau nầy"
12. **VNCH-29**: Review 13 instance "đang..." - nhiều là đúng ngữ pháp VNCH (thể khía tiếp diễn), không phải lỗi. Cập nhật rule.
13. **VNCH-30**: Review 19 instance "nó" - phần lớn là chủ ngữ chỉ vật/sự việc, đúng VNCH. Cập nhật rule.

---

## TIÊU CHÍ PASS/FAIL CHO QUALITY GATE (Theo translation-quality-gate skill)

| # | Tiêu chí | Trạng thái hiện tại | Cần làm gì |
|---|---|---|---|
| 1 | Encoding UTF-8/NFC/no BOM/LF | ✅ PASS | - |
| 2 | Orthography: 0× "chính trị", 0× từ miền Bắc | ❌ FAIL | Fix VNCH-02, VNCH-12, VNCH-25/26 |
| 3 | Đồng bộ đoạn: src = vi | ⚠️ PARTIAL | 33/33 đoạn OK, nhưng sentence count mismatch P010, P015 |
| 4 | Đồng bộ cước chú: src = vi | ⚠️ PARTIAL | 19/19 footnotes OK, nhưng marker [3] drift |
| 5 | Không fabricate | ✅ PASS | - |
| 6 | Văn phong tự nhiên (S1-S20, P1-P10) | ❌ FAIL | Fix alignment, VNCH grammar issues |
| 6b | VLP-01 Tiếng Việt trước | ⚠️ PARTIAL | Còn "Indochina" trong header, "Indochine" trong footnotes |
| 7 | DOCX tồn tại 09_docx/ | ✅ PASS | - |
| 8 | DOCX cước chú: OK N/N, Word Footnotes.Count | ⚠️ UNVERIFIED | Cần Word COM verify |

---

## KẾT LUẬN

**Chương 10 CHƯA ĐẠT CHUẨN HOÀN_TẤT.** 

Các vấn đề nghiêm trọng nhất:
1. **Alignment loss tại P010 (-3 câu) và P015 (-7 câu)** - mất thông tin quan trọng (bài học Hòa Bình)
2. **VNCH orthography 68 CRITICAL** - chủ yếu false positive VNCH-12 ("này"→"nầy") nhưng có 3 instance thực sự sai "chính phủ"
3. **Footnote marker [3] drift** - vi phạm alignment footnote

**Khuyến nghị:** KHÔNG ĐÁNH DẤU HOÀN_TẤT cho đến khi Phase 1 và 2 hoàn tất và Quality Gate PASS.

---

## FILES LIÊN QUAN

- Source: `translation-project/04_translation/v1/ch10/v1_ch10_src.txt`
- Translation: `translation-project/04_translation/v1/ch10/v1_ch10_vi.txt`
- DOCX: `translation-project/09_docx/V1-C10_The-French-Indochina-War-in-Northern-Vietnam.docx`
- Image manifest: `translation-project/00_plan/image_manifest.json` (v1-C10-IMG001, v1-C10-IMG002)
- Progress: `translation-project/00_plan/progress.json` (V1-C10 entry)
- VNCH issues detail: `vnch_issues_detail.txt`
- Alignment check: `alignment_check.txt`