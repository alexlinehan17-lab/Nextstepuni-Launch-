#!/usr/bin/env python3
"""Chemistry 2023 Higher Level — parts the deck had not carded.

Two things about this paper decide how every card below is built.

The markdown parser finds nothing at all in it. Scheme's QHEAD only recognises
the "Q3" form and this scheme heads its answers "QUESTION 3", so Scheme.parts
is empty for the whole paper and source='md' returns no candidates for any
part. Every answer here therefore comes from the PDF parser.

The PDF parser's keys do not agree with the paper's numbering. Its question
number comes from whichever block last looked like a heading, so the numbered
marking preamble ("4. The bold text indicates...") claims a Question 4 and most
of Sections A and B end up filed under its Q4 and Q8 letters — Q1(d)'s
titration calculation under (8, 'd'), Q2(a)'s apparatus under (8, 'a') and
(8, 'c', 'iv'), Q11(a)(ii)'s gas-law explanation under (4, 'a', 'ii'). Each
from_run below was found by searching every key for the answer text and then
reading the scheme page that prints it; the citation follows the paper, as it
must. The paper's own numbering and the scheme's agree throughout — it is only
the parser that is out of step, so no card needs a renumbering note.

Three of these ids already exist in scripts/markbank/authored/chemistry.json as
hand-authored cards that have never shipped: q10-b-iii, q10-b-iv and q11-a-ii.
Each fails the build's provenance gate because its answer was retyped with the
fractions rebuilt by hand ("1.77/(14n + 90) = 2.43/(14n + 134)",
"pV = nRT => V/T = nR/p = constant") and no such string exists in the scheme.
The cards here answer the same parts with text the scheme actually prints, so
they are takeovers, not duplicates: merge.py will refuse them until those three
ids are listed in authored/adopted-ids.json, which is the mechanism it provides
for exactly this and is deliberately left to the operator rather than done here.

Refused, and why, so a later pass can pick them up:

  Q4(i)        the answer is a drawn structure of glycerol. The text layer
               carries "DRAW:" and the bracketed partial-credit note and
               nothing else.
  Q8(a)(ii),   every one of these names a conversion (A, B, C, E) lettered on
  Q8(b),       the reaction scheme at the head of Question 8. That scheme is
  Q8(c)(ii),   chemistry-2023-HL-paper-p09-i1, extracted and described but not
  Q8(d)(i),    bound to any card, and the letters it uses are decoded by the
  Q8(d)(ii)    figure rather than by the marking scheme — which names only D,
               in passing, as "D (ethanol to ethene)". Unanswerable without the
               scheme in front of you, so they belong to a figure pass.
  Q8(e)(i)–(ii)  the same, against the four boiling-point curves A–D, and the
               paper's block for these two parts is empty besides: the romans
               sit in a narrow column with no text of their own.
  Q8(e)(iii)   the paper sets (iii), (iv) and (v) in that same column and the
               block runs all three together, ending "(18) A B C D". A first
               sentence trim cannot confirm itself here because a Chemistry
               scheme never reprints the question, and the ask points at the
               curves anyway.
  Q8(c)(i)     "Draw two repeating units of poly(ethene)" — again a structure,
               with only examiner instructions in the text layer.
  Q9(b)(i)     the Kc expression comes out "[𝐏𝐏𝐏𝐏𝐏𝐏𝟓𝟓]": mathematical-bold
               glyphs, every character doubled.
  Q9(g)        not a part. The paper's Question 9 runs (a) to (d); the census
               reads the state symbol in "PCl5 (g)  ΔH = –87.9 kJ mol–1" as a
               part letter and files the thermochemical datum as its text.
  Q10(b)(ii)   the two answers are fractions, printed in the same doubled
               mathematical-bold glyphs.
  Q10(c)(iii)  the completed nuclear equation is superscript and subscript
               artwork the text layer scrambles into "𝟏𝟏𝟏𝟏𝟏𝟏 𝐗𝐗𝐗𝐗 ... 𝟓𝟓𝟓𝟓 –1".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2023, 'hl')

# ── Question 1, the manganate(VII) titration calculation ───────────────────
# Q1(d) is priced (18) on the paper and the scheme splits it 9 + 3 + 3 + 3 over
# the four calculations. (d)(i) is already carded; these are the other three.
# Each prints its answer twice — once as the headline and once at the end of
# the working — so the second (3) is the same three marks restated, not a
# fourth mark.
TITRATION = '9 + 3 + 3 + 3 across the four calculations of Q1(d)'
CALC_RUNON = ('The paper sets Q1(d)(i) to (iv) as a numbered list under one '
              '"Calculate" cue, so each part ends on the comma that carries the '
              'list on rather than on a full stop. Page 2 of the 2023 Higher '
              'Level paper prints this part exactly as the card carries it.')

A.card(1, 'd', 'ii', topic='chem-4-1', concept='moles-of-iron-ii-in-a-25-cm3-portion',
       source='pdf', from_run=((8, 'd', None), 6, slice(2, 12)), marks=[3],
       notation=TITRATION, checked=CALC_RUNON,
       notes='The scheme requires the answer to Q1(d)(i) to be divided by 40 — the '
             '25.0 cm3 portion is a fortieth of the litre that part (i) reports.')

A.card(1, 'd', 'iii', topic='chem-4-1', concept='moles-of-manganate-vii-reduced',
       source='pdf', from_run=((8, 'd', None), 8, slice(9, 18)), marks=[3],
       notation=TITRATION, checked=CALC_RUNON,
       notes='The scheme sets out the mole ratio Fe2+ : potassium manganate(VII) '
             'as 5 : 1 above this answer and requires the answer to Q1(d)(ii) to be '
             'divided by five.')

A.card(1, 'd', 'iv', topic='chem-4-1', concept='concentration-of-manganate-vii-solution',
       source='pdf', from_run=((8, 'd', None), 0, slice(37, 42)), marks=[3],
       notation=TITRATION,
       checked='The paper prints the part mark "(18)" after the last of the four '
               'calculations, so the text ends on a bracketed number. Page 2 of the '
               '2023 Higher Level paper shows the ask complete: "the concentration of '
               'the potassium manganate(VII) solution in moles per litre."',
       notes='A range, not a single value: the scheme accepts anything from 0.02 to '
             '0.022 M. It gets there by putting the moles from Q1(d)(iii) against the '
             '22.6 cm3 average titre the question gives, and it refuses to award all '
             '18 marks of Q1(d) for a correct answer to this part alone.')

# ── Question 2, preparing ethyne ───────────────────────────────────────────
# Q2(a) is priced (14): 3 + 3 + 3 for the diagram here and 5 for (a)(ii),
# already carded. The two chemicals are the whole of the chemistry; the third
# mark is the scheme's own criterion for the apparatus, kept so the card does
# not understate what the diagram is worth.
A.card(2, 'a', 'i', topic='chem-u2', concept='preparing-and-collecting-ethyne-apparatus',
       source='pdf',
       from_runs=[((8, 'c', 'iv'), 4, slice(0, 2)),
                  ((8, 'c', 'iv'), 5, slice(0, 3)),
                  ((8, 'a', 'i'), 0, slice(1, 5))],
       marks=[3, 3, 3], notation='3 + 3 + 3',
       notes='Two of the three marks are for naming the right chemicals in the right '
             'places; the third is for the arrangement of the apparatus itself, and '
             'the scheme says no more about it than the row does.')

# ── Question 6, the alkane heat-of-combustion graph ────────────────────────
# Q6(e) is priced (11): 6 for (e)(i), already carded, and 5 here. The paper's
# block above this part is the graph's x-axis label, so the card carries no
# stem rather than "Number of carbons".
A.card(6, 'e', 'ii', topic='chem-3-1',
       concept='delta-h-difference-between-successive-alkanes',
       source='pdf', from_run=((4, 'e', 'ii'), 0, slice(1, 6)), marks=[5],
       stem=False,
       checked='The paper prints the part mark "(11)" after the question, so the text '
               'ends on a bracketed number. Page 7 of the 2023 Higher Level paper '
               'prints the ask in full above it.',
       notes='An estimate read off a graph, so the scheme accepts a range rather than '
             'a value. The graph itself is not needed to learn what the step between '
             'successive alkanes is worth.')

# ── Question 9, the PCl5 equilibrium ───────────────────────────────────────
A.card(9, 'd', 'i', topic='chem-3-3',
       concept='le-chatelier-on-adding-chlorine-to-the-pcl5-equilibrium',
       source='pdf',
       from_runs=[((4, 'd', 'i'), 2, slice(1, 7)),
                  ((4, 'd', 'i'), 2, slice(8, 26))],
       marks=[3, 3], notation='2 × 3',
       notes='The scheme writes the two marks as one point split by its double '
             'solidus — the stress, then how the equilibrium relieves it — so the '
             'second mark is not available for naming the stress a second time.')

# ── Question 10(b), succinic acid ──────────────────────────────────────────
# Q10(b) is priced (25) and the scheme splits it 6 + 6 + 7 + 6. (iii) is the
# seven: (2) for reducing the two mole expressions to one equation, (2) for n,
# (3) for the molar mass that follows. The scheme prints two routes to the
# first two marks and a trial-and-error box worth the same, and forbids taking
# marks from both boxes.
A.card(10, 'b', 'iii', topic='chem-1-4', concept='find-n-and-molar-mass-succinic-acid',
       source='pdf',
       from_runs=[((4, 'b', 'iii'), 9, slice(1, 4)),
                  ((4, 'b', 'iii'), 8, slice(0, 7)),
                  ((4, 'b', 'iii'), 10, slice(1, 4)),
                  ((4, 'b', 'iii'), 11, slice(0, 7))],
       use=[[0, 1], [2], [3]], marks=[2, 2, 3], notation='2 + 2 + 3',
       notes='The first row is the equation that comes of setting the two mole '
             'expressions of Q10(b)(ii) equal to each other; the scheme prints the '
             'expanded and the collected form and takes either. It also allows the '
             'whole part to be done by trial and error from n = 2, but marks from the '
             'two routes may not be mixed.')

A.card(10, 'b', 'iv', topic='chem-1-4', concept='volume-of-naoh-for-complete-reaction',
       source='pdf',
       from_runs=[((4, 'b', 'iv'), 5, slice(2, 5)),
                  ((4, 'b', 'iv'), 6, slice(1, 4)),
                  ((4, 'b', 'iv'), 8, slice(2, 6))],
       marks=[2, 2, 2], notation='2 + 2 + 2',
       checked='The paper prints the part mark "(25)" after the last part of Q10(b), '
               'so the text ends on a bracketed number. Page 11 of the 2023 Higher '
               'Level paper prints the ask in full above it.',
       notes='Three marked steps rather than one answer: the moles of acid, the moles '
             'of sodium hydroxide those need — twice the acid, from the balanced '
             'equation in the question — and the volume that holds them.')

# ── Question 11(a), the ideal gas equation ─────────────────────────────────
# The scheme's first form of this answer is the rearrangement V/T = nR/p, which
# the PDF renders as doubled mathematical-bold glyphs. The row takes the
# scheme's other form, which is words and traces.
A.card(11, 'a', 'ii', topic='chem-2-3', concept='charles-law-consistent-with-pv-nrt',
       source='pdf', from_run=((4, 'a', 'ii'), 20, slice(0, 14)), marks=[3],
       notes='The scheme gives this answer twice, once as the rearrangement of '
             'pV = nRT and once as the sentence the row carries; the row takes the '
             'sentence because the rearranged form survives only as mangled glyphs in '
             'the scheme\'s text layer. The paper sets the lead-in to Q11(a)(iii) '
             'directly beneath this part with no marker between them, so the block '
             'ends on that sentence about the limitations of pV = nRT; the ask is the '
             'first sentence.')

A.emit()
