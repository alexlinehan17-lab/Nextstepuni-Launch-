#!/usr/bin/env python3
"""2013 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2013_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2013_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2013_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2013 ol

No 2013 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The 2013 paper sets each question's number in one run with its first words
("1. A sample of soap ...") or with its first letter ("3. (a)"); chem_print
reads the first as the head (split_heads, gated to 2013 OL by OLD_OL_HEADS),
without which the paper reader found no question at all. Its scheme prints the
running footer "Chemistry ATGL 2013" on every page (dropped for the same
sittings) and sets Q2(f)'s answers under the cue "FIND:" with no "(f)" (read
with the letter the paper prints, gated to 2013 OL).

The paper sets several asks unnumbered inside one letter, each priced by a
cell of its own -- Q3(a), Q5(a), Q7(a), Q10(a), Q10(b)(iii), Q11(b) and
Q11(c)A(ii) -- one card each, the later ones cited by what they ask. It sets
romans inside one sentence -- Q4(g), Q7(a) "Define (i) acid, (ii) base", Q7(b),
Q9(a) and Q10(a) "Explain why ... (i) ..., (ii) ..." -- which the scheme
numbers; the cards follow the scheme's cells and take the paper's sentence as
their question. The paper underlines the term Q2(a), Q5(c)(i) and Q11(c)B(i)
ask about, prints Q4(i)'s equation with an arrow the text layer cannot read and
Q11(a)'s passage with numbered blanks: those take the paper's own print as
their question, as do Q1(b) (the diagram it copies) and Q8(b) and Q8(d) (the
reaction scheme that names X, Y and Z, whose answers are the scheme's
drawings). Q4(k) and Q11(c) offer whole alternative parts A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN, point)

P = Printed(2013, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2013-OL-'
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
        raise Refused(f'"{text}" is not in the 2013 ol scheme')
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


_RAW = read_lines(P.scheme_path)


def raw_lines(page, rect):
    """The scheme's own printed lines inside a region of a page, in reading order:
    the labels of a drawing (read as the drawing's, 'scheme-labels', so the
    reader leaves them out of the answers)."""
    x0, y0, x1, y1 = rect
    return [display(l.text) for l in _RAW if l.page == page and l.x0 >= x0 and l.y0 >= y0
            and l.x1 <= x1 and l.y1 <= y1]


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Preparing soap ────────────────────────────────────────────────────────
Q1 = FIG + 'paper-q1'
assert cells(k('1', 'a')) == ['[7 + 1]'], P.items(k('1', 'a'))
C.ordered([k('1', 'a')], 'chem-4-2', 'reactants-for-making-soap', figure=Q1)
# (b): the scheme draws the apparatus with twelve labels (its labels are the
# picture's, 'scheme-labels'), prints the criterion "diagram with two correct
# labels:" and prices the part "ANY TWO: (9 + 3)": any two of its labels, the
# first (9), the second (3). The diagram the student copies is the paper's print.
_q1b = P.items(k('1', 'b'))
assert [(it.cell, it.text, it.asides) for it in _q1b] == [
    ('[9 + 3]', 'diagram with two correct labels:', ['[any two]'])], _q1b
_labels1 = raw_lines(4, (140, 212, 412, 435))
assert _labels1 == ['thermometer', 'still-head', 'water out', 'condenser', 'adaptor', 'reaction mixture', 'flask',
                    'water in', 'heater', 'beaker', 'antibumping granules', 'distillate (ethanol)'], _labels1
C.add([k('1', 'b')], 'chem-u2', 'distillation-apparatus-in-making-soap', [anyN(
    'r-1', options(_labels1)[0], 12, 2, 9, options(_labels1),
    'Any two of these labels, the first (9) and the second (3): the scheme prints "'
    + traced(_q1b[0].text) + '", labels its drawing with these and prices the part "'
    + traced('ANY TWO: (9 + 3)') + '".', steps=[9, 3])],
    total=12, figure=S + 'q1b', notes='The scheme draws the labelled apparatus; its own print is shown with the '
                                      'answer.')
print_question('paper-q1b-print')
C.fixed([k('1', 'c')], 'chem-u2', 'ensuring-smooth-boiling', figure=Q1)
C.fixed([k('1', 'd')], 'chem-u2', 'what-the-distillation-removes', figure=Q1)
assert cells(k('1', 'e')) == ['[5 + 3 + 1]'], P.items(k('1', 'e'))
C.ordered([k('1', 'e')], 'chem-u2', 'brine-and-separating-the-soap', figure=Q1,
          row_notes={0: 'For "What is brine?"', 2: 'For "How was the precipitate of soap removed from the brine?"'})
# (f): the reason to wash, its aside "[Allow safety]" on a row of its own
# beneath it, then why not warm water, priced together (7 + 2).
_q1f = P.items(k('1', 'f'))
assert [(it.cell, it.asides) for it in _q1f] == [('[7 + 2]', ['[Allow safety]'])], _q1f
_wash = _q1f[0].points()
assert len(_wash) == 2 and _wash[0].endswith('/ to remove impurities'), _wash
C.add([k('1', 'f')], 'chem-u2', 'washing-the-soap', [
    lift('r-1', _wash[0], None, 'For "Why was it necessary to wash the soap ...?" ' + adds(_q1f[0].asides)),
    lift('r-2', _wash[1], None, 'For "Why should warm water not have been used ...?"')],
    kind='orderedSplit', notation='[7 + 2]', total=9, notes=SPLIT.format('(7 + 2)'), figure=Q1)

# ── Q2 A standard solution of sodium carbonate, and a titration ──────────────
Q2 = FIG + 'paper-q2'
# (a): the paper underlines "standard solution".
assert cells(k('2', 'a')) == ['[3 + 2]'], P.items(k('2', 'a'))
C.ordered([k('2', 'a')], 'chem-4-1', 'standard-solution')
print_question('paper-q2a-print')
C.fixed([k('2', 'b')], 'chem-4-1', 'a-primary-standard')
_flask = P.items(k('2', 'c'))[0].text
assert _flask == 'volumetric flask', _flask
C.fixed([k('2', 'c')], 'chem-4-1', 'the-volumetric-flask', figure=Q2,
        label_key=[{'letter': 'B', 'meaning': _flask, 'askedInThisQuestion': True}])
# (d): "ANY ONE: (9)" of four points.
C.menu([k('2', 'd')], 'chem-4-1', 'transferring-all-the-solution-to-the-flask', figure=Q2,
       note='The scheme prices the part "' + traced('ANY ONE: (9)') + '".')
# (e): the procedure, five points marked "(ANY ONE)", then the further step;
# the two priced together (9 + 3): the procedure a choice of one, as one row.
_q2e = P.items(k('2', 'e'))
assert [it.cell for it in _q2e] == ['[9 + 3]'], _q2e
_rows2e = [r.text for r in _q2e[0].rows if r.text]
assert _rows2e[0] == 'flask on level surface // [Accept “flat” for “level.”]' \
    and _rows2e[4] == 'until bottom of meniscus on (level with) mark (ANY ONE)' and len(_rows2e) == 6, _rows2e
_outline = [_rows2e[0][:-len(' // [Accept “flat” for “level.”]')]] + [bare(t) for t in _rows2e[1:4]] \
    + [_rows2e[4][:-len(' (ANY ONE)')]]
C.add([k('2', 'e')], 'chem-4-1', 'making-up-to-the-mark-and-mixing', [
    {'id': 'r-1', 'kind': 'anyN', 'verbatim': options(_outline)[0], 'marks': None, 'openList': True,
     'contextNote': 'For "Outline the procedure ...": any one of these, the scheme marking its list "'
                    + traced('(ANY ONE)') + '". The scheme adds: ' + traced('[Accept “flat” for “level.”]'),
     'group': {'claimMax': 1, 'options': options(_outline)}},
    lift('r-2', _rows2e[5], None, 'For "What further step should be taken ...?"')],
    kind='orderedSplit', notation='[9 + 3]', total=12, notes=SPLIT.format('(9 + 3)'), figure=Q2)
# (f)(i): the answer (9), then its working in a box whose stacked fractions the
# text layer cannot read (only "M = 0.14 (3)" comes through): the scheme's print
# of the working is the figure.
_q2f1 = P.items(k('2', 'f', 'i'))
assert [(it.cell, it.text) for it in _q2f1] == [('[9]', '0.14 moles per litre'), ('[3]', 'M = 0.14')], _q2f1
C.answer_only([k('2', 'f', 'i')], 'chem-4-1', 'concentration-of-hydrochloric-acid-in-moles-per-litre',
              S + 'q2f-i', notes=adds(_q2f1[1].asides))
# (ii): the answer (3), then the same three marks boxed as its working.
_q2f2 = P.items(k('2', 'f', 'ii'))
assert [(it.cell, it.text) for it in _q2f2] == [('[3]', '5.11 grams per litre'), ('[3]', '0.14 × 36.5 = 5.11')], \
    _q2f2
C.add([k('2', 'f', 'ii')], 'chem-4-1', 'concentration-of-hydrochloric-acid-in-grams-per-litre', [
    lift('r-1', _q2f2[0].text, 3, 'The scheme sets out the working in a box beneath it, "' + traced(_q2f2[1].text)
         + '" (3), the same three marks. ' + adds(_q2f2[1].asides))])

# ── Q3 Flame tests, zinc in copper(II) sulfate, and anion tests ──────────────
Q3A = FIG + 'paper-q3a'
_q3a_ask = P.ask(k('3', 'a'))
Q3A_SALTS = cut(_q3a_ask, None, 'Describe how')
assert Q3A_SALTS == 'Samples of three salts are provided on clock glasses as shown above.', _q3a_ask
_q3a = P.items(k('3', 'a'))
assert [(it.cell, it.asides) for it in _q3a] == [('[8 + 3]', ['[any two]']), ('[6 + 2 + 1]', [])], _q3a
# (a): two asks under one printed mark, each priced by a cell of its own: the
# procedure, "ANY TWO: (8 + 3)" of six points, then the three colours (6 + 2 + 1).
_flame = options(_q3a[0].options())
assert len(_flame) == 6, _flame
C.add([k('3', 'a')], 'chem-u2', 'flame-test-procedure', [anyN(
    'r-1', _flame[0], 11, 2, 8, _flame, 'Any two of these, the first (8) and the second (3): the scheme lists six '
    'points and prices them "' + traced('ANY TWO: (8 + 3)') + '".', steps=[8, 3])],
    total=11, qtext=cut(_q3a_ask, 'Describe how', 'In the case of'), stem=Q3A_SALTS, figure=Q3A)
_colours = _q3a[1].points()
assert len(_colours) == 3 and _colours[0] == 'sodium: yellow / orange', _colours
C.add([k('3', 'a')], 'chem-1-2', 'flame-colours-of-sodium-potassium-and-copper', [
    lift(f'r-{i + 1}', t, None) for i, t in enumerate(_colours)],
    kind='orderedSplit', notation='[6 + 2 + 1]', total=9, notes=SPLIT.format('(6 + 2 + 1)'),
    qtext=cut(_q3a_ask, 'In the case of'), stem=Q3A_SALTS, figure=Q3A, cid='q3-a-flame-colours',
    ref_suffix='flame colours')
# (b)(i)-(ii): the paper prints (6) for each; the scheme prices the observation
# and the explanation together, one cell (9 + 3).
assert [cells(k('3', 'b', r)) for r in ('i', 'ii')] == [[None], ['[9 + 3]']]
C.ordered([k('3', 'b', 'i'), k('3', 'b', 'ii')], 'chem-3-5', 'zinc-in-a-solution-of-copper-ions',
          figure=FIG + 'paper-q3b', row_notes={0: 'For (i).', 1: 'For (ii).'})
assert cells(k('3', 'c', 'i')) == ['[9 + 3]'], P.items(k('3', 'c', 'i'))
C.ordered([k('3', 'c', 'i')], 'chem-u2', 'test-for-the-chloride-ion',
          row_notes={0: 'For the test.', 1: 'For what is seen.'})
# (ii): "ANY TWO (2 × 3)" of five points. The next page opens "SECTION B",
# which the reader files under this part; the menu is read from the first item.
_q3c2 = P.items(k('3', 'c', 'ii'))
assert [(it.cell, it.asides) for it in _q3c2] == [('[2 × 3]', ['[any two]']), (None, [])] \
    and _q3c2[1].text == 'SECTION B', _q3c2
_ring = options(_q3c2[0].options())
assert len(_ring) == 5, _ring
C.add([k('3', 'c', 'ii')], 'chem-u2', 'brown-ring-test-for-nitrate', [anyN(
    'r-1', _ring[0], 6, 2, 3, _ring, 'Any two of these: the scheme lists five points and prices them "'
    + traced('ANY TWO (2 × 3)') + '".')], total=6)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
Q4B = FIG + 'paper-q4b'
Q4F = FIG + 'paper-q4f'
C.fixed([k('4', 'a')], 'chem-1-1', 'particles-in-a-solid', notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-3', 'atomic-radius', notes=Q4_NOTE, figure=Q4B)
assert cells(k('4', 'c')) == ['[2 × 3]'], P.items(k('4', 'c'))
C.fixed([k('4', 'c')], 'chem-3-1', 'endothermic-reaction', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-1-4', 'empirical-formula-of-ethanoic-acid', notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-4-2', 'chlorine-and-methane-in-ultraviolet-light', notes=Q4_NOTE)
assert cells(k('4', 'f')) == ['[5 + 1]'], P.items(k('4', 'f'))
C.ordered([k('4', 'f')], 'chem-u2', 'preparing-ethyne', figure=Q4F, notes=Q4_NOTE,
          row_notes={0: 'For liquid A.', 1: 'For solid B.'})
# (g): "State the shape of (i) ..., (ii) ..." is one sentence; the scheme
# numbers the two shapes and prices them together (5 + 1), and draws the water
# molecule beside (ii) (its atoms are the picture's, 'scheme-labels').
_q4g = f"{P.ask(k('4', 'g'))} (ii) {P.ask(k('4', 'g', 'ii'))}"
assert _q4g == 'State the shape of (i) the hydrogen chloride molecule (HCl), (ii) the water molecule (H₂O).', _q4g
C._criteria = []
_q4g_rows, _q4g_cell = C.split([k('4', 'g', 'i'), k('4', 'g', 'ii')], notes={0: 'For (i).', 1: 'For (ii).'})
assert _q4g_cell == '[5 + 1]' and len(_q4g_rows) == 2, (_q4g_rows, _q4g_cell)
C.add([k('4', 'g')], 'chem-2-2', 'shapes-of-hydrogen-chloride-and-water', _q4g_rows, kind='orderedSplit',
      notation=_q4g_cell, total=6, qtext=_q4g, figure=S + 'q4g',
      notes=SPLIT.format('(5 + 1)') + ' The scheme draws the water molecule beside (ii); its own print is shown '
                                      'with the answer. ' + Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-4-3', 'temporary-and-permanent-hardness', notes=Q4_NOTE)
# (i): the equation's arrow is a glyph the text layer cannot read (its line is
# 'labels'): the paper's print is the question; the scheme's answer is a
# fraction, its own print.
C.drawn([k('4', 'i')], 'chem-3-3', 'kc-expression-for-the-haber-equilibrium', S + 'q4i', notes=Q4_NOTE)
print_question('paper-q4i-print')
C.fixed([k('4', 'j')], 'chem-1-1', 'diffusion', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'fixing-nitrogen-in-nature', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-3-5', 'a-metal-extracted-by-electrolysis', notes=Q4_NOTE)

# ── Q5 Atomic structure, the periodic table and radioactivity ────────────────
# (a): two asks, each printed with its mark, (11) and (6), and priced by a cell
# of its own: the distinction (5 + 3 + 3), then the reason (6). The first's
# last point wraps short ("... ¹/₁₂ mass of" over "carbon-12 atom") and is read
# from its printed rows.
_q5a_ask = P.ask(k('5', 'a'))
_q5a = P.items(k('5', 'a'))
assert [it.cell for it in _q5a] == ['[5 + 3 + 3]', '[6]'], _q5a
_dist = _q5a[0].points()
assert len(_dist) == 4 and _dist[2].endswith('mass of') and _dist[3] == 'carbon-12 atom', _dist
C.add([k('5', 'a')], 'chem-1-2', 'mass-number-and-relative-atomic-mass', [
    lift('r-1', _dist[0], None, 'For mass number.'),
    lift('r-2', _dist[1], None, 'For relative atomic mass.'),
    lift('r-3', f'{_dist[2]} {_dist[3]}', None, 'For relative atomic mass.')],
    kind='orderedSplit', notation='[5 + 3 + 3]', total=11, notes=SPLIT.format('(5 + 3 + 3)'),
    qtext=cut(_q5a_ask, None, 'You will notice'), stem='')
C.add([k('5', 'a')], 'chem-1-2', 'why-relative-atomic-masses-are-rarely-whole-numbers', [
    lift('r-1', _q5a[1].text, 6)],
    qtext=cut(_q5a_ask, 'Give the reason'), stem=cut(_q5a_ask, 'You will notice', 'Give the reason'),
    cid='q5-a-the-reason', ref_suffix='the reason')
assert [cells(k('5', 'b', r)) for r in ('i', 'ii')] == [[None], ['[8 + 1]']]
C.ordered([k('5', 'b', 'i'), k('5', 'b', 'ii')], 'chem-1-3', 'mendeleev-and-the-modern-periodic-table',
          figure=FIG + 'paper-q5b', row_notes={0: 'For (i).', 1: 'For (ii).'})
# (c)(i): the paper underlines "radioactive"; "ANY TWO: (5 + 1)" of four points.
C.menu([k('5', 'c', 'i')], 'chem-1-2', 'radioactivity',
       note='The scheme prices the part "' + traced('ANY TWO: (5 + 1)') + '": the first (5), the second (1).')
print_question('paper-q5c-i-print')
C.fixed([k('5', 'c', 'ii')], 'chem-1-2', 'beta-particles')
# (iii): "time taken //", then the second point's wordings on three rows, the
# third set without a solidus before it (scheme PDF page 8): the first two are
# the row, the third quoted.
_q5c3 = P.items(k('5', 'c', 'iii'))
assert [it.cell for it in _q5c3] == ['[5 + 1]'], _q5c3
_hl = [r.text for r in _q5c3[0].rows if r.text]
assert _hl == ['time taken //', 'for half the radioactive atoms to decay /',
               'for half the mass (amount) (sample) of the element to decay', 'for activity to decrease by a half'], _hl
C.add([k('5', 'c', 'iii')], 'chem-1-2', 'half-life', [
    lift('r-1', bare(_hl[0]), None),
    lift('r-2', f'{_hl[1]} {_hl[2]}', None, 'The scheme prints a third line beneath, "' + traced(_hl[3])
         + '", with no solidus before it.')],
    kind='orderedSplit', notation='[5 + 1]', total=6, notes=SPLIT.format('(5 + 1)'))
C.fixed([k('5', 'c', 'iv')], 'chem-1-2', 'a-use-of-carbon-14')
C.drawn([k('5', 'd')], 'chem-1-2', 'electron-arrangement-in-carbon-14', S + 'q5d')

# ── Q6 Alkanes and alkenes ───────────────────────────────────────────────────
C.menu([k('6', 'a')], 'chem-2-4', 'sources-of-hydrocarbons',
       note='The scheme prices the part "' + traced('ANY TWO: (5 + 3)') + '": the first (5), the second (3).')
# (b)(i)-(iv): one cell (6 + 6 + 3 × 3) closes the four parts, five points.
_q6b = [k('6', 'b', r) for r in ('i', 'ii', 'iii', 'iv')]
assert [cells(x) for x in _q6b] == [[None]] * 3 + [['[6 + 6 + 3 × 3]']], [P.items(x) for x in _q6b]
C.ordered(_q6b, 'chem-2-4', 'lpg-propane-and-mercaptans', figure=FIG + 'paper-q6b',
          row_notes={0: 'For (i).', 1: 'For (ii).', 2: 'For (iii), "What are these compounds?"',
                     3: 'For (iii), "How do they make ... safer?"', 4: 'For (iv).'})
# (c): the name, then the structure the scheme draws two ways and writes
# "CH₃CH=CH₂" between them, priced together (6 + 3).
_q6c = P.items(k('6', 'c'))
assert [(it.cell, [r.text for r in it.rows]) for it in _q6c] == [
    ('[6 + 3]', ['propene / propylene', '/ – C – C = C CH₃CH=CH₂ /'])], _q6c
_q6c_ask = P.ask(k('6', 'c'))
assert _q6c_ask.endswith('Name this compound. Draw its structural formula.'), _q6c_ask
C.add([k('6', 'c')], 'chem-2-4', 'name-and-structure-of-propene', [
    lift('r-1', _q6c[0].rows[0].text, None, 'For "Name this compound."'),
    C.mark_ask(point('r-2', cut(_q6c_ask, 'Draw its'), None, DRAWN + ' It writes the structure "'
                     + traced('CH₃CH=CH₂') + '" between its two drawings.'))],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('(6 + 3)'), figure=S + 'q6c')
assert cells(k('6', 'd')) == ['[6 + 3 + 3]'], P.items(k('6', 'd'))
C.ordered([k('6', 'd')], 'chem-2-4', 'methylbenzene-and-octane-number', figure=FIG + 'paper-q6d',
          row_notes={0: 'For "Name this hydrocarbon."', 1: 'For "Would you expect its octane number to be high or '
                                                             'low?"', 2: 'For "Give a reason for your answer."'})

# ── Q7 Acids, bases and suspended and dissolved solids ───────────────────────
Q7A = FIG + 'paper-q7a'
# (a): three asks, each printed with its mark, (8), (6), (6): "Define (i)
# acid, (ii) base, ..." -- the two definitions priced together (5 + 3) --,
# then neutralisation (5 + 1) and the acid in gastric juice (5 + 1), a cell
# each. The reader files the later two under (ii).
_q7a_ask = P.ask(k('7', 'a'))
_q7a1, _q7a2 = P.items(k('7', 'a', 'i')), P.items(k('7', 'a', 'ii'))
assert [it.cell for it in _q7a1] == [None] and [it.cell for it in _q7a2] == ['[5 + 3]', '[5 + 1]', '[5 + 1]'], \
    (_q7a1, _q7a2)
C.add([k('7', 'a', 'i'), k('7', 'a', 'ii')], 'chem-3-4', 'arrhenius-acids-and-bases', [
    lift('r-1', bare(_q7a1[0].text), None, 'For (i).'),
    lift('r-2', _q7a2[0].text, None, 'For (ii). ' + adds(_q7a2[0].asides))],
    kind='orderedSplit', notation='[5 + 3]', total=8, notes=SPLIT.format('(5 + 3)'),
    qtext=cut(_q7a_ask, None, 'Explain the term'), stem='', figure=Q7A)
_neut = _q7a2[1].points()
assert len(_neut) == 2, _neut
C.add([k('7', 'a')], 'chem-3-4', 'neutralisation', [lift('r-1', _neut[0], None), lift('r-2', _neut[1], None)],
      kind='orderedSplit', notation='[5 + 1]', total=6, notes=SPLIT.format('(5 + 1)'),
      qtext=cut(_q7a_ask, 'Explain the term', 'Give the name'), stem='', cid='q7-a-neutralisation',
      ref_suffix='neutralisation')
_hcl = _q7a2[2].points()
assert _hcl == ['name: hydrochloric acid', 'formula : HCl'], _hcl
C.add([k('7', 'a')], 'chem-3-4', 'hydrochloric-acid-in-gastric-juice', [
    lift('r-1', _hcl[0], None, 'For the name.'), lift('r-2', _hcl[1], None, 'For the formula.')],
    kind='orderedSplit', notation='[5 + 1]', total=6, notes=SPLIT.format('(5 + 1)'),
    qtext=cut(_q7a_ask, 'Give the name'), stem='', cid='q7-a-gastric-juice', ref_suffix='the acid in gastric juice')
# (b): "Describe how you would measure the concentration (i) ..., (ii) ..." is
# one sentence; the scheme lists six points for each and prices the part "ANY
# THREE from (i) or (ii): (3 × 6)": any three, six each. "subtract weighings"
# closes both lists and is offered once.
_q7b1, _q7b2 = P.items(k('7', 'b', 'i')), P.items(k('7', 'b', 'ii'))
assert [it.cell for it in _q7b1] == [None] and [it.cell for it in _q7b2] == ['[3 × 6]'], (_q7b1, _q7b2)
_any3 = 'ANY THREE from (i) or (ii):'
assert _q7b2[0].text.endswith(' ' + _any3), _q7b2
_susp = [x.strip() for x in _q7b1[0].text.split('//')]
_diss = [x.strip() for x in _q7b2[0].text[:-len(_any3)].split('//')]
assert len(_susp) == 6 and len(_diss) == 6 and _susp[-1] == _diss[-1] == 'subtract weighings', (_susp, _diss)
_solids = options(_susp + _diss[:-1])
C.add([k('7', 'b')], 'chem-4-3', 'measuring-suspended-and-dissolved-solids', [anyN(
    'r-1', _solids[0], 18, 3, 6, _solids,
    'Any three of these: the scheme lists six points for (i), suspended solids (the first six here), and six for '
    '(ii), dissolved solids (the rest, its last point "subtract weighings" the same as (i)\'s), and prices the '
    'part "' + traced(_any3 + ' (3 × 6)') + '".')],
    total=18, qtext=f"{P.ask(k('7', 'b'))} (ii) {P.ask(k('7', 'b', 'ii'))}", stem='')
# (c)(i): the two answers (2 × 3), then the working in a box of fractions the
# text layer cannot read, (3) a step: the scheme's print of the working is the
# figure.
_q7c1 = P.items(k('7', 'c', 'i'))
assert [(it.cell, it.text) for it in _q7c1] == [('[2 × 3]', '0.15 g/l // 1.7 g/l'), ('[3]', ''), ('[3]', '')], _q7c1
_gl = [x.strip() for x in _q7c1[0].text.split('//')]
C.add([k('7', 'c', 'i')], 'chem-4-3', 'concentration-of-solids-in-grams-per-litre', [
    lift('r-1', _gl[0], 3, 'For the suspended solids. The scheme prices this answer and the next (2 × 3), one each.'),
    lift('r-2', _gl[1], 3, 'For the dissolved solids. ' + adds(_q7c1[2].asides))], figure=S + 'q7c-i',
    notes='The scheme sets out the working that earns each answer in a box, (3) a step; its own print is shown '
          'with the answer.')
# (ii): the two answers (2 × 3), then the working, (3) a step, quoted.
_q7c2 = P.items(k('7', 'c', 'ii'))
assert [it.cell for it in _q7c2] == ['[2 × 3]', '[3]', '[3]'], _q7c2
_ppm = [x.strip() for x in _q7c2[0].text.split('//')]
C.add([k('7', 'c', 'ii')], 'chem-4-3', 'concentration-of-solids-in-ppm', [
    lift('r-1', _ppm[0], 3, 'For the suspended solids. The scheme prices this answer and the next (2 × 3), one '
         'each, and sets out the working beneath: "' + traced(_q7c2[1].text) + '" (3).'),
    lift('r-2', _ppm[1], 3, 'For the dissolved solids. The working: "' + traced(_q7c2[2].text) + '" (3). '
         + adds(_q7c2[2].asides))])

# ── Q8 Ethanol, ethanal and ethene ───────────────────────────────────────────
Q8 = FIG + 'paper-q8'
# The question's opening sentence names X, Y and Z in the reaction scheme it
# prints: the stem of the parts that show the scheme as their figure.
Q8_LEAD = P.ask(k('8'))
assert Q8_LEAD == ('Answer the questions below with reference to the compounds X, Y and Z in the following '
                   'reaction scheme.'), Q8_LEAD
assert cells(k('8', 'a')) == ['[6 + 4 + 1]'], P.items(k('8', 'a'))
C.ordered([k('8', 'a')], 'chem-4-2', 'naming-ethanol-ethanal-and-ethene', figure=Q8, stem=Q8_LEAD,
          fixes={'X ethanol / ethyl alcohol //': 'X ethanol / ethyl alcohol'})
# (b): which compound (6), its structure (3) -- the scheme's drawing, its atoms
# the picture's ('scheme-labels') -- and the planar carbon marked (3), priced
# together (6 + 2 × 3). The reaction scheme that names Y travels with the
# question's print.
_q8b_ask = P.ask(k('8', 'b'))
_q8b = P.items(k('8', 'b'))
assert [(it.cell, it.asides) for it in _q8b] == [('[6 + 2 × 3]', ['[Allow correct structure of X, Y or Z]'])], _q8b
_q8b_pts = _q8b[0].points()
assert _q8b_pts == ['Y / CH₃CHO / ethanal / acetaldehyde / the aldehyde',
                    'planar carbon correctly identified e.g. with asterisk'], _q8b_pts
C.add([k('8', 'b')], 'chem-2-2', 'the-planar-carbon-in-ethanal', [
    lift('r-1', _q8b_pts[0], None, 'For "Which one of the compounds ... contains only one planar carbon atom?"'),
    C.mark_ask(point('r-2', cut(_q8b_ask, 'Draw the', ' and indicate'), None,
                     DRAWN + ' ' + adds(_q8b[0].asides))),
    lift('r-3', _q8b_pts[1], None, 'For "... indicate clearly the carbon atom that is in planar geometry."')],
    kind='orderedSplit', notation='[6 + 2 × 3]', total=12, notes=SPLIT.format('(6 + 2 × 3)'), figure=S + 'q8b')
print_question('paper-q8b-print')
# (c): the type of reaction (3), then the Fehling's test, "ANY TWO: (6 + 3)" of
# three points.
_q8c_ask = P.ask(k('8', 'c'))
_q8c = P.items(k('8', 'c'))
assert [(it.cell, it.asides) for it in _q8c] == [('[3]', []), ('[6 + 3]', ['[any two]'])], _q8c
_fehling = options(_q8c[1].options())
assert len(_fehling) == 3, _fehling
C.add([k('8', 'c')], 'chem-4-2', 'oxidising-ethanol-and-fehlings-test', [
    lift('r-1', _q8c[0].text, 3, 'For "What type of reaction is involved in conversion A?"'),
    anyN('r-2', _fehling[0], 9, 2, 6, _fehling, 'For "Describe how you would test product Y ...": any two of these, '
         'the first (6) and the second (3); the scheme prices them "' + traced('ANY TWO: (6 + 3)') + '".',
         steps=[6, 3])], total=12, figure=Q8, stem=Q8_LEAD)
# (d): the scheme draws the apparatus (its labels are 'scheme-labels') and
# prices "ANY TWO CORRECT LABELS: (6 + 3)", then "Give (2 × 3) for left
# assembly and right assembly"; the reader reads the first cell as words and the
# second's sentence around its cell.
_q8d = P.items(k('8', 'd'))
assert [(it.cell, it.text) for it in _q8d] == [('[2 × 3]', '(6 + 3) Give'),
                                                (None, 'for left assembly and right assembly')], _q8d
_labels8 = raw_lines(11, (140, 512, 435, 652))
assert _labels8 == ['delivery tube', 'glass wool', 'aluminium oxide', 'X', 'Z', 'test tube', 'water', 'trough',
                    'Bunsen'], _labels8
_assembly = traced('Give (2 × 3) for left assembly and right assembly')
C.add([k('8', 'd')], 'chem-u2', 'preparing-ethene-from-ethanol', [
    anyN('r-1', options(_labels8)[0], 9, 2, 6, options(_labels8),
         'Any two of these labels, the first (6) and the second (3): the scheme labels its drawing with these, X and '
         'Z among them, and prices them "' + traced('ANY TWO CORRECT LABELS: (6 + 3)') + '".', steps=[6, 3]),
    lift('r-2', 'left assembly', 3, f'The scheme: "{_assembly}".'),
    lift('r-3', 'right assembly', 3)],
    total=15, figure=S + 'q8d', notes='The scheme draws the labelled apparatus; its own print is shown with the '
                                      'answer.')
print_question('paper-q8d-print')

# ── Q9 Catalysts and rates of reaction ───────────────────────────────────────
# (a): "Define (i) rate of reaction, (ii) catalyst." is one sentence; the
# scheme prices each definition with a cell of its own, (3 + 2) and (5 + 1):
# one card each, showing the sentence.
_q9a = P.ask(k('9', 'a'))
assert _q9a == 'Define (i) rate of reaction, (ii) catalyst.', _q9a
for r, cell, concept in (('i', '[3 + 2]', 'definition-of-rate-of-reaction'), ('ii', '[5 + 1]', 'definition-of-a-catalyst')):
    assert cells(k('9', 'a', r)) == [cell], P.items(k('9', 'a', r))
    C.ordered([k('9', 'a', r)], 'chem-3-2', concept, qtext=_q9a, stem='', cid=f'q9-a-{r}',
              row_notes={0: f'For ({r}).'})
C.fixed([k('9', 'b')], 'chem-3-2', 'catalyst-for-decomposing-hydrogen-peroxide')
assert cells(k('9', 'c')) == ['[6 + 3]'], P.items(k('9', 'c'))
C.ordered([k('9', 'c')], 'chem-3-2', 'enzymes', row_notes={0: 'For the term.', 1: 'For the example.'})
# (d)(i): its second ask, "What is the reason for this difference?", prints
# at the margin (its line runs from x 50), so the reader takes it for a
# lead-in: it is (i)'s.
Q9D = FIG + 'paper-q9d'
Q9D_LEAD = P.ask(k('9', 'd'))
assert Q9D_LEAD.startswith('The flasks, A and B, shown on the right'), Q9D_LEAD
_q9d1 = f"{P.ask(k('9', 'd', 'i'))} {P.lead(k('9', 'd', 'i'))}"
assert _q9d1.endswith('between the two flasks? What is the reason for this difference?'), _q9d1
# Its answers: the difference, then the reason as two points, "different
# surface area(s) // particle size" -- three points priced (6 + 3): a cell
# pricing fewer points than the scheme lists is a choice, any two of them, the
# first (6), the second (3).
_q9d1_its = P.items(k('9', 'd', 'i'))
assert [it.cell for it in _q9d1_its] == ['[6 + 3]'], _q9d1_its
_rate = [r.text for r in _q9d1_its[0].rows if r.text]
assert _rate == ['rate slower in A / rate faster in B', 'different surface area(s) // particle size'], _rate
_rate_opts = options([_rate[0]] + [x.strip() for x in _rate[1].split('//')])
C.add([k('9', 'd', 'i')], 'chem-3-2', 'particle-size-and-rate', [anyN(
    'r-1', _rate_opts[0], 9, 2, 6, _rate_opts, 'Any two of these, the first (6) and the second (3): the scheme gives '
    'the difference, then the reason as two points, "' + traced(_rate[1]) + '", and prices the part (6 + 3).',
    steps=[6, 3])], total=9, figure=Q9D, qtext=_q9d1, stem=Q9D_LEAD)
C.fixed([k('9', 'd', 'ii')], 'chem-3-2', 'temperature-and-rate', figure=Q9D, stem=Q9D_LEAD)
# (e): "ANY TWO: (5 + 1)" of three catalysts, then the benefit (3); the paper
# prints one mark (9) for both.
_q9e = P.items(k('9', 'e'))
assert [(it.cell, it.asides) for it in _q9e] == [('[5 + 1]', ['[any two]', '[Accept symbols]']), ('[3]', [])], _q9e
_metals = options(_q9e[0].options())
assert _metals == ['platinum', 'palladium', 'rhodium'], _metals
C.add([k('9', 'e')], 'chem-3-2', 'catalytic-converters', [
    anyN('r-1', _metals[0], 6, 2, 5, _metals, 'For "Name two catalysts ...": any two of these, the first (5) and the '
         'second (1); the scheme prices them "' + traced('ANY TWO: (5 + 1)') + '". The scheme adds: [Accept symbols]',
         steps=[5, 1]),
    lift('r-2', _q9e[1].text, 3, 'For "Give one way in which ... benefits the environment."')], total=9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): three asks, each printed with its mark, (7), (9), (9), and priced by a
# cell of its own (scheme PDF page 13): the definition (4 + 3), "Explain why
# ... (i) ..., (ii) ..." (6 + 3) over the scheme's two romans, then the bonding
# (5 + 2 + 2), which the reader files under (ii).
_q10a_ask = P.ask(k('10', 'a'))
assert cells(k('10', 'a')) == ['[4 + 3]'], P.items(k('10', 'a'))
C.ordered([k('10', 'a')], 'chem-2-1', 'definition-of-electronegativity', qtext=cut(_q10a_ask, None, 'Explain why'))
_q10a1, _q10a2 = P.items(k('10', 'a', 'i')), P.items(k('10', 'a', 'ii'))
assert [it.cell for it in _q10a1] == [None] and [it.cell for it in _q10a2] == ['[6 + 3]', '[5 + 2 + 2]'], \
    (_q10a1, _q10a2)
_why = _q10a1[0].points() + _q10a2[0].points()
assert len(_why) == 2, _why
C.add([k('10', 'a', 'i'), k('10', 'a', 'ii')], 'chem-1-3', 'electronegativity-across-a-period-and-down-a-group', [
    lift('r-1', _why[0], None, 'For (i). ' + adds(_q10a1[0].asides)), lift('r-2', _why[1], None, 'For (ii).')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('(6 + 3)'),
    qtext=cut(_q10a_ask, 'Explain why', 'Use electronegativity'), stem='')
_bond = _q10a2[1].points()
assert _bond == ['HCl: polar // [Accept covalent]', 'NaCl: ionic', 'H₂: covalent'], _bond
C.add([k('10', 'a')], 'chem-2-1', 'bonding-predicted-from-electronegativity', [
    lift('r-1', 'HCl: polar', None, 'The scheme adds: ' + traced('[Accept covalent]')),
    lift('r-2', _bond[1], None), lift('r-3', _bond[2], None)],
    kind='orderedSplit', notation='[5 + 2 + 2]', total=9, notes=SPLIT.format('(5 + 2 + 2)'),
    qtext=cut(_q10a_ask, 'Use electronegativity'), cid='q10-a-bonding', ref_suffix='the bonding')
C.route([k('10', 'b', 'i')], 'chem-1-4', 'moles-of-sodium-hydrogencarbonate')
C.route([k('10', 'b', 'ii')], 'chem-1-4', 'mass-of-water-produced')
# (iii): two asks under one mark (12), each an answer (6) and its working, (3)
# a step; the scheme's next page opens "Question 10 continued", which the
# reader files under this part.
_q10b3_ask = P.ask(k('10', 'b', 'iii'))
_q10b3 = P.items(k('10', 'b', 'iii'))
assert [it.cell for it in _q10b3] == ['[6]', '[3]', '[3]', '[6]', '[3]', '[3]', None] \
    and _q10b3[6].text == 'Question 10 continued', _q10b3
C.route([k('10', 'b', 'iii')], 'chem-1-4', 'volume-of-carbon-dioxide-at-stp', take=2,
        qtext=cut(_q10b3_ask, None, 'How many molecules'))
C.add([k('10', 'b', 'iii')], 'chem-1-4', 'molecules-of-carbon-dioxide', [
    lift('r-1', _q10b3[4].text, 3), lift('r-2', _q10b3[5].text, 3, adds(_q10b3[5].asides))],
    qtext=cut(_q10b3_ask, 'How many molecules'), cid='q10-b-iii-molecules', ref_suffix='molecules',
    notes='The scheme gives the answer, ' + display(_q10b3[3].text) + ', priced (6), then the working that earns it, '
          'step by step.')
# (c)(i): four points priced (4 + 3): a cell pricing fewer points than the
# scheme lists is a choice, any two of them, the first (4), the second (3).
C.menu([k('10', 'c', 'i')], 'chem-u2', 'principle-of-chromatography', claim=2,
       note='Any two of these, the first (4) and the second (3): the scheme lists four points and prices the part '
            '(4 + 3).')
C.fixed([k('10', 'c', 'ii')], 'chem-u2', 'gas-chromatography-in-blood-alcohol-testing')
# (iii): the scheme describes paper, thin-layer and column chromatography,
# four points each, each priced "ANY THREE: (6 + 3 + 3)": one menu of the three
# lists, any three, the first (6), the others (3).
_q10c3 = P.items(k('10', 'c', 'iii'))
assert [(it.cell, it.asides) for it in _q10c3] == [('[6 + 3 + 3]', ['[any three]'])] * 3 + [
    (None, ['[Marks can be awarded for labelled diagram, and least one label being present.]'])], _q10c3
_paper = [r.text for r in _q10c3[0].rows if r.text]
_tlc = [r.text for r in _q10c3[1].rows if r.text]
_column = [r.text for r in _q10c3[2].rows if r.text]
assert _paper[0] == 'Paper chromatography' and _tlc[2] == 'Thin layer chromatography' \
    and _column[0] == 'Column chromatography', (_paper, _tlc, _column)
_footnote1 = _tlc[0]
assert _footnote1 == '* The eluent** can be at the top of the tank and move down the paper.' and _tlc[1] == 'or', _tlc
_paper_pts = [x.strip() for x in ' '.join(_paper[1:]).split('//')]
_tlc_pts = [x.strip() for x in ' '.join(_tlc[3:]).split('//')]
# Column: "dissolve mixture in eluent** // add to column /" over "add mixture
# to column // add eluent**" over "continue to add eluent** ... column //" over
# "separation occurs into bands": four points, the third set over two lines
# with no solidus between them (scheme PDF page 14): its first line is the
# option, the second quoted.
assert _column[1:] == ['dissolve mixture in eluent** // add to column /', 'add mixture to column // add eluent**',
                       'continue to add eluent** so that it flows through column //',
                       'separation occurs into bands'], _column
_col_pts = [x.strip() for x in ' '.join(_column[1:]).split('//')]
_continue = 'continue to add eluent** so that it flows through column'
assert _col_pts[2] == 'add eluent** ' + _continue and len(_col_pts) == 4, _col_pts
_col_pts[2] = 'add eluent**'
assert len(_paper_pts) == 4 and len(_tlc_pts) == 4, (_paper_pts, _tlc_pts)
_chrom = options(_paper_pts + _tlc_pts + _col_pts)
_footnote2 = _q10c3[3].text
assert _footnote2 == '** For eluent accept mobile phase or solvent or named solvent, e.g. water.', _footnote2
C.add([k('10', 'c', 'iii')], 'chem-u2', 'separating-indicators-by-chromatography', [anyN(
    'r-1', _chrom[0], 12, 3, 6, _chrom,
    'Claim three points of one method, paper, thin-layer or column chromatography, not a mix. '
    'Any three of these, the first (6), the others (3), from the method used: the scheme lists four points for '
    'paper chromatography (the first four here), four for thin-layer chromatography (the next four) and four for '
    'column chromatography (the rest; under its third, "add eluent**", it prints "' + traced(_continue)
    + '" with no solidus between), and prices each method "' + traced('ANY THREE: (6 + 3 + 3)') + '". The scheme adds: "'
    + traced(_footnote1) + '" "' + traced(_footnote2) + '" ' + ' '.join(_q10c3[3].asides), steps=[6, 3, 3])],
    total=12)

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): five blanks priced "(12 + 6 + (2 × 3) +1)"; the passage with its
# numbered blanks is the paper's print.
assert cells(k('11', 'a')) == ['[12 + 6 + (2 × 3) +1]'], P.items(k('11', 'a'))
C.ordered([k('11', 'a')], 'chem-1-2', 'history-of-the-atom',
          notes='The scheme sets the cell as "' + traced('(12 + 6 + (2 × 3) +1)') + '". Each answer is numbered by '
                                                                                     'its blank.')
print_question('paper-q11a-print')
# (b)(i)-(v): one cell (5 + 5 + 2 + 2 + 1) closes the five parts; then, set
# after (v) under marks of their own, the filtering material (3) and the
# nitrates "ANY TWO: (6 + 1)", which the reader files under (v).
_q11b_v = P.ask(k('11', 'b', 'v'))
_fluorine = cut(_q11b_v, None, 'Name the material')
_q11b = {r: P.items(k('11', 'b', r)) for r in ('i', 'ii', 'iii', 'iv', 'v')}
assert {r: [it.cell for it in x] for r, x in _q11b.items()} == {
    'i': [None], 'ii': [None], 'iii': [None], 'iv': [None], 'v': ['[5 + 5 + 2 + 2 + 1]', '[3]', '[6 + 1]']}, _q11b
_purpose = []
for r in ('i', 'ii', 'iii', 'iv'):
    t = _q11b[r][0].text
    _purpose.append(t.split(' // [')[0] if ' // [' in t else bare(t))
_purpose.append(_q11b['v'][0].text)
assert _purpose == ['clumping (removing) suspended particles', 'raising the pH', 'lowering the pH',
                    'killing harmful bacteria / sterilizing', 'preventing tooth decay'], _purpose
_accept2 = _q11b['ii'][0].text[len('raising the pH // '):]
_accept3 = _q11b['iii'][0].text[len('lowering the pH // '):]
C.add([k('11', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-4-3', 'stages-of-water-purification', [
    lift('r-1', _purpose[0], None, 'For (i).'),
    lift('r-2', _purpose[1], None, 'For (ii). The scheme adds: ' + traced(_accept2)),
    lift('r-3', _purpose[2], None, 'For (iii). The scheme adds: ' + traced(_accept3)),
    lift('r-4', _purpose[3], None, 'For (iv).'),
    lift('r-5', _purpose[4], None, 'For (v).')],
    kind='orderedSplit', notation='[5 + 5 + 2 + 2 + 1]', total=15, notes=SPLIT.format('(5 + 5 + 2 + 2 + 1)'),
    stem=P.ask(k('11', 'b')), qtext=' '.join(f'({r}) {P.ask(k("11", "b", r))}' for r in ('i', 'ii', 'iii', 'iv')) + f' (v) {_fluorine}')
C.add([k('11', 'b')], 'chem-4-3', 'filtering-material-in-water-treatment', [lift('r-1', _q11b['v'][1].text, 3)],
      qtext=cut(_q11b_v, 'Name the material', 'It is important'), stem='', cid='q11-b-filtering',
      ref_suffix='after (v), the filtering material')
_nitrate = _q11b['v'][2]
C.add([k('11', 'b')], 'chem-4-3', 'how-nitrates-get-into-water', [anyN(
    'r-1', options(_nitrate.options())[0], 7, 2, 6, options(_nitrate.options()),
    'Any two of these, the first (6) and the second (1): the scheme prices them "' + traced('ANY TWO: (6 + 1)')
    + '". ' + adds([a for a in _nitrate.asides if a != '[any two]']), steps=[6, 1])],
    total=7, qtext=cut(_q11b_v, 'Suggest two ways'), stem=cut(_q11b_v, 'It is important', 'Suggest two ways'),
    cid='q11-b-nitrates', ref_suffix='after (v), nitrates in water')
# (c)A
C.menu([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'extracting-oxygen-from-air',
       note='The scheme prices the part "' + traced('ANY TWO: (7 + 3)') + '": the first (7), the second (3).')
# (ii): two asks under one mark (9), a cell each: what the letters stand for
# (5 + 1), then a use (3).
_ca2_ask = P.ask(ka('11', 'c', 'ii', 'A'))
_ca2 = P.items(ka('11', 'c', 'ii', 'A'))
assert [it.cell for it in _ca2] == ['[5 + 1]', '[3]'], _ca2
_cfc = _ca2[0].points()
assert len(_cfc) == 2, _cfc
C.add([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'cfcs-and-hcfcs', [lift('r-1', _cfc[0], None),
                                                                  lift('r-2', _cfc[1], None)],
      kind='orderedSplit', notation='[5 + 1]', total=6, notes=SPLIT.format('(5 + 1)'),
      qtext=cut(_ca2_ask, None, 'Give one common use'))
C.add([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'uses-of-cfcs', [lift('r-1', _ca2[1].text, 3)],
      qtext=cut(_ca2_ask, 'Give one common use'), cid='q11-c-a-ii-use', ref_suffix='a use of CFCs')
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-4-3', 'importance-of-the-ozone-layer')
# (c)B(i): the paper underlines "electrochemical series".
assert cells(ka('11', 'c', 'i', 'B')) == ['[4 + 3]'], P.items(ka('11', 'c', 'i', 'B'))
C.ordered([ka('11', 'c', 'i', 'B')], 'chem-3-5', 'the-electrochemical-series')
print_question('paper-q11c-b-i-print')
C.menu([ka('11', 'c', 'ii', 'B')], 'chem-1-3', 'properties-of-transition-elements',
       note='The scheme prices the part "' + traced('ANY TWO: (2 × 3)') + '".')
assert cells(ka('11', 'c', 'iii', 'B')) == ['[3]', '[3]'], P.items(ka('11', 'c', 'iii', 'B'))
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-3-5', 'iron-corrodes-more-readily-than-copper',
        row_notes={0: 'For "Which of the two elements ...?"', 1: 'For "Give a reason for your answer."'})
# (iv): "ANY TWO: (2 × 3)" of six methods; the scheme's last four pages print
# "Blank Page", which the reader files under this part.
_cb4 = P.items(ka('11', 'c', 'iv', 'B'))
assert [(it.cell, it.asides) for it in _cb4] == [('[2 × 3]', ['[any two]']), (None, [])] \
    and _cb4[1].text == ' '.join(['Blank Page'] * 4), _cb4
_protect = options(_cb4[0].options())
assert len(_protect) == 6, _protect
C.add([ka('11', 'c', 'iv', 'B')], 'chem-3-5', 'protecting-metals-from-corrosion', [anyN(
    'r-1', _protect[0], 6, 2, 3, _protect, 'Any two of these: the scheme lists six methods and prices them "'
    + traced('ANY TWO: (2 × 3)') + '".')], total=6)


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
    Q7(a), Q10(a), Q11(b) and Q11(c) in subtotals ("(11)" then "(6)"), so the
    sum of every mark printed under the letter, not the last."""
    out = {}
    for s in P.pseg:
        q, letter, _roman, alt = s.key
        if letter and s.marks_at:
            out[(q, letter, alt)] = out.get((q, letter, alt), 0) + sum(m for _n, m in s.marks_at)
    for (q, letter, _r, _a), m in P.marks.items():
        if letter and not any(key[:2] == (q, letter) for key in out):
            out[(q, letter, None)] = m
    # A subtotal printed at the end of a line of words, which the reader strips
    # from the ask without recording where it fell: Q3(b)(ii)'s "(6)" after
    # "... in terms of electron transfer." (paper page 3), the letter's second.
    for key, (page, tail, m) in {('3', 'b', None): (3, 'in terms of electron transfer. (6)', 6)}.items():
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
