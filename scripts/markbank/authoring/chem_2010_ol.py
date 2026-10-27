#!/usr/bin/env python3
"""2010 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2010_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2010_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2010_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2010 ol

No 2010 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The 2010 paper sets each question's number in one run with its first words
("1. A group of students prepared ethene ...") or with its first letter ("9.
(a)"); chem_print reads the first as the head (split_heads, the sitting joining
OLD_OL_HEADS), without which the paper reader found no question at all. Its
scheme prints the running footer "page N of 13" in lower case on every page
(dropped, gated to 2010 OL, Printed.__init__).

The scheme sets no letters A and B under Q4(k) -- B's answers follow A's after
"or" -- and Q11(c)A's unnumbered last ask, "State two ways in which chemistry
benefits society." (7), is its "(iv)": each is read from the scheme's own items
below. Q2(d)'s cell is set as an aside, "[Any 2 (9 + 3)]".

The paper sets romans inside one sentence -- Q2(b) "Explain the terms (i)
standard solution, (ii) primary standard", Q5(b), Q6(a), Q7(a), Q7(b), Q8(b),
Q9(a) -- which the scheme numbers (or labels "N:", "H:"); the cards follow the
scheme's cells and take the paper's sentence as their question. Q5(a) and
Q9(a) hold several asks under marks of their own: one card each, the later
cited by what they ask. The paper prints Q4(i)'s equilibrium with an arrow the
text layer cannot read, Q3(b)'s ions with charges it splits, Q8(d)'s data in a
table and Q9(b) and Q11(b) as a passage and a table to complete: those take the
paper's own print as their question.

A cell that prices fewer points than the scheme lists is a choice: an any-N
menu at the cell's values, where the scheme says which value each earns, or
inside an unpriced split where it does not (Q2(b), Q6(c), Q6(d), Q8(b)).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN, point)

P = Printed(2010, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2010-OL-'
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


def rows(key, i=0):
    """The printed rows of the key's i-th scheme item, blank rows apart."""
    return [r.text for r in P.items(key)[i].rows if r.text]


def traced(text):
    """A string quoted from the scheme in a note, checked against the scheme."""
    if not P.traceable(text):
        raise Refused(f'"{text}" is not in the 2010 ol scheme')
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


def routed(row, route):
    """A row on one side of the scheme's "or": a student who claims a row of one
    route has the other route's rows locked (the session's mutually exclusive
    routes), so the two answers are both claimable and never mixed."""
    row['route'] = route
    return row


def bare(text):
    """An answer less the double solidus the scheme sets after it."""
    assert text.endswith('//'), text
    return text[:-2].rstrip()


def uncue(text, cue):
    """An answer less the scheme's cue ("Formula:", "Reag.:") set before it on
    its row, which the reader takes off only when it is set in capitals."""
    assert text.startswith(cue + ' '), (text, cue)
    traced(cue)
    return text[len(cue) + 1:]


def options(texts):
    """Menu options lifted from the scheme, each refused unless the gate finds it."""
    return [lift('x', t, None)['verbatim'] for t in texts]


def split_points(text):
    """The points a scheme row separates with a double solidus, as printed."""
    return [x.strip() for x in text.split('//') if x.strip()]


def menu(rid, opts, claim, per, note, steps=None, marks=None):
    """An any-N row over options lifted from the scheme."""
    total = marks if marks is not None else (sum(steps) if steps else claim * per)
    return anyN(rid, opts[0], total, claim, per, opts, note, steps=steps)


def null_menu(rid, opts, claim, note):
    """An any-N choice inside an unpriced split: no value of its own."""
    return {'id': rid, 'kind': 'anyN', 'verbatim': opts[0], 'marks': None, 'openList': True,
            'contextNote': note, 'group': {'claimMax': claim, 'options': opts}}


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + traced(_q4[0].text) + '"'

WITHDRAWN = {}

# ── Q1 Preparing ethene ──────────────────────────────────────────────────────
Q1 = FIG + 'paper-q1'
# (a): the name, then the formula under the cue "Formula:", priced (5 + 3).
assert rows(k('1', 'a')) == ['Ethanol', 'Formula: C₂H₅OH / CH₃CH₂OH'] and cells(k('1', 'a')) == ['[5 + 3]']
C.add([k('1', 'a')], 'chem-u2', 'ethanol-as-the-source-of-ethene', [
    lift('r-1', 'Ethanol', None, 'For the name.'),
    lift('r-2', uncue(rows(k('1', 'a'))[1], 'Formula:'), None, 'For the formula.')],
    kind='orderedSplit', notation='[5 + 3]', total=8, notes=SPLIT.format('(5 + 3)'), figure=Q1)
assert cells(k('1', 'b')) == ['[3]', '[3]'], P.items(k('1', 'b'))
C.fixed([k('1', 'b')], 'chem-u2', 'aluminium-oxide-in-preparing-ethene', figure=Q1,
        row_notes={0: 'For "Identify solid Y".', 1: 'For "describe its appearance".'})
# (c)(i)-(iii): the three positions, then "How was the liquid X kept ...?",
# printed after (iii) under the letter's one mark (15), priced together "[6 +
# (3 × 3)]" beside the last answer (scheme PDF page 5): four points, four terms.
_q1c = [P.items(k('1', 'c', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in x] for x in _q1c] == [[None], [None], ['[6 + (3 × 3)]']], _q1c
assert rows(k('1', 'c', 'iii')) == ['Under the solid', 'Glass wool'], _q1c
C.add([k('1', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-u2', 'setting-up-the-preparation-of-ethene', [
    lift('r-1', _q1c[0][0].text, None, 'For (i).'),
    lift('r-2', _q1c[1][0].text, None, 'For (ii).'),
    lift('r-3', 'Under the solid', None, 'For (iii).'),
    lift('r-4', 'Glass wool', None, 'For "How was the liquid X kept in its proper position ...?" The scheme sets '
         'it under the cue "' + traced('How:') + '".')],
    kind='orderedSplit', notation='[6 + (3 × 3)]', total=15, notes=SPLIT.format('[6 + (3 × 3)]'), figure=Q1)
# (d): the precaution and what could happen, priced (9 + 3), each under a cue.
_q1d = rows(k('1', 'd'))
assert cells(k('1', 'd')) == ['[9 + 3]'] and len(_q1d) == 2, _q1d
C.add([k('1', 'd')], 'chem-u2', 'preventing-suck-back', [
    lift('r-1', uncue(_q1d[0], 'What action:'), None, 'For "What precaution should have been taken ...?"'),
    lift('r-2', uncue(_q1d[1], 'What happens:'), None, 'For "What could have happened ...?"')],
    kind='orderedSplit', notation='[9 + 3]', total=12, notes=SPLIT.format('(9 + 3)'), figure=Q1)
# (e): three points, (3 × 3): the colour before // after, then what it shows.
_q1e = rows(k('1', 'e'))
assert cells(k('1', 'e')) == ['[3 × 3]'] and _q1e == [
    'What colour: Purple (pink) //', 'to colourless [Allow 3 for decolourises]', 'What info.: Unsaturated'], _q1e
C.add([k('1', 'e')], 'chem-2-4', 'test-for-unsaturation-with-permanganate', [
    lift('r-1', 'Purple (pink)', 3, 'For the colour change, its start. The scheme prices the three points (3 × 3), '
         'one each.'),
    lift('r-2', 'to colourless', 3, 'For the colour change, its end. The scheme adds: '
         + traced('[Allow 3 for decolourises]')),
    lift('r-3', uncue(_q1e[2], 'What info.:'), 3, 'For "What information does this test result give about '
         'ethene?"')], figure=Q1)

# ── Q2 A standard solution of sodium carbonate, and a titration ──────────────
Q2 = FIG + 'paper-q2'
_q2a = rows(k('2', 'a'))
assert cells(k('2', 'a')) == ['[5 + 3]'] and _q2a == ['A: Wash bottle', 'B: Volumetric flask'], _q2a
C.add([k('2', 'a')], 'chem-4-1', 'the-wash-bottle-and-volumetric-flask', [
    lift('r-1', _q2a[0], None), lift('r-2', _q2a[1], None)],
    kind='orderedSplit', notation='[5 + 3]', total=8, notes=SPLIT.format('(5 + 3)'), figure=Q2,
    label_key=[{'letter': 'A', 'meaning': 'Wash bottle', 'askedInThisQuestion': True},
               {'letter': 'B', 'meaning': 'Volumetric flask', 'askedInThisQuestion': True}])
# (b): "Explain the terms (i) standard solution, (ii) primary standard, ..." is one
# sentence; the scheme numbers the two and prices them together (6 + 3), (ii) in
# either of two wordings set with "//" between them (scheme PDF page 6): one row
# (i), one choice of the two (ii).
_q2b1, _q2b2 = P.items(k('2', 'b', 'i')), P.items(k('2', 'b', 'ii'))
assert [it.cell for it in _q2b1] == [None] and [it.cell for it in _q2b2] == ['[6 + 3]'], (_q2b1, _q2b2)
_primary = options([bare(_q2b2[0].rows[0].text), _q2b2[0].rows[1].text])
assert len(_q2b2[0].rows) == 2 and all(o.startswith('Substance') for o in _primary), _primary
C.add([k('2', 'b', 'i'), k('2', 'b', 'ii')], 'chem-4-1', 'standard-solution-and-primary-standard', [
    lift('r-1', _q2b1[0].text, None, 'For (i).'),
    null_menu('r-2', _primary, 1, 'For (ii), either of these: the scheme prints the two definitions with "//" '
              'between them.')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('(6 + 3)'),
    qtext=P.ask(k('2', 'b')), stem=C.context(k('2', 'b')))
assert cells(k('2', 'c')) == ['[3]', '[3]'], P.items(k('2', 'c'))
C.fixed([k('2', 'c')], 'chem-4-1', 'anhydrous-sodium-carbonate-as-a-primary-standard',
        row_notes={0: 'For "What is meant by describing the sodium carbonate used as anhydrous?"',
                   1: 'For "Give one property ...": any one of these.'})
# (d): three uses priced "[Any 2 (9 + 3)]" (scheme PDF page 6, set as an aside):
# any two, the first (9), the second (3).
_q2d = P.items(k('2', 'd'))
assert [(it.cell, it.asides) for it in _q2d] == [(None, ['[Any 2 (9 + 3)]'])], _q2d
_uses = options(split_points(_q2d[0].text))
assert len(_uses) == 3, _uses
C.add([k('2', 'd')], 'chem-4-1', 'uses-of-the-wash-bottle', [menu(
    'r-1', _uses, 2, 9, 'Any two of these, the first (9), the second (3): the scheme lists three uses and prices '
    'them "' + traced('[Any 2 (9 + 3)]') + '".', steps=[9, 3])], total=12, figure=Q2)
# (e): the working (6), its aside set with a script ("M_(r)") the note shows as printed.
_q2e = P.items(k('2', 'e'))
assert [(it.cell, it.text, it.asides) for it in _q2e] == [
    ('[6]', '5.3 ÷ 106 = 0.05', ['[Allow 3 marks for arriving at the M_(r) of 106]'])], _q2e
C.add([k('2', 'e')], 'chem-4-1', 'concentration-of-the-sodium-carbonate-solution', [
    lift('r-1', _q2e[0].text, 6, 'The scheme adds: ' + traced(display(_q2e[0].asides[0])))])
# (f): the answer (9), "Calc.:" before it, then its working in a box of stacked
# fractions the text layer cannot order, (3) a step: the scheme's print of the
# working is the figure.
_q2f = P.items(k('2', 'f'))
assert [it.cell for it in _q2f] == ['[9]', '[3]', '[3]', '[3]'] and _q2f[0].text == 'Calc.: 0.09 M', _q2f
C.answer_only([k('2', 'f')], 'chem-4-1', 'molarity-of-the-hydrochloric-acid', S + 'q2f',
              fixes={'Calc.: 0.09 M': '0.09 M'})

# ── Q3 Flame tests and anion tests ───────────────────────────────────────────
Q3 = FIG + 'paper-q3'
# The question's lead-in says what the student was asked, "(i) to identify ...,
# (ii) to confirm ...", romans the reader files as parts of their own; with the
# sentence after them it is the stem of both parts. The table it introduces is
# the picture's (q3-table).
Q3_STEM = (f"{P.ask(k('3'))} (i) {P.ask(k('3', None, 'i'))} (ii) {P.ask(k('3', None, 'ii'))} "
           f"{P.lead(k('3', None, 'ii'))}")
assert Q3_STEM.endswith('The student presented the results in a table as shown below.'), Q3_STEM
_q3a_ask = P.ask(k('3', 'a'))
_q3a = P.items(k('3', 'a'))
assert [it.cell for it in _q3a] == ['[3 × 3]', '[3 × 3]'], _q3a
# (a): two cells (3 × 3) each, the procedure's three points and the three
# colours: six fixed rows outrun a card (row cap 5), so a card each.
_flame = split_points(_q3a[0].text)
assert len(_flame) == 3, _flame
C.add([k('3', 'a')], 'chem-u2', 'flame-test-procedure', [
    lift(f'r-{i + 1}', t, 3, 'The scheme prices the three points (3 × 3), one each.' if not i else '')
    for i, t in enumerate(_flame)],
    qtext=cut(_q3a_ask, None, 'In the case of'), stem=Q3_STEM, figure=Q3, ref_suffix='the flame test')
_colours = rows(k('3', 'a'), 1)
assert [c.split(':')[0] for c in _colours] == ['Lithium', 'Sodium', 'Potassium'], _colours
C.add([k('3', 'a')], 'chem-1-2', 'flame-colours-of-lithium-sodium-and-potassium', [
    lift(f'r-{i + 1}', t, 3, 'The scheme prices the three colours (3 × 3), one each.' if not i else '')
    for i, t in enumerate(_colours)],
    qtext=cut(_q3a_ask, 'In the case of'), stem=Q3_STEM, figure=Q3, cid='q3-a-colours',
    ref_suffix='the flame colours')
# (b)(i)-(iii): each test's ion and observation, priced together "[(4 × 6) + (2 ×
# 4)]" beside the last (scheme PDF page 7): six points, six terms. The scheme
# sets each formula's charge above it in a run of its own ("–", "2–"), which the
# reader sets after the formula; the gate reads the sulfate's "2" before the line
# it belongs to, so that formula is lifted without its charge, and the scheme's
# own print of the answers is shown with them. The paper's print of (b) is the
# question (its "(NO₃⁻)" and "(SO₄²⁻)" read the same way).
_q3b = [rows(k('3', 'b', r)) for r in ('i', 'ii', 'iii')]
assert _q3b == [['ion: Nitrate / NO₃ –', 'obs.: Brown ring'], ['ion: Chloride / Cl –', 'obs.: White precipitate'],
                ['ion: Sulfate / SO₄ 2–', 'obs.: White precipitate']], _q3b
assert [cells(k('3', 'b', r)) for r in ('i', 'ii', 'iii')] == [[None], [None], ['[(4 × 6) + (2 × 4)]']]
for _r, _ion in zip(_q3b, ('Nitrate / NO₃⁻', 'Chloride / Cl⁻', 'Sulfate / SO₄')):
    assert display(uncue(_r[0], 'ion:')).replace(' –', '⁻').replace(' 2–', '') == _ion, _r
_charge = 'The scheme sets the formula\'s charge, "' + traced('2–') + '", above it; its own print is shown with the answer.'
C.add([k('3', 'b', r) for r in ('i', 'ii', 'iii')], 'chem-u2', 'tests-for-nitrate-chloride-and-sulfate-ions', [
    lift('r-1', 'Nitrate / NO₃⁻', None, 'For (i), the ion.'),
    lift('r-2', uncue(_q3b[0][1], 'obs.:'), None, 'For (i), the observation.'),
    lift('r-3', 'Chloride / Cl⁻', None, 'For (ii), the ion.'),
    lift('r-4', uncue(_q3b[1][1], 'obs.:'), None, 'For (ii), the observation.'),
    lift('r-5', 'Sulfate / SO₄', None, 'For (iii), the ion. ' + _charge),
    lift('r-6', uncue(_q3b[2][1], 'obs.:'), None, 'For (iii), the observation.')],
    kind='orderedSplit', notation='[(4 × 6) + (2 × 4)]', total=32, notes=SPLIT.format('[(4 × 6) + (2 × 4)]'),
    stem=Q3_STEM, figure=S + 'q3b')
print_question('paper-q3b-print')

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-2', 'rutherford-and-the-nucleus', notes=Q4_NOTE, figure=FIG + 'paper-q4a')
# (b): four differences priced (2 × 3): any two.
_q4b = P.items(k('4', 'b'))
assert [it.cell for it in _q4b] == ['[2 × 3]'], _q4b
_mendeleev = options(split_points(_q4b[0].text))
assert len(_mendeleev) == 4, _mendeleev
C.add([k('4', 'b')], 'chem-1-3', 'mendeleevs-periodic-table-and-the-modern-one', [menu(
    'r-1', _mendeleev, 2, 3, 'Any two of these: the scheme lists four differences and prices them "'
    + traced('(2 × 3)') + '".')], total=6, notes=Q4_NOTE)
assert cells(k('4', 'c')) == ['[2 × 3]'], P.items(k('4', 'c'))
C.fixed([k('4', 'c')], 'chem-2-1', 'covalent-bond', notes=Q4_NOTE)
# (d): four uses priced (6): any one.
_q4d = P.items(k('4', 'd'))
assert [it.cell for it in _q4d] == ['[6]'], _q4d
_tlc = options(split_points(_q4d[0].text))
assert len(_tlc) == 4, _tlc
C.add([k('4', 'd')], 'chem-u2', 'uses-of-thin-layer-chromatography', [menu(
    'r-1', _tlc, 1, 6, 'Any one of these: the scheme lists four uses and prices one (6).')], total=6, notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-2-2', 'shape-of-the-methane-molecule', notes=Q4_NOTE, figure=FIG + 'paper-q4e')
# (f): three points set with "//" between them, priced (6): any one.
_q4f = P.items(k('4', 'f'))
assert [it.cell for it in _q4f] == ['[6]'], _q4f
_fehling = options(split_points(_q4f[0].text))
assert _fehling == ['Formation of a brick colour', 'red colour', 'precipitate'], _fehling
C.add([k('4', 'f')], 'chem-4-2', 'ethanal-and-fehlings-reagent', [menu(
    'r-1', _fehling, 1, 6, 'Any one of these: the scheme sets the three with "//" between them and prices one (6).')],
    total=6, notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-4-3', 'temporary-and-permanent-hardness', notes=Q4_NOTE,
        fixes={'Dist.: Temporary hardness is removed by boiling': 'Temporary hardness is removed by boiling'})
# (h): the reader ends the ask at its first line and takes the rest for a
# lead-in: the whole is the ask.
_q4h = f"{P.ask(k('4', 'h'))} {P.lead(k('4', 'h'))}"
assert _q4h.startswith('The picture on the right') and _q4h.endswith('bears his name.'), _q4h
C.fixed([k('4', 'h')], 'chem-2-3', 'charles-law', notes=Q4_NOTE, figure=FIG + 'paper-q4h', qtext=_q4h)
# (i): the equilibrium's arrow is a glyph the text layer cannot read (its line is
# 'labels'): the paper's print is the question; the scheme's answer is a
# fraction, its own print.
_q4i = P.items(k('4', 'i'))
assert [it.cell for it in _q4i] == ['[6]', None] and _q4i[0].text == '[CO] . [H₂]³', _q4i
_allow4i = traced('[Allow 3 marks for top or bottom correct or 3 marks for inverted expression]')
assert _q4i[1].rows[-1].text == _allow4i, _q4i
C.drawn([k('4', 'i')], 'chem-3-3', 'kc-expression-for-steam-reforming-of-methane', S + 'q4i',
        notes=Q4_NOTE + ' The scheme adds: ' + _allow4i)
print_question('paper-q4i-print')
# (j): the reader ends the ask at its first line: the whole is the ask.
_q4j = f"{P.ask(k('4', 'j'))} {P.lead(k('4', 'j'))}"
assert _q4j.endswith('so as to minimise heat loss?'), _q4j
assert rows(k('4', 'j')) == ['Thermometer', 'Polystyrene'] and cells(k('4', 'j')) == ['[2 × 3]']
C.add([k('4', 'j')], 'chem-3-1', 'measuring-a-heat-of-reaction', [
    lift('r-1', 'Thermometer', 3, 'For "Name the piece of equipment C." The scheme prices the two answers (2 × 3), '
         'one each.'),
    lift('r-2', 'Polystyrene', 3, 'For "What material would you choose for vessel V ...?"')],
    notes=Q4_NOTE, figure=FIG + 'paper-q4j', qtext=_q4j,
    label_key=[{'letter': 'C', 'meaning': 'Thermometer', 'askedInThisQuestion': True}])
# (k): the scheme sets no "A" or "B": A's answers, then "or", then B's (scheme
# PDF page 8), each priced (2 × 3).
_q4k = P.items(k('4', 'k'))
assert [it.cell for it in _q4k] == ['[2 × 3]', '[2 × 3]'], _q4k
_factors = options(split_points(_q4k[0].text))
assert len(_factors) == 5, _factors
C.add([ka('4', 'k', None, 'A')], 'chem-u3', 'location-of-a-chemical-factory', [menu(
    'r-1', _factors, 2, 3, 'Any two of these: the scheme lists five factors and prices them "'
    + traced('(2 × 3)') + '".')], total=6, notes=Q4_NOTE)
_alloy = [r.text for r in _q4k[1].rows]
assert _alloy == ['Mixture of metals [or metal with another element such as carbon]',
                  'Exa.: Steel // bronze // brass // solder // pewter'], _alloy
_examples = options(split_points(uncue(_alloy[1], 'Exa.:')))
assert len(_examples) == 5, _examples
C.add([ka('4', 'k', None, 'B')], 'chem-1-3', 'alloys', [
    lift('r-1', 'Mixture of metals', 3, 'For "Explain the term alloy." The scheme prices the explanation and the '
         'example (2 × 3), one each, and adds: ' + traced('[or metal with another element such as carbon]')),
    menu('r-2', _examples, 1, 3, 'For "Give an example of an alloy.": any one of these.')], total=6, notes=Q4_NOTE)

# ── Q5 Dalton, isotopes, and bonding in ammonia ──────────────────────────────
Q5 = FIG + 'paper-q5'
_q5a_ask = P.ask(k('5', 'a'))
_q5a = P.items(k('5', 'a'))
assert [it.cell for it in _q5a] == ['[5]', '[6 + (2 × 3)]'] and _q5a[0].text == 'Dalton', _q5a
# (a): three asks under the paper's (5) and (12): the name, priced (5); then why
# he was wrong and the term, priced together "[6 + (2 × 3)]" (scheme PDF page 9):
# three points, three terms.
C.add([k('5', 'a')], 'chem-1-2', 'dalton', [lift('r-1', 'Dalton', 5)], figure=Q5,
      qtext=cut(_q5a_ask, None, 'Explain by reference'), ref_suffix='the English scientist')
_iso = [r.text for r in _q5a[1].rows]
assert len(_iso) == 3, _iso
C.add([k('5', 'a')], 'chem-1-2', 'isotopes', [
    lift('r-1', bare(_iso[0]), None, 'For "Explain by reference to a named element ...".'),
    lift('r-2', bare(_iso[1]), None),
    lift('r-3', uncue(_iso[2], 'Term:'), None, 'For "What term is used ...?"')],
    kind='orderedSplit', notation='[6 + (2 × 3)]', total=12, notes=SPLIT.format('[6 + (2 × 3)]'), figure=Q5,
    qtext=cut(_q5a_ask, 'Explain by reference'), cid='q5-a-isotopes', ref_suffix='why he was incorrect')
# (b): "State the valency (i) of nitrogen, (ii) of hydrogen, in ammonia." is one
# sentence; the scheme prices each valency (3), labelled "N:" and "H:", then the
# explanation printed after it, two points (2 × 3): a card each.
Q5B = FIG + 'paper-q5b'
_q5b_ask = P.ask(k('5', 'b'))
_q5b = P.items(k('5', 'b'))
assert [(it.cell, it.text) for it in _q5b[:2]] == [('[3]', 'N: 3'), ('[3]', 'H: 1')] \
    and _q5b[2].cell == '[2 × 3]' and len(_q5b) == 3, _q5b
_valency = cut(_q5b_ask, 'State the valency', 'Explain how')
_q5b_stem = cut(_q5b_ask, None, 'State the valency')
for r, it, concept in (('i', _q5b[0], 'valency-of-nitrogen'), ('ii', _q5b[1], 'valency-of-hydrogen')):
    C.add([k('5', 'b', r)], 'chem-2-1', concept, [lift('r-1', it.text, 3, f'For ({r}).')],
          qtext=_valency, stem=_q5b_stem, figure=Q5B)
_noble = [bare(_q5b[2].rows[0].text), _q5b[2].rows[1].text]
C.add([k('5', 'b')], 'chem-2-1', 'valency-and-the-noble-gases', [
    lift('r-1', _noble[0], 3, 'The scheme prices the two points (2 × 3), one each.'), lift('r-2', _noble[1], 3)],
    qtext=cut(_q5b_ask, 'Explain how'), stem=f'{_q5b_stem} {_valency}', figure=Q5B, cid='q5-b-noble-gases',
    ref_suffix='after (ii), the noble gases')
# (c)-(d) take no stem: the question's lead-in, Dalton "pictured on the right", is
# (a)'s.
# (c): the dot and cross diagram, priced (2 × 3) by what it shows -- the scheme
# draws it (scheme PDF page 9, its print the answer) with its criteria beneath --
# then the shape (6).
_q5c_ask = P.ask(k('5', 'c'))
_q5c = P.items(k('5', 'c'))
assert [(it.cell, it.text) for it in _q5c] == [('[2 × 3]', 'Use:'), ('[6]', 'Pyramidal')], _q5c
_crit = traced(_q5c[0].asides[0])
C.add([k('5', 'c')], 'chem-2-2', 'bonding-and-shape-of-the-ammonia-molecule', [
    C.mark_ask(point('r-1', cut(_q5c_ask, None, 'What is the shape'), 6,
                     'The scheme answers this with a drawing; its own print is shown with the answer. It prices the '
                     'drawing (2 × 3) by what it shows: ' + _crit)),
    lift('r-2', 'Pyramidal', 6, adds(_q5c[1].asides) + ' For "What is the shape of the ammonia molecule?"')],
    figure=S + 'q5c', stem='')
# (d): the definition, two points (2 × 3), then the bond (3) under "Use:".
assert cells(k('5', 'd')) == ['[2 × 3]', '[3]'], P.items(k('5', 'd'))
C.fixed([k('5', 'd')], 'chem-2-1', 'electronegativity-and-the-nitrogen-hydrogen-bond',
        fixes={'Use: Polar covalent': 'Polar covalent'}, stem='',
        row_notes={0: 'For "Define electronegativity."', 2: 'For "Use electronegativity values to predict the type of '
                                                          'bond ..."'})

# ── Q6 Alkanes as fuels ──────────────────────────────────────────────────────
Q6_STEM = P.ask(k('6'))
Q6A = P.ask(k('6', 'a'))
assert Q6A == 'What are (i) hydrocarbons, (ii) isomers?', Q6A
# (a): one sentence; the scheme prices (i) (5) and (ii) two points (2 × 3): a
# card each.
assert cells(k('6', 'a', 'i')) == ['[5]'] and cells(k('6', 'a', 'ii')) == ['[2 × 3]']
C.fixed([k('6', 'a', 'i')], 'chem-2-4', 'hydrocarbons', qtext=Q6A, stem=Q6_STEM, row_notes={0: 'For (i).'})
C.fixed([k('6', 'a', 'ii')], 'chem-2-4', 'structural-isomers', qtext=Q6A, stem=Q6_STEM, row_notes={0: 'For (ii).'})
# (b): three sources priced (2 × 3): any two.
_q6b = P.items(k('6', 'b'))
assert [it.cell for it in _q6b] == ['[2 × 3]'], _q6b
_sources = options(split_points(_q6b[0].text))
assert _sources == ['Oil', 'coal', 'natural gas'], _sources
C.add([k('6', 'b')], 'chem-2-4', 'sources-of-hydrocarbon-fuels', [menu(
    'r-1', _sources, 2, 3, 'Any two of these: the scheme lists three sources and prices them "'
    + traced('(2 × 3)') + '".')], total=6)
# (c): four situations under "Mention:" and two reasons under "Why:" (the cue
# taken off), priced together "[9 + (2 × 3)]" (scheme PDF page 10): three points
# priced, six listed, without saying which earns which. The paper asks for two
# situations and why: any two of the four, any one of the two, unpriced.
_q6c = rows(k('6', 'c'))
assert cells(k('6', 'c')) == ['[9 + (2 × 3)]'] and len(_q6c) == 3, _q6c
_situations = options(split_points(uncue(_q6c[0], 'Mention:') + ' ' + _q6c[1]))
_why = options(split_points(_q6c[2]))
assert len(_situations) == 4 and len(_why) == 2, (_situations, _why)
C.add([k('6', 'c')], 'chem-2-4', 'methane-build-up-and-the-environment', [
    null_menu('r-1', _situations, 2, 'For "Mention two situations ...": any two of these.'),
    null_menu('r-2', _why, 1, 'For "Why are the levels of methane ...?": either of these; the scheme sets it under the '
              'cue "' + traced('Why:') + '".')],
    kind='orderedSplit', notation='[9 + (2 × 3)]', total=15,
    notes='The scheme prices the two situations and the reason together as "' + traced('[9 + (2 × 3)]') + '" without '
          'saying which earns which, so no per-point value is shown.')
# (d): the three asks priced together (9 + 6 + 3), the second in either of two
# answers set with "//" between them; the scheme writes the structural formula
# out on one line.
_q6d = rows(k('6', 'd'))
assert cells(k('6', 'd')) == ['[9 + 6 + 3]'] and len(_q6d) == 3, _q6d
C.add([k('6', 'd')], 'chem-2-4', 'octane-number-and-2-2-4-trimethylpentane', [
    lift('r-1', _q6d[0], None, 'For "What do you understand by the octane number of a fuel?"'),
    null_menu('r-2', options(split_points(_q6d[1])), 1, 'For "What is the significance of the compound '
              '2,2,4-trimethylpentane ...?": either of these.'),
    lift('r-3', _q6d[2], None, 'For "Draw the structural formula of 2,2,4-trimethylpentane."')],
    kind='orderedSplit', notation='[9 + 6 + 3]', total=18, notes=SPLIT.format('(9 + 6 + 3)'))

# ── Q7 Four organic compounds ────────────────────────────────────────────────
# The question's opening sentence and the four formulae it lists are the stem of
# every part, which the reader's context leaves out as an instruction
# ("Answer ...").
Q7_LEAD = P.ask(k('7'))
assert Q7_LEAD == ('Answer the questions below with reference to the organic compounds listed. C₂H₂ CH₂CH₂ '
                   'CH₃CH₂OH CH₃COOH'), Q7_LEAD
# (a): one sentence; the scheme numbers the two and prices them together (5 + 3).
assert [cells(k('7', 'a', r)) for r in ('i', 'ii')] == [[None], ['[5 + 3]']]
C.ordered([k('7', 'a', 'i'), k('7', 'a', 'ii')], 'chem-2-2', 'tetrahedral-and-planar-carbon-atoms',
          qtext=P.ask(k('7', 'a')), stem=Q7_LEAD, row_notes={0: 'For (i).', 1: 'For (ii).'})
# (b): one sentence, "Give the systematic (IUPAC) names for (i) C₂H₂, (ii)
# CH₃COOH."; the scheme numbers the two and prices them (2 × 3).
_q7b = [P.items(k('7', 'b', r)) for r in ('i', 'ii')]
assert [[(it.cell, it.text) for it in x] for x in _q7b] == [[(None, 'Ethyne')], [('[2 × 3]', 'Ethanoic acid')]], _q7b
C.add([k('7', 'b')], 'chem-4-2', 'iupac-names-of-ethyne-and-ethanoic-acid', [
    lift('r-1', 'Ethyne', 3, 'For (i). The scheme prices the two names (2 × 3), one each.'),
    lift('r-2', 'Ethanoic acid', 3, 'For (ii).')], stem=Q7_LEAD)
# (c)(i)-(iii): three answers priced (3 × 3) beside the last, one each.
_q7c = [P.items(k('7', 'c', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in x] for x in _q7c] == [[None], [None], ['[3 × 3]']], _q7c
C.add([k('7', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-4-2', 'ethanol-ethanoic-acid-and-ethene-in-use', [
    lift(f'r-{i + 1}', x[0].text, 3, f'For ({r}).' + (' The scheme prices the three answers (3 × 3), one each.'
                                                       if not i else ''))
    for i, (r, x) in enumerate(zip(('i', 'ii', 'iii'), _q7c))], stem=f"{Q7_LEAD} {P.ask(k('7', 'c'))}")
assert cells(k('7', 'd')) == ['[3]', '[6]'], P.items(k('7', 'd'))
C.fixed([k('7', 'd')], 'chem-2-4', 'burning-ethyne', stem=Q7_LEAD,
        row_notes={0: 'For "Describe the appearance of the flame ..."', 1: 'For the balanced equation.'})
# (e)(i)-(ii): each conversion's type and its reagent or reagents, five points
# ((i): "Addition / hydration", "Water / H₂O"; (ii): "Oxidation", the dichromate,
# "Acidified // sulfuric acid / H₂SO₄"), priced "[9 + (3 × 3)]" (scheme PDF page
# 11): four priced, five listed -- any four, the first (9), the others (3).
_q7e1, _q7e2 = rows(k('7', 'e', 'i')), rows(k('7', 'e', 'ii'))
assert cells(k('7', 'e', 'i')) == [None] and cells(k('7', 'e', 'ii')) == ['[9 + (3 × 3)]'], (_q7e1, _q7e2)
assert len(_q7e1) == 2 and len(_q7e2) == 3, (_q7e1, _q7e2)
_conv = options([_q7e1[0], uncue(_q7e1[1], 'Reag.:'), _q7e2[0], uncue(_q7e2[1], 'Reag.:'), _q7e2[2]])
C.add([k('7', 'e', 'i'), k('7', 'e', 'ii')], 'chem-4-2', 'hydration-and-oxidation-and-their-reagents', [menu(
    'r-1', _conv, 4, 9, 'Any four of these, the first (9), the others (3): the scheme lists (i)\'s type and reagent '
    '(the first two here) and (ii)\'s type and reagents (the last three), and prices them "'
    + traced('[9 + (3 × 3)]') + '".', steps=[9, 3, 3, 3])], total=18, stem=f"{Q7_LEAD} {P.ask(k('7', 'e'))}")

# ── Q8 The decomposition of hydrogen peroxide ────────────────────────────────
Q8 = FIG + 'paper-q8'
Q8_STEM = P.ask(k('8'))
assert Q8_STEM.endswith('The results are shown in the table below.'), Q8_STEM
C.fixed([k('8', 'a')], 'chem-3-2', 'definition-of-a-catalyst', figure=Q8)
# (b): one sentence; the scheme numbers the two and prices them together (9 + 3),
# each a name // formula, as the paper asks: either.
_q8b = [rows(k('8', 'b', r)) for r in ('i', 'ii')]
assert _q8b == [['Hydrogen peroxide // H₂O₂'], ['Manganese dioxide // MnO₂']] \
    and cells(k('8', 'b', 'ii')) == ['[9 + 3]'], _q8b
C.add([k('8', 'b', 'i'), k('8', 'b', 'ii')], 'chem-3-2', 'hydrogen-peroxide-and-manganese-dioxide', [
    null_menu('r-1', options(split_points(_q8b[0][0])), 1, 'For (i), either the name or the formula.'),
    null_menu('r-2', options(split_points(_q8b[1][0])), 1, 'For (ii), either the name or the formula.')],
    kind='orderedSplit', notation='[9 + 3]', total=12, notes=SPLIT.format('(9 + 3)'), qtext=P.ask(k('8', 'b')),
    stem=Q8_STEM, figure=Q8)
C.fixed([k('8', 'c')], 'chem-3-2', 'when-the-reaction-is-over', figure=Q8,
        fixes={'When: No more gas being given off': 'No more gas being given off'})
# (d): the graph priced by what it shows -- its axes (2 × 3), its points (6), its
# curve (3) -- the scheme drawing it (scheme PDF page 12, its print the answer),
# then the reading (3). The table it plots is the paper's print of the part.
assert cells(k('8', 'd')) == ['[2 × 3]', '[6]', '[3]', '[3]'], P.items(k('8', 'd'))
C.fixed([k('8', 'd')], 'chem-3-2', 'plotting-the-volume-of-oxygen-against-time', figure=S + 'q8d',
        fixes={'Plot: Axes': 'Axes', 'From: 34 ± 2': '34 ± 2'}, stem=Q8_STEM,
        row_notes={0: 'For the graph: the scheme prices what it shows and draws it, shown with the answer.',
                   3: 'For "From the graph estimate the volume of gas liberated after 3 minutes."'})
print_question('paper-q8d-print')
# (e): two points set with "//" between them, priced (3): either.
_q8e = P.items(k('8', 'e'))
assert [it.cell for it in _q8e] == ['[3]'], _q8e
C.add([k('8', 'e')], 'chem-3-2', 'why-the-rate-decreases', [menu(
    'r-1', options(split_points(_q8e[0].text)), 1, 3, 'Either of these: the scheme sets the two with "//" between '
    'them and prices one (3).')], total=3, stem=Q8_STEM, figure=Q8)
_q8f = P.items(k('8', 'f'))
assert [it.cell for it in _q8f] == ['[6]'], _q8f
C.add([k('8', 'f')], 'chem-3-2', 'increasing-the-rate-of-decomposition', [menu(
    'r-1', options(split_points(uncue(_q8f[0].text, 'Using:'))), 1, 6, 'Either of these: the scheme sets the two '
    'with "//" between them and prices one (6).')], total=6, stem=Q8_STEM, figure=Q8)

# ── Q9 Water and sewage treatment ────────────────────────────────────────────
Q9A = P.ask(k('9', 'a'))
_q9a_lead = cut(Q9A, 'In the treatment', 'Name a substance')
# (a): four asks under the paper's (5), (6), (6) and (12), each priced by a cell
# of its own (scheme PDF page 13): a card each, the later cited by what they ask.
assert [(it.cell, it.text) for it in P.items(k('9', 'a'))] == [('[3 + 2]', '–log₁₀ // [H⁺]')]
C.add([k('9', 'a')], 'chem-3-4', 'definition-of-ph', [
    lift('r-1', '–log₁₀', None), lift('r-2', '[H⁺]', None)],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('(3 + 2)'),
    qtext=cut(Q9A, None, 'In the treatment'), stem='', ref_suffix='define pH')
# The substances: one sentence, "(i) if the pH is too high, (ii) if the pH is too
# low", priced (2 × 3) beside (ii); each a name // another, as the paper asks for
# one: either.
_q9a1, _q9a2 = P.items(k('9', 'a', 'i')), P.items(k('9', 'a', 'ii'))
assert [(it.cell, it.text) for it in _q9a1] == [(None, 'Sulfuric acid // acid')] \
    and [it.cell for it in _q9a2] == ['[2 × 3]', '[6]', '[2 × 6]', '[2 × 6]'] \
    and _q9a2[0].text == 'Lime // sodium hydroxide', (_q9a1, _q9a2)
C.add([k('9', 'a', 'i'), k('9', 'a', 'ii')], 'chem-4-3', 'adjusting-the-ph-of-drinking-water', [
    menu('r-1', options(split_points(_q9a1[0].text)), 1, 3, 'For (i), either of these. The scheme prices the two '
         'substances (2 × 3), one each.'),
    menu('r-2', options(split_points(_q9a2[0].text)), 1, 3, 'For (ii), either of these.')],
    total=6, qtext=cut(Q9A, 'Name a substance', 'What harm'), stem=_q9a_lead)
C.add([k('9', 'a')], 'chem-4-3', 'harm-from-acidic-drinking-water', [lift('r-1', _q9a2[1].text, 6)],
      qtext=cut(Q9A, 'What harm', 'Flocculation'), stem=_q9a_lead, cid='q9-a-harm',
      ref_suffix='after (ii), a pH too low')
# Then flocculation or fluoridation, "how and why": the scheme prices either
# process (2 × 6), printing "or" between them (scheme PDF page 13); its two points
# are the process's how and why. Each process is a route, its how and its why a
# row each: a student claims the two points of the process they explained, and
# the other process's rows lock, so a how of one is never paired with a why of
# the other.
_floc = [r.text for r in _q9a2[2].rows]
_fluor = [r.text for r in _q9a2[3].rows]
assert len(_floc) == 3 and len(_fluor) == 3, (_floc, _fluor)
_how = options([bare(uncue(_floc[0], 'Flocculation:')), bare(uncue(_fluor[0], 'Fluoridation:') + ' ' + _fluor[1])])
_why = options([f'{_floc[1]} {_floc[2]}', _fluor[2]])
C.add([k('9', 'a')], 'chem-4-3', 'flocculation-and-fluoridation', [
    routed(lift('r-1', _how[0], 6, 'Flocculation, how it is carried out. The scheme prices either process (2 × 6), '
                'one each, and prints "or" between them: flocculation is this row and the next, fluoridation the '
                'last two. The examiner marks the process explained, not a mix of the two.'), 'a'),
    routed(lift('r-2', _why[0], 6, 'Flocculation, why.'), 'a'),
    routed(lift('r-3', _how[1], 6, 'Or fluoridation, how it is carried out.'), 'b'),
    routed(lift('r-4', _why[1], 6, 'Fluoridation, why.'), 'b')],
    total=12, qtext=cut(Q9A, 'Flocculation'), stem='', cid='q9-a-flocculation-or-fluoridation',
    ref_suffix='after (ii), flocculation or fluoridation')
# (b): four blanks priced "[9 + 6 + (2 × 3)]" without saying which earns which;
# the passage with its numbered blanks is the paper's print.
_q9b = rows(k('9', 'b'))
assert cells(k('9', 'b')) == ['[9 + 6 + (2 × 3)]'] and [b[:2] for b in _q9b] == ['1:', '2:', '3:', '4:'], _q9b
C.add([k('9', 'b')], 'chem-4-3', 'stages-of-sewage-treatment', [
    lift(f'r-{i + 1}', b, None) for i, b in enumerate(_q9b)],
    kind='orderedSplit', notation='[9 + 6 + (2 × 3)]', total=21,
    notes=SPLIT.format('[9 + 6 + (2 × 3)]') + ' Each answer is numbered by its blank.')
print_question('paper-q9b-print')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a)(i): two answers, each under its label, priced together (4 + 3).
_q10a1 = rows(k('10', 'a', 'i'))
assert cells(k('10', 'a', 'i')) == ['[4 + 3]'] and _q10a1 == ['Cu: 0.1', 'Acid: 0.2'], _q10a1
C.add([k('10', 'a', 'i')], 'chem-1-4', 'moles-of-copper-and-sulfuric-acid', [
    lift('r-1', _q10a1[0], None, 'For "How many moles of copper were used?"'),
    lift('r-2', _q10a1[1], None, 'For "How many moles of sulfuric acid were used up?"')],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'))
# (ii)-(iii): each answer priced with its working beside it after "//" (scheme
# PDF page 14): the answer is the row, the working quoted.
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [(it.cell, it.text) for it in _q10a2] == [('[6]', 'Water: 3.6 g // 0.2 × 18')], _q10a2
_water = split_points(uncue(_q10a2[0].text, 'Water:'))
C.add([k('10', 'a', 'ii')], 'chem-1-4', 'mass-of-water-produced', [
    lift('r-1', _water[0], 6, 'The scheme sets the working beside it: "' + traced(_water[1]) + '".')])
_q10a3 = P.items(k('10', 'a', 'iii'))
assert [it.cell for it in _q10a3] == ['[6]', '[6]'], _q10a3
_volume = split_points(uncue(_q10a3[0].text, 'Volume:'))
_molecules = split_points(_q10a3[1].text)
assert len(_volume) == 2 and len(_molecules) == 2, (_volume, _molecules)
C.add([k('10', 'a', 'iii')], 'chem-1-4', 'volume-and-molecules-of-sulfur-dioxide', [
    lift('r-1', _volume[0], 6, 'For the volume. The scheme sets the working beside it: "' + traced(_volume[1]) + '".'),
    lift('r-2', _molecules[0], 6, 'For the molecules. The scheme sets the working beside it: "'
         + traced(_molecules[1]) + '".')])
_q10b1 = rows(k('10', 'b', 'i'))
assert cells(k('10', 'b', 'i')) == ['[4 + 3]'] and len(_q10b1) == 2, _q10b1
C.add([k('10', 'b', 'i')], 'chem-4-3', 'free-chlorine-in-swimming-pools', [
    lift('r-1', _q10b1[0], None, 'For "What is meant by free chlorine?"'),
    lift('r-2', uncue(_q10b1[1], 'Function:'), None, 'For "What is its function in swimming pools?"')],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'))
C.fixed([k('10', 'b', 'ii')], 'chem-4-3', 'monitoring-free-chlorine')
# (iii): five steps priced "[6 + (2 × 3)]": any three, the first (6), the others (3).
_q10b3 = P.items(k('10', 'b', 'iii'))
assert [it.cell for it in _q10b3] == ['[6 + (2 × 3)]'], _q10b3
_steps = options(split_points(_q10b3[0].text))
assert len(_steps) == 5, _steps
C.add([k('10', 'b', 'iii')], 'chem-u2', 'estimating-free-chlorine-with-a-comparator', [menu(
    'r-1', _steps, 3, 6, 'Any three of these, the first (6), the others (3): the scheme lists five steps and prices '
    'them "' + traced('[6 + (2 × 3)]') + '".', steps=[6, 3, 3])], total=12)
Q10C = FIG + 'paper-q10c'
_q10c1 = rows(k('10', 'c', 'i'))
assert cells(k('10', 'c', 'i')) == ['[4 + 3]'] and _q10c1 == ['What Clove oil', 'Cloves'], _q10c1
C.add([k('10', 'c', 'i')], 'chem-u2', 'clove-oil-by-steam-distillation', [
    lift('r-1', uncue(_q10c1[0], 'What'), None, 'For "What substance did you extract ...?"'),
    lift('r-2', _q10c1[1], None, 'For "From what was this substance extracted?"')],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'), figure=Q10C)
# (ii): two answers set with "//" between them, priced (6): either. The ask names
# the tube "labelled X"; its meaning is the scheme's own answer.
_q10c2 = P.items(k('10', 'c', 'ii'))
assert [it.cell for it in _q10c2] == ['[6]'], _q10c2
C.add([k('10', 'c', 'ii')], 'chem-u2', 'the-safety-tube', [menu(
    'r-1', options(split_points(_q10c2[0].text)), 1, 6, 'Either of these: the scheme sets the two with "//" between '
    'them and prices one (6).')], total=6, figure=Q10C,
    label_key=[{'letter': 'X', 'meaning': display(_q10c2[0].text), 'askedInThisQuestion': True}])
_q10c3 = rows(k('10', 'c', 'iii'))
assert cells(k('10', 'c', 'iii')) == ['[9 + 3]'] and _q10c3 == ['Y: Water', 'Z: Steam'], _q10c3
C.add([k('10', 'c', 'iii')], 'chem-u2', 'water-and-steam-in-steam-distillation', [
    lift('r-1', _q10c3[0], None, 'For "Name the other substance."'),
    lift('r-2', _q10c3[1], None, 'For "Name the substance that travels along the tube labelled Z."')],
    kind='orderedSplit', notation='[9 + 3]', total=12, notes=SPLIT.format('(9 + 3)'), figure=Q10C,
    label_key=[{'letter': 'Z', 'meaning': 'Steam', 'askedInThisQuestion': True}])

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('11', 'a', 'i')], 'chem-2-4', 'aromatic-compounds')
_q11a2 = rows(k('11', 'a', 'ii'))
assert cells(k('11', 'a', 'ii')) == ['[6 + 3]'] and len(_q11a2) == 2, _q11a2
C.add([k('11', 'a', 'ii')], 'chem-2-4', 'toluene', [
    lift('r-1', _q11a2[0], None, 'For the name.'),
    lift('r-2', uncue(_q11a2[1], 'Structure:'), None, 'For the structural formula: the scheme writes it on one line.')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('(6 + 3)'))
_q11a3 = rows(k('11', 'a', 'iii'))
assert cells(k('11', 'a', 'iii')) == ['[6 + 3]'] and _q11a3 == ['Recrystallisation', 'Is: Solids'], _q11a3
C.add([k('11', 'a', 'iii')], 'chem-u2', 'recrystallisation-of-benzoic-acid', [
    lift('r-1', _q11a3[0], None, 'For "Name the method ..."'),
    lift('r-2', uncue(_q11a3[1], 'Is:'), None, 'For "Is this method used for purifying solids, liquids or gases?"')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('(6 + 3)'))
C.fixed([k('11', 'a', 'iv')], 'chem-2-4', 'benzene-as-a-carcinogen')
# (b): six matches priced "[9 + 6 + 4 + (2 × 3)]" (scheme PDF page 15): five
# priced, six listed -- any five, at the cell's values in its order. The terms and
# the table are the paper's print.
_q11b = rows(k('11', 'b'))
assert cells(k('11', 'b')) == ['[9 + 6 + 4 + (2 × 3)]'] and len(_q11b) == 6, _q11b
_match = options([uncue(_q11b[0], 'Match:')] + _q11b[1:])
assert [m[:2] for m in _match] == ['A:', 'B:', 'C:', 'D:', 'E:', 'F:'], _match
C.add([k('11', 'b')], 'chem-1-1', 'matching-terms-in-chemistry', [menu(
    'r-1', _match, 5, 9, 'Any five of these, the first (9), then (6), (4), (3) and (3): the scheme lists six matches '
    'and prices them "' + traced('[9 + 6 + 4 + (2 × 3)]') + '".', steps=[9, 6, 4, 3, 3])], total=25)
print_question('paper-q11b-print')
# (c)A: three pairs (6) each; then, printed after (iii) under a mark of its own
# (7), "State two ways in which chemistry benefits society.", which the scheme
# numbers (iv): four ways priced (4 + 3), any two, the first (4), the second (3).
_ca3_ask = P.ask(ka('11', 'c', 'iii', 'A'))
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-u3', 'main-product-and-co-product')
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-u3', 'fixed-and-variable-costs')
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-u3', 'batch-and-continuous-processes',
        qtext=cut(_ca3_ask, None, 'State two ways'))
_society = P.items(ka('11', 'c', 'iv', 'A'))
assert [it.cell for it in _society] == ['[4 + 3]'], _society
_ways = options(split_points(_society[0].text))
assert len(_ways) == 4, _ways
C.add([ka('11', 'c', None, 'A')], 'chem-u3', 'how-chemistry-benefits-society', [menu(
    'r-1', _ways, 2, 4, 'Any two of these, the first (4), the second (3): the scheme numbers this ask (iv), lists '
    'four ways and prices them "' + traced('(4 + 3)') + '".', steps=[4, 3])],
    total=7, qtext=cut(_ca3_ask, 'State two ways'), stem='', cid='q11-c-a-chemistry-and-society',
    ref_suffix='after (iii), chemistry and society')
# (c)B
_cb1 = P.items(ka('11', 'c', 'i', 'B'))
assert [it.cell for it in _cb1] == ['[4 + 3]'], _cb1
_polymer = split_points(_cb1[0].text)
assert len(_polymer) == 2, _polymer
C.add([ka('11', 'c', 'i', 'B')], 'chem-4-2', 'polymers', [lift('r-1', _polymer[0], None), lift('r-2', _polymer[1], None)],
      kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'))
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-4-2', 'a-use-of-ldpe')
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-4-2', 'ldpe-as-an-addition-polymer')
# (iv): six stages priced (3 × 3): any three.
C.menu([ka('11', 'c', 'iv', 'B')], 'chem-4-2', 'stages-in-recycling-a-plastic', claim=3,
       note='Any three of these: the scheme lists six stages and prices them "' + traced('(3 × 3)') + '".')
C.fixed([ka('11', 'c', 'v', 'B')], 'chem-4-2', 'a-benefit-of-recycling-plastics')


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
    """Every letter's printed marks, alternatives apart: the paper prints Q5(a),
    Q9(a) and Q10 and Q11's letters in subtotals ("(5)" then "(12)"), so the sum
    of every mark printed under the letter, not the last."""
    out = {}
    for s in P.pseg:
        q, letter, _roman, alt = s.key
        if letter and s.marks_at:
            out[(q, letter, alt)] = out.get((q, letter, alt), 0) + sum(m for _n, m in s.marks_at)
    for (q, letter, _r, _a), m in P.marks.items():
        if letter and not any(key[:2] == (q, letter) for key in out):
            out[(q, letter, None)] = m
    # A subtotal printed at the end of a line of words, which the reader strips
    # from the ask without recording where it fell: Q10(a)(i)'s "(7)" after "...
    # How many moles of sulfuric acid were used up?" and Q10(c)(i)'s "(7)" after
    # "... From what was this substance extracted?" (paper page 6), each its
    # letter's first.
    for key, (page, tail, m) in {('10', 'a', None): (6, 'sulfuric acid were used up? (7)', 7),
                                 ('10', 'c', None): (6, 'was this substance extracted? (7)', 7)}.items():
        lines = [l.text for l in read_lines(P.paper_path) if l.page == page]
        assert sum(t.endswith(tail) for t in lines) == 1, tail
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
