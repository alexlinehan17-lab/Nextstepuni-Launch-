import json
from pathlib import Path
year = 2023
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
path = Path('scripts/markbank/authored/business-paper-reviews.json')
d = json.loads(path.read_text())
docs = {doc['paperFileid']: doc for doc in inv['documents'] if doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'}
notes = {
  'LC033ALP032EV.pdf': dict(scheme=[6] + list(range(16, 24)), notes=[
    'Visually reviewed all 40 pages of the 2023 Section 1 and Answerbook booklet: cover (with the COVID-19 adjustment notice), instructions, the twelve short questions on pages 3-10 (including the Elverys and WhatsApp images), the Section 2 answerbook instructions, two graph-paper pages, 26 ruled answer pages and the back cover.',
    'Each short question was checked against the allocation table on scheme PDF page 6 and support notes on pages 16-23. All eighteen legacy IDs keep their ID and total with correction records. Q2, Q4 and Q9 keep the cumulative 3,2,2,2,1 tariff with the official keys; Q3(b) keeps the four data figures and the six marks read from the rendered scheme (visible imports 2, each balance and surplus 1).',
    'Q5(a) is a 6-mark (3@2m) diagram. A new complete card carries all three 2-mark components; the legacy 4-mark card keeps its ID as the two components the scheme names (title and production department). The held third-component card remains held. Indigenous-firm cards move to categories of industry.',
    'All nine raw selection matches in this booklet are classified. Topic Atlas uses the booklet-specific p1 identity for the short questions.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
  'LC033ALP041EV.pdf': dict(scheme=[7, 8, 9, 10, 11, 12, 13, 14, 15] + list(range(24, 61)), notes=[
    'Visually reviewed all twelve pages of the 2023 Sections 2 and 3 booklet, including the Crowley Housebuilders case, every Section 3 extract and image, the Tommy tax table, the MJ Sports break-even data, the blank page 11 and the back cover. ABQ support pages 24-29 were reviewed previously; Section 3 was checked against allocation pages 8-15 and support pages 30-60.',
    'All 39 legacy Section 3 IDs keep their ID and total. Q1(A) stays as the scheme\'s two 10-mark relationship blocks with the full printed question restored on both. Unequal splits (Q1(C), Q2(B), Q3(C)) are not tied to named items. Q3(B) evaluation uses 0/1/3. Q7(B) tax cards keep the itemised marks and (iv) supplies the scheme results of (i)-(iii).',
    'Q8(C): a new complete 25-mark chart card carries all nine published elements, including the X-axis mark that no legacy card held; the legacy calculations-only (12) and chart-component cards keep their IDs and are labelled. Summary/support allocation conflicts (Q2(A), Q6(A)(ii), Q7(C)(ii), the Unfair Dismissals Act date) are documented; cards follow the summary and the paper.',
    'No finite printed choose-k pool occurs, and both raw selection matches in this booklet are classified. Topic Atlas uses p2 for long questions and the ABQ.',
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
