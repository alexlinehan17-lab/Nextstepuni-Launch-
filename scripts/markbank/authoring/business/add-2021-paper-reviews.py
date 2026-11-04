import json
from pathlib import Path
year = 2021
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
path = Path('scripts/markbank/authored/business-paper-reviews.json')
d = json.loads(path.read_text())
docs = {doc['paperFileid']: doc for doc in inv['documents'] if doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'}
notes = {
  'LC033ALP032EV.pdf': dict(scheme=[4] + list(range(14, 21)), pools=[], notes=[
    'Visually reviewed all 36 pages of the 2021 Section 1 and Answerbook booklet (answer four of twelve): cover (with the COVID-19 adjustment notice), instructions, the twelve short questions on pages 3-8 (including the Camile and Pfizer logos), the Sections 2 and 3 answerbook instructions, two graph-paper pages, 25 ruled answer pages and the back cover.',
    'Each short question was checked against the allocation table on scheme PDF page 4 and support notes on pages 14-20. All sixteen legacy IDs keep their ID and total with correction records. Q1, Q2 and Q4 keep the cumulative 3,2,2,2,1 tariff with official keys; Q5 keeps the per-row state-agency marks 3/3/2/2; Q8(i) keeps the Stylish Tile & Bath figures and six one-mark points read from the rendered scheme; Q8(ii) supplies the 12.5% result.',
    'All ten raw selection matches in this booklet are classified. Topic Atlas uses the booklet-specific p1 identity for the short questions.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
  'LC033ALP041EV.pdf': dict(scheme=[5, 6, 7, 8, 9, 10, 11, 12, 13] + list(range(21, 59)), pools=['bus-2021-hl-s3-q3c'], notes=[
    'Visually reviewed all twelve pages of the 2021 Sections 2 and 3 booklet (answer three questions): the Miriam\'s Creche case, every Section 3 extract and image, the Moon Moods break-even data, the blank pages 10 and 11 and the back cover. ABQ support pages 21-26 were reviewed previously; Section 3 was checked against allocation pages 6-13 and support pages 27-58.',
    'All 33 base Section 3 legacy IDs keep their ID and total. The Q3(C) choose-two EU-policy pool is expanded into three routes (each policy 2 x 4 (2+2) + 2 evaluation); the legacy card keeps its ID as the first printed pair (CAP and Competition Policy), and two routes are new.',
    'Two new cards fill published boundaries no legacy card held: Q6(C)(ii) one other reward (7 marks) and Q7(B) the complete 25-mark break-even chart (the legacy indicator cards carried only the 12-mark calculation route and are labelled). Named variables, rewards, challenges and the first four development stages are required headings. Teamwork moves to HRM and unfair-dismissal redress to industrial relations.',
    'Summary/support conflicts are documented: Q1(A) third element (2+3+1) vs (2+2+2); Q6(A)(ii) header 10 vs 2 x 7. All six raw selection matches in this booklet are classified. Topic Atlas uses p2 for long questions and the ABQ.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
}
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['level'] == 'higher' and r['language'] == 'ev')]
for fileid, meta in notes.items():
    doc = docs[fileid]
    assert all(item['reviewStatus'] == 'reviewed' for item in doc['selectionDirectives']), fileid
    d['reviews'].append(dict(year=year, level='higher', language='ev', paperFileid=fileid, schemeFileid=doc['schemeFileid'],
        paperSha256=doc['paperSha256'], schemeSha256=doc['schemeSha256'], status='complete-paper-and-scheme-review',
        paperPagesReviewed=list(range(1, doc['paperPages'] + 1)), schemePagesReviewed=meta['scheme'],
        questionIdsReviewed=doc['paperTrailQuestionIds'], authoredCardIds=doc['authoredCardIds'], finiteRoutePoolIds=meta['pools'],
        reviewNotes=meta['notes']))
    print(fileid, len(doc['authoredCardIds']), doc['paperTrailQuestionIds'])
d['reviews'].sort(key=lambda r: (r['year'], r['paperFileid']))
path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
