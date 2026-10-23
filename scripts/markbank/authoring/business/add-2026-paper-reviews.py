import json
from pathlib import Path
year = 2026
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
path = Path('scripts/markbank/authored/business-paper-reviews.json')
d = json.loads(path.read_text())
docs = {doc['paperFileid']: doc for doc in inv['documents'] if doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'}
notes = {
  'LC033ALP032EV.pdf': dict(scheme=[5] + list(range(13, 22)), notes=[
    'Visually reviewed all 40 pages of the Section 1 and Answerbook booklet: cover, instructions, the twelve short questions on pages 3–8, the Section 2 & 3 answerbook instructions, two graph-paper pages, 28 ruled answer pages and the back cover.',
    'Each short question was checked against the Section 1 allocation table on scheme page 5 and support notes on pages 13–21. Q4, Q6 and Q10 split at their printed sub-part allocations (5/5, 6/4, 4/3/3). Q2, Q5, Q7 and Q9 keep all five rows with the cumulative 3+2+2+2+1 tariff and the official answer keys.',
    'Q10 cards each retain the full Delectable Delights figure table, so the margin of safety can be practised without the preceding card; the scheme marks shaded answers on own figures. Q11 keeps organic and inorganic growth together as required headings with examples.',
    'All nine raw selection matches in this booklet are classified. Topic Atlas uses the booklet-specific p1 identity for the short questions.',
    'This source-pinned record covers the English Higher booklet only. Source hashes and exact ID sets detect stale evidence; parser counts do not independently prove completeness.']),
  'LC033ALP041EV.pdf': dict(scheme=[6, 7, 8, 9, 10, 11, 12] + list(range(22, 71)), notes=[
    'Visually reviewed all twelve pages of the Sections 2 and 3 booklet, including the Coffee & Chill case, every Section 3 extract, the Swift Ltd and industry-average tables, the blank page 11 and the back cover. ABQ support pages 22–27 were reviewed previously; Section 3 was checked against allocation pages 7–12 and support pages 28–70.',
    'Section 3 splits at the printed and published sub-part allocations. Required pairs and bulleted headings stay whole: condition/warranty, both stakeholder pairs, constructive/unfair dismissal, customers/investors, benefits and challenges, short- and long-term implications. Q7(A) keeps the diagram (10) and stage actions (10) in one card because one printed task asks for both about the same chosen product.',
    'Q7(B) splits into the four ratio calculations at 4/4/5/7 with the full Swift Ltd table on each card; Q7(C) carries the data and industry averages, and its guidance gives the scheme’s part (B) results. Evaluation allowances (Q1(C), Q4(C), Q5(C), Q8(B)(ii)) are separate 2-mark responses. Q3(C) keeps the 2-mark position with either Yes or No accepted.',
    'No finite printed choose-k pool occurs. All four raw selection matches in this booklet are classified. Topic Atlas uses p2 for long questions and the ABQ.',
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
