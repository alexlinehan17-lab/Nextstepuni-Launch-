#!/usr/bin/env python3
"""Biology 2025 Ordinary Level — the order of the stages of mitosis.

The four images the question orders are catalogued as a truncated crop, so the
card cannot show them. It does not need to: the answer is the order itself, and
the letters are named in the question the paper prints.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2025, 'ol')

A.card(7, 'a', topic='bio-1-4', concept='order-of-the-stages-of-mitosis',
       source='pdf', from_run=((6, 'a', None), 2, slice(0, 4)), marks=[6],
       notation='3 for any two in the right place, 6 for all four',
       notes='The scheme numbers this answer under its own Question 6 while the paper '
             'prints Question 7.')

A.emit()
