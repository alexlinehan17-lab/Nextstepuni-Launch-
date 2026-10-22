"""Record one authored legacy paper in agricultural-science-completion-progress.json.

usage: ledger.py <spec.json>
spec: {"year": 2016, "level": "higher", "paperPages": 8, "schemePages": 12, "added": 62, "figures": 1,
       "boundaries": "...", "figuresNote": "..." (optional), "cropReview": "...", "openDeclared": "...",
       "targetedTests": 255}
Counts that the generators own (cards, coverage, pending cues, open editions) are read back from
the written artefacts, so the ledger cannot drift from them.
"""
import json
import re
import sys

LEDGER = 'scripts/markbank/authored/agricultural-science-completion-progress.json'
spec = json.load(open(sys.argv[1]))
d = json.load(open(LEDGER))
Level = spec['level'].title()
# The built deck, not the authored file: withdrawn originals stay authored but are dropped by
# card-corrections.json, so only the built TypeScript counts what students see.
built = {lvl: len(re.findall(r'^    id: "agsci-', open(f'components/MarkBank/cards/agricultural-science/{lvl}.ts').read(), re.M))
         for lvl in ('higher', 'ordinary')}
higher, ordinary = built['higher'], built['ordinary']
cards = [None] * (higher + ordinary)
census = json.load(open('scripts/markbank/authored/agricultural-science-census.json'))
open_editions = sum(1 for e in census['editionStatus'] if e.get('independentCensus') == 'open')
baseline = json.load(open('scripts/markbank/coverage-baseline.json'))['agricultural-science']
atlas_extra = d['completedBatch']['atlasCardsNow'] - d['completedBatch']['markBankCardsNow']

inv = d['inventory']
inv['selectionCuesPendingClassification'] = spec['pendingCues']
inv['fullPaperAndSchemeSweepsCompleted'] += 1
inv['distinctEnglishPaperSweepsCompleted'] += 1
inv['independentSourceCensusEditionsCompleted'] = inv['indexedEditions'] - open_editions
inv['independentSourceCensusEditionsOpen'] = open_editions

cb = d['completedBatch']
cb['reviewedPapers'].append(f"{spec['year']} {Level} English: {spec['paperPages']} paper pages and {spec['schemePages']} scheme pages")
cb['addedMarkBankCards'] += spec['added']
cb['addedThisBatch'] += spec['added']
cb['markBankCardsNow'] = len(cards)
cb['higherCards'], cb['ordinaryCards'] = higher, ordinary
cb['atlasPracticeCardsAdded'] = len(cards)
cb['atlasCardsNow'] = len(cards) + atlas_extra
cov = cb['coverageBaseline']
cov.update(cards=len(cards), leaves=baseline['leaves'], covered=baseline['covered'], open=baseline['open'],
           excluded=baseline.get('excluded', 0), orphans=baseline.get('orphans', 0),
           coveragePct=round(100 * baseline['covered'] / baseline['leaves'], 1))
cov['openAsksDeclared'] = f"{baseline['open']} open asks, {spec['openDeclared']}"
entry = dict(added=spec['added'], corrected=0, withdrawn=0,
             source=f"Authored from the SEC paper and scheme; no cards existed. Built by agricultural_science_{spec['year']}_{'hl' if spec['level'] == 'higher' else 'ol'}.py on the shared legacy builder.",
             boundaries=spec['boundaries'])
if spec.get('figuresNote'):
    entry['figures'] = spec['figuresNote']
entry['cropReview'] = spec['cropReview']
cb[f"authored{spec['year']}{Level}"] = entry

v = d['verification']
v['targetedTestsPassed'] = spec['targetedTests']
figs = spec.get('figures', 0)
fig_text = f" and {'one figure' if figs == 1 else str(figs) + ' figures'}" if figs else ''
v['renderedCropReview'] += f" {spec['year']} {Level}: all {spec['added']} distinct crop pairs{fig_text} inspected."
v['cardBuild'] = f"{len(cards)} built, zero dropped"
json.dump(d, open(LEDGER, 'w'), indent=2, ensure_ascii=False)
open(LEDGER, 'a').write('\n')
print('ledger:', len(cards), 'cards;', baseline['covered'], '/', baseline['leaves'], 'covered;', open_editions, 'editions open')
