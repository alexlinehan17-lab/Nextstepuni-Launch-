import json
from pathlib import Path

def record(year, level, notes):
    inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
    path = Path('scripts/markbank/authored/business-paper-reviews.json')
    d = json.loads(path.read_text())
    docs = {doc['paperFileid']: doc for doc in inv['documents'] if doc['year'] == year and doc['level'] == level and doc['language'] == 'ev'}
    d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['level'] == level and r['language'] == 'ev')]
    for fileid, meta in notes.items():
        doc = docs[fileid]
        assert all(item['reviewStatus'] == 'reviewed' for item in doc['selectionDirectives']), fileid
        d['reviews'].append(dict(year=year, level=level, language='ev', paperFileid=fileid, schemeFileid=doc['schemeFileid'],
            paperSha256=doc['paperSha256'], schemeSha256=doc['schemeSha256'], status='complete-paper-and-scheme-review',
            paperPagesReviewed=list(range(1, doc['paperPages'] + 1)), schemePagesReviewed=meta['scheme'],
            questionIdsReviewed=doc['paperTrailQuestionIds'], authoredCardIds=doc['authoredCardIds'], finiteRoutePoolIds=meta.get('pools', []), **({'finiteChoiceCardIds': meta['choices']} if meta.get('choices') else {}),
            reviewNotes=meta['notes']))
        print(fileid, len(doc['authoredCardIds']), doc['paperTrailQuestionIds'])
    d['reviews'].sort(key=lambda r: (r['year'], r['level'], r['paperFileid']))
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
