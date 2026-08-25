#!/usr/bin/env python3
"""Chemistry 2022 Higher Level — parts the deck had not carded.

Every card here is source='pdf'. The markdown parser finds nothing at all in
this scheme: it heads each question "QUESTION 3" and Scheme only recognises the
"Q3" form, so Scheme.parts is empty for the whole sitting and source='md'
returns no candidates for any part.

The PDF parser's keys do not agree with the paper's numbering either. It files
the whole of Sections A and B under two addresses, a Q7 group and a Q60 group,
and then walks (a), (b), (c)... through each. Both heads were checked rather
than guessed at, by re-walking SchemePdf._blocks() and printing what QHEAD
matched: Q7 is the marking preamble's seventh numbered instruction, "7. Bonus
marks at the rate of 10% ...", and Q60 is the bold denominator in the Q4(f)
diamond working, "60 (0.016667) moles C per carat". Every part after each of
them inherits it. So a parser key is only an address, never evidence. Each
from_run below was found by searching every key for the answer text and then
reading the scheme page against the paper page; the citation follows the
paper, as law 3 requires.

Tariffs are the scheme's own and each is checked against the total the paper
prints for the parent:

  Q3(c)  the paper prints (24). The scheme pays the plot 4 x 3 = 12, then
         (i) 3, (ii) 3, (iii) 3 + 3. 12 + 3 + 3 + 6 = 24, so the split is
         confirmed rather than assumed.
  Q8(b)  the paper prints (32). Part (i) is priced on its own — FORMULAE (3)
         BALANCING (3) — and the scheme then says of the rest: "(ii) to (vii)
         has SEVEN POINTS: [(2 x 6) + (4 x 3) + 2]", which is 26. 6 + 26 = 32.
         That is a sliding scale over seven points, not a mark per part, so
         both Q8(b) cards are ladder= — rows with no mark of their own and the
         shape written into the notation.

Thirteen of the eighteen open asks are refused, for four reasons, printed on
stderr by the REFUSED list at the foot of this file:

  * Q5(d)(i)-(iii) and Q11(a)(v)-(vi) are already authored. authored/
    chemistry.json holds chem-2022-hl-q5-d and chem-2022-hl-q11-a-v-vi, whose
    question text and rows cover exactly those romans; neither has reached
    components/MarkBank/cards/chemistry/higher.ts, which is what reconcile
    reads. They are open in the ledger because of a merge gap, not a gap in
    the bank, and carding them again would double-card the content.
  * Q4(b) and Q9(d)(i)-(iii) are anchored to art the deck has no figure for.
  * Q8(b)(ii), (iii) and (v) each ask about "the ester E", and the sentence
    that defines E is filed by Paper as Q8(b)'s own text rather than as a stem,
    so no API here can put it on the card.
  * Q8(b)(vii) prints its two boiling points with the Symbol-font degree sign,
    U+F0B0, and glyphmap.json has no entry for it, so build-deck's repairGlyphs
    would leave it on the card.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2022, 'hl')

# ── Question 3(c): reading the hydrogen peroxide graph (paper page 4) ─────────
#
# The graph is the candidate's own — the paper prints the volume/time table in
# the part (c) stem and asks for it to be plotted — so these three need no
# figure. The scheme's answers sit in the Q3 PLOT run, which the PDF parser
# files at (7, 'c', None): point 2 answers (i), point 3 answers (ii) with its
# worked route at point 6, and (iii) straddles points 7 and 8 — the tangent on
# 7, the slope on 8, because points() splits a run on the scheme's own ' / '.

GRAPH_LIST = ('The paper sets (i), (ii) and (iii) as a comma-separated list under '
              '"Use your graph to find", so this item ends on a comma rather than a '
              'full stop. Page 4 confirms the ask is complete as lifted.')

A.card(3, 'c', 'i', topic='chem-3-2', concept='reaction-completion-time-from-a-graph',
       source='pdf', from_run=((7, 'c', None), 2, slice(2, 6)), marks=[3],
       notation='(4 x 3) + 3 + 3 + 3 + 3',
       checked=GRAPH_LIST,
       notes='A range, not a single value: it is read off the curve the candidate '
             'plotted, at the point where the volume stops rising.')

A.card(3, 'c', 'ii', topic='chem-3-2', concept='average-rate-from-a-rate-graph',
       source='pdf',
       from_runs=[((7, 'c', None), 3, slice(2, 9)),
                  ((7, 'c', None), 6, slice(0, 9))],
       use=[[0, 1]], marks=[3],
       notation='(4 x 3) + 3 + 3 + 3 + 3',
       checked=GRAPH_LIST + ' The paper also breaks the line inside the bracket, '
               'so "(in cm3 O2 per minute at room temperature and pressure)" runs '
               'across two lines of page 4.',
       notes='The accepted alternative is the scheme\'s own worked route: total volume '
             'divided by total time, which for this data is 78 over 4.')

A.card(3, 'c', 'iii', topic='chem-3-2', concept='instantaneous-rate-from-a-tangent',
       source='pdf',
       from_runs=[((7, 'c', None), 7, slice(2, 11)),
                  ((7, 'c', None), 8, slice(12, 26))],
       marks=[3, 3],
       notation='(4 x 3) + 3 + 3 + 3 + 3',
       checked='Page 4 prints "(24)" — the mark for the whole of part (c) — on the line '
               'after this last sub-part, and the block takes it in. The ask itself is '
               'complete: "the instantaneous rate of the reaction at 4.0 minutes (in '
               'cm3 O2 per minute at room temperature and pressure)."',
       notes='Reaching the second 3 marks means reading two points off the tangent, or '
             'its rise and run, before the slope. The scheme insists the tangent be '
             'drawn for full marks, but will still allow those last 3 for a rate inside '
             'the stated range with no tangent drawn, or consequentially for work done '
             'on a poor tangent or one placed at the wrong time.')

# ── Question 8(b): the raspberry ester (paper page 9) ─────────────────────────
#
# Priced as a ladder. The scheme prints one tariff over the seven marking
# points in (ii) to (vii) and never says which point takes which rate, so no
# part of that block has a mark of its own.

ESTER_LADDER = ('Q8(b)(ii) to (vii) share one tariff — the scheme prints "SEVEN POINTS: '
                '[(2 x 6) + (4 x 3) + 2]" over them — so no part of the block has a mark '
                'of its own. totalMarks is what this card\'s answers are worth at the '
                'top rate of the scale.')

A.card(8, 'b', 'iv', topic='chem-4-2', concept='classifying-esterification-as-substitution',
       source='pdf', from_run=((60, 'b', 'iv'), 3, slice(1, 2)),
       tariff='orderedSplit', ladder=6, notation='(2 x 6) + (4 x 3) + 2',
       notes=ESTER_LADDER + ' The reaction being classified is the esterification of '
             'methanoic acid with ethanol, written out in part (i).')

A.card(8, 'b', 'vi', topic='chem-4-2', concept='products-of-base-hydrolysis-of-an-ester',
       source='pdf',
       from_runs=[((60, 'b', 'vi'), 0, slice(1, 2)),
                  ((60, 'b', 'vi'), 1, slice(0, 1)),
                  ((60, 'b', 'vi'), 1, slice(2, 4)),
                  ((60, 'b', 'vi'), 2, slice(0, 1))],
       use=[[0, 1], [2, 3]],
       tariff='orderedSplit', ladder=12, notation='(2 x 6) + (4 x 3) + 2',
       notes=ESTER_LADDER + ' Both products are wanted: the scheme separates them with '
             'a double solidus, which is its notation for two separately marked points.')


# ── Section, re-filed ────────────────────────────────────────────────────────
# lib.py files a card under Section A whenever its question number is 12 or
# less, which is Biology's split. Chemistry's is different: page 5 of this
# paper prints "Section B" above Question 4, and every Q4-Q11 card already in
# components/MarkBank/cards/chemistry/higher.ts carries "B". Section is not
# decoration — build-deck reads it to pick the option cap and to resolve which
# paper a card binds to — so the two Question 8 cards are re-filed here.
for _card in A.cards:
    _q = int(re.match(r'\d{4} \w{2} Q(\d+)', _card['questionRef']).group(1))
    _card['section'] = 'A' if _q <= 3 else 'B'


# ── Refused, with the reason each is refused ─────────────────────────────────
REFUSED = [
    ('2022 HL Q4(b)',
     'anchored to art the deck cannot show. The ask is "The diagram shows the origin of '
     'one of the lines in the Balmer series ... as the electron moves from one energy '
     'level to another as shown", and the scheme answers it in terms of n = 3 and n = 2 '
     '— which only the printed energy-level diagram supplies. Page 5 of the paper draws '
     'it as vector art with a "red light" label, and the figure pass did not extract it: '
     'authored/chemistry-figures.json holds only Q4(f) and Q4(k) for that page. Needs a '
     'bound figure.'),

    ('2022 HL Q5(d)(i)',
     'already authored. chem-2022-hl-q5-d in authored/chemistry.json carries all three '
     'romans of Q5(d) in one card, priced 2 x 3 + 3 + 3 = 12. It has not been merged '
     'into components/MarkBank/cards/chemistry/higher.ts, which is the file reconcile '
     'reads, so the ledger shows the part open. That is a merge gap, not a gap in the '
     'bank; carding it here would ship the content twice.'),
    ('2022 HL Q5(d)(ii)', 'already authored — see Q5(d)(i); the same card carries it.'),
    ('2022 HL Q5(d)(iii)', 'already authored — see Q5(d)(i); the same card carries it.'),

    ('2022 HL Q8(b)(ii)',
     '"Give the systematic IUPAC name for E." E is defined by the sentence "The pure '
     'ester E has a rum-like aroma and is partially responsible for the flavour of '
     'raspberries", which Paper files as Q8(b)\'s own text rather than as a stem — '
     'paper.stem(8, "b") and paper.stem(8) are both None. card() takes its stem from '
     'those two calls and nothing here may type the sentence, so the card would ask for '
     'the name of an ester it never identifies.'),
    ('2022 HL Q8(b)(iii)',
     '"How many carbon atoms in a molecule of the ester E are in planar geometry?" — '
     'same missing stem as (ii); the answer depends on knowing what E is.'),
    ('2022 HL Q8(b)(v)',
     '"Another ester F ... is a structural isomer of E. Identify F." — same missing stem '
     'as (ii); F cannot be identified without E.'),
    ('2022 HL Q8(b)(vii)',
     'the paper prints the two boiling points with U+F0B0, the Symbol-font degree sign, '
     'so the lifted text reads "ethanoic acid (118 C)", with a private-use character '
     'where the degree sign belongs. glyphmap.json carries twelve other private-use '
     'characters out of these papers -- U+F0AE to an arrow, U+F0B7 to a bullet -- but '
     'no entry for U+F0B0, so build-deck\'s repairGlyphs would leave it on the card, '
     'and the shipped Chemistry deck holds no private-use character anywhere against '
     '21 proper degree signs. The answer itself is clean; the card becomes available '
     'as soon as derive_glyphs.py maps U+F0B0.'),

    ('2022 HL Q9(d)(i)',
     '"What volume of the NaOH solution neutralised solution A?" A is one of four pH '
     'titration curves drawn on the paper and the answer, 20.0 cm3, is read off that '
     'graph. There is no stem naming A and no figure for the page in '
     'authored/chemistry-figures.json, so the card needs a bound figure and a decoded '
     'label key for A to D.'),
    ('2022 HL Q9(d)(ii)',
     '"Deduce the molar concentrations of solutions A, B, C and D." — names all four '
     'lettered curves; needs the bound figure and the label key, as (i) does.'),
    ('2022 HL Q9(d)(iii)',
     '"Which of the weak acids C and D has the greater acid dissociation constant (Ka) '
     'value?" — the justification the scheme accepts is read off the two curves '
     '("first part of C curve below D curve", "C curve becomes steep first"), so this '
     'needs the bound figure and the label key too.'),

    ('2022 HL Q11(a)(v)',
     'already authored. chem-2022-hl-q11-a-v-vi in authored/chemistry.json carries both '
     'romans, with the oxidation numbers, the balanced equation and the reducing agent '
     'as four rows of 3. Like Q5(d) it has not been merged into the shipped deck, which '
     'is why the ledger shows it open.'),
    ('2022 HL Q11(a)(vi)', 'already authored — see Q11(a)(v); the same card carries it.'),
]
for ref, why in REFUSED:
    print(f'  REFUSED {ref}: {why}', file=sys.stderr)

A.emit()
