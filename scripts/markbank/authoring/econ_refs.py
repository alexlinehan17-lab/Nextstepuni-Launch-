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
    'econ-2021-ol-q13-c-ii': '2021 OL Q14(b)(ii) — care for the environment',
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
    # 2021 Higher — the homelessness stimulus is part (c) of question 16; the
    # cards were keyed (a) off the scheme's running order. Found by the
    # adversarial verification fleet, confirmed against the paper: (a) is the
    # air-passenger data, (b) the minimum-wage graph, (c) homelessness.
    'econ-2021-hl-q16-a-i': '2021 HL Q16(c)(i)',
    'econ-2021-hl-q16-a-ii': '2021 HL Q16(c)(ii)',
    # 2023 Higher — MNC over-reliance and competitiveness are question 13(c);
    # (b) is the MPS/multiplier table the deck never carded.
    'econ-2023-hl-q13-b-i': '2023 HL Q13(c)(i)',
    'econ-2023-hl-q13-b-ii': '2023 HL Q13(c)(ii)',
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
    # 2021 HL backfill: four-word asks below refcheck's six-token floor, each
    # verified by hand against the paper (pages 19, 31, 32).
    'econ-2021-hl-q12-a-i',
    'econ-2021-hl-q15-b-i',
    'econ-2021-hl-q15-c-i',
    'econ-2021-hl-q12-a-ii-pos',      # paper asks for both sides in one sentence
    'econ-2021-hl-q12-a-ii-neg',
    'econ-2021-hl-q13-c-ii',          # paper: "Based on the figure you have calculated"
    'econ-2021-hl-q11-c-i',           # 2021 HL p18: "(i) Define Internal Economies of Scale." (five words)
    'econ-2021-ol-q11-b-iii',         # paper writes "MNCs", the card writes it out
    'econ-2021-ol-q11-b-i-neg',       # paper offers advantage OR disadvantage
    'econ-2021-ol-q11-b-i-pos',
    'econ-2021-ol-q11-c-i',           # 2021 OL p12: "Explain the term economic growth." (five words)
    'econ-2021-ol-q14-b-i',           # 2021 OL p20: "(i) Define the term mixed economy." (five words)
    'econ-2021-ol-q15-c-i',           # 2021 OL p24: "Explain the concept of scarcity." (five words)
    'econ-2022-hl-q13-c-i',           # paper names the OECD in full over two lines
    'econ-2022-hl-q12-a-iii',         # 2022 HL p19: "(iii) Explain the term privatisation." (four words)
    'econ-2022-hl-q11-c-i',           # 2022 HL p16: "(i) Explain the term opportunity cost." (five words)
    'econ-2022-ol-sa-q1-ii',          # 2022 OL p3: "(ii) Explain the term economic growth." (five words)
    'econ-2022-ol-sa-q7-a-i',         # 2022 OL p7: "(i) Explain the term fixed costs." (five words)
    'econ-2022-ol-sa-q10-b',          # 2022 OL p9: "(b) Explain the term National Debt." (five words)
    'econ-2022-ol-q12-c-i',           # 2022 OL p15: "(i) Explain the term sustainability." (four words)
    'econ-2022-ol-q16-b-i',           # 2022 OL p26: "(i) Explain the term price inflation." (five words)
    'econ-2023-hl-q11-b-ii',          # paper: "influence geographical mobility"
    'econ-2023-hl-q16-b-ii',          # paper: "challenges the economy will face"
    'econ-2023-hl-q16-b-iii',         # paper: "Describe initiatives the Irish government"
    'econ-2023-ol-q16-a-i',           # paper: "Explain any two of the above terms"
    'econ-2025-ol-q15-a-i',           # paper: "the Irish government and citizens in Ireland"
    'econ-2025-ol-q15-a-i-entrepreneur',  # 2025 OL p23: "Explain the term entrepreneur." (four words)
    'econ-2025-ol-q15-b-ii',          # 2025 OL p24: "(ii) Explain your answer." (three words)
    'econ-2024-hl-sa-q5-b',           # 2024 HL p7: "(b) Explain your diagram above." (four words)
    'econ-2024-hl-q13-b-i',           # 2024 HL p22: "(i) Explain the term globalisation." (four words)
    'econ-2024-ol-q15-b-ii',          # 2024 OL p23: "(ii) Explain your answer." (three words)
    'econ-2023-hl-q15-b-i',           # 2023 HL p30: "(i) Explain the term monetary policy." (five words)
    'econ-2019-ol-sb-q3-b-i',         # 2019 OL p7: "(i) Explain the term underlined above." (five words)
    'econ-2019-ol-sb-q4-c-i',         # 2019 OL p7: "(i) Explain the term opportunity cost." (five words)
    'econ-2019-ol-sb-q8-b-i',         # 2019 OL p10: "(i) Explain the term infrastructure." (four words)
    'econ-2020-hl-sa-q6-i',           # 2020 HL p4: "(i) Define the term fiscal policy:" (five words)
    'econ-2020-hl-sb-q3-a-i',         # 2020 HL p8: "(i) Define the underlined term." (four words)
    'econ-2020-hl-sb-q4-c-i',         # 2020 HL p9: "(i) Define internal economies of scale." (five words)
    'econ-2018-hl-sb-q4-a-i',         # 2018 HL p8: "(i) Define the term labour productivity." (five words)
    'econ-2018-hl-sb-q5-b-i',         # 2018 HL p8: "(i) Explain the term indirect tax." (five words)
    'econ-2018-hl-sb-q5-c-i',         # 2018 HL p8: "(i) Define the term budget deficit." (five words)
    'econ-2018-hl-sb-q8-a-iv',        # 2018 HL p10: "(iv) the size of the Multiplier." (four words)
    'econ-2018-hl-sa-q9-a',           # 2018 HL p5: "(a) Define the term price discrimination." (five words)
    'econ-2018-hl-sb-q3-a-i',         # 2018 HL p7: "(i) Define the term marginal cost." (five words)
    'econ-2018-ol-sa-q4-i',           # 2018 OL p3: "(i) Name economist:" (two words; the ask is its stem)
    'econ-2018-ol-sa-q7-i',           # 2018 OL p3: "(i) Price Inflation:" (two words; the ask is its stem)
    'econ-2018-ol-sb-q5-b-i',         # 2018 OL p8: "(i) Name each tax above." (four words)
    'econ-2018-ol-sb-q5-c-i',         # 2018 OL p8: "(i) Explain the term opportunity cost." (five words)
    'econ-2018-ol-sb-q7-a-i',         # 2018 OL p9: "(i) Explain the term open economy." (five words)
    'econ-2017-hl-sb-q5-b-i',         # 2017 HL p7: "(i) Describe two trade protectionist measures." (five words)
    'econ-2017-hl-sb-q7-b-i',         # 2017 HL p8: "(i) Explain the term privatisation." (four words)
    'econ-2017-ol-sb-q4-c-i',         # 2017 OL p7: "(i) Explain the term price inflation." (five words)
    'econ-2017-ol-sb-q5-a-i',         # 2017 OL p8: "(i) Explain the term multiplier." (four words)
    'econ-2017-ol-sb-q5-c-i',         # 2017 OL p8: "(i) Explain the term economic growth." (five words)
    'econ-2017-ol-sb-q7-b-i',         # 2017 OL p9: "(i) Explain the underlined term." (four words)
    'econ-2016-hl-sa-q1-b-ii',        # 2016 HL p2: "(ii) Explain the term supernormal profit" (five words)
    'econ-2016-hl-sa-q7-a',           # 2016 HL p4: "(a) Define the term monetary policy." (five words)
    'econ-2016-hl-sb-q5-a-i',         # 2016 HL p7: "(i) Define the term full employment." (five words)
    'econ-2016-hl-sb-q6-a-i',         # 2016 HL p7: "(i) Explain the term exchange rate." (five words)
    'econ-2016-ol-sa-q4-b',           # 2016 OL p3: "(b) Profit made on sales." (four words)
    'econ-2016-ol-sa-q7-a',           # 2016 OL p4: "(a) Explain the term branding." (four words)
    'econ-2016-ol-sa-q8-a',           # 2016 OL p4: "(a) Explain the term black economy." (five words)
    'econ-2016-ol-sb-q1-b-i',         # 2016 OL p5: "(i) Explain the underlined term." (four words; the only one on p5)
    'econ-2015-hl-sb-q1-b-i',         # 2015 HL p5: "(i) Exceptionally wet weather conditions" (four words; the stem carries the ask)
    'econ-2015-hl-sb-q7-c-i',         # 2015 HL p8: "(i) Define the term economic growth." (five words)
    'econ-2015-ol-sb-q1-c-i',         # 2015 OL p5: "(i) Explain the term brand loyalty." (six words)
    'econ-2015-ol-sb-q3-a-i',         # 2015 OL p7: "(i) Explain the underlined term above." (five words)
    'econ-2015-ol-sb-q5-b-i',         # 2015 OL p8: "(i) Explain the economic term embargo." (six words)
    'econ-2014-hl-sb-q7-a-ii',        # 2014 HL p8: "(ii) Outline three characteristics of LDCs." (five words)
    'econ-2014-ol-sb-q1-b-i',         # 2014 OL p5: "(i) Explain the underlined term." (four words; the stem carries the term)
    'econ-2014-ol-sb-q2-b-i',         # 2014 OL p6: "(i) Explain the Law of Demand." (five words)
    'econ-2014-ol-sb-q6-a-i',         # 2014 OL p8: "(a) Explain the following terms: (i) Barter;" (the ask with its own term)
    'econ-2014-ol-sb-q6-a-ii',        # 2014 OL p8: "(a) Explain the following terms: ... (ii) Money;"
    'econ-2014-ol-sb-q6-a-iii',       # 2014 OL p8: "(a) Explain the following terms: ... (iii) Price Inflation."
    'econ-2013-hl-sb-q2-c-i',         # 2013 HL p4: "(i) Explain the term ‘competitive advertising’." (five words)
    'econ-2013-ol-sb-q4-b-i',         # 2013 OL p6: "(i) Explain the term 'VAT'." (four words)
    'econ-2013-ol-sb-q7-c-ii',        # 2013 OL p8: "(ii) Name one other Irish MNC." (five words)
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
