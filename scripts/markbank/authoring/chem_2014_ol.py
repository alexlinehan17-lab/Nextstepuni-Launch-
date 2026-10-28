#!/usr/bin/env python3
"""2014 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2014_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2014_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2014_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2014 ol

No 2014 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The 2014 scheme heads Question 10 "QUESTION 10:" with its rubric on the next
line; chem_print reads it as the head (gated to 2014 OL, Printed.__init__),
without which Q10's and Q11's rows fell into Q9.

The paper sets several asks unnumbered inside one letter, each priced by a
cell of its own -- Q5(b) (after (ii), the noble gases), Q6(b), Q6(d), Q7(a),
Q9(a), Q10(b) and Q11(b) -- one card each, the later ones cited by what they
ask. It sets some romans inside one sentence -- Q7(a) "Define (i) acid, (ii)
base.", Q7(c), Q7(d), Q10(b) "How many (i) moles ..., (ii) molecules ...",
Q11(b) "Define (i) oxidation, (ii) reduction ..." and "Identify (iii) ...,
(iv) ..., (v) ..." -- which the scheme numbers; the cards follow the scheme's
cells and take the paper's sentence as their question. Q11(c)A opens with two
asks of its own before (i). The paper underlines the term Q2(a) and Q10(c)(i)
ask about, prints Q4(a)'s nuclide and Q4(d)'s state symbols in a form the text
layer scatters, and prints Q9(b)'s passage with numbered blanks and Q11(a)'s
descriptions in a table: those take the paper's own print as their question,
as do Q3(d) (the table it plots), Q8(b) (the reaction scheme that names W and
A), Q10(a)(iii) (the table it completes) and Q10(c)(ii) (the equation it
needs). Q4(k) and Q11(c) offer whole alternative parts A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import (Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined,  # noqa: E402
                        read_lines, anyN)

P = Printed(2014, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2014-OL-'
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
        raise Refused(f'"{text}" is not in the 2014 ol scheme')
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


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Preparing ethyne ──────────────────────────────────────────────────────
Q1 = FIG + 'paper-q1'
assert cells(k('1', 'a')) == ['[2 × 3]', '[5]'], P.items(k('1', 'a'))
C.fixed([k('1', 'a')], 'chem-2-4', 'hydrocarbons-and-the-alkynes', figure=Q1,
        row_notes={0: 'For "Explain the term hydrocarbon."',
                   2: 'For "To which homologous series does ethyne belong?"'})
# (b)(i)-(iii): one cell (3 × 3) closes the three parts: equal terms, three each.
_q1b = [P.items(k('1', 'b', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in x] for x in _q1b] == [[None], [None], ['[3 × 3]']], _q1b
C.add([k('1', 'b', r) for r in ('i', 'ii', 'iii')], 'chem-u2', 'reagents-for-preparing-ethyne', [
    lift('r-1', bare(_q1b[0][0].text), 3, 'For (i). The scheme prices these three answers (3 × 3), one each.'),
    lift('r-2', bare(_q1b[1][0].text), 3, 'For (ii).'),
    lift('r-3', bare(_q1b[2][0].text), 3, 'For (iii).')], figure=Q1)
C.fixed([k('1', 'c')], 'chem-u2', 'discarding-the-first-test-tubes-of-gas', figure=Q1)
assert cells(k('1', 'd')) == ['[3]', '[3]', '[2 × 3]'], P.items(k('1', 'd'))
C.fixed([k('1', 'd')], 'chem-2-4', 'unsaturation-and-a-test-for-it', figure=Q1,
        row_notes={0: 'For "What is meant by saying that ethyne is unsaturated?"',
                   1: 'For the test: the reagent.'})
C.fixed([k('1', 'e')], 'chem-2-4', 'the-ethyne-flame-and-its-use', figure=Q1,
        row_notes={0: 'For the flame.', 1: 'For "Give a use for this very hot flame."'})

# ── Q2 A titration of sodium hydroxide with hydrochloric acid ────────────────
Q2 = FIG + 'paper-q2'
# (a): the paper underlines "standard solution".
C.fixed([k('2', 'a')], 'chem-4-1', 'standard-solution')
print_question('paper-q2a-print')
assert cells(k('2', 'b')) == ['[3 × 3]'], P.items(k('2', 'b'))
C.fixed([k('2', 'b')], 'chem-4-1', 'naming-titration-equipment', figure=Q2)
assert cells(k('2', 'c')) == ['[2 × 3]'], P.items(k('2', 'c'))
C.fixed([k('2', 'c')], 'chem-4-1', 'the-conical-flask-and-its-use', figure=Q2,
        row_notes={0: 'For the glassware named.', 1: 'For its use.'})
C.fixed([k('2', 'd')], 'chem-4-1', 'rinsing-the-pipette', figure=Q2)
C.fixed([k('2', 'e')], 'chem-4-1', 'using-the-wash-bottle', figure=Q2)
# (f): the indicator (3), then its colour change, "colour before // colour
# after" (2 × 3), with each indicator's two colours boxed beneath (scheme PDF
# page 6): the rows are methyl orange's, the other two indicators' in the notes.
_q2f = P.items(k('2', 'f'))
assert [it.cell for it in _q2f] == ['[3]', '[2 × 3]', None], _q2f
assert _q2f[1].text == 'colour before // colour after', _q2f[1]
_box = [r.text for r in _q2f[2].rows if r.text]
assert _box == ['methyl orange: yellow (orange) // red (pink, peach)', 'methyl red: yellow // red',
                'phenolphthalein: purple (pink, violet) // colourless'], _box
_mo = [x.strip() for x in _box[0][len('methyl orange:'):].split('//')]
assert _mo == ['yellow (orange)', 'red (pink, peach)'], _mo
C.add([k('2', 'f')], 'chem-4-1', 'indicator-and-colour-change-for-a-strong-acid-and-base', [
    lift('r-1', _q2f[0].text, 3, 'For the indicator.'),
    lift('r-2', _mo[0], 3, 'For the colour change, with methyl orange: the colour before. The scheme prices "'
         + traced(_q2f[1].text) + '" (2 × 3), one each, and boxes each indicator\'s two colours: "'
         + traced(_box[1]) + '" and "' + traced(_box[2]) + '".'),
    lift('r-3', _mo[1], 3, 'The colour after, with methyl orange.')], figure=Q2)
# (g): the answer and the working that earns it, step by step; the sentence
# printed under (g) -- the titration and its equation -- is the stem.
Q2G = P.ask(k('2', 'g'))
assert Q2G.startswith('It was found that 25.0 cm³') and Q2G.endswith('of the sodium hydroxide solution'), Q2G
assert cells(k('2', 'g', 'i')) == ['[9]', '[6]', '[3]'], P.items(k('2', 'g', 'i'))
C.route([k('2', 'g', 'i')], 'chem-4-1', 'concentration-of-sodium-hydroxide-in-moles-per-litre', stem=Q2G)
assert cells(k('2', 'g', 'ii')) == ['[3]', '[3]'], P.items(k('2', 'g', 'ii'))
C.route([k('2', 'g', 'ii')], 'chem-4-1', 'concentration-of-sodium-hydroxide-in-grams-per-litre', stem=Q2G)

# ── Q3 The decomposition of hydrogen peroxide ────────────────────────────────
Q3T = FIG + 'paper-q3-table'
Q3_LEAD = P.ask(k('3'))
_table = ' The results are shown in the table below.'
assert Q3_LEAD.endswith(_table), Q3_LEAD
Q3_SETUP = Q3_LEAD[:-len(_table)]
assert cells(k('3', 'a')) == ['[2 × 3]', '[5]'], P.items(k('3', 'a'))
C.fixed([k('3', 'a')], 'chem-3-2', 'catalysts-and-a-catalyst-for-hydrogen-peroxide', stem=Q3_SETUP,
        row_notes={0: 'For "What is a catalyst?"', 2: 'For "Suggest a suitable catalyst ..."'})
C.fixed([k('3', 'b')], 'chem-3-2', 'gas-from-decomposing-hydrogen-peroxide', stem=Q3_SETUP)
# (c): the scheme draws two set-ups (their labels are its picture,
# 'scheme-labels') and prices the drawing (6) and any two labels (2 × 3).
assert cells(k('3', 'c')) == ['[6]', '[2 × 3]'], P.items(k('3', 'c'))
C.fixed([k('3', 'c')], 'chem-u2', 'apparatus-for-measuring-the-oxygen-given-off', figure=S + 'q3c',
        stem=Q3_SETUP, notes='The scheme draws two suitable set-ups above these points; its own print is shown '
                             'with the answer.')
# (d): the axes, any two of four points "Any two: (2 × 3)"; the points and the
# curve (2 × 3); the estimate (6). The scheme's graph is the answer picture
# (its axis labels are 'scheme-labels'); the table it plots is the paper's print.
_q3d = P.items(k('3', 'd'))
assert [it.cell for it in _q3d] == ['[2 × 3]', '[2 × 3]', '[6]'] and _q3d[0].asides[0] == '[any two]', _q3d
_axes = [lift('x', o, None)['verbatim'] for o in _q3d[0].options()]
assert len(_axes) == 4, _axes
_plot = _q3d[1].points()
assert _plot == ['six points correctly plotted', 'smooth curve correctly drawn'], _plot
C.add([k('3', 'd')], 'chem-3-2', 'graph-of-oxygen-volume-against-time', [
    anyN('r-1', _axes[0], 6, 2, 3, _axes, 'Any two of these: the scheme lists four points and prices them "'
         + traced('Any two: (2 × 3)') + '". ' + adds([traced(_q3d[0].asides[1])])),
    lift('r-2', _plot[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-3', _plot[1], 3),
    lift('r-4', _q3d[2].text, 6, 'For "Estimate, from your graph, the volume of gas produced after 1.25 minutes."')],
    total=18, figure=S + 'q3d')
print_question('paper-q3d-print')
assert cells(k('3', 'e')) == ['[2 × 3]', None], P.items(k('3', 'e'))
C.fixed([k('3', 'e')], 'chem-3-2', 'why-the-rate-falls-with-time', figure=Q3T,
        row_notes={0: 'For "Does the rate of reaction increase or decrease with time?"', 1: 'For the reason.'})

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
# (a): the paper prints the nuclide with its mass and atomic numbers stacked
# (their print is 'labels'), which the text layer cannot set: the paper's print.
C.fixed([k('4', 'a')], 'chem-1-2', 'neutrons-in-a-lithium-atom', notes=Q4_NOTE)
print_question('paper-q4a-print')
assert cells(k('4', 'b')) == ['[2 × 3]'], P.items(k('4', 'b'))
C.fixed([k('4', 'b')], 'chem-2-1', 'electronegativity', notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-2-2', 'shape-of-an-ammonia-molecule', notes=Q4_NOTE)
# (d): the equation's state symbols are subscripts the text layer scatters
# ("3H_(2 ()g)"), so the equation is read as a picture ('labels') and the
# paper's print of the item is the question.
assert cells(k('4', 'd')) == ['[2 × 3]'], P.items(k('4', 'd'))
C.fixed([k('4', 'd')], 'chem-3-1', 'endothermic-formation-of-benzene', notes=Q4_NOTE,
        row_notes={0: 'For "Is this reaction exothermic or endothermic?"', 1: 'For "Explain your answer."'})
print_question('paper-q4d-print')
C.fixed([k('4', 'e')], 'chem-2-2', 'a-polar-liquid-and-a-charged-rod', notes=Q4_NOTE, figure=FIG + 'paper-q4e')
C.fixed([k('4', 'f')], 'chem-4-3', 'chlorinating-swimming-pools', notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-3-5', 'what-carries-the-current-in-electrolysis', notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-1-2', 'alpha-particles', notes=Q4_NOTE)
# (i): the answer (6) and its working in a box, (3) a step, a fraction set
# stacked ("32" over "80"): the scheme's print of the working is the figure.
assert cells(k('4', 'i')) == ['[6]', '[3]', '[3]'], P.items(k('4', 'i'))
C.answer_only([k('4', 'i')], 'chem-1-4', 'percentage-of-sulfur-in-sulfur-trioxide', S + 'q4i', notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-u2', 'melting-point-of-an-impure-substance', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-u3', 'safety-in-a-chemical-plant', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-4-2', 'naming-pvc-from-its-repeating-units', notes=Q4_NOTE,
        figure=FIG + 'paper-q4k-b')

# ── Q5 Atomic structure and the periodic table ───────────────────────────────
C.fixed([k('5', 'a')], 'chem-1-2', 'atomic-number')
# (b)(i)-(ii): one cell (6 + 6) closes the two parts: equal terms, six each.
# The ask the paper sets after (ii) under the same mark, "Why do the elements
# of group 18 ...?", is priced (6) on its own: a card of its own.
Q5B = P.ask(k('5', 'b'))
Q5B_SETUP = cut(Q5B, None, ' In terms of the distribution')
_q5b2_ask = P.ask(k('5', 'b', 'ii'))
_period = cut(_q5b2_ask, None, ' Why do the elements')
_noble = cut(_q5b2_ask, 'Why do the elements')
_q5b = [P.items(k('5', 'b', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q5b] == [[None], ['[6 + 6]', '[6]']], _q5b
C.add([k('5', 'b', 'i'), k('5', 'b', 'ii')], 'chem-1-3', 'electron-arrangements-in-groups-and-periods', [
    lift('r-1', bare(_q5b[0][0].text), 6, 'For (i). The scheme prices this point and the next (6 + 6), one each.'),
    lift('r-2', _q5b[1][0].text, 6, 'For (ii).')],
    qtext=f"(i) {P.ask(k('5', 'b', 'i'))} (ii) {_period}")
C.add([k('5', 'b')], 'chem-1-3', 'why-the-noble-gases-are-unreactive', [
    lift('r-1', _q5b[1][1].text, 6, adds(_q5b[1][1].asides))],
    qtext=_noble, stem=Q5B_SETUP, cid='q5-b-noble-gases', ref_suffix='after (ii), the noble gases')
# (c): "(i) an atom of magnesium (Mg), (ii) an atom of oxygen (O)" -- one cell
# (6 + 6) over the two: equal terms, six each.
_q5c = [P.items(k('5', 'c', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q5c] == [[None], ['[6 + 6]']], _q5c
C.add([k('5', 'c', 'i'), k('5', 'c', 'ii')], 'chem-1-2', 'electron-arrangements-of-magnesium-and-oxygen', [
    lift('r-1', bare(_q5c[0][0].text), 6, 'For (i). The scheme prices this point and the next (6 + 6), one each. '
         + adds(_q5c[0][0].asides)),
    lift('r-2', bare(_q5c[1][0].text), 6, 'For (ii). ' + adds(_q5c[1][0].asides))])
assert cells(k('5', 'd')) == ['[2 × 3]', '[6]', '[3]'], P.items(k('5', 'd'))
C.fixed([k('5', 'd')], 'chem-2-1', 'magnesium-oxide-and-ionic-bonding',
        row_notes={0: 'For the name.', 1: 'For the formula.', 2: 'For the type of bond.',
                   3: 'For "Give one characteristic of compounds with this type of bond."'})

# ── Q6 Hydrocarbons in fuels ─────────────────────────────────────────────────
Q6 = FIG + 'paper-q6'
Q6_LEAD = P.ask(k('6'))
assert Q6_LEAD == 'Compounds A, B, C and D in the table are found in fuels.', Q6_LEAD
assert cells(k('6', 'a')) == ['[5 + 3]'], P.items(k('6', 'a'))
C.ordered([k('6', 'a')], 'chem-2-4', 'naming-methane-and-butane', figure=Q6)
# (b): two asks, each printed with its mark (6) and priced by a cell of its
# own: the source (6), then the balanced equation (2 × 3), one card each.
_q6b = P.items(k('6', 'b'))
assert [it.cell for it in _q6b] == ['[6]', '[2 × 3]'], _q6b
_q6b_lead = P.lead(k('6', 'b'))
_copy = cut(_q6b_lead, 'Copy the equation')
_burned = cut(_q6b_lead, None, 'Copy the equation')
assert _burned.endswith('CH₄ + O₂ → CO₂ + H₂O'), _burned
C.add([k('6', 'b')], 'chem-4-3', 'sources-of-methane', [lift('r-1', _q6b[0].text, 6)], figure=Q6)
_eq = _q6b[1].text
assert _eq == 'CH₄ + 2O₂ → CO₂ + 2H₂ O', _eq
C.add([k('6', 'b')], 'chem-1-4', 'balancing-the-combustion-of-methane', [
    lift('r-1', _eq.replace('2H₂ O', '2H₂O'), 6, 'The scheme prices the balanced equation (2 × 3).')],
    qtext=_copy, stem=f'{Q6_LEAD} {_burned}', cid='q6-b-balanced-equation', ref_suffix='the balanced equation',
    figure=Q6)
_q6c = P.items(k('6', 'c'))
assert [it.cell for it in _q6c] == ['[6 + 6]'] and len(_q6c[0].points()) == 2, _q6c
_lpg = _q6c[0].points()
C.add([k('6', 'c')], 'chem-2-4', 'lpg', [
    lift('r-1', _lpg[0], 6, 'For "What do the letters LPG stand for?" The scheme prices this point and the next '
         '(6 + 6), one each.'),
    lift('r-2', _lpg[1], 6, 'For "Name another substance found in LPG."')], stem=Q6_LEAD, figure=Q6)
# (d): three asks priced by cells of their own: the octane number (6), then C
# or D and why (2 × 3), then lead compounds, why added and why stopped (2 × 3).
_q6d_ask = P.ask(k('6', 'd'))
_q6d = P.items(k('6', 'd'))
assert [it.cell for it in _q6d] == ['[6]', '[2 × 3]', '[2 × 3]'], _q6d
_cd, _lead = _q6d[1].points(), _q6d[2].points()
assert _cd == ['D', 'shorter chain / branched'] and len(_lead) == 2, (_cd, _lead)
C.add([k('6', 'd')], 'chem-2-4', 'octane-number', [lift('r-1', _q6d[0].text, 6)],
      qtext=cut(_q6d_ask, None, 'Would you expect'), stem='')
C.add([k('6', 'd')], 'chem-2-4', 'branching-and-octane-number', [
    lift('r-1', _cd[0], 3, 'For "Would you expect compound C or compound D ...?" The scheme prices this point and '
         'the next (2 × 3), one each.'),
    lift('r-2', _cd[1], 3, 'For "Give a reason for your answer."')],
    qtext=cut(_q6d_ask, 'Would you expect', 'Why were lead'), stem=Q6_LEAD, figure=Q6, cid='q6-d-c-or-d',
    ref_suffix='compound C or D')
C.add([k('6', 'd')], 'chem-2-4', 'lead-compounds-in-motor-fuel', [
    lift('r-1', _lead[0], 3, 'For "Why were lead compounds added ...?" The scheme prices this point and the next '
         '(2 × 3), one each.'),
    lift('r-2', _lead[1], 3, 'For "Why was the addition ... discontinued?"')],
    qtext=cut(_q6d_ask, 'Why were lead'), stem='', cid='q6-d-lead-compounds', ref_suffix='lead compounds')

# ── Q7 Acids, bases and pH ───────────────────────────────────────────────────
# (a): "Define (i) acid, (ii) base." is one sentence; the scheme prices the two
# definitions "(2 × 4)", one cell: one card, four each. The ask after it,
# "What is meant by the term neutralisation?", is priced (9): a card of its own.
_q7a_ask = P.ask(k('7', 'a'))
_q7a = [P.items(k('7', 'a', r)) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _q7a] == [[None], ['[2 × 4]', '[9]']], _q7a
_acid = bare(_q7a[0][0].text)
assert ', H + ) donor' in _acid and 'H₃O⁺ )' in _acid, _acid
_acid = P.rearranged(P.rearranged(_acid, ', H + ) donor', ', H⁺) donor'), 'H₃O⁺ )', 'H₃O⁺)')
_base = _q7a[1][0].text
assert 'H⁺ ) acceptor' in _base, _base
_base = P.rearranged(_base, 'H⁺ ) acceptor', 'H⁺) acceptor')
C.add([k('7', 'a', 'i'), k('7', 'a', 'ii')], 'chem-3-4', 'definitions-of-an-acid-and-a-base', [
    lift('r-1', _acid, 4, 'For (i). The scheme prices this point and the next (2 × 4), one each.'),
    lift('r-2', _base, 4, 'For (ii).')],
    qtext=cut(_q7a_ask, None, 'What is meant'), stem='')
C.add([k('7', 'a')], 'chem-3-4', 'neutralisation', [lift('r-1', _q7a[1][1].text, 9)],
      qtext=cut(_q7a_ask, 'What is meant'), stem='', cid='q7-a-neutralisation',
      ref_suffix='after (ii), neutralisation')
# (b): "Define pH." (2 × 3), then how to measure it (6). The reader sets the
# scheme's "[H⁺]" as "[H +]" (its superscript plus printed as a run of its own).
assert cells(k('7', 'b')) == ['[2 × 3]', '[6]'], P.items(k('7', 'b'))
C.fixed([k('7', 'b')], 'chem-3-4', 'defining-and-measuring-ph', fixes={'[H +] / [H₃O⁺ ]': '[H⁺] / [H₃O⁺]'},
        row_notes={0: 'For "Define pH."', 2: 'For "How would you measure the pH ...?"'})
# (c): "(i) ..., (ii) ..." set inside one sentence; the scheme prices the two
# answers (6 + 6), one each, and boxes the working, with its marks, beneath.
_q7c1, _q7c2 = P.items(k('7', 'c', 'i')), P.items(k('7', 'c', 'ii'))
assert [it.cell for it in _q7c1] == ['[3]', '[3]'] and _q7c1[0].points()[0] == '2', _q7c1
assert [it.cell for it in _q7c2] == ['[6 + 6]', '[6]'] and _q7c2[0].text == '12', _q7c2
_q7c_ask = P.ask(k('7', 'c'))
C.add([k('7', 'c', 'i'), k('7', 'c', 'ii')], 'chem-3-4', 'ph-of-a-strong-acid-and-a-strong-base', [
    lift('r-1', _q7c1[0].points()[0], 6, 'For (i). The scheme prices this answer and the next (6 + 6), one each.'),
    lift('r-2', _q7c2[0].text, 6, 'For (ii).')],
    qtext=_q7c_ask, stem='', figure=S + 'q7c',
    notes='The scheme sets out the working that earns each answer in a box, with the marks for each step; its own '
          'print is shown with the answer.')
# (d): "(i) is neutral, (ii) is basic" (2 × 3), then the beer diluted (3).
_q7d1, _q7d2 = P.items(k('7', 'd', 'i')), P.items(k('7', 'd', 'ii'))
assert [it.cell for it in _q7d1] == [None] and [it.cell for it in _q7d2] == ['[2 × 3]', '[3]'], (_q7d1, _q7d2)
C.add([k('7', 'd')], 'chem-3-4', 'ph-of-beer-water-and-saliva', [
    lift('r-1', bare(_q7d1[0].text), 3, 'For (i). The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _q7d2[0].text, 3, 'For (ii).'),
    lift('r-3', _q7d2[1].text, 3, 'For "If a large volume of pure water were added to the beer ...?"')], stem='')

# ── Q8 Ethanol, ethanal, ethanoic acid and ethene ────────────────────────────
Q8 = FIG + 'paper-q8'
assert cells(k('8', 'a')) == ['[5 + 3]'], P.items(k('8', 'a'))
C.ordered([k('8', 'a')], 'chem-4-2', 'naming-ethene-and-ethanol', figure=Q8)
# (b): the drawing's two parts (3) and (3), then four points priced (3 × 3): a
# cell pricing fewer points than the scheme lists is a choice, any three of
# the four, three each. The scheme's drawing (its labels are 'scheme-labels')
# is the answer picture; the reaction scheme naming W and A is the question's.
_q8b = P.items(k('8', 'b'))
assert [it.cell for it in _q8b] == ['[3]', '[3]', '[3 × 3]'], _q8b
_prep = [lift('x', t, None)['verbatim'] for t in _q8b[2].points()]
assert len(_prep) == 4, _prep
C.add([k('8', 'b')], 'chem-u2', 'preparing-and-collecting-ethene', [
    lift('r-1', _q8b[0].text, 3),
    lift('r-2', _q8b[1].text, 3),
    anyN('r-3', _prep[0], 9, 3, 3, _prep, 'Any three of these: the scheme lists four points and prices them (3 × 3).')],
    total=15, figure=S + 'q8b', notes='The scheme draws the apparatus above these points; its own print is shown '
                                      'with the answer.')
print_question('paper-q8b-print')
# (c)(i)-(iii): one cell (6 + 6 + 3) closes the three parts.
assert [cells(k('8', 'c', r)) for r in ('i', 'ii', 'iii')] == [[None], [None], ['[6 + 6 + 3]']]
C.ordered([k('8', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-4-2', 'identifying-ethanoic-acid-ethanol-and-ethanal',
          figure=Q8, row_notes={0: 'For (i).', 1: 'For (ii).', 2: 'For (iii).'})
assert cells(k('8', 'd')) == ['[3]', '[2 × 3]', '[3]'], P.items(k('8', 'd'))
C.fixed([k('8', 'd')], 'chem-4-2', 'carboxylic-acids-and-carbon-dioxide', figure=Q8,
        row_notes={0: 'For "What gas is produced ...?"', 1: 'For "How could you test for this gas?"',
                   3: 'For "What other carboxylic acid ...?"'})

# ── Q9 Hard water and sewage treatment ───────────────────────────────────────
# (a): five asks, priced (6), (6), (6), (2 × 3), (2 × 3) (scheme PDF page 14):
# what hard water is, the limestone district (yes, and why), temporary and
# permanent hardness, an advantage and a disadvantage -- a card each.
_q9a_ask = P.ask(k('9', 'a'))
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a] == ['[6]', '[6]', '[6]', '[2 × 3]', '[2 × 3]'], _q9a
C.add([k('9', 'a')], 'chem-4-3', 'what-hard-water-is', [lift('r-1', _q9a[0].text, 6)],
      qtext=cut(_q9a_ask, None, 'Would you expect'))
# The reason's subscripts: the reader sets the "2" of H₂CO₃ apart ("H 2CO₃") and
# files the "3" of CaCO₃ (scheme page 14, x 425, y 153) at the start of the
# next row, where the scheme prints none; both set back where the page prints them.
_why = _q9a[2].text
_dist = _q9a[3].points()
assert _why.endswith('(calcium carbonate, CaCO )') and _dist[0] == '3' and _q9a[3].text.startswith('3 temporary:'), \
    (_why, _dist)
_why = P.rearranged(_why + ' 3', 'CaCO ) 3', 'CaCO₃)')
_why = P.rearranged(P.rearranged(_why, 'H 2CO₃ )', 'H₂CO₃)'), 'Ca²⁺ )', 'Ca²⁺)')
_allow = _q9a[3].asides
assert _allow == ['[Allow 3 marks for ‘contains calcium’.]'], _allow
C.add([k('9', 'a')], 'chem-4-3', 'hard-water-in-a-limestone-district', [
    lift('r-1', _q9a[1].text, 6, 'For "Would you expect the water supply in a limestone district to be hard?"'),
    lift('r-2', _why, 6, 'For "Give a reason for your answer." ' + adds(_allow))],
    qtext=cut(_q9a_ask, 'Would you expect', 'Distinguish between'), cid='q9-a-limestone-district',
    ref_suffix='a limestone district')
assert len(_dist) == 3, _dist
C.add([k('9', 'a')], 'chem-4-3', 'temporary-and-permanent-hardness', [
    lift('r-1', _dist[1], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _dist[2], 3)],
    qtext=cut(_q9a_ask, 'Distinguish between', 'State one advantage'), cid='q9-a-temporary-and-permanent',
    ref_suffix='temporary and permanent hardness')
_adv = _q9a[4].points()
assert len(_adv) == 2 and _adv[0].startswith('advantage:'), _adv
C.add([k('9', 'a')], 'chem-4-3', 'advantages-and-disadvantages-of-hard-water', [
    lift('r-1', _adv[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _adv[1], 3)],
    qtext=cut(_q9a_ask, 'State one advantage'), cid='q9-a-advantage-and-disadvantage',
    ref_suffix='an advantage and a disadvantage')
# (b): five blanks, (5 × 4): five each priced, four each; the passage with its
# numbered blanks is the paper's print.
assert cells(k('9', 'b')) == ['[5 × 4]'] and len(P.items(k('9', 'b'))[0].points()) == 5, P.items(k('9', 'b'))
C.fixed([k('9', 'b')], 'chem-4-3', 'sewage-treatment', notes='Each answer is numbered by its blank.')
print_question('paper-q9b-print')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
assert cells(k('10', 'a', 'i')) == ['[4 × 3]'], P.items(k('10', 'a', 'i'))
C.fixed([k('10', 'a', 'i')], 'chem-u2', 'flame-test-procedure')
C.fixed([k('10', 'a', 'ii')], 'chem-u2', 'test-for-the-chloride-ion')
# (iii): the scheme completes the table (its entries are 'scheme-labels') and
# prices it "correct flame colour // correct anion test result (4 + 3)"; the
# rows are its two entries, the table the paper prints is the question's.
_q10a3 = P.items(k('10', 'a', 'iii'))
assert [(it.cell, it.text) for it in _q10a3] == [('[4 + 3]', 'correct flame colour // correct anion test result')], \
    _q10a3
_crit = _q10a3[0].text.split(' // ')
C.add([k('10', 'a', 'iii')], 'chem-u2', 'flame-test-and-chloride-test-results-for-lithium-chloride', [
    lift('r-1', 'Crimson (Red)', None, 'The flame test result. The scheme\'s criterion: "' + traced(_crit[0]) + '".'),
    lift('r-2', 'White Precipitate', None, 'The chloride test observation. The scheme\'s criterion: "'
         + traced(_crit[1]) + '".')],
    kind='orderedSplit', notation='[4 + 3]', total=7,
    notes=SPLIT.format('(4 + 3)') + ' The scheme sets the two entries in the completed table; its own print is shown '
                                    'with the answer.', figure=S + 'q10a-iii')
print_question('paper-q10a-iii-print')
# (b): four asks, each printed with its mark ((6), (6), (6), (7)) and priced by
# cells of its own (scheme PDF page 15), the third "How many (i) moles ...,
# (ii) molecules ...?" with the scheme's romans: a card each.
_q10b_ask = P.ask(k('10', 'b'))
_q10b = P.items(k('10', 'b'))
assert [it.cell for it in _q10b] == ['[6]', '[2 × 3]'], _q10b
_q10b1 = P.items(k('10', 'b', 'i'))
assert [it.cell for it in _q10b1] == ['[2 × 3]', '[3]', '[7]'], _q10b1
C.add([k('10', 'b')], 'chem-1-1', 'particles-move-fastest-in-a-gas', [lift('r-1', _q10b[0].text, 6)],
      qtext=cut(_q10b_ask, None, 'State Boyle'), stem='')
_boyle = _q10b[1].points()
_law = 'pressure is inversely proportional to volume / pV = k / p ∝ V / p₁V₁ = p₂V₂ 1'
assert len(_boyle) == 2 and _boyle[1] == _law, _boyle
# The scheme sets "p ∝ 1/V" as a fraction, its "1" over the "V" (page 15, x 420,
# y 407): given in the one form the gate finds, with a note.
C.add([k('10', 'b')], 'chem-2-3', 'boyles-law', [
    lift('r-1', _boyle[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', 'pressure is inversely proportional to volume / pV = k / p ∝ 1/V / p₁V₁ = p₂V₂', 3,
         'The scheme sets "p ∝ 1/V" as a fraction.')],
    qtext=cut(_q10b_ask, 'State Boyle', 'A sample of ammonia'), stem='', cid='q10-b-boyles-law',
    ref_suffix='Boyle’s law')
_moles = _q10b1[0].text.split(' // (ii) ')
assert _moles == ['O.5 mol', '3 × 10²³ molecules'], _moles
C.add([k('10', 'b', 'i'), k('10', 'b', 'ii')], 'chem-1-4', 'moles-and-molecules-of-ammonia', [
    lift('r-1', _moles[0], 3, 'For (i). The scheme prices this answer and the next (2 × 3), one each.'),
    lift('r-2', _moles[1], 3, 'For (ii).')],
    qtext=cut(_q10b_ask, 'How many', 'Name the process'), stem=cut(_q10b_ask, 'A sample of ammonia', 'How many'),
    figure=S + 'q10b-i',
    notes='The scheme sets out the working that earns each answer in a box, (3) a step; its own print is shown with '
          'the answer.')
C.add([k('10', 'b')], 'chem-1-1', 'diffusion', [lift('r-1', _q10b1[2].text, 7)],
      qtext=cut(_q10b_ask, 'Name the process'), stem='', figure=FIG + 'paper-q10b', cid='q10-b-diffusion',
      ref_suffix='after (ii), the white ring')
# (c): the paper underlines "chemical equilibrium" and prints the equation with
# an arrow the text layer reads as another glyph; (i) and (ii) take the paper's
# print as their question, (iii) the chemist's photograph and (iv) the equation.
C.fixed([k('10', 'c', 'i')], 'chem-3-3', 'definition-of-chemical-equilibrium')
print_question('paper-q10c-i-print')
# (ii): the Kc expression is a fraction (its print is 'scheme-labels').
C.drawn([k('10', 'c', 'ii')], 'chem-3-3', 'kc-expression-for-the-haber-equilibrium', S + 'q10c-ii')
print_question('paper-q10c-ii-print')
Q10C_CHEMIST = P.lead(k('10', 'c', 'ii'))
assert Q10C_CHEMIST.startswith('The French industrial chemist, pictured on the right'), Q10C_CHEMIST
C.fixed([k('10', 'c', 'iii')], 'chem-3-3', 'le-chatelier', stem=Q10C_CHEMIST, figure=FIG + 'paper-q10c-photo')
C.fixed([k('10', 'c', 'iv')], 'chem-3-3', 'pressure-and-the-ammonia-equilibrium', figure=FIG + 'paper-q10c-eq')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): six descriptions, "ANY FIVE: (5 × 5)": any five, five each; the terms and
# the table of descriptions are the paper's print.
C.menu([k('11', 'a')], 'chem-u2', 'separation-techniques', claim=5,
       note='The scheme prices the part "' + traced('ANY FIVE: (5 × 5)') + '".')
print_question('paper-q11a-print')
# (b): "Define (i) oxidation, (ii) reduction" (2 × 3); "Identify (iii) ..., (iv)
# ..., (v) ..." (6 + 2 × 3); then above or below, and why (4 + 3). The paper sets
# the romans inside its sentences; the scheme numbers them.
_q11b_ask = P.ask(k('11', 'b'))
_zinc = cut(_q11b_ask, 'When a zinc rod', 'Identify')
assert _zinc.endswith('Zn + Cu²⁺ → Zn²⁺ + Cu'), _zinc
_q11b = {r: P.items(k('11', 'b', r)) for r in ('i', 'ii', 'iii', 'iv', 'v')}
assert {r: [it.cell for it in x] for r, x in _q11b.items()} == {
    'i': [None], 'ii': ['[2 × 3]'], 'iii': [None], 'iv': [None], 'v': ['[6 + 2 × 3]', '[4 + 3]']}, _q11b
C.add([k('11', 'b', 'i'), k('11', 'b', 'ii')], 'chem-3-5', 'oxidation-and-reduction-as-electron-transfer', [
    lift('r-1', bare(_q11b['i'][0].text), 3, 'For (i). The scheme prices this point and the next (2 × 3), one each.'),
    lift('r-2', _q11b['ii'][0].text, 3, 'For (ii).')],
    qtext=cut(_q11b_ask, None, 'When a zinc rod'), stem='')
# (v): the reader sets the scheme's "Cu²⁺" as "Cu 2+" (its superscript printed
# as a run of its own, page 16, x 184, y 289).
_v = _q11b['v'][0].text
assert _v == 'Cu 2+', _v
C.add([k('11', 'b', r) for r in ('iii', 'iv', 'v')], 'chem-3-5', 'species-oxidised-reduced-and-the-oxidising-agent', [
    lift('r-1', bare(_q11b['iii'][0].text), None, 'For (iii).'),
    lift('r-2', bare(_q11b['iv'][0].text), None, 'For (iv).'),
    lift('r-3', P.rearranged(_v, 'Cu 2+', 'Cu²⁺'), None, 'For (v).')],
    kind='orderedSplit', notation='[6 + 2 × 3]', total=12, notes=SPLIT.format('(6 + 2 × 3)'),
    qtext=cut(_q11b_ask, 'Identify', 'Is zinc'), stem=_zinc)
_series = _q11b['v'][1].points()
assert len(_series) == 2 and _series[0] == 'above', _series
C.add([k('11', 'b')], 'chem-3-5', 'zinc-and-copper-in-the-electrochemical-series', [
    lift('r-1', _series[0], None, 'For "Is zinc (Zn) placed above or below copper (Cu) ...?"'),
    lift('r-2', _series[1], None, 'For "Give a reason for your answer."')],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('(4 + 3)'),
    qtext=cut(_q11b_ask, 'Is zinc'), stem=_zinc, cid='q11-b-electrochemical-series',
    ref_suffix='after (v), the electrochemical series')
# (c)A: two asks before (i), (2 × 3) and (4); then the case study.
assert cells(ka('11', 'c', None, 'A')) == ['[2 × 3]', '[4]'], P.items(ka('11', 'c', None, 'A'))
C.fixed([ka('11', 'c', None, 'A')], 'chem-u3', 'batch-and-continuous-processes-and-energy-costs',
        row_notes={0: 'For "Distinguish between the two."', 2: 'For "Suggest one way of reducing energy costs ..."'})
Q11CA_STUDY = P.lead(ka('11', 'c', None, 'A'))
assert Q11CA_STUDY.startswith('Answer the following questions in relation to the chemical process'), Q11CA_STUDY
# (i), (ii): the candidate chooses the process, so the scheme prints only what
# the examiner looks for -- "location", "name of product", "use of product" --
# and that criterion is the row, as printed; the reasons are "ANY TWO:(2 × 3)".
CHOSEN = ('The scheme prints only the criterion "{}" for this: the answer depends on which process the '
          'candidate studied.')
_ca1 = P.items(ka('11', 'c', 'i', 'A'))
assert [(it.cell, it.text) for it in _ca1][0] == ('[3]', 'location') and _ca1[1].cell == '[2 × 3]' \
    and _ca1[1].asides == ['[any two]'], _ca1
_reasons = [lift('x', o, None)['verbatim'] for o in _ca1[1].options()]
assert len(_reasons) == 5, _reasons
C.add([ka('11', 'c', 'i', 'A')], 'chem-u3', 'location-of-an-irish-chemical-process', [
    lift('r-1', _ca1[0].text, 3, 'For "State the location ...". ' + CHOSEN.format('location')),
    anyN('r-2', _reasons[0], 6, 2, 3, _reasons, 'For "Suggest two reasons ...". Any two of these: the scheme prices '
         'them "' + traced('ANY TWO:(2 × 3)') + '".')], total=9, stem=Q11CA_STUDY)
_ca2 = P.items(ka('11', 'c', 'ii', 'A'))
assert [(it.cell, it.text) for it in _ca2] == [('[2 × 3]', 'name of product // use of product')], _ca2
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-u3', 'product-of-an-irish-chemical-process', stem=Q11CA_STUDY,
        row_notes={0: CHOSEN.format('name of product'), 1: CHOSEN.format('use of product')})
# (c)B: (i)-(ii) one cell (2 × 5), five each; (iii)-(v) a cell each.
Q11CB_DIAMOND = FIG + 'paper-q11c-b-diamond'
Q11CB_NACL = FIG + 'paper-q11c-b-nacl'
_cb = [P.items(ka('11', 'c', r, 'B')) for r in ('i', 'ii')]
assert [[it.cell for it in x] for x in _cb] == [[None], ['[2 × 5]']], _cb
C.add([ka('11', 'c', 'i', 'B'), ka('11', 'c', 'ii', 'B')], 'chem-2-1', 'diamond-and-the-allotropes-of-carbon', [
    lift('r-1', bare(_cb[0][0].text), 5, 'For (i). The scheme prices this point and the next (2 × 5), one each.'),
    lift('r-2', _cb[1][0].text, 5, 'For (ii).')], figure=Q11CB_DIAMOND)
Q11CB_NACL_LEAD = P.lead(ka('11', 'c', 'ii', 'B'))
assert Q11CB_NACL_LEAD == 'A small part of the cubic crystal lattice of sodium chloride is also shown.', Q11CB_NACL_LEAD
assert cells(ka('11', 'c', 'iii', 'B')) == ['[2 × 3]'], P.items(ka('11', 'c', 'iii', 'B'))
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-2-1', 'particles-in-a-sodium-chloride-crystal', stem=Q11CB_NACL_LEAD,
        figure=Q11CB_NACL)
C.fixed([ka('11', 'c', 'iv', 'B')], 'chem-2-1', 'binding-forces-in-a-sodium-chloride-crystal',
        stem=Q11CB_NACL_LEAD, figure=Q11CB_NACL)
# (v): the scheme's page prints "Blank Page" under its answer.
C.fixed([ka('11', 'c', 'v', 'B')], 'chem-2-1', 'x-ray-crystallography', stem=Q11CB_NACL_LEAD, figure=Q11CB_NACL,
        skip=('Blank Page',))


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
    """Every letter's printed marks, alternatives apart: the paper prints Q6(b),
    Q6(d), Q7(a), Q7(b), Q9(a), Q10(a)-(c), Q11(b) and Q11(c) in subtotals ("(6)"
    then "(12)"), so the sum of every mark printed under the letter, not the last."""
    out = {}
    for s in P.pseg:
        q, letter, _roman, alt = s.key
        if letter and s.marks_at:
            out[(q, letter, alt)] = out.get((q, letter, alt), 0) + sum(m for _n, m in s.marks_at)
    for (q, letter, _r, _a), m in P.marks.items():
        if letter and not any(key[:2] == (q, letter) for key in out):
            out[(q, letter, None)] = m
    # Two subtotals print at the end of a line of words, which the reader strips
    # from the ask without recording where they fell: Q6(b)'s second "(6)" after
    # "... and balance it." (paper page 5) and Q10(a)(i)'s "(12)" after "... a
    # flame test on the solid." (page 6). They are added to their letters here.
    for key, (page, tail, m) in {('6', 'b', None): (5, 'and balance it. (6)', 6),
                                 ('10', 'a', None): (6, 'test on the solid. (12)', 12)}.items():
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
