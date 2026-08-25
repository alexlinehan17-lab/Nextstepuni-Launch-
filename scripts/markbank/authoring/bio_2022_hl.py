#!/usr/bin/env python3
"""Biology 2022 Higher Level — Question 5's true/false statements, and the
paper asks the first wave left open.

Two separate jobs live in this file.

The first is Question 5. The scheme answers these by ticking a True or False
column, and the tick is a glyph the text layer drops. With nothing to attribute
to this question both parsers roll on and hand it the NEXT question's marking
points, so joining the two documents on their keys would put the wrong answers
under these statements. Each answer was read off page 9 of the scheme.

The second is the reconcile backlog. Everything below the Q5 loop is a part the
2022 Higher Level paper prints and the Mark Bank had no card for. They were left
open for two reasons, and only one of them held up:

  * The markdown scheme parser is useless on this paper. It looks for a 'Q<n>'
    line to head a question and the 2022 scheme heads every one 'Question <n>',
    so almost nothing is keyed; worse, the parser runs past the real scheme into
    the appended `<!-- markbank:table-cells -->` block, whose glyph-mangled text
    ('Deoxyribose or r ibose') then gets served as marking points. Every card
    here therefore reads the PDF parser, which keeps the answers clean but files
    them under its own renumbering — the scheme's Question 17 comes out as its
    Q10, Question 11 as its Q3, and so on. Each card names the run it lifts from
    and says where the disagreement is.
  * The drawing and sketch parts were skipped wholesale. Most of them are
    perfectly cardable: the scheme prints what has to be visible in the drawing
    and what each label is worth, and that is exactly the mark split a student
    cannot reconstruct. Those are carded. The ones whose whole marking point is
    'Correct arrow' or 'Any valid example' are not, and neither are the ones
    whose answer only means something against an image the deck cannot show.

The refusals are printed to stderr as the script runs, each with its reason.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2022, 'hl')
READ = ('The scheme answers this by ticking a True/False column and the tick is a '
        'glyph the text extraction drops, so it was read from page 9 of the 2022 '
        'Higher Level marking scheme. Q5 is marked 6(3) + 2 over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'False', 'bio-1-2', 'copper-is-a-trace-element'),
        ('b', 'True', 'bio-1-1', 'response-as-a-characteristic-of-life'),
        ('c', 'False', 'bio-1-3', 'animal-cell-in-a-concentrated-solution'),
        ('d', 'False', 'bio-2-6', 'which-cells-secrete-perforin'),
        ('e', 'True', 'bio-1-3', 'what-an-organ-is'),
        ('f', 'True', 'bio-2-4', 'ethene-ripens-fruit'),
        ('g', 'True', 'bio-3-2', 'fungi-are-heterotrophic'),
):
    A.card(5, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False)


def refuse(ref, why):
    """A paper ask this file deliberately leaves uncarded, and why."""
    print(f'REFUSED {ref}: {why}', file=sys.stderr)


# ---------------------------------------------------------------- Section A --

# The scheme prints one conclusion two ways round — faster with bile salts, or
# slower without them — so they are one row and its alternative, not two marks.
A.card(6, 'a', topic='bio-2-6', concept='bile-salts-and-rate-of-lipid-digestion',
       source='pdf',
       from_runs=[((5, 'a', None), 3, slice(0, None)),
                  ((5, 'a', None), 4, slice(0, None))],
       use=[[0, 1]], tariff='orderedSplit', ladder=3, notation='6(3) + 2',
       notes='Q6 is marked 6(3) + 2 across its six parts, so no part carries a printed '
             'mark of its own; each correct response is worth 3. The graph itself is not '
             'needed to reach the conclusion — the paper names both plotted lines and both '
             'axes in the stem the card carries, and the scheme takes the comparison '
             'stated either way round.')

refuse('Q7(b)', "the scheme's whole marking point is 'Correct arrow' — a criterion for the "
                'examiner, not an answer a student can learn.')
refuse('Q7(e)', "the scheme's whole marking point is 'Any valid harmful virus.' — "
                'content-free scaffolding, so there is nothing to put on the card.')

# ---------------------------------------------------------------- Section B --

# (b)(i) asks which of two micrographs is plant tissue and (b)(ii) asks why. The
# 'why' is real, image-independent content — how plant tissue is recognised down
# a microscope — so it is carded and the picture-reading part is not.
A.card(8, 'b', 'ii', topic='bio-u2', concept='recognising-plant-tissue-under-the-microscope',
       source='pdf', from_run=((2, 'b', 'i'), 3, slice(0, None)), marks=[3], stem=False,
       context='The paper prints part (b)(i) as "Which image, A or B, represents plant '
               'tissue?"; this part asks for the reason behind that choice.',
       notes='The paper\'s part (b) stem reads "A student observed the following images '
             'when examining stained cells using a light microscope. Image A was observed '
             'at x400 and image B at x100." The extractor files that sentence as a part of '
             'its own rather than as a stem, so it is quoted here instead of being lost. '
             'The named routes the scheme lists are all differences a candidate can state '
             'in words, which is why the answer stands without the images themselves.')

refuse('Q8(b)(i)', "the answer is '*B' — which of two printed micrographs shows plant "
                   'tissue. No figure for Q8(b) is bound into the deck, so the card could '
                   'not show what is being chosen between.')
refuse('Q8(b)(iii)', "'Identify structure Z' — Z exists only as a letter printed on the "
                     'micrograph, and no figure for Q8(b) is bound into the deck.')

A.card(8, 'b', 'v', topic='bio-u2', concept='calculating-actual-cell-width',
       source='pdf', from_run=((2, None, 'v'), 1, slice(0, None)), marks=[3], stem=False,
       context='The paper\'s part (b) stem reads "Image A was observed at x400 and image B '
               'at x100.", which is where the 400 in the scheme\'s answer comes from.',
       notes='The scheme prints the working as well as the result — 2/400 (cm) — and the '
             '400 is the magnification of image A, which the PAPER states and the scheme '
             'does not. That sentence is quoted on the card because the extractor files it '
             'as a part of its own rather than as the stem it is. Any correct unit scores.')

A.card(9, 'b', 'vi', topic='bio-u2', concept='sketching-photosynthesis-rate-graphs',
       source='pdf',
       from_runs=[((2, 'b', 'vi'), 0, slice(8, 15)),
                  ((2, None, None), 14, slice(12, 22))],
       marks=[3, 3],
       notes='The paper sets both sketches inside part (vi) — the solid line at 25 °C and '
             'the dashed line at 60 °C — and the extractor splits them, so the second '
             'requirement arrives on the stem rather than in the question text. One row '
             'per line, 3 marks each. Neither mark is for the drawing: they are for the '
             'shape of each line.')

A.card(10, 'b', 'ii', topic='bio-u2', concept='setting-up-the-iaa-investigation',
       source='pdf',
       from_runs=[((2, 'b', 'ii'), 3, slice(0, None)),
                  ((2, 'b', 'ii'), 4, slice(0, None)),
                  ((2, 'b', 'ii'), 5, slice(0, None)),
                  ((2, 'b', 'ii'), 6, slice(0, None)),
                  ((2, 'b', 'ii'), 8, slice(0, None))],
       use=[0, 1, 2, 3], spread=True, marks=[3, 3, 3, 3], notation='4(3)', stem=False,
       notes='The investigation is the one the scheme heads "Effect of IAA growth '
             'regulator on a plant tissue". Any four of the scheme\'s steps score, at 3 '
             'marks each, which is why each row carries the others as alternatives. Two of '
             'its seven listed steps are not shown: "named piece of apparatus" and "any '
             'other correct practical step" tell a candidate what the examiner wants to '
             'see rather than what to write.')

# ---------------------------------------------------------------- Section C --

# The drawing and the labels are priced separately: 3 for the drawing, then 1 a
# label for any three. Both halves are on the card because the split is the part
# a student cannot guess.
A.card(11, 'b', 'i', topic='bio-3-2', concept='drawing-a-bacterial-cell',
       source='pdf',
       from_runs=[((3, 'b', 'i'), 8, slice(6, 16)),
                  ((1, 'b', None), 5, slice(0, None)),
                  ((1, 'b', None), 6, slice(0, None)),
                  ((1, 'b', None), 7, slice(0, None))],
       marks=[3, 1, 1, 1], notation='Drawing 3 + Labels 3(1)', stem=False,
       notes='The scheme prices this part twice over: 3 marks for the drawing, awarded '
             'only if cell wall, cell membrane and an indication of nucleic acid are all '
             'visible, and then 1 mark for each of any three correct labels. The scheme\'s '
             'label list is cell wall / cell membrane / cytoplasm / chromosome / plasmid / '
             'flagella / capsule or slime layer; the three rows shown are the first three '
             'of that list the drawing row does not already name.')

refuse('Q11(c)(ii)', "the scheme's whole marking point is 'Matching explanation (accept "
                     'enzyme activity as explanation for temperature, pH, water '
                     "availability, etc)' — a criterion keyed to whichever factor the "
                     'candidate happened to name at (c)(i), not an answer.')

A.card(11, 'c', 'iv', topic='bio-3-2', concept='sketching-the-microbial-growth-curve',
       source='pdf',
       from_runs=[((7, 'c', 'iv'), 0, slice(12, 18)),
                  ((7, 'c', 'iv'), 0, slice(19, 30)),
                  ((7, 'c', 'iv'), 0, slice(31, 43))],
       marks=[3, 3, 3],
       notes='The scheme prices this part three ways at 3 marks each: the sketch itself, '
             'the axis labels, and the phase labels in the correct order. The five phase '
             'names the question asks to be placed on the curve are printed on the paper '
             'and arrive on the card as the stem, in the scrambled order the paper gives '
             'them.')

refuse('Q12(c)(iv)', "the scheme's whole marking point is 'Any valid example' — the "
                     'examiner is told to accept anything sensible, so there is no answer '
                     'to put on a card.')

# The paper prints this part as 13(a); the scheme prints it as 13(a)(i). The
# citation follows the paper, as it must.
A.card(13, 'a', topic='bio-1-4', concept='parts-of-a-nucleotide',
       source='pdf',
       from_runs=[((2, None, None), 17, slice(0, 3)),
                  ((2, None, None), 17, slice(4, 7)),
                  ((2, None, None), 17, slice(8, 16))],
       marks=[1, 1, 1], notation='3(1)',
       checked='The paper (Section C, p.4) prints "Nucleic acids are composed of subunits '
               'called nucleotides. Draw and label the structure of any one nucleotide." '
               'and then the part mark "(9)" on its own line, which is why the extracted '
               'text does not end on punctuation. The question is exactly as printed.',
       notes='The paper numbers this part 13(a); the marking scheme numbers the same '
             'answer 13(a)(i), and its annotation table calls it Q13 (a) (i) as well. The '
             'citation follows the paper. The part carries 9 marks: 6 for the drawing '
             'itself, scored 6, 3 or 0, and then 1 mark for each of the three labels shown '
             'here. The scheme prints nothing about the drawing beyond that band, so the '
             'three labels are the whole of what it states.')

A.card(13, 'c', 'ii', topic='bio-1-4', concept='drawing-parental-chromosome-diagrams',
       source='pdf',
       from_runs=[((9, 'c', 'ii'), 3, slice(0, None)),
                  ((9, 'c', 'ii'), 4, slice(0, None)),
                  ((9, 'c', 'ii'), 5, slice(0, 12)),
                  ((9, 'c', 'ii'), 5, slice(13, 20))],
       marks=[3, 3, 3, 3],
       notes='All 12 marks are in the two diagrams — four separate marking points at 3 '
             'marks each, and none of them for writing. The allele letters in the second '
             'row are the ones defined in the paper\'s own part (c) stem, which this card '
             'does not reproduce.')

refuse('Q13(c)(iii)', "the scheme's answers are '*FfDd' and '*White and disc-shaped fruit', "
                      'which mean nothing except against the F/f and D/d allele key and the '
                      "specific cross set in the paper's part (c) stem. The block parser "
                      'files that stem as a part of its own rather than attaching it, so '
                      'the card would carry a genotype with nothing to read it against.')

refuse('Q14(b)(iii)', "'Identify molecule Y' — Y is defined only by its position in the "
                      'photosynthesis flow diagram, alongside molecules X and Z. No figure '
                      'for Q14(b) is bound into the deck, so nothing on the card would say '
                      'which molecule Y is.')

A.card(14, 'b', 'v', topic='bio-2-2', concept='naming-the-light-independent-stage',
       source='pdf', from_run=((3, 'b', 'v'), 1, slice(0, 9)), marks=[3], stem=False,
       notes='The diagram is not needed to answer this: photosynthesis has two stages, and '
             'the paper has already fixed stage 1 in words at (b)(i) as the stage in which '
             'water is split using the energy in light.')

A.card(14, 'c', 'iii', topic='bio-2-3', concept='drawing-anaphase-of-mitosis',
       source='pdf',
       from_runs=[((3, 'c', 'iii'), 6, slice(1, 3)),
                  ((3, 'c', 'iii'), 6, slice(4, 8)),
                  ((2, 'c', None), 2, slice(0, None)),
                  ((2, 'c', None), 3, slice(0, None)),
                  ((2, 'c', None), 4, slice(0, None))],
       marks=[3, 3, 1, 1, 1], notation='Diagram 2(3) + Labels 3(1)',
       notes='The scheme prices the diagram twice at 3 marks — eight chromosomes, and '
             'those chromosomes being pulled apart — and then 1 mark for each of any three '
             'correct labels, from its list of chromosome / spindle / equator / poles / '
             'centromere.')

refuse('Q15(b)(ii)', 'the question names the lettered regions A, B and C on the printed '
                     'kidney diagram. A card naming lettered parts has to carry the '
                     'labelled figure and a decoded label key, and no figure for Q15(b) is '
                     'bound into the deck.')

A.card(15, 'c', 'ii', topic='bio-2-6', concept='drawing-a-root-transverse-section',
       source='pdf',
       from_runs=[((1, 'c', 'ii'), 0, slice(4, 11)),
                  ((1, 'c', None), 1, slice(1, 2)),
                  ((1, 'c', None), 1, slice(3, 4)),
                  ((1, 'c', None), 1, slice(5, 6))],
       marks=[3, 1, 1, 1], notation='Drawing 3 + Labels 3(1)',
       notes='The drawing scores 3 only if dermal tissue, vascular tissue and a root hair '
             'are all shown — note the root hair, which the question does not ask for. The '
             'three labels the question itself names are then worth 1 mark each, for 6 in '
             'total.')

A.card(16, 'a', 'i', topic='bio-2-4', concept='two-parts-of-the-nervous-system',
       source='pdf',
       from_runs=[((5, 'c', 'i'), 0, slice(0, 4)),
                  ((5, 'c', 'i'), 0, slice(5, 9))],
       marks=[3, 3],
       notes='The scheme sets both answers on one line with 3 marks against each.')

A.card(16, 'a', 'ii', topic='bio-2-4', concept='drawing-a-neuron',
       source='pdf',
       from_runs=[((2, 'a', 'ii'), 1, slice(4, 11)),
                  ((2, 'a', None), 5, slice(1, 2)),
                  ((2, 'a', None), 5, slice(3, 4)),
                  ((2, 'a', None), 5, slice(5, 7))],
       marks=[6, 1, 1, 1], notation='Drawing 6, 3, 0 + Labels 3(1)',
       notes='The drawing is scored 6, 3 or 0 — the scheme prints "any one missing = 3" '
             'beside it, so all three features earn 6 and two of the three earn 3. Note '
             'that cell body is one of them and the question does not ask for it. Each of '
             'the three labels the question does name is then worth 1 mark, for 9 in '
             'total.')

A.card(16, 'b', 'iv', topic='bio-2-4', concept='pupil-size-in-bright-and-dim-light',
       source='pdf',
       from_runs=[((3, 'b', 'iv'), 6, slice(0, 8)),
                  ((2, None, None), 22, slice(0, 8))],
       marks=[3, 3], stem=False,
       notes='Both marks are for the size of the pupil, not for the quality of the sketch.')

refuse('Q17(c)(vii)', "the scheme's whole marking point is 'Any named example' — content-"
                      'free scaffolding, so a card would have nothing on its back.')

A.card(17, 'd', 'v', topic='bio-2-6', concept='cause-of-heart-sounds',
       source='pdf', from_run=((2, None, 'v'), 6, slice(4, 6)), marks=[3], stem=False,
       notes='Two words are the whole of what the scheme prints, and they carry all 3 '
             'marks.')

A.emit()
