#!/usr/bin/env python3
"""Biology 2021 Ordinary Level — parts the deck had not carded.

The scheme answers on the same line as the question it is repeating, so each
answer is taken out of that line rather than off one of its own.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2021, 'ol')

# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(9, 'b', 'vii', topic='bio-2-1', concept='enzyme-activity-against-ph-curve',
       source='pdf', from_run=((9, 'b', 'vii'), 0, slice(13, None)), marks=[3])

A.card(11, 'b', 'vii', topic='bio-3-1', concept='food-chain-from-a-passage',
       source='pdf', from_run=((11, 'b', 'vii'), 0, slice(11, 18)), marks=[3],
       checked='The paper prints the part mark "(27)" after the question, so the text ends '
               'on a bracketed number rather than punctuation.')

A.card(14, 'c', 'ii', topic='bio-2-6', concept='where-the-endocrine-glands-are',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3], notation='3 at 3 marks each',
       row_kind='anyN',
       checked='The question runs its list of glands on after the instruction without '
               'punctuation between them, which is why the text is flagged. Both halves '
               'are the question as printed.',
       notes='Any three of the scheme\'s six: it also allows the pancreas, the ovaries '
             'and the testes.')

# ── Section A, Q7: the human-skeleton diagram ──────────────────────────────
# Neither parser keys Q7's parts under 7. The markdown one takes its question
# numbers off the mark-band lines ("Q7 (a) – (f)"), and this scheme prints those
# AFTER the answers they price, so everything in Q7 lands under (7)(a) welded to
# the band; the PDF one runs one question behind through Section A, filing Q7(b)
# and Q7(c) under its own (6)(b) and (6)(c). Both were read off page 10 of the
# 2021 Ordinary Level scheme before being lifted out of those blocks.
#
# Q7 is priced as one ordered split, 2(6) + 3(2) + 2(1) = 20 over the seven
# responses in (a)-(f) ("Number of correct responses 1 2 3 4 5 6 7 / Mark 6 12
# 14 16 18 19 20"), so no part of it has a mark of its own. ladder= says that
# out loud rather than inventing a per-part split, and matches the shipped
# Q7(a), Q7(d), Q7(e) and Q7(f) cards.
SKELETON = 'biology-2021-OL-paper1-p07-i0'
Q7_LADDER = dict(tariff='orderedSplit', notation='2(6) + 3(2) + 2(1)', ladder=20)

A.card(7, 'b', topic='bio-2-4', concept='where-a-synovial-joint-is-on-the-skeleton',
       source='pdf', from_run=((6, 'b', None), 1, slice(0, None)),
       figure=SKELETON, stem=False, **Q7_LADDER,
       notes='Same catalogued crop as the shipped Q7(d) card, and the image was opened '
             'again for this one: front-view human skeleton, complete on every edge, '
             'with Q7(a)-(f) printed down the left column. The ONLY word printed on the '
             'skeleton is "Skull"; no X and no F are pre-printed, which is why this card '
             'carries the figure with no label key — there are no letters to decode. The '
             'stem is dropped rather than lifted because the paper block that holds it '
             'drags that "Skull" label in after the sentence; the crop shows the diagram '
             'and its own instruction, so nothing is lost. Q7 is one ordered split over '
             '(a)-(f), so the row carries no mark and totalMarks is the question\'s 20.')

# 2021 OL Q7(c) is NOT carded. The paper asks "Name the type of synovial joint
# you have labelled X on the diagram", and the scheme answers it conditionally —
# "Ball and socket (if X is located at the shoulder or hip) or hinge (if X is
# located at the knee or elbow)". X is a mark the candidate makes: the crop
# carries no letters at all (the catalogue entry warns in capitals that it must
# never be captioned as already showing X or F), so there is no honest label key
# for it, and build-deck drops any card whose question names a letter it cannot
# decode. The ask is answerable only relative to something a card cannot show.

# ── Section B, Q9(b)(i) ────────────────────────────────────────────────────
# The markdown parser re-keys (9)(b)(i) when it reaches the band line at the end
# of Q9(b), so the mark ladder is welded onto the tail of the real answer:
# "Correctly named enzyme (e.g. catalase or pepsin or amylase) Mark 9 18 19 20
# 21 22 23". The words up to the closing bracket are the scheme's own answer.
#
# This is a criterion that NAMES the things — the distinction contentFree.mjs
# draws, and the reason it is carded where Q11(c)(ii)'s bare "Correctly named
# pollutant" is not. The paper's own wording gives the candidate no list of
# enzymes to choose from, so which three the examiner accepts is real recall.
A.card(9, 'b', 'i', topic='bio-u2', concept='enzyme-used-in-the-ph-investigation',
       from_run=((9, 'b', 'i'), 0, slice(0, 9)), stem=False,
       tariff='orderedSplit', notation='2(9) + 6(1)', ladder=24,
       notes='Q9(b) is priced as one ordered split, 2(9) + 6(1) = 24 over the seven '
             'responses in (b)(i)-(vii), so no part of it has a mark of its own — the '
             'same shape as the shipped Q9(b)(ii)-(vi) cards. The stem is dropped rather '
             'than lifted: the paper block for it holds only the graph axis labels '
             '("Rate of enzyme activity pH") from part (vii) further down the page.')
A.cards[-1]['section'] = 'B'      # Section B is Q8-Q10; lib letters Q1-Q12 'A'.

# ── Section C, Q11(b)(iv) ──────────────────────────────────────────────────
# The one part of this batch where the key join is trustworthy: the scheme
# prints its own cue, "Name a predator mentioned in the passage:", directly
# above the answer, and the paper prints "Name a predator mentioned in the
# passage above." at (b)(iv). Cited to the paper; the scheme drops "above".
A.card(11, 'b', 'iv', topic='bio-3-1', concept='predator-named-in-the-passage',
       marks=[3],
       notes='Q11(b) is a comprehension on a passage about red and grey squirrels in '
             'Ireland; the pine marten is the predator it names. Q11(b) is marked 3 a '
             'response over nine responses (3 6 9 12 15 18 21 24 27), so the part is '
             'worth a flat 3 — the same tariff the shipped Q11(b)(iii), (v) and (vi) '
             'cards carry.')
A.cards[-1]['section'] = 'C'      # Section C is a separate booklet (LC025GLP040EV);
                                  # lib letters Q1-Q12 'A', which would cite the wrong
                                  # paper. The shipped hand-authored Q11 cards say 'C'.

# ── Refused, and why ───────────────────────────────────────────────────────
# Five more of the 2021 OL open asks are answered by the scheme only with
# scaffolding — a criterion for the examiner with no content behind it — so
# there is nothing a student could learn from the back of the card:
#
#   Q8(a)(i)    "X correctly positioned"
#   Q8(a)(ii)   "Y correctly positioned"
#   Q11(c)(ii)  "Correctly named pollutant" + "Matching effect"
#   Q11(c)(iii) "Matching control method"
#   Q13(a)(ii)  "Correct blood cell type" + "Matching function"
#   Q16(a)(vi)  "Named disorder" + "Method of correction"
#
# And Q12(c)(iv) asks for "one simple labelled diagram which represents both
# stages of the cell cycle", which the scheme prices 2(3) but answers only
# "Chart correct: 3 marks / Both labels correct: 3marks". It never says what the
# chart shows or what the two labels are, so it is a drawing question with no
# stated criteria — the drawing- case, not the drawing+ one.

A.emit()
