# PHASE 0 — POST-G2 DATA RECONCILIATION REPORT

> Ngày: 2026-11-18. UTF-8, NFC, không BOM.
> Mục đích: Giải quyết chênh lệch thống kê trước khi chuyển sang G4/G5.

## 1. Giải quyết chênh lệch thống kê

### 1.1. Phát hiện

Báo cáo G2 trước đó có hai con số khác nhau:

| File | Con số |
|---|---:|
| `library_progress.json` | 264 master / 220 domain-core |
| `LIBRARY_CATALOG.md` | 264 master / 309 tổng |

Cả hai đều **đúng** nhưng đo các đối tượng khác nhau.

### 1.2. Định nghĩa chính xác (xác minh từ dữ liệu thực tế)

| Chỉ số | Giá trị | Định nghĩa | Nguồn |
|---|---:|---|---|
| **MASTER_LEXICON rows** | 264 | Số dòng dữ liệu trong `10_LEXICAL_DATABASE/MASTER_LEXICON.csv` (trừ header) | Đếm thực tế |
| **MASTER_LEXICON unique** | 263 | Số `tu_chuan` duy nhất (1 bản trùng `nấy` ×2) | `len(set(tu_chuan))` |
| **MASTER_LEXICON domain-core** | 220 | Số dòng ML có `muc_loi_vuc ≠ ho_tro` | Đếm thực tế |
| **TERMINOLOGY rows** | 25 | Số dòng `08_SPECIALIZED_TERMINOLOGY/TERMINOLOGY_DATABASE.csv` (trừ header) | Đếm thực tế |
| **ORTHOGRAPHY rows** | 20 | Số dòng `02_ORTHOGRAPHY/ORTHOGRAPHY_DATABASE.csv` (trừ header) | Đếm thực tế |
| **Tổng bản ghi (3 CSDL)** | 309 | 264 ML + 25 TERM + 20 ORTHO | Cộng thực tế |
| **Tổng domain-core (3 CSDL)** | 252 | ML 220 + TERM 25 + ORTHO 7 (trừ 13 ho_tro) | Cộng thực tế |

### 1.3. Phân bố domain tổng hợp (309 bản ghi)

| Domain | ML | TERM | ORTHO | Tổng |
|---|---:|---:|---:|---:|
| Kinh tế | 73 | 2 | 2 | 77 |
| Chính trị | 71 | 5 | 2 | 78 |
| Địa lý | 35 | 7 | 1 | 43 |
| Lịch sử | 41 | 11 | 2 | 54 |
| Hỗ trợ (ho_tro) | 44 | 0 | 13 | 57 |
| **Tổng** | **264** | **25** | **20** | **309** |

### 1.4. Kết luận reconciliation

- **Không có lỗi** — hai con số 220 và 309 đều đúng nhưng đo hai đối tượng khác nhau.
- `220` = domain-core **chỉ trong MASTER_LEXICON**.
- `309` = **tổng tất cả bản ghi** (ML + TERM + ORTHO).
- `252` = domain-core **tổng hợp 3 CSDL** (con số này chưa được báo cáo trước đây — cần bổ sung).
- Tất cả file metadata sẽ ghi rõ **định nghĩa** cho mỗi con số.

## 2. Duplicate audit — `nấy` (×2)

### 2.1. Chi tiết hai bản ghi

| Thuộc tính | Bản ghi 1 (Row 6) | Bản ghi 2 (Row 38) |
|---|---|---|
| tu_chuan | nấy | nấy |
| loai_tu | tinh_tu | tinh_tu |
| nghia | Ấy, đó (thay cho 'ấy' trong Nam Bộ) | Ấy (Nam Bộ) |
| vi_du_nguyen_ban | …càng phân chừng nào lại càng lộn xộn chừng nấy. | …càng lộn xộn chừng nấy. |
| nguon | SRC-021 | SRC-021 |
| ghi_chu | Dạng Nam Bộ của 'ấy' | Trùng với mục trên — gộp khi hoàn thiện |
| domain | ho_tro | ho_tro |

### 2.2. Đánh giá

- **Cùng nguồn**: SRC-021 (Phan Khôi 1932, Wikisource).
- **Cùng nghĩa**: cả hai đều định nghĩa `nấy` = dạng Nam Bộ của `ấy`.
- **Ví dụ**: khác nhau một chút (bản 1 đầy đủ hơn, bản 2 rút gọn) — nhưng cùng câu gốc.
- **Kết luận**: `POSSIBLE_DUPLICATE` — gần chắc chắn trùng lặp, nhưng theo nguyên tắc append-only, **không xóa** bản ghi nào.

### 2.3. Hành động

- Đánh dấu cả hai bản ghi với `POSSIBLE_DUPLICATE` trong metadata (không sửa dữ liệu cốt lõi).
- Giữ nguyên cả hai để bảo toàn lịch sử nguồn.
- Khi hoàn thiện lexicon, sẽ gộp thành một bản ghi duy nhất với `DUPLICATE_OF` đã xác minh.

## 3. Verification semantics — làm rõ

### 3.1. Định nghĩa chuẩn (áp dụng từ G4 trở đi)

| Trạng thái | Định nghĩa | Khác với VERIFIED |
|---|---|---|
| `VERIFIED` | Nội dung được kiểm chứng trực tiếp từ nguồn xác định (đọc được, không suy diễn) | — |
| `CROSS_VERIFIED` | Đối chiếu với nguồn độc lập thứ hai | Có 2 nguồn xác nhận |
| `PARTIALLY_VERIFIED` | Chỉ một phần nội dung được kiểm chứng (ví dụ: nghĩa đúng nhưng không có ví dụ gốc) | Một phần thiếu bằng chứng |
| `UNVERIFIED` | Chưa đủ bằng chứng để xác minh | Chưa xác minh |
| `OCR_PENDING` | Nguồn là OCR, chưa kiểm tra với ảnh gốc | Cần đối chiếu ảnh scan |
| `OCR_REVIEW_REQUIRED` | OCR có kết quả nhưng còn điểm nghi vấn (chữ mờ, trang bẩn) | Cần review thủ công |
| `DOMAIN_GAP` | Không tìm thấy bằng chứng trong nguồn đã tra | Thiếu nguồn |

### 3.2. Nguyên tắc mới (bắt buộc từ G4)

**VERIFIED chỉ xác minh nguồn, KHÔNG xác minh mức độ phổ biến.**

Mỗi trạng thái VERIFIED phải phân biệt 5 lớp xác minh:

1. **Xác minh nguồn** — nguồn tồn tại, đúng thư mục.
2. **Xác minh nội dung** — định nghĩa/cách dùng có trong nguồn.
3. **Xác minh ngữ cảnh** — cách dùng đúng ngữ cảnh (không phải nghĩa khác).
4. **Xác minh mức độ phổ biến** — KHÔNG tự động suy ra từ 1 nguồn. Phải có `popularity_scope` riêng.
5. **Xác minh sắc thái vùng miền/thời kỳ** — phải có `region_scope` và `period_scope` riêng.

→ Không dùng VERIFIED để khẳng định một từ được phổ biến rộng rãi trong toàn xã hội hoặc mọi thời kỳ.

### 3.3. Cột mới cần thêm (G5 trở đi)

Để phân biệt 5 lớp xác minh, lexicon cần thêm các cột:

- `popularity_scope`: `UNKNOWN` | `narrow` | `moderate` | `widespread`
- `region_scope`: `UNKNOWN` | `nam_bo` | `viet_nam_cong_hoa` | `toan_quoc`
- `period_scope`: `UNKNOWN` | `thoi_thuoc_dia` | `chien_tranh_viet_nam` | `viet_nam_cong_hoa` | `sau_1975`

**Không tự điền** các cột này khi chưa có bằng chứng. Mặc định = `UNKNOWN`.

## 4. Thay đổi metadata cần thực hiện

- [x] `library_progress.json`: thêm `combined_domain_core: 252`, định nghĩa rõ từng chỉ số.
- [x] `LIBRARY_CATALOG.md`: ghi rõ 264/309/252 là gì.
- [x] `LIBRARY_MASTER_PLAN.md`: cập nhật §4 nghiệm thu.
- [x] `DOMAIN_CLASSIFICATION.md`: cập nhật số tổng hợp 309, domain-core 252.
- [x] `KNOWLEDGE_GAP_REGISTER.md`: đồng bộ số liệu.
- [x] Tạo `PHASE0_RECONCILIATION_REPORT.md` (tệp này).

## 5. Kết quả Phase 0

**Trạng thái: PASS** — đã giải quyết chênh lệch thống kê, audit duplicate, làm rõ verification semantics.

Sẵn sàng chuyển sang G4.