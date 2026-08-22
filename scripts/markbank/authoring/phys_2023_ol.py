#!/usr/bin/env python3
"""Physics 2023 Ordinary Level — parts the deck had not carded.

The scheme repeats each question before answering it, so the answer is taken
out of the line rather than off one of its own.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2023, 'ol')

A.card(13, 'b', 'v', topic='phys-4-4', concept='daughter-nucleus-after-beta-decay',
       source='pdf', from_run=((13, 'b', 'v'), 1, slice(0, 2)), marks=[3],
       checked='The paper prints the part mark "(7)" after the question, so the text ends '
               'on a bracketed number rather than punctuation. The question itself is '
               'complete.',
       notes='The scheme prints "[3 + 2 + 2]" against this line, covering this part and '
             'the two that follow it.')

A.card(10, None, 'vi', topic='phys-2-4', concept='nodes-on-a-stationary-wave',
       source='pdf', from_run=((10, None, 'vi'), 0, slice(9, 10)), marks=[4],
       notes='The scheme reprints the question above its answer and the two run together '
             'in one line, so the answer is the word after the question mark.')

A.card(10, None, 'vii', topic='phys-2-4', concept='amplitude-on-a-stationary-wave',
       source='pdf', use=[0], marks=[4])

A.card(10, None, 'viii', topic='phys-2-4', concept='wavelength-from-node-separation',
       source='pdf', from_run=((10, None, 'viii'), 1, slice(0, 6)), marks=[6],
       notes='The scheme runs the next part on from this answer in the same line; the '
             'six words taken are this part\'s working and result.')

A.card(13, 'b', 'viii', topic='phys-4-6', concept='why-fusion-is-preferred-to-fission',
       source='pdf', from_run=((13, 'b', 'viii'), 1, slice(12, 17)), marks=[7],
       checked='The paper prints this part as the sentence introducing the question that '
               'follows it in the same block. The question asked is the one the scheme '
               'reprints above its answer.')

A.card(11, None, 'vii', topic='phys-3-3', concept='why-a-filament-graph-curves',
       source='pdf', use=[[1, 2, 3]], marks=[6],
       notes='The scheme prints three ways of saying it and pays six for any of them, '
             'with three for a partial answer.')

A.card(8, None, 'iv', topic='phys-2-3', concept='angle-of-refraction-from-snells-law',
       source='pdf', first_sentence=True,
       from_runs=[((8, None, 'iv'), 0, slice(12, 17)),
                  ((8, None, 'iv'), 0, slice(18, 19)),
                  ((8, None, 'iv'), 0, slice(20, 23))],
       marks=[3, 3, 3])

# 2023 OL Q3(i) is not carded. It asks for the equipment labelled A on a diagram
# the card cannot show, and the build refuses a card that names a lettered part
# without a labelled figure behind it.

A.card(7, None, 'v', topic='phys-1-4', concept='velocity-from-energy-or-suvat',
       source='pdf',
       from_runs=[((7, None, 'v'), 0, slice(0, 9)),
                  ((7, None, 'v'), 0, slice(10, 11)),
                  ((7, None, 'v'), 0, slice(12, 17))],
       marks=[3, 3, 3],
       notes='Either route scores, the energy one or the equation of motion, but a '
             'partial answer cannot be taken from both.')

A.card(8, None, 'vi', topic='phys-2-3', concept='image-position-for-a-converging-lens',
       source='pdf',
       from_runs=[((8, None, 'vi'), 0, slice(7, 12)),
                  ((8, None, 'vi'), 0, slice(13, 14)),
                  ((8, None, 'vi'), 0, slice(15, 19))],
       marks=[3, 3, 3])

A.card(11, None, 'v', topic='phys-3-3', concept='total-resistance-of-two-parallel-bulbs',
       source='pdf',
       from_runs=[((11, None, 'v'), 0, slice(9, 14)),
                  ((11, None, 'v'), 0, slice(15, 16)),
                  ((11, None, 'v'), 0, slice(17, 21))],
       marks=[3, 3, 3])

A.emit()
