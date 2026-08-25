#!/usr/bin/env python3
"""Biology 2024 Higher Level — Question 5, the true/false statements.

The scheme answers these by ticking a True or False column, and the tick is a
glyph the text layer drops. With nothing to attribute to this question both
parsers roll on and hand it the NEXT question's marking points, so joining the
two documents on their keys would put the wrong answers under these statements.

Questions lifted from the paper as always; each answer read off page 10 of the
2024 Higher Level marking scheme. Marked 6(3) + 2 across seven statements.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2024, 'hl')
READ = ('The scheme answers this by ticking a True/False column and the tick is a '
        'glyph the text extraction drops, so it was read from page 10 of the 2024 '
        'Higher Level marking scheme. Q5 is marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'False', 'bio-1-3', 'which-cells-have-cell-walls'),
        ('b', 'False', 'bio-1-3', 'what-a-turgid-cell-is'),
        ('c', 'True', 'bio-2-2', 'fermentation-is-anaerobic'),
        ('d', 'False', 'bio-1-4', 'where-dna-is-found-in-the-cell'),
        ('e', 'False', 'bio-1-4', 'hydrogen-bonds-in-dna'),
        ('f', 'True', 'bio-1-4', 'which-bases-are-purines'),
        ('g', 'True', 'bio-1-4', 'what-chromosomes-are-made-of'),
):
    A.card(5, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False)

A.card(12, 'c', 'iv', topic='bio-3-1', concept='counting-trophic-levels',
       source='pdf', from_run=((3, None, 'iv'), 0, slice(0, None)), marks=[3],
       checked='The paper runs this part into the next in one block, so the text stops at '
               '"in part". The question asked is the one the scheme answers.',
       notes='The scheme numbers this answer under its own Question 3 while the paper '
             'prints Question 12.')

A.card(12, 'b', 'ii', topic='bio-3-1', concept='explaining-a-predator-prey-graph',
       source='pdf',
       from_runs=[((2, 'b', 'ii'), 1, slice(0, None)),
                  ((2, 'b', 'ii'), 2, slice(0, None)),
                  ((2, 'b', 'ii'), 4, slice(0, None))],
       marks=[2, 2, 2],
       notes='The scheme numbers this answer under its own Question 2 while the paper '
             'prints Question 12. It wants three separate observations: the shape of the '
             'line, the numbers involved, and the delay in time.')

A.card(12, 'b', 'iii', topic='bio-3-1', concept='what-happens-to-prey-if-the-predator-fails',
       source='pdf',
       from_runs=[((2, 'b', 'iii'), 1, slice(0, None)),
                  ((2, 'b', 'iii'), 3, slice(0, None))],
       marks=[3, 3])

# 2024 HL Q12(c)(iii) is not carded. Its whole marking point is "Any correct
# food chain from the food web", which the build refuses as a content-free row —
# rightly, because a card whose answer is "any correct answer" teaches nothing.

A.card(12, 'b', 'i', topic='bio-3-1', concept='drawing-the-predator-curve',
       source='pdf',
       from_runs=[((2, 'b', 'i'), 1, slice(0, None)),
                  ((2, 'b', 'i'), 2, slice(0, None))],
       marks=[2, 2],
       notes='The scheme numbers this answer under its own Question 2 while the paper '
             'prints Question 12. Both marks are for the shape of the curve rather than '
             'for the drawing itself.')

A.card(12, 'b', 'v', topic='bio-3-1', concept='why-human-numbers-do-not-follow-the-curve',
       source='pdf',
       from_runs=[((2, 'b', 'v'), 1, slice(0, None)),
                  ((2, 'b', 'v'), 2, slice(0, None))],
       marks=[4, 4], notation='2 at 4 marks each',
       notes='The scheme also allows a lack of predators, or any other correct reason.',
       checked='The paper prints the part mark "(27)" after the question and runs the '
               'graph labels on after it, so the text does not end on punctuation.')


# ── Second pass over the open parts ────────────────────────────────────────
# Every answer below comes from the PDF parser, because the markdown one finds
# nothing at all in a Biology scheme: it heads a question "Question 3" and the
# markdown parser only recognises the "Q3" form, so Scheme.parts is empty for
# this paper and `source='md'` returns no candidates for any part.
#
# The PDF parser's keys do not agree with the paper's numbering. Section A
# answers are scattered across its Q1–Q3 keys — one key per COLUMN of the
# scheme's two-column tables rather than one per question — and Section C
# answers sit under bare-roman keys (its Q2(ii), Q3(vii)) that belong to no real
# question at all. Each from_run below was found by searching every key for the
# answer text and then reading the scheme page to confirm the part it answers;
# the citation follows the paper, as it must.

# Q3: the scheme prices (a) separately at 3(1) — a mark for each lettered part —
# and runs (b)–(f) together as one 5(3) + 2 block, which is why those rows carry
# no mark of their own. What A, B and C are is the scheme's own answer to (a),
# so the later parts can name them without the diagram.
ALIMENTARY = ('The paper prints parts (a) to (f) beside one diagram of the human '
              'alimentary canal. Parts (b) to (f) share the tariff "5(3) + 2", so no '
              'part of that block has a mark of its own; totalMarks is the 3-mark '
              'rate the first five correct answers are paid.')

A.card(3, 'a', topic='bio-2-6', concept='naming-the-parts-of-the-alimentary-canal',
       source='pdf',
       from_runs=[((3, 'a', None), 4, slice(0, 2)),
                  ((3, 'a', None), 5, slice(0, 2)),
                  ((3, 'a', None), 6, slice(0, 2))],
       marks=[1, 1, 1], notation='3(1)', labels='auto',
       notes='The scheme sets these three answers in one table cell, so each row is '
             'the label and its answer cut from that cell: the mark column ("1") and '
             'the next row\'s cue word ("Organ", "Gland") follow each one in the same '
             'cell and are left off. Part (a) is priced 3(1) on its own, apart from '
             'the 5(3) + 2 that covers (b) to (f).')

A.card(3, 'b', topic='bio-2-6', concept='function-of-the-oesophagus',
       source='pdf', from_run=((3, 'b', None), 11, slice(0, None)),
       ladder=3, tariff='orderedSplit', notation='5(3) + 2',
       labels={'A': {'meaning': 'Oesophagus', 'askedInThisQuestion': False}},
       notes=ALIMENTARY + ' What tube A is comes from the scheme\'s own answer to '
             'Q3(a) on the same diagram.')

A.card(3, 'c', topic='bio-2-6', concept='function-of-the-liver',
       source='pdf', from_run=((3, 'c', None), 14, slice(0, None)),
       ladder=3, tariff='orderedSplit', notation='5(3) + 2',
       labels={'B': {'meaning': 'Liver', 'askedInThisQuestion': False}},
       notes=ALIMENTARY + ' What organ B is comes from the scheme\'s own answer to '
             'Q3(a) on the same diagram.')

# The paper's block for (d) picks up the diagram label "Small intestine" and
# nothing else, so this card carries no stem rather than a stem that names the
# wrong organ.
A.card(3, 'd', topic='bio-2-6', concept='function-of-the-pancreas-in-digestion',
       source='pdf', from_run=((3, 'd', None), 6, slice(0, None)),
       ladder=3, tariff='orderedSplit', notation='5(3) + 2', stem=False,
       labels={'C': {'meaning': 'Pancreas', 'askedInThisQuestion': False}},
       notes=ALIMENTARY + ' The paper sets the words "Small intestine" as a diagram '
             'label directly above this part, and the block segmentation reads them '
             'as its stem, so the card is left without one. What gland C is comes '
             'from the scheme\'s own answer to Q3(a).')

# 2024 HL Q4(a) is not carded. The paper asks the candidate to label any one
# structure on the xylem/phloem drawing and draw an arrow to it; the scheme's
# whole answer is "Correct label and correct arrow indicating structure", which
# names no structure and is an instruction to the examiner, not an answer.

A.card(7, 'b', topic='bio-3-3', concept='naming-the-stages-of-genetic-engineering',
       source='pdf',
       from_runs=[((3, 'b', None), 16, slice(0, None)),
                  ((3, 'b', None), 17, slice(0, None)),
                  ((3, 'b', None), 18, slice(0, None))],
       ladder=9, tariff='orderedSplit', notation='6(3) + 2',
       notes='Question 7 is marked 6(3) + 2 across its seven markable items — (a), '
             'the three stages here, and the three parts of (c) — so no item has a '
             'mark of its own; totalMarks is three items at the 3-mark rate. The '
             'stages are lettered on the paper\'s flow diagram, and the scheme names '
             'each one in full, so the rows carry the naming without it.')

# 2024 HL Q7(c)(i), (ii) and (iii) are not carded. The scheme answers all three
# with "Any correct application given" — for plant, for animal, for
# micro-organism — which states the criterion and no application.

# 2024 HL Q9(b)(i) is not carded: the scheme's whole answer is "Correctly named
# enzyme or cell", a criterion.
#
# 2024 HL Q9(b)(iii) is not carded either, for the same reason four times over.
# Its entire marking point reads "Description: Matching substrate / Named product
# or name of test or how tested / Valid control or comparison / Result described
# Any three", every clause of which tells the examiner what to look for and the
# candidate nothing they could learn.

# Q10(b)(i) is marked 5(3). The fifth point is the general criterion
# "Description: Relevant piece of apparatus named or suitable temperature or
# suitable safety precaution", which the deck does not put on a card, so the four
# rows here are the four steps the scheme actually describes and totalMarks is
# their 12. Each row's trailing solidus — the scheme's own separator, left behind
# because the PDF breaks the list across lines — is cut with the slice.
A.card(10, 'b', 'i', topic='bio-u2',
       concept='setting-up-the-seed-digestion-investigation',
       source='pdf',
       from_runs=[((3, 'b', 'i'), 5, slice(0, -1)),
                  ((3, 'b', 'i'), 6, slice(0, -1)),
                  ((3, 'b', 'i'), 7, slice(0, -1)),
                  ((3, 'b', 'i'), 8, slice(0, -1))],
       marks=[3, 3, 3, 3], stem=False,
       notes='The paper prints this part on the last question page of the answerbook, '
             'and the block above it is the answerbook\'s own instructions, so the '
             'card carries no stem. The investigation is the action of digestive '
             'enzymes in germinating seeds on starch agar or skimmed milk plates. '
             'Marked 5(3): the fifth point is the scheme\'s general criterion about '
             'naming apparatus, a suitable temperature or a safety precaution, which '
             'is not an answer and is left off.')

FLOWER = {'A': 'Anther', 'B': 'Filament', 'C': 'Stigma'}

A.card(11, 'b', 'i', topic='bio-2-5',
       concept='naming-the-parts-of-a-wind-pollinated-flower',
       source='pdf',
       from_runs=[((3, 'b', 'i'), 11, slice(1, None)),
                  ((3, 'b', 'i'), 12, slice(1, None)),
                  ((3, 'b', 'i'), 13, slice(1, None))],
       marks=[1, 1, 1], notation='3(1)', labels=FLOWER,
       notes='The scheme marks each of these three answers with its essential-answer '
             'asterisk; the asterisk is an instruction to the examiner and comes off, '
             'as it does on every card in the deck. Priced 3(1) — one mark each — '
             'separately from the 8(3) that covers the rest of part (b).')

A.card(11, 'b', 'ii', topic='bio-2-5', concept='adaptations-for-wind-pollination',
       source='pdf', from_run=((3, 'b', 'ii'), 14, slice(0, None)), marks=[3])

A.card(11, 'b', 'iii', topic='bio-2-5', concept='where-pollen-is-formed',
       source='pdf', from_run=((3, 'b', 'iii'), 8, slice(0, None)), marks=[3],
       labels={'A': 'Anther',
               'B': {'meaning': 'Filament', 'askedInThisQuestion': False},
               'C': {'meaning': 'Stigma', 'askedInThisQuestion': False}},
       notes='The scheme accepts either the letter or the part\'s name. What the '
             'three letters stand for is the scheme\'s own answer to Q11(b)(i) on the '
             'same diagram.')

# 2024 HL Q12(c)(i) is not carded. It asks for a producer, a secondary consumer
# and a top consumer from the printed marine food web. The scheme answers the
# second and third ("Salmon or herring or octopus", "Peregrine falcon or orca
# whale"), but its answer to the first is set as the bare table cell
# "Phytoplankton or seaweed 3", which both parsers read as a mark column and
# neither returns as a marking point — so it cannot be lifted. A card that
# answered two of the three named examples would leave a third of a 6(3) part
# unanswered, which is worse than no card.

# 2024 HL Q12(c)(iii) is not carded. Its whole marking point is "Any correct
# food chain from the food web", which the build refuses as a content-free row —
# rightly, because a card whose answer is "any correct answer" teaches nothing.

A.card(12, 'c', 'vii', topic='bio-3-1', concept='naming-the-ecological-pyramid',
       source='pdf', from_run=((3, None, 'vii'), 1, slice(0, -1)), marks=[2],
       checked='The paper prints part (c)\'s tariff "(24)" immediately after this, the '
               'last of its seven sub-parts, so the block does not end on punctuation. '
               'Page 3 of the Section C paper shows the question is complete as it '
               'stands.',
       notes='The scheme prints its own cue in an abbreviated form ("Name the type of '
             'diagram an ecologist may draw…"); the question text here is the paper\'s '
             'full wording. Parts (v), (vi) and (vii) share the tariff 3(2), which is '
             'why this one is worth 2 and not 3. The scheme sets the mark in the same '
             'cell as the answer, so the trailing "2" is cut with the slice.')

A.card(13, 'c', 'iii', topic='bio-2-2',
       concept='fate-of-the-energised-electrons-in-pathway-1',
       source='pdf',
       from_runs=[((3, 'c', 'iii'), 5, slice(0, None)),
                  ((3, 'c', 'iii'), 6, slice(0, None)),
                  ((3, 'c', 'iii'), 7, slice(0, None)),
                  ((3, 'c', 'iii'), 8, slice(0, -2))],
       use=[0, 1], marks=[3, 3], spread=True, notation='Any two 2(3)', stem=False,
       notes='Marked "Any two 2(3)": the scheme lists four points and pays 3 for each '
             'of the first two, so both rows carry the other two as accepted '
             'alternatives. The paper sets this part under a passage about the light '
             'stage of photosynthesis splitting into pathway 1 and pathway 2; the '
             'block segmentation hands this part the sub-questions of (c)(v) as a '
             'stem instead, so the card is left without one.')

A.card(14, 'b', 'i', topic='bio-1-3', concept='drawing-and-labelling-a-bacterial-cell',
       source='pdf',
       from_runs=[((3, 'b', 'i'), 17, slice(0, None)),
                  ((3, 'b', 'i'), 18, slice(0, None)),
                  ((3, 'b', 'i'), 19, slice(0, None)),
                  ((3, 'b', 'i'), 20, slice(0, None)),
                  ((3, 'b', 'i'), 21, slice(0, None)),
                  ((3, 'b', 'i'), 22, slice(0, None)),
                  ((3, 'b', 'i'), 23, slice(0, None)),
                  ((3, 'b', 'i'), 24, slice(0, None)),
                  ((3, 'b', 'i'), 25, slice(0, None))],
       use=[0, [1, 2, 3, 4, 5, 6, 7, 8]], marks=[3, 3],
       notation='diagram 1(3) + any three labels 3(1)',
       notes='A drawing question the scheme answers in words: 3 for a drawing that '
             'shows the three named structures, and 3(1) — a mark each — for any '
             'three correct labels, which is why the label row is worth 3 and carries '
             'the rest of the scheme\'s list as alternatives.')

# Q15(b): the paper opens (ii) with the cross itself and puts the instruction on
# the next line, which the block segmentation files with part (b)'s stem. Both
# halves are the paper's own words and the card carries both, the instruction in
# the stem and the cross as the question.
A.card(15, 'b', 'ii', topic='bio-1-4', concept='genotypes-of-the-parent-plants',
       source='pdf',
       from_runs=[((2, 'b', 'ii'), 6, slice(0, None)),
                  ((2, 'b', 'ii'), 7, slice(0, 1))],
       marks=[3, 3],
       notes='The paper prints part (ii) over two lines — the cross on the first and '
             '"Using suitable letters, give the genotypes of both plants in the above '
             'cross." on the second — and the second line is read as part of the '
             'question stem, which is where this card carries it. The scheme adds '
             '"Allow alternative letters for Rr e.g. RW" beside the second genotype; '
             'that is an instruction to the examiner and is not on the card.')

A.card(15, 'b', 'iii', topic='bio-1-4',
       concept='offspring-genotypes-and-phenotypes-of-the-cross',
       source='pdf',
       from_runs=[((2, 'b', 'iii'), 5, slice(1, None)),
                  ((2, 'b', 'iii'), 6, slice(1, None)),
                  ((2, 'b', 'iii'), 7, slice(1, None)),
                  ((2, 'b', 'iii'), 8, slice(1, None))],
       marks=[3, 3, 3, 3],
       notes='The rows run in the scheme\'s own order: a genotype, then the phenotype '
             'that goes with it, twice. The scheme labels each row "Genotype:" or '
             '"Phenotype:" and marks each answer with its essential-answer asterisk; '
             'the asterisk comes off and the label is cut, because it belongs to the '
             'scheme\'s table and not to the answer.')

A.card(15, 'b', 'iv', topic='bio-1-4', concept='percentage-of-pink-offspring',
       source='pdf', from_run=((2, 'b', 'iv'), 2, slice(-2, -1)), marks=[3],
       checked='The paper prints part (b)\'s tariff "(27)" immediately after this, the '
               'last of its four sub-parts, so the block does not end on punctuation. '
               'Page 6 of the Section C paper shows the question is complete as it '
               'stands.',
       notes='The scheme sets the cue, the answer and the mark in one cell — "What '
             'percentage of the offspring of the cross have pink flowers? *50% 3" — '
             'so the row is the answer cut from the middle of it.')

A.card(15, 'c', 'i', topic='bio-1-5', concept='who-proposed-natural-selection',
       source='pdf',
       from_runs=[((2, 'c', 'i'), 2, slice(0, None)),
                  ((2, 'c', 'i'), 3, slice(0, None))],
       marks=[3, 3],
       notes='The paper sets this under "Two famous biologists independently '
             'developed the theory of evolution by natural selection."; that sentence '
             'is in a block of its own that the segmentation does not attach to the '
             'part, so the card carries no stem.')

# 2024 HL Q16(b)(iii) is not carded. It asks, for any named hormone, for a
# symptom of deficiency, a symptom of excess and a corrective measure; the
# scheme's three answers are "Deficiency symptom to match hormone named", "Excess
# symptom to match hormone named" and "Corrective measure to match either
# symptom". Every one is the matching rule and none is a symptom or a measure.

# Q17(a): the paper sets both parts under a graph of enzyme activity against pH
# for two digestive enzymes, A and B. The graph's axis text is what the block
# segmentation offers as a stem, so these cards carry none.
A.card(17, 'a', 'i', topic='bio-2-1', concept='optimal-ph-of-a-stomach-enzyme',
       source='pdf', from_run=((3, None, 'i'), 10, slice(0, None)), marks=[4],
       stem=False,
       notes='The paper numbers two asks under (i) — the optimal pH of enzyme A and '
             'of enzyme B — and prints each on its own line; the block segmentation '
             'keeps only the first, which is the one this card asks and answers. '
             'Marked 2(4), four marks for each of the two.')

A.card(17, 'a', 'ii', topic='bio-2-1', concept='which-enzyme-works-in-the-stomach',
       source='pdf',
       from_runs=[((2, None, 'ii'), 20, slice(1, None)),
                  ((2, None, 'ii'), 21, slice(1, None))],
       marks=[4, 3], stem=False,
       notes='The scheme prices the two halves separately — 1(4) for naming the '
             'enzyme and 1(3) for the justification — so the rows are worth 4 and 3.')

A.card(17, 'b', 'ii', topic='bio-3-2',
       concept='drawing-rhizopus-in-asexual-reproduction',
       source='pdf',
       from_runs=[((2, None, 'ii'), 23, slice(0, None)),
                  ((2, None, 'ii'), 24, slice(0, None)),
                  ((2, None, 'ii'), 25, slice(0, None)),
                  ((2, None, 'ii'), 26, slice(0, None)),
                  ((2, None, 'ii'), 27, slice(0, None)),
                  ((2, None, 'ii'), 28, slice(0, None)),
                  ((2, None, 'ii'), 29, slice(0, None)),
                  ((2, None, 'ii'), 30, slice(0, None)),
                  ((2, None, 'ii'), 31, slice(0, None)),
                  ((2, None, 'ii'), 32, slice(0, None)),
                  ((2, None, 'ii'), 35, slice(0, None))],
       use=[0, [1, 2, 3, 4, 5, 6, 7, 8, 9], 10], marks=[3, 3, 3], stem=False,
       notation='diagram 2(3) + any three labels 3(1) + 1(3) for the indication',
       notes='A drawing question the scheme answers in words. The part is worth 12 in '
             'all; the card carries 9 of them. The scheme\'s second diagram mark — 3 '
             'for showing a stolon or a rhizoid — is set as a bare cell that both '
             'parsers read as a mark column, so it cannot be lifted as a row, but '
             'both structures are in the label list this card does carry. The paper '
             'block above this part is the tail of (b)(iii), so the card has no stem.')

A.card(17, 'c', 'ii', topic='bio-2-6', concept='drawing-and-labelling-the-nephron',
       source='pdf',
       from_runs=[((2, None, 'ii'), 39, slice(0, None)),
                  ((2, None, 'ii'), 40, slice(0, None)),
                  ((2, None, 'ii'), 41, slice(0, None)),
                  ((2, None, 'ii'), 42, slice(0, None)),
                  ((2, None, 'ii'), 43, slice(0, None)),
                  ((2, None, 'ii'), 44, slice(0, None)),
                  ((2, None, 'ii'), 45, slice(0, None)),
                  ((2, None, 'ii'), 46, slice(0, None)),
                  ((2, None, 'ii'), 47, slice(0, None)),
                  ((2, None, 'ii'), 48, slice(0, None)),
                  ((2, None, 'ii'), 49, slice(0, None)),
                  ((2, None, 'ii'), 50, slice(0, None))],
       use=[0, 1, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]], marks=[3, 3, 6], stem=False,
       notation='diagram 2(3) + any six labels 6(1)',
       notes='A drawing question the scheme answers in words: 3 for the tubule itself, '
             '3 for the blood supply and 6(1) — a mark each — for any six correct '
             'labels, which is why the label row is worth 6 and carries the rest of '
             'the scheme\'s list as alternatives. The paper block above this part is '
             'the two sub-asks of (c)(iv), so the card has no stem.')

A.card(17, 'd', 'v', topic='bio-2-3', concept='sketching-a-cell-at-metaphase',
       source='pdf',
       from_runs=[((2, None, 'v'), 15, slice(0, None)),
                  ((2, None, 'v'), 16, slice(0, None))],
       marks=[3, 3], stem=False,
       notes='The stage named at (d)(iv) is metaphase. The scheme abbreviates its own '
             'cue to "Sketch a simple cell with a diploid number of 4 that is at the '
             'stage you named above."; the question text here is the paper\'s full '
             'wording. The paper block above this part runs into the copyright notice '
             'on the back page, so the card carries no stem.')

A.card(17, 'd', 'vii', topic='bio-2-3', concept='loss-of-control-of-mitosis',
       source='pdf', from_run=((2, None, 'vii'), 18, slice(0, None)), marks=[3],
       stem=False,
       notes='The scheme abbreviates its cue to "What name is given to the group of '
             'disorders….?"; the question text here is the paper\'s full wording. The '
             'paper block above this part runs into the copyright notice on the back '
             'page, so the card carries no stem.')

A.emit()
