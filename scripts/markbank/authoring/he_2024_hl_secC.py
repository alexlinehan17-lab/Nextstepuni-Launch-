"""2024 Higher Level, Section C."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2024, 'higher')
SEC = tidy(T[29409:56338])
Y, LV, PFX = 2024, 'higher', 'he-2024-hl-sc-'
CAP = 14
END = 'Leaving Certificate Examination 2024'
cards, held = [], []

def C(*a, **k):
    k.setdefault('section', 'C')
    return card(*a, **k)

def bundle(h, prefix='', n=None):
    seg = semis(h, prefix)
    return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 –', 'Elective 2 –')
E1a = block(E1, '1.(a) ‘A well-planned', 'and 1.(b)')

ch = block(E1a, '1 point on each factor & 2 other points', '(ii) Identify three design principles')
h_cost, h_fam, h_erg = heads(ch, ['cost budget constraints', 'family stage and circumstances',
                                  'ergonomics design of room'])
o_cost, o_fam, o_erg = semis(h_cost, 'cost'), semis(h_fam, 'family stage and circumstances'), semis(h_erg, 'ergonomics')
cards.append(C(
    PFX + 'q1ai', Y, LV, 'home-economics-3-4', 'interior-design-influencing-factors',
    '2024 HL Section C E1 Q1(a)(i)',
    'Discuss the factors that influence the interior design of a home. Refer to: cost; family stage and circumstances; ergonomics.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'cost', 4, 1, 4, o_cost[:CAP],
          'One point, 4 marks, graded 4:2:0. The shortest list of the three — the scheme\'s own point is that a limited budget is not the same as poor design, so say what you would spend on and what you would economise on.'),
     anyN('r-2', 'family stage and circumstances', 4, 1, 4, o_fam[:CAP],
          'One point, 4 marks, graded 4:2:0. Name the stage and the design consequence — young children means easy-clean surfaces and play areas, an older family means study space. Current and future needs is a separate creditable point.'),
     anyN('r-3', 'ergonomics', 4, 1, 4, o_erg[:CAP],
          'One point, 4 marks, graded 4:2:0. Ergonomics is fitting the room to the body and the work done in it: traffic flow, the work triangle, worktops at the user\'s height.'),
     anyN('r-4', 'Two further points, from any of the three factors', 8, 2, 4, (o_cost + o_fam + o_erg)[:CAP],
          'Eight of the twenty marks float: the scheme reads "1 point on each factor & 2 other points", so after covering all three factors add two more from whichever you know best.')],
    'Fixed: one point pinned to each of the three named factors and two floating. Ignoring a factor caps you at 16 however much you write on the others.',
    stem='‘A well-planned, well-designed home looks elegant, and improves a person’s quality of life.’ (www.homesandgardens.com)',
    tariff_kind='fixed'))

PRIN = ['proportion objects must be', 'emphasis achieved by', 'balance applied using', 'rhythm can be achieved']
ch = block(E1a, 'proportion objects must be', '(iii) Evaluate how the design')
pb = heads(ch, PRIN)
o_desc = [x for h, p in zip(pb, PRIN) for x in semis(h, p.split()[0])]
cards.append(C(
    PFX + 'q1aii', Y, LV, 'home-economics-3-4', 'design-principles-in-interior-design',
    '2024 HL Section C E1 Q1(a)(ii)',
    'Identify three design principles and describe how each design principle identified could be applied in an interior design space.',
    '3 principles @ 6 marks (graded 6:4:2:0) [Name 2 marks, description 4 marks] x3', 18,
    [anyN('r-1', 'Design principles', 6, 3, 2, ['proportion', 'emphasis', 'balance', 'rhythm'],
          'Three principles named, 2 marks each, graded 2:0 — all-or-nothing per name. The scheme accepts only these four, so naming three of the four is six guaranteed marks before you describe anything.'),
     anyN('r-2', 'How each principle is applied in an interior design space', 12, 3, 4, o_desc[:CAP],
          'Three descriptions at 4 marks, graded 4:2:0 — twelve of the eighteen marks. Each must be applied to a room, not defined in the abstract: a fireplace as the focal point for emphasis, a colour repeated around the room for rhythm.')],
    'Fixed: the scheme prices the name and the description separately inside each 6-mark principle, so the card splits them into a naming row and a describing row.',
    stem='‘A well-planned, well-designed home looks elegant, and improves a person’s quality of life.’ (www.homesandgardens.com)',
    tariff_kind='fixed'))

ch = block(E1a, '3 points @ 4 marks (graded 4:2:0) renewable energy sources')
cards.append(C(
    PFX + 'q1aiii', Y, LV, 'home-economics-3-6', 'house-design-and-lower-energy-use',
    '2024 HL Section C E1 Q1(a)(iii)',
    'Evaluate how the design and construction of a house can help lower the energy use of its occupants.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'How design and construction lower energy use', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three points at 4 marks, graded 4:2:0. Evaluate, so say what each feature saves — south-facing glazing collects heat, MVHR recovers heat from air being expelled. Naming the feature alone is 2.')],
    'One flat list, taken in order to the cap.',
    stem='‘A well-planned, well-designed home looks elegant, and improves a person’s quality of life.’ (www.homesandgardens.com)'))

E1b = block(E1, 'and 1.(b) ‘Electricity', 'or 1.(c)')
ch = block(E1b, 'miniature circuit breaker will trip', '(ii) Identify three inefficient')
h_mcb, h_e = heads(ch, ['miniature circuit breaker will trip', 'earth wire is'])
cards.append(C(
    PFX + 'q1bi', Y, LV, 'home-economics-3-5', 'electrical-safety-mcb-and-earth-wire',
    '2024 HL Section C E1 Q1(b)(i)',
    'Describe how each of the following contribute to the safe use of electrical appliances in the home: miniature circuit breaker; earth wire.',
    '2 points @ 6 marks (graded 6:4:2:0)', 12,
    [anyN('r-1', 'miniature circuit breaker', 6, 1, 6, semis(h_mcb, 'miniature circuit breaker')[:CAP],
          'One point, 6 marks, on a 6:4:2:0 ladder — so this is really a short paragraph, not a sentence. The full chain is: detects the fault, trips to off, breaks the circuit, stops the current, and can be reset once the fault is fixed. The scheme accepts labelled diagrams.'),
     anyN('r-2', 'earth wire', 6, 1, 6, semis(h_e, 'earth wire is')[:CAP],
          'One point, 6 marks, 6:4:2:0. The marks are in the danger and the remedy: a damaged live wire can make the metal casing live, touching it would electrocute you, and the earth wire carries that current safely to a plate in the ground.')],
    'Fixed: two named safety devices at 6 marks each. Both are 6:4:2:0, so a one-line answer scores 2 of 6 — these need the whole sequence written out.',
    stem='‘Electricity is a powerful and versatile energy often taken for granted, but safe use is vital.’ (www.esbnetworks.com)',
    tariff_kind='fixed'))

INEF = ['heat loss insulate walls', 'heating system install', 'open fires install stove',
        'water heating install timer', 'appliances choose A rated', 'water use repair leaking',
        'lighting chose LED']
ch = block(E1b, 'heat loss insulate walls')
ib = heads(ch, INEF)
o_strat = [x for h, p in zip(ib, INEF) for x in semis(h, ' '.join(p.split()[:2]))]
cards.append(C(
    PFX + 'q1bii', Y, LV, 'home-economics-3-6', 'inefficient-energy-use-and-strategies',
    '2024 HL Section C E1 Q1(b)(ii)',
    'Identify three inefficient uses of energy in the home and assess a strategy you would recommend to improve energy efficiency in each case identified.',
    '3 inefficiencies @ 2 marks (graded 2:0); 3 strategies @ 4 marks (graded 4:2:0)', 18,
    [anyN('r-1', 'Inefficient uses of energy in the home', 6, 3, 2,
          ['heat loss', 'heating system', 'open fires', 'water heating', 'appliances', 'water use', 'lighting'],
          'Three identified, 2 marks each, graded 2:0 — all-or-nothing, and naming the area is all that is asked. Six easy marks; the scheme accepts seven areas so there is no excuse for losing any.'),
     anyN('r-2', 'Strategies to improve energy efficiency', 12, 3, 4, o_strat[:CAP],
          'Three strategies at 4 marks, graded 4:2:0 — twelve of the eighteen marks. Each strategy must answer the inefficiency you identified, and assess means saying what it saves, not just naming the fix.')],
    'Fixed: identifying is priced at 2 and assessing at 4, so two thirds of the marks are in the strategies. The rows pair up — a strategy only scores against an inefficiency you actually named.',
    stem='‘Electricity is a powerful and versatile energy often taken for granted, but safe use is vital.’ (www.esbnetworks.com)',
    tariff_kind='fixed'))

E1c = block(E1, 'or 1.(c) ‘If your home is well insulated')
ch = block(E1c, 'underlying principle 3 points @ 2 marks (graded 2:1:0)', 'methods of home insulation')
o_prin = semis(ch, 'underlying principle 3 points @ 2 marks (graded 2:1:0)')
METH = ['attic/roof fibre blanket', 'walls cavity walls air', 'solid walls blanket',
        'floor fill gaps', 'draught excluders brush', 'windows/doors well-fitting']
mb = heads(block(E1c, 'attic/roof fibre blanket', '(ii) Discuss the importance'), METH)
cards.append(C(
    PFX + 'q1ci', Y, LV, 'home-economics-3-6', 'insulation-principle-and-methods',
    '2024 HL Section C E1 Q1(c)(i)',
    'Explain the underlying principle of insulation used in the home. Identify and describe three different methods of home insulation.',
    'Principle 3 points @ 2 marks (graded 2:1:0); methods 3 points @ 4 marks (graded 4:3:2:1:0)', 18,
    [anyN('r-1', 'Underlying principle of insulation', 6, 3, 2, o_prin[:CAP],
          'Three points at 2 marks, graded 2:1:0. The principle is that trapped air and poor conductors slow heat escaping — name the materials, say they are poor conductors, and say what that prevents. Six quick marks.'),
     anyN('r-2', 'Methods of home insulation', 12, 3, 4,
          [bundle(h, ' '.join(p.split()[:2]), 3) for h, p in zip(mb, METH)][:CAP],
          'Three methods at 4 marks on a 4:3:2:1:0 ladder, so partial credit is real and a half-remembered method still scores. Describe, so give the material and where it goes. Taking one from the attic, the walls and the windows gives three that cannot be read as the same method. The scheme accepts a labelled diagram.')],
    'Fixed: the principle is priced at 6 and the methods at 12. The methods row shows one option per location, each carrying that location\'s own materials.',
    stem='‘If your home is well insulated; you also need good ventilation.’ (www.seai.com)',
    tariff_kind='fixed'))

ch = block(E1c, '3 points @ 4 marks (graded 4:2:0) provides oxygen rich')
cards.append(C(
    PFX + 'q1cii', Y, LV, 'home-economics-3-5', 'importance-of-adequate-ventilation',
    '2024 HL Section C E1 Q1(c)(ii)',
    'Discuss the importance of having adequate ventilation in a house.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Importance of adequate ventilation in a house', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three points at 4 marks, graded 4:2:0. The last two options are the ones that separate answers: poor ventilation causes medical conditions, and it causes structural damage to the house. Name the condition or the damage and you have the full 4.')],
    'One flat list, taken in order to the cap.',
    stem='‘If your home is well insulated; you also need good ventilation.’ (www.seai.com)'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 –', 'Elective 3 –')
E2a = block(E2, '2.(a) Being stylish', 'and 2.(b)')
ch = block(E2a, 'comfort loose fitting dress', '(ii) Discuss how social and economic')
h_c, h_a, h_t = heads(ch, ['comfort loose fitting', 'aesthetic appeal relaxed', 'current fashion trends fashionable'])
held.append(dict(C(
    PFX + 'q2ai', Y, LV, 'home-economics-3-8', 'evaluating-outfit-design-for-an-occasion',
    '2024 HL Section C E2 Q2(a)(i)',
    'Evaluate the design of the outfits shown above for a summer family gathering. Refer to: comfort; aesthetic appeal; current fashion trends.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'comfort', 5, 1, 5, semis(h_c, 'comfort')[:CAP], 'One point, 5 marks, graded 5:3:0.'),
     anyN('r-2', 'aesthetic appeal', 5, 1, 5, semis(h_a, 'aesthetic appeal')[:CAP], 'One point, 5 marks, graded 5:3:0.'),
     anyN('r-3', 'current fashion trends', 5, 1, 5, semis(h_t, 'current fashion trends')[:CAP], 'One point, 5 marks, graded 5:3:0.')],
    'Fixed: three headings named in the question, priced equally.',
    stem='Being stylish, yet comfortable is key for many family gatherings and parties.', tariff_kind='fixed'),
    heldReason='Marks two outfits printed on the paper. Every option describes that image ("asymmetrical hem line on dress", "repeating colour in T-shirt and runners"), so the card is unanswerable without the figure and the markdown extraction does not carry it.'))

ch = block(E2a, 'social factors media')
h_s, h_e = heads(ch, ['social factors media', 'economic factors amount'])
cards.append(C(
    PFX + 'q2aii', Y, LV, 'home-economics-3-8', 'social-and-economic-influences-on-clothing',
    '2024 HL Section C E2 Q2(a)(ii)',
    'Discuss how social and economic factors influence the design and construction of clothing.',
    '2 points @ 5 marks (graded 5:3:0), 1 point on each heading', 10,
    [anyN('r-1', 'social factors', 5, 1, 5, semis(h_s, 'social factors')[:CAP],
          'One point, 5 marks, graded 5:3:0 — no 4, so a named factor without a consequence drops to 3. Social factors are about who is watching: media, influencers, the occasion, status, profession.'),
     anyN('r-2', 'economic factors', 5, 1, 5, semis(h_e, 'economic factors')[:CAP],
          'One point, 5 marks, graded 5:3:0. Economic factors split into what the buyer can spend (disposable income, recession, inflation) and what the maker must pay (raw materials, labour, production costs) — either side scores.')],
    'Fixed: the scheme pins one point to each heading, so answering only one caps you at 5 of 10.',
    stem='Being stylish, yet comfortable is key for many family gatherings and parties.', tariff_kind='fixed'))

# 2(b) — one full profile card per natural fibre
E2b = block(E2, 'and 2.(b) ‘Natural fabrics', 'or 2.(c)')
prod = heads(block(E2b, 'fibre production wool fleece', 'fabric properties wool durable'),
             ['wool fleece', 'silk silkworms', 'cotton comes from', 'linen made from'])
props = heads(block(E2b, 'fabric properties wool durable', 'identification test wool doesn'),
              ['wool durable', 'silk strong', 'cotton strong', 'linen strong'])
iden = heads(block(E2b, 'identification test wool doesn'),
             ['wool doesn', 'silk doesn', 'cotton burns quickly', 'linen burns quickly'])
FIBRES = [
    ('wool', 'Wool', 'the fleece of sheep, goats and llamas'),
    ('silk', 'Silk', 'the cocoon of the silkworm'),
    ('cotton', 'Cotton', 'the boll of the cotton plant'),
    ('linen', 'Linen', 'the stem of the flax plant'),
]
for i, (slug, name, src) in enumerate(FIBRES):
    cards.append(C(
        PFX + 'q2b-' + slug, Y, LV, 'home-economics-3-7', f'natural-fibre-profile-{slug}',
        f'2024 HL Section C E2 Q2(b) - {name}',
        f'Write a profile of a fabric manufactured from natural fibres. Refer to: name; fibre production; fabric properties; identification test.',
        'Name 1 @ 2 marks; production 3 @ 2 marks; properties 3 @ 1 mark; identification 2 @ 2 marks', 15,
        [anyN('r-1', 'Name of the fabric', 2, 1, 2, [name.lower()],
              f'Name the fabric, 2 marks, graded 2:0 — all-or-nothing. This profile follows {name.lower()}; the scheme prints a parallel profile for silk, cotton and linen too, each marked the same way.'),
         anyN('r-2', 'Fibre production', 6, 3, 2, semis(prod[i], slug)[:CAP],
              f'Three points at 2 marks, graded 2:1:0. {name} comes from {src}. The scheme lists the stages in order, so writing the process as a sequence gives three points without having to recall them separately.'),
         anyN('r-3', 'Fabric properties', 3, 3, 1, semis(props[i], slug)[:CAP],
              'Three properties at 1 mark each, graded 1:0 — one word each, all-or-nothing. Three of the cheapest marks on the paper; do not write sentences for them.'),
         anyN('r-4', 'Identification test', 4, 2, 2, semis(iden[i], slug)[:CAP],
              'Two points at 2 marks, graded 2:1:0. This is the burn test, and the marks are in what you observe: how it takes the flame, the colour of the flame, the smell, and what the residue is like.')],
        f'One of four parallel profiles the scheme prints under Q2(b). A candidate profiles a single fibre, so each fibre is its own card with its own questionRef rather than pooling four sets of marking points into one menu.',
        stem='‘Natural fabrics are renewable; a good choice for sustainable living.’ (www.studioheijne.com)',
        tariff_kind='fixed'))

E2c = block(E2, 'or 2.(c) ‘The fashion and textile industry')
ch = block(E2c, '2 points @ 3 marks (graded 3:2:0) comfort', '(ii) Name one Irish fashion designer')
cards.append(C(
    PFX + 'q2ci', Y, LV, 'home-economics-3-8', 'emergence-of-leisure-wear',
    '2024 HL Section C E2 Q2(c)(i)',
    'Discuss the emergence of leisure wear as a current fashion trend.',
    '2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'The emergence of leisure wear as a current fashion trend', 6, 2, 3,
          semis(ch, '2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Only two points at 3 marks — a six-mark part, so keep it short. The scheme wants why it caught on: comfort, versatility, and the shift to healthier, more active lifestyles.')],
    'One flat list, taken in order to the cap.',
    stem='‘The fashion and textile industry continue to play its part in Ireland’s social, cultural and economic development.’ (www.ndcg.ie)'))

ch = block(E2c, 'name of designer John Rocha')
h_n, h_w = heads(ch, ['name of designer John Rocha', 'work designing clothes'])
cards.append(C(
    PFX + 'q2cii', Y, LV, 'home-economics-3-8', 'irish-fashion-designers',
    '2024 HL Section C E2 Q2(c)(ii)',
    'Name one Irish fashion designer. Outline their work in the Irish fashion industry.',
    'Name 1 point @ 3 marks; work 2 points @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Irish fashion designers', 3, 1, 3, semis(h_n, 'name of designer')[:CAP],
          'Name one, 3 marks, graded 3:2:0. The scheme accepts eight designers — pick the one whose actual output you can describe, because the other 6 marks depend on it.'),
     anyN('r-2', 'Their work in the Irish fashion industry', 6, 2, 3, semis(h_w, 'work')[:CAP],
          'Two points at 3 marks, graded 3:2:0. The scheme credits who they design for and what for — royalty, celebrities, world leaders, major world events, the Riverdance costumes.')],
    'Fixed: the name is priced at 3 and the work at 6.',
    stem='‘The fashion and textile industry continue to play its part in Ireland’s social, cultural and economic development.’ (www.ndcg.ie)',
    tariff_kind='fixed'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 –', 'Question 4 – Core')
E3a = block(E3, '3.(a) ‘Education gives people', 'and 3.(b)')
ch = block(E3a, 'as a method of socialisation formal in the classroom', '(ii) Evaluate a range')
h_soc, h_work = heads(ch, ['as a method of socialisation formal', 'as preparation for work develops'])
o_soc, o_work = semis(h_soc, 'as a method of socialisation'), semis(h_work, 'as preparation for work')
cards.append(C(
    PFX + 'q3ai', Y, LV, 'home-economics-3-10', 'role-of-education-in-society',
    '2024 HL Section C E3 Q3(a)(i)',
    'Discuss the role of education in society. Refer to education: as a method of socialisation; as preparation for work.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'as a method of socialisation', 8, 2, 4, o_soc[:CAP],
          'Two points at 4 marks, graded 4:2:0. The formal/informal split and the hidden curriculum are the technical terms the scheme rewards — name them and say what they teach.'),
     anyN('r-2', 'as preparation for work', 8, 2, 4, o_work[:CAP],
          'Two points at 4 marks, graded 4:2:0. Split between personal qualities (responsibility, punctuality, teamwork) and formal preparation (qualifications, TY, LCA, LCVP work experience, career guidance).'),
     anyN('r-3', 'One further point, from either heading', 4, 1, 4, (o_soc + o_work)[:CAP],
          'The scheme reads "2 points on method of socialisation, 2 points on preparation for work + 1 other point", so the fifth floats.')],
    'Fixed: two points pinned to each named strand and the fifth floating. Answering only one strand caps you at 12 of 20.',
    stem='‘Education gives people the opportunity and ability to improve their own lives.’ (www.legalstudymatieral.com)',
    tariff_kind='fixed'))

ch = block(E3a, '3 supports @ 5 marks (graded 5:4:3:2:0)', '(iii) Analyse how socio-economic')
cards.append(C(
    PFX + 'q3aii', Y, LV, 'home-economics-3-10', 'educational-supports-for-special-needs',
    '2024 HL Section C E3 Q3(a)(ii)',
    'Evaluate a range of educational supports available in second level schools for students with special educational needs.',
    '3 supports @ 5 marks (graded 5:4:3:2:0)', 15,
    [anyN('r-1', 'Educational supports for students with special educational needs', 15, 3, 5,
          semis(ch, '3 supports @ 5 marks (graded 5:4:3:2:0)')[:CAP],
          'Three supports at 5 marks on a 5:4:3:2:0 ladder — the finest grading here, so a partly-developed support still scores well. Evaluate, so say who each support helps and how. Reasonable accommodations for state exams and assistive technology are the two most developable.')],
    'One flat list, taken in order to the cap.',
    stem='‘Education gives people the opportunity and ability to improve their own lives.’ (www.legalstudymatieral.com)'))

ch = block(E3a, '3 factors @ 5 marks (graded 5:3:0) cost of school books')
cards.append(C(
    PFX + 'q3aiii', Y, LV, 'home-economics-3-10', 'socio-economic-status-and-educational-opportunity',
    '2024 HL Section C E3 Q3(a)(iii)',
    'Analyse how socio-economic status impacts equality of opportunity in education.',
    '3 factors @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'How socio-economic status impacts equality of opportunity', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0 — no 4, so a factor named without its effect drops to 3. The list runs both ways: costs that hold families back, and the schemes (book rental, clothing and footwear allowance, student grant, DEIS) that offset them. Using one of each shows the analysis the verb asks for.')],
    'One flat list, taken in order to the cap.',
    stem='‘Education gives people the opportunity and ability to improve their own lives.’ (www.legalstudymatieral.com)'))

E3b = block(E3, 'and 3.(b) While Ireland’s unemployment', 'or 3.(c)')
GRP = ['migrants; ethnic groups', 'early school leavers', 'people with criminal records',
       'people with illnesses', 'homeless people', 'long term unemployed']
gb = heads(block(E3b, 'migrants; ethnic groups', '(ii) Name and give details'), GRP)
cards.append(C(
    PFX + 'q3bi', Y, LV, 'home-economics-3-9', 'groups-excluded-from-the-labour-market',
    '2024 HL Section C E3 Q3(b)(i)',
    'Identify three groups of people who have difficulty in securing employment and discuss the reason why each group identified have high unemployment rates.',
    '3 points @ 6 marks (graded 6:4:2:0)', 18,
    [anyN('r-1', 'Groups with difficulty securing employment, and why', 18, 3, 6,
          [bundle(h) for h in gb][:CAP],
          'Three at 6 marks on a 6:4:2:0 ladder. Naming the group alone is 2 — the other 4 come from the reason, and the scheme prints a specific reason for each group (language and unrecognised qualifications for migrants, no formal qualifications for early school leavers, discrimination and transport for people with disabilities). Identify and explain, every time.')],
    'One option per group, each carrying that group\'s own reasons, because the question ties the reason to the group identified.',
    stem='While Ireland’s unemployment figures are at a record low, some people may be excluded from the labour market.'))

ch = block(E3b, 'co-operatives formed by group of people')
h_co, h_cot = heads(ch, ['co-operatives formed by', 'cottage industries seen an increase'])
o_names = ['co-operatives', 'cottage industries'] + semis(block(ch, 'Accept farmers markets'), 'Accept')
cards.append(C(
    PFX + 'q3bii', Y, LV, 'home-economics-3-9', 'community-based-employment-initiatives',
    '2024 HL Section C E3 Q3(b)(ii)',
    'Name and give details of one community-based initiative that helps to create employment.',
    'Name 1 @ 4 marks; explain 2 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Community-based initiatives that create employment', 4, 1, 4, o_names[:CAP],
          'Name one, 4 marks, graded 4:2:0. Co-operatives and cottage industries are the two the scheme details in full, so they are the safe choices — the accepted extras (farmers markets, artisan producers, community café) score the name but leave you to supply the detail yourself.'),
     anyN('r-2', 'Details of the initiative', 8, 2, 4,
          (semis(h_co, 'co-operatives') + semis(h_cot, 'cottage industries'))[:CAP],
          'Two points at 4 marks, graded 4:2:0 — two thirds of the marks. For a co-operative the marks are in pooled resources, the sectors it operates in, and profits returning to members; for a cottage industry, small-scale home-based production of unique goods of superior quality.')],
    'Fixed: naming is priced at 4 and the two detail points at 8. The details row pools the scheme\'s two fully-described initiatives.',
    stem='While Ireland’s unemployment figures are at a record low, some people may be excluded from the labour market.',
    tariff_kind='fixed'))

E3c = block(E3, 'or 3.(c) ‘Leisure is not wasteful')
ch = block(E3c, 'physical development help with physical fitness', '(ii) Analyse the social and cultural')
h_p, h_s, h_e = heads(ch, ['physical development help', 'social development social outlets', 'emotional development relax'])
cards.append(C(
    PFX + 'q3ci', Y, LV, 'home-economics-3-11', 'leisure-and-family-development',
    '2024 HL Section C E3 Q3(c)(i)',
    'Evaluate how individual and family leisure activities contribute to the physical, social and emotional development of family members.',
    '3 points @ 6 marks (graded 6:4:2:0)', 18,
    [anyN('r-1', 'physical development', 6, 1, 6, semis(h_p, 'physical development')[:CAP],
          'One point, 6 marks, on a 6:4:2:0 ladder — so this is a developed paragraph, not a phrase. Fitness, muscle strength, energy, weight control, bone density.'),
     anyN('r-2', 'social development', 6, 1, 6, semis(h_s, 'social development')[:CAP],
          'One point, 6 marks, 6:4:2:0. Meeting people with shared interests, building friendships, teamwork and leadership, and preventing loneliness and isolation.'),
     anyN('r-3', 'emotional development', 6, 1, 6, semis(h_e, 'emotional development')[:CAP],
          'One point, 6 marks, 6:4:2:0. Relaxation, self-esteem, coping with success and failure, a sense of belonging. Teamwork and leadership appear under both social and emotional, so that one point can be used either way — but not twice.')],
    'Fixed: the scheme requires one reference to each of the three named areas, so all three must be attempted. Missing one costs a straight 6.',
    stem='‘Leisure is not wasteful or an unproductive use of time; its benefits are far reaching.’ (www.physologytoday.com)',
    tariff_kind='fixed'))

ch = block(E3c, 'social factors leisure activities of socio-economic')
h_sf, h_cf = heads(ch, ['social factors leisure activities', 'cultural factors certain activities'])
o_sf, o_cf = semis(h_sf, 'social factors'), semis(h_cf, 'cultural factors')
cards.append(C(
    PFX + 'q3cii', Y, LV, 'home-economics-3-11', 'social-and-cultural-influences-on-leisure',
    '2024 HL Section C E3 Q3(c)(ii)',
    'Analyse the social and cultural factors that influence an individual’s choice of leisure activities.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'social factors', 4, 1, 4, o_sf[:CAP],
          'One point, 4 marks, graded 4:2:0. Social factors are about position and money — socio-economic group, status, income, what amenities exist locally, and who is influencing the trend.'),
     anyN('r-2', 'cultural factors', 4, 1, 4, o_cf[:CAP],
          'One point, 4 marks, graded 4:2:0. Cultural factors are about place and tradition — sports tied to particular counties, the sporting or dance culture of a community, and the wider range that multicultural Ireland has brought.'),
     anyN('r-3', 'One further point, from either heading', 4, 1, 4, (o_sf + o_cf)[:CAP],
          'The scheme reads "1 reference to social factors, 1 reference to cultural factors & 1 other point", so the third floats.')],
    'Fixed: one point pinned to each named factor and one floating.',
    stem='‘Leisure is not wasteful or an unproductive use of time; its benefits are far reaching.’ (www.physologytoday.com)',
    tariff_kind='fixed'))

# ------------------------------------------------------- Question 4 (Core)
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) ‘Fats are essential', 'and 4.(b)')
NUT = ['protein trace amounts', 'fat 82% fat in butter', 'carbohydrates (trace amount in suet)',
       'Vitamin A (retinol)', 'Vitamin D needed', 'Vitamin E trace amounts', 'calcium trace amounts',
       'sodium can be added', 'water content is in proportion']
ch = block(Q4a, 'protein trace amounts', '(ii) Outline the stages')
cards.append(C(
    PFX + 'q4ai', Y, LV, 'home-economics-0-7', 'nutritional-significance-of-fats-and-oils',
    '2024 HL Section C Q4(a)(i) - Core',
    'Evaluate the nutritional significance of fats and oils in the diet.',
    '5 points @ 4 marks (graded 4:3:2:1:0)', 20,
    [anyN('r-1', 'Nutritional significance of fats and oils', 20, 5, 4,
          [bundle(h, '', 4) for h in heads(ch, NUT)][:CAP],
          'Five points at 4 marks on a 4:3:2:1:0 ladder — the finest grading on the paper, so partial credit is real. The scheme groups its marking points under nine nutrients and prices five, so take one nutrient per point: give the amount present and what it does. The fat heading is the richest — saturated in butter and animal fats, monounsaturated in olive oil, polyunsaturated in vegetable and nut oils, LDL against HDL cholesterol.')],
    'One option per nutrient heading rather than one per fragment: the scheme prints nine nutrient blocks and prices five points, so a student picks nutrients, not sentences.',
    stem='‘Fats are essential for health; but choosing the correct types and amount is vital.’ (www.fsai.ie)'))

STAGE = ['oil extraction oil is extracted', 'hydrogenation hydrogen gas', 'other ingredients added skimmed milk',
         'emulsification lecithin', 'churning votator', 'weighed retail portions']
sb = heads(block(Q4a, 'oil extraction oil is extracted', 'packaging foil wrap'), STAGE)
o_pl = (semis(block(Q4a, 'packaging foil wrap', 'labelling brand name'), 'packaging')
        + semis(block(Q4a, 'labelling brand name', END), 'labelling'))
cards.append(C(
    PFX + 'q4aii', Y, LV, 'home-economics-0-11', 'production-of-margarine',
    '2024 HL Section C Q4(a)(ii) - Core',
    'Outline the stages involved in the production of margarine to include details of packaging and labelling.',
    'Stages 5 points @ 2 marks (graded 2:1:0); packaging and labelling 5 points @ 1 mark (graded 1:0)', 15,
    [anyN('r-1', 'Stages in the production of margarine', 10, 5, 2,
          [bundle(h, ' '.join(p.split()[:2]), 2) for h, p in zip(sb, STAGE)][:CAP],
          'Five stages at 2 marks, graded 2:1:0. The scheme states that hydrogenation is an essential point, so it must appear — hydrogen forced into the unsaturated oil at the double bonds over a nickel catalyst, turning liquid oil into semi-solid fat. Take the rest in process order.'),
     anyN('r-2', 'Packaging and labelling', 5, 5, 1, o_pl[:CAP],
          'Five points at 1 mark each, graded 1:0 — one word or phrase each, all-or-nothing. Five of the cheapest marks in Section C, and almost all of them are on the label: brand name, type, ingredients, allergens, expiry date, storage, weight, nutritional information.')],
    'Fixed: the process is priced at 10 and packaging and labelling at 5. Hydrogenation is compulsory within the first row, which the row note carries.',
    stem='‘Fats are essential for health; but choosing the correct types and amount is vital.’ (www.fsai.ie)',
    tariff_kind='fixed'))

IMPL = ['obesity regular consumption', 'coronary heart disease LDL', 'high blood pressure too much',
        'type 2 diabetes extra weight', 'gall stones small stones', 'varicose veins pressure',
        'infertility if overweight']
ch = block(Q4a, 'obesity regular consumption')
cards.append(C(
    PFX + 'q4aiii', Y, LV, 'home-economics-0-7', 'health-implications-of-saturated-fat',
    '2024 HL Section C Q4(a)(iii) - Core',
    'Assess the health implications for a person consuming a diet high in saturated fat.',
    '3 health implications @ 5 marks (graded 5:4:3:2:1:0)', 15,
    [anyN('r-1', 'Health implications of a diet high in saturated fat', 15, 3, 5,
          [bundle(h, ' '.join(p.split()[:2])) for h, p in zip(heads(ch, IMPL), IMPL)][:CAP],
          'Three implications at 5 marks on a 5:4:3:2:1:0 ladder — six grades, the finest on the paper, so every sentence of mechanism adds a mark. Assess means naming the condition is not enough: say how the saturated fat causes it. The scheme gives the chain for each — LDL building up in arteries, extra weight making insulin less effective, cholesterol forming gall stones.')],
    'One option per named condition, each carrying the scheme\'s own mechanism for it.',
    stem='‘Fats are essential for health; but choosing the correct types and amount is vital.’ (www.fsai.ie)'))

Q4b = block(Q4, 'and 4.(b) The use of household resources', 'or Leaving Certificate Examination 2024')
ch = block(Q4b, '3 points @ 4 marks (graded 4:2:0) cost', '(ii) Set out details')
cards.append(C(
    PFX + 'q4bi', Y, LV, 'home-economics-1-4', 'selection-criteria-household-textiles',
    '2024 HL Section C Q4(b)(i) - Core',
    'Assess the selection criteria that should be considered when choosing household textiles.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Selection criteria for household textiles', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three criteria at 4 marks, graded 4:2:0 — naming the criterion is 2, and assessing it takes the other 2. Tie each to the room and the use: ease of cleaning matters for a kitchen, durability for a stair carpet, safety for children\'s furnishings.')],
    'One flat list, taken in order to the cap.',
    stem='The use of household resources play a valuable role in everyday living.'))

ch = block(Q4b, '• working principle 3 points @ 2 marks (graded 2:1:0)')
o_wp = semis(block(ch, '• working principle', '• guidelines for use'), '• working principle 3 points @ 2 marks (graded 2:1:0)')
o_gu = semis(block(ch, '• guidelines for use', '• energy efficiency'), '• guidelines for use 3 points @ 2 marks (graded 2:1:0)')
o_ee = semis(block(ch, '• energy efficiency'), '• energy efficiency 2 points @ 2 marks (graded 2:1:0)')
cards.append(C(
    PFX + 'q4bii-study', Y, LV, 'home-economics-1-3', 'appliance-with-a-motor-study',
    '2024 HL Section C Q4(b)(ii) - Core - working principle, use and efficiency',
    'Set out details of a study you have carried out on one type of electrical appliance with a motor. Refer to: working principle; guidelines for use; energy efficiency.',
    'Working principle 3 @ 2 marks; guidelines 3 @ 2 marks; energy efficiency 2 @ 2 marks (graded 2:1:0)', 16,
    [anyN('r-1', 'Working principle', 6, 3, 2, o_wp[:CAP],
          'Three points at 2 marks, graded 2:1:0. The scheme\'s chain works for any motor appliance: electricity drives the motor, the motor turns the belt, the belt spins the parts, the parts do the job. Labelled diagrams are accepted here.'),
     anyN('r-2', 'Guidelines for use', 6, 3, 2, o_gu[:CAP],
          'Three points at 2 marks, graded 2:1:0. Correct attachment for the job, do not overfill, rest it to avoid overheating, use the safety features.'),
     anyN('r-3', 'Energy efficiency', 4, 2, 2, o_ee[:CAP],
          'Two points at 2 marks, graded 2:1:0. Do not overfill, choose A-rated, do not run it for long stretches, match the size of the appliance to the job.')],
    'The three listed strands of Q4(b)(ii), worth 16 of the part\'s 18 marks. The remaining 2 are for naming the appliance, and the scheme prints no list for it — it reads "Accept all household appliances with motor", so any motor appliance scores and there is nothing to show.',
    stem='The use of household resources play a valuable role in everyday living.',
    tariff_kind='fixed'))

Q4c = block(Q4, '4.(c) ‘Sensory analysis testing')
ch = block(Q4c, '5 points @ 3 marks (graded 3:2:0) silence', '(ii) Evaluate the role of artisan')
cards.append(C(
    PFX + 'q4ci', Y, LV, 'home-economics-0-11', 'conditions-for-sensory-analysis-testing',
    '2024 HL Section C Q4(c)(i) - Core',
    'Describe the conditions necessary to follow for sensory analysis testing in the classroom to ensure accurate results.',
    '5 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'Conditions necessary for sensory analysis testing', 15, 5, 3,
          semis(ch, '5 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Five conditions at 3 marks, graded 3:2:0 — naming the condition is 2, saying what it protects against is 3. The point of every one is removing bias: silence so tasters do not influence each other, coded samples so they cannot guess, a palate cleanser so one sample does not carry into the next.')],
    'One flat list, taken in order to the cap.',
    stem='‘Sensory analysis testing provides food developers and companies with valuable, insightful information.’ (www.intertek.com)'))

ch = block(Q4c, '3 points @ 5 marks (graded 5:3:0) speciality foods', END)
cards.append(C(
    PFX + 'q4cii', Y, LV, 'home-economics-0-11', 'artisan-producers-in-the-irish-food-industry',
    '2024 HL Section C Q4(c)(ii) - Core',
    'Evaluate the role of artisan producers/small businesses in the Irish food industry.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Role of artisan producers and small businesses', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0 — no 4, so a point without development drops to 3. The list runs from how they produce (limited quantities, traditional non-industrial skills, family run) to what they do for the country (rural employment, promoting the local area, Ireland\'s reputation for high-quality food). One from each end reads as genuine evaluation.')],
    'One flat list, taken in order to the cap.',
    stem='‘Sensory analysis testing provides food developers and companies with valuable, insightful information.’ (www.intertek.com)'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2024hl_secC.json'), 'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
