#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dich Batch 3: P025-P037 (trang 35-39) cho Chương 1.
Ap dung 7 buoc Grammar Engine + Style Guide Phan B (VNCH pre-1975).
UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

lines = []

# P025 (trang 35)
lines.append("--- [V1C01-P025] (trang 35) ---")
lines.append("Tuy nhiên, đồng thời, các nhà sử học ở Nam Việt Nam, như các đồng sự trong chính phủ, cũng đóng góp vào tiến trình giải thực dân. Dầu họ xây dựng và trích dẫn công tác của các nhà sử học thời thuộc địa, các nhà sử học Nam Việt Nam cũng tìm cách sản sinh học thuật sử học mới có thể giúp tạo nên tinh thần dân tộc cho quốc gia trẻ của họ. Đại Học Huế, thành lập năm 1957, đã khởi động tiến trình nầy. Đại Học Huế đã thuê một nhà sử học từ Đài Loan từng dành thời gian tại EFEO vào thập niên 1940, Chen Jinghe, để dẫn đầu một nhóm học giả bắt đầu phân loại và dịch các tài liệu triều Nguyễn. Đại Học Huế cũng xuất bản một tờ tạp chí gọi là University (Đại học) đăng các bài về nhiều chủ đề từ triết học Pháp đến ngôn ngữ học và sử học Việt Nam. Một trong các số đầu tiên có một bài của một nhà sử học trẻ vừa trở về từ trường cao học ở Bỉ, Trương Bửu Lâm, kêu gọi một chương trình sử học quốc gia mới.")
lines.append("")

# P026 (trang 35-36)
lines.append("--- [V1C01-P026] (trang 35-36) ---")
lines.append("Đại Học Huế được hỗ trợ không chỉ bởi chính phủ Nam Việt Nam mà còn bởi các tổ chức nước ngoài như Ủy Ban Cứu Trợ Quốc Tế, Quỹ Châu Á, Ủy Ban Người Mỹ Tài Trợ của Đại Học Huế, và Hội Hữu Nghị Mỹ–Việt Nam. Nó là một phần trong nỗ lực thời Chiến Tranh Lạnh để xây dựng một Nam Việt Nam dân chủ và thịnh vượng. Nỗ lực ấy đã bắt đầu lung lay, dầu vậy, khi đại học bị cuốn vào các sự kiện hỗn loạn năm 1963 dẫn đến vụ ám sát Tổng thống Ngô Đình Diệm vào tháng Mười Một của năm nầy. Hiệu trưởng Công giáo của đại học, Cao Văn Luận, bị Tổng thống Diệm sa thải vì ủng hộ Phật giáo, và dầu được phục chức ngắn ngủi sau vụ ám sát Diệm, thời thế đã thay đổi. Tạp chí Đại học ngừng xuất bản và dự án nguồn sử của triều Nguyễn bị đình chỉ.")
lines.append("")

# P027 (trang 36)
lines.append("--- [V1C01-P027] (trang 36) ---")
lines.append("Điều nầy tuy nhiên không phải là kết thúc cho học thuật sử học ở Nam Việt Nam. Trái lại, các giáo sư và sinh viên tại Đại Học Sư Phạm Sài Gòn hợp tác bắt đầu xuất bản một tờ tạp chí năm 1965 tên Lịch Sử và Địa lý. Tạp chí nầy được xuất bản liên tục cho đến năm 1975 và đăng các bài của các nhà sử học đã trưởng thành trong thời kỳ thuộc địa, như Phạm Văn Sơn, Hoàng Xuân Hãn, Hồ Hữu Tường và Phan Khoang, cũng như một thế hệ mới các nhà sử học Nam Việt Nam, như Tạ Chí Đài Trường và Nguyễn Thế Anh. Trong nỗ lực tạo nên tinh thần dân tộc, dầu mang sắc thái miền Nam, các nhà sử học nầy đăng các bài về các nhân vật nổi tiếng trong sử lịch sử Việt Nam, như Trương Công Định, một quan chức triều Nguyễn đã lãnh đạo cuộc kháng chiến chống người Pháp ở Nam Kỳ trong thập niên 1860, Phan Thanh Giản, một quan chức triều Nguyễn đã tự tử năm 1867 vì không ngăn được người Pháp giành quyền kiểm soát Nam Kỳ, và Nguyễn Huệ, người lãnh đạo Khởi Nghĩa Tây Sơn.")
lines.append("")

# P028 (trang 36) - Heading
lines.append("--- [V1C01-P028] (trang 36) — đề mục ---")
lines.append("Historical Scholarship in North Vietnam")
lines.append("")

# P029 (trang 36)
lines.append("--- [V1C01-P029] (trang 36) ---")
lines.append("Giống như các đồng sự ở Nam Việt Nam, các nhà sử học ở Bắc Việt Nam rất háo hức sản sinh các tác phẩm sử học để giáo dục dân chúng dưới quyền họ. Tuy nhiên, trong khi các nhà sử học Nam Việt Nam xây dựng trên công tác của các nhà sử học thời thuộc địa, các nhà sử học ở Bắc Việt Nam tìm cách đoạn tuyệt có chủ ý với thế giới học thuật thuộc địa. Họ phán xét \"tâm lý thuộc địa\" của các học giả EFEO và cố gắng sản sinh học thuật không bị ảnh hưởng thuộc địa. Và đáng ngạc nhiên, các nhà sử học Bắc Việt Nam cố làm điều nầy bằng cách tuân theo sát một mô hình nước ngoài khác về sản xuất tri thức, sử học Mác-xít, mà họ học từ các tác phẩm Trung Hoa và Xô Viết.")
lines.append("")

# P030 (trang 36-37)
lines.append("--- [V1C01-P030] (trang 36-37) ---")
lines.append("Tiến trình nầy chính thức bắt đầu năm 1953, khi Chiến tranh Đông Dương vẫn đang diễn ra, với việc thành lập Viện Sử Học. Các học giả liên kết với viện nầy đã bắt đầu thảo luận về nhiều vấn đề mà các đồng sự Trung Hoa và Xô Viết của họ đang tranh luận, như cách phân kỳ sử lịch sử Việt Nam theo các giai đoạn phát triển của Mác-xít, và cách xác định khi nào quốc gia/dân tộc Việt Nam được hình thành, dùng định nghĩa của Stalin về quốc gia/dân tộc. Nhiều quan điểm mà các học giả đề xuất đã được đăng trong một tờ tạp chí gọi là Văn sử địa.")
lines.append("")

# P031 (trang 37)
lines.append("--- [V1C01-P031] (trang 37) ---")
lines.append("Một số nhà sử học cũng làm việc để sản sinh các công trình khảo sát về sử lịch sử Việt Nam. Người đầu tiên làm điều nầy là một người viết dưới bút danh Minh Tranh (Khuất Duy Tiễn). Năm 1936 Minh Tranh trở thành cộng sản, và trong Chiến tranh Đông Dương Ông ấy phục vụ như một viên tuyên truyền, ký giả và biên tập viên cho Việt Minh. Ông ấy cũng là uỷ viên của Ban Nghiên cứu Văn Sử Địa Trung ương. Năm 1954 Minh Tranh xuất bản một cuốn sách mang tên Sơ thảo lược sử Việt Nam nhằm làm sách giáo khoa sử cho các trường ở Bắc Việt Nam. Tác phẩm nầy tuân theo sát lý thuyết Mác-xít. Nó chia sử lịch sử Việt Nam thành các thời kỳ cộng sản nguyên thủy, xã hội nô lệ, phong kiến, v.v., và nhấn mạnh các cuộc nổi dậy nông dân như ví dụ về đấu tranh của giai cấp lao động chống lại áp bức của giới phong kiến.")
lines.append("")

# P032 (trang 37)
lines.append("--- [V1C01-P032] (trang 37) ---")
lines.append("Hai năm sau, vào năm 1956, nhà sử học Đào Duy Anh xuất bản một cuộc khảo sát khác mang tên Lịch sử Việt Nam. Đào Duy Anh thấy giá trị trong cách tiếp cận Mác-xít đối với sử học; tuy nhiên, Ông ấy cảm thấy lý thuyết Mác-xít phải được điều chỉnh cho phù hợp với bối cảnh Việt Nam thay vì được áp đặt cứng nhắc, và cuộc khảo sát nầy về cơ bản không có lý thuyết Mác-xít. Hơn nữa, trong một cuộc phỏng vấn được đăng cùng năm nầy trong tờ tạp chí Nhân Văn, Đào Duy Anh đã phán xét các hạn chế đang được đặt lên các nhà sử học vào thời điểm nầy.")
lines.append("")

# P033 (trang 37)
lines.append("--- [V1C01-P033] (trang 37) ---")
lines.append("Tờ tạp chí nầy là một trong hai tờ tạp chí (tờ kia là Giai Phẩm, hoặc Kiệt Tác) phán xét các hạn chế của chính phủ đối với đời sống nghệ thuật và trí thức sau Chiến tranh Đông Dương. Chính phủ Bắc Việt Nam đã đàn áp sự phán xét nầy, một sự kiện được biết đến như Vụ Nhân văn–Giai phẩm. Năm 1958 học thuật của Đào Duy Anh bị tố cáo, và Sơ thảo lược sử Việt Nam của Minh Tranh được tôn vinh như một mô hình lý tưởng cho việc viết sử lịch sử Việt Nam. Tuy nhiên, vinh dự ấy không kéo dài lâu – Minh Tranh bị giáng chức năm 1963 vì quan điểm \"sửa đổi\" của Ông ấy chống lại việc mở rộng chiến tranh ở Nam.")
lines.append("")

# P034 (trang 38)
lines.append("--- [V1C01-P034] (trang 38) ---")
lines.append("Cả hai người nầy đều ở tuổi năm mươi khi bị giáng chức, và một thế hệ mới các nhà sử học ở tuổi hai mươi đã xuất hiện để thay thế. Vào đầu thập niên 1960, ví dụ, nhà khảo cổ Hà Văn Tấn và nhà sử học Trần Quốc Vượng đã xuất bản một tập về sử sơ khai tên Lịch sử chế độ cộng sản nguyên thủy ở Việt Nam và đóng góp một tập về sử sơ khai vào một công tác ba tập tên Lịch sử chế độ phong kiến Việt Nam. Tập thứ hai trong loạt nầy, về sử thời tiền hiện đại, do nhà sử học Phan Huy Lê viết. Trong khi đó, tập cuối, về sử hiện đại, do Phan Huy Lê, Chu Thiên, Vương Hoàng Tuyên và Đinh Xuân Lâm viết. Bốn người nầy – Hà Văn Tấn, Trần Quốc Vượng, Phan Huy Lê và Đinh Xuân Lâm – sẽ tiếp tục sản sinh các tác phẩm sử học trong nhiều thập niên nữa và được biết đến như \"Tứ trụ sử học.\"")
lines.append("")

# P035 (trang 38)
lines.append("--- [V1C01-P035] (trang 38) ---")
lines.append("Dầu các nhan đề của các tác phẩm nầy cho thấy nỗ lực tuân theo ý tưởng của sử học Mác-xít, với sự mở rộng chiến tranh vào năm 1963 các nhà sử học ở Bắc Việt Nam đã từ bỏ sự tuân thủ nghiêm ngặt lý thuyết Mác-xít mà Minh Tranh đã thúc đẩy trong thập niên 1950 để ủng hộ một cách tiếp cận mang khuynh hướng dân tộc hơn đối với quá khứ. Các nhà sử học Bắc Việt Nam ngừng viết về phân chia và xung đột giai cấp, thay vào đó tập trung vào sự đoàn kết. Hơn nữa, sự chia rẽ Tàu–Xô, Cách Mạng Văn Hóa, và chuyến thăm Trung Hoa của Nixon đều là những sự kiện dần dần đưa một yếu tố chống Trung Hoa vào các tác phẩm sử học. Chủ đề nầy được đặt ra một cách tinh tế vào giữa thập niên 1960 khi các nhà sử học bắt đầu viết về một sử lịch sử \"kháng cự ngoại xâm\" để động viên dân chúng, nhưng nó cuối cùng đạt mức cực đoan trong và sau cuộc chiến biên giới năm 1979 với Trung Hoa.")
lines.append("")

# P036 (trang 38-39)
lines.append("--- [V1C01-P036] (trang 38-39) ---")
lines.append("Một diễn biến quan trọng khác trong thời kỳ nầy là sự tập trung mạnh mẽ vào sử cổ. Một loạt hội nghị đã được tổ chức ở Hà Nội vào cuối thập niên 1960 và đầu thập niên 1970 trong đó các học giả từ nhiều lĩnh vực tìm cách chứng minh rằng các vị vua đầu tiên ở Đồng Bằng Sông Hồng, các vua Hùng huyền thoại, thực sự đã tồn tại. Ở đây công tác của các nhà khảo cổ Bắc Việt Nam đặc biệt quan trọng vì họ cố gắng tìm bằng chứng vật chất cho sự tồn tại của các vị vua nầy để bù đắp cho sự thiếu vắng thông tin văn bản vững chắc. Cuối cùng, các nhà khảo cổ đã tìm thấy nhiều hiện vật, nhưng không gì có thể chứng minh không thể chối cãi sự tồn tại của các vua Hùng. Như vậy, dầu các học giả ban đầu tìm cách xác minh rằng những vị vua ấy đã tồn tại, họ đã kết thúc bằng việc tuyên bố rằng \"thời kỳ\" của các vua Hùng đã tồn tại. Tuy nhiên, điều nầy đủ để phục vụ nhu cầu dân tộc của thời điểm để động viên dân chúng đứng sau nỗ lực chiến tranh bằng cách chỉ ra sự cổ xưa giả định của quốc gia/dân tộc Việt Nam với trái tim ở Đồng Bằng Sông Hồng.")
lines.append("")

# P037 (trang 39)
lines.append("--- [V1C01-P037] (trang 39) ---")
lines.append("Vào thập niên 1970, các diễn biến nầy đã đạt đến đỉnh điểm trong cái mà chúng ta có thể xem là sử lịch sử Việt Nam chính thống như được biết ngày nầy ở Việt Nam. Bản diễn giải về quá khứ nầy lập luận rằng đã có một nhóm người thống nhất và có văn hóa, ngôn ngữ riêng biệt sống ở Đồng Bằng Sông Hồng từ lâu trước khi các triều Qin và Han của Trung Hoa mở rộng quyền kiểm soát vào khu vực nầy vào cuối thiên niên kỷ thứ nhất trước Công nguyên. Nhóm người nầy chịu đựng một thiên niên kỷ bị Trung Hoa cai trị, nhưng xuất hiện trở lại như một quốc gia/dân tộc độc lập, và quốc gia/dân tộc ấy đã chiến đấu chống lại những nỗ lực liên tiếp của người ngoại quốc xâm lấn đất của họ từ đó đến nay. Cuối cùng, trong thế kỷ hai mươi, sử lịch sử Việt Nam chính thống nầy lập luận, nhiệm vụ kháng cự ngoại xâm được Đảng Cộng Sản lãnh đạo.")
lines.append("")

content = "\n".join(lines) + "\n"
content = unicodedata.normalize("NFC", content)
with open(VI, "a", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"Da append Batch 3 (P025-P037) vao {VI}: {len(lines)} dong")
