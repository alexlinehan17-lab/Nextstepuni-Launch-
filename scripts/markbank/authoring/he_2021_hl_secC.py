"""2021 Higher Level, Section C."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2021, 'higher')
SEC = tidy(T[29684:56679])
Y, LV, PFX, CAP = 2021, 'higher', 'he-2021-hl-sc-', 14
cards, held = [], []
def C(*a, **k):
    k.setdefault('section', 'C'); return card(*a, **k)
def bundle(h, prefix='', n=None):
    seg = semis(h, prefix); return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 – Home Design', 'Elective 2 – Textiles')
E1a = block(E1, '1.(a) A well designed home', '1.(b) ‘Lighting')

h_loc, h_sty = heads(block(E1a, 'Location: urban or rural setting', '(ii) Discuss the following factors'),
                     ['Location: urban or rural setting', 'House style: personal preference'])
o_loc, o_sty = semis(h_loc, 'Location:')[:CAP], semis(h_sty, 'House style:')[:CAP]
cards.append(C(
    PFX+'q1ai', Y, LV, 'home-economics-3-3', 'location-and-house-style',
    '2021 HL Section C E1 Q1(a)(i)',
    'Explain the importance of location and house style when building a new home.',
    '4 points @ 4 marks (graded 4:2:0) - 1 reference to location, 1 reference to house style + 2 other points', 16,
    [anyN('r-1', 'One reference to location', 4, 1, 4, o_loc,
          'One point at 4 marks, and the scheme requires at least one. Location is everything outside the house - what it is near, which way the site faces, whether services and drainage are there, and what the local authority will allow.'),
     anyN('r-2', 'One reference to house style', 4, 1, 4, o_sty,
          'One point at 4 marks, also required. Style is the house itself - storeys and type, enough space for the family now and later, and whether it fits the surrounding area and local materials.'),
     anyN('r-3', 'Two further points, from either', 8, 2, 4, (o_loc + o_sty)[:CAP],
          'Two further points at 4 marks each, from either strand - "1 reference to location, 1 reference to house style + 2 other points". Develop whichever you know better rather than reaching for a weak fourth idea.')],
    'Fixed: the scheme requires one point on each strand, then floats the remaining 8 marks across both. Modelled as three rows so the two compulsory points cannot be lost.',
    stem='A well designed home should have a positive impact on people’s lives.',
    tariff_kind='fixed'))

DES = ['Initial and maintenance costs –', 'Technological developments –', 'Energy efficiency -']
h_cost, h_tech, h_eff = heads(block(E1a, 'Initial and maintenance costs –', '(iii) Outline the procedure'), DES)
cards.append(C(
    PFX+'q1aii', Y, LV, 'home-economics-3-3', 'factors-influencing-house-design',
    '2021 HL Section C E1 Q1(a)(ii)',
    'Discuss the following factors that influence house design/construction: initial and/or maintenance costs; technological developments; energy efficiency.',
    '2 points @ 4 marks (graded 4:2:0) x 3', 24,
    [anyN('r-1', 'Initial and/or maintenance costs', 8, 2, 4, semis(h_cost, 'Initial and maintenance costs –')[:CAP],
          'Two points at 4 marks. The idea worth writing is that the two costs pull against each other - spending more at the start on solar panels or underfloor heating reduces what the house costs to run for the next thirty years.'),
     anyN('r-2', 'Technological developments', 8, 2, 4, semis(h_tech, 'Technological developments –')[:CAP],
          'Two points at 4 marks. The scheme runs from how the house is designed (CAD, virtual reality tours) to what is built into it (sensor lighting, zoned heating, monitored security, smart appliances). One of each shows range.'),
     anyN('r-3', 'Energy efficiency', 8, 2, 4, semis(h_eff, 'Energy efficiency -')[:CAP],
          'Two points at 4 marks. Keeping heat in (insulation, low-emissivity glazing) and controlling how it is used (zoned heating, thermostats, timers) are the two halves - renewable sources are the third.')],
    'Fixed: the question names three factors and prices them identically at 8 marks each.',
    stem='A well designed home should have a positive impact on people’s lives.',
    tariff_kind='fixed'))

ch = block(E1a, '5 points @ 2 marks (graded 2:1:0) Pre-planning meeting')
cards.append(C(
    PFX+'q1aiii', Y, LV, 'home-economics-3-3', 'obtaining-full-planning-permission',
    '2021 HL Section C E1 Q1(a)(iii)',
    'Outline the procedure involved in obtaining full planning permission to build a house.',
    '5 points @ 2 marks (graded 2:1:0)', 10,
    [anyN('r-1', 'Procedure for obtaining full planning permission', 10, 5, 2,
          semis(ch, '5 points @ 2 marks (graded 2:1:0)')[:CAP],
          'Five points at 2 marks - a procedure, so write it in order: pre-planning meeting, notice in the local paper, application and fee to the planning authority, site notice erected, public and site inspection, then permission granted or refused with reasons.')],
    'One flat list, taken in scheme order - which is also the order the procedure happens in.',
    stem='A well designed home should have a positive impact on people’s lives.'))

# ------------------------------------------------------------------- 1.(b)
E1b = block(E1, '1.(b) ‘Lighting', 'or 1.(c) Water covers')
LGT = ['Reflected –', 'Refracted –', 'Diffused –', 'Absorbed –', 'Dispersed –']
ch = block(E1b, 'Reflected – rays of light bounce', '(ii) Identify and evaluate two contemporary')
cards.append(C(
    PFX+'q1bi', Y, LV, 'home-economics-3-5', 'properties-of-light-in-the-home',
    '2021 HL Section C E1 Q1(b)(i)',
    'Discuss three properties of light and in each case give an example of the application of each in the home.',
    '3 properties @ 6 marks (graded 6:4:2:0)', 18,
    [anyN('r-1', 'Properties of light and their application in the home', 18, 3, 6,
          [f'{a.rstrip(" –")} - {bundle(h, a)}' for h, a in zip(heads(ch, LGT), LGT)][:CAP],
          'Three properties at 6 marks, graded 6:4:2:0 - the long ladder rewards a partial answer, so attempt all three. Each needs the physics AND the home example: light bounces off a mirror or white ceiling, bends through glass bricks, scatters through an opaque shade, is swallowed by dark matt walls, or splits into colours in a crystal chandelier.')],
    'One option per named property, each carrying that property’s own explanation and example, because the scheme groups its marking points under five headings and prices three.',
    stem='‘Lighting isn’t just a practical necessity. It’s a style accessory, too.’ (www.ikea.com)'))

ch = block(E1b, 'Sensor and motion activated lights')
cards.append(C(
    PFX+'q1bii', Y, LV, 'home-economics-3-5', 'contemporary-lighting-technology',
    '2021 HL Section C E1 Q1(b)(ii)',
    'Identify and evaluate two contemporary developments in lighting technology.',
    'Name 2 marks (graded 2:0) x 2; evaluate 1 point @ 4 marks (graded 4:2:0) x 2', 12,
    [anyN('r-1', 'Name of the lighting development', 4, 2, 2, semis(ch)[:CAP],
          'Two developments at 2 marks each, graded 2:0. The scheme accepts a long list, but pick two you can then evaluate - sensor lighting and smart remote-controlled lighting are the easiest to say something real about.'),
     anyN('r-2', 'Evaluation of the developments named', 8, 2, 4, semis(ch)[:CAP],
          'One evaluation per development at 4 marks - two thirds of the marks. The scheme names the technologies only, so the judgement is entirely yours: what it does for convenience, safety or the electricity bill, and what it costs to install.')],
    'Fixed: naming is priced at 4 across the two developments and the evaluation at 8. Both rows draw on the same list, because the scheme names the developments without evaluating them.',
    stem='‘Lighting isn’t just a practical necessity. It’s a style accessory, too.’ (www.ikea.com)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 1.(c)
E1c = block(E1, 'or 1.(c) Water covers')
h_urb, h_rur = heads(block(E1c, 'Urban areas: public supply', 'Stop cock -'),
                     ['Urban areas: public supply', 'Rural areas: public supply'])
ch_sc = block(E1c, 'Stop cock - a valve found', 'Storage tank/cistern –')
ch_st = block(E1c, 'Storage tank/cistern – located in the attic', '(ii) Identify inefficient uses')
cards.append(C(
    PFX+'q1ci', Y, LV, 'home-economics-3-5', 'water-supply-and-storage-in-the-home',
    '2021 HL Section C E1 Q1(c)(i)',
    'Explain how water is supplied to and stored in the home. Refer to: urban or rural supply; stop cock; storage tank/cistern.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'Urban or rural supply', 6, 2, 3,
          (semis(h_urb, 'Urban areas:') + semis(h_rur, 'Rural areas:'))[:CAP],
          'Two points at 3 marks, and either supply is accepted. Urban is a chain from the reservoir: mains, service pipe, external stopcock, then the kitchen sink for drinking water and a branch to the attic tank. Rural is a well or spring, lined against contamination, tested and pumped in.'),
     anyN('r-2', 'Stop cock', 6, 2, 3, semis(ch_sc, 'Stop cock -')[:CAP],
          'Two points at 3 marks. Two things to say: where it is (on the service pipe outside, or under the kitchen sink) and what it does (shuts the supply off if there is a problem).'),
     anyN('r-3', 'Storage tank/cistern', 6, 2, 3, semis(ch_st, 'Storage tank/cistern –')[:CAP],
          'Two points at 3 marks. The height is the point - it sits in the attic so gravity gives the pressure, a ball valve keeps the level right, and it feeds the cold taps, toilets and hot press.')],
    'Fixed: the question names three strands and prices them identically at 6 marks each.',
    stem='Water covers 71% of the planet but only 1% is available to us as drinking water. (Irish Water)',
    tariff_kind='fixed'))

ch_in = block(E1c, 'Inefficient uses of water –', 'Strategies for conserving')
ch_str = block(E1c, 'Strategies for conserving and managing water -')
cards.append(C(
    PFX+'q1cii', Y, LV, 'home-economics-3-6', 'conserving-water-in-the-home',
    '2021 HL Section C E1 Q1(c)(ii)',
    'Identify inefficient uses of water in the home and suggest strategies for conserving and managing this resource.',
    'inefficient uses 2 @ 2 marks (graded 2:0); strategies 2 @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Inefficient uses of water in the home', 4, 2, 2, semis(ch_in, 'Inefficient uses of water –')[:CAP],
          'Two at 2 marks, graded 2:0. The scheme prints only three bare words - toilets, appliances, taps - so identify them and move on. The marks are in the next row.'),
     anyN('r-2', 'Strategies for conserving and managing water', 8, 2, 4, semis(ch_str, 'Strategies for conserving and managing water -')[:CAP],
          'Two strategies at 4 marks - two thirds of the marks. Match the strategy to the waste you identified, and use the scheme’s own figure if you can: a leaking tap wastes up to a litre an hour. Dual flush, full loads, and a shower instead of a bath are the strongest.')],
    'Fixed: identifying the waste is priced at 4 and the strategies at 8.',
    stem='Water covers 71% of the planet but only 1% is available to us as drinking water. (Irish Water)',
    tariff_kind='fixed'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 – Textiles', 'Elective 3 – Social Studies')
E2a = block(E2, '2.(a) Athleisure wear is a way', 'and 2.(b)')

ch = block(E2a, '3 points @ 5 marks (graded 5:3:0) Comfort', '(ii) Outline the steps')
cards.append(C(
    PFX+'q2ai', Y, LV, 'home-economics-3-8', 'athleisure-wear-as-a-wardrobe-staple',
    '2021 HL Section C E2 Q2(a)(i)',
    'Evaluate the suitability of athleisure wear as a wardrobe staple.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Suitability of athleisure wear as a wardrobe staple', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0. The scheme names bare qualities, so the mark is in what you add - a wardrobe staple is worn often and in many settings, so versatility, durability and comfort matter more than the trend. Say why each one makes it wearable day to day.')],
    'One flat list, taken in order to the cap. The scheme names the qualities only, so the evaluation is entirely the candidate’s.',
    stem='Athleisure wear is a way of dressing that combines sportswear with ready-to-wear.'))

ch = block(E2a, '5 steps @ 2 marks (graded 2:0) Define the task')
cards.append(C(
    PFX+'q2aii', Y, LV, 'home-economics-3-8', 'steps-of-the-design-process',
    '2021 HL Section C E2 Q2(a)(ii)',
    'Outline the steps of the design process when constructing a garment.',
    '5 steps @ 2 marks (graded 2:0)', 10,
    [anyN('r-1', 'Steps of the design process', 10, 5, 2,
          semis(ch, '5 steps @ 2 marks (graded 2:0)')[:CAP],
          'Five steps at 2 marks, graded 2:0 - each is all or nothing, and they are in order. Define the task, analyse the brief, research, generate ideas, present them, refine, make, evaluate. Learn the sequence and this is ten marks in a minute.')],
    'One flat list, taken in scheme order - which is the order of the design process itself.',
    stem='Athleisure wear is a way of dressing that combines sportswear with ready-to-wear.'))

# ------------------------------------------------------------------- 2.(b)
E2b = block(E2, 'and 2.(b) The sustainability of natural fibres', 'or 2.(c)')
FAB = ['Cotton Fibre production:', 'Linen Fibre production:', 'Wool Fibre production:', 'Silk Fibre production:']
fab_chunks = heads(block(E2b, 'Cotton Fibre production:'), FAB)
def verbatim(chunk, label):
    """The raw slice, label stripped, trailing 'etc.' trimmed.

    Not bundle(): semis() strips 'etc.' from the END of every segment, and wool's
    first segment ends "sheep, goats, llamas etc". Rejoining therefore dropped an
    'etc' from the MIDDLE of the marking point and broke contiguity with the
    scheme. Slicing the raw text and trimming only the tail keeps it verbatim."""
    t = tidy(chunk)
    if t.startswith(label):
        t = tidy(t[len(label):])
    return tidy(t.rstrip().rstrip('.').rstrip().removesuffix('etc').rstrip().rstrip(';'))

prod, props, uses = [], [], []
for h, a in zip(fab_chunks, FAB):
    name = a.split(' ')[0]
    ip, iu = h.find('Properties:'), h.find('Uses:')
    prod.append(f'{name} Fibre production: {verbatim(h[:ip], a)}')
    props.append(verbatim(h[ip:iu], 'Properties:'))
    uses.append(verbatim(h[iu:], 'Uses:'))
cards.append(C(
    PFX+'q2b', Y, LV, 'home-economics-3-7', 'profile-of-a-natural-fibre-fabric',
    '2021 HL Section C E2 Q2(b)',
    'Write a profile of one fabric manufactured from natural fibres. Refer to: fibre production; fabric properties; uses.',
    'name 3 marks (graded 3:0); fibre production 3 points @ 2 marks; properties 3 @ 1 mark; uses 3 @ 1 mark', 15,
    [anyN('r-1', 'Name of the fabric', 3, 1, 3, ['Cotton', 'Linen', 'Wool', 'Silk'],
          'Name one, 3 marks, graded 3:0 - all or nothing for a single word. Cotton and wool have the fullest production accounts in the scheme and are the easiest to describe end to end.'),
     anyN('r-2', 'Fibre production', 6, 3, 2, prod[:CAP],
          'Three points at 2 marks - the biggest row. Production is a sequence from plant or animal to yarn, so tell it in order: where the fibre comes from, how it is harvested, how it is cleaned and separated, how it is spun. Read the option for the fabric you named.'),
     anyN('r-3', 'Fabric properties', 3, 3, 1, props[:CAP],
          'Three properties at 1 mark each, graded 1:0 - single words, no development needed. Listed in the same order as the fabrics above: cotton, linen, wool, silk. Include a weakness as well as a strength; the scheme lists both.'),
     anyN('r-4', 'Uses', 3, 3, 1, uses[:CAP],
          'Three uses at 1 mark each, graded 1:0. Again in fabric order. Easy marks - name garments or household items, and make sure they match the fabric you profiled.')],
    'Fixed: the question prices four strands at 3, 6, 3 and 3. Production carries the fabric name because the scheme prints it adjacent; properties and uses do not, so those options are listed in the same fabric order instead.',
    stem='The sustainability of natural fibres has led to an upsurge in their use.',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 2.(c)
E2c = block(E2, 'or 2.(c) The design of fashion')
ch = block(E2c, '1 point @ 6 marks (graded 6:3:0) Modesty', '(ii) Analyse the impact')
cards.append(C(
    PFX+'q2ci', Y, LV, 'home-economics-3-8', 'function-and-choice-of-clothing',
    '2021 HL Section C E2 Q2(c)(i)',
    'Explain how the choice of clothing is determined by its function.',
    '1 point @ 6 marks (graded 6:3:0)', 6,
    [anyN('r-1', 'How function determines the choice of clothing', 6, 1, 6,
          semis(ch, '1 point @ 6 marks (graded 6:3:0)')[:CAP],
          'One point at 6 marks, graded 6:3:0 - so 6 or 3, and a bare word is the 3. Take one function and develop it properly: protection from weather means warmth, waterproofing and covering, and it changes what you reach for in January versus July.')],
    'One flat list, taken in order to the cap. The scheme names the functions only, so the explanation is entirely the candidate’s.',
    stem='The design of fashion can be influenced by cultural, historical and social factors.'))

ch = block(E2c, '3 points @ 3 marks (graded 3:2:0) Public figures')
cards.append(C(
    PFX+'q2cii', Y, LV, 'home-economics-3-8', 'social-influences-on-clothing-design',
    '2021 HL Section C E2 Q2(c)(ii)',
    'Analyse the impact of social influences on the design of clothing.',
    '3 points @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Social influences on the design of clothing', 9, 3, 3,
          semis(ch, '3 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Three influences at 3 marks, graded 3:2:0. Analyse means say how the influence reaches the clothes - an influencer wears a piece and demand follows, environmental concern pushes designers toward recycled fabric, travel and music carry styles between cultures.')],
    'One flat list, taken in order to the cap.',
    stem='The design of fashion can be influenced by cultural, historical and social factors.'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 – Social Studies', 'Question 4 – Core')
E3a = block(E3, '3.(a) ‘Life on a low income', '3.(b) People in work')

ch = block(E3a, 'Poverty: being without adequate food', '(ii) In relation to poverty')
cards.append(C(
    PFX+'q3ai', Y, LV, 'home-economics-3-9', 'defining-poverty-hl',
    '2021 HL Section C E3 Q3(a)(i)',
    # The paper says just "Define poverty.", which the build rejects as too
    # short to stand alone. Same question, phrased so the card reads on its own.
    'Define what is meant by poverty.',
    '2 points @ 4 marks (graded 4:2:0)', 8,
    [anyN('r-1', 'Definition of poverty', 8, 2, 4, semis(ch, 'Poverty:')[:CAP],
          'Two points at 4 marks, graded 4:2:0. The scheme prints two ideas and both are worth having: not being able to afford basic needs, and being excluded from what Irish society treats as a normal standard of living. The second is what lifts it above "having no money".')],
    'One flat list, taken in order to the cap.',
    stem='‘Life on a low income is the norm for a large proportion of our society.’ (Poverty Focus, Social Justice Ireland, 2020)'))

POV = ['Relative poverty:', 'Poverty line:', 'Poverty trap:']
h_rel, h_line, h_trap = heads(block(E3a, 'Relative poverty: people living below', '(iii) Discuss the extent'), POV)
cards.append(C(
    PFX+'q3aii', Y, LV, 'home-economics-3-9', 'relative-poverty-poverty-line-poverty-trap',
    '2021 HL Section C E3 Q3(a)(ii)',
    'In relation to poverty explain each of the following: relative poverty; the poverty line; the poverty trap.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'Relative poverty', 6, 2, 3, semis(h_rel, 'Relative poverty:')[:CAP],
          'Two points at 3 marks. Relative is measured against everyone else - below what society treats as a basic standard, and shut out of activities other people take for granted.'),
     anyN('r-2', 'The poverty line', 6, 2, 3, semis(h_line, 'Poverty line:')[:CAP],
          'Two points at 3 marks. A figure, not a condition: the minimum income reckoned necessary to maintain a basic standard of living, enough for food, clothing and shelter.'),
     anyN('r-3', 'The poverty trap', 6, 2, 3, semis(h_trap, 'Poverty trap:')[:CAP],
          'Two points at 3 marks. The trap is the disincentive - benefits are lost on returning to work, and a low-paid job can leave a household worse off than the payments it replaced.')],
    'Fixed: the question names three terms and prices them identically at 6 marks each.',
    stem='‘Life on a low income is the norm for a large proportion of our society.’ (Poverty Focus, Social Justice Ireland, 2020)',
    tariff_kind='fixed'))

h_ext, h_dist = heads(block(E3a, 'Extent: the number of people below', '(iv) Name and give details'),
                      ['Extent: the number of people below', 'Distribution: groups at risk'])
o_ext, o_dist = semis(h_ext, 'Extent:')[:CAP], semis(h_dist, 'Distribution:')[:CAP]
cards.append(C(
    PFX+'q3aiii', Y, LV, 'home-economics-3-9', 'extent-and-distribution-of-poverty',
    '2021 HL Section C E3 Q3(a)(iii)',
    'Discuss the extent and distribution of poverty in Ireland today.',
    '3 points @ 4 marks (graded 4:2:0) - 1 reference to extent, 1 reference to distribution + 1 other point', 12,
    [anyN('r-1', 'One reference to extent', 4, 1, 4, o_ext,
          'One point at 4 marks, and the scheme requires at least one. Extent is how many - over 20% of households below the poverty line, one in four children, and one of the highest rates in Europe. A figure is worth more than a general statement.'),
     anyN('r-2', 'One reference to distribution', 4, 1, 4, o_dist,
          'One point at 4 marks, also required. Distribution is who - the scheme lists the at-risk groups: women over 65, lone parents, the unemployed, low-paid workers, people with disabilities, Travellers and ethnic minorities.'),
     anyN('r-3', 'One further point, from either', 4, 1, 4, (o_ext + o_dist)[:CAP],
          'One further point at 4 marks, from either strand. The historical sweep in the extent list - recession in the 1980s, the Celtic Tiger, the housing costs of the 2000s, then COVID - is the easiest place to find a third.')],
    'Fixed: the scheme requires one point on each strand, then floats the remaining 4 marks across both. Modelled as three rows so the two compulsory points cannot be lost.',
    stem='‘Life on a low income is the norm for a large proportion of our society.’ (Poverty Focus, Social Justice Ireland, 2020)',
    tariff_kind='fixed'))

ch = block(E3a, 'State pension (non-contributory)')
cards.append(C(
    PFX+'q3aiv', Y, LV, 'home-economics-3-9', 'social-welfare-supports-for-poverty',
    '2021 HL Section C E3 Q3(a)(iv)',
    'Name and give details of one social welfare assistance/benefit available to people who are experiencing poverty.',
    'Name 4 marks (graded 4:2:0); details 2 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Name of the social welfare assistance/benefit', 4, 1, 4, semis(ch)[:CAP],
          'Name one, 4 marks. Eight are accepted. Name the payment exactly - "jobseeker’s allowance", not "the dole" - and pick one you can then describe for the other 8 marks.'),
     anyN('r-2', 'Details of the payment', 8, 2, 4, semis(ch)[:CAP],
          'Two details at 4 marks - two thirds of the marks, and the scheme prints no detail for any of them, so this is entirely yours. Say who qualifies, what it is for, and whether it is means tested. Working family payment and child benefit are the easiest to describe.')],
    'Fixed: naming is priced at 4 and the details at 8. Both rows draw on the same list, because the scheme names the payments without describing them.',
    stem='‘Life on a low income is the norm for a large proportion of our society.’ (Poverty Focus, Social Justice Ireland, 2020)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 3.(b)
E3b = block(E3, '3.(b) People in work', 'or 3.(c) 42%')
ATT = ['Social group:', 'Education:', 'Extrinsic satisfaction:', 'Intrinsic satisfaction:',
       'Work ethic:', 'Personal identity:', 'Working conditions:', 'Social contact:']
ch = block(E3b, 'Social group: children from higher socio-economic', '(ii) Discuss giving examples')
cards.append(C(
    PFX+'q3bi', Y, LV, 'home-economics-2-2', 'factors-affecting-attitude-to-work',
    '2021 HL Section C E3 Q3(b)(i)',
    'Identify and elaborate on the factors that affect an individual’s attitude to work.',
    '3 factors @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors affecting an individual’s attitude to work', 15, 3, 5,
          [f'{a.rstrip(":")} - {bundle(h, a)}' for h, a in zip(heads(ch, ATT), ATT)][:CAP],
          'Three factors at 5 marks, graded 5:3:0. Identify AND elaborate - the name is the 3, the elaboration is the 5. The pair worth knowing is extrinsic against intrinsic satisfaction: one is working for what the wage buys, the other is the work itself giving pride and status.')],
    'One option per named factor, each carrying that factor’s own detail, because the scheme groups its marking points under eight headings and prices three.',
    stem='People in work, paid or unpaid, tend to enjoy happier and healthier lives.'))

ch = block(E3b, '3 points @ 5 marks (graded 5:3:0) Provides range of services quickly')
cards.append(C(
    PFX+'q3bii', Y, LV, 'home-economics-3-11', 'community-benefits-of-volunteering',
    '2021 HL Section C E3 Q3(b)(ii)',
    'Discuss, giving examples, how a community can benefit from the work of volunteers.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'How a community benefits from volunteers', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0 - and the question says "giving examples", so name one: St Vincent de Paul for a personal local service, tidy towns for community spirit. The scheme supplies both. Keep the benefit at community level, not the volunteer’s.')],
    'One flat list, taken in order to the cap.',
    stem='People in work, paid or unpaid, tend to enjoy happier and healthier lives.'))

# ------------------------------------------------------------------- 3.(c)
E3c = block(E3, 'or 3.(c) 42%')
ch = block(E3c, 'Both parents now generally involved', '(ii) Discuss how improvements')
cards.append(C(
    PFX+'q3ci', Y, LV, 'home-economics-2-0', 'distribution-of-work-and-childcare-in-families',
    '2021 HL Section C E3 Q3(c)(i)',
    'Explain the importance of the distribution of work tasks and childcare responsibilities in families.',
    '3 points @ 5 marks (graded 5:3:0) - 1 reference to work tasks, 1 reference to childcare + 1 other point', 15,
    [anyN('r-1', 'Importance of distributing work tasks and childcare', 15, 3, 5,
          semis(ch)[:CAP],
          'Three points at 5 marks, and the scheme wants at least one on work tasks and one on childcare. Sharing childcare builds closer parent-child relationships and cuts role overload; sharing chores teaches children responsibility and shows gender equity by example.')],
    'One flat list pooling both strands, because the scheme prints its marking points as a single list even though it asks for a reference to each.',
    stem='42% of people who are working from home said that “managing the boundary between work and home life was very difficult”. (Irish Independent, 2020)'))

ch = block(E3c, 'Pre-schools /Naíonraí')
cards.append(C(
    PFX+'q3cii', Y, LV, 'home-economics-3-10', 'improvements-in-education-and-family-life',
    '2021 HL Section C E3 Q3(c)(ii)',
    'Discuss how improvements in the provision of education has impacted on family life.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'How improvements in education have impacted family life', 15, 3, 5,
          semis(ch)[:CAP],
          'Three points at 5 marks, graded 5:3:0. The scheme runs across the whole life course - pre-schools and homework clubs freeing parents to work, SNAs and autism units supporting children with additional needs, and free fees, grants, PLCs and distance learning opening third level to adults. Take one from each stage.')],
    'One flat list, taken in order to the cap.',
    stem='42% of people who are working from home said that “managing the boundary between work and home life was very difficult”. (Irish Independent, 2020)'))

# ------------------------------------------------------------- Question 4 Core
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) Ireland has a population', 'and 4.(b)')

MILK = ['Protein: 3.5%', 'Fat: 0.2% in skimmed', 'Carbohydrate: 4-5% lactose', 'Vitamins: 0.3%',
        'Minerals: 0.7%', 'Water: 87%']
ch = block(Q4a, 'Protein: 3.5%', '(ii) Describe one process')
cards.append(C(
    PFX+'q4ai', Y, LV, 'home-economics-0-9', 'nutritional-significance-of-milk',
    '2021 HL Section C Q4(a)(i) - Core',
    'Discuss the nutritional significance of milk in the diet of young children.',
    '5 points @ 4 marks (graded 4:3:2:1:0)', 20,
    [anyN('r-1', 'Nutritional significance of milk for young children', 20, 5, 4,
          [f'{a.split(":")[0]} - {bundle(h, a.split(":")[0] + ":")}' for h, a in zip(heads(ch, MILK), MILK)][:CAP],
          'Five points at 4 marks, graded 4:3:2:1:0 - the long ladder means a partial answer still scores, so write something on all five. Keep tying it back to young children: HBV protein for growth, full fat for energy and vitamins A and D, calcium and phosphorus for bones and teeth. Milk’s weakness - almost no iron - is worth naming too.')],
    'One option per nutrient, each carrying that nutrient’s own figure and function, because the scheme groups its marking points under six nutrient headings and prices five points.',
    stem='Ireland has a population of less than five million people, yet it produces enough dairy to feed multiples of that. (Dairy Sector Profile, Bord Bia)'))

PROC = ['Pasteurisation Milk is homogenised', 'Sterilisation Milk is homogenised', 'UHT Milk is heated',
        'Evaporated Milk is homogenised', 'Dried Milk is homogenised', 'Condensed Milk is homogenised']
proc_chunks = heads(block(Q4a, 'Pasteurisation Milk is homogenised', 'Packaging: type:'), PROC)
ch_pack = block(Q4a, 'Packaging: type:', 'Labelling:')
ch_lab = block(Q4a, 'Labelling: type of milk', '(iii) Outline the measures')
cards.append(C(
    PFX+'q4aii', Y, LV, 'home-economics-0-9', 'processing-milk-to-extend-shelf-life',
    '2021 HL Section C Q4(a)(ii) - Core',
    'Describe one process used by manufacturers to extend the shelf life of milk. Refer to: name of process; how the process is carried out; packaging and labelling.',
    'name 2 marks (graded 2:0); process 4 points @ 2 marks; packaging and labelling 8 points @ 1 mark (4 packaging, 4 labelling)', 18,
    [anyN('r-1', 'Name of the process', 2, 1, 2,
          ['Pasteurisation', 'Sterilisation', 'UHT', 'Evaporated', 'Dried', 'Condensed'],
          'Name one, 2 marks, graded 2:0. Six are offered. Pasteurisation is the one most students can give temperatures for, and the temperatures are where the next row’s marks are.'),
     anyN('r-2', 'How the process is carried out', 8, 4, 2,
          [f'{a.split(" ")[0]} - {bundle(h, a.split(" ")[0])}' for h, a in zip(proc_chunks, PROC)][:CAP],
          'Four points at 2 marks - the biggest row, and it wants numbers. Each process is a sequence of temperature, time and what happens after: pasteurisation is 72-75°C for 15-25 seconds then cooled rapidly to 10°C. Learn one process precisely rather than six vaguely.'),
     anyN('r-3', 'Packaging', 4, 4, 1, semis(ch_pack, 'Packaging: type:')[:CAP],
          'Four references at 1 mark each, graded 1:0 - single words. Glass bottles, metal cans, plastic cartons, waxed cardboard. Match the packaging to the process you named.'),
     anyN('r-4', 'Labelling', 4, 4, 1, semis(ch_lab, 'Labelling:')[:CAP],
          'Four references at 1 mark each, graded 1:0. Type of milk, brand, quantity, nutritional information, date stamp, storage instructions. Eight marks across this row and the last for naming things off a carton.')],
    'Fixed: the question prices four strands at 2, 8, 4 and 4. The process row carries one option per process, because the four points must match whichever was named.',
    stem='Ireland has a population of less than five million people, yet it produces enough dairy to feed multiples of that. (Dairy Sector Profile, Bord Bia)',
    tariff_kind='fixed'))

DAIRY = ['Milk- variety', 'Cheese – low fat', 'Yoghurt – flavoured', 'Butter – sustainable packaging',
         'Cream – single cream', 'Others – crème fraiche']
ch = block(Q4a, 'Milk- variety – low fat')
cards.append(C(
    PFX+'q4aiii', Y, LV, 'home-economics-0-11', 'dairy-industry-and-consumer-trends',
    '2021 HL Section C Q4(a)(iii) - Core',
    'Outline the measures (initiatives) taken by the dairy industry to meet current consumer trends.',
    '3 initiatives @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Initiatives taken by the dairy industry', 12, 3, 4,
          [verbatim(h, '') for h in heads(ch, DAIRY)][:CAP],
          'Three initiatives at 4 marks, graded 4:2:0. Name the product and the trend it answers - low fat and fortified milk for health, grated and snack-pack cheese for convenience, probiotic and functional yoghurt for wellbeing, sustainable packaging for the environment.')],
    'One option per dairy product, each carrying that product’s own initiatives, because the scheme groups its marking points under six product headings and prices three.',
    stem='Ireland has a population of less than five million people, yet it produces enough dairy to feed multiples of that. (Dairy Sector Profile, Bord Bia)'))

# ------------------------------------------------------------------- 4.(b)
Q4b = block(Q4, 'and 4.(b) “It is anticipated', 'or 4.(c) Market research')
TYP = ['Type 1 -', 'Type 2 -', 'Gestational -']
h_t1, h_t2, h_ge = heads(block(Q4b, 'Type 1 - (insulin dependent', 'dietary requirements –'), TYP)
ch_diet = block(Q4b, 'Eat 3 regular meals a day', '(ii) Outline the uses of sweeteners')
cards.append(C(
    PFX+'q4bi', Y, LV, 'home-economics-0-1', 'types-of-diabetes-and-dietary-requirements',
    '2021 HL Section C Q4(b)(i) - Core',
    'In relation to diabetes give an account of types, and dietary requirements that should be followed for individuals with diabetes.',
    'types 2 points @ 4 marks (graded 4:2:0) x 2 (reference to 2 types); dietary requirements 4 points @ 3 marks', 20,
    [anyN('r-1', 'Types of diabetes', 8, 2, 4,
          [f'{a.rstrip(" -")} - {bundle(h, a)}' for h, a in zip([h_t1, h_t2, h_ge], TYP)][:CAP],
          'Two types at 4 marks each, and the scheme expects reference to two. Type 1 is deficient insulin production needing daily insulin; type 2 is the body using insulin ineffectively, 90% of cases, linked to weight and inactivity. Gestational is the third if you want it.'),
     anyN('r-2', 'Dietary requirements', 12, 4, 3, semis(ch_diet)[:CAP],
          'Four requirements at 3 marks - 12 of the 20 marks. The theme is steady blood sugar: three regular meals, low GI, more fibre and starchy carbohydrate, less sugar and saturated fat. Say what each one does to blood sugar rather than just listing it.')],
    'Fixed: the question names two strands and prices types at 8 and dietary requirements at 12.',
    stem='“It is anticipated that the prevalence of diabetes in Ireland will increase to 278,000 by 2030” (Changing Lives 2016 – 2020, Diabetes Ireland)',
    tariff_kind='fixed'))

ch = block(Q4b, '2 uses @ 5 marks (graded 5:3:0) Used to sweeten food')
cards.append(C(
    PFX+'q4bii', Y, LV, 'home-economics-0-11', 'uses-of-sweeteners-in-food-production',
    '2021 HL Section C Q4(b)(ii) - Core',
    'Outline the uses of sweeteners in food production.',
    '2 uses @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Uses of sweeteners in food production', 10, 2, 5,
          semis(ch, '2 uses @ 5 marks (graded 5:3:0)')[:CAP],
          'Two uses at 5 marks, graded 5:3:0. "To sweeten" is the obvious one and the weakest - the marks are in the functional uses: preserving jam, acting as a humectant so cakes do not dry out, bulking, and replacing sugar in diabetic and low-calorie foods.')],
    'One flat list, taken in order to the cap.',
    stem='“It is anticipated that the prevalence of diabetes in Ireland will increase to 278,000 by 2030” (Changing Lives 2016 – 2020, Diabetes Ireland)'))

# ------------------------------------------------------------------- 4.(c)
Q4c = block(Q4, 'or 4.(c) Market research')
RES = ['Desk research/ Primary research:', 'Field research/ Secondary research:']
h_desk, h_field = heads(block(Q4c, 'Desk research/ Primary research:', '(ii) Outline the benefits'), RES)
cards.append(C(
    PFX+'q4ci', Y, LV, 'home-economics-1-2', 'methods-of-consumer-research',
    '2021 HL Section C Q4(c)(i) - Core',
    'Name and describe two methods of consumer research.',
    'Name 2 marks (graded 2:0) x 2; describe 2 points @ 2 marks (graded 2:1:0) x 2', 12,
    [anyN('r-1', 'Name of the research method', 4, 2, 2, ['Desk research', 'Field research'],
          'Two methods at 2 marks each, graded 2:0. The scheme offers desk research and field research - name both and you have 4 marks before describing anything.'),
     anyN('r-2', 'Description of the methods named', 8, 2, 4,
          [verbatim(h, '') for h in [h_desk, h_field]][:CAP],
          'Two points on each method at 2 marks - two thirds of the marks. The contrast is what to write: desk research gathers existing data from agencies and the internet, so it is fast, cheap and general; field research goes out and observes, interviews and surveys, so it is detailed and about actual behaviour.')],
    'Fixed: naming is priced at 4 across the two methods and the descriptions at 8.',
    stem='Market research involves the use of a variety of consumer research methods.',
    tariff_kind='fixed'))

h_con, h_ret = heads(block(Q4c, 'Consumer: Requirements of consumer'), ['Consumer: Requirements of consumer', 'Retailer: Identifies the type of person'])
o_con, o_ret = semis(h_con, 'Consumer:')[:CAP], semis(h_ret, 'Retailer:')[:CAP]
cards.append(C(
    PFX+'q4cii', Y, LV, 'home-economics-1-2', 'benefits-of-consumer-research',
    '2021 HL Section C Q4(c)(ii) - Core',
    'Outline the benefits of consumer research for both the consumer and the retailer.',
    '6 points @ 3 marks (graded 3:2:0) - 2 references to consumer, 2 references to retailer + 2 other points', 18,
    [anyN('r-1', 'Two references to the consumer', 6, 2, 3, o_con,
          'Two points at 3 marks, and the scheme requires them. The consumer gains because research finds out what they actually want - so products improve, and competition can bring prices down.'),
     anyN('r-2', 'Two references to the retailer', 6, 2, 3, o_ret,
          'Two points at 3 marks, also required. The retailer gains targeting: who will buy it, how big that market is, where it is, and whether the product actually meets the need.'),
     anyN('r-3', 'Two further points, from either', 6, 2, 3, (o_con + o_ret)[:CAP],
          'Two further points at 3 marks, from either side - "2 references to consumer, 2 references to retailer + 2 other points". The retailer list is longer, so it is the easier place to find them.')],
    'Fixed: the scheme requires two points on each side, then floats the remaining 6 marks across both. Modelled as three rows so the four compulsory points cannot be lost.',
    stem='Market research involves the use of a variety of consumer research methods.',
    tariff_kind='fixed'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2021hl_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
