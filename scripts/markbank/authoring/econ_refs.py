"""Cards whose id names the wrong question, and the citation the paper gives.

A card's id was written by hand from where its part sat in the marking scheme.
For nineteen cards that count was wrong. The scheme is a table flattened into
one long line, and a question number printed at the foot of one page comes back
as more parts of the previous question — so "Question 15" was read as more of
question 14, and every card built from that block cited a question it did not
come from. Nothing upstream could notice: the claims still traced, because the
claims came from the right block of text. It was econ_refcheck.py, which checks
each citation against the QUESTION PAPER rather than the scheme, that found
them.

The ids are deliberately left alone. A card id is the key a student's review
history is stored under; renaming nineteen of them would orphan that history to
correct a string no student ever sees. What a student does see — the citation
printed on the card — is corrected here, and econ_refcheck.py is what keeps it
correct from now on.

Every entry below was confirmed by reading the paper: the page it is printed on,
the "Question N" heading that page falls under, and the part letters between
that heading and the text.
"""

# card id -> the citation the question paper supports
CORRECTIONS = {
    # 2021 Higher — the air-passenger part is on page 35, under Question 16.
    'econ-2021-hl-q15-b-iii': '2021 HL Q16(a)(iii)',
    # 2021 Ordinary — questions 14 and 16 each absorbed the one after them.
    'econ-2021-ol-q13-c-ii': '2021 OL Q14(b)(ii)',
    'econ-2021-ol-q13-c-iii': '2021 OL Q14(c)(iii)',
    'econ-2021-ol-q14-a-i': '2021 OL Q16(b)(i)',
    'econ-2021-ol-q15-a-i': '2021 OL Q16(c)(i)',
    'econ-2021-ol-q15-a-ii': '2021 OL Q16(c)(ii)',
    # 2022 Ordinary — every Section B citation after question 13 was one short.
    'econ-2022-ol-q13-a-i': '2022 OL Q14(c)(i)',
    'econ-2022-ol-q13-a-ii': '2022 OL Q14(c)(ii)',
    'econ-2022-ol-q14-a-ii': '2022 OL Q15(b)(ii)',
    'econ-2022-ol-q14-a-iii': '2022 OL Q15(b)(iii)',
    'econ-2022-ol-q14-b-ii': '2022 OL Q15(c)(ii)',
    'econ-2022-ol-q15-a-i': '2022 OL Q16(a)(i)',
    'econ-2022-ol-q15-a-iii-social': '2022 OL Q16(a)(iii) — social benefit',
    'econ-2022-ol-q15-a-iii-private': '2022 OL Q16(a)(iii) — private benefit',
    # 2023 Higher — trade protection is question 14(c), on page 28; question 15
    # does not start until page 29.
    'econ-2023-hl-q15-b-ii': '2023 HL Q14(c)(ii)',
    'econ-2023-hl-q15-b-iii': '2023 HL Q14(c)(iii)',
    # 2024 Ordinary — the energy part is question 11(c), not 12(c).
    'econ-2024-ol-q12-c-ii': '2024 OL Q11(c)(ii)',
    # Right question, wrong part letter. Neither of these could be caught by the
    # question-number check; both were found by reading the paper for the cards
    # it could not place, which is why that list is reported and not ignored.
    'econ-2023-ol-q16-a-i': '2023 OL Q16(b)(i)',
    'econ-2025-ol-q15-a-i': '2025 OL Q15(c)(i)',
    # Found on the second pass, by reading the 2025 Ordinary paper's own part
    # structure while working the Section B backlog. The question NUMBER was
    # right in each, which is why econ_refcheck.py could not see them: it
    # asserts the number, because the number comes from a heading the paper
    # prints and the part path has to be reconstructed from markers in an
    # answer booklet. Paths still need eyes.
    'econ-2025-ol-q16-a-iii': '2025 OL Q16(b)(iii)',
    'econ-2025-ol-q16-b-i-ag': '2025 OL Q16(c)(i) — agricultural sector',
    'econ-2025-ol-q16-b-i-ind': '2025 OL Q16(c)(i) — industrial sector',
    # 2024 OL Q14(a)(ii) is "outline one reason why the Irish government
    # contributes to the EU Budget". The exports question is Q14(c)(ii). Found
    # when a duplicate-question-text check paired this card with a new one
    # written from the same block of the scheme.
    'econ-2024-ol-q14-a-ii': '2024 OL Q14(c)(ii)',
}


# Cards econ_refcheck.py cannot place, each read against the paper by hand and
# found to cite it correctly. They cannot be placed automatically because the
# card asks the question in fewer words than the paper does — "Outline two
# positive impacts of globalisation" against a paper that asks for two positive
# AND two negative in one sentence, or "multinational companies" against a paper
# that writes "MNCs" — so no six-word run of the card appears in the paper.
#
# Listed so that a card the checker cannot place is a thing someone decided
# about, not a thing nobody noticed. A NEW unplaceable card is reported.
HAND_CHECKED = {
    'econ-2021-hl-q12-a-ii-pos',      # paper asks for both sides in one sentence
    'econ-2021-hl-q12-a-ii-neg',
    'econ-2021-hl-q13-c-ii',          # paper: "Based on the figure you have calculated"
    'econ-2021-ol-q11-b-iii',         # paper writes "MNCs", the card writes it out
    'econ-2021-ol-q11-b-i-neg',       # paper offers advantage OR disadvantage
    'econ-2021-ol-q11-b-i-pos',
    'econ-2022-hl-q13-c-i',           # paper names the OECD in full over two lines
    'econ-2023-hl-q11-b-ii',          # paper: "influence geographical mobility"
    'econ-2023-hl-q16-b-ii',          # paper: "challenges the economy will face"
    'econ-2023-hl-q16-b-iii',         # paper: "Describe initiatives the Irish government"
    'econ-2023-ol-q16-a-i',           # paper: "Explain any two of the above terms"
    'econ-2025-ol-q15-a-i',           # paper: "the Irish government and citizens in Ireland"
    # The card asks a narrower question than the part it comes from: the paper
    # asks the student to explain price discrimination AND give an example, and
    # this card is the example alone, because the explanation is printed as the
    # question head and there is nothing left of it to mark against. Read
    # against the 2024 Higher paper: question 8(a).
    'econ-2024-hl-sa-q8-a',
}


# Cards deliberately withdrawn, and why. rebaseline.py refuses to drop a card id
# that is not listed here, because a vanished id is normally a slicing accident
# and the whole point of the baseline is to catch it. A withdrawal has to be a
# decision someone wrote down.
WITHDRAWN = {
    # Shipped 22 August 2026 in the Section B backlog pass and withdrawn the same
    # day. It asked the identical question of the identical paper as
    # econ-2024-ol-q14-a-ii — "outline two reasons why exports are important for
    # the Irish economy" — because that card's id counts the wrong question
    # (Q14(a)(ii) is the EU Budget question) and the part-path heuristic put the
    # exports part one letter away, so the coverage check could not see it. The
    # older id is kept because a student's review history is on it; its citation
    # and its tariff are corrected above and in econ_2024_ol.py.
    'econ-2024-ol-q14-c-ii',
}
