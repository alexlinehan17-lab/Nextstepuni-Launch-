#!/usr/bin/env python3
"""Construction Studies 2019 Ordinary Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2019, 'ol')

PLAN = [
    (1, 'a', 'cons-1-5', 'vertical-section-through-top-portion-window'),
    (2, 'b', 'cons-1-1', 'trapdoor-also-insulated-well-sealed-insulation'),
    (2, 'c', 'cons-3-9', 'reasons-why-couple-should-begin-insulating'),
    (3, 'a', 'cons-5-2', 'dwelling-should-have-clean-water-supply'),
    (3, 'b', 'cons-5-6', 'shows-valve-usually-used-turn-off'),
    (3, 'c', 'cons-5-6', 'advantage-installing-dual-flush-toilet'),
    (4, 'b', 'cons-1-1', 'method-connecting-inner-outer-leaves-wall'),
    (4, 'c', 'cons-1-1', 'advantages-ready-mixed-concrete-foundations-dwelling'),
    (5, 'a', 'cons-4-3', 'vertical-section-parallel-joists-through-floor'),
    (5, 'b', 'cons-4-5', 'position-insulation-partition'),
    (6, 'a', 'cons-1-8', 'specific-safety-precautions-observed-construction-studies'),
    (6, 'b', 'cons-1-8', 'specific-safety-precautions-observed-when-operating'),
    (6, 'c', 'cons-1-8', 'reasons-why-safety-instruction-necessary-all'),
    (7, 'b', 'cons-1-1', 'select-floor-type-kitchen-area-another'),
    (7, 'c', 'cons-1-1', 'design-showing-position-island-unit-kitchen'),
    (9, 'a', 'cons-3-3', 'wood-external-cladding-reasons-choice'),
    (9, 'b', 'cons-1-1', 'home-office-modified-provide-greater-views'),
    (9, 'c', 'cons-1-1', 'advantages-home-office-user-increasing-visual'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2019-ol-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
