#!/usr/bin/env python3
"""Economics 2024 Ordinary Level — Section A.

100 marks over ten questions of twelve, eight of which are answered, with a
mark added for each of the first four answered correctly.

Not carded: the true/false and tick-the-box parts, and question 10, whose
responses the extractor could not separate from the Section B header printed
directly beneath them.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2024, 'ordinary', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('one reason why our oceans and seas are a valuable economic resource',
       'econ-2024-ol-sa-q1-i', 'economics-0-2', 'oceans-as-an-economic-resource',
       'Explain one reason why our oceans and seas are a valuable economic resource.',
       'A reason the oceans are valuable — any one',
       'One reason, 8 marks.',
       ref='2024 OL Section A Q1(i)', claim=1, per=8, drop=SCAFFOLD,
       stem='UN Sustainable Development Goal 14 is to conserve and sustainably use the oceans, '
            'seas and marine resources.')

P.menu('one way individuals can help protect this valuable resource', 'econ-2024-ol-sa-q1-ii',
       'economics-0-2', 'protecting-the-marine-environment',
       'Outline one way individuals can help protect the oceans and seas.',
       'A way an individual can help — any one',
       'One way, 4 marks.',
       ref='2024 OL Section A Q1(ii)', claim=1, per=4, drop=SCAFFOLD)

P.menu('Competitive advertising promotes the advantages of one firm', 'econ-2024-ol-sa-q3-b',
       'economics-2-0', 'when-advertising-does-not-help-consumers',
       'Competitive advertising promotes the advantages of one firm’s product over that of its '
       'competitors. Outline two reasons why competitive advertising may not always benefit the '
       'consumer.',
       'A reason advertising may not benefit the consumer — any two',
       'Two reasons, the first paid 8 and the second 4.',
       ref='2024 OL Section A Q3(b)', steps=[8, 4], drop=SCAFFOLD)

P.menu('do not contribute to a rainy', 'econ-2024-ol-sa-q4-a',
       'economics-1-1', 'why-households-are-not-saving',
       'Explain one reason why these families may not be saving.',
       'A reason a family is not saving — any one',
       'One reason, 12 marks.',
       ref='2024 OL Section A Q4(a)', claim=1, per=12, drop=SCAFFOLD,
       stem='47% of Irish families with young children do not contribute to a rainy-day savings '
            'fund.')

P.menu('measure financial institutions in Ireland could take to encourage citizens',
       'econ-2024-ol-sa-q4-b', 'economics-3-4', 'encouraging-households-to-save',
       'Outline one measure financial institutions in Ireland could take to encourage citizens '
       'in Ireland to save.',
       'A measure a bank could take — any one',
       'One measure, 12 marks.',
       ref='2024 OL Section A Q4(b)', claim=1, per=12, drop=SCAFFOLD)

P.menu('Deposit Return Scheme was introduced', 'econ-2024-ol-sa-q6',
       'economics-0-2', 'effects-of-the-deposit-return-scheme',
       'Outline two effects the Deposit Return Scheme may have on Irish consumers.',
       'An effect on consumers — any two',
       'Two effects, the first paid 8 and the second 4.',
       ref='2024 OL Section A Q6', steps=[8, 4], drop=SCAFFOLD,
       stem='Under the Deposit Return Scheme, introduced on 1 February 2024, a consumer pays a '
            'deposit on a drink container and gets it back when the container is returned.')

P.emit()
