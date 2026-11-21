# LIBRARY MASTER PLAN — THƯ VIỆN NGÔN NGỮ KINH TẾ · CHÍNH TRỊ · ĐỊA LÝ · LỊCH SỬ MIỀN NAM (VNCH 1954–1975)

> Tài liệu điều phối tổng thể. Mã hoá UTF-8, NFC. Phiên bản 2.0 (2026-11-18).
> **Phạm vi đã thu hẹp (xem `13_RESEARCH_REPORTS/SCOPE_REFINE_REPORT.md`):** 4 lĩnh vực lõi — Kinh tế · Chính trị · Địa lý · Lịch sử Miền Nam. Không còn là hệ thống ngôn ngữ học tổng quát.

## 1. Mục tiêu
Xây dựng thư viện ngôn ngữ **Kinh tế · Chính trị · Địa lý · Lịch sử** tiếng Việt miền Nam (VNCH trước 1975) đủ tin cậy để:
1. Viết sách học thuật hàng trăm trang.
2. Dịch sử-chính-trị-kinh tế-địa lý từ Anh/Pháp sang Việt.
3. Viết văn xuôi, khảo cứu, nghị luận theo văn phong trí thức Nam.
4. Kiểm soát chính tả, từ vựng, ngữ pháp, văn phong xuyên suốt.
5. Tránh pha trộn văn phong Bắc.
6. Bảo tồn cách dùng từ và thuật ngữ chuyên ngành Miền Nam (đặc biệt trước 1975).

> Ưu tiên **chất lượng, chiều sâu, tính xác thực** hơn số lượng từ vựng/nguồn. Không thu thập nguồn chỉ để tăng số lượng.

## 2. Nguyên tắc
- **Không tự tạo trích dẫn/số trang/ví dụ giả.** Mỗi mục phải có nguồn thật.
- **Phân loại bằng chứng**: VERIFIED / CROSS_VERIFIED / PARTIALLY_VERIFIED / UNVERIFIED / DOMAIN_GAP.
- **Không thổi phồng**: không tuyên bố đủ dùng chỉ vì đạt số mục tùy ý.
- **UTF-8, NFC** toàn bộ.

## 3. Lộ trình theo batch (đã điều chỉnh theo 4 domain)

| GĐ | Nội dung | Trạng thái |
|---|---|---|
| G0 | Kiểm kê nguồn Internet, xác định nguồn toàn văn | ✅ HOÀN TẤT (22 nguồn) |
| G1 | Từ điển, chính tả, ngữ pháp (nền tảng `ho_tro`) | 🔄 ĐANG LÀM (3 từ điển tải, 20 quy tắc chính tả) |
| G2 | **Từ vựng domain KINH TẾ + CHÍNH TRỊ** (từ Lê Văn Đức + văn kiện VNCH) | ✅ HOÀN TẤT (97 mục econ/politics từ Lê Văn Đức; kinh_te 73, chinh_tri 71) |
| G3 | **Từ vựng domain ĐỊA LÝ + LỊCH SỬ** (từ Lê Văn Đức + Sử Địa) | ✅ HOÀN TẤT (48 mục geo/history từ Lê Văn Đức; dia_ly 35, lich_su 41) |
| G4 | Trích xuất, OCR lại, chuẩn hoá, lập chỉ mục (Bách Khoa nhiễu) | 🔄 (corpus ~1.75M từ; cần OCR lại) |
| G5 | Xây từ điển & CSDL ngữ liệu theo 4 domain | 🔄 (309 bản ghi / 220 domain lõi) |
| G6 | Phân tích cú pháp, cấu trúc câu, văn phong | 🔄 (GRAMMAR + SENTENCE_PATTERNS + WRITING_STYLE) |
| G7 | Bộ quy chuẩn viết sách | ⏳ (dựa trên G1–G6) |
| G8 | Thử nghiệm viết văn bản học thuật dài | ⏳ |

> **Điều chỉnh G2–G4 (theo scope mới):**
> - G2 = **Kinh tế + Chính trị** (phục vụ dịch Cambridge ngay) — không còn là "báo chí/văn học tổng quát".
> - G3 = **Địa lý + Lịch sử** (từ Lê Văn Đức + Sử Địa).
> - G4 = **OCR lại + chuẩn hoá corpus** — bắt buộc vì Bách Khoa nhiễu; Lê Văn Đức đọc được nhưng thiếu số trang.
> - Các hạng mục "báo chí/văn học tổng quát" cũ **chuyển sang `ho_tro`** và **không mở rộng thêm**.

## 4. Cấu trúc thư mục
```
08_southern_vietnamese_library/
├── 00_LIBRARY_MASTER_PLAN/   ← LIBRARY_CATALOG.md, MASTER_PLAN (này)
├── 01_DICTIONARIES/          ← 3 file OCR Lê Văn Đức
├── 02_ORTHOGRAPHY/           ← ORTHOGRAPHY_DATABASE.csv (20 quy tắc)
├── 03_GRAMMAR/               ← GRAMMAR_DATABASE.md
├── 04_NEWSPAPERS_MAGAZINES/  ← BachKhoa_405
├── 05_LITERATURE/            ← (đang thu thập)
├── 06_ACADEMIC_BOOKS/        ← (đang thu thập)
├── 07_GOVERNMENT_DOCUMENTS/  ← (đang thu thập)
├── 08_SPECIALIZED_TERMINOLOGY/ ← TERMINOLOGY_DATABASE.csv (25 mục)
├── 09_CORPUS_TEXT/           ← corpus đã chuẩn hoá
├── 10_LEXICAL_DATABASE/      ← MASTER_LEXICON.csv (264 mục, có phân loại domain)
├── 11_WRITING_STYLE/         ← SOUTHERN_WRITING_STYLE, SENTENCE_PATTERNS
├── 12_SOURCE_REGISTRY/       ← SOURCE_REGISTRY.csv (22 nguồn)
└── 13_RESEARCH_REPORTS/      ← SCOPE_REFINE_REPORT, DOMAIN_CLASSIFICATION, SOURCE_VERIFICATION_REPORT, KNOWLEDGE_GAP_REGISTER
```

## 5. Điều kiện nghiệm thu (theo nhiệm vụ)
Thư viện chỉ "hoàn thành giai đoạn xây dựng ban đầu" khi:
1. ✅ Có nguồn từ điển & chính tả đáng tin cậy (Lê Văn Đức 1970 — đọc được; Lê Ngọc Trụ — cần tải).
2. 🔄 Có ngữ liệu thực tế từ tài liệu Nam (Lê Văn Đức, Phan Khôi — một phần; Bách Khoa cần OCR lại).
3. ✅ Có dữ liệu từ vựng domain xác minh (**252 bản ghi domain lõi** tổng 3 CSDL / 309 tổng — đã hoàn tất G2+G3; ML: 220/264).
4. ✅ Có hệ thống ngữ pháp & cách hành văn (GRAMMAR + WRITING_STYLE).
5. 🔄 Có thuật ngữ chuyên ngành 4 domain (kinh_te 73, lich_su 41, chinh_tri 71, dia_ly 35 — cần mở rộng thêm từ VNCH documents).
6. ✅ Có khả năng tra cứu & truy xuất dẫn chứng (SOURCE_REGISTRY + MASTER_LEXICON + DOMAIN_CLASSIFICATION).
7. ✅ Có quy chuẩn biên tập thống nhất (STYLE_GUIDE + ORTHOGRAPHY + WRITING_STYLE).
8. ⏳ Có thử nghiệm viết văn bản học thuật dài (G8 — chưa làm).

→ **Chưa đạt nghiệm thu cuối.** Đã hoàn tất G2 (Kinh tế + Chính trị) và G3 (Địa lý + Lịch sử); đang ở G4–G5.

## 6. Báo cáo tiến độ
Xem `13_RESEARCH_REPORTS/SCOPE_REFINE_REPORT.md`, `DOMAIN_CLASSIFICATION.md`, `SOURCE_VERIFICATION_REPORT.md` và `KNOWLEDGE_GAP_REGISTER.md`.