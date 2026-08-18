#!/usr/bin/env python3
"""Home Economics 2023 Ordinary Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2023, 'ordinary', 'he-2023-ol-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
if 'Section C' in T:
    T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "'Protein bars are a sector of the nutrition market that is rapidly expanding.' (www.tastetech.com) The table gives nutritional information per 100 g for three protein bars: Peanut & chocolate, Peanut & caramel, and Crunchy peanut butter."
cls = semis(block(T, 'high biological value/animal protein', '• dietary sources'))
src = semis(block(T, 'meat; fish; dairy products', '• functions in the body'))
fun = semis(block(T, 'growth; repair of body cells', '(c) Explain the importance of including water'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-5', 'protein-account-ol',
    '2023 OL Section B Q1(b)',
    'Give an account of protein under each of the following headings: classification; dietary sources; functions in the body.',
    'classification 2 classes @ 3 marks (graded 3:2:0); sources 3 @ 4 marks (graded 4:2:0); functions 2 @ 4 marks (graded 4:2:0)',
    26,
    [anyN('r-1', 'Classification', 6, 2, 3, cls,
          "Two classes at 3 marks. High biological value and low biological value is the pair the examiner expects, and the scheme accepts the animal/plant wording for the same idea. Simple and conjugated proteins is a different classification and also scores — but pick one system and stay in it."),
     anyN('r-2', 'Dietary sources', 12, 3, 4, src,
          "Three sources at 4 marks — the biggest strand at 12 marks. Naming the food is 2; saying whether it gives HBV or LBV protein is the other 2, and that link is what most answers leave out."),
     anyN('r-3', 'Functions in the body', 8, 2, 4, fun,
          "Two functions at 4 marks. Growth and repair is one function, not two — pair it with something structural (muscle, skin, cell membranes) or with the manufacturing functions (hormones, antibodies, enzymes) for a clearly separate second point.")],
    "26 marks split 6 + 12 + 8 across the three headings. The sources strand is worth double the classification, which is the opposite of how long each takes to write.",
    stem=Q1S, tariff_kind='fixed'))

wat = semis(block(T, 'regulates body temperature; component of all body cells', '(d) Discuss four guidelines'))
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-8', 'water-in-sport-diet',
    '2023 OL Section B Q1(c)',
    'Explain the importance of including water in the diet of a person who plays sport.',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Explain the importance of including water in the diet of a person who plays sport',
          10, 2, 5, wat,
          "Two points at 5 marks, so both need explaining. The question says \"who plays sport\", and the two functions that answer it directly are regulating body temperature and transporting nutrients and oxygen — a general list of what water does earns the 3 but not the 5.")],
    "One flat list, evenly priced.",
    stem=Q1S))

gl = semis(block(T, 'plan meals on a weekly basis', 'Question 2'))
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-1-1', 'reducing-household-food-costs',
    '2023 OL Section B Q1(d)',
    'Discuss four guidelines consumers should follow to reduce household costs when planning and purchasing food.',
    '4 guidelines @ 5 marks each (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss four guidelines consumers should follow to reduce household costs when planning and purchasing food',
          20, 4, 5, gl[:14],
          "Four guidelines at 5 marks, graded 5:3:0 — named is 3, discussed is 5. The list splits into planning ahead, buying cheaper alternatives and shopping smarter; four points spread across those reads as four guidelines, whereas own brands, special offers and discount supermarkets are three versions of one idea.")],
    "The scheme prints more guidelines than a card may show, taken in order to the cap.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "'17% of Irish consumers are now buying better quality beef.' (www.farmersjournal.ie)"
ten = semis(block(T, 'before slaughter inject with proteolytic enzymes', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-0-9', 'tenderising-meat',
    '2023 OL Section B Q2(c)',
    'Describe two different methods of tenderising meat.',
    '2 methods @ 5 marks each (graded 5:3:0)', 10,
    [anyN('r-1', 'Describe two different methods of tenderising meat', 10, 2, 5, ten,
          "Two methods at 5 marks. The scheme's list runs in time order — before slaughter, before cooking, during cooking — and picking from two different stages makes the \"different\" in the question obvious. Naming the method is 3; saying what it does to the connective tissue or muscle fibre is the 5.")],
    "One flat list, evenly priced.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "Safe food preparation and storage helps to prevent food waste in Irish households."
prep_b, stor_b = heads(block(T, 'preparation: avoid over-handling food', '(b) Set out the results of a study'),
                       ['preparation:', 'storage:'])
hyg = semis(prep_b, drop_prefix='preparation:')[:7] + semis(stor_b, drop_prefix='storage:')[:7]
cards.append(card(
    f'{P}-q3a', Y, L, 'home-economics-0-4', 'kitchen-hygiene-practices',
    '2023 OL Section B Q3(a)',
    'Discuss four kitchen hygiene practices that should be followed to ensure the safe preparation and storage of food.',
    '4 points @ 4 marks (graded 4:2:0); 1 reference to preparation, 1 reference to storage + 2 other points',
    16,
    [anyN('r-1', 'Discuss four kitchen hygiene practices for the safe preparation and storage of food',
          16, 4, 4, hyg,
          "Four practices at 4 marks, with a mark reserved on each of preparation and storage — four excellent storage points cannot reach 16. The storage temperatures are marking content: below 5C for perishables, -18C for frozen. Naming the practice is 2 and saying what it prevents (cross contamination, bacterial growth) is the other 2.")],
    "The scheme groups the practices under the question's own two words and reserves a mark for each; the options are the individual practices, taken evenly from both groups so neither is squeezed out by the cap.",
    stem=Q3S))

typ = semis(block(T, 'standard under the counter; larder fridge', '• guidelines for use'))
gu = semis(block(T, 'follow manufacturer’s instructions; avoid opening the door', '• care and cleaning'))
cc = semis(block(T, 'position away from heat source; defrost regularly', '(c) Describe how technology'))
cards.append(card(
    f'{P}-q3b', Y, L, 'home-economics-1-3', 'refrigeration-appliance-study',
    '2023 OL Section B Q3(b)',
    'Set out the results of a study you have carried out on a refrigeration appliance. Refer to: type of refrigeration appliance; guidelines for use; care and cleaning.',
    'type 1 @ 2 marks (graded 2:1:0); guidelines for use 3 @ 4 marks (graded 4:2:0); care and cleaning 3 @ 4 marks (graded 4:2:0)',
    26,
    [anyN('r-1', 'Type of refrigeration appliance', 2, 1, 2, typ,
          "Naming the type is worth only 2 marks of the 26 — but it is one word and it is the mark most often skipped in a question that otherwise reads as an essay."),
     anyN('r-2', 'Guidelines for use', 12, 3, 4, gu,
          "Three guidelines at 4 marks. These are about using the fridge day to day — what you put in, how, and how often you open it. Naming the guideline is 2; saying what it protects (temperature, cross contamination, food quality) is the other 2."),
     anyN('r-3', 'Care and cleaning', 12, 3, 4, cc,
          "Three guidelines at 4 marks, equal in weight to the use strand — so an answer heavy on use and light on cleaning gives away 12 marks. The bread soda and the door seal are the two most specific points here and the easiest to develop.")],
    "26 marks split 2 + 12 + 12 across the question's three bullets. The two big strands are equal, which is the thing to plan around.",
    stem=Q3S, tariff_kind='fixed'))

tech = semis(block(T, 'timers lower fuel bills; electrical appliances', 'Question 4'))
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-1-3', 'technology-meal-efficiency',
    '2023 OL Section B Q3(c)',
    'Describe how technology has contributed to greater efficiency when planning and preparing family meals.',
    '2 points @ 4 marks (graded 4:2:0)', 8,
    [anyN('r-1', 'Describe how technology has contributed to greater efficiency when planning and preparing family meals',
          8, 2, 4, tech,
          "Only two points at 4 marks — the smallest part in this Section B, so do not overspend on it. The question says planning AND preparing, and the scheme's list covers both: apps and online shopping for planning, appliances and induction hobs for preparing. One from each is the natural answer.")],
    "One flat list, evenly priced.",
    stem=Q3S))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "The family home is a base that provides comfort and security for family members."
_h = heads(block(T, 'family needs: young children', '(b) Describe three advantages of having household insurance'),
           ['family needs:', 'cost:', 'location:', 'trends in housing development:'])
home = (semis(_h[0], drop_prefix='family needs:')[:4] + semis(_h[1], drop_prefix='cost:')[:4]
        + semis(_h[2], drop_prefix='location:')[:3] + semis(_h[3], drop_prefix='trends in housing development:')[:3])
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-3-3', 'choosing-a-family-home',
    '2023 OL Section B Q4(a)',
    'Explain how the following factors influence the family’s choice when buying or renting a family home: family needs; cost; location; trends in housing development.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Explain how family needs, cost, location and trends in housing development influence the choice of a family home',
          20, 4, 5, home,
          "Four points at 5 marks, and the question names exactly four factors — so this is one point on each, not a free choice. Graded 5:3:0: naming the consideration is 3, and explaining how it changes which house a family ends up in is the 5. The BER rating appears under both cost and trends, and it is the most current point on the list.")],
    "Four factors named in the question, with the options taken evenly from each of the scheme's four lists so every factor stays visible under the option cap.",
    stem=Q4S))

ins = semis(block(T, 'provides peace of mind; protects assets', '(c) Outline three different ways consumers'))
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-1', 'household-insurance',
    '2023 OL Section B Q4(b)',
    'Describe three advantages of having household insurance.',
    '3 advantages @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Describe three advantages of having household insurance', 15, 3, 5, ins,
          "Three advantages at 5 marks. The list is short, so the marks come from developing rather than listing: peace of mind is a 3, and saying that a family can replace what a fire or burglary destroyed without borrowing is the 5. Public liability is the one most students have never heard of and it is worth knowing.")],
    "One flat list, evenly priced.",
    stem=Q4S))

pol = semis(block(T, 'use phosphate detergents; limit use of artificial fertilisers', 'Question 5'))
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-5', 'reducing-pollution',
    '2023 OL Section B Q4(c)',
    'Outline three different ways consumers can reduce pollution to protect the environment.',
    '3 ways @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Outline three different ways consumers can reduce pollution to protect the environment',
          15, 3, 5, pol[:14],
          "Three ways at 5 marks. \"Different\" matters again: recycle, reuse and buy second hand are one idea in three coats. Spread across energy, transport and waste instead. Naming the action is 3; naming the pollution it prevents is the 5.")],
    "The scheme prints a long list, taken in order to the cap.",
    stem=Q4S))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "'Ireland has officially been recognised as one of the best places to grow old.' (WHO)"
_r = heads(block(T, 'roles: spending time with their children', '(b) (i) Identify two causes of conflict'),
           ['roles:', 'responsibility:'])
older = semis(_r[0], drop_prefix='roles:') + semis(_r[1], drop_prefix='responsibility:')
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-3', 'older-people-roles',
    '2023 OL Section B Q5(a)',
    'Discuss four roles and responsibilities of older people within the family.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Discuss four roles and responsibilities of older people within the family', 20, 4, 5, older[:14],
          "Four points at 5 marks, graded 5:3:0. The scheme divides them into roles (what an older person does — childcare, financial help, home maintenance) and responsibilities (what they pass on — respect, values, being a role model). Taking from both halves makes it easier to reach four genuinely different points.")],
    "The scheme's two groups flattened into individual points, since the question asks for four across both rather than a fixed split.",
    stem=Q5S))

cau = semis(block(T, 'teenagers question rules and authority', '(ii) Explain two ways of dealing'))
way = semis(block(T, 'good communication avoids confrontation', '(c) Outline two reasons why it is important'))
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-1', 'teenage-adult-conflict',
    '2023 OL Section B Q5(b)',
    'Identify two causes of conflict between teenagers and adults, and explain two ways of dealing with this conflict.',
    'causes 2 @ 5 marks (graded 5:3:0); ways 2 @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Identify two causes of conflict between teenagers and adults', 10, 2, 5, cau[:14],
          "Two causes at 5 marks. \"Identify\" reads like a one-word instruction but it is priced at 5, so the cause still has to be explained — social media use is a 3, and what it is actually a conflict about (time, privacy, trust) is the 5."),
     anyN('r-2', 'Explain two ways of dealing with this conflict', 10, 2, 5, way,
          "Two ways at 5 marks. Communication and boundaries are the two the scheme leads with, and \"do not ignore conflict\" is a point in its own right. Match the ways to the causes you gave — an answer where the solutions do not address the stated problems reads as two unconnected lists.")],
    "The question's two halves are priced identically at 10 marks each, so two rows.",
    stem=Q5S, tariff_kind='fixed'))

wil = semis(block(T, 'person’s wishes about the distribution of their estate', None))
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-3', 'making-a-will',
    '2023 OL Section B Q5(c)',
    'Outline two reasons why it is important for an older person to make a will.',
    '2 reasons @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Outline two reasons why it is important for an older person to make a will', 10, 2, 5, wil,
          "Two reasons at 5 marks. The strongest point in the scheme is the consequence of NOT making one — a sizable portion of the estate going to the state — because it explains itself. Inheritance tax and guardianship of children are the two most specific of the rest.")],
    "One flat list, evenly priced.",
    stem=Q5S))

emit(cards)
