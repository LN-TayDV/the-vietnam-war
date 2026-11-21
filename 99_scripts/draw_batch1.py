#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dich Batch 1: P001-P012 (trang 27-31) cho Chương 1.
Ap dung 7 buoc Grammar Engine + Style Guide Phan B (VNCH pre-1975).
UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

# Header
lines = []
lines.append("===== V1-C01 · Trí nhớ, Truyền thống và Sử học về \"Việt Nam\" · Liam C. Kelley =====")
lines.append("Nguồn: 02_extracted_text/v1/ch01.txt · PDF 43-59 · trang in 27-43")
lines.append("")

# P001 (trang 27)
lines.append("--- [V1C01-P001] (trang 27) ---")
lines.append("Ngày 1 tháng 2 năm 1942, nhà cách mạng Hồ Chí Minh đăng một bài ngắn mang nhan đề \"Nên học sử ta\" (Our History Must be Studied). Bài viết xuất trên tờ báo mà năm trước Ông ấy đã thành lập, lấy tên là Việt Nam độc lập (Independent Vietnam). Tờ báo ấy xuất bản tại tỉnh miền Bắc Cao Bằng, nơi Hồ Chí Minh từng ở một thời gian vào những năm 1941 và 1942, sau khi vượt biên từ miền Nam Trung Hoa để tổ chức mặt trận thống nhất chống cai trị của Pháp và cuộc chiếm đóng của Nhật Bản, gọi là Việt Minh. Ra ba kỳ một tháng với số phát hành 400 bản, tầm ảnh hưởng của Việt Nam độc lập có lẽ khá hạn chế. Dầu vậy, cách diễn giải quá khứ mà Hồ Chí Minh trình bày trong bài viết ngắn ngủi này đã được nhắc lại vô số lần trong ba mươi năm cách mạng và chiến tranh từ 1945 đến 1975, và cho đến ngày nầy vẫn là một yếu tố then chốt trong chủ nghĩa dân tộc và bản sắc của người Việt. [1]")
lines.append("")

# P002 (trang 27)
lines.append("--- [V1C01-P002] (trang 27) ---")
lines.append("Cốt lõi trong cái nhìn của Hồ Chí Minh về lịch sử Việt Nam được tóm gọn trong hai câu xuất hiện ở cuối bài: \"Khi nào dân ta đoàn kết một lòng, nước ta được độc lập và tự do. Trái lại, khi nào dân ta không đoàn kết, ta bị các nước ngoài xâm lăng.\" Cùng số báo đó của Việt Nam độc lập có một danh sách \"Mười điều nên\" (10 Điều nên) do chính Hồ Chí Minh viết ra. Đây là mười việc mà Hồ Chí Minh tuyên bố các thành viên Việt Minh phải thực hiện: phải bảo mật về Việt Minh, phải trung thành trọn vẹn với Việt Minh, phải phổ biến mục đích của Việt Minh, phải hết sức tìm thành viên mới cho Việt Minh, phải hết sức làm việc cho Việt Minh, phải đóng phí đúng hạn, phải giúp đỡ lẫn nhau, phải nỗ lực học tập, phải đọc sách và báo của Việt Minh, và phải ủng hộ tờ báo của Việt Minh. [2] [3]")
lines.append("")

# P003 (trang 27-28)
lines.append("--- [V1C01-P003] (trang 27-28) ---")
lines.append("Dầu Hồ Chí Minh lập luận vào năm 1942 rằng bài học cốt yếu rút ra từ quá khứ Việt Nam là người Việt cần đoàn kết để bảo vệ nền độc lập của nước, ngày nay ta có thể thấy điều mà Ông ấy tìm cách hợp nhất trên tờ Việt Nam độc lập năm 1942 chính là sử học và chánh trị cách mạng. Dẫu có người cho rằng mọi văn bản sử học về Việt Nam xưa nay vốn mang tính chánh trị, thì các tác phẩm trước đó đã phụng vụ các loại chánh trị khác, chẳng hạn chánh trị triều đình, rồi sau đó là chánh trị thuộc địa. Bởi thế, thuật lại câu chuyện về sự ra đời của tri thức sử học về Việt Nam, như tôi sẽ làm trong bài này, cũng chính là thuật lại lịch sử chánh trị của Việt Nam, và hai tiến trình này phản chiếu lẫn nhau một cách khít khắp.")
lines.append("")

# P004 (trang 28)
lines.append("--- [V1C01-P004] (trang 28) ---")
lines.append("Đã vậy, mục tiêu của bài này không chỉ đơn thuần là chỉ ra các văn bản sử học về Việt Nam đã chịu ảnh hưởng của chánh trị ra sao. Trái lại, mục đích của bài cung cấp một nền sử liệu để độc giả có thể hiểu rõ hơn các bài trong cuốn Cambridge History of the Vietnam War này. Trong những chương sau đây có nhiều ý tưởng về lịch sử Việt Nam là mới. Chúng mới không chỉ vì các học giả đã nghiên cứu điều mới và có những phát hiện mới, mà cũng vì đã có một chuyển hướng rời xa những \"chân lý\" trước kia từng thống trị các tác phẩm về lịch sử Việt Nam. Trong bài này, chúng ta sẽ xem xét những \"chân lý\" ấy từ đâu mà ra, và bằng cách nào chúng đã được các học giả viết bằng tiếng Anh tiếp nhận.")
lines.append("")

# P005 (trang 28) - Heading
lines.append("--- [V1C01-P005] (trang 28) — đề mục ---")
lines.append("From Traditional to Modern Histories")
lines.append("")

# P006 (trang 28-29)
lines.append("--- [V1C01-P006] (trang 28-29) ---")
lines.append("Những tác phẩm sử đầu tiên do người Việt soạn đều là sử triều đình. Hai bộ quan trọng nhất viết trước năm 1900 là Complete Book of the Historical Records of Dai Viet (Đại Việt sử ký toàn thư; sau đây gọi tắt là Toàn thư) thế kỷ mười lăm và Imperially Commissioned Itemized Summaries of the Comprehensive Mirror of Viet History (Khâm định Việt sử thông giám cương mục; sau đây gọi tắt là Cương mục) thế kỷ mười chín. Các tác phẩm này soạn bằng chữ Hán cổ, một ngôn ngữ chỉ một phần nhỏ dân số có thể hiểu. Mỗi bộ đều đưa ra những ví dụ lịch sử về chánh trị tốt và xấu, trong hy vọng các quan lại đương triều sẽ học hỏi từ quá khứ.")
lines.append("")

# P007 (trang 29)
lines.append("--- [V1C01-P007] (trang 29) ---")
lines.append("Cho đến thế kỷ mười chín, lịch sử Việt Nam do đó là một chủ đề phần lớn chỉ giới hạn trong giới quan lại triều đình và tầng lớp sĩ phu biết chữ rất nhỏ mong muốn vào làm quan. Tuy một số giáo sĩ và du khách phương Tây có học được một vài điều từ những người bản xứ mà họ tiếp xúc, nhưng muốn tiếp cận trực tiếp các văn bản sử thì lại là chuyện khó.")
lines.append("")

# P008 (trang 29)
lines.append("--- [V1C01-P008] (trang 29) ---")
lines.append("Tình hình ấy đã thay đổi, dầu vậy, cùng với cuộc chinh phục Việt Nam của Pháp. Việc Pháp mở rộng quyền kiểm soát trên Việt Nam là một tiến trình kéo dài hàng thập niên, nhưng khởi đầu bằng những hiệp ước trong thập niên 1860, theo đó triều Nguyễn phân nhượng cho Pháp quyền kiểm soát trực tiếp phần ba phía Nam Việt Nam, hoặc cái mà họ gọi là Cochinchine (Cochinchina). Trong thời kỳ nầy, một giáo sĩ Pháp tên là Théophile Marie Legrand de la Liraye đã viết cuốn sách sử về Việt Nam đầu tiên bằng tiếng Pháp. Công trình nầy tuy dựa trên các nguồn sử học Việt, song đã khởi đầu một quá trình \"phương Tây hóa\" của sử học Việt Nam, vì Legrand de la Liraye đã dùng các khái niệm của Châu Âu để giải thích quá khứ.")
lines.append("")

# P009 (trang 29-30)
lines.append("--- [V1C01-P009] (trang 29-30) ---")
lines.append("Trong khi Toàn thư và Cương mục chép một phả hệ chánh trị từ nhà cai trị nầy sang nhà cai trị kia, mục đích của công trình Legrand de la Liraye là giáo dục độc giả về lịch sử của một dân tộc, hay cái mà ông gọi là \"Annamite nation\" (dân tộc Annam). Để làm điều nầy, Legrand de la Liraye đã cố xác định chủng tộc Annamites thuộc chủng tộc nào, để độc giả Châu Âu của ông có thể hiểu những người nầy là ai trong liên hệ với các nhóm chủng tộc khác trong khu vực. Hai khái niệm dân tộc và chủng tộc nầy là các khái niệm của phương Tây, và trước đây chưa từng được áp dụng cho lịch sử Việt Nam. [4]")
lines.append("")

# P010 (trang 30)
lines.append("--- [V1C01-P010] (trang 30) ---")
lines.append("Một ý tưởng quan trọng khác mà Legrand de la Liraye đưa vào việc viết sử lịch sử Việt Nam là khái niệm \"độc lập\". Có một thời kỳ vào đầu thế kỷ mười lăm khi triều Minh của Trung Hoa kiểm soát các vùng bây giờ là miền Bắc và Bắc Trung Bộ Việt Nam. Thời kỳ ngắn ngủi nầy bị chấm dứt bởi một người tên là Lê Lợi, vị vua sáng lập triều Lê. Toàn thư đơn giản chép rằng Lê Lợi đã \"tước bình Minh tặc\" (削平明賊). Trái lại, Legrand de la Liraye mô tả sự kiện lịch sử tương tự nầy như một \"cuộc chiến giành độc lập\" (guerre de l'indépendance). Đây là một khái niệm mới khác. Do đó, khi Hồ Chí Minh tuyên bố vào năm 1942 rằng lịch sử Việt Nam là một câu chuyện bất diệt về người Việt Nam (dân tộc) đoàn kết để bảo vệ nền độc lập (độc lập) và tự do (tự do) của nước, thì cách diễn giải quá khứ của Ông ấy đầy đặn những từ ngữ và khái niệm mà tổ tiên Ông ấy sẽ không hiểu được. Sở dĩ Hồ Chí Minh hiểu được những từ ngữ và khái niệm nầy là vì tất cả đã trở thành một phần trong thế giới quan của người Việt trong những năm cai trị thuộc địa của Pháp.")
lines.append("")

# P011 (trang 30-31)
lines.append("--- [V1C01-P011] (trang 30-31) ---")
lines.append("Những ý tưởng nầy được tiếp nhận trước tiên ở Nam Kỳ. Tại nầy, người Pháp thiết lập một hệ thống giáo dục mới, và vào năm 1875, Trương Vĩnh Ký, một nhà bác học Công giáo Việt Nam, đã soạn một cuốn sách sử về Việt Nam bằng tiếng Pháp cho học sinh Việt Nam tại nầy. Đến năm 1906, một bản dịch tiếng Việt của một cuốn sách sử về Việt Nam bằng tiếng Pháp tương tự được xuất bản ở Nam Kỳ, mang tên Đại Nam quốc lược sử. Trong cùng năm nầy, các cải cách giáo dục được thực hiện ở trung tâm và miền Bắc Việt Nam nhằm hiện đại hóa chương trình học cho các kỳ thi khoa cử truyền thống. Và vào cuối thế kỷ mười chín, cả trung tâm và miền Bắc Việt Nam đều đã trở thành các xứ bảo hộ của Pháp. Gọi là Annam và Tonkin, lần lượt, các xứ nầy vẫn được cai trị bởi các quan lại triều Nguyễn, tuy dưới sự hướng dẫn của các cố vấn Pháp. Thành thạo chữ Hán cổ, một số quan lại trong số họ đã học được rất nhiều về phương Tây tại thời điểm nầy thông qua các tác phẩm của các trí thức cải cách Trung Hoa, và họ đã biến đổi chương trình giáo dục theo các ý tưởng mới nầy.")
lines.append("")

# P012 (trang 30-31)
lines.append("--- [V1C01-P012] (trang 30-31) ---")
lines.append("Một ví dụ rõ ràng về điều nầy là một công trình được soạn vào năm 1906 và được dùng trong chương trình cải cách ở Annam và Tonkin bởi một học giả tên là Hoàng Đạo Thành có nhan đề Complete Compilation of the New Convention of Việt History (Việt sử tân ước toàn biên). Văn bản của Hoàng Đạo Thành là cuốn sử đầu tiên do người Việt soạn có cấu trúc xoay quanh khái niệm dân tộc. Nó nhắm rõ ràng vào việc gieo trong độc giả một cảm xúc tự hào về dân tộc. Trong khi Toàn thư và Cương mục được thiết kế để dạy các quan hàm hành chính về chánh trị thẳng thắn và nhu cầu trung thành (trung) với vua, sử học của Hoàng Đạo Thành được thiết kế để dạy học sinh được yêu nước (ái quốc). Thuật ngữ nầy về nghĩa đen có nghĩa là \"yêu nước\". Đây là một khái niệm phương Tây được đưa vào giới học giả Việt Nam thông qua các tác phẩm của các trí thức cải cách Trung Hoa, và đây cũng là từ mà Hồ Chí Minh lấy làm một phần trong tên cách mạng của Ông ấy, Nguyễn Ái Quốc, không lâu sau khi Hoàng Đạo Thành ra đời công trình sử mới về quá khứ Việt Nam.")
lines.append("")

content = "\n".join(lines) + "\n"
content = unicodedata.normalize("NFC", content)
VI.write_text(content, encoding="utf-8", newline="\n")
print(f"Da viet Batch 1 (P001-P012) vao {VI}: {len(lines)} dong")
