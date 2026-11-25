import json,glob,os,collections,re,random
random.seed(7)
PAT={
 'dash_run': re.compile(r'[-–—_]{3,}|(?:[-–—] ){3,}'),
 'dot_leader': re.compile(r'\.{4,}|…{2,}|(?:\. ){4,}'),
 'pipe_table': re.compile(r'\|.*\|'),
 'slash_sep': re.compile(r'\s/\s.*\s/\s.*\s/\s'),
 'multi_slash': re.compile(r'//'),
 'repl_char': re.compile(r'[�□-]'),
 'ctrl': re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]'),
 'newline_heavy': re.compile(r'(?:\n[^\n]{0,40}){6,}'),
 'caret_math': re.compile(r'\^|_\{|\\frac|sqrt\('),
 'flat_fraction': re.compile(r'\(\S[^()]{0,30}\)/\(\S[^()]{0,30}\)'),
 'spaced_nums': re.compile(r'(?:\b\d[\d,.]*\s+){6,}'),
 'double_space': re.compile(r'\S {3,}\S'),
 'embedded_marks': re.compile(r'\(\d{1,3}\s*marks?\)|\[\d{1,3}\]|\(\d{1,2}\)\s*$'),
 'sibling_parts': re.compile(r'(?:^|\s)\((?:[a-h]|i{1,3}|iv|v|vi{0,3})\)\s+\S.*\s\((?:[a-h]|i{1,3}|iv|v|vi{0,3})\)\s+\S.*\s\((?:[a-h]|i{1,3}|iv|v|vi{0,3})\)\s'),
 'orphan_bracket': re.compile(r'^\W|\(\s*\)|\[\s*\]'),
 'allcaps_run': re.compile(r'(?:\b[A-Z]{4,}\b\s+){5,}'),
 'hyphen_break': re.compile(r'[a-z]-\s[a-z]{2,}'),
}
def strings(o,path=''):
    if isinstance(o,str): yield path,o
    elif isinstance(o,list):
        for x in o: yield from strings(x,path)
    elif isinstance(o,dict):
        for k,v in o.items():
            if k in ('src','srcHash','candId','id','attribution','schemeCitation','sourceFileid','paperFileid','playbackUrl','canonicalUrl','secFileid','alt','presentationNote','specVersion','conceptId','topicId','subjectId'): continue
            yield from strings(v,k)
Q=('stem','questionText','questionChoices','practiceFocus')
res={}
samples=collections.defaultdict(lambda: collections.defaultdict(list))
for f in sorted(glob.glob('decks/*__*.json')):
    s=os.path.basename(f).split('__')[0]
    r=res.setdefault(s,{'n':0,'q':collections.Counter(),'a':collections.Counter(),'qlen':[],'alen':[],'rows':[]})
    for c in json.load(open(f)):
        r['n']+=1
        qtxt=' '.join(str(c.get(k) or '') for k in ('stem','questionText'))
        r['qlen'].append(len(qtxt))
        qf=set(); af=set(); al=0
        for p,t in strings({k:c.get(k) for k in Q}):
            for n,rx in PAT.items():
                if rx.search(t): qf.add(n); samples[s]['q:'+n].append((c['id'],t[:300]))
        for p,t in strings({k:v for k,v in c.items() if k in ('rows','rubric','answerVariants','notes','questionBonus','taskGroups')}):
            al+=len(t)
            for n,rx in PAT.items():
                if rx.search(t): af.add(n); samples[s]['a:'+n].append((c['id'],t[:300]))
        r['alen'].append(al); r['rows'].append(len(c.get('rows') or []))
        r['q'].update(qf); r['a'].update(af)
out={}
for s,r in res.items():
    n=r['n']; med=lambda L: sorted(L)[len(L)//2]; p95=lambda L: sorted(L)[int(len(L)*.95)]
    out[s]={'n':n,'q':{k:round(100*v/n,1) for k,v in r['q'].items() if v/n>0.005},'a':{k:round(100*v/n,1) for k,v in r['a'].items() if v/n>0.005},'qlen_med':med(r['qlen']),'qlen_p95':p95(r['qlen']),'alen_med':med(r['alen']),'alen_p95':p95(r['alen']),'rows_med':med(r['rows']),'rows_p95':p95(r['rows'])}
json.dump(out,open('textaudit.json','w'),indent=1)
json.dump({s:{k:random.sample(v,min(6,len(v))) for k,v in d.items()} for s,d in samples.items()},open('textsamples.json','w'),ensure_ascii=False,indent=1)
for s,o in out.items(): print(s,o['n'],'Q',o['q'],'| A',o['a'],'| qlen',o['qlen_med'],o['qlen_p95'],'alen',o['alen_med'],o['alen_p95'],'rows',o['rows_med'],o['rows_p95'])
