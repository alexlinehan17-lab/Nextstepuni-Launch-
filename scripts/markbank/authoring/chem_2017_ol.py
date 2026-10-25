#!/usr/bin/env python3
"""2017 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2017_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2017_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2017_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2017 ol

No 2017 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The paper sets some romans inside one sentence -- Q11(b) "Define (i) an acid,
(ii) pH.", Q11(c)A "How does (i) the greenhouse effect, (ii) the ozone layer,
help make conditions favourable for life on Earth?" -- and the scheme prices
each with a cell of its own: those cards take the sentence as their question.
Q5(d), Q11(b) and Q11(c)A set asks unnumbered after their last roman, each
priced by a cell of its own: one card each, cited "after (ii)". Q6(c) asks two
things in one letter, priced "(6)" and "(6 + 3)": one card each, the second
cited by what it asks. The paper prints Q7(a)'s passage with numbered blanks
and underlines the term Q10(b)(i) asks about, which no text layer carries:
those take the paper's own print as their question, as do Q9(d) (the table it
plots) and Q11(a)(ii) (the equation, whose subscripts the text layer drops),
whose answers are the scheme's drawings. Q4(k) and Q11(c) offer whole
alternative parts A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN, point)

P = Printed(2017, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2017-OL-'
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
        raise Refused(f'"{text}" is not in the 2017 ol scheme')
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

# ── Q1 Ethene, ethyne and chromatography ─────────────────────────────────────
C.fixed([k('1', 'a', 'i')], 'chem-2-4', 'reagent-to-test-for-unsaturation')
# (ii): the two colours, priced (2 × 3), print a line each.
assert cells(k('1', 'a', 'ii')) == ['[2 × 3]'], P.items(k('1', 'a', 'ii'))
C.fixed([k('1', 'a', 'ii')], 'chem-2-4', 'colour-change-in-the-unsaturation-test')
C.fixed([k('1', 'b', 'i')], 'chem-2-4', 'combustion-test-on-ethyne')
C.fixed([k('1', 'b', 'ii')], 'chem-2-4', 'flame-of-burning-ethyne')
# (iii): the cue "COPY, / COMPLETE, / BALANCE:" leaves its first two lines on the
# equation's row; the cell is "PRODUCTS: (3), BALANCING: (3)".
_q1b3 = P.items(k('1', 'b', 'iii'))
assert [it.cell for it in _q1b3] == ['[3 + 3]'], _q1b3
_t = _q1b3[0].text
assert _t.startswith('COPY, ') and _t.endswith(' COMPLETE,'), _t
C.fixed([k('1', 'b', 'iii')], 'chem-3-1', 'combustion-of-ethyne',
        fixes={_t: _t[len('COPY, '):-len(' COMPLETE,')]})
C.fixed([k('1', 'b', 'iv')], 'chem-u2', 'limewater-test-for-carbon-dioxide')
Q1C = FIG + 'paper-q1c'
assert cells(k('1', 'c', 'i')) == ['[3]', '[3]', '[3]'], P.items(k('1', 'c', 'i'))
C.fixed([k('1', 'c', 'i')], 'chem-u2', 'labelling-a-chromatogram', figure=Q1C)
C.fixed([k('1', 'c', 'ii')], 'chem-u2', 'how-many-indicators-were-separated', figure=Q1C)
C.fixed([k('1', 'c', 'iii')], 'chem-u2', 'component-carried-fastest', figure=Q1C)
C.fixed([k('1', 'c', 'iv')], 'chem-u2', 'why-components-separate-in-chromatography', figure=Q1C)

# ── Q2 A titration of sodium hydroxide with hydrochloric acid ────────────────
Q2 = FIG + 'paper-q2'
C.fixed([k('2', 'a', 'i')], 'chem-4-1', 'naming-the-conical-flask', figure=Q2)
C.fixed([k('2', 'a', 'ii')], 'chem-4-1', 'rinsing-the-conical-flask', figure=Q2)
C.fixed([k('2', 'b', 'i')], 'chem-4-1', 'naming-the-wash-bottle', figure=Q2)
C.fixed([k('2', 'b', 'ii')], 'chem-4-1', 'what-the-wash-bottle-is-for', figure=Q2)
C.fixed([k('2', 'c', 'i')], 'chem-4-1', 'indicator-for-an-acid-base-titration', figure=Q2)
C.fixed([k('2', 'c', 'ii')], 'chem-4-1', 'why-use-a-white-tile', figure=Q2)
C.fixed([k('2', 'd', 'i')], 'chem-4-1', 'why-do-a-rough-titration')
C.fixed([k('2', 'd', 'ii')], 'chem-4-1', 'average-titre')
# (e): the titres it needs are printed in (d), after (d)(i): the stem carries
# that sentence between the question's lead-in and (e)'s.
_readings = P.lead(k('2', 'd', 'i'))
assert _readings.startswith('The burette readings noted in this experiment were'), _readings
Q2E = ' '.join([P.ask(k('2')), _readings, P.ask(k('2', 'e'))])
# (e)(i): the answer (9) and the working that earns it, a box of stacked
# fractions the text layer cannot order.
assert cells(k('2', 'e', 'i'))[0] == '[9]', P.items(k('2', 'e', 'i'))
C.answer_only([k('2', 'e', 'i')], 'chem-4-1', 'concentration-of-sodium-hydroxide-in-moles-per-litre',
              S + 'q2e-i', stem=Q2E)
_q2e2 = P.items(k('2', 'e', 'ii'))
assert [it.cell for it in _q2e2] == ['[6]', '[3]', '[3]', None], _q2e2
C.route([k('2', 'e', 'ii')], 'chem-4-1', 'concentration-of-sodium-hydroxide-in-grams-per-litre', stem=Q2E,
        notes='The scheme adds: ' + traced(_q2e2[3].text))

# ── Q3 The heat of neutralisation ────────────────────────────────────────────
Q3 = FIG + 'paper-q3'
Q3D = FIG + 'paper-q3d'
C.fixed([k('3', 'a')], 'chem-3-1', 'neutralisation-is-exothermic', figure=Q3)
C.fixed([k('3', 'b')], 'chem-u2', 'preventing-heat-loss-and-stirring', figure=Q3)
C.fixed([k('3', 'c')], 'chem-u2', 'measuring-100-cm3-accurately', figure=Q3)
C.fixed([k('3', 'd', 'i')], 'chem-u2', 'corrosive-hazard-pictogram', figure=Q3D)
C.fixed([k('3', 'd', 'ii')], 'chem-u2', 'handling-a-corrosive-solution-safely', figure=Q3D)
C.fixed([k('3', 'e', 'i')], 'chem-3-1', 'temperature-rise-with-half-the-base', figure=Q3)
C.fixed([k('3', 'e', 'ii')], 'chem-3-1', 'why-the-temperature-rise-is-halved', figure=Q3)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-2', 'marie-curie', notes=Q4_NOTE, figure=FIG + 'paper-q4a')
assert cells(k('4', 'b')) == ['[2 × 3]'], P.items(k('4', 'b'))
C.fixed([k('4', 'b')], 'chem-1-2', 'rutherfords-two-parts-of-an-atom', notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-3-5', 'oxidation-as-loss-of-electrons', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-1-3', 'atomic-radius-across-a-period', notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-2-3', 'charles-law', notes=Q4_NOTE)
assert cells(k('4', 'f')) == ['[3 + 3]'], P.items(k('4', 'f'))
C.fixed([k('4', 'f')], 'chem-1-4', 'equation-for-magnesium-burning-in-oxygen', notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-4-2', 'substitution-reaction-of-methane', notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-1-1', 'diffusion', notes=Q4_NOTE, figure=FIG + 'paper-q4h')
# (i): the answer (6), then two boxed routes side by side, (3) a step; the rows
# are the first route, the second in the notes. The text layer reads the two
# boxes across, so the first route is items 1 and 3.
_q4i = P.items(k('4', 'i'))
assert [it.cell for it in _q4i] == ['[6]', '[3]', '[3]', '[3]', '[3]'], _q4i
assert _q4i[1].text.startswith('0.016 × 10 ') and _q4i[3].text.startswith('0.16 × 1000 '), _q4i
C.add([k('4', 'i')], 'chem-1-4', 'concentration-in-parts-per-million', [
    C.lifted('r-1', _q4i[1].text, 3, 'Or, by the scheme\'s second route, "' + traced(_q4i[2].text) + '" (3).'),
    C.lifted('r-2', _q4i[3].text, 3, 'Or, by the second route, "' + traced(_q4i[4].text) + '" (3).')],
    notes='The scheme gives the answer, ' + display(_q4i[0].text) + ', priced (6), then the working that '
          'earns it in two boxed routes, step by step; the steps here are its first route. ' + Q4_NOTE)
assert cells(k('4', 'j')) == ['[2 × 3]'], P.items(k('4', 'j'))
C.fixed([k('4', 'j')], 'chem-3-5', 'products-of-electrolysing-acidified-water', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'natural-fixation-of-nitrogen', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-u3', 'carbon-in-steel', notes=Q4_NOTE)

# ── Q5 Elements and atoms ────────────────────────────────────────────────────
C.fixed([k('5', 'a', 'i')], 'chem-1-1', 'definition-of-an-element')
C.fixed([k('5', 'a', 'ii')], 'chem-1-3', 'mendeleevs-periodic-table', figure=FIG + 'paper-q5')
C.fixed([k('5', 'b')], 'chem-1-2', 'definition-of-atomic-number')
# (c): the nuclides print with the mass number over the atomic number before X,
# which the text layer reads "¹² 6 X".


def nuclides(text):
    return P.rearranged(P.rearranged(text, '¹² 6 X', '¹²₆X'), '¹⁴ 6 X', '¹⁴₆X')


Q5C = nuclides(C.context(k('5', 'c', 'i')))
C.fixed([k('5', 'c', 'i')], 'chem-1-2', 'how-isotopes-of-an-element-differ', stem=Q5C,
        qtext=nuclides(P.ask(k('5', 'c', 'i'))))
C.fixed([k('5', 'c', 'ii')], 'chem-1-2', 'isotopes', stem=Q5C)
C.fixed([k('5', 'c', 'iii')], 'chem-1-2', 'electrons-in-the-carbon-isotopes', stem=Q5C)
C.fixed([k('5', 'c', 'iv')], 'chem-1-2', 'identifying-carbon', stem=Q5C)
# (d): two drawings priced together "(6 + 3)", then an ask the paper sets
# unnumbered after (ii), priced (3) and (3).
_q5d = P.items(k('5', 'd', 'ii'))
assert [it.cell for it in _q5d] == ['[6 + 3]', '[3]', '[3]', '[3]', None], _q5d
assert _q5d[0].text == '' and cells(k('5', 'd', 'i')) == [], _q5d
_q5d_draw = P.lead(k('5', 'd'))
assert _q5d_draw.startswith('Draw diagrams') if _q5d_draw else True
_q5d_lead = P.ask(k('5', 'd'))
_neon = P.ask(k('5', 'd', 'i'))
_fluorine = P.ask(k('5', 'd', 'ii'), upto='a fluorine atom.')
_explain = cut(P.ask(k('5', 'd', 'ii')), 'Referring to')
assert _q5d_lead.startswith('Draw diagrams') and _neon == 'a neon atom,', (_q5d_lead, _neon)
Q5_STEM = P.ask(k('5'))
C.add([k('5', 'd', 'i'), k('5', 'd', 'ii')], 'chem-1-2', 'electron-arrangements-of-neon-and-fluorine', [
    C.mark_ask(point('r-1', _neon, None, 'For (i). ' + DRAWN)),
    C.mark_ask(point('r-2', _fluorine, None, 'For (ii). ' + DRAWN + ' ' + adds(_q5d[0].asides)))],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'), figure=S + 'q5d',
    qtext=f'{_q5d_lead} (i) {_neon} (ii) {_fluorine}', stem=Q5_STEM)
# The aside under the second answer runs over two lines; the reader takes its
# "(3)" for a cell. It is one aside.
_q5d_aside = traced(_q5d[3].text + ' (3) ' + _q5d[4].text)
C.add([k('5', 'd')], 'chem-1-3', 'why-fluorine-is-more-reactive-than-neon', [
    C.lifted('r-1', _q5d[1].text, 3),
    C.lifted('r-2', _q5d[2].text, 3, 'The scheme adds: ' + _q5d_aside)],
    qtext=_explain, stem=f'{Q5_STEM} {_q5d_lead} (i) {_neon} (ii) {_fluorine}', cid='q5-d-more-reactive',
    ref_suffix='after (ii), the more reactive element')

# ── Q6 Hydrocarbons ──────────────────────────────────────────────────────────
Q6 = FIG + 'paper-q6'
C.fixed([k('6', 'a')], 'chem-2-4', 'what-makes-a-hydrocarbon', figure=Q6)
C.fixed([k('6', 'b')], 'chem-2-4', 'a-source-of-methane-and-why-mercaptans-are-added', figure=Q6)
# (c): two asks, priced (6) and (6 + 3): the series, then another member named
# and drawn, the name and structure priced together. One card each; the
# scheme draws ethane and propane beside their formulae.
_q6c = P.items(k('6', 'c'))
assert [it.cell for it in _q6c] == ['[6]', '[6 + 3]', None], _q6c
_q6c_pts = _q6c[1].points()
assert len(_q6c_pts) == 2 and _q6c[2].text.startswith('[Hs need not'), (_q6c_pts, _q6c)
_series = cut(P.ask(k('6', 'c')), None, 'Name one other')
_member = cut(P.ask(k('6', 'c')), 'Name one other')
C.add([k('6', 'c')], 'chem-2-4', 'homologous-series-of-methane-and-butane', [
    C.lifted('r-1', _q6c[0].text, 6)], qtext=_series, figure=Q6)
C.add([k('6', 'c')], 'chem-2-4', 'another-alkane-and-its-structure', [
    C.lifted('r-1', _q6c_pts[0], None, 'For "Name one other member of this series".'),
    C.lifted('r-2', _q6c_pts[1], None, 'For "draw the structure of one of its molecules". The scheme draws the '
             'structures too; its own print is shown with the answer. The scheme adds: '
             + traced(_q6c[2].text))],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'), figure=S + 'q6c',
    qtext=_member, stem=C.context(k('6', 'c')) + ' ' + _series, cid='q6-c-another-alkane',
    ref_suffix='another alkane and its structure')
C.fixed([k('6', 'd')], 'chem-2-4', 'fractional-distillation-of-crude-oil', figure=Q6)
# (e): the definition (6), then "ANY ONE: (6)" of the ways to raise the octane
# number: one menu row. "addition of lead /addition of oxygenates" prints
# without a space after its solidus.
_q6e = P.items(k('6', 'e'))
assert [it.cell for it in _q6e] == ['[6]', '[6]'] and _q6e[1].asides == ['[any one]'], _q6e
_ways = [traced(w.strip()) for w in _q6e[1].text.split('/')]
assert len(_ways) == 7 and _ways[3] == 'addition of lead', _ways
C.add([k('6', 'e')], 'chem-2-4', 'octane-number', [
    C.lifted('r-1', _q6e[0].points()[0], 6),
    anyN('r-2', _ways[0], 6, 1, 6, _ways, 'Any one of these: the scheme prices the method "'
         + traced('ANY ONE: (6)') + '".')], total=12, figure=Q6)

# ── Q7 Ionic bonding, a flame test and the chloride test ─────────────────────
# (a): six words, the cell labelled "FIRST FIVE:", the passage the paper's print.
assert cells(k('7', 'a')) == ['[6 + 4 × 5]'], P.items(k('7', 'a'))
C.ordered([k('7', 'a')], 'chem-2-1', 'ionic-bonding-in-sodium-chloride',
          notes='The scheme sets the cell as "' + traced('FIRST FIVE: (6 + 4 × 5)') + '": six blanks, '
                'the first five answers marked.')
print_question('paper-q7a-print')
# (b)(i): three methods set out as a table, each in three steps priced (4); the
# text layer reads the table across its columns, so each cell is read from the
# lines inside its column and row (scheme PDF page 11), Method 1 as the rows
# and the others in the notes, and the scheme's own print of the table is the
# answer picture. The passage printed after (a) is (a)'s, not (b)'s lead-in.
assert [it.cell for it in P.items(k('7', 'b', 'i'))] == ['[3 × 4]', '[4]', '[4]', '[4]', None]
_lines11 = [l for l in read_lines(P.scheme_path) if l.page == 11]


def _cell(x0, x1, y0, y1):
    got = sorted((l for l in _lines11 if x0 <= (l.x0 + l.x1) / 2 < x1 and y0 <= l.y0 < y1),
                 key=lambda l: (l.y0, l.x0))
    for l in got:
        traced(l.text)
    return display(' '.join(l.text for l in got))


_cols = [(135, 248), (248, 354), (354, 474)]
_rows = [(224, 312), (312, 386), (386, 420)]
_methods = [[_cell(x0, x1, y0, y1) for y0, y1 in _rows] for x0, x1 in _cols]
# Method 1's first cell ends "(HCl)", which the .md sets on a line of its own:
# the row is the cell up to it, the formula quoted.
_m1 = _methods[0][0]
assert _m1.endswith(' (HCl)'), _m1
_m1 = traced(_m1[:-len(' (HCl)')])
_q7b_asides = [traced(l.text) if l.text.endswith(']') else l.text for l in _lines11 if 428 <= l.y0 < 486]
assert len(_q7b_asides) == 4 and _q7b_asides[0].startswith('*[Allow'), _q7b_asides
_record = traced(_q7b_asides[1] + ' ' + _q7b_asides[2])
C.add([k('7', 'b', 'i')], 'chem-u2', 'flame-test-procedure', [
    C.lifted('r-1', _m1, 4, f'Method 1; the scheme\'s cell ends "(HCl)". Or Method 2, "{_methods[1][0]}", or '
             f'Method 3, "{_methods[2][0]}". The scheme adds: ' + _q7b_asides[0]),
    C.lifted('r-2', _methods[0][1], 4, f'Method 1. Or Method 2, "{_methods[1][1]}", or Method 3, '
             f'"{_methods[2][1]}".'),
    C.lifted('r-3', _methods[0][2], 4, f'Each method\'s last step. The scheme adds: {_record}')],
    figure=S + 'q7b-i', stem='',
    notes='The scheme sets out three methods in a table, each in three steps priced (4), (3 × 4) in all; '
          'the rows here are Method 1, and its own print of all three is shown with the answer. The scheme '
          'adds: ' + traced(_q7b_asides[3]))
C.fixed([k('7', 'b', 'ii')], 'chem-1-2', 'flame-colour-of-sodium', stem='')
C.fixed([k('7', 'c')], 'chem-u2', 'test-for-chloride-ion')

# ── Q8 Ethanol, ethanal and ethanoic acid ────────────────────────────────────
Q8 = FIG + 'paper-q8'
# (a): the structure drawn (5), its functional group circled (6), and why it
# dissolves (6); the drawing's row is the paper's ask.
_q8a = P.items(k('8', 'a'))
assert [(it.cell, it.text) for it in _q8a][:2] == [('[5]', ''), ('[6]', 'circle around OH')], _q8a
assert [it.cell for it in _q8a] == ['[5]', '[6]', '[6]', None], _q8a
_q8a_ask = P.ask(k('8', 'a'))
_draw8 = cut(_q8a_ask, None, 'Circle its')
C.add([k('8', 'a')], 'chem-4-2', 'structure-and-solubility-of-ethanol', [
    C.mark_ask(point('r-1', _draw8, 5, DRAWN + ' ' + adds(_q8a[0].asides))),
    C.lifted('r-2', _q8a[1].text, 6, adds(_q8a[1].asides)),
    C.lifted('r-3', _q8a[2].text, 6, 'The scheme adds: ' + traced(_q8a[3].text))], figure=S + 'q8a')
C.fixed([k('8', 'b')], 'chem-4-2', 'homologous-series-of-ethanal', figure=Q8)
assert cells(k('8', 'c', 'iii')) == ['[6 + 6 + 3]'], P.items(k('8', 'c', 'iii'))
C.ordered([k('8', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-4-2', 'ethanol-ethanal-and-ethanoic-acid',
          figure=Q8)
# (d): the two reagents print either side of the second line of the cue "NAME OR
# / GIVE:" (scheme PDF page 12), so the second rides on the first.
_q8d = P.items(k('8', 'd'))
assert [it.cell for it in _q8d] == ['[6]'] and len(_q8d[0].rows) == 2, _q8d
_reagents = [display(r.text).rstrip('/ ') for r in _q8d[0].rows]
assert _reagents[0].startswith('potassium permanganate') and _reagents[1].startswith('sodium'), _reagents
C.add([k('8', 'd')], 'chem-4-2', 'oxidising-ethanol', [
    C.lifted('r-1', _reagents[0], 6, 'Or "' + traced(_reagents[1]) + '".')], figure=Q8)
C.fixed([k('8', 'e')], 'chem-u2', 'detecting-ethanol-in-blood', figure=Q8)

# ── Q9 The decomposition of hydrogen peroxide by liver ───────────────────────
# The equation prints "enzyme" over its arrow and the results are a table: both
# are a picture (paper-q9). A card that shows another picture leaves out the
# sentence that introduces them.
Q9 = FIG + 'paper-q9'
_q9_eq = ' The reaction that took place was:'


def q9_stem(key):
    ctx = C.context(key)
    assert ctx.count(_q9_eq) == 1, ctx
    return ctx.replace(_q9_eq, '')


assert cells(k('9', 'a')) == ['[3 + 2]'], P.items(k('9', 'a'))
C.ordered([k('9', 'a')], 'chem-3-2', 'rate-and-the-time-to-make-an-amount-of-product', figure=Q9)
C.fixed([k('9', 'b', 'i')], 'chem-3-2', 'definition-of-a-catalyst', figure=Q9)
C.fixed([k('9', 'b', 'ii')], 'chem-3-2', 'definition-of-an-enzyme', figure=Q9)
C.fixed([k('9', 'b', 'iii')], 'chem-3-2', 'a-black-powder-catalyst', figure=Q9)
# (c): the scheme answers with its own drawings, lettered A, B and C for (i)
# and X and Y for (ii), priced together (6 + 3).
C.ordered([k('9', 'c', 'i'), k('9', 'c', 'ii')], 'chem-u2', 'apparatus-to-measure-the-oxygen-produced',
          drawn=(k('9', 'c', 'i'), k('9', 'c', 'ii')), figure=S + 'q9c', stem=q9_stem(k('9', 'c', 'i')),
          notes='A, B, C, X and Y name the scheme\'s own drawings, shown with the answer.')
C.fixed([k('9', 'd')], 'chem-3-2', 'graph-of-oxygen-volume-against-time', figure=S + 'q9d')
print_question('paper-q9d-print')
C.fixed([k('9', 'e')], 'chem-3-2', 'volume-read-from-the-graph', figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('10', 'a', 'i')], 'chem-4-3', 'primary-sewage-treatment')
C.fixed([k('10', 'a', 'ii')], 'chem-4-3', 'secondary-sewage-treatment')
C.fixed([k('10', 'a', 'iii')], 'chem-4-3', 'tertiary-sewage-treatment')
C.fixed([k('10', 'a', 'iv')], 'chem-4-3', 'eutrophication')
# (b)(i): the paper underlines "covalent bonds".
C.fixed([k('10', 'b', 'i')], 'chem-2-1', 'covalent-bond')
print_question('paper-q10b-i-print')
C.menu([k('10', 'b', 'ii')], 'chem-2-1', 'dot-and-cross-diagram-of-water', figure=S + 'q10b-ii',
       note='The scheme draws the molecule two ways and prices the part "' + traced('ANY THREE: (3 × 3)')
            + '"; its own print is shown with the answer.')
C.fixed([k('10', 'b', 'iii')], 'chem-2-2', 'shape-of-a-water-molecule')
C.fixed([k('10', 'b', 'iv')], 'chem-2-1', 'definition-of-electronegativity')
C.fixed([k('10', 'b', 'v')], 'chem-2-1', 'polar-covalent-bonds-in-water')
Q10C = FIG + 'paper-q10c'
# (c)(i): a pair priced (2 × 3), or instead the scheme's second pair after "or"
# (the reader drops the "or" between them).
_q10c1 = P.items(k('10', 'c', 'i'))
assert [it.cell for it in _q10c1] == ['[2 × 3]'], _q10c1
_law = _q10c1[0].points()
assert len(_law) == 4, _law
C.add([k('10', 'c', 'i')], 'chem-1-4', 'law-of-conservation-of-mass', [
    C.lifted('r-1', _law[0], 3, 'The scheme prices this point and the next (2 × 3), one each; or instead, '
             '(2 × 3), the pair "' + traced(_law[2] + ' // ' + _law[3]) + '".'),
    C.lifted('r-2', _law[1], 3)], figure=Q10C)
C.fixed([k('10', 'c', 'ii')], 'chem-1-4', 'molar-mass-of-sodium-azide', figure=Q10C)
assert cells(k('10', 'c', 'iii')) == ['[6]', '[6]'], P.items(k('10', 'c', 'iii'))
C.answer_only([k('10', 'c', 'iii')], 'chem-1-4', 'moles-of-sodium-azide', S + 'q10c-iii')
# (iv): the answer (3), then two boxed routes to it, (3) each.
_q10c4 = P.items(k('10', 'c', 'iv'))
assert [it.cell for it in _q10c4] == ['[3]', '[3]', '[3]'], _q10c4
# The working is text; the card's picture is the stimulus, not a print of the routes.
C.route([k('10', 'c', 'iv')], 'chem-1-4', 'mass-of-nitrogen-formed',
        notes='Or, by its second route, "' + traced(display(_q10c4[2].text)) + '" (3).')
C.cards[-1]['figureKey'] = Q10C
C.route([k('10', 'c', 'v')], 'chem-1-4', 'moles-of-nitrogen-at-stp')
C.cards[-1]['figureKey'] = Q10C

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the equation's subscripts print in the size of its state symbols, which
# the text layer reads as "2SO2 (g)": the equation is a picture (paper-q11a).
Q11A = FIG + 'paper-q11a'
assert cells(k('11', 'a', 'i')) == ['[4 + 3]'], P.items(k('11', 'a', 'i'))
C.ordered([k('11', 'a', 'i')], 'chem-3-3', 'equilibrium-is-dynamic', figure=Q11A)
# (ii): the Kc expression is a fraction; the aside under it runs over two lines
# and the reader takes its last "(3)" for a cell. It is one aside.
_q11a2 = P.items(k('11', 'a', 'ii'))
assert [(it.cell, bool(it.text)) for it in _q11a2] == [('[6]', False), ('[3]', True), (None, True)], _q11a2
_kc_aside = traced(_q11a2[1].text + ' (3) ' + _q11a2[2].text)
C.add([k('11', 'a', 'ii')], 'chem-3-3', 'kc-expression-for-sulfur-trioxide', [
    C.mark_ask(point('r-1', C.drawn_ask(k('11', 'a', 'ii')), 6,
                     'The scheme answers this with the expression set as a fraction, which its text cannot '
                     'carry; its own print is shown with the answer. The scheme adds: ' + _kc_aside))],
    figure=S + 'q11a-ii')
print_question('paper-q11a-ii-print')
assert cells(k('11', 'a', 'iv')) == ['[9 + 3]'], P.items(k('11', 'a', 'iv'))
C.ordered([k('11', 'a', 'iii'), k('11', 'a', 'iv')], 'chem-3-3', 'changing-the-yield-of-sulfur-trioxide',
          figure=Q11A)
# (b): "Define (i) an acid, (ii) pH." is one sentence, priced (4) and (2 × 3);
# three asks follow unnumbered, priced (3), (6) and (6). The scheme files all
# of them under its "(ii)" (PDF page 17).
Q11B = FIG + 'paper-q11b'
_q11b = P.ask(k('11', 'b'))
_sorensen = cut(_q11b, None, 'Define (i)')
_define = cut(_q11b, 'Define (i)', 'What is the relationship')
_poh = cut(_q11b, 'What is the relationship', 'Calculate the pH')
_calc = cut(_q11b, 'Calculate the pH', 'List, in order')
_list = cut(_q11b, 'List, in order')
assert cells(k('11', 'b', 'i')) == ['[4]'], P.items(k('11', 'b', 'i'))
C.fixed([k('11', 'b', 'i')], 'chem-3-4', 'definition-of-an-acid', qtext=_define, stem=_sorensen,
        cid='q11-b-i', row_notes={0: 'For (i).'}, figure=Q11B)
_q11b2 = P.items(k('11', 'b', 'ii'))
assert [it.cell for it in _q11b2] == ['[2 × 3]', '[3]', '[6]', '[3]', '[3]', '[6]'], _q11b2
_ph = _q11b2[0].points()
assert len(_ph) == 2, _ph
C.add([k('11', 'b', 'ii')], 'chem-3-4', 'definition-of-ph', [
    C.lifted('r-1', _ph[0], 3, 'For (ii). The scheme prices this point and the next (2 × 3), one each.'),
    C.lifted('r-2', _ph[1], 3)], qtext=_define, stem=_sorensen, figure=Q11B)
C.add([k('11', 'b')], 'chem-3-4', 'ph-plus-poh', [C.lifted('r-1', _q11b2[1].text, 3)],
      qtext=_poh, stem=_sorensen, figure=Q11B, cid='q11-b-ph-and-poh', ref_suffix='after (ii), pH and pOH')
C.add([k('11', 'b')], 'chem-3-4', 'ph-of-hydrochloric-acid', [
    C.lifted('r-1', _q11b2[3].text, 3), C.lifted('r-2', _q11b2[4].text, 3)],
    qtext=_calc, stem=_sorensen, figure=Q11B, cid='q11-b-ph-of-hcl',
    ref_suffix='after (ii), pH of hydrochloric acid',
    notes='The scheme gives the answer, ' + display(_q11b2[2].text) + ', priced (6), then the working that '
          'earns it, step by step.')
C.add([k('11', 'b')], 'chem-3-4', 'ordering-by-acidity', [
    C.lifted('r-1', _q11b2[5].text, 6, adds(_q11b2[5].asides))],
    qtext=_list, stem=_sorensen, figure=Q11B, cid='q11-b-increasing-acidity',
    ref_suffix='after (ii), increasing acidity')
# (c)A: "How does (i) the greenhouse effect, (ii) the ozone layer, help make
# conditions favourable for life on Earth?" is one sentence, priced (6) and
# (6); two asks follow unnumbered, priced (6 + 3), then one priced (4).
_a = P.ask(ka('11', 'c', None, 'A'))
assert _a.endswith(' How does'), _a
_a_lead = _a[:-len(' How does')]
_a1 = P.ask(ka('11', 'c', 'i', 'A'))
_a2 = P.ask(ka('11', 'c', 'ii', 'A'))
_ozone = cut(_a2, None, 'Give one way')
_howdoes = f'How does (i) {_a1} (ii) {_ozone}'
_q11ca1 = P.items(ka('11', 'c', 'i', 'A'))
assert [it.cell for it in _q11ca1] == ['[6]'], _q11ca1
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'the-greenhouse-effect-and-life', qtext=_howdoes,
        stem=_a_lead, cid='q11-c-a-i', row_notes={0: 'For (i).'})
_q11ca2 = P.items(ka('11', 'c', 'ii', 'A'))
assert [it.cell for it in _q11ca2] == ['[6]', '[6 + 3]', '[4]'], _q11ca2
C.add([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'the-ozone-layer-and-life', [
    C.lifted('r-1', _q11ca2[0].text, 6, 'For (ii). ' + adds(_q11ca2[0].asides))],
    qtext=_howdoes, stem=_a_lead)
_gh = _q11ca2[1].points()
assert len(_gh) == 2 and _gh[0].startswith('deforestation') and _gh[1].startswith('global warming'), _gh
_give = cut(_a2, 'Give one way', 'What possible')
_outcome = cut(_a2, 'What possible', 'How have humans')
C.add([ka('11', 'c', None, 'A')], 'chem-4-3', 'causes-and-effects-of-an-increased-greenhouse-effect', [
    C.lifted('r-1', _gh[0], None, f'For "{_give}"'),
    C.lifted('r-2', _gh[1], None, f'For "{_outcome}"')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'),
    qtext=f'{_give} {_outcome}', stem=_a_lead, cid='q11-c-a-greenhouse-effect',
    ref_suffix='after (ii), the greenhouse effect')
C.add([ka('11', 'c', None, 'A')], 'chem-4-3', 'reducing-ozone-depletion', [
    C.lifted('r-1', _q11ca2[2].text, 4)], qtext=cut(_a2, 'How have humans'), stem=_a_lead,
    cid='q11-c-a-ozone-depletion', ref_suffix='after (ii), ozone depletion')
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-3-5', 'why-gold-is-used-in-jewellery')
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-3-5', 'the-metal-that-corrodes-most-readily')
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-3-5', 'rusting-and-galvanising', figure=FIG + 'paper-q11c-b')
C.fixed([ka('11', 'c', 'iv', 'B')], 'chem-4-3', 'why-recycle-aluminium', skip=('Blank Page',))


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
    letters in subtotals ("(13)" then "(12)"), so the sum of every mark printed
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
