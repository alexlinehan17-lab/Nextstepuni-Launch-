#!/usr/bin/env python3
"""Construction Studies 2020 Ordinary Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2020, 'ol')

PLAN = [
    (1, 'a', 'cons-2-4', 'vertical-section-through-strip-foundation-external'),
    (2, 'a', 'cons-1-1', 'method-insulating-proposed-cavity-type-thickness'),
    (2, 'b', 'cons-1-1', 'list-advantages-installing-insulation-cavity'),
    (2, 'c', 'cons-1-1', 'separate-method-providing-additional-insulation-this'),
    (3, 'a', 'cons-5-2', 'wood-burning-stove-can-used-heat'),
    (3, 'b', 'cons-5-3', 'installation-underfloor-heating-system-now-alternative'),
    (4, 'a', 'cons-1-1', 'reasons-why-construction-company-should-have'),
    (4, 'c', 'cons-1-1', 'other-method-sorting-storing-waste-materials'),
    (5, 'a', 'cons-3-8', 'vertical-section-through-roof-ridge-typical'),
    (5, 'b', 'cons-1-1', 'method-ventilating-roof'),
    (6, 'a', 'cons-1-8', 'large-safety-signs-highlighting-use-personal'),
    (6, 'b', 'cons-1-8', 'safety-precautions-workers-must-follow-when'),
    (6, 'c', 'cons-1-8', 'reasons-why-all-workers-must-undertake'),
    (7, 'a', 'cons-5-6', 'given-design-preferred-location-bathroom-toilet'),
    (7, 'b', 'cons-5-6', 'homeowner-has-decided-install-grab-rails'),
    (7, 'c', 'cons-5-6', 'advantage-designing-bathroom-person-reduced-mobility'),
    (8, None, 'cons-2-4', 'explain-five-stud-partition-domino-joint'),
    (9, 'a', 'cons-1-1', 'reasons-why-homeowner-would-build-extension'),
    (9, 'b', 'cons-7-4', 'modifications-extension-would-allow-more-natural'),
    (9, 'c', 'cons-7-4', 'advantages-occupants-increasing-amount-natural-light'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2020-ol-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
