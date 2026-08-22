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

A.emit()
