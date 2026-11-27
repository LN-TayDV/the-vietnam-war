import json, re, unicodedata

V2 = r"C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\02_extracted_text\v2"

with open(V2 + r"\v2_ch02_src.txt", encoding="utf-8") as f:
    content = f.read()

# Check for soft hyphens remaining
soft_hyphens = content.count("\u00ad")
print("Soft hyphens remaining:", soft_hyphens)

# Check for mid-sentence paragraph breaks
paras = re.findall(r"\[V1C02-P\d+\] \(trang \d+\)\n(.*?)(?=\n\[V1C02-P|\Z)", content, re.DOTALL)
print("Paragraphs found:", len(paras))

def ends_sentence(t):
    t = t.rstrip()
    return bool(t) and t[-1] in ".!?…\u2019\u201d"

no_sentence_end = 0
for p in paras:
    t = p.strip()
    if t and not ends_sentence(t):
        no_sentence_end += 1
        print(f'  No sentence end: "{t[-60:]}"')

print("Paragraphs not ending with sentence punctuation:", no_sentence_end)

# Check for zero-width spaces
zwsp = content.count("\u200b")
print("Zero-width spaces:", zwsp)

print()
print("File size:", len(content), "characters")
print()
print("First 800 chars:")
print(content[:800])
