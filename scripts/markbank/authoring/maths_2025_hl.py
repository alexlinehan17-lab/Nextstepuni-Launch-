#!/usr/bin/env python3
"""Mathematics 2025 Higher Level, both papers.

Filed by maths_topics.py. See maths_lib.py for the card shape and mathtext.py
for why the notation survives at all.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maths_lib import Author, Refused  # noqa: E402
from maths_topics import topic_for, concept_for  # noqa: E402

A = Author(2025, 'hl')

for key in A.S.parts():
    paper, q, letter = key
    qtext = A.question(key)
    topic, _ = topic_for(qtext)
    if not topic:
        print(f'UNFILED {A.ref(key)}: {qtext[:60]}', file=sys.stderr)
        continue
    cid = f'maths-2025-hl-p{paper}-q{q}' + (f'-{letter}' if letter else '')
    try:
        A.card(key, cid=cid, topic=topic, concept=concept_for(qtext))
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
