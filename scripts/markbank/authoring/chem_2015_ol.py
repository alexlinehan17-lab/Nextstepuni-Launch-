#!/usr/bin/env python3
"""2015 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2015_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2015_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2015_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2015 ol

No 2015 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The 2015 paper sets several asks unnumbered inside one letter, each priced by
a cell of its own: Q5(e) ("Define electronegativity." then "Use
electronegativity values ..."), Q10(b) (five asks over two printed marks,
(10) and (15)), Q11(a) (the passage, then "State one observation ...") and
Q11(b) (the underlined term, the Kc expression, then the effect of pressure
and the Haber process). One card each, the later ones cited by what they ask.
Q4(e) sets its romans inside one sentence, "How many electrons are shared
between the atoms in (i) a single covalent bond, (ii) a triple covalent bond?",
and the scheme prices each with a cell of its own: one card each, showing the
sentence. The scheme prices several cells as a sum the reader cannot read as
one cell -- Q6(c) "(2 × 6) + (2 × 3)", Q8(d) "(Four responses: (6) + (3 ×
3))", Q10(a) "(3 × 4) + (3 × 1)", Q11(a) "(2 × 4) + (4 × 3)" -- so those
cards are set by hand from the scheme's own lines. The paper underlines the
term Q10(a)(i) and Q11(b) ask about and prints Q11(a)'s passage with numbered
blanks, which no text layer carries: those take the paper's own print as
their question, as do Q2(c) (the flask it sketches), Q8(a) (the reaction
scheme that names W), Q9(b) (the table it plots), Q10(a) (the table it
completes) and Q11(b)'s Kc expression, whose answers are the scheme's
drawings. Q4(k) and Q11(c) offer whole alternative parts A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN, point)

P = Printed(2015, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2015-OL-'
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
        raise Refused(f'"{text}" is not in the 2015 ol scheme')
    return text


def cut(text, start=None, end=None):
    """The part of `text` from `start` (inclusive) up to `end` (exclusive), each
    asserted to be in it: a sentence lifted out of the paper's print."""
    a = text.index(start) if start else 0
    b = text.index(end, a) if end else len(text)
    return text[a:b].strip()


def adds(asides):
    return ('The scheme adds: ' + ' '.join(asides)) if asides else ''


def strip_tail(text, tail):
    """`text` less a tail asserted to end it: a sum cell the reader leaves on
    the answer's line ("D / propane / C₃H₈ (2 × 6) +")."""
    assert text.endswith(tail), (text, tail)
    return text[:-len(tail)].rstrip()


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Steam distillation of clove oil, and a separating funnel ─────────────
Q1A = FIG + 'paper-q1a'
Q1B = FIG + 'paper-q1b'
# (a)(i)-(v): one cell (8 + (4 × 3)) closes the five parts.
_q1a = [k('1', 'a', r) for r in ('i', 'ii', 'iii', 'iv', 'v')]
assert [cells(x) for x in _q1a] == [[None]] * 4 + [['[8 + (4 × 3)]']], [P.items(x) for x in _q1a]
_condenser = P.items(k('1', 'a', 'ii'))[0].text
assert _condenser == 'Liebig condenser', _condenser
C.ordered(_q1a, 'chem-u2', 'steam-distillation-of-clove-oil', figure=Q1A,
          row_notes={0: 'For (i).', 1: 'For (ii).', 2: 'For (iii).', 3: 'For (iv).', 4: 'For (v).'},
          label_key=[{'letter': 'A', 'meaning': _condenser, 'askedInThisQuestion': True}])
# (b)(i): the scheme draws cyclohexane three ways (its atoms are the picture's,
# 'scheme-labels').
assert cells(k('1', 'b', 'i')) == ['[6]'], P.items(k('1', 'b', 'i'))
# Its stem points at the separating funnel's diagram, which a drawing card does
# not show and the drawing does not need.
C.drawn([k('1', 'b', 'i')], 'chem-2-4', 'structure-of-cyclohexane', S + 'q1b-i', stem='')
C.fixed([k('1', 'b', 'ii')], 'chem-u2', 'organic-and-aqueous-layers', figure=Q1B)
# (iii): six points priced (2 × 6): a cell pricing fewer points than the
# scheme lists is a choice, any two of the six, six each.
_q1b3 = P.items(k('1', 'b', 'iii'))
assert [it.cell for it in _q1b3] == ['[2 × 6]'] and len(_q1b3[0].points()) == 6, _q1b3
_wash = [C.lifted('x', t, None)['verbatim'] for t in _q1b3[0].points()]
C.add([k('1', 'b', 'iii')], 'chem-u2', 'washing-the-emulsion-in-a-separating-funnel', [anyN(
    'r-1', _wash[0], 12, 2, 6, _wash, 'Any two of these: the scheme lists six points and prices the part (2 × 6).')],
    total=12, figure=Q1B)
C.fixed([k('1', 'b', 'iv')], 'chem-u2', 'isolating-clove-oil-from-the-solvent', figure=Q1B)

# ── Q2 A standard solution of sodium carbonate, and a titration ──────────────
Q2 = FIG + 'paper-q2'
_flask = P.items(k('2', 'a'))[0].text
assert _flask == 'volumetric flask', _flask
C.fixed([k('2', 'a')], 'chem-4-1', 'the-volumetric-flask', figure=Q2,
        label_key=[{'letter': 'F', 'meaning': _flask, 'askedInThisQuestion': True}])
C.fixed([k('2', 'b')], 'chem-4-1', 'transferring-all-the-solute-to-the-flask', figure=Q2)
# (c): the sketch's two points priced (2 × 3); the scheme draws the meniscus
# (its label "L" is the picture's, 'scheme-labels').
assert cells(k('2', 'c')) == ['[2 × 3]'], P.items(k('2', 'c'))
C.fixed([k('2', 'c')], 'chem-4-1', 'filling-a-volumetric-flask-to-the-mark', figure=S + 'q2c')
print_question('paper-q2c-print')
C.fixed([k('2', 'd')], 'chem-4-1', 'inverting-the-volumetric-flask', figure=Q2)
# (e): the answer (9), then two boxed routes side by side, (3) a step; the rows
# are the first route, the second in the notes. The text layer reads the two
# boxes across, so the first route is items 1, 3 and the first half of 4.
_q2e = P.items(k('2', 'e'))
assert [it.cell for it in _q2e] == ['[9]', '[3]', '[3]', '[3]', '[3]', '[3]'], _q2e
_mr = display(_q2e[1].text)
assert _mr == display(_q2e[2].text) == 'Mr = 106', _q2e
_r1c = '5.3 ÷ 2 = 2.65 g / 500 cm³'
_r2b = '106 ÷ 2 = 53 g'
assert _q2e[4].text == f'{_r1c} {_r2b}', _q2e[4]
C.add([k('2', 'e')], 'chem-4-1', 'mass-of-sodium-carbonate-for-a-standard-solution', [
    C.lifted('r-1', _mr, 3, 'Both of the scheme\'s routes open with this step.'),
    C.lifted('r-2', _q2e[3].text, 3, f'Or, by the scheme\'s second route, "{traced(_r2b)}" (3).'),
    C.lifted('r-3', _r1c, 3, f'Or, by the second route, "{traced(_q2e[5].text)}" (3).')],
    notes='The scheme gives the answer, ' + display(_q2e[0].text) + ', priced (9), then the working that '
          'earns it in two boxed routes, step by step; the steps here are its first route.', figure=Q2)
# (f)-(h): the sentence printed after (e) -- the titration and its equation --
# is their lead-in. (The question's opening sentence, which points at the
# flask's diagram, is not: the titration names the solutions it uses.)
Q2_TITRATION = P.lead(k('2', 'e'))
assert Q2_TITRATION.startswith('It was found by titration') and Q2_TITRATION.endswith('+ CO₂'), Q2_TITRATION
_measure = P.ask(k('2', 'f'))
assert _measure == 'Name the piece of equipment used to measure out', _measure
C.fixed([k('2', 'f', 'i')], 'chem-4-1', 'the-pipette', stem=f'{Q2_TITRATION} {_measure}')
C.fixed([k('2', 'f', 'ii')], 'chem-4-1', 'the-burette', stem=f'{Q2_TITRATION} {_measure}')
# (g): the indicator (3), then its colour change (2 × 3). The scheme sets the
# two indicators side by side ("methyl orange // phenolphthalein") and their
# colours in the same two columns, the second colour below the first (scheme
# PDF page 6): the rows are methyl orange's, phenolphthalein's in the notes.
# Its aside runs over three lines, and the reader takes the "(3)" quoted in it
# for a cell. It is one aside.
_q2g = P.items(k('2', 'g'))
assert [it.cell for it in _q2g] == ['[3]', '[2 × 3]', '[3]', None], _q2g
_ind = [x.strip() for x in _q2g[0].text.split('//')]
_first, _second = ([x.strip() for x in r.text.split('//')] for r in _q2g[1].rows[:2])
assert _ind == ['methyl orange', 'phenolphthalein'] and _first[0] == 'yellow (orange)' \
    and _second == ['red (pink, peach)', 'colourless'], (_ind, _first, _second)
_q2g_aside = traced(_q2g[2].text + ' (3) ' + _q2g[3].text)
C.add([k('2', 'g')], 'chem-4-1', 'indicator-and-colour-change-for-a-carbonate-titration', [
    C.lifted('r-1', _ind[0], 3, f'For the indicator. Or "{traced(_ind[1])}".'),
    C.lifted('r-2', _first[0], 3, 'For the colour change. The scheme prices the two colours (2 × 3), one each, '
             f'and sets them under the indicators in two columns: for phenolphthalein, "{traced(_first[1])}".'),
    C.lifted('r-3', _second[0], 3, f'For phenolphthalein, "{traced(_second[1])}". The scheme adds: {_q2g_aside}')],
    stem=Q2_TITRATION)
# (h): the answer (9) and the working that earns it, a box of stacked
# fractions the text layer cannot read (its digits come through as glyphs).
assert cells(k('2', 'h'))[0] == '[9]', P.items(k('2', 'h'))
C.answer_only([k('2', 'h')], 'chem-4-1', 'concentration-of-the-hydrochloric-acid', S + 'q2h', stem=Q2_TITRATION)

# ── Q3 Investigating river water ─────────────────────────────────────────────
C.fixed([k('3', 'a')], 'chem-1-2', 'flame-colour-of-potassium')
# (b)(i)-(iv): one cell (6 + (3 × 3)) closes the four parts.
_q3b = [k('3', 'b', r) for r in ('i', 'ii', 'iii', 'iv')]
assert [cells(x) for x in _q3b] == [[None]] * 3 + [['[6 + (3 × 3)]']], [P.items(x) for x in _q3b]
C.ordered(_q3b, 'chem-u2', 'brown-ring-test-for-nitrate', figure=FIG + 'paper-q3b',
          row_notes={0: 'For (i).', 1: 'For (ii).', 2: 'For (iii).', 3: 'For (iv).'})
# (c), (d): eight and nine points, each part priced (6 + 3): a cell pricing
# fewer points than the scheme lists is a choice, any two of them, the first
# (6) and the second (3).
_q3c = P.items(k('3', 'c'))
assert [it.cell for it in _q3c] == ['[6 + 3]'] and len(_q3c[0].points()) == 8 and not _q3c[0].asides, _q3c
_susp = [C.lifted('x', t, None)['verbatim'] for t in _q3c[0].points()]
C.add([k('3', 'c')], 'chem-u2', 'measuring-suspended-solids', [anyN(
    'r-1', _susp[0], 9, 2, 6, _susp, 'Any two of these, the first (6) and the second (3): the scheme lists eight '
    'points and prices the part (6 + 3).', steps=[6, 3])], total=9)
_q3d = P.items(k('3', 'd'))
assert [it.cell for it in _q3d] == ['[6 + 3]'] and len(_q3d[0].points()) == 9 \
    and _q3d[0].asides == ['[No diagram maximum (6) marks.]'], _q3d
_diss = [C.lifted('x', t, None)['verbatim'] for t in _q3d[0].points()]
C.add([k('3', 'd')], 'chem-u2', 'measuring-dissolved-solids', [anyN(
    'r-1', _diss[0], 9, 2, 6, _diss, 'Any two of these, the first (6) and the second (3): the scheme lists nine '
    'points and prices the part (6 + 3). ' + adds([traced(a) for a in _q3d[0].asides]), steps=[6, 3])], total=9)
C.route([k('3', 'e', 'i')], 'chem-4-3', 'concentration-of-suspended-solids')
C.route([k('3', 'e', 'ii')], 'chem-4-3', 'concentration-of-dissolved-solids-in-ppm')

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-3', 'mendeleevs-contribution', notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-2', 'an-excited-electron-falling-back', notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-2-2', 'shape-of-a-water-molecule', notes=Q4_NOTE)
assert cells(k('4', 'd')) == ['[3 + 3]'], P.items(k('4', 'd'))
C.fixed([k('4', 'd')], 'chem-1-4', 'equation-for-magnesium-burning-in-oxygen', notes=Q4_NOTE)
# (e): "(i) a single covalent bond, (ii) a triple covalent bond" are set inside
# one sentence, and the scheme prices each (3): one card each, showing the
# sentence. The paper breaks the line before "(ii)", so only (ii) is a part of
# the reader's own; (i) is the scheme's.
_q4e = f"{P.ask(k('4', 'e'))} (ii) {P.ask(k('4', 'e', 'ii'))}"
assert _q4e.startswith('How many electrons are shared between the atoms in (i) a single covalent bond,'), _q4e
assert cells(k('4', 'e', 'i')) == ['[3]'] and cells(k('4', 'e', 'ii')) == ['[3]']
C.fixed([k('4', 'e', 'i')], 'chem-2-1', 'electrons-in-a-single-covalent-bond', qtext=_q4e, stem='',
        row_notes={0: 'For (i).'}, notes=Q4_NOTE)
C.fixed([k('4', 'e', 'ii')], 'chem-2-1', 'electrons-in-a-triple-covalent-bond', qtext=_q4e, stem='',
        row_notes={0: 'For (ii).'}, notes=Q4_NOTE)
assert cells(k('4', 'f')) == ['[2 × 3]'], P.items(k('4', 'f'))
C.fixed([k('4', 'f')], 'chem-2-3', 'boyles-law', notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-3-2', 'catalysts-in-a-catalytic-converter', notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-4-2', 'the-acid-in-vinegar', notes=Q4_NOTE)
C.fixed([k('4', 'i')], 'chem-4-3', 'removing-phosphates-and-nitrates-from-sewage', notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-u2', 'chromatography', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'greenhouse-gases', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-1-3', 'metals-that-corrode-easily-in-air', notes=Q4_NOTE)

# ── Q5 Sodium chloride ───────────────────────────────────────────────────────
Q5 = FIG + 'paper-q5'
Q5_STEM = P.ask(k('5'))
C.fixed([k('5', 'a')], 'chem-2-1', 'what-is-an-ion', figure=Q5)
# (b), (c): a drawing (6), then how the atom becomes an ion (3). The asides the
# scheme prints under the drawing reach the reader on the explanation's row.


def atom_to_ion(key, concept, explain_text, asides):
    ask = P.ask(key)
    draw = cut(ask, None, 'Explain in words')
    its = P.items(key)
    assert [it.cell for it in its] == ['[6]', '[3]'] and its[0].text == '', its
    # (No stem: the question's opening sentence points at the crystal's
    # diagram, which a drawing card does not show and the drawing does not need.)
    return C.add([key], 'chem-2-1', concept, [
        C.mark_ask(point('r-1', draw, 6, DRAWN + ' ' + adds([traced(a) for a in asides]))),
        C.lifted('r-2', explain_text, 3, f'For "{cut(ask, "Explain in words")}"')],
        figure=S + f'q5{key[1]}', stem='')


_q5b = P.items(k('5', 'b'))
_q5b_asides = ['[Allow (3) for two correctly filled inner shells.]', '[Allow (3) marks for 2, 8, 1.]']
assert _q5b[1].text == ' '.join(_q5b_asides) + ' loses an electron', _q5b
atom_to_ion(k('5', 'b'), 'sodium-atom-to-sodium-ion', 'loses an electron', _q5b_asides)
_q5c = P.items(k('5', 'c'))
assert _q5c[0].asides == ['[Allow (3) marks for 2, 8, 7.]'] and _q5c[1].text == 'gains an electron', _q5c
atom_to_ion(k('5', 'c'), 'chlorine-atom-to-chloride-ion', 'gains an electron', _q5c[0].asides)
C.fixed([k('5', 'd')], 'chem-1-3', 'why-chlorine-atoms-are-smaller-than-sodium-atoms', figure=Q5)
# (e): "Define electronegativity." (2 × 3) and "Use electronegativity values
# ..." (2 × 3) are set before (i) and (ii), unnumbered, each priced by a cell of
# its own (scheme PDF page 9): one card each. Then "Explain why (i) ..., (ii)
# ...", a cell each.
_q5e_ask = P.ask(k('5', 'e'))
_define = cut(_q5e_ask, None, 'Use electronegativity')
_use = cut(_q5e_ask, 'Use electronegativity', 'Explain why')
assert _define == 'Define electronegativity.' and cut(_q5e_ask, 'Explain why') == 'Explain why', _q5e_ask
_q5e = P.items(k('5', 'e'))
assert [it.cell for it in _q5e] == ['[2 × 3]', '[2 × 3]'], _q5e
_en, _bond = _q5e[0].points(), _q5e[1].points()
assert len(_en) == 2 and len(_bond) == 2 and _q5e[1].asides == ['[Award marks once for ‘polar’.]'], _q5e
C.add([k('5', 'e')], 'chem-2-1', 'definition-of-electronegativity', [
    C.lifted('r-1', _en[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    C.lifted('r-2', _en[1], 3)], qtext=_define, stem=Q5_STEM, figure=Q5)
C.add([k('5', 'e')], 'chem-2-1', 'bonding-in-water-from-electronegativity', [
    C.lifted('r-1', _bond[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    C.lifted('r-2', _bond[1], 3, adds(_q5e[1].asides))],
    qtext=_use, stem=Q5_STEM, cid='q5-e-bonding-in-water', ref_suffix='bonding in a water molecule', figure=Q5)
# (e)(i): two points priced (2 × 3). The scheme sets them as two columns over
# two lines, "attraction between the ions of the crystal // ionic compounds /"
# over "and polar (partially charged) water molecules // dissolve in water"
# (scheme PDF page 9, as Q2(g)'s indicators): the rows are the first column.
_q5e1 = P.items(k('5', 'e', 'i'))
assert [it.cell for it in _q5e1] == ['[2 × 3]'] and _q5e1[0].asides == ['[Allow (3) marks for ‘like dissolves like’.]']
_top, _bottom = ([x.strip().rstrip('/').strip() for x in r.text.split('//')] for r in _q5e1[0].rows[:2])
assert _top == ['attraction between the ions of the crystal', 'ionic compounds'] \
    and _bottom == ['and polar (partially charged) water molecules', 'dissolve in water'], (_top, _bottom)
_explain = f'{Q5_STEM} Explain why'
C.add([k('5', 'e', 'i')], 'chem-2-2', 'why-sodium-chloride-dissolves-in-water', [
    C.lifted('r-1', _top[0], 3, 'The scheme prices this point and the next (2 × 3), one each. It prints them with '
             f'a second column beside them: "{traced(_top[0] + " // " + _top[1])} /" over "{traced(_bottom[0])} // '
             f'{traced(_bottom[1])}".'),
    C.lifted('r-2', _bottom[0], 3, adds(_q5e1[0].asides))], stem=_explain, figure=Q5)
C.fixed([k('5', 'e', 'ii')], 'chem-2-1', 'why-sodium-chloride-solution-conducts', stem=_explain, figure=Q5)

# ── Q6 Five hydrocarbons ─────────────────────────────────────────────────────
Q6 = FIG + 'paper-q6'
C.fixed([k('6', 'a')], 'chem-2-4', 'what-makes-a-hydrocarbon', figure=Q6)
# (b): any three of the five names, (3 × 3); the aside under it is a note.
C.menu([k('6', 'b')], 'chem-2-4', 'iupac-names-of-the-hydrocarbons', claim=3, figure=Q6,
       note='The paper asks for any three of the five.')
# (c)(i)-(iv): one cell "(2 × 6) + (2 × 3)", which the reader leaves on (iv)'s
# answer line as "(2 × 6) +" and reads its "(2 × 3)" as the cell.
_q6c = [k('6', 'c', r) for r in ('i', 'ii', 'iii', 'iv')]
_q6c_its = [P.items(x) for x in _q6c]
assert [[it.cell for it in x] for x in _q6c_its] == [[None]] * 3 + [['[2 × 3]']], _q6c_its
_which = [x[0].text for x in _q6c_its[:3]] + [strip_tail(_q6c_its[3][0].text, '(2 × 6) +')]
C.add(_q6c, 'chem-2-4', 'identifying-hydrocarbons-by-use-and-type', [
    C.lifted(f'r-{i + 1}', t, None, f'For ({r}).') for i, (t, r) in enumerate(zip(_which, ('i', 'ii', 'iii', 'iv')))],
    kind='orderedSplit', notation='[(2 × 6) + (2 × 3)]', total=18,
    notes=SPLIT.format('"' + traced('(2 × 6) + (2 × 3)') + '"'), figure=FIG + 'paper-q6c')
assert cells(k('6', 'd')) == ['[2 × 3]'], P.items(k('6', 'd'))
C.fixed([k('6', 'd')], 'chem-2-4', 'products-of-burning-hydrocarbons', figure=Q6)
assert cells(k('6', 'e')) == ['[6 + 3 + 3]'], P.items(k('6', 'e'))
C.ordered([k('6', 'e')], 'chem-2-4', 'aromatic-compounds-and-octane-number', figure=Q6,
          row_notes={0: 'For "Explain aromatic in terms of chemical structure."',
                     1: 'For "Would you expect compound E to have a high octane number?"',
                     2: 'For "Explain your answer."'})

# ── Q7 Acids, bases and water treatment ──────────────────────────────────────
# (a): "Define (i) an acid, (ii) a base." is one sentence; the scheme prices the
# two definitions "(2 × 4)", one cell: one card, four each.
_q7a = [P.items(k('7', 'a', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q7a] == [[None], ['[2 × 4]']], _q7a
assert _q7a[0][0].text.endswith(' //'), _q7a
C.add([k('7', 'a')], 'chem-3-4', 'definitions-of-an-acid-and-a-base', [
    C.lifted('r-1', _q7a[0][0].text[:-len(' //')], 4,
             'For (i). The scheme prices this point and the next (2 × 4), one each.'),
    C.lifted('r-2', _q7a[1][0].text, 4, 'For (ii).')])
assert cells(k('7', 'b', 'i')) == ['[2 × 3]'], P.items(k('7', 'b', 'i'))
C.fixed([k('7', 'b', 'i')], 'chem-3-4', 'definition-of-ph')
C.fixed([k('7', 'b', 'ii')], 'chem-3-4', 'ordering-by-acidity')
C.route([k('7', 'b', 'iii')], 'chem-3-4', 'ph-of-sulfuric-acid')
C.fixed([k('7', 'c', 'i')], 'chem-4-3', 'flocculation')
# (ii): the reason and the disadvantage, priced together (6 + 3); the reason's
# row reaches the margin, so the reader joins it to the next: the rows are read
# from the item's printed rows.
_q7c2 = P.items(k('7', 'c', 'ii'))
assert [it.cell for it in _q7c2] == ['[6 + 3]'], _q7c2
_rows7 = [r.text for r in _q7c2[0].rows if r.text]
assert len(_rows7) == 3 and _rows7[0].startswith('to kill microorganisms'), _rows7
C.add([k('7', 'c', 'ii')], 'chem-4-3', 'chlorinating-drinking-water', [
    C.lifted('r-1', _rows7[0], None, 'For "Why is drinking water chlorinated?"'),
    C.lifted('r-2', traced(display(' '.join(_rows7[1:]))), None, 'For "Give one disadvantage ..."')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'))
assert cells(k('7', 'c', 'iii')) == ['[6 + 3]'], P.items(k('7', 'c', 'iii'))
C.ordered([k('7', 'c', 'iii')], 'chem-4-3', 'drinking-water-with-too-low-a-ph',
          row_notes={0: 'For "State one problem ..."', 1: 'For "What is added to the water if the pH is too low?"'})

# ── Q8 Ethanol, ethene and ethanal ───────────────────────────────────────────
Q8 = FIG + 'paper-q8'
# (a): the name and the structure, priced together (5 + 3); the scheme's
# drawing (its atoms are 'scheme-labels') is the answer picture, and the
# reaction scheme that says what W is travels with the question's print.
_q8a = P.items(k('8', 'a'))
assert [(it.cell, it.text) for it in _q8a] == [('[5 + 3]', 'ethene')], _q8a
_q8a_ask = P.ask(k('8', 'a'))
C.add([k('8', 'a')], 'chem-4-2', 'name-and-structure-of-ethene', [
    C.lifted('r-1', 'ethene', None, f'For "{cut(_q8a_ask, None, " and draw")}"'),
    C.mark_ask(point('r-2', cut(_q8a_ask, 'draw its'), None, DRAWN))],
    kind='orderedSplit', notation='[5 + 3]', total=8, notes=SPLIT.format('[5 + 3]'), figure=S + 'q8a')
print_question('paper-q8a-print')
assert [cells(k('8', 'b', r)) for r in ('i', 'ii')] == [[None], ['[9 + 3]']]
C.ordered([k('8', 'b', 'i'), k('8', 'b', 'ii')], 'chem-4-2', 'preparing-ethene-from-ethanol',
          figure=FIG + 'paper-q8b', row_notes={0: 'For (i).', 1: 'For (ii).'})
C.fixed([k('8', 'c', 'i')], 'chem-2-4', 'what-unsaturated-means', figure=Q8)
assert cells(k('8', 'c', 'ii')) == ['[6 + 3]'], P.items(k('8', 'c', 'ii'))
C.ordered([k('8', 'c', 'ii')], 'chem-2-4', 'test-for-unsaturation', figure=Q8,
          row_notes={0: 'For the test.', 1: 'For what is observed.'})
# (d): four responses over (i)-(iii) -- (iii) asks "Which ...? Why?" -- priced
# "(Four responses: (6) + (3 × 3))", which the reader leaves as words.
_q8d = [P.items(k('8', 'd', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in x] for x in _q8d] == [[None]] * 3, _q8d
_q8d3 = _q8d[2][0].points()
_four = traced('(Four responses: (6) + (3 × 3))')
assert len(_q8d3) == 3 and _q8d3[0] == 'ethanol' and _q8d3[2] == _four, _q8d3
C.add([k('8', 'd', r) for r in ('i', 'ii', 'iii')], 'chem-4-2', 'ethanal-from-ethanol-and-solubility-in-water', [
    C.lifted('r-1', _q8d[0][0].text, None, 'For (i).'),
    C.lifted('r-2', _q8d[1][0].text, None, 'For (ii).'),
    C.lifted('r-3', _q8d3[0], None, 'For (iii), "Which one ...?"'),
    C.lifted('r-4', _q8d3[1], None, 'For (iii), "Why?"')],
    kind='orderedSplit', notation='[6 + (3 × 3)]', total=15,
    notes=SPLIT.format(f'"{_four}"'), figure=Q8)

# ── Q9 The rate of reaction of seashells with hydrochloric acid ─────────────
Q9 = FIG + 'paper-q9'
Q9T = FIG + 'paper-q9-table'
assert cells(k('9', 'a')) == ['[3 + 2]'], P.items(k('9', 'a'))
C.ordered([k('9', 'a')], 'chem-3-2', 'definition-of-rate-of-reaction', figure=Q9)
# (b): the scheme's graph is the answer picture (its axis labels are
# 'scheme-labels'); the table it plots is the paper's print.
assert cells(k('9', 'b')) == ['[3]', '[3]', '[6]', '[3]'], P.items(k('9', 'b'))
C.fixed([k('9', 'b')], 'chem-3-2', 'graph-of-carbon-dioxide-volume-against-time', figure=S + 'q9b')
print_question('paper-q9b-print')
C.fixed([k('9', 'c')], 'chem-3-2', 'why-the-rate-falls-with-time', figure=Q9)
C.fixed([k('9', 'd')], 'chem-3-2', 'knowing-the-reaction-has-ended', figure=Q9)
C.fixed([k('9', 'e', 'i')], 'chem-3-2', 'volume-read-from-the-graph', figure=Q9T)
# (ii): the answer (3), then the same expression boxed beneath it, (3): the
# working of the same three marks.
_q9e2 = P.items(k('9', 'e', 'ii'))
assert [it.cell for it in _q9e2] == ['[3]', '[3]'] and _q9e2[0].text == _q9e2[1].text, _q9e2
C.add([k('9', 'e', 'ii')], 'chem-3-2', 'average-rate-over-the-first-minutes', [
    C.lifted('r-1', _q9e2[0].text, 3, 'The scheme prints the same expression again in a box beneath it, as the '
             'working, (3).')], figure=Q9T)
# (f)(i)-(iii): one cell (3 × 3) closes the three parts: equal terms, three each.
_q9f = [P.items(k('9', 'f', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in x] for x in _q9f] == [[None], [None], ['[3 × 3]']], _q9f
C.add([k('9', 'f', r) for r in ('i', 'ii', 'iii')], 'chem-3-2', 'factors-affecting-the-rate', [
    C.lifted('r-1', _q9f[0][0].text, 3, 'For (i). The scheme prices these three answers (3 × 3), one each.'),
    C.lifted('r-2', _q9f[1][0].text, 3, 'For (ii).'),
    C.lifted('r-3', _q9f[2][0].text, 3, 'For (iii).')], figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the completed table is the scheme's (its entries are 'scheme-labels'),
# priced "(3 × 4) + (3 × 1)", which the reader reads as the cell "[3 × 1]" and
# the words "(3 × 4) +"; the table the paper prints is the question's print.
_q10a = P.items(k('10', 'a'))
assert [(it.cell, it.text) for it in _q10a] == [('[3 × 1]', '(3 × 4) +')], _q10a
C.add([k('10', 'a')], 'chem-1-2', 'atomic-number-mass-number-and-neutrons', [
    C.mark_ask(point('r-1', P.ask(k('10', 'a')), 15,
                     'The scheme answers this with the completed table, priced "' + traced('(3 × 4) + (3 × 1)')
                     + '"; its own print is shown with the answer.'))], total=15, figure=S + 'q10a', stem='')
print_question('paper-q10a-print')
# (a)(i): the paper underlines "radioactive".
C.fixed([k('10', 'a', 'i')], 'chem-1-2', 'radioactive', stem='')
print_question('paper-q10a-i-print')
C.fixed([k('10', 'a', 'ii')], 'chem-1-2', 'the-metal-foil-in-rutherfords-experiment', stem='')
# (b): five asks set unnumbered, under two printed marks, (10) and (15), each
# priced by cells of its own (scheme PDF page 12): one card each.
_q10b = P.ask(k('10', 'b'))
_exo = cut(_q10b, None, 'Name the instrument')
_instrument = cut(_q10b, 'Name the instrument', 'Define heat')
_define_hc = cut(_q10b, 'Define heat', 'Two moles')
_hexane = cut(_q10b, 'Two moles', 'Calculate the heat')
_calc = cut(_q10b, 'Calculate the heat', 'Is this reaction')
_is_exo = cut(_q10b, 'Is this reaction')
assert _hexane.endswith('2C₆H₁₄ + 19O₂ → 12CO₂ + 14H₂O ∆H = – 8326 kJ'), _hexane
_q10b_its = P.items(k('10', 'b'))
assert [it.cell for it in _q10b_its] == ['[6]', '[2 × 2]', '[2 × 3]', '[3]', '[3]', '[3]', '[3]'], _q10b_its
_bomb, _hc = _q10b_its[1].points(), _q10b_its[2].points()
assert _bomb == ['bomb', 'calorimeter'] and len(_hc) == 2, (_bomb, _hc)
C.add([k('10', 'b')], 'chem-3-1', 'exothermic-reaction', [C.lifted('r-1', _q10b_its[0].text, 6)],
      qtext=_exo, stem='')
C.add([k('10', 'b')], 'chem-3-1', 'the-bomb-calorimeter', [
    C.lifted('r-1', _bomb[0], 2, 'The scheme prices this point and the next (2 × 2), one each.'),
    C.lifted('r-2', _bomb[1], 2)], qtext=_instrument, stem='', cid='q10-b-bomb-calorimeter',
    ref_suffix='the instrument')
C.add([k('10', 'b')], 'chem-3-1', 'definition-of-heat-of-combustion', [
    C.lifted('r-1', _hc[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    C.lifted('r-2', _hc[1], 3)], qtext=_define_hc, stem='', cid='q10-b-heat-of-combustion',
    ref_suffix='heat of combustion')
C.add([k('10', 'b')], 'chem-3-1', 'heat-of-combustion-of-hexane', [
    C.lifted('r-1', _q10b_its[4].text, 3)], qtext=_calc, stem=_hexane, cid='q10-b-calculation',
    ref_suffix='the heat of combustion of hexane',
    notes='The scheme gives the answer, ' + display(_q10b_its[3].text) + ', priced (3), then the working that '
          'earns it, (3).')
C.add([k('10', 'b')], 'chem-3-1', 'is-the-combustion-of-hexane-exothermic', [
    C.lifted('r-1', _q10b_its[5].text, 3, 'For "Is this reaction exothermic?"'),
    C.lifted('r-2', _q10b_its[6].text, 3, 'For "Give a reason for your answer."')],
    qtext=_is_exo, stem=_hexane, cid='q10-b-exothermic', ref_suffix='is the reaction exothermic')
Q10C = FIG + 'paper-q10c'
C.fixed([k('10', 'c', 'i')], 'chem-1-4', 'molar-mass-of-neon', figure=Q10C)
# (ii): the answer (6), then its working in a box, the fraction 5/20 set
# stacked, which the text layer reads "20 = 5".
assert cells(k('10', 'c', 'ii')) == ['[6]', '[3]', '[3]'], P.items(k('10', 'c', 'ii'))
C.answer_only([k('10', 'c', 'ii')], 'chem-1-4', 'moles-of-neon', S + 'q10c-ii')
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'atoms-of-neon')
C.cards[-1]['figureKey'] = Q10C
C.route([k('10', 'c', 'iv')], 'chem-1-4', 'volume-of-neon-at-stp')
C.cards[-1]['figureKey'] = Q10C

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): six blanks priced "(2 × 4) + (4 × 3)", which the reader leaves on the
# sixth answer as "(2 × 4) +" and reads its "(4 × 3)" as the cell; then one
# observation (5). The passage is the paper's print.
_q11a = P.items(k('11', 'a'))
assert [it.cell for it in _q11a] == ['[4 × 3]', '[5]'], _q11a
_blanks = _q11a[0].points()
assert len(_blanks) == 6, _blanks
_blanks[5] = strip_tail(_blanks[5], '(2 × 4) +')
_q11a_ask = P.ask(k('11', 'a'))
C.add([k('11', 'a')], 'chem-3-5', 'redox-and-zinc-in-copper-sulfate', [
    C.lifted(f'r-{i + 1}', b, None) for i, b in enumerate(_blanks)],
    kind='orderedSplit', notation='[(2 × 4) + (4 × 3)]', total=20,
    notes=SPLIT.format('"' + traced('(2 × 4) + (4 × 3)') + '"') + ' Each answer is numbered by its blank.',
    qtext=cut(_q11a_ask, None, 'State one observation'))
print_question('paper-q11a-print')
C.add([k('11', 'a')], 'chem-3-5', 'observing-zinc-in-copper-sulfate', [C.lifted('r-1', _q11a[1].text, 5)],
      qtext=cut(_q11a_ask, 'State one observation'), stem='', cid='q11-a-observation',
      ref_suffix='an observation')
# (b): three asks set unnumbered, each priced by cells of its own (scheme PDF
# page 13): the underlined term (4 + 3), the Kc expression (6), then the effect
# of pressure and the Haber process (6 + (2 × 3)). The equation is a picture
# (paper-q11b-eq): its arrow is a glyph the text layer cannot read.
_q11b_ask = P.ask(k('11', 'b'))
Q11B_LEAD = cut(_q11b_ask, None, 'Explain the underlined')
_q11b = P.items(k('11', 'b'))
assert [(it.cell, bool(it.text)) for it in _q11b] == [('[4 + 3]', True), ('[6]', False), ('[6 + (2 × 3)]', True)], _q11b
_eq_pts = _q11b[0].points()
assert len(_eq_pts) == 2, _eq_pts
C.add([k('11', 'b')], 'chem-3-3', 'definition-of-chemical-equilibrium', [
    C.lifted('r-1', _eq_pts[0], None), C.lifted('r-2', _eq_pts[1], None)],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'),
    qtext=cut(_q11b_ask, 'Explain the underlined', 'Write the equilibrium'), stem=Q11B_LEAD)
print_question('paper-q11b-print')
_kc = cut(_q11b_ask, 'Write the equilibrium', 'What effect')
C.add([k('11', 'b')], 'chem-3-3', 'kc-expression-for-the-haber-equilibrium', [
    C.mark_ask(point('r-1', _kc, 6, 'The scheme answers this with the expression set as a fraction, which its '
                     'text cannot carry; its own print is shown with the answer.'))],
    qtext=_kc, stem=Q11B_LEAD, figure=S + 'q11b-kc', cid='q11-b-kc', ref_suffix='the Kc expression')
print_question('paper-q11b-kc-print')
_pressure = _q11b[2].points()
assert len(_pressure) == 3 and _pressure[2] == 'cost / safety', _pressure
_effect = cut(_q11b_ask, 'What effect', 'This equilibrium')
C.add([k('11', 'b')], 'chem-3-3', 'pressure-and-the-haber-process', [
    C.lifted('r-1', _pressure[0], None, f'For "{cut(_effect, None, " Explain your answer.")}"'),
    C.lifted('r-2', _pressure[1], None, 'For "Explain your answer."'),
    C.lifted('r-3', _pressure[2], None, 'For "Give one reason why extremely high pressures are not used ..."')],
    kind='orderedSplit', notation='[6 + (2 × 3)]', total=12, notes=SPLIT.format('[6 + (2 × 3)]'),
    qtext=cut(_q11b_ask, 'What effect'), stem=Q11B_LEAD, figure=FIG + 'paper-q11b-eq', cid='q11-b-pressure',
    ref_suffix='pressure and the Haber process')
# (c)A(i): three asks, a cell each, (4), (3) and (3).
_ca1 = P.ask(ka('11', 'c', 'i', 'A'))
assert cells(ka('11', 'c', 'i', 'A')) == ['[4]', '[3]', '[3]'], P.items(ka('11', 'c', 'i', 'A'))
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-4-3', 'nitrogen-from-the-air', row_notes={
    0: f'For "{cut(_ca1, "What other gas", " What is the approximate")}"',
    1: f'For "{cut(_ca1, "What is the approximate", " Give a widespread")}"',
    2: f'For "{cut(_ca1, "Give a widespread")}"'})
assert cells(ka('11', 'c', 'ii', 'A')) == ['[6 + 6 + 3]'], P.items(ka('11', 'c', 'ii', 'A'))
C.ordered([ka('11', 'c', 'ii', 'A')], 'chem-4-3', 'the-ozone-layer',
          row_notes={0: 'For "Name the other form of oxygen gas ..."', 1: 'For "What environmentally beneficial '
                     'effect does O₃ have?"', 2: 'For "Identify a group of chemicals that damages O₃."'})
Q11CB = FIG + 'paper-q11c-b'
assert cells(ka('11', 'c', 'i', 'B')) == ['[6 + 6 + 3]'], P.items(ka('11', 'c', 'i', 'B'))
C.ordered([ka('11', 'c', 'i', 'B')], 'chem-u3', 'the-blast-furnace', figure=Q11CB,
          row_notes={0: 'For "Give the name or formula of an ore of iron."', 1: 'For "Name another substance '
                     'added in the charge ..."', 2: 'For "What name is given to the impurity removed at X?"'})
# (ii): the scheme's last page prints "BLANK PAGE" under its answers.
assert cells(ka('11', 'c', 'ii', 'B')) == ['[6 + 4]', None], P.items(ka('11', 'c', 'ii', 'B'))
C.ordered([ka('11', 'c', 'ii', 'B')], 'chem-u3', 'steel', figure=Q11CB, drop=('BLANK PAGE', 'Blank Page'),
          row_notes={0: 'For "Name this alloy."', 1: 'For "What other element is always present in this alloy?"'})


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
    """Every letter's printed marks, alternatives apart: the paper prints Q10(a),
    Q10(b), Q11(b) and Q11(c)A in subtotals ("(10)" then "(15)"), so the sum of
    every mark printed under the letter, not the last."""
    out = {}
    for s in P.pseg:
        q, letter, _roman, alt = s.key
        if letter and s.marks_at:
            out[(q, letter, alt)] = out.get((q, letter, alt), 0) + sum(m for _n, m in s.marks_at)
    for (q, letter, _r, _a), m in P.marks.items():
        if letter and not any(key[:2] == (q, letter) for key in out):
            out[(q, letter, None)] = m
    # Two marks print at the end of a line of words, which the reader strips
    # from the ask without recording where they fell (paper page 6): Q10(b)'s
    # "(10)" after "... calorific values of different foods." and Q10(c)(iv)'s
    # "(6)" after "... at s.t.p.?". They are added to their letters here.
    page6 = [l.text for l in read_lines(P.paper_path) if l.page == 6]
    for key, (tail, m) in {('10', 'b', None): ('different foods. (10)', 10),
                           ('10', 'c', None): ('at s.t.p.? (6)', 6)}.items():
        assert sum(t.endswith(tail) for t in page6) == 1, tail
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
