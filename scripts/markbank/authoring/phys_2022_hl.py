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


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(3, None, 'iii', topic='phys-u2', concept='graph-to-verify-snells-law',
       source='pdf',
       from_runs=[((3, None, 'iii'), 0, slice(0, 7)),
                  ((3, None, 'iii'), 2, slice(0, 2)),
                  ((3, None, 'iii'), 2, slice(3, 6)),
                  ((3, None, 'iii'), 2, slice(7, 11))],
       marks=[3, 3, 3, 3],
       notes='Snell\'s law is verified against the sines, not the angles, so the first '
             'mark is for working those out before plotting anything.')

A.card(5, None, 'iii', topic='phys-u2', concept='graph-to-verify-joules-law',
       source='pdf',
       from_runs=[((5, None, 'iii'), 0, slice(0, 3)),
                  ((5, None, 'iii'), 3, slice(0, 2)),
                  ((5, None, 'iii'), 3, slice(3, 6)),
                  ((5, None, 'iii'), 3, slice(7, 11))],
       marks=[3, 3, 3, 3])

A.card(9, 'a', 'i', topic='phys-3-1', concept='electric-field-around-a-charged-sphere',
       source='pdf',
       from_runs=[((8, 'a', 'i'), 0, slice(0, 4)),
                  ((8, 'a', 'i'), 0, slice(5, 10))],
       marks=[3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme numbers this answer under its own Question 8 while the paper '
             'prints Question 9.')

A.card(12, 'b', 'ii', topic='phys-3-5', concept='parts-of-a-moving-coil-galvanometer',
       source='pdf',
       from_runs=[((12, 'b', 'ii'), 0, slice(0, 1)),
                  ((12, 'b', 'ii'), 0, slice(2, 3)),
                  ((12, 'b', 'ii'), 0, slice(4, 7)),
                  ((12, 'b', 'ii'), 0, slice(8, 11))],
       marks=[3, 3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(12, 'b', 'iv', topic='phys-3-3', concept='converting-a-galvanometer-to-an-ammeter',
       source='pdf',
       from_runs=[((12, 'b', 'iv'), 0, slice(0, 3)),
                  ((12, 'b', 'iv'), 0, slice(4, 8))],
       marks=[3, 3])

A.card(12, 'b', 'v', topic='phys-3-3', concept='converting-a-galvanometer-to-an-ohmmeter',
       source='pdf',
       from_runs=[((12, 'b', 'v'), 0, slice(0, 6)),
                  ((12, 'b', 'v'), 0, slice(7, 9))],
       marks=[3, 3])

A.emit()
