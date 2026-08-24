#!/usr/bin/env python3
"""Physics 2023 Higher Level — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'. The scheme reprints the question above its own answer, which is
why index 0 is often the cue rather than a marking point.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2023, 'hl')

A.card(1, None, 'v', topic='phys-u2', concept='g-from-the-slope-of-a-graph',
       source='pdf',
       from_runs=[((1, None, 'v'), 0, slice(0, None)),
                  ((1, None, 'v'), 1, slice(0, 6)),
                  ((1, None, 'v'), 1, slice(7, 14))],
       marks=[3, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(9, None, 'ii', topic='phys-4-4', concept='energy-released-in-a-decay',
       source='pdf',
       from_runs=[((9, None, 'ii'), 0, slice(0, 3)),
                  ((9, None, 'ii'), 1, slice(0, 6)),
                  ((9, None, 'ii'), 2, slice(0, 4))],
       marks=[3, 3, 3], first_sentence=True)

A.card(14, 'c', 'iii', topic='phys-3-3', concept='total-resistance-of-a-mixed-circuit',
       source='pdf',
       from_runs=[((14, 'c', 'iii'), 0, slice(0, 5)),
                  ((14, 'c', 'iii'), 0, slice(6, 10)),
                  ((14, 'c', 'iii'), 0, slice(11, 15))],
       marks=[3, 3, 3])

A.card(14, 'c', 'iv', topic='phys-3-3', concept='how-to-lower-total-resistance',
       source='pdf', from_run=((14, 'c', 'iv'), 0, slice(0, 2)), marks=[3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(1, None, 'iv', topic='phys-u2', concept='graph-of-distance-against-time-squared',
       source='pdf',
       from_runs=[((1, None, 'iv'), 0, slice(0, 2)),
                  ((1, None, 'iv'), 3, slice(0, 2)),
                  ((1, None, 'iv'), 3, slice(3, 6)),
                  ((1, None, 'iv'), 3, slice(7, 12))],
       marks=[3, 3, 3, 3],
       notes='The relationship is linear against the SQUARE of the time, so the first '
             'mark is for working those values out before plotting anything.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-grating-experiment',
       source='pdf',
       from_runs=[((3, None, 'i'), 0, slice(0, 3)),
                  ((3, None, 'i'), 0, slice(4, 5)),
                  ((3, None, 'i'), 0, slice(6, 8)),
                  ((3, None, 'i'), 0, slice(9, 10))],
       marks=[3, 3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-for-the-latent-heat-experiment',
       source='pdf',
       from_runs=[((4, None, 'i'), 0, slice(0, 5)),
                  ((4, None, 'i'), 0, slice(6, 9)),
                  ((4, None, 'i'), 0, slice(10, 11)),
                  ((4, None, 'i'), 0, slice(12, 13))],
       marks=[3, 3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(8, None, 'vi', topic='phys-2-4', concept='drawing-the-third-harmonic',
       source='pdf', card_id='phys-2023-hl-q8a-vi',
       from_runs=[((8, 'a', 'vi'), 0, slice(0, 4)),
                  ((8, 'a', 'vi'), 0, slice(5, 11))],
       marks=[3, 3],
       notes='The scheme files this answer under its own 8(a); the paper prints '
             'plain (vi).')

A.card(10, None, 'vii', topic='phys-4-2', concept='parts-of-an-x-ray-tube',
       source='pdf',
       from_runs=[((10, None, 'vii'), 2, slice(0, 2)),
                  ((10, None, 'vii'), 2, slice(3, 6)),
                  ((10, None, 'vii'), 2, slice(7, 13))],
       marks=[2, 2, 2], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme also credits cooling, shielding, a window and a partial vacuum.')

A.card(12, 'b', 'iv', topic='phys-3-3', concept='circuit-to-convert-ac-to-dc',
       source='pdf',
       from_runs=[((11, 'b', 'iv'), 0, slice(2, 7)),
                  ((11, 'b', 'iv'), 0, slice(8, 10)),
                  ((11, 'b', 'iv'), 0, slice(11, 17))],
       marks=[3, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme numbers this answer under its own Question 11 while the paper '
             'prints Question 12.')

A.card(12, 'b', 'v', topic='phys-3-3', concept='circuit-of-a-voltage-inverter',
       source='pdf',
       from_runs=[((11, 'b', 'v'), 0, slice(0, 5)),
                  ((11, 'b', 'v'), 0, slice(6, 9)),
                  ((11, 'b', 'v'), 0, slice(10, 13))],
       marks=[3, 3, 3])

A.card(12, 'b', 'vi', topic='phys-3-3', concept='truth-table-of-a-not-gate',
       source='pdf',
       from_runs=[((11, 'b', 'vi'), 0, slice(4, 8)),
                  ((11, 'b', 'vi'), 0, slice(9, 13))],
       marks=[3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(14, 'a', 'iv', topic='phys-2-1', concept='graph-that-explains-boyles-law',
       source='pdf',
       from_runs=[((14, 'a', 'iv'), 0, slice(6, 12)),
                  ((14, 'a', 'iv'), 0, slice(15, 20))],
       marks=[5, 2], notation='3 + 2 for the axes, 2 for the line', checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(2, None, 'iii', topic='phys-u2', concept='apparatus-with-u-and-v-marked',
       source='pdf',
       from_runs=[((2, None, 'iii'), 0, slice(7, 10)),
                  ((2, None, 'iii'), 0, slice(11, 13)),
                  ((2, None, 'iii'), 0, slice(14, 16))],
       marks=[3, 3, 3], first_sentence=True)

A.card(5, None, 'i', topic='phys-u2', concept='circuit-for-a-diode-in-forward-bias',
       source='pdf',
       from_runs=[((5, None, 'i'), 0, slice(0, 3)),
                  ((5, None, 'i'), 0, slice(4, 8)),
                  ((5, None, 'i'), 0, slice(9, 13)),
                  ((5, None, 'i'), 0, slice(14, 17))],
       marks=[3, 3, 3, 3])

A.card(5, None, 'iv', topic='phys-u2', concept='circuit-for-a-diode-in-reverse-bias',
       source='pdf',
       from_runs=[((5, None, 'iv'), 0, slice(0, 4)),
                  ((5, None, 'iv'), 0, slice(5, 11))],
       marks=[3, 3],
       notes='The ammeter changes with the bias: a milliammeter in forward bias, a '
             'microammeter in reverse, because the reverse current is tiny.')


# ── Closing the remaining open parts ───────────────────────────────────────
A.card(1, None, 'i', topic='phys-u2', concept='apparatus-for-the-free-fall-experiment',
       source='pdf', from_run=((1, None, 'i'), 0, slice(0, 9)), marks=[9],
       notation='any three correct items merit 3 × 3',
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(1, None, 'ii', topic='phys-u2', concept='indicating-the-fall-distance',
       source='pdf', use=[0], marks=[3])

A.card(2, None, 'v', topic='phys-u2', concept='focal-length-from-the-mirror-formula',
       source='pdf',
       from_runs=[((2, None, 'v'), 0, slice(0, 5)),
                  ((2, None, 'v'), 0, slice(6, 12)),
                  ((2, None, 'v'), 0, slice(13, 17)),
                  ((2, None, 'v'), 0, slice(18, 23)),
                  ((2, None, 'v'), 0, slice(26, 34))],
       marks=[2, 2, 2, 2, 2],
       notation='the two further calculations score 2 × 1',
       checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(5, None, 'ii', topic='phys-u2', concept='graph-of-current-against-voltage-in-forward-bias',
       source='pdf',
       from_runs=[((5, None, 'ii'), 0, slice(0, 2)),
                  ((5, None, 'ii'), 0, slice(3, 6)),
                  ((5, None, 'ii'), 0, slice(7, 11))],
       marks=[3, 3, 3],
       checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(5, None, 'v', topic='phys-u2', concept='graph-of-current-against-voltage-in-reverse-bias',
       source='pdf', first_sentence=True,
       from_runs=[((5, None, 'v'), 0, slice(0, 2)),
                  ((5, None, 'v'), 0, slice(3, 5))],
       marks=[3, 4])

A.card(6, 'e', None, topic='phys-2-3', concept='turning-light-through-90-degrees-with-a-prism',
       source='pdf', card_id='phys-2023-hl-q6-e',
       from_runs=[((6, 'e', None), 0, slice(0, 7)),
                  ((6, 'e', None), 0, slice(8, 15)),
                  ((6, 'e', None), 0, slice(16, 19))],
       marks=[2, 2, 3])

# Q8(iii) asks for three sketches — f against √T, f against 1/l, f against
# 1/√μ — and six rows breach the five-row cap, so each sketch is its own card
# under the deck's split-item convention (the suffix rides the citation).
A.card(8, None, 'iii', topic='phys-2-6', concept='sketch-f-against-root-tension',
       source='pdf', card_id='phys-2023-hl-q8-iii-t',
       from_runs=[((8, None, 'iii'), 0, slice(12, 18)),
                  ((8, None, 'iii'), 0, slice(19, 24))],
       marks=[2, 2],
       checked='The paper ends this question on its printed list of variable pairs — (a) f and T (b) f and l (c) f and µ — rather than punctuation. The question itself is complete.',
       notes='Sketch (a): f against √T for a stretched string — labelled axes, '
             'straight line through the origin.')

A.card(8, None, 'iii', topic='phys-2-6', concept='sketch-f-against-inverse-length',
       source='pdf', card_id='phys-2023-hl-q8-iii-l',
       from_runs=[((8, None, 'iii'), 0, slice(25, 31)),
                  ((8, None, 'iii'), 0, slice(32, 37))],
       marks=[2, 2],
       checked='The paper ends this question on its printed list of variable pairs rather than punctuation. The question itself is complete.',
       notes='Sketch (b): f against 1/l — labelled axes, straight line through '
             'the origin.')

A.card(8, None, 'iii', topic='phys-2-6', concept='sketch-f-against-inverse-root-mu',
       source='pdf', card_id='phys-2023-hl-q8-iii-mu',
       from_runs=[((8, None, 'iii'), 0, slice(38, 44)),
                  ((8, None, 'iii'), 0, slice(45, 50))],
       marks=[2, 2],
       checked='The paper ends this question on its printed list of variable pairs rather than punctuation. The question itself is complete.',
       notes='Sketch (c): f against 1/√μ, μ the linear density (mass per unit '
             'length) — labelled axes, straight line through the origin.')

# The three sketch cards share one part; the item rides the citation so the
# build's one-card-per-ref rule sees three distinct addresses (the CS split
# convention: '… — safety training').
for _c in A.cards:
    if _c['id'] == 'phys-2023-hl-q8-iii-t':
        _c['questionRef'] += ' — f and √T'
    elif _c['id'] == 'phys-2023-hl-q8-iii-l':
        _c['questionRef'] += ' — f and 1/l'
    elif _c['id'] == 'phys-2023-hl-q8-iii-mu':
        _c['questionRef'] += ' — f and 1/√μ'

A.card(9, None, 'i', topic='phys-4-4', concept='alpha-decay-equation',
       source='pdf', from_run=((9, None, 'i'), 1, slice(3, 11)), marks=[8],
       notation='8 × 1',
       notes='The scheme prints the parent nuclide, plutonium-238, in a maths font '
             'that the text layer mangles, so the row begins at the arrow. The '
             'numbers beside each symbol are its atomic and mass numbers, and the '
             'scheme deducts 3 for each additional incorrect species.')

A.card(9, None, 'iv', topic='phys-2-1', concept='arrangement-of-a-thermocouple',
       source='pdf', first_sentence=True,
       from_runs=[((9, None, 'iv'), 0, slice(0, 3)),
                  ((9, None, 'iv'), 0, slice(4, 9)),
                  ((9, None, 'iv'), 0, slice(10, 16))],
       marks=[3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(10, None, 'iii', topic='phys-3-2', concept='electric-field-around-a-charged-dome',
       source='pdf',
       from_runs=[((10, None, 'iii'), 0, slice(0, 3)),
                  ((10, None, 'iii'), 0, slice(4, 8))],
       marks=[3, 3])

A.card(12, 'a', 'iii', topic='phys-4-5', concept='pair-production-equation',
       source='pdf',
       from_runs=[((11, 'a', 'iii'), 1, slice(0, 2)),
                  ((11, 'a', 'iii'), 0, slice(0, 2)),
                  ((11, 'a', 'iii'), 3, slice(0, 7)),
                  ((11, 'a', 'iii'), 2, slice(0, 1))],
       use=[[0, 1], [2, 3]], marks=[3, 3],
       notes='Read as two complete equations: the particle form γ = e + e, where '
             'the digits around each e are its flattened subscript charge (–1, +1) '
             'and superscript mass number (0), or the energy form hf = 2mec2. Pair '
             'each left-hand side with its own right-hand side.')

A.card(12, 'b', 'i', topic='phys-3-3', concept='structure-of-diode-and-transistor',
       source='pdf', first_sentence=True,
       from_runs=[((11, 'b', 'i'), 0, slice(0, 5)),
                  ((11, 'b', 'i'), 0, slice(6, 12))],
       marks=[6, 6],
       notes='The a and b heading the rows mark the two diagrams: (a) the diode, '
             '(b) the transistor.')

A.card(12, 'b', 'vii', topic='phys-3-3', concept='parts-of-an-electromagnetic-relay',
       source='pdf',
       from_runs=[((11, 'b', 'vii'), 1, slice(0, 3)),
                  ((11, 'b', 'vii'), 1, slice(4, 5)),
                  ((11, 'b', 'vii'), 1, slice(6, 8))],
       marks=[2, 2, 2],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.emit()
