#!/usr/bin/env python3
"""2011 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2011_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2011_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2011_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2011 ol

No 2011 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The 2011 paper sets each question's number in one run with its first words
("1. The two arrangements ...") or with its first letter ("5. (a)"); chem_print
reads the first as the head (split_heads, the sitting joining OLD_OL_HEADS),
without which the paper reader found no question at all. Its scheme prints the
running footer "ATGL Chemistry 2011", "Marking Scheme", "Page N of 13" on every
page (dropped, gated to 2011 OL, Printed.__init__).

The scheme sets its "Any" beside the mark cell ("Any (2 × 3)", "Any two 2 × (4 +
3)"), which the reader reads as the last word of the answer: those menus are
built here from the points the scheme lists, the stray word asserted and left
out. It sets Q3(c)(iii)'s answer under (ii) with the cue "USE:" and no "(iii)",
Q10(a)(i)'s under the cue "WHAT (i)" in one run with (a)'s unread cell "[(4 + 4 ×
3)]", and prices Q11(c)B's unnumbered "Name the English scientist" (3) on top of
the paper's (7) + (6) + (12), capping B at 25: each is read from the scheme's own
lines below, with the page evidence.

The paper sets romans inside one sentence -- Q5(a) "Define (i) atomic number,
(ii) mass number.", Q6(a), Q7(a), Q7(d) "Calculate the pH of (i) ..., (ii) ...",
Q10(a) and Q10(c) "Define (i) oxidation, (ii) reduction" -- which the scheme
numbers; the cards follow the scheme's cells and take the paper's sentence as
their question. Several letters hold two asks under cells of their own (Q1(b)(iii),
Q7(d), Q10(a)): one card each, the later cited by what it asks. The paper prints
Q4(g)'s equilibrium with an arrow the text layer cannot read and Q9(a)'s passage
with numbered blanks: those take the paper's own print as their question. Q4(k)
and Q11(c) offer whole alternative parts A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN)

P = Printed(2011, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2011-OL-'
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
        raise Refused(f'"{text}" is not in the 2011 ol scheme')
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
    assert text.endswith('//'), text
    return text[:-2].rstrip()


def options(texts):
    """Menu options lifted from the scheme, each refused unless the gate finds it."""
    return [lift('x', t, None)['verbatim'] for t in texts]


def split_points(text):
    """The points a scheme row separates with a double solidus, as printed."""
    return [x.strip() for x in text.split('//') if x.strip()]


def less_any(text, tail=' Any'):
    """An answer less the scheme's "Any", set beside its cell ("Any (2 × 3)") and
    read by the reader as the answer's last word."""
    assert text.endswith(tail), text
    return text[:-len(tail)]


_RAW = read_lines(P.scheme_path)


def raw_lines(page, rect):
    """The scheme's own printed lines inside a region of a page, in reading order."""
    x0, y0, x1, y1 = rect
    return [l for l in _RAW if l.page == page and l.x0 >= x0 and l.y0 >= y0
            and l.x1 <= x1 and l.y1 <= y1]


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Distillation and reflux ───────────────────────────────────────────────
Q1A = FIG + 'paper-q1a'
Q1B = FIG + 'paper-q1b'
Q1 = FIG + 'paper-q1'
# (a)(i)-(ii): the technique, the experiment and what was collected at X, priced
# together (8 + 3 + 3) beside (ii)'s last answer.
assert [cells(k('1', 'a', r)) for r in ('i', 'ii')] == [[None], ['[8 + 3 + 3]']]
C.ordered([k('1', 'a', 'i'), k('1', 'a', 'ii')], 'chem-u2', 'distillation-and-the-experiment-it-served',
          figure=Q1A, row_notes={0: 'For (i).', 1: 'For (ii), "Identify an organic experiment ..."',
                                 2: 'For (ii), "What substance was collected at X ...?"'})
# (b)(i)-(iii): the process, the experiment and the purpose priced together (6 +
# 6 + 3) beside (iii)'s purpose; then (iii)'s second ask, what happens to the
# liquid, three points priced "Any (2 × 3)" (scheme PDF page 5, the "Any" beside
# the cell): any two.
_q1b1, _q1b2, _q1b3 = (P.items(k('1', 'b', r)) for r in ('i', 'ii', 'iii'))
assert [it.cell for it in _q1b1] == [None] and [it.cell for it in _q1b2] == [None] \
    and [it.cell for it in _q1b3] == ['[6 + 6 + 3]', '[2 × 3]'], (_q1b1, _q1b2, _q1b3)
_q1b3_ask = P.ask(k('1', 'b', 'iii'))
C.add([k('1', 'b', 'i'), k('1', 'b', 'iii')], 'chem-u2', 'reflux-and-the-experiment-it-served', [
    lift('r-1', bare(_q1b1[0].text), None, 'For (i).'),
    lift('r-2', bare(_q1b2[0].text), None, 'For (ii).'),
    lift('r-3', _q1b3[0].text, None, 'For (iii), "What was the purpose of carrying out this process?"')],
    kind='orderedSplit', notation='[6 + 6 + 3]', total=15, notes=SPLIT.format('(6 + 6 + 3)'), figure=Q1B,
    qtext=f"(i) {P.ask(k('1', 'b', 'i'))} (ii) {P.ask(k('1', 'b', 'ii'))} (iii) "
          f"{cut(_q1b3_ask, None, 'Explain what happens')}")
_liquid = options(split_points(less_any(' '.join(r.text for r in _q1b3[1].rows if r.text))))
assert len(_liquid) == 3, _liquid
C.add([k('1', 'b', 'iii')], 'chem-u2', 'what-happens-to-the-liquid-under-reflux', [anyN(
    'r-1', _liquid[0], 6, 2, 3, _liquid, 'Any two of these: the scheme lists three points and prices them "'
    + traced('Any (2 × 3)') + '".')], total=6, qtext=cut(_q1b3_ask, 'Explain what happens'), figure=Q1B,
    cid='q1-b-iii-explain', ref_suffix='what happens to the liquid')
# (c): the part's name (3), the sketch's connection (3) -- a criterion: the
# scheme prints no drawing -- and how it works (3).
assert cells(k('1', 'c')) == ['[3]', '[3]', '[3]'], P.items(k('1', 'c'))
_q1c_z = P.items(k('1', 'c'))[0].text
assert display(_q1c_z) == '(Liebig) condenser', _q1c_z
C.fixed([k('1', 'c')], 'chem-u2', 'the-condenser-and-its-water-supply', figure=Q1,
        row_notes={0: 'For "Name the common part labelled Z ..."',
                   1: 'For the sketch, "... clearly indicate which part of Z should be connected to the water supply '
                      'from a cold tap": the scheme prints only the criterion, and no drawing.',
                   2: 'For "How does this part of the apparatus work?"'},
        # The ask names the part "labelled Z"; its meaning is the scheme's own answer.
        label_key=[{'letter': 'Z', 'meaning': _q1c_z, 'askedInThisQuestion': True}])
C.fixed([k('1', 'd')], 'chem-u2', 'anti-bumping-granules', figure=Q1)

# ── Q2 A standard solution of sodium carbonate, and a titration ──────────────
Q2 = FIG + 'paper-q2'
C.fixed([k('2', 'a')], 'chem-4-1', 'the-volumetric-flask', figure=Q2)
assert cells(k('2', 'b')) == ['[3]', '[3]'], P.items(k('2', 'b'))
C.fixed([k('2', 'b')], 'chem-4-1', 'mixing-a-standard-solution', figure=Q2,
        row_notes={0: 'For "What should be done with A and its contents ...?"', 1: 'For "Why is this important?"'})
# (c): the answer (6), the cue "CALC.:" before it (no capital-letters cue the
# reader takes off: its full stop), then the working beneath in two routes, the
# last "(3)" read as its cell: the same six marks, quoted.
_q2c = P.items(k('2', 'c'))
assert [(it.cell, it.text) for it in _q2c] == [
    ('[6]', 'CALC.: 5.3'), ('[3]', 'x ÷ 106 (3) = 0.05 (3) / 0.05 × 106 (3) = x')], _q2c
C.add([k('2', 'c')], 'chem-4-1', 'mass-of-sodium-carbonate-for-a-standard-solution', [
    lift('r-1', '5.3', 6, 'The scheme sets out the working that earns it beneath, either way: "'
         + traced(_q2c[1].text + ' (3)') + '".')], figure=Q2)
assert cells(k('2', 'd')) == ['[3]', '[3]'], P.items(k('2', 'd'))
C.fixed([k('2', 'd')], 'chem-4-1', 'the-pipette-and-burette', figure=Q2)
# (e): the scheme names no letter of the figure; D's key is the answer it prices,
# held back as the ask's.
_q2e = P.items(k('2', 'e'))
assert [(it.cell, it.text) for it in _q2e] == [('[6]', 'Wash down sides of titration flask')], _q2e
C.fixed([k('2', 'e')], 'chem-4-1', 'the-wash-bottle', figure=Q2,
        label_key=[{'letter': 'D', 'meaning': _q2e[0].text, 'askedInThisQuestion': True}])
# (f): the indicator (3), the scheme printing "indicator", then its colour change
# "initial colour // final colour" (2 × 3), over a table of nine indicators and
# their colours (scheme PDF page 6): the indicators are the first row's menu; the
# colours are the scheme's criteria, each indicator's in its table, shown with the
# answer.
_q2f = P.items(k('2', 'f'))
assert [(it.cell, it.text) for it in _q2f[:2]] == [('[3]', 'indicator'), ('[2 × 3]', 'initial colour // final colour')] \
    and _q2f[2].cell is None and len(_q2f) == 3, _q2f
_indicators = [display(l.text) for l in raw_lines(6, (130, 420, 230, 540))]
assert _indicators == ['methyl orange', 'Methyl red', 'phenolphthalein', 'thymolphthalein', 'thymol blue',
                       'cresol purple', 'neutral red', 'phenol red', 'bromothymol blue'], _indicators
_colour = split_points(_q2f[1].text)
C.add([k('2', 'f')], 'chem-4-1', 'indicator-and-colour-change-for-a-titration', [
    anyN('r-1', options(_indicators)[0], 3, 1, 3, options(_indicators),
         'For the indicator, any one of these: the scheme prices "' + traced(_q2f[0].text) + '" (3) and tables these '
         'indicators with their colours.'),
    lift('r-2', _colour[0], 3, 'For the colour change: the scheme prices "' + traced(_q2f[1].text) + '" (2 × 3), '
         'one each, and tables each indicator\'s colour before and after the end point, shown with the answer. '
         + adds(_q2f[1].asides)),
    lift('r-3', _colour[1], 3, adds(_q2f[2].asides))], total=9, figure=S + 'q2f')
C.fixed([k('2', 'g')], 'chem-4-1', 'the-white-tile', figure=Q2)
# (h): the answer (9), "CALC.:" before it, then its working in a box of stacked
# fractions the text layer cannot order, (3) a step: the scheme's print of the
# working is the figure.
_q2h = P.items(k('2', 'h'))
assert [it.cell for it in _q2h] == ['[9]', '[3]', '[3]', '[3]'] and _q2h[0].text == 'CALC.: 0.11 M', _q2h
C.answer_only([k('2', 'h')], 'chem-4-1', 'concentration-of-hydrochloric-acid-in-moles-per-litre', S + 'q2h',
              fixes={'CALC.: 0.11 M': '0.11 M'}, notes=adds(_q2h[3].asides))

# ── Q3 The rate of decomposition of hydrogen peroxide ────────────────────────
Q3C = FIG + 'paper-q3c'
# (a): the name, then the formula under the cue "FORM.:" (its full stop keeps the
# reader from taking the cue off), priced together (5 + 3).
_q3a = P.items(k('3', 'a'))
assert [(it.cell, [r.text for r in it.rows]) for it in _q3a] == [('[5 + 3]', ['manganese dioxide', 'FORM.: MnO₂'])], _q3a
C.add([k('3', 'a')], 'chem-3-2', 'manganese-dioxide-as-the-catalyst', [
    lift('r-1', 'manganese dioxide', None, 'For the name.'),
    lift('r-2', 'MnO₂', None, 'For the formula.')],
    kind='orderedSplit', notation='[5 + 3]', total=8, notes=SPLIT.format('(5 + 3)'))
# (b): five points priced "Any (4 × 3)" (scheme PDF page 7): any four. The scheme
# prints no drawing.
_q3b = P.items(k('3', 'b'))
assert [(it.cell, it.asides) for it in _q3b] == [('[4 × 3]', ['[no diagram – deduct 3 marks]'])], _q3b
_q3b_pts = options([bare(r.text) for r in _q3b[0].rows[:4]] + [less_any(_q3b[0].rows[4].text)])
assert len(_q3b_pts) == 5 and len(_q3b[0].rows) == 5, _q3b_pts
C.add([k('3', 'b')], 'chem-u2', 'apparatus-for-measuring-the-oxygen-produced', [anyN(
    'r-1', _q3b_pts[0], 12, 4, 3, _q3b_pts, 'Any four of these: the scheme lists five points the diagram shows and '
    'prices them "' + traced('Any (4 × 3)') + '". ' + adds(_q3b[0].asides))], total=12)
assert cells(k('3', 'c', 'i')) == ['[3]', '[3]', '[6]', '[3]'], P.items(k('3', 'c', 'i'))
C.fixed([k('3', 'c', 'i')], 'chem-3-2', 'plotting-the-volume-of-oxygen-against-time', figure=Q3C)
# (ii)-(iii): the scheme sets (iii)'s answer under (ii), with the cue "USE:" and no
# "(iii)" (scheme PDF page 7, x 121, y 386; its outline, page 4, prices "(ii) FROM:
# (6); USE: (3)"); the paper prints (iii) "Use your graph to find the time at which
# the reaction was finished." (3). Each answer is carded with the part it answers.
_q3c2 = P.items(k('3', 'c', 'ii'))
assert [(it.cell, it.text) for it in _q3c2] == [('[6]', '52 ± 2 cm³'),
                                                ('[3]', '11 – 12 minutes [consistent with graph]')], _q3c2
C.add([k('3', 'c', 'ii')], 'chem-3-2', 'reading-a-volume-from-the-graph', [
    lift('r-1', _q3c2[0].text, 6, adds(_q3c2[0].asides))], figure=Q3C)
C.add([k('3', 'c', 'iii')], 'chem-3-2', 'reading-when-the-reaction-finished', [
    lift('r-1', '11 – 12 minutes', 3, 'The scheme adds: ' + traced('[consistent with graph]') + ' It sets this answer '
         'under (ii), with the cue "USE:" and no "(iii)".')], figure=Q3C)
# (d): the next page opens "SECTION B", which the reader files under this part.
C.fixed([k('3', 'd')], 'chem-3-2', 'concentration-and-rate', skip=('SECTION B',))

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
# (a): three points priced "Any (2 × 3)" (scheme PDF page 8): any two.
_q4a = P.items(k('4', 'a'))
assert [it.cell for it in _q4a] == ['[2 × 3]'], _q4a
_dalton = options(split_points(less_any(_q4a[0].text)))
assert _dalton == ['small', 'identical', 'indivisible'], _dalton
C.add([k('4', 'a')], 'chem-1-2', 'daltons-description-of-atoms', [anyN(
    'r-1', _dalton[0], 6, 2, 3, _dalton, 'Any two of these: the scheme lists three points and prices them "'
    + traced('Any (2 × 3)') + '".')], total=6, notes=Q4_NOTE)
assert cells(k('4', 'b')) == ['[2 × 3]'], P.items(k('4', 'b'))
C.fixed([k('4', 'b')], 'chem-3-1', 'the-bomb-calorimeter', notes=Q4_NOTE)
assert cells(k('4', 'c')) == ['[2 × 3]'], P.items(k('4', 'c'))
C.fixed([k('4', 'c')], 'chem-3-1', 'exothermic-reaction', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-2-4', 'raising-the-octane-number', notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-2-4', 'benzene-in-the-school-laboratory', notes=Q4_NOTE)
# (f): the reader ends the ask at its first line (its next lines are set back from
# the marker's text) and takes the rest for a lead-in: the whole is the ask.
_q4f = f"{P.ask(k('4', 'f'))} {P.lead(k('4', 'f'))}"
assert _q4f.startswith('The Irish scientist') and _q4f.endswith('What is his name?'), _q4f
C.fixed([k('4', 'f')], 'chem-2-3', 'robert-boyle', notes=Q4_NOTE, figure=FIG + 'paper-q4f', qtext=_q4f)
# (g): the equilibrium's arrow is a glyph the text layer cannot read (its line is
# 'labels'): the paper's print is the question; the scheme's answer is a
# fraction, its own print.
C.drawn([k('4', 'g')], 'chem-3-3', 'kc-expression-for-the-haber-equilibrium', S + 'q4g', notes=Q4_NOTE)
print_question('paper-q4g-print')
C.fixed([k('4', 'h')], 'chem-1-3', 'atomic-radius-across-a-period', notes=Q4_NOTE)
# (i): the answer (6), its working a fraction in a box, (3) a step: the scheme's
# print of the working is the figure.
assert [(it.cell, it.text) for it in P.items(k('4', 'i'))][0] == ('[6]', '35 %'), P.items(k('4', 'i'))
C.answer_only([k('4', 'i')], 'chem-1-4', 'percentage-of-nitrogen-in-ammonium-nitrate', S + 'q4i', notes=Q4_NOTE)
# (j): four metals priced "Any (2 × 3)": any two.
_q4j = P.items(k('4', 'j'))
assert [it.cell for it in _q4j] == ['[2 × 3]'], _q4j
_metals = options(split_points(less_any(_q4j[0].text)))
assert _metals == ['platinum', 'rhodium', 'palladium', 'cerium'], _metals
C.add([k('4', 'j')], 'chem-3-2', 'catalysts-in-the-catalytic-converter', [anyN(
    'r-1', _metals[0], 6, 2, 3, _metals, 'Any two of these: the scheme lists four metals and prices them "'
    + traced('Any (2 × 3)') + '".')], total=6, notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'uses-of-cfcs', notes=Q4_NOTE)
# (k)B: the paper rules a line under the item (page 4, y 460), read with its words.
_q4kb = P.ask(ka('4', 'k', None, 'B'))
assert _q4kb.endswith('less than 1.7%. ____________________________'), _q4kb
C.fixed([ka('4', 'k', None, 'B')], 'chem-1-3', 'carbon-in-steel', notes=Q4_NOTE,
        qtext=cut(_q4kb, None, ' ____'))

# ── Q5 Atomic structure and bonding ──────────────────────────────────────────
Q5A = P.ask(k('5', 'a'))
assert Q5A == 'Define (i) atomic number, (ii) mass number.', Q5A
# (a): "Define (i) atomic number, (ii) mass number." is one sentence; the scheme
# prices each definition with a cell of its own, (6) and (5): one card each,
# showing the sentence.
for r, cell, concept in (('i', '[6]', 'atomic-number'), ('ii', '[5]', 'mass-number')):
    assert cells(k('5', 'a', r)) == [cell], P.items(k('5', 'a', r))
    C.fixed([k('5', 'a', r)], 'chem-1-2', concept, qtext=Q5A, stem='', row_notes={0: f'For ({r}).'})
C.fixed([k('5', 'b')], 'chem-1-2', 'jj-thomson-and-the-electron', figure=FIG + 'paper-q5b')
C.fixed([k('5', 'c')], 'chem-1-2', 'electrons-in-the-second-shell')
# (d): the scheme prices the drawing by what it shows, two points (2 × 3); it
# prints no drawing.
assert cells(k('5', 'd')) == ['[2 × 3]'], P.items(k('5', 'd'))
C.fixed([k('5', 'd')], 'chem-1-2', 'electron-arrangement-of-oxygen',
        notes='The scheme prices the drawing by what it shows and prints no drawing.')
assert cells(k('5', 'e')) == ['[2 × 3]'], P.items(k('5', 'e'))
C.fixed([k('5', 'e')], 'chem-2-1', 'definition-of-electronegativity')
assert cells(k('5', 'f')) == ['[2 × 3]'], P.items(k('5', 'f'))
C.fixed([k('5', 'f')], 'chem-2-1', 'polar-covalent-bonding-in-water')
# (g): the dot and cross diagram, three points (3 × 3) -- the scheme prints no
# drawing -- then the shape (3).
assert cells(k('5', 'g')) == ['[3 × 3]', '[3]'], P.items(k('5', 'g'))
C.fixed([k('5', 'g')], 'chem-2-2', 'bonding-and-shape-of-the-water-molecule',
        row_notes={0: 'For the dot and cross diagram: the scheme prices it by what it shows, three points, and prints '
                      'no drawing.', 3: 'For "State the shape of a water molecule."'})

# ── Q6 Fuels ─────────────────────────────────────────────────────────────────
Q6D = FIG + 'paper-q6d'
# (a): the three romans are set inside one sentence; the scheme numbers the three
# gases and prices them together (2 × 4 + 3).
assert [cells(k('6', 'a', r)) for r in ('i', 'ii', 'iii')] == [[None], [None], ['[2 × 4 + 3]']]
C._criteria = []
_q6a_rows, _q6a_cell = C.split([k('6', 'a', r) for r in ('i', 'ii', 'iii')],
                               notes={0: 'For (i).', 1: 'For (ii).', 2: 'For (iii).'})
assert _q6a_cell == '[2 × 4 + 3]' and len(_q6a_rows) == 3, (_q6a_rows, _q6a_cell)
C.add([k('6', 'a')], 'chem-2-4', 'methane-butane-and-ethyne-as-fuels', _q6a_rows, kind='orderedSplit',
      notation=_q6a_cell, total=11, notes=SPLIT.format('(2 × 4 + 3)'))
C.fixed([k('6', 'b')], 'chem-2-4', 'mercaptans-in-fuel-gases')
# (c)(i)-(ii): the scheme sets no romans, but a use of each fraction under its
# name ("kerosene:", "bitumen:"), each priced (3): a card each.
_q6c = P.items(k('6', 'c'))
assert [(it.cell, it.text) for it in _q6c] == [('[3]', 'kerosene: aviation fuel / heating'),
                                               ('[3]', 'bitumen: road surfacing / roofing / water proofing')], _q6c
Q6C = P.ask(k('6', 'c'))
assert Q6C == 'Give a major use of', Q6C
Q6C_STEM = f"{P.ask(k('6'))} {P.lead(k('6', 'b'))}"
for r, (name, it), concept in (('i', ('kerosene:', _q6c[0]), 'uses-of-kerosene'),
                               ('ii', ('bitumen:', _q6c[1]), 'uses-of-bitumen')):
    C.add([k('6', 'c', r)], 'chem-2-4', concept, [
        lift('r-1', cut(it.text, it.text.split()[1]), 3, f'The scheme sets it under "{traced(name)}".')],
        qtext=f"{Q6C} ({r}) {P.ask(k('6', 'c', r))}", stem=Q6C_STEM)
assert cells(k('6', 'd', 'i')) == ['[6]', '[6]'], P.items(k('6', 'd', 'i'))
C.fixed([k('6', 'd', 'i')], 'chem-u2', 'reagents-for-preparing-ethyne', figure=Q6D)
assert cells(k('6', 'd', 'ii')) == ['[6]', '[6]'], P.items(k('6', 'd', 'ii'))
C.fixed([k('6', 'd', 'ii')], 'chem-2-4', 'burning-ethyne', figure=Q6D,
        row_notes={0: 'For "Describe what you would see ..."', 1: 'For the balanced equation.'})
C.fixed([k('6', 'e')], 'chem-2-4', 'hydrogen-as-a-fuel')

# ── Q7 Acids, bases and pH ───────────────────────────────────────────────────
# (a): "Define (i) an acid, (ii) a base, ..." is one sentence; the scheme numbers
# the two and prices them together (5 + 3).
assert [cells(k('7', 'a', r)) for r in ('i', 'ii')] == [[None], ['[5 + 3]']]
C._criteria = []
_q7a_rows, _q7a_cell = C.split([k('7', 'a', 'i'), k('7', 'a', 'ii')], notes={0: 'For (i).', 1: 'For (ii).'})
assert _q7a_cell == '[5 + 3]' and len(_q7a_rows) == 2, (_q7a_rows, _q7a_cell)
C.add([k('7', 'a')], 'chem-3-4', 'arrhenius-acids-and-bases', _q7a_rows, kind='orderedSplit',
      notation=_q7a_cell, total=8, notes=SPLIT.format('(5 + 3)'))
# (b): the scheme prints only what each point is.
assert [(it.cell, it.text) for it in P.items(k('7', 'b'))] == [('[3]', 'valid acid'), ('[3]', 'valid base')]
C.fixed([k('7', 'b')], 'chem-3-4', 'household-acids-and-bases',
        row_notes={0: 'The scheme prints only what the point is: a valid common household acid.',
                   1: 'The scheme prints only what the point is: a valid common household base.'})
assert cells(k('7', 'c')) == ['[2 × 3]', '[6]'], P.items(k('7', 'c'))
C.fixed([k('7', 'c')], 'chem-3-4', 'neutralisation',
        row_notes={0: 'For "Explain the term neutralisation."', 2: 'For "Give one everyday example."'})
# (d): three asks under the paper's (6) and (12), each priced by a cell of its own
# (scheme PDF page 9): the definition (6), its breakdown "{– log ₁₀ (3) [H⁺] (3)}"
# set beneath (read in two pieces around its first "(3)", with the next cue
# "CALC.:"), then (i) (9) and (ii) (3), each answer with its working in a box.
# The paper sets (i) and (ii) inside one sentence.
_q7d_ask = P.ask(k('7', 'd'))
_q7d = P.items(k('7', 'd'))
assert [(it.cell, it.text) for it in _q7d] == [('[6]', '– log ₁₀ [H⁺]'), ('[3]', '{– log ₁₀'),
                                               (None, '[H⁺] (3)} CALC.:')], _q7d
C.add([k('7', 'd')], 'chem-3-4', 'definition-of-ph', [
    lift('r-1', _q7d[0].text, 6, 'The scheme breaks the mark down beneath: "' + traced('{– log ₁₀ (3) [H⁺] (3)}')
         + '".')], qtext=cut(_q7d_ask, None, 'Calculate'), stem='', ref_suffix='define pH')
_q7d_calc = cut(_q7d_ask, 'Calculate')
assert _q7d_calc == 'Calculate the pH of (i) 0.1 M hydrochloric acid (HCl), (ii) 0.1 M sulfuric acid (H₂SO₄).', \
    _q7d_calc
_q7d1, _q7d2 = P.items(k('7', 'd', 'i')), P.items(k('7', 'd', 'ii'))
assert [(it.cell, it.text) for it in _q7d1] == [('[9]', '1'), ('[3]', '{– log ₁₀ [0.1] (6)}= 1')] \
    and [(it.cell, it.text) for it in _q7d2] == [('[3]', '0.7'), ('[3]', '{– log ₁₀ [0.2]}= 0.7')], (_q7d1, _q7d2)
C.add([k('7', 'd', 'i')], 'chem-3-4', 'ph-of-hydrochloric-acid', [
    lift('r-1', '1', 9, 'For (i). The scheme sets out the working that earns it in a box: "'
         + traced(_q7d1[1].text + ' (3)') + '".')], qtext=_q7d_calc, stem='')
C.add([k('7', 'd', 'ii')], 'chem-3-4', 'ph-of-sulfuric-acid', [
    lift('r-1', '0.7', 3, 'For (ii). The scheme sets out the working in a box, the same three marks: "'
         + traced(_q7d2[1].text + ' (3)') + '".')], qtext=_q7d_calc, stem='')
C.fixed([k('7', 'e')], 'chem-3-4', 'limitation-of-the-ph-scale')

# ── Q8 Ethene, ethanol, ethanal and ethanoic acid ────────────────────────────
Q8 = FIG + 'paper-q8'
# The question's opening sentence names W, X, Y and Z in the reaction scheme it
# prints (its formulae and letters are the picture's, 'paper'): the stem of every
# part, which the reader's context leaves out as an instruction ("Answer ...").
Q8_LEAD = P.ask(k('8'))
assert Q8_LEAD == ('Answer the questions below with reference to compounds W, X, Y and Z in the following reaction '
                   'scheme.'), Q8_LEAD
C.fixed([k('8', 'a')], 'chem-2-2', 'tetrahedral-carbon-atoms', figure=Q8, stem=Q8_LEAD)
assert cells(k('8', 'b')) == ['[4 × 3]'], P.items(k('8', 'b'))
C.fixed([k('8', 'b')], 'chem-4-2', 'naming-ethene-ethanol-ethanal-and-ethanoic-acid', figure=Q8, stem=Q8_LEAD)
# (c)(i)-(ii): one sentence after "What word describes", priced together (9 + 3).
assert [cells(k('8', 'c', r)) for r in ('i', 'ii')] == [[None], ['[9 + 3]']]
C.ordered([k('8', 'c', 'i'), k('8', 'c', 'ii')], 'chem-4-2', 'hydration-and-oxidation', figure=Q8,
          row_notes={0: 'For (i).', 1: 'For (ii).'}, stem=Q8_LEAD,
          qtext=f"{P.ask(k('8', 'c'))} {C.qtext([k('8', 'c', 'i'), k('8', 'c', 'ii')])}")
assert cells(k('8', 'd')) == ['[2 × 3]'], P.items(k('8', 'd'))
C.fixed([k('8', 'd')], 'chem-4-2', 'test-for-unsaturation', figure=Q8, stem=Q8_LEAD)
C.fixed([k('8', 'e')], 'chem-4-2', 'household-use-of-ethanoic-acid', figure=Q8, stem=Q8_LEAD)
assert cells(k('8', 'f')) == ['[6 + 3]'], P.items(k('8', 'f'))
C.ordered([k('8', 'f')], 'chem-4-2', 'polymerising-ethene', figure=Q8, stem=Q8_LEAD,
          row_notes={0: 'For "Which of the compounds can be polymerised ...?"', 1: 'For the name of the plastic.'})

# ── Q9 Water and sewage treatment ────────────────────────────────────────────
# (a): six blanks priced "[(3 × 9) + (3 × 3)]" without saying which blank earns
# which; the passage with its numbered blanks is the paper's print.
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a] == ['[(3 × 9) + (3 × 3)]'], _q9a
_blanks = [r.text for r in _q9a[0].rows if r.text]
assert [b[:2] for b in _blanks] == ['1:', '2:', '3:', '4:', '5:', '6:'], _blanks
C.add([k('9', 'a')], 'chem-4-3', 'stages-of-water-treatment', [
    lift(f'r-{i + 1}', b, None) for i, b in enumerate(_blanks)],
    kind='orderedSplit', notation='[(3 × 9) + (3 × 3)]', total=36,
    notes=SPLIT.format('"' + traced('[(3 × 9) + (3 × 3)]') + '"') + ' Each answer is numbered by its blank.')
print_question('paper-q9a-print')
# (b): for each of three stages a process // its effect, priced "Any two 2 × (4 +
# 3)" (scheme PDF page 11, the label beside the cell, which the reader reads as
# "[4 + 3]" and the words "Any two 2 ×" at the end of the last answer): the
# processes of any two stages (4) each, and their effects (3) each.
_q9b = P.items(k('9', 'b'))
assert [it.cell for it in _q9b] == ['[4 + 3]', None] and _q9b[1].text == '[* settling can only be used once]', _q9b
_r9 = [r.text for r in _q9b[0].rows if r.text]
assert len(_r9) == 8, _r9
_process = options([bare(_r9[0]), f'{_r9[2]} {bare(_r9[3])}', f'{_r9[5]} {bare(_r9[6])}'])
_effect = options([_r9[1], _r9[4], less_any(_r9[7], ' Any two 2 ×')])
assert [p.split(':')[0] for p in _process] == ['primary', 'secondary', 'tertiary'], _process
_any9 = traced('Any two 2 × (4 + 3)')
C.add([k('9', 'b')], 'chem-4-3', 'stages-of-sewage-treatment', [
    anyN('r-1', _process[0], 8, 2, 4, _process, 'For the processes of any two stages, (4) each: the scheme prices '
         'each stage\'s process and its effect "' + _any9 + '". The scheme adds: ' + _q9b[1].text),
    anyN('r-2', _effect[0], 6, 2, 3, _effect, 'For the effects of the same two stages, (3) each, in the scheme\'s '
         'order: primary, secondary, tertiary.')], total=14)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the flame test, six points, then the colours. The scheme sets the test's
# cell "[(4 + 4 × 3)]" (PDF page 14, x 486, y 167) in a form the reader does not
# read as a cell, and (i)'s answer under the cue "WHAT (i)" (x 73, y 191) with no
# colon, so the test's points, its cell and (i)'s answer come as one item under
# (a), and (ii)'s answer and the colours' cell (6 + 3) under (ii). Six points
# priced (4 + 4 × 3), five: a choice, any five, the first (4), the others (3).
_q10a_ask = P.ask(k('10', 'a'))
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == [None], _q10a
_q10a_text = _q10a[0].text
_cell10a = ' [(4 + 4 × 3)] WHAT (i) '
assert _q10a_text.count(_cell10a) == 1 and _q10a_text.endswith(' //'), _q10a_text
_test_text, _sodium = _q10a_text.split(_cell10a)
_flame = options(split_points(_test_text))
assert len(_flame) == 6, _flame
Q10A_STEM = cut(_q10a_ask, None, 'Describe how')
assert Q10A_STEM == 'A flame test can be used to identify the metal present in a salt.', Q10A_STEM
C.add([k('10', 'a')], 'chem-u2', 'flame-test-procedure', [anyN(
    'r-1', _flame[0], 16, 5, 4, _flame, 'Any five of these, the first (4), the others (3): the scheme lists six '
    'points and prices them "' + traced('[(4 + 4 × 3)]') + '".', steps=[4, 3, 3, 3, 3])],
    total=16, qtext=cut(_q10a_ask, 'Describe how'), stem=Q10A_STEM)
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [(it.cell, it.text) for it in _q10a2] == [('[6 + 3]', 'lilac / purple')], _q10a2
C.add([k('10', 'a', 'i'), k('10', 'a', 'ii')], 'chem-1-2', 'flame-colours-of-sodium-and-potassium', [
    lift('r-1', bare(_sodium), None, 'For (i).'), lift('r-2', _q10a2[0].text, None, 'For (ii).')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('(6 + 3)'),
    qtext=f"{P.lead(k('10', 'a'))} (i) {P.ask(k('10', 'a', 'i'))} (ii) {P.ask(k('10', 'a', 'ii'))}",
    stem=Q10A_STEM)
C.fixed([k('10', 'b', 'i')], 'chem-u2', 'chromatography-in-forensic-science')
# (b)(ii): "see table below" priced "Any (5 × 3)" (scheme PDF page 14): the table
# sets six points for a plate in a tank (left) and six for a column (right), the
# last two the same in both: one menu of the ten, any five.
_q10b2 = P.items(k('10', 'b', 'ii'))
assert [(it.cell, it.text, it.asides) for it in _q10b2][0] == (
    '[5 × 3]', 'see table below Any', ['[some points can be got from a diagram]']) and len(_q10b2) == 2, _q10b2
_table = raw_lines(14, (108, 323, 520, 430))
assert display(_table[0].text) == 'Chromatography', _table
_left = [display(l.text) for l in _table[1:] if l.x0 < 300]
_right = [display(l.text) for l in _table[1:] if l.x0 > 300]
assert _right[4] == 'column' and _right[3].endswith('addition to'), _right
_right = _right[:3] + [f'{_right[3]} {_right[4]}'] + _right[5:]
assert len(_left) == len(_right) == 6 and _left[4:] == _right[4:] == ['Elution', 'Separation observed'], (_left, _right)
_chrom = options(_left + _right[:4])
C.add([k('10', 'b', 'ii')], 'chem-u2', 'a-chromatography-experiment', [anyN(
    'r-1', _chrom[0], 15, 5, 3, _chrom, 'Any five of these, from the method described: the scheme prints "'
    + traced(less_any(_q10b2[0].text)) + '", tables six points for a plate in a tank (the first six here) and six '
    'for a column (the rest, its last two, "Elution" and "Separation observed", the same as the first column\'s), and '
    'prices them "' + traced('Any (5 × 3)') + '". ' + adds(_q10b2[0].asides))], total=15, figure=S + 'q10b-ii',
    notes='The scheme\'s table is shown with the answer.')
assert cells(k('10', 'b', 'iii')) == ['[2 × 3]'], P.items(k('10', 'b', 'iii'))
C.fixed([k('10', 'b', 'iii')], 'chem-u2', 'principle-of-chromatography')
# (c)(i)-(ii): "Define (i) oxidation, (ii) reduction, ..." is one sentence; the
# scheme numbers the two and prices them together (4 + 3).
Q10C = P.ask(k('10', 'c'))
assert Q10C == 'Define (i) oxidation, (ii) reduction, in terms of electron transfer.', Q10C
assert [cells(k('10', 'c', r)) for r in ('i', 'ii')] == [[None], ['[4 + 3]']]
C._criteria = []
_q10c_rows, _q10c_cell = C.split([k('10', 'c', 'i'), k('10', 'c', 'ii')], notes={0: 'For (i).', 1: 'For (ii).'})
assert _q10c_cell == '[4 + 3]' and len(_q10c_rows) == 2, (_q10c_rows, _q10c_cell)
C.add([k('10', 'c', 'i'), k('10', 'c', 'ii')], 'chem-3-5', 'oxidation-and-reduction-by-electron-transfer',
      _q10c_rows, kind='orderedSplit', notation=_q10c_cell, total=7, notes=SPLIT.format('(4 + 3)'), qtext=Q10C,
      stem='')
# (iii): the equation the paper prints after (ii), its arrow a glyph the text
# layer cannot read, is the picture; its sentence is the stem.
Q10C_EQ = P.lead(k('10', 'c'))
assert Q10C_EQ == ('The equation below describes the reaction between magnesium and chlorine to form magnesium '
                   'chloride.'), Q10C_EQ
assert cells(k('10', 'c', 'iii')) == ['[3 × 3]'], P.items(k('10', 'c', 'iii'))
C.fixed([k('10', 'c', 'iii')], 'chem-3-5', 'substances-oxidised-and-reduced', figure=FIG + 'paper-q10c-eq',
        stem=Q10C_EQ, row_notes={0: 'For the substance oxidised.', 1: 'For the substance reduced.',
                                 2: 'For "Justify your answer."'})
# (iv): four points priced "Any (3 × 3)": any three.
_q10c4 = P.items(k('10', 'c', 'iv'))
assert [it.cell for it in _q10c4] == ['[3 × 3]'], _q10c4
_chloride = options(split_points(less_any(_q10c4[0].text)))
assert len(_chloride) == 4, _chloride
C.add([k('10', 'c', 'iv')], 'chem-u2', 'test-for-the-chloride-ion', [anyN(
    'r-1', _chloride[0], 9, 3, 3, _chloride, 'Any three of these: the scheme lists four points and prices them "'
    + traced('Any (3 × 3)') + '".')], total=9, stem='')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q11A = FIG + 'paper-q11a'
# (a): two points priced together (4 + 3).
_q11a = P.items(k('11', 'a'))
assert [it.cell for it in _q11a] == ['[4 + 3]'], _q11a
_radio = split_points(_q11a[0].text)
assert len(_radio) == 2, _radio
C.add([k('11', 'a')], 'chem-1-2', 'radioactivity', [lift('r-1', _radio[0], None), lift('r-2', _radio[1], None)],
      kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'))
# (i)-(ii): (a)'s own ask, "What is radioactivity?", is no lead-in of theirs.
assert cells(k('11', 'a', 'i')) == ['[3 × 3]', '[3]'], P.items(k('11', 'a', 'i'))
C.fixed([k('11', 'a', 'i')], 'chem-1-2', 'alpha-beta-and-gamma-radiation', stem='',
        row_notes={0: 'For the three types.', 3: 'For "Which is the most penetrating ...?"'})
assert cells(k('11', 'a', 'ii')) == ['[2 × 3]'], P.items(k('11', 'a', 'ii'))
C.fixed([k('11', 'a', 'ii')], 'chem-1-2', 'radium-and-polonium', figure=Q11A, stem='')
# (b)(i)-(iii): each answer priced for the whole part, its working beneath on one
# line under a cell of its own that adds to the same marks: the answer is the
# row, the working quoted.
Q11B = FIG + 'paper-q11b-eq'
for r, concept, working in (('i', 'moles-of-aluminium', ('[9]', '0.1', '[3 × 3]', '2.7 ÷ 27 = 0.1', '(3 × 3)')),
                            ('ii', 'moles-of-hydrochloric-acid', ('[4]', '0.3', '[4]', '0.1 × 3', '(4)')),
                            ('iii', 'mass-of-aluminium-chloride',
                             ('[12]', '13.35', '[4 × 3]', '[27 + 3(35.5)] × 0.1', '(4 × 3)'))):
    its = P.items(k('11', 'b', r))
    assert [(it.cell, it.text) for it in its] == [working[:2], working[2:4]], its
    total = int(working[0].strip('[]'))
    C.add([k('11', 'b', r)], 'chem-1-4', concept, [
        lift('r-1', working[1], total, 'The scheme sets out the working that earns it beneath: "'
             + traced(working[3]) + '" ' + working[4] + '.')], figure=Q11B)
# (c)A
Q11CA = FIG + 'paper-q11c-a'
# (i): the explanation, two points (2 × 2), then two consequences priced (2 × 3)
# from the four the scheme prints as alternatives: any two.
_ca1 = P.items(ka('11', 'c', 'i', 'A'))
assert [it.cell for it in _ca1] == ['[2 × 2]', '[2 × 3]'], _ca1
_explain = split_points(_ca1[0].text)
_conseq = options([x.strip() for x in _ca1[1].text.split('/')])
assert len(_explain) == 2 and len(_conseq) == 4, (_explain, _conseq)
C.add([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'the-greenhouse-effect', [
    lift('r-1', _explain[0], 2, 'For "Explain the greenhouse effect." The scheme prices this point and the next '
         '(2 × 2), one each.'),
    lift('r-2', _explain[1], 2),
    anyN('r-3', _conseq[0], 6, 2, 3, _conseq, 'For "State two possible consequences ...": any two of these; the '
         'scheme prints them as alternatives and prices two (2 × 3).')], total=10, figure=Q11CA)
assert cells(ka('11', 'c', 'ii', 'A')) == ['[6 + 3]'], P.items(ka('11', 'c', 'ii', 'A'))
C.ordered([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'methane-and-water-vapour-in-the-atmosphere', figure=Q11CA)
# (iii): the name and the formula (2 × 3), each a list of alternatives, the
# scheme's bracketed alternative names kept on the row; then "Correct name and
# formula matched for full marks", quoted.
_ca3 = P.items(ka('11', 'c', 'iii', 'A'))
assert [it.cell for it in _ca3] == ['[2 × 3]', None], _ca3
_oxide = split_points(' '.join(r.text for r in _ca3[0].rows if r.text))
assert len(_oxide) == 2 and _oxide[1] == 'NO / NO₂ / SO₂ / SO₃', _oxide
C.add([ka('11', 'c', 'iii', 'A')], 'chem-4-3', 'oxides-that-cause-acid-rain', [
    lift('r-1', _oxide[0], 3, 'For the name. The scheme prices the name and the formula (2 × 3), one each.'),
    lift('r-2', _oxide[1], 3, 'For the formula. The scheme adds: "' + traced(_ca3[1].text) + '"')], figure=Q11CA)
# (c)B: the paper prints no mark for "Name the English scientist ..." (its marks
# are (7), (6) and (12), 25); the scheme prices it "WHO: (3)" and caps B, "[Q 11 (c)
# B can receive a maximum of 25 marks]" (PDF pages 4 and 15).
Q11CB = FIG + 'paper-q11c-b'
_cap = traced('[Q 11 (c) B can receive a maximum of 25 marks]')
assert [(it.cell, it.text) for it in P.items(ka('11', 'c', None, 'B'))] == [('[3]', 'Humphry Davy')]
C.fixed([ka('11', 'c', None, 'B')], 'chem-3-5', 'humphry-davy', figure=Q11CB, stem='', ref_suffix='the scientist',
        row_notes={0: 'The paper prints no mark for this ask; the scheme prices it "' + traced('WHO: (3)')
                      + '" and adds: ' + _cap})
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-3-5', 'isolating-sodium-by-electrolysis', figure=Q11CB)
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-3-5', 'why-sodium-is-not-extracted-in-a-blast-furnace', figure=Q11CB)
_cb3 = P.items(ka('11', 'c', 'iii', 'B'))
assert [(it.cell, it.asides) for it in _cb3] == [('[6]', []), ('[6]', [_cap])], _cb3
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-3-5', 'galvanising-iron', figure=Q11CB,
        row_notes={0: 'For "How is iron galvanised?"', 1: 'For "How does galvanising protect iron from corrosion?"'})


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
    """Every letter's printed marks, alternatives apart: the paper prints Q1(a)-(c),
    Q3(c), Q5(g), Q6(d), Q7(d), Q10 and Q11's letters in subtotals ("(6)" then
    "(12)"), so the sum of every mark printed under the letter, not the last."""
    out = {}
    for s in P.pseg:
        q, letter, _roman, alt = s.key
        if letter and s.marks_at:
            out[(q, letter, alt)] = out.get((q, letter, alt), 0) + sum(m for _n, m in s.marks_at)
    for (q, letter, _r, _a), m in P.marks.items():
        if letter and not any(key[:2] == (q, letter) for key in out):
            out[(q, letter, None)] = m
    # A subtotal printed at the end of a line of words, which the reader strips
    # from the ask without recording where it fell: Q6(d)(i)'s "(12)" after "...
    # suitable for this preparation." (paper page 5) and Q11(c)A(i)'s "(10)" after
    # "... of an increased greenhouse effect." (page 7), each its letter's first.
    for key, (page, tail, m) in {('6', 'd', None): (5, 'suitable for this preparation. (12)', 12),
                                 ('11', 'c', 'A'): (7, 'of an increased greenhouse effect. (10)', 10)}.items():
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
        if key == ('11', 'c', 'B'):
            # The scheme prices B's unnumbered "Name the English scientist" (3), which
            # the paper prints no mark for, and caps B at the paper's 25.
            out.append(f'{label} printed {want.get(key)}, scheme 3 more for the scientist, capped "{_cap}", '
                       f'carded {got.get(key)}' + ('' if got.get(key) == want.get(key) + 3 else '   <-- differs'))
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
