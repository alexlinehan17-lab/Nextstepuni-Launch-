#!/usr/bin/env python3
"""2010 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2010_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2010_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2010_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2010 hl

No 2010 Higher card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its steps where the text layer carries them cleanly, the other routes' steps
as alternatives beside them, and the scheme's own print of the working as the
card's figure.

Reader (chem_print, gated to 2010 HL). The paper sets the head of Question 4 in
one run with its words ("4. Answer eight of the following items ..."), as the
2012 Higher paper does; unread, the paper reader found Questions 1-3 only
(OLD_OL_HEADS joined). The scheme's running footer "page N of 14" (lower case)
and its head "SECTION B" were filed as answers of the part before them: dropped
(chem_print.Printed, the 2010 HL block). With the paper reader whole, the census
reads Q4(k) and Q11(c) as their A and B alternatives (paper_census.
chemistry_choice_parts): 74 -> 78 asks, no flags.

Romans the paper sets inside one sentence are one census ask and a card per
scheme cell, each showing the sentence with a "For (i)."-style note: Q8(b) and
Q11(b) (a cell each) and Q8(c)'s calculation (a cell each); Q9(b) (one cell over
both: one card). Q5(b) sets its romans on lines of their own and the census
keeps Q5(b) whole, as it keeps 2014 OL Q8(c) of the same shape; the scheme
prices them (3 x 3), one card. Q10(a) lists three compounds "(i) hydrogen
chloride, HCl, (ii) water, H2O, (iii) ammonia, NH3." inside its sentence; the
paper reader takes the list's markers for parts, so the sentence is read back
from them. Where a letter prints a mark after each of several asks, each run is
a card cited with what it holds (Q8(a), Q8(c), Q10(a), Q11(b)). Asks the paper
sets after a letter's last roman are cards cited "— after (iii)" (Q1(e)
"Repeat these calculations ...", Q11(c)A's bucky balls and X-ray pioneers).
Q4(k) and Q11(c) offer alternative parts A and B; the scheme sets Q4(k)'s B
after "or" with no letter of its own.

The paper underlines the terms Q7(a) asks about, which no text layer carries:
that card takes the paper's own print as its question, as do the parts whose
answer is a scheme crop and whose ask needs the paper's data, equation or
reaction scheme (Q2(d), Q3(d), Q6(e), Q7(c), Q9(c), Q9(e), Q9(f)). The paper
draws the arrows of the Q1, Q7 and Q8 equations and stacks the nuclide numbers
of Q11(b)'s: those equations are paper crops, kept out of the text, as are the
Q2 equation and apparatus, the Q3 table, the Q6 hydrocarbons, the reaction
scheme, the Q11(a) electrolysis cell and the bucky ball.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, point, read_lines, tidy  # noqa: E402

P = Printed(2010, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2010-HL-'
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
        raise Refused(f'"{text}" is not in the 2010 hl scheme')
    return text


def cut(text, at):
    """`text` split where `at` begins (the paper's print, cut between two asks
    it sets in one run)."""
    i = text.index(at)
    return text[:i].strip(), text[i:].strip()


def split_asides(text):
    """(the answer, its examiner's asides): the asides the scheme sets inside an
    answer's line lifted out."""
    from chem_print import INLINE_ASIDE
    asides = INLINE_ASIDE.findall(text)
    return tidy(INLINE_ASIDE.sub(' ', text)), [a.strip() for a in asides]


def pts(item):
    """An item's "//"-separated points, as printed."""
    return [display(x).strip() for x in item.text.split('//')]


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 Total hardness before and after a deioniser, by edta titration ────────
# The equation the lead-in ends with (paper page 2, y 190) draws its arrow, which
# the text layer does not carry: it is the paper's crop 'paper-q1-eq', the figure
# of the (e) cards that need it; the other cards' stem ends before it.
Q1_FULL = C.context(k('1', 'a'))
assert Q1_FULL.endswith('(represented by H₂Y²⁻) is given in the following balanced equation.'), Q1_FULL
Q1_STEM = cut(Q1_FULL, 'The reaction between')[0]
Q1EQ = FIG + 'paper-q1-eq'
# (a): NAME "Ethylenediamine // tetraacetic acid (3 + 2)", or "1,2-bis[bis(carboxymethyl)
# amino] // ethane. (3 + 2)" (scheme page 5, y 112-152): one name in two points.
_q1a = P.items(k('1', 'a'))
assert [it.cell for it in _q1a] == ['[3 + 2]', '[3 + 2]'] and pts(_q1a[0]) == ['Ethylenediamine', 'tetraacetic acid'] \
    and pts(_q1a[1]) == ['1,2-bis[bis(carboxymethyl)amino]', 'ethane.'], _q1a
C.add([k('1', 'a')], 'chem-4-1', 'the-full-name-of-edta', [
    menu_row('r-1', [pts(_q1a[0])[0], pts(_q1a[1])[0]], 1, 'One of these: the first name\'s first part, or, after "or", '
             'the second name\'s; the scheme prices the two parts of each name (3 + 2).'),
    menu_row('r-2', [pts(_q1a[0])[1], 'ethane'], 1, 'And the second part of that same name.')],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), stem=Q1_STEM)
C.fixed([k('1', 'b')], 'chem-4-1', 'indicator-for-an-edta-titration-and-its-colour-change', stem=Q1_STEM,
        row_notes={0: 'NAME.', 1: 'COLOURS.'})
C.fixed([k('1', 'c')], 'chem-4-1', 'the-buffer-in-an-edta-titration', stem=Q1_STEM,
        row_notes={0: 'PURPOSE.', 1: 'BUFFER.', 2: 'PROBLEM.'})
# (d): EXPLAIN, four points "ANY TWO: (2 × 3)" (scheme page 5, y 352-379), the cell set in
# one run with the last point.
_two1 = raw(5, 363, 380, 160)
assert _two1.endswith(' On white surface ANY TWO: (2 × 3)'), _two1
_two1 = _two1[-len('ANY TWO: (2 × 3)'):]
C.menu([k('1', 'd')], 'chem-4-1', 'swirling-and-washing-down-during-a-titration', claim=2, stem=Q1_STEM,
       fixes={'On white surface ANY TWO:': 'On white surface'}, note='"' + _two1 + '".')
# (e): the paper sets (i)-(iii) on lines of their own (page 2, y 426-464) completing
# one sentence, then "Repeat these calculations for the water after ion-exchange."
# under the letter's one mark (15). The scheme prices (i) (6), its working in a box
# (3) and (3); (ii) (3); (iii) (3); REPEAT (3): a card each, the repeat cited after
# (iii).
Q1E_IN = P.ask(k('1', 'e'))
assert Q1E_IN.startswith('It was found that') and Q1E_IN.endswith('before ion exchange in'), Q1E_IN
Q1E_PPM, Q1E_REPEAT = cut(P.ask(k('1', 'e', 'iii')), 'Repeat these')
Q1E = (Q1E_IN + ' (i) ' + P.ask(k('1', 'e', 'i')) + ' (ii) ' + P.ask(k('1', 'e', 'ii')) + ' (iii) ' + Q1E_PPM)
assert Q1E.endswith('(iii) ppm in terms of CaCO₃.') and \
    Q1E_REPEAT == 'Repeat these calculations for the water after ion-exchange.', (Q1E, Q1E_REPEAT)
_q1e1 = P.items(k('1', 'e', 'i'))
assert [it.cell for it in _q1e1] == ['[6]', '[3]', '[3]'] and display(_q1e1[0].text) == '1.84 × 10⁻³ / 0.00184 M', _q1e1
assert display(_q1e1[1].text) == '50 × M 9.2 × 0.01 =' and \
    display(_q1e1[2].text) == '1 1 Concentration = 1.84 × 10⁻³ M', _q1e1
C.add([k('1', 'e', 'i')], 'chem-4-1', 'hardness-in-moles-per-litre-from-an-edta-titre', [
    lift('r-1', '50 × M = 9.2 × 0.01', 3, 'For (i). The scheme gives the answer, "1.84 × 10⁻³ / 0.00184 M", priced (6), '
         'then works it in a box: 50 × M over 1 = 9.2 × 0.01 over 1, each side set as a fraction, (3).'),
    lift('r-2', 'Concentration = 1.84 × 10⁻³ M', 3)],
    qtext=Q1E, stem=Q1_FULL, figure=Q1EQ)
_q1e2, _q1e3 = P.items(k('1', 'e', 'ii')), P.items(k('1', 'e', 'iii'))
assert [(it.cell, display(it.text), it.asides) for it in _q1e2] == [
    ('[3]', '1.84 × 10⁻¹ / 0.184', ['[Answer (i) × 100]'])], _q1e2
C.add([k('1', 'e', 'ii')], 'chem-4-1', 'hardness-in-grams-per-litre-of-calcium-carbonate', [
    lift('r-1', _q1e2[0].text, 3, 'For (ii). The scheme adds: ' + _q1e2[0].asides[0])],
    qtext=Q1E, stem=Q1_FULL, figure=Q1EQ)
assert [it.cell for it in _q1e3] == ['[3]', '[3]'] and display(_q1e3[0].text) == '184' and \
    _q1e3[0].asides == ['[Answer (ii) × 1000]'], _q1e3
C.add([k('1', 'e', 'iii')], 'chem-4-1', 'hardness-in-ppm-of-calcium-carbonate', [
    lift('r-1', '184', 3, 'For (iii). The scheme adds: ' + _q1e3[0].asides[0])],
    qtext=Q1E, stem=Q1_FULL, figure=Q1EQ)
# REPEAT (3): the three results printed on three lines (scheme page 5, y 602-644),
# priced together as one point.
_rep = display(_q1e3[1].text)
assert _rep == '4.8 × 10⁻⁴ / 0.00048 M 4.8 × 10⁻² / 0.048 48', _rep
_rep3 = ['4.8 × 10⁻⁴ / 0.00048 M', '4.8 × 10⁻² / 0.048', '48']
assert ' '.join(_rep3) == _rep
C.add([k('1', 'e', 'iii')], 'chem-4-1', 'hardness-after-ion-exchange', [
    lift('r-1', '; '.join(_rep3), 3, 'REPEAT: the scheme prints the three results on three lines, moles per litre, '
         'grams per litre and ppm, and prices them together (3). It adds: ' + _q1e3[1].asides[0])],
    qtext=Q1E_REPEAT, stem=Q1_FULL + ' ' + Q1E, figure=Q1EQ, cid='q1-e-repeat',
    ref_suffix='after (iii), the water after ion-exchange')
C.fixed([k('1', 'f')], 'chem-4-3', 'whether-a-deioniser-needs-regenerating', stem=Q1_STEM)

# ── Q2 Preparing soap ────────────────────────────────────────────────────────
# The equation (paper page 3, x 72-404, y 111-197) sets its structures and names
# as a picture ('paper-q2-eq'), and the apparatus on the right with its label
# "NaOH, ethanol, fat" is 'paper-q2'; both are kept out of the text.
Q2EQ, Q2APP = FIG + 'paper-q2-eq', FIG + 'paper-q2'
Q2_STEM = C.context(k('2', 'a'))
assert Q2_STEM.endswith('The balanced equation for the reaction is as follows:'), Q2_STEM
# (The cards whose figure is the apparatus, or the scheme's drawing, end the stem before
# the equation.)
Q2_LEAD = cut(Q2_STEM, 'The balanced equation')[0]
C.fixed([k('2', 'a')], 'chem-4-2', 'iupac-name-of-glycerol', figure=Q2EQ)
C.fixed([k('2', 'b')], 'chem-4-2', 'reflux-and-saponification-in-making-soap', figure=Q2APP, stem=Q2_LEAD,
        row_notes={0: 'WHY.', 1: 'NAME.', 2: 'WHAT.'})
# (c)(i): DESC (2 × 3) beside the scheme's drawing of the distillation apparatus
# (page 6, x 222-414, y 284-414; a raster, its labels inside it).
_q2c1 = P.items(k('2', 'c', 'i'))
assert [it.cell for it in _q2c1] == ['[2 × 3]'] and _q2c1[0].asides == [
    '[At least one correct label required]', '[No diagram – lose 3 marks]'], _q2c1
# Its stem points at the reflux apparatus "shown on the right", which the scheme's drawing
# (the solution) is not: the paper's own print (the lead-in and equation, the apparatus,
# then (c)(i)) is the question.
C.fixed([k('2', 'c', 'i')], 'chem-u2', 'distilling-off-the-ethanol', figure=S + 'q2c-i', stem=Q2_LEAD,
        row_notes={0: 'DESC. The scheme draws the apparatus below its points, shown with the answer.'})
print_question('paper-q2c-i-print')
C.fixed([k('2', 'c', 'ii')], 'chem-u2', 'isolating-soap-with-brine', figure=Q2APP, stem=Q2_LEAD)
C.fixed([k('2', 'c', 'iii')], 'chem-u2', 'purifying-and-drying-soap', figure=Q2APP, stem=Q2_LEAD,
        row_notes={0: 'PURIFIED.', 1: 'DRIED.'})
# (d): Calculate (12), four steps (3) each in four routes, a box of two columns
# and two rows (scheme page 6, y 592-716); the text layer runs each printed row of
# the box across both columns. Each route's steps are read from those rows, cut at
# their cells, and each step is a menu over the routes. The paper's print (the
# lead-in with its masses and equation, then (d)) is the question.
_d = [raw(6, y0 - 1, y1 + 1, 60, 510) for y0, y1 in ((592, 607), (605, 620), (617, 633), (628, 649), (659, 674),
                                                  (671, 687), (684, 700), (695, 716))]
# (The numerators and denominators the text layer marks as scripts, "^(6.82)/_(8.9)", are
# read as the slash fraction the page prints, "6.82/8.9".)
_d = [[re.sub(r'\^\(?|_\(|\)(?=/| x| =)', '', x).strip() for x in re.split(r'\s*\(3\)\s*', row) if x.strip()]
      for row in _d]
assert all(len(row) == 2 for row in _d), _d
_r1, _r2 = [row[0] for row in _d[:4]], [row[1] for row in _d[:4]]
_r3, _r4 = [row[0] for row in _d[4:]], [row[1] for row in _d[4:]]
assert _r1 == ['8.9 ÷ 890* = 0.01 mol glyceryl tri.', 'x 3 = 0.03 mol soap (th. yield)',
               '0.03 x 306* = 9.18 g soap (th. yield)', '7/9.18 x 100 = 76 – 77 %'] and \
    _r2[3] == '0.0076/0.0077/0.01 = 76 – 77 %' and _r3[3] == '0.023/0.03 x 100 = 76 – 77 %' and \
    _r4 == ['7.0 ÷ 306* = 0.023 mol soap (act. yield)', '0.023 ÷ 3 = 0.0076/0.0077 mol gly. t. reqd.',
            '0.0076/0.0077 x 890* = 6.82 g gly. t. reqd.', '6.82/8.9 x 100 = 76 – 77 %'], (_r1, _r2, _r3, _r4)
_q2d = P.items(k('2', 'd'))
assert _q2d[0].cell == '[12]' and display(_q2d[0].text) == '76 – 77%', _q2d
_slip2 = traced('*Addition must be shown for error to be treated as a slip (apply only once); consequential '
                'marking applies')
_routes = [_r1, _r2, _r3, _r4]
C.add([k('2', 'd')], 'chem-1-4', 'percentage-yield-of-soap', [
    menu_row(f'r-{i + 1}', list(dict.fromkeys(r[i] for r in _routes)), 1, ' '.join(x for x in [
        'The scheme gives the answer, 76 – 77%, priced (12), then four routes in a box, four steps (3) each: the '
        'first step of the route used, (3). Each "a/b" is printed as a fraction.' if i == 0 else
        f'Step {i + 1} of that same route, (3).', ('The scheme adds: "[' + _slip2 + ']"') if i == 3 else ''] if x),
        per=3, total=3) for i in range(4)], total=12, figure=S + 'q2d')
print_question('paper-q2d-print')

# ── Q3 Rate of the thiosulfate-acid reaction ─────────────────────────────────
# The results table (paper page 3, y 516-574) is the paper's crop 'paper-q3-table',
# kept out of the stem.
Q3T = FIG + 'paper-q3-table'
C.fixed([k('3', 'a')], 'chem-3-2', 'the-precipitate-in-the-thiosulfate-reaction', figure=Q3T)
C.fixed([k('3', 'b')], 'chem-u2', 'diluting-a-stock-solution', figure=Q3T)
C.fixed([k('3', 'c')], 'chem-u2', 'keeping-the-acid-constant', figure=Q3T)
# (d): PLOT (2 × 3), (3), (3) and CONCLUSION (6) beside the scheme's graph (page 7,
# x 66-545, y 300-616; its axis numbers and labels read as its picture's). The
# question needs the paper's table: its own print is the question.
_q3d = P.items(k('3', 'd'))
assert [it.cell for it in _q3d] == ['[2 × 3]', '[3]', '[3]', '[6]'] and \
    _q3d[3].asides == ['[Allow 3 marks for “Linear relationship”]'], _q3d
C.fixed([k('3', 'd')], 'chem-3-2', 'plotting-rate-against-concentration', figure=S + 'q3d',
        row_notes={0: 'PLOT. The scheme draws the graph below its points, shown with the answer.', 4: 'CONCLUSION.'})
print_question('paper-q3d-print')
C.fixed([k('3', 'e')], 'chem-3-2', 'reading-a-reaction-time-off-the-graph', figure=S + 'q3d',
        row_notes={0: 'USE. The scheme\'s graph reads the rate at 0.10 M with dashed lines, shown with the answer.'})
C.fixed([k('3', 'f')], 'chem-3-2', 'reaction-time-and-temperature', figure=Q3T,
        row_notes={0: 'WOULD.', 1: 'JUSTIFY.'})

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-2', 'electron-configuration-of-the-oxide-ion', notes=Q4_NOTE)
# (b): STATE, six points priced (2 × 3): any two.
C.menu([k('4', 'b')], 'chem-1-3', 'mendeleevs-table-and-the-modern-table', claim=2, notes=Q4_NOTE,
       note='STATE: the scheme prices two of these points (2 × 3), one each.')
C.fixed([k('4', 'c')], 'chem-2-2', 'shapes-of-molecules-of-formula-qx2', notes=Q4_NOTE)
C.route([k('4', 'd')], 'chem-1-4', 'number-of-iron-atoms-in-a-serving', notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-2-3', 'gay-lussacs-law-of-combining-volumes', notes=Q4_NOTE)
C.fixed([k('4', 'f')], 'chem-3-2', 'activation-energy', notes=Q4_NOTE)
# (g): the cue "DISTING.:" is set in one run with the first point (scheme page 8, x 94).
_q4g = P.items(k('4', 'g'))
assert pts(_q4g[0])[0] == 'DISTING.: Sigma involves end-on overlap of orbitals', _q4g
C.fixed([k('4', 'g')], 'chem-2-1', 'sigma-and-pi-bonds', notes=Q4_NOTE,
        fixes={'DISTING.: Sigma involves end-on overlap of orbitals': 'Sigma involves end-on overlap of orbitals'})
C.fixed([k('4', 'h')], 'chem-2-3', 'an-ideal-gas', notes=Q4_NOTE)
C.fixed([k('4', 'i')], 'chem-4-3', 'secondary-sewage-treatment', notes=Q4_NOTE)
# (j): DRAW (2 × 3), three structures drawn side by side (scheme page 8, x 160-460,
# y 593-650), any two: the scheme's drawing is the answer ('scheme-q4j', its atoms read
# as its picture's).
C.drawn([k('4', 'j')], 'chem-4-2', 'isomers-of-formula-c3h6o2', S + 'q4j', notes=Q4_NOTE)
shown('The scheme draws three structures side by side, "//" between them, and prices any two (2 × 3), one each.')
# (k): the scheme sets A's answer, then "or" and B's under a cue of its own, with no
# letter (page 8, y 665-737): the first item is A's, the second B's.
_q4k = P.items(k('4', 'k'))
assert [(it.cell, display(it.text)) for it in _q4k] == [('[2 × 3]', 'Fe₂O₃ + 3CO → 2Fe + 3CO₂'),
                                                       ('[6]', 'SO₂ + H₂O → H₂SO₃')], _q4k
assert _q4k[0].asides == ['[Formulae 3 marks; balancing 3 marks]'] and \
    raw(8, 688, 706, 90, 110) == 'or', (_q4k, raw(8, 688, 706, 90, 110))
C.add([ka('4', 'k', None, 'A')], 'chem-u3', 'reducing-iron-oxide-in-the-blast-furnace', [
    lift('r-1', _q4k[0].text, 6, 'The scheme prices the equation (2 × 3) and adds: ' + _q4k[0].asides[0])],
    notes=Q4_NOTE)
_q4kb = P.ask(ka('4', 'k', None, 'B'))
assert _q4kb.endswith(' dissolves in water. ____________________________'), _q4kb
C.add([ka('4', 'k', None, 'B')], 'chem-4-3', 'sulfur-dioxide-dissolving-in-water', [
    lift('r-1', _q4k[1].text, 6, 'The scheme adds: ' + display(_q4k[1].asides[0]))],
    notes=Q4_NOTE, qtext=cut(_q4kb, '____')[0])

# ── Q5 Atomic structure: Dalton, the electron, Bohr and orbitals ─────────────
# (a): STATE, three points priced (2 × 4): any two.
C.menu([k('5', 'a')], 'chem-1-2', 'daltons-atomic-theory', claim=2,
       note='STATE: the scheme prices two of these points (2 × 4), one each.')
# (b): NAME (i) // (ii) // (iii) (3 × 3), the paper's romans on lines of their own
# (page 4, y 558-614) completing "Name the scientist".
Q5B = P.ask(k('5', 'b')) + ' (i) ' + P.ask(k('5', 'b', 'i')) + ' (ii) ' + P.ask(k('5', 'b', 'ii')) + ' (iii) ' + \
    P.ask(k('5', 'b', 'iii'))
assert Q5B.endswith('(iii) who, about 1911, measured the charge on the electron, e.'), Q5B
_q5b = [display(it.text) for r in ('i', 'ii', 'iii') for it in P.items(k('5', 'b', r))]
assert _q5b == ['Thomson //', 'Rutherford //', 'Millikan'] and cells(k('5', 'b', 'iii')) == ['[3 × 3]'], _q5b
C.add([k('5', 'b')], 'chem-1-2', 'scientists-who-studied-the-electron', [
    lift('r-1', 'Thomson', 3, 'For (i). The scheme prices these points (3 × 3), one each.'),
    lift('r-2', 'Rutherford', 3, 'For (ii).'),
    lift('r-3', 'Millikan', 3, 'For (iii).')], qtext=Q5B)
# (c): OUTLINE, eight points "ANY FOUR: (6 + 3 × 3)" (scheme page 9, y 199-408).
_q5c = P.items(k('5', 'c'))
assert [it.cell for it in _q5c] == ['[6 + 3 × 3]'] and '[any four]' in _q5c[0].asides, _q5c
_four5 = raw(9, 393, 410, 420)
assert _four5 == 'ANY FOUR: (6 + 3 × 3)', _four5
_bohr = pts(_q5c[0])
assert len(_bohr) == 8 and _bohr[0].startswith('The electron in a hydrogen atom'), _bohr
C.add([k('5', 'c')], 'chem-1-2', 'bohrs-theory-and-the-hydrogen-spectrum', [
    menu_row('r-1', _bohr, 4, 'OUTLINE: any four of these, the first (6) and the others (3) each: "' + _four5 + '". '
             'The scheme adds: ' + ' '.join(a for a in _q5c[0].asides if not a.startswith('[any')),
             per=6, steps=[6, 3, 3, 3], total=15)], total=15, figure=FIG + 'paper-q5c')
# (d): STATE, five points, the cell "(ANY 2 × 3)" set at the end of the last
# (scheme page 9, y 431-546), which the reader does not take for a cell.
_q5d = P.items(k('5', 'd'))
_lim = pts(_q5d[0])
assert [it.cell for it in _q5d] == [None] and len(_lim) == 5 and _lim[4].endswith(' (ANY 2 × 3)'), _q5d
_lim[4] = _lim[4][:-len(' (ANY 2 × 3)')]
C.add([k('5', 'd')], 'chem-1-2', 'limitations-of-bohrs-theory', [
    menu_row('r-1', _lim, 2, 'STATE: any two of these, (3) each: "(ANY 2 × 3)".', per=3, total=6)], total=6)
# (e): DEFINE (2 × 3), two points, or after "or" two others (scheme page 9, y 569-635);
# DRAW (3), the p-orbital drawn three ways (crop 'scheme-q5e'); STATE (3).
_q5e = P.items(k('5', 'e'))
_orb = pts(_q5e[0])
assert [it.cell for it in _q5e] == ['[2 × 3]', '[3]', '[3]'] and len(_orb) == 4 and \
    _orb[2] == 'space occupied by electron' and raw(9, 606, 623, 280, 320) == 'or', (_q5e, _orb)
assert display(_q5e[1].text) == 'Dumbbell drawn' and display(_q5e[2].text) == 'two / 2', _q5e
C.add([k('5', 'e')], 'chem-1-2', 'atomic-orbitals-and-the-p-orbital', [
    menu_row('r-1', [_orb[0], _orb[2]], 1, 'DEFINE: one of these, (3): the first wording\'s first point, or, after "or", '
             'the second\'s; the scheme prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_orb[1], _orb[3]], 1, 'And the second point of that same wording, (3).', per=3, total=3),
    lift('r-3', 'Dumbbell drawn', 3, 'DRAW. The scheme draws the dumbbell three ways, alone and on axes, shown with the '
         'answer.'),
    lift('r-4', 'two / 2', 3, 'STATE.')], total=12, figure=S + 'q5e')

# ── Q6 Hydrocarbons, octane numbers and heats of reaction ────────────────────
# Compounds X, Y and Z are drawn in a column right of (a)-(c) (paper page 5, x 433-544,
# y 48-192), the paper's crop 'paper-q6'.
Q6 = FIG + 'paper-q6'
# (a): GIVE "X: Heptane // Y: Cyclohexane // Z: Methylbenzene" priced [(2 × 3) + 2].
_q6a = P.items(k('6', 'a'))
_xyz = pts(_q6a[0])
assert [it.cell for it in _q6a] == ['[(2 × 3) + 2]'] and _xyz == ['X: Heptane', 'Y: Cyclohexane', 'Z: Methylbenzene'], \
    _q6a
C.add([k('6', 'a')], 'chem-2-4', 'naming-heptane-cyclohexane-and-methylbenzene', [
    lift('r-1', _xyz[0], None, 'GIVE. The scheme prices these points [(2 × 3) + 2].'),
    lift('r-2', _xyz[1], None),
    lift('r-3', _xyz[2], None)], kind='orderedSplit', notation='[(2 × 3) + 2]', total=8,
    notes=SPLIT.format('[(2 × 3) + 2]'), figure=Q6)
C.fixed([k('6', 'b')], 'chem-2-4', 'the-fraction-x-and-z-come-from', figure=Q6, row_notes={0: 'NAME.', 1: 'WHAT.'})
C.fixed([k('6', 'c')], 'chem-2-4', 'auto-ignition-and-the-octane-scale', figure=Q6, row_notes={0: 'WHAT.', 1: 'NAME.'})
# (d): DEFINE (2 × 3); OUTLINE, six points "(ANY THREE: 3 × 3)", the cell set at the end
# of the last (scheme page 10, y 289-452), which the reader does not take for a cell.
_q6d = P.items(k('6', 'd'))
_hc = pts(_q6d[0])
_bomb = pts(_q6d[1])
assert [it.cell for it in _q6d] == ['[2 × 3]', None] and len(_hc) == 2 and len(_bomb) == 6 and \
    _bomb[0].startswith('Place known amount (mass) of substance') and \
    _bomb[5].endswith(' (ANY THREE: 3 × 3)'), _q6d
_bomb[5] = _bomb[5][:-len(' (ANY THREE: 3 × 3)')]
C.add([k('6', 'd')], 'chem-3-1', 'heat-of-combustion-by-bomb-calorimeter', [
    lift('r-1', _hc[0], 3, 'DEFINE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _hc[1], 3),
    menu_row('r-3', _bomb, 3, 'OUTLINE: any three of these, (3) each: "(ANY THREE: 3 × 3)".', per=3, total=9)],
    total=15, figure=Q6)
# (e): CALC (9): three equations (3) each in a box; or, after "or", the sums of heats
# of formation, three terms (3) each, two ways (scheme page 10, y 471-667): each
# step a menu over the routes. STATE (3). The question needs the paper's equation,
# its state symbols set as subscripts the text layer scatters: its own print is the
# question.
_q6e = P.items(k('6', 'e'))
_e = [display(it.text) for it in _q6e]
assert [it.cell for it in _q6e] == ['[3]', '[9]'] + ['[3]'] * 6 and _e[0] == 'CALC.: 236.6 kJ mol⁻¹ {– 236.6 gets' \
    and _e[1] == 'only}', _q6e
assert _e[2:5] == ['C₇H₁₆ → 7C + 8H₂ ∆H = 224.2 kJ mol⁻¹', '7C + 4H₂ → C₇H₈ ∆H = 12.4 kJ mol⁻¹',
                   'C₇H₁₆ → C₇H₈ + 4H₂ ∆H = 236.6 kJ mol⁻¹'], _e
assert _e[5] == 'ΣΔHf(products) – ΣΔHf(reactants) = ΔH(reaction) 12.4 (3) – (– 224.2) (3) = 236.6' and \
    _e[6] == 'OR 12.4 (3) + 224.2 (3) = 236.6', _e
_only = traced('{– 236.6 gets (3) only}')
_sums = traced('ΣΔHf(products) – ΣΔHf(reactants) = ΔH(reaction)')
C.add([k('6', 'e')], 'chem-3-1', 'heat-of-reforming-heptane', [
    menu_row('r-1', [_e[2], '12.4'], 1, 'CALC: the scheme gives the answer, "236.6 kJ mol⁻¹ ' + _only + '", priced (9), '
             'then three equations (3) each in a box; or, after "or", from "' + _sums + '": "12.4 (3) – (– 224.2) (3) '
             '= 236.6 (3)", or "12.4 (3) + 224.2 (3) = 236.6 (3)". The first step of the route used, (3); its own print '
             'is shown with the answer.', per=3, total=3),
    menu_row('r-2', [_e[3], '– (– 224.2)', '+ 224.2'], 1, 'The second step of that same route, (3).', per=3, total=3),
    menu_row('r-3', [_e[4], '= 236.6'], 1, 'And the third, (3).', per=3, total=3),
    lift('r-4', _e[7], 3, 'STATE.')], total=12, figure=S + 'q6e')
print_question('paper-q6e-print')

# ── Q7 The phosphorus(V) chloride equilibrium ────────────────────────────────
# The equation (paper page 5, y 377-391) sets its equilibrium arrows as a drawn glyph
# the text layer does not carry: it is the paper's crop 'paper-q7-eq', kept out of
# the text.
Q7EQ = FIG + 'paper-q7-eq'
# (a): EXPLAIN Rev. // Equ. // Why, priced [(2 × 4) + 3]. The paper underlines
# "reversible reaction" and "equilibrium" (page 5, y 397): its own print is the question.
_q7a = P.items(k('7', 'a'))
_rev = pts(_q7a[0])
assert [it.cell for it in _q7a] == ['[(2 × 4) + 3]'] and len(_rev) == 3 and _rev[0].startswith('Rev.: Products') and \
    _rev[1].startswith('Equ.: A steady state') and _rev[2].startswith('Reactants producing products'), _q7a
# (The labels "Rev.:", "Equ.:" and "Why:" stand in a column of their own, scheme page 11, x 150.)
assert raw(11, 70, 170, 145, 180) == 'Rev.: Equ.: Why:', raw(11, 70, 170, 145, 180)
C.add([k('7', 'a')], 'chem-3-3', 'reversible-reactions-and-dynamic-equilibrium', [
    lift('r-1', _rev[0][len('Rev.: '):], None, 'Rev. The scheme prices these points [(2 × 4) + 3].'),
    lift('r-2', _rev[1][len('Equ.: '):], None, 'Equ.'),
    lift('r-3', _rev[2], None, 'Why.')], kind='orderedSplit', notation='[(2 × 4) + 3]', total=11,
    notes=SPLIT.format('[(2 × 4) + 3]'))
print_question('paper-q7a-print')
# (b): STATE (2 × 3); WRITE (6), the expression set as a fraction (scheme page 11,
# y 370-410), its denominator read as an aside.
_q7b = P.items(k('7', 'b'))
assert [it.cell for it in _q7b] == ['[2 × 3]', '[6]'] and display(_q7b[1].text) == '[PCl₃] . [Cl₂]' and \
    [display(a) for a in _q7b[1].asides] == ['[PCl₅]', '[Square brackets required]'], _q7b
_lc = pts(_q7b[0])
C.add([k('7', 'b')], 'chem-3-3', 'le-chateliers-principle-and-kc-for-pcl5', [
    lift('r-1', _lc[0], 3, 'STATE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _lc[1], 3),
    lift('r-3', '[PCl₃] . [Cl₂] ÷ [PCl₅]', 6, 'WRITE. ' + FRACTION.format('[PCl₃] . [Cl₂]', '[PCl₅]')
         + ' It adds: [Square brackets required]')], figure=Q7EQ)
# (c): CALCULATE (12): a table in a box, four steps (3) each (scheme page 11, y 333-
# 572), the second step's row printed three ways, each closed by "/". The question
# needs the paper's equation: its own print is the question.
_q7c = P.items(k('7', 'c'))
_c = [display(it.text) for it in _q7c]
assert [it.cell for it in _q7c] == ['[12]', '[3]', '[3]', '[3]', '[3]', None] and _c[0] == '0.0225 mol l⁻¹', _q7c
assert _c[1] == 'Conversion to moles: 208.5/208.5* = 1 53.25/71* = 0.75 PCl₅ PCl₃ Cl₂ Initially 1* mole 0 moles 0 moles' \
    and _c[2] == 'Next step 1 – x x x / 0.25 moles 0.75 moles 0.75* moles / 0.01* mol 0 moles 0 moles' and \
    _c[3] == 'At Equil. 0.0025 moles / l 0.0075 moles / l 0.0075* moles / l' and \
    _c[4] == '[0.0075] . [0.0075] = 0.0225', _c
_conv = traced('Conversion to moles: 208.5/208.5* = 1 53.25/71* = 0.75')
_star7 = traced('*Addition must be shown for error to be treated as a slip (apply only once); consequential marking '
                'applies.')
C.add([k('7', 'c')], 'chem-3-3', 'kc-for-the-pcl5-equilibrium', [
    lift('r-1', 'Initially 1* mole 0 moles 0 moles', 3, 'The scheme gives the answer, "0.0225 mol l⁻¹", priced (12), then '
         'works it as a table under PCl₅, PCl₃ and Cl₂, four steps (3) each, after "' + _conv + '"; its own print is '
         'shown with the answer.'),
    menu_row('r-2', ['Next step 1 – x x x', '0.25 moles 0.75 moles 0.75* moles', '0.01* mol 0 moles 0 moles'], 1,
             'One of these rows of the table, (3): the scheme prints the next step three ways, each closed by "/".',
             per=3, total=3),
    lift('r-3', _c[3], 3),
    lift('r-4', '[0.0075] . [0.0075] ÷ [0.0025] = 0.0225', 3, FRACTION.format('[0.0075] . [0.0075]', '[0.0025]')
         + ' It adds: "' + _star7 + '"')], total=12, figure=S + 'q7c')
print_question('paper-q7c-print')
C.fixed([k('7', 'd')], 'chem-3-3', 'is-pcl5-decomposition-endothermic', figure=Q7EQ, row_notes={0: 'IS.', 1: 'JUSTIFY.'})
C.fixed([k('7', 'e')], 'chem-3-3', 'pressure-and-the-value-of-kc', figure=Q7EQ, row_notes={0: 'WHAT.', 1: 'EXPLAIN.'})

# ── Q8 Acids, bases and methyl orange ────────────────────────────────────────
# (a) prints (8) after its definitions, then the methyl orange lead-in (its
# equilibrium arrows drawn: the paper's crop 'paper-q8a-eq'), then (6) and (3) after
# two more asks (page 5, y 577-680): a card each. The scheme sets DEFINE (i) and
# (ii) (2 × 4), DISTINGUISH (2 × 3) and WHAT (3) under its romans (page 12, y 77-213).
Q8EQ = FIG + 'paper-q8a-eq'
Q8A_DEF, _r = cut(P.ask(k('8', 'a')), 'In acting as')
Q8_HX, _r = cut(_r, 'Distinguish between')
Q8A_DIST, Q8A_WHAT = cut(_r, 'What is the conjugate')
assert Q8A_DEF == 'Define (i) acid, (ii) conjugate acid, according to the Brønsted-Lowry theory.' and \
    Q8_HX.endswith('the dissociated form (X⁻) is yellow.') and Q8A_WHAT == 'What is the conjugate base of HX?', \
    (Q8A_DEF, Q8_HX, Q8A_WHAT)
_q8a1, _q8a2 = P.items(k('8', 'a', 'i')), P.items(k('8', 'a', 'ii'))
assert [(it.cell, display(it.text)) for it in _q8a1] == [(None, 'Proton (H⁺) donor //')] and \
    [it.cell for it in _q8a2] == ['[2 × 4]', '[2 × 3]', '[3]', None], (_q8a1, _q8a2)
C.add([k('8', 'a')], 'chem-3-4', 'bronsted-lowry-acid-and-conjugate-acid', [
    lift('r-1', 'Proton (H⁺) donor', 4, 'For (i). The scheme prices these points (2 × 4), one each.'),
    lift('r-2', _q8a2[0].text, 4, 'For (ii).')], qtext=Q8A_DEF, stem='', cid='q8-a-define',
    ref_suffix='acid and conjugate acid defined')
_sw = pts(_q8a2[1])
_sa = display(_q8a2[3].text)
assert len(_sw) == 2 and _sa.startswith('[“SA diss fully” and “WA diss. slightly” (3)'), (_sw, _sa)
C.add([k('8', 'a')], 'chem-3-4', 'strong-and-weak-acids', [
    lift('r-1', _sw[0], 3, 'DISTINGUISH. The scheme prices these points (2 × 3), one each, and adds: ' + traced(_sa)),
    lift('r-2', _sw[1], 3)], qtext=Q8A_DIST, stem=Q8_HX, figure=Q8EQ, cid='q8-a-distinguish',
    ref_suffix='strong and weak acid')
C.add([k('8', 'a')], 'chem-3-4', 'conjugate-base-of-methyl-orange', [
    lift('r-1', _q8a2[2].text, 3, 'WHAT.')], qtext=Q8A_WHAT, stem=Q8_HX, figure=Q8EQ, cid='q8-a-conjugate-base',
    ref_suffix='conjugate base of HX')
# (b): STATE // EXPL. (2 × 3) for (i) and again for (ii), the paper setting both inside
# one sentence (page 5, y 684-709): a card each.
Q8B = P.ask(k('8', 'b')) + ' (i) ' + P.ask(k('8', 'b', 'i')) + ' (ii) ' + P.ask(k('8', 'b', 'ii'))
assert Q8B.endswith('is added to (i) a 0.1 M solution of HCl, (ii) a 0.1 M solution of NaOH.'), Q8B
for _r8, _concept in (('i', 'methyl-orange-in-acid'), ('ii', 'methyl-orange-in-alkali')):
    _it = P.items(k('8', 'b', _r8))
    _se = pts(_it[0])
    assert [it.cell for it in _it] == ['[2 × 3]'] and len(_se) == 2 and _se[1].startswith('EXPL.: Equilibrium shifted'), _it
    C.add([k('8', 'b', _r8)], 'chem-3-4', _concept, [
        lift('r-1', _se[0], 3, f'For ({_r8}). STATE. The scheme prices these points (2 × 3), one each.'),
        lift('r-2', _se[1][len('EXPL.: '):], 3, 'EXPL.')], qtext=Q8B, stem=Q8_HX, figure=Q8EQ)
# (c): the paper prints (9) after the two calculations, set inside one sentence, and
# (12) after the pH curve and its explanation (page 5, y 716-784). CALC (i) "13 [ – log
# 0.1 = 1 (2) 14 – 1 = 13 (1)] (3)"; (ii) (6), two steps (3) each in two routes in a
# box; DRAW (3 × 3) beside the scheme's curve (page 12, y 461-745, its axis labels read
# as its picture's) and EXPLAIN (3): a card each.
Q8C_CALC, Q8C_DRAW = cut(P.ask(k('8', 'c')), 'Draw a clearly')
assert Q8C_CALC.endswith('if methyl orange has a Ka value of 3.5 × 10⁻⁴.') and Q8C_DRAW.endswith(
    'can be used in this titration.'), (Q8C_CALC, Q8C_DRAW)
_c1 = P.items(k('8', 'c', 'i'))
assert [(it.cell, display(it.text)) for it in _c1] == [('[3]', '13 [ – log 0.1 = 1 (2) 14 – 1 = 13 (1)]')], _c1
C.add([k('8', 'c', 'i')], 'chem-3-4', 'ph-of-0-1-m-sodium-hydroxide', [
    lift('r-1', '– log 0.1 = 1', 2, 'For (i). The scheme gives the answer, 13, priced (3), and in brackets the two '
         'steps that earn it, (2) and (1).'),
    lift('r-2', '14 – 1 = 13', 1)], qtext=Q8C_CALC, stem='')
_c2 = P.items(k('8', 'c', 'ii'))
assert [it.cell for it in _c2] == ['[6]', '[3]', '[3]', '[3]', '[3]', '[3 × 3]', '[3]'] and \
    display(_c2[0].text) == '2.9', _c2
_s1 = [x.strip() for x in display(_c2[1].text).split(' / ')] + [x.strip() for x in display(_c2[3].text).split(' / ')]
assert len(_s1) == 5 and _s1[3] == 'pH = – log √(Ka x M)', _s1
C.add([k('8', 'c', 'ii')], 'chem-3-4', 'ph-of-a-methyl-orange-solution', [
    menu_row('r-1', _s1, 1, 'For (ii). The scheme gives the answer, 2.9, priced (6), then two routes in a box, two '
             'steps (3) each, the second after "OR": the first step of the route used, (3); its own print is shown '
             'with the answer.', per=3, total=3),
    menu_row('r-2', [display(_c2[2].text), display(_c2[4].text)], 1, 'And the pH by that same route, (3).', per=3,
             total=3)], total=6, qtext=Q8C_CALC, stem='', figure=S + 'q8c-ii')
_curve = pts(_c2[5])
assert len(_curve) == 3 and _curve[0].startswith('DRAW.: Axes labelled'), _curve
_paper8 = traced(raw(12, 494, 537, 430))
assert _paper8 == 'Curve does not have to be drawn on graph paper.', _paper8
C.add([k('8', 'c')], 'chem-3-4', 'ph-curve-for-a-strong-acid-and-strong-base', [
    lift('r-1', _curve[0][len('DRAW.: '):], 3, 'DRAW. The scheme prices these points (3 × 3), one each, and draws the '
         'curve, shown with the answer, beside "' + _paper8 + '"'),
    lift('r-2', _curve[1], 3),
    lift('r-3', _curve[2], 3),
    lift('r-4', _c2[6].text, 3, 'EXPLAIN.')], qtext=Q8C_DRAW, stem='', figure=S + 'q8c-curve', cid='q8-c-curve',
    ref_suffix='the pH curve')

# ── Q9 A reaction scheme from ethanol to PVC ─────────────────────────────────
# The reaction scheme (paper page 6, x 177-435, y 60-168) is the paper's crop
# 'paper-q9', its compounds and letters kept out of the text. The parts whose answer
# is the scheme's drawing take the paper's print of the reaction scheme and the
# part as their question.
Q9 = FIG + 'paper-q9'
Q9_STEM = C.context(k('9', 'a'))
assert Q9_STEM == 'Study the reaction scheme and answer the questions that follow.', Q9_STEM
C.fixed([k('9', 'a')], 'chem-2-2', 'the-molecule-with-no-tetrahedral-carbon', figure=Q9)
# (b): IDENTIFY "(i): Y / V [Accept W] // (ii): Z" (2 × 3), the paper setting (i) and
# (ii) inside its ask (page 6, y 199).
_b1, _b2 = P.items(k('9', 'b', 'i')), P.items(k('9', 'b', 'ii'))
assert [(it.cell, display(it.text)) for it in _b1] == [(None, 'Y / V [Accept W] //')] and \
    [(it.cell, display(it.text)) for it in _b2] == [('[2 × 3]', 'Z')], (_b1, _b2)
C.add([k('9', 'b')], 'chem-4-2', 'addition-and-substitution-in-the-scheme', [
    lift('r-1', 'Y / V', 3, 'For (i). The scheme prices these points (2 × 3), one each, and adds: [Accept W]'),
    lift('r-2', 'Z', 3, 'For (ii).')], figure=Q9)
# (c): DESCRIBE, four points (4 × 3); the third draws the carbonium ion after it
# (scheme page 13, x 150-300, y 229-296: crop 'scheme-q9c', its atoms read as its
# picture's). The text layer sets the second point's charge "Clδ–)" as "Clδ)–".
_q9c = P.items(k('9', 'c'))
_mech = pts(_q9c[0])
assert [it.cell for it in _q9c] == ['[4 × 3]', None] and len(_mech) == 4 and \
    _mech[2] == 'Forming a localised carbonium* ion (carbocation*) / *Accept positive carbon (C⁺)', _mech
_mech[1] = P.rearranged(_mech[1], 'Clδ)–', 'Clδ–)')
_carb, _acc9 = cut(_mech[2], '/ *Accept')
_acc9 = _acc9[len('/ '):]
_curly = display(_q9c[1].text)
assert _curly == '[Note : Where appropriate, allow correct use of ‘curly’ arrows.]', _curly
C.add([k('9', 'c')], 'chem-4-2', 'mechanism-of-adding-hcl-to-ethene', [
    lift('r-1', _mech[0], 3, 'DESCRIBE. The scheme prices these points (4 × 3), one each.'),
    lift('r-2', _mech[1], 3),
    lift('r-3', _carb, 3, 'The scheme adds "' + traced(_acc9) + '" and draws the carbonium ion beside this point, shown '
         'with the answer.'),
    lift('r-4', _mech[3], 3, 'The scheme adds: ' + _curly)], figure=S + 'q9c')
print_question('paper-q9c-print')
# (d): the paper sets (i) and (ii) on a line of their own (page 6, y 243) completing
# one sentence; the scheme prices (i) (6), with a note on a condition alone (3), and
# (ii) (2 × 3): a card each.
Q9D = P.ask(k('9', 'd')) + ' (i) ' + P.ask(k('9', 'd', 'i')) + ' (ii) ' + P.ask(k('9', 'd', 'ii'))
assert Q9D == 'State the reagent(s) and condition(s) required to bring about (i) conversion V, (ii) conversion Z.', Q9D
_d1 = P.items(k('9', 'd', 'i'))
assert [it.cell for it in _d1] == ['[6]', '[3]', None] and display(_d1[0].text).startswith('H₂ Accept H₂'), _d1
# (The page prints the temperature "140" with a raised "o", which the text layer reads as a
# script and the .md as "140o"; the note shows it as the degree sign it is.)
_acc_h2 = traced(display(_d1[0].text)[len('H₂ '):])
_cond = display(_d1[1].text) + ' (3) ' + display(_d1[2].text)
assert '140^o' in _cond and traced(_cond.replace('140^o', '140o')), _cond
_cond = _cond.replace('140^o', '140°')
C.add([k('9', 'd', 'i')], 'chem-4-2', 'reagent-for-hydrogenating-ethene', [
    lift('r-1', 'H₂', 6, 'For (i). The scheme adds: "' + _acc_h2 + '" and "' + _cond + '"')], qtext=Q9D, stem=Q9_STEM,
    figure=Q9)
_d2 = P.items(k('9', 'd', 'ii'))
assert [(it.cell, pts(it)) for it in _d2] == [('[2 × 3]', ['Cl₂', 'hf (hν) / ultraviolet (uv) light / sunlight / heat'])], \
    _d2
C.add([k('9', 'd', 'ii')], 'chem-4-2', 'chlorinating-ethane', [
    lift('r-1', 'Cl₂', 3, 'For (ii). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', pts(_d2[0])[1], 3)], qtext=Q9D, stem=Q9_STEM, figure=Q9)
# (e): DRAW, three points (3 × 3) above the scheme's drawing (page 13, x 185-456,
# y 488-607: crop 'scheme-q9e', its labels read as its picture's).
C.fixed([k('9', 'e')], 'chem-4-2', 'dehydrating-ethanol-over-aluminium-oxide', figure=S + 'q9e',
        row_notes={0: 'DRAW. The scheme draws the apparatus, shown with the answer.'})
print_question('paper-q9e-print')
# (f): the scheme draws the two intermediates (page 13, x 150-470, y 644-718: crop
# 'scheme-q9f') priced (2 × 3), and allows their condensed formulas.
_q9f = P.items(k('9', 'f'))
assert [(it.cell, it.text.strip(), it.asides) for it in _q9f] == [('[2 × 3]', '', ['[Allow CH₂ClCH₂Cl and CH₂=CHCl]'])], \
    _q9f
C.add([k('9', 'f')], 'chem-4-2', 'intermediates-from-ethene-to-pvc', [
    lift('r-1', 'CH₂ClCH₂Cl', 3, 'The scheme draws the two structures, shown with the answer, prices them (2 × 3), one '
         'each, and adds: ' + _q9f[0].asides[0]),
    lift('r-2', 'CH₂=CHCl', 3)], figure=S + 'q9f')
print_question('paper-q9f-print')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the paper prints (6), (6), (9) and (4) after four asks (page 6, y 353-456): a card
# each. The compounds of the third are listed "(i) hydrogen chloride, HCl, (ii) water,
# H₂O, (iii) ammonia, NH₃." inside its sentence (y 416); the paper reader takes the
# list's markers for parts, and the sentence is read back from them.
Q10A_DEF, Q10A_FAC = cut(P.ask(k('10', 'a')), 'State two factors')
_hb = P.lead(k('10', 'a')) + ' (i) ' + P.ask(k('10', 'a', 'i')) + ' (ii) ' + P.ask(k('10', 'a', 'ii'))
Q10A_HB, Q10A_SUG = cut(_hb, 'Suggest a reason')
assert Q10A_DEF == 'Define electronegativity.' and Q10A_HB == ('State which of the following compounds contain '
                                                              'intermolecular hydrogen bonds: (i) hydrogen chloride, HCl, (ii) water, H₂O, (iii) ammonia, '
                                                              'NH₃. Justify your answer.'), (Q10A_DEF, Q10A_HB)
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == ['[2 × 3]', '[2 × 3]', '[2 × 3]', '[3]', '[4]'] and \
    pts(_q10a[2]) == ['H₂O', 'NH₃'], _q10a
_en = pts(_q10a[0])
C.add([k('10', 'a')], 'chem-1-3', 'electronegativity', [
    lift('r-1', _en[0], 3, 'DEFINE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _en[1], 3)], qtext=Q10A_DEF, stem='', cid='q10-a-define', ref_suffix='electronegativity defined')
_fac = pts(_q10a[1])
C.add([k('10', 'a')], 'chem-1-3', 'why-electronegativity-rises-across-a-period', [
    lift('r-1', _fac[0], 3, 'STATE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _fac[1], 3)], qtext=Q10A_FAC, stem='', cid='q10-a-factors', ref_suffix='factors across a period')
_just, _just_a = display(_q10a[3].text), _q10a[3].asides
assert _just == 'Hydrogen bonded to small highly electronegative element (bonded to O, N, F)' and \
    _just_a == ['[If either one of “small / highly” omitted (– 1)]'], (_just, _just_a)
C.add([k('10', 'a')], 'chem-2-2', 'which-hydrides-hydrogen-bond', [
    lift('r-1', 'H₂O', 3, 'STATE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'NH₃', 3),
    lift('r-3', _just, 3, 'JUSTIFY. The scheme adds: ' + _just_a[0])], qtext=Q10A_HB, stem='', cid='q10-a-hydrogen-bonds',
    ref_suffix='intermolecular hydrogen bonds')
# (The scheme breaks "electronegativity" across two lines with a hyphen, "electroneg-" /
# "ativity" (page 14, y 248-276): read as the one word it prints.)
_sug = display(_q10a[4].text)
assert _sug.count('electroneg- ativity') == 1, _sug
C.add([k('10', 'a')], 'chem-2-2', 'boiling-points-of-ammonia-and-water', [
    lift('r-1', _sug.replace('electroneg- ativity', 'electronegativity'), 4, 'SUGGEST.')], qtext=Q10A_SUG, stem='', cid='q10-a-boiling-points',
    ref_suffix='the boiling point of ammonia')
# (b)(i): DESC., four points priced [6 + (2 × 3)] (scheme page 14, y 318-397): any three,
# the first (6).
_b1 = P.items(k('10', 'b', 'i'))
_mp = pts(_b1[0])
assert [it.cell for it in _b1] == ['[6 + (2 × 3)]', None] and len(_mp) == 4 and _mp[0].startswith('DESC.: Sample') and \
    display(_b1[1].text) == '[No diagram deduct 3 marks] *Or other suitable liquid (not water)', _b1
_mp[0] = _mp[0][len('DESC.: '):]
C.add([k('10', 'b', 'i')], 'chem-u2', 'measuring-a-melting-point', [
    menu_row('r-1', _mp, 3, 'DESC.: the scheme prices three of these points [6 + (2 × 3)], the first (6) and the others '
             '(3) each. It adds: ' + traced(display(_b1[1].text)), per=6, steps=[6, 3, 3], total=12)], total=12)
C.menu([k('10', 'b', 'ii')], 'chem-u2', 'melting-point-and-purity', claim=2,
       note='GIVE: the scheme prices two of these points (2 × 3), one each.')
C.fixed([k('10', 'b', 'iii')], 'chem-4-2', 'infrared-spectroscopy')
C.fixed([k('10', 'b', 'iv')], 'chem-4-2', 'uses-of-benzoic-acid')
# (c)(i): DEDUCE "+6 / 6 / VI // +3 / 3 / III" priced (4 + 3), on one row (scheme page 14,
# y 530).
_c1 = P.items(k('10', 'c', 'i'))
assert [(it.cell, pts(it)) for it in _c1] == [('[4 + 3]', ['+6 / 6 / VI', '+3 / 3 / III'])], _c1
C.add([k('10', 'c', 'i')], 'chem-3-5', 'oxidation-numbers-of-chromium', [
    lift('r-1', '+6 / 6 / VI', None, 'DEDUCE. The scheme prices its two points (4 + 3).'),
    lift('r-2', '+3 / 3 / III', None)], kind='orderedSplit', notation='[4 + 3]', total=7,
    notes=SPLIT.format('[4 + 3]'))
C.fixed([k('10', 'c', 'ii')], 'chem-4-2', 'colour-change-of-dichromate')
_c3 = P.items(k('10', 'c', 'iii'))
assert pts(_c3[0])[0] == 'DESC.: Heat (warm) with', _c3
C.fixed([k('10', 'c', 'iii')], 'chem-4-2', 'testing-for-an-aldehyde',
        fixes={'DESC.: Heat (warm) with': 'Heat (warm) with'})
# (iv): GIVE (2 × 3): the name, and the structure the scheme draws (page 14, x 155-300,
# y 680-750: crop 'scheme-q10c-iv'), accepting "CH₃COOH".
_c4 = P.items(k('10', 'c', 'iv'))
assert [(it.cell, pts(it), it.asides) for it in _c4] == [('[2 × 3]', ['Ethanoic acid / acetic acid',
                                                                     '[Accept ‘ethyl ethanoate / ethyl acetate.’]'],
                                                         ['[Accept CH₃COOH]'])], _c4
C.add([k('10', 'c', 'iv')], 'chem-4-2', 'ethanoic-acid-from-ethanol', [
    lift('r-1', 'Ethanoic acid / acetic acid', 3, 'GIVE. The scheme prices these points (2 × 3), one each, and adds: '
         '[Accept ‘ethyl ethanoate / ethyl acetate.’]'),
    lift('r-2', 'CH₃COOH', 3, 'The scheme draws the structure of ethanoic acid, shown with the answer, and adds: '
         '[Accept CH₃COOH]')], figure=S + 'q10c-iv')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the electrolysis cell (paper page 7, x 449-560, y 54-233), its electrodes
# labelled A and B, is the paper's crop 'paper-q11a'.
Q11A = FIG + 'paper-q11a'
C.fixed([k('11', 'a', 'i')], 'chem-3-5', 'inert-electrodes-for-electrolysing-sodium-sulfate', figure=Q11A)
C.fixed([k('11', 'a', 'ii')], 'chem-3-5', 'how-an-electrolyte-conducts', figure=Q11A)
C.fixed([k('11', 'a', 'iii')], 'chem-3-5', 'oxidation-at-the-anode-in-sodium-sulfate', figure=Q11A,
        row_notes={0: 'WHICH.', 1: 'WRITE.'})
C.fixed([k('11', 'a', 'iv')], 'chem-3-5', 'volumes-of-gas-at-the-electrodes', figure=Q11A)
C.fixed([k('11', 'a', 'v')], 'chem-3-5', 'where-the-indicator-turns-blue', figure=Q11A,
        row_notes={0: 'WHICH.', 1: 'JUSTIFY.'})
# (b): the paper prints (10), (6), (3), (3) and (3) after five runs of asks (page 7,
# y 235-410). DEFINE (i) and (ii) are set inside one sentence and priced a cell each
# (scheme page 15, y 292-487): (i) two points (3 + 2), or after "or" two others; (ii)
# two points (3 + 2), or after "or" one (5), or after "or" the formula (3) and the
# meaning of λ (2). Then DETERMINE (2 × 3), STATE (3), EXPLAIN (3), EXPLAIN (3): a card
# each. The nuclear equation (page 7, y 311-329) stacks its mass and atomic numbers:
# the paper's crop 'paper-q11b-eq', kept out of the text.
Q11B = P.ask(k('11', 'b'))
Q11B_DEF, _r = cut(Q11B, 'Americium–241 is')
Q11B_AM, _r = cut(_r, 'Determine the value')
Q11B_DET, _r = cut(_r, 'Alpha particles are')
Q11B_RISK, _r = cut(_r, 'Explain why the occupants')
Q11B_OCC, Q11B_BAT = cut(_r, 'Householders are')
assert Q11B_DEF == 'Define (i) radioactivity, (ii) the half-life of a radioactive isotope.' and \
    Q11B_DET.endswith('for the alpha decay of an americium–241 nucleus.') and \
    Q11B_BAT.endswith('needs to be replaced regularly also.'), Q11B
assert [raw(15, y0, y1, 160, 190) for y0, y1 in ((317, 334), (411, 428), (436, 453))] == ['or'] * 3
_d1, _d2 = P.items(k('11', 'b')), P.items(k('11', 'b', 'ii'))
assert [it.cell for it in _d1] == ['[3 + 2]', '[3 + 2]'] and pts(_d1[0])[0].startswith('DEFINE (i): Spontaneous') and \
    [it.cell for it in _d2] == ['[3 + 2]', '[5]', '[3]', '[2]', '[2 × 3]', '[3]', '[3]', '[3]'], (_d1, _d2)
_ra = [pts(_d1[0])[0][len('DEFINE (i): '):], pts(_d1[0])[1]]
_rb = pts(_d1[1])
C.add([k('11', 'b', 'i')], 'chem-1-2', 'radioactivity', [
    menu_row('r-1', [_ra[0], _rb[0]], 1, 'For (i). One of these: the first wording\'s first point, or, after "or", the '
             'second\'s; the scheme prices the two points of each (3 + 2).'),
    menu_row('r-2', [_ra[1], _rb[1]], 1, 'And the second point of that same wording.')],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), qtext=Q11B_DEF, stem='')
_ha = pts(_d2[0])
assert display(_d2[1].text) == 'time for sample to reach half its activity' and \
    display(_d2[2].text) == 'Half-life formula: t½ = ln2/λ' and display(_d2[3].text) == 'meaning of λ', _d2
C.add([k('11', 'b', 'ii')], 'chem-1-2', 'half-life', [
    menu_row('r-1', [_ha[0], display(_d2[1].text), display(_d2[2].text)], 1, 'For (ii). One of these: the first '
             'wording\'s first point, the scheme pricing its two points (3 + 2); or, after "or", the second wording '
             'whole, priced (5) alone; or, after "or", the formula (3). Claim the second wording here and again below.'),
    menu_row('r-2', [_ha[1], display(_d2[1].text), display(_d2[3].text)], 1, 'And the rest of that same answer: the '
             'first wording\'s second point, or the second wording again, or "meaning of λ" (2) with the formula, for '
             'which the scheme prints the criterion and no wording.')],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), qtext=Q11B_DEF, stem='')
assert pts(_d2[4]) == ['A = 237', 'Z = 93'], _d2[4]
C.add([k('11', 'b')], 'chem-1-2', 'alpha-decay-of-americium-241', [
    lift('r-1', 'A = 237', 3, 'DETERMINE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'Z = 93', 3)], qtext=Q11B_DET, stem=Q11B_AM, figure=FIG + 'paper-q11b-eq', cid='q11-b-determine',
    ref_suffix='the nuclear equation')
C.add([k('11', 'b')], 'chem-1-2', 'a-risk-of-alpha-radiation', [
    lift('r-1', _d2[5].text, 3, 'STATE.')], qtext=Q11B_RISK, stem=Q11B_AM, cid='q11-b-risk',
    ref_suffix='a risk of alpha radiation')
C.add([k('11', 'b')], 'chem-1-2', 'why-smoke-detectors-are-safe', [
    lift('r-1', _d2[6].text, 3, 'EXPLAIN.')], qtext=Q11B_OCC, stem=Q11B_AM, cid='q11-b-occupants',
    ref_suffix='the occupants of the house')
_long = pts(_d2[7])
assert _long == ['Half life is over 400 years (very long)', 'sample does not deplete quickly'], _long
C.add([k('11', 'b')], 'chem-1-2', 'why-americium-241-lasts', [
    menu_row('r-1', _long, 1, 'EXPLAIN: the scheme prices one of these points (3).', per=3, total=3)],
    total=3, qtext=Q11B_BAT, stem=Q11B_AM, cid='q11-b-batteries', ref_suffix='replacing the batteries')
# (c)A: the paper sets (i)-(iii) on lines of their own completing "Explain in terms of
# bonding", printed (18), then two asks unnumbered after (iii), printed (3) and (4)
# (page 7, y 492-640): a card each, the last two cited after (iii). The bucky ball
# (x 407-540, y 429-559) is the paper's crop 'paper-q11c-a'.
Q11CA_LEAD = P.ask(ka('11', 'c', None, 'A'))
Q11CA_III, _r = cut(P.ask(ka('11', 'c', 'iii', 'A')), 'Buckminsterfullerene')
Q11CA_BUCKY, Q11CA_XRAY = cut(_r, 'The spatial arrangement')
Q11CA = (Q11CA_LEAD + ' (i) ' + P.ask(ka('11', 'c', 'i', 'A')) + ' (ii) ' + P.ask(ka('11', 'c', 'ii', 'A')) + ' (iii) '
         + Q11CA_III)
assert Q11CA.startswith('Diamond and graphite are macromolecular') and \
    Q11CA.endswith('(iii) the electrical conductivity of graphite.') and \
    Q11CA_BUCKY.endswith('in these ‘bucky balls’?') and Q11CA_XRAY.endswith('who pioneered this technique?'), \
    (Q11CA, Q11CA_BUCKY, Q11CA_XRAY)
for _rn, _concept in (('i', 'why-diamond-is-hard'), ('ii', 'why-graphite-is-soft'),
                      ('iii', 'why-graphite-conducts')):
    _ai = P.items(ka('11', 'c', _rn, 'A'))
    assert _ai[0].cell == '[2 × 3]' and len(pts(_ai[0])) == 2, _ai
    C.add([ka('11', 'c', _rn, 'A')], 'chem-2-1', _concept, [
        lift('r-1', pts(_ai[0])[0], 3, f'For ({_rn}). The scheme prices these points (2 × 3), one each.'),
        lift('r-2', pts(_ai[0])[1], 3)], qtext=Q11CA, stem='')
_a3 = P.items(ka('11', 'c', 'iii', 'A'))
assert [(it.cell, display(it.text)) for it in _a3][1:] == [('[3]', 'Covalent'), ('[4]', 'Bragg')], _a3
C.add([ka('11', 'c', 'iii', 'A')], 'chem-2-1', 'bonding-in-buckminsterfullerene', [
    lift('r-1', 'Covalent', 3, 'GIVE.')], qtext=Q11CA_BUCKY, stem=cut(Q11CA_LEAD, 'Explain in terms')[0],
    figure=FIG + 'paper-q11c-a', cid='q11-c-a-bucky-balls', ref_suffix='after (iii), the bond in bucky balls')
C.add([ka('11', 'c', 'iii', 'A')], 'chem-2-1', 'x-ray-crystallography-pioneers', [
    lift('r-1', 'Bragg', 4, 'WHAT.')], qtext=Q11CA_XRAY,
    stem=cut(Q11CA_LEAD, 'Explain in terms')[0] + ' ' + cut(Q11CA_BUCKY, 'What type of bond')[0],
    figure=FIG + 'paper-q11c-a', cid='q11-c-a-x-rays', ref_suffix='after (iii), the father and son')
# (c)B: oxygen from liquid air.
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-u3', 'purifying-air-before-liquefying-it')
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-u3', 'fractional-distillation-of-liquid-air', figure=S + 'q11c-b-ii',
        row_notes={0: 'DESCRIBE. The scheme draws the column beside its points, shown with the answer.'})
# (iii): EXPLAIN "Continuous // Air goes in at one end ..." (2 × 3), then "Air is cooled
# and fractionated continuously [Give the two (3)s for this.]" (scheme page 16, y 451-504).
_b3 = P.items(ka('11', 'c', 'iii', 'B'))
_cont = pts(_b3[0])
_alt, _alt_a = split_asides(display(_b3[1].text))
assert [it.cell for it in _b3] == ['[2 × 3]', None] and _cont[0] == 'Continuous' and \
    _alt == 'Air is cooled and fractionated continuously' and _alt_a == ['[Give the two (3)s for this.]'], _b3
C.add([ka('11', 'c', 'iii', 'B')], 'chem-u3', 'a-continuous-process', [
    menu_row('r-1', [_cont[0], _alt], 1, 'EXPLAIN: the scheme prices its two points (2 × 3), one each; below them it '
             'prints the second wording and adds "' + _alt_a[0] + '": claim it here and again below.', per=3, total=3),
    menu_row('r-2', [_cont[1], _alt], 1, 'And the reason, (3), or the second wording again.', per=3, total=3)], total=6)
# (iv): NAME (3); USE (3), one use of the co-product named, the scheme's four lists
# (page 16, y 551-660).
_b4 = P.items(ka('11', 'c', 'iv', 'B'))
assert [it.cell for it in _b4] == ['[3]', '[3]'] and _b4[1].asides == ['[Use must be matched with named co-product]'], _b4
_uses = [raw(16, 550, 580, 160), raw(16, 588, 605, 160), raw(16, 610, 627, 160), raw(16, 632, 662, 160, 510)]
assert [u.split(':')[0] for u in _uses] == ['Nitrogen', 'Neon', 'Argon', 'Xenon'] and _uses[3].endswith('MRI /CT'), _uses
C.add([ka('11', 'c', 'iv', 'B')], 'chem-u3', 'co-products-of-air-and-their-uses', [
    lift('r-1', _b4[0].text, 3, 'NAME.'),
    menu_row('r-2', _uses, 1, 'USE: one use of the co-product named, (3), from the scheme\'s list for it. The scheme adds: '
             + _b4[1].asides[0], per=3, total=3)], total=6)


# A note quoted from the scheme in the reader's script notation ("K_(c)") is
# shown as the page sets it.
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or '') or '^(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'] and '^(' not in _r['contextNote'], _r


# ── review ───────────────────────────────────────────────────────────────────
def printed():
    """Every letter's printed marks: the paper sets one mark after a letter's
    last part, or several, one after each run of asks."""
    out = {}
    for key, last in P.marks.items():
        if not key[1]:
            continue
        at = [m for s in P.pseg if s.key[:2] == key[:2] for _n, m in s.marks_at]
        out[key[:2]] = sum(at) if at else last
    # Q10(b)(iii)'s mark "(3)" prints in one run with its words ("... low energy
    # electromagnetic radiations. (3)", paper page 6, x 122-532, y 566): the reader takes
    # it off the ask as the letter's mark, not as a mark after a run of text.
    iii = P.pseg_of(k('10', 'b', 'iii'))
    assert not iii.marks_at and out[('10', 'b')] == 22, (iii.marks_at, out[('10', 'b')])
    out[('10', 'b')] += 3
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
