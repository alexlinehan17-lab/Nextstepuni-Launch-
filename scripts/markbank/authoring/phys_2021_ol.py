#!/usr/bin/env python3
"""Physics 2021 Ordinary Level — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'. This scheme restarts its roman part markers with every question
and the block parser files each restart under whichever key it saw first, so a
from_run parent key rarely matches the paper's question number — the slices
below were each located by searching every parsed point for the answer text,
not by trusting the key.

Parts the scheme answers with a bare marking convention or with the drawn
figure itself carry nothing a card can lift and are left alone:
  Q11(x)  — "apparatus 3 method 3 observation/conclusion 3", no content.
  Q13(e)  — the credit is the drawn battery symbol; no words for it.
  Q13(g)  — "correct diagram" only.
  Q14(c)(iii) — "correct diagram" only.
Q3(ii) has a worded answer ("correctly marked u and v distances") but its PDF
block is dropped by both parsers, so there is no point to lift it from.
Q9(vi)-(viii) need the circuit diagram (12 V, 3 Ω in series with 5/2/4 Ω in
parallel) and both crops of paper page 8 are truncated; Q10(iv) needs the
incomplete ray diagram on paper page 9, which has no crop at all.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2021, 'ol')
MARK = ('The paper prints the part mark in brackets after the question, so the text ends '
        'on a number rather than punctuation. The question itself is complete.')

A.card(8, None, 'vii', topic='phys-2-3', concept='what-diffraction-through-a-gap-looks-like',
       source='pdf', from_run=((2, None, 'vii'), 0, slice(17, 23)), marks=[6],
       notation='6, or 3 for a partial answer',
       notes='The scheme numbers this answer under its own Question 2 while the paper '
             'prints Question 8.')

# ── Section A: the five experiment questions ───────────────────────────────
A.card(1, None, 'i', topic='phys-u2', concept='apparatus-for-the-free-fall-experiment',
       source='pdf',
       from_runs=[((9, None, 'i'), 2, slice(0, 5)),
                  ((9, None, 'i'), 2, slice(6, 11)),
                  ((9, None, 'i'), 2, slice(12, 16)),
                  ((9, None, 'i'), 2, slice(17, 26))],
       marks=[3, 3, 3, 3], notation='4 × 3', checked=MARK,
       notes='The scheme takes 2 marks off a diagram with no labels, and caps a wrong '
             'experiment at 2 × 3.')

A.card(1, None, 'vi', topic='phys-u2', concept='more-values-for-g-and-their-average',
       source='pdf',
       from_runs=[((9, None, 'vi'), 0, slice(3, 20)),
                  ((9, None, 'vi'), 0, slice(21, 26))],
       marks=[3, 3], notation='2 × 3',
       notes='The five values are g worked from each remaining row of the results table; '
             'any two of them earn the first 3 marks. "m s-2" is the flattened m s⁻².')

A.card(2, None, 'i', topic='phys-u2', concept='apparatus-for-the-boyles-law-experiment',
       source='pdf',
       from_runs=[((9, None, 'i'), 3, slice(7, 11)),
                  ((9, None, 'i'), 3, slice(11, 17)),
                  ((9, None, 'i'), 3, slice(17, 26)),
                  ((9, None, 'i'), 3, slice(26, 33))],
       marks=[3, 3, 3, 3], notation='4 × 3',
       notes='The scheme lists a fifth creditable line, "detail e.g. correct arrangement", '
             'and credits any four of the five lines at 3 marks each. No labels: deduct 2.')

A.card(2, None, 'iv', topic='phys-u2', concept='calculating-one-over-v-for-boyles-law',
       source='pdf', from_run=((9, None, 'iv'), 7, slice(3, 9)), marks=[6],
       notation='6 × 1',
       context='One value per row of the table, in the printed order of V: 19, 17, 15, '
               '13, 11, 9 cm3.',
       notes='The paper\'s fraction glyphs flatten in extraction — the question asks for '
             '1/V, calculated to three decimal places, for each value of V in the table.')

A.card(2, None, 'v', topic='phys-u2', concept='plotting-pressure-against-one-over-volume',
       source='pdf',
       from_runs=[((9, None, 'v'), 10, slice(0, 3)),
                  ((9, None, 'v'), 12, slice(3, 7)),
                  ((9, None, 'v'), 12, slice(10, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3',
       notes='Axis labels may be a name, a symbol or a unit. Not drawn on graph paper: '
             'maximum mark 3 × 3. The graph asked for is p against 1/V — the paper\'s '
             'fraction glyph flattens in extraction.')

A.card(2, None, 'vi', topic='phys-u2', concept='volume-at-a-given-pressure-from-the-graph',
       source='pdf',
       from_runs=[((9, None, 'vi'), 13, slice(0, 7)),
                  ((9, None, 'vi'), 15, slice(0, 9))],
       marks=[2, 2], notation='2 × 2', checked=MARK,
       context='The scheme\'s row reads "reads 1/V value from graph" — the leading '
               '"1 𝑉" is the flattened fraction 1/V.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-focal-length-experiment',
       source='pdf',
       from_runs=[((9, None, 'i'), 6, slice(0, 4)),
                  ((9, None, 'i'), 6, slice(5, 7)),
                  ((9, None, 'i'), 6, slice(8, 9)),
                  ((9, None, 'i'), 6, slice(10, 19))],
       marks=[3, 3, 3, 3], notation='4 × 3',
       notes='The scheme takes 2 marks off a diagram with no labels.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-for-the-latent-heat-experiment',
       source='pdf', from_run=((9, None, 'i'), 9, slice(4, 13)), marks=[12],
       notation='4 × 3', checked=MARK,
       notes='Any four of the five listed lines at 3 marks each. No labels: deduct 2; '
             'wrong experiment: maximum mark 3 × 3.')

A.card(4, None, 'vi', topic='phys-u2', concept='completing-the-latent-heat-calculation',
       source='pdf',
       from_runs=[((9, None, 'vi'), 29, slice(0, 21)),
                  ((9, None, 'vi'), 32, slice(0, 12))],
       marks=[8, 4], notation='4 × 2 + 4',
       context='With the measured values in place the scheme\'s line reads: (0.0014) l + '
               '(0.0014)(4200)(64) = (0.0433)(4200)(16) + (0.0894)(390)(16) — i.e. '
               'A = 0.0433 kg, B = 0.0014 kg, C = 16 °C, D = 64 °C.',
       notes='The scheme credits 4 × 2 for the correct substitutions and 4 for finishing '
             'the calculation. "2.2 × 106" is the flattened 2.2 × 10⁶.')

A.card(5, None, 'iv', topic='phys-u2', concept='plotting-current-against-voltage',
       source='pdf',
       from_runs=[((9, None, 'iv'), 12, slice(0, 3)),
                  ((9, None, 'iv'), 14, slice(3, 7)),
                  ((9, None, 'iv'), 14, slice(10, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3',
       notes='Axis labels may be a name, a symbol or a unit. Not drawn on graph paper: '
             'maximum mark 3 × 3.')

# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(6, 'f', None, topic='phys-2-3', concept='light-along-an-optical-fibre',
       source='pdf', from_run=((9, 'f', None), 0, slice(3, 10)), marks=[7],
       notation='7, or 4 for a partial answer')

A.card(6, 'k', None, topic='phys-4-3', concept='bohr-model-of-the-atom',
       source='pdf', from_run=((9, 'h', 'i'), 2, slice(15, 25)), marks=[7],
       notation='7, or 4 for a partial answer',
       notes='Any two of the three listed features earn the full 7.')

A.card(8, None, 'ix', topic='phys-2-7', concept='what-polarisation-looks-like',
       source='pdf', from_run=((2, None, 'viii'), 1, slice(26, 40)), marks=[6],
       notation='6, or 3 for a partial answer', checked=MARK,
       notes='The scheme takes 2 marks off a diagram with no labels.')

A.card(10, None, 'i', topic='phys-2-3', concept='how-a-periscope-works',
       source='pdf', from_run=((2, None, 'i'), 7, slice(23, 32)), marks=[10],
       notation='10, or 7 or 4 for a partial answer', stem=False,
       notes='No labels: deduct 2. A description with no diagram is capped at 7.')

A.card(13, 'h', None, topic='phys-3-2', concept='forces-on-a-balanced-oil-drop',
       source='pdf', from_run=((2, 'h', None), 0, slice(3, 14)), marks=[7],
       notation='7, or 4 for a partial answer', checked=MARK, stem=False,
       context='"The drop" is the charged oil drop of Millikan\'s experiment, held '
               'stationary between the plates by the applied electric field.')

# ── Section B calculations and short answers ───────────────────────────────
A.card(10, None, 'v', topic='phys-2-3', concept='magnification-from-image-and-object-height',
       source='pdf', from_run=((2, None, 'v'), 10, slice(0, 2)), marks=[6],
       notation='6, or 3 for a partial answer',
       context='Scheme working: (M = v/u =). The extracted scheme flattens the fraction: '
               '"3 2" reads 3/2 = 1.5, the image height over the object height.')

A.card(10, None, 'vi', topic='phys-2-3', concept='image-distance-from-magnification',
       source='pdf', from_run=((2, None, 'vi'), 15, slice(7, 10)), marks=[6],
       notation='6, or 3 for a partial answer',
       context='Scheme working: (v/u = 3/2 ⟹ v = 1.5u = (1.5)(17) = ). The extracted '
               'scheme splits the decimal: "25. 5 cm" reads 25.5 cm.')

A.card(11, None, 'vii', topic='phys-2-1', concept='area-of-the-garden',
       source='pdf', from_run=((2, None, 'vii'), 3, slice(1, 6)), marks=[4],
       figure='physics-2021-OL-paper-p10-i1',
       notes='The 6 m and 9 m sides are read off the paper\'s diagram of the garden. '
             '"m2" is the flattened m².')

A.card(11, None, 'viii', topic='phys-2-1', concept='seconds-in-twelve-hours',
       source='pdf', from_run=((2, None, 'viii'), 17, slice(1, 5)), marks=[3])

A.card(11, None, 'ix', topic='phys-2-1', concept='energy-from-the-solar-constant',
       source='pdf', from_run=((2, None, 'viii'), 17, slice(23, 31)), marks=[6],
       notation='6, or 3 for a partial answer',
       context='The paper gives the solar constant as 1.36 kW m−2 — energy = solar '
               'constant × time in seconds × area, using the answers to (vii) and '
               '(viii). "103" and "109" are the flattened 10³ and 10⁹.')

A.card(12, None, 'v', topic='phys-4-3', concept='electrons-in-an-atom-from-the-atomic-number',
       source='pdf', from_run=((2, None, 'v'), 15, slice(3, 5)), marks=[4],
       first_sentence=True,
       context='Scheme working: (Mt109 268 = ) — meitnerium\'s atomic number, 109, read '
               'from page 79 of the Formulae and Tables booklet; a neutral atom has one '
               'electron per proton.',
       notes='The paper block welds the following passage about Marie Curie onto this '
             'question; the scheme\'s reprint confirms the question is its first sentence.')

A.emit()
