"""2023 Higher Level, Section C."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2023, 'higher')
SEC = tidy(T[28125:55919])
Y, LV, PFX, CAP = 2023, 'higher', 'he-2023-hl-sc-', 14
cards, held = [], []
def C(*a, **k):
    k.setdefault('section', 'C'); return card(*a, **k)
def bundle(h, prefix='', n=None):
    seg = semis(h, prefix); return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 –', 'Elective 2 –')
E1a = block(E1, '1.(a) ‘Ireland’s Better Energy', 'and 1.(b)')
ch = block(E1a, '2 points on each heading + 1 other', '(ii) Discuss levels of thermal comfort')
h_aes, h_env = heads(ch, ['aesthetic and comfort factors elements', 'environmental awareness impact'])
o_aes, o_env = semis(h_aes, 'aesthetic and comfort factors'), semis(h_env, 'environmental awareness')
cards.append(C(
    PFX+'q1ai', Y, LV, 'home-economics-3-4', 'factors-influencing-interior-design',
    '2023 HL Section C E1 Q1(a)(i)',
    'Describe the factors that influence interior design in the home. Refer to: aesthetic and comfort factors; environmental awareness.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'aesthetic and comfort factors', 8, 2, 4, o_aes[:CAP],
          'Two points at 4 marks, graded 4:2:0 — the longer of the two lists, covering both halves of the heading: how a room looks (elements and principles of design, personal taste, trends) and how it works to live in (comfort, heating, lighting, ergonomics).'),
     anyN('r-2', 'environmental awareness', 8, 2, 4, o_env[:CAP],
          'Two points at 4 marks, graded 4:2:0. The scheme runs the whole product life cycle — making it, using it, disposing of it — plus where the materials came from. Reuse, recycle and repurpose are three separate options.'),
     anyN('r-3', 'One further point, from either heading', 4, 1, 4, (o_aes + o_env)[:CAP],
          'The scheme reads "2 points on each heading + 1 other", so the fifth point floats.')],
    'Fixed: two points pinned to each named heading and the fifth floating. Ignoring a heading caps you at 12 of 20.',
    stem='‘Ireland’s Better Energy Warmer Homes scheme aims to help individuals make their homes warmer, healthier and cheaper to run.’ (www.seai.ie)',
    tariff_kind='fixed'))

ch = block(E1a, 'depends on room function', '(iii) Explain the underlying principle')
o_t = semis(ch, '')
cards.append(C(
    PFX+'q1aii', Y, LV, 'home-economics-3-5', 'thermal-comfort-in-living-spaces',
    '2023 HL Section C E1 Q1(a)(ii)',
    'Discuss levels of thermal comfort in relation to two different living spaces in the home.',
    '2 points @ 6 marks: identify room @ 2 marks (graded 2:0), discussion @ 4 marks (graded 4:2:0), x2', 12,
    [anyN('r-1', 'Rooms identified', 4, 2, 2, ['living rooms', 'bedrooms', 'kitchens', 'bathrooms'],
          'Two rooms named, 2 marks each, graded 2:0 — all-or-nothing and almost free. Name them before you discuss anything.'),
     anyN('r-2', 'Thermal comfort in the rooms identified', 8, 2, 4, o_t[:CAP],
          'Two discussions at 4 marks, graded 4:2:0. The temperature ranges are the marks and they differ sharply by room — living rooms 17–21°C, bedrooms 10–16°C, kitchens 15–19°C, bathrooms 16–19°C. Quote the range and say why the room needs it. A minimum of 20°C is recommended for older people whatever the room.')],
    'Fixed: the scheme prices naming the room separately from discussing it, twice over, so the card splits them into a naming row and a discussion row.',
    stem='‘Ireland’s Better Energy Warmer Homes scheme aims to help individuals make their homes warmer, healthier and cheaper to run.’ (www.seai.ie)',
    tariff_kind='fixed'))

ch = block(E1a, 'underlying principle based on the principle of thermal expansion')
h_p, h_u = heads(ch, ['underlying principle based', 'use in the home central heating'])
cards.append(C(
    PFX+'q1aiii', Y, LV, 'home-economics-3-5', 'thermostat-principle-and-use',
    '2023 HL Section C E1 Q1(a)(iii)',
    'Explain the underlying principle of a thermostat and describe how it can be used in the home.',
    'Underlying principle 4 points @ 3 marks; use in the home 2 points @ 3 marks (graded 3:2:0)', 18,
    [anyN('r-1', 'Underlying principle of a thermostat', 12, 4, 3, semis(h_p, 'underlying principle')[:CAP],
          'Four points at 3 marks, graded 3:2:0 — twelve of the eighteen marks. The scheme wants the bimetal strip in sequence: two metals, brass expands readily and invar barely, so the strip bends on heating, which breaks the circuit and switches the appliance off, and it straightens on cooling to switch it back on. That chain is four points on its own.'),
     anyN('r-2', 'Use in the home', 6, 2, 3, semis(h_u, 'use in the home')[:CAP],
          'Two points at 3 marks, graded 3:2:0. Ten appliances are accepted, so this half should never be lost — name the appliance and say what the thermostat holds steady in it.')],
    'Fixed: the principle is priced at 12 and the uses at 6, so two thirds of the marks are in the physics.',
    stem='‘Ireland’s Better Energy Warmer Homes scheme aims to help individuals make their homes warmer, healthier and cheaper to run.’ (www.seai.ie)',
    tariff_kind='fixed'))

E1b = block(E1, 'and 1.(b) ‘Lighting ideas', 'or 1.(c)')
held.append(dict(C(
    PFX+'q1bi', Y, LV, 'home-economics-3-5', 'properties-of-light-in-the-home',
    '2023 HL Section C E1 Q1(b)(i)',
    'Describe four properties of light and give an example of how each property is used in the home.',
    'Name 4 @ 2 marks; description 4 @ 2 marks; example 4 @ 1 mark', 20,
    [anyN('r-1', 'Properties of light', 8, 4, 2,
          ['Reflected', 'Diffused', 'Absorbed', 'Dispersed', 'Refracted'],
          'Four properties named, 2 marks each, graded 2:0.')],
    'Held — see heldReason.',
    stem='‘Lighting ideas are an essential part of space design.’ (www.homesandgardens.com)'),
    heldReason='The scheme prints this as a three-column table (Property / Explanation / Example) and the PDF extraction interleaves the columns line by line: the Diffused row reads "Rays of light are scattered when they pass net curtains; frosted glass; through translucent substances or hit a non- translucent lampshades; etc. reflecting surface". Explanation and example cannot be separated from the markdown with confidence, and both historical scheme corruptions in this repo came from reconstructing a table by hand. Needs the columns re-extracted from the PDF.'))

ch = block(E1b, 'CFL/Fluorescents lights made compact')
h_cfl, h_led = heads(ch, ['CFL/Fluorescents lights made', 'LED (Light Emitting Diode) when switched'])
cards.append(C(
    PFX+'q1bii', Y, LV, 'home-economics-3-6', 'energy-efficient-lighting-principle',
    '2023 HL Section C E1 Q1(b)(ii)',
    'Explain the underlying principle of one type of energy-efficient lighting.',
    'Name 4 marks (graded 4:2:0); underlying principle 2 points @ 3 marks (graded 3:2:0)', 10,
    [anyN('r-1', 'Types of energy-efficient lighting', 4, 1, 4,
          ['CFL/Fluorescents', 'LED (Light Emitting Diode)'],
          'Name one, 4 marks, graded 4:2:0. Only two are accepted, and the CFL has by far the longer explanation in the scheme — name that one unless you are confident on the LED semiconductor account.'),
     anyN('r-2', 'Underlying principle of the type named', 6, 2, 3,
          (semis(h_cfl, 'CFL/Fluorescents') + semis(h_led, 'LED (Light Emitting Diode)'))[:CAP],
          'Two points at 3 marks, graded 3:2:0. For the CFL the chain is: a phosphor-coated tube holding argon and mercury, electrodes heat up and vaporise the mercury, the gas reacts with the phosphor and it glows. For the LED it is electroluminescence — electrons combine with holes and release photons.')],
    'Fixed: the name is priced at 4 and the principle at 6. The principle row pools both accepted types, because the two points are awarded for whichever was named.',
    stem='‘Lighting ideas are an essential part of space design.’ (www.homesandgardens.com)',
    tariff_kind='fixed'))

E1c = block(E1, 'or 1.(c) ‘We have been forced to rethink')
ch = block(E1c, 'environmental factors energy efficiency', '(ii) Describe the impact of burning')
h_en, h_ec, h_so = heads(ch, ['environmental factors energy', 'economic factors household income', 'social factors personal likes'])
cards.append(C(
    PFX+'q1ci', Y, LV, 'home-economics-3-3', 'factors-influencing-housing-style-choice',
    '2023 HL Section C E1 Q1(c)(i)',
    'Discuss how environmental, economic and social factors influence the choice of housing styles in Ireland today.',
    '3 points @ 6 marks (graded 6:4:2:0)', 18,
    [anyN('r-1', 'environmental factors', 6, 1, 6, semis(h_en, 'environmental factors')[:CAP],
          'One point, 6 marks, on a 6:4:2:0 ladder — a developed paragraph, not a phrase. Energy efficiency, the aspect of the site, local materials, climate and building regulations.'),
     anyN('r-2', 'economic factors', 6, 1, 6, semis(h_ec, 'economic factors')[:CAP],
          'One point, 6 marks, 6:4:2:0. The longest list: income, site cost, size and style, materials, bills, and the resale or investment value.'),
     anyN('r-3', 'social factors', 6, 1, 6, semis(h_so, 'social factors')[:CAP],
          'One point, 6 marks, 6:4:2:0. Personal taste, location, what the family needs, a member with special needs, and local tradition.')],
    'Fixed: the scheme expects one point on each named factor, so all three must be attempted. Missing one costs a straight 6.',
    stem='‘We have been forced to rethink how we live in our homes in recent years.’ (The Irish Times)',
    tariff_kind='fixed'))

ch = block(E1c, 'Emissions carbon dioxide')
h_em, h_ef, h_st = heads(ch, ['Emissions carbon dioxide', 'effects on the environment increasing',
                              'a strategy households could implement in order to reduce emissions use renewable'])
cards.append(C(
    PFX+'q1cii', Y, LV, 'home-economics-3-6', 'impact-of-burning-fossil-fuels',
    '2023 HL Section C E1 Q1(c)(ii)',
    'Describe the impact of burning fossil fuels in the home. Refer to: an emission produced by burning fossil fuels; effects on the environment; a strategy households could implement in order to reduce emissions.',
    'Emission 1 @ 3 marks (graded 3:0); effects 2 points @ 3 marks; strategy 1 point @ 3 marks (graded 3:2:0)', 12,
    [anyN('r-1', 'An emission produced by burning fossil fuels', 3, 1, 3, semis(h_em, 'Emissions')[:CAP],
          'Name one emission, 3 marks, graded 3:0 — all-or-nothing, and naming a second adds nothing. Six are accepted, so this is three free marks.'),
     anyN('r-2', 'Effects on the environment', 6, 2, 3, semis(h_ef, 'effects on the environment')[:CAP],
          'Two effects at 3 marks, graded 3:2:0. The scheme goes past "climate change" to the consequences — rising sea levels, damage to crops, spread of infectious disease, shifting plant and animal ranges. Naming the effect is 2; saying what it does is 3.'),
     anyN('r-3', 'A strategy households could implement', 3, 1, 3, semis(h_st, 'a strategy households could implement in order to reduce emissions')[:CAP],
          'One strategy, 3 marks, graded 3:2:0. It must be something a household can actually do — switch to renewables or smokeless fuel, fit timers and thermostats, stop burning rubbish.')],
    'Fixed: three headings named in the question, priced 3 / 6 / 3.',
    stem='‘We have been forced to rethink how we live in our homes in recent years.’ (The Irish Times)',
    tariff_kind='fixed'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 –', 'Elective 3 –')
E2a = block(E2, '2.(a) A special occasion', 'and 2.(b)')
ch = block(E2a, 'sketch should show detail', '(ii) Suggest a suitable fabric')
h_sk, h_de = heads(ch, ['sketch should show detail', 'description colour'])
cards.append(C(
    PFX+'q2ai', Y, LV, 'home-economics-3-8', 'sketching-and-describing-an-outfit',
    '2023 HL Section C E2 Q2(a)(i)',
    'Sketch and describe an outfit to wear for your graduation ball.',
    'Sketch 6 marks (graded 6:4:2:0); description 3 points @ 2 marks (graded 2:1:0)', 12,
    [anyN('r-1', 'The sketch', 6, 1, 6, semis(h_sk, 'sketch')[:CAP],
          'Six marks for the drawing, on a 6:4:2:0 ladder — half the part. The scheme wants design features visible and labelled: line, shape, proportion and harmony. Label the sketch; an unlabelled drawing cannot show the examiner you knew what you were doing.'),
     anyN('r-2', 'Description of the outfit', 6, 3, 2, semis(h_de, 'description')[:CAP],
          'Three points at 2 marks, graded 2:1:0 — short items, not sentences. Twelve features are accepted, so pick three that are actually visible in your sketch.')],
    'Fixed: the sketch is priced at 6 and the description at 6. The sketch is the candidate\'s own drawing, so unlike the outfit-evaluation questions on other papers this needs no figure from the exam paper.',
    stem='A special occasion is an opportunity for an individual to showcase their unique sense of style.',
    tariff_kind='fixed'))

ch = block(E2a, 'fabric silk; satin', '(iii) Name one design principle')
h_fa, h_re = heads(ch, ['fabric silk', 'reason lightweight'])
cards.append(C(
    PFX+'q2aii', Y, LV, 'home-economics-3-7', 'choosing-a-fabric-for-an-outfit',
    '2023 HL Section C E2 Q2(a)(ii)',
    'Suggest a suitable fabric for the outfit and give a reason for your answer.',
    'Fabric 3 marks (graded 3:0); reason 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Suitable fabrics', 3, 1, 3, semis(h_fa, 'fabric')[:CAP],
          'Name one fabric, 3 marks, graded 3:0 — all-or-nothing. Seven are accepted.'),
     anyN('r-2', 'Reason for the choice', 3, 1, 3, semis(h_re, 'reason')[:CAP],
          'One reason, 3 marks, graded 3:2:0. The reason must be a property of the fabric you named — drape and sheerness for chiffon, warmth for wool. A reason that would suit any fabric is 2.')],
    'Fixed: the fabric is priced at 3 and the reason at 3.',
    stem='A special occasion is an opportunity for an individual to showcase their unique sense of style.',
    tariff_kind='fixed'))

PRIN = ['balance can be vertical', 'emphasis achieved through', 'proportion relationship between', 'rhythm associated with']
ch = block(E2a, 'balance can be vertical')
cards.append(C(
    PFX+'q2aiii', Y, LV, 'home-economics-3-8', 'design-principle-applied-to-an-outfit',
    '2023 HL Section C E2 Q2(a)(iii)',
    'Name one design principle and evaluate how it applies to your outfit.',
    'Name 2 marks (graded 2:0); evaluate 5 marks (graded 5:3:0)', 7,
    [anyN('r-1', 'Design principles', 2, 1, 2, ['balance', 'emphasis', 'proportion', 'rhythm'],
          'Name one, 2 marks, graded 2:0 — all-or-nothing. Only these four are accepted.'),
     anyN('r-2', 'How the principle applies to your outfit', 5, 1, 5,
          [x for h, p in zip(heads(ch, PRIN), PRIN) for x in semis(h, p.split()[0])][:CAP],
          'One evaluation, 5 marks, graded 5:3:0 — no 4, so a definition of the principle with no reference to your own outfit drops to 3. Say where in the outfit it appears. Emphasis is the easiest: the scheme notes there should be only one centre of emphasis, so naming yours and saying why it works is a full answer.')],
    'Fixed: the name is priced at 2 and the evaluation at 5. The evaluation row pools all four principles, because the 5 marks are awarded for whichever was named.',
    stem='A special occasion is an opportunity for an individual to showcase their unique sense of style.',
    tariff_kind='fixed'))

E2b = block(E2, 'and 2.(b) Blended fabrics', 'or 2.(c)')
pb = heads(block(E2b, 'Production Blend: Wool and Nylon', 'Properties wool warm'),
           ['wool fleece is graded', 'nylon two chemicals', 'cotton boll is harvested',
            'polyester viscous liquid', 'Blending combinations'])
qb = heads(block(E2b, 'Properties wool warm', 'Uses clothing'),
           ['wool warm', 'nylon strong', 'cotton strong', 'polyester strong'])
o_uses = semis(block(E2b, 'Uses clothing'), 'Uses')
BLEND = [('wool-nylon', 'Wool and Nylon', 0, 1, 0, 1), ('cotton-polyester', 'Cotton and Polyester', 2, 3, 2, 3)]
for slug, name, pa, pbi, qa, qbi in BLEND:
    a, b = name.split(' and ')
    cards.append(C(
        PFX+'q2b-'+slug, Y, LV, 'home-economics-3-7', f'blended-fabric-profile-{slug}',
        f'2023 HL Section C E2 Q2(b) - {name}',
        'Write a profile of one blended fabric. Refer to: fabric production; fabric properties; uses.',
        'Production 3 points @ 3 marks (graded 3:2:0); properties 3 points @ 1 mark; uses 3 points @ 1 mark', 15,
        [anyN('r-1', f'Production of a {name.lower()} blend', 9, 3, 3,
              (semis(pb[pa], a.lower()) + semis(pb[pbi], b.lower()) + semis(pb[4], 'Blending'))[:CAP],
              f'Three points at 3 marks, graded 3:2:0 — nine of the fifteen marks. A blend has three production stories and the scheme credits all of them: how {a.lower()} is prepared, how {b.lower()} is made, and how the two are blended by weaving in the warp and weft.'),
         anyN('r-2', 'Properties of the blend', 3, 3, 1,
              (semis(qb[qa], a.lower()) + semis(qb[qbi], b.lower()))[:CAP],
              f'Three properties at 1 mark each, graded 1:0 — one word each, all-or-nothing. The point of a blend is that it takes the best of both, so mix them: {a.lower()}\'s properties and {b.lower()}\'s.'),
         anyN('r-3', 'Uses', 3, 3, 1, o_uses[:CAP],
              'Three uses at 1 mark each, graded 1:0. Four are accepted and they are one word each — three of the cheapest marks in the elective, so never leave this row blank.')],
        'One of two blends the scheme details. A candidate profiles a single blended fabric, so each blend is its own card with its own questionRef. The uses list is common to both.',
        stem='Blended fabrics have combined properties of each component fibre.',
        tariff_kind='fixed'))

E2c = block(E2, 'or 2.(c) ‘The vintage clothing industry')
ch = block(E2c, 'pattern bold statement patterns', '(ii) Name and give details')
h_pa, h_in, h_ac = heads(ch, ['pattern bold statement', 'influences contemporary', 'accessories draws attention'])
cards.append(C(
    PFX+'q2ci', Y, LV, 'home-economics-3-8', 'vintage-clothing-as-a-fashion-trend',
    '2023 HL Section C E2 Q2(c)(i)',
    'Discuss the emergence of vintage clothing as a current fashion trend. Refer to: pattern; influences; accessories.',
    '3 points @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'pattern', 3, 1, 3, semis(h_pa, 'pattern')[:CAP],
          'One point, 3 marks, graded 3:2:0. Bold, eye-catching, retro, unique — the appeal is that the pattern is not what everyone else is wearing.'),
     anyN('r-2', 'influences', 3, 1, 3, semis(h_in, 'influences')[:CAP],
          'One point, 3 marks, graded 3:2:0. Sustainability is the driver the scheme leads with, along with organic fabrics and up-cycling.'),
     anyN('r-3', 'accessories', 3, 1, 3, semis(h_ac, 'accessories')[:CAP],
          'One point, 3 marks, graded 3:2:0. What the accessory does for the outfit — draws attention, brightens it, ties it together.')],
    'Fixed: three headings named in the question, priced identically. A nine-mark part, so keep each to a sentence or two.',
    stem='‘The vintage clothing industry is growing 25 times faster than the overall retail market.’ (www.rediscoverycentre.ie)',
    tariff_kind='fixed'))

ch = block(E2c, 'fashion designers; tailors')
held.append(dict(C(
    PFX+'q2cii', Y, LV, 'home-economics-3-8', 'careers-in-clothing-and-textiles',
    '2023 HL Section C E2 Q2(c)(ii)',
    'Name and give details of one career opportunity in the clothing and textile industry.',
    'Name 1 point @ 2 marks (graded 2:0); detail 1 point @ 4 marks (graded 4:2:0)', 6,
    [anyN('r-1', 'Careers in the clothing and textile industry', 2, 1, 2, semis(ch, '')[:CAP],
          'Name one, 2 marks, graded 2:0.')],
    'Held — see heldReason.',
    stem='‘The vintage clothing industry is growing 25 times faster than the overall retail market.’ (www.rediscoverycentre.ie)'),
    heldReason='The scheme prints the list of career names and no marking points at all for the detail point, which carries 4 of the part\'s 6 marks. Unlike the naming strands split out on other papers, what is left here is a 2-mark card, too thin to ship on its own.'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 –', 'Question 4 – Core')
E3a = block(E3, '3.(a) ‘We are currently witnessing', 'and 3.(b)')
ch = block(E3a, 'technology automation and increased output', '(ii) Describe the impact of dual-earner')
h_t, h_f = heads(ch, ['technology automation', 'flexibility flexi-time'])
o_t, o_f = semis(h_t, 'technology'), semis(h_f, 'flexibility')
cards.append(C(
    PFX+'q3ai', Y, LV, 'home-economics-2-2', 'technology-flexibility-and-patterns-of-work',
    '2023 HL Section C E3 Q3(a)(i)',
    'Discuss how technology and increasing flexibility in working hours affect patterns of work and work availability.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'technology', 4, 1, 4, o_t[:CAP],
          'One point, 4 marks, graded 4:2:0. Evaluate both directions: automation cut hours and cut jobs, manufacturing declined and services grew, and constant electronic contact makes it hard to switch off.'),
     anyN('r-2', 'increasing flexibility in working hours', 4, 1, 4, o_f[:CAP],
          'One point, 4 marks, graded 4:2:0. Name the arrangement (flexi-time, term time, job sharing, working from home, parental leave, career breaks) and say who it lets work who otherwise could not.'),
     anyN('r-3', 'Three further points, from either heading', 12, 3, 4, (o_t + o_f)[:CAP],
          'Twelve of the twenty marks float: the scheme reads "1 point relating to technology and 1 point to increasing flexibility and any other 3 points". Cover both headings first, then take three more from whichever you know better.')],
    'Fixed: one point pinned to each named strand and three floating — the largest floating share in the elective, so breadth on either heading pays.',
    stem='‘We are currently witnessing the nature of employment being redefined in Ireland and across the world.’ (www.skillnetireland.ie)',
    tariff_kind='fixed'))

ch = block(E3a, 'Role overload occurs when', '(iii) Recommend one type of child care')
h_ro, h_rc, h_dp = heads(ch, ['Role overload occurs', 'Role conflict caused', 'Distribution of parental responsibilities in the home greater'])
cards.append(C(
    PFX+'q3aii', Y, LV, 'home-economics-2-0', 'dual-earner-families-role-overload-and-conflict',
    '2023 HL Section C E3 Q3(a)(ii)',
    'Describe the impact of dual-earner families on family life. Refer to: role overload; role conflict; distribution of parental responsibilities in the home.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'role overload', 5, 1, 5, semis(h_ro, 'Role overload')[:CAP],
          'One point, 5 marks, graded 5:3:0 — no 4, so define the term and then give a consequence. Overload is playing several roles at once: less leisure, more stress, promotion prospects hit, nobody free to care for vulnerable family members.'),
     anyN('r-2', 'role conflict', 5, 1, 5, semis(h_rc, 'Role conflict')[:CAP],
          'One point, 5 marks, graded 5:3:0 — the shortest list, so use all of it. Conflict is when what one role expects clashes with another, forcing work or family to be prioritised. Do not confuse it with overload: overload is too much, conflict is incompatible.'),
     anyN('r-3', 'distribution of parental responsibilities in the home', 5, 1, 5,
          semis(h_dp, 'Distribution of parental responsibilities in the home')[:CAP],
          'One point, 5 marks, graded 5:3:0 — the longest list. Both positive and negative score: shared decision-making and both parents active in childcare, but also less time with children, outside help, and extra responsibility falling on older children.')],
    'Fixed: three headings named in the question, priced identically. Role overload and role conflict are the two terms students blur, and the scheme prices them separately.',
    stem='‘We are currently witnessing the nature of employment being redefined in Ireland and across the world.’ (www.skillnetireland.ie)',
    tariff_kind='fixed'))

ch = block(E3a, 'Name 3 marks (graded 3:0), detail 4 points @ 3 marks (graded 3:2:0)')
o_n = semis(block(ch, 'creche; child minder', 'location; opening hours'), '')
o_d = semis(block(ch, 'location; opening hours'), '')
cards.append(C(
    PFX+'q3aiii', Y, LV, 'home-economics-3-11', 'recommending-a-childcare-option',
    '2023 HL Section C E3 Q3(a)(iii)',
    'Recommend one type of child care option available to working parents. Analyse how the chosen child care option meets the requirements of the family.',
    'Name 3 marks (graded 3:0); detail 4 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'Child care options available to working parents', 3, 1, 3, o_n[:CAP],
          'Name one, 3 marks, graded 3:0 — all-or-nothing, and naming a second adds nothing. Eight are accepted. Pick the one you can analyse on four separate criteria, because the other 12 marks hang off it.'),
     anyN('r-2', 'How the option meets the requirements of the family', 12, 4, 3, o_d[:CAP],
          'Four points at 3 marks, graded 3:2:0 — twelve of the fifteen marks. Analyse, so each criterion needs a judgement about the option you recommended, not a definition of the criterion. Suitability to the age of the child and to the needs of the child are separate points.')],
    'Fixed: the name is priced at 3 and the analysis at 12.',
    stem='‘We are currently witnessing the nature of employment being redefined in Ireland and across the world.’ (www.skillnetireland.ie)',
    tariff_kind='fixed'))

E3b = block(E3, 'and 3.(b) ‘One in every nine people', 'or 3.(c)')
ch = block(E3b, 'cycle of deprivation in geographical areas inner cities', '(ii) Name and give details')
h_cd, h_sp = heads(ch, ['cycle of deprivation in geographical areas inner cities', 'the influence of social policy on poverty state responds'])
cards.append(C(
    PFX+'q3bi', Y, LV, 'home-economics-3-9', 'contributory-factors-to-poverty',
    '2023 HL Section C E3 Q3(b)(i)',
    'Analyse the following as contributory factors to poverty in Ireland today: cycle of deprivation in geographical areas; the influence of social policy on poverty.',
    '4 points @ 4 marks (graded 4:2:0), 2 points on each factor', 16,
    [anyN('r-1', 'cycle of deprivation in geographical areas', 8, 2, 4,
          semis(h_cd, 'cycle of deprivation in geographical areas')[:CAP],
          'Two points at 4 marks, graded 4:2:0. Name the kind of area and say why deprivation persists there — inner cities in economic decline, isolated rural areas, large social housing estates, places of long-term high unemployment.'),
     anyN('r-2', 'the influence of social policy on poverty', 8, 2, 4,
          semis(h_sp, 'the influence of social policy on poverty')[:CAP],
          'Two points at 4 marks, graded 4:2:0. The scheme deliberately cuts both ways: welfare meets basic needs, but it can also perpetuate poverty when payments exceed low wages and leaving welfare would mean a financial loss. That is the poverty trap, and naming both directions is the analysis the verb asks for.')],
    'Fixed: two points pinned to each named factor. Writing only about one caps you at 8 of 16.',
    stem='‘One in every nine people in Ireland lives on an income below the poverty line.’ (poverty focus 2022, socialjusticeireland.ie)',
    tariff_kind='fixed'))

SCHEMES = ['working family payment', 'back to school clothing and footwear allowance', 'national fuel scheme',
           'book rental schemes', 'medical cards', 'GP visit card', 'Housing Assistance Payment (HAP)',
           'mortgage allowance scheme']
sb = heads(block(E3b, 'working family payment weekly tax-free'), SCHEMES)
cards.append(C(
    PFX+'q3bii', Y, LV, 'home-economics-3-9', 'statutory-schemes-for-low-income-families',
    '2023 HL Section C E3 Q3(b)(ii)',
    'Name and give details of two statutory schemes that reduce expenditure for low-income families.',
    '(Name 3 marks (graded 3:2:0), detail 4 marks (graded 4:2:0)) x2', 14,
    [anyN('r-1', 'Statutory schemes that reduce expenditure for low-income families', 6, 2, 3,
          SCHEMES[:CAP],
          'Two schemes named, 3 marks each, graded 3:2:0. Eight are accepted, so six marks are there for the taking — but name the two you can then detail, because the other eight marks depend on it.'),
     anyN('r-2', 'Details of the two schemes named', 8, 2, 4,
          [bundle(h, s, 3) for h, s in zip(sb, SCHEMES)][:CAP],
          'Two details at 4 marks, graded 4:2:0. Detail means the rules: who qualifies, what it pays, and who runs it. The Working Family Payment and HAP have the most specific detail in the scheme — a weekly tax-free payment of 60% of the income shortfall for employees with a dependent child, and a local-authority rent payment made directly to the landlord.')],
    'Fixed: naming is priced at 6 and the details at 8. The details row shows one option per scheme, each carrying that scheme\'s own rules.',
    stem='‘One in every nine people in Ireland lives on an income below the poverty line.’ (poverty focus 2022, socialjusticeireland.ie)',
    tariff_kind='fixed'))

E3c = block(E3, 'or 3.(c) ‘Contemporary society')
ch = block(E3c, 'changing attitudes to marriage divorce and separation', '(ii) Describe how the Protection')
h_m, h_p, h_w = heads(ch, ['changing attitudes to marriage divorce', 'parenting roles women as breadwinners',
                           'increased participation of women in the workforce increase in disposable'])
cards.append(C(
    PFX+'q3ci', Y, LV, 'home-economics-2-0', 'impact-of-social-change-on-the-family',
    '2023 HL Section C E3 Q3(c)(i)',
    'Analyse the impact of social change on the family. Refer to: changing attitudes to marriage; parenting roles; increased participation of women in the workforce.',
    '3 points @ 6 marks (graded 6:3:0)', 18,
    [anyN('r-1', 'changing attitudes to marriage', 6, 1, 6, semis(h_m, 'changing attitudes to marriage')[:CAP],
          'One point, 6 marks — and note the ladder is 6:3:0, not 6:4:2:0, so there is no middle grade to fall back on. Either the point is developed or it halves. Divorce and separation breaking the traditional nuclear family, blended families, cohabiting couples, children born outside marriage, same-sex marriage.'),
     anyN('r-2', 'parenting roles', 6, 1, 6, semis(h_p, 'parenting roles')[:CAP],
          'One point, 6 marks, 6:3:0. The longest list: women as breadwinners, men at home, more democratic decisions, an egalitarian split of childcare and housework, and the role conflict and overload that follow.'),
     anyN('r-3', 'increased participation of women in the workforce', 6, 1, 6,
          semis(h_w, 'increased participation of women in the workforce')[:CAP],
          'One point, 6 marks, 6:3:0. More disposable income, but also role overload, more childcare needed, smaller families, and older children taking on extra responsibility.')],
    'Fixed: the scheme requires one point under each named heading, so all three must be attempted. The 6:3:0 grading is unusually harsh — a half-developed point loses three marks, not two.',
    stem='‘Contemporary society is experiencing rapid social change.’ (Social Change Research Group, wit.ie)',
    tariff_kind='fixed'))

ch = block(E3c, '3 points @ 4 marks (graded 4:2:0) limits number of hours')
cards.append(C(
    PFX+'q3cii', Y, LV, 'home-economics-2-2', 'protection-of-young-persons-employment-act-1996',
    '2023 HL Section C E3 Q3(c)(ii)',
    'Describe how the Protection of Young Persons (Employment), Act 1996 offers protection to young people in work.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Protections offered by the Protection of Young Persons (Employment) Act 1996', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three points at 4 marks, graded 4:2:0. This question is almost entirely numbers, and the numbers are the marks: no full-time employment under 16, no work during term under 14, 8 hours a week at 15, 40 hours at 16 and 17, a 30-minute break every 4 hours, two rest days a week, and no work before 6 a.m. or after 10 p.m. Quote them.')],
    'One flat list, taken in order to the cap.',
    stem='‘Contemporary society is experiencing rapid social change.’ (Social Change Research Group, wit.ie)'))

# ------------------------------------------------------- Question 4 (Core)
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) ‘The meat sector', 'and 4.(b)')
ch = block(Q4a, '3 points @ 4 marks (graded 4:2:0) Department of Agriculture', '(ii) Meat is a versatile food')
cards.append(C(
    PFX+'q4ai', Y, LV, 'home-economics-0-11', 'measures-ensuring-meat-safety',
    '2023 HL Section C Q4(a)(i) - Core',
    'Discuss the measures that have been implemented in the Irish food industry to ensure meat is safe for consumption.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Measures ensuring meat is safe for consumption', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three measures at 4 marks, graded 4:2:0. Traceability is the thread running through the whole list — recorded antibiotic use, controlled feed, routine disease testing, livestock identification, and the Bord Bia scheme keeping veterinary records. Name the body or the scheme and say what it actually enforces.')],
    'One flat list, taken in order to the cap.',
    stem='‘The meat sector in Ireland is one of the most important industries in the national economy.’ (www.ibec.ie)'))

METHODS = ['Boiling conduction', 'Poaching conduction', 'Steaming meat is cooked', 'Stewing conduction',
           'Braising meat seared', 'Pressure cooking high temperatures', 'Roasting conduction',
           'Grilling/Barbecuing radiant heat', 'Frying conduction']
NAMES = ['Boiling', 'Poaching', 'Steaming', 'Stewing', 'Braising', 'Pressure cooking', 'Roasting',
         'Grilling/Barbecuing', 'Frying']
mb = heads(block(Q4a, 'Boiling conduction', '(iii) Identify a type of material'), METHODS)
for i, (anchor, name) in enumerate(zip(METHODS, NAMES)):
    o_pr = semis(block(mb[i], anchor, 'affects'), name)
    o_af = semis(block(mb[i], 'affects'), 'affects')
    cards.append(C(
        PFX+'q4aii-'+name.lower().replace('/', '-').replace(' ', '-'), Y, LV,
        'home-economics-0-3', f'evaluating-{name.lower().replace("/","-").replace(" ","-")}-meat',
        f'2023 HL Section C Q4(a)(ii) - Core - {name}',
        'Meat is a versatile food and can be cooked in a variety of ways. Evaluate one method of cooking meat. Refer to: name of cooking method; underlying principle; how the cooking method chosen affects the meat.',
        'Name 1 point @ 3 marks (graded 3:0); principle 3 points @ 3 marks; effects 4 points @ 3 marks (graded 3:2:0)', 24,
        [anyN('r-1', 'Name of cooking method', 3, 1, 3, NAMES[:CAP],
              f'Name one, 3 marks, graded 3:0 — all-or-nothing. This card follows {name.lower()}; the scheme prints a parallel account for each of the nine methods it accepts, marked identically.'),
         anyN('r-2', f'Underlying principle of {name.lower()}', 9, 3, 3, o_pr[:CAP],
              'Three points at 3 marks, graded 3:2:0. The principle is the physics plus the numbers: which forms of heat transfer are at work, and the temperature it happens at. The scheme prices the method of heat transfer and the temperature as separate points, so quote the figure.'),
         anyN('r-3', f'How {name.lower()} affects the meat', 12, 4, 3, o_af[:CAP],
              'Four points at 3 marks, graded 3:2:0 — half the whole question. Effects fall into colour, texture and tenderness, flavour, and nutrient loss. Taking one from each of those four areas gives four points that cannot be read as the same effect twice, and the B-group vitamin behaviour is a marking point in nearly every method.')],
        f'One of nine parallel accounts the scheme prints under Q4(a)(ii). A candidate evaluates a single method, so each is its own card with its own questionRef rather than pooling nine sets of marking points into one menu. At 24 marks this is the largest single part in Section C.',
        stem='‘The meat sector in Ireland is one of the most important industries in the national economy.’ (www.ibec.ie)',
        tariff_kind='fixed'))

# The scheme opens each material with the forms it comes in, then a dash, then
# the first suitability point. Strip the whole run-in, or it rides along as part
# of that first option.
MATS = [('glass', 'Glass', 'Glass bottles, jars', 'etc. 100% recyclable',
         'Glass bottles, jars'),
        ('metal', 'Metal', 'Metal aluminium, tinfoil', 'etc. recyclable',
         'Metal aluminium, tinfoil cartons, stainless steel –'),
        ('paper', 'Paper', 'Paper waxed cartons', 'etc. recyclable',
         'Paper waxed cartons, greaseproof paper, cardboard –'),
        ('plastic', 'Plastic', 'Plastic cartons, containers', 'etc. recyclable',
         'Plastic cartons, containers, bags, vacuum packed -')]
matb = heads(block(Q4a, 'Glass bottles, jars'), [a for _, _, a, _, _ in MATS])
for i, (slug, name, anchor, envmark, supfx) in enumerate(MATS):
    o_su = semis(block(matb[i], anchor, envmark), supfx)
    o_ev = semis(block(matb[i], envmark), '')
    cards.append(C(
        PFX+'q4aiii-'+slug, Y, LV, 'home-economics-0-11', f'packaging-material-{slug}',
        f'2023 HL Section C Q4(a)(iii) - Core - {name}',
        'Identify a type of material suitable for packaging perishable foods. Assess the suitability for purpose and environmental impact of the material identified.',
        'Name @ 4 marks (graded 4:2:0); 2 points @ 5 marks (graded 5:3:0)', 14,
        [anyN('r-1', 'Materials suitable for packaging perishable foods', 4, 1, 4,
              ['Glass', 'Metal', 'Paper', 'Plastic'],
              f'Name one, 4 marks, graded 4:2:0. This card follows {name.lower()}; the scheme prints a parallel account for each of the four materials. Naming the material and its form (jars, tinfoil, waxed cartons, vacuum packs) earns the full 4.'),
         anyN('r-2', 'Suitability for purpose', 5, 1, 5, o_su[:CAP],
              'One point, 5 marks, graded 5:3:0 — no 4, so a bare property drops to 3. Suitability means what the packaging does for the food: keeps contamination out, survives heat processing, keeps moisture in.'),
         anyN('r-3', 'Environmental impact', 5, 1, 5, o_ev[:CAP],
              'One point, 5 marks, graded 5:3:0. The scheme expects both sides. Recyclability, lower emissions and conserved raw materials sit on one side; whether the material is biodegradable is the sharpest divider — only paper is, and glass, metal and plastic are not.')],
        'One of four parallel accounts the scheme prints under Q4(a)(iii). The question asks for one identified material, so each is its own card with its own questionRef. The scheme requires one point on suitability and one on environmental impact, which is why those are separate rows.',
        stem='‘The meat sector in Ireland is one of the most important industries in the national economy.’ (www.ibec.ie)',
        tariff_kind='fixed'))

Q4b = block(Q4, 'and 4.(b) Everyday living includes', 'or 4.(c)')
FACT = ['family stage mortgage', 'family circumstances special needs', 'gender more women',
        'social class some from poorer', 'culture some cultures focus']
ch = block(Q4b, 'family stage mortgage', '(ii) Describe how the state assists')
cards.append(C(
    PFX+'q4bi', Y, LV, 'home-economics-1-1', 'socio-economic-factors-and-household-expenditure',
    '2023 HL Section C Q4(b)(i) - Core',
    'Evaluate the socio-economic factors that impact household expenditure.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Socio-economic factors impacting household expenditure', 15, 3, 5,
          [bundle(h, ' '.join(a.split()[:2]), 4) for h, a in zip(heads(ch, FACT), FACT)][:CAP],
          'Three factors at 5 marks, graded 5:3:0 — no 4, so a factor named without its effect on spending drops to 3. The scheme prints five factors; take three different ones rather than three angles on income. Social class and culture have the most developed accounts.')],
    'One option per named factor, each carrying that factor\'s own account, because the scheme groups its marking points under five headings and prices three points.',
    stem='Everyday living includes many transactions that require consumer spending.'))

ch = block(Q4b, '3 points @ 5 marks (graded 5:3:0) social welfare payments')
cards.append(C(
    PFX+'q4bii', Y, LV, 'home-economics-1-1', 'state-support-for-the-economic-function',
    '2023 HL Section C Q4(b)(ii) - Core',
    'Describe how the state assists the family in carrying out its economic function in society.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'How the state assists the family\'s economic function', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0 — the shortest list in Q4, so all seven options are worth knowing. Naming the payment is 3; saying which cost it covers and for whom takes it to 5.')],
    'One flat list, taken in order to the cap.',
    stem='Everyday living includes many transactions that require consumer spending.'))

Q4c = block(Q4, 'or 4.(c) ‘Irish people are cooking more')
ch = block(Q4c, '3 points @ 5 marks (graded 5:3:0) food cooks quickly', '(ii) Describe the working principle')
cards.append(C(
    PFX+'q4ci', Y, LV, 'home-economics-1-3', 'microwave-oven-contribution-to-home-management',
    '2023 HL Section C Q4(c)(i) - Core',
    'Evaluate the contribution of the microwave oven to the management of the home.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Contribution of the microwave oven to home management', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0. Management is the key word — these are savings of time, energy, skill and washing-up, so tie each point to the resource it saves the household.')],
    'One flat list, taken in order to the cap.',
    stem='‘Irish people are cooking more at home, and how we shop for food, cook and eat has changed significantly.’ (The Irish Times)'))

ch = block(Q4c, '5 points @ 3marks (graded 3:2:0) transformer')
cards.append(C(
    PFX+'q4cii', Y, LV, 'home-economics-1-3', 'microwave-oven-working-principle',
    '2023 HL Section C Q4(c)(ii) - Core',
    'Describe the working principle of the microwave oven.',
    '5 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'Working principle of the microwave oven', 15, 5, 3,
          semis(ch, '5 points @ 3marks (graded 3:2:0)')[:CAP],
          'Five points at 3 marks, graded 3:2:0. The scheme lists the chain in order and following it gives five points without effort: the transformer raises the voltage, the magnetron turns electricity into electromagnetic waves, the wave-guide directs them into the cabinet, they penetrate 2–4 cm and vibrate the food molecules, and the friction produces heat that conducts to the centre. Standing time is a marking point because the molecules keep vibrating after the timer stops.')],
    'One flat list, taken in order to the cap.',
    stem='‘Irish people are cooking more at home, and how we shop for food, cook and eat has changed significantly.’ (The Irish Times)'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2023hl_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
