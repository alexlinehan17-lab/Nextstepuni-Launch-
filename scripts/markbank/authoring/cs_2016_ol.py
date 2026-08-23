#!/usr/bin/env python3
"""Construction Studies 2016 Ordinary Level.

Filed by cs_topics.py rather than by hand. Filing is a librarian's decision --
the question and the answer are lifted either way -- and one rule applied to
twenty papers is more consistent than a judgement made part by part across ten.
See cs_2021_hl.py for the card shape.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_lib import Author, Refused  # noqa: E402

A = Author(2016, 'ol')

PLAN = [
    (2, 'b', 'cons-3-9', 'reasons-why-attic-space-chosen-first'),
    (3, 'a', 'cons-5-2', 'large-given-diagram-also-include-main'),
    (3, 'b', 'cons-5-2', 'same-also-pipework-necessary-connect-solar'),
    (3, 'c', 'cons-5-2', 'advantages-including-solar-collector-provide-domestic'),
    (4, 'a', 'cons-1-3', 'reasons-why-necessary-apply-planning-permission'),
    (4, 'b', 'cons-1-1', 'information-must-contained-planning-documents-site'),
    (4, 'c', 'cons-1-1', 'reason-why-planning-authority-allows-public'),
    (5, 'a', 'cons-4-4', 'vertical-section-through-bottom-steps-stairs'),
    (6, 'a', 'cons-1-8', 'specific-safety-precautions-observed-construction-studies'),
    (7, 'a', 'cons-4-5', 'typical-construction-details-stud-partition-clearly'),
    (7, 'c', 'cons-4-6', 'briefly-method-providing-surface-finish-plasterboard'),
    (9, 'c', 'cons-1-1', 'features-design-ensure-garden-room-eco'),]

for q, letter, topic, concept in PLAN:
    try:
        A.card(q, letter, cid=f'cons-2016-ol-q{q}-{letter}', topic=topic,
               concept=concept)
    except Refused as e:
        print(f'REFUSED {e}', file=sys.stderr)

A.emit()
