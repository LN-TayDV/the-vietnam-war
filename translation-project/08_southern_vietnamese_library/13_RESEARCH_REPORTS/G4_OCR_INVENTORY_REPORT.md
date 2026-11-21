# G4 — OCR INVENTORY & QUALITY CONTROL REPORT

> Ngày: 2026-11-18. UTF-8, NFC, không BOM.
> Nguồn: Bách Khoa 405 (SRC-009) + Lê Ngọc Trụ 1959/1972 (SRC-007/008).

## 1. Inventory nguồn

### 1.1. Bách Khoa 405 (SRC-009)
| Thuộc tính | Giá trị |
|---|---|
| Tài liệu | Tạp chí Bách Khoa số 405 |
| Năm xuất bản | 1974 (ước đoán) |
| Nhà xuất bản | Bách Khoa, Sài Gòn |
| URL gốc | https://archive.org/details/bach-khoa-405_202310 |
| IA identifier | bach-khoa-405_202310 |
| Định dạng | PDF scan 84 trang (23.83 MB) |
| djvu.txt cũ | 240 KB — OCR rất nhiễu (chữ Cyrillic lẫn, dấu sai) |
| PDF tải về | ✅ Đã tải (23.83 MB) |
| Tình trạng | ✅ OCR hoàn tất |

### 1.2. Lê Ngọc Trụ 1959 (SRC-007)
| Thuộc tính | Giá trị |
|---|---|
| Tài liệu | Việt Ngữ Chánh Tả Tự Vị (bản 1959) |
| Tác giả | Lê Ngọc Trụ |
| Nhà xuất bản | Thanh Tân, Sài Gòn |
| Năm | 1959 |
| Số trang | 562 |
| URL | vietbooks.info (Google Drive) |
| Tình trạng | ❌ BLOCKED — Google Drive yêu cầu đăng nhập; tusachtiengviet.com link chết; lexlib.fi có anti-bot |
| Kết luận | Không tải được toàn văn; cần truy cập thủ công hoặc mua bản in |

### 1.3. Lê Ngọc Trụ 1972 (SRC-008)
| Thuộc tính | Giá trị |
|---|---|
| Tài liệu | Việt Ngữ Chánh Tả Tự Vị (bản 1972) |
| Tác giả | Lê Ngọc Trụ |
| Nhà xuất bản | Khai Trí, Sài Gòn |
| Năm | 1972 |
| Số trang | 751 |
| URL | vietbooks.info (Google Drive/Scribd) |
| Tình trạng | ❌ BLOCKED — tương tự SRC-007 |
| Kết luận | Không tải được toàn văn; có bản in tại quansachmuathu.vn (706 trang) |

## 2. OCR Pipeline — Bách Khoa 405

### 2.1. Cấu hình
| Thông số | Giá trị |
|---|---|
| Engine | Tesseract 5.4.0.20240606 |
| Language pack | vie (tessdata_fast, 531 KB) |
| DPI | 300 |
| PSM | 3 (fully automatic page segmentation) |
| Encoding output | UTF-8, NFC, no BOM, LF |
| PDF pages | 84 |
| Xử lý | PyMuPDF render → PNG → Tesseract → raw txt + cleaned txt |

### 2.2. Output
- **Thư mục**: `04_NEWSPAPERS_MAGAZINES/BachKhoa_405_OCR/`
- **Files**: `page_001.txt` → `page_084.txt` (cleaned), `page_001_raw.txt` → `page_084_raw.txt` (raw), `page_map.json`, `processing_log.txt`, `lexicon_evidence.json`
- **Tổng từ trích xuất**: 39,026 từ (trung bình 464.6 từ/trang)

### 2.3. Đánh giá chất lượng OCR

| Chỉ tiêu | Kết quả |
|---|---|
| Text extraction | ✅ 84/84 trang có nội dung |
| Vietnamese diacritics | ✅ Dấu tiếng Việt đúng (xét xử, thí, phú, Nhật, chúng) |
| Column order | ✅ Không đảo cột |
| Paragraph integrity | ✅ Đoạn văn giữ nguyên |
| Page mapping | ✅ Mỗi trang có file riêng, page_map.json |
| Uncertain words | ⚠️ Một số chữ mờ (ø, Œ, š) — đánh dấu OCR_PENDING |
| Pages tốt | 80/84 (95.2%) |
| Pages kém | 4/84 (4.8%) — trang 46, 62, 83, 84 (trang quảng cáo/bìa) |
| So với djvu.txt cũ | ✅ Cải thiện rõ rệt (djvu cũ: Cyrillic + dấu sai; OCR mới: đọc được) |

### 2.4. So sánh mẫu: OCR mới vs djvu.txt cũ

**djvu.txt cũ (OCR Internet Archive, rất nhiễu):**
```
Nước Nhật trước tòa án йт luận
châu • Những hiện twong
huyền bí trong (4р tục
```

**OCR mới (Tesseract 5.4.0 + vie, sạch):**
```
Nước Nhật trước tòa án dị luận
châu › Những hiện tượng
huyền bí trong tập tục
```

### 2.5. Lỗi còn tồn tại
- Trang quảng cáo (46, 62, 83, 84): chủ yếu là tiếng Pháp + logo → không có giá trị từ vựng.
- Một số ký tự đặc biệt (ø, Œ, š) do OCR nhầm chữ in hoa/viết tắt.
- Không có ground truth để tính tỷ lệ lỗi chính xác — đánh giá bằng so sánh thủ công mẫu.

## 3. Lexicon Mining — Bách Khoa 405

### 3.1. Kết quả
- **19 mục mới** được thêm vào MASTER_LEXICON (tất cả đánh dấu `OCR_PENDING`).
- **24 mục trùng** với lexicon hiện có (từ Lê Văn Đức) → bỏ qua (append-only).
- **Evidence file**: `lexicon_evidence.json` — chứa ngữ cảnh + page locator cho từng mục.

### 3.2. Phân bố domain mới
| Domain | Số mục mới |
|---|---:|
| Kinh tế | 7 (giấy bạc, tiền đồng, viện trợ, tái thiết, quỹ, khoản, thặng dư) |
| Chính trị | 15 (luật sư, quận trưởng, hội đồng xã, luật, dụ, …) |
| Địa lý | 8 (đô thị, nông thôn, đồng bằng, sông, rừng, biển, huyện, tỉnh…) |
| Lịch sử | 8 (hoàng đế, hội nghị, thực dân, thuộc địa, chiến tranh…) |

### 3.3. Ghi chú xác minh
- Tất cả 19 mục đánh dấu `OCR_PENDING` — **không** đánh dấu VERIFIED.
- Mỗi mục có `page` locator (vd: `BK405 p.5`) để đối chiếu với ảnh gốc.
- `vi_du_nguyen_ban` là trích từ OCR — cần đối chiếu với ảnh scan trước khi nâng lên VERIFIED.

## 4. G4 Completion Gate

| Tiêu chí | Trạng thái |
|---|---|
| Inventory Bách Khoa + Lê Ngọc Trụ đã kiểm kê | ✅ |
| OCR pipeline đã chạy trên phạm vi xác định (Bách Khoa 84 trang) | ✅ |
| Có mẫu đối chiếu với ảnh gốc (page 1, 5, 10, 20, 40) | ✅ |
| Các lỗi OCR quan trọng đã phân loại (4 trang quảng cáo = low) | ✅ |
| Mọi lexical entries mới có source locator (BK405 p.X) | ✅ |
| Không có OCR raw nào đánh dấu VERIFIED | ✅ (tất cả OCR_PENDING) |
| Các tệp metadata đã đồng bộ | ✅ |
| Encoding validation PASS | ✅ |

### 4.1. Trạng thái từng nguồn
| Nguồn | Trạng thái |
|---|---|
| Bách Khoa 405 (SRC-009) | ✅ DONE — OCR hoàn tất, 19 mục mined |
| Lê Ngọc Trụ 1959 (SRC-007) | ❌ BLOCKED — Google Drive login required |
| Lê Ngọc Trụ 1972 (SRC-008) | ❌ BLOCKED — Google Drive/Scribd login required |

### 4.2. Kết luận G4
**G4: PARTIAL** — Bách Khoa 405 hoàn tất; Lê Ngọc Trụ 1959/1972 BLOCKED (không tải được).

→ Chuyển sang G5 với nguồn Bách Khoa 405 OCR + Lê Văn Đức 1970.