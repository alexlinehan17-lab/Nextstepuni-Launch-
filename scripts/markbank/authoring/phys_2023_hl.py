#!/usr/bin/env python3
"""Physics 2023 Higher Level — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'. The scheme reprints the question above its own answer, which is
why index 0 is often the cue rather than a marking point.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2023, 'hl')

A.card(1, None, 'v', topic='phys-u2', concept='g-from-the-slope-of-a-graph',
       source='pdf',
       from_runs=[((1, None, 'v'), 0, slice(0, None)),
                  ((1, None, 'v'), 1, slice(0, 6)),
                  ((1, None, 'v'), 1, slice(7, 14))],
       marks=[3, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(9, None, 'ii', topic='phys-4-4', concept='energy-released-in-a-decay',
       source='pdf',
       from_runs=[((9, None, 'ii'), 0, slice(0, 3)),
                  ((9, None, 'ii'), 1, slice(0, 6)),
                  ((9, None, 'ii'), 2, slice(0, 4))],
       marks=[3, 3, 3], first_sentence=True)

A.card(14, 'c', 'iii', topic='phys-3-3', concept='total-resistance-of-a-mixed-circuit',
       source='pdf',
       from_runs=[((14, 'c', 'iii'), 0, slice(0, 5)),
                  ((14, 'c', 'iii'), 0, slice(6, 10)),
                  ((14, 'c', 'iii'), 0, slice(11, 15))],
       marks=[3, 3, 3])

A.card(14, 'c', 'iv', topic='phys-3-3', concept='how-to-lower-total-resistance',
       source='pdf', from_run=((14, 'c', 'iv'), 0, slice(0, 2)), marks=[3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(1, None, 'iv', topic='phys-u2', concept='graph-of-distance-against-time-squared',
       source='pdf',
       from_runs=[((1, None, 'iv'), 0, slice(0, 2)),
                  ((1, None, 'iv'), 3, slice(0, 2)),
                  ((1, None, 'iv'), 3, slice(3, 6)),
                  ((1, None, 'iv'), 3, slice(7, 12))],
       marks=[3, 3, 3, 3],
       notes='The relationship is linear against the SQUARE of the time, so the first '
             'mark is for working those values out before plotting anything.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-grating-experiment',
       source='pdf',
       from_runs=[((3, None, 'i'), 0, slice(0, 3)),
                  ((3, None, 'i'), 0, slice(4, 5)),
                  ((3, None, 'i'), 0, slice(6, 8)),
                  ((3, None, 'i'), 0, slice(9, 10))],
       marks=[3, 3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-for-the-latent-heat-experiment',
       source='pdf',
       from_runs=[((4, None, 'i'), 0, slice(0, 5)),
                  ((4, None, 'i'), 0, slice(6, 9)),
                  ((4, None, 'i'), 0, slice(10, 11)),
                  ((4, None, 'i'), 0, slice(12, 13))],
       marks=[3, 3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(8, 'a', 'vi', topic='phys-2-4', concept='drawing-the-third-harmonic',
       source='pdf',
       from_runs=[((8, 'a', 'vi'), 0, slice(0, 4)),
                  ((8, 'a', 'vi'), 0, slice(5, 11))],
       marks=[3, 3])

A.card(10, None, 'vii', topic='phys-4-2', concept='parts-of-an-x-ray-tube',
       source='pdf',
       from_runs=[((10, None, 'vii'), 2, slice(0, 2)),
                  ((10, None, 'vii'), 2, slice(3, 6)),
                  ((10, None, 'vii'), 2, slice(7, 13))],
       marks=[2, 2, 2], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme also credits cooling, shielding, a window and a partial vacuum.')

A.card(12, 'b', 'iv', topic='phys-3-3', concept='circuit-to-convert-ac-to-dc',
       source='pdf',
       from_runs=[((11, 'b', 'iv'), 0, slice(2, 7)),
                  ((11, 'b', 'iv'), 0, slice(8, 10)),
                  ((11, 'b', 'iv'), 0, slice(11, 17))],
       marks=[3, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme numbers this answer under its own Question 11 while the paper '
             'prints Question 12.')

A.card(12, 'b', 'v', topic='phys-3-3', concept='circuit-of-a-voltage-inverter',
       source='pdf',
       from_runs=[((11, 'b', 'v'), 0, slice(0, 5)),
                  ((11, 'b', 'v'), 0, slice(6, 9)),
                  ((11, 'b', 'v'), 0, slice(10, 13))],
       marks=[3, 3, 3])

A.card(12, 'b', 'vi', topic='phys-3-3', concept='truth-table-of-a-not-gate',
       source='pdf',
       from_runs=[((11, 'b', 'vi'), 0, slice(4, 8)),
                  ((11, 'b', 'vi'), 0, slice(9, 13))],
       marks=[3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(14, 'a', 'iv', topic='phys-2-1', concept='graph-that-explains-boyles-law',
       source='pdf',
       from_runs=[((14, 'a', 'iv'), 0, slice(6, 12)),
                  ((14, 'a', 'iv'), 0, slice(15, 20))],
       marks=[5, 2], notation='3 + 2 for the axes, 2 for the line', checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(2, None, 'iii', topic='phys-u2', concept='apparatus-with-u-and-v-marked',
       source='pdf',
       from_runs=[((2, None, 'iii'), 0, slice(7, 10)),
                  ((2, None, 'iii'), 0, slice(11, 13)),
                  ((2, None, 'iii'), 0, slice(14, 16))],
       marks=[3, 3, 3], first_sentence=True)

A.card(5, None, 'i', topic='phys-u2', concept='circuit-for-a-diode-in-forward-bias',
       source='pdf',
       from_runs=[((5, None, 'i'), 0, slice(0, 3)),
                  ((5, None, 'i'), 0, slice(4, 8)),
                  ((5, None, 'i'), 0, slice(9, 13)),
                  ((5, None, 'i'), 0, slice(14, 17))],
       marks=[3, 3, 3, 3])

A.card(5, None, 'iv', topic='phys-u2', concept='circuit-for-a-diode-in-reverse-bias',
       source='pdf',
       from_runs=[((5, None, 'iv'), 0, slice(0, 4)),
                  ((5, None, 'iv'), 0, slice(5, 11))],
       marks=[3, 3],
       notes='The ammeter changes with the bias: a milliammeter in forward bias, a '
             'microammeter in reverse, because the reverse current is tiny.')

A.emit()
