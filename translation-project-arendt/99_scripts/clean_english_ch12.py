# -*- coding: utf-8 -*-
"""Translate leftover English fragments in ch12 (and ch13) body to VNCH Vietnamese.
Phrase-level replacements, context-verified. Idempotent."""
import unicodedata as u

CH12 = [
    ("apparently unrelated và uncon-nected", "rõ ràng không liên quan và rời rạc"),
    ("apparently không ở trong vị trí", "có vẻ không ở trong vị trí"),
    ("ông apparently làm điều", "ông có vẻ làm điều"),
    ("Hitler apparently không bao giờ", "Hitler có vẻ không bao giờ"),
    ("presumably đã quyết định", "có lẽ đã quyết định"),
    ("presumably còn không nghi ngờ", "có lẽ còn không nghi ngờ"),
    ("presumably đang rack their brains", "có lẽ đang vắt óc"),
    ("còn exclusively hơn cho quan sát", "còn riêng biệt hơn cho quan sát"),
    ("bị frightened exclusively bởi", "chỉ bị sợ hãi bởi"),
    ("altogether khác biệt", "hoàn toàn khác biệt"),
    ("altogether chỉ là một incitement nữa để throw", "hoàn toàn chỉ là một sự xúi giục nữa để tung ra"),
    ("một hiến pháp entirely mới", "một hiến pháp hoàn toàn mới"),
    ("cho điều entirely khác", "cho điều hoàn toàn khác"),
    ("hiến pháp turns out là", "hiến pháp hóa ra là"),
    ("turns out to be một công cụ ideally suited", "hóa ra là một công cụ lý tưởng phù hợp"),
    ("không bao giờ bị repudiated", "không bao giờ bị bác bỏ"),
    ("để circumscribe các trách nhiệm", "để khoanh vùng các trách nhiệm"),
    ("để counter \"sự vô chính phủ", "để chống lại \"sự vô chính phủ"),
    ("sẽ powerful hơn counterpart", "sẽ mạnh hơn đối tác"),
    ("có counterpart trong các mạng lưới", "có đối tác trong các mạng lưới"),
    ("không bao giờ có thể absolutely sure", "không bao giờ có thể hoàn toàn chắc chắn"),
    ("absolutely essential cho functioning", "hoàn toàn thiết yếu cho hoạt động"),
    ("Viện Munich consequently bị", "Viện Munich do đó bị"),
    ("duy nhất là eventually một trong", "duy nhất là rốt cuộc một trong"),
    ("biết considerably less về", "biết ít hơn đáng kể về"),
    ("Quân đội Đỏ được làm autonomous", "Quân đội Đỏ được làm cho tự trị"),
    ("taken as seriously và as literally", "được xem nghiêm túc và theo nghĩa đen"),
    ("và act accordingly", "và hành động tương ứng"),
    ("totalitarian solely như một công cụ", "totalitarian chỉ như một công cụ"),
    ("hay induce họ từ bỏ", "hay thúc họ từ bỏ"),
    ("một sự thật induce nhiều người", "một sự thật thúc đẩy nhiều người"),
    ("sự kỹ lưỡng fantastique", "sự kỹ lưỡng phi thường"),
    ("lời tuyên thệ có giuramento của Rudolf Diels", "lời tuyên thệ của Rudolf Diels"),
    ("hiểu được điều stakes thực sự là gì", "hiểu được điều thực sự bị đe dọa là gì"),
    ("bác bỏ mọi contend rằng", "bác bỏ mọi lập luận rằng"),
    ("trở nên steadily khó duy trì", "trở nên ngày càng khó duy trì"),
    ("đã solidly lined up against them", "đã đoàn kết vững chắc chống lại họ"),
    ("không kể revolutionary về nội dung", "không kể mang tính cách mạng về nội dung"),
    ("bọn Nazi để loose một avalanche", "bọn Nazi để tuôn ra một thác lũ"),
    ("quan tâm nào whatsoever về", "quan tâm nào cả về"),
    ("không manner nào được bao phủ", "không cách nào được bao phủ"),
    ("sự pacification của đất nước", "sự bình định của đất nước"),
    ("như có thể gather từ các thủ tục", "như có thể thu thập từ các thủ tục"),
    ("đã trở thành definitely stateless", "đã trở thành hoàn toàn không quốc tịch"),
    ("một settlement comparatively permanent", "một sự định chế tương đối lâu dài"),
    ("và uncon-nected tại Nga", "và rời rạc tại Nga"),
    ("của phong trào, absolutely", "của phong trào, hoàn toàn"),
]

CH13 = [
    ("counter", "chống lại"),
    ("control", "kiểm soát"),
    ("settlement", "sự định chế"),
    ("revolutionary", "cách mạng"),
]


def apply(path, repls):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    new = raw
    for o, n in repls:
        new = new.replace(o, n)
    if new != raw:
        open(path, "w", encoding="utf-8", newline="\n").write(u.normalize("NFC", new))
        return True
    return False


print("ch12:", apply("04_translation/v2/ch12/v1_ch12_vi.txt", CH12))
print("ch13:", apply("04_translation/v2/ch13/v1_ch13_vi.txt", CH13))