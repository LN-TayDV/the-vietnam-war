#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dich Batch 2: P013-P024 (trang 31-35) cho Chương 1.
Ap dung 7 buoc Grammar Engine + Style Guide Phan B (VNCH pre-1975).
UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

lines = []

# P013 (trang 31)
lines.append("--- [V1C01-P013] (trang 31) ---")
lines.append("Dầu sử học của Hoàng Đạo Thành là một công trình tiên phong, nó được viết vào thời điểm chữ Hán cổ bắt đầu mất đi vị thế ưu việt tại Việt Nam.")
lines.append("")

# P014 (trang 31-32)
lines.append("--- [V1C01-P014] (trang 31-32) ---")
lines.append("Vào năm 1909, các quan chức thuộc địa Charles Maybon và Henri Russier đã soạn một công trình sử lịch sử Việt Nam mới bằng tiếng Pháp cho chương trình thi khoa cử đã được cải cách. Có nhan đề Notions d'histoire d'Annam (Một số ý kiến về lịch sử Annam), công trình nầy cố ý trình bày lịch sử theo \"phương pháp Châu Âu\" để giải thích quá khứ và tầm quan trọng của nó, chứ không tuân theo \"mô hình Trung Hoa\" trong việc chép lại sự kiện mà họ phán xét. Họ cũng tìm cách gieo trong độc giả Việt Nam một lòng biết ơn đối với người Pháp, thay vì niềm tự hào dân tộc. Dầu họ thừa nhận rằng trong quá khứ đã có một \"khuynh hướng hướng về thống nhất\", họ vẫn lập luận rằng nền thống nhất và độc lập chân chính chỉ tới vào thế kỷ mười chín, khi người Pháp giúp Gia Long, vị hoàng đế đầu tiên của triều Nguyễn, thiết lập quyền cai trị trên toàn cõi Việt Nam, và khi người Pháp buộc triều Thanh phải chấm dứt địa vị chư hầu của Việt Nam.")
lines.append("")

# P015 (trang 32)
lines.append("--- [V1C01-P015] (trang 32) ---")
lines.append("Cái nhìn về quá khứ nầy đầy rẫy mâu thuẫn, nhưng cái nhìn ấy là chuẩn mực từ thập niên 1910 cho đến thập niên 1930. Dầu các kỳ thi khoa cử đã bị bãi bỏ vào năm 1919, một hệ thống trường Pháp–An Nam với giảng dạy bằng tiếng Việt và tiếng Pháp đã được thành lập vào thời điểm nầy, và một phiên bản cập nhật của sử học Maybon và Russier vẫn tiếp tục được dùng trong chương trình học của các trường ấy. Cũng được ưa chuộng là một cách thuật lại quá khứ mang tính bảo thủ của học giả Việt Nam Trần Trọng Kim, An Outline of the History of Vietnam (Việt Nam sử lược).")
lines.append("")

# P016 (trang 32)
lines.append("--- [V1C01-P016] (trang 32) ---")
lines.append("Có thể lập luận rằng vào thập niên 1930 có một mức độ chững lặp nhất định trong kiến thức về quá khứ Việt Nam. Sự chững lặp tri thức ấy là hình ảnh phản chiếu của sự ổn định đã được thiết lập tại Việt Nam thuộc địa và được chống đỡ bởi những cá nhân, cả Việt lẫn Pháp, những người duy trì trật tự thuộc địa. Tuy nhiên, vào thập niên 1940, trật tự thuộc địa ấy đã bị thách thức, và khi điều nầy xảy ra, tri thức sử học Việt Nam đã hồi sinh.")
lines.append("")

# P017 (trang 32) - Heading
lines.append("--- [V1C01-P017] (trang 32) — đề mục ---")
lines.append("Historical Writings of the 1940s")
lines.append("")

# P018 (trang 32)
lines.append("--- [V1C01-P018] (trang 32) ---")
lines.append("Vào mùa hè năm 1940, nước Pháp bị nước Đức Nazi chiếm đóng và một chính phủ cộng tác với Đức, được gọi là Pháp Vichy, đã được thành lập. Người Nhật đã tận dụng sự biến đổi chính trị nầy để đưa quân vào Đông Dương thuộc Pháp nhằm ngăn chặn nguồn tiếp tế chiến dịch đi tới Trung Hoa Dân Quốc qua đường sắt Hà Nội–Côn Mênh, cũng như để chuẩn bị cho việc chiếm đóng phần còn lại của Đông Nam Á sau nầy. Dầu các quan chức Vichy cho phép điều nầy thực chất trở thành một cuộc chiếm đóng quân sự của Nhật, họ vẫn tìm cách đối phó với tuyên truyền chiến tranh của Nhật kêu gọi người Châu Á đoàn kết chống lại phương Tây. Các quan chức thuộc địa Pháp Vichy đã làm điều nầy bằng cách cổ vũ chủ nghĩa dân tộc Việt Nam.")
lines.append("")

# P019 (trang 32-33)
lines.append("--- [V1C01-P019] (trang 32-33) ---")
lines.append("Một số trí thức Việt Nam đã nắm lấy cơ hội nầy để bày tỏ những ý tưởng trước đây bị cấm đoán. Về mặt sử học, một tờ tạp chí gọi là Trí Tân (New Knowledge) đã được thành lập vào năm 1941, và trong hơn 200 số được xuất bản trong bốn năm tiếp theo, các nhà văn đã bước đi những bước đầu tiên nhằm đưa tri thức sử học ra khỏi các khuôn mẫu mà nó đã rơi vào trong những thập niên trước. Trong số đầu tiên, ví dụ, Ứng Hòe Nguyễn Văn Tố, một nhà nghiên cứu tại École Française d'Extrême-Orient (EFEO), một viện nghiên cứu do người Pháp thành lập vào đầu thế kỷ hai mươi, đã viết một bài khuyến khích mọi người không dùng từ \"Annam\" để chỉ quốc gia. Ông ấy đã đưa ra bằng chứng sử học để lập luận rằng đây là một từ mà người Trung Hoa đã tạo ra cho Việt Nam khi nước nầy dưới sự kiểm soát của họ và rằng nó có hàm ý phục tùng. Thay vì dùng từ \"Annam,\" Nguyễn Văn Tố lập luận rằng từ lịch sử có ý nghĩa nhất để dùng là \"Đại Nam,\" nghĩa là \"Miền Nam Lớn,\" một tên mà hoàng đế Minh Mạng của triều Nguyễn đã chính thức đưa vào năm 1838.")
lines.append("")

# P020 (trang 33)
lines.append("--- [V1C01-P020] (trang 33) ---")
lines.append("Việc Nguyễn Văn Tố không gợi ý dùng từ \"Việt Nam\" cho thấy các ý tưởng về quốc gia và quá khứ của ông vẫn còn chưa rõ rệt vào thời điểm nầy. Trong bối cảnh nầy, Hồ Chí Minh đã viết lại bài \"Our History Must be Studied\" vào năm sau. Ông ấy cũng đã viết và xuất bản một bài thơ vào thời điểm nầy mang tên \"Lịch sử nước ta\" (The History of Our Country) tóm tắt các sự kiện chính trong hai thiên niên kỷ trước. Giống như trong bài viết, Hồ Chí Minh nhấn mạnh tầm quan trọng của sự đoàn kết và kết thúc bài thơ bằng lời kêu gọi mọi người đoàn kết dưới cờ Việt Minh. Nói cách khác, Hồ Chí Minh đã cố gắng xác định một yếu tố then chốt của quá khứ – sự đoàn kết – và tuyên bố rằng Việt Minh có sứ mệnh để thực hiện mục tiêu ấy (Hình 1.1).")
lines.append("")

# P021 (trang 33)
lines.append("--- [V1C01-P021] (trang 33) ---")
lines.append("Bản diễn giải mới về quá khứ nầy là một điều mà nhiều người Việt Nam khác cũng chia sẻ. Tuy nhiên, không phải tất cả đồng ý với Hồ Chí Minh về nhu cầu phải đoàn kết dưới cờ Việt Minh. Vào tháng Ba năm 1945, người Nhật đã nắm quyền kiểm soát toàn bộ Đông Dương thuộc Pháp bằng cách giam các quan chức Vichy và ra lệnh cho Hoàng đế Bảo Đại của triều Nguyễn tuyên bố độc lập cho Việt Nam. Một chính phủ đã được thành lập nhanh chóng với nhà sử học Trần Trọng Kim giữ chức thủ tướng. Dầu sử học của chính Trần Trọng Kim mang cách tiếp cận bảo thủ, một người tên là Nguyễn Duy Phương đã nhanh chóng soạn một cuốn sách sử về Việt Nam mới để đánh dấu việc thành lập chính phủ nầy và sự độc lập danh nghĩa của đất nước. Có nhan đề The History of the Independence of Vietnam, Nguyễn Duy Phương đã cố gắng đặt chính phủ Trần Trọng Kim ở cuối một dây dài các cuộc đấu tranh giành độc lập trong lịch sử. Đã vậy, với chỉ hai mươi sáu trang, và không nghi ngờ là được viết vội, cuốn sách của Nguyễn Duy Phương chỉ đưa ra những trình bày sơ lược và thiếu đều đặn về quá khứ. Nó bắt đầu bằng một cuộc thảo luận về cuộc đấu tranh của các chị em Trưng chống lại cai trị của nhà Hán vào thế kỷ thứ nhất sau Công nguyên và sau đó thảo luận về các sự kiện chống đối khác trong nghìn năm cai trị của Trung Hoa. Điều nầy được theo sau bởi một cuộc thảo luận chi tiết về cuộc đấu tranh của Lê Lợi chống lại nhà Minh vào đầu thế kỷ mười lăm. Văn bản kết thúc với một vài nhận xét ngắn gọn về thời kỳ thuộc địa.")
lines.append("")

# P022 (trang 33-34)
lines.append("--- [V1C01-P022] (trang 33-34) ---")
lines.append("Chính phủ Trần Trọng Kim không tồn tại lâu, nhưng mô hình viết về quá khứ Việt Nam đầu tiên xuất hiện vào thập niên 1940 qua những bài viết ngắn của Hồ Chí Minh và Nguyễn Duy Phương thì còn mãi. Vào tháng Tám năm 1945 Nhật đầu hàng và Việt Minh tuyên bố Việt Nam độc lập dưới quyền của mình. Điều nầy đương nhiên bị người Pháp thách thức và Chiến tranh Đông Dương bắt đầu cuối năm sau. Dầu một số trí thức gia nhập Việt Minh, các trí thức khác vẫn ở lại vùng đất do Pháp kiểm soát. Một người nầy, Phạm Văn Sơn, đã nhân dịp nầy viết một cuốn sách sử về Việt Nam toàn diện hơn cả Hồ Chí Minh và Nguyễn Duy Phương từng làm được. Mang tên A History of Vietnamese Struggles, tác phẩm của Phạm Văn Sơn cũng tập trung vào chủ đề đấu tranh giành độc lập và kháng cự ngoại xâm. Ông ấy gọi hai chị em Trưng là \"hai Jeanne d'Arc của Việt Nam.\" Ông dành các chương cho chiến tranh với người Trung Hoa và người Chăm và trình bày chi tiết các \"vận động độc lập\" nảy sinh giữa năm 1861 và 1945. Các đảng cách mạng tìm cách giành độc lập trong nửa đầu thế kỷ hai mươi cũng được bàn đến, cũng như Cách mạng Tháng Tám năm 1945. Không chắc chắn về hướng đi tương lai của Việt Nam, Phạm Văn Sơn dành các chương trong sách của Ông ấy cho Hoàng đế Bảo Đại, người vừa đồng ý làm việc với Pháp để lập ra Quốc gia Việt Nam, và Hồ Chí Minh, người đang chiến đấu với người Pháp.")
lines.append("")

# P023 (trang 35) - Heading
lines.append("--- [V1C01-P023] (trang 35) — đề mục ---")
lines.append("Historical Scholarship in South Vietnam")
lines.append("")

# P024 (trang 35)
lines.append("--- [V1C01-P024] (trang 35) ---")
lines.append("A History of Vietnamese Struggles của Phạm Văn Sơn được xuất bản lần đầu ở Hà Nội vào năm 1949. Khi Chiến tranh Đông Dương kết thúc năm 1954, Phạm Văn Sơn đã đi theo hàng trăm nghìn người khác di cư vào Nam. Văn bản của Ông ấy sau đó được tái bản nhiều lần ở Sài Gòn. Đồng thời, Phạm Văn Sơn tiếp tục viết các tác phẩm mới, bao gồm một cuộc khảo sát nhiều tập về sử lịch sử Việt Nam mang tên A New Compilation of Việt History bắt đầu xuất hiện vào năm 1956. Như vậy, học thuật của Phạm Văn Sơn có thể được xem là sự tiếp nối ở Nam Việt Nam của một cách viết về quá khứ có liên hệ với các thời kỳ trước, vì nó giữ gìn những ý tưởng đã được các nhà sử học tạo ra trong thời kỳ thuộc địa, dưới chính quyền Trần Trọng Kim và Quốc gia Việt Nam. Cách nầy, các tác phẩm sử học của Phạm Văn Sơn không khác gì chính phủ Nam Việt Nam, đã xây dựng trên chuyên môn của những người từng phục vụ trong các chế độ trước.")
lines.append("")

content = "\n".join(lines) + "\n"
content = unicodedata.normalize("NFC", content)
with open(VI, "a", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"Da append Batch 2 (P013-P024) vao {VI}: {len(lines)} dong")
