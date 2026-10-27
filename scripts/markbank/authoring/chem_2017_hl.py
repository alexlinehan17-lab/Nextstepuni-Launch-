#!/usr/bin/env python3
"""2017 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2017_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2017_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2017_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2017 hl

No 2017 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

The 2017 scheme is the labelled ("cue") layout. Two of its parts are keyed
differently from the paper. Q9(a): the paper sets "Define (i) a base, (ii) a
conjugate acid-base pair" inside one sentence (paper page 8, one run at x 113,
y 516), so the census holds one Q9(a); the scheme sets its own "(i)" and "(ii)"
at x 135 (scheme page 21, y 62 and 75) under one cell (2 x 3). They are one
card, Q9(a). Q9(b)(i) and (ii): the scheme labels them together, "(i) & (ii)"
(x 78, y 223), which its reader takes as (i) alone; one cell set prices the two
together, so they are one card, Q9(b)(i)-(ii).

Q4(k) and Q11(c) offer whole alternative parts A and B. The paper underlines
the term Q1(a)(i) asks about, which no text layer carries: that card takes the
paper's own print as its question, as do the parts whose figure is the
scheme's and whose ask needs the paper's equation, scheme or table.
"""
import json
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, read_lines, tidy  # noqa: E402

P = Printed(2017, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2017-HL-'
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


def shown(text, i=0):
    """An examiner's direction the student needs while self-marking, set on a
    row's note: a card's own notes are the author's record and never ship."""
    r = C.cards[-1]['rows'][i]
    r['contextNote'] = tidy(' '.join(x for x in (r.get('contextNote') or '', text) if x))


def cells(key):
    return [it.cell for it in P.items(key)]


def lift(rid, text, marks, note=''):
    return C.lifted(rid, display(text).strip(), marks, note)


def menu_row(rid, options, claim, note, per=None, steps=None, total=None):
    """An "any N" row: options lifted from the scheme, each refused unless the gate finds it."""
    opts = [C.lifted('x', display(o).strip(), None)['verbatim'] for o in options]
    if per is None:
        # Inside an orderedSplit: the whole is priced, the options are not.
        return {'id': rid, 'kind': 'anyN', 'verbatim': opts[0], 'marks': None, 'openList': True,
                'contextNote': note, 'group': {'claimMax': claim, 'options': opts}}
    return anyN(rid, opts[0], total, claim, per, opts, note, steps=steps)


_RAW = read_lines(P.scheme_path)


def raw(page, y0, y1, x0=0, x1=600):
    """The scheme's own printed lines inside a region, joined (a label or an
    examiner's note the cue reader splits off or welds to an answer)."""
    return tidy(' '.join(display(l.text) for l in _RAW if l.page == page and y0 <= l.y0 and l.y1 <= y1
                         and x0 <= l.x0 and l.x1 <= x1))


def cut(text, at):
    """`text` split where `at` begins (the paper's print, cut between two asks
    it sets in one run)."""
    i = text.index(at)
    return text[:i].strip(), text[i:].strip()


def table_rows(page, rect, cols):
    """The rows of a table the scheme prints as its answer, read between the
    table's own rules: each row is the text of each column (x0, x1) in it.
    Empty rows are not rows."""
    x0, y0, x1, y1 = rect
    pg = fitz.open(P.scheme_path)[page - 1]
    ys = set()
    for dr in pg.get_drawings():
        for it in dr['items']:
            if it[0] == 'l' and abs(it[1].y - it[2].y) < 0.5 and abs(it[1].x - it[2].x) > 100 \
                    and y0 <= it[1].y <= y1:
                ys.add(round(it[1].y, 1))
            elif it[0] == 're' and it[1].height < 1.5 and it[1].width > 100 and y0 <= it[1].y0 <= y1:
                ys.add(round(it[1].y0, 1))
    ys = sorted(ys)
    out = []
    for top, bot in zip(ys, ys[1:]):
        row = [l for l in _RAW if l.page == page and top <= l.y0 and l.y1 <= bot + 1]
        texts = tuple(tidy(' '.join(display(l.text) for l in row if a <= l.x0 < b)) for a, b in cols)
        if any(texts):
            out.append(texts)
    return out


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 Standardising potassium manganate(VII) ────────────────────────────────
C.fixed([k('1', 'a', 'i')], 'chem-4-1', 'what-a-standard-solution-is')
print_question('paper-q1a-i-print')          # the term is underlined in the question's opening
C.menu([k('1', 'a', 'ii')], 'chem-4-1', 'properties-of-a-primary-standard')
C.fixed([k('1', 'b', 'i')], 'chem-4-1', 'acid-to-keep-iron-ii-from-air-oxidation')
C.fixed([k('1', 'b', 'ii')], 'chem-4-1', 'excess-acid-in-a-manganate-vii-titration')
# (c): DESCRIBE, any four of nine (4 x 3); then the end point (3).
_q1c = P.items(k('1', 'c'))
assert [it.cell for it in _q1c] == ['[4 × 3]', '[3]'] and '[any four]' in _q1c[0].asides, _q1c
_any4 = raw(5, 530, 545, 400)
assert _any4 == 'ANY FOUR: (4 × 3)', _any4
C.add([k('1', 'c')], 'chem-4-1', 'end-point-of-a-manganate-vii-titration', [
    menu_row('r-1', _q1c[0].options(), 4, 'DESCRIBE: any four of these, (3) each: "' + _any4 + '". The scheme '
             'adds: ' + ' '.join(a for a in _q1c[0].asides if not a.startswith('[any')), per=3, total=12),
    lift('r-2', _q1c[1].text, 3, 'WHAT OBS. The scheme adds: ' + ' '.join(_q1c[1].asides))], total=15)
# (d)(i): the answer (6), then four boxed routes of two steps (3) each, set as
# fractions side by side: the answer line, with the scheme's print of the routes.
_q1d1 = P.items(k('1', 'd', 'i'))
assert _q1d1[0].cell == '[6]' and len(_q1d1[-1].asides) == 2, _q1d1
C.answer_only([k('1', 'd', 'i')], 'chem-4-1', 'moles-of-iron-ii-in-a-portion', S + 'q1d-i',
              notes='The scheme sets out four boxed routes, each two steps priced (3), and adds: '
                    + ' '.join(_q1d1[-1].asides))
shown('The scheme prices each of its routes in two steps, (3) each, and adds: ' + ' '.join(_q1d1[-1].asides))
C.route([k('1', 'd', 'ii')], 'chem-4-1', 'moles-of-manganate-vii-from-moles-of-iron-ii')
_q1d3 = P.items(k('1', 'd', 'iii'))
assert _q1d3[0].cell == '[6]' and len(_q1d3[-1].asides) == 1, _q1d3
C.answer_only([k('1', 'd', 'iii')], 'chem-4-1', 'molarity-of-the-manganate-vii-solution', S + 'q1d-iii',
              notes='The scheme sets out two boxed routes, each two steps priced (3), and adds: '
                    + _q1d3[-1].asides[0])
shown('The scheme prices each of its two routes in two steps, (3) each, and adds: ' + _q1d3[-1].asides[0])

# ── Q2 Ethene and ethyne ─────────────────────────────────────────────────────
Q2 = FIG + 'paper-q2'
C.fixed([k('2', 'a', 'i')], 'chem-u2', 'calcium-carbide-and-water', figure=Q2)
C.fixed([k('2', 'a', 'ii')], 'chem-u2', 'why-the-first-gas-collected-is-discarded', figure=Q2)
# (b)(i): DRAW, two points (2 x 3), then any two of three (2 x 3); the scheme's
# drawing is shown with the answer.
_q2b1 = P.items(k('2', 'b', 'i'))
assert [it.cell for it in _q2b1] == ['[2 × 3]', '[2 × 3]'] and '[any two]' in _q2b1[1].asides, _q2b1
_p = _q2b1[0].points()
assert len(_p) == 2, _p
_two = raw(7, 209, 224, 460)
assert _two == 'ANY TWO: (2 × 3)', _two
C.add([k('2', 'b', 'i')], 'chem-u2', 'apparatus-for-preparing-ethene', [
    lift('r-1', _p[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _p[1], 3),
    menu_row('r-3', _q2b1[1].options(), 2, 'Any two of these, (3) each: "' + _two + '". The scheme adds: '
             + ' '.join(a for a in _q2b1[1].asides if not a.startswith('[any')) + ' Its own drawing is shown '
             'with the answer.', per=3, total=6)], total=12, figure=S + 'q2b-i')
# (b)(ii): any two precautions (2 x 3) and their linked explanations (2 x 3),
# read from the scheme's table row by row: state | (3) | explain | (3).
_q2t = table_rows(7, (55, 414, 545, 775), [(60, 260), (330, 465)])
assert _q2t[0] == ('State Precaution', 'Explain Precaution') and len(_q2t) == 8, _q2t
# The third precaution breaks "test-tube" over two lines ("test-" / "tube").
assert 'test- tube' in _q2t[3][0], _q2t[3]
# The fifth ends with the solidus the scheme prints after it ("use safety screen) /").
_states = [s.replace('test- tube', 'test-tube').rstrip('/ ') for s, _e in _q2t[1:]]
_lab = [raw(7, 384, 399, 380), raw(7, 397, 413, 380)]
assert _lab == ['ANY TWO STATED PRECAUTIONS: (2 × 3)', 'ANY TWO LINKED EXPLANATIONS: (2 × 3)'], _lab
# The explanation column: every cell is an option, read whole. The first row's
# cell and the cell beside eye-protection and gloves are set over lines the flat
# extraction reads apart from the precautions beside them; the scheme's table
# cells, appended to its extraction by append-scheme-tables.py (read out of
# their own cells by PyMuPDF), are where the gate finds them. The cell beside
# eye-protection is printed again beside gloves: offered once.
_expl = [e for _s, e in _q2t[1:]]
assert _expl[0] == ('avoid suckback into hot test-tube/ avoid flying glass (chemical splash) / avoid test-tube '
                    '(apparatus) cracking'), _expl[0]
assert _expl[4] == _expl[5] == 'avoid burns (cuts from flying glass, contact with chemicals)', _expl[4:6]
_opts = [_expl[i] for i in (0, 1, 2, 3, 4, 6)]
_corr = raw(7, 772, 789)
assert _corr.startswith('[Correct, linked, specific'), _corr
C.add([k('2', 'b', 'ii')], 'chem-u2', 'safety-in-preparing-ethene', [
    menu_row('r-1', _states, 2, 'STATE: any two precautions, (3) each: "' + _lab[0] + '".', per=3, total=6),
    menu_row('r-2', _opts, 2, 'EXPLAIN: the explanation the scheme\'s table sets beside each precaution '
             'stated, (3) each: "' + _lab[1] + '". The table sets "' + _expl[4] + '" beside both '
             'eye-protection and gloves or tongs; its own print of the table is shown with the answer. '
             'It adds: ' + _corr, per=3, total=6)],
    total=12, figure=S + 'q2b-ii')
C.fixed([k('2', 'c', 'i')], 'chem-2-4', 'combustion-of-ethene-and-ethyne-compared')
C.fixed([k('2', 'c', 'ii')], 'chem-2-4', 'equation-for-the-combustion-of-ethyne')
C.fixed([k('2', 'd')], 'chem-2-4', 'reagent-to-test-for-unsaturation')
C.route([k('2', 'e')], 'chem-1-4', 'number-of-ethyne-molecules-from-calcium-carbide',
        fixes={'64∗ = 0.05 moles calcium carbide 3.2': '3.2 ÷ 64∗ = 0.05 moles calcium carbide'},
        row_notes={0: FRACTION.format('3.2', '64∗')})
C.cards[-1]['figureKey'] = Q2       # the apparatus the part names ("like that shown above")

# ── Q3 Concentration and the rate of the thiosulfate reaction ────────────────
Q3T = FIG + 'paper-q3-table'
Q3_LEAD = P.lead(k('3', 'a'))
assert Q3_LEAD.startswith('In the reaction of sodium thiosulfate') and Q3_LEAD.endswith(
    'The table contains the data collected.'), Q3_LEAD
# (a): the definition (3) and "of one reactant" (2), or the same as a
# derivative (5), which the text layer cannot carry: shown with the answer.
_q3a = P.items(k('3', 'a'))
assert [it.cell for it in _q3a][:3] == ['[3]', '[2]', '[5]'], _q3a
_def = raw(9, 61, 77, 130, 500)
assert _def == 'change in concentration per unit time / rate of change of concentration /', _def
_one = raw(9, 94, 110, 130, 500)
assert _one == 'of one (a) reactant (product)', _one
C.add([k('3', 'a')], 'chem-3-2', 'definition-of-rate-of-reaction', [
    lift('r-1', _def.rstrip('/ '), 3, 'The scheme also writes the change in concentration over time as a '
         'fraction, and accepts instead, after "or", the rate written as the derivative of a reactant\'s or '
         'product\'s concentration with time (5); its own print is shown with the answer.'),
    lift('r-2', _one, 2)], figure=S + 'q3a')
# (b): three methods, each after "or", any two points of the one used (6 + 3).
_q3b = P.items(k('3', 'b'))
assert [it.cell for it in _q3b] == ['[6 + 3]'] * 3, _q3b
_m = [it.points() for it in _q3b]
assert [len(x) for x in _m] == [3, 3, 2] and _m[0][2] == _m[1][2] and _m[1][1] == _m[2][1], _m
_any = raw(9, 221, 236, 460)
assert _any == 'ANY TWO: (6 + 3)', _any
C.add([k('3', 'b')], 'chem-u2', 'judging-when-the-same-mass-of-sulfur-has-formed', [menu_row(
    'r-1', _m[0] + [_m[1][0], _m[1][1], _m[2][0]], 2,
    'Any two points of the one method used, the first (6) and the second (3): "' + _any + '". The scheme '
    'sets three methods, the second and third each after "or": a cross under the flask, obscured, with the '
    'same depth or flask; a light meter reading reaching the same value, with the same depth or flask; and a '
    'pH or conductivity meter reading reaching the same value (6 + 3).', per=6, steps=[6, 3], total=9)],
    total=9, stem=Q3_LEAD, figure=Q3T)
# (c): the first concentration (3), then the other three (3).
_q3c = [raw(9, 409, 424, 130, 300), raw(9, 422.5, 438, 130, 300)]
assert _q3c == ['24.0 (24) g/L', '18.0 (18), 12.0 (12), 6.0 (6) g/L'], _q3c
assert cells(k('3', 'c'))[1:3] == ['[6]', '[3]'], cells(k('3', 'c'))
C.add([k('3', 'c')], 'chem-3-2', 'concentrations-of-diluted-thiosulfate', [
    lift('r-1', _q3c[0], 3, 'The scheme works each as 30 × 0.8, 30 × 0.6, 30 × 0.4 and 30 × 0.2 in its table.'),
    lift('r-2', _q3c[1], 3)], stem=Q3_LEAD, figure=Q3T)
_q3d1 = [raw(9, 604, 621, 160, 300), raw(9, 619, 635, 160, 310)]
assert _q3d1 == ['0.020 s⁻¹', '0.016, 0.012, 0.008, 0.004 s⁻¹'], _q3d1
_ded = raw(9, 705, 762, 340, 450)
assert _ded == '1 mark to be deducted for any one of these four values incorrectly rounded but make at most one deduction.', _ded
C.add([k('3', 'd', 'i')], 'chem-3-2', 'rates-as-inverse-times', [
    lift('r-1', _q3d1[0], 3),
    lift('r-2', _q3d1[1], 3, 'The scheme\'s table notes: "' + _ded + '"')], stem=Q3_LEAD, figure=Q3T)
C.fixed([k('3', 'd', 'ii')], 'chem-3-2', 'graph-of-concentration-against-rate', figure=S + 'q3d-ii',
        stem=Q3_LEAD)
shown('The scheme draws the graph both ways round; its own print is shown with the answer.', -1)
print_question('paper-q3d-ii-print')
C.fixed([k('3', 'd', 'iii')], 'chem-3-2', 'rate-proportional-to-concentration', stem=Q3_LEAD, figure=Q3T)
C.menu([k('3', 'e')], 'chem-u2', 'investigating-temperature-and-rate-with-thiosulfate', stem=Q3_LEAD,
       figure=Q3T, note='"' + raw(10, 620, 635, 450) + '".')

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-3', 'tellurium-before-iodine-in-mendeleevs-table', notes=Q4_NOTE)
# (b): "3 and // 2", priced (4 + 2), order not important.
_q4b = P.items(k('4', 'b'))
assert [it.cell for it in _q4b] == ['[4 + 2]', None] and _q4b[0].points() == ['3 and', '2'], _q4b
C.add([k('4', 'b')], 'chem-1-2', 'energy-levels-of-the-red-balmer-line', [
    lift('r-1', '3', None, 'The scheme prints "3 and // 2".'),
    lift('r-2', '2', None, 'The scheme adds: ' + display(_q4b[1].text))],
    kind='orderedSplit', notation='[4 + 2]', total=6, notes=Q4_NOTE + ' ' + SPLIT.format('[4 + 2]'))
C.fixed([k('4', 'c')], 'chem-1-2', 'daughter-nucleus-of-the-beta-decay-of-caesium-137', notes=Q4_NOTE,
        figure=FIG + 'paper-q4c-eq')
# (d): one cell (2 x 3) prices (i) and (ii), one each.
_q4d = [P.items(k('4', 'd', r)) for r in ('i', 'ii')]
assert [[it.cell for it in its] for its in _q4d] == [[None], ['[2 × 3]']], _q4d
assert display(_q4d[0][0].text) == '2 / +2 //' and display(_q4d[1][0].text) == '4 /+4', _q4d
C.add([k('4', 'd', 'i'), k('4', 'd', 'ii')], 'chem-3-5', 'oxidation-numbers-of-oxygen-and-xenon', [
    lift('r-1', '2 / +2', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '4 /+4', 3, 'For (ii).')], notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-2-3', 'avogadros-law', notes=Q4_NOTE)
C.route([k('4', 'f')], 'chem-1-4', 'mass-of-salt-in-a-saline-solution', notes=Q4_NOTE)
C.cards[-1]['figureKey'] = FIG + 'paper-q4f'      # the saline bag the item stands beside
# (g): one cell (4 + 2) over (i) and (ii).
C.ordered([k('4', 'g', 'i'), k('4', 'g', 'ii')], 'chem-2-2', 'bonding-and-intermolecular-forces-in-ammonia',
          row_notes={0: 'For (i).', 1: 'For (ii).'}, notes=Q4_NOTE)
# (h): one cell (4 + 2) over (i) and (ii); the formula is set in a large font
# the text layer reads without its subscripts.
C.ordered([k('4', 'h', 'i'), k('4', 'h', 'ii')], 'chem-4-2', 'molecular-formula-of-eugenol-and-its-identification',
          fixes={'C10H12O2': 'C₁₀H₁₂O₂'}, row_notes={0: 'For (i).', 1: 'For (ii).'}, notes=Q4_NOTE,
          figure=FIG + 'paper-q4h')
C.fixed([k('4', 'i')], 'chem-3-5', 'copper-displacing-silver', notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-4-3', 'hardness-removed-by-boiling', notes=Q4_NOTE)
# (k)A: two pairs of equations (2 x 3) each, or the one overall equation (6).
_q4ka = P.items(ka('4', 'k', None, 'A'))
assert [it.cell for it in _q4ka] == ['[2 × 3]', '[2 × 3]', '[6]'], _q4ka
C.add([ka('4', 'k', None, 'A')], 'chem-4-3', 'sulfuric-acid-in-acid-rain', [menu_row(
    'r-1', [it.text for it in _q4ka], 1,
    'One of these, as the student gave it: the scheme sets the second pair and the overall equation each '
    'after "or". Each pair is priced (2 × 3), an equation each; the overall equation (6).',
    per=6, total=6)], total=6, notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-3-5', 'anodising-aluminium', notes=Q4_NOTE)

# ── Q5 Orbitals, atomic radius and ionisation energy ─────────────────────────
# (a): DEFINE, two wordings, each two points (2 x 3); WRITE (3); HOW MANY (3).
_q5a = P.items(k('5', 'a'))
assert [it.cell for it in _q5a] == ['[2 × 3]', '[3]', '[3]'], _q5a
_w = _q5a[0].points()
assert len(_w) == 4 and _w[2] == 'approximate solution', _w
C.add([k('5', 'a')], 'chem-1-2', 'atomic-orbital-and-the-configuration-of-carbon', [
    menu_row('r-1', [_w[0], _w[2]], 1, 'DEFINE: one of these wordings, the scheme setting the second after "or"; '
             'it prices the two points of each (2 × 3), one each. It adds: ' + ' '.join(_q5a[0].asides),
             per=3, total=3),
    menu_row('r-2', [_w[1], _w[3]], 1, 'And the second point of that same wording, (3).', per=3, total=3),
    lift('r-3', _q5a[1].text, 3, 'WRITE. The scheme adds: ' + ' '.join(_q5a[1].asides)),
    lift('r-4', _q5a[2].text, 3, 'HOW MANY.')], total=12)
C.fixed([k('5', 'b')], 'chem-1-3', 'atomic-boundary-and-covalent-radius')
C.fixed([k('5', 'c', 'i')], 'chem-1-3', 'covalent-radius-down-group-1')
C.fixed([k('5', 'c', 'ii')], 'chem-1-3', 'covalent-radius-across-the-second-period', figure=FIG + 'paper-q5c')
C.fixed([k('5', 'd')], 'chem-1-3', 'first-ionisation-energy-across-the-second-period')
C.fixed([k('5', 'e', 'i')], 'chem-1-2', 'electrons-in-carbon-from-ionisation-energies')
C.fixed([k('5', 'e', 'ii')], 'chem-1-2', 'carbons-energy-levels-from-ionisation-energies')

# ── Q6 Fuels ─────────────────────────────────────────────────────────────────
# (a): one cell (5 + 3 + 3) closes IDENTIFY, GIVE and WHY.
_q6a = P.items(k('6', 'a'))
assert [it.cell for it in _q6a] == ['[5 + 3 + 3]'], _q6a
_p = _q6a[0].points()
assert len(_p) == 3 and _p[2].endswith(', etc]'), _p
C.add([k('6', 'a')], 'chem-2-4', 'methane-from-anaerobic-decomposition', [
    lift('r-1', _p[0], None, 'IDENTIFY.'),
    lift('r-2', _p[1], None, 'GIVE.'),
    # The scheme closes its list "etc]" with no bracket opened; the row is its words.
    lift('r-3', _p[2][:-1], None, 'WHY. The scheme adds: ' + ' '.join(_q6a[0].asides))],
    kind='orderedSplit', notation='[5 + 3 + 3]', total=11, notes=SPLIT.format('[5 + 3 + 3]'))
C.fixed([k('6', 'b')], 'chem-2-2', 'boiling-points-of-alkanes')
# (c)(i): the scheme's third equation draws methylbenzene as its structure,
# which the text layer cannot carry: the row is the first two, the drawing shown.
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'dehydrocyclisation-of-heptane', figure=S + 'q6c-i',
        fixes={'C₇H₁₆ → C₆H₅CH₃ + 4H₂ / C₇H₁₆ → C₇H₈ + 4H₂ / C₇H₁₆ → + 4H₂':
               'C₇H₁₆ → C₆H₅CH₃ + 4H₂ / C₇H₁₆ → C₇H₈ + 4H₂'},
        row_notes={0: 'The scheme also accepts the equation with methylbenzene drawn as its structure; its own '
                      'print is shown with the answer.'})
C.fixed([k('6', 'c', 'ii')], 'chem-2-4', 'purpose-of-dehydrocyclisation')
# (d)(i): the two structures (2 x 3), drawn in the scheme's table under their names.
_q6d1 = P.items(k('6', 'd', 'i'))
assert [it.cell for it in _q6d1] == ['[2 × 3]'] and not _q6d1[0].text, _q6d1
assert raw(15, 424, 439) == 'but-2-ene 2-methylbutane', raw(15, 424, 439)
C.add([k('6', 'd', 'i')], 'chem-2-4', 'structures-of-but-2-ene-and-2-methylbutane', [
    lift('r-1', 'but-2-ene', 3, 'Its structural formula, drawn; the scheme prices the two drawings (2 × 3), one '
         'each, and sets several forms of each in its table, shown with the answer. It adds: '
         + ' '.join(_q6d1[0].asides)),
    lift('r-2', '2-methylbutane', 3, 'Its structural formula, drawn.')], figure=S + 'q6d-i')
C.fixed([k('6', 'd', 'ii')], 'chem-2-4', 'formula-of-the-third-cracking-product')
# (e): STATE (2 x 3); CALCULATE (9), the first route's three steps (3) each.
_q6e = P.items(k('6', 'e'))
assert [it.cell for it in _q6e][:2] == ['[2 × 3]', '[9]'], _q6e
_h = _q6e[0].points()
assert len(_h) == 2, _h
_st = raw(16, 167, 183, 240, 480)
assert _st == '[(–9.3) + (–178.4) + (20.0)] kJ (3) – (– 350.9) kJ (3)', _st
_s1, _s2 = [x.strip() for x in _st.split(' (3)')[:2]]
_alt2 = raw(16, 180, 196, 240, 480)
assert _alt2 == '[(–9.3) + (–178.4) + (20.0)] kJ (3) + 350.9 kJ (3)', _alt2
_alt3 = raw(16, 194, 209, 240, 480)
assert _alt3 == '–167.7 kJ (3) + 350.9 kJ (3)', _alt3
_fin = [a for a in _q6e[-1].asides]
assert len(_fin) == 2 and _fin[0].startswith('[Final Answer'), _q6e[-1]
C.add([k('6', 'e')], 'chem-3-1', 'hess-law-and-the-heat-of-cracking', [
    lift('r-1', _h[0], 3, 'STATE. The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _h[1], 3),
    # The scheme's three boxed routes write each step one of two ways: each step a row that
    # accepts the other way (_alt2, _alt3).
    C.accepting(lift('r-3', _s1, 3, 'CALCULATE: ΔH cracking = ΣΔH formation products – ΣΔH formation reactants; '
                     'the products\' heats of formation first, or added up (3).'), '–167.7 kJ'),
    C.accepting(lift('r-4', _s2, 3, 'Then the reactant\'s, subtracted, or written added (3).'), '+ 350.9 kJ'),
    lift('r-5', '183.2 kJ', 3, 'The scheme gives the answer, 183.2 kJ, priced (9) with its working, and accepts '
         'two other routes, adding equations; its own print of every route is shown with the answer. It adds: '
         + ' '.join(_fin))], figure=S + 'q6e')
print_question('paper-q6e-print')

# ── Q7 The dinitrogen tetroxide equilibrium ──────────────────────────────────
Q7_LEAD = P.lead(k('7', 'a'))
assert Q7_LEAD.startswith('Consider the following chemical equilibrium') and Q7_LEAD.endswith('temperature T.'), Q7_LEAD
Q7EQ = FIG + 'paper-q7-eq'
C.fixed([k('7', 'a')], 'chem-3-3', 'dynamic-equilibrium-and-le-chateliers-principle')
C.drawn([k('7', 'b')], 'chem-3-3', 'kc-expression-for-dinitrogen-tetroxide', S + 'q7b', stem=Q7_LEAD)
print_question('paper-q7b-print')
_q7c = P.items(k('7', 'c'))
assert _q7c[0].cell == '[18]' and len(_q7c[-1].asides) == 4, _q7c
C.answer_only([k('7', 'c')], 'chem-3-3', 'equilibrium-concentrations-of-dinitrogen-tetroxide-and-nitrogen-dioxide',
              S + 'q7c', stem=Q7_LEAD,
              notes='The scheme sets out four boxed routes (2x or y moles of NO₂, in moles per litre or in '
                    'moles), each six steps priced (3), and adds: ' + ' '.join(_q7c[-1].asides))
shown('The scheme prices each of its routes in six steps, (3) each, and adds: ' + ' '.join(_q7c[-1].asides))
print_question('paper-q7c-print')
C.fixed([k('7', 'd')], 'chem-3-3', 'temperature-and-the-colour-of-the-equilibrium-mixture', stem=Q7_LEAD,
        figure=Q7EQ)
C.fixed([k('7', 'e')], 'chem-3-3', 'kc-and-the-initial-concentration', stem=Q7_LEAD, figure=Q7EQ)

# ── Q8 Redox reactions of organic compounds ──────────────────────────────────
Q8 = FIG + 'paper-q8'
# (a): WHAT (3) and EXPLAIN (3 + 3) before (i); the paper's third sentence leads (i) and (ii).
_q8a = P.items(k('8', 'a'))
assert [it.cell for it in _q8a] == ['[3]', '[3]', '[3]'], _q8a
_wh = display(_q8a[0].text).split(' / ')
assert len(_wh) == 2 and _wh[0] == _wh[1] == 'colourless to purple (pink) to brown to colourless (white)', _wh
C.add([k('8', 'a')], 'chem-4-2', 'colour-change-oxidising-phenylmethanol-with-manganate-vii', [
    lift('r-1', _wh[0], 3, 'WHAT. The scheme sets this twice, the second after "/", bolding "purple (pink)" and '
         '"colourless (white)" in the first and "brown to colourless (white)" in the second.'),
    lift('r-2', _q8a[1].text, 3, 'EXPLAIN.'),
    lift('r-3', _q8a[2].text, 3, 'The scheme adds: ' + ' '.join(_q8a[2].asides))],
    qtext=P.ask(k('8', 'a'), upto='transition metal reagent used.'), figure=Q8)
C.drawn([k('8', 'a', 'i')], 'chem-4-2', 'bonds-broken-in-phenylmethanol', S + 'q8a-i')
print_question('paper-q8a-i-print')
C.drawn([k('8', 'a', 'ii')], 'chem-4-2', 'bonds-formed-in-benzoic-acid', S + 'q8a-ii')
print_question('paper-q8a-ii-print')
# (b): GIVE (2 x 3); DRAW (2 x 3), the scheme's table of structures.
_q8b = P.items(k('8', 'b'))
assert [it.cell for it in _q8b] == ['[2 × 3]', '[2 × 3]'] and not _q8b[1].text, _q8b
_p = _q8b[0].points()
assert _p == ['A = propanal', 'B = propanone'], _p
C.add([k('8', 'b')], 'chem-4-2', 'propanal-and-propanone', [
    lift('r-1', _p[0], 3, 'GIVE. The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _p[1], 3, 'The scheme adds: ' + ' '.join(_q8b[0].asides)),
    lift('r-3', 'propanal', 3, 'DRAW: the structure of propanal; the scheme prices the two structures (2 × 3), '
         'one each, and sets several forms of each in its table, shown with the answer. It adds: '
         + ' '.join(_q8b[1].asides)),
    lift('r-4', 'propanone', 3, 'The structure of propanone.')], figure=S + 'q8b')
print_question('paper-q8b-print')
_q8c = P.ask(k('8', 'c'))
assert _q8c.endswith('propan-2-ol.(6)'), _q8c       # the paper sets its mark against the full stop
C.fixed([k('8', 'c')], 'chem-4-2', 'reducing-propanone-to-propan-2-ol', qtext=_q8c[:-len('(6)')], figure=Q8)
C.fixed([k('8', 'd')], 'chem-4-2', 'weak-oxidising-agent-to-tell-aldehyde-from-ketone', figure=Q8)
# (e): NAME (6); IDENTIFY (3 + 2), the alcohol and the acid of the ester named.
_q8e = P.items(k('8', 'e'))
assert [it.cell for it in _q8e] == ['[6]', '[3 + 2]', '[3 + 2]', None], _q8e
_ids = [raw(20, 170, 186, 240, 340), raw(20, 184, 199, 230, 355), raw(20, 170, 186, 380, 470),
        raw(20, 184, 199, 360, 490)]
assert _ids == ['methanol / CH₃OH', 'ethanoic acid / CH₃COOH', 'ethanol / C₂H₅OH', 'methanoic acid / HCOOH'], _ids
C.add([k('8', 'e')], 'chem-4-2', 'ester-isomer-of-propanoic-acid', [
    lift('r-1', _q8e[0].text, 6, 'NAME. The scheme adds: ' + ' '.join(_q8e[0].asides)),
    menu_row('r-2', _ids, 2, 'IDENTIFY: the alcohol and the carboxylic acid of the ester named, the first (3) and '
             'the second (2). The scheme\'s table sets methanol and ethanoic acid under methyl ethanoate, and '
             'ethanol and methanoic acid under ethyl methanoate. It adds: ' + ' '.join(_q8e[3].asides),
             per=3, steps=[3, 2], total=5)], total=11, figure=Q8)

# ── Q9 Acids and bases ───────────────────────────────────────────────────────
# (a): the paper sets (i) and (ii) inside one sentence; the scheme prices them
# with one cell (2 x 3) under markers of its own, then WHAT (3).
C.fixed([k('9', 'a')], 'chem-3-4', 'bronsted-lowry-base-and-conjugate-pair', deep=True,
        row_notes={0: 'For (i).', 1: 'For (ii).', 2: 'WHAT.'})
# (b): DEFINE (3). The aside the reader sets under it, "[Allow 'hydrochloric' for
# HCl ...]", is printed beside ACCOUNT (scheme page 21, y 183) and rides on (i)-(ii).
_q9b = P.items(k('9', 'b'))
assert [it.cell for it in _q9b] == ['[3]'] and _q9b[0].asides[0].startswith('[Allow ‘hydrochloric’'), _q9b
C.add([k('9', 'b')], 'chem-3-4', 'definition-of-ph', [lift('r-1', _q9b[0].text, 3)])
Q9B_DATA, Q9B_ASK = cut(P.lead(k('9', 'b')), 'In terms of hydrogen ions')
assert Q9B_DATA.endswith('2.37 respectively.'), Q9B_DATA
# (b)(i)-(ii): "(i) & (ii)": the first (9) from one of two boxes, then the
# methanoic acid (3).
_b1 = [raw(21, 262, 278, 130, 480), raw(21, 289, 318.5, 130, 470), raw(21, 340, 409, 130, 480)]
_b2 = [raw(21, 465, 481, 130, 480), raw(21, 492, 535, 130, 480), raw(21, 555, 571, 130, 480)]
_hcooh = raw(21, 621, 691, 130, 515)
assert _b1[0] == _b2[2] == '0.10 M HCl produces 0.10 M H⁺ ion / pH HCl = –log (0.10)', (_b1, _b2)
assert _b1[1].startswith('HCl monoprotic') and _b1[2].startswith('0.10 M H₂SO₄ produces 0.20 M') \
    and _b2[0] == '0.10 M H₂SO₄ produces 0.20 M H⁺ ion / pH H₂SO₄ = –log (0.20)' \
    and _b2[1].startswith('H₂SO₄ diprotic') and _hcooh.startswith('0.10 M methanoic acid'), (_b1, _b2, _hcooh)
_first = raw(21, 222, 238)
assert _first == '(i) & (ii) First (9) marks available from one of the boxes below.', _first
C.add([k('9', 'b', 'i'), k('9', 'b', 'ii')], 'chem-3-4', 'strong-diprotic-and-weak-acids-compared', [
    menu_row('r-1', [_b1[0], _b1[1], _b2[0]], 1,
             'For (i): "' + _first[len('(i) & (ii) '):] + '" Either the hydrochloric acid information, or after "or" '
             'the two points priced (2 × 3), one each (the first box), or the sulfuric acid information (the '
             'second box), (6). The second box also accepts, after "or", that sulfuric acid is diprotic, '
             'priced (3).', per=6, total=6),
    menu_row('r-2', [_b1[2], _b2[2]], 1, 'And, from that same box, the other acid\'s information, (3).',
             per=3, total=3),
    lift('r-3', _hcooh, 3, 'For (ii): the methanoic acid information. The scheme adds: '
         + ' '.join(P.items(k('9', 'b'))[0].asides))],
    total=12, figure=S + 'q9b-i', stem=Q9B_DATA + ' ' + Q9B_ASK)
Q9B_USE = P.lead(k('9', 'b', 'ii'))
assert Q9B_USE == 'Use the pH value given for 0.10 M methanoic acid to calculate', Q9B_USE
_q9b3 = P.items(k('9', 'b', 'iii'))
assert _q9b3[0].cell == '[6]', _q9b3
_h = raw(22, 74, 90, 80, 500)
_om = raw(22, 88, 103, 80, 500)
assert _om == '*Omission of minus loses this (3)', _om
C.add([k('9', 'b', 'iii')], 'chem-3-4', 'ka-of-methanoic-acid-from-its-ph', [
    lift('r-1', _h, 3, 'The scheme adds: "' + _om + '"'),
    lift('r-2', _q9b3[0].text, 3, 'The scheme works it from Ka = [H⁺][A⁻] over [HA], set as fractions; its own '
         'print is shown with the answer. It adds: "' + raw(22, 192, 208, 80, 300) + '"')],
    figure=S + 'q9b-iii', stem=Q9B_DATA + ' ' + Q9B_USE,
    notes='The scheme gives the answer, ' + display(_q9b3[0].text) + ', priced (6), then the working that earns '
          'it in two steps, (3) each.')
_q9b4 = P.items(k('9', 'b', 'iv'))
assert _q9b4[0].cell == '[3]', _q9b4
C.answer_only([k('9', 'b', 'iv')], 'chem-3-4', 'ph-of-a-weak-acid-from-ka', S + 'q9b-iv',
              stem=Q9B_DATA + ' ' + Q9B_USE)
shown('The scheme works it as minus log of the square root of Ka × [HA], and adds: "'
      + raw(22, 279, 294, 80, 300) + '"')
# (c): DRAW, any three of four (3 x 3); NAME (6); EXPLAIN (2).
_q9c = P.items(k('9', 'c'))
assert [it.cell for it in _q9c] == ['[3 × 3]', '[6]', '[2]'] and '[any three]' in _q9c[0].asides, _q9c
_three = raw(22, 410, 425, 450)
assert _three == 'ANY THREE: (3 × 3)', _three
C.add([k('9', 'c')], 'chem-3-4', 'ph-curve-for-methanoic-acid-and-sodium-hydroxide', [
    menu_row('r-1', _q9c[0].options(), 3, 'DRAW: any three of these, (3) each: "' + _three + '". The scheme adds: '
             + ' '.join(a for a in _q9c[0].asides if not a.startswith('[any')) + ' Its own curve is shown with '
             'the answer.', per=3, total=9),
    lift('r-2', _q9c[1].text, 6, 'NAME.'),
    lift('r-3', _q9c[2].text, 2, 'EXPLAIN. The scheme adds: ' + ' '.join(_q9c[2].asides))],
    total=17, figure=S + 'q9c')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): DRAW, two methods, "ANY FOUR POINTS: 4 + (3 x 2)" of the one drawn.
_flask = [x.strip() for x in raw(23, 60, 144, 130, 480).split('//')]
_syr = [x.strip() for x in raw(23, 200, 284, 130, 520).split('//')]
assert len(_flask) == 6 and _flask[0].startswith('conical flask') and len(_syr) == 5 \
    and _syr[0] == 'vapour in gas syringe', (_flask, _syr)
_four = raw(23, 169, 184, 400)
assert _four == raw(23, 323, 338, 400) == 'ANY FOUR POINTS: 4 + (3 × 2)', _four
_q10a = P.items(k('10', 'a'))
_dir = list(dict.fromkeys(a for it in _q10a for a in it.asides))
assert len(_dir) == 3, _dir
C.add([k('10', 'a')], 'chem-u2', 'apparatus-for-the-mr-of-a-volatile-liquid', [menu_row(
    'r-1', _flask + _syr, 4,
    'Any four points of the one method drawn, the first (4) and the others (2) each: "' + _four + '". The first '
    'six are for a flask in boiling water; the scheme sets the last five, for a gas syringe, after "or". It '
    'adds: ' + ' '.join(_dir) + ' Its own drawings of both are shown with the answer.',
    per=4, steps=[4, 2, 2, 2], total=10)], total=10, figure=S + 'q10a')
_q10stem = cut(P.ask(k('10', 'a')), 'Draw a large')[0] + ' ' + P.lead(k('10', 'a'))
# (a)(i): every number of the working and of the answer is set in an equation
# font whose doubled digits the text layer reads as "1100^−33": the row is the
# paper's ask, the scheme's print its answer.
_q10a1 = P.items(k('10', 'a', 'i'))
assert [it.cell for it in _q10a1] == ['[9]', '[6]', '[3]', '[6]', '[3]'] and '1100' in _q10a1[0].text, _q10a1
C.add([k('10', 'a', 'i')], 'chem-2-3', 'moles-of-vapour-from-the-ideal-gas-equation', [C.ask_row(
    k('10', 'a', 'i'), 9, 'The scheme\'s answer and working are set in an equation font its text cannot carry; '
    'its own print is shown with the answer. It prices the answer (9), from the ideal gas equation or from the '
    'combined gas law, the working (6) and the moles (3) in each route, and adds: '
    + _q10a1[2].asides[0])], total=9, figure=S + 'q10a-i', stem=_q10stem)
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [it.cell for it in _q10a2] == ['[6]', '[3]', '[3]', None], _q10a2
C.add([k('10', 'a', 'ii')], 'chem-2-3', 'relative-molecular-mass-of-the-volatile-liquid', [
    lift('r-1', '0.28 ÷ 8.787 × 10⁻³', 3, 'The scheme opens with n = m over Mr, or Mr = m over n. '
         + FRACTION.format('0.28', '8.787 × 10⁻³')),
    lift('r-2', _q10a2[2].text, 3, 'The scheme adds: ' + ' '.join(_q10a2[2].asides) + ' "'
         + display(_q10a2[3].text) + '"')],
    figure=S + 'q10a-ii', stem=_q10stem,
    notes='The scheme gives the answer, ' + display(_q10a2[0].text) + ', priced (6), then the two steps that '
          'earn it, (3) each.')
# (b): WHAT (6), any one of its wordings, the nuclide symbol shown with the answer.
_q10b = P.items(k('10', 'b'))
assert [it.cell for it in _q10b] == ['[6]', None], _q10b
_al = [raw(25, 48, 64, 140, 300).rstrip('/ '), raw(25, 62, 78, 140, 400).rstrip('/ '), raw(25, 88, 106, 185, 300)]
assert _al == ['helium (He) nucleus', 'particle consisting of two protons and two neutrons', '/ He²⁺'], _al
C.add([k('10', 'b')], 'chem-1-2', 'what-an-alpha-particle-is', [menu_row(
    'r-1', _al[:2] + [_al[2][2:]], 1, 'Any one of these, the scheme setting each after "/" and, before He²⁺, the '
    'helium nucleus written with its mass and atomic numbers; its own print is shown with the answer. It prices '
    'the answer (6).', per=6, total=6)], total=6, figure=S + 'q10b')
Q10B = FIG + 'paper-q10b'
Q10B_LEAD = P.lead(k('10', 'b'))
assert Q10B_LEAD.startswith('Before 1909') and Q10B_LEAD.endswith('as illustrated.'), Q10B_LEAD
_marks = raw(25, 316, 332)
assert _marks.startswith('[Marks in (i), (ii), and (iii)'), _marks
C.fixed([k('10', 'b', 'i')], 'chem-1-2', 'rutherfords-expected-result', stem=Q10B_LEAD, figure=Q10B)
shown('The scheme adds, under (iii): ' + _marks, -1)
C.fixed([k('10', 'b', 'ii')], 'chem-1-2', 'rutherfords-actual-result', stem=Q10B_LEAD, figure=Q10B)
shown('The scheme adds, under (iii): ' + _marks, -1)
C.fixed([k('10', 'b', 'iii')], 'chem-1-2', 'the-nuclear-model-of-the-atom', stem=Q10B_LEAD, figure=Q10B)
# (c)(i): WHAT (2); NAME (2); DESCRIBE (3 x 3), the three steps of any one of
# three descriptions, each with its diagrams.
_q10c1 = P.items(k('10', 'c', 'i'))
assert [it.cell for it in _q10c1][:3] == ['[2]', '[2]', '[3 × 3]'], _q10c1
_a1 = raw(25, 422, 452, 100, 540)
assert _a1.startswith('DESCRIBE: polar bond') and _a1.endswith(' //'), _a1
_a1 = _a1[len('DESCRIBE: '):-len(' //')]
_a2 = raw(25, 450, 506, 140, 540)
assert _a2.startswith('double bond in ethene breaks') and _a2.endswith(' //'), _a2
_a2 = _a2[:-len(' //')]
_a3 = raw(25, 504, 533, 140, 500)
_b1_ = raw(26, 75, 132, 160, 560)
assert _b1_.startswith('hydrogen of hydrogen chloride') and _b1_.endswith(' //'), _b1_
_b2_ = raw(26, 130, 173, 160, 560)
assert _b2_.startswith('double bond breaks and new C-H') and _b2_.endswith(' //'), _b2_
_b3_ = raw(26, 170, 199, 160, 500)
assert _a3 == _b3_ == 'addition of Cl⁻ to carbonium ion (carbocation, C⁺, intermediate) gives product (chloroethane)', \
    (_a3, _b3_)
_c1 = raw(26, 444, 460, 160, 500)
_c23 = tidy(raw(26, 458, 487, 160, 540) + ' ' + raw(26, 485, 500, 160, 500))   # its cell (6) at x 519
assert _c1 == 'polar bond in hydrogen chloride breaks into ions / HCl → H⁺ + (and) Cl⁻' and _c23.startswith(
    'double bond breaks with H⁺ adding to ethene') and _c23.endswith('regenerating a H⁺'), (_c1, _c23)
_adds = raw(25, 685, 770, 140, 545)
assert _adds.startswith('[Allow cyclic carbocation.]') and _adds.endswith('in third step.]'), _adds
C.add([k('10', 'c', 'i')], 'chem-4-2', 'ionic-addition-of-hydrogen-chloride-to-ethene', [
    lift('r-1', _q10c1[0].text, 2, 'WHAT.'),
    lift('r-2', _q10c1[1].text, 2, 'NAME.'),
    menu_row('r-3', [_a1, _b1_[:-len(' //')], _c1], 1,
             'DESCRIBE, "(3 × 3)": the first step of the one description given. The scheme sets three, the '
             'second and third each after "or", each with its diagrams, which earn the same marks; its own '
             'print is shown with the answer.', per=3, total=3),
    # The third description sets its second and last steps as one line priced (6). It is
    # offered once, in the second step's menu, so no line can be claimed twice; the card
    # can count it (3), and the row note says the scheme's other (3) is the student's to add.
    menu_row('r-4', [_a2, _b2_[:-len(' //')], _c23], 1,
             'The second step, as that same description sets it (3). The third description sets this step '
             'and the last as one line, its third option here, priced together (6): it can be claimed once, '
             'here, for (3), so a student who gave it adds the other (3) for the last step.', per=3, total=3),
    lift('r-5', _a3, 3, 'The last step (3), in the words the first two descriptions both set (the third '
         'description\'s is in its line above). The scheme adds: ' + _adds)], total=13, figure=S + 'q10c-i')
C.fixed([k('10', 'c', 'ii')], 'chem-2-2', 'geometry-around-carbon-in-ethene-and-chloroethane')
C.fixed([k('10', 'c', 'iii')], 'chem-4-2', 'chloroethane-from-ethane')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a)(i)-(iii): the routes are boxed side by side; the rows are the first box's
# steps, read from the page. The equation is the paper's, so each takes the
# paper's print of the letter as its question.
_q11a1 = P.items(k('11', 'a', 'i'))
assert _q11a1[0].cell == '[9]', _q11a1
_st = [raw(28, 84, 100, 80, 250), raw(28, 110, 130, 80, 310), raw(28, 177, 193, 80, 250)]
assert _st == ['Mr azurite = 344.5*', '63.5 = 0.06 moles Cu ⇒ 0.02 (1/50) moles azurite', 'm = 6.89 g azurite'], _st
assert raw(28, 108, 118, 80, 100) == '3.81' and raw(28, 276, 292) == '[*Addition must be shown for error to be treated as slip.]'
C.add([k('11', 'a', 'i')], 'chem-1-4', 'mass-of-azurite-containing-a-mass-of-copper', [
    lift('r-1', _st[0], 3),
    lift('r-2', '3.81 ÷ ' + _st[1], 3, FRACTION.format('3.81', '63.5')),
    lift('r-3', _st[2], 3, 'The scheme opens this step with m over 344.5 = 0.02 moles. It adds: '
         + raw(28, 276, 292))],
    figure=S + 'q11a-i',
    notes='The scheme gives the answer, ' + display(_q11a1[0].text) + ', priced (9), then three boxed routes of '
          'three steps (3) each; the steps here are its first route, and its own print of every route is shown '
          'with the answer.')
shown('The scheme gives the answer as "' + display(_q11a1[0].text) + '" (9), and accepts two other routes; its '
      'own print of every route is shown with the answer.', 2)
print_question('paper-q11a-i-print')
_q11a2 = P.items(k('11', 'a', 'ii'))
assert _q11a2[0].cell == '[9]', _q11a2
_st = [raw(28, 324, 340, 60, 200), raw(28, 348, 378, 60, 240), raw(28, 386, 401, 60, 240)]
assert _st == ['Mr malachite = 221**', '0.06 moles Cu or 0.02 moles azurite ⇒ 0.03 (3/100) moles malachite (3)',
               '0.03 × 221 = 6.63 g malachite (3)'], _st
_slip = raw(28, 505, 562)
assert _slip.startswith('[**Addition must be shown') and _slip.endswith('malachite.]'), _slip
C.add([k('11', 'a', 'ii')], 'chem-1-4', 'mass-of-malachite-formed-from-azurite', [
    lift('r-1', _st[0], 3),
    lift('r-2', _st[1][:-len(' (3)')], 3),
    lift('r-3', _st[2][:-len(' (3)')], 3, 'The scheme adds: ' + _slip)],
    figure=S + 'q11a-ii',
    notes='The scheme gives the answer, ' + display(_q11a2[0].text) + ', priced (9), then three boxed routes of '
          'three steps (3) each; the steps here are its first route.')
shown('The scheme gives the answer as "' + display(_q11a2[0].text) + '" (9), and accepts two other routes; its '
      'own print of every route is shown with the answer.', 2)
print_question('paper-q11a-ii-print')
C.route([k('11', 'a', 'iii')], 'chem-1-4', 'volume-of-carbon-dioxide-released', figure=S + 'q11a-iii',
        fixes={'0.01 (1/100) moles CO₂ gas or': '0.01 (1/100) moles CO₂ gas'})
print_question('paper-q11a-iii-print')
_q11a_stem = P.ask(k('11', 'a'))
C.fixed([k('11', 'a', 'iv')], 'chem-1-4', 'slowing-the-deterioration-of-a-painting', figure=FIG + 'paper-q11a-eq')
C.fixed([k('11', 'b')], 'chem-2-1', 'definition-of-electronegativity')
Q11B_DRAW = P.lead(k('11', 'b'))
assert Q11B_DRAW == 'Draw dot and cross diagrams to show the bonding in a molecule of', Q11B_DRAW
# (i)-(iii): each drawing (3), the scheme's table setting two forms of each.
_q11b3 = P.items(k('11', 'b', 'iii'))
assert [it.cell for it in _q11b3] == ['[3]', '[3]'] and _q11b3[0].asides == [
    '[Only bond pairs required for each molecule.]', '[BF₃ ionic unacceptable but cancellation not applied.]'], _q11b3
_cl, _use = cut(P.ask(k('11', 'b', 'iii')), 'Use electron pair repulsion')
for r, formula, concept in (('i', 'NF₃', 'dot-and-cross-diagram-of-nitrogen-trifluoride'),
                            ('ii', 'BF₃', 'dot-and-cross-diagram-of-boron-trifluoride'),
                            ('iii', 'ClF', 'dot-and-cross-diagram-of-chlorine-monofluoride')):
    _it = P.items(k('11', 'b', r))[0]
    assert _it.cell == '[3]' and display(_it.text) == formula, _it
    C.add([k('11', 'b', r)], 'chem-2-1', concept, [lift(
        'r-1', formula, 3, 'Its dot and cross diagram, drawn; the scheme draws it two ways, shown with the answer. '
        'It adds: ' + (' '.join(_q11b3[0].asides) if r == 'ii' else _q11b3[0].asides[0]))],
        figure=S + 'q11b-' + r, stem=Q11B_DRAW,
        qtext=_cl if r == 'iii' else None)
# The shape of BF3, set unnumbered after (iii) under (12).
C.add([k('11', 'b')], 'chem-2-2', 'shape-of-boron-trifluoride', [
    lift('r-1', _q11b3[1].text, 3, 'USE. The scheme adds: ' + ' '.join(_q11b3[1].asides))],
    qtext=_use, stem='', cid='q11-b-after-iii', ref_suffix='after (iii)')
Q11B_EN = P.lead(k('11', 'b', 'iii'))
assert Q11B_EN == 'Use electronegativity values to', Q11B_EN
C.fixed([k('11', 'b', 'iv')], 'chem-2-1', 'partial-charges-in-chlorine-monofluoride', figure=S + 'q11b-iv',
        stem=Q11B_EN)
shown('The scheme marks the charges on its two diagrams; its own print is shown with the answer.', -1)
C.fixed([k('11', 'b', 'v')], 'chem-2-1', 'polar-covalent-bond-in-chlorine-monofluoride', stem=Q11B_EN)
# (c)A: the fractional distillation of liquefied air.
Q11A = FIG + 'paper-q11c-a'
_q11ca1 = P.items(ka('11', 'c', 'i', 'A'))
assert [it.cell for it in _q11ca1] == ['[4 + 3]'], _q11ca1
_o = _q11ca1[0].options()
assert _o[-1] == 'etc' and _o[-2].endswith('industry,'), _o
_two = raw(30, 102, 118, 460)
assert _two == 'ANY TWO: (4 + 3)', _two
C.add([ka('11', 'c', 'i', 'A')], 'chem-u3', 'uses-of-nitrogen', [menu_row(
    'r-1', _o[:-2] + [_o[-2].rstrip(',')], 2, 'Any two of these, the first (4) and the second (3): "' + _two
    + '". The scheme ends its list with "etc".', per=4, steps=[4, 3], total=7)], total=7, figure=Q11A)
_two = raw(30, 129, 144, 460)
assert _two == 'ANY TWO: (2 × 3)', _two
C.menu([ka('11', 'c', 'ii', 'A')], 'chem-u3', 'components-removed-from-air-before-distillation', figure=Q11A,
       note='Any two of these, (3) each: "' + _two + '".')
_q11ca3 = P.items(ka('11', 'c', 'iii', 'A'))
assert [it.cell for it in _q11ca3] == ['[2 × 3]', '[2 × 3]'], _q11ca3
_w1, _w2 = _q11ca3[0].points(), _q11ca3[1].points()
assert _w1 == ['cooled', 'compressed (placed under pressure)'] and _w2 == ['compressed (placed under pressure)',
                                                                          'and allowed to expand'], (_w1, _w2)
C.add([ka('11', 'c', 'iii', 'A')], 'chem-u3', 'liquefying-air', [
    menu_row('r-1', [_w1[0], _w2[0]], 1, 'One of these wordings, the scheme setting the second after "or"; it '
             'prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_w1[1], _w2[1]], 1, 'And the second point of that same wording, (3).', per=3, total=3)],
    total=6, figure=Q11A)
C.fixed([ka('11', 'c', 'iv', 'A')], 'chem-u3', 'which-product-has-the-lower-boiling-point', figure=Q11A)
C.fixed([ka('11', 'c', 'v', 'A')], 'chem-u3', 'which-product-is-oxygen', figure=Q11A)
# (c)B: poly(ethene).
_q11cb1 = P.items(ka('11', 'c', 'i', 'B'))
assert [it.cell for it in _q11cb1][:2] == ['[6]', '[4]'] and not _q11cb1[0].text and not _q11cb1[1].text, _q11cb1
_crit = _q11cb1[1].asides[0][1:-1]
assert _crit.startswith('Three repeating units of poly(ethene)'), _crit
_where = raw(30, 603, 633)
assert _where == '[Where 2 ethenes make a carbon chain with four carbon atoms, award (3) for ethenes and (2) for chain.]', _where
C.add([ka('11', 'c', 'i', 'B')], 'chem-4-2', 'addition-polymerisation-of-ethene', [
    C.ask_row(ka('11', 'c', 'i', 'B'), 6, 'The three ethene molecules, drawn, (6): the scheme answers with its '
              'drawings, shown with the answer.'),
    lift('r-2', _crit, 4, 'The chain, drawn, (4). The scheme adds: ' + _q11cb1[1].asides[1] + ' ' + _where)],
    figure=S + 'q11c-b-i')
C.cards[-1]['rows'][0]['id'] = 'r-1'
_q11cb2 = P.items(ka('11', 'c', 'ii', 'B'))
assert [it.cell for it in _q11cb2] == ['[6 + 3]'], _q11cb2
_ldpe = raw(30, 644, 673, 160, 480)
assert _ldpe.startswith('LDPE: more branched'), _ldpe
_two = raw(30, 658, 673, 460)
assert _two == 'ANY TWO: (6 + 3)', _two
C.add([ka('11', 'c', 'ii', 'B')], 'chem-4-2', 'ldpe-and-hdpe-compared', [menu_row(
    'r-1', _q11cb2[0].options(), 2, 'Any two of these, for LDPE, the first (6) and the second (3): "' + _two
    + '". The scheme adds: ' + ' '.join(a for a in _q11cb2[0].asides if not a.startswith('[any')),
    per=6, steps=[6, 3], total=9)], total=9)
_cond = [raw(30, 698, 713, 160, 480), raw(30, 724, 754, 160, 480)]
assert _cond[0] == 'HDPE: organometallic (Ziegler-Natta) catalyst' and _cond[1].startswith('LDPE: high(er)'), _cond
assert cells(ka('11', 'c', 'iii', 'B'))[:2] == ['[3]', '[3]'], cells(ka('11', 'c', 'iii', 'B'))
C.add([ka('11', 'c', 'iii', 'B')], 'chem-4-2', 'conditions-for-making-ldpe-and-hdpe', [
    lift('r-1', _cond[0], 3), lift('r-2', _cond[1], 3)])


# A note quoted from the scheme in the reader's script notation ("r_(f)",
# "K_(c)") is shown as the page sets it.
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'], _r


# ── review ───────────────────────────────────────────────────────────────────
# Q8(c) sets its mark against the full stop of its ask, "...to propan-2-ol.(6)"
# (paper page 8, y 377): the reader takes no mark off the line.
_q8c_line = [l for l in P.paper_lines if l.page == 8 and l.text.endswith('propan-2-ol.(6)')]
assert len(_q8c_line) == 1, _q8c_line
INLINE = {('8', 'c'): 6}


def printed():
    """Every letter's printed marks: the paper sets one mark after a letter's
    last part, or -- Q9(b), Q10(a), Q10(b), Q11 -- several, one after each run
    of asks."""
    out = {}
    for key, last in P.marks.items():
        if not key[1]:
            continue
        at = [m for s in P.pseg if s.key[:2] == key[:2] for _n, m in s.marks_at]
        out[key[:2]] = sum(at) if at else last
    for key, m in INLINE.items():
        out[key] = out.get(key, 0) + m
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
        key = tuple(c['keys'][0][:2])
        if key[0] != '4':
            got[key] = got.get(key, 0) + c['totalMarks']
    marks = printed()
    for key in sorted(set(got) | set(marks), key=lambda kv: (int(kv[0]), kv[1])):
        line = f'Q{key[0]}({key[1]}) printed {marks.get(key)}, carded {got.get(key)}'
        if key == ('11', 'c'):
            line += ' (A and B are alternatives, 25 each; the paper prints each one\'s marks, 2 x 25)'
        if key in INLINE:
            line += ' (the paper sets the mark against the ask\'s full stop)'
        out.append(line)
    q4 = [c for c in C.cards if c['keys'][0][0] == '4']
    out.append(f'Q4 printed 50 for eight of eleven items, six each and one more to the best two; '
               f'carded {len(q4)} cards, (a)-(j) and (k) as A and B, {sorted({c["totalMarks"] for c in q4})} each')
    for key, ask, s in dict.fromkeys(P.inexact):
        out.append(f'PAPER≠REPRINT {key}: paper "{ask}" / scheme "{s}"')
    return '\n'.join(out)


def exclusions():
    return []


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
