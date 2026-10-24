"""Field values edited after their generator ran, re-applied so a replay reproduces the committed cards.

These ten edits were made to the 2013, 2015 and 2019 Higher cards after generation, in the work that
became the 2026-10-11 checkpoint (3643e3529), and no script recorded them: the 2013 short-question and
worked-table marking notes, six 2015 guidance lines trimmed of their "not a printed choice" asides, and
the 2019 ABQ (C) opinion allocation restricted to 0 or 3. Each value below is the committed one.
"""
import json
from pathlib import Path

EDITS = [
    ('bus-2013-hl-s1-q4', ['rubric', 'markingGuideNote'], "Use the published answer key and the cumulative mark sequence above. Each correct statement or match counts once."),
    ('bus-2013-hl-s1-q8', ['rubric', 'markingGuideNote'], "Use the published answer key and the cumulative mark sequence above. Each correct statement or match counts once."),
    ('bus-2013-hl-s3-q5a', ['rubric', 'markingGuideNote'], "Follow the official worked table and its marked own-figure allowances. The unpriced subtotals do not earn additional marks."),
    ('bus-2015-hl-s3-q1a', ['rubric', 'guidance'], []),
    ('bus-2015-hl-s3-q1c-ii', ['rubric', 'guidance'], ["Gender and disability are expressly excluded. Use the historical Act specified in the examination."]),
    ('bus-2015-hl-s3-q2c', ['rubric', 'guidance'], ["The support notes accept measures taken by a business or qualities of an environmentally conscious business."]),
    ('bus-2015-hl-s3-q3a', ['rubric', 'guidance'], ["Use the 2015 examination context."]),
    ('bus-2015-hl-s3-q3b', ['rubric', 'guidance'], ["For the adapted marketing mix, the example may apply to any one element."]),
    ('bus-2015-hl-s3-q7c-ii', ['rubric', 'guidance'], []),
    ('bus-2019-hl-s2-abq-c', ['rubric', 'responses', 0, 'allocations', 0, 'permittedMarks'], [0, 3]),
]

path = Path('components/MarkBank/cards/business/rubric-authored.json')
d = json.loads(path.read_text())
cards = {c['id']: c for c in d['cards']}
for cid, keys, value in EDITS:
    node = cards[cid]
    for k in keys[:-1]:
        node = node[k]
    node[keys[-1]] = value
path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print(f'Re-applied {len(EDITS)} post-generation edits.')
