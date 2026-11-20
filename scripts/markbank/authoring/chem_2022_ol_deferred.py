#!/usr/bin/env python3
"""2022 Ordinary Level Chemistry, DEFERRED sitting: every part carded from the deferred paper and scheme.

    python3 scripts/markbank/authoring/chem_2022_ol_deferred.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_2022_ol_deferred.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2022 ol --deferred   # write them

The deferred sitting's own paper and scheme (deferredexams/2022/LC022GLP000EV,
deferredmarkingschemes/2022/LC022GLP000EV), read by chem_print.Printed(...,
sitting='deferred') in the labelled ("cue") layout June 2022 uses. Every card
is new (ids chem-2022-ol-deferred-...), cited "... — Deferred sitting".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, routed, anyN, point, mark_terms, display, tidy  # noqa: E402,F401
import chem_deferred_lib as LIB  # noqa: E402

P = Printed(2022, 'ol', figures=True, sitting='deferred')
C = Cards(P)
FIG = 'chemistry-2022-OL-deferred-'  # chem_print_figures.name(2022, 'ol-deferred', ...)
S = FIG + 'scheme-'
TOPIC = 'chem-u2'   # a stand-in at each call: every card's topic and concept are REVIEWED's, set below
FRACTION = 'The scheme prints {} over {} as a fraction; ÷ stands for its bar.'


def k(*parts):
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)



def pieces(key, notes=None):
    return LIB.pieces(P, C, key, notes)


def pieces_of(items, key, notes=None):
    return LIB.pieces_of(C, items, key, notes)


def menu_of(key, item, claim, note):
    return LIB.menu_of(P, C, key, item, claim, note)


def split_words(key, tail, notation, total, concept, note=''):
    return LIB.split_words(P, C, key, tail, notation, total, TOPIC, concept, note)

WITHDRAWN = {}

# ── Q1 ────────────────────────────────────────────────────────────
# Q1(a): the scheme prices the five words "FIVE: (3 × 7) + (2 × 2)", set right of the answers on the last word's
# line, which the reader takes partly as answer text.
_q1a = P.items(k('1', 'a'))
assert len(_q1a) == 1 and _q1a[0].cell == '[2 × 2]' and _q1a[0].text.endswith(' (3 × 7) +'), _q1a
_SPLIT_1A = '[(3 × 7) + (2 × 2)]'
C.add([k('1', 'a')], TOPIC, 'words-omitted-paragraph-below-cooling-soluble', [
    C.lifted(f'r-{i}', w, None) for i, w in enumerate(
        [w.strip() for w in _q1a[0].text.replace(' (3 × 7) +', '').split('//')], 1)],
    kind='orderedSplit', notation=_SPLIT_1A, total=25,
    notes=f'The scheme prices these points together as {_SPLIT_1A} without saying which point earns which part, '
          'so no per-point value is shown.')
C.fixed([k('1', 'b')], TOPIC, 'suggest-suitable-solvent-recrystallise-benzoic-acid')
C.menu([k('1', 'c')], TOPIC, 'aid-labelled-diagram-measure-melting-point')
C.fixed([k('1', 'd')], TOPIC, 'way-melting-point-impure-crystals-differs')

# ── Q2 ────────────────────────────────────────────────────────────
C.fixed([k('2', 'a')], TOPIC, 'meant-standard-solution')
C.menu([k('2', 'b')], TOPIC, 'mention-precaution-taken-when-using-pipette')
C.add([k('2', 'c')], TOPIC, 'piece-equipment-measure-hydrochloric-acid-solution', pieces(k('2', 'c')), total=15)
C.fixed([k('2', 'd')], TOPIC, 'suitable-indicator-titration-colour-change-observed')
C.answer_only([k('2', 'e')], TOPIC, 'after-accurate-titrations-found-25-cm', S + 'q2e')

# ── Q3 ────────────────────────────────────────────────────────────
C.ordered([k('3', 'a')], TOPIC, 'pieces-equipment')
C.fixed([k('3', 'b')], TOPIC, 'advisable-filter-water-first')
# Q3(c): "(2 × 4) + 1" for the three points, set at the end of the last.
split_words(k('3', 'c'), ' (2 × 4) + 1', '[(2 × 4) + 1]', 9, 'filtering-seawater')
C.menu([k('3', 'd')], TOPIC, 'student-carried-out-rest-experiment')
C.route([k('3', 'e', 'i')], TOPIC, 'dissolved-solids-grams-per-litre')
C.route([k('3', 'e', 'ii')], TOPIC, 'dissolved-solids-in-ppm')

# ── Q4 ────────────────────────────────────────────────────────────
C.ordered([k('4', 'a')], TOPIC, 'example-household-acid-ii-household-base', deep=True)
C.fixed([k('4', 'b')], TOPIC, 'major-use-ethyne')
C.fixed([k('4', 'c')], TOPIC, 'chemical-formula-calcium-chloride')
C.fixed([k('4', 'd')], TOPIC, 'piece-equipment-measure-energy-value-fuel')
C.fixed([k('4', 'e')], TOPIC, 'radioisotopes-am-co-cancer-treatment')
C.fixed([k('4', 'f')], TOPIC, 'trend-size-atomic-radii-across-period')
C.fixed([k('4', 'g')], TOPIC, 'process-treatment-drinking-water-carried-out')
# Q4(h): the scheme leaves CALCULATE's answer line blank and ends its working "= 48%": the card's answer is that.
C.answer_only([k('4', 'h')], TOPIC, 'percentage-mass-oxygen-calcium-carbonate-caco', S + 'q4h', fixes={'': '48%'})
C.fixed([k('4', 'i')], TOPIC, 'scientist-pictured-right-who-received-nobel')
C.fixed([k('4', 'j')], TOPIC, 'electronegativities-hydrogen-chlorine-20-16-respectively')
C.fixed([k('4', 'k')], TOPIC, 'shape-water-molecule')
C.fixed([ka('4', 'l', None, 'A')], TOPIC, 'chemical-industry-meant-term-feedstock')
C.menu([ka('4', 'l', None, 'B')], TOPIC, 'list-stages-recycling-polystyrene')

# ── Q5 ────────────────────────────────────────────────────────────
C.fixed([k('5', 'a')], TOPIC, 'element-outline-john-dalton-atomic-theory')
C.ordered([k('5', 'b', 'i')], TOPIC, 'number-protons-neutrons-electrons-atom-lithium')
C.fixed([k('5', 'b', 'ii')], TOPIC, 'arrangement-electrons-main-energy-levels-potassium')
C.ordered([k('5', 'b', 'iii')], TOPIC, 'observe-if-small-piece-sodium-dropped')
C.ordered([k('5', 'b', 'iv')], TOPIC, 'alkali-metal-sometimes-street-lighting-colour')

# ── Q6 ────────────────────────────────────────────────────────────
C.ordered([k('6', 'a', 'i'), k('6', 'a', 'ii'), k('6', 'a', 'iii'), k('6', 'a', 'iv')], TOPIC, 'meant-term-hydrocarbon')
C.ordered([k('6', 'b')], TOPIC, 'methylpropane-structural-isomer-butane')
C.ordered([k('6', 'c', 'i'), k('6', 'c', 'ii'), k('6', 'c', 'iii')], TOPIC, 'draw-structural-formula-benzene')

# ── Q7 ────────────────────────────────────────────────────────────
C.fixed([k('7', 'a', 'i')], TOPIC, 'meant-hardness-water')
C.fixed([k('7', 'a', 'ii')], TOPIC, 'suggest-suitable-acid-test')
C.ordered([k('7', 'a', 'iii')], TOPIC, 'gas-released-reaction-tube-liquid-placed')
# Q7(b): define pH (2 × 3), then the pH of 0.05 M sulfuric acid, priced as its answer 1.0 (12) and the working that
# earns it (6, 3, 3).
_q7b = P.items(k('7', 'b'))
assert [it.cell for it in _q7b] == ['[2 × 3]', '[12]', '[6]', '[3]', '[3]'], _q7b
C.add([k('7', 'b')], TOPIC, 'ph-of-sulfuric-acid', [
    *pieces_of(_q7b[:1], k('7', 'b')),
    point('r-3', C._verbatim(_q7b[2].text, {}, k('7', 'b'))[0], 6,
          'The scheme gives the answer, 1.0, priced (12), then the working that earns it, step by step.'),
    point('r-4', C._verbatim(_q7b[3].text, {}, k('7', 'b'))[0], 3, ''),
    point('r-5', C._verbatim(_q7b[4].text, {}, k('7', 'b'))[0], 3,
          'The scheme adds: [Allow 6 marks for –log 0.05 = 1.3]')], total=18)

# ── Q8 ────────────────────────────────────────────────────────────
C.fixed([k('8', 'a')], TOPIC, 'compounds-contains-only-tetrahedrally-bonded-carbon')
C.ordered([k('8', 'b')], TOPIC, 'compounds')
C.ordered([k('8', 'c')], TOPIC, 'classify-each-conversions-addition-substitution-oxidation')
C.fixed([k('8', 'd')], TOPIC, 'substance-required-bring-about-conversion')
C.fixed([k('8', 'e')], TOPIC, 'compounds-can-motor-fuel-instead-petrol')
C.ordered([k('8', 'f')], TOPIC, 'compounds-polymerises-widely-plastic-plastic')

# ── Q9 ────────────────────────────────────────────────────────────
C.ordered([k('9', 'a')], TOPIC, 'catalyst')
C.fixed([k('9', 'b')], TOPIC, 'plot-graph-graph-paper-volume-oxygen')
C.ordered([k('9', 'c', 'i'), k('9', 'c', 'ii'), k('9', 'c', 'iii')], TOPIC, 'volume-oxygen-produced-first-75-seconds')
C.ordered([k('9', 'd')], TOPIC, 'most-modern-cars-catalytic-converter-fitted')

# ── Q10 ────────────────────────────────────────────────────────────
# Q10(a) prints four asks: STATE a property, USE dot and cross diagrams, DESCRIBE a test, WHERE in the home. The
# scheme prices the last three (5 + 1), (5 + 1) and (6) and prints no price for STATE's answers; the paper prices
# (a) at 25, which leaves STATE the 7 the scheme does not print (25 − 18).
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == ['[5 + 1]', '[5 + 1]', '[6]'], _q10a
_STATE = [C.lifted('x', o, 7, '')['verbatim'] for o in (
    'soluble in water', 'conduct electricity when molten', 'conduct electricity in aqueous solution',
    'high melting points', 'high boiling points', 'solid (crystalline)')]
_HOME = [C.lifted('x', o, 6, '')['verbatim'] for o in (
    'on food', 'cooking', 'antiseptic wash', 'eyewash', 'melting ice on paths')]
C.add([k('10', 'a')], TOPIC, 'characteristic-property-ionic-substances-use-dot', [
    anyN('r-1', _STATE[0], 7, 1, 7, _STATE,
         'Any one property. The scheme prints no mark for this ask; the paper prices (a) at 25 and the scheme its '
         'other three asks at 18, which leaves 7.'),
    C.lifted('r-2', 'sodium ion with 10 electrons', 5, 'The scheme prices the two ions (5 + 1).'),
    C.lifted('r-3', 'chloride ion with 18 electrons or 8 in valence shell', 1,
             'The scheme adds: [accept Na⁺Cl‐ with 8 electrons shown in valence shell of Cl]'),
    C.lifted('r-4', 'add silver nitrate (AgNO₃)', 5, 'The scheme prices the test and its result (5 + 1).'),
    C.lifted('r-5', 'white precipitate', 1, ''),
    anyN('r-6', _HOME[0], 6, 1, 6, _HOME, 'Any one, (6); the scheme closes its list "etc".')], total=25)
# Q10(b) sets its two definitions inline, "Define (i) atomic mass number, (ii) relative atomic mass", then the
# relative molecular mass of glucose, its empirical formula and B's molecular formula: one card, each answer priced.
_q10b = P.items(k('10', 'b'), deep=True)   # (the scheme keys its inline (i) and (ii))
assert [it.cell for it in _q10b] == ['[8]', '[5 + 1]', '[6]', '[3 + 2]'], _q10b
C.add([k('10', 'b')], TOPIC, 'atomic-mass-number-ii-relative-atomic', [
    C.lifted('r-1', 'number of protons and neutrons in nucleus of an atom', 8, '(i).'),
    C.lifted('r-2', 'average mass of an atom / mass of an atom taking natural abundances of its isotopes into account',
             5, '(ii). The scheme prices the definition (5 + 1).'),
    C.lifted('r-3', 'compared to 1/12th carbon‐12 atom (isotope)', 1, ''),
    C.lifted('r-4', '(6 × 12) + (12 × 1) + 6 × 16) = 180*', 6,
             'The scheme adds: * Addition must be shown for error to be treated as a slip.'),
    C.lifted('r-5', 'CH₂O', 3, 'The empirical formula; the scheme prices the two formulae (3 + 2).'),
    C.lifted('r-6', 'C₂H₄O₂', 2, 'The molecular formula of B.')], total=25)
# Q10(c): the scheme prices (ii) (6) and then "THREE POINTS: (9 + 2 + 1)" for (iii)'s answer and (iv)'s effect and
# explanation; it prints no mark for (i)'s answer. The paper prices (c) at 25, which leaves (i) the 7 the scheme does
# not print (25 − 6 − 12). (ii)'s expression is set as a stacked fraction: the scheme's own print is its answer.
assert [it.cell for it in P.items(k('10', 'c', 'i'))] == [None] \
    and [it.cell for it in P.items(k('10', 'c', 'iii'))] == [None] \
    and [it.cell for it in P.items(k('10', 'c', 'iv'))] == ['[9 + 2 + 1]']
C.add([k('10', 'c', 'i')], TOPIC, 'le-chatelier-principle', [
    C.lifted('r-1', 'stress (change of conditions) placed on system in chemical equilibrium // results in reaction '
             'to relieve(reduce, absorb, counteract) the stress', 7,
             'The scheme prints no mark for this ask; the paper prices (c) at 25 and the scheme its other asks at 18 '
             '((ii) 6, then (9 + 2 + 1) for (iii) and (iv)), which leaves 7.')], total=7)
C.drawn([k('10', 'c', 'ii')], TOPIC, 'equilibrium-constant-expression-ammonia', S + 'q10c-ii')   # Kc set as a fraction
_SPLIT_10C = '[9 + 2 + 1]'
C.add([k('10', 'c', 'iii'), k('10', 'c', 'iv')], TOPIC, 'pressure-and-ammonia-equilibrium', [
    C.lifted('r-1', 'state of equilibrium equilibrium / reversible reaction', None, '(iii)'),
    C.lifted('r-2', 'more NH₃ (ammonia, product) / bigger yield / less reactants (hydrogen and nitrogen) / '
             'equilibrium moves to the right', None, '(iv), the effect.'),
    C.lifted('r-3', 'equilibrium moves to side with fewer moles (molecules) / Le Châtelier’s principle / stress '
             'opposed by making fewer molecules (moles) of gas', None, '(iv), EXPLAIN.')],
    kind='orderedSplit', notation=_SPLIT_10C, total=12,
    notes=f'The scheme prices these points together as {_SPLIT_10C} ("THREE POINTS") without saying which point '
          'earns which part, so no per-point value is shown.')

# ── Q11 ────────────────────────────────────────────────────────────
# Q11(a): seven words, "(2 × 6) + (2 × 5) + (3 × 1)", the cell set at the end of the last (its brackets read as the
# cell's: "[2 × 6) + (2 × 5) + (3 × 1]").
split_words(k('11', 'a'), ' [2 × 6) + (2 × 5) + (3 × 1]', '[(2 × 6) + (2 × 5) + (3 × 1)]', 25, 'chromatography-passage')
# Q11(b): the scheme prints no romans; its three cells answer the paper's (i) [7], (ii)-(iii) [9 + 3] and (iv)-(v)
# [5 + 1], in order, each answer labelled with its ask ("oxidized:", "reduced:", "blue at start:", ...).
_q11b = P.items(k('11', 'b'))
assert [it.cell for it in _q11b] == ['[7]', '[9 + 3]', '[5 + 1]'], _q11b
C.add([k('11', 'b', 'i')], TOPIC, 'oxidation-as-loss-of-electrons', [
    C.lifted('r-1', 'loss of electrons', 7, '')], total=7)
C.add([k('11', 'b', 'ii'), k('11', 'b', 'iii')], TOPIC, 'species-oxidised-and-reduced', pieces_of(_q11b[1:2], k('11', 'b')),
      total=12)
C.add([k('11', 'b', 'iv'), k('11', 'b', 'v')], TOPIC, 'copper-ions-and-copper-colours', pieces_of(_q11b[2:3], k('11', 'b')),
      total=6)
C.ordered([k('11', 'c', 'i'), k('11', 'c', 'ii')], TOPIC, 'oxygen-atoms-molecule-bonded-covalently-covalent')
C.route([k('11', 'c', 'iii')], TOPIC, 'mass-mercury-metal-produced-when-moles')
C.route([k('11', 'c', 'iv')], TOPIC, 'many-moles-oxygen-gas-priestley-obtained',
        fixes={'(Allow 1 mark for 0.4 moles of oxygen atoms) 0.2 × 22.4 = 4.48 l': '0.2 × 22.4 = 4.48 l'},
        row_notes={0: 'The scheme adds: (Allow 1 mark for 0.4 moles of oxygen atoms)'})
# Q11(d): the scheme does not part A from B for the reader; each alternative is carded from its own printed lines
# (scheme page 16), each lifted. A's lead-in prints three asks: two ways industrial chemistry contributes (ANY TWO:
# 4 + 3), two differences between a batch and a continuous process (ANY TWO: 9 + 3), and one chemical property of glass
# and stainless steel, which the scheme neither answers nor prices: its prices for A add to the paper's 25 without it.
# That third ask is held open (coordinator, 20 Nov: never a mark the SEC did not print, and no row the session cannot
# show unpriced) until the unpricedSection field (CARD-STANDARD 10i) can show it. Then "Answer any one of the
# following" (i)-(iii), ANY ONE: (6).
_ways = [C.lifted('x', o, 4, '')['verbatim'] for o in (
    'makes drugs to cure disease', 'makes artificial fertilizer', 'produces new materials, e.g fabrics or plastics',
    'produces dyes (semiconductors, fuels)', 'provides employment')]
_batch = [C.lifted('x', o, 9, '')['verbatim'] for o in (
    'reactants added at start only', 'product removed only at the end', 'definite reaction time')]
_cont = [C.lifted('x', o, 9, '')['verbatim'] for o in (
    'constant supply of reactant in one end of the reactor', 'product is being removed throughout the process',
    'continuous reaction')]
C.add([ka('11', 'd', None, 'A')], TOPIC, 'industrial-chemistry-batch-and-continuous', [
    anyN('r-1', _ways[0], 7, 2, 4, _ways, 'Any two, (4 + 3); the scheme closes its list "etc".', steps=[4, 3]),
    anyN('r-2', _batch[0], 12, 2, 9, _batch + _cont,
         'Any two differences, (9 + 3). The scheme lists what marks a batch process (the first three: "Batch: '
         'reactants added at start only / product removed only at the end / definite reaction time / etc") and a '
         'continuous one (the last three: "Continuous: ... / etc").', steps=[9, 3])], total=19)
C.add([ka('11', 'd', 'i', 'A'), ka('11', 'd', 'ii', 'A'), ka('11', 'd', 'iii', 'A')], TOPIC,
      'ammonia-nitrogen-monoxide-magnesium-oxide', [
    anyN('r-1', 'making fertilizer / making explosives', 6, 1, 6, [
        C.lifted('x', o, 6, '')['verbatim'] for o in (
            'making fertilizer / making explosives', '2NO + O₂ → 2NO₂ / NO + ½ O₂ → NO₂', 'MgO')],
         'Answer any one: (i) a use for ammonia, (ii) the equation, (iii) the formula, ANY ONE: (6). The scheme '
         'prices (ii)\'s equation FORMULAE: (3); BALANCING: (3).')], total=6)
_SPLIT_11DB = '[11 + 6 + 3 + 3 + 2]'
C.add([ka('11', 'd', 'i', 'B'), ka('11', 'd', 'ii', 'B'), ka('11', 'd', 'iii', 'B')], TOPIC, 'diamond-and-graphite', [
    C.lifted('r-1', 'diamond', None, '(i), NAME.'), C.lifted('r-2', 'covalent', None, '(i), WHAT.'),
    C.lifted('r-3', 'graphite', None, '(ii), NAME.'),
    C.lifted('r-4', 'lubricant / lead in pencils / electrodes / etc', None, '(ii), WHAT.'),
    C.lifted('r-5', 'x‐ray crystallography', None, '(iii), WHAT.')],
    kind='orderedSplit', notation=_SPLIT_11DB, total=25,
    notes=f'The scheme prices these points together as {_SPLIT_11DB} (headed "SEVEN POINTS") without saying which '
          'point earns which part, so no per-point value is shown.')


# ── The paper's pictures, and asks the reader sets under a neighbour ─────────────
_ids = {c['id'][len(C.prefix):]: c for c in C.cards}


def paper_lines(key, *spans):
    seg = [x for x in P.pseg if x.key == key]
    assert len(seg) == 1, key
    lines = seg[0].text
    return tidy(' '.join(display(lines[i].text) for lo, hi in spans for i in range(lo, hi)))


# Q10(c)(iii) is printed on its own line, "(iii) What information is given by the symbol ⇋ ?", which the reader
# files under (ii): each card's question is its own printed ask.
_Q10CII, _Q10CIV = k('10', 'c', 'ii'), k('10', 'c', 'iv')
assert paper_lines(_Q10CII, (2, 3)) == 'What information is given by the symbol ⇋ ?'
QUESTIONS = {   # card -> question
    'q10-c-ii': paper_lines(_Q10CII, (0, 2)),
    'q10-c-iii-iv': f"(iii) {paper_lines(_Q10CII, (2, 3))} (iv) {paper_lines(_Q10CIV, (0, 4))}",
}
for _cid, _q in QUESTIONS.items():
    _ids[_cid]['questionText'] = _q
# Q10(c)(ii)'s drawn card: its ask is (ii)'s own, and its mark the (6) printed beside the expression; the "(3)" the
# reader takes as a second cell is inside the scheme's bracketed note, which the row quotes.
_q10c2 = _ids['q10-c-ii']
assert _q10c2['totalMarks'] == 9 and len(_q10c2['rows']) == 1, _q10c2
_q10c2['totalMarks'] = 6
_q10c2['rows'][0].update(
    verbatim=QUESTIONS['q10-c-ii'], marks=6,
    contextNote='The scheme answers this part with a drawing or notation its text cannot carry; its own print is shown '
                'with the answer. It adds: [Allow (3) for numerator only correct; allow (3) for denominator only '
                'correct; allow (3) for correct numerator and denominator inverted.]')

# Each card shows the figure its ask reads from (chemistry/crops/2022-ol-deferred.json). Where the card's own
# figure is already the scheme's answer, the paper's figure is its question figure instead, shown beside the
# printed ask (questionFigureIncludesPrompt: False).
PAPER_FIGURES = {
    **{c: 'paper-q1' for c in ('q1-a', 'q1-b', 'q1-c', 'q1-d')},   # the stages of the recrystallisation
    'q3-a': 'paper-q3',                                              # the equipment A, B and C
    'q4-i': 'paper-q4i',                                             # the scientist pictured
    'q5-b-iii': 'paper-q5b-iii',                                     # sodium, tweezers, trough, water
    **{c: 'paper-q7a' for c in ('q7-a-ii', 'q7-a-iii')},             # the apparatus, tubes A and B, liquid X
    **{c: 'paper-q8' for c in ('q8-a', 'q8-b', 'q8-c', 'q8-d', 'q8-e', 'q8-f')},   # the reaction scheme
    **{c: 'paper-q9' for c in ('q9-b', 'q9-c-i-iii')},               # the results table
    'q11-d-b-i-iii': 'paper-q11d-b',                                 # the two forms of carbon, A and B
}
# Q5(b)(i) names lithium as the paper prints it, ⁷₃Li, which no text layer carries: its print is the question.
PRINTS = {'q5-b-i': 'paper-q5b-i-print'}
assert set(PAPER_FIGURES) <= set(_ids) and set(PRINTS) <= set(_ids), (set(PAPER_FIGURES) | set(PRINTS)) - set(_ids)
for _cid, _fig in PAPER_FIGURES.items():
    _c = _ids[_cid]
    if _c['figureKey']:
        _c['questionFigureKey'] = FIG + _fig
        _c['questionFigureIncludesPrompt'] = False
    else:
        _c['figureKey'] = FIG + _fig
for _cid, _fig in PRINTS.items():
    _ids[_cid]['questionFigureKey'] = FIG + _fig


# Each card's syllabus topic and concept, filed by two independent readers against the June filings in
# authored/chemistry.json: 64 of 65 agreed; the one they split on, Q3(d) (how to finish measuring the dissolved
# solids), follows June's majority for that ask: chem-4-3, as 2013 OL Q7(b), 2023 OL Q3(a)(ii) and 2026 HL Q3(b)(i)
# are (2015 OL Q3(d) is chem-u2).
REVIEWED = {
    'q1-a': ('chem-u2', 'recrystallisation-stages-passage'),
    'q1-b': ('chem-u2', 'solvent-for-recrystallising-benzoic-acid'),
    'q1-c': ('chem-u2', 'measuring-melting-point-of-benzoic-acid'),
    'q1-d': ('chem-u2', 'impure-crystals-melting-point'),
    'q2-a': ('chem-4-1', 'standard-solution-meaning'),
    'q2-b': ('chem-4-1', 'pipette-precaution'),
    'q2-c': ('chem-4-1', 'burette-and-rinsing-procedure'),
    'q2-d': ('chem-4-1', 'indicator-and-end-point-colour'),
    'q2-e': ('chem-4-1', 'hcl-concentration-from-naoh-titration'),
    'q3-a': ('chem-u2', 'naming-filtration-and-evaporation-apparatus'),
    'q3-b': ('chem-u2', 'why-filter-seawater-first'),
    'q3-c': ('chem-u2', 'filtering-a-water-sample'),
    'q3-d': ('chem-4-3', 'evaporating-to-dryness-for-dissolved-solids'),
    'q3-e-i': ('chem-4-3', 'dissolved-solids-in-grams-per-litre'),
    'q3-e-ii': ('chem-4-3', 'dissolved-solids-in-ppm'),
    'q4-a': ('chem-3-4', 'household-acid-and-base'),
    'q4-b': ('chem-2-4', 'major-use-of-ethyne'),
    'q4-c': ('chem-1-4', 'formula-of-calcium-chloride'),
    'q4-d': ('chem-3-1', 'bomb-calorimeter-for-energy-values'),
    'q4-e': ('chem-1-2', 'cobalt-60-in-cancer-treatment'),
    'q4-f': ('chem-1-3', 'atomic-radius-trend-across-a-period'),
    'q4-g': ('chem-4-3', 'fluoridation-of-drinking-water'),
    'q4-h': ('chem-1-4', 'percentage-oxygen-in-calcium-carbonate'),
    'q4-i': ('chem-1-2', 'marie-curie-polonium-and-radium'),
    'q4-j': ('chem-2-1', 'polarity-of-the-hcl-bond'),
    'q4-k': ('chem-2-2', 'shape-of-a-water-molecule'),
    'q4-l-a': ('chem-u3', 'meaning-of-feedstock'),
    'q4-l-b': ('chem-4-2', 'stages-in-recycling-polystyrene'),
    'q5-a': ('chem-1-2', 'element-and-daltons-atomic-theory'),
    'q5-b-i': ('chem-1-2', 'subatomic-particles-in-lithium-7'),
    'q5-b-ii': ('chem-1-2', 'electron-arrangement-of-potassium'),
    'q5-b-iii': ('chem-1-3', 'sodium-reacting-with-water'),
    'q5-b-iv': ('chem-1-2', 'sodium-street-lights-yellow-emission'),
    'q6-a-i-iv': ('chem-2-4', 'methane-hazards-and-homologous-series'),
    'q6-b': ('chem-2-4', 'methylpropane-isomer-of-butane'),
    'q6-c-i-iii': ('chem-2-4', 'benzene-structure-solubility-and-toxicity'),
    'q7-a-i': ('chem-4-3', 'meaning-of-water-hardness'),
    'q7-a-ii': ('chem-u2', 'acid-for-the-carbonate-test'),
    'q7-a-iii': ('chem-u2', 'limewater-test-for-carbon-dioxide'),
    'q7-b': ('chem-3-4', 'ph-of-dilute-sulfuric-acid'),
    'q8-a': ('chem-2-2', 'only-tetrahedral-carbons-in-ethanol'),
    'q8-b': ('chem-4-2', 'naming-ethene-and-ethanoic-acid'),
    'q8-c': ('chem-4-2', 'addition-and-oxidation-conversions'),
    'q8-d': ('chem-4-2', 'aluminium-oxide-dehydrates-ethanol'),
    'q8-e': ('chem-4-2', 'ethanol-as-a-motor-fuel'),
    'q8-f': ('chem-4-2', 'ethene-polymerises-to-polythene'),
    'q9-a': ('chem-3-2', 'catalyst-definition'),
    'q9-b': ('chem-3-2', 'plotting-oxygen-volume-against-time'),
    'q9-c-i-iii': ('chem-3-2', 'reading-volume-time-and-average-rate'),
    'q9-d': ('chem-3-2', 'catalytic-converter-metals-and-reactions'),
    'q10-a': ('chem-2-1', 'ionic-bonding-in-sodium-chloride'),
    'q10-b': ('chem-1-4', 'glucose-mr-empirical-and-molecular-formula'),
    'q10-c-i': ('chem-3-3', 'le-chateliers-principle'),
    'q10-c-ii': ('chem-3-3', 'kc-expression-for-ammonia-synthesis'),
    'q10-c-iii-iv': ('chem-3-3', 'pressure-effect-on-ammonia-yield'),
    'q11-a': ('chem-u2', 'chromatography-passage'),
    'q11-b-i': ('chem-3-5', 'oxidation-as-loss-of-electrons'),
    'q11-b-ii-iii': ('chem-3-5', 'zinc-oxidised-copper-ions-reduced'),
    'q11-b-iv-v': ('chem-3-5', 'copper-ions-blue-copper-precipitate'),
    'q11-c-i-ii': ('chem-2-1', 'covalent-bond-and-endothermic-reaction'),
    'q11-c-iii': ('chem-1-4', 'mass-of-mercury-from-hgo'),
    'q11-c-iv': ('chem-1-4', 'oxygen-moles-and-volume-at-stp'),
    'q11-d-a': ('chem-u3', 'batch-continuous-and-reaction-vessels'),
    'q11-d-a-i-iii': ('chem-u3', 'ammonia-nitric-acid-or-magnesia-industry'),
    'q11-d-b-i-iii': ('chem-2-1', 'diamond-graphite-and-x-ray-crystallography'),
}
assert set(REVIEWED) == set(_ids), set(REVIEWED) ^ set(_ids)
for _cid, (_topic, _concept) in REVIEWED.items():
    _ids[_cid]['topicId'], _ids[_cid]['conceptId'] = _topic, _concept


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
