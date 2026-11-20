#!/usr/bin/env python3
"""Reviewed specs for the Dutch classic examination (small-languages lane).

One entry per printed ask; see sl_lib.py for the selector language. Line
numbers are lines of examiner-reports/dutch/schemes/<year>-hl.md.
"""
from sl_lib import (R, S, J, L, PL, QP, Run, pre, prerun, PP, SP, PY, RX, PARTP, one, shown, graded, crit,  # noqa: F401
                    examples, quote, unprinted, part, NoScheme)


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)

SPECS = {}

# ================================================================ 2010 HL ===
# Paper p4 heads Deel 1 a second time over its questions (the first head stands
# over the numbered passage). Deel 1 prices each expression "(1 punt)" and
# Questions 2-6 "(5 punten)"; the scheme splits Question 2 "2 / 2 / 1 punten".
# Deel 2 and Deel 3 share the four criteria printed at the scheme's end (p3).
CRIT_2010 = crit(58, (59, 60), (61, 62), 63)
SPECS[2010] = [
    R('I1a', [one(S(18, after='a: '), PP())],
      question=QP(4, '1) Waarnaar verwijzen', 'a: ‘hun’')),
    R('I1b', [one(S(19, after='b: '), PP())],
      question=QP(4, '1) Waarnaar verwijzen', 'b: ‘dat’')),
    R('I1c', [one(S(21, after='c: '), PP())],
      question=QP(4, 'Wat betekenen de volgende', 'c: ‘het bloed')),
    R('I1d', [one(S(22, after='d: '), PP())],
      question=QP(4, 'Wat betekenen de volgende', 'd: ‘van leer')),
    R('I1e', [one(L(24, 25, after='e: '), PP())]),
    R('I2', [one(S(27, before=' 2 punten'), SP(27)), one(S(28, before=' 2 punten'), SP(28)),
             one(S(29, before=' 1 punten'), SP(29))]),
    R('I3', [one(S(31), PP())], rownote=quote(S(30, after='3) ', before=' 5 punten'), lead='The scheme heads it')),
    R('I4', [one(L(33, 35), PP())], rownote=quote(S(32, after='4) ', before=' 5 punten'), lead='The scheme heads it')),
    R('I5', [one(L(37, 38), PP())], rownote=quote(S(36, after='5) ', before=' 5 punten'), lead='The scheme heads it')),
    R('I6', [one(L(40, 41), PP())], rownote=quote(S(39, after='6) ', before=' 5 punten'), lead='The scheme heads it')),
    R('II1', [graded(S(57), PARTP(), CRIT_2010)],
      rownote=examples(S(43), *[S(n) for n in range(44, 49)])),
    R('III1', [graded(L(54, 55), PARTP(), CRIT_2010)],
      question=QP(4, 'Schrijf een opstel', 'a) Omgangsvormen')),
    R('III2', [graded(L(54, 55), PARTP(), CRIT_2010)],
      question=QP(4, 'Schrijf een opstel', 'b) Niemand')),
]


# ================================================================ 2011 HL ===
# The scheme reprints every question with its price, then its answer. Q5's
# answer is how it is marked ("Goede uitleg en verwijzingen naar eigen
# onderwijs.", second reader 20 Nov): a row at the printed price. Q6 prints
# what an answer may contain: shown, priced as a whole (10a).
CRIT_2011 = crit(90, (91, 92), (93, 94), 95)
SPECS[2011] = [
    R('I1a', [one(S(25), PP())], question=QP(3, '1) Waarnaar verwijzen', 'a: ‘die’')),
    R('I1b', [one(S(27), PP())], question=QP(3, '1) Waarnaar verwijzen', 'b: ‘ze’')),
    R('I1c', [one(S(30), PP())], question=QP(3, 'Wat betekenen de volgende', 'c: ‘De leefwereld')),
    R('I1d', [one(L(32, 33), PP())], question=QP(3, 'Wat betekenen de volgende', 'd: ‘Wij hebben')),
    R('I1e', [one(L(36, 37), PP())]),
    R('I2', [one(L(40, 42), PP())]),
    R('I3', [one(L(48, 50), PP())]),
    R('I4', [one(L(54, 55), PP())]),
    R('I5', [one(S(61), PP())]),
    R('I6', [shown(S(66, after='• ')), shown(S(67, after='• ')), shown(S(68, after='• '))], whole=True,
      rownote=quote(S(64), S(65), lead='The scheme heads its points')),
    R('II1', [graded(S(89), PARTP(), CRIT_2011)],
      rownote=examples(S(73), *[S(n, after='• ') for n in range(74, 77)])),
    R('III1', [graded(L(86, 87), PARTP(), CRIT_2011)],
      question=QP(4, 'Schrijf een opstel', 'a) Mensen zijn')),
    R('III2', [graded(L(86, 87), PARTP(), CRIT_2011)],
      question=QP(4, 'Schrijf een opstel', 'b) In onze')),
]

# ================================================================ 2012 HL ===
# The scheme reprints the passage and every question. Under Q5 and under the
# tasks of Deel 2 and Deel 3 it prints nothing at all (p6 ends at Deel 3's two
# titles): the R4 line at the paper's printed price.
NOTHING_2012 = 'The scheme reprints this task and prints nothing under it.'
SPECS[2012] = [
    R('I1a', [one(S(82), PP())], question=QP(3, '1. Waarnaar verwijzen', 'a: ‘dit’')),
    R('I1b', [one(S(84), PP())], question=QP(3, '1. Waarnaar verwijzen', 'b: ‘hij of zij’')),
    R('I1c', [one(S(87), PP())], question=QP(3, 'Wat betekenen de volgende', 'c: ‘Zij zijn')),
    R('I1d', [one(S(90), PP())], question=QP(3, 'Wat betekenen de volgende', 'd: ‘In die zin')),
    R('I1e', [one(S(93), PP())], question=QP(3, 'Wat betekenen de volgende', 'e: ‘elke leraar')),
    R('I2', [one(S(100), PP())]),
    R('I3', [one(S(103), PP())]),
    R('I4', [one(S(106), PP())]),
    R('I5', [unprinted('The scheme reprints this question and prints nothing under it.')]),
    R('I6', [one(S(114), PP())]),
    R('II1', [unprinted(NOTHING_2012)]),
    R('III1', [unprinted(NOTHING_2012)], question=QP(4, 'Schrijf een opstel', 'a) Het gebruik')),
    R('III2', [unprinted(NOTHING_2012)], question=QP(4, 'Schrijf een opstel', 'b) In onze')),
]

# ================================================================ 2013 HL ===
# The scheme reprints the passage and the questions; each answer is followed by
# the passage sentence it rests on, in brackets, quoted in the row's note. Q5,
# Deel 2 and Deel 3: nothing printed under them (R4). Q6 answers only the
# first half of what it asks (the two demands, not the opinion): shown, priced
# as a whole.
def _passage(a, b):
    return quote(L(a, b), lead='The scheme quotes the passage beside its answer')


NOTHING_2013 = 'The scheme reprints this task and prints nothing under it.'
SPECS[2013] = [
    R('I1a', [one(S(113), PP())], question=QP(3, '1) Waarnaar verwijzen', 'a: ‘die’'),
      rownote=_passage(114, 115)),
    R('I1b', [one(S(117), PP())], question=QP(3, '1) Waarnaar verwijzen', 'b: ‘ze’'),
      rownote=_passage(118, 119)),
    R('I1c', [one(S(127), PP())], question=QP(3, 'Wat betekenen de volgende', 'c: ‘Taal staat'),
      rownote=_passage(128, 132)),
    R('I1d', [one(S(134), PP())], question=QP(3, 'Wat betekenen de volgende', 'd: ‘een wangedrocht'),
      rownote=_passage(135, 137)),
    R('I1e', [one(S(140), PP())]),
    R('I2', [one(S(145), PP())]),
    R('I3', [one(S(148), PP())], rownote=_passage(149, 151)),
    R('I4', [one(S(154), PP())], rownote=_passage(155, 159)),
    R('I5', [unprinted('The scheme reprints this question and prints nothing under it.')]),
    R('I6', [shown(S(171))], whole=True, rownote=_passage(172, 174)),
    R('II1', [unprinted('Under Deel 2 the scheme prints the task in other words than the paper '
                        '("ongeveer 100 woorden", and without the paper\'s closing question) and nothing '
                        'under it.')]),
    R('III1', [unprinted(NOTHING_2013)], question=QP(4, 'Schrijf een opstel', Run('a) Zolang iemand', 'is.'))),
    R('III2', [unprinted(NOTHING_2013)], question=QP(4, 'Schrijf een opstel', 'b) Je dromen')),
]

# ================================================================ 2014 HL ===
# Q1(a) and (b) are answered with the passage itself; Q5 and Q6 print what an
# answer must refer to "in elk geval" and the question also asks the
# candidate's own view: shown, priced as a whole. Deel 2 and Deel 3 print
# nothing under the task (R4); the scheme sets Deel 3's two titles in the
# other order from the paper's (the paper's a) is its b)), and the paper wins.
NOTHING_2014 = 'The scheme reprints this task and prints nothing under it.'
SPECS[2014] = [
    R('I1a', [one(S(50, after='In een ', before=', die'), PP())],
      question=QP(3, '1) Waarnaar verwijzen', 'a: ‘die’'),
      rownote=quote(S(50), lead='The scheme prints its answer in bold inside the passage')),
    R('I1b', [one(S(54, before=', die'), PP())], question=pre(3, '1) Waarnaar verwijzen'),
      rownote=quote(L(54, 57), lead='The scheme prints its answer in bold inside the passage')),
    R('I1c', [one(S(61), PP())]),
    R('I1d', [one(S(66), PP())]),
    R('I1e', [one(S(70), PP())]),
    R('I2', [one(L(74, 75), PP())]),
    R('I3', [one(S(81, before=' (5 punten)'), PP())]),
    R('I4', [one(L(84, 86), PP())]),
    R('I5', [shown(L(90, 91))], whole=True),
    R('I6', [shown(L(96, 97))], whole=True),
    R('II1', [unprinted(NOTHING_2014)]),
    R('III1', [unprinted('The scheme reprints the two titles, this one as its b), and prints nothing under '
                         'them.')],
      question=QP(4, 'Schrijf een opstel', 'a) ‘Mijn afhankelijkheid')),
    R('III2', [unprinted('The scheme reprints the two titles, this one as its a), and prints nothing under '
                         'them.')],
      question=QP(4, 'Schrijf een opstel', 'b) ‘Hoewel')),
]

# ================================================================ 2015 HL ===
# Deel 2: the scheme reprints the task and lists what an answer may raise, with
# no criteria and no marks beside them: shown under the paper's 30 (10a).
# Deel 3: nothing under the titles (R4).
NOTHING_2015 = 'The scheme reprints this task and prints nothing under it.'
SPECS[2015] = [
    R('I1a', [one(S(53), PP())], question=QP(3, '1) Waarnaar verwijzen', 'a: ‘ze’')),
    R('I1b', [one(S(56), PP())], question=pre(3, '1) Waarnaar verwijzen')),
    R('I1c', [one(S(59, before=' (1 punt)'), PP())]),
    R('I1d', [one(S(64), PP())]),
    R('I1e', [one(S(68), PP())]),
    R('I2', [one(S(72), PP())]),
    R('I3', [one(L(78, 79), PP())]),
    R('I4', [one(L(87, 88, before=' (5 punten)'), PP())]),
    R('I5', [one(S(90), PP())]),
    R('I6', [one(L(93, 94), PP())]),
    R('II1', [shown(S(n)) for n in range(99, 104)], whole=True),
    R('III1', [unprinted(NOTHING_2015)], question=QP(4, 'Schrijf een opstel', 'a) ‘Mijn taal')),
    R('III2', [unprinted(NOTHING_2015)], question=pre(4, 'Schrijf een opstel')),
]

# ================================================================ 2016 HL ===
# Q2 prints the reasons an answer must contain, Q4 and Q6 a position and
# arguments "ondermeer", Deel 2 what candidates may draw on: each shown, priced
# as a whole (10a). Q3 prices its three reasons "(1 p)", "(2 p)", "(2 p)". Q5
# prints two sub-tasks, "(2 punten)" and "(3 punten)", under one "(5 punten)"
# (paper p4): two criterion rows. Deel 3: nothing under the titles (R4).
NOTHING_2016 = 'The scheme reprints this task and prints nothing under it.'
SPECS[2016] = [
    R('I1a', [one(S(53), PP())], question=pre(3, '1. Waarnaar verwijzen')),
    R('I1b', [one(S(56), PP())], question=pre(3, '1. Waarnaar verwijzen')),
    R('I1c', [one(S(60), PP())]),
    R('I1d', [one(S(65), PP())]),
    R('I1e', [one(S(68), PP())]),
    R('I2', [shown(S(n, after='-')) for n in (77, 78, 79)], whole=True,
      rownote=quote(S(76), lead='The scheme heads its points')),
    R('I3', [one(S(81, before=' (1 p)'), RX(81, r'\((\d) p\)')),
             one(S(82, before=' (2 p)'), RX(82, r'\((\d) p\)')),
             one(S(83, before=' (2 p)'), RX(83, r'\((\d) p\)'))]),
    R('I4', [shown(S(89, after='- '))], whole=True,
      rownote=both(quote(S(88), lead='The scheme heads it'),
                   examples(L(90, 91), *[S(n, after='- ') for n in (92, 93)][:1], J(S(93, after='- '), S(94)),
                            *[S(n, after='- ') for n in (95, 96, 97)]),
                   examples(L(98, 99), *[S(n, after='- ') for n in (100, 101, 102, 103, 104)],
                            J(S(105, after='- '), S(106)), S(107, after='- ')))),
    R('I5', [part(L(112, 113, after='5. ', before=' (2 punten)'), RX(113, r'\((\d) punten\)'),
                  both(examples(S(115), L(116, 116, after='- '), L(117, 118, after='- '), S(119, after='- ')),
                       examples(S(120), L(121, 122, after='- '), S(123, after='- '), S(124, after='- '),
                                S(125, after='- ')))),
             part(S(126, before=' (3 punten)'), RX(126, r'\((\d) punten\)'),
                  quote(S(127), S(128, after='- '), S(129, after='- '), lead='The scheme prints'))],
      total=PY(4, 277)),
    R('I6', [shown(x) for x in (S(136), L(137, 138), S(139), S(140), S(145), L(146, 147))], whole=True,
      rownote=quote(S(134), S(135), lead='The scheme heads its points')),
    R('II1', [shown(L(151, 153)), shown(S(154)), shown(S(155))], whole=True),
    R('III1', [unprinted(NOTHING_2016)], question=QP(4, 'Schrijf een opstel', 'a) ‘Mijn taal')),
    R('III2', [unprinted(NOTHING_2016)], question=pre(4, 'Schrijf een opstel')),
]

# ================================================================ 2017 HL ===
# Prices printed "(1 p)" and "(5 p)"; Q3's and Q4's on lines of their own under
# the question (paper p4). From Q2 on the scheme prints examples, requirements
# or a model per question with no split: shown, priced as a whole (10a); Deel 2
# likewise under the paper's 30. Deel 3: nothing under the titles (R4).
NOTHING_2017 = 'The scheme reprints this task and prints nothing under it.'
SPECS[2017] = [
    R('I1a', [one(S(51), PP())]),
    R('I1b', [one(S(53), PP())]),
    R('I1c', [one(S(57), PP())]),
    R('I1d', [one(S(60), PP())]),
    R('I1e', [one(S(69), PP())]),
    R('I2', [shown(S(73, after='- ')), shown(L(74, 75, after='- ')), shown(L(76, 77, after='- ')),
             shown(S(78, after='- ')), shown(S(79, after='- ')), shown(S(80, after='- ')),
             shown(L(81, 82, after='- '))], whole=True,
      rownote=quote(S(72), lead='The scheme heads its points')),
    R('I3', [shown(L(86, 87)), shown(L(88, 89, before=' (5 p)'))], whole=True, total=PY(4, 168),
      question=QP(4, Run('3. ‘De oorzaak', 'verplaatst van'), 'Wat is dat onheil?')),
    R('I4', [shown(L(98, 100)), shown(L(101, 102))], whole=True, total=PY(4, 267),
      question=QP(4, Run('4. Ook professor', 'waarom de professor'), 'Ben je het eens')),
    R('I5', [shown(L(105, 107)), shown(L(108, 110)), shown(L(111, 112))], whole=True),
    R('I6', [shown(S(116)), shown(S(117)), shown(L(118, 119))], whole=True),
    R('II1', [shown(L(128, 130)), shown(L(131, 133)), shown(L(134, 135))], whole=True),
    R('III1', [unprinted(NOTHING_2017)], question=QP(4, 'Schrijf een opstel', 'a) ‘Mijn taal')),
    R('III2', [unprinted(NOTHING_2017)], question=pre(4, 'Schrijf een opstel')),
]

# ================================================================ 2018 HL ===
# Q2 prices each of five reasons "(1 p)". Q5: the paper prints only "(5
# punten)"; the scheme reprints it as two sub-tasks "(2 punten)" + "(3 punten)"
# (two criterion rows, its model answer in the first's note). Q3, Q4, Q6 and
# Deel 2 print requirements and examples: shown, priced as a whole (10a).
# Deel 3: nothing under the titles (R4).
NOTHING_2018 = 'The scheme reprints this task and prints nothing under it.'
P1 = r'\((\d) p\)'
SPECS[2018] = [
    R('I1a', [one(S(49), PP())]),
    R('I1b', [one(L(51, 52), PP())]),
    R('I1c', [one(S(55), PP())]),
    R('I1d', [one(S(59), PP())]),
    R('I1e', [one(L(64, 65), PP())]),
    R('I2', [one(L(73, 74, after='- ', before=' (1 p)'), RX(74, P1)), one(S(75, after='- '), RX(76, P1)),
             one(S(77, after='- ', before=' (1 p)'), RX(77, P1)),
             one(L(78, 79, after='- ', before=' (1 p)'), RX(79, P1)), one(S(80, after='- '), RX(81, P1))]),
    R('I3', [shown(L(88, 90, after='- ')), shown(L(91, 92, after='- '))], whole=True,
      rownote=quote(L(85, 87), lead='The scheme prints')),
    R('I4', [shown(S(106, after='- ')), shown(S(107, after='- ')), shown(S(108, after='- ')),
             shown(L(109, 110, after='- ')), shown(L(111, 113, after='- ')), shown(L(114, 115, after='- '))],
      whole=True, rownote=quote(L(101, 102), L(103, 104), S(105), lead='The scheme prints')),
    R('I5', [part(L(116, 117, after='5. ', before=' (2 punten)'), RX(117, r'\((\d) punten\)'),
                  quote(L(121, 122), L(123, 124), L(125, 126), lead='The scheme answers')),
             part(L(118, 119, before=' (3 punten)'), RX(119, r'\((\d) punten\)'),
                  quote(L(127, 128), lead='The scheme prints'))]),
    R('I6', [shown(S(142)), shown(S(143)), shown(S(144))], whole=True,
      rownote=quote(L(139, 141), lead='The scheme prints')),
    R('II1', [shown(L(152, 153)), shown(L(154, 155))], whole=True,
      rownote=quote(L(149, 151), lead='The scheme prints')),
    R('III1', [unprinted(NOTHING_2018)], question=QP(4, 'Schrijf een opstel', "a) 'De beste regels")),
    R('III2', [unprinted(NOTHING_2018)], question=pre(4, 'Schrijf een opstel')),
]

# ================================================================ 2019 HL ===
# Q2 prices its three reasons "(1 p)", "(2 p)", "(2 p)". Q5: the paper prints
# one question at "(5 punten)" (p4); the scheme prices that answer "(2 punten)"
# and adds a second question the paper does not print, "(3 punten)": carded on
# the paper's question and total, the scheme's lines quoted (CARD-STANDARD 5,
# 10f). Q3, Q4, Q6 and Deel 2: points and requirements shown, priced as a
# whole (10a). Deel 3: the scheme prints a different first title from the
# paper's and nothing under either (R4).
SPECS[2019] = [
    R('I1a', [one(S(53), PP())]),
    R('I1b', [one(S(55), PP())]),
    R('I1c', [one(S(59), PP())]),
    R('I1d', [one(S(63), PP())]),
    R('I1e', [one(S(71), PP())]),
    R('I2', [one(S(75, after='- ', before=' (1 p)'), RX(75, P1)),
             one(S(76, after='- ', before=' (2 p)'), RX(76, P1)),
             one(S(77, after='- ', before=' (2 p)'), RX(77, P1))]),
    R('I3', [shown(S(n)) for n in range(81, 89)], whole=True),
    R('I4', [shown(L(93, 95)), shown(L(96, 97)), shown(L(98, 99))], whole=True),
    R('I5', [shown(L(107, 108)), shown(L(109, 110)), shown(L(111, 112))], whole=True,
      question=QP(4, Run('5. Gebaseerd op de tekst', 'onderwijs een verbod')),
      rownote=lambda d: (f'The scheme prices this answer “{S(113).text(d)}” and goes on to a second question '
                         f'the paper does not print, “{L(114, 115).text(d)}” “{S(116).text(d)}”, with '
                         f'“{L(117, 118).text(d)}” The paper prints the question above at '
                         f'“(5 punten)”, and that is the card\'s total.')),
    R('I6', [shown(L(123, 125)), shown(L(126, 128)), shown(L(129, 130))], whole=True),
    R('II1', [shown(L(138, 139)), shown(L(140, 141)), shown(S(142))], whole=True),
    R('III1', [unprinted(lambda d: f'At a) the scheme prints a different title from the paper\'s, '
                                   f'“{S(145, after="a) ").text(d)}”, and nothing under either title.')],
      question=pre(4, 'Schrijf een opstel')),
    R('III2', [unprinted('The scheme reprints this title and prints nothing under it.')],
      question=pre(4, 'Schrijf een opstel')),
]

# ================================================================ 2020 HL ===
# Q1-Q4 answered with the scheme's own lines (Q2 and Q3 quote the passage).
# Q5 and Q6 print what an answer must refer to: shown, priced as a whole
# (10a). Deel 2 and Deel 3: nothing printed under the task (R4).
NOTHING_2020 = 'The scheme reprints this task and prints nothing under it.'
SPECS[2020] = [
    R('I1a', [one(L(53, 54), PP())], question=QP(3, '1) Waarnaar verwijzen', 'a: ‘dat’')),
    R('I1b', [one(L(56, 57), PP())], question=QP(3, '1) Waarnaar verwijzen', 'b: ‘daarvan’')),
    R('I1c', [one(S(61), PP())]),
    R('I1d', [one(S(65), PP())]),
    R('I1e', [one(S(73), PP())]),
    R('I2', [one(L(76, 80), PP())]),
    R('I3', [one(L(84, 89), PP())]),
    R('I4', [one(L(93, 95), PP())]),
    R('I5', [shown(L(103, 105))], whole=True),
    R('I6', [shown(L(109, 111)), shown(S(112))], whole=True),
    R('II1', [unprinted(NOTHING_2020)]),
    R('III1', [unprinted(NOTHING_2020)], question=QP(4, 'Schrijf een opstel', 'a) Taal verdeelt')),
    R('III2', [unprinted(NOTHING_2020)], question=QP(4, 'Schrijf een opstel', 'b) Mensen laten')),
]

# ================================================================ 2026 HL ===
# The paper's instruction over Q1 says (a) and (b) test grammar and (c)-(e)
# vocabulary; the second three carry it, the first two their own "Waarnaar
# verwijzen". Q5's census text lost "(19)" (Dorea Laan's age, read as a price,
# which also made the census price Q5 at 24): question and price read from the
# paper's own lines. From Q2 on the scheme prints points or requirements with
# no split: shown, priced as a whole (10a). Q6, Deel 2 and Deel 3: nothing
# printed under the task (R4).
NOTHING_2026 = 'The scheme reprints this task and prints nothing under it.'
VOCAB_2026 = prerun(3, 'Vragen a en b', 'woorden in de zinnen')
SPECS[2026] = [
    R('I1a', [one(S(69), PP())], question=pre(3, '1. Waarnaar verwijzen')),
    R('I1b', [one(S(73), PP())], question=pre(3, '1. Waarnaar verwijzen')),
    R('I1c', [one(S(77), PP())], question=VOCAB_2026),
    R('I1d', [one(S(81), PP())], question=VOCAB_2026),
    R('I1e', [one(S(85), PP())], question=VOCAB_2026),
    R('I2', [shown(S(92)), shown(S(93)), shown(S(94))], whole=True),
    R('I3', [shown(L(97, 100)), shown(L(101, 103))], whole=True),
    R('I4', [shown(L(109, 110))], whole=True),
    R('I5', [shown(L(116, 117))], whole=True, total=PY(4, 364),
      question=QP(4, Run('5. Dorea Laan', 'het geen 9 was'), Run('Uitgaande van', 'veeleisend ze'))),
    R('I6', [unprinted('The scheme reprints this question and prints nothing under it.')]),
    R('II1', [unprinted(NOTHING_2026)]),
    R('III1', [unprinted(NOTHING_2026)], question=QP(4, 'Schrijf een opstel', '1. Het is helemaal')),
    R('III2', [unprinted(NOTHING_2026)],
      question=QP(4, 'Schrijf een opstel', Run('2. Het leven', '(Louis Couperus)'))),
]

# ================================================================ 2021 HL ===
# Live: Q1-Q5 (9 cards). The three asks the old reader excluded: Q6 and Deel 2's
# two titles (this sitting has no commentary; Deel 2 is the essay, 40). The
# scheme reprints each and prints nothing under it (R4).
SPECS[2021] = [
    R('I6', [unprinted('The scheme reprints this question and prints nothing under it.')]),
    R('II1', [unprinted('The scheme reprints the two titles and prints nothing under them.')],
      question=pre(4, 'Schrijf een opstel')),
    R('II2', [unprinted('The scheme reprints the two titles and prints nothing under them.')],
      question=pre(4, 'Schrijf een opstel')),
]

# ================================================================ 2022 HL ===
# Live: Q1-Q5 (9 cards). Q6 and Deel 2's two titles: nothing printed (R4).
SPECS[2022] = [
    R('I6', [unprinted('The scheme reprints this question and prints nothing under it.')]),
    R('II1', [unprinted('The scheme reprints the two titles and prints nothing under them.')],
      question=pre(4, 'Schrijf een opstel')),
    R('II2', [unprinted('The scheme reprints the two titles and prints nothing under them.')],
      question=pre(4, 'Schrijf een opstel')),
]

# The pages each sitting prints its reading text on. Every Dutch booklet sets
# its passage on pp2-3 (cover p1, questions from p3 or p4); the census reads
# pp2-4 for 2010 and p3 alone where the passage opens with an unnumbered
# title (second reader, 20 Nov; checked on every paper's p2).
PAGES = {y: (2, 3) for y in list(range(2010, 2023)) + [2026]}


def specs(year):
    out = SPECS.get(year, [])
    for spec in out:
        if getattr(spec, 'pages', None) is None and year in PAGES:
            spec.pages = PAGES[year]
    return out
