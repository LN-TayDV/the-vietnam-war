# -*- coding: utf-8 -*-
"""
extract_chapters.py — Trích xuất văn bản từng chương từ PDF gốc.
- Chuẩn hoá Unicode NFC (gộp dấu tiếng Việt).
- Bỏ dòng watermark của Cambridge (doi.org / 'Published online by').
- Giữ nguyên số trang in (printed page label) làm mốc đối chiếu.
- Ghi mỗi chương ra file .txt UTF-8 trong 02_extracted_text/vol<CH>/ch<NN>.txt
- Ghi manifest.json chứa ánh xạ chương -> dải trang PDF/in.
Yêu cầu: pymupdf
"""
import pymupdf, re, os, json, sys, unicodedata, hashlib

PDF = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\The_Cambridge_History_of_the_Vietnam_War.pdf'
ROOT = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project'
OUTDIR = os.path.join(ROOT, '02_extracted_text')
PLAN = os.path.join(ROOT, '00_plan')

WATERMARK = re.compile(r'https?://doi\.org/\S+.*$', re.MULTILINE)
# Cambridge fonts encode đ/Đ as base 'd'/'D' + U+0335 (combining short stroke overlay),
# which NFC cannot compose. Map explicitly to precomposed đ (U+0111) / Đ (U+0110).
STROKE_FIX = [('d\u0335', '\u0111'), ('D\u0335', '\u0110')]

def printed_label(page):
    for line in page.get_text("text").split("\n")[:4]:
        m = re.fullmatch(r'\s*(\d{1,4})\s*', line)
        if m:
            return int(m.group(1))
    return None

def clean(text):
    text = WATERMARK.sub('', text)
    for a, b in STROKE_FIX:
        text = text.replace(a, b)
    text = unicodedata.normalize('NFC', text)
    return text

def main():
    d = pymupdf.open(PDF)
    toc = d.get_toc()
    bounds = [(1,509,'V1'),(510,1221,'V2'),(1222,1866,'V3')]
    def vol_of(p):
        for a,b,n in bounds:
            if a<=p<=b: return n
    chaps = [(e[1],e[2]) for e in toc if e[0]==3]
    idx_pages = [e[2] for e in toc if e[1].strip()=='Index']
    # end pages
    meta=[]
    for k,(name,p) in enumerate(chaps):
        v=vol_of(p); end=None
        for name2,p2 in chaps[k+1:]:
            if vol_of(p2)==v: end=p2-1; break
        if end is None:
            vs,ve=[(a,b) for a,b,n in bounds if n==v][0]
            idxp=[ip for ip in idx_pages if vs<=ip<=ve]
            end=(idxp[0]-1) if idxp else ve
        meta.append((v,name,p,end))
    # number chapters per volume
    from collections import defaultdict
    cnt=defaultdict(int); manifest=[]
    for v,name,p,end in meta:
        cnt[v]+=1; chno=cnt[v]
        title=re.sub(r'^\d+\s*[\.\-]\s*','',name).strip()
        vdir=os.path.join(OUTDIR, v.lower())
        os.makedirs(vdir, exist_ok=True)
        pages=[]
        buf=[]
        for pi in range(p, end+1):
            pg=d[pi-1]
            t=clean(pg.get_text("text"))
            buf.append(t)
            pages.append({'pdf_page':pi,'printed':printed_label(pg)})
        full="\n".join(buf)
        # collapse >2 blank lines
        full=re.sub(r'\n{3,}','\n\n',full).strip()+"\n"
        rel=os.path.join('02_extracted_text', v.lower(), f'ch{chno:02d}.txt')
        with open(os.path.join(ROOT, rel.replace('/', os.sep)), 'w', encoding='utf-8', newline='\n') as f:
            f.write(full)
        words=len(full.split())
        manifest.append({'volume':v,'chapter':chno,'title_en':title,'title_vi':'',
                         'pdf_start':p,'pdf_end':end,'pages':pages,
                         'file':rel,'words':words,'char_count':len(full),
                         'status':'extracted'})
    # general intro / introduction blocks (front matter body): V1 pdf17-42, etc.
    with open(os.path.join(PLAN,'manifest.json'),'w',encoding='utf-8',newline='\n') as f:
        json.dump({'source_pdf':PDF,
                   'source_sha256':'338BC8B8141A22638E1ED71A4DB285E3E10817DFAA789026E18EA988716768D1',
                   'total_pages':d.page_count,'chapters':manifest}, f, ensure_ascii=False, indent=2)
    print("Extracted", len(manifest), "chapters. Total words:", sum(m['words'] for m in manifest))
    for v in ['V1','V2','V3']:
        print(v, sum(1 for m in manifest if m['volume']==v), "chapters,",
              sum(m['words'] for m in manifest if m['volume']==v), "words")

if __name__=='__main__':
    main()