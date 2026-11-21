---
name: contextual-translation
description: Phân tích ngữ cảnh, lập luận và ý nghĩa trước khi dịch. Bắt buộc đọc toàn câu, đoạn, chương liên quan; xác định chủ thể, vị ngữ, đối tượng, quan hệ logic, ý đồ tác giả. Dùng cho mọi đoạn dịch trong dự án The Cambridge History of the Vietnam War. Tích hợp Bảng Đối Chiếu Tiếng Việt PDF (doi-chieu-tieng-viet.pdf) để chọn từ đúng ngữ cảnh VNCH.
---

# Skill: Contextual Translation — Dịch Theo Ngữ Cảnh

## 1. MỤC ĐÍCH
Đảm bảo mỗi câu dịch phản ánh đúng ý nghĩa, lập luận và sắc thái của tác giả trong bối cảnh lịch sử, chính trị và học thuật. **Cấm dịch từng từ (word-for-word)** — phải hiểu ngữ cảnh toàn bộ.

## 2. KHI NÀO KÍCH HOẠT
- **Bắt buộc** cho mỗi câu/đoạn dịch (Grammar Engine Bước 1-3).
- Khi gặp từ/câu khó (Quy tắc 20).
- Khi review/audit bản dịch (kiểm tra có hiểu đúng ngữ cảnh không).

## 3. ĐẦU VÀO CẦN ĐỌC
| File | Mục đích |
|---|---|
| `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` §1-3 | Quy trình 7 bước, VNCH Grammar Database, checklist S1-S20 |
| `07_style_guide/STYLE_GUIDE_PHAN_B.md` | 29 quy tắc VNCH (v2.3) |
| `05_qa/AUDIT_REPORT_CH01-06.md` §15.4 | Quy trình 5 bước xử lý từ/câu khó |
| Bản dịch đã hoàn tất các chương trước | Đối chiếu cách dùng từ, thuật ngữ nhất quán |
| **Bảng Đối Chiếu Tiếng Việt PDF** | `books/doi-chieu-tieng-viet.pdf` — ~120 cặp từ VNCH-VC từ T.V.G., Đặc San Kỷ Niêm 25 Năm TNSP |

## 4. QUY TRÌNH PHÂN TÍCH NGỮ CẢNH (BẮT BUỘC)

### 4.1 Mở rộng phân tích (KHI GẶP VẤN ĐỀ HOẶC TRƯỚC KHI DỊCH)
1. **Đọc toàn bộ câu** — không chỉ cụm từ.
2. **Đọc đoạn văn chứa câu** — hiểu ý chính đoạn (topic sentence).
3. **Đọc đoạn trước & đoạn sau** — liên kết logic, từ nối, quy chiếu đại từ.
4. **Xác định vị trí trong chương** — heading, phần nào, lập luận gì.
5. **Nếu cần: đọc chương liên quan / sách khác trong series** — thuật ngữ lặp lại.

### 4.2 Xác định 4 yếu tố cốt lõi (Grammar Engine Bước 2)
| Yếu tố | Câu hỏi | Cách tìm |
|---|---|---|
| **Chủ thể** | Ai/thứ gì thực hiện hành động? | Tìm noun phrase trước động từ; nếu passive → tìm "by..." |
| **Vị ngữ** | Hành động/tình trạng gì? | Động từ chính + bổ ngữ |
| **Đối tượng** | Ai/thứ gì chịu tác động? | Noun phrase sau động từ túc trực |
| **Quan hệ logic** | Mệnh đề phụ liên kết thế nào? | Từ nối: because, although, however, therefore, etc. |

### 4.3 Phân tích quan hệ logic (Grammar Engine §1.8 — Bước 3)
| Quan hệ | Từ nối tiếng Anh | Từ nối VNCH ưu tiên | Ví dụ |
|---|---|---|---|
| Nhượng bộ | although, though, even though | **dầu, dẫu** | "Dầu đã nỗ lực..." |
| Tương phản | however, but, on the other hand | **trái lại** | "Trái lại, miền Nam..." |
| Chuyển ý | however (chuyển chủ đề) | **tuy vậy, đã vậy, song** | "Tuy vậy, kết quả..." |
| Nhân quả | therefore, thus, so, consequently | **bởi thế, do đó, cho nên** | "Bởi thế, chánh phủ..." |
| Bổ sung | moreover, furthermore, additionally | **vả, lại, cũng** | "Vả, còn có..." |
| Điều kiện | if, provided that, in case | **khi... thì, nếu... thì** | "Khi hiệp định ký..." |
| Mục đích | in order to, so that, to | **để, hầu, nhằm** | "Để độc lập..." |

## 5. XỬ LÝ TỪ/CÂU KHÓ — QUY TRÌNH 5 BƯỚC (Quy tắc 20)

**KHI GẶP TỪ HOẶC CÂU KHÓ HIỂU:**

| Bước | Hành động | Đầu ra |
|---|---|---|
| **1. Mở rộng ngữ cảnh** | Đọc đoạn trước/sau, heading, chương liên quan | Hiểu bối cảnh lịch sử, lập luận tác giả |
| **2. Xác định ý đồ tác giả** | Tác giả muốn chứng minh gì? Sắc thái gì? (trung tính, biện hộ, phê phán?) | Lập luận cốt lõi của đoạn |
| **3. Tra cứu nguồn** | Từ điển (Lê Văn Đức, Oxford), tài liệu chuyên ngành, lịch sử (MASTER_LEXICON, SOURCES.md, **Bảng Đối Chiếu PDF**) | Nghĩa từ có căn cứ |
| **4. Đối chiếu chỗ khác** | Từ này xuất hiện ở đâu nữa trong sách? Dùng như thế nào? | Nhất quán thuật ngữ |
| **5. Tái dựng & diễn đạt** | Kết hợp ý nghĩa nguyên văn + ngữ cảnh + văn phong VNCH → câu tiếng Việt tự nhiên | Câu dịch hoàn chỉnh |

**GHI NHẬN CĂN CỤ BẮT BUỘC:**
- Căn cứ văn bản (trích dẫn câu gốc).
- Ngữ cảnh (đoạn, heading, chương).
- Nguồn tra cứu (từ điển, tài liệu, lexicon, **Bảng Đối Chiếu PDF**).
- Lập luận (tại sao chọn nghĩa này).
- Phân biệt: Nghĩa nguyên văn / Nghĩa theo ngữ cảnh / Cách diễn đạt bản dịch.
- Mức độ chắc chắn (90%, 95%, 100%) + Lý do.

**CẤM:**
- Đánh dấu `UNRESOLVED` rồi bỏ qua.
- Giữ nguyên tiếng Anh vì "không hiểu".
- Dịch từng từ rồi ghép (Quy tắc 19).
- Tự suy diễn không có căn cứ.

## 6. ĐỐI CHIẾU LẬP LUẬN TÁC GIẢ (Grammar Engine C1)

Sau khi dịch xong chương:
1. Xác định hệ thống lập luận chính của tác giả.
2. Kiểm tra bản dịch có giữ nguyên: thứ tự lập luận, quan hệ nhân quả, trọng điểm.
3. Không được: đảo trật tự, làm mờ đối lập, thêm lập luận của người dịch.

## 7. KIỂM TRA NGỮ CẢNH KHI REVIEW (Deep Translation Review)

Khi audit/review bản dịch:
- Mỗi câu: Đọc câu gốc → đọc câu dịch → hỏi: "Ý này có đúng không? Sắc thái có giữ được không?"
- Mỗi đoạn: Đọc liền mạch → ý chính có rõ không? Từ nối logic có tự nhiên không? (P2)
- Toàn chương: Lập luận tác giả có bị lệch không? (C1)

## 8. CHỌN TỪ VNCH THEO NGỮ CẢNH (Từ Bảng Đối Chiếu PDF)

### 8.1 Nguyên tắc: Không áp dụng máy móc, phải phân tích ngữ cảnh
| Tình huống | Từ VC/miền Bắc | Từ VNCH | Cách chọn |
|---|---|---|---|
| **Thân bài, thuật ngữ chính trị** | giải phóng | **độc lập / kháng cự** | Tác giả dùng "liberation" trung tính → dịch "độc lập" |
| **Tên riêng, tên tổ chức** | Cờ Giải Phóng, Quân Giải Phóng, Mặt Trận Giải Phóng | **Giữ nguyên "Giải Phóng"** + ghi chú `[ND: tên riêng, VNCH dùng "độc lập/kháng cự"]` | Tên cố hữu, không dịch |
| **Tên thuộc địa trong trích dẫn** | Annam, Tonkin, Cochinchine, Indochine | **Giữ nguyên** (trích dẫn tiếng Pháp/Anh) | Rule 15: trích dẫn giữ nguyên |
| **Tên thuộc địa trong thân bài** | Annam | **Trung Kỳ (Annam)** | Rule 15: thân bài dùng tên VNCH + gốc trong ngoặc |
| **Từ đồng nghĩa nhưng sắc thái khác** | chính phủ | **chánh phủ** | Rule 1, 4, 12: "chính" = chính quyền, "chánh" = chính trực |
| **Từ hiện đại áp đặt** | tài chính | **tài chánh** | Rule 3: VNCH dùng "tài chánh" |
| **Từ miền Bắc trong văn phong** | này | **nầy** | Rule 22: "năm nầy, trước nầy, sau nầy" |
| **Từ nối logic** | tuy nhiên | **tuy vậy / đã vậy / song** | Rule 25: VNCH ưu tiên "tuy vậy" |
| **Thể khía** | đã ký | **đã ký hẵng / đã ký rùi** | Rule 23: Dạng đầy đủ Nam Bộ |
| **Đại từ nhân xưng** | hắn, y, nó (chỉ người) | **người ấy / ông ấy / bà ấy / họ** | Rule 24: Cấm hắn/y/nó chỉ người |

### 8.2 Danh sách ưu tiên từ PDF (Bảng Đối Chiếu) — Phân tích theo ngữ cảnh
| Nhóm | Từ VC/miền Bắc | VNCH Chuẩn | Lưu ý ngữ cảnh |
|---|---|---|---|
| **Chính trị - Hành chính** | chính trị | chánh trị | Luôn thay thế (69 lần/6 chương) |
|  | chính phủ | chánh phủ | Luôn thay thế (12 lần) |
|  | chính đảng | chánh đảng | Luôn thay thế |
|  | đảo chính | đảo chánh | Luôn thay thế |
|  | đại biểu | dân biểu | Luôn thay thế (Hạ Nghị Viện) |
|  | nghị sĩ | nghị sĩ | Giữ (Thượng Nghị Viện) |
|  | lương hưu | hưu bổng | Luôn thay thế |
|  | bất động sản | địa ốc | Luôn thay thế |
|  | ngân sách (cơ quan) | ngân khố | Phân biệt: cơ quan vs kế hoạch |
|  | bảo hiểm | an toàn | "bảo hiểm (mù) → an toàn (mù)" |
|  | báo cáo | thưa trình, nói, kể | Theo ngữ cảnh: báo cáo văn bản/thuộc ngữ/định kỳ |
|  | bảo quản | che chở, gìn giữ, bảo vệ | Theo ngữ cảnh vật/người |
|  | bài nói | diễn văn | Văn phong học thuật/trang trọng |
|  | cách ly | cô lập | "cách ly" mang sắc thái y tế hiện đại |
|  | cái A-lô | cái điện thoại | Thuật ngữ đời thường VNCH |
|  | cân (làm) | căng thẳng | Sắc thái "intense" |
|  | cầu lông | vũ cầu | Tên thể thao VNCH |
|  | chất lượng | phẩm chất tốt | Chỉ cấp "quality", không cấp "quantity" |
|  | chế độ | quy chế | Văn bản pháp lý/hành chính |
|  | chỉ đạo | chỉ thị, ra lệnh | Hành động cấp trên xuống cấp dưới |
|  | chỉ tiêu | định suất | Kinh tế/kế hoạch hóa |
|  | chúng nhiêm | trường ban, khoa trưởng | Cấp quản lý trường học |
|  | chủ trễ | chú tôa | "chủ trễ" → "chú tôa" (phát âm miền Nam) |
|  | chửa cháy | cầu hỏa | Thuật ngữ PCCC |
|  | chiếu đãi | thất đãi | Sắc thái tiêu cực "thất" |
|  | chui | lén lút | Hành động trốn tránh |
|  | chuyện chèo | nói lên, nêu ra | "Chèo" = nói chuyện dài dòng, VNCH dùng "nêu ra" |
|  | chuyện ngữ | dịch | "Chuyện ngữ" = dịch thuật, VNCH dùng "dịch" |
|  | chứng minh nhân dân | thẻ căn cước | Giấy tờ tùy thân VNCH |
|  | chữ đạo | chính | "Chữ" = chính sách/đạo chính |
|  | co cụm | thu hẹp | Kinh tế/chiến lược |
|  | công đoàn | nghiệp đoàn | Tổ chức người lao động VNCH |
|  | công nghiệp | kỹ nghê | "Nghiệp" mang sắc thái thủ công/cổ truyền |
|  | công trình | công tác | "Công trình" = kiến trúc, "công tác" = công việc |
|  | cơ bản | căn bản | Phát âm miền Nam |
|  | cơ khí | cần bản | "Cơ" = máy móc, "cần" = thủ công/cơ khí |
|  | cơ sở | căn bản, nguồn gốc | Theo ngữ cảnh |
|  | cửa khẩu | phi cảng, hải cảng | Cảng hàng không / cảng biển |
|  | cụm từ | nhóm chữ | Học thuật/ngữ pháp |
|  | cứu hộ | cứu cấp | Y tế/cấp cứu |
|  | diễn | thành phần | Hóa học/quân sự: "diễn" = thành phần |
|  | đấu kiện | phương định | Pháp lý: "đấu kiện" = kiện tụng, "phương định" = quy định |
|  | đạo trí | tự nhiên | "Đạo trí" = bản tính, VNCH dùng "tự nhiên" |
|  | đầu ra / đầu vào | xuất lượng / nhập lượng | Kinh tế: output/input |
|  | đại tiệc / tiểu tiệc | nấu ăn chung, ăn tập thể / nấu ăn riêng, ăn gia đình | Văn hóa ẩm thực |
|  | đại trà | quy mô, cỡ lớn | Sắc thái "lớn, vĩ đại" |
|  | đảm bảo | bảo đảm | "Đảm" = nắm giữ, "bảo" = gìn giữ |
|  | đăng ký | ghi danh, ghi tên | Hành chính: đăng ký = ghi danh |
|  | đáp án | kết quả, trả lời | Thi cử/hỏi đáp |
|  | đăng kí | ghi danh | Phép viết khác của "đăng ký" |
|  | đồng bằng | phi đạo | Địa lý: "phi đạo" = đồng bằng (từ Hán-Việt) |
|  | đường cao tốc | xa lộ | Giao thông: "xa lộ" = đường cao tốc |
|  | gia công | làm ăn công | "Gia công" = gia công cơ khí, VNCH dùng "làm ăn công" |
|  | giải phóng | lấy lại, đem đi... | VC dùng nhiều; thân bài VNCH dùng "độc lập/kháng cự" |
|  | giải phóng mặt bằng | đứt cho đất bằng | Quân sự: "giải phóng" = lấy lại kiểm soát |
|  | giản đơn | đơn giản | Phép viết miền Nam |
|  | giao lưu | giao tiếp, trao đổi | "Giao lưu" mang sắc thái văn hóa, "giao tiếp" = liên lạc |
|  | hạch toán | kế toán | "Hạch" = ghi sổ, VNCH dùng "kế toán" |
|  | hải quan | quan thuế | "Hải quan" = cảng biển, "quan thuế" = cơ quan thuế |
|  | hàng không dân dụng | hàng không dân sự | "Dân dụng" = dùng cho dân, "dân sự" = thuộc dân sự |
|  | hát đôi | song ca | Âm nhạc: "song ca" = hai người hát |
|  | hát tập | hợp ca | Âm nhạc: "hợp ca" = nhóm hát |
|  | hát nhân (vũ khí) | nguyên tử | Vũ khí hạt nhân |
|  | hậu cần | tiếp liệu | Quân sự: "hậu cần" = logistics, VNCH dùng "tiếp liệu" |
|  | học vị | bằng cấp | "Học vị" = academic degree, VNCH dùng "bằng cấp" |
|  | hệ quả | hậu quả | "Hệ" = hệ thống, "hậu" = sau cùng/kết quả |
|  | hiện đại | tối tân | "Hiện" = hiện tại, "tối" = mới nhất/tân tiến |
|  | hộ nhà | gia đình | "Hộ" = hộ khẩu, "gia đình" = đơn vị xã hội |
|  | hộ chiếu | sổ thông hành | Giấy đi lại VNCH |
|  | họp hội | phân khu | "Họp hội" = meeting, "phân khu" = assembly/phân chia khu vực |
|  | họ khẩu | tổ khai gia đình | Đăng ký hộ khẩu VNCH |
|  | hội chữ thập đỏ | hội Hồng Thập Tự | Tổ chức nhân đạo VNCH |
|  | kiều hời | ngoại tệ | Tiền tệ nước ngoài |
|  | kiệt xuất | giải, xuất sắc | "Kiệt" = vượt trội, "giải/xuất sắc" = cấp độ |
|  | kinh qua | trải qua | "Kinh" = trải qua/qua lại |
|  | làm gái | làm điếm | "Gái" = gái điếm (thô tục), "điếm" = điếm kh Europäischen |
|  | làm việc | thẩm vấn, điều tra | "Làm việc" = làm việc chung, "thẩm vấn/điều tra" = police interview |
|  | lâu năm góc / nhà tráng | ngụy Giác Đốc / Tòa Bạch ốc | Tên cơ quan an ninh VNCH |
|  | liên hoan | đại hội, ăn mừng | "Liên hoan" = tiệc lớn, "đại hội/ăn mừng" = rõ nghĩa hơn |
|  | liên hệ | liên lạc | "Liên hệ" = contact (cách dùng hiện đại), "liên lạc" = liên lạc truyền thống |
|  | linh tinh | vỏ vần | "Linh tinh" = lẫn lộn, "vỏ vần" = vụn vặt/lẻ tẻ |
|  | lính gái | nữ quân nhân | "Gái" = con gái, "nữ quân nhân" = phụ nữ trong quân đội |
|  | lính thủy đánh bộ | thủy quân lực lượng chiến | Đơn vị amphibious |
|  | lợi nhuận | lợi tức | "Nhuận" = lợi nhuận, "lợi tức" = thu nhập/lợi tức |
|  | lực tôm | tôm lực | Món ăn: "tôm lực" = tôm chiên bơ tỏi |
|  | lý giải | giải thích | "Lý" = thuyết phục, "giải thích" = make clear |
|  | máy bay lên thẳng | trực thăng | "Trực thăng" = helicopter (từ Hán-Việt) |
|  | múa đòi | khiêu vũ | "Múa đòi" = múa dân gian, "khiêu vũ" = ballroom dance |
|  | Mĩ — Mĩ (Hoa kỳ) | Mỹ | Quốc gia: Mỹ |
|  | nằm bật | nằm ngửa | "Bật" = ngửa mặt lên trời |
|  | nâng cấp | nâng, hoặc đưa giá trị lên | "Cấp" = cấp độ, "nâng/đưa giá trị" = upgrade |
|  | năng nổ | siêng năng, tháo vát | "Năng" = năng lực, "siêng năng" = chăm chỉ |
|  | nghệ nhân | thờ, nghệ sỹ | "Nghệ nhân" = craftsman, "thờ/nghệ sỹ" = artisan/artist |
|  | nghệ danh | Tên (nghệ sỹ - stage name) dùng ngoài tên thật | Nghệ thuật: nghệ danh |
|  | nghĩa vụ quân sự | Đi quân dịch | "Nghĩa vụ" = obligation, "Đi quân dịch" = conscription |
|  | nghiêm túc | nghiêm chính | "Túc" = đầy đủ, "chính" = chính xác/trang trọng |
|  | nghiệp dư | Đi làm thêm (2nd job / nghề phụ, nghề tay trái) | "Nghiệp dư" = amateur, "Đi làm thêm" = moonlighing |
|  | nhà khách | khách sạn | "Nhà khách" = guest house, "khách sạn" = hotel |
|  | nhất trí | đồng lòng, đồng ý | "Trí" = ý chí, "đồng lòng" = unity of heart |
|  | nhất quán | luôn luôn, trước sau như một | "Quán" = xuyên suốt, "luôn luôn" = consistent |
|  | người nước ngoài | ngoại kiều | "Nước ngoài" = foreign country, "ngoại kiều" = overseas Vietnamese/foreigner |
|  | noi niệm (tính từ!) | viễn suy tư | "Noi niệm" = niệm nhớ, "viễn suy tư" = thinking of afar |
|  | phân cứng | cường liệu | Nông nghiệp: phân bón |
|  | phân mềm | nhu liệu | Nông nghiệp: phân hữu cơ |
|  | phản ánh | phản ảnh | "Ánh" = reflection, "ảnh" = image/reflection |
|  | phản hồi | trả lời, hồi âm | "Hồi" = trả lại, "hồi âm" = feedback |
|  | phát sóng | phát thanh | Radio: "phát thanh" = broadcast |
|  | phó tiến sĩ | cao học | Academic: "cao học" = graduate studies |
|  | phi khẩu | phi trường, phi cảng | Airfield/airport |
|  | phi vụ | một vụ trao đổi thường mại | Business deal |
|  | phục hồi nhân phẩm | hoàn lượng | "Phục hồi" = restore, "hoàn lượng" = restore character |
|  | phương án | kế hoạch | "Phương án" = option, "kế hoạch" = plan |
|  | quá tài | quá sướng, quá mức | "Tài" = talent, "quá sướng" = too lucky/good |
|  | quan triết | hiểu rõ | "Triết" = philosophy, "hiểu rõ" = understand deeply |
|  | quân lý | quân trị | "Lý" = reason, "trị" = govern/military admin |
|  | quảng trường | công trường | "Quảng" = wide, "công" = public/official |
|  | quân hàm | cấp bậc | Military rank |
|  | quy hoạch | kế hoạch | "Hoạch" = planning, "kế hoạch" = plan |
|  | quy trình | tiến trình | "Trình" = sequence, "tiến trình" = process |
|  | sốc (shocked) | kinh hoàng, kinh ngạc, ngạc nhiên | "Sốc" = shock (từ ngoại lai), VNCH dùng từ thuần Việt |
|  | sổ tân | tân cương | "Sổ" = register, "tân cương" = new register |
|  | sư - sư đoàn | sư đoàn | Military: division |
|  | sức khỏe công dân | y tế công cộng | Public health |
|  | sự cố | trở ngại | "Cố" = incident, "trở ngại" = obstacle/difficulty |
|  | tạp đoàn / doanh nghiệp | công ty | "Tạp đoàn" = regiment/enterprise, "công ty" = company |
|  | tên lứa | hòa tiến | Pen name |
|  | tham gia lưu thông (xe cộ) | lưu hành | Traffic: circulation |
|  | tham quan | thẩm viếng | "Tham quan" = visit (sightseeing), "thẩm viếng" = inspect/visit officially |
|  | thanh lý | thanh toán, chứng minh | Finance/legal: settle/liquidate |
|  | thần thượng | thần mê | "Thượng" = high, "mê" = ecstasy/rapture |
|  | thi công | làm | Construction: "thi công" = construct, "làm" = make/do |
|  | thí phần | thí trường | Test site/field |
|  | thu nhập | lợi tức | Income |
|  | thư giãn | tĩnh táo, giải trí | "Thư" = relax, "tĩnh táo" = calm/tranquil |
|  | thuyết phục (tính) | có lý (makes sense), hợp lý - tin được | "Thuyết phục" = persuade, "có lý/hợp lý" = reasonable/convincing |
|  | tiến tiến | xuất sắc | "Tiến" = advance, "xuất sắc" = excellent |
|  | tiến công | tấn công | Military: attack |
|  | tiếp thu | tiếp nhận, thâu nhận, lãnh hội | Receive/accept |
|  | tiêu dùng | tiêu thụ | Consume |
|  | tổ lái | phi hành đoàn | Flight crew |
|  | tổ rơi | truyền đơn | Airdrop |
|  | tranh thủ | cố gắng | "Thanh thủ" = strive for time, "cố gắng" = try hard |
|  | trí tuệ | kiến thức | Intellect/intelligence |
|  | triển khai | khai triển | Deploy/expand |
|  | tư duy | suy nghĩ | Thought/thinking |
|  | tư liệu | tài liệu | Document/material |
|  | từ | tiếng, chữ | Word |
|  | uốn tạc | tắt nghiêng | Distort |
|  | văn dân | văn đề | Literature/writing |
|  | văn động viên | lực sĩ | Cultural troupe |
|  | viện ung bướu | viện ung thư | Cancer institute |
|  | vô tư | tự nhiên | Spontaneous/natural |
|  | xác tín | chính xác | Verify/confirm |
|  | xe con | xe du lịch | Sedan/car |
|  | xe khách | xe đồ | Bus/truck |
|  | xử lý | giải quyết, thi hành | Handle/process |

## 9. VÍ DỤ THỰC TẾ TỪ AUDIT 6 CHƯƠNG + PDF

### Ví dụ 1: "giải phóng" (Ch3, Ch4, Ch5)
- **Nguyên văn**: "liberation", "liberation front", "liberation army"
- **Ngữ cảnh**: Tác giả Stein Tønnesson dùng thuật ngữ trung lập lịch sử.
- **VNCH**: "giải phóng" = thuật ngữ Cộng sản (giải phóng miền Nam, giải phóng giai cấp).
- **Quyết định**: Thân bài dịch "giải phóng" → "độc lập" / "kháng cự"; tên riêng (Cờ Giải Phóng, Quân Giải phóng) → giữ nguyên có ghi chú.
- **Mức độ chắc chắn**: 95% (Style Guide Rule 8, 15; MASTER_LEXICON; PDF: "giải phóng → lấy lại, đem đi...").

### Ví dụ 2: "Annam / Tonkin / Cochinchina / Indochine" (Ch2, Ch4)
- **Nguyên văn**: Tên gọi thuộc địa Pháp.
- **Ngữ cảnh**: Xuất hiện trong trích dẫn sách, tên báo, tên khóa học, tên tổ chức pháp lý.
- **Quy tắc 15 (Style Guide)**: Tên riêng, tên sách, tên báo, thuật ngữ pháp lý — **giữ nguyên** dạng gốc, thêm tên VNCH trong ngoặc đơn lần đầu.
- **Quyết định**: "Annam" → "Trung Kỳ (Annam)"; "Tonkin" → "Bắc Kỳ (Tonkin)"; "Cochinchina" → "Nam Kỳ (Cochinchina)"; "Indochine" → "Đông Dương (Indochine)". Trong trích dẫn tiếng Pháp/Anh — giữ nguyên hoàn toàn.
- **Mức độ chắc chắn**: 100%.

### Ví dụ 3: "chính trị" → "chánh trị" (Toàn bộ 6 chương)
- **Nguyên văn**: "political", "politics", "politically"
- **Ngữ cảnh**: Thuật ngữ cốt lõi VNCH. "Chính" = chính quyền, "chánh" = chính trực.
- **Quyết định**: Thay thế tất cả 69 lần. Trong tên sách "Sử Chính Trị Việt Nam" → "Sử Chánh Trị Việt Nam".
- **Mức độ chắc chắn**: 100% (Style Guide Rule 1, 4, 12; MASTER_LEXICON; PDF: "chính trị → chánh trị").

### Ví dụ 4: "báo cáo" → "thưa trình/nói/kể" (PDF)
- **Nguyên văn**: "report", "reported", "reporting"
- **Ngữ cảnh**: Tác giả dùng "report" theo nhiều nghĩa: báo cáo văn bản, báo cáo thuộc ngữ, báo cáo định kỳ.
- **VNCH**: "báo cáo" → "thưa trình" (cấp dưới lên cấp trên), "nói" (truyền đạt), "kể" (vần chuyện).
- **Quyết định**: Phân tích ngữ cảnh từng câu để chọn từ phù hợp.
- **Mức độ chắc chắn**: 90% (PDF: "báo cáo → thưa trình, nói, kể").

## 10. CHECKLIST NGỮ CẢNH MỖI CÂU (S1-S6, S12-S14)

```
[ ] S1: Chủ ngữ rõ ràng (người ấy/ông ấy/bà ấy/người nầy)
[ ] S2: Vị ngữ đúng hành động (chủ động hóa nếu passive)
[ ] S3: Đối tượng rõ ràng
[ ] S4: Đại từ có quy chiếu rõ (thay bằng danh từ cụ thể nếu mơ hồ)
[ ] S5: Mệnh đề phụ gắn đúng đối tượng
[ ] S6: Quan hệ nhân quả đúng chiều (dùng từ nối Nam Bộ: dầu, trái lại, tuy vậy, bởi thế, vả)
[ ] S12: Thuật ngữ có trong lexicon / VNCH Grammar Database / PDF
[ ] S13: Không dùng từ miền Bắc (này, giải phóng, đồng chí, chính phủ, chính trị, bài nói, báo cáo, bảo quản, cách ly, cái A-lô, cân, chất lượng, chế độ, chỉ đạo, chỉ tiêu, chúng nhiêm, chủ trễ, chửa cháy, chiếu đãi, chui, chuyện chèo, chuyện ngữ, chứng minh nhân dân, chữ đạo, co cụm, công đoàn, công nghiệp, công trình, cơ bản, cơ khí, cơ sở, cửa khẩu, cụm từ, cứu hộ, diễn, đấu kiện, đại học mái, đạo trí, đầu ra/đầu vào, đại tiệc/tiểu tiệc, đại trà, đảm bảo, đăng ký, đáp án, đăng kí, đồng bằng, đường cao tốc, gia công, giải phóng, giản đơn, giao lưu, hạch toán, hải quan, hàng không dân dụng, hát đôi, hát tập, hát nhân, hậu cần, học vị, hệ quả, hiện đại, hộ nhà, hộ chiếu, họp hội, họ khẩu, hội chữ thập đỏ, kiều hời, kiệt xuất, kinh qua, làm gái, làm việc, lâu năm góc/nhà tráng, liên hoan, liên hệ, linh tinh, lính gái, lính thủy đánh bộ, lợi nhuận, lực tôm, lý giải, máy bay lên thẳng, múa đòi, Mĩ, nằm bật, nâng cấp, năng nổ, nghệ nhân, nghệ danh, nghĩa vụ quân sự, nghiêm túc, nghiệp dư, nhà khách, nhất trí, nhất quán, người nước ngoài, noi niệm, phân cứng, phân mềm, phản ánh, phản hồi, phát sóng, phó tiến sĩ, phi khẩu, phi vụ, phục hồi nhân phẩm, phương án, quá tài, quan triết, quân lý, quảng trường, quân hàm, quy hoạch, quy trình, sốc, sổ tân, sư đoàn, sức khỏe công dân, sự cố, tạp đoàn/doanh nghiệp, tên lứa, tham gia lưu thông, tham quan, thanh lý, thần thượng, thi công, thí phần, thu nhập, thư giãn, thuyết phục, tiến tiến, tiến công, tiếp thu, tiêu dùng, tổ lái, tổ rơi, tranh thủ, trí tuệ, triển khai, tư duy, tư liệu, từ, uốn tạc, văn dân, văn động viên, viện ung bướu, vô tư, xác tín, xe con, xe khách, xử lý)
[ ] S14: Không dùng từ hiện đại áp đặt (tài chính→tài chánh, đại biểu→dân biểu, lương hưu→hưu bổng, ngân sách cơ quan→ngân khố, bất động sản→địa ốc, bảo hiểm→an toàn, báo cáo→thưa trình/nói/kể, bảo quản→che chở/gìn giữ/bảo vệ, bài nói→diễn văn, cách ly→cô lập, cảnh báo→báo động/phải chú ý, cái A-lô→cái điện thoại, cân→căng thẳng, cầu lông→vũ cầu, chất lượng→phẩm chất tốt, chất xám→trí tuệ/sự thông minh, chế độ→quy chế, chỉ đạo→chỉ thị/ra lệnh, chỉ tiêu→định suất, chúng nhiêm→trường ban/khoa trưởng, chủ trễ→chú tôa, chửa cháy→cầu hỏa, chiếu đãi→thất đãi, chui→lén lút, chuyện chèo→nói lên/nêu ra, chuyện ngữ→dịch, chứng minh nhân dân→thẻ căn cước, chữ đạo→chính, co cụm→thu hẹp, công đoàn→nghiệp đoàn, công nghiệp→kỹ nghê, công trình→công tác, cơ bản→căn bản, cơ khí→cần bản, cơ sở→căn bản/nguồn gốc, cửa khẩu→phi cảng/hải cảng, cụm từ→nhóm chữ, cứu hộ→cứu cấp, diễn→thành phần, đấu kiện→phương định, đạo trí→tự nhiên, đầu ra/đầu vào→xuất lượng/nhập lượng, đại tiệc/tiểu tiệc→nấu ăn chung/ăn tập thể/nấu ăn riêng/ăn gia đình, đại trà→quy mô/cỡ lớn, đảm bảo→bảo đảm, đăng ký→ghi danh/ghi tên, đáp án→kết quả/trả lời, đăng kí→ghi danh, đồng bằng→phi đạo, đường cao tốc→xa lộ, gia công→làm ăn công, giải phóng→lấy lại/đem đi, giản đơn→đơn giản, giao lưu→giao tiếp/trao đổi, hạch toán→kế toán, hải quan→quan thuế, hàng không dân dụng→hàng không dân sự, hát đôi→song ca, hát tập→hợp ca, hát nhân→nguyên tử, hậu cần→tiếp liệu, học vị→bằng cấp, hệ quả→hậu quả, hiện đại→tối tân, hộ nhà→gia đình, hộ chiếu→sổ thông hành, họp hội→phân khu, họ khẩu→tổ khai gia đình, hội chữ thập đỏ→hội Hồng Thập Tự, kiều hời→ngoại tệ, kiệt xuất→giải/xuất sắc, kinh qua→trải qua, làm gái→làm điếm, làm việc→thẩm vấn/điều tra, lâu năm góc/nhà tráng→ngụy Giác Đốc/Tòa Bạch ốc, liên hoan→đại hội/ăn mừng, liên hệ→liên lạc, linh tinh→vỏ vần, lính gái→nữ quân nhân, lính thủy đánh bộ→thủy quân lực lượng chiến, lợi nhuận→lợi tức, lực tôm→tôm lực, lý giải→giải thích, máy bay lên thẳng→trực thăng, múa đòi→khiêu vũ, Mĩ→Mỹ, nằm bật→nằm ngửa, nâng cấp→nâng/đưa giá trị lên, năng nổ→siêng năng/tháo vát, nghệ nhân→thờ/nghệ sỹ, nghệ danh→Tên nghệ sỹ, nghĩa vụ quân sự→Đi quân dịch, nghiêm túc→nghiêm chính, nghiệp dư→đi làm thêm, nhà khách→khách sạn, nhất trí→đồng lòng/đồng ý, nhất quán→luôn luôn/trước sau như một, người nước ngoài→ngoại kiều, noi niệm→viễn suy tư, phân cứng→cường liệu, phân mềm→nhu liệu, phản ánh→phản ảnh, phản hồi→trả lời/hồi âm, phát sóng→phát thanh, phó tiến sĩ→cao học, phi khẩu→phi trường/phi cảng, phi vụ→một vụ trao đổi thường mại, phục hồi nhân phẩm→hoàn lượng, phương án→kế hoạch, quá tài→quá sướng/quá mức, quan triết→hiểu rõ, quân lý→quân trị, quảng trường→công trường, quân hàm→cấp bậc, quy hoạch→kế hoạch, quy trình→tiến trình, sốc→kinh hoàng/kinh ngạc/ngạc nhiên, sổ tân→tân cương, sư đoàn, sức khỏe công dân→y tế công cộng, sự cố→trở ngại, tạp đoàn/doanh nghiệp→công ty, tên lứa→hòa tiến, tham gia lưu thông→lưu hành, tham quan→thẩm viếng, thanh lý→thanh toán/chứng minh, thần thượng→thần mê, thi công→làm, thí phần→thí trường, thu nhập→lợi tức, thư giãn→tĩnh táo/giải trí, thuyết phục→có lý/hợp lý/tin được, tiến tiến→xuất sắc, tiến công→tấn công, tiếp thu→tiếp nhận/thâu nhận/lãnh hội, tiêu dùng→tiêu thụ, tổ lái→phi hành đoàn, tổ rơi→truyền đơn, tranh thủ→cố gắng, trí tuệ→kiến thức, triển khai→khai triển, tư duy→suy nghĩ, tư liệu→tài liệu, từ→tiếng/chữ, uốn tạc→tắt nghiêng, văn dân→văn đề, văn động viên→lực sĩ, viện ung bướu→viện ung thư, vô tư→tự nhiên, xác tín→chính xác, xe con→xe du lịch, xe khách→xe đồ, xử lý→giải quyết/thi hành)
```

## 11. LIÊN KẾT SKILLS
- **historical-book-translation**: Bước 1-3 quy trình dịch.
- **southern-vietnamese-editorial-style**: Dùng từ nối, trạng từ, đại từ VNCH.
- **historical-terminology-research**: Tra cứu thuật ngữ chuyên ngành (Lexicon + PDF).
- **translation-error-detection**: Phát hiện lỗi sai ngữ cảnh, dịch word-for-word.
- **deep-translation-review**: Kiểm tra ngữ cảnh khi audit.
- **translation-quality-gate**: Orthography check.

---

*Cập nhật: 2026-11-20 — Dựa trên Grammar Engine v2.1 §1-3, Audit 6 chương §15.4, Bảng Đối Chiếu Tiếng Việt (PDF: doi-chieu-tieng-viet.pdf, T.V.G., Đặc San Kỷ Niêm 25 Năm TNSP, ~120 cặp từ VNCH-VC).*