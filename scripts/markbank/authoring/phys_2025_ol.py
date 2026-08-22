#!/usr/bin/env python3
"""Physics 2025 Ordinary Level — the case for fusion over fission.

The scheme numbers its answer sections independently of the paper, so this
part's answers sit under its Question 11 while the paper prints Question 12.
from_run names the scheme's key rather than the paper's for that reason.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2025, 'ol')

A.card(12, 'b', 'vii', topic='phys-4-6', concept='advantage-of-fusion-over-fission',
       source='pdf', from_run=((11, 'b', 'vii'), 1, slice(0, 5)), marks=[3],
       row_kind='criterion',
       checked='The paper prints the part mark "(36)" for the whole question after this '
               'part, so the text ends on a number and a page footer. The question itself '
               'is complete.')

A.card(8, None, 'vii', topic='phys-2-3', concept='why-sound-diffracts-and-light-does-not',
       source='pdf', from_run=((8, None, 'vii'), 2, slice(0, 3)), marks=[4],
       row_kind='criterion')

A.emit()
