#!/usr/bin/env python3
"""2018 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2018_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2018_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2018_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2018 ol

No 2018 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The paper sets some romans inside one sentence -- Q9(a) "Define (i) oxidation,
(ii) reduction, ...", Q10(b) "Define (i) atomic number, (ii) mass number, (iii)
isotopes.", Q11(c)A "... in terms of (i) hardness, (ii) lustre?" -- and the
scheme prices them: Q9(a) with one cell "(2 × 6)", Q10(b) with a cell each,
Q11(c)A with one cell "(6 + 3)". The cards follow the cells and take the
sentence as their question. Q11(a) and Q11(c)A set asks unnumbered after their
last roman, each priced by a cell of its own: one card each, cited "after
(ii)". The paper underlines the term Q2(d) and Q11(b)(i) ask about and prints
Q10(a) and Q11(a)'s statement of Boyle's law with numbered blanks, which no
text layer carries: those take the paper's own print as their question, as do
Q2(f), Q3(c) and Q3(d)(i), whose answers are the scheme's. Q11(c)B is answered
for the one industry the candidate studied: the scheme gives each industry's
answer, and the card offers them as a menu to claim from. Q4(k) and Q11(c) offer
whole alternative parts A and B.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import routed  # noqa: E402
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN, point)

P = Printed(2018, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2018-OL-'
S = FIG + 'scheme-'
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


def cells(key):
    return [it.cell for it in P.items(key)]


def traced(text):
    """A string quoted from the scheme in a note, checked against the scheme."""
    if not P.traceable(text):
        raise Refused(f'"{text}" is not in the 2018 ol scheme')
    return text


def cut(text, start=None, end=None):
    """The part of `text` from `start` (inclusive) up to `end` (exclusive), each
    asserted to be in it: a sentence lifted out of the paper's print."""
    a = text.index(start) if start else 0
    b = text.index(end, a) if end else len(text)
    return text[a:b].strip()


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Preparing ethene ──────────────────────────────────────────────────────
Q1 = FIG + 'paper-q1'
C.fixed([k('1', 'a')], 'chem-u2', 'catalyst-in-preparing-ethene', figure=Q1)
C.ordered([k('1', 'b', 'i'), k('1', 'b', 'ii')], 'chem-u2', 'collecting-ethene-and-discarding-the-first-tubes',
          figure=Q1)
C.ordered([k('1', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-u2', 'suck-back', figure=Q1)
C.fixed([k('1', 'd', 'i')], 'chem-2-4', 'reagent-to-test-for-unsaturation', figure=Q1)
C.fixed([k('1', 'd', 'ii')], 'chem-2-4', 'colour-change-in-the-unsaturation-test', figure=Q1)
C.fixed([k('1', 'e', 'i')], 'chem-2-4', 'combustion-test-on-ethene', figure=Q1)
C.fixed([k('1', 'e', 'ii')], 'chem-2-4', 'flame-of-burning-ethene', figure=Q1)
# (iii): the cue "COPY, / COMPLETE, / BALANCE:" leaves its first two lines on the
# equation's row; the cell is "PRODUCTS: (3), BALANCING: (3)".
_q1e3 = P.items(k('1', 'e', 'iii'))
assert [it.cell for it in _q1e3] == ['[3 + 3]'], _q1e3
_t = _q1e3[0].text
assert _t.startswith('COPY, ') and _t.endswith(' COMPLETE,'), _t
C.fixed([k('1', 'e', 'iii')], 'chem-3-1', 'combustion-of-ethene', figure=Q1,
        fixes={_t: _t[len('COPY, '):-len(' COMPLETE,')]})

# ── Q2 A standard solution and a titration ───────────────────────────────────
Q2 = FIG + 'paper-q2'
C.ordered([k('2', 'a')], 'chem-4-1', 'naming-titration-glassware', figure=Q2)
C.ordered([k('2', 'b', r) for r in ('i', 'ii', 'iii')], 'chem-4-1', 'which-glassware-for-each-task',
          figure=Q2)
C.fixed([k('2', 'c')], 'chem-4-1', 'glassware-rinsed-with-the-solution-it-holds', figure=Q2)
C.fixed([k('2', 'd')], 'chem-4-1', 'definition-of-a-standard-solution')
print_question('paper-q2d-print')
C.fixed([k('2', 'e', 'i')], 'chem-4-1', 'indicator-for-a-carbonate-titration', figure=Q2)
# (e)(ii): the aside "[Marks may be given ... Allow (3) for correct colours
# reversed ... (9) marks only available ...]" runs over three lines; the reader
# takes its "(3)" for a cell. It is one aside, on the two colours priced (2 × 3).
_q2e = P.items(k('2', 'e', 'ii'))
assert [it.cell for it in _q2e] == ['[2 × 3]', '[3]', None], _q2e
_pp = _q2e[0].points()
assert len(_pp) == 2, _pp
_q2e_aside = traced(_q2e[1].text + ' (3) ' + _q2e[2].text)
C.add([k('2', 'e', 'ii')], 'chem-4-1', 'colour-change-of-methyl-orange-at-end-point', [
    C.lifted('r-1', _pp[0], 3, 'The scheme prices these points (2 × 3), one each.'),
    C.lifted('r-2', _pp[1], 3, 'The scheme adds: ' + _q2e_aside)], figure=Q2)
# (f): the average titre (3), then the answer (9) and the working that earns it,
# boxed two ways with stacked fractions the text layer cannot order.
_q2f = P.items(k('2', 'f'))
assert [it.cell for it in _q2f] == ['[3]', '[9]', '[3]', '[3]', '[3]', '[3]', '[9]', None], _q2f
_slip = traced(_q2f[6].asides[0])
C.add([k('2', 'f')], 'chem-4-1', 'concentration-of-hydrochloric-acid', [
    C.lifted('r-1', _q2f[0].text, 3),
    C.lifted('r-2', _q2f[1].text, 9, 'The scheme sets out the working that earns it in two boxed routes, '
             '(3) a step; its own print is shown with the answer. The scheme adds: ' + _slip)],
    figure=S + 'q2f')
print_question('paper-q2f-print')

# ── Q3 The decomposition of hydrogen peroxide ────────────────────────────────
# The equation prints MnO2 over its arrow, which the text layer drops: the
# equation is a picture (paper-q3), and the stems of (c) and (d) leave out the
# sentence that introduces it.
Q3 = FIG + 'paper-q3'
Q3T = FIG + 'paper-q3d-table'
_q3_eq = ' The equation for the reaction is:'


def q3_stem(key):
    ctx = C.context(key)
    assert ctx.count(_q3_eq) == 1, ctx
    return ctx.replace(_q3_eq, '')


C.fixed([k('3', 'a')], 'chem-u2', 'measuring-out-5-cm3-of-solution', figure=Q3)
C.fixed([k('3', 'b')], 'chem-3-2', 'appearance-of-manganese-dioxide', figure=Q3)
# (c): one cell (6 + 3) over (i) and (ii). (ii)'s two answers print either side
# of the cue "& LABEL:" (scheme PDF page 7), so the second rides on the first.
_q3c = [P.items(k('3', 'c', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q3c] == [[None], ['[6 + 3]']], _q3c
_gas = _q3c[1][0].text.split(' / ')
assert len(_gas) == 2, _gas
C.add([k('3', 'c', 'i'), k('3', 'c', 'ii')], 'chem-u2', 'placing-the-catalyst-and-collecting-the-oxygen', [
    C.lifted('r-1', _q3c[0][0].text, None, 'For (i). The scheme adds: ' + ' '.join(_q3c[0][0].asides)),
    C.accepting(C.lifted('r-2', _gas[0], None, 'For (ii). The scheme adds: ' + ' '.join(_q3c[1][0].asides)),
                _gas[1])],
    kind='orderedSplit', notation='[6 + 3]', total=9, figure=S + 'q3c',
    notes=SPLIT.format('[6 + 3]') + ' A, B, X and Y name the scheme\'s own drawings, shown with the answer.',
    stem=q3_stem(k('3', 'c', 'i')))
print_question('paper-q3c-print')
Q3D = q3_stem(k('3', 'd', 'i'))
C.fixed([k('3', 'd', 'i')], 'chem-3-2', 'graph-of-oxygen-volume-against-time', figure=S + 'q3d-i', stem=Q3D)
print_question('paper-q3d-i-print')
C.fixed([k('3', 'd', 'ii')], 'chem-3-2', 'why-the-rate-falls', figure=Q3T, stem=Q3D)
C.fixed([k('3', 'd', 'iii')], 'chem-3-2', 'volume-read-from-the-graph', figure=Q3T, stem=Q3D)
# (iv): the scheme's next page opens "SECTION B", which the reader files under it.
C.ordered([k('3', 'd', 'iv')], 'chem-3-2', 'curve-for-half-the-hydrogen-peroxide', figure=S + 'q3d-iv',
          stem=Q3D, drop=('SECTION B',))

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-3', 'mendeleevs-table-and-the-modern-table', notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-3-2', 'catalysts-in-a-catalytic-converter', notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-3-5', 'gases-from-electrolysing-acidified-water', notes=Q4_NOTE,
        figure=FIG + 'paper-q4c')
assert cells(k('4', 'd')) == ['[3 + 3]'], P.items(k('4', 'd'))
C.fixed([k('4', 'd')], 'chem-1-4', 'equation-for-hydrogen-and-chlorine', notes=Q4_NOTE)
C.route([k('4', 'e')], 'chem-3-4', 'ph-of-sulfuric-acid', notes=Q4_NOTE)
C.fixed([k('4', 'f')], 'chem-3-1', 'combustion-of-methanol-is-exothermic', notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-1-4', 'empirical-formula-of-glucose', notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-4-3', 'primary-sewage-treatment', notes=Q4_NOTE)
# (i): the answer (6), then two boxed routes side by side, (3) a step; the rows
# are the first route, the second in the notes.
_q4i = P.items(k('4', 'i'))
assert [it.cell for it in _q4i] == ['[6]', '[3]', '[3]', '[3]', '[3]'] and _q4i[2].text == '', _q4i
_first = _q4i[1].text.split(' / ')
assert len(_first) == 2, _first
C.add([k('4', 'i')], 'chem-1-4', 'concentration-in-parts-per-million', [
    routed(C.lifted('r-1', _first[0], 3, 'The scheme\'s first route, this step and the next; its second route is the '
                    'last two rows. The examiner marks one route, not a mix.'), 'a'),
    routed(C.lifted('r-2', _q4i[3].text, 3), 'a'),
    routed(C.lifted('r-3', _first[1], 3, 'Or by the scheme\'s second route, this step and the next.'), 'b'),
    routed(C.lifted('r-4', _q4i[4].text, 3), 'b')],
    total=6, notes='The scheme gives the answer, ' + _q4i[0].text + ', priced (6), then the working that earns '
          'it in two boxed routes, step by step; the steps here are its first route. ' + Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-1-2', 'beta-decay', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-1-1', 'buckminsterfullerene', notes=Q4_NOTE,
        figure=FIG + 'paper-q4k-a')
C.fixed([ka('4', 'k', None, 'B')], 'chem-u3', 'why-reaction-vessels-are-made-of-steel', notes=Q4_NOTE)

# ── Q5 Bonding ───────────────────────────────────────────────────────────────
C.fixed([k('5', 'a')], 'chem-1-2', 'why-argon-is-unreactive')
# (b): the scheme draws both molecules, priced (9 + 3), with the faults it
# deducts for in words beside them; the row is the paper's ask, the sentence
# before it the stem.
_q5b = P.items(k('5', 'b'))
assert [(it.cell, it.text) for it in _q5b][0] == ('[9 + 3]', ''), _q5b
_draw = cut(P.ask(k('5', 'b')), 'Draw dot and cross')
C.add([k('5', 'b')], 'chem-2-1', 'dot-and-cross-diagrams-of-fluorine-and-oxygen', [
    C.mark_ask(point('r-1', _draw, 12, 'The scheme answers this part with drawings, priced (9 + 3); its own '
                     'print, with the faults it deducts for, is shown with the answer. The scheme adds: '
                     + ' '.join(_q5b[1].asides)))],
    qtext=_draw, stem=cut(P.ask(k('5', 'b')), None, 'Draw dot and cross'), figure=S + 'q5b')
C.fixed([k('5', 'c')], 'chem-2-1', 'definition-of-electronegativity')
# (d): "Explain your reasoning in each case." is printed once, after (iii); each
# roman's second cell prices the reason, so (i) and (ii) carry the sentence too.
Q5D = FIG + 'paper-q5d'
_explain = cut(P.ask(k('5', 'd', 'iii')), 'Explain your reasoning')
for r, concept in (('i', 'identifying-ionic-bonding-from-properties'),
                   ('ii', 'identifying-polar-covalent-bonding-from-properties'),
                   ('iii', 'identifying-pure-covalent-bonding-from-properties')):
    assert cells(k('5', 'd', r)) == ['[5]', '[2]'], P.items(k('5', 'd', r))
    C.fixed([k('5', 'd', r)], 'chem-2-1', concept, figure=Q5D,
            qtext=None if r == 'iii' else P.ask(k('5', 'd', r)) + ' ' + _explain)
C.fixed([k('5', 'e')], 'chem-2-2', 'shape-of-a-water-molecule')

# ── Q6 Hydrocarbons ──────────────────────────────────────────────────────────
Q6 = FIG + 'paper-q6'
C.fixed([k('6', 'a')], 'chem-2-4', 'hydrocarbons', figure=Q6)
assert cells(k('6', 'b')) == ['[3 × 3]'], P.items(k('6', 'b'))
C.fixed([k('6', 'b')], 'chem-2-4', 'iupac-names-of-three-hydrocarbons', figure=Q6)
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'homologous-series-of-methane-and-ethane', figure=Q6)
C.fixed([k('6', 'c', 'ii')], 'chem-2-4', 'homologous-series-of-ethyne', figure=Q6)
C.ordered([k('6', 'd', r) for r in ('i', 'ii', 'iii')], 'chem-2-4', 'benzene', figure=Q6)
C.fixed([k('6', 'e')], 'chem-2-4', 'ethyne-for-cutting-and-welding', figure=Q6)
C.ordered([k('6', 'f')], 'chem-2-4', 'methane-from-animal-waste', figure=FIG + 'paper-q6f')

# ── Q7 Hard water and water treatment ────────────────────────────────────────
C.fixed([k('7', 'a', 'i')], 'chem-4-3', 'hard-water')
# (ii): the salt's calcium and magnesium forms print either side of the second
# line of the cue "NAME OR / FORMULA:" (scheme PDF page 10).
_q7a2 = P.items(k('7', 'a', 'ii'))
assert [it.cell for it in _q7a2] == ['[3]', '[3]'], _q7a2
_salts = [s.rstrip(' /') for s in _q7a2[1].text.split(' / magnesium hydrogencarbonate')]
assert len(_salts) == 2, _salts
_salts[1] = 'magnesium hydrogencarbonate' + _salts[1]
C.add([k('7', 'a', 'ii')], 'chem-4-3', 'temporary-hardness-and-its-cause', [
    C.lifted('r-1', _q7a2[0].text, 3),
    C.accepting(C.lifted('r-2', _salts[0], 3), _salts[1])])
C.fixed([k('7', 'a', 'iii')], 'chem-4-3', 'a-problem-caused-by-hard-water')
C.fixed([k('7', 'a', 'iv')], 'chem-4-3', 'an-advantage-of-hard-water')
assert cells(k('7', 'b', 'v')) == ['[8 + (2 × 6) + (2 × 3)]'], P.items(k('7', 'b', 'v'))
C.ordered([k('7', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-4-3',
          'treating-a-drinking-water-supply')

# ── Q8 Ethene, ethanol, ethanal and ethanoic acid ────────────────────────────
Q8 = FIG + 'paper-q8'
C.ordered([k('8', 'a')], 'chem-4-2', 'naming-ethene-ethanal-and-ethanoic-acid', figure=Q8)
# (b): the scheme draws the structure and accepts two condensed formulae beside it.
_q8b = P.items(k('8', 'b'))
assert [(it.cell, it.text) for it in _q8b] == [('[6]', ''), (None, '/ CH₃CH₂OH / C₂H₅OH')], _q8b
C.drawn([k('8', 'b')], 'chem-4-2', 'structure-of-ethanol', S + 'q8b',
        notes='Beside its drawing the scheme accepts "' + traced(_q8b[1].text.lstrip('/ ')) + '".')
C.fixed([k('8', 'c')], 'chem-2-2', 'carbon-atoms-in-planar-geometry', figure=Q8)
C.ordered([k('8', 'd', 'i'), k('8', 'd', 'ii')], 'chem-4-2', 'classifying-the-two-conversions', figure=Q8)
# (e): a pair priced (6 + 3), or instead the scheme's second pair after "or".
_q8e = P.items(k('8', 'e'))
assert [it.cell for it in _q8e] == ['[6 + 3]', '[6 + 3]'], _q8e
_pe = _q8e[0].points()
assert len(_pe) == 2, _pe
# Two pairs, the second after "or", priced together (6 + 3): each point accepts its
# counterpart in the other pair (an unpriced card cannot take routes).
_pe2 = [x.strip() for x in _q8e[1].text.split('//')]
assert len(_pe2) == 2, _pe2
C.add([k('8', 'e')], 'chem-4-2', 'fehlings-test-on-ethanal', [
    C.accepting(C.lifted('r-1', _pe[0], None, 'The scheme prices this point and the next together (6 + 3), or '
                         'instead, (6 + 3), the pair after "or". Claim both points from the same pair.'), _pe2[0]),
    C.accepting(C.lifted('r-2', _pe[1], None, 'The scheme adds: ' + ' '.join(_q8e[0].asides)), _pe2[1])],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'), figure=Q8)
C.fixed([k('8', 'f')], 'chem-4-2', 'a-use-of-ethanoic-acid-in-food', figure=Q8)

# ── Q9 Redox, a flame test and the chloride test ─────────────────────────────
# (a): "Define (i) oxidation, (ii) reduction, ..." is one sentence; the scheme
# prices the two definitions "(2 × 6)", one cell: one card, six each.
_q9a = [P.items(k('9', 'a', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q9a] == [[None], ['[2 × 6]']], _q9a
assert _q9a[0][0].text.endswith(' //'), _q9a
C.add([k('9', 'a')], 'chem-3-5', 'oxidation-and-reduction-as-electron-transfer', [
    C.lifted('r-1', _q9a[0][0].text[:-len(' //')], 6,
             'For (i). The scheme prices this point and the next (2 × 6), one each.'),
    C.lifted('r-2', _q9a[1][0].text, 6, 'For (ii).')])
C.fixed([k('9', 'b', 'i')], 'chem-3-5', 'element-oxidised-when-potassium-burns-in-chlorine')
C.fixed([k('9', 'b', 'ii')], 'chem-3-5', 'the-oxidising-agent')
# (c)(i): three methods set out as a table, each in three steps priced (6), (5)
# and (1); the text layer reads the table across its columns, so each cell is
# read from the lines inside its column and row (scheme PDF page 14), Method 1
# as the rows and the others in the notes, and the scheme's own print of the
# table is the answer picture.
_q9c = P.items(k('9', 'c', 'i'))
assert [it.cell for it in _q9c] == ['[6 + 5 + 1]', '[6]', '[5]', '[1]', None], _q9c
_lines14 = [l for l in read_lines(P.scheme_path) if l.page == 14]


def _cell(x0, x1, y0, y1):
    got = sorted((l for l in _lines14 if x0 <= (l.x0 + l.x1) / 2 < x1 and y0 <= l.y0 < y1),
                 key=lambda l: (l.y0, l.x0))
    return traced(display(' '.join(l.text for l in got)))


_cols = [(140, 255), (255, 360), (360, 482)]
_rows = [(228, 298), (298, 352), (352, 382)]
_methods = [[_cell(x0, x1, y0, y1) for y0, y1 in _rows] for x0, x1 in _cols]
_q9c_asides = [traced(l.text) for l in _lines14 if 390 <= l.y0 < 420]
assert len(_q9c_asides) == 2 and all(a.endswith(']') for a in _q9c_asides), _q9c_asides
# "the white salt" of (c) is the one (b) introduces: (b)'s lead is (c)'s stem.
Q9B = P.ask(k('9', 'b'))
C.add([k('9', 'c', 'i')], 'chem-u2', 'flame-test-procedure', [
    # Each step one row accepting the other methods' (three methods' steps routed would pass
    # the row cap); the last step reads the same in all three.
    C.accepting(C.lifted(f'r-{i + 1}', _methods[0][i], m,
                         ('Claim the steps of one method, not a mix: Method 1 first, then Methods 2 and 3.'
                          if i == 0 else 'Method 1, then Methods 2 and 3, of the same method as above.')
                         + (' The scheme adds: ' + ' '.join(_q9c_asides) if i == 2 else '')),
                *dict.fromkeys(x for x in (_methods[1][i], _methods[2][i]) if x != _methods[0][i]))
    for i, m in enumerate((6, 5, 1))],
    figure=S + 'q9c-i', stem=Q9B,
    notes='The scheme sets out three methods in a table, each in three steps priced (6), (5) and (1), '
          '(6 + 5 + 1) in all; the rows here are Method 1, and its own print of all three is shown with '
          'the answer.')
C.fixed([k('9', 'c', 'ii')], 'chem-1-2', 'flame-colour-of-potassium', stem=Q9B)
C.fixed([k('9', 'd')], 'chem-u2', 'test-for-chloride-ion')
C.fixed([k('9', 'e')], 'chem-1-3', 'why-potassium-is-more-reactive-than-sodium')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
assert cells(k('10', 'a')) == ['[7 + (6 × 3)]'], P.items(k('10', 'a'))
C.ordered([k('10', 'a')], 'chem-3-4', 'acids-bases-and-neutralisation')
print_question('paper-q10a-print')
# (b): "Define (i) atomic number, (ii) mass number, (iii) isotopes." is one
# sentence; the scheme prices each definition with a cell of its own.
_q10b = P.ask(k('10', 'b'))
_define = cut(_q10b, None, 'Refer to')
_refer = cut(_q10b, 'Refer to')
# (i)'s answer ends in a solidus before its aside, which runs on to the next lines.
_q10b1 = P.items(k('10', 'b', 'i'))
assert [it.cell for it in _q10b1] == ['[3]'], _q10b1
_q10b1_t = cut(_q10b1[0].text, None, ' [Allow')
assert _q10b1_t.endswith(' /'), _q10b1_t
_q10b_fix = {_q10b1_t: _q10b1_t[:-len(' /')]}
for r, concept in (('i', 'definition-of-atomic-number'), ('ii', 'definition-of-mass-number'),
                   ('iii', 'definition-of-isotopes')):
    assert cells(k('10', 'b', r)) == [['[3]'], ['[3]'], ['[2 × 3]']][['i', 'ii', 'iii'].index(r)]
    C.fixed([k('10', 'b', r)], 'chem-1-2', concept, qtext=_define, stem='', cid=f'q10-b-{r}',
            row_notes={0: f'For ({r}).'}, fixes=_q10b_fix if r == 'i' else None)
C.fixed([k('10', 'b', 'iv')], 'chem-1-2', 'atomic-number-of-chlorine', stem=_refer)
C.fixed([k('10', 'b', 'v')], 'chem-1-2', 'electron-arrangement-of-chlorine', stem=_refer)
C.fixed([k('10', 'b', 'vi')], 'chem-1-2', 'relative-atomic-mass-of-chlorine', stem=_refer)
C.fixed([k('10', 'b', 'vii')], 'chem-1-2', 'why-chlorines-relative-atomic-mass-is-not-whole', stem=_refer)
Q10C = FIG + 'paper-q10c'
assert cells(k('10', 'c', 'i')) == ['[3 × 3]'], P.items(k('10', 'c', 'i'))
C.fixed([k('10', 'c', 'i')], 'chem-1-4', 'a-mole-of-dinitrogen-oxide', figure=Q10C)
C.fixed([k('10', 'c', 'ii')], 'chem-1-4', 'molar-mass-of-ammonium-nitrate', figure=Q10C)
# (iii): two asks, each priced by its answer, (6) and (7), with boxed working
# beneath, (3) + (3) and (3) + (4); a fraction in the first box.
_q10c3 = P.items(k('10', 'c', 'iii'))
assert [it.cell for it in _q10c3] == ['[6]', '[3]', '[3]', '[7]', '[3]', '[4]'], _q10c3
C.add([k('10', 'c', 'iii')], 'chem-1-4', 'moles-of-water-and-volume-of-dinitrogen-oxide', [
    C.lifted('r-1', _q10c3[0].text, 6, 'For "how many moles of water are formed?" The scheme sets out the '
             'working that earns it in a box, (3) + (3).'),
    C.lifted('r-2', _q10c3[3].text, 7, 'For "What volume does the N₂O gas produced occupy at s.t.p.?" The '
             'scheme sets out the working that earns it in a box, (3) + (4).')],
    figure=S + 'q10c-iii',
    notes='The scheme prices each answer and boxes the working beneath it; its own print of the working '
          'is shown with the answer.')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): its own ask (5), (i) and (ii) (3 each), then two asks the paper sets
# unnumbered after (ii), each priced by a cell of its own: (6) and (3 + 3 + 2).
_q11a = P.ask(k('11', 'a'))
_matter = cut(_q11a, None, 'Name the three')
_states = cut(_q11a, 'Name the three', 'What is the difference')
_diff = cut(_q11a, 'What is the difference')
C.fixed([k('11', 'a')], 'chem-1-1', 'three-states-of-matter', qtext=_states, stem=_matter)
_q11a2 = P.items(k('11', 'a', 'ii'))
assert [it.cell for it in _q11a2] == ['[3]', '[6]', '[3 + 3 + 2]', None], _q11a2
C.fixed([k('11', 'a', 'i')], 'chem-1-2', 'difference-between-an-atom-and-an-ion', stem=_matter + ' ' + _diff)
C.add([k('11', 'a', 'ii')], 'chem-1-1', 'difference-between-an-atom-and-a-molecule', [
    C.lifted('r-1', _q11a2[0].text, 3)], stem=_matter + ' ' + _diff, qtext=P.ask(k('11', 'a', 'ii'),
                                                                                upto='molecule?'))
_after = P.ask(k('11', 'a', 'ii'))
C.add([k('11', 'a')], 'chem-1-1', 'an-example-of-diffusion', [
    C.lifted('r-1', _q11a2[1].text, 6, 'The scheme adds: ' + ' '.join(_q11a2[1].asides))],
    stem=_matter, qtext=cut(_after, 'Diffusion is', 'Supply the missing'), cid='q11-a-diffusion',
    ref_suffix='after (ii), diffusion')
_boyle = _q11a2[2].points() + [_q11a2[3].text]
assert len(_boyle) == 3, _boyle
C.add([k('11', 'a')], 'chem-2-3', 'boyles-law', [
    C.lifted(f'r-{i + 1}', t, None, 'The scheme adds: ' + ' '.join(_q11a2[3].asides) if i == 2 else '')
    for i, t in enumerate(_boyle)],
    kind='orderedSplit', notation='[3 + 3 + 2]', total=8, notes=SPLIT.format('[3 + 3 + 2]'),
    stem=_matter, qtext=cut(_after, 'Supply the missing'), cid='q11-a-boyles-law',
    ref_suffix='after (ii), Boyle’s law')
print_question('paper-q11a-boyle-print')
# (b): the paper underlines "chemical equilibrium"; (ii)'s answer is a fraction.
Q11B = FIG + 'paper-q11b'
C.ordered([k('11', 'b', 'i')], 'chem-3-3', 'definition-of-chemical-equilibrium')
print_question('paper-q11b-i-print')
C.drawn([k('11', 'b', 'ii')], 'chem-3-3', 'kc-expression-for-sulfuryl-chloride', S + 'q11b-ii')
C.ordered([k('11', 'b', 'iii'), k('11', 'b', 'iv')], 'chem-3-3', 'changing-the-colour-of-the-equilibrium-mixture',
          figure=Q11B)
# (c)A: "How do most metals compare to most plastics in terms of (i) hardness,
# (ii) lustre?" is one sentence, priced (6 + 3); two asks follow unnumbered, each
# (6); then (iii) and (iv), priced (2 × 2).
_q11ca = P.ask(ka('11', 'c', None, 'A'))
_metals = cut(_q11ca, None, 'Copper is used')
_copper = cut(_q11ca, 'Copper is used', 'What property')
_cable = cut(_q11ca, 'What property')
_q11ca_lead = P.lead(ka('11', 'c', None, 'A'))
_plumbing = cut(_q11ca_lead, None, 'What metallic')
_metallic = cut(_q11ca_lead, 'What metallic')
_ca = [P.items(ka('11', 'c', r, 'A')) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _ca] == [[None], ['[6 + 3]', '[6]', '[6]']], _ca
assert _ca[0][0].text.endswith(' //'), _ca
C.add([ka('11', 'c', 'i', 'A'), ka('11', 'c', 'ii', 'A')], 'chem-1-3', 'metals-and-plastics-compared', [
    C.lifted('r-1', _ca[0][0].text[:-len(' //')], None, 'For (i).'),
    C.lifted('r-2', _ca[1][0].text, None, 'For (ii).')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'), qtext=_metals, stem='')
C.add([ka('11', 'c', None, 'A')], 'chem-4-2', 'why-pvc-suits-electrical-cable', [
    C.lifted('r-1', _ca[1][1].text, 6)], qtext=_cable, stem=_copper, cid='q11-c-a-pvc-in-cable',
    ref_suffix='after (ii), PVC in electrical cable')
C.add([ka('11', 'c', None, 'A')], 'chem-4-2', 'an-advantage-of-pvc-plumbing', [
    C.lifted('r-1', _ca[1][2].text, 6, 'The scheme adds: ' + ' '.join(_ca[1][2].asides))],
    qtext=_plumbing, stem=_copper, cid='q11-c-a-pvc-for-plumbing', ref_suffix='after (ii), PVC for plumbing')
_cb = [P.items(ka('11', 'c', r, 'A')) for r in ('iii', 'iv')]
assert [[it.cell for it in x] for x in _cb] == [[None], ['[2 × 2]']] and _cb[0][0].text.endswith(' //'), _cb
C.add([ka('11', 'c', 'iii', 'A'), ka('11', 'c', 'iv', 'A')], 'chem-1-3', 'malleability-and-ductility', [
    C.lifted('r-1', _cb[0][0].text[:-len(' //')], 2,
             'For (iii). The scheme prices this point and the next (2 × 2), one each.'),
    C.lifted('r-2', _cb[1][0].text, 2, 'For (iv).')], stem=_copper + ' ' + _metallic)
# (c)B: the candidate answers for the one industry studied. The scheme prints
# (ii), (iii) and (v) industry by industry, each answer linked to the formula
# given in (i): the industries' answers are the options of one menu, and the
# candidate claims the one (or, for (iii), the two) for the industry studied.
Q11CB = FIG + 'paper-q11c-b'
INDUSTRY = ('The scheme gives the answer for each of the three industries; only the one for the '
            'industry the candidate studied, named in (i), earns the marks.')
# The instruction that opens B names the three case studies: it is each card's stem.
Q11CB_STEM = P.ask(ka('11', 'c', None, 'B'))
assert Q11CB_STEM.startswith('Answer the questions below about any one of these three case studies:'), Q11CB_STEM
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-u3', 'formula-of-the-main-product', stem=Q11CB_STEM)
_ind = re.compile(r' (?=(?:NH₃|HNO₃|MgO): )')
_b2 = P.items(ka('11', 'c', 'ii', 'B'))
assert [it.cell for it in _b2] == ['[6]'], _b2
_uses = [traced(u) for u in _ind.split(display(_b2[0].text))]
assert [u.split(':')[0] for u in _uses] == ['NH₃', 'HNO₃', 'MgO'], _uses
C.add([ka('11', 'c', 'ii', 'B')], 'chem-u3', 'major-use-of-the-main-product', [
    anyN('r-1', _uses[0], 6, 1, 6, _uses, 'Any one of these: the one for the industry studied.')], total=6,
    stem=Q11CB_STEM,
    notes=INDUSTRY + ' The scheme adds: ' + ' '.join(_b2[0].asides))
# (iii): "ANY TWO FROM ONE LINE: (2 × 3)" -- two feedstocks from the line of the
# industry studied. The options are the three lines in order, each opening with
# its industry's formula as printed; "river water", printed on all three lines,
# is offered once.
_b3 = P.items(ka('11', 'c', 'iii', 'B'))
assert [it.cell for it in _b3] == [None], _b3
_feeds = _ind.split(display(_b3[0].text))
assert [f.split(':')[0] for f in _feeds] == ['NH₃', 'HNO₃', 'MgO'], _feeds
_opts = list(dict.fromkeys(traced(o) for f in _feeds for o in f.split(' / ')))
assert len(_opts) == 7 and _opts.count('river water') == 1, _opts
C.add([ka('11', 'c', 'iii', 'B')], 'chem-u3', 'feedstocks-of-the-industry-studied', [
    anyN('r-1', _opts[0], 6, 2, 3, _opts, 'Any two of these, from the line of the industry studied.')],
    total=6, figure=Q11CB, stem=Q11CB_STEM,
    notes=INDUSTRY + ' The scheme sets each industry\'s feedstocks on a line of its own -- NH₃, then HNO₃, '
          'then MgO, each line ending "river water" -- and prices the part "'
          + traced('ANY TWO FROM ONE LINE: (2 × 3)') + '". The scheme adds: ' + ' '.join(_b3[0].asides))
_b4 = P.items(ka('11', 'c', 'iv', 'B'))
assert [it.cell for it in _b4] == [None], _b4
# Each feature opens a printed line of its own; "(market, customers, workforce)"
# is the last one's wrapped tail.
_feats = []
for row in (r.text for r in _b4[0].rows if r.text):
    if row.startswith('(') and _feats:
        _feats[-1] += ' ' + row
    else:
        _feats.append(row)
_feats = [traced(display(f)) for f in _feats]
assert len(_feats) == 4 and all(': ' in f for f in _feats), _feats
C.add([ka('11', 'c', 'iv', 'B')], 'chem-u3', 'infrastructure-an-industry-needs', [
    anyN('r-1', _feats[0], 6, 1, 6, _feats, 'Any one of these.')], total=6, figure=Q11CB, stem=Q11CB_STEM,
    notes='The scheme sets out each feature on the right of the paper\'s picture with the explanation it '
          'accepts, and prices the part "' + traced('ANY EXPLANATION: (6)') + '". The scheme adds: '
          + ' '.join(_b4[0].asides))
# (v): emissions or waste effluent, for each industry: six answers, one claimed.
_b5 = P.items(ka('11', 'c', 'v', 'B'))
assert [it.cell for it in _b5] == ['[4]', None] and _b5[1].text == 'Blank Page', _b5
_t = display(_b5[0].text)
assert _t.startswith('emissions ') and ' / waste effluent ' in _t, _t
_emis, _waste = _t[len('emissions '):].split(' / waste effluent ')
_ways = [traced(re.sub(r'\s*/$', '', line)) for block in (_emis, _waste) for line in _ind.split(block)]
assert [w.split(':')[0] for w in _ways] == ['NH₃', 'HNO₃', 'MgO'] * 2, _ways
assert ' oxides of / nitrogen' in _ways[1], _ways
C.add([ka('11', 'c', 'v', 'B')], 'chem-u3', 'dealing-with-emissions-or-waste-effluent', [
    anyN('r-1', _ways[0], 4, 1, 4, _ways, 'Any one of these: the first three are the scheme\'s answers for '
         'emissions, the last three for waste effluent.')], total=4, stem=Q11CB_STEM,
    notes=INDUSTRY + ' The question asks for either emissions or waste effluent, and the scheme sets out '
          'both for each industry. In the HNO₃ emissions answer the scheme prints its solidus between '
          '"oxides of" and "nitrogen (ammonia)", where its line wraps. The scheme adds: '
          + ' '.join(_b5[0].asides))


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
    """Every letter's printed marks, alternatives apart: the paper prints Q11's
    letters in subtotals ("(11)" then "(14)"), so the sum of every mark printed
    under the letter, not the last."""
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
