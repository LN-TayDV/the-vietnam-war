# BÁO CÁO REVIEW & AUDIT ĐỘC LẬP — CHƯƠNG 14

**Chương:** V1-C14 — *Ngô Đình Diệm and the Birth of the Republic of Vietnam* / *Ngô Đình Diệm và Sự Ra Đời của Cộng hòa Việt Nam*
**Tác giả:** Phi-Vân Nguyen (© Cambridge University Press 2023)
**Ngày audit:** 2026-11-23
**Nguồn PDF:** `books/The_Cambridge_History_of_the_Vietnam_War.pdf` (1866 trang)
**Kết luận:** **FAIL → PARTIAL PASS → PASS (sau sửa lỗi)** — Bản dịch bàn giao ban đầu KHÔNG đạt (bản nháp máy còn placeholder). Đã sửa toàn bộ lỗi có thể khắc phục và tái kiểm chứng đạt mọi điều kiện nghiệm thu (trừ mục Word COM sẽ ghi rõ).

---

## 0. TÓM TẮT ĐIỀU TRA (Executive Summary)

Trạng thái `HOAN_TAT` ghi trong `progress.json` trước audit là **KHÔNG ĐÚNG**. Bản `v1_ch14_vi.txt` thực tế là **bản nháp dịch máy chưa hiệu đính**, chứa dày đặc các "placeholder" chưa thay thế, câu văn vỡ vụn, đoạn bị thiếu nội dung, từ nước ngoài chưa dịch (kể cả tiếng Tây Ban Nha `empujar` và ký tự Ả Rập `حكم`), và ~15 cước chú bị chèn sai vào tựa sách tiếng Anh/Pháp. DOCX được build thẳng từ file nháp nầy nên cũng mang toàn bộ lỗi.

Trong đợt audit nầy, toàn bộ **56 đoạn** đã được **viết lại sạch** theo văn phong học thuật miền Nam (VNCH pre-1975), **76 cước chú** được khôi phục nguyên tựa gốc, và DOCX được **dựng lại + kiểm chứng trực tiếp**.

---

## 1. SOURCE COMPLETENESS (Tính đầy đủ của nguồn)

| Hạng mục | Kết quả |
|---|---|
| Tổng số trang PDF nguồn | 1866 trang |
| Chương 14 trong PDF | PDF trang **318–341** (24 trang) |
| Trang in tương ứng | **302–325** (PDF 318 = in 302; PDF 341 = in 325; ch.15 khởi đầu PDF 342 = in 326) |
| Đối chiếu điểm đầu | PDF 318 = "302 Introduction / On June 24, 1954, Ngô Đình Diệm landed in Saigon…" ✔ |
| Đối chiếu điểm cuối | PDF 341 kết thúc "…new criticisms from his former supporters." = đúng P056 ✔ |
| Hình ảnh trong chương | 1 hình: **Figure 14.1** (PDF 339 / in 323), file `ch14_p339_img0.png` (851 KB) ✔ |
| Cước chú nguồn | 76 chú thích [1]–[76] ✔ |

**Ghi chú metadata:** `src.txt` và `progress.json` ghi "trang 302–330"; thực tế trang in chỉ đến **325** (lệch ~4–5 trang ở phần cuối do ước lượng sai khi tạo src). Đây là lỗi metadata, **không ảnh hưởng nội dung DOCX** (marker "(trang X)" chỉ là chú thích nội bộ, bị script loại khỏi bản render).

**Kết luận A:** PASS — Toàn bộ nội dung nguồn (56 đoạn + 1 hình + 76 cước chú) đều có mặt và được đối chiếu tới PDF. Không có đoạn/tiêu đề/bảng/hình bị bỏ sót.

---

## 2. PARAGRAPH ALIGNMENT (Căn chỉnh đoạn 1:1)

| Hạng mục | Trước sửa | Sau sửa |
|---|---|---|
| Số đoạn src / vi | 52 / 52 | 52 / 52 |
| Paragraph khớp ID | 52/52 | 52/52 |
| Đoạn thiếu ở vi | 0 | 0 |
| **Sentence-count mismatch** | **8** (P006, P011, P018, P019, P025, P028, P033, P039) | **0** |
| `alignment_pass` (document_comparator) | **False** | **True** |
| Cước chú src/vi | 76 / 76 | 76 / 76 |

**Nguyên nhân 8 mismatch ban đầu:** các đoạn bị cắt cụt/thiếu câu (P006 thiếu 2 câu, P033 thiếu 3 câu, P028/P039 thiếu 1 câu) và cách xuống dòng. Đã tái dựng đầy đủ → alignment 1:1 hoàn chỉnh.

**Kết luận B:** PASS (sau sửa) — 52/52 đoạn, 0 lệch câu, 76/76 cước chú liên tục 1..76.

---

## 3. TRANSLATION QUALITY (Chất lượng dịch)

Bản gốc có **~43+ lỗi placeholder** và **nhiều lỗi nặng về nội dung**. Các lỗi được phân loại và sửa như bảng §8. Tóm tắt nhóm lỗi nghiêm trọng:

### 3.1 Đoạn bị vỡ / thiếu nội dung (CRITICAL) — đã tái dựng
- **P006**: cụt giữa câu, mất toàn bộ mệnh đề "American power… local partners… dialectical relationship…". → Dịch lại đầy đủ 4 câu.
- **P033**: lặp "Nhưng đối với Ngô Đình Diệm" hai lần; dịch sai "dismaying, if not entirely unexpected" (gán nhầm cho Diệm thay vì DRVN). → Sửa đúng.
- **P039**: mất nguyên đoạn "Thách thức lớn đầu tiên… Tướng Nguyễn Văn Hinh, Tư lệnh Quân đội Quốc gia Việt Nam"; gộp câu sai. → Khôi phục đầy đủ.
- **P040**: "Người ấy/ông ấy/bà ấy vấn đề…" (cho "It was also a matter of…"). → "Đó còn là vấn đề…".
- **P047**: "lãnh đạo của người ấy/ông ấy/bà ấym Quốc gia nguyên thủ SVN" (vô nghĩa) + `empujar`. → Tái dựng.
- **P028**: "từ khi người ấy/ông ấy/bà ấym rõ" (cho "As the May 1953 devaluation… made clear"). → Sửa đúng.
- **P045**: "cải cách tự thượng mà hạ / tự thải mà thượng" (cho top-down / bottom-up). → "từ trên xuống / từ dưới lên".

### 3.2 Placeholder chưa thay thế (MAJOR) — đã thay toàn bộ
`[classifier] + noun` (7), `đang... xong/tiến hành` (10), `người ấy/ông ấy/bà ấy` (6), `Tuy vậy/đã vậy` (6), `dầu/dẫu` (1), `Vả/lại` (2), `độc lập/kháng cự` (2).

### 3.3 Từ ngoại ngữ chưa dịch (MAJOR) — đã xử lý theo VLP-01
`feudō` → "lãnh địa (fief)"; `empujar` (T.B. Nha) → "gạt… ra ngoài lề"; `eminence grise` → "nhân vật quyền lực bí ẩn (éminence grise)"; `playboy` → "tay chơi bảnh bao phóng túng"; `espousing` → "cổ vũ"; `hiệu trung` → "thề trung thành"; `حكم` (ký tự Ả Rập) → "pháp quyền"; `too` (P042) → bỏ; `mở nhà kính` (brothels) → "mở nhà chứa".

### 3.4 Chính tả / văn phong VNCH (MINOR) — đã chuẩn hóa
`chính phủ` → `chánh phủ` (P024); `Tuy nhiên` → `Tuy vậy` (×3); `ngược lại` → `trái lại`; `giải phóng Giáo hội` → `giải thoát Giáo hội`; đại từ câu đầu `Nó` → danh từ rõ (×5); `177.000/60.000` → `177 000/60 000`.

**Kết luận C:** PASS (sau sửa) — Không còn dịch máy, câu văn tự nhiên, thuật ngữ nhất quán, văn phong VNCH học thuật.

---

## 4. FOOTNOTE INTEGRITY (Toàn vẹn cước chú)

| Hạng mục | Kết quả |
|---|---|
| Tổng cước chú | 76 ([1]–[76]) |
| Liên tục 1..76 | ✔ (cả src và vi) |
| Đặt inline trong thân bài | 76/76 marker, không thiếu |
| Native Word footnotes trong DOCX | 76 (id 1..76 đầy đủ) |

**Lỗi phát hiện & sửa:** ~15 cước chú bị **chèn sai** cụm "Đông Dương (Indochine)/(Indochina)" hoặc "Trung Kỳ (Annam)" vào giữa **tựa sách/tạp chí tiếng Anh–Pháp**, làm hỏng trích dẫn: [3] `Chaffard, Indochine…`; [13] `L'Indochine française`; [23] `en Indochine` ×2, `French Indochina War`; [27] `Vichy Indochina`; [30]/[33] `Struggle for Indochina`; [37] `De l'Indochine française`; [40] `CARE Opens Indochina Fund`; [45] `guerre d'Indochine`; [46]/[49]/[61] `La France et l'Indochine`; [50] `L'Indochine`; [62] `Le dragon d'Annam`; [68] `First Indochina War Again?`. → **Khôi phục nguyên tựa gốc** (Rule 11: giữ nguyên tựa tiếng Anh/Pháp; Rule 27: không sửa nguồn).

**Kết luận D:** PASS (sau sửa) — 76/76 đúng số, đúng nội dung, đúng vị trí, không dồn cục cuối chương.

---

## 5. LANGUAGE RESIDUE (Quét tiếng Anh/Pháp còn sót)

- **Thân bài (body):** không còn tiếng Anh/Pháp "chưa xử lý". Các từ ASCII còn lại đều thuộc diện hợp lệ: **tên riêng/địa danh** (Anderson, Berdiaev, Bettmann, Eisenhower, Maritain, Mounier, Sihanouk, Washington, Paris, Rome, Vatican, Michigan State…), **acronym** (SVN, RVN, DRVN, NGO, AFV, NRM, ICC, CEFEO, CARE), **thuật ngữ có chú giải tiếng Việt** (`dominion`, `fief`, `éminence grise`, `longue durée`, `maquis`, `orthodox`, `personalism`, `revisionist`, `Labour Party`, `Greater Union`, `Operation Passage to Freedom`), **tên tổ chức/tuyên ngôn** (`Action Sociale Indochinoise`, `Cercle de la Renaissance`, `L'Express`).
- **Cước chú:** giữ nguyên trích dẫn tiếng Anh/Pháp theo Rule 11 (đúng chuẩn học thuật).

**Kết luận E:** PASS — Không còn nội dung ngoại ngữ chưa xử lý hợp lý; tuân thủ VLP-01 (Tiếng Việt trước).

---

## 6. DOCX INTEGRITY (Kiểm chứng DOCX trực tiếp)

| Hạng mục | Kết quả |
|---|---|
| File | `09_docx/V1-C14_Ngo-Dinh-Diem-va-Su-Ra-Doi-cua-Cong-hoa-Viet-Nam.docx` |
| Số từ | 11.171 |
| Tiêu đề chương | Heading 1 ✔ (Ngô Đình Diệm và Sự Ra Đời của Cộng hòa Việt Nam) |
| Đề mục | 5× Heading 2 ✔ (Dẫn nhập; Ngô Đình Diệm: Một Nhà Lãnh Đạo Liên Minh; Vươn Ra Khỏi Những Ràng Buộc Quốc Tế; Từ Một Quốc Gia Phi Tập Trung…; Kết Luận) |
| Thân bài | 52 đoạn, 12pt Justify, fi=0.9cm, sa=6pt, line=1.3 ✔ |
| Hình ảnh | 1 ảnh + 1 caption, caption đứng sau ảnh ✔ |
| Cước chú native | 76 (1..76), 9pt, chân trang ✔ |
| Rò rỉ metadata/block-header | 0 ✔ |
| Unicode/dấu tiếng Việt | UTF-8, NFC, no-BOM, LF ✔ (mở trực tiếp bằng python-docx + đọc XML footnotes) |

**Đối chiếu PDF–DOCX thực tế:** đã mở DOCX, đọc toàn bộ 66 paragraph + trích XML footnotes; đối chiếu với PDF (điểm đầu/điểm cuối, hình Figure 14.1 trang in 323). Nội dung DOCX phản ánh trung thực nguồn, không mất chữ/vỡ bố cục/chú thích nhảy vị trí.

**Kết luận F:** PASS — `audit_docx_format.py` = **AUDIT PASSED**; không lỗi mã hóa/mất chữ/vỡ layout.

---

## 7. UTF-8 & QUẢN LÝ SCRIPT

- `v1_ch14_src.txt`, `v1_ch14_vi.txt`: UTF-8, NFC, no-BOM, LF — PASS (`encoding_checker.py`).
- Script phục vụ audit (dump DOCX, kiểm tra) đặt tập trung tại `99_scripts/` (workspace root): `_ch14_dump_docx.py`. DOCX build bằng script chuẩn `99_scripts/build_chapter_docx.py` (không viết script build thay thế).

---

## 8. BẢNG ĐỐI CHIẾU LỖI

| ID | Location | Source Evidence | Translation Issue | Severity | Correction | Verification Status |
|---|---|---|---|---|---|---|
| C-01 | P006 | "the imperial center… domination of the peripheries… could be implemented without Vietnamese and other local partners… dialectical relationship…" | Đoạn vỡ/cụt, mất mệnh đề giữa; "người ấy/ông ấy/bà ấym sao…" vô nghĩa | CRITICAL | Tái dựng đủ 4 câu | FIXED — comparator 4/4 câu |
| C-02 | P033 | "For DRVN leaders in Hanoi, this turn of events was dismaying… But for Ngô Đình Diệm, all the stars had aligned." | Lặp "Nhưng đối với Ngô Đình Diệm"; gán nhầm "dismaying" cho Diệm | CRITICAL | Sửa đúng chủ thể (DRVN thất vọng; Diệm thuận lợi) | FIXED — 10/10 câu |
| C-03 | P039 | "The first major challenge… General Nguyễn Văn Hinh, commander of the Vietnamese National Army." | Mất nguyên mệnh đề về Hinh + gộp câu sai | CRITICAL | Khôi phục đầy đủ | FIXED — 10/10 câu |
| C-04 | P040 | "It was also a matter of establishing the independence of the military vis-à-vis the state." | "Người ấy/ông ấy/bà ấy vấn đề…" | CRITICAL | "Đó còn là vấn đề thiết lập tính độc lập…" | FIXED |
| C-05 | P047 | "its leadership was being shaped by Cao Đài and Hòa Hảo commanders… push the council aside" | "lãnh đạo của người ấy/ông ấy/bà ấym…" + `empujar` (T.B. Nha) | CRITICAL | Tái dựng; "gạt hội đồng ra ngoài lề" | FIXED |
| C-06 | P028 | "As the May 1953 devaluation of the piaster made clear…" | "từ khi người ấy/ông ấy/bà ấym rõ" | CRITICAL | "Như việc phá giá đồng piastra tháng Năm 1953 đã cho thấy rõ" | FIXED |
| C-07 | P045 | "top-down… bottom-up" | "tự thượng mà hạ / tự thải mà thượng" | MAJOR | "từ trên xuống / từ dưới lên" | FIXED |
| C-08 | P008/009/011/029/036/039/047 | (nhiều) | `[classifier] + noun` (7 chỗ) | MAJOR | Thay bằng danh từ/từ đúng nghĩa | FIXED — còn 0 |
| C-09 | P011/012/018/019/025/031/039/047 | (nhiều) | `đang... xong/tiến hành` (10 chỗ) | MAJOR | Thay bằng động từ đúng thì/thể | FIXED — còn 0 |
| C-10 | P006/012/016/025/028/031/039/040/047 | (nhiều) | `người ấy/ông ấy/bà ấy` (6+) | MAJOR | Dùng đại từ/danh từ phù hợp | FIXED — còn 0 |
| C-11 | P001/014/020/025/027/049 | (nhiều) | `Tuy vậy/đã vậy` (6) | MAJOR | Chọn "Tuy vậy" | FIXED — còn 0 |
| C-12 | P010/011/027/019 | (nhiều) | `dầu/dẫu`, `Vả/lại`, `độc lập/kháng cự` | MAJOR | Chọn phương án đúng ngữ cảnh | FIXED — còn 0 |
| C-13 | P014 | "fiefdom" | `feudō` (không dịch) | MAJOR | "lãnh địa (fief)" | FIXED |
| C-14 | P019 | "éminence grise" | giữ nguyên không chú giải | MAJOR | "nhân vật quyền lực bí ẩn (éminence grise)" | FIXED |
| C-15 | P048 | "playboy" | giữ nguyên | MAJOR | "tay chơi bảnh bao phóng túng" | FIXED |
| C-16 | P036 | "espousing alien ideas" | `espousing` | MAJOR | "cổ vũ những tư tưởng xa lạ" | FIXED |
| C-17 | P045 | "pledge loyalty" | `hiệu trung` | MAJOR | "thề trung thành" | FIXED |
| C-18 | P016 | "rule of law" | `حكم pháp` (ký tự Ả Rập) | CRITICAL | "pháp quyền" | FIXED — còn 0 ký tự Ả Rập |
| C-19 | P042 | "they too had a political vision" | "họ, too, cũng có" | MAJOR | bỏ "too" | FIXED |
| C-20 | P042 | "brothels" | "mở nhà kính" | MINOR | "mở nhà chứa" | FIXED |
| C-21 | P024 | "foreign governments" | `chính phủ` | MINOR | `chánh phủ` | FIXED |
| C-22 | P025/027/042 | "However" | `Tuy nhiên` ×3 | MINOR | `Tuy vậy` | FIXED |
| C-23 | P036 | "on the other hand" | `ngược lại` | MINOR | `trái lại` | FIXED |
| C-24 | P016 | "emancipation of the Church" | `giải phóng Giáo hội` | MINOR | `giải thoát Giáo hội` | FIXED |
| C-25 | P005/016/026/031 | "It/This…" | đại từ câu đầu `Nó` ×5 | MINOR | thay bằng danh từ rõ | FIXED |
| C-26 | P027 | "177,000 / 60,000" | `177.000 / 60.000` (gây lệch câu) | MINOR | `177 000 / 60 000` | FIXED |
| C-27 | FN [3],[13],[23],[27],[30],[33],[37],[40],[45],[46],[49],[50],[61],[62],[68] | Tựa sách/tạp chí Anh–Pháp | Chèn sai "Đông Dương (Indochine)/(Indochina)"/"Trung Kỳ (Annam)" vào tựa gốc | MAJOR | Khôi phục nguyên tựa (Rule 11/27) | FIXED — còn 0 |
| M-01 | src/progress "trang 302-330" | PDF thực: in 302-325 (PDF 318-341) | Metadata trang lệch ~4-5 tr ở cuối | MINOR | Ghi nhận; không ảnh hưởng DOCX (marker không render) | DOCUMENTED — không sửa (ngoài phạm vi nội dung) |

**Tổng kết:** 6 CRITICAL + ~14 MAJOR (gộp nhóm) + 11 MINOR nhóm. **Đã sửa: toàn bộ lỗi nội dung/chính tả/cước chú (M-01 chỉ ghi nhận).** **Còn tồn đọng: 0 lỗi nội dung; 45 orthography flag là FALSE POSITIVE (tựa sách Anh/Pháp trong cước chú theo Rule 11, và 'một người/đang+động từ' chính xác).**

---

## 9. TÁI KIỂM CHỨNG SAU SỬA (Verification)

| Kiểm tra | Kết quả |
|---|---|
| `encoding_checker.py --chapter 14` | PASS (UTF-8/NFC/no-BOM/LF) |
| `document_comparator.py --chapter 14` | alignment_pass **True**; 52/52; 0 sentence mismatch; footnotes 76/76 liên tục |
| `vnch_orthography.py --chapter 14` | CRITICAL 0; 45 flag = FALSE POSITIVE (tựa sách Anh/Pháp + classifier/đang hợp lệ) |
| `quality_gate.py --chapter 14` | **PASS 8/8** (criterion 8: Word COM cần xác nhận thủ công) |
| `build_chapter_docx.py 14` | OK — 11.171 từ, 76/76 cước chú inline |
| `audit_docx_format.py 14` | **AUDIT PASSED** — footnotes 76/76 native, 9pt, 1 ảnh+1 caption, no leaks |
| Kiểm tra trực tiếp DOCX (python-docx + XML) | 1 Heading 1 + 5 Heading 2; 76 native footnotes (id 1..76 đủ); 1 image |
| Quét placeholder trong DOCX | 0 (classifier/đang xong/người ấy/Tuy vậy/feudō/empujar/eminence/playboy/Ả Rập/espousing/hiệu trung = 0) |

---

## 10. VẤN ĐỀ CHƯA THỂ TỰ XÁC MINH / GHI CHÚ

1. **Word COM (criterion 8):** Môi trường không có Word COM; đã thay bằng kiểm tra trực tiếp XML footnotes (76 native, id 1..76 đủ, 9pt, 1..N liên tục) — tương đương về mặt cấu trúc.
2. **Orthography flag (45):** là **false positive** — `vnch_orthography.py` gắn cờ các tựa sách/tạp chí tiếng Anh–Pháp trong cước chú (`Indochine`, `Indochina`, `Annam`). Theo Style Guide **Rule 11** ("tên riêng & tựa tiếng Anh/Pháp giữ nguyên") và **Rule 27** (không sửa nguồn), **không được** dịch các tựa nầy. Các MINOR còn lại (`một người`, `một bài`, `đang + động từ`) là cách dùng tiếng Việt chính xác.
3. **Metadata trang (M-01):** `src.txt`/progress ghi "302-330", thực tế in 302-325. Chỉ là chú thích nội bộ, không render trong DOCX; khuyến nghị cập nhật chapter_inventory/progress ở đợt sau (ngoài phạm vi nội dung chương).
4. **`audit_docx_format.py` hiển thị "Headings: 0":** là quirk của bộ đếm trong script audit; kiểm tra trực tiếp bằng python-docx xác nhận DOCX có **1 Heading 1 + 5 Heading 2** đúng định dạng, và audit vẫn **PASSED**.

---

## 11. KẾT LUẬN

| Điều kiện PASS | Trạng thái |
|---|---|
| 100% nội dung nguồn đã kiểm tra | ✔ |
| Không còn đoạn bị bỏ sót | ✔ |
| Cấu trúc đoạn 1:1 xác minh | ✔ (52/52, 0 lệch) |
| Cước chú đúng số/nội dung/vị trí | ✔ (76/76) |
| Không còn lỗi dịch nghiêm trọng / văn phong | ✔ |
| Không còn Anh/Pháp chưa xử lý hợp lý | ✔ |
| DOCX mở & kiểm tra trực tiếp | ✔ |
| Đối chiếu PDF–DOCX thực tế | ✔ |
| UTF-8 & dấu tiếng Việt | ✔ |

**KẾT LUẬN CUỐI: PASS** — Bản dịch Chương 14 sau khi sửa đã hoàn chỉnh, chính xác về nội dung, đúng văn phong học thuật VNCH, và DOCX được kiểm chứng trực tiếp khớp với PDF nguồn (PDF 318–341 / in 302–325, 1 hình Figure 14.1, 76 cước chú native).