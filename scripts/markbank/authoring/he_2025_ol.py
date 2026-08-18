#!/usr/bin/env python3
"""Home Economics 2025 Ordinary Level, Section B."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2025, 'ordinary', 'he-2025-ol-sb'
T = load(Y, L)
T = T[T.index('Question 1\nWhen purchasing convenience foods'):]
cards = []

# ── Q1 ──────────────────────────────────────────────────────────────────────
Q1S = "When purchasing convenience foods, consumers should consider nutritional value. The table gives nutritional information per 100 g and cost of two types of convenience vegetable soup: Soup A (cook-chill, EUR 2.89) and Soup B (canned, EUR 2.00)."

b = block(T, '• dietary sources', '• functions in the body')
sources = semis(b.split('\n', 1)[1])
b = block(T, '• functions in the body', '• effect of deficiency')
functions = semis(b.split('4 marks (graded 4:2:0)', 1)[1])
b = block(T, '• effect of deficiency', '(c) Outline three different ways')
deficiency = semis(b.split('4 marks (graded 4:2:0)', 1)[1])
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-8', 'vitamin-c',
    '2025 OL Section B Q1(b)',
    'Give an account of Vitamin C under each of the following headings: dietary sources; functions in the body; effect of deficiency.',
    'sources 3 @ 4 marks (graded 4:2:0); functions 2 @ 4 marks (graded 4:2:0); deficiency 1 @ 4 marks (graded 4:2:0)',
    24,
    [anyN('r-1', 'Dietary sources', 12, 3, 4, sources,
          "Three sources at 4 marks, graded 4:2:0 — half marks or nothing, so a named source with nothing said about it sits at 2. The scheme opens with \"accept any fruit/vegetable source\", which makes this the most forgiving 12 marks on the question: almost any fruit or vegetable earns the 2, and the other 2 comes from saying it is a good source."),
     anyN('r-2', 'Functions in the body', 8, 2, 4, functions,
          "Two functions at 4 marks. Note what counts as a function: forming collagen or assisting iron absorption is a function, whereas \"prevents scurvy\" is a deficiency effect and belongs in the third heading — using it here answers the wrong bullet."),
     anyN('r-3', 'Effect of deficiency', 4, 1, 4, deficiency,
          "One deficiency effect, 4 marks, graded 4:2:0. Only 4 marks are here, so a long list of deficiency signs earns no more than the first one properly explained.")],
    "Three headings printed in the question and priced separately (12 + 8 + 4), so three rows. The mark split is uneven and worth seeing: sources are worth three times the deficiency.",
    stem="Eggs and Vitamin C: the question sets three headings.",
    tariff_kind='fixed'))

ways = semis(block(T, '3 ways @ 4 marks (graded 4:2:0)', '(d) Describe four factors').split('\n', 1)[1])
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-10', 'fruit-veg-in-teenage-diet',
    '2025 OL Section B Q1(c)',
    'Outline three different ways a teenager can include fruit and vegetables in their diet.',
    '3 ways @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Outline three different ways a teenager can include fruit and vegetables in their diet',
          12, 3, 4, ways[:14],
          "Three ways at 4 marks, graded 4:2:0. The word doing the work is \"different\": three variations on the same idea — soups, sauces, blended sauces — read as one way, and the scheme's list is deliberately spread across meals and snacks. Naming the method is the 2; saying how it gets fruit or veg into the day is the other 2.")],
    "The scheme prints 15 ways and a card may show 14, so the list is shown to the cap in scheme order. Everything dropped is a near-duplicate of a way already listed, and the row stays openList so any correct method still scores."))

factors = semis(block(T, '4 factors @ 5 marks (graded 5:3:0)', 'Question 2').split('\n', 1)[1])
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-1-2', 'convenience-food-selection',
    '2025 OL Section B Q1(d)',
    'Describe four factors consumers should consider when selecting convenience food products.',
    '4 factors @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Describe four factors consumers should consider when selecting convenience food products',
          20, 4, 5, factors,
          "Four factors at 5 marks, graded 5:3:0 — named is 3, described is 5, and nothing in between. \"Describe\" is the whole gap: \"cost\" is a 3, and what a consumer actually compares when weighing cost is the 5. The list runs well beyond nutrition, and allergens, storage instructions and food miles are the ones most often missed.")],
    "One flat list in the scheme, priced evenly, so a single group.",
    stem=Q1S))

# ── Q2 ──────────────────────────────────────────────────────────────────────
Q2S = "Eggs provide the body with essential nutrients."
nutritive, dietetic = heads(block(T, 'Nutritive: HBV protein', '(b) Set out a menu'),
                            ['Nutritive:', 'Dietetic:'])
HELD_Q2A = (card(
    f'{P}-q2a', Y, L, 'home-economics-0-9', 'eggs-nutritive-dietetic',
    '2025 OL Section B Q2(a)',
    'Give an account of (i) the nutritive value and (ii) dietetic value of eggs.',
    '4 points @ 5 marks (graded 5:4:3:2:0); 1 reference to nutritive value, 1 reference to dietetic value, + 2 other points',
    20,
    [anyN('r-1', 'Give an account of the nutritive value and dietetic value of eggs', 20, 4, 5,
          [nutritive, dietetic],
          "Four points at 5 marks, but the distribution is fixed: at least one on nutritive value, at least one on dietetic value, then two from either. Four excellent nutritive points cannot score 20, because a dietetic mark is reserved. The distinction is the thing to hold onto — nutritive value is what an egg contains, dietetic value is what that means for who should eat it. Note both lists include what eggs LACK (carbohydrate, vitamin C), and those count.")],
    "The scheme prints two grouped lists and the notation reserves a mark for each, so the groups are the options and the reservation is carried in the notation.",
    stem=Q2S, answer=4, of_parts=2, per_part=5))


effects = semis(block(T, '3 effects @ 4 marks (graded 4:2:0)', 'Question 3').split('\n', 1)[1])
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-0-2', 'effects-of-heat-on-eggs',
    '2025 OL Section B Q2(c)',
    'Outline the effects of heat on eggs.',
    '3 effects @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Outline the effects of heat on eggs', 12, 3, 4, effects,
          "Three effects at 4 marks, graded 4:2:0. These are chemistry, not cookery: coagulation, curdling at high temperature, and the iron-sulphur reaction that greens the yolk are the three the scheme leads with. Naming the effect is 2; saying what heat does to the protein to cause it is the other 2.")],
    "One flat list, evenly priced.",
    stem=Q2S))

# ── Q3 ──────────────────────────────────────────────────────────────────────
Q3S = "Various factors impact food preservation and food spoilage."
causes = heads(block(T, 'moisture loss:', '(b) Name and give details'),
               ['moisture loss:', 'enzyme action:', 'microbial contamination:', 'chemical contamination:'])
cards.append(card(
    f'{P}-q3a', Y, L, 'home-economics-0-4', 'causes-of-food-spoilage',
    '2025 OL Section B Q3(a)',
    'Describe three main causes of food spoilage.',
    '3 causes @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Describe three main causes of food spoilage', 15, 3, 5, causes,
          "Three causes at 5 marks, graded 5:3:0. Naming the cause is 3 and describing how it spoils food is 5 — and each option carries its own examples for exactly that reason. Enzyme action is the one students most often leave at the name; the browning of a cut apple is the description that earns the extra 2.")],
    "Four causes in the scheme, best three taken. Each is kept with its examples because the examples are what turn a 3 into a 5.",
    stem=Q3S))

adv = semis(block(T, '2 advantages @ 5 marks (graded 5:3:0)', 'Question 4').split('\n', 1)[1])
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-0-4', 'advantages-of-preservation',
    '2025 OL Section B Q3(c)',
    'Discuss two advantages of food preservation.',
    '2 advantages @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Discuss two advantages of food preservation', 10, 2, 5, adv,
          "Only two advantages, at 5 marks each — so this is a short answer where each point has to be developed, not a list. Graded 5:3:0: naming the advantage is 3. \"Discuss\" wants the consequence, and the environmental and food-waste points are the two that most easily carry a sentence of development.")],
    "One flat list, evenly priced.",
    stem=Q3S))

# ── Q4 ──────────────────────────────────────────────────────────────────────
Q4S = "Budgeting has become an ever more important household task."
badv = semis(block(T, '4 advantages @ 5 marks (graded 5:3:0)', '(b) Set out a weekly budget plan').split('\n', 1)[1])
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-1-1', 'advantages-of-budgeting',
    '2025 OL Section B Q4(a)',
    'Discuss four advantages of budgeting.',
    '4 advantages @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss four advantages of budgeting', 20, 4, 5, badv,
          "Four advantages at 5 marks, graded 5:3:0 — named is 3, discussed is 5. Several of these are close relatives (financial security, money for emergencies, covering unplanned events) and a marker will not pay twice for the same idea in different words, so spread the four across money management, debt, security and stress.")],
    "One flat list, evenly priced.",
    stem=Q4S))

plan = semis(block(T, '5 points @ 4 marks (graded 4:2:0)', '(c) Outline the role of the Money Advice').split('\n', 1)[1])
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-1', 'weekly-budget-plan',
    '2025 OL Section B Q4(b)',
    'Set out a weekly budget plan for a family of two adults and two children with a net income of EUR 900 a week in total.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Set out a weekly budget plan for a family of two adults and two children with a net income of EUR 900 a week',
          20, 5, 4, plan,
          "Five points at 4 marks, graded 4:2:0. This is a plan, not an essay: the scheme's own percentages are the answer, and a heading with a percentage against it earns the 4 where a heading alone earns 2. They total 100%, so the arithmetic has to work against the EUR 900 — a budget that does not add up loses marks the headings had already earned. \"Evaluate/review the budget regularly\" is a point in its own right and the one most often left off.")],
    "One flat list, evenly priced. The percentages are the scheme's and are kept in the options because they are the marking content.",
    stem=Q4S))

mabs = semis(block(T, '2 points @ 5 marks (graded 5:3:0)', 'Question 5').split('\n', 1)[1])
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-1', 'mabs-role',
    '2025 OL Section B Q4(c)',
    'Outline the role of the Money Advice and Budgeting Service (MABS).',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Outline the role of the Money Advice and Budgeting Service (MABS)', 10, 2, 5, mabs,
          "Two points at 5 marks. The first mark most students have is that the service is free and independent; the second 5 needs something MABS actually does — negotiating with lenders, building a repayment schedule, personal insolvency advice. Naming the service back to the examiner earns nothing.")],
    "One flat list, evenly priced.",
    stem=Q4S))

# ── Q5 ──────────────────────────────────────────────────────────────────────
Q5S = "A wedding is an important day in a couple's life."
ways5 = semis(block(T, '4 ways @ 5 marks (graded 5:3:0)', '(b) Explain the rights and responsibilities').split('\n', 1)[1])
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-1', 'marriage-customs-cultures',
    '2025 OL Section B Q5(a)',
    'Describe four ways that marriage customs may differ between cultures.',
    '4 ways @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Describe four ways that marriage customs may differ between cultures', 20, 4, 5, ways5,
          "Four ways at 5 marks, graded 5:3:0. \"Differ between cultures\" is the requirement: naming a custom is 3, and contrasting how it varies from one culture to another is 5. An answer describing an Irish church wedding four times over scores 12 at best.")],
    "One flat list. The scheme's \"type of: veils; rings; ceremony; clothing\" is kept as printed because those are variations on one way, not four.",
    stem=Q5S))

rights_blk, resp_blk = heads(block(T, 'Rights: to each other', '(c) Discuss how pre-marriage courses'),
                             ['Rights:', 'Responsibilities:'])
rights_resp = semis(rights_blk, drop_prefix='Rights:') + semis(resp_blk, drop_prefix='Responsibilities:')
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-1', 'marriage-rights-responsibilities',
    '2025 OL Section B Q5(b)',
    'Explain the rights and responsibilities of marriage partners.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Explain the rights and responsibilities of marriage partners', 20, 4, 5, rights_resp,
          "Four points at 5 marks. The question names both rights AND responsibilities, so an answer drawn entirely from one list is answering half the question. The clean test: a right is something you receive from the marriage, a responsibility is something you owe to it — inheritance is a right, providing for dependent children is a responsibility.")],
    "The scheme prints the points under two headings (Rights / Responsibilities) but prices them as one pool of four, so they are one group of individual points rather than two options. The headings are not shown, deliberately: sorting a point into the right column is part of what the question asks, and the contextNote gives the test rather than the answer.",
    stem=Q5S, answer=4, of_parts=2, per_part=5))

pre = semis(block(T, '(c) Discuss how pre-marriage courses', 'Section C').split('(graded 5:3:0)', 1)[1])
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-1', 'pre-marriage-courses',
    '2025 OL Section B Q5(c)',
    'Discuss how pre-marriage courses can help couples to prepare for marriage.',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Discuss how pre-marriage courses can help couples to prepare for marriage', 10, 2, 5, pre,
          "Two points at 5 marks, so both need developing. The scheme names Accord as the provider, which is worth knowing, but the marks are for what a course does — surfacing expectations, agreeing roles, handling money and conflict — rather than for naming who runs it.")],
    "One flat list, evenly priced.",
    stem=Q5S))

# ── Q3(b) 25 marks — one method of preservation ────────────────────────────
name_opts = heads(block(T, 'heat treatment: jam making', 'Method of preservation 4 points'),
                  ['heat treatment:', 'chemical preservation:', 'drying:', 'freezing:'])
meth_opts = heads(block(T, 'jam/chutney making: wash jars', '(c) Discuss two advantages'),
                  ['jam/chutney making:', 'bottling/aseptic canning/in container canning:',
                   'drying: tie herbs', 'freezing: blanch', 'commercial freezing:', 'commercial drying:'])
cards.append(card(
    f'{P}-q3b', Y, L, 'home-economics-0-4', 'food-preservation-method',
    '2025 OL Section B Q3(b)',
    'Name and give details of how one method of food preservation is carried out.',
    'name 1 point @ 5 marks (graded 5:3:0); method of preservation 4 points @ 5 marks (graded 5:3:0)',
    25,
    [anyN('r-1', 'Name one method of food preservation', 5, 1, 5, name_opts,
          "Naming the method is worth 5 on its own, graded 5:3:0 — a whole fifth of the question for one word, and the scheme's four families are broad enough that almost any named method lands. Name it precisely (jam making, not \"heat\"), because the four method marks below are then marked against the method you named."),
     anyN('r-2', 'Give details of how the method is carried out', 20, 4, 5, meth_opts,
          "Four points at 5 marks on the method NAMED above — the two rows are marked together, so steps borrowed from a different method do not pay. These are ordered processes and the scheme lists them in sequence: for jam, sterilising the jars comes before the fruit and setting point before potting. A step out of order describes a process that would not work.")],
    "25 marks split 5 + 20. Kept as two rows because the naming mark is priced separately and is the single cheapest mark in Section B.",
    stem=Q3S, tariff_kind='fixed'))

emit(cards)
