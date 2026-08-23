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

A.card(16, 'b', 'i', topic='bio-3-4', concept='parts-of-the-male-reproductive-system',
       source='pdf', from_run=((16, None, 'i'), 0, slice(0, 9)), marks=[6],
       notation='3 + 3, and only 3 if any one of the four is missing',
       checked='The question runs its list of parts to label on after the instruction '
               'without punctuation between them, which is why the text is flagged. Both '
               'halves are the question as printed.')

A.emit()
