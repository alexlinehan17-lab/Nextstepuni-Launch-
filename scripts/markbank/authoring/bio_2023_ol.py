#!/usr/bin/env python3
"""Biology 2023 Ordinary Level — Question 2, the true/false statements.

Two things had to be settled before these could be carded.

The answers are ticks, read by ticks.py from the glyph's position against the
True/False column headings.

The questions come off a page that sets Question 2 beside another question, so
the block segmentation welds the neighbour's text on: (c) arrives as "Data
always involves numbers. Three bases together are known as a ………". The statement
is the first sentence, and first_sentence=True trims to it — but only after
checking the trimmed text appears in the marking scheme, which prints these
statements too. All seven are confirmed that way.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2023, 'ol')
READ = ('The scheme answers this by ticking a True/False column; the tick was read '
        'from its position on page 8 of the 2023 Ordinary Level marking scheme. The '
        'paper prints this statement beside another question, so the question text '
        'is the statement alone, confirmed against the scheme. Q2 is marked 6(3) + 2 '
        'over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'True',  'bio-u2', 'what-a-hypothesis-is'),
        ('b', 'False', 'bio-u2', 'sample-size-in-a-good-experiment'),
        ('c', 'False', 'bio-u2', 'data-need-not-be-numerical'),
        ('d', 'True',  'bio-u2', 'safety-as-a-principle-of-experimentation'),
        ('e', 'True',  'bio-u2', 'random-selection-in-experiments'),
        ('f', 'True',  'bio-u1', 'limitations-of-the-scientific-method'),
        ('g', 'False', 'bio-u1', 'a-theory-is-not-an-unsupported-hypothesis')):
    A.card(2, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False, first_sentence=True)

A.emit()
