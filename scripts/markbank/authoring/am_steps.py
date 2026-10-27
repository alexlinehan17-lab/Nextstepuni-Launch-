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
bare number in the margin); the part total printed after the last step (20, 30, …) is not a step; a stray
number that is not a step's price (an equation's "4" that drifted into the margin) is dropped when the
remaining marks then match the steps one for one. A card whose marks do not match its published steps in
number and value keeps the whole-solution crop and is listed with its reason in
authored/applied-maths-steps-residue.json. A "Published scale" prices the whole solution and needs no cut.
Nothing is typed: the regions are the page's own geometry.
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
    s=card['rubric']['solution']; out=[]
    for p,reg in zip(s.get('pages') or [], s.get('regions') or []):
        page=doc(card['year'],s['sourceFileid'])[p-1]; W,H=page.rect.width,page.rect.height
        for w in page.get_text('words'):
            xf,y0,y1=w[0]/W,w[1]/H,w[3]/H
            if not (reg[1]-0.02<=y0<=reg[3]+0.03): continue
            m=BR.match(w[4])
            if m and xf>=0.45: out.append({'p':p,'y0':y0,'y1':y1,'n':int(m.group(1))}); continue
            m=BARE.match(w[4])
            if m and xf>=0.68: out.append({'p':p,'y0':y0,'y1':y1,'n':int(m.group(1))})
    return sorted(out, key=lambda m:(m['p'],m['y0']))
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
    got=[m for m in found if not (m['n']>max(want) and (m['n']==card['totalMarks'] or m['n']>=15))]
    if [m['n'] for m in got]!=want:
        pruned=[m for m in got if m['n'] in prices]
        if [m['n'] for m in pruned]==want: got=pruned
        elif siblings:
            # the region is shared: the siblings' step prices, in order, are the whole print
            whole=[max(a['credit']) for sib in siblings for a in sib['rubric']['allocations'] if a['label'].startswith('Published step')]
            cand=pruned if [m['n'] for m in pruned]==whole else got if [m['n'] for m in got]==whole else None
            if cand is None: return None, f"margin marks {[m['n'] for m in got]} do not match the shared steps {whole}"
            start=sum(len([a for a in sib['rubric']['allocations'] if a['label'].startswith('Published step')]) for sib in siblings[:[x['id'] for x in siblings].index(card['id'])])
            got=cand[start:start+len(want)]
        elif len(pruned)>len(want) and [m['n'] for m in pruned][-len(want):]==want:
            got=pruned[-len(want):]   # a mark of the part before, caught at the top of the region
        else: return None, f"margin marks {[m['n'] for m in got]} do not match the steps {want}"
    out=[]; region_by_page={p:r for p,r in zip(pages,regs)}
    for i,(a,m) in enumerate(zip(steps,got)):
        r=region_by_page[m['p']]
        prev=got[i-1] if i>0 and got[i-1]['p']==m['p'] else None
        top=max(r[1], (prev['y1']+0.002) if prev else r[1])
        bottom=min(r[3], m['y1']+0.004)
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
