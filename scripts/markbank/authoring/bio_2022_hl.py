#!/usr/bin/env python3
"""Biology 2022 Higher Level — Question 5, the true/false statements.

The scheme answers these by ticking a True or False column, and the tick is a
glyph the text layer drops. With nothing to attribute to this question both
parsers roll on and hand it the NEXT question's marking points, so joining the
two documents on their keys would put the wrong answers under these statements.

Questions lifted from the paper as always; each answer read off page 9 of the
2022 Higher Level marking scheme. Marked 6(3) + 2 across seven statements.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2022, 'hl')
READ = ('The scheme answers this by ticking a True/False column and the tick is a '
        'glyph the text extraction drops, so it was read from page 9 of the 2022 '
        'Higher Level marking scheme. Q5 is marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'False', 'bio-1-2', 'copper-is-a-trace-element'),
        ('b', 'True', 'bio-1-1', 'response-as-a-characteristic-of-life'),
        ('c', 'False', 'bio-1-3', 'animal-cell-in-a-concentrated-solution'),
        ('d', 'False', 'bio-2-6', 'which-cells-secrete-perforin'),
        ('e', 'True', 'bio-1-3', 'what-an-organ-is'),
        ('f', 'True', 'bio-2-4', 'ethene-ripens-fruit'),
        ('g', 'True', 'bio-3-2', 'fungi-are-heterotrophic'),
):
    A.card(5, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False)

A.emit()
