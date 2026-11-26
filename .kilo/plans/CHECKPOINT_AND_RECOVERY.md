# CHECKPOINT_AND_RECOVERY.md — CƠ CHẺ CHECKPOINT VÀ PHỤC HỒI

**Dự án:** The Origins of Totalitarianism — Hannah Arendt (VNCH rebuild)  
**File:** `.kilo/plans/CHECKPOINT_AND_RECOVERY.md`  
**Phiên bản:** 1.0

---

## 1. CHECKPOINT SYSTEM

Mỗi checkpoint được lưu sau khi hoàn thành một giai đoạn cho một chapter. Checkpoint ghi vào `00_plan/progress.json` và (tùy chọn) file checkpoint riêng.

### 1.1 Checkpoint Levels

| Level | Mô tả | Lưu vào |
|-------|-------|---------|
| CP-0 | Chưa bắt đầu | `progress.json` status = "not_started" |
| CP-1 | Source TXT đã trích xuất | `progress.json` + file checkpoint |
| CP-2 | Translation TXT đã dịch xong | `progress.json` + file checkpoint |
| CP-3 | Hiệu đính đã hoàn tất | `progress.json` + file checkpoint |
| CP-4 | Đối chiếu đã hoàn tất (alignment PASS) | `progress.json` + file checkpoint |
| CP-5 | DOCX đã build | `progress.json` + file checkpoint |
| CP-6 | QA đã pass tất cả 10 mục | `progress.json` status = "HOAN_TAT" |

### 1.2 Checkpoint File Format

File checkpoint được lưu tại `00_plan/checkpoints/{chapter}_cp{level}.json`:

```json
{
  "chapter": "ch05",
  "level": 3,
  "timestamp": "2026-11-26T14:30:00Z",
  "files": {
    "source_txt": "02_extracted_text/v2/ch05_src.txt",
    "translation_txt": "04_translation/v2/ch05/v1_ch05_vi.txt"
  },
  "counts": {
    "source_paragraphs": 37,
    "translation_paragraphs": 37,
    "footnotes": 60
  },
  "qa_results": {
    "Q1": "PASS",
    "Q2": "PASS",
    "Q3": "PASS",
    "Q4": "PASS",
    "Q5": "PASS",
    "Q6": "PASS",
    "Q7": "PASS",
    "Q8": "PASS",
    "Q9": "PASS",
    "Q10": "PASS"
  },
  "notes": "All 10 QA criteria PASS. Ready for DOCX build."
}
```

---

## 2. PROGRESS.JSON STRUCTURE

File `00_plan/progress.json` là source of truth cho trạng thái toàn bộ dự án.

### 2.1 Schema

```json
{
  "project": "The Origins of Totalitarianism - Hannah Arendt",
  "target": "Vietnamese (VNCH pre-1975 Southern standard)",
  "source_pdf": "books/Hannah-Arendt-The-Origins-of-Totalitarianism-Harcourt-Brace-Jovanovich-1973.pdf",
  "updated": "ISO 8601 timestamp",
  "dashboard": "dashboard.html status",
  "chapters": {
    "front_matter": { "pages": "1-7", "status": "HOAN_TAT|...", "checkpoint": 0-6 },
    "preface_first_edition": { ... },
    ...
    "ch01": { "pages": "48-55", "status": "...", "checkpoint": 0-6, "docx": "...", "docx_status": "..." },
    ...
    "ch13": { ... }
  },
  "qa_gate": "X/13 PASS",
  "phase_status": "GIAI ĐOẠN X/HOÀN TẤT"
}
```

### 2.2 Status Values

| Giá trị | Ý nghĩa |
|---------|---------|
| `not_started` | Chưa bắt đầu |
| `extracting` | Đang trích xuất PDF |
| `translating` | Đang dịch |
| `editing` | Đang hiệu đính |
| `qa_pending` | Chưa chạy QA |
| `qa_done` | QA đã chạy, đang sửa lỗi |
| `docx_built` | DOCX đã build |
| `HOAN_TAT` | Hoàn tất tất cả 10 mục QA + DOCX |

---

## 3. CÁCH TIẾP TUYẾN KHI GIẢN ĐOẠN

### 3.1 Phát hiện điểm dừng cuối cùng

```bash
# Kiểm tra progress.json để xem chapter cuối cùng đã HOAN_TAT
# Tìm chapter có status != HOAN_TAT, bắt đầu từ chapter đầu tiên
```

### 3.2 Các bước tiếp tục

1. **Đọc `00_plan/progress.json`** — xác định chapter cuối cùng đã HOAN_TAT
2. **Đọc checkpoint file** (nếu có) — xác định level checkpoint cuối cùng của chapter tiếp theo
3. **Tiếp tục từ level tiếp theo** — không bắt đầu lại từ đầu
4. **Không ghi đè file đã HOAN_TAT** — chỉ ghi đè file của chapter đang xử lý
5. **Cập nhật `progress.json`** sau mỗi checkpoint

### 3.3 Ví dụ: Gián đoạn tại ch05 level 3 (hiệu đính xong, chưa đối chiếu)

```
Trạng thái: ch05 status = "editing", checkpoint = 3
Hành động: Tiếp tục từ CP-4 (đối chiếu alignment)
           Chạy debug_align.py ch05
           Nếu PASS → cập nhật checkpoint = 4, status = "qa_pending"
           Tiếp tục CP-5 (build DOCX), CP-6 (QA, HOAN_TAT)
```

---

## 4. PHỤC HỒI TỪ LỖI

### 4.1 Lỗi trong quá trình dịch (Sai nghĩa, thiếu thông tin)

- Không xóa file translation đã viết
- Ghi lại lỗi vào Error Log (theo format tại QA_ACCEPTANCE_CRITERIA.md §3)
- Sửa lỗi tại paragraph tương ứng
- Cập nhật checkpoint nếu cần

### 4.2 Lỗi alignment (src ≠ vi paragraph count)

- Không gộp/tách đoạn tùy tiện
- Xác định nguyên nhân: đoạn bị ngắt trang không gộp, hoặc đoạn bị bỏ sót
- Sửa tại source TXT hoặc translation TXT tương ứng
- Chạy lại `debug_align.py` để xác nhận PASS

### 4.3 Lỗi DOCX (build thất bại, footnote mismatch)

- Xóa file DOCX lỗi (nếu có)
- Chạy lại `build_chapter_docx_v2.py chNN`
- Xác nhận `Footnotes.Count` khớp với progress.json

### 4.4 Lỗi encoding (BOM, CRLF, non-NFC)

- Chuyển đổi file sang UTF-8/NFC/LF bằng Python script
- Không dùng PowerShell heredoc cho tiếng Việt (cp1252 issue)

---

## 5. FILES KHÔNG ĐƯỢC GHI ĐÈ/XÓA

| File | Lý do |
|------|-------|
| `books/*.pdf` | Nguyên bản, nguồn chân lý |
| `02_extracted_text/v1/*.txt` | Dữ liệu trích xuất từ PDF |
| `02_extracted_text/v2/*_src.txt` | Source TXT đã tái lập cấu trúc |
| `00_plan/progress.json` | Source of truth trạng thái dự án |
| `99_scripts/extract_chapters.py` | Script trích xuất PDF |
| `99_scripts/ocr_reconstruct.py` | Script tái lập cấu trúc |

---

## 6. CHECKPOINT SUMMARY (TỔNG QUAN)

Khi bắt đầu một session mới, kiểm tra tổng quan:

```json
{
  "total_chapters": 19,
  "completed": X,
  "in_progress": Y,
  "not_started": Z,
  "last_checkpoint": "{chapter}_cp{level}",
  "next_action": "{chapter} CP-{level+1}"
}
```

Cập nhật thông tin này vào `progress.json` và `dashboard.html` sau mỗi session.
