#!/usr/bin/env python3
"""Biology 2021 Ordinary Level — parts the deck had not carded.

The scheme answers on the same line as the question it is repeating, so each
answer is taken out of that line rather than off one of its own.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2021, 'ol')

# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(9, 'b', 'vii', topic='bio-2-1', concept='enzyme-activity-against-ph-curve',
       source='pdf', from_run=((9, 'b', 'vii'), 0, slice(13, None)), marks=[3])

A.card(11, 'b', 'vii', topic='bio-3-1', concept='food-chain-from-a-passage',
       source='pdf', from_run=((11, 'b', 'vii'), 0, slice(11, 18)), marks=[3],
       checked='The paper prints the part mark "(27)" after the question, so the text ends '
               'on a bracketed number rather than punctuation.')

A.emit()
