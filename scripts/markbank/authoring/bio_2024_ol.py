#!/usr/bin/env python3
"""Biology 2024 Ordinary Level — Question 6, the true/false statements.

Answers read by ticks.py, which finds the tick glyph (U+F050) in the text layer
and matches its x against the True/False column headings and its y against the
statement beside it. Checked against a rendered page on three other sets before
being trusted here.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2024, 'ol')
READ = ('The scheme answers this by ticking a True/False column. The tick is a glyph '
        'the text extraction leaves in an empty-looking block, so it was read from '
        'its position on page 10 of the 2024 Ordinary Level marking scheme. Q6 is '
        'marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'True',  'bio-u2',  'what-the-microscope-stage-does'),
        ('b', 'True',  'bio-1-3', 'where-protein-synthesis-happens'),
        ('c', 'False', 'bio-1-3', 'which-cells-have-cell-walls'),
        ('d', 'False', 'bio-1-3', 'what-a-tissue-is'),
        ('e', 'True',  'bio-2-1', 'immobilised-enzymes-are-reusable'),
        ('f', 'True',  'bio-1-3', 'osmosis-as-a-kind-of-diffusion'),
        ('g', 'False', 'bio-1-3', 'cell-membranes-are-selectively-permeable')):
    A.card(6, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False)

A.emit()
