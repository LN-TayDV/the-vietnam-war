# KẾ HOẠCH DỊCH TOÀN BỘ SÁCH
## *The Cambridge History of the Vietnam War* (Cambridge University Press)

> Tài liệu lập kế hoạch — **Chưa dịch nội dung.**
> Trạng thái: chờ phê duyệt.
> Ngày lập: 2026-11-18.

---

## 0. Thông tin nguồn & kiểm định

| Mục | Giá trị |
|---|---|
| Tệp gốc | `The_Cambridge_History_of_the_Vietnam_War.pdf` |
| Dung lượng | 41.743.651 byte (~39,8 MB) |
| Tổng số trang PDF | **1866** |
| Phiên bản PDF | 1.7, không mã hoá, có đánh dấu (tagged: no) |
| SHA-256 | `338BC8B8141A22638E1ED71A4DB285E3E10817DFAA789026E18EA988716768D1` |
| Kích thước trang | 427,7 × 647,6 pt (khổ sách in nhỏ gọn) |
| Nhà xuất bản / DOI | Cambridge University Press — DOI gốc `10.1017/9781316225240`, `…5264`, `…5288` |
| Ngày metadata | Sửa đổi 2025-07-26 |
| Cấu trúc | **3 tập** (Volume I–III), 77 chương |

Bản PDF là **bản in điện tử (e-book) có lớp văn bản thật** — không phải bản scan ảnh. Toàn bộ nội dung là chữ nạp nhúng (embedded fonts) và trích xuất được ~99,8%.

---

## 1. Tổng quan cấu trúc cuốn sách

Cuốn sách gồm **3 tập**, mỗi tập có: bìa → bản quyền → mục lục → danh mục hình/bản đồ/bảng → danh sách cộng tác viên → Dẫn nhập chung (General Introduction, Lien-Hang T. Nguyen) → Dẫn nhập (Introduction) → các phần (Parts) chứa chương → Chỉ mục (Index).

### 1.1 Phân bổ trang (PDF page ↔ trang in)

| Tập | PDF pages | Trang in (first–last) | Số chương | Số từ (thân bài, đã gồm cước chú) |
|---|---|---|---|---|
| **V1 — Origins** | 1–509 | 1–493 | 21 | ~186.200 |
| **V2 — Escalation and Stalemate** | 510–1221 | 1–695 | 30 | ~267.800 |
| **V3 — Endings and Aftermaths** | 1222–1866 | 1–630 | 26 | ~244.500 |
| **Tổng** | **1866** | — | **77** | **~698.500** |

> Tổng toàn sách (kể cả dẫn nhập, chỉ mục, chú thích thư mục) ước ~**776.700 từ** (đếm whitespace). Tổng ký tự trích xuất ~5,04 triệu.
>
> **Dịch Việt Nam** thường nở ra ~10–20% so với tiếng Anh → dự kiến bản dịch ~**800.000–900.000 từ** tương đương.

### 1.2 Cơ chế trang in &watermark (quan trọng cho khâu đối chiếu)

- Mỗi trang thân bài bắt đầu bằng **số trang in** (1–n trong tập), và kết thúc bằng dòng watermark `https://doi.org/10.1017/… Published online by Cambridge University Press`.
- **Độ lệch trang PDF ↔ trang in** không cố định theo tập:
  - V1: trang PDF 17 = trang in 1 → lệch +16; chương 1 PDF 43 = trang in 27.
  - V2: chương 1 PDF 553 = trang in 27 → lệch ~+525.
  - V3: chương 1 PDF 1259 = trang in 23 → lệch ~+1236.
- Ma trận đầy đủ `pdf_page ↔ printed_page` đã lưu trong `00_plan/manifest.json` cho từng trang của từng chương.

### 1.3 Định dạng chú thích (rất quan trọng khi dịch)

- **Chú thích là cước chú cuối trang (footnotes)**, KHÔNG phải endnote cuối chương, và **KHÔNG có mục "Bibliography/References" riêng**.
- Mỗi trang: thân bài → dải cước chú (đánh số `1 2 3…`) → watermark.
- Cuối mỗi chương chỉ có **thân bài + cước chú**; tài liệu tham khảo nằm trong chính cước chú (định dạng Chicago).
- Hình vẽ/bản đồ/bảng được nhúng giữa bài, có chú thích hình (caption) dạng `Figure 1.1 …`.
- Hệ quả: khi dịch, **giữ nguyên vị trí cước chú theo trang**, không gom về cuối chương.

---

## 2. Danh sách toàn bộ chương cần dịch (77 chương)

Ký hiệu tập: **V1** Origins · **V2** Escalation & Stalemate · **V3** Endings & Aftermaths.
Cột "PDF" là dải trang PDF; "in" là trang in bắt đầu. Chi tiết đầy đủ (pdf_start/pdf_end/số trang/số từ) ở `00_plan/chapter_inventory.csv` và `00_plan/manifest.json`.

### Tập I — Origins (21 chương)

| # | Tên chương (EN) | Tác giả | PDF | in |
|---|---|---|---|---|
| GI | *General Introduction* | Lien-Hang T. Nguyen | 17–23 | 1 |
| IN | *Introduction: Points of Departure — The Global and Local Origins of the Vietnam War* | Edward Miller | 24–40 | 8 |
| **I** | **Phần I — Empires, Nations, and Revolutions** | | 41–142 | |
| 1 | Memory, Tradition, and the History of "Vietnam" | Liam C. Kelley | 43–59 | 27 |
| 2 | The Origins of the Vietnamese Revolution | Hue-Tam Ho Tai | 60–81 | 44 |
| 3 | Hồ Chí Minh and the Rise of the Vietnamese Communist Party | Pierre Brocheux† | 82–99 | 66 |
| 4 | Indochina during World War II | Eric T. Jennings | 100–121 | 84 |
| 5 | The August Revolution of 1945 | Stein Tønnesson | 122–142 | 106 |
| **II** | **Phần II — The French Indochina War** | | 141–276 | |
| 6 | The Birth of the Democratic Republic of Vietnam | David G. Marr | 143–169 | 127 |
| 7 | France's Indochina War | Pierre Grosser | 170–188 | 154 |
| 8 | China and the French Indochina War | Chen Jian | 189–210 | 173 |
| 9 | The French Indochina War in the Central Highlands | Oscar Salemink† | 211–233 | 195 |
| 10 | The French Indochina War in Northern Vietnam | Christopher Goscha | 234–253 | 218 |
| 11 | The Battle of Điện Biên Phủ | Christopher Goscha | 254–276 | 238 |
| **III** | **Phần III — The Two Vietnams** | | 275–494 | |
| 12 | The Geneva Conference of 1954 | Martin Thomas | 277–297 | 261 |
| 13 | Eisenhower and Vietnam | David L. Anderson | 298–317 | 282 |
| 14 | Ngô Đình Diệm and the Birth of the Republic of Vietnam | Phi-Vân Nguyen | 318–341 | 302 |
| 15 | Nation-Building in South Vietnam after Geneva | Van Nguyen-Marshall | 342–362 | 326 |
| 16 | Building Socialism in North Vietnam after Geneva | Alec Holcombe | 363–383 | 347 |
| 17 | North Vietnam's Road to War | Tuong Vu | 384–404 | 368 |
| 18 | Laos between Two Wars | Vatthana Pholsena | 405–425 | 389 |
| 19 | The Origins of the Insurgency in South Vietnam | David W. P. Elliott | 426–448 | 410 |
| 20 | Kennedy and Vietnam | Marc J. Selverstone | 449–469 | 433 |
| 21 | The Crisis of 1963 and the Origins of the Vietnam War | Edward Miller | 470–494 | 454 |

### Tập II — Escalation and Stalemate (30 chương)

| # | Tên chương (EN) | Tác giả | PDF | in |
|---|---|---|---|---|
| GI | *General Introduction* | Lien-Hang T. Nguyen | 527–533 | 1 |
| IN | *Introduction* | Andrew Preston | 534–550 | 8 |
| **I** | **Phần I — Battlefields** | | 551–828 | |
| 1 | Reconsidering American Strategy in Vietnam | Gregory A. Daddis | 553–583 | 27 |
| 2 | The Air Wars in Vietnam | Mark Clodfelter | 584–608 | 58 |
| 3 | US Combat Soldiers in Vietnam | Ron Milam | 609–625 | 83 |
| 4 | American Women and the Vietnam War | Heather Marie Stur | 626–642 | 100 |
| 5 | The Conundrum of Pacification | John Prados† | 643–658 | 117 |
| 6 | The US Military Presence in South Vietnam | Meredith H. Lair | 659–679 | 133 |
| 7 | The ARVN Experience | Andrew Wiest | 680–699 | 154 |
| 8 | The National Liberation Front | Robert K. Brigham | 700–714 | 174 |
| 9 | The People's Army of Vietnam | Hai Thanh Nguyen | 715–743 | 189 |
| 10 | Vietnamese Women and the War | Amanda Boczar | 744–761 | 218 |
| 11 | Vietnam's Ethnic Minorities at War | Oscar Salemink† | 762–785 | 236 |
| 12 | The War in Numbers | Edwin E. Moïse | 786–806 | 260 |
| 13 | The Tet Offensive | James H. Willbanks | 807–828 | 281 |
| **II** | **Phần II — Homefronts** | | 827–1034 | |
| 14 | Dominoes Abroad and at Home | Fredrik Logevall | 829–846 | 303 |
| 15 | LBJ, the Great Society, and Vietnam | Julian E. Zelizer | 847–868 | 321 |
| 16 | Politics in South Vietnam, 1963–1968 | Simon Toner | 869–890 | 343 |
| 17 | Domestic Politics in the Democratic Republic of Vietnam, 1963–1968 | Martin Grossheim | 891–907 | 365 |
| 18 | The Antiwar Movement in the United States | Simon Hall | 908–931 | 382 |
| 19 | Vietnam and American Race Relations | Brenda Gayle Plummer | 932–953 | 406 |
| 20 | Prowar Sentiment in the United States | Sandra Scanlon | 954–975 | 428 |
| 21 | The US News Media and Vietnam | Chester Pach | 976–997 | 450 |
| 22 | The South Vietnamese Homefront | Mai Elliott | 998–1018 | 472 |
| 23 | The North Vietnamese Homefront | Phạm Quang Minh | 1019–1034 | 493 |
| **III** | **Phần III — Global Vietnam** | | 1033–1190 | |
| 24 | International Radicalism and Antiwar Protest | Judy Tzu-Chun Wu | 1035–1054 | 509 |
| 25 | The Vietnam War and the Sino-Soviet Split | Sergey Radchenko | 1055–1074 | 529 |
| 26 | Western Europe and the Vietnam War | Christian F. Ostermann | 1075–1104 | 549 |
| 27 | International Peace Initiatives | James G. Hershberg | 1105–1129 | 579 |
| 28 | Japan and the Vietnam War | Jennifer M. Miller | 1130–1150 | 604 |
| 29 | The Economics of the Vietnam War | Daniel Sargent | 1151–1173 | 625 |
| 30 | Vietnam and the Global 1968 | Adrienne Minh-Châu Lê | 1174–1190 | 648 |

### Tập III — Endings and Aftermaths (26 chương)

| # | Tên chương (EN) | Tác giả | PDF | in |
|---|---|---|---|---|
| GI | *General Introduction* | Lien-Hang T. Nguyen | 1237–1243 | 1 |
| IN | *Introduction* | Pierre Asselin | 1244–1256 | 8 |
| **I** | **Phần I — The Late Vietnam War** | | 1257–1534 | |
| 1 | Nixon's War | Antoine Coppolani | 1259–1280 | 23 |
| 2 | US Military Strategy in the Nixon Era | Gregory A. Daddis | 1281–1307 | 45 |
| 3 | The US Congress and the Vietnam War | Robert David (KC) Johnson | 1308–1331 | 72 |
| 4 | US Antiwar Sentiment and International Relationships in the Late Vietnam War | Jessica M. Frazier | 1332–1352 | 96 |
| 5 | Saigon War Politics, 1968–1975 | Sean Fear | 1353–1376 | 117 |
| 6 | Hanoi's Politburo at War, 1969–1975 | Pierre Asselin | 1377–1398 | 141 |
| 7 | The Vietnam War and the Regional Context | Wen-Qing Ngoei | 1399–1424 | 163 |
| 8 | Moscow, Beijing, and Détente | Lorenz M. Lüthi | 1425–1442 | 189 |
| 9 | The Easter Offensive and the Second Air War | Stephen P. Randolph | 1443–1468 | 207 |
| 10 | The Second Civil War, 1973–1975 | George J. Veith | 1469–1489 | 233 |
| 11 | Cambodia at War | T. Christopher Jespersen | 1490–1514 | 254 |
| 12 | Laos at War | Ian G. Baird | 1515–1534 | 279 |
| **II** | **Phần II — The Postwar Era** | | 1533–1680 | |
| 13 | Vietnam after "Liberation" | Ngo Vinh Long† | 1535–1548 | 299 |
| 14 | The Third World and the Communist Triumph in Vietnam | Paul Thomas Chamberlin | 1549–1568 | 313 |
| 15 | The Third Indochina War | Ang Cheng Guan | 1569–1588 | 333 |
| 16 | Vietnam in the Reform Era | Tuong Vu & Thuy Nguyen | 1589–1615 | 353 |
| 17 | Postwar US–Vietnam Relations | George C. Herring† | 1616–1637 | 380 |
| 18 | Refugees and US–Vietnam Relations | Amanda C. Demmer | 1638–1659 | 402 |
| 19 | The US POW Experience, American Veterans, and the War | Michael J. Allen | 1660–1680 | 424 |
| **III** | **Phần III — Legacies** | | 1679–1844 | |
| 20 | The Vietnam War and International Law | Kevin Jon Heller & Samuel Moyn | 1681–1711 | 445 |
| 21 | Environmental Legacies of the Vietnam War | David Biggs | 1712–1731 | 476 |
| 22 | The Vietnamese Diaspora | Tuan Hoang | 1732–1751 | 496 |
| 23 | The Vietnam War in Vietnamese Official and Personal Memory | Trinh M. Luu | 1752–1768 | 516 |
| 24 | The Vietnam War in American Culture | Patrick Hagopian | 1769–1796 | 533 |
| 25 | The Specter of Vietnam | Lloyd C. Gardner (với T. C. Jespersen) | 1797–1823 | 561 |
| 26 | Vietnam's Search for Its Place in the World | Alexander L. Vuving | 1824–1844 | 588 |

† = tác giả đã mất (được ghi chú trong sách).

> **Chỉ mục (Index)** cuối mỗi tập: không dịch nội dung chỉ mục chữ, chỉ giữ tham chiếu số trang bản in; có thể lập chỉ mục riêng cho bản dịch ở giai đoạn cuối (xem §7).

---

## 3. Đánh giá chất lượng PDF & khả năng trích xuất

### 3.1 Kết quả kiểm tra thực tế

| Tiêu chí | Kết quả |
|---|---|
| Lớp văn bản (text layer) | ✅ Có thật, đầy đủ — không cần OCR |
| Font nhúng | ✅ Toàn bộ nhúng (Dante MT Std, STIX, Myriad, Garamond, Helvetica, Noto Sans…) — có `uni=yes` (Unicode map) |
| Trang chỉ có ảnh | ⚠️ 4 trang: PDF 1, 2, 510, 1222 (bìa 3 tập) — không có nội dung dịch |
| Trang ít ký tự (<150) | 27 trang (trang phân cách phần, trang đề chương, trang trắng) — bình thường |
| Dung lượng trích xuất | ~5,04 triệu ký tự; ~776.700 từ toàn sách |
| Độ chính xác OCR | **Không cần OCR** — trích xuất trực tiếp, không sai chính tả do nhận dạng |

### 3.2 Các vấn đề đã phát hiện & biện pháp xử lý (đã tích hợp vào script)

1. **Dấu tiếng Việt ở dạng tổ hợp (decomposed):** PDF dùng dấu tổ hợp (U+0300, U+0301, U+0309, U+0323, U+031B…) thay vì ký tự dựng sẵn.
   → **Đã xử lý:** chuẩn hoá **NFC** trong `99_scripts/extract_chapters.py` (đã kiểm chứng: `Hồ Chí Minh`, `Việt Nam`, `Điện Biên Phủ` hiển thị đúng).
2. **`đ`/`Đ` bị mã hoá sai:** ký tự `đ` trích ra thành `d` + U+0335 (combining short stroke overlay), NFC không tự gộp.
   → **Đã xử lý:** ánh xạ tường minh `d+\u0335 → đ (U+0111)`, `D+\u0335 → Đ (U+0110)`. Đã xác minh không còn sót.
3. **Watermark Cambridge cuối mỗi trang:** `https://doi.org/… Published online by Cambridge University Press`.
   → **Đã xử lý:** regex xoá watermark khi trích xuất. (Lưu ý: một số URL CBV trong cước chú chứa `dangcongsan.vn` **không bị** xoá nhầm vì chỉ khớp `doi.org`.)
4. **Số trang in lẫn trong dòng đầu:** số trang in (vd `27`) nằm ở dòng đầu trang.
   → Giữ lại trong file extracted để đối chiếu, sẽ tách khi dựng bản dịch sạch.
5. **Chân trang header chạy:** tên chương/tác giả lặp ở đầu trang — cần de-duplicate khi dịch.

### 3.3 Kết luận đánh giá
PDF **chất lượng cao, không cần OCR**, trích xuất đạt độ chính xác đủ để dịch. Rủi ro còn lại chủ yếu là **hình vẽ/bản đồ/bảng** (chữ trong ảnh không trích được) — xử lý riêng ở §6.

---

## 4. Quy trình dịch toàn bộ sách (end-to-end)

### 4.1 Sơ đồ tổng thể

```
[0] Chuẩn bị (đã xong 1 phần)
    ├─ Kiểm tra PDF, metadata, outline ............... ✅ HOÀN TẤT
    ├─ Trích xuất text theo chương (NFC + fix đ) ..... ✅ HOÀN TẤT (77 file)
    └─ Lập manifest + inventory ....................... ✅ HOÀN TẤT
[1] Xây nền tảng thuật ngữ & style guide
    ├─ Dựng glossary lõi (tên riêng, địa danh, tổ chức, sự kiện)
    ├─ Chốt style guide (xưng hô, trích dẫn, số, ngày, phiên âm)
    └─ Pilot dịch 1 chương mẫu + hiệu chỉnh
[2] Dịch theo batch (mỗi chương = 1 đơn vị; nhóm 3–5 chương = 1 batch)
    ├─ Tiền xử lý: gộp dòng, tách header/footer/watermark, đánh số đoạn
    ├─ Dịch (giữ cấu trúc, cước chú, trích dẫn)
    ├─ Chuẩn hoá thuật ngữ theo glossary
    └─ Ghi file dịch + cập nhật checkpoint
[3] Hậu kiểm & đối chiếu (QA) — xem §6
[4] Dựng bản xuất (DOCX/EPUB/PDF) + chỉ mục + phê duyệt
```

### 4.2 Đơn vị & thứ tự làm việc

- **Đơn vị dịch = 1 chương** (kể cả GI/IN của tập). Chương lớn (~12–15k từ) có thể chia 2–3 lượt con (part) nhưng vẫn là 1 checkpoint.
- **Thứ tự:** GI → IN → các chương theo số thứ tự trong tập; làm lần lượt **V1 → V2 → V3** (hoặc V3 trước nếu ưu tiên phần "hậu chiến" — xem §8).
- **Batch:** gom 3–5 chương ~30–45k từ/batch để dễ checkpoint và QA. Với 77 chương + 6 mục GI/IN ⇒ ~18–22 batch.

### 4.3 Vòng đời một chương (SOP)

| Bước | Việc | Công cụ | Đầu ra |
|---|---|---|---|
| 1 | Lấy text đã trích (`02_extracted_text/vol/chNN.txt`) | script | input |
| 2 | Làm sạch: bỏ số trang/header lặp, tách cước chú theo trang | script `clean_for_translation.py` | `src_clean` |
| 3 | Gán ID đoạn `(v,c,p,idx)` | script | bản 2 cột |
| 4 | Dịch | người/máy + glossary | bản dịch |
| 5 | Rà thuật ngữ (glossary) | người | bản đã chuẩn hoá |
| 6 | QA đối chiếu | checklist §6 | xác nhận |
| 7 | Checkpoint + log tiến độ | `progress.json` | cập nhật |

---

## 5. Bộ quy chuẩn dịch thuật

> **CẬP NHẬT v2.0 (2026-11-18):** bổ sung **chuẩn ngôn ngữ miền Nam bắt buộc** — xem `07_style_guide/STYLE_GUIDE.md`, Phần B (SOUTHERN_VIETNAMESE_LANGUAGE_STANDARD). Mọi mục dưới đây phải đọc cùng Phần B.

### 5.0 Định hướng ngôn ngữ bắt buộc (MỚI)
- Bản dịch dùng **tiếng Việt miền Nam** theo truyền thống ngôn ngữ, văn chương, báo chí, học thuật của **Việt Nam Cộng hòa trước 1975**. Áp dụng xuyên suốt 3 tập, 77 chương, mọi cước chú.
- **Không dùng văn phong miền Bắc làm chuẩn.** Không dựa vào cảm nhận để kết luận từ nào Nam/Bắc — mọi phán đoán phải có nguồn kiểm chứng (từ điển VNCH, Bách Khoa, Sử Địa, Văn Học, chính luận VNCH) và ghi trong `03_terminology/glossary_nam_bac_compare.tsv`.
- Không áp đặt thuật ngữ chính trị của bất kỳ phía nào lên nguyên tác; tôn trọng cách gọi lịch sử của từng thời kỳ; không đổi nội dung/đảng điểm tác giả.
- Từ chưa xác định được vùng miền → ghi vào `03_terminology/uncertain_terms.md`, **không tự ý kết luận**.
- Xem chi tiết + bảng đối chiếu + quy chuẩn theo lĩnh vực tại `07_style_guide/STYLE_GUIDE.md` (Phần B, C, D, E).

### 5.1 Nguyên tắc bất di bất dịch
1. **Trung thành học thuật:** giữ nguyên luận điểm, lập luận, sắc thái phản biện, hedging ("may", "arguably", "it seems") — **không** thêm/bớt ý.
2. **Không lược bỏ, không tóm tắt, không diễn giải thay.** Dịch đủ 100% câu chữ của nguyên tác.
3. **Không phát sinh nội dung** ngoài nguyên tác (không thêm chú thích của người dịch trừ khi đánh dấu rõ `[ND: …]`).
4. **Giữ cấu trúc:** tiêu đề phần/mục, số đoạn, cước chú, trích dẫn, câu trích trong ngoặc kép.

### 5.2 Thuật ngữ
- **Thuật ngữ lịch sử/chính trị/quân sự/QHQT:** ưu tiên **thuật ngữ Nam Bộ đã kiểm chứng** (xem `glossary_nam_bac_compare.tsv` và Phần C của STYLE_GUIDE). Không mặc định dùng thuật ngữ Bắc.
- Khi thuật ngữ Anh có sắc thái riêng, dịch + chú `[thuật ngữ gốc: …]` ở lần xuất hiện đầu.
- **Thuật ngữ không có tương đương chuẩn:** giữ nguyên Anh + (chú thích) ở lần đầu, dùng nhất quán.
- **Từ viết tắt:** giữ nguyên dạng Anh (VNCH, NLF, PAVN, MACV, DRVN…) kèm giải nghĩa tiếng Việt lần đầu.

### 5.3 Tên riêng
| Loại | Quy tắc |
|---|---|
| Người Việt | Dùng dạng chuẩn tiếng Việt có dấu (Hồ Chí Minh, Ngô Đình Diệm, Võ Nguyên Giáp…). Tôn trọng † (tác giả quá cố) trong phần metadata. |
| Người nước ngoài | Phiên âm Hán-Việt nếu đã quen dùng (Mao Trạch Đông, Chu Ân Lai, Tưởng Giới Thạch…); còn lại transliterate + giữ nguyên Anh trong ngoặc lần đầu. |
| Địa danh VN | Dùng tên Việt chuẩn (Điện Biên Phủ, Huế, Đà Nẵng, Sài Gòn…). Theo thời kỳ lịch sử (B.5). |
| Địa danh nước ngoài | Tên tiếng Việt thông dụng; lần đầu kèm nguyên Anh. Paris → "Ba Lê (Paris)" theo lối VNCH. |
| Tổ chức | Dịch thoát nghĩa theo lối Nam + giữ viết tắt Anh (VD: "Đảng Cộng sản Việt Nam (Vietnamese Communist Party)"). |
| Sự kiện | Dùng tên chuẩn VN (Cách mạng Tháng Tám, Tổng Công Kích Tết Mậu Thân, Chiến dịch Điện Biên Phủ…). |

> Toàn bộ ánh xạ tên/địa danh/tổ chức/sự kiện sẽ được **chốt trong `03_terminology/glossary_*`** trước khi dịch hàng loạt, tránh mỗi chương một kiểu.

### 5.4 Văn phong
- **Tiếng Việt miền Nam học thuật**, mạch lạc, tự nhiên; câu không quá dài dòng, tránh dịch từng từ cứng nhắc.
- Giữ **thì & sắc thái** học thuật (diễn đạt phỏng đoán, quy kết, phản biện).
- **Số liệu, ngày tháng, trích dẫn:** giữ nguyên định dạng; theo chuẩn chốt ở §5.5 / STYLE_GUIDE D.3.
- **Ngoặc kép/câu trích:** dịch nội dung nhưng nếu là trích nguyên văn nguồn Việt thì đối chiếu bản gốc.

### 5.5 Quyết định cần chốt (đã đưa vào STYLE_GUIDE, chờ duyệt)
1. Viết năm/tháng: `1968` hay `năm 1968`; ngày `30/4/1975` hay `30 tháng 4 năm 1975`.
2. Số thập phân, phân cách nghìn (dấu phẩy VN vs Anh).
3. Chữ in nghiêng (tên sách/tạp chí/foreign terms) — quy ước `_…_` trong bản dịch.
4. Địa danh "Saigon" vs "Sài Gòn"/"TP. Hồ Chí Minh" theo ngữ cảnh lịch sử.
5. Xưng hô chung của người dịch (trung tính, ngôi thứ ba).
6. **(MỚI) Chính tả Nam Bộ:** "nầy" vs "này"; "dầu" vs "dù"; quy tắc hỏi/ngã; viết hoa VNCH (Chánh Phủ, Tổng Thống…).
7. **(MỚI)** Dạng địa danh VNCH: "Ba Lê (Paris)", "Mậu Thân", "Cao Nguyên Trung Phần".

> Chi tiết đầy đủ: `07_style_guide/STYLE_GUIDE.md` Phần B & D; bảng đối chiếu Nam/Bắc: `03_terminology/glossary_nam_bac_compare.tsv`; mục chờ nghiên cứu: `03_terminology/uncertain_terms.md`; rà soát pilot: `05_qa/v1_ch01_pilot_review.md`.

---

## 6. Cơ chế kiểm tra đối chiếu & QA

### 6.1 Đối chiếu song song (bilingual check)
- Mỗi chương có **2 file song song:** `…_src.txt` (nguyên) và `…_vi.txt` (dịch), chia theo cùng ID đoạn `(volume,chapter,page,para)`.
- **Quy tắc vàng:** mỗi đoạn nguồn phải có đúng 1 đoạn đích tương ứng → chống **bỏ sót** và **dịch trùng**.
- Script kiểm: đếm số đoạn nguồn = số đoạn đích; cảnh báo lệch.

### 6.2 Checklist QA mỗi chương (tampon)
- [ ] Đủ 100% đoạn (không sót, không lặp).
- [ ] Đúng số cước chú; nội dung cước chú khớp nguồn.
- [ ] Giữ nguyên trích dẫn, số liệu, tên riêng theo glossary.
- [ ] Không thêm/bớt luận điểm; hedging được bảo toàn.
- [ ] Chính tả & dấu tiếng Việt đúng (NFC, không lỗi font).
- [ ] Thuật ngữ nhất quán với glossary.
- [ ] Văn phong tự nhiên (đọc lướt không "lỗi dịch máy").

### 6.3 Kiểm định theo mẫu (sampling)
- Mỗi batch: chọn ngẫu nhiên 2 đoạn dài + 1 đoạn khó → đối chiếu ngược (back-translation) để phát hiện sai lệch nghĩa.
- Ghi kết quả vào `05_qa/`.

### 6.4 Chống trùng/thiếu (idempotency)
- `progress.json` lưu trạng thái từng đơn vị: `pending | translating | done | qa_passed`.
- Mỗi chương có **checkpoint** riêng; gián đoạn giữa chừng → chạy lại script sẽ bỏ qua phần đã `done`, chỉ làm tiếp phần dở.
- Mỗi chương có **mã định danh duy nhất** `Vx-Cnn`; file đặt tên theo mã này ⇒ không thể ghi đè nhầm.

---

## 7. Cấu trúc thư mục & hệ thống quản lý dữ liệu

Đã tạo khung thư mục tại `the-vietnam-war/translation-project/`:

```
translation-project/
├── 00_plan/                    # Kế hoạch (tài liệu này) + dữ liệu cấu trúc
│   ├── MASTER_PLAN.md          # ← tài liệu hiện tại
│   ├── chapter_inventory.csv   # 77 dòng: vol, chương, tên, PDF start/end, trang in, số từ
│   ├── manifest.json           # manifest máy đọc: sha, page map từng chương, trạng thái
│   └── progress.json           # (sẽ tạo) tiến độ từng chương/batch
├── 01_source_pdf/              # (đặt bản sao hoặc symlink tới PDF gốc + checksum)
├── 02_extracted_text/          # ✅ ĐÃ TẠO — text trích theo chương
│   ├── v1/ch01.txt … ch21.txt  #   (NFC + fix đ, đã bỏ watermark)
│   ├── v2/ch01.txt … ch30.txt
│   └── v3/ch01.txt … ch26.txt
├── 03_terminology/             # Từ điển thuật ngữ
│   ├── glossary_core.tsv       # lõi: người/địa danh/tổ chức/sự kiện
│   ├── glossary_terms.tsv      # thuật ngữ chuyên ngành
│   └── decisions.md            # các quyết định style đã chốt
├── 04_translation/             # Bản dịch theo cấu trúc song song
│   ├── v1/ch01/
│   │   ├── v1_ch01_src.txt     # nguồn đã làm sạch (2 cột/đoạn)
│   │   ├── v1_ch01_vi.txt      # bản dịch
│   │   └── v1_ch01_meta.json   # trạng thái, người dịch, ngày, QA
│   └── …
├── 05_qa/                      # Kết quả kiểm định theo batch
├── 06_reports/                 # Báo cáo tiến độ, tổng hợp
├── 07_style_guide/             # Style guide + quy tắc trình bày
│   └── STYLE_GUIDE.md
└── 99_scripts/                 # Tự động hoá
    ├── extract_chapters.py     # ✅ trích xuất (NFC, fix đ, watermark)
    ├── clean_for_translation.py# (sẽ tạo) tách cước chú, đánh ID đoạn
    ├── qa_check.py             # (sẽ tạo) đối chiếu đoạn nguồn↔đích
    └── progress.py             # (sẽ tạo) cập nhật/đọc progress.json
```

### 7.1 Định dạng dữ liệu
- **Text:** UTF-8, `newline='\n'` (đã thiết lập trong script), không BOM.
- **Metadata/manifest/progress:** JSON UTF-8.
- **Glossary:** TSV UTF-8 (cột: `en | vi | loại | ghi chú | nguồn_chốt`) để dễ tra & merge.
- **Đối chiếu:** file 2 cột ngăn bởi ` ||| ` hoặc song song dòng — script kiểm được.

### 7.2 Quy ước đặt tên
- Mã chương: `Vx-Cnn` (V1-C01 … V3-C26); mục đặc biệt: `Vx-GI`, `Vx-IN` (General Introduction / Introduction).
- File trích: `02_extracted_text/vx/chNN.txt`.
- File dịch: `04_translation/vx/chNN/vx_chNN_src.txt`, `…_vi.txt`, `…_meta.json`.

### 7.3 Sao lưu & an toàn
- PDF gốc + sha256 là **bản chuẩn** — mọi thứ dẫn xuất từ nó.
- `progress.json` commit thường xuyên (checkpoint) để resume sau gián đoạn.
- Mỗi batch xong → snapshot vào `06_reports/` + cập nhật manifest.

---

## 8. Lộ trình thực hiện theo giai đoạn

> Ước lượng mang tính tương đối; phụ thuộc tốc độ & số người dịch. Con số từ đếm thực tế.

| GĐ | Nội dung | Khối lượng | Đầu ra checkpoint |
|---|---|---|---|
| **G0 — Sửa soạn** | Kiểm tra PDF, trích xuất, manifest, inventory | 1866 trang / 77 chương | ✅ **ĐÃ HOÀN TẤT** (text 77 chương, inventory.csv, manifest.json) |
| **G1 — Nền tảng** | **STYLE_GUIDE v2.0 (chuẩn miền Nam) + glossary đối chiếu Nam/Bắc + nguồn tham chiếu** | ~80 mục glossary + 25 mục chờ nghiên cứu | ✅ **ĐÃ HOÀN TẤT** `07_style_guide/STYLE_GUIDE.md`, `03_terminology/*` |
| **G1.5 — Pilot** | Dịch thử **V1-Ch1 (Kelley)** + rà soát theo chuẩn Nam Bộ | ~1.2k từ mẫu | ✅ **ĐÃ HOÀN TẤT** `04_translation/v1/ch01/`, `05_qa/v1_ch01_pilot_review.md` — chờ duyệt |
| **G2 — Tập I** | Dịch 21 chương + GI/IN | ~186k từ | checkpoint từng chương; ~6–8 batch |
| **G3 — Tập II** | Dịch 30 chương + GI/IN | ~268k từ | ~8–10 batch |
| **G4 — Tập III** | Dịch 26 chương + GI/IN | ~245k từ | ~7–9 batch |
| **G5 — QA toàn tập** | Rà soát chéo glossary, đối chiếu mẫu, thống nhất thuật ngữ toàn sách | 77 chương | Báo cáo QA |
| **G6 — Dựng bản & chỉ mục** | Gộp DOCX/EPUB, chỉ mục, danh mục hình/bản đồ/bảng, bìa, mục lục VN | toàn sách | Bản thảo hoàn chỉnh |

> **Trạng thái mới (2026-11-18):** G0–G1.5 hoàn tất. Đang chờ người dùng **duyệt quy chuẩn ngôn ngữ (Phần B STYLE_GUIDE) + bản dịch thử V1-Ch1** trước khi khởi động G2.

**Tổng ước tính:** ~698k từ nguồn → bản dịch ~800–900k từ. Với năng suất dịch học thuật ~2.500–3.500 từ/ngày/người, khối lượng ~**230–300 ngày-công** (1 người) — có thể chia 3–5 dịch giả theo tập để rút ngắn, nhưng **phải dùng chung glossary & style guide** để nhất quán.

> Nếu chia nhóm: khuyến nghị **1 người/gói chương** nhưng **chốt glossary toàn sách trước**, và **cross-QA chéo** giữa các dịch giả ở G5.

### 8.1 Đề xuất thứ tự ưu tiên (tuỳ chọn)
- Nếu ưu tiên giá trị sử dụng: **V3 (Endings & Aftermaths)** trước vì chứa phần hậu chiến, di sản, quan hệ VN–Mỹ, diaspora — gần với độc giả VN.
- Nếu ưu tiên logic sử liệu: theo thứ tự in V1 → V2 → V3.
→ Cần chốt khi phê duyệt.

---

## 9. Tiêu chí nghiệm thu chất lượng bản dịch

Một chương/bản dịch được coi là **ĐẠT** khi thoả **tất cả**:

1. **Đầy đủ:** 100% đoạn nguồn có đoạn đích tương ứng; không sót, không lặp (script xác nhận).
2. **Trung thành:** không thêm/bớt luận điểm; đối chiếu mẫu (2 đoạn dài + 1 đoạn khó/batch) đạt, back-translation không lệch nghĩa cốt lõi.
3. **Thuật ngữ:** 100% thuật ngữ/tên trong glossary được dùng nhất quán; không tự chế cách dịch khác.
4. **Chú thích & trích dẫn:** đúng số lượng, đúng vị trí (cước chú theo trang), giữ nguyên số liệu & nguồn.
5. **Cấu trúc:** giữ nguyên tiêu đề phần/mục, thứ tự đoạn, câu trích.
6. **Ngôn ngữ:** tiếng Việt đúng ngữ pháp, có dấu chuẩn NFC, văn phong học thuật tự nhiên (mẫu đọc thử đạt).
7. **Toàn vẹn kỹ thuật:** file UTF-8, không lỗi font, không còn watermark/dấu tổ hợp bất thường.
8. **Kiểm định độc lập:** 1 người rà soát khác ký xác nhận (nếu làm nhóm).

> Chỉ khi checklist §6.2 + tiêu chí §9 đạt, chương mới chuyển trạng thái `qa_passed` trong `progress.json`.

---

## 10. Rủi ro & giảm thiểu

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Chữ trong hình/bản đồ/bảng không trích được | Trung bình | Ghi chú vị trí; dịch caption; phần chữ trong ảnh xử lý thủ công riêng (không có OCR cài sẵn — cần cài Tesseract nếu muốn) |
| Không nhất quán thuật ngữ giữa nhiều chương | Cao | Chốt glossary toàn tập trước; cross-QA |
| Dịch thừa/thiếu do bỏ sót cước chú | Trung bình | Song song theo ID đoạn; script đếm |
| Sai tên riêng ít gặp (ngoại lai) | Trung bình | Tra cứu + glossary; giữ nguyên Anh kèm phiên âm |
| Lệch sắc thái học thuật (dịch máy móc) | Trung bình | Rà người; back-translation; pilot chương mẫu |
| Gián đoạn giữa chừng | Thấp | Checkpoint `progress.json` + mã chương duy nhất |

---

## 11. Trạng thái hiện tại & việc cần làm tiếp

**Đã hoàn tất (GĐ G0 + G1 + G1.5):**
- ✅ Xác minh PDF: 1866 trang, 3 tập, 77 chương, không mã hoá, có text layer.
- ✅ Trích xuất đủ 77 chương ra `02_extracted_text/` (UTF-8, NFC, fix đ, bỏ watermark) — ~698.500 từ.
- ✅ Lập `00_plan/chapter_inventory.csv` (77 dòng) và `00_plan/manifest.json` (page-map + trạng thái).
- ✅ Khung thư mục `translation-project/` (9 thư mục).
- ✅ Tài liệu kế hoạch này (MASTER_PLAN.md).
- ✅ **G1: STYLE_GUIDE v2.0** — `07_style_guide/STYLE_GUIDE.md` (có Phần B: chuẩn ngôn ngữ miền Nam bắt buộc).
- ✅ **G1: Glossary đối chiếu Nam/Bắc** — `03_terminology/glossary_nam_bac_compare.tsv` (~79 mục, 8 cột, có nguồn).
- ✅ **G1: Nguồn tham chiếu** — `03_terminology/SOURCES.md`; danh sách chờ nghiên cứu `03_terminology/uncertain_terms.md`.
- ✅ **G1.5: Dịch thử V1-Ch1 (Kelley)** — `04_translation/v1/ch01/v1_ch01_src.txt` + `v1_ch01_vi.txt` + rà soát `05_qa/v1_ch01_pilot_review.md` (ĐẠT).

**Chưa làm (chờ phê duyệt):**
- G2–G4: Dịch 77 chương theo chuẩn Nam Bộ.
- G5–G6: QA toàn tập + dựng bản xuất.

**Cần người dùng quyết (sau khi duyệt quy chuẩn):**
1. Phê duyệt **chuẩn ngôn ngữ miền Nam** (STYLE_GUIDE Phần B) + bản dịch thử V1-Ch1.
2. Chốt các mục §5.5 / STYLE_GUIDE D (chính tả "nầy/này", "dầu/dù", hỏi/ngã, viết hoa VNCH; ngày/số; "Ba Lê").
3. Chọn thứ tự ưu tiên (V1→V3 hay V3 trước).
4. Mô hình thực thi: 1 người tuần tự, hay chia nhóm theo tập (kèm cross-QA).

---

*Hết kế hoạch — chờ phê duyệt quy chuẩn ngôn ngữ & chương dịch thử.*