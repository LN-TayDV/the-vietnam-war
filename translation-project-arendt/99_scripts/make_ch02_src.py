import json
import re
import unicodedata

V2 = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\02_extracted_text\v2"

with open(V2 + r"\ch02_structure.json", encoding="utf-8") as f:
    data = json.load(f)

paras = data["paragraphs"]
print("Total paragraphs:", len(paras))

def ends_sentence(t):
    t = t.rstrip()
    return bool(t) and t[-1] in ".!?…\u2019\u201d"

# Clean text: remove soft hyphens and join word parts split across lines
def clean_text(t):
    # Remove zero-width spaces
    t = t.replace("\u200b", "")
    # Remove soft hyphen and the space that follows it (word split across visual line)
    # Pattern: letter + soft hyphen + space + letter → join without space
    t = re.sub(r'(\w)\u00ad\s+(\w)', r'\1\2', t)
    # Also handle soft hyphen at end without space (rare)
    t = t.replace("\u00ad", "")
    # Normalize multiple spaces
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

# Merge paragraphs across page boundaries where one ends mid-sentence
merged = []
i = 0
while i < len(paras):
    cur = dict(paras[i])
    cur["text"] = clean_text(cur["text"])
    j = i + 1
    while j < len(paras):
        nxt = paras[j]
        nxt_text = clean_text(nxt["text"])
        if cur["text"] and not ends_sentence(cur["text"]):
            if nxt_text and nxt_text[0].islower():
                cur["text"] = cur["text"] + " " + nxt_text
                j += 1
                continue
        break
    merged.append(cur)
    i = j if j > i + 1 else i + 1

print("After merging:", len(merged))

# Write clean src txt
lines = []
lines.append("# ch02 — The Jews, the Nation-State, and the Birth of Antisemitism")
lines.append("# Source structure rebuilt from original PDF")
lines.append("# Encoding: UTF-8, NFC, LF")
lines.append("")

for p in merged:
    pid = p["para_id"]
    page = p["page"]
    text = p["text"].strip()
    if not text:
        continue
    lines.append(f"[{pid}] (trang {page})")
    lines.append(text)
    lines.append("")

content = "\n".join(lines)
content = unicodedata.normalize("NFC", content)

out_path = V2 + r"\v2_ch02_src.txt"
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"Saved: {out_path}")
print(f"Total characters: {len(content)}")
print(f"Total paragraphs written: {len(merged)}")

# Quick verification
soft_hyphens = content.count("\u00ad")
print("Soft hyphens remaining:", soft_hyphens)
zwsp = content.count("\u200b")
print("Zero-width spaces:", zwsp)
