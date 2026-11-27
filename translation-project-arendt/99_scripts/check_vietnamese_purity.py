# -*- coding: utf-8 -*-
"""
check_vietnamese_purity.py — Kiểm tra bản dịch tiếng Việt không còn từ/Anh remnant.
Áp dụng VLP-01 (Tiếng Việt trước): không còn từ/cụm ngoại ngữ có thể dịch nhưng bị giữ nguyên.
"""

import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt"
TRANS_DIR = os.path.join(BASE, "04_translation", "v2")

# Từ/cụm Anh phổ biến hay bị để lại trong bản dịch (không dịch)
ENGLISH_REMNANT_PATTERNS = [
    r"\baccident\b", r"\bideology\b", r"\bpolicy\b", r"\bpersecution\b", r"\bextermination\b",
    r"\bJewish question\b", r"\bpublic opinion\b", r"\bpretext\b", r"\bdemagogy\b",
    r"\bcommon sense\b", r"\bnation-state\b", r"\bnationalism\b", r"\bantisemitism\b",
    r"\bJew-hatred\b", r"\bemancipation\b", r"\bassimilation\b", r"\btotalitarianism\b",
    r"\btotalitarian\b", r"\bdemocracy\b", r"\brepublic\b", r"\bparliament\b",
    r"\bcongress\b", r"\bmovement\b", r"\bparty\b", r"\bgovernment\b", r"\bstate\b",
    r"\bnation\b", r"\bpeople\b", r"\bpower\b", r"\bauthority\b", r"\bpolitics\b",
    r"\bpolitical\b", r"\bsociety\b", r"\bsocial\b", r"\beconomic\b", r"\bhistory\b",
    r"\bhistorical\b", r"\bhistorian\b", r"\bcentury\b", r"\brevolution\b",
    r"\bwar\b", r"\bpeace\b", r"\bfreedom\b", r"\blegality\b", r"\bjustice\b",
    r"\bright\b", r"\blaw\b", r"\blegal\b", r"\bconstitution\b", r"\bdemocratic\b",
    r"\btolerated\b", r"\bclaims\b", r"\balibi\b", r"\bby-passed\b",
    r"\bDark Ages\b", r"\bliquidate\b", r"\bsuccumb\b", r"\babsolute\b",
    r"\bPhaedrus\b", r"\bTheaetetus\b", r"\bforefront\b", r"\bjudenrein\b",
    r"\bjted\b", r"\bclaimed\b", r"\bclaimed\b", r"\bpropaganda\b",
    r"\bclaim\b", r"\bcommunist\b", r"\bcommunism\b", r"\bcommunist\b",
    r"\bsocialist\b", r"\bsocialism\b", r"\bcapitalist\b", r"\bcapitalism\b",
    r"\bliberal\b", r"\bliberalism\b", r"\bconservative\b", r"\bconservatism\b",
    r"\bfascist\b", r"\bfascism\b", r"\bnazi\b", r"\bnazism\b",
    r"\bbolshevik\b", r"\bbolshevism\b",
]


def check_file(filepath):
    """Kiểm tra một file vi.txt cho từ/Anh remnant."""
    issues = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    para_pattern = re.compile(r"^\[(V1[A-Z0-9]+-P\d{3})\]\s\(trang \d+\)\s*$")

    i = 0
    while i < len(lines):
        m = para_pattern.match(lines[i])
        if m:
            pid = m.group(1)
            # Lấy văn bản (dòng sau header)
            text = ""
            if i + 1 < len(lines):
                text = lines[i + 1]

            # Bỏ qua block footnotes
            if text.strip() == "=== FOOTNOTES ===":
                i += 3
                continue

            # Kiểm tra từng pattern Anh
            for pattern in ENGLISH_REMNANT_PATTERNS:
                if re.search(pattern, text, re.IGNORECASE):
                    issues.append(f"{pid}: '{pattern}' trong: '{text[:100]}...'")

            i += 3  # Skip header, text, empty
        else:
            i += 1

    return issues


def main():
    # Kiểm tra tất cả chapter
    chapters = sorted([d for d in os.listdir(TRANS_DIR)
                       if os.path.isdir(os.path.join(TRANS_DIR, d))])

    total_issues = 0
    for ch in chapters:
        vi_path = os.path.join(TRANS_DIR, ch, f"v1_{ch}_vi.txt")
        if not os.path.exists(vi_path):
            print(f"  {ch}: CHƯA CÓ FILE VI.TXT")
            continue

        issues = check_file(vi_path)
        if issues:
            print(f"  {ch}: {len(issues)} lỗi tiếng Anh còn sót")
            for iss in issues[:10]:
                print(f"    - {iss}")
            if len(issues) > 10:
                print(f"    ... và {len(issues) - 10} lỗi khác")
            total_issues += len(issues)
        else:
            print(f"  {ch}: KHÔNG CÓ LỖI TIẾNG ANH")

    print(f"\nTỔNG: {total_issues} lỗi tiếng Anh còn sót trên {len(chapters)} chương")


if __name__ == "__main__":
    main()
