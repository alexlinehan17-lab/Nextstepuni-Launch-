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

A.emit()
