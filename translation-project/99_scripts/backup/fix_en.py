import pathlib, re
p=pathlib.Path(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch04\v1_ch04_vi.txt')
t=p.read_text(encoding='utf-8')
reps = [
 # garbled full-sentence fixes first
 ('Khoảng trống quyền lực ensuing rendering cuộc Cách mạng tháng Tám 1945',
  'Khoảng trống quyền lực sau đó đã làm cho cuộc Cách mạng tháng Tám 1945'),
 ('Nor, evidently, were youth the only group targeted by this athletic campaign. By 1943, most Indochinese civil servants had formed sporting associations, supported by the colonial government in Hanoi.36',
  'Không chỉ vậy, rõ ràng thanh niên không phải nhóm duy nhất bị nhắm đến trong cuộc thi thể thao này. Đến năm 1943, hầu hết các công chức Đông Dương đã hình thành các hiệp hội thể thao, được chính quyền thuộc địa tại Hà Nội hỗ trợ.36'),
 ('Và yet để phục vụ các mục tiêu quân sự của mình',
  'Và để phục vụ các mục tiêu quân sự của mình'),
 # word-level
 ('staging một cuộc tấn công','thực hiện một cuộc tấn công'),
 ('ensuing','sau đó'),
 ('rendering more virile','làm cho trở nên tráng trinh hơn'),
 ('rendering','làm cho'),
 ('Given rằng','Bởi vì rằng'),
 ('Nor,','Không chỉ vậy,'),
 ('irredentist','đòi lại lãnh thổ'),
 ('teleology','teleology (lẽ suy nghĩ theo kết quả trước)'),
 ('coolie','lao động thuê (coolie)'),
 ('Discourse giải phóng','Diễn ngôn giải phóng'),
 ('các correspondents Đông Dương','các phóng viên Đông Dương'),
 ('đã switched trading partners','đã chuyển đổi đối tác thương mại'),
 ('trading partners','đối tác thương mại'),
 ('bắt đầu chart các con đường mới','bắt đầu vạch ra các con đường mới'),
 ('đã revive các schemes','đã khôi phục lại các kế hoạch'),
 ('các schemes trước đây','các kế hoạch trước đây'),
 ('những kế hoạch này là earnest','những kế hoạch này là nghiêm túc'),
 ('các cách counter ảnh hưởng','các cách chống lại ảnh hưởng'),
 ('cũng failed to recognize','cũng không nhận ra'),
 ('failed to recognize','không nhận ra'),
 ('đã backward-looking','đã mang tính ngược dòng'),
 ('bị internment','bị giam giữ'),
 ('thông tư enjoinging','thông tư bắtbuộc'),
 ('bị stranded','bị kẹt'),
 ('sự ngạc nhiên là total','sự ngạc nhiên là toàn phần'),
 ('bảng chuyển đổi intriguing','bảng chuyển đổi hấp dẫn'),
 ('quan hệ cordial','quan hệ thân thiện'),
 ('Jacquinot rose từ','Jacquinot đứng dậy từ'),
 ('đến citadel','đến tòa thành'),
 ('secure các khu vực','kiem soát các khu vực'),
 ('driving Jacquinot indoors','ép Jacquinot vào nhà'),
 ('seizing vũ khí','tịch thu vũ khí'),
 ('được Decoux handpick','do Decoux chọn tay'),
 ('được reimplemented','được thực thi lại'),
 ('null và void','bất hợp pháp và vô hiệu'),
 ('vowed sẽ hoạt động','cam kết sẽ hoạt động'),
 ('nhà vua sẽ warn','nhà vua sẽ cảnh báo'),
 ('đồng hồ không thể bị turned back','đồng hồ không thể bị quay lui lại'),
 ('en route để tham gia','trong hành trình đến tham gia'),
]
count=0
for a,b in reps:
    n=t.count(a)
    if n:
        t=t.replace(a,b)
        count+=n
p.write_text(t, encoding='utf-8', newline='\n')
print('total replacements:', count)

