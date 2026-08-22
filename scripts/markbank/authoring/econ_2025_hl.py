#!/usr/bin/env python3
"""Economics 2025 Higher Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2025, 'higher')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'More possible response',
            'Possible benefits:', 'Economic difficulties:')

P.menu('entry of this new firm into the Irish health insurance', 'econ-2025-hl-q11-a-ii',
       'economics-2-0', 'effects-of-new-market-entrant',
       'With the entry of this new firm into the Irish health insurance market, outline two '
       'potential economic effects on the existing firms in the industry.',
       'An effect on the existing firms — any two',
       'Two effects, 7 marks each. The scheme lists gains and losses together — a new entrant is '
       'not simply bad news for the incumbents.',
       drop=SCAFFOLD,
       stem='Level Health, a new health insurance provider, entered the Irish market in November '
            '2024. Three firms already held 97% of it.')

P.menu('effects that the above development may have on existing /', 'econ-2025-hl-q11-c-i',
       'economics-2-1', 'effects-of-a-gp-shortage',
       'Around 700 GPs are due to retire in the next five years. Outline two possible effects '
       'this may have on existing and potential patients.',
       'An effect on patients — any two',
       'Two effects, 4 marks each.',
       drop=SCAFFOLD)

P.menu('sources of comparative advantage in Ireland', 'econ-2025-hl-q13-b-ii',
       'economics-4-2', 'sources-of-comparative-advantage',
       'Outline two sources of comparative advantage in Ireland which help attract foreign '
       'direct investment from pharmaceutical companies.',
       'A source of Ireland’s comparative advantage — any two',
       'Two sources, 6 marks each.',
       drop=SCAFFOLD)

P.menu('benefits of online shopping for consumers', 'econ-2025-hl-q14-a-i',
       'economics-1-1', 'benefits-of-online-shopping',
       'Outline two benefits of online shopping for consumers in Ireland, other than being able '
       'to choose from a wider selection of products.',
       'A benefit of online shopping — any two',
       'Two benefits, 5 marks each. Wider selection is excluded by the question.',
       drop=SCAFFOLD)

P.menu('Amazon plans to open a dedicated store', 'econ-2025-hl-q14-a-ii',
       'economics-2-0', 'amazon-expansion-and-small-retailers',
       'Amazon plans to open a dedicated store in Ireland in 2025. Outline two economic '
       'difficulties this may create for small and medium-sized retailers in Ireland.',
       'A difficulty for small and medium retailers — any two',
       'Two difficulties, 5 marks each.',
       drop=SCAFFOLD)

P.menu('factors, which affect the amount of credit', 'econ-2025-hl-q15-a-ii',
       'economics-3-4', 'factors-affecting-credit-creation',
       'Outline two factors which affect the amount of credit that Irish retail banks can create.',
       'A factor affecting credit creation — any two',
       'Two factors, 6 marks each.',
       drop=SCAFFOLD)

P.menu('Rising property prices is affecting the labour market', 'econ-2025-hl-q15-b-ii',
       'economics-2-1', 'property-prices-and-the-labour-market',
       'Rising property prices are affecting the labour market in Ireland. Discuss two economic '
       'effects this may have on the Irish labour market.',
       'An effect on the labour market — any two',
       'Two effects, 6 marks each.',
       drop=SCAFFOLD)

P.menu('challenges for the Irish economy, if government expenditure on', 'econ-2025-hl-q15-c-ii',
       'economics-3-1', 'challenges-of-cutting-capital-spending',
       'Discuss two possible challenges for the Irish economy if government expenditure on '
       'capital projects were reduced.',
       'A challenge for the economy — any two',
       'Two challenges, 5 marks each.',
       drop=SCAFFOLD)

P.menu('levels of expenditure by the Irish government for the years', 'econ-2025-hl-q15-c-iii',
       'economics-3-1', 'why-government-spending-rose',
       'Explain two economic reasons for the significant increase in government expenditure over '
       'this period.',
       'A reason spending rose — any two',
       'Two reasons, 5 marks each.',
       drop=SCAFFOLD)

P.menu('objectives the owner of the smoothie and juice bar', 'econ-2025-hl-q16-a-iii',
       'economics-1-5', 'firm-objectives-other-than-profit',
       'Outline two objectives the owner of the smoothie and juice bar may pursue other than '
       'profit maximisation.',
       'An objective other than profit — any two',
       'Two objectives, 7 marks each.',
       drop=SCAFFOLD)

P.menu('economic measures the Irish government could implement to help reduce',
       'econ-2025-hl-q16-b-i', 'economics-1-3', 'supporting-small-business',
       'Outline two economic measures the Irish government could implement to help reduce the '
       'pressures facing small businesses.',
       'A measure to support small business — any two',
       'Two measures, 6 marks each.',
       drop=SCAFFOLD)

P.menu('Entrepreneurship is central to Ireland', 'econ-2025-hl-q16-c',
       'economics-0-0', 'importance-of-entrepreneurship',
       'Discuss two reasons why entrepreneurship is important to the continued development of '
       'the Irish economy.',
       'A reason entrepreneurship matters — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD + ('Higher Level Economics',), cap=10)

P.menu('barrier to entry often found in monopoly', 'econ-2025-hl-q11-b-ii',
       'economics-2-0', 'barriers-to-entry-in-monopoly',
       'Outline one barrier to entry often found in monopoly markets, other than a patent.',
       'A barrier to entry — any one',
       'One barrier, 4 marks. Patents are excluded by the question.',
       claim=1, per=4, drop=SCAFFOLD)

P.emit()
