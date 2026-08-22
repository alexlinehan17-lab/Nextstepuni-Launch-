#!/usr/bin/env python3
"""Economics 2025 Higher Level — Section B.

Same rules as econ_2024_hl.py. `econ_scout.py 2025 higher` lists every mark cell
with the question text before it, which is the unit each of these was made from.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, card, defurnish, emit, heads, load, tidy  # noqa: E402

YEAR, LEVEL = 2025, 'higher'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'Question 11 Possible Responses Max Mark', 'Student Research Project', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, headings, note, notes='', steps=None, stem=''):
    chunk = block(BODY, start, end)
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      [defurnish(h) for h in heads(chunk, headings)], note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    # ── Question 11 — market structures ─────────────────────────────────────
    menu('econ-2025-hl-q11-a-ii', 'economics-2-0', 'effects-of-new-market-entrant',
         '2025 HL Q11(a)(ii)',
         'With the entry of this new firm into the Irish health insurance market, outline two '
         'potential economic effects on the existing firms in the industry.',
         '2 @ 7', 14, 'An effect on the existing firms — any two', 2, 7,
         'Increased competition and lower prices', '(b) (i) A patent gives a pharmaceutical',
         ['Increased competition and lower prices', 'Improved services and innovation',
          'Market share redistribution', 'Pressure on profit margins',
          'Regulatory and market responses', 'Potential for mergers or exits',
          'Increased consumer choice / Market Expansion',
          'Potential for a price war / short-term instability', 'Impact on the labour market'],
         'Two effects, 7 marks each. The scheme lists gains and losses together — a new entrant '
         'is not simply bad news for the incumbents.',
         stem='Level Health, a new health insurance provider, entered the Irish market in '
              'November 2024. Three firms already held 97% of it.'),

    menu('econ-2025-hl-q11-b-ii', 'economics-2-0', 'barriers-to-entry-in-monopoly',
         '2025 HL Q11(b)(ii)',
         'Outline one barrier to entry often found in monopoly markets, other than a patent.',
         '1 @ 4', 4, 'A barrier to entry — any one', 1, 4,
         'Government-legislated monopolies', '(iii) Outline one economic advantage and one economic',
         ['Government-legislated monopolies', 'Collusion and trade agreements',
          'Exclusive ownership of raw materials', 'High capital requirements / Economies of scale',
          'Mergers and acquisitions', 'Intimidation and unfair practices'],
         'One barrier, 4 marks. Patents are excluded by the question.'),

    menu('econ-2025-hl-q11-c-i', 'economics-2-1', 'effects-of-a-gp-shortage', '2025 HL Q11(c)(i)',
         'Outline two possible effects that the above development may have on existing / '
         'potential patients.',
         '2 @ 4', 8, 'An effect on patients — any two', 2, 4,
         'Longer waiting times – with fewer GPs available',
         '(ii) Suggest one economic measure the Irish government could take',
         ['Longer waiting times', 'Overcrowded GP practices', 'Increased pressure on hospitals',
          'Higher costs for private care', 'Health risks due to delayed care',
          'Increased health inequality'],
         'Two effects, 4 marks each.',
         stem='Around 700 GPs are due to retire in the next five years.'),

    # ── Question 13 — international economics ───────────────────────────────
    menu('econ-2025-hl-q13-b-ii', 'economics-4-2', 'sources-of-comparative-advantage',
         '2025 HL Q13(b)(ii)',
         'Outline two sources of comparative advantage in Ireland, which help to attract foreign '
         'direct investment from pharmaceutical companies.',
         '2 @ 6', 12, 'A source of Ireland’s comparative advantage — any two', 2, 6,
         'Reputation / Track record – Ireland has long established itself',
         '(iii)',
         ['Reputation / Track record', 'R&D / innovation supports', 'Pharmaceutical ‘cluster',
          'Highly skilled workforce', 'open economy', 'Low corporate tax rate',
          'Proximity to the EU market'],
         'Two sources, 6 marks each.'),

    # ── Question 14 — the consumer and the firm ─────────────────────────────
    menu('econ-2025-hl-q14-a-i', 'economics-1-1', 'benefits-of-online-shopping',
         '2025 HL Q14(a)(i)',
         'Outline two benefits of online shopping for consumers in Ireland, other than being able '
         'to choose from a wider selection of products.',
         '2 @ 5', 10, 'A benefit of online shopping — any two', 2, 5,
         'Increased convenience / accessibility / efficiency',
         '(ii) Amazon plans to open a dedicated store',
         ['Increased convenience / accessibility / efficiency', 'Cheaper prices / Discounts',
          'Home delivery / Subscription services',
          'Access to reviews / Better informed decisions', 'Flexible payments', 'Easy returns',
          'Less impulse buying', 'Environmental benefits'],
         'Two benefits, 5 marks each. Wider selection is excluded by the question.'),
]

emit(cards)
