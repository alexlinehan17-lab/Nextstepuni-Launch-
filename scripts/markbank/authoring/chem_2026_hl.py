#!/usr/bin/env python3
"""2026 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2026_hl.py          # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2026_hl.py --review # the review ledger

Every question text, stem and lead-in is the PAPER's print of its part
(chem_print.Printed.ask / context); every marking point is the SCHEME's bold
answer, closed by its own mark cell. What this file adds is judgement only:
which parts form one card, the syllabus topic, a concept slug, which figure a
part needs, and -- where the scheme's text layer cannot carry a printed
fraction -- the one form of the line it can. Each such form is checked against
the scheme by the same normalisation the build's provenance gate applies, and
refused if it is not there.

Card boundaries follow the scheme's mark cells. One cell printed against two or
more parts ("[6+2+2+2]" closing Q1(b)(i) and (ii)) is one card whose points
carry no value of their own (orderedSplit). A printed choice ("[any two]")
is one anyN row listing every option. Q4's twelve items are each a card; Q4(l)
and Q11(d) offer whole alternative parts A and B, each its own card(s).

Seven parts are answered in the scheme by a drawing and no words. Each is a
card whose marking point is the part's own ask and whose answer is the
scheme's drawing, cropped and held back until the reveal (see Cards.drawn).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, point, MAX_OPTIONS  # noqa: E402

P = Printed(2026, 'hl')
C = Cards(P)
FIG = 'chemistry-2026-HL-'
Q4_NOTE = ('The scheme: "Eight items to be answered. Six marks to be allocated to each item and '
           'one additional mark to be added to each of the first two items attempted."')

# ── Q1 Volumetric analysis: water of crystallisation in washing soda ─────────
C.menu([('1', 'a', 'i', None)], 'chem-4-1', 'transferring-a-solid-to-a-volumetric-flask')
C.fixed([('1', 'a', 'ii', None)], 'chem-4-1', 'hydrated-sodium-carbonate-not-a-primary-standard')
C.ordered([('1', 'b', 'i', None), ('1', 'b', 'ii', None)], 'chem-4-1',
          'rinsing-the-burette-and-end-point-precautions')
C.fixed([('1', 'c', 'i', None)], 'chem-4-1', 'indicator-for-a-carbonate-acid-titration')
C.fixed([('1', 'c', 'ii', None)], 'chem-4-1', 'indicator-colour-change-at-the-end-point')
C.fixed([('1', 'd', 'i', None)], 'chem-4-1', 'moles-of-acid-in-the-titre',
        fixes={'1000 × 28.35 = 0.002835 (moles of HCl per 28.35 cm³)':
               '0.10 ÷ 1000 × 28.35 = 0.002835 (moles of HCl per 28.35 cm³)'},
        row_notes={0: 'The scheme prints 0.10 over 1000 as a fraction; ÷ stands for its bar.'})
C.fixed([('1', 'd', 'ii', None)], 'chem-4-1', 'moles-of-sodium-carbonate-in-the-flask')
C.fixed([('1', 'd', 'iii', None)], 'chem-4-1', 'mass-of-sodium-carbonate-in-the-flask')
C.fixed([('1', 'd', 'iv', None)], 'chem-4-1', 'moles-of-water-of-crystallisation')
C.fixed([('1', 'd', 'v', None)], 'chem-4-1', 'value-of-x-in-washing-soda')

# ── Q2 Ethyne, soap, ethanoic acid ───────────────────────────────────────────
for roman, concept in [('i', 'reactants-for-preparing-ethyne'),
                       ('ii', 'collecting-ethyne-over-water'),
                       ('iii', 'obtaining-a-pure-sample-of-ethyne'),
                       ('iv', 'test-for-unsaturation-in-ethyne'),
                       ('v', 'unsaturation-test-colour-change')]:
    C.fixed([('2', 'a', roman, None)], 'chem-2-4', concept, figure=FIG + 'paper-q2a')
C.ordered([('2', 'b', r, None) for r in ('i', 'ii', 'iii', 'iv')], 'chem-4-2',
          'preparation-of-soap')
C.fixed([('2', 'c', 'i', None)], 'chem-4-2', 'salt-formed-by-ethanoic-acid-and-magnesium')
C.fixed([('2', 'c', 'ii', None)], 'chem-1-4', 'volume-of-hydrogen-from-ethanoic-acid',
        fixes={'0.75 60 = 0.0125 (moles CH₃COOH per 15 cm³)':
               '0.75 ÷ 60 = 0.0125 (moles CH₃COOH per 15 cm³)'},
        row_notes={2: 'The scheme prints 0.75 over 60 as a fraction; ÷ stands for its bar.'})

# ── Q3 Swimming pool water ───────────────────────────────────────────────────
C.ordered([('3', 'a', 'i', None)], 'chem-4-3', 'principle-of-colorimetry',
          row_notes={0: 'Printed in two columns: absorbance goes with directly proportional, '
                        'transmission with inversely proportional. A partial answer from one '
                        'side of // may not be taken with one from the other side.'})
C.fixed([('3', 'a', 'ii', None)], 'chem-4-3', 'why-chlorine-is-added-to-pool-water')
C.fixed([('3', 'a', 'iii', None)], 'chem-4-3', 'free-chlorine-species-in-pool-water')
C.fixed([('3', 'a', 'iv', None)], 'chem-4-3', 'reagents-to-test-for-free-chlorine')
C.ordered([('3', 'a', 'v', None)], 'chem-4-3', 'free-chlorine-test-colour-change',
          row_notes={1: 'Red / brown goes with potassium iodide and ethanoic acid; pink / red '
                        'with DPD.'})
C.ordered([('3', 'b', 'i', None)], 'chem-4-3', 'measuring-suspended-solids')
C.fixed([('3', 'b', 'ii', None)], 'chem-4-3', 'dissolved-solids-in-ppm',
        fixes={'1750 × 1250 = 1400 (p.p.m.)': '1400 (p.p.m.)'},
        row_notes={1: 'The scheme prints this step as 1750 × 1000 over 1250.'})
C.ordered([('3', 'c', 'i', None)], 'chem-4-3', 'brown-ring-test-for-nitrate')
C.fixed([('3', 'c', 'ii', None)], 'chem-4-3', 'silver-nitrate-test-for-chloride')

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
Q4 = [('a', 'chem-1-2', 'protons-and-electrons-in-an-ion', {}),
      ('b', 'chem-1-2', 'thomson-and-millikan', {}),
      ('d', 'chem-2-2', 'bond-angles-in-becl2-and-water', {}),
      ('e', 'chem-1-2', 'relative-atomic-mass-of-chlorine', {}),
      ('f', 'chem-3-4', 'conjugate-acid-and-base-of-hydrogenphosphate',
       {'fixes': {'(ii) PO43–': '(ii) PO₄³⁻'}}),
      ('g', 'chem-u2', 'principle-of-chromatography', {}),
      ('h', 'chem-4-3', 'water-treatment-chemicals', {}),
      ('i', 'chem-1-4', 'number-of-molecules-from-a-mass',
       {'fixes': {'126 = 1.349 × 10⁻⁵ (moles of C₆H₆O₃)':
                  '0.0017 ÷ 126 = 1.349 × 10⁻⁵ (moles of C₆H₆O₃)'},
        'row_notes': {1: 'The scheme prints 0.0017 over 126 as a fraction; ÷ stands for its bar.'},
        'figure': FIG + 'paper-q4i'}),
      ('j', 'chem-3-5', 'electrolysis-of-potassium-iodide', {})]
for letter, topic, concept, kw in Q4:
    C.fixed([('4', letter, None, None)], topic, concept, deep=True, notes=Q4_NOTE, **kw)
C.fixed([('4', 'l', None, 'A')], 'chem-4-3', 'nitrogen-fixation-by-lightning', notes=Q4_NOTE)
C.fixed([('4', 'l', None, 'B')], 'chem-2-1', 'examples-of-crystal-types', notes=Q4_NOTE)

# ── Q5 Ionisation energy and electronegativity ───────────────────────────────
C.ordered([('5', 'a', 'i', None)], 'chem-1-2', 'first-ionisation-energy')
C.menu([('5', 'a', 'ii', None)], 'chem-1-2', 'oxygen-and-sulfur-ionisation-energies')
C.fixed([('5', 'a', 'iii', None)], 'chem-1-2', 'boron-and-beryllium-ionisation-energies')
C.ordered([('5', 'a', 'iv', None)], 'chem-1-2', 'second-ionisation-energies-of-sodium-and-magnesium')
C.ordered([('5', 'b', 'i', None)], 'chem-2-1', 'electronegativity')
C.ordered([('5', 'b', 'ii', None)], 'chem-2-1', 'bonding-in-arsine-from-electronegativity')
C.ordered([('5', 'b', 'iv', None)], 'chem-2-2', 'polarity-of-arsine')
C.ordered([('5', 'c', None, None)], 'chem-3-5', 'reducing-agents-and-ionisation-energy')

# ── Q6 Fuels and heats of reaction ───────────────────────────────────────────
C.ordered([('6', 'a', r, None) for r in ('i', 'ii', 'iii')], 'chem-2-4', 'octane-number')
Q6B_STEM = P.ask(('6', None, None, None)) + ' ' + P.text(
    ('6', 'b', None, None), upto='octane number of a fuel.')
for roman, concept in [('i', 'product-of-reforming'), ('ii', 'product-of-cracking'),
                       ('iii', 'homologous-series-of-a-cracking-product')]:
    C.fixed([('6', 'b', roman, None)], 'chem-2-4', concept, figure=FIG + 'paper-q6b',
            stem=Q6B_STEM)
C.fixed([('6', 'c', 'i', None)], 'chem-3-1', 'heat-of-formation')

# Q6(c)(ii): three working lines, each priced "(2 [multiplicative factor] +1
# [sign])" at its right, then the answer [4]. The text layer reads the whole
# block as one item closed by [4]; the rows below are its printed rows.
_it = P.items(('6', 'c', 'ii', None))
assert len(_it) == 1 and _it[0].cell == '[4]', _it
_rows = []
for r in _it[0].rows:
    head, sep, price = r.text.partition(' (2 [multiplicative factor] +1 [sign])')
    if sep:
        _rows.append(point(f'r-{len(_rows) + 1}', head, 3,
                           'The scheme prices each line (2 [multiplicative factor] +1 [sign]).'))
    else:
        _rows.append(point(f'r-{len(_rows) + 1}', r.text.replace('∆H_(f)', '∆Hf'), 4,
                           'The scheme adds: ' + ' '.join(_it[0].asides)))
for r in _rows:
    if not P.traceable(r['verbatim']):
        raise Refused(f'Q6(c)(ii): "{r["verbatim"]}" is not in the scheme')
C.add([('6', 'c', 'ii', None)], 'chem-3-1', 'heat-of-formation-of-hydrogen-sulfide', _rows)

# ── Q7 Chemical equilibrium: steam reforming ─────────────────────────────────
C.ordered([('7', 'a', 'i', None), ('7', 'a', 'ii', None)], 'chem-3-3',
          'equilibrium-and-the-effect-of-a-catalyst')
C.fixed([('7', 'b', 'i', None)], 'chem-3-3', 'moles-of-methane-at-equilibrium')
C.fixed([('7', 'b', 'ii', None)], 'chem-3-3', 'moles-of-steam-at-equilibrium')
C.fixed([('7', 'b', 'iii', None)], 'chem-3-3', 'moles-of-hydrogen-at-equilibrium')
C.fixed([('7', 'b', 'iv', None)], 'chem-3-3', 'kc-expression-for-steam-reforming',
        fixes={'[CO][H₂]³ [CH₄][H₂O]': '[CO][H₂]³'},
        row_notes={0: 'Printed as a fraction with [CH₄][H₂O] beneath the bar; the scheme\'s '
                      'own print is shown with the answer.'},
        figure=FIG + 'scheme-q7b-iv')
C.fixed([('7', 'b', 'v', None)], 'chem-3-3', 'calculating-kc',
        fixes={'i.e. 4 = 0.2 (mol L⁻¹ of CH₄), 4 = 0.9 (mol L⁻¹ of H₂O), 4 = 1.7 (mol L⁻¹ CO), '
               '4 = 5.1 (mol L⁻¹ H₂) K_(c) = [0.2][0.9] = 1252.8 (mol²L⁻²)': '1252.8 (mol²L⁻²)'},
        row_notes={1: 'The scheme sets its working as fractions; its own print is shown with '
                      'the answer.'},
        figure=FIG + 'scheme-q7b-v')
C.ordered([('7', 'c', 'i', None)], 'chem-3-3', 'le-chateliers-principle')
C.ordered([('7', 'c', 'ii', None)], 'chem-3-3', 'effect-of-concentration-on-kc')
C.ordered([('7', 'c', 'iii', None)], 'chem-3-3', 'effect-of-temperature-on-kc')

# ── Q8 Reaction scheme from ethanol ──────────────────────────────────────────
Q8 = FIG + 'paper-q8'
C.fixed([('8', 'a', 'i', None)], 'chem-4-2', 'homologous-series-of-ethanol', figure=Q8)
C.fixed([('8', 'a', 'ii', None)], 'chem-4-2', 'dehydration-of-ethanol', figure=Q8)
C.fixed([('8', 'a', 'iii', None)], 'chem-4-2', 'features-of-an-elimination-reaction', figure=Q8)
C.fixed([('8', 'b', 'ii', None)], 'chem-4-2', 'addition-polymer-of-ethene', figure=Q8)
C.fixed([('8', 'b', 'iii', None)], 'chem-4-2', 'geometry-change-on-polymerisation', figure=Q8)
C.fixed([('8', 'b', 'iv', None)], 'chem-4-2', 'why-ethene-undergoes-addition', figure=Q8)
for roman, concept in [('i', 'initiating-free-radical-substitution'),
                       ('ii', 'initiation-is-endothermic'),
                       ('iii', 'propagation-steps-of-free-radical-substitution'),
                       ('iv', 'tetraethyl-lead-as-a-radical-source')]:
    C.fixed([('8', 'c', roman, None)], 'chem-4-2', concept, figure=Q8)

# ── Q9 Rates of reaction and catalysis ───────────────────────────────────────
Q9A_STEM = P.text(('9', 'a', None, None), upto='by a metal catalyst.')
for roman, concept in [('i', 'plotting-a-concentration-time-graph'),
                       ('ii', 'instantaneous-rate-from-a-tangent'),
                       ('iii', 'effect-of-temperature-on-rate'),
                       ('iv', 'effect-of-catalyst-surface-area')]:
    C.fixed([('9', 'a', roman, None)], 'chem-3-2', concept, figure=FIG + 'paper-q9a',
            stem=Q9A_STEM)
Q9B_STEM = (P.text(('9', 'a', None, None), upto='2O2(g)') + ' '
            + P.ask(('9', 'b', None, None)))
C.fixed([('9', 'b', 'i', None)], 'chem-3-2', 'catalytic-converter-metals', stem=Q9B_STEM)
C.ordered([('9', 'b', 'ii', None)], 'chem-3-2', 'reaction-in-a-catalytic-converter', stem=Q9B_STEM)
C.fixed([('9', 'b', 'iii', None)], 'chem-3-2', 'catalyst-poisons', stem=Q9B_STEM)
C.fixed([('9', 'b', 'iv', None)], 'chem-3-2', 'how-a-catalyst-poison-acts', stem=Q9B_STEM)
C.ordered([('9', 'c', r, None) for r in ('i', 'ii', 'iii')], 'chem-3-2',
          'heterogeneous-catalysis-with-platinum-wire', figure=FIG + 'paper-q9c')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([('10', 'a', 'i', None)], 'chem-1-2', 'line-emission-spectrum')
C.menu([('10', 'a', 'ii', None)], 'chem-1-2', 'flame-test-method')
C.fixed([('10', 'a', 'iii', None)], 'chem-1-2', 'instrument-for-viewing-spectra')
C.fixed([('10', 'a', 'iv', None)], 'chem-1-2', 'origin-of-line-emission-spectra')
C.fixed([('10', 'a', 'v', None)], 'chem-1-2', 'spectra-as-evidence-for-energy-levels')
C.fixed([('10', 'a', 'vi', None)], 'chem-1-2', 'why-element-spectra-differ')
C.ordered([('10', 'b', 'i', None), ('10', 'b', 'ii', None)], 'chem-2-3',
          'ideal-gases-and-real-gas-behaviour')
C.fixed([('10', 'b', 'iii', None)], 'chem-2-3', 'volume-from-the-ideal-gas-equation')
C.fixed([('10', 'b', 'iv', None)], 'chem-2-3', 'why-ammonia-is-not-ideal')
C.fixed([('10', 'c', 'i', None)], 'chem-1-4', 'moles-of-phenylmethanol',
        fixes={'2.808 108 = 0.026 (moles of C₆H₅CH₂OH)': '2.808 ÷ 108 = 0.026 (moles of C₆H₅CH₂OH)'},
        row_notes={2: 'The scheme prints 2.808 over 108 as a fraction; ÷ stands for its bar.'})
C.fixed([('10', 'c', 'ii', None)], 'chem-1-4', 'showing-a-reagent-is-in-excess',
        fixes={'158 = 0.040 (moles of KMnO₄) present': '6.32 ÷ 158 = 0.040 (moles of KMnO₄) present',
               '0.026 × 3 = 0.0347 (moles of KMnO₄) required': '0.0347 (moles of KMnO₄) required'},
        row_notes={1: 'The scheme prints 6.32 over 158 as a fraction; ÷ stands for its bar.',
                   2: 'The scheme prints this step as 0.026 × 4 over 3.'})
C.fixed([('10', 'c', 'iii', None)], 'chem-1-4', 'mass-of-unreacted-reagent')
C.fixed([('10', 'c', 'iv', None)], 'chem-1-4', 'theoretical-yield-of-benzoic-acid')
C.fixed([('10', 'c', 'v', None)], 'chem-1-4', 'percentage-yield-of-benzoic-acid',
        fixes={'1.97 g 3.17 g / 0.01615 moles 0.026 moles':
               '1.97 g ÷ 3.17 g / 0.01615 moles ÷ 0.026 moles'},
        row_notes={1: 'The scheme prints each ratio as a fraction; ÷ stands for its bar.'})

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
Q11A = FIG + 'paper-q11a'
C.ordered([('11', 'a', r, None) for r in ('i', 'ii', 'iii')], 'chem-4-2',
          'oxidation-of-a-secondary-alcohol', figure=Q11A)
C.fixed([('11', 'a', 'vi', None)], 'chem-4-2', 'propanal-from-propan-1-ol', figure=Q11A)
C.fixed([('11', 'b', 'i', None)], 'chem-3-5', 'oxidation-as-electron-loss')
C.fixed([('11', 'b', 'ii', None)], 'chem-3-5', 'oxidation-number-of-manganese')
C.fixed([('11', 'b', 'iii', None)], 'chem-3-5', 'oxidation-numbers-of-carbon')
C.fixed([('11', 'b', 'iv', None)], 'chem-3-5', 'balancing-a-redox-equation')
C.ordered([('11', 'b', 'v', None)], 'chem-3-5', 'identifying-the-reducing-agent',
          fixes={'C2O42–': 'C₂O₄²⁻'},
          stem=P.ask(('11', 'b', 'iv', None)).split('equation: ', 1)[1])
Q11C = FIG + 'paper-q11c'
for roman, concept in [('i', 'bronsted-lowry-acid'), ('ii', 'ethanoic-acid-as-a-bronsted-lowry-acid'),
                       ('iii', 'ka-of-ethanoic-acid'), ('iv', 'ph-of-diluted-hydrochloric-acid'),
                       ('v', 'strong-and-weak-acid-ph')]:
    C.fixed([('11', 'c', roman, None)], 'chem-3-4', concept, figure=Q11C,
            stem=C.context(('11', 'c', roman, None), heads=False),
            fixes={'pH = –log₁₀[H₃O⁺] / [H⁺] = √KaMacid / [H⁺] = 10^-2.8':
                   'pH = –log₁₀[H₃O⁺] / [H⁺] = √(KaMacid) / [H⁺] = 10^-2.8'},
            row_notes={0: 'The scheme sets Ka and Macid together under one root sign.'}
            if roman == 'iii' else None)
for roman, concept, how in [('i', 'greenhouse-gas', 'fixed'),
                            ('ii', 'human-sources-of-carbon-dioxide', 'menu'),
                            ('iii', 'acidic-oxide', 'fixed'),
                            ('iv', 'showing-carbon-dioxide-is-an-acidic-oxide', 'fixed'),
                            ('v', 'scrubbing-acidic-oxides', 'fixed'),
                            ('vi', 'species-formed-when-carbon-dioxide-dissolves', 'menu3')]:
    key = [('11', 'd', roman, 'A')]
    if how == 'fixed':
        C.fixed(key, 'chem-4-3', concept)
    else:
        C.menu(key, 'chem-4-3', concept, claim=3 if how == 'menu3' else None)
for roman, concept in [('i', 'ore-of-aluminium'), ('ii', 'why-alumina-must-be-molten'),
                       ('iii', 'anode-material-for-aluminium-extraction'),
                       ('iv', 'reaction-at-the-anode'),
                       ('v', 'cathode-material-for-aluminium-extraction'),
                       ('vi', 'reaction-at-the-cathode')]:
    C.fixed([('11', 'd', roman, 'B')], 'chem-3-5', concept, figure=FIG + 'paper-q11d-b')

# ── drawn answers ─────────────────────────────────────────────────────────────
# Seven parts the scheme answers with a drawing and no words. Each is carded
# with the paper's own ask as its marking point and the scheme's drawing,
# cropped by chem_print_figures.py, as a solution figure held back until the
# reveal (Cards.drawn).
S = FIG + 'scheme-'
C.drawn([('4', 'c', None, None)], 'chem-1-2', 'beta-decay-of-carbon-14', S + 'q4c', notes=Q4_NOTE)
C.drawn([('4', 'k', None, None)], 'chem-4-2', 'ester-from-methanol-and-ethanoic-acid', S + 'q4k',
        notes=Q4_NOTE)
C.drawn([('5', 'b', 'iii', None)], 'chem-2-1', 'dot-and-cross-diagram-of-arsine', S + 'q5b-iii')
C.drawn([('6', 'b', 'iv', None)], 'chem-2-4', 'isomers-of-pentane', S + 'q6b-iv', stem=Q6B_STEM)
C.drawn([('8', 'b', 'i', None)], 'chem-4-2', 'repeating-units-of-polyethene', S + 'q8b-i')
C.drawn([('11', 'a', 'iv', None)], 'chem-4-2', 'bonds-broken-in-propan-2-ol', S + 'q11a-iv')
C.drawn([('11', 'a', 'v', None)], 'chem-4-2', 'bonds-formed-in-propanone', S + 'q11a-v')


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
