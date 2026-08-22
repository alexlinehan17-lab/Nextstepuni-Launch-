#!/usr/bin/env python3
"""Biology 2025 Higher Level — the two photosynthesis pathways.

The scheme numbers its answers independently of the paper: this part's answer
sits under its Question 3 while the paper prints Question 13, so the card names
the scheme's key as its source.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2025, 'hl')

A.card(13, 'b', 'iii', topic='bio-2-3', concept='cyclic-and-non-cyclic-electron-flow',
       source='pdf', from_run=((3, 'b', 'iii'), 2, slice(0, None)), marks=[3])

A.emit()
