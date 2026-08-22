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

A.emit()
