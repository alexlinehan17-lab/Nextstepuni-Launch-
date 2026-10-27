#!/usr/bin/env python3
"""2012 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2012_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2012_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2012_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2012 ol

No 2012 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The 2012 scheme prints Question 4's answers under "SECTION B" with no
"QUESTION 4" head, and its running footer "Chemistry ATGL 2012 Marking Scheme
Page Nof 15" on every page; chem_print reads the first as Q4's head and drops
the second (both gated to 2012 OL, Printed.__init__), without which Q4 to Q11
fell into Q3.

The paper sets several asks unnumbered inside one letter, each priced by a
cell of its own -- Q2(a), Q3(d) (after (ii), the heat of reaction), Q7(a),
Q10(b) and Q11(b)(iii) -- one card each, the later ones cited by what they ask.
It sets romans inside one sentence -- Q1(a) "Identify: (i) liquid X, (ii) solid
Y.", Q4(d), Q5(a) "Define (i) atom, (ii) molecule.", Q9(a) and Q9(b) -- which
the scheme numbers; the cards follow the scheme's cells and take the paper's
sentence as their question. The paper underlines the term Q3(a) and Q8(a) ask
about, prints Q5(b)'s and Q11(c)B(i)'s tables to be filled in, Q10(c)'s passage
with numbered blanks and Q11(b)'s equilibrium with an arrow the text layer
cannot read: those take the paper's own print as their question, as do
Q10(a)(ii)-(iii) (the table they plot and read) and Q11(b)(ii). Q4(k) and Q11(c)
offer whole alternative parts A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN, point)

P = Printed(2012, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2012-OL-'
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
        raise Refused(f'"{text}" is not in the 2012 ol scheme')
    return text


def cut(text, start=None, end=None):
    """The part of `text` from `start` (inclusive) up to `end` (exclusive), each
    asserted to be in it: a sentence lifted out of the paper's print."""
    a = text.index(start) if start else 0
    b = text.index(end, a) if end else len(text)
    return text[a:b].strip()


def adds(asides):
    return ('The scheme adds: ' + ' '.join(asides)) if asides else ''


def lift(rid, text, marks, note=''):
    """A scheme answer lifted as a row, refused unless the gate finds it."""
    return C.lifted(rid, display(text).strip(), marks, note)


def bare(text):
    """An answer less the double solidus the scheme sets after it."""
    assert text.endswith(' //'), text
    return text[:-len(' //')]


def options(texts):
    """Menu options lifted from the scheme, each refused unless the gate finds it."""
    return [lift('x', t, None)['verbatim'] for t in texts]


def split_points(text):
    """The points a scheme row separates with a double solidus, as printed."""
    return [x.strip() for x in text.split('//') if x.strip()]


_RAW = read_lines(P.scheme_path)


def raw_lines(page, rect):
    """The scheme's own printed lines inside a region of a page, in reading order."""
    x0, y0, x1, y1 = rect
    return [display(l.text) for l in _RAW if l.page == page and l.x0 >= x0 and l.y0 >= y0
            and l.x1 <= x1 and l.y1 <= y1]


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Ethene and ethyne ─────────────────────────────────────────────────────
Q1 = FIG + 'paper-q1'
# (a): "Identify: (i) liquid X, (ii) solid Y." is one sentence (paper page 2, the
# romans inside it, which the paper reader keeps as one ask); the scheme numbers
# the two answers and prices them together (5 + 3).
_q1a = P.ask(k('1', 'a'))
assert _q1a.endswith('Identify: (i) liquid X, (ii) solid Y.'), _q1a
assert [cells(k('1', 'a', r)) for r in ('i', 'ii')] == [[None], ['[5 + 3]']]
C._criteria = []
_q1a_rows, _q1a_cell = C.split([k('1', 'a', 'i'), k('1', 'a', 'ii')], notes={0: 'For (i), liquid X.',
                                                                            1: 'For (ii), solid Y.'})
assert _q1a_cell == '[5 + 3]' and len(_q1a_rows) == 2, (_q1a_rows, _q1a_cell)
C.add([k('1', 'a')], 'chem-u2', 'reagents-for-preparing-ethene', _q1a_rows, kind='orderedSplit',
      notation=_q1a_cell, total=8, notes=SPLIT.format('(5 + 3)'), figure=Q1)
# (b): the prevention, two points (2 × 3), then the risk (6).
assert cells(k('1', 'b')) == ['[2 × 3]', '[6]'], P.items(k('1', 'b'))
C.fixed([k('1', 'b')], 'chem-u2', 'preventing-suck-back', figure=Q1,
        row_notes={0: 'For "How would you prevent a ‘suck-back’ ...?"',
                   2: 'For "What risk does a ‘suck-back’ present?"'})
C.fixed([k('1', 'c')], 'chem-4-2', 'dehydration-of-ethanol-to-ethene', figure=Q1)
# (d): the scheme draws the apparatus (its labels "water", "CaC₂", "water" are
# the picture's, 'scheme-labels') and prices four points "ANY THREE: (6 + 2 ×
# 3)": any three, the first (6), the others (3).
_q1d = P.items(k('1', 'd'))
assert [(it.cell, it.asides) for it in _q1d] == [
    ('[6 + 2 × 3]', ['[any three]', '[Absence of diagram lose 3 marks]'])], _q1d
assert len(_q1d[0].options()) == 4, _q1d[0].options()
C.menu([k('1', 'd')], 'chem-u2', 'preparing-and-collecting-ethyne', figure=S + 'q1d',
       note='Any three of these, the first (6), the others (3): the scheme lists four points and prices them "'
            + traced('ANY THREE: (6 + 2 × 3)') + '".',
       notes='The scheme draws the labelled apparatus; its own print is shown with the answer.')
assert cells(k('1', 'e')) == ['[6 + 2 × 3]'], P.items(k('1', 'e'))
C.ordered([k('1', 'e')], 'chem-2-4', 'unsaturation-and-a-test-for-it',
          row_notes={0: 'For "Explain what is meant by saying that ethene and ethyne are unsaturated compounds."',
                     1: 'For the test: the reagent.', 2: 'For what is seen.'})

# ── Q2 Volumetric glassware and a titration ──────────────────────────────────
Q2 = FIG + 'paper-q2'
# (a): two asks under one printed mark (11), a cell each: the names (5 + 3), then
# why C (3).
_q2a_ask = P.ask(k('2', 'a'))
_q2a = P.items(k('2', 'a'))
assert [it.cell for it in _q2a] == ['[5 + 3]', '[3]'], _q2a
_names = _q2a[0].points()
assert _names == ['A pipette', 'B burette'], _names
C.add([k('2', 'a')], 'chem-4-1', 'the-pipette-and-burette', [
    lift('r-1', _names[0], None, 'For A.'), lift('r-2', _names[1], None, 'For B.')],
    kind='orderedSplit', notation='[5 + 3]', total=8, notes=SPLIT.format('(5 + 3)'),
    qtext=cut(_q2a_ask, None, 'Why is it'), figure=Q2)
C.add([k('2', 'a')], 'chem-4-1', 'why-use-a-pipette-filler', [lift('r-1', _q2a[1].text, 3)],
      qtext=cut(_q2a_ask, 'Why is it'), figure=Q2, cid='q2-a-why-c', ref_suffix='why C')
# (b): three points under the cell "(6) (2 × 3)" (scheme PDF page 6, x 469, y 270),
# which the reader reads as its last term: (6 + 2 × 3), as the scheme's outline
# prints it, without saying which point earns which.
_q2b = P.items(k('2', 'b'))
assert [it.cell for it in _q2b] == ['[2 × 3]'], _q2b
_rinse = _q2b[0].points()
assert _rinse == ['with deionised (distilled, pure)', 'water', 'with a little of the solution to be measured'], _rinse
C.add([k('2', 'b')], 'chem-4-1', 'rinsing-the-pipette-and-burette', [
    lift(f'r-{i + 1}', t, None) for i, t in enumerate(_rinse)],
    kind='orderedSplit', notation='[6 + 2 × 3]', total=12,
    notes=SPLIT.format('"' + traced('(6) (2 × 3)') + '"'), figure=Q2)
C.fixed([k('2', 'c')], 'chem-4-1', 'the-last-drop-in-the-pipette', figure=Q2)
# (d)-(f): the titration the paper prints after (c) is their lead-in.
Q2_TITRATION = P.lead(k('2', 'c'))
assert Q2_TITRATION.startswith('Using A, B and C, and some other pieces of equipment') \
    and Q2_TITRATION.endswith('HCl + NaOH → NaCl + H₂O'), Q2_TITRATION
C.fixed([k('2', 'd')], 'chem-4-1', 'other-titration-equipment', stem=Q2_TITRATION)
# (e): the indicator (3), then its colour change "initial colour // final colour"
# (2 × 3), over a table of nine indicators and their colours (scheme PDF page 6):
# the indicators are the first row's menu; the colours are the scheme's
# criteria, each indicator's in its table, shown with the answer.
_q2e = P.items(k('2', 'e'))
assert [(it.cell, it.text) for it in _q2e[:2]] == [('[3]', 'name of suitable indicator'),
                                                    ('[2 × 3]', 'initial colour // final colour')] \
    and _q2e[2].cell is None and len(_q2e) == 3, _q2e
_indicators = list(dict.fromkeys(raw_lines(6, (145, 497, 240, 615))))
assert _indicators == ['methyl orange', 'methyl red', 'phenolphthalein', 'bromothymol blue', 'cresol purple',
                       'neutral red', 'phenol red', 'thymolphthalein'], _indicators
_colour = split_points(_q2e[1].text)
C.add([k('2', 'e')], 'chem-4-1', 'indicator-and-colour-change-for-a-titration', [
    anyN('r-1', options(_indicators)[0], 3, 1, 3, options(_indicators),
         'For the indicator, any one of these: the scheme prices "' + traced(_q2e[0].text) + '" (3) and tables '
         'these indicators with their colours.'),
    lift('r-2', _colour[0], 3, 'For the colour change: the scheme prices "' + traced(_q2e[1].text) + '" (2 × 3), '
         'one each, and tables each indicator\'s colour before and after the end point, shown with the answer.'),
    lift('r-3', _colour[1], 3, adds(_q2e[1].asides))], total=9, figure=S + 'q2e', stem=Q2_TITRATION)
# (f): the answer (9), then its working in a box (3) a step: the scheme's print of
# the working is the figure.
assert cells(k('2', 'f')) == ['[9]', '[3]', '[3]'], P.items(k('2', 'f'))
C.answer_only([k('2', 'f')], 'chem-4-1', 'concentration-of-sodium-hydroxide-in-moles-per-litre', S + 'q2f',
              stem=Q2_TITRATION)

# ── Q3 The heat of reaction of hydrochloric acid and sodium hydroxide ────────
Q3 = FIG + 'paper-q3'
# (a): the paper underlines "heat of reaction" in the question's opening sentence.
assert cells(k('3', 'a')) == ['[5 + 3]'], P.items(k('3', 'a'))
C.ordered([k('3', 'a')], 'chem-3-1', 'heat-of-reaction')
print_question('paper-q3a-print')
assert cells(k('3', 'b')) == ['[6 + 3]'], P.items(k('3', 'b'))
C.ordered([k('3', 'b')], 'chem-3-1', 'exothermic-reactions', figure=Q3,
          row_notes={0: 'For "What is an exothermic reaction?"', 1: 'For the evidence.'})
assert cells(k('3', 'c')) == ['[2 × 3]', '[3]'], P.items(k('3', 'c'))
C.fixed([k('3', 'c')], 'chem-3-1', 'minimising-heat-loss-in-the-polystyrene-cup', figure=Q3,
        row_notes={0: 'For "Indicate two features of the apparatus ...".',
                   2: 'For "In the case of either feature, explain how it does this."'})
# (d)(i)-(ii): each answer priced for the whole part, its working set as
# fractions in a box (scheme PDF page 7), shown with the answer.
assert cells(k('3', 'd', 'i')) == ['[9]', '[6]', '[3]'], P.items(k('3', 'd', 'i'))
C.answer_only([k('3', 'd', 'i')], 'chem-3-1', 'moles-of-hydrochloric-acid', S + 'q3d-i')
_q3d2_ask = P.ask(k('3', 'd', 'ii'))
_q3d2 = P.items(k('3', 'd', 'ii'))
assert [it.cell for it in _q3d2] == ['[6]', '[3]', '[3]', '[3]'] \
    and display(_q3d2[3].text) == 'ΔH – 57 kJ mol⁻¹', _q3d2
C.answer_only([k('3', 'd', 'ii')], 'chem-3-1', 'heat-produced-per-mole-of-hydrochloric-acid', S + 'q3d-ii',
              qtext=cut(_q3d2_ask, None, 'What is the heat'))
# Then, set after (ii) under the letter's one mark (18), the heat of reaction:
# the scheme sets it under "ΔH" (3).
C.add([k('3', 'd')], 'chem-3-1', 'heat-of-reaction-of-hydrochloric-acid-and-sodium-hydroxide', [
    lift('r-1', '– 57 kJ mol⁻¹', 3, 'The scheme sets it under "ΔH".')],
    qtext=cut(_q3d2_ask, 'What is the heat'), cid='q3-d-heat-of-reaction', figure=Q3,
    ref_suffix='after (ii), the heat of reaction')
C.fixed([k('3', 'e')], 'chem-u2', 'corrosive-hazard-pictogram', figure=FIG + 'paper-q3e')

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-1', 'three-states-of-matter', notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-2', 'identifying-an-element-from-its-shells', notes=Q4_NOTE,
        figure=FIG + 'paper-q4b')
assert cells(k('4', 'c')) == ['[2 × 3]'], P.items(k('4', 'c'))
C.fixed([k('4', 'c')], 'chem-1-1', 'chemical-compound', notes=Q4_NOTE)
# (d): "What colour is given to the Bunsen flame by (i) a lithium salt, (ii) a
# copper salt?" is one sentence; the scheme numbers the two answers and prices
# them (2 × 3), one each.
_q4d1, _q4d2 = P.items(k('4', 'd', 'i')), P.items(k('4', 'd', 'ii'))
assert [it.cell for it in _q4d1] == [None] and [it.cell for it in _q4d2] == ['[2 × 3]'], (_q4d1, _q4d2)
C.add([k('4', 'd')], 'chem-1-2', 'flame-colours-of-lithium-and-copper', [
    lift('r-1', bare(_q4d1[0].text), 3, 'For (i). The scheme prices these two answers (2 × 3), one each.'),
    lift('r-2', _q4d2[0].text, 3, 'For (ii).')], qtext=P.ask(k('4', 'd'), deep=True), notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-2-1', 'electronegativity', notes=Q4_NOTE)
C.fixed([k('4', 'f')], 'chem-u2', 'brown-ring-test-reagents', notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-2-2', 'a-charged-rod-and-a-stream-of-water', notes=Q4_NOTE, figure=FIG + 'paper-q4g')
# (h): "pyramidal /" and a drawing of the molecule, priced (6).
C.fixed([k('4', 'h')], 'chem-2-2', 'shape-of-the-ammonia-molecule', figure=S + 'q4h',
        notes='The scheme also accepts the molecule drawn, as it draws it; its own print is shown with the answer. '
              + Q4_NOTE)
# (i): the scheme prints no mark beside "16 g" (scheme PDF page 8, the only item
# of the page without one); its rubric allots six marks to each item, and its
# outline prices the item "(6)".
_q4i = P.items(k('4', 'i'))
assert [(it.cell, it.text) for it in _q4i] == [(None, '16 g')], _q4i
C.add([k('4', 'i')], 'chem-1-4', 'mass-of-oxygen-gas-at-stp', [
    lift('r-1', _q4i[0].text, 6, 'The scheme prints no mark beside this answer: its rubric allots six to each item, '
         'and its outline prices the item "' + traced('(i) (6)') + '". ' + adds(_q4i[0].asides))], notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-1-2', 'uses-of-the-mass-spectrometer', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-u3', 'co-product', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-2-1', 'x-ray-crystallography', notes=Q4_NOTE, figure=FIG + 'paper-q4k-b')

# ── Q5 Atoms, molecules and subatomic particles ──────────────────────────────
# (a): "Define (i) atom, (ii) molecule." is one sentence; the scheme numbers the
# two definitions and prices them together (5 + 3).
assert [cells(k('5', 'a', r)) for r in ('i', 'ii')] == [[None], ['[5 + 3]']]
C._criteria = []
_q5a_rows, _q5a_cell = C.split([k('5', 'a', 'i'), k('5', 'a', 'ii')], notes={0: 'For (i).', 1: 'For (ii).'})
assert _q5a_cell == '[5 + 3]' and len(_q5a_rows) == 2, (_q5a_rows, _q5a_cell)
C.add([k('5', 'a')], 'chem-1-1', 'atoms-and-molecules', _q5a_rows, kind='orderedSplit', notation=_q5a_cell,
      total=8, notes=SPLIT.format('(5 + 3)'))
# (b): the scheme fills in the table, a mark (3) beside each of its seven
# entries, "(7 × 3)" (scheme PDF page 9): one menu of all seven, three each (a
# fixed card holds at most five rows). The table to fill in is the paper's print.
assert cells(k('5', 'b'))[0] == '[7 × 3]', P.items(k('5', 'b'))
_table5 = ['electron', '0.0005 to 0.00056*', 'cloud / shell(s) / outside nucleus', 'neutron', 'nucleus', '1',
           '1 / +1 / +']
assert raw_lines(9, (100, 245, 495, 315)) == [
    'PARTICLE', 'RELATIVE MASS', 'RELATIVE CHARGE', 'LOCATION', 'electron (3)', '0.0005 to 0.00056* (3)', '–1',
    'cloud / shell(s) /', 'outside nucleus (3)', 'neutron (3)', '1', '0', 'nucleus (3)', 'proton', '1 (3)',
    '1 / +1 / + (3)', 'nucleus']
_footnote5 = display(P.items(k('5', 'b'))[-1].text)
assert _footnote5 == '* 1/2000 to 1/1800 [Accept “negligible”]', _footnote5
C.add([k('5', 'b')], 'chem-1-2', 'mass-charge-and-location-of-subatomic-particles', [anyN(
    'r-1', options(_table5)[0], 21, 7, 3, options(_table5),
    'All seven entries the scheme fills in, three each, in its table\'s order: the electron\'s name, relative mass '
    'and location; the neutron\'s name and location; the proton\'s relative mass and relative charge. Its own '
    'print of the completed table is shown with the answer. The scheme adds: "' + traced(_footnote5) + '"')],
    total=21, figure=S + 'q5b')
print_question('paper-q5b-print')
# (c): two points, "it has one proton only // it has no neutron", priced (6): a
# cell pricing fewer points than the scheme lists is a choice, either of them.
_q5c = P.items(k('5', 'c'))
assert [it.cell for it in _q5c] == ['[6]'], _q5c
_q5c_opts = options(split_points(_q5c[0].text))
assert len(_q5c_opts) == 2, _q5c_opts
C.add([k('5', 'c')], 'chem-1-2', 'composition-of-the-hydrogen-nucleus', [anyN(
    'r-1', _q5c_opts[0], 6, 1, 6, _q5c_opts, 'Either of these: the scheme lists two points and prices the part (6).')],
    total=6)
assert cells(k('5', 'd')) == ['[2 × 3]', '[3]'], P.items(k('5', 'd'))
C.fixed([k('5', 'd')], 'chem-1-2', 'carbon-12-and-carbon-14',
        row_notes={0: 'For the two ways in which they are similar.', 2: 'For the way in which they differ.'})
C.fixed([k('5', 'e')], 'chem-1-2', 'rutherford-and-the-nucleus', figure=FIG + 'paper-q5e')

# ── Q6 Crude oil, octane numbers and benzene ─────────────────────────────────
C.fixed([k('6', 'a')], 'chem-2-4', 'hydrocarbons')
# (b): any two of six fractions "ANY TWO: (6 + 3)", then a use of each, any two of
# the six fractions' uses (2 × 3).
_q6b = P.items(k('6', 'b'))
assert [(it.cell, it.asides) for it in _q6b] == [('[6 + 3]', ['[any two]']), ('[2 × 3]', [])], _q6b
_fractions = options(_q6b[0].options())
assert len(_fractions) == 6, _fractions
_uses_raw = split_points(_q6b[1].text)
_must = '[The two uses must correspond to the two named fractions, one for each fraction.]'
assert len(_uses_raw) == 6 and _uses_raw[5].endswith(' ' + _must), _uses_raw
_uses = options(_uses_raw[:5] + [_uses_raw[5][:-len(' ' + _must)]])
C.add([k('6', 'b')], 'chem-2-4', 'fractions-of-crude-oil-and-their-uses', [
    anyN('r-1', _fractions[0], 9, 2, 6, _fractions, 'For "Name any two of the fractions ...": any two of these, the '
         'first (6) and the second (3); the scheme prices them "' + traced('ANY TWO: (6 + 3)') + '".', steps=[6, 3]),
    anyN('r-2', _uses[0], 6, 2, 3, _uses, 'For "Give one use of each fraction you have named.": a use of each of '
         'the two fractions named, (2 × 3). The scheme adds: ' + traced(_must))], total=15)
# (c)(i)-(iii): four answers -- the two octane numbers, a structural formula and a
# way to raise the octane number -- priced together "ANY FOUR: (2 × 6 + 2 × 3)"
# beside (iii) (scheme PDF page 10). (ii)'s formula is written two ways and drawn
# four (its drawings are the picture's, 'scheme-labels'): the written formulae
# are the row, the drawings shown with the answer.
_q6c = [k('6', 'c', r) for r in ('i', 'ii', 'iii')]
_q6c_its = [P.items(x) for x in _q6c]
assert [[it.cell for it in x] for x in _q6c_its] == [[None], [None], ['[2 × 6 + 2 × 3]']], _q6c_its
_octane = _q6c_its[0][0].points()
assert _octane == ['heptane: 0', '2,2,4-trimethylpentane: 100'], _octane
_heptane = _q6c_its[1][0].points()
assert _heptane == ['CH₃CH₂CH₂CH₂CH₂CH₂CH₃ / CH₃(CH₂)₅CH₃'], _heptane
_ways = _q6c_its[2][0].points()
assert len(_ways) == 1 and _ways[0].startswith('isomerisation / reforming'), _ways
C.add(_q6c, 'chem-2-4', 'octane-numbers', [
    lift('r-1', _octane[0], None, 'For (i).'),
    lift('r-2', _octane[1], None, 'For (i).'),
    lift('r-3', _heptane[0], None, 'For (ii). The scheme also accepts the structures it draws, displayed and '
         'skeletal, for heptane and for 2,2,4-trimethylpentane; its own print is shown with the answer.'),
    lift('r-4', _ways[0], None, 'For (iii).')],
    kind='orderedSplit', notation='[2 × 6 + 2 × 3]', total=18,
    notes=SPLIT.format('"' + traced('ANY FOUR: (2 × 6 + 2 × 3)') + '"'), figure=S + 'q6c-ii')
# (d)(i)-(ii): the structure of benzene, which the scheme draws three ways
# (scheme-art), and the health concern, priced together (9 + 3).
assert [cells(k('6', 'd', r)) for r in ('i', 'ii')] == [[], ['[9 + 3]']], [P.items(k('6', 'd', r))
                                                                            for r in ('i', 'ii')]
C.add([k('6', 'd', 'i'), k('6', 'd', 'ii')], 'chem-2-4', 'benzene-and-its-health-concern', [
    C.mark_ask(point('r-1', P.ask(k('6', 'd', 'i')), None, 'For (i). ' + DRAWN)),
    lift('r-2', P.items(k('6', 'd', 'ii'))[0].text, None, 'For (ii).')],
    kind='orderedSplit', notation='[9 + 3]', total=12, notes=SPLIT.format('(9 + 3)'), figure=S + 'q6d-i')

# ── Q7 pH and water treatment ────────────────────────────────────────────────
C.fixed([k('7', 'a')], 'chem-3-4', 'definition-of-ph')
# (a)(i): the answer (6), then the working set out two ways side by side in a box
# (scheme PDF page 11), (3) a step: the left route (pOH) is the rows, the right
# route quoted, both routes' print shown with the answer.
Q7A_LEAD = P.lead(k('7', 'a'))
assert Q7A_LEAD == 'Calculate the pH of:', Q7A_LEAD
_q7a1 = P.items(k('7', 'a', 'i'))
assert [(it.cell, display(it.text)) for it in _q7a1] == [
    ('[6]', '12'), ('[3]', 'pOH = – log 0.01 / = 2'), ('[3]', '[H⁺] = 10⁻¹⁴ ÷ 0.01 = 10⁻¹²'),
    ('[3]', 'pH = 14 – 2 / = 12'), ('[3]', 'pH = – log 10⁻¹² = 12')], _q7a1
C.add([k('7', 'a', 'i')], 'chem-3-4', 'ph-of-a-sodium-hydroxide-solution', [
    lift('r-1', _q7a1[1].text, 3),
    lift('r-2', _q7a1[3].text, 3, 'Or by the scheme\'s second route: "' + traced(display(_q7a1[2].text))
         + '" (3), then "' + traced(display(_q7a1[4].text)) + '" (3).')],
    stem=Q7A_LEAD, figure=S + 'q7a-i',
    notes='The scheme gives the answer, 12, priced (6), then the working that earns it, step by step; the steps here '
          'are its first route, and its own print of both routes is shown with the answer.')
assert cells(k('7', 'a', 'ii')) == ['[6]', '[3]', '[3]'], P.items(k('7', 'a', 'ii'))
C.route([k('7', 'a', 'ii')], 'chem-3-4', 'ph-of-a-hydrochloric-acid-solution', stem=Q7A_LEAD)
assert [cells(k('7', 'b', r)) for r in ('i', 'ii')] == [[None], ['[6 + 3]']]
C.ordered([k('7', 'b', 'i'), k('7', 'b', 'ii')], 'chem-4-3', 'adjusting-the-ph-of-drinking-water',
          row_notes={0: 'For (i).', 1: 'For (ii).'})
C.fixed([k('7', 'c')], 'chem-4-3', 'flocculation',
        row_notes={0: 'For the flocculating agent.', 1: 'For how it helps.'})
C.fixed([k('7', 'd', 'i')], 'chem-4-3', 'hardness-of-water')
C.fixed([k('7', 'd', 'ii')], 'chem-4-3', 'temporary-and-permanent-hardness')
C.fixed([k('7', 'd', 'iii')], 'chem-4-3', 'advantages-and-disadvantages-of-hard-water')

# ── Q8 Alkanes, alcohols and carboxylic acids ────────────────────────────────
# (a): the paper underlines "homologous series"; the scheme prices six points
# "ANY TWO: (5 + 3)", the label printed at the end of the last point's line.
_q8a = P.items(k('8', 'a'))
assert [(it.cell, it.asides) for it in _q8a] == [
    ('[5 + 3]', ['[Accept “uniform chemical type” for “similar chemical properties.”]'])], _q8a
_series = split_points(_q8a[0].text)
assert len(_series) == 6 and _series[5] == 'similar preparation ANY TWO:', _series
_series = options(_series[:5] + ['similar preparation'])
C.add([k('8', 'a')], 'chem-2-4', 'homologous-series', [anyN(
    'r-1', _series[0], 8, 2, 5, _series, 'Any two of these, the first (5) and the second (3): the scheme lists six '
    'points and prices them "' + traced('ANY TWO: (5 + 3)') + '". ' + adds(_q8a[0].asides), steps=[5, 3])], total=8)
print_question('paper-q8a-print')
# (b): "name 1 // name 2" and "structure 1 // structure 2", priced together (2 × 6
# + 2 × 3), with examples in a box (scheme PDF page 12): the scheme prints only
# what each point is, which are the rows; its examples are shown with the answer.
_q8b = P.items(k('8', 'b'))
assert [it.cell for it in _q8b] == ['[2 × 6 + 2 × 3]', None] and _q8b[1].text.startswith('Examples'), _q8b
_q8b_pts = split_points(' // '.join(r.text for r in _q8b[0].rows if r.text))
assert _q8b_pts == ['name 1', 'name 2', 'structure 1', 'structure 2'], _q8b_pts
C.add([k('8', 'b')], 'chem-4-2', 'naming-and-drawing-an-alkane-an-alcohol-and-an-acid', [
    lift('r-1', _q8b_pts[0], None, 'The name of one member of the first series chosen.'),
    lift('r-2', _q8b_pts[1], None, 'The name of one member of the second.'),
    lift('r-3', _q8b_pts[2], None, 'The structural formula of the first.'),
    lift('r-4', _q8b_pts[3], None, 'The structural formula of the second. ' + adds(_q8b[0].asides))],
    kind='orderedSplit', notation='[2 × 6 + 2 × 3]', total=18,
    notes=SPLIT.format('(2 × 6 + 2 × 3)') + ' The scheme prints only what each point is, and examples of each '
                                           'series in a box, shown with the answer.', figure=S + 'q8b')
# (c): "use of 1 // use of 2" (2 × 3), with the uses of each compound in a box
# beneath, which repeats the cell (2 × 3) (scheme PDF page 12).
_q8c = P.items(k('8', 'c'))
assert [it.cell for it in _q8c] == ['[2 × 3]', '[2 × 3]'] and _q8c[1].text.startswith('Uses:'), _q8c
_q8c_pts = split_points(_q8c[0].text)
assert _q8c_pts == ['use of 1', 'use of 2'], _q8c_pts
C.add([k('8', 'c')], 'chem-4-2', 'uses-of-alkanes-alcohols-and-acids', [
    lift('r-1', _q8c_pts[0], 3, 'A use of the first compound named in (b). The scheme prices these two points '
         '(2 × 3), one each.'),
    lift('r-2', _q8c_pts[1], 3, 'A use of the second. ' + adds(_q8c[1].asides))],
    notes='The scheme prints only what each point is, and the uses of each compound in a box, shown with the answer.',
    figure=S + 'q8c')
C.fixed([k('8', 'd')], 'chem-4-2', 'oxidising-alcohols-to-carboxylic-acids')
assert cells(k('8', 'e')) == ['[6]', '[2 × 3]'], P.items(k('8', 'e'))
C.fixed([k('8', 'e')], 'chem-4-2', 'carbon-dioxide-and-the-limewater-test',
        row_notes={0: 'For the gas.', 1: 'For the test.'})

# ── Q9 Oxidation, reduction and bonding ──────────────────────────────────────
# (a): "Define (i) oxidation, (ii) reduction, ..." is one sentence; the scheme
# numbers the two and prices them together (5 + 3).
assert [cells(k('9', 'a', r)) for r in ('i', 'ii')] == [[None], ['[5 + 3]']]
C._criteria = []
_q9a_rows, _q9a_cell = C.split([k('9', 'a', 'i'), k('9', 'a', 'ii')], notes={0: 'For (i).', 1: 'For (ii).'})
assert _q9a_cell == '[5 + 3]' and len(_q9a_rows) == 2, (_q9a_rows, _q9a_cell)
C.add([k('9', 'a')], 'chem-3-5', 'oxidation-and-reduction-by-electron-transfer', _q9a_rows, kind='orderedSplit',
      notation=_q9a_cell, total=8, notes=SPLIT.format('(5 + 3)'))
# (b): "Identify (i) ..., (ii) ..." is one sentence; the scheme numbers the two and
# prices them (2 × 3), one each.
_q9b1, _q9b2 = P.items(k('9', 'b', 'i')), P.items(k('9', 'b', 'ii'))
assert [it.cell for it in _q9b1] == [None] and [it.cell for it in _q9b2] == ['[2 × 3]'], (_q9b1, _q9b2)
assert _q9b2[0].text == 'chlorine / Cl₂ / ½Cl₂ [Accept Cl.]', _q9b2
C.add([k('9', 'b')], 'chem-3-5', 'substance-oxidised-and-oxidising-agent', [
    lift('r-1', bare(_q9b1[0].text), 3, 'For (i). The scheme prices these two answers (2 × 3), one each.'),
    lift('r-2', 'chlorine / Cl₂ / ½Cl₂', 3, 'For (ii). The scheme adds: ' + traced('[Accept Cl.]'))])


def bond_card(letter, concept, topic, notes):
    """Q9(c) and (d): the bond (3), an example (3), then two properties, "ANY TWO:
    (2 × 3)" of those the scheme lists."""
    its = P.items(k('9', letter))
    assert [(it.cell, [a for a in it.asides if a == '[any two]']) for it in its] == [
        ('[3]', []), ('[3]', []), ('[2 × 3]', ['[any two]'])], its
    props = options(its[2].options())
    return C.add([k('9', letter)], topic, concept, [
        lift('r-1', its[0].text, 3, notes[0]),
        lift('r-2', its[1].text, 3, ' '.join(x for x in [notes[1], adds(its[1].asides)] if x)),
        anyN('r-3', props[0], 6, 2, 3, props, notes[2] + ': any two of these; the scheme prices them "'
             + traced('ANY TWO: (2 × 3)') + '".')], total=12)


bond_card('c', 'covalent-bonding-in-chlorine', 'chem-2-1',
          ('For the type of bond.', 'For the other example.', 'For the two properties'))
bond_card('d', 'ionic-bonding-in-sodium-chloride', 'chem-2-1',
          ('For the type of bonding.', 'For the other example.', 'For the two properties'))
# (e): what is seen, "ANY TWO: (2 × 3)" of seven points, then a product (6).
_q9e = P.items(k('9', 'e'))
assert [(it.cell, it.asides) for it in _q9e] == [('[2 × 3]', ['[any two]']), ('[6]', [])], _q9e
_seen = options(_q9e[0].options())
assert len(_seen) == 7, _seen
_product = _q9e[1].text
assert _product == 'sodium hydroxide (caustic soda) / hydrogen [Accept formula.]', _product
C.add([k('9', 'e')], 'chem-1-3', 'sodium-and-water', [
    anyN('r-1', _seen[0], 6, 2, 3, _seen, 'For "Describe what you would observe ...": any two of these; the scheme '
         'prices them "' + traced('ANY TWO: (2 × 3)') + '".'),
    lift('r-2', 'sodium hydroxide (caustic soda) / hydrogen', 6,
         'For "Name one product of the reaction that occurs." The scheme adds: ' + traced('[Accept formula.]'))],
    total=12)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q10A = FIG + 'paper-q10a'
# (a)(i): the name and the formula, "hydrogen peroxide // H₂O₂" on one row,
# priced together (4 + 3).
_q10a1 = P.items(k('10', 'a', 'i'))
assert [it.cell for it in _q10a1] == ['[4 + 3]'], _q10a1
_x = split_points(_q10a1[0].text)
assert _x == ['hydrogen peroxide', 'H₂O₂'], _x
C.add([k('10', 'a', 'i')], 'chem-3-2', 'hydrogen-peroxide-and-its-formula', [
    lift('r-1', _x[0], None, 'For the name.'), lift('r-2', _x[1], None, 'For the formula.')],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'), figure=Q10A)
# (ii): the axes, "ANY TWO: (2 × 3)" of four points, then the points and the
# curve (2 × 3); the scheme's graph is shown with the answer and the table the
# graph plots is the paper's print.
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [(it.cell, it.asides) for it in _q10a2] == [
    ('[2 × 3]', ['[Accept “time” or “min” & “vol” or “cm³.”]', '[any two]']), ('[2 × 3]', [])], _q10a2
_axes = _q10a2[0].options()
assert len(_axes) == 4 and _axes[0] == 'See graph below. axes correctly labelled', _axes
_axes = options(['axes correctly labelled'] + _axes[1:])
_plot = split_points(_q10a2[1].text)
assert _plot == ['six points correctly plotted', 'curve correctly drawn'], _plot
C.add([k('10', 'a', 'ii')], 'chem-3-2', 'plotting-the-volume-of-oxygen-against-time', [
    anyN('r-1', _axes[0], 6, 2, 3, _axes, 'For the axes, any two of these: the scheme prices them "'
         + traced('ANY TWO: (2 × 3)') + '". The scheme adds: ' + traced(_q10a2[0].asides[0])),
    lift('r-2', _plot[0], 3, 'The scheme prices these two points (2 × 3), one each.'),
    lift('r-3', _plot[1], 3)], total=12, figure=S + 'q10a',
    notes='The scheme draws the graph ("' + traced('See graph below.') + '"); its own print is shown with the answer.')
print_question('paper-q10a-ii-print')
# (iii): the estimate (6); the scheme's next page opens "Question 10 continued/",
# which the reader files under this part.
_q10a3 = P.items(k('10', 'a', 'iii'))
assert [(it.cell, it.text) for it in _q10a3] == [('[6]', 'See graph below 58 to 62 cm³'),
                                                  (None, 'Question 10 continued/')], _q10a3
C.add([k('10', 'a', 'iii')], 'chem-3-2', 'reading-a-volume-from-the-graph', [
    lift('r-1', '58 to 62 cm³', 6, 'The scheme reads it off its graph ("' + traced('See graph below') + '"), shown '
         'with the answer.')], figure=S + 'q10a')
print_question('paper-q10a-iii-print')
# (b): four asks, each printed with its mark, (7), (6), (6), (6), and priced by a
# cell of its own (scheme PDF page 15): the definition (4 + 3), then three
# answers (6) each with its working, (3) a step.
_q10b_ask = P.ask(k('10', 'b'))
_q10b = P.items(k('10', 'b'))
assert [it.cell for it in _q10b] == ['[4 + 3]', '[6]', '[3]', '[3]', '[6]', '[3]', '[6]', '[3]'], _q10b
assert [display(it.text) for it in _q10b[1:]] == [
    '180', '6 × 12 + 12 + 6 × 16 / 72 + 12 + 96', '= 180', '6.6 to 6.7%', '12/180 (3) // × 100 (3) / = 6.6 to 6.7',
    '0.05 mol', '9/180 (3) = 0.05'], _q10b
_mr = _q10b[0].points()
assert len(_mr) == 2, _mr
C.add([k('10', 'b')], 'chem-1-4', 'relative-molecular-mass', [
    lift('r-1', _mr[0], None), lift('r-2', _mr[1], None)],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'),
    qtext=cut(_q10b_ask, None, 'Calculate the'), stem='')
C.add([k('10', 'b')], 'chem-1-4', 'relative-molecular-mass-of-glucose', [
    lift('r-1', _q10b[2].text, 3), lift('r-2', _q10b[3].text, 3)],
    qtext=cut(_q10b_ask, 'Calculate the', 'Find the'), stem='', cid='q10-b-mr-of-glucose',
    ref_suffix='the relative molecular mass of glucose',
    notes='The scheme gives the answer, 180, priced (6), then the working that earns it, step by step.')
# The percentage and the moles: each answer priced for its ask, its working (a
# fraction set in a box, (3) a step) shown with the answer.
WORKING = ('The scheme prices the answer for the whole ask and sets out the working that earns it, with the marks '
           'for each step, in a box; its own print is shown with the answer.')
C.add([k('10', 'b')], 'chem-1-4', 'percentage-of-hydrogen-in-glucose', [lift('r-1', _q10b[4].text, 6, WORKING)],
      qtext=cut(_q10b_ask, 'Find the', 'How many'), stem='', cid='q10-b-percentage-of-hydrogen',
      ref_suffix='the percentage of hydrogen', figure=S + 'q10b-percentage')
C.add([k('10', 'b')], 'chem-1-4', 'moles-of-glucose', [lift('r-1', _q10b[6].text, 6, WORKING)],
      qtext=cut(_q10b_ask, 'How many'), stem='', cid='q10-b-moles-of-glucose', ref_suffix='the moles of glucose',
      figure=S + 'q10b-moles')
# (c): five blanks priced "(3 × 6) + (1 × 4) + (1 × 3)" (the reader takes "(1 ×
# 3)" for the cell and the rest for words); the passage with its numbered blanks
# is the paper's print.
_q10c = P.items(k('10', 'c'))
assert [it.cell for it in _q10c] == ['[1 × 3]'], _q10c
_blanks = split_points(_q10c[0].text)
assert _blanks[:4] == ['1: The Greeks', '2: Boyle', '3: Davy', '4: Mendeleev'] \
    and _blanks[4] == '5: Moseley (3 × 6) + (1 × 4) +', _blanks
_cell10c = traced('(3 × 6) + (1 × 4) + (1 × 3)')
C.add([k('10', 'c')], 'chem-1-3', 'history-of-the-elements', [
    lift(f'r-{i + 1}', t, None) for i, t in enumerate(_blanks[:4] + ['5: Moseley'])],
    kind='orderedSplit', notation='[' + _cell10c + ']', total=25,
    notes=SPLIT.format('"' + _cell10c + '"') + ' Each answer is numbered by its blank.')
print_question('paper-q10c-print')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q11A = FIG + 'paper-q11a'
C.fixed([k('11', 'a', 'i')], 'chem-u2', 'steam-distillation', figure=Q11A)
assert [(it.cell, it.text) for it in P.items(k('11', 'a', 'ii'))] == [('[6]', 'condenser')]
C.fixed([k('11', 'a', 'ii')], 'chem-u2', 'the-condenser', figure=Q11A,
        label_key=[{'letter': 'X', 'meaning': 'condenser', 'askedInThisQuestion': True}])
C.fixed([k('11', 'a', 'iii')], 'chem-u2', 'cold-water-into-the-condenser', figure=Q11A)
C.fixed([k('11', 'a', 'iv')], 'chem-u2', 'the-safety-tube', figure=Q11A)
C.fixed([k('11', 'a', 'v')], 'chem-u2', 'a-substance-extracted-by-steam-distillation', figure=Q11A)
# (b): the equilibrium, its arrow a glyph the text layer cannot read, is the
# picture travelling with each ask.
Q11B = FIG + 'paper-q11b-eq'
Q11B_LEAD = P.ask(k('11', 'b'))
assert Q11B_LEAD == 'A stage in the manufacture of sulfuric acid involves the following equilibrium:', Q11B_LEAD
C.fixed([k('11', 'b', 'i')], 'chem-3-3', 'chemical-equilibrium', figure=Q11B)
# (ii): the scheme's answer is a fraction, its own print; the paper's print of the
# ask with the equilibrium is the question.
C.drawn([k('11', 'b', 'ii')], 'chem-3-3', 'kc-expression-for-sulfur-trioxide', S + 'q11b-ii')
print_question('paper-q11b-ii-print')
# (iii): two asks under one mark (12), a cell each: the principle, two points
# (2 × 3) in either of two wordings with "or" between (scheme PDF page 16), one
# menu per point; then the explanation (2 × 3).
_q11b3_ask = P.ask(k('11', 'b', 'iii'))
_q11b3 = P.items(k('11', 'b', 'iii'))
assert [it.cell for it in _q11b3] == ['[2 × 3]', '[2 × 3]', '[2 × 3]', None] \
    and _q11b3[3].text == 'Question 11 continued/', _q11b3
_lc1, _lc2 = split_points(_q11b3[0].text), split_points(_q11b3[1].text)
assert len(_lc1) == len(_lc2) == 2, (_lc1, _lc2)
assert raw_lines(16, (300, 476, 320, 493)) == ['or'], raw_lines(16, (300, 476, 320, 493))
C.add([k('11', 'b', 'iii')], 'chem-3-3', 'le-chateliers-principle', [
    anyN('r-1', options([_lc1[0], _lc2[0]])[0], 3, 1, 3, options([_lc1[0], _lc2[0]]),
         'Either wording: the scheme prints the principle twice, "or" between, each priced (2 × 3).'),
    anyN('r-2', options([_lc1[1], _lc2[1]])[0], 3, 1, 3, options([_lc1[1], _lc2[1]]), 'Either wording.')],
    total=6, qtext=cut(_q11b3_ask, None, 'Explain'), figure=Q11B)
_why = split_points(_q11b3[2].text)
assert len(_why) == 2, _why
C.add([k('11', 'b', 'iii')], 'chem-3-3', 'temperature-and-the-sulfur-trioxide-equilibrium', [
    lift('r-1', _why[0], 3, 'The scheme prices these two points (2 × 3), one each.'),
    lift('r-2', _why[1], 3, adds(_q11b3[2].asides))],
    qtext=cut(_q11b3_ask, 'Explain'), figure=Q11B, cid='q11-b-iii-explain', ref_suffix='explain')
# (c)A: the candidate's own case study. (i) prints only the criteria "name of main
# product // one important use" (4 + 3), which are the rows, as 2026 OL Q11(d)A.
assert cells(ka('11', 'c', 'i', 'A')) == ['[4 + 3]'], P.items(ka('11', 'c', 'i', 'A'))
C.ordered([ka('11', 'c', 'i', 'A')], 'chem-u3', 'main-product-of-an-industry-and-its-use',
          row_notes={0: 'The scheme prints only what the point is: the main product of the industry studied.',
                     1: 'The scheme prints only what the point is: an important use of that product.'})
# (ii): the location (3), a criterion, then "two reasons that are appropriate to
# the chosen location such as: ..." (2 × 3): any two of the scheme's six (its
# "etc." left out).
_ca2 = P.items(ka('11', 'c', 'ii', 'A'))
assert [(it.cell, it.text) for it in _ca2][0] == ('[3]', 'location') and _ca2[1].cell == '[2 × 3]', _ca2
_such = 'two reasons that are appropriate to the chosen location such as:'
_reasons = split_points(_ca2[1].text)
assert _reasons[0].startswith(_such + ' ') and _reasons[-1] == 'etc.' and len(_reasons) == 7, _reasons
_reasons = options([_reasons[0][len(_such) + 1:]] + _reasons[1:6])
C.add([ka('11', 'c', 'ii', 'A')], 'chem-u3', 'location-of-an-irish-chemical-industry', [
    lift('r-1', 'location', 3, 'For "Where in Ireland is the industry located?" The scheme prints only what the '
         'point is: the location of the industry studied.'),
    anyN('r-2', _reasons[0], 6, 2, 3, _reasons, 'For the two reasons, any two of these: the scheme prices "'
         + traced(_such) + '" (2 × 3), listing these and "etc."')], total=9)
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-u3', 'safety-in-the-chemical-industry')
C.fixed([ka('11', 'c', 'iv', 'A')], 'chem-u3', 'minimising-costs-in-the-chemical-industry')
# (c)B(i): the scheme fills in the table, metal then non-metal on each property's
# row, "(5 × 3)": a row each, three each. The table to fill in is the paper's
# print; the scheme's completed table is shown with the answer.
_cb1 = P.items(ka('11', 'c', 'i', 'B'))
assert [it.cell for it in _cb1] == ['[5 × 3]'], _cb1
_props = split_points(_cb1[0].text)
assert _props[0] == 'PROPERTY METALS NON-METALS Hardness hard / soft' and len(_props) == 5, _props
_props = ['Hardness hard / soft'] + _props[1:]
assert _props[1:] == ['Lustre yes / no', 'Conduction of heat yes / no', 'Conduction of electricity yes / no',
                      'Ductility yes / no'], _props
C.add([ka('11', 'c', 'i', 'B')], 'chem-1-3', 'properties-of-metals-and-non-metals', [
    lift(f'r-{i + 1}', t, 3, 'For the property\'s row: the metals\' entry, then the non-metals\'. The scheme prices '
         'the five rows (5 × 3), one each.' if i == 0 else '') for i, t in enumerate(_props)],
    figure=S + 'q11c-b-i', notes='The scheme\'s completed table is shown with the answer.')
print_question('paper-q11c-b-i-print')
assert cells(ka('11', 'c', 'ii', 'B')) == ['[2 × 3]', '[4]'], P.items(ka('11', 'c', 'ii', 'B'))
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-1-3', 'alloys',
        row_notes={0: 'For "What is an alloy?"', 2: 'For "Give one example."'})


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
    """Every letter's printed marks, alternatives apart: the paper prints Q7(a),
    Q10 and Q11's letters in subtotals ("(5)" then "(12)"), so the sum of every
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
