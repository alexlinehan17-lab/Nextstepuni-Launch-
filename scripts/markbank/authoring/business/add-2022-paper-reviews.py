import json
from pathlib import Path
year = 2022
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
path = Path('scripts/markbank/authored/business-paper-reviews.json')
d = json.loads(path.read_text())
docs = {doc['paperFileid']: doc for doc in inv['documents'] if doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'}
notes = {
  'LC033ALP032EV.pdf': dict(scheme=[4] + list(range(14, 21)), pools=[], notes=[
    'Visually reviewed all 36 pages of the 2022 Section 1 and Answerbook booklet (answer four of twelve): cover (with the COVID-19 adjustment notice), instructions, the twelve short questions on pages 3-8 (including the Coca Cola and myAccount images), the Sections 2 and 3 answerbook instructions, two graph-paper pages, 25 ruled answer pages and the back cover.',
    'Each short question was checked against the allocation table on scheme page 4 and support notes on pages 14-20. All fourteen legacy IDs keep their ID and total with correction records. Q1, Q2, Q4 and Q7 keep the cumulative 3,2,2,2,1 tariff with official keys; Q5 keeps the email format (5 @ 1) and two rights (3, 2); Q9 keeps the Fleming Ltd data and 3,3,2,2; Q12 keeps the 4,4,2 PAYE marks with the 2-mark partial credit for one tax credit.',
    'All ten raw selection matches in this booklet are classified. Topic Atlas uses the booklet-specific p1 identity for the short questions.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
  'LC033ALP041EV.pdf': dict(scheme=[5, 6, 7, 8, 9, 10, 11, 12, 13] + list(range(21, 58)), pools=['bus-2022-hl-s3-q2a', 'bus-2022-hl-s3-q6c', 'bus-2022-hl-s3-q8c'], notes=[
    'Visually reviewed all twelve pages of the 2022 Sections 2 and 3 booklet (answer three questions): the Mike\'s Pizza case, every Section 3 extract and image, the Cleaning Crew table, the blank page 11 and the back cover. ABQ support pages 21-27 were reviewed previously; Section 3 was checked against allocation pages 6-13 and support pages 28-57.',
    'All 34 base Section 3 IDs keep their ID and total. Three finite printed pools are expanded: Q2(A) one of two company types (2 routes), Q6(C) any three of four taxation headings (4 routes, 7/7/6 unattached) and Q8(C) any three of four advertising types (4 routes, 7/7/6 unattached). Each legacy pooled card keeps its ID as the first printed route; seven routes are new.',
    'Stakeholders (Q1(A)(ii)), HR functions (Q6(A)) and leadership styles (Q5(A)) are open choices. Q1(C)(ii) grounds use 0/3/6/8/10/12. Q7(A)(ii) keeps formula 3 and 2 x 6 (2+1+1+2) with the full table; (iii) supplies the two ratios. The support notes restate Q3(B)(ii) as opportunities of exporting internationally; the card follows the paper. Discrimination moves to industrial-relations law and indigenous business to categories of industry.',
    'All eighteen raw selection matches in this booklet are classified. Topic Atlas uses p2 for long questions and the ABQ.',
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
