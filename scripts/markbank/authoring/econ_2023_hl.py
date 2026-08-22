#!/usr/bin/env python3
"""Economics 2023 Higher Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for. This
paper writes its descending tariffs in words ("1st @ 5", "2nd @ 4"), which is
the Ordinary style — the two are not a level split.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2023, 'higher')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Deduct 1m', 'The Research Process')

P.menu('factors which are likely to have influenced this trend in the Irish population',
       'econ-2023-hl-q11-a-ii', 'economics-3-5', 'drivers-of-population-growth',
       'Explain two factors which are likely to have influenced this trend in the Irish '
       'population.',
       'A factor behind the population trend — any two',
       'Two factors, 5 marks each.',
       drop=SCAFFOLD)

P.menu('factors that influence the geographical mobility of labour', 'econ-2023-hl-q11-b-ii',
       'economics-2-1', 'geographical-mobility-of-labour',
       'Explain two factors that influence the geographical mobility of labour.',
       'A factor affecting geographical mobility — any two',
       'Two factors, the first paid 5 and the second 4.',
       drop=SCAFFOLD)

P.menu('ways the government can possibly increase geographical mobility', 'econ-2023-hl-q11-b-iii',
       'economics-2-1', 'increasing-mobility-of-labour',
       'Explain two ways the government can possibly increase geographical mobility of labour.',
       'A way to increase mobility of labour — any two',
       'Two ways, the first paid 5 and the second 4.',
       drop=SCAFFOLD)

P.menu('Despite Ireland’s high HDI ranking', 'econ-2023-hl-q11-c-ii',
       'economics-3-1', 'policies-to-address-inequality',
       'Despite Ireland’s high HDI ranking, inequalities still exist. Outline two economic '
       'policies the Irish Government could consider to address inequality. Justify your answers.',
       'A policy to address inequality — any two',
       'Two policies, the first paid 5 and the second 4. The marks are for the justification as '
       'much as the policy.',
       drop=SCAFFOLD + ('Outline two economic pol',))

P.menu('above were introduced, outline two possible economic disadvantages', 'econ-2023-hl-q11-c-iii',
       'economics-3-1', 'disadvantages-of-inequality-policies',
       'If the policies you suggested above were introduced, outline two possible economic '
       'disadvantages of their implementation.',
       'A disadvantage of those policies — any two',
       'Two disadvantages, the first paid 5 and the second 4. Each answers one of the policies '
       'from part (ii), so the two parts are marked as a pair.',
       drop=SCAFFOLD + ('college and universities',))

P.menu('Identify three characteristics of a perfectly competitive market', 'econ-2023-hl-q12-a-i',
       'economics-2-0', 'perfect-competition-characteristics',
       'Identify three characteristics of a perfectly competitive market.',
       'A characteristic of perfect competition — any three',
       'Three characteristics, 4 marks each.',
       drop=SCAFFOLD)

P.menu('Explain the terms injections and leakages', 'econ-2023-hl-q13-a-ii',
       'economics-3-0', 'injections-and-leakages',
       'Explain the terms injections and leakages, and refer to two examples of each.',
       'The two terms — both of them',
       'Both terms, and the scheme prints two examples of each. The question names them, so this '
       'is not a choice.',
       drop=SCAFFOLD)

P.menu('Some citizens engage in activities in the hidden economy', 'econ-2023-hl-q13-a-iii',
       'economics-3-1', 'effects-of-the-hidden-economy-hl',
       'Some citizens engage in activities in the hidden economy in Ireland. Outline two effects '
       'on the Irish economy.',
       'An effect of the hidden economy — any two',
       'Two effects, 4 marks each.',
       drop=SCAFFOLD)

P.menu('risks associated with over-reliance on MNCs', 'econ-2023-hl-q13-b-i',
       'economics-4-1', 'risks-of-over-reliance-on-mncs',
       'Outline two risks associated with over-reliance on MNCs for Ireland’s tax revenue.',
       'A risk of over-reliance on MNCs — any two',
       'Two risks, the first paid 7 and the second 5.',
       drop=SCAFFOLD + ('which is hugely volatile',))

P.menu('factors that are currently impacting on Ireland’s international competitiveness',
       'econ-2023-hl-q13-b-ii', 'economics-4-2', 'factors-affecting-competitiveness',
       'Discuss two factors that are currently impacting on Ireland’s international '
       'competitiveness.',
       'A factor affecting competitiveness — any two',
       'Two factors, 4 marks each.',
       drop=SCAFFOLD + ('insurance), these tend t',))

P.menu('Describe two types of unemployment', 'econ-2023-hl-q14-a-iii',
       'economics-3-2', 'types-of-unemployment',
       'Describe two types of unemployment, giving examples to support your answer.',
       'A type of unemployment — any two',
       'Two types, 7 marks each. Structural unemployment is given in the question, so the scheme '
       'lists the others.',
       drop=SCAFFOLD + ('of the year. E.g. a pers',))

P.menu('Maintaining full employment is an objective of the government', 'econ-2023-hl-q14-b-ii',
       'economics-3-1', 'government-economic-objectives',
       'Maintaining full employment is an objective of the government. Outline two other current '
       'economic objectives of the Irish government.',
       'An economic objective — any two',
       'Two objectives, 4 marks each. Full employment is excluded by the question.',
       drop=SCAFFOLD)

P.menu('Pandemic Unemployment Payment (PUP)', 'econ-2023-hl-q14-b-iii',
       'economics-3-0', 'the-multiplier-and-the-pup',
       'The Irish government spent €8.8bn on the Pandemic Unemployment Payment in 2021. Use the '
       'multiplier to explain the effect of this expenditure on the Irish economy.',
       'A step in the multiplier effect — any three',
       'Three points, 4 marks each. The scheme walks the money round the circular flow, so the '
       'points are a sequence rather than alternatives.',
       drop=SCAFFOLD + ('citizens received money',))

P.menu('countries are now favouring a return to trade protection', 'econ-2023-hl-q15-b-ii',
       'economics-4-2', 'reasons-for-trade-protection',
       'Some countries are now favouring a return to trade protection measures. Discuss two '
       'economic reasons for this.',
       'A reason for trade protection — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD + ('produced goods. This wil',))

P.menu('possible disadvantages of trade protection', 'econ-2023-hl-q15-b-iii',
       'economics-4-2', 'disadvantages-of-trade-protection',
       'Outline two possible disadvantages of trade protection.',
       'A disadvantage of trade protection — any two',
       'Two disadvantages, 4 marks each.',
       drop=SCAFFOLD + ('market because of limita',))

P.menu('Circular Economy and Miscellaneous Provisions Act 2022', 'econ-2023-hl-q16-b-ii',
       'economics-0-2', 'moving-to-a-circular-economy',
       'Outline two changes required if Ireland is to move to a circular economy.',
       'A change the circular economy requires — any two',
       'Two changes, 4 marks each.',
       drop=SCAFFOLD + ('acknowledge/unaware of t',))

P.menu('households in Ireland are responsible for 117 kg of food waste', 'econ-2023-hl-q16-b-iii',
       'economics-0-2', 'reducing-household-food-waste',
       'Outline two measures that could be taken to reduce household food waste in Ireland.',
       'A measure to reduce food waste — any two',
       'Two measures, the first paid 6 and the second 4.',
       drop=SCAFFOLD + ('widespread public awaren',))

P.menu('market for Irish milk can no longer be considered', 'econ-2023-hl-q12-a-ii',
       'economics-2-0', 'irish-milk-not-perfectly-competitive',
       'Identify one reason why the market for Irish milk can no longer be considered perfectly '
       'competitive.',
       'A reason the milk market is not perfectly competitive — any one',
       'One reason, 4 marks.',
       claim=1, per=4, drop=SCAFFOLD)

P.emit()
