#!/usr/bin/env python3
"""Chemistry 2023 Ordinary Level — parts the deck had not carded.

Two facts about this paper's scheme shape everything below.

First, the markdown parser finds NOTHING in it: Scheme.parts is empty for
2023 OL, because the examiners head each answer block "QUESTION 8" and the
markdown grammar only recognises the "Q8" form. Every card here therefore
reads source='pdf'.

Second, the PDF parser's keys do not agree with the paper's numbering and
never could. The scheme sets the whole paper as two-column tables, so the
block parser files answers by COLUMN POSITION rather than by question: the
answer to Q9(b)(i) sits under its key (4, 'b', 'i') and the answer to
Q1(c)(i) under (7, 'c', 'i'). Each from_run below was found by searching
every key for the answer text and then reading the scheme page to confirm
which part it answers; the citation follows the paper, as law 3 requires.

Marks are not guessed anywhere. This scheme prints one combined tariff per
part — "(6 + 6 + 3 + 3)" against Q1(c), "(8 + 3)" against Q3(a)(i) — and its
own preamble (point 4) says a double solidus separates points for which
SEPARATE marks are allocated. Where the count of //-separated points equals
the count of numbers in the tariff, the split is read off in order and then
checked against the total the PAPER prints. Every card below closes that
check; the one part where it cannot close — Q3(a)(ii), six separately-marked
points against two numbers — is refused rather than priced by guess, and the
refusals are all set out at the foot of the file.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author, Refused  # noqa: E402

A = Author('chemistry', 2023, 'ol')


def card(*args, **kw):
    """Card it, or print why not and carry on.

    A refusal is the point of the exercise, not a failure of it: the parts
    this paper leaves uncardable are uncardable for reasons a later figure
    pass can act on, and they are worth more written down than guessed at.
    """
    try:
        return A.card(*args, **kw)
    except Refused as exc:
        print(f'REFUSED {exc}', file=sys.stderr)


# ── Q1(c)(i) ───────────────────────────────────────────────────────────────
# A drawing question the scheme answers in text. Its whole answer is the
# structural formula "H–C≡C–H", printed on a line of its own, which the text
# layer carries intact — so this is a liftable structure, not a picture.
# Q1(c) is priced (6 + 6 + 3 + 3) over four //-separated points: the drawing,
# the explanation at (ii), and the two halves of (iii). The deck's shipped
# cards for (ii) and (iii) carry 6 and 3 + 3, which leaves 6 here, and the
# paper prints (18) against Q1(c) — 6 + 6 + 3 + 3.
card(1, 'c', 'i', topic='chem-2-4', concept='structure-of-the-ethyne-molecule',
     source='pdf', from_run=((7, 'c', 'i'), 1, slice(0, None)), marks=[6],
     notation='6 + 6 + 3 + 3 across Q1(c)', stem=False,
     notes='The scheme prints the answer as the structural formula on its own line, '
           'directly under its "DRAW:" cue. The triple bond is what "showing all of '
           'its bonds" is asking for. The paper sets this part under a diagram of the '
           'ethyne generator whose labels the block segmentation reads as the question '
           'stem, so the card carries no stem.')

# ── Q2(d)(ii) ──────────────────────────────────────────────────────────────
# The scheme states the averaged titre twice: as the answer ("22.45 cm3") and
# as the arithmetic that produces it. The arithmetic is the row, because it
# shows which two of the three printed titrations count — the rough one is
# left out — and the bare value rides as the accepted alternative.
card(2, 'd', 'ii', topic='chem-4-1', concept='average-titre-from-the-accurate-titrations',
     source='pdf',
     from_runs=[((7, 'd', 'iii'), 6, slice(0, None)),
                ((7, 'd', 'ii'), 2, slice(1, None))],
     use=[[0, 1]], marks=[3],
     notes='Q2(d) is priced (3 + 3 + 9) and the paper prints (15) against it. The '
           'rough titration is excluded from the average: only the two accurate '
           'titres are used. The card\'s stem is the paper\'s own table of titres.')

# ── Q2(d)(iii) ─────────────────────────────────────────────────────────────
# Priced (9) by the scheme and worked in three steps of 3. The rows are those
# three steps as the scheme prints them.
card(2, 'd', 'iii', topic='chem-4-1', concept='concentration-of-hcl-from-the-titration',
     source='pdf',
     from_runs=[((7, 'd', 'iii'), 10, slice(2, -1)),
                ((7, 'd', 'iii'), 12, slice(0, -1)),
                ((7, 'd', 'iii'), 17, slice(2, None))],
     marks=[3, 3, 3], notation='3 + 3 + 3',
     checked='The paper prints part (d)\'s tariff "(15)" immediately after this, the '
             'last of its three sub-parts, so the block does not end on punctuation. '
             'Page 3 of the paper shows the question is complete as it stands: '
             '"Calculate the concentration, in moles per litre, of the HCl solution."',
     notes='The scheme sets each step of the working as a fraction, so the flattened '
           'text splits a numerator from its denominator. Row 1 is therefore the '
           'moles of Na2CO3 the first step arrives at, cut from the line that carries '
           'it, rather than the whole fraction; rows 2 and 3 are printed on one line '
           'each and are lifted whole. The 2 : 1 mole ratio in row 2 is the one in the '
           'balanced equation the paper prints above the table.')

# ── Q3(a)(i) ───────────────────────────────────────────────────────────────
# Two //-separated points against the tariff (8 + 3): the labelled diagram,
# then the procedure. Q3(a) as a whole is (8 + 3) + (6 + 3) + (3) + (3) = 26,
# which is what the paper prints against it, so the split is confirmed rather
# than assumed.
card(3, 'a', 'i', topic='chem-u2', concept='measuring-suspended-solids-by-filtration',
     source='pdf',
     from_runs=[((7, 'a', 'i'), 4, slice(1, 8)),
                ((7, 'a', 'i'), 4, slice(9, None)),
                ((7, 'a', 'i'), 5, slice(0, None)),
                ((7, 'a', 'i'), 6, slice(0, None))],
     use=[0, [1, 2, 3]], marks=[8, 3], notation='8 + 3', stem=False,
     notes='A drawing question the scheme answers in words: 8 of the 11 marks are for '
           'a labelled filtration diagram and 3 for the measurement itself. The paper '
           'sets parts (iii) and (iv) of this question in the block above (a)(i), so '
           'the segmentation offers them as a stem and the card is left without one.')

# ── Q3(a)(ii) is refused. See the note at the foot of this file. ───────────

# ── Q3(b)(i) ───────────────────────────────────────────────────────────────
# Q3(b) is priced (6 + [6 × 3]) — seven numbers for the seven //-separated
# points across (i) to (v) — and the paper prints (24), which is 6 + 18. The
# deck's shipped cards for (ii)–(v) carry 15 of that between them, leaving 9
# here: 6 for the chloride ion and 3 for the nitrate ion.
card(3, 'b', 'i', topic='chem-4-3', concept='which-of-the-tested-ions-are-anions',
     source='pdf',
     from_runs=[((7, 'b', 'i'), 4, slice(1, 3)),
                ((7, 'b', 'i'), 4, slice(4, 6))],
     marks=[6, 3], notation='6 + [6 × 3] across Q3(b)',
     notes='The third ion in the paper\'s table, the sodium ion (Na+), is a cation and '
           'is not part of the answer. The card\'s stem is the paper\'s own table of '
           'ions, formulas and tests, which is the "first column" the question sends '
           'the candidate to.')

# ── Q9(b)(i) ───────────────────────────────────────────────────────────────
# A plotting question the scheme answers in words, five points at 3 marks
# each. Q9(b) is priced 15 here and 3 + 3 at (b)(ii), and the paper prints
# (21) against Q9(b).
card(9, 'b', 'i', topic='chem-u1', concept='plotting-mass-of-co2-against-time',
     source='pdf',
     from_runs=[((4, 'b', 'i'), 11, slice(1, 7)),
                ((4, 'b', 'i'), 11, slice(8, 15)),
                ((4, 'b', 'i'), 11, slice(16, 19)),
                ((4, 'b', 'i'), 11, slice(20, 31)),
                ((4, 'b', 'i'), 11, slice(32, 41))],
     marks=[3, 3, 3, 3, 3], notation='5 × 3',
     notes='The scheme will not accept the points joined by straight lines — the curve '
           'has to be a smooth one through the points and the origin — and it accepts '
           'the axes reversed. The card\'s stem is the paper\'s account of the '
           'experiment together with its table of results; the words "HCl solution '
           'CaCO3 before during" inside it are labels on the paper\'s apparatus '
           'diagram that the block segmentation picks up.')

# ── Q9(c) ──────────────────────────────────────────────────────────────────
# Three readings off the graph the previous part plots, priced (6 + 6 + 3),
# which is the (15) the paper prints. The scheme gives each answer as a range,
# because it is marking a value read off the candidate's own curve.
card(9, 'c', topic='chem-3-2', concept='reading-values-off-the-rate-graph',
     source='pdf',
     from_runs=[((4, 'c', None), 1, slice(2, 6)),
                ((4, 'c', None), 1, slice(8, 12)),
                ((4, 'c', None), 1, slice(14, 19))],
     marks=[6, 6, 3], notation='6 + 6 + 3',
     checked='The paper prints part (c)\'s tariff "(15)" immediately after the third '
             'of its sub-asks, so the block does not end on punctuation. Page 10 of '
             'the paper shows the question is complete as it stands: "From your graph '
             'find (i) the time taken until the reaction was complete, (ii) the time '
             'taken for 0.30 g of CO2 to be produced and lost from the flask, (iii) '
             'the mass of CO2 produced over the first 2.5 minutes."',
     notes='Each answer is a range because it is read off the candidate\'s own graph. '
           'The rows run in the paper\'s order: (i) when the reaction finished, (ii) '
           'when 0.30 g of CO2 had been lost, (iii) how much CO2 was lost in the first '
           '2.5 minutes. The reaction is complete where the curve flattens, which the '
           'paper\'s own table shows happening at 0.60 g.')


# ── The parts this file refuses, and why ───────────────────────────────────
#
# Q3(a)(ii) — "Describe how the concentration of dissolved solids could then
# have been determined." The scheme lists SIX points separated by the double
# solidus its preamble reserves for separately-marked points — evaporate to
# dryness // known (stated) volume // filtered water // in beaker // find mass
# residue // calculate the concentration — and prices them "(6 + 3)". Six
# separately-marked points cannot be paid out of two numbers, and there is no
# second document to break the tie: Q3(a) totals 26 whichever way the 9 is
# split, so the paper's tariff confirms nothing here. Every other multi-point
# part in this paper prints one number per point. Pricing this one would be
# inventing a tariff, so it stays open.
#
# Q4(b) — "Draw a dot and cross diagram to show the covalent bonding in a
# molecule of hydrogen (H2)." The scheme's entire answer is the block
# "DRAW: (6) or": the diagram itself is an image in the PDF and the text layer
# carries nothing of it. There is no answer to lift.
#
# Q8(b)(i) — "Draw the structure of a molecule of X ... Circle the group of
# atoms in your structure that makes X very soluble in water." Same again: the
# scheme's blocks are "DRAW:" and "[O–H bond not required] CIRCLE: OH circled".
# The structure is drawn, not written, and "OH circled" is an instruction to
# the examiner about the candidate's own drawing rather than an answer.
# Unlike Q1(c)(i), where the scheme prints H–C≡C–H in text, there is nothing
# here for a card to carry.
#
# Q11(b)(ii) — "Write the equilibrium constant (Kc) expression for this
# reaction." The scheme sets the expression as a fraction in a bold-maths
# font, and the extraction wrecks it twice over: the numerator and denominator
# come out as two separate blocks ("WRITE: Kc = [𝐍𝐍𝐇𝐇𝟑𝟑 ]𝟐𝟐" and
# "[𝐍𝐍𝟐𝟐][𝐇𝐇𝟐𝟐]𝟑𝟑 (6)"), and every glyph in that font is doubled. Repairing it
# means retyping the expression, which is exactly what law 1 forbids — and an
# earlier attempt at this card did retype it ("Numerator - [NH3]^2") and was
# dropped by the build's provenance gate, which is why the part reads open.
# It needs the glyph-repair pass, not a card.
#
# The four below all turn on the same missing thing: figures. No chemistry
# 2023 OL image is bound in figure_bindings.json, so a card for any of them
# would ask about something it cannot show.
#
# Q6(c)(i) — "Name the aromatic compound whose structure is shown on the
# right." The compound is only identifiable from the printed skeletal
# structure. Scheme answer: methylbenzene / phenylmethane / toluene, worth 8
# of Q6(c)'s 12. Ready to card the moment the structure is bound.
#
# Q8(a)(i) — "Give the systematic IUPAC names for X, Y and Z." X, Y and Z are
# positions on the paper's printed reaction scheme, and which compound each
# stands for can only be read off that diagram. The scheme decodes all three
# (X: ethanol // Y: ethanal // Z: ethanoic acid, 5 + 2 + 2), so the label key
# exists — but binding the figure and attaching the key is a figure pass, not
# something this file can do.
#
# Q8(d)(ii) — "Identify the organic reactant and the organic product of the
# elimination reaction in the scheme above." Same diagram: which arrow is the
# elimination step is only visible on it, and the scheme's answer again names
# a letter ("X (ethanol, C2H5OH) // ethene (C2H4)", 2 + 2 of Q8(d)'s 11).
#
# Q11(c) — the fractional-distillation passage with seven blanks, A to G. The
# paper's own instruction is "Refer to the diagram and write in your
# answerbook the omitted term corresponding to each of the letters A to G",
# and the letters sit in a passage printed beside a fractionating-column
# diagram. The block segmentation interleaves the two, so the paper's question
# text comes out as the bare sentence "The following terms are omitted from
# the passage below." with the passage and the column's labels welded together
# in the stem. The scheme answers all seven (A kerosene // B low // C high //
# D refinery gas // E small // F residue // G large, priced 7 + 7 + 3 +
# [4 × 2] = the 25 the paper prints), so this too is a figure pass away.

A.emit()
