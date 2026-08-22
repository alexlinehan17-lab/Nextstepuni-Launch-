#!/usr/bin/env python3
"""Economics 2025 Higher Level — Section B.

Same rules as econ_2024_hl.py. `econ_scout.py 2025 higher` lists every mark cell
with the question text before it, which is the unit each of these was made from.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, as_option, block, card, defurnish, emit, heads, load, tidy  # noqa: E402

YEAR, LEVEL = 2025, 'higher'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'Question 11 Possible Responses Max Mark', 'Student Research Project', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, headings, note, notes='', steps=None, stem=''):
    chunk = block(BODY, start, end)
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      [as_option(h) for h in heads(chunk, headings)], note, steps=steps)],
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
         ['Reputation / Track record', 'R&D / innovation supports',
          'Pharmaceutical ‘cluster e ect’', 'Highly skilled workforce',
          'Low corporate tax rate', 'Proximity to the EU market', 'English-speaking nation',
          'Alignment with regulatory / quality standards', 'Political and economic stability'],
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

cards += [
    menu('econ-2025-hl-q14-a-ii', 'economics-2-0', 'amazon-expansion-and-small-retailers',
         '2025 HL Q14(a)(ii)',
         'Amazon plans to open a dedicated store in Ireland in 2025. Outline two economic '
         'difficulties which Amazon’s expansion may create for small and medium-sized retailers '
         'operating in Ireland.',
         '2 @ 5', 10, 'A difficulty for small and medium retailers — any two', 2, 5,
         'Increased competition –', '(b)',
         ['Increased competition', 'Squeezed profit margins', 'Erosion of customer loyalty',
          'Supply chain challenges', 'Community impact', 'Job losses in small businesses',
          'Negative impact on retail property market'],
         'Two difficulties, 5 marks each.'),

    menu('econ-2025-hl-q15-a-ii', 'economics-3-4', 'factors-affecting-credit-creation',
         '2025 HL Q15(a)(ii)',
         'Outline two factors which affect the amount of credit that Irish retail banks can create.',
         '2 @ 6', 12, 'A factor affecting credit creation — any two', 2, 6,
         'Future economic expectations – if retail banks are optimistic', '(b)',
         ['Future economic expectations', 'ECB changes in interest rates / monetary policy',
          'Competition within the retail banking sector', 'Central bank reserve ratios',
          'Ability of banks to raise capital'],
         'Two factors, 6 marks each.'),

    menu('econ-2025-hl-q15-b-ii', 'economics-2-1', 'property-prices-and-the-labour-market',
         '2025 HL Q15(b)(ii)',
         'Rising property prices are affecting the labour market in Ireland. Discuss two economic '
         'effects this may have on the Irish labour market.',
         '2 @ 6', 12, 'An effect on the labour market — any two', 2, 6,
         'Reduced geographical mobility of labour – geographical mobility', '(c)',
         ['Reduced geographical mobility of labour', 'Increased wage demands',
          'Skills shortages / Emigration', 'Impact on entrepreneurship and small businesses',
          'Greater reliance on remote working', 'Expansion of commuter belt',
          'Increase in informal employment –'],
         'Two effects, 6 marks each.'),

    menu('econ-2025-hl-q16-c', 'economics-0-0', 'importance-of-entrepreneurship',
         '2025 HL Q16(c)',
         'Discuss two reasons why entrepreneurship is important to the continued development of '
         'the Irish economy.',
         '2 @ 4', 8, 'A reason entrepreneurship matters — any two', 2, 4,
         'Creates employment – entrepreneurs employ people',
         None,   # the last carded part of the paper, so it runs to the end of the body
         ['Creates employment', 'Organises production', 'Determines what gets produced',
          'Encourages investment', 'Provides tax revenue', 'Creates income and wealth',
          'Supports regional development', 'Reduces a reliance on multinationals',
          'Improves standards of living', 'Encourages a culture of enterprise'],
         'Two reasons, 4 marks each.'),
]

emit(cards)
