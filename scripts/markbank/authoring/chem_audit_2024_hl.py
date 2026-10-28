#!/usr/bin/env python3
"""2024 Higher Level Chemistry, re-carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_audit_2024_hl.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2024_hl.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2024 hl    # write them

Drafted by chem_draft.py and corrected card by card, the way
chem_audit_2025_hl.py re-cards 2025: every question text, stem and lead-in is
the PAPER's print of its part; every marking point is the SCHEME's answer
closed by its own mark cell. Pre-audit ids are kept (a card that joined parts
priced by separate cells keeps its id on its first part; later parts are new
cards), and the pre-audit cards that duplicated another or held a piece of a
task the scheme prices as one are withdrawn with an alias (WITHDRAWN).

The 2024 Higher scheme reprints each part above its answer, as 2025's does.
Its Q4 labels answers with the part's romans again ("(i) 2 (ii) 1"), which
the reader takes as answer labels. The paper prints Q2(c)'s third part as a
second "(ii)"; the scheme marks it (iii), and so do the census and the card.

Where the scheme's text layer cannot carry a printed fraction, the one form of
the line it can is given as a fix, checked against the scheme by the
provenance gate's own normalisation, with a note saying ÷ stands for the bar;
where a line is set as a table or a picture (the ICE table in Q7(b)(ii), the
structures in Q2(c), Q6(c), Q8(c), the dot and cross diagram in Q11(a)), the
scheme's own print is the card's solution figure.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS  # noqa: E402

P = Printed(2024, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2024-HL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'


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

JOINED = ('The scheme prices {parts} with one cell ({cell}), so they are one task; carded '
          'once, as {new}.')
WITHDRAWN = {
    'chem-2024-hl-q6-a-iii': (
        'chem-2024-hl-q6-a-iii-fig',
        'Duplicated chem-2024-hl-q6-a-iii-fig (the same Q6(a)(iii), never built: the build '
        'keeps one card per citation).'),
    'chem-2024-hl-q6-b': (
        'chem-2024-hl-q6-b-fig',
        'Duplicated chem-2024-hl-q6-b-fig (the same Q6(b), never built). Q6(b)(i) is carded as '
        'chem-2024-hl-q6-b-fig, (ii) as -q6-b-ii.'),
    'chem-2024-hl-q10-b-iii-v': (
        'chem-2024-hl-q10-b-i-ii',
        JOINED.format(parts='Q10(b)(i)-(v)', cell='[6 + 3 + 2 + 2 + 2]',
                      new='chem-2024-hl-q10-b-i-ii')),
    'chem-2024-hl-q11-d-b-fig': (
        'chem-2024-hl-q11-db-i-iii',
        'Duplicated chem-2024-hl-q11-db-i-iii (both cited Q11(d)B(i)-(iii)). Each part is now a '
        'card of its own; Q11(d)B(i) is chem-2024-hl-q11-db-i-iii, and the blast furnace '
        'figure is on every Q11(d)B card.'),
}

# ── Q1 Ethanoic acid in vinegar by titration ─────────────────────────────────
for r in ('i', 'ii', 'iii'):
    C.fixed([k('1', 'a', r)], None, None)
C.fixed([k('1', 'b', 'i')], None, None)
C.fixed([k('1', 'b', 'ii')], None, None)
C.fixed([k('1', 'c', 'i')], None, None)
C.fixed([k('1', 'c', 'ii')], None, None)
C.fixed([k('1', 'd', 'i')], None, None, skip=('1000',),
        fixes={'0.09 × 25.0 = 0.00225 (moles)': '0.09 × 25.0 ÷ 1000 = 0.00225 (moles)'},
        row_notes={0: FRACTION.format('0.09 × 25.0', '1000')})
C.fixed([k('1', 'd', 'ii')], None, None)
C.fixed([k('1', 'd', 'iii')], None, None)
C.fixed([k('1', 'd', 'iv')], None, None, skip=('10',),
        fixes={'0.91 × 60 = 5.44 (%)': '0.91 × 60 ÷ 10 = 5.44 (%)'},
        row_notes={1: FRACTION.format('0.91 × 60', '10')})

# ── Q2 Recrystallisation, the oxidation of ethanal, soap ─────────────────────
Q2A = 'chemistry-2024-HL-paper-p03-i0'
C.fixed([k('2', 'a', 'i')], None, None)
C.fixed([k('2', 'a', 'ii')], None, None)
C.fixed([k('2', 'a', 'iii')], None, None, cid='q2-a-iii-fig', figure=Q2A)
C.fixed([k('2', 'a', 'iv')], None, None)
C.fixed([k('2', 'a', 'v')], None, None)
for r in ('i', 'ii', 'iii', 'iv'):
    C.fixed([k('2', 'b', r)], None, None)
C.fixed([k('2', 'c', 'i')], None, None)
C.fixed([k('2', 'c', 'ii')], None, None)
# The paper prints this part "(ii)" a second time; the scheme marks it (iii).
C.drawn_with([k('2', 'c', 'iii')], 'chem-4-2', 'glycerol-the-co-product-of-soap-making',
             S + 'q2c-iii',
             notes='The paper prints this part as a second (ii); the scheme marks it (iii).')

# ── Q3 Rate of the thiosulfate-acid reaction ─────────────────────────────────
Q3 = 'chemistry-2024-hl-paper-p004-i0'
Q3D = FIG + 'paper-q3d'
C.fixed([k('3', 'a', 'i')], None, None, figure=Q3)
C.fixed([k('3', 'a', 'ii')], None, None, figure=Q3)
C.fixed([k('3', 'b', 'i')], None, None, figure=Q3)
C.fixed([k('3', 'b', 'ii')], None, None, figure=Q3)
C.fixed([k('3', 'b', 'iii')], 'chem-3-2', 'what-the-rate-concentration-graph-shows', figure=Q3)
C.fixed([k('3', 'c', 'i')], None, None, figure=Q3)
C.fixed([k('3', 'c', 'ii')], None, None, figure=Q3,
        fixes={'0.003 = 333 (s) 1': '1 ÷ 0.003 = 333 (s)'},
        row_notes={0: FRACTION.format('1', '0.003')})
C.fixed([k('3', 'd', 'i')], None, None, figure=Q3D)
C.fixed([k('3', 'd', 'ii')], None, None, figure=Q3D)

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
C.ordered([k('4', 'a')], None, None, deep=True, notes=Q4_NOTE)
C.ordered([k('4', 'b')], None, None, notes=Q4_NOTE)
C.menu([k('4', 'c')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'd')], None, None, cid='q4-d-fig', figure='chemistry-2024-HL-paper-p05-i0',
          notes=Q4_NOTE,
          fixes={'2.4 × 4 32 = 0.3 (g)': '2.4 × 4 ÷ 32 = 0.3 (g)'},
          row_notes={1: FRACTION.format('2.4 × 4', '32')})
# Q4(e): the scheme sets both answers on one line, "(i) kJ mol⁻¹ / J mol⁻¹
# (ii) parts per million / ...", priced [4 + 2]; each is the line's own text.
_q4e = P.items(k('4', 'e', 'i'))
assert len(_q4e) == 1 and _q4e[0].cell == '[4 + 2]', _q4e
_e1, _e2 = _q4e[0].text.split(' (ii) ')
C.add([k('4', 'e', 'i'), k('4', 'e', 'ii')], None, None,
      [C.lifted('r-1', _e1, None), C.lifted('r-2', _e2, None)],
      kind='orderedSplit', notation='[4 + 2]', total=6, cid='q4-e',
      notes='The scheme prints the answers to (i) and (ii) on one line and prices them '
            'together as [4 + 2] without saying which point earns which part, so no per-point '
            'value is shown. ' + Q4_NOTE)
C.menu([k('4', 'f')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'g', 'i'), k('4', 'g', 'ii')], None, None, cid='q4-g', notes=Q4_NOTE)
C.ordered([k('4', 'h', 'i'), k('4', 'h', 'ii')], None, None, cid='q4-h', notes=Q4_NOTE)
C.ordered([k('4', 'i')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'j')], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'k')], None, None, cid='q4-k-fig', figure='chemistry-2024-HL-paper-p05-i1',
          notes=Q4_NOTE,
          fixes={'21.5 × 165 = 0.68, i.e. 68 (%) 2412.3': '2412.3 ÷ 21.5 × 165 = 0.68, i.e. 68 (%)'},
          row_notes={1: 'The scheme prints 2412.3 over 21.5 × 165 as a fraction; ÷ stands for '
                        'its bar.'})
C.menu([ka('4', 'l', None, 'A')], None, None, cid='q4-l-a', notes=Q4_NOTE)
C.ordered([ka('4', 'l', 'i', 'B'), ka('4', 'l', 'ii', 'B')], None, None, cid='q4-l-b',
          notes=Q4_NOTE)

# ── Q5 Bohr, Balmer and the electron ─────────────────────────────────────────
Q5 = 'chemistry-2024-hl-paper-p006-i0'
for r in ('i', 'ii', 'iii', 'iv'):
    C.fixed([k('5', 'a', r)], None, None, figure=Q5)
for r in ('i', 'ii', 'iii', 'iv', 'v'):
    C.fixed([k('5', 'b', r)], None, None, figure=Q5)
C.fixed([k('5', 'b', 'vi')], None, None, figure='chemistry-2024-HL-scheme-q5b-vi')

# ── Q6 Hydrocarbons A and B ──────────────────────────────────────────────────
Q6 = 'chemistry-2024-HL-paper-p07-i0'
C.fixed([k('6', 'a', 'i')], None, None, figure=Q6)
C.ordered([k('6', 'a', 'ii')], None, None, cid='q6-a-ii-fig', figure=Q6)
C.fixed([k('6', 'a', 'iii')], None, None, cid='q6-a-iii-fig', figure=Q6)
C.fixed([k('6', 'b', 'i')], 'chem-2-4', 'isomerisation-of-octane', cid='q6-b-fig', figure=Q6)
C.fixed([k('6', 'b', 'ii')], 'chem-2-4', 'why-isomerisation-is-carried-out', figure=Q6)
# Q6(c): the answers are the scheme's drawings, so a card's figure is the
# scheme's. Drawing methylpropane needs only (c)'s own lead-in; naming the
# isomers of C needs A's structure, so (c)(ii)'s question picture is the
# paper's own print: Q6's opening line and structures, (c)'s lead-in, (ii).
C.drawn([k('6', 'c', 'i')], 'chem-2-4', 'structure-of-methylpropane', S + 'q6c-i',
        stem=P.ask(k('6', 'c')))
C.drawn_with([k('6', 'c', 'ii')], 'chem-2-4', 'names-and-structures-of-butene-isomers',
             S + 'q6c-ii')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q6c-ii-print'
# Q6(d)(i): three working lines, each priced "(2 [multiplicative factor] + 1
# [sign])" beside it, then the answer [2].
PRICE = '(2 [multiplicative factor] + 1 [sign])'
_q6d = P.items(k('6', 'd', 'i'))
assert len(_q6d) == 1 and _q6d[0].cell == '[2]', _q6d
_rows = []
for row in _q6d[0].rows:
    head, sep, _ = row.text.partition(' ' + PRICE)
    if sep:
        _rows.append(C.lifted(f'r-{len(_rows) + 1}', head, 3,
                              f'The scheme prices this line {PRICE}.'))
    else:
        _rows.append(C.lifted(f'r-{len(_rows) + 1}', row.text, 2))
assert [r['marks'] for r in _rows] == [3, 3, 3, 2], _rows
C.add([k('6', 'd', 'i')], None, None, _rows, figure=Q6)
C.fixed([k('6', 'd', 'ii')], None, None, figure=Q6)

# ── Q7 Steam and carbon monoxide at equilibrium ──────────────────────────────
_q7 = P.ask(k('7'))
for old, new in [('H2O(g) + CO(g) ⇌ H2(g) + CO2(g)', 'H₂O(g) + CO(g) ⇌ H₂(g) + CO₂(g)')]:
    _q7 = P.rearranged(_q7, old, new)
C.fixed([k('7', 'a', 'i')], None, None, stem=_q7)
C.fixed([k('7', 'a', 'ii')], None, None, stem=_q7, figure=S + 'q7a-ii',
        fixes={'[H₂O][CO] [H₂] [CO₂]': '[H₂] [CO₂] ÷ [H₂O][CO]'},
        row_notes={0: "The scheme prints [H₂] [CO₂] over [H₂O][CO] as a fraction; ÷ stands for "
                      "its bar, and its own print is shown with the answer."})
C.fixed([k('7', 'a', 'iii')], None, None, stem=_q7,
        fixes={'[H₂O] = 3.2 V // [CO] = 0.2 V // [CO₂] = 0.8 V':
               '[H₂O] = 3.2 ÷ V // [CO] = 0.2 ÷ V // [CO₂] = 0.8 ÷ V',
               '0.8 × 0.8 3.2 × 0.2 = 1': '0.8 × 0.8 ÷ 3.2 × 0.2 = 1'},
        row_notes={0: 'The scheme prints each concentration as a fraction over V; ÷ stands for '
                      'each bar.',
                   1: 'The scheme prints 0.8 × 0.8 over 3.2 × 0.2 as a fraction; ÷ stands for '
                      'its bar.'})
C.fixed([k('7', 'b', 'i')], None, None, stem=_q7)
_q7b = P.items(k('7', 'b', 'ii'))
assert [it.cell for it in _q7b] == ['[3]', '[3]', '[2]', '[2]', '[2]'], _q7b
C.add([k('7', 'b', 'ii')], None, None, [
    C.lifted('r-1', 'equilibrium 2.5 – x 2.5 – x x x', 3,
             'The scheme sets this point as a table of moles under the equation, initially and '
             'at equilibrium; its own print is shown with the answer. The scheme adds: '
             + ' '.join(_q7b[0].asides)),
    C.lifted('r-2', 'x² ÷ (2.5 - x)² = 1', 3, FRACTION.format('x²', '(2.5 - x)²')),
    C.lifted('r-3', 'x = 1.25 (moles)', 2),
    C.lifted('r-4', 'Mr = 44', 2),
    C.lifted('r-5', 'mass = 55 g', 2)], stem=_q7, figure=S + 'q7b-ii')
for r in ('i', 'ii', 'iii'):
    C.fixed([k('7', 'c', r)], None, None, stem=_q7)

# ── Q8 Reactions of ethene; PVC ──────────────────────────────────────────────
Q8 = FIG + 'paper-q8-fig0'
C.fixed([k('8', 'a')], 'chem-2-2', 'geometry-change-when-ethene-becomes-ethane', figure=Q8)
C.fixed([k('8', 'b', 'i')], None, None, figure=Q8)
C.fixed([k('8', 'b', 'ii')], None, None, figure=Q8,
        fixes={'(propagation): C₂H₆ + Cl•) → ^(•C₂H₅ + HCl':
               '(propagation): C₂H₆ + Cl• → •C₂H₅ + HCl'},
        row_notes={1: 'The text layer reads the raised dot of •C₂H₅ out of place; the line is '
                      'given as the scheme prints it.'})
C.fixed([k('8', 'b', 'iii')], 'chem-4-2', 'butane-as-evidence-for-free-radicals',
        cid='q8-b-iii-iv', figure=Q8)
C.fixed([k('8', 'b', 'iv')], 'chem-4-2', 'other-evidence-for-a-free-radical-mechanism',
        figure=Q8)
C.fixed([k('8', 'c', 'i')], 'chem-4-2', 'naming-1-2-dichloroethane', cid='q8-c-i-ii', figure=Q8)
C.fixed([k('8', 'c', 'ii')], 'chem-4-2', 'hydrogen-chloride-eliminated', figure=Q8)
C.drawn_with([k('8', 'c', 'iii')], None, None, S + 'q8c-iii')
C.drawn_with([k('8', 'c', 'iv')], None, None, S + 'q8c-iv')
C.drawn([k('8', 'c', 'v')], 'chem-4-2', 'repeating-units-of-pvc', S + 'q8c-v')

# ── Q9 Acids and bases ───────────────────────────────────────────────────────
C.fixed([k('9', 'a', 'i')], None, None)
C.fixed([k('9', 'a', 'ii')], 'chem-3-4', 'conjugate-acid-of-ammonia', cid='q9-a-ii-iii')
C.fixed([k('9', 'a', 'iii')], 'chem-3-4', 'conjugate-base-of-ammonia')
for r in ('i', 'ii', 'iii'):
    C.fixed([k('9', 'b', r)], None, None)
C.fixed([k('9', 'b', 'iv')], None, None,
        fixes={'pH = –log₁₀(√KaMacid) / [H⁺] = √KaMacid / [H⁺] = 10–pH / √KaMacid = 0.00105':
               'pH = –log₁₀(√(KaMacid)) / [H⁺] = √(KaMacid) / [H⁺] = 10^–pH / √(KaMacid) = 0.00105'},
        row_notes={0: 'The scheme sets Ka and Macid together under one root sign, and –pH as '
                      'the power of 10.'})
C.fixed([k('9', 'c')], None, None)
C.ordered([k('9', 'd', 'i'), k('9', 'd', 'ii')], 'chem-3-4',
          'strong-acid-titration-curve-and-indicator', figure=FIG + 'paper-q9d')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('10', 'a', 'i')], 'chem-3-5', 'oxidation-as-loss-of-electrons', cid='q10-a-i-iii')
C.ordered([k('10', 'a', 'ii')], 'chem-3-5', 'oxidation-numbers-of-phosphorus')
C.ordered([k('10', 'a', 'iii')], 'chem-3-5', 'oxidation-numbers-of-nitrogen')
C.fixed([k('10', 'a', 'iv')], 'chem-3-5', 'balancing-a-redox-equation', cid='q10-a-iv-v')
C.fixed([k('10', 'a', 'v')], 'chem-3-5', 'reducing-agent-in-a-redox-equation')
C.ordered([k('10', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-1-2',
          'radioactivity-half-life-and-alpha-decay', cid='q10-b-i-ii',
          figure=FIG + 'paper-q10b-eq')
C.ordered([k('10', 'b', 'vi')], None, None)
C.fixed([k('10', 'b', 'vii')], None, None,
        fixes={'226 297 × 0.1 = 0.076 (g)': '226 ÷ 297 × 0.1 = 0.076 (g)'},
        row_notes={1: FRACTION.format('226', '297')})
C.fixed([k('10', 'c', 'i')], None, None, skip=('101325',),
        fixes={'1.92 32 = 0.06 (moles of O₂)': '1.92 ÷ 32 = 0.06 (moles of O₂)',
               '0.06 × 22.4 = 1.34 L // 0.06 × 8.3 × 273 = 0.00134 m³':
               '0.06 × 22.4 = 1.34 L // 0.06 × 8.3 × 273 ÷ 101325 = 0.00134 m³'},
        row_notes={1: FRACTION.format('1.92', '32'),
                   2: FRACTION.format('0.06 × 8.3 × 273', '101325')})
C.fixed([k('10', 'c', 'ii')], None, None,
        fixes={'Mr = 160 // 0.06 3 × 4 = 0.08 (moles of Fe)':
               'Mr = 160 // 0.06 ÷ 3 × 4 = 0.08 (moles of Fe)',
               '0.06 3 × 2 = 0.04 (moles of Fe₂O₃) // 0.08 × 56 = 4.48 (g of Fe)':
               '0.06 ÷ 3 × 2 = 0.04 (moles of Fe₂O₃) // 0.08 × 56 = 4.48 (g of Fe)'},
        row_notes={0: 'Two routes, printed side by side and separated by //. '
                      + FRACTION.format('0.06', '3'),
                   1: FRACTION.format('0.06', '3')})
C.fixed([k('10', 'c', 'iii')], None, None)
C.fixed([k('10', 'c', 'iv')], None, None)

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.drawn([k('11', 'a', 'i')], 'chem-2-1', 'dot-and-cross-diagram-of-bf3', S + 'q11a-i')
C.fixed([k('11', 'a', 'ii')], 'chem-2-2', 'polarity-of-the-b-f-bond', cid='q11-a-ii-iii')
C.fixed([k('11', 'a', 'iii')], 'chem-2-2', 'polarity-of-the-bf3-molecule')
C.fixed([k('11', 'a', 'iv')], 'chem-2-2', 'shape-of-phosphane', cid='q11-a-iv-v')
C.fixed([k('11', 'a', 'v')], 'chem-2-2', 'solubility-of-bf3-and-ph3-in-water')
Q11B = FIG + 'paper-q11b'
C.fixed([k('11', 'b', 'i')], 'chem-4-2', 'naming-compounds-a-to-e', figure=Q11B, each=True)
C.fixed([k('11', 'b', 'ii')], 'chem-4-2', 'classifying-a-secondary-alcohol', cid='q11-b-ii-iii',
        figure=Q11B)
C.fixed([k('11', 'b', 'iii')], 'chem-4-2', 'are-d-and-e-structural-isomers', figure=Q11B)
C.ordered([k('11', 'c', 'i')], 'chem-4-3', 'ions-causing-water-hardness', cid='q11-c-i-iii')
C.fixed([k('11', 'c', 'ii')], 'chem-4-3', 'anion-in-temporary-hardness')
C.fixed([k('11', 'c', 'iii')], 'chem-4-3', 'anion-in-permanent-hardness')
C.ordered([k('11', 'c', 'iv')], 'chem-4-3', 'formation-of-limescale', cid='q11-c-iv-vi')
C.fixed([k('11', 'c', 'v')], 'chem-4-3', 'deionising-with-ion-exchange-resins')
C.fixed([k('11', 'c', 'vi')], 'chem-4-3', 'deionised-versus-distilled-water')
C.fixed([ka('11', 'd', 'i', 'A')], 'chem-4-3', 'what-ozone-is', cid='q11-da-i-ii')
C.fixed([ka('11', 'd', 'ii', 'A')], 'chem-4-3', 'formation-of-ozone-in-the-stratosphere',
        cid='q11-da-ii')
C.fixed([ka('11', 'd', 'iii', 'A')], 'chem-4-3', 'what-cfcs-are', cid='q11-da-iii-iv')
C.fixed([ka('11', 'd', 'iv', 'A')], 'chem-4-3', 'uses-of-cfcs', cid='q11-da-iv')
C.fixed([ka('11', 'd', 'v', 'A')], 'chem-4-3', 'how-cfcs-damage-the-ozone-layer',
        cid='q11-da-v-vi')
C.fixed([ka('11', 'd', 'vi', 'A')], 'chem-4-3', 'ozone-friendly-cfc-replacements',
        cid='q11-da-vi')
Q11DB = 'chemistry-2024-HL-paper-p13-i1'
C.fixed([ka('11', 'd', 'i', 'B')], 'chem-u3', 'materials-added-with-the-iron-ore',
        cid='q11-db-i-iii', figure=Q11DB)
C.fixed([ka('11', 'd', 'ii', 'B')], 'chem-u3', 'hot-gas-blown-into-the-blast-furnace',
        cid='q11-db-ii', figure=Q11DB)
C.fixed([ka('11', 'd', 'iii', 'B')], 'chem-u3', 'by-product-removed-from-the-furnace',
        cid='q11-db-iii', figure=Q11DB)
C.ordered([ka('11', 'd', 'iv', 'B')], 'chem-u3', 'reduction-of-iron-oxide-by-carbon-monoxide',
          cid='q11-db-iv-v', figure=Q11DB)
C.menu([ka('11', 'd', 'v', 'B')], 'chem-u3', 'stages-of-the-electric-arc-process',
       cid='q11-db-v', figure=Q11DB)


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for ref, reason in C.open:
        out.append(f'OPEN {ref}: {reason}')
    out.append('')
    for key, (got, want) in sorted(C.letter_totals().items(),
                                   key=lambda kv: (int(kv[0][0]), kv[0][1])):
        out.append(f'Q{key[0]}({key[1]}) printed {want}, carded {got}')
    for key, ask, s in dict.fromkeys(P.inexact):
        out.append(f'PAPER≠REPRINT {key}: paper "{ask}" / scheme "{s}"')
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
