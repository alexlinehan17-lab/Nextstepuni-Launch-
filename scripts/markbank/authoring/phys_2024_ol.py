#!/usr/bin/env python3
"""Physics 2024 Ordinary Level — two parts whose answer runs on from the cue.

The scheme sets the question and its answer in one line, so both cards take
their marking point out of that line rather than off one of its own.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2024, 'ol')

A.card(11, None, 'i', topic='phys-3-3', concept='example-of-an-electrical-conductor',
       source='pdf', from_run=((11, None, 'i'), 0, slice(7, 10)), marks=[5],
       row_kind='criterion')

A.card(14, 'a', 'ii', topic='phys-1-1', concept='acceleration-at-constant-velocity',
       source='pdf', from_run=((14, 'a', 'ii'), 0, slice(7, 10)), marks=[2])

A.card(13, 'a', topic='phys-1-4', concept='height-of-the-iss',
       source='pdf', from_run=((13, 'a', None), 0, slice(8, 10)), marks=[7],
       checked='The paper prints the part mark "(7)" after the question, so the text ends '
               'on a bracketed number rather than punctuation.')

A.card(14, 'a', 'iii', topic='phys-1-1', concept='velocity-after-constant-acceleration',
       source='pdf', from_run=((14, 'a', 'iii'), 0, slice(10, 13)), marks=[2])

A.card(3, None, 'ii', topic='phys-u2', concept='supplying-heat-in-the-calorimeter-experiment',
       source='pdf', from_run=((3, None, 'ii'), 0, slice(18, 21)), marks=[6],
       row_kind='criterion',
       checked='The paper prints the part mark "(16)" after the question. The scheme '
               'reprints the question as "supply the heat energy to increase", dropping '
               'the paper\'s "needed", so the trim cannot be confirmed against it — the '
               'paper\'s own wording is what the card carries.')

A.card(5, None, 'ii', topic='phys-u2', concept='varying-temperature-in-the-resistance-experiment',
       source='pdf', from_run=((5, None, 'ii'), 0, slice(11, 15)), marks=[6],
       row_kind='criterion')

A.card(1, None, 'v', topic='phys-u2', concept='clockwise-moments-on-a-metre-stick',
       source='pdf', use=[0], marks=[6])

A.card(14, 'a', 'i', topic='phys-1-2', concept='net-force-when-forces-balance',
       source='pdf', from_run=((14, 'a', 'i'), 0, slice(0, 6)), marks=[4])

A.card(14, 'a', 'v', topic='phys-1-2', concept='net-force-when-forces-do-not-balance',
       source='pdf', from_run=((14, 'a', 'v'), 0, slice(0, 7)), marks=[5])

A.card(14, 'a', 'vii', topic='phys-1-1', concept='velocity-under-an-unbalanced-force',
       source='pdf', from_run=((14, 'a', 'vii'), 0, slice(0, 9)), marks=[5], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(2, None, 'i', topic='phys-u2', concept='apparatus-for-the-focal-length-experiment',
       source='pdf',
       from_runs=[((2, None, 'i'), 0, slice(0, 2)),
                  ((2, None, 'i'), 0, slice(2, 3)),
                  ((2, None, 'i'), 0, slice(3, 4)),
                  ((2, None, 'i'), 0, slice(4, 6))],
       marks=[4, 4, 2, 2], notation='4 + 4 + 2 + 2', notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(5, None, 'i', topic='phys-u2', concept='apparatus-for-the-resistance-temperature-experiment',
       source='pdf',
       from_runs=[((5, None, 'i'), 0, slice(0, 1)),
                  ((5, None, 'i'), 0, slice(1, 2)),
                  ((5, None, 'i'), 0, slice(2, 3)),
                  ((5, None, 'i'), 0, slice(3, 4))],
       marks=[4, 4, 2, 2], notation='4 + 4 + 2 + 2', notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(5, None, 'iv', topic='phys-u2', concept='graph-of-resistance-against-temperature-ol',
       source='pdf',
       from_runs=[((5, None, 'iv'), 0, slice(0, 2)),
                  ((5, None, 'iv'), 0, slice(3, 6)),
                  ((5, None, 'iv'), 0, slice(6, 10))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3')

A.card(7, None, 'iv', topic='phys-1-2', concept='forces-on-a-bar-held-still',
       source='pdf', from_run=((7, None, 'iv'), 0, slice(0, 6)), marks=[9],
       notation='4 + 4 + 1')

A.card(7, None, 'viii', topic='phys-1-1', concept='velocity-time-graph-of-a-bus-journey',
       source='pdf',
       from_runs=[((7, None, 'viii'), 0, slice(0, 2)),
                  ((7, None, 'viii'), 0, slice(3, 5)),
                  ((7, None, 'viii'), 0, slice(6, 9)),
                  ((7, None, 'viii'), 0, slice(10, 12))],
       marks=[3, 3, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(8, None, 'v', topic='phys-2-3', concept='ray-diagram-for-a-magnified-image',
       source='pdf',
       from_runs=[((8, None, 'v'), 0, slice(0, 3)),
                  ((8, None, 'v'), 0, slice(4, 7)),
                  ((8, None, 'v'), 0, slice(8, 11)),
                  ((8, None, 'v'), 0, slice(12, 14))],
       marks=[3, 3, 3, 2])

A.card(12, None, 'vii', topic='phys-4-3', concept='where-the-neutrons-are-in-an-atom',
       source='pdf', from_run=((12, None, 'vii'), 0, slice(0, 8)), marks=[6])

A.card(13, 'e', topic='phys-4-2', concept='parts-of-an-x-ray-tube-ol',
       source='pdf',
       from_runs=[((13, 'e', None), 0, slice(0, 2)),
                  ((13, 'e', None), 0, slice(2, 6)),
                  ((13, 'e', None), 1, slice(0, 2))],
       marks=[3, 2, 2], notation='3 + 2 + 2', checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme also credits shielding and the glass tube, and takes a mark off '
             'if the diagram carries no labels.')

A.card(14, 'b', 'ii', topic='phys-3-3', concept='resistance-temperature-graph-for-a-thermistor',
       source='pdf',
       from_runs=[((14, 'b', 'ii'), 0, slice(0, 2)),
                  ((14, 'b', 'ii'), 0, slice(3, 5))],
       marks=[3, 3])

A.card(14, 'd', 'v', topic='phys-3-1', concept='charge-on-a-pear-shaped-conductor',
       source='pdf', from_run=((14, 'd', 'v'), 0, slice(0, 6)), marks=[4], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(4, None, 'vi', topic='phys-u2', concept='graph-of-frequency-against-one-over-length-ol',
       source='pdf',
       from_runs=[((4, None, 'vi'), 1, slice(2, 4)),
                  ((4, None, 'vi'), 1, slice(5, 7)),
                  ((4, None, 'vi'), 1, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3', checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(10, None, 'iv', topic='phys-2-6', concept='next-harmonic-in-a-closed-pipe',
       source='pdf', use=[0], marks=[6],
       context='The pipe is the clarinet of the preceding parts, modelled as a pipe '
               'closed at one end.')


# ── Closing the remaining open parts ───────────────────────────────────────
A.card(1, None, 'iv', topic='phys-u2', concept='verifying-the-first-law-of-equilibrium',
       source='pdf', from_run=((1, None, 'iv'), 0, slice(0, 20)), marks=[6])

A.card(1, None, 'vi', topic='phys-u2', concept='anticlockwise-moments-on-a-metre-stick',
       source='pdf', use=[0], marks=[6])

A.card(1, None, 'vii', topic='phys-u2', concept='verifying-the-second-law-of-equilibrium',
       source='pdf', use=[0], marks=[4],
       checked='The paper prints the question total "(22)" after the question, so the '
               'text ends on a bracketed number rather than punctuation. The question '
               'itself is complete.')

A.card(2, None, 'ii', topic='phys-u2', concept='labelling-object-and-image-distances',
       source='pdf', first_sentence=True,
       from_run=((2, None, 'ii'), 0, slice(0, 4)), marks=[6],
       notation='4 + 2', row_kind='criterion')

A.card(3, None, 'i', topic='phys-u2',
       concept='apparatus-for-the-specific-heat-capacity-experiment',
       source='pdf', from_run=((3, None, 'i'), 0, slice(0, 20)), marks=[10],
       notation='any 4: 4 + 2 + 2 + 2', row_kind='criterion',
       notes='The scheme pays for any four of the listed items and takes a mark off '
             'if the diagram carries no labels.')

A.card(3, None, 'v', topic='phys-u2',
       concept='completing-the-specific-heat-capacity-calculation',
       source='pdf',
       from_runs=[((3, None, 'v'), 0, slice(0, 3)),
                  ((3, None, 'v'), 0, slice(4, 7)),
                  ((3, None, 'v'), 0, slice(8, 14))],
       marks=[4, 4, 4],
       context='The paper prints the calculation to complete: ∆E = mwater cwater '
               'Δθwater + mcalorimeter ccopper Δθcalorimeter, filled in as '
               '3467 = A × cwater × B + 0.106 × 390 × B.')

A.card(4, None, 'v', topic='phys-u2', concept='completing-the-one-over-length-table',
       source='pdf', from_run=((4, None, 'v'), 2, slice(5, 9)), marks=[4],
       notation='4 × 1',
       notes='The four values are the missing entries of the 1/l row, in table '
             'order; each scores one mark.')

A.card(5, None, 'iii', topic='phys-u2',
       concept='safety-precaution-in-the-resistance-experiment',
       source='pdf', first_sentence=True,
       from_run=((5, None, 'iii'), 0, slice(0, 3)), marks=[4], row_kind='criterion')

A.card(5, None, 'vi', topic='phys-u2', concept='estimating-temperature-from-the-graph',
       source='pdf', first_sentence=True, use=[0], marks=[3],
       context='The student used the apparatus to estimate the temperature of an '
               'unknown liquid; its resistance measured 5.5 Ω.')

A.card(8, None, 'vii', topic='phys-2-3', concept='magnification-of-a-concave-mirror-image',
       source='pdf', from_run=((8, None, 'vii'), 2, slice(1, 3)), marks=[6],
       notes='The scheme sets the working, image distance over object distance, as a '
             'stacked fraction the text layer cannot carry, so the card holds the '
             'result line alone, its unit as printed.')

A.card(8, None, 'viii', topic='phys-2-3', concept='image-height-from-magnification',
       source='pdf', use=[0], marks=[6],
       checked='The paper prints the question total "(29)" after the question, so the '
               'text ends on a bracketed number rather than punctuation. The question '
               'itself is complete.')

A.card(9, None, 'vii', topic='phys-2-1', concept='parts-of-a-heat-pump',
       source='pdf', first_sentence=True,
       from_runs=[((9, None, 'vii'), 0, slice(0, 2)),
                  ((9, None, 'vii'), 0, slice(3, 5)),
                  ((9, None, 'vii'), 0, slice(6, 8))],
       marks=[3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(10, None, 'viii', topic='phys-2-6', concept='fundamental-in-a-pipe-open-at-both-ends',
       source='pdf', from_run=((10, None, 'viii'), 0, slice(0, 10)), marks=[6])

A.card(12, None, 'vi', topic='phys-4-4', concept='daughter-nucleus-after-alpha-decay',
       source='pdf', from_run=((12, None, 'vi'), 1, slice(0, 2)), marks=[6],
       notation='3 × 2',
       notes='The scheme sets each nuclide with stacked atomic and mass numbers; the '
             'text layer flattens them to bare digits after the symbol, in the '
             'question and in the answer alike.')

A.card(14, 'a', 'vi', topic='phys-1-1', concept='acceleration-under-an-unbalanced-force',
       source='pdf', from_run=((14, 'a', 'vi'), 2, slice(1, 4)), marks=[5],
       notes='The scheme sets the working, force over mass, as a stacked fraction '
             'the text layer cannot carry, so the card holds the result at the '
             'part\'s full printed tariff.')

A.emit()
