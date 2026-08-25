#!/usr/bin/env python3
"""Chemistry 2024 Ordinary Level — parts the deck had not carded.

Every pairing here was read and confirmed rather than assumed. The wording
score cannot vouch for most of them — an electron configuration shares no words
with "Write the electron configuration for an atom of nitrogen" — so the aligner
places them on order alone, and order alone is not evidence. Read against the
scheme they are unambiguous: 1s2, 2s2, 2p3 for nitrogen and 2p5 for fluorine,
3.98 - 3.04 for the electronegativity difference between N and F, polar covalent
for the bonding that follows from it.

Marks are not guessed. The scheme prints one combined tariff per question —
"(9 + 6 + 4 + 3 + 2 + 2 + 2)" against Q5(b) and "(8 + 6 + 2 + 2)" against Q8(a) —
which splits over the parts in order. Q5(b)'s seven numbers sum to 28 and the
paper prints (28) at the end of that question, so the split is confirmed rather
than assumed.

Q4(f)(ii) is not here: it asks about hazard symbol B and that symbol is not
among the published figures, so the card would ask about something it cannot
show.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2024, 'ol')

# Not carded here: chem-2024-ol-q5-b-i is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q5-b-ii is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q5-b-iii is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q5-b-v is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q5-b-vi is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q8-a-i is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q8-a-ii is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q5-b-vii is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.

# Not carded here: chem-2024-ol-q7-a-ii is already a shipped hand-authored card.
# merge.py refuses the collision, and it is right to — a script must not
# quietly replace verified content.


# ── Second pass over the open parts ────────────────────────────────────────
# Everything below lifts through source='pdf', because the markdown parser finds
# nothing at all in this scheme: Scheme('chemistry', 2024, 'ol').parts is empty.
# The scheme heads its questions "1." and "8. (a)" and the markdown parser wants
# the "Q8" form, so every part comes back with no candidates and source='md'
# cannot card a single one of them.
#
# Two consequences of reading the PDF instead, both handled per card below.
#
# First, the tariff. Neither parser reads this scheme's mark column reliably, so
# `marks=` is passed on every card — and every split is checked against the
# total the PAPER prints, not inferred from the scheme alone. Q2(c) prints (15)
# and the scheme's two parts are 3 + 3 and 3 + 3 + 3; Q3(b) prints (25) and the
# scheme's are 4 + 4 + 1 then 8 + 4 + 2 + 2; Q7(a) prints (27) against
# 3 + 3, 15, 3, 3; Q8(a) prints (18) against 8 + 6 + 2 + 2; Q8(b) prints (21)
# against 6, 6, 3 + 3, 3; Q11(c) prints (25) against 6 + 3, 3 + 3 + 3, 4 × 1, 3.
# Each sums, so the per-part figures are confirmed by a second document rather
# than assumed from position.
#
# Second, the glyphs. The subset font maps "ti" to U+019F, so the PDF text layer
# hands back "addiƟon" and "staƟonary". Those characters are in
# scripts/markbank/authoring/glyphmap.json and build-deck's repairGlyphs walks
# every string on a card, so they render correctly in the built deck — the same
# route the Biology 2023 cards take. The verifier normalises them too, which is
# why they trace against the clean markdown.

A.card(2, 'c', 'i', topic='chem-4-1', concept='average-titre-from-accurate-results',
       source='pdf',
       from_runs=[((2, 'c', 'i'), 0, slice(0, 2)),
                  ((2, 'c', 'i'), 0, slice(3, 5))],
       marks=[3, 3], notation='3 + 3',
       notes='Only the two accurate titrations are averaged; the approximate one is '
             'discarded, which is why the answer is 20.55 and not the mean of all three.')

A.card(3, 'b', 'i', topic='chem-u2', concept='limewater-test-for-carbon-dioxide',
       source='pdf', use=[1, 2, 3], marks=[4, 4, 1], notation='4 + 4 + 1',
       notes='A drawing question the scheme prices by what the diagram must show, so the '
             'three things it wants are the card. The single mark is for the detail that '
             'is most often dropped: the mouth of the delivery tube has to be below the '
             'surface of the limewater.')

A.card(7, 'a', 'iii', topic='chem-u1', concept='reading-a-volume-off-the-rate-graph',
       source='pdf', use=[0], marks=[3],
       notes='The three marks are for reading the graph, not for the number: the scheme '
             'brackets 68 cm3 as the expected value rather than requiring it.')

A.card(7, 'a', 'iv', topic='chem-3-2', concept='average-rate-of-reaction-calculation',
       source='pdf', use=[0], marks=[3], first_sentence=True,
       notes='The 48 is the volume of O2 collected by 4 minutes, read from the table in '
             'the stem.')

A.card(8, 'a', 'iii', topic='chem-4-2', concept='naming-the-carboxylic-acid-in-the-series',
       source='pdf', use=[[1, 2]], marks=[2], notation='8 + 6 + 2 + 2')

A.card(8, 'a', 'iv', topic='chem-4-2', concept='classifying-the-ethene-to-ethanol-step',
       source='pdf', use=[1], marks=[2], notation='8 + 6 + 2 + 2', first_sentence=True)

A.card(8, 'b', 'i', topic='chem-4-2', concept='identifying-the-aldehyde-in-the-series',
       source='pdf', use=[[1, 2]], marks=[6])

# Question 11 is filed under the parser key Q86: the radon-222 nuclide on the
# previous page sets its atomic number 86 as a block of its own, QHEAD reads the
# bare number as a question head, and every part after it inherits it. The card
# lifts from that key and cites the PAPER's numbering, which is Q11(c)(ii).
A.card(11, 'c', 'ii', topic='chem-u2', concept='separating-indicators-by-chromatography',
       source='pdf',
       from_runs=[((86, 'c', 'ii'), 1, slice(0, None)),
                  ((86, 'c', 'ii'), 2, slice(0, None)),
                  ((86, 'c', 'ii'), 3, slice(0, None))],
       marks=[3, 3, 3], notation='3 + 3 + 3',
       checked='Page 12 of the paper prints the part in full as "Describe how '
               'chromatography could be used to separate a mixture of chemical '
               'indicators. (A labelled diagram may help your answer.)" The flag is '
               'raised only because the sentence ends on a closing bracket instead of a '
               'full stop; nothing is missing and no neighbour has been pulled in.',
       notes='The scheme numbers this answer under its own Q11(c)(ii) as well; only the '
             'PDF parser\'s key disagrees.')


# ── Refused, with the reason ───────────────────────────────────────────────
# Thirteen of the twenty-one open parts are not carded. They fall into three
# groups, and none of them is a case where more effort would produce a card.
#
# 1. The answer is a drawing.
#      Q5(b)(iv) — dot and cross diagram for NF3. The scheme's answer is the
#        diagram itself; the text layer returns the loose glyphs '● ●', '× ×'
#        and three stray 'F's.
#      Q6(a)(ii) — the molecular structures of the two C4H10 isomers. Same:
#        'H H H C H H H' and '[allow maximum marks of 3 + 3 for expanded
#        molecular formulae]'.
#      Q8(b)(ii) — the molecular structure of ethanal. 'O', 'H', 'C C', 'H H'.
#      Lifting any of these gives a row that is not an answer.
#
# 2. The answer is a fraction, or a working line the layout has cut in two.
#      Q2(c)(ii) — (20.55 × M)/2 = (25 × 0.05)/1. The denominators 2 and 1 are
#        the mole ratio from the balanced equation, which is the chemistry the
#        part is testing, and they sit on their own lines. Rows reading
#        '20.55 × M' and '25 × 0.05' would teach the wrong method.
#      Q10(a)(ii) — the empirical formula, worked as 70.59/12, 10.59/1 and
#        18.82/16. Each fraction breaks into 'C: 70.59' and '12 = 5.88', and
#        each PAIR carries one (3), so there is no split to give the two rows.
#      Q10(a)(iii) — the molecular formula. Here the right-aligned results were
#        read as the mark column, so the candidates end mid-equation:
#        '5 × 12 + 9 × 1 + 1 × 16 =' and '170 ÷ 85 ='. Only '85' and '2' would
#        complete them and they are in marks(), not in points().
#      Q10(b)(i) — the Kc expression, [N2O4] over [NO2]2. The scheme prices the
#        whole expression at (7); splitting it over two rows means inventing a
#        tariff for each half, which is exactly what law 2 forbids.
#      Q11(b)(iii) — the combined gas law. The blocks merge to
#        'P1V1 T1 = P2V2 T2', which is not the equation the scheme prints.
#      Q11(b)(iv) — the gas calculation. The substitution is the same two-line
#        fraction and it carries 5 of the 7 marks; only '267 (cm3)' survives.
#
# 3. The card would name a letter it cannot show.
#      Q4(f)(i) and Q4(f)(ii) — 'State the chemical hazard indicated by symbol
#        A' / 'symbol B'. The answers, oxidising and corrosive, are clean; the
#        symbols are not among the extracted figures. Only
#        chemistry-2024-ol-paper-p006-i0 and -p009-i0 exist for this paper, and
#        neither is page 7.
#      Q4(k) — 'Which of these hydrocarbons is an aromatic compound?' The whole
#        answer is 'X', a label on two structures the card cannot show.
#      Q9(c) — the seven water-treatment stages. The answers are a clean label
#        key (A: screening ... G: pH adjustment) and the marks are printed
#        (9 + 4 + 5 × 2 = 23, which is what the paper prints), so this one is
#        cardable the moment its stem is. The obstacle is that the only paper
#        text decoding A to G is the stem block, and that block ends
#        '... (23) Leaving Certificate, 2024 Chemistry – Ordinary Level 10'. No
#        chemistry card carries a page footer in its stem and this should not be
#        the first. Without the stem the seven rows name letters nothing on the
#        card explains.
#      All four want a figure or stem pass, not an authoring one.

A.emit()
