#!/usr/bin/env python3
"""2025 Ordinary Level Chemistry, re-carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_audit_2025_ol.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2025_ol.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2025 ol    # write them

The sitting was carded before the audit (chem_2025_ol.py and its siblings).
This file replaces those cards' text with the paper's and the scheme's own,
the way chem_audit_2025_hl.py does for the Higher paper, and keeps every card
id a student may have progress on:

  * a pre-audit card whose parts are still one card keeps its id;
  * a pre-audit card that joined parts the scheme prices with cells of their
    own keeps its id on its FIRST part, and each later part is a new card;
    where the old concept slug named the joined parts, the first part gets
    its own;
  * a pre-audit card that duplicated another, or held a piece of a task the
    scheme prices with ONE cell (Q7(c), Q10(b), Q10(c), Q11(a)), is withdrawn
    (WITHDRAWN below): chem_apply_print.py drops it at build time with a
    card-corrections.json record naming the card that now holds its parts,
    and aliases its id there so its review history carries over.

The Ordinary scheme prices many letters with ONE cell for all their parts
("[9 + 6 + 2 + 2 + 2]" closes Q6(b)(i)-(iv)): those letters are one
orderedSplit card each, with no per-point value. Where such a cell spans a
part answered by a drawing (Q6(b)(iii), Q11(b)(vi)), that part's row is its
own ask and the scheme's drawing is the card's solution figure.

Every question text, stem and lead-in is the PAPER's print of its part; every
marking point is the SCHEME's answer closed by its own mark cell. The paper's
figures (chem_print_figures.py CROPS) are read as pictures: their labels stay
out of the text (Printed(..., figures=True)).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS  # noqa: E402

P = Printed(2025, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2025-OL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'


def k(*parts):
    """A part key: k('1', 'a', 'i') -> ('1', 'a', 'i', None)."""
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


# The scheme's note on Q4, lifted from its print.
_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

# Pre-audit cards withdrawn, each with the card that now holds its parts.
JOINED = ('The scheme prices {parts} with one cell ({cell}), so they are one task; carded '
          'once, as {new}.')
WITHDRAWN = {
    'chem-2025-ol-q1-b-fig': (
        'chem-2025-ol-q1-b',
        'Duplicated chem-2025-ol-q1-b (the same Q1(b) parts, never built: the build keeps one '
        'card per citation). Q1(b)(i) is carded as chem-2025-ol-q1-b, (ii) as -q1-b-ii.'),
    'chem-2025-ol-q2-b-fig': (
        'chem-2025-ol-q2-b',
        'Duplicated chem-2025-ol-q2-b (the same Q2(b) parts, never built). Q2(b)(i)-(iv) is '
        'one task, carded as chem-2025-ol-q2-b.'),
    'chem-2025-ol-q6-c': (
        'chem-2025-ol-q6-c-fig',
        'Duplicated chem-2025-ol-q6-c-fig (the same Q6(c) parts, never built). Q6(c)(i)-(ii) '
        'is carded as chem-2025-ol-q6-c-fig.'),
    'chem-2025-ol-q7-c-iii': (
        'chem-2025-ol-q7-c-i-ii',
        JOINED.format(parts='Q7(c)(i)-(iv)', cell='[8 + 6 + 2 + 2 + 2 + 2 + 2]',
                      new='chem-2025-ol-q7-c-i-ii')),
    'chem-2025-ol-q7-c-iv': (
        'chem-2025-ol-q7-c-i-ii',
        JOINED.format(parts='Q7(c)(i)-(iv)', cell='[8 + 6 + 2 + 2 + 2 + 2 + 2]',
                      new='chem-2025-ol-q7-c-i-ii')),
    'chem-2025-ol-q10-b-iv-v': (
        'chem-2025-ol-q10-b-i-iii',
        JOINED.format(parts='Q10(b)(i)-(v)', cell='[9 + 3 + 3 + 2 + 2 + 2 + 2 + 2]',
                      new='chem-2025-ol-q10-b-i-iii')),
    'chem-2025-ol-q10-c-iv-v': (
        'chem-2025-ol-q10-c-i-iii',
        JOINED.format(parts='Q10(c)(i)-(v)', cell='[9 + 8 + 2 + 2 + 2 + 2]',
                      new='chem-2025-ol-q10-c-i-iii')),
    'chem-2025-ol-q11-a-2': (
        'chem-2025-ol-q11-a-1',
        JOINED.format(parts='all seven numbers of Q11(a)', cell='[9 + 6 + 2 + 2 + 2 + 2 + 2]',
                      new='chem-2025-ol-q11-a-1')),
    'chem-2025-ol-q11-a-3': (
        'chem-2025-ol-q11-a-1',
        JOINED.format(parts='all seven numbers of Q11(a)', cell='[9 + 6 + 2 + 2 + 2 + 2 + 2]',
                      new='chem-2025-ol-q11-a-1')),
}

# ── Q1 Making soap ───────────────────────────────────────────────────────────
Q1 = FIG + 'paper-q1'
C.fixed([k('1', 'a')], None, None, figure=Q1)       # the stem points at Diagrams 1 and 2
C.fixed([k('1', 'b', 'i')], 'chem-u2', 'reflux-to-heat-without-losing-solvent', figure=Q1,
        cid='q1-b')
C.fixed([k('1', 'b', 'ii')], 'chem-u2', 'distillation-to-remove-ethanol', figure=Q1)
C.fixed([k('1', 'c', 'i')], 'chem-u2', 'liebig-condenser', figure=Q1, cid='q1-c-fig',
        label_key=[{'letter': 'C', 'meaning': '(liebig) condenser', 'askedInThisQuestion': True}])
C.fixed([k('1', 'c', 'ii')], 'chem-1-1', 'change-of-state-in-a-condenser', figure=Q1)
C.fixed([k('1', 'd', 'i')], 'chem-u2', 'what-brine-is', cid='q1-d', figure=Q1)
C.fixed([k('1', 'd', 'ii')], 'chem-u2', 'separating-the-soap-precipitate', figure=Q1)
# Q1(e): the pictograms are introduced by the line the paper prints after
# (d)(ii); it is the question's lead-in to (e).
C.fixed([k('1', 'e')], None, None, cid='q1-e-fig', figure=FIG + 'paper-q1e',
        stem=P.ask(k('1')) + ' ' + P.lead(k('1', 'd', 'ii')))

# ── Q2 Titration of hydrochloric acid against sodium carbonate ───────────────
Q2 = FIG + 'paper-q2'
C.fixed([k('2', 'a')], None, None)
C.ordered([k('2', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], None, None, cid='q2-b',
          figure=Q2, label_key=[{'letter': 'P', 'meaning': 'volumetric flask',
                                 'askedInThisQuestion': True}])
C.fixed([k('2', 'c', 'i')], 'chem-4-1', 'indicator-for-a-sodium-carbonate-titration', cid='q2-c')
C.fixed([k('2', 'c', 'ii')], 'chem-4-1', 'end-point-colour-change-of-methyl-orange')
C.fixed([k('2', 'c', 'iii')], 'chem-4-1', 'why-a-white-tile-is-used')
# Q2(d): one cell, [5 + 2 + 2], over two routes the scheme prints side by
# side. The route by moles is carded line by line, each line given in the one
# form the provenance gate finds; the route by the titration formula is set
# wholly as fractions the text layer cannot order, so the scheme's own print
# of both routes is the card's answer picture.
_q2d = P.items(k('2', 'd'))
# (d) prints its setting, then the equation and the ask after it.
_Q2D_LEAD = P.lead(k('2', 'd'))
assert [it.cell for it in _q2d] == ['[5 + 2 + 2]', None], _q2d
C.add([k('2', 'd')], 'chem-4-1', 'concentration-of-hydrochloric-acid-from-a-titration', [
    C.lifted('r-1', '(0.05)(25) ÷ 1000 = 0.00125 (moles per 25 cm³)', None,
             FRACTION.format('(0.05)(25)', '1000')),
    C.lifted('r-2', '0.00125 × 2 = 0.0025', None),
    C.lifted('r-3', '(0.0025)(1000) ÷ 18 = 0.13 - 0.14 M', None,
             FRACTION.format('(0.0025)(1000)', '18'))],
      kind='orderedSplit', notation='[5 + 2 + 2]', total=9, figure=S + 'q2d',
      stem=P.ask(k('2')) + ' ' + P.ask(k('2', 'd')) + ' ' + _Q2D_LEAD[:_Q2D_LEAD.index('Calculate')],
      qtext=_Q2D_LEAD[_Q2D_LEAD.index('Calculate'):],
      notes='The scheme prices the calculation [5 + 2 + 2] and prints two routes side by side: '
            'the one carded here, by moles, and one by the titration formula; its own print of '
            'both is shown with the answer. The scheme adds: ' + ' '.join(_q2d[1].asides or
                                                                          [_q2d[1].text]))

# ── Q3 Rate of the thiosulfate-acid reaction ─────────────────────────────────
Q3 = FIG + 'paper-q3'
C.fixed([k('3', 'a', 'i')], 'chem-3-2', 'product-that-obscures-the-cross', cid='q3-a', figure=Q3)
C.fixed([k('3', 'a', 'ii')], 'chem-u2', 'measuring-out-ten-cubic-centimetres-of-acid',
        figure=Q3)
C.fixed([k('3', 'a', 'iii')], 'chem-3-2', 'a-condition-kept-constant', figure=Q3)
C.fixed([k('3', 'b', 'i')], None, None, figure=Q3)
C.fixed([k('3', 'b', 'ii')], None, None, figure=Q3)
C.ordered([k('3', 'b', 'iii')], None, None, figure=Q3)
C.ordered([k('3', 'b', 'iv')], None, None, figure=Q3)

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
for letter in ('a', 'c', 'd', 'g', 'i', 'j', 'k'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
for letter in ('b', 'e'):
    C.ordered([k('4', letter)], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'f')], None, None, notes=Q4_NOTE,
        fixes={'100 × 100 = 84 %': '84 ÷ 100 × 100 = 84 %'},
        row_notes={2: FRACTION.format('84', '100')})
C.ordered([k('4', 'h')], None, None, notes=Q4_NOTE,
          qtext=P.ask(k('4', 'h')) + ' ' + P.lead(k('4', 'h')))
C.fixed([ka('4', 'l', None, 'A')], None, None, notes=Q4_NOTE, cid='q4-l-a')
C.fixed([ka('4', 'l', None, 'B')], None, None, notes=Q4_NOTE, cid='q4-l-b')

# ── Q5 The atom ──────────────────────────────────────────────────────────────
C.ordered([k('5', 'a', r) for r in ('i', 'ii', 'iii')], None, None, cid='q5-a')
C.fixed([k('5', 'b', 'i')], None, None)
C.fixed([k('5', 'b', 'ii')], None, None)
C.ordered([k('5', 'b', 'iii')], None, None)
C.fixed([k('5', 'b', 'iv')], None, None)
C.ordered([k('5', 'c', r) for r in ('i', 'ii')], None, None, cid='q5-c')

# ── Q6 Hydrocarbons ──────────────────────────────────────────────────────────
# The paper lists C₄H₁₀ and C₅H₁₂ in a font whose numbers the text layer
# reads on the line; they are the same characters, set as the page shows.
Q6_STEM = P.rearranged(P.rearranged(P.ask(k('6')), 'C4H10', 'C₄H₁₀'), 'C5H12', 'C₅H₁₂')
C.fixed([k('6', 'a')], None, None, stem=Q6_STEM)
C.ordered([k('6', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-2-4',
          'alkanes-aromatics-and-propene', cid='q6-b', stem=Q6_STEM,
          drawn={k('6', 'b', 'iii')}, figure=S + 'q6b-iii')
C.ordered([k('6', 'c', r) for r in ('i', 'ii')], None, None, cid='q6-c-fig', stem=Q6_STEM,
          figure=FIG + 'paper-q6c')
C.fixed([k('6', 'd')], None, None, stem=Q6_STEM, skip=('C₂H₂ Br₂ solution',))

# ── Q7 Acids, bases and pH ───────────────────────────────────────────────────
C.fixed([k('7', 'a')], None, None)
C.fixed([k('7', 'b', 'i')], 'chem-3-4', 'formula-equation-for-potassium-and-water', cid='q7-b')
C.fixed([k('7', 'b', 'ii')], 'chem-3-4', 'balancing-the-potassium-water-equation')
C.ordered([k('7', 'b', 'iii')], None, None)
C.ordered([k('7', 'c', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-3-4',
          'ph-definition-calculation-and-ph-up', cid='q7-c-i-ii')

# ── Q8 Reactions of ethene ───────────────────────────────────────────────────
Q8 = FIG + 'paper-q8-fig0'
C.fixed([k('8', 'a', 'i')], None, None, figure=Q8)
# Drawing ethanol needs nothing from the reaction scheme: no stem.
C.drawn([k('8', 'a', 'ii')], 'chem-4-2', 'structure-of-ethanol', S + 'q8a-ii', stem='')
C.fixed([k('8', 'a', 'iii')], None, None, figure=Q8)
C.fixed([k('8', 'a', 'iv')], None, None, figure=Q8)
C.fixed([k('8', 'b', 'i')], 'chem-4-2', 'catalyst-for-dehydrating-ethanol', cid='q8-b', figure=Q8)
C.fixed([k('8', 'b', 'ii')], 'chem-4-2', 'ethanol-to-ethene-is-elimination', figure=Q8)
C.fixed([k('8', 'c', 'i')], 'chem-4-2', 'adding-hcl-to-ethene', cid='q8-c', figure=Q8)
C.fixed([k('8', 'c', 'ii')], 'chem-4-2', 'adding-chlorine-to-ethene', figure=Q8)
C.ordered([k('8', 'd', r) for r in ('i', 'ii')], None, None, cid='q8-d', figure=Q8)

# ── Q9 Redox and electrolysis ────────────────────────────────────────────────
C.fixed([k('9', 'a')], None, None, deep=True)
# The paper sets Q9(b)'s equations in a font whose charges and subscripts the
# text layer reads on the line; they are the same characters, set as printed.
_q9b = P.ask(k('9', 'b'))
for old, new in [('Cu2+(aq) + 2e– → Cu(s)', 'Cu²⁺(aq) + 2e⁻ → Cu(s)'),
                 ('Zn(s) → Zn2+(aq) + 2e–', 'Zn(s) → Zn²⁺(aq) + 2e⁻'),
                 ('CuSO4(aq) + Zn(s) → Cu(s) + ZnSO4(aq)', 'CuSO₄(aq) + Zn(s) → Cu(s) + ZnSO₄(aq)')]:
    _q9b = P.rearranged(_q9b, old, new)
C.fixed([k('9', 'b', 'i')], 'chem-3-5', 'copper-half-equation-is-reduction', cid='q9-b',
        stem=_q9b)
C.fixed([k('9', 'b', 'ii')], 'chem-3-5', 'reducing-agent-in-zinc-and-copper-sulfate', stem=_q9b)
C.fixed([k('9', 'b', 'iii')], 'chem-3-5', 'observation-when-zinc-meets-copper-sulfate', stem=_q9b)
C.fixed([k('9', 'b', 'iv')], 'chem-3-5', 'zinc-above-copper-in-the-electrochemical-series',
        stem=_q9b)
Q9C = FIG + 'paper-q9c'
C.fixed([k('9', 'c', 'i')], 'chem-3-5', 'meaning-of-inert-electrodes', cid='q9-c-i-iii',
        figure=Q9C)
C.fixed([k('9', 'c', 'ii')], 'chem-3-5', 'material-for-inert-electrodes', figure=Q9C)
C.fixed([k('9', 'c', 'iii')], 'chem-3-5', 'why-acid-is-added-before-electrolysing-water',
        figure=Q9C)
C.fixed([k('9', 'c', 'iv')], 'chem-3-5', 'gases-from-electrolysing-water', cid='q9-c-iv-v',
        figure=Q9C)
C.fixed([k('9', 'c', 'v')], 'chem-3-5', 'gas-formed-at-the-negative-electrode', figure=Q9C)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.ordered([k('10', 'a', r) for r in ('i', 'ii', 'iii', 'iv')], None, None, cid='q10-a',
          figure=FIG + 'paper-q10a')
C.ordered([k('10', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-1-1',
          'states-of-matter-and-particles', cid='q10-b-i-iii')
C.ordered([k('10', 'c', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-1-4',
          'moles-mass-and-gas-volume-from-an-equation', cid='q10-c-i-iii',
          fixes={'70 = 2 (moles)': '140 ÷ 70 = 2 (moles)'},
          row_notes={0: FRACTION.format('140', '70')})

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.ordered([k('11', 'a')], 'chem-1-3', 'elements-of-the-periodic-table-passage',
          cid='q11-a-1', figure=FIG + 'paper-q11a')
C.ordered([k('11', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v', 'vi')], 'chem-2-1',
          'bonding-type-solubility-and-dot-and-cross', cid='q11-b',
          drawn={k('11', 'b', 'vi')}, figure=S + 'q11b-vi')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q11b-print'
_q11c = P.rearranged(P.ask(k('11', 'c')), 'H2(g) + I2(g) ⇌ 2HI(g)', 'H₂(g) + I₂(g) ⇌ 2HI(g)')
C.ordered([k('11', 'c', r) for r in ('i', 'ii', 'iii', 'iv')], None, None, cid='q11-c',
          stem=_q11c, drawn={k('11', 'c', 'ii')}, figure=S + 'q11c-ii')
C.ordered([ka('11', 'd', r, 'A') for r in ('i', 'ii', 'iii', 'iv', 'v')], None, None,
          cid='q11-d-a', figure=FIG + 'paper-q11d-a')
C.ordered([ka('11', 'd', r, 'B') for r in ('i', 'ii', 'iii', 'iv', 'v')], None, None,
          cid='q11-d-b')


def review():
    """The ledger: every card's citation, tariff and rows; every letter's
    cards against the paper's printed mark; every place the paper and the
    scheme reprint differ."""
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for ref, reason in C.open:
        out.append(f'OPEN {ref}: {reason}')
    out.append('')
    for key, (got, want) in sorted(C.letter_totals().items(),
                                   key=lambda kv: (int(kv[0][0]), kv[0][1])):
        out.append(f'Q{key[0]}({key[1]}) printed {want}, carded {got}')
    for key, ask, s in dict.fromkeys(P.inexact):
        out.append(f'PAPER≠REPRINT {key}: paper "{ask}" / scheme "{s}"')
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
