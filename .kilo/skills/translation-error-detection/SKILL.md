---
name: translation-error-detection
description: Phát hiện lỗi dịch thuật phổ biến: alignment lệch, dịch từng từ (word-for-word), sai thuật ngữ VNCH, từ miền Bắc, từ hiện đại, tên thuộc địa, câu tối nghĩa, tiếng Anh còn sót, thiếu chỉ định, sai trạng từ, sai thể khía, sai đại từ, sai từ nối, fabricate, encoding sai. Dựa trên Error Taxonomy E01-E16 từ Grammar Engine v2.1 và bài học Audit 6 chương đầu + Bảng Đối Chiếu Tiếng Việt PDF (VNCH vs VC).
---

# Skill: Translation Error Detection — Phát Hiện Lỗi Dịch Thuật

## 1. MỤC ĐÍCH
Tự động và thủ công phát hiện các lỗi dịch thuật phổ biến trong bản dịch The Cambridge History of the Vietnam War. Dùng cho: review quá trình dịch, audit chương hoàn tất, quality gate.

## 2. KHI NÀO KÍCH HOẠT
- Sau khi dịch xong chương (trước khi build DOCX).
- Khi chạy `vnch_orthography.py` (phát hiện lỗi thuật ngữ).
- Khi chạy `document_comparator.py` (phát hiện alignment).
- Khi deep review/audit (Deep Translation Review).
- Khi user yêu cầu re-review.

## 3. HỆ THỐNG PHÂN LOẠI LỖI (Error Taxonomy E01-E16)

### 3.1 Lỗi CRITICAL (Phải sửa ngay, chặn HOAN_TAT)

| Mã | Tên lỗi | Mô tả | Cách phát hiện | Ví dụ thực tế |
|---|---|---|---|---|
| **E01** | Thiếu đoạn giữa câu | Câu bị cắt giữa chừng, thiếu tân ngữ/bổ ngữ | Grep pattern `"—$"` hoặc câu không có dấu chấm cuối; đối chiếu số câu src vs vi | Ch1 P012: "Thuật ngữ này —" (bỏ lửng 3 câu cuối) |
| **E02** | Alignment lệch đoạn | Số đoạn src ≠ số đoạn vi; hoặc mapping 1-1 bị phá vỡ | Chạy `document_comparator.py --chapter NN`; đối chiếu marker `[V1CNN-Pxxx]` | Ch1: 49 src vs 50 vi (lệch từ P008, thiếu 11 đoạn); Ch5: 15 src vs 9 vi |
| **E03** | Dịch từng từ ghép lại (Word-for-word) | Giữ cấu trúc tiếng Anh, dịch từ điển từng từ | Grep từ VNCH sai: *chính phủ, chính trị, giải phóng, đồng chí, Annam, Tonkin*; kiểm tra câu có chủ động hóa không | *chính phủ, giải phóng, đồng chí, Annam/Tonkin* xuất hiện 222+ lần trong 6 chương |
| **E04** | Sai thuật ngữ VNCH core | Dùng từ miền Bắc/hiện đại cho thuật ngữ cốt lõi | Chạy `vnch_orthography.py --chapter NN`; grep 120+ từ khóa VNCH | *chính trị→chánh trị* (69), *chính phủ→chánh phủ* (12), *đại biểu→dân biểu* (8) |
| **E14** | Fabricate thông tin | Bịa số trang, trích dẫn, sự kiện, nhân vật không có trong gốc | Đối chiếu số trang, trích dẫn với extracted text; check `[ND: ...]` | Không có trong 6 chương audit, nhưng cần phòng ngừa |
| **E15** | Encoding sai | File không phải UTF-8/NFC/no BOM/LF | Script check bytes; `encoding_checker.py` | PowerShell heredoc tạo cp1252 |
| **E16** | Quality Gate không PASS | Chưa đủ 8 tiêu chí | Chạy full Quality Gate checklist | Chưa đủ 8/8 PASS |

### 3.2 Lỗi MAJOR (Phải sửa, ảnh hưởng chất lượng)

| Mã | Tên lỗi | Mô tả | Cách phát hiện | Ví dụ thực tế |
|---|---|---|---|---|
| **E05** | Sai từ miền Bắc | Dùng *này, giải phóng, đồng chí, chính phủ, chính trị, lương hưu, bất động sản* | Grep danh sách từ miền Bắc (30+ từ); `vnch_orthography.py` | *này→nầy* (47), *giải phóng→độc lập* (28), *đồng chí→đồng đạo* (21) |
| **E06** | Sai từ hiện đại áp đặt | Dùng *tài chính, đại biểu, lương hưu, ngân sách (cơ quan), bất động sản* | Grep danh sách từ hiện đại; `vnch_orthography.py` | *tài chính→tài chánh* (5), *đại biểu→dân biểu* (8), *lương hưu→hưu bổng* (1) |
| **E07** | Sai tên thuộc địa | Giữ *Annam, Tonkin, Cochinchina, Indochine* trong thân bài | Grep *Annam, Tonkin, Cochinchina, Indochine*; Rule 15 check | *Annam/Tonkin/Cochinchina/Indochine* → *Trung Kỳ/Bắc Kỳ/Nam Kỳ/Đông Dương* (38) |
| **E17** | Sai từ vựng VNCH từ PDF | Dùng từ VC/miền Bắc thay vì VNCH theo Bảng Đối Chiếu | Grep 120+ cặp từ từ PDF *doi-chieu-tieng-viet.pdf* | *báo cáo→thưa trình, bảo quản→che chở, bài nói→diễn văn, cách ly→cô lập, cai A-lô→cái điện thoại, cân→căng thẳng, cầu lông→vũ cầu, chất lượng→phẩm chất, chế độ→quy chế, chỉ đạo→chỉ thị, chỉ tiêu→định suất, chúng nhiêm→trường ban, chủ trễ→chú tôa, chửa cháy→cầu hỏa, chiếu đãi→thất đãi, chui→lén lút, chuyện chèo→nói lên, chuyện ngữ→dịch, chứng minh nhân dân→thẻ căn cước, chữ đạo→chính, co cụm→thu hẹp, công đoàn→nghiệp đoàn, công nghiệp→kỹ nghê, công trình→công tác, cơ bản→căn bản, cơ khí→cần bản, cơ sở→căn bản/nguồn gốc, cửa khẩu→phi cảng/hải cảng, cụm từ→nhóm chữ, cứu hộ→cứu cấp, diễn→thành phần, đấu kiện→phương định, đạo trí→tự nhiên, đầu ra/đầu vào→xuất lượng/nhập lượng, đại tiệc/tiểu tiệc→nấu ăn chung/ăn tập thể/nấu ăn riêng/ăn gia đình, đại trà→quy mô/cỡ lớn, đảm bảo→bảo đảm, đăng ký→ghi danh/ghi tên, đáp án→kết quả/trả lời, đăng kí→ghi danh, đồng bằng→phi đạo, đường cao tốc→xa lộ, gia công→làm ăn công, giải phóng→lấy lại/đem đi, giản đơn→đơn giản, giao lưu→giao tiếp/trao đổi, hạch toán→kế toán, hải quan→quan thuế, hàng không dân dụng→hàng không dân sự, hát đôi→song ca, hát tập→hợp ca, hát nhân→nguyên tử, hậu cần→tiếp liệu, học vị→bằng cấp, hệ quả→hậu quả, hiện đại→tối tân, hộ nhà→gia đình, hộ chiếu→sổ thông hành, họp hội→phân khu, họ khẩu→tổ khai gia đình, hội chữ thập đỏ→hội Hồng Thập Tự, kiều hời→ngoại tệ, kiệt xuất→giải/xuất sắc, kinh qua→trải qua, làm gái→làm điếm, làm việc→thẩm vấn/điều tra, lâu năm góc/nhà tráng→ngụy Giác Đốc/Tòa Bạch ốc, liên hoan→đại hội/ăn mừng, liên hệ→liên lạc, linh tinh→vỏ vần, lính gái→nữ quân nhân, lính thủy đánh bộ→thủy quân lực lượng chiến, lợi nhuận→lợi tức, lực tôm→tôm lực, lý giải→giải thích, máy bay lên thẳng→trực thăng, múa đòi→khiêu vũ, mĩ→Mỹ, nằm bật→nằm ngửa, nâng cấp→nâng/đưa giá trị lên, năng nổ→siêng năng/tháo vát, nghệ nhân→thờ/nghệ sỹ, nghệ danh→Tên nghệ sỹ, nghĩa vụ quân sự→Đi quân dịch, nghiêm túc→nghiêm chính, nghiệp dư→đi làm thêm, nhà khách→khách sạn, nhất trí→đồng lòng/đồng ý, nhất quán→luôn luôn/trước sau như một, người nước ngoài→ngoại kiều, noi niệm→viễn suy tư, phân cứng→cường liệu, phân mềm→nhu liệu, phản ánh→phản ảnh, phản hồi→trả lời/hồi âm, phát sóng→phát thanh, phó tiến sĩ→cao học, phi khẩu→phi trường/phi cảng, phi vụ→một vụ trao đổi thường mại, phục hồi nhân phẩm→hoàn lượng, phương án→kế hoạch, quá tài→quá sướng/quá mức, quan triết→hiểu rõ, quân lý→quân trị, quảng trường→công trường, quân hàm→cấp bậc, quy hoạch→kế hoạch, quy trình→tiến trình, sốc→kinh hoàng/kinh ngạc/ngạc nhiên, sổ tân→tân cương, sư đoàn, sức khỏe công dân→y tế công cộng, sự cố→trở ngại, tạp đoàn/doanh nghiệp→công ty, tên lứa→hòa tiến, tham gia lưu thông→lưu hành, tham quan→thẩm viếng, thanh lý→thanh toán/chứng minh, thần thượng→thần mê, thi công→làm, thí phần→thí trường, thu nhập→lợi tức, thư giãn→tĩnh táo/giải trí, thuyết phục→có lý/hợp lý/tin được, tiến tiến→xuất sắc, tiến công→tấn công, tiếp thu→tiếp nhận/thâu nhận/lãnh hội, tiêu dùng→tiêu thụ, tổ lái→phi hành đoàn, tổ rơi→truyền đơn, tranh thủ→cố gắng, trí tuệ→kiến thức, triển khai→khai triển, tư duy→suy nghĩ, tư liệu→tài liệu, từ→tiếng/chữ, uốn tạc→tắt nghiêng, văn dân→văn đề, văn động viên→lực sĩ, viện ung bướu→viện ung thư, vô tư→tự nhiên, xác tín→chính xác, xe con→xe du lịch, xe khách→xe đồ, xử lý→giải quyết/thi hành |

### 3.3 Lỗi MINOR (Nên sửa, ảnh hưởng văn phong)

| Mã | Tên lỗi | Mô tả | Cách phát hiện | Ví dụ thực tế |
|---|---|---|---|---|
| E08 | Bê nguyên cấu trúc bị động | Không chủ động hóa passive tiếng Anh | Grep *bị + V, được + V, bởi + N* | *được ký bởi* → *Chánh phủ đã ký* |
| E09 | Thiếu chỉ định danh từ | *một sách, một kỳ, một người* thiếu *cuốn/cái/con/cây/cục/bài* | Grep `một\s+\w+` không có chỉ định; Rule 21 check | *một sách* → *một cuốn sách / một cái sách* |
| E10 | Sai trạng từ *này/nầy* | Dùng *này* thay *nầy* | Grep `\bnày\b` (loại trừ "trong này, ngoài này..."); Rule 22 | *năm này* → *năm nầy* |
| E11 | Sai thể khía | *đang ký kết* (văn viết) thay *đang tiến hành ký kết* | Grep `đang\s+\w+` không có *xong/tiến hành*; Rule 23 | *đang ký kết* → *đang tiến hành ký kết* |
| E12 | Sai từ nối logic | *tuy nhiên, ngược lại, vì vậy, hơn nữa* | Grep *tuy nhiên, ngược lại, vì vậy, hơn nữa*; Rule 25 | *tuy nhiên* → *tuy vậy/đã vậy*; *ngược lại* → *trái lại* |
| E13 | Sai đại từ nhân xưng | *hắn, y, nó* chỉ người; *ta, tui, mình* (người 1) | Grep *hắn, y, nó* chỉ người; *ta, tui, mình* trong thân bài; Rule 24 | *hắn lập luận* → *người ấy/ông ấy lập luận* |

## 4. CÔNG CỤ PHÁT HIỆN TỰ ĐỘNG

### 4.1 `vnch_orthography.py` — Phát hiện lỗi thuật ngữ (E03, E04, E05, E06, E07, E17)
- Áp dụng 120+ quy tắc VNCH Grammar + Style Guide + PDF.
- Output: danh sách vị trí, từ sai, từ đúng, số lượng, mức độ (CRITICAL/MAJOR/MINOR).
- **False positive handling**: 43 lỗi trong tên sách/trích dẫn/tổ chức tiếng Pháp — KHÔNG SỬA (Style Guide Rule 15).

### 4.2 `document_comparator.py` — Phát hiện alignment (E02)
- So sánh số đoạn src vs vi.
- So sánh số câu mỗi đoạn.
- So sánh cước chú inline markers.
- Output: lệch ở đoạn nào, lệch bao nhiêu câu.

### 4.3 `encoding_checker.py` — Phát hiện encoding (E15)
- Kiểm tra UTF-8, NFC, no BOM, LF.
- Detect cp1252, BOM, CRLF.

### 4.4 `translation_validator.py` — Phát hiện tiếng Anh còn sót, term consistency (E03)
- Quét từ tiếng Anh còn sót trong bản dịch.
- Kiểm tra thuật ngữ không nhất quán.
- Kiểm tra nội dung rỗng.

### 4.5 `quality_gate.py` — Quality Gate 8 tiêu chí (E16)
- Chạy tất cả 8 tiêu chí, output JSON.

### 4.6 Grep Patterns Thủ Công (cho Deep Review)
```bash
# E01: Câu thiếu dấu chấm/bỏ lửng
grep -n "—$" v1_chXX_vi.txt

# E03/E04/E17: Từ VNCH sai (từ PDF + Style Guide)
grep -n -E "chính trị|chính phủ|chính đảng|đảo chính|tài chính|đại biểu|lương hưu|bất động sản|giải phóng|đồng chí|báo cáo|bảo quản|bài nói|cách ly|cái A-lô|cân|cầu lông|chất lượng|chế độ|chỉ đạo|chỉ tiêu|chúng nhiêm|chủ trễ|chửa cháy|chiếu đãi|chui|chuyện chèo|chuyện ngữ|chứng minh nhân dân|chữ đạo|co cụm|công đoàn|công nghiệp|công trình|cơ bản|cơ khí|cơ sở|cửa khẩu|cụm từ|cứu hộ|diễn|đấu kiện|đạo trí|đầu ra|đầu vào|đại tiệc|tiểu tiệc|đại trà|đảm bảo|đăng ký|đáp án|đăng kí|đồng bằng|đường cao tốc|gia công|giải phóng|giản đơn|giao lưu|hạch toán|hải quan|hàng không dân dụng|hát đôi|hát tập|hát nhân|hậu cần|học vị|hệ quả|hiện đại|hộ nhà|hộ chiếu|họp hội|họ khẩu|hội chữ thập đỏ|kiều hời|kiệt xuất|kinh qua|làm gái|làm việc|lâu năm góc|nhà tráng|liên hoan|liên hệ|linh tinh|lính gái|lính thủy đánh bộ|lợi nhuận|lực tôm|lý giải|máy bay lên thẳng|múa đòi|mĩ|nằm bật|nâng cấp|năng nổ|nghệ nhân|nghệ danh|nghĩa vụ quân sự|nghiêm túc|nghiệp dư|nhà khách|nhất trí|nhất quán|người nước ngoài|noi niệm|phân cứng|phân mềm|phản ánh|phản hồi|phát sóng|phó tiến sĩ|phi khẩu|phi vụ|phục hồi nhân phẩm|phương án|quá tài|quan triết|quân lý|quảng trường|quân hàm|quy hoạch|quy trình|sốc|sổ tân|sư đoàn|sức khỏe công dân|sự cố|tạp đoàn|doanh nghiệp|tên lứa|tham gia lưu thông|tham quan|thanh lý|thần thượng|thi công|thí phần|thu nhập|thư giãn|thuyết phục|tiến tiến|tiến công|tiếp thu|tiêu dùng|tổ lái|tổ rơi|tranh thủ|trí tuệ|triển khai|tư duy|tư liệu|từ|uốn tạc|văn dân|văn động viên|viện ung bướu|vô tư|xác tín|xe con|xe khách|xử lý" v1_chXX_vi.txt

# E05: Từ miền Bắc
grep -n -E "\bnày\b(?!.*(trong|ngoài|trước|sau)\s+nầy)" v1_chXX_vi.txt

# E06: Từ hiện đại
grep -n -E "tài chính|đại biểu|lương hưu|ngân sách.*cơ quan|bất động sản|bảo hiểm|báo cáo|bảo quản|bài nói|cách ly|cảnh báo|cái A-lô|cân|cầu lông|chất lượng|chế độ|chỉ đạo|chỉ tiêu|chúng nhiêm|chủ trễ|chửa cháy|chiếu đãi|chui|chuyện chèo|chuyện ngữ|chứng minh nhân dân|chữ đạo|co cụm|công đoàn|công nghiệp|công trình|cơ bản|cơ khí|cơ sở|cửa khẩu|cụm từ|cứu hộ|diễn|đấu kiện|đạo trí|đầu ra|đầu vào|đại tiệc|tiểu tiệc|đại trà|đảm bảo|đăng ký|đáp án|đăng kí|đồng bằng|đường cao tốc|gia công|giải phóng|giản đơn|giao lưu|hạch toán|hải quan|hàng không dân dụng|hát đôi|hát tập|hát nhân|hậu cần|học vị|hệ quả|hiện đại|hộ nhà|hộ chiếu|họp hội|họ khẩu|hội chữ thập đỏ|kiều hời|kiệt xuất|kinh qua|làm gái|làm việc|lâu năm góc|nhà tráng|liên hoan|liên hệ|linh tinh|lính gái|lính thủy đánh bộ|lợi nhuận|lực tôm|lý giải|máy bay lên thẳng|múa đòi|mĩ|nằm bật|nâng cấp|năng nổ|nghệ nhân|nghệ danh|nghĩa vụ quân sự|nghiêm túc|nghiệp dư|nhà khách|nhất trí|nhất quán|người nước ngoài|noi niệm|phân cứng|phân mềm|phản ánh|phản hồi|phát sóng|phó tiến sĩ|phi khẩu|phi vụ|phục hồi nhân phẩm|phương án|quá tài|quan triết|quân lý|quảng trường|quân hàm|quy hoạch|quy trình|sốc|sổ tân|sư đoàn|sức khỏe công dân|sự cố|tạp đoàn|doanh nghiệp|tên lứa|tham gia lưu thông|tham quan|thanh lý|thần thượng|thi công|thí phần|thu nhập|thư giãn|thuyết phục|tiến tiến|tiến công|tiếp thu|tiêu dùng|tổ lái|tổ rơi|tranh thủ|trí tuệ|triển khai|tư duy|tư liệu|từ|uốn tạc|văn dân|văn động viên|viện ung bướu|vô tư|xác tín|xe con|xe khách|xử lý" v1_chXX_vi.txt

# E07: Tên thuộc địa
grep -n -E "Annam|Tonkin|Cochinchina|Cochinchine|Indochine" v1_chXX_vi.txt

# E08: Bị động
grep -n -E "bị\s+\w+|được\s+\w+|bởi\s+\w+" v1_chXX_vi.txt

# E09: Thiếu chỉ định
grep -n -E "một\s+(sách|ký|người|ngày|năm|cái|cuốn|bài)" v1_chXX_vi.txt

# E10: này/nầy
grep -n "\bnày\b" v1_chXX_vi.txt

# E11: thể khía
grep -n "đang\s+\w+$" v1_chXX_vi.txt

# E12: từ nối
grep -n -E "tuy nhiên|ngược lại|vì vậy|hơn nữa" v1_chXX_vi.txt

# E13: đại từ
grep -n -E "\b(hắn|y|nó)\b.*[^.]*[^.]*[^.]*\." v1_chXX_vi.txt

# E15: Encoding
file v1_chXX_vi.txt  # phải ra "UTF-8 Unicode text"
```

## 5. QUY TRÌNH PHÁT HIỆN TRONG DEEP REVIEW

### 5.1 Tự động (chạy scripts)
```bash
# 1. Kiểm tra alignment
python .kilo/scripts/common/document_comparator.py --chapter NN

# 2. Kiểm tra thuật ngữ VNCH (từ PDF + Style Guide)
python .kilo/scripts/common/vnch_orthography.py --chapter NN

# 3. Kiểm tra encoding
python .kilo/scripts/common/encoding_checker.py --chapter NN

# 4. Kiểm tra validation (tiếng Anh còn sót, term consistency)
python .kilo/scripts/common/translation_validator.py --chapter NN

# 5. Quality Gate tổng hợp
python .kilo/scripts/common/quality_gate.py --chapter NN

# 6. Build DOCX verify (dùng docx_builder.py)
python -c "from docx_builder import DocxBuilder; from pathlib import Path; b=DocxBuilder(Path('.')); r=b.build_chapter(Path('translation-project/04_translation/v1/chNN/v1_chNN_vi.txt'), Path('translation-project/09_docx/V1-CNN_<slug>.docx')); print(r)"

# 7. Word COM check
# Footnotes.Count = progress.json notes
```

### 5.2 Thủ công (Deep Review)
- Chạy grep patterns (§4.6) cho từng loại lỗi.
- Đối chiếu từng câu S1-S20.
- Đối chiếu từng đoạn P1-P10.
- Kiểm tra alignment C2, cước chú C3, encoding C6.

## 6. XỬ LÝ FALSE POSITIVE (Quan trọng)

| Loại | Ví dụ | Xử lý |
|---|---|---|
| Tên sách/trích dẫn | "The Politics of Annam" → giữ "Annam" | **KHÔNG SỬA** — Style Guide Rule 15 |
| Tên tổ chức tiếng Pháp | "Parti Communiste Français" → giữ "Communiste" | **KHÔNG SỬA** — Rule 15 |
| Tên tổ chức VNCH có "Đồng Chí/Giải Phóng" | "Việt Nam Thanh Niên Cách Mạng Đồng Chí Hội" | **Giữ nguyên** — tên riêng, thêm ghi chú `[ND: ...]` |
| Trích dẫn tiếng Anh/Pháp trong cước chú | Giữ nguyên hoàn toàn | **KHÔNG SỬA** — Rule 11 |

**43 false positive** trong audit 6 chương đều thuộc loại này.

## 7. LIÊN KẾT SKILLS
- **deep-translation-review**: Sử dụng taxonomy E01-E17 khi audit.
- **southern-vietnamese-editorial-style**: Cung cấp danh sách từ sai/đúng (120+ quy tắc từ PDF + Style Guide).
- **historical-terminology-research**: Cung cấp thuật ngữ chuẩn.
- **translation-quality-gate**: Chặn HOAN_TAT nếu còn lỗi CRITICAL/MAJOR.
- **historical-book-translation**: Chạy phát hiện trước build DOCX.
- **contextual-translation**: Phân tích ngữ cảnh để chọn từ đúng.

---

*Cập nhật: 2026-11-20 — Dựa trên Grammar Engine v2.1 §6 (Error Taxonomy E01-E16), Audit 6 chương §2, Bảng Đối Chiếu Tiếng Việt (PDF: doi-chieu-tieng-viet.pdf, ~120 cặp từ VNCH-VC), vnch_orthography.py, document_comparator.py, translation_validator.py, quality_gate.py.*