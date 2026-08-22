#!/usr/bin/env python3
"""Biology 2024 Higher Level — Question 5, the true/false statements.

The scheme answers these by ticking a True or False column, and the tick is a
glyph the text layer drops. With nothing to attribute to this question both
parsers roll on and hand it the NEXT question's marking points, so joining the
two documents on their keys would put the wrong answers under these statements.

Questions lifted from the paper as always; each answer read off page 10 of the
2024 Higher Level marking scheme. Marked 6(3) + 2 across seven statements.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2024, 'hl')
READ = ('The scheme answers this by ticking a True/False column and the tick is a '
        'glyph the text extraction drops, so it was read from page 10 of the 2024 '
        'Higher Level marking scheme. Q5 is marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'False', 'bio-1-3', 'which-cells-have-cell-walls'),
        ('b', 'False', 'bio-1-3', 'what-a-turgid-cell-is'),
        ('c', 'True', 'bio-2-2', 'fermentation-is-anaerobic'),
        ('d', 'False', 'bio-1-4', 'where-dna-is-found-in-the-cell'),
        ('e', 'False', 'bio-1-4', 'hydrogen-bonds-in-dna'),
        ('f', 'True', 'bio-1-4', 'which-bases-are-purines'),
        ('g', 'True', 'bio-1-4', 'what-chromosomes-are-made-of'),
):
    A.card(5, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False)

A.card(12, 'c', 'iv', topic='bio-3-1', concept='counting-trophic-levels',
       source='pdf', from_run=((3, None, 'iv'), 0, slice(0, None)), marks=[3],
       checked='The paper runs this part into the next in one block, so the text stops at '
               '"in part". The question asked is the one the scheme answers.',
       notes='The scheme numbers this answer under its own Question 3 while the paper '
             'prints Question 12.')

A.emit()
