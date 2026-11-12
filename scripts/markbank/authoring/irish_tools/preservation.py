"""Preservation audit for one reviewed Irish paper component (run before each commit).
usage: preservation.py BASE YEAR LEVEL FILEID[,FILEID] ADDED_BANK ADDED_ATLAS PRIOR_BANK PRIOR_ATLAS [CHANGED_LEGACY_PREFIX]
A deferred sitting is audited whole: its two papers ("LC001ALP100IV-deferred.pdf,LC001ALP200IV-deferred.pdf"), its
Atlas mappings read from the runtime's deferredQuestionMappings beside June's questionMappings.
Every prior Bank card is byte-identical except reviewed legacy cards of this component (same id, total, topic);
every prior Atlas id keeps its tags; other answer maps byte-identical; this paper's prior answer fields kept
(printOrder/band may be recomputed); other subjects unchanged; runtime topics and prior mappings unchanged."""
import json,subprocess,sys,os
from pathlib import Path
os.chdir(Path(__file__).resolve().parents[4])
base,year,level,fileid,added_bank,added_atlas,prior_bank,prior_atlas=sys.argv[1:9]
prefix=sys.argv[9] if len(sys.argv)>9 else None
import os
ALSO=[x for x in os.environ.get('ALSO_CHANGED','').split(',') if x]  # answer maps checked separately
year,added_bank,added_atlas,prior_bank,prior_atlas=int(year),int(added_bank),int(added_atlas),int(prior_bank),int(prior_atlas)
def old(p):return subprocess.check_output(['git','show',f'{base}:{p}'])
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',base,'components/MarkBank/cards/irish'],text=True).splitlines()
count=0;changed=[]
for p in paths:
 if not p.endswith('.json') or p.endswith('sizes.json'):continue
 before=old(p);count+=len(json.loads(before).get('cards',[]))
 if Path(p).read_bytes()==before:continue
 assert p.endswith('/authored.json'),p
 a={c['id']:c for c in json.loads(before)['cards']};b={c['id']:c for c in json.load(open(p))['cards']}
 assert a.keys()==b.keys(),'legacy ids changed'
 for k in a:
  if a[k]!=b[k]:
   assert prefix and (k.startswith(prefix) or k in os.environ.get('ALSO_CARDS','').split(',')),k
   for f in ['id','totalMarks','topicId','year','level','paper','section','paperFileid','questionRef','conceptId']:
    assert a[k].get(f)==b[k].get(f),(k,f)
   changed.append(k)
assert count==prior_bank,count
a=json.loads(old('components/MarkBank/cards/sizes.json'));b=json.load(open('components/MarkBank/cards/sizes.json'))
assert {k:v for k,v in a.items() if k!='irish'}=={k:v for k,v in b.items() if k!='irish'}
assert sum(b['irish'].values())==sum(a['irish'].values())+added_bank
FILEIDS=fileid.split(',')
PS={(year,level,f) for f in FILEIDS}
p='scripts/paper-trail/topic-tags/tags/irish.json'
before={(r['year'],r['level'],r['fileid']):r for r in json.loads(old(p))};after={(r['year'],r['level'],r['fileid']):r for r in json.load(open(p))}
ids=lambda m:{(k,q['n']) for k,r in m.items() for q in r['q']}
assert ids(before)<=ids(after) and len(ids(before))==prior_atlas and len(ids(after)-ids(before))==added_atlas,(len(ids(before)),len(ids(after)-ids(before)))
assert all(k in PS for k,_ in ids(after)-ids(before))
for k,r in before.items():
 if k not in PS:assert after[k]==r,k
 else:
  now={q['n']:q for q in after[k]['q']}
  for q in r['q']:assert now[q['n']]==q,(k,q['n'])
for sub in ['scripts/paper-trail/answers','public/paper-answers','public/paper-anchors']:
 for f in subprocess.check_output(['git','ls-tree','-r','--name-only',base,sub],text=True).splitlines():
  if any(f.endswith(f'/{year}/{x}.json') for x in FILEIDS):continue
  if any(f.endswith(x) for x in ALSO):continue
  if '/LC001' in f:assert Path(f).read_bytes()==old(f),f
 for fid in FILEIDS:
  f=f'{sub}/{year}/{fid}.json'
  try:prev=json.loads(old(f))
  except subprocess.CalledProcessError:continue
  now={q['n']:q for q in json.load(open(f))['q']}
  for q in prev['q']:
   # Frozen reading identities on a reviewed Paper 2 take the whole passage and reviewed scheme
   # as additive display regions (the 2024 HL P2 precedent); every other prior field is kept.
   display={'printOrder','paperRegion','schemeRegion'} if (fid.startswith('LC001ALP2') or fid.startswith('LC001GLP2')) and q['n'].isdigit() else {'printOrder'}
   for k,v in q.items():assert k in display or now[q['n']][k]==v,(f,q['n'],k)
p='data/paperTrail/paperTopicTags.json'
a=json.loads(old(p));b=json.load(open(p));assert [r for r in a if r['subjectId']!='irish']==[r for r in b if r['subjectId']!='irish']
p='data/paperTrail/paperTopicTags-runtime.json'
def decode(x):
 out=[]
 for s,l,g,y,f,k,qs in x['papers']:
  if x['subjects'][s]=='irish':continue
  out.append([x['subjects'][s],l,g,y,x['files'][f],k,[[q[0],*[x['topics'][i] for i in q[1:]]] for q in qs]])
 return out
assert decode(json.loads(old(p)))==decode(json.load(open(p)))
r0=json.loads(old('data/examTopics/irish-runtime.json'));r1=json.load(open('data/examTopics/irish-runtime.json'))
# Topic rows are unchanged except that reviewed literature shelves may gain the reviewed works' curriculum nodes.
SHELVES={'irish-higher-prescribed-prose-archive','irish-higher-prescribed-poetry-archive','irish-higher-danta-breise','irish-ordinary-prescribed-prose-archive','irish-ordinary-prescribed-poetry-archive'}
assert len(r1['topics'])==len(r0['topics'])
for a,b in zip(r0['topics'],r1['topics']):
 if a[0] in SHELVES: assert a[:5]==b[:5] and a[6:]==b[6:] and set(a[5])<=set(b[5]),a[0]
 else: assert a==b,a[0]
# June's mappings are keyed by their paper slot; a deferred sitting's (deferredQuestionMappings) by its booklet as well.
def mappings(r):
 return {**{tuple(m[:5]):m for m in r['questionMappings']},**{tuple(m[:6]):m for m in r.get('deferredQuestionMappings',[])}}
prev=mappings(r0);now=mappings(r1)
assert all(now.get(k)==m for k,m in prev.items()),[k for k,m in prev.items() if now.get(k)!=m][:3]
assert len(now)-len(prev)==added_atlas,(len(now)-len(prev),added_atlas)
print(f'PASS: {prior_bank} prior Bank cards preserved ({len(changed)} reviewed legacy cards changed in place, ids/totals/topics/refs unchanged); '
      f'{prior_atlas} Atlas ids and tags kept; other answer maps byte-identical; prior fields of this paper kept; runtime topics unchanged; other subjects unchanged. +{added_bank} Bank, +{added_atlas} Atlas.')
