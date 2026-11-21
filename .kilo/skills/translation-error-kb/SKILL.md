---
name: translation-error-kb
description: Cơ sở tri thức lỗi dịch thuật thực tế — chuyển các lỗi đã gặp trong audit 6 chương đầu thành quy tắc phòng ngừa có thể tái sử dụng. Mỗi lỗi có: mô tả, nguyên nhân, ví dụ thực tế, quy tắc phòng ngừa, cách phát hiện, cách khắc phục, skill chịu trách nhiệm. Dựa trên Audit 6 chương đầu (222 lỗi thuật ngữ, alignment lệch, word-for-word, từ/câu khó).
---

# Skill: Translation Error Knowledge Base — Cơ Sở Tri Thức Lỗi Dịch Thuật

## 1. MỤC ĐÍCH
Chuyển **lỗi thực tế đã gặp** trong audit 6 chương đầu thành **tri thức phòng ngừa có thể tái sử dụng**. Mỗi lỗi có: mô tả, nguyên nhân, ví dụ thực tế, quy tắc phòng ngừa, cách phát hiện, cách khắc phục, skill chịu trách nhiệm.

**Không bịa ví dụ. Không đưa lỗi giả định.** Chỉ ghi nhận lỗi thực tế đã gặp và đã sửa trong audit 6 chương đầu (2026-11-19).

## 2. CẤU TRÚC MỖI LỖI
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E01-E16 (theo Error Taxonomy Grammar Engine §6) |
| **Mô tả** | Tóm tắt ngắn gọn lỗi |
| **Nguyên nhân** | Tại sao lỗi xảy ra |
| **Ví dụ thực tế** | Trích dẫn từ audit 6 chương (chương, đoạn, câu gốc ↔ câu dịch) |
| **Quy tắc phòng ngừa** | Quy tắc trong Style Guide / Grammar Engine ngăn lỗi này |
| **Cách phát hiện** | Script, grep pattern, checklist, manual review |
| **Cách khắc phục** | Bước sửa cụ thể |
| **Skill chịu trách nhiệm** | Skill nào phát hiện/sửa lỗi này |

## 3. DANH SÁCH LỖI THỰC TẾ (TỪ AUDIT 6 CHƯƠNG ĐẦU)

---

### E01: Thiếu đoạn giữa câu (CRITICAL)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E01 |
| **Mô tả** | Câu bị cắt giữa chừng, bỏ lửng tân ngữ/bổ ngữ, thiếu dấu chấm kết thúc |
| **Nguyên nhân** | Dịch không đối chiếu số câu; footnotes chen lấn vào thân bài; alignment lệch làm mất câu cuối đoạn |
| **Ví dụ thực tế** | **Ch1 P012**: Nguyên tác có 3 câu cuối "The term 'ai quoc'... Nguyen Ai Quoc." → Bản dịch chỉ còn "Thuật ngữ này —" (bỏ lửng, thiếu 3 câu) |
| **Quy tắc phòng ngừa** | **Quy tắc 16**: Kết thúc bằng dấu chấm, đủ số câu như nguyên tác. **S11**: Không bớt nghĩa. **P4**: Đoạn kết thúc bằng dấu chấm. |
| **Cách phát hiện** | `grep -n "—$" v1_chXX_vi.txt` (câu kết thúc bằng dash); đối chiếu số câu src vs vi (S11, P5); `debug_align.py` |
| **Cách khắc phục** | Dịch lại câu bị cắt; đối chiếu số câu; realign nếu cần (`ch01_realign.py` sentence-level alignment) |
| **Skill chịu trách nhiệm** | `deep-translation-review` (S11, P4, P5), `translation-quality-gate` (C2, C10), `historical-book-translation` (Bước 6-7) |

---

### E02: Alignment lệch đoạn (CRITICAL)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E02 |
| **Mô tả** | Số đoạn src ≠ số đoạn vi; mapping 1-1 bị phá vỡ; cước chú neo sai vị trí |
| **Nguyên nhân** | Dịch gộp nhiều đoạn gốc thành 1 block; hoặc tách 1 đoạn thành nhiều; footnotes chen lấn làm lệch marker |
| **Ví dụ thực tế** | **Ch1**: 49 src paragraphs vs 50 vi paragraphs (lệch từ P008), thiếu 11 đoạn cuối "Anglophone Histories". **Ch5**: 15 src vs 9 vi (gộp block). **Ch2,3,4,6**: Lệch 1-2 câu ở nhiều đoạn. |
| **Quy tắc phòng ngừa** | **Quy tắc 18**: Bắt buộc `số đoạn src == số đoạn vi` trước build DOCX. **C2**: Chạy `debug_align.py`. **P5**: Số câu đoạn dịch = số câu gốc. |
| **Cách phát hiện** | `python 99_scripts/debug_align.py NN` → so sánh số đoạn, số câu mỗi đoạn; kiểm tra marker `[V1CNN-Pxxx]` |
| **Cách khắc phục** | Chạy `realign.py` (sentence-level alignment cho Ch1/Ch5); fix thủ công lệch câu nhỏ; rebuild DOCX |
| **Skill chịu trách nhiệm** | `translation-quality-gate` (C2, C10), `deep-translation-review` (C2, P5), `historical-book-translation` (Bước 2, Bước 6) |

---

### E03: Dịch từng từ ghép lại — Word-for-Word (CRITICAL)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E03 |
| **Mô tả** | Giữ cấu trúc tiếng Anh, dịch từ điển từng từ/cụm từ rồi ghép lại → câu cứng, sai ngữ pháp, sai thuật ngữ |
| **Nguyên nhân** | Không đọc toàn câu/đoạn/ngữ cảnh; không phân tích chủ thể/vị ngữ/đối tượng; không tái cấu trúc theo VNCH Grammar |
| **Ví dụ thực tế** | 222 lỗi trong 6 chương: *chính phủ, giải phóng, đồng chí, Annam, Tonkin, Cochinchina, Indochine, tài chính, đại biểu, lương hưu, bất động sản, ngân sách* — dịch theo từ điển từng từ |
| **Quy tắc phòng ngừa** | **Quy tắc 19 (CẤM KỊ)**: Tuyệt đối cấm dịch từng từ rồi ghép. **Bước 5 Grammar Engine**: Đọc toàn câu/đoạn/ngữ cảnh → phân tích chủ thể/vị ngữ/đối tượng/quan hệ logic → tra lexicon/VNCH Grammar → tái cấu trúc câu Việt tự nhiên. **S9**: Không cấu trúc ngoại ngữ bê nguyên. |
| **Cách phát hiện** | Grep 30 từ khóa VNCH sai: `grep -n "chính trị\|chính phủ\|giải phóng\|đồng chí\|Annam\|Tonkin\|Cochinchina\|Indochine\|tài chính\|đại biểu\|lương hưu\|bất động sản" v1_chXX_vi.txt`; Checklist S9 (cấu trúc ngoại ngữ) |
| **Cách khắc phục** | Viết lại toàn bộ câu theo quy trình Bước 5: đọc ngữ cảnh → phân tích → tra lexicon → tái cấu trúc VNCH (chủ động hóa, chỉ định, trạng từ nầy/đó/kia, thể khía, đại từ, từ nối, từ nối logic Nam Bộ) |
| **Skill chịu trách nhiệm** | `contextual-translation` (Bước 1-5), `southern-vietnamese-editorial-style` (S9, S13-S20), `deep-translation-review` (S9, E03), `translation-error-detection` (E03) |

---

### E04: Sai thuật ngữ VNCH core (CRITICAL)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E04 |
| **Mô tả** | Dùng từ miền Bắc/hiện đại cho thuật ngữ cốt lõi VNCH: *chính trị, chính phủ, chính đảng, đảo chính, tài chính, đại biểu, lương hưu, bất động sản, ngân sách* |
| **Nguyên nhân** | Không tra MASTER_LEXICON; không áp dụng Style Guide Quy tắc 1, 3, 4, 12; dùng từ điển hiện đại/miền Bắc |
| **Ví dụ thực tế** | 222 lỗi trong 6 chương: *chính trị→chánh trị* (69), *chính phủ→chánh phủ* (12), *chính đảng→chánh đảng* (3), *đảo chính→đảo chánh* (2), *tài chính→tài chánh* (5), *đại biểu→dân biểu* (8), *lương hưu→hưu bổng* (1), *bất động sản→địa ốc* (0), *ngân sách (cơ quan)→ngân khố* |
| **Quy tắc phòng ngừa** | **Quy tắc 1, 3, 4, 12**: Ưu tiên dạng VNCH đã kiểm chứng. **MASTER_LEXICON** tra cứu bắt buộc. **S12**: Thuật ngữ có trong lexicon. **S13, S14**: Không dùng từ miền Bắc/hiện đại. **apply_vnch_fixes.py** áp dụng 30 quy tắc tự động. |
| **Cách phát hiện** | `python 99_scripts/apply_vnch_fixes.py --check-only NN`; grep 30 từ khóa; Orthography check (Quality Gate tiêu chí 2) |
| **Cách khắc phục** | Chạy `python 99_scripts/apply_vnch_fixes.py NN` (fix tự động 30 quy tắc); review 43 false positive (tên sách/trích dẫn/tổ chức tiếng Pháp — KHÔNG SỬA); fix thủ công lỗi còn lại |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S12-S14), `historical-terminology-research` (tra cứu), `translation-error-detection` (E04), `translation-quality-gate` (tiêu chí 2) |

---

### E05: Sai từ miền Bắc (MAJOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E05 |
| **Mô tả** | Dùng từ miền Bắc trong thân bài: *này, giải phóng, đồng chí, chính phủ, chính trị, lương hưu, bất động sản, ngân sách (cơ quan)* |
| **Nguyên nhân** | Thói quen dùng từ điển hiện đại/miền Bắc; không áp dụng Style Guide Quy tắc 2, 8, 22, 24 |
| **Ví dụ thực tế** | *này→nầy* (47), *giải phóng→độc lập/kháng cự* (28), *đồng chí→đồng đạo* (21), *mặc dù→dầu/dẫu* (4), *tuy nhiên→tuy vậy/đã vậy* (15), *vì vậy→bởi thế/do đó* (12), *hơn nữa→vả/lại* (3), *người ấy/ông ấy/bà ấy* thay *hắn/y/nó* |
| **Quy tắc phòng ngừa** | **Quy tắc 2**: Dùng dạng Nam Bộ. **Quy tắc 22**: *nầy/đó/kia*. **Quy tắc 24**: *người ấy/ông ấy/bà ấy/họ*. **Quy tắc 25**: *dầu/dẫu, trái lại, tuy vậy, bởi thế, vả*. **S13, S16, S17, S19, S20** checklist. |
| **Cách phát hiện** | `apply_vnch_fixes.py --check-only`; grep patterns: `\bnày\b`, `giải phóng`, `đồng chí`, `mặc dù`, `tuy nhiên`, `vì vậy`, `hơn nữa`, `hắn|y|nó` chỉ người |
| **Cách khắc phục** | Chạy `apply_vnch_fixes.py` (fix tự động); fix thủ công trạng từ *nầy/đó/kia*, thể khía, đại từ |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S13-S20), `contextual-translation` (ngữ cảnh), `translation-error-detection` (E05) |

---

### E06: Sai từ hiện đại áp đặt (MAJOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E06 |
| **Mô tả** | Dùng thuật ngữ hiện đại áp đặt vào văn bản VNCH: *tài chính, đại biểu, lương hưu, ngân sách (cơ quan), bất động sản* |
| **Nguyên nhân** | Không tuân thủ Quy tắc 12 (KHÔNG hiện đại hóa); dùng từ điển hiện đại |
| **Ví dụ thực tế** | *tài chính→tài chánh* (5), *đại biểu→dân biểu* (8), *lương hưu→hưu bổng* (1), *ngân sách (cơ quan)→ngân khố*, *bất động sản→địa ốc* |
| **Quy tắc phòng ngừa** | **Quy tắc 12**: KHÔNG thay thuật ngữ VNCH bằng hiện đại. **Quy tắc 3, 4**: Thuật ngữ kinh tế/chính trị VNCH. **S14** checklist. |
| **Cách phát hiện** | `apply_vnch_fixes.py --check-only`; grep `tài chính|đại biểu|lương hưu|ngân sách.*cơ quan|bất động sản` |
| **Cách khắc phục** | Chạy `apply_vnch_fixes.py`; tra MASTER_LEXICON để xác nhận dạng VNCH |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S14), `historical-terminology-research` (tra cứu), `translation-error-detection` (E06) |

---

### E07: Sai tên thuộc địa (MAJOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E07 |
| **Mô tả** | Giữ tên gọi thuộc địa Pháp (*Annam, Tonkin, Cochinchina, Cochinchine, Indochine*) trong thân bài bản dịch |
| **Nguyên nhân** | Không áp dụng Quy tắc 15: Tên thuộc địa → tên VNCH + gốc trong ngoặc lần đầu |
| **Ví dụ thực tế** | 38 lần trong 6 chương: *Annam→Trung Kỳ (Annam)*, *Tonkin→Bắc Kỳ (Tonkin)*, *Cochinchina/Cochinchine→Nam Kỳ (Cochinchina)*, *Indochine→Đông Dương (Indochine)*. Trong trích dẫn tiếng Anh/Pháp → giữ nguyên. |
| **Quy tắc phòng ngừa** | **Quy tắc 15**: Dùng tên VNCH (Nam Kỳ, Trung Kỳ, Bắc Kỳ, Đông Dương) + gốc trong ngoặc lần đầu. Trong trích dẫn tiếng Anh/Pháp → giữ nguyên. **S15** (tương tự). |
| **Cách phát hiện** | `apply_vnch_fixes.py --check-only`; grep `Annam|Tonkin|Cochinchina|Cochinchine|Indochine` (loại trừ trích dẫn) |
| **Cách khắc phục** | Chạy `apply_vnch_fixes.py`; fix thủ công: thêm tên VNCH, giữ gốc trong ngoặc lần đầu; trích dẫn tiếng Anh/Pháp giữ nguyên |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (Quy tắc 15), `historical-terminology-research` (Rule 15), `translation-error-detection` (E07) |

---

### E08: Bê nguyên cấu trúc bị động (MINOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E08 |
| **Mô tả** | Không chủ động hóa passive tiếng Anh khi tiếng Việt tự nhiên hơn |
| **Nguyên nhân** | Không áp dụng Quy tắc 26 (QUY TẮC VÀNG: luôn ưu tiên chủ động hóa) |
| **Ví dụ thực tế** | *was signed by the government* → *được ký bởi chánh phủ* (sai) → đúng: *Chánh phủ đã ký...*; *was brought to an end by Lê Lợi* → *bị chấm dứt bởi Lê Lợi* (sai) → đúng: *Lê Lợi đã chấm dứt...* |
| **Quy tắc phòng ngừa** | **Quy tắc 26**: Luôn ưu tiên chủ động hóa. **S18** checklist. **§1.6 Grammar Engine**: Passive *bị + V* chỉ dùng khi mang sắc thái tiêu cực. |
| **Cách phát hiện** | Grep `bị\s+\w+|được\s+\w+|bởi\s+\w+`; Checklist S18 |
| **Cách khắc phục** | Chuyển sang chủ động: xác định tác nhân (by...) → làm chủ ngữ; thể hoàn thành *đã... rùi/hẵng* |
| **Skill chịu trách nhiệm** | `contextual-translation` (Bước 2, Bước 5), `southern-vietnamese-editorial-style` (S18, Quy tắc 26), `deep-translation-review` (S18) |

---

### E09: Thiếu chỉ định danh từ (MINOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E09 |
| **Mô tả** | Danh từ không có chỉ định phù hợp Nam Bộ: *một sách* (thiếu *cuốn/cái*), *một kỳ* (thiếu *thời kỳ*), *một người* (thiếu *con/người/ngài*) |
| **Nguyên nhân** | Không áp dụng Quy tắc 21 (Chỉ định danh từ Nam Bộ) |
| **Ví dụ thực tế** | *một sách* → *một cuốn sách / một cái sách*; *một kỳ* → *một thời kỳ nầy*; *a man* → *một con người / một người ấy* |
| **Quy tắc phòng ngừa** | **Quy tắc 21**: Bắt buộc thêm chỉ định theo bảng §1.3. **S15** checklist. |
| **Cách phát hiện** | Grep `một\s+(sách|ký|người|ngày|năm|cái|cuốn|bài)` thiếu chỉ định; Checklist S15 |
| **Cách khắc phục** | Thêm chỉ định: *cuốn/cái/con/cây/cục/bài/người/ngài* theo bảng §1.3 |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S15, Quy tắc 21), `contextual-translation` (Bước 5), `deep-translation-review` (S15) |

---

### E10: Sai trạng từ *này/nầy* (MINOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E10 |
| **Mô tả** | Dùng *này* thay *nầy* (trừ "trong này, ngoài này, trước này, sau này") |
| **Nguyên nhân** | Không áp dụng Quy tắc 22 (Trạng từ không gian/thời gian Nam Bộ) |
| **Ví dụ thực tế** | *năm này* → *năm nầy*; *ngày này* → *ngày nầy*; *trước đây* → *trước nầy*; *sau này* → *sau nầy* (trừ cụ trúc "trong này, ngoài này, trước này, sau này") |
| **Quy tắc phòng ngừa** | **Quy tắc 22**: Bắt buộc *nầy/đó/kia*. **S16** checklist. **§1.4 Grammar Engine**. |
| **Cách phát hiện** | Grep `\bnày\b` (loại trừ "trong này|ngoài này|trước này|sau này"); Checklist S16 |
| **Cách khắc phục** | Thay *này* → *nầy* (trừ 4 cụ trúc cố định) |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S16, Quy tắc 22), `deep-translation-review` (S16) |

---

### E11: Sai thể khía *đang* (MINOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E11 |
| **Mô tả** | Dùng *đang + V* (dạng rút gọn) thay dạng đầy đủ Nam Bộ *đang... xong/tiến hành* trong văn viết |
| **Nguyên nhân** | Không áp dụng Quy tắc 23 (Thể khía Nam Bộ đầy đủ) |
| **Ví dụ thực tế** | *đang ký kết* → *đang tiến hành ký kết / đang ký kết xong*; *đang dựng* → *đang tiến hành dựng / đang dựng xong* |
| **Quy tắc phòng ngừa** | **Quy tắc 23**: Dạng đầy đủ *đang... xong/tiến hành*. **S17** checklist. **§1.5 Grammar Engine**. |
| **Cách phát hiện** | Grep `đang\s+\w+$` (cuối câu) hoặc `đang\s+\w+` không có *xong/tiến hành*; Checklist S17 |
| **Cách khắc phục** | Mở rộng: *đang tiến hành + V* hoặc *đang + V + xong* |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S17, Quy tắc 23), `deep-translation-review` (S17) |

---

### E12: Sai từ nối logic (MINOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E12 |
| **Mô tả** | Dùng từ nối miền Bắc/hiện đại: *tuy nhiên, ngược lại, vì vậy, hơn nữa* |
| **Nguyên nhân** | Không áp dụng Quy tắc 25 (Từ nối logic Nam Bộ) |
| **Ví dụ thực tế** | *Tuy nhiên, kết quả...* → *Tuy vậy / Đã vậy / Bởi thế, kết quả...*; *Ngược lại, miền Nam...* → *Trái lại, miền Nam...*; *Vì vậy, chánh phủ...* → *Bởi thế / Do đó, chánh phủ...*; *Hơn nữa, còn có...* → *Vả / Lại / Cũng, còn có...* |
| **Quy tắc phòng ngừa** | **Quy tắc 25**: Ưu tiên *dầu/dẫu, trái lại, tuy vậy/đã vậy/song, bởi thế/do đó/cho nên, vả/lại/cũng*. **S20** checklist. **§1.8 Grammar Engine**. |
| **Cách phát hiện** | Grep `tuy nhiên|ngược lại|vì vậy|hơn nữa|hơn thế nữa`; Checklist S20 |
| **Cách khắc phục** | Thay thế theo bảng Quy tắc 25 |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S20, Quy tắc 25), `contextual-translation` (Bước 3), `deep-translation-review` (S20) |

---

### E13: Sai đại từ nhân xưng (MINOR)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E13 |
| **Mô tả** | Dùng *hắn, y, nó* chỉ người; *ta, tui, mình* (người 1); *mày, tao, cậu* (người 2) trong thân bài học thuật |
| **Nguyên nhân** | Không áp dụng Quy tắc 24 (Đại từ nhân xưng trang trọng VNCH) |
| **Ví dụ thực tế** | *hắn lập luận* → *người ấy/ông ấy lập luận*; *nó là nhà sử học* → *người ấy/ông ấy là nhà sử học*; *ta thấy rằng* → *tôi/tác giả nhận thấy rằng* |
| **Quy tắc phòng ngừa** | **Quy tắc 24**: Bắt buộc *người ấy/ông ấy/bà ấy/họ*. Cấm *hắn, y, nó* chỉ người; *ta, tui, mình*; *mày, tao, cậu*. **S19** checklist. **§1.7 Grammar Engine**. |
| **Cách phát hiện** | Grep `\b(hắn|y|nó)\b` chỉ người; `ta|tui|mình` (người 1); `mày|tao|cậu` (người 2) trong thân bài; Checklist S19 |
| **Cách khắc phục** | Thay: *hắn/y/nó* → *người ấy/ông ấy/bà ấy/nó* (vật); *ta/tui/mình* → *tôi/tác giả/chúng tôi*; *mày/tao/cậu* → *ông/bà/quý vị* |
| **Skill chịu trách nhiệm** | `southern-vietnamese-editorial-style` (S19, Quy tắc 24), `deep-translation-review` (S19) |

---

### E14: Fabricate thông tin (CRITICAL)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E14 |
| **Mô tả** | Bịa đặt số trang, trích dẫn, ví dụ, sự kiện, nhân vật không có trong nguyên tác |
| **Nguyên nhân** | Tự thêm thông tin "giúp người đọc hiểu hơn" mà không có trong gốc |
| **Ví dụ thực tế** | Audit 6 chương: **Không có fabricate** (PASS), nhưng cần quy tắc phòng ngừa. Nếu cần bổ sung ngữ cảnh → dùng cước chú `[ND: Người dịch bổ sung...]`. |
| **Quy tắc phòng ngừa** | **Quy tắc 27**: Tuyệt đối cấm fabricate. Mọi thông tin phải truy xuất về nguyên tác. Bổ sung ngữ cảnh → cước chú `[ND: ...]`. **P10** checklist. |
| **Cách phát hiện** | Đối chiếu số trang, trích dẫn, tên người, sự kiện với extracted text; check `[ND: ...]` có phải người dịch bổ sung không |
| **Cách khắc phục** | Xóa phần bịa; nếu cần ngữ cảnh → thêm cước chú `[ND: Người dịch bổ sung...]` |
| **Skill chịu trách nhiệm** | `translation-quality-gate` (tiêu chí 5), `deep-translation-review` (P10), `historical-book-translation` (Bước 3) |

---

### E15: Encoding sai (CRITICAL)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E15 |
| **Mô tả** | File không phải UTF-8/NFC/no BOM/LF (cp1252, BOM, CRLF) → lỗi font, dấu thanh, dấu câu |
| **Nguyên nhân** | Dùng PowerShell heredoc cho tiếng Việt (cp1252 issue); không dùng Python script ghi file |
| **Ví dụ thực tế** | PowerShell `cat <<EOF > file.txt` với tiếng Việt → cp1252, hỏng dấu thanh. Python `open(..., encoding='utf-8', newline='\n')` → đúng. |
| **Quy tắc phòng ngừa** | **Quy tắc 28**: Bắt buộc UTF-8, NFC, no BOM, LF. Python: `encoding="utf-8", newline="\n"`. PowerShell: KHÔNG heredoc tiếng Việt — dùng Python script. **C6** checklist. |
| **Cách phát hiện** | `python -c "import sys; f=open('file.txt','rb'); b=f.read(); print('UTF-8:', all(b[i]<128 or (b[i]>>5)==6 and b[i+1]>>6==2 for i in range(len(b)-1) if b[i]>>5==6))"`; `file file.txt` (phải ra "UTF-8 Unicode text") |
| **Cách khắc phục** | Ghi lại file bằng Python script: `open(path, 'w', encoding='utf-8', newline='\n')` |
| **Skill chịu trách nhiệm** | `historical-book-translation` (Bước 6), `translation-quality-gate` (C6), `translation-error-detection` (E15) |

---

### E16: Quality Gate không PASS (CRITICAL)
| Trường | Nội dung |
|---|---|
| **Mã lỗi** | E16 |
| **Mô tả** | Chương chưa đủ 8 tiêu chí Quality Gate nhưng vẫn được đánh dấu HOAN_TAT |
| **Nguyên nhân** | Không chạy đầy đủ Quality Gate; bỏ qua tiêu chí khó; tự nhận "xong" |
| **Ví dụ thực tế** | Audit 6 chương: Tất cả 6 chương PASS 8/8 sau khi fix. Trước fix: Ch1 alignment fail, Ch5 alignment fail, orthography fail. |
| **Quy tắc phòng ngừa** | **Quy tắc 29**: Chỉ HOAN_TAT khi 8 tiêu chí PASS. **C10** checklist. **progress.json** chỉ cập nhật khi tất cả PASS. |
| **Cách phát hiện** | Chạy đầy đủ 8 tiêu chí Quality Gate (script + Word COM); check `progress.json` status |
| **Cách khắc phục** | Fix tiêu chí FAIL → chạy lại toàn bộ 8 tiêu chí → mới cập nhật `status: "HOAN_TAT"` |
| **Skill chịu trách nhiệm** | `translation-quality-gate` (C10), `historical-book-translation` (Bước 8), `translation-error-detection` (E16) |

---

## 4. TỔNG KẾT: PHÂN BỔ SKILL CHỊU TRÁCH NHIỆM

| Skill | Lỗi chịu trách nhiệm phát hiện/sửa |
|---|---|
| **historical-book-translation** | E01 (Bước 6-7), E02 (Bước 2,6), E14 (Bước 3), E15 (Bước 6), E16 (Bước 8) |
| **contextual-translation** | E03 (Bước 1-5), E08 (Bước 2,5), E09 (Bước 5) |
| **southern-vietnamese-editorial-style** | E04 (S12-S14), E05 (S13-S20), E06 (S14), E07 (Quy tắc 15), E08 (S18), E09 (S15), E10 (S16), E11 (S17), E12 (S20), E13 (S19) |
| **historical-terminology-research** | E04 (tra cứu), E06 (tra cứu), E07 (Rule 15) |
| **deep-translation-review** | E01 (S11,P4,P5), E02 (C2,P5), E03 (S9,E03), E04 (S12), E05 (S13-S20), E08 (S18), E09 (S15), E10 (S16), E11 (S17), E12 (S20), E13 (S19), E14 (P10) |
| **translation-error-detection** | E01-E16 (phát hiện qua script/grep/checklist) |
| **translation-quality-gate** | E01-E16 (chặn HOAN_TAT qua 8 tiêu chí), E14 (tiêu chí 5), E15 (C6), E16 (C10) |
| **historical-book-translation** | Toàn bộ quy trình tích hợp các skill trên |

---

## 5. LIÊN KẾT SKILLS
- Tất cả skills trong hệ thống `.kilo/skills` đều tham chiếu KB này.
- Khi phát hiện lỗi mới trong audit/review → bổ sung vào KB này (có ví dụ thực tế, không giả định).
- KB này là **single source of truth** cho lỗi thực tế đã gặp.

---

*Cập nhật: 2026-11-20 — Dựa trên Audit 6 chương đầu (2026-11-19), Grammar Engine v2.1 §6 (E01-E16), Task re-review 2026-11-20.*