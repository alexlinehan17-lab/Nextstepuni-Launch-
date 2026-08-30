#!/usr/bin/env python3
"""Mathematics 2023 Higher Level, both papers.

Filed by maths_topics.py. See maths_lib.py for the card shape and mathtext.py
for why the notation survives at all.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maths_lib import Author, Refused  # noqa: E402
from maths_topics import topic_for, concept_for  # noqa: E402
import maths_figures  # noqa: E402

A = Author(2023, 'hl')
# The model solution rides on the card as an image: its notation extracts but
# its structure does not, so the SEC's own typesetting is the only honest way to
# show it. See mathtext.py.
FIGURES = maths_figures.names(2023, 'hl')

# Two passes. A continuation part -- "Hence, or otherwise, find the value of
# A(100)" -- names nothing a keyword can file, but it is unambiguously the same
# topic as the rest of its question, so the parts that DO file decide for the
# ones that do not. Only within a question, and only where that question filed
# somewhere.
filed, votes = {}, {}
for key in A.S.parts():
    t, _ = topic_for(A.question(key))
    filed[key] = t
    if not t:
        # The paper's wording files nothing; let the scheme's own method vote.
        t2, _ = topic_for(A.topic_evidence(key))
        if t2:
            votes.setdefault((key[0], key[1]), []).append(t2)
    if t:
        votes.setdefault((key[0], key[1]), []).append(t)

for key in A.S.parts():
    paper, q, letter, roman = key[0], key[1], key[2], key[3]
    qtext = A.question(key)
    topic = filed[key]
    if not topic:
        near = votes.get((paper, q))
        topic = max(set(near), key=near.count) if near else None
    if not topic:
        print(f'UNFILED {A.ref(key)}: {qtext[:60]}', file=sys.stderr)
        continue
    cid = (f'maths-2023-hl-p{paper}-q{q}'
           + (f'-{letter}' if letter else '') + (f'-{roman}' if roman else ''))
    try:
        A.card(key, cid=cid, topic=topic, concept=concept_for(qtext),
               figure_key=FIGURES.get(key, ''))
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
