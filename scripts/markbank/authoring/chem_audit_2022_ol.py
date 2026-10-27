#!/usr/bin/env python3
"""2022 Ordinary Level Chemistry, re-carded part by part from the paper and the labelled scheme.

    python3 scripts/markbank/authoring/chem_audit_2022_ol.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2022_ol.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2022 ol    # write them

Drafted by chem_draft.py and corrected card by card, the way
chem_audit_2023_ol.py re-cards 2023 OL. The 2022 Ordinary scheme labels its
letter-level cells with their count of points ("SIX POINTS: [11 + 6 + 6 + 2 +
2 + 2]", "ANY THREE: [6 + 4 + 2]"); a letter priced by one such cell is one
orderedSplit card.

Pre-audit ids are kept (a card that joined parts priced by separate cells
keeps its id on its first part; later parts are new cards); WITHDRAWN lists the
pre-audit cards that duplicated another or held a piece of a task the scheme
prices as one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import routed  # noqa: E402
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, anyN, point  # noqa: E402

P = Printed(2022, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2022-OL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'
SPLIT = ('The scheme prices these points together as {} without saying which point earns which '
         'part, so no per-point value is shown.')


def k(*parts):
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {
    'chem-2022-ol-q1-a-ii-iii': (
        'chem-2022-ol-q1-a',
        'The scheme prices Q1(a)(i)-(iii) with one cell ([11 + 6 + 6 + 2 + 2 + 2]), so they are '
        'one task; carded once, as chem-2022-ol-q1-a.'),
    'chem-2022-ol-q7-b-2': (
        'chem-2022-ol-q7-b-1',
        'Duplicated chem-2022-ol-q7-b-1 (both cited Q7(b), which the scheme prices with one cell, '
        '(4 × 6) + (3 × 2)).'),
}

# ── Q1 Ethene, and the oxidation of phenylmethanol ───────────────────────────
Q1A = FIG + 'paper-p02-i1'
Q1B = FIG + 'paper-p02-i0'
C.ordered([k('1', 'a', 'i'), k('1', 'a', 'ii'), k('1', 'a', 'iii')], 'chem-u2',
          'preparing-and-testing-ethene', cid='q1-a', figure=S + 'q1a-i',
          fixes={'shake (mix, bubble into, add, use) with bromine (Br₂) solution (water) / shake '
                 '(mix, bubble into, add, use) with acidified potassium permanganate {manganate(VII)} '
                 'solution (H⁺/KMnO₄ or H⁺/MnO₄⁻) brown (red, orange, yellow, pink, purple) colour':
                 'shake (mix, bubble into, add, use) with bromine (Br₂) solution (water) / shake '
                 '(mix, bubble into, add, use) with acidified potassium permanganate {manganate(VII)} '
                 'solution (H⁺/KMnO₄ or H⁺/MnO₄⁻)',
                 'disappears (decolourises, fades)':
                 'brown (red, orange, yellow, pink, purple) colour disappears (decolourises, fades)'})
# (i) asks for the paper's diagram to be completed, and the card's figure is the
# scheme's completed drawing: the question picture is the paper's own print.
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q1a-print'
C.ordered([k('1', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v', 'vi')], None, None, cid='q1-b',
          figure=Q1B)

# ── Q2 A standard solution of sodium carbonate ───────────────────────────────
C.fixed([k('2', 'a')], None, None)
C.menu([k('2', 'b')], None, None)
C.route([k('2', 'c', 'i')], 'chem-4-1', 'mass-of-005-moles-of-sodium-carbonate', cid='q2-c')
C.answer_only([k('2', 'c', 'ii')], 'chem-4-1', 'mass-of-sodium-carbonate-for-250-cm3',
              S + 'q2c-ii')
C.fixed([k('2', 'd')], None, None)
C.fixed([k('2', 'e', 'i')], 'chem-4-1', 'indicator-for-carbonate-titration', cid='q2-e')
C.fixed([k('2', 'e', 'ii')], 'chem-4-1', 'methyl-orange-colour-change-at-end-point')
C.answer_only([k('2', 'f')], None, None, S + 'q2f')

# ── Q3 Decomposition of hydrogen peroxide ────────────────────────────────────
Q3 = FIG + 'paper-p04-i0'
# Q3(a): one point each for (i) and (ii), and for (iii) two points, given as
# three pairs with "or" between them; the four priced [9 + 5 + 2 + 2].
_q3a = [P.items(k('3', 'a', r)) for r in ('i', 'ii', 'iii')]
assert [it.cell for it in _q3a[2]] == ['[9 + 5 + 2 + 2]'], _q3a
C.add([k('3', 'a', 'i'), k('3', 'a', 'ii'), k('3', 'a', 'iii')], None, None, [
    C.lifted('r-1', _q3a[0][0].text, None, 'The scheme adds: [Apply (–2) for manganese oxide.]'),
    C.lifted('r-2', _q3a[1][0].text, None),
    # Three pairs for (iii), "or" between them, priced together: each point accepts its
    # counterparts in the other pairs (an unpriced card cannot take routes).
    C.accepting(C.lifted('r-3', 'catalyst initially in neck of flask lying on its side', None,
                         'The scheme gives this point and the next as one of three pairs, with "or" between them; '
                         'claim both points from the same pair. Its own print is shown with the answer.'),
                'catalyst and peroxide initially separated using small test tube', 'open (replace, insert) stopper'),
    C.accepting(C.lifted('r-4', 'rotate flask so combine catalyst with solution', None),
                'disturb to mix catalyst and solution', 'add catalyst quickly')],
    kind='orderedSplit', notation='[9 + 5 + 2 + 2]', total=18, cid='q3-a', figure=S + 'q3a-iii',
    notes=SPLIT.format('[9 + 5 + 2 + 2]'))
# Its only figure is the scheme's drawing, held back until the reveal, while the lead-in's last
# sentence ends "using the apparatus shown below", and (iii) turns on that apparatus (the catalyst
# added to the flask without losing oxygen through the tubing). The paper's own print is the
# question: the lead-in with the apparatus, then (a) ((a)'s mark "(18)" left out).
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q3a-print'
C.fixed([k('3', 'b', 'i')], None, None, figure=Q3)
C.fixed([k('3', 'b', 'ii')], None, None, figure=Q3)
C.route([k('3', 'b', 'iii')], None, None, figure=Q3)
C.ordered([k('3', 'c')], None, None, figure=Q3)

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'b', 'i'), k('4', 'b', 'ii')], None, None, cid='q4-b', notes=Q4_NOTE)
C.fixed([k('4', 'c')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'd')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'e')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'f')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'g')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'h')], None, None, notes=Q4_NOTE)
C.route([k('4', 'i')], None, None, figure=S + 'q4i', notes=Q4_NOTE,
        fixes={'% Co = 177 × 100 = 33% 59': '% Co = 59 ÷ 177 × 100 = 33%'},
        row_notes={1: FRACTION.format('59', '177')})
C.fixed([k('4', 'j')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'k')], None, None, figure='chemistry-2022-ol-paper-p006-i0', notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'A')], None, None, cid='q4-l-a', notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'B')], None, None, cid='q4-l-b', notes=Q4_NOTE)

# ── Q5 Bonding ───────────────────────────────────────────────────────────────
C.fixed([k('5', 'a', 'i')], 'chem-2-1', 'ionic-bonding-from-electron-transfer', cid='q5-a')
C.fixed([k('5', 'a', 'ii')], 'chem-2-1', 'covalent-bonding-from-shared-electrons')
# (iii)-(iv) are led by "When two hydrogen atoms join to form a H₂ molecule,", not
# by (i)-(ii)'s "Identify the type of bonding that arises".
Q5A3 = C.context(k('5', 'a', 'iii')).replace('Identify the type of bonding that arises ', '')
C.fixed([k('5', 'a', 'iii')], 'chem-2-1', 'whether-h-atoms-in-h2-reach-a-noble-gas-arrangement',
        stem=Q5A3)
C.fixed([k('5', 'a', 'iv')], 'chem-2-1', 'whether-the-octet-rule-holds-in-h2', stem=Q5A3)
C.fixed([k('5', 'b')], None, None)
# (i) and (ii) are one word each ("sodium,"); each card's question is the
# letter's lead and its own ask, as printed.
Q5C = C.context(k('5', 'c', 'i'))
_at = Q5C.index('Write down the arrangement')
Q5C_STEM, Q5C_LEAD = Q5C[:_at].strip(), Q5C[_at:]
C.fixed([k('5', 'c', 'i')], 'chem-1-2', 'electron-arrangement-of-sodium', cid='q5-c-i-ii',
        stem=Q5C_STEM, qtext=Q5C_LEAD + ' ' + P.ask(k('5', 'c', 'i')))
C.fixed([k('5', 'c', 'ii')], 'chem-1-2', 'electron-arrangement-of-fluorine',
        stem=Q5C_STEM, qtext=Q5C_LEAD + ' ' + P.ask(k('5', 'c', 'ii')))
C.fixed([k('5', 'c', 'iii')], None, None)
# Q5(c)(iv): the worded point (3), or a diagram of the ions (3).
_q5c4 = P.items(k('5', 'c', 'iv'))
assert [it.cell for it in _q5c4] == ['[3]', '[3]'], _q5c4
C.add([k('5', 'c', 'iv')], None, None, [
    C.lifted('r-1', _q5c4[0].text, 3,
             'Or instead, priced the same, the dot and cross diagrams the scheme draws: '
             '"diagram showing sodium ion with no electrons in third shell and fluoride ion with '
             '8 electrons in outer shell"; its own print is shown with the answer.')],
    figure=S + 'q5c-iv')
C.ordered([k('5', 'd', 'i'), k('5', 'd', 'ii')], None, None, cid='q5-d', figure=FIG + 'paper-p07-i0')

# ── Q6 Hydrocarbons A to E ───────────────────────────────────────────────────
Q6 = FIG + 'paper-q6-fig0'
C.fixed([k('6', 'a')], None, None, figure=Q6)
C.ordered([k('6', 'b')], 'chem-2-4', 'iupac-names-of-ethane-ethyne-and-methylbenzene', figure=Q6)
C.menu([k('6', 'c', 'i')], 'chem-2-4', 'which-hydrocarbons-are-gases-at-room-temperature',
       figure=Q6)
C.ordered([k('6', 'c', 'ii')], None, None, figure=Q6)
C.ordered([k('6', 'd', 'i'), k('6', 'd', 'ii')], 'chem-2-4', 'industrial-uses-of-ethyne-and-ethene',
          figure=Q6)
# Q6(e): the products (2 × 3) and the balanced equation (3).
_q6e = P.items(k('6', 'e'))
assert [it.cell for it in _q6e] == ['[3]'], _q6e
C.add([k('6', 'e')], None, None, [
    C.lifted('r-1', 'CO₂', 3, 'The scheme prices the two products (2 × 3), one each.'),
    C.lifted('r-2', 'H₂O', 3),
    C.lifted('r-3', 'C₂H₂ + 2½O₂ → 2CO₂ + H₂O / 2C₂H₂ + 5O₂ → 4CO₂ + 2H₂O', 3,
             'The scheme prices the balancing (3).')],
    figure=Q6)
C.drawn([k('6', 'f', 'i')], 'chem-2-4', 'structure-of-propene', S + 'q6f-i')
C.drawn([k('6', 'f', 'ii')], 'chem-2-4', 'tetrahedral-carbon-in-propene', S + 'q6f-ii')

# ── Q7 Acids, bases and pH ───────────────────────────────────────────────────
# Q7(a): the paper sets (i) and (ii) inside one sentence; the scheme answers
# each under its own marker and prices them together [5 + 3].
_q7a = [P.items(k('7', 'a', r)) for r in ('i', 'ii')]
assert [it.cell for it in _q7a[1]] == ['[5 + 3]'], _q7a
C.add([k('7', 'a', 'i'), k('7', 'a', 'ii')], None, None, [
    C.lifted('r-1', _q7a[0][0].text, None, 'For (i).'),
    C.lifted('r-2', _q7a[1][0].text, None, 'For (ii).')],
    kind='orderedSplit', notation='[5 + 3]', total=8, cid='q7-a-i-ii',
    qtext=P.ask(k('7', 'a')), stem='', notes=SPLIT.format('[5 + 3]'))
# (iii) and (iv) are not led by (a)'s own asks; (iv) by the dilution it follows.
Q7A4 = C.context(k('7', 'a', 'iv'))
Q7A4 = Q7A4[Q7A4.index('A 0.03 M HCl'):]
C.fixed([k('7', 'a', 'iii')], None, None, stem='')
C.route([k('7', 'a', 'iv')], None, None, stem=Q7A4)
# Q7(b): the letters A to G, priced (4 × 6) + (3 × 2).
_q7b = P.items(k('7', 'b'))
_q7bp = [x.strip() for x in _q7b[0].text.split('//')]
assert len(_q7bp) == 7 and _q7bp[-1].startswith('G decreases'), _q7bp
_q7bp[-1] = 'G decreases'
C.add([k('7', 'b')], None, None, [C.lifted(f'r-{i + 1}', t, None) for i, t in enumerate(_q7bp)],
      kind='orderedSplit', notation='[(4 × 6) + (3 × 2)]', total=30, cid='q7-b-1',
      notes=SPLIT.format('(4 × 6) + (3 × 2)'))

# ── Q8 From glucose to ethanoic acid ─────────────────────────────────────────
Q8 = FIG + 'paper-q8-fig0'
C.ordered([k('8', 'a', r) for r in ('i', 'ii', 'iii')], None, None, cid='q8-a', figure=Q8)
C.ordered([k('8', 'b', r) for r in ('i', 'ii', 'iii')], 'chem-4-2',
          'oxidation-of-ethanol-to-ethanal', cid='q8-b-i', figure=Q8)
C.ordered([k('8', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-4-2',
          'oxidation-of-ethanal-to-ethanoic-acid', cid='q8-c-i', figure=Q8)

# ── Q9 Sodium, flame tests and redox ─────────────────────────────────────────
# Q9(a): any three of the four steps the scheme tabulates for three methods.
_q9a_opts = [
    'clean a platinum (nichrome) wire* (rod, probe) in HCl (concentrated hydrochloric acid) / '
    'soak wood (splint, stick) overnight in water / use damp (wet) wood (splint, stick) / '
    'prepare a solution of the given salt',
    'dip wet rod in salt (sample) / dip** splint (stick) in salt (sample) / in water and ethanol '
    '(propanol)',
    'hold salt in or over hot (blue) part of Bunsen flame / spray salt solution onto (into) hot '
    '(blue) part of Bunsen flame',
    'yellow (amber, orange) colour confirms sodium salt']
C.add([k('9', 'a')], None, None, [anyN(
    'r-1', _q9a_opts[0], 12, 3, 6,
    [C.lifted('x', o, None)['verbatim'] for o in _q9a_opts],
    'The scheme sets these four steps in a table for three methods, the methods\' wordings of '
    'each step separated here by solidi, and prices any three steps [6 + 4 + 2]; its own print '
    'is shown with the answer. It adds: [*Allow ‘metal inoculating loop’, or ‘metal spatula’ for '
    '‘platinum (nichrome) wire’.] [**Method 2: ‘Soak splint (stick) in salt solution’ merits '
    'marks for two points.] [Clear labelled diagram for some or all points acceptable.]',
    steps=[6, 4, 2])], total=12, figure=S + 'q9a')
C.ordered([k('9', 'b', 'i'), k('9', 'b', 'ii')], None, None, cid='q9-b')
C.fixed([k('9', 'b', 'iii')], None, None)
C.ordered([k('9', 'c', r) for r in ('i', 'ii', 'iii')], None, None, cid='q9-c')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# The paper sets the hydrogen isotopes' mass and atomic numbers around their
# symbols; the text layer reads them on the line. The same characters, set as
# printed.
Q10A = P.rearranged(P.ask(k('10', 'a')), 'H 1, H 2, and H 3.1 1 1', '¹₁H, ²₁H, and ³₁H.')
_at = Q10A.index('What is meant by')
Q10A_STEM, Q10A_ASK = Q10A[:_at].strip(), Q10A[_at:]
_q10a = [P.items(k('10', 'a', r)) for r in ('i', 'ii', 'iii')]
assert [it.cell for it in _q10a[2]] == ['[6 + 3 + 2 + 1]'], _q10a
_p3 = _q10a[2][0].points()
C.add([k('10', 'a', 'i'), k('10', 'a', 'ii'), k('10', 'a', 'iii')], 'chem-1-2',
      'atomic-number-mass-number-isotopes', [
          C.lifted('r-1', _q10a[0][0].text, None,
                   'For (i). The scheme adds: [Allow number of electrons in a neutral atom]'),
          C.lifted('r-2', _q10a[1][0].text, None, 'For (ii).'),
          C.lifted('r-3', _p3[0], None, 'For (iii).'),
          C.lifted('r-4', _p3[1], None)],
      kind='orderedSplit', notation='[6 + 3 + 2 + 1]', total=12, cid='q10-a-i-iii',
      stem=Q10A_STEM, qtext=Q10A_ASK + ' (iii) ' + P.ask(k('10', 'a', 'iii')),
      notes=SPLIT.format('[6 + 3 + 2 + 1]'))
_q10a4 = P.rearranged(P.ask(k('10', 'a', 'iv')), 'H 1 and H 2 differ? 1 1', '¹₁H and ²₁H differ?')
_q10a6 = P.rearranged(P.ask(k('10', 'a', 'vi')),
                      '3 is radioactive and decays by emitting a beta particle. H 1',
                      '³₁H is radioactive and decays by emitting a beta particle.')
_q10b = [P.items(k('10', 'a', r)) for r in ('iv', 'v', 'vi')]
assert [it.cell for it in _q10b[2]] == ['[6 + 3 + 3 + 1]'], _q10b
_p5 = _q10b[1][0].points()
C.add([k('10', 'a', 'iv'), k('10', 'a', 'v'), k('10', 'a', 'vi')], 'chem-1-2',
      'hydrogen-isotopes-radioactivity-and-beta-particles', [
          C.lifted('r-1', 'no neutron (one nucleon) in H₁¹, one neutron (two nucleons) in H₁² / '
                          'differ by one neutron / one proton in H₁¹, one proton and one neutron '
                          'in H₁²', None,
                   'For (iv). The scheme sets the mass and atomic numbers beside each H.'),
          C.lifted('r-2', _p5[0], None, 'For (v).'),
          C.lifted('r-3', _p5[1], None, 'The scheme adds: [Allow decay of unstable atom but '
                                        'apply (–1)]'),
          C.lifted('r-4', _q10b[2][0].text, None, 'For (vi).')],
      kind='orderedSplit', notation='[6 + 3 + 3 + 1]', total=13, cid='q10-a-iv-vi', stem=Q10A_STEM,
      qtext=' '.join(['(iv) ' + _q10a4, '(v) ' + P.ask(k('10', 'a', 'v')), '(vi) ' + _q10a6]),
      notes=SPLIT.format('[6 + 3 + 3 + 1]'))
# Q10(b): the equilibrium's subscripts sit on the line in the text layer.
Q10B = P.rearranged(C.context(k('10', 'b', 'i')), 'N2O4 (g) ⇌ 2NO2 (g)', 'N₂O₄ (g) ⇌ 2NO₂ (g)')
# (i): two pairs of points with "or" between them, priced (2 × 3).
_q10b1 = P.items(k('10', 'b', 'i'))
assert [it.cell for it in _q10b1] == ['[2 × 3]'], _q10b1
# Two pairs, the second after "or", each (2 × 3): each a route.
C.add([k('10', 'b', 'i')], None, None, [
    routed(C.lifted('r-1', 'state where forward and reverse reactions', 3,
                    'The scheme prices this point and the next (2 × 3), one each, or instead the last two rows. '
                    'The examiner marks one pair or the other, not a mix.'), 'a'),
    routed(C.lifted('r-2', 'have equal rates', 3), 'a'),
    routed(C.lifted('r-3', 'state where concentrations of reactants and products', 3,
                    'Or instead, this point and the next (2 × 3), one each.'), 'b'),
    routed(C.lifted('r-4', 'are constant', 3), 'b')], total=6, stem=Q10B)
# (ii): one point (2); below it the text layer reads (iii)'s Kc numerator.
_q10b2 = P.items(k('10', 'b', 'ii'))
assert [it.cell for it in _q10b2] == ['[2]', None], _q10b2
C.add([k('10', 'b', 'ii')], None, None, [C.lifted('r-1', _q10b2[0].text, 2)], stem=Q10B)
C.drawn([k('10', 'b', 'iii')], 'chem-3-3', 'kc-expression-for-n2o4-and-no2', S + 'q10b-iii',
        stem=Q10B)
Q10B4 = C.context(k('10', 'b', 'iv'))
C.ordered([k('10', 'b', 'iv'), k('10', 'b', 'v')], None, None, cid='q10-b-iv-v',
          stem=P.rearranged(Q10B4, 'N2O4 (g) ⇌ 2NO2 (g)', 'N₂O₄ (g) ⇌ 2NO₂ (g)'))
C.route([k('10', 'c', 'i')], None, None, figure=S + 'q10c-i',
        fixes={'n = Mr⇒ m 5.4 32': 'n = m ÷ Mr ⇒ 5.4 ÷ 32'},
        row_notes={0: 'The scheme prints m over Mr and 5.4 over 32 as fractions; ÷ stands for '
                      'their bars.'})
C.route([k('10', 'c', 'ii')], None, None)
C.route([k('10', 'c', 'iii')], None, None)
C.route([k('10', 'c', 'iv')], None, None)
C.route([k('10', 'c', 'v')], None, None, figure=S + 'q10c-v',
        fixes={'Mr CO = 28 / n = Mr m': 'Mr CO = 28 / n = m ÷ Mr'},
        row_notes={0: FRACTION.format('m', 'Mr')})

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
Q11A = FIG + 'paper-q11a'
C.fixed([k('11', 'a', 'i')], None, None, figure=Q11A)
C.ordered([k('11', 'a', 'ii')], None, None, figure=Q11A)
C.ordered([k('11', 'a', r) for r in ('iii', 'iv', 'v')], None, None, cid='q11-a-iii-v',
          figure=Q11A)
C.fixed([k('11', 'b', 'i')], None, None)
C.fixed([k('11', 'b', 'ii')], None, None)
C.fixed([k('11', 'b', 'iii')], None, None, figure=FIG + 'paper-p12-i0')
# Q11(b)(iv) asks for the volume, priced as its answer (9) with the working
# beneath, and the law, priced (1).
_q11b4 = P.items(k('11', 'b', 'iv'))
assert [it.cell for it in _q11b4] == ['[9]', '[3]', '[3]', '[1]'], _q11b4
C.add([k('11', 'b', 'iv')], None, None, [
    C.lifted('r-1', _q11b4[0].text, 9,
             'The scheme prices the answer (9) and sets out the working that earns it, (3) for '
             'each step, with Kelvin essential; its own print is shown with the answer. It adds: '
             '[Allow 56.3 litres …6]'),
    C.lifted('r-2', _q11b4[3].text, 1)], figure=S + 'q11b-iv')
Q11C = FIG + 'paper-q11c'
for r in ('i', 'ii', 'iii', 'iv'):
    C.fixed([k('11', 'c', r)], None, None, figure=Q11C)
# (v)-(vi): the cue "LABEL X:" / "LABEL Y:" heads the answer.
C.fixed([k('11', 'c', 'v')], 'chem-4-3', 'component-most-strongly-adsorbed', figure=Q11C,
        fixes={'LABEL X: P: lowest (can include S) / T: lowest (can include S) / C: highest (can '
               'include top of column)': 'P: lowest (can include S) / T: lowest (can include S) / '
                                         'C: highest (can include top of column)'})
C.fixed([k('11', 'c', 'vi')], None, None, figure=Q11C,
        fixes={'LABEL Y: P: highest / T: highest / C: lowest': 'P: highest / T: highest / C: lowest'})
C.fixed([k('11', 'c', 'vii')], None, None, figure=Q11C)
C.ordered([ka('11', 'd', 'i', 'A'), ka('11', 'd', 'ii', 'A')], 'chem-u3',
          'batch-process-and-steel-reaction-vessels')
C.menu([ka('11', 'd', 'iii', 'A')], 'chem-u3', 'increasing-the-rate-of-production')
C.fixed([ka('11', 'd', 'iv', 'A')], 'chem-u3', 'what-happens-to-co-products')
C.fixed([ka('11', 'd', 'v', 'A')], 'chem-u3', 'recycling-solvent-and-unreacted-reagents')
C.ordered([ka('11', 'd', 'i', 'B')], None, None)
C.menu([ka('11', 'd', 'ii', 'B')], 'chem-1-1', 'properties-of-aluminium-for-food-wrapping')
C.drawn([ka('11', 'd', 'iii', 'B')], 'chem-4-2', 'structure-of-chloroethene', S + 'q11db-iii')
C.drawn([ka('11', 'd', 'iv', 'B')], 'chem-4-2', 'repeating-units-of-pvc', S + 'q11db-iv')


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
