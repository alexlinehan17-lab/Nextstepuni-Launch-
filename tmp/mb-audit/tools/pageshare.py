import json,glob,os,collections,re
from PIL import Image
ROOT='/home/user/Nextstepuni-Launch-/public'
topq=lambda ref: (re.search(r'Q(\d+)',ref) or re.search(r'\b(ABQ|Section [A-Z0-9]+|Part [A-Z0-9]+|Frage \d+|Text \w+)',ref) or [None,None])[1] if ref else None
out={}
for s in sorted({os.path.basename(f).split('__')[0] for f in glob.glob('decks/*__*.json')}):
    cards=[c for f in glob.glob(f'decks/{s}__*.json') for c in json.load(open(f))]
    pages=collections.defaultdict(list)   # (file,year,level,page) -> cards
    nsrc=0
    for c in cards:
        sm=c.get('sourceMaterial')
        if not sm or sm.get('regions') or sm['kind'] in('linked-reading','supplementary-text'): continue
        nsrc+=1
        for p in sm.get('pages',[]): pages[(sm.get('sourceFileid') or c.get('paperFileid'),c['year'],c['level'],p)].append(c)
    multiQ=multiT=0; flagged=set(); flaggedT=set(); ex=[]
    for k,cs in pages.items():
        qs={topq(c['questionRef']) for c in cs}; ts={c['topicId'] for c in cs}
        if len(qs)>1:
            multiQ+=1; flagged.update(c['id'] for c in cs)
        if len(ts)>1 and len(qs)>1:
            multiT+=1; flaggedT.update(c['id'] for c in cs)
            if len(ex)<3: ex.append((k[1],k[2],k[3],sorted({(c['questionRef'],c['topicId']) for c in cs})[:4]))
    # figures
    fw=[];fh=[];tall=0;nf=0;miss=0;incl=0
    for c in cards:
        for key in('figure','questionFigure'):
            fg=c.get(key)
            if not fg: continue
            nf+=1; incl+=bool(fg.get('includesPrompt'))
            try:
                w,h=Image.open(ROOT+fg['src']).size; fw.append(w); fh.append(h); tall+= h>1.6*w
            except Exception: miss+=1
    med=lambda L: sorted(L)[len(L)//2] if L else 0
    out[s]={'cards':len(cards),'withWholePageSource':nsrc,'pages':len(pages),'pagesMultiQuestion':multiQ,'pagesMultiTopic':multiT,'cardsOnMultiQPage':len(flagged),'cardsOnMultiTopicPage':len(flaggedT),'examples':ex,
            'figs':nf,'figMissing':miss,'figMedW':med(fw),'figP90W':sorted(fw)[int(len(fw)*.9)] if fw else 0,'figWide>1200':sum(w>1200 for w in fw),'figTall':tall,'includesPrompt':incl,
            'qFigCards':sum(1 for c in cards if c.get('questionFigure')),'figCards':sum(1 for c in cards if c.get('figure'))}
json.dump(out,open('pageshare.json','w'),indent=1)
for s,o in out.items():
    print(f"{s:22} cards {o['cards']:5} wholePageSrc {o['withWholePageSource']:5} onMultiQpage {o['cardsOnMultiQPage']:5} onMultiTopicPage {o['cardsOnMultiTopicPage']:5} | figs {o['figs']:5} qFig {o['qFigCards']:5} medW {o['figMedW']:5} p90W {o['figP90W']:5} >1200 {o['figWide>1200']:5} tall {o['figTall']:4} miss {o['figMissing']}")
