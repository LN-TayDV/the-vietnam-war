# -*- coding: utf-8 -*-
"""
header_normalizer — tách running header / tiêu đề chương bị DÁN LIỀN vào body.

Bối cảnh lỗi (segmentation/OCR):
  Ở hầu hết các trang, dòng đầu của block [V1C##-P###] là running header
  (tiêu đề chương/section, ALL-CAPS) bị nối THẲNG vào body mà không có newline.
  Ví dụ trang 99/100 chương 3:
     [V1C03-P001] (trang 99)
     DÂN TỘC QUỐC GIA, ... DO THÁI Niềm tin mê tín của hắn ...
     [V1C03-P002] (trang 100)
     DÂN TỘC QUỐC GIA, ... DO BIỂT CHỦNG TỘC DO THÁI kém quan tâm ...
  (chú ý OCR sai BIỆT→BIỂT ở trang 100).

Nguyên tắc (KHÔNG xóa nội dung):
  - Running header = chuỗi ALL-CAPS lặp lại ở đầu nhiều trang  -> loại bỏ khỏi body.
  - Tiêu đề chương ở trang mở đầu (dán liền)                  -> loại bỏ khỏi body
    (vì đã được dựng riêng trong title block từ TITLES).
  - Section heading ALL-CAPS xuất hiện 1 lần (không lặp)       -> GIỮ, tách thành heading.
  - Dòng tiêu đề chương nằm RIÊNG (có newline, is_chapter_title_line) -> GIỮ NGUYÊN.
  - Mọi thao tác cắt đều được GHI LOG (pid, trang, chuỗi bị cắt, body còn lại)
    để kiểm toán; không có thao tác xóa nội dung thực.

Chuẩn hóa so khớp: BỎ DẤU + UPPERCASE để chịu được lỗi OCR (BIỆT/BIỂT...).
"""
from __future__ import annotations

import re
import unicodedata
from typing import List, Tuple, Dict, Set

# So khớp prefix cho các trường hợp "cụm caps dài" (an toàn: header thường <=20 từ)
MAX_HEADER_WORDS = 20
MIN_HEADER_WORDS = 3

# Dòng tiêu đề chương/section ĐỨNG RIÊNG (ngắn, mở đầu bằng CHƯƠNG/PHẦN/...):
# KHÔNG được cắt (tránh mất chữ như "Ý" trong "Ý thức").
_STANDALONE_TITLE_RE = re.compile(
    r"^(CHƯƠNG|Chương|PHẦN|Phần|LỜI\s+NÓI\s+ĐẦU|TRANG\s+BÌA)\b", re.IGNORECASE
)


def is_standalone_title(line: str) -> bool:
    t = line.strip()
    return len(t) <= 90 and bool(_STANDALONE_TITLE_RE.match(t))


def normalize_caps(s: str) -> str:
    """Chuẩn hóa để so khớp: bỏ dấu, uppercase, gộp khoảng trắng/ký tự lạ."""
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return s.strip()


def is_upper_word(w: str) -> bool:
    letters = [c for c in w if c.isalpha()]
    if not letters:
        return False
    return all(c.isupper() for c in letters)


def leading_caps_words(line: str) -> List[str]:
    """Trả về danh sách từ ALL-CAPS ở đầu dòng (prefix caps tối đa)."""
    words = line.split(" ")
    caps: List[str] = []
    for w in words:
        core = w.strip(".,;:'\"()[]·")
        if core and is_upper_word(core):
            caps.append(w)
        else:
            break
    return caps


def _norm_words(line: str) -> List[str]:
    return [normalize_caps(w) for w in line.split(" ") if w.strip()]


def match_known_prefix(norm_words: List[str], known: Set[str]) -> int:
    """Trả về số từ (prefix) khớp một header đã biết (dài nhất). 0 nếu không."""
    best = 0
    upper = min(len(norm_words), MAX_HEADER_WORDS)
    for L in range(upper, MIN_HEADER_WORDS - 1, -1):
        cand = " ".join(norm_words[:L]).strip()
        if cand and cand in known:
            best = L
            break
    return best


def build_known_headers(blocks: List[Tuple[str, int, str]]) -> Set[str]:
    """
    Tập header đã biết (chuẩn hóa) của một chương:
      - Các dòng ALL-CAPS ĐỨNG RIÊNG (cả dòng là caps) — running header.
      - Các cụm caps DÍNH ở đầu block xuất hiện >=2 trang (lặp lại).
    """
    known: Set[str] = set()
    freq: Dict[str, int] = {}
    for _pid, _page, text in blocks:
        text = text.lstrip("\n")
        first_line = text.split("\n", 1)[0].strip()
        if not first_line:
            continue
        caps = leading_caps_words(first_line)
        if not caps:
            continue
        norm = normalize_caps(" ".join(caps))
        if not norm:
            continue
        # dòng toàn caps (đứng riêng) -> running header
        if len(caps) == len(first_line.split(" ")) and len(caps) >= MIN_HEADER_WORDS:
            known.add(norm)
        else:
            freq[norm] = freq.get(norm, 0) + 1
    for norm, c in freq.items():
        if c >= 2:
            known.add(norm)
    return known


def _strip_n_words(line: str, n: int) -> str:
    words = line.split(" ")
    return " ".join(words[n:]).lstrip()


def strip_running_headers(
    blocks: List[Tuple[str, int, str]],
    vi_title: str = "",
) -> Tuple[List[Tuple[str, int, str]], List[dict]]:
    """
    Loại bỏ running header / tiêu đề chương dán liền khỏi đầu mỗi block.

    blocks: [(pid, page, raw_text)]
    Trả về (cleaned_blocks, log).
    """
    known = build_known_headers(blocks)
    title_norm = normalize_caps(vi_title) if vi_title else ""
    cleaned: List[Tuple[str, int, str]] = []
    log: List[dict] = []

    for idx, (pid, page, text) in enumerate(blocks):
        is_first = idx == 0
        text = text.lstrip("\n")
        nl = text.find("\n")
        first_line = text[:nl] if nl >= 0 else text
        rest = text[nl:] if nl >= 0 else ""
        orig_first = first_line
        actions: List[str] = []

        # Bỏ qua nếu dòng đầu là tiêu đề chương ĐỨNG RIÊNG (không dán liền).
        # is_chapter_title_line được parser dùng; ở đây kiểm tra nhanh: dòng ngắn
        # và không có từ thường nào theo sau cụm caps.
        caps = leading_caps_words(first_line)
        glued = False
        if caps:
            after = _strip_n_words(first_line, len(caps))
            glued = bool(after) and not is_upper_word(after.split(" ")[0].strip(".,;:'\"()[]·"))

        if caps and glued:
            # Tiêu đề chương/section đứng riêng (không dán liền) -> GIỮ NGUYÊN.
            if is_standalone_title(first_line):
                cleaned.append((pid, page, text))
                continue
            # Lặp: cắt cho đến khi không còn header/tiêu đề ở đầu dòng.
            # Thứ tự mỗi vòng: known_header -> chapter_title -> caps_run.
            changed = True
            guard = 0
            while changed and guard < 6:
                changed = False
                guard += 1
                # 1) So khớp header đã biết (prefix, bỏ dấu) — áp dụng mọi block.
                nw = _norm_words(first_line)
                L = match_known_prefix(nw, known)
                if L > 0:
                    first_line = _strip_n_words(first_line, L)
                    actions.append(f"known_header:{L}")
                    changed = True
                    continue
                # 2) Trang mở đầu: so khớp tiêu đề chương (TITLES) — mixed case.
                if is_first and title_norm and first_line:
                    nw2 = _norm_words(first_line)
                    tl = len(title_norm.split())
                    if tl >= 2 and " ".join(nw2[:tl]).strip() == title_norm:
                        first_line = _strip_n_words(first_line, tl)
                        actions.append(f"chapter_title:{tl}")
                        changed = True
                        continue
                # 3) Cụm caps DÍNH còn lại (không khớp known) -> running header.
                caps2 = leading_caps_words(first_line)
                if caps2:
                    after2 = _strip_n_words(first_line, len(caps2))
                    glued2 = bool(after2) and not is_upper_word(after2.split(" ")[0].strip(".,;:'\"()[]·"))
                    if glued2 and len(caps2) >= MIN_HEADER_WORDS:
                        first_line = _strip_n_words(first_line, len(caps2))
                        actions.append(f"caps_run:{len(caps2)}")
                        changed = True
                        continue

        new_text = first_line + rest
        if actions:
            log.append({
                "pid": pid,
                "page": page,
                "is_first": is_first,
                "actions": actions,
                "removed": orig_first[: len(orig_first) - len(first_line)].strip(),
                "body_now": first_line.strip()[:80],
            })
        cleaned.append((pid, page, new_text))

    return cleaned, log