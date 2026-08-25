#!/usr/bin/env python3
"""Chemistry 2025 Ordinary Level — the parts the deck had not carded.

Ten asks were open. Four are carded here and six are refused, with the reason
each is refused written out at the foot of the file.

Two facts about this paper shape everything above that.

The markdown parser finds nothing at all in this scheme:
Scheme('chemistry', 2025, 'ol').parts is empty, because Scheme.QHEAD only
recognises the "Q3" form and the Chemistry examiners head their questions "3.".
So source='md' returns no candidates for any part and every answer here comes
from the PDF parser.

And the PDF parser's keys do not agree with the paper's numbering. The scheme
sets its pages in two columns and the parser interleaves them, so the answers
for the paper's Q3(b) are filed under its Q2(b) keys and the answers for the
paper's Q7(b)(iii) under its Q6(b)(iii). Each from_run below was found by
searching every key for the answer text and then reading the scheme page to
confirm which part it answers; the citation follows the PAPER, as law 3 requires.

Tariffs are read off the scheme and checked against the total the PAPER prints.
Q3(b) is priced (33) on page 4 of the paper and the scheme's four criteria for
it are 3 + 3 + (6 × 1) + 3 for (i), 6 for (ii), 4 + 2 for (iii) and 4 + 2 for
(iv) — which sums to 33 exactly. Q7(b) is priced (18) on page 8 and the scheme's
parts are 4 × 1, 2 and 9 + 3 — 18 exactly. Q4(h) is one of the Section B short
items, each worth 6, and the scheme splits it 4 + 2. No split here is inferred
from position; each is confirmed by a second document.

One field is knowingly wrong and is left wrong. lib.card() sets section from
`'A' if q <= 12 else 'B'`, which is Biology's split, not Chemistry's — this paper
prints "Section B" above Question 4. Every card lib has authored for Chemistry
carries the same value (chem-2024-ol-q5-b-i and chem-2024-ol-q8-a-i are both
"A"), so these four follow it rather than becoming the only four in the subject
that disagree. The fix belongs in lib.py, which this script may not touch.

One glyph note. The subset font maps "t" to U+01A9 and "fi" to the ligature
U+FB01, so the PDF text layer hands back "ploƩed" and "ﬁt" on the Q3(b)(i) card.
Both characters are in scripts/markbank/authoring/glyphmap.json (U+01A9 → "t",
U+FB01 → "fi") and build-deck's repairGlyphs walks every string on a card, so
they render as "plotted" and "fit" in the built deck. The verifier normalises
them too, which is why they still trace against the clean markdown.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2025, 'ol')


# ── Q3(b), the sodium thiosulfate rate experiment ────────────────────────────
# The paper prints the whole results table in Q3's stem — six concentrations and
# their six rates — so both graph parts are answerable from the card without a
# figure. The scheme's four criteria for the plot sit in one block under the
# parser's Q2(b)(i), so each row is a slice of that block and the bracketed
# instruction to the examiner is left off the card.
A.card(3, 'b', 'i', topic='chem-u2', concept='plotting-concentration-against-rate',
       source='pdf',
       from_runs=[((2, 'b', 'i'), 1, slice(0, 2)),
                  ((2, 'b', 'i'), 1, slice(3, 5)),
                  ((2, 'b', 'i'), 1, slice(6, 8)),
                  ((2, 'b', 'i'), 1, slice(11, 15))],
       marks=[3, 3, 6, 3], notation='3 + 3 + 6 × 1 + 3',
       notes='The six plotting marks are one for each point in the table. The scheme '
             'caps the whole part at twelve marks if graph paper is not used. Fifteen of '
             'the thirty-three marks the paper prints against Q3(b) are for this plot '
             'alone.')

# The scheme brackets the expected reading rather than requiring it, so the six
# marks are for taking a value off the candidate's own line, not for the number.
A.card(3, 'b', 'ii', topic='chem-u2', concept='estimating-a-rate-from-the-graph',
       source='pdf', from_run=((2, 'b', 'ii'), 2, slice(0, 7)), marks=[6],
       notes='0.05 M is not one of the six concentrations in the table, so the answer '
             'has to be interpolated from the line of best fit drawn in part (i). The '
             'scheme prints the expected value behind an approximation sign, which is '
             'why a reading close to it scores.')


# ── Q4(h), the chromatography sentence ───────────────────────────────────────
# The scheme runs the question cue and both answers together in one block —
# "Copy and complete the following sentence: speeds stationary (4 + 2)" — so
# each row is the single word that fills one of the paper's two blanks.
A.card(4, 'h', topic='chem-u2', concept='mobile-and-stationary-phase-in-chromatography',
       source='pdf',
       from_runs=[((4, 'h', None), 0, slice(6, 7)),
                  ((4, 'h', None), 0, slice(7, 8))],
       marks=[4, 2], notation='4 + 2',
       checked='Page 5 of the paper prints item (h) in full and this is all of it. The '
               'flag is raised only because the text ends on the closing quotation mark '
               'of the sentence to be completed rather than on a full stop; item (i) '
               'begins cleanly after it and nothing has been pulled in from a neighbour.',
       notes='The two rows fill the paper\'s two blanks in order: the first is what the '
             'components are carried at, the second is the phase the mobile phase is in '
             'contact with. The scheme prices them unevenly, 4 then 2.')


# ── Q7(b)(iii), testing that the solution is basic ───────────────────────────
# The parser files this answer under its own Q6(b)(iii), because the paper's
# Q6(b)(iii) is a drawing the scheme answers with nothing at all: the key holds
# that question's cue text and then rolls straight on into this one's answer.
#
# The scheme prints two matched routes, one above the other and each side of its
# own solidus — an indicator with its colour change, or a pH meter with its
# reading. `use` leads each row with the pH-meter route and carries the indicator
# route as its accepts, because "named indicator" bare is an instruction to the
# examiner rather than something a student writes, and no card should show that
# on its face. Both routes are the scheme's own words either way.
A.card(7, 'b', 'iii', topic='chem-3-4', concept='testing-a-solution-for-a-base',
       source='pdf',
       from_runs=[((6, 'b', 'iii'), 2, slice(0, 2)),
                  ((6, 'b', 'iii'), 1, slice(0, 2)),
                  ((6, 'b', 'iii'), 3, slice(0, 2)),
                  ((6, 'b', 'iii'), 2, slice(2, 6))],
       use=[[0, 1], [2, 3]], marks=[9, 3], notation='9 + 3',
       checked='Page 8 of the paper prints the part in full — "Describe how the solution '
               'of potassium hydroxide formed could be tested to show that it was basic." '
               'The flag is raised because the text ends on the bracketed "(18)", which '
               'is the mark for the whole of Q7(b): (i) is 4 × 1, (ii) is 2 and this part '
               'is 9 + 3, which sums to 18.',
       notes='The two rows are matched, not free choice: a named indicator has to be '
             'paired with its own colour change, and a pH meter with a pH reading. Three '
             'of the twelve marks are for the second row, which is the half candidates '
             'leave out — naming the test without saying what it shows.')


# ── Refused, with the reason each is refused ─────────────────────────────────
# Six of the ten open asks are not carded. None is a case where more effort
# inside this script would produce a card.
REFUSED = [
    ('2025 OL Q2(d)',
     'the scheme sets this calculation as two methods side by side in two columns, and '
     'the parser interleaves them into single lines. Two of the three steps are '
     'fractions whose numerator and denominator land in separate blocks: '
     '"(0.05)(25)" then "1000 = 0.00125 (moles per 25 cm3)", and "(0.0025)(1000)" then '
     '"18 = 0.13 - 0.14 M". Written onto a row either of those reads as a false '
     'equation, which no card may print. The one step that survives whole, '
     '"0.00125 x 2 = 0.0025", carries 2 of the part\'s 9 marks, so a card built from it '
     'alone would price a nine-mark calculation at two. There is no honest tariff here '
     'and law 2 forbids inventing one.'),

    ('2025 OL Q6(b)(iii)',
     '"Draw the molecular structure of C3H6 including all atoms and bonds." The scheme '
     'prints no marking point for it whatsoever — the parser key holds the question cue '
     'and then runs straight on into the answer for the paper\'s Q7(b)(iii). The whole '
     'answer is the drawn structure, and a structure is not something the text layer '
     'can carry.'),

    ('2025 OL Q8(a)(ii)',
     '"Draw the structure of a molecule of ethanol, showing all the atoms and bonds." '
     'The scheme\'s entire answer is the drawing and the bare tariff "(6)". There is no '
     'text to lift.'),

    ('2025 OL Q8(a)(iii)',
     '"Name polymer P, two repeating units of which are shown in the reaction scheme." '
     'The answer, polyethene, is clean and the scheme prices it at 6. The obstacle is P: '
     'the card would name a label that only the Q8 reaction scheme decodes, and that '
     'diagram is not available as a bound figure. The three crops extracted for page 9 — '
     'chemistry-2025-OL-paper-p09-i0, -i1 and -i2 — are all marked truncated, each a '
     'horizontal slice through the scheme rather than the whole of it. This needs a '
     'figure pass that re-crops page 9 and a decoded label key, neither of which can be '
     'added here.'),

    ('2025 OL Q8(a)(iv)',
     '"Identify a carbonyl compound from the reaction scheme." Same obstacle, one step '
     'weaker: no letter is named, but the question asks the candidate to read a diagram '
     'the card cannot show. The only stem available is the paper\'s block for Q8, which '
     'is the lead-in sentence followed by the reaction scheme\'s labels run together by '
     'the text layer — "heated C2H5OH ethanol solid S P ethene HCl Cl2 CH3CHO X Y '
     'ethanal". That is a picture taken apart, not a stem, and it should not be the '
     'first one a chemistry card carries. Card it after page 9 is re-cropped.'),

    ('2025 OL Q11(b)(vi)',
     '"Draw a dot and cross diagram to show the arrangement of the valence shell '
     'electrons in any one of these substances." The scheme answers it with nothing at '
     'all: under this part it prints only the question text and then the tariff line '
     '"(9 + 6 + 4 + 2 + 2 + 2)", which is the split across the whole of Q11(b). There is '
     'no marking point to lift and no mark priced against this roman on its own, so the '
     'card would fail both law 1 and law 2.'),
]

for ref, why in REFUSED:
    print(f'REFUSED {ref}: {why}', file=sys.stderr)

A.emit()
