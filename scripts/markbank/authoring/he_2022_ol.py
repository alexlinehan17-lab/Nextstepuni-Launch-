#!/usr/bin/env python3
"""Home Economics 2022 Ordinary Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2022, 'ordinary', 'he-2022-ol-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
if 'Section C' in T:
    T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "'Milk is a staple food in the diets of Irish children.' (www.nationaldairycouncil.ie) The table gives the nutritional content per 100 ml of Whole Milk and Super Milk Fat-free. (www.avonmore.ie)"
ways = semis(block(T, 'Milk in cereal; milkshakes, smoothies', '(c) Give an account of calcium'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-9', 'dairy-in-teenage-diet',
    '2022 OL Section B Q1(b)',
    'Outline three interesting ways of including dairy products into a teenager’s diet.',
    '3 ways @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Outline three interesting ways of including dairy products into a teenager’s diet',
          12, 3, 4, ways[:14],
          "Three ways at 4 marks, graded 4:2:0. The scheme's list runs through milk, then yoghurt, then cheese — taking one from each makes three obviously different ways, where three milk-based drinks read as one. \"Interesting\" is not marked, but \"outline\" is: naming the dish is 2 and saying how it gets dairy into the day is the other 2.")],
    "One long list in the scheme grouped by product, taken in order to the cap.",
    stem=Q1S))

cfun = semis(block(T, 'Strong bones; healthy teeth; clotting of blood', '• dietary sources'))
csrc = semis(block(T, 'Hard water; dairy products; canned fish', '• effect of deficiency'))
cdef = semis(block(T, 'Rickets; osteomalacia; osteoporosis; dental decay', '(d) Discuss four factors'))
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-8', 'calcium-account-ol',
    '2022 OL Section B Q1(c)',
    'Give an account of calcium under each of the following headings: functions in the body; dietary sources; effect of deficiency.',
    'functions 3 @ 4 marks (graded 4:2:0); sources 3 @ 4 marks (graded 4:2:0); deficiency 1 effect @ 4 marks (graded 4:2:0)',
    28,
    [anyN('r-1', 'Functions in the body', 12, 3, 4, cfun,
          "Three functions at 4 marks. Bones and teeth is the obvious one, but it is a single function — pair it with two of the less obvious ones (blood clotting, muscle contraction, nerve function) rather than splitting bones and teeth into two points."),
     anyN('r-2', 'Dietary sources', 12, 3, 4, csrc,
          "Three sources at 4 marks. Hard water is the first thing the scheme lists and the one almost nobody writes. Naming the food is 2; saying it is a good source or how it is fortified is the other 2."),
     anyN('r-3', 'Effect of deficiency', 4, 1, 4, cdef,
          "One effect, 4 marks — only 4 of the 28 marks, so name it, say who gets it, and stop. Rickets in children or osteoporosis in later life are the two that explain themselves.")],
    "28 marks split 12 + 12 + 4. The two big strands are equal and the deficiency is worth a third of either, which is not how the headings look on the page.",
    stem=Q1S, tariff_kind='fixed'))

buy_b, sto_b = heads(block(T, 'Buying: shop using list', 'Question 2'), ['Buying:', 'Storing:'])
dairy = semis(buy_b, drop_prefix='Buying:')[:7] + semis(sto_b, drop_prefix='Storing:')[:7]
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-1-5', 'buying-storing-dairy',
    '2022 OL Section B Q1(d)',
    'Discuss four factors to be considered when buying and storing dairy products in order to reduce food waste.',
    '4 factors @ 5 marks (graded 5:3:0); 1 reference to buying, 1 reference to storing, plus 2 others',
    20,
    [anyN('r-1', 'Discuss four factors to be considered when buying and storing dairy products in order to reduce food waste',
          20, 4, 5, dairy,
          "Four factors at 5 marks, with a mark reserved on each of buying and storing — four storage points cannot reach 20. The temperature is marking content (4C for dairy in the fridge), and so is the cheese detail: wrapped loosely in parchment rather than sealed, so it does not dry out. Naming the factor is 3; tying it to food not being thrown away is the 5.")],
    "The scheme groups the factors under the question's own two words and reserves a mark for each; the options are individual factors taken evenly from both groups so neither is lost to the cap.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "'Six in ten primary school children are not eating enough fibre.' (www.bordbia.ie)"
eff = semis(block(T, 'Moist heat causes starch grains to swell', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-0-2', 'effects-of-heat-on-cereals',
    '2022 OL Section B Q2(c)',
    'Outline the effects of heat on cereals.',
    '3 effects @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Outline the effects of heat on cereals', 12, 3, 4, eff,
          "Three effects at 4 marks. The first two are the same process in different media — starch grains swell and burst, absorbing cooking liquid in moist heat and fat in dry heat — and the scheme's examples (boiled rice, popcorn) are what make them two separate points. Naming the effect is 2; the example or the mechanism is the other 2.")],
    "One flat list, evenly priced.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "Home food preservation helps to reduce food waste."
saf = semis(block(T, 'Take care when using sharp knives', '(c) State two ways food labelling'))
cards.append(card(
    f'{P}-q3b', Y, L, 'home-economics-0-3', 'food-preservation-safety',
    '2022 OL Section B Q3(b)',
    'Describe four safety guidelines to follow when preserving food in the home.',
    '4 guidelines @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Describe four safety guidelines to follow when preserving food in the home', 16, 4, 4, saf[:14],
          "Four guidelines at 4 marks, graded 4:2:0. The list covers three different hazards — sharp equipment, heat and hot jars, and electricity — plus personal hygiene. Spreading four points across those reads better than four variations on knife safety. Naming the guideline is 2; saying which accident it prevents is the other 2.")],
    "The scheme prints a long list, taken in order to the cap.",
    stem=Q3S))

lab = semis(block(T, 'Informs consumer on properties of processed food', 'Question 4'))
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-1-2', 'food-labelling-benefits',
    '2022 OL Section B Q3(c)',
    'State two ways food labelling benefits the consumer when purchasing processed foods.',
    '2 ways @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'State two ways food labelling benefits the consumer when purchasing processed foods',
          10, 2, 5, lab[:14],
          "Two ways at 5 marks. \"State\" reads cheap but it is priced at 5, so each way still needs developing. The strongest are the ones that change a decision: allergen information for someone who cannot eat it, and use-by dates for someone deciding whether to buy. Listing what a label contains is a 3; saying what the shopper does with it is the 5.")],
    "One flat list, taken in order to the cap.",
    stem=Q3S))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "'When you buy a product or a service you have a number of rights under Irish legislation.' (www.citizensinformation.ie)"
rts = semis(block(T, 'Value for money; right to honest and truthful information', '(b) Set out the results of a study'))
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-1-2', 'consumer-rights-appliances',
    '2022 OL Section B Q4(a)',
    'Name and explain four consumer rights when buying household appliances.',
    '4 rights @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Name and explain four consumer rights when buying household appliances', 16, 4, 4, rts,
          "Four rights at 4 marks. The question says name AND explain, and that is the 2 + 2: \"right to redress\" is the name, and repair, replacement or refund is the explanation. Value for money and right to quality are close cousins — take one, not both.")],
    "One flat list, evenly priced.",
    stem=Q4S))

typ = semis(block(T, 'Type of appliance: microwave; kettle', '4 guidelines @ 3 marks'), drop_prefix='Type of appliance:')
gu = semis(block(T, 'Guidelines for use: follow manufacturer', '3 guidelines @ 3 marks'), drop_prefix='Guidelines for use:')
cc = semis(block(T, 'Guidelines for care and cleaning: unplug before cleaning', '(c) Explain two benefits'),
           drop_prefix='Guidelines for care and cleaning:')
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-3', 'small-electrical-appliance-study',
    '2022 OL Section B Q4(b)',
    'Set out the results of a study you have carried out on a small electrical kitchen appliance. Refer to: type of appliance; guidelines for use; guidelines for care and cleaning.',
    'type 1 @ 3 marks (graded 3:2:0); guidelines for use 4 @ 3 marks (graded 3:2:0); care and cleaning 3 @ 3 marks (graded 3:2:0)',
    24,
    [anyN('r-1', 'Type of appliance', 3, 1, 3, typ,
          "Naming the appliance is 3 marks for one word — and it anchors everything after it, because the use and cleaning guidelines are marked against the appliance you named. Descaling belongs to a kettle, blades to a food processor."),
     anyN('r-2', 'Guidelines for use', 12, 4, 3, gu[:14],
          "Four guidelines at 3 marks — half the question. These are about operating it safely and correctly: assembly, speeds, not overfilling, dry hands, no trailing flexes."),
     anyN('r-3', 'Guidelines for care and cleaning', 9, 3, 3, cc,
          "Three guidelines at 3 marks. The one that matters most is never immersing the motor or electrical section in water; unplugging before cleaning is the other non-negotiable. Both are safety points as much as care points.")],
    "24 marks split 3 + 12 + 9 across the question's three bullets.",
    stem=Q4S, tariff_kind='fixed'))

en = semis(block(T, 'Enables consumers to choose appliances based on their energy efficiency', 'Question 5'))
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-3', 'eu-energy-label',
    '2022 OL Section B Q4(c)',
    'Explain two benefits to the consumer of the EU energy label on electrical appliances.',
    '2 benefits @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Explain two benefits to the consumer of the EU energy label on electrical appliances',
          10, 2, 5, en,
          "Two benefits at 5 marks. The A-G scale is the detail worth having, and the two benefits that explain themselves are money (lower energy bills) and environment (a more sustainable choice). The QR code linking to an EU-wide database is the most recent addition and the one few students know.")],
    "One flat list, evenly priced.",
    stem=Q4S))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "Marriage is a popular lifestyle choice for couples in Irish society."
r_b, resp_b = heads(block(T, 'Rights: to each other’s company', '(b) Give an account of the following options'),
                    ['Rights:', 'Responsibilities:'])
rr = semis(r_b, drop_prefix='Rights:') + semis(resp_b, drop_prefix='Responsibilities:')
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-1', 'marriage-rights-responsibilities-ol',
    '2022 OL Section B Q5(a)',
    'Discuss the rights and responsibilities of a couple within a marriage relationship.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss the rights and responsibilities of a couple within a marriage relationship', 20, 4, 5, rr[:14],
          "Four points at 5 marks. The question names both rights and responsibilities, so an answer drawn from one list only is answering half of it. The clean test: a right is something the marriage gives you, a responsibility something it asks of you — inheritance under the Succession Act 1965 is a right, providing for dependent children is a responsibility.")],
    "The scheme's two headings flattened into individual points, since the tariff pools four across both.",
    stem=Q5S))

ls_b, dv_b = heads(block(T, 'Legal separation: Deed of Separation', '(c) Describe two different cultural variations'),
                   ['Legal separation:', 'Divorce:'])
sep = semis(ls_b, drop_prefix='Legal separation:')[:7] + semis(dv_b, drop_prefix='Divorce:')[:7]
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-1', 'legal-separation-divorce',
    '2022 OL Section B Q5(b)',
    'Give an account of the following options available to married couples who are separating: legal separation; divorce.',
    '4 points @ 5 marks (graded 5:3:0); 1 reference to legal separation, 1 reference to divorce, plus 2 others',
    20,
    [anyN('r-1', 'Give an account of legal separation and divorce as options for couples who are separating',
          20, 4, 5, sep,
          "Four points at 5 marks with a mark reserved on each option, so both must be covered. The distinguishing facts are what earn the 5: a legal separation is an agreement drawn up by a solicitor that avoids court, while a divorce ends the marriage, requires living apart for two of the previous three years, and gives the right to remarry. That two-of-three-years condition is the single most quotable detail here.")],
    "The scheme's two options flattened into individual points, taken evenly from each so both stay visible under the cap; the reserved mark on each is carried in the notation.",
    stem=Q5S))

cul = heads(block(T, 'Age: in Ireland, minimum age for marriage is 18', None),
            ['Age:', 'Choice of Spouse:', 'Arranged marriages:', 'Number of Partners/Spouses:',
             'Same sex marriage:', 'Wedding customs:', 'Types of ceremony:', 'Location:'])
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-1', 'cultural-variations-marriage',
    '2022 OL Section B Q5(c)',
    'Describe two different cultural variations in marital arrangements.',
    '2 cultural variations @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Describe two different cultural variations in marital arrangements', 10, 2, 5, cul,
          "Two variations at 5 marks. \"Cultural variation\" means the contrast, not the custom: naming arranged marriage is a 3, and saying it is decided by parents on background and suitability and remains common in the Travelling community is the 5. Each option carries the scheme's own comparison for that reason.")],
    "Eight variations in the scheme, best two taken, each kept with its own example.",
    stem=Q5S))

emit(cards)
