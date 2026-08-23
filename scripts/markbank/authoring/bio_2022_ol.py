#!/usr/bin/env python3
"""Biology 2022 Ordinary Level — Question 6, the true/false statements.

The scheme answers these by ticking a True or False column, and the tick is a
glyph the text layer drops. With nothing to attribute to this question both
parsers roll on and hand it the NEXT question's marking points, so joining the
two documents on their keys would put the wrong answers under these statements.

Questions lifted from the paper as always; each answer read off page 9 of the
2022 Ordinary Level marking scheme. Marked 6(3) + 2 across seven statements.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2022, 'ol')
READ = ('The scheme answers this by ticking a True/False column and the tick is a '
        'glyph the text extraction drops, so it was read from page 9 of the 2022 '
        'Ordinary Level marking scheme. Q6 is marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'True', 'bio-2-4', 'endocrine-glands-produce-hormones'),
        ('b', 'True', 'bio-2-5', 'where-fertilisation-occurs'),
        ('c', 'False', 'bio-2-6', 'which-organ-produces-hydrochloric-acid'),
        ('d', 'False', 'bio-2-6', 'which-organ-produces-bile'),
        ('e', 'True', 'bio-2-4', 'nerve-cells-produce-neurotransmitters'),
        ('f', 'False', 'bio-3-2', 'what-produces-antibiotics'),
        ('g', 'True', 'bio-2-6', 'salivary-glands-produce-amylase'),
):
    A.card(6, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False)

# ── Q7(b): the matching table ─────────────────────────────────────────────
# The scheme prints the description and the term it matches on one line, and
# its own mark column gives four.
A.card(7, 'b', topic='bio-u1', concept='what-a-hypothesis-is',
       source='pdf', from_run=((6, 'b', None), 0, slice(6, 7)), marks=[4],
       checked='The paper prints this part as a Column A description in a matching table, so it has no verb of its own. The instruction to match it to a term in the list sits in the question stem the card already carries.')

A.card(8, 'b', 'iii', topic='bio-u1', concept='percentage-frequency-from-a-quadrat-table',
       source='pdf',
       from_runs=[((8, 'b', 'iii'), 0, slice(14, 18)),
                  ((8, 'b', 'iii'), 0, slice(19, 23))],
       marks=[3, 3])

A.card(14, 'c', 'iii', topic='bio-1-3', concept='which-cell-is-turgid',
       source='pdf', from_run=((14, 'c', 'iii'), 0, slice(4, 6)), marks=[3],
       notes='A and B are the two plant cells drawn in the paper, one full and firm '
             'against its wall, the other with the membrane pulled away from it.')

A.card(11, 'b', 'vii', topic='bio-3-1', concept='writing-a-food-chain-from-a-web',
       source='pdf', from_run=((11, 'b', 'vii'), 0, slice(1, 8)), marks=[3],
       notes='The scheme requires the chain to start with a producer.')

A.card(14, 'c', 'v', topic='bio-1-3', concept='the-storage-organelle-of-a-plant-cell',
       source='pdf', from_run=((14, 'c', 'v'), 0, slice(0, 1)), marks=[3])

A.card(16, 'b', 'i', topic='bio-1-2', concept='drawing-a-typical-bacterial-cell',
       source='pdf',
       from_runs=[((16, 'a', 'i'), 3, slice(1, None)),
                  ((16, 'a', 'i'), 4, slice(1, None))],
       marks=[7, 2], notation='7 for the diagram, 2 a label',
       notes='The scheme numbers this answer under its own Question 16(a) while the '
             'paper prints 16(b). Cell wall, cell membrane and an indication of DNA are '
             'what the drawing must contain.')

A.card(17, 'c', 'i', topic='bio-2-4', concept='drawing-the-internal-structure-of-the-heart',
       source='pdf',
       from_runs=[((17, 'b', 'i'), 3, slice(1, 7)),
                  ((17, 'b', 'i'), 3, slice(8, None))],
       marks=[7, 2], notation='7 for the diagram, 2 a label',
       notes='The scheme numbers this answer under its own Question 17(b) while the '
             'paper prints 17(c).')

A.card(7, 'c', topic='bio-u1', concept='what-data-is',
       source='md', from_run=((6, 'c', None), 0, slice(0, 1)), marks=[4],
       checked='Question 7 is a matching table. The paper prints this part as a Column A '
               'description with no verb of its own, and the instruction to match it to a '
               'term in the list sits in the question stem the card already carries.',
       notes='The scheme prices Q7(a) to (e) on a scale of 4, 8, 12, 16, 20 for one to '
             'five correct — evenly, so each is worth four.')

A.emit()
