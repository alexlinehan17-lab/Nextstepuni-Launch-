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

A.emit()
