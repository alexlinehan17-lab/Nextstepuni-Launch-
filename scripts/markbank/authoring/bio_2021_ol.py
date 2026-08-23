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

A.card(14, 'c', 'ii', topic='bio-2-6', concept='where-the-endocrine-glands-are',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3], notation='3 at 3 marks each',
       row_kind='anyN',
       checked='The question runs its list of glands on after the instruction without '
               'punctuation between them, which is why the text is flagged. Both halves '
               'are the question as printed.',
       notes='Any three of the scheme\'s six: it also allows the pancreas, the ovaries '
             'and the testes.')

A.emit()
