#!/usr/bin/env python3
"""Physics 2022 Higher Level — the net force part of the equilibrium experiment.

The two nuclear-equation parts of Question 10 are not here: the scheme sets
them in a bold font the text layer reads as doubled letters, so the equation
comes out as a run of repeated characters rather than nuclide symbols. They are
in the same class as the Chemistry formulae already recorded as font-mangled.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2022, 'hl')

A.card(1, None, 'vii', topic='phys-u2', concept='net-vertical-force-on-a-metre-stick',
       source='pdf', use=[0], marks=[3],
       notes='The scheme keeps "[upwards]" on the answer — the direction is part of it.')

A.card(11, None, 'i', topic='phys-2-1', concept='heat-capacity-and-specific-heat-capacity',
       source='pdf',
       from_runs=[((11, None, 'i'), 0, slice(12, 25)),
                  ((11, None, 'i'), 0, slice(27, 41))],
       marks=[3, 3],
       notes='Each definition may be given in words or as the formula beside it, which is '
             'what the scheme\'s solidus separates.')

A.card(14, 'd', 'i', topic='phys-3-6', concept='laws-of-electromagnetic-induction',
       source='pdf', first_sentence=True,
       from_runs=[((14, 'd', 'i'), 0, slice(0, 6)),
                  ((14, 'd', 'i'), 0, slice(7, 16)),
                  ((14, 'd', 'i'), 0, slice(17, 21)),
                  ((14, 'd', 'i'), 0, slice(22, 32))],
       marks=[3, 3, 3, 3])

A.card(1, None, 'vi', topic='phys-u2', concept='net-moment-about-a-point',
       source='pdf',
       from_runs=[((1, None, 'vi'), 0, slice(0, 15)),
                  ((1, None, 'vi'), 0, slice(16, 27)),
                  ((1, None, 'vi'), 0, slice(28, 35))],
       marks=[3, 3, 3])

A.card(3, None, 'iv', topic='phys-u2', concept='refractive-index-from-a-slope',
       source='pdf',
       from_runs=[((3, None, 'iv'), 0, slice(0, 2)),
                  ((3, None, 'iv'), 0, slice(3, 6))],
       marks=[3, 3])

A.emit()
