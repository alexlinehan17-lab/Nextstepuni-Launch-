#!/usr/bin/env python3
"""Chemistry 2021 Ordinary Level — parts the deck had not carded.

The scheme numbers its answer sections independently of the paper, so this
part's answers sit under its Question 6 while the paper prints Question 11.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2021, 'ol')

A.card(11, 'a', 'iii', topic='chem-1-2', concept='elements-with-the-same-energy-levels',
       source='pdf',
       from_runs=[((6, 'a', 'iii'), 0, slice(1, None)),
                  ((6, 'a', 'iii'), 1, slice(0, 2))],
       marks=[6], use=[[0, 1]],
       notes='Either element scores: both lithium and beryllium fill the same two main '
             'energy levels that boron does.')

A.emit()
