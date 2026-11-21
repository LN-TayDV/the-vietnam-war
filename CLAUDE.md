# The Cambridge History of the Vietnam War — Project Instructions

> **Tự động nạp khi mở session mới** — Không cần nhắc lại quy trình, quy tắc, skill, glossary, công cụ.

---

## 1. KHỞI ĐỘNG TỰ ĐỘNG (AUTO-STARTUP)

Khi session mới bắt đầu, **bắt buộc** thực hiện theo thứ tự:

```python
# 1. Đọc project instructions (file này)
# 2. Đọc progress.json → xác định chương tiếp theo
# 3. Tự động nạp Rules bắt buộc (Rules/ directory hoặc Skills)
# 4. Tự động kích hoạt Skills theo loại nhiệm vụ
# 5. Tự động sử dụng Common Scripts cho kiểm tra
# 6. Chỉ đọc tài liệu chi tiết khi cần thiết
```

### 1.1 Xác định loại nhiệm vụ & Kích hoạt Skills

| Nhiệm vụ | Skills tự động kích hoạt | Rules bắt buộc |
|---|---|---|
| **Dịch chương mới** | `historical-book-translation`, `contextual-translation`, `southern-vietnamese-editorial-style`, `historical-terminology-research` | Accuracy, Grammar, Terminology, Contextual Research, File/Encoding |
| **Review bản dịch** | `deep-translation-review`, `translation-error-detection`, `translation-error-kb` | Review & Audit, Grammar, Terminology |
| **Audit toàn bộ** | `deep-translation-review`, `translation-error-detection`, `translation-quality-gate`, `translation-error-kb` | Tất cả Rules |
| **Quality Gate** | `translation-quality-gate`, `translation-error-detection` | Quality Gate 8 tiêu chí, Orthography, Encoding |
| **Nghiên cứu thuật ngữ** | `historical-terminology-research`, `contextual-translation` | Terminology, Contextual Research |

---

## 2. RULES BẮT BUỘC (TỰ ĐỘNG NẠP)

> **Không vi phạm được** — Chặn HOAN_TAT nếu lỗi.

### 2.1 Translation Accuracy Rules
- **Quy tắc 19**: CẤM KỊ dịch từng từ rồi ghép lại (Word-for-Word). Phải đọc toàn câu/đoạn/ngữ cảnh → tái cấu trúc.
- **Quy tắc 20**: Xử lý từ/câu khó — 5 bước bắt buộc (mở rộng ngữ cảnh → xác định ý đồ → tra cứu → đối chiếu → tái dựng).
- **Quy tắc 16**: Câu phải kết thúc bằng dấu chấm, đủ số câu như nguyên tác.
- **Quy tắc 27**: CẤM fabricate (bịa số trang, trích dẫn, ví dụ).

### 2.2 Vietnamese Grammar & Clarity Rules (VNCH Grammar Database)
- **Quy tắc 21**: Chỉ định danh từ Nam Bộ: *con/cái/cuốn/cây/cục/bài/người/ngài*.
- **Quy tắc 22**: Trạng từ không gian/thời gian: *nầy/đó/kia* (CẤM *này/đó/kia* chung).
- **Quy tắc 23**: Thể khía đầy đủ: *đã...rùi/hẵng, đang...xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa...mới/mới...xong, chưa...bao giờ/vẫn chưa*.
- **Quy tắc 24**: Đại từ nhân xưng trang trọng: *người ấy/ông ấy/bà ấy/họ* — CẤM *hắn/y/nó* chỉ người.
- **Quy tắc 25**: Từ nối logic Nam Bộ: *dầu/dẫu, trái lại, tuy vậy/đã vậy/song, bởi thế/do đó/cho nên, vả/lại/cũng*.
- **Quy tắc 26 (QUY TẮC VÀNG)**: Luôn ưu tiên chủ động hóa câu bị động tiếng Anh.

### 2.3 Historical & Political Terminology Rules
- **Quy tắc 1,3,4,12**: Thuật ngữ VNCH core: *chánh trị/chánh phủ/chánh đảng/đảo chánh/tài chánh/dân biểu/nghị sĩ/hưu bổng/địa ốc/ngân khố*.
- **Quy tắc 15**: Tên thuộc địa: *Annam→Trung Kỳ (Annam), Tonkin→Bắc Kỳ (Tonkin), Cochinchina→Nam Kỳ (Cochinchina), Indochine→Đông Dương (Indochine)* — giữ gốc trong ngoặc lần đầu; trích dẫn tiếng Anh/Pháp giữ nguyên.
- **Quy tắc 8, 15**: *giải phóng* → *độc lập/kháng cự* (thân bài); *đồng chí* → *đồng đạo* (thân bài); tên riêng giữ nguyên.

### 2.4 Contextual Research Rules
- **Quy tắc 20**: 5 bước bắt buộc khi gặp từ/câu khó.
- Tra cứu theo thứ tự: MASTER_LEXICON → VNCH Grammar Database → Nguồn VNCH sơ cấp → SOURCES.md → glossary_nam_bac_compare.tsv → Giữ nguyên + `[CẦN BỔ SUNG LEXICON]`.

### 2.5 Translation Review & Audit Rules
- **3 cấp kiểm soát**: S1-S20 (câu), P1-P10 (đoạn), C1-C10 (chương).
- **Error Taxonomy E01-E16**: Phân loại CRITICAL/MAJOR/MINOR.
- Review độc lập — **KHÔNG** tin audit cũ.

### 2.6 File & Encoding Rules
- **Quy tắc 28**: UTF-8, NFC, no BOM, LF. Python: `encoding="utf-8", newline="\n"`.
- **Quy tắc 18**: Alignment — `số đoạn src == số đoạn vi` (bắt buộc trước build DOCX).
- Mỗi thư mục chương chỉ 2 file: `v1_chXX_src.txt` + `v1_chXX_vi.txt`.

---

## 3. QUALITY GATE 8 TIÊU CHÍ (TỰ ĐỘNG CHẠY)

Trước khi đánh dấu `HOAN_TAT`, **bắt buộc** PASS hết 8 tiêu chí:

| # | Tiêu chí | Script kiểm tra |
|---|---|---|
| 1 | Encoding UTF-8, NFC, no BOM, LF | `encoding_checker.py` |
| 2 | Orthography: 0× "chính trị", 0× từ miền Bắc | `vnch_orthography.py` |
| 3 | Đồng bộ đoạn: src = vi | `document_comparator.py` |
| 4 | Đồng bộ cước chú: src = vi | `docx_builder.py` (build_chapter) → `OK N/N` |
| 5 | Không fabricate | Manual review |
| 6 | Văn phong tự nhiên (S1-S20, P1-P10) | `deep-translation-review` checklist |
| 7 | DOCX tồn tại 09_docx/, sinh bởi `docx_builder.py` | File exists |
| 8 | DOCX cước chú: `OK N/N`, Word `Footnotes.Count` = `notes`, footnote chân trang 9pt, 1..N | Word COM check |

**Chỉ cập nhật `progress.json` status="HOAN_TAT" khi TẤT CẢ PASS.**

---

## 4. COMMON SCRIPTS (THƯ VIỆN DÙNG CHUNG)

> **Vị trí:** `.kilo/scripts/common/` — **Một chức năng chỉ có một implementation.**

### 4.1 Danh sách Scripts

| Script | Chức năng | Skills sử dụng |
|---|---|---|
| `file_integrity.py` | Kiểm tra cấu trúc 2 file/chương, encoding, tên file | Tất cả |
| `translation_validator.py` | Quét từ Anh còn sót, thuật ngữ không nhất quán, nội dung rỗng | `translation-error-detection`, `translation-quality-gate` |
| `document_comparator.py` | Đối chiếu src vs vi: số đoạn, số câu, cấu trúc, alignment | `deep-translation-review`, `translation-error-detection` |
| `quality_gate.py` | Chạy 8 tiêu chí Quality Gate, output JSON | `translation-quality-gate` |
| `vnch_orthography.py` | Kiểm tra 30 quy tắc VNCH (từ `apply_vnch_fixes.py` logic) | `southern-vietnamese-editorial-style`, `translation-error-detection` |
| `encoding_checker.py` | Kiểm tra UTF-8, NFC, no BOM, LF | `translation-quality-gate`, `translation-error-detection` |
| `docx_builder.py` | Build DOCX chapter/volume với real Word footnotes, A4 layout | `historical-book-translation`, `translation-quality-gate` |

### 4.2 Nguyên tắc sử dụng
- Skills **phải gọi Common Scripts** thay vì tự triển khai logic.
- **Không sao chép** script vào thư mục chương.
- **Không viết lại** script đã có — chỉ mở rộng nếu cần.
- Output: JSON có cấu trúc, exit code 0=PASS, 1=FAIL.

### 4.3 Project Scripts (translation-project/99_scripts/)
*Specialized scripts không dùng chung, chỉ cho tác vụ đặc thù:*

| Script | Chức năng |
|---|---|
| `build_chapter_docx.py` | Legacy chapter DOCX builder (giữ để backward compat) |
| `build_volume_docx.py` | Legacy volume DOCX builder (giữ để backward compat) |
| `extract_chapters.py` | One-time PDF → text extraction (pymupdf) |
| `build_lexicon.py` | Lexicon management: `build`, `update`, `verify`, `stats` |
| `write_translation.py` | AI translation writer (79KB, specialized) |
| `build_corpus.py` | Corpus building for research |

*Đã xóa: 42 script cũ/debug/chapter-specific/tmp (xem consolidation report).*

---

## 5. WORKFLOW TỰ ĐỘNG THEO LOẠI NHIỆM VỤ

### 5.1 Dịch chương mới (`Dịch chương X`)

```
1. Đọc progress.json → xác định chương
2. Kích hoạt: historical-book-translation + contextual-translation + southern-vietnamese-editorial-style + historical-terminology-research
3. Đọc STYLE_GUIDE_PHAN_B.md + TRANSLATION_GRAMMAR_ENGINE.md + MASTER_LEXICON.csv + AUDIT_REPORT_CH01-06.md
4. Dịch theo 7 bước Grammar Engine + VNCH Grammar Database
5. Chạy file_integrity.py → translation_validator.py → document_comparator.py → vnch_orthography.py
6. Chạy quality_gate.py (8 tiêu chí)
7. Nếu PASS: docx_builder.py build_chapter → Word COM check → cập nhật progress.json HOAN_TAT
```

### 5.2 Review bản dịch (`Review chương X`)

```
1. Kích hoạt: deep-translation-review + translation-error-detection + translation-error-kb
2. Chạy document_comparator.py (alignment, sentence count)
3. Chạy translation_validator.py (từ Anh còn sót, thuật ngữ)
4. Chạy checklist S1-S20, P1-P10, C1-C10
5. Sửa trực tiếp v1_chXX_vi.txt
6. Chạy quality_gate.py
```

### 5.3 Audit toàn bộ (`Audit chương X`)

```
1. Kích hoạt: deep-translation-review + translation-error-detection + translation-quality-gate + translation-error-kb
2. Chạy full quality_gate.py
3. Đối chiếu từng câu S1-S20, đoạn P1-P10, chương C1-C10
4. Phát hiện lỗi E01-E16 qua translation-error-kb
5. Báo cáo chi tiết
```

### 5.4 Quản lý từ điển (`Lexicon`)

```
build_lexicon.py build     # Tạo mới từ seed data
build_lexicon.py update    # Thêm thuật ngữ từ audit/dịch
build_lexicon.py verify    # Kiểm tra trùng lặp, cột, encoding
build_lexicon.py stats     # Thống kê theo verification/domain/class
```

---

## 6. TÀI LIỆU CHUNG (SHARED ARTIFACTS)

| File | Vị trí | Dùng cho |
|---|---|---|
| `STYLE_GUIDE_PHAN_B.md` | `07_style_guide/` | 29 quy tắc VNCH (v2.3) |
| `TRANSLATION_GRAMMAR_ENGINE.md` | `07_style_guide/` | 7 bước + VNCH Grammar + Checklist S1-S20/P1-P10/C1-C10 |
| `MASTER_LEXICON.csv` | `08_southern_vietnamese_library/10_LEXICAL_DATABASE/` | 76+ mục từ điển Nam (VNCH verified) |
| `AUDIT_REPORT_CH01-06.md` | `05_qa/` | 222 lỗi đã fix, bài học 6 chương |
| `progress.json` | `00_plan/` | Checkpoint trạng thái |
| `manifest.json` | `00_plan/` | Metadata 77 chương |
| `build_lexicon.py` | `99_scripts/` | Lexicon management: build/update/verify/stats |

---

## 7. KIỂM TRA TỰ ĐỘNG KHI MỞ SESSION (HEALTH CHECK)

```bash
# 1. Kiểm tra rác workspace
Get-ChildItem C:\Users\PC\Documents\AI_project\the-vietnam-war -File -Include *.py,*.txt,*.docx,*.md `
  | Where-Object { $_.FullName -notmatch '\\.kilo\\|translation-project\\|\\.git\\' }

# 2. Kiểm tra progress.json
# 3. Kiểm tra Common Scripts tồn tại
# 4. Kiểm tra Skills load được
```

---

## 8. GHI NHỚ: BA LỚP KIẾN TRÚC

```
┌─────────────────────────────────────┐
│ Project Instructions (file này)     │ ← Điểm khởi động, auto-load
├─────────────────────────────────────┤
│ Rules (Bắt buộc, chặn HOAN_TAT)     │ ← Accuracy, Grammar, Terminology,
│                                     │     Review, File/Encoding, QG
├─────────────────────────────────────┤
│ Skills (Hướng dẫn suy nghĩ/thao tác) │ ← Dịch, Nghiên cứu, Review, Audit, QA
├─────────────────────────────────────┤
│ Common Scripts (Kiểm tra kỹ thuật)   │ ← File integrity, Validation,
│ .kilo/scripts/common/               │     Comparison, QA, Orthography
├─────────────────────────────────────┤
│ Quality Gates (Kiểm định)           │ ← 8 tiêu chí PASS → HOAN_TAT
└─────────────────────────────────────┘
```

**Skill hướng dẫn AI suy nghĩ; Script thực hiện kiểm tra lặp lại; Rules xác định điều tuyệt đối không vi phạm. Ba lớp phối hợp, không thay thế lẫn nhau.**

---

*File này được tự động nạp bởi Kilo khi mở project. Không cần đọc thủ công.*