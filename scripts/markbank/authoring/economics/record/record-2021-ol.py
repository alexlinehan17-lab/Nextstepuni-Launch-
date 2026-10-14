"""Promote the 2021 OL EV census to a review and record its Atlas mappings (idempotent).

The full review replaces the targeted 2021 Ordinary Q3 mapping.
"""
from pathlib import Path
import json, sys
W = str(Path(__file__).resolve().parents[5])
draft = json.load(open(f'{W}/scripts/markbank/authoring/drafts/economics-2021-ol-ev.json'))
review = dict(draft)
review['status'] = 'paper-and-scheme-boundaries-reviewed'
review['reviewNote'] = sys.argv[1] if len(sys.argv) > 1 else draft['reviewNote']
open(f'{W}/scripts/markbank/authoring/reviews/economics-2021-ol-ev.json', 'w').write(
    json.dumps(review, ensure_ascii=False, indent=2) + '\n')
path = f'{W}/data/examTopics/economics-sec-topic-reviews.json'
atlas = json.load(open(path))
key = lambda q: (q['level'], q['lang'], q['year'], q['fileid'], q['n'])
mine = []
for q in draft['questions']:
    mine.append({'level': 'ordinary', 'lang': 'ev', 'year': 2021, 'n': q['n'],
                 'fileid': 'LC034GLP000EV.pdf', 'pages': q['paperPages'],
                 'canonicalNodeIds': q['canonicalNodeIds'],
                 'reason': q['topicReason'] + ' ' + q['boundaryReason'],
                 'paperSha256': draft['paperSha256']})
keys = {key(q) for q in mine}
pos = {key(q): i for i, q in enumerate(atlas['questions'])}
if all(key(m) in pos for m in mine):
    # A re-run replaces each mapping where it stands; the scope note is left as it is.
    for m in mine:
        atlas['questions'][pos[key(m)]] = m
else:
    atlas['questions'] = [q for q in atlas['questions'] if key(q) not in keys] + mine
    atlas['reviewedAt'] = '2026-10-12'
    atlas['reviewScope'] = ('Complete visual paper/scheme reviews: 2022–2024 Higher/Ordinary English/Irish; '
                            '2025 Higher and Ordinary English; 2026 Higher and Ordinary English; 2021 Higher '
                            'and Ordinary English (the 2021 Ordinary review replaces the targeted Q3 mapping). '
                            'Remaining 48 physical variants pending.')
open(path, 'w').write(json.dumps(atlas, ensure_ascii=False, indent=2))
print(len(mine), 'Atlas mappings;', sum(len(q['tasks']) for q in draft['questions']), 'routes')
