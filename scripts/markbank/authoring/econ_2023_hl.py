#!/usr/bin/env python3
"""Economics 2023 Higher Level — Section B.

Same rules as econ_2024_hl.py. This paper writes its descending tariffs in words
("1st @ 5", "2nd @ 4") and bullets its responses, which is the Ordinary layout —
the two are not a level split, so the splitter is chosen per paper.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, bullets, card, emit, load, tidy  # noqa: E402

YEAR, LEVEL = 2023, 'higher'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'bour market should increase meaning increased tax revenue', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, note, notes='', steps=None, stem=''):
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      bullets(block(BODY, start, end)), note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    menu('econ-2023-hl-q11-b-ii', 'economics-2-1', 'geographical-mobility-of-labour',
         '2023 HL Q11(b)(ii)',
         'Explain two factors that influence the geographical mobility of labour.',
         '1st @ 5 + 2nd @ 4', 9, 'A factor affecting geographical mobility — any two', 2, 5,
         '• Housing: if there is affordable housing available',
         '(iii) Explain two ways the government can possibly increase geographical mobility',
         'Two factors. The paper pays the first 5 and the second 4.',
         steps=[5, 4]),

    menu('econ-2023-hl-q11-b-iii', 'economics-2-1', 'increasing-mobility-of-labour',
         '2023 HL Q11(b)(iii)',
         'Explain two ways the government can possibly increase geographical mobility of labour.',
         '1st @ 5 + 2nd @ 4', 9, 'A way to increase mobility of labour — any two', 2, 5,
         '• Financial incentives: to encourage firm to relocate', '(c)',
         'Two ways, the first paid 5 and the second 4.',
         steps=[5, 4]),

    menu('econ-2023-hl-q11-c-ii', 'economics-3-1', 'policies-to-address-inequality',
         '2023 HL Q11(c)(ii)',
         'Despite Ireland’s high HDI ranking, inequalities still exist. Outline two economic '
         'policies which the Irish Government could consider to address inequality in Ireland. '
         'Justify your answers.',
         '1st @ 5 + 2nd @ 4', 9, 'A policy to address inequality — any two', 2, 5,
         '• Invest in education: If the government abolished',
         '(iii) If the policies you suggested in (ii) above',
         'Two policies, the first paid 5 and the second 4. The marks are for the justification '
         'as much as the policy.',
         steps=[5, 4]),

    menu('econ-2023-hl-q11-c-iii', 'economics-3-1', 'disadvantages-of-inequality-policies',
         '2023 HL Q11(c)(iii)',
         'If the policies you suggested above were introduced, outline two possible economic '
         'disadvantages of the implementation of these policies.',
         '1st @ 5 + 2nd @ 4', 9, 'A disadvantage of those policies — any two', 2, 5,
         '• Education: abolishing fees could lead to too many people', 'Question 12',
         'Two disadvantages, the first paid 5 and the second 4. Each answers one of the policies '
         'from part (ii), so the two parts are marked as a pair.',
         steps=[5, 4]),

    menu('econ-2023-hl-q12-a-i', 'economics-2-0', 'perfect-competition-characteristics',
         '2023 HL Q12(a)(i)',
         'Outline three characteristics of a perfectly competitive market.',
         '3 @ 4', 12, 'A characteristic of perfect competition — any three', 3, 4,
         '• Large number of buyers. No individual buyer',
         '(ii) Identify one reason why the market for Irish milk',
         'Three characteristics, 4 marks each.'),

    menu('econ-2023-hl-q12-a-ii', 'economics-2-0', 'irish-milk-not-perfectly-competitive',
         '2023 HL Q12(a)(ii)',
         'Identify one reason why the market for Irish milk can no longer be considered '
         'perfectly competitive.',
         '1 @ 4', 4, 'A reason the milk market is not perfectly competitive — any one', 1, 4,
         '• There are some large sellers in the industry', '(b)',
         'One reason, 4 marks.'),
]

emit(cards)
