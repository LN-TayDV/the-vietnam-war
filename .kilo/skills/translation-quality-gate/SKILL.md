---
name: translation-quality-gate
description: Quality Gate 8 tiêu chí bắt buộc PASS mới được đánh dấu chương HOAN_TAT. Kiểm tra: Encoding, Orthography, Đồng bộ đoạn/cước chú, Không fabricate, Văn phong, DOCX tồn tại, DOCX cước chú, DOCX bố cục. Tích hợp với docx_builder.py (Common), Word COM check, progress.json.
---

# Skill: Translation Quality Gate — Cổng Chất Lượng Xuất Bản

## 1. MỤC ĐÍCH
Đảm bảo **mọi chương** đạt chuẩn xuất bản trước khi đánh dấu `HOAN_TAT`. **8 tiêu chí CẤT BUỘC PASS** — thiếu 1 là KHÔNG được HOAN_TAT.

## 2. KHI NÀO KÍCH HOẠT
- **Bắt buộc** sau khi dịch xong, chạy Common scripts (`vnch_orthography.py`, `document_comparator.py`), trước khi build DOCX.
- Sau khi build DOCX (`docx_builder.py`).
- Khi audit chương hoàn tất (Deep Translation Review).
- Khi user yêu cầu verify chương đã hoàn tất.

## 3. 8 TIÊU CHÍ QUALITY GATE (Quy tắc 29, Grammar Engine)

| # | Tiêu chí | Mô tả | Cách kiểm tra | PASS khi |
|---|---|---|---|---|
| **1** | **Encoding** | UTF-8, NFC, no BOM, LF | `encoding_checker.py --chapter NN` | File đọc đúng tiếng Việt, không lỗi font |
| **2** | **Orthography** | 0× "chính trị", 0× từ miền Bắc không phù hợp | `vnch_orthography.py --chapter NN` | 0 occurrence từ sai CRITICAL/MAJOR; false positive trong trích dẫn được ghi nhận |
| **3** | **Đồng bộ đoạn** | Số đoạn src = số đoạn vi | `document_comparator.py --chapter NN` | src paragraphs = vi paragraphs; marker `[V1CNN-Pxxx]` khớp 1-1 |
| **4** | **Đồng bộ cước chú** | Số cước chú src = số cước chú vi | `docx_builder.py` build → `OK N/N`; Word COM `Footnotes.Count` = `notes` | Số lượng khớp, thứ tự 1..N đúng |
| **5** | **Không fabricate** | Không bịa số trang, trích dẫn, ví dụ | Đối chiếu số trang, trích dẫn với extracted text; check `[ND: ...]` | Tất cả thông tin truy xuất được về nguyên tác |
| **6** | **Văn phong tự nhiên** | Câu có ý nghĩa, không dịch máy từng từ | Checklist S1-S20, P1-P10; `translation_validator.py` | S7 PASS (hiểu ngay lần đầu), S9 PASS (không cấu trúc ngoại ngữ) |
| **7** | **DOCX tồn tại** | File `09_docx/V1-CNN_<slug>.docx` sinh bởi `docx_builder.py` | File exists; script log `OK ...` | File tồn tại, script báo OK |
| **8** | **DOCX cước chú & bố cục** | Footnote chân trang 9pt, đánh số 1..N; bố cục A4 chuẩn | Word COM: `Footnotes.Count` = `notes`; check footnote format; page layout | Footnotes.Count khớp; 9pt, hanging indent 0.4cm, liên tục 1..N; A4, lề 1.9/1.8/2.1/1.8cm |

## 4. QUY TRÌNH CHẠY QUALITY GATE (COMMON SCRIPTS)

### 4.1 Tự động (Common Scripts)
```bash
# 1. Kiểm tra encoding
python .kilo/scripts/common/encoding_checker.py --chapter NN
# Output: UTF-8 OK, NFC OK, no BOM, LF OK

# 2. Kiểm tra orthography (VNCH terminology)
python .kilo/scripts/common/vnch_orthography.py --chapter NN
# Output: 0 lỗi CRITICAL/MAJOR; false positive listed

# 3. Kiểm tra alignment (đoạn, câu, cước chú)
python .kilo/scripts/common/document_comparator.py --chapter NN
# Output: src_paragraphs = vi_paragraphs = XX; sentence_count match; footnotes aligned

# 4. Quality Gate tổng hợp
python .kilo/scripts/common/quality_gate.py --chapter NN
# Output: PASS/FAIL cho 8 tiêu chí, JSON structured

# 5. Build DOCX (Common docx_builder)
python -c "from docx_builder import DocxBuilder; from pathlib import Path; b=DocxBuilder(Path('.')); r=b.build_chapter(Path('translation-project/04_translation/v1/chNN/v1_chNN_vi.txt'), Path('translation-project/09_docx/V1-CNN_<slug>.docx')); print(r)"

# 6. Word COM verify (PowerShell)
$w = New-Object -ComObject Word.Application; $w.Visible=$false
$f = (Get-ChildItem "translation-project\09_docx" -Filter "V1-CNN_*.docx").FullName
$d = $w.Documents.Open($f,$false,$true)
"footnotes=" + $d.Footnotes.Count
"last-page=" + $d.Range($d.Content.End-1,$d.Content.End-1).Information(3)
$d.Close($false); $w.Quit()
# Output: footnotes=N (khớp progress.json); last-page=M (số trang thật)
```

### 4.2 Thủ công (Deep Review)
- Chạy checklist S1-S20, P1-P10, C1-C10 (Deep Translation Review).
- Đối chiếu từng câu S7 (hiểu ngay lần đầu).
- Đọc lại toàn chương liên mạch (C1, P9).

## 5. QUY TRÌNH XỬ LÝ KHI FAIL

| Tiêu chí FAIL | Hành động bắt buộc |
|---|---|
| **1. Encoding** | Fix file: Python `encoding="utf-8", newline="\n"`; không dùng PowerShell heredoc. Re-save file. |
| **2. Orthography** | Chạy `vnch_orthography.py` để xem chi tiết; fix thủ công lỗi còn lại; review false positive. |
| **3. Đồng bộ đoạn** | Chạy `document_comparator.py` xem chi tiết; nếu lệch → fix thủ công hoặc chạy realign logic. |
| **4. Đồng bộ cước chú** | Kiểm tra marker `[N]`/`N` trong vi.txt; khôi phục marker thiếu từ src; rebuild DOCX. |
| **5. Fabricate** | Xóa phần bịa; thêm `[ND: Người dịch bổ sung...]` nếu cần ngữ cảnh. |
| **6. Văn phong** | Chạy `translation_validator.py`; fix thủ công S9 (cấu trúc ngoại ngữ), S7 (khó hiểu); rewrite câu cứng. |
| **7. DOCX không tồn tại** | Chạy `docx_builder.py` build_chapter; fix lỗi input (thường do alignment hoặc cước chú). |
| **8. DOCX cước chú/bố cục** | Kiểm tra `docx_builder.py` logic (footnote, page layout); fix script nếu cần, rebuild toàn bộ. |

**QUAN TRỌNG**: Mọi fix phải chạy lại **TẤT CẢ 8 tiêu chí** từ đầu. Không được bỏ qua tiêu chí đã PASS trước đó.

## 6. CẬP NHẬT PROGRESS.JSON (SAU KHI PASS)

Chỉ cập nhật `progress.json` khi **TẤT CẢ 8 TIÊU CHÍ PASS**:

```json
{
  "chapter_status": {
    "V1-CNN": {
      "title_en": "...",
      "author": "...",
      "status": "HOAN_TAT",
      "pages": "XX-YY",
      "paragraphs": NN,
      "footnotes": MM,
      "docx": "09_docx/V1-CNN_<slug>.docx",
      "docx_status": "DONE (bố cục sách A4; footnote chân trang 9pt; N/N cước chú)"
    }
  }
}
```

**KHÔNG** cập nhật `status: "HOAN_TAT"` nếu chưa PASS hết 8 tiêu chí.

## 7. KẾT QUẢ MONG ĐỢI (Từ Audit 6 Chương Đầu)

| Chương | Encoding | Ortho | Đoạn | Cước chú | Fabricate | Văn phong | DOCX tồn tại | DOCX cước chú | KẾT QUẢ |
|---|---|---|---|---|---|---|---|---|---|
| Ch1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **HOAN_TAT** |
| Ch2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **HOAN_TAT** |
| Ch3 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **HOAN_TAT** |
| Ch4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **HOAN_TAT** |
| Ch5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **HOAN_TAT** |
| Ch6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **HOAN_TAT** |

## 8. LIÊN KẾT SKILLS
- **historical-book-translation**: Bước 8 (Xuất DOCX) + Quality Gate.
- **deep-translation-review**: Cung cấp checklist S1-S20, P1-P10, C1-C10.
- **translation-error-detection**: Phát hiện lỗi E01-E16 chặn Quality Gate.
- **southern-vietnamese-editorial-style**: Orthography check (Tiêu chí 2).
- **historical-terminology-research**: Thuật ngữ chuẩn cho Orthography.
- **translation-error-kb**: Tra cứu lỗi thực tế đã gặp.

## 9. COMMON SCRIPTS HỖ TRỢ
| Script | Chức năng | Quality Gate liên quan |
|---|---|---|
| `encoding_checker.py` | Check UTF-8, NFC, no BOM, LF | Tiêu chí 1 |
| `vnch_orthography.py` | Fix/check thuật ngữ VNCH (30 quy tắc) | Tiêu chí 2, 6 |
| `document_comparator.py` | So sánh src vs vi: đoạn, câu, cước chú | Tiêu chí 3, 4 |
| `translation_validator.py` | Quét tiếng Anh còn sót, term consistency | Tiêu chí 6 |
| `quality_gate.py` | Chạy 8 tiêu chí tổng hợp, output JSON | Tất cả 8 tiêu chí |
| `docx_builder.py` | Build DOCX chapter/volume, real Word footnotes | Tiêu chí 7, 8 |
| Word COM script | Verify `Footnotes.Count`, page count | Tiêu chí 4, 8 |

## 10. LIÊN KẾT SKILLS
- **historical-book-translation**: Bước 8 + Quality Gate final.
- **deep-translation-review**: Cung cấp checklist chi tiết cho tiêu chí 6.
- **translation-error-detection**: Phát hiện lỗi chặn Quality Gate (E01-E16).
- **southern-vietnamese-editorial-style**: Orthography check tự động.
- **translation-error-kb**: Tra cứu lỗi thực tế.

---

*Cập nhật: 2026-11-20 — Dựa trên Grammar Engine v2.1 §9 (Quality Gate 8 tiêu chí), Quy tắc 29, Audit 6 chương §4, Consolidated Common Scripts system.*