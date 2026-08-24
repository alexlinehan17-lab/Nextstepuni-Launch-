#!/usr/bin/env python3
"""Physics 2021 Higher Level — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'; the markdown extraction has no points for any of these parts. The
scheme reprints the question above its own answer, which is why index 0 is
never used — it is the cue, not a marking point.

Only parts whose scheme prints an answer are here. Where it prints the marking
convention instead — "apparatus, method, observation (3 × 3)" against a
describe-an-experiment part — there is nothing to put on the back of a card, and
Q8(ii), Q10(ii) and Q14(b)(ii) are left alone for the reason Q10(i)'s note
already gives. Q2(iv) is the same shape: "On your diagram, indicate u and v.
(2 × 3)" is a tariff against the candidate's own drawing, with no answer content
printed. Q10(iii) prints "correct shape (3) correct direction (3)" — grader
labels for the drawn field, naming neither the shape nor the direction, unlike
Q12(vi) whose scheme names "parallel field lines" and "from + to −". And the
nuclear equations of Q11(i) and Q13(a)(iv) are set in a font the text layer
mangles — "4 → C6", "1 + pത -1" — the same class as 2022 HL Q10's equations.
None of those five parts can be carded from this scheme.

Q7(ix) is not here either: the scheme itemises its answer (weight arrow, tension
arrow, 3 marks each), but the question is about a sphere B hanging from a string
in a diagram drawn on page 6 of the paper, and the paper's stem for Q7 both
loses that sentence and carries the later "The string is cut..." line, which
would mislead. The card waits for a crop of that drawn diagram.

The pdf parser keys Section A's answers oddly: a preamble block sets the
question counter before "SECTION A ... 1." arrives in a block whose head the
parser cannot see, so Q1's parts land under (11, ...) and the real Q11's under
(1, ...); likewise Q6's letters land under (5, ...) and Q7's run merges into
(0, None, 'iii'). The from_runs parents below name the keys where the parser
put each block — the text itself is still the scheme's, and every row still
traces through the gate against the markdown copy.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2021, 'hl')
MARK = ('The paper prints the part mark in brackets after the question, so the text ends '
        'on a number rather than punctuation. The question itself is complete.')

A.card(4, None, 'vi', topic='phys-3-3', concept='resistivity-of-a-metal-calculation',
       source='pdf', use=[1, 3, 4], marks=[3, 3, 3], checked=MARK,
       notes='The scheme lists "substitution" between the formula and the area with no mark '
             'of its own, so it is not a row here.')

A.card(8, None, 'iv', topic='phys-2-6', concept='deriving-the-grating-formula',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3], checked=MARK)

A.card(10, None, 'vi', topic='phys-3-6', concept='emf-induced-in-a-loop-entering-a-field',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3],
       notes='Each line carries two routes to the same mark, separated by the scheme’s '
             'own solidus: the flux route on the left, the Bsv route on the right.')

A.card(12, None, 'vi', topic='phys-3-2', concept='field-pattern-in-a-parallel-plate-capacitor',
       source='pdf', use=[1, 2], marks=[3, 3], first_sentence=True)

A.card(13, 'b', 'iv', topic='phys-3-3', concept='structure-of-a-bipolar-transistor',
       source='pdf', use=[1], marks=[7], checked=MARK,
       notes='The scheme splits the seven marks 3 + 2 + 2 across the three layers.')

A.card(14, 'b', 'iii', topic='phys-2-5', concept='doppler-speed-of-a-source',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3])

# 2021 HL Q14(c)(ii) is not here. The paper prints it as one line of a list of
# conditions — "f > fo , f is increasing and I is constant," — which is not a
# question on its own, and a card would have to supply the sentence introducing
# the list. That sentence would be written rather than lifted, so the part is
# left for a pass that can carry the stem.

A.card(2, None, 'v', topic='phys-u2', concept='focal-length-from-all-the-data',
       source='pdf', use=[1, 2], marks=[3, 3], first_sentence=True,
       notes='The scheme takes a mark off if the values are not averaged.')

A.card(2, None, 'vii', topic='phys-u2', concept='focal-length-from-a-graph',
       source='pdf', use=[1, 2], marks=[3, 3], checked=MARK)

A.card(3, None, 'iv', topic='phys-u2', concept='linear-density-from-a-graph',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 2, 3, 2], first_sentence=True)

A.card(4, None, 'iv', topic='phys-u2', concept='reading-a-temperature-off-a-resistance-graph',
       source='pdf', use=[1], marks=[3], first_sentence=True)

A.card(5, None, 'iv', topic='phys-u2', concept='average-resistance-of-a-heating-coil',
       source='pdf', use=[1, 2, 4, 5, 6], marks=[3, 3, 3, 2, 2], first_sentence=True,
       notes='The scheme prints the two energy expressions on either side of the equation '
             'it wants them set equal in.')

A.card(12, None, 'v', topic='phys-3-2', concept='why-parallel-capacitors-add',
       source='pdf', use=[1], marks=[3], first_sentence=True)


# ── Drawing questions whose scheme says what the drawing must show ─────────
# A question that asks for a diagram is not automatically uncardable. Where the
# scheme answers it with a marking convention — "apparatus, method, observation"
# — there is nothing to put on a card. Where it says WHAT the drawing must
# contain, that is the answer, and the card asks a student to say what they would
# draw and what earns each mark.
A.card(4, None, 'iii', topic='phys-u2', concept='graph-for-resistance-against-temperature',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3])

A.card(5, None, 'iii', topic='phys-u2', concept='graph-to-verify-joules-law',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3],
       notes='Joule\'s law is verified against the square of the current, so the first '
             'mark is for working those values out before plotting anything.')

A.card(9, None, 'v', topic='phys-2-1', concept='parts-of-a-heat-pump',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3])

A.card(13, 'b', 'ii', topic='phys-3-3', concept='circuit-of-a-bridge-rectifier',
       source='pdf', use=[1, 2], marks=[4, 3], first_sentence=True)

A.card(13, 'b', 'iii', topic='phys-3-3', concept='input-and-output-of-a-bridge-rectifier',
       source='pdf', use=[1, 2, 3], marks=[3, 2, 2], checked=MARK)

A.card(13, 'b', 'v', topic='phys-3-3', concept='circuit-of-a-voltage-amplifier',
       source='pdf', use=[1, 2, 3, 4, 5], marks=[3, 3, 3, 3, 2], checked=MARK)

A.card(14, 'b', 'iv', topic='phys-2-3', concept='refraction-of-sound-from-water-into-air',
       source='pdf', use=[1, 2], marks=[3, 2], first_sentence=True)

A.card(2, None, 'iii', topic='phys-u2', concept='apparatus-for-the-concave-mirror-experiment',
       source='pdf', from_run=((2, None, 'iii'), 1, slice(0, 5)), marks=[4],
       notation='4 × 1',
       notes='The scheme takes a mark off if there is no diagram at all, and another if '
             'it carries no labels.')


# ── Section A: the pendulum experiment, whose answers the parser keys under 11 ─
A.card(1, None, 'i', topic='phys-u2', concept='apparatus-for-the-simple-pendulum-experiment',
       source='pdf',
       from_runs=[((11, None, 'i'), 1, slice(0, 4)),
                  ((11, None, 'i'), 2, slice(0, 1)),
                  ((11, None, 'i'), 3, slice(0, 4)),
                  ((11, None, 'i'), 4, slice(0, 1)),
                  ((11, None, 'i'), 5, slice(0, 2))],
       use=[0, 1, [2, 3, 4]], marks=[3, 3, 3],
       notes='The scheme\'s solidus offers split cork or similar, timer and metre stick as '
             'alternatives for the final three marks. It takes a mark off if there is no '
             'diagram at all, and another if it carries no labels.')

A.card(1, None, 'ii', topic='phys-u2',
       concept='marking-the-suspension-point-and-length-of-the-pendulum',
       source='pdf',
       from_runs=[((11, 'a', None), 1, slice(0, 6)),
                  ((11, 'b', None), 1, slice(0, 5)),
                  ((11, 'b', None), 2, slice(0, 4))],
       marks=[3, 2, 2],
       notes='The distance l earns its marks in two halves: two for starting at the fixed '
             'point of suspension, two for ending at the midpoint of the bob.')

A.card(1, None, 'iv', topic='phys-u2', concept='graph-to-calculate-g',
       source='pdf',
       from_runs=[((11, 'b', 'iv'), 1, slice(0, 3)),
                  ((11, 'b', 'iv'), 2, slice(0, 2)),
                  ((11, 'b', 'iv'), 3, slice(0, 3)),
                  ((11, 'b', 'iv'), 4, slice(0, 4))],
       marks=[3, 3, 3, 3],
       notes='The graph needs the period squared, so the first mark is for working out '
             '(t/20)2 before plotting anything.')

A.card(1, None, 'v', topic='phys-u2', concept='g-from-the-slope-of-the-graph',
       source='pdf', checked=MARK,
       from_runs=[((11, 'b', 'v'), 1, slice(0, 2)),
                  ((11, 'b', 'v'), 2, slice(0, 5))],
       marks=[3, 3])


# ── The remaining Section A drawing parts whose scheme says what to draw ───
A.card(2, None, 'vi', topic='phys-u2', concept='sketching-the-focal-length-graph',
       source='pdf',
       from_runs=[((2, None, 'vi'), 1, slice(0, None)),
                  ((2, None, 'vi'), 2, slice(0, None)),
                  ((2, None, 'v'), 6, slice(0, None))],
       marks=[3, 3, 3],
       notes='Each row carries the two graphs the scheme accepts, separated by its own '
             'double solidus: 1/v against 1/u on the left, v against u on the right.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-stretched-string-experiment',
       source='pdf', use=[1, [2, 3], [4, 5, 6], 7], marks=[3, 3, 3, 3],
       notes='The scheme\'s solidus makes newtonmeter and weights-and-pan alternatives, and '
             'likewise metre stick, bridge(s) and paper rider. It takes a mark off if there '
             'is no diagram at all, and another if it carries no labels.')

A.card(3, None, 'iii', topic='phys-u2', concept='graph-of-frequency-against-tension',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3],
       notes='The relationship is linear between f2 and T (or f and √T), so the first mark '
             'is for working out those values before plotting anything.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-for-the-resistance-temperature-experiment',
       source='pdf', use=[1], marks=[12], notation='4 × 3',
       notes='The scheme takes a mark off if there is no diagram at all, and another if '
             'it carries no labels.')

A.card(5, None, 'i', topic='phys-u2', concept='apparatus-for-the-joules-law-experiment',
       source='pdf', use=[1, 2, 3, [4, 5]], marks=[3, 3, 3, 3],
       notes='The scheme\'s solidus makes thermometer and coil-in-water alternatives for '
             'the final three marks. It takes a mark off if there is no diagram at all, '
             'and another if it carries no labels.')


# ── Question 6 parts, whose answers the parser keys under 5 ────────────────
# The deck's Q6 siblings carry a dash before the letter — phys-2021-hl-q6-e —
# so these three follow them rather than the id the letter would generate.
A.card(6, 'f', None, topic='phys-2-5', concept='second-harmonic-in-an-open-pipe',
       source='pdf', card_id='phys-2021-hl-q6-f',
       from_runs=[((5, 'f', None), 1, slice(0, 5)),
                  ((5, 'f', None), 2, slice(0, None))],
       marks=[4, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(6, 'h', None, topic='phys-2-4', concept='mixing-two-primary-colours',
       source='pdf', card_id='phys-2021-hl-q6-h',
       from_runs=[((5, 'h', None), 1, slice(0, None)),
                  ((5, 'h', None), 2, slice(0, None))],
       marks=[4, 3],
       notes='The scheme\'s double solidus separates three self-consistent routes, read in '
             'column: red and blue make magenta, blue and green make cyan, green and red '
             'make yellow. Each named primary earns two marks, the mixture three.')

A.card(6, 'j', None, topic='phys-3-3', concept='measuring-a-diode-in-reverse-bias',
       source='pdf', card_id='phys-2021-hl-q6-j',
       from_runs=[((5, 'h', 'i'), 4, slice(0, 5)),
                  ((5, 'h', 'i'), 5, slice(0, 5)),
                  ((5, 'h', 'i'), 6, slice(0, 5))],
       marks=[3, 2, 2])


# ── Question 11 and 13(a), whose answers the parser keys under 1 ───────────
A.card(11, None, 'ii', topic='phys-4-5', concept='kinetic-energy-from-the-mass-defect',
       source='pdf', first_sentence=True,
       from_runs=[((1, None, 'ii'), 0, slice(0, 3)),
                  ((1, None, 'ii'), 0, slice(4, 9)),
                  ((1, None, 'ii'), 0, slice(10, 13)),
                  ((1, None, 'ii'), 0, slice(14, 21))],
       marks=[3, 3, 3, 3],
       notes='The event is the one the stem describes — an alpha particle absorbed by a '
             'beryllium-9 nucleus, emitting a neutron. The nuclide masses come from the '
             'formulae and tables booklet; the paper prints none.')

A.card(11, None, 'iv', topic='phys-4-4', concept='principle-of-operation-of-a-radiation-detector',
       source='pdf', first_sentence=True,
       from_runs=[((1, None, 'iv'), 0, slice(0, 1)),
                  ((1, None, 'iv'), 1, slice(0, 8)),
                  ((1, None, 'iv'), 1, slice(9, 15)),
                  ((1, None, 'iv'), 1, slice(16, 22))],
       use=[[1, 0], 2, 3], marks=[3, 3, 3],
       notes='Each row carries three mutually exclusive routes separated by the scheme\'s '
             'double solidus: a G-M tube, a solid-state detector, a charged gold leaf '
             'electroscope — the paper\'s part (iii) names the first two. On the first line '
             'the scheme offers gas and anode as alternatives for the G-M route. It takes '
             'a mark off if there is no diagram.')

A.card(11, None, 'v', topic='phys-4-3', concept='the-gold-foil-experiment',
       source='pdf',
       from_runs=[((1, None, 'v'), 0, slice(0, 5)),
                  ((1, None, 'v'), 0, slice(6, 11))],
       marks=[3, 3],
       notes='The scheme takes a mark off if there is no diagram.')

# Q13(a)(v) already ships as a hand-authored card (phys-2021-hl-q13a-v);
# it looked open only because the paper census loses the (13,'a','v') key.
# lib's section rule (A up to question 12) fits the papers it was written for,
# not Physics, whose Section B starts at question 6. The deck's shipped Q6 and
# Q11 cards already say B, so the new siblings match them; this script's older
# cards shipped as A and are left exactly as they shipped.
for c in A.cards:
    if c['id'].startswith(('phys-2021-hl-q6-', 'phys-2021-hl-q11-')):
        c['section'] = 'B'

A.emit()
