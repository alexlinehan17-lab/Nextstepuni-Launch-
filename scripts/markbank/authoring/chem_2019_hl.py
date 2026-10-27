#!/usr/bin/env python3
"""2019 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2019_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2019_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2019_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2019 hl

No 2019 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

The 2019 scheme is the labelled ("cue") layout. Where a part's tariff is set
on its cue line ("GIVE: (6)") and its breakdown under the answer ("TWO PARTS:
(2 x 3)", "ANY TWO: (4 + 2)", "THREE ITEMS: (2 + 2 + 1)"), the reader holds
the total as the cell and the breakdown as text; those cards are set here from
the reader's own text, each asserting the cells it relies on.

Q3 offers two whole methods (a flask in a beaker, or a gas syringe); every
part of it is carded with both, the student claiming the one they used. Q4(k)
and Q11(c) offer whole alternative parts A and B. The paper underlines the
terms Q5(b)(i), Q9(d) and Q10(a)(i) ask about, which no text layer carries:
those take the paper's own print as their question.
"""
import json
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, read_lines, tidy  # noqa: E402

P = Printed(2019, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2019-HL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'
SPLIT = ('The scheme prices these points together as {} without saying which point earns which '
         'part, so no per-point value is shown.')
TICK = ' (✓)'


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


def untick(t):
    """A point the scheme closes with its tick mark "(✓)", without the mark."""
    t = display(t).strip()
    assert t.endswith('(✓)'), t
    return t[:-3].strip()


def lift(rid, text, marks, note=''):
    return C.lifted(rid, display(text).strip(), marks, note)


def routed(row, route):
    """A row on one side of the scheme's "or": a student who claims a row of one
    route has the other route's rows locked (the session's mutually exclusive
    routes), so two alternative answers are both claimable and never mixed."""
    row['route'] = route
    return row


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
    """The scheme's own printed lines inside a region, joined (an examiner's note
    the cue reader splits around a cell it reads inside the note)."""
    return tidy(' '.join(display(l.text) for l in _RAW if l.page == page and y0 <= l.y0 and l.y1 <= y1
                         and x0 <= l.x0 and l.x1 <= x1))


def table_lines(page, rect, split_x):
    """The lines of a two-column table the scheme prints as its answer, read
    row by row between the table's own rules: each line is its left cell, then
    its right cell. The header row and empty rows are not lines."""
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
        cell = [l for l in _RAW if l.page == page and top <= l.y0 and l.y1 <= bot + 1 and x0 <= l.x0 < x1]
        left = tidy(' '.join(display(l.text) for l in cell if l.x0 < split_x))
        right = tidy(' '.join(display(l.text) for l in cell if l.x0 >= split_x))
        if left or right:
            out.append((left, right))
    return out


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 Dissolved oxygen by titration ─────────────────────────────────────────
# (a): one cell, (4 + 4 + 4), closes the three parts: equal terms, four each.
_q1a = [P.items(k('1', 'a', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in its] for its in _q1a] == [[None], [None], ['[4 + 4 + 4]']], _q1a
C.add([k('1', 'a', r) for r in ('i', 'ii', 'iii')], 'chem-4-1', 'reagents-and-observations-in-the-winkler-method', [
    lift('r-1', _q1a[0][0].text, 4, 'For (i). The scheme prices these three points (4 + 4 + 4), one each. '
         'It adds: ' + ' '.join(_q1a[0][0].asides)),
    lift('r-2', _q1a[1][0].text, 4, 'For (ii).'),
    lift('r-3', _q1a[2][0].text, 4, 'For (iii).')])
# (b)(i): (9) on its cue line, then the two points priced "Prepation and one use: (6 + 3)".
_q1b = P.items(k('1', 'b', 'i'))
assert [it.cell for it in _q1b] == ['[9]', '[6 + 3]'] and not _q1b[0].text, _q1b
_p = _q1b[1].points()
assert len(_p) == 3 and _p[2] == 'Prepation and one use:', _p
C.add([k('1', 'b', 'i')], 'chem-4-1', 'preparing-and-using-the-conical-flask', [
    lift('r-1', _p[0], None, 'The scheme adds: ' + ' '.join(_q1b[1].asides)),
    lift('r-2', _p[1], None)],
    kind='orderedSplit', notation='[6 + 3]', total=9,
    notes=SPLIT.format('[6 + 3]') + ' It labels them "' + _p[2] + ' (6 + 3)".')
shown('The scheme labels these two points "' + _p[2] + ' (6 + 3)".')
C.fixed([k('1', 'b', 'ii')], 'chem-4-1', 'reading-a-burette-at-eye-level')
C.fixed([k('1', 'c', 'i')], 'chem-4-1', 'colour-of-iodine-fading-to-straw')
C.fixed([k('1', 'c', 'ii')], 'chem-4-1', 'starch-iodine-end-point-colour')
C.route([k('1', 'd', 'i')], 'chem-4-1', 'moles-of-thiosulfate-in-a-titre',
        fixes={'ܯ= 3.1 248 = 0.0125 (1/80) M': '3.1 ÷ 248 = 0.0125 (1/80) M',
               '6.0 × 0.0125 = 0.000075 (7.5 × 10⁻⁵, 3/40000) moles thiosulfate':
               '6.0 × 0.0125 ÷ 1000 = 0.000075 (7.5 × 10⁻⁵, 3/40000) moles thiosulfate'},
        row_notes={1: FRACTION.format('3.1', '248'), 2: FRACTION.format('6.0 × 0.0125', '1000')})
C.route([k('1', 'd', 'ii')], 'chem-4-1', 'moles-of-oxygen-from-moles-of-thiosulfate')
C.route([k('1', 'd', 'iii')], 'chem-4-1', 'concentration-of-dissolved-oxygen-in-moles-per-litre',
        figure=S + 'q1d-iii')
# (iv): the answer (5), then two steps the scheme prices together (4 + 1).
_q1d4 = P.items(k('1', 'd', 'iv'))
assert [it.cell for it in _q1d4] == ['[5]', '[4 + 1]'], _q1d4
_p = _q1d4[1].points()
assert len(_p) == 2, _p
C.add([k('1', 'd', 'iv')], 'chem-4-1', 'dissolved-oxygen-in-parts-per-million', [
    lift('r-1', _p[0], None, 'The scheme adds: ' + _q1d4[1].asides[0]),
    lift('r-2', _p[1], None, 'The scheme adds: ' + ' '.join(_q1d4[1].asides[1:]))],
    kind='orderedSplit', notation='[4 + 1]', total=5,
    notes='The scheme gives the answer, ' + display(_q1d4[0].text) + ', priced (5), then the working '
          'that earns it. ' + SPLIT.format('[4 + 1]'))

# ── Q2 Ethanoic acid, ethanal and ethanol ────────────────────────────────────
Q2 = FIG + 'paper-q2'
Q2C = FIG + 'paper-q2c-eq'
C.fixed([k('2', 'a', 'i')], 'chem-4-2', 'magnesium-in-dilute-ethanoic-acid', figure=Q2)
C.fixed([k('2', 'a', 'ii')], 'chem-4-2', 'products-of-magnesium-and-ethanoic-acid', figure=Q2)
# (b): four tests, each priced (6 + 3); the scheme gives Tollens' first, and
# Fehling's, acidified permanganate and acidified dichromate after "or".
_q2b = P.items(k('2', 'b'))
assert [it.cell for it in _q2b] == ['[6 + 3]', '[6 + 3]'], _q2b
_t, _u = _q2b[0].points(), _q2b[1].points()
assert len(_t) == 4 and _u[0] == 'or allow' and _u[3] == 'or allow' and len(_u) == 6, (_t, _u)
C.add([k('2', 'b')], 'chem-4-2', 'test-showing-ethanal-is-easily-oxidised', [
    menu_row('r-1', [_t[0], _t[2], _u[1], _u[4]], 1,
             'One test, its reagent: the scheme sets four, Tollens\' first, Fehling\'s after "or", and '
             'acidified permanganate and acidified dichromate each after "or allow".'),
    menu_row('r-2', [_t[1], _t[3], _u[2], _u[5]], 1, 'And the result of that same test, in the same order.')],
    kind='orderedSplit', notation='[6 + 3]', total=9, figure=Q2,
    notes='The scheme prices each test (6 + 3). ' + SPLIT.format('[6 + 3]'))
# (c)(i): the apparatus (2 x 3), then the four labelled locations (4 x 1), which
# the scheme prints as its drawing's labels.
_q2c1 = P.items(k('2', 'c', 'i'))
assert [it.cell for it in _q2c1] == ['[2 × 3]', None], _q2c1
_lab = display(_q2c1[1].text)
assert _lab == 'glass wool soaked in ethanol ethene heat catalyst / Al₂O₃ (4 × 1)', _lab
_labels = [_lab[:28], _lab[29:35], _lab[36:40], _lab[41:57]]
assert _labels == ['glass wool soaked in ethanol', 'ethene', 'heat', 'catalyst / Al₂O₃'], _labels
_loc = raw(7, 651, 664)
assert _loc == 'FOUR CORRECT LOCATIONS: (4 × 1)', _loc
_p = _q2c1[0].points()
C.add([k('2', 'c', 'i')], 'chem-u2', 'apparatus-for-preparing-ethene', [
    lift('r-1', _p[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _p[1], 3),
    # The four locations are one cell, (4 x 1): one menu of all four, a mark each.
    menu_row('r-3', _labels, 4, 'The labels on the scheme\'s drawing, which is shown with the answer: "'
             + _loc + '". The scheme adds: ' + ' '.join(_q2c1[1].asides), per=1, total=4)],
    total=10, figure=S + 'q2c-i')
print_question('paper-q2c-i-print')
C.fixed([k('2', 'c', 'ii')], 'chem-u2', 'aluminium-oxide-catalyst', figure=Q2C)
# (iii): EXPLAIN, then HOW, priced (3 + 3): equal terms, three each.
_q2c3 = P.items(k('2', 'c', 'iii'))
assert [it.cell for it in _q2c3] == ['[3 + 3]'], _q2c3
_t = display(_q2c3[0].text)
_cut = _t.index(' remove delivery tube (apparatus) from water (trough) before')
C.add([k('2', 'c', 'iii')], 'chem-u2', 'suck-back-and-how-to-prevent-it', [
    lift('r-1', _t[:_cut], 3, 'The scheme prices this point and the next (3 + 3), one each.'),
    lift('r-2', _t[_cut:], 3)], figure=Q2C)
C.answer_only([k('2', 'c', 'iv')], 'chem-1-4', 'volume-of-ethene-from-ethanol-in-26-percent-yield',
              S + 'q2c-iv',
              notes='The scheme ticks four steps of each route, "' + raw(8, 453, 466) + '", and says: "'
                    + raw(8, 466, 480) + ' (3 + 3 + 1 + 1)". It adds: "' + raw(8, 707, 721) + '"')
shown(C.cards[-1]['notes'])
print_question('paper-q2c-iv-print')

# ── Q3 The relative molecular mass of a volatile liquid ──────────────────────
# Two methods throughout: a flask in a beaker of water, or a gas syringe.
Q3 = FIG + 'paper-q3'
Q3A = S + 'q3a'
_q3a = P.items(k('3', 'a'))
_q3a1 = P.items(k('3', 'a', 'i'))
_q3a2 = P.items(k('3', 'a', 'ii'))
assert [it.cell for it in _q3a] == ['[5]', '[2 + 2 + 1]'], _q3a
assert [it.cell for it in _q3a1] == ['[4]', '[4]'], _q3a1
assert [it.cell for it in _q3a2] == ['[2]', '[5]', '[2 + 2 + 1]', '[2]'], _q3a2
_m1, _m2 = _q3a[1].points(), _q3a2[2].points()
assert _m1[3] == 'Three items:' and _m2[3] == 'Three items:', (_m1, _m2)
# The drawing: three items from the one method drawn, (2 + 2 + 1). Each method
# lists its three items in that order, so row k offers item k of either method.
_one = 'one of these, as the method drawn: the first for the flask in a beaker, the second for the gas syringe.'
C.add([k('3', 'a')], 'chem-u2', 'apparatus-for-the-mr-of-a-volatile-liquid', [
    menu_row('r-1', [_m1[0], _m2[0]], 1, 'The first of the three items, (2 + 2 + 1), ' + _one
             + ' The scheme adds, for the flask in a beaker: ' + ' '.join(_q3a[1].asides)
             + ' For the gas syringe: ' + ' '.join(_q3a2[2].asides)),
    menu_row('r-2', [_m1[1], _m2[1]], 1, 'The second item, ' + _one),
    menu_row('r-3', [_m1[2], _m2[2]], 1, 'The third item, ' + _one)],
    kind='orderedSplit', notation='[2 + 2 + 1]', total=5, figure=Q3A,
    qtext=P.ask(k('3', 'a'), upto='this experiment.'),
    notes='The scheme prices the drawing (5), three items of the one method drawn, (2 + 2 + 1), and '
          'draws both methods; its own print is shown with the answer. ' + SPLIT.format('[2 + 2 + 1]'))
shown('The scheme draws both methods; its own print is shown with the answer.')
print_question('paper-q3a-print')
C.add([k('3', 'a', 'i')], 'chem-u2', 'heating-the-volatile-liquid', [menu_row(
    'r-1', [_q3a1[0].text, _q3a1[1].text], 1,
    'One of these, as the method drawn: the first for the flask in a beaker, the second for the gas '
    'syringe; the scheme prices either (4).', per=4, total=4)], total=4, figure=Q3A)
print_question('paper-q3a-i-print')
C.add([k('3', 'a', 'ii')], 'chem-u2', 'measuring-the-temperature-of-the-vapour', [menu_row(
    'r-1', [_q3a2[0].text, _q3a2[3].text], 1,
    'One of these, as the method drawn: the first for the flask in a beaker, the second for the gas '
    'syringe; the scheme prices either (2). It adds: ' + _q3a2[0].asides[0], per=2, total=2)],
    total=2, figure=Q3A)
print_question('paper-q3a-ii-print')
# (b): one cell, (6 + 3), closes (i) and (ii); each part has its two methods.
_q3b = [P.items(k('3', 'b', r)) for r in ('i', 'ii')]
assert [[it.cell for it in its] for its in _q3b] == [[None], ['[6 + 3]']], _q3b


def methods(item):
    """The two methods' answers to one part: "flask in beaker method: ..." or
    "gas syringe method: ...", as the scheme labels them."""
    p = item.points()
    assert p[0] == 'flask in beaker method:' and p[2] == 'or' and p[3] == 'gas syringe method:', p
    return [p[0] + ' ' + p[1], p[3] + ' ' + p[4]]


C.add([k('3', 'b', 'i'), k('3', 'b', 'ii')], 'chem-u2', 'pressure-and-volume-of-the-vapour', [
    menu_row('r-1', methods(_q3b[0][0]), 1, 'For (i), one of these, as the method drawn. The scheme '
             'adds: ' + ' '.join(_q3b[0][0].asides)),
    menu_row('r-2', methods(_q3b[1][0]), 1, 'For (ii), one of these, as the method drawn. The scheme '
             'adds: ' + ' '.join(_q3b[1][0].asides))],
    kind='orderedSplit', notation='[6 + 3]', total=9, figure=Q3, notes=SPLIT.format('[6 + 3]'))
_q3c = P.items(k('3', 'c'))
assert [it.cell for it in _q3c] == ['[6]', None], _q3c
_p = _q3c[0].points()
assert _p[0] == 'flask in beaker method:' and _p[2] == 'gas syringe method:', _p
_cut = _p[1].index(' [DESCRIBE linked')
C.add([k('3', 'c')], 'chem-u2', 'finding-the-mass-of-the-vapour', [menu_row(
    'r-1', [_p[0] + ' ' + _p[1][:_cut], _p[2] + ' ' + _p[3]], 1,
    'One of these, as the method drawn; the scheme prices either (6). It adds: ' + display(_q3c[1].text)
    + ' ' + ' '.join(_q3c[0].asides), per=6, total=6)], total=6, figure=Q3)
_q3d = P.items(k('3', 'd'))
assert _q3d[0].cell == '[15]' and _q3d[-1].cell is None, _q3d
C.answer_only([k('3', 'd')], 'chem-2-3', 'relative-molecular-mass-from-the-ideal-gas-equation', S + 'q3d',
              notes='The scheme adds: "' + display(_q3d[-1].text) + '"')
shown(C.cards[-1]['notes'])
print_question('paper-q3d-print')
C.fixed([k('3', 'e')], 'chem-2-2', 'why-bromine-is-more-volatile-than-water', figure=Q3)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-2', 'cathode-rays', notes=Q4_NOTE, tail=True)
C.fixed([k('4', 'b')], 'chem-1-2', 'daughter-nucleus-of-beta-decay-of-potassium-40', notes=Q4_NOTE,
        figure=S + 'q4b',
        row_notes={0: 'The scheme also writes the nuclide with its mass and atomic numbers; its own print '
                      'is shown with the answer.'})
print_question('paper-q4b-print')
C.fixed([k('4', 'c')], 'chem-2-3', 'avogadros-law', notes=Q4_NOTE)
# (d): the scheme prints no (i) or (ii); its two answers, (2 x 3), are labelled by formula.
_q4d = P.items(k('4', 'd'))
assert [it.cell for it in _q4d] == ['[2 × 3]'], _q4d
_p = _q4d[0].points()
assert len(_p) == 2, _p
C.add([k('4', 'd', 'i'), k('4', 'd', 'ii')], 'chem-3-5', 'oxidation-numbers-of-sulfur', [
    lift('r-1', _p[0], 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _p[1], 3, 'For (ii). The scheme adds: ' + ' '.join(_q4d[0].asides))], notes=Q4_NOTE)
# (e): any two lines of the scheme's table, (2 x 3).
_q4e = table_lines(12, (28, 262, 560, 512), 300)
assert _q4e[0] == ('sigma (σ):', 'pi (π):') and len(_q4e) == 10, _q4e
assert re.fullmatch(r'ANY TWO LINES: \(2 × 3\)', raw(12, 525, 537)), raw(12, 525, 537)
C.add([k('4', 'e')], 'chem-2-1', 'sigma-and-pi-bonds-compared', [menu_row(
    'r-1', [a + ' — ' + b for a, b in _q4e[1:]], 2,
    'Any two lines of the scheme\'s table, each its statement for the sigma bond, then for the pi '
    'bond: "' + raw(12, 525, 537) + '". The scheme adds: ' + raw(12, 538, 578) + ' Its own print of '
    'the table is shown with the answer.', per=3, total=6)], total=6, figure=S + 'q4e', notes=Q4_NOTE)
C.fixed([k('4', 'f')], 'chem-3-5', 'half-equation-at-the-cathode-in-electrolysis-of-ki', notes=Q4_NOTE,
        figure=FIG + 'paper-q4f-eq')
_q4g = P.items(k('4', 'g'))
assert [it.cell for it in _q4g] == ['[2 × 3]'], _q4g
_p = _q4g[0].points()
assert len(_p) == 3, _p
_cut = _p[1].index(' average amount of bond dissociation energies')
# Two definitions, the second after "or", each two points (2 × 3): two routes, so
# a student claims the points of the definition they gave and the other's lock.
C.add([k('4', 'g')], 'chem-3-1', 'definition-of-bond-energy', [
    routed(lift('r-1', _p[0], 3, 'The scheme prices this point and the next (2 × 3), one each. It sets a '
                'second definition after "or", the last two rows: the examiner marks one definition or the '
                'other, not a mix of the two.'), 'a'),
    routed(lift('r-2', _p[1][:_cut], 3), 'a'),
    routed(lift('r-3', _p[1][_cut:], 3, 'Or instead, after "or": this point and the next (2 × 3), one each.'), 'b'),
    routed(lift('r-4', _p[2], 3), 'b')], total=6, notes=Q4_NOTE)
_q4h = P.items(k('4', 'h'))
assert [it.cell for it in _q4h] == ['[2 × 3]', '[2 × 3]'], _q4h
_p, _o = _q4h[0].points(), _q4h[1].points()
# Two statements of the principle, the second after "or", each two points
# (2 × 3): two routes, as (g).
C.add([k('4', 'h')], 'chem-4-2', 'principle-of-chromatography', [
    routed(lift('r-1', _p[0], 3, 'The scheme prices this point and the next (2 × 3), one each. It sets a '
                'second answer after "or", the last two rows: the examiner marks one answer or the other, not '
                'a mix of the two.'), 'a'),
    routed(lift('r-2', _p[1], 3), 'a'),
    routed(lift('r-3', _o[0], 3, 'Or instead, after "or": this point and the next (2 × 3), one each.'), 'b'),
    routed(lift('r-4', _o[1], 3), 'b')], total=6, notes=Q4_NOTE)
# (i): the answer (6), then its working, (2 x 3): the Mr, then n = m over Mr.
_q4i = P.items(k('4', 'i'))
assert [it.cell for it in _q4i] == ['[6]', '[2 × 3]'], _q4i
_p = _q4i[1].points()
_w = display(_p[1])
_w = _w[_w.index('4.86'):_w.index('100.116 mg') + 10]
C.add([k('4', 'i')], 'chem-1-4', 'mass-of-ibuprofen-in-a-dose', [
    lift('r-1', _p[0], 3, 'The scheme prices this step and the next (2 × 3), one each. It adds: '
         + ' '.join(_q4i[1].asides)),
    lift('r-2', _w, 3, 'The scheme opens this step with n = m over Mr, as a fraction; its own print is '
         'shown with the answer.')], figure=S + 'q4i',
    notes='The scheme gives the answer, ' + display(_q4i[0].text) + ', priced (6), then the working that '
          'earns it. ' + Q4_NOTE)
shown('The scheme gives the answer, "' + display(_q4i[0].text) + '", priced (6), and this working.', 1)
print_question('paper-q4i-print')
# (j): the equation, priced for its left side and for its right side (3 + 3).
_q4j = P.items(k('4', 'j'))
assert [it.cell for it in _q4j] == ['[3]'], _q4j
_p = _q4j[0].points()
assert _p[1].startswith('Allow: '), _p
_tar = raw(13, 356, 368)
assert _tar == 'LEFT SIDE FORMULAE: (3) RIGHT SIDE FORMULA IF EQUATION BALANCED: (3)', _tar
C.add([k('4', 'j')], 'chem-4-3', 'equation-for-temporary-hardness', [
    lift('r-1', _p[0], 6, 'The scheme prices this equation "' + _tar + '", and adds: "' + display(_p[1])
         + '".')], notes=Q4_NOTE)
_one = raw(13, 413, 426, 480)
assert _one == 'ANY ONE: (6)', _one
C.menu([ka('4', 'k', None, 'A')], 'chem-2-1', 'why-nitrogen-is-unreactive', notes=Q4_NOTE,
       note='Any one of these: "' + _one + '".')
_q4kb = P.items(ka('4', 'k', None, 'B'))
C.drawn([ka('4', 'k', None, 'B')], 'chem-4-2', 'repeating-units-of-polypropene', S + 'q4k-b',
        notes=Q4_NOTE + ' The scheme adds: "' + display(_q4kb[1].text) + '".')
shown('The scheme adds: "' + display(_q4kb[1].text) + '".')

# ── Q5 The periodic table at 150 ─────────────────────────────────────────────
Q5 = FIG + 'paper-q5'
_q5a = [P.items(k('5', 'a', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in its] for its in _q5a] == [[None], [None], ['[5 + 4 + 2]']], _q5a
C.add([k('5', 'a', r) for r in ('i', 'ii', 'iii')], 'chem-1-3', 'mendeleevs-periodic-table', [
    lift('r-1', _q5a[0][0].text, None, 'For (i).'),
    lift('r-2', _q5a[1][0].text, None, 'For (ii).'),
    lift('r-3', _q5a[2][0].text, None, 'For (iii).')],
    kind='orderedSplit', notation='[5 + 4 + 2]', total=11, figure=Q5, notes=SPLIT.format('[5 + 4 + 2]'))
# (b)(i): each definition opens with the scheme's "DEFINE 1:" / "DEFINE 2:" cue.
_q5b = P.items(k('5', 'b', 'i'))
assert [it.cell for it in _q5b] == ['[3]', '[2 × 3]'], _q5b
_d1, _d2 = _q5b[0].points(), _q5b[1].points()
assert _d1[0] == 'DEFINE 1: Atomic number:' and _d2[0] == 'DEFINE 2: Relative atomic mass:', (_d1, _d2)
C.add([k('5', 'b', 'i')], 'chem-1-2', 'atomic-number-and-relative-atomic-mass', [
    lift('r-1', _d1[0][len('DEFINE 1: '):] + ' ' + _d1[1], 3),
    lift('r-2', _d2[0][len('DEFINE 2: '):] + ' ' + _d2[1], 3,
         'The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-3', _d2[2], 3)])
print_question('paper-q5b-i-print')
C.fixed([k('5', 'b', 'ii')], 'chem-1-3', 'advantage-of-ordering-by-atomic-number')
C.fixed([k('5', 'c', 'i')], 'chem-1-3', 'why-group-18-is-inert')
C.ordered([k('5', 'c', 'ii')], 'chem-1-3', 'reactivity-of-the-halogens-down-the-group')
C.fixed([k('5', 'd', 'i')], 'chem-1-3', 'francium-in-water')
C.ordered([k('5', 'd', 'ii')], 'chem-1-3', 'products-of-francium-and-water')

# ── Q6 Fuels: isomers, cracking and tetraethyllead ───────────────────────────
# (a): six ticks over (i)-(iv), priced (5 + 5 + 2 + 2 + 2 + 2) by the order
# in which correct ticks fall, not by part.
_q6a = [P.items(k('6', 'a', r)) for r in ('i', 'ii', 'iii', 'iv')]
assert [[it.cell for it in its] for its in _q6a] == [[None], [None], [None], ['[5 + 5 + 2 + 2 + 2 + 2]']], _q6a
_names = [x.strip() + TICK for x in display(_q6a[3][0].points()[0]).split('(✓)') if x.strip()]
assert len(_names) == 3, _names
_award = ' '.join(_q6a[3][0].points()[1:])
assert _award.startswith('Award 5 marks'), _award
C.add([k('6', 'a', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-2-4', 'isomers-of-pentane', [
    lift('r-1', untick(_q6a[0][0].text), None, 'For (i).'),
    lift('r-2', untick(_q6a[1][0].text), None, 'For (ii).'),
    lift('r-3', untick(_q6a[2][0].text), None, 'For (iii).'),
    lift('r-4', untick(_names[0]), None, 'For (iv).'),
    lift('r-5', untick(_names[1]), None),
    lift('r-6', untick(_names[2]), None, 'The scheme adds: ' + ' '.join(_q6a[3][0].asides))],
    kind='orderedSplit', notation='[5 + 5 + 2 + 2 + 2 + 2]', total=18, figure=FIG + 'paper-q6a',
    notes='The scheme ticks these six points and says: "' + _award + '"')
shown('The scheme ticks these six points and says: "' + _award + '"')
C.fixed([k('6', 'b', 'i')], 'chem-2-4', 'catalytic-cracking')
C.fixed([k('6', 'b', 'ii')], 'chem-2-4', 'formula-of-the-cracked-alkane')
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'why-tetraethyllead-was-added-to-petrol')
C.fixed([k('6', 'c', 'ii')], 'chem-2-4', 'why-leaded-petrol-was-discontinued')
_q6c3 = P.items(k('6', 'c', 'iii'))
assert _q6c3[0].cell == '[17]' and _q6c3[-1].cell is None, _q6c3
_p = _q6c3[-1].points()
assert _p[0] == 'Mixing and matching from different boxes not acceptable.', _p
C.answer_only([k('6', 'c', 'iii')], 'chem-3-1', 'heat-of-combustion-of-tetraethyllead', S + 'q6c-iii',
              notes='The scheme sets out four boxed routes and adds: "' + display(_q6c3[-1].text) + '"')
shown(C.cards[-1]['notes'])

# ── Q7 Brønsted-Lowry acids and bases; the ionic product of water ────────────
Q7B = FIG + 'paper-q7b'
# (a)(i), (ii): each equation is set a little above its marker and cell, so the
# reader files (i)'s under the question's head and (ii)'s under (i); each part
# keeps its own cell (3).
_q7 = P.items(k('7'))
_q7a1 = P.items(k('7', 'a', 'i'))
_q7a2 = P.items(k('7', 'a', 'ii'))
assert [it.cell for it in _q7] == [None] and display(_q7[0].text) == 'H₂O + HCl ⇌ H₃O⁺ + Cl⁻', _q7
assert [it.cell for it in _q7a1] == ['[3]', None] and not _q7a1[0].text, _q7a1
assert display(_q7a1[1].text) == 'H₂O + NH₃ ⇌ NH₄⁺ + OH⁻', _q7a1
assert [it.cell for it in _q7a2] == ['[3]'] and not _q7a2[0].text, _q7a2
C.add([k('7', 'a', 'i')], 'chem-3-4', 'hydrochloric-acid-as-a-bronsted-lowry-acid', [
    lift('r-1', _q7[0].text, 3, 'The scheme adds: ' + ' '.join(_q7a1[0].asides))])
C.add([k('7', 'a', 'ii')], 'chem-3-4', 'ammonia-as-a-bronsted-lowry-base', [
    lift('r-1', _q7a1[1].text, 3, 'The scheme adds: ' + ' '.join(_q7a2[0].asides))])
# (iii), (iv): led by the "Explain why" the paper sets after (ii), not by (a)'s "Use equations".
_why = P.lead(k('7', 'a', 'ii'))
assert _why == 'Explain why', _why
C.fixed([k('7', 'a', 'iii')], 'chem-3-4', 'why-hydrochloric-acid-has-a-weak-conjugate-base', stem=_why)
C.fixed([k('7', 'a', 'iv')], 'chem-3-4', 'why-ammonia-has-a-strong-conjugate-acid', stem=_why)
C.fixed([k('7', 'b', 'i')], 'chem-3-4', 'expression-for-kw', figure=Q7B)
C.fixed([k('7', 'b', 'ii')], 'chem-3-3', 'self-ionisation-of-water-is-endothermic', figure=Q7B)
C.fixed([k('7', 'b', 'iii')], 'chem-3-4', 'graph-of-kw-against-temperature', figure=Q7B)
# The aside quoted under C reads "K_(w)" in the reader's script notation; shown as the page sets it, "Kw".
_r = C.cards[-1]['rows'][2]
assert 'K_(w)' in _r['contextNote'], _r
_r['contextNote'] = display(_r['contextNote'])
assert '_(' not in _r['contextNote'], _r
C.fixed([k('7', 'b', 'iv')], 'chem-3-4', 'kw-at-body-temperature-from-the-graph', figure=Q7B)
C.route([k('7', 'b', 'v')], 'chem-3-4', 'hydronium-concentration-of-pure-water-from-kw',
        fixes={'[H⁺] = √ܭw / [H⁺] = √2.3 × 10^−14 ⇒ [H⁺] = 1.51 × 10⁻⁷':
               '[H⁺] = √2.3 × 10⁻¹⁴ ⇒ [H⁺] = 1.51 × 10⁻⁷'},
        row_notes={0: 'The scheme also writes this as [H⁺] = √Kw, with the square root over the whole '
                      'of 2.3 × 10⁻¹⁴.'})
C.cards[-1]['figureKey'] = Q7B       # the table, not the scheme's working
_q7b6 = P.items(k('7', 'b', 'vi'))
assert [it.cell for it in _q7b6] == ['[3]', '[2]', '[1]', None], _q7b6
# The text layer drops the script off the second power of ten: "10⁻7" for the printed 10⁻⁷.
C.route([k('7', 'b', 'vi')], 'chem-3-4', 'temperature-of-pure-water-from-its-ph',
        fixes={'[H⁺] = inverse log (– 6.77) / [H⁺] = antilog(– 6.77) / [H⁺] = 10^–6.77 / [H⁺] = 1.69 × 10⁻7 – 1.7 × 10⁻7':
               '[H⁺] = inverse log (– 6.77) / [H⁺] = antilog(– 6.77) / [H⁺] = 10^–6.77 / [H⁺] = 1.69 × 10⁻⁷ – 1.7 × 10⁻⁷'},
        notes='The scheme adds: "' + display(_q7b6[3].text) + '"')
C.cards[-1]['figureKey'] = Q7B
shown('The scheme adds: "' + display(_q7b6[3].text) + '"', -1)

# ── Q8 Alcohols ──────────────────────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
_q8a1 = P.items(k('8', 'a', 'i'))
assert [it.cell for it in _q8a1] == ['[5]', '[5]'], _q8a1
C.add([k('8', 'a', 'i')], 'chem-4-2', 'what-a-secondary-alcohol-is', [menu_row(
    'r-1', [_q8a1[0].text, _q8a1[1].text], 1,
    'Either of these, as the scheme sets them, the second after "or", each (5). It adds: '
    + ' '.join(_q8a1[1].asides), per=5, total=5)], total=5, figure=Q8)
_q8a2 = P.items(k('8', 'a', 'ii'))
assert [it.cell for it in _q8a2] == ['[3]', '[6]', None] and _q8a2[2].text == '(6 × 1)', _q8a2
_six = raw(19, 251, 263)
assert _six == 'SIX POINTS: (6 × 1)', _six
C.add([k('8', 'a', 'ii')], 'chem-2-2', 'graph-of-boiling-points-of-alcohols', [
    lift('r-1', _q8a2[0].text, 3, 'The scheme adds: ' + ' '.join(_q8a2[0].asides)),
    lift('r-2', _q8a2[1].text, 6, 'The scheme prices the six points "' + _six + '", one mark each. It '
         'adds: ' + ' '.join(_q8a2[2].asides))], figure=Q8)
C.fixed([k('8', 'a', 'iii')], 'chem-2-2', 'boiling-points-of-primary-alcohols', figure=Q8)
C.fixed([k('8', 'a', 'iv')], 'chem-2-2', 'predicting-the-boiling-point-of-a-secondary-alcohol', figure=Q8)
# (b) and (c) stand apart from the table Q8 opens with: each is led by its own letter's sentence.
Q8B, Q8C = P.ask(k('8', 'b')), P.ask(k('8', 'c'))
assert Q8B.startswith('Consider the oxidation') and Q8C.startswith('The ester formed'), (Q8B, Q8C)
# (b)(i): (6) on the cue line; the two names priced "TWO NAMES: (2 x 3)".
_q8b1 = P.items(k('8', 'b', 'i'))
assert [it.cell for it in _q8b1] == ['[6]', None] and not _q8b1[0].text, _q8b1
_p = _q8b1[1].points()
assert len(_p) == 2 and _p[1].endswith(' (2 × 3)'), _p
assert raw(19, 501, 514) == 'TWO NAMES: (2 × 3)', raw(19, 501, 514)
C.add([k('8', 'b', 'i')], 'chem-4-2', 'products-of-oxidising-butan-1-ol', [
    lift('r-1', _p[0], 3, 'The scheme prices these points "TWO NAMES: (2 × 3)", one each.'),
    lift('r-2', _p[1][:-len(' (2 × 3)')], 3, 'The scheme adds: ' + ' '.join(_q8b1[1].asides))], stem=Q8B)
C.drawn([k('8', 'b', 'ii')], 'chem-4-2', 'structure-of-butanone', S + 'q8b-ii', stem=Q8B)
_q8b3 = P.items(k('8', 'b', 'iii'))
assert [it.cell for it in _q8b3] == ['[6]', None] and not _q8b3[0].text, _q8b3
_p = _q8b3[1].points()
assert len(_p) == 2 and _p[1].endswith(' (4 + 2)'), _p
assert raw(20, 118, 131) == 'TWO BONDS: (4 + 2)', raw(20, 118, 131)
C.add([k('8', 'b', 'iii')], 'chem-4-2', 'bonds-broken-in-oxidising-butan-2-ol', [
    lift('r-1', _p[0], None),
    lift('r-2', _p[1][:-len(' (4 + 2)')], None, 'The scheme also boxes the two bonds on a drawing of '
         'butan-2-ol; its own print is shown with the answer. It adds: ' + ' '.join(_q8b3[1].asides))],
    kind='orderedSplit', notation='[4 + 2]', total=6, figure=S + 'q8b-iii', stem=Q8B,
    notes='The scheme labels these "TWO BONDS: (4 + 2)". ' + SPLIT.format('[4 + 2]'))
shown('The scheme labels these two bonds "TWO BONDS: (4 + 2)".')
C.drawn([k('8', 'c', 'i')], 'chem-4-2', 'structure-of-methyl-propanoate', S + 'q8c-i', stem=Q8C)
C.fixed([k('8', 'c', 'ii')], 'chem-2-2', 'tetrahedral-carbons-in-methyl-propanoate', fixes={'HOW 3': '3'},
        stem=Q8C)
_q8c3 = P.items(k('8', 'c', 'iii'))
assert [it.cell for it in _q8c3] == ['[2]', None] and not _q8c3[0].text, _q8c3
_p = _q8c3[1].points()
assert len(_p) == 2 and _p[1].endswith(' (2 × 1)'), _p
assert raw(20, 498, 511) == 'TWO PRODUCTS: (2 × 1)', raw(20, 498, 511)
C.add([k('8', 'c', 'iii')], 'chem-4-2', 'products-of-base-hydrolysis-of-an-ester', [
    lift('r-1', _p[0], 1, 'The scheme prices these points "TWO PRODUCTS: (2 × 1)", one each.'),
    lift('r-2', _p[1][:-len(' (2 × 1)')], 1)], stem=Q8C)

# ── Q9 A heterogeneously catalysed decomposition ─────────────────────────────
Q9 = FIG + 'paper-q9'
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a] == ['[6]', None], _q9a
_t = display(_q9a[0].text)
assert _t == 'change in concentration per unit time (rate of change of concentration, ) of one reactant (product)', _t
C.add([k('9', 'a')], 'chem-3-2', 'definition-of-rate-of-reaction', [
    lift('r-1', _t.replace('concentration, )', 'concentration)'), 6,
         'The scheme writes the rate of change of concentration as a fraction inside the brackets, and '
         'accepts instead the rate written as a derivative of a reactant\'s or product\'s concentration '
         'with time; its own print is shown with the answer.')], figure=S + 'q9a', stem='')
# (b): the average rate is set as a fraction above (b)'s marker and cell, so
# the reader files it under (a); (b)'s first cell (3) holds no words.
_q9b = P.items(k('9', 'b'))
assert [it.cell for it in _q9b] == ['[3]', '[3]'] and not _q9b[0].text, _q9b
_f = display(_q9a[1].text)
assert _f == '0.002 500= 4.0 × 10⁻⁶ M s⁻¹ of C', _f
C.add([k('9', 'b')], 'chem-3-2', 'average-and-instantaneous-rate-from-a-graph', [
    lift('r-1', '0.002 ÷ ' + _f[len('0.002 '):].replace('500=', '500 ='), 3, FRACTION.format('0.002', '500')),
    lift('r-2', _q9b[1].text, 3)], figure=Q9)
# (c): EXPLAIN (3); DESCRIBE (9), any two of three parts (6 + 3); EXPLAIN (3).
_q9c = P.items(k('9', 'c'))
assert [it.cell for it in _q9c] == ['[3]', '[9]', '[3]'] and not _q9c[1].text, _q9c
_p = _q9c[2].points()
assert len(_p) == 4 and _p[2].endswith(' (6 + 3)'), _p
_any = raw(21, 487, 500)
assert _any == 'ANY TWO PARTS: (6 + 3)', _any
C.add([k('9', 'c')], 'chem-3-2', 'heterogeneous-catalysis-and-surface-adsorption', [
    lift('r-1', _q9c[0].text, 3, 'The scheme adds: ' + ' '.join(_q9c[0].asides)),
    menu_row('r-2', [_p[0], _p[1], _p[2][:-len(' (6 + 3)')]], 2,
             'Any two of these three parts of the theory, the first (6) and the second (3): "' + _any + '".',
             per=6, steps=[6, 3], total=9),
    lift('r-3', _p[3], 3)], total=15, figure=Q9)
# (d): EXPLAIN (6), two parts (2 x 3); then two ways, each STATE (4) and EXPLAIN (2).
_q9d = P.items(k('9', 'd'))
assert [it.cell for it in _q9d] == ['[6]', '[4]', '[2]', '[4]', '[2]', '[4]', '[2]'] and not _q9d[0].text, _q9d
_p = _q9d[1].points()
assert len(_p) == 5 and _p[3].endswith(' (2 × 3)'), _p
_w = _q9d[5].points()
assert _w[0] == 'or allow', _w
_two = raw(21, 648, 661)
assert _two == 'TWO PARTS : (2 × 3)', _two
C.add([k('9', 'd')], 'chem-3-2', 'activation-energy-and-raising-the-rate', [
    lift('r-1', _p[0], 3, 'The scheme prices this point and the next "' + _two + '", one each, or instead the pair "' + _p[2] + ' // ' + _p[3][:-len(' (2 × 3)')] + '". It adds: '
         + ' '.join(_q9d[1].asides)),
    lift('r-2', _p[1], 3),
    menu_row('r-3', [_p[4], _q9d[3].text, _w[1]], 2,
             'Any two ways (STATE), each (4); the scheme sets the third after "or allow". It adds: '
             + ' '.join(_q9d[3].asides), per=4, total=8),
    menu_row('r-4', [_q9d[2].text, _q9d[4].text, _q9d[6].text], 2,
             'And the explanation of each way stated (EXPLAIN), each (2), in the same order. The scheme '
             'adds: ' + ' '.join(dict.fromkeys(a for i in (2, 4, 6) for a in _q9d[i].asides)),
             per=2, total=4)], total=18)
print_question('paper-q9d-print')
C.fixed([k('9', 'e')], 'chem-3-3', 'is-the-reaction-an-equilibrium', figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): seven ticks over (i)-(iv), priced (6 + 6 + 3 + 3 + 3 + 3 + 1) in the
# order correct ticks fall.
_q10a = [P.items(k('10', 'a', r)) for r in ('i', 'ii', 'iii', 'iv')]
assert [[it.cell for it in its] for its in _q10a[:3]] == [[None], [None], [None]], _q10a
assert [it.cell for it in _q10a[3]] == ['[3]', '[1]', '[6 + 6 + 3 + 3 + 3 + 3 + 1]'], _q10a[3]
_iii = [x.strip() + TICK for x in display(_q10a[2][0].text).split('(✓)') if x.strip()]
_iv = display(_q10a[3][0].points()[0])
_iv = [x.strip() + TICK for x in _iv.split('(✓)') if x.strip()]
assert len(_iii) == 3 and len(_iv) == 2, (_iii, _iv)
_pen = raw(23, 527, 555)
assert _pen.startswith('[Reference to chloride radical') and _pen.endswith('(1) once (iv).]'), _pen
_award = _q10a[3][2].points()[1]
assert _award.startswith('Award 6 marks'), _award
C.add([k('10', 'a', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-4-2', 'free-radical-substitution-of-methane', [
    lift('r-1', untick(_q10a[0][0].text), None, 'For (i).'),
    lift('r-2', untick(_q10a[1][0].text), None, 'For (ii). The scheme also gives the equation, written '
         'with "uv" over the arrow and with curly arrows; its own print is shown with the answer. It adds: '
         + ' '.join(_q10a[1][0].asides)),
    lift('r-3', untick(_iii[0]), None, 'For (iii).'),
    lift('r-4', untick(_iii[1]), None),
    lift('r-5', untick(_iii[2]), None, 'The scheme adds: ' + ' '.join(_q10a[2][0].asides)),
    lift('r-6', untick(_iv[0]), None, 'For (iv).'),
    lift('r-7', untick(_iv[1]), None, 'The scheme adds: ' + ' '.join(_q10a[3][0].asides) + ' ' + _pen + ' '
         + ' '.join(_q10a[3][2].asides))],
    kind='orderedSplit', notation='[6 + 6 + 3 + 3 + 3 + 3 + 1]', total=25, figure=S + 'q10a-ii',
    notes='The scheme ticks these seven points and says: "' + _award + '" It also says: "'
          + display(P.items(k('10', 'a'))[0].text) + '"')
shown(C.cards[-1]['notes'])
print_question('paper-q10a-print')
C.fixed([k('10', 'b', 'i')], 'chem-1-2', 'atomic-energy-level')
_q10b2 = table_lines(24, (130, 100, 510, 300), 305)
assert _q10b2[0] == ('Bohr orbit', 'orbital') and len(_q10b2) == 8, _q10b2
_lines = raw(24, 311, 324)
assert _lines == 'ANY TWO LINES FROM TABLE: (2 × 3)', _lines
assert cells(k('10', 'b', 'ii')) == ['[6]', None], cells(k('10', 'b', 'ii'))
C.add([k('10', 'b', 'ii')], 'chem-1-2', 'bohr-orbit-and-atomic-orbital-compared', [menu_row(
    'r-1', [a + ' — ' + b for a, b in _q10b2[1:]], 2,
    'Any two lines of the scheme\'s table, each its statement for the Bohr orbit, then for the orbital: "'
    + _lines + '". The scheme adds: ' + ' '.join(P.items(k('10', 'b', 'ii'))[1].asides) + ' Its own print '
    'of the table is shown with the answer.', per=3, total=6)], total=6, figure=S + 'q10b-ii')
_q10b3 = P.items(k('10', 'b', 'iii'))
assert [it.cell for it in _q10b3] == ['[6]', None], _q10b3
_dir = raw(24, 574, 600)
assert _dir == 'If separate orbitals are not labelled x, y and z they must have different orientations', _dir
C.drawn([k('10', 'b', 'iii')], 'chem-1-2', 'p-orbital-and-p-sub-level', S + 'q10b-iii',
        notes='The scheme draws the two, side by side, any one line of its table: "' + raw(24, 717, 730)
              + '". It adds: "' + _dir + '" and "' + _q10b3[1].points()[1] + '"')
shown(C.cards[-1]['notes'])
_q10b4 = P.items(k('10', 'b', 'iv'))
assert [it.cell for it in _q10b4] == ['[6]', None] and not _q10b4[0].text, _q10b4
_p = _q10b4[1].points()
assert len(_p) == 2 and _p[1].endswith(' (2 × 3)'), _p
assert raw(25, 107, 120) == 'TWO PARTS: (2 × 3)', raw(25, 107, 120)
C.add([k('10', 'b', 'iv')], 'chem-1-2', 'electron-configuration-of-nickel', [
    lift('r-1', _p[0], 3, 'The scheme prices these points "TWO PARTS: (2 × 3)", one each.'),
    lift('r-2', _p[1][:-len(' (2 × 3)')], 3, 'The scheme adds: ' + ' '.join(_q10b4[1].asides))])
C.fixed([k('10', 'b', 'v')], 'chem-1-2', 'evidence-for-atomic-energy-levels')
_q10c1 = P.items(k('10', 'c', 'i'))
assert [it.cell for it in _q10c1] == ['[12]', '[6 + 3 + 3]'], _q10c1
C.answer_only([k('10', 'c', 'i')], 'chem-1-4', 'mass-of-c3n4-from-mercury-thiocyanate', S + 'q10c-i',
              notes='The scheme prices the working (6 + 3 + 3) and adds: ' + ' '.join(_q10c1[1].asides))
shown(C.cards[-1]['notes'])
C.route([k('10', 'c', 'ii')], 'chem-1-4', 'volume-of-oxygen-to-burn-carbon-disulfide')
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'number-of-mercury-atoms-produced')
_q10c4 = P.items(k('10', 'c', 'iv'))
assert [it.cell for it in _q10c4] == ['[1]', '[1]'], _q10c4
C.answer_only([k('10', 'c', 'iv')], 'chem-1-4', 'total-moles-of-gas-formed', S + 'q10c-iv',
              notes='The scheme adds: ' + ' '.join(_q10c4[1].asides))
shown(C.cards[-1]['notes'])

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
_q11a1 = P.items(k('11', 'a', 'i'))
assert [it.cell for it in _q11a1] == ['[6]', None] and not _q11a1[0].text, _q11a1
_p = _q11a1[1].points()
assert len(_p) == 2 and _p[1].endswith(' (4 + 2)'), _p
_lab = raw(27, 104, 117)
assert _lab == 'TWO PARTS: (4 + 2)', _lab
C.add([k('11', 'a', 'i')], 'chem-2-1', 'definition-of-electronegativity', [
    lift('r-1', _p[0], None), lift('r-2', _p[1][:-len(' (4 + 2)')], None)],
    kind='orderedSplit', notation='[4 + 2]', total=6,
    notes='The scheme labels these "' + _lab + '". ' + SPLIT.format('[4 + 2]'))
shown('The scheme labels these two points "' + _lab + '".')
C.fixed([k('11', 'a', 'ii')], 'chem-2-1', 'electronegativity-across-the-second-period')
C.fixed([k('11', 'a', 'iii')], 'chem-2-1', 'bonding-in-oxygen-difluoride')
C.fixed([k('11', 'a', 'iv')], 'chem-2-2', 'shape-of-oxygen-difluoride')
# (v): the angle (3), then its reasons (1), any of four the scheme sets after "or".
_q11a5 = P.items(k('11', 'a', 'v'))
assert [it.cell for it in _q11a5] == ['[3]', '[1]'], _q11a5
_r = _q11a5[1].points()
assert [_r[1], _r[5]] == ['or', 'or'] and _r[7].endswith(' or allow') and len(_r) == 9, _r
C.add([k('11', 'a', 'v')], 'chem-2-2', 'bond-angle-in-oxygen-difluoride', [
    lift('r-1', _q11a5[0].text, 3),
    menu_row('r-2', [_r[0], ' '.join(_r[2:5]), _r[6] + ' ' + _r[7][:-len(' or allow')], _r[8]], 1,
             'Any one of these reasons, the scheme setting each after "or" and the last after "or allow" '
             '(1). It adds: ' + ' '.join(_q11a5[1].asides), per=1, total=1)], total=4)
C.drawn([k('11', 'b', 'i')], 'chem-3-3', 'kc-expression-for-bromine-monochloride', S + 'q11b-i')
_q11b2 = P.items(k('11', 'b', 'ii'))
assert _q11b2[0].cell == '[12]', _q11b2
_mix, _slip = raw(29, 667, 680), raw(29, 679, 693)
assert _mix == 'Mixing and matching boxes not acceptable.' and _slip.startswith('*Treat as'), (_mix, _slip)
C.answer_only([k('11', 'b', 'ii')], 'chem-3-3', 'percentage-decomposition-of-bromine-monochloride',
              S + 'q11b-ii', fixes={'48% First correct tick 6, each other correct tick 2 marks': '48%'},
              notes='The scheme ticks four steps, A to D, in each of four boxed routes (x as moles of Br₂ '
                    'formed or of BrCl decomposed, in moles or in moles per litre): "First correct tick 6, '
                    'each other correct tick 2 marks". The first two routes are shown with the answer. It '
                    'adds: "' + _mix + '" and "' + _slip + '"')
shown(C.cards[-1]['notes'])
C.fixed([k('11', 'b', 'iii')], 'chem-3-3', 'pressure-colour-and-dissociation-of-bromine-monochloride')
Q11A = FIG + 'paper-q11c-a'
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'the-greenhouse-effect', figure=Q11A)
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'why-the-greenhouse-effect-is-essential', figure=Q11A)
for r, concept in (('iii', 'human-activities-enhancing-the-greenhouse-effect'),
                   ('iv', 'why-greenhouse-gases-differ-in-impact')):
    _it = P.items(ka('11', 'c', r, 'A'))
    assert [it.cell for it in _it] == ['[6]', None] and not _it[0].text, _it
    _t = display(_it[1].text)
    assert _t.endswith(' (4 + 2)'), _t
    _o = [x.strip() for x in _t[:-len(' (4 + 2)')].split('//')]
    if _o[-1] == 'etc':
        _o = _o[:-1]
        _etc = ' The scheme ends its list with "etc".'
    else:
        _etc = ''
    C.add([ka('11', 'c', r, 'A')], 'chem-4-3', concept, [menu_row(
        'r-1', _o, 2, 'Any two of these, the first (4) and the second (2): "ANY TWO: (4 + 2)".' + _etc,
        per=4, steps=[4, 2], total=6)], total=6, figure=Q11A)
assert raw(30, 212, 225) == raw(30, 293, 306) == 'ANY TWO: (4 + 2)', (raw(30, 212, 225), raw(30, 293, 306))
_q11ca5 = P.items(ka('11', 'c', 'v', 'A'))
assert [it.cell for it in _q11ca5] == ['[5 + 2]'], _q11ca5
_t = display(_q11ca5[0].text)
_cut = _t.index(' water vapour is the most')
C.add([ka('11', 'c', 'v', 'A')], 'chem-4-3', 'water-vapour-and-carbon-dioxide-as-greenhouse-gases', [
    lift('r-1', _t[:_cut], None, 'COMPARE.'),
    lift('r-2', _t[_cut:], None, 'ACCOUNT. The scheme adds: ' + ' '.join(_q11ca5[0].asides))],
    kind='orderedSplit', notation='[5 + 2]', total=7, figure=Q11A, notes=SPLIT.format('[5 + 2]'))
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-2-1', 'what-a-crystal-is')
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-2-1', 'iodine-is-a-molecular-crystal')
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-2-1', 'x-ray-crystallography')
for r, concept, fig, y in (('iv', 'why-graphite-is-a-lubricant', FIG + 'paper-q11c-b', 655),
                           ('v', 'why-silver-conducts-electricity', '', 722)):
    _it = P.items(ka('11', 'c', r, 'B'))
    assert [it.cell for it in _it] in (['[6]', '[4 +2]'], ['[6]', '[4 + 2]']) and not _it[0].text, _it
    _p = _it[1].points()
    assert len(_p) == 2, _p
    _lab = raw(30, y, y + 13)
    assert _lab.startswith('TWO POINTS:'), _lab
    C.add([ka('11', 'c', r, 'B')], 'chem-2-1', concept, [lift('r-1', _p[0], None), lift('r-2', _p[1], None)],
          kind='orderedSplit', notation='[4 + 2]', total=6, figure=fig,
          notes='The scheme labels these "' + _lab + '". ' + SPLIT.format('[4 + 2]'))
    shown('The scheme labels these two points "' + _lab + '".')


# ── review ───────────────────────────────────────────────────────────────────
def printed():
    """Every letter's printed marks: the paper sets one mark after a letter's
    last part, or -- Q7(b), Q11 -- several, one after each run of parts."""
    out = {}
    for key, last in P.marks.items():
        if not key[1]:
            continue
        at = [m for s in P.pseg if s.key[:2] == key[:2] for _n, m in s.marks_at]
        out[key] = sum(at) if at else last
    return out


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for key, reason in EXCLUDED:
        out.append(f'EXCLUDED {C.ref([key])}: {reason}')
    totals = C.letter_totals()
    marks = printed()
    for key, (got, want) in sorted(totals.items(), key=lambda kv: (int(kv[0][0]), kv[0][1])):
        line = f'Q{key[0]}({key[1]}) printed {marks[key]}, carded {got}'
        if marks[key] != want:
            line += f' (the reader keeps only the last mark printed, {want})'
        if key[0] == '11' and key[1] == 'c':
            line += ' (A and B are alternatives, 25 each)'
        out.append(line)
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
