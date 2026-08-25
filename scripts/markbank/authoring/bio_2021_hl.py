#!/usr/bin/env python3
"""Biology 2021 Higher Level — Question 6, the true/false statements.

The scheme answers these by putting a tick glyph in a True or False column. The
glyph leaves an empty block behind in the text layer, so no parser can read it —
and worse, with nothing to attribute to Question 6 the parsers roll straight on
and hand it Question 7's marking points, which are about tendons, biceps and
the axial skeleton. Joining the two documents on their keys would have put those
answers under these statements.

So the questions are lifted from the paper as always and each answer was read
off the rendered scheme page (2021 HL scheme, page 9). The deck already carries
this convention — see bio-2025-ol-q3-a.

Q6 is marked 6(3) + 2 across seven statements: 3 marks a correct response, with
the tariff capped at 20, so a card carries the 3 its own statement is worth.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2021, 'hl')
READ = ('The scheme answers this by ticking a True/False column, and the tick is a '
        'glyph the text extraction drops. Read from page 9 of the 2021 Higher Level '
        'marking scheme. Q6 is marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'True',  'bio-2-4', 'adrenaline-release'),
        ('b', 'True',  'bio-2-2', 'plants-respire-as-well-as-photosynthesise'),
        ('c', 'False', 'bio-2-4', 'neurotransmitters-act-at-the-synapse'),
        ('d', 'False', 'bio-2-6', 'the-potato-is-a-stem-tuber'),
        ('e', 'True',  'bio-1-3', 'tissue-culture-medium'),
        ('f', 'False', 'bio-2-4', 'bones-of-the-middle-ear'),
        ('g', 'True',  'bio-2-6', 'monocotyledons-are-herbaceous')):
    A.card(6, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', suffix='', notes=READ, stem=False)


# ── Parts the deck had not carded ──────────────────────────────────────────
# The scheme answers these on the same line as the question it is repeating, so
# each answer is taken out of that line rather than off one of its own. The
# leading asterisk on an essential answer is an annotation to the examiner and
# no card in any deck carries one.
A.card(10, 'b', 'iii', topic='bio-u1', concept='the-purpose-of-a-control-plate',
       source='pdf', from_run=((10, 'b', 'iii'), 0, slice(10, 20)), marks=[3])

A.card(10, 'b', 'v', topic='bio-3-3', concept='why-urban-and-rural-plates-differ',
       source='pdf', use=[[1, 2, 3]], marks=[3],
       notes='The scheme accepts the comparison either way round, and names smoke, '
             'sulphur dioxide and harmful chemicals as the pollution meant.')

A.card(12, 'b', 'i', topic='bio-3-2', concept='genotype-heterozygous-for-two-traits',
       source='pdf', from_run=((12, 'b', 'i'), 0, slice(10, 11)), marks=[3])

A.card(14, 'c', 'i', topic='bio-2-4', concept='which-leaf-transpires-least',
       source='pdf',
       from_runs=[((14, 'c', 'i'), 0, slice(12, 13)),
                  ((14, 'c', 'i'), 1, slice(3, None))],
       marks=[3, 3],
       notes='The three plants are shown in the paper with their stomata counted, and '
             'the scheme wants the one with fewest.')

A.card(12, 'b', 'v', topic='bio-3-2', concept='which-offspring-genotypes-show-variation',
       source='pdf',
       from_runs=[((12, 'b', 'v'), 0, slice(9, 10)),
                  ((12, 'b', 'v'), 0, slice(11, 12))],
       marks=[3, 3],
       checked='The paper prints the part mark "(27)" after the question, so the text ends '
               'on a bracketed number rather than punctuation.')

A.card(13, 'b', 'i', topic='bio-2-2', concept='the-name-of-stage-1-of-respiration',
       source='pdf', from_run=((13, 'b', 'i'), 0, slice(6, 7)), marks=[3])

A.card(13, 'b', 'ii', topic='bio-2-2', concept='the-molecule-released-in-stage-1',
       source='pdf', from_run=((13, 'b', 'ii'), 0, slice(3, 8)), marks=[3])

A.card(13, 'b', 'iii', topic='bio-2-2', concept='how-atp-and-nadh-are-made',
       source='pdf',
       from_runs=[((13, 'b', 'iii'), 1, slice(2, None)),
                  ((13, 'b', 'iii'), 2, slice(4, None))],
       marks=[3, 3],
       notes='Which answer applies depends on which molecule was named at part (ii) — the '
             'scheme gives one route for ATP and one for NADH.')


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(9, 'b', 'iv', topic='bio-2-1', concept='enzyme-activity-against-temperature-curve',
       source='pdf', from_run=((9, 'b', 'iv'), 0, slice(17, None)), marks=[3],
       notes='The curve rises to a peak at the optimum and falls away sharply after it, '
             'because the enzyme denatures rather than merely slowing.')

A.card(16, 'b', 'i', topic='bio-2-5', concept='parts-of-the-male-reproductive-system',
       source='pdf', from_run=((16, None, 'i'), 0, slice(0, 9)), marks=[6],
       notation='3 + 3, and only 3 if any one of the four is missing',
       checked='The question runs its list of parts to label on after the instruction '
               'without punctuation between them, which is why the text is flagged. Both '
               'halves are the question as printed.')


# ══ Second pass: the asks reconcile still reported open ════════════════════
# Everything below was open because a parser could not attribute the scheme's
# answer to the part the paper numbers. In Section C the PDF parser runs one
# question behind from Question 11 on (the "Section C Best 3" banner is read as
# a question head), so the answer to Q11(a)(i) sits under its key (10, 'a', 'i')
# and Q17(d)'s answers sit interleaved with Q17(a)-(c) under (17, None, ...).
# The parent keys below are those parser keys; the citation on every card is the
# PAPER's own numbering, which is what A.card() writes.


# ── Q2, the nitrogen cycle ────────────────────────────────────────────────
# Q2 is marked '6(3) + 2' — the ladder under it (1 -> 3 ... 6 -> 18, 7 -> 20)
# fixes each of the first six correct responses at 3 marks, which is the tariff
# bio-2021-hl-q2-a and -q2-d already carry.
#
# Q2(b) and Q2(c) stay uncarded. Their answers are a letter-to-arrow mapping on
# the nitrogen-cycle diagram — "A: Nitrogen fixation B: Denitrification" and
# "C: Nitrifying (bacteria)" — and that diagram is vector artwork on page 4 of
# the Section A paper which no extractor has ever put in the figure library
# (components/MarkBank/figures.json has nothing for 2021 HL paper 1 page 4). A
# card that asks which process is at A while showing no A teaches nothing.
A.card(2, 'e', topic='bio-3-2', concept='where-decomposers-act-in-the-nitrogen-cycle',
       from_run=((1, 'e', None), 0, slice(0, None)), marks=[3], notation='6(3) + 2',
       notes='The scheme keys this answer under its own Question 1 while the paper prints '
             'Question 2. It is a mark-the-diagram ask, but the scheme answers it in words '
             '— the arrows that end at soil ammonia — and the paper stem names every box '
             'in the cycle, so the answer stands without the artwork.')


# ── Q5, the human embryo diagram ──────────────────────────────────────────
# Q5(a), Q5(c) and Q5(d) stay uncarded, for the same reason as Q2(b)-(c) and no
# other. The scheme answers them "A: Ovulation", "B: Morula C: Blastocyst" and
# "Implantation (or described)", but A, B, C and D are arrowheads on a drawing
# of the female reproductive tract: A at the ovary, B and C at two points along
# the fallopian tube, D at the uterine wall. Which stage is B rather than C is
# purely positional, the drawing is not in the figure library, and the paper
# stem this deck would print alongside comes out of the text layer mangled
# ("... development of a human embryo. B Fertilisation").


# ── Q11, ecology ──────────────────────────────────────────────────────────
A.card(11, 'a', 'i', topic='bio-3-1', concept='pyramid-of-numbers-for-a-food-chain',
       source='pdf', from_run=((10, 'a', 'i'), 2, slice(0, None)), marks=[3],
       checked='The paper sets the food chain out with drawn arrows between the organisms '
               'and the text layer drops them, so the lifted text reads "Cowslips Moth Bat '
               'Mites". Page 2 of the Section C paper prints exactly those four organisms, '
               'in that order, joined by arrows, and nothing else in the part.',
       notes='The scheme prices this part at 3 + 3. The other 3 is for the shape of the '
             'pyramid, which the scheme states by printing three drawn alternatives rather '
             'than by describing them, so only the half it puts in words is on this card.')

A.card(11, 'b', 'iii', topic='bio-3-1', concept='sketching-a-predator-prey-graph',
       use=[0, 1, 2], marks=[3, 3, 3],
       notes='A drawing question the scheme answers in words: it prices the axes, the pair '
             'of repeating curves, and the predator curve sitting lower and lagging behind '
             'the prey, at 3 marks each.')


# ── Q12, genetics ─────────────────────────────────────────────────────────
A.card(12, 'b', 'iv', topic='bio-1-4', concept='punnett-square-for-a-dihybrid-test-cross',
       source='pdf',
       from_runs=[((12, 'b', 'iv'), 1, slice(8, 9)),
                  ((12, 'b', 'iv'), 1, slice(13, 26))],
       marks=[3, 3], notation='3 + 3 + 3, the third for the Punnet square itself',
       notes='Row one is the gametes of the other parent — homozygous recessive for both '
             'traits, so it makes only one kind — and row two the genotypes of the '
             'offspring. The scheme pays a third 3 marks for the Punnet square itself, '
             'before anything is written into it; that row is left off because "Punnet '
             'square" is the question repeated back, not an answer to learn.')

# 2021 HL Q12(c)(iii) and Q12(c)(iv) are not carded. The scheme's entire answer
# to each is "Any valid example" — for one application of genetic engineering in
# animals and one in plants. There is no marking content to lift: a card whose
# back reads "any valid example" tells a student only what they already knew
# from the question.


# ── Q13, respiration ──────────────────────────────────────────────────────
A.card(13, 'b', 'ix', topic='bio-2-2', concept='energy-released-with-and-without-oxygen',
       source='pdf', from_run=((13, 'b', 'viii'), 2, slice(0, None)), marks=[3],
       checked='The paper prints the part mark "(27)" after the question, so the text ends '
               'on a bracketed number rather than punctuation. Page 4 of the Section C '
               'paper carries the question in full above it.',
       notes='The scheme sets this out on the same line as part (viii), under its own '
             '"(ix)" cue, and wants both halves of the comparison for the one mark.')


# ── Q14, the xylem vessel drawing ─────────────────────────────────────────
# The scheme prices the drawing and the labels on two separate ladders — one
# response at 3 for the drawing, then 1, 2 or 3 marks for one, two or three
# correct labels — so the labels are three rows of 1 rather than one row of 3.
A.card(14, 'c', 'iv', topic='bio-2-6', concept='ls-of-a-xylem-vessel',
       source='pdf',
       from_runs=[((14, None, 'iv'), 0, slice(12, 19)),
                  ((14, 'c', None), 0, slice(1, 2)),
                  ((14, 'c', None), 1, slice(0, None)),
                  ((14, 'c', None), 2, slice(0, None))],
       marks=[3, 1, 1, 1], notation='Drawing 3; Labels 3(1)', stem=False,
       checked='The paper prints the part mark "(24)" after the question, so the text ends '
               'on a bracketed number. Page 5 of the Section C paper prints the question as '
               'the last part of 14(c).',
       notes='The paper asks for a longitudinal section; the scheme calls it a detailed '
             'longitudinal section. The three labels are worth one mark each, to a maximum '
             'of three.')


# ── Q15, seeds ────────────────────────────────────────────────────────────
A.card(15, 'c', 'i', topic='bio-2-5', concept='germination-dispersal-and-dormancy',
       source='pdf',
       from_runs=[((15, 'c', 'i'), 0, slice(0, 15)),
                  ((15, 'c', 'i'), 0, slice(16, 29)),
                  ((15, 'c', 'i'), 0, slice(30, 43))],
       marks=[3, 3, 3],
       notes='The underlined terms are germination, dispersal and dormancy, from the '
             'sentence the paper prints above the part; the scheme names each one at the '
             'head of its own definition, so each row says which term it explains.')


# ── Q17(d), the red onion osmosis images ──────────────────────────────────
# The figure carries BOTH panels: biology-2021-HL-paper2-p10-i0 is manifested as
# "Two side-by-side rectangular greyscale micrograph-style panels ... Left panel,
# headed 'A' ... Right panel, headed 'B'", verified complete against a full
# render of page 10. Parts (iii) to (vi) reason from those panels and are
# answerable with them on the card.
#
# The stem is suppressed on all four: paper.stem(17, 'd') runs off the end of
# the question and comes back with the back-cover matter ("Do not hand this
# question paper up ... Copyright notice ..."), which is not a stem.
FIG = 'biology-2021-HL-paper2-p10-i0'

A.card(17, 'd', 'iii', topic='bio-1-3', concept='comparing-two-bathing-solutions',
       source='pdf', from_run=((17, None, 'iii'), 3, slice(0, None)), marks=[3],
       figure=FIG, stem=False,
       notes='The cells in panel B have pulled away from their walls, which is what the '
             'answer is read off. The scheme interleaves Q17(d) with Q17(a)-(c) because '
             'the four options run side by side on its page.')

A.card(17, 'd', 'iv', topic='bio-1-3', concept='osmosis-out-of-a-plant-cell',
       source='pdf',
       from_runs=[((17, None, 'iv'), 2, slice(9, 10)),
                  ((17, None, 'iv'), 2, slice(12, 22)),
                  ((17, None, 'iv'), 3, slice(0, None))],
       marks=[3, 3, 3], figure=FIG, stem=False,
       notes='Naming the process earns 3; the description earns the other 6, and the '
             'scheme wants both the direction of the water and the membrane it crosses.')

A.card(17, 'd', 'v', topic='bio-1-3', concept='reversing-plasmolysis',
       source='pdf', from_run=((17, None, 'v'), 11, slice(10, 18)), marks=[3],
       figure=FIG, stem=False)

A.card(17, 'd', 'vi', topic='bio-1-3', concept='osmosis-applied-to-food-production',
       source='pdf', from_run=((17, None, 'vi'), 6, slice(0, 21)), marks=[3],
       figure=FIG, stem=False,
       notes='The scheme runs the answer straight into part (vii) on the same line, so the '
             'lift stops where the "(vii)" cue starts.')

A.emit()
