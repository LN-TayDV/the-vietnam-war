# -*- coding: utf-8 -*-
"""
Clean CJK (Han/Korean) and Cyrillic contamination in Vietnamese body text.
Each replacement is context-verified; proper nouns and intentional foreign
quotes are preserved. Idempotent.
"""
import re
import unicodedata as u

# Ordered list of (chapter, old, new). old must be exact substring.
REPL = {
    "ch01": [
        ("sự 촉促 có ý nghĩa", "sự thúc đẩy có ý nghĩa"),
        ("và卷入 vào nghiên cứu", "và lao vào nghiên cứu"),
        ("khủng bố甚至 không bị", "khủng bố thậm chí không bị"),
        ("bản 위造", "bản ngụy tạo"),
        ("và tất cả càng thêm天真因为他们的同化已经绕过",
         "và tất cả càng thêm rối rắm bởi sự đồng hóa của họ đã thấm sâu vào"),
        ("điều 당 nhiên", "điều đương nhiên"),
    ],
    "ch02": [
        ("bán thuốc chữa百病", "bán thuốc chữa bách bệnh"),
        ("để争取选票 của", "để giành lá phiếu của"),
        ("không còn là sự亵渎", "không còn là sự báng bổ"),
        ("khinh thường người Do Thái 당作当然而然",
         "khinh thường người Do Thái một cách đương nhiên"),
        ("thần职 Pháp", "thần chức Pháp"),
        ("bán tài sản thần职", "bán tài sản thần chức"),
        ("sự ủng hộ mạnh mẽ của thần职", "sự ủng hộ mạnh mẽ của thần chức"),
        ("chủ nghĩa chống thần职", "chủ nghĩa chống thần chức"),
        ("loại bỏ đồng胞公民", "loại bỏ đồng bào công dân"),
        ("với đồng胞公民 của họ", "với đồng bào công dân của họ"),
        ("các tiệm當铺", "các tiệm cầm đồ"),
        ("cửa hàng百货", "cửa hàng bách hóa"),
        ("những追求纯智力", "những truy cầu trí tuệ thuần túy"),
        ("người viết bài 評论", "người viết bài bình luận"),
        ("điều 당 nhiên", "điều đương nhiên"),
    ],
    "ch03": [
        ("nền Kitô giáo忘恩負義 này", "nền Kitô giáo vong ân bội nghĩa này"),
        ("Những chủ đề談 luận", "Những chủ đề đàm luận"),
        ("Những chủ đề谈 luận", "Những chủ đề đàm luận"),
        ("hoàn toàn dị質", "hoàn toàn dị chất"),
        ("họ tự觉采纳 Disraeli", "họ tự giác thu nạp niềm tin của Disraeli"),
        ("thảm họa cuối cùng降临 đến", "thảm họa cuối cùng giáng xuống"),
        ("sự kết黨 đó", "sự kết đảng đó"),
        ("sự kết党 đó", "sự kết đảng đó"),
        ("bằng sự kết党 xã hội", "bằng sự kết đảng xã hội"),
        ("nó确实 giải thích", "nó thực sự giải thích"),
        ("tuy vậy,既是 kết quả", "tuy vậy, vừa là kết quả"),
        ("vì,畢竟,", "vì, rốt cuộc,"),
        ("chưa接管 giấc mơ", "chưa tiếp quản giấc mơ"),
        ("việc b败 lộ", "việc bại lộ"),
        ("điều 당 nhiên", "điều đương nhiên"),
        ("chơi 궁금 bán ý thức", "trò chơi cờ bạc bán ý thức"),
        ("Hắn 본 năng biết", "Hắn bản năng biết"),
        ("chủng tộc không lai 섞", "chủng tộc không lai tạp"),
    ],
    "ch12": [
        ("và строго speaking là", "và nói một cách nghiêm ngặt là"),
        ("Kinh nghiệm và常识 thông thường", "Kinh nghiệm và lẽ thường thông thường"),
        ("và một常识 thông thường", "và một lẽ thường thông thường"),
        ("được preceded bởi", "được đi trước bởi"),
        ("việc 획득 một dạng", "việc giành được một dạng"),
    ],
}

# ch13 Cyrillic: page-number OCR garbage (isolated Cyrillic letters) -> remove
CH13_CYR = ["Ҡ", "Ӂ", "Ӄ", "ҟ", "ӂ"]


def clean_text(txt, repls):
    for old, new in repls:
        txt = txt.replace(old, new)
    return txt


def main():
    for ch, repls in REPL.items():
        path = f"04_translation/v2/{ch}/v1_{ch}_vi.txt"
        raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
        new = clean_text(raw, repls)
        if new != raw:
            new = u.normalize("NFC", new)
            open(path, "w", encoding="utf-8", newline="\n").write(new)
            print(f"OK {ch}: cleaned")
        else:
            print(f"-- {ch}: no change")
    # ch13 cyrillic
    path = "04_translation/v2/ch13/v1_ch13_vi.txt"
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    new = raw
    for c in CH13_CYR:
        new = new.replace(c, "")
    if new != raw:
        new = u.normalize("NFC", new)
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        print("OK ch13: removed cyrillic page artifacts")
    else:
        print("-- ch13: no change")


if __name__ == "__main__":
    main()