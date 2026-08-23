#!/usr/bin/env python3
"""Construction Studies 2017 Higher Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2017, 'hl')

PLAN = [
    (1, 'b', 'cons-4-3', 'typical-design-detailing-cross-ventilation-suspended'),
    (2, 'a', 'cons-5-6', 'functional-requirements-bathroom-designed-lifetime-use'),
    (2, 'b', 'cons-4-2', 'shows-ground-floor-plan-semi-detached'),
    (2, 'c', 'cons-5-6', 'proposed-design-layout-bathroom-design-location'),
    (3, 'a', 'cons-1-1', 'proposed-design-layout-incorporates-above-requirements'),
    (3, 'b', 'cons-1-1', 'reasons-proposed-design-layout'),
    (4, 'c', 'cons-1-1', 'construction-wall-type-selected-under-headings'),
    (5, 'b', 'cons-6-1', 'proposed-upgrade-thermal-properties-above-wall'),
    (5, 'c', 'cons-6-1', 'calculate-cost-heat-lost-annually-through'),
    (6, 'a', 'cons-1-1', 'advantages-eco-friendly-house-design-21st'),
    (6, 'b', 'cons-1-1', 'features-given-design-contribute-making-house'),
    (6, 'c', 'cons-1-1', 'low-operating-costs-are-important-consideration'),
    (7, 'b', 'cons-1-1', 'typical-dimensions-roof-members'),
    (8, 'a', 'cons-7-4', 'importance-providing-adequate-light-work-surface'),
    (8, 'b', 'cons-3-6', 'home-office-shown-measures-metres-long'),
    (9, 'a', 'cons-2-4', 'reinforced-concrete-strip-foundation-supports-400'),
    (9, 'c', 'cons-1-1', 'test-may-carried-out-measure-consistency'),
    (10, 'a', 'cons-6-2', 'importance-passive-house-design-airtightness-indoor'),
    (10, 'b', 'cons-4-2', 'diagram-shows-ground-floor-plan-semi'),
    (10, 'c', 'cons-1-2', 'advantages-siting-mhrv-unit-hallway-shown'),
    (7, 'a', 'cons-3-8', 'vertical-section-through-roof-structure-typical'),
    (3, 'c', 'cons-1-1', 'advantages-building-extension-farmhouse-shown'),
    (4, 'a', 'cons-3-3', 'functional-requirements-external-wall-new-dwelling'),
    (8, 'c', 'cons-3-6', 'advances-glazing-technology-make-modern-glazing'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2017-hl-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
