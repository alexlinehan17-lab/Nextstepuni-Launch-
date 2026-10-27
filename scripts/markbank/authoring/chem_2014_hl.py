#!/usr/bin/env python3
"""2014 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2014_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2014_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2014_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2014 hl

No 2014 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

The 2014 scheme is the labelled ("cue") layout. It heads Questions 2 and 4
"QUSESTION 2" and "QUSESTION 4" (PDF pages 7 and 10), an SEC misprint the
reader now reads as the heads they are (chem_print.Printed, gated to 2014 HL);
without it the scheme never left Question 1.

The census keeps the paper's 75 asks. Romans the paper sets inside one sentence
are one census ask and a card per scheme cell, each showing the sentence with a
"For (i)."-style note: Q1(e) ("in (i) moles per litre, (ii) grams per litre",
a cell each), Q5(a) ("Hence, state how many (i) main energy levels, (ii) atomic
orbitals", one cell (2 x 3): one card cited over both), Q5(b) (its (i) and (ii)
each open a line of their own, paper page 4, y 645 and 660, but continue the
sentence "Explain why the first ionisation energy value of silicon is"; the
paper reader keys them apart, the census keeps Q5(b) whole, and the cards, a
cell each, cite Q5(b)(i) and (ii), which reconcile reads as Q5(b)), Q9(c), Q10(b)
and Q10(c). Asks the paper sets unnumbered after a letter's romans are a card
each cited "— after (ii), ..." or "— after (iv), ..." (Q10(b), Q10(c)). Where a
letter's asks would outrun a card's five rows, each ask, or each run under one
printed mark, is a card cited with what it holds (Q2(a), Q5(a), Q6(d), Q7(c),
Q11(a)). Q4(k) and Q11(c) offer alternative parts A and B.

The paper underlines the term Q1(a) and Q11(c)B(i) ask about, which no text
layer carries: those cards take the paper's own print as their question, as do
the parts whose figure is the scheme's and whose ask needs the paper's
equation, nuclide, table or formulae (Q2(e), Q2(f), Q3(c), Q3(e), Q4(c), Q8(a),
Q8(b), Q8(d)(ii), Q9(b), Q10(a)(ii), Q10(a)(iii)). The equations of Q7(b) and
Q9 set their equilibrium arrow in a glyph the text layer cannot read (U+0595):
they are paper crops, kept out of the text.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, norm, read_lines, tidy  # noqa: E402

P = Printed(2014, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2014-HL-'
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


def traced(text):
    """A string quoted from the scheme in a note, checked against the scheme."""
    if not P.traceable(text):
        raise Refused(f'"{text}" is not in the 2014 hl scheme')
    return text


def cut(text, at):
    """`text` split where `at` begins (the paper's print, cut between two asks
    it sets in one run)."""
    i = text.index(at)
    return text[:i].strip(), text[i:].strip()


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 Water of crystallisation in washing soda ──────────────────────────────
Q1_STEM = C.context(k('1', 'a'))
assert Q1_STEM.startswith('A batch of washing soda crystals') and Q1_STEM.endswith('2NaCl + H₂O + CO₂'), Q1_STEM
# (a): the paper underlines "standardised" (page 2, y 179); its own print is the question.
assert cells(k('1', 'a')) == ['[5]'], cells(k('1', 'a'))
C.fixed([k('1', 'a')], 'chem-4-1', 'a-standardised-solution', stem=Q1_STEM)
print_question('paper-q1a-print')
# (b): DISSOLVED AND MADE-UP: four points priced (6 + 3 + 3) -- a choice of
# three, the first claimed (6), the others (3), in the cell's order.
_q1b = P.items(k('1', 'b'))
_o = [display(x) for x in _q1b[0].options()]
assert [it.cell for it in _q1b] == ['[6 + 3 + 3]'] and len(_o) == 4 and _o[2].startswith('MADE-UP: '), _o
C.menu([k('1', 'b')], 'chem-4-1', 'making-up-a-standard-solution-of-a-solid', claim=3, stem=Q1_STEM,
       fixes={_o[2]: _o[2][len('MADE-UP: '):]},
       note='The scheme lists four points under "DISSOLVED AND MADE-UP:" and prices three of them (6 + 3 + 3): '
            'the first point claimed earns (6), the next two (3) each.')
C.fixed([k('1', 'c')], 'chem-4-1', 'a-precaution-near-the-end-point', stem=Q1_STEM,
        row_notes={0: 'STATE.', 1: 'EXPLAIN.'})
# (d): NAME (3); CHANGE, before // after (2 x 3), read from the scheme's table
# (page 5, y 387-452), matched with the indicator named.
_q1d = P.items(k('1', 'd'))
assert [it.cell for it in _q1d] == ['[3]', '[2 × 3]', '[3]', '[3]', None], _q1d
_names = display(_q1d[0].text)
assert _names == 'methyl orange / methyl red / bromophenol blue / bromocresol green', _names
_tab = [raw(5, y - 1, y + 16, 150, 480) for y in (399.6, 412.1, 424.9, 437.5)]
_before, _after = [], []
for _row, _name in zip(_tab, _names.split(' / ')):
    _l, _r = _row.split(' // ')
    assert _l.startswith(_name + ' '), (_row, _name)
    _before.append(_l[len(_name) + 1:])
    _after.append(_r)
assert _before == ['orange (yellow)', 'orange (yellow)', 'blue (purple, violet)', 'blue'], _before
assert _after == ['red (pink, peach)', 'red (pink)', 'yellow', 'yellow'], _after
_match = traced('[Colour change must be matched with named indicator.]')
C.add([k('1', 'd')], 'chem-4-1', 'indicator-for-a-carbonate-titration', [
    lift('r-1', _names, 3, 'NAME.'),
    menu_row('r-2', list(dict.fromkeys(_before)), 1, 'CHANGE: the colour before, (3), of the indicator named; the '
             'scheme\'s table, shown with the answer, gives each indicator\'s colours. The scheme adds: ' + _match,
             per=3, total=3),
    menu_row('r-3', list(dict.fromkeys(_after)), 1, 'And the colour after, (3), of the same indicator.',
             per=3, total=3)], total=9, stem=Q1_STEM, figure=S + 'q1d')
# (e): the paper sets (i) and (ii) inside one sentence (page 2, y 410-436); the
# scheme prices each with a cell of its own.
Q1E = P.ask(k('1', 'e'))
assert Q1E.endswith('in (i) moles per litre, (ii) grams per litre.'), Q1E
_q1e1 = P.items(k('1', 'e', 'i'))
assert [it.cell for it in _q1e1][0] == '[6]' and display(_q1e1[0].text) == '0.0432 M', _q1e1
_round = raw(5, 525, 576, 355, 545)
assert _round.startswith('[M = 0.04 or 0.043, deduct 1 mark') and _round.endswith('made once only.]'), _round
C.add([k('1', 'e', 'i')], 'chem-4-1', 'molarity-of-sodium-carbonate-from-a-titration', [
    lift('r-1', _q1e1[0].text, 6, 'For (i). The scheme prices the answer (6) and works it in two steps, (3) each: the '
         'titration formula, set as fractions, then M = 0.0432; its own print is shown with the answer. It adds: '
         + ' '.join(_q1e1[0].asides) + ' ' + _round)],
    qtext=Q1E, stem=Q1_STEM, figure=S + 'q1e-i')
C.route([k('1', 'e', 'ii')], 'chem-4-1', 'concentration-of-sodium-carbonate-in-grams-per-litre', qtext=Q1E,
        stem=Q1_STEM, row_notes={0: 'For (ii).'})
# (f): % WATER (3), the working in a box beside it; VALUE OF x (6), ten routes
# in a table of two columns, each two steps (3) each.
_q1f = P.items(k('1', 'f'))
assert _q1f[0].cell == '[3]' and display(_q1f[0].text) == '% WATER: 54 – 54.4%', _q1f
assert _q1f[2].cell == '[6]' and display(_q1f[2].text).endswith('VALUE OF x: 6.9 – 7'), _q1f
_remind = traced('[Reminder: second 3 may be awarded consequentially.]')
C.add([k('1', 'f')], 'chem-4-1', 'water-of-crystallisation-in-washing-soda', [
    lift('r-1', '54 – 54.4%', 3, '% WATER. The scheme works it in a box beside the answer: hydrated, anhydrous and '
         'water masses, then the percentage; its own print is shown with the answer.'),
    lift('r-2', '6.9 – 7', 6, 'VALUE OF x. The scheme sets out ten routes, side by side in pairs, each in two steps '
         '(3) each, and adds: ' + _remind)],
    stem=Q1_STEM, figure=S + 'q1f')

# ── Q2 Preparing soap ────────────────────────────────────────────────────────
Q2 = FIG + 'paper-q2'
# (a): PURPOSE, two points priced (3 + 2); NAME (3). A card each.
_q2a = P.items(k('2', 'a'))
assert [it.cell for it in _q2a] == ['[3 + 2]', '[3]'], _q2a
Q2A_PURP, Q2A_NAME = cut(P.ask(k('2', 'a')), 'Name the type')
_pp = [display(x) for x in _q2a[0].points()]
assert len(_pp) == 2 and _pp[1].startswith('without losing'), _pp
C.add([k('2', 'a')], 'chem-u2', 'refluxing-in-soap-making', [
    lift('r-1', _pp[0], None), lift('r-2', _pp[1], None)],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), qtext=Q2A_PURP, figure=Q2,
    cid='q2-a-reflux', ref_suffix='purpose of refluxing')
C.add([k('2', 'a')], 'chem-4-2', 'saponification', [
    lift('r-1', _q2a[1].text, 3, 'NAME. The scheme adds: ' + ' '.join(_q2a[1].asides))],
    qtext=Q2A_NAME, figure=Q2, cid='q2-a-reaction', ref_suffix='type of reaction')
C.fixed([k('2', 'b')], 'chem-u2', 'ethanol-removed-by-distillation', figure=Q2)
C.fixed([k('2', 'c')], 'chem-u2', 'brine-precipitating-the-soap', figure=Q2)
C.fixed([k('2', 'd')], 'chem-u2', 'washing-the-soap', figure=Q2, row_notes={0: 'WHY.', 1: 'HOW.'})
# (e): DRAW or NAME (6), the structures drawn in a row (page 7, y 326-366);
# WHERE (3). The co-product is the paper's equation's: its own print is the question.
_q2e = P.items(k('2', 'e'))
assert [it.cell for it in _q2e] == ['[6]', '[3]'], _q2e
assert display(_q2e[0].text).endswith('propane-1,2,3-triol / glycerol / glycerine'), _q2e
C.add([k('2', 'e')], 'chem-4-2', 'glycerol-the-co-product-of-saponification', [
    lift('r-1', 'propane-1,2,3-triol / glycerol / glycerine', 6, 'DRAW or NAME: the name, or the structure as the '
         'scheme draws it, in full, as a skeleton or as CH₂OHCHOHCH₂OH; its own print is shown with the answer. It '
         'adds: ' + ' '.join(_q2e[0].asides)),
    lift('r-2', _q2e[1].text, 3, 'WHERE. The scheme adds: ' + ' '.join(_q2e[1].asides))],
    figure=S + 'q2e')
print_question('paper-q2e-print')
# (f): GIVEN (12); four steps (3) each, the first two on one row: 4.45 over 890,
# set as a fraction, (3), then 0.005 mol fat (3).
_q2f = P.items(k('2', 'f'))
assert [it.cell for it in _q2f] == ['[12]', '[3]', '[3]', '[3]'] and display(_q2f[0].text) == '4.59 g', _q2f
assert display(_q2f[1].text) == '4.45 890 (3) = 0.005 mol fat', _q2f
_mr = raw(7, 538, 590, 430)          # the box beside the working (page 7, x 435-539)
assert _mr == 'For incorrect Mr (for 890 or 306), apply usual deductions of –3 and – 1, respectively. See page 1.', _mr
C.add([k('2', 'f')], 'chem-1-4', 'maximum-yield-of-soap', [
    lift('r-1', '0.005 mol fat', 6, 'The scheme prints 4.45 over 890 as a fraction and prices it (3), then "= 0.005 mol '
         'fat" (3). Beside the working it adds: "' + _mr + '"'),
    lift('r-2', _q2f[2].text, 3),
    lift('r-3', _q2f[3].text, 3, 'The scheme adds: ' + ' '.join(_q2f[3].asides))],
    figure=S + 'q2f',
    notes='The scheme gives the answer, 4.59 g, priced (12), then four steps (3) each, the first two on one row.')
shown('The scheme gives the answer as "4.59 g" (12); its own print of the working is shown with the answer.')
print_question('paper-q2f-print')
_q2g = P.items(k('2', 'g'))
_g = display(_q2g[0].text)
assert _g.startswith('C17H35 {hydrocarbon') and '(non- polar substances)' in _g, _g
C.fixed([k('2', 'g')], 'chem-2-2', 'how-soap-dissolves-oils-and-salts', figure=Q2,
        fixes={_g: _g.replace('C17H35', 'C₁₇H₃₅').replace('(non- polar', '(non-polar')})

# ── Q3 Temperature and the rate of the thiosulfate reaction ──────────────────
Q3T = FIG + 'paper-q3-table'
_q3a = P.items(k('3', 'a'))
assert [(it.cell, it.text) for it in _q3a][1:] == [(None, 'time')], _q3a
_rate = display(_q3a[0].text)
_frac = 'change in concentration of one reactant (product)'
assert _rate.endswith(' / ' + _frac), _rate
C.add([k('3', 'a')], 'chem-3-2', 'rate-of-reaction', [
    lift('r-1', _rate + ' ÷ time', 5, FRACTION.format('its last form, "' + _frac + '",', '"time"'))], figure=Q3T)
_q3b1 = P.items(k('3', 'b', 'i'))
assert [it.cell for it in _q3b1] == ['[3]', '[3]'], _q3b1
C.fixed([k('3', 'b', 'i')], 'chem-3-2', 'sulfur-clouding-the-thiosulfate-reaction', figure=Q3T,
        row_notes={0: 'DESCRIBE.', 1: 'EXPLAIN.'})
C.fixed([k('3', 'b', 'ii')], 'chem-u2', 'timing-the-reaction-by-the-cross', figure=Q3T)
# (c): PLOT, four criteria (4 x 3) beside the scheme's graph (page 8); the ask
# needs the paper's table: its own print is the question.
_q3c = P.items(k('3', 'c'))
assert [it.cell for it in _q3c] == ['[4 × 3]'], _q3c
C.fixed([k('3', 'c')], 'chem-3-2', 'plotting-rate-against-temperature', figure=S + 'q3c',
        row_notes={3: 'The scheme\'s graph is shown with the answer.'})
print_question('paper-q3c-print')
# (d): DESCRIBE, two wordings, the second after "or", each two points (2 x 3);
# EXPLAIN (3).
_q3d = P.items(k('3', 'd'))
_d = [display(x) for x in _q3d[0].points()]
assert [it.cell for it in _q3d] == ['[2 × 3]', '[3]'] and len(_d) == 4 and raw(9, 80, 96) == 'or', _q3d
C.add([k('3', 'd')], 'chem-3-2', 'rate-rising-with-temperature', [
    menu_row('r-1', [_d[0], _d[2]], 1, 'DESCRIBE: one of these wordings, the scheme setting the second after "or"; it '
             'prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_d[1], _d[3]], 1, 'And the second point of that same wording, (3).', per=3, total=3),
    lift('r-3', _q3d[1].text, 3, 'EXPLAIN. The scheme adds: ' + ' '.join(_q3d[1].asides))], total=9, figure=Q3T)
# (e): the answer (6); two steps (3) each, the second set as a fraction. The ask
# needs the table it is read from: its own print is the question.
_q3e = P.items(k('3', 'e'))
assert [it.cell for it in _q3e] == ['[6]', '[3]', '[3]'] and display(_q3e[0].text) == '66 – 72 s', _q3e
assert display(_q3e[2].text) == '1 Time = 0.0145 = 69 s [66 – 72]', _q3e
C.add([k('3', 'e')], 'chem-3-2', 'reaction-time-read-from-the-graph', [
    lift('r-1', _q3e[1].text, 3),
    lift('r-2', '69 s [66 – 72]', 3, 'The scheme prints "Time =" 1 over 0.0145 as a fraction, "= 69 s [66 – 72]". It '
         'adds: ' + ' '.join(_q3e[2].asides))],
    figure=S + 'q3c',
    notes='The scheme gives the answer, 66 – 72 s, priced (6), then two steps (3) each; its graph shows the reading '
          'at 35 °C.')
shown('The scheme gives the answer as "66 – 72 s" (6); its graph, with the reading at 35 °C marked, is shown with '
      'the answer.')
print_question('paper-q3e-print')
C.fixed([k('3', 'f')], 'chem-3-2', 'halving-the-thiosulfate-concentration', figure=Q3T,
        row_notes={0: 'WHAT.', 1: 'JUSTIFY.'})

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
# (a): (i) and (ii) inside one sentence, priced (2 x 3), one each.
_q4a = P.items(k('4', 'a', 'i'))
assert [(it.cell, display(it.text)) for it in _q4a] == [('[2 × 3]', 'green (yellow-green) // (ii) crimson (red)')], _q4a
C.add([k('4', 'a')], 'chem-1-2', 'flame-colours-of-barium-and-lithium', [
    lift('r-1', 'green (yellow-green)', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'crimson (red)', 3, 'For (ii).')], notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-2', 'thomsons-plum-pudding-model', figure=S + 'q4b', notes=Q4_NOTE,
        row_notes={1: 'The scheme\'s labelled diagram is shown with the answer.'})
# (c): the equation with its nuclides' mass and atomic numbers stacked (scheme
# page 10, y 253-272), which the text layer cannot order: the scheme's print is
# the answer; the paper's nuclide (page 4, y 140-165) its question.
C.drawn([k('4', 'c')], 'chem-1-2', 'beta-decay-of-francium-223', S + 'q4c', notes=Q4_NOTE)
print_question('paper-q4c-print')
C.fixed([k('4', 'd')], 'chem-1-2', 'heisenbergs-uncertainty-principle', figure=FIG + 'paper-q4d', notes=Q4_NOTE)
_q4e = P.items(k('4', 'e', 'i'))
assert [(it.cell, display(it.text)) for it in _q4e] == [('[2 × 3]', '1 sigma // (ii) 2 pi')], _q4e
C.add([k('4', 'e')], 'chem-2-1', 'sigma-and-pi-bonds-in-nitrogen', [
    lift('r-1', '1 sigma', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '2 pi', 3, 'For (ii).')], notes=Q4_NOTE)
# (f): three wordings, each after "or", each two points (2 x 3).
_q4f = P.items(k('4', 'f'))
assert [it.cell for it in _q4f] == ['[2 × 3]'], _q4f
_w = [(raw(10, 420, 437, 130), raw(10, 432, 450, 130)), (raw(10, 482, 500, 130), raw(10, 496, 513, 130)),
      (raw(10, 546, 564, 130), raw(10, 559, 576, 130, 300))]
assert [a[-3:] for a, _b in _w] == [' //'] * 3 and [b[-2:] for _a, b in _w] == [' /', ' /', 'ms'] and \
    [raw(10, y - 1, y + 16) for y in (459.0, 522.2)] == ['or', 'or'], _w
C.add([k('4', 'f')], 'chem-1-4', 'what-a-mole-is', [
    menu_row('r-1', [a[:-len(' //')] for a, _b in _w], 1, 'One of these wordings, the scheme setting each after '
             '"or"; it prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [b.rstrip('/ ') for _a, b in _w], 1, 'And the second point of that same wording, (3). The scheme '
             'adds: ' + _q4f[0].asides[0], per=3, total=3)], total=6, notes=Q4_NOTE)
# (g): the answer (6); two steps (3) each, the first set as fractions.
_q4g = P.items(k('4', 'g'))
assert [it.cell for it in _q4g] == ['[6]', '[3]', '[3]'] and display(_q4g[0].text) == 'SO₃', _q4g
assert display(_q4g[1].text) == '40 60 32 = 1.25; 16 = 3.75 / 1 : 3', _q4g
C.add([k('4', 'g')], 'chem-1-4', 'empirical-formula-of-a-sulfur-oxide', [
    lift('r-1', '1 : 3', 3, 'The scheme prints 40 over 32 = 1.25 and 60 over 16 = 3.75 as fractions, then this '
         'ratio; its own print is shown with the answer.'),
    lift('r-2', 'SO₃', 3)], figure=S + 'q4g', notes=Q4_NOTE)
# (h): the answer (6); three routes side by side, two steps (3) each, set as fractions.
_q4h = P.items(k('4', 'h'))
assert [it.cell for it in _q4h] == ['[6]', '[3]', '[3]', None], _q4h
C.answer_only([k('4', 'h')], 'chem-1-4', 'mass-of-potassium-iodide-for-the-rda', S + 'q4h', notes=Q4_NOTE)
shown('The scheme sets out three routes side by side, each two steps (3) each, and adds: ' + display(_q4h[3].text))
C.menu([k('4', 'i')], 'chem-2-4', 'structures-of-high-octane-hydrocarbons', notes=Q4_NOTE,
       note='"' + raw(11, 186, 204, 440) + '".')
C.menu([k('4', 'j')], 'chem-4-3', 'primary-sewage-treatment', notes=Q4_NOTE, note='"' + raw(11, 237, 254, 440) + '".')
C.menu([ka('4', 'k', None, 'A')], 'chem-u3', 'uses-of-oxygen-from-liquid-air', notes=Q4_NOTE,
       note='"' + raw(11, 350, 368, 440) + '".')
C.menu([ka('4', 'k', None, 'B')], 'chem-3-5', 'advantages-of-anodising-aluminium', notes=Q4_NOTE,
       note='"' + raw(11, 389, 406, 440) + '".')

# ── Q5 Energy levels and ionisation energies of silicon ──────────────────────
# (a): NAME (5) and DISTING (3 and 2 x 3) under (14); WRITE (6) under (6);
# HENCE (i) and (ii) (2 x 3) under (6). Seven rows outrun a card: a card each.
Q5A = P.ask(k('5', 'a'))
Q5A_NAME, _r = cut(Q5A, 'Write the electron')
Q5A_WRITE = _r
assert Q5A_NAME.endswith('energy level and atomic orbital.') and Q5A_WRITE.endswith('in the ground state.'), Q5A
Q5A_HENCE = P.lead(k('5', 'a')) + ' (ii) ' + P.ask(k('5', 'a', 'ii'))
assert Q5A_HENCE == ('Hence, state how many (i) main energy levels, (ii) atomic orbitals, are occupied in the silicon '
                     'atom in its ground state.'), Q5A_HENCE
_q5a = P.items(k('5', 'a'))
assert [it.cell for it in _q5a] == ['[5]', '[3]', '[2 × 3]', '[2 × 3]', '[6]', '[3]', '[3]'], _q5a
_orb1, _orb2 = [display(x) for x in _q5a[2].points()], [display(x) for x in _q5a[3].points()]
assert len(_orb1) == 2 and _orb1[0].startswith('atomic orbital: ') and len(_orb2) == 2 and raw(12, 233, 251) == 'or', \
    (_orb1, _orb2)
C.add([k('5', 'a')], 'chem-1-2', 'bohr-and-energy-levels-against-orbitals', [
    lift('r-1', _q5a[0].text, 5, 'NAME.'),
    lift('r-2', _q5a[1].text, 3, 'DISTING.'),
    menu_row('r-3', [_orb1[0], _orb2[0]], 1, 'One of these wordings for the atomic orbital, the scheme setting the '
             'second after "or"; it prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-4', [_orb1[1], _orb2[1]], 1, 'And the second point of that same wording, (3).', per=3, total=3)],
    total=14, qtext=Q5A_NAME, stem='', figure=FIG + 'paper-q5a', cid='q5-a-bohr', ref_suffix='the scientist; energy level and orbital')
# WRITE: the full configuration (6), or after "or" the short one (3) and the
# distribution in 2p and 3p shown (3); the scheme's boxes are shown with the answer.
_full = raw(12, 295, 315, 130, 300)
assert _full == '1s² 2s² 2px 2 2py 2 2pz 2 3s² 3px 1 3py 1', _full      # the "/" after it at x 298-308
for _a, _b in (('2px 2', '2px²'), ('2py 2', '2py²'), ('2pz 2', '2pz²'), ('3px 1', '3px¹'), ('3py 1', '3py¹')):
    _full = P.rearranged(_full, _a, _b)
_short, _dist = display(_q5a[5].text), display(_q5a[6].points()[0])
assert _short == '1s² 2s² 2p⁶ 3s² 3p²' and _dist == 'distribution of electrons in 2p and 3p clearly shown:', \
    (_short, _dist)
C.add([k('5', 'a')], 'chem-1-2', 'electron-configuration-of-silicon', [
    menu_row('r-1', [_full, _short], 1, 'The configuration with its orbitals written out, which the scheme prices (6) '
             'on its own (claim it here and again below), or after "or" the short configuration (3).',
             per=3, total=3),
    menu_row('r-2', [_full, _dist[:-1]], 1, 'And the full configuration again, or the distribution of electrons in 2p '
             'and 3p clearly shown, (3); the scheme draws both as orbital boxes, shown with the answer. It adds: '
             + _q5a[6].asides[0], per=3, total=3)],
    total=6, qtext=Q5A_WRITE, stem='', figure=S + 'q5a-write', cid='q5-a-configuration',
    ref_suffix='electron configuration')
_q5a1, _q5a2 = P.items(k('5', 'a', 'i')), P.items(k('5', 'a', 'ii'))
assert [(it.cell, it.text) for it in _q5a1] == [(None, '3 //')] and \
    [(it.cell, it.text) for it in _q5a2] == [('[2 × 3]', '8')], (_q5a1, _q5a2)
C.add([k('5', 'a', 'i'), k('5', 'a', 'ii')], 'chem-1-2', 'energy-levels-and-orbitals-occupied-in-silicon', [
    lift('r-1', '3', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '8', 3, 'For (ii).')], qtext=Q5A_HENCE, stem=Q5A_WRITE)
# (b): DEFINE (2 x 3); EXPLAIN (i) (2 x 3) and (ii) (3), the paper setting (i) and
# (ii) on lines of their own inside one sentence (page 4, y 616-672).
# The reader ends (b)'s ask at its first mark, (6): the sentence the romans
# complete is its lead (page 4, y 616-641).
Q5B_DEF, Q5B_WHY = P.ask(k('5', 'b')), P.lead(k('5', 'b'))
assert Q5B_DEF == 'Define first ionisation energy.', Q5B_DEF
Q5B_SENT = Q5B_WHY + ' (i) ' + P.ask(k('5', 'b', 'i')) + ' (ii) ' + P.ask(k('5', 'b', 'ii'))
assert Q5B_SENT == ('Explain why the first ionisation energy value of silicon is (i) greater than that of aluminium, '
                    '(ii) less than that of carbon.'), Q5B_SENT
C.fixed([k('5', 'b')], 'chem-1-3', 'first-ionisation-energy', qtext=Q5B_DEF, stem='')
C.fixed([k('5', 'b', 'i')], 'chem-1-3', 'silicon-above-aluminium-in-ionisation-energy', qtext=Q5B_SENT, stem='',
        row_notes={0: 'For (i).'})
C.fixed([k('5', 'b', 'ii')], 'chem-1-3', 'silicon-below-carbon-in-ionisation-energy', qtext=Q5B_SENT, stem='',
        row_notes={0: 'For (ii).'})
# (c): EXPLAIN (2 x 3), two points, or after "or" any two of three (2 x 3);
# OTHER (3).
_q5c = P.items(k('5', 'c'))
assert [it.cell for it in _q5c] == ['[2 × 3]', '[2 × 3]', '[3]'] and '[any two]' in _q5c[1].asides, _q5c
_e1, _e2 = _q5c[0].points(), _q5c[1].points()
assert len(_e1) == 2 and len(_e2) == 3 and raw(13, 325, 343) == 'or', (_e1, _e2)
_any2 = raw(13, 489, 507, 430)
assert _any2 == 'ANY TWO: (2 × 3)', _any2
C.add([k('5', 'c')], 'chem-1-2', 'ionisation-energies-as-evidence-for-energy-levels', [
    menu_row('r-1', _e1 + _e2, 2, 'EXPLAIN: two points, (3) each: the first two together, or, after "or", any two of '
             'the last three ("' + _any2 + '"). The scheme adds: ' + _q5c[1].asides[1], per=3, total=6),
    lift('r-2', _q5c[2].text, 3, 'OTHER.')], total=9, figure=FIG + 'paper-q5c')

# ── Q6 Propane, butane and its isomer ────────────────────────────────────────
Q6 = FIG + 'paper-q6'
_q6a = P.items(k('6', 'a'))
assert [it.cell for it in _q6a] == ['[5 + 3]'] and display(_q6a[0].text).startswith('alkanes '), _q6a
C.add([k('6', 'a')], 'chem-2-4', 'propane-an-alkane', [
    lift('r-1', 'alkanes', None, 'NAME.'),
    lift('r-2', 'CH₃CH₂CH₃', None, 'DRAW: or the structure in full or as a skeleton, as the scheme draws them, shown '
         'with the answer. It adds: ' + ' '.join(_q6a[0].asides))],
    kind='orderedSplit', notation='[5 + 3]', total=8, notes=SPLIT.format('[5 + 3]'), figure=S + 'q6a')
C.fixed([k('6', 'b')], 'chem-2-2', 'boiling-points-of-propane-and-butane', figure=Q6)
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'structural-isomers', figure=Q6)
_q6c2 = P.items(k('6', 'c', 'ii'))
assert [it.cell for it in _q6c2] == ['[6]'] and len(_q6c2[0].asides) == 2, _q6c2
C.add([k('6', 'c', 'ii')], 'chem-2-4', 'methylpropane-the-isomer-of-butane', [
    menu_row('r-1', ['(CH₃)₂CHCH₃', 'CH(CH₃)₃'], 1, 'One of these, or the structure in full or as a skeleton, as the '
             'scheme draws them, shown with the answer. It adds: ' + ' '.join(_q6c2[0].asides), per=6, total=6)],
    total=6, figure=S + 'q6c-ii')
# (d): DEFINE (2 x 3); WRITE (6), "FORMULAS: (3) BALANCING: (3)"; CALCULATE (12),
# four equations (3) each, then after "or" the sums of heats of formation.
# Under one printed mark (24): a card each, cited with what it holds.
_d6 = P.ask(k('6', 'd'))
Q6D_DEF, _r = cut(_d6, 'Write the balanced')
Q6D_EQ, Q6D_CALC = cut(_r, 'Calculate the heat')
assert Q6D_DEF == 'Define heat of combustion.' and Q6D_CALC.endswith('respectively.'), _d6
_q6d = P.items(k('6', 'd'))
assert [it.cell for it in _q6d][:3] == ['[2 × 3]', '[3]', '[12]'], _q6d
_def = [display(x) for x in _q6d[0].points()]
assert len(_def) == 2, _def
C.add([k('6', 'd')], 'chem-3-1', 'heat-of-combustion', [
    lift('r-1', _def[0], 3, 'The scheme prices these points (2 × 3), one each.'), lift('r-2', _def[1], 3)],
    qtext=Q6D_DEF, figure=Q6, cid='q6-d-definition', ref_suffix='heat of combustion defined')
_cell = raw(14, 570, 588, 380)
assert _cell == 'FORMULAS: (3) BALANCING: (3)', _cell
C.add([k('6', 'd')], 'chem-3-1', 'combustion-of-butane', [
    lift('r-1', 'C₄H₁₀ + 6½O₂ → 4CO₂ + 5H₂O', 6, 'WRITE: "' + _cell + '". The scheme adds: '
         + ' '.join(_q6d[1].asides))],
    qtext=Q6D_EQ, figure=Q6, cid='q6-d-equation', ref_suffix='combustion equation')
_line = display(_q6d[6].text)
assert _line.startswith('_____') and _line.endswith('C₄H₁₀ + 6½O₂ → 4CO₂ + 5H₂O ΔH = – 2877.3 kJ mol⁻¹'), _line
# The answer (12), then four equations (3) each, the last under a rule the text
# layer reads as underscores (scheme page 15, y 107).
assert display(_q6d[2].text) == '– 2877.3 kJ mol⁻¹' and [it.cell for it in _q6d][3:7] == ['[3]'] * 4, _q6d
C.add([k('6', 'd')], 'chem-3-1', 'heat-of-combustion-of-butane-from-heats-of-formation', [
    lift('r-1', _q6d[3].text, 3), lift('r-2', _q6d[4].text, 3), lift('r-3', _q6d[5].text, 3),
    lift('r-4', _line.lstrip('_ '), 3)],
    figure=S + 'q6d', qtext=Q6D_CALC, cid='q6-d-calculation', ref_suffix='heat of combustion',
    notes='The scheme gives the answer, – 2877.3 kJ mol⁻¹, priced (12), then four equations (3) each; after "or" it '
          'works it from the sums of heats of formation, three terms (3) each and the answer (3).')
# Its two notes (page 15, y 237-279) set CnH2n+2 and (n + 1)H2 with scripts the
# text layer reads apart ("C nH2n+2", "(n +1)H ... 2"): quoted as the page sets them.
_alk = raw(15, 236, 281)
assert _alk.startswith('[If 2C₄H₁₀ used above') and _alk.endswith('summation if correct.] 2'), _alk
_alk = P.rearranged(P.rearranged(_alk[:-len(' 2')] + ' 2', 'C nH2n+2', 'CnH2n+2'),
                    '(n +1)H correctly burned and 3 for summation if correct.] 2',
                    '(n +1)H2 correctly burned and 3 for summation if correct.]')
shown('After "or" the scheme sets a second route, from the sums of heats of formation; its own print of both is '
      'shown with the answer. It adds: ' + _alk)

# ── Q7 Nitrous acid ──────────────────────────────────────────────────────────
C.ordered([k('7', 'a')], 'chem-3-4', 'strong-and-weak-acids-bronsted-lowry')
# (b): the equation's arrow is a glyph the text layer cannot read: the paper's
# print of it is the card's figure.
_q7b = P.items(k('7', 'b'))
assert [(it.cell, display(it.text)) for it in _q7b] == [('[2 × 3]', 'H₂O // NO₂ ¯')], _q7b
C.add([k('7', 'b')], 'chem-3-4', 'bases-in-the-nitrous-acid-equilibrium', [
    lift('r-1', 'H₂O', 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'NO₂⁻', 3)], figure=FIG + 'paper-q7b')
# (c): five asks under (18): DEFINE (3), CALCULATE (3), EXPLAIN (3), WHAT (3),
# CALCULATE (6). Two cards, the first three asks and the last two.
_c7 = P.ask(k('7', 'c'))
Q7C_PH, Q7C_NITRIC = cut(_c7, 'What concentration of nitric')
assert Q7C_PH.startswith('Define pH.') and Q7C_PH.endswith('is a weak acid.') and \
    Q7C_NITRIC.endswith('both of these acidic solutions.'), _c7
for _a, _b in (('H₃O + ion', 'H₃O⁺ ion'), ('OH – ion', 'OH⁻ ion')):
    if _a in Q7C_PH:
        Q7C_PH = P.rearranged(Q7C_PH, _a, _b)
    if _a in Q7C_NITRIC:
        Q7C_NITRIC = P.rearranged(Q7C_NITRIC, _a, _b)
assert 'H₃O +' not in Q7C_PH + Q7C_NITRIC and 'OH –' not in Q7C_NITRIC, (Q7C_PH, Q7C_NITRIC)
_q7c = P.items(k('7', 'c'))
assert [it.cell for it in _q7c] == ['[3]'] * 5 + ['[6]'] + ['[3]'] * 4, _q7c
_sq = traced('[Square brackets essential.][Mathematical definition expressed in words is acceptable.]')
_inv = display(_q7c[2].text)
assert _inv == '[H₃O⁺] = inverse log₁₀(– 2) = 0.01 M', _inv
C.add([k('7', 'c')], 'chem-3-4', 'ph-and-the-hydronium-ion-in-nitrous-acid', [
    lift('r-1', _q7c[0].text, 3, 'DEFINE. The scheme adds: ' + _sq),
    lift('r-2', _inv, 3, 'CALCULATE: the scheme gives the answer, 0.01 M, priced (3), and works it so.'),
    lift('r-3', _q7c[3].text, 3, 'EXPLAIN.')],
    qtext=Q7C_PH, cid='q7-c-ph', ref_suffix='pH and the H₃O⁺ ion')
_oh = [display(_q7c[i].text) for i in (6, 7, 8, 9)]
assert _oh[0] == '[H₃O⁺][OH¯] = 1 × 10⁻¹⁴' and _oh[2] == 'pH + pOH = 14 / pOH = 12', _oh
_oh = [x.replace('OH¯', 'OH⁻') for x in _oh]
C.add([k('7', 'c')], 'chem-3-4', 'nitric-acid-and-the-hydroxide-ion', [
    lift('r-1', _q7c[4].text, 3, 'WHAT.'),
    menu_row('r-2', [_oh[0], _oh[2]], 1, 'CALCULATE: the scheme gives the answer, 1 × 10⁻¹² M, priced (6), then two '
             'routes of two steps (3) each, the second under the first; the first step of either, (3).',
             per=3, total=3),
    menu_row('r-3', [_oh[1], _oh[3]], 1, 'And the second step of that same route, (3).', per=3, total=3)],
    total=9, qtext=Q7C_NITRIC, stem=Q7C_PH, cid='q7-c-hydroxide', ref_suffix='nitric acid and the hydroxide ion')
# (d): three points priced (6 + 2 x 3), the second wrapped onto a line of its
# own (scheme page 16, y 616-628), which the reader takes for a point.
_q7d = P.items(k('7', 'd'))
_bp = [display(x) for x in _q7d[0].points()]
assert [it.cell for it in _q7d] == ['[6 + 2 × 3]'] and len(_bp) == 4 and _bp[2].startswith('(carefully, slowly)'), _bp
C.add([k('7', 'd')], 'chem-u2', 'brown-ring-test-for-nitrate', [
    lift('r-1', _bp[0], None), lift('r-2', _bp[1] + ' ' + _bp[2], None),
    lift('r-3', _bp[3], None, 'The scheme adds: ' + ' '.join(_q7d[0].asides))],
    kind='orderedSplit', notation='[6 + 2 × 3]', total=12, notes=SPLIT.format('[6 + 2 × 3]'),
    qtext=P.rearranged(P.ask(k('7', 'd')), '(NO₃ –)', '(NO₃⁻)'))
C.fixed([k('7', 'e')], 'chem-4-3', 'nitrates-and-dissolved-oxygen')

# ── Q8 Ethyne, ethene and ethane ─────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
# (a): GIVE and DRAW priced together (3 + 2); the structure is drawn in a box of
# three forms (page 17, y 109-158). The formulae of A, B and C are the paper's
# print, the card's question.
_q8a = P.items(k('8', 'a'))
assert [it.cell for it in _q8a] == ['[3 + 2]'], _q8a
C.add([k('8', 'a')], 'chem-2-4', 'ethene-named-and-drawn', [
    lift('r-1', 'ethene', None, 'GIVE.'),
    lift('r-2', 'CH₂=CH₂ / H₂C=CH₂', None, 'DRAW: or the structure in full, as the scheme draws it, shown with the '
         'answer. It adds: ' + ' '.join(_q8a[0].asides))],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), figure=S + 'q8a')
print_question('paper-q8a-print')
# (b): four points (4 x 3) beside the scheme's labelled apparatus (page 17).
assert cells(k('8', 'b')) == ['[4 × 3]'], cells(k('8', 'b'))
C.fixed([k('8', 'b')], 'chem-u2', 'preparing-and-collecting-ethyne', figure=S + 'q8b',
        row_notes={0: 'The scheme\'s labelled diagram is shown with the answer.'})
print_question('paper-q8b-print')
_q8c = P.items(k('8', 'c'))
_t = [display(x) for x in _q8c[0].points()]
assert [it.cell for it in _q8c] == ['[3 × 3]'] and len(_t) == 4 and _t[3].startswith('[The reagent'), _t
C.add([k('8', 'c')], 'chem-4-2', 'telling-ethene-from-ethane', [
    lift('r-1', _t[0].replace('(KMnO 4/H⁺)', '(KMnO₄/H⁺)').replace('(MnO₄¯/H⁺ )', '(MnO₄⁻/H⁺)'), 3,
         'The scheme prices these points (3 × 3), one each.'),
    lift('r-2', _t[1], 3),
    lift('r-3', _t[2], 3, 'The scheme adds: ' + _t[3])], figure=Q8)
C.fixed([k('8', 'd', 'i')], 'chem-4-2', 'free-radical-substitution', figure=Q8)
# (d)(ii): five steps (3) each. Two boxes in the scheme's left margin (page 18,
# x 21-113) are examiner's notes to the whole of (d), quoted on the rows.
_q8d2 = P.items(k('8', 'd', 'ii'))
assert [it.cell for it in _q8d2] == ['[3]'] * 5, _q8d2
_m1, _m2 = raw(18, 94, 271, 0, 113), raw(18, 307, 444, 0, 113)
assert _m1.startswith('Where a candidate refers') and _m1.endswith('only once in (d).') and \
    _m2.startswith('Where a radical') and _m2.endswith('applies each time.'), (_m1, _m2)
_s = [norm(display(it.text)) for it in _q8d2]


def of(i, *pieces):
    """The pieces, each asserted to be in the reader's text of step i: a row
    lifted in the forms the gate finds, from the step the cell prices."""
    for x in pieces:
        assert norm(x) in _s[i], (i, x, _s[i])
    return pieces


# The scheme prints each step in words, then "/" and its equation(s); the text
# layer splits some of them where a superscript or the margin notes fall, so
# each step is a row of the forms the gate finds, one of them to claim.
_ini = of(0, 'initiation: homolysis (splitting, fission) of chlorine molecule (Cl₂) into free radicals (atoms, Cl●)',
          'by ultraviolet (uv) light')
_p1 = of(1, 'propagation (1):', 'Cl● + C₂H₆ → HCl + C₂H₅● / Cl + C₂H₆ → HCl + C₂H₅●')
_p1w = 'chlorine radical (atom, Cl●, Cl) reacts with ethane molecule (C₂H₆) giving hydrogen chloride (HCl) and an ' \
       'ethyl radical (C₂H₅●)'
assert norm(_p1w) in _s[1], _s[1]
_p2 = of(2, 'propagation (2): ethyl radical (C₂H₅●) reacts with chlorine molecule (Cl₂) giving monochloroethane '
            '(C₂H₅Cl) and a chlorine radical (atom, Cl●, Cl)', 'C₂H₅● + Cl₂ → C₂H₅Cl + Cl● / C₂H₅● + Cl₂ → C₂H₅Cl + Cl')
_term = of(4, 'termination: combination of remaining radicals to form molecules (chlorine, chloroethane, butane)',
           '2Cl● → Cl₂ / 2Cl → Cl₂', 'Cl● + C₂H₅● → C₂H₅Cl / Cl + C₂H₅● → C₂H₅Cl', '2C₂H₅● → C₄H₁₀')
_where = traced('[Where C₂H₅ used instead of C₂H₅● deduct 3 marks but only once in (d).]')
assert _s[2].startswith(norm(_where)), _s[2]          # printed under (1)'s cell, read with (2)
C.add([k('8', 'd', 'ii')], 'chem-4-2', 'mechanism-of-chlorinating-ethane', [
    lift('r-1', _ini[0], 3, 'The scheme goes on "' + _ini[1] + '", and accepts the equation, "uv" over its arrow, as '
         'it prints it, shown with the answer. Beside (d) the scheme notes: "' + _m1 + '"'),
    lift('r-2', _p1[1], 3, 'propagation (1): the scheme gives this step in words, "' + _p1w + '", or as these '
         'equations. It adds: ' + ' '.join(_q8d2[1].asides) + ' ' + _where),
    menu_row('r-3', list(_p2), 1, 'One of these, (3): the step in words or as its equations.', per=3, total=3),
    lift('r-4', _q8d2[3].text, 3, 'The scheme adds: ' + ' '.join(_q8d2[3].asides)),
    menu_row('r-5', list(_term), 1, 'One of these, (3): the step in words or one of its equations. Beside (d) the '
             'scheme notes: "' + _m2 + '"', per=3, total=3)], total=15, figure=S + 'q8d-ii')
print_question('paper-q8d-ii-print')
C.fixed([k('8', 'd', 'iii')], 'chem-4-2', 'butane-as-evidence-for-free-radicals', figure=Q8)

# ── Q9 The decomposition of nitrogen monoxide ────────────────────────────────
Q9 = FIG + 'paper-q9'
assert [(it.cell, display(it.text)) for it in P.items(k('9', 'a'))] == [('[5]', '[NO]²')], P.items(k('9', 'a'))
C.add([k('9', 'a')], 'chem-3-3', 'kc-for-the-decomposition-of-no', [
    lift('r-1', '[N₂][O₂] ÷ [NO]²', 5, FRACTION.format('[N₂][O₂]', '[NO]²'))], figure=Q9)
# (b): the answer (12); two routes side by side, four steps (3) each, set as
# fractions and a quadratic the text layer cannot order.
_q9b = P.items(k('9', 'b'))
assert _q9b[0].cell == '[12]' and display(_q9b[0].text) == '0.9 mol' and len(_q9b[-1].asides) == 2, _q9b
C.answer_only([k('9', 'b')], 'chem-3-3', 'moles-of-nitrogen-at-equilibrium', S + 'q9b',
              notes='The scheme sets out two routes side by side, each four steps (3) each: the moles at equilibrium, '
                    'Kc in terms of x, then x by a square root or by a quadratic equation.')
shown('The scheme prices each of its two routes in four steps, (3) each, and adds: ' + ' '.join(_q9b[-1].asides))
print_question('paper-q9b-print')
# (c): STATE (2 x 3) under (6); WHAT (i) // (ii) (2 x 3) and JUSTIFY (i) // (ii)
# (2 x 3) under (12), the paper setting (i) and (ii) inside one sentence.
Q9C_STATE, Q9C_WHAT = cut(P.ask(k('9', 'c')), 'What effect')
assert Q9C_STATE == 'State Le Châtelier’s principle.' and Q9C_WHAT.endswith('Justify your answer in each case.'), \
    Q9C_WHAT
C.fixed([k('9', 'c')], 'chem-3-3', 'le-chateliers-principle', qtext=Q9C_STATE, figure=Q9)
_q9c1, _q9c2 = P.items(k('9', 'c', 'i')), P.items(k('9', 'c', 'ii'))
_w1 = [display(x) for x in _q9c1[0].points()]
assert [it.cell for it in _q9c1] == [None] and len(_w1) == 2 and [it.cell for it in _q9c2] == ['[2 × 3]'] * 2, \
    (_q9c1, _q9c2)
C.add([k('9', 'c', 'i'), k('9', 'c', 'ii')], 'chem-3-3', 'temperature-pressure-and-kc', [
    lift('r-1', _w1[0], 3, 'WHAT, for (i). The scheme prices WHAT (2 × 3), one for each part.'),
    lift('r-2', _q9c2[0].text, 3, 'WHAT, for (ii). The scheme adds: ' + ' '.join(_q9c2[0].asides)),
    lift('r-3', _w1[1], 3, 'JUSTIFY, for (i). The scheme prices JUSTIFY (2 × 3), one for each part.'),
    lift('r-4', _q9c2[1].text, 3, 'JUSTIFY, for (ii). The scheme adds: ' + ' '.join(_q9c2[1].asides))],
    qtext=Q9C_WHAT, stem=C.context(k('9', 'c')), figure=Q9)
# (d): NAME any two (2 x 3); WHAT (3), its two notes printed under it; GIVE (3); NAME (3).
_q9d = P.items(k('9', 'd'))
assert [it.cell for it in _q9d] == ['[2 × 3]', '[3]', '[3]', '[3]'] and '[any two]' in _q9d[0].asides, _q9d
_whatn = _q9d[2].points()[0]
assert _whatn == '[‘Hetero-catalysis’ unacceptable.][Accept surface absorption.]', _whatn
_give = display(_q9d[2].points()[1])
C.add([k('9', 'd')], 'chem-3-2', 'catalytic-converters', [
    menu_row('r-1', _q9d[0].options(), 2, 'NAME: any two of these, (3) each: "' + raw(20, 47, 64, 440) + '". The scheme '
             'adds: [Symbols unacceptable.]', per=3, total=6),
    lift('r-2', _q9d[1].text, 3, 'WHAT. The scheme adds: ' + _whatn),
    lift('r-3', _give, 3, 'GIVE. The scheme adds: ' + ' '.join(_q9d[2].asides)),
    lift('r-4', _q9d[3].text, 3, 'NAME. The scheme adds: ' + ' '.join(_q9d[3].asides))], total=15, figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q10A = FIG + 'paper-q10a'
C.fixed([k('10', 'a', 'i')], 'chem-4-2', 'a-use-of-ethanoic-acid', figure=Q10A)
# (ii): the scheme draws ethanal (page 21, y 128-182) and prices it (2 x 3).
C.drawn([k('10', 'a', 'ii')], 'chem-4-2', 'the-structure-of-ethanal', S + 'q10a-ii')
print_question('paper-q10a-ii-print')
# (iii): DRAW (6), the ester's formula beside its drawing; IDENTIFY (3), the
# carbonyl carbon ringed on a second drawing.
_q10a3 = P.items(k('10', 'a', 'iii'))
assert [it.cell for it in _q10a3] == ['[6]', '[3]', None], _q10a3
_planar = raw(21, 334, 368, 160, 530)
assert _planar.startswith('carbonyl carbon / [May be indicated by arrow,'), _planar
C.add([k('10', 'a', 'iii')], 'chem-4-2', 'ethyl-ethanoate-and-its-planar-carbon', [
    lift('r-1', 'CH₃COOC₂H₅', 6, 'DRAW: or the structure, as the scheme draws it, shown with the answer. It adds: '
         + ' '.join(_q10a3[0].asides)),
    lift('r-2', 'carbonyl carbon', 3, 'IDENTIFY. The scheme adds: [May be indicated by arrow, colouring, asterisk, '
         'etc.] ' + ' '.join(_q10a3[2].asides))], figure=S + 'q10a-iii')
print_question('paper-q10a-iii-print')
# (iv): two points (2 x 3), or after "or" one answer (6): two rows, each its
# point or that answer, which the student claims twice.
_q10a4 = P.items(k('10', 'a', 'iv'))
assert [it.cell for it in _q10a4] == ['[2 × 3]', '[6]', None] and _q10a4[2].text == '4', _q10a4
_h = [display(x) for x in _q10a4[0].options()]
_lia = display(_q10a4[1].text)
assert len(_h) == 2 and _lia.endswith('(sodium tetrahydroborate, NaBH )'), (_h, _lia)
_lia = _lia.replace('NaBH )', 'NaBH₄)')
C.add([k('10', 'a', 'iv')], 'chem-4-2', 'reducing-ethanal-to-ethanol', [
    menu_row('r-1', [_h[0], _lia], 1, 'The first point, (3), or after "or" the answer the scheme prices (6) on its own: '
             'claim it here and again below.', per=3, total=3),
    menu_row('r-2', [_h[1], _lia], 1, 'The second point, (3), or that answer again.', per=3, total=3)],
    total=6, figure=Q10A)
# (b): DEFINE (i) (3) and (ii) (2 x 3) under (9), the paper setting (i) and (ii)
# inside one sentence; WHAT (2 x 3); LIST (3); CALCULATE (7), each under its own mark.
Q10B = P.ask(k('10', 'b'))
Q10B_DEF, _r = cut(Q10B, 'Three of the five')
Q10B_THREE, _r = cut(_r, 'What are the two')
Q10B_WHAT, _r = cut(_r, 'List all five')
Q10B_LIST, _r = cut(_r, 'A sample of')
Q10B_GA, Q10B_CALC = cut(_r, 'Calculate the relative')
assert Q10B_DEF == 'Define (i) mass number, (ii) relative atomic mass.' and Q10B_CALC.endswith('from this information.'), \
    Q10B
_q10b1, _q10b2 = P.items(k('10', 'b', 'i')), P.items(k('10', 'b', 'ii'))
assert [it.cell for it in _q10b1] == ['[3]'] and [it.cell for it in _q10b2] == ['[2 × 3]', '[2 × 3]', '[3]', '[7]',
                                                                               '[2]', '[2]', '[3]'], _q10b2
C.add([k('10', 'b', 'i')], 'chem-1-2', 'mass-number', [lift('r-1', _q10b1[0].text, 3, 'For (i).')],
      qtext=Q10B_DEF, stem='')
_ram = [display(x) for x in _q10b2[0].points()]
assert _ram[1] == 'relative to 12 of mass of carbon–12 atom 1', _ram
C.add([k('10', 'b', 'ii')], 'chem-1-2', 'relative-atomic-mass', [
    lift('r-1', _ram[0], 3, 'For (ii). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'relative to 1 ÷ 12 of mass of carbon–12 atom', 3, FRACTION.format('1', '12') + ' The scheme adds: '
         + ' '.join(_q10b2[0].asides))],
    qtext=Q10B_DEF, stem='')
C.add([k('10', 'b')], 'chem-1-2', 'ionisation-and-separation-in-the-mass-spectrometer', [
    lift('r-1', _q10b2[1].options()[0], 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _q10b2[1].options()[1], 3, 'The scheme adds: ' + ' '.join(_q10b2[1].asides))],
    qtext=Q10B_WHAT, stem=Q10B_THREE, cid='q10-b-processes', ref_suffix='after (ii), the two other processes')
C.add([k('10', 'b')], 'chem-1-2', 'the-order-of-processes-in-mass-spectrometry', [
    lift('r-1', _q10b2[2].text, 3, 'The scheme adds: ' + ' '.join(_q10b2[2].asides))],
    qtext=Q10B_LIST, stem=Q10B_THREE, cid='q10-b-order', ref_suffix='after (ii), the five processes in order')
_ar = display(_q10b2[6].text)
assert _ar == '100 atoms = 6979.8 Ar = 69.798 (69.8)', _ar
C.add([k('10', 'b')], 'chem-1-4', 'relative-atomic-mass-of-gallium', [
    lift('r-1', _q10b2[4].text, 2),
    lift('r-2', _q10b2[5].text, 2),
    lift('r-3', _ar, 3, 'The scheme adds: ' + ' '.join(_q10b2[6].asides))],
    qtext=Q10B_CALC, stem=Q10B_GA, cid='q10-b-gallium', ref_suffix='after (ii), relative atomic mass of gallium',
    notes='The scheme gives the answer, 69.798 (69.8), priced (7), then the working in three steps, (2), (2) and (3).')
shown('The scheme gives the answer as "69.798 (69.8)" (7).')
# (c): DEFINE (i) // (ii) (2 x 3) under (6); USE (iii) (2 x 3) and (iv) (2 x 3)
# under (12), oxidation numbers printed "+5 (5) → +2 (2)", a bracketed number
# that the cue reader takes for a cell (page 22, y 428-490); BALANCE (7).
Q10C = P.ask(k('10', 'c'))
Q10C_DEF, _r = cut(Q10C, 'Use oxidation numbers')
Q10C_USE, Q10C_BAL = cut(_r, 'Hence, or otherwise')
assert Q10C_DEF == 'Define oxidation in terms of (i) electron transfer, (ii) change in oxidation number.' and \
    Q10C_BAL == 'Hence, or otherwise, balance the equation.', Q10C
Q10C_USE = P.rearranged(Q10C_USE, 'NO₃ – →', 'NO₃⁻ →')
assert Q10C_USE.endswith('in the following reaction. Cd + H⁺ + NO₃⁻ → Cd²⁺ + NO + H₂O'), Q10C_USE
_q10c = [P.items(k('10', 'c', r)) for r in ('i', 'ii', 'iii', 'iv')]
assert [[it.cell for it in its] for its in _q10c] == [[None], ['[2 × 3]'], ['[5]', '[2]'], ['[2 × 3]', '[7]', None]], \
    _q10c
C.add([k('10', 'c', 'i'), k('10', 'c', 'ii')], 'chem-3-5', 'oxidation-defined-two-ways', [
    lift('r-1', 'loss of electrons', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _q10c[1][0].text, 3, 'For (ii).')], qtext=Q10C_DEF, stem='')
_ox = raw(22, 426, 444, 130, 400)
_red = raw(22, 474, 492, 130, 400)
assert _ox == '(iii) oxidising agent: NO₃ ¯ // +5 (5) → +2 (2)' and _red == '(iv) reducing agent: Cd // 0 → +2 (2)', \
    (_ox, _red)
_use = raw(22, 426, 444, 480)
assert _use == '(2 × 3)', _use
C.add([k('10', 'c', 'iii')], 'chem-3-5', 'the-oxidising-agent', [
    lift('r-1', 'oxidising agent: NO₃⁻', 3, 'For (iii). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '+5 (5) → +2 (2)', 3, 'The scheme adds: ' + ' '.join(_q10c[2][1].asides))],
    qtext=Q10C_USE, stem=Q10C_DEF)
C.add([k('10', 'c', 'iv')], 'chem-3-5', 'the-reducing-agent', [
    lift('r-1', 'reducing agent: Cd', 3, 'For (iv). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '0 → +2 (2)', 3)],
    qtext=Q10C_USE, stem=Q10C_DEF)
_bal = display(_q10c[3][1].text)
assert _bal == '3Cd + 8H⁺ + 2NO₃¯ → 3Cd²⁺ + 2NO + 4H₂ O', _bal
C.add([k('10', 'c')], 'chem-3-5', 'balancing-a-redox-equation', [
    lift('r-1', '3Cd + 8H⁺ + 2NO₃⁻ → 3Cd²⁺ + 2NO + 4H₂O', 7, 'The scheme adds: ' + ' '.join(_q10c[3][1].asides) + ' '
         + display(_q10c[3][2].text) + ' ' + ' '.join(_q10c[3][2].asides))],
    qtext=Q10C_BAL, stem=Q10C_USE, cid='q10-c-balancing', ref_suffix='after (iv), balancing')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): five asks, each under its printed mark, (6), (6), (3), (6), (4); eight
# rows outrun a card, so each is a card, cited with what it holds.
Q11A = P.ask(k('11', 'a'))
Q11A_DEF, _r = cut(Q11A, 'Ammonia (NH₃)')
Q11A_SMALL, _r = cut(_r, 'Account for')
Q11A_ACC, _r = cut(_r, 'Use electronegativity')
Q11A_USE, _r = cut(_r, 'Which of the two')
Q11A_HB, Q11A_GIVE = cut(_r, 'Give the reason')
assert Q11A_DEF == 'Define electronegativity.' and Q11A_SMALL.endswith('the central atom.') and \
    Q11A_GIVE == 'Give the reason why a molecule with polar bonds can be non-polar.', Q11A
_q11a = P.items(k('11', 'a'))
assert [it.cell for it in _q11a] == ['[2 × 3]', '[2 × 3]', '[3]', '[3]', '[3]', '[4]'], _q11a
_en = [display(x) for x in _q11a[0].points()]
C.add([k('11', 'a')], 'chem-1-3', 'electronegativity', [
    lift('r-1', _en[0], 3, 'The scheme prices these points (2 × 3), one each.'), lift('r-2', _en[1], 3)],
    qtext=Q11A_DEF, stem='', cid='q11-a-electronegativity', ref_suffix='electronegativity defined')
_acc = [display(x) for x in _q11a[1].points()]
C.add([k('11', 'a')], 'chem-2-2', 'bond-angles-of-ammonia-and-silane', [
    lift('r-1', _acc[0], 3, 'The scheme prices these points (2 × 3), one each.'), lift('r-2', _acc[1], 3)],
    qtext=Q11A_ACC, stem=Q11A_SMALL, cid='q11-a-bond-angles', ref_suffix='bond angles')
C.add([k('11', 'a')], 'chem-2-2', 'the-more-polar-bond', [lift('r-1', _q11a[2].text, 3)],
      qtext=Q11A_USE, stem=Q11A_SMALL, cid='q11-a-polar-bond', ref_suffix='the more polar bond')
_link = _q11a[5].points()[0]
assert _link == '[Both parts to be linked].', _link
C.add([k('11', 'a')], 'chem-2-2', 'hydrogen-bonding-in-ammonia', [
    lift('r-1', _q11a[3].text.rstrip('/ '), 3, 'WHICH.'),
    lift('r-2', _q11a[4].text, 3, 'JUSTIFY. The scheme adds: ' + _link)],
    qtext=Q11A_HB, stem=Q11A_SMALL, cid='q11-a-hydrogen-bonding', ref_suffix='hydrogen bonding')
C.add([k('11', 'a')], 'chem-2-2', 'polar-bonds-in-a-non-polar-molecule', [
    lift('r-1', _q11a[5].points()[1], 4, 'The scheme adds: ' + ' '.join(_q11a[5].asides))],
    qtext=Q11A_GIVE, stem='', cid='q11-a-non-polar', ref_suffix='polar bonds, non-polar molecule')
# (b): the answer to each roman, then its working, steps (3) each ((2) in (iv)).
_q11b1 = P.items(k('11', 'b', 'i'))
assert [it.cell for it in _q11b1] == ['[6]', '[3]', '[3]'] and display(_q11b1[0].text) == '0.05 mol', _q11b1
C.add([k('11', 'b', 'i')], 'chem-1-4', 'moles-of-ammonium-dichromate', [
    lift('r-1', 'Mr = 252', 3),
    lift('r-2', '0.05 mol', 3, 'The scheme prints 12.6 over 252 as a fraction, "= 0.05 mol".')],
    notes='The scheme gives the answer, 0.05 mol, priced (6), then two steps (3) each.')
C.route([k('11', 'b', 'ii')], 'chem-1-4', 'mass-of-chromium-iii-oxide-formed')
C.route([k('11', 'b', 'iii')], 'chem-1-4', 'volume-of-nitrogen-evolved')
_q11b4 = P.items(k('11', 'b', 'iv'))
assert [it.cell for it in _q11b4] == ['[4]', '[2]', '[2]', '[3]', '[3]'], _q11b4
C.add([k('11', 'b', 'iv')], 'chem-1-4', 'molecules-and-atoms-in-the-water-produced', [
    lift('r-1', _q11b4[1].text, 2, 'NUMBER: the scheme gives the answer, 1.2 × 10²³, priced (4), then two steps (2) each.'),
    lift('r-2', _q11b4[2].text, 2),
    lift('r-3', _q11b4[4].text, 3, 'HOW MANY: the scheme gives the answer, 3.6 × 10²³, priced (3), and works it so.')])
# (c)A: acid rain.
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'why-rainwater-is-always-acidic')
C.menu([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'damage-done-by-acid-rain', note='"' + raw(24, 98, 115, 440) + '".')
# (iii): SHOW (3), then two equations (2 x 3) or after "or" one (6): two rows,
# each its equation or that one, which the student claims twice.
_q11a3 = P.items(ka('11', 'c', 'iii', 'A'))
assert [it.cell for it in _q11a3] == ['[3]', '[2 × 3]', '[6]', None], _q11a3
_two = [display(x) for x in _q11a3[1].points()]
assert _two[0] == 'and' and len(_two) == 3, _two
_two = [_two[1], _two[2].replace('SO 3 + H₂O', 'SO₃ + H₂O')]
_one = display(_q11a3[2].text)
C.add([ka('11', 'c', 'iii', 'A')], 'chem-4-3', 'sulfur-dioxide-to-acid-rain', [
    lift('r-1', _q11a3[0].text, 3, 'SHOW.'),
    menu_row('r-2', [_two[0], _one], 1, '"and" the first of two equations, (3), or after "or" the answer the scheme '
             'prices (6) on its own: claim it here and again below.', per=3, total=3),
    menu_row('r-3', [_two[1], _one], 1, 'The second equation, (3), or that answer again. The scheme adds: '
             + display(_q11a3[3].text), per=3, total=3)], total=9)
C.fixed([ka('11', 'c', 'iv', 'A')], 'chem-4-3', 'human-sources-of-sulfur-dioxide')
C.fixed([ka('11', 'c', 'v', 'A')], 'chem-4-3', 'why-irelands-air-is-clean')
# (c)B: crystals. (i) two points priced (4 + 3); the paper underlines "crystals".
C.ordered([ka('11', 'c', 'i', 'B')], 'chem-2-1', 'what-a-crystal-is')
print_question('paper-q11c-b-i-print')
Q11CB = FIG + 'paper-q11c-b'
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-2-1', 'bonding-in-graphite', figure=Q11CB)
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-2-1', 'the-hardness-of-diamond')
C.fixed([ka('11', 'c', 'iv', 'B')], 'chem-2-1', 'why-metals-conduct-electricity', skip=('Blank Page',))


# A script run the text layer sets apart from the bracket that closes it
# ("(FeSO₄ )", "[H⁺ ]", "(from 4th to 5th )", "(Mr )", the r a subscript), from
# its radical's dot ("C₂H₅ ●") or from its number ("2 nd") is shown as the page
# sets it; the gate reads both alike (spaces fold away), checked again here.
# "(measure of )" is the scheme's own spacing.
_SPACED = [(re.compile(r'([₀-₉⁰-⁹¹²³⁺⁻]|\dth|\bMr) ([)\]])'), r'\1\2'), (re.compile(r'([₀-₉]) ●'), r'\1●'),
           (re.compile(r'(\d) (st|nd|th)\b'), r'\1\2')]


def _closed(t):
    for rx, rep in _SPACED:
        t = rx.sub(rep, t)
    if not P.traceable(t):
        raise Refused(f'"{t}" is not in the 2014 hl scheme')
    return t


for _c in C.cards:
    for _r in _c['rows']:
        if not _r.get('ask'):
            _r['verbatim'] = _closed(_r['verbatim'])
        if _r.get('group'):
            _r['group']['options'] = [_closed(o) for o in _r['group']['options']]


# A note quoted from the scheme in the reader's script notation ("E_(n>2)",
# "K_(c)") is shown as the page sets it.
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'], _r


# ── review ───────────────────────────────────────────────────────────────────
# Q5(a) prints its first mark, (14), at the end of a line of its own text
# ("... energy level and atomic orbital. (14)", paper page 4, y 488), which the
# reader takes off the line rather than recording where it fell.
INLINE = {('5', 'a'): 14}


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
    for key in sorted(set(got) | set(marks), key=lambda kv: (int(kv[0]), kv[1] or '')):
        if key == ('4', None):
            continue
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
