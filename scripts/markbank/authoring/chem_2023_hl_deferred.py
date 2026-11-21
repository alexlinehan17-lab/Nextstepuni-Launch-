#!/usr/bin/env python3
"""2023 Higher Level Chemistry, DEFERRED sitting: every part carded from the deferred paper and scheme.

    python3 scripts/markbank/authoring/chem_2023_hl_deferred.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_2023_hl_deferred.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2023 hl --deferred   # write them

The deferred sitting's own paper and scheme (deferredexams/2023/LC022ALP000EV,
deferredmarkingschemes/2023/LC022ALP000EV), read by chem_print.Printed(...,
sitting='deferred') in the labelled ("cue") layout June 2023 uses. Every card
is new (ids chem-2023-hl-deferred-...), cited "... — Deferred sitting".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, routed, anyN, point, mark_terms, display, tidy  # noqa: E402,F401
import chem_deferred_lib as LIB  # noqa: E402

P = Printed(2023, 'hl', figures=True, sitting='deferred')
C = Cards(P)
FIG = 'chemistry-2023-HL-deferred-'  # chem_print_figures.name(2023, 'hl-deferred', ...)
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
C.ordered([k('1', 'a', 'i'), k('1', 'a', 'ii'), k('1', 'a', 'iii')], TOPIC, 'compound-usually-added-water-provide-mn')
C.fixed([k('1', 'b', 'i')], TOPIC, 'standard-solution')
C.fixed([k('1', 'b', 'ii')], TOPIC, 'using-pipette-150-cm-iodine-solution')
C.fixed([k('1', 'b', 'iii')], TOPIC, 'indicator-titrations')
C.fixed([k('1', 'b', 'iv')], TOPIC, 'colour-change-observed-conical-flask-end')
C.answer_only([k('1', 'c', 'i')], TOPIC, 'average-number-moles-sodium-thiosulfate-titration', S + 'q1c-i')
C.route([k('1', 'c', 'ii')], TOPIC, 'number-moles-150-cm-solution-titrated',
        fixes={'thiosulfate : I₂ = 2 : 1 ⇒ 0.000114 (1.14 × 10⁻⁴, 57/500000) \uf0b8 2 = 0.000057 (5.7 × 10⁻⁵, 57/1000000) moles I₂ in 150.0 cm³':
               'thiosulfate : I₂ = 2 : 1 ⇒ 0.000114 (1.14 × 10⁻⁴, 57/500000) ÷ 2 = 0.000057 (5.7 × 10⁻⁵, 57/1000000) moles I₂ in 150.0 cm³'})
C.answer_only([k('1', 'c', 'iii')], TOPIC, 'concentration-dissolved-oxygen-lake-water-moles', S + 'q1c-iii')
C.answer_only([k('1', 'c', 'iv')], TOPIC, 'concentration-dissolved-oxygen-lake-water-mg', S + 'q1c-iv')

# ── Q2 ────────────────────────────────────────────────────────────
C.fixed([k('2', 'a', 'i')], TOPIC, 'when-combustion-tests-carried-out-separately')
C.fixed([k('2', 'a', 'ii')], TOPIC, 'expect-observe-adding-few-drops-dilute')
C.fixed([k('2', 'b', 'i')], TOPIC, 'liquid')
C.ordered([k('2', 'b', 'ii')], TOPIC, 'balanced-equation-reaction-took-place-between')
C.fixed([k('2', 'b', 'iii')], TOPIC, 'based-observation-liquid-second-sample-bottle')
C.fixed([k('2', 'b', 'iv')], TOPIC, 'another-redox-chemical-test-confirm-identification')
C.fixed([k('2', 'c', 'i')], TOPIC, 'aid-labelled-diagram-method-measure-melting')
# Q2(c)(ii): two methods, each priced (6), the second after "or" ("[Both parts linked.]"): each a route.
_q2c2 = P.items(k('2', 'c', 'ii'))
assert [it.cell for it in _q2c2] == ['[6]', '[6]'], _q2c2
C.add([k('2', 'c', 'ii')], TOPIC, 'been-verified-recrystallised-benzoic-acid-crystals', [
    routed(point('r-1', C._verbatim(_q2c2[0].text, {}, k('2', 'c', 'ii'))[0], 6,
                 'The scheme prices this method (6), or instead the next.'), 'a'),
    routed(point('r-2', C._verbatim(_q2c2[1].text, {}, k('2', 'c', 'ii'))[0], 6,
                 'Or instead this method (6). ' + ' '.join(_q2c2[1].asides)), 'b')], total=6)
C.answer_only([k('2', 'c', 'iii')], TOPIC, 'percentage-recovery-filter-crystals-recrystallisation-paper', S + 'q2c-iii')
C.fixed([k('2', 'c', 'iv')], TOPIC, 'during-recrystallisation-hot-solution-benzoic-acid')

# ── Q3 ────────────────────────────────────────────────────────────
C.ordered([k('3', 'a', 'i'), k('3', 'a', 'ii'), k('3', 'a', 'iii')], TOPIC, 'chemical-hazard-indicated-pictogram')
C.route([k('3', 'b', 'i')], TOPIC, 'number-moles-hydrogen-peroxide-10-cm')
C.route([k('3', 'b', 'ii')], TOPIC, 'find-theoretical-volume-oxygen-gas-measured')
C.fixed([k('3', 'b', 'iii')], TOPIC, 'suggest-suitable-vessel-collect-measure-oxygen')
C.drawn([k('3', 'b', 'iv')], TOPIC, 'draw-labelled-diagram-arrangement-apparatus-chemicals', S + 'q3b-iv')
C.fixed([k('3', 'c', 'i')], TOPIC, 'use-data-table-plot-graph-volume')
# Q3(c)(ii): the tangent (3) and the rate, 0.42 cm³ O₂ per second (3), its working set out beneath it (two points
# read from the tangent, then the division, in a box priced (3) again for the same mark): the paper prices (c) at
# 18 and the scheme (i) at 12, so (ii) at 6.
_q3c2 = P.items(k('3', 'c', 'ii'))
assert [it.cell for it in _q3c2] == ['[3]', '[3]', '[3]'], _q3c2
C.add([k('3', 'c', 'ii')], TOPIC, 'use-graph-determine-instantaneous-rate-240', [
    C.lifted('r-1', 'good tangent drawn to plotted curve at 240 seconds', 3, ''),
    C.lifted('r-2', '0.42 cm³ O₂ per second [0.32 – 0.46] cm³ O₂ per second', 3,
             'The scheme sets out the working that earns the rate: any two points from tangent read correctly, e.g. '
             '(0, 105) and (320, 240) / rise and run correctly read from tangent, e.g. 134 cm³, 240 seconds; then the '
             'division, in a form its text cannot carry; its own print is shown with the answer. It adds: '
             + ' '.join(_q3c2[2].asides))], total=6, figure=S + 'q3c-ii')

# ── Q4 ────────────────────────────────────────────────────────────
C.fixed([k('4', 'a')], TOPIC, 'iridium-naturally-occurring-stable-isotopes-iridium')
C.fixed([k('4', 'b')], TOPIC, 'first-fundamental-processes-mass-spectrometry-order')
C.answer_only([k('4', 'c')], TOPIC, 'copy-complete-equation-alpha-decay-polonium', S + 'q4c')
C.fixed([k('4', 'd')], TOPIC, 'polar-ice-caps-melt-environmentalists-concerned')
C.fixed([k('4', 'e')], TOPIC, 'avogadro-law')
C.answer_only([k('4', 'f')], TOPIC, 'racing-car-tyre-like-contained-294', S + 'q4f')
C.fixed([k('4', 'g')], TOPIC, 'becl-molecule-linear-shape-but-molecule')
C.fixed([k('4', 'h')], TOPIC, 'confirm-presence-sulfite-ions-aqueous-solution')
C.ordered([k('4', 'i')], TOPIC, 'marble-statue-david-michelangelo-kept-indoors')
C.fixed([k('4', 'j')], TOPIC, 'total-number-sigma-bonds-benzene-molecule')
C.drawn([k('4', 'k')], TOPIC, 'draw-structure-molecule-propane-triol-glycerol', S + 'q4k')
C.fixed([ka('4', 'l', None, 'A')], TOPIC, 'nitrogen-chemically-inert')
C.fixed([ka('4', 'l', None, 'B')], TOPIC, 'reference-sublevel-zinc-not-considered-transition')

# ── Q5 ────────────────────────────────────────────────────────────
C.ordered([k('5', 'a')], TOPIC, 'triad-elements-according-dobereiner')
C.drawn([k('5', 'b')], TOPIC, 'carry-out-flame-test-confirm-presence', S + 'q5b')   # three methods set as a table
C.fixed([k('5', 'c', 'i')], TOPIC, 'electron-configuration-potassium-atom-ground')
C.fixed([k('5', 'c', 'ii')], TOPIC, 'many-energy-sublevels-occupied-electrons-potassium')
C.fixed([k('5', 'd', 'i')], TOPIC, 'first-ionisation-energy-neutral-gaseous-atom')
C.fixed([k('5', 'd', 'ii')], TOPIC, 'balanced-equation-represent-first-ionisation-potassium')
C.fixed([k('5', 'd', 'iii')], TOPIC, 'account-decreasing-trend-first-ionisation-energy')
C.fixed([k('5', 'd', 'iv')], TOPIC, 'general-increase-first-ionisation-energy-values')
C.fixed([k('5', 'd', 'v')], TOPIC, 'magnesium-significantly-larger-first-ionisation-energy')

# ── Q6 ────────────────────────────────────────────────────────────
C.drawn([k('6', 'a', 'i')], TOPIC, 'aid-labelled-diagram-kerosene-obtained-oil', S + 'q6a-i')
C.fixed([k('6', 'a', 'ii')], TOPIC, 'property-kerosene-allows-separated-other-constituents')
C.fixed([k('6', 'a', 'iii')], TOPIC, 'kerosene-mixture-hydrocarbons-some-compounds-occur')
C.answer_only([k('6', 'b', 'i')], TOPIC, 'heat-combustion-given-heats-formation-carbon', S + 'q6b-i')
C.route([k('6', 'b', 'ii')], TOPIC, 'particular-aircraft-fuel-tank-holds-235')
C.fixed([k('6', 'c', 'i')], TOPIC, 'hydrogen-gas-manufactured-industrial-scale')
C.fixed([k('6', 'c', 'ii')], TOPIC, 'suggest-disadvantage-hydrogen-fuel-aircraft')

# ── Q7 ────────────────────────────────────────────────────────────
C.fixed([k('7', 'a', 'i')], TOPIC, 'underlined-term')
C.fixed([k('7', 'a', 'ii')], TOPIC, 'le-ch-telier-principle')
C.fixed([k('7', 'b', 'i')], TOPIC, 'equilibrium-established-faster-when-particle-size')
C.fixed([k('7', 'b', 'ii')], TOPIC, 'platinum-metal-originally-catalyst-conversion-however', skip=('[SO₃]² Kc = [SO₂]²[O₂]∗',))  # (7(c)'s Kc expression reaches (b)(ii)'s lines)
C.drawn([k('7', 'c', 'i')], TOPIC, 'equilibrium-constant-kc-expression-reaction', S + 'q7c-i')   # Kc set as a fraction
C.answer_only([k('7', 'c', 'ii')], TOPIC, 'number-moles-so-present-equilibrium-hence', S + 'q7c-ii')
C.fixed([k('7', 'd', 'i')], TOPIC, 'equilibrium-yield-so-change-result')
C.fixed([k('7', 'd', 'ii')], TOPIC, 'value-kc-change-result')
C.fixed([k('7', 'd', 'iii')], TOPIC, 'industrial-disadvantage-operating-higher-pressure-than')
C.fixed([k('7', 'e', 'i')], TOPIC, 'forward-reaction-exothermic-endothermic-reasoning')
C.fixed([k('7', 'e', 'ii')], TOPIC, 'suggest-temperature-lower-than-730-not')

# ── Q8 ────────────────────────────────────────────────────────────
C.fixed([k('8', 'a', 'i')], TOPIC, 'systematic-iupac-names')
C.fixed([k('8', 'a', 'ii')], TOPIC, 'four-compounds-molecules-contain-only-carbon')
C.fixed([k('8', 'b', 'i')], TOPIC, 'reagent-conditions-required-bring-about-conversion')
C.ordered([k('8', 'b', 'ii')], TOPIC, 'mechanism-reaction')  # an [any N] menu inside a split
C.fixed([k('8', 'b', 'iii')], TOPIC, 'can-addition-little-tetraethyl-lead-reaction')
C.fixed([k('8', 'c', 'i')], TOPIC, 'reagent-required-bring-about-conversion')
C.fixed([k('8', 'c', 'ii')], TOPIC, 'organic-reaction-type-involved-conversion')
C.fixed([k('8', 'd', 'i')], TOPIC, 'polymer-produced-reaction')
C.drawn([k('8', 'd', 'ii')], TOPIC, 'draw-repeating-units-polymer', S + 'q8d-ii')
C.fixed([k('8', 'd', 'iii')], TOPIC, 'does-geometry-around-carbon-atoms-change')

# ── Q9 ────────────────────────────────────────────────────────────
C.fixed([k('9', 'a', 'i')], TOPIC, 'arrhenius-theory')
C.fixed([k('9', 'a', 'ii')], TOPIC, 'br-nsted-lowry-theory')
C.fixed([k('9', 'a', 'iii')], TOPIC, 'species-acting-br-nsted-lowry-acids')
C.fixed([k('9', 'a', 'iv')], TOPIC, 'can-ammonia-nh-not-classified-base')
C.fixed([k('9', 'b', 'i')], TOPIC, 'ph')
C.fixed([k('9', 'b', 'ii')], TOPIC, 'limitation-ph-scale')
C.route([k('9', 'b', 'iii')], TOPIC, 'ammonium-hydroxide-nh-oh-produced-when')
C.fixed([k('9', 'c', 'i')], TOPIC, 'hin-acts-acid-base-indicator')
C.fixed([k('9', 'c', 'ii')], TOPIC, 'indicator-hin-changes-colour-ph-range')

# ── Q10 ────────────────────────────────────────────────────────────
C.route([k('10', 'a', 'i')], TOPIC, 'mass-oxygen-had-reacted-feo-sample')
C.answer_only([k('10', 'a', 'ii')], TOPIC, 'total-mass-oxygen-had-reacted-whole', S + 'q10a-ii')
C.route([k('10', 'a', 'iii')], TOPIC, 'total-number-moles-fe-produced')
C.fixed([k('10', 'a', 'iv')], TOPIC, 'oxidation-numbers-iron-feo-fe-fe')
C.fixed([k('10', 'b', 'i')], TOPIC, 'technique-suitable-extraction-clove-oil-cloves')
# Q10(b)(ii): the scheme prints two answers, each of two points (2 × 3), joined by "or" on a line of its own, which
# the reader runs together: each side is a route.
_q10b2 = P.items(k('10', 'b', 'ii'))
assert [it.cell for it in _q10b2] == ['[2 × 3]'], _q10b2
C.add([k('10', 'b', 'ii')], TOPIC, 'principle-separation-components-mixture-using-any', [
    routed(C.lifted('r-1', 'components have different attractions (affinities, interactions, solubilities) for (in) / '
                    'components differentially partitioned (dissolved) between', 3,
                    'The scheme prices this point and the next (2 × 3), one each, or instead the two points after them.'),
           'a'),
    routed(C.lifted('r-2', 'stationary and mobile phases', 3), 'a'),
    routed(C.lifted('r-3', 'mobile phase carrying the mixture through (in contact with) stationary phase', 3,
                    'Or instead, this point and the next (2 × 3), one each.'), 'b'),
    routed(C.lifted('r-4', 'components selectively (differently) adsorbed (retained) by stationary phase / components '
                    'pass (move, elute) through (on, along) stationary phase at different speeds (rates)', 3), 'b')],
    total=6)
C.fixed([k('10', 'b', 'iii')], TOPIC, 'infrared-spectrometry-described-fingerprinting-technique')
C.route([k('10', 'b', 'iv')], TOPIC, 'relative-molecular-mass-mr-eugenol')
C.answer_only([k('10', 'b', 'v')], TOPIC, 'elemental-percentage-composition-mass-eugenol', S + 'q10b-v')
C.fixed([k('10', 'b', 'vi')], TOPIC, 'expect-eugenol-decolourise-solution-bromine-justify')
C.fixed([k('10', 'c', 'i')], TOPIC, 'chemical-cause-flocculation-water-treatment')
C.fixed([k('10', 'c', 'ii')], TOPIC, 'result-adding-flocculant')
C.fixed([k('10', 'c', 'iii')], TOPIC, 'purpose-adding-chlorine-drinking-water-supply')
C.fixed([k('10', 'c', 'iv')], TOPIC, 'important-not-add-too-much-chlorine')
C.fixed([k('10', 'c', 'v')], TOPIC, 'chemical-fluoridate-drinking-water')
C.fixed([k('10', 'c', 'vi')], TOPIC, 'important-not-add-too-much-fluorine')
C.fixed([k('10', 'c', 'vii')], TOPIC, 'example-problem-arise-if-ph-public')

# ── Q11 ────────────────────────────────────────────────────────────
C.fixed([k('11', 'a', 'i')], TOPIC, 'electronegativity')
# Q11(a): the scheme prints no "(iii)"; (ii)'s cell answers (ii), and the four after it, IDENTIFY (2), IDENTIFY (2),
# DESCRIBE (3) and ACCOUNT (3), answer the paper's (iii), in order.
_q11a2 = P.items(k('11', 'a', 'ii'))
assert [it.cell for it in _q11a2] == ['[3 × 2]', '[2]', '[2]', '[3]', '[3]'], _q11a2
C.add([k('11', 'a', 'ii')], TOPIC, 'compounds-listed-does-hydrogen-bonding-occur', pieces_of(_q11a2[:1], k('11', 'a', 'ii')),
      total=6)
C.add([k('11', 'a', 'iii')], TOPIC, 'hydrogen-chloride-solubility-in-water', [
    point('r-1', C._verbatim(_q11a2[1].text, {}, k('11', 'a', 'ii'))[0], 2, 'IDENTIFY, the compound.'),
    point('r-2', C._verbatim(_q11a2[2].text, {}, k('11', 'a', 'ii'))[0], 2,
          'IDENTIFY, the force. The scheme adds: ' + ' '.join(_q11a2[2].asides)),
    point('r-3', C._verbatim(_q11a2[3].text, {}, k('11', 'a', 'ii'))[0], 3,
          'DESCRIBE. The scheme adds: ' + ' '.join(_q11a2[3].asides) + ' Its diagram is shown with the answer.'),
    point('r-4', C._verbatim(_q11a2[4].text, {}, k('11', 'a', 'ii'))[0], 3, 'ACCOUNT.')], total=10,
    figure=S + 'q11a-iii')
C.fixed([k('11', 'a', 'iv')], TOPIC, 'weak-intermolecular-forces-in-hydrogen')
C.answer_only([k('11', 'b', 'i')], TOPIC, 'rate-chemical-reaction', S + 'q11b-i')
# Q11(b)(ii): three answers, each of two points (2 × 2), joined by "or" on lines of their own: each side a route.
_q11b2 = P.items(k('11', 'b', 'ii'))
assert [it.cell for it in _q11b2] == ['[2 × 2]'], _q11b2
_EA = 'The scheme adds: [At least one mention of collisions or colliding is essential for full marks.]'
C.add([k('11', 'b', 'ii')], TOPIC, 'meant-activation-energy-reaction', [
    routed(C.lifted('r-1', 'minimum combined energy of colliding particles (molecules)', 2,
                    'The scheme prices this point and the next (2 × 2), one each, or instead either pair after them. '
                    + _EA), 'a'),
    routed(C.lifted('r-2', 'for reaction to take place between them', 2), 'a'),
    routed(C.lifted('r-3', 'minimum combined energy of reacting particles (molecules)', 2,
                    'Or instead, this point and the next (2 × 2), one each.'), 'b'),
    routed(C.lifted('r-4', 'for (of) effective collisions', 2), 'b'),
    routed(C.lifted('r-5', 'minimum energy of reacting molecules (particles)', 2,
                    'Or instead, this point and the next (2 × 2), one each.'), 'c'),
    routed(C.lifted('r-6', 'for product molecule(s) to be formed / for reaction to occur / for intermediate (transition '
                    'state) to be formed / for internal bonds to be broken', 2), 'c')], total=4)
C.fixed([k('11', 'b', 'iii')], TOPIC, 'rates-many-reactions-increase-when-concentration')
C.fixed([k('11', 'b', 'iv')], TOPIC, 'rates-reactions-generally-increase-temperature')
C.fixed([k('11', 'b', 'v')], TOPIC, 'reactions-fast-room-temperature-when-both')
C.fixed([k('11', 'b', 'vi')], TOPIC, 'reactions-often-slow-room-temperature-when')
C.fixed([k('11', 'b', 'vii')], TOPIC, 'suggest-reason-chemical-reactions-generally-slow')
C.fixed([k('11', 'c', 'i')], TOPIC, 'reduction-terms-electron-transfer')
C.fixed([k('11', 'c', 'ii')], TOPIC, 'platinum-electrodes-described-inert')
C.fixed([k('11', 'c', 'iii')], TOPIC, 'gas-produced-negative-electrode-during-electrolysis')
C.ordered([k('11', 'c', 'iv')], TOPIC, 'balanced-half-equation-reduction-reaction-occurred')
C.fixed([k('11', 'c', 'v')], TOPIC, 'colours-observed-electrodes-electrolysis-proceeds')
C.fixed([k('11', 'c', 'vi')], TOPIC, 'sodium-ions-solution-not-reduced-sodium')
C.fixed([ka('11', 'd', 'i', 'A')], TOPIC, 'ozone')
C.fixed([ka('11', 'd', 'ii', 'A')], TOPIC, 'type-electromagnetic-radiation-absorbed-ozone-layer')
C.fixed([ka('11', 'd', 'iii', 'A')], TOPIC, 'cfc-compound-cfc-compound')
C.fixed([ka('11', 'd', 'iv', 'A')], TOPIC, 'balanced-equation-breakdown-molecule-stratosphere-giving')
C.fixed([ka('11', 'd', 'v', 'A')], TOPIC, 'balanced-equations-show-chlorine-free-radicals')
C.fixed([ka('11', 'd', 'vi', 'A')], TOPIC, 'underlined-term')
C.fixed([ka('11', 'd', 'vii', 'A')], TOPIC, 'demonstrate-co-acidic-oxide')
C.fixed([ka('11', 'd', 'i', 'B')], TOPIC, 'second-product-downs-cell')
C.fixed([ka('11', 'd', 'ii', 'B')], TOPIC, 'do-products-kept-separate-achieved-downs')
C.fixed([ka('11', 'd', 'iii', 'B')], TOPIC, 'temperature-molten-electrolyte-downs-cell-only')
C.fixed([ka('11', 'd', 'iv', 'B')], TOPIC, 'material-positive-electrode-downs-cell-choice')
C.ordered([ka('11', 'd', 'v', 'B')], TOPIC, 'balanced-half-equation-reaction-takes-place')
C.fixed([ka('11', 'd', 'vi', 'B')], TOPIC, 'usually-only-electropositive-metals-extracted-their')


# ── The paper's pictures, and a lead-in the reader carries too far ──────────────
_ids = {c['id'][len(C.prefix):]: c for c in C.cards}
# Q9(a)'s lead-in "What is an acid according to" belongs to (i) and (ii); (iii) is an ask of its own.
assert _ids['q9-a-iii']['stem'] == 'What is an acid according to', _ids['q9-a-iii']['stem']
_ids['q9-a-iii']['stem'] = ''

# Each card shows the figure its ask reads from (chemistry/crops/2023-hl-deferred.json). Where the card's own
# figure is already the scheme's answer, the paper's figure is its question figure instead, shown beside the
# printed ask (questionFigureIncludesPrompt: False).
PAPER_FIGURES = {
    'q1-a-i-iii': 'paper-q1',                                       # the dropper and the stoppered sample bottle
    # Q1(b) and Q1(c)(ii) carry Q1's stem, "using a dropper as shown in the diagram" (card lint, 20 Nov); Q1(c)(i),
    # (iii) and (iv) already show the scheme's answer and Q1(a) the paper's drawing.
    **{c: 'paper-q1' for c in ('q1-b-i', 'q1-b-ii', 'q1-b-iii', 'q1-b-iv', 'q1-c-ii')},
    'q2-c-iv': 'paper-q2c',                                         # the fluted filter paper "as shown"
    'q3-a-i-iii': 'paper-q3a',                                      # the hazard pictogram
    **{c: 'paper-q3c' for c in ('q3-c-i', 'q3-c-ii')},              # the results table
    'q4-f': 'paper-q4f',                                            # the racing car tyre "like that shown"
    **{c: 'paper-q8' for c in ('q8-a-i', 'q8-a-ii', 'q8-b-i', 'q8-b-ii', 'q8-b-iii', 'q8-c-i', 'q8-c-ii',
                               'q8-d-i', 'q8-d-ii', 'q8-d-iii')},  # the four compounds A-D
    **{c: 'paper-q10b' for c in ('q10-b-i', 'q10-b-ii', 'q10-b-iii', 'q10-b-iv', 'q10-b-v', 'q10-b-vi')},  # eugenol
    **{c: 'paper-q11c' for c in ('q11-c-i', 'q11-c-ii', 'q11-c-iii', 'q11-c-iv', 'q11-c-v', 'q11-c-vi')},
    **{c: 'paper-q11d-a' for c in ('q11-d-a-i', 'q11-d-a-ii', 'q11-d-a-iii', 'q11-d-a-iv', 'q11-d-a-v',
                                   'q11-d-a-vii')},                 # the four refrigerants
}
# Asks the paper prints with notation no text layer carries (Q4(c)'s nuclear equation) or about a term it
# underlines: the paper's own print is the card's question.
PRINTS = {'q4-c': 'paper-q4c-print', 'q6-a-iii': 'paper-q6a-iii-print', 'q7-a-i': 'paper-q7a-i-print',
          'q11-d-a-vi': 'paper-q11d-a-vi-print'}
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
# authored/chemistry.json: 129 of 132 agreed; the three they split on follow June's majority for that kind of ask
# (Q4(l)B, why zinc is no transition metal: chem-1-3, as 5 of June's 9 transition-element asks and every one that
# classifies; Q6(c)(i)-(ii), hydrogen as a fuel: chem-2-4, as 4 of 7 and this lane's 2022 Higher Q6(d)).
REVIEWED = {
    'q1-a-i-iii': ('chem-4-1', 'winkler-manganese-salt-and-brown-precipitate'),
    'q1-b-i': ('chem-4-1', 'what-a-standard-solution-is'),
    'q1-b-ii': ('chem-4-1', 'rinsing-and-filling-a-pipette'),
    'q1-b-iii': ('chem-4-1', 'starch-indicator-for-iodine-titration'),
    'q1-b-iv': ('chem-4-1', 'starch-iodine-end-point-colour'),
    'q1-c-i': ('chem-4-1', 'moles-of-thiosulfate-in-a-titre'),
    'q1-c-ii': ('chem-4-1', 'moles-of-iodine-from-thiosulfate'),
    'q1-c-iii': ('chem-4-1', 'dissolved-oxygen-in-moles-per-litre'),
    'q1-c-iv': ('chem-4-1', 'dissolved-oxygen-in-parts-per-million'),
    'q2-a-i': ('chem-2-4', 'sooty-flame-of-ethyne-versus-ethene'),
    'q2-a-ii': ('chem-2-4', 'acidified-permanganate-test-for-unsaturation'),
    'q2-b-i': ('chem-4-2', 'carbonate-test-identifies-ethanoic-acid'),
    'q2-b-ii': ('chem-4-2', 'ethanoic-acid-with-sodium-carbonate-equation'),
    'q2-b-iii': ('chem-4-2', 'silver-mirror-identifies-ethanal'),
    'q2-b-iv': ('chem-4-2', 'fehlings-test-for-ethanal'),
    'q2-c-i': ('chem-u2', 'measuring-a-melting-point-range'),
    'q2-c-ii': ('chem-u2', 'showing-recrystallised-acid-is-purer'),
    'q2-c-iii': ('chem-1-4', 'percentage-recovery-from-recrystallisation'),
    'q2-c-iv': ('chem-u2', 'hot-filtration-removes-insoluble-impurities'),
    'q3-a-i-iii': ('chem-u2', 'peroxide-hazard-precaution-and-catalyst-appearance'),
    'q3-b-i': ('chem-1-4', 'moles-of-hydrogen-peroxide-from-percentage'),
    'q3-b-ii': ('chem-1-4', 'theoretical-volume-of-oxygen-from-peroxide'),
    'q3-b-iii': ('chem-u2', 'vessel-to-collect-and-measure-oxygen'),
    'q3-b-iv': ('chem-u2', 'apparatus-for-collecting-oxygen-from-peroxide'),
    'q3-c-i': ('chem-3-2', 'plotting-oxygen-volume-against-time'),
    'q3-c-ii': ('chem-3-2', 'instantaneous-rate-from-a-tangent'),
    'q4-a': ('chem-1-2', 'what-isotopes-are'),
    'q4-b': ('chem-1-2', 'first-processes-of-mass-spectrometry'),
    'q4-c': ('chem-1-2', 'alpha-decay-of-polonium-208'),
    'q4-d': ('chem-1-4', 'formula-of-methane-hydrate-from-percentage'),
    'q4-e': ('chem-2-3', 'avogadros-law'),
    'q4-f': ('chem-2-3', 'gas-pressure-from-ideal-gas-equation'),
    'q4-g': ('chem-2-2', 'linear-becl2-versus-bent-water'),
    'q4-h': ('chem-u2', 'test-for-the-sulfite-ion'),
    'q4-i': ('chem-4-3', 'limestone-and-carbonic-acid-equation'),
    'q4-j': ('chem-2-1', 'sigma-bonds-in-benzene'),
    'q4-k': ('chem-4-2', 'structure-of-glycerol'),
    'q4-l-a': ('chem-2-1', 'why-nitrogen-is-chemically-inert'),
    'q4-l-b': ('chem-1-3', 'zinc-not-a-transition-metal'),
    'q5-a': ('chem-1-3', 'dobereiner-triads'),
    'q5-b': ('chem-u2', 'flame-test-for-strontium'),
    'q5-c-i': ('chem-1-2', 'electron-configuration-of-potassium'),
    'q5-c-ii': ('chem-1-2', 'sublevels-occupied-in-potassium'),
    'q5-d-i': ('chem-1-2', 'definition-of-first-ionisation-energy'),
    'q5-d-ii': ('chem-1-2', 'equation-for-first-ionisation-of-potassium'),
    'q5-d-iii': ('chem-1-3', 'ionisation-energy-down-group-1'),
    'q5-d-iv': ('chem-1-3', 'ionisation-energy-across-third-period'),
    'q5-d-v': ('chem-1-3', 'magnesium-versus-sodium-ionisation-energy'),
    'q6-a-i': ('chem-2-4', 'fractional-distillation-of-crude-oil'),
    'q6-a-ii': ('chem-2-4', 'property-that-separates-the-fractions'),
    'q6-a-iii': ('chem-2-4', 'what-structural-isomers-are'),
    'q6-b-i': ('chem-3-1', 'heat-of-combustion-of-dodecane'),
    'q6-b-ii': ('chem-1-4', 'carbon-dioxide-molecules-from-burning-kerosene'),
    'q6-c-i': ('chem-2-4', 'industrial-manufacture-of-hydrogen'),
    'q6-c-ii': ('chem-2-4', 'disadvantage-of-hydrogen-as-a-fuel'),
    'q7-a-i': ('chem-3-3', 'dynamic-chemical-equilibrium'),
    'q7-a-ii': ('chem-3-3', 'le-chateliers-principle'),
    'q7-b-i': ('chem-3-2', 'small-catalyst-particles-and-surface-area'),
    'q7-b-ii': ('chem-3-2', 'how-a-catalyst-poison-acts'),
    'q7-c-i': ('chem-3-3', 'kc-expression-for-sulfur-trioxide'),
    'q7-c-ii': ('chem-3-3', 'kc-from-equilibrium-moles-of-so3'),
    'q7-d-i': ('chem-3-3', 'pressure-and-sulfur-trioxide-yield'),
    'q7-d-ii': ('chem-3-3', 'pressure-does-not-change-kc'),
    'q7-d-iii': ('chem-3-3', 'industrial-cost-of-high-pressure'),
    'q7-e-i': ('chem-3-3', 'exothermic-from-kc-falling-with-temperature'),
    'q7-e-ii': ('chem-3-3', 'rate-too-slow-at-low-temperature'),
    'q8-a-i': ('chem-2-4', 'naming-ethane-and-methylbenzene'),
    'q8-a-ii': ('chem-2-2', 'compound-with-only-planar-carbons'),
    'q8-b-i': ('chem-4-2', 'chlorine-and-uv-light-for-substitution'),
    'q8-b-ii': ('chem-4-2', 'free-radical-chlorination-of-ethane-mechanism'),
    'q8-b-iii': ('chem-4-2', 'tetraethyl-lead-evidence-for-radicals'),
    'q8-c-i': ('chem-4-2', 'hydrogen-chloride-adds-to-ethene'),
    'q8-c-ii': ('chem-4-2', 'ethene-to-chloroethane-is-addition'),
    'q8-d-i': ('chem-4-2', 'addition-polymer-of-ethene'),
    'q8-d-ii': ('chem-4-2', 'repeating-units-of-polyethene'),
    'q8-d-iii': ('chem-2-2', 'geometry-change-when-ethene-is-polymerised'),
    'q9-a-i': ('chem-3-4', 'arrhenius-definition-of-an-acid'),
    'q9-a-ii': ('chem-3-4', 'bronsted-lowry-definition-of-an-acid'),
    'q9-a-iii': ('chem-3-4', 'bronsted-lowry-acids-in-an-equilibrium'),
    'q9-a-iv': ('chem-3-4', 'ammonia-not-an-arrhenius-base'),
    'q9-b-i': ('chem-3-4', 'definition-of-ph'),
    'q9-b-ii': ('chem-3-4', 'limitation-of-the-ph-scale'),
    'q9-b-iii': ('chem-3-4', 'ph-of-ammonium-hydroxide-from-kb'),
    'q9-c-i': ('chem-3-4', 'how-an-acid-base-indicator-works'),
    'q9-c-ii': ('chem-3-4', 'indicator-for-weak-base-titration'),
    'q10-a-i': ('chem-1-4', 'mass-of-oxygen-reacting-with-feo'),
    'q10-a-ii': ('chem-1-4', 'total-oxygen-reacting-with-iron-oxides'),
    'q10-a-iii': ('chem-1-4', 'moles-of-fe2o3-produced'),
    'q10-a-iv': ('chem-3-5', 'oxidation-numbers-of-iron-in-oxides'),
    'q10-b-i': ('chem-u2', 'steam-distillation-of-clove-oil'),
    'q10-b-ii': ('chem-u2', 'principle-of-chromatography'),
    'q10-b-iii': ('chem-4-2', 'infrared-as-a-fingerprinting-technique'),
    'q10-b-iv': ('chem-1-4', 'relative-molecular-mass-of-eugenol'),
    'q10-b-v': ('chem-1-4', 'percentage-composition-of-eugenol'),
    'q10-b-vi': ('chem-2-4', 'eugenol-decolourises-bromine'),
    'q10-c-i': ('chem-4-3', 'flocculating-agent-in-water-treatment'),
    'q10-c-ii': ('chem-4-3', 'result-of-adding-a-flocculant'),
    'q10-c-iii': ('chem-4-3', 'chlorination-of-drinking-water'),
    'q10-c-iv': ('chem-4-3', 'excess-chlorine-affects-taste'),
    'q10-c-v': ('chem-4-3', 'fluoridating-agent-for-drinking-water'),
    'q10-c-vi': ('chem-4-3', 'excess-fluoride-causes-fluorosis'),
    'q10-c-vii': ('chem-4-3', 'low-ph-water-corrodes-pipes'),
    'q11-a-i': ('chem-2-1', 'definition-of-electronegativity'),
    'q11-a-ii': ('chem-2-2', 'hydrides-that-hydrogen-bond'),
    'q11-a-iii': ('chem-2-2', 'dipole-dipole-forces-and-hcl-solubility'),
    'q11-a-iv': ('chem-2-2', 'van-der-waals-forces-in-hydrogen'),
    'q11-b-i': ('chem-3-2', 'definition-of-rate-of-reaction'),
    'q11-b-ii': ('chem-3-2', 'activation-energy-definition'),
    'q11-b-iii': ('chem-3-2', 'concentration-and-collision-frequency'),
    'q11-b-iv': ('chem-3-2', 'temperature-and-effective-collisions'),
    'q11-b-v': ('chem-3-2', 'ionic-reactions-in-solution-are-fast'),
    'q11-b-vi': ('chem-3-2', 'covalent-bonds-slow-reactions'),
    'q11-b-vii': ('chem-3-2', 'solid-state-reactions-are-slow'),
    'q11-c-i': ('chem-3-5', 'reduction-defined-by-electron-transfer'),
    'q11-c-ii': ('chem-3-5', 'why-platinum-electrodes-are-inert'),
    'q11-c-iii': ('chem-3-5', 'hydrogen-at-cathode-electrolysing-sodium-sulfate'),
    'q11-c-iv': ('chem-3-5', 'cathode-half-equation-for-water-reduction'),
    'q11-c-v': ('chem-3-5', 'indicator-colours-at-the-electrodes'),
    'q11-c-vi': ('chem-3-5', 'why-sodium-ions-are-not-reduced'),
    'q11-d-a-i': ('chem-4-3', 'what-ozone-is'),
    'q11-d-a-ii': ('chem-4-3', 'ozone-layer-absorbs-ultraviolet'),
    'q11-d-a-iii': ('chem-4-3', 'what-a-cfc-is'),
    'q11-d-a-iv': ('chem-4-3', 'photodissociation-of-a-cfc'),
    'q11-d-a-v': ('chem-4-3', 'chlorine-radical-chain-destroying-ozone'),
    'q11-d-a-vi': ('chem-4-3', 'what-a-greenhouse-gas-is'),
    'q11-d-a-vii': ('chem-4-3', 'demonstrating-carbon-dioxide-is-acidic'),
    'q11-d-b-i': ('chem-u3', 'chlorine-from-the-downs-cell'),
    'q11-d-b-ii': ('chem-u3', 'keeping-downs-cell-products-apart'),
    'q11-d-b-iii': ('chem-u3', 'calcium-chloride-lowers-electrolyte-temperature'),
    'q11-d-b-iv': ('chem-3-5', 'graphite-anode-in-the-downs-cell'),
    'q11-d-b-v': ('chem-3-5', 'chloride-oxidation-half-equation'),
    'q11-d-b-vi': ('chem-u3', 'electrolysis-cost-limits-metal-extraction'),
}
assert set(REVIEWED) == set(_ids), set(REVIEWED) ^ set(_ids)
for _cid, (_topic, _concept) in REVIEWED.items():
    _ids[_cid]['topicId'], _ids[_cid]['conceptId'] = _topic, _concept


# Printed errors in the scheme's own print and its self-contradictions, said in plain words on the card's first row
# (CARD-STANDARD 10f), so a student reading the scheme's crop is told which figure is wrong.
SCHEME_ERRORS = {
    'q1-c-iii': 'A misprint in the scheme: it writes 0.0000285 as "2.85 × 10⁻⁴" (twice); 0.0000285 is 2.85 × 10⁻⁵.',
    'q1-c-iv': 'A misprint in the scheme: its rounding note says the deduction is made once only "in (d)"; this is '
               'part (c).',
    'q3-c-i': 'The scheme labels the time axis "minutes"; the paper\'s table gives the time in seconds.',
    'q3-c-ii': 'A slip in the scheme: its rise-and-run example, "134 cm³, 240 seconds", does not match its own two '
               'points, (0, 105) and (320, 240), which give a rise of 135 cm³ over 320 seconds, as its division uses.',
    'q6-b-i': 'A misprint in the scheme: its box of equations ends "ΔHcombustion –8,083.9 kJ", but the three '
              'equations add to –8,088.1 kJ, the answer it states.',
    'q7-c-i': 'A misprint in the scheme: its note names "(d)(i)" and "(d) (iv) CALCULATE"; on this paper the '
              'expression is (c)(i) and the calculation (c)(ii).',
    'q7-c-ii': 'A misprint in the scheme: its answer line gives "33.45 – 34.5 mol O₂", but both its worked methods '
               'give 34.45 – 34.5 mol O₂. Each method\'s printed step marks also add to 18, against the part\'s 12.',
}
for _cid, _note in SCHEME_ERRORS.items():
    _row = _ids[_cid]['rows'][0]
    _row['contextNote'] = tidy(' '.join(x for x in (_row.get('contextNote') or '', _note) if x))

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
