#!/usr/bin/env python3
"""2022 Higher Level Chemistry, re-carded part by part from the paper and the labelled scheme.

    python3 scripts/markbank/authoring/chem_audit_2022_hl.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2022_hl.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2022 hl    # write them

Drafted by chem_draft.py and corrected card by card, the way
chem_audit_2023_hl.py re-cards 2023 HL: the scheme is the labelled ("cue")
layout and does not reprint the question, so every question text, stem and
lead-in is the PAPER's print of its part and every marking point is the
SCHEME's answer closed by its own mark cell. A calculation is its first
route's steps (Cards.route) where the text layer carries them cleanly, and
the answer line with the scheme's print of the working (Cards.answer_only)
where it does not.

Pre-audit ids are kept (a card that joined parts priced by separate cells
keeps its id on its first part; later parts are new cards); WITHDRAWN lists the
pre-audit cards that duplicated another or held a piece of a task the scheme
prices as one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, anyN, point  # noqa: E402

P = Printed(2022, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2022-HL-'
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
    'chem-2022-hl-q2-b': (
        'chem-2022-hl-q2-b-fig', 'Duplicated chem-2022-hl-q2-b-fig (both cited Q2(b)).'),
    'chem-2022-hl-q5-c2': (
        'chem-2022-hl-q5-c1', 'Duplicated chem-2022-hl-q5-c1 (both cited parts of Q5(c)). '
        'Each part is now a card of its own; Q5(c)(i) is chem-2022-hl-q5-c1.'),
    'chem-2022-hl-q5-d': (
        'chem-2022-hl-q5-d-i', 'Duplicated chem-2022-hl-q5-d-i (both cited Q5(d)(i)).'),
    'chem-2022-hl-q10-b-shapes': (
        'chem-2022-hl-q10-b-def', 'Duplicated chem-2022-hl-q10-b-def (both cited Q10(b)). '
        'Each part is now a card of its own; the letter\'s own asks are chem-2022-hl-q10-b-def.'),
    'chem-2022-hl-q11-c-ii-iv-fig': (
        'chem-2022-hl-q11-c-ii', 'Held Q11(c)(ii)-(iv), which the scheme prices with a cell '
        'each; carded as their own cards, Q11(c)(ii) first.'),
    'chem-2022-hl-q8-b-iv': (
        'chem-2022-hl-q8-b-ii', 'The scheme prices Q8(b)(ii)-(vii) with one cell '
        '([(2 × 6) + (4 × 3) + 2]), so they are one task; carded once, as chem-2022-hl-q8-b-ii.'),
    'chem-2022-hl-q8-b-vi': (
        'chem-2022-hl-q8-b-ii', 'The scheme prices Q8(b)(ii)-(vii) with one cell '
        '([(2 × 6) + (4 × 3) + 2]); carded once, as chem-2022-hl-q8-b-ii.'),
}

# ── Q1 Total hardness by edta titration ──────────────────────────────────────
C.ordered([k('1', 'a', 'i')], 'chem-4-3', 'ions-that-cause-hardness', cid='q1-a')
C.fixed([k('1', 'a', 'ii')], 'chem-4-3', 'total-hardness')
C.fixed([k('1', 'b', 'i')], 'chem-4-1', 'indicator-for-edta-titration', cid='q1-b')
C.fixed([k('1', 'b', 'ii')], 'chem-4-1', 'end-point-colour-change-in-edta-titration')
C.fixed([k('1', 'c', 'i')], 'chem-4-1', 'ph-of-the-edta-buffer', cid='q1-c')
C.fixed([k('1', 'c', 'ii')], 'chem-4-1', 'why-the-ph-is-held-in-an-edta-titration')
C.menu([k('1', 'd')], None, None)
C.route([k('1', 'e', 'i')], 'chem-4-1', 'moles-of-edta-in-the-titre', cid='q1-e',
        fixes={'9.2 × 0.010 = 0.000092 (9.2 × 10⁻⁵, 23/250000) moles edta':
               '9.2 × 0.010 ÷ 1000 = 0.000092 (9.2 × 10⁻⁵, 23/250000) moles edta'},
        row_notes={0: FRACTION.format('9.2 × 0.010', '1000')})
C.route([k('1', 'e', 'ii')], 'chem-4-1', 'moles-of-hardness-ions-reacting-with-edta')
C.route([k('1', 'e', 'iii')], 'chem-4-1', 'moles-of-hardness-ions-removed-per-litre',
        figure=S + 'q1e-iii')
# Q1(e)(iv) asks for the hardness two ways, each priced as its answer (3) and
# one step (3): the rows are the two steps.
_q1e4 = P.items(k('1', 'e', 'iv'))
assert [it.cell for it in _q1e4] == ['[3]'] * 4, _q1e4
C.add([k('1', 'e', 'iv')], 'chem-4-1', 'hardness-removed-as-caco3', [
    C.lifted('r-1', _q1e4[1].text, 3, 'The scheme gives this answer, 0.368 – 0.37 g CaCO₃ per '
             'litre, priced (3), then this step, priced (3). It adds: [Multiply (iii) by 100* '
             'essential.] [*Addition must be shown for error to be treated as slip.]'),
    C.lifted('r-2', _q1e4[3].text, 3, 'The scheme gives this answer, 368 – 370 p.p.m. CaCO₃, '
             'priced (3), then this step, priced (3). It adds: [Multiply by 1000 essential.] [1 '
             'mark to be deducted for each mathematical slip, e.g. transposing numbers, addition '
             'error in *Mr where atomic masses shown but added incorrectly, etc.]')],
    figure=S + 'q1e-iv')

# ── Q2 Ethene ────────────────────────────────────────────────────────────────
# Q2(a): the drawing is the letter's own ask; "When carrying out this
# preparation, state one way of avoiding" leads (i) and (ii).
_q2a = P.ask(k('2', 'a'))
C.fixed([k('2', 'a')], 'chem-u2', 'apparatus-for-preparing-ethene', figure=S + 'q2a',
        cid='q2-a-draw', qtext=_q2a[:_q2a.index(' When carrying out')])
Q2A_LEAD = _q2a[_q2a.index('When carrying out'):]
Q2A_DRAW = _q2a[:_q2a.index(' When carrying out')]
C.fixed([k('2', 'a', 'i')], 'chem-u2', 'avoiding-suck-back-in-the-ethene-preparation', cid='q2-a',
        stem=Q2A_DRAW, qtext=Q2A_LEAD + ' ' + P.ask(k('2', 'a', 'i')))
C.fixed([k('2', 'a', 'ii')], 'chem-u2', 'avoiding-fire-in-the-ethene-preparation',
        stem=Q2A_DRAW, qtext=Q2A_LEAD + ' ' + P.ask(k('2', 'a', 'ii')))
Q2B = FIG + 'paper-p03-i0'
C.fixed([k('2', 'b', 'i')], 'chem-2-4', 'ethene-with-acidified-permanganate', cid='q2-b-fig',
        figure=Q2B)
C.fixed([k('2', 'b', 'ii')], 'chem-2-4', 'ethene-with-bromine-water', figure=Q2B)
C.fixed([k('2', 'b', 'iii')], 'chem-2-4', 'reaction-type-of-ethene-with-bromine', figure=Q2B)
C.fixed([k('2', 'b', 'iv')], 'chem-2-4', 'product-of-ethene-with-bromine', figure=Q2B)
Q2C = FIG + 'paper-p03-i2'
C.fixed([k('2', 'c', 'i')], None, None, cid='q2-c-i-fig', figure=Q2C)
C.fixed([k('2', 'c', 'ii')], 'chem-u2', 'between-the-two-filtrations', cid='q2-c', figure=Q2C)
C.fixed([k('2', 'c', 'iii')], 'chem-u2', 'after-the-second-filtration', figure=Q2C)
C.fixed([k('2', 'c', 'iv')], 'chem-u2', 'melting-point-of-recrystallised-benzoic-acid',
        figure=Q2C)

# ── Q3 Decomposition of hydrogen peroxide ────────────────────────────────────
C.ordered([k('3', 'a')], None, None)
C.fixed([k('3', 'b')], None, None)
_q3c = P.ask(k('3', 'c'))
C.fixed([k('3', 'c')], 'chem-3-2', 'plotting-volume-of-oxygen-against-time',
        figure=S + 'q3c', qtext=_q3c[:_q3c.index(' Use your graph to find')])
C.fixed([k('3', 'c', 'i')], None, None, figure=S + 'q3c')
C.route([k('3', 'c', 'ii')], None, None, figure=S + 'q3c',
        fixes={'total volume total time = 78 ÷ 4 = 19.5 cm³ O₂ per minute':
               'total volume ÷ total time = 78 ÷ 4 = 19.5 cm³ O₂ per minute'},
        row_notes={0: FRACTION.format('total volume', 'total time')})
# Q3(c)(iii): the tangent (3), then the slope (3), with the criterion for reading
# the tangent above it and the working in a box below.
_q3c3 = P.items(k('3', 'c', 'iii'))
assert [it.cell for it in _q3c3] == ['[3]', '[3]', '[3]'], _q3c3
C.add([k('3', 'c', 'iii')], None, None, [
    C.lifted('r-1', _q3c3[0].text, 3),
    C.lifted('r-2', 'slope = 9.8 cm³ O₂ per minute [8.8 – 12.2] cm³ O₂ per minute', 3,
             'Above it the scheme sets "any two points from tangent read correctly, e.g. (0, '
             '40) and (8.2, 120) / rise and run correctly read from tangent, e.g. 80 cm³, 8.2 '
             'minutes", and below it the working, 120 − 40 over 8.2 − 0 = 80 over 8.2 = 9.8, '
             'priced (3); its own print is shown with the answer. It adds: [Tangent must be drawn '
             'for work on instantaneous rate to be awarded full marks.] [Last 3 marks can be '
             'awarded for rate within stated range with no tangent drawn or consequentially for '
             'work done on a poor tangent or a tangent placed at an incorrect time.]')],
    figure=S + 'q3c-iii')
C.fixed([k('3', 'd', 'i')], 'chem-3-2', 'curve-for-half-the-concentration', cid='q3-d')
C.fixed([k('3', 'd', 'ii')], 'chem-3-2', 'curve-for-more-catalyst')

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'b')], None, None, figure=FIG + 'paper-q4-fig0', notes=Q4_NOTE)
C.fixed([k('4', 'c')], None, None, notes=Q4_NOTE, tail=True)
C.ordered([k('4', 'd', 'i'), k('4', 'd', 'ii')], None, None, cid='q4-d', notes=Q4_NOTE)
C.fixed([k('4', 'e')], None, None, notes=Q4_NOTE)
C.answer_only([k('4', 'f')], None, None, S + 'q4f', notes=Q4_NOTE)
# Q4(g): two pairs of reagents with "or" between them, priced [4 + 2].
_q4g = P.items(k('4', 'g'))
assert [it.cell for it in _q4g] == ['[4 + 2]'], _q4g
C.add([k('4', 'g')], None, None, [
    C.lifted('r-1', 'iron(II) sulfate (FeSO₄, ammonium iron(II) sulfate) / (C₆H₅)₂NH '
                    '(diphenylamine) and NH₄Cl (ammonium chloride) / copper (Cu)', None,
             'Or instead the pair "sodium hydroxide (NaOH) solution // aluminium (Al) / copper '
             '(Cu) / zinc (Zn)".'),
    C.lifted('r-2', 'concentrated sulfuric acid (H₂SO₄)', None)],
    kind='orderedSplit', notation='[4 + 2]', total=6,
    notes='The scheme prices these points together as [4 + 2] without saying which point earns '
          'which part, so no per-point value is shown. ' + Q4_NOTE)
C.ordered([k('4', 'h', 'i'), k('4', 'h', 'ii')], None, None, cid='q4-h', notes=Q4_NOTE)
C.ordered([k('4', 'i')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'j')], None, None, notes=Q4_NOTE)
C.answer_only([k('4', 'k')], None, None, S + 'q4k', cid='q4-k-fig', notes=Q4_NOTE)
# Q4(l)A: after "CO₂ + H₂O → H₂CO₃" the scheme gives the two equations (2 × 3), or
# the one equation for both steps (6).
_q4la = P.items(ka('4', 'l', None, 'A'))
assert [it.cell for it in _q4la][:2] == ['[2 × 3]', '[6]'], _q4la
C.add([ka('4', 'l', None, 'A')], None, None, [
    C.lifted('r-1', 'H₂CO₃ ⇌ (→) HCO₃⁻ + H⁺ / H₂CO₃ + H₂O ⇌ (→) HCO₃⁻ + H₃O⁺', 3,
             'The scheme sets "CO₂ + H₂O → H₂CO₃" above the two equations and prices them '
             '(2 × 3), one each.'),
    C.lifted('r-2', 'HCO₃⁻ ⇌ (→) CO₃²⁻ + H⁺ / HCO₃⁻ + H₂O ⇌ (→) CO₃²⁻ + H₃O⁺', 3,
             'Or instead the one equation "H₂CO₃ ⇌ (→) HCO₃⁻ + H⁺ ⇌ (→) CO₃²⁻ + 2H⁺", priced '
             '(6). The scheme adds: [Allow 2H₂CO₃ ⇌ (→) HCO₃⁻ + CO₃²⁻ + 3H⁺ or 2H₂CO₃ + 3H₂O ⇌ '
             '(→) HCO₃⁻ + CO₃²⁻ + 3H₃O⁺]')],
    cid='q4-l-a', notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'B')], None, None, cid='q4-l-b', notes=Q4_NOTE)

# ── Q5 Atomic structure ──────────────────────────────────────────────────────
C.ordered([k('5', 'a', 'i'), k('5', 'a', 'ii')], None, None, cid='q5-a')
C.fixed([k('5', 'b')], None, None, deep=True)
_q5c = P.ask(k('5', 'c'))
C.fixed([k('5', 'c')], 'chem-1-2', 'electron-configuration-of-calcium', cid='q5-c1',
        qtext=_q5c[:_q5c.index(' In an atom of calcium')])
C.fixed([k('5', 'c', 'i')], 'chem-1-2', 'main-energy-levels-occupied-in-calcium')
C.fixed([k('5', 'c', 'ii')], 'chem-1-2', 'orbitals-occupied-in-calcium-and-its-behaviour')
C.fixed([k('5', 'd', 'i')], None, None)
# Q5(d)(ii): the scheme answers with the completed equation, its mass and
# atomic numbers set around the symbols (and accepts them set the other way
# round); the text layer reads them on the line. The paper's equation likewise.
_q5d2 = P.rearranged(P.ask(k('5', 'd', 'ii')), '86 222Rn → + ₂ 4He', '²²²₈₆Rn → + ⁴₂He')
C.add([k('5', 'd', 'ii')], 'chem-1-2', 'alpha-decay-of-radon-222', qtext=_q5d2, rows=[C.ask_row(
    k('5', 'd', 'ii'), 3, 'The scheme answers with the completed nuclear equation, printed in a '
                          'form its text cannot carry; its own print is shown with the answer.')],
    figure=S + 'q5d-ii')
C.cards[-1]['rows'][0]['verbatim'] = _q5d2      # the ask row is the ask as set
C.fixed([k('5', 'd', 'iii')], None, None)

# ── Q6 Fuels ─────────────────────────────────────────────────────────────────
C.ordered([k('6', 'a', 'i'), k('6', 'a', 'ii')], None, None, cid='q6-a')
C.fixed([k('6', 'b', 'i')], None, None)
# Q6(b)(ii)-(iii): the name, then the condensed formula with the skeletal and
# full structures the scheme draws beside it, separated by solidi.
DRAWN_TOO = ('The scheme also accepts the structures it draws beside the formula, separated by '
             'solidi; its own print is shown with the answer.')
C.fixed([k('6', 'b', 'ii')], 'chem-2-4', 'alkane-of-octane-number-zero', figure=S + 'q6b-ii',
        tail=True, row_notes={1: DRAWN_TOO})
C.fixed([k('6', 'b', 'iii')], 'chem-2-4', 'alkane-of-octane-number-100', figure=S + 'q6b-iii',
        tail=True, row_notes={1: DRAWN_TOO})
C.fixed([k('6', 'b', 'iv')], None, None)
# The fuel-cell equation's subscripts sit on the line in the text layer.
Q6C = P.rearranged(C.context(k('6', 'c', 'i')), 'H2 (g) + ½O2 (g) → H2O (l)',
                   'H₂ (g) + ½O₂ (g) → H₂O (l)')
C.fixed([k('6', 'c', 'i')], 'chem-u3', 'why-hydrogen-is-not-found-free-on-earth', cid='q6-c-i-ii',
        stem=Q6C)
C.fixed([k('6', 'c', 'ii')], 'chem-u3', 'a-source-of-hydrogen-other-than-steam-reforming',
        stem=Q6C)
C.fixed([k('6', 'c', 'iii')], None, None, stem=Q6C)
C.fixed([k('6', 'c', 'iv')], None, None, stem=Q6C)
C.answer_only([k('6', 'c', 'v')], None, None, S + 'q6c-v', stem=Q6C)

# ── Q7 Methanol equilibrium ──────────────────────────────────────────────────
# Q7(a): one point for each ask, priced together [6 + 2]. Under (ii) the scheme
# also accepts the equilibrium-constant expression set equal to a constant, in
# fractions the text layer cannot carry, and below them sets (b)(i)'s answer.
_q7ai, _q7aii = P.items(k('7', 'a', 'i')), P.items(k('7', 'a', 'ii'))
assert [it.cell for it in _q7ai] == [None] and [it.cell for it in _q7aii] == ['[6 + 2]', None]
C.add([k('7', 'a', 'i'), k('7', 'a', 'ii')], None, None, [
    C.lifted('r-1', _q7ai[0].text, None),
    C.lifted('r-2', 'state reached at which these concentrations (they) are constant', None,
             'The scheme also accepts the equilibrium constant expression set equal to a '
             'constant, in general form or for this reaction; its own print is shown with the '
             'answer. The scheme adds: [Square brackets essential.]')],
    kind='orderedSplit', notation='[6 + 2]', total=8, cid='q7-a', figure=S + 'q7a',
    notes='The scheme prices these points together as [6 + 2] without saying which point '
          'earns which part, so no per-point value is shown.')
C.drawn([k('7', 'b', 'i')], None, None, S + 'q7b-i')
C.answer_only([k('7', 'b', 'ii')], None, None, S + 'q7b-ii')
C.fixed([k('7', 'c')], None, None)
C.fixed([k('7', 'd', 'i')], None, None)
C.fixed([k('7', 'd', 'ii')], None, None)
C.fixed([k('7', 'd', 'iii')], None, None)

# ── Q8 Carboxylic acids and esters ───────────────────────────────────────────
# Q8(a)(i): the scheme draws the delocalised carboxylate and the inductive effect
# between the wordings of the second point.
C.fixed([k('8', 'a', 'i')], None, None, figure=S + 'q8a-i',
        fixes={'(–COO⁻) stable (exists as resonance hybrid) / delocalised charge on –COO⁻ (RCOO⁻) / '
               '/ inductive effect draws electrons away from H of OH bond / / δ⁺ carbonyl carbon '
               'draws electrons away from H of OH bond':
               '(–COO⁻) stable (exists as resonance hybrid) / delocalised charge on –COO⁻ (RCOO⁻) / '
               'inductive effect draws electrons away from H of OH bond / δ⁺ carbonyl carbon draws '
               'electrons away from H of OH bond'},
        row_notes={1: 'The scheme draws the carboxylate ion and the inductive effect beside these; '
                      'its own print is shown with the answer.'})
C.fixed([k('8', 'a', 'ii')], None, None)
C.fixed([k('8', 'a', 'iii')], None, None)
C.ordered([k('8', 'b', 'i')], None, None)
C.ordered([k('8', 'b', r) for r in ('ii', 'iii', 'iv', 'v', 'vi', 'vii')], 'chem-4-2',
          'the-ester-ethyl-methanoate', cid='q8-b-ii', drop=('to (vii) has SEVEN POINTS:',),
          notes='The scheme heads the cell "(ii) to (vii) has SEVEN POINTS".')

# ── Q9 Acids, bases and pH ───────────────────────────────────────────────────
C.ordered([k('9', 'a')], None, None)
C.fixed([k('9', 'b')], None, None)
C.route([k('9', 'c', 'i')], 'chem-3-4', 'concentration-of-a-strong-acid-from-ph', cid='q9-c')
C.route([k('9', 'c', 'ii')], 'chem-3-4', 'hydroxide-concentration-from-ph')
Q9D = FIG + 'paper-q9d'
C.fixed([k('9', 'd', 'i')], None, None, figure=Q9D)
C.fixed([k('9', 'd', 'ii')], None, None, figure=Q9D)
C.fixed([k('9', 'd', 'iii')], 'chem-3-4', 'which-weak-acid-has-the-larger-ka', figure=Q9D)
C.fixed([k('9', 'd', 'iv')], None, None, figure=Q9D)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# Q10(a)(i): two definitions with "or" between them, each priced (4): either.
_q10a1 = P.items(k('10', 'a', 'i'))
assert [it.cell for it in _q10a1] == ['[4]', '[4]'], _q10a1
_opts = [C.lifted('x', it.text, 4)['verbatim'] for it in _q10a1]
C.add([k('10', 'a', 'i')], 'chem-2-3', 'what-an-ideal-gas-is',
      [anyN('r-1', _opts[0], 4, 1, 4, _opts, 'The scheme gives these two definitions with "or" '
            'between them, (4) for either. It adds: [Allow molecules instead of particles '
            'above.]')], total=4, cid='q10-a-i-ii')
C.fixed([k('10', 'a', 'ii')], 'chem-2-3', 'conditions-for-real-gases-to-be-nearly-ideal')
C.fixed([k('10', 'a', 'iii')], None, None)
C.answer_only([k('10', 'a', 'iv')], None, None, S + 'q10a-iv')
_q10b = P.ask(k('10', 'b'))
C.fixed([k('10', 'b')], 'chem-1-3', 'electronegativity-and-its-trend-down-group-17',
        cid='q10-b-def', qtext=_q10b[:_q10b.index(' Predict the shape')])
# (i)-(iii) are led by "Predict the shape of a molecule of"; (iv)-(v) by "Which one
# of these three compounds", whose three are (i)-(iii)'s.
Q10B = _q10b[_q10b.index('Predict the shape'):]
Q10B3 = ' '.join([Q10B] + [f'({r}) ' + P.ask(k('10', 'b', r)) for r in ('i', 'ii', 'iii')] +
                 ['Which one of these three compounds'])
C.fixed([k('10', 'b', 'i')], 'chem-2-2', 'shape-of-silicon-tetrachloride', stem=Q10B)
C.fixed([k('10', 'b', 'ii')], 'chem-2-2', 'shape-of-sulfur-dichloride', stem=Q10B)
C.fixed([k('10', 'b', 'iii')], 'chem-2-2', 'shape-of-phosphorus-trichloride', stem=Q10B)
C.fixed([k('10', 'b', 'iv')], 'chem-2-2', 'which-of-the-three-is-non-polar', stem=Q10B3)
C.fixed([k('10', 'b', 'v')], 'chem-2-2', 'which-has-the-least-polar-bonds', stem=Q10B3)
C.route([k('10', 'c', 'i')], 'chem-1-4', 'moles-of-hydrogen-from-water', cid='q10-c')
C.route([k('10', 'c', 'ii')], 'chem-1-4', 'moles-of-carbon-from-koh',
        fixes={'3.584 56∗= 0.064 moles KOH': '3.584 ÷ 56∗ = 0.064 moles KOH'},
        row_notes={0: FRACTION.format('3.584', '56∗')})
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'moles-of-sulfur-from-so2',
        fixes={'22400= 0.002 / 2 × 10⁻³ / 1/500 moles SO₂ 44.8 ⇒ 0.002 / 2 × 10⁻³ / 1/500 moles S':
               '44.8 ÷ 22400 = 0.002 / 2 × 10⁻³ / 1/500 moles SO₂ ⇒ 0.002 / 2 × 10⁻³ / 1/500 '
               'moles S'},
        row_notes={0: FRACTION.format('44.8', '22400')})
# Q10(c)(iv) asks two things under one roman: the moles of nitrogen, priced as
# its answer (4) and one step (4), and the empirical formula, priced as its
# answer (6) and three steps (2, 3, 1). The rows are each's working.
_q10c4 = P.items(k('10', 'c', 'iv'))
assert [it.cell for it in _q10c4] == ['[4]', '[4]', '[6]', '[2]', '[3]', '[1]'], _q10c4
C.add([k('10', 'c', 'iv')], 'chem-1-4', 'moles-of-nitrogen-and-the-empirical-formula', [
    C.lifted('r-1', '2.4 × 10²¹ ÷ 6 × 10²³ = 0.004 / 4 × 10⁻³ / 1/250 moles NO₂ ⇒ 0.004 / 4 × '
                    '10⁻³ / 1/250 moles N or 0.002 / 2 × 10⁻³ / 1/500 moles N₂', 4,
             FRACTION.format('2.4 × 10²¹', '6 × 10²³') + ' The scheme gives the answer, 0.004 '
             'moles N or 0.002 moles N₂, priced (4), then this step, priced (4).'),
    C.lifted('r-2', 'C : H : N : O : S = 0.032 : 0.036 : 0.004 : 0.008 : 0.002', 2,
             'The scheme gives the empirical formula, C₁₆H₁₈N₂O₄S, priced (6), then these three '
             'steps. It adds: [Number of moles H atoms and number of moles of N atoms '
             'essential.]'),
    C.lifted('r-3', 'Divide C : H : N : O : S ratio by smallest number of moles', 3),
    C.lifted('r-4', '⇒ C₁₆H₁₈N₂O₄S', 1, 'The scheme adds: [Last mark available ONLY for '
             'C₁₆H₁₈N₂O₄S] [Full marks available where elements are not in alphabetical order.]')],
    figure=S + 'q10c-iv')

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.ordered([k('11', 'a', 'i'), k('11', 'a', 'ii')], None, None, cid='q11-a-i-ii')
C.fixed([k('11', 'a', 'iii')], 'chem-3-5', 'oxidation-number-of-hydrogen-in-metal-hydrides',
        cid='q11-a-iii-iv')
C.fixed([k('11', 'a', 'iv')], 'chem-3-5', 'oxidation-number-of-oxygen-in-of2')
# Q11(a)(v): the answer is the balanced equation with the oxidation numbers set
# beneath its manganese and bismuth species (9); the scheme then prices the
# manganese numbers, the bismuth numbers and the balancing, (3) each.
_q11a5 = P.items(k('11', 'a', 'v'))
assert [it.cell for it in _q11a5] == ['[9]', '[3]', '[3]', '[3]'], _q11a5
C.add([k('11', 'a', 'v')], 'chem-3-5', 'balancing-a-redox-equation-by-oxidation-numbers', [
    C.lifted('r-1', _q11a5[0].text, 9,
             'The scheme sets the oxidation numbers +2, +5, +7 and +3 beneath Mn²⁺, BiO₃⁻, MnO₄⁻ '
             'and Bi³⁺, then prices the manganese numbers, the bismuth numbers and the balanced '
             'equation (3) each; its own print is shown with the answer. It adds: "Award marks '
             'for correct oxidation numbers of manganese and bismuth only." [Allow Roman '
             'numerals for oxidation states.] [Plus signs need not be given for the positive '
             'oxidation numbers, i.e. +2 and 2 equally acceptable]')],
    cid='q11-a-v-vi', figure=S + 'q11a-v')
C.fixed([k('11', 'a', 'vi')], None, None)
C.fixed([k('11', 'b', 'i')], 'chem-4-2', 'ethanal-with-acidified-permanganate',
        cid='q11-b-i-iii')
C.fixed([k('11', 'b', 'ii')], 'chem-4-2', 'ethanal-with-fehlings-reagent')
C.fixed([k('11', 'b', 'iii')], 'chem-4-2', 'product-of-oxidising-ethanal')
C.fixed([k('11', 'b', 'iv')], 'chem-4-2', 'ease-of-oxidising-ethanal', cid='q11-b-iv-v')
C.fixed([k('11', 'b', 'v')], 'chem-4-2', 'half-equation-for-reducing-copper-ii')
# Q11(b)(vi): two points (2 × 2), or instead the scheme's drawing of the carbonyl
# group with its partial charges, priced (4).
_q11b6 = P.items(k('11', 'b', 'vi'))
assert [it.cell for it in _q11b6] == ['[2 × 2]', '[4]'] and not _q11b6[1].text, _q11b6
_p1, _p2 = _q11b6[0].points()
C.add([k('11', 'b', 'vi')], 'chem-2-2', 'polarity-of-the-carbonyl-group', [
    C.lifted('r-1', _p1, 2, 'The scheme prices these points (2 × 2), one each.'),
    C.lifted('r-2', _p2, 2, 'Or instead the scheme\'s drawing of the carbonyl group with δ⁻ on '
                            'the oxygen and δ⁺ on the carbon, priced (4); its own print is shown '
                            'with the answer.')],
    cid='q11-b-vi-vii', figure=S + 'q11b-vi')
C.fixed([k('11', 'b', 'vii')], 'chem-2-2', 'why-ethanal-dissolves-in-water')
Q11C = FIG + 'paper-p13-i0'
# Q11(c)(i): two pairs of points with "or" between them, priced (2 × 2).
_q11c1 = P.items(k('11', 'c', 'i'))
assert [it.cell for it in _q11c1] == ['[2 × 2]'], _q11c1
C.add([k('11', 'c', 'i')], None, None, [
    C.lifted('r-1', 'minimum combined energy of colliding particles (molecules)', 2,
             'The scheme prices this point and the next (2 × 2), one each, or instead the pair '
             '"minimum combined energy of particles (molecules) // for (of) effective '
             'collisions".'),
    C.lifted('r-2', 'for reaction to take place between them', 2,
             'The scheme adds: [At least one mention of collisions or colliding is essential for '
             'full marks.]')],
    figure=Q11C)
C.fixed([k('11', 'c', 'ii')], 'chem-3-2', 'activation-energy-from-a-reaction-profile', figure=Q11C)
C.fixed([k('11', 'c', 'iii')], 'chem-3-2', 'how-much-the-catalyst-lowers-ea', figure=Q11C)
C.fixed([k('11', 'c', 'iv')], 'chem-3-2', 'heat-of-the-reverse-reaction', figure=Q11C)
# (v) and (vi) are led by the paragraph on platinum catalysis alone; the profile
# diagram above it belongs to (i)-(iv).
Q11CV = C.context(k('11', 'c', 'v'))
Q11CV = Q11CV[Q11CV.index('The reaction between pure hydrogen'):]
C.fixed([k('11', 'c', 'v')], None, None, stem=Q11CV)
C.menu([k('11', 'c', 'vi')], None, None, stem=Q11CV)
C.fixed([ka('11', 'd', 'i', 'A')], 'chem-4-3', 'photodissociation', cid='q11-d-a-i-iii')
C.fixed([ka('11', 'd', 'ii', 'A')], 'chem-4-3', 'photodissociation-of-ozone')
C.fixed([ka('11', 'd', 'iii', 'A')], 'chem-4-3', 'a-use-of-cfcs')
C.fixed([ka('11', 'd', 'iv', 'A')], 'chem-4-3', 'chlorine-radicals-and-ozone', cid='q11-d-a-iv-v')
C.fixed([ka('11', 'd', 'v', 'A')], 'chem-4-3', 'methane-and-chlorine-radicals')
C.fixed([ka('11', 'd', 'i', 'B')], 'chem-3-5', 'how-galvanising-protects-iron', cid='q11-d-b-i-iv')
C.fixed([ka('11', 'd', 'ii', 'B')], 'chem-3-5', 'metal-for-sacrificial-anodes')
C.fixed([ka('11', 'd', 'iii', 'B')], 'chem-3-5', 'how-a-sacrificial-anode-protects-steel')
C.fixed([ka('11', 'd', 'iv', 'B')], 'chem-3-5', 'anodised-aluminium')
Q11DB = FIG + 'paper-q11db'
C.fixed([ka('11', 'd', 'v', 'B')], 'chem-3-5', 'electrode-half-equations-for-molten-lead-bromide',
        cid='q11-d-b-v-vi', figure=Q11DB)
C.fixed([ka('11', 'd', 'vi', 'B')], 'chem-3-5', 'how-charge-moves-through-molten-lead-bromide',
        figure=Q11DB)


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
