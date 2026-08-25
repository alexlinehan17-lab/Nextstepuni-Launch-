#!/usr/bin/env python3
"""Chemistry 2021 Ordinary Level — parts the deck had not carded.

Nothing here is joined on the part key. The two scheme parsers disagree about
this sitting badly enough that the key is worthless: Scheme (markdown) finds no
parts at all, and SchemePdf files the whole paper under Questions 1, 4 and 6 —
the leading digits of the passage answers "4 Rutherford" and "6 Bohr" are eaten
as question heads, and every part after them is filed behind. So the parser key
that holds a run is only an address; the pairing was made by reading the paper
page against the scheme page, and each card below says which page.

The scheme's own numbering does agree with the paper's — Question 3 answers
Question 3, Question 11 answers Question 11. It is the parse that moved, not the
document.

Tariffs are read off the scheme and checked against the total the paper prints
for the parent part, which is what makes a split confirmed rather than assumed:
Q3(a) 5 x 3 = the 15 the paper prints; Q7(a) 6 + 6 + 6 + 3 + 3 = the 24;
Q8(a) 3 + 6 + 6 = the 15; Q9(b) 15 + 6 = the 21 and Q9(c) 3 + 6 + 6 = the 15;
Q10(c) 6 + 12 + 7 = the 25; Q5(c) 3 + 3 + 6 = the 12.

Q10(a) is the one part with no per-row tariff: the scheme prices its seven
blanks as one lot, "2 x 6 + 4 x 3 + 1", and never says which blank carries
which mark. It is carded ladder= — rows with no marks of their own, the shape
written into the notation — rather than given a split nobody printed.

One known wrong field, left wrong on purpose. This paper puts Questions 1-3 in
Section A and 4-11 in Section B, but lib.Author sets section from `q <= 12`, so
every card below outside Question 3 ships section "A" when the paper says "B".
That is lib's rule, not this file's, and the card already shipped from here —
chem-2021-ol-q11-a-iii — carries the same "A" while the hand-written
chem-2021-ol-q9-a and chem-2021-ol-q10-b-iii carry "B". Fixing it means fixing
lib for every subject at once, which is a change this file must not make alone.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2021, 'ol')

A.card(11, 'a', 'iii', topic='chem-1-2', concept='elements-with-the-same-energy-levels',
       source='pdf',
       from_runs=[((6, 'a', 'iii'), 0, slice(1, None)),
                  ((6, 'a', 'iii'), 1, slice(0, 2))],
       marks=[6], use=[[0, 1]],
       notes='Either element scores: both lithium and beryllium fill the same two main '
             'energy levels that boron does.')

# -- Question 3, the neutralisation calorimetry experiment (paper page 4) ------

# The five plotting marks are printed as one run against the parent, each with
# its own (3) inline. The paper prints (15) for part (a) and 5 x 3 is that 15.
A.card(3, 'a', topic='chem-u2', concept='graph-of-temperature-against-time',
       source='pdf',
       from_runs=[((1, 'a', None), 1, slice(1, 18)),
                  ((1, 'a', None), 1, slice(19, 22)),
                  ((1, 'a', None), 1, slice(23, 27)),
                  ((1, 'a', None), 1, slice(28, 33)),
                  ((1, 'a', None), 1, slice(45, 50))],
       marks=[3, 3, 3, 3, 3], notation='5 x 3',
       checked='Page 4 prints the ask and its tariff in one block, so the lifted text '
               'ends "(15)". The (15) is the mark for part (a) — the scheme awards '
               'five plotting marks of 3 — and the ask itself is complete: "Plot a '
               'graph (on graph paper) of temperature versus time (x-axis)."',
       notes='The scheme takes 3 off if the graph is not drawn on graph paper, accepts '
             'the axes the other way round, and on this graph allows the points to be '
             'joined by straight lines rather than a curve.')

A.card(3, 'b', 'i', topic='chem-3-1', concept='maximum-temperature-change',
       source='pdf', from_run=((1, 'b', 'i'), 3, slice(1, 5)), marks=[6],
       notes='A range, not a single value: the change is read off the graph plotted in '
             'part (a), against an initial temperature of 16.0 °C.')

# -- Question 5, bonding in BeO (paper page 7) --------------------------------

# The paper asks for a dot and cross diagram "or otherwise" and the scheme says
# "[Diagram not essential.]", printing the transfer in words as an equally
# accepted route — which is why this one is carded and Q5(d)(ii) below is not.
A.card(5, 'c', 'iii', topic='chem-2-1', concept='electron-transfer-in-beo',
       source='pdf',
       from_runs=[((1, 'c', 'iii'), 3, slice(0, None)),
                  ((1, 'c', 'iii'), 4, slice(1, None))],
       marks=[3, 3], notation='2 x 3',
       checked='Page 7 prints (12) against the whole of Q5(c). Its (i) and (ii) take 3 '
               'each for the two electron arrangements, leaving 6 here, which is the '
               '(2 x 3) the scheme prints. The ask itself ends at "show how the bonding '
               'in BeO arises."',
       notes='The scheme prints "[Diagram not essential.]", so describing the transfer '
             'in words scores the full six; a dot and cross diagram showing the two '
             'ions is the other accepted route.')

# -- Question 7, treating acidic drinking water (paper page 8) -----------------

A.card(7, 'a', 'v', topic='chem-3-4', concept='effect-of-adding-base-on-ph',
       source='pdf', from_run=((1, 'a', 'v'), 0, slice(1, 2)), marks=[3],
       checked='Page 8 prints (24) after this ask as the mark for the whole of Q7(a): '
               'its five parts take 6 + 6 + 6 + 3 + 3. The ask itself ends at "Does the '
               'pH of water increase or decrease when base is added to it?"')

# -- Question 8, the ethene reaction scheme (paper page 9) ---------------------

A.card(8, 'a', 'i', topic='chem-2-4', concept='homologous-series-of-ethene',
       source='pdf', from_run=((1, 'a', 'i'), 10, slice(1, 2)), marks=[3],
       notation='3 of the 15 the scheme splits 3 + 6 + 6 across Q8(a)')

A.card(8, 'b', 'i', topic='chem-4-2', concept='product-of-adding-hydrogen-to-ethene',
       source='pdf', from_run=((1, 'b', 'i'), 6, slice(1, 2)), marks=[6],
       notes='X is the product of the addition printed on the scheme as "+ H2"; the '
             'other 6 of the 12 the paper prints for Q8(b) belong to part (ii).')

# -- Question 9, rate of formation of hydrogen (paper page 10) -----------------

A.card(9, 'b', 'i', topic='chem-u2', concept='graph-of-hydrogen-volume-against-time',
       source='pdf',
       from_runs=[((1, 'b', 'i'), 7, slice(1, 22)),
                  ((1, 'b', 'i'), 7, slice(23, 26)),
                  ((1, 'b', 'i'), 7, slice(27, 31)),
                  ((1, 'b', 'i'), 7, slice(32, 37)),
                  ((1, 'b', 'i'), 7, slice(49, 58))],
       marks=[3, 3, 3, 3, 3], notation='5 x 3',
       notes='The paper prints 21 for Q9(b); 15 of it is this graph and 6 is part (ii). '
             'The scheme takes 3 off if the graph is not on graph paper and accepts the '
             'axes reversed. Unlike the Question 3 graph, this one has to be a smooth '
             'curve and has to pass through the origin.')

A.card(9, 'c', topic='chem-3-2', concept='reading-rate-and-volume-from-a-graph',
       source='pdf',
       from_runs=[((1, 'c', None), 21, slice(2, 4)),
                  ((1, 'c', None), 21, slice(7, 11)),
                  ((1, 'c', None), 21, slice(25, 32))],
       marks=[3, 6, 6], notation='3 + 6 + 6',
       checked='Page 10 sets (i), (ii) and (iii) inside part (c) and prints (15) once, '
               'at the end, for all three. The lifted text therefore ends on that '
               'bracketed number; the three asks themselves are complete and in the '
               "paper's order.",
       notes='The rows answer (i), (ii) and (iii) in that order. Two of the three are '
             'ranges because they are read off the candidate\'s own graph. The scheme '
             'allows the first 3 of the 6 marks for (ii) to be earned by extrapolating '
             'from half the total volume.')

# -- Question 10, atomic structure and AdBlue (paper page 11) ------------------

# Seven blanks, one combined tariff. The parse scattered the answers across
# three addresses because the leading "4" and "6" of the fourth and sixth
# answers were read as question heads; the run is one list on scheme page 16.
A.card(10, 'a', topic='chem-1-2', concept='atomic-number-mass-number-and-atomic-models',
       source='pdf',
       from_runs=[((1, 'a', None), 10, slice(2, 3)),
                  ((1, 'a', None), 11, slice(1, 2)),
                  ((1, 'a', None), 12, slice(1, 2)),
                  ((4, None, None), 0, slice(0, 1)),
                  ((4, None, None), 1, slice(1, 2)),
                  ((6, None, None), 0, slice(0, 1)),
                  ((6, None, None), 1, slice(1, 2))],
       tariff='orderedSplit', ladder=25, notation='2 x 6 + 4 x 3 + 1',
       notes='The rows are the words for blanks 1 to 7, in the order the passage prints '
             'them. No row carries a mark of its own: the scheme prices the seven '
             'blanks as one lot, 2 x 6 + 4 x 3 + 1, and does not say which blank is '
             'worth which, so the 25 sits on the part and not on the rows.')

A.card(10, 'c', 'iii', topic='chem-1-4', concept='moles-and-volume-of-gas-at-stp',
       source='pdf',
       from_runs=[((6, 'c', 'iii'), 0, slice(2, 9)),
                  ((6, 'c', 'iii'), 0, slice(12, 15))],
       marks=[3, 4], notation='3 + 4',
       checked='Page 11 prints (25) after this ask as the mark for the whole of Q10(c) '
               '— the rubric is "Answer any two of the parts (a), (b) and (c). (2 x 25)" '
               '— and (c)(i) takes 6 and (c)(ii) 12, leaving the 7 the scheme splits 3 '
               'and 4 here. Both asks of the part are complete.',
       notes='The scheme reads the mole ratio straight off the balanced equation printed '
             'in the stem, then multiplies by the molar volume at s.t.p.; the four marks '
             'for the volume split 2 for the multiplication and 2 for the answer. A '
             'candidate who carries forward the 27 moles of urea found in part (ii) is '
             'allowed the volume that follows from it.')

# -- refused, with the reason -------------------------------------------------
#
# Each of these is an ask the paper prints and this script leaves uncarded. The
# reason is recorded here because a documented refusal is worth more than a card
# that looks right and is not.
REFUSED = [
    ('Q5(d)(ii)', 'Use a dot and cross diagram to show the arrangement of the '
                  'electrons in an O2 molecule. The scheme answers with the diagram '
                  'itself — a grid of x and O glyphs the text layer returns as "x x / '
                  'O O / x x / x x" — and its two priced points, "two bond pairs '
                  'shown" and "two lone pairs in valence shell of each oxygen shown", '
                  'are the examiner\'s checklist for that drawing, not something a '
                  'candidate writes. Contrast Q5(c)(iii), which is carded: there the '
                  'scheme prints "[Diagram not essential.]" and gives the answer in '
                  'words as an equally accepted route. Nothing of the sort is offered '
                  'here.'),
    ('Q8(a)(ii)', 'Draw the structure of an ethene molecule showing all of its atoms '
                  'and bonds. The scheme\'s whole answer for this part is "DRAW: (6)" '
                  'followed by the structure as artwork — a tariff and a picture, no '
                  'text to lift.'),
    ('Q8(b)(ii)', 'A and B are two other addition reactions of ethene. Identify the '
                  'substance added to ethene in each case. The answers are priced and '
                  'real (3 each), but A and B are arrow labels on the reaction scheme '
                  'the paper draws at the top of page 9, and the text layer returns '
                  'that scheme as loose fragments ("ethanol 1,2-dibromoethane '
                  'chloroethane", "Al2O3", "A B", "X polymer Y", "+ H2") with no '
                  'geometry. A card naming A and B needs that scheme bound as a figure '
                  'and a label key saying which arrow each letter sits on, neither of '
                  'which can be added from here. A figure pass over page 9 opens this '
                  'part.'),
    ('Q8(e)(ii)', 'Draw the structure of a benzene molecule. The scheme prints "DRAW:" '
                  'and then twelve bare H glyphs — the hydrogens of the drawn ring, '
                  'stripped of the ring — with the tariff "(6 + 5)". There is no '
                  'answer in the text layer, only the leftovers of one.'),
    ('Q11(b)(iii)', 'Supply the missing words in the following statement ... according '
                    'to __________ principle ... is observed to __________. The answer '
                    'is priced and liftable ("Le Chatelier\'s // increase", 2 x 3), and '
                    'this is refused on the question side. Page 12 sets (i) to (iv) of '
                    'Q11(b) in one block and prints the stem for (iv) — "Marine '
                    'shellfish and coral use carbonate ions ... increasing '
                    'concentration of carbonic acid in seawater." — between (iii) and '
                    '(iv). Splitting the block on part markers welds that stem onto the '
                    'tail of (iii), and it cannot be trimmed off: the statement (iii) '
                    'quotes closes on a curly quote rather than a full stop, so the '
                    'first-sentence trim runs straight past it and stops inside the '
                    'shellfish prose instead. The card would ask about Le Chatelier and '
                    'then hand the reader two sentences about shell-making that belong '
                    'to the next part. Fix the segmentation on page 12 and this part '
                    'is a clean two-row card.'),
]
for ref, why in REFUSED:
    print(f'REFUSED 2021 OL {ref}: {why}', file=sys.stderr)

A.emit()
