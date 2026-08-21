"""2021 Ordinary Level, Section C. The last Section C paper in the bank."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2021, 'ordinary')
SEC = tidy(T[22035:43751])
Y, LV, PFX, CAP = 2021, 'ordinary', 'he-2021-ol-sc-', 14
cards, held = [], []
def C(*a, **k):
    k.setdefault('section', 'C'); return card(*a, **k)
def bundle(h, prefix='', n=None):
    seg = semis(h, prefix); return '; '.join(seg[:n] if n else seg)
def verbatim(chunk, label):
    """Raw slice, label stripped, trailing 'etc.' trimmed. See he_2021_hl_secC."""
    t = tidy(chunk)
    if label and t.startswith(label):
        t = tidy(t[len(label):])
    return tidy(t.rstrip().rstrip('.').rstrip().removesuffix('etc').rstrip().rstrip(';'))

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 – Home Design', 'Elective 2 – Textiles')
E1a = block(E1, '1.(a) The diagram below', 'and 1.(b)')

ch = block(E1a, '4 advantages @ 5 marks each (graded 5:3:0) Reduces heating bills', '(ii) Name and describe')
cards.append(C(
    PFX+'q1ai', Y, LV, 'home-economics-3-6', 'advantages-of-home-insulation',
    '2021 OL Section C E1 Q1(a)(i)',
    'State four advantages of having a house well insulated.',
    '4 advantages @ 5 marks each (graded 5:3:0)', 20,
    [anyN('r-1', 'Advantages of a well insulated house', 20, 4, 5,
          semis(ch, '4 advantages @ 5 marks each (graded 5:3:0)')[:CAP],
          'Four advantages at 5 marks, graded 5:3:0 - 20 marks, the biggest part here. The scheme runs three ways: money (lower bills), comfort (steady temperature, less noise), and environment (less energy used, lower CO2, better BER). Take from all three rather than saying "saves money" four ways.')],
    'One flat list, taken in order to the cap.',
    stem='The diagram below shows the average heat loss for a family home. (www.ors.ie)'))

INS = ['(a) attic:', '(b) walls:', '(c) windows:']
h_at, h_wl, h_wn = heads(block(E1a, '(a) attic: blanket insulation', '(iii) State the advantages'), INS)
cards.append(C(
    PFX+'q1aii', Y, LV, 'home-economics-3-6', 'methods-of-insulation-attic-walls-windows',
    '2021 OL Section C E1 Q1(a)(ii)',
    'Name and describe the method of insulation you would recommend for each of the following: attic; walls; windows.',
    'Name 2 marks (graded 2:0) and description 3 marks (graded 3:0), x 3', 15,
    [anyN('r-1', 'Attic', 5, 1, 5, semis(h_at, '(a) attic:')[:CAP],
          'Name and describe one, 5 marks. Blanket insulation is the one to know - rolls of fibreglass or mineral wool laid between the joists. Loose fill, foam and blown fibre are the alternatives.'),
     anyN('r-2', 'Walls', 5, 1, 5, semis(h_wl, '(b) walls:')[:CAP],
          'Name and describe one, 5 marks. Cavity wall is the classic: two layers of block 5-10cm apart with the air gap acting as the insulator, or foam and beads pumped into that cavity. Dry lining and external render are the alternatives for solid walls.'),
     anyN('r-3', 'Windows', 5, 1, 5, semis(h_wn, '(c) windows:')[:CAP],
          'Name and describe one, 5 marks. Double or triple glazing - two or three sheets of glass with an air or argon gap. Low-emissivity glass reflects heat back into the room, and heavy lined curtains count too.')],
    'Fixed: three named areas of the house, priced identically at 5 marks each. Skipping one costs a straight 5.',
    stem='The diagram below shows the average heat loss for a family home. (www.ors.ie)',
    tariff_kind='fixed'))

h_adv, h_dis = heads(block(E1a, 'Advantages: provides a plentiful supply'), ['Advantages: provides a plentiful', 'Disadvantages: expensive to purchase'])
cards.append(C(
    PFX+'q1aiii', Y, LV, 'home-economics-3-6', 'advantages-and-disadvantages-of-solar-energy',
    '2021 OL Section C E1 Q1(a)(iii)',
    'State the advantages and/or the disadvantages of solar energy.',
    '3 points @ 5 marks each (graded 5:3:0)', 15,
    [anyN('r-1', 'Advantages and/or disadvantages of solar energy', 15, 3, 5,
          (semis(h_adv, 'Advantages:') + semis(h_dis, 'Disadvantages:'))[:CAP],
          'Three points at 5 marks, graded 5:3:0. "And/or" means all three may come from one side, so you are not forced to balance them - but two advantages and one disadvantage reads as a fuller answer. The SEAI grant and the BER increase are the two most students forget.')],
    'One flat list pooling both sides, because the question says "and/or" and the scheme prices three points across both.',
    stem='The diagram below shows the average heat loss for a family home. (www.ors.ie)'))

# ------------------------------------------------------------------- 1.(b)
E1b = block(E1, 'and 1.(b) Buying a first home', 'or 1.(c)')
h_ba, h_bd = heads(block(E1b, 'Advantages: an investment', '(ii) Discuss how the housing requirements'),
                   ['Advantages: an investment', 'Disadvantages: long-term commitment'])
o_ba, o_bd = semis(h_ba, 'Advantages:')[:CAP], semis(h_bd, 'Disadvantages:')[:CAP]
cards.append(C(
    PFX+'q1bi', Y, LV, 'home-economics-1-1', 'buying-a-home-advantages-and-disadvantages',
    '2021 OL Section C E1 Q1(b)(i)',
    'State the advantages and the disadvantages of buying a home of your own.',
    '3 points @ 4 marks each (graded 4:2:0) - 1 advantage + 1 disadvantage + 1 other point', 12,
    [anyN('r-1', 'One advantage of buying a home', 4, 1, 4, o_ba,
          'One advantage at 4 marks, and the scheme requires it. The strongest is that it is an investment with security of tenure - it is yours, and the value can rise.'),
     anyN('r-2', 'One disadvantage of buying a home', 4, 1, 4, o_bd,
          'One disadvantage at 4 marks, also required. The costs beyond the price are the real answer: deposit, legal fees, stamp duty, survey, property tax, and maintenance forever after.'),
     anyN('r-3', 'One further point, from either', 4, 1, 4, (o_ba + o_bd)[:CAP],
          'One further point at 4 marks, from either side - "1 advantage + 1 disadvantage + 1 other point". Whichever list you found easier is where to take it from.')],
    'Fixed: the scheme requires one point on each side, then floats the remaining 4 marks across both. Modelled as three rows so the two compulsory points cannot be lost.',
    stem='Buying a first home is an exciting adventure.',
    tariff_kind='fixed'))

h_fam, h_solo = heads(block(E1b, 'Family with children: depends on size'),
                      ['Family with children: depends on size', 'Person living on their own:'])
cards.append(C(
    PFX+'q1bii', Y, LV, 'home-economics-3-3', 'housing-requirements-family-versus-single-person',
    '2021 OL Section C E1 Q1(b)(ii)',
    'Discuss how the housing requirements of a family with children may differ from that of a person living on their own.',
    '3 points @ 6 marks each (graded 6:3:0)', 18,
    [anyN('r-1', 'How housing requirements differ', 18, 3, 6,
          (semis(h_fam, 'Family with children:') + semis(h_solo, 'Person living on their own:'))[:CAP],
          'Three points at 6 marks, graded 6:3:0 - the highest per-point rate on the paper, so develop each one. The word is "differ", so write in contrasts: a family needs space, storage and a garden and wants to be near schools; someone on their own needs less space and can choose a location and lifestyle to suit only themselves.')],
    'One flat list pooling both households, because the question asks how they differ and the scheme prices three points across both.',
    stem='Buying a first home is an exciting adventure.'))

# ------------------------------------------------------------------- 1.(c)
E1c = block(E1, 'or 1.(c) Interior designers')
ch = block(E1c, '3 factors @ 5 marks each (graded 5:3:0) Space available', '(ii) Explain how soft furnishings')
cards.append(C(
    PFX+'q1ci', Y, LV, 'home-economics-3-4', 'planning-the-interior-design-of-a-house',
    '2021 OL Section C E1 Q1(c)(i)',
    'Discuss three factors to be considered when planning the interior design of a house.',
    '3 factors @ 5 marks each (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors when planning interior design', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks each (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0. The scheme names them only, so the mark is in the sentence you add. Function of the room is the strongest - what happens in the room decides the flooring, the lighting and the furniture.')],
    'One flat list, taken in order to the cap.',
    stem='Interior designers help people create their dream home.'))

ch = block(E1c, '3 factors @ 5 marks each (graded 5:3:0) Add colour/pattern/texture')
cards.append(C(
    PFX+'q1cii', Y, LV, 'home-economics-3-4', 'soft-furnishings-and-room-appearance',
    '2021 OL Section C E1 Q1(c)(ii)',
    'Explain how soft furnishings can enhance the overall appearance of a room.',
    '3 factors @ 5 marks each (graded 5:3:0)', 15,
    [anyN('r-1', 'How soft furnishings enhance a room', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks each (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0. Name the furnishing as well as the effect - cushions and a throw add colour and texture, curtains make a room warm and cosy, a rug can act as the focal point. The economical-makeover point is the one worth ending on.')],
    'One flat list, taken in order to the cap.',
    stem='Interior designers help people create their dream home.'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 – Textiles', 'Elective 3 – Social Studies')
E2a = block(E2, '2.(a) ‘Fashions fade', 'and 2.(b)')

OCC = ['Woman: shape:', 'Man: shape:']
h_w, h_m = heads(block(E2a, 'Woman: shape: strong ballerina line', '(ii) Suggest one accessory'), OCC)
held.append(dict(C(
    PFX+'q2ai', Y, LV, 'home-economics-3-8', 'evaluating-occasion-wear',
    '2021 OL Section C E2 Q2(a)(i)',
    'Comment on the suitability of the occasion wear shown above. Refer to: shape; comfort; design features.',
    '2 points @ 3 marks each (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'Suitability of the occasion wear shown', 18, 6, 3,
          (semis(h_w, 'Woman:') + semis(h_m, 'Man:'))[:CAP], 'Held - see heldReason.')],
    'Held - see heldReason.',
    stem='‘Fashions fade, style is eternal.’ (Yves Saint Laurent)'),
    heldReason='Marks two outfit photographs printed on the paper. Every marking point describes those images ("strong ballerina line", "folded skirt adds width", "single button detail on jacket", "contrasting handkerchief in jacket pocket"), so the card is unanswerable without the figures and the markdown extraction does not carry them.'))

ACC = ['Woman: pashmina shawl', 'Man: cufflinks']
h_wa, h_ma = heads(block(E2a, 'Woman: pashmina shawl'), ACC)
o_acc = semis(h_wa, 'Woman:') + semis(h_ma, 'Man:')
cards.append(C(
    PFX+'q2aii', Y, LV, 'home-economics-3-8', 'accessorising-occasion-wear',
    '2021 OL Section C E2 Q2(a)(ii)',
    'Suggest one accessory you could add to enhance an occasion wear outfit, and give one reason for your choice.',
    '1 accessory @ 3 marks (graded 3:0); 1 reason @ 4 marks (graded 4:2:0)', 7,
    [anyN('r-1', 'The accessory', 3, 1, 3, o_acc[:CAP],
          'Name one, 3 marks, graded 3:0 - all or nothing, but any accessory in the list counts: a shawl, jewellery, a fascinator, cufflinks, a tie pin, a watch.'),
     anyN('r-2', 'Reason for the choice', 4, 1, 4, o_acc[:CAP],
          'One reason at 4 marks - more than the accessory itself, so this is where the marks are. The scheme’s reasons are about how the piece works with the outfit: it adds a layer, it complements the suit, it picks up the colour of the handkerchief.')],
    'Fixed: the accessory is priced at 3 and the reason at 4. Both rows draw on the same list, because the scheme prints each accessory together with the reason it works.',
    stem='‘Fashions fade, style is eternal.’ (Yves Saint Laurent)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 2.(b)
E2b = block(E2, 'and 2.(b) Today’s consumers', 'or 2.(c)')
CON = ['Weaving: is done on a loom', 'Knitting: can be done', 'Bonding: two or more fabrics']
con_opts = [verbatim(h, '') for h in heads(block(E2b, 'Weaving: is done on a loom', 'Macramé;'), CON)]
FAB = ['Linen:', 'Cotton:', 'Wool:', 'Silk:']
fab_opts = [f'{a.rstrip(":")} - {bundle(h, a)}'
            for h, a in zip(heads(block(E2b, 'Linen: absorbent', '(ii) Give two advantages'), FAB), FAB)]
cards.append(C(
    PFX+'q2bi', Y, LV, 'home-economics-3-7', 'profile-of-a-natural-fabric-ol',
    '2021 OL Section C E2 Q2(b)(i)',
    'Write a profile of a natural fabric under each of the following headings: how the fabric is constructed; properties.',
    'construction 1 point @ 3 marks (graded 3:2:0); properties 2 points @ 3 marks each (graded 3:2:0)', 9,
    [anyN('r-1', 'How the fabric is constructed', 3, 1, 3, con_opts[:CAP],
          'One point at 3 marks. Weaving is the one the scheme explains properly - the warp runs down the loom, the weft passes over and under it, and the selvedge forms at the edges. Knitting and bonding are the shorter alternatives.'),
     anyN('r-2', 'Properties', 6, 2, 3, fab_opts[:CAP],
          'Two properties at 3 marks each - two thirds of the marks. Pick the fabric first, then take two from its own line. Include a weakness as well as a strength: linen is strong and cool but creases badly, wool is warm but shrinks and can itch.')],
    'Fixed: construction is priced at 3 and the properties at 6. The properties row carries one option per fabric, because the two points must match whichever fabric was profiled.',
    stem='Today’s consumers are willing to pay more for clothing produced with natural fabrics.',
    tariff_kind='fixed'))

ch = block(E2b, '2 advantages @ 3 marks each (graded 3:2:0) Lightweight for summer wear')
cards.append(C(
    PFX+'q2bii', Y, LV, 'home-economics-3-7', 'advantages-of-natural-fibres',
    '2021 OL Section C E2 Q2(b)(ii)',
    'Give two advantages of using natural fibres/fabric in everyday wear.',
    '2 advantages @ 3 marks each (graded 3:2:0)', 6,
    [anyN('r-1', 'Advantages of natural fibres in everyday wear', 6, 2, 3,
          semis(ch, '2 advantages @ 3 marks each (graded 3:2:0)')[:CAP],
          'Two advantages at 3 marks, graded 3:2:0. The scheme ties several to a specific fabric and use - wool is warm for winter, cotton absorbs sweat so it suits sportswear, linen is lightweight for summer. Naming the fabric with the advantage is what makes it a 3.')],
    'One flat list, taken in order to the cap.',
    stem='Today’s consumers are willing to pay more for clothing produced with natural fabrics.'))

# ------------------------------------------------------------------- 2.(c)
E2c = block(E2, 'or 2.(c) Irish fashion is thriving')
CLO = ['(a) Function:', '(b) Money available:', '(c) Cultural influences:']
h_fn, h_mn, h_cu = heads(block(E2c, '(a) Function: 1 point @ 3 marks', '(ii) Discuss the contribution'), CLO)
cards.append(C(
    PFX+'q2ci', Y, LV, 'home-economics-3-8', 'factors-influencing-choice-of-clothing-ol',
    '2021 OL Section C E2 Q2(c)(i)',
    'Explain how each of the following factors may influence a person’s choice of clothing: function; money available; cultural influences.',
    '1 point @ 3 marks (graded 3:2:0) x 3', 9,
    [anyN('r-1', 'Function', 3, 1, 3, semis(h_fn, '(a) Function: 1 point @ 3 marks (graded 3:2:0)')[:CAP],
          'One point, 3 marks. Function is what the clothing has to do - the scheme’s example is a waterproof coat in winter. Name an occasion or condition and the garment that suits it.'),
     anyN('r-2', 'Money available', 3, 1, 3, semis(h_mn, '(b) Money available: 1 point @ 3 marks (graded 3:2:0)')[:CAP],
          'One point, 3 marks. Budget decides where you shop as much as what you buy - designer, chain store or charity shop - and value for money over time is the point worth making.'),
     anyN('r-3', 'Cultural influences', 3, 1, 3, semis(h_cu, '(c) Cultural influences: 1 point @ 3 marks (graded 3:2:0)')[:CAP],
          'One point, 3 marks. Modesty is the scheme’s main idea - different cultures cover differently - along with features borrowed between cultures, like pashminas, embroidery and beading.')],
    'Fixed: the question names all three factors, so all three must be answered. Priced identically at 3 marks each.',
    stem='Irish fashion is thriving on the international stage.',
    tariff_kind='fixed'))

ch = block(E2c, '2 contributions @ 3 marks each (graded 3:2:0) Young people want to wear')
cards.append(C(
    PFX+'q2cii', Y, LV, 'home-economics-3-8', 'trendsetters-and-fashion-trends',
    '2021 OL Section C E2 Q2(c)(ii)',
    'Discuss the contribution of trendsetters/bloggers to current fashion trends.',
    '2 contributions @ 3 marks each (graded 3:2:0)', 6,
    [anyN('r-1', 'Contribution of trendsetters and bloggers', 6, 2, 3,
          semis(ch, '2 contributions @ 3 marks each (graded 3:2:0)')[:CAP],
          'Two contributions at 3 marks, graded 3:2:0. Say the mechanism - young people copy what trendsetters wear, brands sponsor celebrities and hand them clothes for media events, and social media spreads it in hours rather than seasons.')],
    'One flat list, taken in order to the cap.',
    stem='Irish fashion is thriving on the international stage.'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 – Social Studies', 'Question 4 – Core')
E3a = block(E3, '3.(a) Education for a child', 'and 3.(b)')

DEV = ['Physical development:', 'Emotional development:', 'Intellectual development:']
h_ph, h_em, h_in = heads(block(E3a, 'Physical development: playing with toys', '(ii) Give an account of four factors'), DEV)
cards.append(C(
    PFX+'q3ai', Y, LV, 'home-economics-3-10', 'education-and-development-of-the-individual',
    '2021 OL Section C E3 Q3(a)(i)',
    'Outline how education contributes to the development of the individual. Refer to each of the following: physical development; emotional development; intellectual development.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'Physical development', 6, 2, 3, semis(h_ph, 'Physical development:')[:CAP],
          'Two points at 3 marks. School builds the body two ways - fine motor skills through practical subjects and handling equipment, and gross motor skills, bone and muscle through PE and sport.'),
     anyN('r-2', 'Emotional development', 6, 2, 3, semis(h_em, 'Emotional development:')[:CAP],
          'Two points at 3 marks. Starting school is the first real independence from parents, and it is where children learn to notice and respond to how other people feel.'),
     anyN('r-3', 'Intellectual development', 6, 2, 3, semis(h_in, 'Intellectual development:')[:CAP],
          'Two points at 3 marks, and the longest list. The range of subjects and the resources are the obvious ones; competition from classmates and the challenge of examinations are the ones that read as thought-out.')],
    'Fixed: the question names all three kinds of development and prices them identically at 6 marks each.',
    stem='Education for a child begins at home and is a lifelong process.',
    tariff_kind='fixed'))

ch = block(E3a, '4 factors @ 5 marks each (graded 5:3:0) Intellectual ability', '(iii) Explain three benefits')
cards.append(C(
    PFX+'q3aii', Y, LV, 'home-economics-3-10', 'factors-influencing-educational-achievement-ol',
    '2021 OL Section C E3 Q3(a)(ii)',
    'Give an account of four factors that influence the educational achievement of school children.',
    '4 factors @ 5 marks each (graded 5:3:0)', 20,
    [anyN('r-1', 'Factors influencing educational achievement', 20, 4, 5,
          semis(ch, '4 factors @ 5 marks each (graded 5:3:0)')[:CAP],
          'Four factors at 5 marks, graded 5:3:0 - 20 marks, the biggest part here. Say how the factor works, not just its name: a large family means financial strain and less one-to-one attention; the school environment covers resources, class size, SNAs and resource teachers.')],
    'One flat list, taken in order to the cap.',
    stem='Education for a child begins at home and is a lifelong process.'))

ch = block(E3a, '3 benefits @ 4 marks each (graded 4:2:0) Helps students decide')
cards.append(C(
    PFX+'q3aiii', Y, LV, 'home-economics-2-2', 'benefits-of-work-experience',
    '2021 OL Section C E3 Q3(a)(iii)',
    'Explain three benefits to students of participating in work experience while in second level school.',
    '3 benefits @ 4 marks each (graded 4:2:0)', 12,
    [anyN('r-1', 'Benefits of work experience to students', 12, 3, 4,
          semis(ch, '3 benefits @ 4 marks each (graded 4:2:0)')[:CAP],
          'Three benefits at 4 marks, graded 4:2:0. The scheme splits into finding direction (deciding on a career, seeing what a job actually involves) and building skills (communication, teamwork, timekeeping, confidence). One from each is the fullest answer, and "it goes on your CV" is a legitimate third.')],
    'One flat list, taken in order to the cap.',
    stem='Education for a child begins at home and is a lifelong process.'))

# ------------------------------------------------------------------- 3.(b)
E3b = block(E3, 'and 3.(b) ‘Physical activity plays', 'or 3.(c)')
ch = block(E3b, '3 reasons @ 5 marks each (graded 5:3:0) Helps people relax', '(ii) Describe how a person’s choice')
cards.append(C(
    PFX+'q3bi', Y, LV, 'home-economics-3-11', 'importance-of-leisure',
    '2021 OL Section C E3 Q3(b)(i)',
    'Discuss three reasons why leisure is important in today’s society.',
    '3 reasons @ 5 marks each (graded 5:3:0)', 15,
    [anyN('r-1', 'Reasons leisure is important', 15, 3, 5,
          semis(ch, '3 reasons @ 5 marks each (graded 5:3:0)')[:CAP],
          'Three reasons at 5 marks, graded 5:3:0. The scheme covers mind (relaxing, mental wellbeing, self-esteem), body (physical health) and people (social interaction, family bonding, community). One from each is the widest answer.')],
    'One flat list, taken in order to the cap.',
    stem='‘Physical activity plays an important role in the lives of children and young people.’ (www.education.ie)'))

LEI = ['Cost:', 'Occupation:', 'Age:']
h_c, h_o, h_a = heads(block(E3b, 'Cost: membership/annual/joining fee'), LEI)
cards.append(C(
    PFX+'q3bii', Y, LV, 'home-economics-3-11', 'influences-on-choice-of-leisure-activity',
    '2021 OL Section C E3 Q3(b)(ii)',
    'Describe how a person’s choice of leisure activities are influenced by each of the following: cost; occupation; age.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'Cost', 5, 1, 5, semis(h_c, 'Cost:')[:CAP],
          'One point, 5 marks. It is not only the fee - equipment and special clothing cost too, and someone with less disposable income turns to activities that are free, like walking.'),
     anyN('r-2', 'Occupation', 5, 1, 5, semis(h_o, 'Occupation:')[:CAP],
          'One point, 5 marks. The idea worth writing is contrast: someone sitting at a desk all day tends to choose something active, and someone doing physical work chooses something restful. Work also decides both the money and the hours available.'),
     anyN('r-3', 'Age', 5, 1, 5, semis(h_a, 'Age:')[:CAP],
          'One point, 5 marks. Time and money move in opposite directions across a life - young people have time but little money, parents of small children have neither, and retired people have time again.')],
    'Fixed: the question names all three influences, so all three must be answered. Priced identically at 5 marks each.',
    stem='‘Physical activity plays an important role in the lives of children and young people.’ (www.education.ie)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 3.(c)
E3c = block(E3, 'or 3.(c) The impact of unemployment')
UNE = ['Young individuals:', 'The family:', 'Society:']
h_y, h_f, h_s = heads(block(E3c, 'Young individuals: loss of income', '(ii) Name and give details'), UNE)
cards.append(C(
    PFX+'q3ci', Y, LV, 'home-economics-3-9', 'effects-of-unemployment-ol',
    '2021 OL Section C E3 Q3(c)(i)',
    'Discuss the effects of unemployment on: young individuals; the family; society.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'Young individuals', 6, 2, 3, semis(h_y, 'Young individuals:')[:CAP],
          'Two points at 3 marks. The scheme goes further into the mind than the wallet - worthlessness, loss of identity and status, isolation, boredom, depression. Take one money point and one of those.'),
     anyN('r-2', 'The family', 6, 2, 3, semis(h_f, 'The family:')[:CAP],
          'Two points at 3 marks. Keep it at household level: trouble paying rent and bills, strain on relationships, children suffering at school, and at worst losing the home.'),
     anyN('r-3', 'Society', 6, 2, 3, semis(h_s, 'Society:')[:CAP],
          'Two points at 3 marks - the row most students leave thin. It is about cost and consequence to the country: benefits to pay, higher taxes, emigration, crime, and the cycle of poverty continuing.')],
    'Fixed: three named strands, priced identically at 6 marks each. Answer all three - six good points about young people still scores 6.',
    stem='The impact of unemployment can be long lasting.',
    tariff_kind='fixed'))

ch_names = block(E3c, 'St. Vincent de Paul; Rotary', 'Can act as pressure groups')
ch_det = block(E3c, 'Can act as pressure groups')
cards.append(C(
    PFX+'q3cii', Y, LV, 'home-economics-3-9', 'voluntary-organisations-supporting-the-unemployed',
    '2021 OL Section C E3 Q3(c)(ii)',
    'Name and give details of one voluntary organisation that provides support to the unemployed.',
    'Name 4 marks (graded 4:0); 2 details @ 4 marks each (graded 4:2:0)', 12,
    [anyN('r-1', 'Name of the voluntary organisation', 4, 1, 4, semis(ch_names)[:CAP],
          'Name one, 4 marks, graded 4:0 - all or nothing, so give the organisation’s actual name. Seven are accepted, including Men’s Sheds, which students often overlook.'),
     # This one list is comma-separated, not semicolon-separated, so semis()
     # returns it as a single option and the audit rejected 2 claims from 1.
     # Each comma-separated clause is verbatim in the scheme on its own.
     anyN('r-2', 'Details of the organisation', 8, 2, 4,
          [tidy(x).rstrip('.') for x in verbatim(ch_det, '').split(',') if tidy(x)][:CAP],
          'Two details at 4 marks - two thirds of the marks. The scheme prints one shared list rather than describing each body, so these apply to whichever you named: acting as a pressure group, informing government, funding classes that teach coping skills, and giving people a place to talk about their situation.')],
    'Fixed: naming is priced at 4 and the details at 8. The scheme prints one set of details covering all the organisations rather than describing each, so the details row is a single shared list.',
    stem='The impact of unemployment can be long lasting.',
    tariff_kind='fixed'))

# ------------------------------------------------------------- Question 4 Core
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) The ultimate convenience food', 'and 4.(b)')

h_nut, h_die = heads(block(Q4a, 'Nutritive value: HBV protein', '(ii) Outline:'),
                     ['Nutritive value: HBV protein', 'Dietetic Value:'])
o_nut, o_die = semis(h_nut, 'Nutritive value:')[:CAP], semis(h_die, 'Dietetic Value:')[:CAP]
cards.append(C(
    PFX+'q4ai', Y, LV, 'home-economics-0-9', 'nutritive-and-dietetic-value-of-eggs',
    '2021 OL Section C Q4(a)(i) - Core',
    'Give an account of the nutritive value and the dietetic value of eggs.',
    '5 points @ 4 marks each (graded 4:2:0) - 2 references to nutritive value, 2 references to dietetic value, plus 1 other', 20,
    [anyN('r-1', 'Two references to nutritive value', 8, 2, 4, o_nut,
          'Two points at 4 marks, and the scheme requires them. Nutritive value is what is in the egg - HBV protein at 100% biological value, lecithin as a natural emulsifier, fat-soluble vitamins A, D, E and K. Worth knowing that the white is fat free and the yolk carries the cholesterol.'),
     anyN('r-2', 'Two references to dietetic value', 8, 2, 4, o_die,
          'Two points at 4 marks, also required. Dietetic value is who it suits and why - easy to digest, quick to cook, ideal for growing children, and important in a vegetarian diet. Its weaknesses count too: no vitamin C, and the cholesterol.'),
     anyN('r-3', 'One further point, from either value', 4, 1, 4, (o_nut + o_die)[:CAP],
          'One further point at 4 marks, from either list - "2 references to nutritive value, 2 references to dietetic value, plus 1 other".')],
    'Fixed: the scheme requires two points on each value, then floats the remaining 4 marks across both. Modelled as three rows so the four compulsory points cannot be lost.',
    stem='The ultimate convenience food, eggs are powerhouses of nutrition. (www.bbcgoodfood.com)',
    tariff_kind='fixed'))

ch_ways = block(Q4a, 'Eating on their own e.g. scrambled', '3 effects @ 3 marks each')
ch_eff = block(Q4a, '3 effects @ 3 marks each (graded 3:2:0) Protein coagulates', '(iii) Give three reasons')
cards.append(C(
    PFX+'q4aii', Y, LV, 'home-economics-0-9', 'using-eggs-in-the-diet-and-effects-of-heat',
    '2021 OL Section C Q4(a)(ii) - Core',
    'Outline different ways of including eggs in the diet, and the effects of heat on eggs.',
    'ways 3 @ 3 marks each; effects 3 @ 3 marks each (graded 3:2:0)', 18,
    [anyN('r-1', 'Ways of including eggs in the diet', 9, 3, 3, semis(ch_ways)[:CAP],
          'Three ways at 3 marks. The scheme gives an example with every point, so use them - the mark comes from the dish, not the category. Work through the day: scrambled at breakfast, quiche at lunch, scotch eggs at dinner, meringue for dessert.'),
     anyN('r-2', 'Effects of heat on eggs', 9, 3, 3,
          semis(ch_eff, '3 effects @ 3 marks each (graded 3:2:0)')[:CAP],
          'Three effects at 3 marks. Protein coagulating so the egg sets is the central one. The two that show real knowledge are curdling, and the green-grey iron/sulphur ring around the yolk of an overboiled egg.')],
    'Fixed: the question names two strands and prices them identically at 9 marks each.',
    stem='The ultimate convenience food, eggs are powerhouses of nutrition. (www.bbcgoodfood.com)',
    tariff_kind='fixed'))

ch = block(Q4a, '3 reasons @ 4 marks each (graded 4:2:0) Foods healthier')
cards.append(C(
    PFX+'q4aiii', Y, LV, 'home-economics-0-11', 'popularity-of-small-irish-food-producers',
    '2021 OL Section C Q4(a)(iii) - Core',
    'Give three reasons for the growing popularity of goods supplied by small Irish food producers.',
    '3 reasons @ 4 marks each (graded 4:2:0)', 12,
    [anyN('r-1', 'Reasons for the popularity of small Irish food producers', 12, 3, 4,
          semis(ch, '3 reasons @ 4 marks each (graded 4:2:0)')[:CAP],
          'Three reasons at 4 marks, graded 4:2:0. The scheme is short - quality and taste, organic production, local employment, and people willing to pay more for better. Say why each one draws the shopper in.')],
    'One flat list, taken in order to the cap.',
    stem='The ultimate convenience food, eggs are powerhouses of nutrition. (www.bbcgoodfood.com)'))

# ------------------------------------------------------------------- 4.(b)
Q4b = block(Q4, 'and 4.(b) Consumers want to hear', 'or 4.(c)')
SHOP = ['Household income:', 'Discount offers:', 'Shopper loyalty schemes:']
h_hi, h_do, h_ls = heads(block(Q4b, 'Household income: amount of money', '(ii) State the advantages'), SHOP)
cards.append(C(
    PFX+'q4bi', Y, LV, 'home-economics-1-2', 'influences-on-consumer-decision-making',
    '2021 OL Section C Q4(b)(i) - Core',
    'Discuss how the following might affect consumers’ decision making when shopping: household income; discount offers; shopper loyalty schemes.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'Household income', 5, 1, 5, semis(h_hi, 'Household income:')[:CAP],
          'One point, 5 marks. When money is tight the order changes - needs before luxuries, and value for money becomes the deciding factor rather than preference.'),
     anyN('r-2', 'Discount offers', 5, 1, 5, semis(h_do, 'Discount offers:')[:CAP],
          'One point, 5 marks. The scheme is blunt about it: offers create the impression of a bargain and push impulse buying, so people end up spending more, not less.'),
     anyN('r-3', 'Shopper loyalty schemes', 5, 1, 5, semis(h_ls, 'Shopper loyalty schemes:')[:CAP],
          'One point, 5 marks, and the longest list. Points and perks build an emotional tie to one shop, which is exactly the point - a loyal shopper stops comparing prices elsewhere.')],
    'Fixed: the question names all three influences, so all three must be answered. Priced identically at 5 marks each.',
    stem='‘Consumers want to hear about discounts and sales, not just products.’ (www.retail-week.com)',
    tariff_kind='fixed'))

h_oa, h_od = heads(block(Q4b, 'Advantages: Do not have to leave home'),
                   ['Advantages: Do not have to leave home', 'Disadvantages: delay in delivery'])
o_oa, o_od = semis(h_oa, 'Advantages:')[:CAP], semis(h_od, 'Disadvantages:')[:CAP]
cards.append(C(
    PFX+'q4bii', Y, LV, 'home-economics-1-2', 'advantages-and-disadvantages-of-online-shopping',
    '2021 OL Section C Q4(b)(ii) - Core',
    'State the advantages and the disadvantages of online shopping.',
    '3 points @ 5 marks each (graded 5:3:0) - 1 advantage, 1 disadvantage, plus 1 other', 15,
    [anyN('r-1', 'One advantage of online shopping', 5, 1, 5, o_oa,
          'One advantage at 5 marks, and the scheme requires it. Convenience is the heart of it - no need to leave home, no opening hours, and you can compare across sites and read reviews before buying.'),
     anyN('r-2', 'One disadvantage of online shopping', 5, 1, 5, o_od,
          'One disadvantage at 5 marks, also required. Not being able to touch or try the goods is the main one, along with the risks - fraud, sites that are not legitimate, and the cost and hassle of returning things.'),
     anyN('r-3', 'One further point, from either', 5, 1, 5, (o_oa + o_od)[:CAP],
          'One further point at 5 marks, from either side - "1 advantage, 1 disadvantage, plus 1 other".')],
    'Fixed: the scheme requires one point on each side, then floats the remaining 5 marks across both. Modelled as three rows so the two compulsory points cannot be lost.',
    stem='‘Consumers want to hear about discounts and sales, not just products.’ (www.retail-week.com)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 4.(c)
Q4c = block(Q4, 'or 4.(c) The goal of conflict resolution')
ch = block(Q4c, '3 factors @ 5 marks each (graded 5:3:0) Peer pressure', '(ii) Discuss three aspect')
cards.append(C(
    PFX+'q4ci', Y, LV, 'home-economics-2-1', 'influences-on-adolescent-behaviour',
    '2021 OL Section C Q4(c)(i) - Core',
    'Identify three factors which may influence an adolescent’s/teenager’s behaviour.',
    '3 factors @ 5 marks each (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors influencing an adolescent’s behaviour', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks each (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0. Peer and exam pressure are the two students name first; the ones that develop best are about the home - parents as role models, and whether the relationship is open enough for a teenager to say what they feel.')],
    'One flat list, taken in order to the cap.',
    stem='The goal of conflict resolution is not to decide who is right or wrong.'))

ch = block(Q4c, '3 aspects @ 5 marks each (graded 5:3:0) Adolescent question rules')
cards.append(C(
    PFX+'q4cii', Y, LV, 'home-economics-2-1', 'adolescent-behaviour-and-conflict-in-the-home',
    '2021 OL Section C Q4(c)(ii) - Core',
    'Discuss three aspects of adolescent/teenager’s behaviour that may lead to conflict in the home.',
    '3 aspects @ 5 marks each (graded 5:3:0)', 15,
    [anyN('r-1', 'Aspects of adolescent behaviour leading to conflict', 15, 3, 5,
          semis(ch, '3 aspects @ 5 marks each (graded 5:3:0)')[:CAP],
          'Three aspects at 5 marks, graded 5:3:0. Say where the friction comes from, not just the behaviour - questioning rules is a teenager pushing for independence, and rows about study or an untidy room are usually about who gets to decide.')],
    'One flat list, taken in order to the cap.',
    stem='The goal of conflict resolution is not to decide who is right or wrong.'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2021ol_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
