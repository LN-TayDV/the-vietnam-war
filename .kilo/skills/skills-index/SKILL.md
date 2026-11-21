---
name: skills-index
description: Danh mục tổng hợp tất cả skills trong .kilo/skills cho dự án The Cambridge History of the Vietnam War. Cung cấp tổng quan, quan hệ giữa các skills, và hướng dẫn kích hoạt.
---

# Skills Index — The Cambridge History of the Vietnam War Translation Project

## 1. TỔNG QUAN HỆ THỐNG SKILLS

Dự án hiện có **9 skills chuyên biệt** trong `.kilo/skills/`, mỗi skill chịu trách nhiệm một khía cạnh cụ thể của quy trình dịch thuật. Các skills được thiết kế để **bổ sung cho nhau**, không trùng lặp chức năng.

```
.kilo/skills/
├── translation-workflow/              # Workflow chính (entry point)
├── historical-book-translation/       # Quy trình dịch sách lịch sử end-to-end
├── contextual-translation/            # Phân tích ngữ cảnh, lập luận trước khi dịch
├── southern-vietnamese-editorial-style/  # Chuẩn hóa văn phong VNCH (29 quy tắc)
├── historical-terminology-research/   # Nghiên cứu thuật ngữ lịch sử/chính trị/quân sự
├── deep-translation-review/           # Đối chiếu sâu cấp câu/đoạn/chương
├── translation-error-detection/       # Phát hiện lỗi E01-E16 (taxonomy)
├── translation-quality-gate/          # Quality Gate 8 tiêu chí
└── translation-error-kb/              # Cơ sở tri thức lỗi thực tế (E01-E16)
```

## 2. MA TRẬN PHÂN CÔNG CHỨC NĂNG

| Chức năng | Skill chính | Skills hỗ trợ |
|---|---|---|
| **Khởi động session mới** | `translation-workflow` | Tất cả |
| **Đọc nguyên tác, phân đoạn** | `historical-book-translation` | - |
| **Phân tích ngữ pháp, chủ thể/vị ngữ/đối tượng** | `contextual-translation` | `historical-book-translation` |
| **Phân tích quan hệ logic, từ nối** | `contextual-translation` | `southern-vietnamese-editorial-style` |
| **Tra cứu thuật ngữ, xử lý từ/câu khó** | `historical-terminology-research` | `contextual-translation`, `southern-vietnamese-editorial-style` |
| **Tái cấu trúc câu VNCH (chủ động hóa, chỉ định, trạng từ, thể, đại từ, từ nối)** | `southern-vietnamese-editorial-style` | `contextual-translation` |
| **Đối chiếu sâu (câu/đoạn/chương)** | `deep-translation-review` | `translation-error-detection`, `translation-error-kb` |
| **Phát hiện lỗi tự động/thủ công** | `translation-error-detection` | `translation-error-kb`, `deep-translation-review` |
| **Chạy Quality Gate 8 tiêu chí** | `translation-quality-gate` | `translation-error-detection`, `southern-vietnamese-editorial-style` |
| **Tra cứu lỗi thực tế đã gặp** | `translation-error-kb` | `translation-error-detection`, `deep-translation-review` |
| **Quy trình end-to-end chương** | `historical-book-translation` | Tất cả skills trên |

## 3. THỨ TỰ KÍCH HOẠT KHUYẾN NGHỊ

### 3.1 Khi bắt đầu session mới
```
1. translation-workflow (luôn đọc trước)
2. historical-book-translation (nếu dịch chương mới)
3. contextual-translation (luôn kích hoạt khi dịch)
4. southern-vietnamese-editorial-style (luôn kích hoạt khi dịch)
5. historical-terminology-research (khi gặp thuật ngữ/câu khó)
```

### 3.2 Khi dịch một đoạn
```
1. contextual-translation (Bước 1-3: phân tích ngữ pháp, chủ thể/vị ngữ/đối tượng, quan hệ logic)
2. historical-terminology-research (Bước 4: tra cứu thuật ngữ)
3. southern-vietnamese-editorial-style (Bước 5: tái cấu trúc VNCH)
```

### 3.3 Sau khi dịch xong chương
```
1. southern-vietnamese-editorial-style (chạy apply_vnch_fixes.py)
2. translation-error-detection (chạy debug_align.py, check_encoding.py)
3. deep-translation-review (chạy checklist S1-S20, P1-P10, C1-C10)
3. translation-quality-gate (chạy Quality Gate 8 tiêu chí)
4. historical-book-translation (build DOCX, cập nhật progress.json)
```

### 3.4 Khi audit/review
```
1. deep-translation-review (chạy checklist đầy đủ)
2. translation-error-detection (phát hiện E01-E16)
3. translation-error-kb (tra cứu lỗi thực tế, phòng ngừa)
4. translation-quality-gate (verify 8 tiêu chí)
```

## 4. QUAN HỆ GIỮA CÁC SKILLS

```
translation-workflow
    │
    ├── historical-book-translation ────► contextual-translation
    │                                        │
    │                                        ├──► southern-vietnamese-editorial-style
    │                                        │
    │                                        └──► historical-terminology-research
    │
    ├──► deep-translation-review ──────────► translation-error-detection
    │                                        │
    │                                        ├──► translation-error-kb
    │                                        │
    │                                        └──► southern-vietnamese-editorial-style
    │
    └──► translation-quality-gate ─────────► translation-error-detection
                                             │
                                             ├──► southern-vietnamese-editorial-style
                                             │
                                             └──► translation-error-kb
```

**Lưu ý**: Mọi skill đều có thể tham chiếu `translation-error-kb` để tra cứu lỗi thực tế đã gặp.

## 5. TÀI LIỆU CHUNG (SHARED ARTIFACTS)

| Artifact | Vị trí | Skills sử dụng |
|---|---|---|
| `STYLE_GUIDE_PHAN_B.md` | `07_style_guide/` | Tất cả (cơ sở quy tắc) |
| `TRANSLATION_GRAMMAR_ENGINE.md` | `07_style_guide/` | Tất cả (cơ sở quy trình) |
| `MASTER_LEXICON.csv` | `08_southern_vietnamese_library/10_LEXICAL_DATABASE/` | `historical-terminology-research`, `southern-vietnamese-editorial-style`, `contextual-translation` |
| `AUDIT_REPORT_CH01-06.md` | `05_qa/` | Tất cả (bài học thực tế) |
| `progress.json` | `00_plan/` | `translation-workflow`, `historical-book-translation`, `translation-quality-gate` |
| `AUDIT_REPORT_CH01-06.md` §15 | `05_qa/` | `translation-error-kb`, `translation-error-detection` |

## 5. SCRIPTS CHUNG (SHARED TOOLS)

| Script | Vị trí | Skills sử dụng |
|---|---|---|
| `file_integrity.py` | `.kilo/scripts/common/` | Tất cả |
| `translation_validator.py` | `.kilo/scripts/common/` | `translation-error-detection`, `translation-quality-gate` |
| `document_comparator.py` | `.kilo/scripts/common/` | `translation-error-detection`, `translation-quality-gate`, `deep-translation-review` |
| `quality_gate.py` | `.kilo/scripts/common/` | `translation-quality-gate` |
| `vnch_orthography.py` | `.kilo/scripts/common/` | `southern-vietnamese-editorial-style`, `translation-error-detection`, `translation-quality-gate` |
| `encoding_checker.py` | `.kilo/scripts/common/` | `translation-error-detection`, `translation-quality-gate` |
| `docx_builder.py` | `.kilo/scripts/common/` | `historical-book-translation`, `translation-quality-gate` |

**Legacy scripts** (chỉ backward compat):
| Script | Vị trí | Skills sử dụng |
|---|---|---|
| `build_chapter_docx.py` | `99_scripts/` | `historical-book-translation`, `translation-quality-gate` |
| `build_volume_docx.py` | `99_scripts/` | `historical-book-translation`, `translation-quality-gate` |

*Đã xóa: 42 script cũ/debug/chapter-specific/tmp (xem consolidation report).*

## 6. TRẠNG THÁI CẬP NHẬT (2026-11-20)

| Skill | Phiên bản | Trạng thái | Cập nhật lần cuối |
|---|---|---|---|
| `translation-workflow` | v2.0 | ✅ Đã tích hợp 9 skills | 2026-11-20 |
| `historical-book-translation` | v1.0 | ✅ Mới tạo | 2026-11-20 |
| `contextual-translation` | v1.0 | ✅ Mới tạo | 2026-11-20 |
| `southern-vietnamese-editorial-style` | v1.0 | ✅ Mới tạo | 2026-11-20 |
| `historical-terminology-research` | v1.0 | ✅ Mới tạo | 2026-11-20 |
| `deep-translation-review` | v1.0 | ✅ Mới tạo | 2026-11-20 |
| `translation-error-detection` | v1.0 | ✅ Mới tạo | 2026-11-20 |
| `translation-quality-gate` | v1.0 | ✅ Mới tạo | 2026-11-20 |
| `translation-error-kb` | v1.0 | ✅ Mới tạo | 2026-11-20 |

## 7. HƯỚNG DẪN CHO SESSION MỚI

### 7.1 Bước 1: Luôn đọc trước
```bash
# 1. Workflow chính
cat .kilo/skills/translation-workflow/SKILL.md

# 2. Nếu dịch chương mới
cat .kilo/skills/historical-book-translation/SKILL.md

# 3. Luôn kích hoạt khi dịch
cat .kilo/skills/contextual-translation/SKILL.md
cat .kilo/skills/southern-vietnamese-editorial-style/SKILL.md
```

### 7.2 Bước 2: Kích hoạt skill theo nhu cầu
- Gặp thuật ngữ/câu khó → đọc `historical-terminology-research`
- Cần review sâu → đọc `deep-translation-review`
- Phát hiện lỗi → đọc `translation-error-detection` + `translation-error-kb`
- Chạy Quality Gate → đọc `translation-quality-gate`

### 7.3 Bước 3: Tham chiếu tài liệu chung
- `07_style_guide/STYLE_GUIDE_PHAN_B.md` (29 quy tắc)
- `07_style_guide/TRANSLATION_GRAMMAR_ENGINE.md` (7 bước + VNCH Grammar + Checklist)
- `05_qa/AUDIT_REPORT_CH01-06.md` (bài học 6 chương)
- `08_southern_vietnamese_library/10_LEXICAL_DATABASE/MASTER_LEXICON.csv` (321 mục)

## 8. QUY TẮC QUAN TRỌNG

1. **Không bỏ qua skill nào** trong quy trình — mỗi skill có trách nhiệm riêng.
2. **Luôn chạy Quality Gate 8 tiêu chí** trước khi HOAN_TAT.
3. **Không tạo skill mới trùng lặp** — mở rộng skill hiện có.
3. **Lỗi mới phát hiện** → bổ sung vào `translation-error-kb` (có ví dụ thực tế).
4. **Không tự ý thay đổi** cấu trúc thư mục `.kilo/skills` nếu không cần thiết.
5. **Backup trước khi sửa** skill đã ổn định.

---

*Cập nhật: 2026-11-20 — Hệ thống 9 skills hoàn chỉnh cho The Cambridge History of the Vietnam War.*