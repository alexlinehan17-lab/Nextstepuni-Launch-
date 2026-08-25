#!/usr/bin/env python3
"""Chemistry 2024 Higher Level — parts the deck had not carded.

Everything below the second rule was authored in a later pass over the open
asks. Two facts about this paper shape all of it.

The markdown parser finds nothing at all in this scheme: Scheme.QHEAD only
recognises the "Q3" form and the Chemistry examiners head their questions "3.",
so Scheme.parts is empty and source='md' returns no candidates for any part.
Every answer here comes from the PDF parser.

And the PDF parser's keys stop agreeing with the paper's numbering after Q8.
It interleaves the two-column pages, so the paper's Q10(c) calculation is filed
under its Q8(c)(ii) and the paper's Q9(d) under its Q8(d)(i)-(ii). Each from_run
below was found by searching every key for the answer text and then reading the
scheme page to confirm which part it answers; the citation follows the paper, as
it must.

Tariffs are read off the paper, which prices Q3(b) at 20, Q3(c) at 8, Q8(c) at
24, Q10(c) at 25 and Q11(a)/(b) at 25 each. Every split used here sums to the
printed total: 6 + 11 + 3 = 20 across Q3(b), 4 + 4 = 8 across Q3(c),
3 + 3 + 6 + 6 + 6 = 24 across Q8(c), 6 + 6 + 4 + 9 = 25 across Q10(c).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2024, 'hl')

# The scheme runs its answer on from the question it is repeating — "What can be
# concluded from your graph? rate proportional to concentration" — so the card
# takes the words after it. The "(3)" printed against the second conclusion is
# the mark for the pair; both are readings of the same graph.
A.card(3, 'b', 'iii', topic='chem-u2', concept='what-a-rate-graph-shows',
       source='pdf', from_run=((3, 'b', 'iii'), 0, slice(7, None)), marks=[3],
       checked='The paper prints the part mark "(20)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The question itself '
               'is complete: "What can be concluded from your graph?"')

A.card(5, 'b', 'vi', topic='chem-1-2', concept='shape-of-a-p-orbital',
       source='pdf', use=[0], marks=[6], first_sentence=True,
       notes='Three of the six are given for a drawing showing the two lobes overlapping.')

A.card(8, 'a', topic='chem-1-4', concept='geometry-change-during-addition',
       source='pdf', first_sentence=True,
       from_runs=[((8, 'a', None), 0, slice(12, 13)),
                  ((8, 'a', None), 3, slice(0, 1)),
                  ((8, 'a', None), 3, slice(2, 4)),
                  ((8, 'a', None), 4, slice(0, 1))],
       marks=[2, 1, 1, 1],
       notation='3 for the shape it starts as, 2 for what it becomes',
       notes='The scheme accepts trigonal or triangular for planar.')


# ── Q3, the rate-of-reaction experiment ──────────────────────────────────────
# The paper prints the whole results table in Q3's stem — concentrations, times,
# and the first two rate values already filled in — so every part of (b) and (c)
# is answerable from the card without a figure.
A.card(3, 'b', 'i', topic='chem-u2', concept='rate-values-from-reaction-times',
       source='pdf', use=[0], marks=[6], notation='6 × 1',
       notes='One mark for each of the six values. They fill the third row of the '
             'paper\'s table from left to right, from the 0.08 M run to the 0.03 M run.')

# The scheme sets its three criteria and their marks in one block, so each row is
# a slice of it and the bracketed instructions to the examiner are left out.
A.card(3, 'b', 'ii', topic='chem-u2', concept='graph-of-rate-against-concentration',
       source='pdf',
       from_runs=[((3, 'b', 'ii'), 10, slice(0, 2)),
                  ((3, 'b', 'ii'), 10, slice(3, 5)),
                  ((3, 'b', 'ii'), 10, slice(25, 29))],
       marks=[3, 6, 2], notation='3 + 6 + 2',
       notes='The scheme takes a mark off for each incorrectly plotted point, and caps '
             'the plotting marks at three if graph paper is not used.')

A.card(3, 'c', 'i', topic='chem-u2', concept='estimating-a-rate-from-the-graph',
       source='pdf', use=[0], marks=[4], notation='4 + 4 across Q3(c)',
       notes='The scheme prints the value behind an approximation sign, so a reading '
             'close to it scores: this is a value read off the candidate\'s own graph.')

# The scheme sets the working as the fraction 1 ÷ 0.003 and the numerator sits in
# a block of its own with the mark, so the text layer runs the rest together as
# "0.003 = 333 (s)" — a false equation, which no card may print. The row is the
# value the four marks are actually awarded for.
A.card(3, 'c', 'ii', topic='chem-u2', concept='time-from-an-estimated-rate',
       source='pdf', from_run=((3, 'c', 'ii'), 1, slice(2, 4)), marks=[4],
       notation='4 + 4 across Q3(c)',
       checked='The paper prints the part mark "(8)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. Page 4 of the paper '
               'shows the question is complete — "Calculate the time taken for the '
               'sulfur to precipitate in this case." — and the (8) is the mark for both '
               'romans of Q3(c) together.',
       notes='"This case" is the 0.015 M solution of part (c)(i). The scheme writes the '
             'working as a fraction whose numerator sits in a block of its own, so the '
             'card carries the value the four marks are awarded for rather than an '
             'equation the text layer has run together.')


# ── Q8(c), the elimination step of the PVC synthesis ─────────────────────────
# Both of these parts are marked 3 + 3: three for the structure drawn and three
# for the bonds marked on it. Only the second three is text the scheme prints —
# the structure comes back from the text layer as loose atom labels — so each
# card carries that row alone and says so on its face.
A.card(8, 'c', 'iii', topic='chem-4-2', concept='bonds-broken-in-an-elimination',
       source='pdf', from_run=((8, 'c', 'iii'), 8, slice(1, 14)), marks=[3],
       notation='3 for the structure drawn + 3 for the bonds indicated',
       notes='Six marks in all. The other three are for the drawn structure of X, which '
             'the scheme prints as a diagram and this card cannot show.')

A.card(8, 'c', 'iv', topic='chem-4-2', concept='bond-formed-in-an-elimination',
       source='pdf', from_run=((8, 'c', 'iv'), 4, slice(2, 10)), marks=[3],
       notation='3 for the structure drawn + 3 for the bond indicated',
       notes='Six marks in all. The other three are for the drawn structure of Y, which '
             'the scheme prints as a diagram and this card cannot show.')


# ── Q10(c)(ii), the mass of iron(III) oxide ──────────────────────────────────
# The scheme prints two routes side by side, separated by its own double solidus,
# and prices them as one column of three marks: 2 + 2 + 2. Each row here carries
# the first route, with the second as its accepts. The parser files the whole
# calculation under its own Q8(c)(ii); the citation follows the paper.
A.card(10, 'c', 'ii', topic='chem-2-3', concept='mass-of-product-from-moles-of-reactant',
       source='pdf',
       from_runs=[((8, 'c', 'ii'), 1, slice(0, 3)),
                  ((8, 'c', 'ii'), 3, slice(4, 8)),
                  ((8, 'c', 'ii'), 5, slice(4, 8)),
                  ((8, 'c', 'ii'), 5, slice(9, 17)),
                  ((8, 'c', 'ii'), 5, slice(18, 24)),
                  ((8, 'c', 'ii'), 5, slice(25, 30))],
       use=[[0, 1], [2, 3], [4, 5]], marks=[2, 2, 2], notation='2 + 2 + 2',
       notes='The accepts on each row are the scheme\'s second route, through the mass '
             'of iron that reacted rather than the moles of Fe2O3. The paper sets this '
             'part under the Q10(c) lead-in, which the block segmentation reads as a '
             'part of its own rather than as a stem, so this card carries no stem; the '
             '0.06 moles of O2 the calculation starts from is part (i)\'s own answer.')


# ── Refused, with the reason each is refused ─────────────────────────────────
REFUSED = [
    ('2024 HL Q6(c)(i)',
     '"Draw the molecular structure of methylpropane, including all atoms and bonds." '
     'The whole three-mark answer is the drawn structure. The text layer returns it as '
     'loose atom labels — "C H H H", "H H", "C C C H H H H", "H" — which is a picture '
     'taken apart, not an answer, so there is nothing here to lift.'),

    ('2024 HL Q6(c)(ii)',
     'the card would ask for isomers of a compound it never identifies. Compound C is '
     'defined by Q6(c)\'s own lead-in — "A molecule of compound A can undergo catalytic '
     'cracking to produce a molecule of methylpropane and a molecule of compound C" — '
     'which Paper files as the text of Q6(c) rather than as a stem: paper.stem(6, "c") '
     'is None and paper.stem(6) returns Q6\'s opening line, which is about A and B. '
     'card() takes its stem from exactly those two calls. Separately, 9 of the part\'s '
     '15 marks are the three drawn structures, so even with a stem the card would show '
     'only the "3 × 2" for the names.'),

    ('2024 HL Q8(c)(v)',
     '"Draw two repeating units of the polymer PVC." The whole six-mark answer is the '
     'drawn polymer; the only text the scheme prints beside it is the examiner\'s '
     'consistency instruction, "[award 3 marks two repeating units consistent with '
     'answer in part (iv)]". A card whose one row is an instruction to the examiner '
     'teaches nothing.'),

    ('2024 HL Q9(d)(i)',
     'anchored to art the deck cannot show. "What evidence is there that acid Z is a '
     'strong acid?" is answered by reading the titration curve printed beside it, and '
     'the scheme answers in those terms — "pH is close to 0 (when pure) / weak base and '
     'long vertical". Page 10 of the paper draws that curve as vector art and the '
     'figure pass did not extract it: authored/chemistry-figures.json holds no figure '
     'for the page at all. The paper\'s stem block for Q9(d) is no help either — it '
     'comes back as the graph\'s own axis numbers, "14 12 10 8 pH ... 6 4" — so the '
     'card would name an acid Z it never shows. Needs a bound figure. The tariff is '
     'legible: the scheme prints "(5 + 2 + 2)" across (d)(i) and (d)(ii) and the paper '
     'prints (9) for the pair, so (d)(i) is 5.'),
    ('2024 HL Q9(d)(ii)',
     'the same missing curve as (d)(i). The answer is "after" and the justification the '
     'scheme accepts is read straight off the graph — "vertical part of the graph ends '
     'before 10". Needs the same bound figure; the two marking points are 2 and 2.'),

    ('2024 HL Q11(a)(i)',
     '"Draw a dot and cross diagram to show the arrangement of the valence electrons in '
     'a molecule of BF3." The whole four-mark answer is the diagram. The scheme block '
     'for it holds no answer text at all, only the examiner\'s partial-credit note — '
     '"(4) [award 2 marks if lone pair electrons are omitted from F(s)]" — so there is '
     'no marking point to put on a card.'),

    ('2024 HL Q11(b)(i)',
     '"State the systematic IUPAC names for compounds A, B, C, D and E." The five '
     'compounds are structural formulae drawn in a table on page 12 of the paper, and '
     'naming them is the whole question. authored/chemistry-figures.json holds no '
     'figure for page 12, and the paper\'s stem for Q11(b) comes back as two stray '
     'characters from inside one of the structures, "O H". This needs a bound figure '
     'and a decoded label key for A to E before it can be carded; the scheme does print '
     'the five names, priced 5 × 3.'),
]
for ref, why in REFUSED:
    print(f'  REFUSED {ref}: {why}', file=sys.stderr)

A.emit()
