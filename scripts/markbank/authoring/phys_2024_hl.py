#!/usr/bin/env python3
"""Physics 2024 Higher Level — the charge held by the capacitor."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2024, 'hl')

A.card(11, None, 'vii', topic='phys-3-2', concept='charge-on-a-capacitor-mid-discharge',
       source='pdf', use=[0, 1, 2], marks=[2, 3, 3])

A.card(5, None, 'iii', topic='phys-u2', concept='resistance-from-the-slope-of-a-graph',
       source='pdf', first_sentence=True,
       from_runs=[((5, None, 'iii'), 0, slice(0, 2)),
                  ((5, None, 'iii'), 0, slice(3, 7))],
       marks=[3, 2])

A.card(9, 'a', 'iv', topic='phys-3-3', concept='intrinsic-and-extrinsic-conduction',
       source='pdf',
       from_runs=[((8, 'a', 'iv'), 1, slice(0, 12)),
                  ((8, 'a', 'iv'), 1, slice(13, 25))],
       marks=[2, 2],
       checked='The paper sets this part in a block with no text of its own, so the '
               'question is the one the scheme reprints above its answer.',
       notes='The scheme numbers this answer under its own Question 8 while the paper '
             'prints Question 9.')

A.card(11, None, 'vi', topic='phys-3-3', concept='potential-difference-across-a-resistor',
       source='pdf',
       from_runs=[((11, None, 'vi'), 0, slice(0, 3)),
                  ((11, None, 'vi'), 0, slice(4, 8))],
       marks=[3, 3])

A.card(1, None, 'ii', topic='phys-u2', concept='how-acceleration-was-determined',
       source='pdf',
       from_runs=[((1, None, 'ii'), 0, slice(0, 6)),
                  ((1, None, 'ii'), 0, slice(7, 12)),
                  ((1, None, 'ii'), 0, slice(13, 16))],
       marks=[3, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(7, None, 'i', topic='phys-1-6', concept='deriving-v-equals-r-omega',
       source='pdf', use=[0, 1, 2], marks=[3, 3, 3])


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(1, None, 'iii', topic='phys-u2', concept='graph-of-force-against-acceleration',
       source='pdf',
       from_runs=[((1, None, 'iii'), 0, slice(0, 2)),
                  ((1, None, 'iii'), 0, slice(3, 5)),
                  ((1, None, 'iii'), 0, slice(6, 10))],
       marks=[3, 3, 3])

A.card(5, None, 'i', topic='phys-u2', concept='circuit-for-the-resistivity-experiment',
       source='pdf',
       from_runs=[((5, None, 'i'), 0, slice(0, 6)),
                  ((5, None, 'i'), 0, slice(10, 18)),
                  ((5, None, 'i'), 0, slice(19, 22))],
       marks=[3, 3, 3],
       notation='any three of the four components at 1 each, then 3 and 3')

A.card(5, None, 'ii', topic='phys-u2', concept='graph-of-current-against-voltage',
       source='pdf',
       from_runs=[((5, None, 'ii'), 0, slice(0, 2)),
                  ((5, None, 'ii'), 0, slice(3, 6)),
                  ((5, None, 'ii'), 0, slice(7, 11))],
       marks=[3, 3, 3])

A.card(8, None, 'iii', topic='phys-3-4', concept='field-around-a-straight-current-carrying-wire',
       source='pdf',
       from_runs=[((8, None, 'iii'), 0, slice(0, 1)),
                  ((8, None, 'iii'), 0, slice(2, 3))],
       marks=[3, 3])

A.card(12, 'b', 'iii', topic='phys-3-3', concept='circuit-of-a-half-wave-rectifier',
       source='pdf',
       from_runs=[((11, 'b', 'iii'), 1, slice(0, 1)),
                  ((11, 'b', 'iii'), 2, slice(0, 5)),
                  ((11, 'b', 'iii'), 3, slice(0, 1))],
       marks=[3, 3, 3],
       notes='The scheme numbers this answer under its own Question 11 while the paper '
             'prints Question 12.')

A.card(12, 'b', 'v', topic='phys-3-3', concept='structure-of-a-bipolar-transistor',
       source='pdf', from_run=((11, 'b', 'v'), 1, slice(0, 6)), marks=[7],
       notation='3 + 2 + 2 across the three layers', notes='The scheme numbers this answer under its own Question 11 while the paper prints Question 12.')

A.card(12, 'b', 'vi', topic='phys-3-3', concept='truth-table-of-a-not-gate',
       source='pdf',
       from_runs=[((11, 'b', 'vi'), 1, slice(0, 5)),
                  ((11, 'b', 'vi'), 2, slice(0, 5))],
       marks=[2, 2], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(12, 'b', 'vii', topic='phys-3-6', concept='parts-of-an-induction-coil',
       source='pdf',
       from_runs=[((11, 'b', 'vii'), 1, slice(0, 8)),
                  ((11, 'b', 'vii'), 2, slice(0, 7)),
                  ((11, 'b', 'vii'), 3, slice(0, 8))],
       marks=[3, 3, 3], notes='The scheme numbers this answer under its own Question 11 while the paper prints Question 12.')

A.card(14, 'c', 'ii', topic='phys-4-2', concept='parts-of-a-cathode-ray-tube',
       source='pdf',
       from_runs=[((13, 'c', 'ii'), 1, slice(0, 2)),
                  ((13, 'c', 'ii'), 2, slice(0, 5)),
                  ((13, 'c', 'ii'), 3, slice(0, 2)),
                  ((13, 'c', 'ii'), 4, slice(0, 3))],
       marks=[2, 2, 2, 2], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme numbers this answer under its own Question 13 while the paper '
             'prints Question 14.')

A.card(14, 'd', 'i', topic='phys-2-6', concept='parts-of-a-spectrometer',
       source='pdf', from_run=((13, 'd', 'i'), 1, slice(0, 6)), marks=[8],
       notation='2 + 2 + 2 + 2', checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme numbers this answer under its own Question 13 while the paper '
             'prints Question 14.')

A.emit()
