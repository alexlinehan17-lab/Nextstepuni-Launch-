#!/usr/bin/env python3
"""2023 Ordinary Level Chemistry, re-carded part by part from the paper and the labelled scheme.

    python3 scripts/markbank/authoring/chem_audit_2023_ol.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2023_ol.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2023 ol    # write them

Drafted by chem_draft.py and corrected card by card, the way
chem_audit_2023_hl.py re-cards 2023 HL: the scheme is the labelled ("cue")
layout and does not reprint the question, so every question text, stem and
lead-in is the PAPER's print of its part and every marking point is the
SCHEME's answer closed by its own mark cell. The Ordinary scheme prices many
letters with one cell for all their parts ("(6 + [6 × 3])" under Q3(b)(v));
those letters are one orderedSplit card each.

Pre-audit ids are kept (a card that joined parts priced by separate cells
keeps its id on its first part; later parts are new cards); WITHDRAWN lists the
pre-audit cards that duplicated another or held a piece of a task the scheme
prices as one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, point  # noqa: E402

P = Printed(2023, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2023-OL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'


def k(*parts):
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {
    'chem-2023-ol-q1-c-ii': (
        'chem-2023-ol-q1-c-i',
        'The scheme prices Q1(c)(i)-(iii) with one cell ([6 + 6 + 3 + 3]), so they are one task; '
        'carded once, as chem-2023-ol-q1-c-i.'),
    'chem-2023-ol-q1-c-iii': (
        'chem-2023-ol-q1-c-i',
        'The scheme prices Q1(c)(i)-(iii) with one cell ([6 + 6 + 3 + 3]); carded once, as '
        'chem-2023-ol-q1-c-i.'),
    'chem-2023-ol-q1-d-iii': (
        'chem-2023-ol-q1-d-i-ii',
        'The scheme prices Q1(d)(i)-(iii) with one cell ([7 + 3 + 2]); carded once, as '
        'chem-2023-ol-q1-d-i-ii.'),
    'chem-2023-ol-q3-b-ii-iii': (
        'chem-2023-ol-q3-b-i',
        'The scheme prices Q3(b)(i)-(v) with one cell ((6 + [6 × 3])); carded once, as '
        'chem-2023-ol-q3-b-i.'),
    'chem-2023-ol-q3-b-iv-v': (
        'chem-2023-ol-q3-b-i',
        'The scheme prices Q3(b)(i)-(v) with one cell ((6 + [6 × 3])); carded once, as '
        'chem-2023-ol-q3-b-i.'),
    'chem-2023-ol-q5-a-ii-iii': (
        'chem-2023-ol-q5-a-i',
        'The scheme prices Q5(a)(i)-(iii) with one cell ([9 + 6 + 3]); carded once, as '
        'chem-2023-ol-q5-a-i.'),
    'chem-2023-ol-q6-a-ii-iii': (
        'chem-2023-ol-q6-a-i',
        'The scheme prices Q6(a)(i)-(iii) with one cell ([6 + 4 + 2 + 2]); carded once, as '
        'chem-2023-ol-q6-a-i.'),
    'chem-2023-ol-q6-b-i-iv': (
        'chem-2023-ol-q6-b',
        'Duplicated chem-2023-ol-q6-b (both cited Q6(b)(i)-(iv)).'),
    'chem-2023-ol-q6-c-ii': (
        'chem-2023-ol-q6-c',
        'The scheme prices Q6(c)(i)-(ii) with one cell ([8 + 2 + 2]); carded once, as '
        'chem-2023-ol-q6-c.'),
    'chem-2023-ol-q7-d-iv': (
        'chem-2023-ol-q7-d-iii',
        'The scheme prices Q7(d)(iii)-(iv) with one cell ([9 + 3]); carded once, as '
        'chem-2023-ol-q7-d-iii.'),
    'chem-2023-ol-q8-b-ii': (
        'chem-2023-ol-q8-b',
        'The scheme prices Q8(b)(i)-(ii) with one cell ([8 + 2 + 2]); carded once, as '
        'chem-2023-ol-q8-b.'),
    'chem-2023-ol-q10-a-iii-iv-fig': (
        'chem-2023-ol-q10-a-iii-iv',
        'Duplicated chem-2023-ol-q10-a-iii-iv (both cited Q10(a)(iii)-(iv)).'),
    'chem-2023-ol-q10-b-iii-v': (
        'chem-2023-ol-q10-b-i-ii',
        'The scheme prices Q10(b)(i)-(vi) with one cell ((6 + 4 + [5 × 3])); carded once, as '
        'chem-2023-ol-q10-b-i-ii.'),
    'chem-2023-ol-q10-b-vi': (
        'chem-2023-ol-q10-b-i-ii',
        'The scheme prices Q10(b)(i)-(vi) with one cell ((6 + 4 + [5 × 3])); carded once, as '
        'chem-2023-ol-q10-b-i-ii.'),
}

# ── Q1 Preparing ethyne ──────────────────────────────────────────────────────
Q1 = FIG + 'paper-p02-i0'
C.ordered([k('1', 'a', 'i'), k('1', 'a', 'ii')], None, None, cid='q1-a-fig', figure=Q1)
C.ordered([k('1', 'b', 'i'), k('1', 'b', 'ii')], None, None, cid='q1-b', figure=Q1)
C.ordered([k('1', 'c', 'i'), k('1', 'c', 'ii'), k('1', 'c', 'iii')], 'chem-2-4',
          'ethyne-structure-unsaturation-and-bromine-test', cid='q1-c-i', figure=Q1)
C.ordered([k('1', 'd', 'i'), k('1', 'd', 'ii'), k('1', 'd', 'iii')], 'chem-u2',
          'combustion-test-and-use-of-ethyne', cid='q1-d-i-ii', figure=Q1)

# ── Q2 Titrating sodium carbonate with hydrochloric acid ─────────────────────
Q2 = FIG + 'paper-p03-i0'
C.fixed([k('2', 'a')], None, None, figure=Q2)
C.fixed([k('2', 'b', 'i')], None, None, cid='q2-b-i-fig', figure=Q2)
C.fixed([k('2', 'b', 'ii')], None, None, cid='q2-b-ii-fig', figure=Q2)
C.fixed([k('2', 'b', 'iii')], None, None, cid='q2-b-iii-fig', figure=Q2)
C.fixed([k('2', 'b', 'iv')], None, None, figure=Q2)
C.fixed([k('2', 'c', 'i')], 'chem-4-1', 'indicator-for-carbonate-titration', cid='q2-c',
        figure=Q2)
C.fixed([k('2', 'c', 'ii')], 'chem-4-1', 'methyl-orange-colour-change-at-end-point', figure=Q2)
C.fixed([k('2', 'd', 'i')], None, None, figure=Q2)
C.route([k('2', 'd', 'ii')], None, None, figure=Q2)
# Its only figure is the scheme's working, held back until the reveal, so the lead-in's sentence
# "Some pieces of apparatus used to carry out the titration are shown below." would point at
# nothing. Nothing in (d)(iii) depends on the apparatus: the concentration comes from the 25.0 cm³
# of 0.05 M sodium carbonate, the equation and the titres, which the stem's other sentences print.
# That sentence is left out of this card's stem.
_Q2_APPARATUS = 'Some pieces of apparatus used to carry out the titration are shown below.'
_q2d3_lead = C.context(k('2', 'd', 'iii'))
assert _q2d3_lead.count(_Q2_APPARATUS) == 1 and _q2d3_lead.endswith('22.5 cm³ 22.4 cm³'), _q2d3_lead
_before, _after = _q2d3_lead.split(_Q2_APPARATUS)
C.answer_only([k('2', 'd', 'iii')], None, None, S + 'q2d-iii', stem=_before.strip() + ' ' + _after.strip())

# ── Q3 Estuary water ─────────────────────────────────────────────────────────
C.ordered([k('3', 'a', 'i')], None, None, figure=S + 'q3a-i')
C.ordered([k('3', 'a', 'ii')], None, None)
C.route([k('3', 'a', 'iii')], 'chem-4-3', 'suspended-solids-in-grams-per-litre', cid='q3-a-iii-iv')
C.route([k('3', 'a', 'iv')], 'chem-4-3', 'suspended-solids-in-mg-per-litre')
C.ordered([k('3', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-4-3',
          'tests-for-chloride-nitrate-and-sodium-ions', cid='q3-b-i', figure=FIG + 'paper-q3b-table')

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], None, None, notes=Q4_NOTE)
C.drawn([k('4', 'b')], 'chem-2-1', 'dot-and-cross-diagram-of-hydrogen', S + 'q4b', notes=Q4_NOTE)
for letter in ('c', 'd', 'e'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.route([k('4', 'f')], None, None, figure=S + 'q4f', notes=Q4_NOTE)
for letter in ('g', 'h', 'i'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.route([k('4', 'j')], None, None, figure=S + 'q4j', notes=Q4_NOTE,
        fixes={'% Ti = 48 80 × 100 = 60%': '% Ti = 48 ÷ 80 × 100 = 60%'},
        row_notes={1: FRACTION.format('48', '80')})
C.ordered([k('4', 'k', 'i'), k('4', 'k', 'ii')], None, None, cid='q4-k-fig',
          figure=FIG + 'paper-p06-i0', notes=Q4_NOTE,
          label_key=[{'letter': 'X', 'meaning': 'Liebig (reflux) condenser',
                      'askedInThisQuestion': True}])
C.fixed([ka('4', 'l', None, 'A')], None, None, cid='q4-l-a', notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'B')], None, None, cid='q4-l-b', notes=Q4_NOTE)

# ── Q5 The periodic table ────────────────────────────────────────────────────
C.ordered([k('5', 'a', 'i'), k('5', 'a', 'ii'), k('5', 'a', 'iii')], 'chem-1-3',
          'elements-and-mendeleevs-periodic-table', cid='q5-a-i')
C.fixed([k('5', 'b', 'i')], 'chem-1-2', 'atomic-number-definition', cid='q5-b-i-ii-iii')
C.fixed([k('5', 'b', 'ii')], 'chem-1-2', 'atomic-number-of-lithium')
# The paper sets the nuclide's mass and atomic numbers around its symbol; the
# text layer reads them on the line. The same characters, set as printed.
C.fixed([k('5', 'b', 'iii')], 'chem-1-2', 'neutrons-in-lithium-7',
        qtext=P.rearranged(P.ask(k('5', 'b', 'iii')), 'Li 7 ? 3', '⁷₃Li?'))
C.fixed([k('5', 'b', 'iv')], 'chem-1-2', 'electron-arrangement-of-lithium', cid='q5-b-iv-v-vi')
C.fixed([k('5', 'b', 'v')], 'chem-1-2', 'electron-arrangement-of-neon')
C.fixed([k('5', 'b', 'vi')], 'chem-1-2', 'reactivity-of-lithium-and-neon-from-electrons')
C.ordered([k('5', 'c', 'i'), k('5', 'c', 'ii')], None, None, cid='q5-c', figure=FIG + 'paper-q5c')

# ── Q6 Methane and natural gas ───────────────────────────────────────────────
C.ordered([k('6', 'a', 'i'), k('6', 'a', 'ii'), k('6', 'a', 'iii')], 'chem-4-3',
          'methane-sources-formula-and-hydrocarbons', cid='q6-a-i')
C.ordered([k('6', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], None, None, cid='q6-b')
C.fixed([k('6', 'b', 'v')], None, None)
C.ordered([k('6', 'c', 'i'), k('6', 'c', 'ii')], 'chem-2-4', 'aromatic-and-aliphatic-compounds',
          cid='q6-c', figure=FIG + 'paper-q6c')

# ── Q7 Acids and bases ───────────────────────────────────────────────────────
C.ordered([k('7', 'a')], None, None, deep=True)
C.fixed([k('7', 'b', 'i')], 'chem-3-4', 'neutralisation-word-equation', cid='q7-b')
# Q7(b)(ii): one equation, priced by what it gets right: the scheme sets
# "two correct molecular formulae: (2 + 2)" and "full balanced equation: (2)"
# beneath it. One row for the equation, worth the part's 6.
_q7b2 = P.items(k('7', 'b', 'ii'))
assert [it.cell for it in _q7b2] == ['[2 + 2]', '[2]'], _q7b2
assert _q7b2[0].text.endswith(' two correct molecular formulae:'), _q7b2
C.add([k('7', 'b', 'ii')], 'chem-3-4', 'balanced-equation-for-hcl-and-koh', [
    C.lifted('r-1', _q7b2[0].text[:-len(' two correct molecular formulae:')], 6,
             'The scheme gives (2 + 2) for two correct molecular formulae and (2) for the full '
             'balanced equation.')])
C.fixed([k('7', 'c', 'i')], 'chem-3-4', 'household-or-garden-base', cid='q7-c')
C.fixed([k('7', 'c', 'ii')], 'chem-3-4', 'use-of-a-household-base',
        row_notes={0: 'The scheme prices any one use (3); the uses it lists after a named base '
                      'are for that base.'})
C.fixed([k('7', 'd', 'i')], 'chem-3-4', 'ph-definition', cid='q7-d-i-ii')
C.route([k('7', 'd', 'ii')], 'chem-3-4', 'ph-of-dilute-nitric-acid')
C.ordered([k('7', 'd', 'iii'), k('7', 'd', 'iv')], 'chem-u2', 'measuring-ph', cid='q7-d-iii')

# ── Q8 Reaction scheme from ethanol ──────────────────────────────────────────
Q8 = FIG + 'paper-q8-fig0'
C.ordered([k('8', 'a', 'i')], 'chem-4-2', 'iupac-names-of-ethanol-ethanal-ethanoic-acid',
          figure=Q8)
C.fixed([k('8', 'a', 'ii')], None, None, figure=Q8)
# Q8(b): the scheme draws (i)'s structure, then "CIRCLE: OH circled", then
# (ii)'s answer, and prices all three [8 + 2 + 2]. The drawing's row is the
# paper's ask; its print is the card's solution figure.
_q8bi, _q8bii = P.items(k('8', 'b', 'i')), P.items(k('8', 'b', 'ii'))
assert [it.cell for it in _q8bi] == [None] and _q8bi[0].text == 'OH circled', _q8bi
assert [it.cell for it in _q8bii] == ['[8 + 2 + 2]'], _q8bii
C.add([k('8', 'b', 'i'), k('8', 'b', 'ii')], 'chem-2-2', 'ethanol-structure-and-solubility', [
    C.mark_ask(point('r-1', C.drawn_ask(k('8', 'b', 'i')), None,
                     'The scheme answers (i) with a drawing; its own print is shown with the '
                     'answer. It adds: [O–H bond not required]')),
    C.lifted('r-2', 'OH circled', None),
    C.lifted('r-3', _q8bii[0].text, None)],
    kind='orderedSplit', notation='[8 + 2 + 2]', total=12, cid='q8-b', figure=S + 'q8b-i',
    notes='The scheme prices these points together as [8 + 2 + 2] without saying which point '
          'earns which part, so no per-point value is shown.')
# X is given only in the reaction scheme, and the card's figure is the scheme's
# answer: the question picture is the paper's own print of the scheme and (b).
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q8b-print'
C.ordered([k('8', 'c', 'i'), k('8', 'c', 'ii'), k('8', 'c', 'iii')], None, None, cid='q8-c',
          figure=Q8)
C.ordered([k('8', 'd', 'i'), k('8', 'd', 'ii')], 'chem-4-2', 'addition-and-elimination-in-the-scheme',
          cid='q8-d-i', figure=Q8)

# ── Q9 Rate of reaction ──────────────────────────────────────────────────────
Q9 = 'chemistry-2023-ol-paper-p010-i0'
C.ordered([k('9', 'a')], None, None, figure=Q9)
# (b)(i) and (c): the only figure is the scheme's graph, held back until the reveal, while the
# lead-in points at "The apparatus shown below" and the graph is plotted from the table of masses.
# The paper's own print is the question: the lead-in, the balances and the table, then the part's
# own ask ((b)(i) alone; (c) with its three romans, (c)'s mark "(15)" left out).
C.fixed([k('9', 'b', 'i')], None, None, figure=S + 'q9b-i')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q9b-i-print'
C.fixed([k('9', 'b', 'ii')], None, None, figure=Q9)
C.ordered([k('9', 'c', 'i'), k('9', 'c', 'ii'), k('9', 'c', 'iii')], None, None, cid='q9-c',
          figure=S + 'q9b-i')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q9c-print'
C.ordered([k('9', 'd')], None, None, figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q10A = FIG + 'paper-p11-i0'
C.fixed([k('10', 'a', 'i')], 'chem-2-1', 'how-a-sodium-atom-becomes-an-ion', cid='q10-a-i-ii',
        figure=Q10A)
C.fixed([k('10', 'a', 'ii')], 'chem-2-1', 'how-a-chlorine-atom-becomes-an-ion', figure=Q10A)
C.fixed([k('10', 'a', 'iii')], 'chem-2-1', 'coordination-of-chloride-in-sodium-chloride',
        cid='q10-a-iii-iv', figure=Q10A)
C.fixed([k('10', 'a', 'iv')], 'chem-2-1', 'what-holds-the-ions-together-in-nacl', figure=Q10A)
C.menu([k('10', 'a', 'v')], None, None, figure=Q10A)
C.ordered([k('10', 'b')], 'chem-3-5', 'redox-of-magnesium-and-copper-sulfate', deep=True,
          cid='q10-b-i-ii')
# The letter's lead-in (the equation) and its first ask share one printed
# paragraph; the lead-in is the stem, the asks from "Define" the question.
_c = C.cards[-1]
_at = _c['questionText'].index('Define (i)')
_c['stem'], _c['questionText'] = _c['questionText'][:_at].strip(), _c['questionText'][_at:]
C.ordered([k('10', 'c', 'i')], None, None)
C.route([k('10', 'c', 'ii')], 'chem-1-4', 'atoms-in-moles-of-magnesium', cid='q10-c-ii-v')
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'moles-of-nitrogen-reacting-with-magnesium')
C.route([k('10', 'c', 'iv')], 'chem-1-4', 'volume-of-nitrogen-at-stp')
C.route([k('10', 'c', 'v')], 'chem-1-4', 'molar-mass-of-magnesium-nitride')
C.route([k('10', 'c', 'vi')], None, None)

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
Q11A = FIG + 'paper-q11a-table'
C.fixed([k('11', 'a', 'i')], 'chem-4-3', 'flocculation-in-water-treatment', cid='q11-a-i-ii',
        figure=Q11A)
C.fixed([k('11', 'a', 'ii')], 'chem-4-3', 'filtration-material-in-water-treatment', figure=Q11A)
C.fixed([k('11', 'a', 'iii')], 'chem-4-3', 'why-and-how-water-is-disinfected', cid='q11-a-iii-iv',
        figure=Q11A)
C.fixed([k('11', 'a', 'iv')], 'chem-4-3', 'why-water-is-fluoridated', figure=Q11A)
C.fixed([k('11', 'a', 'v')], 'chem-4-3', 'problem-of-unadjusted-acidic-water', cid='q11-a-v-vi',
        figure=Q11A)
C.fixed([k('11', 'a', 'vi')], 'chem-4-3', 'what-calcium-hydrogencarbonate-shows-about-water',
        figure=Q11A)
# Q11(b)(i): two terms, each answered under its own label; the second gives two
# pairs of points with "or" between them, priced (2 × 2). Below them the text
# layer reads the numerator of (ii)'s Kc, set in the 2023 equation font, as a
# third line ("[NH₃₃ ]22"); it is (ii)'s, carded there from the scheme's print.
# The Haber equation's subscripts sit on the line in the text layer ("N2 (g)").
Q11B = P.rearranged(C.context(k('11', 'b', 'i')), 'N2 (g) + 3H2 (g) ⇌ 2NH3 (g)',
                    'N₂ (g) + 3H₂ (g) ⇌ 2NH₃ (g)')
_q11b1 = P.items(k('11', 'b', 'i'))
assert [it.cell for it in _q11b1] == ['[3]', '[2 × 2]', None], _q11b1
C.add([k('11', 'b', 'i')], None, None, [
    C.lifted('r-1', _q11b1[0].text, 3),
    C.lifted('r-2', 'chemical equilibrium: forward and reverse reactions', 2,
             'The scheme prices this point and the next (2 × 2), one each, or instead the pair '
             '"concentrations of reactants and products // are constant".'),
    C.lifted('r-3', 'have equal rates', 2)], stem=Q11B)
C.drawn([k('11', 'b', 'ii')], None, None, S + 'q11b-ii', stem=Q11B)
C.fixed([k('11', 'b', 'iii')], None, None, stem=Q11B)
C.fixed([k('11', 'b', 'iv')], 'chem-3-3', 'why-the-haber-process-avoids-very-high-pressure',
        cid='q11-b-iv-v', stem=Q11B)
C.fixed([k('11', 'b', 'v')], 'chem-3-3', 'why-the-haber-process-runs-at-400-500-c', stem=Q11B)
C.ordered([k('11', 'c')], 'chem-4-1', 'fractional-distillation-of-crude-oil',
          figure=FIG + 'paper-p13-i0')
C.fixed([ka('11', 'd', 'i', 'A')], 'chem-4-3', 'a-use-of-oxygen', cid='q11-d-a-i-ii')
C.fixed([ka('11', 'd', 'ii', 'A')], 'chem-4-3', 'a-use-of-nitrogen-from-its-inertness')
C.fixed([ka('11', 'd', 'iii', 'A')], None, None)
C.fixed([ka('11', 'd', 'iv', 'A')], 'chem-4-3', 'abundance-of-nitrogen-in-air', cid='q11-d-a-iv-v')
C.fixed([ka('11', 'd', 'v', 'A')], 'chem-4-3', 'nitrogen-fixation')
C.fixed([ka('11', 'd', 'vi', 'A')], None, None)
C.menu([ka('11', 'd', 'i', 'B')], None, None)
C.fixed([ka('11', 'd', 'ii', 'B')], 'chem-3-5', 'corrosion-of-metals', cid='q11-d-b-ii-iii')
C.fixed([ka('11', 'd', 'iii', 'B')], 'chem-3-5', 'why-iron-corrodes-more-easily')
C.fixed([ka('11', 'd', 'iv', 'B')], None, None)
C.fixed([ka('11', 'd', 'v', 'B')], None, None)


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for key, (got, want) in sorted(C.letter_totals().items(),
                                   key=lambda kv: (int(kv[0][0]), kv[0][1])):
        out.append(f'Q{key[0]}({key[1]}) printed {want}, carded {got}')
    return '\n'.join(out)


if __name__ == '__main__':
    problems = make_audit(MAX_OPTIONS)(C.cards)
    for p in problems:
        print('AUDIT', p, file=sys.stderr)
    if '--review' in sys.argv:
        print(review())
    else:
        print(json.dumps(C.finish(), ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)
