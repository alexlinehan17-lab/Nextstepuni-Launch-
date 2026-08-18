"""2025 Ordinary Level, Section C — electives 1/2/3 and Question 4 (Core)."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2025, 'ordinary')
SEC = tidy(T[19449:36732])
Y, LV, PFX = 2025, 'ordinary', 'he-2025-ol-sc-'
CAP = 14
cards, held = [], []

def C(*a, **k):
    k.setdefault('section', 'C')
    return card(*a, **k)

def bundle(h, prefix, n=None):
    seg = semis(h, prefix)
    return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 –', 'Elective 2 –')
E1a = block(E1, '1.(a) The diagram below', 'and 1.(b)')

# 1(a)(i) — methods of insulating a home, 20 marks
METH = ['attic: blanket insulation:', 'loose fill:', 'foam insulation:', 'blown fibre insulation:',
        'walls: cavity walls:', 'internal solid walls:', 'external walls:',
        'windows: double or triple glaze:', 'curtains:', 'floors:', 'external:',
        'hot water cylinder/pipes:']
ch = block(E1a, 'attic: blanket insulation:', '(ii) Discuss three advantages')
cards.append(C(
    PFX + 'q1ai', Y, LV, 'home-economics-3-6', 'methods-of-insulating-a-home',
    '2025 OL Section C E1 Q1(a)(i)',
    'Describe four methods of insulating a home.',
    '4 methods @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Methods of insulating a home', 20, 4, 5,
          [bundle(h, '', 2) for h in heads(ch, METH)][:CAP],
          'Four methods at 5 marks, graded 5:3:0 — there is no 4, so a method named without saying how it is fitted drops straight to 3. Describe, so each answer needs the material and where it goes. The scheme groups by location, so taking one from the attic, walls, windows and floors gives four that cannot be read as the same method twice.')],
    'One option per named method: the scheme prints twelve methods grouped by location, each with its own material and fitting detail, and prices four. Each option is that method\'s own opening detail, kept contiguous.'))

# 1(a)(ii) — advantages of a well-insulated home, 15 marks
ch = block(E1a, '3 advantages @ 5 marks (graded 5:3:0)', '(iii) Suggest three different')
cards.append(C(
    PFX + 'q1aii', Y, LV, 'home-economics-3-6', 'advantages-of-a-well-insulated-home',
    '2025 OL Section C E1 Q1(a)(ii)',
    'Discuss three advantages of a well-insulated home.',
    '3 advantages @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Advantages of a well-insulated home', 15, 3, 5,
          semis(ch, '3 advantages @ 5 marks (graded 5:3:0)')[:CAP],
          'Three advantages at 5 marks, graded 5:3:0. Discuss, so each needs a consequence: lower bills because less heat escapes, fewer emissions because less fuel is burned. The BER rating point is the one most students miss and it is worth the same 5.')],
    'One flat list, taken in order to the cap.'))

# 1(a)(iii) — sustainable practices that save energy, 15 marks
ch = block(E1a, '3 practices @ 5 marks (graded 5:3:0)')
cards.append(C(
    PFX + 'q1aiii', Y, LV, 'home-economics-3-6', 'sustainable-practices-saving-energy',
    '2025 OL Section C E1 Q1(a)(iii)',
    'Suggest three different sustainable practices that save energy in the home.',
    '3 practices @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Sustainable practices that save energy in the home', 15, 3, 5,
          semis(ch, '3 practices @ 5 marks (graded 5:3:0)')[:CAP],
          'Three practices at 5 marks, graded 5:3:0. The question says different, so three ways of using less electricity will read as one practice — spread across heating, appliances and lighting. Each needs a sentence on how it saves the energy.')],
    'One flat list, taken in order to the cap.'))

# 1(b)(i) — electricity delivered into the home, 15 marks
E1b = block(E1, 'and 1.(b) ‘Electricity', 'or 1.(c)')
ch = block(E1b, '3 points @ 5 marks (graded 5:3:0)', '(ii) Explain each of the following')
cards.append(C(
    PFX + 'q1bi', Y, LV, 'home-economics-3-5', 'electricity-delivery-into-the-home',
    '2025 OL Section C E1 Q1(b)(i)',
    'Describe how electricity is delivered into the home.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'How electricity is delivered into the home', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0. The scheme lists the route in order — generation, transformer, mains service cable, meter cabinet, fuse board, circuit breakers, circuits, sockets — so describing the journey in sequence gives three points without having to think of them separately.')],
    'One flat list, taken in order to the cap.'))

# 1(b)(ii) — electrical terms, 15 marks
ch = block(E1b, 'Miniature circuit breaker: safety feature')
h_mcb, h_v, h_kwh = heads(ch, ['Miniature circuit breaker:', 'Voltage:', 'Kilowatt per hour (kWh):'])
cards.append(C(
    PFX + 'q1bii', Y, LV, 'home-economics-3-5', 'electrical-terms-mcb-voltage-kwh',
    '2025 OL Section C E1 Q1(b)(ii)',
    'Explain each of the following electrical terms: miniature circuit breakers; voltage; kilowatt per hour (kWh).',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'miniature circuit breakers', 5, 1, 5, semis(h_mcb, 'Miniature circuit breaker:')[:CAP],
          'One point, 5 marks, graded 5:3:0. Saying it is a safety device is 3; 5 needs what it actually does — trips to break the circuit on a fault or overload, and can be reset once the fault is fixed. The scheme accepts a labelled diagram here.'),
     anyN('r-2', 'voltage', 5, 1, 5, semis(h_v, 'Voltage:')[:CAP],
          'One point, 5 marks, graded 5:3:0. The Irish mains figure — 230 volts — is a marking point in its own right, so quote it.'),
     anyN('r-3', 'kilowatt per hour (kWh)', 5, 1, 5, semis(h_kwh, 'Kilowatt per hour (kWh):')[:CAP],
          'One point, 5 marks, graded 5:3:0. Two facts carry it: a kilowatt is 1000 watts, and a kWh is the electricity an appliance uses in one hour of operation. This is the unit the bill is charged in.')],
    'Fixed: three terms, priced identically at 5 marks each. All three are short definitions, so this is the cheapest 15 marks in the elective.',
    tariff_kind='fixed'))

# 1(c)(i) — interior design planning, 15 marks
E1c = block(E1, 'or 1.(c) Interior designers')
ch = block(E1c, 'Family size and stage:', '(ii) Explain the term')
h_fam, h_cost, h_com = heads(ch, ['Family size and stage:', 'Cost:', 'Comfort:'])
cards.append(C(
    PFX + 'q1ci', Y, LV, 'home-economics-3-4', 'interior-design-planning-factors',
    '2025 OL Section C E1 Q1(c)(i)',
    'Discuss the importance of each of the following when planning the interior design of a home: family size and stage; cost; comfort.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'family size and stage', 5, 1, 5, semis(h_fam, 'Family size and stage:')[:CAP],
          'One point, 5 marks, graded 5:3:0. Tie the choice to the stage of the family — non-slip flooring and stain-resistant surfaces because there are young children, flexible design because the family will change.'),
     anyN('r-2', 'cost', 5, 1, 5, semis(h_cost, 'Cost:')[:CAP],
          'One point, 5 marks, graded 5:3:0. The scheme makes the point that a limited budget does not mean poor design, and it separates initial cost from maintenance cost — either distinction earns the full 5.'),
     anyN('r-3', 'comfort', 5, 1, 5, semis(h_com, 'Comfort:')[:CAP],
          'One point, 5 marks, graded 5:3:0. The longest list of the three, so this is the safest to answer: space, function of the room, ease of movement, heating and ventilation all count.')],
    'Fixed: three headings named in the question, priced identically. Skipping one costs a straight 5 marks.',
    tariff_kind='fixed'))

# 1(c)(ii) — texture, 15 marks
ch = block(E1c, '1 point on texture @ 5 marks (graded 5:3:0)')
o_tex = semis(block(ch, '1 point on texture', '2 examples @ 5 marks'),
              '1 point on texture @ 5 marks (graded 5:3:0)')
ex = block(ch, '2 examples @ 5 marks')
h_sm, h_ro = heads(ex, ['smooth textures:', 'rough textures:'])
cards.append(C(
    PFX + 'q1cii', Y, LV, 'home-economics-3-4', 'texture-in-interior-design',
    '2025 OL Section C E1 Q1(c)(ii)',
    'Explain the term ‘texture’, and give two examples of how texture may be used to enhance the interior design of a room.',
    'Texture 1 point @ 5 marks; 2 examples @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'The term ‘texture’', 5, 1, 5, o_tex[:CAP],
          'One point, 5 marks, graded 5:3:0. Texture is the visual and tactile quality of a surface — say both, and that it adds depth, and the 5 is safe.'),
     anyN('r-2', 'Examples of texture used to enhance interior design', 10, 2, 5,
          (semis(h_sm, 'smooth textures:') + semis(h_ro, 'rough textures:'))[:CAP],
          'Two examples at 5 marks, graded 5:3:0 — ten of the fifteen marks. The scheme splits its list into smooth and rough textures, so one from each reads as two genuinely different examples. Name the surface and say what it does to the room.')],
    'Fixed: the explanation is priced at 5 and the two examples at 10. The examples row pools the scheme\'s smooth and rough lists, which is how the two examples are meant to contrast.',
    tariff_kind='fixed'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 –', 'Elective 3 –')
E2a = block(E2, '2.(a) Special events', 'and 2.(b)')
ch = block(E2a, 'Comfort: flowing fabric', '(ii) Suggest one accessory')
h_c, h_f, h_a = heads(ch, ['Comfort: flowing fabric', 'Function: slim leg', 'Aesthetic appeal: elongated'])
held.append(dict(C(
    PFX + 'q2ai', Y, LV, 'home-economics-3-8', 'suitability-of-outfits-for-an-occasion',
    '2025 OL Section C E2 Q2(a)(i)',
    'Comment on the suitability of the outfits shown above for a winter wedding. Refer to: comfort; function; aesthetic appeal.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'comfort', 6, 2, 3, semis(h_c, 'Comfort:')[:CAP], 'Two points at 3 marks, graded 3:2:0.'),
     anyN('r-2', 'function', 6, 2, 3, semis(h_f, 'Function:')[:CAP], 'Two points at 3 marks, graded 3:2:0.'),
     anyN('r-3', 'aesthetic appeal', 6, 2, 3, semis(h_a, 'Aesthetic appeal:')[:CAP], 'Two points at 3 marks, graded 3:2:0.')],
    'Fixed: three headings named in the question, priced equally.',
    stem='Special events require special occasion clothing.', tariff_kind='fixed'),
    heldReason='Marks an image of outfits printed on the paper. Every option in the scheme describes that image ("flowing fabric is comfortable to wear", "short length in the jacket gives height"), so the card is unanswerable without the figure and the markdown extraction does not carry it.'))
held.append(dict(C(
    PFX + 'q2aii', Y, LV, 'home-economics-3-8', 'accessorising-an-outfit',
    '2025 OL Section C E2 Q2(a)(ii)',
    'Suggest one accessory you could add to enhance any one of the above outfits. Give one reason for your choice.',
    '1 accessory @ 3 marks (graded 3:0); 1 reason @ 4 marks (graded 4:2:0)', 7,
    [anyN('r-1', 'Accessories', 3, 1, 3,
          semis(block(E2a, '1 accessory @ 3 marks (graded 3:0), 1 reason @ 4 marks (graded 4:2:0)'),
                '1 accessory @ 3 marks (graded 3:0), 1 reason @ 4 marks (graded 4:2:0)')[:CAP],
          'Name one accessory, 3 marks, graded 3:0 — all-or-nothing.'),
     anyN('r-2', 'Reason for the choice', 4, 1, 4, [], 'One reason, 4 marks, graded 4:2:0.')],
    'Fixed: the accessory is priced at 3 and the reason at 4.',
    stem='Special events require special occasion clothing.', tariff_kind='fixed'),
    heldReason='The reason must be given for one of the outfits printed on the paper, and the scheme prints no marking points at all for it — only the accessory list. Four of the seven marks have nothing behind them, and the figure is missing as well.'))

# 2(b)(i) — why fabric finishes are used, 6 marks
E2b = block(E2, 'and 2.(b) A variety of fabric finishes', 'or 2.(c)')
ch = block(E2b, '2 reasons @ 3 marks (graded 3:2:0)', '(ii) Name and describe')
cards.append(C(
    PFX + 'q2bi', Y, LV, 'home-economics-3-7', 'why-fabric-finishes-are-used',
    '2025 OL Section C E2 Q2(b)(i)',
    'Explain why fabric finishes are used on fabric.',
    '2 reasons @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Why fabric finishes are used on fabric', 6, 2, 3,
          semis(ch, '2 reasons @ 3 marks (graded 3:2:0)')[:CAP],
          'Only two reasons at 3 marks — a six-mark part, so keep it short. Each reason is a problem the finish removes: creasing, shrinking, staining, catching fire.')],
    'One flat list, taken in order to the cap.',
    stem='A variety of fabric finishes can be applied to textiles.'))

# 2(b)(ii) — name, describe and exemplify a fabric finish, 9 marks
FIN = ['waterproofing:', 'anti-static:', 'stain resistant:', 'crease resistant:',
       'mercerising:', 'flame retardant:']
fb = heads(block(E2b, 'waterproofing: makes fabric'), FIN)
names = [f[:-1] for f in FIN]
descs = [semis(h, f)[0] for h, f in zip(fb, FIN)]
exs = [semis(h, f)[1] for h, f in zip(fb, FIN)]
cards.append(C(
    PFX + 'q2bii', Y, LV, 'home-economics-3-7', 'fabric-finishes-named-described-and-used',
    '2025 OL Section C E2 Q2(b)(ii)',
    'Name and describe one fabric finish. Give one example of its use in textiles.',
    'Name 3 marks; description 1 point 3 marks; example 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Fabric finishes', 3, 1, 3, names[:CAP],
          'Name one finish, 3 marks, graded 3:2:0. All six in the scheme are equally creditable — pick the one whose effect and use you can state, because the other 6 marks follow from it.'),
     anyN('r-2', 'What the finish does', 3, 1, 3, descs[:CAP],
          'One description, 3 marks, graded 3:2:0, matching the finish you named. Each of the scheme\'s descriptions is a single clause about what the fabric can now do — that is the whole answer, not a paragraph.'),
     anyN('r-3', 'Example of its use in textiles', 3, 1, 3, exs[:CAP],
          'One example, 3 marks, graded 3:2:0. It must be a garment or household item, not a fabric: the scheme pairs waterproofing with a rain coat, flame retardant with children\'s night wear, mercerising with bed sheets.')],
    'Fixed, three equal rows. The scheme prints six finishes each as name, effect and example, so the rows are the three columns of that list and the option a student picks in one row fixes their answer in the other two.',
    stem='A variety of fabric finishes can be applied to textiles.', tariff_kind='fixed'))

# 2(c)(i) — selecting a commercial sewing pattern, 9 marks
E2c = block(E2, 'or 2.(c) Sewing has become')
ch = block(E2c, '3 factors @ 3 marks (graded 3:2:0)', '(ii) State the importance')
cards.append(C(
    PFX + 'q2ci', Y, LV, 'home-economics-3-8', 'selecting-a-commercial-sewing-pattern',
    '2025 OL Section C E2 Q2(c)(i)',
    'Outline three factors to consider when selecting a commercial sewing pattern.',
    '3 factors @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Factors to consider when selecting a commercial sewing pattern', 9, 3, 3,
          semis(ch, '3 factors @ 3 marks (graded 3:2:0)')[:CAP],
          'Three factors at 3 marks, graded 3:2:0. The two measurement rules are the specific marks here and the scheme keeps them separate: hip measurement sizes skirts and trousers, chest measurement sizes dresses, shirts, coats and jackets.')],
    'One flat list, taken in order to the cap.',
    stem='Sewing has become popular and trendy.'))

# 2(c)(ii) — pressing during construction, 6 marks
ch = block(E2c, '2 points @ 3 marks (graded 3:2:0) improves the overall appearance')
cards.append(C(
    PFX + 'q2cii', Y, LV, 'home-economics-3-8', 'importance-of-pressing-a-garment',
    '2025 OL Section C E2 Q2(c)(ii)',
    'State the importance of pressing a garment during construction.',
    '2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Importance of pressing a garment during construction', 6, 2, 3,
          semis(ch, '2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Two points at 3 marks — the question says state, so a phrase each is enough. Pressing during construction is about the seams and darts, not about the finished look, and the scheme credits both.')],
    'One flat list, taken in order to the cap.',
    stem='Sewing has become popular and trendy.'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 –', 'Question 4 – Core')
E3a = block(E3, '3.(a) Child-centred education', 'and 3.(b)')

# 3(a)(i) — primary school education, 20 marks
ch = block(E3a, 'Age range of primary school children:', '(ii) Name and give details')
h_age, h_ch, h_cur = heads(ch, ['Age range of primary school children:',
                                'Choice / types of primary schools:', 'Curriculum offered:'])
o_age, o_ch, o_cur = (semis(h_age, 'Age range of primary school children:'),
                      semis(h_ch, 'Choice / types of primary schools:'),
                      semis(h_cur, 'Curriculum offered:'))
cards.append(C(
    PFX + 'q3ai', Y, LV, 'home-economics-3-10', 'primary-school-education-in-ireland',
    '2025 OL Section C E3 Q3(a)(i)',
    'Describe primary school education in Ireland. Refer to: age range of primary school children; choices / types of primary schools; curriculum offered.',
    '1 point @ 5 marks (graded 5:3:0) x 3, + 1 other point @ 5 marks', 20,
    [anyN('r-1', 'age range of primary school children', 5, 1, 5, o_age[:CAP],
          'One point, 5 marks, graded 5:3:0. This heading is pure fact and the numbers are the marks: enrolment from age 4, compulsory by 6, an eight-year cycle, finishing at 12.'),
     anyN('r-2', 'choices / types of primary schools', 5, 1, 5, o_ch[:CAP],
          'One point, 5 marks, graded 5:3:0. The scheme accepts thirteen school types, so this is the safest of the three headings — name types and say what distinguishes them.'),
     anyN('r-3', 'curriculum offered', 5, 1, 5, o_cur[:CAP],
          'One point, 5 marks, graded 5:3:0. Say what the curriculum is for, not what subjects exist: building self-esteem, literacy and numeracy, a broad learning experience.'),
     anyN('r-4', 'One further point, from any of the three headings', 5, 1, 5,
          (o_age + o_ch + o_cur)[:CAP],
          'The fourth point floats: the scheme reads three headings "+ 1 other point @ 5 marks", so add one more from whichever heading you know best.')],
    'Fixed: one point pinned to each of the three named headings and a fourth floating. Missing a heading costs 5 and cannot be made up by writing more on another.',
    stem='Child-centred education is a modern approach to curriculum.', tariff_kind='fixed'))

# 3(a)(ii) — the naming strand only; the two detail points have no scheme list
ch = block(E3a, 'Name: 5 marks (graded 5:3:0), 2 details @ 5 marks (graded 5:3:0)',
           '(iii) Discuss how education contributes')
o_init = semis(ch, 'Name: 5 marks (graded 5:3:0), 2 details @ 5 marks (graded 5:3:0)')
cards.append(C(
    PFX + 'q3aii-name', Y, LV, 'home-economics-3-10', 'education-initiatives-supporting-attendance',
    '2025 OL Section C E3 Q3(a)(ii) - naming the initiative',
    'Name one education initiative that helps to support school attendance.',
    'Name 1 @ 5 marks (graded 5:3:0)', 5,
    [anyN('r-1', 'Education initiatives that support school attendance', 5, 1, 5, o_init[:CAP],
          'Name one, 5 marks, graded 5:3:0. The scheme accepts a long list, and the ones tied directly to attendance rather than to attainment — the School Meals Scheme, School Transport, Home School Community Liaison, DEIS — are the easiest to then give details for.')],
    'The naming strand of Q3(a)(ii) only, worth 5 of the part\'s 15 marks. The two detail points at 5 marks each are held: the scheme prints the initiative list and no marking points at all for the details.',
    stem='Child-centred education is a modern approach to curriculum.'))
held.append(dict(C(
    PFX + 'q3aii-details', Y, LV, 'home-economics-3-10', 'education-initiative-details',
    '2025 OL Section C E3 Q3(a)(ii) - details of the initiative',
    'Give details of one education initiative that helps to support school attendance.',
    '2 details @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Details of the named initiative', 10, 2, 5, [], 'Two details at 5 marks.')],
    'The details strand of Q3(a)(ii).',
    stem='Child-centred education is a modern approach to curriculum.'),
    heldReason='The scheme prints the list of initiative names and then no marking points whatsoever for the two detail points, which carry 10 of the part\'s 15 marks. The naming strand ships as he-2025-ol-sc-q3aii-name.'))

# 3(a)(iii) — education and social/physical development, 15 marks
ch = block(E3a, '1 reference to social, 1 reference to physical, + 1 other point')
h_soc, h_phy = heads(ch, ['social: reinforces', 'physical: activities'])
o_soc, o_phy = semis(h_soc, 'social:'), semis(h_phy, 'physical:')
cards.append(C(
    PFX + 'q3aiii', Y, LV, 'home-economics-3-10', 'education-and-child-development',
    '2025 OL Section C E3 Q3(a)(iii)',
    'Discuss how education contributes to the social and physical development of children.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'social development', 5, 1, 5, o_soc[:CAP],
          'One point, 5 marks, graded 5:3:0. Social means learning to be with others — sharing, teamwork, friendships, respect for rules. The scheme also credits the primary/secondary and formal/informal socialisation terms, which are worth knowing by name.'),
     anyN('r-2', 'physical development', 5, 1, 5, o_phy[:CAP],
          'One point, 5 marks, graded 5:3:0. The shorter of the two lists and the one students forget: hand-eye co-ordination, dexterity, speed, and extra-curricular activities.'),
     anyN('r-3', 'One further point, from either heading', 5, 1, 5, (o_soc + o_phy)[:CAP],
          'The scheme reads "1 reference to social, 1 reference to physical, + 1 other point", so the third comes from whichever list you can develop further.')],
    'Fixed: one point pinned to each named area and one floating. Writing only about the social side caps you at 10 of 15.',
    stem='Child-centred education is a modern approach to curriculum.', tariff_kind='fixed'))

# 3(b)(i) — choosing a childcare option, 15 marks
E3b = block(E3, 'and 3.(b) There are many childcare options', 'or 3.(c)')
ch = block(E3b, '3 points @ 5 marks (graded 5:3:0)', '(ii) Name and give details')
cards.append(C(
    PFX + 'q3bi', Y, LV, 'home-economics-3-11', 'choosing-a-childcare-option',
    '2025 OL Section C E3 Q3(b)(i)',
    'Discuss three factors parents should consider when choosing a childcare option.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors to consider when choosing a childcare option', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0 — no 4, so a factor named without a reason drops to 3. Say why each factor matters to the parent or the child, not just that it should be considered.')],
    'One flat list, taken in order to the cap.',
    stem='There are many childcare options available in Ireland to suit different family needs.'))

# 3(b)(ii) — the naming strand only
ch = block(E3b, 'Name: 1 @ 5 marks (graded 5:3:0), 2 details @ 5 marks (graded 5:3:0)')
o_sup = semis(ch, 'Name: 1 @ 5 marks (graded 5:3:0), 2 details @ 5 marks (graded 5:3:0)')
cards.append(C(
    PFX + 'q3bii-name', Y, LV, 'home-economics-3-11', 'state-supports-for-families-with-children',
    '2025 OL Section C E3 Q3(b)(ii) - naming the support',
    'Name one government / state support provided to families with children.',
    'Name 1 @ 5 marks (graded 5:3:0)', 5,
    [anyN('r-1', 'Government / state supports for families with children', 5, 1, 5, o_sup[:CAP],
          'Name one, 5 marks, graded 5:3:0. Child Benefit, the Working Family Payment and the ECCE scheme are the three most detail-rich, so they are the best to name when the rest of the part asks what the support actually provides.')],
    'The naming strand of Q3(b)(ii) only, worth 5 of the part\'s 15 marks. The two detail points at 5 marks each are held: the scheme lists the supports and prints no marking points for their details.',
    stem='There are many childcare options available in Ireland to suit different family needs.'))
held.append(dict(C(
    PFX + 'q3bii-details', Y, LV, 'home-economics-3-11', 'state-support-details',
    '2025 OL Section C E3 Q3(b)(ii) - details of the support',
    'Give details of one government / state support provided to families with children.',
    '2 details @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Details of the named support', 10, 2, 5, [], 'Two details at 5 marks.')],
    'The details strand of Q3(b)(ii).',
    stem='There are many childcare options available in Ireland to suit different family needs.'),
    heldReason='The scheme lists the supports by name and prints no marking points for the two detail points, which carry 10 of the part\'s 15 marks. The naming strand ships as he-2025-ol-sc-q3bii-name.'))

# 3(c)(i) — reasons at risk of poverty, 15 marks
E3c = block(E3, 'or 3.(c) 10.6% of people')
ch = block(E3c, '3 reasons @ 5 marks (graded 5:3:0)', '(ii) Describe the effects')
cards.append(C(
    PFX + 'q3ci', Y, LV, 'home-economics-3-9', 'reasons-for-risk-of-poverty',
    '2025 OL Section C E3 Q3(c)(i)',
    'Discuss three reasons why people might be at risk of poverty.',
    '3 reasons @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Reasons why people might be at risk of poverty', 15, 3, 5,
          semis(ch, '3 reasons @ 5 marks (graded 5:3:0)')[:CAP],
          'Three reasons at 5 marks, graded 5:3:0. Housing cost and social housing shortage are two separate options, so both can be used. The cycle of poverty and the poverty trap are the two technical terms on the list and each is worth a full 5 if you explain it.')],
    'One flat list, taken in order to the cap.',
    stem='10.6% of people in Ireland were at risk of poverty in 2023. (www.cso.ie)'))

# 3(c)(ii) — effects of poverty on families, 15 marks
ch = block(E3c, '3 effects @ 5 marks (graded 5:3:0)')
cards.append(C(
    PFX + 'q3cii', Y, LV, 'home-economics-3-9', 'effects-of-poverty-on-families',
    '2025 OL Section C E3 Q3(c)(ii)',
    'Describe the effects of poverty on families with children.',
    '3 effects @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Effects of poverty on families with children', 15, 3, 5,
          semis(ch, '3 effects @ 5 marks (graded 5:3:0)')[:CAP],
          'Three effects at 5 marks, graded 5:3:0. The scheme runs from the material (poor housing, poor nutrition, going without basics) to the social and emotional (exclusion, low self-esteem, anxiety) — take one from each end and they cannot be read as the same effect twice.')],
    'One flat list, taken in order to the cap.',
    stem='10.6% of people in Ireland were at risk of poverty in 2023. (www.cso.ie)'))

# ------------------------------------------------------- Question 4 (Core)
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) ‘Yoghurt continues', 'and 4.(b)')

# 4(a)(i) — nutritive and dietetic value of yoghurt, 20 marks
ch = block(Q4a, 'Nutritive value HBV protein', '(ii) In relation to yoghurt')
h_nut, h_die = heads(ch, ['Nutritive value HBV protein', 'Dietetic value HBV protein'])
o_nut, o_die = semis(h_nut, 'Nutritive value'), semis(h_die, 'Dietetic value')
cards.append(C(
    PFX + 'q4ai', Y, LV, 'home-economics-0-9', 'nutritive-and-dietetic-value-of-yoghurt',
    '2025 OL Section C Q4(a)(i) - Core',
    'Give an account of the nutritive value and the dietetic value of yoghurt.',
    '4 points @ 5 marks (graded 5:4:3:2:0)', 20,
    [anyN('r-1', 'Nutritive value', 5, 1, 5, o_nut[:CAP],
          'One point, 5 marks, on a 5:4:3:2:0 ladder — the finest grading on the paper, so a partly-right answer still scores. Nutritive value means which nutrients are present and in what amount: HBV protein, calcium, lactose, 87% water. The two deficiencies, vitamin C and iron, are marking points too.'),
     anyN('r-2', 'Dietetic value', 5, 1, 5, o_die[:CAP],
          'One point, 5 marks, 5:4:3:2:0. Dietetic value is who the food suits and why — easy to digest, cheap, suits children, teenagers, pregnant women and older people. This is the half students merge into the first one and lose.'),
     anyN('r-3', 'Two further points, from either heading', 10, 2, 5, (o_nut + o_die)[:CAP],
          'The scheme reads "1 reference to nutritive value, 1 reference to dietetic value, + 2 other points", so half the marks float. Take both from whichever heading you know better.')],
    'Fixed: one point pinned to each named value and two floating. The distinction is the whole question — nutritive is what is in it, dietetic is who it suits.',
    stem='‘Yoghurt continues to be a favourite product today.’ (www.glanbianutritionals.com)',
    tariff_kind='fixed'))

# 4(a)(ii) — culinary uses, buying, storing, 18 marks
ch = block(Q4a, 'Culinary uses: on its own', '(iii) There is an increasing variety')
h_cu, h_bu, h_st = heads(ch, ['Culinary uses:', 'Guidelines for buying:', 'Guidelines for storing:'])
cards.append(C(
    PFX + 'q4aii', Y, LV, 'home-economics-0-9', 'yoghurt-uses-buying-and-storing',
    '2025 OL Section C Q4(a)(ii) - Core',
    'In relation to yoghurt describe each of the following: culinary uses; guidelines for buying; guidelines for storing.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'culinary uses', 6, 2, 3, semis(h_cu, 'Culinary uses:')[:CAP],
          'Two uses at 3 marks, graded 3:2:0. Name the dish or the course, not just "in cooking" — desserts, salads, garnishing, or as an alternative to cream.'),
     anyN('r-2', 'guidelines for buying', 6, 2, 3, semis(h_bu, 'Guidelines for buying:')[:CAP],
          'Two guidelines at 3 marks, graded 3:2:0. The dome-shaped lid is the specific one the scheme rewards — it means the yoghurt has fermented in the pot. Check the use-by date is the other reliable mark.'),
     anyN('r-3', 'guidelines for storing', 6, 2, 3, semis(h_st, 'Guidelines for storing:')[:CAP],
          'Two guidelines at 3 marks, graded 3:2:0. Refrigerate promptly, use in rotation, reseal with the original lid, use by the date. Short answers — do not over-write a 6-mark row.')],
    'Fixed: three headings named in the question, priced identically at 6 marks each.',
    stem='‘Yoghurt continues to be a favourite product today.’ (www.glanbianutritionals.com)',
    tariff_kind='fixed'))

# 4(a)(iii) — variety of yoghurt products, 12 marks
ch = block(Q4a, '3 reasons @ 4 marks (graded 4:2:0)')
cards.append(C(
    PFX + 'q4aiii', Y, LV, 'home-economics-0-11', 'reasons-for-variety-of-yoghurt-products',
    '2025 OL Section C Q4(a)(iii) - Core',
    'There is an increasing variety of yoghurt and yoghurt drinks available in Irish supermarkets. Give three reasons for this trend.',
    '3 reasons @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Reasons for the increasing variety of yoghurt products', 12, 3, 4,
          semis(ch, '3 reasons @ 4 marks (graded 4:2:0)')[:CAP],
          'Three reasons at 4 marks, graded 4:2:0 — naming a product type is 2, saying which consumer it is aimed at takes it to 4. The scheme is really listing market segments: lactose free, sugar free, probiotic, added protein, soya.')],
    'One flat list, taken in order to the cap.',
    stem='‘Yoghurt continues to be a favourite product today.’ (www.glanbianutritionals.com)'))

# 4(b)(i) — importance of regular saving, 15 marks
Q4b = block(Q4, 'and 4.(b) ‘Saving money', 'or 4.(c)')
ch = block(Q4b, '3 reasons @ 5 marks (graded 5:3:0)', '(ii) Name and give details')
cards.append(C(
    PFX + 'q4bi', Y, LV, 'home-economics-1-1', 'importance-of-regular-saving',
    '2025 OL Section C Q4(b)(i) - Core',
    'Discuss three reasons why regular savings is important.',
    '3 reasons @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Reasons why regular saving is important', 15, 3, 5,
          semis(ch, '3 reasons @ 5 marks (graded 5:3:0)')[:CAP],
          'Three reasons at 5 marks, graded 5:3:0. Discuss, so each needs its consequence for the household — savings mean an emergency does not become a loan, and a record of saving is what a lender looks for later.')],
    'One flat list, taken in order to the cap.',
    stem='‘Saving money is one of the key aspects of having a secure financial future.’ (www.iciciprulife.com)'))

# 4(b)(ii) — the name and reasons strands; the two detail points have no scheme list
PROV = ['An Post:', 'Banks & Building Societies:', 'Credit Union:']
ch = block(Q4b, 'An Post: deposit account')
o_scheme = [bundle(h, '') for h in heads(block(ch, 'An Post:', '2 reasons @ 3 marks'), PROV)]
o_reason = semis(block(ch, '2 reasons @ 3 marks (graded 3:2:0)'), '2 reasons @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX + 'q4bii-name-reasons', Y, LV, 'home-economics-1-1', 'choosing-a-family-saving-scheme',
    '2025 OL Section C Q4(b)(ii) - Core - naming the scheme and reasons',
    'Name one saving scheme suitable for a family. Give two reasons for your choice.',
    'Name 3 marks (graded 3:2:0); 2 reasons @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Saving schemes suitable for a family', 3, 1, 3, o_scheme[:CAP],
          'Name one, 3 marks, graded 3:2:0. The scheme groups its options by provider — An Post, banks and building societies, credit unions — so naming the provider and the account type together is the safe answer.'),
     anyN('r-2', 'Reasons for the choice', 6, 2, 3, o_reason[:CAP],
          'Two reasons at 3 marks, graded 3:2:0. These are the practical comparisons between schemes: how easily you can get at the money, how safe it is, what interest it earns, whether it is taxed, and where and when you can call in.')],
    'The naming and reasons strands of Q4(b)(ii), worth 9 of the part\'s 15 marks. The two detail points at 3 marks each are held: the scheme lists the schemes and the reasons, and prints no marking points for the details.',
    stem='‘Saving money is one of the key aspects of having a secure financial future.’ (www.iciciprulife.com)',
    tariff_kind='fixed'))
held.append(dict(C(
    PFX + 'q4bii-details', Y, LV, 'home-economics-1-1', 'saving-scheme-details',
    '2025 OL Section C Q4(b)(ii) - Core - details of the scheme',
    'Give details of one saving scheme suitable for a family.',
    'Details 2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Details of the named saving scheme', 6, 2, 3, [], 'Two details at 3 marks.')],
    'The details strand of Q4(b)(ii).',
    stem='‘Saving money is one of the key aspects of having a secure financial future.’ (www.iciciprulife.com)'),
    heldReason='The scheme lists the saving schemes by provider and lists the reasons, but prints no marking points for the two detail points, which carry 6 of the part\'s 15 marks. The naming and reasons strands ship as he-2025-ol-sc-q4bii-name-reasons.'))

# 4(c)(i) — dealing with conflict, 15 marks
Q4c = block(Q4, 'or 4.(c) Conflict between generations')
ch = block(Q4c, '3 ways @ 5 marks (graded 5:3:0)', '(ii) Discuss three ways grandparents', occ=0)
cards.append(C(
    PFX + 'q4ci', Y, LV, 'home-economics-2-1', 'dealing-with-teenager-parent-conflict',
    '2025 OL Section C Q4(c)(i) - Core',
    'Describe three ways of dealing with conflict between teenagers and parents.',
    '3 ways @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Ways of dealing with conflict between teenagers and parents', 15, 3, 5,
          semis(ch, '3 ways @ 5 marks (graded 5:3:0)')[:CAP],
          'Three ways at 5 marks, graded 5:3:0. The scheme opens with "do not ignore conflict", which is the point most answers skip. Boundaries that everyone knows in advance, and compromise, are the two that are easiest to develop to a full 5.')],
    'One flat list, taken in order to the cap.',
    stem='Conflict between generations often revolves around differences in core values and life experiences.'))

# 4(c)(ii) — grandparents' support, 15 marks
ch = block(Q4c, '3 ways @ 5 marks (graded 5:3:0) help their children out financially')
cards.append(C(
    PFX + 'q4cii', Y, LV, 'home-economics-2-3', 'grandparents-support-for-the-family',
    '2025 OL Section C Q4(c)(ii) - Core',
    'Discuss three ways grandparents provide support for other family members.',
    '3 ways @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Ways grandparents provide support for other family members', 15, 3, 5,
          semis(ch, '3 ways @ 5 marks (graded 5:3:0)')[:CAP],
          'Three ways at 5 marks, graded 5:3:0. The scheme credits practical, financial and emotional support as separate categories, so one from each reads as three distinct ways. Passing on values between generations is the one worth naming explicitly.')],
    'One flat list, taken in order to the cap.',
    stem='Conflict between generations often revolves around differences in core values and life experiences.'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2025ol_secC.json'), 'w'),
          ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
