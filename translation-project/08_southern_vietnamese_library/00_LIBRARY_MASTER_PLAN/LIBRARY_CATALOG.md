# LIBRARY_CATALOG — THƯ VIỆN NGÔN NGỮ KINH TẾ · CHÍNH TRỊ · ĐỊA LÝ · LỊCH SỬ MIỀN NAM

> Phiên bản: 2.0 (G0–G3 hoàn tất, phạm vi 4 domain). Mã hoá UTF-8, NFC. Ngày: 2026-11-18.

## 1. Tổng quan
Thư viện xây dựng theo **4 lĩnh vực lõi — Kinh tế · Chính trị · Địa lý · Lịch sử** tiếng Việt miền Nam (VNCH trước 1975), dùng để:
- Biên soạn sách học thuật, dịch sử-chính-trị-kinh tế-địa lý.
- Kiểm soát chính tả, từ vựng, ngữ pháp, văn phong.
- Tránh pha trộn văn phong miền Bắc.
- Bảo tồn thuật ngữ chuyên ngành và văn phong Miền Nam.

> Phạm vi chi tiết: xem `13_RESEARCH_REPORTS/SCOPE_REFINE_REPORT.md`.

## 2. Các thành phần hiện có

### 2.1 Từ điển (01_DICTIONARIES/)
| File | Nguồn | Dung lượng | Trạng thái |
|---|---|---|---|
| LeVanDuc_VNTD_1970_djvu.txt | Lê Văn Đức 1970 (IA) | 8.1 MB | ✅ tải, OCR nhiễu |
| LeVanDuc_QuyenThuong_AL_djvu.txt | Lê Văn Đức 1970 Quyển Thượng A-L (IA) | 5.4 MB | ✅ tải, OCR khá hơn |
| LeVanDuc_QuyenHa_MX_djvu.txt | Lê Văn Đức 1970 Quyển Hạ M-X (IA) | 5.0 MB | ✅ tải |
| HoaiTri_1931_VNTD_djvu.txt | Khai Trí 1931 (IA) | — | ⚠️ 401 (lending restricted) |

### 2.2 Chính tả (02_ORTHOGRAPHY/)
| File | Nội dung |
|---|---|
| ORTHOGRAPHY_DATABASE.csv | 20 quy tắc chính tả Nam Bộ (hỏi/ngã, nầy, chớ, gởi, thơ, nhứt, chừng nấy, vả, chánh phủ, phi cơ…) |

### 2.3 Ngữ pháp (03_GRAMMAR/)
| File | Nội dung |
|---|---|
| GRAMMAR_DATABASE.md | Cấu trúc "càng…chừng nào…chừng nấy", "chớ", "vả", "làm gì", "cầm…là", xưng hô, liên từ, Hán-Việt |

### 2.4 Báo chí / tạp chí (04_NEWSPAPERS_MAGAZINES/)
| File | Nguồn | Dung lượng | Trạng thái |
|---|---|---|---|
| BachKhoa_405_djvu.txt | Bách Khoa số 405 (IA) | 240 KB | ✅ tải, OCR rất nhiễu |
| (mục lục 426 số) | namkyluctinh.org | — | 📋 đã lập danh mục |

### 2.5 Ngữ liệu (09_CORPUS_TEXT/)
| File | Dung lượng (từ) | Nguồn |
|---|---|---|
| LeVanDuc_QuyenThuong_AL.txt | ~891k | SRC-001 |
| LeVanDuc_QuyenHa_MX.txt | ~817k | SRC-002 |
| BachKhoa_405.txt | ~38k | SRC-009 |
| sample_PhanKhoi_1932.txt | ~500 (20 mẫu) | SRC-021 (Wikisource, sạch) |

### 2.6 Cơ sở dữ liệu từ vựng (10_LEXICAL_DATABASE/)
| File | Số mục | Xác minh |
|---|---|---|
| MASTER_LEXICON.csv | 264 (119 cũ + 145 mới từ Lê Văn Đức G2+G3) | 258 VERIFIED, 2 CROSS, 1 PARTIAL, 3 UNVERIFIED |

### 2.7 Thuật ngữ chuyên ngành (08_SPECIALIZED_TERMINOLOGY/)
| File | Số mục |
|---|---|
| TERMINOLOGY_DATABASE.csv | 25 thuật ngữ VNCH (MTGPMN, QLVNCH, Ba Lê, Tổng Công Kích Mậu Thân, Cao Nguyên Trung Phần…) — đã phân loại 4 domain |

### 2.8 Văn phong (11_WRITING_STYLE/)
| File | Nội dung |
|---|---|
| SOUTHERN_WRITING_STYLE.md | 9 mục: nguyên tắc, từ vựng, cú pháp, giọng, dịch thuật, khảo cứu, nghị luận, điều KHÔNG làm, bảng kiểm |
| SENTENCE_PATTERNS.md | Mẫu câu mở/kết/chuyển đoạn/diễn đạt + ví dụ thật |

### 2.9 Nguồn & báo cáo (12_SOURCE_REGISTRY/, 13_RESEARCH_REPORTS/)
| File | Nội dung |
|---|---|
| SOURCE_REGISTRY.csv | 22 nguồn (từ điển, chính tả, báo, khảo cứu, ngôn ngữ học) + trạng thái truy cập |
| corpus_extraction_report.json | Thống kê corpus đã trích xuất |
| SOURCE_VERIFICATION_REPORT.md | Báo cáo kiểm chứng nguồn |
| SCOPE_REFINE_REPORT.md | Quyết định thu hẹp phạm vi + audit + phân loại |
| DOMAIN_CLASSIFICATION.md | Phân loại 264 bản ghi theo 4 domain |
| KNOWLEDGE_GAP_REGISTER.md | Lĩnh vực còn thiếu (theo 4 domain) |

## 3. Thống kê bao phủ hiện tại (sau tinh chỉnh + Phase 0 reconciliation)

### 3.1. Định nghĩa các chỉ số (Phase 0 làm rõ)
- **MASTER_LEXICON rows = 264**: số dòng dữ liệu trong `MASTER_LEXICON.csv` (trừ header).
- **MASTER_LEXICON unique = 263**: số `tu_chuan` duy nhất (1 bản trùng `nấy` ×2 — POSSIBLE_DUPLICATE).
- **MASTER domain-core = 220**: số dòng ML có `muc_loi_vuc ≠ ho_tro`.
- **Tổng bản ghi 3 CSDL = 309**: 264 ML + 25 TERMINOLOGY + 20 ORTHOGRAPHY.
- **Tổng domain-core 3 CSDL = 252**: ML 220 + TERM 25 + ORTHO 7 (trừ 13 ho_tro trong ORTHO).

### 3.2. Thống kê
- **Nguồn đã xác minh**: 22 (4 tải toàn văn, 3 consult online, 4 print-only).
- **Corpus**: ~1.75 triệu từ (Lê Văn Đức OCR đọc được; Bách Khoa OCR nhiễu).
- **Bản ghi từ vựng**: 309 tổng (264 MASTER_LEXICON + 25 TERMINOLOGY + 20 ORTHOGRAPHY).
- **Phân bố 4 domain (MASTER)**: kinh_te 73, chinh_tri 71, lich_su 41, dia_ly 35, ho_tro 44 → **220 domain lõi**.
- **Phân bố 4 domain (kết hợp 3 CSDL)**: kinh_te 77, chinh_tri 78, lich_su 54, dia_ly 43, ho_tro 57 → **252 domain lõi**.
- **Mục domain mới từ Lê Văn Đức 1970**: 145 mục (97 econ/politics + 48 geo/history, tất cả VERIFIED).

## 4. Đánh giá trung thực (không thổi phồng)
- Đã hoàn tất **G0–G3** + Phase 0 reconciliation. 252 bản ghi domain lõi (kết hợp 3 CSDL) là **cơ sở hạt nhân**, chưa phải "hàng nghìn mục".
- **Lê Văn Đức 1970 đọc được** (OCR nhiễu vừa), nhưng bản djvu **không có số trang** → mục từ Lê Văn Đức để `trang=""`, không bịa số trang.
- **Bách Khoa 405 OCR quá nhiễu** → chưa dùng làm ví dụ đích thực; cần OCR lại.
- Ngữ liệu sạch nhất: **Phan Khôi 1932 (Wikisource)** — nhưng là văn phê bình văn học, ít thuật ngữ 4 domain.
- **DOMAIN_GAP**: còn thiếu văn kiện VNCH chuyên ngành (kinh tế, chính trị, địa lý, lịch sử) và ngữ liệu sử học (Sử Địa).
- **VERIFIED semantics**: VERIFIED chỉ xác minh nguồn, KHÔNG xác minh mức độ phổ biến. Phải phân biệt 5 lớp (xem `PHASE0_RECONCILIATION_REPORT.md`).
- **Duplicate**: `nấy` ×2 (SRC-021) đánh dấu POSSIBLE_DUPLICATE, giữ nguyên theo append-only.

## 5. Bước tiếp theo (G4–G5, theo scope mới)
1. OCR lại Bách Khoa bằng tesseract tiếng Việt → trích mục từ sạch.
2. Tải Lê Ngọc Trụ 1959/1972 (chính tả) + nhiều số Bách Khoa.
3. Mở rộng MASTER_LEXICON bằng văn kiện VNCH chuyên ngành (kinh tế, chính trị, địa lý, lịch sử).
4. Đối chiếu bản PDF Lê Văn Đức để bổ sung số trang khi cần.
5. Trình bày quy chuẩn ngôn ngữ (STYLE_GUIDE Phần B) + pilot V1-Ch1 để người dùng duyệt.