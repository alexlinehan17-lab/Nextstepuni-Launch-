#!/usr/bin/env python3
"""Chemistry 2022 Ordinary Level — parts the deck had not carded.

Every card here is source='pdf'. The markdown parser finds nothing at all in
this scheme: it heads each question "QUESTION 1" and Scheme only recognises the
"Q1" form, so Scheme.parts is empty for the whole sitting and source='md'
returns no candidates for any part of it.

The PDF parser's keys do not agree with the paper's numbering either. It finds
only two question heads in the scheme — a Q1 group and a Q4 group — and then
walks (a), (b), (c)... through each, so one key holds the same-positioned part
of several different questions at once. (4, 'c', 'v'), for instance, carries
Q5(c)(iv)'s working, Q10(c)(i)–(v)'s calculations and Q11(c)(v)'s label answer,
in that order. A parser key is therefore only an address, never evidence: each
from_run below was found by searching every key for the answer text and then
reading the scheme page against the paper page. The citation follows the paper,
as law 3 requires.

Tariffs are the scheme's own, and each is checked against the total the paper
prints for the parent:

  Q3(b)  the paper prints (24) once, over (i)–(iii), and the paper's own block
         segmentation runs the three romans together as a single ask — which is
         why the ledger lists only (b)(i) as open. The scheme pays the plot
         5 x 3 = 15, then (ii) 6 and (iii) 3. 15 + 6 + 3 = 24, so the split is
         confirmed rather than assumed, and the card carries all seven rows.
  Q4(k)  the scheme prints "(6)" against the answer and Q4's rubric prints
         "Six marks to be allocated to each item".
  Q7(b)  "(4 x 6) + (3 x 2)" = 30, which is the (30) the paper prints. That is
         a sliding scale over seven lettered blanks, not a mark per blank, so
         the card is ladder= — rows with no mark of their own and the shape
         written into the notation.
  Q8(b)  "FOUR POINTS: [6 + 6 + 2 + 1]" = 15, the (15) the paper prints over
         (i)-(iii). Two of the four points fall in (i).
  Q8(c)  "FIVE POINTS: [6 + 6 + 3 + 2 + 1]" = 18, the (18) the paper prints
         over (i)-(iii). Two of the five points fall in (i).
  Q9(a)  "ANY THREE: [6 + 4 + 2]" = 12, the (12) the paper prints.
  Q10(c) the paper prints (25) over the five romans and the scheme pays
         6 + 6 + 6 + 3 + 4 = 25, so (iv)'s 3 and (v)'s 4 are confirmed.

Twenty of the twenty-nine open asks are refused, printed on stderr by the
REFUSED list at the foot of this file. Four reasons account for all of them:
art the deck cannot show, a pronoun whose antecedent no API here can put on the
card, an answer that is a drawing, and an answer whose exponents the text layer
lost.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2022, 'ol')


# ── Question 3(b): the hydrogen peroxide graph (paper page 4) ────────────────
#
# The graph is the candidate's own — the paper prints the volume/time table in
# the part (b) stem and asks for it to be plotted — so this needs no figure.
# The scheme's plotting marks sit in one run at (1, 'b', 'i'); (ii)'s and
# (iii)'s banded answers are at (1, 'b', 'ii') and (1, 'b', 'iii').
A.card(3, 'b', 'i', topic='chem-u2', concept='plotting-the-h2o2-decomposition-graph',
       source='pdf',
       from_runs=[((1, 'b', 'i'), 0, slice(1, 7)),
                  ((1, 'b', 'i'), 0, slice(8, 15)),
                  ((1, 'b', 'i'), 0, slice(16, 19)),
                  ((1, 'b', 'i'), 0, slice(20, 30)),
                  ((1, 'b', 'i'), 0, slice(31, 37))],
       marks=[3, 3, 3, 3, 3], notation='(5 × 3) + 6 + 3 (the plot)',
       checked='Page 4 of the paper was opened. The paper sets (b)(i), (ii) and (iii) as '
               'one block and prints the part mark "(24)" at the end of it, so the lifted '
               'text ends on a bracketed number rather than punctuation. The block is '
               'exactly what the page prints.',
       notes='The paper runs (b)(i)–(iii) together in one block and prices them with a '
             'single (24), so the card carries all three: the first five rows are the '
             'plotting marks for (i), then (ii)\'s estimate and (iii)\'s rate. The '
             'citation follows the paper\'s numbering for the head of that block. The '
             'scheme adds three conditions: points joined by straight lines are '
             'unacceptable, minus 3 if the graph is not on graph paper, and reversed '
             'axes are acceptable.')

# Not carded: the two values read off the finished graph, which the scheme
# prices in the same lot as the five plotting criteria ((5 x 3) + 6 + 3). They
# belong to the paper's own parts (b)(ii) and (b)(iii), but the page sets
# (b)(i)-(iii) as ONE block, so all three parts share a single lifted question
# text — and a second card carrying that same text is refused by the
# duplicate-question guard, rightly. Separating them needs the page-4
# segmentation fixed in paper.py, not a second card here.


# ── Question 4(k): the molecular formula of phenol (paper page 6) ────────────
#
# The scheme runs items (i), (j) and (k) into one block, so the answer is cut
# out of it by token. The paper draws benzene and phenol beside the question,
# but it also names phenol and gives benzene's formula in the question text, so
# the ask stands without the drawing.
A.card(4, 'k', topic='chem-1-4', concept='molecular-formula-of-phenol',
       source='pdf',
       from_runs=[((4, 'h', 'i'), 0, slice(14, 15)),
                  ((4, 'h', 'i'), 1, slice(0, 1))],
       use=[[0, 1]], marks=[6],
       notes='The scheme allows 3 of the 6 for an incorrect formula with six carbons and '
             'one oxygen. The paper draws the two structures beside the question, but the '
             'question itself names phenol and gives benzene\'s formula, so the drawing '
             'prompts the answer rather than carrying it.')


# ── Question 7(b): the pH scale passage (paper page 8) ───────────────────────
#
# The paper's block segmentation puts the word bank, the instruction and the
# whole passage into the part's stem and leaves "The following terms are
# omitted from the passage below." as the question text. Nothing is missing —
# the seven lettered blanks are in the stem where the paper prints them — but
# the two halves are the wrong way round on the card's face.
A.card(7, 'b', card_id='chem-2022-ol-q7-b-1', topic='chem-3-4',
       concept='the-ph-scale-and-the-ions-that-set-it',
       source='pdf',
       from_runs=[((4, 'b', None), 8, slice(1, 3)),
                  ((4, 'b', None), 11, slice(0, 2)),
                  ((4, 'b', None), 12, slice(0, 2)),
                  ((4, 'b', None), 13, slice(0, 2))],
       tariff='orderedSplit', ladder=30,
       notation='(4 x 6) + (3 x 2) (blanks A-D)',
       notes='Each row keeps the scheme\'s letter in front of its term, because the term only scores against the blank it belongs to. "(4 x 6) + (3 x 2)" pays the first four correct terms 6 each and the next three 2 each - the rate depends on how many blanks are right, not on which ones, so no blank has a mark of its own and every row is null. The paper prints the word bank, the instruction and the passage above the question; the block segmentation files all three as this part\'s stem. Split at blank D because a seven-row card does not fit the deck.')

A.card(7, 'b', card_id='chem-2022-ol-q7-b-2', topic='chem-3-4',
       concept='how-ph-changes-with-acidity-and-alkalinity',
       source='pdf',
       from_runs=[((4, 'b', None), 14, slice(0, 2)),
                  ((4, 'b', None), 15, slice(0, 2)),
                  ((4, 'b', None), 16, slice(0, 2))],
       tariff='orderedSplit', ladder=30, notation='(4 × 6) + (3 × 2)',
       notes='Each row keeps the scheme\'s letter in front of its term, because the term '
             'only scores against the blank it belongs to. "(4 × 6) + (3 × 2)" pays the '
             'first four correct terms 6 each and the next three 2 each — the rate '
             'depends on how many blanks are right, not on which ones, so no blank has a '
             'mark of its own and every row is null. The paper prints the word bank, the '
             'instruction and the passage above the question; the block segmentation '
             'files all three as this part\'s stem.')


# ── Question 8(b) and (c): oxidising ethanol along the scheme (paper page 9) ─
#
# Only the two "how many atoms, of which element" asks are carded. They name
# both molecules in the question itself, so neither needs the reaction scheme
# the paper draws; the other four romans of (b) and (c) say "this reaction",
# "reaction X" and "reaction Y", and the sentences that define X and Y are
# filed by Paper as part text rather than as a stem — see the REFUSED list.
# stem=False on both: paper.stem(8, 'b') and paper.stem(8, 'c') are both None,
# so card() would fall back to Q8's own stem, which the segmentation has left
# holding a fragment of the drawn scheme ("C6H12O6 glucose zymase W").
ETHANOL_POOL = ('Q8(b) is one pool of FOUR POINTS: [6 + 6 + 2 + 1] = 15 across (i)–(iii), '
                'the (15) the paper prints. Two of those four points fall in (i) — the '
                'number and the element are separately marked — and k correct points take '
                'the top k values, so these two are worth 6 + 6 = 12. The rate depends on '
                'how many points are right rather than on which, so both rows are null.')

A.card(8, 'b', 'i', topic='chem-4-2', concept='atoms-lost-when-ethanol-becomes-ethanal',
       source='pdf', stem=False,
       from_runs=[((4, 'b', 'i'), 1, slice(2, 3)),
                  ((4, 'b', 'i'), 1, slice(4, 6))],
       tariff='orderedSplit', ladder=12, notation='FOUR POINTS: [6 + 6 + 2 + 1]',
       notes=ETHANOL_POOL)

A.card(8, 'c', 'i', topic='chem-4-2', concept='atoms-gained-when-ethanal-becomes-ethanoic-acid',
       source='pdf', stem=False,
       from_runs=[((4, 'c', 'i'), 7, slice(2, 3)),
                  ((4, 'c', 'i'), 7, slice(4, 6))],
       tariff='orderedSplit', ladder=12,
       notation='FIVE POINTS: [6 + 6 + 3 + 2 + 1]',
       notes='Q8(c) is one pool of FIVE POINTS: [6 + 6 + 3 + 2 + 1] = 18 across (i)–(iii), '
             'the (18) the paper prints. Two of those five points fall in (i) — the number '
             'and the element are separately marked — and k correct points take the top k '
             'values, so these two are worth 6 + 6 = 12. Both rows are null because the '
             'rate depends on how many points are right rather than on which.')


# ── Question 9(a): the sodium flame test (paper page 10) ─────────────────────
#
# The scheme answers this with a four-row, three-column table: one column per
# method, one row per point. The PDF parser keeps most cells intact — the
# header row is welded onto Method 1's first cell and Methods 2 and 3 share the
# second-row cell, so those two are cut by token. The card follows Method 1
# down its column and hangs the other methods' cells on as alternatives where
# the parser left them whole.
A.card(9, 'a', topic='chem-u2', concept='flame-test-for-sodium',
       source='pdf',
       from_runs=[((4, 'b', None), 19, slice(7, None)),
                  ((4, 'b', None), 20, slice(0, None)),
                  ((4, 'b', None), 21, slice(0, None)),
                  ((4, 'b', None), 22, slice(0, None)),
                  ((4, 'b', None), 23, slice(0, 6)),
                  ((4, 'b', None), 24, slice(0, None)),
                  ((4, 'b', None), 26, slice(0, None)),
                  ((4, 'b', None), 27, slice(0, None))],
       use=[[0, 1, 2, 3], [4], [5, 6], [7]],
       tariff='orderedSplit', ladder=12, notation='ANY THREE: [6 + 4 + 2]',
       context='[*Allow ‘metal inoculating loop’, or ‘metal spatula’ for '
               '‘platinum (nichrome) wire’.]',
       checked='Page 10 of the paper was opened. The paper prints the part mark "(12)" '
               'after the question, so the text ends on a bracketed number rather than '
               'punctuation. The question itself is complete: "Describe how you could '
               'carry out a flame test to confirm the presence of sodium in a sample of '
               'a salt."',
       notes='The scheme sets three complete methods side by side and awards ANY THREE '
             'points from the table at [6 + 4 + 2]: three correct points score 12, two '
             'score 10, one scores 6. A point\'s value depends on how many were given '
             'rather than on which, so every row is null. The rows follow Method 1 — '
             'clean wire, dip, hold in the flame, read the colour — and the alternatives '
             'on the first and third rows are the matching cells of Methods 2 and 3. The '
             'asterisk on "wire" is the scheme\'s own footnote marker, quoted in the note '
             'on the first row. Method 2\'s and Method 3\'s second-row cells are not '
             'offered: the parser welded them into one block that cannot be cut apart '
             'without splitting a phrase.')


# ── Question 10(c): the MOXIE calculation on Mars (paper page 11) ────────────
#
# The stem carries the balanced equation with U+F0AE where the arrow belongs;
# glyphmap.json maps that character to "→", so build-deck's repairGlyphs fixes
# it. Both cards quote the scheme's banded final answer with its unit, which is
# the shape chem-2022-ol-q10-c-i and -c-ii already use for (i) and (ii).
A.card(10, 'c', 'iv', topic='chem-1-4', concept='moles-of-co2-from-the-mole-ratio',
       source='pdf', from_run=((4, 'c', 'iv'), 3, slice(2, 7)), marks=[3],
       context='The balanced equation 2CO2 → O2 + 2CO takes two moles of CO2 for every '
               'mole of O2, so the working is 0.16875 × 2. The scheme accepts anything '
               'in the range shown.',
       notes='chem-2022-ol-q10-c-ii records this part as skipped "because the scheme\'s '
             'own answer line names CO2 while the following part treats the same 0.3375 '
             'moles as CO". The two lines do not contradict each other: 2CO2 → O2 + 2CO '
             'consumes two moles of CO2 and releases two moles of CO for every mole of '
             'O2, so 0.16875 mol of O2 accounts for 0.3375 mol of CO2 in and 0.3375 mol '
             'of CO out, and the same number is correct in both places.')

A.card(10, 'c', 'v', topic='chem-1-4', concept='mass-of-co-from-moles',
       source='pdf', from_run=((4, 'c', 'v'), 0, slice(2, 7)), marks=[4],
       context='Two of the four marks are for Mr CO = 28 with n = m/Mr, and two for the '
               'answer, 0.3375 × 28. The scheme accepts anything in the range shown.',
       checked='Page 11 of the paper was opened. This is the last roman of Q10(c), so the '
               'paper prints the part mark "(25)" after it and the lifted text ends on a '
               'bracketed number rather than punctuation. The question itself is '
               'complete: "What mass of CO by-product was produced by MOXIE in one hour?"',
       notes='chem-2022-ol-q10-c-ii records this part as skipped "because it depends on '
             'the answer to (iv)". The scheme prices it on its own — a banded final '
             'answer of 9.45 – 9.52 g CO for 4 — so the card quotes that, in the same '
             'shape as the cards for (i) and (ii).')


# ── Question 11(b)(iii): the spreading smoke plume (paper page 12) ───────────
#
# The question points at the photograph of the Cumbre Vieja eruption, but it
# describes the phenomenon in words — "the spreading out of smoke in air" — so
# the term asked for does not depend on seeing the picture. stem=False because
# the segmentation left Q11(b)'s stem holding the sewage flow-chart labels from
# part (a) and the tail of (b)(iv).
A.card(11, 'b', 'iii', topic='chem-1-1', concept='diffusion-of-smoke-in-air',
       source='pdf', stem=False,
       from_runs=[((4, 'b', 'iii'), 5, slice(1, 2)),
                  ((4, 'b', 'iii'), 6, slice(0, 1))],
       use=[[0, 1]], marks=[3],
       notes='chem-2022-ol-q11-b-ii records this part as skipped because the Cumbre '
             'Vieja photograph is not reproduced. The question describes the phenomenon '
             'in words — "the spreading out of smoke in air" — and the term asked for '
             'follows from that description, so the photograph illustrates the ask '
             'rather than carrying it. Q11(b) is priced (3 × 3) + 3 + 3 + 9 + 1 = 25, '
             'the (25) the paper prints, and this roman is the third of those threes.')


# ── Refused, with the reason each is refused ─────────────────────────────────
REFUSED = [
    ('2022 OL Q1(a)(i)',
     'a copy-and-complete-the-diagram ask. "Copy and complete the diagram by labelling '
     'the locations of the ethanol and the catalyst and showing how the ethene gas could '
     'have been collected." Every marking point is a label placed on the apparatus '
     'drawing — LABELS: ethanol // catalyst, SHOW: collection over water / collection in '
     'gas syringe — so the card cannot ask the question without the drawing. The drawing '
     'exists as chemistry-2022-OL-paper-p02-i1.png in authored/chemistry-figures.json '
     'but is bound to no card, and nothing here may bind it. Needs a bound figure.'),

    ('2022 OL Q6(b)',
     'names lettered parts of art the deck cannot show. "Give the IUPAC names for '
     'compounds A, C and E" — A to E are five structural formulae drawn in a table on '
     'page 8, and the scheme answers "A: ethane // C: ethyne // E: methylbenzene". '
     'authored/chemistry-figures.json holds no figure for page 8, so the card needs a '
     'bound figure and a decoded label key for A to E.'),
    ('2022 OL Q6(c)(i)',
     '"Identify two compounds from the table that are gaseous at room temperature" — the '
     'scheme answers "A (ethane) / B (ethene) / C (ethyne)". Same missing table as Q6(b); '
     'needs the bound figure and the label key.'),
    ('2022 OL Q6(c)(ii)',
     '"Identify two aromatic hydrocarbons in the table" — the scheme answers '
     '"D (benzene) // E (methylbenzene, phenylmethane)". Same missing table as Q6(b).'),
    ('2022 OL Q6(d)',
     '"Which one of the compounds in the table is used industrially (i) in cutting and '
     'welding metals, (ii) to make addition polymers?" — the scheme answers "C (ethyne)" '
     'and "B (ethene)". Same missing table as Q6(b).'),
    ('2022 OL Q6(f)(i)',
     'the answer is a drawing. "Draw the structural formula for the second member of the '
     'homologous series to which B belongs." The scheme prints a displayed structure and '
     'the text layer carries only its caption, "CH3CHCH2", which has lost the double bond '
     'that is the whole point of the answer. The ask also depends on knowing which '
     'compound B is, which only the page 8 table supplies.'),
    ('2022 OL Q6(f)(ii)',
     'the answer is an annotation on a drawing. "In the structure you have drawn, clearly '
     'indicate any carbon atoms in tetrahedral geometry." The scheme\'s whole answer is '
     '"INDICATE:" followed by the marked-up structure, so the text layer holds no answer '
     'at all — a content-free row.'),

    ('2022 OL Q8(b)(ii)',
     '"Classify this reaction as an oxidation reaction or as a reduction reaction." What '
     '"this reaction" is comes from the part preamble, "Reaction X occurs in the human '
     'body as ethanol is metabolised", and from the reaction scheme drawn on page 9. '
     'paper.stem(8, "b") is None, so card() takes its stem from Q8\'s own, which holds '
     'only a fragment of the drawn scheme. Nothing here may type the preamble, so the '
     'card would ask a student to classify a reaction it never names.'),
    ('2022 OL Q8(b)(iii)',
     '"How does the geometry around the carbon atom to which the oxygen is attached '
     'change as reaction X occurs?" — same missing preamble as (ii). The answer, '
     '"tetrahedral to planar", is clean; the card becomes available as soon as the '
     'sentence defining reaction X can reach its stem.'),
    ('2022 OL Q8(c)(ii)',
     '"Classify this reaction as an oxidation reaction or as a reduction reaction." — '
     'the same sentence as (b)(ii), and the same missing preamble: "Reaction Y occurs '
     'when some ethanal is added to warm dilute acidified KMnO4 in a test-tube" is filed '
     'as part text, and paper.stem(8, "c") is None.'),
    ('2022 OL Q8(c)(iii)',
     '"What colour change is observed during reaction Y?" — same missing preamble as '
     '(c)(ii). The paper\'s block for this part also welds the whole drawn reaction '
     'scheme onto the end of the question ("... during reaction Y? (18) Y C2H5OH CH3CHO '
     'CH3COOH X KMnO4 / H+ ethanol ethanal ethanoic acid"), and suspect() does not flag '
     'it, so checked= cannot gate the trim.'),

    ('2022 OL Q9(b)(iii)',
     '"Identify the reducing agent in the redox reaction above." The reaction above is '
     '2Na + Cl2 → 2NaCl, printed in the part (b) preamble, and paper.stem(9, "b") and '
     'paper.stem(9) are both None — so the card would carry no equation and the phrase '
     '"the redox reaction above" would point at nothing. The answer, sodium (Na) for 3, '
     'is clean; the card needs the equation on its stem.'),

    ('2022 OL Q10(b)(iii)',
     '"Write the equilibrium constant (Kc) expression for this reaction." The scheme '
     'sets the answer as a stacked fraction in a bold maths font, and the text layer '
     'carries it as "Kc = ሾ𝐍𝐎𝟐 ሿ𝟐" over "ሾ𝐍𝟐𝐎𝟒ሿ" — the square brackets are private-use '
     'characters glyphmap.json does not map, the exponent is inline, and the division is '
     'lost with the layout. Lifting that ships an unreadable answer; composing '
     '"[NO2]²/[N2O4]" would be writing it, which law 1 forbids.'),
    ('2022 OL Q10(c)(iii)',
     '"How many molecules are there in this quantity of oxygen?" The scheme\'s answer is '
     '1.0 × 10^23 to 1.02 × 10^23 molecules of O2, and the extractor lost the '
     'superscripts: the lifted text reads "1.0 × 1023 – 1.02 × 1023 molecules O2", which '
     'is wrong by twenty-one orders of magnitude. Typing the exponent back in is writing '
     'the answer. chem-2022-ol-q10-c-ii already records this in its notes.'),

    ('2022 OL Q11(c)(ii)',
     '"In C what is the purpose of the glass wool plug?" C is column chromatography, one '
     'of three set-ups drawn on page 13 and lettered P, T and C. '
     'authored/chemistry-figures.json holds no figure for page 13, and the paper\'s '
     'block segmentation leaves Q11(c) a stem of "glass wool plug S P T or", so neither '
     'the drawing nor a key to its letters can reach the card. Needs a bound figure and '
     'a decoded label key for P, T and C.'),
    ('2022 OL Q11(c)(iii)',
     '"State what material acts as the stationary phase in the separation you have '
     'drawn." The scheme answers per set-up — "P: paper and water", "T: silica / '
     'alumina", "C: silica / alumina" — so the answer cannot be given without saying '
     'which of P, T and C was drawn. Needs the bound figure and the label key.'),
    ('2022 OL Q11(c)(iv)',
     '"Does the mobile phase move up or down through the stationary phase in the '
     'separation you have drawn?" — answered "P: up / T: up / C: down". Needs the bound '
     'figure and the label key.'),
    ('2022 OL Q11(c)(v)',
     '"Label with an X on your diagram the component most strongly adsorbed by the '
     'stationary phase." The answer is a position on the candidate\'s own drawing, and '
     'the scheme gives it per set-up: "P: lowest (can include S) / T: lowest / C: highest '
     '(can include top of column)". Needs the bound figure and the label key.'),
    ('2022 OL Q11(c)(vi)',
     '"Label with a Y on your diagram the component carried fastest by the mobile phase." '
     '— answered "P: highest / T: highest / C: lowest", a position on a drawing. Needs '
     'the bound figure and the label key.'),
    ('2022 OL Q11(c)(vii)',
     'the paper\'s block welds the question\'s tail onto it: the lifted text is "Describe '
     'the result you would expect to get if the components of the mixture were all '
     'insoluble in the mobile phase. (25) This question continues on the next page." '
     'suspect() does not flag it, so checked= cannot gate a trim, and first_sentence= '
     'refuses because this scheme prints no question text for the trim to be confirmed '
     'against. Only one card in the whole 806-card Chemistry deck carries a trailing part '
     'mark; this would be the first to carry a page-turn instruction as well. The first '
     'three of the scheme\'s alternatives — no separation / no bands / no spots — are '
     'clean and free of P, T and C, so the card becomes available as soon as the text can '
     'be trimmed.'),
]
for ref, why in REFUSED:
    print(f'  REFUSED {ref}: {why}', file=sys.stderr)

A.emit()
