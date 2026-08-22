#!/usr/bin/env python3
"""Economics 2021 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.

Two parts here answer a question about two DIFFERENT subjects under one heading
— one economic effect of Brexit on the consumer and on the firm, one benefit of
perfect competition to the consumer and to society — and the scheme lists both
sets together. Each side is carded on its own, which is the rule for parallel
accounts, so a student picking "one effect on the consumer" is not offered the
firm's.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2021, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Evidence of Data', 'Deduct')

P.menu('reasons why MNC’s locate in Ireland', 'econ-2021-ol-q11-b-iii',
       'economics-4-1', 'why-mncs-locate-in-ireland',
       'Outline two reasons why multinational companies locate in Ireland.',
       'A reason MNCs locate in Ireland — any two',
       'Two reasons, 7 marks each, split 3 for the reason and 4 for developing it.',
       drop=SCAFFOLD)

P.menu('outdoor flower market in Stoneybatter', 'econ-2021-ol-q12-b',
       'economics-2-0', 'assumptions-of-perfect-competition',
       'This firm operates in perfect competition where there are many homogeneous products. '
       'Discuss three main assumptions of this type of market structure.',
       'An assumption of perfect competition — any three',
       'Three assumptions, 5 marks each.',
       claim=3, per=5, drop=SCAFFOLD,
       stem='Set on a photograph of the outdoor flower market in Stoneybatter, Dublin, given as '
            'an example of perfect competition.')

P.menu('impact the introduction of a new mortgage lender', 'econ-2021-ol-q13-b-i',
       'economics-3-4', 'effect-of-a-new-mortgage-lender',
       'Outline the impact the introduction of a new mortgage lender in Ireland will have on '
       'consumers applying for a mortgage and on interest rates.',
       'An impact of a new lender — either one',
       'The scheme answers this in two halves — what it does for the borrower, and what it does '
       'to the rate — and pays 7 for each.',
       claim=2, per=7, drop=SCAFFOLD)

P.menu('one measure the Irish government could use to achieve', 'econ-2021-ol-q13-c-ii',
       'economics-0-2', 'measures-for-sustainable-objectives',
       'Outline one measure the Irish government could use to achieve its objectives on care for '
       'the environment and sustainable development.',
       'A measure the government could take — any one',
       'One measure, 8 marks.',
       claim=1, per=8, drop=SCAFFOLD)

P.menu('reasons why the Irish Government may intervene', 'econ-2021-ol-q13-c-iii',
       'economics-1-3', 'why-government-intervenes',
       'Outline two reasons why the Irish Government may intervene in an economy.',
       'A reason for government intervention — any two',
       'Two reasons, 5 marks each.',
       drop=SCAFFOLD)

P.menu('one social benefit and one economic benefit resulting from the introduction of the sugar tax',
       'econ-2021-ol-q14-a-i', 'economics-2-2', 'benefits-of-the-sugar-tax',
       'Explain one social benefit and one economic benefit resulting from the introduction of '
       'the sugar tax in Ireland.',
       'A benefit of the sugar tax — any two',
       'Two benefits, 10 marks each. The scheme lists the social benefits first and the economic '
       'ones after, and the question wants one of each.',
       drop=SCAFFOLD)

P.menu('Discuss one economic effect Brexit will have on each of the following',
       'econ-2021-ol-q15-a-i', 'economics-4-2', 'effects-of-brexit-on-consumers-and-firms',
       'Discuss one economic effect Brexit will have on the Irish consumer and one on the Irish '
       'firm.',
       'An economic effect of Brexit — any two',
       'Two effects, 8 marks each. The scheme lists the consumer effects first and the firm '
       'effects after, and the question wants one of each.',
       drop=SCAFFOLD)

P.menu('Irish exports to the UK have grown by 16%', 'econ-2021-ol-q15-a-ii',
       'economics-4-2', 'benefits-of-exports-to-ireland',
       'Irish exports to the UK have grown by 16% despite the uncertainty surrounding Brexit. '
       'Outline one benefit of this for the Irish economy.',
       'A benefit of rising exports — any one',
       'One benefit, 8 marks.',
       # The scheme's list here runs straight into the next question with no
       # marker of any kind, so the tail is bounded by count: five named
       # benefits, then the examiner's data-evidence note.
       claim=1, per=8, drop=SCAFFOLD, cap=5)

P.menu('one advantage or one disadvantage of Globalisation', 'econ-2021-ol-q11-b-i-neg',
       'economics-4-1', 'disadvantages-of-globalisation',
       'Outline one disadvantage of globalisation.',
       'A disadvantage of globalisation — any one',
       'One disadvantage, 5 marks.',
       ref='2021 OL Q11(b)(i) — disadvantage',
       claim=1, per=5,
       drop=SCAFFOLD + ('Improvements in fair trade', 'New experiences',
                        'Improved government relations', 'Possible disadvantages'),
       notes='The part lets a student answer with EITHER an advantage or a disadvantage and the '
             'scheme heads the two lists separately, so each side is its own card.')

P.menu('one advantage or one disadvantage of Globalisation', 'econ-2021-ol-q11-b-i-pos',
       'economics-4-1', 'advantages-of-globalisation',
       'Outline one advantage of globalisation.',
       'An advantage of globalisation — any one',
       'One advantage, 5 marks.',
       ref='2021 OL Q11(b)(i) — advantage',
       claim=1, per=5, drop=SCAFFOLD, stop='Possible disadvantages')

P.emit()
