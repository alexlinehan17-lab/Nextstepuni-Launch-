#!/usr/bin/env python3
"""2012 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2012_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2012_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2012_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2012 hl

No 2012 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, the
second route's steps as alternatives beside them, and the scheme's own print of
the working as the card's figure.

Reader (chem_print, gated to 2012 HL). The paper sets the head of Question 4 in
one run with its words ("4. Answer eight of the following items ..."); unread,
the paper reader found Questions 1-3 only (OLD_OL_HEADS joined). It sets the
state symbol "(l)" of the product Q6(a)(iii) draws as a run of its own, read as
a letter marker (a phantom Q6(l)): dropped. The scheme's running footer "ATAL
Chemistry 2012 - Marking Scheme Page N of 15", the head "SECTION B" and the
line "Question 11 continued/" were filed as answers of the part before them:
dropped (chem_print.Printed, the 2012 HL block).

Census (paper.py, gated to 2012 HL Chemistry): the three conversions Q6(a)
names are set as numbered equations in a column right of its words, a text
block that opens above the "6." head; read first, its romans were filed as
Q5(e)(i)-(iii) and Q5(e) itself was lost (paper.FIGURE_BLOCKS). With the paper
reader whole, Q4(k) and Q11(c) are read as their A and B alternatives
(paper_census.chemistry_choice_parts). The census keeps the paper's 75 asks.

Romans the paper sets inside one sentence are one census ask and a card per
scheme cell, each showing the sentence with a "For (i)."-style note: Q3(b),
Q8(a) and Q10(b)'s calculation (a cell each); Q4(a), Q4(h) and Q5(e) (one cell
over both: one card). Where a letter prints a mark after each of several asks,
each run is a card cited with what it holds (Q1(b), Q7(a), Q7(b), Q9(a), Q9(b),
Q10(b), Q11(b)). Q4(k) and Q11(c) offer alternative parts A and B.

The paper underlines the terms Q1(a) and Q8(b) ask about, which no text layer
carries: those cards take the paper's own print as their question, as do the
parts whose answer is a scheme crop and whose ask needs the paper's equation,
table or reaction scheme (Q1(e), Q6(b), Q8(d), Q9(a) three times, Q10(b)'s
calculation, Q11(b)'s expression and calculation). Q8(d) names the conversions
labelled R: its label key is the scheme's own answer, as 2011 OL's Z. The paper draws the arrows of the Q1, Q4(e)
and Q10(c) equations and sets the equilibrium arrows of Q10(b) and Q11(b) in a
glyph the text layer reads as U+0595: those equations are paper crops, kept out
of the text. The scheme draws the arrows of Q2(d) and Q4(e) too: each is set
back where the page prints it, asserted on the reader's text.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, point, read_lines, tidy  # noqa: E402

P = Printed(2012, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2012-HL-'
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
        raise Refused(f'"{text}" is not in the 2012 hl scheme')
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


def arrow(text, before, after):
    """The scheme's equation with its arrow set back where the page draws it: the
    arrow is a drawn line the text layer does not carry ("C₂H₅OH C₂H₄ + H₂O")."""
    old = before + ' ' + after
    assert text.count(old) == 1, (text, old)
    return text.replace(old, before + ' → ' + after)


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 A primary standard and a titration of hydrochloric acid ───────────────
# The equation the lead-in ends with (paper page 2, y 200) draws its arrow, which
# the text layer does not carry: it is read as a picture's ('q1-eq'), and the
# cards that need it take the paper's print of the lead-in as their question.
Q1_FULL = C.context(k('1', 'b'))
assert Q1_FULL.endswith('The mean titre was 20.8 cm³. The balanced equation for the titration reaction was:'), Q1_FULL
Q1_STEM = cut(Q1_FULL, 'The balanced equation')[0]
# (a): EXPLAIN, two points "ANY TWO: (3 + 2)" (scheme page 5, y 67-137). The paper
# underlines "primary standard" (page 2, y 124): its own print is the question.
_q1a = P.items(k('1', 'a'))
assert [it.cell for it in _q1a] == ['[3 + 2]'] and '[any two]' in _q1a[0].asides, _q1a
_pts = [display(p) for p in _q1a[0].points()]
assert len(_pts) == 2 and _pts[1].endswith('mass (Mr)'), _pts
_two = raw(5, 120, 140, 400)
assert _two == 'ANY TWO: (3 + 2)', _two
C.add([k('1', 'a')], 'chem-4-1', 'a-primary-standard', [
    lift('r-1', _pts[0], None, 'The scheme prices its two points "' + _two + '".'),
    lift('r-2', _pts[1], None)], kind='orderedSplit', notation='[3 + 2]', total=5,
    notes=SPLIT.format('[3 + 2]'), stem=Q1_STEM)
print_question('paper-q1a-print')
# (b): DESCR, four points "ANY FOUR: (4 × 3)", printed (12); CALC (6), printed (6),
# worked in a box, a fraction (3) and its value (3): a card each.
Q1B_DESC, Q1B_CALC = cut(P.ask(k('1', 'b')), 'Calculate the exact mass')
_q1b = P.items(k('1', 'b'))
assert [it.cell for it in _q1b] == ['[4 × 3]', '[6]', '[3]', None], _q1b
_desc = [display(p) for p in _q1b[0].points()]
assert len(_desc) == 4 and _desc[2].startswith('add deionised* water'), _desc
_four = raw(5, 168, 186, 400)
_dei = traced(raw(5, 180, 198, 120))
assert _four == 'ANY FOUR: (4 × 3)' and _dei.startswith('*[Accept if “deionised water”'), (_four, _dei)
C.add([k('1', 'b')], 'chem-4-1', 'making-up-a-primary-standard-solution', [
    lift('r-1', _desc[0], 3, 'The scheme prices these points "' + _four + '", one each.'),
    lift('r-2', _desc[1], 3),
    lift('r-3', _desc[2], 3, 'The scheme adds: ' + _dei),
    lift('r-4', _desc[3], 3)],
    qtext=Q1B_DESC, stem=Q1_STEM, cid='q1-b-describe', ref_suffix='making up the solution')
assert display(_q1b[1].text).endswith(' 2.65 g') and display(_q1b[2].text) == '500 × 0.05 × 106* (3) = 2.65', _q1b
_slip = traced('* Addition must be shown for error to be treated as a slip.')
C.add([k('1', 'b')], 'chem-4-1', 'mass-of-sodium-carbonate-for-a-standard-solution', [
    lift('r-1', '500 × 0.05 × 106* ÷ 1000', 3, 'CALC: the scheme gives the answer, 2.65 g, priced (6), then two '
         'steps (3) each, in a box. ' + FRACTION.format('500 × 0.05 × 106*', '1000') + ' It adds: "' + _slip + '"'),
    lift('r-2', '= 2.65', 3)],
    qtext=Q1B_CALC, stem=Q1B_DESC, figure=S + 'q1b', cid='q1-b-mass', ref_suffix='mass of sodium carbonate')
C.fixed([k('1', 'c', 'i')], 'chem-4-1', 'adjusting-a-burette-to-the-zero-mark', stem=Q1_STEM)
C.fixed([k('1', 'c', 'ii')], 'chem-4-1', 'why-a-pipette-filler-is-used', stem=Q1_STEM)
# (d): NAME "indicator" (3), CHANGE "colour before // colour after" (2 × 3), from
# the scheme's table of five indicators (page 5, y 397-473), matched.
_q1d = P.items(k('1', 'd'))
assert [it.cell for it in _q1d] == ['[3]', '[2 × 3]', None] and display(_q1d[0].text) == 'indicator' and \
    display(_q1d[1].text) == 'colour before // colour after', _q1d
_tab = [(raw(5, y - 1, y + 15, 130, 230), raw(5, y - 1, y + 15, 230, 335), raw(5, y - 1, y + 15, 335, 410))
        for y in (409.6, 422.0, 434.3, 446.7, 459.1)]
assert [t[0] for t in _tab] == ['Methyl orange', 'Methyl red', 'Methyl yellow', 'Bromophenol blue',
                                'Bromocresol green'], _tab
assert [t[1] for t in _tab] == ['Orange (yellow)', 'Yellow', 'Yellow', 'Blue (purple, violet)', 'Blue'] and \
    [t[2] for t in _tab] == ['Red (pink)', 'Red (pink)', 'Red (pink)', 'Yellow', 'Yellow'], _tab
_link = _q1d[2].asides[0]
assert _link.startswith('[Linked marks'), _q1d[2]
C.add([k('1', 'd')], 'chem-4-1', 'indicator-for-hydrochloric-acid-and-sodium-carbonate', [
    menu_row('r-1', [t[0] for t in _tab], 1, 'NAME: "indicator" (3), one of those in the scheme\'s table, shown with '
             'the answer.', per=3, total=3),
    menu_row('r-2', list(dict.fromkeys(t[1] for t in _tab)), 1, 'CHANGE: "colour before // colour after" (2 × 3): the '
             'colour before, (3), of the indicator named, as the scheme\'s table gives it. The scheme adds: ' + _link,
             per=3, total=3),
    menu_row('r-3', list(dict.fromkeys(t[2] for t in _tab)), 1, 'And the colour after, (3), of the same indicator.',
             per=3, total=3)], total=9, stem=Q1_STEM, figure=S + 'q1d')
# (e): the paper sets (i) and (ii) on lines of their own (page 2, y 418 and 437)
# completing one sentence; the scheme prices (i) (9), its working in a box as a
# fraction the text layer reads apart, and (ii) (3), the one step that earns it.
Q1E = P.ask(k('1', 'e')) + ' (i) ' + P.ask(k('1', 'e', 'i')) + ' (ii) ' + P.ask(k('1', 'e', 'ii'))
assert Q1E.endswith('acid solution in (i) moles per litre, (ii) grams per litre.'), Q1E
_q1e1 = P.items(k('1', 'e', 'i'))
assert [it.cell for it in _q1e1] == ['[9]', '[6]', '[3]'] and display(_q1e1[0].text) == '0.12 M' and \
    display(_q1e1[2].text).endswith('MHCl = 0.12'), _q1e1
C.add([k('1', 'e', 'i')], 'chem-4-1', 'concentration-of-hydrochloric-acid-in-moles-per-litre', [
    lift('r-1', '0.12 M', 9, 'For (i). The scheme prices the answer (9) and works it in a box: 20.8 × MHCl over 2 = '
         '25 × 0.05 over 1, set as fractions, (6), then MHCl = 0.12 (3); its own print is shown with the answer.')],
    qtext=Q1E, stem=Q1_STEM, figure=S + 'q1e')
print_question('paper-q1e-print')
_q1e2 = P.items(k('1', 'e', 'ii'))
_note = traced('NOTE: Treat answers not given to two decimal places as slips.')
assert [it.cell for it in _q1e2] == ['[3]', '[3]', None] and display(_q1e2[0].text) == '4.38 / 4.39 g l⁻¹' and \
    display(_q1e2[1].text) == '0.12 × 36.5* = 4.38', _q1e2
C.add([k('1', 'e', 'ii')], 'chem-4-1', 'concentration-of-hydrochloric-acid-in-grams-per-litre', [
    lift('r-1', _q1e2[0].text, 3, 'For (ii). The scheme gives the answer, priced (3), and the one step that earns it: '
         '"0.12 × 36.5* = 4.38" (3). It adds: "' + _slip + '" "' + _note + '"')],
    qtext=Q1E, stem=Q1_STEM, figure=S + 'q1e')
print_question('paper-q1e-print')

# ── Q2 Preparing ethene from ethanol ─────────────────────────────────────────
# (a): DRAW, four points (3), (3), (3), (2), beside the scheme's drawing (page 6,
# x 312-547), whose labels are read as its picture's (crop 'scheme-q2a').
_q2a = P.items(k('2', 'a'))
assert [it.cell for it in _q2a] == ['[3]', '[3]', '[3]', '[2]', None] and display(_q2a[4].text) == 'No diagram: – 3', _q2a
C.fixed([k('2', 'a')], 'chem-4-2', 'apparatus-for-preparing-ethene-from-ethanol', figure=S + 'q2a', tail=True,
        row_notes={0: 'The scheme prices four points of the diagram (3), (3), (3) and (2) and draws the apparatus '
                      'beside them, shown with the answer.'})
C.fixed([k('2', 'b', 'i')], 'chem-u2', 'when-suck-back-happens')
C.fixed([k('2', 'b', 'ii')], 'chem-u2', 'what-a-suck-back-can-do')
C.fixed([k('2', 'b', 'iii')], 'chem-u2', 'avoiding-suck-back')
# (c): TEST, "reagent used" (3), then "bubble through (shake with) // colour before //
# colour after ANY TWO: (2 × 3)", the reagents and their colours in a table (scheme
# page 6, y 354-440).
_q2c = P.items(k('2', 'c'))
assert [it.cell for it in _q2c][:2] == ['[3]', '[2 × 3]'] and display(_q2c[0].text) == 'reagent used' and \
    display(_q2c[1].text) == 'bubble through (shake with) // colour before // colour after', _q2c
_br = raw(6, 365, 381, 135, 295)
_mn = raw(6, 401, 429, 135, 295)
assert _br == 'Bromine (Br₂) water (soln) (3)' and _mn == 'Acidified manganate(VII)* solution (3)', (_br, _mn)
_red, _purple = raw(6, 365, 381, 295, 460), raw(6, 401, 417, 295, 460)
_col = raw(6, 377, 393, 295, 460)
assert _red == 'Red (orange, yellow, brown) (3)' and _purple == 'Purple (violet, pink) (3)' and \
    _col == 'to colourless[not “clear”] (3)', (_red, _purple, _col)
_dec = traced('[Allow 3 marks for decolourise]')
_star = traced(raw(6, 440, 458, 120))
assert _star.startswith('*For “manganate(VII)” accept'), _star
_anytwo = raw(6, 333, 350, 440)
assert _anytwo == 'ANY TWO: (2 × 3)', _anytwo
C.add([k('2', 'c')], 'chem-2-4', 'testing-ethene-for-unsaturation', [
    menu_row('r-1', [_br[:-len(' (3)')], _mn[:-len(' (3)')]], 1, 'TEST: "reagent used" (3), one of the two in the '
             'scheme\'s table, shown with the answer. The scheme adds: ' + _star, per=3, total=3),
    menu_row('r-2', ['bubble through (shake with)', _red[:-len(' (3)')], _purple[:-len(' (3)')], 'to colourless'], 2,
             'Claim the colour before of the reagent claimed above, not the other reagent\'s. '
             'Any two of these, (3) each: "bubble through (shake with) // colour before // colour after ' + _anytwo
             + '". The colour before is the reagent\'s own, red (orange, yellow, brown) for bromine water and purple '
             '(violet, pink) for acidified manganate(VII); the colour after is colourless for both. The scheme adds: '
             '[not “clear”] ' + _dec, per=3, total=6)], total=9, figure=S + 'q2c')
# (d): WRITE (6). The scheme draws the equation's arrow (page 6, x 165-200, y 497).
_q2d = P.items(k('2', 'd'))
assert [it.cell for it in _q2d] == ['[6]'] and display(_q2d[0].text) == 'C₂H₅OH C₂H₄ + H₂O' and \
    len(_q2d[0].asides) == 2, _q2d
_allow = arrow(display(_q2d[0].asides[1]), 'C₂H₅OH', 'C₂H₄ ]').replace('C₂H₄ ]', 'C₂H₄]')
C.add([k('2', 'd')], 'chem-4-2', 'equation-for-dehydrating-ethanol', [
    lift('r-1', arrow(display(_q2d[0].text), 'C₂H₅OH', 'C₂H₄'), 6, 'The scheme adds: ' + display(_q2d[0].asides[0])
         + ' ' + _allow)])
# (e): NUMBER (15), five steps (3) each in a box, the third and fourth in two
# routes side by side (page 6, y 570-680).
_q2e = P.items(k('2', 'e'))
_e = [display(it.text) for it in _q2e]
assert [it.cell for it in _q2e] == ['[15]'] + ['[3]'] * 7 + [None] and _e[0] == '8 test tubes', _q2e
assert _e[3].startswith('0.042 (0.0417) × 24000') and _e[4].startswith('60% of 0.042') and \
    _e[5].startswith('60% of 1008') and _e[6].startswith('0.0252 (0.025) × 24000'), _e
_molar = traced('Note: Use of 22.4 litres as molar volume loses 3.')
C.add([k('2', 'e')], 'chem-1-4', 'test-tubes-of-ethene-from-ethanol-at-60-percent-yield', [
    lift('r-1', _e[1], 3, 'The scheme gives the answer, 8 test tubes, priced (15), then five steps (3) each.'),
    lift('r-2', _e[2], 3, 'The scheme adds: "' + _slip + '"'),
    menu_row('r-3', [_e[3], _e[4]], 1, 'One of these, (3): the volume of ethene in theory, or the moles at 60%, '
             'as the scheme\'s two routes set them side by side.', per=3, total=3),
    menu_row('r-4', [_e[5], _e[6]], 1, 'And the next step of that same route, (3).', per=3, total=3),
    lift('r-5', _e[7], 3, 'The scheme adds: "' + _molar + '"')], total=15, figure=S + 'q2e')

# ── Q3 The relative molecular mass of a volatile liquid ──────────────────────
Q3 = FIG + 'paper-q3'
Q3_STEM = C.context(k('3', 'a'))
assert Q3_STEM.endswith('either apparatus A or apparatus B shown below.'), Q3_STEM
C.fixed([k('3', 'a')], 'chem-2-3', 'a-volatile-liquid-for-the-experiment', figure=Q3)
# (b): the paper sets (i) and (ii) inside one sentence (page 3, y 175); the scheme
# prices (i) (3 × 3) and (ii) (6), each for apparatus A, or after "or" for B.
Q3B = P.ask(k('3', 'b'))
assert Q3B == 'Describe how (i) the mass, (ii) the volume, of the vapour is determined.', Q3B
_mass_a = [x.strip() for x in raw(7, 157, 185, 130).split('//')]
_mass_b = [x.strip() for x in raw(7, 221, 250, 130, 506).split('//')]
assert len(_mass_a) == 3 and len(_mass_b) == 3 and _mass_a[2] == 'mass is difference (find difference)' and \
    _mass_b[2] == 'mass is difference (find difference)' and cells(k('3', 'b', 'i')) == ['[3 × 3]'], (_mass_a, _mass_b)
C.add([k('3', 'b', 'i')], 'chem-2-3', 'finding-the-mass-of-the-vapour', [
    menu_row('r-1', [_mass_a[0], _mass_b[0]], 1, 'For (i). One of these, (3): the first for "Apparatus A*", the '
             'second, after "or", for "Apparatus B*"; the scheme prices the three points of each (3 × 3), one each.',
             per=3, total=3),
    menu_row('r-2', [_mass_a[1], _mass_b[1]], 1, 'And the next point for that same apparatus, (3).', per=3, total=3),
    lift('r-3', _mass_a[2], 3, 'The same third point for either apparatus.')],
    total=9, qtext=Q3B, stem=Q3_STEM, figure=Q3)
_vol_a, _vol_b = raw(7, 274, 291, 130), raw(7, 321, 338, 130, 500)
assert _vol_a.startswith('fill flask with water') and _vol_b.startswith('read volume from scale') and \
    cells(k('3', 'b', 'ii')) == ['[6]'], (_vol_a, _vol_b)
C.add([k('3', 'b', 'ii')], 'chem-2-3', 'finding-the-volume-of-the-vapour', [
    menu_row('r-1', [_vol_a, _vol_b], 1, 'For (ii). One of these, (6): the first for "Apparatus A*", the second, '
             'after "or", for "Apparatus B*".', per=6, total=6)],
    total=6, qtext=Q3B, stem=Q3_STEM, figure=Q3)
# (c): EXPL (2 × 3), two points for apparatus A or, after "or", two for B.
_ca = [x.strip() for x in raw(7, 345, 373, 130).split('//')]
_cb = [x.strip() for x in raw(7, 381, 421, 130, 522).split('//')]
_nb = traced(raw(7, 416, 457, 130))
assert len(_ca) == 2 and len(_cb) == 2 and _cb[1].startswith('until vapour pressure reaches') and _nb.startswith('N.B. Marks to be awarded for either A or B') and \
    cells(k('3', 'c')) == ['[2 × 3]', None], (_ca, _cb)
C.add([k('3', 'c')], 'chem-2-3', 'why-the-vapour-is-at-atmospheric-pressure', [
    menu_row('r-1', [_ca[0], _cb[0]], 1, 'One of these, (3), for the apparatus used; the scheme sets the second after '
             '"or" and prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_ca[1], _cb[1]], 1, 'And the second point for that same apparatus, (3). The scheme adds: "'
             + _nb + '"', per=3, total=3)], total=6, figure=Q3)
# (d): MOL (9), three steps (3) each in two routes side by side; Mr (6), two steps
# (3) each (scheme page 7, y 465-646).
_q3d = P.items(k('3', 'd'))
assert [it.cell for it in _q3d][0] == '[9]' and display(_q3d[0].text) == '0.01076 [Allow 0.01 to 0.011 mol]', _q3d
_r1 = [raw(7, 488, 505, 130, 300), raw(7, 511, 541, 130, 300), raw(7, 548, 565, 130, 300)]
_r2 = [raw(7, 523, 541, 320, 480), raw(7, 548, 565, 320, 480)]
assert _r1 == ['equation of state (correct) (3)', '101 × 10³× 330 × 10⁻⁶ 8.3 × 373 (3)', '= 0.01076 to 0.011 (3)'] \
    and _r2 == ['Vroom = 259 cm³ (3)', '259 ÷ 24000 = 0.0108 (3)'], (_r1, _r2)
_mr = [raw(7, 606, 623, 140), raw(7, 630, 647, 140)]
_stp = traced(raw(7, 571, 588, 320))
assert _mr == ['0.63 ÷ 0.01076 to 0.011 (3)', '= 57 to 63 (3)'] and _stp == '*similar method at s.t.p.', (_mr, _stp)
# Its only figure is the scheme's working, held back until the reveal, so the question's
# lead-in "... either apparatus A or apparatus B shown below." would point at nothing. Nothing
# in (d) depends on the apparatus: it prints the mass, volume, temperature and pressure the
# moles and the relative molecular mass are worked from. The lead-in is left out of its stem.
assert C.context(k('3', 'd')) == ('The relative molecular mass of a volatile liquid can be found by means of a '
                                  'procedure involving the use of either apparatus A or apparatus B shown below.'), \
    C.context(k('3', 'd'))
C.add([k('3', 'd')], 'chem-2-3', 'moles-and-relative-molecular-mass-of-the-vapour', [
    lift('r-1', 'equation of state (correct)', 3, 'MOL: the scheme gives the answer, "0.01076 [Allow 0.01 to 0.011 '
         'mol]", priced (9), then three steps (3) each; or, after "or", Vroom over 293* = 330 over 373, set as '
         'fractions, (3), "' + _stp + '"'),
    menu_row('r-2', ['101 × 10³× 330 × 10⁻⁶ ÷ 8.3 × 373', 'Vroom = 259 cm³'], 1, 'One of these, (3), by the route '
             'used. ' + FRACTION.format('101 × 10³ × 330 × 10⁻⁶', '8.3 × 373'), per=3, total=3),
    menu_row('r-3', ['= 0.01076 to 0.011', '259 ÷ 24000 = 0.0108'], 1, 'And the moles by that same route, (3).',
             per=3, total=3),
    lift('r-4', '0.63 ÷ 0.01076 to 0.011', 3, 'Mr: the scheme gives the answer, "57 to 63", priced (6), then two '
         'steps (3) each.'),
    lift('r-5', '= 57 to 63', 3)], total=15, figure=S + 'q3d', stem='')
C.fixed([k('3', 'e')], 'chem-2-3', 'limits-of-the-method-and-the-mass-spectrometer', figure=Q3,
        row_notes={0: 'WHY.', 1: 'WHAT.'})

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
# (a): STATE "(i) 5, (ii) 9" (2 × 3), the paper setting (i) and (ii) inside its ask.
_q4a = P.items(k('4', 'a', 'i'))
assert [(it.cell, display(it.text)) for it in _q4a] == [('[2 × 3]', '5, (ii) 9')] and not P.items(k('4', 'a')), _q4a
C.add([k('4', 'a')], 'chem-1-2', 'sublevels-and-orbitals-occupied-in-argon', [
    lift('r-1', '(i) 5', 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '(ii) 9', 3)], notes=Q4_NOTE)
# (b): WRITE (6): the scheme answers with the nuclear equation, its mass and atomic
# numbers set above and below each symbol (page 8, x 150-340, y 150-188), read as
# its picture's (crop 'scheme-q4b').
C.drawn([k('4', 'b')], 'chem-1-2', 'beta-decay-of-iodine-131', S + 'q4b', notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-1-2', 'relative-atomic-mass', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-2-1', 'sigma-and-pi-bonds-distinguished', notes=Q4_NOTE)
# (e): BALANCE (6). The scheme draws the equation's arrow (page 8, x 280-330, y 338);
# the paper's own equation, its arrow drawn too, is the card's figure.
_q4e = P.items(k('4', 'e'))
assert [it.cell for it in _q4e] == ['[6]'] and display(_q4e[0].text) == 'Cu + 2NO₃¯ + 4H⁺ Cu²⁺ + 2NO₂ + 2H₂O', _q4e
C.add([k('4', 'e')], 'chem-3-5', 'balancing-copper-and-nitric-acid-by-oxidation-numbers', [
    lift('r-1', arrow(display(_q4e[0].text), '4H⁺', 'Cu²⁺').replace('2NO₃¯', '2NO₃⁻'), 6)],
    notes=Q4_NOTE, figure=FIG + 'paper-q4e')
C.fixed([k('4', 'f')], 'chem-2-3', 'avogadros-law', notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-3-2', 'why-rate-rises-with-temperature', notes=Q4_NOTE)
# (h): NAME "(i) hydrogen // (ii) hydroxyl (hydroxide, OH¯) ions" (2 × 3).
_q4h = P.items(k('4', 'h', 'i'))
assert [(it.cell, display(it.text)) for it in _q4h] == [('[2 × 3]', 'hydrogen // (ii) hydroxyl (hydroxide, OH¯) ions')], \
    _q4h
C.add([k('4', 'h')], 'chem-3-5', 'products-at-the-cathode-in-sodium-sulfate-electrolysis', [
    lift('r-1', '(i) hydrogen', 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '(ii) hydroxyl (hydroxide, OH⁻) ions', 3)], notes=Q4_NOTE)
C.fixed([k('4', 'i')], 'chem-3-1', 'definition-of-bond-energy', notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-4-3', 'secondary-sewage-treatment', notes=Q4_NOTE)
# (k): A, "Low: ... // High: ..." (2 × 3), its letter set "(k) A:" in one run (page 8,
# x 64, y 575) and read under (k); or B, "Scrub: ... // ..." (2 × 3).
_q4ka = P.items(k('4', 'k'))
_ka = [display(x).strip() for x in _q4ka[0].text.split('//')]
assert [it.cell for it in _q4ka] == ['[2 × 3]'] and _ka[0].startswith('A: Low: have branching') and len(_ka) == 2, _q4ka
C.add([ka('4', 'k', None, 'A')], 'chem-4-2', 'low-and-high-density-polyethene', [
    lift('r-1', _ka[0][len('A: '):], 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _ka[1], 3, 'The scheme adds: ' + ' '.join(_q4ka[0].asides))], notes=Q4_NOTE)
_q4kb = P.items(ka('4', 'k', None, 'B'))
_kb = [display(x).strip() for x in _q4kb[0].text.split('//')]
assert [it.cell for it in _q4kb] == ['[2 × 3]'] and _kb[0] == 'Scrub: lime (CaO) / limestone (CaCO₃)', _q4kb
C.add([ka('4', 'k', None, 'B')], 'chem-4-3', 'scrubbing-acidic-waste-gases', [
    lift('r-1', _kb[0][len('Scrub: '):], 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _kb[1], 3, 'The scheme adds: ' + ' '.join(_q4kb[0].asides))], notes=Q4_NOTE,
    qtext=P.ask(ka('4', 'k', None, 'B'), upto='in industry?'))

# ── Q5 Electrons, atomic radius and bonding in hydrides ──────────────────────
# (a): WRITE (3 + 2): "1s²2s² // 2px²2py¹2pz¹ /" or "1s²2s² // 2p⁴ and" the 2p
# orbitals drawn as boxes (scheme page 9, y 65-120).
_q5a = P.items(k('5', 'a'))
assert [it.cell for it in _q5a] == ['[3 + 2]'] and \
    display(_q5a[0].text) == '1s²2s² // 2px²2py¹2pz¹ / 1s²2s² // 2p⁴ and', _q5a
_acc5 = traced('The electron pair can be in any one of the p orbitals. Lines or dots will do in place of arrows in the '
               'boxes.')
C.add([k('5', 'a')], 'chem-1-2', 'electron-configuration-of-oxygen-in-orbitals', [
    lift('r-1', '1s²2s²', None, 'The scheme prices its two points (3 + 2).'),
    menu_row('r-2', ['2px²2py¹2pz¹', '2p⁴'], 1, 'One of these: the scheme sets the second as "2p⁴ and" the three 2p '
             'orbitals drawn as boxes, two arrows in the first, one in each of the others; its own print is shown with '
             'the answer. It adds that subscripts are accepted, and: "' + _acc5 + '"')],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), figure=S + 'q5a')
C.fixed([k('5', 'b')], 'chem-1-3', 'atomic-radius-and-its-trend-across-a-period',
        row_notes={0: 'DEFINE.', 1: 'STATE.', 2: 'EXPLAIN.'})
C.fixed([k('5', 'c')], 'chem-1-3', 'why-electronegativity-rises-across-a-period')
C.fixed([k('5', 'd', 'i')], 'chem-2-1', 'bonding-in-phosphine-and-the-other-hydrides', row_notes={0: 'STATE.', 1: 'WHAT.'})
_q5d2 = P.items(k('5', 'd', 'ii'))
assert [(it.cell, display(it.text)) for it in _q5d2][0] == ('[2 × 3]', 'H₂O // NH₃'), _q5d2
C.add([k('5', 'd', 'ii')], 'chem-2-2', 'hydrides-that-hydrogen-bond', [
    lift('r-1', 'H₂O', 3, 'FROM. The scheme prices these points (2 × 3), one each, and adds: '
         + display(' '.join(_q5d2[0].asides))),
    lift('r-2', 'NH₃', 3),
    lift('r-3', _q5d2[1].text, 3, 'GIVE.')])
C.fixed([k('5', 'd', 'iii')], 'chem-2-2', 'shape-of-the-phosphine-molecule', figure=S + 'q5d-iii',
        row_notes={0: 'SHAPE.', 1: 'EXPL. After the first wording\'s "/" the scheme draws the PH₃ molecule, its lone '
                                 'pair on the P; its own print is shown with the answer.'})
# (e): WOULD "(i) B – Cl bond: polar // (ii) BCl₃ molecule: non-polar" (2 × 3), the
# paper setting (i) and (ii) inside its ask; JUSTIFY (3).
_q5e = P.items(k('5', 'e', 'i'))
assert [(it.cell, display(it.text)) for it in _q5e][0] == ('[2 × 3]', 'B – Cl bond: polar // (ii) BCl₃ molecule: '
                                                                        'non-polar') and _q5e[1].cell == '[3]', _q5e
C.add([k('5', 'e')], 'chem-2-2', 'polar-bonds-in-a-non-polar-molecule', [
    lift('r-1', '(i) B – Cl bond: polar', 3, 'WOULD. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '(ii) BCl₃ molecule: non-polar', 3),
    lift('r-3', _q5e[1].text, 3, 'JUSTIFY.')])

# ── Q6 Oil refining and the heat of formation of isooctane ───────────────────
# The three conversions are numbered equations in a column right of (a) and (b)
# (paper page 5, x 257-538, y 25-180), the paper's crop 'paper-q6'.
Q6 = FIG + 'paper-q6'
# (a): NAME, (i) // (ii) // (iii) priced together (3 + 3 + 2).
_q6a = [display(it.text) for r in ('i', 'ii', 'iii') for it in P.items(k('6', 'a', r))]
assert _q6a == ['dehydrocyclisation (cyclodehydrogenation) / reforming //', 'catalytic cracking //',
                'isomerisation / reforming'] and cells(k('6', 'a', 'iii')) == ['[3 + 3 + 2]'], _q6a
C.add([k('6', 'a')], 'chem-2-4', 'reforming-cracking-and-isomerisation', [
    lift('r-1', '(i) ' + _q6a[0].rstrip('/ '), None, 'The scheme prices these points (3 + 3 + 2).'),
    lift('r-2', '(ii) ' + _q6a[1].rstrip('/ '), None),
    lift('r-3', '(iii) ' + _q6a[2], None)],
    kind='orderedSplit', notation='[3 + 3 + 2]', total=8, notes=SPLIT.format('[3 + 3 + 2]'), figure=Q6)
# (b): HYDROCARBON (3), STRUCTURE (3), PRODUCT (3), OCTANE NUMBER (3) (scheme page
# 10, y 117-324). The structures are formulas, a branch drawn under the third, then
# skeletons, and cyclobutane and methylcyclopropane accepted, each drawn twice: its
# own print is the card's figure. The paper's mark "(12)" prints at the end of the
# text column (page 5, x 230, y 165), the column right of it taken by the equations,
# and is read as words of (b): left out of the ask. The question needs X and process
# (iii): its own print (the equations, then (b)) is the question.
_q6b = P.items(k('6', 'b'))
assert [it.cell for it in _q6b] == ['[3]'] * 4, _q6b
_hc = display(_q6b[0].text)
_st = raw(10, 140, 157, 80)
assert _st.startswith('STRUCTURE: '), _st
_st = _st[len('STRUCTURE: '):]
_acc6 = raw(10, 235, 252, 130)
_nm = traced(raw(10, 264, 281, 130))
assert _hc == 'but-1-ene (1-butene) / but-2-ene (2-butene) / 2-methylpropene' and \
    _st == 'CH₂ =CHCH₂CH₃ / CH₃CH=CHCH₃ / CH₃C=CH₂ [(CH₃)₂C=CH₂]' and \
    _acc6 == 'Accept cyclobutane ( / ) & methylcyclopropane ( / )' and _nm.startswith('[Name and formula'), \
    (_hc, _st, _acc6, _nm)
_prod = raw(10, 291, 308, 160)
assert _prod == '2,2,4-trimethylpentane / isooctane (3)' and display(_q6b[3].text) == '100', (_prod, _q6b)
Q6B_LEAD = P.lead(k('6', 'b'))
assert Q6B_LEAD.endswith(' (12)'), Q6B_LEAD
C.add([k('6', 'b')], 'chem-2-4', 'a-hydrocarbon-for-x-and-isooctane', [
    menu_row('r-1', _hc.split(' / ') + ['cyclobutane', 'methylcyclopropane'], 1, 'HYDROCARBON: one of these, (3): '
             'the scheme also accepts cyclobutane and methylcyclopropane, drawing each structure twice.', per=3,
             total=3),
    menu_row('r-2', ['CH₂ =CHCH₂CH₃', 'CH₃CH=CHCH₃', '(CH₃)₂C=CH₂'], 1, 'STRUCTURE: one of these, (3), for the '
             'hydrocarbon named; the scheme sets the third as "CH₃C=CH₂" with a CH₃ drawn under its second carbon, '
             'then "[(CH₃)₂C=CH₂]", and draws each as a skeleton, shown with the answer. It adds: ' + _nm,
             per=3, total=3),
    lift('r-3', _prod[:-len(' (3)')], 3, 'PRODUCT.'),
    lift('r-4', '100', 3, 'OCTANE NUMBER.')],
    total=12, qtext=P.ask(k('6', 'b')) + ' ' + Q6B_LEAD[:-len(' (12)')], figure=S + 'q6b')
print_question('paper-q6b-print')
C.fixed([k('6', 'c')], 'chem-2-4', 'mtbe-and-leaded-petrol', tail=True,
        row_notes={0: 'EXPLAIN.', 1: 'NAME.', 2: 'STATE.'})
C.fixed([k('6', 'd')], 'chem-3-1', 'heat-of-combustion-and-the-bomb-calorimeter',
        row_notes={0: 'DEFINE.', 2: 'NAME.'})
# (e): CALCULATE (12): four equations (3) each, the last under a rule; then after
# "Equations not required" the sums of heats of formation (scheme page 10, y 550-709).
_q6e = P.items(k('6', 'e'))
_last = display(_q6e[4].text)
assert [it.cell for it in _q6e] == ['[12]'] + ['[3]'] * 7 and _last.endswith(' 8C + 9H₂ → C₈H₁₈ ΔH = – 224 kJ') and \
    _last.startswith('______'), _q6e
C.route([k('6', 'e')], 'chem-3-1', 'heat-of-formation-of-isooctane', figure=S + 'q6e',
        fixes={_last: '8C + 9H₂ → C₈H₁₈ ΔH = – 224 kJ'},
        notes='After "Equations not required" the scheme works it from the sums of heats of formation instead, '
              'pricing each term it uses (3).')
shown('The scheme gives the answer as "– 224 kJ mol⁻¹" (12). After "Equations not required" it works it from the sums '
      'of heats of formation instead, pricing each term (3), and adds "[+224 merits 3 marks only]"; its own print of '
      'both is shown with the answer.')

# ── Q7 Water: hardness, treatment and testing ────────────────────────────────
# (a): CAUSE (3) and WASTE (3); DE-ION, two points priced (3 + 2): a card each,
# the paper asking the first two in one sentence and the third in another.
Q7A_HARD, Q7A_ION = cut(P.ask(k('7', 'a')), 'How can hard water')
_q7a = P.items(k('7', 'a'))
assert [it.cell for it in _q7a] == ['[3]', '[3]', '[3 + 2]'], _q7a
_cause, _cause_a = split_asides(display(_q7a[0].text))
assert _cause.endswith('other soluble magnesium salt') and _cause_a == ['[Accept formulas]'], (_cause, _cause_a)
C.add([k('7', 'a')], 'chem-4-3', 'causes-of-hardness-and-soap-scum', [
    lift('r-1', _cause, 3, 'CAUSE. The scheme adds: ' + _cause_a[0]),
    lift('r-2', _q7a[1].text, 3, 'WASTE. The scheme adds: ' + ' '.join(_q7a[1].asides).replace('2RCOO¯', '2RCOO⁻'))],
    qtext=Q7A_HARD, cid='q7-a-hardness', ref_suffix='cause and soap')
_ion = [display(x).strip() for x in _q7a[2].text.split('//')]
assert _ion[0].startswith('DE-ION: pass through resin') and len(_ion) == 2, _ion
C.add([k('7', 'a')], 'chem-4-3', 'deionising-water-by-ion-exchange', [
    lift('r-1', _ion[0][len('DE-ION: '):], None, 'DE-ION. The scheme prices its two points (3 + 2).'),
    lift('r-2', _ion[1].replace('(OH¯)', '(OH⁻)'), None)],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), qtext=Q7A_ION, stem=Q7A_HARD,
    cid='q7-a-ion-exchange', ref_suffix='ion exchange')
# (b): the paper sets (i)-(v) inside its first sentence (page 5, y 375-400), printed
# (15), then the second ask, printed (6). The scheme prices PURPOSE (i)-(v) (5 × 3)
# and STATE (i)-(v) "ANY TWO: (2 × 3)" (page 11, y 252-431), its romans set again
# under STATE, so the reader files both answers of each roman together: its own
# lines are read here. A card each.
Q7B = P.ask(k('7', 'b')) + ' (ii) ' + P.ask(k('7', 'b', 'ii')) + ' (iii) ' + P.ask(k('7', 'b', 'iii'))
Q7B_PURPOSE, Q7B_EXCESS = cut(Q7B, 'State the problem')
assert Q7B_PURPOSE.endswith('(iv) calcium hydroxide, (v) sulfuric acid?') and Q7B_EXCESS.endswith('quantity.'), Q7B
_purpose = [raw(11, y - 1, y + 15, 120, 480).rstrip('/ ') for y in (252.6, 270.1, 287.7, 305.3, 322.8)]
_excess = [raw(11, y - 1, y + 15, 120, 495).rstrip('/ ') for y in (358.5, 373.2, 388.0, 402.7, 417.4)]
# (The first purpose's "(i)" is set in one run with "(b) PURPOSE:", x 65.)
assert _purpose[0].startswith('clumping') and raw(11, 251, 268, 60, 140) == '(b) PURPOSE: (i)'
_purpose[0] = '(i) ' + _purpose[0]
assert _purpose[0].startswith('(i) clumping') and _purpose[4] == '(v) lowers pH' and _excess[0].startswith(
    '(i) slight danger') and _excess[4] == '(v) pH too low (too acidic) / corrosion / tooth decay', (_purpose, _excess)
assert cells(k('7', 'b', 'v')) == ['[5 × 3]', '[2 × 3]'], cells(k('7', 'b', 'v'))
C.add([k('7', 'b')], 'chem-4-3', 'why-each-substance-is-added-in-water-treatment', [
    lift('r-1', _purpose[0], 3, 'PURPOSE. The scheme prices these points (5 × 3), one each.'),
    *[lift(f'r-{i + 2}', p, 3) for i, p in enumerate(_purpose[1:])]],
    qtext=Q7B_PURPOSE, cid='q7-b-purposes', ref_suffix='the purpose of each')
_two7 = raw(11, 415, 433, 440)
assert _two7 == 'ANY TWO: (2 × 3)', _two7
C.add([k('7', 'b')], 'chem-4-3', 'too-much-of-a-water-treatment-chemical', [
    menu_row('r-1', _excess, 2, 'STATE: any two of these, (3) each: "' + _two7 + '"; each is the problem for the '
             'substance its roman numbers.', per=3, total=6)],
    total=6, qtext=Q7B_EXCESS, stem=Q7B_PURPOSE, cid='q7-b-excess', ref_suffix='in excess')
C.fixed([k('7', 'c')], 'chem-4-3', 'heavy-metal-ions-in-water', row_notes={0: 'CONCERN.', 1: 'NAME.', 2: 'EXPLAIN.'})
C.fixed([k('7', 'd')], 'chem-4-3', 'test-for-chloride-ion-in-water')

# ── Q8 Propanal, propanone and their reaction scheme ─────────────────────────
Q8 = FIG + 'paper-q8'
Q8_STEM = C.context(k('8', 'a'))
assert Q8_STEM == 'Study the reaction scheme and answer the questions that follow.', Q8_STEM
# (a): the paper sets (i) and (ii) inside one sentence (page 5, y 634); the scheme
# prices (i) (5) and (ii) (3): a card each.
Q8A = P.ask(k('8', 'a'))
C.fixed([k('8', 'a', 'i')], 'chem-4-2', 'naming-alcohol-a', qtext=Q8A, stem=Q8_STEM, figure=Q8,
        row_notes={0: 'For (i).'})
C.fixed([k('8', 'a', 'ii')], 'chem-4-2', 'naming-ester-b', qtext=Q8A, stem=Q8_STEM, figure=Q8,
        row_notes={0: 'For (ii).'})
# (b): EXPLAIN (2 × 3), WHAT (2 × 3), IDENTIFY (6). The paper underlines "structural
# isomers" (page 5, y 650): its own print, with the reaction scheme, is the question.
C.fixed([k('8', 'b')], 'chem-4-2', 'structural-isomers-and-primary-and-secondary-alcohols', stem=Q8_STEM,
        row_notes={0: 'EXPLAIN.', 2: 'WHAT.', 4: 'IDENTIFY.'})
print_question('paper-q8b-print')
C.fixed([k('8', 'c')], 'chem-2-2', 'a-compound-whose-carbons-are-all-tetrahedral', stem=Q8_STEM, figure=Q8)
# (d): the conversions labelled R are drawn in the reaction scheme: the paper's own
# print (the scheme, then (d)) is the question. The ask names R; what R is, the
# reagent and catalyst that bring the conversions about, is the scheme's own answer.
_q8d = P.items(k('8', 'd'))
assert [(it.cell, display(it.text)) for it in _q8d] == [('[2 × 3]', 'reagent: hydrogen // catalyst: nickel / '
                                                                    'palladium / platinum')], _q8d
C.fixed([k('8', 'd')], 'chem-4-2', 'reducing-propanal-and-propanone', stem=Q8_STEM,
        label_key=[{'letter': 'R', 'meaning': display(_q8d[0].text), 'askedInThisQuestion': True}])
print_question('paper-q8d-print')
# (e): DESC "ANY THREE: (3 × 3)" over four points (scheme page 12, y 471-562); the
# first reads "Fehling's A (1) and Fehling's B (2)", the solutions' numbers, which the
# reader takes for cells: its own line is read here. WHY (3).
_q8e = P.items(k('8', 'e'))
assert [it.cell for it in _q8e] == ['[1]', '[2]', '[3 × 3]', '[3]'], _q8e
_mix = raw(12, 470, 487, 120)
assert _mix == 'mix (add) equal amounts of Fehling’s A (1) and Fehling’s B (2) in a test tube //', _mix
_desc8 = [_mix.rstrip('/ ')] + [display(x).strip() for x in _q8e[2].text.split('//')][1:]
assert len(_desc8) == 4 and _desc8[3].startswith('note any change'), _desc8
_three8 = raw(12, 546, 563, 440)
assert _three8 == 'ANY THREE: (3 × 3)', _three8
C.add([k('8', 'e')], 'chem-4-2', 'fehlings-test-on-propanal', [
    menu_row('r-1', _desc8, 3, 'DESC: any three of these, (3) each: "' + _three8 + '".', per=3, total=9),
    lift('r-2', _q8e[3].text, 3, 'WHY.')], total=12, stem=Q8_STEM, figure=Q8)
C.fixed([k('8', 'f')], 'chem-4-2', 'the-compound-with-a-fruity-odour', stem=Q8_STEM, figure=Q8)

# ── Q9 Rates: marble chips and acid, and cobalt(II) catalysis ────────────────
# (a): the paper prints (5) after "Define rate of reaction.", then the data, and (12),
# (6) and (9) after the three asks on its graph: a card each. The scheme draws the
# graph, the tangent at 60 s and the 1 M curve on a page of its own (PDF page 14),
# printed sideways: its own print is the answer for the three graph cards. Their
# questions need the paper's data table: its own print is the question.
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a] == ['[5]', '[4 × 3]', '[6]', '[2 × 3]', '[3]'], _q9a
Q9A = P.ask(k('9', 'a'))
Q9A_DEF, _r = cut(Q9A, 'The loss of mass')
Q9A_DATA, _r = cut(_r, 'Plot a graph')
Q9A_PLOT, _r = cut(_r, 'Use your graph')
Q9A_USE, Q9A_MARK = cut(_r, 'Mark clearly')
assert Q9A_DEF == 'Define rate of reaction.' and Q9A_DATA.endswith('the following data were recorded.'), Q9A
_rate = display(_q9a[0].text)
assert _rate == 'change in concentration per unit time / rate of change of concentration / change in concentration time', \
    _rate
C.add([k('9', 'a')], 'chem-3-2', 'rate-of-reaction', [
    lift('r-1', _rate.replace('change in concentration time', 'change in concentration ÷ time'), 5,
         FRACTION.format('"change in concentration"', '"time"'))],
    qtext=Q9A_DEF, stem='', cid='q9-a-define', ref_suffix='rate of reaction defined')
_plot = [display(x).strip() for x in _q9a[1].text.split('//')]
assert _plot[0].startswith('See graph below. axes correctly labelled') and len(_plot) == 4, _plot
_plot[0] = _plot[0][len('See graph below. '):]
_plot = [split_asides(x) for x in _plot]
C.add([k('9', 'a')], 'chem-3-2', 'plotting-loss-of-mass-against-time', [
    lift('r-1', _plot[0][0], 3, 'The scheme opens "See graph below." and prices these points (4 × 3), one each. It '
         'adds: ' + ' '.join(_plot[0][1])),
    lift('r-2', _plot[1][0], 3),
    lift('r-3', _plot[2][0], 3, 'The scheme adds: ' + ' '.join(_plot[2][1])),
    lift('r-4', _plot[3][0], 3, 'The scheme adds: ' + ' '.join(_q9a[1].asides))],
    qtext=Q9A_PLOT, stem=Q9A_DATA, figure=S + 'q9a', cid='q9-a-plot', ref_suffix='the graph plotted')
print_question('paper-q9a-plot-print')
C.add([k('9', 'a')], 'chem-3-2', 'instantaneous-rate-from-a-tangent', [
    lift('r-1', _q9a[2].text, 6, 'USE. The scheme adds: ' + ' '.join(_q9a[2].asides) + ' Its graph draws the tangent '
         'at 60 seconds and works the rate in a box, shown with the answer.')],
    qtext=Q9A_USE, stem=Q9A_DATA, figure=S + 'q9a', cid='q9-a-use', ref_suffix='rate at 60 seconds')
print_question('paper-q9a-use-print')
_mark = [display(x).strip() for x in _q9a[3].text.split('//')]
assert _mark[0] == 'See graph below. curve drawn with the following: rises to half the height' and len(_mark) == 2, _mark
_just = [display(x).strip() for x in _q9a[4].text.split('//')]
assert len(_just) == 3 and '[any one]' in _q9a[4].asides, _just
_one9 = raw(13, 408, 425, 440)
assert _one9 == 'ANY ONE: (3)', _one9
C.add([k('9', 'a')], 'chem-3-2', 'the-curve-for-half-the-acid-concentration', [
    lift('r-1', 'rises to half the height', 3, 'MARK: the scheme opens "See graph below. curve drawn with the '
         'following:" and prices these points (2 × 3), one each; its graph draws the 1 M curve, shown with the answer.'),
    lift('r-2', _mark[1], 3),
    menu_row('r-3', _just, 1, 'JUSTIFY: any one of these, (3): "' + _one9 + '". The scheme adds: '
             + ' '.join(a for a in _q9a[4].asides if not a.startswith('[any')), per=3, total=3)],
    total=9, qtext=Q9A_MARK, stem=Q9A_DATA, figure=S + 'q9a', cid='q9-a-mark', ref_suffix='the 1 M curve')
print_question('paper-q9a-mark-print')
# (b): TYPE (3), COLOURS (6), EXPLAIN (3 × 3), printed (3), (6) and (9): a card each.
Q9B = P.ask(k('9', 'b'))
Q9B_STEM, _r = cut(Q9B, 'What type of catalysis')
Q9B_TYPE, _r = cut(_r, 'What colour changes')
Q9B_COL, Q9B_SIG = cut(_r, 'Explain the significance')
_q9b = P.items(k('9', 'b'))
assert [it.cell for it in _q9b] == ['[3]', '[6]', '[3 × 3]'], _q9b
C.add([k('9', 'b')], 'chem-3-2', 'homogeneous-catalysis', [lift('r-1', _q9b[0].text, 3, 'TYPE.')],
      qtext=Q9B_TYPE, stem=Q9B_STEM, cid='q9-b-type', ref_suffix='type of catalysis')
C.add([k('9', 'b')], 'chem-3-2', 'colour-changes-with-cobalt-ii-catalyst', [lift('r-1', _q9b[1].text, 6, 'COLOURS.')],
      qtext=Q9B_COL, stem=Q9B_STEM, cid='q9-b-colours', ref_suffix='colour changes')
_sig = [display(x).strip() for x in _q9b[2].text.split('//')]
assert len(_sig) == 3, _sig
C.add([k('9', 'b')], 'chem-3-2', 'an-intermediate-in-homogeneous-catalysis', [
    lift('r-1', _sig[0], 3, 'EXPLAIN. The scheme prices these points (3 × 3), one each.'),
    lift('r-2', _sig[1], 3),
    lift('r-3', _sig[2], 3, 'The scheme adds: ' + ' '.join(_q9b[2].asides))],
    qtext=Q9B_SIG, stem=Q9B_STEM + ' ' + Q9B_COL, cid='q9-b-significance', ref_suffix='significance of the colours')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a)(i): two points priced (4 + 3); (ii): MECHANISM (4 × 3), the bromonium and
# carbonium ions drawn beside the third point (scheme page 15, x 421-534, crop
# 'scheme-q10a-ii', its labels read as its picture's), STATE (6).
C.ordered([k('10', 'a', 'i')], 'chem-4-2', 'why-alkenes-are-more-reactive-than-alkanes')
C.fixed([k('10', 'a', 'ii')], 'chem-4-2', 'mechanism-of-adding-bromine-to-ethene', figure=S + 'q10a-ii',
        row_notes={0: 'MECHANISM.', 2: 'The scheme draws the bridged (cyclic) bromonium ion and the carbonium ion '
                                       'beside this point, shown with the answer.', 4: 'STATE.'})
# (b): DEFINE and WHAT (4 + 3), printed (7); STATE and EXPLAIN (2 × 3), printed (6);
# CALC (i) (6) and (ii) (6), the paper setting (i) and (ii) inside one sentence,
# printed (12): a card each.
Q10B = P.ask(k('10', 'b'))
Q10B_DEF, _r = cut(Q10B, 'A certain water soluble')
Q10B_HIN, _r = cut(_r, 'State and explain')
Q10B_COL, Q10B_CALC = cut(_r, 'Calculate the pH')
assert Q10B_DEF == 'Define an acid in terms of the Brønsted-Lowry theory. What is a conjugate pair?' and \
    Q10B_HIN.endswith('dissociates as follows in water.') and Q10B_CALC.endswith('is 2.0 × 10⁻⁵.'), Q10B
_q10b = P.items(k('10', 'b'))
assert [it.cell for it in _q10b] == ['[4 + 3]', '[2 × 3]'], _q10b
_dw = [display(x) for x in _q10b[0].points()]
assert _dw == ['proton (hydrogen ion, H⁺) donor', 'acid and base that differ by a proton (hydrogen ion, H⁺)'], _dw
C.add([k('10', 'b')], 'chem-3-4', 'bronsted-lowry-acid-and-conjugate-pair', [
    lift('r-1', _dw[0], None, 'DEFINE. The scheme prices its two points (4 + 3).'),
    lift('r-2', _dw[1], None, 'WHAT.')],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'), qtext=Q10B_DEF, stem='',
    cid='q10-b-acid', ref_suffix='acid and conjugate pair')
_se = [display(x).strip() for x in _q10b[1].text.split('//')]
assert _se[0] == 'purple' and len(_se) == 2, _se
C.add([k('10', 'b')], 'chem-3-4', 'indicator-colour-in-sodium-hydroxide', [
    lift('r-1', 'purple', 3, 'STATE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _se[1].replace('(OH¯)', '(OH⁻)'), 3, 'EXPLAIN.')],
    qtext=Q10B_COL, stem=Q10B_HIN, figure=FIG + 'paper-q10b', cid='q10-b-colour', ref_suffix='colour in NaOH')
_b1 = [display(it.text) for it in P.items(k('10', 'b', 'i'))]
assert _b1 == ['pH =13.7', 'pOH = – log 0.5 = 0.3', '[H⁺] = 10⁻¹⁴÷ 0.5 = 2 × 10⁻¹⁴', 'pH = 14 – 0.3 = 13.7',
               'pH = – log 2 × 10⁻¹⁴ = 13.7'] and cells(k('10', 'b', 'i')) == ['[6]'] + ['[3]'] * 4, _b1
C.add([k('10', 'b', 'i')], 'chem-3-4', 'ph-of-0-5-m-sodium-hydroxide', [
    menu_row('r-1', [_b1[1], _b1[2]], 1, 'For (i). The scheme gives the answer, "pH =13.7", priced (6), then two routes '
             'side by side, two steps (3) each: one of these, (3).', per=3, total=3),
    menu_row('r-2', [_b1[3], _b1[4]], 1, 'And the pH by that same route, (3).', per=3, total=3)],
    total=6, qtext=Q10B_CALC, stem=Q10B_HIN, figure=S + 'q10b-i')
print_question('paper-q10b-calc-print')
_b2 = [display(it.text) for it in P.items(k('10', 'b', 'ii'))]
assert _b2 == ['pH =2.85', 'pH =– log√2.0 × 10⁻⁵× 0.1 [H⁺] = √2.0 × 10⁻⁵× 0.1', '= 2.85', 'pH = - log [H⁺] = 2.85'] \
    and cells(k('10', 'b', 'ii')) == ['[6]'] + ['[3]'] * 3, _b2
_root = [raw(15, 515, 533, 160, 330), raw(15, 515, 533, 330, 480)]
assert _root == ['pH =– log√2.0 × 10⁻⁵× 0.1 (3)', '[H⁺] = √2.0 × 10⁻⁵× 0.1 (3)'], _root
C.add([k('10', 'b', 'ii')], 'chem-3-4', 'ph-of-a-weak-acid-indicator', [
    menu_row('r-1', [x[:-len(' (3)')] for x in _root], 1, 'For (ii). The scheme gives the answer, "pH =2.85", priced (6), '
             'then two routes side by side, two steps (3) each, a root sign drawn over "2.0 × 10⁻⁵ × 0.1": one of '
             'these, (3).', per=3, total=3),
    menu_row('r-2', [_b2[2], _b2[3]], 1, 'And the pH by that same route, (3).', per=3, total=3)],
    total=6, qtext=Q10B_CALC, stem=Q10B_HIN, figure=S + 'q10b-ii')
print_question('paper-q10b-calc-print')
# (c): the equation (paper page 6, y 664) draws its arrow: the paper's crop is each
# card's figure. Each step the scheme prices (3) is a row; the answer is in a note.
Q10C = FIG + 'paper-q10c'
C.fixed([k('10', 'c', 'i')], 'chem-3-5', 'the-substance-oxidised-in-cleaning-silver', figure=Q10C)
_c2 = P.items(k('10', 'c', 'ii'))
assert [(it.cell, display(it.text)) for it in _c2] == [('[6]', '0.0003 mol sulfur'), ('[3]', '0.0096 ÷ 32 (3) = 0.0003')], _c2
C.add([k('10', 'c', 'ii')], 'chem-1-4', 'moles-of-sulfur-removed-from-the-bracelet', [
    lift('r-1', '0.0096 ÷ 32', 3, 'The scheme gives the answer, "0.0003 mol sulfur", priced (6), then two steps (3) '
         'each.'),
    lift('r-2', '= 0.0003', 3)], figure=Q10C)
_c3 = P.items(k('10', 'c', 'iii'))
assert [(it.cell, display(it.text)) for it in _c3] == [('[9]', '0.0054 g aluminium'), ('[3]', '0.0003 mol S ≡ 0.0003 '
                                                       'mol Ag₂S'), ('[3]', '≡0.0002 mol Al (3) = 0.0054 g Al')], _c3
C.add([k('10', 'c', 'iii')], 'chem-1-4', 'mass-of-aluminium-used-to-clean-the-bracelet', [
    lift('r-1', _c3[1].text, 3, 'The scheme gives the answer, "0.0054 g aluminium", priced (9), then three steps (3) '
         'each.'),
    lift('r-2', '≡0.0002 mol Al', 3),
    lift('r-3', '= 0.0054 g Al', 3)], figure=Q10C)
_c4 = P.items(k('10', 'c', 'iv'))
assert [(it.cell, display(it.text)) for it in _c4][:2] == [('[6]', '0.0744 g lost'), (
    '[3]', '0.0003 mol S ≡ 0.0003 mol Ag₂S (3) × 248* = 0.0744')], _c4
C.add([k('10', 'c', 'iv')], 'chem-1-4', 'mass-lost-by-polishing-off-the-silver-sulfide', [
    lift('r-1', '0.0003 mol S ≡ 0.0003 mol Ag₂S', 3, 'The scheme gives the answer, "0.0744 g lost", priced (6), then '
         'two steps (3) each.'),
    lift('r-2', '× 248* = 0.0744', 3, 'The scheme adds: "' + _slip + '"')], figure=Q10C)

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('11', 'a', 'i')], 'chem-1-2', 'what-an-alpha-particle-is')
C.fixed([k('11', 'a', 'ii')], 'chem-1-2', 'thomsons-plum-pudding-model', figure=S + 'q11a-ii',
        row_notes={0: 'The scheme draws the model beside its points, its labels "electron (negative charge)" and "+ '
                      'charge", shown with the answer.'})
C.fixed([k('11', 'a', 'iii')], 'chem-1-2', 'why-alpha-particles-were-deflected')
C.fixed([k('11', 'a', 'iv')], 'chem-1-2', 'why-few-alpha-particles-bounced-back', row_notes={0: 'SOME.', 1: 'SMALL.'})
C.fixed([k('11', 'a', 'v')], 'chem-1-2', 'rutherfords-nuclear-model-of-the-atom', figure=S + 'q11a-v',
        row_notes={0: 'DRAW. The scheme draws the atom beside this, its labels "electron (shell, cloud)" and "nucleus", '
                      'shown with the answer.'})
# (b): WRITE (6), printed (6); CALC (12), printed (12); STATE and EXPLAIN (4 + 3),
# printed (7): a card each. The scheme sets the expression and its working as
# fractions in a box (page 16, y 427-627), which the reader welds together: its own
# lines are read here. The equation (paper page 7, y 321) sets its equilibrium arrow
# in a glyph the text layer reads as U+0595: it is the paper's crop.
Q11B = P.ask(k('11', 'b'))
Q11B_STEM, _r = cut(Q11B, 'Write the equilibrium')
Q11B_WRITE, _r = cut(_r, 'Calculate the value')
Q11B_CALC, Q11B_STATE = cut(_r, 'State and explain')
Q11B_STEM = P.rearranged(P.rearranged(Q11B_STEM, '(I ⁻)', '(I⁻)'), '(I₃ –)', '(I₃⁻)')
assert Q11B_STEM.endswith('0.0793 moles of triiodide ions (I₃⁻) were present at equilibrium.') and \
    Q11B_WRITE == 'Write the equilibrium constant (Kc) expression for this equilibrium reaction.', (Q11B_STEM, Q11B_WRITE)
_q11b = P.items(k('11', 'b'))
assert [it.cell for it in _q11b] == ['[6]', '[12]', '[3]', '[3]', '[3]', '[4 + 3]'] and \
    display(_q11b[0].text) == '[I₃ –] [I₂][I⁻]' and display(_q11b[1].text) == '704.95 / 705 M⁻¹', _q11b
C.add([k('11', 'b')], 'chem-3-3', 'kc-expression-for-triiodide', [
    lift('r-1', '[I₃⁻] ÷ [I₂][I⁻]', 6, FRACTION.format('[I₃⁻]', '[I₂][I⁻]'))],
    qtext=Q11B_WRITE, stem=Q11B_STEM, figure=S + 'q11b-write', cid='q11-b-expression', ref_suffix='Kc expression')
print_question('paper-q11b-write-print')
_equil = raw(16, 563, 581, 160)
_frac = [raw(16, 599, 616, 160, 210), raw(16, 611, 628, 160, 260), raw(16, 603, 621, 270)]
assert _equil == 'Equil 0.0007 M (3) 0.1607 M (3) 0.0793 M' and _frac == ['0.0793', '0.0007 × 0.1607',
                                                                         '(3) = 704.95 / 705 (3)'], (_equil, _frac)
C.add([k('11', 'b')], 'chem-3-3', 'calculating-kc-for-triiodide', [
    lift('r-1', '0.0007 M', 3, 'The scheme gives the answer, "704.95 / 705 M⁻¹", priced (12), then sets out a table, '
         'its row "' + _equil + '": the equilibrium value under I₂, (3).'),
    lift('r-2', '0.1607 M', 3, 'The equilibrium value under I⁻, (3).'),
    lift('r-3', '0.0793 ÷ 0.0007 × 0.1607', 3, FRACTION.format('0.0793', '0.0007 × 0.1607')),
    lift('r-4', '= 704.95 / 705', 3)],
    qtext=Q11B_CALC, stem=Q11B_WRITE, figure=S + 'q11b-calc', cid='q11-b-calculation', ref_suffix='Kc calculated')
print_question('paper-q11b-calc-print')
_state = [raw(16, 647, 664, 130), raw(16, 671, 688, 130, 500)]
assert _state == ['concentration of triiodide ions decreases', 'reaction shifts backward (reverse, to the left) to '
                  'restore (increase) iodine conc.'] and _q11b[5].asides == ['[Linked responses]'], _state
C.add([k('11', 'b')], 'chem-3-3', 'removing-iodine-from-the-triiodide-equilibrium', [
    lift('r-1', _state[0], None, 'STATE. The scheme prices its two points (4 + 3).'),
    lift('r-2', _state[1], None, 'EXPLAIN. The scheme adds: [Linked responses]')],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'), qtext=Q11B_STATE,
    stem=Q11B_STEM, figure=FIG + 'paper-q11b', cid='q11-b-starch', ref_suffix='adding starch')
# (c)A: alumina and aluminium.
_four11 = raw(17, 203, 221, 470)
assert _four11 == 'ANY FOUR: (4 × 3)', _four11
C.menu([ka('11', 'c', 'i', 'A')], 'chem-u3', 'producing-alumina-from-bauxite', note='"' + _four11 + '".')
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-3-5', 'the-cell-for-extracting-aluminium', figure=S + 'q11c-a-ii',
        row_notes={0: 'The scheme draws the cell beside these points, its labels "graphite anodes", "graphite '
                      'cathode" and "molten alumina and cryolite", shown with the answer.'})
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-u3', 'why-recycle-aluminium')
# (c)B: nitrogen.
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-u3', 'uses-of-nitrogen')
_two11 = raw(17, 516, 533, 470)
assert _two11 == 'ANY TWO: (2 × 3)', _two11
C.menu([ka('11', 'c', 'ii', 'B')], 'chem-2-1', 'why-nitrogen-is-unreactive', note='"' + _two11 + '".')
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-4-3', 'nitrogen-fixation')
_three11 = raw(17, 673, 690, 465)
assert _three11 == 'ANY THREE: (3 × 3)', _three11
C.menu([ka('11', 'c', 'iv', 'B')], 'chem-4-3', 'fixing-nitrogen-by-lightning', note='"' + _three11 + '".')


# A charge the scheme sets as a macron ("Cl¯", "MnO₄¯") is shown as the minus it
# prints; a script run the text layer sets apart from the bracket that closes it
# ("(not hygroscopic )") stays as the page sets it. The gate reads both alike.
def _charge(t):
    t2 = re.sub(r'(?<=[A-Za-z₀-₉)\]])¯', '⁻', t)
    if t2 != t and not P.traceable(t2):
        raise Refused(f'"{t2}" is not in the 2012 hl scheme')
    return t2


for _c in C.cards:
    for _r in _c['rows']:
        if not _r.get('ask'):
            _r['verbatim'] = _charge(_r['verbatim'])
        if _r.get('contextNote'):
            _r['contextNote'] = re.sub(r'(?<=[A-Za-z₀-₉)\]])¯', '⁻', _r['contextNote'])
        if _r.get('group'):
            _r['group']['options'] = [_charge(o) for o in _r['group']['options']]
            _r['verbatim'] = _r['group']['options'][0]

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
    # Q6(b)'s mark "(12)" prints at the end of the text column (paper page 5, x 230,
    # y 165), the equations taking the column right of it; the reader takes marks at
    # x > 250 only, and reads it as words of (b) (Q6B_LEAD, asserted above).
    assert ('6', 'b') not in out
    out[('6', 'b')] = 12
    # Q11(a)(v)'s mark "(3)" prints in one run with its words ("... proposed by
    # Rutherford. (3)", paper page 7, x 94-527, y 241): the reader takes it off the
    # ask as the letter's last mark, not as a mark after a run of text.
    v = P.pseg_of(k('11', 'a', 'v'))
    assert not v.marks_at and P.marks[('11', 'a', None, None)] == 3, (v.marks_at, P.marks)
    out[('11', 'a')] += 3
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
