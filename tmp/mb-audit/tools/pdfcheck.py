import json,glob,os,collections,re,random,subprocess,urllib.parse,sys
import fitz
random.seed(3)
FOLDER={'home-economics':'home-economics-s-and-s','applied-maths':'applied-mathematics','dcg':'design-and-communication-graphics','maths':'mathematics','lcvp':'link-modules'}
SUBS=sys.argv[1:] 
topq=lambda ref:(re.search(r'Q(\d+)',ref) or [None,None])[1]
QRX=re.compile(r'^\s*(?:Question\s+|Q\.?\s*)?(\d{1,2})[\.\)]?\s+(?:\(?[a-zA-Z(]|$)')
QRX2=re.compile(r'^\s*Question\s+(\d{1,2})\b',re.I)
def page_questions(page):
    qs=[]
    W=page.rect.width
    for b in page.get_text('blocks'):
        x0,y0,x1,y1,txt=b[:5]
        first=txt.strip().split('\n')[0]
        m=QRX2.match(first) or (QRX.match(first) if x0<W*0.22 else None)
        if m and 1<=int(m.group(1))<=20: qs.append((round(y0),int(m.group(1))))
    return qs
res={}
for s in SUBS:
    cards=[c for f in sorted(glob.glob(f'decks/{s}__*.json')) for c in json.load(open(f))]
    files=collections.defaultdict(list)
    for c in cards:
        sm=c.get('sourceMaterial')
        if not sm or sm.get('regions') or sm['kind'] in('linked-reading','supplementary-text') or sm.get('documentKind')=='scheme': continue
        fid=sm.get('sourceFileid') or c.get('paperFileid')
        if not fid: continue
        files[(fid if fid.lower().endswith(('.pdf','.jpg','.png')) else fid+'.pdf', sm.get('sourceYear') or c['year'])].append(c)
    keys=[k for k in files if k[0].endswith('.pdf')]; random.shuffle(keys)
    n=other=noq=0; ex=[]; npages=[]
    for fid,year in keys[:10]:
        local=f'pdfs/{s}-{year}-{fid}'
        if not os.path.exists(local):
            path=f'papers/lc/{FOLDER.get(s,s)}/{year}/paper/{fid}'
            url='https://firebasestorage.googleapis.com/v0/b/nextstepuni-app.firebasestorage.app/o/'+urllib.parse.quote(path,safe='')+'?alt=media'
            subprocess.run(['curl','-s','-f','-o',local,url])
        if not os.path.exists(local): continue
        try: doc=fitz.open(local)
        except Exception: continue
        for c in files[(fid,year)]:
            sm=c['sourceMaterial']; own=topq(c['questionRef'])
            found=[]
            for p in sm.get('pages',[]):
                if 1<=p<=len(doc): found+= [q for _,q in page_questions(doc[p-1])]
            n+=1; npages.append(len(sm.get('pages',[])))
            others=sorted({q for q in found if own is None or q!=int(own)})
            if not found: noq+=1
            if others and own is not None:
                other+=1
                if len(ex)<4: ex.append((c['id'],c['questionRef'],sm['pages'],'also shows Q'+','.join(map(str,others))))
    res[s]={'cardsChecked':n,'pageShowsOtherQuestion':other,'pct':round(100*other/n,1) if n else None,'noQuestionNumberDetected':noq,'avgPages':round(sum(npages)/len(npages),2) if npages else 0,'examples':ex}
    print(s,res[s],flush=True)
json.dump(res,open(f'pdfcheck-{SUBS[0]}.json','w'),indent=1)
