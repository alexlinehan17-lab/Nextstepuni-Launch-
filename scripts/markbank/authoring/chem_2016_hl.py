#!/usr/bin/env python3
"""2016 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2016_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2016_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2016_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2016 hl

No 2016 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

The 2016 scheme is the labelled ("cue") layout. The paper sets several runs of
romans inside one sentence, which the census keeps as one ask while the scheme
prices them under markers of its own: Q4(a) and Q4(e) ("What is (i) the atomic
number, (ii) the mass number, of M?", one cell 2 x 3: one card each); Q6(e)
("Draw the molecular structure of (i) octane, (ii) 2,2,4-trimethylpentane,
(iii) ethylbenzene.", paper page 7, y 403-417, one cell 3 x 3: one card); Q7(a)
("(i) temperature, (ii) pressure", a cell each: a card each, showing the
sentence); Q10(b) ("Define reduction in terms of (i) ..., (ii) ...", and
"Assign oxidation numbers ... to identify (iii) ..., (iv) ...", a cell each).
The scheme sets Q10(b)'s ASSIGN under its own (ii) (page 22, y 108); Q11(a)(iii)'s
answer, "WHAT: 9.4 g K2O (6)", it prints with no "(iii)" at all (page 24, y 693),
so the reader files it under (ii): (iii)'s card takes (ii)'s last three items.

Asks the paper sets unnumbered are the letter's own card before its first roman
(Q7(a), Q11(b)) or a card each after the roman they follow, cited "— after (ii),
..." (Q3(d), Q7(a), Q10(b)). Where one part's asks would outrun a card's five
rows, or one letter sets a calculation beside its other asks, each ask is a card
cited with what it holds (Q6(c), Q7(c), Q8(c), Q11(a)(i)). Q4(k) and Q11(c) offer
alternative parts A and B. Parts whose asks need the paper's table, equations or
reaction scheme while the answer is the scheme's print take the paper's own print
as their question (Q3(b), Q6(c), Q10(b), Q10(c)(ii)).
"""
import json
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, point, read_lines, tidy  # noqa: E402

P = Printed(2016, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2016-HL-'
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

# ── Q1 Ethanoic acid in vinegar ──────────────────────────────────────────────
# (a): MEASURE, any three of four points (3 x 3), the fourth set for a pipette
# and, after it, for a burette; DILUTE, any two of four (2 x 3).
_q1a = P.items(k('1', 'a'))
assert [it.cell for it in _q1a] == ['[3 × 3]', '[2 × 3]'], _q1a
_m = _q1a[0].options()
assert len(_m) == 4 and _m[3].startswith('pipette:') and ' burette: ' in _m[3], _m
_pip, _bur = cut(_m[3], 'burette:')
_three, _two = raw(6, 149, 165, 400), raw(6, 212, 228, 400)
assert (_three, _two) == ('ANY THREE: (3 × 3)', 'ANY TWO: (2 × 3)'), (_three, _two)
_d = _q1a[1].options()
assert len(_d) == 4 and _d[0].startswith('transfer to 250'), _d
C.add([k('1', 'a')], 'chem-4-1', 'measuring-and-diluting-vinegar', [
    menu_row('r-1', _m[:3] + [_pip, _bur], 3, 'MEASURE: any three of these, (3) each: "' + _three + '". The '
             'scheme sets its fourth point for a pipette and, after it, for a burette: the one used.',
             per=3, total=9),
    menu_row('r-2', _d, 2, 'DILUTE: any two of these, (3) each: "' + _two + '". The scheme adds: '
             + ' '.join(a for a in _q1a[1].asides if not a.startswith('[any')), per=3, total=6)], total=15)
C.fixed([k('1', 'b')], 'chem-4-1', 'phenolphthalein-in-an-ethanoic-acid-titration',
        row_notes={0: 'NAME.', 1: 'WHAT.'})
# (c)(i): the answer (6), then three boxed routes of two steps (3) each, set as
# fractions side by side: the answer line, with the scheme's print of the routes.
_q1c1 = P.items(k('1', 'c', 'i'))
assert _q1c1[0].cell == '[6]' and _q1c1[-1].asides == ['[*Addition must be shown for error to be treated as slip.]'], _q1c1
C.answer_only([k('1', 'c', 'i')], 'chem-4-1', 'moles-of-sodium-hydroxide-in-a-portion', S + 'q1c-i',
              notes='The scheme sets out three boxed routes, each two steps priced (3), and adds: '
                    + _q1c1[-1].asides[0])
shown('The scheme prices each of its three routes in two steps, (3) each, and adds: ' + _q1c1[-1].asides[0])
# (c)(ii): the answer (6), then two boxed routes; the first is two lines of text.
_q1c2 = P.items(k('1', 'c', 'ii'))
assert _q1c2[0].cell == '[6]' and display(_q1c2[0].text) == '0.00008 (8 × 10⁻⁵) moles per cm³', _q1c2
_st = [raw(6, 488, 504, 95, 230), tidy(raw(6, 514, 530, 95, 230) + ' ' + raw(6, 527, 543, 95, 281))]
assert _st == ['0.0015 moles CH₃COOH', '0.0015 ÷ 18.75 = 0.00008 (8 × 10⁻⁵) moles per cm³ (3)'], _st
_st[1] = _st[1][:-len(' (3)')]
C.add([k('1', 'c', 'ii')], 'chem-4-1', 'moles-of-ethanoic-acid-per-cm3-of-diluted-vinegar', [
    lift('r-1', _st[0], 3),
    lift('r-2', _st[1], 3, 'The scheme accepts a second route, from 18.75 × M = 25 × 0.06 to M = 0.08 M (3) and '
         'then 0.08 over 1000 (3); its own print of both is shown with the answer.')],
    figure=S + 'q1c-ii',
    notes='The scheme gives the answer, ' + display(_q1c2[0].text) + ', priced (6), then two boxed routes of two '
          'steps (3) each; the steps here are its first route.')
shown('The scheme gives the answer as "' + display(_q1c2[0].text) + '" (6).')
# (d)(i): the answer (3), by either of two one-step routes (3).
_q1d1 = P.items(k('1', 'd', 'i'))
assert [it.cell for it in _q1d1] == ['[3]'] * 3 and display(_q1d1[0].text) == '0.8 M', _q1d1
_r = [display(_q1d1[1].text), display(_q1d1[2].text).lstrip('/ ')]
assert _r == ['0.00008 × 1000 × 10 = 0.8 moles/L', '0.08 (Molarity***) × 10 = 0.8 moles/L'], _r
C.add([k('1', 'd', 'i')], 'chem-4-1', 'molarity-of-ethanoic-acid-in-the-original-vinegar', [menu_row(
    'r-1', _r, 1, 'Either route, the second after "/": the scheme gives the answer, 0.8 M, priced (3), and prices '
    'each route (3).', per=3, total=3)], total=3)
# (d)(ii): the answer (6), by either of two routes of two steps (3) each.
_q1d2 = P.items(k('1', 'd', 'ii'))
assert [it.cell for it in _q1d2] == ['[6]', '[3]', '[3]', '[3]', '[3]'], _q1d2
_a1 = [raw(6, 650, 666, 95, 200), '48 ÷ 10 = 4.8 g/100 cm³ = 4.8 % (w/v)']
_a2 = [raw(6, 650, 666, 320, 545), raw(6, 669, 686, 320, 545)]
assert _a1[0] == '0.8 × 60* = 48 g/L' and _a2 == ['0.8 ÷ 10 = 0.08 moles/100 cm³ (3)',
                                                  '0.08 × 60* = 4.8 g/100 cm³ = 4.8 % (w/v) (3)'], (_a1, _a2)
_a2 = [x[:-len(' (3)')] for x in _a2]
# The first route's second step sets 48 over 10 as a fraction (scheme page 6, y 665-687).
assert raw(6, 665, 688, 100, 300) == '48 10 = 4.8 g/100 cm³ = 4.8 % (w/v) (3)', raw(6, 665, 688, 100, 300)
_slip = raw(6, 703, 719)
assert _slip == '[*Addition must be shown for error to be treated as slip]', _slip
C.add([k('1', 'd', 'ii')], 'chem-4-1', 'ethanoic-acid-in-vinegar-as-a-percentage', [
    menu_row('r-1', [_a1[0], _a2[0]], 1, 'The first step of either route, the second after "/", (3).',
             per=3, total=3),
    menu_row('r-2', [_a1[1], _a2[1]], 1, 'And the second step of that same route, (3). ' + FRACTION.format('48', '10')
             + ' The scheme adds: ' + _slip, per=3, total=3)],
    total=6, notes='The scheme gives the answer, ' + display(_q1d2[0].text) + ', priced (6), then two routes of two '
                   'steps (3) each.')
shown('The scheme gives the answer as "' + display(_q1d2[0].text) + '" (6).')
# (e): "(3 + 2)" over two points, with "[Award (3) for correct titrations in reverse order.]".
_q1e = P.items(k('1', 'e'))
assert [it.cell for it in _q1e] == ['[3 + 2]'], _q1e
C.ordered([k('1', 'e')], 'chem-4-1', 'standardising-sodium-hydroxide-from-sodium-carbonate')

# ── Q2 Identifying organic liquids and purifying benzoic acid ───────────────
Q2 = FIG + 'paper-q2'
# (a): the reagent (3); then "decolourises // if unsaturated" or, after "or",
# "no change in colour // if saturated" (2 x 3), one point each.
_q2a = P.items(k('2', 'a'))
assert [it.cell for it in _q2a] == ['[3]', '[2 × 3]'], _q2a
_w = _q2a[1].points()
assert _w == ['decolourises (changes to colourless, colour disappears)', 'if unsaturated', 'no change in colour',
              'if saturated'], _w
assert raw(7, 129, 145) == 'or', raw(7, 129, 145)
C.add([k('2', 'a')], 'chem-2-4', 'testing-a-hydrocarbon-for-unsaturation', [
    lift('r-1', _q2a[0].text, 3),
    menu_row('r-2', [_w[0], _w[2]], 1, 'One of these, the scheme setting the second after "or"; it prices the two '
             'points of each (2 × 3), one each. The scheme adds: ' + ' '.join(_q2a[1].asides), per=3, total=3),
    menu_row('r-3', [_w[1], _w[3]], 1, 'And the second point of that same wording, (3).', per=3, total=3)],
    total=9, figure=Q2)
# (b)(i): DEDUCE (3); DESCRIBE, three points (3 x 3).
C.fixed([k('2', 'b', 'i')], 'chem-4-2', 'ethanal-and-its-easy-oxidation', figure=Q2,
        row_notes={0: 'DEDUCE.', 1: 'DESCRIBE.'})
# (b)(ii): IDENTIFY (2 x 3), "E: ethanoic acid (CH3COOH) /" followed by a box of
# the two structures (scheme page 7, x 391-481, y 363-463); WHAT (3).
_q2b2 = P.items(k('2', 'b', 'ii'))
assert [it.cell for it in _q2b2] == ['[2 × 3]', '[3]'] and display(_q2b2[0].text).endswith('(CH₃COOH) /'), _q2b2
C.fixed([k('2', 'b', 'ii')], 'chem-4-2', 'eugenol-and-ethanoic-acid-with-water-and-cyclohexane',
        figure=S + 'q2b-ii',
        row_notes={0: 'IDENTIFY. The scheme sets the structures of eugenol and ethanoic acid in a box beside these '
                      'two answers, after "/"; its own print is shown with the answer.', 2: 'WHAT.'})
C.fixed([k('2', 'b', 'iii')], 'chem-4-2', 'ethanoic-acid-and-magnesium', figure=Q2)
C.fixed([k('2', 'c', 'i')], 'chem-u2', 'measuring-the-melting-point-of-benzoic-acid', figure=Q2)
C.fixed([k('2', 'c', 'ii')], 'chem-u2', 'melting-point-range-and-purity', figure=Q2)
C.fixed([k('2', 'c', 'iii')], 'chem-u2', 'purifying-benzoic-acid', figure=Q2)

# ── Q3 The catalytic decomposition of hydrogen peroxide ──────────────────────
Q3T = FIG + 'paper-q3-table'
# (a): DRAW, two points (4 + 4), each an examiner's bracket set in it; the
# scheme's drawings A, B, C, X and Y, which the points name, are shown with the answer.
_q3a = P.items(k('3', 'a'))
assert [it.cell for it in _q3a] == ['[4 + 4]'], _q3a
_p1, _p1x = cut(raw(8, 60, 101, 130), '[hydrogen')
_p2 = raw(8, 98, 114, 130)
_p2x = raw(8, 111, 127, 130, 420)
assert _p1 == ('both reactants in flask (reaction vessel), e.g. A, B or C below, and one reactant labelled with '
               'name or formula'), _p1
assert _p1x == '[hydrogen peroxide added from dropping funnel not acceptable] //', _p1x
assert _p2 == 'flask connected to graduated container, e.g. X or Y below, for oxygen collection /', _p2
assert _p2x == '[graduations marked or collecting graduated container labelled]', _p2x
C.add([k('3', 'a')], 'chem-u2', 'apparatus-for-collecting-oxygen-from-hydrogen-peroxide', [
    lift('r-1', _p1, 4, 'The scheme prices its two points (4 + 4), and adds: ' + _p1x[:-len(' //')]
         + ' Its own drawings are shown with the answer.'),
    lift('r-2', _p2.rstrip('/ '), 4, 'The scheme adds, after "/": ' + _p2x)], figure=S + 'q3a')
# (b): the axes (3) and scales (3), the two curves (6 + 3), the same volume (3).
_q3b = P.items(k('3', 'b'))
assert [it.cell for it in _q3b][:3] == ['[3]', '[6 + 3]', '[3]'], _q3b
_ax = raw(8, 313, 329, 130)
assert _ax == 'both axes correctly labelled (V / volume / cm³ / oxygen / O₂ / time / t / minutes / min)(3)', _ax
_sc = raw(8, 335, 351, 130, 400)
assert _sc == 'appropriate, correct numeric scales on both axes', _sc
_cv = _q3b[1].options()
assert len(_cv) == 2 and _cv[0].endswith('run A') and _cv[1].endswith('run B'), _cv
C.add([k('3', 'b')], 'chem-3-2', 'graph-of-oxygen-volume-against-time-for-two-runs', [
    lift('r-1', _ax[:-len('(3)')], 3),
    lift('r-2', _sc, 3),
    menu_row('r-3', _cv, 2, 'The two curves, the first (6) and the second (3), as the scheme prices them '
             '"(6 + 3)".', per=6, steps=[6, 3], total=9),
    lift('r-4', _q3b[2].text, 3, 'The scheme adds: ' + ' '.join(_q3b[2].asides) + ' Its own graph is shown with '
         'the answer.')], total=18, figure=S + 'q3b')
print_question('paper-q3b-print')
# (c): the answer (6); the scheme's box works it from a tangent at 4 minutes,
# set as a fraction, priced (6).
_q3c = P.items(k('3', 'c'))
assert [it.cell for it in _q3c] == ['[6]', '[6]'] and _q3c[1].asides == [
    '[Deduct 1 mark if tangent correctly drawn at 4 minutes on curve B.]'], _q3c
C.answer_only([k('3', 'c')], 'chem-3-2', 'instantaneous-rate-from-a-tangent', S + 'q3c',
              notes='The scheme boxes the working, any two points from a tangent drawn at 4 minutes on curve A, '
                    'worked to 8.6 [8.2 – 9.5] cm³ oxygen per minute, priced (6).')
shown('The scheme works it from any two points on a tangent drawn at 4 minutes on curve A, and adds: '
      + _q3c[1].asides[0])
# (d)(i)-(ii): one cell (2 x 3), one each; WHAT and SUGGEST, set unnumbered after
# (ii) under (12), are a card each.
_q3d = [P.items(k('3', 'd', r)) for r in ('i', 'ii')]
assert [[it.cell for it in its] for its in _q3d] == [[None], ['[2 × 3]', '[3]', '[3]']], _q3d
assert display(_q3d[0][0].text) == 'A //' and display(_q3d[1][0].text) == 'B', _q3d
C.add([k('3', 'd', 'i'), k('3', 'd', 'ii')], 'chem-3-2', 'which-run-finished-first-and-started-slower', [
    lift('r-1', 'A', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'B', 3, 'For (ii).')], figure=Q3T,
    qtext=P.ask(k('3', 'd')) + ' (i) ' + P.ask(k('3', 'd', 'i')) + ' (ii) '
    + cut(P.ask(k('3', 'd', 'ii')), 'What type of catalysis')[0], stem=C.context(k('3', 'd')))
_after = cut(P.ask(k('3', 'd', 'ii')), 'What type of catalysis')[1]
_what, _suggest = cut(_after, 'Suggest how')
assert _what == 'What type of catalysis was involved in the reactions?' and _suggest.endswith('parts (i) and (ii).'), _after
_wt = _q3d[1][1]
assert display(_wt.text) == 'surface adsorption / heterogeneous [Accept ‘surface absorption’]', _wt
C.add([k('3', 'd')], 'chem-3-2', 'heterogeneous-catalysis-of-hydrogen-peroxide', [
    lift('r-1', 'surface adsorption / heterogeneous', 3, 'The scheme adds: [Accept ‘surface absorption’]')],
    qtext=_what, figure=Q3T, cid='q3-d-catalysis-type', ref_suffix='after (ii), type of catalysis')
C.add([k('3', 'd')], 'chem-3-2', 'how-the-two-catalysts-differed', [
    lift('r-1', _q3d[1][2].text, 3, 'The scheme adds: ' + ' '.join(_q3d[1][2].asides))],
    qtext=_suggest, figure=Q3T, cid='q3-d-catalyst-difference', ref_suffix='after (ii), the catalysts',
    stem=tidy(C.context(k('3', 'd')) + ' ' + C.cards[-2]['questionText']))
C.fixed([k('3', 'e', 'i')], 'chem-u2', 'hazard-of-hydrogen-peroxide', figure=FIG + 'paper-q3e')
C.fixed([k('3', 'e', 'ii')], 'chem-u2', 'hazard-of-manganese-iv-oxide', figure=FIG + 'paper-q3e')

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
# (a): the paper sets (i) and (ii) inside one sentence; the scheme prices them
# with one cell (2 x 3) under markers of its own.
C.fixed([k('4', 'a')], 'chem-1-2', 'atomic-and-mass-number-of-a-dipositive-ion', deep=True,
        row_notes={0: 'For (i).', 1: 'For (ii).'}, notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-2', 'thomsons-plum-pudding-model', notes=Q4_NOTE)
# (c): two wordings, the second after "or", each two points (2 x 3).
_q4c = P.items(k('4', 'c'))
assert [it.cell for it in _q4c] == ['[2 × 3]'] and raw(11, 261, 276) == 'or', _q4c
_w = _q4c[0].points()
assert len(_w) == 4 and _w[0] == 'nitrogen is relatively stable' and _w[2].startswith('oxygen is'), _w
C.add([k('4', 'c')], 'chem-1-3', 'first-ionisation-energies-of-nitrogen-and-oxygen', [
    menu_row('r-1', [_w[0], _w[2]], 1, 'One of these wordings, the scheme setting the second after "or"; it prices '
             'the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_w[1], _w[3]], 1, 'And the second point of that same wording, (3). The scheme adds, under '
             'each: ' + _q4c[0].asides[0], per=3, total=3)], total=6, notes=Q4_NOTE)
# (d): five pairs, each after "or", each a statement for the sigma bond and one
# for the pi bond (2 x 3); the first pair's aside is set under it.
_pairs = [(raw(11, 380, 396, 130), raw(11, 393, 409, 130)), (raw(11, 441, 457.5, 130), raw(11, 454, 470, 130)),
          (raw(11, 497, 513, 130), raw(11, 510, 526, 130)), (raw(11, 545, 561, 130), raw(11, 558, 574, 130)),
          (raw(11, 608, 623, 130), raw(11, 620, 649, 130))]
assert all(a.endswith(' //') for a, _b in _pairs) and [b[:6] for _a, b in _pairs] == [
    'pi (π)', 'pi (π)', 'pi (π)', 'pi (π)', 'sigma '], _pairs
assert [raw(11, y - 1, y + 16) for y in (424, 480, 528, 584)] == ['or'] * 4
_q4d = P.items(k('4', 'd'))
assert [it.cell for it in _q4d] == ['[2 × 3]'], _q4d
_orb = raw(11, 406, 422)
assert _orb == '[Orbitals need not be mentioned twice.] [Allow ‘collision’ of orbitals.]', _orb
C.add([k('4', 'd')], 'chem-2-1', 'sigma-and-pi-bonds-distinguished', [
    menu_row('r-1', [a[:-len(' //')] for a, _b in _pairs], 1, 'One of these, the scheme setting each after "or"; '
             'it prices the two points of each pair (2 × 3), one each. Under the first pair it adds: ' + _orb,
             per=3, total=3),
    menu_row('r-2', [b for _a, b in _pairs], 1, 'And the second point of that same pair, (3). The scheme adds: '
             + _q4d[0].asides[0], per=3, total=3)], total=6, notes=Q4_NOTE)
# (e): the paper sets (i) and (ii) inside one sentence; the scheme prices them
# with one cell (2 x 3). The formulae are set in a large font the text layer
# reads without its scripts ("H3PO4", "HPO4" and "2–" a line of its own,
# scheme page 11, y 684-717).
_q4e = P.items(k('4', 'e'), deep=True)
assert [it.cell for it in _q4e] == ['[2 × 3]'] and _q4e[0].text == 'H3PO4 // HPO4 2–', _q4e
C.add([k('4', 'e')], 'chem-3-4', 'conjugate-acid-and-base-of-dihydrogenphosphate', [
    lift('r-1', 'H₃PO₄', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'HPO₄²⁻', 3, 'For (ii).')], notes=Q4_NOTE,
    qtext=P.rearranged(P.ask(k('4', 'e')), 'H₂PO₄ –.', 'H₂PO₄⁻.'))
C.fixed([k('4', 'f')], 'chem-2-3', 'gay-lussacs-law-of-combining-volumes', notes=Q4_NOTE)
# (g): the answer (6), then the working, two steps (3) each, the second a fraction.
_q4g = P.items(k('4', 'g'))
assert [it.cell for it in _q4g] == ['[6]', '[3]', '[3]'] and display(_q4g[1].text) == 'Mr = 132*', _q4g
assert raw(12, 178, 203, 140, 300) == '= 1.65 132 = 0.0125 / 0.013 moles', raw(12, 178, 203, 140, 300)
C.add([k('4', 'g')], 'chem-1-4', 'moles-of-cinnamaldehyde-in-a-mass', [
    lift('r-1', _q4g[1].text, 3),
    lift('r-2', '1.65 ÷ 132 = 0.0125 / 0.013 moles', 3, FRACTION.format('1.65', '132') + ' The scheme adds: '
         + ' '.join(_q4g[2].asides))],
    figure=FIG + 'paper-q4g', notes=Q4_NOTE + ' The scheme gives the answer, ' + display(_q4g[0].text)
    + ', priced (6), then the working that earns it, two steps (3) each.')
shown('The scheme gives the answer as "' + display(_q4g[0].text) + '" (6).')
C.fixed([k('4', 'h')], 'chem-u2', 'test-for-the-sulfite-ion', notes=Q4_NOTE)
# (i): two wordings, the second after "or", each two points (2 x 3).
_q4i = P.items(k('4', 'i'))
assert [it.cell for it in _q4i] == ['[2 × 3]'] and raw(12, 344, 359) == 'or', _q4i
_w = _q4i[0].points()
assert len(_w) == 4 and _w[1] == 'for reaction to take place between them', _w
C.add([k('4', 'i')], 'chem-3-2', 'activation-energy', [
    menu_row('r-1', [_w[0], _w[2]], 1, 'One of these wordings, the scheme setting the second after "or"; it prices '
             'the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_w[1], _w[3]], 1, 'And the second point of that same wording, (3). The scheme adds: '
             + _q4i[0].asides[0], per=3, total=3)], total=6, notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-4-2', 'principle-of-infrared-spectrometry', notes=Q4_NOTE, figure=FIG + 'paper-q4j')
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'removing-acidic-gases-from-chimney-waste', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-2-1', 'x-ray-crystallography', notes=Q4_NOTE)

# ── Q5 The hydrogen spectrum and electron configuration ──────────────────────
Q5A = FIG + 'paper-q5a'
C.fixed([k('5', 'a', 'i')], 'chem-1-2', 'ground-state-and-excited-states', figure=Q5A)
C.fixed([k('5', 'a', 'ii')], 'chem-1-2', 'exciting-the-electron-in-hydrogen', figure=Q5A)
# (a)(iii): EXPLAIN, three points (3 x 3); WHAT (3). The first point sets
# "(En>2)" with its "n>2" subscript, which the reader writes "(E_(n>2))".
C.fixed([k('5', 'a', 'iii')], 'chem-1-2', 'origin-of-the-balmer-series', figure=Q5A,
        fixes={'excited electron falls back from n = 3, 4, etc / excited electron falls back from n = 3, etc / '
               'excited electron falls back from n > 2 (E_(n>2)) / excited electron falls from higher energy levels':
               'excited electron falls back from n = 3, 4, etc / excited electron falls back from n = 3, etc / '
               'excited electron falls back from n > 2 (En>2) / excited electron falls from higher energy levels'},
        row_notes={0: 'EXPLAIN.', 3: 'WHAT.'})
C.fixed([k('5', 'a', 'iv')], 'chem-1-2', 'no-yellow-line-in-the-hydrogen-spectrum', figure=Q5A)
# (b): DESCRIBE (3 x 3), a table of three methods, three steps each (scheme page
# 14, between its rules). Two cells run past a line the scheme's text sets
# apart from them: the first method's "(HCl)" and the second's "Bunsen flame".
_q5b = P.items(k('5', 'b'))
assert [it.cell for it in _q5b][:4] == ['[3 × 3]', '[3]', '[3]', '[3]'], _q5b
_s1 = [raw(14, 75, 142, 150, 262), raw(14, 80, 149, 262, 372), raw(14, 94, 136, 372, 492)]
_hcl = raw(14, 139, 155, 150, 262)
_s2 = [raw(14, 158, 200, 150, 262), raw(14, 152, 193, 262, 372), raw(14, 158, 200, 372, 492)]
_bf = raw(14, 190, 206, 262, 372)
_s3 = [raw(14, 202, 245, 150, 262), raw(14, 202, 245, 262, 372), raw(14, 202, 245, 372, 492)]
assert _s1 == ['clean a platinum (nichrome) wire* (rod, probe) in concentrated hydrochloric acid',
               'soak wood (splint, stick) overnight in water / use damp (wet) wood (splint, stick)',
               'prepare a solution of the given salt in water and ethanol (propanol)'] and _hcl == '(HCl)', _s1
assert _s2 == ['dip rod in salt and hold salt in hot (blue) part of Bunsen flame',
               'dip splint (stick) in salt and hold salt in hot (blue) part of',
               'spray solution onto (into) hot (blue) part of Bunsen flame'] and _bf == 'Bunsen flame', _s2
assert _s3 == ['red (crimson) colour is a positive result for lithium'] * 3, _s3
_star = [raw(14, 250, 266), raw(14, 263, 279)]
assert _star == ['*[Allow ‘inoculating loop’, or ‘spatula’ for ‘platinum wire’.]',
                 '[Clear labelled diagram for some or all points acceptable.]'], _star
assert raw(14, 62, 78) == 'Method 1 Method 2 Method 3', raw(14, 62, 78)
C.add([k('5', 'b')], 'chem-u2', 'flame-test-for-lithium', [
    menu_row('r-1', _s1, 1, 'DESCRIBE: the first step of the one method used, (3). The scheme sets three methods '
             'side by side in a table, priced (3 × 3); the first method\'s step ends "(HCl)" on a line of its '
             'own. It adds: ' + ' '.join(_star) + ' Its own print of the table is shown with the answer.',
             per=3, total=3),
    menu_row('r-2', _s2, 1, 'The second step of that same method, (3); the second method\'s step ends "Bunsen '
             'flame" on a line of its own.', per=3, total=3),
    lift('r-3', _s3[0], 3, 'The last step, the same for each method.')], total=9, figure=S + 'q5b')
# (c): DEFINE, two wordings, the second after "or", each two points (2 x 3);
# DISTINGUISH (3); WRITE (4); EXPLAIN (4).
_q5c = P.items(k('5', 'c'))
assert [it.cell for it in _q5c] == ['[2 × 3]', '[3]', '[4]', '[4]'] and raw(14, 340, 356) == 'or', _q5c
_w = _q5c[0].points()
assert len(_w) == 4 and _w[2] == 'approximate solution', _w
C.add([k('5', 'c')], 'chem-1-2', 'orbitals-sublevels-and-the-configuration-of-calcium', [
    menu_row('r-1', [_w[0], _w[2]], 1, 'DEFINE: one of these wordings, the scheme setting the second after "or"; '
             'it prices the two points of each (2 × 3), one each. It adds: ' + ' '.join(_q5c[0].asides),
             per=3, total=3),
    menu_row('r-2', [_w[1], _w[3]], 1, 'And the second point of that same wording, (3).', per=3, total=3),
    lift('r-3', _q5c[1].text, 3, 'DISTINGUISH.'),
    lift('r-4', _q5c[2].text, 4, 'WRITE. The scheme adds: ' + ' '.join(_q5c[2].asides)),
    lift('r-5', _q5c[3].text, 4, 'EXPLAIN.')], total=17)

# ── Q6 Oil refining ──────────────────────────────────────────────────────────
Q6 = FIG + 'paper-q6'
C.fixed([k('6', 'a')], 'chem-2-4', 'fractional-distillation-of-crude-oil', figure=Q6,
        row_notes={0: 'NAME.', 1: 'IDENTIFY.'})
C.fixed([k('6', 'b', 'i')], 'chem-2-4', 'a-use-for-kerosene', figure=Q6)
C.fixed([k('6', 'b', 'ii')], 'chem-2-4', 'a-use-for-the-residue', figure=Q6)
# (c): NAME (3), NAME (3), EXPLAIN (3); CALCULATE (9), two boxed routes of
# three steps (3) each. Seven rows outrun a card, so the calculation is a card
# of its own on the part, each cited with the asks it holds.
_q6c = P.items(k('6', 'c'))
assert [it.cell for it in _q6c] == ['[3]'] * 3 + ['[9]'] + ['[3]'] * 6 and display(_q6c[3].text) == '237.6 kJ', _q6c
Q6C_NAMES, Q6C_CALC = cut(P.ask(k('6', 'c')), 'Calculate the heat')
assert Q6C_NAMES.endswith('according to the following balanced equation. Explain why these conversions are '
                          'desirable.') and Q6C_CALC.endswith('kJ mol⁻¹ respectively.'), (Q6C_NAMES, Q6C_CALC)
C.add([k('6', 'c')], 'chem-2-4', 'isomerisation-and-dehydrocyclisation', [
    lift('r-1', _q6c[0].text, 3, 'NAME.'), lift('r-2', _q6c[1].text, 3, 'NAME.'),
    lift('r-3', _q6c[2].text, 3, 'EXPLAIN.')],
    qtext=Q6C_NAMES, figure=FIG + 'paper-q6c-eq', cid='q6-c-names', ref_suffix='the processes and why')
_r1 = [tidy(raw(15, 330, 346, 140, 335) + ' ' + raw(15, 330, 346, 360)), tidy(raw(15, 343, 360, 140, 335) + ' '
       + raw(15, 343, 360, 360)), tidy(raw(15, 363, 380, 140, 335) + ' ' + raw(15, 363, 380, 360))]
assert _r1 == ['C₈H₁₈ → 8C + 9H₂ ΔH = 250.1 kJ (3)', '8C + 5H₂ → C₈H₁₀ ΔH = –12.5 kJ (3)',
               'C₈H₁₈ → C₈H₁₀ + 4H₂ ΔH = 237.6 kJ (3)'], _r1
_r1 = [x[:-len(' (3)')] for x in _r1]
_r2 = [raw(15, 413, 430, 140), raw(15, 427, 444, 140), raw(15, 441, 458, 140), raw(15, 454, 471, 140)]
assert _r2 == ['ΔHreaction = ΣΔHf(products) – ΣΔHf(reactants)', 'ΔHreaction = –12.5 (3) – [–250.1] (3)',
               'or ΔHreaction = –12.5 (3) + 250.1 (3)', '= 237.6 kJ mol⁻¹ (3)'], _r2
C.add([k('6', 'c')], 'chem-3-1', 'heat-of-reaction-for-dehydrocyclisation-of-octane', [
    menu_row('r-1', [_r1[1], 'ΔHreaction = –12.5'], 1, 'The heat of formation of ethylbenzene, (3): as the '
             'second equation of the scheme\'s first route, or as the products\' term of its second, after "or": "'
             + _r2[0] + '".', per=3, total=3),
    menu_row('r-2', [_r1[0], '– [–250.1]', '+ 250.1'], 1, 'That of octane, (3): the first equation of the first '
             'route, or subtracted in the second, "– [–250.1]", or written "+ 250.1".', per=3, total=3),
    menu_row('r-3', [_r1[2], _r2[3][:-len(' (3)')]], 1, 'The heat of reaction, (3), from either route.',
             per=3, total=3)],
    total=9, figure=S + 'q6c', qtext=Q6C_CALC, cid='q6-c-calculation', ref_suffix='heat of reaction',
    notes='The scheme gives the answer, 237.6 kJ, priced (9), then two boxed routes of three steps (3) each, the '
          'second after "or"; its own print of both is shown with the answer.')
shown('The scheme gives the answer as "237.6 kJ" (9); its own print of both routes is shown with the answer.')
print_question('paper-q6c-calc-print')
C.fixed([k('6', 'd')], 'chem-2-4', 'the-third-product-of-cracking-c18h38', fixes={'C7H14': 'C₇H₁₄'})
# (e): the paper sets (i), (ii) and (iii) inside one sentence; the scheme draws
# the three structures in a table under one cell (3 x 3).
_q6e = P.items(k('6', 'e', 'iii'))
assert [it.cell for it in _q6e] == ['[3 × 3]'] and len(_q6e[0].asides) == 2, _q6e
assert [raw(15, 551, 566, 50, 110), raw(15, 551, 566, 260, 400), raw(15, 551, 566, 430)] == [
    '(i) octane', '(ii) 2,2,4-trimethylpentane', '(iii) ethylbenzene']
C.add([k('6', 'e')], 'chem-2-4', 'structures-of-octane-isooctane-and-ethylbenzene', [
    lift('r-1', 'octane', 3, 'For (i): its structure, drawn. The scheme prices the three structures (3 × 3), one '
         'each, and draws them in a table, shown with the answer. It adds: ' + ' '.join(_q6e[0].asides)),
    lift('r-2', '2,2,4-trimethylpentane', 3, 'For (ii): its structure, drawn.'),
    lift('r-3', 'ethylbenzene', 3, 'For (iii): its structure, drawn; the scheme draws it two ways, the second after '
         '"/".')],
    figure=S + 'q6e', qtext=P.ask(k('6', 'e')) + ' (iii) ' + P.ask(k('6', 'e', 'iii')))

# ── Q7 The Contact process equilibrium ───────────────────────────────────────
# (a): STATE (3 + 2), the letter's own ask before (i); the paper then sets (i)
# and (ii) inside one sentence, each priced PREDICT // EXPLAIN (2 x 3); the
# EXPLAIN set after (ii) is a card of its own.
_q7a = P.items(k('7', 'a'))
assert [it.cell for it in _q7a] == ['[3 + 2]'] and len(_q7a[0].asides) == 1, _q7a
Q7A_STATE, Q7A_USE = cut(P.ask(k('7', 'a')), 'Use Le Châtelier')
assert Q7A_STATE == 'State Le Châtelier’s principle.', Q7A_STATE
C.ordered([k('7', 'a')], 'chem-3-3', 'le-chateliers-principle', qtext=Q7A_STATE)
Q7A_SENTENCE, Q7A_WHY = cut(Q7A_USE + ' (i) ' + P.ask(k('7', 'a', 'i')) + ' (ii) ' + P.ask(k('7', 'a', 'ii')),
                            'Explain why')
assert Q7A_SENTENCE.endswith('(ii) pressure, that would maximise the yield of sulfur trioxide.') and \
    Q7A_WHY == 'Explain why the temperature conditions predicted are not used industrially.', (Q7A_SENTENCE, Q7A_WHY)
# Each PREDICT's aside is set under it, between it and the EXPLAIN (page 16, y 159 and 247).
_q7a1 = P.items(k('7', 'a', 'i'))
assert [it.cell for it in _q7a1] == ['[2 × 3]'] and _q7a1[0].asides == ['[Allow ‘decrease in temperature’.]'], _q7a1
_pt = [raw(16, 145, 161, 160).rstrip('/ '), raw(16, 170, 225, 160, 515)]
assert _pt[0] == 'low temperature' and _pt[1].startswith('favours (results in, produces more) exothermic') and \
    _pt[1].endswith('reverse reaction which is endothermic'), _pt
C.add([k('7', 'a', 'i')], 'chem-3-3', 'temperature-for-the-best-yield-of-sulfur-trioxide', [
    lift('r-1', _pt[0], 3, 'For (i): PREDICT. The scheme prices these points (2 × 3), one each, and adds: '
         + _q7a1[0].asides[0]),
    lift('r-2', _pt[1], 3, 'EXPLAIN.')], qtext=Q7A_SENTENCE, stem=C.context(k('7', 'a')))
_q7a2 = P.items(k('7', 'a', 'ii'))
assert [it.cell for it in _q7a2] == ['[2 × 3]', '[3]'], _q7a2
_pp = _q7a2[0].points()
assert len(_pp) == 2 and _pp[0] == 'high pressure', _pp
C.add([k('7', 'a', 'ii')], 'chem-3-3', 'pressure-for-the-best-yield-of-sulfur-trioxide', [
    lift('r-1', _pp[0], 3, 'For (ii): PREDICT. The scheme prices these points (2 × 3), one each, and adds: '
         + _q7a2[0].asides[0]),
    lift('r-2', _pp[1], 3, 'EXPLAIN. The scheme adds: ' + _q7a2[0].asides[1])], qtext=Q7A_SENTENCE,
    stem=C.context(k('7', 'a')))
C.add([k('7', 'a')], 'chem-3-3', 'why-a-low-temperature-is-not-used', [
    lift('r-1', _q7a2[1].text, 3, 'EXPLAIN.')], qtext=Q7A_WHY, cid='q7-a-industrial-temperature',
    ref_suffix='after (ii), the temperature used')
# (b): STATE (3) and EXPLAIN (3); the examiner's note under them is set on its own row.
_q7b = P.items(k('7', 'b'))
_link = raw(16, 458, 474)
assert _link == '[EXPLAIN marks linked to STATE marks.][‘Equilibrium reached faster’ insufficient on its own.]', _link
assert [it.cell for it in _q7b] == ['[3]', '[3]', None] and _q7b[2].text == _link, _q7b
C.add([k('7', 'b')], 'chem-3-3', 'a-catalyst-and-the-equilibrium-yield', [
    lift('r-1', _q7b[0].text, 3, 'STATE.'), lift('r-2', _q7b[1].text, 3, 'EXPLAIN. The scheme adds: ' + _link)])
# (c): WRITE (6), the expression set as a fraction in an equation font; CALCULATE
# (18), the answer with three boxed routes, each six steps (3), set as fractions
# and tables. Two asks, a card each.
_q7c = P.items(k('7', 'c'))
assert [it.cell for it in _q7c][:2] == ['[6]', '[18]'] and display(_q7c[0].text) == 'Kc =', _q7c
Q7C_DATA, Q7C_ASKS = cut(P.ask(k('7', 'c')), 'Write the equilibrium')
Q7C_WRITE, Q7C_CALC = cut(Q7C_ASKS, 'Calculate the value')
assert Q7C_DATA.endswith('were present.') and Q7C_WRITE.endswith('for this reaction.'), (Q7C_DATA, Q7C_WRITE)
C.add([k('7', 'c')], 'chem-3-3', 'kc-expression-for-the-contact-process', [C.mark_ask(point(
    'r-1', Q7C_WRITE, 6, 'The scheme answers with the expression set as a fraction its text cannot carry; its own '
    'print is shown with the answer.'))], qtext=Q7C_WRITE, stem=tidy(C.context(k('7', 'c')) + ' ' + Q7C_DATA),
    figure=S + 'q7c-kc', cid='q7-c-kc-expression', ref_suffix='the Kc expression')
_calc = raw(17, 85, 102, 70, 300)
assert _calc == 'CALCULATE: 196000 / 1.96 × 10⁵', _calc
_cons = raw(17, 351, 411)
assert _cons.startswith('[*Addition must be shown') and _cons.endswith('up to a maximum of 15 marks.]'), _cons
C.add([k('7', 'c')], 'chem-3-3', 'value-of-kc-for-the-contact-process', [
    lift('r-1', _calc[len('CALCULATE: '):], 18, 'The scheme prices the answer (18) and sets out three boxed routes, '
         'each six steps priced (3), as fractions and tables its text cannot carry; its own print is shown with the '
         'answer. It adds: ' + _cons)],
    qtext=Q7C_CALC, stem=tidy(C.context(k('7', 'c')) + ' ' + Q7C_DATA), figure=S + 'q7c',
    cid='q7-c-kc-value', ref_suffix='the value of Kc')

# ── Q8 Reactions of ethene ───────────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
C.fixed([k('8', 'a')], 'chem-4-2', 'ethanol-and-polyethene-in-the-scheme', figure=Q8)
C.fixed([k('8', 'b')], 'chem-4-2', 'dehydrating-ethanol-to-ethene', figure=Q8,
        row_notes={0: 'IDENTIFY.', 1: 'WHAT.', 2: 'HOW.'})
# (c): WHAT (3); DESCRIBE, five steps (3) each; EXPLAIN (3). Three asks, a card
# each (seven rows outrun a card). The scheme sets two examiner's notes in boxes
# down the left margin (page 16, x 48-123), which the reader welds into the
# steps' text: the steps are read from the answer column, the boxes quoted.
_q8c = P.items(k('8', 'c'))
assert [it.cell for it in _q8c] == ['[3]'] * 7, _q8c
Q8C_WHAT, _rest = cut(P.ask(k('8', 'c')), 'Describe in detail')
Q8C_MECH, Q8C_TEL = cut(_rest, 'Explain the effect')
_box1, _box2 = raw(18, 195, 364, 40, 125), raw(18, 374, 517, 40, 125)
assert _box1.startswith('Where a candidate refers') and _box1.endswith('but only once in (c).') and \
    _box2.startswith('Where a radical is referred') and _box2.endswith('applies each time.'), (_box1, _box2)
_steps = [raw(18, 187, 215, 130).rstrip('/ '), raw(18, 254, 295, 130, 530), raw(18, 342, 383, 130, 530),
          raw(18, 393, 421, 130, 500), raw(18, 456, 510, 130, 545)]
assert _steps[4].endswith(' (3)'), _steps[4]           # its cell, at the margin on the step's last line
_steps[4] = _steps[4][:-len(' (3)')]
_labels = [raw(18, 174, 190, 130), raw(18, 241, 257, 130), raw(18, 329, 345, 130), raw(18, 443, 459, 130)]
assert _labels == ['initiation:', 'propagation (1):', 'propagation (2):', 'termination:'], _labels
assert _steps[0] == ('homolysis (splitting, fission) of chlorine molecule (Cl₂) into free radicals (atoms, Cl●, Cl) '
                     'by ultraviolet (uv) light'), _steps[0]
assert raw(18, 212, 231, 130, 330) == 'Cl₂ uv 2Cl● / Cl₂ uv 2Cl', raw(18, 212, 231, 130, 330)
assert _steps[1].endswith('Cl + C₂H₆ → HCl + C₂H₅●') and _steps[2].endswith('C₂H₅● + Cl₂ → C₂H₅Cl + Cl') and \
    _steps[3].startswith('chain reaction occurs') and _steps[4].endswith('2C₂H₅● → C₄H₁₀'), _steps
_p1x = [raw(18, 291, 307, 130), raw(18, 304, 320, 130)]
_chain = raw(18, 418, 434, 130)
assert _p1x[0].startswith('[Hydrochloric acid') and _p1x[1].startswith('[Where C₂H₅ used') and \
    _chain == '[Accept ‘chain reaction occurs’ anywhere in (c).]', (_p1x, _chain)
C.add([k('8', 'c')], 'chem-4-2', 'substitution-of-ethane-by-chlorine', [lift('r-1', _q8c[0].text, 3)],
      qtext=Q8C_WHAT, figure=Q8, cid='q8-c-reaction-type', ref_suffix='the reaction type')
C.add([k('8', 'c')], 'chem-4-2', 'free-radical-mechanism-for-chlorinating-ethane', [
    lift('r-1', _steps[0], 3, 'Initiation. The scheme also accepts, after "/", the equation splitting Cl₂ into 2Cl● '
         '(or 2Cl) with "uv" over its arrow; its own print is shown with the answer. In a box beside the steps it '
         'adds: "' + _box1 + '"'),
    lift('r-2', _steps[1], 3, 'Propagation (1). The scheme adds: ' + ' '.join(_p1x)),
    lift('r-3', _steps[2], 3, 'Propagation (2).'),
    lift('r-4', _steps[3], 3, 'The scheme adds: ' + _chain),
    lift('r-5', _steps[4], 3, 'Termination. In a box beside the steps the scheme adds: "' + _box2 + '"')],
    qtext=Q8C_MECH, figure=S + 'q8c', cid='q8-c-mechanism', ref_suffix='the mechanism')
_tel = raw(18, 532, 586, 130, 545)
assert _tel.startswith('tetraethyllead increases the rate') and _tel.endswith('ethyl free radicals (3)'), _tel
_tel = _tel[:-len(' (3)')]
C.add([k('8', 'c')], 'chem-4-2', 'tetraethyllead-and-the-chlorination-of-ethane', [
    lift('r-1', _tel, 3, 'The scheme adds: ' + raw(18, 583, 598))],
    qtext=Q8C_TEL, cid='q8-c-tetraethyllead', ref_suffix='tetraethyllead')
# (d): NAME (3); DRAW (6), four structures in boxes; CIRCLE (3); WHAT (2).
_q8d = P.items(k('8', 'd'))
assert [it.cell for it in _q8d] == ['[3]', '[6]', '[3]', '[2]'] and not _q8d[1].text, _q8d
_note = raw(19, 151, 179)
assert _note.startswith('Note some or all of the hydrogens') and _note.endswith('[NAME and DRAW not linked.]'), _note
_circ = raw(19, 189, 204, 130, 500)
assert _circ == 'only the carbonyl group circled', _circ
C.add([k('8', 'd')], 'chem-4-2', 'ethyl-methanoate-and-its-saponification', [
    lift('r-1', _q8d[0].text, 3, 'NAME.'),
    lift('r-2', 'ethyl methanoate', 6, 'DRAW: its structure, drawn; the scheme draws it four ways, each with its '
         'carbonyl group circled, shown with the answer, and adds: "' + _note + '"'),
    lift('r-3', _circ, 3, 'CIRCLE. The scheme adds: ' + ' '.join(_q8d[2].asides)),
    lift('r-4', _q8d[3].text, 2, 'WHAT.')], figure=S + 'q8d')

# ── Q9 Water ─────────────────────────────────────────────────────────────────
# (a)(i): two points (2 x 3); the aside under them, "[Allow 19-21 °C.]", is the first point's.
_q9a1 = P.items(k('9', 'a', 'i'))
assert [it.cell for it in _q9a1] == ['[2 × 3]'] and _q9a1[0].points() == ['20 °C', 'in the dark'] and \
    _q9a1[0].asides == ['[Allow 19-21 °C.]'], _q9a1
C.add([k('9', 'a', 'i')], 'chem-4-3', 'storing-a-bod-sample', [
    lift('r-1', '20 °C', 3, 'The scheme prices these points (2 × 3), one each, and adds: ' + _q9a1[0].asides[0]),
    lift('r-2', 'in the dark', 3)])
# (a)(ii): the scheme prints "five (5) days" (3) on one line (page 20, y 113);
# the reader takes its "(5)" for a mark cell.
_q9a2 = P.items(k('9', 'a', 'ii'))
assert [(it.cell, it.text) for it in _q9a2] == [('[5]', 'five'), ('[3]', 'days')], _q9a2
assert raw(20, 112, 129, 160, 300) == 'five (5) days', raw(20, 112, 129, 160, 300)
C.add([k('9', 'a', 'ii')], 'chem-4-3', 'incubation-time-for-a-bod-test', [lift('r-1', 'five (5) days', 3)])
C.fixed([k('9', 'a', 'iii')], 'chem-4-3', 'eutrophication-and-its-effects', row_notes={0: 'DEFINE.', 1: 'STATE.'})
C.fixed([k('9', 'a', 'iv')], 'chem-4-3', 'a-cause-of-eutrophication')
C.fixed([k('9', 'b')], 'chem-4-3', 'lead-in-drinking-water', row_notes={0: 'WHY.', 1: 'NAME.', 2: 'HOW.'})
# (c): HOW, two points (2 x 3) or, after "or", the equation (6): two rows, each
# its point or the equation, which the student claims twice.
_q9c = P.items(k('9', 'c'))
assert [it.cell for it in _q9c] == ['[2 × 3]', '[6]'] and raw(20, 556, 572) == 'or', _q9c
_pt = _q9c[0].options()
assert len(_pt) == 2 and _pt[1].startswith('rain (water) reacts with limestone'), _pt
C.add([k('9', 'c')], 'chem-4-3', 'how-temporary-hardness-arises', [
    menu_row('r-1', [_pt[0], _q9c[1].text], 1, 'The first point, (3), or after "or" the equation, which the scheme '
             'prices (6) on its own: claim it here and again below.', per=3, total=3),
    menu_row('r-2', [_pt[1], _q9c[1].text], 1, 'The second point, (3), or the equation again.', per=3, total=3)],
    total=6)
C.fixed([k('9', 'c', 'i')], 'chem-4-3', 'limescale-from-boiling-hard-water')
C.ordered([k('9', 'c', 'ii')], 'chem-4-3', 'deionising-hard-water-with-ion-exchange-resins')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('10', 'a', 'i')], 'chem-3-4', 'strong-and-weak-acids-distinguished')
# (a)(ii): two asks, each its answer (6) and two steps (3) each. The weak acid's
# middle step is set in an equation font (doubled digits, "11.88 × 1111^−44"):
# its row is the expression in the forms the text layer carries, the scheme's
# print shown with the answer.
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [it.cell for it in _q10a2] == ['[6]', '[3]', '[3]', '[6]', '[3]', '[3]', None], _q10a2
assert display(_q10a2[0].text) == '0.005 M' and display(_q10a2[3].text) == '5/9 (0.556) M [0.55 – 0.56 M]', _q10a2
_ha = raw(21, 347, 364, 80, 470)
assert _ha == '[HA] = = 5/9 (0.55555) M [0.5556 – 0.56 M]', _ha
_ma = raw(21, 373, 389)
assert _ma == '[acid] = [HA] = [HX] = M = Ma', _ma
assert raw(21, 259, 275, 80, 320) == display(_q10a2[1].text), raw(21, 259, 275, 80, 320)
C.add([k('10', 'a', 'ii')], 'chem-3-4', 'molarity-of-sulfuric-acid-and-of-a-weak-acid-from-ph', [
    lift('r-1', _q10a2[1].text, 3, 'For the sulfuric acid: the scheme gives the answer, 0.005 M, priced (6), then '
         'these two steps.'),
    lift('r-2', _q10a2[2].text, 3),
    menu_row('r-3', ['[H⁺] = √Ka[HA]', '[H⁺]² = Ka[HA]'], 1, 'For the weak acid: the scheme gives the answer, '
             '5/9 (0.556) M [0.55 – 0.56 M], priced (6), then works it from [H⁺] = 0.01 as before to the expression '
             'with 1.8 × 10⁻⁴ and 0.01 put in it, (3), which it sets several ways, Ka = [H⁺][A⁻] over [HA] among '
             'them, in an equation font its text cannot carry; its own print is shown with the answer.',
             per=3, total=3),
    lift('r-4', _ha, 3, 'The scheme adds: "' + _ma + '"')], total=12, figure=S + 'q10a-ii')

# (a)(iii): DEFINE (3); WHAT (4), its working boxed, the answer its last line.
_q10a3 = P.items(k('10', 'a', 'iii'))
assert [it.cell for it in _q10a3] == ['[3]', '[4]', '[4]'] and display(_q10a3[1].text) == '3.0 × 10⁻⁷ M', _q10a3
_kw = display(_q10a3[0].text)
assert _kw.startswith('Kw = [H⁺][OH –] / Kw = [H₃O⁺][OH –] /'), _kw
C.add([k('10', 'a', 'iii')], 'chem-3-4', 'kw-and-the-hydrogen-ion-concentration-of-pure-water', [
    lift('r-1', _kw.replace('[OH –]', '[OH⁻]'), 3, 'DEFINE.'),
    lift('r-2', _q10a3[1].text, 4, 'WHAT. The scheme works it from Kw (9.0 × 10⁻¹⁴) = [H⁺]², or [H⁺] = √Kw, or '
         '[H⁺] = [OH⁻], to "⇒ [H⁺] = 3.0 × 10⁻⁷ M", priced (4).')])
# (b): the paper sets (i) and (ii) inside one sentence, priced (3) each; then two
# equations, and "Assign oxidation numbers in the first equation above to identify
# (iii) the reducing reagent, (iv) the oxidising reagent." (9): the scheme prices
# ASSIGN (3), set under its (ii) (page 22, y 108-135), and (iii) and (iv) (3)
# each; then "balance either equation", unnumbered after (iv) (10).
Q10B_EQ = FIG + 'paper-q10b-eq'
Q10B_DEF = P.ask(k('10', 'b'))
assert Q10B_DEF == 'Define reduction in terms of (i) electron transfer, (ii) change in oxidation number.', Q10B_DEF
_q10b = [P.items(k('10', 'b', r)) for r in ('i', 'ii')]
assert [[it.cell for it in its] for its in _q10b] == [['[3]'], ['[3]', '[3]']], _q10b
for r, it in (('i', _q10b[0][0]), ('ii', _q10b[1][0])):
    C.add([k('10', 'b', r)], 'chem-3-5', 'reduction-defined-by-' + ('electron-transfer' if r == 'i' else
                                                                  'oxidation-number'),
          [lift('r-1', it.text, 3, f'For ({r}).')], qtext=Q10B_DEF, stem='')
_assign = display(_q10b[1][1].text)
assert _assign == 'ClO – + S₂O₃ 2– + OH – → Cl – + SO₄ 2– + H⁺ +1 +2 –1 +6', _assign
Q10B_LEAD = P.lead(k('10', 'b'))
assert Q10B_LEAD == 'Assign oxidation numbers in the first equation above to identify', Q10B_LEAD
Q10B_ID = Q10B_LEAD + ' (iii) ' + P.ask(k('10', 'b', 'iii')) + ' (iv) ' + cut(P.ask(k('10', 'b', 'iv')), 'Using')[0]
Q10B_BAL = cut(P.ask(k('10', 'b', 'iv')), 'Using')[1]
assert Q10B_ID.endswith('(iv) the oxidising reagent.') and Q10B_BAL == ('Using oxidation numbers, or otherwise, '
                                                                          'balance either equation.'), (Q10B_ID, Q10B_BAL)
C.add([k('10', 'b')], 'chem-3-5', 'oxidation-numbers-in-the-hypochlorite-thiosulfate-equation', [C.mark_ask(point(
    'r-1', cut(Q10B_LEAD, ' to identify')[0], 3, 'ASSIGN: the scheme answers with the oxidation numbers written under the equation\'s '
    'species, which its text cannot set in place; its own print is shown with the answer.'))],
    qtext=Q10B_ID, stem='', figure=S + 'q10b-assign', cid='q10-b-oxidation-numbers',
    ref_suffix='after (ii), oxidation numbers')
print_question('paper-q10b-assign-print')
_q10b3 = P.items(k('10', 'b', 'iii'))
assert [it.cell for it in _q10b3] == ['[3]'], _q10b3
C.fixed([k('10', 'b', 'iii')], 'chem-3-5', 'the-reducing-reagent', figure=Q10B_EQ, qtext=Q10B_ID, stem='',
        fixes={display(_q10b3[0].text): display(_q10b3[0].text).replace('S₂O₃ 2–', 'S₂O₃²⁻')},
        row_notes={0: 'For (iii).'})
_q10b4 = P.items(k('10', 'b', 'iv'))
assert [it.cell for it in _q10b4] == ['[3]', '[10]', '[10]', None], _q10b4
C.add([k('10', 'b', 'iv')], 'chem-3-5', 'the-oxidising-reagent', [lift('r-1', _q10b4[0].text, 3, 'For (iv).')],
      figure=Q10B_EQ, qtext=Q10B_ID, stem='')
_eq1 = display(_q10b4[1].text)
assert _eq1 == '4ClO – + S₂O₃ 2– + OH – → 4Cl – + 2SO₄ 2– + H⁺', _eq1
_eq2 = raw(22, 389, 410, 130, 400)
assert _eq2 == 'ClO3 – + 6Br – + 6H⁺ → Cl – + 3Br2 + 3H2O', _eq2
_part = [raw(22, 304, 320), raw(22, 333, 349), raw(22, 431, 447), raw(22, 460, 477), raw(22, 498, 515)]
assert _part == ['Where 10 marks not awarded for the balanced equation',
                 'award 3 marks for sulfur balanced and 3 marks for chlorine balanced.',
                 'Where10 marks not awarded for the balanced equation',
                 'award 3 marks for bromine balanced and 3 marks chlorine balanced.',
                 'Award marks for one equation only.'], _part
C.add([k('10', 'b')], 'chem-3-5', 'balancing-a-redox-equation-by-oxidation-numbers', [menu_row(
    'r-1', ['4ClO⁻ + S₂O₃²⁻ + OH⁻ → 4Cl⁻ + 2SO₄²⁻ + H⁺', 'ClO₃⁻ + 6Br⁻ + 6H⁺ → Cl⁻ + 3Br₂ + 3H₂O'], 1,
    'Either equation, balanced, the second after "or", (10) each: "' + _part[4] + '" [Charges essential '
    'throughout.] For the first: "' + _part[0] + ' ... ' + _part[1] + '" For the second: "' + _part[2] + ' ... '
    + _part[3] + '"', per=10, total=10)],
    total=10, qtext=Q10B_BAL, stem='', figure=Q10B_EQ, cid='q10-b-balancing', ref_suffix='after (iv), balancing')
# (c)(i): WHAT (2 x 3), WHAT (3), DEFINE (2 x 2).
C.fixed([k('10', 'c', 'i')], 'chem-1-2', 'isotopes-radioisotopes-and-half-life')
# (c)(ii): COMPLETE (2 x 3); the nuclides are set with their mass and atomic
# numbers stacked before the symbol (page 23, y 217-240).
_q10c2 = P.items(k('10', 'c', 'ii'))
assert [(it.cell, display(it.text)) for it in _q10c2] == [('[2 × 3]', '222 Rn // 4 He'), (None, '86 2')], _q10c2
C.add([k('10', 'c', 'ii')], 'chem-1-2', 'alpha-decay-of-radium-226', [
    lift('r-1', '²²²₈₆Rn', 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'He', 3, 'The scheme writes the helium nucleus with its mass number, 4, and atomic number, 2, '
         'stacked before the symbol; its own print is shown with the answer.')], figure=S + 'q10c-ii')
print_question('paper-q10c-ii-print')
# (c)(iii): the answer (6); four boxed routes, each two steps (3), some set as fractions.
_q10c3 = P.items(k('10', 'c', 'iii'))
assert _q10c3[0].cell == '[6]' and display(_q10c3[0].text) == 'HOW 7.5 × 10¹⁸ atoms of radium–223', _q10c3
_f = [raw(23, 288, 299, 150, 215), raw(23, 291, 307, 210, 400), raw(23, 398, 409, 150, 215),
      raw(23, 401, 418, 205, 400)]
assert _f == ['1 ×10^−4 × 12.5', '= 1.25 × 10⁻⁵ moles radium–223 left', '6 ×10¹⁹ × 12.5',
              '= 7.5 × 10¹⁸ atoms radium–223 left'] and raw(23, 302, 311, 170, 200) == '100', _f
_s1 = [_f[0].replace('^−4', '⁻⁴') + ' ÷ 100 ' + _f[1], raw(23, 374, 390, 150, 470),
       raw(23, 492, 508, 150, 470)]
_s2 = [raw(23, 318, 334, 150, 430), _f[2] + ' ÷ 100 ' + _f[3], raw(23, 631, 646, 150, 470)]
assert _s1[1].endswith('atoms of radium–223 initially') and _s1[2].startswith('1.0 × 10⁻⁴ – 8.75') and \
    _s2[0].startswith('1.25 × 10⁻⁵ × 6.0') and _s2[2].startswith('6.0 × 10¹⁹ – 5.25'), (_s1, _s2)
C.add([k('10', 'c', 'iii')], 'chem-1-2', 'atoms-remaining-after-87-5-percent-decay', [
    menu_row('r-1', _s1, 1, 'The first step of the route used, (3). The scheme sets four routes, each after "or"; '
             'the third works the moles decayed first, 1 × 10⁻⁴ × 87.5 over 100 = 8.75 × 10⁻⁵, and the fourth the '
             'atoms decayed, 6 × 10¹⁹ × 87.5 over 100 = 5.25 × 10¹⁹, neither priced. '
             + FRACTION.format('1 × 10⁻⁴ × 12.5', '100'), per=3, total=3),
    menu_row('r-2', _s2, 1, 'And its second step, (3). ' + FRACTION.format('6 × 10¹⁹ × 12.5', '100'),
             per=3, total=3)],
    total=6, figure=S + 'q10c-iii',
    notes='The scheme gives the answer, 7.5 × 10¹⁸ atoms of radium–223, priced (6), then four boxed routes of two '
          'steps (3) each.')
shown('The scheme gives the answer as "7.5 × 10¹⁸ atoms of radium–223" (6); its own print of every route is '
      'shown with the answer.')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q11A = FIG + 'paper-q11a-eq'
# (a)(i): WHICH (1); WHAT (12), the moles of each (3 + 3) and then one of three
# boxes whose priced steps are the same (2 + 2 + 2). Six rows outrun a card: the
# two asks are a card each.
_q11a1 = P.items(k('11', 'a', 'i'))
assert [it.cell for it in _q11a1] == ['[1]', '[12]', '[3]', '[3]'] + ['[2]'] * 9, _q11a1
Q11A_WHICH, Q11A_MASS = cut(P.ask(k('11', 'a', 'i')), 'What mass')
C.add([k('11', 'a', 'i')], 'chem-1-4', 'reactant-in-excess', [lift('r-1', _q11a1[0].text, 1, 'WHICH.')],
      qtext=Q11A_WHICH, figure=Q11A, cid='q11-a-i-excess', ref_suffix='which reactant')
_m = [raw(24, 108, 129, 110, 250), raw(24, 137, 160, 110, 250)]
assert _m == ['101∗ = 0.2 moles KNO₃ (3) 20.2', '24.0 32 = 0.75 moles S (3)'], _m   # 20.2 over 101, 24.0 over 32
_b = [raw(24, 184, 206, 110, 420), raw(24, 212, 227, 110, 420), raw(24, 234, 250, 110, 420)]
assert _b == ['0.2 × 5 = 0.25 moles S required to react with 0.2 moles KNO₃ (2) 4',
              '0.75 – 0.25 = 0.5(0) moles S unused (in excess) (2)', '0.5 × 32 = 16 g S unused (2)'], _b
_and = raw(24, 161, 177, 100, 140)
assert _and == 'and', _and
C.add([k('11', 'a', 'i')], 'chem-1-4', 'mass-of-sulfur-unused', [
    lift('r-1', '20.2 ÷ 101∗ = 0.2 moles KNO₃', 3, FRACTION.format('20.2', '101∗') + ' The scheme gives the answer, '
         '16 g S, priced (12).'),
    lift('r-2', '24.0 ÷ 32 = 0.75 moles S', 3, FRACTION.format('24.0', '32')),
    lift('r-3', '0.2 × 5 ÷ 4 = 0.25 moles S required to react with 0.2 moles KNO₃', 2, 'Then, "and", one of three '
         'boxes, each after "or"; the other two open by showing the potassium nitrate is limiting, unpriced, and '
         'then price the same three steps. ' + FRACTION.format('0.2 × 5', '4')),
    lift('r-4', _b[1][:-len(' (2)')], 2),
    lift('r-5', _b[2][:-len(' (2)')], 2)],
    qtext=Q11A_MASS, figure=Q11A, cid='q11-a-i-mass-unused', ref_suffix='mass unused')
# (a)(ii) and (a)(iii): the scheme prints (iii)'s answer, "WHAT: 9.4 g K₂O (6)",
# with no "(iii)" (page 24, y 693): the reader files it under (ii), whose last
# three items are (iii)'s.
_q11a2 = P.items(k('11', 'a', 'ii'))
assert [it.cell for it in _q11a2] == ['[6]', '[3]', '[3]', '[6]', '[3]', '[3]'] and \
    [display(it.text) for it in _q11a2][::3] == ['7.84 litres', '9.4 g K₂O'], _q11a2
assert raw(24, 692, 708, 100) == 'WHAT: 9.4 g K₂O (6)', raw(24, 692, 708, 100)
# (An "or" in the text layer at x 411, y 598, is hidden under the box's fill: the page prints none.)
_gas = raw(24, 596, 619, 155, 405)
assert _gas == '0.2 × 7 / 0.2 × 2 + 0.2 × 5 = 0.35 moles gas (3) 4 4 4', _gas
_note = raw(24, 654, 683)
assert _note == '[Award final answer of 2.24 litres and 5.60 litres (5)] [Use of 24 L as molar volume not acceptable here.]', _note
C.add([k('11', 'a', 'ii')], 'chem-1-4', 'volume-of-gas-produced', [
    lift('r-1', '= 0.35 moles gas', 3, 'The scheme works the moles of gas as 0.2 × 7 over 4, or 0.2 × 2 over 4 + 0.2 '
         '× 5 over 4, set as fractions; its own print is shown with the answer. It gives the answer, 7.84 litres, '
         'priced (6).'),
    lift('r-2', '0.35 × 22.4 = 7.84 litres', 3, 'The scheme adds: ' + _note)],
    figure=S + 'q11a-ii')
_k2o = [raw(24, 722, 741, 165, 300), raw(24, 742, 757, 165, 300)]
assert _k2o == ['0.2 × 2 = 0.1 moles K₂O', '94* × 0.1 = 9.4 g K₂O'] and raw(24, 735, 745, 180, 190) == '4', _k2o
_slip = raw(24, 768, 784)
assert _slip == '[*Addition must be shown for error to be treated as slip.]', _slip
C.add([k('11', 'a', 'iii')], 'chem-1-4', 'mass-of-solid-produced', [
    lift('r-1', '0.2 × 2 ÷ 4 = 0.1 moles K₂O', 3, FRACTION.format('0.2 × 2', '4') + ' The scheme gives the answer, '
         '9.4 g K₂O, priced (6).'),
    lift('r-2', _k2o[1], 3, 'The scheme adds: ' + _slip)], figure=Q11A)
# (b): DETERMINE (4), DRAW (6), PREDICT (3), the letter's own asks before (i),
# under (13); WHICH (3) and JUSTIFY (3), also before (i), under (12) with (i) and (ii).
Q11B = FIG + 'paper-q11b-table'
_q11b = P.items(k('11', 'b'))
assert [it.cell for it in _q11b] == ['[4]', '[6]', '[3]', '[3]', '[3]'] and not _q11b[1].text, _q11b
assert _q11b[2].asides == ['[No marks for ‘trigonal’ on its own.]', raw(25, 404, 433)], _q11b[2].asides
_det = raw(25, 60, 76, 70, 400)
assert _det == 'DETERMINE: pure covalent / non-polar covalent', _det
Q11B_ASK = P.ask(k('11', 'b'))
Q11B_DATA, _r = cut(Q11B_ASK, 'Using data')
Q11B_DET, _r = cut(_r, 'Draw a dot')
Q11B_DRAW, Q11B_SHAPE = cut(_r, 'Predict the shape')
assert Q11B_DATA == 'Consider the three gaseous hydrides NH₃, PH₃ and AsH₃.' and \
    Q11B_SHAPE == 'Predict the shape of the arsine molecule.', (Q11B_DATA, Q11B_SHAPE)
_ins = raw(25, 404, 433)
assert _ins == '[Diagram insufficient unless a 3d representation using at least one wedge or dash, as shown.]', _ins
C.add([k('11', 'b')], 'chem-2-2', 'bonding-and-shape-of-arsine', [
    lift('r-1', _det[len('DETERMINE: '):], 4, 'DETERMINE. The scheme adds: ' + ' '.join(_q11b[0].asides)),
    C.mark_ask(point('r-2', Q11B_DRAW, 6, 'DRAW: the scheme answers with two dot and cross diagrams; its own print '
                     'is shown with the answer.')),
    lift('r-3', _q11b[2].text, 3, 'PREDICT. The scheme adds: ' + _q11b[2].asides[0] + ' It draws the shape five '
         'ways, each with a wedge or a dash, and adds: ' + _ins)],
    qtext=tidy(Q11B_DET + ' ' + Q11B_DRAW + ' ' + Q11B_SHAPE), stem=Q11B_DATA, figure=S + 'q11b',
    cid='q11-b-arsine', ref_suffix='bonding, dot and cross diagram, shape')
_wj = [raw(25, 455, 471, 130, 400), raw(25, 468, 496, 130, 500)]
assert _wj == ['azane / ammonia / NH₃', 'nitrogen (N) small and strongly electronegative / hydrogen bonds occur when '
               'hydrogen is bonded to nitrogen, oxygen, fluorine (N, O, F)'], _wj
Q11B_LEAD = P.lead(k('11', 'b'))
Q11B_HB, Q11B_SUGGEST = cut(Q11B_LEAD, 'Suggest a reason why')
assert Q11B_HB == ('Which, if any, of the three hydrides would you expect to have intermolecular hydrogen bonding? '
                   'Justify your answer.') and Q11B_SUGGEST == 'Suggest a reason why', Q11B_LEAD
C.add([k('11', 'b')], 'chem-2-2', 'which-hydride-has-hydrogen-bonding', [
    lift('r-1', _wj[0], 3, 'WHICH.'),
    lift('r-2', _wj[1], 3, 'JUSTIFY. The scheme adds: ' + _q11b[4].asides[0])],
    qtext=Q11B_HB, stem=Q11B_DATA, figure=Q11B, cid='q11-b-hydrogen-bonding', ref_suffix='hydrogen bonding')
_q11b1 = P.items(k('11', 'b', 'i'))
assert [it.cell for it in _q11b1] == ['[3]'] and display(_q11b1[0].text).endswith('intermolecular force //'), _q11b1
C.add([k('11', 'b', 'i')], 'chem-2-2', 'why-ammonia-boils-highest',
      [lift('r-1', display(_q11b1[0].text)[:-len(' //')], 3)],
      stem=Q11B_DATA + ' ' + Q11B_SUGGEST, figure=Q11B)
C.fixed([k('11', 'b', 'ii')], 'chem-2-2', 'why-phosphine-boils-below-arsine', stem=Q11B_DATA + ' ' + Q11B_SUGGEST,
        figure=Q11B)
# (c)A: the ozone layer.
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'the-ozone-layer-and-ultraviolet-radiation')
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'how-ozone-forms-in-the-stratosphere')
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-4-3', 'chlorine-radicals-destroying-ozone')
C.fixed([ka('11', 'c', 'iv', 'A')], 'chem-4-3', 'why-hcfcs-are-less-damaging')
# (c)B: the Downs cell.
Q11CB = FIG + 'paper-q11c-b'
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-u3', 'uses-of-sodium-and-chlorine', figure=Q11CB)
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-u3', 'molten-electrolyte-and-calcium-chloride', figure=Q11CB,
        row_notes={0: 'WHY.', 1: 'HOW.'})
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-u3', 'the-steel-mesh-in-the-downs-cell', figure=Q11CB)
_q11cb4 = P.items(ka('11', 'c', 'iv', 'B'))
_w = display(_q11cb4[0].text)
assert [it.cell for it in _q11cb4] == ['[3 + 3]'] and _w.count('Cl –') == 2, _q11cb4
C.fixed([ka('11', 'c', 'iv', 'B')], 'chem-u3', 'the-downs-cell-reaction', figure=Q11CB,
        fixes={_w: _w.replace('Cl –', 'Cl⁻')})
# (v): the reader takes the "Blank Page" of the scheme's next page (page 27) as
# a line under (v)'s answer.
_q11cb5 = P.items(ka('11', 'c', 'v', 'B'))
assert [(it.cell, it.text) for it in _q11cb5][1:] == [(None, 'Blank Page')] and _q11cb5[0].cell == '[4]', _q11cb5
C.add([ka('11', 'c', 'v', 'B')], 'chem-u3', 'why-aluminium-is-extracted-by-electrolysis',
      [lift('r-1', _q11cb5[0].text, 4)], figure=Q11CB)

# @@QUESTIONS@@


# A note quoted from the scheme in the reader's script notation ("E_(n>2)",
# "K_(c)") is shown as the page sets it.
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'], _r


# ── review ───────────────────────────────────────────────────────────────────
INLINE = {}


def printed():
    """Every letter's printed marks: the paper sets one mark after a letter's
    last part, or several, one after each run of asks."""
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
