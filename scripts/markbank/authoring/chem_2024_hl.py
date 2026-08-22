#!/usr/bin/env python3
"""Chemistry 2024 Higher Level — parts the deck had not carded."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2024, 'hl')

# The scheme runs its answer on from the question it is repeating — "What can be
# concluded from your graph? rate proportional to concentration" — so the card
# takes the words after it. The "(3)" printed against the second conclusion is
# the mark for the pair; both are readings of the same graph.
A.card(3, 'b', 'iii', topic='chem-u2', concept='what-a-rate-graph-shows',
       source='pdf', from_run=((3, 'b', 'iii'), 0, slice(7, None)), marks=[3],
       checked='The paper prints the part mark "(20)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The question itself '
               'is complete: "What can be concluded from your graph?"')

A.card(5, 'b', 'vi', topic='chem-1-2', concept='shape-of-a-p-orbital',
       source='pdf', use=[0], marks=[6], first_sentence=True,
       notes='Three of the six are given for a drawing showing the two lobes overlapping.')

A.card(8, 'a', topic='chem-1-4', concept='geometry-change-during-addition',
       source='pdf', first_sentence=True,
       from_runs=[((8, 'a', None), 0, slice(12, 13)),
                  ((8, 'a', None), 3, slice(0, 1)),
                  ((8, 'a', None), 3, slice(2, 4)),
                  ((8, 'a', None), 4, slice(0, 1))],
       marks=[2, 1, 1, 1],
       notation='3 for the shape it starts as, 2 for what it becomes',
       notes='The scheme accepts trigonal or triangular for planar.')

A.emit()
