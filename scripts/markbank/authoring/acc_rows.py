#!/usr/bin/env python3
"""Accounting Mark Bank rows: every figure the scheme prices, lifted from the scheme PDF's own geometry.

    python3 scripts/markbank/authoring/acc_rows.py [--write]

The Accounting marking scheme prints its solution as the account itself, each figure followed by its marks
in brackets — "Purchases W2 1,126,000 [9]" — with section totals in drawn squares and theory parts as a
block of points under one "[6]". Until October 2026 the card showed the page as a crop and offered a
half-mark stepper to the task total. Alex's rule (2026-10-23): what the scheme prices is a row the student
claims with its marks on it.

For each authored task (authored.json: the scheme pages a vision audit bound to it) the pages are read as
word lines with PyMuPDF; the 2022 schemes, whose subset fonts carry no ToUnicode map, are read glyph by
glyph through glyphmap-accounting-2022.json (derived by acc_glyphs_2022.py from word evidence, never
hand-typed). A row is a bracketed mark with the figure printed before it and the words that label the
line ("Purchases W2 1,126,000", 9 marks); a mark printed on its own line takes the figure above or below it
at the same x and that line's words, or the column heading over it; a mark with no figure is a theory part
and takes the unpriced lines that follow it; a boxed section total that no mark follows prices a block of
points. Section totals (drawn squares, the question title's bracketed total, a lone bracketed sum of two or
more parts) are not rows.

A task's rows are its heading span ("(a)" … next letter, "(i)" … next roman) when those rows add up to its
total; otherwise the question's rows in reading order are shared out to its tasks in paper order, each
taking rows until its total is met. A part the scheme prices only through its section total (its span
prints no mark) takes a single flagged block row. A task whose rows cannot be made to add up, or whose
figures sit in a grid the geometry cannot label, is left as it was (the crop and the stepper) and listed
in accounting-rows-residue.json with its reason. Nothing is typed: every row is the scheme's words.
"""

import fitz, re, json, collections, sys, os, unicodedata
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE, '..', '..', '..'))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'scripts/paper-trail')); import accounting_era as era
cards=json.load(open('components/MarkBank/cards/accounting/authored.json'))['cards']
# The scheme's text layer draws "ti", "tt", "fi" as single ligature glyphs and its bullets from the Symbol font;
# the shared repair map (glyphmap.json, ligature test) and NFKC make them the printed letters.
GLYPHMAP=json.load(open(os.path.join(HERE, 'glyphmap.json')))
BULLETS={'\uf0b7': '•', '\uf0a7': '•', '\uf0d8': '•', '\uf076': '•', '\uf0fc': '✓'}
def repaired(text):
    text=''.join(GLYPHMAP.get(ch, BULLETS.get(ch, ch)) for ch in text)
    return unicodedata.normalize('NFKC', text)
MARK=re.compile(r'^\[(\d+)\]$')
MARK_IN=re.compile(r'\[(\d+)\]|[>\[](\d+)[@\]]')
FIG=re.compile(r'^(?:\(€?\d[\d,.]*\)|€?\d[\d,.]*)$')
HEAD=re.compile(r'^\(([a-z]{1,4})\)$')
ROMAN={'i','ii','iii','iv','v','vi','vii','viii','ix','x'}
INTRO=re.compile(r'INTRODUCTION|Marks allocated to each line', re.I)
docs={}; page_cache={}
def doc_for(year,fid):
    key=(year,fid)
    if key not in docs: docs[key]=fitz.open(f'paper-trail-corpus/markingschemes/{year}/{fid}')
    return docs[key]
def tokens(word, x0, x1):
    """Split a word on bracketed marks: '[3](150,700)' -> '[3]', '(150,700)'; '180,000[1]' -> '180,000', '[1]'."""
    out=[]; pos=0
    for m in MARK_IN.finditer(word):
        if m.start()>pos: out.append(word[pos:m.start()])
        out.append(f'[{m.group(1) or m.group(2)}]'); pos=m.end()
    if pos<len(word): out.append(word[pos:])
    n=len(out) or 1; w=(x1-x0)/n
    return [(x0+i*w, x0+(i+1)*w, t) for i,t in enumerate(out) if t]
def boxes(page):
    """The small drawn squares the scheme prints its section totals in."""
    out=[]
    for d in page.get_drawings():
        r=d.get('rect')
        # a section-total square is at least 20 × 20; the cell drawn around each "[3]" is about 15 × 15
        if r is not None and 20<=r.width<90 and 20<=r.height<45: out.append(r)
    return out
GLYPHS=json.load(open(os.path.join(HERE, 'glyphmap-accounting-2022.json')))
GMAP={fam:{int(k[2:],16):v for k,v in m.items()} for fam,m in GLYPHS['map_by_family'].items()}
def words_2022(page):
    """Words with bboxes for a 2022 page: glyph ids read from rawdict and repaired per font family."""
    out=[]
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                fam=span['font'].split('+')[-1].split(',')[0]; m=GMAP.get(fam)
                cur=[]; 
                def flush():
                    if cur:
                        t=''.join(c for _,c in cur); x0=min(b[0] for b,_ in cur); x1=max(b[2] for b,_ in cur); y0=min(b[1] for b,_ in cur); y1=max(b[3] for b,_ in cur)
                        out.append((x0,y0,x1,y1,t))
                    cur.clear()
                prev_x1=None
                for ch in span['chars']:
                    c=ch['c']; cp=ord(c) if len(c)==1 else -1
                    if m is not None and cp in m: c=m[cp]
                    elif m is not None and 0<=cp<0x20: c=' '
                    if c==' ' or c=='\xa0': flush(); prev_x1=None; continue
                    if prev_x1 is not None and ch['bbox'][0]-prev_x1>2.5: flush()
                    cur.append((ch['bbox'], c)); prev_x1=ch['bbox'][2]
                flush()
    return out
def page_lines(year,fid,p):
    key=(year,fid,p)
    if key in page_cache: return page_cache[key]
    page=doc_for(year,fid)[p-1]; W,H=page.rect.width,page.rect.height; bx=boxes(page)
    rows=collections.defaultdict(list)
    for w in (words_2022(page) if year==2022 else page.get_text('words')):
        boxed=any(r.x0-3<=w[0] and w[2]<=r.x1+3 and r.y0-3<=w[1] and w[3]<=r.y1+3 for r in bx)
        for x0,x1,t in tokens(w[4],w[0],w[2]):
            if boxed and (MARK.match(t) or re.fullmatch(r'\d{1,3}', t)): t=f'<box {MARK.match(t).group(1) if MARK.match(t) else t}>'
            rows[round(w[1]/3)].append((x0,w[1],x1,t))
    out=[]
    for k in sorted(rows):
        ws=sorted(rows[k], key=lambda w:w[0])
        if len(ws)==1 and re.fullmatch(r'\d{1,3}', ws[0][3]) and ws[0][0]/W>=0.75:
            ws=[(ws[0][0],ws[0][1],ws[0][2],f'<box {ws[0][3]}>')]
        out.append({'p':p,'y':ws[0][1],'yf':ws[0][1]/H,'xf':ws[0][0]/W,'ws':ws,'W':W})
    if any(INTRO.search(' '.join(t for *_,t in l['ws'])) for l in out[:14]): out=[]
    page_cache[key]=out; return out
BOX=re.compile(r'^<box (\d+)>$')
TITLE=re.compile(r'^(?:\d{1,2}\.|QUESTION|Question|Q\.?\d)', re.I)
LETTERS=re.compile(r'[A-Za-z]{3}')
def figure_near(lines, i, x, span=1):
    """A figure within 45pt of x on the line before or after line i."""
    for j in (i-1, i+1, i-2, i+2):
        if 0<=j<len(lines):
            cand=[(abs(px0-x),t) for px0,py0,px1,t in lines[j]['ws'] if FIG.match(t) and abs(px0-x)<45]
            if cand: return min(cand)[1], j
    return None, None
def column_heading(lines, i, x):
    """The nearest earlier line with a word near x that is not a figure or mark: a grid's column heading."""
    for j in range(i-1, max(-1, i-14), -1):
        words=[t for px0,py0,px1,t in lines[j]['ws'] if abs(px0-x)<60 and LETTERS.search(t) and not MARK.match(t) and not BOX.match(t)]
        if words: return ' '.join(words)
    return ''
def rows_of(lines, totals):
    """Rows from lines: each [N] with the figure before it and its label; a mark with no figure (a theory part)
    takes the unpriced lines after it as its text; a boxed total with no marks after it prices a block."""
    rows=[]; qtotal=sum(totals)
    sums={sum(totals[i:j]) for i in range(len(totals)) for j in range(i+2,len(totals)+1)}
    pending_box=None
    def flush_box():
        nonlocal pending_box
        if pending_box and pending_box[2]:
            n,p,texts,y=pending_box
            rows.append({'text':' '.join(texts)[:400],'figure':None,'marks':n,'p':p,'y':y,'block':True})
        pending_box=None
    for i,line in enumerate(lines):
        ws=line['ws']; texts=[t for *_,t in ws]
        boxed=[int(BOX.match(t).group(1)) for t in texts if BOX.match(t)]
        marks=[(k,int(MARK.match(t).group(1))) for k,t in enumerate(texts) if MARK.match(t)]
        if TITLE.match(texts[0]) and line['xf']<0.2 and marks and all(n>=10 for _,n in marks):
            marks=[]   # the question title carries its total in brackets ("1. Final Accounts … [80]")
        if boxed and not marks:
            flush_box(); pending_box=(boxed[0], line['p'], [], round(line['y']))
            rest=[t for t in texts if not BOX.match(t)]
            if rest: pending_box[2].append(' '.join(rest))
            continue
        if not marks:
            if pending_box: pending_box[2].append(' '.join(texts))
            continue
        pending_box=None
        only_marks=all(MARK.match(t) or BOX.match(t) for t in texts)
        if len(marks)==1:
            n=marks[0][1]; others=[t for t in texts if not MARK.match(t)]
            # a section total: the sum of two or more parts, printed alone or on a part heading
            if n in sums and (only_marks or (len(others)==1 and HEAD.match(others[0]))): continue
            if only_marks and n>=10 and n==qtotal: continue
        label=[]
        for k,(x0,y0,x1,t) in enumerate(ws):
            if MARK.match(t) or BOX.match(t): break
            if FIG.match(t) and k>0: break
            label.append(t)
        for k,n in marks:
            fig=None; lab=label; theory=False
            if not only_marks:
                for j in range(k-1,-1,-1):
                    if FIG.match(texts[j]): fig=texts[j]; break
                    if MARK.match(texts[j]): break
                if fig is None and len(marks)==1: theory=True
            else:
                x=ws[k][0]; fig,j=figure_near(lines,i,x)
                lab=[]
                if fig is not None:
                    lab=[t for px0,py0,px1,t in lines[j]['ws'] if not FIG.match(t) and not MARK.match(t) and not BOX.match(t) and LETTERS.search(t)]
                    if not lab:
                        head=column_heading(lines, i, x)
                        lab=[head] if head else []
            if fig is not None and not any(LETTERS.search(t) for t in lab):
                head=column_heading(lines, i, ws[k][0])
                if head: lab=[head]
            text=' '.join(lab+([fig] if fig else [])).strip()
            if theory:
                after=[]; j=i+1
                while j<len(lines):
                    nt=[t for *_,t in lines[j]['ws']]
                    if any(MARK.match(t) or BOX.match(t) for t in nt) or (HEAD.match(nt[0]) and lines[j]['xf']<0.3): break
                    if sum(1 for t in nt if FIG.match(t))>=2: break
                    if LETTERS.search(' '.join(nt)): after.append(' '.join(nt))
                    j+=1
                text=(' '.join([text]+after)).strip()[:400]
            rows.append({'text':text or '(unlabelled)','figure':fig,'marks':n,'p':line['p'],'y':round(line['y'])})
    flush_box()
    return rows
def task_parts(taskkey):
    m=re.match(r'^(\d+)([A-Z]?)(?:\(([a-z]+)\))?(?:\(([ivx]+)\))?(?:\(([a-z])\))?(?:-(.+))?$', taskkey)
    return None if not m else {'q':int(m.group(1)),'sub':m.group(2),'letter':m.group(3),'roman':m.group(4),'sub2':m.group(5),'split':m.group(6)}
def heading_span(lines, tp):
    if not tp['letter']: return None
    heads=[(i,HEAD.match(l['ws'][0][3]).group(1)) for i,l in enumerate(lines) if HEAD.match(l['ws'][0][3]) and l['xf']<0.3]
    letters=[(i,h) for i,h in heads if h not in ROMAN]; romans=[(i,h) for i,h in heads if h in ROMAN]
    start=next((i for i,h in letters if h==tp['letter']), None)
    if start is None: return None
    end=next((i for i,h in letters if i>start), len(lines)); seg=(start,end)
    if tp['roman']:
        rs=[(i,h) for i,h in romans if start<=i<end]
        s=next((i for i,h in rs if h==tp['roman']), None)
        if s is None: return None
        e=next((i for i,h in rs if i>s), end); seg=(s,e)
    return seg
# group cards by question
groups=collections.OrderedDict()
# a page every card of a sitting cites is the annotation key or introduction, not a solution page
common=collections.defaultdict(lambda:None)
for c in cards:
    k=(c['year'],c['level']); ps={r['p'] for r in c['schemeRegions']}
    common[k]=ps if common[k] is None else common[k]&ps
for c in cards:
    tp=task_parts(c['taskKey'])
    if tp: groups.setdefault((c['year'],c['level'],c['paperFileid'],f"{tp['q']}{tp['sub']}"), []).append((c,tp))
# pages owned per question, to cut shared pages at heads
owners=collections.defaultdict(set)
for key,cs in groups.items():
    for c,tp in cs:
        for r in c['schemeRegions']: owners[(key[0],key[2],r['p'])].add(key[3])
qnum=lambda k: int(re.match(r'\d+',k).group(0))
stats=collections.Counter(); per=collections.defaultdict(lambda:[0,0]); out={}; bad=[]; heads_cache={}; scales=collections.Counter(); gridcards=[]
def solve(cs, lines, totals, scale):
    """Resolve every card of a question at a printed-marks scale (1, or 2 for Ordinary schemes that print doubled marks)."""
    allrows=rows_of(lines, [t*scale for t in totals]); resolved={}; used=set(); how={}
    for c,tp in cs:
        seg=heading_span(lines, tp)
        if not seg: continue
        rows=rows_of(lines[seg[0]:seg[1]], [t*scale for t in totals])
        if rows and sum(r['marks'] for r in rows)==c['totalMarks']*scale and not tp['split']:
            resolved[c['id']]=rows; how[c['id']]='heading'; used.update((r['p'],r['y'],r['marks'],r['text']) for r in rows)
    pool=[r for r in allrows if (r['p'],r['y'],r['marks'],r['text']) not in used]
    pos=0; ok=True
    for c,tp in cs:
        if c['id'] in resolved: continue
        need=c['totalMarks']*scale; got=0; take=[]
        while pos<len(pool) and got<need: take.append(pool[pos]); got+=pool[pos]['marks']; pos+=1
        if got!=need:
            seg=heading_span(lines, tp)
            if got==0 and seg and not rows_of(lines[seg[0]:seg[1]], totals):
                span=lines[seg[0]:seg[1]]; text=' '.join(t for l in span for *_,t in l['ws'] if not BOX.match(t))[:400]
                resolved[c['id']]=[{'text':text,'figure':None,'marks':need,'p':span[0]['p'],'y':round(span[0]['y']),'block':True,'inferred':True}]; how[c['id']]='inferred'
                continue
            ok=False; break
        resolved[c['id']]=take; how[c['id']]='partition'
    leftover=len(pool)-pos if ok else None
    return ok, resolved, how, leftover, allrows
for key,cs in groups.items():
    year,level,fid,q=key; qn=qnum(q)
    if (year,fid) not in heads_cache: heads_cache[(year,fid)]=era.scheme_heads(doc_for(year,fid))[0]
    have=heads_cache[(year,fid)]
    pages=sorted({r['p'] for c,tp in cs for r in c['schemeRegions']}-(common[(year,level)] or set()))
    lines=[]
    for p in pages:
        ls=page_lines(year,fid,p)
        lo=have.get(qn); hi=have.get(qn+1)
        nmarks=lambda L: sum(1 for l in L for *_,t in l['ws'] if MARK.match(t))
        if lo and lo[0]==p:
            cut=[l for l in ls if l['yf']>=lo[1]-0.002]
            if nmarks(cut)>0 or nmarks(ls)==0: ls=cut   # a head placed below the content is not trusted
        if hi and hi[0]==p:
            cut=[l for l in ls if l['yf']<hi[1]-0.002]
            if nmarks(cut)>0 or nmarks(ls)==0: ls=cut
        lines.extend(ls)
    totals=[c['totalMarks'] for c,tp in cs]
    for c,tp in cs: per[f"{year}-{level}"][1]+=1
    result=None
    for scale in (1,):
        ok,resolved,how,leftover,allrows=solve(cs,lines,totals,scale)
        if ok: result=(scale,resolved,how,leftover); break
        if result is None or len(resolved)>len(result[1]): result=(scale,resolved,how,leftover) if not ok else result
    scale,resolved,how,leftover=result
    full=all(c['id'] in resolved for c,tp in cs)
    for c,tp in cs:
        if c['id'] in resolved:
            rws=resolved[c['id']]
            if any(r['text']=='(unlabelled)' or not re.search(r'[A-Za-z0-9]', r['text']) for r in rws):
                del resolved[c['id']]; stats['grid']+=1; gridcards.append(c['id']); continue
            per[f"{year}-{level}"][0]+=1; out[c['id']]={'scale':scale,'how':how[c['id']],'rows':rws}
    scales[(level,scale)]+=sum(1 for c,tp in cs if c['id'] in resolved)
    if full: stats['ok' if not leftover else 'ok+spill']+=1
    else:
        stats['partial' if resolved else 'fails']+=1
        total=sum(r['marks'] for r in allrows)
        bad.append((str(key), f'marks {total} vs totals {sum(totals)}', totals, [r['marks'] for r in allrows][:60], f'resolved {len(resolved)}/{len(cs)} scale {scale}'))
print(stats, 'questions', len(groups), file=sys.stderr)
tot=[0,0]
for k in sorted(per): tot[0]+=per[k][0]; tot[1]+=per[k][1]
print(f'{tot[0]} of {tot[1]} tasks carry rows', file=sys.stderr)
def row_id(i, r): return f"r{i+1}"
sidecar={}
for cid in sorted(out):
    v=out[cid]
    rows=[]
    for i,r in enumerate(v['rows']):
        row={'id':row_id(i,r),'text':repaired(r['text']),'marks':r['marks'],'page':r['p']}
        if r.get('figure'): row['figure']=repaired(r['figure'])
        if r.get('block'): row['block']=True
        if r.get('inferred'): row['inferred']=True
        rows.append(row)
    sidecar[cid]={'how':v['how'],'rows':rows}
reasons={}
for b in bad:
    key=eval(b[0]); year,level,fid,q=key
    for c,tp in groups[key]:
        if c['id'] not in out and c['id'] not in gridcards: reasons[c['id']]=b[1]+' over the question; '+b[4]
for cid in gridcards: reasons[cid]='figures sit in a grid the geometry cannot label'
for c in cards:
    if c['id'] not in out and c['id'] not in reasons: reasons[c['id']]='task key or heading not read'
residue=[{'id':cid,'reason':reasons[cid]} for cid in sorted(reasons)]
if '--write' in sys.argv:
    json.dump({'note':'GENERATED by scripts/markbank/authoring/acc_rows.py from the scheme PDFs; do not edit by hand.','cards':sidecar}, open('components/MarkBank/cards/accounting/rows.json','w'), ensure_ascii=False, indent=1)
    json.dump({'note':'GENERATED by scripts/markbank/authoring/acc_rows.py: tasks whose scheme rows could not be lifted, with the reason.','tasks':residue}, open('scripts/markbank/authored/accounting-rows-residue.json','w'), ensure_ascii=False, indent=1)
    print(f'wrote rows for {len(sidecar)} tasks, {len(residue)} in the residue', file=sys.stderr)
