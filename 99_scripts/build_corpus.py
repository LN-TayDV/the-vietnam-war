# -*- coding: utf-8 -*-
"""
build_corpus.py — Trích và chuẩn hoá ngữ liệu từ các nguồn đã tải.
- Chuẩn hoá NFC.
- Lưu corpus sạch vào 09_CORPUS_TEXT/ với metadata nguồn.
- KHÔNG bịa: chỉ xử lý văn bản thật đã tải.
"""
import os, unicodedata, re, json, hashlib
base=r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\08_southern_vietnamese_library'
corpus_dir=os.path.join(base,'09_CORPUS_TEXT')
os.makedirs(corpus_dir, exist_ok=True)

def norm(s):
    return unicodedata.normalize('NFC', s)

sources = {
 'LeVanDuc_QuyenThuong_AL': os.path.join(base,'01_DICTIONARIES','LeVanDuc_QuyenThuong_AL_djvu.txt'),
 'LeVanDuc_QuyenHa_MX': os.path.join(base,'01_DICTIONARIES','LeVanDuc_QuyenHa_MX_djvu.txt'),
 'BachKhoa_405': os.path.join(base,'04_NEWSPAPERS_MAGAZINES','BachKhoa_405_djvu.txt'),
}

report=[]
for name, path in sources.items():
    if not os.path.exists(path):
        report.append({'source':name,'status':'missing'}); continue
    raw=open(path,encoding='utf-8',errors='replace').read()
    txt=norm(raw)
    # save cleaned corpus
    outp=os.path.join(corpus_dir, name+'.txt')
    open(outp,'w',encoding='utf-8',newline='\n').write(txt)
    lines=txt.split('\n')
    nonblank=[l for l in lines if l.strip()]
    chars=len(txt); words=len(txt.split())
    report.append({'source':name,'in_path':path,'out':outp,'bytes':len(txt.encode('utf-8')),
                   'chars':chars,'words':words,'lines':len(lines),'nonblank_lines':len(nonblank),
                   'sha256':hashlib.sha256(txt.encode('utf-8')).hexdigest()})
print(json.dumps(report, ensure_ascii=False, indent=2))
json.dump(report, open(os.path.join(base,'13_RESEARCH_REPORTS','corpus_extraction_report.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=2)