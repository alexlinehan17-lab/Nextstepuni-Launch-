#!/usr/bin/env python3
"""Biology 2025 Ordinary Level.

Where the answers live
----------------------
The scheme and the paper agree on numbering for this sitting: scheme page 13 is
Question 7 and the paper prints the mitosis question as Question 7. What does
not agree is the two PARSERS. Both drift, and they drift by different amounts on
different pages — Scheme files Q7(b)'s "Nucleus" under its own Q7(a), SchemePdf
files it under Q6(b); Q17(a)(i)'s heart answers land under SchemePdf's Q16(d)(i)
and Q17(c)(i)'s under its Q17(b)(i). So `from_run` below names the PARSER's key,
never the scheme's, and every citation is the paper's own. Each key was found by
searching both parsers for the answer text rather than by trusting either one's
numbering.

The other structural fact: Section A (Q1–Q7) prices nothing per part. One ladder
covers a whole question — "Q7 (a) – (e) Number of correct responses 1 2 3 4 5 6 7
/ Mark 3 6 9 12 15 18 20" — so a Section A part with no printed mark is carded
`ladder=`, which puts the scale in the notation and refuses to invent a per-part
tariff. Section B and C do print a mark beside each answer, so those are ordinary
`marks=`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2025, 'ol')

# CORRECTION, not an addition. This card shipped answering "write the letters in
# the correct order" with the string "Question 7" — the scheme PDF's page HEADING,
# taken because the run index was 2 where the answer sits at 4. The heading traced
# to the scheme, so the provenance gate passed it, and a card that teaches the
# order of mitosis taught a page number instead. The id, the citation and the
# tariff are untouched; only the wrong marking point is replaced.
#
# The old note was wrong too. The scheme does NOT number this under its own
# Question 6 — page 13 of the scheme is headed "Question 7", same as the paper.
# It is the PDF parser that keys the block as Q6(a), which is why from_run says 6.
A.card(7, 'a', topic='bio-1-4', concept='order-of-the-stages-of-mitosis',
       source='pdf', from_run=((6, 'a', None), 4, slice(0, 4)), marks=[6],
       notation='3 for any two in the right place, 6 for all four',
       notes='The scheme prints the order as "C, B, D, A" and pays 3 for any two '
             'letters in the right place, 6 for all four.')

# ── Section A ──────────────────────────────────────────────────────────────
# No per-part mark exists anywhere on scheme page 13; the ladder is the tariff.
A.card(7, 'b', topic='bio-2-3', concept='organelle-labelled-in-a-mitosis-image',
       source='pdf', from_run=((6, 'b', None), 1, slice(0, None)),
       ladder=3, tariff='orderedSplit', notation='6(3) + 2',
       notes='Q7 (a)–(e) is marked on one ladder — 6(3) + 2, three marks a response up '
             'to six and capped at 20 — so no part of it carries a mark of its own. '
             'Image A is the one where the cell is pinched at its waist and X points to '
             'the lower of its two new nuclei.')

# ── Section B ──────────────────────────────────────────────────────────────
A.card(9, 'b', 'vii', topic='bio-u2',
       concept='labelling-the-axes-of-an-enzyme-rate-graph',
       source='pdf', use=[1, 2], marks=[3, 3], labels='auto', stem=False,
       notes='The stem is dropped: the paper reader hands Q9(b) the graph\'s x-axis '
             'scale, "2 4 6 8 10 12", which is figure furniture rather than prose.')

# ── Section C ──────────────────────────────────────────────────────────────
# Q11(c) — the two word-cycle diagrams, X and Y.
A.card(11, 'c', 'i', topic='bio-3-2', concept='naming-the-nitrogen-cycle',
       source='md', use=[0], marks=[3], stem=False,
       notes='Diagram X runs nitrogen gas in the atmosphere to nitrates in the soil to '
             'plant protein to animal protein to ammonia and back.')

A.card(11, 'c', 'ii', topic='bio-3-2',
       concept='nitrogen-cycle-stages-on-the-diagram',
       source='pdf', use=[2, 3, 4], marks=[3, 3, 3], labels='auto', stem=False)

A.card(11, 'c', 'iii', topic='bio-3-2', concept='naming-the-carbon-cycle',
       source='md', use=[0], marks=[3], stem=False,
       notes='Diagram Y runs carbon dioxide gas in the atmosphere to plant carbohydrate '
             'to animal carbohydrate to dead organic matter and fossil fuels.')

A.card(11, 'c', 'iv', topic='bio-3-2',
       concept='carbon-cycle-stages-on-the-diagram',
       source='pdf', use=[2, 3, 4], marks=[3, 3, 3], labels='auto', stem=False,
       checked='The paper sets all four parts of Q11(c) in one block and prints the '
               'part mark "(24)" at the end of it, so this part\'s text is flagged only '
               'because it ends on the tariff rather than on punctuation. Page 2 of the '
               'Section C paper shows the ask whole.')

# Q12(b) — the pea-plant crosses. Both parts are answer-plus-justification, which
# is the shape the scheme prints and the shape the card keeps.
A.card(12, 'b', 'iv', topic='bio-1-4',
       concept='whether-two-short-parents-can-give-a-tall-plant',
       source='md', use=[0, 1], marks=[3, 3],
       notes='Tallness (T) is dominant to shortness (t); a short plant can only be tt.')

A.card(12, 'b', 'v', topic='bio-1-4',
       concept='whether-two-tall-parents-can-give-a-short-plant',
       source='md', use=[0, 1], marks=[3, 3],
       checked='The paper sets the whole of Q12(b) in one block and prints the part '
               'mark "(27)" after this last part, so the text is flagged only for '
               'ending on the tariff. Page 3 of the Section C paper shows the ask '
               'whole.',
       notes='Tallness (T) is dominant to shortness (t), so a tall parent may be TT or '
             'Tt — which is what makes this the opposite answer to part (iv).')

A.card(12, 'c', 'i', topic='bio-1-4',
       concept='replication-transcription-and-translation-diagrams',
       source='md', use=[0, 1, 2], marks=[3, 3, 3], stem=False,
       checked='The paper runs Q12(c)(i) straight into (ii) inside one block, so this '
               'part stops on the last of its three numbered descriptions with no full '
               'stop. Page 3 of the Section C paper shows the three descriptions are '
               'the whole of what is to be matched.',
       notes='The three diagrams on the paper are: a DNA helix separating into two '
             'identical helices (A), a ribosome with a beaded strand through it (B), '
             'and DNA with messenger RNA leaving it (C). The stem is dropped: the '
             'paper reader hands Q12(c) the captions of all three diagrams together '
             'with the wording of later parts.')

# Q13 — metabolism, and the name for anaerobic respiration in micro-organisms.
A.card(13, 'a', 'i', topic='bio-2-2', concept='what-metabolism-is',
       source='pdf', from_run=((12, 'a', 'i'), 2, slice(0, None)), marks=[3],
       notes='The scheme accepts either the sentence itself or just the letter A.')

A.card(13, 'c', 'iv', topic='bio-2-2',
       concept='anaerobic-respiration-in-micro-organisms',
       source='md', use=[0], marks=[3], stem=False,
       checked='The paper sets all four parts of Q13(c) in one block and prints the '
               'part mark "(24)" at the end, so this part\'s text is flagged only for '
               'ending on the tariff. Page 4 of the Section C paper shows the ask and '
               'its three options — Filtration, Fermentation, Diffusion — whole. The '
               'stem is dropped: the paper reader hands Q13(c) the wording of part '
               '(ii), which is a different ask.')

# Q14(a)(ii) — the shoot system on the whole-plant diagram.
A.card(14, 'a', 'ii', topic='bio-2-6',
       concept='shoot-system-on-the-plant-diagram',
       source='md', from_run=((13, 'a', 'ii'), 0, slice(0, None)), marks=[3],
       notes='The paper braces the plant twice: the lower brace is labelled "Root '
             'system" in words, the upper one — spanning stem and leaves — carries the '
             'letter X.')

# Q15 — reproduction.
A.card(15, 'b', 'vi', topic='bio-2-5',
       concept='placenta-and-foetus-on-the-diagram',
       source='md', use=[0, 1], marks=[3, 3], stem=False,
       labels={'X': 'Placenta', 'Y': 'Foetus'},
       notes='The stem is dropped: the paper reader hands Q15(b) the single letter "X" '
             'lifted off the diagram.')

A.card(15, 'c', 'i', topic='bio-2-5',
       concept='male-reproductive-parts-on-the-diagram',
       source='md', use=[0, 1, 2], marks=[3, 3, 3],
       labels={'A': 'Sperm duct', 'B': 'Prostate gland', 'C': 'Testis'},
       notes='The scheme prints the match the other way round — term first, then the '
             'letter — so the rows read "1. Testis C" rather than "C: Testis".')

A.card(15, 'c', 'iv', topic='bio-2-5', concept='sketching-a-sperm-cell',
       source='md', first_sentence=True, row_kind='criterion',
       from_runs=[((15, 'c', 'iv'), 0, slice(4, None)),
                  ((15, 'c', 'iv'), 1, slice(0, None))],
       marks=[3, 6], notation='3 + 2(3)',
       notes='The scheme pays the sketch and the labels separately: three marks for a '
             'sketch showing a head and a tail, and 2(3) — two labels at three marks '
             'each — for naming and positioning them. The paper prints the part mark '
             '"(24)" and the diagram letter "C" after the question; the card carries '
             'the scheme-confirmed first sentence instead.')

# Q16(a)(ii) — the substrate/enzyme/product table.
A.card(16, 'a', 'ii', topic='bio-2-1',
       concept='matching-enzymes-to-substrates-and-products',
       source='pdf',
       from_runs=[((15, 'c', 'ii'), 2, slice(0, None)),
                  ((15, 'c', 'ii'), 3, slice(0, None)),
                  ((15, 'c', 'ii'), 4, slice(0, None))],
       marks=[6, 3, 3], notation='4(3)', stem=False,
       checked='The paper sets the table as four separate blocks and the reader welds '
               'them onto the question, so the text runs "…complete the table. List: '
               'Protease Maltose Starch Lipase Substrate Enzyme Product Amylase Lipids '
               'Triglycerides Protein Amino acid" with no full stop at the end. Page 7 '
               'of the Section C paper shows those trailing words are the table\'s '
               'header row and its already-filled cells, which is why they are flagged '
               'and why they are right.',
       notes='The scheme prices this 4(3) — four words placed at three marks each, '
             'twelve in all. The paper leaves two cells blank in the amylase row '
             '(Starch and Maltose) and one in each of the other two (Lipase, '
             'Protease), which is how the twelve divide across the three rows here. '
             'The rows are the completed table; the words the candidate had to place '
             'are Protease, Maltose, Starch and Lipase.')

# Q16(d)(i) — draw a virus. A drawing question, split by what the scheme says.
A.card(16, 'd', 'i', topic='bio-3-2', concept='drawing-and-labelling-a-virus',
       source='md', row_kind='criterion',
       from_runs=[((15, 'c', 'i'), 6, slice(0, None)),
                  ((15, 'c', 'i'), 7, slice(0, None))],
       marks=[3, 6], notation='3 + 2(3)', stem=False,
       notes='The scheme pays the drawing three and the two labels 2(3) — three marks '
             'each. It names the second label "DNA" where the paper asks for "Nucleic '
             'acid". The stem is dropped: the paper reader hands Q16(d) the bacterial '
             'shapes wording, which belongs to part (v).')

# Q17(a) — the heart.
A.card(17, 'a', 'i', topic='bio-2-6', concept='heart-parts-on-the-diagram',
       source='pdf',
       from_runs=[((16, 'd', 'i'), 5, slice(0, None)),
                  ((16, 'd', 'i'), 6, slice(0, None)),
                  ((16, 'd', 'i'), 7, slice(0, None))],
       marks=[3, 3, 3], labels='auto', stem=False,
       notes='The stem is dropped: the paper reader hands Q17(a) the diagram\'s own '
             'labels, "Right ventricle Y X".')

A.card(17, 'a', 'iv', topic='bio-2-6', concept='telling-an-artery-from-a-vein',
       source='md',
       from_runs=[((16, 'd', 'iv'), 0, slice(0, None)),
                  ((16, 'd', 'iv'), 1, slice(0, None))],
       marks=[3, 3], stem=False,
       notes='The scheme wants the letter and the reason separately; either feature of '
             'the wall alone earns the second three marks.')

# Q17(c) — the breathing system.
A.card(17, 'c', 'i', topic='bio-2-6',
       concept='breathing-system-parts-on-the-diagram',
       source='pdf',
       from_runs=[((17, 'b', 'i'), 4, slice(0, None)),
                  ((17, 'b', 'i'), 5, slice(0, None)),
                  ((17, 'b', 'i'), 6, slice(0, None))],
       marks=[3, 3, 3], labels='auto', stem=False,
       notes='The stem is dropped: the paper reader hands Q17(c) the wording of part '
             '(ii) together with the diagram labels Capillary, Alveolus, Rib and '
             'Diaphragm.')

A.card(17, 'c', 'iii', topic='bio-2-6',
       concept='how-the-diaphragm-moves-during-inhalation',
       source='md', from_run=((17, 'b', 'iii'), 0, slice(2, None)), marks=[3],
       stem=False)

A.card(17, 'c', 'iv', topic='bio-2-6',
       concept='how-the-ribcage-moves-during-inhalation',
       source='md', from_run=((17, 'b', 'iv'), 0, slice(2, None)), marks=[3],
       stem=False)

# ── Refused, and why ───────────────────────────────────────────────────────
# Said out loud rather than left as silence, so the next pass over this sitting
# does not have to rediscover any of it. Every entry below is a paper ask the
# scheme does not support a card for.
for ref, why in (
    ('2025 OL Q1(c)',
     'the scheme answers the tick-box by redrawing the correct structure, and the '
     'drawing extracts as four detached labels — "Fatty acid", "Glycerol", "Fatty '
     'acid", "Fatty acid". No printed text says which of the paper\'s boxes is '
     'right, so a single row would have to be assembled here rather than lifted'),
    ('2025 OL Q5(a)',
     'the four tropisms are matched to four UNLETTERED diagrams and the scheme '
     'answers positionally — "Geotropism Hydrotropism" sits under one row of '
     'panels, "Chemotropism Phototropism" under the other. Pairing a tropism to '
     'its panel in text means composing the pair; labels= needs letters the paper '
     'never prints, and the catalogued crops of the grid are truncated'),
    ('2025 OL Q5(d)',
     'the scheme answers "Give one way in which plant growth regulators are used '
     'commercially." with "Correct commercial use given" and names no use'),
    ('2025 OL Q8(b)(i)',
     'the scheme answers with "Named test or named reagent" and names neither the '
     'test nor the reagent for starch'),
    ('2025 OL Q8(b)(ii)',
     'the scheme answers with "Named test or named reagent(s)" and names neither '
     'the test nor the reagent for a reducing sugar'),
    ('2025 OL Q8(b)(iii)',
     'the scheme answers with "Named test or named reagents" and names neither the '
     'test nor the reagent for protein'),
    ('2025 OL Q8(b)(iv)',
     'the scheme answers with "Named test or named reagent" and names neither the '
     'test nor the reagent for lipid'),
    ('2025 OL Q9(b)(i)',
     'the scheme answers "Name the enzyme you used." with "Correctly named enzyme" '
     'and names no enzyme'),
    ('2025 OL Q9(b)(ii)',
     'the scheme answers with "Correctly named and matching substrate" and names no '
     'substrate — it cannot, because the answer has to match whatever enzyme the '
     'candidate named in (b)(i)'),
    ('2025 OL Q9(b)(vi)',
     'the scheme answers with "Correct safety precaution given" and gives none'),
    ('2025 OL Q10(b)(i)',
     'the scheme answers with "Correctly named suitable seed" and names no seed'),
    ('2025 OL Q11(b)(i)',
     'the scheme answers "Give one adaptation of the lesser horseshoe bat." with '
     '"Correct adaptation given" and gives none'),
    ('2025 OL Q11(b)(ii)',
     'the scheme answers with "Correct habitat named" and names no habitat'),
    ('2025 OL Q13(b)(vi)',
     'the scheme answers with "Valid way suggested" and suggests none'),
    ('2025 OL Q15(c)(iii)',
     'the scheme answers "Name any method of contraception." with "Correct method '
     'named" and names no method'),
    ('2025 OL Q16(d)(iii)',
     'the scheme answers "Name any two harmful examples of viruses." with "Two '
     'correctly named" and names none'),
    ('2025 OL Q17(b)(v)',
     'the scheme answers with "Correct matching function given" and gives none — it '
     'has to match whichever of P, Q or R the candidate names'),
    ('2025 OL Q17(b)(vi)',
     'the scheme answers with "Correct possible cause given" and gives no cause for '
     'either arthritis or osteoporosis'),
    ('2025 OL Q17(c)(v)',
     'the scheme answers with "Valid disorder of the breathing system named" and '
     '"Valid and matching treatment given" — two criteria, no disorder and no '
     'treatment'),
):
    print(f'REFUSED {ref}: {why}', file=sys.stderr)

A.emit()
