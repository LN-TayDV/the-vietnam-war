# -*- coding: utf-8 -*-
"""
Translate foreign language remnants in v2 chapter files to VNCH pre-1975 Vietnamese.
- German phrases → VNCH
- French phrases → VNCH
- Latin phrases → VNCH
- English words/phrases → VNCH
- Keep proper nouns/book titles in original language (italicized)
- Fix OCR artifacts: Pan-Xlaven→Pan-Xlavơ, Pan-Duc→Pan-Dức
- Idempotent; outputs a change report
"""
import re
import unicodedata
from pathlib import Path
from typing import List, Tuple, Dict

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "04_translation" / "v2"

# ============================================================
# Translation mappings: (pattern, replacement, description)
# Patterns are exact strings or regex for context-sensitive replacement
# ============================================================

# German → VNCH
GERMAN_TRANSLATIONS = [
    # ch02 P029 - extensive German paragraph
    ("Nirgends hatten die Juden dem Staat so große Dienste geleistet wie in Österreich, dessen viele Nationalitäten nur durch die Doppelfronarchie des Hauses Habsburg zusammengehalten wurden, und wo der jüdische Staatsbankier, im Gegensatz zu allen anderen europäischen Ländern, den Untergang der Monarchie überlebte.",
     "Nirgends người Do Thái đã đóng góp cho nhà nước to lớn như ở Áo, nơi nhiều quốc tịch của nó chỉ được giữ chung bởi chế độ song vương triều của nhà Habsburg, và nơi ngân gia nhà nước người Do Thái, trái ngược với tất cả các nước Châu Âu khác, đã sống sót qua sự sụp đổ của vương triều.",
     "ch02 P029: German paragraph about Jews in Austria"),

    ("Genau wie zu Beginn dieser Entwicklung im frühen achtzehnten Jahrhundert Samuel Oppenheimers Kredit identisch war mit dem Kredit des Hauses Habsburg, so war \"am Ende der österreichische Kredit der der Creditanstalt\" — eines Rothschild-Bankhauses.",
     "Chính xác như ở khởi đầu phát triển này vào đầu thế kỷ mười tám, uy tín của Samuel Oppenheimer trùng hợp với uy tín của nhà Habsburg, thì \"cuối cùng uy tín Áo là uy tín của Creditanstalt\" — một ngân hàng của gia tộc Rothschild.",
     "ch02 P029: German paragraph about Oppenheimer/Rothschild"),

    ("Diew die Donautonarchie keine homogene Bevölkerung hatte, die wichtigste Voraussetzung für die Entwicklung zum Nationalstaat, konnte sie die Verwandlung eines aufgeklärten Despotismus in eine konstitutionelle Monarchie und die Schaffung moderner Beamtenapparate nicht vermeiden.",
     "Vì chế độ Danube không có dân cư đồng nhất, tiền đề quan trọng nhất để phát triển thành dân tộc quốc gia, nó không thể tránh khỏi việc biến đổi từ một chuyên chế khai sáng thành một quân chủ lập hiến và sự tạo ra bộ máy quan liêu hiện đại.",
     "ch02 P029: German paragraph about Danube monarchy"),

    ("Zum einen wuchs das moderne Klassensystem entlang der Nationalitätenlinien, sodass bestimmte Nationalitäten begannen, sich mit bestimmten Klassen oder zumindest Berufen zu identifizieren.",
     "Thứ nhất, hệ thống giai cấp hiện đại phát triển dọc theo đường phân chia quốc tịch, khiến một số quốc tịch bắt đầu gắn liền với những giai cấp nhất định hoặc ít nhất là những nghề nghiệp.",
     "ch02 P029: German paragraph about class system"),

    ("Die Deutschen wurden zur dominierenden Nationalität in sehr ähnlichem Sinne, wie das Bürgertum zur dominierenden Klasse in den Nationalstaaten wurde.",
     "Người Đức trở thành quốc tịch thống trị theo ý nghĩa rất tương tự như giai cấp tư sản trở thành giai cấp thống trị trong các dân tộc quốc gia.",
     "ch02 P029: German paragraph about Germans as dominant nationality"),

    ("Der ungarische Grossgrundbesitzadel chơi một vai trò, còn nổi bật hơn, nhưng về cơ bản tương tự như vai trò của quý tộc trong các nước khác.",
     "Quý tộc địa chủ lớn Hungari chơi một vai trò, còn nổi bật hơn, nhưng về cơ bản tương tự như vai trò của quý tộc trong các nước khác.",
     "ch02 P029: German mixed with VNCH"),

    # ch10 - German phrases
    ("Partei und Staat", "Đảng và Nhà nước", "ch10: German 'Partei und Staat'"),
    ("Gottfried Neesse", "Gottfried Neesse", "ch10: Proper name - keep"),

    # ch11 - German phrases
    ("Fuehrer", "Führer", "ch11: German 'Fuehrer' -> Führer (keep original German spelling)"),
    ("Völkischer Beobachter", "Völkischer Beobachter", "ch11: Newspaper name - keep original"),
    ("Fuehrerkorps", "Führerkorps", "ch11: German 'Fuehrerkorps' -> Führerkorps"),
    ("Die Reden des Führers", "Die Reden des Führers", "ch11: Book title - keep original"),
    ("Volk im Werden", "Volk im Werden", "ch11: Publication name - keep original"),

    # ch08 - OCR artifacts
    ("Pan-Xlaven", "Pan-Xlavơ", "ch08: OCR artifact Pan-Xlaven -> Pan-Xlavơ"),
    ("Pan-Duc", "Pan-Dức", "ch08: OCR artifact Pan-Duc -> Pan-Dức"),
]

# French → VNCH
FRENCH_TRANSLATIONS = [
    # ch03
    ("la capitale du dixneuvieme siecle", "thủ đô của thế kỷ mười chín (Walter Benjamin)", "ch03: French 'la capitale du dixneuvieme siecle'"),
    ("Sodome et Ghomorre", "Sô-dôm và Gô-mô-rơ", "ch03: French 'Sodome et Ghomorre'"),
    ("par excellence", "điển hình", "ch03: French 'par excellence'"),
    ("le plebiscite de tous les jours", "cuộc trưng cầu dân ý hàng ngày", "ch05: French 'le plebiscite de tous les jours'"),

    # ch04
    ("bordereau", "bản liệt kê (bordereau)", "ch04: French 'bordereau'"),
    ("Une erreur judiciaire", "Một sai lầm tư pháp", "ch04: French 'Une erreur judiciaire'"),
    ("L'Accuse", "Lời Kiện Cáo (L'Accuse)", "ch04: French 'L'Accuse' (Zola's article)"),
    ("Action Française", "Hành Động Pháp Lan (Action Française)", "ch04: Organization name"),
    ("Précis de l'Affaire Dreyfus", "Tóm Tắt Vụ Án Dreyfus (Précis de l'Affaire Dreyfus)", "ch04: Book title"),
    ("La Voix du Nord", "Giọng Nói Của Phương Bắc (La Voix du Nord)", "ch04: Newspaper"),
    ("Libre Parole", "Lời Nói Tự Do (Libre Parole)", "ch04: Newspaper"),

    # ch06
    ("La Philosophie", "Triết Học (La Philosophie)", "ch06: French 'La Philosophie'"),
    ("La raison est de tous les climats.", "Lý trí thuộc về mọi khí hậu.", "ch06: French 'La raison est de tous les climats.'"),
    ("fortune des armes", "vận mệnh của vũ lực / may mắn chiến đấu", "ch06: French 'fortune des armes'"),
    ("Tiers Etat", "Thân Phân Thứ Ba (Tiers État)", "ch06: French 'Tiers Etat'"),
    ("Gallo-Romain", "Ga-Lô-La Mã (Gallo-Romain)", "ch06: French 'Gallo-Romain'"),
    ("les neiges d'antan", "những tuyết xưa (les neiges d'antan)", "ch06: French 'les neiges d'antan' (Villon)"),

    # ch07
    ("affranchissement", "giải phóng (affranchissement)", "ch07: French 'affranchissement'"),
    ("Tiers Etat", "Thân Phân Thứ Ba (Tiers État)", "ch07: French 'Tiers Etat'"),

    # ch09
    ("apatride", "vô quốc tịch (apatride)", "ch09: French 'apatride'"),
    ("de nationalité indéterminée", "có quốc tịch không xác định", "ch09: French 'de nationalité indéterminée'"),
]

# Latin → VNCH
LATIN_TRANSLATIONS = [
    # ch03
    ("apologia pro vita sua", "bài biện minh cho cuộc đời mình (apologia pro vita sua)", "ch03: Latin 'apologia pro vita sua'"),
    ("tr\\. ²⁹260 tt\\.", "tr. 260 (chú thích 29)", "ch03: garbled footnote reference"),

    # ch05
    ("ius", "quyền / luật (ius)", "ch05: Latin 'ius'"),
    ("imperium", "quyền lực / đế quốc (imperium)", "ch05: Latin 'imperium'"),
    ("force noire", "lực lượng đen (force noire - French)", "ch05: French 'force noire'"),
    ("dominion", "lãnh địa tự trị (dominion - English)", "ch05: English 'dominion'"),

    # ch06
    ("primus inter pares", "thứ nhất trong số các đẳng cấp (primus inter pares)", "ch06: Latin 'primus inter pares'"),
    ("Ethics", "Luận Khí Chất (Ethics - Spinoza)", "ch06: Book title - keep original"),
    ("Latinism", "Latinism (từ Latinh)", "ch06: English 'Latinism'"),
    ("Germanism", "Germanism (từ Đức)", "ch06: English 'Germanism'"),
    ("descend du chủng tộc", "xuất thân từ chủng tộc", "ch06: Mixed French/VNCH"),

    # ch13
    ("Initium ut esset homo creatus est", "Để con người được tạo ra phải có một sự khởi đầu (Initium ut esset homo creatus est)", "ch13: Latin 'Initium ut esset homo creatus est' (Augustine)"),
    ("consensus iuris", "sự đồng thuận về pháp lý (consensus iuris)", "ch13: Latin 'consensus iuris'"),
]

# English → VNCH (narrative words, not proper nouns)
ENGLISH_TRANSLATIONS = [
    # ch01
    ("con substitutions", "lý thuyết con substitutions (thay thế)", "ch01: English 'con substitutions'"),

    # ch02
    ("Christian-Socials", "Cơ Đốc-Xã Hội (Christian-Socials)", "ch02: Party name"),
    ("Social Democrats", "Xã Hội Dân Chủ (Social Democrats)", "ch02: Party name"),
    ("Pan-Germanist (Pan-Đức)", "Pan-Germanist (Pan-Đức)", "ch02: Already has VNCH gloss"),
    ("Pan-Slav", "Pan-Xlavơ", "ch02: Pan-Slav -> VNCH Pan-Xlavơ"),
    ("Pan-Deutsch", "Pan-Đức", "ch02: Pan-Deutsch -> VNCH Pan-Đức"),

    # ch03
    ("Remembrance of Things Past", "Tìm Kiếm Thời Gian Đã Mất (Remembrance of Things Past)", "ch03: Book title - Proust"),
    ("pariah", "bàng nhân / người bị đày (pariah)", "ch03: English 'pariah'"),

    # ch05
    ("Ostafrikanische Gesellschaft", "Công Ty Đông Phi (Ostafrikanische Gesellschaft)", "ch05: German company name"),
    ("Leviathan", "Lê-vi-a-than (Leviathan - Hobbes)", "ch05: Book title"),

    # ch07
    ("Heart of Darkness", "Trái Tim Bóng Tối (Heart of Darkness - Conrad)", "ch07: Book title"),
    ("Mr. Kurtz", "Ông Kurtz", "ch07: Character name"),
    ("Mr. Heyst", "Ông Heyst", "ch07: Character name"),

    # ch08
    ("Slavophile", "Người Yêu Nga (Slavophile)", "ch08: English 'Slavophile'"),
    ("Hapsburg", "Habsburg (Hapsburg)", "ch08: Dynasty name"),
    ("corpus separatum", "thực thể riêng biệt (corpus separatum)", "ch08: Latin legal term"),

    # ch09
    ("Hit-lê", "Hit-lê", "ch09: VNCH transliteration - keep"),
    ("DP", "người tị nạn (DP - Displaced Persons)", "ch09: English abbreviation"),
    ("Heimatlosen", "người mất quê hương (Heimatlosen - German)", "ch09: German 'Heimatlosen'"),

    # ch10
    ("Goebbels Diaries", "Nhật Ký Goebbels (Goebbels Diaries)", "ch10: Book title"),
    ("Hitler's Tischgespräche", "Cuộc Trò Chuyện Bàn Ăn Của Hitler (Hitler's Tischgespräche)", "ch10: Book title"),
    ("Untermenschen", "người dưới loài (Untermenschen)", "ch10: German 'Untermenschen'"),

    # ch11
    ("Protocols of the Elders of Zion", "Giao Thức Của Các Trưởng Lão Do Thái (Protocols of the Elders of Zion)", "ch11: Book title"),
    ("Hitler's Speeches", "Các Bài Phát Biểu Của Hitler (Hitler's Speeches)", "ch11: Book title"),

    # ch12
    ("totalitarian", "toàn trị", "ch12: English 'totalitarian' -> VNCH 'toàn trị'"),
    ("TOTALITARIANISM IN POWER", "TOÀN TRỊ TẠI QUYỀN", "ch12: Running header - English"),
    ("CHAPTER TWELVE :", "CHƯƠNG MƯỜI HAI :", "ch12: Chapter header - English"),

    # ch13
    ("Bibliography", "Tài Liệu Tham Khảo", "ch13: Section header"),
    ("Part One: Antisemitism", "Phần Một: Chủ Nghĩa Bài Do Thái", "ch13: Section header"),
    ("Part Two: Imperialism", "Phần Hai: Chủ Nghĩa Đế Quốc", "ch13: Section header"),
    ("Part Three: Totalitarianism", "Phần Ba: Chủ Nghĩa Toàn Trị", "ch13: Section header"),
]

# Combined all translations
ALL_TRANSLATIONS = (
    GERMAN_TRANSLATIONS +
    FRENCH_TRANSLATIONS +
    LATIN_TRANSLATIONS +
    ENGLISH_TRANSLATIONS
)


def apply_translations(text: str, translations: List[Tuple[str, str, str]], chapter: str) -> Tuple[str, List[str]]:
    """Apply translations to body text only (not FOOTNOTES block). Returns (new_text, changes)."""
    body_part, sep, fn_part = text.partition("=== FOOTNOTES ===")
    changes = []

    for pattern, replacement, desc in translations:
        # Only apply if pattern exists in body
        if pattern in body_part:
            # Count occurrences
            count = body_part.count(pattern)
            body_part = body_part.replace(pattern, replacement)
            if count > 0:
                changes.append(f"{chapter}: {desc} ({count} occurrence{'s' if count > 1 else ''})")

    new_text = body_part + sep + fn_part
    return new_text, changes


def process_chapter(ch: str) -> List[str]:
    """Process a single chapter file. Returns list of changes made."""
    path = V2 / ch / f"v1_{ch}_vi.txt"
    if not path.exists():
        return [f"SKIP {ch}: file not found"]

    raw = path.read_text(encoding="utf-8")
    raw = raw.replace("\r\n", "\n")

    # Filter translations relevant to this chapter
    relevant = [(p, r, d) for p, r, d in ALL_TRANSLATIONS if d.startswith(f"{ch}:")]

    new_text, changes = apply_translations(raw, relevant, ch)

    # Also apply any remaining general translations that might appear
    # (e.g., "totalitarian" appears throughout ch12)
    general_translations = [
        ("totalitarian", "toàn trị", "general: totalitarian -> toàn trị"),
        ("Pan-Xlaven", "Pan-Xlavơ", "general: Pan-Xlaven -> Pan-Xlavơ"),
        ("Pan-Duc", "Pan-Dức", "general: Pan-Duc -> Pan-Dức"),
    ]
    for pattern, replacement, desc in general_translations:
        if pattern in new_text and not any(d.startswith(f"{ch}:") and pattern in d for _, _, d in relevant):
            count = new_text.count(pattern)
            if count > 0:
                new_text = new_text.replace(pattern, replacement)
                changes.append(f"{ch}: {desc} ({count} occurrence{'s' if count > 1 else ''})")

    new_text = unicodedata.normalize("NFC", new_text)

    if new_text != raw:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        changes.append(f"{ch}: FILE UPDATED")
    else:
        changes.append(f"{ch}: no changes")

    return changes


def main():
    chapters = [f"ch{i:02d}" for i in range(1, 14)]
    all_changes = []

    for ch in chapters:
        changes = process_chapter(ch)
        all_changes.extend(changes)
        for c in changes:
            print(c)

    # Write report
    report_path = ROOT / "TRANSLATION_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Translation Report: Foreign Language Remnants\n\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().isoformat()}\n\n")
        for c in all_changes:
            f.write(f"- {c}\n")

    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    main()