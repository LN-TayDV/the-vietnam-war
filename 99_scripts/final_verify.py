with open('translation-project/04_translation/v1/ch11/v1_ch11_vi.txt', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Count paragraphs
paras = re.findall(r'--- \[V1C11-P\d+\]', content)
print('Total paragraphs: ' + str(len(paras)))

# List paragraph numbers
para_nums = [int(re.search(r'P(\d+)', p).group(1)) for p in paras]
print('Paragraph numbers: ' + str(para_nums[:10]) + '...' + str(para_nums[-5:]))
print('Min: ' + str(min(para_nums)) + ', Max: ' + str(max(para_nums)))

# Check headings
headings = [p for p in paras if '— đề mục' in p]
print('Headings: ' + str(len(headings)))

# Check image marker
images = [p for p in paras if 'PIMG' in p]
print('Image markers: ' + str(len(images)))

# Check for duplicates
seen = set()
dupes = []
for p in paras:
    num = int(re.search(r'P(\d+)', p).group(1))
    if num in seen:
        dupes.append(num)
    seen.add(num)
print('Duplicate paragraph numbers: ' + str(dupes))

# Check key VNCH terms used
terms = ['chánh phủ', 'chánh trị', 'tài chánh', 'dân biểu', 'ngân khố', 'hưu bổng', 'địa ốc', 
         'nghiệp đoàn', 'kỹ nghê', 'quan thuế', 'hàng không dân sự', 'kế toán', 'sổ thông hành',
         'phân khu', 'tổ khai gia đình', 'hội Hồng Thập Tự', 'ngoại tệ', 'phi đạo', 'xa lộ',
         'làm ăn công', 'trực thăng', 'khiêu vũ', 'Mỹ', 'siêng năng', 'tháo vát', 'nghệ sỹ',
         'khách sạn', 'đồng lòng', 'ngoại kiều', 'viễn suy tư', 'cường liệu', 'nhu liệu',
         'phản ảnh', 'phát thanh', 'cao học', 'phi trường', 'phi cảng', 'hoàn lượng',
         'quân trị', 'công trường', 'cấp bậc', 'tiến trình', 'tân cương', 'sư đoàn',
         'y tế công cộng', 'trở ngại', 'công ty', 'hòa tiến', 'lưu hành', 'thẩm viếng',
         'thanh toán', 'chứng minh', 'thần mê', 'xe du lịch', 'xe đồ', 'giải quyết', 'thi hành',
         'độc lập', 'đồng đạo', 'Nam Kỳ', 'Trung Kỳ', 'Bắc Kỳ', 'Đông Dương',
         'chủ nghĩa tự do', 'chủ nghĩa bảo thủ', 'chủ nghĩa xã hội', 'chủ nghĩa cộng sản',
         'chủ nghĩa phát xít', 'chủ nghĩa dân tộc', 'chủ nghĩa đế quốc', 'chủ nghĩa thực dân',
         'chủ nghĩa toàn trị', 'chủ nghĩa chuyên chế', 'chủ nghĩa sai lệch phải', 'chủ nghĩa sai lệch trái',
         'chủ nghĩa sửa đổi', 'chủ nghĩa cải cách', 'chủ nghĩa tư bản', 'chủ nghĩa tập thể',
         'chủ nghĩa hiệp đoàn', 'chủ nghĩa bảo hộ', 'chủ nghĩa mới tự do',
         'tư tưởng', 'học thuyết', 'triết học', 'phong trào', 'trường phái', 'xu hướng',
         'chủ quyền', 'hiến chính', 'pháp trị', 'xã hội dân sự', 'liên bang chủ nghĩa',
         'thống nhất chủ nghĩa', 'áp chiến lược', 'tìm kiếm và tiêu diệt', 'an bình',
         'việt nam hóa', 'thuyết domino', 'mác-xít', 'lênin', 'lênin chủ nghĩa', 'xta-lin',
         'mao trạch đông', 'trốt-xki']

found = []
missing = []
for t in terms:
    if t in content:
        found.append(t)
    else:
        missing.append(t)

print('\nVNCH Terms found: ' + str(len(found)))
print('VNCH Terms missing: ' + str(len(missing)))
if missing:
    print('Missing: ' + ', '.join(missing[:20]))

# Check VNCH orthography terms
ortho = ['dầu', 'tuy vậy', 'vả', 'chớ không', 'người ấy', 'ông ấy', 'bà ấy',
         'đã... rùi', 'đã... hẵng', 'đang... xong', 'đang... tiến hành',
         'sắp sẽ', 'chuẩn bị sẽ', 'vừa... mới', 'mới... xong',
         'chưa... bao giờ', 'vẫn chưa', 'trái lại', 'bởi thế',
         'dẫu', 'chừng nấy', 'chừng nào', 'nhứt là', 'bổn báo',
         'gởi', 'thơ', 'hết thảy', 'may sao', 'ra vai', 'công cuộc',
         'đôi chục', 'vả', 'quào', 'săng', 'bù quào', 'trang',
         'sỉ nhục', 'cấm kỵ', 'lộn xộn', 'thiệt hành', 'giá ngự',
         'não tủy', 'phổ thông', 'trứ thuật', 'trước tác', 'loại thơ',
         'nhứt', 'mua đồng niên', 'bổn báo']

found_ortho = [t for t in ortho if t in content]
print('\nVNCH Orthography terms found: ' + str(len(found_ortho)) + '/' + str(len(ortho)))