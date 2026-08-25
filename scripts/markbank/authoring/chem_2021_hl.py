#!/usr/bin/env python3
"""Chemistry 2021 Higher Level — parts the deck had not carded.

Every answer below comes from the PDF parser, because the markdown one finds
nothing at all in this scheme: it heads a question "QUESTION 6" and the markdown
parser only recognises the "Q6" form, so Scheme.parts is empty for this paper and
source='md' returns no candidates for any part.

The PDF parser's keys do not agree with the paper's numbering either. It reads
the scheme's blocks in page order and files every part under the FIRST question
head it saw, so the whole paper's (a)(i) answers pile up under its Q4(a)(i), the
(b)(ii) answers under its Q4(b)(ii), and so on — Questions 8 to 11 have no keys
of their own at all. Each from_run below was found by searching every key for the
answer text and then reading the scheme page to confirm which part it answers;
the citation follows the paper, as it must.

Marks are the scheme's throughout. Where a part's tariff is printed once against
several answers ("ANY TWO: (2 × 3)") the shape is written into the notation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2021, 'hl')

# ── Question 6: crude oil ───────────────────────────────────────────────────
# Q6(b) is priced (18) in total: (i) 2 × 3, (ii) (3) + ANY TWO: (2 × 3), (iii) 3.
#
# The scheme sets (ii) in a single block that opens with the examiner's cue, and
# the cue strip cuts at the first full stop — which lands inside "b.p." — so the
# first two of the three interchangeable ways of stating the opening 3-mark point
# come back truncated. The third comes back whole and is what row 1 carries.
A.card(6, 'b', 'ii', topic='chem-2-4', concept='how-crude-oil-is-fractionally-distilled',
       source='pdf',
       from_runs=[((4, 'b', 'ii'), 2, slice(0, 10)),
                  ((4, 'b', 'ii'), 2, slice(11, 22)),
                  ((4, 'b', 'ii'), 2, slice(23, 29)),
                  ((4, 'b', 'ii'), 2, slice(30, 40))],
       use=[0, 1, [2, 3]], marks=[3, 3, 3], notation='(3) + ANY TWO: (2 × 3)',
       notes='A diagram question the scheme answers in words — "Points of information '
             'can be taken from labelled diagram", and an answer with no diagram at all '
             'loses 3. The scheme prints three interchangeable wordings of the opening '
             '3-mark point; the block segmentation truncates two of them, so row 1 is '
             'the one that comes back whole. Rows 2 and 3 are the column itself, of '
             'which any two of the scheme\'s three score, which is why row 3 carries '
             'the third as an accepted alternative.')

A.card(6, 'b', 'iii', topic='chem-2-4',
       concept='where-the-fractions-separate-in-the-column', source='pdf',
       from_run=((4, 'b', 'iii'), 1, slice(1, 8)), marks=[3],
       checked='Page 8 of the paper prints this part complete — "Show on your diagram '
               'where the refinery gas and gas oil fractions separate." — and then part '
               '(b)\'s own tariff "(18)" on the same line, so the block ends on a '
               'bracketed number rather than punctuation.',
       notes='The scheme states the answer as a relative position on the candidate\'s '
             'own part (ii) diagram: "refinery gas (LPG) above gas oil (diesel) shown in '
             'part (ii) diagram". The card carries the placement itself.')

# ── Question 10(a): electron pair repulsion ─────────────────────────────────
# Q10(a) is priced (25): (i) 4 + 3, (ii) 3, (iii) 2 × 3, (iv) 3, (v) 6.
A.card(10, 'a', 'i', topic='chem-2-2', concept='dot-and-cross-diagram-of-ammonia',
       source='pdf',
       from_runs=[((4, 'a', 'i'), 6, slice(1, 5)),
                  ((4, 'a', 'i'), 6, slice(6, 10))],
       ladder=7, tariff='orderedSplit', notation='(4 + 3)',
       notes='A drawing question the scheme answers in words: the two things the dot '
             'and cross diagram has to show. The tariff is printed once as "(4 + 3)" '
             'across the pair, so neither point has a mark of its own and the rows '
             'carry none; totalMarks is the 7 the two are worth together. The scheme '
             'prints a worked diagram beside them, which is artwork the text layer does '
             'not carry — these two points are the whole of what it says in words.')

A.card(10, 'a', 'v', topic='chem-2-2',
       concept='bond-angle-evidence-for-repulsion-strength', source='pdf',
       from_runs=[((4, 'a', 'v'), 0, slice(1, None)),
                  ((4, 'a', 'v'), 1, slice(0, None))],
       use=[[0, 1]], marks=[6],
       checked='Page 11 of the paper prints this part complete, ending in its question '
               'mark — "...lone-pair bond-pair (lp bp) repulsions?" — and then part '
               '(a)\'s own tariff "(25)" on the same line, so the block ends on a '
               'bracketed number rather than punctuation.',
       notes='The paper prints a four-row table (Formula | Boiling point | Bond angle | '
             'Shape) beside parts (i) to (iv), and this part reads its bond-angle '
             'column. No figure is bound: the only crop of that table in the figure '
             'manifest, chemistry-2021-HL-paper-p11-i0, is recorded there as keeping '
             'the header and the CH4 row alone, so a figure pass has to re-crop it. '
             'Both of the scheme\'s two accepted wordings state the comparison in full, '
             'and the second gives the two angles, so the answer stands without it.')

# ── Question 10(b): rate of reaction ────────────────────────────────────────
# Q10(b) is priced (25): (i) 6, (ii) 4 × 3, (iii) 4 + 3.
A.card(10, 'b', 'ii', topic='chem-3-2', concept='plotting-two-concentration-time-curves',
       source='pdf',
       from_runs=[((4, 'b', 'ii'), 5, slice(1, 12)),
                  ((4, 'b', 'ii'), 6, slice(0, 7)),
                  ((4, 'b', 'ii'), 6, slice(8, 15)),
                  ((4, 'b', 'ii'), 6, slice(25, 36))],
       marks=[3, 3, 3, 3], notation='(4 × 3)',
       notes='The four things the graph is marked on, in the scheme\'s own order. The '
             'scheme adds that the marks are not available if the points are joined by '
             'straight lines, that a time-versus-concentration graph is equally '
             'acceptable, that each of the first three badly plotted points costs 1, '
             'and that 6 comes off for using different scales for the two curves, for '
             'not using graph paper, for putting the curves on different sheets, or for '
             'setting them side by side with separate axes on the one sheet.')

A.card(10, 'b', 'iii', topic='chem-3-2',
       concept='instantaneous-rate-from-the-slope-of-a-tangent', source='pdf',
       from_run=((4, 'b', 'iii'), 4, slice(13, 25)), marks=[3],
       checked='Page 11 of the paper prints this part complete — "Find the instantaneous '
               'rate of HCl formation (in M s–1) at 120 s." — and then part (b)\'s own '
               'tariff "(25)" on the same line, so the block ends on a bracketed number '
               'rather than punctuation.',
       notes='The part is worth 7; the card carries 3 of them. The scheme\'s other 4 '
             'marks are the point "good tangent drawn to either curve at 120 s", which '
             'opens the examiner\'s cue block and is cut away with it by the cue strip, '
             'so it cannot be lifted as a row. The 3 marks here are for reading the '
             'slope off that tangent, and the scheme prints the accepted range beside '
             'the value.')

# ── Question 11(a): ethene ──────────────────────────────────────────────────
# Q11(a) is priced (25): (i) 4, (ii) ANY THREE: 3 × 3, (iii) 6, (iv) 2 × 3.
#
# The paper sets parts (ii) and (iii) above the gas-solubility apparatus drawn
# for part (iv), and the block segmentation offers that drawing's labels — "push
# plunger slowly empty syringe syringe full of ethene water or cyclohexane" — as
# the stem, so both cards are left without one.
A.card(11, 'a', 'ii', topic='chem-u2', concept='apparatus-to-prepare-and-collect-ethene',
       source='pdf',
       from_runs=[((4, 'a', 'ii'), 25, slice(1, 9)),
                  ((4, 'a', 'ii'), 25, slice(10, 18)),
                  ((4, 'a', 'ii'), 25, slice(19, 29)),
                  ((4, 'a', 'ii'), 25, slice(30, 41))],
       use=[0, 1, 2], marks=[3, 3, 3], spread=True, stem=False,
       notation='ANY THREE: (3 × 3)',
       notes='A drawing question the scheme answers in words: four features of the '
             'apparatus, any three of which score 3 each, so every row carries the '
             'fourth as an accepted alternative. The scheme also requires a diagram '
             'with at least one chemical or item of apparatus labelled, and takes 3 off '
             'an unlabelled one. The paper prints the gas-solubility drawing for part '
             '(iv) directly under this part, so the card carries no stem.')

A.card(11, 'a', 'iii', topic='chem-4-2', concept='organic-product-of-ethene-with-bromine',
       source='pdf',
       from_runs=[((4, 'a', 'iii'), 15, slice(0, None)),
                  ((4, 'a', 'iii'), 16, slice(0, None)),
                  ((4, 'a', 'iii'), 22, slice(0, None))],
       use=[[0, 1, 2]], marks=[6], stem=False,
       notes='The scheme draws three structures and prints the condensed formula beside '
             'each; any one scores the 6. The drawings themselves are artwork the text '
             'layer does not carry, but the formulae do carry the answer, so the rows '
             'are the formulae. The scheme rules out 1,1-dibromoethane and '
             '1-bromoethanol. The paper prints the gas-solubility drawing for part (iv) '
             'directly under this part, so the card carries no stem.')


# -- refused, with the reason -------------------------------------------------
#
# Each of these is an ask the paper prints and this script leaves uncarded. The
# reason is recorded here because a documented refusal is worth more than a card
# that looks right and is not.
REFUSED = [
    ('Q6(d)',
     'Two things stop it. First, the paper sets the part over three blocks — the '
     'heat of combustion, then the balanced equation, then "Use this heat of '
     'reaction and the heats of formation ... to calculate the heat of formation '
     'of ethanethiol." — and the block segmentation hands Paper.text() the first '
     'of those and files the instruction itself in the stem, so the card\'s '
     'question text would be a statement of data and not the ask. There is no way '
     'to say so from here: card() takes its question text from the paper and '
     'nothing else, which is the point of it. Second, the id chem-2021-hl-q6-d is '
     'already held by a hand-authored card in scripts/markbank/authored/'
     'chemistry.json (it does not ship — its rows are re-typed equations that do '
     'not trace), and merge.py refuses a script id that collides with a '
     'hand-authored one unless it is listed in adopted-ids.json, which is not this '
     'file\'s to edit.'),
    ('Q8(b)(ii)',
     '"Draw an expanded molecular structure for Y, indicating clearly which of its '
     'bonds are formed when Z is reduced." The scheme prices the drawing at (3) '
     'and sets it as a picture with no text layer at all; only the INDICATE half — '
     '"OH bond // CH bond of carbon to which OH is attached", 2 × 3 — is in words. '
     'Worse, what Y and Z are is stated only by the reaction scheme printed at the '
     'head of Question 8, which is an image: its text comes back as the unordered '
     'run "H2O H2 Ni CH3CHCH2 CH3CH(OH)CH3 Z Y X", so no stem this script can lift '
     'says which compound is which, and the two liftable marking points would '
     'float free of the molecule they describe. This one needs the reaction scheme '
     'bound as a figure with its labels decoded, which a figure pass has to do.'),
    ('Q9(c)(ii)',
     '"Calculate the value of Kc under these conditions." The conditions are the '
     'quantities the paper sets in part (c)\'s own opening block — 9.0 moles '
     'nitrogen, 27.0 moles hydrogen, a 10.0 litre container, 6.0 moles ammonia at '
     'equilibrium — and Paper.stem(9, "c") does not hold it; the fallback is the '
     'stem of Question 9 as a whole, which is the equation, the graph description '
     'and the graph\'s pressure labels. A card asking for a calculation whose data '
     'it does not carry cannot be answered. The scheme is no help either: it sets '
     'the answer as the fraction 25/243 split across two blocks and every line of '
     'working in the mangled-glyph font, so the only thing that lifts cleanly is '
     'the bare decimal, worth 12 on its own. The id chem-2021-hl-q9-c-ii is also '
     'already held by a hand-authored card in the authored file, and merge.py '
     'refuses a collision.'),
]
for ref, why in REFUSED:
    print(f'REFUSED 2021 HL {ref}: {why}', file=sys.stderr)

A.emit()
