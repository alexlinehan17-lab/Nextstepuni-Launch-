#!/usr/bin/env python3
"""Physics 2022 OL — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2022, 'ol')

A.card(2, None, 'v', topic='phys-u2', concept='average-refractive-index-from-results',
       source='pdf',
       from_runs=[((2, None, 'v'), 0, slice(0, 12)),
                  ((2, None, 'v'), 0, slice(13, 18))],
       marks=[3, 3],
       notes='Either route scores: an average of the calculated values, or the slope of '
             'a graph of sin i against sin r.')

A.card(5, None, 'v', topic='phys-u2', concept='reading-a-current-off-a-graph',
       source='pdf',
       from_runs=[((5, None, 'v'), 0, slice(0, 5)),
                  ((5, None, 'v'), 0, slice(6, 10))],
       marks=[3, 3])

A.card(7, None, 'ii', topic='phys-u5', concept='converting-minutes-to-seconds',
       source='pdf', from_run=((7, None, 'ii'), 0, slice(0, 6)), marks=[6])

A.card(9, None, 'iv', topic='phys-2-3', concept='image-position-from-the-lens-formula',
       source='pdf',
       from_runs=[((9, None, 'iv'), 0, slice(0, 5)),
                  ((9, None, 'iv'), 0, slice(6, 7)),
                  ((9, None, 'iv'), 0, slice(8, 12))],
       marks=[6, 3, 3])

A.card(14, 'a', 'iv', topic='phys-1-4', concept='kinetic-energy-of-a-thrown-stone',
       source='pdf', from_run=((14, 'a', 'iv'), 0, slice(0, 8)), marks=[5])

A.card(14, 'a', 'v', topic='phys-1-4', concept='maximum-height-from-kinetic-energy',
       source='pdf', from_run=((14, 'a', 'v'), 0, slice(0, 8)), marks=[5],
       notes='The scheme accepts the suvat route as well.')

A.card(2, None, 'vi', topic='phys-u2', concept='whether-the-results-verify-snells-law',
       source='pdf',
       from_runs=[((2, None, 'vi'), 0, slice(0, 6)),
                  ((2, None, 'vi'), 0, slice(7, 18))],
       marks=[3, 3])


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(5, None, 'iv', topic='phys-u2', concept='plotting-current-squared-against-temperature-rise',
       source='pdf',
       from_runs=[((5, None, 'iv'), 0, slice(0, 2)),
                  ((5, None, 'iv'), 0, slice(3, 8)),
                  ((5, None, 'iv'), 0, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3')

A.card(7, None, 'vii', topic='phys-1-2', concept='forces-on-a-train-at-constant-speed',
       source='pdf', from_run=((7, None, 'vii'), 0, slice(0, 3)), marks=[9],
       notes='The scheme takes a mark off for each of the four forces left out.')

A.card(1, None, 'ii', topic='phys-u2', concept='what-distance-was-measured-on-the-tape',
       source='pdf', use=[[0, 1, 2]], marks=[3])

A.card(3, None, 'ii', topic='phys-u2', concept='what-length-of-string-was-measured',
       source='pdf', use=[[0, 1]], marks=[3])

A.card(3, None, 'viii', topic='phys-u2', concept='graph-of-frequency-against-one-over-length',
       source='pdf',
       from_runs=[((3, None, 'viii'), 1, slice(0, 2)),
                  ((3, None, 'viii'), 1, slice(3, 5)),
                  ((3, None, 'viii'), 1, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3', checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(9, None, 'ii', topic='phys-2-3', concept='ray-diagram-for-a-magnified-image-ol',
       source='pdf',
       from_runs=[((9, None, 'ii'), 1, slice(0, 3)),
                  ((9, None, 'ii'), 1, slice(4, 7)),
                  ((9, None, 'ii'), 1, slice(8, 11))],
       marks=[5, 2, 2])

A.card(9, None, 'vii', topic='phys-2-3', concept='which-side-of-a-convex-mirror-reflects',
       source='pdf',
       from_runs=[((9, None, 'vii'), 2, slice(0, 1)),
                  ((9, None, 'vii'), 2, slice(2, 3))],
       marks=[3, 3], first_sentence=True)

A.emit()
