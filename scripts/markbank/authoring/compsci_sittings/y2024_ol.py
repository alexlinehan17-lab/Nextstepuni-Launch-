"""Computer Science 2024 Ordinary Level: the 3 printed asks the bank did not hold.

41 of the sitting's 44 asks are covered by the cards shipped in August; these
3 complete it. Paper pages 5, 8 and 12-13 and scheme pages 5, 8 and 10 were
opened.
"""
from compsci_lane import (P, S, anyn, crit, crop, pt, stack)  # noqa: F401

CROPS = {
    'q5-flow': stack([('038', 5, (56, 160, 560, 488)), ('038', 5, (55, 560, 508, 743))],
                     ref='2024 OL Q5',
                     alt='Figure 1: a flowchart. START, price = 20.00, Input age, Input student '
                         '(Yes/No), then a decision Is age < 16?; Yes leads to an empty box B and '
                         'on to an empty box D; No leads to an empty box A, whose Yes branch goes '
                         'through an empty box C to D and whose No branch goes straight to D. '
                         'Below it, the table '
                         'whose Column A lists PRINT(price), Is age < 21 AND student = "yes"?, '
                         'price = price – (20% of price) and price = price – (10% of price), and '
                         'whose Column B (Flowchart Letter) is blank.'),
    'q11-fig2': crop('038', 8, (284, 489, 541, 596), ref='2024 OL Q11',
                     alt='Figure 2: photographs of two single-board computers, a Raspberry Pi '
                         'and a micro:bit.'),
}

CARDS = [
    dict(key=(5, None, None), topic='cs-2-2', qfigure='q5-flow', total=6,
         why='p5: match four statements to the flowchart\'s letters; the scheme prints them, 4 '
             'correct 6, 3 correct 5, 2 correct 3, 1 correct 2',
         ask=[P(5, 'There are three different ticket prices', 'some information missing.'),
              P(5, 'Select the appropriate letter from the flowchart', 'the correct statement in Column A.')],
         rows=[anyn([S(5, 'PRINT(price) D'), S(5, 'Is age < 21 AND student = “yes”? A'),
                     S(5, 'price = price – (20% of price) B'), S(5, 'price = price – (10% of price) C')],
                    4, 2, steps=[2, 1, 2, 1], head=S(5, 'Flowchart Symbol Description Flowchart Place'),
                    note=S(5, '4 correct – 6 marks', '1 correct – 2 mark'))]),
    dict(key=(11, None, None), topic='cs-2-3', qfigure='q11-fig2', total=6,
         why='p8: one digital and one analogue input; the scheme lists both, each 3 / 2',
         ask=P(8, 'Provide one example of a digital input and one example of an analogue input',
               'such as those shown in Figure 2.'),
         rows=[anyn([S(8, 'Button'), S(8, 'On/ Off Switch'), S(8, 'Shake'), S(8, 'Pins'),
                     S(8, 'Accept any relevant digital input')], 1, 3, head=S(8, 'Digital Inputs:'),
                    open_list=True, note=S(8, 'For each (digital/analogue):', 'Fair example 2 marks')),
               anyn([S(8, 'Accelerometer'), S(8, 'Magnetometer'), S(8, 'Temperature Sensor'),
                     S(8, 'Light Sensor'), S(8, 'Moisture Sensor'), S(8, 'Sound Sensor'),
                     S(8, 'Pressure Sensor'), S(8, 'Distance Sensor'),
                     S(8, 'Accept any relevant analogue input')], 1, 3, head=S(8, 'Analogue Inputs:'),
                    open_list=True, note=S(8, 'For each (digital/analogue):', 'Fair example 2 marks'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-2-2', total=6,
         why='p13: one disadvantage of linear search on large data; the scheme answers it, 6 / 4',
         stem=P(12, 'The bottles are numbered and are stored electronically in a list.', '19 67 31'),
         ask=P(13, 'Explain one disadvantage of the linear search algorithm', 'large data sets.'),
         rows=[crit(S(10, 'The linear search might have to check every item', 'take a lot more time.'), 6, [4],
                    note=S(10, 'Good description – clear understanding demonstrated 6 marks',
                           'Fair description – limited understanding 4 marks'))]),
]
