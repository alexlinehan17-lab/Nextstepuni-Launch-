#!/usr/bin/env python3
"""Biology 2025 Higher Level.

The 2025 Higher Level scheme heads its questions "Question 11", not "Q11", and
neither parser recognises that spelling: Scheme finds no parts at all and
SchemePdf files every block under the numbered lines of its own marking
preamble ("1. Key words...", "2. Cancelled answers", "3. Surplus answers").
So the scheme's key for a part is not the paper's — this paper's Q13(b)(iii)
sits under the PDF parser's (3, 'b', 'iii'), Q17(b)(iii) under its (2, None,
'iii'), Q17(d)(i) under its (3, None, 'i') — and every card here names the
parser's key and takes its own answer out of that run by position.

The citation is always the PAPER's numbering; the key in from_run/from_runs is
only the address the parser happens to file the answer under.

Refusals live at the bottom, each with the scheme line that caused it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2025, 'hl')

# Said on every card rather than once here, because a card is read on its own.
KEYNOTE = ('The 2025 Higher Level scheme spells its question heads out in full '
           '("Question 17"), which no parser reads, so its answers are filed '
           'under the numbered lines of the marking preamble instead of under '
           "the question. The citation above is the paper's own numbering.")

# lib.py files a card as Section A when the question number is 12 or under and
# Section B otherwise, which is right for the subjects it was written against
# and wrong for Biology: this paper runs A over Q1-Q7, B over Q8-Q10 and C over
# Q11-Q17, and the section is what picks the paper the card links out to
# (Sections A and B are component 038, Section C is component 040). New Section C
# cards say so; the shipped Q13(b)(iii) card below is left exactly as it shipped,
# section and all, because its card is already in the deck.
SECTION_C = 'C'

A.card(13, 'b', 'iii', topic='bio-2-3', concept='cyclic-and-non-cyclic-electron-flow',
       source='pdf', from_run=((3, 'b', 'iii'), 2, slice(0, None)), marks=[3])

# ---------------------------------------------------------------- Section A --

# Q2(d). The scheme prices the drawing and the labels separately — "Drawing ... 3"
# then "Labels: ... Any two 2(1)" — so the card is two rows, 3 + 2, which is the
# whole of the part. The four labels are the scheme's own list and any two of
# them score a mark each; they ride as alternatives on the label row because the
# solidus is the scheme's separator for exactly that list.
A.card(2, 'd', topic='bio-2-6', concept='root-transverse-section',
       source='pdf',
       from_runs=[((3, 'd', None), 3, slice(0, None)),
                  ((3, 'd', None), 4, slice(0, None)),
                  ((3, 'd', None), 5, slice(0, None)),
                  ((3, 'd', None), 6, slice(0, None)),
                  ((3, 'd', None), 7, slice(0, None))],
       use=[0, [1, 2, 3, 4]], marks=[3, 2], notation='3 + 2(1)',
       figure='biology-2025-HL-paper1-p04-i1',
       context='The drawing mark is for the section itself; the scheme wants the '
               'vascular tissue visible in the centre of the circle.',
       notes='The label row is worth 2(1) — any two of the labels the scheme lists, '
             'one mark each — not 2 marks for the first one. The figure is the '
             "paper's own Question 2 artwork, which is where the dashed line the "
             'question cuts along is printed. ' + KEYNOTE)

# Q5(e). Two marks, one row, and the scheme says only what the line does.
A.card(5, 'e', topic='bio-3-2', concept='growth-curve-after-nutrients-run-out',
       source='pdf', from_run=((3, 'e', None), 6, slice(0, 2)), marks=[2],
       stem=False, figure='biology-2025-HL-paper1-p07-i0',
       notes='Stem suppressed: the paper sets the graph axis labels in the same '
             'block as the Question 5 preamble, so the lifted stem ends "Y '
             'Population X Time". The figure carries the curve the question asks '
             'the candidate to continue. ' + KEYNOTE)

# Q6(e). Same two-part shape as Q2(d): draw any two of three, label any two of
# three. 3 + 2 is the whole part.
A.card(6, 'e', topic='bio-2-6', concept='villus-internal-structure',
       source='pdf',
       from_runs=[((3, 'e', None), 10, slice(0, None)),
                  ((3, 'e', None), 11, slice(0, None)),
                  ((3, 'e', None), 12, slice(0, 2)),
                  ((3, 'e', None), 13, slice(0, None)),
                  ((3, 'e', None), 14, slice(0, None)),
                  ((3, 'e', None), 15, slice(0, 6))],
       use=[[0, 1, 2], [3, 4, 5]], marks=[3, 2], notation='Any two 3 + Any two 2(1)',
       context='The scheme wants any two of the three structures drawn.',
       notes='Both rows are "any two" menus in the scheme, not single answers: the '
             'drawing row is worth 3 for any two of the structures listed, the '
             'label row 2(1) for any two of its own list. ' + KEYNOTE)

# ---------------------------------------------------------------- Section C --

# Q16(a)(iii).
rhizopus = A.card(16, 'a', 'iii', topic='bio-3-2', concept='rhizopus-nutrition',
                  source='pdf', from_run=((4, None, 'iii'), 5, slice(0, None)),
                  marks=[3], stem=False,
                  notes='Stem suppressed: the paper sets the Question 16(a) preamble '
                        'in the same block as the (iv) sub-items, so the lifted stem '
                        'is the wrong text. ' + KEYNOTE)

# Q17(b)(ii). The scheme's first point, "Correctly named antagonistic muscle
# pair", is a criterion — it says what the examiner must see and names nothing —
# so it is left off and the card carries 6 of the part's 9 marks. The two
# movement points do state the mechanism, which is the recallable half.
antagonists = A.card(
       17, 'b', 'ii', topic='bio-2-4', concept='how-an-antagonistic-pair-moves-a-joint',
       source='pdf',
       from_runs=[((2, None, 'ii'), 20, slice(0, None)),
                  ((2, None, 'ii'), 21, slice(0, None))],
       marks=[3, 3],
       notes='PARTIAL. The part is worth 9. The scheme\'s third point, "Correctly '
             'named antagonistic muscle pair", is a content-free criterion — it '
             'credits naming any pair and supplies no answer — so it is not carded '
             'and this card covers the remaining 6 marks. ' + KEYNOTE)

# Q17(b)(iii) and Q17(d)(i). Both are drawing questions the scheme answers with
# a named list, which is what makes them cardable: "Diagram: Epiphysis and
# diaphysis and medullary cavity", "Diagram: Penis and testes and sperm duct and
# urethra". The tariff after each is descending — all of them for 6, one missing
# for 3, otherwise 0 — which goes in the notation, not in the answer.
long_bone = A.card(
       17, 'b', 'iii', topic='bio-2-4', concept='long-bone-internal-structure',
       source='pdf',
       from_runs=[((2, None, 'iii'), 19, slice(0, 7)),
                  ((2, None, 'iii'), 20, slice(0, None)),
                  ((2, None, 'iii'), 21, slice(0, None)),
                  ((2, None, 'iii'), 22, slice(0, None)),
                  ((2, None, 'iii'), 23, slice(0, None)),
                  ((2, None, 'iii'), 24, slice(0, None)),
                  # The scheme's last label carries its own dot leader, which is
                  # how it says the list goes on; taken as printed.
                  ((2, None, 'iii'), 25, slice(0, 1))],
       use=[0, [1, 2, 3, 4, 5, 6]], marks=[6, 3],
       notation='6, 3, 0 + 3(1)',
       context='The scheme prints "6, 3, 0" against the diagram: all three '
               'structures scores 6, any one missing scores 3, otherwise nothing.',
       notes='The label row is 3(1) — any three of the labels the scheme lists, one '
             'mark each. Rows sum to the 9 the scheme prices the part at. ' + KEYNOTE)

male_repro = A.card(
       17, 'd', 'i', topic='bio-2-5', concept='male-reproductive-system-diagram',
       source='pdf',
       from_runs=[((3, None, 'i'), 17, slice(0, 9)),
                  ((3, None, 'i'), 18, slice(0, None)),
                  ((3, None, 'i'), 19, slice(0, None)),
                  ((3, None, 'i'), 20, slice(0, None)),
                  ((3, None, 'i'), 21, slice(0, None)),
                  ((3, None, 'i'), 22, slice(0, None)),
                  ((3, None, 'i'), 23, slice(0, None)),
                  ((3, None, 'i'), 24, slice(0, None)),
                  ((3, None, 'i'), 25, slice(0, 1))],
       use=[0, [1, 2, 3, 4, 5, 6, 7, 8]], marks=[6, 3],
       notation='6, 3, 0 + 3(1)', stem=False,
       checked='2025 Higher Level paper, component 040, page 10. The part is printed '
               'exactly as lifted; it is flagged only because it ends on "(Z)" '
               'rather than on punctuation.',
       context='The scheme prints "6, 3, 0" against the diagram: all four structures '
               'scores 6, any one missing scores 3, otherwise nothing.',
       notes='PARTIAL. The part is worth 12: 6 for the diagram, 3(1) for any three '
             'labels, and three further 1-mark points for siting X, Y and Z on it. '
             'Those last three are not carded — the scheme sets them as table cells '
             'the PDF reader collapses into its mark column, so no parser hands them '
             'back whole and they would have to be typed. Stem suppressed: the paper '
             'block the parser reaches for is the acknowledgements list. ' + KEYNOTE)

# Q16 and Q17 are Section C, which is where the paper link is decided. See the
# note on SECTION_C above.
for card in (rhizopus, antagonists, long_bone, male_repro):
    card['section'] = SECTION_C

# ------------------------------------------------------------------ refused --
#
# Every remaining open 2025 HL ask, and the scheme line that refuses it. The
# common shape is a part whose answer depends on which example the candidate
# chose, which the scheme can only price as a criterion — "Correct example
# given", "Correct matching treatment". A card whose back reads that teaches
# nothing the student did not already know from the question.
#
#   Q11(c)(iv)   "Correct example given 3" (twice) — the plant is the
#                candidate's own choice and the scheme names none.
#   Q13(c)(iv)   "Two correct and relevant named chemicals / First correct
#                physical procedural step described / Second correct physical
#                procedural step described" — three criteria, no method.
#   Q14(b)(iv)   "Matching corrective measure described."
#   Q14(c)(iv)   "Correct matching cause / Correct matching treatment."
#   Q15(c)(iii)  "Name: correctly named pollutant / Effect: correct matching
#                effect."
#   Q15(c)(iv)   "Correct matching control measure described."
#   Q16(a)(v)    "Correct beneficial effect named / Correct harmful effect
#                named."
#   Q16(b)(vi)   "Correct matching treatment."
#   Q16(d)(iii)  "Name of lymphocyte 1 / Correct matching role of lymphocyte 1"
#                and the same again for lymphocyte 2 — four criteria, and the
#                scheme names no type of lymphocyte at all.
#   Q17(b)(i)    "Three correctly named joint types 3(2) / Matching locations
#                stated correctly 3(2)" — no joint and no location is named.
#   Q17(d)(v)    "Correct cause given / Corrective measure given."
#   Q8(b)(ii)    "Correctly named abiotic factor 1 / Matching method of
#                measurement of factor 1 outlined", and the same for factor 2 —
#                the factors are the candidate's own study.
#
#   Q4(d)(i)     A different reason. The scheme's only substantive row is
#                "Correct sketch: showing cell membrane and cell wall", which
#                the build's own content-free gate reads as a criterion
#                ("correct sketch"), and the two rows left are "Cell membrane"
#                and "Cell wall" — the two labels the question itself names. A
#                card of those two teaches nothing and would show 2 of the
#                part's 5 marks.
#
#   Q9(b)(ii)    Already decided, and left decided. The authored deck carries
#                bio-2025-hl-q9-b-ii marked DELIBERATELY LEFT DROPPED: six of
#                the scheme's seven points are examiner criteria, and the card
#                that survives them teaches a student to under-answer a 21-mark
#                part. Not re-authored here.

A.emit()
