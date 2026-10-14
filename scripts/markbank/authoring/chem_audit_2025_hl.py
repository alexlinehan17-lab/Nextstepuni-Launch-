#!/usr/bin/env python3
"""2025 Higher Level Chemistry, re-carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_audit_2025_hl.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_audit_2025_hl.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2025 hl    # write them

The sitting was carded before the audit (chem_2025_hl.py and its siblings).
This file replaces those cards' text with the paper's and the scheme's own,
the way chem_2026_hl.py cards 2026, and keeps every card id a student may
have progress on:

  * a pre-audit card whose parts are still one card keeps its id;
  * a pre-audit card that joined parts the scheme prices with cells of their
    own ("(i)-(iii)", each part closed by its own "(3)") keeps its id on its
    FIRST part, and each later part is a new card. Where the old concept slug
    named the joined parts, the first part gets its own;
  * a pre-audit card that duplicated another is withdrawn (WITHDRAWN below):
    chem_apply_print.py drops it at build time with a card-corrections.json
    record naming its replacement, and aliases its id to that replacement so
    its review history carries over.

Every question text, stem and lead-in is the PAPER's print of its part; every
marking point is the SCHEME's bold answer closed by its own mark cell. The
paper's figures (chem_print_figures.py CROPS) are read as pictures: their
labels stay out of the text (Printed(..., figures=True)). Where the scheme's
text layer cannot carry a printed fraction or root, the one form of the line
it can is given as a fix, checked against the scheme by the provenance gate's
own normalisation, and the scheme's print is shown with the answer where the
form loses its layout.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, point, MAX_OPTIONS  # noqa: E402

P = Printed(2025, 'hl', figures=True)
C = Cards(P)
# New cards under Q11(d) follow the sitting's own pre-audit ids
# ("q11-da-iii", "q11-db-iii"), not the 2026 form ("q11-d-a-iii").
FIG = 'chemistry-2025-HL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'

# The scheme's note on Q4, lifted from its print.
Q4_NOTE = 'The scheme: "' + P.items(('4', None, None, None))[0].text + '"'
if not P.traceable(Q4_NOTE[13:-1]):
    raise Refused('Q4 note is not in the scheme')

# Pre-audit cards withdrawn, each with the card that now holds its parts.
WITHDRAWN = {
    'chem-2025-hl-q10-c-i-total': (
        'chem-2025-hl-q10-c-i-mr',
        'Q10(c)(i) is one part, priced as nine (2) points; the pre-audit deck split it into '
        'two cards with the same citation and the build kept only one. Carded once, as '
        'chem-2025-hl-q10-c-i-mr.'),
    'chem-2025-hl-q11-db-i-iii-fig': (
        'chem-2025-hl-q11-db-i-ii',
        'Duplicated Q11(d)B(i)-(iii) beside chem-2025-hl-q11-db-i-ii and -db-iii. Each part '
        'is now its own card; the apparatus figure is on every Q11(d)B card.'),
}

# ── Q1 Volumetric analysis: iron(II) in iron tablets ─────────────────────────
C.fixed([('1', 'a', None, None)], None, None)
C.fixed([('1', 'b', 'i', None)], None, None)
C.fixed([('1', 'b', 'ii', None)], None, None)
C.fixed([('1', 'c', 'i', None)], 'chem-4-1', 'apparatus-for-transferring-an-exact-volume',
        cid='q1-c')
C.fixed([('1', 'c', 'ii', None)], 'chem-4-1', 'pipette-rinsing-before-use')
C.fixed([('1', 'd', 'i', None)], None, None)
C.fixed([('1', 'd', 'ii', None)], None, None)
C.fixed([('1', 'd', 'iii', None)], None, None)
C.fixed([('1', 'e', 'i', None)], None, None,
        fixes={'0.010 1000 × 22.5 = 0.000225 / 2.25 × 10⁻⁴ (moles per 22.5 cm³)':
               '0.010 ÷ 1000 × 22.5 = 0.000225 / 2.25 × 10⁻⁴ (moles per 22.5 cm³)'},
        row_notes={0: FRACTION.format('0.010', '1000')})
C.fixed([('1', 'e', 'ii', None)], None, None)
C.fixed([('1', 'e', 'iii', None)], None, None)
C.fixed([('1', 'e', 'iv', None)], None, None,
        fixes={'0.416 = 0.2524, × 100 = 25.24 (%) // 0.105 2.496 = 0.2524, × 100 = 25.24 (%) 0.630':
               '0.105 ÷ 0.416 = 0.2524, × 100 = 25.24 (%) // 0.630 ÷ 2.496 = 0.2524, × 100 = 25.24 (%)'},
        row_notes={0: 'The scheme prints 0.105 over 0.416 and 0.630 over 2.496 as fractions; '
                      '÷ stands for each bar.'})

# ── Q2 Steam distillation of clove oil; extracting eugenol ───────────────────
Q2 = FIG + 'paper-q2'
for roman in ('i', 'ii', 'iii'):
    C.fixed([('2', 'a', roman, None)], None, None, figure=Q2)
C.menu([('2', 'b', 'i', None)], None, None, figure=Q2)
C.menu([('2', 'b', 'ii', None)], None, None, figure=Q2)
C.fixed([('2', 'b', 'iii', None)], None, None, figure=Q2)
C.fixed([('2', 'b', 'iv', None)], None, None, figure=Q2)
C.fixed([('2', 'c', 'i', None)], None, None, figure=Q2)
C.drawn([('2', 'c', 'ii', None)], 'chem-4-2', 'structure-of-eugenol', S + 'q2c-ii')
C.fixed([('2', 'c', 'iii', None)], None, None, figure=Q2)
C.ordered([('2', 'c', 'iv', None)], None, None, figure=Q2)

# ── Q3 Rate of decomposition of hydrogen peroxide ────────────────────────────
Q3 = FIG + 'paper-q3'
C.fixed([('3', 'a', 'i', None)], None, None, figure=Q3)
C.fixed([('3', 'a', 'ii', None)], None, None, figure=Q3)
C.fixed([('3', 'b', 'i', None)], None, None, figure=Q3)
C.ordered([('3', 'b', 'ii', None)], None, None, figure=Q3)
C.ordered([('3', 'b', 'iii', None)], None, None, figure=Q3)
C.fixed([('3', 'c', 'i', None)], None, None, figure=Q3, cid='q3-c')
C.fixed([('3', 'c', 'ii', None)], 'chem-3-2', 'average-rate-over-the-second-minute', figure=Q3)
C.fixed([('3', 'c', 'iii', None)], 'chem-3-2', 'why-the-rate-falls-as-the-reaction-proceeds',
        figure=Q3)
C.ordered([('3', 'd', 'i', None), ('3', 'd', 'ii', None)], None, None, figure=Q3, cid='q3-d')

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
for letter in ('a', 'c', 'd', 'f', 'h', 'i', 'j', 'k'):
    C.fixed([('4', letter, None, None)], None, None, deep=True, notes=Q4_NOTE)
C.fixed([('4', 'b', None, None)], None, None, notes=Q4_NOTE,
        qtext=P.rearranged(P.ask(('4', 'b', None, None)), 'Cr³⁺ 52 ion? 24', '⁵²₂₄Cr³⁺ ion?'))
C.fixed([('4', 'e', None, None)], None, None, notes=Q4_NOTE,
        fixes={'57.84 12 : 3.61 1 : 38.55 16': '57.84 ÷ 12 : 3.61 ÷ 1 : 38.55 ÷ 16'},
        row_notes={0: 'The scheme prints each ratio as a fraction (57.84 over 12, 3.61 over 1, '
                      '38.55 over 16); ÷ stands for each bar.'})
C.drawn([('4', 'g', None, None)], 'chem-2-4', 'isomers-of-butane', S + 'q4g', notes=Q4_NOTE)
C.fixed([('4', 'l', None, 'A')], None, None, notes=Q4_NOTE, cid='q4-l-a')
C.fixed([('4', 'l', None, 'B')], None, None, notes=Q4_NOTE, cid='q4-lb-fig',
        figure=FIG + 'paper-q4l-b')

# ── Q5 Isotopes, orbitals, atomic radius ─────────────────────────────────────
for roman in ('i', 'ii', 'iii', 'iv'):
    C.fixed([('5', 'a', roman, None)], None, None)
Q5B = FIG + 'paper-q5b'
C.fixed([('5', 'b', 'i', None)], None, None, figure=Q5B)
C.drawn([('5', 'b', 'ii', None)], 'chem-1-2', 'shape-of-an-s-orbital', S + 'q5b-ii')
for roman in ('iii', 'iv', 'v'):
    C.fixed([('5', 'b', roman, None)], None, None, figure=Q5B)
C.ordered([('5', 'c', r, None) for r in ('i', 'ii', 'iii')], None, None, cid='q5-c')

# ── Q6 Fuels and heats of reaction ───────────────────────────────────────────
for roman in ('i', 'ii', 'iii', 'iv', 'v'):
    C.fixed([('6', 'a', roman, None)], None, None)
C.ordered([('6', 'b', r, None) for r in ('i', 'ii', 'iii')], None, None, cid='q6-b')

# Q6(c): four working lines, each priced "(2 [multiplicative factor] + 1
# [sign])" beside its (3), then the answer (2).
PRICE = ' (2 [multiplicative factor] + 1 [sign])'
_rows = []
for it in P.items(('6', 'c', None, None)):
    head, sep, _ = it.text.partition(PRICE)
    note = 'The scheme prices this line' + PRICE + '.' if sep else ''
    _rows.append(C.lifted(f'r-{len(_rows) + 1}', head, int(it.cell.strip('[]')), note))
C.add([('6', 'c', None, None)], None, None, _rows)

# ── Q7 Acids and bases ───────────────────────────────────────────────────────
C.fixed([('7', 'a', 'i', None)], 'chem-3-4', 'bronsted-lowry-acid-and-base', cid='q7-a-i-ii')
C.fixed([('7', 'a', 'ii', None)], 'chem-3-4', 'strong-and-weak-acids-bronsted-lowry')
C.fixed([('7', 'a', 'iii', None)], None, None, cid='q7-a-iii-iv')
C.fixed([('7', 'a', 'iv', None)], 'chem-3-4', 'identifying-conjugate-acid-base-pairs',
        qtext=P.rearranged(P.ask(('7', 'a', 'iv', None)),
                           'HCO3—(aq) + H2O(l) ⇌ H2CO3(aq)', 'HCO₃⁻(aq) + H₂O(l) ⇌ H₂CO₃(aq)'))
C.fixed([('7', 'b', 'i', None)], None, None)
C.fixed([('7', 'b', 'ii', None)], None, None)
C.fixed([('7', 'b', 'iii', None)], None, None,
        fixes={'√KaMacid = [H⁺] / –log₁₀√KaMacid': '√(KaMacid) = [H⁺] / –log₁₀√(KaMacid)',
               'KaMacid = 0.0000048 / √KaMacid = 0.00219': 'KaMacid = 0.0000048 / √(KaMacid) = 0.00219'},
        row_notes={0: 'The scheme sets Ka and Macid together under one root sign.',
                   1: 'The scheme sets Ka and Macid together under one root sign.'})
C.fixed([('7', 'c', 'i', None)], None, None)
C.fixed([('7', 'c', 'ii', None)], None, None,
        fixes={'[H⁺] = √9.61 × 10⁻¹⁴ / [H⁺] = 3.1 × 10⁻⁷': '[H⁺] = √(9.61 × 10⁻¹⁴) / [H⁺] = 3.1 × 10⁻⁷'},
        row_notes={0: 'The scheme sets 9.61 × 10⁻¹⁴ under one root sign.'})
C.fixed([('7', 'd', 'i', None)], None, None, figure=FIG + 'paper-q7d-eq')
C.fixed([('7', 'd', 'ii', None)], 'chem-3-4', 'choosing-an-indicator-from-a-ph-curve',
        figure=FIG + 'paper-q7d-ii')

# ── Q8 Reaction scheme from ethanal ──────────────────────────────────────────
Q8 = FIG + 'paper-q8'
# The scheme answers Q8(a)'s three parts together after the third, each line
# carrying its part's label: "(i) C" (2), "(ii) B" (2), "(iii) A" (2).
_q8a = P.items(('8', 'a', 'iii', None))
assert [it.cell for it in _q8a] == ['[2]'] * 3, _q8a
for i, (roman, concept) in enumerate([('i', 'identifying-a-substitution-reaction'),
                                      ('ii', 'identifying-an-oxidation-reaction'),
                                      ('iii', 'identifying-a-reduction-reaction')]):
    label, answer = _q8a[i].text.split(' ', 1)
    assert label == f'({roman})', _q8a[i].text
    C.add([('8', 'a', roman, None)], 'chem-4-2', concept,
          [C.lifted('r-1', answer, 2, f'The scheme prints the answers to (i)-(iii) together '
                                      f'after (iii), this one as "{_q8a[i].text}".')],
          figure=Q8)
C.fixed([('8', 'b', 'i', None)], 'chem-4-2', 'homologous-series-of-ethanal', cid='q8-b-i-ii',
        figure=Q8)
C.fixed([('8', 'b', 'ii', None)], 'chem-4-2', 'fehlings-test-colour-change', figure=Q8)
C.fixed([('8', 'b', 'iii', None)], None, None, figure=Q8)
C.drawn([('8', 'c', 'i', None)], 'chem-4-2', 'structure-of-ethyl-ethanoate', S + 'q8c-i')
C.drawn([('8', 'c', 'ii', None)], 'chem-4-2', 'labelled-oxygen-in-ethyl-ethanoate', S + 'q8c-ii')
C.drawn([('8', 'c', 'iii', None)], 'chem-4-2', 'bond-formed-in-esterification', S + 'q8c-iii')
C.fixed([('8', 'c', 'iv', None)], 'chem-2-1', 'sigma-bond-electrons-in-ethyl-ethanoate',
        cid='q8-c-iv-vi', figure=Q8)
C.fixed([('8', 'c', 'v', None)], 'chem-2-1', 'pi-bond-electrons-in-ethyl-ethanoate', figure=Q8)
C.fixed([('8', 'c', 'vi', None)], 'chem-2-1', 'lone-pairs-in-ethyl-ethanoate', figure=Q8)
C.fixed([('8', 'd', 'i', None)], None, None, figure=Q8)
C.fixed([('8', 'd', 'ii', None)], None, None, figure=Q8)

# ── Q9 Chemical equilibrium: nitrosyl bromide ────────────────────────────────
C.fixed([('9', 'a', 'i', None)], 'chem-3-3', 'reversible-reaction', cid='q9-a')
C.fixed([('9', 'a', 'ii', None)], 'chem-3-3', 'constant-concentrations-at-dynamic-equilibrium')
C.fixed([('9', 'b', 'i', None)], None, None,
        fixes={'110 = 0.5 (moles of NOBr) 55': '55 ÷ 110 = 0.5 (moles of NOBr)'},
        row_notes={1: FRACTION.format('55', '110')})
C.fixed([('9', 'b', 'ii', None)], None, None)
# Q9(b)(iii): the Kc expression is one fraction priced (6). Its denominator,
# "[NOBr]", is bracketed like an examiner's aside, so the row is given whole.
_kc = P.items(('9', 'b', 'iii', None))
assert len(_kc) == 1 and _kc[0].cell == '[6]', _kc
C.add([('9', 'b', 'iii', None)], None, None, [C.lifted(
    'r-1', '[NO]²[Br₂] ÷ [NOBr]²', 6,
    'The scheme prints [NO]²[Br₂] over [NOBr]² as a fraction; ÷ stands for its bar, and its '
    'own print is shown with the answer. The scheme adds: ' + ' '.join(_kc[0].asides))],
    figure=S + 'q9b-iii')
C.fixed([('9', 'b', 'iv', None)], None, None, figure=S + 'q9b-iv', skip=('(0.055)²',),
        fixes={'(0.195)² (0.0975) Kc = = 1.2 (mol L⁻¹)': '1.2 (mol L⁻¹)'},
        row_notes={3: 'The scheme sets this step as Kc = (0.195)² (0.0975) over (0.055)² '
                      '= 1.2 (mol L⁻¹); its own print is shown with the answer.'})
for roman in ('i', 'ii', 'iii'):
    C.ordered([('9', 'c', roman, None)], None, None)

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([('10', 'a', 'i', None)], None, None)
C.drawn([('10', 'a', 'ii', None)], 'chem-2-1', 'dot-and-cross-diagram-of-nf3', S + 'q10a-ii')
C.fixed([('10', 'a', 'iii', None)], None, None)
C.drawn([('10', 'a', 'iv', None)], 'chem-2-2', 'dipole-dipole-forces-between-nf3-molecules',
        S + 'q10a-iv')
C.fixed([('10', 'a', 'v', None)], None, None)
C.fixed([('10', 'a', 'vi', None)], None, None)
C.drawn([('10', 'b', 'i', None)], 'chem-4-2', 'structure-of-ethene', S + 'q10b-i')
C.fixed([('10', 'b', 'ii', None)], None, None)
C.fixed([('10', 'b', 'iii', None)], None, None)
C.drawn([('10', 'b', 'iv', None)], 'chem-4-2', 'carbocation-intermediate-in-ionic-addition',
        S + 'q10b-iv')
C.fixed([('10', 'b', 'v', None)], None, None)
C.fixed([('10', 'b', 'vi', None)], None, None)
C.fixed([('10', 'c', 'i', None)], 'chem-1-4', 'mass-of-sodium-hydrogencarbonate-for-two-acids',
        cid='q10-c-i-mr',
        fixes={'192 = 0.0005 (moles of C₆H₈O₇)': '0.096 ÷ 192 = 0.0005 (moles of C₆H₈O₇)',
               '150 = 0.001 (moles of C₄H₆O₆)': '0.15 ÷ 150 = 0.001 (moles of C₄H₆O₆)'},
        row_notes={3: FRACTION.format('0.096', '192'), 5: FRACTION.format('0.15', '150')})
C.fixed([('10', 'c', 'ii', None)], None, None)
C.fixed([('10', 'c', 'iii', None)], 'chem-1-4', 'number-of-water-molecules-produced')

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.fixed([('11', 'a', 'i', None)], 'chem-4-3', 'total-hardness', cid='q11-a-i-iii')
C.fixed([('11', 'a', 'ii', None)], 'chem-4-3', 'full-name-of-edta')
C.fixed([('11', 'a', 'iii', None)], 'chem-4-3', 'removing-total-hardness')
C.fixed([('11', 'a', 'iv', None)], None, None)
C.fixed([('11', 'a', 'v', None)], 'chem-4-3', 'detecting-lead-ions-in-water', cid='q11-a-v-vi')
C.fixed([('11', 'a', 'vi', None)], 'chem-4-3', 'removing-lead-ions-from-water')
C.fixed([('11', 'a', 'vii', None)], None, None)
C.fixed([('11', 'b', 'i', None)], 'chem-3-1', 'why-the-temperature-rises-on-neutralisation',
        cid='q11-b-i-ii')
C.fixed([('11', 'b', 'ii', None)], 'chem-3-1', 'heat-of-reaction-meaning')
C.fixed([('11', 'b', 'iii', None)], None, None,
        fixes={'1000 = 0.08 (moles) 80': '80 ÷ 1000 = 0.08 (moles)'},
        row_notes={0: FRACTION.format('80', '1000')})
C.fixed([('11', 'b', 'iv', None)], 'chem-3-1', 'heat-energy-from-mc-delta-theta', cid='q11-b-iv-v')
C.fixed([('11', 'b', 'v', None)], 'chem-3-1', 'heat-of-neutralisation-from-heat-energy')
C.fixed([('11', 'c', 'i', None)], 'chem-1-2', 'discovery-of-radium', cid='q11-c-i-iii')
C.fixed([('11', 'c', 'ii', None)], 'chem-1-2', 'what-an-alpha-particle-is')
C.fixed([('11', 'c', 'iii', None)], 'chem-1-2', 'radium-226-alpha-decay')
C.fixed([('11', 'c', 'iv', None)], 'chem-1-2', 'low-penetrating-power-of-alpha-radiation',
        cid='q11-c-iv-v')
C.fixed([('11', 'c', 'v', None)], 'chem-1-2', 'long-half-life-of-radium-226',
        skip=('225 Ra → Z X + 0 e 88 Y —1',))
Q11C = FIG + 'paper-q11c-eq'
C.fixed([('11', 'c', 'vi', None)], 'chem-1-2', 'mass-number-after-beta-decay', cid='q11-c-vi-viii',
        figure=Q11C)
C.fixed([('11', 'c', 'vii', None)], 'chem-1-2', 'atomic-number-after-beta-decay', figure=Q11C)
C.fixed([('11', 'c', 'viii', None)], 'chem-1-2', 'element-formed-by-beta-decay-of-radium-225',
        figure=Q11C)
C.fixed([('11', 'd', 'i', 'A')], 'chem-4-3', 'inertness-of-nitrogen-gas', cid='q11-da-i-ii')
C.fixed([('11', 'd', 'ii', 'A')], 'chem-4-3', 'fixation-of-nitrogen-by-lightning',
        cid='q11-da-ii')
C.fixed([('11', 'd', 'iii', 'A')], None, None, cid='q11-da-iii')
C.fixed([('11', 'd', 'iv', 'A')], 'chem-4-3', 'why-plants-need-nitrogen', cid='q11-da-iv-vi')
C.fixed([('11', 'd', 'v', 'A')], 'chem-4-3', 'denitrification', cid='q11-da-v')
C.fixed([('11', 'd', 'vi', 'A')], 'chem-4-3', 'recycling-nitrogen-from-living-organisms',
        cid='q11-da-vi')
Q11DB = FIG + 'paper-q11d-b'
C.fixed([('11', 'd', 'i', 'B')], 'chem-3-5', 'meaning-of-electrolysis', cid='q11-db-i-ii',
        figure=Q11DB)
C.fixed([('11', 'd', 'ii', 'B')], 'chem-3-5', 'inert-electrode-materials', cid='q11-db-ii',
        figure=Q11DB)
C.fixed([('11', 'd', 'iii', 'B')], None, None, cid='q11-db-iii', figure=Q11DB)
C.fixed([('11', 'd', 'iv', 'B')], 'chem-3-5', 'oxidation-as-electron-loss', cid='q11-db-iv-vi',
        figure=Q11DB)
C.fixed([('11', 'd', 'v', 'B')], 'chem-3-5', 'product-at-the-anode', cid='q11-db-v',
        figure=Q11DB)
C.fixed([('11', 'd', 'vi', 'B')], 'chem-3-5', 'anode-half-equation-for-lead-bromide',
        cid='q11-db-vi', figure=Q11DB)


def review():
    """The ledger: every card's citation, tariff and rows; every open part;
    every letter's cards against the paper's printed mark; every place the
    paper and the scheme reprint differ."""
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for ref, reason in C.open:
        out.append(f'OPEN {ref}: {reason}')
    out.append('')
    for k, (got, want) in sorted(C.letter_totals().items(), key=lambda kv: (int(kv[0][0]), kv[0][1])):
        out.append(f'Q{k[0]}({k[1]}) printed {want}, carded {got}')
    for key, ask, s in P.inexact:
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
