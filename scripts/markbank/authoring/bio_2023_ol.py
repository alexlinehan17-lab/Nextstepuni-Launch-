#!/usr/bin/env python3
"""Biology 2023 Ordinary Level — the true/false statements, and the open asks.

Part one: Question 2, the true/false statements.

Two things had to be settled before these could be carded.

The answers are ticks, read by ticks.py from the glyph's position against the
True/False column headings.

The questions come off a page that sets Question 2 beside another question, so
the block segmentation welds the neighbour's text on: (c) arrives as "Data
always involves numbers. Three bases together are known as a ………". The statement
is the first sentence, and first_sentence=True trims to it — but only after
checking the trimmed text appears in the marking scheme, which prints these
statements too. All seven are confirmed that way.

Part two: the parts reconcile still reports open.

Two facts govern every card below.

The scheme's part keys do not line up with the paper's. This scheme numbers its
questions exactly as the paper does, but both parsers drift a part or a whole
question out of step wherever the SEC prints a mark-band table, a page footer or
a bare "Question 16 (a)" sub-head between two answers. Joining on the key would
hand real answers to the wrong questions — Q16(a)(iii)'s "Bladder" is filed
under the parser's (15, c, iii), one question early. Every card here therefore
names the parser key that actually holds its text with from_run/from_runs, and
its questionRef cites the PAPER. The disagreement is recorded on each card.

Ordinary Level Section A/B/C prices a whole question, not a part: "Q16 (a) (i) –
(vi) Number of correct responses 1 2 3 4 5 6 7 8 9 10 / Mark 7 14 16 18 20 22 24
26 28 30". No part carries a mark of its own, so every card is ladder=, with the
scheme table's award for the number of correct responses that card carries, and
the notation prints the question's own split. That is the shape the 2023 OL
cards already in the deck use.

One thing lib.py cannot express: section is derived as 'A' if q <= 12 else 'B',
which is right for a paper with two sections and wrong for Biology, whose
Ordinary Level paper runs Section A (Q1-Q7), Section B (Q8-Q10) and Section C
(Q11-Q17). The 2023 OL cards already in the deck carry the true letter, so the
returned card's section is corrected here rather than left to disagree with its
own neighbours. Nothing else about the card is touched.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2023, 'ol')
READ = ('The scheme answers this by ticking a True/False column; the tick was read '
        'from its position on page 8 of the 2023 Ordinary Level marking scheme. The '
        'paper prints this statement beside another question, so the question text '
        'is the statement alone, confirmed against the scheme. Q2 is marked 6(3) + 2 '
        'over seven statements.')

for letter, answer, topic, concept in (
        ('a', 'True',  'bio-u2', 'what-a-hypothesis-is'),
        ('b', 'False', 'bio-u2', 'sample-size-in-a-good-experiment'),
        ('c', 'False', 'bio-u2', 'data-need-not-be-numerical'),
        ('d', 'True',  'bio-u2', 'safety-as-a-principle-of-experimentation'),
        ('e', 'True',  'bio-u2', 'random-selection-in-experiments'),
        ('f', 'True',  'bio-u1', 'limitations-of-the-scientific-method'),
        ('g', 'False', 'bio-u1', 'a-theory-is-not-an-unsupported-hypothesis')):
    A.card(2, letter, topic=topic, concept=concept, tick=answer, marks=[3],
           notation='6(3) + 2', notes=READ, stem=False, first_sentence=True)


# Biology's Ordinary Level paper runs three sections; lib.py's q <= 12 rule
# knows only two. Correcting the field the moment the card is made keeps these
# cards agreeing with the 2023 OL cards already in the deck.
SECTIONS = {'A': range(1, 8), 'B': range(8, 11), 'C': range(11, 18)}


def card(q, *args, **kw):
    made = A.card(q, *args, **kw)
    made['section'] = next(s for s, qs in SECTIONS.items() if q in qs)
    return made


KEYED = ('The scheme prints its answer to this part under the parser key {}, '
         'not under the paper\'s own {}: this scheme drifts a part out of step '
         'wherever a mark-band table, a page footer or a bare sub-head sits '
         'between two answers. The citation follows the PAPER.')


# -- Section B ----------------------------------------------------------------

# Q8(b)(ii) is NOT carded. Its answer is priced and real ("Dandelion: 60% Grass:
# 100%"), but the ask is a calculation on the paper's presence/absence table,
# and that table cannot be put on a card: the tick is U+F050, a private-use
# glyph the text layer carries no font for, so paper.stem() returns the row as
# "Dandelion <U+F050> x <U+F050> x <U+F050>", which renders as tofu, and page 9
# of the paper has no crop in biology-figures.json. A card showing "Calculate
# the percentage frequency" with 60% and 100% and no data teaches two numbers,
# not a method. Cropping the table
# on page 9 would unlock it.
card(8, 'b', 'iii', topic='bio-u2', concept='bar-chart-of-percentage-frequency',
     source='pdf', stem=False,
     from_runs=[((7, 'b', 'iii'), 1, slice(0, 9)),
                ((7, 'b', 'iii'), 1, slice(9, 13)),
                ((7, 'b', 'iii'), 1, slice(13, 18))],
     ladder=20, notation='2(9) + 6(1)', tariff='orderedSplit',
     notes=('A drawing task the scheme answers with content, so it is carded: the '
            'marks are for what the axes are called and for the bars being there, '
            'not for the values plotted, which is why the card stands without the '
            "paper's data table. The scheme sets all three on one line; each row "
            'here is a slice of it. The stem is dropped: it is the presence/absence '
            'table, whose tick is a private-use glyph the text layer loses. '
            'Q8(b) is marked 2(9) + 6(1) across (i)-(iii) and no part carries a mark '
            "of its own; totalMarks is the scheme table's award for the three "
            'correct responses this card holds (20), not the 24-mark block. '
            + KEYED.format('(7, b, iii)', 'Q8(b)(iii)')))

card(9, 'b', 'i', topic='bio-u2', concept='osmosis-apparatus-diagram',
     source='pdf', from_run=((9, 'b', 'i'), 0, slice(0, 8)),
     ladder=9, notation='2(9) + 6(1)', tariff='orderedSplit',
     notes=('The scheme answers this in two lines and only the first is a marking '
            'point: "Diagram showing two solutions and membrane or tissue" names '
            'what the drawing must show, while "Any two correct labels" is a '
            'criterion for the examiner and carries no answer, so it is not shown '
            'and is not counted. Q9(b) is marked 2(9) + 6(1) across (i)-(iii); '
            "totalMarks is the scheme table's award for the one correct response "
            'this card holds (9), not the 24-mark block.'))


# -- Section C ----------------------------------------------------------------

card(15, 'b', 'v', topic='bio-2-6', concept='breathing-disorders',
     source='pdf', from_run=((3, None, 'v'), 1, slice(0, None)),
     ladder=5, notation='3(5) + 6(2)', tariff='orderedSplit', first_sentence=True,
     notes=('Half of this ask is carded and half is refused. The scheme answers the '
            'naming half with real content — "Name: Bronchitis or asthma or other '
            'correct" — and the causal half only with "Cause: Matching cause named '
            'or described", a rule for the examiner rather than an answer, so no '
            'second row exists to show. The paper welds the part mark "(27)" onto '
            'the end of this question; first_sentence trims it, and the trim is '
            "confirmed against the scheme, which prints the question too. Q15(b) is "
            "marked 3(5) + 6(2) across (i)-(v); totalMarks is the scheme table's "
            'award for the one correct response this card holds (5). '
            + KEYED.format('(3, None, v)', 'Q15(b)(v)')))

card(16, 'a', 'iii', topic='bio-2-6', concept='urinary-system-beyond-the-ureter',
     source='pdf', from_run=((15, 'c', 'iii'), 3, slice(0, None)),
     ladder=7, notation='2(7) + 8(2)', tariff='orderedSplit',
     notes=('Earlier waves held this part back because the scheme prints its cue as '
            'the bare "Name this other part." and the referent looked to be on the '
            'kidney diagram. It is not: the paper prints the whole ask in words — '
            '"The ureter connects the kidney to another part of the urinary system. '
            'Name this other part." — so the card stands on the paper text alone and '
            'needs no figure. Q16 is answered as any two of (a)-(d), each worth 30, '
            "and 16(a) is marked 2(7) + 8(2) across (i)-(vi); totalMarks is the "
            "scheme table's award for the one correct response this card holds (7). "
            + KEYED.format('(15, c, iii)', 'Q16(a)(iii)')))

card(16, 'a', 'iv', topic='bio-2-6', concept='fat-layer-around-the-kidney',
     source='pdf', from_run=((15, 'c', 'iv'), 3, slice(0, None)),
     ladder=7, notation='2(7) + 8(2)', tariff='orderedSplit',
     notes=('Same recovery as (a)(iii): the scheme\'s cue is the bare "Give one '
            'function of this layer of fat." but the paper prints the lead-in — '
            '"The kidneys are surrounded by a thick layer of fat." — so the ask is '
            'complete in words and no fat layer needs to be visible on the diagram. '
            "totalMarks is the scheme table's award for the one correct response "
            'this card holds (7); 30 is the whole Q16(a) block. '
            + KEYED.format('(15, c, iv)', 'Q16(a)(iv)')))

card(16, 'b', 'vi', topic='bio-2-4', concept='where-optic-nerve-impulses-travel',
     source='pdf', from_run=((16, 'a', 'vi'), 1, slice(0, None)),
     ladder=7, notation='2(7) + 8(2)', tariff='orderedSplit', stem=False,
     notes=('Held back before because the scheme\'s cue, "To which organ do these '
            'impulses travel?", leaves "these impulses" undefined. The paper defines '
            'them in the same sentence — "The optic nerve carries impulses." — so the '
            'card carries the ask whole. The stem is dropped: the paper block yields '
            'only the stray diagram letter "Z". Q16(b) is marked 2(7) + 8(2) across '
            "(i)-(vii); totalMarks is the scheme table's award for the one correct "
            'response this card holds (7). '
            + KEYED.format('(16, a, vi)', 'Q16(b)(vi)')))

card(17, 'b', 'ii', topic='bio-2-4', concept='glands-hormones-and-their-functions',
     source='pdf',
     from_runs=[((17, 'a', 'ii'), 2, slice(0, None)),
                ((17, 'a', 'ii'), 3, slice(0, 2)),
                ((17, 'a', 'ii'), 5, slice(0, None))],
     ladder=20, notation='2(7) + 8(2)', tariff='orderedSplit',
     notes=('A table-completion. The paper prints three rows and pre-fills four '
            'cells — the hormones Thyroxine and Adrenaline, the fight-or-flight '
            'function, and the gland Testes — leaving five blanks; the stem is the '
            "paper's own table, flattened by the text layer into one line, which is "
            'why it reads as a run of headings and given cells. The scheme prints '
            'the completed table and each row here is one of its rows. The second '
            'row is sliced to "Adrenal Adrenaline" because the third cell of that '
            'row was already filled in on the paper as the example, and because the '
            "scheme's own line breaks mid-phrase there. Q17(b) is marked 2(7) + 8(2) "
            "across (i)-(iv); totalMarks is the scheme table's award for the five "
            'correct responses this card holds (20) — five blanks, not three rows. '
            + KEYED.format('(17, a, ii)', 'Q17(b)(ii)')))

card(17, 'c', 'ii', topic='bio-3-2', concept='rhizopus-diagram-structures',
     source='pdf', from_run=((17, 'b', 'ii'), 1, slice(0, None)),
     ladder=7, notation='2(7) + 8(2)', tariff='orderedSplit',
     notes=('A drawing task, carded on what the scheme says rather than refused for '
            'being a drawing: "Diagram: Sporangium and sporangiophore" names the two '
            'structures the drawing must show. The scheme\'s second line, "Labels: '
            'Any two correct labels", is a criterion with no answer in it, so it is '
            'neither shown nor counted. Q17(c) is marked 2(7) + 8(2) across (i)-(vi); '
            "totalMarks is the scheme table's award for the one correct response this "
            'card holds (7). ' + KEYED.format('(17, b, ii)', 'Q17(c)(ii)')))


# -- refused, with the reason -------------------------------------------------
#
# Each of these is an ask the paper prints and this script leaves uncarded. The
# reason is recorded here because a documented refusal is worth more than a card
# that looks right and is not.
REFUSED = [
    ('Q1(a)', 'Give one source of carbohydrate in the diet. The scheme\'s whole '
              'answer is "Any correct source" — a criterion, no content.'),
    ('Q4(a)', 'Identify gases X and Y. X and Y are set in bold inside a word '
              'equation the paper draws as a graphic; the text layer returns it '
              'scrambled as "X Glucose + Y Water +", so the card cannot show which '
              'side of the arrow each gas is on. biology-figures.json catalogues '
              'the crop (biology-2023-OL-paper1-p05-i0) as complete and "Fit for a '
              'card", but the PNG was never extracted and the key is not bound, so '
              'there is no figure to hang it on. Extract and bind that crop and '
              'this part becomes a straightforward two-row figure card.'),
    ('Q5(b)', 'Using the letter X, indicate on the diagram above the source of '
              'light. The scheme\'s whole answer is "Correct location indicated" — '
              'a criterion. Contrast Q7(c), where the scheme does say where the '
              'answer goes ("Arrow from left to right").'),
    ('Q7(a)', 'Name the parts labelled A, B and C. The answers (Dendrite, Axon, '
              'Schwann cell or myelin sheath) are priced and real, but the letters '
              'live only on the paper\'s neuron drawing. That figure IS catalogued '
              '— biology-2023-OL-paper1-p08-i0 — and its manifest entry reads '
              '"TRUNCATED — do not put this crop on a card as it stands": the '
              'picture is two stacked XObjects and the crop caught only the top '
              'half. No PNG exists on disk either. Re-crop page 8 over roughly '
              'x 91-505 pt, y 92-281 pt, per the manifest, and all three of Q7(a), '
              '(b) and (c) open at once.'),
    ('Q7(b)', 'Give the function of the part labelled A. Answer "Receive impulses", '
              'but A is a bare letter on the same truncated neuron crop as Q7(a), '
              'and a stem naming A would hand over Q7(a)\'s answer.'),
    ('Q7(c)', 'Draw an arrow showing the direction the nerve impulse will travel. '
              'The scheme answers with content — "Arrow from left to right" — so '
              'this is not refused for being a drawing. It is refused because "left '
              'to right" is meaningless without the neuron, and the box the arrow '
              'goes in is precisely what the truncated crop cuts off.'),
    ('Q8(b)(ii)', 'Calculate the percentage frequency of dandelion and grass. '
                  'Answer "Dandelion: 60% Grass: 100%". The data is a '
                  'presence/absence table whose tick is U+F050, a private-use glyph '
                  'the text layer drops, and page 9 has no crop in the figure set, '
                  'so the card cannot carry the numbers the calculation runs on.'),
    ('Q11(a)(ii)', 'Describe one human activity that may cause pollution and suggest '
                   'one way it could be controlled. The scheme answers "Human '
                   'activity: Any valid activity" and "Prevent: Any valid and '
                   'matching preventative measure" — both criteria.'),
    ('Q11(c)(iv)', 'Give one biotic factor mentioned in the article. The scheme\'s '
                   'whole answer is "Any one correct".'),
    ('Q14(c)(iv)', 'Name two methods of contraception. The scheme\'s whole answer is '
                   '"Any two correct methods or examples".'),
    ('Q16(b)(vii)', 'Name a disorder of the eye or the ear and give a corrective '
                    'measure. The scheme answers "Eye: Named disorder or Ear: Named '
                    'disorder" and "Matching corrective measure" — criteria on both '
                    'halves, unlike Q15(b)(v) where the naming half is answered.'),
]
for ref, why in REFUSED:
    print(f'REFUSED 2023 OL {ref}: {why}', file=sys.stderr)

A.emit()
