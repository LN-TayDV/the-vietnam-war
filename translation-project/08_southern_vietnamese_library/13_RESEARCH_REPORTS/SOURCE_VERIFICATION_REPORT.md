# SOURCE VERIFICATION REPORT — BÁO CÁO KIỂM CHỨNG NGUỒN

> Phiên bản 0.1. Ngày: 2026-11-18. Mã hoá UTF-8.

## 1. Phương pháp
Mỗi nguồn được kiểm: tên, tác giả, NXB, năm, nơi XB, URL, tình trạng truy cập, toàn văn?, tải PDF?, quyền SD, ghi chú. Kết quả ghi trong `SOURCE_REGISTRY.csv`.

## 2. Nguồn đã xác minh (VERIFIED) và tải được toàn văn

| ID | Tài liệu | URL | Tải | Toàn văn | Ghi chú |
|---|---|---|---|---|---|
| SRC-001 | Lê Văn Đức, VNTD Quyển Thượng A-L (1970) | archive.org/details/viet-nam-tu-dien-quyen-thuong-al-le-van-duc | ✅ 5.4MB | ✅ djvu.txt | OCR khá hơn, đọc được |
| SRC-002 | Lê Văn Đức, VNTD Quyển Hạ M-X (1970) | (cùng item) | ✅ 5.0MB | ✅ djvu.txt | |
| SRC-003 | Lê Văn Đức, VNTD bản gộp (1970) | archive.org/details/viet-nam-tu-dien-khai-tri-1970 | ✅ 8.1MB | ✅ djvu.txt | OCR nhiễu hơn |
| SRC-009 | Bách Khoa số 405 | archive.org/details/bach-khoa-405_202310 | ✅ 240KB | ✅ djvu.txt | OCR rất nhiễu (chữ Hán lẫn) |
| SRC-021 | Phan Khôi, "Tập VNTD của hội Khai trí" (1932) | vi.wikisource.org/... | — | ✅ văn bản sạch | CC BY-SA, văn xuôi Nam chuẩn |

## 3. Nguồn có toàn văn nhưng KHÔNG tải trực tiếp được
| ID | Tài liệu | Lý do | Cách truy cập |
|---|---|---|---|
| SRC-004 | Khai Trí 1931 (hanviet.org) | HTML dạng ảnh PNG | Đọc online; cần OCR nếu muốn |
| SRC-006 | Khai Trí 1931 (IA bwb_S0-ECZ-512) | 401 lending restricted | Mượn số hóa (in_copyright_lending) |
| SRC-005 | Khai Trí 1931 (Thư viện Nguyễn Văn Hướng) | Cần đăng ký | library_access |

## 4. Nguồn cần đăng ký / in
| ID | Tài liệu | Tình trạng |
|---|---|---|
| SRC-007/008 | Lê Ngọc Trụ, Chánh tả tự vị (1959/1972) | Google Drive link; cần tải thủ công |
| SRC-017–020 | Vương Hồng Sển, Huỳnh Công Tín, Nguyễn Văn Ái, Huỳnh Tịnh Của | print_only; chưa số hóa toàn văn |

## 5. Đánh giá chất lượng OCR (phát hiện quan trọng)
- **Lê Văn Đức (SRC-001/002)**: OCR đọc được ~70–80%, còn nhiễu (dấu sai, chữ Hán lẫn). Dùng làm **corpus tham khảo**, không dùng trực tiếp để trích mục từ sạch.
- **Bách Khoa (SRC-009)**: OCR **rất nhiễu** (ví dụ "йт luận", "twong", "ТАМ Пп bạc") — do chữ in cũ + chữ Hán. Cần OCR lại bằng công cụ tốt hơn (tesseract có cấu hình tiếng Việt) hoặc hiệu đính thủ công.
- **Phan Khôi (SRC-021)**: văn bản **sạch nhất** (Wikisource đã hiệu đính) — nguồn ngữ liệu Nam Bộ đáng tin cậy nhất hiện có.

## 6. Kết luận kiểm chứng
- 5 nguồn **VERIFIED + tải được toàn văn** (3 từ điển Lê Văn Đức + 1 Bách Khoa + 1 Phan Khôi).
- 3 nguồn **VERIFIED nhưng hạn chế truy cập** (Khai Trí 1931).
- Chất lượng OCR là **thách thức chính** → G4 cần OCR lại hoặc hiệu đính.
- **Không phát hiện nguồn giả** — mọi URL đều truy cập thực tế (trừ lending-restricted).

## 7. Việc tiếp theo
- Tải Lê Ngọc Trụ (SRC-007/008) từ Google Drive.
- OCR lại Bách Khoa bằng tesseract tiếng Việt (nếu cài được) hoặc tải thêm số khác.
- Tìm thêm ngữ liệu văn học/giáo dục Nam (SRC-013+).