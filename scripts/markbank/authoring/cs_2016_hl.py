#!/usr/bin/env python3
"""Construction Studies 2016 Higher Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2016, 'hl')

PLAN = [
    (2, 'a', 'cons-1-8', 'importance-developing-positive-safety-culture-among'),
    (2, 'b', 'cons-1-8', 'importance-when-deciding-use-ladder-appropriate'),
    (2, 'c', 'cons-1-8', 'specific-best-practice-guidelines-should-observed'),
    (3, 'a', 'cons-7-4', 'revised-design-bungalow-which-will-ensure'),
    (3, 'b', 'cons-1-1', 'reasons-proposed-design-choices-redesign-bungalow'),
    (4, 'a', 'cons-1-1', 'reasons-why-site-may-considered-new'),
    (4, 'b', 'cons-6-4', 'well-proportioned-redraw-given-site-immediate'),
    (5, 'b', 'cons-6-1', 'calculate-cost-heat-lost-annually-through'),
    (5, 'c', 'cons-6-1', 'proposed-upgrade-thermal-properties-above-wall'),
    (9, 'a', 'cons-5-8', 'where-electrical-circuits-are-typically-used'),
    (10, 'a', 'cons-4-2', 'minimising-heat-loss-storing-heat-gain'),
    (10, 'c', 'cons-1-2', 'advantages-disadvantages-making-passive-house-standard'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2016-hl-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
