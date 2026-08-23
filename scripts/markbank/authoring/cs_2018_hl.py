#!/usr/bin/env python3
"""Construction Studies 2018 Higher Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2018, 'hl')

PLAN = [
    (1, 'b', 'cons-1-1', 'typical-design-detailing-prevent-ingress-rainwater'),
    (2, 'c', 'cons-1-8', 'strategies-would-promote-positive-safety-culture'),
    (3, 'a', 'cons-6-5', 'considerations-should-taken-into-account-design'),
    (3, 'c', 'cons-1-1', 'how-proposed-design-meets-consideration-discussed'),
    (4, 'a', 'cons-1-1', 'importance-when-identifying-site-new-house'),
    (4, 'c', 'cons-6-4', 'well-proportioned-selected-site-immediate-boundaries'),
    (5, 'a', 'cons-6-1', 'calculate-value-uninsulated-concrete-ground-floor'),
    (5, 'b', 'cons-6-1', 'value-concrete-floor-obtained-above-data'),
    (5, 'c', 'cons-6-3', 'proposed-redesign-above-floor-upgrade-its'),
    (6, 'a', 'cons-1-1', 'advantages-disadvantages-self-build-method-building'),
    (6, 'b', 'cons-1-1', 'features-design-shown-make-house-self'),
    (7, 'b', 'cons-6-2', 'clearly-best-practice-design-detailing-ensure'),
    (8, 'c', 'cons-5-3', 'design-considerations-should-taken-into-account'),
    (9, 'c', 'cons-6-2', 'design-prevent-air-leakage-junction-stud'),
    (10, 'c', 'cons-6-4', 'preferred-orientation-upgraded-design-include-sun'),
    (4, 'b', 'cons-1-3', 'extract-from-site-location-map-shown'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2018-hl-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
