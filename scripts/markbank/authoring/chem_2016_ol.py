#!/usr/bin/env python3
"""2016 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2016_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2016_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2016_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2016 ol

No 2016 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The paper sets some romans inside one sentence -- Q7(a) "Define (i) oxidation,
(ii) reduction, ...", Q10(a) "Identify (i) the mobile phase, (ii) the
stationary phase, ...", Q10(b) "Define (i) an acid, (ii) a base." -- and the
scheme prices them: Q7(a) and Q10(b) with one cell, "(2 × 6)" and "(2 × 4)",
Q10(a) with a cell each. The cards follow the cells and take the sentence as
their question. Q10(a), Q10(b) and Q10(c) set several asks in one letter,
each priced by cells of its own: one card each, the later ones cited by what
they ask. The scheme answers Q6(c)'s (i) and (ii) under "WHAT:" and "GIVE:"
with no romans of its own. The paper underlines the term Q2(a), Q9(b)(i),
Q11(a)(i) and Q11(c)A(ii) ask about and prints Q9(a)'s passage with numbered
blanks, which no text layer carries: those take the paper's own print as
their question, as do Q3(c) (the table it plots), Q4(j) (the molecules it
names), Q11(a)(iii) (the equation it needs) and Q11(c)B(ii) (the reactions it
completes), whose answers are the scheme's. Q4(k) and Q11(c) offer whole
alternative parts A and B.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN, point)

P = Printed(2016, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2016-OL-'
S = FIG + 'scheme-'
SPLIT = ('The scheme prices these points together as {} without saying which point earns which '
         'part, so no per-point value is shown.')
DRAWN = 'The scheme answers this with a drawing; its own print is shown with the answer.'


def k(*parts):
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


def print_question(suffix):
    """The paper's own print of the part as the card's question."""
    C.cards[-1]['questionFigureKey'] = FIG + suffix


def cells(key):
    return [it.cell for it in P.items(key)]


def traced(text):
    """A string quoted from the scheme in a note, checked against the scheme."""
    if not P.traceable(text):
        raise Refused(f'"{text}" is not in the 2016 ol scheme')
    return text


def cut(text, start=None, end=None):
    """The part of `text` from `start` (inclusive) up to `end` (exclusive), each
    asserted to be in it: a sentence lifted out of the paper's print."""
    a = text.index(start) if start else 0
    b = text.index(end, a) if end else len(text)
    return text[a:b].strip()


def adds(asides):
    return ('The scheme adds: ' + ' '.join(asides)) if asides else ''


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Preparing ethene and ethyne ───────────────────────────────────────────
Q1A = FIG + 'paper-q1a'
Q1B = FIG + 'paper-q1b'
# (a)(i)-(ii): one cell (6 + 3) closes the two parts.
assert [cells(k('1', 'a', r)) for r in ('i', 'ii')] == [[None], ['[6 + 3]']]
C.ordered([k('1', 'a', 'i'), k('1', 'a', 'ii')], 'chem-u2', 'reagents-for-preparing-ethene', figure=Q1A,
          row_notes={0: 'For (i).', 1: 'For (ii).'})
C.fixed([k('1', 'a', 'iii')], 'chem-u2', 'a-precaution-in-preparing-ethene', figure=Q1A)
assert cells(k('1', 'a', 'iv')) == ['[3 × 3]'], P.items(k('1', 'a', 'iv'))
C.fixed([k('1', 'a', 'iv')], 'chem-2-4', 'test-for-unsaturation', figure=Q1A)
# (v): the cell is "PRODUCTS: (3) BALANCING: (3)".
assert cells(k('1', 'a', 'v')) == ['[3 + 3]'], P.items(k('1', 'a', 'v'))
C.fixed([k('1', 'a', 'v')], 'chem-3-1', 'combustion-of-ethene', figure=Q1A)
C.fixed([k('1', 'b', 'i')], 'chem-u2', 'solid-for-preparing-ethyne', figure=Q1B)
# (ii): the procedure and what is observed, printed on two rows under one cell (6 + 3).
_q1b2 = P.items(k('1', 'b', 'ii'))
assert [it.cell for it in _q1b2] == ['[6 + 3]'] and len(_q1b2[0].points()) == 2, _q1b2
C.ordered([k('1', 'b', 'ii')], 'chem-2-4', 'combustion-test-on-ethyne', figure=Q1B,
          row_notes={0: 'For the test.', 1: 'For "What would be observed?"'})
C.fixed([k('1', 'b', 'iii')], 'chem-2-4', 'a-use-of-ethyne', figure=Q1B)

# ── Q2 A titration of sodium hydroxide with hydrochloric acid ────────────────
Q2 = FIG + 'paper-q2'
# (a): the paper underlines "end point"; the scheme underlines the words its
# aside refers to, so its own print is shown with the answer.
C.fixed([k('2', 'a')], 'chem-4-1', 'end-point-of-a-titration', figure=S + 'q2a')
print_question('paper-q2a-print')
C.fixed([k('2', 'b')], 'chem-4-1', 'indicator-for-an-acid-base-titration')
# (c)(i): a pair priced (2 × 3), or instead one statement priced (6).
_q2c1 = P.items(k('2', 'c', 'i'))
assert [it.cell for it in _q2c1] == ['[2 × 3]', '[6]'], _q2c1
_rinse = _q2c1[0].points()
assert len(_rinse) == 2, _rinse
C.add([k('2', 'c', 'i')], 'chem-4-1', 'rinsing-the-burette', [
    C.lifted('r-1', _rinse[0], 3, 'The scheme prices this point and the next (2 × 3), one each; or instead, (6), "'
             + traced(_q2c1[1].text) + '".'),
    C.lifted('r-2', _rinse[1], 3)], figure=Q2)
C.fixed([k('2', 'c', 'ii')], 'chem-4-1', 'naming-the-pipette', figure=Q2)
# (d)(i): the answer (9) and the working that earns it, a box of stacked
# fractions the text layer cannot order.
assert cells(k('2', 'd', 'i'))[0] == '[9]', P.items(k('2', 'd', 'i'))
C.answer_only([k('2', 'd', 'i')], 'chem-4-1', 'concentration-of-sodium-hydroxide-in-moles-per-litre',
              S + 'q2d-i')
_q2d2 = P.items(k('2', 'd', 'ii'))
assert [it.cell for it in _q2d2] == ['[6]', '[3]', '[3]', None], _q2d2
C.route([k('2', 'd', 'ii')], 'chem-4-1', 'concentration-of-sodium-hydroxide-in-grams-per-litre',
        notes='The scheme adds: ' + traced(_q2d2[3].text) + ' ' + ' '.join(_q2d2[3].asides))
# (e): five points priced (3 × 3): a cell pricing fewer points than the scheme
# lists is a choice, any three of the five, three each. The two asides under
# them print on one row, which the reader keeps as one line of words.
_q2e = P.items(k('2', 'e'))
assert [it.cell for it in _q2e] == ['[3 × 3]', None], _q2e
_salt = [C.lifted('x', t, None)['verbatim'] for t in _q2e[0].points()]
assert len(_salt) == 5, _salt
_diag = _q2e[1].text
assert _diag == '[Allow marks for good diagram(s).][Deduct 3 where there is no diagram.]', _diag
C.add([k('2', 'e')], 'chem-u2', 'obtaining-a-pure-dry-sample-of-sodium-chloride', [anyN(
    'r-1', _salt[0], 9, 3, 3, _salt, 'Any three of these: the scheme lists five points and prices the part '
    '(3 × 3). The scheme adds: ' + traced(_diag))], total=9)
C.fixed([k('2', 'f')], 'chem-1-2', 'flame-colour-of-sodium')

# ── Q3 The decomposition of hydrogen peroxide ────────────────────────────────
Q3 = FIG + 'paper-q3'
Q3T = FIG + 'paper-q3-table'
Q3_LEAD = P.ask(k('3'))
_table = ' The results obtained are shown in the following table.'
assert Q3_LEAD.endswith(_table), Q3_LEAD
Q3_SETUP = Q3_LEAD[:-len(_table)]
assert cells(k('3', 'a')) == ['[5]', '[6]'], P.items(k('3', 'a'))
C.fixed([k('3', 'a')], 'chem-3-2', 'catalysts-and-a-catalyst-for-hydrogen-peroxide', figure=Q3, stem=Q3_SETUP)
# (b): the cue "COMPLETE / & BALANCE:" leaves its second line on the equation's
# row; the cell is "PRODUCT: (3), BALANCING: (3)".
_q3b = P.items(k('3', 'b'))
assert [it.cell for it in _q3b] == ['[3 + 3]'], _q3b
_t = _q3b[0].text
assert _t.startswith('& BALANCE: '), _t
C.fixed([k('3', 'b')], 'chem-1-4', 'equation-for-the-decomposition-of-hydrogen-peroxide', stem=Q3_SETUP,
        figure=Q3, fixes={_t: _t[len('& BALANCE: '):]})
assert cells(k('3', 'c')) == ['[3]', '[3]', '[6]', '[3]'], P.items(k('3', 'c'))
C.fixed([k('3', 'c')], 'chem-3-2', 'graph-of-oxygen-volume-against-time', figure=S + 'q3c')
print_question('paper-q3c-print')
C.fixed([k('3', 'd')], 'chem-3-2', 'volume-read-from-the-graph-and-why-the-rate-falls', figure=Q3T,
        stem=Q3_LEAD)
C.fixed([k('3', 'e')], 'chem-3-2', 'curve-for-the-reaction-cooled-in-ice-water', figure=S + 'q3e',
        stem=Q3_SETUP)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-1', 'three-states-of-matter', notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-2', 'origin-of-the-idea-of-atoms', notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-1-1', 'smoke-filling-a-room', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-3-1', 'measuring-calorific-value', notes=Q4_NOTE)
# (e): one word (6), or instead two points (2 × 3).
_q4e = P.items(k('4', 'e'))
assert [it.cell for it in _q4e] == ['[6]', '[2 × 3]'], _q4e
_vap = _q4e[1].points()
assert len(_vap) == 2, _vap
C.add([k('4', 'e')], 'chem-u2', 'reflux', [
    C.lifted('r-1', _q4e[0].text, 6, 'Or instead, (2 × 3), one each, "' + traced(_vap[0]) + '" and "'
             + traced(_vap[1]) + '".')], notes=Q4_NOTE, figure=FIG + 'paper-q4e')
# (f): a pair (2 × 3), or instead the law as an equation (6), its proportion set
# as a fraction the text layer cannot order.
_q4f = P.items(k('4', 'f'))
assert [it.cell for it in _q4f] == ['[2 × 3]', '[6]'], _q4f
_boyle = _q4f[0].points()
assert len(_boyle) == 2, _boyle
_eqn = _q4f[1].text
assert _eqn.startswith('P₁V₁ = constant (k) / P₁V₁ = P₂V₂ / P'), _eqn
C.add([k('4', 'f')], 'chem-2-3', 'boyles-law', [
    C.lifted('r-1', _boyle[0], 3, 'The scheme prices this point and the next (2 × 3), one each; or instead, (6), "'
             + traced('P₁V₁ = constant (k) / P₁V₁ = P₂V₂') + '" or "' + traced('P ∝ 1/V')
             + '", which the scheme sets as a fraction.'),
    C.lifted('r-2', _boyle[1], 3)], notes=Q4_NOTE)
C.route([k('4', 'g')], 'chem-1-4', 'molar-volume-of-helium', notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-1-2', 'half-life', notes=Q4_NOTE)
C.fixed([k('4', 'i')], 'chem-4-3', 'removing-nitrates-and-phosphates-from-sewage', notes=Q4_NOTE)
# (j): "benzene /" then the ring drawn; the molecules are a table the paper prints.
assert [(it.cell, it.text) for it in P.items(k('4', 'j'))] == [('[6]', 'benzene /')], P.items(k('4', 'j'))
C.fixed([k('4', 'j')], 'chem-2-4', 'the-aromatic-molecule', notes=Q4_NOTE, figure=S + 'q4j',
        row_notes={0: 'After a solidus the scheme draws the ring as well; its own print is shown with the answer.'})
print_question('paper-q4j-print')
C.menu([ka('4', 'k', None, 'A')], 'chem-1-3', 'physical-properties-of-metals', notes=Q4_NOTE,
       note='The scheme prices the part "' + traced('ANY TWO: (2 × 3)') + '".')
# (k)B: the reason (3), then the product of the factory near the town chosen
# (3). The scheme names each town in small capitals before its product
# ("DROGHEDA:", scheme PDF page 9), which the reader takes for a cue: the
# products are read from the printed lines and offered as a menu, the
# candidate claiming the one for the town chosen.
_kb = P.items(ka('4', 'k', None, 'B'))
assert [it.cell for it in _kb] == ['[3]', '[3]'], _kb
_p9 = [l for l in read_lines(P.scheme_path) if l.page == 9]
_state = [l.text for l in _p9 if 135 < l.x0 < 500 and 720 <= l.y0 < 742]
assert len(_state) == 2 and _state[0].startswith('DROGHEDA: magnesium oxide'), _state
_towns = [traced(t) for t in re.split(r' / (?=(?:ARKLOW|COBH): )', ' '.join(_state))]
assert [t.split(':')[0] for t in _towns] == ['DROGHEDA', 'ARKLOW', 'COBH'], _towns
C.add([ka('4', 'k', None, 'B')], 'chem-u3', 'location-and-product-of-an-irish-chemical-factory', [
    C.lifted('r-1', _kb[0].text, 3, 'For the reason for the location.'),
    anyN('r-2', _towns[0], 3, 1, 3, _towns, 'For the product: the one for the town chosen. '
         + adds(_kb[1].asides))], total=6, notes=Q4_NOTE, figure=FIG + 'paper-q4k-b')

# ── Q5 Atoms and the periodic table ──────────────────────────────────────────
Q5B = FIG + 'paper-q5b'
assert cells(k('5', 'a')) == ['[5]', '[6]'], P.items(k('5', 'a'))
C.fixed([k('5', 'a')], 'chem-1-3', 'mendeleev-and-groups-of-the-periodic-table', figure=FIG + 'paper-q5a')
_q5b1 = P.items(k('5', 'b', 'i'))
assert [it.cell for it in _q5b1] == ['[3 × 3]'] and len(_q5b1[0].points()) == 3, _q5b1
C.fixed([k('5', 'b', 'i')], 'chem-1-2', 'identifying-elements-from-electron-arrangements', figure=Q5B)
C.fixed([k('5', 'b', 'ii')], 'chem-1-2', 'mass-number-from-neutrons', figure=Q5B)
C.drawn([k('5', 'b', 'iii')], 'chem-1-2', 'electron-arrangement-of-neon', S + 'q5b-iii')
print_question('paper-q5b-iii-print')
C.fixed([k('5', 'b', 'iv')], 'chem-1-2', 'why-neon-is-unreactive', figure=Q5B)
C.ordered([k('5', 'b', 'v')], 'chem-1-3', 'atomic-radius-across-a-period', figure=Q5B)
assert cells(k('5', 'c')) == ['[2 × 3]', '[6]'], P.items(k('5', 'c'))
# (c) asks about "element Z" of (b): (b)'s lead-in and diagrams are its stem and figure.
C.fixed([k('5', 'c')], 'chem-2-1', 'electronegativity-and-bond-type', stem=P.ask(k('5', 'b')), figure=Q5B)

# ── Q6 Hydrocarbons from crude oil ───────────────────────────────────────────
Q6 = FIG + 'paper-q6'
C.fixed([k('6', 'a')], 'chem-2-4', 'hydrocarbons', figure=Q6)
C.ordered([k('6', 'b', 'i')], 'chem-2-4', 'components-of-lpg', figure=Q6)
# (ii): the condensed formulae, then both structures drawn (their atoms are
# the scheme's picture, 'scheme-labels').
assert [(it.cell, it.text) for it in P.items(k('6', 'b', 'ii'))] == [('[3]', 'CH₃CH₂CH₃ / CH₃CH₂CH₂CH₃ /')], \
    P.items(k('6', 'b', 'ii'))
C.fixed([k('6', 'b', 'ii')], 'chem-2-4', 'structural-formula-of-propane-or-butane', figure=S + 'q6b-ii',
        row_notes={0: 'After a solidus the scheme draws both structures; its own print is shown with the answer.'})
C.fixed([k('6', 'b', 'iii')], 'chem-2-4', 'why-mercaptans-are-added-to-lpg', figure=Q6)
# (c): the paper numbers (i) and (ii); the scheme prints their answers under
# (c) as "WHAT:" (6) and "GIVE:" (6), with no romans (scheme PDF page 11).
_q6c = P.items(k('6', 'c'))
assert [it.cell for it in _q6c] == ['[6]', '[6]'], _q6c
assert _q6c[0].text.startswith('tendency of fuel to resist') and _q6c[1].text.startswith('isomerisation'), _q6c
C.add([k('6', 'c', 'i')], 'chem-2-4', 'octane-number', [C.lifted('r-1', _q6c[0].text, 6)], figure=Q6)
C.add([k('6', 'c', 'ii')], 'chem-2-4', 'raising-the-octane-number', [C.lifted('r-1', _q6c[1].text, 6)],
      figure=Q6)
C.fixed([k('6', 'd', 'i')], 'chem-2-4', 'the-fraction-used-as-jet-fuel', figure=Q6)
C.fixed([k('6', 'd', 'ii')], 'chem-2-4', 'a-use-of-the-residue', figure=Q6)

# ── Q7 Redox, and sodium in water ────────────────────────────────────────────
# (a): "Define (i) oxidation, (ii) reduction, ..." is one sentence; the scheme
# prices the two definitions "(2 × 6)", one cell: one card, six each.
_q7a = [P.items(k('7', 'a', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q7a] == [[None], ['[2 × 6]']], _q7a
assert _q7a[0][0].text.endswith(' //'), _q7a
C.add([k('7', 'a')], 'chem-3-5', 'oxidation-and-reduction-as-electron-transfer', [
    C.lifted('r-1', _q7a[0][0].text[:-len(' //')], 6,
             'For (i). The scheme prices this point and the next (2 × 6), one each. ' + adds(_q7a[0][0].asides)),
    C.lifted('r-2', _q7a[1][0].text, 6, 'For (ii). ' + adds(_q7a[1][0].asides))])
# (b)(i)-(ii): one cell, (6 + 6), closes the two parts: equal terms, six each.
_q7b = [P.items(k('7', 'b', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q7b] == [[None], ['[6 + 6]']], _q7b
C.add([k('7', 'b', 'i'), k('7', 'b', 'ii')], 'chem-3-5', 'zinc-in-copper-sulfate', [
    C.lifted('r-1', _q7b[0][0].text, 6, 'For (i). The scheme prices this point and the next (6 + 6), one each.'),
    C.lifted('r-2', _q7b[1][0].text, 6, 'For (ii).')])
assert cells(k('7', 'b', 'iii')) == ['[2 × 3]'], P.items(k('7', 'b', 'iii'))
C.fixed([k('7', 'b', 'iii')], 'chem-3-5', 'oxidising-and-reducing-agents')
Q7C = FIG + 'paper-q7c'
C.fixed([k('7', 'c', 'i')], 'chem-1-3', 'why-sodium-is-not-handled', figure=Q7C)
C.fixed([k('7', 'c', 'ii')], 'chem-1-3', 'sodium-reacting-with-water', figure=Q7C)
C.fixed([k('7', 'c', 'iii')], 'chem-1-3', 'gas-from-sodium-and-water', figure=Q7C)
C.fixed([k('7', 'c', 'iv')], 'chem-1-3', 'potassium-compared-with-sodium-in-water', figure=Q7C)

# ── Q8 Ethane, chloroethane, ethanol and ethanoic acid ───────────────────────
Q8 = FIG + 'paper-q8'
# (a): the structures drawn ((2 × 6) + 3), the asterisk marked (2). The
# scheme's drawings (their atoms are 'scheme-labels') carry the asterisk; the
# rows are the paper's asks.
_q8a = P.items(k('8', 'a'))
assert [(it.cell, it.text) for it in _q8a] == [('[(2 × 6) + 3]', ''), ('[2]', '*')], _q8a
_q8a_ask = P.ask(k('8', 'a'))
C.add([k('8', 'a')], 'chem-4-2', 'structures-of-the-three-compounds', [
    C.mark_ask(point('r-1', cut(_q8a_ask, None, 'Mark clearly'), 15,
                     'The scheme answers this with drawings of A, B and C, priced ((2 × 6) + 3); its own print is '
                     'shown with the answer.')),
    C.mark_ask(point('r-2', cut(_q8a_ask, 'Mark clearly'), 2,
                     'The scheme prices the asterisk (2) and sets it in its drawings, shown with the answer.'))],
    figure=S + 'q8a')
assert cells(k('8', 'b')) == ['[6 + (2 × 3)]'], P.items(k('8', 'b'))
C.ordered([k('8', 'b')], 'chem-4-2', 'iupac-names-of-the-three-compounds', figure=Q8)
assert cells(k('8', 'c')) == ['[2 × 3]'], P.items(k('8', 'c'))
C.fixed([k('8', 'c')], 'chem-2-2', 'which-compounds-are-soluble-in-water', figure=Q8)
# (d): one cell, ((2 × 6) + 3), over (i), (ii) and the ask the paper sets after
# (ii) under the same mark.
assert [cells(k('8', 'd', r)) for r in ('i', 'ii')] == [[None], ['[(2 × 6) + 3]']]
C.ordered([k('8', 'd', 'i'), k('8', 'd', 'ii')], 'chem-4-2', 'classifying-conversions-x-and-y', figure=Q8,
          row_notes={0: 'For (i).', 1: 'For (ii).', 2: 'For "What other condition is required for this reaction?"'})

# ── Q9 Water treatment and hard water ────────────────────────────────────────
# (a): six blanks, the cell labelled "FIRST FIVE:" (5 × 5): any five of the
# six, five each, each answer numbered by its blank; the passage the paper's print.
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a] == ['[5 × 5]'], _q9a
_blanks9 = [C.lifted('x', t, None)['verbatim'] for t in _q9a[0].points()]
assert len(_blanks9) == 6 and _blanks9[0] == '1 a flocculating agent', _blanks9
C.add([k('9', 'a')], 'chem-4-3', 'treating-a-water-supply', [anyN(
    'r-1', _blanks9[0], 25, 5, 5, _blanks9, 'Any five of these: the scheme sets the cell as "'
    + traced('FIRST FIVE: (5 × 5)') + '": six blanks, the first five answers marked.')], total=25)
print_question('paper-q9a-print')
# (b)(i): the paper underlines "hard water".
C.fixed([k('9', 'b', 'i')], 'chem-4-3', 'hard-water')
print_question('paper-q9b-i-print')
assert cells(k('9', 'b', 'ii')) == ['[2 × 3]'], P.items(k('9', 'b', 'ii'))
C.fixed([k('9', 'b', 'ii')], 'chem-4-3', 'two-types-of-hardness')
assert cells(k('9', 'b', 'iii')) == ['[5]', '[5]'], P.items(k('9', 'b', 'iii'))
C.fixed([k('9', 'b', 'iii')], 'chem-4-3', 'scale-and-temporary-hardness')
C.fixed([k('9', 'b', 'iv')], 'chem-4-3', 'gas-from-scale-and-acid', figure=FIG + 'paper-q9b')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the experiment, three methods each in four points priced (6 + 3 + 3);
# then "Identify (i) ..., (ii) ...", a cell each; then the result, (4 + 3).
_q10a = P.ask(k('10', 'a'))
_experiment = cut(_q10a, None, 'Identify (i)')
_identify = cut(_q10a, 'Identify (i)', 'Describe and explain')
_result = cut(_q10a, 'Describe and explain')
_q10a_its = P.items(k('10', 'a'))
assert [it.cell for it in _q10a_its] == ['[6 + 3 + 3]'] * 3, _q10a_its
_meth = [it.points() for it in _q10a_its]
assert [m[0] for m in _meth] == ['paper chromatography', 'thin-layer chromatography', 'column chromatography'] \
    and all(len(m) == 5 for m in _meth), _meth
_q10a_asides = [traced(a) for a in _q10a_its[2].asides]
assert len(_q10a_asides) == 3, _q10a_asides
# The cell prices three of each method's four points, (6 + 3 + 3): a choice,
# any three, the first (6), then (3) and (3).
_paper = [C.lifted('x', _meth[0][i], None)['verbatim'] for i in range(1, 5)]
C.add([k('10', 'a')], 'chem-u2', 'separating-indicators-by-chromatography', [anyN(
    'r-1', _paper[0], 12, 3, 6, _paper, 'Any three of these, the first (6), then (3) and (3): by paper '
    'chromatography, the scheme listing four points and pricing the part (6 + 3 + 3).', steps=[6, 3, 3])],
    total=12, qtext=_experiment,
    notes='The scheme sets out three methods -- paper, thin-layer and column chromatography -- each in four '
          'points priced (6 + 3 + 3); the options here are paper chromatography\'s. By thin-layer '
          'chromatography: ' + '; '.join(f'"{traced(_meth[1][i])}"' for i in range(1, 5)) + '. By column '
          'chromatography: ' + '; '.join(f'"{traced(_meth[2][i])}"' for i in range(1, 5)) + '. The scheme adds: '
          + ' '.join(_q10a_asides))
assert cells(k('10', 'a', 'i')) == ['[3]'], P.items(k('10', 'a', 'i'))
C.fixed([k('10', 'a', 'i')], 'chem-u2', 'the-mobile-phase', qtext=_identify, stem=_experiment,
        row_notes={0: 'For (i).'})
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [it.cell for it in _q10a2] == ['[3]', '[4 + 3]'], _q10a2
C.add([k('10', 'a', 'ii')], 'chem-u2', 'the-stationary-phase', [C.lifted('r-1', _q10a2[0].text, 3, 'For (ii).')],
      qtext=_identify, stem=_experiment)
_res = _q10a2[1].points()
assert len(_res) == 2 and len(_q10a2[1].asides) == 2, _q10a2
C.add([k('10', 'a')], 'chem-u2', 'result-of-separating-the-indicators', [
    C.lifted('r-1', _res[0], None, 'For "Describe". The scheme adds: ' + _q10a2[1].asides[0]),
    C.lifted('r-2', _res[1], None, 'For "explain". The scheme adds: ' + _q10a2[1].asides[1])],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'), qtext=_result,
    stem=_experiment, cid='q10-a-result', ref_suffix='the result of the experiment')
# (b): "Define (i) an acid, (ii) a base." is one sentence, priced (2 × 4); the
# asks that follow unnumbered are priced (2 × 3), (6) with its working, and
# (3) + (2). The scheme files all of them under its "(ii)" (PDF page 16).
Q10B = FIG + 'paper-q10b'
_q10b = P.ask(k('10', 'b'))
_acidbase = cut(_q10b, None, 'Define pH.')
_defph = cut(_q10b, 'Define pH.', 'Both nitric')
_strong = cut(_q10b, 'Both nitric', 'Calculate the pH')
_calc = cut(_q10b, 'Calculate the pH', 'Which has')
_which = cut(_q10b, 'Which has')
_q10b1 = P.items(k('10', 'b', 'i'))
_q10b2 = P.items(k('10', 'b', 'ii'))
assert [it.cell for it in _q10b1] == [None] and _q10b1[0].text.endswith(' //'), _q10b1
assert [it.cell for it in _q10b2] == ['[2 × 4]', '[2 × 3]', '[6]', '[3]', '[3]', '[3]', '[2]'], _q10b2
C.add([k('10', 'b')], 'chem-3-4', 'definitions-of-an-acid-and-a-base', [
    C.lifted('r-1', _q10b1[0].text[:-len(' //')], 4,
             'For (i). The scheme prices this point and the next (2 × 4), one each.'),
    C.lifted('r-2', _q10b2[0].text, 4, 'For (ii).')], qtext=_acidbase)
_ph = _q10b2[1].points()
assert len(_ph) == 2, _ph
C.add([k('10', 'b')], 'chem-3-4', 'definition-of-ph', [
    C.lifted('r-1', _ph[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    C.lifted('r-2', _ph[1], 3)], qtext=_defph, cid='q10-b-ph', ref_suffix='after (ii), pH')
C.add([k('10', 'b')], 'chem-3-4', 'ph-of-nitric-acid', [
    C.lifted('r-1', _q10b2[3].text, 3), C.lifted('r-2', _q10b2[4].text, 3)],
    qtext=_calc, stem=_strong, figure=Q10B, cid='q10-b-ph-of-nitric-acid', ref_suffix='after (ii), pH of nitric acid',
    notes='The scheme gives the answer, ' + display(_q10b2[2].text) + ', priced (6), then the working that '
          'earns it, step by step.')
C.add([k('10', 'b')], 'chem-3-4', 'nitric-and-sulfuric-acid-compared', [
    C.lifted('r-1', _q10b2[5].text, 3), C.lifted('r-2', display(_q10b2[6].text), 2)],
    qtext=_which, stem=_strong, figure=Q10B, cid='q10-b-higher-ph', ref_suffix='after (ii), the higher pH')
# (c): two groups of asks, printed with their own marks, (13) and (12). The
# scheme's dot and cross diagrams are its picture ('scheme-labels'); its aside
# on them prints on a row of its own, which the reader joins to the next answer.
_q10c = P.ask(k('10', 'c'))
_bond = cut(_q10c, None, 'State the shape')
_shape = cut(_q10c, 'State the shape')
_q10c_its = P.items(k('10', 'c'))
assert [it.cell for it in _q10c_its] == ['[4]', '[3 × 3]', '[6]', '[2 × 3]'], _q10c_its
_dot = _q10c_its[1].points()
assert len(_dot) == 3, _dot
_diagram = '[Diagram essential.][Non-valence electrons not required.]'
assert _q10c_its[2].text.startswith(_diagram + ' '), _q10c_its[2]
_tetra = _q10c_its[2].text[len(_diagram) + 1:]
_sol = _q10c_its[3].points()
assert len(_sol) == 2, _sol
C.add([k('10', 'c')], 'chem-2-1', 'covalent-bonding-in-methane', [
    C.lifted('r-1', _q10c_its[0].text, 4),
    C.lifted('r-2', _dot[0], 3, 'For the dot and cross diagram. The scheme prices this point and the next two '
             '(3 × 3), one each, and draws the molecule two ways; its own print is shown with the answer.'),
    C.lifted('r-3', _dot[1], 3),
    C.lifted('r-4', _dot[2], 3, 'The scheme adds: ' + traced(_diagram))], qtext=_bond, figure=S + 'q10c')
C.add([k('10', 'c')], 'chem-2-2', 'shape-and-solubility-of-methane', [
    C.lifted('r-1', _tetra, 6, adds(_q10c_its[2].asides)),
    C.lifted('r-2', _sol[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    C.lifted('r-3', _sol[1], 3, adds(_q10c_its[3].asides))],
    qtext=_shape, cid='q10-c-shape-and-solubility', ref_suffix='the shape and solubility of methane')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the equation and the colours printed under it are a picture (paper-q11a).
Q11A = FIG + 'paper-q11a'
# (i): the paper underlines "chemical equilibrium"; a pair priced (4 + 3), or
# instead the scheme's second pair after "or".
_q11a1 = P.items(k('11', 'a', 'i'))
assert [it.cell for it in _q11a1] == ['[4 + 3]', '[4 + 3]'], _q11a1
_rates, _conc = _q11a1[0].points(), _q11a1[1].points()
assert len(_rates) == 2 and len(_conc) == 2, (_rates, _conc)
C.add([k('11', 'a', 'i')], 'chem-3-3', 'definition-of-chemical-equilibrium', [
    C.lifted('r-1', _rates[0], None, 'The scheme prices this point and the next together (4 + 3), or instead, '
             '(4 + 3), the pair "' + traced(_conc[0] + ' // ' + _conc[1]) + '".'),
    C.lifted('r-2', _rates[1], None)],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'))
print_question('paper-q11a-i-print')
assert cells(k('11', 'a', 'ii')) == ['[3]'], P.items(k('11', 'a', 'ii'))
C.fixed([k('11', 'a', 'ii')], 'chem-3-3', 'colour-of-the-equilibrium-mixture', figure=Q11A)
# (iii): the Kc expression is a fraction (its print is 'scheme-labels').
C.drawn([k('11', 'a', 'iii')], 'chem-3-3', 'kc-expression-for-hydrogen-iodide', S + 'q11a-iii')
print_question('paper-q11a-iii-print')
assert cells(k('11', 'a', 'iv')) == ['[3]', '[6]', None], P.items(k('11', 'a', 'iv'))
C.fixed([k('11', 'a', 'iv')], 'chem-3-3', 'le-chateliers-principle-and-adding-hydrogen', figure=Q11A)
Q11B = FIG + 'paper-q11b'
C.fixed([k('11', 'b', 'i')], 'chem-3-1', 'exothermic-reactions', figure=Q11B)
# (ii): the prediction and its explanation, priced together (6 + 3); the
# prediction runs over two rows to the margin, so the reader cannot tell them
# apart: the rows are read from the item's printed rows.
_q11b2 = P.items(k('11', 'b', 'ii'))
assert [it.cell for it in _q11b2] == ['[6 + 3]'], _q11b2
_rows = [r.text for r in _q11b2[0].rows if r.text]
assert len(_rows) == 4 and _rows[2].startswith('pellets have smaller'), _rows
C.add([k('11', 'b', 'ii')], 'chem-3-2', 'iron-pellets-instead-of-powder', [
    C.lifted('r-1', traced(display(' '.join(_rows[:2]))), None, 'For the prediction.'),
    C.lifted('r-2', traced(display(' '.join(_rows[2:]))), None, 'For "Explain your answer."')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'), figure=Q11B)
# (iii): two asks, each priced by its answer, (6) and (6), with boxed working
# beneath, (3) + (3) each; a fraction in the first box.
_q11b3 = P.items(k('11', 'b', 'iii'))
assert [it.cell for it in _q11b3] == ['[6]', '[3]', '[3]', '[6]', '[3]', '[3]'], _q11b3
_iii = P.ask(k('11', 'b', 'iii'))
_mfe = cut(_iii, None, 'How many moles of iron oxide')
_mox = cut(_iii, 'How many moles of iron oxide')
C.add([k('11', 'b', 'iii')], 'chem-1-4', 'moles-of-iron-and-of-iron-oxide', [
    C.lifted('r-1', _q11b3[0].text, 6, f'For "{_mfe}" The scheme sets out the working that earns it in a box, '
             '(3) + (3).'),
    C.lifted('r-2', display(_q11b3[3].text), 6, f'For "{_mox}" The scheme sets out the working that earns it in '
             'a box, (3) + (3).')],
    figure=S + 'q11b-iii',
    notes='The scheme prices each answer and boxes the working beneath it; its own print of the working is '
          'shown with the answer.')
# (c)A: wine-making as a batch process.
Q11CA = FIG + 'paper-q11c-a'
# (i): "any two valid points (2 × 3)" -- the cell's label is not an "ANY TWO:"
# cue, so the menu is read from the item: its options are the scheme's solidi.
_ca1 = P.items(ka('11', 'c', 'i', 'A'))
assert [it.cell for it in _ca1] == ['[2 × 3]'], _ca1
_any = ' any two valid points'
assert _ca1[0].text.endswith(_any), _ca1
_batch = [traced(o.strip()) for o in _ca1[0].text[:-len(_any)].split(' / ')]
assert len(_batch) == 7, _batch
C.add([ka('11', 'c', 'i', 'A')], 'chem-u3', 'batch-process', [
    anyN('r-1', _batch[0], 6, 2, 3, _batch, 'Any two of these: the scheme prices the part "'
         + traced('any two valid points (2 × 3)') + '".')], total=6, figure=Q11CA)
# (ii): the paper underlines "co-product".
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-u3', 'co-product')
print_question('paper-q11c-a-ii-print')
assert cells(ka('11', 'c', 'iii', 'A')) == ['[2 × 3]'], P.items(ka('11', 'c', 'iii', 'A'))
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-3-2', 'definition-of-an-enzyme')
C.fixed([ka('11', 'c', 'iv', 'A')], 'chem-u3', 'steel-reaction-vessels', figure=Q11CA)
# (c)B: polymers and recycling.
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-4-2', 'monomers')
# (ii): the scheme draws the polymer and prices three points about it (3 × 3);
# the reactions the part completes are the paper's print.
assert cells(ka('11', 'c', 'ii', 'B')) == ['[3 × 3]'], P.items(ka('11', 'c', 'ii', 'B'))
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-4-2', 'addition-polymerisation-of-chloroethene', figure=S + 'q11c-b-ii',
        notes='The scheme draws the polymer above these points; its own print is shown with the answer.')
print_question('paper-q11c-b-ii-print')
# (iii)-(iv): the sentence before (ii), "... as shown.", is (ii)'s lead-in, not theirs.
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-4-3', 'why-recycle-plastic', stem='')
C.fixed([ka('11', 'c', 'iv', 'B')], 'chem-4-3', 'recycling-plastic', skip=('Blank Page',), stem='')


# ── excluded ─────────────────────────────────────────────────────────────────
# None: every part the paper prints has an answer in the scheme.
EXCLUDED = []


def exclusions():
    out = []
    for key, reason in EXCLUDED:
        sg = P.sseg_of(key)
        said = ' '.join(x.strip() for x in [it.text + (f' {it.cell}' if it.cell else '')
                                            for it in P.items(key)] if x.strip())
        out.append({'ref': C.ref([key]), 'reason': reason,
                    'evidence': f'{P.year} OL scheme p.{sg.answers[0].page if sg.answers else sg.text[0].page}: '
                                f'"{C.label(key)} {display(joined(sg.text))}" — {said}'})
    return out


def printed_marks():
    """Every letter's printed marks, alternatives apart: the paper prints Q10(b),
    Q10(c) and Q11(a)-(b) in subtotals ("(13)" then "(12)"), so the sum of every
    mark printed under the letter, not the last."""
    out = {}
    for s in P.pseg:
        q, letter, _roman, alt = s.key
        if letter and s.marks_at:
            out[(q, letter, alt)] = out.get((q, letter, alt), 0) + sum(m for _n, m in s.marks_at)
    for (q, letter, _r, _a), m in P.marks.items():
        if letter and not any(key[:2] == (q, letter) for key in out):
            out[(q, letter, None)] = m
    return out


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for key, reason in EXCLUDED:
        out.append(f'EXCLUDED {C.ref([key])}: {reason}')
    got = {}
    for c in C.cards:
        q, letter, _r, alt = c['keys'][0]
        got[(q, letter, alt)] = got.get((q, letter, alt), 0) + c['totalMarks']
    want = printed_marks()
    for key in sorted(set(got) | set(want), key=lambda x: (int(x[0]), x[1] or '', x[2] or '')):
        if key[1] is None:
            continue
        label = f'Q{key[0]}({key[1]}){key[2] or ""}'
        if key[0] == '4':
            # The paper prints "(50)" for eight items and no mark per item; the
            # scheme allots six to each (one more to the best two, at marking).
            out.append(f'{label} printed (50) for eight items, scheme 6 each, carded {got.get(key)}'
                       + ('' if got.get(key) == 6 else '   <-- differs'))
            continue
        out.append(f'{label} printed {want.get(key)}, carded {got.get(key)}'
                   + ('' if want.get(key) == got.get(key) else '   <-- differs'))
    for key, ask, s in dict.fromkeys(P.inexact):
        out.append(f'PAPER≠REPRINT {key}: paper "{ask}" / scheme "{s}"')
    return '\n'.join(out)


if __name__ == '__main__':
    problems = make_audit(MAX_OPTIONS)(C.cards)
    for p in problems:
        print('AUDIT', p, file=sys.stderr)
    if '--exclusions' in sys.argv:
        print(json.dumps(exclusions(), ensure_ascii=False, indent=1))
    elif '--review' in sys.argv:
        print(review())
    else:
        print(json.dumps(C.finish(), ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)
