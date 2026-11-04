#!/usr/bin/env python3
"""Construction Studies drawing rows as option groups: every detail the scheme prices, as an option the student claims.

    python3 scripts/markbank/authoring/construction_choices.py [--write]

An Ordinary Level drawing question is priced "Any 7 of the above details (5 marks each)": the scheme's
table lists each detail with its price — "19 mm external render 5", "Proprietary cavity closer 5" — and
the card offered one strip stepping by 5. Alex's rule (2026-10-23): what the scheme prices is a button with
its marks. The row becomes an anyN group (claimMax 7, perOption 5) whose options are the scheme's own detail
lines, read from the scheme PDF's table (construction_paper.sources, PyMuPDF): the lines between the
question's head and the row's own "Any N …" summary line that end in the unit price and carry words;
table furniture ("Sub-total", "Ceist") and lines priced for another row are not options; a line printed twice is
a detail drawn twice and stays twice. Higher Level prices the same way under PERFORMANCE CRITERIA, the part's
own tariff line ("(b) Any 4 × 4marks (Sketch 3 Annotation 1)") heading its labels; a first part whose tariff line
carries no letter ("Any 12 × 4marks", 2019 Q1(a)) lists its details as bullets under menu headings with the unit
price printed once per pair, and every bullet is an option. A row whose table yields fewer options than its
claim is left alone and reported. Complete-question cards mirror their task's
row. The row's id, text and marks are unchanged; the yearly validators carry the group in CHOICES and the
row without steps in LEAF (construction_paper.validate), so the card is still pinned to the paper.
"""
import json, re, os, sys, ast, collections, fitz
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import construction_paper as cp
ROOT=os.path.abspath(os.path.join(HERE,'..','..','..')); os.chdir(ROOT)
AUTHORED='scripts/markbank/authored/construction-studies.json'
DRAFT_2015='docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-q1-draft/q1-draft.json'
ANY=re.compile(r'^Any (\d+)\s*(?:of the above details|x|×)', re.I)
FURNITURE=re.compile(r'^(?:Sub-?total|Ceist|Question|Part|Total|Marks?|Details?|Quality of sketch(?:es)?)\b', re.I)
def lines_words(page):
    rows=collections.defaultdict(list)
    for w in page.get_text('words'): rows[round(w[1]/3)].append(w)
    return [sorted(v,key=lambda w:w[0]) for k,v in sorted(rows.items())]
def lines_of(page):
    return [' '.join(w[4] for w in ws) for ws in lines_words(page)]
def options_for(card, row):
    """The scheme's priced detail lines for a drawing row, or (None, reason)."""
    m=ANY.match(' '.join(row['verbatim'].split())); n=int(m.group(1)); per=row['marks']//n
    if per*n!=row['marks']: return None, f'{n} × {per} is not {row["marks"]}'
    year=card['year']; level=card['level']; qn=int(re.search(r'-q(\d+)', card['id']).group(1))
    P,S=cp.sources(year,level); doc=fitz.open(S)
    best=None
    for p in range(1, doc.page_count+1):
        page=doc[p-1]; W=page.rect.width; texts=lines_of(page)
        if not any(re.search(rf'^(?:Question|Ceist)\s+{qn}\b|^{qn}\.(?:\s|$)', t, re.I) for t in texts): continue
        stop=next((i for i,t in enumerate(texts) if ANY.match(t)), len(texts))
        opts=[]
        for t in texts[:stop]:
            mm=re.match(rf'^(.+?)\s+{per}$', t)
            if mm and re.search('[A-Za-z]', mm.group(1)) and not FURNITURE.match(mm.group(1)):
                opts.append(mm.group(1).strip())
        priced=list(opts)
        if len(opts)<n and stop<len(texts) and any(re.match(r'^(?:DETAILS|Details)\b.*(?:MARKS|Marks)', t) for t in texts[:stop]):
            # the 2020+ layout prints the price in its own column, often on its own baseline: the details are the
            # label lines between the table head ("DETAILS … MARKS" / "Part (a)") and the row's "Any N" line
            start=max([i for i,t in enumerate(texts[:stop]) if re.match(r'^(?:DETAILS|Part \(a\)|Details)', t)] or [-1])
            page=doc[p-1]; W=page.rect.width
            labels=[]
            for ws in lines_words(page)[start+1:stop]:
                t=' '.join(w[4] for w in ws)
                if ws[0][0]/W<0.3 and re.search('[A-Za-z]{3}', t) and not FURNITURE.match(t) and not ANY.match(t) and not re.match(r'^(?:Draw|Pipework|Vertical section|Given sketch|Horizontal section)', t) and not t.rstrip().endswith('.') and len(t.split())<=9:
                    t=re.sub(rf'\s+{per}$', '', t)
                    labels.append(t.strip())
            if len(labels)>=n: opts=labels
        part=re.search(r'-q\d+-([a-z])$', card['id'])
        head_i=next((i for i,t in enumerate(texts) if part and re.match(rf'^\({part.group(1)}\)\s+Any {n}\b', t, re.I)), None)
        if len(opts)<n and head_i is not None:
            # the Higher Level layout (PERFORMANCE CRITERIA | MAXIMUM MARK): the part's own tariff line, "(b) Any 4 × 4marks
            # (Sketch 3 Annotation 1)", heads its detail labels, one per line at the next indent until the next part's line;
            # the unit price sits in the MARK column on its own baseline or welded to a label ("Pump 4")
            labels=[]
            for ws in lines_words(page)[head_i+1:]:
                t=' '.join(w[4] for w in ws)
                if re.match(r'^\([a-z]\)', t) or re.match(r'^Total\b', t, re.I): break
                if re.fullmatch(r'\d+', t) or ws[0][0]/W>=0.4 or not re.search('[A-Za-z]{3}', t) or FURNITURE.match(t): continue
                labels.append(re.sub(rf'\s+{per}$', '', t).strip())
            if len(labels)>=n: opts=labels
        if len(opts)<n and part and part.group(1)=='a':
            # the Higher Level pool (2019 Q1(a)): the first part's tariff line carries no letter ("Any 12 × 4marks"), the details are
            # bulleted under their menu headings ("External Timber Frame Wall", "Triple Glazing"), and the MARK column prints the
            # unit price once per pair of bullets, so no detail line ends in its price; every bullet is an option, a heading is not
            rows_=lines_words(page); tariff_i=next((i for i,ws in enumerate(rows_) if ANY.match(' '.join(w[4] for w in ws))), None)
            if tariff_i is not None:
                labels=[]; pending=False
                for ws in rows_[tariff_i+1:]:
                    t=' '.join(w[4] for w in ws).strip()
                    if re.match(r'^\([a-z]\)', t) or re.match(r'^(?:Total|Scale)\b', t, re.I): break
                    if t in ('•','●','▪'): pending=True; continue
                    bullet=re.match(r'^[•●▪]\s*(.+)$', t)
                    if bullet: labels.append(re.sub(rf'\s+{per}$', '', bullet.group(1)).strip()); pending=False; continue
                    if pending and re.search('[A-Za-z]{3}', t): labels.append(re.sub(rf'\s+{per}$', '', t).strip()); pending=False; continue
                    pending=False
                if len(labels)>=n: opts=labels
        score=(1 if len(priced)>=n else 0, len(opts))
        if len(opts)>=n and (best is None or score>best[2]): best=(p, opts, score)
    if not best: return None, 'the scheme table does not list enough priced details'
    p,opts,_=best
    # a line the table prints twice is a detail the drawing shows twice, each at its price ("Stop valve 5" on two
    # valves, "70 x 20 mm architrave 4" each side of a door): both stay options
    uniq=opts
    texts=lines_of(doc[p-1])
    head=next((re.match(r'^((?:DETAILS|Details)(?:\s*[-–]\s*typical (?:sizes|details))?|PERFORMANCE CRITERIA)', t).group(1) for t in texts if re.match(r'^(?:DETAILS|Details|PERFORMANCE CRITERIA)\b', t)), 'Details')
    return {'page':p,'claimMax':n,'perOption':per,'options':uniq,'heading':head}, None
REASON=('The details the scheme lists for the drawing, each at its printed price, are the options of the row\'s group; '
        'the row itself, its text and its marks are unchanged.')
def as_group(row, res):
    row['kind']='anyN'; row.pop('permittedMarks', None); row.pop('parts', None)
    note=(row.get('contextNote') or '').strip()
    row['contextNote']=(row['verbatim'].strip()+('. '+note if note else ''))   # the printed tariff line stays as the row's note
    row['verbatim']=res['heading']
    row['group']={'claimMax':res['claimMax'],'perOption':res['perOption'],'options':res['options']}
def main():
    from construction_corrections import card_hash
    write='--write' in sys.argv
    cards=json.load(open(AUTHORED)); by_id={c['id']:c for c in cards}; stats=collections.Counter(); found={}; why={}
    for c in cards:
        if c.get('taskGroups'): continue
        for r in c['rows']:
            if r.get('kind')=='criterion' and ANY.match(' '.join(r['verbatim'].split())):
                res,w=options_for(c,r)
                if res: found[(c['id'],r['id'])]=res; stats['lifted']+=1
                else: why[(c['id'],r['id'])]=w; stats['left']+=1
    print(dict(stats), file=sys.stderr)
    for k,w in why.items(): print('LEFT', k, w, file=sys.stderr)
    if not write: return found, why
    import glob
    changed=[]
    for path in sorted(glob.glob('scripts/markbank/authored/construction-studies-*-reviewed.json')):
        review=json.load(open(path)); rcards={t['card']['id']:t['card'] for t in review['tasks']}
        before={cid:card_hash(c) for cid,c in rcards.items()}
        for cid,card in rcards.items():
            if 'taskGroups' in card: continue
            for r in card['rows']:
                if (cid,r['id']) in found: as_group(r, found[(cid,r['id'])])
        for card in rcards.values():
            for g in card.get('taskGroups', []):
                kid=rcards[g['sourceCardId']]; prefix=g['rowIds'][0][:len(g['rowIds'][0])-len(kid['rows'][0]['id'])]
                for kid_row,row in zip(kid['rows'], [r for r in card['rows'] if r['id'] in g['rowIds']]):
                    assert row['id']==prefix+kid_row['id'], (card['id'], row['id'])
                    if kid_row.get('kind')=='anyN' and (kid['id'],kid_row['id']) in found:
                        as_group(row, found[(kid['id'],kid_row['id'])])
        for cid,card in rcards.items():
            after=card_hash(card)
            if after!=before[cid]:
                fixes=[f for f in review.get('corrections',[])+review.get('revisions',[]) if f['cardId']==cid]
                if fixes:
                    assert fixes[0]['correctedSha256']==before[cid], (cid,'ledger does not hold the current hash')
                    fixes[0].setdefault('supersededSha256',[]).append(before[cid]); fixes[0]['correctedSha256']=after
                else:
                    review.setdefault('revisions',[]).append({'cardId':cid,'priorSha256':before[cid],'correctedSha256':after,'reason':REASON})
                assert cid in by_id, cid; by_id[cid]['rows']=card['rows']; changed.append(cid)
        open(path,'w').write(json.dumps(review, ensure_ascii=False, indent=2)+'\n')
    open(AUTHORED,'w').write(json.dumps(cards, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(changed)} cards changed', file=sys.stderr)
    if os.path.exists(DRAFT_2015):   # construction_2015_ordinary.py pins Q1 to this checkpoint draft: mirror the converted rows
        draft=json.load(open(DRAFT_2015)); k=0
        for t in draft['tasks']:
            live=by_id.get(t['card']['id'])
            for r in (t['card']['rows'] if live else []):
                lr=next((x for x in live['rows'] if x['id']==r['id']), None)
                if lr and lr.get('kind')=='anyN' and r.get('kind')!='anyN': r.clear(); r.update(json.loads(json.dumps(lr))); k+=1
        if k: open(DRAFT_2015,'w').write(json.dumps(draft, ensure_ascii=False, indent=2)+'\n'); print(f'{k} draft rows mirrored', file=sys.stderr)
    # the yearly validators: the row without steps in LEAF, the group in CHOICES
    per_file=collections.defaultdict(dict)
    for (cid,rid),res in found.items():
        c=by_id[cid]; key=re.sub(r'^cons-\d{4}-(?:hl|ol)-', '', cid)
        per_file[f"scripts/markbank/authoring/construction_{c['year']}_{c['level']}.py"][key]=(rid,res)
    for path,entries in sorted(per_file.items()):
        src=open(path).read()
        for key,(rid,res) in entries.items():
            pat=re.compile(r"(\('%s',\s*\d+,\s*)(?:list\(range\([^)]*\)\)|r\(\d+\)|\[[^\]]*\]|BAND\w*|None)(\))" % re.escape(rid))
            # only inside the LEAF entry of this key
            start=src.index("'%s':" % key, src.index('LEAF = {')); end=src.index('\n', start)
            seg=src[start:end]; new_seg,n=pat.subn(r"\1None\2", seg, count=1)
            assert n==1, (path, key, rid, seg[:120])
            src=src[:start]+new_seg+src[end:]
        entry='CHOICES.update({' + ', '.join("'%s': ('%s', %d, %d, %s)" % (key, rid, res['claimMax'], res['perOption'], json.dumps(res['options'], ensure_ascii=False)) for key,(rid,res) in sorted(entries.items())) + '})  # drawing details as option groups (construction_choices.py)\n'
        if 'construction_choices.py' not in src:
            node=next((x for x in ast.parse(src).body if isinstance(x, ast.Assign) and any(getattr(t,'id','')=='CHOICES' for t in x.targets)), None)
            if node:   # the dict may span several lines: insert after its last one
                lines=src.split('\n'); lines.insert(node.end_lineno, entry.rstrip('\n')); src='\n'.join(lines)
            else: src=src.replace('\nLEAF = {', '\nCHOICES = {}\n'+entry+'LEAF = {', 1)
        open(path,'w').write(src)
    print(f'{len(per_file)} validators patched', file=sys.stderr)
    return found, why
if __name__=='__main__': main()
