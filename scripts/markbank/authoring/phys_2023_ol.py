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

A.emit()
