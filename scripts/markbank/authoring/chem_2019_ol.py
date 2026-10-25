#!/usr/bin/env python3
"""2019 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2019_ol.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2019_ol.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2019_ol.py --exclusions # recorded exclusions (none)
    python3 scripts/markbank/authoring/chem_apply_print.py 2019 ol

No 2019 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The paper sets some romans inside one sentence -- Q6(e) "(i) the ethanol, (ii)
the Al2O3, (iii) the heat source", Q9(a) "Define (i) an acid, (ii) a base.",
Q11(a) "Define (i) atomic number, (ii) mass number." -- and the scheme prices
each with a cell of its own: those cards take the sentence as their question.
The paper underlines the term Q2(d)(ii) and Q10(b)(i) ask about and prints
Q10(a) and Q10(b)(iv) with numbered blanks, which no text layer carries: those
take the paper's own print as their question. The scheme labels the paper's
Q11(c)B(iv) "(v)" (PDF page 17); that card reads the scheme's "(v)". Q4(k)
and Q11(c) offer whole alternative parts A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, display, joined  # noqa: E402

P = Printed(2019, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2019-OL-'
S = FIG + 'scheme-'
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'
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
        raise Refused(f'"{text}" is not in the 2019 ol scheme')
    return text


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Preparing ethyne ──────────────────────────────────────────────────────
Q1 = FIG + 'paper-q1'
_q1a = [P.items(k('1', 'a', r)) for r in ('i', 'ii', 'iii')]
assert [[it.cell for it in x] for x in _q1a] == [[None], [None], ['[5 + 3 + 3]']], _q1a
_meaning = [display(x[0].text.split(' [')[0]) for x in _q1a]      # the scheme's answer, its asides apart
# (i)'s two asides print hard against each other on a row of their own, which
# the reader takes for a point: they ride on (i)'s answer, quoted.
_q1a_asides = traced('[Allow separating funnel.][Burette or funnel unacceptable.]')
C.ordered([k('1', 'a', r) for r in ('i', 'ii', 'iii')], 'chem-u2',
          'apparatus-and-reagents-for-preparing-ethyne', figure=Q1, drop=(_q1a_asides,),
          row_notes={0: 'The scheme adds: ' + _q1a_asides}, label_key=[
              {'letter': 'X', 'meaning': _meaning[0], 'askedInThisQuestion': True},
              {'letter': 'A', 'meaning': _meaning[1], 'askedInThisQuestion': True},
              {'letter': 'B', 'meaning': _meaning[2], 'askedInThisQuestion': True}])
C.fixed([k('1', 'b', 'i')], 'chem-u2', 'observations-when-liquid-a-meets-solid-b', figure=Q1)
C.fixed([k('1', 'b', 'ii')], 'chem-u2', 'why-the-first-test-tubes-are-not-tested', figure=Q1)
C.fixed([k('1', 'c', 'i')], 'chem-2-4', 'bromine-test-on-ethyne', figure=Q1)
C.fixed([k('1', 'c', 'ii')], 'chem-2-4', 'unsaturation-of-ethyne', figure=Q1)
C.fixed([k('1', 'c', 'iii')], 'chem-2-4', 'another-compound-that-reacts-with-bromine', figure=Q1)
C.fixed([k('1', 'd')], 'chem-2-4', 'flame-of-burning-ethyne', figure=Q1)
C.fixed([k('1', 'e')], 'chem-2-4', 'a-use-of-ethyne', figure=Q1)

# ── Q2 A standard solution and a titration ───────────────────────────────────
Q2 = FIG + 'paper-q2'
C.fixed([k('2', 'a')], 'chem-4-1', 'why-a-conical-flask-not-a-beaker', figure=Q2)
C.fixed([k('2', 'b', 'i')], 'chem-4-1', 'rinsing-the-pipette', figure=Q2)
C.fixed([k('2', 'b', 'ii')], 'chem-4-1', 'rinsing-the-conical-flask', figure=Q2)
C.fixed([k('2', 'c')], 'chem-4-1', 'reading-a-burette-accurately', figure=Q2)
C.fixed([k('2', 'd', 'i')], 'chem-4-1', 'properties-of-a-primary-standard')
C.fixed([k('2', 'd', 'ii')], 'chem-4-1', 'definition-of-a-standard-solution')
print_question('paper-q2d-ii-print')
C.fixed([k('2', 'e', 'i')], 'chem-4-1', 'indicator-for-a-carbonate-titration')
C.fixed([k('2', 'e', 'ii')], 'chem-4-1', 'colour-change-of-methyl-orange-at-end-point')
C.answer_only([k('2', 'f')], 'chem-4-1', 'concentration-of-hydrochloric-acid', S + 'q2f')

# ── Q3 Dissolved solids in Dead Sea water ────────────────────────────────────
Q3 = FIG + 'paper-q3'
C.fixed([k('3', 'a')], 'chem-u2', 'why-filter-the-lake-water', figure=Q3)
C.fixed([k('3', 'b')], 'chem-u2', 'measuring-200-cm3-accurately', figure=Q3)
C.ordered([k('3', 'c', 'i'), k('3', 'c', 'ii')], 'chem-u2', 'heating-a-sample-to-dryness-safely',
          figure=Q3)
# (d)(i): three methods set out as a table, three steps each, priced (3 × 3);
# the text layer reads the table across its columns, so the rows are lifted
# cell by cell and the scheme's own print of the table is the answer picture.
_q3d = P.items(k('3', 'd', 'i'))
assert [it.cell for it in _q3d] == ['[3 × 3]', '[3]', '[3]', '[3]', None], _q3d
_m1 = ['clean a platinum (nichrome) wire* (rod, probe) in concentrated hydrochloric acid (HCl) / '
       'clean platinum wire', 'dip rod in salt',
       'hold salt in (over) hot (blue) part of flame (Bunsen) / observe colour of flame']
_m2 = ['soak wood (splint, stick) overnight in water / use damp (wet) wood (splint, stick)',
       'dip splint (stick) in salt',
       'hold salt in (over) hot (blue) part of flame (Bunsen) / observe colour of flame']
_m3 = ['prepare a solution of the salt in water and ethanol (propanol)', 'spray solution',
       'onto (into) hot (blue) part of flame (Bunsen) / observe colour of flame']
_q3d_asides = ['*[Allow ‘inoculating loop’, or ‘spatula’ for ‘platinum wire’.]',
               '[Clear labelled diagram for some or all points acceptable.]']
for t in _m2 + _m3 + _q3d_asides:
    traced(t)
C.add([k('3', 'd', 'i')], 'chem-u2', 'flame-test-procedure', [
    C.lifted(f'r-{i + 1}', _m1[i], 3,
             f'Method 1. Or Method 2, "{_m2[i]}", or Method 3, "{_m3[i]}".'
             + (' The scheme adds: ' + ' '.join(_q3d_asides) if i == 2 else ''))
    for i in range(3)],
    figure=S + 'q3d-i',
    notes='The scheme sets out three methods in a table, each in three steps priced (3) each, '
          '(3 × 3) in all; the rows here are Method 1, and its own print of all three is shown with '
          'the answer.')
print_question('paper-q3d-i-print')
C.fixed([k('3', 'd', 'ii')], 'chem-1-2', 'flame-colour-of-sodium', figure=Q3)
# The working is text; the card's picture is the stimulus, not a print of the routes.
C.route([k('3', 'e', 'i')], 'chem-1-4', 'mass-of-dissolved-solids')
C.cards[-1]['figureKey'] = Q3
C.route([k('3', 'e', 'ii')], 'chem-1-4', 'concentration-in-grams-per-litre')
C.cards[-1]['figureKey'] = Q3
C.fixed([k('3', 'f')], 'chem-u2', 'test-for-chloride-ion', figure=Q3)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-2', 'bohr-and-electron-orbits', notes=Q4_NOTE, figure=FIG + 'paper-q4a')
# (b): the aside "[Allow (3) for ... or (3) for Boyle's law.]" runs onto a
# second line whose "(3)" the reader takes for a cell; it is one aside.
_q4b = P.items(k('4', 'b'))
assert [it.cell for it in _q4b] == ['[6]', '[3]', None], _q4b
_q4b_aside = traced(_q4b[1].text + ' (3) ' + _q4b[2].text)
C.add([k('4', 'b')], 'chem-2-3', 'boyles-law', [
    C.lifted('r-1', display(_q4b[0].text), 6, 'The scheme adds: ' + _q4b_aside)], notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-1-2', 'composition-of-an-alpha-particle', notes=Q4_NOTE)
C.fixed([k('4', 'd', 'i')], 'chem-3-5', 'element-reduced-when-magnesium-burns', notes=Q4_NOTE)
C.fixed([k('4', 'd', 'ii')], 'chem-3-5', 'reduction-as-gain-of-electrons', notes=Q4_NOTE)
# (e): one equation, priced "FORMULAE: (3); BALANCING OF CORRECT FORMULAE: (3)".
_q4e = P.items(k('4', 'e'))
assert [it.cell for it in _q4e] == ['[3 + 3]'], _q4e
C.add([k('4', 'e')], 'chem-1-3', 'equation-for-sodium-and-water', [
    C.lifted('r-1', display(_q4e[0].text), 6,
             'The scheme prices the equation "' + traced('FORMULAE: (3); BALANCING OF CORRECT FORMULAE: (3)')
             + '".')], notes=Q4_NOTE)
C.fixed([k('4', 'f')], 'chem-3-2', 'enzymes-as-biological-catalysts', notes=Q4_NOTE)
_q4g = P.items(k('4', 'g'))
assert [it.cell for it in _q4g] == ['[6]', '[3]', '[3]'], _q4g
C.add([k('4', 'g')], 'chem-1-4', 'percentage-of-zinc-in-zinc-oxide', [
    C.lifted('r-1', display(_q4g[1].text), 3),
    C.lifted('r-2', '% Zn = 65 ÷ 81 × 100 = 80.2 %', 3, FRACTION.format('65', '81'))],
    notes='The scheme gives the answer, 80.2 %, priced (6), then the working that earns it, step by '
          'step. ' + Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-2-4', 'octane-number', notes=Q4_NOTE)
C.fixed([k('4', 'i')], 'chem-4-3', 'secondary-sewage-treatment', notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-4-3', 'hardness-removed-by-boiling', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'gases-that-make-rain-acidic', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-1-3', 'transition-metals-in-a-list', notes=Q4_NOTE)

# ── Q5 Elements, electronegativity and bonding ───────────────────────────────
C.fixed([k('5', 'a')], 'chem-1-1', 'definition-of-an-element')
C.drawn([k('5', 'b', 'i')], 'chem-1-2', 'electron-arrangement-of-hydrogen', S + 'q5b-i')
C.drawn([k('5', 'b', 'ii')], 'chem-1-2', 'electron-arrangement-of-oxygen', S + 'q5b-ii')
C.fixed([k('5', 'c', 'i')], 'chem-2-1', 'definition-of-electronegativity')
C.fixed([k('5', 'c', 'ii')], 'chem-2-1', 'electronegativities-of-hydrogen-and-oxygen')
C.fixed([k('5', 'c', 'iii')], 'chem-2-1', 'polar-covalent-bonding-in-water')
# (iv): the scheme draws the molecule two ways and prices two criteria in words.
assert cells(k('5', 'c', 'iv')) == ['[3]', '[3]', None], P.items(k('5', 'c', 'iv'))
C.fixed([k('5', 'c', 'iv')], 'chem-2-1', 'electron-arrangement-in-a-water-molecule', tail=True,
        figure=S + 'q5c-iv',
        row_notes={0: 'The scheme draws the molecule two ways; its own print is shown with the answer.'})
C.fixed([k('5', 'd', 'i')], 'chem-2-1', 'ionic-bonding-from-electronegativity')
C.fixed([k('5', 'd', 'ii')], 'chem-2-1', 'melting-point-of-an-ionic-compound')
C.fixed([k('5', 'd', 'iii')], 'chem-2-1', 'solubility-of-an-ionic-compound')
C.fixed([k('5', 'e')], 'chem-1-3', 'why-mendeleev-left-out-the-noble-gases')

# ── Q6 Hydrocarbons ──────────────────────────────────────────────────────────
Q6 = FIG + 'paper-q6'
C.fixed([k('6', 'a')], 'chem-2-4', 'alkanes', figure=Q6)
# (b): four names priced together "(3 × 4)".
assert cells(k('6', 'b')) == ['[3 × 4]'], P.items(k('6', 'b'))
C.ordered([k('6', 'b')], 'chem-2-4', 'iupac-names-of-four-hydrocarbons', figure=Q6)
C.ordered([k('6', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-2-4', 'liquefied-petroleum-gas',
          figure=FIG + 'paper-q6c')
C.ordered([k('6', 'd', 'i'), k('6', 'd', 'ii')], 'chem-2-4', 'methane-from-dumps-and-carcinogenic-benzene',
          figure=Q6)
# (e): the paper sets (i)-(iii) inside one sentence; the scheme prices each (3)
# and draws the apparatus with the three places labelled.
_q6e = P.ask(k('6', 'e'), deep=True)
_cut = _q6e.index('Indicate on your diagram')
for r, concept in (('i', 'where-the-ethanol-goes'), ('ii', 'where-the-aluminium-oxide-goes'),
                   ('iii', 'where-the-heat-is-applied')):
    assert cells(k('6', 'e', r)) == ['[3]'], P.items(k('6', 'e', r))
    C.fixed([k('6', 'e', r)], 'chem-u2', concept, qtext=_q6e[_cut:], stem=_q6e[:_cut].strip(),
            figure=S + 'q6e', cid=f'q6-e-{r}', row_notes={0: f'For ({r}).'})
    print_question('paper-q6e-print')

# ── Q7 Eggshell and hydrochloric acid ────────────────────────────────────────
Q7 = FIG + 'paper-q7'
Q7T = FIG + 'paper-q7-table'
C.fixed([k('7', 'a', 'i')], 'chem-3-2', 'graph-of-mass-of-co2-against-time', figure=S + 'q7a-i')
print_question('paper-q7a-i-print')
C.fixed([k('7', 'a', 'ii')], 'chem-3-2', 'mass-read-from-the-graph', figure=Q7T)
C.fixed([k('7', 'b')], 'chem-3-2', 'why-the-rate-falls', figure=Q7)
# (c)(i): "mortar // and pestle", priced (3 + 3): one each.
_q7c = P.items(k('7', 'c', 'i'))
assert [it.cell for it in _q7c] == ['[3 + 3]'] and len(_q7c[0].points()) == 2, _q7c
_pm = _q7c[0].points()
C.add([k('7', 'c', 'i')], 'chem-u2', 'crushing-eggshell', [
    C.lifted('r-1', _pm[0], 3, 'The scheme prices this point and the next (3 + 3), one each.'),
    C.lifted('r-2', _pm[1], 3, 'The scheme adds: ' + ' '.join(_q7c[0].asides))], figure=Q7)
C.fixed([k('7', 'c', 'ii')], 'chem-3-2', 'particle-size-and-rate', figure=Q7)
C.fixed([k('7', 'd')], 'chem-3-2', 'temperature-and-rate', figure=Q7)

# ── Q8 Methanol, methanal and methanoic acid ─────────────────────────────────
Q8 = FIG + 'paper-q8'
C.fixed([k('8', 'a')], 'chem-4-2', 'naming-methanol-methanal-and-methanoic-acid', figure=Q8)
C.ordered([k('8', 'b', r) for r in ('i', 'ii', 'iii')], 'chem-4-2', 'where-the-three-compounds-are-found',
          figure=Q8)
C.drawn([k('8', 'c')], 'chem-4-2', 'structure-of-methanal', S + 'q8c')
C.ordered([k('8', 'd', 'i'), k('8', 'd', 'ii')], 'chem-2-2', 'tetrahedral-and-planar-carbon', figure=Q8)
C.ordered([k('8', 'e', 'i'), k('8', 'e', 'ii')], 'chem-4-2', 'oxidising-methanol-to-methanoic-acid',
          figure=Q8)
# (f): the cue "COPY, / COMPLETE & / BALANCE:" leaves its first line on the
# equation's row.
C.fixed([k('8', 'f')], 'chem-3-1', 'combustion-of-methanol', figure=Q8,
        fixes={'CH₃OH + 1½O₂ → CO₂ + 2H₂O COPY,': 'CH₃OH + 1½O₂ → CO₂ + 2H₂O'})

# ── Q9 Acids, bases, pH and water treatment ──────────────────────────────────
_q9a = P.ask(k('9', 'a'))
for r, concept in (('i', 'definition-of-an-acid'), ('ii', 'definition-of-a-base')):
    assert cells(k('9', 'a', r)) == ['[6]'], P.items(k('9', 'a', r))
    C.fixed([k('9', 'a', r)], 'chem-3-4', concept, qtext=_q9a, stem='', cid=f'q9-a-{r}',
            row_notes={0: f'For ({r}).'})
C.fixed([k('9', 'b', 'i')], 'chem-3-4', 'definition-of-ph')
C.fixed([k('9', 'b', 'ii')], 'chem-3-4', 'ph-plus-poh')
C.fixed([k('9', 'b', 'iii')], 'chem-3-4', 'poh-of-neutral-water')
C.route([k('9', 'b', 'iv')], 'chem-3-4', 'ph-of-a-sodium-hydroxide-solution')
C.ordered([k('9', 'c', r) for r in ('i', 'ii', 'iii')], 'chem-4-3', 'stages-of-water-treatment')
C.fixed([k('9', 'c', 'iv')], 'chem-4-3', 'raising-the-ph-of-a-water-supply')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): seven words priced together, the cell labelled "FIRST SIX:".
assert cells(k('10', 'a')) == ['[7 + (6 × 3)]'], P.items(k('10', 'a'))
C.ordered([k('10', 'a')], 'chem-2-4', 'fractional-distillation-of-crude-oil',
          notes='The scheme sets the cell as "' + traced('FIRST SIX: (7 + (6 × 3))') + '".')
print_question('paper-q10a-print')
_q10b1 = P.items(k('10', 'b', 'i'))
assert [it.cell for it in _q10b1] == ['[4 + 3]', '[4 + 3]'], _q10b1
_pp = _q10b1[0].points()
assert len(_pp) == 2, _pp
C.add([k('10', 'b', 'i')], 'chem-3-3', 'definition-of-chemical-equilibrium', [
    C.lifted('r-1', _pp[0], None, 'The scheme prices this point and the next together (4 + 3), or '
             'instead, (4 + 3), the pair "' + _q10b1[1].text + '".'),
    C.lifted('r-2', _pp[1], None)],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'))
print_question('paper-q10b-i-print')
C.fixed([k('10', 'b', 'ii')], 'chem-3-1', 'exothermic-from-negative-delta-h')
C.drawn([k('10', 'b', 'iii')], 'chem-3-3', 'kc-expression-for-sulfur-trioxide', S + 'q10b-iii')
C.fixed([k('10', 'b', 'iv')], 'chem-3-3', 'le-chateliers-principle')
print_question('paper-q10b-iv-print')
# (c)(i): the answer (6) and the working that earns it, a fraction in a box (6).
_q10c1 = P.items(k('10', 'c', 'i'))
assert [it.cell for it in _q10c1] == ['[3]', '[6]', '[6]'], _q10c1
C.add([k('10', 'c', 'i')], 'chem-1-4', 'moles-of-silver', [
    C.lifted('r-1', _q10c1[0].text, 3),
    C.lifted('r-2', _q10c1[1].text, 6, 'The scheme sets out the working that earns it, n = m over Ar, '
             'priced (6); its own print is shown with the answer.')],
    figure=S + 'q10c-i')
_q10c2 = P.items(k('10', 'c', 'ii'))
assert [it.cell for it in _q10c2] == ['[3]'] * 5, _q10c2
C.add([k('10', 'c', 'ii')], 'chem-1-4', 'moles-and-volume-of-hydrogen', [
    C.lifted('r-1', _q10c2[0].text, 3),
    C.lifted('r-2', _q10c2[1].text, 3, 'Or its working, "' + display(_q10c2[2].text) + '" (3).'),
    C.lifted('r-3', _q10c2[3].text, 3, 'Or its working, "' + display(_q10c2[4].text) + '" (3).')])
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'mass-of-silver-sulfide')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): "Define (i) atomic number, (ii) mass number." is one sentence; the scheme
# prices (i) and (ii) (6) each. The nuclide prints as 25 over 12 before Mg,
# which the text layer reads "²⁵ 12Mg".
_q11a = P.ask(k('11', 'a'))
for r, concept in (('i', 'definition-of-atomic-number'), ('ii', 'definition-of-mass-number')):
    assert cells(k('11', 'a', r)) == ['[6]'], P.items(k('11', 'a', r))
    C.fixed([k('11', 'a', r)], 'chem-1-2', concept, qtext=_q11a, stem='', cid=f'q11-a-{r}',
            row_notes={0: f'For ({r}).'})
_mg = P.rearranged(P.lead(k('11', 'a')), '²⁵ 12Mg', '²⁵₁₂Mg')
_mg4 = P.rearranged(P.lead(k('11', 'a', 'iv')), '²⁵ 12Mg', '²⁵₁₂Mg')
C.fixed([k('11', 'a', 'iii')], 'chem-1-2', 'atomic-number-of-magnesium', stem=_mg)
C.fixed([k('11', 'a', 'iv')], 'chem-1-2', 'neutrons-in-magnesium-25', stem=_mg,
        qtext=P.rearranged(P.ask(k('11', 'a', 'iv')), '²⁵ 12Mg', '²⁵₁₂Mg'))
C.fixed([k('11', 'a', 'v')], 'chem-1-2', 'isotopes', stem=_mg + ' ' + _mg4)
C.fixed([k('11', 'a', 'vi')], 'chem-1-2', 'electrons-in-a-neutral-magnesium-atom', stem=_mg + ' ' + _mg4)
# (b): its own ask (6), then (i)-(iii) (9), then three asks the paper sets
# unnumbered after (iii), under one mark (10), which the scheme prices (3), (3)
# and (4): one card, cited as (b)'s, after (iii).
Q11B = FIG + 'paper-q11b'
_q11b = P.ask(k('11', 'b'))
_cut = _q11b.index('If the volume')
C.fixed([k('11', 'b')], 'chem-1-4', 'molecules-in-22-4-litres-of-gas', stem=_q11b[:_cut].strip(),
        qtext=_q11b[_cut:], figure=Q11B)
_q11b_lead = P.lead(k('11', 'b'))
C.fixed([k('11', 'b', 'i')], 'chem-2-4', 'main-constituent-of-natural-gas', stem=_q11b_lead)
C.fixed([k('11', 'b', 'ii')], 'chem-1-1', 'a-gas-of-diatomic-molecules', stem=_q11b_lead)
_q11b3 = P.items(k('11', 'b', 'iii'))
assert [it.cell for it in _q11b3] == ['[3]', '[3]', '[3]', '[4]'], _q11b3
_a3 = P.ask(k('11', 'b', 'iii'))
_cut = _a3.index('?') + 1
C.add([k('11', 'b', 'iii')], 'chem-1-3', 'a-gas-of-single-atoms', [
    C.lifted('r-1', _q11b3[0].text, 3)], qtext=_a3[:_cut], stem=_q11b_lead)
C.add([k('11', 'b')], 'chem-1-3', 'why-helium-is-unreactive-and-safe', [
    C.lifted('r-1', _q11b3[1].text, 3, 'For "Which one of these gases is chemically unreactive?"'),
    C.lifted('r-2', _q11b3[2].text, 3, 'For "Explain why this gas is chemically unreactive."'),
    C.lifted('r-3', _q11b3[3].text, 4, 'For "Suggest a reason why the balloon shown in the diagram '
             'should not be filled with either of the other two gases."')],
    qtext=_a3[_cut:].strip(), stem=_q11b_lead[:_q11b_lead.index(' Which of these gases')],
    figure=Q11B, cid='q11-b-after-iii', ref_suffix='after (iii)')
Q11CA = FIG + 'paper-q11c-a'
for r, concept in (('i', 'nitrogen-in-the-air'), ('ii', 'natural-fixation-of-nitrogen'),
                   ('iii', 'how-plants-take-in-nitrogen-compounds'),
                   ('iv', 'nitrogen-compounds-from-plants-to-animals'),
                   ('v', 'what-living-things-use-nitrogen-compounds-for'),
                   ('vi', 'why-the-nitrogen-cycle-is-a-cycle')):
    C.fixed([ka('11', 'c', r, 'A')], 'chem-4-3', concept, figure=Q11CA)
Q11CB = FIG + 'paper-q11c-b'
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-3-5', 'definition-of-corrosion', figure=Q11CB)
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-3-5', 'corrosion-of-iron-and-aluminium', figure=Q11CB)
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-3-5', 'extracting-iron-from-its-ores', figure=Q11CB)
# (iv): the scheme prints this part's answer under "(v)" (PDF page 17); the
# paper's (iv) is its last part and the scheme has no (iv) for B.
_q11cb4 = P.items(ka('11', 'c', 'v', 'B'))
assert [it.cell for it in _q11cb4] == ['[4]', None] and _q11cb4[1].text == 'BLANK PAGE', _q11cb4
C.add([ka('11', 'c', 'iv', 'B')], 'chem-4-3', 'why-recycle-aluminium', [
    C.lifted('r-1', _q11cb4[0].text, 4, 'The scheme labels this answer "(v)"; the paper prints the '
             'part as (iv).')], figure=Q11CB)


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
    """Every letter's printed marks, alternatives apart: the paper prints Q11's
    letters in subtotals ("(12)" then "(13)"), so the sum of every mark printed
    under the letter, not the last."""
    out = {}
    for s in P.pseg:
        q, letter, _roman, alt = s.key
        if letter and s.marks_at:
            out[(q, letter, alt)] = out.get((q, letter, alt), 0) + sum(m for _n, m in s.marks_at)
    for (q, letter, _r, _a), m in P.marks.items():
        if letter and not any(key[:2] == (q, letter) for key in out):
            out[(q, letter, None)] = m
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
