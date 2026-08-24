#!/usr/bin/env python3
"""Physics 2024 Higher Level — the charge held by the capacitor.

A part whose scheme prints only the marking convention — "apparatus [3]
method [3] observation [3]", "two items [4 + 3]", "any 4 named [4 × 1]" —
with no answer content is never carded; there is nothing to lift. The same
goes for a sketch whose only creditable content is the drawing itself.
"""
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

A.card(1, None, 'i', topic='phys-u2', concept='apparatus-for-the-newtons-second-law-experiment',
       source='pdf',
       from_runs=[((1, None, 'i'), 1, slice(0, 1)),
                  ((1, None, 'i'), 1, slice(2, 4)),
                  ((1, None, 'i'), 1, slice(5, 8))],
       marks=[4, 3, 3], notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-for-the-stretched-string-experiment',
       source='pdf',
       from_runs=[((4, None, 'i'), 1, slice(0, 2)),
                  ((4, None, 'i'), 2, slice(0, 1)),
                  ((4, None, 'i'), 3, slice(0, 2))],
       marks=[2, 2, 2],
       notes='The scheme also credits a newtonmeter, a tuning fork, a metre stick and '
             'the bridges.')

A.card(7, None, 'iii', topic='phys-1-6', concept='forces-on-a-ball-in-circular-motion',
       source='pdf', use=[1, 2], marks=[3, 3], first_sentence=True,
       notes='The scheme takes three marks off for any extra force drawn in — there is '
             'no outward force on the ball.')

A.card(9, 'a', 'ii', topic='phys-3-3', concept='temperature-resistance-graph-for-a-thermistor',
       source='pdf',
       from_runs=[((8, 'a', 'ii'), 1, slice(0, 2)),
                  ((8, 'a', 'ii'), 2, slice(0, 1))],
       marks=[3, 3],
       notes='The scheme numbers this answer under its own Question 8 while the paper '
             'prints Question 9.')

A.card(11, None, 'iii', topic='phys-3-2', concept='graph-of-capacitance-against-plate-area',
       source='pdf',
       from_runs=[((11, None, 'iii'), 1, slice(0, 2)),
                  ((11, None, 'iii'), 2, slice(0, 2))],
       marks=[3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(12, 'b', 'ii', topic='phys-3-6', concept='voltage-time-graphs-for-ac-and-dc',
       source='pdf',
       from_runs=[((11, 'b', 'ii'), 1, slice(0, 2)),
                  ((11, 'b', 'ii'), 2, slice(0, 2)),
                  ((11, 'b', 'ii'), 3, slice(0, 2))],
       marks=[3, 3, 3],
       notes='The scheme numbers this answer under its own Question 11 while the paper '
             'prints Question 12.')

# ── Closing the open coverage ──────────────────────────────────────────────
A.card(1, None, 'v', topic='phys-u2', concept='mass-from-the-slope-of-a-graph',
       source='pdf',
       from_runs=[((1, None, 'v'), 0, slice(0, 2)),
                  ((1, None, 'v'), 0, slice(3, 7))],
       marks=[3, 2])

A.card(2, None, 'ii', topic='phys-u2', concept='apparatus-for-the-focal-length-experiment',
       source='pdf',
       from_runs=[((2, None, 'ii'), 0, slice(0, 1)),
                  ((2, None, 'ii'), 0, slice(2, 3)),
                  ((2, None, 'ii'), 0, slice(4, 5)),
                  ((2, None, 'ii'), 0, slice(6, 10))],
       marks=[2, 2, 2, 3])

A.card(2, None, 'iv', topic='phys-u2', concept='focal-length-from-all-of-the-data',
       source='pdf',
       from_runs=[((2, None, 'iv'), 0, slice(0, 11)),
                  ((2, None, 'iv'), 0, slice(12, 19)),
                  ((2, None, 'iv'), 0, slice(20, 32)),
                  ((2, None, 'iv'), 0, slice(33, 40))],
       marks=[3, 3, 3, 3],
       notes='The // pairs the calculation route with the graph route — either '
             'side of each line earns its marks, but the two routes cannot be mixed.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-latent-heat-experiment',
       source='pdf',
       from_runs=[((3, None, 'i'), 0, slice(0, 1)),
                  ((3, None, 'i'), 0, slice(2, 5)),
                  ((3, None, 'i'), 0, slice(6, 7)),
                  ((3, None, 'i'), 0, slice(8, 9))],
       marks=[2, 2, 2, 2],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(4, None, 'iv', topic='phys-u2', concept='graph-of-frequency-against-tension',
       source='pdf',
       from_runs=[((4, 'a', 'iv'), 4, slice(0, 2)),
                  ((4, 'a', 'iv'), 4, slice(3, 6)),
                  ((4, 'a', 'iv'), 4, slice(7, 11))],
       marks=[3, 3, 3],
       notes='The scheme awards a further 3 marks, not shown here, for first '
             'working out the values to plot — the square of each frequency or '
             'the square root of each tension; that line is typeset with a '
             'radical sign the text layer cannot carry.')

# The first row's words are this part's own — the scheme prints "slope
# formula, f = …" — lifted from Q5(iii)'s identical line to leave the
# scheme's comma and unrenderable typeset maths behind.
A.card(4, None, 'vi', topic='phys-u2', concept='mass-per-unit-length-from-the-slope',
       source='pdf',
       from_runs=[((5, None, 'iii'), 0, slice(0, 2)),
                  ((4, 'a', 'vi'), 4, slice(0, 7))],
       marks=[5, 3], notation='3 + 2 for the slope formula, then 3',
       checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme writes the slope formula out in full as typeset maths '
             'that does not survive the text layer; the 3 + 2 covers stating '
             'and using it.')

A.card(7, None, 'vi', topic='phys-1-1', concept='resolving-velocity-into-components',
       source='pdf',
       from_runs=[((7, None, 'vi'), 0, slice(0, 6)),
                  ((7, None, 'vi'), 0, slice(7, 12)),
                  ((7, None, 'vi'), 0, slice(13, 18))],
       marks=[3, 3, 3],
       notes='The 27 m s–1 is the speed of the ball as it is released, '
             'calculated in the previous part.')

A.card(9, 'b', 'iv', topic='phys-3-3', concept='percentage-efficiency-of-a-drill',
       source='pdf',
       from_runs=[((8, 'b', 'iv'), 2, slice(2, 5)),
                  ((8, 'b', 'iv'), 3, slice(0, 2))],
       marks=[3, 3],
       checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme equally accepts the ratio of output power to input '
             'power for the first mark; it is typeset as maths the text layer '
             'cannot carry. The input power comes from the previous part.')

A.card(11, None, 'viii', topic='phys-3-2', concept='field-between-the-plates-of-a-capacitor',
       source='pdf', first_sentence=True,
       from_runs=[((11, None, 'viii'), 1, slice(0, 1)),
                  ((11, None, 'viii'), 2, slice(0, 1))],
       marks=[3, 3])

A.card(12, 'a', 'xi', topic='phys-4-5', concept='pair-annihilation-equation',
       source='pdf',
       from_run=((11, None, 'viii'), 11, slice(27, 30)), marks=[6],
       checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme equally accepts the annihilation equation written in '
             'full nuclear notation; its stacked sub- and superscripts do not '
             'survive the text layer, so the card shows the // alternative.')

A.emit()
