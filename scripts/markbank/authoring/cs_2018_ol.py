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
    (7, 'c', 'cons-1-1', 'advantage-storing-rainwater-underground-tank'),
    (3, 'a', 'cons-5-2', 'wood-burning-stove-back-boiler-shown'),
    (1, 'b', 'cons-1-1', 'typical-design-detailing-prevent-radon-gas'),
    (2, 'b', 'cons-4-6', 'clearly-steps-followed-applying-surface-finish'),
    (5, 'b', 'cons-3-10', 'how-roof-ventilated-eaves'),
    (6, 'b', 'cons-1-8', 'design-feature-above-safety-items-helps'),
    (7, 'a', 'cons-5-2', 'given-pipework-necessary-collect-rainwater-from'),
    (7, 'b', 'cons-5-2', 'stored-rainwater-used-flushing-toilet-pipework'),
    (9, 'a', 'cons-3-3', 'how-blockwork-over-opening-typically-supported'),
    (2, 'c', 'cons-1-1', 'advantage-disadvantage-applying-external-system-insulation'),
    (5, 'a', 'cons-3-8', 'vertical-section-through-eaves-flat-roof'),
    (9, 'b', 'cons-1-1', 'how-doorframe-held-square-while-being'),
    (2, 'a', 'cons-1-1', 'method-applying-external-insulation-system-wall'),
    (9, 'c', 'cons-1-1', 'advantage-disadvantage-fitting-glazed-double-doors'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2018-ol-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
