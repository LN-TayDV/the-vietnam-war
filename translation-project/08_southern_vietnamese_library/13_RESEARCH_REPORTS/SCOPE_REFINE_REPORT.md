# SCOPE REFINEMENT — THƯ VIỆN NGÔN NGỮ KINH TẾ · CHÍNH TRỊ · ĐỊA LÝ · LỊCH SỬ MIỀN NAM

> Phiên bản 1.0. Ngày: 2026-11-18. Mã hoá UTF-8, NFC, không BOM.
> Tài liệu này ghi lại quyết định thu hẹp phạm vi, kết quả audit và cách phân loại.

## 1. Quyết định chiến lược

Dự án `08_southern_vietnamese_library/` **không còn** phát triển một hệ thống ngôn ngữ học tổng quát.

Phạm vi mới:

> **SOUTHERN VIETNAMESE ECONOMIC, POLITICAL, GEOGRAPHICAL & HISTORICAL LANGUAGE LIBRARY**
> (Thư viện ngôn ngữ Miền Nam về Kinh tế · Chính trị · Địa lý · Lịch sử)

### Mục đích phục vụ
1. Dịch thuật sách tiếng Anh sang tiếng Việt.
2. Nghiên cứu kinh tế và chính trị.
3. Nghiên cứu địa lý và lịch sử Việt Nam.
4. Viết luận, khảo cứu và biên soạn tài liệu.
5. Bảo tồn cách dùng từ và văn phong Miền Nam, đặc biệt trước 1975.

### Bốn lĩnh vực lõi (core domains)
| Mã | Domain | Phạm vi chính |
|---|---|---|
| `kinh_te` | ECONOMICS | Kinh tế học, tài chính–ngân hàng, tiền tệ–tài khóa, thuế–tài chính công, thương mại, nông nghiệp–công nghiệp, đầu tư–vốn, kinh tế quốc tế, địa lý kinh tế, lịch sử kinh tế |
| `chinh_tri` | POLITICS | Khoa học chính trị, nhà nước–chính quyền, luật hiến định–thể chế, lập/hành/tư pháp, hành chánh công vụ, đảng phái–phong trào, ngoại giao–quan hệ quốc tế, ý thức hệ, chính sách công, lịch sử chính trị |
| `dia_ly` | GEOGRAPHY | Địa lý tự nhiên, địa lý nhân văn, địa lý kinh tế, địa lý chính trị, địa lý hành chánh, địa danh–địa danh lịch sử, dân số–di cư, lãnh thổ–biên giới–chủ quyền, địa lý vùng Việt Nam |
| `lich_su` | HISTORY | Lịch sử Việt Nam, Đông Nam Á, thế giới (liên quan VN), lịch sử chính trị–thể chế, lịch sử kinh tế, lịch sử ngoại giao, lịch sử quân sự, lịch sử xã hội, sử liệu–thư tịch |

### Nhãn hỗ trợ (supporting)
- `ho_tro` — từ vựng phổ thông, chính tả, ngữ pháp, Hán-Việt học thuật chung, văn học.
- Các mục `ho_tro` **không thuộc phạm vi lõi trực tiếp** nhưng vẫn giữ vì chúng là **nền tảng chính tả/ngữ pháp/văn phong** cần cho việc dịch thuật và viết đúng chuẩn Miền Nam.

## 2. Nguyên tắc phân loại từ vựng (§3 đề bài)
Mỗi mục từ phân loại theo: `muc_loi_vuc` (core domain), `muc_phu` (subdomain), `thoi_ky_lich_su` (historical period), `phan_loai_khu_vuc` (regional usage), `van_phong` (register).

Phân biệt rõ 6 loại: (1) từ Việt Nam phổ thông, (2) từ Miền Nam, (3) từ Miền Nam lịch sử, (4) thuật ngữ VNCH, (5) thuật ngữ học thuật chuyên ngành, (6) từ lịch sử/lỗi thời.
→ **Không mặc định mọi từ trong tài liệu Miền Nam là từ riêng của Miền Nam.** Các mục phổ thông được đánh dấu `phan_loai_khu_vuc = chung`.

## 3. Kết quả audit hiện trạng (trước tinh chỉnh)

| Thành phần | Trước | Ghi chú |
|---|---|---|
| MASTER_LEXICON.csv | 50 mục (44 VERIFIED) | Chủ yếu từ Phan Khôi 1932 (văn học/phổ thông) |
| TERMINOLOGY_DATABASE.csv | 25 thuật ngữ | Quân sự, chính trị, ngoại giao, địa danh VNCH |
| ORTHOGRAPHY_DATABASE.csv | 20 quy tắc | Chính tả Nam Bộ |
| SOURCE_REGISTRY.csv | 22 nguồn | 4 tải toàn văn, 3 hạn chế, 4 print-only |
| Corpus | ~1.75M từ | Lê Văn Đức (OCR), Bách Khoa (OCR nhiễu), Phan Khôi (sạch) |

### Phát hiện quan trọng khi audit
1. **Lê Văn Đức 1970 (SRC-001/002) là nguồn từ điển Miền Nam THẬT, đọc được.** OCR chỉ nhiễu vừa phải ở chữ Hán/dấu; phần định nghĩa mục từ đọc được và **có thể trích dẫn trung thực**.
2. **Bách Khoa 405 (SRC-009) OCR quá nhiễu** ("đề nước", "thứ trị", "Tình thần") → **không dùng làm ví dụ đích thực** cho đến khi OCR lại.
3. **Bản djvu của Lê Văn Đức KHÔNG có dấu phân trang (form-feed)** → **không thể trích số trang chính xác**. Các mục từ Lê Văn Đức để `trang = ""` và ghi chú rõ "không có số trang trong bản djvu". Đây là giới hạn trung thực, không bịa số trang.
4. Nguồn sạch nhất: Phan Khôi 1932 (Wikisource, CC BY-SA) — nhưng là văn phê bình văn học, ít thuật ngữ 4 domain.

## 4. Hành động đã thực hiện (không xóa dữ liệu)
1. **Không xóa** bất kỳ mục cũ nào. Mọi bản ghi cũ được giữ nguyên + bổ sung cột phân loại.
2. Thêm 5 cột phân loại vào cả 3 CSDL: `muc_loi_vuc, muc_phu, thoi_ky_lich_su, phan_loai_khu_vuc, van_phong`.
3. Phân loại toàn bộ 95 mục cũ (50 lexicon + 25 terminology + 20 orthography).
4. **Bổ sung 69 mục từ domain đích thực** trích từ Lê Văn Đức 1970 (SRC-001/002), có định nghĩa + ví dụ + nguồn + trạng thái VERIFIED.
5. Kết quả: **MASTER_LEXICON 50 → 119 mục**; tổng 3 CSDL = **164 bản ghi**.

## 5. Phân bố domain sau tinh chỉnh
| Domain | MASTER_LEXICON | TERMINOLOGY | ORTHOGRAPHY | Tổng |
|---|---|---|---|---|
| kinh_te | 27 | 2 | 2 | 31 |
| lich_su | 17 | 11 | 2 | 30 |
| chinh_tri | 20 | 5 | 2 | 27 |
| dia_ly | 11 | 7 | 1 | 19 |
| ho_tro | 44 | 0 | 13 | 57 |
| **Tổng** | **119** | **25** | **20** | **164** |

## 6. Trạng thái xác minh (MASTER_LEXICON, 119 mục)
- VERIFIED: 113 · CROSS_VERIFIED: 2 · PARTIALLY_VERIFIED: 1 · UNVERIFIED: 3.
- 69 mục mới đều VERIFIED (định nghĩa + ví dụ có trong Lê Văn Đức 1970).

## 7. Giới hạn trung thực (chưa lấp)
- Số trang Lê Văn Đức: **không trích được** (djvu không có marker trang).
- Thuật ngữ 4 domain hiện ~107 mục lõi (trừ ho_tro) — **vẫn còn mỏng**, cần mở rộng tiếp theo từng domain.
- Chưa có văn kiện VNCH chuyên ngành (công báo, ngân hàng, luật) — xem KNOWLEDGE_GAP_REGISTER.

## 8. Bước tiếp theo
1. Mở rộng từ vựng theo từng domainưu tiên: kinh_te & chinh_tri (phục vụ dịch Cambridge ngay).
2. Tải Lê Ngọc Trụ 1959/1972 (chính tả) + nhiều số Bách Khoa.
3. OCR lại Bách Khoa bằng tesseract tiếng Việt → trích mục từ sạch.
4. Tra cứu Lê Văn Đức có đối chiếu trang (bản PDF) khi cần trích số trang.