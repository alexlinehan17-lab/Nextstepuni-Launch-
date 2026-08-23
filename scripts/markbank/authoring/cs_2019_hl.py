#!/usr/bin/env python3
"""Construction Studies 2019 Higher Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2019, 'hl')

PLAN = [
    (1, 'b', 'cons-3-6', 'typical-design-detailing-prevent-ingress-rainwater'),
    (3, 'a', 'cons-5-6', 'design-considerations-proposed-bedroom-suite-bathroom'),
    (3, 'b', 'cons-5-6', 'proposed-internal-layout-bedroom-suite-bathroom'),
    (4, 'a', 'cons-1-1', 'benefits-local-community-refurbishing-townhouses-family'),
    (5, 'a', 'cons-6-1', 'calculate-value-wall-given-construction-has'),
    (5, 'b', 'cons-6-1', 'value-wall-obtained-above-data-calculate'),
    (5, 'c', 'cons-6-3', 'proposed-upgrade-thermal-properties-above-wall'),
    (6, 'a', 'cons-6-3', 'reference-design-shown-features-design-contribute'),
    (6, 'b', 'cons-1-1', 'renewable-energy-technologies-identify-how-contributes'),
    (6, 'c', 'cons-1-1', 'advantages-local-craft-skills-when-building'),
    (7, 'a', 'cons-4-4', 'vertical-section-through-centre-stairs-section'),
    (7, 'b', 'cons-1-1', 'indicate-design-features-ensure-stairs-safe'),
    (8, 'a', 'cons-1-3', 'considerations-ensure-proper-treatment-disposal-sewage'),
    (8, 'c', 'cons-5-5', 'alternative-method-other-than-typical-percolation'),
    (9, 'b', 'cons-1-1', 'negative-impacts-thermal-bridging-result-poor'),
    (10, 'a', 'cons-6-3', 'design-considerations-necessary-achieve-enerphit-passive'),
    (10, 'b', 'cons-6-3', 'how-you-would-retrofit-given-house'),
    (10, 'c', 'cons-6-3', 'advantages-retrofitting-existing-house-meet-enerphit'),
    (2, 'a', 'cons-1-1', 'functional-requirements-roof-domestic-dwelling-house'),
    (2, 'c', 'cons-1-1', 'select-different-roofing-material-roof-types'),
    (8, 'b', 'cons-5-5', 'shows-site-layout-map-new-house'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2019-hl-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
