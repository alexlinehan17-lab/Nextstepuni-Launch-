import json
from pathlib import Path
year = 2025
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
path = Path('scripts/markbank/authored/business-paper-reviews.json')
d = json.loads(path.read_text())
docs = {doc['paperFileid']: doc for doc in inv['documents'] if doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'}
notes = {
  'LC033ALP032EV.pdf': dict(scheme=[5] + list(range(12, 18)), notes=[
    'Visually reviewed all 40 pages of the 2025 Section 1 and Answerbook booklet: cover (with the COVID-19 adjustment notice), instructions, the twelve short questions on pages 3-7, the Section 2 & 3 answerbook instructions, two graph-paper pages, 29 ruled answer pages and the back cover.',
    'Each short question was checked against the allocation table on scheme page 5 and support notes on pages 12-17. All sixteen existing card IDs already sat at published boundaries (Q2, Q7, Q9 and Q11 split at 6/4, 5/5, 5/5 and 6/4). Each keeps its ID and total and moves to the reviewed rubric renderer with a correction record.',
    'Q1, Q3 and Q4 keep all five rows with the cumulative 3,2,2,2,1 tariff; the Q1 key (1 D, 2 E, 3 A, 4 C, 5 F) is printed as an image grid on scheme page 12 and was read from the rendered page. Q7(b) keeps the Korn Ltd figures, including the authorised share capital distractor, and its five one-mark points.',
    'All six raw selection matches in this booklet are classified. Topic Atlas uses the booklet-specific p1 identity for the short questions.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
  'LC033ALP041EV.pdf': dict(scheme=[6, 7, 8, 9, 10, 11] + list(range(18, 52)), notes=[
    'Visually reviewed all twelve pages of the 2025 Sections 2 and 3 booklet, including the Inis Bia case, every Section 3 extract, the Gemma tax table, the P&G break-even data, the blank page 11 and the back cover. ABQ support pages 18-24 were reviewed previously; Section 3 was checked against allocation pages 7-11 and support pages 25-51.',
    'All 36 existing Section 3 IDs keep their ID and total and move to the rubric renderer with correction records. Discrimination (Q1(C)) and fair-dismissal grounds (Q4(B)) move from HRM to industrial-relations law, matching the question topics. Q7(C) hire purchase, loan and leasing become open source responses plus the two one-mark needs.',
    'Named items with unequal (4+1),(4+1),(3+2),(3+2) splits (contract elements, organisation types, trade barriers, termination methods, hotel insurance) stay together with ordered responses rather than tying the larger split to a named item. Required pairs stay whole. The Q6(C) tax cards keep the scheme’s itemised marks; (iv) supplies the scheme results of (i)-(iii).',
    'Q8(C) is one 25-mark chart task. A new complete-chart card carries the full published allocation and the 12-mark calculations-only limit. The five legacy component IDs (title and axes, chart lines, and the three indicators) are retained for saved progress and labelled as components; the indicator cards accept chart or calculation. No finite printed choose-k pool occurs, and all three raw selection matches are classified.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
}
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['level'] == 'higher' and r['language'] == 'ev')]
for fileid, meta in notes.items():
    doc = docs[fileid]
    assert all(item['reviewStatus'] == 'reviewed' for item in doc['selectionDirectives']), fileid
    d['reviews'].append(dict(year=year, level='higher', language='ev', paperFileid=fileid, schemeFileid=doc['schemeFileid'],
        paperSha256=doc['paperSha256'], schemeSha256=doc['schemeSha256'], status='complete-paper-and-scheme-review',
        paperPagesReviewed=list(range(1, doc['paperPages'] + 1)), schemePagesReviewed=meta['scheme'],
        questionIdsReviewed=doc['paperTrailQuestionIds'], authoredCardIds=doc['authoredCardIds'], finiteRoutePoolIds=[],
        reviewNotes=meta['notes']))
    print(fileid, len(doc['authoredCardIds']), doc['paperTrailQuestionIds'])
d['reviews'].sort(key=lambda r: (r['year'], r['paperFileid']))
path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
