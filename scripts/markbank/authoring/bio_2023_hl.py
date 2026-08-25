#!/usr/bin/env python3
"""Biology 2023 Higher Level — the asks reconcile still reports open.

Three facts govern every card below.

**Most of what was open is a drawing.** An earlier wave wrote drawings off in
bulk: "Q15(b)(i) skipped: labelled diagram of the male reproductive system
(drawing)", "Q16(d)(iv) skipped: diagram of Rhizopus", "Q17(d)(vi) skipped: draw
and label an L.S. of vascular tissue". That is the wrong cut. Split them by what
the SCHEME says instead. "Diagram: Penis, testis, urethra and sperm duct" names
the four structures the drawing must show and is the thing candidates actually
lose the marks on; "Correct arrow to a slightly movable joint" names nothing the
question had not already said. The first is carded, the second is refused, and
each refusal below says which of the two it is.

**The scheme's part keys do not line up with the paper's.** Neither parser sees
this scheme's "Question 12" heads — both anchor on "Q12" or a bare number — so
every part is filed under whichever marker was read last, and the drift is
large: Q17(c)(ii)'s alveolus sketch is filed under the markdown parser's
(4, c, ii) and Q11(b)(iv)'s pyramid under the PDF parser's (3, b, iv). Joining
the two documents on the key would therefore hand real answers to the wrong
questions. Every card here names the parser key that actually holds its text
with from_run/from_runs, and cites the PAPER. The disagreement is on each card.

**Section A is priced on a ladder.** "Q2 (a) - (f) Number of correct responses
1 2 3 4 5 6 7 / Mark 5 10 12 14 16 18 20" is one scale for the whole question,
so no part of Q2, Q4 or Q5 carries a mark of its own. Those cards are ladder=,
with the scheme table's award for one correct response, and the notation prints
the question's own split — the shape the 2023 HL Section A cards already use.

One thing lib.py cannot express: section is derived as 'A' if q <= 12 else 'B',
which is right for a paper with two sections and wrong for Biology, whose Higher
Level paper runs Section A (Q1-Q7), Section B (Q8-Q10) and Section C (Q11-Q17).
The 2023 HL cards already in the deck carry the true letter, so the returned
card's section is corrected here rather than left to disagree with its own
neighbours. Nothing else about the card is touched.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2023, 'hl')


# Biology's Higher Level paper runs three sections; lib.py's q <= 12 rule knows
# only two. Correcting the field the moment the card is made keeps these cards
# agreeing with the 2023 HL cards already in the deck.
SECTIONS = {'A': range(1, 8), 'B': range(8, 11), 'C': range(11, 18)}


def card(q, *args, **kw):
    made = A.card(q, *args, **kw)
    made['section'] = next(s for s, qs in SECTIONS.items() if q in qs)
    return made


KEYED = ('Neither parser reads this scheme\'s "Question {}" head, so the answer '
         'to this part is filed under the parser key {} rather than under the '
         "paper's own {}. The card lifts from that key and cites the PAPER.")

LADDER_A = ('Question {q} is marked {n} across ({first})-({last}), one ladder for '
            'the whole question, so no part of it carries a mark of its own. '
            "totalMarks is the scheme table's award for one correct response (5).")


# -- Section A ----------------------------------------------------------------

card(2, 'c', topic='bio-u2', concept='naming-a-variable-in-an-investigation',
     source='pdf', from_run=((6, 'c', None), 0, slice(0, None)),
     ladder=5, notation='2(5) + 5(2)', tariff='orderedSplit',
     notes=('Held back before as "the investigation is printed on the paper and not '
            'reproduced in the scheme". It does not need to be: the paper prints the '
            "horticulturist's germination trial as Question 2's own stem, which the "
            'card carries, and the scheme answers the part with content — the two '
            'quantities the trial actually varied and measured. '
            + LADDER_A.format(q=2, n='2(5) + 5(2)', first='a', last='f') + ' '
            + KEYED.format(2, '(6, c, None)', 'Q2(c)')))

card(4, 'b', topic='bio-1-4', concept='what-makes-up-one-dna-nucleotide',
     source='pdf', from_run=((7, 'b', None), 6, slice(0, None)),
     ladder=5, notation='2(5) + 5(2)', tariff='orderedSplit',
     notes=('A draw-on-the-printed-diagram part, carded on what the scheme says '
            'rather than refused for being a drawing: the marking point does not '
            'stop at "rectangle correctly indicating one DNA nucleotide" but goes on '
            'to name the three things that rectangle has to enclose, which is the '
            'recallable content and the reason candidates draw the box in the wrong '
            'place. The card therefore stands without the printed diagram. '
            + LADDER_A.format(q=4, n='2(5) + 5(2)', first='a', last='g') + ' '
            + KEYED.format(4, '(7, b, None)', 'Q4(b)')))

card(5, 'f', 'i', topic='bio-3-2', concept='first-phases-of-a-bacterial-growth-curve',
     from_run=((4, 'f', 'i'), 0, slice(0, None)), stem=False,
     ladder=5, notation='2(5) + 5(2)', tariff='orderedSplit',
     notes=('Held back before as "a drawing-on-a-graph criterion". The scheme does '
            'not give a criterion here — it names the two phases the drawn curve has '
            'to show, which is the answer and is learnable without the printed axes. '
            'The stem is dropped: the paper block yields only the graph furniture '
            '"Population Z Time". '
            + LADDER_A.format(q=5, n='2(5) + 5(2)', first='a', last='f') + ' '
            + KEYED.format(5, '(4, f, i)', 'Q5(f)(i)')))


# -- Section B ----------------------------------------------------------------

card(9, 'b', 'i', topic='bio-u2', concept='apparatus-for-preparing-alcohol-with-yeast',
     source='pdf',
     from_runs=[((2, 'b', 'i'), 1, slice(1, 4)),
                ((2, 'b', 'i'), 1, slice(5, 16)),
                ((2, 'b', None), 0, slice(1, None)),
                ((2, 'b', None), 1, slice(0, None)),
                ((2, 'b', None), 2, slice(0, None)),
                ((2, 'b', None), 3, slice(0, None)),
                ((2, 'b', None), 4, slice(0, None)),
                ((2, 'b', None), 5, slice(0, None))],
     use=[0, 1, [2, 3, 4, 5, 6, 7]], marks=[3, 3, 3],
     notation='Diagram 2(3) + Labels 3(1)',
     notes=('bio-2023-hl-q9-b records this part as "skipped: it asks for a labelled '
            'diagram of the apparatus (drawing)". The scheme answers it with content '
            'on both halves, so it is carded. The drawing is priced 2(3) — a 3-mark '
            'point for what is in the vessel and another for the anaerobic condition '
            'being shown — and the labels 3(1), any three of the six the scheme lists, '
            'which is the third row and its alternatives. The question does not name '
            'the labels, so unlike Q15(b)(i) and Q16(d)(iv) the label list here is '
            'answer content rather than a copy of the ask. totalMarks 9 is the two '
            'tariffs added. ' + KEYED.format(9, '(2, b, i) and (2, b, None)',
                                             'Q9(b)(i)')))


# -- Section C ----------------------------------------------------------------

card(11, 'b', 'iv', topic='bio-3-1', concept='sketching-a-pyramid-of-numbers',
     source='pdf',
     from_runs=[((3, 'b', 'iv'), 3, slice(0, 7)),
                ((3, 'b', 'iv'), 3, slice(8, 12))],
     marks=[3, 3], notation='9(3)',
     notes=('bio-2023-hl-q11-b-i-ii records this as "skipped: sketch a pyramid of '
            'numbers (drawing)". The scheme prices the sketch on two things a '
            'candidate can be told in advance — which organism goes on the bottom '
            'step, and that the pyramid is only partially upright — so it is carded. '
            'The scheme sets both on one line and each row here is a slice of it. '
            "The stem is kept because the passage is what part (b)(iii)'s food chain "
            'was read off, and it is the paper\'s own; the sentence about "the '
            'importance of this type of ecological relationship" at the end of it is '
            'the tail of part (b)(vi), which the block segmentation swept in. '
            'Q11(b) is marked 9(3) across (i)-(vi) and the scheme prints 3 against '
            'each of these two responses. '
            + KEYED.format(11, '(3, b, iv)', 'Q11(b)(iv)')))

card(12, 'a', 'ii', topic='bio-1-1', concept='anabolic-or-catabolic-reaction',
     from_runs=[((4, 'a', 'ii'), 5, slice(0, None)),
                ((4, 'a', 'ii'), 6, slice(3, None))],
     marks=[3, 3], notation='3(3)', stem=False,
     notes=('Two responses, priced 3 each: the scheme starts the naming half with an '
            'asterisk, its mark for an answer that must be exact, and answers the '
            '"explain" half with the property that makes it catabolic. The second '
            "row is sliced past the scheme's own cue, \"Explain your answer.\", "
            'which it welds onto the front of the marking point. The stem is '
            'dropped: the paper block yields only the reaction graphic flattened to '
            '"A B + C Energy +". '
            + KEYED.format(12, '(4, a, ii)', 'Q12(a)(ii)')))

card(12, 'b', 'v', topic='bio-2-2', concept='the-atp-word-equation',
     source='pdf', from_run=((3, 'b', 'v'), 8, slice(0, None)),
     marks=[6], notation='2(3)', stem=False,
     notes=('The paper prints the equation with two blanks — "ADP + ______ + Energy '
            '-> ATP + ______" — and the scheme prints it filled in. The arrow is set '
            'in the Symbol font and reaches the text layer as U+F067; glyphmap.json '
            'maps that character, so build-deck\'s repairGlyphs renders it as an '
            'arrow. Contrast Q11(b)(iii), refused below, whose arrow is U+F08E and '
            'is not in the map. The scheme prices this 2(3), one mark per blank '
            'filled correctly, which is why the single row carries 6. The stem is '
            "dropped: the paper block interleaves the diagram label \"Nucleus\" and "
            'the part mark with the equation. '
            + KEYED.format(12, '(3, b, v)', 'Q12(b)(v)')))

card(13, 'c', 'ii', topic='bio-1-4',
     concept='chromosome-diagrams-for-a-sex-linked-cross',
     source='pdf',
     from_runs=[((9, 'c', 'ii'), 14, slice(12, 18)),
                ((9, 'c', 'ii'), 14, slice(19, 26)),
                ((9, 'c', 'ii'), 14, slice(27, 32))],
     marks=[3, 3, 3], notation='8(3)', stem=False,
     notes=('bio-2023-hl-q13-c-i records this as "skipped: draw two labelled '
            'chromosome diagrams (drawing)". The scheme prices the drawing on three '
            'separate things and the first of them is content — that the two '
            'diagrams are XX and XY — so it is carded. The scheme sets all three on '
            "one line, after its own cue, and each row here is a slice of it. Unlike "
            'part (iii), nothing in these three marking points is written in the '
            'superscript allele notation the text layer flattens. The stem is '
            "dropped: the paper block yields only the pedigree chart's key and its "
            'person numbers. ' + KEYED.format(13, '(9, c, ii)', 'Q13(c)(ii)')))

card(15, 'b', 'i', topic='bio-2-5', concept='diagram-of-the-male-reproductive-system',
     source='pdf', from_run=((3, 'b', 'i'), 19, slice(1, 7)),
     marks=[6], notation='3+3', stem=False,
     checked=('Opened page 6 of the 2023 Higher Level Section C paper. The ask ends '
              'on a colon and the six parts to label are set as their own block on '
              'the next line, so the continuation joins them and the text stops on '
              'the list rather than on punctuation — which is what raised the flag. '
              'The wording is the paper\'s. The same page carries the SEC misprint '
              'paper.py already overrides: this part is headed with a bold "16." '
              'where "(b)" belongs, and the citation follows the paper\'s real '
              'numbering, which the scheme confirms as 15(b)(i).'),
     notes=('bio-2023-hl-q15-b-ii records this as "skipped: labelled diagram of the '
            'male reproductive system (drawing)". The scheme names the four '
            'structures the drawing must contain, and that list is not the same as '
            'the six the question asks you to label — urethra is on it and is not in '
            'the question — so the marking point carries content the ask does not. '
            'Priced 3+3, all six marks for a drawing showing all four, three if one '
            'is missing. The separate 6(1) for labels is not shown: those labels are '
            "the question's own list. The stem is dropped: the paper block yields "
            'the following sub-part, about the sperm cell, not this one. '
            + KEYED.format(15, '(3, b, i)', 'Q15(b)(i)')))

card(16, 'a', 'iii', topic='bio-1-3',
     concept='sugar-concentration-with-no-change-in-mass',
     source='pdf', from_run=((8, 'c', 'iii'), 5, slice(15, 17)),
     marks=[3], notation='10(3)', stem=False,
     notes=('A read-off-the-graph part whose answer the scheme prints as a number '
            'with its units, and marks with the asterisk it uses for an answer that '
            'has to be exact. The value is the concentration at which water enters '
            'and leaves the tissue at the same rate, which the deck already teaches '
            'from the other side in bio-2023-hl-q16-a-i-ii-iv, so the card stands '
            'without the printed graph. The stem is dropped: the paper block yields '
            "the graph's axis furniture and the tail of a neighbouring sub-part. "
            'Q16 is answered as any two of (a)-(d), each worth 30, and 16(a) is '
            'marked 10(3) across (i)-(vii). '
            + KEYED.format(16, '(8, c, iii)', 'Q16(a)(iii)')))

card(16, 'd', 'iv', topic='bio-3-2', concept='diagram-of-rhizopus',
     source='pdf', from_run=((3, 'd', 'iv'), 4, slice(3, None)),
     marks=[6], notation='3+3',
     notes=('bio-2023-hl-q16-d-v-vi records this as "skipped: diagram of Rhizopus '
            'plus its label table (drawing)". The scheme names four structures the '
            'diagram must show and the question asks for three: sporangiophore is in '
            'the marking point and not in the ask, so a candidate who draws only '
            'what was listed loses marks. That is the content the card carries. '
            'Priced 3+3, all six for all four structures and three if one is '
            "missing. The separate 3(1) for labels is not shown: it repeats the "
            "question's own list. " + KEYED.format(16, '(3, d, iv)', 'Q16(d)(iv)')))

card(17, 'c', 'ii', topic='bio-2-6', concept='sketching-an-alveolus-and-gas-movement',
     from_runs=[((4, 'c', 'ii'), 39, slice(1, None)),
                ((4, 'c', 'ii'), 40, slice(16, None)),
                ((4, 'c', 'ii'), 41, slice(0, None))],
     marks=[3, 3, 3], notation='10(3)', stem=False,
     notes=('Three separate responses at 3 each: what the sketch has to contain, and '
            'then the direction of each gas, which is the half candidates reverse. '
            "The second row is sliced past the scheme's own cue, which it welds onto "
            'the front of the marking point. The stem is dropped: the paper block '
            'yields the tails of the neighbouring sub-parts (c)(i) and (c)(iii). '
            'Q17 is answered as any two of (a)-(d), each worth 30, and 17(c) is '
            'marked 10(3) across (i)-(iii). '
            + KEYED.format(17, '(4, c, ii)', 'Q17(c)(ii)')))

card(17, 'd', 'vi', topic='bio-2-6', concept='longitudinal-section-of-vascular-tissue',
     source='pdf',
     from_runs=[((6, 'd', 'vi'), 1, slice(1, 11)),
                ((6, 'd', 'vi'), 1, slice(12, 20))],
     use=[[0, 1]], marks=[3], notation='3', stem=False,
     notes=('bio-2023-hl-q17-d-iv-v records this as "skipped: draw and label an L.S. '
            'of vascular tissue (drawing), including its label table". The scheme '
            'names what each of the two sections has to show, which is content, so '
            'it is carded — as one row with two alternatives, because the question '
            'lets a candidate choose either tissue and the scheme prices the drawing '
            'once, at 3. The further 3(1) the scheme awards for any three labels on '
            'that drawing is not shown: its two lists are xylem labels and phloem '
            'labels and only the list matching the chosen drawing can score, which '
            'one alternatives row cannot express. The stem is dropped: the paper '
            "block yields the page's copyright notice. "
            + KEYED.format(17, '(6, d, vi)', 'Q17(d)(vi)')))


# -- refused, with the reason -------------------------------------------------
#
# Each of these is an ask the paper prints and this script leaves uncarded. The
# reason is recorded here because a documented refusal is worth more than a card
# that looks right and is not.
REFUSED = [
    ('Q2(a)', 'Draw a vertical line on the graph that indicates a pH most suitable '
              'for the germination of grass seeds. The scheme\'s whole answer is '
              '"Correct vertical line drawn through peak" — a criterion that says '
              'the line goes where the curve is highest, which is what "most '
              'suitable" already means. Nothing is left to recall, and the peak it '
              'points at is on a graph the card cannot show: the crop of it, '
              'biology-2023-HL-paper1-p04-i0, is flagged truncated in '
              'biology-figures.json and is not usable as it stands.'),
    ('Q3(e)', 'Draw an arrow from the letter X to show the location of a slightly '
              'movable joint. The scheme\'s whole answer is "Correct arrow to a '
              'slightly movable joint" — the question\'s own words back again, with '
              'no joint named. Contrast Q11(b)(iv), carded above, where the scheme '
              'does say what the drawing must show.'),
    ('Q4(a)', 'Complete the diagram of the DNA molecule by drawing on it and '
              'labelling the parts you draw. The scheme\'s whole answer is "A and C '
              'correctly drawn and labelled": two bare letters off the printed '
              'diagram, with nothing saying what A and C are. A card naming letters '
              'needs a labelled figure behind it, and page 6 of the Sections A and B '
              'paper — where this DNA drawing is printed — has no crop at all in '
              'biology-figures.json, so there is nothing to decode them from.'),
    ('Q4(d)', 'What type of bonding is represented by the letter X on the diagram? '
              'The answer, "Hydrogen or H (bonding)", is real and priced — but X is '
              'a letter on the paper\'s DNA drawing and the drawing has two kinds of '
              'bond in it, so without the figure the ask is not answerable. Crop '
              'page 6 of the Sections A and B paper, which biology-figures.json does '
              'not cover at all, and this becomes a one-row figure card — the same '
              'crop would open Q4(a) as well.'),
    ('Q5(b)', 'Draw an arrow from X to the location of the bacterial cell wall. The '
              'scheme\'s whole answer is "Arrow drawn correctly to cell wall" — the '
              'ask restated. bio-2023-hl-q5-a-fig already carries this micrograph '
              'and its label key records X as the point candidates draw from, which '
              'is all this part has to teach.'),
    ('Q5(e)', 'Name any one harmful bacterium. The scheme\'s whole answer is "Any '
              'named harmful bacterium" — a criterion, no content.'),
    ('Q5(f)(ii)', 'Name the stage indicated by the letter Z. The answer, "Decline or '
                  'death", is priced and real, but Z is a letter on the printed '
                  'growth curve and the curve has four stages; a card that shows the '
                  'ask without the graph is asking the student to guess which one. '
                  'The only crop biology-figures.json holds from that page is the '
                  'bacterial micrograph, biology-2023-HL-paper1-p07-i0, not the '
                  'curve. Part (f)(i) is carded because its answer names its phases '
                  'rather than pointing at them.'),
    ('Q11(b)(iii)', 'Write down a food chain based on the passage. The scheme gives '
                    'the chain itself — three named organisms joined by arrows — so '
                    'this is not a criterion and not refused as one. It is refused '
                    'on the arrows: they reach the text layer as U+F08E, and unlike '
                    'the U+F067 arrow in Q12(b)(v) that character has no entry in '
                    'scripts/markbank/authoring/glyphmap.json, so build-deck\'s '
                    'repairGlyphs would leave it in place and the card would print a '
                    'placeholder box between each pair of names. Dropping the arrows '
                    'is not an option either — the order of the three names is the '
                    'entire answer. Add U+F08E to glyphmap.json and this part is a '
                    'one-row card.'),
    ('Q12(b)(i)', 'Copy the diagram of the cell and indicate the specific locations '
                  'of stage 1 and stage 2. The scheme answers this with the drawing '
                  "itself; all its text layer holds is the picture's own three "
                  'labels, "Stage 1", "Stage 2" and "Nucleus", which name the things '
                  'being located and not where they are. Naming the two locations '
                  'would mean writing the answer, which is exactly what is not '
                  'allowed.'),
    ('Q13(c)(iii)', 'Show how it is possible for the parents to have a male child '
                    'who does not suffer from haemophilia. The scheme answers with '
                    'gametes and a genotype written in superscript allele notation, '
                    'and both text layers flatten the superscripts away: the three '
                    'marking points arrive as "Gametes from Parent 1: XN", "Gametes '
                    'from Parent 2: Y-" and "Genotype of son: XYN- genotype '
                    'indicated as a non-sufferer". A student who wrote those down as '
                    'printed would have the wrong genotypes, and restoring the '
                    'superscripts means writing the answer rather than lifting it.'),
    ('Q16(b)(iv)', 'State one application of genetic engineering for animals, '
                   'microorganisms and plants. All three marking points are "Any '
                   'correct application given" — criteria on every half.'),
    ('Q17(a)(iii)', 'Copy the outline of the human body and draw in the pituitary, '
                    'thyroid and adrenal glands in their correct locations. The '
                    "scheme answers with the marked-up outline; its text layer holds "
                    'only the three gland names back again, which the question '
                    'already lists. Where each gland goes is stated by the picture '
                    'alone, so there is nothing to lift.'),
]
for ref, why in REFUSED:
    print(f'REFUSED 2023 HL {ref}: {why}', file=sys.stderr)

A.emit()
