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

A.emit()
