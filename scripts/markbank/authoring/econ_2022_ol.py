#!/usr/bin/env python3
"""Economics 2022 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2022, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Minimum Unit Price for A')

P.menu('advantages for consumers of many firms providing streaming', 'econ-2022-ol-q11-a-ii',
       'economics-2-0', 'advantages-of-many-firms-for-consumers',
       'Outline two advantages for consumers of many firms providing streaming services in this '
       'market.',
       'An advantage to consumers — any two',
       'Two advantages, the first paid 8 and the second 4.',
       claim=2, per=8, steps=[8, 4], drop=SCAFFOLD,
       stem='Set on a chart of US streaming services by number of users — YouTube highest, '
            'Vimeo lowest.')

P.menu('Firms who may wish to enter a monopoly industry face barriers', 'econ-2022-ol-q11-c-ii',
       'economics-2-0', 'barriers-to-entry',
       'Firms who may wish to enter a monopoly industry face barriers to entry. Outline two '
       'possible barriers to entry.',
       'A barrier to entry — any two',
       'Two barriers, 4 marks each.',
       drop=SCAFFOLD)

P.menu('two ways that a business could be more sustainable', 'econ-2022-ol-q12-c-ii',
       'economics-0-2', 'ways-a-business-can-be-sustainable',
       'Suggest two ways that a business could be more sustainable.',
       'A way to be more sustainable — any two',
       'Two ways, 7 marks each.',
       drop=SCAFFOLD)

P.menu('features/characteristics of a less developed nation', 'econ-2022-ol-q13-a-i',
       'economics-4-0', 'features-of-a-less-developed-nation',
       'Outline two features/characteristics of a less developed nation.',
       'A feature of a less developed nation — any two',
       'Two features, 8 marks each.',
       drop=SCAFFOLD)

P.menu('reasons why the Irish government gives aid', 'econ-2022-ol-q13-a-ii',
       'economics-4-0', 'why-ireland-gives-aid',
       'Outline two reasons why the Irish government gives aid to less developed nations.',
       'A reason Ireland gives aid — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD)

P.menu('reasons why TikTok would locate in Ireland', 'econ-2022-ol-q14-a-ii',
       'economics-4-1', 'why-mncs-locate-in-ireland-ol',
       'Outline two reasons why TikTok would locate in Ireland.',
       'A reason an MNC locates in Ireland — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD)

P.menu('economic benefits to the local community of a Multi-National', 'econ-2022-ol-q14-a-iii',
       'economics-4-1', 'local-benefits-of-an-mnc',
       'Describe two possible economic benefits to the local community of a Multi-National '
       'Company locating there.',
       'A benefit to the local community — any two',
       'Two benefits, 4 marks each.',
       drop=SCAFFOLD)

P.menu('benefits to the Irish economy of exporting', 'econ-2022-ol-q14-b-ii',
       'economics-4-2', 'benefits-of-exporting',
       'Outline two benefits to the Irish economy of exporting to other countries.',
       'A benefit of exporting — any two',
       'Two benefits, 8 marks each.',
       drop=SCAFFOLD, cap=5)

P.menu('reasons why the government introduced minimum pricing', 'econ-2022-ol-q15-a-i',
       'economics-1-3', 'minimum-pricing-on-alcohol',
       'Outline two reasons why the government introduced minimum pricing on alcohol.',
       'A reason for minimum pricing — any two',
       'Two reasons, 6 marks each.',
       drop=SCAFFOLD)

P.menu('one social benefit and one private benefit of the government increasing the tax on cigaret',
       'econ-2022-ol-q15-a-iii-social', 'economics-2-2', 'social-benefits-of-cigarette-tax',
       'Outline one social benefit of the government increasing the tax on cigarettes.',
       'A social benefit — any one',
       'One social benefit, 4 marks; the paper pays a private benefit at 4 as well.',
       ref='2022 OL Q15(a)(iii) — social benefit',
       claim=1, per=4, drop=SCAFFOLD, stop='Private Benefits',
       notes='The scheme heads the social benefits and the private benefits separately, and the '
             'question wants one of each, so each side is its own card.')

P.menu('one social benefit and one private benefit of the government increasing the tax on cigaret',
       'econ-2022-ol-q15-a-iii-private', 'economics-2-2', 'private-benefits-of-cigarette-tax',
       'Outline one private benefit of the government increasing the tax on cigarettes.',
       'A private benefit — any one',
       'One private benefit, 4 marks.',
       ref='2022 OL Q15(a)(iii) — private benefit',
       claim=1, per=4,
       drop=SCAFFOLD + ('Greater productivity', 'Reduction in cancer', 'Reduced pressure on hosp',
                        'Population healthier', 'Improved environment', 'Private Benefits'))

P.menu('economic effects which this rate of price inflation may have', 'econ-2022-ol-q16-a-ii',
       'economics-3-3', 'effects-of-inflation-on-citizens',
       'Discuss two economic effects which this rate of price inflation may have on Irish '
       'citizens.',
       'An effect on citizens — any two',
       'Two effects, 8 marks each.',
       drop=SCAFFOLD)

P.menu('governments can intervene in the market', 'econ-2022-ol-q11-c-iii',
       'economics-1-3', 'government-intervention-dominant-firm',
       'Suggest one way governments can intervene in the market if one firm becomes too dominant.',
       'A way government can intervene — either one',
       'One way, 4 marks. The scheme names two: regulate the firm, or legislate against the '
       'behaviour.',
       claim=1, per=4, drop=SCAFFOLD)

P.emit()
