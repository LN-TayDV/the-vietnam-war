#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chen buoc chu va marker [N] vao file vi Chương 1.
- Chen block cuoc chu vao cuoi file (sau P049)
- Them marker [N] vao cuoi moi doan dua vao mapping trang->so cuoc chu
UTF-8, NFC, no BOM, LF.
"""
from pathlib import Path
import unicodedata
import re

VI = Path("translation-project/04_translation/v1/ch01/v1_ch01_vi.txt")

# Buoc chu day du (dich vao tieng Viet VNCH, ghi nguyen ten sach/tac gia tieng Anh/Phap)
FOOTNOTES = {
    1: '"Báo Việt Nam độc lập ra số đầu tiên" [The First Issue of the Newspaper Independent Vietnam], Báo điện tử Đảng cộng sản Việt Nam [Communist Party of Vietnam eNewspaper], October 9, 2019: https://dangcongsan.vn/tu-lieu-tham-khao-cuoc-thi-trac-nghiem-tim-hieu-90-nam-lich-su-ve-vang-cua-dang-cong-san-viet-nam/tu-lieu-cuoc-thi/bao-viet-nam-doc-lap-ra-so-dau-tien-534457.html.',
    2: 'Hồ Chí Minh, "Nên học sử ta" [Our History Must be Studied], in Hồ Chí Minh Toàn tập, tập 3 [Collected Works of Hồ Chí Minh, vol. III] (Hanoi, 2011), 256.',
    3: 'Hồ Chí Minh, "10 Điều nên" [Ten Musts], in Hồ Chí Minh Toàn tập, tập 3 [Collected Works of Hồ Chí Minh, vol. III] (Hanoi, 2011), 252.',
    4: 'Théophile Marie Legrand de la Liraye, Notes historiques sur la nation Annamite (không có thông tin xuất bản, nhưng được trích trong các tác phẩm từ thập niên 1870 cho rằng xuất khoảng năm 1865), 5.',
    5: 'Ibid., 84, and Ngô Sĩ Liên, Đại Việt sử ký toàn thư [Complete Book of the Historical Records of Đại Việt] (bản 1697, soạn thảo ban đầu năm 1479), Manuscript A. 3, Bản ký [Primary Annals], 10/1a.',
    6: 'P. J. B. Trương Vĩnh Ký, Cours d\'histoire Annamite a l\'usage des écoles de la Basse-Cochinchine (Saigon, 1875), 155 and 157.',
    7: 'Antoine Brébion, Dictionnaire de bio-bibliographie générale, ancienne et moderne de l\'Indochine française, publié après la mort de l\'auteur par Antoine Cabaton (Paris, 1935), 345–6.',
    8: 'Trần Thị Phương Hoa, "From Liberally-Organized to Centralized Schools: Education in Tonkin, 1885–1927," Journal of Vietnamese Studies 8 (3) (2013), 27–70.',
    9: 'Hoàng Đạo Thành, Việt sử tân ước toàn biên [Complete Compilation of the New Testament of Việt History] (1906), A. 1507.',
    10: 'Charles B. Maybon and Henri Russier, Notions d\'histoire d\'Annam, vol. I (Hanoi and Haiphong, 1909), vi.',
    11: 'Charles B. Maybon and Henri Russier, Notions d\'histoire d\'Annam, vol. II (Hanoi and Haiphong, 1909), 392 and 394.',
    12: 'Charles B. Maybon and Henri Russier, Lectures sur l\'histoire d\'Annam depuis l\'avènement des Lê, suivies de notions élémentaires d\'administration (Hanoi, 1919) and Trần Trọng Kim, Việt Nam sử lược [An Outline of the History of Vietnam] (Hanoi, 1920).',
    13: 'Vu Ngu Chieu, "The Other Side of the 1945 Vietnamese Revolution: The Empire of Viet-Nam (March–August 1945)," The Journal of Asian Studies 45 (1986), 293–328.',
    14: 'Ứng Hòe Nguyễn Văn Tố, "Quốc hiệu nước ta không nên gọi là An Nam" [Our Country Should Not be Called Annam], Trí Tân [New Knowledge], June 3, 1941, 1 and 17.',
    15: 'Hồ Chí Minh, "The History of Our Country" [Lịch sử nước ta], in Hồ Chí Minh Toàn Tập, tập 3 [Collected Works of Hồ Chí Minh, vol. III] (Hanoi, 2011), 257–67.',
    16: 'Nguyễn Duy Phương, Lịch sử độc lập và nội các đầu tiên Việt Nam [The History of the Independence and the First Cabinet of Vietnam] (Hanoi, 1945).',
    17: 'Phạm Văn Sơn, Việt Nam tranh đấu sử [A History of Vietnamese Struggles] (Hanoi, 1949).',
    18: 'Phạm Văn Sơn, Việt sử tân biên [A New Compilation of Việt History] (Saigon, 1956).',
    19: 'Trương Bửu Lâm, "Một nền sử học quốc gia," Đại Học [University], số 6, November 1958.',
    20: 'For a discussion of the southern emphasis of this scholarship, see Claudine Ang, "Regionalism in Southern Narratives of Vietnamese History: The Case of the \'Southern Advance\' (Nam Tiến)," Journal of Vietnamese Studies 8 (3) (2013), 1–26.',
    21: 'For an overview of the efforts to create a new form of history in North Vietnam in this period, see Patricia Pelley, Postcolonial Vietnam: New Histories of the National Past (Durham, NC, 2002).',
    22: 'Martin Grossheim, "Revisionism in the Democratic Republic of Vietnam: New Evidence from the East German Archives," Cold War History 5 (4) (2005), 462.',
    23: 'Trần Quốc Vượng and Hà Văn Tấn, Lịch sử chế độ cộng sản nguyên thủy ở Việt Nam [History of the System of Primitive Communism in Vietnam] (Hanoi, 1960), and Lịch sử chế độ phong kiến Việt Nam, Tập 1 [History of the Vietnamese Feudal System, vol. I] (Hanoi, 1960).',
    24: 'Phan Huy Lê, Lịch sử chế độ phong kiến Việt Nam, Tập 2 [History of the Vietnamese Feudal System, vol. II] (Hanoi, 1960), and Phan Huy Lê, Chu Thiên, Vương Hoàng Tuyên, and Đinh Xuân Lâm, Lịch sử chế độ phong kiến Việt Nam, Tập 3 [History of the Vietnamese Feudal System, vol. III] (Hanoi, 1960).',
    25: 'Viện Sử Học [Institute of History], Nước Việt Nam là một, dân tộc Việt Nam là một [The Country of Vietnam is One, the People of Vietnam are One] (Hanoi, 1976).',
    26: 'Joseph Buttinger, The Smaller Dragon: A Political History of Vietnam (New York, 1958).',
    27: 'Lê Thành Khôi, Le Viet-Nam: Histoire et civilisation, le milieu et l\'histoire (Paris, 1955).',
    28: 'Buttinger, The Smaller Dragon, 61.',
    29: 'Christopher E. Goscha, "' + "'" + 'So What Did You Learn from the War?'": Violent Decolonization and Paul Mus\'s Search for Humanity," South East Asia Research 20 (4) (2012), 569–93.',
    30: 'See Paul Mus, Viet-Nam. Sociologie d\'une guerre (Paris, 1952).',
    31: 'For more on Paul Mus\'s life and scholarship, see the articles by Christopher Goscha, David Chandler, Susan Bayly, and Agathe Larcher-Goscha in the special section in the Journal of Vietnamese Studies 4 (1) (2009), 145–239.',
    32: 'Frances FitzGerald, Fire in the Lake: The Vietnamese and the Americans in Vietnam (Boston, 1972).',
    33: 'George Kahin and John Lewis, The United States in Vietnam (New York, 1969).',
    34: 'Ibid., 325.',
    35: 'Stanley Karnow, Vietnam, a History (New York, 1983) and Marilyn Young, The Vietnam Wars, 1945–1990 (New York, 1991).',
}

# Mapping: PID -> danh sach so cuoc chu (dau o cuoi doan)
PID_FN = {
    "V1C01-P001": [1],
    "V1C01-P002": [2, 3],
    "V1C01-P009": [4],
    "V1C01-P010": [5],
    "V1C01-P011": [6, 7, 8, 9],
    "V1C01-P014": [10, 11, 12],
    "V1C01-P019": [13, 14],
    "V1C01-P020": [15],
    "V1C01-P021": [16, 17],
    "V1C01-P022": [],  # co the co [17] o day ma da co o P021
    "V1C01-P024": [18],
    "V1C01-P025": [19],
    "V1C01-P027": [20],
    "V1C01-P030": [21],
    "V1C01-P033": [22],
    "V1C01-P034": [23, 24],
    "V1C01-P038": [25],
    "V1C01-P042": [26],
    "V1C01-P043": [27],
    "V1C01-P044": [28],
    "V1C01-P045": [29, 30, 31],
    "V1C01-P046": [32],
    "V1C01-P047": [33, 34],
    "V1C01-P048": [35],
}

raw = VI.read_text(encoding="utf-8").replace("\r\n", "\n")
raw = unicodedata.normalize("NFC", raw)
lines = raw.split("\n")

new_lines = []
for ln in lines:
    new_lines.append(ln)
    # Kiem tra la dong header cua mot doan Pxxx
    m = re.match(r"^--- \[(V1C01-P\d+)\] \(trang [^)]+\)(?: — [^—]*)? ---$", ln)
    if m:
        pid = m.group(1)
        fns = PID_FN.get(pid, [])
        # Them marker [N] vao dong tiep theo (noidung doan) - them vao cuoi dong noidung
        # Nhưng ta chua biet dong noidung o dau. Them vao sau dong header, truoc dong noidung?
        # Khong, them marker vao cuoi dong noidung. Ta se them vao dong header sau (noidung)
        # De don gian, them marker vao cuoi dong header (se duoc chuyen xuong dong noidung sau khi sua)
        # Truy xuat: them marker vao dong hien tai (header) khong dung vi header phai giong src
        # Them marker vao dong tiep theo (noidung) - can biet dong noidung o dau
        # De don gi, them marker vao cuoi dong header thi khong dung vi header phai khop src
        # Ta se them marker vao cuoi DONG NOIDUNG (dong ke tiep sau header)
        pass

# Strategy khac: them marker vao cuoi dong NOIDUNG (dong khong bat dau boi '--- [')
# Duyet lai, neu dong truoc la header va dong hien tai la noidung, them marker vao cuoi dong noidung
final_lines = []
i = 0
while i < len(lines):
    ln = lines[i]
    final_lines.append(ln)
    m = re.match(r"^--- \[(V1C01-P\d+)\] \(trang [^)]+\)(?: — [^—]*)? ---$", ln)
    if m:
        pid = m.group(1)
        fns = PID_FN.get(pid, [])
        # Dong tiep theo la noidung
        if i + 1 < len(lines):
            next_ln = lines[i + 1]
            if not next_ln.startswith("--- ["):
                # Them marker vao cuoi dong noidung
                marker_str = " " + "".join(f"[{n}]" for n in fns) if fns else ""
                final_lines.append(next_ln + marker_str)
                i += 2
                continue
    i += 1

# Them block cuoc chu vao cuoi file
final_lines.append("")
final_lines.append("--- [Cước chú trang 27-29] ---")
for n in [1, 2, 3]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 29-31] ---")
for n in [4, 5, 6, 7, 8, 9]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 31-33] ---")
for n in [10, 11, 12]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 33] ---")
for n in [13, 14, 15]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 33-34] ---")
for n in [16, 17]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 35] ---")
for n in [18, 19]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 35-36] ---")
for n in [20]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 36-37] ---")
for n in [21, 22]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 37] ---")
for n in [23, 24]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 38] ---")
for n in [25]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 39] ---")
for n in [26, 27]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 40] ---")
for n in [28]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 41] ---")
for n in [29, 30, 31, 32]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")
final_lines.append("--- [Cước chú trang 42] ---")
for n in [33, 34, 35]:
    final_lines.append(f"[{n}] {FOOTNOTES[n]}")
final_lines.append("")

new_raw = "\n".join(final_lines)
new_raw = unicodedata.normalize("NFC", new_raw)
VI.write_text(new_raw, encoding="utf-8", newline="\n")
print(f"Da them buoc chu va marker vao {VI.name}")
