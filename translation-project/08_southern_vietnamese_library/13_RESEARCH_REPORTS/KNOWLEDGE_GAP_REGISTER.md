# KNOWLEDGE GAP REGISTER — LĨNH VỰC CÒN THIẾU (THEO PHẠM VI MỚI)

> Phiên bản 2.0. Ngày: 2026-11-18. Mã hoá UTF-8, NFC, không BOM.
> Phạm vi: **Kinh tế · Chính trị · Địa lý · Lịch sử Miền Nam** (xem SCOPE_REFINE_REPORT.md).
> Nguyên tắc: ưu tiên chất lượng, chiều sâu, tính xác thực; KHÔNG thu thập nguồn chỉ để tăng số lượng.

## 0. Trạng thái hiện tại (sau tinh chỉnh — G2+G3 hoàn tất + Phase 0 reconciliation)
- 309 bản ghi / 3 CSDL; **252 bản ghi thuộc 4 domain lõi** (kinh_te 77, lich_su 54, chinh_tri 78, dia_ly 43, ho_tro 57).
- Trong đó MASTER_LEXICON: 264 rows (263 unique) / 220 domain-core.
- Mục domain mới từ Lê Văn Đức 1970: 145 mục (97 econ/politics + 48 geo/history, tất cả VERIFIED, có định nghĩa + ví dụ + nguồn).
- Đã hoàn tất G2 (Kinh tế + Chính trị) và G3 (Địa lý + Lịch sử) — giai đoạn hạt nhân đã mở rộng đáng kể.
- Duplicate: `nấy` ×2 (SRC-021) — POSSIBLE_DUPLICATE, giữ nguyên append-only.
- VERIFIED semantics: chỉ xác minh nguồn, KHÔNG xác minh mức độ phổ biến (xem PHASE0_RECONCILIATION_REPORT.md).

## 1. Từ điển chuyên ngành & chính tả (nền tảng)
| # | Thiếu | Mức độ | Hành động | Domain liên quan |
|---|---|---|---|---|
| 1 | Lê Ngọc Trụ, Việt Ngữ Chánh Tả Tự Vị 1959/1972 (toàn văn) | Cao | Tải từ Google Drive (SRC-007/008) | ho_tro (nền tảng) |
| 2 | Từ điển Việt–Anh/Pháp–Việt Sài Gòn (đối chiếu thuật ngữ) | Cao | Tìm IA/Google Books | kinh_te, chinh_tri |
| 3 | Lê Văn Đức bản PDF (để trích số trang) | Trung bình | Tải PDF SRC-001/003, map trang | 4 domain |
| 4 | Bảng chính tả hỏi/ngã Nam Bộ đầy đủ | Cao | Đối chiếu Lê Ngọc Trụ + corpus | ho_tro |

## 2. Kinh tế (Economics) — THUẬN TIỆN DỊCH CAMBRIDGE
| # | Thiếu | Mức độ | Hành động |
|---|---|---|---|
| 5 | Tài chính–ngân hàng VNCH (Ngân hàng Quốc gia, kho bạc) | Cao | Tìm báo cáo/dự luật VNCH |
| 6 | Kinh tế nông nghiệp (điền địa, canh nông, nông sản) | Cao | Khai thác Lê Văn Đức + Bách Khoa (sau OCR lại) |
| 7 | Thương mại–xuất nhập cảng, ngoại hối | Trung bình | Văn kiện Bộ Kinh tế VNCH |
| 8 | Kinh tế quốc tế, viện trợ, tái thiết | Trung bình | Tài liệu VNCH/CIA đã giải mật |

## 3. Chính trị (Politics)
| # | Thiếu | Mức độ | Hành động |
|---|---|---|---|
| 9 | Công báo VNCH (chính trị, hành chính, luật) | Cao | TT-TV / lưu trữ quốc gia |
| 10 | Văn kiện QLVNCH (quân sử) | Cao | Quân sử VNCH |
| 11 | Văn kiện ngoại giao VNCH (Ba Lê, Genève) | Trung bình | Hồi ký, Bộ Ngoại giao |
| 12 | Luật pháp VNCH (hiến pháp, luật hình, dân sự) | Trung bình | Công báo, tạp chí Luật |
| 13 | Đảng phái, phong trào chính trị Nam | Trung bình | Bách Khoa, báo chí Nam |

## 4. Địa lý (Geography)
| # | Thiếu | Mức độ | Hành động |
|---|---|---|---|
| 14 | Địa danh hành chánh VNCH (tỉnh/huyện/quận/xã ấp) | Cao | Bản đồ hành chánh VNCH |
| 15 | Địa lý vùng (Cao Nguyên Trung Phần, Đồng Bằng Sông Cửu Long) | Trung bình | Sử Địa, địa chí Nam |
| 16 | Biên giới–lãnh thổ–lãnh hải (Hoàng Sa, Trường Sa) | Trung bình | Văn kiện chủ quyền VNCH |

## 5. Lịch sử (History)
| # | Thiếu | Mức độ | Hành động |
|---|---|---|---|
| 17 | Tập san Sử Địa (29 số) — ngữ liệu sử học Nam | Cao | Tải từ Issuu (SRC-012) |
| 18 | Sử liệu VNCH (Quốc sử quán, sử gia Nam) | Trung bình | Sử Địa, sách sử Nam |
| 19 | Lịch sử quân sự VNCH | Cao | Quân sử (gối với #10) |
| 20 | Lịch sử kinh tế–xã hội Nam | Trung bình | Bách Khoa, khảo cứu Nam |

## 6. Ngữ liệu & công cụ
| # | Thiếu | Mức độ | Hành động |
|---|---|---|---|
| 21 | Bách Khoa (426 số) — mới có 1 số, OCR nhiễu | Cao | Tải thêm số + OCR lại (tesseract tiếng Việt) |
| 22 | Corpus văn xuôi Nam đa dạng (truyện, ký, luận) | Trung bình | Thu thập SRC-013–020 |
| 23 | Số trang chính xác cho mục từ Lê Văn Đức | Trung bình | Dùng bản PDF + đối chiếu |

## 7. Ngoài phạm vi — ĐÃ LOẠI (không còn ưu tiên)
Các hướng nghiên cứu ngôn ngữ học tổng quát sau **không còn** nằm trong phạm vi:
- ✗ Ngữ âm học/tự vị học đại cương không phục vụ 4 domain.
- ✗ Từ điển thành ngữ/tục ngữ Nam Bộ toàn tập (chỉ giữ phần liên quan văn phong).
- ✗ Nghiên cứu phương ngữ khẩu ngữ Nam Bộ mở rộng (ổng/ảnh, té/mắc…) — chỉ giữ ở mức `ho_tro` tối thiểu.
→ Các mục này vẫn được **đánh dấu `ho_tro`** và **không xóa**, nhưng **không mở rộng thêm**.

## 8. Ưu tiên điền vào (theo thứ tự, bám 4 domain)
1. **Kinh tế & Chính trị** (phục vụ dịch Cambridge ngay): #5, #9, #2.
2. **Chính tả nền tảng**: #1 (Lê Ngọc Trụ) — để chuẩn hóa chính tả mọi bản dịch.
3. **Địa lý hành chánh & Lịch sử quân sự**: #14, #10.
4. **Mở rộng từ vựng domain** từ Lê Văn Đức (đối chiếu trang bằng bản PDF #3) + Sử Địa #17.
5. **OCR lại Bách Khoa** → trích mục từ sạch (#21).

## 9. Lưu ý trung thực
- Thư viện **chưa lấp đầy** các DOMAIN_GAP trên. Đây vẫn là giai đoạn hạt nhân.
- Không tuyên bố "đủ dùng" khi các mục 1–23 còn mở.
- Mọi mục từ mới phải có nguồn, văn cảnh, và ghi rõ giới hạn (vd: thiếu số trang).