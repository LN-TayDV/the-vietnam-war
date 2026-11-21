import re

# Read the fixed translation (main section)
with open('translation-project/04_translation/v1/ch01/v1_ch01_vi_fixed.txt', 'r', encoding='utf-8') as f:
    fixed = f.read()

# Read source for markers
with open('translation-project/04_translation/v1/ch01/v1_ch01_src.txt', 'r', encoding='utf-8') as f:
    src = f.read()

# Split source for markers
src_paras = re.split(r'--- \[V1C01-P\d+\]', src)
src_paras = [p.strip() for p in src_paras[1:] if p.strip()]

# Missing translations (from ch01_missing_translations.py)
MISSING = {
    38: '— [V1C01-P039] (trang 40) — đề mục —\nSử Việt Nam Trong Các Ngôn Ngữ Anh',
    39: '— [V1C01-P040] (trang 40) —\nNhư phần bàn luận trên nên làm rõ, bản sử Việt Nam trở nên nổi bật ở Việt Nam sau năm 1975 có lịch sử riêng dài và phức tạp. Trái lại, các bài viết về quá khứ Việt Nam trong tiếng Anh có lịch sử ngắn hơn. Tuy vậy, trong các năm sau khi Chiến tranh Việt Nam kết thúc, các bài viết này cũng đạt đến một dạng "chính thức" về quá khứ Việt Nam, một bản phản chiếu bản chính thức ở Việt Nam theo nhiều cách quan trọng.',
    40: '— [V1C01-P041] (trang 40) —\nKhi chánh phủ Hoa Kỳ lần đầu can thiệp vào các vấn đề Việt Nam trong thập niên 1950, có rất ít thông tin bằng tiếng Anh về sử Việt Nam. Trong hai thập niên tiếp theo, nhiều nhà văn và học giả cố gắng lấp khoảng trống ấy. Thiếu kiến thức về tiếng Việt, các nhà văn tiếng Anh đầu tiên dựa nhiều vào công trình của một số học giả rất giới hạn viết bằng tiếng Pháp, như Lê Thành Khôi, một người Việt di cư ở Paris, và Paul Mus, một học giả Pháp và quan chức thuộc địa.',
    41: '— [V1C01-P042] (trang 40) —\nCông trình tổng quan đầu tiên về sử Việt Nam bằng tiếng Anh là _Con Rồng Nhỏ: Một Sử Chính Trị Việt Nam_ của Joseph Buttinger.[26] Buttinger là một chánh trị gia xã hội chủ nghĩa sinh ở Áo đã chạy trốn quê hương năm 1938, đầu tiên sang Pháp rồi sang Hoa Kỳ. Trong Thế Chiến II, Buttinger bắt đầu làm việc cho Ủy Ban Cứu Trợ Quốc Tế (IRC), một tổ chức cứu trợ người tị nạn. Năm 1954 IRC gửi Buttinger đến Nam Việt Nam để giúp chánh phủ định cư hàng trăm ngàn người tị nạn di cư về phía Nam vĩ tuyến 17 theo Hiệp Định Genève. Đây là lần đầu Buttinger tiếp xúc với Việt Nam, và ông bị đất nước và dân tộc ấy gây ấn tượng mạnh đến nỗi ông dành bốn năm tiếp theo đọc mọi thứ ông tìm thấy bằng các ngôn ngữ Tây phương về Việt Nam và viết một công trình tổng quan về sử Việt Nam.',
    42: '— [V1C01-P043] (trang 40-41) —\nTrong quá trình nghiên cứu và viết cuốn sách này, Buttinger bị ảnh hưởng đặc biệt bởi một công trình tổng quan về sử Việt Nam xuất bản năm 1955, _Việt Nam: Sử Và Văn Minh, Môi Trường Và Lịch Sử_ của Lê Thành Khôi.[27] Lê Thành Khôi sinh và lớn lên ở Hà Nội nhưng sau đó đi học ở Âu châu, nơi ông nhận bằng tiến sĩ kinh tế ở Paris năm 1949 rồi tiếp tục học luật quốc tế tại La Haye. _Việt Nam: Sử Và Văn Minh_ là công trình sử học đầu tiên của ông. Bị ảnh hưởng phần nào bởi lý thuyết Marx, Lê Thành Khôi lập luận rằng thực dân Pháp đã dẫn đến sự xuất hiện của giai cấp tư sản và giai cấp vô sản, nhưng một cảm giác lãng mạn về quá khứ khiến ông giảm nhẹ sự tồn tại của bất kỳ sự đối kháng giai cấp nào trong thời kỳ tiền thuộc địa. Ông cũng lạc quan tương tự về tương lai dưới "dân chủ Marx" trong "Việt Nam mới," chủ đề của chương kết ngắn của ông.',
    43: '— [V1C01-P044] (trang 41) —\nButtinger không tái sản xuất quan điểm của Lê Thành Khôi, nhưng ông dựa nhiều vào _Việt Nam: Sử Và Văn Minh_ để tạo nên một câu chuyện cơ bản về quá khứ Việt Nam. Công trình của Buttinger cũng phản chiếu của Lê Thành Khôi ở chỗ nó tập trung chủ yếu vào sử thời tiền hiện đại, và thực ra chỉ cung cấp một biên niên sự kiện cho thế kỷ hai mươi. Trong một cước chú, Buttinger đổ lỗi cho các học giả Pháp về sự mất cân đối trong thông tin sử về Việt Nam, vì ông lập luận rằng người Pháp, "theo chính sách thuộc địa Pháp," đã "liên tục bỏ qua thực tại của chủ nghĩa dân tộc Việt Nam" và nhiều diễn biến dẫn đến sự trỗi dậy của nó. "Tóm lại," ông ghi, "họ đã bỏ qua sự phát triển của các lực lượng mà họ phải chiến đấu sau năm 1945."[28]',
    44: '— [V1C01-P045] (trang 41) —\nKhi chiến tranh nổ ra sau năm 1945, có một học giả Pháp tìm cách hiểu các lực lượng mà người Pháp đối mặt ở Việt Nam: Paul Mus. Sinh ở Pháp nhưng lớn lên ở Hà Nội, Mus trở thành chuyên gia về Ấn Độ sơ kỳ và Đông Nam Á và được EFEO thuê. Sau đó ông chiến đấu trong nhiều khả năng trong Thế Chiến II, phục vụ như cố vấn chánh trị cho Cao Ủy Đông Dương trong những năm ngay sau chiến tranh, và cuối cùng trở lại học viện, dạy cả ở Pháp và tại Đại Học Yale. Chiến tranh và Cách mạng Tháng Tám 1945 có tác dụng biến đổi đối với ý tưởng của Mus.[29] Không như nhiều đồng sự của ông, Mus nghiêm túc xem xét những khát vọng dân tộc chủ nghĩa Việt Nam và thậm chí đồng cảm với người Việt.[30] Tuy vậy, đồng thời, quan điểm tích cực của ông về người Việt và cuộc tranh đấu chống thực dân của họ vẫn được đặt trong các thuật ngữ Phương Đông giải thích cho độc giả Phương Tây cách những người Phương Đông ấy, dẫu năng động, suy nghĩ.[31]',
    45: '— [V1C01-P046] (trang 41-42) —\nKhi Chiến tranh Việt Nam bắt đầu, mô tả của Mus về người Việt Nam gây tiếng vang với sinh viên của ông ở Hoa Kỳ, đặc biệt là Frances FitzGerald, người viếng thăm Việt Nam năm 1966 như ký giả và sau đó xuất bản một công trình đoạt Pulitzer về Chiến tranh Việt Nam và bối cảnh sử của nó, _Ngọn Lửa Trong Hồ: Người Việt Nam Và Người Mỹ Ở Việt Nam_.[32] Cuốn sách bắt đầu với một chương tên "Trạng Thái Tinh Thần," và theo Mus, người mà cuốn sách được dành tặng, FitzGerald mô tả thế giới Việt Nam như một thế giới hoạt động dựa trên một logic khác. Với nhiều trích dẫn từ các văn bản và ý tưởng trong truyền thống văn hóa Hán, từ _Kinh Dịch_, hay Kinh Điển về Thay Đổi, đến ý tưởng Thiên Mệnh, FitzGerald mô tả một thế giới tư tưởng và hành động hoàn toàn xa lạ với trải nghiệm Mỹ.',
    46: '— [V1C01-P047] (trang 42) —\nCuối cùng, điều FitzGerald và nhiều người khác theo sau lập luận là Việt Nam là một đất nước mà người Mỹ đơn giản là không hiểu, và rằng một khi họ hiểu Việt Nam tốt hơn họ sẽ thấy đây là một kẻ thù Hoa Kỳ không thể xem nhẹ. Điểm sau được nhấn mạnh trong một công trình cực kỳ có ảnh hưởng của George Kahin và John Lewis mang tên _Hoa Kỳ Ở Việt Nam_. Dẫu các tác giả không biết tiếng Việt, mô tả của họ về sử Việt Nam rõ rệt giống với bản diễn giải mà Hồ Chí Minh năm 1942 lập luận đồng bào ông phải chấp nhận. Như Hồ Chí Minh, Kahin và Lewis xem sử Việt Nam như một câu chuyện dài về nỗ lực kháng cự xâm nhập ngoại quốc và duy trì độc lập của đất nước, lập luận rằng "trong nhiều thế kỷ một chủ đề cơ bản và không đổi của [chủ nghĩa dân tộc Việt Nam] là tự do khỏi sự thống trị của Trung Hoa," và rằng với sự kết thúc của thời kỳ thuộc địa, "chủ đề ấy tái khẳng định với sinh lực truyền thống."[33] Một sự khác biệt với quá khứ, theo Kahin và Lewis, là bây giờ chủ nghĩa dân tộc đã "hợp nhất" với chủ nghĩa cộng sản.[34] Thông điệp của họ vì thế là người Mỹ đang đối mặt với một kẻ thù đã trong thiên niên kỷ chiến đấu chống lại những nỗ lực trước của người ngoại quốc kiểm soát đất của họ.',
    47: '— [V1C01-P048] (trang 42) —\nBản diễn giải về quá khứ Việt Nam này trở nên cực kỳ phổ biến trong các thành viên phong trào phản chiến, và theo thời gian nó đi vào vô số ấn phẩm, hai trong số có ảnh hưởng nhất là _Việt Nam, Một Lịch Sử_ của Stanley Karnow và _Các Chiến Tranh Việt Nam, 1945–1990_ của Marilyn Young.[35] Các tác phẩm này thường được sản sinh bởi các tác giả không biết tiếng Việt. Trong khi đó, trong thập niên 1970 và 1980 có các học giả thành thạo ngôn ngữ ấy sản sinh các nghiên cứu vững chắc hơn về quá khứ Việt Nam. Tuy vậy, nhiều nghiên cứu này tập trung vào việc hiểu tốt hơn phía cộng sản, và theo đó kéo dài bản diễn giải của Hồ Chí Minh về quá khứ đặt cộng sản ở trung tâm sử Việt Nam.',
    48: '— [V1C01-P049] (trang 42-43) —\nTừ thập niên 1990, đã có một làn sóng mới học thuật tiếng Anh về sử Việt Nam. Được sản sinh bởi các học giả viết bằng tiếng Anh nhưng đọc tiếng Việt và đã tiến hành nghiên cứu lưu trữ rộng rãi, khối học thuật này đã đi xa khỏi các mô tả *essentialized* (tinh huyết hóa/đơn giản hóa bản chất) về người Việt và sử Việt Nam được sản sinh trong và ngoài Việt Nam trong thế kỷ hai mươi. Công trình này đã tránh mô tả quá khứ Việt Nam như một cuộc tranh đấu vĩnh cửu chống sự thống trị ngoại quốc; nó cũng thách thức thói quen mô tả cộng sản như các động lực chính và các tác nhân trung tâm trong sử Việt Nam thế kỷ hai mươi. Trong các bản tường thuật này, sử Việt Nam hiện đại xuất hiện như một câu chuyện phức tạp hơn nhiều về nhiều nỗ lực xây dựng Việt Nam dựa trên các tầm nhìn cạnh tranh về tương lai. Học thuật này, đến lượt nó, đã mở ra các góc nhìn mới về sử các Chiến Tranh Đông Dương – bao gồm "Chiến Tranh Việt Nam" bắt đầu từ cuối thập niên 1950 và tiếp tục cho đến năm 1975. Trong các chương tiếp theo, độc giả sẽ tìm thấy nhiều ví dụ về các góc nhìn mới ấy và những hiểu biết sử học có thể rút ra từ chúng. Các góc nhìn và hiểu biết mới ấy chắc chắn rất khác những gì Hồ Chí Minh có trong đầu khi ông tuyên bố năm 1942 rằng "sử ta phải được học." Nhưng chúng không kém phần là một phần của truyền thống còn đang diễn ra về tìm cách hiểu Việt Nam qua lịch sử sôi động và hấp dẫn của nó.'
}

# Parse the fixed translation
fixed_paras = re.split(r'--- \[V1C01-P\d+\]', fixed)
fixed_paras = [p.strip() for p in fixed_paras[1:] if p.strip()]

# Replace missing paragraphs (indices 38-48) with translations
for i in range(38, 49):
    if i < len(fixed_paras):
        fixed_paras[i] = MISSING[i]
    else:
        fixed_paras.append(MISSING[i])

# Now rebuild the complete file with proper markers from source
output = '===== V1-C01 · Trí nhớ, Truyền thống và Sử học về "Việt Nam" · Liam C. Kelley =====\n'
output += 'Nguồn: 02_extracted_text/v1/ch01.txt · PDF 43-59 · trang in 27-43\n\n'

for i, src_para in enumerate(src_paras):
    # Extract page/heading marker from source
    marker_match = re.search(r'(\(trang [\d\-]+\)\s*---.*?)(?=\n)', src_para)
    if marker_match:
        marker = marker_match.group(1)
    else:
        marker = '(trang ???) ---'
    
    is_heading = '— đề mục' in src_para or 'heading' in src_para.lower()
    if is_heading:
        marker = marker.replace('---', '— đề mục ---')
    
    vi_para = fixed_paras[i] if i < len(fixed_paras) else '[MISSING]'
    output += f'--- [V1C01-P{i+1:03d}] {marker}\n{vi_para}\n\n'

# Add footnotes from original translation
with open('translation-project/04_translation/v1/ch01/v1_ch01_vi.txt', 'r', encoding='utf-8') as f:
    orig_vi = f.read()

footnote_blocks = re.findall(r'--- \[Cước chú.*?---', orig_vi, re.DOTALL)
if footnote_blocks:
    output += '\n'.join(footnote_blocks)

# Save complete fixed translation
with open('translation-project/04_translation/v1/ch01/v1_ch01_vi_complete.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(output)

print('Complete fixed translation saved to v1_ch01_vi_complete.txt')
print(f'Total paragraphs: {len(fixed_paras)}')