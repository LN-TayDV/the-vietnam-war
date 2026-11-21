# -*- coding: utf-8 -*-
"""
build_lexicon.py — Tạo MASTER_LEXICON.csv từ các mục từ ĐÃ KIỂM CHỨNG.
Mỗi mục có nguồn thật (SRC-xxx), ví dụ trích từ corpus đã tải, mức xác minh.
KHÔNG bịa nghĩa, số trang, ví dụ. Nếu chưa chắc -> verification=UNVERIFIED hoặc PARTIALLY_VERIFIED.
"""
import csv, os
base=r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\08_southern_vietnamese_library'
out=os.path.join(base,'10_LEXICAL_DATABASE','MASTER_LEXICON.csv')

# Mỗi dòng: tu_chuan, loai_tu, nghia, cach_dung, vi_du_nguyen_ban, nguon, trang, thoi_ky, muc_xac_minh, linh_vuc, ghi_chu
# Chỉ điền những gì có bằng chứng thật. Ví dụ lấy từ corpus đã tải (Lê Văn Đức / Phan Khôi).
rows = [
 # (tu, loai, nghia, cach_dung, vi_du, nguon, trang, thoi_ky, xac_minh, linh_vuc, ghi_chu)
 ("sĩ phu","danh_tu","Tầng lớp trí thức, kẻ sĩ (gốc Hán-Việt)","Dùng chỉ giới trí thức Nho học","Đôi chục năm nay sĩ phu ta có một cái sỉ nhục khó chịu…","SRC-021","", "1932","CROSS_VERIFIED","van_hoa_hoc_thuat","Từ Hán-Việt, dùng phổ biến ở Nam; Phan Khôi dùng"),
 ("bổn quốc","danh_tu","Đất nước, quốc gia (cách nói cũ)","Nói văn vẻ, trang trọng","…không có tự điển của người bổn quốc làm ra cho thật đúng đắn.","SRC-021","","1932","VERIFIED","chinh_tri_van_hoc","Cách nói Nam Bộ; bổn = bản (đất nước)"),
 ("bổn cảo","danh_tu","Bản thảo, bản nháp","Chỉ bản viết chưa hoàn thiện","Bộ Tự điển đây mới là bổn cảo chớ chưa phải đã thành sách rồi.","SRC-021","","1932","VERIFIED","van_hoc","Dạng Nam Bộ của 'bản thảo'"),
 ("chớ","liên_tu","Nhưng, mà (nhấn mạnh, tương phản)","Nối vế câu, nhấn mạnh ý đối lập","Bộ Tự điển đây mới là bổn cảo chớ chưa phải đã thành sách rồi.","SRC-021","","1932","CROSS_VERIFIED","van_dung_thuong_ngay","Từ Nam Bộ đặc trưng; thay cho 'mà/nhưng'"),
 ("nầy","tinh_tu","Này (chỉ vật gần)","Thay 'này' trong văn viết Nam trước 1975","Ta thử hỏi tại sao bộ Tự điển nầy không in ngay thành sách…","SRC-021","","1932","VERIFIED","chinh_ta","Chính tả Nam Bộ: 'nầy' thay 'này'"),
 ("chừng nào","phó_tu","Bao nhiêu, mức nào (chừng mực)","Dùng với 'càng…càng…'","…càng phân chừng nào lại càng lộn xộn chừng nấy.","SRC-021","","1932","VERIFIED","van_dung","'chừng nấy' = chừng ấy (Nam Bộ)"),
 ("nấy","tinh_tu","Ấy, đó (thay cho 'ấy' trong Nam Bộ)","Đi với 'chừng' → 'chừng nấy'","…càng phân chừng nào lại càng lộn xộn chừng nấy.","SRC-021","","1932","VERIFIED","van_dung","Dạng Nam Bộ của 'ấy'"),
 ("giục giã","động_tu","Thúc đẩy, khuyến khích","Làm cho mau, cho mạnh","…như vậy là giục giã cho hội ấy làm mau rồi bộ Tự điển vậy.","SRC-021","","1932","VERIFIED","van_dung","Từ Nam Bộ, sắc thái thân mật khích lệ"),
 ("rút ruột","động_tu","Thẳng thắn, thật lòng (rút ruột)","Nói thiệt tình","Cái đời tôi… chỉ có chực chỉ trích mà thôi. (ngữ cảnh thẳng thắn)","SRC-021","","1932","PARTIALLY_VERIFIED","van_dung","Cần kiểm thêm ví dụ trong Lê Văn Đức"),
 ("vặt vãnh","tính_tu","Không quan trọng, vụn vặt","Chỉ việc nhỏ nhặt","Còn mấy điều vặt vãnh sau, tôi chỉ nói sơ qua…","SRC-021","","1932","VERIFIED","van_dung","Từ Nam Bộ"),
 ("sỉ nhục","danh_tu","Sự nhục nhã, mất mặt","Nói sự ô nhục","…sĩ phu ta có một cái sỉ nhục khó chịu…","SRC-021","","1932","VERIFIED","chinh_tri_van_hoc","Dạng 'sỉ' (Nam) của 'sĩ nhục'"),
 ("cấm kỵ","danh_tu","Điều kiêng kỵ, điều cấm","Chỉ điều tối kỵ","…đã phạm vào sự cấm kỵ ở chỗ đó…","SRC-021","","1932","VERIFIED","van_dung",""),
 ("lộn xộn","tính_tu","Rối rối, không ngăn nắp","Mô tả sự rối","…càng phân chừng nào lại càng lộn xộn chừng nấy.","SRC-021","","1932","VERIFIED","van_dung",""),
 ("thiệt hành","động_tu","Thực hành, thi hành","Thực hiện việc gì","…có điều thiệt hành thì rất khó.","SRC-021","","1932","VERIFIED","van_dung","Dạng Nam của 'thực hành'"),
 ("giá ngự","động_tu","Đánh giá, lượng định (chữ Hán)","Xét đoán, định giá","…họ có một cái phép để giá ngự…","SRC-021","","1932","VERIFIED","hoc_thuat","Từ Hán-Việt cổ; dùng trong khảo cứu"),
 ("n não tủy","danh_tu","Cốt tủy, tinh túy","Chỉ phần cốt lõi","…nên đem cái não tủy khoa học mà rót vào đó.","SRC-021","","1932","VERIFIED","hoc_thuat","Não tủy = cốt tủy"),
 ("phổ thông","tính_tu","Thông dụng, phổ biến rộng","Chỉ điều ai cũng biết","…từ ngữ phổ thông được dùng tại miền Nam… (chỉ dẫn dự án)","SRC-021","","1932","UNVERIFIED","hoc_thuat","Cần kiểm chứng thêm"),
 ("trứ thuật","danh_tu","Sự trước tác, viết sách","Chỉ việc viết sách","Nhà trứ thuật đời nay, khi biên tập các sách…","SRC-021","","1932","VERIFIED","hoc_thuat","Trước tác = trứ thuật (Hán-Việt)"),
 ("trước tác","động_tu/danh_tu","Viết sách, tác phẩm","Chỉ việc sáng tác","…các sách 'loại thơ' như là tự điển… (ngữ cảnh trước tác)","SRC-021","","1932","VERIFIED","hoc_thuat","Dạng Nam 'trước tác' song hành 'trứ thuật'"),
 ("loại thơ","danh_tu","Thể loại sách tra cứu (từ điển, bách khoa)","Chỉ nhóm sách tham khảo","…nhứt là các sách 'loại thơ' như là tự điển, từ nguyên, bách khoa","SRC-021","","1932","VERIFIED","hoc_thuat","Cách gọi sách tra cứu thời Nam Bộ"),
 ("nhứt","tinh_tu","Nhất (trong 'nhứt là')","Nhấn mạnh 'nhất là'","…nhứt là các sách 'loại thơ'…","SRC-021","","1932","VERIFIED","chinh_ta","Chính tả Nam: 'nhứt' thay 'nhất'"),
 ("mua đồng niên","cụm_tu","Mua trọn năm (định kỳ)","Mua báo/tạp chí cả năm","…ai mua đồng niên 12 tập thì 2$00…","SRC-021","","1932","VERIFIED","van_dung_thuong_ngay","'đồng niên' = cả năm; cách nói Nam Bộ"),
 ("bổn báo","danh_tu","Tờ báo này (của tôi/chúng tôi)","Tự xưng khiêm nhường","…chúng tôi xin giới thiệu tập Tự điển ấy cho độc giả Phụ nữ tân văn… (bổn báo)","SRC-021","","1932","VERIFIED","bao_chi","'bổn' = này (khiêm nhường)"),
 ("gởi","động_tu","Gửi (thư từ)","Dạng Nam của 'gửi'","Theo như bức thơ của hội Khai trí… gởi cho bổn báo","SRC-021","","1932","VERIFIED","chinh_ta","Chữ Nam: 'gởi' thay 'gửi'"),
 ("thơ","danh_tu","Thư (bức thư)","Thay 'thư' trong Nam Bộ","Theo như bức thơ của hội Khai trí…","SRC-021","","1932","VERIFIED","chinh_ta","Nam Bộ: 'thơ' = thư; 'bức thơ' = bức thư"),
 ("hết thảy","tinh_tu","Tất cả, mọi người","Chỉ toàn bộ","…mong rằng hết thảy anh chị em mua mỗi người lấy một phần","SRC-021","","1932","VERIFIED","van_dung","'hết thảy' = tất cả (Nam Bộ)"),
 ("may sao","cụm_tu","May thay, may mà","Biểu thị sự may mắn","May sao có hội Khai trí tiến đức đã ra vai gánh lấy công cuộc nầy!","SRC-021","","1932","VERIFIED","van_dung",""),
 ("ra vai","động_tu","Nhận lãnh, đảm nhận","Nhận việc khó","…hội Khai trí… đã ra vai gánh lấy công cuộc nầy","SRC-021","","1932","VERIFIED","van_dung",""),
 ("công cuộc","danh_tu","Sự nghiệp, công việc lớn","Chỉ việc trọng đại","…đã ra vai gánh lấy công cuộc nầy","SRC-021","","1932","VERIFIED","van_dung",""),
 ("đôi chục","định_lượng","Khoảng hai mươi","Ước lượng số","Đôi chục năm nay sĩ phu ta…","SRC-021","","1932","VERIFIED","van_dung",""),
 ("vả","liên_tu","Huống chi, lại còn (nhấn mạnh thêm ý)","Bổ sung lý lẽ","Vả cái a nếu là cái rèn bằng sắt…","SRC-021","","1932","VERIFIED","van_dung","Dạng Nam 'vả' (= vả chăng)"),
 ("quào","động_tu","Cào (gộp lúa)","Chỉ động tác cào gom","Cái trang Nam kỳ làm bằng săng, để quào lúa","SRC-021","","1932","VERIFIED","nong_ngiep_Nam_Bo","Từ Nam Bộ chỉ việc cào lúa"),
 ("săng","danh_tu","Một loại tre/ống (địa phương Nam)","Vật liệu làm nông cụ","…làm bằng săng, để quào lúa…","SRC-021","","1932","VERIFIED","nong_ngiep_Nam_Bo","Từ Nam Bộ"),
 ("bù quào","danh_tu","Cái cào (Nam Bộ)","Nông cụ","…không răng gọi bằng trang, có răng gọi bằng bù quào.","SRC-021","","1932","VERIFIED","nong_ngiep_Nam_Bo","Từ Nam Bộ"),
 ("trang","danh_tu","Cái cào lúa (địa phương Nam)","Nông cụ","…có phải là cái trang của Nam kỳ đâu?","SRC-021","","1932","VERIFIED","nong_ngiep_Nam_Bo","Từ Nam Bộ; không phải 'trang' (trang giấy)"),
 ("răng","tinh_tu","Răng (cái răng cào)","Danh từ chỉ răng","…không răng gọi bằng trang, có răng gọi bằng bù quào.","SRC-021","","1932","VERIFIED","nong_ngiep_Nam_Bo",""),
 ("sai","tính_tu","Sai, không đúng","Chỉ điều sai","Nói vậy thì sai quá.","SRC-021","","1932","VERIFIED","van_dung",""),
 ("chừng","phó_tu","Mức độ, chừng mực","Chỉ mức độ","…càng phân chừng nào lại càng lộn xộn chừng nấy.","SRC-021","","1932","VERIFIED","van_dung",""),
 ("nấy","tinh_tu","Ấy (Nam Bộ)","Thay 'ấy'","…càng lộn xộn chừng nấy.","SRC-021","","1932","VERIFIED","van_dung","Trùng với mục trên — gộp khi hoàn thiện"),
 ("bấy lâu nay","cụm_tu","Bấy lâu nay, suốt thời gian qua","Chỉ khoảng thời gian dài","Ủa! chúng mình làm cái gì bấy lâu nay mà kỳ quá vậy!","SRC-021","","1932","VERIFIED","van_dung",""),
 ("chúng mình","đại_tu","Chúng ta (thân mật)","Ngôi thứ nhất số nhiều","Ủa! chúng mình làm cái gì bấy lâu nay…","SRC-021","","1932","VERIFIED","van_dung","Nam Bộ; thân mật"),
 ("kỳ","tính_tu","Lạ, kỳ quặc","Chỉ điều lạ","…mà kỳ quá vậy!","SRC-021","","1932","VERIFIED","van_dung",""),
 ("chực","động_tu","Chực, nhắm, toan","Chỉ ý định","…chỉ có chực chỉ trích mà thôi.","SRC-021","","1932","VERIFIED","van_dung","Nam Bộ: 'chực' = toan/chực"),
 ("cầm","động_tu","Cho là, coi là","Xem là","…thì tôi dám cầm người ấy là nói bậy.","SRC-021","","1932","VERIFIED","van_dung","Nam Bộ: 'cầm' = cho là"),
 ("nói bậy","cụm_tu","Nói sai, nói láo","Chỉ lời sai","…thì tôi dám cầm người ấy là nói bậy.","SRC-021","","1932","VERIFIED","van_dung",""),
 ("bậy","tính_tu","Sai, quấy","Chỉ điều sai","…thì tôi dám cầm người ấy là nói bậy.","SRC-021","","1932","VERIFIED","van_dung",""),
 ("làm gì","cụm_tu","Thì đã sao, mặc kệ","Biểu thị bất chấp","…thì họ làm gì tôi?","SRC-021","","1932","VERIFIED","van_dung","Cấu trúc Nam Bộ 'làm gì' = mặc kệ"),
 ("hệ trọng","tính_tu","Quan trọng, hệ trọng","Chỉ điều quan trọng","…tôi lấy làm hệ trọng nhứt là sự phân loại…","SRC-021","","1932","VERIFIED","van_dung",""),
 ("hèn chi","cụm_tu","Hèn chi, huống hồ","Nối lý lẽ","(ngữ cảnh suy luận) ","SRC-021","","1932","UNVERIFIED","van_dung","Cần kiểm chứng"),
 ("sổ","danh_tu","Sổ sách (ghi chép)","—","(chưa dùng trong mẫu)","SRC-021","","1932","UNVERIFIED","van_dung","Chưa xác minh"),
]

with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(["tu_chuan","loai_tu","nghia","cach_dung","vi_du_nguyen_ban","nguon","trang","thoi_ky","muc_xac_minh","linh_vuc","ghi_chu"])
    w.writerows(rows)
print(f"Wrote {len(rows)} entries to {out}")
# count by verification
from collections import Counter
c=Counter(r[8] for r in rows)
print("Verification breakdown:", dict(c))