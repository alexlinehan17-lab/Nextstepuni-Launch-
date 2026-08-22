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

A.emit()
