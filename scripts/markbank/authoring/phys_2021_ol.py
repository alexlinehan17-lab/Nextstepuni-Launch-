#!/usr/bin/env python3
"""Physics 2021 Ordinary Level — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2021, 'ol')

A.card(8, None, 'vii', topic='phys-2-3', concept='what-diffraction-through-a-gap-looks-like',
       source='pdf', from_run=((2, None, 'vii'), 0, slice(17, 23)), marks=[6],
       notation='6, or 3 for a partial answer',
       notes='The scheme numbers this answer under its own Question 2 while the paper '
             'prints Question 8.')

A.emit()
