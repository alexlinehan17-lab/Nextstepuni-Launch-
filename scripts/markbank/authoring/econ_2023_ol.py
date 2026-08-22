#!/usr/bin/env python3
"""Economics 2023 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import card, point  # noqa: E402

P = Paper(2023, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('hair and beauty industries are an', 'econ-2023-ol-q11-a-i',
       'economics-2-0', 'monopolistic-competition-identified',
       'Outline two reasons why, in your opinion, the hair and beauty industries are an example '
       'of monopolistic competition.',
       'A reason it is monopolistic competition — any two',
       'Two reasons, the first paid 6 and the second 4.',
       drop=SCAFFOLD + ('example of monopolistic',))

P.menu('advantages for consumers of monopolistic competition', 'econ-2023-ol-q11-a-ii',
       'economics-2-0', 'monopolistic-competition-consumer-advantages',
       'Outline two advantages for consumers of monopolistic competition.',
       'An advantage to consumers — any two',
       'Two advantages, the first paid 6 and the second 4.',
       drop=SCAFFOLD)

P.menu('one effect the hidden economy in the hair and beauty industry', 'econ-2023-ol-q11-c-ii',
       'economics-3-1', 'effects-of-the-hidden-economy-ol',
       'Outline one effect the hidden economy in the hair and beauty industry has on businesses '
       'in this industry and on the Irish Government.',
       'An effect of the hidden economy — any two',
       'The paper pays 6 for the effect on business and 4 for the effect on government; the '
       'scheme lists the business effects first.',
       drop=SCAFFOLD + ('businesses in this indus',))

P.menu('other principles of a good tax system', 'econ-2023-ol-q12-b-ii',
       'economics-3-1', 'principles-of-a-good-tax-system',
       'Explain two other principles of a good tax system that you would consider important in '
       'the current economic climate.',
       'A principle of a good tax system — any two',
       'Two principles, the first paid 8 and the second 4. Equity — ability to pay — is excluded '
       'by the question.',
       drop=SCAFFOLD + ('in the current economic',))

P.menu('actions an Irish household could take to reduce their electricity', 'econ-2023-ol-q12-c-ii',
       'economics-0-2', 'household-actions-to-cut-electricity-use',
       'Describe two actions an Irish household could take to reduce their electricity bills and '
       'make them more sustainable.',
       'An action the household could take — any two',
       'Two actions, the first paid 10 and the second 4.',
       drop=SCAFFOLD + ('make them more sustainab',))

P.menu('advantages of exports for the Irish economy', 'econ-2023-ol-q13-a-ii',
       'economics-4-2', 'advantages-of-exports',
       'Describe two advantages of exports for the Irish economy.',
       'An advantage of exports — any two',
       'Two advantages, the first paid 8 and the second 2.',
       drop=SCAFFOLD)

P.menu('ways the Irish government may influence consumers to switch to electric',
       'econ-2023-ol-q15-a-i', 'economics-1-3', 'encouraging-electric-vehicles',
       'Outline two ways the Irish government may influence consumers to switch to electric '
       'vehicles.',
       'A way to encourage electric vehicles — any two',
       'Two ways, the first paid 8 and the second 4.',
       drop=SCAFFOLD)

P.menu('Explain any two of the above terms', 'econ-2023-ol-q16-a-i',
       'economics-0-1', 'properties-of-an-economic-good',
       'Explain any two of the following terms: scarce; transferable; utility.',
       'One of the three terms — any two',
       'Two terms, 7 marks each. The scheme explains each against the same example, a bag of '
       'crisps.',
       drop=SCAFFOLD)

P.menu('benefit of this electricity credit', 'econ-2023-ol-q12-c-i',
       'economics-1-3', 'benefit-of-the-electricity-credit',
       'Outline one benefit of the €600 electricity credit to the Irish household.',
       'A benefit to the household — any one',
       'One benefit, 10 marks.',
       claim=1, per=10, drop=SCAFFOLD)


# ── A figure card ───────────────────────────────────────────────────────────
P.cards.append(card(
    'econ-2023-ol-q11-b-i', 2023, 'ordinary', 'economics-2-0',
    'labelling-monopolistic-competition', '2023 OL Q11(b)(i)',
    'The diagram represents the long run equilibrium of a firm in the hair and beauty industry. '
    'Write out in full what each of the three numbered items represents.',
    'fixed', 24,
    [point('r-1', 'AVERAGE COST', 8, 'Item 1 — the blue U-shaped curve, whose minimum is point W.'),
     point('r-2', 'AVERAGE REVENUE / DEMAND', 8, 'Item 2 — the yellow line falling to the right.'),
     point('r-3', 'QUANTITY', 8, 'Item 3 — the horizontal axis. MC and MR are already labelled.')],
    'Abbreviations are not accepted.', tariff_kind='fixed',
    figure_key='economics-2023-OL-paper-p11-art',
    label_key=[{'letter': '1', 'meaning': 'AVERAGE COST', 'askedInThisQuestion': True},
               {'letter': '2', 'meaning': 'AVERAGE REVENUE / DEMAND', 'askedInThisQuestion': True},
               {'letter': '3', 'meaning': 'QUANTITY', 'askedInThisQuestion': True},
               {'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': False},
               {'letter': 'MR', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': False}]))

P.emit()
