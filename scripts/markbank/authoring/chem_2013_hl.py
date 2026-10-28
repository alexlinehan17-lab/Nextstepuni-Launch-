#!/usr/bin/env python3
"""2013 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2013_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2013_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2013_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2013 hl

No 2013 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

Reader (chem_print, gated to 2013 HL). The paper sets the heads of Questions 8,
10 and 11 in one run with their words ("8. Study the reaction scheme ..."), as
the 2013 Ordinary paper sets all of its own, and Q11(c)'s choice as "Answer
either part A or part B."; the scheme's Introduction numbers its notes "1."-"6."
in roman type, read as heads, and its running footer is "Chemistry ATAL 2013".
Each is read as the page means it (chem_print: OLD_OL_HEADS joined,
PAPER_ALT_LETTERS, and the 2013 HL block of Printed); the census reads Q11(c)'s
alternatives the same way (paper_census.chemistry_choice_parts).

The census keeps the paper's 79 asks. Romans the paper sets inside one sentence
are one census ask and a card per scheme cell, each showing the sentence with a
"For (i)."-style note: Q3(c), Q8(b) (one cell (3 x 3): one card), Q9(b) (its
(i) and (ii) on lines of their own after "Explain"; the census keeps Q9(b)
whole and the cards cite Q9(b)(i) and (ii), which reconcile reads as Q9(b)),
Q7(e) (one cell (3 x 3) with the drawing: one card) and Q11(b) (three asks
printed (7), (6), (12): a card each). Asks the paper sets before a letter's
first roman are the letter's own card (Q1(f), Q10(a), Q11(a)); the ask set
after Q11(c)B(iv) is a card cited "— after (iv)". Where a letter's asks
outrun a card's five rows, or the paper prints them under marks of their own,
each run is a card cited with what it holds (Q5(b), Q7(d), Q9(a), Q9(c),
Q11(b)). Q4(k) and Q11(c) offer alternative parts A and B.

The paper underlines the terms Q5(c) and Q8(a) ask about, which no text layer
carries: those cards take the paper's own print as their question, as do Q6(c)
(its equation's state symbols), the ask after Q11(c)B(iv) (its table of
industries and sites), and the parts whose figure is the scheme's and whose ask
needs the paper's structures, reaction scheme, equation or graph (Q6(b)(ii),
Q8(c), Q8(d), Q9(c) twice, Q11(a)(iii)).

The scheme sets its fractions and square roots in Cambria Math glyphs the text
layer maps to spaces (Q1(f), Q3(e), Q4(e), Q4(h), Q7(a), Q7(d), Q9(c), Q11(b)):
those steps are rows lifted from the words around them, each with a note saying
what the fraction prints, and the scheme's own print is the card's figure. Two
such glyphs inside answers are set back where the page prints them, each asserted
on the reader's text: the degree sign of "0.2°C" (Q3(d), glyph 953) and the arrow
of "0.2 mol ⇒ 0.2 M" (Q11(b), glyph 1436).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, norm, point, read_lines, tidy  # noqa: E402

P = Printed(2013, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2013-HL-'
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
        raise Refused(f'"{text}" is not in the 2013 hl scheme')
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


def split_asides(text):
    """(the answer, its examiner's asides): the asides the scheme sets inside an
    answer's line ("[Do not accept “fill the tap.”] use tap ...") lifted out."""
    from chem_print import INLINE_ASIDE
    asides = INLINE_ASIDE.findall(text)
    return tidy(INLINE_ASIDE.sub(' ', text)), [a.strip() for a in asides]


# ── Q1 Dissolved oxygen in a river water sample ──────────────────────────────
Q1 = FIG + 'paper-q1'
Q1_STEM = C.context(k('1', 'a'))
assert Q1_STEM.startswith('In an experiment to measure the dissolved oxygen') and \
    Q1_STEM.endswith('inverted several times to ensure thorough mixing.'), Q1_STEM
# The titration the paper sets after (c) (page 2, y 388-455), its equation's
# charges read after their ions; set where the page prints them.
Q1_TITR = P.lead(k('1', 'c'))
assert Q1_TITR.startswith('After the three additions') and \
    Q1_TITR.endswith('2S₂O₃ 2– + I₂ → S₄O₆ 2– + 2I –'), Q1_TITR
Q1_TITR = P.rearranged(Q1_TITR, '2S₂O₃ 2– + I₂ → S₄O₆ 2– + 2I –', '2S₂O₃²⁻ + I₂ → S₄O₆²⁻ + 2I⁻')
Q1_LATER = Q1_STEM + ' ' + Q1_TITR
C.fixed([k('1', 'a')], 'chem-4-3', 'air-bubbles-in-a-dissolved-oxygen-sample', stem=Q1_STEM, figure=Q1)
C.fixed([k('1', 'b')], 'chem-4-3', 'manganese-ii-sulfate-in-the-winkler-method', stem=Q1_STEM, figure=Q1)
C.fixed([k('1', 'c')], 'chem-4-3', 'iodine-released-on-adding-the-acid', stem=Q1_STEM, figure=Q1)
# (d): RINSE, two points (2 x 3); FILL, any three of four (3 x 3).
_q1d = P.items(k('1', 'd'))
assert [it.cell for it in _q1d] == ['[2 × 3]', '[3 × 3]'] and '[any three]' in _q1d[1].asides, _q1d
_rinse = [display(x).strip() for x in _q1d[0].text.split('//')]
assert _rinse == ['rinse with deionised (distilled) water', 'rinse with a little of the thiosulfate solution',
                  '[Accept “rinse with thiosulfate.]'], _rinse
_fill, _fill_asides = [], []
for _o in _q1d[1].options():
    _t, _a = split_asides(_o)
    _fill.append(_t)
    _fill_asides += _a
assert len(_fill) == 4 and _fill[3].startswith('use tap (or dropper)'), _fill
_any3 = raw(5, 368, 386, 440)
assert _any3 == 'ANY THREE: (3 × 3)', _any3
C.add([k('1', 'd')], 'chem-4-1', 'rinsing-and-filling-a-burette', [
    lift('r-1', _rinse[0], 3, 'RINSE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _rinse[1], 3, 'The scheme adds: ' + _rinse[2]),
    menu_row('r-3', _fill, 3, 'FILL: any three of these, (3) each: "' + _any3 + '". The scheme adds: '
             + ' '.join(_fill_asides + [a for a in _q1d[1].asides if not a.startswith('[any')]), per=3, total=9)],
    total=15, stem=Q1_LATER, figure=Q1)
C.fixed([k('1', 'e')], 'chem-4-1', 'starch-indicator-for-the-iodine-titration', stem=Q1_LATER, figure=Q1)
# (f): CALC, the answer (6), worked in a box as a fraction (3) and x (3), which
# the text layer reads as spaces (Cambria Math glyphs mapped to U+0020).
Q1F_IODINE, Q1F_LEAD = cut(P.ask(k('1', 'f')), 'For every')
assert Q1F_IODINE == 'Calculate the concentration of iodine (I₂) in the sample bottle in moles per litre.', Q1F_IODINE
assert Q1F_LEAD.endswith('Calculate the concentration of dissolved oxygen in the river water sample'), Q1F_LEAD
_q1f = P.items(k('1', 'f'))
assert [it.cell for it in _q1f] == ['[6]', '[3]', '[3]'] and display(_q1f[2].text) == 'x = 0.00047', _q1f
# Its only figure is the scheme's working, held back until the reveal, so the stem's sentence on
# "the method shown in the diagram" would point at nothing. Nothing in (f) depends on it: the
# iodine comes from the titre, the thiosulfate's concentration and the equation, which the
# stem's other sentences print. That sentence is left out of this card's stem.
_DIAG = 'These additions were made using the method shown in the diagram, avoiding the addition of bubbles of air.'
assert Q1_LATER.count(_DIAG) == 1, Q1_LATER
_before, _after = Q1_LATER.split(_DIAG)
C.answer_only([k('1', 'f')], 'chem-4-1', 'iodine-concentration-from-the-thiosulfate-titre', S + 'q1f',
              qtext=Q1F_IODINE, stem=_before.strip() + ' ' + _after.strip())
shown('The scheme works it in a box, the titration formula set as fractions (3) and x = 0.00047 (3), and adds: '
      + ' '.join(_q1f[1].asides + _q1f[2].asides))
# (i)-(iii) complete one sentence, on lines of their own (page 2, y 523-607);
# each is priced (3), its answer and the one step that earns it.
Q1F_SENT = Q1F_LEAD + ' (i) ' + P.ask(k('1', 'f', 'i')) + ' (ii) ' + P.ask(k('1', 'f', 'ii')) + ' (iii) ' + \
    P.ask(k('1', 'f', 'iii'))
assert Q1F_SENT.endswith('sample (i) in moles per litre, (ii) in grams per litre, (iii) in ppm.'), Q1F_SENT
for _r, _concept, _ans, _step in (
        ('i', 'dissolved-oxygen-in-moles-per-litre', '0.000235 mol l⁻¹ O₂', '0.00047 ÷ 2 = 0.000235'),
        ('ii', 'dissolved-oxygen-in-grams-per-litre', '0.00752 g l⁻¹ O₂', '0.000235 × 32 = 0.00752'),
        ('iii', 'dissolved-oxygen-in-ppm', '7.52 ppm O₂', '0.00752 × 1000 = 7.52')):
    _its = P.items(k('1', 'f', _r))
    _a, _accept = split_asides(display(_its[0].text))
    assert [it.cell for it in _its] == ['[3]', '[3]'] and _a == _ans and display(_its[1].text) == _step, _its
    C.add([k('1', 'f', _r)], 'chem-4-1', _concept, [
        lift('r-1', _ans, 3, f'For ({_r}). The scheme gives the answer, priced (3), and the one step that earns it: "{_step}" '
             '(3). It adds: '
             + ' '.join(_accept + _its[1].asides))],
        qtext=Q1F_SENT, stem=Q1_TITR + ' ' + Q1F_IODINE)
C.fixed([k('1', 'g')], 'chem-4-3', 'a-white-precipitate-and-no-dissolved-oxygen', stem=Q1_STEM, figure=Q1)
C.fixed([k('1', 'h')], 'chem-4-3', 'measuring-dissolved-oxygen-at-once', stem=Q1_STEM, figure=Q1)

# ── Q2 Tasks in a practical examination ──────────────────────────────────────
# A note in the scheme's left margin beside (a)'s box of tests (page 6, x 60-111,
# y 162-257), read as a picture's labels (crops 'q2a-margin') and quoted here.
_link = traced(raw(6, 160, 258, 55, 115))
assert _link == 'In part (a) and in part (b) do not apply linkage when acidification of a correct reagent is omitted', \
    _link
# (a): HOW, priced "(5 or 3)" (page 6, x 506, y 93), a cell the reader does not
# read: the reagent named with its result, either from the box of tests below it
# (page 6, y 135-329), those showing ethanoic acid and those showing not ethanol.
_how = [raw(6, 66, 82, 120), raw(6, 79, 95, 120), raw(6, 92, 108, 120)]
assert _how[2] == '[Named substance, reagent & result linked; ethanoic acid may be inferred.] (5 or 3)', _how
_acid = [raw(6, 135, 151, 120), raw(6, 173, 189, 120), raw(6, 199, 214, 120), raw(6, 210, 227, 120)]
_not = [raw(6, 248, 265, 120) + ' ' + raw(6, 262, 278, 120), raw(6, 275, 290, 120), raw(6, 312, 329, 120)]
assert _acid[0].startswith('ethanoic acid: ') and _not[0].startswith('not ethanol: '), (_acid, _not)
_ind, _only = split_asides(_acid[0][len('ethanoic acid: '):])
_tests = [_ind] + _acid[1:] + [P.rearranged(_not[0][len('not ethanol: '):], 'MnO₄ –])', 'MnO₄⁻])')] + _not[1:]
assert _tests[3].endswith('– fruity (ester) odour') and _tests[6].endswith('– no fruity (ester) odour'), _tests
_star = raw(6, 148, 164, 200) + ' ' + raw(6, 161, 176, 200)
_dichro = raw(6, 299, 316, 200)
assert _star.endswith('[*Accept “phenolphthalein” but not “no colour change”.]') and \
    _dichro == '[allow acidified dichromate H⁺/Cr₂O₇ ²⁻][*Accept “permanganate.”]', (_star, _dichro)
C.add([k('2', 'a')], 'chem-4-2', 'telling-ethanoic-acid-from-ethanol', [
    menu_row('r-1', _tests, 1, 'HOW: one test, the reagent named with its result; the first four show the liquid is '
             'ethanoic acid ("ethanoic acid:"), the last three that it is not ethanol ("not ethanol:"). The scheme '
             'prices it "(5 or 3)": "' + _how[0] + ' ' + _how[1] + '" ' + _how[2][:-len(' (5 or 3)')] + ' It adds: '
             + ' '.join(_only) + ' ' + _star + ' [NB: alkali metals unsuitable] '
             + _dichro.replace('Cr₂O₇ ²⁻]', 'Cr₂O₇²⁻]') + ' Beside the box: "' + _link + '".', per=5, total=5)],
    total=5, notes='The scheme prices HOW "(5 or 3)" without saying when 3 is awarded; the row is worth the 5.')
# (b): DESCRIBE, "with named reagent (3) // colour before (3) // colour after (6)"
# (page 6, y 370), over a box of two reagents (y 398-451).
_desc = raw(6, 369, 386, 70)
assert _desc == 'DESCRIBE: with named reagent (3) // colour before (3) // colour after (6) [Reagent & colours linked.]', \
    _desc
_br = (raw(6, 398, 414, 120) + ' ' + raw(6, 410, 426, 120)).split(' // ')
_mn = (raw(6, 422, 439, 120) + ' ' + raw(6, 436, 451, 120)).split(' // ')
assert _br[2] == 'colourless (disappears) [Not “clear”.]' and \
    _mn[2] == 'colourless (disappears) [Not “clear” .][* Accept “permanganate.”]', (_br, _mn)
C.add([k('2', 'b')], 'chem-4-2', 'testing-ethene-for-unsaturation', [
    menu_row('r-1', [_br[0], P.rearranged(_mn[0], 'MnO₄ –]', 'MnO₄⁻]')], 1,
             'With named reagent, (3). The scheme prices its points "' + _desc[len('DESCRIBE: '):] + '" Beside the box: "'
             + _link + '".', per=3, total=3),
    menu_row('r-2', [_br[1], _mn[1]], 1, 'Colour before, (3), of the reagent named.', per=3, total=3),
    lift('r-3', 'colourless (disappears)', 6, 'Colour after, (6). The scheme adds: [Not “clear”.] '
         '[* Accept “permanganate.”]')], total=12)
# (c): DESCRIBE, the points of the one method drawn and described: paper or
# thin-layer chromatography, four points (4 x 3), or column chromatography, two of
# three points (2 x 3) then two (2 x 3) (pages 6-7). The diagrams' labels are
# read as pictures' (crops 'q2c-...-labels'); the scheme's own print is shown.
_paper = [raw(6, y - 1, y + 16, 165).rstrip('/ ') for y in (494.8, 507.1, 519.9, 532.7)]
_tlc = [raw(6, y - 1, y + 16, 165).rstrip('/ ') for y in (637.9, 650.3, 662.9, 675.9)]
_col = [raw(7, y - 1, y + 16, 165, 500).rstrip('/ ') for y in (88.4, 103.1, 117.5, 132.3, 146.9)]
assert _paper[0].endswith('spot on paper') and _tlc[0].endswith('spot on plate') and \
    _col[0] == 'dissolve mixture in eluent*' and _col[4].startswith('separation of components'), (_paper, _tlc, _col)
assert _paper[2] == _tlc[2], (_paper, _tlc)
_chrom = list(dict.fromkeys(_paper + _tlc + _col))
assert len(_chrom) == 12, _chrom
_c2 = [it.cell for it in P.items(k('2', 'c'))]
assert _c2 == ['[4 × 3]', '[4 × 3]', '[2 × 3]', '[2 × 3]'], _c2
_lid = traced('[Lid not required in diagram.]')
_elu = traced(raw(6, 544, 586, 165, 500))
_soak, _mob = traced(raw(6, 741, 758, 165)), traced(raw(7, 160, 177, 165))
_nodia = traced(raw(7, 197, 227, 165))
assert _elu.startswith('[The elution stage') and _nodia.startswith('[If there is no diagram'), (_elu, _nodia)
C.add([k('2', 'c')], 'chem-u2', 'separating-indicators-by-chromatography', [
    menu_row('r-1', _chrom, 4, 'Claim four points of one method, paper, thin-layer or column chromatography, not '
             'a mix. DESCRIBE: four points of the one method used, (3) each. Paper chromatography is '
             'points 1-4 (4 × 3); thin-layer chromatography points 5-7, with point 3 as its third (4 × 3); column '
             'chromatography points 8-12, two of points 8-10 (2 × 3) and points 11-12 (2 × 3). The scheme draws each '
             'method, labelled; its own print is shown with the answer. It adds: '
             + ' '.join([_lid, _elu, _soak, _mob, _nodia]), per=3, total=12)],
    total=12, figure=S + 'q2c')
# (d): WHICH (2 x 3), SOLVENT (3), EXPLAIN (6); the paper prints (6) and (9).
_q2d = P.items(k('2', 'd'))
assert [it.cell for it in _q2d] == ['[2 × 3]', '[3]', '[6]'], _q2d
_which = [display(x).strip() for x in _q2d[0].text.split('//')]
assert _which[0] == 'B' and len(_which) == 2, _which
C.add([k('2', 'd')], 'chem-u2', 'purity-by-melting-point-and-recrystallisation', [
    lift('r-1', _which[0], 3, 'WHICH. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _which[1], 3, 'The justification.'),
    lift('r-3', _q2d[1].text, 3, 'SOLVENT.'),
    lift('r-4', _q2d[2].text, 6, 'EXPLAIN.')])
# (e): IDENTIFY (3) or STATE (6), "[Mark IDENTIFY and STATE independently and
# award the higher of the two marks.]": the flaw or the remedy for the first 3,
# the remedy again for the second.
_q2e = P.items(k('2', 'e'))
assert [it.cell for it in _q2e] == ['[3]', '[6]'] and len(_q2e[1].asides) == 2, _q2e
C.add([k('2', 'e')], 'chem-u2', 'a-fault-in-a-steam-distillation-apparatus', [
    menu_row('r-1', [_q2e[0].text, _q2e[1].text], 1, 'IDENTIFY, (3), or STATE, which the scheme prices (6) on its own: '
             'claim STATE here and again below. The scheme adds: ' + ' '.join(_q2e[1].asides), per=3, total=3),
    lift('r-2', _q2e[1].text, 3, 'STATE again, for the second (3).')], total=6, figure=FIG + 'paper-q2e')

# ── Q3 Heat of reaction of hydrochloric acid with sodium hydroxide ───────────
C.fixed([k('3', 'a')], 'chem-3-1', 'heat-of-reaction')
C.fixed([k('3', 'b')], 'chem-u2', 'an-insulating-reaction-vessel')
# (c): (i) and (ii) inside one sentence, priced (2 x 3), one each.
_q3c1, _q3c2 = P.items(k('3', 'c', 'i')), P.items(k('3', 'c', 'ii'))
assert [it.cell for it in _q3c1] == [None] and [it.cell for it in _q3c2] == ['[2 × 3]'], (_q3c1, _q3c2)
_adv, _adv_a = split_asides(display(_q3c1[0].text).rstrip('/ ').replace(' //', ''))
assert _adv.endswith('behind on sides)') and _adv_a == ['[not “easier to read”.]'], (_adv, _adv_a)
C.add([k('3', 'c')], 'chem-u2', 'a-burette-against-a-graduated-cylinder', [
    lift('r-1', _adv, 3, 'For (i). The scheme prices these points (2 × 3), one each. It adds: ' + _adv_a[0]),
    lift('r-2', _q3c2[0].text, 3, 'For (ii). The scheme adds: ' + ' '.join(_q3c2[0].asides))])
# (d): STATE, any two (2 x 3). The page prints "0.2°C" (page 8, x 323): its degree
# sign is a Cambria Math glyph (id 953) the text layer maps to a space.
_q3d = P.items(k('3', 'd'))
assert [it.cell for it in _q3d] == ['[2 × 3]'] and '[any two]' in _q3d[0].asides, _q3d
_ways = [display(x).strip() for x in _q3d[0].text.split('//')]
assert len(_ways) == 6 and 'reading to 0.2 C or better' in _ways[0], _ways
_ways[0] = _ways[0].replace('0.2 C', '0.2°C')
C.add([k('3', 'd')], 'chem-u2', 'measuring-the-temperature-rise-accurately', [
    menu_row('r-1', _ways, 2, 'Any two of these, (3) each: "' + raw(8, 275, 292, 460) + '".', per=3, total=6)], total=6)
# (e): HOW (3), CALC (9), HENCE (6) under one printed mark (18). The fractions in
# the scheme's boxes (page 8, y 335-576) are Cambria Math glyphs the text layer
# maps to spaces: its own print is shown with the answer.
_q3e = P.items(k('3', 'e'))
assert [it.cell for it in _q3e] == ['[3]', '[3]', '[9]', '[3]', '[3]', '[3]', '[6]', '[3]'], _q3e
assert [display(_q3e[i].text) for i in (0, 2, 6)] == ['0.075 mol HCl', '4.347 (4.35) kJ', '– 57.96 ( – 58) kJ'], _q3e
assert display(_q3e[4].text) == 'Temp rise: 20.9 – = 6.9 K' and display(_q3e[7].text) == '= – (3) 57.96', _q3e
C.add([k('3', 'e')], 'chem-3-1', 'heat-of-neutralisation-from-a-temperature-rise', [
    lift('r-1', _q3e[0].text, 3, 'HOW. The scheme works it in a box: 75 × 1 over 1000, set as a fraction, "= 0.075" '
         '(3).'),
    lift('r-2', _q3e[3].text, 3, 'CALC: the scheme gives the answer, 4.347 (4.35) kJ, priced (9), then three steps (3) '
         'each: the mass.'),
    lift('r-3', '6.9 K', 3, 'The temperature rise: the scheme prints "Temp rise: 20.9 –" (15.0+13.0) over 2, set as a '
         'fraction, "= 6.9 K".'),
    lift('r-4', _q3e[5].text, 3, 'The heat produced. The scheme adds: ' + ' '.join(_q3e[5].asides)),
    lift('r-5', _q3e[6].text, 6, 'HENCE: the scheme prints 4.347 over 0.075, set as a fraction, "= –" (3) "57.96" '
         '(3).')],
    figure=S + 'q3e')
# (f): IDENTIFY (6); DESCRIBE (3), the warning symbol drawn twice (page 8, x 129-189
# and 415-473) between "/" and its description; WHAT (3). "SECTION B", the next
# page's head, is read under (f): left out.
_q3f = P.items(k('3', 'f'))
assert [it.cell for it in _q3f] == ['[6]', '[3]', '[3]', None] and _q3f[3].text == 'SECTION B', _q3f
assert display(_q3f[1].text) == '/ test tube(s) dripping (pouring) onto surface / / cross', _q3f
C.add([k('3', 'f')], 'chem-4-3', 'the-hazard-of-concentrated-acid-and-base', [
    lift('r-1', _q3f[0].text, 6, 'IDENTIFY. The scheme adds: ' + ' '.join(_q3f[0].asides)),
    menu_row('r-2', ['test tube(s) dripping (pouring) onto surface', 'cross'], 1, 'DESCRIBE: one of these, or either '
             'symbol drawn as the scheme prints them beside these words, shown with the answer. The scheme adds: '
             + ' '.join(_q3f[1].asides), per=3, total=3),
    lift('r-3', _q3f[2].text, 3, 'WHAT. The scheme adds: ' + ' '.join(_q3f[2].asides))],
    total=12, figure=S + 'q3f')

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
# (a): WRITE (2 x 3); the notes under it set p's x, y and z as subscripts and
# the 2s as superscripts the text layer reads apart (scheme page 9, y 149-178).
_q4a = P.items(k('4', 'a'))
assert [it.cell for it in _q4a] == ['[2 × 3]', None], _q4a
_cfg = [display(x).strip() for x in _q4a[0].text.split('//')]
_acc = P.rearranged(raw(9, 149, 166), 'px 2py 2pz 2 for', 'px²py²pz² for')
_ar = traced('[Allow Ar instead of 1s²2s²2p⁶3s²3p⁶.]')
assert _cfg == ['1s²2s²2p⁶', '3s²3p⁶3d¹⁰4s² / 3s²3p⁶4s²3d¹⁰'] and \
    _acc == '[Accept px²py²pz² for p⁶. Allow with subscripts.]' and _ar in display(_q4a[1].text), (_cfg, _acc)
C.add([k('4', 'a')], 'chem-1-2', 'electron-configuration-of-zinc', [
    lift('r-1', _cfg[0], 3, 'The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _cfg[1], 3, 'The scheme adds: ' + _acc + ' ' + _ar + ' Its note allowing (3) for the p orbitals set '
         'with their subscripts and superscripts is in its own print, shown with the answer.')],
    notes=Q4_NOTE, figure=S + 'q4a')
C.fixed([k('4', 'b')], 'chem-1-2', 'relative-atomic-mass', notes=Q4_NOTE)
C.route([k('4', 'c')], 'chem-1-4', 'neutrons-in-a-mass-of-carbon-14', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-2-2', 'shape-and-bond-angle-of-a-group-4-hydride', notes=Q4_NOTE)
# (e): the answer (6); two steps (3) each, the first ending in fractions the text
# layer reads as spaces (scheme page 9, y 406-425).
_q4e = P.items(k('4', 'e'))
assert [it.cell for it in _q4e] == ['[6]', '[3]', '[3]'] and display(_q4e[0].text) == 'CuO', _q4e
_mass = 'mass of copper = 1.27 g; mass of oxygen = 1.59 – 1.27 = 0.32'
assert display(_q4e[1].text) == _mass + ' = 0.02; = 0.02' and display(_q4e[2].text) == '⇒ empirical formula = CuO', _q4e
C.add([k('4', 'e')], 'chem-1-4', 'empirical-formula-of-copper-oxide', [
    lift('r-1', _mass, 3, 'The scheme goes on: 1.27 over 63.5 "= 0.02;" 0.32 over 16 "= 0.02", set as fractions, '
         'and prices the step (3); its own print is shown with the answer.'),
    lift('r-2', _q4e[2].text, 3)], figure=S + 'q4e', notes=Q4_NOTE)
shown('The scheme gives the answer as "CuO" (6).')
_eq = 'FORMULAS: (3) BALANCING: (3)'
assert raw(9, 472, 490, 400) == _eq and raw(9, 700, 717, 400) == _eq and raw(9, 743, 760, 400) == _eq
_q4f = P.items(k('4', 'f'))
_na = display(_q4f[0].text)
assert [it.cell for it in _q4f] == ['[3]'] and _na.endswith(' (3) BALANCING:'), _q4f
C.add([k('4', 'f')], 'chem-4-2', 'sodium-and-ethanol', [
    lift('r-1', _na[:-len(' (3) BALANCING:')], 6, 'COMPLETE: "' + _eq + '". The scheme adds: '
         + ' '.join(_q4f[0].asides))], notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-u2', 'the-brown-ring-test-reagents', notes=Q4_NOTE)
# (h): STATE (2 x 3); the law in words, or as V over T* = k, or V1 over T1 = V2
# over T2, set as fractions (scheme page 9, y 552-572), or V ∝ T, or the
# expansion by 1/273: one of them, then the condition.
_q4h = P.items(k('4', 'h'))
_law = display(_q4h[0].text)
assert [it.cell for it in _q4h] == ['[2 × 3]'] and _law.startswith('volume varies directly with kelvin (absolute) '
                                                                   'temperature / = k / = / V ∝ T / gas expands'), _law
_ch, _cond = _law.split(' // ')
_ch = _ch.split(' / ')
_cond, _cap = split_asides(_cond)
assert _cond == 'for a definite mass of gas at constant pressure', _cond
C.add([k('4', 'h')], 'chem-2-3', 'charles-law', [
    menu_row('r-1', [_ch[0], _ch[3], _ch[4]], 1, 'One of these, (3), or the law as V over T* = k or V₁ over T₁ = '
             'V₂ over T₂, set as fractions; its own print is shown with the answer. The scheme prices these points '
             '(2 × 3), one each.', per=3, total=3),
    lift('r-2', _cond, 3, 'The scheme adds: ' + ' '.join(_cap))], total=6, notes=Q4_NOTE, figure=S + 'q4h')
C.fixed([k('4', 'i')], 'chem-4-3', 'secondary-sewage-treatment', notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-3-2', 'heterogeneous-catalysis', notes=Q4_NOTE)
for _alt, _concept, _topic in (('A', 'calcium-silicate-slag-in-steelmaking', 'chem-u3'),
                               ('B', 'forming-ozone-in-the-stratosphere', 'chem-4-3')):
    _its = P.items(ka('4', 'k', None, _alt))
    _w = display(_its[0].text)
    assert [it.cell for it in _its] == ['[3]'] and _w.endswith(' (3) BALANCING:'), _its
    _w, _wa = split_asides(_w[:-len(' (3) BALANCING:')])
    C.add([ka('4', 'k', None, _alt)], _topic, _concept, [
        lift('r-1', _w, 6, 'WRITE: "' + _eq + '".' + (' The scheme adds: ' + ' '.join(_wa) if _wa else ''))],
        notes=Q4_NOTE)

# ── Q5 Boyle, Bohr and the atom ──────────────────────────────────────────────
# (a): WHAT (5), two wordings on two lines (scheme page 10, y 73-101).
_q5a = P.items(k('5', 'a'))
assert [it.cell for it in _q5a] == ['[5]'] and len(_q5a[0].rows) == 3, _q5a
_el = [display(r.text) for r in _q5a[0].rows[:2]]
assert _el == ['an element cannot be broken (split, divided) into anything simpler*',
               'an element is a simple substance'], _el
C.add([k('5', 'a')], 'chem-1-1', 'boyles-idea-of-an-element', [
    menu_row('r-1', _el, 1, 'One of these wordings, the scheme setting the second on the line below the first. It '
             'adds: ' + ' '.join(_q5a[0].asides), per=5, total=5)], total=5, figure=FIG + 'paper-q5a')
# (b): USE any five (5 x 3), printed (15); EXPLAIN (2 x 3), printed (6); WHAT (3)
# and DESCRIBE (2 x 3), printed (9): a card each, cited with what it holds.
Q5B = P.ask(k('5', 'b'))
Q5B_BOHR, _r = cut(Q5B, 'Explain, in terms')
Q5B_FLAME, Q5B_LI = cut(_r, 'What colour')
assert Q5B_BOHR.endswith('of the hydrogen atom.') and Q5B_LI == ('What colour is observed in a flame test on lithium '
                                                                  'chloride? Describe the testing procedure.'), Q5B
_q5b = P.items(k('5', 'b'))
assert [it.cell for it in _q5b] == ['[5 × 3]', '[2 × 3]', '[3]', '[2 × 3]'] and '[any five]' in _q5b[0].asides, _q5b
_bohr = _q5b[0].options()
assert len(_bohr) == 6, _bohr
_five = raw(10, 330, 347, 460)
assert _five == 'ANY FIVE: (5 × 3)', _five
C.add([k('5', 'b')], 'chem-1-2', 'bohrs-theory-and-the-hydrogen-spectrum', [
    menu_row('r-1', _bohr, 5, 'USE: any five of these, (3) each: "' + _five + '". The scheme adds: '
             + ' '.join(a for a in _q5b[0].asides if not a.startswith('[any')), per=3, total=15)],
    total=15, qtext=Q5B_BOHR, cid='q5-b-bohr', ref_suffix='Bohr and the hydrogen spectrum')
_flame = [display(x).strip() for x in _q5b[1].text.split('//')]
assert len(_flame) == 2 and _flame[1].startswith('therefore they emit'), _flame
C.add([k('5', 'b')], 'chem-1-2', 'why-metals-give-different-flame-colours', [
    lift('r-1', _flame[0], 3, 'EXPLAIN. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _flame[1], 3)],
    qtext=Q5B_FLAME, stem=Q5B_BOHR, cid='q5-b-flame-colours', ref_suffix='different flame colours')
_test = [display(x).strip() for x in _q5b[3].text.split('//')]
assert len(_test) == 2 and _test[1].startswith('hold in'), _test
C.add([k('5', 'b')], 'chem-1-2', 'the-flame-test-for-lithium', [
    lift('r-1', _q5b[2].text, 3, 'WHAT.'),
    lift('r-2', _test[0], 3, 'DESCRIBE. The scheme prices these points (2 × 3), one each.'),
    lift('r-3', _test[1], 3, 'The scheme adds: ' + ' '.join(_q5b[3].asides))],
    qtext=Q5B_LI, stem=Q5B_FLAME, cid='q5-b-lithium', ref_suffix='lithium flame test')
# (c): EXPLAIN (2 x 3); GIVE any one (3); WHAT (2 x 3), two wordings, the second
# after "or". The paper underlines "uncertainty principle" (page 4, y 694):
# its own print is the question.
_q5c = P.items(k('5', 'c'))
assert [it.cell for it in _q5c] == ['[2 × 3]', '[3]', '[2 × 3]'] and '[any one]' in _q5c[1].asides, _q5c
_unc = [display(x).strip() for x in _q5c[0].text.split('//')]
# One answer of six, set with single solidi over three rows (page 10, y 620-673).
_give, _ornot = split_asides(display(_q5c[1].text))
_give = _give.split(' / ')
assert len(_unc) == 2 and len(_give) == 6 and _ornot == ['[Do not accept “orbitals.”]'], (_unc, _give)
_w1 = [display(x).strip() for x in raw(10, 682, 731, 120, 505).split(' // ')]
_w2 = [display(x).strip() for x in raw(10, 739, 756, 120, 500).split(' // ')]
assert raw(10, 726, 743) == 'or' and len(_w1) == 2 and _w2 == ['space occupied by electron',
                                                                'described by solution of Schrödinger equation'], _w1
_one = raw(10, 657, 674, 470)
assert _one == 'ANY ONE: (3)', _one
C.add([k('5', 'c')], 'chem-1-2', 'uncertainty-and-the-atomic-orbital', [
    lift('r-1', _unc[0], 3, 'EXPLAIN. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _unc[1], 3, 'The scheme adds: ' + ' '.join(_q5c[0].asides)),
    menu_row('r-3', _give, 1, 'GIVE: any one of these, (3): "' + _one + '". The scheme adds: ' + _ornot[0],
             per=3, total=3),
    menu_row('r-4', [_w1[0], _w2[0]], 1, 'WHAT: one of these wordings, the scheme setting the second after "or"; it '
             'prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-5', [_w1[1], _w2[1]], 1, 'And the second point of that same wording, (3).', per=3, total=3)],
    total=15)
print_question('paper-q5c-print')

# ── Q6 Octane numbers, ethyne and benzene ────────────────────────────────────
Q6B = FIG + 'paper-q6b'
C.fixed([k('6', 'a')], 'chem-2-4', 'octane-number')
# (b)(i): GIVE, A // B (2 x 3), each name after its letter (scheme page 11, y 170-204).
_q6b1 = P.items(k('6', 'b', 'i'))
assert [(it.cell, display(it.text)) for it in _q6b1] == [('[2 × 3]', 'A pentane // B 2-methylbutane')], _q6b1
C.add([k('6', 'b', 'i')], 'chem-2-4', 'naming-pentane-and-2-methylbutane', [
    lift('r-1', 'pentane', 3, 'For A. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', '2-methylbutane', 3, 'For B. The scheme adds: ' + ' '.join(_q6b1[0].asides))], figure=Q6B)
# (b)(ii): EXPLAIN (2 x 3); DRAW (3), three formulas and three drawings, one of
# them (scheme page 11, y 309-387); the note beside the drawings is quoted. The
# question needs the paper's A and B: its own print (the lead-in, the ask and
# the two structures, stacked) is the card's question.
_q6b2 = P.items(k('6', 'b', 'ii'))
assert [it.cell for it in _q6b2] == ['[2 × 3]', '[3]'], _q6b2
_iso = [display(x).strip() for x in _q6b2[0].text.split('//')]
_draw = [display(x).strip() for x in _q6b2[1].text.split('//') if x.strip()]
assert len(_iso) == 2 and _draw == ['C(CH₃)₄', '(CH₃)₃C(CH₃)', '(CH₃)₂C(CH₃)₂'], (_iso, _draw)
_isoa, _isob = split_asides(_iso[0]), split_asides(_iso[1])
_drawn = traced(raw(11, 326, 377, 400))
assert _drawn.startswith('In the fully expanded formula'), _drawn
C.add([k('6', 'b', 'ii')], 'chem-2-4', 'isomerisation-and-an-isomer-of-pentane', [
    lift('r-1', _iso[0], 3, 'EXPLAIN. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _iso[1], 3),
    menu_row('r-3', _draw, 1, 'DRAW: one of these, or the structure in full or as a skeleton, as the scheme draws them; '
             'its own print is shown with the answer. Beside the drawings: "' + _drawn + '"', per=3, total=3)],
    total=9, figure=S + 'q6b-ii')
print_question('paper-q6b-ii-print')
# (b)(iii): PREDICT and JUSTIFY, linked, (2 x 3).
_q6b3 = P.items(k('6', 'b', 'iii'))
_pj = display(_q6b3[0].text)
assert [it.cell for it in _q6b3] == ['[2 × 3]'] and _pj.startswith('B / 2-methylbutane // [Accept'), _q6b3
_pred, _just = _pj.split(' // ')
_just, _acc6 = split_asides(_just)
C.add([k('6', 'b', 'iii')], 'chem-2-4', 'branching-and-octane-number', [
    lift('r-1', _pred, 3, 'PREDICT. The scheme prices these points (2 × 3), one each, and adds: ' + ' '.join(_acc6)),
    lift('r-2', _just, 3, 'JUSTIFY. The scheme adds: ' + ' '.join(_q6b3[0].asides))], figure=Q6B)
# (c): the answer (15); five equations (3) each, then after "or" the sums of
# heats of formation. The paper's equation sets state symbols the text layer
# reads apart ("CaC₂ _((s))"): its own print is the question.
_q6c = P.items(k('6', 'c'))
assert [it.cell for it in _q6c] == ['[15]'] + ['[3]'] * 7, _q6c
_award = raw(11, 563, 580, 45)
assert _award == 'Equations not required. [Award (3) for 126.4 (+126.4) unless it can be seen to merit more.]', _award
C.route([k('6', 'c')], 'chem-3-1', 'heat-change-for-calcium-carbide-and-water', figure=S + 'q6c',
        notes='After "or" the scheme works it from the sums of heats of formation, four terms (3) each and the '
              'answer (3).')
shown('The scheme gives the answer as "– 126.4 kJ" (15). Under the equations it adds: "' + _award + '" After "or" '
      'it works it from the sums of heats of formation; its own print of both is shown with the answer.')
print_question('paper-q6c-print')
# (d): (i) (3) and (ii) (2 x 3) complete one sentence; a note in the scheme's
# right margin (page 11, x 483-574, y 666-761, crops 'q6d-margin') is quoted.
Q6D = P.ask(k('6', 'd')) + ' (i) ' + P.ask(k('6', 'd', 'i')) + ' (ii) ' + P.ask(k('6', 'd', 'ii'))
assert Q6D == ('Describe the structure of benzene in terms of (i) the bonding between the carbon atoms and the hydrogen '
               'atoms, (ii) the bonding between the carbon atoms.'), Q6D
_ring = traced(raw(11, 665, 762, 480))
assert _ring.startswith('If no marks have been awarded for part (d)'), _ring
C.fixed([k('6', 'd', 'i')], 'chem-2-1', 'bonding-between-carbon-and-hydrogen-in-benzene', qtext=Q6D, stem='',
        row_notes={0: 'For (i). Beside (d) the scheme notes: "' + _ring + '"'})
C.fixed([k('6', 'd', 'ii')], 'chem-2-1', 'bonding-between-the-carbons-of-benzene', qtext=Q6D, stem='',
        row_notes={0: 'For (ii).', 1: 'Beside (d) the scheme notes: "' + _ring + '"'})

# ── Q7 Rates of reaction ─────────────────────────────────────────────────────
# (a): DEFINE (5): two wordings, then after "/" a third set as a fraction the
# text layer reads as spaces (scheme page 12, y 82-104).
_q7a = P.items(k('7', 'a'))
_rate = display(_q7a[0].text)
assert [it.cell for it in _q7a] == ['[5]'] and _rate.endswith('rate of change of concentration /'), _q7a
C.add([k('7', 'a')], 'chem-3-2', 'rate-of-reaction', [
    lift('r-1', _rate.rstrip('/ '), 5, 'After "/" the scheme sets "change in concentration" over "time" as a fraction; '
         'its own print is shown with the answer.')], figure=S + 'q7a')
C.menu([k('7', 'b')], 'chem-3-2', 'ionic-reactions-in-solution-are-fast', note='"' + raw(12, 144, 162, 470) + '".')
# (c): SUGGEST any two (2 x 3), "ANY TWO:" set at the end of the answer's own
# line (scheme page 12, y 196); EXPLAIN any two (2 x 3), linked.
_q7c = P.items(k('7', 'c'))
_sug = display(_q7c[0].text)
assert [it.cell for it in _q7c] == ['[2 × 3]', '[2 × 3]'] and _sug.endswith(' ANY TWO:'), _q7c
_sug, _suga = split_asides(_sug[:-len(' ANY TWO:')])
_sug = [x.strip() for x in _sug.split('//')]
_exp = [display(x).strip() for x in _q7c[1].text.split('//')]
assert len(_sug) == 3 and [x.split(':')[0] for x in _exp] == ['pressure (concentration)', 'temperature', 'catalyst'], \
    (_sug, _exp)
C.add([k('7', 'c')], 'chem-3-2', 'speeding-up-the-ammonia-reaction', [
    menu_row('r-1', _sug, 2, 'SUGGEST: any two of these, (3) each: "' + raw(12, 194, 212, 120)[-len('ANY TWO: (2 × 3)'):]
             + '". The scheme adds: ' + ' '.join(_suga), per=3, total=6),
    menu_row('r-2', _exp, 2, 'EXPLAIN: the explanations of the two ways suggested, (3) each: "'
             + raw(12, 345, 362, 460) + '". The scheme adds: ' + _q7c[1].asides[1], per=3, total=6)], total=12)
# (d): DESCRIBE (3 x 3), three points; DESCRIBE (3 x 3), three points, the third
# with two forms set as fractions (scheme page 12, y 534-553). Six rows outrun a
# card: a card each, cited with what it holds.
Q7D_TIME, Q7D_PROP = cut(P.ask(k('7', 'd')), 'If you were given')
assert Q7D_TIME.endswith('Na₂S₂O₃ + 2HCl → 2NaCl + SO₂ + S + H₂O') and Q7D_PROP.endswith('thiosulfate solution.'), \
    (Q7D_TIME, Q7D_PROP)
_q7d = P.items(k('7', 'd'))
assert [it.cell for it in _q7d] == ['[3 × 3]', '[3 × 3]'], _q7d
_d1 = [split_asides(display(x).strip()) for x in _q7d[0].text.split('//')]
_d2 = [display(x).strip() for x in _q7d[1].text.split('//')]
assert len(_d1) == 3 and len(_d2) == 3 and _d2[2].endswith(' / = k / = k / plot of rate against concentration gives '
                                                             'a straight line through the origin (0, 0)'), (_d1, _d2)
C.add([k('7', 'd')], 'chem-3-2', 'timing-the-thiosulfate-reaction', [
    lift('r-1', _d1[0][0], 3, 'The scheme prices these points (3 × 3), one each.'),
    lift('r-2', _d1[1][0], 3),
    lift('r-3', _d1[2][0], 3, 'The scheme adds: ' + ' '.join(_d1[2][1] + _q7d[0].asides))],
    qtext=Q7D_TIME, cid='q7-d-time', ref_suffix='measuring the reaction time')
_const = _d2[2].split(' / ')
C.add([k('7', 'd')], 'chem-3-2', 'rate-proportional-to-thiosulfate-concentration', [
    lift('r-1', _d2[0], 3, 'The scheme prices these points (3 × 3), one each.'),
    lift('r-2', _d2[1], 3),
    menu_row('r-3', [_const[0], _const[3]], 1, 'One of these, (3), or "rate" over "conc" = k, or "conc" over "rate" = k, '
             'set as fractions; its own print is shown with the answer. The scheme adds: ' + ' '.join(_q7d[1].asides),
             per=3, total=3)],
    total=9, qtext=Q7D_PROP, stem=Q7D_TIME, figure=S + 'q7d', cid='q7-d-proportional',
    ref_suffix='rate proportional to concentration')
# (e): DRAW (3 x 3): the profile drawn (scheme page 12, x 163-262), its three
# points worded beside it, the paper setting (i) and (ii) inside the ask.
_e = [display(it.text) for key in (k('7', 'e'), k('7', 'e', 'i'), k('7', 'e', 'ii')) for it in P.items(key)]
assert _e == ['exothermic reaction shown //', 'activation energy (EA) //', 'heat of reaction (ΔH)',
              'The marks for (i) and (ii) may be given for an endothermic reaction diagram.'], _e
assert cells(k('7', 'e', 'ii')) == ['[3 × 3]', None], cells(k('7', 'e', 'ii'))
C.add([k('7', 'e')], 'chem-3-2', 'reaction-profile-of-an-exothermic-reaction', [
    lift('r-1', 'exothermic reaction shown', 3, 'The scheme prices these points (3 × 3), one each, beside its drawing, '
         'shown with the answer.'),
    lift('r-2', 'activation energy (EA)', 3, 'For (i).'),
    lift('r-3', 'heat of reaction (ΔH)', 3, 'For (ii). The scheme adds: "' + _e[3] + '"')],
    qtext=P.ask(k('7', 'e'), deep=True), figure=S + 'q7e')

# ── Q8 From ethene to PVC ────────────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
# (a): EXPLAIN any one (6); WHAT (3); HOW (2 x 3). The paper underlines
# "homologous series" (page 5, y 619): its own print, with the reaction scheme,
# is the question.
_q8a = P.items(k('8', 'a'))
assert [it.cell for it in _q8a] == ['[6]', '[3]', '[2 × 3]'] and '[any one]' in _q8a[0].asides, _q8a
_geo = [display(x).strip() for x in _q8a[2].text.split('//')]
assert len(_geo) == 2, _geo
C.add([k('8', 'a')], 'chem-2-4', 'homologous-series-and-adding-hydrogen-to-ethene', [
    menu_row('r-1', _q8a[0].options(), 1, 'EXPLAIN: any one of these, (6): "' + raw(13, 100, 118, 480) + '". The scheme '
             'adds: ' + _q8a[0].asides[0], per=6, total=6),
    lift('r-2', _q8a[1].text, 3, 'WHAT.'),
    lift('r-3', _geo[0], 3, 'HOW. The scheme prices these points (2 × 3), one each.'),
    lift('r-4', _geo[1], 3, 'The scheme adds: ' + ' '.join(_q8a[2].asides))], total=15)
print_question('paper-q8a-print')
# (b): IDENTIFY (3 x 3), the paper setting (i)-(iii) inside one line (page 5, y 722).
_q8b = [display(it.text) for r in ('i', 'ii', 'iii') for it in P.items(k('8', 'b', r))]
assert _q8b == ['chlorine (Cl₂) // [Do not accept Cl.]', 'hydrogen chloride (HCl) //',
                'chlorine (Cl₂) [Do not accept Cl.]'] and cells(k('8', 'b', 'iii')) == ['[3 × 3]'], _q8b
C.add([k('8', 'b')], 'chem-4-2', 'reagents-for-conversions-x-y-and-z', [
    lift('r-1', 'chlorine (Cl₂)', 3, 'For (i). The scheme prices these points (3 × 3), one each, and adds: '
         '[Do not accept Cl.]'),
    lift('r-2', 'hydrogen chloride (HCl)', 3, 'For (ii).'),
    lift('r-3', 'chlorine (Cl₂)', 3, 'For (iii). The scheme adds: [Do not accept Cl.]')],
    qtext=P.ask(k('8', 'b'), deep=True), figure=Q8)
# (c): DESCRIBE "ANY FOUR: (4 x 3)" (scheme page 13, y 449) over four points the
# scheme separates with "//" (y 259-463): the second offers, after "/" at the end
# of its row, the addition of Cl+ to the double bond; the third the chloronium
# ion and two drawings. Its examiner's notes follow (y 474-621).
_mech = [raw(13, 258, 279, 130), raw(13, 274, 295, 130), raw(13, 303, 323, 130), raw(13, 335, 355, 130),
         raw(13, 430, 451, 130) + ' ' + raw(13, 448, 464, 130, 440)]
assert _mech[0] == 'polarisation of chlorine molecule by double bond / (Clδ+–*Clδ–) // [*Line essential]' and \
    _mech[1].endswith('Cl₂ → Cl⁺ +*Cl¯ /') and _mech[2].endswith('to the double bond //') and \
    _mech[3].endswith('[*Accept positive carbon (C⁺).]') and _mech[4].endswith('to give 1,2-dichloroethane'), _mech
_four = raw(13, 448, 464, 440)
assert _four == 'ANY FOUR: (4 × 3)', _four
_polar, _line = split_asides(_mech[0])
_bond, _orient = (traced('[* Bond must not be shown.]'),
                         traced(raw(13, 318, 340, 130)))
_carb, _pos = split_asides(_mech[3])
_cancel, _curly, _hcl = raw(13, 472, 503, 130), raw(13, 510, 541, 130), raw(13, 592, 623, 130)
assert _cancel.startswith('[In each step') and _curly.endswith('curly arrows, e.g') and \
    _hcl.startswith('[If addition of HCl'), (_cancel, _curly, _hcl)
C.add([k('8', 'c')], 'chem-4-2', 'mechanism-of-adding-chlorine-to-ethene', [
    lift('r-1', _polar.rstrip('/ '), 3, 'The scheme prices four points "' + _four + '", one each. It adds: ' + _line[0]),
    menu_row('r-2', [_mech[1].rstrip('/ ').replace('Cl¯', 'Cl⁻'), _mech[2].rstrip('/ ')], 1, 'One of these, (3), the '
             'scheme setting the second after "/" on the row below. It adds: ' + _bond + ' ' + _orient, per=3,
             total=3),
    lift('r-3', _carb, 3, 'The scheme adds: ' + ' '.join(_pos) + ' and goes on "(chloronium ion) /", then two drawings '
         'of the ions, shown with the answer.'),
    lift('r-4', _mech[4], 3, 'The scheme adds: ' + _cancel + ' ' + _curly + ' (a drawing with curly arrows, shown with '
         'the answer) ] ' + _hcl)], total=12, figure=S + 'q8c')
print_question('paper-q8c-print')
# (d): DRAW (6), the formula or the structure drawn (scheme page 13, x 208-253);
# NAME (3). The question needs the paper's reaction scheme: its own print is
# the question.
_q8d = P.items(k('8', 'd'))
assert [(it.cell, display(it.text)) for it in _q8d][0] == ('[6]', 'CH₂ = CHCl /') and cells(k('8', 'd')) == \
    ['[6]', '[3]'], _q8d
C.add([k('8', 'd')], 'chem-4-2', 'chloroethene', [
    lift('r-1', 'CH₂ = CHCl', 6, 'DRAW: or the structure as the scheme draws it after "/", shown with the answer.'),
    lift('r-2', _q8d[1].text, 3, 'NAME.')], figure=S + 'q8d')
print_question('paper-q8d-print')
_q8e = P.items(k('8', 'e'))
assert [(it.cell, display(it.text)) for it in _q8e] == [('[5]', '/ – CH₂ – CHCl – CH₂ – CHCl –')], _q8e
C.add([k('8', 'e')], 'chem-4-2', 'repeating-units-of-pvc', [
    lift('r-1', '– CH₂ – CHCl – CH₂ – CHCl –', 5, 'Or the two units drawn in full, as the scheme draws them before "/", '
         'shown with the answer. It adds: ' + ' '.join(_q8e[0].asides))], figure=S + 'q8e')

# ── Q9 The iron(III) thiocyanate equilibrium ─────────────────────────────────
Q9 = FIG + 'paper-q9b'
# (a): WHAT (5) and WHY (3), printed (8); STATE (2 x 3), printed (6): a card each.
Q9A_EQ, Q9A_LC = cut(P.ask(k('9', 'a')), 'State Le')
assert Q9A_LC == 'State Le Châtelier’s principle.', Q9A_LC
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a] == ['[5]', '[3]', '[2 × 3]'], _q9a
_lc = [display(x).strip() for x in _q9a[2].text.split('//')]
C.add([k('9', 'a')], 'chem-3-3', 'dynamic-chemical-equilibrium', [
    lift('r-1', _q9a[0].text, 5, 'WHAT.'), lift('r-2', _q9a[1].text, 3, 'WHY.')],
    qtext=Q9A_EQ, stem='', cid='q9-a-equilibrium', ref_suffix='chemical equilibrium')
C.add([k('9', 'a')], 'chem-3-3', 'le-chateliers-principle', [
    lift('r-1', _lc[0], 3, 'STATE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _lc[1], 3, 'The scheme adds: ' + ' '.join(_q9a[2].asides))],
    qtext=Q9A_LC, stem='', cid='q9-a-le-chatelier', ref_suffix='Le Châtelier’s principle')
# (b): the equation's arrow and its colours are printed (page 6, y 124-152) in a
# form the text layer does not carry: the paper's print of it is the figure.
# (i) (2 x 3) and (ii) (3) complete the sentence "Explain".
Q9B = P.ask(k('9', 'b'))
assert Q9B.endswith('the following equilibrium was established:') and P.lead(k('9', 'b')) == 'Explain', Q9B
Q9B_SENT = 'Explain (i) ' + P.ask(k('9', 'b', 'i')) + ' (ii) ' + P.ask(k('9', 'b', 'ii'))
assert Q9B_SENT.endswith('(ii) why changing the pressure has no effect on this equilibrium.'), Q9B_SENT
_q9b1 = P.items(k('9', 'b', 'i'))
_dec = [display(x).strip() for x in _q9b1[0].text.split('//')]
assert [it.cell for it in _q9b1] == ['[2 × 3]'] and _dec[0] == 'decrease' and len(_dec) == 2, _q9b1
C.add([k('9', 'b', 'i')], 'chem-3-3', 'adding-thiocyanate-to-the-equilibrium', [
    lift('r-1', _dec[0], 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _dec[1].replace('CNS¯', 'CNS⁻'), 3, 'The scheme adds: ' + ' '.join(_q9b1[0].asides))],
    qtext=Q9B_SENT, stem=Q9B, figure=Q9)
C.fixed([k('9', 'b', 'ii')], 'chem-3-3', 'pressure-and-an-equilibrium-in-solution', qtext=Q9B_SENT, stem=Q9B,
        figure=Q9, row_notes={0: 'For (ii).'})
# (c): WRITE (6), printed (6): the scheme sets the expression as a fraction the
# text layer reads as spaces (scheme page 14, y 405-445), so the row is the
# paper's ask and the scheme's print its answer. CALCULATE (12), printed (12):
# the answer, then a table and four steps (3) each. Both need the paper's
# equation: their own print (the equation, then the part) is the question.
Q9C_WRITE, Q9C_CALC = cut(P.ask(k('9', 'c')), 'A mixture')
assert Q9C_WRITE == 'Write the equilibrium constant (Kc) expression for this reaction.', Q9C_WRITE
Q9C_CALC = P.rearranged(P.rearranged(Q9C_CALC, '10⁻3 moles', '10⁻³ moles'), '10⁻4 moles', '10⁻⁴ moles')
_q9c = P.items(k('9', 'c'))
assert [it.cell for it in _q9c] == ['[6]', '[12]', '[3]', '[3]', '[3]', '[3]'] and display(_q9c[0].text) == '' and \
    display(_q9c[1].text) == '138.87 (138.9, 139) M⁻¹', _q9c
C.add([k('9', 'c')], 'chem-3-3', 'kc-expression-for-iron-iii-thiocyanate', [
    C.mark_ask(point('r-1', Q9C_WRITE, 6, 'The scheme answers with the expression set as a fraction, shown with the '
                    'answer, and adds: ' + ' '.join(_q9c[0].asides)))],
    qtext=Q9C_WRITE, stem=Q9B, figure=S + 'q9c-write', cid='q9-c-expression', ref_suffix='Kc expression')
print_question('paper-q9c-write-print')
_eqm = raw(14, 538, 557, 85)
assert _eqm == 'Equil (M) 8.9 × 10⁻⁴ (3) Ms the same (3) 1.1 × 10⁻⁴ mol', _eqm
_inc = raw(14, 565, 597, 300, 470)
assert _inc == '[Accept correct use of an incorrect Kc expression from (c) WRITE.]', _inc
C.add([k('9', 'c')], 'chem-3-3', 'calculating-kc-for-iron-iii-thiocyanate', [
    lift('r-1', '8.9 × 10⁻⁴', 3, 'The scheme sets out a table, its row "' + _eqm + '": the equilibrium value under '
         'Fe³⁺, (3).'),
    lift('r-2', 'Ms the same', 3, 'The equilibrium value under CNS⁻, (3).'),
    lift('r-3', '138.87 (138.9, 139)', 6, 'The scheme prints Kc = 1.1 × 10⁻⁴ over (8.9 × 10⁻⁴)², set as a fraction, '
         'and prices it (3), then "= 138.87 (138.9, 139)" (3). It adds: ' + traced(_inc))],
    qtext=Q9C_CALC, stem=Q9C_WRITE, figure=S + 'q9c', cid='q9-c-calculation', ref_suffix='Kc calculated',
    notes='The scheme gives the answer, 138.87 (138.9, 139) M⁻¹, priced (12), then four steps (3) each.')
shown('The scheme gives the answer as "138.87 (138.9, 139) M⁻¹" (12); its own print of the table and working is shown '
      'with the answer.')
print_question('paper-q9c-calc-print')
C.fixed([k('9', 'd')], 'chem-3-3', 'cooling-the-equilibrium-and-kc', stem=Q9B, figure=Q9,
        row_notes={0: 'STATE.', 1: 'IS.', 2: 'JUSTIFY.'})

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): DISTINGUISH, two points priced (4 + 3); (i) (6); (ii) and (iii) (2 x 3).
Q10A, Q10A_LEAD = P.ask(k('10', 'a')), P.lead(k('10', 'a'))
assert Q10A_LEAD == 'Explain each of the following in terms of intramolecular bonding or intermolecular forces or both.'
C.ordered([k('10', 'a')], 'chem-2-2', 'intramolecular-bonding-and-intermolecular-forces', stem='')
_q10a1 = P.items(k('10', 'a', 'i'))
assert [it.cell for it in _q10a1] == ['[6]'], _q10a1
C.add([k('10', 'a', 'i')], 'chem-2-2', 'boiling-points-of-hydrogen-and-oxygen', [
    lift('r-1', _q10a1[0].text, 6, 'The scheme adds: ' + ' '.join(_q10a1[0].asides))], stem=Q10A_LEAD)
C.fixed([k('10', 'a', 'ii')], 'chem-2-2', 'iodine-barely-dissolving-in-water', stem=Q10A_LEAD)
C.fixed([k('10', 'a', 'iii')], 'chem-2-2', 'a-charged-rod-deflecting-water', stem=Q10A_LEAD)
# (b)(i): DEFINE (3); SHOW (2 x 3), the scheme reprinting the equation, then for
# Al "increased (oxidised) // 0 to +3 (3)" or for Fe "decreased (reduced) //
# +2⅔ (2⅔)* to 0" (scheme page 15, y 383), the bracketed numbers each the same
# number without its sign; IDENTIFY (3).
Q10B = C.context(k('10', 'b', 'i'))
assert Q10B.endswith('sections of railway track: 8Al + 3Fe₃O₄ → 4Al₂O₃ + 9Fe'), Q10B
_q10b1 = P.items(k('10', 'b', 'i'))
assert [it.cell for it in _q10b1] == ['[3]', '[2 × 3]', '[3]'], _q10b1
_show = raw(15, 382, 399, 140)
assert _show == 'Al increased (oxidised) // 0 to +3 (3) / Fe decreased (reduced) // +2⅔ (2⅔)* to 0', _show
_al, _fe = [x.split(' // ') for x in _show.split(' (3) / ')]
_al[1] += ' (3)'
_sh_a = raw(15, 397, 415, 140, 500) + ' ' + raw(15, 413, 430, 140)
assert _sh_a == '[Accept Fe₃O₄ for Fe.] [*Accept 3 or 2.] [Change in oxidation numbers must be shown in some form.]', _sh_a
C.add([k('10', 'b', 'i')], 'chem-3-5', 'the-thermit-reaction-as-a-redox-reaction', [
    lift('r-1', _q10b1[0].text, 3, 'DEFINE.'),
    menu_row('r-2', [_al[0], _fe[0]], 1, 'SHOW: the change for aluminium or for iron, the scheme reprinting the equation '
             'above them and setting the second after "/"; it prices the two points of each (2 × 3), one each.',
             per=3, total=3),
    menu_row('r-3', [_al[1], _fe[1]], 1, 'And the oxidation numbers of that same element, (3). The scheme adds: '
             + _sh_a, per=3, total=3),
    lift('r-4', _q10b1[2].text, 3, 'IDENTIFY.')], total=12, stem=Q10B)
# (ii): WHAT (9), three steps (3) each, and WHAT (4), two steps (2) each, in
# boxes (scheme page 15, y 479-543); a note in the right margin (x 494-570,
# crops 'q10b-ii-margin') is quoted.
_q10b2 = P.items(k('10', 'b', 'ii'))
assert [(it.cell, display(it.text)) for it in _q10b2] == [
    ('[9]', '432 g'), ('[3]', '1008 g Fe ÷ 56 = 18 mol'), ('[3]', '≡ 16 mol Al (3) × 27 = 432 g'), ('[4]', '816 g'),
    ('[2]', '16 mol Al ≡ 8 mol Al₂O₃ (2) × 102 = 816 g')], _q10b2
_ratio = traced(raw(15, 476, 552, 490))
assert _ratio == 'Marks may be awarded to candidates for use of correct ratio of masses based on Mr.', _ratio
C.add([k('10', 'b', 'ii')], 'chem-1-4', 'masses-of-aluminium-and-its-oxide-in-the-thermit-weld', [
    lift('r-1', '1008 g Fe ÷ 56 = 18 mol', 3, 'WHAT: the scheme gives the answer, 432 g, priced (9), then three steps '
         '(3) each. Beside the boxes it notes: "' + _ratio + '"'),
    lift('r-2', '≡ 16 mol Al', 3),
    lift('r-3', '× 27 = 432 g', 3),
    lift('r-4', '16 mol Al ≡ 8 mol Al₂O₃', 2, 'WHAT: the scheme gives the answer, 816 g, priced (4), then two steps (2) '
         'each.'),
    lift('r-5', '× 102 = 816 g', 2)], stem=Q10B, figure=S + 'q10b-ii')
# (c): (i) DEFINE (6), two wordings, the second after "or"; (ii) and (iii) GIVE any
# two (2 x 3), "ANY TWO:" set at the end of the last answer row; (iv) WHAT (7),
# whose answer prints above its cue (scheme page 16, y 349) and is read under (iii).
Q10C = C.context(k('10', 'c', 'i'))
assert Q10C.startswith('Caesium–137 is a radioactive isotope') and Q10C.endswith('half-life of 30 days.'), Q10C
_q10c1 = P.items(k('10', 'c', 'i'))
_rad = [raw(16, 47, 77, 140), raw(16, 85, 115, 140, 520)]
assert raw(16, 72, 90, 140) == 'or' and [it.cell for it in _q10c1] == ['[6]'] and _rad[1].endswith('a nucleus*'), _rad
C.add([k('10', 'c', 'i')], 'chem-1-2', 'radioactivity', [
    menu_row('r-1', _rad, 1, 'One of these wordings, the scheme setting the second after "or". It adds: '
             + ' '.join(_q10c1[0].asides), per=6, total=6)], total=6, stem=Q10C)
_chem = raw(16, 139, 181, 140).split(' // ')
_nuc = raw(16, 181, 222, 140).split(' // ')
assert _chem[0].startswith('chemical: ') and _nuc[0].startswith('nuclear: ') and len(_chem) == len(_nuc) == 6, \
    (_chem, _nuc)
_chem[0], _nuc[0] = _chem[0][len('chemical: '):], _nuc[0][len('nuclear: '):]
_pt = raw(16, 222, 238, 140)
assert _pt == '[Point given for chemical, assume opposite for nuclear, & vice versa.] ANY TWO: (2 × 3)', _pt
C.add([k('10', 'c', 'ii')], 'chem-1-2', 'chemical-and-nuclear-reactions-compared', [
    menu_row('r-1', _chem + _nuc, 2, 'Any two of these, (3) each: "ANY TWO: (2 × 3)". The first six are the scheme\'s '
             'for chemical reactions ("chemical:"), the last six for nuclear ("nuclear:"). It adds: '
             + _pt[:-len(' ANY TWO: (2 × 3)')], per=3, total=6)], total=6, stem=Q10C)
_beta = raw(16, 247, 340, 140)
assert _beta.endswith(' [*Allow “positive” but only if positron is mentioned.]ANY TWO: (2 × 3)'), _beta
_beta, _pos = split_asides(_beta[:-len('ANY TWO: (2 × 3)')])
_beta = _beta.split(' // ')
assert len(_beta) == 9, _beta
C.add([k('10', 'c', 'iii')], 'chem-1-2', 'properties-of-beta-particles', [
    menu_row('r-1', _beta, 2, 'Any two of these, (3) each: "ANY TWO: (2 × 3)". The scheme adds: ' + ' '.join(_pos),
             per=3, total=6)], total=6, stem=Q10C)
_eighth = raw(16, 348, 371, 140, 400)
_acc10 = raw(16, 370, 390, 140)
assert _eighth == 'one-eighth / ⅛ / 0.125 / 12.5%' and _acc10 == '[Accept 0.994 or 99.4% or (7)]', (_eighth, _acc10)
assert cells(k('10', 'c', 'iv')) == ['[7]', None], cells(k('10', 'c', 'iv'))
C.add([k('10', 'c', 'iv')], 'chem-1-2', 'fraction-of-caesium-137-left-after-three-half-lives', [
    lift('r-1', _eighth, 7, 'The scheme adds: "[Accept 0.994 or 99.4% or" 994 over 1000, set as a fraction, "(7)]".')],
    stem=Q10C)

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q11A_LEAD = P.lead(k('11', 'a'))
assert Q11A_LEAD.startswith('The graph shows the first ionisation energy values'), Q11A_LEAD
Q11A = FIG + 'paper-q11a'
C.ordered([k('11', 'a')], 'chem-1-3', 'first-ionisation-energy', stem='')
_q11a1 = P.items(k('11', 'a', 'i'))
assert [(it.cell, display(it.text)) for it in _q11a1] == [('[2 × 3]', 'B is helium // P is sulfur (sulphur)'),
                                                          ('[3]', '900')], _q11a1
# The graph's letters each question names are decoded by the scheme's own answer
# ("B is helium", "R (argon)", "H (oxygen)"): its label key, asked in the question.


def asked(text, *letters):
    out = []
    for letter in letters:
        m = re.search(r'\b' + letter + r' (?:is |\()(\w+(?: \(\w+\))?)', text)
        assert m, (letter, text)
        out.append({'letter': letter, 'meaning': m.group(1), 'askedInThisQuestion': True})
    return out


C.add([k('11', 'a', 'i')], 'chem-1-3', 'reading-elements-and-a-value-off-the-graph', [
    lift('r-1', 'B is helium', 3, 'DEDUCE. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'P is sulfur (sulphur)', 3),
    lift('r-3', '900', 3, 'WHAT.')], stem=Q11A_LEAD, figure=Q11A,
    label_key=asked(display(_q11a1[0].text), 'B', 'P'))
_q11a2 = display(P.items(k('11', 'a', 'ii'))[0].text)
C.fixed([k('11', 'a', 'ii')], 'chem-1-3', 'the-drop-from-argon-to-potassium', stem=Q11A_LEAD, figure=Q11A,
        label_key=asked(_q11a2, 'R', 'S'))
# (iii): EXPLAIN (2 x 3): the first point, then the reason for H or, set below it,
# for G; each prints the 2p orbitals as boxes after "or 2p" (scheme page 17,
# x 317-371 and 478-531), and its subscripts and superscripts read apart. The
# question needs the paper's graph: its own print is the question.
_q11a3 = P.items(k('11', 'a', 'iii'))
assert [it.cell for it in _q11a3] == ['[2 × 3]'], _q11a3
_half = raw(17, 293, 323, 150)
_h = P.rearranged(raw(17, 328, 389, 150), '2px 22py 12pz 1 or', '2px²2py¹2pz¹ or')
_g = P.rearranged(raw(17, 397, 439, 150, 550), '2px 12py 12pz 1 or', '2px¹2py¹2pz¹ or')
assert _half.endswith('unstable //') and _h.endswith('or 2p⁴ or 2p / loss of electron from H gives half-full 2p') \
    and _g.endswith('or 2p³ or 2p / half-full 2p-sublevel /'), (_half, _h, _g)
C.add([k('11', 'a', 'iii')], 'chem-1-3', 'ionisation-energies-of-oxygen-and-nitrogen', [
    lift('r-1', _half.rstrip('/ '), 3, 'The scheme prices these points (2 × 3), one each.'),
    menu_row('r-2', [_h, _g.rstrip('/ ')], 1, 'The reason for H, or, set below it, for G, (3); each draws the 2p orbitals '
             'as boxes after "or 2p", shown with the answer.', per=3, total=3)], total=6, figure=S + 'q11a-iii',
    stem=Q11A_LEAD, label_key=asked(_h + ' ' + _g, 'H', 'G'))
print_question('paper-q11a-iii-print')
# (b): DEFINE (i) and (ii) (4 + 3), printed (7); GIVE (i) // (ii) (2 x 3), printed
# (6); CALCULATE (12), printed (12): a card each. The scheme's (i) and (ii) under
# DEFINE and again under GIVE are read as one run (page 17, y 467-538): its own
# lines are read here.
Q11B = P.ask(k('11', 'b'))
Q11B_DEF, _r = cut(Q11B, 'Give (i)')
Q11B_GIVE, _r = cut(_r, 'Ammonium hydroxide')
Q11B_GIVE = P.rearranged(Q11B_GIVE, 'HPO₄ 2–.', 'HPO₄²⁻.')
assert Q11B_DEF == 'Define a base according to (i) the Arrhenius theory, (ii) the Brønsted-Lowry theory.' and \
    Q11B_GIVE == 'Give (i) the conjugate acid, (ii) the conjugate base, of HPO₄²⁻.', (Q11B_DEF, Q11B_GIVE)
_arr = raw(17, 466, 497, 150)
_bl = raw(17, 497, 515, 150, 500)
assert _arr.endswith('in aqueous solution (water) //') and _bl == 'Brønsted-Lowry: proton (hydrogen ion, H⁺) acceptor' \
    and raw(17, 497, 515, 500) == '(4 + 3)', (_arr, _bl)
C.add([k('11', 'b')], 'chem-3-4', 'arrhenius-and-bronsted-lowry-bases', [
    lift('r-1', _arr.rstrip('/ ').replace('(OH¯)', '(OH⁻)'), None, 'For (i).'),
    lift('r-2', _bl, None, 'For (ii).')], kind='orderedSplit', notation='[4 + 3]', total=7,
    notes=SPLIT.format('[4 + 3]'), qtext=Q11B_DEF, stem='', cid='q11-b-bases', ref_suffix='bases defined')
# (The text layer reads GIVE's row "(i) H₂PO₄⁻ // (ii) PO₄³⁻" with the charge first, its
# runs starting 6 points apart: "– // (ii) PO₄ 3–" (x 190, y 515) before "H₂PO₄" (x 156, y 521).)
assert raw(17, 513, 540, 150, 300) == '– // (ii) PO₄ 3– H₂PO₄', raw(17, 513, 540, 150, 300)
C.add([k('11', 'b')], 'chem-3-4', 'conjugate-acid-and-base-of-hydrogenphosphate', [
    lift('r-1', 'H₂PO₄⁻', 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', 'PO₄³⁻', 3, 'For (ii).')], qtext=Q11B_GIVE, stem='', cid='q11-b-conjugates',
    ref_suffix='conjugate acid and base')
Q11B_CALC = _r
assert Q11B_CALC.startswith('Ammonium hydroxide (NH₄OH)') and Q11B_CALC.endswith('is 1.8 × 10⁻⁵.'), Q11B_CALC
_ph = [display(it.text) for it in P.items(k('11', 'b', 'i'))]
assert _ph[1:] == ['11.28 (11.3)', '7 g of NH₄OH = 7 ÷ 35 = 0.2 mol 0.2 M NH₄OH', '[OH¯] = / 1.9 × 10⁻³',
                   'pOH = – log 1.9 × 10⁻³ = 2.72 (2.7)', 'pH = 14 – 2.72 (2.7) = 11.28 (11.3)',
                   '[OH¯] = / 1.9 × 10⁻³', '[H⁺] = 5.3 × 10⁻¹²', 'pH = – log 5.3 × 10⁻¹² = 11.28 (11.3)'], _ph
# The page prints "0.2 mol ⇒ 0.2 M" (scheme page 17, x 330): the arrow is a Cambria Math glyph
# (id 1436) the text layer maps to a space.
_nh4 = _ph[2].replace('0.2 mol 0.2 M', '0.2 mol ⇒ 0.2 M')
assert _nh4 != _ph[2], _ph[2]
C.add([k('11', 'b')], 'chem-3-4', 'ph-of-ammonium-hydroxide', [
    lift('r-1', _nh4, 3, 'The scheme gives the answer, 11.28 (11.3), priced (12), then two routes in one box, four '
         'steps (3) each, the first step shared; its own print is shown with the answer.'),
    lift('r-2', '1.9 × 10⁻³', 3, 'The scheme prints "[OH⁻] =" the square root of 1.8 × 10⁻⁵ × 0.2, a root sign drawn '
         'over it, "/ 1.9 × 10⁻³".'),
    menu_row('r-3', [_ph[4], '5.3 × 10⁻¹²'], 1, 'Then pOH, or, in the second route, "[H⁺] =" 1 × 10⁻¹⁴ over that square '
             'root or over 1.9 × 10⁻³, set as fractions, "/ 5.3 × 10⁻¹²", (3).', per=3, total=3),
    menu_row('r-4', [_ph[5], _ph[8]], 1, 'And the pH by that same route, (3).', per=3, total=3)],
    total=12, qtext=Q11B_CALC, stem='', figure=S + 'q11b', cid='q11-b-ph', ref_suffix='pH of ammonium hydroxide')
# (c)A: electrolysis of molten lead bromide; the diagram's labels ("A", "PbBr₂")
# are the picture's (crops 'paper-q11c-a').
Q11CA = FIG + 'paper-q11c-a'
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-3-5', 'electrolysis', figure=Q11CA)
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-3-5', 'why-the-lead-bromide-must-be-molten', figure=Q11CA)
C.fixed([ka('11', 'c', 'iii', 'A')], 'chem-3-5', 'inert-electrodes', figure=Q11CA)
_a4 = P.items(ka('11', 'c', 'iv', 'A'))
_br2 = display(_a4[1].text)
assert [it.cell for it in _a4] == ['[3]', '[3]'] and _br2.endswith(' (3) BALANCING:') and raw(18, 210, 228, 400) == _eq, \
    _a4
C.add([ka('11', 'c', 'iv', 'A')], 'chem-3-5', 'electrode-reactions-in-molten-lead-bromide', [
    lift('r-1', _a4[0].text, 3),
    menu_row('r-2', _br2[:-len(' (3) BALANCING:')].split(' / '), 1, 'One of these, (6): "' + _eq + '".', per=6,
             total=6)], total=9, figure=Q11CA)
_a5 = P.items(ka('11', 'c', 'v', 'A'))
_name = [display(x).strip() for x in _a5[0].text.split('//')]
_name1, _na1 = split_asides(_name[1])
assert [it.cell for it in _a5] == ['[2 × 3]', None] and _name[0] == 'sodium / aluminium' and \
    _name1 == 'sodium from sodium chloride / aluminium from aluminium oxide (alumina)*', _a5
C.add([ka('11', 'c', 'v', 'A')], 'chem-3-5', 'metals-extracted-by-electrolysis', [
    lift('r-1', _name[0], 3, 'NAME. The scheme prices these points (2 × 3), one each. It adds: ' + ' '.join(_na1)),
    lift('r-2', _name1, 3, 'NAME. The scheme adds: ' + display(_a5[1].text) + ' ' + ' '.join(_a5[1].asides))],
    figure=Q11CA)
# (c)B: the chemical industry.
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-u3', 'feedstock-and-raw-materials')
# (ii): two points (2 x 3), or the scheme's second pair inside "[Or accept: ...]".
_b2 = P.items(ka('11', 'c', 'ii', 'B'))
_fixed = [display(x).strip() for x in _b2[0].text.split('//')]
_or = _b2[0].asides[0]
assert [it.cell for it in _b2] == ['[2 × 3]'] and _or.startswith('[Or accept: variable costs // as wages') and \
    _or.endswith('workers on different contracts (2 × 3)]'), _b2
_var = [x.strip() for x in _or[len('[Or accept: '):-len(' (2 × 3)]')].split(' // ')]
C.add([ka('11', 'c', 'ii', 'B')], 'chem-u3', 'labour-as-a-fixed-cost', [
    menu_row('r-1', [_fixed[0], _var[0]], 1, 'One of these, (3), the scheme accepting the second in a note: "[Or '
             'accept: ...]"; it prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_fixed[1], _var[1]], 1, 'And the reason that goes with it, (3).', per=3, total=3)], total=6)
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-u3', 'glass-and-steel-reaction-vessels')
# (iv): GIVE (2 x 3), one advantage of each, a list one to a row (scheme page 18,
# y 516-664).
_rows = lambda y0, y1: [display(l.text) for l in _RAW if l.page == 18 and y0 <= l.y0 < y1 and 150 < l.x0 < 500]
_batch = [t.rstrip('/ ') for t in _rows(515, 608)]
_cont = [t.rstrip('/ ') for t in _rows(609, 664)]
assert _batch[0].startswith('batch: ') and _cont[0].startswith('contin: ') and len(_batch) == 7 and len(_cont) == 4, \
    (_batch, _cont)
_batch[0], _cont[0] = _batch[0][len('batch: '):], _cont[0][len('contin: '):]
C.add([ka('11', 'c', 'iv', 'B')], 'chem-u3', 'batch-and-continuous-processes', [
    menu_row('r-1', _batch, 1, 'One advantage of a batch process ("batch:"), (3). The scheme prices these points '
             '(2 × 3), one each.', per=3, total=3),
    menu_row('r-2', _cont, 1, 'One advantage of a continuous process ("contin:"), (3).', per=3, total=3)],
    total=6, qtext=cut(P.ask(ka('11', 'c', 'iv', 'B')), 'Select one')[0])
# After (iv): GIVE (4), one reason for the site of the industry chosen: the
# scheme lists them industry by industry (page 18, y 674-777), some in more than
# one list. The paper sets the industries and sites as a table (page 7, y
# 751-776): its own print is the question.
_b4 = P.items(ka('11', 'c', 'iv', 'B'))
assert [it.cell for it in _b4] == ['[2 × 3]', '[4]', None] and _b4[2].text == 'Blank Page', _b4
_site = {}
for _ind, (y0, y1) in (('ammonia', (673, 704)), ('nitric acid', (704, 735)), ('periclase', (735, 779))):
    _t = tidy(' '.join(_rows(y0, y1)))
    _site[_ind] = [x.strip() for x in re.split(r'\s*/\s*', _t) if x.strip()]
assert len(_site['ammonia']) == 5 and len(_site['nitric acid']) == 5 and len(_site['periclase']) == 8, _site
_reasons = list(dict.fromkeys(_site['ammonia'] + _site['nitric acid'] + _site['periclase']))
assert len(_reasons) == 12, _reasons
C.add([ka('11', 'c', 'iv', 'B')], 'chem-u3', 'why-an-irish-chemical-plant-was-sited-where-it-was', [
    menu_row('r-1', _reasons, 1, 'One reason, (4), for the industry chosen. The scheme lists, "ammonia:" '
             + ' / '.join(_site['ammonia']) + '; "nitric acid:" ' + ' / '.join(_site['nitric acid'])
             + '; "periclase:" ' + ' / '.join(_site['periclase']) + '.', per=4, total=4)],
    total=4, qtext=cut(P.ask(ka('11', 'c', 'iv', 'B')), 'Select one')[1], cid='q11-c-b-site',
    ref_suffix='after (iv), why the process is where it is')
print_question('paper-q11c-b-iv-print')


# A script run the text layer sets apart from the bracket that closes it
# ("(FeSO₄ )", "[H⁺ ]") or from its number ("2 nd") is shown as the page sets it;
# the gate reads both alike (spaces fold away), checked again here.
_SPACED = [(re.compile(r'([₀-₉⁰-⁹¹²³⁺⁻]|\dth|\bMr) ([)\]])'), r'\1\2'), (re.compile(r'(\d) (st|nd|th)\b'), r'\1\2')]


def _closed(t):
    for rx, rep in _SPACED:
        t = rx.sub(rep, t)
    if not P.traceable(t):
        raise Refused(f'"{t}" is not in the 2013 hl scheme')
    return t


for _c in C.cards:
    for _r in _c['rows']:
        if not _r.get('ask'):
            _r['verbatim'] = _closed(_r['verbatim'])
        if _r.get('group'):
            _r['group']['options'] = [_closed(o) for o in _r['group']['options']]


# A note quoted from the scheme in the reader's script notation ("K_(c)") is
# shown as the page sets it.
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'], _r


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
