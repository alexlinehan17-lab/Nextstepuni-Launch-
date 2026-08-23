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


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(2, None, 'v', topic='phys-u2', concept='plotting-one-over-pressure-against-volume',
       source='pdf',
       from_runs=[((2, None, 'v'), 2, slice(0, 2)),
                  ((2, None, 'v'), 2, slice(3, 5)),
                  ((2, None, 'v'), 2, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3')

A.card(7, None, 'viii', topic='phys-1-2', concept='forces-on-a-skydiver-at-constant-velocity',
       source='pdf',
       from_runs=[((7, None, 'viii'), 1, slice(10, 12)),
                  ((7, None, 'viii'), 1, slice(13, 15)),
                  ((7, None, 'viii'), 1, slice(16, 19))],
       marks=[2, 2, 2], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(9, None, 'ii', topic='phys-2-3', concept='ray-diagram-for-a-real-image',
       source='pdf',
       from_runs=[((9, None, 'ii'), 0, slice(0, 3)),
                  ((9, None, 'ii'), 0, slice(4, 7)),
                  ((9, None, 'ii'), 0, slice(8, 11)),
                  ((9, None, 'ii'), 0, slice(12, 18))],
       marks=[3, 3, 3, 2])

A.emit()
