#!/usr/bin/env python3
"""2022 Higher Level Chemistry, DEFERRED sitting: every part carded from the deferred paper and scheme.

    python3 scripts/markbank/authoring/chem_2022_hl_deferred.py          # cards as JSON
    python3 scripts/markbank/authoring/chem_2022_hl_deferred.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2022 hl --deferred   # write them

The deferred sitting's own paper and scheme (deferredexams/2022/LC022ALP000EV,
deferredmarkingschemes/2022/LC022ALP000EV), read by chem_print.Printed(...,
sitting='deferred') in the labelled ("cue") layout June 2022 uses. Every card
is new (ids chem-2022-hl-deferred-...), cited "... — Deferred sitting".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, routed, anyN, point, mark_terms, display, tidy  # noqa: E402,F401
import chem_deferred_lib as LIB  # noqa: E402

P = Printed(2022, 'hl', figures=True, sitting='deferred')
C = Cards(P)
FIG = 'chemistry-2022-HL-deferred-'  # chem_print_figures.name(2022, 'hl-deferred', ...)
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
# Q1(a): the scheme prices the three points "4 + (2 × 2)"; the reader takes the "4 +" for answer text.
_q1a = P.items(k('1', 'a'))
assert [it.cell for it in _q1a] == ['[2 × 2]'] and _q1a[0].text.endswith(' 4 +'), _q1a
C.add([k('1', 'a')], TOPIC, 'ensure-all-solution-transferred-small-beaker', [
    C.lifted('r-1', 'rinse (wash) beaker a number (a few, several) times / rinse (wash) repeatedly', 4,
             'The scheme prices the three points 4 + (2 × 2).'),
    C.lifted('r-2', 'with small quantities of deionised water', 2, ''),
    C.lifted('r-3', 'add rinsings into volumetric flask', 2, '')], total=8)
# Q1(b): the washing priced [2 × 3] (two rinses, in order), then the filling, any one of six [6].
_q1b = P.items(k('1', 'b'))
assert [it.cell for it in _q1b] == ['[2 × 3]', '[6]'], _q1b
_fill = [C._verbatim(o, {}, k('1', 'b'))[0] for o in _q1b[1].options()]
C.add([k('1', 'b')], TOPIC, 'procedure-washing-filling-burette-potassium-manganate', [
    C.lifted('r-1', 'rinse (wash) with deionised water', 3,
             'The scheme prices the washing [2 × 3], one for each rinse, and adds: [correct order essential; '
             'one correct (3)].'),
    C.lifted('r-2', 'rinse (wash) with potassium manganate(VII) (permanganate, KMnO₄, MnO₄ –, solution it is '
             'to contain)', 3),
    anyN('r-3', _fill[0], 6, 1, 6, _fill, 'Any one of these for the filling, [6].')], total=12)
C.fixed([k('1', 'c')], TOPIC, 'dilute-sulfuric-acid-added-iron-ii')
C.ordered([k('1', 'd')], TOPIC, 'end-point-detected')
C.route([k('1', 'e', 'i')], TOPIC, 'concentration-solution-volumetric-flask-moles-per',
        fixes={'30 × 0.02 1000 = 0.0006 moles MnO₄ –': '30 × 0.02 ÷ 1000 = 0.0006 moles MnO₄ –'},
        row_notes={0: FRACTION.format('30 × 0.02', '1000')})
C.route([k('1', 'e', 'ii')], TOPIC, 'mass-iron-ii-11-76-crystals',
        fixes={'6.72 \uf0b8 4 = 1.68 g per 250 cm³': '6.72 ÷ 4 = 1.68 g per 250 cm³'})
C.answer_only([k('1', 'e', 'iii')], TOPIC, 'percentage-mass-iron-ii-crystals', S + 'q1e-iii')

# ── Q2 ────────────────────────────────────────────────────────────
C.ordered([k('2', 'a', 'i'), k('2', 'a', 'ii')], TOPIC, 'carbon-atom-tetrahedral-geometry')
C.fixed([k('2', 'b')], TOPIC, 'underlined-term-appearance-distillate')
C.ordered([k('2', 'c')], TOPIC, 'ethanol-unsuitable-solvent-use-liquid-liquid')
C.fixed([k('2', 'd', 'i')], TOPIC, 'distillate-washed-separate-times-using-10')
C.fixed([k('2', 'd', 'ii')], TOPIC, 'tap-stoppered-separating-funnel-opened-briefly')
C.fixed([k('2', 'e')], TOPIC, 'having-separated-aqueous-organic-layers-into')
C.answer_only([k('2', 'f')], TOPIC, 'volume-dry-clove-oil-density-05', S + 'q2f')
C.fixed([k('2', 'g')], TOPIC, 'commercial-use-clove-oil')

# ── Q3 ────────────────────────────────────────────────────────────
C.drawn([k('3', 'a')], TOPIC, 'draw-labelled-diagram-apparatus-been-experiment', S + 'q3a')
C.fixed([k('3', 'b')], TOPIC, 'transition-metal-catalyst-been-when-carrying')
# Q3(c): the scheme's four worded points [3] each, then its own graph, whose axis labels and scale
# reach the text layer as a line of their own; its print is the figure.
C.fixed([k('3', 'c')], TOPIC, 'draw-graph-volume-axis-against-time', skip=('60 50 40 Volume 30 20 10 0 0 1 2 3 4 5 6 7 8 Time',), figure=S + 'q3c')
C.route([k('3', 'd', 'i')], TOPIC, 'time-required-produce-00116-moles-oxygen')
C.answer_only([k('3', 'd', 'ii')], TOPIC, 'instantaneous-rate-reaction-minutes', S + 'q3d-ii')
C.fixed([k('3', 'e')], TOPIC, 'mark-clearly-graph-approximate-curve-expect')

# ── Q4 ────────────────────────────────────────────────────────────
C.menu([k('4', 'a')], TOPIC, 'did-mendeleev-arrange-elements-form-his')
C.ordered([k('4', 'b', 'i'), k('4', 'b', 'ii')], TOPIC, 'atomic-number')
C.ordered([k('4', 'c', 'i'), k('4', 'c', 'ii')], TOPIC, 'so')
C.answer_only([k('4', 'd')], TOPIC, 'many-atoms-448-cm-carbon-dioxide', S + 'q4d')
C.ordered([k('4', 'e')], TOPIC, 'under-conditions-do-gases-come-closest')
C.answer_only([k('4', 'f')], TOPIC, 'molarity-solution-ethanoic-acid-ch-cooh', S + 'q4f')
C.fixed([k('4', 'g')], TOPIC, 'avogadro-law', skip=('CH₃ CH₃',))  # (4(h)'s drawn structure reaches 4(g)'s lines)
C.ordered([k('4', 'h', 'i'), k('4', 'h', 'ii')], TOPIC, 'dimethylpropane')
C.ordered([k('4', 'i')], TOPIC, 'principle-involved-separating-mixture-chromatography')
C.ordered([k('4', 'j', 'i'), k('4', 'j', 'ii')], TOPIC, 'sting-nettles')
C.ordered([k('4', 'k', 'i'), k('4', 'k', 'ii')], TOPIC, 'silicon-chloride')
C.ordered([ka('4', 'l', None, 'A')], TOPIC, 'aid-balanced-equation-atmospheric-nitrogen-gas')
C.fixed([ka('4', 'l', None, 'B')], TOPIC, 'does-sacrificial-anode-protect-piece-metal')

# ── Q5 ────────────────────────────────────────────────────────────
C.fixed([k('5', 'a', 'i')], TOPIC, 'who-coined-electron')
# Q5(a)(ii): Thomson, any two of his printed contributions [6 + 3], and Millikan's one [3].
_q5 = P.items(k('5', 'a', 'ii'))
assert [it.cell for it in _q5] == ['[6 + 3]', '[3]'], _q5
_thomson = [C._verbatim(o, {}, k('5', 'a', 'ii'))[0] for o in _q5[0].options()]
C.add([k('5', 'a', 'ii')], TOPIC, 'contributions-thomson-millikan-our-understanding-electrons', [
    anyN('r-1', _thomson[0], 9, 2, 6, _thomson, 'Any two of these for Thomson, [6 + 3].', steps=[6, 3]),
    point('r-2', C._verbatim(_q5[1].text, {}, k('5', 'a', 'ii'))[0], 3, '')], total=12)
C.fixed([k('5', 'a', 'iii')], TOPIC, 'electronic-configuration-etc-copper-ground')
C.fixed([k('5', 'a', 'iv')], TOPIC, 'electrons-arranged-orbitals-highest-occupied-sub')
C.ordered([k('5', 'b', 'i')], TOPIC, 'given-type-nuclear-radiation-involving-release')
C.ordered([k('5', 'b', 'ii')], TOPIC, 'emission-electrons-carbon-14-according-nuclear')

# ── Q6 ────────────────────────────────────────────────────────────
C.fixed([k('6', 'a')], TOPIC, 'heat-combustion-substance-apparatus-accurately-measure')
C.fixed([k('6', 'b')], TOPIC, 'use-made-kilogram-calorific-values-various')
# Q6(c) prints three asks under one letter: the calculation (12), the reaction profile diagram (6) and an
# advantage of bioethanol (6). One card each, the later two named after the ask ("Q6(c) — ...").
C.answer_only([k('6', 'c')], TOPIC, 'carbon-dioxide-water-produced-burning-liquid', S + 'q6c')
C.add([k('6', 'c')], TOPIC, 'reaction-profile-diagram-combustion-ethanol', [
    C.lifted('r-1', 'y‐axis: energy [Must be shown and labelled.] x‐axis: [Must be shown but need not be labelled.]', 3,
             'The scheme prices the labelled axes (3) and the curve (3).'),
    C.lifted('r-2', 'suitable curve with energy of reactants greater than energy of products', 3, '')],
    total=6, cid='q6-c-profile', ref_suffix='reaction profile diagram', figure=S + 'q6c-profile')
_bio = [C.lifted('x', o, 6, '')['verbatim'] for o in
        ('bioethanol is renewable', 'environmentally friendly', 'reduces knocking', 'cheaper')]
C.add([k('6', 'c')], TOPIC, 'advantage-of-bioethanol-as-motor-fuel', [
    anyN('r-1', _bio[0], 6, 1, 6, _bio, 'Any one of these, [6].')],
    total=6, cid='q6-c-bioethanol', ref_suffix='advantage of bioethanol')
# Q6(d): the process [3], its equation [3 + 3] (formulae, balancing), and any two advantages [2 × 3].
_q6d = P.items(k('6', 'd'))
assert [it.cell for it in _q6d] == ['[3]', '[3 + 3]', '[2 × 3]'], _q6d
_adv = [C._verbatim(o.strip(), {}, k('6', 'd'))[0] for o in _q6d[2].text.split(' / ')]
C.add([k('6', 'd')], TOPIC, 'aid-balanced-equation-hydrogen-produced-large', [
    point('r-1', C._verbatim(_q6d[0].text, {}, k('6', 'd'))[0], 3, ''),
    point('r-2', C._verbatim(_q6d[1].text, {}, k('6', 'd'))[0], 6, 'The scheme prices the equation [3 + 3]: formulae (3), balancing (3).'),
    anyN('r-3', _adv[0], 6, 2, 3, _adv, 'Any two of these advantages, [2 × 3].')], total=15)

# ── Q7 ────────────────────────────────────────────────────────────
C.ordered([k('7', 'a')], TOPIC, 'le-ch-telier-principle')
C.ordered([k('7', 'b')], TOPIC, 'le-ch-telier-principle-may-determine')
C.fixed([k('7', 'c')], TOPIC, 'conditions-not-industry-preparation-ammonia', skip=('[NH₃]² Kc =',))  # (7(d)'s Kc expression reaches 7(c)'s lines)
C.fixed([k('7', 'd')], TOPIC, 'equilibrium-constant-expression-kc-reaction')
C.answer_only([k('7', 'e')], TOPIC, 'experiment-mixture-16-nitrogen-hydrogen-placed', S + 'q7e')
# Q7(f): each roman's EXPLAIN answer (3), then the WHY for both, priced together [2 × 3] (one each) on the
# next page, the first set under (i) without a cell of its own: EXPLAIN & WHY linked.
_q7f1, _q7f2 = P.items(k('7', 'f', 'i')), P.items(k('7', 'f', 'ii'))
assert [it.cell for it in _q7f1] == ['[3]', None] and [it.cell for it in _q7f2] == ['[3]', '[2 × 3]'], (_q7f1, _q7f2)
_WHY = ('The scheme prices the two WHY answers, this one and the other roman\'s, [2 × 3]: one each. It adds: '
        '[EXPLAIN & WHY linked] [Marks only available for WHY if EXPLAIN marks awarded].')
C.add([k('7', 'f', 'i')], TOPIC, 'increase-equilibrium-temperature', [
    point('r-1', C._verbatim(_q7f1[0].text, {}, k('7', 'f', 'i'))[0], 3, ''),
    C.lifted('r-2', 'increased temperature favours endothermic (reverse) reaction', 3, _WHY)], total=6)
C.add([k('7', 'f', 'ii')], TOPIC, 'use-more-efficient-catalyst-justify-each', [
    point('r-1', C._verbatim(_q7f2[0].text, {}, k('7', 'f', 'ii'))[0], 3, ''),
    point('r-2', C._verbatim(_q7f2[1].text, {}, k('7', 'f', 'ii'))[0], 3, _WHY)], total=6)

# ── Q8 ────────────────────────────────────────────────────────────
C.fixed([k('8', 'a')], TOPIC, 'alkenes-alkynes-described-unsaturated-hydrocarbons-meaning')
C.fixed([k('8', 'b')], TOPIC, 'aid-diagrams-difference-structure-between-alkene')
C.ordered([k('8', 'c', 'i')], TOPIC, 'balanced-equation-reaction-involved-laboratory-preparation')
C.fixed([k('8', 'c', 'ii')], TOPIC, 'test-carry-out-show-ethyne-unsaturated')
C.fixed([k('8', 'c', 'iii')], TOPIC, 'large-scale-use-ethyne')
C.ordered([k('8', 'd', 'i'), k('8', 'd', 'ii'), k('8', 'd', 'iii')], TOPIC, 'ethanol-ethene')
_evidence = [C.lifted('x', o, 3, '')['verbatim'] for o in (
    'tetraethyllead (source of radicals) increases the rate (speeds up reaction) by providing (producing, breaking '
    'into) ethyl free radicals',
    'oxygen (radical inhibitor) decreases the rate (slows down reaction) by removing free radicals',
    'only occurs in sunlight (UV)', 'reaction cannot occur in darkness',
    'for every photon absorbed, many choromethane molecules obtained', 'small amounts of ethane formed')]
# Q8(e): the mechanism (initiation, two propagation steps, termination) and one piece of evidence, each
# (3); the scheme sets its notes in a side column, so each row is the answer column's own line.
C.add([k('8', 'e')], TOPIC, 'reaction-mechanism-monochlorination-methane-piece-experimental', [
    C.lifted('r-1', 'homolysis (splitting, fission) of chlorine molecule (Cl₂) into free radicals (atoms, Cl●, '
             'Cl) by ultraviolet (uv) light / Cl₂ uv 2Cl● / Cl₂ uv 2Cl', 3, 'Initiation.'),
    C.lifted('r-2', 'chlorine radical (atom, Cl●, Cl) reacts with methane molecule (CH₄) giving hydrogen chloride '
             '(HCl) and a methyl radical (CH₃●) / Cl● + CH₄ → HCl + CH₃● / Cl + CH₄ → HCl + CH₃●', 3,
             'Propagation (1). The scheme adds: [Hydrochloric acid not acceptable for HCl and cancellation '
             'applies.] [Where CH₃ used instead of CH₃● deduct 3 marks but only once in (c).]'),
    C.lifted('r-3', 'methyl radical (CH₃●) reacts with chlorine molecule (Cl₂) giving monochloromethane (CH₃Cl) '
             'and a chlorine radical (atom, Cl●, Cl) / CH₃● + Cl₂ → CH₃Cl + Cl● / CH₃● + Cl₂ → CH₃Cl + Cl', 3,
             'Propagation (2). The scheme adds: Allow (3) for chain reaction occurs / propagation steps repeat '
             'until one reactant used up / propagation steps repeat until termination reached if (0) marks '
             'awarded for propagation (1) and propagation (2).'),
    C.lifted('r-4', 'combination of remaining radicals 2Cl● → Cl₂ / 2Cl → Cl₂ / Cl● + CH₃● → CH₃Cl / Cl + CH₃● → '
             'CH₃Cl / 2CH₃● → C₂H₆', 3, 'Termination.'),
    anyN('r-5', _evidence[0], 3, 1, 3, _evidence, 'Any one piece of evidence, (3).')], total=15, figure=S + 'q8e')

# ── Q9 ────────────────────────────────────────────────────────────
C.fixed([k('9', 'a', 'i')], TOPIC, 'do-letters-edta-stand')
C.fixed([k('9', 'a', 'ii')], TOPIC, 'substances-must-added-50-cm-water')
C.answer_only([k('9', 'a', 'iii')], TOPIC, 'total-hardness-water-sample-terms-caco', S + 'q9a-iii')
# Q9(a)(iv): the scheme prints its price inside the answer line, "(ANY THREE 5 + 2 + 2)".
_q9a4 = P.items(k('9', 'a', 'iv'))
assert len(_q9a4) == 1 and _q9a4[0].cell is None and _q9a4[0].text.endswith('(ANY THREE 5 + 2 + 2)'), _q9a4
_temp = [C.lifted('x', o, 5, '')['verbatim'] for o in (
    'boil water', 'filter water', 'repeat titration',
    'subtract (difference between) the two readings is temporary hardness')]
C.add([k('9', 'a', 'iv')], TOPIC, 'adapt-titration-temporary-hardness', [
    anyN('r-1', _temp[0], 9, 3, 5, _temp, 'Any three, (5 + 2 + 2).', steps=[5, 2, 2])], total=9)
C.ordered([k('9', 'b')], TOPIC, 'diagram-shows-ion-exchanger-makes-use')

# ── Q10 ────────────────────────────────────────────────────────────
# Q10(a) prints two asks: the steps of organic synthesis [4 + 3], and the three-step scheme with its reagents, each
# [3 × 3] ("DESCRIBE and IDENTIFY are linked"): one card each.
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == ['[4 + 3]', '[3 × 3]', '[3 × 3]'], _q10a
C.add([k('10', 'a')], TOPIC, 'steps-involved-organic-chemical-synthesis-using', pieces_of(_q10a[:1], k('10', 'a')),
      total=7)
C.add([k('10', 'a')], TOPIC, 'ethene-to-ethyl-ethanoate', pieces_of(_q10a[1:], k('10', 'a')), total=18,
      cid='q10-a-scheme', ref_suffix='reaction scheme')
# Q10(b) prints three asks under one letter: another application of mass spectrometry (4), the relative
# atomic mass of chromium (9) and the processes in sequence (12). One card each.
_q10b = P.items(k('10', 'b'))
assert [it.cell for it in _q10b] == ['[4]', '[9]', '[3]', '[3]', '[3]', '[4 × 3]'], _q10b
_apps = [C.lifted('x', o.strip(), 4, '')['verbatim'] for o in _q10b[0].text.split(' /') if o.strip() and o.strip() != 'etc.']
C.add([k('10', 'b')], TOPIC, 'mass-spectrometry-can-determine-isotopic-abundance', [
    anyN('r-1', _apps[0], 4, 1, 4, _apps, 'Any one application, (4); the scheme closes its list "etc.".')], total=4)
C.add([k('10', 'b')], TOPIC, 'relative-atomic-mass-of-chromium', [
    point('r-1', C._verbatim(_q10b[1].text, {}, k('10', 'b'))[0], 9,
          'The scheme prices the answer for the whole calculation (9) and sets out its working, with the marks for '
          'each step, in a form its text cannot carry; its own print is shown with the answer. It adds: Minus 1 if '
          'not rounded to 1 decimal place.')],
    total=9, cid='q10-b-calculation', ref_suffix='relative atomic mass', figure=S + 'q10b-calculation')
_steps = [C.lifted('x', o.strip(), 3, '')['verbatim'] for o in
          ('vaporisation of substance', 'ionisation (production of positive ions)', 'acceleration',
           'separation (deflection in magnetic field)', 'detection')]
C.add([k('10', 'b')], TOPIC, 'processes-in-a-mass-spectrometer', [
    anyN('r-1', _steps[0], 12, 4, 3, _steps, 'Any four, in sequence, (4 × 3). The scheme adds: [Sequence incorrect (–3).]')],
    total=12, cid='q10-b-processes', ref_suffix='processes in a mass spectrometer')
# Q10(c) prints three asks: the shapes possible for QX₂ [4 + 3], the shapes of NH₃ and CCl₄ predicted and explained
# (each [2 × 3], "PREDICT and EXPLAIN are linked"), and the more soluble of the two, justified ([3], [3]).
_q10c = P.items(k('10', 'c'))
assert [it.cell for it in _q10c] == ['[4 + 3]', '[2 × 3]', '[2 × 3]', '[3]', '[3]'], _q10c
C.add([k('10', 'c')], TOPIC, 'shapes-possible-molecule-formula-qx-use', pieces_of(_q10c[:1], k('10', 'c')), total=7)
C.add([k('10', 'c')], TOPIC, 'shapes-of-ammonia-and-tetrachloromethane', pieces_of(_q10c[1:3], k('10', 'c')),
      total=12, cid='q10-c-shapes', ref_suffix='shapes of NH₃ and CCl₄')
C.add([k('10', 'c')], TOPIC, 'solubility-of-ammonia-in-water', pieces_of(_q10c[3:], k('10', 'c')), total=6,
      cid='q10-c-solubility', ref_suffix='more soluble in water')

# ── Q11 ────────────────────────────────────────────────────────────
_q11a = P.items(k('11', 'a'))
assert [it.cell for it in _q11a] == ['[3]', '[6 + 3]', '[5 + 5 + 3]'], _q11a
C.add([k('11', 'a')], TOPIC, 'term-octane-number-molecular-characteristics-required', [
    point('r-1', C._verbatim(_q11a[0].text, {}, k('11', 'a'))[0], 3, ''),
    menu_of(k('11', 'a'), 1, 2, 'Any two, (6 + 3).'),
    menu_of(k('11', 'a'), 2, 3, 'Any three, (5 + 5 + 3).')], total=25)
C.answer_only([k('11', 'b')], TOPIC, 'reactant-in-excess-zinc-sulfuric-acid', S + 'q11b')
C.route([k('11', 'b', 'i')], TOPIC, 'mass-znso-produced')
C.route([k('11', 'b', 'ii')], TOPIC, 'mass-unused-reactant',
        fixes={'0.0031 – 0.0025 = 0.0006 moles zinc unused or': '0.0031 – 0.0025 = 0.0006 moles zinc unused'})
# Q11(c): the scheme sets (i) and (ii)'s equations on one row priced [6 + 3] and files (v)'s answer and
# working under (ii); each is placed with the part it answers.
_q11c1, _q11c2 = P.items(k('11', 'c', 'i')), P.items(k('11', 'c', 'ii'))
assert _q11c1[0].cell is None and [it.cell for it in _q11c2] == ['[6 + 3]', '[4]', '[2]', '[2]'], (_q11c1, _q11c2)
C.add([k('11', 'c', 'i'), k('11', 'c', 'ii')], TOPIC, 'hcl-strong-acid', [
    C.lifted('r-1', 'HCl + H₂O → Cl⁻ + H₃O⁺ / HCl → H⁺ + Cl‐', 6, 'The scheme prices the two equations [6 + 3], in order.'),
    C.lifted('r-2', 'HCN + H₂O ⇌ CN⁻ + H₃O⁺ / HCN ⇌ H⁺ + CN‐', 3, '')], total=9)
C.fixed([k('11', 'c', 'iii')], TOPIC, 'species-acting-bases-equilibrium-hcl-aq')
C.route([k('11', 'c', 'iv')], TOPIC, 'ph-tfr-solution-oh-ion-concentration',
        fixes={'[H₃O⁺] = 1.0 × 10⁻¹⁴ \uf0b8 0.04 = 2.50 × 10⁻¹³': '[H₃O⁺] = 1.0 × 10⁻¹⁴ ÷ 0.04 = 2.50 × 10⁻¹³'})
C.add([k('11', 'c', 'v')], TOPIC, 'concentration-h3o-ion-alloy-wheel-cleaner', [
    point('r-1', C._verbatim(_q11c2[2].text, {}, k('11', 'c', 'v'))[0], 2,
          'The scheme gives the answer, [H₃O⁺] = 0.063 moles per litre, priced [4], then the working that earns '
          'it, step by step.'),
    point('r-2', C._verbatim(_q11c2[3].text, {}, k('11', 'c', 'v'))[0], 2, '')], total=4)
C.menu([ka('11', 'd', 'i', 'A')], TOPIC, 'issues')
C.ordered([ka('11', 'd', 'ii', 'A')], TOPIC, 'chemical-formulae-oxides-oxide-nitrogen-oxide')
C.menu([ka('11', 'd', 'iii', 'A')], TOPIC, 'each-oxides-enters-atmosphere')
C.fixed([ka('11', 'd', 'iv', 'A')], TOPIC, 'measure-been-taken-reduce-release-oxides')
C.fixed([ka('11', 'd', None, 'B')], TOPIC, 'aluminium-corrodes-more-slowly-than-iron')
C.fixed([ka('11', 'd', 'i', 'B')], TOPIC, 'suitable-material-anode-cathode')
C.fixed([ka('11', 'd', 'ii', 'B')], TOPIC, 'equations-reactions-take-place-anode-cathode')
C.fixed([ka('11', 'd', 'iii', 'B')], TOPIC, 'feature-process-reduces-cost-producing-aluminium')



# ── The paper's pictures ─────────────────────────────────────────────────────────
# Each card shows the figure its ask reads from (chemistry/crops/2022-hl-deferred.json). Where the card's
# own figure is already the scheme's answer (a drawn graph, a worked calculation), the paper's figure is
# its question figure instead, shown beside the printed ask (questionFigureIncludesPrompt: False).
_ids = {c['id'][len(C.prefix):]: c for c in C.cards}
PAPER_FIGURES = {
    'q2-a-i-ii': 'paper-q2',                      # the structure of eugenol it copies
    'q2-c': 'paper-q2-funnel', 'q2-d-i': 'paper-q2-funnel', 'q2-d-ii': 'paper-q2-funnel',
    'q3-c': 'paper-q3', 'q3-d-i': 'paper-q3', 'q3-d-ii': 'paper-q3', 'q3-e': 'paper-q3',   # the results table
    'q4-j-i-ii': 'paper-q4j',                     # the photographs of nettles and almonds
    'q8-c-i': 'paper-q8c', 'q8-c-ii': 'paper-q8c', 'q8-c-iii': 'paper-q8c',
    'q5-b-ii': 'paper-q5b-ii-eq',                 # the nuclear equation, set with its numbers above and below
    'q9-b': 'paper-q9b',
    'q10-b-calculation': 'paper-q10b',            # the isotopes' abundances
    'q11-d-b-i': 'paper-q11d-b', 'q11-d-b-ii': 'paper-q11d-b',
}
# A letter that prints several asks and is carded as one card per ask: each card's question is its own
# printed ask, lifted from the paper's lines (by index, asserted), and its stem the lines it reads from.
def paper_lines(key, *spans):
    seg = [x for x in P.pseg if x.key == key]
    assert len(seg) == 1, key
    lines = seg[0].text
    return tidy(' '.join(display(lines[i].text) for lo, hi in spans for i in range(lo, hi)))


_Q6, _Q6C, _Q10B = k('6'), k('6', 'c'), k('10', 'b')
assert paper_lines(_Q6C, (5, 6)).startswith('Draw a clearly labelled reaction profile') \
    and paper_lines(_Q10B, (7, 9)).endswith('the operation of a mass spectrometer?') \
    and paper_lines(k('11', 'b'), (4, 5)) == 'Determine which is the limiting reactant.' \
    and paper_lines(ka('11', 'd', None, 'B'), (3, 4)) == 'Why is this the case?' \
    and paper_lines(k('10', 'a'), (3, 4)).startswith('Identify, where appropriate') \
    and paper_lines(k('10', 'c'), (6, 7)) == 'Justify your answer.'
_Q6_STEM = C.context(_Q6C)
QUESTIONS = {   # card -> (stem, question)
    'q6-c': (_Q6_STEM, paper_lines(_Q6C, (0, 5))),
    'q6-c-profile': (tidy(_Q6_STEM + ' ' + paper_lines(_Q6C, (0, 3))), paper_lines(_Q6C, (5, 6))),
    'q6-c-bioethanol': (_Q6_STEM, paper_lines(_Q6C, (6, 7))),
    'q10-b': ('', paper_lines(_Q10B, (0, 3))),
    'q10-b-calculation': (paper_lines(_Q10B, (0, 2), (3, 5)), paper_lines(_Q10B, (5, 7))),
    'q10-b-processes': (paper_lines(_Q10B, (0, 2)), paper_lines(_Q10B, (7, 9))),
    'q11-b': (paper_lines(k('11', 'b'), (0, 4)), paper_lines(k('11', 'b'), (4, 5))),
    'q10-a': ('', paper_lines(k('10', 'a'), (0, 1))),
    'q10-a-scheme': ('', paper_lines(k('10', 'a'), (1, 4))),
    'q10-c': ('', paper_lines(k('10', 'c'), (0, 1))),
    'q10-c-shapes': ('', paper_lines(k('10', 'c'), (1, 4))),
    'q10-c-solubility': ('', paper_lines(k('10', 'c'), (4, 7))),
    'q11-d-b': (C.context(ka('11', 'd', None, 'B')), paper_lines(ka('11', 'd', None, 'B'), (0, 4))),
}
for _cid, (_stem, _q) in QUESTIONS.items():
    _ids[_cid]['stem'], _ids[_cid]['questionText'] = _stem, _q
# Asks about a term the paper underlines, which no text layer carries: the paper's own print is the
# card's question.
PRINTS = {'q2-b': 'paper-q2b-print', 'q8-a': 'paper-q8a-print'}
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
# authored/chemistry.json: 82 of 86 agreed; the four they split on follow June's majority for that kind of
# ask (Q2(f) a percentage-yield calculation, chem-1-4 as 6 of June's 7; Q6(c)'s reaction profile, chem-3-2 as
# all 4; Q6(c)'s bioethanol and Q6(d)'s hydrogen as fuels, chem-2-4 as 4 of 5 and 4 of 7). Q10(a) and Q10(c),
# later split one card per printed ask (the six-row cap), keep the topic both readers gave the whole letter.
REVIEWED = {
    'q1-a': ('chem-4-1', 'transferring-all-solution-to-volumetric-flask'),
    'q1-b': ('chem-4-1', 'rinsing-and-filling-the-burette'),
    'q1-c': ('chem-4-1', 'excess-acid-in-manganate-titration'),
    'q1-d': ('chem-4-1', 'manganate-titration-end-point'),
    'q1-e-i': ('chem-4-1', 'iron-ii-concentration-from-titre'),
    'q1-e-ii': ('chem-4-1', 'mass-of-iron-ii-in-crystals'),
    'q1-e-iii': ('chem-4-1', 'percentage-iron-in-ammonium-iron-sulfate'),
    'q2-a-i-ii': ('chem-4-2', 'eugenol-tetrahedral-carbon-and-double-bond'),
    'q2-b': ('chem-u2', 'clove-oil-emulsion-and-distillate-appearance'),
    'q2-c': ('chem-u2', 'solvent-choice-for-liquid-liquid-extraction'),
    'q2-d-i': ('chem-u2', 'several-small-extractions-improve-yield'),
    'q2-d-ii': ('chem-u2', 'venting-the-separating-funnel'),
    'q2-e': ('chem-u2', 'evaporating-solvent-to-isolate-clove-oil'),
    'q2-f': ('chem-1-4', 'volume-of-clove-oil-from-yield'),
    'q2-g': ('chem-u3', 'commercial-use-of-clove-oil'),
    'q3-a': ('chem-u2', 'apparatus-for-collecting-oxygen-from-peroxide'),
    'q3-b': ('chem-3-2', 'manganese-dioxide-heterogeneous-catalysis'),
    'q3-c': ('chem-3-2', 'plotting-oxygen-volume-against-time'),
    'q3-d-i': ('chem-3-2', 'time-to-produce-moles-of-oxygen'),
    'q3-d-ii': ('chem-3-2', 'instantaneous-rate-from-a-tangent'),
    'q3-e': ('chem-3-2', 'curve-for-half-the-peroxide-concentration'),
    'q4-a': ('chem-1-3', 'how-mendeleev-arranged-the-elements'),
    'q4-b-i-ii': ('chem-1-2', 'atomic-and-mass-number-from-ion'),
    'q4-c-i-ii': ('chem-3-5', 'oxidation-numbers-of-sulfur'),
    'q4-d': ('chem-1-4', 'atoms-in-gas-volume-at-stp'),
    'q4-e': ('chem-2-3', 'conditions-for-near-ideal-gas-behaviour'),
    'q4-f': ('chem-1-4', 'molarity-of-percent-w-v-solution'),
    'q4-g': ('chem-2-3', 'avogadros-law'),
    'q4-h-i-ii': ('chem-2-4', 'structures-of-dimethylpropane-and-ethylbenzene'),
    'q4-i': ('chem-u2', 'principle-of-chromatography'),
    'q4-j-i-ii': ('chem-4-2', 'compounds-in-nettles-and-almonds'),
    'q4-k-i-ii': ('chem-1-4', 'formulae-of-silicon-and-manganese-compounds'),
    'q4-l-a': ('chem-4-3', 'nitrogen-fixation-by-lightning'),
    'q4-l-b': ('chem-3-5', 'how-a-sacrificial-anode-protects'),
    'q5-a-i': ('chem-1-2', 'stoney-named-the-electron'),
    'q5-a-ii': ('chem-1-2', 'thomson-and-millikan-on-electrons'),
    'q5-a-iii': ('chem-1-2', 'electron-configuration-of-copper'),
    'q5-a-iv': ('chem-1-2', 'nitrogen-2p-orbitals-singly-occupied'),
    'q5-b-i': ('chem-1-2', 'beta-radiation-and-penetrating-power'),
    'q5-b-ii': ('chem-1-2', 'beta-decay-of-carbon-14'),
    'q6-a': ('chem-3-1', 'heat-of-combustion-and-bomb-calorimeter'),
    'q6-b': ('chem-3-1', 'use-of-kilogram-calorific-values'),
    'q6-c': ('chem-3-1', 'heat-of-combustion-of-ethanol'),
    'q6-c-profile': ('chem-3-2', 'exothermic-reaction-profile-diagram'),
    'q6-c-bioethanol': ('chem-2-4', 'bioethanol-as-renewable-motor-fuel'),
    'q6-d': ('chem-2-4', 'steam-reforming-and-hydrogen-as-fuel'),
    'q7-a': ('chem-3-3', 'le-chateliers-principle'),
    'q7-b': ('chem-3-3', 'optimum-conditions-for-ammonia-yield'),
    'q7-c': ('chem-3-3', 'why-optimum-conditions-are-uneconomical'),
    'q7-d': ('chem-3-3', 'kc-expression-for-ammonia-synthesis'),
    'q7-e': ('chem-3-3', 'kc-from-equilibrium-masses'),
    'q7-f-i': ('chem-3-3', 'temperature-rise-lowers-kc'),
    'q7-f-ii': ('chem-3-3', 'catalyst-does-not-change-kc'),
    'q8-a': ('chem-2-4', 'unsaturated-hydrocarbon-meaning'),
    'q8-b': ('chem-2-4', 'alkene-versus-alkyne-structure'),
    'q8-c-i': ('chem-2-4', 'equation-for-preparing-ethyne'),
    'q8-c-ii': ('chem-2-4', 'test-for-unsaturation-in-ethyne'),
    'q8-c-iii': ('chem-2-4', 'large-scale-use-of-ethyne'),
    'q8-d-i-iii': ('chem-4-2', 'classifying-addition-elimination-substitution'),
    'q8-e': ('chem-4-2', 'monochlorination-of-methane-mechanism'),
    'q9-a-i': ('chem-4-1', 'full-name-of-edta'),
    'q9-a-ii': ('chem-4-1', 'buffer-and-indicator-in-edta-titration'),
    'q9-a-iii': ('chem-4-1', 'total-hardness-in-ppm-caco3'),
    'q9-a-iv': ('chem-4-3', 'boiling-to-measure-temporary-hardness'),
    'q9-b': ('chem-4-3', 'deionising-with-ion-exchange-resins'),
    'q10-a': ('chem-4-2', 'steps-of-organic-synthesis'),
    'q10-a-scheme': ('chem-4-2', 'synthesis-of-ethyl-ethanoate-from-ethene'),
    'q10-b': ('chem-1-2', 'another-application-of-mass-spectrometry'),
    'q10-b-calculation': ('chem-1-2', 'relative-atomic-mass-of-chromium'),
    'q10-b-processes': ('chem-1-2', 'processes-in-a-mass-spectrometer'),
    'q10-c': ('chem-2-2', 'shapes-possible-for-qx2'),
    'q10-c-shapes': ('chem-2-2', 'vsepr-shapes-of-ammonia-and-ccl4'),
    'q10-c-solubility': ('chem-2-2', 'solubility-of-ammonia-in-water'),
    'q11-a': ('chem-2-4', 'octane-number-and-raising-it'),
    'q11-b': ('chem-1-4', 'limiting-reactant-zinc-and-sulfuric-acid'),
    'q11-b-i': ('chem-1-4', 'mass-of-zinc-sulfate-produced'),
    'q11-b-ii': ('chem-1-4', 'mass-of-unused-zinc'),
    'q11-c-i-ii': ('chem-3-4', 'dissociation-of-strong-and-weak-acids'),
    'q11-c-iii': ('chem-3-4', 'bronsted-lowry-bases-in-an-equilibrium'),
    'q11-c-iv': ('chem-3-4', 'ph-from-hydroxide-ion-concentration'),
    'q11-c-v': ('chem-3-4', 'hydronium-concentration-from-ph'),
    'q11-d-a-i': ('chem-4-3', 'environmental-issues-from-acidic-oxides'),
    'q11-d-a-ii': ('chem-4-3', 'formulae-of-acid-rain-oxides'),
    'q11-d-a-iii': ('chem-4-3', 'sources-of-nitrogen-and-sulfur-oxides'),
    'q11-d-a-iv': ('chem-4-3', 'reducing-emissions-of-acidic-oxides'),
    'q11-d-b': ('chem-3-5', 'why-aluminium-corrodes-slower-than-iron'),
    'q11-d-b-i': ('chem-3-5', 'electrode-material-for-aluminium-extraction'),
    'q11-d-b-ii': ('chem-3-5', 'electrode-equations-for-aluminium-extraction'),
    'q11-d-b-iii': ('chem-u3', 'lowering-the-cost-of-aluminium-production'),
}
assert set(REVIEWED) == set(_ids), set(REVIEWED) ^ set(_ids)
for _cid, (_topic, _concept) in REVIEWED.items():
    _ids[_cid]['topicId'], _ids[_cid]['conceptId'] = _topic, _concept


# Printed errors in the scheme's own print, said in plain words on the card's first row (CARD-STANDARD 10f), so a
# student reading the scheme's crop is told which figure is wrong.
SCHEME_ERRORS = {
    'q9-a-iii': 'A misprint in the scheme: its second method gives "M = 0.308 M", but its own next line works with '
                '0.00308 moles per litre, the molarity the first method finds.',
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
