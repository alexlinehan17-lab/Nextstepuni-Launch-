"""Promote the 2022 HL deferred EV census to a review and record its Atlas mappings (idempotent).

The deferred sitting is its own paper variant: fileid "LC034ALP000EV-deferred"
in the review (econ_review keys it apart from June's) and
"LC034ALP000EV-deferred.pdf" in the Atlas mappings, the id Paper Trail indexes.
"""
from pathlib import Path
import json, sys
W = str(Path(__file__).resolve().parents[5])
draft = json.load(open(f'{W}/scripts/markbank/authoring/drafts/economics-2022-hl-deferred-ev.json'))
review = dict(draft)
review['status'] = 'paper-and-scheme-boundaries-reviewed'
review['reviewNote'] = sys.argv[1] if len(sys.argv) > 1 else draft['reviewNote']
open(f'{W}/scripts/markbank/authoring/reviews/economics-2022-hl-deferred-ev.json', 'w').write(
    json.dumps(review, ensure_ascii=False, indent=2) + '\n')
path = f'{W}/data/examTopics/economics-sec-topic-reviews.json'
atlas = json.load(open(path))
key = lambda q: (q['level'], q['lang'], q['year'], q['fileid'], q['n'])
mine = []
for q in draft['questions']:
    mine.append({'level': 'higher', 'lang': 'ev', 'year': 2022, 'n': q['n'],
                 'fileid': 'LC034ALP000EV-deferred.pdf', 'pages': q['paperPages'],
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
    atlas['reviewedAt'] = '2026-11-04'
    atlas['reviewScope'] = ('Complete visual paper/scheme reviews: 2022–2024 Higher/Ordinary English/Irish; '
                            '2025 Higher and Ordinary English; 2026 Higher and Ordinary English; 2021 Higher '
                            'and Ordinary English (the 2021 Ordinary review replaces the targeted Q3 mapping); '
                            '2010-2019 Higher and Ordinary and 2020 Higher English (old syllabus; Section B keyed B1-B8 as the Atlas numbers it); '
                            'the 2022 Higher deferred sitting, English (its own paper, LC034ALP000EV-deferred.pdf). '
                            'Remaining 27 physical variants pending.')
open(path, 'w').write(json.dumps(atlas, ensure_ascii=False, indent=2))
print(len(mine), 'Atlas mappings;', sum(len(q['tasks']) for q in draft['questions']), 'routes')
