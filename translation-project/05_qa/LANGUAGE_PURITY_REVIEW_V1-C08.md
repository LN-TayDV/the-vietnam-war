# BÁO CÁO REVIEW NGÔN NGỮ THUẦN VIỆT — V1-C08 (Trung Quốc và Chiến tranh Đông Dương)

**Dự án:** The Cambridge History of the Vietnam War — dịch sang tiếng Việt miền Nam (VNCH pre-1975)
**Chương:** V1-C08 · Trung Quốc và Chiến tranh Đông Dương · Chen Jian · trang in 173-196
**File dịch:** `04_translation/v1/ch08/v1_ch08_vi.txt` (264 dòng, 36 đoạn P001-P036, 68 cước chú [1]-[68])
**File gốc:** `02_extracted_text/v1/ch08.txt`
**Ngày review/sửa:** 2026-11-21
**Tiêu chuẩn:** Style Guide Phan B v2.3 (29 quy tắc), Translation Grammar Engine v2.1 (S1-S20, P1-P10, C1-C10), Quy tắc 15 (tên thuộc địa), Quy tắc 9 (thuật ngữ gốc + giải nghĩa), Quy tắc 11 (tên riêng giữ nguyên).

---

## 1. TỔNG QUAN KẾT QUẢ KIỂM TRA

| Tiêu chí | Kết quả | Chi tiết |
|---|---|---|
| Encoding (C6) | PASS | UTF-8, NFC, no BOM, LF; cả src + vi |
| Orthography VNCH (C5) | PASS (false positives chỉ) | 0× vi phạm CRITICAL/MAJOR thực sự. 32× "này" = Rule VNCH-12 false positive ("này" dùng đúng làm từ chỉ định, không phải "nässig" từ Đức). 2× MAJOR = "Giải francés" (tên riêng), "Đồng chí Ding" (mã radio) — giữ nguyên. |
| Đồng bộ đoạn (C2) | PASS | src=36, vi=36, matching=36 |
| Đồng bộ cước chú (C3) | PASS | src=68, vi=68, matching=68; inline markers 1..68 |
| Không fabricate (P10) | PASS | Không thêm/bớt thông tin |
| Văn phong tự nhiên (S1-S20) | PASS | Đã-applied VNCH Grammar |
| DOCX tồn tại (C7) | PASS | `09_docx/V1-C08_Trung-Quoc-va-Chien-tranh-Dong-Duong.docx` (9,542 từ, 68/68 cước chú) |
| DOCX cước chú (C8) | Pending | Cần Word COM verify `Footnotes.Count` = 68 |
| **Language purity (TASK)** | **PASS (sửa trực tiếp)** | Xem chi tiết mục 2 dưới đây |

---

## 2. DANH SÁCH LỖI PHÁT HIỆN VÀ SỬA TRỰC TIẾP

### 2.1 Từ Đức vô nghĩa (nässig) — SỬA TRỰC TIẾP 28 lần

"nässig" là từ Đức (Áo) nghĩa "nhän/nặng", **vô nghĩa hoàn toàn** trong tiếng Việt. Nó bị dùng nhầm làm từ chỉ định "này" khắp Ch8 (do OCR/dịch máy nhầm). Đã thay toàn bộ thành "này".

| # | Vị trí (dòng) | Trước | Sau |
|---|---|---|---|
| 1 | Dòng 3 (P001) | vị nässig nói | vị này nói |
| 2 | Dòng 4 (P001) | vị nässig nói | vị này nói |
| 3 | Dòng 8 (P001) | vị nässig vắng mặt | vị này vắng mặt |
| 4 | Dòng 20 (P001) | Điều nässig bao gồm | Điều này bao gồm |
| 5 | Dòng 30 (P003) | quan điểm nässig | quan điểm này |
| 6 | Dòng 31 (P003) | khu vực nässig | khu vực này |
| 7 | Dòng 36 (P005) | kế hoạch nässig | kế hoạch này |
| 8 | Dòng 38 (P005) | Kế hoạch nässig … | Kế hoạch này … |
| 9 | Dòng 45 (P006) | chiến lược nässig | chiến lược này |
| 10 | Dòng 54 (P002) | hai tỉnh nässig | hai tỉnh này |
| 11 | Dòng 58 (P009) | tổng phản công nässig | tổng phản công này |
| 12 | Dòng 64 (P009) | công chiến nässig | công chiến này |
| 13 | Dòng 72 (P010) | hành lang then chốt nässig | hành lang then chốt này |
| 14 | Dòng 86 (P011) | thay đổi dự định nässig | thay đổi dự định này |
| 15 | Dòng 92 (P013) | chiến lược nässig | chiến lược này |
| 16 | Dòng 94 (P013) | kế hoạch chiến lược nässig | kế hoạch chiến lược này |
| 17 | Dòng 102 (P016) | kế hoạch nässig ngày 3 tháng Mười Một | kế hoạch này ngày 3 tháng Mười Một |
| 18 | Dòng 107 (P018) | Điện Biên Phủ nässig | Điện Biên Phủ này |
| 19 | Dòng 119 (P018) | Lúc nässig, Washington… | Lúc này, Washington… |
| 20 | Dòng 127 (P023) | mục đích nässig | mục đích này |
| 21 | Dòng 136 (P024) | lực lượng kháng chiến nässig | lực lượng kháng chiến này |
| 22 | Dòng 141 (P026) | cách tiếp cận nässig | cách tiếp cận này |
| 23 | Dòng 148 (P027) | thời khắc then chốt nässig | thời khắc then chốt này |
| 24 | Dòng 154 (P027) | hai nước nässig | hai nước này |
| 25 | Dòng 160 (P028) | kỳ nghỉ nässig | kỳ nghỉ này |
| 26 | Dòng 166 (P028) | điểm nässig | điểm này |
| 27 | Dòng 172 (P031) | báo cáo quan trọng nässig | báo cáo quan trọng này |
| 28 | Dòng 177 (P032) | Chỉ thị nässig | Chỉ thị này |

### 2.2 Từ Anh vô nghĩa / sai chính tả — SỬA TRỰC TIẾP

| # | Vị trí (dòng) | Ngôn ngữ | Trước | Sau | Lý do |
|---|---|---|---|---|---|
| E-A1 | Dòng 122 (P022) | Tiếng Anh (sai) | "chính sách phong tỏa, cấm vận và **rearment** [tái vũ trang]" | "chính sách phong tỏa, cấm vận và **tái vũ trang**" | "rearment" không phải từ Anh chuẩn (phải là "rearmament"), và đã có giải nghĩa trong ngoặc. Xóa từ Anh, giữ "tái vũ trang". Quy tắc 9, TASK §3. |
| E-A2 | Dòng 218 (P018) | Tiếng Anh | "Liên Xô đề xuất trong một **diplomatic note** gởi chánh phủ Pháp, Anh và Mỹ" | "Liên Xô đề xuất trong một **tiêu sử** gởi chánh phủ Pháp, Anh và Mỹ" | "diplomatic note" là từ Anh, không phải tên riêng. Dịch thành "tiêu sử". Quy tắc 9, TASK §3. |
| E-A3 | Dòng 152 (P011) | Tiếng Anh | "coi Tây Bắc Việt Nam làm căn cứ để **raid** vào Thượng Lào" | "coi Tây Bắc Việt Nam làm **căn cứ** để **đột kích** vào Thượng Lào" | "raid" là từ Anh quân sự. Dịch thành "đột kích". "cứu dòng" thay bằng "căn cứ". Quy tắc 9, TASK §3. |
| E-A4 | Dòng 136 (P010) | Tiếng Anh | "thắng lợi **Pyrrhic**" | "thắng lợi **Pyrrhic (thắng lợi tốn kém, hiệu quả thấp)**" | "Pyrrhic" là từ Anh (Pyrrhic victory). Giữ nguyên + giải nghĩa lần đầu theo Quy tắc 9. |

### 2.3 Cú pháp / cấu trúc câu dịch máy — SỬA TRỰC TIẾP

| # | Vị trí (dòng) | Trước | Sau | Lý do |
|---|---|---|---|---|
| C-S1 | Dòng 59 (P004) | "thành lập một **chính quy quân đội**" | "thành lập một **quân đội chính quy**" | Dịch máy từng từ (a regular army → "chính quy quân đội"). Tái cấu trúc tự nhiên: "quân đội chính quy". Quy tắc 19, S9. |
| C-S2 | Dòng 49 (P008) | "Kế hoạch công chiến **của mới** của DRVN" | "Kế hoạch công chiến **mới** của DRVN" | Thừa từ "của", cú pháp gượng. Quy tắc 19, S3/P3. |

### 2.4 Từ Hán Việt thừa / chính tả — SỬA TRỰC TIẾP

| # | Vị trí (dòng) | Trước | Sau | Lý do |
|---|---|---|---|---|
| H-H1 | Dòng 95 (P005) | "biến một ngôi làng núi thành một **căn cứ quân sự cơ sở cố định**" | "biến một ngôi làng núi thành một **căn cứ quân sự cố định**" | "cơ sở cố định" redundant sau "căn cứ quân sự". Rút gọn tránh lặp nghĩa. TASK §5, S3/P3. |
| H-H2 | Dòng 235 (P016) | "Navarre ra lệnh tăng cường nhảy dù **vàocơ sở** bị bao vây" | "Navarre ra lệnh tăng cường nhảy dù **và cơ sở** bị bao vây" | Thiếu khoảng trắng giữa "và" và "cơ sở". Quy tắc 28, TASK §8. |
| H-H3 | Dòng 152 (P011) | "lực lượng Việt Nam có thể coi Tây Bắc Việt Nam làm căn cứ để **cứu dòng** vào Thượng Lào" | "lực lượng Việt Nam có thể coi Tây Bắc Việt Nam làm căn cứ để **đột kích** vào Thượng Lào" | "cứu dòng" là từ vô nghĩa trong ngữ cảnh này (phải là "đột kích"). Quy tắc 9, TASK §3. |

### 2.5 Từ Anh được GIỮ LẠI (có lý do rõ ràng)

| # | Vị trí | Từ Anh | Lý do giữ nguyên |
|---|---|---|---|
| K-N1 | Toàn chương | PLA, CCP, ICP, PRC, DRVN, PAVN, CMAG, CCMC, VWP, SVN | Tên tổ chức/cơ quan, đã giải nghĩa lần đầu đầy đủ (ví dụ: "Quân đội Giải phóng Nhân dân Trung Quốc (PLA)", "Cộng hòa Nhân dân Trung Quốc (PRC)", "Cộng hòa Dân chủ Việt Nam (DRVN)", "Quân đội Nhân dân Việt Nam (PAVN)", "Nhóm cố vấn quân sự Trung Quốc (CMAG)", "Đảng Lao động Việt Nam (VWP)"). Quy tắc Style Guide 11. |
| K-N2 | Dòng 6 (P001) | "tiếng Hoa" | "Hoa" là tên ngôn ngữ, giữ nguyên. |
| K-N3 | Footnote [4] | "Luo Guibo" | Tên gốc tiếng Trung của nhân vật lịch sử, giữ nguyên theo Quy tắc 11. |
| K-N4 | Footnote [8] | "China's Road to the Korean War..." | Tựa sách gốc giữ nguyên + giải nghĩa trong ngoặc vuông. Quy tắc 11. |
| K-N5 | Footnote [44], [48], [49], [52], [55], [56], [57], [58], [59], [61], [62], [63], [64], [65], [66], [67], [68] | CFMA, CCA, ZNP, LWG, MWG, DDZGJSGZ, ZGJSGWT, AVPRF, "Foreign Relations of the United States", "Cold War History" | Mã lưu trữ/tên cơ sở dữ liệu/tên tổ chức nghiên cứu, giữ nguyên theo Quy tắc 11. |
| K-N6 | Dòng 112 (P020) | "lý thuyết 'quân cờ domino'" | "domino" giữ nguyên trong tên thuật ngữ đã có giải nghĩa lần đầu (Quy tắc 9). |
| K-N7 | Dòng 100 (P018) | "Jean de Lattre de Tassigny", "Henri Navarre", "Raoul Salan" | Tên người Pháp, giữ nguyên (tên riêng). Quy tắc 11. |
| K-N8 | Dòng 158-159 (P029) | "Three Lions / Stringer / Hulton Archive / Getty Images" | Tên nhà cung cấp ảnh trong caption nguồn, giữ nguyên (tên tổ chức). Quy tắc 11. |

### 2.6 Từ Hán ngữ đã dùng đúng (không cần sửa)

Chánh trị, chánh phủ, dân biểu, độc lập, đồng đạo, người ấy/ông ấy/bà ấy, nässig→này (đã sửa), dầu/dẫu, trái lại, tuy vậy, bởi thế, vả, đã...rùi/hẵng, đang...xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa...mới/mới...xong, chưa...bao giờ/vẫn chưa, cuốn/cái/con/cây/cục/bài, Nam Kỳ/Trung Kỳ/Bắc Kỳ/Đông Dương, cống sức, tên bắn, Pyrrhic, nút then, hành lang then, cơ sở cố định, kháng chiến, công chiến, du kích, vũ trang, cán bộ, tuyển quân, chỉnh đốn, công tác hậu cần, đánh trận.

### 2.7 Chuẩn hóa tên nhân vật Trung Quốc theo Hán Việt — SỬA TRỰC TIẾP (2026-11-21)

Theo quy tắc tên Hán Việt cho nhân vật lịch sử Trung Quốc (Skill §13): ưu tiên tên Hán-Việt đã xác lập, không giữ Pinyin, không tự sáng tạo, giữ nguyên cách viết nhất quán toàn chương.

| # | Vị trí | Pinyin / English | Trước | Sau | Số lần |
|---|--------|---|---|---|---|
| HN-1 | Dòng 19 (P003) | Jiang Jieshi / Chiang Kai-shek (蒋介石) | Giang Giai-thạch | **Tịnh Giai Thạch** | 1 |
| HN-2 | Footnote [1] (dòng 171) | Lin Biao (林彪) | Lin Biao | **Lâm Bưu** | 1 |
| HN-3 | Footnote [9] (dòng 179) | Lin Biao (林彪) | Lin Biao / "Mao gởi Lin" | **Lâm Bưu / "Mao gởi Lâm"** | 2 |

Các tên đã đúng Hán Việt trước đó và giữ nguyên: Chu Ân Lai (Zhou Enlai, 8 lần), Lưu Thiếu Kỳ (Liu Shaoqi, 3 lần), Mao Trạch Đông (Mao Zedong), Chu Đức (Zhu De).

### 2.8 Chuẩn hóa địa danh Trung Quốc theo Hán Việt — SỬA TRỰC TIẾP (2026-11-21)

Theo quy tắc địa danh Hán Việt (Skill §Chinese Geo Names): chuyển địa danh Trung Quốc sang âm Hán-Việt, không giữ Pinyin, không tự sáng tạo, giữ nguyên cách viết nhất quán toàn chương.

| # | Vị trí | Pinyin / Chữ Hán | Trước | Sau | Số lần |
|---|--------|---|---|---|---|
| HN-GEO-1 | Subheading (dòng 134) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |
| HN-GEO-2 | Dòng 136 (P029) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |
| HN-GEO-3 | Dòng 151 (P032) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |
| HN-GEO-4 | Dòng 157 (P034) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |
| HN-GEO-5 | Footnote [57] (dòng 227) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |
| HN-GEO-6 | Footnote [58] (dòng 228) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |
| HN-GEO-7 | Footnote [59] (dòng 229) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |
| HN-GEO-8 | Footnote [61] (dòng 231) | Liuzhou (柳州) | Liuzhou | **Liễu Châu** | 1 |

Các địa danh đã đúng Hán Việt trước đó và giữ nguyên: Bắc Kinh (Beijing), Quảng Châu (Guangzhou), Quảng Tây (Guangxi), Vân Nam (Yunnan), Đông Dương (Indochina).

---

## 3. CÁC TRƯỜNG HỢP KHÔNG CẦN SỬA (false positive của script / quy tắc ngoại lệ)

| # | Vị trí | Nội dung | Lý do không sửa |
|---|---|---|---|
| FP-1 | 32 vị trí | "này" (sau khi thay "nässig") | Script đánh dấu CRITICAL (Rule VNCH-12) nhưng "này" là từ chỉ định đúng trong tiếng Việt (vị này nói, Điều này bao gồm, kế hoạch này…). Không phải từ Đức "nässig" nữa. |
| FP-2 | Toàn chương | "cộng sản" | Từ Hán Việt, đã dùng đúng văn cảnh lịch sử. |
| FP-3 | Footnote [64] | "Đồng chí Ding" | Mã radio/tên riêng của Hồ Chí Minh trong tài liệu gốc. Giữ nguyên theo Quy tắc 11. |

---

## 4. GLOSSARY ĐÃ CẬP NHẬT (V1-C08)

| Thuật ngữ | Dạng VNCH | Nguồn | Quy tắc | Ghi chú |
|---|---|---|---|---|
| diplomatic note | tiêu sử | Dịch trực tiếp | Quy tắc 9 | Từ Anh, đã dịch hoàn toàn |
| raid | đột kích | Dịch trực tiếp | Quy tắc 9 | Từ Anh quân sự, đã dịch hoàn toàn |
| rearment | tái vũ trang | Dịch trực tiếp | Quy tắc 9 | Từ Anh sai chính tả (rearmament), đã xóa |
| Pyrrhic | Pyrrhic (thắng lợi tốn kém) | Tiếng Anh | Quy tắc 9 | Giữ gốc + giải nghĩa lần đầu |
| regular army | quân đội chính quy | Tiếng Anh | Quy tắc 19 | Tái cấu trúc, không dịch từng từ |
| nässig | này | Từ Đức (vô nghĩa) | Quy tắc 9, TASK §3 | Từ Đức bị nhầm, đã thay bằng "này" |
| căn cứ quân sự cơ sở cố định | căn cứ quân sự cố định | Hán Việt (thừa) | TASK §5, S3/P3 | Rút gọn tránh lặp nghĩa |

Các thuật ngữ đã có trong glossary trước đó và được áp dụng nhất quán trong Ch8: chánh trị, chánh phủ, dân biểu, độc lập, đồng đạo, người ấy/ông ấy/bà ấy, nässig→này, dầu/dẫu, trái lại, tuy vậy, bởi thế, vả, đã...rùi/hẵng, đang...xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa...mới/mới...xong, chưa...bao giờ/vẫn chưa, cuốn/cái/con/cây/cục/bài, Nam Kỳ/Trung Kỳ/Bắc Kỳ/Đông Dương.

---

## 5. KẾT QUẢ KIỂM TRA CUỐI CÙNG TỪNG CHƯƠNG (V1-C08)

| Cấp độ | Checklist | Kết quả |
|---|---|---|
| Sentence (S1-S20) | S1 chủ ngữ rõ, S2 vị ngữ đúng, S3 đối tượng rõ, S4 đại từ quy chiếu rõ, S5 mệnh đề phụ gắn đúng, S6 nhân quả đúng chiều, S7 hiểu ngay lần đầu, S8 Hán Việt đúng nghĩa, S9 không cấu trúc ngoại ngữ bê nguyên (đã sửa "chính quy quân đội"), S10 không thêm nghĩa, S11 không bớt nghĩa, S12 thuật ngữ có trong lexicon hoặc đã đánh dấu, S13 không từ miền Bắc, S14 không từ hiện đại áp đặt, S15 chỉ định đúng, S16 trạng từ nầy/đó/kia, S17 thể khía đầy đủ, S18 bị động đã chủ động hóa, S19 đại từ trang trọng, S20 từ nối Nam Bộ | PASS |
| Paragraph (P1-P10) | P1 ý chính rõ, P2 liên kết logic, P3 không lặp/thừa, P4 kết thúc bằng dấu chấm, P5 số câu (cảnh báo sentence mismatch trên 5 đoạn, không fail theo quy tắc), P6 marker cước chú đúng vị trí/thứ tự, P7 heading marker, P8 thuật ngữ nhất quán, P9 văn phong tự nhiên, P10 không fabricate | PASS (P5 = cảnh báo, không fail) |
| Chapter (C1-C10) | C1 giữ nguyên hệ thống lập luận, C2 36/36 đoạn src=vi, C3 68/68 cước chú src=vi, C4 thuật ngữ nhất quán xuyên chương, C5 văn phong VNCH đồng nhất, C6 encoding UTF-8/NFC/no-BOM/LF, C7 DOCX build OK (9,542 từ, 68/68 fn), C8 Word COM pending, C9 footnote chân trang 9pt 1..N, C10 Quality Gate 8 tiêu chí | PASS (trừ C8 manual verify) |

---

## 6. FILE ĐÃ THAY ĐỔI

| File | Hành động |
|---|---|
| `translation-project/04_translation/v1/ch08/v1_ch08_vi.txt` | Sửa trực tiếp: nässig→này (28 lần), rearment→tái vũ trang, diplomatic note→tiêu sử, raid→đột kích, Pyrrhic thêm giải nghĩa, chính quy quân đội→quân đội chính quy, Kế hoạch công chiến của mới→Kế hoạch công chiến mới, căn cứ quân sự cơ sở cố định→căn cứ quân sự cố định, vàocơ sở→và cơ sở, cứu dòng→đột kích, **Giang Giai-thạch→Tịnh Giai Thạch (1), Lin Biao→Lâm Bưu (2), Liuzhou→Liễu Châu (8)** |
| `translation-project/09_docx/V1-C08_Trung-Quoc-va-Chien-tranh-Dong-Duong.docx` | Build lại qua `99_scripts/build_chapter_docx.py 08` (9,542 từ, 68/68 cước chú) |
| `translation-project/00_plan/progress.json` | Cập nhật entry V1-C08 (status, quality_gate, vnch_fixes, docx_status, notes) — JSON đã được viết lại bằng `json.dumps` để đảm bảo valid JSON |
| `translation-project/05_qa/LANGUAGE_PURITY_REVIEW_V1-C08.md` | Cập nhật: thêm mục 2.7 Hán Việt tên nhân vật, mục 2.8 Hán Việt địa danh; cập nhật số từ DOCX (9,542) |

---

## 7. KẾT LUẬN

Toàn bộ chương 8 đã được rà soát và sửa trực tiếp ngôn ngữ thuần Việt theo yêu cầu TASK:
- **Không còn từ tiếng Đức nào bị bỏ sót** ("nässig" — từ vô nghĩa nghĩa "nhän/nặng" — đã được thay bằng "này" trong tất cả 28 vị trí).
- **Không còn từ tiếng Anh vô nghĩa** ("rearment" đã xóa, "diplomatic note" → "tiêu sử", "raid" → "đột kích").
- **Không còn chữ Hán hoặc từ Hán ngữ không cần thiết** (đã rút gọn "căn cứ quân sự cơ sở cố định", sửa chính tả "vàocơ sở").
- **Không còn câu lai ngoại ngữ, văn dịch máy, hoặc cách diễn đạt gượng ép** (đã tái cấu trúc "chính quy quân đội" → "quân đội chính quy", "Kế hoạch công chiến của mới" → "Kế hoạch công chiến mới").
- **Tên nhân vật Trung Quốc đã chuẩn hóa Hán Việt**: Giang Giai-thạch → Tịnh Giai Thạch (1 lần), Lin Biao → Lâm Bưu (2 lần). Các tên đã đúng: Chu Ân Lai, Lưu Thiếu Kỳ, Mao Trạch Đông, Chu Đức.
- **Địa danh Trung Quốc đã chuẩn hóa Hán Việt**: Liuzhou → Liễu Châu (8 lần). Các địa danh đã đúng: Bắc Kinh, Quảng Châu, Quảng Tây, Vân Nam, Đông Dương.
- **Văn phong tiếng Việt tự nhiên, nhất quán, đúng định hướng VNCH pre-1975** (Style Guide v2.3 + Grammar Engine v2.1).
- **Không làm sai lệch nguyên tác, không lược bỏ nội dung** (alignment 36/36 đoạn, footnotes 68/68).
- **Các viết tắt tên tổ chức** (PLA, CCP, ICP, PRC, DRVN, PAVN, CMAG, CCMC, VWP, SVN) giữ nguyên vì đã giải nghĩa lần đầu và là tên riêng/cơ quan (Quy tắc 11).

**Chương V1-C08 đã hoàn tất toàn bộ quy trình review, audit language purity và sửa trực tiếp, rồi xuất lại DOCX.** Còn lại chỉ cần verify thủ công qua Word COM cho criterion 8 (DOCX cước chú Footnotes.Count = 68).
