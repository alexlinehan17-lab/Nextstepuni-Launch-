#!/usr/bin/env python3
"""2024 Ordinary Level Chemistry, re-carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_audit_2024_ol.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2024_ol.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2024 ol    # write them

Drafted by chem_draft.py and corrected card by card, the way
chem_audit_2025_ol.py re-cards 2025 OL: every question text, stem and lead-in
is the PAPER's print of its part; every marking point is the SCHEME's answer
closed by its own mark cell. The Ordinary scheme prices many letters with one
cell for all their parts; those letters are one orderedSplit card each.
Pre-audit ids are kept (a card that joined parts priced by separate cells keeps
its id on its first part; later parts are new cards); WITHDRAWN lists the one
pre-audit card that held a piece of a task the scheme prices as one.

The scheme's text layer reports Calibri's "tt" ligature as one "t"
("pipete"); chem_print reads it by glyph id. Where a card needs both the
paper's picture before the reveal and the scheme's drawing after it (Q5(b),
Q8(b)(ii)), the question picture is the paper's own print of the part.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS  # noqa: E402

P = Printed(2024, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2024-OL-'
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
    'chem-2024-ol-q8-a-iv': (
        'chem-2024-ol-q8-a-iii',
        'The scheme prices Q8(a)(i)-(iv) with one cell ([8 + 6 + 2 + 2]), so they are one task; '
        'carded once, as chem-2024-ol-q8-a-iii (the first pre-audit card on it).'),
}
CHOSEN = ('The scheme prints only the criterion "{}" for this part: the answer depends on the '
          'industry the candidate has studied.')

# ── Q1 Preparing ethyne ──────────────────────────────────────────────────────
Q1 = 'chemistry-2024-OL-paper-p02-i0'
C.fixed([k('1', 'a', 'i')], None, None, figure=Q1)
C.fixed([k('1', 'a', 'ii')], None, None, figure=Q1)
C.ordered([k('1', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], None, None, cid='q1-b', figure=Q1)
C.ordered([k('1', 'c', 'i')], None, None, figure=Q1)
C.ordered([k('1', 'c', 'ii')], None, None, figure=Q1)
C.fixed([k('1', 'c', 'iii')], None, None, figure=Q1)

# ── Q2 Titration of hydrochloric acid against sodium carbonate ───────────────
Q2T = FIG + 'paper-q2-table'
C.fixed([k('2', 'a', 'i')], None, None, figure=FIG + 'paper-q2a',
        label_key=[{'letter': 'A', 'meaning': 'pipette', 'askedInThisQuestion': True}])
C.menu([k('2', 'a', 'ii')], None, None)
C.fixed([k('2', 'b', 'i')], 'chem-4-1', 'meaning-of-the-endpoint', cid='q2-b')
C.fixed([k('2', 'b', 'ii')], 'chem-4-1', 'indicator-for-a-sodium-carbonate-titration')
C.fixed([k('2', 'b', 'iii')], 'chem-4-1', 'colour-change-of-methyl-orange')
C.menu([k('2', 'b', 'iv')], None, None)
C.fixed([k('2', 'c', 'i')], None, None, figure=Q2T)
C.fixed([k('2', 'c', 'ii')], 'chem-4-1', 'concentration-of-hydrochloric-acid-from-a-titration',
        figure=Q2T,
        fixes={'20.55 × M': '20.55 × M ÷ 2', '2 25 × 0.05': '25 × 0.05 ÷ 1', '1 0.12 M': '0.12 M'},
        row_notes={0: FRACTION.format('20.55 × M', '2'), 1: FRACTION.format('25 × 0.05', '1')})

# ── Q3 Flame tests and tests for anions ──────────────────────────────────────
C.menu([k('3', 'a', 'i')], None, None)
C.ordered([k('3', 'a', 'ii')], None, None)
C.ordered([k('3', 'b', 'i')], None, None)
C.ordered([k('3', 'b', r) for r in ('ii', 'iii', 'iv', 'v')], None, None, cid='q3-b')

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
for letter in ('a', 'b', 'c', 'e'):
    C.ordered([k('4', letter)], None, None, notes=Q4_NOTE)
for letter in ('d', 'g', 'h', 'i', 'j'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.ordered([k('4', 'f', 'i'), k('4', 'f', 'ii')], 'chem-u2', 'meaning-of-hazard-symbols',
          figure=FIG + 'paper-q4f', notes=Q4_NOTE)
# The scheme's answer is the letter X; X's meaning on the label key is the
# question's own "aromatic compound", held back until the reveal.
C.fixed([k('4', 'k')], 'chem-2-4', 'which-cyclic-hydrocarbon-is-aromatic',
        figure=FIG + 'paper-q4k', notes=Q4_NOTE,
        label_key=[{'letter': 'X', 'meaning': 'aromatic compound', 'askedInThisQuestion': True}])
C.fixed([ka('4', 'l', None, 'A')], None, None, cid='q4-l-a', notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'B')], None, None, cid='q4-l-b', figure=FIG + 'paper-q4l-b',
        notes=Q4_NOTE)

# ── Q5 Electronegativity; nitrogen trifluoride ───────────────────────────────
Q5 = 'chemistry-2024-ol-paper-p006-i0'
C.ordered([k('5', 'a', r) for r in ('i', 'ii', 'iii')], None, None, cid='q5-a', figure=Q5)
# Q5(b): one cell over (i)-(vii); (iv) is answered with a drawing and (v)
# reads the table, so the question picture is the paper's print (Q5's opening
# and table, then (b)) and the figure is the scheme's dot and cross diagram.
C.ordered([k('5', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii')], 'chem-2-1',
          'nitrogen-trifluoride-bonding-and-shape', cid='q5-b', drawn={k('5', 'b', 'iv')},
          figure=S + 'q5b-iv')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q5b-print'

# ── Q6 Isomers of butane; octane number ──────────────────────────────────────
C.ordered([k('6', 'a', 'i')], None, None)
C.drawn([k('6', 'a', 'ii')], 'chem-2-4', 'structures-of-the-isomers-of-butane', S + 'q6a-ii')
C.ordered([k('6', 'a', r) for r in ('iii', 'iv', 'v')], None, None, cid='q6-a-iii-v')
C.ordered([k('6', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], None, None, cid='q6-b')

# ── Q7 Rate of decomposition of hydrogen peroxide ────────────────────────────
Q7 = FIG + 'paper-q7'
C.fixed([k('7', 'a', 'i')], None, None, figure=Q7)
C.fixed([k('7', 'a', 'ii')], 'chem-3-2', 'graph-of-volume-of-oxygen-against-time', figure=Q7)
C.fixed([k('7', 'a', 'iii')], None, None, figure=Q7)
C.fixed([k('7', 'a', 'iv')], None, None, figure=Q7)
C.ordered([k('7', 'b', 'i')], None, None, figure=Q7)
C.ordered([k('7', 'b', 'ii')], None, None, figure=Q7)
# (c) needs none of the apparatus or the results: its own lead-in only.
C.fixed([k('7', 'c', 'i')], 'chem-3-2', 'what-an-enzyme-is', cid='q7-c', stem=P.ask(k('7', 'c')))
C.fixed([k('7', 'c', 'ii')], 'chem-3-2', 'naming-an-enzyme', stem=P.ask(k('7', 'c')))

# ── Q8 The ethene reaction series ────────────────────────────────────────────
Q8 = 'chemistry-2024-ol-paper-p009-i0'
C.ordered([k('8', 'a', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-4-2',
          'compounds-of-the-ethene-reaction-series', cid='q8-a-iii', figure=Q8)
C.fixed([k('8', 'b', 'i')], None, None, figure=Q8)
# Drawing S needs the series that names it: its question picture is the
# paper's print (Q8's series, (b)'s lead-in, the ask); the scheme's drawing is
# the answer.
C.drawn([k('8', 'b', 'ii')], 'chem-4-2', 'structure-of-ethanal', S + 'q8b-ii')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q8b-ii-print'
C.fixed([k('8', 'b', 'iii')], 'chem-4-2', 'fehlings-colour-change-with-an-aldehyde',
        cid='q8-b-iii-iv', figure=Q8)
C.fixed([k('8', 'b', 'iv')], 'chem-4-2', 'copper-in-fehlings-reagent', figure=Q8)
C.ordered([k('8', 'c', 'i'), k('8', 'c', 'ii')], None, None, cid='q8-c', figure=Q8)

# ── Q9 Neutralisation, pH, water treatment ───────────────────────────────────
C.fixed([k('9', 'a', 'i')], None, None)
C.fixed([k('9', 'a', 'ii')], None, None)
C.ordered([k('9', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], None, None, cid='q9-b')
C.ordered([k('9', 'c')], 'chem-4-3', 'stages-of-water-treatment', figure=FIG + 'paper-q9c-table')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('10', 'a', 'i')], None, None)
# (a)(i) and (c)(i) ask about a term the paper underlines, which no text layer carries: the paper's
# own print of the part is the question ((c)'s map, printed beside it, left out).
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q10a-i-print'
C.fixed([k('10', 'a', 'ii')], 'chem-1-4', 'empirical-formula-of-multistriatin',
        fixes={'C: 70.59 12 = 5.88': 'C: 70.59 ÷ 12 = 5.88', 'H: 10.59 1 = 10.59': 'H: 10.59 ÷ 1 = 10.59',
               'O: 18.82 16 = 1.18': 'O: 18.82 ÷ 16 = 1.18'},
        row_notes={0: 'The scheme prints each ratio as a fraction (70.59 over 12, 10.59 over 1, '
                      '18.82 over 16); ÷ stands for each bar.'})
C.fixed([k('10', 'a', 'iii')], None, None)
C.fixed([k('10', 'a', 'iv')], None, None)
_q10b = P.rearranged(P.ask(k('10', 'b')), '2NO2(g) ⇌ N2O4(g)', '2NO₂(g) ⇌ N₂O₄(g)')
C.fixed([k('10', 'b', 'i')], 'chem-3-3', 'kc-expression-for-nitrogen-dioxide-and-dinitrogen-tetroxide',
        stem=_q10b, figure=S + 'q10b-i', fixes={'[N₂O₄] [NO₂]²': '[N₂O₄] ÷ [NO₂]²'},
        row_notes={0: "The scheme prints [N₂O₄] over [NO₂]² as a fraction; ÷ stands for its bar, "
                      "and its own print is shown with the answer."})
C.ordered([k('10', 'b', 'ii')], None, None, stem=_q10b + ' ' + P.lead(k('10', 'b', 'i')))
C.ordered([k('10', 'b', 'iii')], None, None, stem=_q10b + ' ' + P.lead(k('10', 'b', 'i')))
# Q10(c): the paper sets radon-222's mass and atomic numbers around its symbol;
# the text layer reads the atomic number after the line. The same characters,
# set as printed.
_q10c = P.rearranged(P.ask(k('10', 'c')), '( 222 Rn ) are found in areas such as 86 Galway',
                     '(²²²₈₆Rn) are found in areas such as Galway')
C.ordered([k('10', 'c', 'i')], None, None, stem=_q10c)
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q10c-i-print'
C.ordered([k('10', 'c', r) for r in ('ii', 'iii', 'iv')], None, None, cid='q10-c-ii-iv',
          stem=_q10c, qtext=' '.join(
              f'({r}) ' + P.rearranged(P.ask(k('10', 'c', r)), '222 Rn ? 86', '²²²₈₆Rn?')
              for r in ('ii', 'iii', 'iv')))
C.fixed([k('10', 'c', 'v')], None, None, stem=_q10c)
C.fixed([k('10', 'c', 'vi')], None, None, stem=_q10c)

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.ordered([k('11', 'a', r) for r in ('i', 'ii', 'iii')], None, None, cid='q11-a-i-iii')
C.ordered([k('11', 'a', r) for r in ('iv', 'v', 'vi')], None, None, cid='q11-a-iv-vi')
C.ordered([k('11', 'b', r) for r in ('i', 'ii')], None, None, cid='q11-b-i-ii')
C.fixed([k('11', 'b', 'iii')], 'chem-2-3', 'combined-gas-law-equation',
        fixes={'P₁V₁ T₁ = P₂V₂ T₂': 'P₁V₁ ÷ T₁ = P₂V₂ ÷ T₂'},
        row_notes={0: 'The scheme prints P₁V₁ over T₁ and P₂V₂ over T₂ as fractions; ÷ stands '
                      'for each bar.'})
C.ordered([k('11', 'b', 'iv')], 'chem-2-3', 'volume-of-a-gas-from-the-combined-gas-law',
          fixes={'95 × 253 300 = 105 × V₂ 350': '95 × 253 ÷ 300 = 105 × V₂ ÷ 350'},
          row_notes={0: 'The scheme prints 95 × 253 over 300 and 105 × V₂ over 350 as '
                        'fractions; ÷ stands for each bar.'})
C.ordered([k('11', 'c', 'i')], None, None)
C.fixed([k('11', 'c', 'ii')], None, None)
C.fixed([k('11', 'c', 'iii')], 'chem-u2', 'meaning-of-hplc', cid='q11-c-iii-iv')
C.fixed([k('11', 'c', 'iv')], 'chem-u2', 'another-instrumental-method-of-separation')
# Q11(d)A: the candidate names the industry, so for (i)-(iii) the scheme
# prints only what the examiner looks for, and that criterion is the row.
for roman, concept, crit in [('i', 'naming-a-chemical-industry-studied', 'named industry'),
                             ('ii', 'raw-materials-of-a-chemical-industry', 'appropriate raw materials'),
                             ('iii', 'quality-control-in-a-chemical-industry',
                              'description of quality control')]:
    C.fixed([ka('11', 'd', roman, 'A')], 'chem-u3', concept, cid=f'q11-d-a-{roman}',
            row_notes={0: CHOSEN.format(crit)})
C.fixed([ka('11', 'd', 'iv', 'A')], 'chem-u3', 'a-safety-issue-in-a-chemical-industry',
        cid='q11-d-a-iv-v')
C.fixed([ka('11', 'd', 'v', 'A')], 'chem-u3', 'a-factor-in-locating-a-chemical-industry',
        cid='q11-d-a-v')
C.menu([ka('11', 'd', 'i', 'B')], None, None, cid='q11-d-b-i')
C.ordered([ka('11', 'd', 'ii', 'B')], None, None, cid='q11-d-b-ii')
C.fixed([ka('11', 'd', 'iii', 'B')], 'chem-1-1', 'an-example-of-an-alloy', cid='q11-d-b-iii-iv')
C.ordered([ka('11', 'd', 'iv', 'B')], 'chem-1-1', 'composition-of-a-named-alloy',
          cid='q11-d-b-iv')
C.fixed([ka('11', 'd', 'v', 'B')], None, None, cid='q11-d-b-v')


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
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
