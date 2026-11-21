# BÀI HỌC TỪ V1-CH06 (Chương 6) — Cập nhật quy trình cho các session sau

**Ngày:** 2026-11-19  
**Chương:** V1-C06 "Sự Ra Đời Của Nước Việt Nam Dân Chủ Cộng Hòa" (David G. Marr)  
**Trạng thái:** HOAN_TAT (81 đoạn, 43 cước chú, DOCX xuất bản)

---

## 1. Vấn đề phát hiện & Sửa chữa trong quá trình review

### 1.1 Thuật ngữ tiếng Anh được tác giả cung cấp sẵn trong ngoặc — KHÔNG tự dịch

| Vị trí | Sai | Đúng | Nguyên tắc |
|--------|-----|------|------------|
| P045 | `"trinh sát" (secret investigation)` | `trinh sát` | Rule 9, 11: Tác giả ghi *secret investigation (trinh sát)* → dùng từ Việt do tác giả cung cấp |
| P058 | `"giặc mù quáng" (ignorance bandit)` | `"giặc dốt"` | Rule 9, 11: Tác giả ghi *ignorance bandit (giặc dốt)* → dùng từ Việt do tác giả cung cấp |

> **Quy tắc mới:** Khi nguyên tác tiếng Anh có cấu trúc `"English term (Vietnamese term)"`, **luôn dùng Vietnamese term do tác giả cung cấp**, không tự dịch lại. Chỉ giữ thuật ngữ tiếng Anh *in nghiêng + giải nghĩa* khi nguyên tác **không** cung cấp từ Việt.

### 1.2 Thuật ngữ Latin/Pháp không có tương đương Việt — BẮT BUỘC in nghiêng + giải nghĩa lần đầu

| Vị trí | Sai | Đúng | Nguyên tắc |
|--------|-----|------|------------|
| P070 | `modus vivendi` | `*modus vivendi* (thỏa thuận sống cùng nhau)` | Rule 9, 11 |
| P078 | `enclave` | `*enclave* (miền飞地)` | Rule 9, 11 |

> **Quy tắc mới:** Từ vựng ngoại ngữ (Latin, Pháp, Anh) xuất hiện **lần đầu** trong chương → `*nguyên ngữ* (giải nghĩa Việt)`. Các lần sau dùng nguyên ngữ in nghiêng.

### 1.3 Từ nối miền Nam — Tuân thủ cứng Rule 2, 7

| Vị trí | Sai | Đúng |
|--------|-----|------|
| P066 (dòng 200) | `Dẫu vậy, tuy nhiên` | `Dẫu vậy, tuy vậy` |

> **Nhắc lại:** `tuy nhiên` là từ miền Bắc. Miền Nam VNCH dùng `tuy vậy`, `dẫu`, `trái lại`, `vả`. Kiểm tra toàn bộ file bằng `grep "tuy nhiên"` trước khi build.

### 1.4 Tên thuộc địa — Đã đúng Rule 15

- `Tonkin (Bắc Kỳ)`, `Annam (Trung Kỳ)`, `Cochinchina (Nam Kỳ)` / `Nam Kỳ (Cochinchina)` — **giữ nguyên + giải nghĩa trong ngoặc**, không thay thế đơn phương.

---

## 2. Quy trình kiểm tra đã áp dụng (chuẩn hóa cho session sau)

### 2.1 Checklist encoding (bước 6 Grammar Engine)
```powershell
# Kết quả V1-C06
UTF-8 no BOM ✓
NFC ✓
LF only (no CRLF) ✓
```

### 2.2 Checklist orthography (bước 4)
```powershell
# Kết quả V1-C06
0× "chính trị" (chỉ có "chánh trị" — 12 lần) ✓
0× "chính phủ" (chỉ có "chánh phủ" — 17 lần) ✓
0× "tài chính" (chỉ có "tài chánh" — 2 lần) ✓
0× "đại biểu" (chỉ có "dân biểu" — 3 lần) ✓
0× "ngân sách" (cơ quan) — dùng "ngân khố" ✓
0× "đảo chính" (chỉ có "đảo chánh" — 1 lần) ✓
0× "tuy nhiên" ✓ (đã sửa thành "tuy vậy")
```

### 2.3 Checklist đồng bộ src ↔ vi
| Chỉ số | Nguồn | Bản dịch | Trạng thái |
|--------|-------|----------|------------|
| Đoạn | 81 | 81 | ✓ |
| Cước chú | 43 | 43 | ✓ |
| Thứ tự cước chú | 1–43 | 1–43 | ✓ |

### 2.4 Checklist DOCX build
```bash
python translation-project/99_scripts/build_chapter_docx.py 06
# Output: OK ... (43/43 cước chú, nguồn: inline)
```

**Word COM verification:**
- `Footnotes.Count = 43` ✓
- `last-page = 19` ✓
- Cước chú nằm chân trang, 9pt, đánh số 1..43 ✓

---

## 3. Các lỗi thường gặp CẦN TRÁNH (cập nhật từ V1-C06)

| Lỗi | Nguyên nhân | Cách phòng |
|-----|-------------|------------|
| Giữ nguyên `"English (Vietnamese)"` trong bản dịch | Copy nguyên khối từ nguồn mà không xử lý | **Luôn tách**: dùng từ Việt do tác giả cung cấp, bỏ nguyên ngữ Anh |
| Thiếu in nghiêng + giải nghĩa cho thuật ngữ Latin/Pháp lần đầu | Quên Rule 9, 11 | Tìm `grep -i "modus\|enclave\|status quo\|de facto\|de jure\|ad hoc\|etc\."` trước build |
| Dùng `tuy nhiên` thay `tuy vậy` | Thói quen từ miền Bắc | `grep "tuy nhiên"` bắt buộc; thay bằng `tuy vậy` / `dẫu` / `trái lại` |
| Encoding bị BOM hoặc CRLF | Dùng PowerShell heredoc ghi tiếng Việt | **Chỉ dùng Python** `encoding="utf-8", newline="\n"` để ghi file `.txt` |
| Số đoạn/cước chú không khớp progress.json | Không đếm lại sau sửa | Chạy script đếm **sau mỗi lần sửa** trước khi cập nhật progress.json |

---

## 4. Cập nhật quy trình cho session sau (bổ sung vào workflow)

### 4.1 Bước mới: "Bước 3.5 — Kiểm tra thuật ngữ ngoại ngữ & từ nối miền Nam"
**Thêm sau Bước 3 (Dịch), trước Bước 4 (Kiểm tra orthography):**

```bash
# 1. Thuật ngữ có ngoặc trong nguyên tác: "English (Vietnamese)"
grep -n '(secret investigation\|ignorance bandit\|...' v1_chXX_vi.txt
# → Phải dùng từ Việt trong ngoặc, bỏ tiếng Anh

# 2. Thuật ngữ Latin/Pháp lần đầu: modus vivendi, enclave, status quo, de facto, de jure, ad hoc, etc.
grep -in 'modus vivendi\|enclave\|status quo\|de facto\|de jure\|ad hoc\|a priori\|a posteriori\|vice versa\|per se\|ipso facto\|mutatis mutandis' v1_chXX_vi.txt
# → Phải có: *nguyên ngữ* (giải nghĩa Việt) lần đầu

# 3. Từ nối miền Bắc cấm
grep -n "tuy nhiên" v1_chXX_vi.txt
# → Phải 0 kết quả (thay bằng "tuy vậy", "dẫu", "trái lại")
```

### 4.2 Bước mới: "Bước 6.5 — Verify sau sửa chữa"
**Mỗi lần edit file vi.txt, CHẮC CHẮN chạy lại:**
```powershell
# Đếm lại đoạn
(Get-Content 'v1_chXX_vi.txt') -match '^--- \[V1CXX-P' | Measure-Object | Select-Object -ExpandProperty Count

# Đếm lại cước chú
(Get-Content 'v1_chXX_vi.txt') -match '^\[\d+\]' | Measure-Object | Select-Object -ExpandProperty Count

# Kiểm tra encoding
python -c "
import sys
b = open('v1_chXX_vi.txt','rb').read()
print('BOM:', b[:3]==b'\xef\xbb\xbf')
print('Has CR:', b'\r' in b)
print('Has LF:', b'\n' in b)
"
```

---

## 5. Template ghi chú cho chương mới (copy-paste)

> **File:** `05_qa/chXX_review.md` (tạo khi bắt đầu review chương XX)

```markdown
# Review V1-CXX — <Tên chương>

## 1. Thông tin cơ bản
- Đoạn src: ___  | Đoạn vi: ___
- Cước chú src: ___  | Cước chú vi: ___
- Trang: ___

## 2. Kiểm tra thuật ngữ (bước 3.5)
- [ ] "English (Vietnamese)" → dùng từ Việt
- [ ] Latin/Pháp lần đầu → *nguyên ngữ* (giải nghĩa)
- [ ] 0× "tuy nhiên"

## 3. Orthography (bước 4)
- [ ] 0× "chính trị"
- [ ] 0× "chính phủ"
- [ ] 0× "tài chính"
- [ ] 0× "đại biểu"
- [ ] 0× "ngân sách" (cơ quan) — dùng "ngân khố"
- [ ] 0× "đảo chính"

## 4. Encoding (bước 6)
- [ ] UTF-8 no BOM
- [ ] NFC
- [ ] LF only

## 5. Đồng bộ
- [ ] Số đoạn khớp
- [ ] Số cước chú khớp
- [ ] Thứ tự cước chú 1..N

## 6. DOCX build
- [ ] Script: OK N/N
- [ ] Word COM: Footnotes.Count = N
- [ ] Word COM: last-page = ___
- [ ] Cước chú chân trang 9pt

## 7. Vấn đề phát hiện & Sửa
| Vị trí | Vấn đề | Sửa |
|--------|--------|-----|
|        |        |     |

## 8. Cập nhật progress.json
- [ ] status: HOAN_TAT
- [ ] paragraphs: ___
- [ ] footnotes: ___
- [ ] pages: ___
- [ ] docx: 09_docx/V1-CXX_<slug>.docx
- [ ] docx_status: DONE (...)
```

---

## 6. Lưu ý quan trọng cho session sau

1. **Đọc `progress.json` TRƯỚC** để biết chương tiếp theo (V1-C07).
2. **Đọc `STYLE_GUIDE_PHAN_B.md` + `TRANSLATION_GRAMMAR_ENGINE.md`** trước khi dịch.
3. **Tạo `05_qa/chXX_review.md`** theo template mục 5 ngay khi bắt đầu review.
4. **Chạy checklist mục 2 (bước 3.5)** **trước** khi build DOCX — phát hiện sớm các lỗi thuật ngữ.
5. **Backup file HOAN_TAT** trước khi sửa (copy sang `99_scripts/backup/` kèm timestamp).
6. **Dọn dẹp workspace** theo mục 13.3 workflow trước khi kết thúc session.

---

## 7. Cập nhật progress.json (đã làm cho V1-C06)

```json
{
  "chapter_status": {
    "V1-C06": {
      "title_en": "The Birth of the Democratic Republic of Vietnam",
      "author": "David G. Marr",
      "status": "HOAN_TAT",
      "pages": "127-153",
      "paragraphs": 81,
      "footnotes": 43,
      "docx": "09_docx/V1-C06_Su-Ra-Doi-cua-nuoc-Viet-Nam-Dan-chu-Cong-hoa.docx",
      "docx_status": "DONE (bố cục sách A4; footnote chân trang 9pt; 43/43 cước chú; last-page=19)"
    }
  }
}
```

---

**Tóm tắt:** V1-C06 là chương đầu tiên áp dụng **đầy đủ 8 bước Grammar Engine + DOCX build + Quality Gate 8 mục**. 5 lỗi thuật ngữ/từ nối đã được sửa trong review. Các bài học đã được ghi nhận ở trên để các chương sau (V1-C07 trở đi) tránh lặp lại.