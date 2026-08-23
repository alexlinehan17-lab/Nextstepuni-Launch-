#!/usr/bin/env python3
"""Construction Studies 2020 Higher Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2020, 'hl')

PLAN = [
    (1, 'b', 'cons-3-8', 'typical-design-detailing-ensure-ventilation-roof'),
    (2, 'a', 'cons-1-1', 'specific-best-practice-guidelines-observed-when'),
    (2, 'b', 'cons-1-8', 'site-health-safety-officer-performs-key'),
    (3, 'a', 'cons-1-1', 'design-considerations-necessary-when-modifying-internal'),
    (3, 'c', 'cons-1-1', 'advantages-disadvantages-open-plan-living-domestic'),
    (4, 'a', 'cons-1-1', 'importance-considering-characteristics-when-designing-house'),
    (4, 'c', 'cons-1-1', 'advantages-developing-vacant-sites-urban-areas'),
    (5, 'a', 'cons-6-1', 'calculate-value-floor-given-construction-has'),
    (5, 'b', 'cons-6-1', 'value-floor-obtained-above-data-calculate'),
    (6, 'a', 'cons-1-1', 'advantages-disadvantages-retrofitting-vernacular-cottage-shown'),
    (6, 'b', 'cons-6-3', 'reference-design-shown-features-design-contribute'),
    (6, 'c', 'cons-6-3', 'modifications-house-shown-would-further-reduce'),
    (7, 'b', 'cons-5-3', 'typical-detailing-provide-independent-air-supply'),
    (8, 'a', 'cons-4-3', 'considerations-should-taken-into-account-when'),
    (8, 'c', 'cons-5-5', 'considerations-minimise-blockages-occurring-drainage-system'),
    (9, 'a', 'cons-8-3', 'how-contribute-reducing-transmission-sound-dwelling'),
    (9, 'c', 'cons-6-5', 'benefits-sound-insulation-upgrades-will-have'),
    (10, 'a', 'cons-1-1', 'considerations-should-taken-into-account-when'),
    (10, 'c', 'cons-1-2', 'advantages-installing-mvhr-system-into-domestic'),
    (7, 'a', 'cons-5-3', 'vertical-section-through-ground-floor-hearth'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2020-hl-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
