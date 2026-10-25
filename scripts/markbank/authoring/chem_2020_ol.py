#!/usr/bin/env python3
"""2020 Ordinary Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2020_ol.py          # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2020_ol.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2020 ol

No 2020 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell.

The paper underlines the term a part asks about in Q5(a), Q6(a), Q11(b)(i)
and Q11(c)A(i), which no text layer carries: those take the paper's own
print as their question. Q4(k) and Q11(c) offer whole alternative parts A
and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, anyN, display, point  # noqa: E402

P = Printed(2020, 'ol', figures=True)
C = Cards(P)
FIG = 'chemistry-2020-OL-'
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


def pair_or(key):
    """Two points with a second pair the scheme sets after "or"."""
    its = P.items(key)
    t = its[0].text
    first, second = t.split(' state where concentrations')
    second = 'state where concentrations' + second
    pts = [x.strip() for x in first.split('//')]
    assert len(pts) == 2, pts
    return pts, second


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Tests on organic chemicals ────────────────────────────────────────────
Q1A = FIG + 'paper-q1a'
C.fixed([k('1', 'a', 'i')], 'chem-u2', 'colour-of-bromine-solution', figure=Q1A)
C.fixed([k('1', 'a', 'ii')], 'chem-2-4', 'test-for-unsaturation-with-bromine', figure=Q1A)
C.fixed([k('1', 'a', 'iii')], 'chem-2-4', 'meaning-of-unsaturated-hydrocarbon', figure=Q1A)
C.fixed([k('1', 'b', 'i')], 'chem-u2', 'combustion-test-on-ethyne')
C.fixed([k('1', 'b', 'ii')], 'chem-2-4', 'flame-of-burning-ethyne')
Q1C = FIG + 'paper-q1c-table'
C.fixed([k('1', 'c', 'i')], 'chem-u2', 'purer-batch-from-melting-points', figure=Q1C)
C.fixed([k('1', 'c', 'ii')], 'chem-u2', 'melting-point-range-and-purity', figure=Q1C)
C.fixed([k('1', 'c', 'iii')], 'chem-u2', 'recrystallisation', figure=Q1C)
_q1d = P.items(k('1', 'd'))
assert [it.cell for it in _q1d] == ['[3 + 2 + 2 + 2]'], _q1d
_m = ['A: soap', 'B: clove oil', 'C: ethanoic acid', 'D: ethanal']
assert display(_q1d[0].text) == ' '.join(_m), _q1d[0].text
C.add([k('1', 'd')], 'chem-4-2', 'identifying-four-substances-by-tests', [
    C.lifted(f'r-{i + 1}', t, None, 'The scheme adds: ' + ' '.join(_q1d[0].asides) if i == 3 else '')
    for i, t in enumerate(_m)],
    kind='orderedSplit', notation='[3 + 2 + 2 + 2]', total=9, figure=FIG + 'paper-q1d-table',
    notes=SPLIT.format('[3 + 2 + 2 + 2]'))

# ── Q2 A standard solution and a titration ───────────────────────────────────
Q2 = FIG + 'paper-q2'
Q2T = FIG + 'paper-q2-table'
C.fixed([k('2', 'a', 'i')], 'chem-4-1', 'volumetric-flask', figure=Q2)
C.ordered([k('2', 'a', 'ii')], 'chem-4-1', 'transferring-a-solid-to-a-volumetric-flask', figure=Q2)
C.fixed([k('2', 'b')], 'chem-4-1', 'burette-adds-the-acid', figure=Q2)
C.fixed([k('2', 'c', 'i')], 'chem-4-1', 'indicator-for-a-carbonate-titration', figure=Q2)
C.fixed([k('2', 'c', 'ii')], 'chem-4-1', 'colour-change-of-methyl-orange-at-end-point', figure=Q2)
C.fixed([k('2', 'd', 'i')], 'chem-4-1', 'why-a-further-titration', figure=Q2T)
C.fixed([k('2', 'd', 'ii')], 'chem-4-1', 'choosing-concordant-titres', figure=Q2T)
C.fixed([k('2', 'd', 'iii')], 'chem-4-1', 'average-titre', figure=Q2T)
C.answer_only([k('2', 'd', 'iv')], 'chem-4-1', 'concentration-of-hydrochloric-acid', S + 'q2d-iv')

# ── Q3 The decomposition of hydrogen peroxide ────────────────────────────────
Q3 = FIG + 'paper-q3'
Q3T = FIG + 'paper-q3-table'
Q3A = P.rearranged(C.context(k('3', 'a', 'i')), 'catalyst 2H₂O₂ → 2H₂O + O₂',
                   '2H₂O₂ → 2H₂O + O₂ catalyst')
C.fixed([k('3', 'a', 'i')], 'chem-3-2', 'a-catalyst-for-hydrogen-peroxide', figure=Q3, stem=Q3A)
C.fixed([k('3', 'a', 'ii')], 'chem-3-2', 'appearance-of-the-catalyst', figure=Q3, stem=Q3A)
Q3B = FIG + 'paper-q3b'
C.fixed([k('3', 'b', 'i')], 'chem-u2', 'oxidising-hazard-pictogram', figure=Q3B)
C.fixed([k('3', 'b', 'ii')], 'chem-u2', 'handling-hydrogen-peroxide', figure=Q3B)
C.fixed([k('3', 'c')], 'chem-u2', 'starting-the-reaction-and-timer-together', figure=Q3)
C.fixed([k('3', 'd')], 'chem-3-2', 'graph-of-oxygen-volume-against-time', figure=S + 'q3d')
print_question('paper-q3d-print')
C.fixed([k('3', 'e', 'i')], 'chem-3-2', 'volume-from-the-graph-early', figure=Q3T)
C.fixed([k('3', 'e', 'ii')], 'chem-3-2', 'why-the-rate-falls', figure=Q3T)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.fixed([k('4', 'a')], 'chem-1-3', 'properties-of-group-1-metals', notes=Q4_NOTE)
C.fixed([k('4', 'b')], 'chem-1-3', 'the-noble-gases', notes=Q4_NOTE)
_q4c = [P.items(k('4', 'c', r)) for r in ('i', 'ii')]
assert [it.cell for it in _q4c[0]] == [None] and [it.cell for it in _q4c[1]] == ['[2 × 3]'], _q4c
C.add([k('4', 'c', 'i'), k('4', 'c', 'ii')], 'chem-1-2', 'flame-colours-of-sodium-and-copper', [
    C.lifted('r-1', display(_q4c[0][0].text).rstrip('/ '), 3,
             'For (i). The scheme prices these points (2 × 3), one each.'),
    C.lifted('r-2', _q4c[1][0].text, 3, 'For (ii). The scheme adds: ' + ' '.join(_q4c[1][0].asides))],
    notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-3-5', 'gases-from-electrolysing-acidified-water', notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-1-4', 'formula-of-silicon-hydride', notes=Q4_NOTE)
C.fixed([k('4', 'f')], 'chem-4-3', 'chlorine-in-swimming-pools', notes=Q4_NOTE)
C.fixed([k('4', 'g')], 'chem-3-1', 'definition-of-heat-of-combustion', notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-2-4', 'why-catalytic-cracking', notes=Q4_NOTE)
_q4i = P.items(k('4', 'i'))
assert [it.cell for it in _q4i] == ['[6]', '[3]', '[3]'], _q4i
C.add([k('4', 'i')], 'chem-1-4', 'percentage-of-silicon-in-silica', [
    C.lifted('r-1', _q4i[1].text, 3),
    C.lifted('r-2', '% Si = 28 ÷ 60 × 100 = 47%', 3,
             FRACTION.format('28', '60') + ' The scheme adds: ' + ' '.join(_q4i[2].asides))],
    notes='The scheme gives the answer, 47%, priced [6], then the working that earns it, step by '
          'step. ' + Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-4-2', 'chromatography', notes=Q4_NOTE)
C.menu([ka('4', 'k', None, 'A')], 'chem-u3', 'siting-a-chemical-factory', notes=Q4_NOTE)
C.menu([ka('4', 'k', None, 'B')], 'chem-1-3', 'how-metals-differ-from-non-metals', notes=Q4_NOTE)

# ── Q5 Carbon and its isotopes ───────────────────────────────────────────────
Q5 = FIG + 'paper-q5-table'
C.fixed([k('5', 'a')], 'chem-1-2', 'definition-of-atomic-number', figure=Q5)
print_question('paper-q5a-print')
C.ordered([k('5', 'b', 'i'), k('5', 'b', 'ii'), k('5', 'b', 'iii')], 'chem-1-2',
          'where-the-particles-of-an-atom-are', figure=Q5)
C.fixed([k('5', 'b', 'iv')], 'chem-1-2', 'why-mass-is-in-the-nucleus', figure=Q5)
C.fixed([k('5', 'b', 'v')], 'chem-1-2', 'why-atoms-are-neutral', figure=Q5)
C.fixed([k('5', 'c', 'i')], 'chem-1-2', 'definition-of-isotopes', figure=Q5)
_q5c = [P.items(k('5', 'c', r)) for r in ('ii', 'iii')]
assert [it.cell for it in _q5c[0]] == [None] and [it.cell for it in _q5c[1]] == ['[2 × 3]'], _q5c
C.add([k('5', 'c', 'ii'), k('5', 'c', 'iii')], 'chem-1-2', 'neutrons-in-carbon-isotopes', [
    C.lifted('r-1', display(_q5c[0][0].text).rstrip('/ '), 3,
             'For (ii). The scheme prices these points (2 × 3), one each.'),
    C.lifted('r-2', _q5c[1][0].text, 3, 'For (iii).')], figure=Q5)
C.fixed([k('5', 'd')], 'chem-1-2', 'a-type-of-radiation', figure=Q5)
C.fixed([k('5', 'e', 'i')], 'chem-1-2', 'relative-atomic-mass-of-carbon', figure=Q5)
C.fixed([k('5', 'e', 'ii')], 'chem-1-2', 'why-carbon-is-not-exactly-12', figure=Q5)

# ── Q6 Fuels ─────────────────────────────────────────────────────────────────
C.fixed([k('6', 'a')], 'chem-3-1', 'meaning-of-exothermic')
print_question('paper-q6a-print')
_q6b = [P.items(k('6', 'b', r)) for r in ('i', 'ii', 'iii')]
assert [it.cell for it in _q6b[2]] == ['[3 × 3]'], _q6b
C.add([k('6', 'b', 'i'), k('6', 'b', 'ii'), k('6', 'b', 'iii')], 'chem-2-4', 'uses-of-fuels', [
    C.lifted('r-1', _q6b[0][0].text, 3, 'For (i). The scheme prices these points (3 × 3), one each.'),
    C.lifted('r-2', _q6b[1][0].text, 3, 'For (ii).'),
    C.lifted('r-3', _q6b[2][0].text, 3, 'For (iii).')])
_q6c = [P.items(k('6', 'c', r)) for r in ('i', 'ii', 'iii', 'iv')]
assert [it.cell for it in _q6c[3]] == ['[6 + 6 + 3 + 3]'], _q6c
C.add([k('6', 'c', 'i'), k('6', 'c', 'ii'), k('6', 'c', 'iii'), k('6', 'c', 'iv')], 'chem-2-4',
      'methane-name-shape-series-and-mercaptans', [
          C.lifted('r-1', _q6c[0][0].text, None, 'For (i).'),
          C.lifted('r-2', display(_q6c[1][0].text).rstrip('/ '), None,
                   'For (ii). The scheme also draws the tetrahedral molecule; its own print is shown '
                   'with the answer.'),
          C.lifted('r-3', _q6c[2][0].text, None, 'For (iii).'),
          C.lifted('r-4', _q6c[3][0].text, None, 'For (iv).')],
      kind='orderedSplit', notation='[6 + 6 + 3 + 3]', total=18, figure=S + 'q6c',
      notes=SPLIT.format('[6 + 6 + 3 + 3]'))
C.fixed([k('6', 'c', 'v')], 'chem-3-1', 'combustion-of-methane')
C.drawn([k('6', 'd', 'i')], 'chem-2-4', 'structure-of-propane', S + 'q6d-i')
C.fixed([k('6', 'd', 'ii')], 'chem-2-4', 'butane-in-lpg')

# ── Q7 Bases, pH and hard water ──────────────────────────────────────────────
Q7T = FIG + 'paper-q7-table'
_q7a = P.items(k('7', 'a'))
assert [it.cell for it in _q7a] == ['[2 × 3]', '[6]'], _q7a
_pa = _q7a[0].points()
C.add([k('7', 'a')], 'chem-3-4', 'definition-of-a-base', [
    C.lifted('r-1', _pa[0], 3, 'The scheme prices this point and the next (2 × 3), one each, or '
             'instead (6) for "' + _q7a[1].text + '". It adds: ' + ' '.join(_q7a[1].asides)),
    C.lifted('r-2', _pa[1], 3)])
_q7b = P.items(k('7', 'b'))
assert [it.cell for it in _q7b] == ['[2 × 3]', '[6]', '[3]', '[3]'], _q7b
_pb = _q7b[0].points()
C.add([k('7', 'b')], 'chem-3-4', 'definition-of-ph-and-ph-of-a-base', [
    C.lifted('r-1', _pb[0], 3, 'The scheme prices this point and the next (2 × 3), one each.'),
    C.lifted('r-2', _pb[1], 3),
    C.lifted('r-3', _q7b[2].text, 3, 'The scheme gives the answer, 12.7, priced (6), then this step '
             'and the next, (3) each.'),
    C.lifted('r-4', _q7b[3].text, 3, 'The scheme adds: ' + ' '.join(_q7b[3].asides))])
_q7c = P.items(k('7', 'c'))
assert [it.cell for it in _q7c] == ['[2 × 3]'], _q7c
_t = _q7c[0].text
_cut = _t.index(' contains dissolved')
_pc = [x.strip() for x in _t[:_cut].split('//')]
assert len(_pc) == 2, _pc
C.add([k('7', 'c')], 'chem-4-3', 'what-hard-water-is', [
    C.lifted('r-1', _pc[0], 3, 'The scheme prices this point and the next (2 × 3), one each, or '
             'instead the pair "' + _t[_cut:].strip() + '".'),
    C.lifted('r-2', _pc[1], 3)])
for r, concept, topic in (('i', 'acidic-or-basic-from-ph', 'chem-3-4'),
                          ('ii', 'label-evidence-of-hardness', 'chem-4-3'),
                          ('iii', 'label-evidence-of-temporary-hardness', 'chem-4-3'),
                          ('iv', 'test-for-sulfate-ion', 'chem-u2'),
                          ('v', 'advantage-of-mineral-water', 'chem-4-3')):
    C.fixed([k('7', 'd', r)], topic, concept, figure=Q7T)

# ── Q8 Organic compounds A to F ──────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
for r, concept in (('i', 'naming-ethanol-ethanal-and-ethanoic-acid'), ('ii', 'the-alcohols-in-the-table'),
                   ('iii', 'solubility-of-ethene'), ('iv', 'monomer-of-polythene'),
                   ('v', 'an-aromatic-compound')):
    C.fixed([k('8', 'a', r)], 'chem-4-2', concept, figure=Q8)
C.fixed([k('8', 'b', 'i')], 'chem-4-2', 'what-an-enzyme-is', figure=Q8)
C.fixed([k('8', 'b', 'ii')], 'chem-4-2', 'oxidation-reactions-in-the-table', figure=Q8)
C.ordered([k('8', 'c', 'i'), k('8', 'c', 'ii')], 'chem-u2', 'preparing-ethene-from-ethanol',
          figure=S + 'q8c')

# ── Q9 Electrons, redox and ionic substances ─────────────────────────────────
_q9a = [P.items(k('9', 'a', r)) for r in ('i', 'ii')]
assert [it.cell for it in _q9a[1]] == ['[2 × 6]', None], _q9a
C.add([k('9', 'a', 'i'), k('9', 'a', 'ii')], 'chem-1-2', 'electrons-in-main-energy-levels', [
    C.lifted('r-1', _q9a[0][0].text, 6, 'For (i). The scheme prices these points (2 × 6), one each. '
             'It adds: ' + ' '.join(_q9a[0][0].asides)),
    C.lifted('r-2', _q9a[1][0].text, 6, 'For (ii). The scheme adds: ' + ' '.join(_q9a[1][0].asides)
             + ' ' + _q9a[1][1].text)])
_q9b = P.ask(k('9', 'b'))
_q9b12 = [P.items(k('9', 'b', r)) for r in ('i', 'ii')]
C.add([k('9', 'b', 'i'), k('9', 'b', 'ii')], 'chem-3-5', 'oxidation-and-reduction-by-electrons', [
    C.lifted('r-1', _q9b12[0][0].text, 6, 'For (i). The scheme prices these points (2 × 6), one each.'),
    C.lifted('r-2', _q9b12[1][0].text, 6, 'For (ii).' + (
        ' The scheme adds: ' + ' '.join(a for it in _q9b12[1] for a in it.asides)
        if any(it.asides for it in _q9b12[1]) else ''))],
    qtext=_q9b, cid='q9-b-i-ii', stem=P.ask(k('9')))
C.fixed([k('9', 'c', 'i')], 'chem-3-5', 'element-reduced-when-magnesium-burns')
C.fixed([k('9', 'c', 'ii')], 'chem-3-5', 'the-reducing-agent')
_q9c3 = P.items(k('9', 'c', 'iii'))
assert [it.cell for it in _q9c3] == ['[6 + 3]'], _q9c3
_props = [C.lifted('x', o.strip(), None)['verbatim'] for o in _q9c3[0].text.split(' / ')]
C.add([k('9', 'c', 'iii')], 'chem-2-1', 'properties-of-ionic-substances', [anyN(
    'r-1', _props[0], 9, 2, 6, _props, 'Any two of these, the first (6) and the second (3).',
    steps=[6, 3])], total=9)
C.fixed([k('9', 'd')], 'chem-3-5', 'magnesium-oxidised-more-easily-than-copper')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == ['[7 × 3]'], _q10a
_words = [x.strip() for x in display(_q10a[0].text).rsplit(' 4 +', 1)[0].split('//')]
assert len(_words) == 8, _words
C.add([k('10', 'a')], 'chem-4-3', 'stages-of-sewage-treatment', [
    C.lifted(f'r-{i + 1}', w, None) for i, w in enumerate(_words)],
    kind='orderedSplit', notation='[4 + (7 × 3)]', total=25,
    notes='The scheme prices these points together as [4 + (7 × 3)] without saying which point earns '
          'the 4, so no per-point value is shown.')
C.ordered([k('10', 'b', 'i'), k('10', 'b', 'ii')], 'chem-1-1', 'particles-in-a-gas')
# (b)'s lead-in asks (i) and (ii); (iii) stands on its own.
C.fixed([k('10', 'b', 'iii')], 'chem-2-3', 'diffusion', figure=FIG + 'paper-q10b-iii', stem='')
C.answer_only([k('10', 'b', 'iv')], 'chem-2-3', 'volume-from-the-combined-gas-law', S + 'q10b-iv')
print_question('paper-q10b-iv-print')
_q10b5 = P.items(k('10', 'b', 'v'))
assert [it.cell for it in _q10b5] == ['[6 + 3]'], _q10b5
C.add([k('10', 'b', 'v')], 'chem-2-3', 'a-gas-law-named-and-stated', [
    C.lifted('r-1', 'Boyle / Charles / Gay-Lussac of pressure / Ideal Gas Law (Equation of State of an '
                    'Ideal Gas)', None),
    C.lifted('r-2', 'Boyle: pressure and volume inversely proportional at constant temperature', None,
             'Or Charles: temperature and volume directly proportional at constant pressure, or '
             'Gay-Lussac: temperature and pressure directly proportional at constant volume, or Ideal '
             'Gas Law: pV = nRT, each with its formula forms; its own print is shown with the answer. '
             'The scheme adds: ' + ' '.join(_q10b5[0].asides))],
    kind='orderedSplit', notation='[6 + 3]', total=9, figure=S + 'q10b-v',
    notes=SPLIT.format('[6 + 3]'))
print_question('paper-q10b-v-print')
_q10c1 = P.items(k('10', 'c', 'i'))
assert [it.cell for it in _q10c1] == ['[3]', '[6]', '[6]'], _q10c1
C.add([k('10', 'c', 'i')], 'chem-1-4', 'moles-of-glucose', [
    C.lifted('r-1', _q10c1[0].text, 3),
    C.lifted('r-2', _q10c1[1].text, 6, 'The scheme sets out the working, n = m over Mr = 18.0 over 180 '
             '= 0.1 moles glucose, priced (6); its own print is shown with the answer.')],
    figure=S + 'q10c-i')
_q10c2 = P.items(k('10', 'c', 'ii'))
assert [it.cell for it in _q10c2] == ['[3]', '[3]', '[3]', '[3]', '[3]'], _q10c2
C.add([k('10', 'c', 'ii')], 'chem-1-4', 'moles-and-volume-of-oxygen', [
    C.lifted('r-1', _q10c2[0].text, 3),
    C.lifted('r-2', _q10c2[1].text, 3, 'Or its working, "' + display(_q10c2[2].text) + '" (3).'),
    C.lifted('r-3', _q10c2[3].text, 3, 'Or its working, "' + display(_q10c2[4].text) + '" (3).')])
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'mass-of-carbon-dioxide-used')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
C.fixed([k('11', 'a', 'i')], 'chem-2-1', 'dot-and-cross-diagram-of-ammonia', figure=S + 'q11a-i',
        row_notes={0: 'The scheme draws the molecule two ways; its own print is shown with the answer.'})
C.fixed([k('11', 'a', 'ii')], 'chem-2-1', 'definition-of-electronegativity')
C.fixed([k('11', 'a', 'iii')], 'chem-2-1', 'polarity-of-bonds-in-ammonia')
C.fixed([k('11', 'a', 'iv')], 'chem-2-2', 'solubility-of-ammonia')
_pp, _second = pair_or(k('11', 'b', 'i'))
C.add([k('11', 'b', 'i')], 'chem-3-3', 'definition-of-chemical-equilibrium', [
    C.lifted('r-1', _pp[0], None, 'The scheme prices this point and the next together (4 + 3), or '
             'instead the pair "' + _second + '".'),
    C.lifted('r-2', _pp[1], None)],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'))
print_question('paper-q11b-i-print')
C.drawn([k('11', 'b', 'ii')], 'chem-3-3', 'kc-expression-for-steam-reforming', S + 'q11b-ii')
C.fixed([k('11', 'b', 'iii')], 'chem-3-3', 'what-a-catalyst-reduces')
C.menu([k('11', 'b', 'iv')], 'chem-3-3', 'conditions-in-le-chateliers-principle')
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-u3', 'meaning-of-continuous-process')
print_question('paper-q11c-a-i-print')
for r, concept in (('ii', 'feedstock'), ('iii', 'co-products'), ('iv', 'quality-control'),
                   ('v', 'environmental-control')):
    C.fixed([ka('11', 'c', r, 'A')], 'chem-u3', concept)
Q11CB = FIG + 'paper-q11c-b'
C.ordered([ka('11', 'c', 'i', 'B'), ka('11', 'c', 'ii', 'B'), ka('11', 'c', 'iii', 'B')], 'chem-2-1',
          'particles-in-crystals', figure=Q11CB)
C.ordered([ka('11', 'c', 'iv', 'B'), ka('11', 'c', 'v', 'B')], 'chem-2-1',
          'metallic-crystals-and-x-ray-crystallography', figure=Q11CB)


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
