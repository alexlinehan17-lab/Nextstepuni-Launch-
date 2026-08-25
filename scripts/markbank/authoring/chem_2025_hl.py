#!/usr/bin/env python3
"""Chemistry 2025 Higher Level — the parts the deck had not carded.

Three facts about this paper shape every call below.

The markdown parser finds nothing at all in this scheme. Scheme.QHEAD only
recognises the "Q3" form and the Chemistry examiners head their questions "3.",
so Scheme.parts is empty and source='md' returns no candidates for any part of
the paper. Every answer here comes from the PDF parser.

The PDF parser's keys do not agree with the paper's numbering. It reads the
scheme's pages out of order and merges questions that share a letter, so:

    paper Q6      -> its key Q16   (Q16 is a bucket holding Q5, Q6 and Q7)
    paper Q10     -> its key Q9    (Q9 is a bucket holding Q9, Q10 and Q11)
    paper Q11     -> its key Q9    (same bucket, different point indices)

Each from_run below was found by searching every key for the answer text and
then reading the scheme page that prints it, to confirm which part it answers.
The citation follows the PAPER, as it must.

And the examiners set every calculation as a stacked fraction. The text layer
returns the numerator in one block and the denominator glued to the rest of the
line, so "55 over 110 = 0.5" comes back as "110 = 0.5 (moles of NOBr)" — a false
equation, which no card may print. Where that happens the row carries the value
the marks are actually awarded for and the note says so.

Tariffs are read off the paper, which prices Q1(e) at 15, Q2(b) at 21, Q3(a) at
18, Q3(b) at 15, Q6(a) at 24, Q9(b) at 24, Q10(b) at 25, Q10(c) at 25 and
Q11(b) at 25. Every split used here is the scheme's own printed one and sums
inside the printed total: 3 + 4 + 4 + 4 = 15 across Q1(e), 12 + 6 = 18 across
Q3(a), 3 + 6 + 6 = 15 across Q3(b), 3 + 9 + 6 + 3 + 3 = 24 across Q6(a),
4 + 4 + 6 + 10 = 24 across Q9(b), 18 + 2 + 5 = 25 across Q10(c).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2025, 'hl')


# ── Q1(e)(iv), the last step of the iron-tablet titration ────────────────────
# The scheme prints two routes side by side — the mass of iron over the mass of
# one tablet, and the mass of iron in all six over 2.496 — each as a stacked
# fraction. The numerators sit in blocks of their own, so the surviving text
# begins at the ratio the division produced. That ratio and what is done to it
# is the whole of the four-mark answer.
A.card(1, 'e', 'iv', topic='chem-4-1', concept='percentage-by-mass-of-iron-in-a-tablet',
       source='pdf', from_run=((1, 'e', 'iv'), 1, slice(2, 8)), marks=[4],
       checked='The paper prints the part mark "(15)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. Page 2 of the paper '
               'shows the question is complete — "Calculate the percentage by mass of '
               'iron(II) in one tablet." — and the (15) is the mark for the whole of '
               'Q1(e), whose four romans are priced 3 + 4 + 4 + 4.',
       notes='The scheme writes the first step as a stacked fraction whose numerator '
             'sits in a block of its own, so the row starts at the ratio it produced. '
             'The scheme adds "[Allow 3 marks for 0.2524]", so stopping before the '
             'conversion to a percentage still scores three of the four.')


# ── Q2(b)(i), the liquid-liquid extraction of eugenol ────────────────────────
# The scheme lists three acceptable elements and pays for any two of them,
# "[any two] (6 + 3)". The middle one comes back from the text layer with the
# scheme's own alternative marker glued to its first word — "//organic layer
# over an aqueous layer" — so it is named in the note rather than shown as a row
# with a stray separator on its face.
A.card(2, 'b', 'i', topic='chem-u2', concept='liquid-liquid-extraction-procedure',
       source='pdf',
       from_runs=[((2, 'b', 'i'), 0, slice(0, 2)),
                  ((2, 'b', 'i'), 0, slice(9, 18))],
       marks=[6, 3], notation='6 + 3 for any two of the three the scheme lists',
       notes='The third answer the scheme accepts is the organic layer shown lying over '
             'an aqueous layer; the text layer glues the scheme\'s "//" separator to it, '
             'so it is not set as a row here. The scheme also prints "[maximum of 6 '
             'marks awarded if diagram not included]", so the labelled diagram the '
             'question asks for is worth three of the nine on its own.')


# ── Q3, the rate at which hydrogen peroxide gives off oxygen ─────────────────
# The paper prints the whole results table in Q3's stem, so both graph parts are
# answerable from the card without a figure. The scheme sets its plotting
# criteria and their marks in one block, so each row is a slice of it and the
# bracketed instruction to the examiner is left out of the rows.
A.card(3, 'a', 'i', topic='chem-u2', concept='plotting-a-volume-time-graph',
       source='pdf',
       from_runs=[((3, 'a', 'i'), 11, slice(0, 2)),
                  ((3, 'a', 'i'), 11, slice(3, 5)),
                  ((3, 'a', 'i'), 11, slice(21, 25))],
       marks=[3, 7, 2], notation='3 + (7 × 1) + 2',
       notes='One mark for each of the seven points in the paper\'s table. The scheme '
             'caps the plotting marks at three if graph paper is not used.')

A.card(3, 'a', 'ii', topic='chem-3-2', concept='instantaneous-rate-from-a-tangent',
       source='pdf',
       from_runs=[((3, 'a', 'ii'), 0, slice(0, 6)),
                  ((3, 'a', 'ii'), 0, slice(7, 11))],
       marks=[3, 3], notation='3 for the tangent + 3 for the value',
       checked='The paper prints the part mark "(18)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. Page 4 of the paper '
               'shows the question is complete — "Use your graph to find the '
               'instantaneous rate of production of oxygen at 2.5 minutes." — and the '
               '(18) is the mark for Q3(a)(i) and (a)(ii) together.',
       notes='The scheme prints the value behind an approximation sign, so a reading '
             'close to it scores: it is read off the candidate\'s own graph.')

A.card(3, 'b', 'i', topic='chem-3-2', concept='average-rate-from-a-graph',
       source='pdf', use=[0], marks=[3], notation='3 of the 15 marks for Q3(b)',
       notes='Again an approximation sign, because the value is read off the '
             'candidate\'s own graph rather than calculated from the table.')


# ── Q6(a)(ii), the fractionating column ──────────────────────────────────────
# The PDF parser files this under its own Q16(a)(ii); the citation follows the
# paper. The scheme sets all three criteria in one block at (3) each.
#
# No stem: paper.stem(6, 'a') returns "Some fractions undergo further chemical
# processing in order to make them more useful.", which the paper prints between
# (a)(iii) and (a)(iv) and which belongs to those parts, not to this one.
A.card(6, 'a', 'ii', topic='chem-2-4', concept='fractional-distillation-of-crude-oil',
       source='pdf', stem=False,
       from_runs=[((16, 'a', 'ii'), 1, slice(0, 8)),
                  ((16, 'a', 'ii'), 1, slice(9, 17)),
                  ((16, 'a', 'ii'), 1, slice(18, 31))],
       marks=[3, 3, 3], notation='3 + 3 + 3',
       notes='The scheme adds "[maximum of 6 marks awarded if diagram not included]", '
             'so the labelled diagram the question asks for is worth three of the nine '
             'on its own. The card carries no stem: the paper prints Q6(a)\'s lead-in '
             'above (a)(i), and the only prose Paper attaches to Q6(a) is the sentence '
             'printed between (a)(iii) and (a)(iv), which is about a different part.')


# ── Q9(b), the nitrosyl bromide equilibrium ──────────────────────────────────
# The paper prints the masses and the container volume in a lead-in above
# (b)(i) — "When 55 g of nitrosyl bromide were sealed into a 2 litre closed
# container, 78% of the nitrosyl bromide had decomposed at equilibrium at
# temperature T." — which Paper files as neither a part nor a stem:
# paper.stem(9, 'b') is None, so these cards carry Q9's opening statement as
# their stem and say in the note where the figures came from.
LEAD_IN = ('The paper prints the mass sealed in, the volume of the container and the '
           'percentage decomposed in a lead-in above Q9(b)(i), which the block '
           'segmentation attaches to no part, so this card\'s stem is Q9\'s opening '
           'statement rather than that lead-in.')

# "55 over 110" is a stacked fraction whose numerator sits in the block above, so
# the text layer runs the rest together as "110 = 0.5 (moles of NOBr)" — a false
# equation. The second row is the value the second two marks are awarded for.
A.card(9, 'b', 'i', topic='chem-3-3', concept='initial-moles-of-nitrosyl-bromide',
       source='pdf',
       from_runs=[((9, 'b', 'i'), 0, slice(0, 3)),
                  ((9, 'b', 'i'), 1, slice(2, 6))],
       marks=[2, 2], notation='2 + 2',
       notes=LEAD_IN + ' The scheme writes the division as a stacked fraction whose '
             'numerator sits in a block of its own, so the second row carries the '
             'value the two marks are awarded for rather than an equation the text '
             'layer has run together.')

A.card(9, 'b', 'ii', topic='chem-3-3', concept='moles-remaining-at-equilibrium',
       source='pdf',
       from_runs=[((9, 'b', 'ii'), 0, slice(0, 7)),
                  ((9, 'b', 'ii'), 0, slice(8, 18))],
       marks=[2, 2], notation='2 + 2', notes=LEAD_IN)

# The fourth row is the Kc value. The substitution above it is a stacked fraction
# — the numerator "(0.195)2 (0.0975)" in one block, the denominator "(0.055)2" in
# the next — so the row carries the value the three marks are awarded for.
A.card(9, 'b', 'iv', topic='chem-3-3', concept='calculating-kc-from-equilibrium-moles',
       source='pdf',
       from_runs=[((9, 'b', 'iv'), 0, slice(0, 4)),
                  ((9, 'b', 'iv'), 0, slice(5, 9)),
                  ((9, 'b', 'iv'), 0, slice(10, 28)),
                  ((9, 'b', 'iv'), 2, slice(2, 5))],
       marks=[2, 2, 3, 3], notation='2 + 2 + 3 + 3',
       checked='The paper prints the part mark "(24)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. Page 10 of the '
               'paper shows the question is complete — "Calculate the value of Kc for '
               'the equilibrium at temperature T." — and the (24) is the mark for the '
               'four romans of Q9(b) together.',
       notes=LEAD_IN + ' The scheme writes the substitution into the Kc expression as '
             'a stacked fraction split across two blocks, so the last row carries the '
             'value the final three marks are awarded for rather than the broken '
             'equation the text layer returns.')


# ── Q10(b)(ii) and Q10(c), filed by the parser under its Q9 ──────────────────
# The paper's Q10 asks two of its three parts to be answered; the parser
# interleaves it with Q9 and Q11, so every from_run below names a Q9 key. The
# citation follows the paper.
#
# (b)(i) draws the ethene molecule and (b)(ii) marks a bond on that drawing. The
# drawing is not liftable, but which bond breaks is: the scheme says so in words.
A.card(10, 'b', 'ii', topic='chem-4-2', concept='bond-broken-in-ethene-addition',
       source='pdf', from_run=((9, 'b', 'ii'), 1, slice(0, None)), marks=[3],
       notes='Part (b)(i) asks for the structure of ethene to be drawn and this part '
             'marks a bond on that drawing, so the card shows what the three marks are '
             'awarded for rather than the drawing itself.')

# Q10(c) has no stem at all: paper.stem(10, 'c') and paper.stem(10) are both
# None, because the paper prints the tablet's composition and the two balanced
# equations in a lead-in the block segmentation attaches to no part.
NO_STEM = ('The paper prints the two balanced equations and the mass of each acid in '
           'the tablet in a lead-in above Q10(c)(i) which the block segmentation '
           'attaches to no part, so this card carries no stem.')

# Nine steps is not one card. Split where the calculation itself does: the
# three relative molecular masses and the citric-acid route, then the tartaric
# route and the total. Every marking point is the scheme's own; only the
# citation gains an item so each half has its own address.
A.card(10, 'c', 'i', card_id='chem-2025-hl-q10-c-i-mr', topic='chem-1-4',
       concept='relative-molecular-masses-and-moles-of-citric-acid',
       source='pdf',
       from_runs=[((9, 'c', 'i'), 1, slice(0, 4)),
                  ((9, 'c', 'i'), 1, slice(5, 9)),
                  ((9, 'c', 'i'), 1, slice(10, 14)),
                  ((9, 'c', 'i'), 3, slice(2, 6)),
                  ((9, 'c', 'i'), 3, slice(7, 15))],
       marks=[2, 2, 2, 2, 2], notation='9 × 2 (first five)',
       notes=NO_STEM + ' The scheme sets each moles-from-mass step as a stacked '
             'fraction whose numerator sits in a block of its own, so the fourth '
             'row carries the value the mark is awarded for rather than an '
             'equation the text layer has run together. Split from the tartaric '
             'route and the total, which the paper prices in the same nine.')

A.card(10, 'c', 'i', card_id='chem-2025-hl-q10-c-i-total', topic='chem-1-4',
       concept='total-mass-of-sodium-hydrogencarbonate-required',
       source='pdf',
       from_runs=[((9, 'c', 'i'), 5, slice(2, 6)),
                  ((9, 'c', 'i'), 5, slice(7, 15)),
                  ((9, 'c', 'i'), 6, slice(0, 9)),
                  ((9, 'c', 'i'), 6, slice(10, 17))],
       marks=[2, 2, 2, 2], notation='9 × 2 (final four)',
       notes=NO_STEM + ' The tartaric-acid route and the total, split from the '
             'first five of the same nine two-mark steps.')

A.card(10, 'c', 'ii', topic='chem-2-3',
       concept='volume-of-gas-at-room-temperature-and-pressure',
       source='pdf', from_run=((9, 'c', 'ii'), 1, slice(0, None)), marks=[2],
       notes=NO_STEM + ' The 0.0035 moles the calculation starts from is part (c)(i)\'s '
             'own answer, and the scheme takes the molar volume at room temperature '
             'and pressure from the data book.')


# ── Q11(b)(iii), the moles of acid in the heat-of-reaction experiment ────────
# "80 over 1000" is a stacked fraction whose numerator sits in a block of its
# own, so the text layer returns "1000 = 0.08 (moles)". The row is the value all
# six marks are awarded for. Parser key Q9(b)(iii); the citation is the paper's.
#
# No stem: paper.stem(11, 'b') comes back as the page furniture "(25) This
# question continues on the next page." The question names its own volume and
# concentration, so nothing is lost by leaving it off.
A.card(11, 'b', 'iii', topic='chem-1-4', concept='moles-from-volume-and-molarity',
       source='pdf', stem=False,
       from_run=((9, 'b', 'iii'), 6, slice(2, 4)), marks=[6],
       notes='The scheme writes the working as a stacked fraction whose numerator sits '
             'in a block of its own, so the row carries the value the six marks are '
             'awarded for rather than an equation the text layer has run together. The '
             'card has no stem because the paper\'s stem block for Q11(b) comes back as '
             'the page furniture "(25) This question continues on the next page.", and '
             'the question names its own volume and concentration.')


# ── Refused, with the reason each is refused ─────────────────────────────────
REFUSED = [
    ('2025 HL Q2(c)(ii)',
     '"Draw the structure of a molecule of eugenol." The whole six-mark answer is the '
     'drawn structure. The scheme block holds the question cue and the tariff "(6)" and '
     'nothing else, so there is no marking point to put on a card.'),

    ('2025 HL Q4(g)',
     '"Draw the molecular structure of two isomers of C4H10, including all atoms and '
     'bonds." The scheme\'s entire answer is "// (2 × 3)" — its own alternative '
     'separator between two drawn structures, and the tariff. Nothing to lift.'),

    ('2025 HL Q5(b)(ii)',
     '"Draw the shape of the atomic orbital of lowest energy in a bromine atom in its '
     'ground state." The whole three-mark answer is the drawn s-orbital; the scheme '
     'block holds only "(3)".'),

    ('2025 HL Q7(d)(ii)',
     'the paper text cannot be recovered. The question is set beside the pH curve and '
     'the block segmentation welds the graph\'s axis numbers and label onto it: the '
     'text comes back as "Would the indicator HA be a suitable choice of indicator for '
     'the titration? Justify your answer. (10) 6 4 2 0 0 10 20 30 40 50 60 Volume of '
     'strong base added (cm3)". first_sentence would trim it to the first question '
     'mark, which drops "Justify your answer." — and the justification is half the '
     'tariff, since the scheme prices this "yes (2)" plus the reason (2). A card that '
     'pays four marks for a question it only half prints is worse than no card. Needs '
     'the pH-curve figure bound, which would also anchor the scheme\'s answer, "(pH '
     'range of indicator) coincides with vertical portion of the curve".'),

    ('2025 HL Q8(a)(i)',
     'the answer is a letter on a diagram. "Identify a reaction (A to C) in the scheme '
     'above that is: (i) a substitution reaction" is answered "C (2)", and A, B and C '
     'are arrows on the reaction scheme printed above the question. This needs a bound '
     'figure and a decoded label key for A to C before it can be carded — neither of '
     'which this pass can add. The paper also runs the three romans into one block, so '
     'the text for (i) comes back as "a substitution reaction, (ii) an oxidation '
     'reaction, (iii) a reduction reaction. (6)". The tariff is legible: 2 each.'),

    ('2025 HL Q8(c)(i)',
     '"Draw the structure of a molecule of ethyl ethanoate, showing all atoms and '
     'bonds." The whole five-mark answer is the drawn structure; the scheme block holds '
     'the question cue and "(5)".'),

    ('2025 HL Q8(c)(ii)',
     '"Indicate clearly on your diagram the position of the O* atom in ethyl '
     'ethanoate." The answer is a mark made on the candidate\'s own drawing from '
     '(c)(i); the scheme block holds the question cue and "(3)" and says nothing about '
     'where the atom goes.'),

    ('2025 HL Q8(c)(iii)',
     '"Indicate clearly on your diagram the bond that was formed during the formation '
     'of ethyl ethanoate." Same shape as (c)(ii): the scheme block holds the question '
     'cue and "(3) In a single molecule of ethyl ethanoate:", which is the cue for the '
     'next part, and names no bond.'),

    ('2025 HL Q10(a)(ii)',
     '"Draw a dot and cross diagram to show the arrangement of all the valence '
     'electrons in a molecule of NF3." The whole three-mark answer is the diagram; the '
     'scheme block holds only "(3)".'),

    ('2025 HL Q10(a)(iv)',
     '"Draw a diagram to show how intermolecular forces arise between two molecules of '
     'NF3 in the liquid state." The whole three-mark answer is the diagram; the scheme '
     'block holds the question cue and "(3)".'),

    ('2025 HL Q10(b)(i)',
     '"Draw the structure of a molecule of ethene, showing all atoms and bonds." The '
     'whole four-mark answer is the drawn structure; the scheme block holds the '
     'question cue and "(4)".'),

    ('2025 HL Q10(b)(iv)',
     '"Draw the structure of the intermediate ionic species formed during the above '
     'reaction." The whole three-mark answer is the drawn carbocation; the scheme block '
     'holds the rest of the question — "Your diagram should include all atoms, bonds '
     'and relevant charges." — and "(3)".'),

    ('2025 HL Q10(c)(iii)',
     'the answer\'s powers of ten do not survive the text layer. The scheme prints '
     '"0.0005 x 3 (2)" and then Avogadro\'s constant and the result as superscripts, '
     'which come back flattened: the block reads "0.0015 x 6 x 1023 = 9 x 1020 (H2O '
     'molecules) (3)". Lifted verbatim that row is numerically false, and repairing it '
     'means typing the exponents, which is writing the answer rather than lifting it. '
     'The first step alone is 2 of the 5 marks, which would misprice the card.'),
]
for ref, why in REFUSED:
    print(f'  REFUSED {ref}: {why}', file=sys.stderr)

A.emit()
