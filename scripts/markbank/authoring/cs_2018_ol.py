#!/usr/bin/env python3
"""Construction Studies 2018 Ordinary Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2018, 'ol')

PLAN = [
    (1, 'a', 'cons-2-4', 'vertical-section-through-strip-foundation-215'),
    (3, 'b', 'cons-5-3', 'advantage-wood-burning-stove-heat-water'),
    (4, 'a', 'cons-2-4', 'environmental-reason-why-strip-foundation-considered'),
    (6, 'c', 'cons-1-8', 'recommend-other-item-personal-protective-equipment'),
    (7, 'c', 'cons-1-1', 'advantage-storing-rainwater-underground-tank'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2018-ol-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
