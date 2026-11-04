import json
from pathlib import Path
year = 2024
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
path = Path('scripts/markbank/authored/business-paper-reviews.json')
d = json.loads(path.read_text())
docs = {doc['paperFileid']: doc for doc in inv['documents'] if doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'}
notes = {
  'LC033ALP032EV.pdf': dict(scheme=[4] + list(range(14, 23)), pools=[], notes=[
    'Visually reviewed all 40 pages of the 2024 Section 1 and Answerbook booklet: cover (with the COVID-19 adjustment notice), instructions, the twelve short questions on pages 3-7 (including the company logos beside Q7), the Section 2 & 3 answerbook instructions, two graph-paper pages, 29 ruled answer pages and the back cover.',
    'Each short question was checked against the allocation table on scheme page 4 and support notes on pages 14-22. The fourteen existing IDs keep their ID and total with correction records. Q9(i), the 6-mark average-clause calculation, had no card and is added; the reconciliation ledger had flagged it as the only open 2024 Higher ask.',
    'Q1, Q2, Q4 and Q7 keep all five rows with the cumulative 3+2+2+2+1 tariff; keys come from the rendered scheme grids. Q12(ii) uses 0/2/4/5/6 and Q10 keeps the unequal 4/3/3 method-and-example split unattached to a named method. Break-even (Q4) and teamwork (Q12) move to their canonical topics.',
    'All nine raw selection matches in this booklet are classified. Topic Atlas uses the booklet-specific p1 identity for the short questions.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
  'LC033ALP041EV.pdf': dict(scheme=[5, 6, 7, 8, 9, 10, 11, 12, 13] + list(range(23, 59)), pools=['bus-2024-hl-s3-q3cii', 'bus-2024-hl-s3-q7ci', 'bus-2024-hl-s3-q8biii'], notes=[
    'Visually reviewed all twelve pages of the 2024 Sections 2 and 3 booklet, including the New Age Care case, every Section 3 extract and photograph, the CSO trade infographic, the Jackson Ltd cash flow table, the logos, the blank page 11 and the back cover. ABQ support pages 23-30 were reviewed previously; Section 3 was checked against allocation pages 6-13 and support pages 31-58.',
    'All 40 base Section 3 IDs keep their ID and total. Three finite printed pools are expanded: Q3(C)(ii) one of three EU policies (3 routes), Q7(C)(i) three of four financial terms (4 routes) and Q8(B)(iii) two of three businesses (3 routes, 6/5 split unattached). Each legacy pooled card keeps its ID as the first printed route, with a correction record; seven routes are new.',
    'The Q3(A)(ii) card supplies the infographic figures read from the rendered page (goods 72/34, services 93/84 in €bn) and keeps the 6 + 8 itemised marks. Q6(A) cards carry the full cash flow table; (ii) uses 0/3/5/7. Q4(C) keeps four 2+2 roles plus the two 2-mark evaluations. Unfair dismissal grounds and procedures move to industrial-relations law.',
    'All fifteen raw selection matches in this booklet are classified (the ABQ case match was reviewed earlier). Topic Atlas uses p2 for long questions and the ABQ.',
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
