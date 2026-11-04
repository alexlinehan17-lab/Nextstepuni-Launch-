#!/usr/bin/env python3
"""Applied Mathematics: the printed lines each published step prices, as a crop of the scheme page.

    python3 scripts/markbank/authoring/am_steps.py [--write]

An Applied Mathematics card prices its solution in "Published step N" allocations (reviewed.json: 5 marks a
step, 2 for an attempt) beside a crop of the whole solution, so a student placing step 2 had to find step 2
in the crop. The scheme prints each step's marks in the right margin at the step's last line — "5" at the
margin on the 2010–2017 schemes, "(5)" right of the working from 2018 — so a step's own lines are the band of
the solution region from the step before it down to its mark. The text layer of these pages is equation-
editor fragments ("v 2 = u 2 + 2fs" scattered over three baselines), not words, so the step's content is
shown as a crop, never transcribed.

For each card the marks inside its solution region are read (a bracketed number right of the centre line, a
bare number in the margin — the 2013–14 Ordinary Level margin sits at x 0.67, so a bare number there counts
only with nothing printed right of it but a question total); "5, 5" or "5,5" on one line prices two steps
that end on that line, and both show its band; the marks inside the region are matched first and the band
just under it only when the region was drawn short of its last mark, so the next part's first mark never
displaces this part's own; the part total printed after the last step (20, 30, …) is not a step; a stray
number that is not a step's price (an equation's "4" that drifted into the margin) is dropped when the
remaining marks then match the steps one for one; cards that share one printed solution take their own
slice of its marks, after any mark of the part before caught at the top. A step priced beside a diagram
carries its mark at the figure's middle, not its last line, so a band is widened to the drawn figure (and
the labels just under it) that overlaps it, never past the next step's mark; the step after starts where
the widened band ends, and a step whose mark falls inside it shares it. A card whose marks do not
match its published steps in number and value keeps the whole-solution crop and is listed with its reason
in authored/applied-maths-steps-residue.json (empty). A "Published scale" prices the whole solution and
needs no cut. Nothing is typed: the regions are the page's own geometry.
"""
import fitz, json, re, os, sys, collections
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..','..')); os.chdir(ROOT)
PATH='components/MarkBank/cards/applied-maths/reviewed.json'
RESIDUE='scripts/markbank/authored/applied-maths-steps-residue.json'
BR=re.compile(r'^\((\d{1,2})\)$'); BARE=re.compile(r'^(\d{1,2})$')
docs={}
def doc(year,fid):
    if (year,fid) not in docs: docs[(year,fid)]=fitz.open(f'paper-trail-corpus/markingschemes/{year}/{fid}')
    return docs[(year,fid)]
def marks_in(card):
    """The marks printed in and just under the card's solution region, in reading order. "5,5" or "5, 5" on one line
    prices two steps that end on that line; `inside` is False for a mark in the band just under the region (the next
    part's first mark, when the region was drawn short)."""
    s=card['rubric']['solution']; out=[]
    for p,reg in zip(s.get('pages') or [], s.get('regions') or []):
        page=doc(card['year'],s['sourceFileid'])[p-1]; W,H=page.rect.width,page.rect.height
        words=page.get_text('words')
        for w in words:
            xf,y0,y1=w[0]/W,w[1]/H,w[3]/H
            if not (reg[1]-0.02<=y0<=reg[3]+0.03): continue
            for tok in [t for t in w[4].split(',') if t]:
                m=BR.match(tok)
                if m and xf>=0.45: out.append({'p':p,'y0':y0,'y1':y1,'x':xf,'n':int(m.group(1)),'inside':y0<=reg[3]+0.005}); continue
                m=BARE.match(tok)
                if not m or xf<0.66: continue
                # the 2013–14 OL margin sits at x 0.67, where a wide equation's last number can also fall: a margin mark has nothing printed right of it
                # (a question total of 15 or more printed beside it is not such a number)
                if xf<0.70 and any(w2[0]/W>w[2]/W and abs(w2[1]/H-y0)<0.012 and re.search(r'\d', w2[4]) and not (BARE.match(w2[4]) and int(w2[4])>=15) for w2 in words): continue
                out.append({'p':p,'y0':y0,'y1':y1,'x':xf,'n':int(m.group(1)),'inside':y0<=reg[3]+0.005})
    return sorted(out, key=lambda m:(m['p'],round(m['y0'],3),m['x']))
_drawn={}
def drawn(year,fid,p):
    """The page's drawn shapes as page-fraction boxes: a diagram's arrows and boxes, an equation's fraction bars and radicals."""
    if (year,fid,p) not in _drawn:
        page=doc(year,fid)[p-1]; W,H=page.rect.width,page.rect.height
        _drawn[(year,fid,p)]=[(d['rect'].x0/W,d['rect'].y0/H,d['rect'].x1/W,d['rect'].y1/H) for d in page.get_drawings() if d.get('rect') is not None and d['rect'].height>0]
    return _drawn[(year,fid,p)]
def cut(card, siblings=()):
    """[(allocation, region)] for the card's published steps, or (None, reason).

    siblings: the cards that share this card's solution region, in paper order — their steps are printed one
    after another inside it, so this card takes its own slice of the marks."""
    allocs=card['rubric']['allocations']; steps=[a for a in allocs if a['label'].startswith('Published step')]
    if not steps: return [], None
    s=card['rubric']['solution']; pages=s.get('pages') or []; regs=s.get('regions') or []
    if not regs or len(regs)!=len(pages): return None, 'solution has no regions'
    want=[max(a['credit']) for a in steps]; prices=set(want)
    found=marks_in(card)
    def match(found):
        got=[m for m in found if not (m['n']>max(want) and (m['n']==card['totalMarks'] or m['n']>=15))]
        if [m['n'] for m in got]==want: return got, None
        pruned=[m for m in got if m['n'] in prices]
        if [m['n'] for m in pruned]==want: return pruned, None
        if siblings:
            # the region is shared: the siblings' step prices, in order, are the whole print; a mark of the part before may sit at the top
            whole=[max(a['credit']) for sib in siblings for a in sib['rubric']['allocations'] if a['label'].startswith('Published step')]
            cand=pruned if [m['n'] for m in pruned]==whole else got if [m['n'] for m in got]==whole else pruned[-len(whole):] if len(pruned)>len(whole) and [m['n'] for m in pruned[-len(whole):]]==whole else None
            if cand is None: return None, f"margin marks {[m['n'] for m in got]} do not match the shared steps {whole}"
            start=sum(len([a for a in sib['rubric']['allocations'] if a['label'].startswith('Published step')]) for sib in siblings[:[x['id'] for x in siblings].index(card['id'])])
            return cand[start:start+len(want)], None
        if len(pruned)>len(want) and [m['n'] for m in pruned][-len(want):]==want:
            return pruned[-len(want):], None   # a mark of the part before, caught at the top of the region
        return None, f"margin marks {[m['n'] for m in got]} do not match the steps {want}"
    # the marks inside the region first; the band just under it only when the region was drawn short of its last mark
    got,why=match([m for m in found if m['inside']])
    if got is None: got,why=match(found)
    if got is None: return None, why
    out=[]; region_by_page={p:r for p,r in zip(pages,regs)}
    for i,(a,m) in enumerate(zip(steps,got)):
        r=region_by_page[m['p']]
        prev=got[i-1] if i>0 and got[i-1]['p']==m['p'] else None
        if prev and out and (abs(m['y0']-prev['y0'])<0.006 or m['y1']<=out[-1][1]['r'][3]-0.004):
            out.append((a, {'p':out[-1][1]['p'],'r':list(out[-1][1]['r'])})); continue   # "5, 5": two steps priced on one line, or a mark inside the step before's widened band, share it
        top=max(r[1], (prev['y1']+0.002) if prev else r[1], (out[-1][1]['r'][3]-0.0095) if out and out[-1][1]['p']==m['p'] else r[1])   # after a widened band, start where it ends (inside the gate's 0.01 overlap, clear of rounding)
        bottom=min(r[3], m['y1']+0.004)
        # a diagram's mark sits at the figure's middle: widen the band to the drawn figure that overlaps it, and the labels just under it
        nxt=got[i+1] if i+1<len(got) and got[i+1]['p']==m['p'] else None
        limit=max(bottom, min(r[3], nxt['y0']-0.002)) if nxt else r[3]
        # a figure is drawn as many strokes (boxes, arrows, a slope): the strokes within this step's reach, left of the marks
        # column, that touch the mark's line and each other, taken together; a wide, tall cluster that crosses the mark's line
        # is the figure, and the band runs to its foot and the labels just under it. A fraction bar, a radical, a brace over
        # two lines or the box round the marks column never make such a cluster.
        zone=[d for d in drawn(card['year'],s['sourceFileid'],m['p']) if d[0]<0.65 and d[2]>r[0] and d[1]>=top-0.01 and d[3]<=limit+0.01]
        seed=[d for d in zone if d[1]<bottom and d[3]>bottom-0.03]
        if seed:
            cl=list(seed); grew=True
            while grew:
                grew=False
                for d in zone:
                    if d in cl: continue
                    if any(d[0]<e[2]+0.015 and d[2]>e[0]-0.015 and d[1]<e[3]+0.015 and d[3]>e[1]-0.015 for e in cl): cl.append(d); grew=True
            x0=min(d[0] for d in cl); x1=max(d[2] for d in cl); y0_=min(d[1] for d in cl); ext=max(d[3] for d in cl)
            if x1-x0>0.05 and ext-y0_>0.03 and y0_<bottom<ext:
                page=doc(card['year'],s['sourceFileid'])[m['p']-1]; W,H=page.rect.width,page.rect.height
                labels=[w[3]/H for w in page.get_text('words') if w[0]/W<x1+0.03 and w[2]/W>x0-0.03 and ext-0.005<=w[1]/H<=ext+0.02]
                bottom=min(limit, max(bottom, (max(labels) if labels else ext)+0.004))
        if bottom-top<0.012: top=max(r[1], bottom-0.012, out[-1][1]['r'][3] if out and out[-1][1]['p']==m['p'] else r[1])   # reach up to the line, never into the step before
        if bottom-top<0.012: return None, f'step {i+1} would be thinner than a line'
        top=max(r[1], round(top,4)); bottom=min(r[3], round(bottom,4))
        out.append((a, {'p':m['p'],'r':[r[0], top, r[2], bottom]}))
    return out, None
def main():
    write='--write' in sys.argv
    raw=open(PATH,encoding='utf-8').read(); cards=json.loads(raw)
    assert json.dumps(cards,ensure_ascii=False,indent=2)+'\n'==raw, 'reviewed.json is not a byte-identical round trip'
    stats=collections.Counter(); residue=[]
    # cards whose solution regions are identical share one print of their steps
    byregion=collections.defaultdict(list)
    for c in cards:
        s=c['rubric']['solution']
        if s.get('regions'): byregion[(c['year'],c['level'],s['sourceFileid'],json.dumps(s['pages']),json.dumps(s['regions']))].append(c)
    for c in cards:
        for a in c['rubric']['allocations']: a.pop('region', None)
        group=byregion.get((c['year'],c['level'],c['rubric']['solution']['sourceFileid'],json.dumps(c['rubric']['solution'].get('pages')),json.dumps(c['rubric']['solution'].get('regions'))), [])
        result,why=cut(c, tuple(group) if len(group)>1 else ())
        if result is None: stats['residue']+=1; residue.append({'id':c['id'],'reason':why}); continue
        if not result: stats['scale only']+=1; continue
        for a,region in result: a['region']=region
        stats['cut']+=1
    print(dict(stats), file=sys.stderr)
    if write:
        open(PATH,'w',encoding='utf-8').write(json.dumps(cards,ensure_ascii=False,indent=2)+'\n')
        json.dump({'note':'GENERATED by scripts/markbank/authoring/am_steps.py: cards whose published steps could not be cut from the scheme page, with the reason.','cards':residue}, open(RESIDUE,'w'), ensure_ascii=False, indent=1)
        print(f"wrote step regions; {len(residue)} cards in the residue", file=sys.stderr)
if __name__=='__main__': main()
