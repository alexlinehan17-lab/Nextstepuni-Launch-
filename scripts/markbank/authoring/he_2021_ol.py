#!/usr/bin/env python3
"""Home Economics 2021 Ordinary Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2021, 'ordinary', 'he-2021-ol-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
if 'Section C' in T:
    T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "'More than a quarter of young people growing up in Ireland are obese or overweight according to the latest Growing Up in Ireland survey.' (www.irishexaminer.com) The table gives nutritional information per 100 g for full fat, low fat and fat free natural yoghurt."
ob = semis(block(T, 'Imbalance in energy intake and energy expenditure', '(c) Give an account of lipids'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-1', 'causes-of-obesity',
    '2021 OL Section B Q1(b)',
    'State three causes of obesity.',
    '3 causes @ 4 marks each (graded 4:2:0)', 12,
    [anyN('r-1', 'State three causes of obesity', 12, 3, 4, ob,
          "Three causes at 4 marks, graded 4:2:0 — even though the question says \"state\", naming a cause is only 2 and the other 2 comes from saying how it leads to weight gain. The scheme's first cause is the underlying one all the others sit inside: an imbalance between energy taken in and energy used. Sedentary lifestyle and lack of exercise are the same cause twice.")],
    "One flat list, evenly priced.",
    stem=Q1S))

lcls = semis(block(T, 'Animal; plant; marine; saturated', '• functions in the body'))
lfun = semis(block(T, 'Heat; energy; excess lipids are stored', '• dietary sources'))
lsrc = semis(block(T, 'Meat; eggs; oily fish; dairy products', '(d) Discuss four factors'))
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-7', 'lipids-account-ol',
    '2021 OL Section B Q1(c)',
    'Give an account of lipids (fats) under each of the following headings: classification; functions in the body; dietary sources.',
    'classification 2 classes @ 4 marks (graded 4:0); functions 2 @ 4 marks (graded 4:2:0); sources 4 @ 3 marks (graded 3:2:0)',
    28,
    [anyN('r-1', 'Classification', 8, 2, 4, lcls,
          "Two classes at 4 marks, all-or-nothing — 8 marks for two words, the best return on the paper. The scheme accepts two different systems: by origin (animal, plant, marine) or by saturation (saturated, unsaturated). Pick one system and give two from it."),
     anyN('r-2', 'Functions in the body', 8, 2, 4, lfun,
          "Two functions at 4 marks, graded 4:2:0 — so unlike classification, a half-made point scores here. Heat and energy is one function, not two; pair it with insulation, protecting organs, or carrying the fat-soluble vitamins A, D, E and K."),
     anyN('r-3', 'Dietary sources', 12, 4, 3, lsrc,
          "Four sources at 3 marks — the largest strand at 12 marks. Naming the food is 2 and saying which kind of fat it provides is the third mark, so pairing oily fish or olives with unsaturated fat earns more than a bare list.")],
    "28 marks split 8 + 8 + 12 across the three headings. Classification is all-or-nothing while the other two are not, which is worth knowing before you spend time on it.",
    stem=Q1S, tariff_kind='fixed'))

fat = semis(block(T, 'Choose food naturally low in fat', 'Question 2'))
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-0-7', 'reducing-fat-intake',
    '2021 OL Section B Q1(d)',
    'Discuss four factors to be considered when selecting and buying foods to reduce fat intake in the diet.',
    '4 factors @ 5 marks each (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss four factors to be considered when selecting and buying foods to reduce fat intake in the diet',
          20, 4, 5, fat[:14],
          "Four factors at 5 marks, graded 5:3:0 — named is 3, discussed is 5. The traffic-light label system is the most specific point in the scheme and the easiest to develop: colour coding shows at a glance whether a food is high, medium or low in fat. Several other entries are versions of \"read the label\", and a marker will pay for that once.")],
    "One flat list, taken in scheme order to the cap.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "Healthy eating during pregnancy is critical to the baby's growth and development."
preg = semis(block(T, 'Protein for growth and development of new cells', '(b) Having regard to current healthy eating guidelines'))
cards.append(card(
    f'{P}-q2a', Y, L, 'home-economics-0-1', 'pregnancy-dietary-requirements-ol',
    '2021 OL Section B Q2(a)',
    'Discuss four dietary requirements of pregnant women.',
    '4 requirements @ 5 marks each (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss four dietary requirements of pregnant women', 20, 4, 5, preg[:14],
          "Four requirements at 5 marks, graded 5:3:0. Every entry in the scheme pairs a nutrient with a reason, and that pairing is the difference between 3 and 5 — folic acid is a 3, folic acid before and during pregnancy to reduce the risk of neural tube defects is a 5. The list also includes what to avoid (raw eggs, unpasteurised cheese, pâté, alcohol), and those count as requirements too.")],
    "One flat list, taken in scheme order to the cap.",
    stem=Q2S))

lab = semis(block(T, 'Informs consumer on properties of prepacked food', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-1-2', 'food-labelling-buying',
    '2021 OL Section B Q2(c)',
    'Explain how food labelling assists consumers when buying food.',
    '3 points @ 4 marks each (graded 4:2:0)', 12,
    [anyN('r-1', 'Explain how food labelling assists consumers when buying food', 12, 3, 4, lab[:14],
          "Three points at 4 marks. \"Explain how it assists\" is the whole question — listing what a label contains is 2, and saying what the shopper can then do is the other 2. Allergens and use-by dates are the two that change a decision most obviously.")],
    "One flat list, taken in order to the cap.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "Irish grown vegetables get to our shelves quickly, and so are more nutritious."
ck = semis(block(T, 'Effects of cooking: increases digestibility', '3 guidelines @ 3 marks'),
           drop_prefix='Effects of cooking:')
sg = semis(block(T, 'Guidelines for storing: remove from plastic packaging', '(c) Suggest two interesting ways'),
           drop_prefix='Guidelines for storing:')
cards.append(card(
    f'{P}-q3b', Y, L, 'home-economics-0-9', 'vegetables-cooking-storage',
    '2021 OL Section B Q3(b)',
    'Outline: (i) the effects of cooking on vegetables; (ii) the guidelines for storing vegetables.',
    'effects 3 @ 3 marks each (graded 3:2:0); storage guidelines 3 @ 3 marks each (graded 3:2:0)', 18,
    [anyN('r-1', 'The effects of cooking on vegetables', 9, 3, 3, ck,
          "Three effects at 3 marks. These are changes to the vegetable itself — starch grains bursting, cellulose softening, enzymes denatured, vitamin C destroyed — not opinions about taste. Naming the effect is 2; saying what it does for digestibility or nutrient content is the third mark."),
     anyN('r-2', 'The guidelines for storing vegetables', 9, 3, 3, sg,
          "Three guidelines at 3 marks, worth exactly as much as the cooking half — so do not let the first half eat the time. The specifics carry the marks: potatoes in a dark, dry, well-ventilated place, salad in the fridge drawer, packaging removed.")],
    "18 marks split evenly between the question's two numbered halves, so two rows.",
    stem=Q3S, tariff_kind='fixed'))

kid = semis(block(T, 'Stir fry vegetables; use cherry tomatoes in lunch boxes', 'Question 4'))
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-0-10', 'vegetables-for-children',
    '2021 OL Section B Q3(c)',
    'Suggest two interesting ways of including vegetables in the diet of children.',
    '2 ways @ 6 marks each (graded 6:3:0)', 12,
    [anyN('r-1', 'Suggest two interesting ways of including vegetables in the diet of children', 12, 2, 6, kid[:14],
          "Only two ways, but 6 marks each and graded 6:3:0 — half or full, nothing between, so a bare suggestion loses three marks outright. The child angle is what earns the top half: cutters to make animal shapes, grating vegetables into dishes to disguise them, growing them at home. \"Add to stews\" is true of any diet and reads as a 3.")],
    "One flat list, taken in order to the cap.",
    stem=Q3S))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "Good money management is an important life skill."
adv = semis(block(T, 'Areas of overspending identified; provides financial security', '(b) Set out a weekly budget plan'))
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-1-1', 'advantages-household-budget',
    '2021 OL Section B Q4(a)',
    'Discuss four advantages of planning a household budget for a family.',
    '4 advantages @ 5 marks each (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss four advantages of planning a household budget for a family', 20, 4, 5, adv[:14],
          "Four advantages at 5 marks, graded 5:3:0. A large part of this list is the same idea in different clothes — financial security, provides for emergencies, covers unplanned events, avoids debt — and a marker pays once. Spread the four across spotting overspending, security, saving, and the skill itself.")],
    "One flat list, taken in order to the cap.",
    stem=Q4S))

pl = semis(block(T, 'Rent 25%; food 25%; household bills 15%', '(c) State one advantage and one disadvantage'))
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-1', 'weekly-budget-plan-ol',
    '2021 OL Section B Q4(b)',
    'Set out a weekly budget plan for a family (two adults and two children) with a net income of EUR 800 a week.',
    '5 points @ 4 marks each (graded 4:2:0)', 20,
    [anyN('r-1', 'Set out a weekly budget plan for a family with a net income of EUR 800 a week', 20, 5, 4, pl,
          "Five points at 4 marks, graded 4:2:0. This is a plan, not prose: the scheme's percentages are the answer and a heading with its percentage earns the 4 where a heading alone earns 2. They total 100%, so the euro amounts have to add to EUR 800 — an arithmetic slip costs marks the headings had already earned. Reviewing the budget regularly is a point in its own right.")],
    "One flat list; the scheme's percentages are kept inside the options because they are the marking content.",
    stem=Q4S))

cadv = semis(block(T, 'Advantage: buy now pay later', 'Disadvantage: expensive'), drop_prefix='Advantage:')
cdis = semis(block(T, 'Disadvantage: expensive; high rates of interest', 'Question 5'), drop_prefix='Disadvantage:')
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-1', 'buying-on-credit',
    '2021 OL Section B Q4(c)',
    'State one advantage and one disadvantage of buying goods on credit.',
    '2 points @ 5 marks each (graded 5:3:0); 1 advantage, 1 disadvantage', 10,
    [anyN('r-1', 'One advantage of buying goods on credit', 5, 1, 5, cadv,
          "One advantage, 5 marks. The question fixes one of each, so two advantages cannot score 10 however good they are. Graded 5:3:0 — stating it is 3, and explaining what it lets the buyer do is the 5."),
     anyN('r-2', 'One disadvantage of buying goods on credit', 5, 1, 5, cdis,
          "One disadvantage, 5 marks. The strongest are the ones with a consequence attached: goods can be repossessed if repayments are missed, and a poor credit rating makes future borrowing harder.")],
    "The question fixes one advantage and one disadvantage, so two rows rather than a pooled pair.",
    stem=Q4S, tariff_kind='fixed'))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "We live in an increasingly diverse world, even within our own family structures."
_fs = heads(block(T, 'One parent family: consists of one parent', '(b) Discuss the roles and responsibilities of adolescents'),
            ['One parent family:', 'Nuclear family:', 'Blended family:'])
fs = [semis(_fs[0], drop_prefix='One parent family:')[:8],
      semis(_fs[1], drop_prefix='Nuclear family:')[:8],
      semis(_fs[2], drop_prefix='Blended family:')[:8]]
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-0', 'family-structures',
    '2021 OL Section B Q5(a)',
    'Describe each of the following family structures: one parent family; nuclear family; blended family.',
    'one parent 2 points @ 3 marks (graded 3:2:0); nuclear 2 points @ 3 marks (graded 3:2:0); blended 2 points @ 3 marks (graded 3:2:0)',
    18,
    [anyN(f'r-{i+1}', name, 6, 2, 3, fs[i], note) for i, (name, note) in enumerate([
        ('One parent family', "Two points at 3 marks. All three structures are compulsory and identically priced, so this is three short descriptions rather than a choice — skipping one costs a flat 6. Here the two points come easily as what it is and what follows from it: one parent with their children, and the financial or emotional pressures that can result."),
        ('Nuclear family', "Two points at 3 marks. The scheme's description is longer than the others but the tariff is the same — parents and children in a self-contained unit, with shared tasks and small family size. Do not overspend on the structure you know best."),
        ('Blended family', "Two points at 3 marks. The definition is the first point — partners with children from previous relationships, often with children of their own — and the second is best taken from the consequences the scheme lists: extra financial pressure, or discipline between step-parents and children."),
    ])],
    "Three compulsory structures at 6 marks each, so three rows rather than a pooled choice.",
    stem=Q5S, tariff_kind='fixed'))

teen = semis(block(T, 'Roles and responsibilities: son/daughter/brother', '(c) Outline why good communication'),
             drop_prefix='Roles and responsibilities:')
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-1', 'adolescent-roles-responsibilities',
    '2021 OL Section B Q5(b)',
    'Discuss the roles and responsibilities of adolescents/teenagers within a family.',
    '4 points @ 5 marks each (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss the roles and responsibilities of adolescents/teenagers within a family', 20, 4, 5, teen[:14],
          "Four points at 5 marks, graded 5:3:0. The scheme's strongest point is the tension it names outright: role expectations are difficult because an adolescent is no longer a child but does not yet carry the responsibility of an adult. Building an answer around that, rather than listing chores, is what reaches 5 a point.")],
    "One flat list, taken in order to the cap.",
    stem=Q5S))

comm = semis(block(T, 'Helps clarify rules and expectations', None))
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-0', 'family-communication',
    '2021 OL Section B Q5(c)',
    'Outline why good communication is important between family members.',
    '3 points @ 4 marks each (graded 4:2:0)', 12,
    [anyN('r-1', 'Outline why good communication is important between family members', 12, 3, 4, comm,
          "Three points at 4 marks. Every entry has a consequence built into it — trust, resolved conflict, self-esteem, knowing what is expected — and naming the consequence is the second 2. \"It is important to talk\" is not a point; saying that clear expectations prevent conflict is.")],
    "One flat list, evenly priced.",
    stem=Q5S))

emit(cards)
