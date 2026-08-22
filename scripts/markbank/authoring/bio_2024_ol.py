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

# ── Parts the deck had not carded ──────────────────────────────────────────
# Question 3 pays four marks a part and Question 7 pays "5(4)" — five matches
# at four each — both printed in the scheme's own mark column. The scheme
# numbers its Section A answers one behind the paper, so the Question 3 and
# Question 7 cards name the scheme's Question 2 and Question 6 as their source.
A.card(3, 'c', topic='bio-1-4', concept='what-happens-at-stage-2-of-mitosis',
       source='pdf', from_run=((2, 'c', None), 1, slice(0, None)), marks=[4])

A.card(3, 'd', topic='bio-1-4', concept='what-happens-at-stage-3-of-mitosis',
       source='pdf', from_run=((2, 'd', None), 1, slice(0, None)), marks=[4])

A.card(7, 'b', topic='bio-u1', concept='what-tests-a-hypothesis',
       source='pdf', from_run=((6, 'b', None), 0, slice(5, 6)), marks=[4],
       checked='Question 7 is a matching table. The paper prints this part as a Column A description with no verb of its own, and the instruction to match it to a term in the list sits in the question stem the card already carries.')

A.card(7, 'c', topic='bio-u1', concept='what-a-control-is-for',
       source='pdf', from_run=((6, 'c', None), 0, slice(4, 5)), marks=[4],
       checked='Question 7 is a matching table. The paper prints this part as a Column A description with no verb of its own, and the instruction to match it to a term in the list sits in the question stem the card already carries.')

A.card(9, 'b', 'ii', topic='bio-u1', concept='preparing-the-enzyme',
       source='pdf', use=[1], marks=[3], row_kind='criterion')

A.card(13, 'b', 'iv', topic='bio-3-2', concept='fraction-of-f2-that-is-recessive',
       source='pdf', use=[1], marks=[3], first_sentence=True)

A.card(7, 'a', topic='bio-u1', concept='what-a-hypothesis-is',
       source='pdf', from_run=((6, 'a', None), 7, slice(5, 6)), marks=[4],
       checked='The paper prints this part as a Column A description in a matching table, so it has no verb of its own. The instruction to match it to a term in the list sits in the question stem the card already carries.')

A.card(7, 'd', topic='bio-u1', concept='what-data-is',
       source='pdf', from_run=((6, 'd', None), 0, slice(7, 8)), marks=[4],
       checked='Question 7 is a matching table. The paper prints this part as a Column A description with no verb of its own, and the instruction to match it to a term in the list sits in the question stem the card already carries.')

A.card(10, 'b', 'v', topic='bio-u1', concept='a-safety-precaution-in-the-experiment',
       source='pdf', use=[1], marks=[3], row_kind='criterion')

A.card(3, 'b', topic='bio-1-4', concept='the-structure-that-moves-chromosomes',
       source='pdf', from_run=((2, 'b', None), 1, slice(0, None)), marks=[3],
       notes='The scheme numbers this answer under its own Question 2 while the paper '
             'prints Question 3.')

A.card(11, 'b', 'i', topic='bio-3-1', concept='the-producer-in-a-food-web',
       source='pdf', from_run=((11, 'b', 'i'), 0, slice(0, 1)), marks=[3])

A.emit()
