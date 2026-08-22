#!/usr/bin/env python3
"""Economics 2024 Higher Level — Section B.

Every option is SLICED out of the scheme, never retyped, so re-running this is
how a card's provenance is audited without re-reading the PDF.

What is carded and what is not:

  * `⟨N @ M⟩` over a list of named responses is the shape this subject is full
    of, and it becomes one `anyN` row: claim N, M marks each. The option is the
    scheme's whole response — heading AND the sentence explaining it — because
    "Outline" is what the marks are for and the heading alone would teach a
    student to write a bare list.
  * A part whose marks are for a DIAGRAM is carded for its written explanation
    only, and says so on the card. The Mark Bank cannot mark a drawing.
  * Section A is not carded here. Its answers are one or two words keyed to an
    infographic printed on the paper, so they need the figure pipeline.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, card, defurnish, emit, heads, load, point, tidy  # noqa: E402

YEAR, LEVEL = 2024, 'higher'
T = tidy(load(YEAR, LEVEL))

# The scheme prints its answers once and the appended table cells repeat them, so
# the body is bounded to the first pass; an anchor found twice would otherwise be
# ambiguous for reasons that have nothing to do with the paper.
BODY = block(T, 'Question 11 Possible Responses Marks', 'Student Research Project')


def opts(chunk, headings):
    """The scheme's named responses, each with the sentence that explains it."""
    return [defurnish(h) for h in heads(chunk, headings)]


cards = []

# ── Question 11 ─────────────────────────────────────────────────────────────
q11c = block(BODY, '(iii) Outline one possible disadvantage of increasing tourism',
             '(b) (i) It has been estimated')
cards.append(card(
    'econ-2024-hl-q11-a-iii', YEAR, LEVEL, 'economics-4-1', 'disadvantages-of-tourism',
    '2024 HL Q11(a)(iii)',
    'Outline one possible disadvantage of increasing tourism numbers in the Irish economy.',
    '1 @ 6', 6,
    [anyN('r-1', 'A disadvantage of rising tourism numbers — any one', 6, 1, 6,
          opts(q11c, ['Increased pressure on infrastructure', 'Increased prices',
                      'Increased pressure to secure workers', 'Possible damage to the environment',
                      'Increased littering']),
          'One disadvantage, 6 marks. The scheme wants the point AND the explanation of it — '
          'naming the disadvantage without saying why is not what the marks are for.')],
    'Set on a chart of foreign tourist arrivals in July 2021 and August 2023, but the part itself '
    'does not need the chart: it asks for a disadvantage of rising tourism in general.'))

q11b3 = block(BODY, '(iii) Outline two uses of the information provided by national income statistics',
              '(c) Assume the market for brand of organic ice cream')
cards.append(card(
    'econ-2024-hl-q11-b-iii', YEAR, LEVEL, 'economics-3-0', 'uses-of-national-income-statistics',
    '2024 HL Q11(b)(iii)',
    'Outline two uses of the information provided by national income statistics.',
    '2 @ 4', 8,
    [anyN('r-1', 'A use of national income statistics — any two', 8, 2, 4,
          opts(q11b3, ['Indication of alterations to our standard of living',
                       'A way of comparing the standard of living in different countries',
                       'Help determine EU budget contributions',
                       'Formulating economic policy', 'Evaluating economic policy',
                       'Effective research']),
          'Two uses, 4 marks each. Each is the use and what it is used FOR; the scheme pairs them.')],
    ''))

# ── Question 14 ─────────────────────────────────────────────────────────────
q14a = block(BODY, 'Outline three characteristics (other than many sellers)',
             '(ii) Firms operating under monopolistic competition waste resources')
cards.append(card(
    'econ-2024-hl-q14-a-i', YEAR, LEVEL, 'economics-2-0', 'monopolistic-competition-characteristics',
    '2024 HL Q14(a)(i)',
    'Outline three characteristics (other than many sellers) of a firm operating in '
    'monopolistic competition.',
    '3 @ 5', 15,
    [anyN('r-1', 'A characteristic of monopolistic competition — any three', 15, 3, 5,
          opts(q14a, ['There are many buyers', 'Each firm seeks to maximise profits',
                      'Freedom of entry and exit', 'Reasonable knowledge regarding profits',
                      'Product differentiation exists']),
          'Three characteristics, 5 marks each. "Many sellers" is excluded by the question — the '
          'scheme lists five others, all set in the restaurant market the question describes.')],
    'Set in the Irish restaurant market, given as the example of monopolistic competition.'))

q14b2 = block(BODY, '(ii) Outline one possible economic advantage to consumers of monopolistic',
              'The President of the European Central Bank')
cards.append(card(
    'econ-2024-hl-q14-b-ii', YEAR, LEVEL, 'economics-2-0', 'monopolistic-competition-consumer-advantage',
    '2024 HL Q14(b)(ii)',
    'Outline one possible economic advantage to consumers of monopolistic competitive markets.',
    '1 @ 5', 5,
    [anyN('r-1', 'An advantage to consumers — any one', 5, 1, 5,
          opts(q14b2, ['Consumers benefit from increased choice', 'Access to information',
                       'Normal profit', 'Increased quality of services']),
          'One advantage, 5 marks.')],
    ''))

emit(cards)
