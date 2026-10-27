#!/usr/bin/env python3
"""2018 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2018_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2018_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2018_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2018 hl

No 2018 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

The 2018 scheme is the labelled ("cue") layout. Where it prices whole
alternatives -- Q1(b)'s pipette or burette, Q2(c)(iii)'s melting point or
analysis, Q4(g)'s equation or half equations -- the student claims the one they
gave, from a menu row. Q4(k) and Q11(c) offer whole alternative parts A and B,
and Q11(c)A three alternative case studies, (i), (ii) and (iii).

The paper sets several asks unnumbered under a letter: Q10(a) before its (i),
and after the last roman of Q10(a), Q10(b) and Q11(b). Those after a roman are
one card each, cited "Qn(x) — after (r)"; those before (i) are the letter's own
card. It sets two pairs of romans inside one sentence, Q4(k)B ("(i) a molecular
crystal, (ii) a covalent ...", one cell) and Q5(a) ("Define (i) ..., (ii) ...",
a cell each). The paper underlines the terms Q6(a), Q8(b)(i) and Q10(a) ask
about, which no text layer carries: those take the paper's own print as their
question.
"""
import json
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, read_lines, tidy  # noqa: E402

P = Printed(2018, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2018-HL-'
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


def table_lines(page, rect, split_x):
    """The lines of a two-column table the scheme prints as its answer, read
    row by row between the table's own rules: each line is its left cell, then
    its right cell. Empty rows are not lines."""
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


def cut(text, at, keep=False):
    """`text` split where `at` begins (the paper's print, cut between two asks
    it sets in one run)."""
    i = text.index(at)
    return text[:i].strip(), text[i:].strip()


def eq_note(page, y):
    """The scheme's price for an equation, quoted from its own label line."""
    t = raw(page, y - 1, y + 13, 400)
    assert re.fullmatch(r'FORMULAE: \(\d\) BALANCING: \(\d\)', t), (page, y, t)
    return 'The scheme prices this equation "' + t + '".'


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 Total hardness by edta titration ──────────────────────────────────────
C.fixed([k('1', 'a')], 'chem-4-3', 'calcium-compounds-causing-permanent-hardness')
# (b): two whole methods, a pipette or a burette, each "ANY THREE: (6 + 3 + 3)".
_q1b = P.items(k('1', 'b'))
assert [it.cell for it in _q1b] == ['[6 + 3 + 3]', '[6 + 3 + 3]'], _q1b
_pip, _bur = _q1b[0].options(), _q1b[1].options()
assert len(_pip) == 6 and len(_bur) == 6 and _pip[0].startswith('use 25') and _bur[0].startswith('use burette'), \
    (_pip, _bur)
_three = raw(5, 238, 251)
assert _three == raw(5, 412, 425) == 'ANY THREE: (6 + 3 + 3)', _three
C.add([k('1', 'b')], 'chem-4-1', 'measuring-out-water-with-a-pipette-or-a-burette', [menu_row(
    'r-1', _pip + _bur, 3,
    'Any three points of the one method used, the first (6) and the others (3) each: "' + _three + '". '
    'The first six are for a pipette; the scheme sets the last six, for a burette, after "or".',
    per=6, steps=[6, 3, 3], total=12)], total=12)
C.fixed([k('1', 'c', 'i')], 'chem-4-1', 'indicator-for-an-edta-titration')
C.fixed([k('1', 'c', 'ii')], 'chem-4-1', 'indicator-colour-with-metal-ions')
C.fixed([k('1', 'c', 'iii')], 'chem-4-1', 'indicator-colour-at-the-end-point')
_q1d2 = P.items(k('1', 'd', 'ii'))
assert [it.cell for it in _q1d2] == ['[3]'] and len(_q1d2[0].asides) == 1, _q1d2
C.fixed([k('1', 'd', 'i')], 'chem-4-1', 'buffer-added-before-an-edta-titration')
shown('The scheme adds, under (ii): ' + _q1d2[0].asides[0])
C.fixed([k('1', 'd', 'ii')], 'chem-4-1', 'why-a-buffer-is-added')
C.route([k('1', 'e', 'i')], 'chem-4-1', 'moles-of-edta-in-a-titre',
        fixes={'ܯ= 9.3 × 0.010 = 0.000093 (9.3 × 10⁻⁵) moles':
               '9.3 × 0.010 ÷ 1000 = 0.000093 (9.3 × 10⁻⁵) moles'},
        row_notes={0: FRACTION.format('9.3 × 0.010', '1000')})
C.route([k('1', 'e', 'ii')], 'chem-4-1', 'moles-of-metal-ion-from-moles-of-edta')
C.route([k('1', 'e', 'iii')], 'chem-4-1', 'total-hardness-in-grams-per-litre', figure=S + 'q1e-iii')
shown('The scheme adds: ' + display(P.items(k('1', 'e', 'iii'))[-1].asides[0]), -1)
C.route([k('1', 'e', 'iv')], 'chem-4-1', 'total-hardness-in-parts-per-million')
C.fixed([k('1', 'f')], 'chem-4-3', 'testing-for-temporary-hardness')

# ── Q2 Reflux, liquid-liquid extraction and recrystallisation ────────────────
Q2A, Q2B, Q2C = FIG + 'paper-q2a', FIG + 'paper-q2b', FIG + 'paper-q2c'
_x = P.items(k('2', 'a', 'i'))
assert [it.cell for it in _x] == ['[6]'] and _x[0].text == 'condenser', _x
C.fixed([k('2', 'a', 'i')], 'chem-u2', 'reflux-condenser', figure=Q2A,
        label_key=[{'letter': 'X', 'meaning': _x[0].text, 'askedInThisQuestion': True}])
C.fixed([k('2', 'a', 'ii')], 'chem-u2', 'purpose-of-refluxing', figure=Q2A)
C.fixed([k('2', 'a', 'iii')], 'chem-4-2', 'reactants-and-solvent-for-making-soap', figure=Q2A)
C.fixed([k('2', 'b', 'i')], 'chem-u2', 'what-an-emulsion-is', figure=Q2B)
C.fixed([k('2', 'b', 'ii')], 'chem-u2', 'solvent-for-extracting-clove-oil', figure=Q2B)
C.fixed([k('2', 'b', 'iii')], 'chem-u2', 'safety-when-using-a-separating-funnel', figure=Q2B)
C.fixed([k('2', 'b', 'iv')], 'chem-u2', 'isolating-clove-oil-after-extraction', figure=Q2B)
# (v): the answer (6), then two steps (3) each; the second sets 0.1575 over 5.0
# as a fraction in a font the gate cannot read, so its row is the answer it reaches.
_q2b5 = P.items(k('2', 'b', 'v'))
assert [it.cell for it in _q2b5] == ['[6]', '[3]', '[3]'], _q2b5
_m = '0.1575 g [0.1575 – 0.16 g]'
assert display(_q2b5[1].text).endswith('m = 1.05 × 0.15 = ' + _m), _q2b5[1].text
assert display(_q2b5[2].text).endswith('× 100 ⇒ 3.15% [3.15 – 3.2%]'), _q2b5[2].text
C.add([k('2', 'b', 'v')], 'chem-1-4', 'percentage-yield-of-clove-oil-by-mass', [
    lift('r-1', 'm = 1.05 × 0.15 = ' + _m, 3, 'The scheme opens with density = mass over volume = 1.05 = '
         'mass over 0.15; its own print is shown with the answer.'),
    lift('r-2', _q2b5[0].text, 3, 'The scheme reaches this as 0.1575 over 5.0, × 100 ⇒ 3.15% [3.15 – 3.2%] '
         '(3). It adds: ' + ' '.join(_q2b5[2].asides))],
    figure=S + 'q2b-v',
    notes='The scheme gives the answer, ' + display(_q2b5[0].text) + ', priced (6), then the two steps that '
          'earn it, (3) each.')
# (c)(i) and (ii): one label prices them, "ANY CORRECT RESPONSE FOR (i) and ANY
# CORRECT RESPONSE FOR (ii): (6 + 3)", (i) six and (ii) three.
_q2c1, _q2c2 = P.items(k('2', 'c', 'i')), P.items(k('2', 'c', 'ii'))
assert [it.cell for it in _q2c1] == [None] and [it.cell for it in _q2c2] == ['[6 + 3]'], (_q2c1, _q2c2)
_lab = raw(8, 131, 144)
assert _lab == 'ANY CORRECT RESPONSE FOR (i) and ANY CORRECT RESPONSE FOR (ii): (6 + 3)', _lab
_t2 = display(_q2c2[0].text)
assert _t2.endswith(' ' + _lab[:-len(' (6 + 3)')]), _t2
C.add([k('2', 'c', 'i'), k('2', 'c', 'ii')], 'chem-u2', 'recrystallisation-and-suction-filtration', [
    lift('r-1', display(_q2c1[0].text).rstrip('/ '), 6, 'For (i). The scheme prices (i) and (ii) "' + _lab + '".'),
    lift('r-2', _t2[:-len(_lab) + len(' (6 + 3)')].strip(), 3, 'For (ii).')], figure=Q2C)
# (iii): two methods, each a test (3) and its result (2), linked.
_q2c3 = P.items(k('2', 'c', 'iii'))
assert [it.cell for it in _q2c3] == ['[3]', '[2]', '[3]', '[2]'], _q2c3
C.add([k('2', 'c', 'iii')], 'chem-u2', 'showing-the-recrystallised-acid-is-purer', [
    menu_row('r-1', [_q2c3[0].text, _q2c3[2].text], 1,
             'One of these, as the method used; the scheme sets the second after "or" and prices either (3).',
             per=3, total=3),
    menu_row('r-2', [_q2c3[1].text, _q2c3[3].text], 1,
             'And the result for that same method, in the same order, (2). The scheme adds: '
             + ' '.join(_q2c3[1].asides), per=2, total=2)], total=5, figure=Q2C)

# ── Q3 Heat of neutralisation in a cardboard cup ─────────────────────────────
Q3 = FIG + 'paper-q3'
C.fixed([k('3', 'a')], 'chem-3-1', 'neutralisation-is-exothermic', figure=Q3)
C.fixed([k('3', 'b', 'i')], 'chem-u2', 'why-stir-before-reading-the-temperature', figure=Q3)
C.fixed([k('3', 'b', 'ii')], 'chem-u2', 'why-the-temperature-falls-after-the-rise', figure=Q3)
C.fixed([k('3', 'b', 'iii')], 'chem-u2', 'temperature-rise-read-to-the-nearest-kelvin', figure=Q3)
C.fixed([k('3', 'c', 'i')], 'chem-u2', 'why-use-moderately-concentrated-solutions', figure=Q3)
# (c)(ii): the scheme prints the corrosive pictogram itself, then "/", then the
# description, (2 x 3).
_q3c2 = P.items(k('3', 'c', 'ii'))
assert [it.cell for it in _q3c2] == ['[2 × 3]'], _q3c2
_p = _q3c2[0].points()
assert _p == ['/ liquid pouring from test-tube(s)', 'onto hand (object, metal)'], _p
# Its only figure is the scheme's pictogram, held back until the reveal, so the lead-in's "the
# cardboard cup ... in the diagram" would point at nothing. Nothing in (c)(ii) depends on the
# lead-in: the ask names the solution it is about (1.0 M NaOH). The lead-in is left out of this
# card's stem (left out whole: without its first sentence the next reads "also at room
# temperature" of an acid it no longer names).
assert C.context(k('3', 'c', 'ii')).startswith('The cardboard cup with plastic lid in the diagram contained'), \
    C.context(k('3', 'c', 'ii'))
C.add([k('3', 'c', 'ii')], 'chem-u2', 'hazard-pictogram-for-sodium-hydroxide', [
    lift('r-1', _p[0][2:], 3, 'The scheme prices this point and the next (2 × 3), one each. It accepts '
         'instead the pictogram itself, drawn, which it prints before "/"; its own print is shown with the '
         'answer.'),
    lift('r-2', _p[1], 3, 'The scheme adds: ' + ' '.join(_q3c2[0].asides))], figure=S + 'q3c-ii', stem='')
C.route([k('3', 'd', 'i')], 'chem-1-4', 'moles-of-acid-neutralised',
        fixes={'ܯ= 150 × 1.0 1000 = 0.15 moles': '150 × 1.0 ÷ 1000 = 0.15 moles'},
        row_notes={0: FRACTION.format('150 × 1.0', '1000')})
C.cards[-1]['figureKey'] = Q3       # the cup the lead-in names, not the scheme's working
# (d)(ii), (iii): the scheme sets its routes side by side in boxes, which the
# text layer reads across; the rows are the first box's steps, read from the page.
_q3d2 = P.items(k('3', 'd', 'ii'))
assert _q3d2[0].cell == '[9]', _q3d2
_st = [raw(9, 539, 552, 55, 275), raw(9, 553, 567, 55, 275), raw(9, 568, 581, 55, 275)]
assert _st == ['m = 0.31 kg', 'H = mcΔT (mcΔθ ) / H = 0.31 × 4.2 × 6.4', '= 8.3328 kJ [8.3 to 8.333 kJ]'], _st
# The italic theta leaves a gap before its bracket in the text layer; the page prints "(mcΔθ)".
C.add([k('3', 'd', 'ii')], 'chem-3-1', 'heat-produced-from-mass-heat-capacity-and-rise', [
    lift('r-1', _st[0], 3), lift('r-2', _st[1].replace('Δθ )', 'Δθ)'), 3), lift('r-3', _st[2], 3)],
    figure=S + 'q3d-ii',
    notes='The scheme gives the answer, ' + display(_q3d2[0].text) + ', priced (9), then three boxed routes '
          '(in kJ with the mass in kg, in kJ with the heat capacity per gram, or in joules); the steps here '
          'are its first route, and its own print of every route is shown with the answer.')
shown('The scheme gives the answer as "' + display(_q3d2[0].text) + '" (9), and accepts two other routes; '
      'its own print of every route is shown with the answer.')
# (d)(ii), (d)(iii) and (e): the only figure is the scheme's working or table, held back until the
# reveal, while the stem points at the cup "in the diagram" and gives the volumes, the
# concentrations and the temperature rise the answers use. The paper's own print is the question:
# the lead-in and equation with the photograph of the cup beside them ((a)-(c)(i), printed beside
# the photograph's lower half, whited out), then "(d) Calculate" and the part's own ask.
print_question('paper-q3d-ii-print')
_q3d3 = P.items(k('3', 'd', 'iii'))
assert _q3d3[0].cell == '[6]', _q3d3
_st = [raw(9, 703, 718, 55, 270), raw(9, 717, 732, 55, 270)]
assert _st == ['8.3328 ÷ 0.15 = 55.55 to 55.6 kJ mol⁻¹', 'ΔH = –55.6 kJ mol⁻¹ [–55.6 to –55.55 kJ mol⁻¹]'], _st
C.add([k('3', 'd', 'iii')], 'chem-3-1', 'heat-of-neutralisation-per-mole', [
    lift('r-1', _st[0], 3), lift('r-2', _st[1], 3, 'The scheme adds: ' + ' '.join(_q3d3[-1].asides))],
    figure=S + 'q3d-iii',
    notes='The scheme gives the answer, ' + display(_q3d3[0].text) + ', priced (6), then two boxed routes, '
          'in kJ or in joules; the steps here are its first route, and its own print of both is shown with '
          'the answer.')
shown('The scheme gives the answer as "' + display(_q3d3[0].text) + '" (6), and accepts the same in '
      'joules; its own print of both routes is shown with the answer.')
print_question('paper-q3d-iii-print')
# (e): one line of the scheme's table, STATE (3) and EXPLAIN (3), linked.
_q3e = table_lines(10, (100, 95, 520, 660), 250)
assert _q3e[0] == ('STATE (3)', 'EXPLAIN (3)') and len(_q3e) == 13, _q3e
assert cells(k('3', 'e'))[:2] == ['[3]', '[3]'], cells(k('3', 'e'))
_lnk = raw(10, 655, 708)
assert _lnk.startswith('[SUGGEST and EXPLAIN are linked.]'), _lnk
C.add([k('3', 'e')], 'chem-u2', 'improving-the-accuracy-of-the-heat-of-neutralisation', [
    menu_row('r-1', [a for a, _b in _q3e[1:]], 1,
             'One modification, a line of the scheme\'s table (STATE), (3).', per=3, total=3),
    menu_row('r-2', [a + ' — ' + b for a, b in _q3e[1:]], 1,
             'And the explanation the table gives on that same line (EXPLAIN), (3). The scheme adds: ' + _lnk
             + ' Its own print of the table is shown with the answer.', per=3, total=3)],
    total=6, figure=S + 'q3e')
print_question('paper-q3e-print')

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-2', 'purpose-of-millikans-oil-drop-experiment', notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-3', 'atomic-radius-across-a-period', notes=Q4_NOTE)
_q4c = P.items(k('4', 'c'))
assert [it.cell for it in _q4c] == ['[2 × 3]', None], _q4c
C.fixed([k('4', 'c')], 'chem-1-2', 'electron-configuration-of-iron', notes=Q4_NOTE)
shown(' '.join(_q4c[1].asides), -1)
C.fixed([k('4', 'd')], 'chem-2-3', 'why-real-gases-deviate-from-ideal-behaviour', notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-3-4', 'bronsted-lowry-acid-and-conjugate-base', notes=Q4_NOTE)
# (f): the change of oxidation number (3), then "reduced" (3); or the same two
# marks read off the equation the scheme annotates, shown with the answer.
_q4f = P.items(k('4', 'f'))
assert [it.cell for it in _q4f][:2] == ['[3]', '[3]'], _q4f
_or = raw(11, 609, 623)
assert _or == '(3) marks for oxidation numbers of chlorine and (3) for species reduced available from:', _or
C.add([k('4', 'f')], 'chem-3-5', 'chlorine-reduced-in-sodium-hypochlorite', [
    lift('r-1', _q4f[0].text, 3),
    lift('r-2', _q4f[1].text, 3, 'The scheme adds: ' + ' '.join(_q4f[1].asides) + ' Or, after "or": "' + _or
         + '" the equation with chlorine\'s oxidation numbers marked; its own print is shown with the answer.')],
    figure=S + 'q4f', notes=Q4_NOTE)
# (g): the balanced equation, FORMULAE (3) BALANCING (3), or after "or" the two
# half equations, (2 x 3): either route, as the student gave it.
_q4g = P.items(k('4', 'g'))
assert [it.cell for it in _q4g] == ['[3 + 3]', '[2 × 3]'], _q4g
C.add([k('4', 'g')], 'chem-3-5', 'chlorine-displacing-bromide', [menu_row(
    'r-1', [_q4g[0].text, _q4g[1].text], 1,
    'Either the equation, priced "' + raw(12, 79, 92) + '", or, after "or", the two half equations, priced '
    '(2 × 3), one each. The scheme adds: ' + ' '.join(_q4g[1].asides), per=6, total=6)],
    total=6, notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-4-2', 'tetraethyllead-and-the-chlorination-of-methane', notes=Q4_NOTE)
C.answer_only([k('4', 'i')], 'chem-1-4', 'empirical-formula-of-epoxyethane', S + 'q4i',
              fixes={'C2H4O': 'C₂H₄O'}, notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-4-3', 'biochemical-oxygen-demand', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'greatest-contributor-to-the-greenhouse-effect', notes=Q4_NOTE)
print_question('paper-q4k-a-print')      # the three gases it names are set out as a row
# (k)B: "(i) a molecular crystal, (ii) a covalent macromolecular crystal" set in
# one sentence, one cell (2 x 3) under the scheme's own (i) and (ii).
assert cells(ka('4', 'k', 'i', 'B')) == [None] and cells(ka('4', 'k', 'ii', 'B')) == ['[2 × 3]']
C.fixed([ka('4', 'k', None, 'B')], 'chem-2-1', 'molecular-and-macromolecular-crystals', deep=True,
        notes=Q4_NOTE, row_notes={0: 'For (i).', 1: 'For (ii).'})

# ── Q5 Mass spectrometry and radioactivity ───────────────────────────────────
# (a): "Define (i) mass number of an atom, (ii) relative atomic mass of an
# element." is one sentence; the scheme prices (i) (3) and (ii) (3 + 2).
_q5a = P.ask(k('5', 'a'))
assert cells(k('5', 'a', 'i')) == ['[3]'] and cells(k('5', 'a', 'ii')) == ['[3 + 2]']
C.fixed([k('5', 'a', 'i')], 'chem-1-2', 'definition-of-mass-number', qtext=_q5a, stem='', cid='q5-a-i',
        row_notes={0: 'For (i).'})
_p = P.items(k('5', 'a', 'ii'))[0].points()
assert len(_p) == 2, _p
C.add([k('5', 'a', 'ii')], 'chem-1-2', 'definition-of-relative-atomic-mass', [
    lift('r-1', _p[0], None, 'For (ii).'), lift('r-2', _p[1], None)],
    kind='orderedSplit', notation='[3 + 2]', total=5, qtext=_q5a, stem='', cid='q5-a-ii',
    notes=SPLIT.format('[3 + 2]'))
C.fixed([k('5', 'b')], 'chem-1-2', 'processes-in-a-mass-spectrometer')
C.route([k('5', 'c')], 'chem-1-2', 'relative-atomic-mass-from-a-mass-spectrum')
C.cards[-1]['figureKey'] = FIG + 'paper-q5c'      # the spectrum, not the scheme's working
C.fixed([k('5', 'd', 'i')], 'chem-1-2', 'definition-of-radioactivity')
# (d)(ii): in words (6), or after "or" the same in nuclide symbols (6), which
# the text layer cannot carry: shown with the answer.
_q5d2 = P.items(k('5', 'd', 'ii'))
assert [it.cell for it in _q5d2] == ['[6]', '[6]'], _q5d2
C.add([k('5', 'd', 'ii')], 'chem-1-2', 'beta-decay-in-the-nucleus', [
    lift('r-1', _q5d2[0].text, 6, 'The scheme accepts instead, after "or", the same change written in '
         'nuclide symbols, (6); its own print is shown with the answer. It adds: '
         + ' '.join(_q5d2[1].asides))], figure=S + 'q5d-ii')
C.drawn([k('5', 'd', 'iii')], 'chem-1-2', 'equation-for-the-beta-decay-of-carbon-14', S + 'q5d-iii')
# (iv): EXPLAIN (3); then WHAT MASS, the answer (6) and three boxed routes of
# two steps (3) each.
_q5d4 = P.items(k('5', 'd', 'iv'))
assert [it.cell for it in _q5d4] == ['[3]', '[6]'] + ['[3]'] * 6, _q5d4
_why, _mass = cut(P.ask(k('5', 'd', 'iv')), 'What mass')
_ctx, _why = cut(_why, 'Explain why')
C.add([k('5', 'd', 'iv')], 'chem-1-4', 'mass-of-carbon-14-one-half-life-ago', [
    lift('r-1', _q5d4[0].text, 3, 'EXPLAIN.'),
    lift('r-2', _q5d4[2].text, 3, 'WHAT MASS: the first of three routes the scheme accepts; its own print of '
         'all three is shown with the answer.'),
    lift('r-3', _q5d4[3].text, 3, 'The scheme adds: ' + ' '.join(_q5d4[-1].asides))],
    figure=S + 'q5d-iv', qtext=_why + ' ' + _mass,
    stem=C.context(k('5', 'd', 'iv')) + ' ' + _ctx,
    notes='The scheme prices the explanation (3), then gives the mass, ' + display(_q5d4[1].text)
          + ', priced (6), and three boxed routes to it, two steps (3) each.')
shown('The scheme gives the mass as "' + display(_q5d4[1].text) + '" (6).', 1)

# ── Q6 Fuels ─────────────────────────────────────────────────────────────────
C.ordered([k('6', 'a')], 'chem-2-4', 'fractional-distillation-of-crude-oil')
print_question('paper-q6a-print')
C.fixed([k('6', 'b', 'i')], 'chem-2-4', 'components-of-lpg')
C.fixed([k('6', 'b', 'ii')], 'chem-2-4', 'why-a-mercaptan-is-added-to-gas')
_q6b3 = P.items(k('6', 'b', 'iii'))
assert _q6b3[0].cell == '[12]', _q6b3
C.answer_only([k('6', 'b', 'iii')], 'chem-3-1', 'heat-of-combustion-of-methanethiol', S + 'q6b-iii',
              notes='The scheme sets out two routes, from heats of formation or by adding equations, each '
                    'priced (3) a step, and says how a reversed sign is marked.')
shown('The scheme prices each step of either route (3), and says how an answer of +1239.1 kJ is marked.')
Q6C = FIG + 'paper-q6c'
_q6c1 = P.items(k('6', 'c', 'i'))
assert [it.cell for it in _q6c1] == ['[4 × 3]', None], _q6c1
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'naming-the-products-made-from-octane', figure=Q6C)
shown(' '.join(_q6c1[1].asides), -1)
C.fixed([k('6', 'c', 'ii')], 'chem-2-4', 'cracking-and-dehydrocyclisation', figure=Q6C)
C.fixed([k('6', 'c', 'iii')], 'chem-2-4', 'why-octane-is-converted-in-a-refinery', figure=Q6C)
C.fixed([k('6', 'd')], 'chem-2-4', 'boiling-points-of-petrol-and-diesel')

# ── Q7 The decomposition of nitrogen dioxide ─────────────────────────────────
# The paper prints the reaction and its table after (a)(ii); (b), (c) and (d)
# are led by it.
Q7_LEAD = P.lead(k('7', 'a', 'ii'))
assert Q7_LEAD.startswith('The decomposition of nitrogen dioxide') and Q7_LEAD.endswith('∆H = 114.4 kJ'), Q7_LEAD
Q7T = FIG + 'paper-q7-table'
# (a)(i): two wordings (5), or after "or" the same as a fraction or a
# derivative (5), which the text layer cannot carry: shown with the answer.
_q7a1 = P.items(k('7', 'a', 'i'))
assert [it.cell for it in _q7a1] == ['[5]', '[5]', None], _q7a1
_def = raw(17, 63, 90, 130)
assert _def == ('change in concentration per unit (over, with) time of one reactant (product) / rate of change '
                'of concentration of one reactant (product) /'), _def
C.add([k('7', 'a', 'i')], 'chem-3-2', 'definition-of-rate-of-reaction', [
    lift('r-1', _def.rstrip('/ '), 5, 'The scheme also accepts it written as change in concentration over '
         'time, as a fraction, and, after "or", as the derivative of a reactant\'s or product\'s concentration '
         'with time, each (5); its own print is shown with the answer.')], figure=S + 'q7a-i')
# (a)(ii): two wordings, each two points (2 x 3); the scheme sets the second after "or".
_q7a2 = P.items(k('7', 'a', 'ii'))
assert [it.cell for it in _q7a2] == ['[2 × 3]'], _q7a2
_w = _q7a2[0].points()
assert len(_w) == 4, _w
C.add([k('7', 'a', 'ii')], 'chem-3-2', 'definition-of-activation-energy', [
    menu_row('r-1', [_w[0], _w[2]], 1, 'One of these wordings, the scheme setting the second after "or", '
             '(3). It adds: ' + ' '.join(_q7a2[0].asides), per=3, total=3),
    menu_row('r-2', [_w[1], _w[3]], 1, 'And the second point of that same wording, (3).', per=3, total=3)],
    total=6)
C.fixed([k('7', 'b')], 'chem-3-2', 'graphs-of-concentration-against-time', stem=Q7_LEAD, figure=S + 'q7b')
shown('The scheme\'s own graphs are shown with the answer.', -1)
print_question('paper-q7b-print')
# (c): the tangent (6), then the rate it gives (3), with the scheme's working.
_q7c = P.items(k('7', 'c'))
assert [it.cell for it in _q7c] == ['[6]', '[3]', '[3]', None], _q7c
_p = _q7c[1].points()
assert len(_p) == 2 and _p[1] == '1.8 × 10⁻⁵ to 2.5 × 10⁻⁵ M s⁻¹ NO₂', _p
C.add([k('7', 'c')], 'chem-3-2', 'instantaneous-rate-from-a-tangent', [
    lift('r-1', _q7c[0].text, 6, 'The scheme adds: "' + display(_p[0]) + '"'),
    lift('r-2', _p[1], 3, 'The scheme works it as 0.0040−0.0087 over 205−0 = −0.0047 over 205 = –2.3 × 10⁻⁵ '
         '[–2.5 × 10⁻⁵ to –1.8 × 10⁻⁵] M s⁻¹ NO₂ (3), and draws the tangent on its graph; its own print is '
         'shown with the answer. It adds: ' + ' '.join(_q7c[3].asides))],
    stem=Q7_LEAD, figure=S + 'q7c')
print_question('paper-q7c-print')
C.fixed([k('7', 'd', 'i')], 'chem-3-2', 'why-not-every-collision-reacts', stem=Q7_LEAD)
C.fixed([k('7', 'd', 'ii')], 'chem-3-2', 'raising-the-frequency-of-collisions', stem=Q7_LEAD)
# (iii): the axes (3), each axis printed with its own aside, then the curve (3).
_q7d3 = P.items(k('7', 'd', 'iii'))
assert [it.cell for it in _q7d3] == ['[3]', '[3]'], _q7d3
_ax = [raw(19, 137, 150)[len('(iii) SKETCH: '):], raw(19, 150, 164, 130, 500)]
assert _ax == ['y-axis: energy [Must be shown and labelled.]', 'x-axis [Must be shown but need not be labelled.]'], _ax
C.add([k('7', 'd', 'iii')], 'chem-3-2', 'reaction-profile-of-an-endothermic-reaction', [
    # The row is the two axes without the asides set after each, which its note quotes.
    lift('r-1', re.sub(r'\s*\[[^\]]*\]', '', display(_q7d3[0].text)), 3,
         'The scheme sets each axis on a line of its own: "' + _ax[0] + '" and "' + _ax[1] + '".'),
    lift('r-2', _q7d3[1].text, 3, 'The scheme adds: ' + ' '.join(_q7d3[1].asides) + ' It draws the profile; its '
         'own print is shown with the answer.')], stem=Q7_LEAD, figure=S + 'q7d-iii')

# ── Q8 Four compounds of similar mass ────────────────────────────────────────
Q8 = FIG + 'paper-q8'
# (a)(i): the scheme draws the two structures in a table, each priced (3) under
# its name: the rows are those names, the drawings shown with the answer.
_q8a1 = P.items(k('8', 'a', 'i'))
assert [it.cell for it in _q8a1] == ['[2 × 3]', '[3]', '[3]'], _q8a1
assert raw(20, 90, 105) == 'propan-1-ol propanal', raw(20, 90, 105)
C.add([k('8', 'a', 'i')], 'chem-4-2', 'structures-of-propan-1-ol-and-propanal', [
    lift('r-1', 'propan-1-ol', 3, 'B, drawn with all its bonds; the scheme prices the two drawings (2 × 3), '
         'one each, and its own print of them is shown with the answer. It adds: '
         + ' '.join(_q8a1[2].asides)),
    lift('r-2', 'propanal', 3, 'C, drawn with all its bonds.')], figure=S + 'q8a-i')
print_question('paper-q8a-i-print')
C.fixed([k('8', 'a', 'ii')], 'chem-2-2', 'one-tetrahedral-carbon-in-ethanoic-acid', figure=Q8)
# (b)(i): the two terms the paper underlines: structural isomers (2 x 3), then
# primary alcohol (6), any one of three wordings the scheme sets after "or".
_q8b1 = P.items(k('8', 'b', 'i'))
assert [it.cell for it in _q8b1] == ['[2 × 3]', '[6]', '[6]', '[6]'], _q8b1
_si = _q8b1[0].points()
assert _si[0] == 'structural isomers:' and len(_si) == 3, _si
_pa = [display(it.text) for it in _q8b1[1:]]
assert _pa[0].startswith('primary alcohol: '), _pa
C.add([k('8', 'b', 'i')], 'chem-4-2', 'structural-isomers-and-primary-alcohols', [
    lift('r-1', _si[1], 3, 'structural isomers: the scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _si[2], 3),
    menu_row('r-3', [_pa[0][len('primary alcohol: '):]] + _pa[1:], 1,
             'primary alcohol: any one of these wordings, the scheme setting each after "or", (6). It adds: '
             + ' '.join(_q8b1[3].asides), per=6, total=6)], total=12)
print_question('paper-q8b-i-print')
C.fixed([k('8', 'b', 'ii')], 'chem-4-2', 'a-structural-isomer-of-propanal', figure=S + 'q8b-ii',
        fixes={'CH₃COCH₃ / (CH₃)₂CO / / correct structure of another isomer':
               'CH₃COCH₃ / (CH₃)₂CO / correct structure of another isomer'},
        row_notes={0: 'The scheme also draws propanone between these two answers; its drawing is shown with '
                      'the answer.'})
print_question('paper-q8b-ii-print')
_q8b3 = P.items(k('8', 'b', 'iii'))
assert [it.cell for it in _q8b3] == ['[3]'], _q8b3
C.fixed([k('8', 'b', 'iii')], 'chem-4-2', 'naming-the-isomer-of-propanal', figure=S + 'q8b-iii')
shown('The scheme lists the structural isomers of propanal with their names; its table is shown with the '
      'answer.')
print_question('paper-q8b-iii-print')
_q8c = P.ask(k('8', 'c'))
assert _q8c == 'Explain clearly why', _q8c
C.fixed([k('8', 'c', 'i')], 'chem-2-2', 'boiling-points-of-propanal-and-butane', figure=Q8)
C.menu([k('8', 'c', 'ii')], 'chem-2-2', 'boiling-points-of-ethanoic-acid-and-propan-1-ol', figure=Q8,
       note='Any two of these: "' + raw(22, 265, 279, 460) + '".')
C.fixed([k('8', 'd')], 'chem-4-2', 'oxidising-propanal', figure=Q8,
        row_notes={0: 'The scheme also draws the structure of propanoic acid.'})
C.fixed([k('8', 'e')], 'chem-4-2', 'propan-1-ol-and-sodium', figure=Q8)

# ── Q9 Phosgene equilibrium ──────────────────────────────────────────────────
Q9 = FIG + 'paper-q9-eq'
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a] == ['[5]'], _q9a
_w = _q9a[0].points()
assert len(_w) == 2 and _w[0].endswith(' or'), _w
C.add([k('9', 'a')], 'chem-3-3', 'what-a-chemical-equilibrium-is', [menu_row(
    'r-1', [_w[0][:-len(' or')], _w[1]], 1, 'Either of these, the scheme setting the second after "or", (5). It '
    'writes "rr", "rf" and "rb" with the second letter as a subscript.',
    per=5, total=5)], total=5, figure=Q9)
C.drawn([k('9', 'b')], 'chem-3-3', 'kc-expression-for-phosgene', S + 'q9b')
print_question('paper-q9b-print')
_q9c3 = P.items(k('9', 'c', 'iii'))
assert [it.cell for it in _q9c3] == ['[3]', '[3]', None], _q9c3
_order = display(_q9c3[2].text)
assert _order == '[Accept any order of answering STATE and EXPLAIN in each of (i), (ii) and (iii) above.][Not linked.]', _order
for r, concept, fixes in (
        ('i', 'pressure-and-the-colour-of-the-mixture',
         {'STATE & mixture becomes less green / colour fades': 'mixture becomes less green / colour fades'}),
        ('ii', 'temperature-and-the-yield-of-phosgene',
         {'STATE & smaller yield / less phosgene': 'smaller yield / less phosgene'}),
        ('iii', 'a-catalyst-and-the-value-of-kc', {'STATE & no effect (none) /': 'no effect (none)'})):
    C.fixed([k('9', 'c', r)], 'chem-3-3', concept, figure=Q9, fixes=fixes, skip=(_order,) if r == 'iii' else ())
    shown('The scheme adds: ' + _order, -1)
C.answer_only([k('9', 'd')], 'chem-3-3', 'kc-for-phosgene-from-85-percent-reaction', S + 'q9d',
              notes='The scheme sets out two boxed routes, in moles then dividing by 12.0, or dividing the '
                    'initial moles by 12.0 first, each priced (3), (3), (6), (3).')
shown('The scheme prices the steps of either of its two boxed routes (3), (3), (6) and (3), and adds that '
      'marks are not mixed and matched within boxes.')
print_question('paper-q9d-print')
C.fixed([k('9', 'e')], 'chem-3-3', 'why-low-temperature-and-high-pressure-are-avoided', figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the paper sets four asks before its (i) -- DESCRIBE (2 x 3), WOULD (3)
# and EXPLAIN (3) under (12), then EXPLAIN the underlined term (3) -- and one
# after its (ii), under (13).
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == ['[2 × 3]', '[3]', '[3]', '[3]'], _q10a
_d = _q10a[0].points()
assert len(_d) == 2, _d
_lead = P.lead(k('10', 'a'))
_deloc, _howmany = cut(_lead, 'How many electrons')
C.add([k('10', 'a')], 'chem-4-2', 'addition-to-ethene-and-delocalisation-in-benzene', [
    lift('r-1', _d[0], 3, 'DESCRIBE. The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _d[1], 3),
    lift('r-3', _q10a[1].text, 3, 'WOULD.'),
    lift('r-4', _q10a[2].text, 3, 'EXPLAIN. The scheme adds: ' + ' '.join(_q10a[2].asides)),
    lift('r-5', _q10a[3].text, 3, 'EXPLAIN the underlined term. The scheme adds: ' + ' '.join(_q10a[3].asides))],
    qtext=P.ask(k('10', 'a')) + ' ' + _deloc)
print_question('paper-q10a-print')
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [it.cell for it in _q10a2] == ['[3]', '[4]'], _q10a2
_sig, _haz = cut(P.ask(k('10', 'a', 'ii')), 'What health hazard')
C.fixed([k('10', 'a', 'i')], 'chem-4-2', 'delocalised-electrons-in-benzene', stem=_howmany)
C.add([k('10', 'a', 'ii')], 'chem-4-2', 'sigma-bonding-electrons-in-benzene', [lift('r-1', _q10a2[0].text, 3)],
      qtext=_sig, stem=_howmany)
C.add([k('10', 'a')], 'chem-4-2', 'health-hazard-of-benzene', [lift('r-1', _q10a2[1].text, 4)],
      qtext=_haz, stem='', cid='q10-a-after-ii', ref_suffix='after (ii)')
C.fixed([k('10', 'b', 'i')], 'chem-1-2', 'ground-state')
C.fixed([k('10', 'b', 'ii')], 'chem-1-2', 'excited-state')
C.fixed([k('10', 'b', 'iii')], 'chem-1-2', 'what-raises-an-electron-from-the-ground-state')
C.fixed([k('10', 'b', 'iv')], 'chem-1-2', 'why-electrons-fall-back-from-excited-states')
# (v), then two asks the paper sets after it under (b)'s one mark: HOW (2 x 2),
# any one of three wordings, and WHAT (2 x 3), either of two.
_q10b5 = P.items(k('10', 'b', 'v'))
assert [it.cell for it in _q10b5] == ['[3]', '[2 × 2]', '[2 × 2]', '[2 × 2]', '[2 × 3]'], _q10b5
_v, _bohr = cut(P.ask(k('10', 'b', 'v')), 'Bohr’s theory')
_bohr_ctx, _bohr_ask = cut(_bohr, 'How does modern')
C.add([k('10', 'b', 'v')], 'chem-1-2', 'level-the-visible-hydrogen-lines-fall-to', [lift('r-1', _q10b5[0].text, 3)],
      qtext=_v)
_how = [it.points() for it in _q10b5[1:4]]
assert all(len(p) == 2 for p in _how), _how
_orb = _q10b5[4].points()
assert len(_orb) == 4 and _orb[2] == 'approximate solution', _orb
C.add([k('10', 'b')], 'chem-1-2', 'wave-particle-duality-and-orbitals', [
    menu_row('r-1', [p[0] for p in _how], 1, 'HOW: one of these wordings, the scheme setting each after "or"; '
             'it prices the two points of each (2 × 2), one each.', per=2, total=2),
    menu_row('r-2', [p[1] for p in _how], 1, 'And the second point of that same wording, (2).', per=2, total=2),
    menu_row('r-3', [_orb[0], _orb[2]], 1, 'WHAT: one of these wordings, the scheme setting the second after '
             '"or"; it prices the two points of each (2 × 3), one each. It adds: ' + ' '.join(_q10b5[4].asides),
             per=3, total=3),
    menu_row('r-4', [_orb[1], _orb[3]], 1, 'And the second point of that same wording, (3).', per=3, total=3)],
    total=10, qtext=_bohr_ask, stem=_bohr_ctx, cid='q10-b-after-v', ref_suffix='after (v)')
C.route([k('10', 'c', 'i')], 'chem-1-4', 'moles-of-iron-from-iron-phosphate',
        fixes={'4.53 ⇒ 0.03 moles iron 151 = 0.03 moles iron phosphate':
               '4.53 ÷ 151 = 0.03 moles iron phosphate ⇒ 0.03 moles iron'},
        row_notes={1: FRACTION.format('4.53', '151')})
C.route([k('10', 'c', 'ii')], 'chem-1-4', 'mass-of-rust-from-moles-of-iron')
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'volume-of-phosphoric-acid-needed',
        fixes={'0.03 moles phosphoric acid x × 6.0 1000 = 0.03 moles': 'x × 6.0 ÷ 1000 = 0.03 moles'},
        row_notes={0: 'The scheme opens this step with "0.03 moles phosphoric acid". '
                      + FRACTION.format('x × 6.0', '1000')})
C.route([k('10', 'c', 'iv')], 'chem-1-4', 'volume-of-water-produced')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('11', 'a', 'i')], 'chem-2-1', 'definition-of-electronegativity')
C.fixed([k('11', 'a', 'ii')], 'chem-2-1', 'polar-covalent-carbon-chlorine-bond')
C.fixed([k('11', 'a', 'iii')], 'chem-2-1', 'valency-of-carbon')
C.fixed([k('11', 'a', 'iv')], 'chem-2-2', 'shape-of-tetrachloromethane')
C.fixed([k('11', 'a', 'v')], 'chem-2-1', 'dot-and-cross-diagram-of-carbon-disulfide', figure=S + 'q11a-v')
shown('The scheme draws the diagram two ways; its own print is shown with the answer.')
# (b): its own two asks (6), then (i) and (ii) (9), then three asks the paper
# sets after (ii) beside the pH curve, under (10).
C.fixed([k('11', 'b')], 'chem-3-4', 'arrhenius-and-bronsted-lowry-bases')
_calc = P.lead(k('11', 'b'))
assert _calc == 'Calculate the pH value of', _calc
C.route([k('11', 'b', 'i')], 'chem-3-4', 'ph-of-a-strong-acid', stem=_calc)
_q11b2 = P.items(k('11', 'b', 'ii'))
assert [it.cell for it in _q11b2] == ['[6]', '[3]', '[3]', '[3]', '[3 + 1]', '[3]'], _q11b2
_ka, _curve = cut(P.ask(k('11', 'b', 'ii')), 'The pH curve shown')
_curve_ctx, _curve_ask = cut(_curve, 'Which of the two')
_aside = [a for a in _q11b2[3].asides if a.startswith('[–2.52')]
assert len(_aside) == 1, _q11b2[3].asides
C.answer_only([k('11', 'b', 'ii')], 'chem-3-4', 'ph-of-a-weak-acid', S + 'q11b-ii', qtext=_ka, stem=_calc,
              notes='The scheme gives the answer, priced (6), then the working: pH = –log of the square root '
                    'of Ka × [HA] (3), and pH = 2.52 (3).')
shown('The scheme prices the working (3) for the expression and (3) for pH = 2.52, and adds: ' + _aside[0])
_which = display(_q11b2[3].text)
assert _which.endswith(' ethanoic acid / CH₃COOH'), _which
_state = _q11b2[4].options()
assert len(_state) == 3, _state
_two = raw(27, 707, 720, 460)
assert _two == 'ANY TWO: (3 + 1)', _two
C.add([k('11', 'b')], 'chem-3-4', 'reading-a-weak-acid-strong-base-ph-curve', [
    lift('r-1', 'ethanoic acid / CH₃COOH', 3, 'WHICH.'),
    menu_row('r-2', _state, 2, 'STATE: any two of these, the first (3) and the second (1): "' + _two + '". The '
             'scheme adds: ' + ' '.join(a for a in _q11b2[4].asides if not a.startswith('[any')),
             per=3, steps=[3, 1], total=4),
    lift('r-3', _q11b2[5].text, 3, 'WHAT.')],
    total=10, figure=FIG + 'paper-q11b', qtext=_curve_ask,
    stem=tidy(_calc + ' (i) ' + P.ask(k('11', 'b', 'i')) + ' (ii) ' + _ka + ' ' + _curve_ctx),
    cid='q11-b-after-ii', ref_suffix='after (ii)')
# (c)A: three alternative case studies, (i), (ii) and (iii), 25 each; each
# sets its scene, then several asks under two or three marks.


def case(r, concept, scene_end, rows, total):
    ask = tidy(P.ask(ka('11', 'c', r, 'A')) + ' ' + P.lead(ka('11', 'c', r, 'A')))
    scene, asks = cut(ask, scene_end)
    C.add([ka('11', 'c', r, 'A')], 'chem-u3', concept, rows, total=total, qtext=asks, stem=scene)


_a1 = P.items(ka('11', 'c', 'i', 'A'))
assert [it.cell for it in _a1] == ['[3 + 3]', '[3 + 3]', '[3]', '[6]', '[4]'], _a1
_nl = raw(28, 93, 106)
assert _nl == '[Equations not linked.][Any order acceptable.]', _nl
assert display(_a1[2].text).startswith(_nl + ' '), _a1[2].text
case('i', 'magnesium-oxide-from-seawater', 'Write balanced equations', [
    lift('r-1', _a1[0].text, 6, eq_note(28, 52.8)),
    lift('r-2', _a1[1].text, 6, eq_note(28, 80.9) + ' The scheme adds: ' + _nl),
    lift('r-3', display(_a1[2].text)[len(_nl):], 3, 'WHAT.'),
    lift('r-4', _a1[3].text, 6, 'IDENTIFY.'),
    lift('r-5', _a1[4].text, 4, 'STATE.')], 25)
_a2 = P.items(ka('11', 'c', 'ii', 'A'))
assert [it.cell for it in _a2] == ['[3]', '[2 × 3]', '[3 + 3]', '[3 + 3]', '[4]'], _a2
assert display(_a2[4].text).startswith(_nl + ' '), _a2[4].text
_any = raw(28, 350, 363, 460)
assert _any == 'ANY TWO: (2 × 3)', _any
case('ii', 'nitric-acid-from-ammonia', 'Identify the catalyst', [
    lift('r-1', _a2[0].text, 3, 'IDENTIFY.'),
    menu_row('r-2', _a2[1].options(), 2, 'WHAT: any two of these, (3) each: "' + _any + '".', per=3, total=6),
    lift('r-3', _a2[2].text, 6, eq_note(28, 378.4)),
    lift('r-4', _a2[3].text, 6, eq_note(28, 433.2) + ' The scheme adds: ' + _nl),
    lift('r-5', display(_a2[4].text)[len(_nl):], 4, 'EXPLAIN.')], 25)
_a3 = P.items(ka('11', 'c', 'iii', 'A'))
assert [it.cell for it in _a3] == ['[2 × 3]', '[3]', '[3 + 3]', '[4]', '[3 + 3]'], _a3
_p = _a3[0].points()
assert len(_p) == 2, _p
# (iii) sets five asks, each priced by a cell of its own, too many rows for one
# fixed card: two cards on the part, its conditions and catalyst (9), then its
# feedstocks and urea (16), each showing the scene and its own asks. Each names
# which asks it holds after the citation, so the build keeps both.
_a3ask = tidy(P.ask(ka('11', 'c', 'iii', 'A')) + ' ' + P.lead(ka('11', 'c', 'iii', 'A')))
_a3scene, _a3asks = cut(_a3ask, 'State the (approximate)')
_a3first, _a3rest = cut(_a3asks, 'Write a balanced equation to show')
assert _a3first.endswith('What catalyst is used?') and _a3rest.endswith('urea from ammonia.'), (_a3first, _a3rest)
C.add([ka('11', 'c', 'iii', 'A')], 'chem-u3', 'conditions-and-catalyst-for-the-haber-process', [
    lift('r-1', _p[0], 3, 'STATE. The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _p[1], 3),
    lift('r-3', _a3[1].text, 3, 'WHAT.')], qtext=_a3first, stem=_a3scene, ref_suffix='conditions and catalyst')
C.add([ka('11', 'c', 'iii', 'A')], 'chem-u3', 'feedstocks-for-ammonia-and-making-urea', [
    lift('r-1', _a3[2].text, 6, eq_note(28, 636.4)),
    lift('r-2', _a3[3].text, 4, 'EXPLAIN.'),
    lift('r-3', _a3[4].text, 6, eq_note(28, 745.0))], qtext=_a3rest, stem=_a3scene,
    cid='q11-c-a-iii-feedstocks', ref_suffix='feedstocks and urea')
_b1 = P.items(ka('11', 'c', 'i', 'B'))
assert [it.cell for it in _b1] == ['[3 + 3]', '[3 + 3]', None], _b1
_allow = raw(29, 145, 159)
assert _allow == '[Allow NaAl(OH)₄ in balanced equation for NaAlO₂.][Other versions also possible.]', _allow
assert display(_b1[1].text).startswith(_allow + ' ') and display(_b1[2].text) == _nl, _b1
C.add([ka('11', 'c', 'i', 'B')], 'chem-u3', 'alumina-from-sodium-aluminate', [
    lift('r-1', _b1[0].text, 6, eq_note(29, 134.2) + ' The scheme adds: ' + _allow),
    lift('r-2', display(_b1[1].text)[len(_allow):], 6, eq_note(29, 202.5) + ' The scheme adds: ' + _nl)])
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-u3', 'electrolysis-of-alumina')
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-u3', 'making-aluminium-economically-and-greener')


# A note quoted from the scheme in the reader's script notation ("K_(c)") is
# shown as the page sets it, "Kc".
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'], _r


# ── review ───────────────────────────────────────────────────────────────────
# Q11(c)A(iii) sets its last mark in the run of its last ask, "... the formation
# of urea from ammonia. (6)" (paper page 11, y 567): the reader takes the mark
# off the line without recording it among the part's marks.
_urea = [l for l in P.paper_lines if l.page == 11 and l.text.endswith('urea from ammonia. (6)')]
assert len(_urea) == 1, _urea
INLINE = {('11', 'c'): 6}


def printed():
    """Every letter's printed marks: the paper sets one mark after a letter's
    last part, or -- Q10(a), Q11 -- several, one after each run of asks."""
    out = {}
    for key, last in P.marks.items():
        if not key[1]:
            continue
        at = [m for s in P.pseg if s.key[:2] == key[:2] for _n, m in s.marks_at]
        out[key] = sum(at) + INLINE.get(key[:2], 0) if at else last
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
        if key[:2] == ('11', 'c'):
            line += (' (A(i), A(ii), A(iii) and B are alternatives, 25 each; the paper prints each '
                     'one\'s marks, 4 x 25)')
        if key[:2] == ('10', 'a') or key[:2] == ('11', 'b'):
            line += ' (asks the paper sets unnumbered are carded as the letter\'s own, or after its last roman)'
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
