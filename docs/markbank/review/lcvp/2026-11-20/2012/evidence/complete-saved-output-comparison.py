"""Complete the saved183-output comparison; never rerun or alter the failed run."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,subprocess
D=Path(__file__).resolve().parent;R=D/'generator-isolation/run-20261120T120853Z-bd3d47b1';O=D/'saved-output-comparison';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
original={str(p.relative_to(R)):sha(p.read_bytes()) for p in R.rglob('*') if p.is_file()}
r=json.loads((R/'result.json').read_text());assert r['generatorExit']==0 and r['executed'] and not r['success']
assert r['failure']=="AssertionError(('lcvp-2011-cl-a7-2', 'rows', 'authored field changed or omitted'))"
assert r['laneSnapshotsUnchanged'] and r['laneBefore']==r['laneAfter'] and all(not v for v in r['snapshotDifferences'].values())
assert r['immutableSourceFilesUnchanged'] and r['frozenInputFilesUnchanged']
m=json.loads((D/'revision-input-manifest.json').read_text());assert sha((D/'revision-input-manifest.json').read_bytes())==r['compositionManifestSha256']
for p,h in m['immutablePacketFiles'].items():assert sha(Path(p).read_bytes())==h
for p,h in m['localFiles'].items():assert sha((D/p).read_bytes())==h
cards=json.loads((D/'review-183-fixture.json').read_text());generated=json.loads((R/'generated-183-asks.json').read_text());by={c['id']:c for c in generated}
assert len(cards)==len(generated)==len(by)==183 and set(by)=={c['id'] for c in cards}
assert sum(c['totalMarks'] for c in generated)==sum(c['totalMarks'] for c in cards)==840
expectedEmpty={'lcvp-2011-cl-a7-2','lcvp-2013-cl-b2i','lcvp-2013-cl-c1b','lcvp-2013-cl-c1b-2'};seen=set();fields=[]
for c in cards:
 g=by[c['id']];kept=[];omitted=[]
 for k,v in c.items():
  if k in ['figureKey','labelKey']:
   assert not v and k not in g;omitted.append(k);continue
  if ((k=='stem' and v=='') or (k=='additionalTopicIds' and v==[])) and k not in g:
   omitted.append(k);continue
  if k=='rows':
   adjusted=copy.deepcopy(v)
   assert len(g['rows'])==len(v)
   for index,row in enumerate(adjusted):
    if row.get('contextNote')=='' and 'contextNote' not in g['rows'][index]:
     assert c['id'] in expectedEmpty and index==0
     del row['contextNote'];seen.add(c['id']);omitted.append(f'rows[{index}].contextNote (empty string)')
   assert g[k]==adjusted,(c['id'],k)
  else:assert k in g and g[k]==v,(c['id'],k)
  kept.append(k)
 assert g['paperFileid']=='LC462CLP000EV' and g['schemeCitation']
 fields.append({'id':c['id'],'exactFields':kept,'documentedEmptySerializerOmissions':omitted,'paperFileid':g['paperFileid'],'schemeCitation':g['schemeCitation']})
assert seen==expectedEmpty
scratch=R/'scratch';builder=(scratch/'scripts/markbank/build-deck.mjs').read_text();assert "if (r.contextNote) parts.push(`contextNote: ${q(r.contextNote)}`);" in builder
iv=json.loads((D/'june-generator-input-inventory.json').read_text());initial={i['path']:i['sha256'] for i in iv['files']};initial['review-183-fixture.json']=sha((D/'review-183-fixture.json').read_bytes())
final={str(p.relative_to(scratch)):sha(p.read_bytes()) for p in scratch.rglob('*') if p.is_file()};changed={p for p in set(initial)|set(final) if initial.get(p)!=final.get(p)}
assert changed=={'components/MarkBank/cards/lcvp/common.ts','components/MarkBank/cards/sizes.json'}
N=Path('/Users/alexlinehan/Documents/Nextstepuni-Russian-Release-20261119');old=json.loads(subprocess.check_output(['git','--no-optional-locks','show',r['pin']+':components/MarkBank/cards/sizes.json'],cwd=N));new=json.loads((scratch/'components/MarkBank/cards/sizes.json').read_text());assert new['lcvp']=={'common':183};assert {k:v for k,v in old.items() if k!='lcvp'}=={k:v for k,v in new.items() if k!='lcvp'}
log=(R/'generator.stderr.log').read_text();assert 'built 183 cards, dropped 0' in log and 'LEDGER unavailable' in log;assert not any(s in log for s in ['DROPPED ','CORRECTED ','REPAIRED ','OVER CAP ','no paper in the Paper Trail index'])
assert original=={str(p.relative_to(R)):sha(p.read_bytes()) for p in R.rglob('*') if p.is_file()}
(O/'field-proof.json').write_text(json.dumps(fields,ensure_ascii=False,indent=2)+'\n')
result={'at':datetime.now(timezone.utc).isoformat(),'status':'Saved-output comparison passed; original run remains failed and unchanged','originalResult':str(R/'result.json'),'originalResultSha256':original['result.json'],'built':183,'dropped':0,'marks':840,'documentedEmptyContextOmissions':sorted(seen),'allNonemptyAuthoredFieldsPreserved':True,'bothOriginalLaneSnapshotsUnchanged':True,'allOriginalRunFilesUnchanged':True,'originalRunHashes':original,'scratchWrites':sorted(changed),'scope':'Selected source-payload compatibility only. No whole-deck reconciliation, Atlas, current application, hosted media, archive or production clearance.'}
(O/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='originalRunHashes'}))
