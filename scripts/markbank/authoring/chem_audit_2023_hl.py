#!/usr/bin/env python3
"""2023 Higher Level Chemistry, re-carded part by part from the paper and the labelled scheme.

    python3 scripts/markbank/authoring/chem_audit_2023_hl.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2023_hl.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2023 hl    # write them

The 2023 scheme is the labelled ("cue") layout of 2010-2023: it does not
reprint the question; each part's row opens with its letter, roman and an
examiner's cue ("IDENTIFY:"), then the answer, then the cell. chem_print reads
it (cue_lines); a card's question text is the paper's part up to its printed
mark, and what the paper prints after the mark, set back to the letter's
indent, is the next part's lead-in.

A calculation is priced as its answer and total, then the working step by
step, each step with its own cell, then other routes after "or". Where the
first route's text is clean, its steps are the rows (Cards.route); where it is
not -- stacked fractions, routes side by side, and the 2023 equation font's
doubled digits ("111111+9999" for 1.77 over 14n + 90) -- the row is the
scheme's answer line with the cell for the whole part (Cards.answer_only).
Either way the scheme's own print of the working is the card's figure.

Pre-audit ids are kept (a card that joined parts priced by separate cells
keeps its id on its first part; later parts are new cards); WITHDRAWN lists
the pre-audit cards that duplicated another or held a piece of a task the
scheme prices as one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS  # noqa: E402

P = Printed(2023, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2023-HL-'
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
    'chem-2023-hl-q3-c-i': (
        'chem-2023-hl-q3-c-fig',
        'Duplicated chem-2023-hl-q3-c-fig (the same Q3(c)(i)).'),
    'chem-2023-hl-q11-b-iv-vi': (
        'chem-2023-hl-q11-b-fig',
        'Duplicated chem-2023-hl-q11-b-fig (both cited Q11(b)(iv)-(vi)). Each part is now a '
        'card of its own; Q11(b)(iv) is chem-2023-hl-q11-b-fig.'),
    'chem-2023-hl-q11-c-v': (
        'chem-2023-hl-q11-c-fig',
        'Duplicated chem-2023-hl-q11-c-fig (the same Q11(c)(v)).'),
}

# ── Q1 Standardising potassium manganate(VII) ────────────────────────────────
C.menu([k('1', 'a')], None, None)
C.menu([k('1', 'b', 'i')], None, None)
C.fixed([k('1', 'b', 'ii')], None, None)
C.fixed([k('1', 'c', 'i')], None, None)
C.fixed([k('1', 'c', 'ii')], None, None)
C.route([k('1', 'd', 'i')], None, None, figure=S + 'q1d-i',
        fixes={'37.24 392 = 0.095 (9.5 × 10⁻², 19/200) moles (NH₄)₂SO₄·FeSO₄·6H₂O per litre':
               '37.24 ÷ 392 = 0.095 (9.5 × 10⁻², 19/200) moles (NH₄)₂SO₄·FeSO₄·6H₂O per litre'},
        row_notes={2: FRACTION.format('37.24', '392')})
C.answer_only([k('1', 'd', 'ii')], None, None, S + 'q1d-ii')
C.route([k('1', 'd', 'iii')], None, None)
C.answer_only([k('1', 'd', 'iv')], None, None, S + 'q1d-iv')

# ── Q2 Preparing ethyne ──────────────────────────────────────────────────────
C.fixed([k('2', 'a', 'i')], None, None)
C.fixed([k('2', 'a', 'ii')], None, None)
for r in ('i', 'ii', 'iii'):
    C.fixed([k('2', 'b', r)], None, None)
C.fixed([k('2', 'c', 'i')], None, None)
C.fixed([k('2', 'c', 'ii')], None, None)
C.ordered([k('2', 'c', 'iii')], None, None)
C.fixed([k('2', 'c', 'iv')], None, None)
C.answer_only([k('2', 'd')], None, None, S + 'q2d')

# ── Q3 Heat of neutralisation ────────────────────────────────────────────────
Q3 = 'chemistry-2023-HL-paper-p04-i0'
C.ordered([k('3', 'a')], None, None, figure=Q3)
C.fixed([k('3', 'b')], None, None, deep=True, figure=Q3)
C.fixed([k('3', 'c', 'i')], 'chem-3-1', 'why-the-temperature-rises-on-neutralisation',
        cid='q3-c-fig', figure=Q3)
C.fixed([k('3', 'c', 'ii')], None, None, figure=Q3)
C.fixed([k('3', 'c', 'iii')], None, None, figure=Q3)
C.answer_only([k('3', 'd', 'i')], None, None, S + 'q3d-i')
C.answer_only([k('3', 'd', 'ii')], None, None, S + 'q3d-ii')
C.route([k('3', 'd', 'iii')], None, None, figure=S + 'q3d-iii')
C.fixed([k('3', 'e', 'i')], None, None, figure=Q3)
C.fixed([k('3', 'e', 'ii')], None, None, figure=Q3)

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], None, None, deep=True, notes=Q4_NOTE)
C.fixed([k('4', 'b')], None, None, deep=True, notes=Q4_NOTE)
for letter in ('c', 'd', 'e', 'h'):
    C.fixed([k('4', letter)], None, None, notes=Q4_NOTE)
C.fixed([k('4', 'f')], None, None, cid='q4-f-fig', figure='chemistry-2023-HL-paper-p05-i1',
        notes=Q4_NOTE)
C.answer_only([k('4', 'g')], None, None, S + 'q4g', notes=Q4_NOTE)
# The scheme's box sets out the atoms in place but no bond lines: its PDF holds
# the box's frame and the letters, and nothing between them (page 11).
C.drawn([k('4', 'i')], 'chem-4-2', 'structure-of-glycerol', S + 'q4i',
        notes=Q4_NOTE + ' The scheme\'s print sets out the atoms in place without the lines for their bonds.')
C.ordered([k('4', 'j', 'i'), k('4', 'j', 'ii')], None, None, cid='q4-j', notes=Q4_NOTE)
C.answer_only([k('4', 'k')], None, None, S + 'q4k', cid='q4-k-fig', notes=Q4_NOTE)
C.ordered([ka('4', 'l', None, 'A')], None, None, cid='q4-l-a', notes=Q4_NOTE)
C.fixed([ka('4', 'l', None, 'B')], None, None, cid='q4-l-b', notes=Q4_NOTE)

# ── Q5 Atomic structure and electronegativity ────────────────────────────────
for r in ('i', 'ii'):
    C.fixed([k('5', 'a', r)], None, None)
C.menu([k('5', 'a', 'iii')], None, None)
C.fixed([k('5', 'a', 'iv')], None, None)
C.fixed([k('5', 'a', 'v')], None, None)
Q5B = FIG + 'paper-q5b'
for r in ('i', 'ii', 'iii', 'iv', 'v'):
    C.fixed([k('5', 'b', r)], None, None, figure=Q5B)

# ── Q6 Alkanes ───────────────────────────────────────────────────────────────
C.fixed([k('6', 'a', 'i')], 'chem-2-4', 'what-a-hydrocarbon-is', cid='q6-a')
C.fixed([k('6', 'a', 'ii')], 'chem-2-4', 'why-alkanes-are-saturated')
# Q6(b): the scheme draws two accepted structures after the condensed formula,
# separated by solidi; the formula is the row and its print the figure.
C.fixed([k('6', 'b')], None, None, figure=S + 'q6b',
        row_notes={1: 'The scheme also accepts either of the two structures it draws beside the '
                      'formula, separated by solidi; its own print is shown with the answer.'})
C.fixed([k('6', 'c')], None, None)
C.answer_only([k('6', 'd')], None, None, S + 'q6d')
Q6E = FIG + 'paper-q6e'
C.fixed([k('6', 'e', 'i')], None, None, figure=Q6E)
C.fixed([k('6', 'e', 'ii')], None, None, figure=Q6E)

# ── Q7 Acids, bases and water ────────────────────────────────────────────────
C.fixed([k('7', 'a', 'i')], 'chem-3-4', 'bronsted-lowry-acid', cid='q7-a')
C.fixed([k('7', 'a', 'ii')], 'chem-3-4', 'what-a-strong-acid-is')
C.fixed([k('7', 'a', 'iii')], 'chem-3-4', 'conjugate-base-of-hocl')
C.fixed([k('7', 'a', 'iv')], 'chem-3-4', 'conjugate-acid-of-hydrogensulfate')
C.route([k('7', 'b', 'i')], None, None)
C.answer_only([k('7', 'b', 'ii')], None, None, S + 'q7b-ii')
C.menu([k('7', 'c', 'i')], None, None)
C.route([k('7', 'c', 'ii')], None, None, figure=S + 'q7c-ii')
C.ordered([k('7', 'd', 'i')], None, None)
C.ordered([k('7', 'd', 'ii')], None, None)

# ── Q8 Reaction scheme from ethane ───────────────────────────────────────────
Q8 = 'chemistry-2023-HL-paper-q8-fig0'
Q8E = 'chemistry-2023-HL-paper-q8-fig1'
C.fixed([k('8', 'a', 'i')], None, None, figure=Q8)
C.fixed([k('8', 'a', 'ii')], None, None, figure=Q8)
C.fixed([k('8', 'b')], 'chem-4-2', 'reactant-and-catalyst-for-hydrogenation', deep=True,
        figure=Q8)
C.drawn([k('8', 'c', 'i')], 'chem-4-2', 'repeating-units-of-polyethene', S + 'q8c-i')
C.fixed([k('8', 'c', 'ii')], None, None, figure=Q8)
C.fixed([k('8', 'd', 'i')], None, None, figure=Q8)
C.fixed([k('8', 'd', 'ii')], None, None, figure=Q8)
for r in ('i', 'ii', 'iii'):
    C.fixed([k('8', 'e', r)], None, None, figure=Q8E)
C.fixed([k('8', 'e', 'iv')], 'chem-2-2', 'boiling-points-of-ethanal-and-propane', cid='q8-e',
        figure=Q8E)
C.fixed([k('8', 'e', 'v')], 'chem-2-2', 'boiling-points-of-ethanoic-acid-and-propanol',
        figure=Q8E)

# ── Q9 Equilibrium of PCl3, Cl2 and PCl5 ─────────────────────────────────────
C.ordered([k('9', 'a', 'i')], None, None)
C.fixed([k('9', 'a', 'ii')], None, None)
# Q9(b)(i): the Kc expression is set in the 2023 equation font, whose doubled
# glyphs the text layer cannot read back; the scheme's print is the answer.
C.drawn([k('9', 'b', 'i')], None, None, S + 'q9b-i')
C.answer_only([k('9', 'b', 'ii')], None, None, S + 'q9b-ii')
C.fixed([k('9', 'c')], None, None)
Q9D = FIG + 'paper-q9d'
C.fixed([k('9', 'd', 'i')], None, None, figure=Q9D)
C.fixed([k('9', 'd', 'ii')], None, None, figure=Q9D)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q10A = 'chemistry-2023-HL-paper-p11-i1'
C.fixed([k('10', 'a', 'i')], None, None, figure=Q10A)
C.fixed([k('10', 'a', 'ii')], None, None, figure=Q10A)
C.fixed([k('10', 'a', 'iii')], 'chem-2-1', 'electrons-in-carbon-hydrogen-bonds-of-benzene',
        cid='q10-a-electrons', figure=Q10A)
for r, concept in [('iv', 'electrons-in-carbon-carbon-sigma-bonds-of-benzene'),
                   ('v', 'electrons-in-delocalised-pi-bonding-of-benzene'),
                   ('vi', 'electrons-in-carbon-carbon-bonds-of-benzene'),
                   ('vii', 'electrons-not-involved-in-bonding-in-benzene')]:
    C.fixed([k('10', 'a', r)], 'chem-2-1', concept, figure=Q10A)
C.fixed([k('10', 'b', 'i')], None, None)
# Q10(b)(ii): both expressions are fractions in the 2023 equation font, whose
# doubled digits the text layer cannot read back; the scheme's print answers.
C.drawn([k('10', 'b', 'ii')], None, None, S + 'q10b-ii')
# Q10(b)(iii): the first step equates the two mole fractions (doubled digits);
# the scheme prints the same step cleared of fractions beside it, and that is
# the row. Then n and the molar mass, each with its cell.
_q10b3 = P.items(k('10', 'b', 'iii'))
assert [it.cell for it in _q10b3[:3]] == ['[2]', '[2]', '[3]'], _q10b3
C.add([k('10', 'b', 'iii')], None, None, [
    C.lifted('r-1', '24.78n + 237.18 = 34.02n + 218.7 / ⇒ 18.48 = 9.24n', 2,
             'The scheme first equates the two mole expressions, set as fractions, and clears '
             'them to this line; its own print is shown with the answer.'),
    C.lifted('r-2', 'n = 2', 2),
    C.lifted('r-3', 'molar mass of (CH₂)n(COOH)₂ = 118 g', 3)],
    figure=S + 'q10b-iii',
    notes='The scheme also accepts a trial-and-error route (letting n = 2 and showing the moles '
          'of acid and salt are equal), priced in the same marks; its own print is shown with '
          'the answer.')
C.route([k('10', 'b', 'iv')], None, None, figure=S + 'q10b-iv',
        fixes={'1.77 118 = 0.015 moles (CH₂)ₙ(COOH)₂': '1.77 ÷ 118 = 0.015 moles (CH₂)ₙ(COOH)₂',
               '0.03 = 0.12 × V 1000 ⇒ V = 250 cm³': '0.03 = 0.12 × V ÷ 1000 ⇒ V = 250 cm³'},
        row_notes={0: FRACTION.format('1.77', '118'), 2: FRACTION.format('0.12 × V', '1000')})
C.fixed([k('10', 'c', 'i')], None, None)
# Q10(c)(ii)-(iii): the scheme sets (iii)'s completed nuclear equation and its
# cell (3) on the rows under (ii)'s answer, before its own "(iii)" label; the
# equation's numbers are the doubled 2023 equation font. (ii) is its first
# item; (iii) is the paper's ask answered by the scheme's print, priced (3).
_q10c2 = P.items(k('10', 'c', 'ii'))
assert [it.cell for it in _q10c2] == ['[2 × 3]', '[3]'], _q10c2
_r1, _r2 = _q10c2[0].text.split(' // ')
C.add([k('10', 'c', 'ii')], None, None,
      [C.lifted('r-1', _r1, 3, 'The scheme prices these points [2 × 3], one each.'),
       C.lifted('r-2', _r2, 3)])
# The paper sets the nuclides' mass and atomic numbers around their symbols;
# the text layer reads them on the line. The same characters, set as printed.
_q10c3 = P.rearranged(P.ask(k('10', 'c', 'iii')), '53 131I → + 0 e –1', '¹³¹₅₃I → + ⁰₋₁e')
C.add([k('10', 'c', 'iii')], None, None, qtext=_q10c3, rows=[C.ask_row(
    k('10', 'c', 'iii'), 3, 'The scheme answers with the completed nuclear equation, printed in a '
                            'font its text cannot carry; its own print is shown with the answer.')],
    figure=S + 'q10c-iii')
C.cards[-1]['rows'][0]['verbatim'] = _q10c3      # the ask row is the ask as set
C.fixed([k('10', 'c', 'iv')], None, None)
C.fixed([k('10', 'c', 'v')], None, None)

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.ordered([k('11', 'a', 'i')], None, None, figure=S + 'q11a-i')
C.fixed([k('11', 'a', 'ii')], None, None)
C.ordered([k('11', 'a', 'iii')], None, None)
C.answer_only([k('11', 'a', 'iv')], None, None, S + 'q11a-iv')
C.menu([k('11', 'a', 'v')], None, None)
Q11B = 'chemistry-2023-HL-paper-p12-i0'
C.fixed([k('11', 'b', 'i')], 'chem-3-5', 'material-for-inert-electrodes', cid='q11-b-i-ii',
        figure=Q11B)
C.fixed([k('11', 'b', 'ii')], 'chem-3-5', 'oxidation-as-loss-of-electrons', figure=Q11B)
C.ordered([k('11', 'b', 'iii')], None, None, figure=Q11B)
C.fixed([k('11', 'b', 'iv')], 'chem-3-5', 'electrode-where-iodine-forms', cid='q11-b-fig',
        figure=Q11B)
C.fixed([k('11', 'b', 'v')], 'chem-3-5', 'why-phenolphthalein-turns-pink-at-the-cathode',
        figure=Q11B)
C.fixed([k('11', 'b', 'vi')], 'chem-3-5', 'colour-near-the-anode', figure=Q11B)
C.ordered([k('11', 'c', 'i')], None, None)
C.fixed([k('11', 'c', 'ii')], 'chem-3-2', 'effect-of-lowering-activation-energy',
        cid='q11-c-ii-iii')
C.fixed([k('11', 'c', 'iii')], 'chem-3-2', 'how-activation-energy-can-be-changed')
C.fixed([k('11', 'c', 'iv')], None, None)
C.menu([k('11', 'c', 'v')], None, None, cid='q11-c-fig', figure='chemistry-2023-HL-paper-p13-i0')
C.fixed([ka('11', 'd', 'i', 'A')], None, None)
C.fixed([ka('11', 'd', 'ii', 'A')], None, None)
C.answer_only([ka('11', 'd', 'iii', 'A')], None, None, S + 'q11da-iii')
C.fixed([ka('11', 'd', 'iv', 'A')], 'chem-4-3', 'industrial-sources-of-nitrogen-oxides',
        cid='q11-d-a-iv-v')
C.fixed([ka('11', 'd', 'v', 'A')], 'chem-4-3', 'what-a-greenhouse-gas-is', cid='q11-d-a-v')
Q11DB = FIG + 'paper-q11d-b'
C.ordered([ka('11', 'd', 'i', 'B')], None, None, figure=Q11DB)
C.fixed([ka('11', 'd', 'ii', 'B')], 'chem-u3', 'environmental-impact-of-an-alumina-plant',
        cid='q11-d-b-ii-iii', figure=Q11DB)
C.fixed([ka('11', 'd', 'iii', 'B')], 'chem-u3', 'economics-of-locating-an-aluminium-smelter',
        cid='q11-d-b-iii', figure=Q11DB)
C.fixed([ka('11', 'd', 'iv', 'B')], 'chem-3-5', 'why-alumina-must-be-molten',
        cid='q11-d-b-iv-v', figure=Q11DB)
C.ordered([ka('11', 'd', 'v', 'B')], 'chem-3-5', 'cathode-half-equation-for-aluminium',
          cid='q11-d-b-v', figure=Q11DB)
C.fixed([ka('11', 'd', 'vi', 'B')], None, None, figure=Q11DB)


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
