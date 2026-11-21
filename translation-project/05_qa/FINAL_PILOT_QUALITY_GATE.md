# FINAL PILOT QUALITY GATE — V1-CH1 & STYLE_GUIDE B

> Ngày: 2026-11-18. UTF-8, NFC, không BOM.
> Phạm vi kiểm định: `STYLE_GUIDE_PHAN_B.md`, `v1_ch01_vi.txt` (P001–P012, trang 27–31), `v1_ch01_pilot_review.md`.
> Đối chiếu nguyên tác: `02_extracted_text/v1/ch01.txt` (trang 27–31, tác giả Liam C. Kelley).
> Mục tiêu: Xác định pilot và Style Guide có đủ cơ sở phê duyệt trước khi dịch 77 chương hay không.

---

## 1. Executive Summary

Pilot V1-Ch1 (12 đoạn, trang 27–31) thể hiện **năng lực dịch thuật ở mức khá**: văn phong Nam Bộ nhất quán, thuật ngữ VNCH có nguồn cho những từ then chốt (*chánh trị, độc lập, thuộc địa, bảo hộ, triều đình, quan lại, sĩ phu*), và không có lỗi pha trộn miền Bắc.

Tuy nhiên, vòng kiểm định này phát hiện **một lỗi CRITICAL** và **hai lỗi MAJOR** cần sửa trước khi phê duyệt:

1. **CRITICAL — P012 bị cắt giữa đoạn**: Bản dịch kết thúc ở "Thuật ngữ này —" trong khi nguyên tác còn tiếp tục giải thích nghĩa "ái quốc" ("cherish the country") và liên hệ với tên cách mạng Nguyễn Ái Quốc. Đoạn chưa hoàn tất.
2. **MAJOR — P011 và P012: "Annam and Tonkin" bị dịch thành "Trung Kỳ và Bắc Kỳ"**: Nguyên tác dùng tên thuộc địa Pháp (Annam, Tonkin) để nhấn mạnh cách gọi của thực dân; bản dịch thay bằng tên Việt Nam, làm mất ngữ cảnh lịch sử.
3. **MAJOR — Tệp nguồn `v1_ch01_src.txt` không đầy đủ**: Chỉ chứa P001–P007, thiếu P008–P012. Không thể đối chiếu 5 đoạn sau cùng với nguyên tác từ chính tệp này.

Ngoài ra, **6 thuật ngữ** dùng trong pilot chưa có mục trong MASTER_LEXICON (evidence gap): *dân tộc, chủng tộc, Nam Kỳ, Trung Kỳ, Bắc Kỳ, mặt trận*. Các từ này cần được bổ sung vào lexicon hoặc ghi nhận là khoảng trống.

**Kết luận**: Pilot **NEEDS_REVISION**. Cần sửa 3 lỗi nêu trên, bổ sung nguồn cho 6 thuật ngữ, và hoàn thiện tệp nguồn trước khi phê duyệt. Style Guide cần bổ sung 3 quy tắc (xử lý tên thuộc địa Pháp, phương pháp dịch thuật, kiểm tra hoàn tất đoạn).

---

## 2. Sentence-by-Sentence Review

Bảng đối chiếu từng đoạn: Original (Anh) → Translation (Việt) → Term Decisions → Evidence → Review Status.

### P001 (trang 27)

| # | Original | Translation | Term Decisions | Evidence | Status |
|---|---|---|---|---|---|
| 1 | "revolutionary leader Hồ Chí Minh" | "nhà lãnh đạo cách mạng Hồ Chí Minh" | *nhà lãnh đạo cách mạng* (trung tính) | STYLE_GUIDE B.6 | ✅ PASS |
| 1 | "published a short article entitled 'Nên học sử ta'" | "cho đăng một bài ngắn nhan đề 'Nên học sử ta'" | *cho đăng* (nhà lãnh đạo cho đăng); *nhan đề* (Nam Bộ) | STYLE_GUIDE D.4 | ✅ PASS |
| 1 | "a newspaper that Hồ Chí Minh had established the previous year" | "tờ báo mà năm trước Người đã lập ra" | *Người* (kính ngữ Hồ Chí Minh) | STYLE_GUIDE D.2 | ✅ PASS |
| 1 | "called Việt Nam độc lập, or Independent Vietnam" | "lấy tên là _Việt Nam độc lập_ (Independent Vietnam)" | Giữ tên báo + giải nghĩa | STYLE_GUIDE D.4 | ✅ PASS |
| 1 | "the northern province of Cao Bằng" | "tỉnh miền Bắc là Cao Bằng" | *tỉnh miền Bắc* | Lê Văn Đức (SRC-001) | ✅ PASS |
| 1 | "where Hồ Chí Minh resided for a time in 1941 and 1942" | "nơi Hồ Chí Minh từng sống một thời gian trong những năm 1941 và 1942" | *từng sống* | — | ✅ PASS |
| 1 | "after crossing the border from southern China" | "sau khi vượt biên giới từ miền Nam Trung Hoa" | *Trung Hoa* (Nam Bộ, không dùng *Trung Quốc*) | STYLE_GUIDE C.2 | ✅ PASS |
| 1 | "to organize a united front against French rule and Japanese occupation known as the Việt Minh" | "để tổ chức một mặt trận hợp nhất chống lại ách cai trị của Pháp và cuộc chiếm đóng của Nhật, gọi là Việt Minh" | ***mặt trận hợp nhất*** — nên dùng *mặt trận thống nhất* | "thống nhất" VERIFIED (SRC-023, Điều 1); "hợp nhất" KHÔNG có trong lexicon | ⚠️ MINOR |
| 1 | "Published three times a month with a run of 400 copies" | "Mỗi tháng ra ba kỳ với số lượng 400 bản" | *ba kỳ* | — | ✅ PASS |
| 1 | "Independent Vietnam's reach was probably quite limited" | "tầm với của _Việt Nam độc lập_ e rằng cũng khá giới hạn" | *e rằng* (Nam Bộ) | ORTHOGRAPHY CH-02 | ✅ PASS |
| 1 | "However" | "Tuy vậy" | *Tuy vậy* (Nam Bộ) | STYLE_GUIDE B.3(a) | ✅ PASS |
| 1 | "the interpretation of the past... would be repeated countless times" | "cách diễn giải về quá khứ... đã được nhắc lại vô số lần" | *cách diễn giải* | — | ✅ PASS |
| 1 | "in the thirty years of revolution and war from 1945 to 1975" | "trong ba mươi năm cách mạng và chiến tranh từ 1945 đến 1975" | — | — | ✅ PASS |
| 1 | "serves today as a key element in Vietnamese nationalism and identity" | "cho đến nay vẫn là một yếu tố then chốt trong chủ nghĩa dân tộc và căn tính của người Việt" | *căn tính* = identity | — | ✅ PASS |

**Đánh giá P001**: 13/14 câu PASS, 1 câu MINOR (mặt trận hợp nhất → thống nhất).

### P002 (trang 27)

| # | Original | Translation | Status |
|---|---|---|---|
| 2 | "The gist of Hồ Chí Minh's view... summarized in two sentences" | "Cốt lõi trong cái nhìn của Hồ Chí Minh... tóm gọn trong hai câu" | ✅ PASS |
| 2 | "Whenever our people unite as one, our country is independent and free" | "Dân ta khi nào đoàn kết một lòng thì nước ta được độc lập và tự do" | ✅ PASS (trích nguyên văn Hồ Chí Minh) |
| 2 | "By contrast, whenever our people do not unite, we are invaded" | "Trái lại, dân ta khi nào không đoàn kết thì bị ngoại nhân xâm lăng" | ✅ PASS (trích nguyên văn) |
| 2 | "a list of 'Ten Musts' (10 Điều nên)" | "một danh sách 'Mười điều nên' (10 Điều nên)" | ✅ PASS |
| 2 | "also penned by Hồ Chí Minh" | "do chính Hồ Chí Minh chấp bút" | ✅ PASS (*chấp bút* = penned, Nam Bộ) |
| 2 | "ten acts... must carry out" | "mười việc... phải làm" | ✅ PASS |
| 2 | 10 điều (giữ bí mật → ủng hộ báo) | 10 điều (giữ bí mật → ủng hộ báo) | ✅ PASS (từng mục đối chiếu khớp) |

**Đánh giá P002**: 100% PASS.

### P003 (trang 27-28)

| # | Original | Translation | Status |
|---|---|---|---|
| 3 | "Although Hồ Chí Minh argued in 1942" | "Dầu vào năm 1942 Hồ Chí Minh lập luận rằng" | ✅ PASS (*Dầu* = although, Nam Bộ) |
| 3 | "the key lesson to learn from the Vietnamese past" | "bài học cốt yếu rút ra từ quá khứ Việt Nam" | ✅ PASS |
| 3 | "was that Vietnamese needed to unite to maintain independence" | "là người Việt cần đoàn kết để giữ gìn nền độc lập của xứ sở" | ✅ PASS |
| 3 | "we can see today that what Hồ Chí Minh was attempting to unite... was history and revolutionary politics" | "ngày nay ta có thể thấy điều Hồ Chí Minh tìm cách hợp nhất... chính là sử học và chánh trị cách mạng" | ✅ PASS |
| 3 | "While one could argue that historical writings... had always been political" | "Dẫu có người cho rằng mọi trước tác về sử Việt Nam xưa nay vốn đã mang tính chánh trị" | ✅ PASS (*Dẫu* = while/although) |
| 3 | "earlier works had supported other types of politics" | "các công trình trước đó đã phụng sự những thứ chánh trị khác" | ✅ PASS (*phụng sự* = serve, văn chương) |
| 3 | "dynastic politics... colonial politics" | "chánh trị triều đình... chánh trị thuộc địa" | ✅ PASS |
| 3 | "to tell the story of the production of historical knowledge" | "thuật lại câu chuyện sản sinh ra tri thức sử học" | ✅ PASS |
| 3 | "is to tell the story of the political history of Vietnam" | "cũng chính là thuật lại lịch sử chánh trị của Việt Nam" | ✅ PASS |
| 3 | "how the two processes have closely mirrored each other" | "cái cách hai tiến trình ấy soi bóng vào nhau một cách khăng khít" | ✅ PASS (*soi bóng* = mirror, Nam Bộ văn chương) |

**Đánh giá P003**: 100% PASS.

### P004 (trang 28)

| # | Original | Translation | Status |
|---|---|---|---|
| 4 | "That said" | "Đã vậy" | ✅ PASS |
| 4 | "the aim of this essay is not simply to point out" | "mục tiêu của bài này không phải chỉ để chỉ ra" | ✅ PASS |
| 4 | "how writings about Vietnamese history have been influenced by politics" | "những trước tác về sử Việt Nam đã chịu ảnh hưởng của chánh trị ra sao" | ✅ PASS |
| 4 | "Instead, its goal is to provide an historical background" | "Trái lại, chỗ nhắm của nó là cung cấp một cái nền sử liệu" | ✅ PASS (*chỗ nhắm* = aim, Nam Bộ) |
| 4 | "that will enable readers to better understand the articles in this Cambridge History" | "để độc giả có thể hiểu rõ hơn các bài trong bộ _Cambridge History of the Vietnam War_ này" | ✅ PASS |
| 4 | "many ideas... that are new" | "nhiều ý niệm... là mới" | ✅ PASS |
| 4 | "scholars have conducted new research and made new findings" | "giới học giả đã khảo cứu những điều mới và tìm ra những phát hiện mới" | ✅ PASS |
| 4 | "a movement away from certain 'truths'" | "một sự chuyển hướng rời xa những 'chân lý'" | ✅ PASS |
| 4 | "that previously dominated writings" | "trước kia từng ngự trị trong các trước tác" | ✅ PASS (*ngự trị* = dominate, văn chương) |
| 4 | "where those 'truths' came from, and how they came to be adopted" | "những 'chân lý' ấy từ đâu mà ra, và bằng cách nào chúng đã được... chấp nhận" | ✅ PASS |

**Đánh giá P004**: 100% PASS.

### P005 (trang 28) — đề mục

| Original | Translation | Status |
|---|---|---|
| "From Traditional to Modern Histories" | "Từ Sử Học Cổ Truyền đến Sử Học Hiện Đại" | ✅ PASS (viết hoa đề mục đúng) |

### P006 (trang 28-29)

| # | Original | Translation | Status |
|---|---|---|---|
| 6 | "The first histories produced by Vietnamese were dynastic histories" | "Những bộ sử đầu tiên do người Việt soạn ra đều là sử triều đình" | ✅ PASS |
| 6 | "the fifteenth-century Complete Book... (Đại Việt sử ký toàn thư)" | "bộ _Đại Việt sử ký toàn thư_ thế kỷ mười lăm" | ✅ PASS |
| 6 | "the nineteenth-century... (Khâm định Việt sử thông giám cương mục)" | "bộ _Khâm định Việt sử thông giám cương mục_ thế kỷ mười chín" | ✅ PASS |
| 6 | "composed in classical Chinese" | "soạn bằng chữ Hán cổ" | ✅ PASS |
| 6 | "only a small percentage of the population could understand" | "chỉ một phần nhỏ dân chúng mới hiểu được" | ✅ PASS |
| 6 | "historical examples of good and bad governance" | "những thí dụ lịch sử về chánh trị tốt và xấu" | ✅ PASS |
| 6 | "in the hopes that current dynastic officials would learn from the past" | "với hy vọng các quan lại đương triều sẽ học được điều hay từ người xưa" | ✅ PASS |

**Đánh giá P006**: 100% PASS.

### P007 (trang 29)

| # | Original | Translation | Status |
|---|---|---|---|
| 7 | "Until the nineteenth century" | "Cho đến thế kỷ mười chín" | ✅ PASS |
| 7 | "largely restricted to the world of court officials" | "phần lớn chỉ giới hạn trong giới quan lại triều đình" | ✅ PASS |
| 7 | "the tiny literate elite aspiring to enter government service" | "tầng lớp sĩ phu biết chữ rất nhỏ nhoi đang mong vào làm quan" | ✅ PASS |
| 7 | "some Western missionaries and travelers learned what they could" | "một số giáo sĩ và lữ khách phương Tây có học được đôi điều" | ✅ PASS |
| 7 | "gaining access to actual historical texts proved to be difficult" | "muốn với tay đến chính các văn bản sử liệu thì lại là chuyện khó" | ✅ PASS (*với tay* = reach, Nam Bộ) |

**Đánh giá P007**: 100% PASS.

### P008 (trang 29)

| # | Original | Translation | Status |
|---|---|---|---|
| 8 | "That situation changed, however" | "Dầu vậy, tình hình ấy đã thay đổi" | ✅ PASS |
| 8 | "with the French conquest of Vietnam" | "cùng với cuộc chinh phục Việt Nam của Pháp" | ✅ PASS |
| 8 | "The extension of French control... was a decades-long process" | "Việc Pháp mở rộng quyền kiểm soát... là một tiến trình kéo dài hàng thập niên" | ✅ PASS |
| 8 | "but it began with treaties in the 1860s" | "nhưng khởi đầu bằng những hiệp ước trong thập niên 1860" | ✅ PASS |
| 8 | "the ruling Nguyễn Dynasty granted the French direct control" | "triều Nguyễn nhượng cho Pháp quyền kiểm soát trực tiếp" | ✅ PASS |
| 8 | "the southern third of Vietnam, or what they called Cochinchine" | "một phần ba phía Nam Việt Nam, tức xứ mà họ gọi là Nam Kỳ (Cochinchine)" | ✅ PASS |
| 8 | "a French missionary by the name of Théophile Marie Legrand de la Liraye" | "một giáo sĩ Pháp tên là Théophile Marie Legrand de la Liraye" | ✅ PASS |
| 8 | "wrote the first history of Vietnam in French" | "đã viết bộ sử Việt Nam đầu tiên bằng tiếng Pháp" | ✅ PASS |
| 8 | "While this work was based on Vietnamese sources" | "Công trình ấy tuy dựa trên các nguồn sử liệu Việt" | ✅ PASS |
| 8 | "began a process of the 'Westernization'" | "đã khởi đầu một tiến trình 'phương Tây hóa'" | ✅ PASS |
| 8 | "employed European concepts to explain the past" | "dùng các khái niệm Âu châu để giải thích quá khứ" | ✅ PASS |

**Đánh giá P008**: 100% PASS.

### P009 (trang 29-30)

| # | Original | Translation | Status |
|---|---|---|---|
| 9 | "Whereas the Complete Book and Comprehensive Mirror documented" | "Trong khi bộ _Toàn thư_ và bộ _Cương mục_ chép" | ✅ PASS |
| 9 | "a political genealogy from one ruling house to another" | "một phả hệ chánh trị từ triều đại này sang triều đại khác" | ✅ PASS |
| 9 | "the purpose of Legrand de la Liraye's work was to educate" | "thì mục đích công trình của Legrand de la Liraye là để giáo dục" | ✅ PASS |
| 9 | "the history of a people, or what he called the 'Annamite nation'" | "lịch sử của một dân tộc, hay cái mà ông gọi là 'dân tộc Annam'" | ✅ PASS |
| 9 | "attempted to determine what race the Annamites belonged to" | "đã thử xác định người Annam thuộc chủng tộc nào" | ✅ PASS |
| 9 | "so that his European readers could understand" | "để độc giả Âu châu của ông có thể hiểu được" | ✅ PASS |
| 9 | "in relation to other racial groups in the region" | "trong tương quan với các nhóm chủng tộc khác trong vùng" | ✅ PASS |
| 9 | "These two concepts of nation and race were Western concepts" | "Hai khái niệm dân tộc và chủng raced này là các khái niệm phương Tây" | ✅ PASS |
| 9 | "never been previously applied to the history of Vietnam" | "trước đó chưa từng được áp dụng cho lịch sử Việt Nam" | ✅ PASS |

**Đánh giá P009**: 100% PASS.

### P010 (trang 30)

| # | Original | Translation | Status |
|---|---|---|---|
| 10 | "Another important idea... was the concept of 'independence'" | "Một ý niệm quan trọng khác... là khái niệm 'độc lập'" | ✅ PASS |
| 10 | "There was a period in the early fifteenth century" | "Có một thời kỳ vào đầu thế kỷ mười lăm" | ✅ PASS |
| 10 | "the Chinese Ming Dynasty controlled the areas" | "triều Minh của Trung Hoa kiểm soát các vùng" | ✅ PASS (*Trung Hoa* — Nam Bộ) |
| 10 | "what is now northern and north-central Vietnam" | "nay là miền Bắc và Bắc Trung Bộ Việt Nam" | ✅ PASS |
| 10 | "That brief period was brought to an end by a man named Lê Lợi" | "Thời kỳ ngắn ngủi ấy chấm dứt bởi một người tên là Lê Lợi" | ⚠️ MINOR — *chấm dứt bởi* (bị động) hơi cứng; nên dùng chủ động: "một người tên Lê Lợi đã chấm dứt" |
| 10 | "the founder of the Lê Dynasty" | "vị vua sáng lập triều Lê" | ✅ PASS |
| 10 | "The Complete Book simply stated that Lê Lợi had 'wiped out the Ming bandits'" | "Bộ _Toàn thư_ chỉ đơn giản chép rằng Lê Lợi đã 'dẹp yên giặc Minh'" | ✅ PASS |
| 10 | "By contrast, Legrand de la Liraye depicted that same event as a 'war of independence'" | "Trái lại, Legrand de la Liraye mô tả cùng một biến cố lịch sử ấy như một 'cuộc chiến tranh giành độc lập'" | ✅ PASS |
| 10 | "This was another new concept" | "Đây lại là một khái niệm mới" | ✅ PASS |
| 10 | "when Hồ Chí Minh declared in 1942 that Vietnamese history was a timeless story" | "khi Hồ Chí Minh tuyên bố năm 1942 rằng lịch sử Việt Nam là câu chuyện bất diệt" | ✅ PASS |
| 10 | "the Vietnamese people (dân tộc) uniting (đoàn kết)" | "dân tộc Việt Nam đoàn kết" | ✅ PASS |
| 10 | "to maintain the independence (độc lập) and freedom (tự do) of the country" | "để giữ gìn độc lập và tự do của xứ sở" | ✅ PASS |
| 10 | "his interpretation of the past was filled with words and concepts" | "cách diễn giải quá khứ của ông đã đầy ăm ắp những từ ngữ và khái niệm" | ✅ PASS (*đầy ăm ắp* — Nam Bộ) |
| 10 | "that his ancestors would not have understood" | "mà tổ tiên ông hẳn không hiểu được" | ✅ PASS |
| 10 | "That Hồ Chí Minh understood these words... was because they all became part of the Vietnamese worldview" | "Sở dĩ Hồ Chí Minh hiểu được... là vì tất cả đã trở thành một phần trong thế giới quan Việt Nam" | ✅ PASS |
| 10 | "during the years of French colonial rule" | "trong những năm Pháp thuộc" | ✅ PASS |

**Đánh giá P010**: 15/16 PASS, 1 MINOR (chấm dứt bởi → chủ động).

### P011 (trang 30) — ⚠️ CÓ VẤN ĐỀ

| # | Original | Translation | Status |
|---|---|---|---|
| 11 | "Such ideas were adopted first in Cochinchina" | "Những ý niệm ấy được tiếp nhận trước tiên tại Nam Kỳ" | ✅ PASS |
| 11 | "the French established a new educational system" | "người Pháp thiết lập một hệ thống giáo dục mới" | ✅ PASS |
| 11 | "Trương Vĩnh Ký, a Vietnamese Catholic polymath" | "Trương Vĩnh Ký, một học giả Công giáo Việt Nam lỗi lạc" | ⚠️ MINOR — *polymath* (nhà bác học) → *học giả lỗi lạc* mất nghĩa "bác học toàn diện"; nên dùng *nhà bác học* |
| 11 | "produced a history of Vietnam in French for the Vietnamese students" | "đã soạn một bộ sử Việt Nam bằng tiếng Pháp cho học sinh Việt Nam" | ✅ PASS |
| 11 | "a Vietnamese translation... called a Brief History of the Country of Dai Nam" | "nhan đề _Đại Nam quốc lược sử_" | ✅ PASS |
| 11 | "educational reforms were implemented in the center and north" | "cải cách giáo dục được thực hiện tại Trung Kỳ và Bắc Kỳ" | ✅ PASS |
| 11 | "modernize the curriculum for the traditional civil-service examinations" | "hiện đại hóa chương trình học cho các kỳ thi khoa cử truyền thống" | ✅ PASS |
| 11 | "the central and northern regions had both become protectorates of France" | "cả Trung Kỳ và Bắc Kỳ đều đã trở thành xứ bảo hộ của Pháp" | ✅ PASS |
| 11 | **"Known as Annam and Tonkin, respectively"** | **"Gọi là Trung Kỳ và Bắc Kỳ"** | ❌ **MAJOR** — Nguyên tác dùng tên thuộc địa Pháp (Annam, Tonkin) để chỉ cách gọi của thực dân; bản dịch thay bằng tên Việt Nam, mất ngữ cảnh lịch sử |
| 11 | "these regions were still governed by Nguyễn Dynasty officials" | "các xứ này vẫn do quan lại triều Nguyễn cai trị" | ✅ PASS |
| 11 | "albeit under the guidance of French advisors" | "tuy dưới sự hướng dẫn của các cố vấn Pháp" | ✅ PASS |
| 11 | "Proficient in classical Chinese, some of those officials learned a great deal" | "Thành thạo chữ Hán cổ, một số quan lại trong số ấy đã học được rất nhiều điều" | ✅ PASS |
| 11 | "through the writings of Chinese reformist intellectuals" | "qua các trước tác của các trí thức cải cách Trung Hoa" | ✅ PASS |
| 11 | "transformed the educational curriculum in accordance with these new ideas" | "họ đã cải biến chương trình giáo dục theo những ý niệm mới này" | ✅ PASS |

**Đánh giá P011**: 13/15 PASS, 1 MINOR (polymath), **1 MAJOR (Annam/Tonkin → Trung Kỳ/Bắc Kỳ)**.

### P012 (trang 30-31) — ❌ CÓ VẤN ĐỀ NGHIÊM TRỌNG

| # | Original | Translation | Status |
|---|---|---|---|
| 12 | "A clear example of this is a work that was produced in 1906" | "Một thí dụ rõ rệt là một công trình soạn năm 1906" | ✅ PASS |
| 12 | "employed in the reformed curriculum in Annam and Tonkin" | "được dùng trong chương trình cải cách tại Trung Kỳ và Bắc Kỳ" | ❌ **MAJOR** — cùng lỗi P011 (Annam/Tonkin → Trung Kỳ/Bắc Kỳ) |
| 12 | "by a scholar named Hoàng Đạo Thành" | "bởi một học giả tên là Hoàng Đạo Thành" | ✅ PASS |
| 12 | "entitled the Complete Compilation... (Việt sử tân ước toàn biên)" | "nhan đề _Việt sử tân ước toàn biên_" | ✅ PASS |
| 12 | "the first history created by a Vietnamese that was structured around the concept of the nation" | "bộ sử đầu tiên do người Việt soạn có cấu trúc xoay quanh khái niệm dân tộc" | ✅ PASS |
| 12 | "It explicitly aimed to inculcate readers with a sense of pride" | "Nó minh nhiên nhắm đến việc hun đúc cho độc giả một ý thức tự hào" | ✅ PASS (*hun đúc* = inculcate, Nam Bộ) |
| 12 | "the Complete Book and the Comprehensive Mirror were designed to teach" | "bộ _Toàn thư_ và bộ _Cương mục_ được soạn để dạy" | ✅ PASS |
| 12 | "morally upright rule and the need to be loyal (trung) to the monarch" | "đức trị nước ngay thẳng và lòng trung thành với vua" | ✅ PASS |
| 12 | "Hoàng Đạo Thành's history was designed to teach students to be patriotic (ái quốc)" | "bộ sử của Hoàng Đạo Thành được soạn để dạy học sinh lòng ái quốc" | ✅ PASS |
| 12 | **"This term for 'patriotism' literally means 'cherish the country.'"** | **"(THIẾU TRONG BẢN DỊCH)"** | ❌ **CRITICAL** — Bản dịch kết thúc ở "Thuật ngữ này —" giữa đoạn, thiếu phần giải thích nghĩa "ái quốc" |
| 12 | "It was a Western concept introduced to Vietnamese scholars" | "(THIẾU)" | ❌ CRITICAL |
| 12 | "it was a term that Hồ Chí Minh took as part of his revolutionary name, Nguyễn Ái Quốc" | "(THIẾU)" | ❌ CRITICAL |

**Đánh giá P012**: 7/10 PASS, 1 MAJOR (Annam/Tonkin), **1 CRITICAL (bản dịch chưa hoàn tất — thiếu 3 câu cuối)**.

---

## 3. Grammar and Semantic Errors

### 3.1. Lỗi CRITICAL

#### CRITICAL-1: P012 — Bản dịch bị cắt giữa đoạn

| Mục | Nội dung |
|---|---|
| **Original** | "This term for 'patriotism' literally means 'cherish the country.' It was a Western concept introduced to Vietnamese scholars through the writings of Chinese reformers, and it was a term that Hồ Chí Minh took as part of his revolutionary name, Nguyễn Ái Quốc, not long after Hoàng Đạo Thành produced his new account of the Vietnamese past." |
| **Current Translation** | "Thuật ngữ này —" (kết thúc, không có nội dung tiếp theo) |
| **Problem** | Bản dịch dừng giữa câu. Người đọc không hiểu nghĩa "ái quốc" là gì, không biết liên hệ với tên Nguyễn Ái Quốc. Mất thông tin ngữ nghĩa quan trọng của đoạn. |
| **Proposed Translation** | "Thuật ngữ *ái quốc* này theo nghĩa chữ là 'yêu nước, thương nước'. Đó là một khái niệm phương Tây được du nhập vào giới học giả Việt Nam qua các trước tác của các nhà cải cách Trung Hoa, và đó cũng là từ mà Hồ Chí Minh lấy làm một phần tên cách mạng của mình, Nguyễn Ái Quốc, không lâu sau khi Hoàng Đạo Thành cho ra đời công trình sử mới về quá khứ Việt Nam." |
| **Reason** | Hoàn tất đoạn; giữ nghĩa "cherish the country" = yêu nước/thương nước; giải thích liên hệ Nguyễn Ái Quốc. |
| **Evidence** | Nguyên tác `02_extracted_text/v1/ch01.txt` dòng 162–166. |
| **Severity** | **CRITICAL** |

### 3.2. Lỗi MAJOR

#### MAJOR-1: P011 & P012 — "Annam and Tonkin" → "Trung Kỳ và Bắc Kỳ"

| Mục | Nội dung |
|---|---|
| **Original (P011)** | "Known as Annam and Tonkin, respectively, these regions were still governed by Nguyễn Dynasty officials" |
| **Original (P012)** | "employed in the reformed curriculum in Annam and Tonkin" |
| **Current Translation (P011)** | "Gọi là Trung Kỳ và Bắc Kỳ, các xứ này vẫn do quan lại triều Nguyễn cai trị" |
| **Current Translation (P012)** | "được dùng trong chương trình cải cách tại Trung Kỳ và Bắc Kỳ" |
| **Problem** | Nguyên tác dùng tên thuộc địa Pháp (*Annam, Tonkin*) vì đang mô tả cách gọi của thực dân Pháp. Bản dịch thay bằng tên Việt Nam (*Trung Kỳ, Bắc Kỳ*), làm mất ngữ cảnh lịch sử: người đọc không còn thấy sự khác biệt giữa tên gọi thực dân và tên gọi Việt Nam. Đây là thay đổi ngữ nghĩa, không chỉ là dịch thuật. |
| **Proposed Translation (P011)** | "Gọi là Annam (Trung Kỳ) và Tonkin (Bắc Kỳ), các xứ này vẫn do quan lại triều Nguyễn cai trị" |
| **Proposed Translation (P012)** | "được dùng trong chương trình cải cách tại Annam (Trung Kỳ) và Tonkin (Bắc Kỳ)" |
| **Reason** | Giữ tên thuộc địa Pháp (nguyên tác) + giải nghĩa tiếng Việt trong ngoặc. Tuân theo STYLE_GUIDE Quy tắc 9 (giữ thuật ngữ gốc + giải nghĩa). |
| **Evidence** | Nguyên tác dòng 135–136, 142. |
| **Severity** | **MAJOR** |

### 3.3. Lỗi MINOR

#### MINOR-1: P001 — "mặt trận hợp nhất" → "mặt trận thống nhất"

| Mục | Nội dung |
|---|---|
| **Original** | "to organize a united front against French rule" |
| **Current Translation** | "để tổ chức một mặt trận hợp nhất chống lại ách cai trị của Pháp" |
| **Problem** | "United front" trong tiếng Anh chính trị = "mặt trận thống nhất" hoặc "mặt trận đoàn kết". "Hợp nhất" (unify/merge) không sai về từ nguyên nhưng không phải lối nói chuẩn của thuật ngữ này. |
| **Proposed Translation** | "để tổ chức một mặt trận thống nhất chống lại ách cai trị của Pháp" |
| **Reason** | "Thống nhất" có trong lexicon (SRC-023, Hiến pháp 1967, Điều 1 — VERIFIED). "Hợp nhất" không có trong lexicon. |
| **Evidence** | MASTER_LEXICON.csv dòng 315: "thống nhất — VERIFIED — SRC-023". |
| **Severity** | MINOR |

#### MINOR-2: P010 — "chấm dứt bởi" (bị động cứng)

| Mục | Nội dung |
|---|---|
| **Original** | "That brief period was brought to an end by a man named Lê Lợi" |
| **Current Translation** | "Thời kỳ ngắn ngủi ấy chấm dứt bởi một người tên là Lê Lợi" |
| **Problem** | "Chấm dứt bởi" là cấu trúc bị động, hơi cứng trong tiếng Việt. Tiếng Việt ưa dùng chủ động hơn. |
| **Proposed Translation** | "Thời kỳ ngắn ngủi ấy đã chấm dứt khi một người tên là Lê Lợi, vị vua sáng lập triều Lê, đã dẹp yên quân Minh" — hoặc đơn giản: "Một người tên là Lê Lợi đã chấm dứt thời kỳ ngắn ngủi ấy" |
| **Reason** | Giữ nghĩa nguyên tác, nhưng dùng cấu trúc chủ động tự nhiên hơn trong tiếng Việt. |
| **Evidence** | — |
| **Severity** | MINOR |

#### MINOR-3: P011 — "polymath" → "học giả lỗi lạc"

| Mục | Nội dung |
|---|---|
| **Original** | "Trương Vĩnh Ký, a Vietnamese Catholic polymath" |
| **Current Translation** | "Trương Vĩnh Ký, một học giả Công giáo Việt Nam lỗi lạc" |
| **Problem** | *Polymath* = người thông thạo nhiều lĩnh vực (nhà bác học). *Học giả lỗi lạc* = scholar xuất chúng. Hai từ này không đồng nghĩa: *polymath* nhấn mạnh bề rộng kiến thức, *học giả lỗi lạc* nhấn mạnh sự xuất sắc. Trương Vĩnh Ký được gọi là *polymath* vì ông thông thạo nhiều lĩnh vực (ngôn ngữ, văn học, sử học, giáo dục). |
| **Proposed Translation** | "Trương Vĩnh Ký, một nhà bác học Công giáo Việt Nam" |
| **Reason** | *Nhà bác học* là thuật ngữ tiếng Việt cho *polymath* (ví dụ: Lê Quý Đôn, Trương Vĩnh Ký đều được gọi là nhà bác học). Giữ đúng nghĩa nguyên tác. |
| **Evidence** | — |
| **Severity** | MINOR |

### 3.4. Kiểm tra 8 tiêu chí ngữ pháp/ngữ nghĩa

| Tiêu chí | Kết quả |
|---|---|
| 1. Semantic Fidelity (trung thành ngữ nghĩa) | ✅ 11/12 đoạn đúng; ❌ P012 thiếu 3 câu cuối |
| 2. Grammatical Integrity (đúng ngữ pháp) | ✅ Tất cả câu đã dịch đúng ngữ pháp |
| 3. Logical Clarity (rõ ràng logic) | ⚠️ P011-P012: "Annam/Tonkin" → "Trung Kỳ/Bắc Kỳ" làm mờ quan hệ thuộc địa |
| 4. Referential Accuracy (quy chiếu chính xác) | ✅ Đại từ *ông, nó, họ* đều rõ ràng |
| 5. Terminological Consistency (nhất quán thuật ngữ) | ✅ *chánh trị, dân tộc, độc lập* nhất quán |
| 6. Historical Accuracy (chính xác lịch sử) | ❌ P011-P012: Thay tên thuộc địa Pháp bằng tên Việt Nam làm sai bối cảnh |
| 7. Natural Vietnamese (tự nhiên) | ⚠️ *chấm dứt bởi* (MINOR-2) hơi cứng |
| 8. Conciseness (súc tích) | ✅ Không dài dòng, không lặp ý |

### 3.5. Kiểm tra các loại lỗi đặc biệt

| Loại lỗi | Phát hiện |
|---|---|
| Câu không rõ chủ ngữ | ✅ Không có |
| Câu có nhiều cách hiểu | ✅ Không có |
| Quan hệ nguyên nhân – kết quả bị đảo | ✅ Không có |
| Mệnh đề phụ gắn sai đối tượng | ✅ Không có |
| Đại từ không rõ đang chỉ ai | ✅ Không có |
| Câu đúng từng từ nhưng sai nghĩa toàn câu | ❌ P011-P012: "Annam/Tonkin" → "Trung Kỳ/Bắc Kỳ" |
| Câu dài nhưng không truyền đạt thông tin | ✅ Không có |
| Từ Hán Việt dùng sai nghĩa | ⚠️ *chấm dứt bởi* (MINOR-2) — *chấm dứt* dùng đúng nhưng cấu trúc bị động cứng |
| Cấu trúc tiếng Pháp/Anh bị bê nguyên | ✅ Không có |

---

## 4. Terminology Consistency

### 4.1. Thuật ngữ nhất quán trong pilot

| Thuật ngữ | Số lần dùng | Nhất quán? | Nguồn |
|---|---:|---|---|
| chánh trị | 6 | ✅ | SRC-001 (Lê Văn Đức, VERIFIED) |
| dân tộc | 4 | ✅ | (chưa có trong lexicon — xem §9) |
| độc lập | 3 | ✅ | SRC-002 (Lê Văn Đức, VERIFIED); SRC-023 (Hiến pháp, VERIFIED) |
| chủng tộc | 1 | ✅ | (chưa có trong lexicon — xem §9) |
| thuộc địa | 2 | ✅ | SRC-002 (Lê Văn Đức, VERIFIED) |
| triều đình | 2 | ✅ | SRC-001 (Lê Văn Đức, VERIFIED) |
| triều đại | 2 | ✅ | SRC-001 (Lê Văn Đức, VERIFIED) |
| quan lại | 3 | ✅ | SRC-001 (Lê Văn Đức, VERIFIED) |
| sĩ phu | 1 | ✅ | SRC-021 (Phan Khôi, CROSS_VERIFIED) |
| bảo hộ | 1 | ✅ | SRC-001 (Lê Văn Đức, VERIFIED) |
| Nam Kỳ | 2 | ✅ | (chưa có trong lexicon — xem §9) |
| Trung Kỳ | 2 | ⚠️ | (xem MAJOR-1: nên giữ *Annam* + giải nghĩa) |
| Bắc Kỳ | 2 | ⚠️ | (xem MAJOR-1: nên giữ *Tonkin* + giải nghĩa) |

### 4.2. Thuật ngữ chưa có trong lexicon (evidence gap)

6 thuật ngữ dùng trong pilot nhưng **không tìm thấy** trong MASTER_LEXICON.csv:

1. **dân tộc** — dùng 4 lần (P009, P010, P012). Thuật ngữ trung tâm của chương. Cần bổ sung vào lexicon với nguồn (Lê Văn Đức hoặc Hiến pháp VNCH).
2. **chủng raced** — dùng 1 lần (P009). Cần bổ sung.
3. **Nam Kỳ** — dùng 2 lần (P008, P011). Tên gọi vùng đất VNCH. Cần bổ sung.
4. **Trung Kỳ** — dùng 2 lần (P011, P012). Xem MAJOR-1.
5. **Bắc Kỳ** — dùng 2 lần (P011, P012). Xem MAJOR-1.
6. **mặt trận** — dùng 1 lần (P001). Xem MINOR-1.

### 4.3. Xác minh không dùng thuật ngữ OCR_PENDING

✅ **PASS**: Không có thuật ngữ nào từ 19 mục OCR_PENDING (Bách Khoa 405) được dùng trong pilot. Tất cả thuật ngữ trong pilot đều từ nguồn VERIFIED (Lê Văn Đức, Hiến pháp VNCH) hoặc chưa có trong lexicon.

### 4.4. Xác minh không lạm dụng thuật ngữ Hiến pháp 1967

✅ **PASS**: Các thuật ngữ chỉ xuất hiện trong Hiến pháp VNCH 1967 (như *dân biểu, nghị sĩ, chánh phủ, sắc luật*) **không** được áp đặt vào pilot. Pilot chỉ dùng *độc lập* (SRC-023) trong ngữ cảnh chung, không phải ngữ cảnh lập hiến VNCH. Điều này đúng với cảnh báo của người dùng: "32 mục VERIFIED từ Hiến pháp chỉ xác minh việc sử dụng trong văn kiện đó, không đồng nghĩa áp dụng phổ quát cho mọi thời kỳ."

---

## 5. Historical and Regional Language Review

### 5.1. Phân biệt 4 lớp ngôn ngữ

| Lớp | Định nghĩa | Trong pilot |
|---|---|---|
| Historical usage | Từ xuất hiện trong nguồn lịch sử | *triều đình, quan lại, sĩ phu, bảo hộ, thuộc địa* ✅ |
| Southern Vietnamese | Từ dùng ở Nam Bộ | *chánh trị, tuy vậy, đã vậy, e rằng, soi bóng, đầy ăm ắp* ✅ |
| VNCH institutional | Thuật ngữ thể chế VNCH | *không áp dụng trong pilot (đúng — pilot nói về thời thuộc địa, không phải VNCH)* ✅ |
| Contemporary | Từ hiện nay | *không dùng từ hiện đại áp đặt* ✅ |

### 5.2. Kiểm tra không hiện đại hóa

| Từ hiện nay | Có bị áp đặt vào pilot? |
|---|---|
| chính phủ | ✅ Không (không xuất hiện) |
| đại biểu | ✅ Không (không xuất hiện) |
| chính trị | ✅ Không (dùng *chánh trị*) |
| tài chính | ✅ Không (không xuất hiện) |
| bất động sản | ✅ Không (không xuất hiện) |
| lương hưu | ✅ Không (không xuất hiện) |

✅ **PASS**: Không có hiện đại hóa ngôn ngữ.

### 5.3. Kiểm tra không áp đặt miền Bắc

| Từ miền Bắc | Có xuất hiện? |
|---|---|
| đồng chí | ✅ Không |
| ta/địch (trong văn trung tính) | ✅ Không (chỉ trong trích Hồ Chí Minh) |
| giải phóng | ✅ Không |
| xâm lược (trong văn trung tính) | ✅ Không (dùng *chinh phục*) |

✅ **PASS**: Không có áp đặt miền Bắc.

### 5.4. Kiểm tra không đồng nhất VNCH với trước 1945

✅ **PASS**: Pilot nói về thời thuộc địa (1860s–1940s), không áp đặt thuật ngữ VNCH (1954–1975) vào ngữ cảnh này. Các từ như *dân biểu, nghị sĩ, chánh phủ* không xuất hiện trong pilot — đúng, vì chúng là thuật ngữ VNCH, không phải thuật ngữ thời thuộc địa.

### 5.5. Vấn đề tên gọi thuộc địa (Annam/Tonkin)

Đây là vấn đề **lịch sử quan trọng**:

- Nguyên tác dùng *Annam* và *Tonkin* (tên thuộc địa Pháp) để mô tả cách gọi của thực dân.
- Bản dịch thay bằng *Trung Kỳ* và *Bắc Kỳ* (tên Việt Nam).
- **Hệ quả**: Người đọc không còn thấy được sự phân biệt giữa tên gọi thực dân và tên gọi bản địa — một phân biệt quan trọng trong sử học.

**Đề xuất**: Giữ tên thuộc địa Pháp trong ngoặc đơn + tên Việt Nam trong ngoặc kép: *Annam (Trung Kỳ)* và *Tonkin (Bắc Kỳ)*.

### 5.6. Vấn đề "Trung Hoa" vs "Trung Quốc"

✅ **PASS**: Pilot dùng *Trung Hoa* (Nam Bộ/VNCH) thay vì *Trung Quốc* (Bắc/hiện nay). Đây là lựa chọn đúng theo chuẩn VNCH. Tuy nhiên, cần lưu ý: trong ngữ cảnh lịch sử (triều Minh), *Trung Hoa* có thể gây nhầm lẫn với *Trung Hoa Dân Quốc* (1912–1949). Cân nhắc dùng *Trung Quốc* khi nói về triều Minh (thời phong kiến), *Trung Hoa* khi nói về thời hiện đại.

---

## 6. Style Guide Deficiencies

Style Guide Phần B (14 quy tắc) đã bao quát tốt các khía cạnh: lựa chọn từ vựng, Nam Bộ, kinh tế, chính trị, địa lý, lịch sử, cú pháp, văn phong, thuật ngữ không tương đương, đa nghĩa, chú thích, không hiện đại hóa, phân biệt dịch/nguyên tác, cơ chế ghi nhận.

Tuy nhiên, phát hiện **5 khoảng trống** cần bổ sung:

### 6.1. Thiếu quy tắc xử lý tên thuộc địa Pháp

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Pilot P011-P012: *Annam, Tonkin* (tên thuộc địa Pháp) bị thay bằng *Trung Kỳ, Bắc Kỳ* (tên Việt Nam). Style Guide không có quy tắc xử lý các tên gọi thuộc địa trong nguyên tác. |
| **Đề xuất** | Thêm **Quy tắc 15: Xử lý tên gọi thuộc địa và địa danh ngoại quốc**. Khi nguyên tác dùng tên gọi thuộc địa Pháp (Annam, Tonkin, Cochinchine, Đông Dương), giữ nguyên tên gốc + giải nghĩa Việt Nam trong ngoặc: *Annam (Trung Kỳ)*. Không thay thế bằng tên Việt Nam một cách đơn phương vì làm mất ngữ cảnh lịch sử. |
| **Mức độ ưu tiên** | HIGH |

### 6.2. Thiếu quy tắc về từ không có tương đương (polymath)

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Pilot P011: *polymath* → *học giả lỗi lạc* (mất nghĩa "bác học toàn diện"). Style Guide Quy tắc 9 đã có nhưng chưa đủ chi tiết cho các từ như *polymath*. |
| **Đề xuất** | Bổ sung vào Quy tắc 9: liệt kê các từ Anh/Pháp thường gặp trong sử học (polymath, intellectual, scholar, expert) + dạng tiếng Việt tương ứng (*nhà bác học, trí thức, học giả, chuyên gia*) + nguồn. |
| **Mức độ ưu tiên** | MEDIUM |

### 6.3. Thiếu quy tắc kiểm tra hoàn tất đoạn

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Pilot P012 bị cắt giữa đoạn ("Thuật ngữ này —"). Style Guide không có quy tắc kiểm tra hoàn tất. |
| **Đề xuất** | Thêm **Quy tắc 16: Kiểm tra hoàn tất bản dịch**. Sau khi dịch xong một đoạn, đối chiếu số câu trong nguyên tác và bản dịch. Không để câu bỏ lửng. Mỗi đoạn dịch phải kết thúc ở dấu chấm hết, không ở dấu gạch ngang giữa câu. |
| **Mức độ ưu tiên** | HIGH |

### 6.4. Thiếu quy tắc dịch thuật methodology (quy trình dịch)

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Style Guide có quy tắc về *thuật ngữ* và *văn phong*, nhưng không có quy tắc về *quy trình dịch* (phân tích cấu trúc câu, xác định chủ thể/vị ngữ, chuyển sang tiếng Việt tự nhiên, đọc lại độc lập, đối chiếu ngược). |
| **Đề xuất** | Thêm **Quy tắc 17: Quy trình dịch thuật 7 bước**: (1) Đọc toàn bộ đoạn nguyên tác, hiểu nghĩa tổng thể; (2) Xác định chủ thể, vị ngữ, đối tượng chính; (3) Xác định quan hệ logic giữa các mệnh đề (nhân quả, tương phản, điều kiện); (4) Xác định thuật ngữ chuyên ngành cần tra cứu; (5) Dịch sang tiếng Việt tự nhiên (không dịch từng chữ); (6) Đọc lại bản dịch không nhìn nguyên tác, kiểm tra có hiểu được không; (7) Đối chiếu ngược với nguyên tác, sửa sai lệch. |
| **Mức độ ưu tiên** | HIGH |

### 6.5. Thiếu quy tắc cụ thể cho "united front" và các thuật ngữ chính trị tiếng Anh

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Pilot P001: *united front* → *mặt trận hợp nhất* (nên dùng *mặt trận thống nhất*). Style Guide không có danh sách các thuật ngữ chính trị Anh-Việt. |
| **Đề xuất** | Bổ sung bảng thuật ngữ Anh-Việt cho các từ chính trị thường gặp: *united front* → *mặt trận thống nhất*, *coalition* → *liên minh*, *sovereignty* → *chủ quyền*, *protectorate* → *bảo hộ*, *independence* → *độc lập*. |
| **Mức độ ưu tiên** | MEDIUM |

---

## 7. Proposed Corrections

### 7.1. Sửa bản dịch (v1_ch01_vi.txt)

| # | Đoạn | Loại | Sửa đổi | Lý do |
|---|---|---|---|---|
| 1 | P001 | MINOR | *mặt trận hợp nhất* → *mặt trận thống nhất* | "thống nhất" VERIFIED (SRC-023); "hợp nhất" không có nguồn |
| 2 | P010 | MINOR | *chấm dứt bởi* → *đã chấm dứt khi* (chủ động) | Tiếng Việt ưa chủ động |
| 3 | P011 | MAJOR | *Gọi là Trung Kỳ và Bắc Kỳ* → *Gọi là Annam (Trung Kỳ) và Tonkin (Bắc Kỳ)* | Giữ tên thuộc địa Pháp (nguyên tác) |
| 4 | P011 | MINOR | *học giả... lỗi lạc* → *nhà bác học* | *polymath* = *nhà bác học*, không phải *học giả lỗi lạc* |
| 5 | P012 | MAJOR | *tại Trung Kỳ và Bắc Kỳ* → *tại Annam (Trung Kỳ) và Tonkin (Bắc Kỳ)* | Cùng lý do #3 |
| 6 | P012 | CRITICAL | Hoàn tất đoạn: thêm 3 câu về nghĩa "ái quốc" + Nguyễn Ái Quốc | Bản dịch chưa hoàn tất |

### 7.2. Hoàn thiện tệp nguồn (v1_ch01_src.txt)

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Tệp `v1_ch01_src.txt` chỉ chứa P001–P007, thiếu P008–P012. |
| **Đề xuất** | Bổ sung P008–P012 (nguyên tác tiếng Anh từ `02_extracted_text/v1/ch01.txt` dòng 83–166) vào `v1_ch01_src.txt`. |
| **Lý do** | Tệp nguồn phải đầy đủ để đối chiếu. Thiếu 5 đoạn = không thể kiểm định. |

### 7.3. Bổ sung Style Guide

| # | Bổ sung | Mức độ |
|---|---|---|
| 1 | Quy tắc 15: Xử lý tên gọi thuộc địa và địa danh ngoại quốc | HIGH |
| 2 | Quy tắc 16: Kiểm tra hoàn tất bản dịch | HIGH |
| 3 | Quy tắc 17: Quy trình dịch thuật 7 bước | HIGH |
| 4 | Bổ sung Quy tắc 9: danh sách từ Anh/Pháp thường gặp | MEDIUM |
| 5 | Bảng thuật ngữ chính trị Anh-Việt | MEDIUM |

---

## 8. Unresolved Decisions

Các quyết định cần người dùng phê duyệt (không tự động quyết định):

| # | Vấn đề | Lựa chọn | Ảnh hưởng |
|---|---|---|---|
| 1 | **Chánh / Chính** | (A) Dùng *chánh* xuyên suốt (chánh trị, chánh phủ); (B) Dùng theo ngữ cảnh lịch sử | Ảnh hưởng toàn bộ 77 chương |
| 2 | **Nam Kỳ / An Nam** | (A) Cochinchina = Nam Kỳ (VNCH); (B) Giữ *Annam* + giải nghĩa | Ảnh hưởng P008, P011, P012 |
| 3 | **Dân biểu / Đại biểu** | (A) Dân biểu cho Hạ nghị viện VNCH; (B) Theo ngữ cảnh | Ảnh hưởng các chương về chính trị VNCH |
| 4 | **Tiếng Pháp trong ngoặc** | (A) Giữ khi cần xác định; (B) Bỏ tràn lan | Ảnh hưởng cách xử lý tên riêng |
| 5 | **Viết hoa chức danh** | (A) Theo quy chuẩn biên tập; (B) Viết hoa mọi chức danh | Ảnh hưởng toàn bộ |
| 6 | **Trung Hoa vs Trung Quốc** | (A) *Trung Hoa* cho VNCH; *Trung Quốc* cho phong kiến; (B) *Trung Hoa* xuyên suốt | Ảnh hưởng P001, P010, P011 |
| 7 | **V1 / V3 priority** | (A) Hoàn thiện V1 trước; (B) V3 trước | Ảnh hưởng thứ tự dịch |
| 8 | **Mô hình thực thi** | (A) Một dịch giả + một phản biện; (B) Nhóm | Ảnh hưởng tổ chức công việc |

---

## 9. Evidence Gaps

### 9.1. Thuật ngữ chưa có trong lexicon

6 thuật ngữ dùng trong pilot nhưng không có mục trong MASTER_LEXICON.csv:

| Thuật ngữ | Số lần dùng | Nguồn đề xuất | Mức độ ưu tiên |
|---|---:|---|---|
| dân tộc | 4 | Lê Văn Đức 1970 hoặc Hiến pháp VNCH 1967 | HIGH |
| chủng raced | 1 | Lê Văn Đức 1970 | MEDIUM |
| Nam Kỳ | 2 | Lê Văn Đức 1970 hoặc Bách Khoa 405 | HIGH |
| Trung Kỳ | 2 | Lê Văn Đức 1970 | HIGH |
| Bắc Kỳ | 2 | Lê Văn Đức 1970 | HIGH |
| mặt trận | 1 | Lê Văn Đức 1970 hoặc Phan Khôi 1932 | MEDIUM |

### 9.2. Tệp nguồn không đầy đủ

- `v1_ch01_src.txt` chỉ có P001–P007 (7 đoạn).
- Bản dịch có P001–P012 (12 đoạn).
- **Thiếu 5 đoạn nguyên tác (P008–P012)** trong tệp nguồn.

### 9.3. Historical usage layers chưa đủ

Theo `HISTORICAL_USAGE_TRACKING.md`, 8 thuật ngữ được theo dõi qua 8 lớp, nhưng:
- Lớp 4 (tài liệu chuyên ngành VNCH) cho hầu hết thuật ngữ = NOT_YET_RESEARCHED.
- Lớp 5 (dùng hiện nay) = NOT_YET_RESEARCHED.
- Lớp 7 (thay đổi nghĩa theo thời kỳ) = NOT_YET_RESEARCHED.
- Lớp 8 (khác biệt vùng miền) = NOT_YET_RESEARCHED.

### 9.4. OCR_PENDING chưa xác minh

19 mục từ Bách Khoa 405 (SRC-009) có trạng thái OCR_PENDING. Không được dùng làm thuật ngữ đã xác minh. Không có mục nào trong số này được dùng trong pilot (xác nhận tích cực).

---

## 10. Final Recommendation

### 10.1. Kết luận

**PILOT_V1_CH1: NEEDS_REVISION**

**STYLE_GUIDE_B: NEEDS_REVISION**

### 10.2. Điều kiện PASS

Pilot và Style Guide chỉ đạt PASS khi:

- [ ] **CRITICAL-1 đã sửa**: P012 hoàn tất (thêm 3 câu về nghĩa "ái quốc" + Nguyễn Ái Quốc).
- [ ] **MAJOR-1 đã sửa**: P011 và P012 dùng *Annam (Trung Kỳ)* và *Tonkin (Bắc Kỳ)* thay vì chỉ *Trung Kỳ/Bắc Kỳ*.
- [ ] **Tệp nguồn hoàn tất**: `v1_ch01_src.txt` bổ sung P008–P012.
- [ ] **6 thuật ngữ có lexicon entries**: *dân tộc, chủng raced, Nam Kỳ, Trung Kỳ, Bắc Kỳ, mặt trận* được bổ sung vào MASTER_LEXICON.csv với nguồn.
- [ ] **Style Guide bổ sung 3 quy tắc**: Quy tắc 15 (tên thuộc địa), Quy tắc 16 (kiểm tra hoàn tất), Quy tắc 17 (quy trình dịch).
- [ ] **Không còn lỗi MAJOR chưa xử lý**.
- [ ] **Không có câu dịch sai nghĩa**.
- [ ] **Không có thuật ngữ không rõ nguồn gốc dùng như thuật ngữ chuẩn**.
- [ ] **Không có vấn đề quy chiếu/logic khiến người đọc hiểu sai**.

### 10.3. Các quyết định còn tranh luận (ghi nhận riêng)

8 quyết định trong §8 cần người dùng phê duyệt trực tiếp. Không tự động quyết định.

### 10.4. Khuyến nghị tiếp theo

1. Người dùng xem xét 8 quyết định trong §8 và đưa ra lựa chọn.
2. Dịch giả sửa 6 lỗi trong §7.1 (1 CRITICAL, 2 MAJOR, 3 MINOR).
3. Bổ sung P008–P012 vào `v1_ch01_src.txt`.
4. Bổ sung 6 thuật ngữ vào MASTER_LEXICON.csv.
5. Cập nhật Style Guide với 3 quy tắc mới.
6. Chạy lại Quality Gate.
7. **CHỈ SAU KHI PASS** mới chuyển 77_CHAPTER_TRANSLATION thành AUTHORIZED.

### 10.5. Nguyên tắc

Tuân thủ quan điểm của người dùng: **ưu tiên xây dựng hệ thống dịch thuật có khả năng diễn đạt tiếng Việt chính xác, sáng rõ và có chiều sâu lịch sử, thay vì chạy theo số lượng chương đã dịch**. Nếu 12 đoạn pilot chưa đạt chất lượng thì phải sửa phương pháp trước, không mở rộng quy mô.

---

## Phụ lục: Danh sách thuật ngữ pilot + nguồn

| Thuật ngữ | Nguồn | Mức độ xác minh | Lexicon? |
|---|---|---|---|
| chánh trị | SRC-001 (Lê Văn Đức Quý Thượng) | VERIFIED | ✅ Có |
| độc lập | SRC-002 (Lê Văn Đức Quý Hạ); SRC-023 (Hiến pháp 1967) | VERIFIED | ✅ Có |
| thuộc địa | SRC-002 (Lê Văn Đức Quý Hạ) | VERIFIED | ✅ Có |
| triều đình | SRC-001 (Lê Văn Đức Quý Thượng) | VERIFIED | ✅ Có |
| triều đại | SRC-001 (Lê Văn Đức Quý Thượng) | VERIFIED | ✅ Có |
| quan lại | SRC-001 (Lê Văn Đức Quý Thượng) | VERIFIED | ✅ Có |
| sĩ phu | SRC-021 (Phan Khôi 1932) | CROSS_VERIFIED | ✅ Có |
| bảo hộ | SRC-001 (Lê Văn Đức Quý Thượng) | VERIFIED | ✅ Có |
| thực dân | SRC-002 (Lê Văn Đức Quý Hạ) | VERIFIED | ✅ Có |
| thống nhất | SRC-023 (Hiến pháp 1967, Điều 1) | VERIFIED | ✅ Có |
| dân tộc | (chưa tra cứu) | CHƯA XÁC MINH | ❌ Không |
| chủng tộc | (chưa tra cứu) | CHƯA XÁC MINH | ❌ Không |
| Nam Kỳ | (chưa tra cứu) | CHƯA XÁC MINH | ❌ Không |
| Trung Kỳ | (chưa tra cứu) | CHƯA XÁC MINH | ❌ Không |
| Bắc Kỳ | (chưa tra cứu) | CHƯA XÁC MINH | ❌ Không |
| mặt trận | (chưa tra cứu) | CHƯA XÁC MINH | ❌ Không |

---

*Hết báo cáo Final Quality Gate — V1-Ch1 & Style Guide B.*