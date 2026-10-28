#!/usr/bin/env python3
"""2015 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2015_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2015_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2015_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2015 hl

No 2015 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

The 2015 scheme is the labelled ("cue") layout. The census and the paper agree
on the paper's 85 asks; no reader change was needed. The paper sets one run of
romans inside one sentence, Q4(a) ("How many (i) electrons, (ii) neutrons, has
the aluminium ion", paper page 5, y 137), which the census keeps as one ask and
the scheme prices under markers of its own with one cell (2 x 3): one card,
Q4(a). It sets two runs of romans on lines of their own that the scheme prices
with ONE cell each, Q4(g)(i)-(ii) and Q4(h)(i)-(ii) ("(2 x 3)", scheme page 7,
y 610 and page 8, y 61), and Q9(a)(i)-(ii) (page 13, y 74): one card each,
cited over both romans. Q10(a)(i) and (ii) the paper sets on lines of their own
inside one sentence ("Explain whether or not the Kekule structure correctly
describes (i) the number, (ii) the distribution, of the pi-electrons in
benzene.", paper page 9, y 162-209) and the scheme prices with a cell each: a
card each, showing the sentence.

Asks the paper sets unnumbered are the letter's own card before its first roman
(Q3(e), Q5(c), Q10(a)) or a card after the roman they follow, cited "— after
(ii), ..." (Q10(a)). Where one letter's asks would outrun a card's five rows,
each ask (or each run of asks under one printed mark) is a card cited with what
it holds (Q2(b), Q7(e), Q10(a), Q11(a), Q11(b)). Q4(k) and Q11(c) offer
alternative parts A and B. The paper underlines the term Q11(c)A(i) asks about,
which no text layer carries: that card takes the paper's own print as its
question, as do the parts whose figure is the scheme's and whose ask needs the
paper's table, structure or equation (Q3(b), Q4(g), Q9(c), Q9(d)(i), Q11(b)).
"""
import json
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, point, read_lines, tidy  # noqa: E402

P = Printed(2015, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2015-HL-'
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


def cut(text, at):
    """`text` split where `at` begins (the paper's print, cut between two asks
    it sets in one run)."""
    i = text.index(at)
    return text[:i].strip(), text[i:].strip()


def table_rows(page, rect, cols):
    """The rows of a table the scheme prints as its answer, read between the
    table's own rules: each row is the text of each column (x0, x1) in it.
    Empty rows are not rows. (2015 HL: a cell's first line starts up to half a
    point above the rule over it, Q3(d), scheme page 6, rules at y 415.3 and
    428.4, "Comparator" and "add reagent" at y 414.9 and 427.8.)"""
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
        row = [l for l in _RAW if l.page == page and top - 1 <= l.y0 and l.y1 <= bot + 1]
        texts = tuple(tidy(' '.join(display(l.text) for l in row if a <= l.x0 < b)) for a, b in cols)
        if any(texts):
            out.append(texts)
    return out


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 Standardising sodium thiosulfate against iodine ───────────────────────
# The question's equation sets each charge on a line of its own ("2S₂O₃" then
# "2–", paper page 2, y 153-169), which the text layer reads after its formula;
# every Q1 stem shows it as the page prints it.
_Q1_EQ = 'I₂ + 2S₂O₃ 2– → 2I⁻ + S₄O₆ 2–'
assert _Q1_EQ in P.ask(k('1')), P.ask(k('1'))


def q1(key):
    t = C.context(key)
    assert _Q1_EQ in t, t
    return P.rearranged(P.rearranged(t, 'S₂O₃ 2–', 'S₂O₃²⁻'), 'S₄O₆ 2–', 'S₄O₆²⁻')


# (a): one answer (6); the scheme sets the triiodide ion's charge as a line of its own.
_q1a = P.items(k('1', 'a'))
assert [it.cell for it in _q1a] == ['[6]'] and display(_q1a[0].text).count('I₃ –') == 2, _q1a
C.fixed([k('1', 'a')], 'chem-4-1', 'iodine-dissolved-as-triiodide', stem=q1(k('1', 'a')),
        fixes={display(_q1a[0].text): display(_q1a[0].text).replace('I₃ –', 'I₃⁻')})
# (b): any three of six (6 + 3 + 3).
C.menu([k('1', 'b')], 'chem-4-1', 'measuring-a-portion-with-a-pipette', stem=q1(k('1', 'b')),
       note='"' + raw(4, 200, 216, 400) + '".')
C.fixed([k('1', 'c')], 'chem-4-1', 'starch-indicator-for-iodine-and-thiosulfate', stem=q1(k('1', 'c')),
        row_notes={0: 'NAME.', 1: 'AT WHAT.', 2: 'STATE.'})
# (d)(i): the answer (6), then three boxed routes of two steps (3) each, set as
# fractions side by side: the answer line, with the scheme's print of the routes.
_q1d1 = P.items(k('1', 'd', 'i'))
assert _q1d1[0].cell == '[6]' and _q1d1[-1].asides == ['[*Addition must be shown for error to be treated as slip.]'], _q1d1
C.answer_only([k('1', 'd', 'i')], 'chem-4-1', 'moles-of-iodine-in-a-portion', S + 'q1d-i', stem=q1(k('1', 'd', 'i')),
              notes='The scheme sets out three boxed routes, each two steps priced (3), and adds: '
                    + _q1d1[-1].asides[0])
shown('The scheme prices each of its three routes in two steps, (3) each, and adds: ' + _q1d1[-1].asides[0])
C.route([k('1', 'd', 'ii')], 'chem-4-1', 'moles-of-thiosulfate-to-reduce-the-iodine', stem=q1(k('1', 'd', 'ii')))
_q1d3 = P.items(k('1', 'd', 'iii'))
assert _q1d3[0].cell == '[6]' and display(_q1d3[0].text) == '0.14 M', _q1d3
C.answer_only([k('1', 'd', 'iii')], 'chem-4-1', 'molarity-of-the-thiosulfate-solution', S + 'q1d-iii',
              stem=q1(k('1', 'd', 'iii')),
              notes='The scheme sets out two boxed routes, each two steps priced (3), the second after "/".')
shown('The scheme prices each of its two routes in two steps, (3) each.')
# (d)(iv): the answer (3); the working in a box under it, unpriced.
_q1d4 = P.items(k('1', 'd', 'iv'))
assert [it.cell for it in _q1d4] == ['[3]', None] and len(_q1d4[1].asides) == 2, _q1d4
assert display(_q1d4[1].text) == '0.140 × 248** = 34.72 = 35 g / L [34.7 – 35 g / L]', _q1d4
C.add([k('1', 'd', 'iv')], 'chem-4-1', 'thiosulfate-concentration-in-grams-per-litre-of-crystals', [
    lift('r-1', _q1d4[0].text, 3, 'The scheme works it as "' + display(_q1d4[1].text) + '" and adds: '
         + ' '.join(_q1d4[1].asides))], stem=q1(k('1', 'd', 'iv')))
C.fixed([k('1', 'e')], 'chem-4-1', 'distilled-rather-than-deionised-water', stem=q1(k('1', 'e')))

# ── Q2 Oxidising phenylmethanol to benzoic acid ──────────────────────────────
Q2 = FIG + 'paper-q2'
C.fixed([k('2', 'a')], 'chem-4-2', 'appearance-of-phenylmethanol', figure=Q2)
# (b): four asks under (24), each priced (2 x 3), one point each. Eight rows
# outrun a card: each ask is a card, cited with what it holds.
_q2b = P.items(k('2', 'b'))
assert [it.cell for it in _q2b] == ['[2 × 3]'] * 4, _q2b
Q2B = P.ask(k('2', 'b'))
Q2B_STATE, _r = cut(Q2B, 'Identify A and B')
Q2B_ID, _r = cut(_r, 'What changes were observed')
Q2B_WHAT, Q2B_OX = cut(_r, 'State the changes in the oxidation')
assert Q2B_STATE.endswith('sodium carbonate had been added.') and Q2B_OX.endswith('during the experiment.'), Q2B
Q2_LEAD = C.context(k('2', 'b'))
_pts = [it.points() for it in _q2b]
assert [len(p) for p in _pts] == [2] * 4, _pts
_b = [[display(p) for p in pts] for pts in _pts]
assert _b[1] == ['A = HCl / hydrochloric acid', 'B = Na₂SO₃ / sodium sulfite'], _b[1]
assert _b[3] == ['7 / +7 / VII / Mn⁷⁺ to 4 / +4 / IV/ Mn⁴⁺', '4 / +4 / IV / Mn⁴⁺ to 2 / +2 / II / Mn²⁺'], _b[3]
for i, (ask, cue, cid, sfx, concept, stem) in enumerate([
        (Q2B_STATE, 'STATE', 'q2-b-colour-change', 'colour change', 'manganate-vii-oxidising-phenylmethanol', Q2_LEAD),
        (Q2B_ID, 'IDENTIFY', 'q2-b-a-and-b', 'A and B', 'separating-benzoic-acid-after-the-oxidation', Q2_LEAD),
        (Q2B_WHAT, 'WHAT', 'q2-b-changes-observed', 'changes observed', 'adding-acid-and-sulfite-then-cooling',
         tidy(Q2_LEAD + ' ' + Q2B_ID)),
        (Q2B_OX, 'STATE', 'q2-b-oxidation-numbers', 'oxidation numbers', 'oxidation-numbers-of-manganese',
         Q2_LEAD)]):
    _asides = ' '.join(_q2b[i].asides)
    C.add([k('2', 'b')], 'chem-4-2', concept, [
        lift('r-1', _b[i][0], 3, cue + '. The scheme prices these points (2 × 3), one each.'
             + (' It adds: ' + _asides if _asides else '')),
        lift('r-2', _b[i][1], 3)], qtext=ask, stem=stem, figure=Q2, cid=cid, ref_suffix=sfx)
C.fixed([k('2', 'c')], 'chem-u2', 'recrystallising-benzoic-acid', figure=Q2, row_notes={0: 'STATE.', 1: 'HOW.'})
# (d): the answer (12); two routes side by side, four steps (3) each, sharing
# their first two. Steps set as fractions are given in the form the gate finds.
_q2d = P.items(k('2', 'd'))
assert _q2d[0].cell == '[12]' and display(_q2d[0].text) == '58% [57.69 – 58%]' and len(_q2d[-1].asides) == 3, _q2d
C.add([k('2', 'd')], 'chem-1-4', 'percentage-yield-of-benzoic-acid', [
    lift('r-1', '2.7 × 1.04 = 2.808 g', 3, 'The scheme sets two routes side by side; both open with these two '
         'steps.'),
    lift('r-2', '2.808 ÷ 108∗ = 0.026 moles', 3, FRACTION.format('2.808', '108∗')),
    menu_row('r-3', ['0.026 × 122** = 3.172 g', '1.83 ÷ 122∗∗ = 0.015 moles'], 1,
             'The third step of the route used, (3): the theoretical mass of benzoic acid, or (the second route) '
             'the moles of benzoic acid obtained. ' + FRACTION.format('1.83', '122∗∗'), per=3, total=3),
    menu_row('r-4', ['1.83 ÷ 3.172 × 100 = 58% [57.69 – 58%]', '0.015 ÷ 0.026 × 100 = 58% [57.69 – 58%]'], 1,
             'And the last step of that same route, (3). The scheme prints 1.83 over 3.172, and 0.015 over 0.026, '
             'as fractions; ÷ stands for each bar. It adds: ' + ' '.join(_q2d[-1].asides), per=3, total=3)],
    total=12, figure=S + 'q2d',
    notes='The scheme gives the answer, 58% [57.69 – 58%], priced (12), then two routes of four steps (3) each.')
shown('The scheme gives the answer as "58% [57.69 – 58%]" (12); its own print of both routes is shown with the '
      'answer.')
# Its only figure is the scheme's working, held back until the reveal, while its stem points at
# "the reaction scheme below", whose structures give the two molar masses the yield is worked
# from: the paper's own print (the lead-in and the reaction scheme, then (d)) is the question.
print_question('paper-q2d-print')

# ── Q3 Swimming-pool water ───────────────────────────────────────────────────
Q3T = FIG + 'paper-q3-table'
C.menu([k('3', 'a')], 'chem-4-3', 'measuring-suspended-solids', figure=Q3T,
       note='"' + raw(6, 124, 140, 400) + '".')
# (b): the answer (6); two boxed routes of two steps (3) each, side by side.
# The ask needs the table's figure for pool B: the paper's own print is the question.
_q3b = P.items(k('3', 'b'))
assert [it.cell for it in _q3b] == ['[6]'] + ['[3]'] * 4 and display(_q3b[0].text) == '0.35 g / 250 cm³', _q3b
assert display(_q3b[3].text) == '1.4 ÷ 4 = 0.35 g / 250 cm³ /' and _q3b[4].asides == [
    '[1 mark to be deducted for incorrect rounding off.]'], _q3b
C.add([k('3', 'b')], 'chem-4-3', 'dissolved-solids-in-a-volume-of-pool-water', [
    menu_row('r-1', [_q3b[1].text, _q3b[2].text], 1, 'The first step of either route, the second after "/", (3).',
             per=3, total=3),
    menu_row('r-2', ['1.4 ÷ 4 = 0.35 g / 250 cm³', _q3b[4].text], 1, 'And the second step of that same route, (3). '
             'The scheme adds: ' + _q3b[4].asides[0], per=3, total=3)],
    total=6, figure=S + 'q3b',
    notes='The scheme gives the answer, 0.35 g / 250 cm³, priced (6), then two boxed routes of two steps (3) each.')
shown('The scheme gives the answer as "0.35 g / 250 cm³" (6).')
print_question('paper-q3b-print')
# (c): WHAT (6); SUGGEST (3), four worded answers or, after "/", the equation
# with "boiling" set over its arrows (scheme page 6, y 306-332), or either half.
_q3c = P.items(k('3', 'c'))
assert [it.cell for it in _q3c] == ['[6]', '[3]', None], _q3c
_sug = display(_q3c[1].text)
_eq = 'boiling boiling Ca(HCO₃)_(2 ()aq) → / → CaCO₃↓ + H₂O + CO₂'
assert _sug.endswith('by boiling / ' + _eq), _sug
_half = display(_q3c[2].text)
assert _half == '[Half equations above with Mg(HCO₃)₂ or HCO₃ – acceptable in place of Ca(HCO₃)₂.]', _half
C.add([k('3', 'c')], 'chem-4-3', 'edta-and-hardness-removed-by-boiling', [
    lift('r-1', _q3c[0].text, 6, 'WHAT.'),
    lift('r-2', _sug[:-len(' / ' + _eq)].replace('(CO₃ 2–)', '(CO₃²⁻)').replace('(HCO₃ – )', '(HCO₃⁻)'), 3,
         'SUGGEST. The scheme also accepts, after "/", the equation for calcium hydrogencarbonate breaking down on '
         'boiling, "boiling" set over its arrow, or either half of it; its own print is shown with the answer. It '
         'adds: ' + _half.replace('HCO₃ –', 'HCO₃⁻'))],
    figure=S + 'q3c')
# (d): IDENTIFY (6); DESCRIBE, any three steps of the one method used (3 x 3),
# read from the scheme's table, comparator and colorimeter side by side.
_q3d = P.items(k('3', 'd'))
assert _q3d[0].cell == '[6]', _q3d
_t = table_rows(6, (132, 410, 548, 597), [(138, 308), (336, 520)])
assert _t[0] == ('Comparator', 'Colorimeter') and len(_t) == 5, _t
_comp, _col = [r[0] for r in _t[1:]], [r[1] for r in _t[1:]]
_any3 = raw(6, 596, 612, 440)
_incor = raw(6, 596, 612, 130, 440)
assert _any3 == 'ANY THREE: (3 × 3)' and _incor == '[Marks available for description where method incorrectly named.]'
C.add([k('3', 'd')], 'chem-4-3', 'estimating-free-chlorine-with-a-comparator-or-colorimeter', [
    lift('r-1', _q3d[0].text, 6, 'IDENTIFY.'),
    menu_row('r-2', _comp + _col, 3, 'Claim three steps of one method, the comparator\'s or the colorimeter\'s, '
             'not a mix of the two. DESCRIBE: any three steps of the one method used, (3) each: "' + _any3
             + '". The scheme sets the comparator\'s four steps (the first four here) beside the colorimeter\'s '
             '(the last four) in a table, shown with the answer. It adds: ' + _incor, per=3, total=9)],
    total=15, figure=S + 'q3d')
# (e): WHICH (2), the letter's own ask before (i); then (i) and (ii), (3) each.
Q3E_WHICH, Q3E_WHAT = cut(P.ask(k('3', 'e')), 'What problem')
assert Q3E_WHAT == 'What problem might arise for swimmers', Q3E_WHAT
_q3e = P.items(k('3', 'e'))
assert [(it.cell, it.text) for it in _q3e] == [('[2]', 'free chlorine')], _q3e
C.add([k('3', 'e')], 'chem-4-3', 'free-chlorine-making-pools-unsuitable', [lift('r-1', 'free chlorine', 2, 'WHICH.')],
      qtext=Q3E_WHICH, figure=Q3T)
for r, concept in (('i', 'too-little-free-chlorine'), ('ii', 'too-much-free-chlorine')):
    C.fixed([k('3', 'e', r)], 'chem-4-3', concept, figure=Q3T, stem=P.ask(k('3')),
            qtext=Q3E_WHAT + f' ({r}) ' + P.ask(k('3', 'e', r)))

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
# (a): the paper sets (i) and (ii) inside one sentence, with the ion's mass and
# atomic numbers stacked before its symbol (page 5, y 135-158); the scheme
# prices them with one cell (2 x 3) under markers of its own.
C.fixed([k('4', 'a')], 'chem-1-2', 'electrons-and-neutrons-in-an-aluminium-ion', deep=True,
        row_notes={0: 'For (i).', 1: 'For (ii).'}, notes=Q4_NOTE,
        qtext=P.rearranged(P.ask(k('4', 'a')), 'Al³⁺? 27 13', '²⁷₁₃Al³⁺?'))
C.fixed([k('4', 'b')], 'chem-1-2', 'why-relative-atomic-masses-are-not-whole-numbers', notes=Q4_NOTE)
# (c): two points (2 x 3); the first offers, after "/", a nuclear equation set
# in an equation font the text layer cannot read (page 7, y 205-221).
_q4c = P.items(k('4', 'c'))
assert [it.cell for it in _q4c] == ['[2 × 3]'] and len(_q4c[0].asides) == 3, _q4c
_n = raw(7, 204, 220, 130, 335)
assert _n.startswith('a neutron changes into a proton / '), _n      # then the equation's glyphs
_n = _n[:_n.index(' / ')]
_e = raw(7, 214, 234, 130, 302)
assert _e == 'and an electron (+ e⁻) that is emitted', _e
C.add([k('4', 'c')], 'chem-1-2', 'the-nuclear-change-in-beta-decay', [
    lift('r-1', _n, 3, 'The scheme prices these points (2 × 3), one each. It also accepts, after "/", '
         'the nuclear equation of a neutron becoming a proton; its own print is shown with the answer.'),
    lift('r-2', _e, 3, 'The scheme adds: ' + ' '.join(_q4c[0].asides))], notes=Q4_NOTE, figure=S + 'q4c')
# (d): three wordings, each after "or", each two points (2 x 3).
_q4d = P.items(k('4', 'd'))
assert [it.cell for it in _q4d] == ['[2 × 3]'] and _q4d[0].asides == ['[Marks available for good diagrams.]'], _q4d
_w = [(raw(7, 280, 296, 130), raw(7, 293, 322, 130)), (raw(7, 331, 347, 130), raw(7, 344, 360, 130)),
      (raw(7, 369, 385, 130), raw(7, 382, 398, 130))]
assert all(a.endswith(' //') for a, _b in _w) and [b[:8] for _a, b in _w] == ['nitrogen', 'nitrogen', 'but ammo'], _w
assert [raw(7, y - 1, y + 16) for y in (319, 357)] == ['or', 'or']
C.add([k('4', 'd')], 'chem-2-2', 'shapes-of-boron-trifluoride-and-ammonia', [
    menu_row('r-1', [a[:-len(' //')] for a, _b in _w], 1, 'One of these wordings, the scheme setting each after '
             '"or"; it prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [b for _a, b in _w], 1, 'And the second point of that same wording, (3). The scheme adds: '
             + _q4d[0].asides[0], per=3, total=3)], total=6, notes=Q4_NOTE)
# (e): the answer (6); its working, two steps (3) each, set as fractions.
_q4e = P.items(k('4', 'e'))
assert [it.cell for it in _q4e] == ['[6]', '[3]', '[3]'] and display(_q4e[0].text) == 'Cu₃N', _q4e
C.answer_only([k('4', 'e')], 'chem-1-4', 'empirical-formula-of-copper-nitride', S + 'q4e',
              notes=Q4_NOTE + ' The scheme works it in two steps, (3) each: the moles of copper and of nitrogen as '
                              'fractions, their ratio 3 : 1, then the formula.')
shown('The scheme works it in two steps, (3) each: the moles of copper and of nitrogen, set as fractions, and '
      'their ratio, then the formula.')
C.fixed([k('4', 'f')], 'chem-2-3', 'avogadros-law', notes=Q4_NOTE)
# (g)(i)-(ii): one cell (2 x 3) prices the circle and the rectangle, which the
# scheme draws on the structure (page 7, y 616-740) and names "carboxylic acid"
# and "carbonyl". The structure is the paper's: its own print is the question.
_q4g = [P.items(k('4', 'g', r)) for r in ('i', 'ii')]
assert [[(it.cell, it.text) for it in its] for its in _q4g] == [
    [(None, 'carboxylic acid //')], [('[2 × 3]', 'carbonyl')]], _q4g
C.add([k('4', 'g', 'i'), k('4', 'g', 'ii')], 'chem-4-2', 'carboxylic-acid-and-ester-groups-in-aspirin', [
    C.mark_ask(point('r-1', P.ask(k('4', 'g', 'i')), 3, 'For (i): "CIRCLE: carboxylic acid". The scheme prices these '
                     'points (2 × 3), one each, and draws the circle and the rectangle on the structure; its own '
                     'print is shown with the answer.')),
    C.mark_ask(point('r-2', P.ask(k('4', 'g', 'ii')), 3, 'For (ii): "RECTANGLE: carbonyl". The scheme adds: '
                     + _q4g[1][0].asides[0]))], figure=S + 'q4g', notes=Q4_NOTE)
print_question('paper-q4g-print')
# (h)(i)-(ii): one cell (2 x 3), one each.
_q4h = [P.items(k('4', 'h', r)) for r in ('i', 'ii')]
assert [[(it.cell, it.text) for it in its] for its in _q4h] == [
    [(None, 'sodium (Na) //')], [('[2 × 3]', 'beryllium (Be)')]], _q4h
C.add([k('4', 'h', 'i'), k('4', 'h', 'ii')], 'chem-1-3', 'sodium-and-beryllium-beside-magnesium', [
    lift('r-1', 'sodium (Na)', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'beryllium (Be)', 3, 'For (ii).')], notes=Q4_NOTE)
# (i): two points (2 x 3) or, after "or", one answer (6): two rows, each its
# point or that answer, which the student claims twice.
_q4i = P.items(k('4', 'i'))
assert [it.cell for it in _q4i] == ['[2 × 3]', '[6]'] and raw(8, 111, 127) == 'or', _q4i
_pts = _q4i[0].points()
assert _pts == ['reduce (remove, lower) nitrates [nitrate identified by name (formula)]',
                'reduce (remove, lower) phosphates [phosphate identified by name (formula)]'], _pts
_bloom = _q4i[1].text
C.add([k('4', 'i')], 'chem-4-3', 'purpose-of-tertiary-sewage-treatment', [
    menu_row('r-1', ['reduce (remove, lower) nitrates', _bloom], 1, 'The first point, (3), or after "or" the answer '
             'the scheme prices (6) on its own: claim it here and again below. Beside the first point the scheme '
             'adds: [nitrate identified by name (formula)]', per=3, total=3),
    menu_row('r-2', ['reduce (remove, lower) phosphates', _bloom], 1, 'The second point, (3), or that answer again. '
             'The scheme adds: [phosphate identified by name (formula)]', per=3, total=3)], total=6, notes=Q4_NOTE)
# (j): the answer (6); three boxed routes of two steps (3) each, set in an
# equation font the text layer cannot read.
_q4j = P.items(k('4', 'j'))
assert _q4j[0].cell == '[6]' and _q4j[-1].asides[-1] == (
    '[1 mark deducted if the answer is not correct to one significant figure.]'), _q4j
C.answer_only([k('4', 'j')], 'chem-2-3', 'moles-of-gas-in-a-tennis-ball', S + 'q4j',
              notes=Q4_NOTE + ' The scheme sets out three boxed routes, each two steps priced (3): the ideal gas '
                              'equation, and two that correct the volume to standard or room conditions first.')
shown('The scheme prices each of its three routes in two steps, (3) each, and adds: ' + _q4j[-1].asides[-1])
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'nitrogen-fixation-in-nature', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-4-2', 'stages-in-recycling-polystyrene', notes=Q4_NOTE)

# ── Q5 Subatomic particles and energy levels ─────────────────────────────────
Q5A = FIG + 'paper-q5a'
C.fixed([k('5', 'a', 'i')], 'chem-1-2', 'detecting-cathode-rays', figure=Q5A)
C.fixed([k('5', 'a', 'ii')], 'chem-1-2', 'thomson-and-the-electron', figure=Q5A, row_notes={0: 'NAME.', 1: 'WHAT.'})
C.fixed([k('5', 'b')], 'chem-1-2', 'the-1903-nobel-prize-for-radioactivity')
# (c): STATE, three points (3 x 3), the letter's own ask before (i); then the
# paper sets (i) and (ii) on lines of their own inside one sentence, (3) each.
Q5C_LEAD, _r = cut(P.ask(k('5', 'c')), 'State three observations')
Q5C_STATE, Q5C_HOW = cut(_r, 'Explain how Rutherford')
assert Q5C_LEAD.endswith('positive nucleus.') and Q5C_HOW.endswith('that the nucleus is'), (Q5C_LEAD, Q5C_HOW)
Q5C_SENT = Q5C_HOW + ' (i) ' + P.ask(k('5', 'c', 'i')) + ' (ii) ' + P.ask(k('5', 'c', 'ii'))
assert Q5C_SENT.endswith('(i) positive, (ii) small and dense.'), Q5C_SENT
_q5c = P.items(k('5', 'c'))
assert [it.cell for it in _q5c] == ['[3 × 3]'] and len(_q5c[0].options()) == 3, _q5c
C.fixed([k('5', 'c')], 'chem-1-2', 'observations-of-the-gold-foil-experiment', qtext=Q5C_STATE, stem=Q5C_LEAD)
_q5c2 = P.items(k('5', 'c', 'ii'))
assert [it.cell for it in _q5c2] == ['[3]'] and len(_q5c2[0].asides) == 1, _q5c2
C.fixed([k('5', 'c', 'i')], 'chem-1-2', 'why-the-nucleus-is-positive', qtext=Q5C_SENT,
        stem=tidy(Q5C_LEAD + ' ' + Q5C_STATE), row_notes={0: 'For (i).'})
shown('Under (ii) the scheme adds: ' + _q5c2[0].asides[0])
C.fixed([k('5', 'c', 'ii')], 'chem-1-2', 'why-the-nucleus-is-small-and-dense', qtext=Q5C_SENT,
        stem=tidy(Q5C_LEAD + ' ' + Q5C_STATE), row_notes={0: 'For (ii).'})
# (d): any three of four points (3 x 3), then the last point (3).
_q5d = P.items(k('5', 'd'))
assert [it.cell for it in _q5d] == ['[3 × 3]', '[3]'] and _q5d[0].asides == ['[any three]'], _q5d
_any3 = raw(9, 488, 505, 440)
assert _any3 == 'ANY THREE: (3 × 3)', _any3
C.add([k('5', 'd')], 'chem-1-2', 'how-the-hydrogen-line-spectrum-arises', [
    menu_row('r-1', _q5d[0].options(), 3, 'Any three of these, (3) each: "' + _any3 + '".', per=3, total=9),
    lift('r-2', _q5d[1].text, 3, 'The scheme adds: ' + ' '.join(_q5d[1].asides))], total=12)
C.fixed([k('5', 'e')], 'chem-1-2', 'an-element-for-a-blue-green-firework')
C.fixed([k('5', 'f')], 'chem-1-2', 'calcium-configuration-and-2s-against-3s', row_notes={0: 'WRITE.', 1: 'GIVE.'})

# ── Q6 Fuels ─────────────────────────────────────────────────────────────────
C.fixed([k('6', 'a')], 'chem-2-4', 'property-that-sorts-hydrocarbons-into-fractions')
C.fixed([k('6', 'b', 'i')], 'chem-2-4', 'kerosene-for-jet-aircraft')
C.fixed([k('6', 'b', 'ii')], 'chem-2-4', 'catalytic-cracking-of-kerosene')
C.fixed([k('6', 'c')], 'chem-2-4', 'reference-hydrocarbons-for-octane-numbers')
C.fixed([k('6', 'd')], 'chem-2-4', 'advantages-of-oxygenates-in-petrol')
# (e): the answer (12); the first route's four equations (3) each, then after
# "or" a second route by the sums of heats of formation.
_q6e = P.items(k('6', 'e'))
assert _q6e[0].cell == '[12]' and len(_q6e[-1].asides) == 2, _q6e
C.route([k('6', 'e')], 'chem-3-1', 'heat-of-formation-of-ethanol', figure=S + 'q6e',
        notes='After "or" the scheme works it from the sums of heats of formation, three terms (3) each and the '
              'answer (3).')
shown('After "or" the scheme sets a second route, from the sums of heats of formation; its own print of both is '
      'shown with the answer. It adds: ' + ' '.join(_q6e[-1].asides))
C.menu([k('6', 'f', 'i')], 'chem-2-4', 'why-hydrogen-fuelled-the-space-shuttle', note='"' + raw(10, 604, 620, 450) + '".')
C.fixed([k('6', 'f', 'ii')], 'chem-2-4', 'a-disadvantage-of-hydrogen-as-a-fuel')
C.menu([k('6', 'f', 'iii')], 'chem-2-4', 'industrial-sources-of-hydrogen', note='"' + raw(10, 743, 759, 450) + '".')

# ── Q7 Catalysis and rates ───────────────────────────────────────────────────
Q7 = FIG + 'paper-q7'
# The paper prints "The diagram shows the oxidation of methanol using platinum
# wire as catalyst." after (b) and before (c) (page 7, y 521): the lead of (c)
# and (d), which Cards.context carries to romans only.
Q7_LEAD = P.lead(k('7', 'b'))
assert Q7_LEAD == 'The diagram shows the oxidation of methanol using platinum wire as catalyst.', Q7_LEAD
# (a): two wordings, the second after "or", each two points, priced (3 + 2).
_q7a = P.items(k('7', 'a'))
_w = _q7a[0].points()
assert [it.cell for it in _q7a] == ['[3 + 2]'] and len(_w) == 4 and raw(11, 98, 115) == 'or', _q7a
C.add([k('7', 'a')], 'chem-3-2', 'what-a-catalyst-is', [
    menu_row('r-1', [_w[0], _w[2]], 1, 'One of these wordings, the scheme setting the second after "or". Under the '
             'first it adds: ' + _q7a[0].asides[0]),
    menu_row('r-2', [_w[1], _w[3]], 1, 'And the second point of that same wording.')],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'))
C.fixed([k('7', 'b')], 'chem-3-2', 'bonding-and-the-rate-of-reactions-in-solution', row_notes={0: 'EXPLAIN.', 1: 'HOW.'})
# (c): STATE (3); IDENTIFY, any two of three (2 x 3).
_q7c = P.items(k('7', 'c'))
assert [it.cell for it in _q7c] == ['[3]', '[2 × 3]'] and '[any two]' in _q7c[1].asides, _q7c
C.add([k('7', 'c')], 'chem-3-2', 'oxidising-methanol-on-platinum', [
    lift('r-1', _q7c[0].text, 3, 'STATE.'),
    menu_row('r-2', _q7c[1].options(), 2, 'IDENTIFY: any two of these, (3) each: "' + raw(11, 370, 386, 455)
             + '". The scheme adds: ' + ' '.join(a for a in _q7c[1].asides if not a.startswith('[any')),
             per=3, total=6)], total=9, figure=Q7, stem=Q7_LEAD)
C.fixed([k('7', 'd')], 'chem-3-2', 'adsorption-and-catalyst-poisoning', figure=Q7, stem=Q7_LEAD,
        row_notes={0: 'WHAT.', 1: 'EXPLAIN.', 2: 'EXPLAIN.'})
# (e): EXPLAIN, two wordings, the second after "or", each two points (2 x 3);
# SKETCH, four points (3) each, beside the scheme's diagram. Six rows outrun a
# card: the two asks are a card each.
Q7E_DEF, Q7E_SKETCH = cut(P.ask(k('7', 'e')), 'Sketch a reaction')
assert Q7E_DEF == 'Explain the term activation energy of a reaction.', Q7E_DEF
_q7e = P.items(k('7', 'e'))
assert [it.cell for it in _q7e] == ['[2 × 3]'] + ['[3]'] * 4, _q7e
_e1 = [raw(11, 587, 603, 130, 450), raw(11, 600, 616, 130, 330)]
_e2 = [raw(11, 625, 654, 130, 330), raw(11, 651, 666, 130, 260)]
assert _e1[0].endswith(' //') and _e2[0].endswith(' //') and raw(11, 612, 629) == 'or', (_e1, _e2)
_coll = raw(11, 663, 679, 130, 350)
assert _coll == '[Mention of collisions essential but only once.]' and _q7e[0].asides == [_coll], _q7e
C.add([k('7', 'e')], 'chem-3-2', 'activation-energy', [
    menu_row('r-1', [_e1[0][:-len(' //')], _e2[0][:-len(' //')]], 1, 'One of these wordings, the scheme setting the '
             'second after "or"; it prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_e1[1], _e2[1]], 1, 'And the second point of that same wording, (3). The scheme adds: ' + _coll,
             per=3, total=3)],
    total=6, qtext=Q7E_DEF, cid='q7-e-activation-energy', ref_suffix='activation energy')
C.add([k('7', 'e')], 'chem-3-2', 'reaction-profile-of-an-exothermic-reaction', [
    lift('r-1', _q7e[1].text, 3),
    lift('r-2', _q7e[2].text, 3),
    lift('r-3', _q7e[3].text, 3),
    lift('r-4', _q7e[4].text, 3, 'The scheme adds: ' + ' '.join(_q7e[4].asides) + ' Its own diagram is shown with '
         'the answer.')],
    qtext=Q7E_SKETCH, figure=S + 'q7e', cid='q7-e-reaction-profile', ref_suffix='reaction profile')

# ── Q8 Propene, propan-2-ol and propanone ────────────────────────────────────
Q8 = FIG + 'paper-q8'
C.ordered([k('8', 'a')], 'chem-4-2', 'naming-propene-propan-2-ol-and-propanone', figure=Q8)
C.fixed([k('8', 'b')], 'chem-4-2', 'the-addition-polymer-of-propene', figure=Q8)
# (c): three points (3 x 3). The scheme's equation font sets the letter pi as a
# glyph the text layer reads as U+08CA (page 12, y 150, "pi (π) bond"); the
# page prints π.
_q8c = P.items(k('8', 'c'))
_pi = _q8c[0].points()[0]
assert [it.cell for it in _q8c] == ['[3 × 3]'] and _pi.count('࣊') == 2, _q8c
C.fixed([k('8', 'c')], 'chem-4-2', 'bonds-broken-and-formed-reducing-propanone', figure=Q8,
        fixes={display(_pi): display(_pi).replace('࣊', 'π')})
# (d): NAME (2 x 3); DRAW (2 x 3), two structures in boxes; HOW (6).
_q8d = P.items(k('8', 'd'))
assert [it.cell for it in _q8d] == ['[2 × 3]', '[2 × 3]', '[6]'] and not _q8d[1].text, _q8d
_nm = _q8d[0].points()
assert _nm == ['isomer: 1-propanol / propan-1-ol / propyl alcohol', 'aldehyde: propanal / propionaldehyde'], _nm
C.add([k('8', 'd')], 'chem-4-2', 'propan-1-ol-from-propanal', [
    lift('r-1', _nm[0], 3, 'NAME. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _nm[1], 3),
    lift('r-3', 'propan-1-ol', 3, 'DRAW: its full structural formula; the scheme draws both in boxes, shown with the '
         'answer, and prices them (2 × 3), one each. It adds: ' + ' '.join(_q8d[1].asides)),
    lift('r-4', 'propanal', 3, 'DRAW: its full structural formula.'),
    lift('r-5', _q8d[2].text, 6, 'HOW. The scheme adds: ' + ' '.join(_q8d[2].asides))], figure=S + 'q8d')
# (e): IDENTIFY, any two of three (2 x 3); JUSTIFY, the two that correspond
# (2 x 3), its cell set under the three (page 12, y 655), which the cue reader
# misses for the "(3)" inside the aside below.
_q8e = P.items(k('8', 'e'))
assert _q8e[0].cell == '[2 × 3]' and '[any two]' in _q8e[0].asides, _q8e
_id = [o.replace(' oC', ' °C') for o in _q8e[0].options()]
assert len(_id) == 3 and _id[1].endswith('= 82 °C (highest boiling point)'), _id
_js = [raw(12, 578, 607, 130), raw(12, 603, 632, 130), raw(12, 628, 657, 130)]
assert _js[0].endswith('between the molecules //') and _js[1].endswith('between the molecules //') and \
    _js[2].endswith('between the molecules'), _js
_corr = raw(12, 654, 670, 400)
_jx = [raw(12, 666, 695), raw(12, 691, 721)]
assert _corr == 'CORRESPONDING TWO: (2 × 3)' and _jx[0].startswith('[The marks for JUSTIFY') and \
    _jx[1].endswith('(3) may be awarded.]'), (_corr, _jx)
C.add([k('8', 'e')], 'chem-2-2', 'boiling-points-and-intermolecular-forces', [
    menu_row('r-1', _id, 2, 'IDENTIFY: any two of these, (3) each: "' + raw(12, 544, 560, 455) + '".',
             per=3, total=6),
    menu_row('r-2', [j[:-len(' //')] if j.endswith(' //') else j for j in _js], 2, 'JUSTIFY: the two that '
             'correspond, (3) each: "' + _corr + '". The scheme adds: ' + ' '.join(_jx), per=3, total=6)],
    total=12, figure=Q8)

# ── Q9 Acids, pH and a titration curve ──────────────────────────────────────
Q9F = FIG + 'paper-q9'
# (a)(i)-(ii): one cell (2 x 3), one each.
_q9a = [P.items(k('9', 'a', r)) for r in ('i', 'ii')]
assert [[it.cell for it in its] for its in _q9a] == [[None], ['[2 × 3]']], _q9a
_arr = display(_q9a[0][0].text)
assert _arr.endswith(' //'), _arr
C.add([k('9', 'a', 'i'), k('9', 'a', 'ii')], 'chem-3-4', 'arrhenius-and-bronsted-lowry-acids', [
    lift('r-1', _arr[:-len(' //')], 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _q9a[1][0].text, 3, 'For (ii).')],
    qtext=P.ask(k('9', 'a')) + ' (i) ' + P.ask(k('9', 'a', 'i')) + ' (ii) ' + P.ask(k('9', 'a', 'ii')), stem='')
C.fixed([k('9', 'b')], 'chem-3-4', 'ph-and-a-limitation-of-the-scale', row_notes={0: 'DEFINE.', 1: 'STATE.'})
# The paper prints the titration's lead-in after (b) (page 8, y 502-571); the
# table and the apparatus beside it are the crop paper-q9.
Q9_LEAD = P.lead(k('9', 'b'))
assert Q9_LEAD.startswith('A sodium hydroxide solution was titrated') and Q9_LEAD.endswith('shown in the table.'), Q9_LEAD
# (c): four points (3, 3, 3, 6) beside the scheme's graph (page 14); the ask
# needs the paper's table: its own print is the question.
_q9c = P.items(k('9', 'c'))
assert [it.cell for it in _q9c] == ['[3]', '[3]', '[3]', '[6]', None], _q9c
_see = display(_q9c[0].text)
assert _see.startswith('See graph on next page. '), _see
C.fixed([k('9', 'c')], 'chem-3-4', 'ph-curve-of-ethanoic-acid-against-sodium-hydroxide', figure=S + 'q9c', stem=Q9_LEAD,
        fixes={_see: _see[len('See graph on next page. '):]},
        row_notes={0: 'The scheme opens: "See graph on next page."; its graph is shown with the answer.'})
print_question('paper-q9c-print')
# (d)(i): the answer (9); two boxed routes, the hydrogen ion concentration (6)
# and the acid's (3), in an equation font the text layer cannot read.
_q9d1 = P.items(k('9', 'd', 'i'))
assert _q9d1[0].cell == '[9]' and display(_q9d1[0].text) == '0.014 M [0.0139 – 0.014 M]', _q9d1
_take = raw(13, 425, 442, 100)
assert _take == 'Take [acid] or [HA] or M to be [CH₃COOH] and [A⁻] to be [CH₃COO⁻]', _take
_round = raw(13, 586, 602)
assert _round == '[1 mark deducted for incorrect rounding off.]', _round
C.answer_only([k('9', 'd', 'i')], 'chem-3-4', 'concentration-of-a-weak-acid-from-its-ph', S + 'q9d-i', stem=Q9_LEAD,
              notes='The scheme sets out two boxed routes, each the hydrogen ion concentration from the pH (6) and '
                    'then the acid\'s concentration (3).')
shown('The scheme prices each of its two routes in two steps, (6) and (3). Under each it adds: "' + _take + '", and '
      'then: ' + _round)
print_question('paper-q9d-i-print')
C.fixed([k('9', 'd', 'ii')], 'chem-3-4', 'volume-at-neutralisation-from-the-ph-curve', figure=Q9F, stem=Q9_LEAD)
C.fixed([k('9', 'e')], 'chem-3-4', 'choosing-an-indicator-from-the-ph-curve', figure=Q9F, stem=Q9_LEAD,
        row_notes={0: 'WHAT.', 1: 'REFER.'})

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q10A = FIG + 'paper-q10a'
# (a): DISTNG (2 x 2), DESCRIBE (6 and 3), the letter's own asks under (13);
# HOW MANY (3), set before (i); EXPLAIN (i) and (ii), (3) each, the paper
# setting them on lines of their own inside one sentence; GIVE (3), set after
# (ii). Under (12): a card each, cited with what it holds.
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == ['[2 × 2]', '[6]', '[3]', '[3]'] and _q10a[3].text == '6', _q10a
_d = _q10a[0].options()
assert len(_d) == 2 and _d[1].startswith('unsaturated hydrocarbons'), _d
_rg = display(_q10a[1].text)
assert _rg.endswith('(KMnO₄/H⁺) / (MnO₄¯/H⁺)'), _rg
C.add([k('10', 'a')], 'chem-2-4', 'saturated-and-unsaturated-hydrocarbons-and-the-test', [
    lift('r-1', _d[0], 2, 'DISTNG. The scheme prices these points (2 × 2), one each.'),
    lift('r-2', _d[1], 2, 'The scheme adds: ' + _q10a[0].asides[0]),
    # The scheme sets the charge on MnO₄ as a raised macron (page 15, y 187); the page prints a minus.
    lift('r-3', _rg.replace('MnO₄¯', 'MnO₄⁻'), 6, 'DESCRIBE.'),
    lift('r-4', _q10a[2].text, 3, 'The scheme adds: ' + _q10a[2].asides[0])],
    qtext=P.ask(k('10', 'a')), stem='', cid='q10-a-saturation', ref_suffix='saturated and unsaturated')
Q10A_KEK, _r = cut(P.lead(k('10', 'a')), 'How many pi-electrons')
Q10A_HOW, Q10A_EXPL = cut(_r, 'Explain whether')
assert Q10A_KEK == 'In 1865 August Kekulé proposed the structure for benzene shown on the right.' and \
    Q10A_EXPL.endswith('correctly describes'), (Q10A_KEK, Q10A_EXPL)
C.add([k('10', 'a')], 'chem-2-1', 'pi-electrons-in-benzene', [lift('r-1', '6', 3, 'HOW MANY.')],
      qtext=Q10A_HOW, stem=Q10A_KEK, figure=Q10A, cid='q10-a-pi-electrons', ref_suffix='pi-electrons in benzene')
_q10a2_ask, Q10A_GIVE = cut(P.ask(k('10', 'a', 'ii')), 'Give one piece')
Q10A_SENT = Q10A_EXPL + ' (i) ' + P.ask(k('10', 'a', 'i')) + ' (ii) ' + _q10a2_ask
assert Q10A_SENT.endswith('(i) the number, (ii) the distribution, of the pi-electrons in benzene.'), Q10A_SENT
C.fixed([k('10', 'a', 'i')], 'chem-2-1', 'kekule-structure-and-the-number-of-pi-electrons', qtext=Q10A_SENT,
        stem=Q10A_KEK, figure=Q10A, row_notes={0: 'For (i).'})
_q10a2 = P.items(k('10', 'a', 'ii'))
assert [it.cell for it in _q10a2] == ['[3]', '[3]'], _q10a2
C.add([k('10', 'a', 'ii')], 'chem-2-1', 'kekule-structure-and-the-distribution-of-pi-electrons', [
    lift('r-1', _q10a2[0].text, 3, 'For (ii).')], qtext=Q10A_SENT, stem=Q10A_KEK, figure=Q10A)
C.add([k('10', 'a')], 'chem-2-1', 'evidence-for-delocalised-electrons-in-benzene', [
    lift('r-1', _q10a2[1].text, 3, 'GIVE.')], qtext=Q10A_GIVE, stem=tidy(Q10A_KEK + ' ' + Q10A_SENT), figure=Q10A,
    cid='q10-a-evidence', ref_suffix='after (ii), experimental evidence')
# (b)(i): any three of five points (6 + 6 + 3); the scheme's labelled diagram
# (page 15, x 338-568, y 588-766) is shown with the answer.
# Its last point runs on into two asides set hard against each other (page 15,
# y 528): the reader lifts the first; the second is quoted in the note.
_q10b1 = P.items(k('10', 'b', 'i'))
_last = display(_q10b1[0].options()[-1])
_tail = ' [Labelled diagram alone, max 12.]'
assert _last.endswith(' [Explanation with no diagram, max 12.]' + _tail.strip()), _last
_last = tidy(_last.replace('[Explanation with no diagram, max 12.]', ' '))     # the reader's text, first aside lifted
C.menu([k('10', 'b', 'i')], 'chem-3-5', 'purifying-copper-by-electrolysis', figure=S + 'q10b-i',
       fixes={_last: _last[:-len(_tail)]},
       note='The scheme adds: ' + _tail.strip() + ' "' + raw(15, 569, 584, 430) + '". Its own labelled diagram is '
            'shown with the answer.')
# (b)(ii): two equations (2 x 3); the scheme sets each electron's charge as a
# raised macron (page 15, y 585-617), the page a minus.
_q10b2 = P.items(k('10', 'b', 'ii'))
assert [it.cell for it in _q10b2] == ['[2 × 3]'] and display(_q10b2[0].text).count('e¯') == 3, _q10b2
_eq = [display(x) for x in _q10b2[0].options()]
assert len(_eq) == 2, _eq
C.fixed([k('10', 'b', 'ii')], 'chem-3-5', 'electrode-reactions-in-purifying-copper',
        fixes={x: x.replace('e¯', 'e⁻') for x in _eq})
C.fixed([k('10', 'b', 'iii')], 'chem-3-5', 'impurities-in-the-anode-mud')
# (c)(i): three wordings, each after "or", each two points (2 x 3).
_m = [(raw(16, 48, 64, 140), raw(16, 61, 76, 140)), (raw(16, 103, 120, 140), raw(16, 117, 133, 140)),
      (raw(16, 161, 177, 140), raw(16, 173, 189, 140, 300))]
assert [a[-3:] for a, _b in _m] == [' //'] * 3 and [b[-2:] for _a, b in _m] == [' /', '*/', 'ms'] and \
    [raw(16, y - 1, y + 16) for y in (83, 139)] == ['or', 'or'], _m
_star = raw(16, 186, 202)
assert _star.startswith('[* ‘Atoms’'), _star
C.add([k('10', 'c', 'i')], 'chem-1-4', 'what-a-mole-is', [
    menu_row('r-1', [a[:-len(' //')] for a, _b in _m], 1, 'One of these wordings, the scheme setting each after '
             '"or"; it prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [b.rstrip('/ ') for _a, b in _m], 1, 'And the second point of that same wording, (3). The scheme '
             'adds: ' + _star, per=3, total=3)], total=6)
# (c)(ii): the answer (6); two boxed routes of two steps (3) each, side by side,
# their first steps set as fractions.
_q10c2 = P.items(k('10', 'c', 'ii'))
assert _q10c2[0].cell == '[6]' and display(_q10c2[0].text) == '0.4 mol', _q10c2
_s2 = [raw(16, 260, 280, 125, 360), raw(16, 260, 276, 375)]
assert _s2 == ['0.10 mol Mg₂Si → 0.40 = 0.4 mol Mg (3)', '9.6 ÷ 24 = 0.4 mol Mg (3)'], _s2
assert raw(16, 233, 249, 420) == '= 9.6 g Mg (3)', raw(16, 233, 249, 420)
C.add([k('10', 'c', 'ii')], 'chem-1-4', 'moles-of-magnesium-for-a-mass-of-silicide', [
    menu_row('r-1', ['7.6 ÷ 76∗ = 0.10 = 0.10 mol Mg₂Si', '9.6 g Mg'], 1, 'The first step of either route, the second '
             'after "or", (3). ' + FRACTION.format('7.6', '76∗') + ' The second route works 4 × 24 × 7.6 over 76∗ '
             '= 9.6 g Mg; its own print of both is shown with the answer.', per=3, total=3),
    menu_row('r-2', [x[:-len(' (3)')] for x in _s2], 1, 'And the second step of that same route, (3).',
             per=3, total=3)],
    total=6, figure=S + 'q10c-ii',
    notes='The scheme gives the answer, 0.4 mol, priced (6), then two boxed routes of two steps (3) each.')
shown('The scheme gives the answer as "0.4 mol" (6).')
# (c)(iii): CALC, the answer (3) by either of two one-step routes (3); WHAT,
# the answer (6) by either of two routes of two steps (3) each.
_q10c3 = P.items(k('10', 'c', 'iii'))
assert [it.cell for it in _q10c3] == ['[3]', '[3]', '[3]', '[6]', '[3]', '[3]', '[3]', '[3]'], _q10c3
assert display(_q10c3[0].text) == '0.4 mol' and display(_q10c3[3].text) == '76∗ 19 g MgCl₂', _q10c3
C.add([k('10', 'c', 'iii')], 'chem-1-4', 'hydrogen-chloride-and-magnesium-chloride-from-silicide', [
    menu_row('r-1', [_q10c3[1].text, '4 × 36.5 ÷ 76∗ × 7.6 = 14.6 ÷ 36.5 = 0.4 mol HCl'], 1, 'CALC: either route, '
             'the second after "or", (3); the scheme gives the answer, 0.4 mol, priced (3). '
             + FRACTION.format('4 × 36.5', '76∗'), per=3, total=3),
    menu_row('r-2', [_q10c3[4].text, _q10c3[6].text], 1, 'WHAT: the first step of either route, the second after '
             '"or", (3); the scheme gives the answer, 19 g MgCl₂, priced (6).', per=3, total=3),
    menu_row('r-3', [_q10c3[5].text, _q10c3[7].text], 1, 'And the second step of that same route, (3).',
             per=3, total=3)],
    total=9, figure=S + 'q10c-iii')
_q10c4 = P.items(k('10', 'c', 'iv'))
assert _q10c4[0].cell == '[4]' and len(_q10c4[-1].asides) == 4, _q10c4
C.route([k('10', 'c', 'iv')], 'chem-1-4', 'volume-of-oxygen-to-burn-the-silane', figure=S + 'q10c-iv',
        notes='After "or" the scheme works it from 76 g of silicide needing 48 L of oxygen, two steps (2) each.')
shown('After "or" the scheme sets a second route; its own print of both is shown with the answer. It adds: '
      + ' '.join(_q10c4[-1].asides))

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): four runs of asks, each under its printed mark, (6), (6), (6), (7);
# eight rows outrun a card, so each run is a card, cited with what it holds.
Q11A = P.ask(k('11', 'a'))
Q11A_DEF, _r = cut(Q11A, 'Why is there')
Q11A_WHY, _r = cut(_r, 'Mendeleev predicted')
Q11A_MEND, Q11A_GE = cut(_r, 'Write the molecular')
assert Q11A_DEF == 'Define electronegativity.' and Q11A_GE.endswith('Justify your answer.'), Q11A
_q11a = P.items(k('11', 'a'))
assert [it.cell for it in _q11a][:3] == ['[2 × 3]', '[2 × 3]', '[6]'], _q11a
_def = _q11a[0].options()
assert len(_def) == 2 and _def[1].startswith('for shared pair'), _def
C.add([k('11', 'a')], 'chem-1-3', 'electronegativity', [
    lift('r-1', _def[0], 3, 'The scheme prices these points (2 × 3), one each.'), lift('r-2', _def[1], 3)],
    qtext=Q11A_DEF, cid='q11-a-electronegativity', ref_suffix='electronegativity defined')
_why = _q11a[1].options()
assert len(_why) == 2 and _why[1] == 'atomic radius decreasing', _why
C.add([k('11', 'a')], 'chem-1-3', 'electronegativity-from-gallium-to-germanium', [
    lift('r-1', _why[0], 3, 'The scheme prices these points (2 × 3), one each.'), lift('r-2', _why[1], 3)],
    qtext=Q11A_WHY, cid='q11-a-gallium-to-germanium', ref_suffix='gallium to germanium')
_w1 = display(_q11a[2].text)
_w2 = raw(17, 186, 227, 130, 545)
assert _w1.startswith('predicted the properties from') and _w2.startswith('having arranged') and \
    raw(17, 224, 240, 490) == '(3 only)' and raw(17, 173, 189) == 'or', (_w1, _w2)
C.add([k('11', 'a')], 'chem-1-3', 'the-basis-of-mendeleevs-predictions', [
    menu_row('r-1', [_w1, _w2], 1, 'One of these, (3): the scheme sets the second after "or" and prices it '
             '"(3 only)"; the first it prices (6), so claim the first here and again below.', per=3, total=3),
    lift('r-2', _w1, 3, 'The first wording again, for the rest of its (6).')],
    total=6, qtext=Q11A_MEND, cid='q11-a-mendeleev', ref_suffix='Mendeleev\'s predictions')
_ge = raw(17, 255, 271, 130, 200)
_no = raw(17, 281, 296, 130, 200)
_sol = raw(17, 293, 322, 130, 545)
_sec = raw(17, 319, 334)
assert (_ge, _no) == ('GeH₄', 'no //') and _sol.startswith('GeH₄ a non-polar') and _sol.endswith(' (2 × 2)') and \
    _sec == '[Second (2) only available if first (2) is awarded.]', (_ge, _no, _sol, _sec)
_sol = _sol[:-len(' (2 × 2)')]                 # its cell, set on its last line (page 17, y 306)
C.add([k('11', 'a')], 'chem-2-2', 'germanium-hydride-and-water', [
    lift('r-1', _ge, 3, 'WRITE.'),
    lift('r-2', 'no', 2, 'WOULD. The scheme prices this and the next (2 × 2), one each.'),
    lift('r-3', _sol, 2, 'The scheme adds: ' + _sec)],
    qtext=Q11A_GE, cid='q11-a-germanium-hydride', ref_suffix='germanium hydride')
# (b): CALC (13), the answer with two boxed routes in an equation font the text
# layer cannot read; DEDUCE (3) and EXPLAIN (3) under (6); EXPLAIN (2 x 3)
# under (6). A card each. The equation, its arrows set in a glyph the text
# layer reads as U+0596, and the graph are the paper's picture (paper-q11b);
# the calculation card takes the paper's own print of its ask.
Q11B = FIG + 'paper-q11b'
Q11B_DATA, _r = cut(P.ask(k('11', 'b')), 'Calculate the number')
Q11B_CALC, _r = cut(_r, 'The graph shows')
Q11B_GRAPH, _r = cut(_r, 'Deduce whether')
Q11B_DED, Q11B_PRESS = cut(_r, 'Explain how an increase')
assert Q11B_DATA.endswith('stored at 15 °C.') and Q11B_GRAPH.endswith('for this equilibrium.') and \
    Q11B_PRESS.endswith('of the equilibrium mixture.'), P.ask(k('11', 'b'))
_q11b = P.items(k('11', 'b'))
assert _q11b[0].cell == '[13]' and display(_q11b[0].text) == '50 mol', _q11b
assert [(it.cell, it.text) for it in _q11b[-3:-2]] == [('[3]', 'endothermic')], _q11b
C.answer_only([k('11', 'b')], 'chem-3-3', 'moles-at-equilibrium-from-kc', S + 'q11b', qtext=Q11B_CALC,
              stem=Q11B_DATA, cid='q11-b-calculation', ref_suffix='moles at equilibrium',
              notes='The scheme sets out two boxed routes, by concentrations and by moles, priced (3), (3), (3), (3) '
                    'and (1), and under them allows (3) for the Kc expression where no other mark is awarded.')
shown('The scheme prices each of its two routes in five steps, (3), (3), (3), (3) and (1), and under them allows '
      '(3) for the Kc expression where no other mark is awarded; its own print is shown with the answer.')
print_question('paper-q11b-calc-print')
C.add([k('11', 'b')], 'chem-3-3', 'kc-rising-with-temperature', [
    lift('r-1', _q11b[-3].text, 3, 'DEDUCE.'),
    lift('r-2', _q11b[-2].text, 3, 'EXPLAIN. The scheme adds: ' + _q11b[-2].asides[0])],
    qtext=Q11B_DED, stem=tidy(Q11B_DATA + ' ' + Q11B_GRAPH), figure=Q11B, cid='q11-b-endothermic',
    ref_suffix='exothermic or endothermic')
_pr = _q11b[-1].options()
assert _q11b[-1].cell == '[2 × 3]' and len(_pr) == 2 and _pr[0] == 'increase', _q11b[-1]
C.add([k('11', 'b')], 'chem-3-3', 'temperature-and-the-pressure-of-the-mixture', [
    lift('r-1', _pr[0], 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _pr[1], 3, 'The scheme adds: ' + _q11b[-1].asides[0])],
    qtext=Q11B_PRESS, stem=tidy(Q11B_DATA + ' ' + Q11B_GRAPH), figure=Q11B, cid='q11-b-pressure',
    ref_suffix='storage temperature and pressure')
# (c)A: the greenhouse effect.
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'greenhouse-gases')
print_question('paper-q11c-a-i-print')         # the term is underlined in the quotation
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'a-consequence-of-uncontrolled-greenhouse-emissions')
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-4-3', 'greenhouse-factors-and-cfcs-in-the-stratosphere',
        row_notes={0: 'ARRANGE.', 1: 'WHICH.', 2: 'DESCRIBE.'})
# (iv): any two (2 x 3) of a list the scheme ends "// etc", which is no answer.
_q11a4 = P.items(ka('11', 'c', 'iv', 'A'))
_o = _q11a4[0].options()
assert [it.cell for it in _q11a4] == ['[2 × 3]'] and _o[-1] == 'etc' and len(_o) == 14, _o
C.add([ka('11', 'c', 'iv', 'A')], 'chem-4-3', 'reducing-irelands-greenhouse-emissions', [
    menu_row('r-1', _o[:-1], 2, 'Any two of these, (3) each: "' + raw(18, 323, 339, 450) + '". The scheme ends its '
             'list "// etc".', per=3, total=6)], total=6)
# (c)B: the blast furnace.
Q11CB = FIG + 'paper-q11c-b'
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-u3', 'coke-and-limestone-in-the-charge', figure=Q11CB)
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-u3', 'reducing-iron-iii-oxide-in-the-blast-furnace', figure=Q11CB)
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-u3', 'forming-slag-and-its-use', figure=Q11CB,
        row_notes={0: 'USE.', 1: 'GIVE.'})
C.fixed([ka('11', 'c', 'iv', 'B')], 'chem-u3', 'an-environmental-effect-of-the-blast-furnace', figure=Q11CB,
        skip=('Blank Page',), row_notes={0: 'GIVE.', 1: 'HOW.'})


# A note quoted from the scheme in the reader's script notation ("E_(n>2)",
# "K_(c)") is shown as the page sets it.
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'], _r


# ── review ───────────────────────────────────────────────────────────────────
INLINE = {}


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
    for key in sorted(set(got) | set(marks), key=lambda kv: (int(kv[0]), kv[1])):
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
