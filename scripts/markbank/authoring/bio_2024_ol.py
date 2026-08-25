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

# ── Second pass over the open parts ────────────────────────────────────────
# Where an answer lives is a per-part fact, not a per-section one. The two
# parsers disagree about which question a Section A block belongs to — the PDF
# one runs two pages behind at Question 1 and one ahead at Question 3 — so the
# Section A cards below name the parser's key in from_run and cite the paper's.
# In Section C the keys line up for most parts and drift for the matching
# tables, where the scheme sets the answers as a two-column grid: Q14(c)(i)'s
# three answers are filed under the markdown parser's Q13(c)(i) and Q17(b)(ii)'s
# under its Q17(a)(ii). Each was found by searching both parsers for the answer
# text rather than by trusting either one's numbering.

# Q1 prints "5(4)" and a 4 beside every answer, so the tariff is the scheme's.
A.card(1, 'b', topic='bio-1-2', concept='the-fourth-element-in-protein',
       source='pdf', from_run=((3, 'b', None), 1, slice(0, None)), marks=[4],
       notes='Q1 (a)–(e) is marked 5(4) — five responses at four marks each — and '
             'the scheme prints the 4 beside this answer.')

# The PDF parser reads "Chromosome 3" as a mark block and loses the word, so
# this one answer comes from the markdown parser, where it heads a positional
# run of the whole of Question 3.
A.card(3, 'a', topic='bio-1-4', concept='the-structure-made-of-dna-and-protein',
       source='md', from_run=((4, 'a', None), 1, slice(0, 1)), marks=[3],
       notes='Q3 prices each part separately and they sum to the 20 the scheme '
             'prints: 3 + 3 + 4 + 4 + 3 + 3.')

# Q5 has no per-part mark: one ladder covers (a)–(d). `ladder` is the deck's
# shape for that — the row carries no mark, the scale goes in the notation, and
# the total is what the scheme's table pays for this many correct responses.
A.card(5, 'b', topic='bio-2-4', concept='bones-of-the-human-skeleton',
       source='pdf',
       from_runs=[((4, 'b', None), 1, slice(0, None)),
                  ((4, 'b', None), 2, slice(0, None)),
                  ((4, 'b', None), 3, slice(0, None))],
       ladder=9, tariff='orderedSplit', notation='6(3) + 2', labels='auto',
       notes='The paper asks for "the parts of the skeleton labelled A, B and C"; '
             'the scheme prints the same part as "Name the bones labelled A, B and '
             'C?". The citation follows the paper. No per-part mark exists — the '
             "scheme's table for Q5 (a)–(d) pays 9 for three correct responses.")

A.card(5, 'c', topic='bio-2-4', concept='the-joint-between-the-bones-of-the-skull',
       source='pdf', from_run=((4, 'c', None), 1, slice(0, None)),
       ladder=3, tariff='orderedSplit', notation='6(3) + 2', first_sentence=True,
       labels={'A': {'meaning': 'Skull or cranium', 'askedInThisQuestion': False}},
       notes='The paper adds "Put a tick () in the correct box." after the '
             'question; the tick is a private-use glyph the text layer cannot '
             'render, so the card carries the scheme-confirmed first sentence and '
             "the paper's three options sit in the stem. What part A is comes from "
             "the scheme's own answer to Q5(b) on the same diagram.")

A.card(9, 'b', 'vii', topic='bio-u2',
       concept='labelling-the-axes-of-an-enzyme-rate-graph',
       source='md', use=[0, 1], marks=[3, 3], labels='auto')

A.card(11, 'b', 'ii', topic='bio-3-1', concept='a-primary-consumer-in-a-food-web',
       source='md', use=[0], marks=[3])

A.card(11, 'b', 'iii', topic='bio-3-1', concept='a-secondary-consumer-in-a-food-web',
       source='md', use=[0], marks=[3])

A.card(11, 'b', 'iv', topic='bio-3-1', concept='what-the-arrows-in-a-food-web-mean',
       source='md', use=[0], marks=[3])

# The scheme answers this by printing the finished 2 x 2 grid. Its two filled
# rows come back as "PP Pp" and "Pp pp"; sliced a cell at a time they are the
# four genotypes, which is exactly what 4(3) pays for.
A.card(13, 'b', 'iii', topic='bio-1-4', concept='completing-the-f2-punnett-square',
       source='pdf',
       from_runs=[((13, 'b', 'iii'), 3, slice(0, 1)),
                  ((13, 'b', 'iii'), 3, slice(1, 2)),
                  ((13, 'b', 'iii'), 4, slice(0, 1)),
                  ((13, 'b', 'iii'), 4, slice(1, 2))],
       marks=[3, 3, 3, 3], notation='4(3)',
       notes='The scheme prints the answer as the completed Punnett square; the four '
             'cells of the grid are the four rows here.')

A.card(14, 'b', 'i', topic='bio-3-2',
       concept='drawing-and-labelling-a-bacterial-cell', source='md',
       from_runs=[((13, 'b', 'i'), 2, slice(4, None)),
                  ((13, 'b', 'i'), 3, slice(0, None)),
                  ((13, 'b', 'i'), 4, slice(0, None)),
                  ((13, 'b', 'i'), 5, slice(0, None))],
       marks=[3, 3, 3, 3], stem=False,
       checked='The paper ends this instruction on the list of parts to label — '
               '"Cell wall; DNA; Cytosol" — with no full stop, which is the only '
               'reason it is flagged. Page 5 of the Section C paper shows the part '
               'whole. The stem is dropped: the paper reader hands Q14(b) the words '
               '"Explain the underlined term.", which belong to part (iii).',
       notes='The scheme wants the cell membrane in the drawing as well, although the '
             'paper names only three parts to label.')

A.card(14, 'c', 'i', topic='bio-3-2', concept='amoeba-parts-on-the-diagram',
       source='md',
       from_runs=[((13, 'c', 'i'), 4, slice(4, None)),
                  ((13, 'c', 'i'), 5, slice(0, None)),
                  ((13, 'c', 'i'), 6, slice(0, None))],
       marks=[3, 3, 3], stem=False,
       checked='The paper ends this instruction on the third numbered term with no '
               'full stop, which is the only reason it is flagged; page 5 of the '
               'Section C paper shows the three terms are the whole of what is to be '
               'matched. The stem is dropped: the paper reader hands Q14(c) the '
               'asepsis and sterility statements, which belong to part (iv).')

A.card(15, 'b', 'v', topic='bio-2-5', concept='sketching-a-sperm-cell',
       source='md', use=[0], marks=[3], row_kind='criterion')

A.card(17, 'b', 'ii', topic='bio-2-4', concept='ear-parts-on-the-diagram',
       source='md',
       from_runs=[((17, 'a', 'ii'), 0, slice(0, None)),
                  ((17, 'a', 'ii'), 1, slice(0, None)),
                  ((17, 'a', 'ii'), 2, slice(0, None))],
       marks=[3, 3, 3],
       checked='The paper ends this instruction on the third numbered term with no '
               'full stop, which is the only reason it is flagged. Page 9 of the '
               'Section C paper shows the part whole.')

# ── Refused, and why ───────────────────────────────────────────────────────
# Said out loud rather than left as silence, because the next pass over this
# sitting should not have to rediscover any of it.
for ref, why in (
    ('2024 OL Q1(c)',
     'the scheme answers "Give one source of protein in the diet." with '
     '"Correct source named" and names no source, so there is nothing to show'),
    ('2024 OL Q2(f)',
     'the scheme answers the draw-an-arrow instruction with "Label correctly '
     'pointing at cell wall", which only repeats the instruction'),
    ('2024 OL Q4(b)',
     'the scheme answers "Give one example of a harmful virus." with "One harmful '
     'virus named" and names no virus'),
    ('2024 OL Q9(b)(vi)',
     'the scheme answers with "Correct safety precaution given" and gives none'),
    ('2024 OL Q10(b)(ii)',
     'the paper prints the ask ("draw a suitable graph to represent the data") in '
     'the block under the results table, and the reader gives this part only the '
     'lead-in sentence "The student’s average results are shown in the table '
     'below." — carding it would put a statement where the question goes'),
    ('2024 OL Q11(b)(v)',
     'the reader welds the tail of part (vi) onto this one, so the text reads '
     '"1. Write down any one food chain from the food web. 1. above. (27)"'),
    ('2024 OL Q11(b)(vi)',
     'the paper text stops mid-sentence at "the food chain you wrote down in part" '
     'because the reference to (b)(v) was pulled into the previous part'),
    ('2024 OL Q14(b)(iv)',
     'the scheme answers "Give one example of a beneficial bacterium." with "Any '
     'valid beneficial bacterium" and names none'),
    ('2024 OL Q17(c)(ii)',
     'the scheme answers with "Named plant" and "Matching organ used" twice over '
     'and names no plant and no organ'),
):
    print(f'REFUSED {ref}: {why}', file=sys.stderr)

A.emit()
