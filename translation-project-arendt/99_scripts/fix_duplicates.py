# -*- coding: utf-8 -*-
"""
Remediation: fix duplicate paragraphs (content loss) by restoring faithful
VNCH translations of the missing source paragraphs.

Each entry: (chapter, para_id_to_replace, source_para_id, vnch_translation)
The para_id_to_replace currently duplicates the PREVIOUS paragraph; we replace
it with a faithful translation of source_para_id's English content.

Traceability: source_para_id recorded in metadata comment header.
"""
import re
import sys
import unicodedata as u

ROOT = "."

# VNCH translations of the missing source paragraphs.
# Style matched to surrounding translation (academic VNCH, dense).
FIXES = {
    # ---------------- ch05 ----------------
    ("ch05", "V1C05-P007", "V1C05-P007"): (
        "Những phần nào của Đế quốc không được cư ngụ bởi những chủng tộc mà "
        "điều nầy là đúng, thì chưa bao giờ là đối tác trong công cuộc ấy. Chúng "
        "là tài sản riêng của đối tác chiếm ưu thế. . . . Ông có thể có nền thống "
        "trị của người da trắng, hoặc ông có thể có Dominion của Ấn Độ, nhưng "
        "ông không thể có cả hai.\" (Trích từ A. Carthill, The Lost Dominion, 1924.)"
    ),
    ("ch05", "V1C05-P020", "V1C05-P020"): (
        "\"Bởi họ chỉ bảo vệ đời sống của mình.\" Như vậy, tư cách thành viên "
        "trong bất kỳ hình thức cộng đồng nào, đối với Hobbes, là một công việc "
        "tạm thời và giới hạn, về căn bản không làm thay đổi tính cách đơn độc và "
        "riêng tư của cá nhân (kẻ \"không có niềm vui nào, mà trái lại, chỉ có "
        "nhiều buồn phiền to lớn trong việc giao du với người khác, nơi không có "
        "quyền lực nào để áp đảo tất cả\") cũng không tạo nên những mối dây liên "
        "kết vĩnh viễn giữa y với đồng loại của mình. Dường như bức tranh về con "
        "người của Hobbes đã đánh bại chính mục đích của ông là cung cấp cơ sở "
        "cho một Thịnh vượng chung, mà thay vào đó lại đưa ra một khuôn mẫu nhất "
        "quán về những thái độ mà qua đó mọi cộng đồng chân chính đều có thể dễ "
        "dàng bị phá hủy. Điều nầy dẫn đến sự bất ổn cố hữu và được thừa nhận "
        "của Thịnh vượng chung Hobbes, mà chính quan niệm của nó bao hàm sự tan "
        "rã của chính nó — \"khi trong một cuộc chiến (với ngoại quốc, hoặc nội "
        "bộ), kẻ thù giành được chiến thắng cuối cùng . . . thì Thịnh vượng chung "
        "tan rã, và mỗi người tự do bảo vệ mình\" — một sự bất ổn càng nổi bật "
        "hơn khi mục tiêu chính và thường được lặp lại của Hobbes là bảo đảm sự "
        "an toàn và ổn định tối đa. Sẽ là một sự bất công lớn đối với Hobbes và "
        "phẩm giá của ông với tư cách một nhà triết học nếu coi bức tranh về con "
        "người nầy là một nỗ lực nhằm hiện thực luận tâm lý hay chân lý triết "
        "học. Sự thật là Hobbes không quan tâm đến bất kỳ điều nào trong hai điều "
        "ấy, mà chỉ quan tâm độc quyền đến bản thân cấu trúc chánh trị, và ông mô "
        "tả những đặc điểm của con người theo nhu cầu của Leviathan. Vì mục đích "
        "lập luận và xác tín, ông trình bày phác thảo chánh trị của mình như thể "
        "ông khởi sự từ một sự thấu hiểu hiện thực về con người, một hữu thể "
        "\"khao khát quyền lực sau quyền lực,\" và như thể ông tiến từ sự thấu "
        "hiểu nầy đến một kế hoạch cho một thể chế chánh trị tốt nhất . . ."
    ),
    ("ch05", "V1C05-P025", "V1C05-P025"): (
        "\"Bởi Hobbes là một nhà triết học, nên ông đã có thể nhận ra ngay trong "
        "sự trỗi dậy của . . .\""
    ),
    # ---------------- ch06 ----------------
    ("ch06", "V1C06-P008", "V1C06-P008"): (
        "(một sự pha trộn) của mọi chủng tộc và mọi thời đại.\" Rõ ràng thời "
        "cuộc đã đổi thay và những nhà quý tộc không còn thuộc về một chủng tộc "
        "bất khả chinh phục thì cũng phải đổi thay. Họ từ bỏ quan niệm cũ, vốn "
        "rất đỗi thân thương với Boulainvilliers và ngay cả với Montesquieu, rằng "
        "riêng sự chinh phục, vận may của vũ khí, mới quyết định số phận của con "
        "người. Buổi Valmy của các ý thức hệ quý tộc đến khi vị-tu sĩ Sieyès, "
        "trong cuốn pamphlet trứ danh của ông, bảo Tầng lớp Thứ ba hãy \"trả "
        "lại vào rừng rậm Franconia tất cả những gia đình nào còn giữ cái tham "
        "vọng phi lý là mình descend du chủng tộc đi chinh phục và đã thừa kế "
        "quyền của họ.\" Thật khá kỳ lạ là từ những thời kỳ sớm nầy, khi các nhà "
        "quý tộc Pháp trong cuộc đấu tranh giai cấp chống lại giai cấp tư sản đã "
        "khám phá ra rằng họ thuộc về một dân tộc khác, có một nguồn gốc phả hệ "
        "khác, và gắn bó mật thiết hơn với một đẳng cấp quốc tế so với mảnh đất "
        "của Pháp, thì mọi thuyết chủng tộc Pháp đều đã ủng hộ thuyết Germanism "
        "hay ít nhất là ưu thế của các dân tộc Nordic so với chính đồng bào của "
        "họ. Bởi nếu những người của Cách mạng Pháp đã đồng nhất mình về mặt tinh "
        "thần với Rome, thì không phải vì họ đối lập một \"Latinism\" của Tầng "
        "lớp Thứ ba với \"Germanism\" của giới quý tộc mình, mà bởi họ cảm thấy "
        "mình là những kẻ thừa kế tinh thần của các nhà Cộng hòa La Mã. Yêu sách "
        "lịch sử nầy, trái với sự đồng nhất bộ lạc của giới quý tộc, có lẽ đã là "
        "một trong những nguyên nhân ngăn \"Latinism\" trỗi dậy như một thuyết "
        "chủng tộc riêng của nó. Dù sao đi nữa, nghe qua thì có vẻ nghịch lý, "
        "nhưng sự thật là người Pháp đã khăng khăng sớm hơn người Đức . . ."
    ),
    ("ch06", "V1C06-P026", "V1C06-P026"): (
        "Dilke, Greater Britain.\" Xem \"Two Lectures on South Africa,\" trong "
        "Short Studies on Great Subjects, 1867-1881. C. A. Bodelsen, op. cit., "
        "tr. 199."
    ),
    # ---------------- ch07 ----------------
    ("ch07", "V1C07-P017", "V1C07-P017"): (
        "\"Điều nầy cho thấy Bamalo đã sai lầm đến mức nào khi ông ta nghĩ rằng "
        "\"nếu tôi đã được thụ hưởng nền giáo dục của Cecil Rhodes thì đã không "
        "có một Cecil Rhodes\" (ibid.).\""
    ),
    ("ch07", "V1C07-P025", "V1C07-P025"): (
        "Trong một thế hệ đã chứng kiến nước Anh từ bỏ mậu dịch tự do, nước Mỹ "
        "rời bỏ bản vị vàng, Đệ tam Đế chế ôm ấp chế độ tự cung tự cấp . . . thì "
        "sự khăng khăng của Nam Phi rằng đời sống kinh tế của nó phải được tổ "
        "chức để bảo đảm địa vị thống trị của chủng tộc da trắng không phải là "
        "điều gì thực sự lạc lõng\" (Kiewiet, op. cit., tr. 224 và 245)."
    ),
    # ---------------- ch10 ----------------
    ("ch10", "V1C10-P006", "V1C10-P006"): (
        "\"(Goebbels Diaries, tr. 355). — Ước lượng nầy dựa trên những cân nhắc "
        "ý thức hệ, chứ không phải quân sự. Gottfried Neesse, Partei und Staat, "
        "1936, đã đưa ra phiên bản chính thức về cuộc đấu tranh giành quyền lực "
        "của phong trào khi ông viết: \"Đối với chúng ta, mặt trận thống nhất của "
        "hệ thống trải dài từ Đảng Nhân dân Quốc gia Đức [tức là cực Hữu] đến "
        "các Dân chủ Xã hội. Đảng Cộng sản là một kẻ thù bên ngoài hệ thống. Do "
        "đó, trong những tháng đầu năm 1933, khi số phận của hệ thống đã được "
        "định đoạt, chúng ta vẫn còn phải tiến hành một trận chiến quyết định "
        "chống lại Đảng Cộng sản\" (tr. 76). Xem Hitler's Tischgespräche, tr. "
        "113. Ở đó cũng có thể tìm thấy nhiều thí dụ cho thấy rằng, trái với một "
        "số truyền thuyết hậu chiến, Hitler chưa bao giờ có ý định bảo vệ \"phương "
        "Tây\" chống lại chủ nghĩa Bolshevik, mà luôn sẵn sàng sát cánh với \"những "
        "kẻ Đỏ\" để hủy diệt phương Tây, ngay cả giữa cuộc chiến chống lại nước "
        "Nga Xô-viết. Xem đặc biệt các tr. 95, 108, 113 và tiếp theo, 158, 385."
    ),
    # ---------------- ch11 ----------------
    ("ch11", "V1C11-P012", "V1C11-P012"): (
        "\"để đánh. (Hitler's Speeches: 1922-1939, do Baynes biên tập, London, "
        "1942, tr. 29.) Đáng chú ý là chưa từng có một tuyển tập đầy đủ các bài "
        "diễn văn của Hitler được xuất bản tại Đức Quốc xã, đến nỗi người ta buộc "
        "phải viện đến ấn bản tiếng Anh. Rằng điều nầy không phải là ngẫu nhiên "
        "có thể thấy từ một thư mục do Philipp Bouhler biên soạn, Die Reden des "
        "Führers nach der Machtübernahme, 1940: chỉ những bài diễn văn công khai "
        "mới được in nguyên văn trong Völkischer Beobachter; còn các bài diễn văn "
        "trước Fuehrerkorps và các đơn vị đảng khác thì chỉ được \"đề cập đến\" "
        "trong tờ báo ấy. Chúng chưa bao giờ được dự định để xuất bản. \"Những 25 "
        "điểm\" của Feller chỉ chứa những biện pháp tiêu chuẩn mà mọi đảng bài Do "
        "Thái đều viện đến . . ."
    ),
    # ---------------- ch03 (non-consecutive: P014 duplicates P035) ----------------
    ("ch03", "V1C03-P014", "V1C03-P014"): (
        "Đặc quyền cá nhân. Một điều là chắc chắn: nếu người ta muốn tránh mọi "
        "sự nhập nhằng của hiện hữu xã hội, thì phải cam chịu với sự kiện rằng "
        "là một người Do Thái có nghĩa là hoặc thuộc về một giai cấp trên được "
        "đặc quyền quá mức, hoặc thuộc về một đám đông bị tước quyền, mà ở Tây "
        "và Trung Âu, người ta chỉ có thể thuộc về đám đông ấy qua một tình đoàn "
        "kết trí thức và phần nào giả tạo. Số phận xã hội của những người Do Thái "
        "bình thường được định đoạt bởi sự thiếu quyết đoán muôn thuở của họ. Và "
        "xã hội chắc chắn đã không bắt buộc họ phải dứt khoát, bởi chính sự nhập "
        "nhằng nầy về hoàn cảnh và tính cách mới làm cho mối quan hệ với người Do "
        "Thái trở nên hấp dẫn. Phần lớn những người Do Thái đã đồng hóa do đó "
        "sống trong một vùng tranh tối tranh sáng của ân huệ và bất hạnh, và chỉ "
        "biết chắc một điều rằng cả thành công lẫn thất bại đều gắn chặt không "
        "thể tách rời với sự kiện họ là người Do Thái. Đối với họ, vấn đề Do Thái "
        "đã mất đi, một lần cho mãi mãi, mọi ý nghĩa chánh trị; nhưng nó ám ảnh "
        "đời sống riêng tư của họ và chi phối những quyết định cá nhân của họ "
        "một cách càng độc đoán hơn. Cách nói \"một người ngoài đường và một "
        "người Do Thái ở nhà\" đã được hiện thực hóa một cách cay đắng: những vấn "
        "đề chánh trị bị bóp méo đến mức hoàn toàn đồi bại khi người Do Thái cố "
        "giải quyết chúng bằng kinh nghiệm nội tâm và cảm xúc riêng tư; đời sống "
        "riêng tư bị đầu độc đến mức phi nhân — thí dụ trong vấn đề hôn nhân hỗn "
        "hợp — khi gánh nặng nặng nề của những vấn đề công cộng chưa được giải "
        "quyết bị nhồi nhét vào cái hiện hữu riêng tư vốn được cai trị tốt hơn "
        "nhiều bởi những định luật bất khả đoán của dục vọng hơn là bởi những "
        "chánh sách được cân nhắc. Thật không dễ chút nào để không giống \"người "
        "Do Thái nói chung\" mà vẫn là một người Do Thái; để giả vờ không giống "
        "người Do Thái mà vẫn cho thấy đủ rõ ràng rằng mình là người Do Thái. "
        "Người Do Thái bình thường, không phải kẻ trọc phú cũng không phải \"kẻ "
        "cùng đinh có ý thức\" (Bernard Lazare), chỉ có thể nhấn mạnh một cảm "
        "giác trống rỗng về sự khác biệt, mà cảm giác ấy tiếp tục bị diễn giải, "
        "với mọi khía cạnh tâm lý khả dĩ và những biến thể từ sự xa lạ bẩm sinh "
        "đến xã hội . . ."
    ),
}


def replace_para(path, para_id, new_text):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    # Find the para header and replace text up to next header or FOOTNOTES
    pat = re.compile(
        r"(^\[" + re.escape(para_id) + r"\] \(trang \d+\)\s*\n)(.*?)(?=^\[V1\w*-?C\d+-P\d{3}\] \(trang \d+\)|\Z|^=== FOOTNOTES ===)",
        re.S | re.M,
    )
    m = pat.search(raw)
    if not m:
        raise RuntimeError(f"para {para_id} not found in {path}")
    new_block = m.group(1) + new_text.strip() + "\n\n"
    out = raw[: m.start()] + new_block + raw[m.end():]
    out = u.normalize("NFC", out)
    open(path, "w", encoding="utf-8", newline="\n").write(out)
    return True


def main():
    # group fixes by chapter
    from collections import defaultdict
    bychap = defaultdict(list)
    for (ch, pid, srcid), txt in FIXES.items():
        bychap[ch].append((pid, srcid, txt))
    for ch, items in bychap.items():
        path = f"04_translation/v2/{ch}/v1_{ch}_vi.txt"
        for pid, srcid, txt in items:
            replace_para(path, pid, txt)
            print(f"OK {ch} {pid} <- translated from src {srcid}")
    print("DONE")


if __name__ == "__main__":
    main()