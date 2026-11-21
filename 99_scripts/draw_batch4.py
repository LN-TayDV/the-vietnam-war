#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dich Batch 4: P038-P049 (trang 39-43) cho Chương 1.
Ap dung 7 buoc Grammar Engine + Style Guide Phan B (VNCH pre-1975).
UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

lines = []

# P038 (trang 39)
lines.append("--- [V1C01-P038] (trang 39) ---")
lines.append("Đây là bản diễn giải về quá khứ mà Hồ Chí Minh lập luận vào năm 1942 người Việt Nam cần phải biết. Đến khi Chiến tranh Việt Nam kết thúc năm 1975, cư dân nửa miền đất nước mà bây giờ là Việt Nam đã được dạy bản sử nầy trong khoảng hai mươi năm. Trong các năm sau đó, nửa còn lại của Việt Nam được giới thiệu với bản diễn giải về quá khứ nầy. Để khởi động nỗ lực nầy, vào năm 1976, Viện Sử Học ở Hà Nội đã xuất bản một cuốn sách mang tên Nước Việt Nam là một, dân tộc Việt Nam là một. Trong nầy, các tác giả tập thể vô danh lập luận về sự thống nhất lịch sử của Việt Nam, và nhấn mạnh vai trò của Đảng Cộng Sản trong việc thống nhất đất nước.")
lines.append("")

# P039 (trang 40) - Heading
lines.append("--- [V1C01-P039] (trang 40) — đề mục ---")
lines.append("Anglophone Histories of Vietnam")
lines.append("")

# P040 (trang 40)
lines.append("--- [V1C01-P040] (trang 40) ---")
lines.append("Như phần bàn luận trên nên làm rõ, bản sử Việt Nam trở nên nổi bật ở Việt Nam sau năm 1975 có lịch sử riêng dài và phức tạp. Trái lại, các bài viết về quá khứ Việt Nam trong tiếng Anh có lịch sử ngắn hơn. Tuy nhiên, trong các năm sau khi Chiến tranh Việt Nam kết thúc, các bài viết nầy cũng đạt đến một dạng \"chính thức\" về quá khứ Việt Nam, một bản phản chiếu bản chính thức ở Việt Nam theo nhiều cách quan trọng.")
lines.append("")

# P041 (trang 40)
lines.append("--- [V1C01-P041] (trang 40) ---")
lines.append("Khi chính phủ Hoa Kỳ lần đầu can thiệp vào các vấn đề Việt Nam trong thập niên 1950, có rất ít thông tin bằng tiếng Anh về sử lịch sử Việt Nam. Trong hai thập niên tiếp theo, nhiều nhà văn và học giả đã cố gắng lấp khoảng trống nầy. Thiếu kiến thức về tiếng Việt, các nhà văn tiếng Anh đầu tiên đã dựa nhiều vào công tác của một số lượng rất giới hạn các học giả viết bằng tiếng Pháp, như Lê Thành Khôi, một người Việt di cư ở Paris, và Paul Mus, một học giả Pháp và quan chức thuộc địa.")
lines.append("")

# P042 (trang 40)
lines.append("--- [V1C01-P042] (trang 40) ---")
lines.append("Cuộc khảo sát đầu tiên về sử lịch sử Việt Nam bằng tiếng Anh là The Smaller Dragon: A Political History of Vietnam của Joseph Buttinger. Buttinger là một nhà chính trị gia xã hội chủ nghĩa sinh ở Áo đã chạy trốn quê hương của Ông ấy vào năm 1938, đầu tiên sang Pháp rồi sang Hoa Kỳ. Trong Thế Chiến II, Buttinger bắt đầu làm việc cho Ủy Ban Cứu Trợ Quốc Tế (IRC), một tổ chức giúp đỡ người tị nạn. Năm 1954 IRC đã gửi Buttinger đến Nam Việt Nam để giúp chính phủ định cư hàng trăm nghìn người tị nạn di cư về phía Nam vĩ tuyến 17 theo Hiệp Định Genève. Đây là lần đầu Buttinger tiếp xúc với Việt Nam, và Ông ấy bị đất nước và dân tộc ấy gây ấn tượng mạnh đến nỗi Ông ấy dành bốn năm tiếp theo đọc mọi thứ Ông ấy tìm thấy bằng các ngôn ngữ phương Tây về Việt Nam và viết một cuộc khảo sát về sử lịch sử Việt Nam.")
lines.append("")

# P043 (trang 40-41)
lines.append("--- [V1C01-P043] (trang 40-41) ---")
lines.append("Trong quá trình nghiên cứu và viết cuốn sách nầy, Buttinger đã bị ảnh hưởng đặc biệt bởi một cuộc khảo sát về sử lịch sử Việt Nam được xuất bản vào năm 1955, Vietnam: History and Civilization, the Environment and History của Lê Thành Khôi. Lê Thành Khôi sinh và lớn lên ở Hà Nội nhưng sau đó đi học ở Châu Âu, nơi Ông ấy nhận bằng tiến sĩ kinh tế ở Paris vào năm 1949 và sau đó đi học luật quốc tế tại La Haye. Vietnam: History and Civilization là công tác sử đầu tiên của Ông ấy. Bị ảnh hưởng phần nào bởi lý thuyết Mác-xít, Lê Thành Khôi lập luận rằng thực dân hóa của Pháp đã dẫn đến sự xuất hiện của giai cấp tư sản và giai cấp vô sản, nhưng một cảm giác lãng mạn về quá khứ đã khiến Ông ấy giảm nhẹ sự tồn tại của bất kỳ sự đối kháng giai cấp nào trong thời kỳ tiền thuộc địa. Ông ấy cũng lạc quan tương tự về tương lai dưới \"dân chủ Mác-xít\" trong \"Việt Nam mới,\" chủ đề của chương kết ngắn của Ông ấy.")
lines.append("")

# P044 (trang 41)
lines.append("--- [V1C01-P044] (trang 41) ---")
lines.append("Buttinger không tái lập quan điểm của Lê Thành Khôi, nhưng Ông ấy đã dựa nhiều vào Vietnam: History and Civilization để tạo ra một câu chuyện cơ bản về quá khứ Việt Nam. Công tác của Buttinger cũng phản chiếu công tác của Lê Thành Khôi trong việc nó tập trung chủ yếu vào sử tiền hiện đại, và thực tế, chỉ cung cấp một bảng niên biểu các sự kiện cho thế kỷ hai mươi. Trong một cước chú, Buttinger đã trách các học giả Pháp vì một sự bất cân bằng trong thông tin sử học về Việt Nam, vì Ông ấy lập luận rằng người Pháp, \"theo chính sách thuộc địa của Pháp,\" đã \"liên tục bỏ qua thực tế của chủ nghĩa dân tộc Việt Nam\" và nhiều sự phát triển đã dẫn đến sự trỗi dậy của nó. \"Ngắn gọn,\" Ông ấy ghi chú, \"họ đã bỏ qua sự phát triển của những lực lượng mà họ phải chiến đấu sau năm 1945.\"")
lines.append("")

# P045 (trang 41)
lines.append("--- [V1C01-P045] (trang 41) ---")
lines.append("Khi chiến tranh đã bùng phát sau năm 1945, có một học giả Pháp đã tìm cách hiểu những lực lượng mà người Pháp phải đối mặt ở Việt Nam: Paul Mus. Sinh ở Pháp nhưng lớn lên ở Hà Nội, Mus đã trở thành một chuyên gia về Ấn Độ và Đông Nam Á và được EFEO thuê. Ông ấy sau đó đã chiến đấu ở các vị trí khác nhau trong Thế Chiến II, phục vụ như một cố vấn chính trị cho cao ủy cho Đông Dương trong những năm sau chiến tranh, và cuối cùng trở lại giảng dạy, dạy cả ở Pháp và tại Đại học Yale. Chiến tranh và Cách mạng Tháng Tám năm 1945 đã có một tác động chuyển hóa đến những ý tưởng của Mus. Khác với nhiều đồng thời của Ông ấy, Mus đã coi nghiêm túc những nguyện vọng dân tộc Việt Nam và thậm chí đã cảm thông với người Việt Nam. Tại thời điểm nầy, tuy nhiên, những ý tưởng tích cực của Ông ấy về người Việt Nam và cuộc đấu tranh chống thuộc địa của họ vẫn được trình bày theo các thuật ngữ phương Đông, giải thích cho độc giả phương Tây của Ông ấy rằng những người phương Đông nầy, dù năng động, vẫn nghĩ ra sao.")
lines.append("")

# P046 (trang 41-42)
lines.append("--- [V1C01-P046] (trang 41-42) ---")
lines.append("Khi Cách tranh Việt Nam bắt đầu, mô tả của Mus về người Việt Nam đã khơi dậy sự hồi ứng với các học sinh của Ông ấy tại Hoa Kỳ, đặc biệt là Frances FitzGerald người đã đến Việt Nam vào năm 1966 như một nhà báo và sau đó xuất bản một tác phẩm giành giải Pulitzer về Cách tranh Việt Nam và bối cảnh sử học của nó, Fire in the Lake: The Vietnamese and the Americans in Vietnam. Cuốn sách nầy bắt đầu bằng một chương mang tên \"States of Mind,\" và tuân theo tư tưởng của Mus, người cuốn sách nầy được tặng, Fitzgerald mô tả thế giới của người Việt Nam như một thế giới hoạt động dựa trên một logic khác. Với nhiều tham chiếu đến các văn bản và ý tưởng trong truyền thống văn hóa Hán, từ Yijing, hoặc Kinh Dịch, đến ý tưởng về Thiên mệnh, Fitzgerald mô tả một thế giới tư duy và hành động hoàn toàn xa lạ với trải nghiệm của người Mỹ.")
lines.append("")

# P047 (trang 42)
lines.append("--- [V1C01-P047] (trang 42) ---")
lines.append("Cuối cùng, những gì FitzGerald và nhiều người theo sau đã lập luận là Việt Nam là một nước mà người Mỹ đơn giản không hiểu, và khi họ hiểu Việt Nam tốt hơn thì họ sẽ thấy nó là một đối thủ mà Hoa Kỳ không thể coi thường. Điểm sau nầy được nhấn mạnh trong một tác phẩm cực kỳ có ảnh hưởng của George Kahin và John Lewis có tên The United States in Vietnam. Dầu các tác giả không biết tiếng Việt, thì sự miêu tả của họ về sử lịch sử Việt Nam rất tương tự với bản diễn giải mà Hồ Chí Minh vào năm 1942 đã lập luận rằng đồng bào của ông phải tiếp nhận. Giống như Hồ Chí Minh, Kahin và Lewis nhìn sử lịch sử Việt Nam như một câu chuyện dài về các nỗ lực chống lại sự xâm nhập nước ngoài và bảo vệ nền độc lập của nước, lập luận rằng \"trong nhiều thế kỷ một chủ đề cơ bản và không đổi của [chủ nghĩa dân tộc Việt Nam] là tự do khỏi sự thống trị của Trung Hoa,\" và khi kết thúc cai trị thuộc địa, \"chủ đề nầy đã khẳng định lại với sức sống truyền thống.\" Một khác biệt với quá khứ, theo Kahin và Lewis, là hiện tại chủ nghĩa dân tộc đã \"liền nhau\" với cộng sản. Thông điệp của họ là những người Mỹ đang đối mặt với một đối thủ mà trong nhiều thiên niên kỷ đã chống lại các nỗ lực trước đó của người nước ngoài kiểm soát đất của họ.")
lines.append("")

# P048 (trang 42)
lines.append("--- [V1C01-P048] (trang 42) ---")
lines.append("Cái nhìn về quá khứ Việt Nam nầy đã trở nên cực kỳ phổ biến trong các thành viên của phong trào chống chiến tranh, và theo thời gian, nó đã đi vào vô số xuất bản, hai trong số các tác phẩm có ảnh hưởng nhất là Vietnam, a History của Stanley Karnow và The Vietnam Wars, 1945–1990 của Marilyn Young. Các tác phẩm nầy thường được tạo ra bởi các tác giả không biết tiếng Việt. Trong khi đó, trong thập niên 1970 và 1980 có các học giả thạo tiếng Việt đã tạo ra các nghiên cứu có căn cứ hơn về quá khứ Việt Nam. Tuy nhiên, nhiều trong các nghiên cứu nầy tập trung vào việc hiểu rõ hơn về phía cộng sản, và trong đó làm bền vững bản diễn giải của Hồ Chí Minh về quá khứ đặt cộng sản ở trung tâm của sử lịch sử Việt Nam.")
lines.append("")

# P049 (trang 42-43)
lines.append("--- [V1C01-P049] (trang 42-43) ---")
lines.append("Kể từ thập niên 1990, đã có một đợt sóng mới của học thuật tiếng Anh về sử lịch sử Việt Nam. Do các học giả viết bằng tiếng Anh nhưng đọc tiếng Việt và đã nghiên cứu lưu trữ rộng rãi, trường học nầy đã chuyển hướng khỏi những diễn biến cơ bản hóa về người Việt Nam và sử lịch sử Việt Nam đã được tạo ra trong và ngoài Việt Nam trong thế kỷ hai mươi. Công tác nầy đã tránh việc mô tả quá khứ Việt Nam như một cuộc đấu tranh vĩnh viễn chống sự thống trị nước ngoài; nó cũng đã thách thức thói quen miêu tả cộng sản là những người thúc đẩy và nhân vật trung tâm trong sử lịch sử Việt Nam thế kỷ hai mươi. Trong các bản diễn giải nầy, sử lịch sử Việt Nam hiện đại xuất hiện như một câu chuyện phức tạp hơn về nhiều nỗ lực xây dựng Việt Nam dựa trên những tầm nhìn cạnh tranh về tương lai. Học thuật nầy, theo lượt đó, đã mở ra những tầm nhìn mới trên sử lịch sử các Chiến tranh Đông Dương – bao gồm \"Cách tranh Việt Nam\" bắt đầu vào cuối thập niên 1950 và kéo dài cho đến năm 1975. Trong các chương sau, độc giả sẽ tìm thấy nhiều ví dụ về những tầm nhìn mới và những hiểu biết sử học có thể thu được từ chúng. Những tầm nhìn mới và những hiểu biết nầy không nghi ngờ rất khác với những gì Hồ Chí Minh có trong tâm trí khi Ông ấy tuyên bố vào năm 1942 rằng \"lịch sử ta phải được nghiên cứu.\" Nhưng chúng không kém phần là một phần của truyền thống vẫn đang diễn ra tìm hiểu Việt Nam thông qua sử lịch sử sinh động và thú vị của nó.")
lines.append("")

content = "\n".join(lines) + "\n"
content = unicodedata.normalize("NFC", content)
with open(VI, "a", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"Da append Batch 4 (P038-P049) vao {VI}: {len(lines)} dong")
