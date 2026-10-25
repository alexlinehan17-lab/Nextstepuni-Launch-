#!/usr/bin/env python3
"""2021 Ordinary Level Chemistry, re-carded part by part from the paper and the labelled scheme.

    python3 scripts/markbank/authoring/chem_audit_2021_ol.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2021_ol.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2021 ol    # write them

Drafted by chem_draft.py and corrected card by card, the way
chem_audit_2022_ol.py re-cards 2022 OL: every question text, stem and lead-in
is the PAPER's print of its part and every marking point is the SCHEME's answer
closed by its own mark cell.

The 2021 Ordinary paper underlines the term a part asks about ("Gas B is
unsaturated. (i) Explain the underlined term."), which no text layer carries:
those parts take the paper's own print as their question.

Pre-audit ids are kept (a card that joined parts priced by separate cells
keeps its id on its first part; later parts are new cards); WITHDRAWN lists the
pre-audit cards that duplicated another or held a piece of a task the scheme
prices as one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, anyN, display, point  # noqa: E402

P = Printed(2021, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2021-OL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'
SPLIT = ('The scheme prices these points together as {} without saying which point earns which '
         'part, so no per-point value is shown.')


def k(*parts):
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


def print_question(suffix):
    """The paper's own print of the part as the card's question."""
    C.cards[-1]['questionFigureKey'] = FIG + suffix


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {
    'chem-2021-ol-q1-a': ('chem-2021-ol-q1-a-fig', 'Duplicated chem-2021-ol-q1-a-fig (both cited Q1(a)).'),
    'chem-2021-ol-q1-b': ('chem-2021-ol-q1-b-fig', 'Duplicated chem-2021-ol-q1-b-fig (both cited Q1(b)).'),
    'chem-2021-ol-q1-c-ii': (
        'chem-2021-ol-q1-c-fig',
        'The scheme prices Q1(c)(i)-(ii) with one cell ([6 + 3]), so they are one task; carded '
        'once, as chem-2021-ol-q1-c-fig.'),
    'chem-2021-ol-q2-d-i': (
        'chem-2021-ol-q2-d-i-fig', 'Duplicated chem-2021-ol-q2-d-i-fig (both cited Q2(d)(i)).'),
    'chem-2021-ol-q6-b': ('chem-2021-ol-q6-bc-fig', 'Duplicated chem-2021-ol-q6-bc-fig (both cited Q6(b)).'),
    'chem-2021-ol-q9-abd-fig': (
        'chem-2021-ol-q9-a',
        'Joined Q9(a), (b)(ii) and (d), which the scheme prices with separate cells; each is '
        'carded on its own, and Q9(a) as chem-2021-ol-q9-a.'),
    'chem-2021-ol-q10-a-2': ('chem-2021-ol-q10-a-1', 'Duplicated chem-2021-ol-q10-a-1 (both cited Q10(a)).'),
    'chem-2021-ol-q11-c-i': ('chem-2021-ol-q11c-fig', 'Duplicated chem-2021-ol-q11c-fig (both cited Q11(c)(i)).'),
    'chem-2021-ol-q11-d-b-i': (
        'chem-2021-ol-q11d-b-fig', 'Duplicated chem-2021-ol-q11d-b-fig (both cited Q11(d)B(i)).'),
}

# ── Q1 Ethyne from calcium carbide ───────────────────────────────────────────
Q1 = FIG + 'paper-q1'
C.ordered([k('1', 'a', 'i'), k('1', 'a', 'ii')], None, None, cid='q1-a-fig', figure=Q1)
C.fixed([k('1', 'b')], None, None, cid='q1-b-fig', figure=Q1)
C.ordered([k('1', 'c', 'i'), k('1', 'c', 'ii')], None, None, cid='q1-c-fig', figure=Q1)
C.fixed([k('1', 'd', 'i')], None, None, figure=Q1)
print_question('paper-q1d-i-print')
C.fixed([k('1', 'd', 'ii')], None, None, figure=Q1)
C.menu([k('1', 'e')], None, None, figure=Q1)

# ── Q2 A titration, and a pure sample of salt ────────────────────────────────
Q2 = FIG + 'paper-q2'
C.fixed([k('2', 'a', 'i')], None, None, cid='q2-a-i-fig', figure=Q2)
C.fixed([k('2', 'a', 'ii')], None, None, cid='q2-a-ii-fig', figure=Q2)
C.fixed([k('2', 'a', 'iii')], None, None, figure=Q2)
C.fixed([k('2', 'b', 'i')], 'chem-4-1', 'indicator-for-an-acid-base-titration', cid='q2-b')
_q2b2 = P.items(k('2', 'b', 'ii'))
assert [it.cell for it in _q2b2] == ['[2 × 3]', None], _q2b2
C.fixed([k('2', 'b', 'ii')], 'chem-4-1', 'colour-change-observed-end-point-using',
        row_notes={1: 'The scheme adds: ' + ' '.join(_q2b2[1].asides)})
C.menu([k('2', 'b', 'iii')], None, None)
# (c): the answer (9), then two routes of three steps (3) each, the first set
# wholly as fractions; the steps here are the second route's.
_q2c = P.items(k('2', 'c'))
assert _q2c[0].cell == '[9]', _q2c
C.add([k('2', 'c')], None, None, [
    C.lifted('r-1', '23.0 × 0.3 ÷ 1000 = 6.9 × 10⁻³ moles HCl', 3, FRACTION.format('23.0 × 0.3', '1000')),
    C.lifted('r-2', '6.9 × 10⁻³ × 1 = 6.9 × 10⁻³ moles NaOH', 3),
    C.lifted('r-3', 'M = 6.9 × 10⁻³ × 1000 ÷ 25.0 = 0.276 mol l⁻¹', 3,
             FRACTION.format('6.9 × 10⁻³ × 1000', '25.0'))],
    total=9, figure=S + 'q2c',
    notes='The scheme gives the answer, 0.276 moles per litre NaOH, priced [9], then the working '
          'that earns it in two routes; the steps here are its second route, and its own print of '
          'both, with its note that the formula may be awarded 3 if the first 6 are not, is shown '
          'with the answer.')
C.fixed([k('2', 'd', 'i')], None, None, cid='q2-d-i-fig', figure=Q2)
C.route([k('2', 'd', 'ii')], None, None)

# ── Q3 The heat of neutralisation ────────────────────────────────────────────
Q3T = FIG + 'paper-q3-table'
C.fixed([k('3', 'a')], None, None, figure=S + 'q3a')
print_question('paper-q3a-print')
C.fixed([k('3', 'b', 'i')], None, None, figure=Q3T)
C.fixed([k('3', 'b', 'ii')], None, None, figure=Q3T)
C.fixed([k('3', 'c')], None, None, figure=FIG + 'paper-q3-cup')
Q3D = FIG + 'paper-q3d'
C.fixed([k('3', 'd', 'i')], 'chem-u2', 'hazard-shown-by-a-pictogram', cid='q3-d-fig', figure=Q3D)
C.fixed([k('3', 'd', 'ii')], None, None, figure=Q3D)
C.route([k('3', 'e')], None, None,
        fixes={'5.7 0.1 =': '5.7 ÷ 0.1 ='}, row_notes={0: FRACTION.format('5.7', '0.1')})
C.cards[-1]['figureKey'] = Q3T      # the stimulus, not the scheme's working

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'b')], None, None, notes=Q4_NOTE)
print_question('paper-q4b-print')
C.fixed([k('4', 'c')], None, None, notes=Q4_NOTE, figure=FIG + 'paper-q4c')
for letter in ('d', 'e'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'f', 'i')], 'chem-1-1', 'state-in-which-molecules-move-fastest', cid='q4-f',
        notes=Q4_NOTE)
C.fixed([k('4', 'f', 'ii')], 'chem-1-1', 'only-vibrate-about-fixed-positions', notes=Q4_NOTE)
for letter in ('g', 'h'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.route([k('4', 'i')], None, None, notes=Q4_NOTE)
for letter in ('j', 'k'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'A')], None, None, notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'B')], None, None, notes=Q4_NOTE)

# ── Q5 Electronegativity and bonding ─────────────────────────────────────────
C.fixed([k('5', 'a', 'i')], None, None)
C.fixed([k('5', 'a', 'ii')], None, None)
C.fixed([k('5', 'b')], None, None)
# (i) and (ii) are one word each ("oxygen."); each card's question is the
# letter's lead and its own ask, as printed.
Q5C = C.context(k('5', 'c', 'i'))
_at = Q5C.index('Write down the arrangement')
Q5C_STEM, Q5C_LEAD = Q5C[:_at].strip(), Q5C[_at:]
C.fixed([k('5', 'c', 'i')], 'chem-1-2', 'electron-arrangement-of-beryllium', cid='q5-c',
        stem=Q5C_STEM, qtext=Q5C_LEAD + ' ' + P.ask(k('5', 'c', 'i')))
C.fixed([k('5', 'c', 'ii')], 'chem-1-2', 'electron-arrangement-of-oxygen',
        stem=Q5C_STEM, qtext=Q5C_LEAD + ' ' + P.ask(k('5', 'c', 'ii')))
# (c)(iii): two pairs of points, the second with "or" before it, each pair
# priced (2 × 3); the scheme draws the ions two ways above them.
_q5c3 = P.items(k('5', 'c', 'iii'))
assert [it.cell for it in _q5c3] == ['[2 × 3]', '[2 × 3]'], _q5c3
_p1 = _q5c3[0].points()
assert len(_p1) == 2, _p1
C.add([k('5', 'c', 'iii')], None, None, [
    C.lifted('r-1', _p1[0], 3,
             'The scheme draws the ions with their electron shells, or writes Be²⁺ beside O²⁻ with '
             'its eight outer electrons as dots; its own print is shown with the answer. It prices '
             'this point and the next (2 × 3), one each, or instead the pair "outer two electrons '
             'transferred from beryllium atom / Be²⁺ // to an (one) oxygen atom / O²⁻" (2 × 3).'),
    C.lifted('r-2', _p1[1], 3, 'The scheme adds: ' + ' '.join(_q5c3[1].asides))],
    figure=S + 'q5c-iii')
C.fixed([k('5', 'd', 'i')], None, None)
print_question('paper-q5d-i-print')
C.fixed([k('5', 'd', 'ii')], None, None, figure=S + 'q5d-ii',
        row_notes={0: 'The scheme draws the dot and cross diagram two ways; its own print is shown '
                      'with the answer.'})
C.fixed([k('5', 'd', 'iii')], None, None)

# ── Q6 Crude oil ─────────────────────────────────────────────────────────────
Q6 = FIG + 'paper-q6'
C.fixed([k('6', 'a')], None, None)
print_question('paper-q6a-print')
C.fixed([k('6', 'b')], None, None, cid='q6-bc-fig', figure=Q6)
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'where-the-fewest-carbon-atoms-collect', cid='q6-c', figure=Q6)
C.fixed([k('6', 'c', 'ii')], 'chem-2-4', 'highest-boiling-points', figure=Q6)
C.ordered([k('6', 'd', 'i'), k('6', 'd', 'ii')], None, None, cid='q6-d', figure=Q6)
for r in ('i', 'ii', 'iii'):
    C.fixed([k('6', 'e', r)], None, None)

# ── Q7 Water treatment ───────────────────────────────────────────────────────
for r in ('i', 'ii'):
    C.fixed([k('7', 'a', r)], None, None)
C.route([k('7', 'a', 'iii')], None, None)
for r in ('iv', 'v'):
    C.fixed([k('7', 'a', r)], None, None)
for r in ('i', 'ii', 'iii', 'iv'):
    C.fixed([k('7', 'b', r)], None, None)

# ── Q8 Ethene and its reactions ──────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
C.fixed([k('8', 'a', 'i')], None, None, figure=Q8)
C.drawn([k('8', 'a', 'ii')], 'chem-2-2', 'structure-of-ethene', S + 'q8a-ii')
C.fixed([k('8', 'a', 'iii')], None, None, figure=Q8)
C.fixed([k('8', 'b', 'i')], None, None, figure=Q8)
C.fixed([k('8', 'b', 'ii')], None, None, figure=Q8)
C.fixed([k('8', 'c')], None, None, figure=Q8)
C.fixed([k('8', 'd')], None, None, figure=Q8)
# (e): "contains a benzene ring" for (i) and the drawing for (ii), priced
# together (6 + 5).
C.ordered([k('8', 'e', 'i'), k('8', 'e', 'ii')], 'chem-2-4', 'aromatic-compound-and-benzene-structure',
          cid='q8-e-i', drawn=(k('8', 'e', 'ii'),), figure=S + 'q8e')
print_question('paper-q8e-print')

# ── Q9 The rate of a reaction ────────────────────────────────────────────────
Q9 = FIG + 'paper-q9'
_q9a = P.items(k('9', 'a'))
assert _q9a[0].cell == '[6]', _q9a
C.add([k('9', 'a')], None, None, [C.lifted(
    'r-1', 'change in concentration per unit time (rate of change of concentration) of one '
           'reactant or product', 6,
    'The scheme also accepts the change in concentration over time written as a fraction; its own '
    'print is shown with the answer.')], figure=S + 'q9a')
C.fixed([k('9', 'b', 'i')], None, None, figure=S + 'q9b-i')
print_question('paper-q9b-i-print')
C.fixed([k('9', 'b', 'ii')], None, None, figure=Q9)
C.fixed([k('9', 'c', 'i')], 'chem-3-2', 'total-volume-of-gas-from-a-graph', cid='q9-c', figure=Q9)
C.fixed([k('9', 'c', 'ii')], 'chem-3-2', 'time-taken-produce-half-volume-hydrogen', figure=Q9)
C.route([k('9', 'c', 'iii')], 'chem-3-2', 'average-rate-reaction-over-first-minutes')
C.cards[-1]['figureKey'] = Q9       # the stimulus, not the scheme's working
C.ordered([k('9', 'd', 'i'), k('9', 'd', 'ii')], 'chem-3-2', 'factors-affecting-the-initial-rate',
          figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.ordered([k('10', 'a')], None, None, cid='q10-a-1')
# (b): the paper sets (i) and (ii) inside one sentence; the scheme prices them
# together (4 + 3). The cell's equation's subscripts sit on the line.
_q10b = P.rearranged(P.ask(k('10', 'b')), 'H2O (l) → H2 (g) + ½O2 (g)', 'H₂O (l) → H₂ (g) + ½O₂ (g)')
_at = _q10b.index('Define (i)')
Q10B_STEM, Q10B_ASK = _q10b[:_at].strip(), _q10b[_at:]
_q10b12 = [P.items(k('10', 'b', r)) for r in ('i', 'ii')]
assert [it.cell for it in _q10b12[0]] == [None] and [it.cell for it in _q10b12[1]] == ['[4 + 3]'], \
    _q10b12
Q10B = FIG + 'paper-q10b'
C.add([k('10', 'b', 'i'), k('10', 'b', 'ii')], 'chem-3-5', 'oxidation-reduction-electron-definitions', [
    C.lifted('r-1', _q10b12[0][0].text, None, 'For (i).'),
    C.lifted('r-2', _q10b12[1][0].text, None, 'For (ii).')],
    kind='orderedSplit', notation='[4 + 3]', total=7, cid='q10-b-i-ii', stem=Q10B_STEM,
    qtext=Q10B_ASK, figure=Q10B, notes=SPLIT.format('[4 + 3]'))
C.fixed([k('10', 'b', 'iii')], None, None, stem=Q10B_STEM, figure=Q10B)
C.fixed([k('10', 'b', 'iv')], None, None, stem=Q10B_STEM, figure=Q10B)
C.fixed([k('10', 'b', 'v')], None, None, cid='q10-b-v-fig', stem=Q10B_STEM, figure=Q10B)
# (c): the catalyst and temperature are printed over and under the arrow.
Q10C = P.rearranged(C.context(k('10', 'c', 'i')),
                    'catalyst 4NH₂CONH₂ + 6NO₂ → 7N₂ + 8H₂O + 4CO₂ 400 ⁰C',
                    '4NH₂CONH₂ + 6NO₂ → 7N₂ + 8H₂O + 4CO₂ catalyst 400 ⁰C')
C.fixed([k('10', 'c', 'i')], None, None, stem=Q10C)
_q10c2 = P.items(k('10', 'c', 'ii'))
assert [it.cell for it in _q10c2] == ['[6]', '[6]', '[3]', '[3]'], _q10c2
C.add([k('10', 'c', 'ii')], None, None, [
    C.lifted('r-1', _q10c2[0].text, 6),
    C.lifted('r-2', _q10c2[1].text, 6,
             'The scheme sets out the working, n = m over Ar = 1620 over 60 (3), = 27 moles urea (3); '
             'its own print is shown with the answer.')],
    stem=Q10C, figure=S + 'q10c-ii')
_q10c3 = P.items(k('10', 'c', 'iii'))
assert [it.cell for it in _q10c3] == ['[3]', '[3]', '[4]', '[2]', '[2]'], _q10c3
C.add([k('10', 'c', 'iii')], None, None, [
    C.lifted('r-1', _q10c3[0].text, 3,
             'The scheme sets out the working, 4 moles urea ⇒ 6 moles NO₂, 1 mole urea ⇒ 1.5 or 6/4 '
             'or 3/2 moles NO₂ (3).'),
    C.lifted('r-2', _q10c3[2].text, 4,
             'The scheme adds: ' + ' '.join(_q10c3[2].asides) + ' It sets out the working, 1.5 × 22.4 '
             '(2) = 33.6 litres NO₂ (2); its own print is shown with the answer.')],
    stem=Q10C, figure=S + 'q10c-iii')

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.ordered([k('11', 'a', 'i'), k('11', 'a', 'ii')], None, None, cid='q11-a-i-ii')
for r in ('iii', 'iv', 'v'):
    C.fixed([k('11', 'a', r)], None, None)
# (b): the equilibrium's subscripts and charges sit on the line.
Q11B = P.rearranged(C.context(k('11', 'b', 'i')), 'H2CO3 (aq) + CO32– (aq) ⇌ 2HCO3– (aq)',
                    'H₂CO₃ (aq) + CO₃²⁻ (aq) ⇌ 2HCO₃⁻ (aq)')
# (i): two pairs of points with "or" between them, priced (4 + 3); below them
# the text layer reads (ii)'s Kc numerator.
_q11b1 = P.items(k('11', 'b', 'i'))
assert [it.cell for it in _q11b1] == ['[4 + 3]', None], _q11b1
C.add([k('11', 'b', 'i')], None, None, [
    C.lifted('r-1', 'state where forward and reverse reactions', None,
             'The scheme prices this point and the next together (4 + 3), or instead the pair '
             '"state where concentrations of reactants and products // are constant".'),
    C.lifted('r-2', 'have equal rates', None)],
    kind='orderedSplit', notation='[4 + 3]', total=7, stem=Q11B, notes=SPLIT.format('[4 + 3]'))
C.drawn([k('11', 'b', 'ii')], None, None, S + 'q11b-ii', stem=Q11B)
C.fixed([k('11', 'b', 'iii')], None, None, stem=Q11B)
C.fixed([k('11', 'b', 'iv')], None, None,
        stem=P.rearranged(C.context(k('11', 'b', 'iv')), 'H2CO3 (aq) + CO32– (aq) ⇌ 2HCO3– (aq)',
                          'H₂CO₃ (aq) + CO₃²⁻ (aq) ⇌ 2HCO₃⁻ (aq)'))
Q11C = FIG + 'paper-q11c'
C.fixed([k('11', 'c', 'i')], 'chem-u2', 'why-the-crucible-lid-is-raised', cid='q11c-fig', figure=Q11C)
_q11c2 = P.items(k('11', 'c', 'ii'))
assert [it.cell for it in _q11c2] == ['[9]', '[2 × 3]'], _q11c2
C.add([k('11', 'c', 'ii')], None, None, [
    C.lifted('r-1', _q11c2[0].text, 9,
             'Or instead, (2 × 3), "' + _q11c2[1].text + '".')], figure=Q11C)
C.fixed([k('11', 'c', 'iii')], None, None, figure=Q11C)
C.fixed([k('11', 'c', 'iv')], None, None, figure=Q11C)
C.fixed([ka('11', 'd', 'i', 'A')], 'chem-u3', 'most-abundant-element-in-air')
for r in ('ii', 'iii', 'iv', 'v'):
    C.fixed([ka('11', 'd', r, 'A')], None, None)
Q11DB = FIG + 'paper-q11d-b'
C.fixed([ka('11', 'd', 'i', 'B')], 'chem-1-3', 'general-property-of-transition-elements',
        cid='q11d-b-fig', figure=Q11DB)
C.fixed([ka('11', 'd', 'ii', 'B')], 'chem-u3', 'what-is-added-to-reduce-iron-ore', figure=Q11DB)
_q11db3 = P.items(ka('11', 'd', 'iii', 'B'))
assert [it.cell for it in _q11db3] == ['[6 + 3]'], _q11db3
_slag, _use = 'slag / calcium silicate (CaSiO₄)', 'roadmaking (hardcore) / lightweight building blocks / cement making'
assert display(_q11db3[0].text) == display(_slag + ' ' + _use), _q11db3[0].text
C.add([ka('11', 'd', 'iii', 'B')], None, None, [
    C.lifted('r-1', _slag, None), C.lifted('r-2', _use, None)],
    kind='orderedSplit', notation='[6 + 3]', total=9, figure=Q11DB, notes=SPLIT.format('[6 + 3]'))
C.fixed([ka('11', 'd', 'iv', 'B')], 'chem-u3', 'main-impurity-pig-iron-whose-concentration',
        figure=Q11DB)


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for key, (got, want) in sorted(C.letter_totals().items(),
                                   key=lambda kv: (int(kv[0][0]), kv[0][1])):
        out.append(f'Q{key[0]}({key[1]}) printed {want}, carded {got}')
    return '\n'.join(out)


if __name__ == '__main__':
    problems = make_audit(MAX_OPTIONS)(C.cards)
    for p in problems:
        print('AUDIT', p, file=sys.stderr)
    if '--review' in sys.argv:
        print(review())
    else:
        print(json.dumps(C.finish(), ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)
