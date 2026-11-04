#!/usr/bin/env python3
"""2026 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2026_ol.py          # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2026_ol.py --review # the review ledger

Built the way chem_2026_hl.py is: every question text, stem and lead-in is the
PAPER's print of its part, every marking point the SCHEME's, and this file
adds only judgement -- card boundaries, topics, concept slugs, figures, and
the one traceable form of a line the text layer cannot carry.

The Ordinary scheme prices most letters with ONE cell for all their parts
("[12+3+2+2+2]" closes Q1(a)(i)-(v)), so most cards here span a whole letter
and carry no per-point value (orderedSplit). Where a letter's cell spans a
part answered by a drawing (Q1(c)(ii), Q5(a)(iv), Q6(d)(ii)), that part's row
is its own ask and the scheme's drawing is the card's solution figure.

Where the scheme prints only an instruction to the examiner for a point ("any
correct example", "Fraction // Fraction") the point is not a row -- the bank's
content-free rule (contentFree.mjs) refuses it -- and the card's notes quote
the criterion instead.

Q8(a)(iii) and (iv) are drawings of compound Z, which only the paper's
reaction series names: their question picture is the paper's own print (its
opening line and the series, then the one ask) and the scheme's drawing is
the answer. Q3(c)(iv), which the SEC voided for a misprint, is carded with
the scheme's own note awarding its marks; the four Q11(d)A parts whose only
scheme text is a criterion ("formula", "location", "explanation") are carded
with that criterion as the row. Nothing is excluded.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, point, MAX_OPTIONS  # noqa: E402

P = Printed(2026, 'ol')
C = Cards(P)
FIG = 'chemistry-2026-OL-'
Q4_NOTE = ('The scheme: "Eight items to be answered. Six marks to be allocated to each item and '
           'one additional mark to be added to each of the first two items attempted."')
FRACTION = 'The scheme prints {} as a fraction; ÷ stands for its bar.'


def k(*parts):
    """A part key: k('1', 'a', 'i') -> ('1', 'a', 'i', None); k('4', 'l', alt='A')."""
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


# ── Q1 Preparing ethene ──────────────────────────────────────────────────────
C.ordered([k('1', 'a', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-2-4',
          'preparing-and-collecting-ethene', figure=FIG + 'paper-q1',
          criteria=('one appropriate safety or procedural precaution',))
C.ordered([k('1', 'b', r) for r in ('i', 'ii', 'iii')], 'chem-2-4',
          'unsaturation-and-the-test-for-it', figure=FIG + 'paper-q1',
          row_notes={2: 'Printed in two columns: yellow / orange / brown goes with bromine (water), '
                        'purple / pink with (acidified) potassium permanganate.'})
C.ordered([k('1', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-2-4', 'ethene-structure-and-use',
          drawn={k('1', 'c', 'ii')}, figure=FIG + 'scheme-q1c-ii', stem='')

# ── Q2 Titration of sodium hydroxide ─────────────────────────────────────────
Q2_LEAD = P.lead(k('2', 'b', 'ii'))
Q2_LEAD = Q2_LEAD[Q2_LEAD.index('The titration reaction'):Q2_LEAD.index('table below.') + 12]
Q2_STEM = P.ask(k('2')) + ' ' + Q2_LEAD
C.ordered([k('2', 'a', r) for r in ('i', 'ii', 'iii')], 'chem-4-1', 'titration-apparatus',
          figure=FIG + 'paper-q2', label_key=[
              {'letter': 'A', 'meaning': 'burette', 'askedInThisQuestion': True}])
# The scheme sets the paper's equation below (b) in bold, beside its answers.
C.ordered([k('2', 'b', r) for r in ('i', 'ii')], 'chem-4-1', 'indicators-for-acid-base-titration',
          drop=('HCl + NaOH → NaCl + H₂O',),
          row_notes={1: 'Printed in two columns: yellow / orange to pink / red for methyl orange, '
                        'pink to colourless for phenolphthalein.'},
          figure=FIG + 'paper-q2')
C.fixed([k('2', 'c', 'i')], 'chem-4-1', 'average-titre', stem=Q2_STEM, figure=FIG + 'paper-q2c',
        fixes={'26.5+26.6=53.1': '26.5 + 26.6 = 53.1', '53.1 ÷ 2 =26.55 (cm³)': '53.1 ÷ 2 = 26.55 (cm³)'})
C.fixed([k('2', 'c', 'ii')], 'chem-4-1', 'concentration-in-moles-per-litre', stem=Q2_STEM,
        figure=FIG + 'scheme-q2c-ii',
        fixes={'n1 = n2 // 1000 × v': 'M1V1 ÷ n1 = M2V2 ÷ n2 // M ÷ 1000 × v',
               '// 1000×26.55=5.31 ×10^−3': '(0.2)(26.55) ÷ 1 // 0.2 ÷ 1000 × 26.55 = 5.31 × 10⁻³',
               '// ×1000': '(M)(25)'},
        row_notes={0: 'Two routes, printed side by side and separated by //; each line is a '
                      'fraction, ÷ standing for its bar.',
                   2: 'The scheme prints this line as (M)(25) over 1 // 5.31 × 10⁻³ over 25, '
                      '× 1000; its own print is shown with the answer.'})
# Its only figure is the scheme's working, held back until the reveal, while its stem points at the
# burette "shown on the right" and at "the table below", whose titres the concentration is worked
# from (the table is a picture on this card's sibling (c)(i), so its numbers are not in the stem).
# The paper's own print is the question: the opening paragraph with the burette beside it ((a) and
# (b), printed beside the burette, whited out), the equation and the table, then (c)(ii).
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q2c-ii-print'
C.fixed([k('2', 'c', 'iii')], 'chem-4-1', 'concentration-in-grams-per-litre', stem=Q2_STEM,
        figure=FIG + 'paper-q2',
        fixes={'0.21 ×40=8.4 −8.5 (g)': '0.21 × 40 = 8.4 − 8.5 (g)'})
C.ordered([k('2', 'd')], 'chem-4-1', 'obtaining-a-pure-dry-salt', stem=P.ask(k('2')),
          figure=FIG + 'paper-q2')

# ── Q3 Rate of decomposition of hydrogen peroxide ────────────────────────────
C.ordered([k('3', 'a')], 'chem-3-2', 'rate-of-reaction')
Q3B = P.text(k('3', 'b'))
C.fixed([k('3', 'b', 'i')], 'chem-3-2', 'what-a-catalyst-is', stem=Q3B)
C.fixed([k('3', 'b', 'ii')], 'chem-3-2', 'catalyst-for-hydrogen-peroxide', stem=Q3B)
C.menu([k('3', 'b', 'iii')], 'chem-3-2', 'apparatus-for-measuring-oxygen-produced', stem=Q3B)
Q3C = Q3B + ' ' + P.lead(k('3', 'b', 'iii'))[:P.lead(k('3', 'b', 'iii')).index('table below.') + 12]
C.fixed([k('3', 'c', 'i')], 'chem-3-2', 'plotting-volume-against-time', stem=Q3C,
        figure=FIG + 'paper-q3',
        row_notes={3: 'The scheme adds: [max 12 marks if not on graph paper]'})
C.fixed([k('3', 'c', 'ii')], 'chem-3-2', 'reading-a-time-from-the-graph', stem=Q3C,
        figure=FIG + 'paper-q3')
C.fixed([k('3', 'c', 'iii')], 'chem-3-2', 'average-rate-of-reaction', stem=Q3C,
        figure=FIG + 'paper-q3')
# Q3(c)(iv): the SEC voided the part. The scheme prints its cell [4] with no
# answer and, beneath it, its own note awarding the 4 marks to everyone who
# attempted Question 3; that note is the part's one row.
_q3civ = P.items(k('3', 'c', 'iv'))
assert [it.cell for it in _q3civ] == ['[4]', None] and not _q3civ[0].text, _q3civ
C.add([k('3', 'c', 'iv')], 'chem-3-2', 'effect-of-concentration-on-initial-rate', [
    C.lifted('r-1', _q3civ[1].text, 4,
             'The scheme prints no answer for this part: because of a typographical error in '
             'it, the SEC awarded the full 4 marks to every candidate who attempted Question 3.')],
      stem=Q3C, figure=FIG + 'paper-q3')

# ── Q4 Eight of twelve short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-2', 'discovery-of-the-nucleus', notes=Q4_NOTE)
C.ordered([k('4', 'b')], 'chem-3-1', 'exothermic-combustion', notes=Q4_NOTE)
C.ordered([k('4', 'c')], 'chem-u2', 'what-chromatography-is', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-4-3', 'why-fluoride-is-added-to-water', notes=Q4_NOTE)
C.ordered([k('4', 'e')], 'chem-1-2', 'protons-and-electrons-in-an-ion', deep=True, notes=Q4_NOTE)
C.ordered([k('4', 'f')], 'chem-1-2', 'why-relative-atomic-masses-are-not-whole-numbers',
          notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-1-3', 'formula-of-hydrogen-sulfide', notes=Q4_NOTE)
C.ordered([k('4', 'h')], 'chem-u2', 'steam-distillation', notes=Q4_NOTE)
C.fixed([k('4', 'i')], 'chem-1-4', 'percentage-by-mass-of-aluminium', notes=Q4_NOTE,
        fixes={'102': '54 ÷ 102', '×100 ≈53 %': '× 100 ≈ 53 %'},
        row_notes={1: FRACTION.format('54 over 102')})
C.drawn([k('4', 'j')], 'chem-2-4', 'structure-of-benzene', FIG + 'scheme-q4j', notes=Q4_NOTE)
C.ordered([k('4', 'k')], 'chem-1-3', 'alkali-metals', notes=Q4_NOTE, qtext=P.text(k('4', 'k')))
C.ordered([ka('4', 'l', None, 'A')], 'chem-u3', 'batch-and-continuous-processes', notes=Q4_NOTE)
C.ordered([ka('4', 'l', None, 'B')], 'chem-1-3', 'metals-and-non-metals', notes=Q4_NOTE)

# ── Q5 Electronegativity and bonding ─────────────────────────────────────────
C.ordered([k('5', 'a', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-2-1',
          'electronegativity-and-bonding-in-boron-trichloride', figure=FIG + 'scheme-q5a-iv',
          row_notes={6: 'The scheme prints a dot and cross diagram of BCl₃ beneath these two '
                        'points; it is shown with the answer.'})
C.ordered([k('5', 'b', r) for r in ('i', 'ii')], 'chem-1-3', 'electronegativity-trends')
C.ordered([k('5', 'c', r) for r in ('i', 'ii')], 'chem-2-1', 'ionic-bonding',
          criteria=('any correct ionic compound',))

# ── Q6 Hydrocarbons A to E ───────────────────────────────────────────────────
Q6_STEM = P.text(k('6'), upto='in the table below.')
C.ordered([k('6', 'a', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-2-4',
          'naming-hydrocarbons-and-lpg', stem=Q6_STEM, figure=FIG + 'paper-q6')
C.ordered([k('6', 'b', r) for r in ('i', 'ii')], 'chem-2-4', 'homologous-series',
          stem=Q6_STEM, figure=FIG + 'paper-q6')
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'combustion-of-ethyne', stem='',
        qtext=P.text(k('6', 'c', 'i')), figure=FIG + 'scheme-q6c-i',
        fixes={'2O₂ → 2CO₂ + H₂O': '2½O₂ → 2CO₂ + H₂O'},
        row_notes={0: 'The scheme completes C₂H₂ + 2½O₂ → 2CO₂ + H₂O, the ½ set as a small '
                      'fraction; its own print is shown with the answer.'})
C.fixed([k('6', 'c', 'ii')], 'chem-2-4', 'appearance-of-an-ethyne-flame', stem=Q6_STEM,
        figure=FIG + 'paper-q6')
C.ordered([k('6', 'd', r) for r in ('i', 'ii', 'iii')], 'chem-2-4', 'isomers-of-butane',
          drawn={k('6', 'd', 'ii')}, figure=FIG + 'scheme-q6d-ii', stem='')

# ── Q7 Water hardness and pH ─────────────────────────────────────────────────
C.ordered([k('7', 'a', r) for r in ('i', 'ii')], 'chem-4-3', 'testing-river-water')
C.ordered([k('7', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-4-3', 'hardness-in-water')
C.ordered([k('7', 'c', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-3-4', 'acids-and-ph')

# ── Q8 Reaction series W, X, Y, Z ────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
C.fixed([k('8', 'a', 'i')], 'chem-4-2', 'naming-compound-y', figure=Q8)
C.fixed([k('8', 'a', 'ii')], 'chem-4-2', 'naming-compound-z', figure=Q8)
# (iii) and (iv) are answered with a drawing of Z, and Z is named only in the
# paper's reaction series. The question picture is the paper's own print --
# its opening line and the series, then the one ask -- and the scheme's
# drawing is the answer, held back until the reveal.
for roman, concept in [('iii', 'structure-of-ethanal'), ('iv', 'carbonyl-group-of-ethanal')]:
    C.drawn([k('8', 'a', roman)], 'chem-4-2', concept, FIG + f'scheme-q8a-{roman}')
    C.cards[-1]['questionFigureKey'] = FIG + f'paper-q8a-{roman}'
C.fixed([k('8', 'a', 'v')], 'chem-2-2', 'tetrahedral-carbons-in-ethanal', figure=Q8)
for roman, concept in [('i', 'classifying-the-conversion-of-x-to-w'),
                       ('ii', 'classifying-the-conversion-of-y-to-x'),
                       ('iii', 'classifying-the-conversion-of-y-to-z')]:
    C.fixed([k('8', 'b', roman)], 'chem-4-2', concept, figure=Q8)
C.fixed([k('8', 'c', 'i')], 'chem-4-2', 'oxidising-ethanol-to-ethanal', figure=Q8)
C.fixed([k('8', 'c', 'ii')], 'chem-2-2', 'why-ethanol-is-soluble-in-water', figure=Q8)
C.fixed([k('8', 'd', 'i')], 'chem-4-2', 'which-compound-polymerises', figure=Q8)
C.fixed([k('8', 'd', 'ii')], 'chem-4-2', 'halogenation-of-ethane', figure=Q8)

# ── Q9 Equilibrium, diffusion and the gas laws ───────────────────────────────
C.fixed([k('9', 'a', 'i')], 'chem-3-3', 'chemical-equilibrium')
C.fixed([k('9', 'a', 'ii')], 'chem-3-3', 'kc-expression-for-the-contact-process',
        figure=FIG + 'scheme-q9a-ii', fixes={'[SO₃]² [SO₂]²[O₂]': '[SO₃]²'},
        row_notes={0: "Printed as a fraction with [SO₂]²[O₂] beneath the bar; the scheme's own "
                      'print is shown with the answer.'})
for roman, concept in [('iii', 'effect-of-pressure-on-the-contact-process'),
                       ('iv', 'effect-of-temperature-on-the-contact-process'),
                       ('v', 'effect-of-a-catalyst-on-equilibrium')]:
    C.fixed([k('9', 'a', roman)], 'chem-3-3', concept)
C.fixed([k('9', 'b', 'i')], 'chem-1-1', 'diffusion')
C.fixed([k('9', 'b', 'ii')], 'chem-1-1', 'particle-speed-in-states-of-matter')
Q9C_STEM = P.text(k('9', 'c'), upto='combined gas law:')
C.fixed([k('9', 'c', 'i')], 'chem-2-3', 'charles-law', stem=Q9C_STEM, figure=FIG + 'paper-q9c')
# Q9(c)(ii): the scheme sets its first two lines wholly as fractions, which the
# text layer reads as loose digits under the cells. Their traceable forms:
C.add([k('9', 'c', 'ii')], 'chem-2-3', 'volume-from-the-combined-gas-law', [
    C.lifted('r-1', '(2 × 10⁵)(6.1) ÷ 298', 3, FRACTION.format('(2 × 10⁵)(6.1) over 298')),
    C.lifted('r-2', '(1 × 10⁵)(V₂) ÷ 273', 3, FRACTION.format('(1 × 10⁵)(V₂) over 273')),
    C.lifted('r-3', 'V₂ ≈ 11.2 L', 3)], stem=Q9C_STEM, figure=FIG + 'paper-q9c')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.ordered([k('10', 'a', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-3-5',
          'oxidation-and-reduction')
C.ordered([k('10', 'b', r) for r in ('i', 'ii', 'iii', 'iv', 'v', 'vi')], 'chem-1-2',
          'radioactivity', figure=FIG + 'paper-q10b', criteria=('any correct example',))
C.fixed([k('10', 'c', 'i')], 'chem-1-4', 'moles-of-magnesium', fixes={'24': '3.6 ÷ 24'},
        row_notes={0: FRACTION.format('3.6 over 24')})
for roman, concept in [('ii', 'moles-of-hydrochloric-acid-reacting'),
                       ('iii', 'molecules-of-hydrochloric-acid'),
                       ('iv', 'mass-of-magnesium-chloride'),
                       ('v', 'volume-of-hydrogen-at-stp')]:
    C.fixed([k('10', 'c', roman)], 'chem-1-4', concept)

# ── Q11 Any two of (a), (b), (c), (d) ────────────────────────────────────────
C.ordered([k('11', 'a', r) for r in ('i', 'ii', 'iii', 'iv', 'v')], 'chem-1-2', 'flame-tests',
          criteria=('any two relevant safety precautions',))
C.ordered([k('11', 'b', r) for r in ('i', 'ii', 'iii', 'iv')], 'chem-2-4',
          'octane-number-and-oil-fractions',
          criteria=('Fraction // Fraction', 'Corresponding use // Corresponding use'))
C.ordered([k('11', 'c')], 'chem-4-3', 'stages-of-sewage-treatment', stem='')
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q11c'
# Q11(d)A: the candidate chooses the industry, so for four of its five parts
# the scheme prints only what the examiner looks for -- "formula",
# "location", "explanation" -- and that criterion is the row, as printed.
CHOSEN = ('The scheme prints only the criterion "{}" for this part: the answer depends on '
          'which of the three industries the candidate chose.')
for roman, concept, crit in [('i', 'formula-of-a-product-of-a-chosen-industry', 'formula'),
                             ('ii', 'location-of-a-chosen-industry', 'location')]:
    C.fixed([ka('11', 'd', roman, 'A')], 'chem-u3', concept,
            row_notes={0: CHOSEN.format(crit)})
C.fixed([ka('11', 'd', 'iii', 'A')], 'chem-u3', 'reasons-for-an-industrys-location')
for roman, concept in [('iv', 'managing-waste-effluent-in-a-chosen-industry'),
                       ('v', 'promoting-safety-in-a-chosen-industry')]:
    C.fixed([ka('11', 'd', roman, 'A')], 'chem-u3', concept,
            row_notes={0: CHOSEN.format('explanation')})
for roman, concept in [('i', 'properties-of-pvc'), ('ii', 'monomer'), ('iii', 'polymer'),
                       ('iv', 'another-addition-polymer'), ('v', 'importance-of-recycling-plastics')]:
    C.fixed([ka('11', 'd', roman, 'B')], 'chem-4-2', concept)
C.priced_menu([ka('11', 'd', 'vi', 'B')], 'chem-4-2', 'stages-in-recycling-plastics', 2,
              ['sorting', 'shredding', 'washing', 'drying', 're-extrusion'],
              note='The scheme lists the five stages in one line and prices any two together '
                   '[6], without a value for each.')

# ── excluded ─────────────────────────────────────────────────────────────────
# None. The five parts once excluded here -- Q3(c)(iv), which the SEC voided,
# and Q11(d)A(i), (ii), (iv), (v), whose scheme text is a criterion -- are
# carded above with what the scheme prints. A part the scheme prints nothing
# to mark against would be written to
# scripts/markbank/authoring/exclusions/chemistry.json by --exclusions, the
# evidence lifted from the scheme's own lines for the part (P.sseg_of), so it
# cannot drift from what the SEC printed.
EXCLUDED = []


def exclusions():
    out = []
    for key, reason in EXCLUDED:
        sg = P.sseg_of(key)
        said = ' '.join(x.strip() for x in [it.text + (f' {it.cell}' if it.cell else '')
                                            for it in P.items(key)] if x.strip())
        out.append({'ref': C.ref([key]), 'reason': reason,
                    'evidence': f'{P.year} OL scheme p.{sg.answers[0].page if sg.answers else sg.text[0].page}: '
                                f'"{C.label(key)} {display_text(sg)}" — {said}'})
    return out


def display_text(sg):
    from chem_print import display, joined
    return display(joined(sg.text))


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for key, reason in EXCLUDED:
        out.append(f'EXCLUDED {C.ref([key])}: {reason}')
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
    if '--exclusions' in sys.argv:
        print(json.dumps(exclusions(), ensure_ascii=False, indent=1))
    elif '--review' in sys.argv:
        print(review())
    else:
        print(json.dumps(C.finish(), ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)
