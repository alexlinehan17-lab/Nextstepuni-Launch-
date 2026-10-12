"""Cross-check the four source-validated draft packages against integrated data."""
from pathlib import Path
import json,hashlib,importlib
import construction_corrections
R=Path(__file__).resolve().parents[3]
def read(p):return json.loads(p.read_text())
def validate():
 main=read(R/'scripts/markbank/authored/construction-studies-2015-higher-reviewed.json');auth=read(R/'scripts/markbank/authored/construction-studies.json');by={c['id']:c for c in auth};manifest=read(R/'components/MarkBank/figures-construction-studies.json');bridge=read(R/'scripts/markbank/atlas-reviews/construction-studies-2015-higher.json');reviewed={t['card']['id']:t for t in main['tasks']};bindings={b['cardId']:b for b in main['bindings']};bridges={b['cardId']:b for b in bridge['cards']};figures={f['key']:f for f in main['questionFigures']};counts=[]
 for q,n in [(3,576),(4,577),(5,578),(6,579)]:
  a=R/f'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q{q}-draft';d=read(a/f'q{q}-draft.json');module=importlib.import_module(f'construction_2015_higher_q{q}');result=module.validate(d);counts.append(result)
  assert d['sourceHashes']==main['sourceHashes']==bridge['sourceHashes']and main['questionRouteLedgers'][str(q)]==d['routeLedger']
  for t in d['tasks']:assert reviewed[t['card']['id']]==t and by[t['card']['id']]==t['card']
  for b in d['bindings']:assert bindings[b['cardId']]==b==bridges[b['cardId']]
  for f in d['questionFigures']:
   assert figures[f['key']]==f;entry=manifest[f['key']];image=R/'public'/entry['src'].lstrip('/');assert hashlib.sha256(image.read_bytes()).hexdigest()==f['sha256']and hashlib.md5(image.read_bytes()).hexdigest()==entry['md5']and entry['solution']==f['solution']
 prior=read(R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q3-q6-integration/prior-authored-cards.json');assert len(prior)==512;construction_corrections.assert_prior_cards_preserved({c['id']:construction_corrections.card_hash(c) for c in prior},by)  # byte-identical, or a later review's recorded, hash-linked in-place correction
 assert len(by)==len(auth)and set(bridge['cards'][i]['cardId']for i in range(len(bridge['cards'])))==set(reviewed)and bridge['expectedRuntimeCards']==len(reviewed)
 assert {'1','2','3','4','5','6'}<=set(main['questionsReviewed'])and set(main['unreviewedQuestions'])==set(map(str,range(1,11)))-set(main['questionsReviewed'])
 return dict(tasks=sum(x['tasks']for x in counts),sourceFigures=sum(x['figures']for x in counts),wholeQuestionRoutes=sum(x['wholeQuestionRoutes']for x in counts),paperComplete=False)
if __name__=='__main__':print(json.dumps(validate()))
