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

A.emit()
