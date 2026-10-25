#!/usr/bin/env python3
"""2020 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2020_hl.py          # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2020_hl.py --review # the review ledger
    python3 scripts/markbank/authoring/chem_apply_print.py 2020 hl

No 2020 card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
answer line with the scheme's print of the working where it does not.

The 2020 scheme heads each question with a table of its letters' marks; it is
furniture and no part reads it. Q4(k) and Q11(c) offer whole alternative parts
A and B.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, make_audit, MAX_OPTIONS, anyN, display, point  # noqa: E402

P = Printed(2020, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2020-HL-'
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


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}

# ── Q1 Water of crystallisation in washing soda ──────────────────────────────
C.fixed([k('1', 'a')], 'chem-4-1', 'primary-standard-for-hydrochloric-acid')
# (b): six points, priced (4 × 3).
_q1b = P.items(k('1', 'b'))
assert [it.cell for it in _q1b] == ['[4 × 3]'] and len(_q1b[0].points()) == 6, _q1b
_q1b_opts = [C.lifted('x', t, 3)['verbatim'] for t in _q1b[0].points()]
C.add([k('1', 'b')], 'chem-4-1', 'making-up-a-standard-solution-of-washing-soda', [anyN(
    'r-1', _q1b_opts[0], 12, 4, 3, _q1b_opts,
    'Any four of these: the scheme sets six points and prices them (4 × 3).')], total=12)
C.fixed([k('1', 'c', 'i')], 'chem-4-1', 'indicator-for-a-carbonate-titration')
C.fixed([k('1', 'c', 'ii')], 'chem-4-1', 'justifying-the-choice-of-indicator')
C.fixed([k('1', 'c', 'iii')], 'chem-4-1', 'colour-change-of-methyl-orange-at-end-point')
C.route([k('1', 'd', 'i')], 'chem-4-1', 'moles-of-acid-in-a-titre',
        fixes={'21.5 × 0.12 = 0.00258 (2.58 × 10⁻³, 129/50000) moles HCl':
               '21.5 × 0.12 ÷ 1000 = 0.00258 (2.58 × 10⁻³, 129/50000) moles HCl'},
        row_notes={0: FRACTION.format('21.5 × 0.12', '1000')})
C.route([k('1', 'd', 'ii')], 'chem-4-1', 'moles-of-sodium-carbonate-neutralised', figure=S + 'q1d-ii')
C.route([k('1', 'd', 'iii')], 'chem-4-1', 'moles-of-sodium-carbonate-in-the-flask', figure=S + 'q1d-iii')
C.route([k('1', 'd', 'iv')], 'chem-4-1', 'mass-of-sodium-carbonate-in-the-flask')
C.route([k('1', 'd', 'v')], 'chem-4-1', 'mass-and-moles-of-water-of-crystallisation')
_q1d6 = P.items(k('1', 'd', 'vi'))
assert [it.cell for it in _q1d6] == ['[3]', '[3]', None], _q1d6
C.add([k('1', 'd', 'vi')], 'chem-4-1', 'value-of-x-in-washing-soda', [
    C.lifted('r-1', '0.116256 ÷ 0.0129 = 9 = x', 3,
             FRACTION.format('0.116256', '0.0129') + ' The scheme adds: ' + ' '.join(_q1d6[1].asides)
             + ' ' + _q1d6[2].text)],
    total=3, notes='The scheme gives the answer, 9, priced [3], then this step, priced [3].')

# ── Q2 Benzoic acid from phenylmethanol ──────────────────────────────────────
Q2 = FIG + 'paper-q2'
C.ordered([k('2', 'a', 'i'), k('2', 'a', 'ii')], 'chem-u2', 'phenylmethanol-and-measuring-it',
          figure=Q2)
C.fixed([k('2', 'b')], 'chem-u2', 'colour-changes-during-the-oxidation', figure=Q2)
C.fixed([k('2', 'c')], 'chem-u2', 'observations-at-stages-d-and-e', figure=Q2)
C.fixed([k('2', 'd', 'i')], 'chem-u2', 'purifying-benzoic-acid', figure=Q2)
C.fixed([k('2', 'd', 'ii')], 'chem-u2', 'measuring-a-melting-point', tail=True, figure=Q2)
# (e)(i): a "show", priced (12) over four steps; the fourth is reached by any of
# four comparisons, each ending in the same conclusion.
_q2e = P.items(k('2', 'e', 'i'))
assert _q2e[0].cell == '[12]' and not _q2e[0].text, _q2e
_concl = '⇒ 0.0144 moles phenylmethanol limiting or ⇒ 0.02 moles KMnO₄ sufficient (excess)'
C.add([k('2', 'e', 'i')], 'chem-1-4', 'is-there-enough-permanganate', [
    C.lifted('r-1', '1.5 × 1.04 = 1.56 g phenylmethanol', 3),
    C.lifted('r-2', '1.56 ÷ 108∗ = 0.0144 moles phenylmethanol', 3, FRACTION.format('1.56', '108∗')),
    C.lifted('r-3', '3.16 ÷ 158∗∗ = 0.02 moles KMnO₄', 3, FRACTION.format('3.16', '158∗∗')),
    C.lifted('r-4', _concl, 3, 'The scheme reaches this by any of four comparisons of the moles '
                               'and the ratio 3 : 4; its own print of them is shown with the answer.')],
    total=12, figure=S + 'q2e-i',
    notes='The scheme prices the part (12) over these four steps, (3) each.')
C.route([k('2', 'e', 'ii')], 'chem-1-4', 'theoretical-yield-of-benzoic-acid')
C.cards[-1]['figureKey'] = Q2       # the stimulus, not the scheme's working

# ── Q3 Temperature and the rate of reaction ──────────────────────────────────
Q3T = FIG + 'paper-q3-table'
C.fixed([k('3', 'a')], 'chem-u2', 'heating-a-reaction-mixture-to-a-set-temperature', figure=Q3T)
C.fixed([k('3', 'b', 'i')], 'chem-3-2', 'precipitate-in-the-thiosulfate-reaction', figure=Q3T)
_q3b2 = P.items(k('3', 'b', 'ii'))
assert [it.cell for it in _q3b2] == ['[2 × 3]', '[2 × 3]'], _q3b2
_p = _q3b2[0].points()
C.add([k('3', 'b', 'ii')], 'chem-3-2', 'timing-the-reaction-by-the-cross', [
    C.lifted('r-1', _p[0], 3, 'The scheme prices this point and the next (2 × 3), one each, or '
             'instead the pair "' + _q3b2[1].text + '" (2 × 3).'),
    C.lifted('r-2', _p[1], 3)], figure=Q3T)
# (c): the six missing rates, one mark each, in the order of Runs 2 to 7.
_q3c = P.items(k('3', 'c'))
assert [it.cell for it in _q3c] == ['[6 × 1]', None], _q3c
_rates = ['0.005', '0.009', '0.018', '0.029', '0.063', '0.111']
assert display(_q3c[1].text).startswith('r (s⁻¹) No mark ' + ' '.join(_rates)), _q3c[1].text
C.add([k('3', 'c')], 'chem-3-2', 'rate-as-reciprocal-of-time', [anyN(
    'r-1', _rates[0], 6, 6, 1, [C.lifted('x', v, 1)['verbatim'] for v in _rates],
    'One mark for each of the six rates, which the scheme lists for Runs 2 to 7 in order (6 × 1). It '
    'adds: "Apply slip penalty no more than once for not rounding or incorrect rounding in 3(c)."')],
    total=6, figure=Q3T)
C.fixed([k('3', 'd', 'i')], 'chem-3-2', 'graph-of-rate-against-temperature', figure=S + 'q3d-i')
print_question('paper-q3d-i-print')
C.fixed([k('3', 'd', 'ii')], 'chem-3-2', 'temperature-rise-that-doubles-the-rate', figure=Q3T)
C.fixed([k('3', 'd', 'iii')], 'chem-3-2', 'why-rate-rises-with-temperature', figure=Q3T)
Q3E = FIG + 'paper-q3e'
C.fixed([k('3', 'e', 'i')], 'chem-3-2', 'testing-a-point-against-the-curve', figure=Q3E)
C.fixed([k('3', 'e', 'ii')], 'chem-3-2', 'depth-of-liquid-and-apparent-rate', figure=Q3E)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
_q4a = P.items(k('4', 'a'))
C.fixed([k('4', 'a')], 'chem-1-2', 'thomson-plum-pudding-model', notes=Q4_NOTE, figure=S + 'q4a',
        row_notes={0: 'The scheme also draws the model; its own print is shown with the answer.'})
C.fixed([k('4', 'b')], 'chem-1-2', 'element-from-its-4s-and-3d-electrons', notes=Q4_NOTE,
        figure=FIG + 'paper-q4b')
# (c): the paper sets the nuclide's mass and atomic numbers round its symbol.
_q4c = P.items(k('4', 'c'))
assert [it.cell for it in _q4c] == ['[2 × 3]', '[6]', None], _q4c
_q4c_p = _q4c[0].points()
C.add([k('4', 'c')], 'chem-1-2', 'product-of-alpha-decay', [
    C.lifted('r-1', _q4c_p[0], 3, 'The scheme prices this point and the next (2 × 3), one each, or '
             'instead (6) for the nuclide written in full with its mass and atomic numbers, ²³⁷₉₃Np; '
             'its own print is shown with the answer.'),
    C.lifted('r-2', _q4c_p[1], 3)],
    qtext=P.rearranged(P.ask(k('4', 'c')), 'an 241 Am atom releases an alpha particle? 95',
                       'an ²⁴¹₉₅Am atom releases an alpha particle?'),
    figure=S + 'q4c', notes=Q4_NOTE)
# (d): the two formulae, priced (2 × 3) by one cell under (ii).
_q4d = [P.items(k('4', 'd', r)) for r in ('i', 'ii')]
assert [it.cell for it in _q4d[0]] == [None] and [it.cell for it in _q4d[1]] == ['[2 × 3]'], _q4d
C.add([k('4', 'd', 'i'), k('4', 'd', 'ii')], 'chem-1-4', 'formulae-of-two-ionic-compounds', [
    C.lifted('r-1', _q4d[0][0].text, 3, 'For (i). The scheme prices these points (2 × 3), one each.'),
    C.lifted('r-2', _q4d[1][0].text, 3, 'For (ii). The scheme adds: ' + ' '.join(_q4d[1][0].asides))],
    notes=Q4_NOTE)
C.fixed([k('4', 'e')], 'chem-2-2', 'shapes-of-qx3-molecules', notes=Q4_NOTE)
C.answer_only([k('4', 'f')], 'chem-2-3', 'pressure-from-the-gas-law', S + 'q4f', notes=Q4_NOTE)
C.cards[-1]['questionFigureKey'] = FIG + 'paper-q4f-print'
C.fixed([k('4', 'g')], 'chem-3-2', 'how-a-catalyst-lowers-activation-energy', notes=Q4_NOTE)
C.fixed([k('4', 'h')], 'chem-2-1', 'when-ionic-compounds-conduct', notes=Q4_NOTE)
C.fixed([k('4', 'i')], 'chem-4-3', 'limescale-in-a-kettle', notes=Q4_NOTE)
_q4j = [P.items(k('4', 'j', r)) for r in ('i', 'ii')]
assert [it.cell for it in _q4j[0]] == [None] and [it.cell for it in _q4j[1]] == ['[2 × 3]'], _q4j
C.add([k('4', 'j', 'i'), k('4', 'j', 'ii')], 'chem-4-2', 'aldehyde-group-and-formula-of-vanillin', [
    C.lifted('r-1', display(_q4j[0][0].text).rstrip('/ '), 3,
             'For (i). The scheme prices these points (2 × 3), one each.'),
    C.lifted('r-2', _q4j[1][0].text, 3, 'For (ii).')],
    figure=FIG + 'paper-q4j', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-4-3', 'photodissociation-of-ozone', notes=Q4_NOTE, tail=True)
# The aside line ends in the "or" that sets B against A.
C.cards[-1]['rows'][0]['contextNote'] = C.cards[-1]['rows'][0]['contextNote'].replace(
    '[O⁻ is incorrect] or"', '[O⁻ is incorrect]"')
_q4kb = P.items(ka('4', 'k', None, 'B'))
C.drawn([ka('4', 'k', None, 'B')], 'chem-4-2', 'monomer-of-polyphenylethene', S + 'q4k-b',
        notes=Q4_NOTE + ' The scheme adds: "' + _q4kb[1].text + '".')

# ── Q5 Electrons, energy levels and orbitals ─────────────────────────────────
Q5 = FIG + 'paper-q5'
C.menu([k('5', 'a')], 'chem-1-2', 'what-an-electron-is', figure=Q5)
C.fixed([k('5', 'b', 'i')], 'chem-1-2', 'excited-hydrogen-atom', figure=Q5)
C.fixed([k('5', 'b', 'ii')], 'chem-1-2', 'colour-of-the-n3-to-n2-line', figure=Q5)
C.fixed([k('5', 'b', 'iii')], 'chem-1-2', 'balmer-series', figure=Q5)
C.fixed([k('5', 'c', 'i')], 'chem-1-2', 'sub-levels-in-the-third-energy-level', figure=Q5)
_q5c2 = P.items(k('5', 'c', 'ii'))
assert [it.cell for it in _q5c2] == ['[2 × 3]'], _q5c2
_t = _q5c2[0].text
_cut = _t.index(' approximate solution')
_pp = [x.strip() for x in _t[:_cut].split('//')]
assert len(_pp) == 2, _pp
C.add([k('5', 'c', 'ii')], 'chem-1-2', 'definition-of-an-atomic-orbital', [
    C.lifted('r-1', _pp[0], 3, 'The scheme prices this point and the next (2 × 3), one each, or '
             'instead the pair "' + _t[_cut:].strip() + '". It adds: ' + ' '.join(_q5c2[0].asides)),
    C.lifted('r-2', _pp[1], 3)], figure=Q5)
C.fixed([k('5', 'c', 'iii')], 'chem-1-2', 'orbitals-in-the-second-energy-level', figure=Q5)
C.fixed([k('5', 'c', 'iv')], 'chem-1-2', 'electrons-in-the-third-energy-level', figure=Q5)
_q5d = P.ask(k('5', 'd'))
C.fixed([k('5', 'd')], 'chem-1-2', 's-p-configurations-of-four-elements',
        qtext=_q5d[:_q5d.index(' Refer to these')], figure=Q5)
C.fixed([k('5', 'd', 'i')], 'chem-1-3', 'why-noble-gases-are-inert', figure=Q5)
C.fixed([k('5', 'd', 'ii')], 'chem-1-3', 'why-group-2-metals-are-reactive', tail=True, figure=Q5)

# ── Q6 Petrol ────────────────────────────────────────────────────────────────
C.fixed([k('6', 'a')], 'chem-2-4', 'knocking-and-octane-number')
print_question('paper-q6a-print')
for r, concept in (('i', 'naming-oil-refining-reactions'), ('ii', 'deducing-a-cracking-product'),
                   ('iii', 'naming-2-2-4-trimethylpentane')):
    C.fixed([k('6', 'b', r)], 'chem-2-4', concept)
C.fixed([k('6', 'c', 'i')], 'chem-2-4', 'an-oxygenate-in-petrol')
C.fixed([k('6', 'c', 'ii')], 'chem-2-4', 'why-oxygenates-are-added')
C.fixed([k('6', 'd', 'i')], 'chem-3-1', 'definition-of-heat-of-formation')
# (d)(ii): the balanced equation (3), then the heat of combustion (12), whose
# working the scheme sets out in two boxed routes.
_q6d2 = P.items(k('6', 'd', 'ii'))
assert [it.cell for it in _q6d2][:2] == ['[3]', '[12]'], _q6d2
C.add([k('6', 'd', 'ii')], 'chem-3-1', 'heat-of-combustion-of-propane', [
    C.lifted('r-1', _q6d2[0].text, 3),
    C.lifted('r-2', _q6d2[1].text, 12,
             'The scheme prices the answer (12) and sets out the working that earns it, with the '
             'marks for each step, in two boxed routes; its own print is shown with the answer.')],
    figure=S + 'q6d-ii')

# ── Q7 Acids, bases and an indicator ─────────────────────────────────────────
Q7T = FIG + 'paper-q7-table'
_q7a = P.items(k('7', 'a'))
assert [it.cell for it in _q7a] == ['[4]', '[4]', '[2 × 2]'], _q7a
C.add([k('7', 'a')], 'chem-3-4', 'bronsted-lowry-acids-strong-and-weak', [
    C.lifted('r-1', _q7a[0].text, 4),
    C.lifted('r-2', _q7a[1].text, 4, 'Or instead, (2 × 2), "' + _q7a[2].text + '".')])
_q7b = P.ask(k('7', 'b'))
for r, concept, text in (('i', 'conjugate-acid-of-hydrogensulfate', 'H₂SO₄'),
                         ('ii', 'conjugate-base-of-hydrogensulfate', 'SO₄²⁻')):
    _it = P.items(k('7', 'b', r))
    assert [it.cell for it in _it] == ['[3]'], _it
    # Q7 has no lead-in of its own; what the paper prints after (b) leads (c).
    C.add([k('7', 'b', r)], 'chem-3-4', concept, [C.lifted('r-1', text, 3)], qtext=_q7b,
          cid=f'q7-b-{r}', stem='')
C.fixed([k('7', 'c')], 'chem-u2', 'test-for-sulfate-ion', figure=Q7T)
C.route([k('7', 'd', 'i')], 'chem-3-4', 'hydronium-concentration-from-ph', figure=Q7T)
C.cards[-1]['notes'] = C.cards[-1]['notes'].replace(
    ', and its own print of every route it accepts is shown with the answer', '')
C.route([k('7', 'd', 'ii')], 'chem-3-4', 'hydroxide-concentration-from-ph', figure=S + 'q7d-ii')
print_question('paper-q7d-print')
_q7e = P.items(k('7', 'e'))
C.route([k('7', 'e')], 'chem-3-4', 'ph-of-a-weak-acid-indicator',
        notes='The scheme adds: "' + _q7e[-1].text + '"')
_q7f = P.items(k('7', 'f'))
assert [it.cell for it in _q7f] == ['[3]'], _q7f
C.add([k('7', 'f', 'i')], 'chem-3-4', 'dissociation-of-an-indicator', [
    C.lifted('r-1', _q7f[0].text, 3, 'The scheme adds: ' + ' '.join(P.items(k('7', 'f', 'i'))[0].asides))])
C.fixed([k('7', 'f', 'ii')], 'chem-3-4', 'indicator-colour-in-strong-base')

# ── Q8 Ethene and its reactions ──────────────────────────────────────────────
Q8 = FIG + 'paper-q8'
_q8a = P.ask(k('8', 'a'))
for r, concept in (('i', 'substitution-in-the-scheme'), ('ii', 'additions-in-the-scheme')):
    _it = P.items(k('8', 'a', r))
    assert [it.cell for it in _it] == ['[3]'], _it
    C.add([k('8', 'a', r)], 'chem-4-2', concept, [C.lifted('r-1', _it[0].text, 3)],
          qtext=_q8a, figure=Q8, cid=f'q8-a-{r}')
C.fixed([k('8', 'a', 'iii')], 'chem-4-2', 'elimination-in-the-scheme', figure=Q8)
_q8b1 = P.items(k('8', 'b', 'i'))
assert [it.cell for it in _q8b1] == ['[2 × 3]', '[6]'], _q8b1
_pb = _q8b1[0].points()
C.add([k('8', 'b', 'i')], 'chem-4-2', 'reducing-ethanal', [
    C.lifted('r-1', _pb[0], 3, 'The scheme prices this point and the next (2 × 3), one each, or '
             'instead (6) for "' + _q8b1[1].text + '". It adds: ' + ' '.join(_q8b1[0].asides)),
    C.lifted('r-2', _pb[1], 3)], figure=Q8)
C.fixed([k('8', 'b', 'ii')], 'chem-4-2', 'bonds-formed-in-reducing-ethanal', figure=S + 'q8b-ii',
        row_notes={0: 'The scheme draws ethanol with these bonds boxed; its own print is shown with '
                      'the answer.'})
print_question('paper-q8b-ii-print')
C.fixed([k('8', 'c')], 'chem-2-2', 'an-organic-compound-soluble-in-water', figure=Q8)
C.fixed([k('8', 'd', 'i')], 'chem-4-2', 'identify-chloroethene', figure=S + 'q8d-i',
        row_notes={0: 'The scheme also draws its structure; its own print is shown with the answer.'})
C.fixed([k('8', 'd', 'ii')], 'chem-2-2', 'geometry-change-on-elimination', figure=Q8)
C.drawn([k('8', 'd', 'iii')], 'chem-4-2', 'repeating-units-of-pvc', S + 'q8d-iii',
        notes='The scheme adds: "Correct carbon skeleton (4 carbons) with chlorines on alternate '
              'carbons".')
# (e): four numbered points, each ticked, priced (3 + 3 + 3 + 2).
_q8e = P.items(k('8', 'e'))
assert [it.cell for it in _q8e] == ['[3 + 3 + 3 + 2 ]', None], _q8e
_m1 = ('chlorine (Cl₂) undergoes heterolytic fission / Cl₂ → Cl⁺ + Cl⁻ / Clδ+—Clδ– → Cl⁺ + Cl⁻ or '
       'chlorine (Cl₂) polarised approaching double bond / Cl₂ → Clδ+—Clδ–')
_m2 = ('attraction of Cl⁺ to double bond / interaction of Cl⁺ with double bond / or attraction of '
       'positive end of Clδ+—Clδ– (polarised Cl₂ molecule) to double bond / positive end of '
       'Clδ+—Clδ– (polarised Cl₂ molecule) interacts with double bond')
_m3 = 'carbononium ion (carbocation, C⁺, positively-charged intermediate, bridged chloronium ion) formed'
_m4 = ('addition of Cl⁻ to carbonium ion (carbocation, C⁺, intermediate, bridged chloronium ion) '
       'gives product (1,2-dichloroethane)')
C.add([k('8', 'e')], 'chem-4-2', 'ionic-addition-of-chlorine-to-ethene', [
    C.lifted('r-1', _m1, None, 'The scheme adds: [bond (line) essential in Clδ+—Clδ– ][bond (line) '
             'must not be shown between Cl⁺ and Cl⁻]'),
    C.lifted('r-2', _m2, None, 'Or instead: "breaking of double bond in ethene and polarised bond in '
             'chlorine (Cl₂)".'),
    C.lifted('r-3', _m3, None, 'The scheme draws the steps; its own print is shown with the answer.'),
    C.lifted('r-4', _m4, None, 'The scheme adds: [Hs need not be shown explicitly]')],
    kind='orderedSplit', notation='[3 + 3 + 3 + 2]', total=11, figure=S + 'q8e',
    notes=SPLIT.format('[3 + 3 + 3 + 2]'))
print_question('paper-q8e-print')

# ── Q9 Carbon monoxide and steam at equilibrium ──────────────────────────────
C.fixed([k('9', 'a')], 'chem-3-3', 'chemical-equilibrium-and-le-chatelier')
C.drawn([k('9', 'b')], 'chem-3-3', 'kc-expression-for-the-water-gas-shift', S + 'q9b')
C.answer_only([k('9', 'c')], 'chem-3-3', 'moles-at-equilibrium-from-kc', S + 'q9c',
              fixes={'2.097 – 2.1 moles carbon monoxide Each tick 3 marks':
                     '2.097 – 2.1 moles carbon monoxide'})
C.fixed([k('9', 'd', 'i')], 'chem-3-3', 'adding-steam-and-kc')
C.fixed([k('9', 'd', 'ii')], 'chem-3-3', 'adding-steam-and-the-yield-of-hydrogen')
C.fixed([k('9', 'e')], 'chem-3-3', 'temperature-and-kc-for-an-exothermic-reaction')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
for r, concept in (('i', 'definition-of-bod'), ('ii', 'primary-sewage-treatment'),
                   ('iii', 'secondary-sewage-treatment'), ('iv', 'when-tertiary-treatment-is-needed'),
                   ('v', 'why-tertiary-treatment-is-not-always-done'),
                   ('vi', 'impact-of-omitting-tertiary-treatment')):
    C.fixed([k('10', 'a', r)], 'chem-4-3', concept)
C.ordered([k('10', 'b', 'i'), k('10', 'b', 'ii')], 'chem-3-5', 'definitions-of-oxidation')
_q10b3 = P.items(k('10', 'b', 'iii'))
assert [it.cell for it in _q10b3] == ['[3]', '[3]'], _q10b3
C.add([k('10', 'b', 'iii')], 'chem-3-5', 'oxidation-numbers-in-a-lithium-ion-cell', [
    C.mark_ask(point('r-1', P.ask(k('10', 'b', 'iii')), 3,
                     'The scheme writes the oxidation numbers under the equation, for atoms or for '
                     'groups of atoms; its own print is shown with the answer.')),
    C.lifted('r-2', _q10b3[1].text, 3)], figure=S + 'q10b-iii')
C.fixed([k('10', 'b', 'iv')], 'chem-3-5', 'the-oxidising-agent')
_q10b5 = P.items(k('10', 'b', 'v'))
assert [it.cell for it in _q10b5] == ['[6]', '[3]'], _q10b5
C.add([k('10', 'b', 'v')], 'chem-3-5', 'balancing-the-lead-acid-cell-reaction', [
    C.lifted('r-1', _q10b5[0].text, 6,
             'The scheme gives (3) for correct oxidation numbers if the balancing is not correct; its '
             'own print is shown with the answer.')], figure=S + 'q10b-v')
C.fixed([k('10', 'b', 'vi')], 'chem-4-3', 'why-recycle-batteries')
C.answer_only([k('10', 'c', 'i')], 'chem-1-4', 'mass-of-aluminium-carbide', S + 'q10c-i')
C.answer_only([k('10', 'c', 'ii')], 'chem-1-4', 'volume-of-methane-at-stp', S + 'q10c-ii')
C.route([k('10', 'c', 'iii')], 'chem-1-4', 'volume-of-water-used-up')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
Q11A = FIG + 'paper-q11a-table'
C.fixed([k('11', 'a', 'i')], 'chem-2-1', 'definition-of-electronegativity', figure=Q11A)
C.fixed([k('11', 'a', 'ii')], 'chem-2-2', 'hydrogen-bonding-in-water', figure=S + 'q11a-ii',
        row_notes={0: 'The scheme draws the molecules; its own print is shown with the answer.'})
C.fixed([k('11', 'a', 'iii')], 'chem-2-2', 'why-only-water-hydrogen-bonds', figure=Q11A)
C.fixed([k('11', 'a', 'iv')], 'chem-2-2', 'boiling-points-of-the-hydrides', figure=Q11A)
_q11a5 = P.items(k('11', 'a', 'v'))
assert [it.cell for it in _q11a5] == ['[4 + 3]', '[4]'], _q11a5
_t = _q11a5[0].text
_cut = _t.index(' hydrogen selenide (H₂Se) molecule is polar')
C.add([k('11', 'a', 'v')], 'chem-2-2', 'solubility-of-methane-and-hydrogen-selenide', [
    C.lifted('r-1', _t[:_cut], None),
    C.lifted('r-2', _t[_cut:].strip(), None, 'The scheme adds: ' + ' '.join(_q11a5[0].asides) +
             ' And: "' + _q11a5[1].text + '" (4).')],
    kind='orderedSplit', notation='[4 + 3]', total=7, figure=Q11A, notes=SPLIT.format('[4 + 3]'))
C.answer_only([k('11', 'b', 'i')], 'chem-1-4', 'empirical-formula-from-composition', S + 'q11b-i')
C.fixed([k('11', 'b', 'ii')], 'chem-1-4', 'molecular-formula-from-relative-molecular-mass')
C.menu([k('11', 'b', 'iii')], 'chem-4-2', 'compounds-of-formula-c2h4o2')
C.fixed([k('11', 'b', 'iv')], 'chem-4-2', 'test-for-a-carboxylic-acid')
for r, concept in (('i', 'a-use-of-oxygen'), ('ii', 'separating-oxygen-from-air'),
                   ('iii', 'co-product-of-oxygen-separation'), ('iv', 'a-use-of-nitrogen'),
                   ('v', 'why-nitrogen-is-inert')):
    C.fixed([ka('11', 'c', r, 'A')], 'chem-u3', concept)
Q11CB = FIG + 'paper-q11c-b'
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-3-5', 'corrosion-of-a-metal', figure=Q11CB)
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-3-5', 'corrosion-of-iron-and-aluminium', figure=Q11CB)
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-3-5', 'iron-and-steel', figure=Q11CB)
C.ordered([ka('11', 'c', 'iv', 'B')], 'chem-3-5', 'anodising-aluminium', figure=Q11CB)
C.fixed([ka('11', 'c', 'v', 'B')], 'chem-2-1', 'why-metals-conduct', figure=Q11CB)


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
