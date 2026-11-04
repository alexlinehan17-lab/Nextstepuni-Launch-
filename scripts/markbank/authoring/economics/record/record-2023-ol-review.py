"""Promote the 2023 OL EV re-review census to the review and refresh its Atlas reasons (idempotent).

The Atlas node sets are unchanged (same routes and topics); only the reasons are
re-written from this sweep. The Irish review and its Atlas mappings are untouched.
"""
from pathlib import Path
import json, sys
W = str(Path(__file__).resolve().parents[5])
draft = json.load(open(f'{W}/scripts/markbank/authoring/drafts/economics-2023-ol-ev.json'))
review = dict(draft)
review['status'] = 'paper-and-scheme-boundaries-reviewed'
review['reviewNote'] = sys.argv[1] if len(sys.argv) > 1 else draft['reviewNote']
open(f'{W}/scripts/markbank/authoring/reviews/economics-2023-ol-ev.json', 'w').write(
    json.dumps(review, ensure_ascii=False, indent=2) + '\n')
path = f'{W}/data/examTopics/economics-sec-topic-reviews.json'
atlas = json.load(open(path))
key = lambda q: (q['level'], q['lang'], q['year'], q['fileid'], q['n'])
old = {key(q): q for q in atlas['questions']}
mine = []
for q in draft['questions']:
    entry = {'level': 'ordinary', 'lang': 'ev', 'year': 2023, 'n': q['n'],
             'fileid': 'LC034GLP000EV.pdf', 'pages': q['paperPages'],
             'canonicalNodeIds': q['canonicalNodeIds'],
             'reason': q['topicReason'] + ' ' + q['boundaryReason'],
             'paperSha256': draft['paperSha256']}
    prev = old.get(key(entry))
    if prev is None or sorted(prev['canonicalNodeIds']) != sorted(entry['canonicalNodeIds']) \
            or prev['pages'] != entry['pages']:
        sys.exit(f'Atlas mapping for Q{q["n"]} would change nodes or pages: {prev and prev["canonicalNodeIds"]}')
    mine.append(entry)
atlas['questions'] = [mine[[m['n'] for m in mine].index(q['n'])] if key(q) in {key(m) for m in mine} else q
                      for q in atlas['questions']]
open(path, 'w').write(json.dumps(atlas, ensure_ascii=False, indent=2))
print(len(mine), 'Atlas mappings refreshed;', sum(len(q['tasks']) for q in draft['questions']), 'routes')
