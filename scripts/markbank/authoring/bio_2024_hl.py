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

A.card(12, 'b', 'ii', topic='bio-3-1', concept='explaining-a-predator-prey-graph',
       source='pdf',
       from_runs=[((2, 'b', 'ii'), 1, slice(0, None)),
                  ((2, 'b', 'ii'), 2, slice(0, None)),
                  ((2, 'b', 'ii'), 4, slice(0, None))],
       marks=[2, 2, 2],
       notes='The scheme numbers this answer under its own Question 2 while the paper '
             'prints Question 12. It wants three separate observations: the shape of the '
             'line, the numbers involved, and the delay in time.')

A.card(12, 'b', 'iii', topic='bio-3-1', concept='what-happens-to-prey-if-the-predator-fails',
       source='pdf',
       from_runs=[((2, 'b', 'iii'), 1, slice(0, None)),
                  ((2, 'b', 'iii'), 3, slice(0, None))],
       marks=[3, 3])

# 2024 HL Q12(c)(iii) is not carded. Its whole marking point is "Any correct
# food chain from the food web", which the build refuses as a content-free row —
# rightly, because a card whose answer is "any correct answer" teaches nothing.

A.card(12, 'b', 'i', topic='bio-3-1', concept='drawing-the-predator-curve',
       source='pdf',
       from_runs=[((2, 'b', 'i'), 1, slice(0, None)),
                  ((2, 'b', 'i'), 2, slice(0, None))],
       marks=[2, 2],
       notes='The scheme numbers this answer under its own Question 2 while the paper '
             'prints Question 12. Both marks are for the shape of the curve rather than '
             'for the drawing itself.')

A.card(12, 'b', 'v', topic='bio-3-1', concept='why-human-numbers-do-not-follow-the-curve',
       source='pdf',
       from_runs=[((2, 'b', 'v'), 1, slice(0, None)),
                  ((2, 'b', 'v'), 2, slice(0, None))],
       marks=[4, 4], notation='2 at 4 marks each',
       notes='The scheme also allows a lack of predators, or any other correct reason.',
       checked='The paper prints the part mark "(27)" after the question and runs the '
               'graph labels on after it, so the text does not end on punctuation.')

A.emit()
