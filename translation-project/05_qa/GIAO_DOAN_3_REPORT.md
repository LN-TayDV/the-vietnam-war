# GIAI ĐOẠN 3 — BÁO CÁO SỬA LỖI VÀ KIỂM TRA ĐỘC LẬP

> Ngày: 2026-11-18. UTF-8, NFC, không BOM.
> Chương: V1-Ch1 (trang 27–31, 12 đoạn).
> Mục tiêu: Sửa 6 lỗi từ Final Quality Gate, khôi phục P008–P012, chạy 2 vòng kiểm tra độc lập.

---

## 1. Sửa lỗi (6 lỗi)

| # | Mức độ | Đoạn | Lỗi | Sửa | Trạng thái |
|---|---|---|---|---|---|
| 1 | CRITICAL | P012 | Bản dịch cắt giữa đoạn ("Thuật ngữ này —"), thiếu 3 câu cuối | Hoàn tất: thêm nghĩa "ái quốc" = "yêu nước, thương nước"; khái niệm phương Tây; Nguyễn Ái Quốc | ✅ ĐÃ SỬA |
| 2 | MAJOR | P011 | "Gọi là Trung Kỳ và Bắc Kỳ" (mất tên thuộc địa Pháp) | "Gọi là *Annam* (Trung Kỳ) và *Tonkin* (Bắc Kỳ)" | ✅ ĐÃ SỬA |
| 3 | MAJOR | P012 | "tại Trung Kỳ và Bắc Kỳ" (mất tên thuộc địa Pháp) | "tại *Annam* (Trung Kỳ) và *Tonkin* (Bắc Kỳ)" | ✅ ĐÃ SỬA |
| 4 | MINOR | P001 | "mặt trận hợp nhất" (không chuẩn) | "mặt trận thống nhất" (có nguồn: SRC-023, Điều 1) | ✅ ĐÃ SỬA |
| 5 | MINOR | P010 | "chấm dứt bởi" (bị động cứng) | "Một người tên là Lê Lợi... đã chấm dứt thời kỳ ngắn ngủi ấy." (chủ động) | ✅ ĐÃ SỬA |
| 6 | MINOR | P011 | "polymath" → "học giả lỗi lạc" (mất nghĩa) | "nhà bác học" (đúng nghĩa polymath) | ✅ ĐÃ SỬA |

## 2. Khôi phục tệp nguồn

- `v1_ch01_src.txt`: bổ sung P008–P012 (trang 29–31) + cước chú [4]–[9].
- Trước: 29 dòng (P001–P007 + [1]–[3]).
- Sau: 53 dòng (P001–P012 + [1]–[9]).
- Encoding: PASS (UTF-8, NFC, LF, no BOM).

## 3. Vòng kiểm tra 1 — Đối chiếu nguyên tác

Đối chiếu từng đoạn P001–P012 và cước chú [1]–[9] giữa bản dịch (`v1_ch01_vi.txt`) và nguyên tác (`v1_ch01_src.txt`):

| Đoạn | Đối chiếu | Kết quả |
|---|---|---|
| P001 | "united front" → "mặt trận thống nhất" ✅; mọi thành phần khác khớp | ✅ PASS |
| P002 | Trích Hồ Chí Minh + 10 Điều nên: khớp từng mục | ✅ PASS |
| P003 | "Dầu... Dẫu... Bởi thế... soi bóng" — khớp logic | ✅ PASS |
| P004 | "Đã vậy... Trái lại... chỗ nhắm... ngự trị" — khớp | ✅ PASS |
| P005 | Đề mục: "Từ Sử Học Cổ Truyền đến Sử Học Hiện Đại" — khớp | ✅ PASS |
| P006 | Toàn thư + Cương mục + chữ Hán cổ + chánh trị tốt/xấu — khớp | ✅ PASS |
| P007 | "Cho đến thế kỷ mười chín... với tay... chuyện khó" — khớp | ✅ PASS |
| P008 | "Dầu vậy... chinh phục... Nam Kỳ (Cochinchine)... phương Tây hóa" — khớp | ✅ PASS |
| P009 | "phả hệ chánh trị... dân tộc Annam... chủng raced... khái niệm phương Tây" — khớp | ✅ PASS |
| P010 | "Một người tên là Lê Lợi... đã chấm dứt..." (chủ động) ✅; "dẹp yên giặc Minh... cuộc chiến tranh giành độc lập... đầy ăm ắp... thế giới quan" — khớp | ✅ PASS |
| P011 | "nhà bác học" ✅; "*Annam* (Trung Kỳ) và *Tonkin* (Bắc Kỳ)" ✅; "xứ bảo hộ... trí thức cải cách Trung Hoa" — khớp | ✅ PASS |
| P012 | "*Annam* (Trung Kỳ) và *Tonkin* (Bắc Kỳ)" ✅; "hun đúc... ái quốc... 'yêu nước, thương nước'... Nguyễn Ái Quốc" — hoàn tất, khớp | ✅ PASS |
| [1]–[9] | Tên riêng, URL, số trang: khớp nguyên tác | ✅ PASS |

**Kết quả Vòng 1: PASS** — Không có lỗi nghĩa. Tất cả 12 đoạn + 9 cước chú khớp nguyên tác.

## 4. Vòng kiểm tra 2 — Đọc bản tiếng Việt độc lập

Đọc `v1_ch01_vi.txt` không nhìn nguyên tác, kiểm tra:

| Tiêu chí | Kết quả |
|---|---|
| Đúng ngữ pháp tiếng Việt | ✅ 12/12 đoạn |
| Rõ ràng, không mơ hồ | ✅ 12/12 đoạn |
| Tự nhiên, không phải dịch máy | ✅ 12/12 đoạn |
| Hiểu đúng ý tác giả ngay lần đọc đầu | ✅ 12/12 đoạn |
| Văn phong Nam Bộ nhất quán | ✅ *dầu, dẫu, tuy vậy, đã vậy, e rằng, soi bóng, đầy ăm ắp, với tay, chỗ nhắm, chấp bút* |
| Không pha trộn miền Bắc | ✅ Không có *đồng chí, ta/địch, giải phóng* |
| Không hiện đại hóa | ✅ Không có *chính phủ, đại biểu, tài chính* |
| Thuật ngữ có nguồn | ✅ *chánh trị, độc lập, thuộc địa, triều đình, quan lại, sĩ phu, bảo hộ, dân tộc, chủng raced, Nam Kỳ, Trung Kỳ, Bắc Kỳ, mặt trận* — tất cả VERIFIED |

**Kết quả Vòng 2: PASS** — Bản dịch đọc độc lập, hiểu đúng ý tác giả, văn phong Nam Bộ nhất quán.

## 5. Kết luận

| Hạng mục | Trạng thái |
|---|---|
| 6 lỗi đã sửa | ✅ 6/6 |
| P008–P012 khôi phục | ✅ 12/12 đoạn trong src |
| Vòng 1 (đối chiếu nguyên tác) | ✅ PASS |
| Vòng 2 (đọc độc lập) | ✅ PASS |
| Encoding | ✅ PASS (cả 2 tệp) |

**PILOT_V1_CH1: PASS (Giai đoạn 3)**

Chờ Giai đoạn 4 (nghiệm thu cuối) để quyết định 77_CHAPTER_TRANSLATION.

---

*Hết báo cáo Giai đoạn 3.*