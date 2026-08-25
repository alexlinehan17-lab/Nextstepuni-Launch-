#!/usr/bin/env python3
"""Biology 2022 Ordinary Level — Question 6, the true/false statements.

The scheme answers these by ticking a True or False column, and the tick is a
glyph the text layer drops. With nothing to attribute to this question both
parsers roll on and hand it the NEXT question's marking points, so joining the
two documents on their keys would put the wrong answers under these statements.

Questions lifted from the paper as always; each answer read off page 9 of the
2022 Ordinary Level marking scheme. Marked 6(3) + 2 across seven statements.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2022, 'ol')
READ = ('The scheme answers this by ticking a True/False column and the tick is a '
        'glyph the text extraction drops, so it was read from page 9 of the 2022 '
        'Ordinary Level marking scheme. Q6 is marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'True', 'bio-2-4', 'endocrine-glands-produce-hormones'),
        ('b', 'True', 'bio-2-5', 'where-fertilisation-occurs'),
        ('c', 'False', 'bio-2-6', 'which-organ-produces-hydrochloric-acid'),
        ('d', 'False', 'bio-2-6', 'which-organ-produces-bile'),
        ('e', 'True', 'bio-2-4', 'nerve-cells-produce-neurotransmitters'),
        ('f', 'False', 'bio-3-2', 'what-produces-antibiotics'),
        ('g', 'True', 'bio-2-6', 'salivary-glands-produce-amylase'),
):
    A.card(6, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False)

# ── Q7(b): the matching table ─────────────────────────────────────────────
# The scheme prints the description and the term it matches on one line, and
# its own mark column gives four.
A.card(7, 'b', topic='bio-u1', concept='what-a-hypothesis-is',
       source='pdf', from_run=((6, 'b', None), 0, slice(6, 7)), marks=[4],
       checked='The paper prints this part as a Column A description in a matching table, so it has no verb of its own. The instruction to match it to a term in the list sits in the question stem the card already carries.')

A.card(8, 'b', 'iii', topic='bio-u1', concept='percentage-frequency-from-a-quadrat-table',
       source='pdf',
       from_runs=[((8, 'b', 'iii'), 0, slice(14, 18)),
                  ((8, 'b', 'iii'), 0, slice(19, 23))],
       marks=[3, 3])

A.card(14, 'c', 'iii', topic='bio-1-3', concept='which-cell-is-turgid',
       source='pdf', from_run=((14, 'c', 'iii'), 0, slice(4, 6)), marks=[3],
       notes='A and B are the two plant cells drawn in the paper, one full and firm '
             'against its wall, the other with the membrane pulled away from it.')

A.card(11, 'b', 'vii', topic='bio-3-1', concept='writing-a-food-chain-from-a-web',
       source='pdf', from_run=((11, 'b', 'vii'), 0, slice(1, 8)), marks=[3],
       notes='The scheme requires the chain to start with a producer.')

A.card(14, 'c', 'v', topic='bio-1-3', concept='the-storage-organelle-of-a-plant-cell',
       source='pdf', from_run=((14, 'c', 'v'), 0, slice(0, 1)), marks=[3])

A.card(16, 'b', 'i', topic='bio-1-2', concept='drawing-a-typical-bacterial-cell',
       source='pdf',
       from_runs=[((16, 'a', 'i'), 3, slice(1, None)),
                  ((16, 'a', 'i'), 4, slice(1, None))],
       marks=[7, 2], notation='7 for the diagram, 2 a label',
       notes='The scheme numbers this answer under its own Question 16(a) while the '
             'paper prints 16(b). Cell wall, cell membrane and an indication of DNA are '
             'what the drawing must contain.')

A.card(17, 'c', 'i', topic='bio-2-4', concept='drawing-the-internal-structure-of-the-heart',
       source='pdf',
       from_runs=[((17, 'b', 'i'), 3, slice(1, 7)),
                  ((17, 'b', 'i'), 3, slice(8, None))],
       marks=[7, 2], notation='7 for the diagram, 2 a label',
       notes='The scheme numbers this answer under its own Question 17(b) while the '
             'paper prints 17(c).')

A.card(7, 'c', topic='bio-u1', concept='what-data-is',
       source='md', from_run=((6, 'c', None), 0, slice(0, 1)), marks=[4],
       checked='Question 7 is a matching table. The paper prints this part as a Column A '
               'description with no verb of its own, and the instruction to match it to a '
               'term in the list sits in the question stem the card already carries.',
       notes='The scheme prices Q7(a) to (e) on a scale of 4, 8, 12, 16, 20 for one to '
             'five correct — evenly, so each is worth four.')

# ── The parts the paper prints and the deck had no card for ───────────────
#
# Two things make this sitting awkward and both are parser artefacts, not
# disagreements between the documents. Paper and scheme number every question
# alike; it is the block segmentation that slides. In Section A both parsers
# hand question N's answers to key N-1 (the scheme's "Question 4: Name the
# parts A, B in skin" comes out under (3, 'a')), and in Section C they slide
# the sub-letter the same way ("Question 17 (d)" lands on (17, 'c')). Where a
# card below reaches through from_run(s) into a neighbouring key, that is why —
# the citation is always the paper's own numbering, which the scheme shares.
#
# The second is figures. Every diagram these parts hang off is in the manifest
# marked truncated and "do not publish": the skin section loses the letter A,
# the food web loses the word 'Shrew' in the gap between two crops, the
# breathing system loses B, the two plant cells lose both letters, and the
# plant stem has no crop at all. So no card here carries a figureKey, and the
# ones whose answer is keyed to a letter say in a note where the letter lives.

# ── Section A ─────────────────────────────────────────────────────────────
A.card(4, 'a', topic='bio-2-6', concept='skin-structure-parts',
       source='pdf',
       from_runs=[((3, 'a', None), 5, slice(0, None)),
                  ((3, 'a', None), 6, slice(0, None))],
       tariff='orderedSplit', ladder=6, notation='6(3) + 2',
       notes='A and B are two of the four structures marked on the paper\'s section '
             'through human skin; the other two, blood vessel and sweat gland, are '
             'word-labelled on the diagram itself. Q4 carries no per-part mark — its '
             'table pays 3, 6, 9, 12, 15, 18, 20 for one to seven correct responses, '
             'and this part is two of them.')

A.card(5, 'a', topic='bio-3-3', concept='matching-a-dna-profile',
       source='pdf', from_run=((4, 'a', None), 4, slice(0, None)),
       tariff='orderedSplit', ladder=3, notation='6(3) + 2',
       notes='The paper prints the crime-scene profile beside three suspect profiles '
             'labelled A, B and C. The deck holds no figure for that page, so the '
             'letter has to be taken from the scheme rather than read off the bands.')

# ── Section B ─────────────────────────────────────────────────────────────
A.card(8, 'b', 'ii', topic='bio-u1',
       concept='highest-percentage-frequency-from-a-table',
       source='md', marks=[3])

# The scheme names what the drawing must contain — container and liquid,
# anaerobic step, water bath, any two of them — which is answer content, not
# scaffolding. Only the second row is a bare criterion, and it is kept because
# the scheme prices it: Q9(b) is 8(3) over eight responses, of which this part
# is three (the diagram, then two labels), so it is worth 3 + 2(3) = 9.
A.card(9, 'b', 'i', topic='bio-u2',
       concept='drawing-the-alcohol-preparation-apparatus',
       source='pdf',
       from_runs=[((9, 'b', 'i'), 1, slice(0, None)),
                  ((9, 'b', 'i'), 2, slice(0, None)),
                  ((9, 'b', 'i'), 3, slice(0, 2)),
                  ((9, 'b', 'i'), 3, slice(10, 14))],
       use=[[0, 1, 2], 3], marks=[3, 6],
       notation='3 for the diagram, 2(3) for the labels',
       notes='The scheme prints the diagram mark as "3, 0" — all or nothing on any two '
             'of the three items — and does not name the two labels it pays 2(3) for.')

A.card(10, 'b', 'v', topic='bio-u2', concept='germination-investigation-results',
       source='md', stem=False,
       notes='A, B, C and D are the four test tubes in the paper\'s apparatus. The '
             'scheme\'s own earlier parts fix three of them: A is the dry cotton wool '
             'tube, C the boiled water with an oil layer, D the one held at 4 °C.')

# ── Section C ─────────────────────────────────────────────────────────────
WEB = ('The organisms are read off the paper\'s food-web diagram. The deck does not '
       'carry that figure — it survives only as two crops with the word "Shrew" lost '
       'in the gap — so the members come from the scheme. Q11(b) carries no per-part '
       'mark: its table pays 5, 10, 15, 17, 19, 21, 23, 25, 27 for one to nine correct '
       'responses.')

for roman, concept in (('iii', 'identifying-a-producer-in-a-food-web'),
                       ('iv', 'identifying-a-carnivore-in-a-food-web'),
                       ('vi', 'identifying-an-omnivore-in-a-food-web')):
    A.card(11, 'b', roman, topic='bio-3-1', concept=concept,
           source='md', stem=False,
           tariff='orderedSplit', ladder=5, notation='3(5) + 6(2)', notes=WEB)

A.card(13, 'b', 'i', topic='bio-2-6', concept='breathing-system-parts',
       source='pdf', use=[1, 2, 3], stem=False,
       tariff='orderedSplit', ladder=15, notation='3(5) + 6(2)',
       notes='The paper prints the part as "Name the parts A, B, C." beside a diagram '
             'of the human breathing system; the scheme prints it as "Name the parts '
             'A, B, C in the diagram of the breathing system below." Muscles, trachea '
             'and the small air-sacs are word-labelled on the same diagram, so the '
             'three letters are the ones left to name.')

A.card(14, 'b', 'iv', topic='bio-1-2', concept='carbohydrate-general-formula',
       source='md', stem=False,
       tariff='orderedSplit', ladder=5, notation='3(5) + 6(2)')

A.card(14, 'c', 'vi', topic='bio-1-3', concept='plasmolysis-in-a-plant-cell',
       source='md',
       from_runs=[((14, 'c', 'vi'), 0, slice(0, 11)),
                  ((14, 'c', 'vi'), 0, slice(11, 17))],
       tariff='orderedSplit', ladder=12, notation='2(6) + 6(2)',
       checked='The paper prints "(24)" — the mark for part (c) as a whole — on the line '
               'after this last sub-part, and the block takes it in. Page 5 of the '
               'Section C paper reads "(vi) Explain in detail what has happened to cell '
               'B." and the scheme answers that question.',
       notes='The scheme sets the answer on two lines and the table pays 6 and 12 for '
             'one and two correct responses, so both lines are wanted. Cell B is the '
             'right-hand cell of the pair drawn in the paper.')

STEM_SECTION = ('The letters are printed on the paper\'s section through a plant stem. '
                'The deck carries no crop of that diagram, so the letters come from the '
                'scheme. Q15(b) carries no per-part mark: its table pays 5, 10, 15, 17, '
                '19, 21, 23, 25, 27 for one to nine correct responses.')

A.card(15, 'b', 'i', topic='bio-2-6', concept='dermal-and-ground-tissue-names',
       source='pdf', use=[0, 1], stem=False,
       tariff='orderedSplit', ladder=10, notation='3(5) + 6(2)', notes=STEM_SECTION)

A.card(15, 'b', 'iii', topic='bio-2-6', concept='vascular-bundle-name',
       source='md', stem=False,
       tariff='orderedSplit', ladder=5, notation='3(5) + 6(2)', notes=STEM_SECTION)

A.card(15, 'b', 'vii', topic='bio-2-6', concept='dicot-stem-vascular-bundles',
       source='md', stem=False,
       tariff='orderedSplit', ladder=5, notation='3(5) + 6(2)',
       checked='The paper prints "(27)" — the mark for part (b) as a whole — after this '
               'last sub-part and the block takes it in. Page 6 of the Section C paper '
               'reads "(vii) State one reason why the diagram above represents a section '
               'through a dicotyledonous plant stem."',
       notes='The reason is a feature of the paper\'s section through a plant stem, and '
             'the deck carries no crop of that diagram, so it comes from the scheme. '
             'Q15(b) carries no per-part mark: its table pays 5 for the first correct '
             'response.')

A.card(17, 'd', 'iv', topic='bio-2-6', concept='order-of-the-alimentary-canal',
       source='md', from_run=((17, 'c', 'iv'), 0, slice(0, 12)), stem=False,
       tariff='orderedSplit', ladder=7, notation='2(7) + 8(2)',
       notes='The scheme\'s leading arrow runs from the mouth, which the question itself '
             'gives as the starting organ, and it marks the order all or nothing. Q17(d) '
             'carries no per-part mark: its table pays 7 for the first correct response.')

# ── Refused ───────────────────────────────────────────────────────────────
# 2022 OL Q16(c)(iii) is not carded. Two reasons, either enough on its own.
# The paper's text stops at "Draw a diagram of a long bone and label the" — the
# three parts it goes on to name are set as a list below the sentence and the
# block does not take them, so there is no complete question to ask. And the
# scheme adds nothing to card: its whole content is "Compact bone / Spongy bone
# / Bone marrow", which is the list the paper's own question supplies, priced
# "Diagram: one annotation / Labels: three annotations" — a count of examiner
# ticks, not an answer.
#
# 2022 OL Q17(b)(iv) is not carded. The scheme answers it "Plant: Any valid
# example / Animal: Any valid example" and names no example of either, so the
# card's back would say only that any correct answer scores.

A.emit()
