#!/usr/bin/env python3
"""Home Economics 2024 Ordinary Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2024, 'ordinary', 'he-2024-ol-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
if 'Section C' in T:
    T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "'All around the world, people choose to eat different food for many different reasons.' (www.foodfactoflife.org.uk) The diagram lists factors affecting food choice: work patterns, food availability, emotions, likes and dislikes, cooking skills, money, time."
fac = heads(block(T, 'Emotions buy more food', '(b) Give an account of carbohydrates'),
            ['Emotions buy', 'Cooking skills people', 'Time:', 'Money price wars',
             'Likes and dislikes may', 'Food availability foods', 'Work patterns busy'])
cards.append(card(
    f'{P}-q1a', Y, L, 'home-economics-0-10', 'factors-affecting-food-choice',
    '2024 OL Section B Q1(a)',
    'Using the information presented in the table, discuss five factors that affect a person’s food choices.',
    '5 @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Discuss five factors that affect a person’s food choices', 20, 5, 4, fac,
          "Five of the seven factors in the diagram, 4 marks each, graded 4:2:0 — named is 2, discussed is 4, nothing in between. The factors are given to you on the page, so the 2 is nearly free and every mark that matters is in the second half. Time and work patterns overlap heavily; taking both and saying the same thing about convenience food twice earns one 4, not two.")],
    "Seven factors printed in the diagram, best five taken.",
    stem=Q1S))

cls = semis(block(T, 'monosaccharides; disaccharides; polysaccharides', '• functions in the body'))
fun = semis(block(T, 'heat; energy; stimulate peristalsis', '• dietary sources'))
src = semis(block(T, 'breakfast cereals; rice; pasta', '(c) Outline three different ways'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-6', 'carbohydrates-account',
    '2024 OL Section B Q1(b)',
    'Give an account of carbohydrates under each of the following headings: classification; functions in the body; dietary sources.',
    'classification 3 classes @ 2 marks (graded 2:0); functions 2 @ 5 marks (graded 5:3:0); sources 3 @ 4 marks (graded 4:2:0)',
    28,
    [anyN('r-1', 'Classification', 6, 3, 2, cls,
          "Three classes at 2 marks, all-or-nothing. The cheapest 6 marks in Section B: three words. Either the chemical names (mono-, di-, polysaccharides) or the everyday ones (sugar, starch, fibre) score."),
     anyN('r-2', 'Functions in the body', 10, 2, 5, fun,
          "Only two functions but 5 marks each — the opposite shape to the rest of this question, and the strand where a one-word answer costs most. Graded 5:3:0, so \"energy\" is a 3 and saying what the body does with it is the 5."),
     anyN('r-3', 'Dietary sources', 12, 3, 4, src[:14],
          "Three sources at 4 marks. Worth noticing this is the biggest strand of the three at 12 marks — more than classification and worth naming a food and saying which carbohydrate it provides, since the 2 is for the food and the other 2 for the link.")],
    "28 marks split 6 + 10 + 12 across the question's three headings. The split is very uneven and runs opposite to how much there is to say, which is the thing to notice.",
    stem=Q1S, tariff_kind='fixed'))

fib = semis(block(T, 'add bran/fruit to breakfast cereals', '(d) Describe four ways consumers'))
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-6', 'increasing-dietary-fibre',
    '2024 OL Section B Q1(c)',
    'Outline three different ways a person can increase the amount of fibre in their diet.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Outline three different ways a person can increase the amount of fibre in their diet',
          12, 3, 4, fib,
          "Three ways at 4 marks. \"Different\" is doing the work again: brown bread, brown pasta and brown rice are one way — swapping white for wholegrain — not three. Spread the answer across cereals, fruit and vegetables, and wholegrain swaps.")],
    "One flat list, evenly priced.",
    stem=Q1S))

plan_b, purch_b = heads(block(T, 'planning check stocks', 'Question 2'), ['planning check', 'purchasing buy in'])
waste = semis(plan_b, drop_prefix='planning') + semis(purch_b, drop_prefix='purchasing')
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-1-5', 'reducing-food-waste',
    '2024 OL Section B Q1(d)',
    'Describe four ways consumers can reduce food waste when planning meals and purchasing foods.',
    '4 ways @ 5 marks (graded 5:4:3:0); 1 reference to planning, 1 reference to purchasing, & 2 other points',
    20,
    [anyN('r-1', 'Describe four ways consumers can reduce food waste when planning meals and purchasing foods',
          20, 4, 5, waste[:14],
          "Four ways at 5 marks, and the distribution is fixed: at least one on planning, at least one on purchasing, then two of either. Four excellent planning points cannot reach 20. Note the unusual ladder, 5:4:3:0 — there is no 1 or 2, so a way that is recognisable at all is worth at least 3, and the top two marks come from describing how it stops food being thrown out.")],
    "The scheme groups the ways under the question's own two words and reserves a mark for each. The options are the individual ways rather than the two groups, so a student can see what actually counts; the reservation is carried in the notation and the contextNote, since the card model cannot enforce it.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "'Approximately 8% of Irish people are following a vegetarian based diet.' (Bord Bia, 2021)"
stor = semis(block(T, 'remove from wrapping; store in vegetable drawer', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-0-9', 'storing-fruit-vegetables',
    '2024 OL Section B Q2(c)',
    'Describe three guidelines to follow when storing fruit and vegetables in order to maintain their quality.',
    '3 ways @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Describe three guidelines to follow when storing fruit and vegetables', 12, 3, 4, stor,
          "Three guidelines at 4 marks. The ethylene point is the one that separates answers: bananas give off ethylene gas which ripens everything near them, and saying WHY earns the second 2 where \"store away from bananas\" alone does not. Several guidelines pull in opposite directions — some fruit at room temperature, vegetables in the fridge drawer — and that is the scheme's own list, not a contradiction.")],
    "One flat list, evenly priced.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "Ireland's food industry is globally recognised for producing high quality processed foods."
add = heads(block(T, 'colourings used to improve colour', '(b) Identify three major sectors'),
            ['colourings used', 'flavourings used', 'sweeteners natural', 'preservatives increase',
             'antioxidants prevent', 'physical conditioning agents', 'nutritive additives'])
cards.append(card(
    f'{P}-q3a', Y, L, 'home-economics-0-11', 'food-additives',
    '2024 OL Section B Q3(a)',
    'Describe four food additives used in the manufacture of processed foods.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Describe four food additives used in the manufacture of processed foods', 20, 4, 5, add,
          "Four additives at 5 marks, graded 5:3:0. Each option carries what the additive does AND the scheme's natural and artificial examples, because that is the shape of a 5: name it, say what it does, name one. Naming the class alone is a 3.")],
    "Seven classes of additive in the scheme, best four taken, each kept with its examples.",
    stem=Q3S))

sect = heads(block(T, 'dairy and ingredients milk', '(c) Evaluate the role of packaging'),
             ['dairy and ingredients', 'meat and livestock', 'beverages alcoholic',
              'seafood fresh fish', 'edible horticulture and cereals', 'prepared consumer foods'])
cards.append(card(
    f'{P}-q3b', Y, L, 'home-economics-0-11', 'irish-food-industry-sectors',
    '2024 OL Section B Q3(b)',
    'Identify three major sectors of the Irish food industry and give one example of a food product produced in each sector named.',
    '3 sectors @ 3 marks (graded 3:2:0); (1 food @ 2 marks (graded 2:1:0)) x3', 15,
    [anyN('r-1', 'Identify three major sectors of the Irish food industry and give one example from each',
          15, 3, 5, sect,
          "Three sectors at 5 marks each, and each 5 splits: 3 for naming the sector and 2 for a food product from it. Each option below carries its own products for exactly that reason — a product from the wrong sector does not earn the 2. Naming three sectors and no foods scores 9 of 15.")],
    "Six sectors in the scheme, best three taken. Sector and example are kept in one option because the scheme prices them together and the pairing is what is marked.",
    stem=Q3S))

pk = heads(block(T, 'suitability for purpose safe', 'Question 4'),
           ['suitability for purpose safe', 'environmental impact metal', 'as a source of consumer information displays'])
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-0-11', 'packaging-roles',
    '2024 OL Section B Q3(c)',
    'Evaluate the role of packaging in relation to each of the following: suitability for purpose; environmental impact; as a source of consumer information.',
    'suitability 1 role @ 5 marks (graded 5:3:0); environmental impact 1 role @ 5 marks (graded 5:3:0); consumer information 1 role @ 5 marks (graded 5:3:0)',
    15,
    [anyN('r-1', 'Suitability for purpose', 5, 1, 5, pk[0:1],
          "One point, 5 marks, graded 5:3:0. All three headings are compulsory and identically priced, so there is no choosing between them — an answer missing one caps at 10 of 15. Here the 5 comes from tying a property to the food it protects."),
     anyN('r-2', 'Environmental impact', 5, 1, 5, pk[1:2],
          "One point, 5 marks. The scheme runs material by material — metal non-renewable but recyclable, glass reusable, paper biodegradable, plastic neither — and naming the Re-Turn scheme is the most current thing on this list."),
     anyN('r-3', 'As a source of consumer information', 5, 1, 5, pk[2:3],
          "One point, 5 marks. These are the legal requirements a label must carry; naming two or three of them and saying what a shopper does with them is the 5.")],
    "Three compulsory headings at 5 marks each, so three rows rather than a choice of three from a pool.",
    stem=Q3S, tariff_kind='fixed'))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "'From time-to-time problems will arise with goods and services.' (www.ccpc.ie)"
inf = semis(block(T, 'amount of disposable income; personal preferences', '(b) Give an account of the Small Claims Court'))
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-1-2', 'factors-influencing-purchases',
    '2024 OL Section B Q4(a)',
    'Describe four factors that influence consumers when purchasing goods and services.',
    '4 factors @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Describe four factors that influence consumers when purchasing goods and services',
          20, 4, 5, inf[:14],
          "Four factors at 5 marks, graded 5:3:0 — named is 3, described is 5. Several of these are the same idea wearing different clothes (advertising, merchandising, packaging, current trends all pull on how a product is presented), so a spread across money, presentation, other people and after-sales reads as four distinct factors.")],
    "One flat list, taken in scheme order to the cap.",
    stem=Q4S))

scc = semis(block(T, 'part of the district court office', '(c) Explain how the Sale of Goods'))
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-2', 'small-claims-court',
    '2024 OL Section B Q4(b)',
    'Give an account of the Small Claims Court procedure used to resolve a consumer dispute over goods or services.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Give an account of the Small Claims Court procedure', 20, 4, 5, scc,
          "Four points at 5 marks. This is a procedure with numbers in it, and the numbers are marking content: EUR 25 to process the form, 15 days for the respondent to reply, 28 days to comply with a judgment, claims up to EUR 2,000. A step described without its figure sits at 3. Keep the order — application, registration, notice, reply, registrar, hearing — because an account out of sequence describes a process that could not run.")],
    "One ordered procedure, evenly priced.",
    stem=Q4S))

sog = semis(block(T, 'goods should be of merchantable quality', 'Question 5'))
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-2', 'sale-of-goods-1980-ol',
    '2024 OL Section B Q4(c)',
    'Explain how the Sale of Goods and Supply of Services Act 1980, protects the consumer.',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Explain how the Sale of Goods and Supply of Services Act 1980 protects the consumer',
          10, 2, 5, sog,
          "Two points at 5 marks, so both need explaining rather than listing. \"Explain\" is the gap between 3 and 5: merchantable quality is a 3, and what it entitles a consumer to when a kettle fails in a month is the 5. Repair, refund and replacement are one point between them.")],
    "One flat list, evenly priced.",
    stem=Q4S))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "'Caring for our family members, has always been a fundamental part of ethical living.' (www.familycarers.ie)"
fn = heads(block(T, 'physical provides basic needs', '(b) Explain how the state assists'),
           ['physical provides', 'emotional safe and secure', 'social teaches what', 'economic support children'])
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-0', 'functions-of-the-family-ol',
    '2024 OL Section B Q5(a)',
    'Describe each of the following functions of the family: physical; emotional; social; economic.',
    'physical 1 @ 5 marks; emotional 1 @ 5 marks; social 1 @ 5 marks; economic 1 @ 5 marks (each graded 5:3:0)',
    20,
    [anyN(f'r-{i+1}', name, 5, 1, 5, [fn[i]], note) for i, (name, note) in enumerate([
        ('Physical', "One point, 5 marks, graded 5:3:0. All four functions are compulsory and equally priced, so this is four short answers rather than a choice — leaving one out costs a flat 5. Physical is the concrete one: food, clothing, shelter, and protecting vulnerable members."),
        ('Emotional', "One point, 5 marks. The 5 is in the consequence — a child who can express feelings develops self-esteem and can form healthy relationships later. Stopping at \"the family loves the child\" is a 3."),
        ('Social', "One point, 5 marks. Socialisation is about learning what society accepts, and the scheme's mechanism is imitation and observation — naming how the child learns is what lifts this above a 3."),
        ('Economic', "One point, 5 marks. The specifics are worth having: support until 18, or 23 in full-time education, and the family as an economic unit that earns, pays tax and spends."),
    ])],
    "Four compulsory functions at 5 marks each, so four rows rather than a pooled choice.",
    stem=Q5S, tariff_kind='fixed'))

st = heads(block(T, 'physical social welfare allowances', '(c) Discuss three advantages'),
           ['physical social welfare', 'social Early Childhood', 'economic social welfare'])
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-0', 'state-support-family-functions',
    '2024 OL Section B Q5(b)',
    'Explain how the state assists the family in carrying out their physical, social and economic functions.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Explain how the state assists the family in carrying out their physical, social and economic functions',
          15, 3, 5, st,
          "Three points at 5 marks, one from each named function — the question fixes the three, so there is no choosing. These marks are won by naming the actual scheme: ECCE, Working Family Payment, Back to School Clothing and Footwear Allowance, the School Meals Programme, Tusla. \"The government gives money\" is a 3; naming the payment and saying which function it supports is the 5.")],
    "The three functions the question names, each carrying the scheme's own list of supports.",
    stem=Q5S, answer=3, of_parts=3, per_part=5))

adv = semis(block(T, 'children feel valued as they can express', None))
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-0', 'parent-child-relationship',
    '2024 OL Section B Q5(c)',
    'Discuss three advantages of a positive parent-child relationship within the family.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Discuss three advantages of a positive parent-child relationship within the family',
          15, 3, 5, adv,
          "Three advantages at 5 marks. Every point on this list runs the same way — something the child gains now that carries into later life — and the 5 is in that second half. Secure attachment now, healthy relationships later; emotional regulation now, coping under stress later. An advantage stated without its consequence is a 3.")],
    "One flat list, evenly priced.",
    stem=Q5S))

emit(cards)
