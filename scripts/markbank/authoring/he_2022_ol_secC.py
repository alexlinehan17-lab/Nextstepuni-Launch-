"""2022 Ordinary Level, Section C."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2022, 'ordinary')
SEC = tidy(T[25255:45843])
Y, LV, PFX, CAP = 2022, 'ordinary', 'he-2022-ol-sc-', 14
cards, held = [], []
def C(*a, **k):
    k.setdefault('section', 'C'); return card(*a, **k)
def bundle(h, prefix='', n=None):
    seg = semis(h, prefix); return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 – Home Design', 'Elective 2 – Textiles')
E1a = block(E1, '1. (a) A popular open plan', 'and 1. (b)')

ch = block(E1a, '4 points @ 5 marks (graded 5:3:0) Large space', '(ii) Discuss three factors')
held.append(dict(C(
    PFX+'q1ai', Y, LV, 'home-economics-3-4', 'evaluating-an-open-plan-kitchen-living-space',
    '2022 OL Section C E1 Q1(a)(i)',
    'Evaluate the suitability of this kitchen/living space for a family with children.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Suitability of the kitchen/living space', 20, 4, 5,
          semis(ch, '4 points @ 5 marks (graded 5:3:0)')[:CAP], 'Held - see heldReason.')],
    'Held - see heldReason.',
    stem='A popular open plan kitchen/living space is shown below. (www.roomsketcher.com)'),
    heldReason='Marks a floor plan printed on the paper. Every option describes that image ("same flooring throughout, no transition strip", "not enough chairs at kitchen table", "useful to have more worktop space on far side of hob"), so the card is unanswerable without the figure and the markdown extraction does not carry it.'))

ch = block(E1a, '3 factors @ 5 marks (graded 5:3:0) Function of the room', '(iii) Give details of three types')
cards.append(C(
    PFX+'q1aii', Y, LV, 'home-economics-3-5', 'planning-a-lighting-system',
    '2022 OL Section C E1 Q1(a)(ii)',
    'Discuss three factors that should be considered when planning a lighting system for an open plan kitchen/living room.',
    '3 factors @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors when planning a lighting system', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0. Open plan is the word to answer - one room doing several jobs, so it needs different light over the hob than over the sofa. Name the factor and say what it means for this room.')],
    'One flat list, taken in order to the cap.',
    stem='A popular open plan kitchen/living space is shown below. (www.roomsketcher.com)'))

ch = block(E1a, '3 types @ 5 marks (graded 5:3:0) Recess ceiling lights')
cards.append(C(
    PFX+'q1aiii', Y, LV, 'home-economics-3-5', 'contemporary-lighting-types',
    '2022 OL Section C E1 Q1(a)(iii)',
    'Give details of three types of contemporary lighting in the home.',
    '3 types @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Types of contemporary lighting in the home', 15, 3, 5,
          semis(ch, '3 types @ 5 marks (graded 5:3:0)')[:CAP],
          'Three types at 5 marks, graded 5:3:0. The scheme names them only, so all 15 marks are in your details - where it goes and what it is for. Recessed ceiling lights, pendants and under-cabinet lighting are three genuinely different ones.')],
    'One flat list, taken in order to the cap. The scheme names the types only, so the detail is entirely the candidate’s.',
    stem='A popular open plan kitchen/living space is shown below. (www.roomsketcher.com)'))

# ------------------------------------------------------------------- 1.(b)
E1b = block(E1, 'and 1. (b) ‘As people get older', 'or 1. (c)')
ch = block(E1b, '3 factors @ 5 marks (graded 5:3:0) Compact', '(ii) Outline three ways')
cards.append(C(
    PFX+'q1bi', Y, LV, 'home-economics-3-3', 'choice-of-housing-for-an-older-person',
    '2022 OL Section C E1 Q1(b)(i)',
    'Discuss three factors that influence the choice of housing for an older person.',
    '3 factors @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors influencing housing choice for an older person', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0. The scheme runs three ways - where the house is (near shops, services and transport), how it is laid out (single storey, wide doorways, downstairs bedroom), and safety (non-slip floors, good lighting, an alarm). One from each covers the most ground.')],
    'One flat list, taken in order to the cap.',
    stem='‘As people get older, they often spend more time in their homes.’ (Age Friendly Ireland)'))

ch = block(E1b, '3 ways @ 5 marks (graded 5:3:0) Energy efficient appliances')
cards.append(C(
    PFX+'q1bii', Y, LV, 'home-economics-3-6', 'reducing-home-energy-bills',
    '2022 OL Section C E1 Q1(b)(ii)',
    'Outline three ways an older person can reduce their home energy bills.',
    '3 ways @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Ways to reduce home energy bills', 15, 3, 5,
          semis(ch, '3 ways @ 5 marks (graded 5:3:0)')[:CAP],
          'Three ways at 5 marks, graded 5:3:0. Say why each one saves money, not just what it is - insulation and lined curtains keep the heat in so the boiler runs less, a timer stops you heating an empty house, LED bulbs use a fraction of the electricity.')],
    'One flat list, taken in order to the cap.',
    stem='‘As people get older, they often spend more time in their homes.’ (Age Friendly Ireland)'))

# ------------------------------------------------------------------- 1.(c)
E1c = block(E1, 'or 1. (c) ‘Electricity can be dangerous')
h_mcb, h_earth = heads(block(E1c, 'Miniature circuit breaker: safety feature', '(ii) Outline four guidelines'),
                       ['Miniature circuit breaker: safety feature', 'Earth wire:'])
cards.append(C(
    PFX+'q1ci', Y, LV, 'home-economics-3-5', 'electrical-safety-devices',
    '2022 OL Section C E1 Q1(c)(i)',
    'Describe how the following electrical safety devices provide protection when using electricity in the home: miniature circuit breakers; earth wire.',
    '1 point @ 5 marks (graded 5:3:0) x 2', 10,
    [anyN('r-1', 'Miniature circuit breaker', 5, 1, 5, semis(h_mcb, 'Miniature circuit breaker:')[:CAP],
          'One point, 5 marks, graded 5:3:0. The idea is interruption: a trip switch breaks the circuit and cuts the current when there is a fault or an overload, and it can be reset once the fault is fixed. A labelled diagram is accepted.'),
     anyN('r-2', 'Earth wire', 5, 1, 5, semis(h_earth, 'Earth wire:')[:CAP],
          'One point, 5 marks, graded 5:3:0. Tell it as the story the scheme tells: a live wire touches the metal casing of an appliance, anyone touching it would be electrocuted, and the earth wire carries that electricity safely to earth instead.')],
    'Fixed: two named devices, priced identically at 5 marks each.',
    stem='‘Electricity can be dangerous if not used properly.’ (www.safeelectric.ie)',
    tariff_kind='fixed'))

ch = block(E1c, '4 guidelines @ 5 marks (graded 5:3:0) Do not overload sockets')
cards.append(C(
    PFX+'q1cii', Y, LV, 'home-economics-1-3', 'safe-use-of-electricity-guidelines-ol',
    '2022 OL Section C E1 Q1(c)(ii)',
    'Outline four guidelines to follow for the safe use of electricity in the home.',
    '4 guidelines @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Guidelines for the safe use of electricity', 20, 4, 5,
          semis(ch, '4 guidelines @ 5 marks (graded 5:3:0)')[:CAP],
          'Four guidelines at 5 marks, graded 5:3:0 - 20 marks, the biggest part of this elective. Each needs the danger attached: an overloaded socket can overheat and catch fire, wet hands conduct electricity, a trailing flex is a trip hazard.')],
    'One flat list, taken in order to the cap.',
    stem='‘Electricity can be dangerous if not used properly.’ (www.safeelectric.ie)'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 – Textiles', 'Elective 3 – Social Studies')
E2a = block(E2, '2. (a) ‘Athleisure wear', 'and 2. (b)')

ATH = ['Comfort: stretch fabric', 'Function: suitable for activities', 'Design features: monochromatic']
h_cf, h_fn, h_df = heads(block(E2a, 'Comfort: stretch fabric', '(ii) Suggest one accessory'), ATH)
held.append(dict(C(
    PFX+'q2ai', Y, LV, 'home-economics-3-8', 'evaluating-athleisure-wear-outfits',
    '2022 OL Section C E2 Q2(a)(i)',
    'Comment on the suitability of the athleisure wear outfits shown above. Refer to: comfort; function; design features.',
    '1 point @ 6 marks (graded 6:3:0) x 3', 18,
    [anyN('r-1', 'Comfort', 6, 1, 6, semis(h_cf, 'Comfort:')[:CAP], 'Held - see heldReason.'),
     anyN('r-2', 'Function', 6, 1, 6, semis(h_fn, 'Function:')[:CAP], 'Held - see heldReason.'),
     anyN('r-3', 'Design features', 6, 1, 6, semis(h_df, 'Design features:')[:CAP], 'Held - see heldReason.')],
    'Held - see heldReason.',
    stem='‘Athleisure wear is the fashion trend that can be worn anywhere anytime.’ (www.squatwolf.com)',
    tariff_kind='fixed'),
    heldReason='Marks two outfit photographs printed on the paper. The comfort and design-features strands describe those images directly ("round neck t-shirts not restrictive", "zipped jacket", "pull-string waist band", "central opening of jackets with zip detail"), so the card is unanswerable without the figures and the markdown extraction does not carry them.'))

ch = block(E2a, 'Adding jewellery')
cards.append(C(
    PFX+'q2aii', Y, LV, 'home-economics-3-8', 'accessorising-an-outfit',
    '2022 OL Section C E2 Q2(a)(ii)',
    'Suggest one accessory that could enhance the appeal of an athleisurewear outfit and give a reason for your choice.',
    'Name 3 marks (graded 3:2:0); 1 reason @ 4 marks (graded 4:2:0)', 7,
    [anyN('r-1', 'Name of the accessory', 3, 1, 3, semis(ch)[:CAP],
          'Name one, 3 marks. Any accessory in the list is accepted - jewellery, a cap, a belt, a scarf, a crossover bag, or simply different coloured laces.'),
     anyN('r-2', 'Reason for the choice', 4, 1, 4, semis(ch)[:CAP],
          'One reason at 4 marks - more than the naming, so this is where the marks are. The scheme’s reasons are of two kinds: appearance (brightens the outfit, creates contrast, emphasises the waist) and practicality (warmth, somewhere to carry your things). Either works if you say it.')],
    'Fixed: naming is priced at 3 and the reason at 4. Both rows draw on the same list, because the scheme prints each accessory together with the reason it works.',
    stem='‘Athleisure wear is the fashion trend that can be worn anywhere anytime.’ (www.squatwolf.com)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 2.(b)
E2b = block(E2, 'and 2. (b) Man-made fabrics', 'or 2. (c)')
ch_con = block(E2b, 'Weaving: warp stretched on a loom', '• properties.')
FAB = ['Viscose:', 'Acetate:', 'Polyester:', 'Nylon:', 'Acrylic:']
fab_opts = [f'{a.rstrip(":")} - {bundle(h, a)}'
            for h, a in zip(heads(block(E2b, 'Viscose: drapes well', '(ii) Give two advantages'), FAB), FAB)]
cards.append(C(
    PFX+'q2bi', Y, LV, 'home-economics-3-7', 'profile-of-a-man-made-fabric',
    '2022 OL Section C E2 Q2(b)(i)',
    'Write a profile of one man-made fabric under each of the following headings: how the fabric is constructed; properties.',
    'construction 3 points @ 2 marks (graded 2:1:0); 1st property @ 2 marks (graded 2:0); 2nd property @ 1 mark (graded 1:0)', 9,
    [anyN('r-1', 'How the fabric is constructed', 6, 3, 2, semis(ch_con, 'Weaving:')[:CAP],
          'Three points at 2 marks - two thirds of the marks. Weaving is the one the scheme explains: the warp is stretched on the loom, the weft passes over and under it, and the selvedge forms at the edges to stop fraying. Knitting, crochet, lace making, macramé and bonding are all accepted instead.'),
     anyN('r-2', 'First property', 2, 1, 2, fab_opts[:CAP],
          'One property at 2 marks, graded 2:0 - all or nothing. Pick the fabric first, then read its own line: viscose is absorbent but weak when wet, polyester is the opposite.'),
     anyN('r-3', 'Second property', 1, 1, 1, fab_opts[:CAP],
          'A second property at 1 mark, graded 1:0. Take it from the same fabric you profiled - the scheme prices five fabrics separately and the properties are not interchangeable between them.')],
    'Fixed: construction is priced at 6 and the two properties at 2 and 1 - unequal, so they are separate rows. Both property rows carry one option per fabric, each with that fabric’s own properties.',
    stem='Man-made fabrics have many uses including clothing, household items and industrial products.',
    tariff_kind='fixed'))

ch = block(E2b, '2 advantages @ 3 marks (graded 3:2:0) Durable')
cards.append(C(
    PFX+'q2bii', Y, LV, 'home-economics-3-7', 'advantages-of-man-made-fibres',
    '2022 OL Section C E2 Q2(b)(ii)',
    'Give two advantages of using man-made fibres/fabric in everyday wear.',
    '2 advantages @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Advantages of man-made fibres in everyday wear', 6, 2, 3,
          semis(ch, '2 advantages @ 3 marks (graded 3:2:0)')[:CAP],
          'Two advantages at 3 marks, graded 3:2:0. Everyday wear is the frame - the strongest answers are about living in the clothes and looking after them: crease resistant so no ironing, quick to dry, holds its shape after washing.')],
    'One flat list, taken in order to the cap.',
    stem='Man-made fabrics have many uses including clothing, household items and industrial products.'))

# ------------------------------------------------------------------- 2.(c)
E2c = block(E2, 'or 2. (c) Wardrobes are bulging')
ch = block(E2c, '3 factors @ 3 marks (graded 3:2:0) Colour and style', '(ii) Evaluate how social media')
cards.append(C(
    PFX+'q2ci', Y, LV, 'home-economics-3-8', 'factors-influencing-teenage-clothing-choices',
    '2022 OL Section C E2 Q2(c)(i)',
    'Discuss three factors that influence teenagers’ clothing choices.',
    '3 factors @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Factors influencing teenagers’ clothing choices', 9, 3, 3,
          semis(ch, '3 factors @ 3 marks (graded 3:2:0)')[:CAP],
          'Three factors at 3 marks, graded 3:2:0. The scheme names them only, so the mark is in the sentence you add - peers and social media are the two most students can develop, and cost is the honest one.')],
    'One flat list, taken in order to the cap.',
    stem='Wardrobes are bulging, yet we continue to buy more clothes.'))

ch = block(E2c, '2 points @ 3 marks (graded 3:2:0) Informs of latest fashion trends')
cards.append(C(
    PFX+'q2cii', Y, LV, 'home-economics-3-8', 'social-media-and-fashion-trends',
    '2022 OL Section C E2 Q2(c)(ii)',
    'Evaluate how social media contributes to current fashion trends.',
    '2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'How social media contributes to fashion trends', 6, 2, 3,
          semis(ch, '2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Two points at 3 marks, graded 3:2:0. The scheme is mostly about influencers - brands hand them samples, they review and promote, and trends spread and sell faster as a result. Say the mechanism, not just "people see clothes online".')],
    'One flat list, taken in order to the cap.',
    stem='Wardrobes are bulging, yet we continue to buy more clothes.'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 – Social Studies', 'Question 4 – Core')
E3a = block(E3, '3. (a) ‘A quarter of those in poverty', 'and 3. (b)')

ch_def = block(E3a, 'Being without adequate food', 'Explain each of the following')
h_rel, h_abs = heads(block(E3a, 'Relative poverty: living below', '(ii) Describe four reasons'),
                     ['Relative poverty: living below', 'Absolute poverty:'])
cards.append(C(
    PFX+'q3ai', Y, LV, 'home-economics-3-9', 'defining-relative-and-absolute-poverty',
    '2022 OL Section C E3 Q3(a)(i)',
    'Define poverty, and explain each of the following: relative poverty; absolute poverty.',
    'define 1 point @ 4 marks; relative 2 points @ 3 marks; absolute 2 points @ 3 marks', 16,
    [anyN('r-1', 'Definition of poverty', 4, 1, 4, semis(ch_def)[:CAP],
          'One point at 4 marks. The scheme’s definition is about resources being inadequate for the standard of living Irish society regards as normal - so it is not only about food and shelter but about being shut out of ordinary activities.'),
     anyN('r-2', 'Relative poverty', 6, 2, 3, semis(h_rel, 'Relative poverty:')[:CAP],
          'Two points at 3 marks. Relative means measured against everyone else - below the poverty line, defined as 50% of average household income, and unable to take part in what society treats as normal. The winter coat example is the scheme’s own.'),
     anyN('r-3', 'Absolute poverty', 6, 2, 3, semis(h_abs, 'Absolute poverty:')[:CAP],
          'Two points at 3 marks. Absolute is measured against survival, not against other people - income too low to meet basic needs at all: food, clothing, warmth, shelter. Homelessness is the clearest case.')],
    'Fixed: the question prices the definition at 4 and each kind of poverty at 6.',
    stem='‘A quarter of those in poverty are children.’ (Social Justice Ireland, 2021)',
    tariff_kind='fixed'))

ch = block(E3a, '4 reasons @ 5 marks (graded 5:3:0) Social problems', '(iii) Name and give details')
cards.append(C(
    PFX+'q3aii', Y, LV, 'home-economics-3-9', 'why-poverty-persists-in-ireland',
    '2022 OL Section C E3 Q3(a)(ii)',
    'Describe four reasons why poverty continues to be a feature in modern Irish society.',
    '4 reasons @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Reasons poverty continues in modern Irish society', 20, 4, 5,
          semis(ch, '4 reasons @ 5 marks (graded 5:3:0)')[:CAP],
          'Four reasons at 5 marks, graded 5:3:0 - 20 marks, the largest part here. The scheme names them only, so every mark is in your description. Several are linked: lack of education leads to low income leads to dependency on benefits, and saying so is what makes a 5.')],
    'One flat list, taken in order to the cap. The scheme names the reasons only, so the description is entirely the candidate’s.',
    stem='‘A quarter of those in poverty are children.’ (Social Justice Ireland, 2021)'))

VOL = ['St. Vincent de Paul:', 'Simon Community:', 'Focus Ireland:']
vol_chunks = heads(block(E3a, 'St. Vincent de Paul: provides for the most vulnerable', 'Lions Club'), VOL)
ch_more = block(E3a, 'Lions Club')
cards.append(C(
    PFX+'q3aiii', Y, LV, 'home-economics-3-9', 'voluntary-organisations-supporting-families-in-poverty',
    '2022 OL Section C E3 Q3(a)(iii)',
    'Name and give details of one voluntary organisation that provides support to families at risk of poverty.',
    'Name 4 marks (graded 4:2:0); 2 details @ 5 marks (graded 5:3:0)', 14,
    [anyN('r-1', 'Name of the voluntary organisation', 4, 1, 4,
          (['St. Vincent de Paul', 'Simon Community', 'Focus Ireland'] + semis(ch_more))[:CAP],
          'Name one, 4 marks. Three are described in full and the rest are accepted by name. St Vincent de Paul has by far the longest list of services, so it is the easiest to develop for the other 10 marks.'),
     anyN('r-2', 'Details of the organisation', 10, 2, 5,
          [f'{a.rstrip(":")} - {bundle(h, a)}' for h, a in zip(vol_chunks, VOL)][:CAP],
          'Two details at 5 marks - 10 of the 14 marks, and they must be about the organisation you named. Each option here carries that body’s own services: SVP is financial help and home visits, Simon is emergency shelter and addiction support, Focus Ireland is homelessness and tenancy support.')],
    'Fixed: naming is priced at 4 and the details at 10. The details row carries one option per organisation, because the two details must match whichever was named.',
    stem='‘A quarter of those in poverty are children.’ (Social Justice Ireland, 2021)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 3.(b)
E3b = block(E3, 'and 3. (b) ‘Communities are the life blood', 'or 3. (c)')
ch = block(E3b, '3 reasons @ 5 marks (graded 5:3:0) Technological developments', '(ii) Explain how the movement')
cards.append(C(
    PFX+'q3bi', Y, LV, 'home-economics-3-11', 'rural-to-urban-migration-reasons',
    '2022 OL Section C E3 Q3(b)(i)',
    'Discuss three reasons why people are moving from rural areas to urban areas.',
    '3 reasons @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Reasons people move from rural to urban areas', 15, 3, 5,
          semis(ch, '3 reasons @ 5 marks (graded 5:3:0)')[:CAP],
          'Three reasons at 5 marks, graded 5:3:0. The scheme splits into push and pull - farm machinery removing rural jobs is the push, while work, college, services and entertainment are the pull. One push and two pulls reads well.')],
    'One flat list, taken in order to the cap.',
    stem='‘Communities are the life blood of rural Ireland.’ (www.gov.ie)'))

h_rur, h_urb = heads(block(E3b, 'Rural areas: decrease in population'),
                     ['Rural areas: decrease in population', 'Urban areas: more services'])
cards.append(C(
    PFX+'q3bii', Y, LV, 'home-economics-3-11', 'impact-of-rural-to-urban-movement-on-family-life',
    '2022 OL Section C E3 Q3(b)(ii)',
    'Explain how the movement from rural areas to urban areas has impacted family life.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Impact on family life', 15, 3, 5,
          (semis(h_rur, 'Rural areas:') + semis(h_urb, 'Urban areas:'))[:CAP],
          'Three points at 5 marks, graded 5:3:0, pooled across both ends of the move. The strongest answers take from both - families left behind in rural areas lose services and the support of extended family, while families arriving in urban areas meet house prices, congestion and competition for school places.')],
    'One flat list pooling the rural and urban clusters, because the scheme prices three points across both rather than pricing each separately.',
    stem='‘Communities are the life blood of rural Ireland.’ (www.gov.ie)'))

# ------------------------------------------------------------------- 3.(c)
E3c = block(E3, 'or 3. (c) ‘Deciding on childcare')
ch = block(E3c, '3 factors @ 5 marks (graded 5:3:0) Cost', '(ii) Describe how attending pre-school')
cards.append(C(
    PFX+'q3ci', Y, LV, 'home-economics-2-0', 'choosing-a-childcare-facility',
    '2022 OL Section C E3 Q3(c)(i)',
    'Give an account of three factors parents should consider when choosing a childcare facility for their child.',
    '3 factors @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors when choosing a childcare facility', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0. Answer as a parent actually deciding - the staff’s qualifications and first aid training, whether the hours match a working day, and where it sits between home and work. Cost is fine but is the thinnest to develop.')],
    'One flat list, taken in order to the cap.',
    stem='‘Deciding on childcare is a big decision for any parent.’ (www.citizeninformation.ie)'))

ch = block(E3c, '3 points @ 5 marks (graded 5:3:0) Socialisation')
cards.append(C(
    PFX+'q3cii', Y, LV, 'home-economics-2-0', 'pre-school-and-child-development',
    '2022 OL Section C E3 Q3(c)(ii)',
    'Describe how attending pre-school can promote a child’s development.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'How pre-school promotes a child’s development', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0. The scheme covers social, physical and intellectual development, so take one of each rather than three versions of making friends. Preparation for primary school is the one worth ending on.')],
    'One flat list, taken in order to the cap.',
    stem='‘Deciding on childcare is a big decision for any parent.’ (www.citizeninformation.ie)'))

# ------------------------------------------------------------- Question 4 Core
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4. (a) ‘Fish has a reputation', 'and 4. (b)')

h_nut, h_die = heads(block(Q4a, 'Nutritional value: HBV protein', '(ii) Outline:'),
                     ['Nutritional value: HBV protein', 'Dietetic value:'])
o_nut, o_die = semis(h_nut, 'Nutritional value:')[:CAP], semis(h_die, 'Dietetic value:')[:CAP]
cards.append(C(
    PFX+'q4ai', Y, LV, 'home-economics-0-9', 'nutritive-and-dietetic-value-of-fish',
    '2022 OL Section C Q4(a)(i) - Core',
    'Give an account of the nutritive value and the dietetic value of fish.',
    '5 points @ 4 marks (graded 4:2:0) (1 reference to nutritional value, 1 reference to dietetic value, plus 3 others)', 20,
    [anyN('r-1', 'One reference to nutritional value', 4, 1, 4, o_nut,
          'One point at 4 marks, and the scheme requires at least one. Nutritional value is what is IN the fish - HBV protein, omega 3 in oily fish, vitamins A and D, iodine and calcium in tinned fish.'),
     anyN('r-2', 'One reference to dietetic value', 4, 1, 4, o_die,
          'One point at 4 marks, also required. Dietetic value is who it SUITS and why - easy to digest for older people, protein for growing children, white fish for a low-calorie diet, omega 3 to reduce heart disease.'),
     anyN('r-3', 'Three further points, from either value', 12, 3, 4, (o_nut + o_die)[:CAP],
          'Three further points at 4 marks each, and the scheme lets them come from either list - "1 reference to nutritional value, 1 reference to dietetic value, plus 3 others". Whichever you know better is where to spend them.')],
    'Fixed: the scheme requires one point on each value, then floats the remaining 12 marks across both. Modelled as three rows so the two compulsory points cannot be lost.',
    stem='‘Fish has a reputation for being one of the healthiest foods we can eat.’ (www.bbc.com)',
    tariff_kind='fixed'))

ch_buy = block(Q4a, 'Buy from clean and hygienic retailer', '• the effects of cooking on fish')
ch_cook = block(Q4a, '3 effects @ 3 marks (graded 3:2:0) Protein coagulates', '(iii) Name one method of processing')
cards.append(C(
    PFX+'q4aii', Y, LV, 'home-economics-0-9', 'buying-fresh-fish-and-the-effects-of-cooking',
    '2022 OL Section C Q4(a)(ii) - Core',
    'Outline the guidelines to follow when buying fresh fish, and the effects of cooking on fish.',
    'guidelines 3 points @ 3 marks; effects 3 points @ 3 marks (graded 3:2:0)', 18,
    [anyN('r-1', 'Guidelines when buying fresh fish', 9, 3, 3, semis(ch_buy)[:CAP],
          'Three guidelines at 3 marks. Almost all of these are things you can see or smell at the counter - firm elastic flesh, bright bulging eyes, red gills, tightly attached scales, and it should smell of the sea and nothing else.'),
     anyN('r-2', 'Effects of cooking on fish', 9, 3, 3,
          semis(ch_cook, '3 effects @ 3 marks (graded 3:2:0)')[:CAP],
          'Three effects at 3 marks. The scheme wants the science: protein coagulates, the flesh turns from transparent to opaque, collagen becomes gelatine so it flakes and digests easily, and bacteria and parasites are destroyed. Overcooking making it tough is the practical one.')],
    'Fixed: the question names two strands and prices them identically at 9 marks each.',
    stem='‘Fish has a reputation for being one of the healthiest foods we can eat.’ (www.bbc.com)',
    tariff_kind='fixed'))

PROC = ['Freezing: Advantages:', 'Canning: Advantages:', 'Smoking: Advantages:']
proc_chunks = heads(block(Q4a, 'Freezing: Advantages:'), PROC)
# The advantages and disadvantages are separated by an "etc." that semis()
# strips, so a bundle spanning both is not contiguous in the scheme and fails
# provenance. They also cannot share a row: only the advantages sit adjacent to
# the method name, so only they can carry it.
adv, dis = [], []
for h, a in zip(proc_chunks, PROC):
    method = a.split(':')[0]
    cut = h.find('Disadvantage')
    adv.append(f'{method}: Advantages: {bundle(h[:cut], a)}')
    dis.append(bundle(h[cut:], h[cut:].split(':')[0] + ':'))
cards.append(C(
    PFX+'q4aiii', Y, LV, 'home-economics-0-4', 'processing-fish-to-extend-shelf-life',
    '2022 OL Section C Q4(a)(iii) - Core',
    'Name one method of processing fish to extend its shelf life and give one advantage and one disadvantage of the method named.',
    '1 method @ 4 marks (graded 4:0); 1 advantage @ 4 marks; 1 disadvantage @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Method of processing fish', 4, 1, 4, ['Freezing', 'Canning', 'Smoking'],
          'Name one, 4 marks, graded 4:0 - all or nothing, but it is one word and only three are offered. Freezing has the fullest treatment in the scheme.'),
     anyN('r-2', 'One advantage of the method named', 4, 1, 4, adv[:CAP],
          'One advantage at 4 marks, and it must match the method you named - freezing keeps the nutrients, canning softens the bones so the calcium becomes available, smoking gives the distinctive flavour.'),
     anyN('r-3', 'One disadvantage of the method named', 4, 1, 4, dis[:CAP],
          'One disadvantage at 4 marks. Listed in the same order as the advantages above - freezing first (packaging and the cost of running a freezer), then canning (salt added, texture softened), then smoking (colourings and flavourings added).')],
    'Fixed: naming, one advantage and one disadvantage, priced identically at 4 marks each. Advantages and disadvantages are separate rows because only the advantages sit adjacent to the method name in the scheme.',
    stem='‘Fish has a reputation for being one of the healthiest foods we can eat.’ (www.bbc.com)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 4.(b)
Q4b = block(Q4, 'and 4. (b) Retailers use a variety', 'or 4. (c)')
ch = block(Q4b, 'Store layout, size can influence', '(ii) Outline the procedure')
cards.append(C(
    PFX+'q4bi', Y, LV, 'home-economics-1-2', 'retail-techniques-to-encourage-purchase',
    '2022 OL Section C Q4(b)(i) - Core',
    'Give details of three ways retailers can encourage consumers to purchase goods.',
    '3 ways @ 5 marks each (graded 5:3:0)', 15,
    [anyN('r-1', 'Ways retailers encourage consumers to purchase', 15, 3, 5,
          semis(ch)[:CAP],
          'Three ways at 5 marks, graded 5:3:0. Give the detail that shows you know WHY it works - essentials at the back so you walk past everything else, luxuries at eye level, sweets at the checkout, €4.99 reading as cheaper than €5.')],
    'One flat list, taken in order to the cap. The scheme runs its techniques together under running headings, so the technique names sit inside the options.',
    stem='Retailers use a variety of techniques to increase consumer spending.'))

ch = block(Q4b, '5 points @ 3 marks (graded 3:2:0) Return to the retailer')
cards.append(C(
    PFX+'q4bii', Y, LV, 'home-economics-1-2', 'making-a-consumer-complaint',
    '2022 OL Section C Q4(b)(ii) - Core',
    'Outline the procedure a consumer should follow when making a complaint about a faulty product.',
    '5 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'Procedure for making a consumer complaint', 15, 5, 3,
          semis(ch, '5 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Five points at 3 marks - this is a procedure, so write it in order: go back to the retailer with the receipt, complain promptly, ask for the manager, state the fault and the redress you want, put it in writing if that fails, and take it to the Small Claims Court as a last resort.')],
    'One flat list, taken in scheme order - which is also the order the procedure happens in.',
    stem='Retailers use a variety of techniques to increase consumer spending.'))

# ------------------------------------------------------------------- 4.(c)
Q4c = block(Q4, 'or 4. (c) The successful organisation')
MGT = ['Dual roles:', 'Stages in life cycle:', 'Employment patterns:']
h_dr, h_lc, h_ep = heads(block(Q4c, 'Dual roles: if both parents work', '(ii) Describe three ways in which technology'), MGT)
cards.append(C(
    PFX+'q4ci', Y, LV, 'home-economics-1-0', 'factors-affecting-management-of-the-home',
    '2022 OL Section C Q4(c)(i) - Core',
    'Discuss how the following factors may affect the management of the home: dual roles; stages in life cycle; employment patterns.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'Dual roles', 5, 1, 5, semis(h_dr, 'Dual roles:')[:CAP],
          'One point, 5 marks, graded 5:3:0. Dual role means being both earner and homemaker at once - when both parents do that the household needs a different system, with tasks shared and planned rather than assumed.'),
     anyN('r-2', 'Stages in life cycle', 5, 1, 5, semis(h_lc, 'Stages in life cycle:')[:CAP],
          'One point, 5 marks, graded 5:3:0. The needs change as the family ages - small children need constant care, older children can take on jobs and share decisions, and in retirement income is smaller.'),
     anyN('r-3', 'Employment patterns', 5, 1, 5, semis(h_ep, 'Employment patterns:')[:CAP],
          'One point, 5 marks, graded 5:3:0. How many work, and on what hours - one earner with one at home, or both working with children in a crèche. Job sharing and flexitime are the scheme’s examples of patterns that make childcare easier.')],
    'Fixed: the question names all three factors, so all three must be answered. Priced identically at 5 marks each.',
    stem='The successful organisation of the family unit depends on good management skills.',
    tariff_kind='fixed'))

ch = block(Q4c, '3 ways @ 5 marks (graded 5:3:0) Workload is reduced')
cards.append(C(
    PFX+'q4cii', Y, LV, 'home-economics-1-3', 'technology-and-efficient-home-management',
    '2022 OL Section C Q4(c)(ii) - Core',
    'Describe three ways in which technology has contributed to the efficient management of the home.',
    '3 ways @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Ways technology contributes to efficient home management', 15, 3, 5,
          semis(ch, '3 ways @ 5 marks (graded 5:3:0)')[:CAP],
          'Three ways at 5 marks, graded 5:3:0. The scheme gives an example with almost every point, so use them - a washing machine for reduced workload, a food processor for time saved, automation to run appliances while you are out. Name the technology and say what it replaces.')],
    'One flat list, taken in order to the cap.',
    stem='The successful organisation of the family unit depends on good management skills.'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2022ol_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
