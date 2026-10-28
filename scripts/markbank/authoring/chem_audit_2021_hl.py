#!/usr/bin/env python3
"""2021 Higher Level Chemistry, re-carded part by part from the paper and the labelled scheme.

    python3 scripts/markbank/authoring/chem_audit_2021_hl.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2021_hl.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2021 hl    # write them

Drafted by chem_draft.py and corrected card by card, the way
chem_audit_2022_hl.py re-cards 2022 HL: every question text, stem and lead-in
is the PAPER's print of its part and every marking point is the SCHEME's answer
closed by its own mark cell; a calculation is its first route's steps where the
text layer carries them cleanly, and the answer line with the scheme's print of
the working where it does not.

Pre-audit ids are kept (a card that joined parts priced by separate cells
keeps its id on its first part; later parts are new cards); WITHDRAWN lists the
pre-audit cards that duplicated another.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import routed  # noqa: E402
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, anyN, display, point  # noqa: E402

P = Printed(2021, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2021-HL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'
SPLIT = ('The scheme prices these points together as {} without saying which point earns which '
         'part, so no per-point value is shown.')


def k(*parts):
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


def menu_row(rid, it, claim, per, note=''):
    """An "[any N]" item as an anyN row, its options the scheme's own."""
    opts = [C.lifted('x', o, None)['verbatim'] for o in it.options()]
    asides = [a for a in it.asides if not a.lower().startswith('[any ')]
    return anyN(rid, opts[0], claim * per, claim, per, opts,
                ' '.join(x for x in [f'Any {claim} of these.', note,
                                     ('The scheme adds: ' + ' '.join(asides)) if asides else '']
                         if x))


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {
    'chem-2021-hl-q2-b-i': (
        'chem-2021-hl-q2-b-i-fig', 'Duplicated chem-2021-hl-q2-b-i-fig (both cited Q2(b)(i)).'),
    'chem-2021-hl-q2-d': (
        'chem-2021-hl-q2-d-fig', 'Duplicated chem-2021-hl-q2-d-fig (both cited Q2(d)).'),
    'chem-2021-hl-q2-e-fig': (
        'chem-2021-hl-q2-e', 'Duplicated chem-2021-hl-q2-e (both cited Q2(e)).'),
    'chem-2021-hl-q4-k': (
        'chem-2021-hl-q4-k-fig', 'Duplicated chem-2021-hl-q4-k-fig (both cited Q4(k)).'),
}

# ── Q1 Hypochlorite in bleach ────────────────────────────────────────────────
# Q1(a): one point (3), then any two of four (2 × 3).
_q1a = P.items(k('1', 'a'))
assert [it.cell for it in _q1a] == ['[3]', '[2 × 3]'], _q1a
C.add([k('1', 'a')], None, None, [
    C.lifted('r-1', _q1a[0].text, 3),
    menu_row('r-2', _q1a[1], 2, 3)], total=9, cid='q1-a')
C.fixed([k('1', 'b')], None, None)
C.fixed([k('1', 'c')], None, None)
C.fixed([k('1', 'd', 'i')], 'chem-4-1', 'starch-indicator-for-iodine-titration', cid='q1-d')
C.fixed([k('1', 'd', 'ii')], 'chem-4-1', 'end-point-colour-change-with-starch')
C.route([k('1', 'e', 'i')], 'chem-4-1', 'moles-of-thiosulfate-in-the-titre', cid='q1-e-i-ii',
        fixes={'21.4 × 0.09 = 0.001926 (1.926 × 10⁻³, 963/500000) moles sodium thiosulfate':
               '21.4 × 0.09 ÷ 1000 = 0.001926 (1.926 × 10⁻³, 963/500000) moles sodium thiosulfate'},
        row_notes={0: FRACTION.format('21.4 × 0.09', '1000')})
C.route([k('1', 'e', 'ii')], 'chem-4-1', 'moles-of-iodine-reduced', figure=S + 'q1e-ii')
C.route([k('1', 'e', 'iii')], 'chem-4-1', 'molarity-of-hypochlorite-in-the-bleach',
        cid='q1-e-iii-iv', figure=S + 'q1e-iii')
C.route([k('1', 'e', 'iv')], 'chem-4-1', 'hypochlorite-as-percent-w-v', figure=S + 'q1e-iv',
        fixes={'*[Multiply by 51.5 essential.] 39.6756 ÷ 10 = 3.9655 – 4 g ClO⁻ per 100 cm³ '
               'original bleach ⇒ 3.9655 – 4 % (w/v) ClO⁻ in original bleach':
               '39.6756 ÷ 10 = 3.9655 – 4 g ClO⁻ per 100 cm³ original bleach ⇒ 3.9655 – 4 % (w/v) '
               'ClO⁻ in original bleach'},
        row_notes={2: 'The scheme adds: *[Multiply by 51.5 essential.]'},
        notes='Under its second route the scheme adds: ' + ' '.join(P.items(k('1', 'e', 'iv'))[-1].asides))

# ── Q2 Making soap ───────────────────────────────────────────────────────────
Q2 = FIG + 'paper-p03-i1'
# The hydrolysis equation is drawn: its text layer reads "+ 3NaOH → ... + tri-ester
# soap co-product". The paper's print of it (Q2) is the figure of every Q2 card
# but (d), whose figure is the soap diagram and whose stem leaves the equation's
# sentence out.
_q2ctx = C.context(k('2', 'a', 'i'))
_Q2EQ = ' + 3NaOH → 3CH₃(CH₂)₁₀COONa + tri-ester soap co-product'
_Q2EQ_LEAD = ' The following is a balanced equation for the hydrolysis of a tri-ester molecule in coconut oil.'
assert _q2ctx.count(_Q2EQ_LEAD + _Q2EQ) == 1, _q2ctx
Q2S = _q2ctx.replace(_Q2EQ, '')
Q2DS = _q2ctx.replace(_Q2EQ_LEAD + _Q2EQ, '')
for r in ('i', 'ii'):
    C.fixed([k('2', 'a', r)], None, None, tail=True, stem=Q2S, figure=Q2)
# Q2(a)(iii): one point (3), the justification of the method suggested in (ii);
# the scheme sets one block per method, a blank line between them.
_q2a3 = P.items(k('2', 'a', 'iii'))
assert [it.cell for it in _q2a3] == ['[3]'] and len(_q2a3[0].points()) == 3, _q2a3
_q2a3_opts = [C.lifted('x', t, 3)['verbatim'] for t in _q2a3[0].points()]
C.add([k('2', 'a', 'iii')], None, None, [anyN(
    'r-1', _q2a3_opts[0], 3, 1, 3, _q2a3_opts,
    'One of these, the one for the method suggested in (ii). The scheme adds: '
    + ' '.join(_q2a3[0].asides))], total=3, stem=Q2S, figure=Q2)
C.fixed([k('2', 'a', 'iv')], None, None, tail=True, stem=Q2S, figure=Q2)
C.fixed([k('2', 'b', 'i')], None, None, cid='q2-b-i-fig', figure=Q2, stem=Q2S)
C.fixed([k('2', 'b', 'ii')], 'chem-u2', 'what-brine-is', cid='q2-b-ii-iii', stem=Q2S, figure=Q2)
C.fixed([k('2', 'b', 'iii')], 'chem-u2', 'function-of-brine-in-making-soap', stem=Q2S, figure=Q2)
C.fixed([k('2', 'c', 'i')], 'chem-u2', 'separating-the-soap', cid='q2-c', stem=Q2S, figure=Q2)
C.fixed([k('2', 'c', 'ii')], 'chem-u2', 'where-the-excess-sodium-hydroxide-is', stem=Q2S,
        figure=Q2)
C.fixed([k('2', 'd')], None, None, cid='q2-d-fig', figure=FIG + 'paper-p03-i0', stem=Q2DS)
C.route([k('2', 'e')], None, None, figure=Q2, stem=Q2S)

# ── Q3 Sodium sulfite and barium chloride ────────────────────────────────────
# Q3(a): five steps, tabulated for three methods; the rows are the steps, each
# with the methods' wordings separated by solidi.
_q3a_rows = [
    'clean a platinum (nichrome) wire* (rod, probe) in HCl (concentrated hydrochloric acid) / '
    'soak wood (splint, stick) overnight in water / use damp (wet) wood (splint, stick) / '
    'prepare a solution of the given salt',
    'dip wet rod in salt (sample) / dip** splint (stick) in salt (sample) / in water and ethanol '
    '(propanol)',
    'hold salt in or over hot (blue) part of Bunsen flame / spray salt solution onto (into) hot '
    '(blue) part of Bunsen flame',
    'yellow (amber, orange) colour is a positive result for sodium sulfite',
    'yellow-green colour is a positive result for barium chloride']
C.add([k('3', 'a')], None, None, [
    C.lifted(f'r-{i + 1}', t, 3, (
        'The scheme sets these five steps in a table for three methods, the methods\' wordings of '
        'each step separated here by solidi, and prices them (5 × 3); its own print is shown with '
        'the answer. It adds: *[Allow ‘metal inoculating loop’, or ‘metal spatula’ for ‘platinum '
        '(nichrome) wire’.] [Clear labelled diagram for some or all points acceptable.] '
        '[**Method 2: ‘Soak splint (stick) in salt solution’ merits (6).]') if i == 0 else '')
    for i, t in enumerate(_q3a_rows)], figure=S + 'q3a')
Q3B = FIG + 'paper-q3b-table'
C.fixed([k('3', 'b', 'i')], None, None, figure=Q3B)
C.fixed([k('3', 'b', 'ii')], None, None, figure=Q3B)
C.fixed([k('3', 'c', 'i')], 'chem-3-5', 'reducing-ability-of-magnesium-and-copper',
        cid='q3-c-i-ii')
C.fixed([k('3', 'c', 'ii')], 'chem-3-5', 'reducing-ability-of-zinc-and-copper')
C.fixed([k('3', 'c', 'iii')], None, None)
C.fixed([k('3', 'c', 'iv')], None, None)

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
# Q4(a): the paper sets the ion's mass and atomic numbers around its symbol.
C.fixed([k('4', 'a')], None, None, deep=True, notes=Q4_NOTE,
        qtext=P.rearranged(P.ask(k('4', 'a')), '32 S2– ion have? 16', '³²₁₆S²⁻ ion have?'))
C.fixed([k('4', 'b')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'c')], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'd')], None, None, cid='q4-d-fig', figure=FIG + 'paper-p05-i1', notes=Q4_NOTE)
for letter in ('e', 'f', 'g'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.answer_only([k('4', 'h')], None, None, S + 'q4h', notes=Q4_NOTE)
C.fixed([k('4', 'i')], None, None, notes=Q4_NOTE, tail=True)
C.fixed([k('4', 'j')], None, None, notes=Q4_NOTE)
Q4K = FIG + 'paper-p06-i0'
C.fixed([k('4', 'k', 'i')], 'chem-2-1', 'electrons-shared-between-carbons-in-cyclohexane',
        cid='q4-k-fig', figure=Q4K, notes=Q4_NOTE)
C.fixed([k('4', 'k', 'ii')], 'chem-2-1', 'electrons-shared-between-carbons-in-benzene', figure=Q4K,
        notes=Q4_NOTE)
# Q4(l)A: an advantage and a disadvantage, (2 × 3), one each; the reader joins
# the two blocks because the advantages' last row runs to the wrap margin.
_q4la = P.items(ka('4', 'l', None, 'A'))
assert [it.cell for it in _q4la] == ['[2 × 3]'], _q4la
_adv, _dis = _q4la[0].text.split(' disadvantage: ')
C.add([ka('4', 'l', None, 'A')], None, None, [
    C.lifted('r-1', _adv, 3, 'The scheme prices these points [2 × 3], one each.'),
    C.lifted('r-2', 'disadvantage: ' + _dis, 3)], cid='q4-l-a', notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'B')], None, None, cid='q4-l-b', notes=Q4_NOTE)

# ── Q5 Chlorine, argon and potassium ─────────────────────────────────────────
Q5 = FIG + 'paper-p07-i0'
C.ordered([k('5', 'a', 'i')], 'chem-1-3', 'how-mendeleev-arranged-the-elements', cid='q5-a',
          figure=Q5)
C.fixed([k('5', 'a', 'ii')], 'chem-1-3', 'why-mendeleev-did-not-predict-argon', figure=Q5)
C.fixed([k('5', 'a', 'iii')], 'chem-1-3', 'why-new-elements-will-be-super-heavy', figure=Q5)
C.fixed([k('5', 'b', 'i')], None, None, figure=Q5)
# (ii): two pairs of points with "or" between them, each pair (2 × 3).
_q5b2 = P.items(k('5', 'b', 'ii'))
assert [it.cell for it in _q5b2] == ['[2 × 3]', '[2 × 3]'], _q5b2
_p1 = _q5b2[0].points()
# Two pairs, the second after "or", each (2 × 3): each a route.
_p2 = _q5b2[1].points()
assert len(_p2) == 2, _p2
C.add([k('5', 'b', 'ii')], None, None, [
    routed(C.lifted('r-1', _p1[0], 3, 'The scheme prices this point and the next (2 × 3), one each, or instead the '
                    'last two rows. The examiner marks one pair or the other, not a mix.'), 'a'),
    routed(C.lifted('r-2', _p1[1], 3), 'a'),
    routed(C.lifted('r-3', _p2[0], 3, 'Or instead, this point and the next (2 × 3), one each.'), 'b'),
    routed(C.lifted('r-4', _p2[1], 3), 'b')], total=6, figure=Q5)
C.fixed([k('5', 'b', 'iii')], 'chem-1-3', 'covalent-radius-of-chlorine-from-bond-length',
        cid='q5-b-iii-v', figure=Q5)
C.fixed([k('5', 'b', 'iv')], 'chem-1-3', 'why-atomic-radius-falls-across-period-3', figure=Q5)
C.fixed([k('5', 'b', 'v')], 'chem-1-3', 'why-argon-has-no-covalent-radius', figure=Q5)
C.fixed([k('5', 'c', 'i')], None, None, figure=Q5)
C.fixed([k('5', 'c', 'ii')], None, None, figure=Q5)
C.fixed([k('5', 'c', 'iii')], 'chem-1-2', 'why-second-ionisation-energy-is-bigger',
        cid='q5-c-iii-iv', figure=Q5)
C.fixed([k('5', 'c', 'iv')], 'chem-1-2', 'big-second-ionisation-energy-of-potassium', figure=Q5,
        tail=True)

# ── Q6 Hydrogen, LPG and mercaptans ──────────────────────────────────────────
C.menu([k('6', 'a', 'i')], None, None)
C.menu([k('6', 'a', 'ii')], None, None)
C.fixed([k('6', 'b', 'i')], None, None)
# (ii): one point (3), then any two of three (2 × 3).
_q6b2 = P.items(k('6', 'b', 'ii'))
assert [it.cell for it in _q6b2] == ['[3]', '[2 × 3]'], _q6b2
C.add([k('6', 'b', 'ii')], None, None, [
    C.lifted('r-1', _q6b2[0].text, 3),
    menu_row('r-2', _q6b2[1], 2, 3)], total=9)
C.fixed([k('6', 'b', 'iii')], None, None)
C.fixed([k('6', 'c')], None, None)
C.answer_only([k('6', 'd')], None, None, S + 'q6d')

# ── Q7 Acids and bases ───────────────────────────────────────────────────────
# Q7(a)(i)-(ii): the paper sets both inside one sentence; the scheme prices
# each with a cell of its own.
Q7A = P.ask(k('7', 'a'))
C.fixed([k('7', 'a', 'i')], 'chem-3-4', 'arrhenius-definition-of-an-acid', cid='q7-a-i-ii',
        qtext=Q7A, stem='')
C.fixed([k('7', 'a', 'ii')], 'chem-3-4', 'bronsted-lowry-definition-of-an-acid', qtext=Q7A,
        stem='')
C.fixed([k('7', 'a', 'iii')], None, None, stem='')
C.fixed([k('7', 'a', 'iv')], None, None, stem='')
# (b): one answer (6), or two points (2 × 3).
_q7b = P.items(k('7', 'b'))
assert [it.cell for it in _q7b] == ['[6]', '[2 × 3]'], _q7b
# The point (6), or instead strong and weak acids defined (2 × 3): each a route.
_sw = [x.strip() for x in _q7b[1].text.split('//')]
assert len(_sw) == 2 and _sw[0].startswith('strong acid') and _sw[1].startswith('weak acid'), _sw
C.add([k('7', 'b')], None, None, [
    routed(C.lifted('r-1', _q7b[0].text, 6, 'Or instead the last two rows, (2 × 3), one each. The examiner marks one '
                    'or the other, not a mix.'), 'a'),
    routed(C.lifted('r-2', _sw[0], 3, 'Or instead, this point and the next (2 × 3), one each.'), 'b'),
    routed(C.lifted('r-3', _sw[1], 3, 'The scheme adds: [*Accept weak acid only partly dissociated.]'), 'b')],
    total=6)
# (c): the equation (3 + 3); below it the text layer reads (d)(i)'s answer,
# which is carded there.
_q7c = P.items(k('7', 'c'))
assert [it.cell for it in _q7c] == ['[3 + 3]', None], _q7c
C.fixed([k('7', 'c')], None, None, skip=(display(_q7c[1].text),))
C.add([k('7', 'd', 'i')], None, None, [
    C.lifted('r-1', _q7c[1].text, 6, 'The scheme gives (3) for the formulae and (3) for the '
                                     'balancing. It adds: [non equilibrium arrow '
                                     'unacceptable….(–1)]')])
C.route([k('7', 'd', 'ii')], 'chem-3-4', 'ion-concentrations-in-a-weak-acid', cid='q7-d-ii-iii')
C.route([k('7', 'd', 'iii')], 'chem-3-4', 'ph-of-a-weak-acid-solution')
C.answer_only([k('7', 'd', 'iv')], None, None, S + 'q7d-iv')

# ── Q8 Propan-2-ol ───────────────────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
C.ordered([k('8', 'a', 'i'), k('8', 'a', 'ii')], None, None, cid='q8-a', figure=Q8)
# (b)(i): the scheme's answer line ends in a solidus and draws propanone beside
# it, so its print is the answer's figure and the paper's print the question.
C.fixed([k('8', 'b', 'i')], None, None, figure=S + 'q8b-i',
        row_notes={0: 'The scheme also draws the structure of propanone beside this line; its own '
                      'print is shown with the answer.'})
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q8b-i-print'
C.drawn_with([k('8', 'b', 'ii')], 'chem-4-2', 'structure-of-propan-2-ol-and-bonds-formed',
             S + 'q8b-ii')
# Its figure is the scheme's drawing, so the paper's print of Q8's lead-in, the
# reaction scheme and (b)(ii) is its question.
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q8b-ii-print'
C.fixed([k('8', 'b', 'iii')], None, None, figure=Q8)
C.fixed([k('8', 'c', 'i')], 'chem-4-2', 'hydration-of-propene', cid='q8-c', figure=Q8)
C.fixed([k('8', 'c', 'ii')], 'chem-4-2', 'other-product-of-hydrating-propene', figure=Q8)
C.ordered([k('8', 'd', 'i')], 'chem-4-2', 'propan-2-ol-with-sodium', cid='q8-d', figure=Q8)
C.fixed([k('8', 'd', 'ii')], 'chem-4-2', 'what-the-sodium-reaction-shows-about-oh', figure=Q8)
C.route([k('8', 'e', 'i')], None, None,
        fixes={'560 60∗ = 9.333 moles per litre (mol l⁻¹, M)':
               '560 ÷ 60∗ = 9.333 moles per litre (mol l⁻¹, M)'},
        row_notes={2: FRACTION.format('560', '60∗')}, figure=Q8)
C.fixed([k('8', 'e', 'ii')], None, None, figure=Q8)

# ── Q9 The Haber process ─────────────────────────────────────────────────────
Q9 = FIG + 'paper-p10-i0'


def q9stem(key):
    """The Haber equation's subscripts sit on the line in the text layer."""
    return P.rearranged(C.context(key), 'N2 (g) + 3H2 (g) ⇌ 2NH3 (g)', 'N₂ (g) + 3H₂ (g) ⇌ 2NH₃ (g)')


C.fixed([k('9', 'a', 'i')], 'chem-3-3', 'conditions-for-good-yield-and-slow-rate', cid='q9-a-fig',
        figure=Q9, stem=q9stem(k('9', 'a', 'i')))
C.fixed([k('9', 'a', 'ii')], 'chem-3-3', 'conditions-for-high-yield-at-high-cost', figure=Q9,
        stem=q9stem(k('9', 'a', 'ii')))
# (b): the answer and its justification; below them the text layer reads the
# start of (c)(i)'s Kc expression, carded there from the scheme's print.
_q9b = P.items(k('9', 'b'))
C.fixed([k('9', 'b')], None, None, cid='q9-b-fig', figure=Q9, stem=q9stem(k('9', 'b')),
        skip=(display(_q9b[-1].text),))
C.drawn([k('9', 'c', 'i')], None, None, S + 'q9c-i', stem=q9stem(k('9', 'c', 'i')),
        notes='The scheme adds: [Square brackets ESSENTIAL.][Award marks for this expression '
              'given in part (ii).]')
C.add([k('9', 'c', 'ii')], None, None, [C.lifted(
    'r-1', '25 ÷ 243 / 0.103', 12,
    FRACTION.format('25', '243') + ' The scheme prices the answer (12) and sets out the working '
    'that earns it, (3) for each of four steps, in two routes; its own print is shown with the '
    'answer.')], figure=S + 'q9c-ii', stem=q9stem(k('9', 'c', 'ii')))
C.route([k('9', 'c', 'iii')], None, None, stem=q9stem(k('9', 'c', 'iii')), figure=Q9,
        fixes={'30× 100 = 20% 6 / 0.6 3× 100 = 20%': '6 ÷ 30 × 100 = 20% / 0.6 ÷ 3 × 100 = 20%'},
        row_notes={0: 'The scheme prints 6 over 30 and 0.6 over 3 as fractions; ÷ stands for '
                      'their bars.'})
C.fixed([k('9', 'd', 'i')], 'chem-3-3', 'effect-of-pressure-on-ammonia-yield', cid='q9-d',
        tail=True, stem=q9stem(k('9', 'd', 'i')), figure=Q9)
C.fixed([k('9', 'd', 'ii')], 'chem-3-3', 'effect-of-a-better-catalyst-on-yield', tail=True,
        stem=q9stem(k('9', 'd', 'ii')), figure=Q9)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q10A = FIG + 'paper-q10a-table'
C.ordered([k('10', 'a', 'i')], None, None, figure=S + 'q10a-i',
          notes='The scheme draws the dot and cross diagram two ways; its own print is shown with '
                'the answer.')
for r in ('ii', 'iii', 'iv', 'v'):
    C.fixed([k('10', 'a', r)], None, None, figure=Q10A)
_q10b1 = P.items(k('10', 'b', 'i'))
assert [it.cell for it in _q10b1] == ['[6]', None], _q10b1
C.add([k('10', 'b', 'i')], None, None, [C.lifted(
    'r-1', 'change in concentration per unit (over) time', 6,
    'The scheme also accepts the rate of change of concentration written as a fraction, change '
    'in concentration over time, of one reactant or product, or as d[reactant]/dt, '
    '−d[reactant]/dt or d[product]/dt; its own print is shown with the answer.')],
    figure=S + 'q10b-i')
C.fixed([k('10', 'b', 'ii')], None, None, figure=S + 'q10b-ii')
# (ii) and (iii) answer with the scheme's print, so the paper's print of (b)'s
# lead-in, its data table and the part is their question.
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q10b-ii-print'
_q10b3 = P.items(k('10', 'b', 'iii'))
assert [it.cell for it in _q10b3] == ['[4]', '[3]', '[3]'], _q10b3
C.add([k('10', 'b', 'iii')], None, None, [
    C.lifted('r-1', _q10b3[0].text, 4),
    C.lifted('r-2', 'slope = 0.0064 M s⁻¹ HCl [0.004 – 0.009] M s⁻¹ HCl', 3,
             'Above it the scheme sets "any two points from tangent read correctly, e.g. (0, 0.6) '
             'and (200, 1.78) / rise and run correctly read from tangent, e.g. 1.4 M, 240 s", and '
             'below it the working, 1.78 − 0.6 over 200 − 0 = 1.28 over 200 = 0.0064 M s⁻¹, '
             'priced (3); its own print is shown with the answer. It adds: ' +
             ' '.join(_q10b3[2].asides))], figure=S + 'q10b-iii')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q10b-iii-print'
_q10c1 = P.items(k('10', 'c', 'i'))
assert [it.cell for it in _q10c1] == ['[12]', '[3]', '[3]', '[3]', '[3]', '[3]', '[3]', None], \
    _q10c1
C.add([k('10', 'c', 'i')], None, None, [
    C.lifted('r-1', _q10c1[1].text, 3,
             'The scheme gives the mass of silver, 68.58 g Ag, priced (12), then these four steps.'),
    C.lifted('r-2', '22.50 ÷ 187.5 = 0.12 (3/25) moles copper(II) nitrate ⇒ 0.12 (3/25) moles Cu',
             3, FRACTION.format('22.50', '187.5')),
    C.lifted('r-3', _q10c1[3].text, 3),
    C.lifted('r-4', _q10c1[4].text, 3, 'The scheme adds: ' + ' '.join(_q10c1[4].asides)),
    C.lifted('r-5', '9 : 1 = Ag : Cu or 9/10 Ag or 1/10 Cu', 3,
             'The ratio, priced (3), from 68.58 over 7.62, or 7.62 over 76.20; the scheme adds: '
             '"1 : 9 = Cu : Ag …..acceptable 1 : 9 unlabelled or labelled incorrectly treat as '
             'mathematical slip (–1)".')], figure=S + 'q10c-i')
C.route([k('10', 'c', 'ii')], None, None, figure=S + 'q10c-ii',
        fixes={'68.58 ⇒ 108 = 0.635 moles silver 0.635 moles NO₂ from silver':
               '68.58 ÷ 108 = 0.635 moles silver ⇒ 0.635 moles NO₂ from silver'},
        row_notes={0: FRACTION.format('68.58', '108')})

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.fixed([k('11', 'a', 'i')], None, None)
C.menu([k('11', 'a', 'ii')], None, None, figure=S + 'q11a-ii')
C.add([k('11', 'a', 'iii')], None, None, [anyN(
    'r-1', 'CH₂BrCH₂Br / BrCH₂CH₂Br', 6, 1, 6,
    [C.lifted('x', o, None)['verbatim'] for o in ('CH₂BrCH₂Br / BrCH₂CH₂Br', 'CH₂BrCH₂OH')],
    'Any one, drawn: the scheme draws each as full and skeletal structures beside these '
    'formulae; its own print is shown with the answer. It adds: [1,1-dibromoethane '
    'unacceptable and 1-bromoethanol unacceptable.]')], total=6, figure=S + 'q11a-iii')
C.fixed([k('11', 'a', 'iv')], None, None, figure=FIG + 'paper-p12-i2')
# (b)(i) asks about the term the paper underlines, which no text layer carries: its question is the
# paper's own print of (b), the paragraph with its photograph beside it, then (i) ((ii), printed
# beside the photograph, whited out). The print holds the photograph, so it is the card's only figure.
C.fixed([k('11', 'b', 'i')], None, None)
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q11b-i-print'
for r in ('ii', 'iii', 'iv'):
    C.fixed([k('11', 'b', r)], None, None)
C.route([k('11', 'b', 'v')], None, None)
C.menu([k('11', 'c', 'i')], None, None, figure=FIG + 'paper-p13-i0')
C.fixed([k('11', 'c', 'ii')], None, None)
C.add([k('11', 'c', 'iii')], None, None, [
    C.lifted('r-1', 'neutron changes into a proton', 3,
             'The scheme prices this point and the next (2 × 3), one each, and writes each as a '
             'nuclear equation too; its own print is shown with the answer.'),
    C.lifted('r-2', 'and an electron which is emitted', 3,
             'The scheme adds: [Accept ‘proton changes into positron and neutron’ (6)]')],
    figure=S + 'q11c-iii')
C.fixed([k('11', 'c', 'iv')], None, None)
C.route([k('11', 'c', 'v')], None, None)
C.fixed([ka('11', 'd', 'i', 'A')], None, None)
C.menu([ka('11', 'd', 'ii', 'A')], None, None)
C.ordered([ka('11', 'd', 'iii', 'A')], None, None)
C.fixed([ka('11', 'd', 'iv', 'A')], None, None)
C.fixed([ka('11', 'd', 'v', 'A')], None, None)
# B's lead-in refers to its photograph. (i) asks about the term the paper underlines: its question is
# the paper's own print of B, its heading, lead-in and photograph, then (i).
C.fixed([ka('11', 'd', 'i', 'B')], None, None)
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q11d-b-i-print'
for r in ('ii', 'iii', 'iv', 'v', 'vi'):
    C.fixed([ka('11', 'd', r, 'B')], None, None, figure=FIG + 'paper-p14-i1')


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
