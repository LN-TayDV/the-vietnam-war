# STYLE_GUIDE PHẦN B — QUY CHUẨN NGÔN NGỮ MIỀN NAM VNCH (BẢN HOÀN CHỈNH)

> Phiên bản: 2.3 — Cập nhật sau Audit 6 chương đầu (2026-11-19): Quy tắc 18 (Alignment), 19 (Không dịch từng từ), 20 (Xử lý từ/câu khó), 21 (Chỉ định danh từ), 22 (Trạng từ không gian/thời gian), 23 (Thể khía), 24 (Đại từ nhân xưng), 25 (Từ nối logic), 26 (Bị động → Chủ động), 27 (Chống fabricate), 28 (Encoding), 29 (QA Gate).
> Ngày: 2026-11-19. UTF-8, NFC, không BOM.
> Nguồn bằng chứng: Lê Văn Đức 1970 (SRC-001/002), Bách Khoa 405 (SRC-009, OCR), Hiến pháp VNCH 1967 (SRC-023), Phan Khôi 1932 (SRC-021), TRANSLATION_GRAMMAR_ENGINE.md v2.0, FINAL_PILOT_QUALITY_GATE.md, AUDIT_REPORT_CH01-06.md.

## Nguyên tắc chung

Bản dịch dùng **tiếng Việt miền Nam** theo truyền thống ngôn ngữ, văn chương, báo chí và học thuật của **Việt Nam Cộng hòa trước năm 1975**. Đây là chuẩn bắt buộc xuyên suốt 77 chương.

**Phân biệt 5 lớp xác minh** (từ Phase 0):
1. Xác minh nguồn — nguồn tồn tại, đúng thư mục.
2. Xác minh nội dung — định nghĩa/cách dùng có trong nguồn.
3. Xác minh ngữ cảnh — cách dùng đúng ngữ cảnh.
4. Xác minh mức độ phổ biến — KHÔNG tự động suy ra từ 1 nguồn.
5. Xác minh sắc thái vùng miền/thời kỳ — phải có bằng chứng riêng.

---

## 14 QUY TẮC CHI TIẾT (Bản gốc v2.2)

### Quy tắc 1: Nguyên tắc lựa chọn từ vựng
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Ưu tiên dạng từ đã kiểm chứng trong nguồn VNCH (Lê Văn Đức, Bách Khoa, Hiến pháp VNCH). Khi có nhiều dạng, chọn dạng xuất hiện trong nguồn VNCH sơ cấp. |
| **Lý do** | Đảm bảo tính xác thực; tránh áp đặt từ hiện đại hoặc từ miền Bắc. |
| **Nguồn** | Lê Văn Đức 1970 (SRC-001/002), Bách Khoa 405 (SRC-009), Hiến pháp VNCH 1967 (SRC-023) |
| **Ví dụ đúng** | *chánh phủ* (Hiến pháp 1967, Điều 67: "Thủ Tướng điều khiển Chánh phủ") |
| **Ví dụ không nên dùng** | *chính phủ* (dạng hiện nay, không phải chuẩn VNCH) |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (có nguồn sơ cấp VNCH) |

### Quy tắc 2: Quy tắc sử dụng từ ngữ miền Nam
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Dùng dạng Nam Bộ cho từ vựng thường ngày, chính tả, và thuật ngữ chuyên ngành khi đã kiểm chứng. |
| **Lý do** | Phản ánh đúng truyền thống ngôn ngữ VNCH. |
| **Nguồn** | Lê Văn Đức 1970; ORTHOGRAPHY_DATABASE (20 quy tắc) |
| **Ví dụ đúng** | *chớ* (thay *mà/nhưng*), *nầy* (thay *này*), *gởi* (thay *gửi*), *thơ* (thay *thư*), *chừng nấy* (thay *chừng ấy*) |
| **Ví dụ không nên dùng** | *mà, này, gửi, thư, chừng ấy* trong văn phong Nam Bộ |
| **Phạm vi** | Văn viết học thuật VNCH; không áp dụng cho trích dẫn trực tiếp |
| **Mức độ chắc chắn** | VERIFIED (ORTHOGRAPHY CH-01 đến CH-20) |

### Quy tắc 3: Quy tắc dịch thuật ngữ kinh tế
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Dùng *tài chánh* (không *tài chính*), *địa ốc* (thay *bất động sản* khi ngữ cảnh VNCH), *hưu bổng* (thay *lương hưu*), *ngân khố* (cơ quan), *ngân sách* (kế hoạch chi thu). |
| **Lý do** | Phân biệt thuật ngữ VNCH với thuật ngữ hiện nay; giữ sắc thái lịch sử. |
| **Nguồn** | Lê Văn Đức 1970 (SRC-001: tài chánh, địa ốc, hưu bổng, ngân khố, quốc khố); Hiến pháp VNCH 1967 (SRC-023: ngân sách, Điều 46); Bách Khoa 405 (SRC-009: giấy bạc, tiền đồng, viện trợ, tái thiết) |
| **Ví dụ đúng** | *tài chánh* (ORTHOGRAPHY CH-15), *ngân khố* (Lê Văn Đức), *dự thảo ngân sách* (Hiến pháp 1967, Điều 46) |
| **Ví dụ không nên dùng** | *tài chính, lương hưu, ngân sách nhà nước* (thuật ngữ hiện nay) khi dịch văn bản VNCH |
| **Phạm vi** | Kinh tế, tài chính, ngân hàng, thương mại |
| **Mức độ chắc chắn** | VERIFIED (Lê Văn Đức + Hiến pháp VNCH) |

### Quy tắc 4: Quy tắc dịch thuật ngữ chính trị
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Dùng *chánh phủ, chánh đảng, chánh trị* (chánh = chính); *Dân biểu* (Hạ nghị viện), *Nghị sĩ* (Thượng nghị viện); *Tổng Thống, Thủ Tướng, Phó Tổng Thống*; *Tối cao Pháp viện*; *sắc luật, sắc lệnh, nghị định*. |
| **Lý do** | Thuật ngữ chính trị VNCH có hệ thống lưỡng viện (Hạ/Thượng nghị viện) khác với hệ thống hiện nay. |
| **Nguồn** | Hiến pháp VNCH 1967 (SRC-023: Điều 30-33, 51-52, 58, 76-81, 85-88); Lê Văn Đức 1970 (SRC-001: dân biểu, nghị sĩ, chánh phủ) |
| **Ví dụ đúng** | "Dân biểu được bầu theo lối phổ thông đầu phiếu" (Điều 31), "Chánh phủ" (Điều 67), "sắc luật" (Điều 64) |
| **Ví dụ không nên dùng** | *đại biểu Quốc hội* (thuật ngữ hiện nay), *chính phủ* (thiếu "h") |
| **Phạm vi** | Chính trị, hành chính, pháp luật, lập pháp, hành pháp, tư pháp |
| **Mức độ chắc chắn** | VERIFIED (Hiến pháp VNCH 1967 là văn kiện gốc) |

### Quy tắc 5: Quy tắc dịch thuật ngữ địa lý
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Dùng *địa dư, địa đồ, địa thế* (thay *địa lý* khi cần phân biệt); *tỉnh, quận, tổng, xã, ấp, làng* (hành chánh VNCH); *đô thị, nông thôn*; *lãnh thổ, hải phận*. |
| **Lý do** | Hệ thống hành chánh VNCH có cấp tổng (dưới quận), khác với hệ thống hiện nay. |
| **Nguồn** | Lê Văn Đức 1970 (SRC-001: địa dư, địa đồ, địa thế, địa giới); Hiến pháp VNCH 1967 (SRC-023: xã, tỉnh, thị xã, thủ đô, Điều 70-73); Bách Khoa 405 (SRC-009: đô thị, nông thôn) |
| **Ví dụ đúng** | "Xã, Tỉnh, Thị xã, và Thủ đô" (Hiến pháp 1967, Điều 70), *đô thị* (Bách Khoa 405) |
| **Ví dụ không nên dùng** | *thành phố* (thay *thị xã* trong ngữ cảnh hành chánh VNCH) |
| **Phạm vi** | Địa lý, hành chánh địa phương, dân cư |
| **Mức độ chắc chắn** | VERIFIED (Lê Văn Đức + Hiến pháp VNCH + Bách Khoa) |

### Quy tắc 6: Quy tắc dịch thuật ngữ lịch sử
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Dùng *triều đại, triều đình, hoàng đế* (thay *vua* khi trang trọng); *thực dân, thuộc địa* (thời thuộc Pháp); *cộng hòa, lập hiến, lập pháp, hành pháp, tư pháp* (VNCH). |
| **Lý do** | Giữ sắc thái lịch sử; phân biệt thời kỳ. |
| **Nguồn** | Lê Văn Đức 1970 (SRC-001: triều đại, thực dân, thuộc địa); Hiến pháp VNCH 1967 (SRC-023: cộng hòa, lập hiến, tam quyền, Điều 1-3); Bách Khoa 405 (SRC-009: hoàng đế, hội nghị) |
| **Ví dụ đúng** | "chánh thể Cộng Hòa" (Hiến pháp 1967, Lời mở đầu), "tam quyền" (Điều 3) |
| **Ví dụ không nên dùng** | *chế độ cộng hòa* (thiếu "h" và "thể") |
| **Phạm vi** | Lịch sử, chính trị, quân sự |
| **Mức độ chắc chắn** | VERIFIED (Lê Văn Đức + Hiến pháp VNCH) |

### Quy tắc 7: Cú pháp và cấu trúc câu
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Giữ cấu trúc câu học thuật VNCH: câu dài vừa phải, dùng *song, tuy nhiên, tuy vậy* (không *tuy nhiên* quá Bắc); dùng *chớ* (thay *mà/nhưng*) khi nhấn mạnh tương phản; dùng *vả* (bổ sung lý lẽ). |
| **Lý do** | Văn phong VNCH có nhịp điệu riêng, không nặng hành chính Bắc. |
| **Nguồn** | GRAMMAR_DATABASE.md; Phan Khôi 1932 (SRC-021); Bách Khoa 405 (SRC-009) |
| **Ví dụ đúng** | "chớ" (ORTHOGRAPHY CH-04), "vả" (CH-08), "song/tuy nhiên/tuy vậy" |
| **Ví dụ không nên dùng** | Câu ngắn cụt kiểu Bắc; "đồng chí" trong văn trung tính |
| **Phạm vi** | Toàn bộ văn dịch |
| **Mức độ chắc chắn** | VERIFIED (GRAMMAR_DATABASE + ORTHOGRAPHY) |

### Quy tắc 8: Cách diễn đạt theo văn phong sách khảo cứu
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Dùng giọng văn học thuật trung tính, trang trọng; tránh khẩu ngữ (ổng, bả, ảnh, mầy, tao) trong thân bài; chỉ dùng trong trích dẫn trực tiếp. |
| **Lý do** | Sách khảo cứu VNCH có giọng trí thức Nam Bộ. |
| **Nguồn** | Bách Khoa 405 (SRC-009: văn phong tạp chí học thuật); STYLE_GUIDE Phần B.3(d) |
| **Ví dụ đúng** | *ông ấy, bà ấy, người ấy, các ông, họ* (thay *ổng, bả, ảnh*) |
| **Ví dụ không nên dùng** | *ổng, bả, ảnh, mầy, tao, hả, hén, nghen, à nha* trong thân bài |
| **Phạm vi** | Văn phân tích, nghị luận, khảo cứu |
| **Mức độ chắc chắn** | VERIFIED (Bách Khoa 405 + STYLE_GUIDE) |

### Quy tắc 9: Xử lý thuật ngữ không có tương đương trực tiếp
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Giữ nguyên thuật ngữ gốc (in nghiêng) + giải nghĩa lần đầu; không tự tạo từ mới không có nguồn. |
| **Lý do** | Tránh bịa thuật ngữ; giữ tính học thuật. |
| **Nguồn** | STYLE_GUIDE Phần D.4; uncertain_terms.md |
| **Ví dụ đúng** | *domino theory* → *thuyết domino* (giải nghĩa lần đầu) |
| **Ví dụ không nên dùng** | Tự dịch *domino theory* thành *thuyết quân cờ domino* (không có nguồn) |
| **Phạm vi** | Thuật ngữ chuyên ngành mới, thuật ngữ quân sự, ngoại giao |
| **Mức độ chắc chắn** | PARTIALLY_VERIFIED (cần uncertain_terms.md) |

### Quy tắc 10: Xử lý thuật ngữ có nhiều nghĩa
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Phân tích ngữ cảnh; không tự động đồng nhất các nghĩa. Ví dụ: *bảo hộ* (protectorate) vs *bảo hộ mậu dịch* (protectionism). |
| **Lý do** | Từ đồng âm khác nghĩa; nhầm lẫn làm sai lệch nội dung. |
| **Nguồn** | Lê Văn Đức 1970 (SRC-001: bảo hộ = protectorate; bảo hộ mậu dịch = protectionism) |
| **Ví dụ đúng** | *bảo hộ* (thuộc địa) vs *bảo hộ mậu dịch* (kinh tế) |
| **Ví dụ không nên dùng** | Dùng *bảo hộ* cho cả hai nghĩa |
| **Phạm vi** | Thuật ngữ đa nghĩa |
| **Mức độ chắc chắn** | VERIFIED (Lê Văn Đức) |

### Quy tắc 11: Quy tắc chú thích và giữ nguyên thuật ngữ gốc
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Cước chú giữ nguyên vị trí theo trang; tên riêng & tựa tiếng Anh/Pháp giữ nguyên; URL giữ nguyên. |
| **Lý do** | Giữ tính học thuật và truy xuất nguồn. |
| **Nguồn** | STYLE_GUIDE Phần D.1 |
| **Ví dụ đúng** | `[ND: …]` cho chú thích người dịch; tên riêng giữ nguyên |
| **Ví dụ không nên dùng** | Gom cước chú về cuối chương; tạo "Thư mục tham khảo" riêng |
| **Phạm vi** | Toàn bộ cước chú 77 chương |
| **Mức độ chắc chắn** | VERIFIED (STYLE_GUIDE) |

### Quy tắc 12: Quy tắc không hiện đại hóa văn phong một cách tùy tiện
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Không thay thuật ngữ VNCH bằng thuật ngữ hiện nay (dân biểu → đại biểu, chánh phủ → chính phủ, tài chánh → tài chính) khi dịch văn bản VNCH. |
| **Lý do** | Giữ sắc thái lịch sử; thuật ngữ VNCH phản ánh hệ thống chính trị VNCH. |
| **Nguồn** | HISTORICAL_USAGE_TRACKING.md (G5); Hiến pháp VNCH 1967 (SRC-023) |
| **Ví dụ đúng** | *Dân biểu* (VNCH Hạ nghị viện) |
| **Ví dụ không nên dùng** | *đại biểu Quốc hội* (hiện nay) |
| **Phạm vi** | Văn bản VNCH, lịch sử VNCH |
| **Mức độ chắc chắn** | VERIFIED (Hiến pháp VNCH + Lê Văn Đức) |

### Quy tắc 13: Quy tắc phân biệt văn phong dịch với văn phong nguyên tác tiếng Việt
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Khi nguyên tác là văn bản tiếng Việt (Lê Văn Đức, Bách Khoa, Hiến pháp), giữ nguyên văn phong; khi dịch từ tiếng Anh/Pháp, dùng văn phong VNCH nhất quán. |
| **Lý do** | Tránh lẫn lộn văn phong dịch và văn phong nguyên tác. |
| **Nguồn** | STYLE_GUIDE Phần A; Phase 0 reconciliation |
| **Ví dụ đúng** | Trích Hiến pháp 1967 giữ nguyên "chánh phủ"; dịch Cambridge dùng "chánh phủ" nhất quán |
| **Ví dụ không nên dùng** | Trộn *chính phủ* (dịch) và *chánh phủ* (nguyên tác) |
| **Phạm vi** | Toàn bộ dự án |
| **Mức độ chắc chắn** | VERIFIED (STYLE_GUIDE) |

### Quy tắc 14: Cơ chế ghi nhận quyết định dịch thuật
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Mỗi quyết định dịch thuật quan trọng phải ghi vào `translation_decisions.md` với: quy tắc áp dụng, lý do, nguồn, ví dụ, phạm vi, mức độ chắc chắn. |
| **Lý do** | Truy xuất quyết định; tránh bất nhất. |
| **Nguồn** | STYLE_GUIDE Phần E; PHASE0_RECONCILIATION_REPORT.md |
| **Ví dụ đúng** | Ghi "Dân biểu: VERIFIED (Hiến pháp 1967, Điều 31)" |
| **Ví dụ không nên dùng** | Quyết định không ghi nguồn |
| **Phạm vi** | Toàn bộ dự án |
| **Mức độ chắc chắn** | VERIFIED (cơ chế) |

### Quy tắc 15: Xử lý tên gọi thuộc địa và địa danh ngoại quốc
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Khi nguyên tác dùng tên gọi thuộc địa Pháp (*Annam, Tonkin, Cochinchine, Đông Dương*), dùng tên gọi Việt Nam tương ứng: **Nam Kỳ** (Cochinchina), **Trung Kỳ** (Annam), **Bắc Kỳ** (Tonkin), **Đông Dương** (Indochine). Không giữ nguyên tên gọi Pháp trong bản dịch để tránh lộn xộn thuật ngữ, đảm bảo văn phong VNCH tự nhiên, thuận miệng. |
| **Lý do** | Văn phong VNCH ưu tiên tên gọi bản địa. Giữ tên thuộc địa Pháp trong ngoặc làm rối câu văn, không phù hợp với sách dịch Việt Nam miền Nam. Tên gọi bản địa đã đủ rõ ngữ cảnh lịch sử. |
| **Nguồn** | Lê Văn Đức 1970 (SRC-001: Nam Kỳ, Trung Kỳ, Bắc Kỳ); Hiến pháp VNCH 1967 (SRC-023) |
| **Ví dụ đúng** | "Gọi là Nam Kỳ và Bắc Kỳ, các xứ này vẫn do quan lại triều Nguyễn cai trị" |
| **Ví dụ không nên dùng** | "Gọi là *Annam* (Trung Kỳ) và *Tonkin* (Bắc Kỳ)" (giữ tên Pháp làm rối câu, không văn phong VNCH) |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Lê Văn Đức 1970 + văn phong VNCH) |

### Quy tắc 16: Kiểm tra hoàn tất bản dịch
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Sau khi dịch xong một đoạn, đối chiếu số câu trong nguyên tác và bản dịch. Không để câu bỏ lửng. Mỗi đoạn dịch phải kết thúc ở dấu chấm hết, không ở dấu gạch ngang giữa câu. |
| **Lý do** | Pilot V1-Ch1 P012 bị cắt giữa đoạn ("Thuật ngữ này —"), thiếu 3 câu cuối — lỗi CRITICAL. |
| **Nguồn** | FINAL_PILOT_QUALITY_GATE.md (CRITICAL-1); TRANSLATION_GRAMMAR_ENGINE.md (Bước 6–7) |
| **Ví dụ đúng** | Đoạn kết thúc bằng dấu chấm, đủ số câu như nguyên tác, không bỏ sót thông tin. |
| **Ví dụ không nên dùng** | "Thuật ngữ này —" (bỏ lửng, thiếu phần giải thích nghĩa "ái quốc" + Nguyễn Ái Quốc) |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Quality Gate + Grammar Engine) |

### Quy tắc 17: Quy trình dịch thuật 7 bước
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Áp dụng quy trình 7 bước trong `TRANSLATION_GRAMMAR_ENGINE.md` cho mỗi đoạn: (1) Phân tích ngữ pháp nguyên tác; (2) Xác định chủ thể, vị ngữ, đối tượng; (3) Phân tích quan hệ logic giữa các mệnh đề; (4) Xác định thuật ngữ theo ngữ cảnh; (5) Tái cấu trúc thành câu tiếng Việt tự nhiên; (6) Đối chiếu lại nguyên tác; (7) Kiểm tra tính dễ hiểu. |
| **Lý do** | Bảo đảm mỗi câu dịch đạt đồng thời 3 điều kiện: đúng nghĩa nguyên tác, đúng ngữ pháp tiếng Việt, truyền đạt rõ ràng ý tưởng tác giả. |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (Giai đoạn 1 mở rộng) |
| **Ví dụ đúng** | Áp dụng đủ 7 bước cho mỗi đoạn; chạy checklist Sentence (S1–S20), Paragraph (P1–P10), Chapter (C1–C10). |
| **Ví dụ không nên dùng** | Dịch từng từ rồi ghép lại; bỏ qua bước đối chiếu (Bước 6); không kiểm tra dễ hiểu (Bước 7). |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0) |

---

## QUY TẮC MỞ RỘNG TỪ AUDIT 6 CHƯƠNG ĐẦU (v2.3)

### Quy tắc 18: Alignment đoạn văn (Paragraph Alignment) — BẮT BUỘC
| Mục | Nội dung |
|---|---|
| **Quy tắc** | **Trước khi build DOCX, bắt buộc kiểm tra `số đoạn src == số đoạn vi`**. Mỗi đoạn trong file dịch phải tương ứng 1-1 với đoạn trong file nguồn, giữ nguyên marker `[V1CNN-Pxxx] (trang X)`. Không được gộp nhiều đoạn gốc thành 1 đoạn dịch, không được tách 1 đoạn gốc thành nhiều đoạn dịch. |
| **Lý do** | Audit 6 chương: Ch1 lệch từ P008, thiếu 11 đoạn cuối; Ch5 chỉ có 9 block thay vì 15 đoạn. Dẫn đến mất nội dung, cước chú neo sai vị trí. |
| **Nguồn** | AUDIT_REPORT_CH01-06.md (§2.1); build_chapter_docx.py (yêu cầu mapping 1-1) |
| **Cách kiểm tra** | Chạy `python 99_scripts/debug_align.py NN` trước khi build DOCX. Script so sánh số đoạn, số câu src vs vi. |
| **Ví dụ đúng** | Ch1: 49 src paragraphs = 49 vi paragraphs; Ch5: 15 src = 15 vi (sau khi realign). |
| **Ví dụ không nên dùng** | Ch1 gốc: 49 src vs 50 vi (lệch); Ch5 gốc: 15 src vs 9 vi (gộp block). |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Audit 6 chương + build script requirement) |

### Quy tắc 19: Cấm dịch từng từ rồi ghép lại (Word-for-Word Translation) — CẤM KỊ
| Mục | Nội dung |
|---|---|
| **Quy tắc** | **TUYỆT ĐỐI CẤM** dịch từng từ/cụm từ riêng lẻ rồi ghép lại thành câu. Phải đọc và phân tích **toàn bộ câu, đoạn văn, ngữ cảnh trước sau** để xác định ý tác giả, sau đó tái cấu trúc thành câu tiếng Việt tự nhiên theo văn phong VNCH (Bước 5, Grammar Engine v2.0). |
| **Lý do** | Audit 6 chương: Nhiều câu bị dịch máy từng từ (chính phủ, giải phóng, đồng chí, Annam/Tonkin) tạo ra câu cứng, sai ngữ pháp, sai thuật ngữ. |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (Bước 5 + VNCH Grammar Database); AUDIT_REPORT_CH01-06.md (§2.2, §15.4) |
| **Quy trình bắt buộc** | 1. Đọc toàn câu → 2. Phân tích chủ thể/vị ngữ/đối tượng → 3. Xác định quan hệ logic → 4. Tra lexicon/VNCH Grammar cho thuật ngữ → 5. Tái cấu trúc câu Việt tự nhiên → 6. Đối chiếu lại nguyên tác. |
| **Ví dụ đúng** | "A man named Lê Lợi... brought to an end..." → "Một người tên là Lê Lợi, vị vua sáng lập triều Lê, đã chấm dứt thời kỳ ngắn ngủi nầy." (chủ động hóa, chỉ định *thời kỳ nầy*, thể hoàn thành *đã...*). |
| **Ví dụ không nên dùng** | "Một người tên là Lê Lợi... bị chấm dứt bởi..." (bê nguyên bị động, không chủ động hóa, sai chỉ định/thể). |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0 + Audit 6 chương) |

### Quy tắc 20: Xử lý từ/câu khó — Quy trình 5 bước bắt buộc
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Khi gặp từ hoặc câu khó hiểu, **KHÔNG** được: đánh dấu `UNRESOLVED`, bỏ qua, giữ nguyên, hay dịch từng từ. Phải thực hiện lần lượt 5 bước: (1) Mở rộng phân tích sang toàn bộ đoạn văn, đoạn trước/sau, chương, phần liên quan; (2) Xác định chủ đề, lập luận, sự kiện, nhân vật, ý đồ tác giả; (3) Tra cứu từ điển, tài liệu chuyên ngành, nguồn lịch sử; (4) Đối chiếu cách dùng từ trong các phần khác của sách; (5) Tái dựng ý nghĩa tác giả → diễn đạt tiếng Việt tự nhiên theo văn phong VNCH. |
| **Ghi nhận căn cứ bắt buộc** | - Ghi lại căn cứ văn bản, ngữ cảnh, nguồn tra cứu, lập luận. - Phân biệt rõ: nghĩa nguyên văn / nghĩa theo ngữ cảnh / cách diễn đạt bản dịch. - Đánh giá mức độ chắc chắn và lý do. - Nếu mâu thuẫn → tiếp tục mở rộng nghiên cứu. - Không tự ý suy diễn. Nếu buộc chọn khi chưa đủ chứng cứ → chọn cách hiểu có căn cứ tốt nhất, ghi rõ mức độ chắc chắn và lý do trong báo cáo QA. |
| **Lý do** | Audit 6 chương: Nhiều từ/câu khó bị bỏ qua hoặc dịch sai do không làm theo quy trình hệ thống. |
| **Nguồn** | AUDIT_REPORT_CH01-06.md (§15.4); Yêu cầu người dùng 2026-11-19 |
| **Ví dụ đúng** | "giải phóng" trong "Cờ Giải Phóng" → dịch "độc lập" trong thân bài, giữ "Giải Phóng" trong tên riêng có ghi chú. Mức độ chắc chắn 95% (Style Guide Rule 8, 15). |
| **Ví dụ không nên dùng** | Dịch "giải phóng" → "giải phóng" khắp nơi (thuật ngữ Cộng sản), hoặc bỏ qua do khó. |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Yêu cầu người dùng + Audit 6 chương) |

### Quy tắc 21: Chỉ định danh từ (Classifiers) — Nam Bộ
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Khi dịch danh từ có "a/an/the" hoặc không có chỉ định, **bắt buộc thêm chỉ định phù hợp theo Nam Bộ (VNCH)** theo bảng Grammar Engine §1.3: *con* (người/trẻ), *cây* (đồ dài), *cục* (khối), *cái* (tổng quát), *cuốn* (sách/báo), *cái/bài* (bài viết ngắn). |
| **Lý do** | Tiếng Việt Nam Bộ dùng chỉ định nhiều và chính xác hơn tiếng Việt chung. Thiếu chỉ định làm câu thiếu tự nhiên, bị coi là "ngữ pháp kém". |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (§1.3); Phan Khôi 1955 (SRC-021); Lê Văn Đức 1970 (SRC-001) |
| **Ví dụ đúng** | "a book" → *một cuốn sách*; "a period" → *một thời kỳ nầy*; "an article" → *một cái bài*; "a man" → *một con người / một người ấy*. |
| **Ví dụ không nên dùng** | "a book" → *một sách* (thiếu chỉ định *cuốn*); "a period" → *một kỳ* (thiếu *thời kỳ*). |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0 + Phan Khôi 1955) |

### Quy tắc 22: Trạng từ không gian/thời gian — nầy/đó/kia
| Mục | Nội dung |
|---|---|
| **Quy tắc** | **BẮT BUỘC** dùng *nầy* (gần người nói), *đó* (gần người nghe), *kia* (xa) thay vì *này, đó, kia* chung chung. Trạng từ thời gian: *ngày nầy, năm nầy, lúc nầy, trước nầy, sau nầy*. |
| **Lý do** | Phân biệt 3 cấp độ khoảng cách là đặc trưng văn phong VNCH (Phan Khôi, Kỳ 5-6). Dùng *này* cho tất cả là đặc trưng miền Bắc/hiện nay. |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (§1.4); Phan Khôi 1955 (SRC-021, Kỳ 5-6) |
| **Ví dụ đúng** | "ngày nầy", "năm nầy", "trước nầy", "sau nầy", "người nầy", "vấn đề nầy". |
| **Ví dụ không nên dùng** | "ngày này", "năm này", "trước đây", "sau này", "người này", "vấn đề này" (trừ cụ trúc "trong này, ngoài này, trước này, sau này" - giữ "này"). |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0 + Phan Khôi 1955) |

### Quy tắc 23: Thể khía (Aspect) — đã...rồi/đang/sẽ/vừa...mới/chưa
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Dùng thể khía đầy đủ Nam Bộ: Hoàn thành *đã... rùi/đã... hẵng*; Đang diễn ra *đang... nha/đang... nãy* (văn nói) / *đang... xong/đang tiến hành* (văn viết); Sắp tới *sắp... sẽ/chuẩn bị... sẽ*; Vừa mới *vừa... mới/mới... xong*; Chưa *chưa... bao giờ/vẫn chưa*. Văn học thuật dùng dạng đầy đủ hơn hội thoại. |
| **Lý do** | Tiếng Việt Nam Bộ phân biệt thể khía rõ rệt; dạng rút gọn *đang/đã/sẽ* là đặc trưng miền Bắc/hội thoại. |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (§1.5); Phan Khôi 1955 (SRC-021) |
| **Ví dụ đúng** | "đã ký kết rùi", "đang tiến hành ký kết", "sắp sẽ ký", "vừa ký xong", "chưa bao giờ ký". |
| **Ví dụ không nên dùng** | "đã ký", "đang ký", "sẽ ký", "vừa ký", "chưa ký" (dạng rút gọn). |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0 + Phan Khôi 1955) |

### Quy tắc 24: Đại từ nhân xưng — người ấy/ông ấy/bà ấy
| Mục | Nội dung |
|---|---|
| **Quy tắc** | **BẮT BUỘC** dùng *người ấy, ông ấy, bà ấy* (người thứ 3 đơn số); *họ, những người ấy* (số nhiều). **CẤM** dùng *hắn, y, nó* chỉ người; *ta, tui, mình* (người 1); *mày, tao, cậu* (người 2) trong thân bài học thuật. |
| **Lý do** | Văn phong sách VNCH trang trọng, phân biệt giới tính và quan hệ xã hội. |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (§1.7); Phan Khôi 1955 (SRC-021) |
| **Ví dụ đúng** | "Người ấy lập luận rằng...", "Ông ấy là nhà sử học...", "Họ đã ký hiệp định...". |
| **Ví dụ không nên dùng** | "Hắn lập luận rằng...", "Nó là nhà sử học...", "Ta thấy rằng...". |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0 + Phan Khôi 1955) |

### Quy tắc 25: Từ nối logic Nam Bộ — dầu/dẫu, trái lại, tuy vậy, bởi thế, vả
| Mục | Nội dung |
|---|---|
| **Quy tắc** | **Ưu tiên** dùng từ nối Nam Bộ: Nhượng bộ *dầu, dẫu* (thay *mặc dù*); Tương phản *trái lại* (thay *ngược lại*); Chuyển ý *tuy vậy, đã vậy, song* (thay *tuy nhiên*); Nhân quả *bởi thế, do đó, cho nên* (thay *vì vậy*); Bổ sung *vả, lại, cũng* (thay *hơn nữa*). |
| **Lý do** | Từ nối Nam Bộ tạo nhịp điệu văn phong VNCH tự nhiên, khác biệt rõ rệt với miền Bắc. |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (§1.8); Phan Khôi 1955 (SRC-021); Bách Khoa 405 (SRC-009) |
| **Ví dụ đúng** | "Dầu đã nỗ lực...", "Trái lại, miền Nam...", "Tuy vậy, kết quả...", "Bởi thế, chánh phủ...", "Vả, còn có...". |
| **Ví dụ không nên dùng** | "Mặc dù...", "Ngược lại...", "Tuy nhiên...", "Vì vậy...", "Hơn nữa...". |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0 + Phan Khôi 1955) |

### Quy tắc 26: Bị động → Chủ động (Active Voice Preference)
| Mục | Nội dung |
|---|---|
| **Quy tắc** | **LUÔN ƯU TIÊN CHỦ ĐỘNG HÓA** câu bị động tiếng Anh nếu tiếng Việt tự nhiên hơn (Grammar Engine §1.6: "QUY TẮC VÀNG"). Câu bị động *bị + V* chỉ dùng khi mang sắc thái tiêu cực ("bị trấn áp", "bị tước đoạt"). Câu bị động *được + V* hiếm dùng → chuyển chủ động ("người ta ký" thay "được ký"). Thể kiện *tự + V / V + ra/khỏi* cho sự việc tự phát. |
| **Lý do** | Tiếng Việt ưu tiên chủ động; câu bị động tiếng Anh thường cồng kềnh khi dịch sang Việt. |
| **Nguồn** | TRANSLATION_GRAMMAR_ENGINE.md v2.0 (§1.6); Clark 1974 (SRC-024); Thompson 1987 (SRC-022) |
| **Ví dụ đúng** | "was brought to an end by Lê Lợi" → "Lê Lợi đã chấm dứt..."; "was signed by the government" → "Chánh phủ đã ký...". |
| **Ví dụ không nên dùng** | "được ký bởi chánh phủ", "bị chấm dứt bởi Lê Lợi" (trừ khi mang ý tiêu cực: "bị trấn áp"). |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Grammar Engine v2.0 + Clark 1974) |

### Quy tắc 27: Chống Fabricate — Không bịa số trang, trích dẫn, ví dụ
| Mục | Nội dung |
|---|---|
| **Quy tắc** | **TUYỆT ĐỐI CẤM** bịa đặt số trang, trích dẫn, ví dụ, sự kiện, nhân vật không có trong nguyên tác. Mọi thông tin trong bản dịch phải truy xuất được về nguyên tác. Nếu cần bổ sung ngữ cảnh → dùng cước chú `[ND: ...]` và ghi rõ là bổ sung của người dịch. |
| **Lý do** | Audit 6 chương: Không có fabricate, nhưng cần khẳng định lại để phòng ngừa. |
| **Nguồn** | STYLE_GUIDE Phần B.3(c); AUDIT_REPORT_CH01-06.md |
| **Ví dụ đúng** | Chỉ dịch những gì có trong nguyên tác; bổ sung ngữ cảnh dùng `[ND: Người dịch bổ sung...]`. |
| **Ví dụ không nên dùng** | Thêm năm tháng, tên người, sự kiện không có trong sách gốc. |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (Style Guide + Audit) |

### Quy tắc 28: Encoding chuẩn — UTF-8, NFC, no BOM, LF
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Mọi file `.txt`, `.md`, `.csv`, `.py`, `.json` **BẮT BUỘC** dùng **UTF-8, NFC, không BOM, newline LF (`\n`)**. Python: `encoding="utf-8", newline="\n"`. PowerShell: **KHÔNG** dùng heredoc cho tiếng Việt (cp1252 issue) — dùng Python script. |
| **Lý do** | Tránh lỗi font, dấu thanh, dấu câu khi đọc/ghi file tiếng Việt trên Windows. |
| **Nguồn** | SKILL.md (§6); AUDIT_REPORT_CH01-06.md |
| **Kiểm tra** | `python -c "import sys; f=open('file.txt','rb'); b=f.read(); print('UTF-8:', all(b[i]<128 or (b[i]>>5)==6 and b[i+1]>>6==2 for i in range(len(b)-1) if b[i]>>5==6))"` hoặc dùng script check. |
| **Phạm vi** | Toàn bộ dự án |
| **Mức độ chắc chắn** | VERIFIED (SKILL.md + Audit) |

### Quy tắc 29: Quality Gate 8 tiêu chí — Chỉ HOAN_TAT khi tất cả PASS
| Mục | Nội dung |
|---|---|
| **Quy tắc** | Chương chỉ được đánh dấu `HOAN_TAT` khi **cả 8 tiêu chí PASS**: (1) Encoding UTF-8/NFC/no BOM/LF; (2) Orthography 0× "chính trị", 0× từ miền Bắc không phù hợp; (3) Đồng bộ đoạn: src = vi; (4) Đồng bộ cước chú: src = vi; (5) Không fabricate; (6) Văn phong tự nhiên, không dịch từng từ; (7) DOCX tồn tại 09_docx/, sinh bởi `build_chapter_docx.py`; (8) DOCX cước chú: `OK N/N`, Word `Footnotes.Count` = `notes` trong progress.json, footnote chân trang 9pt, đánh số 1..N. |
| **Lý do** | Đảm bảo chất lượng xuất bản nhất quán; tránh đánh dấu HOAN_TAT khi còn lỗi. |
| **Nguồn** | SKILL.md (§9); AUDIT_REPORT_CH01-06.md (§4) |
| **Phạm vi** | Toàn bộ 77 chương |
| **Mức độ chắc chắn** | VERIFIED (SKILL.md + Audit 6 chương) |

---

## Bảng tổng hợp: Thuật ngữ VNCH cần dùng (có nguồn) — CẬP NHẬT V2.3

| Thuật ngữ VNCH | Dạng hiện nay | Nguồn | Quy tắc |
|---|---|---|---|
| chánh phủ | chính phủ | SRC-001, SRC-009, SRC-023 | 1, 4, 12 |
| chánh trị | chính trị | SRC-001 | 1, 4, 12 |
| chánh đảng | chính đảng | SRC-023 | 4 |
| đảo chánh | đảo chính | SRC-001 | 1 |
| tài chánh | tài chính | SRC-001, ORTHO CH-15 | 3 |
| dân biểu | đại biểu | SRC-001, SRC-023 | 4 |
| nghị sĩ | đại biểu Quốc hội | SRC-001, SRC-023 | 4 |
| địa ốc | bất động sản | SRC-001 | 3 |
| hưu bổng | lương hưu | SRC-001 | 3 |
| ngân khố | ngân sách (cơ quan) | SRC-001 | 3 |
| ngân sách | ngân sách (kế hoạch) | SRC-023 | 3 |
| sắc luật | (không có) | SRC-023 | 4 |
| tối cao pháp viện | tòa án tối cao | SRC-023 | 4 |
| giám sát viện | (không có) | SRC-023 | 4 |
| đặc biệt pháp viện | (không có) | SRC-023 | 4 |
| chớ | mà/nhưng | ORTHO CH-04 | 2, 7, 25 |
| nầy | này | ORTHO CH-01 | 2, 22 |
| dầu/dẫu | mặc dù | ORTHO CH-02 | 2, 25 |
| vả | hơn nữa | ORTHO CH-08 | 2, 7, 25 |
| Trái lại | ngược lại | GRAMMAR §1.8 | 25 |
| Tuy vậy/Đã vậy | tuy nhiên | GRAMMAR §1.8 | 25 |
| Bởi thế/Do đó | vì vậy | GRAMMAR §1.8 | 25 |
| Nam Kỳ | Cochinchina/Cochinchine | SRC-001 | 15 |
| Trung Kỳ | Annam | SRC-001 | 15 |
| Bắc Kỳ | Tonkin | SRC-001 | 15 |
| Đông Dương | Indochine | SRC-001 | 15 |
| độc lập | giải phóng | SRC-001, SRC-023 | 8, 15 |
| đồng đạo | đồng chí | SRC-001, SRC-023 | 8 |
| người ấy/ông ấy/bà ấy | hắn/y/nó (người) | GRAMMAR §1.7 | 24 |
| đã... rùi/hẵng | đã | GRAMMAR §1.5 | 23 |
| đang... xong/tiến hành | đang | GRAMMAR §1.5 | 23 |
| sắp sẽ/chuẩn bị sẽ | sẽ | GRAMMAR §1.5 | 23 |
| vừa... mới/mới... xong | vừa mới | GRAMMAR §1.5 | 23 |
| chưa... bao giờ/vẫn chưa | chưa | GRAMMAR §1.5 | 23 |
| con/cái/cuốn/cây/cục/bài | (thiếu chỉ định) | GRAMMAR §1.3 | 21 |

---

## Trạng thái

**STYLE_GUIDE_B: v2.3 — 29 QUY TẮC (ĐÃ CẬP NHẬT SAU AUDIT 6 CHƯƠNG)**

- Quy tắc 1–17: Bản v2.2 (đã có).
- Quy tắc 18: Alignment đoạn văn (BẮT BUỘC).
- Quy tắc 19: Cấm dịch từng từ (CẤM KỊ).
- Quy tắc 20: Xử lý từ/câu khó (5 bước bắt buộc).
- Quy tắc 21–26: VNCH Grammar Database tích hợp (chỉ định, trạng từ, thể, đại từ, từ nối, chủ động hóa).
- Quy tắc 27: Chống fabricate.
- Quy tắc 28: Encoding chuẩn.
- Quy tắc 29: Quality Gate 8 tiêu chí.

**CẦN NGƯỜI DÙNG DUYỆT TRƯỚC KHI ÁP DỤNG CHO 77 CHƯƠNG TIẾP THEO.**