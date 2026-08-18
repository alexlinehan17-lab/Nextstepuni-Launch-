"""2024 Ordinary Level, Section C."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2024, 'ordinary')
SEC = tidy(T[25127:48667])
Y, LV, PFX, CAP = 2024, 'ordinary', 'he-2024-ol-sc-', 14
cards, held = [], []
def C(*a, **k):
    k.setdefault('section', 'C'); return card(*a, **k)
def bundle(h, prefix='', n=None):
    seg = semis(h, prefix); return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 –', 'Elective 2 –')
E1a = block(E1, '1.(a) ‘The quality of drinking water', 'and 1.(b)')
STG = ['screening impurities', 'sedimentation chemicals', 'filtration water passes',
       'chlorination chlorine', 'fluoridation fluoride', 'softening softener', 'testing water is tested']
ch = block(E1a, 'screening impurities', '(ii) Explain what precautions')
cards.append(C(
    PFX+'q1ai', Y, LV, 'home-economics-3-5', 'treatment-of-public-water-supply',
    '2024 OL Section C E1 Q1(a)(i)',
    'Describe four stages involved in the treatment of public water supply to make it safe for human consumption.',
    '4 stages @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Stages in the treatment of public water supply', 20, 4, 5,
          [bundle(h, ' '.join(p.split()[:1])) for h, p in zip(heads(ch, STG), STG)][:CAP],
          'Four stages at 5 marks, graded 5:3:0 — no 4, so naming a stage without saying what it removes drops straight to 3. The stages run in order and the order is the answer: screening takes out debris, sedimentation settles the solids, filtration catches what is left, chlorination kills the bacteria.')],
    'One option per stage, each carrying that stage\'s own description, because the question asks for stages and the scheme prices them as whole steps.',
    stem='‘The quality of drinking water is a powerful environmental determinant of health.’ (www.hse.ie)'))

ch = block(E1a, '3 points @ 5 marks (graded 5:3:0) storage tank in the attic', '(iii) Describe the function')
cards.append(C(
    PFX+'q1aii', Y, LV, 'home-economics-3-5', 'preventing-cold-water-supply-freezing',
    '2024 OL Section C E1 Q1(a)(ii)',
    'Explain what precautions should be taken to prevent the cold-water supply freezing in the home during cold weather.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Precautions to prevent the cold-water supply freezing', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three precautions at 5 marks, graded 5:3:0. Say what each one prevents — lagging the pipes stops them bursting when the water in them expands. Insulating the attic tank and lagging the pipes are two separate points, not one.')],
    'One flat list, taken in order to the cap.',
    stem='‘The quality of drinking water is a powerful environmental determinant of health.’ (www.hse.ie)'))

ch = block(E1a, 'service pipe connects the mains pipe')
h_sp, h_bv, h_st = heads(ch, ['service pipe connects', 'ball valve controls', 'storage tank located'])
cards.append(C(
    PFX+'q1aiii', Y, LV, 'home-economics-3-5', 'cold-water-system-components',
    '2024 OL Section C E1 Q1(a)(iii)',
    'Describe the function of the following in relation to the cold-water supply of a house: service pipe; ball valve; storage tank.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'service pipe', 5, 1, 5, semis(h_sp, 'service pipe')[:CAP],
          'One point, 5 marks, graded 5:3:0. It brings mains water into the house and surfaces at the kitchen sink — that tap is the drinking-water tap, which is why the service pipe matters.'),
     anyN('r-2', 'ball valve', 5, 1, 5, semis(h_bv, 'ball valve')[:CAP],
          'One point, 5 marks, graded 5:3:0. Describe the float: it rides on the surface, closes the valve when the tank is full, and drops to reopen it as water is used. That cycle is the full answer.'),
     anyN('r-3', 'storage tank', 5, 1, 5, semis(h_st, 'storage tank')[:CAP],
          'One point, 5 marks, graded 5:3:0. The height is the point — it sits in the attic so gravity supplies pressure to the taps, toilets and hot press below.')],
    'Fixed: three named components, priced identically. All three are short and factual, so this is the cheapest 15 marks in the elective.',
    stem='‘The quality of drinking water is a powerful environmental determinant of health.’ (www.hse.ie)',
    tariff_kind='fixed'))

E1b = block(E1, 'and 1.(b) ‘Over the past ten years', 'or 1.(c)')
ch = block(E1b, '3 points @ 5 marks (graded 5:3:0) must be got from local planning', '(ii) Discuss the role')
cards.append(C(
    PFX+'q1bi', Y, LV, 'home-economics-3-3', 'applying-for-planning-permission',
    '2024 OL Section C E1 Q1(b)(i)',
    'Describe the procedure to follow when applying for full planning permission to build a house.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Procedure for applying for full planning permission', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0. Follow it as a sequence: apply to the local authority before any work starts, submit the maps, plans, form and fee, publish the newspaper notice and post the site notice, then the authority grants, seeks more information, or refuses.')],
    'One flat list, taken in order to the cap.',
    stem='‘Over the past ten years the way we design our homes has changed a lot.’ (www.houzz.ie)'))

ch = block(E1b, 'architect advises on choice of site')
h_a, h_e, h_s = heads(ch, ['architect advises', 'engineer provides advice', 'solicitor deals with'])
cards.append(C(
    PFX+'q1bii', Y, LV, 'home-economics-3-3', 'professional-services-when-building-a-house',
    '2024 OL Section C E1 Q1(b)(ii)',
    'Discuss the role of the following professional services when designing and building a house: architect; engineer; solicitor.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'architect', 5, 1, 5, semis(h_a, 'architect')[:CAP],
          'One point, 5 marks, graded 5:3:0. The architect has the longest list — site choice, plans, the planning application, and overseeing construction — so this is the easiest of the three to develop.'),
     anyN('r-2', 'engineer', 5, 1, 5, semis(h_e, 'engineer')[:CAP],
          'One point, 5 marks, graded 5:3:0. The shortest list: the engineer is about structure, not appearance. Advises on the structure, oversees the project, solves building problems.'),
     anyN('r-3', 'solicitor', 5, 1, 5, semis(h_s, 'solicitor')[:CAP],
          'One point, 5 marks, graded 5:3:0. Everything legal — building and planning regulations, title deeds, rights of way, and the mortgage.')],
    'Fixed: three named professionals, priced identically. Skipping one costs a straight 5.',
    stem='‘Over the past ten years the way we design our homes has changed a lot.’ (www.houzz.ie)',
    tariff_kind='fixed'))

E1c = block(E1, 'or 1.(c) All homes in Ireland')
ch = block(E1c, '3 points @ 5 marks (graded 5:3:0) provides fresh air', '(ii) Name one method of ventilation')
cards.append(C(
    PFX+'q1ci', Y, LV, 'home-economics-3-5', 'advantages-of-good-ventilation',
    '2024 OL Section C E1 Q1(c)(i)',
    'Discuss three advantages of having good ventilation in the home.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Advantages of good ventilation in the home', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three advantages at 5 marks, graded 5:3:0. The list runs from air quality through to damage prevention — take one from each end (fresh air, prevents mould, reduces illness) so they cannot be read as the same advantage restated.')],
    'One flat list, taken in order to the cap.',
    stem='All homes in Ireland should have good ventilation.'))

ch = block(E1c, 'extractor fan powered by electricity')
h_ef, h_ch, h_av = heads(ch, ['extractor fan powered', 'cooker hood powered', 'air vents warm moisture'])
o_acc = semis(block(ch, 'Accept open doors', 'air vents warm moisture'), 'Accept')
cards.append(C(
    PFX+'q1cii', Y, LV, 'home-economics-3-5', 'kitchen-ventilation-methods',
    '2024 OL Section C E1 Q1(c)(ii)',
    'Name one method of ventilation suitable for a kitchen and explain the underlying principle of the method named.',
    'Name 5 marks (graded 5:3:0); underlying principles 2 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Methods of ventilation suitable for a kitchen', 5, 1, 5,
          (['extractor fan', 'cooker hood', 'air vents'] + o_acc)[:CAP],
          'Name one, 5 marks, graded 5:3:0. The extractor fan and cooker hood are the two the scheme explains in full, so they are the safe choices — the other 10 marks depend on being able to explain the method you named.'),
     anyN('r-2', 'Underlying principle of the method named', 10, 2, 5,
          (semis(h_ef, 'extractor fan') + semis(h_ch, 'cooker hood') + semis(h_av, 'air vents'))[:CAP],
          'Two points at 5 marks, graded 5:3:0 — ten of the fifteen marks. For the powered methods the principle is suction: the motor spins the blades, that draws stale air out, and fresh air is pulled in under doors or through vents. For air vents it is convection instead — warm stale air rises and leaves high up, cold fresh air enters lower down.')],
    'Fixed: naming is priced at 5 and the principle at 10. The principle row pools the scheme\'s three explained methods, because the two marks are awarded for whichever method the candidate named.',
    stem='All homes in Ireland should have good ventilation.',
    tariff_kind='fixed'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 –', 'Elective 3 –')
E2a = block(E2, '2.(a) Sportwear needs', 'and 2.(b)')
ch = block(E2a, 'comfort allows for ease of movement', '(ii) Describe how emphasis')
h_c, h_f, h_ae = heads(ch, ['comfort allows for ease', 'function suitable for different', 'aesthetic appeal stripes'])
held.append(dict(C(
    PFX+'q2ai', Y, LV, 'home-economics-3-8', 'suitability-of-sportswear',
    '2024 OL Section C E2 Q2(a)(i)',
    'Comment on the suitability of the sportwear shown above. Refer to: comfort; function; aesthetic appeal.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'comfort', 6, 2, 3, semis(h_c, 'comfort')[:CAP], 'Two points at 3 marks, graded 3:2:0.'),
     anyN('r-2', 'function', 6, 2, 3, semis(h_f, 'function')[:CAP], 'Two points at 3 marks, graded 3:2:0.'),
     anyN('r-3', 'aesthetic appeal', 6, 2, 3, semis(h_ae, 'aesthetic appeal')[:CAP], 'Two points at 3 marks, graded 3:2:0.')],
    'Fixed: three headings named in the question, priced equally.',
    stem='Sportwear needs to be practical but can also be stylish.', tariff_kind='fixed'),
    heldReason='Marks sportswear printed on the paper. Every option describes that image ("narrowed cuff on man’s hoodie", "woman’s jacket is water resistant"), so the card is unanswerable without the figure and the markdown extraction does not carry it.'))
ch = block(E2a, '1 point @ 4 marks (graded 4:2:0), 2nd point @ 3 marks (graded 3:2:0)')
held.append(dict(C(
    PFX+'q2aii', Y, LV, 'home-economics-3-8', 'emphasis-applied-to-an-outfit',
    '2024 OL Section C E2 Q2(a)(ii)',
    'Describe how emphasis as a design principle is applied to the outfits pictured above.',
    '1 point @ 4 marks (graded 4:2:0); 2nd point @ 3 marks (graded 3:2:0)', 7,
    [anyN('r-1', 'How emphasis is applied to the outfits', 7, 2, 3,
          semis(ch, '1 point @ 4 marks (graded 4:2:0), 2nd point @ 3 marks (graded 3:2:0)')[:CAP],
          'Two points, the first at 4 marks and the second at 3.')],
    'The scheme prices the first point at 4 and the second at 3.',
    stem='Sportwear needs to be practical but can also be stylish.'),
    heldReason='Every option names a colour or feature of the outfits pictured on the paper ("bright yellow t-shirt", "yellow stripe on side and back of tracksuit bottom"), so the card cannot be answered without the figure.'))

E2b = block(E2, 'and 2.(b) ‘Textiles have', 'or 2.(c)')
prod = heads(block(E2b, 'fibre production linen made', 'properties linen absorbent'),
             ['linen made from', 'cotton comes from', 'wool fleece', 'silk silkworms'])
props = heads(block(E2b, 'properties linen absorbent', 'test to identify a natural fibre'),
              ['linen absorbent', 'cotton absorbent', 'wool warm', 'silk absorbent'])
tst = block(E2b, 'test to identify a natural fibre hold fabric over')
o_gen = semis(block(tst, 'test to identify a natural fibre hold fabric over', 'linen takes longer'),
              'test to identify a natural fibre')
iden = heads(tst, ['linen takes longer', 'cotton flares up', 'wool burns slowly', 'silk burns slowly'])
FIB = [('linen', 'Linen', 'the stem of the flax plant'), ('cotton', 'Cotton', 'the boll of the cotton plant'),
       ('wool', 'Wool', 'the fleece of sheep, goats and llamas'), ('silk', 'Silk', 'the cocoon of the silkworm')]
for i, (slug, name, src) in enumerate(FIB):
    cards.append(C(
        PFX+'q2b-'+slug, Y, LV, 'home-economics-3-7', f'natural-fibre-profile-{slug}-ol',
        f'2024 OL Section C E2 Q2(b) - {name}',
        'Write a profile of a natural fibre under each of the following headings: fibre production; properties; test to identify a natural fibre.',
        '1 point @ 5 marks (graded 5:3:0) x 3', 15,
        [anyN('r-1', 'Fibre production', 5, 1, 5, semis(prod[i], slug)[:CAP],
              f'One point, 5 marks, graded 5:3:0 — no 4, so a bare statement drops to 3. {name} comes from {src}. The scheme lists the stages in order, so write the process as a sequence and the 5 is safe.'),
         anyN('r-2', 'Properties', 5, 1, 5, semis(props[i], slug)[:CAP],
              'One point, 5 marks, graded 5:3:0. Single-word properties, so give several and say what each means for wearing or washing the fabric — a list of adjectives alone reads as one thin point.'),
         anyN('r-3', 'Test to identify a natural fibre', 5, 1, 5, (o_gen + semis(iden[i], slug))[:CAP],
              'One point, 5 marks, graded 5:3:0. This is the burn test and the first two options are the method itself — hold the fabric over a flameproof dish and ignite it. The marks then come from what you observe for this fibre: how it takes the flame, the residue, and the smell.')],
        'One of four parallel profiles the scheme prints under Q2(b). A candidate profiles a single fibre, so each fibre is its own card with its own questionRef rather than pooling four sets of marking points into one menu. The test row keeps the scheme\'s shared method lines ahead of the fibre-specific observations.',
        stem='‘Textiles have such an important bearing on our daily lives.’ (www.coats.com)',
        tariff_kind='fixed'))

E2c = block(E2, 'or 2.(c) ‘Fashion has two purposes')
ch = block(E2c, '2 points @ 3 marks (graded 3:2:0) light weight leggings', '(ii) Discuss three factors')
cards.append(C(
    PFX+'q2ci', Y, LV, 'home-economics-3-8', 'summer-fashion-trends',
    '2024 OL Section C E2 Q2(c)(i)',
    'Describe two fashion trends currently popular in summer clothing.',
    '2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Fashion trends currently popular in summer clothing', 6, 2, 3,
          semis(ch, '2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Only two points at 3 marks — a six-mark part. Describe, so name the garment and say what makes it the trend: the cut, the fabric, or the finish.')],
    'One flat list, taken in order to the cap.',
    stem='‘Fashion has two purposes comfort and love.’ (Coco Chanel)'))

ch = block(E2c, '3 points @ 3 marks (graded 3:2:0) comfortable')
cards.append(C(
    PFX+'q2cii', Y, LV, 'home-economics-3-8', 'choosing-work-wear-clothing',
    '2024 OL Section C E2 Q2(c)(ii)',
    'Discuss three factors that influence a person’s choice when choosing work wear clothing.',
    '3 points @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Factors influencing the choice of work wear clothing', 9, 3, 3,
          semis(ch, '3 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Three factors at 3 marks, graded 3:2:0. Tie each to the job — high visibility and waterproofing matter for outdoor work, easy care and ease of movement for a busy indoor job. A factor named without the job it suits is 2.')],
    'One flat list, taken in order to the cap.',
    stem='‘Fashion has two purposes comfort and love.’ (Coco Chanel)'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 –', 'Question 4 – Core')
E3a = block(E3, '3.(a) ‘Of women over 15', 'and 3.(b)')
ch = block(E3a, 'paid work done for financial gain', '(ii) Discuss three reasons')
h_p, h_u, h_v = heads(ch, ['paid work done', 'unpaid work no financial', 'voluntary work involves'])
cards.append(C(
    PFX+'q3ai', Y, LV, 'home-economics-2-2', 'types-of-work-paid-unpaid-voluntary',
    '2024 OL Section C E3 Q3(a)(i)',
    'Explain the following types of work: paid work; unpaid work; voluntary work.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'paid work', 5, 1, 5, semis(h_p, 'paid work')[:CAP],
          'One point, 5 marks, graded 5:3:0 — the longest of the three lists. Beyond "done for money", the scheme credits the forms it takes (permanent, temporary, full-time, part-time, contract) and the security it brings (pension, PRSI, holiday and sick pay).'),
     anyN('r-2', 'unpaid work', 5, 1, 5, semis(h_u, 'unpaid work')[:CAP],
          'One point, 5 marks, graded 5:3:0. Unpaid work is still work — childrearing, caring for older or disabled family members, housework, DIY, and work placement. Name examples, do not just say it is unpaid.'),
     anyN('r-3', 'voluntary work', 5, 1, 5, semis(h_v, 'voluntary work')[:CAP],
          'One point, 5 marks, graded 5:3:0. The shortest list, so it needs all of it: for a community or charity, no financial reward, and done to make a difference to other people.')],
    'Fixed: three named types of work, priced identically. The distinction between unpaid and voluntary is the one students blur — unpaid work is for your own household, voluntary work is for someone else\'s.',
    stem='‘Of women over 15 years of age in Ireland, more than 50% of them are in the workforce.’ (www.cso.ie)',
    tariff_kind='fixed'))

ch = block(E3a, '3 reasons @ 5 marks (graded 5:3:0) better educated', '(iii) Evaluate the impact')
cards.append(C(
    PFX+'q3aii', Y, LV, 'home-economics-2-2', 'women-in-the-workforce',
    '2024 OL Section C E3 Q3(a)(ii)',
    'Discuss three reasons for the increased participation of women in the work force.',
    '3 reasons @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Reasons for the increased participation of women in the workforce', 15, 3, 5,
          semis(ch, '3 reasons @ 5 marks (graded 5:3:0)')[:CAP],
          'Three reasons at 5 marks, graded 5:3:0 — no 4, so a reason without development drops to 3. The list has two halves: what changed for women (better educated, equal pay, equality legislation) and what changed at home (childcare options, flexible hours, two incomes needed). One from each shows range.')],
    'One flat list, taken in order to the cap.',
    stem='‘Of women over 15 years of age in Ireland, more than 50% of them are in the workforce.’ (www.cso.ie)'))

ch = block(E3a, '4 points @ 5 marks (graded 5:3:0) increase in disposable income')
cards.append(C(
    PFX+'q3aiii', Y, LV, 'home-economics-2-0', 'impact-of-dual-earner-families',
    '2024 OL Section C E3 Q3(a)(iii)',
    'Evaluate the impact of dual earner families on family life.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Impact of dual earner families on family life', 20, 4, 5,
          semis(ch, '4 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Four points at 5 marks, graded 5:3:0 — the biggest single row in the elective. Evaluate means both directions score: higher income and both parents sharing the childrearing, but also role overload, role conflict, and children who feel neglected. An answer that is all positive leaves marks behind.')],
    'One flat list, taken in order to the cap.',
    stem='‘Of women over 15 years of age in Ireland, more than 50% of them are in the workforce.’ (www.cso.ie)'))

E3b = block(E3, 'and 3.(b) Leisure time is time', 'or 3.(c)')
ch = block(E3b, 'gender some activities are male/female dominated', '(ii) Evaluate the benefits')
h_g, h_ag, h_cu = heads(ch, ['gender some activities', 'age young people', 'cultural influences in a particular'])
cards.append(C(
    PFX+'q3bi', Y, LV, 'home-economics-3-11', 'influences-on-family-leisure-activities',
    '2024 OL Section C E3 Q3(b)(i)',
    'Discuss how family leisure activities are influenced by each of the following: gender; age; cultural influences.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'gender', 5, 1, 5, semis(h_g, 'gender')[:CAP],
          'One point, 5 marks, graded 5:3:0. Two angles: some activities are still male or female dominated, and whoever works outside the home has less leisure time.'),
     anyN('r-2', 'age', 5, 1, 5, semis(h_ag, 'age')[:CAP],
          'One point, 5 marks, graded 5:3:0 — the richest of the three lists. The scheme walks the life cycle: young people have time but little money, parents of small children have neither, retired couples have both, older people have time but physical limits.'),
     anyN('r-3', 'cultural influences', 5, 1, 5, semis(h_cu, 'cultural influences')[:CAP],
          'One point, 5 marks, graded 5:3:0. Culture here means place and tradition — surfing or hurling tied to a particular county, Irish music tied to the country, and children copying their parents\' activities.')],
    'Fixed: three named influences, priced identically. Skipping one costs a straight 5.',
    stem='Leisure time is time that a person is free from work or other duties.',
    tariff_kind='fixed'))

ch = block(E3b, '3 benefits @ 5 marks (graded 5:3:0)')
cards.append(C(
    PFX+'q3bii', Y, LV, 'home-economics-3-11', 'benefits-of-leisure-activities',
    '2024 OL Section C E3 Q3(b)(ii)',
    'Evaluate the benefits of participating in leisure activities for family members.',
    '3 benefits @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Benefits of participating in leisure activities', 15, 3, 5,
          semis(ch, '3 benefits @ 5 marks (graded 5:3:0)')[:CAP],
          'Three benefits at 5 marks, graded 5:3:0. The scheme covers physical, mental, social and family benefits — taking one from different areas reads as three genuine benefits rather than one restated. Say who benefits and how.')],
    'One flat list, taken in order to the cap.',
    stem='Leisure time is time that a person is free from work or other duties.'))

E3c = block(E3, 'or 3.(c) Social and economic changes')
ch = block(E3c, 'improvements in the provision of education pre-schools', '(ii) Describe how second-level')
h_ed, h_pr, h_wk = heads(ch, ['improvements in the provision of education pre-schools',
                              'parenting roles within the family parents are role models',
                              'improved conditions at work shorter working'])
cards.append(C(
    PFX+'q3ci', Y, LV, 'home-economics-2-0', 'social-and-economic-changes-and-family-life',
    '2024 OL Section C E3 Q3(c)(i)',
    'Evaluate the impact of the following on family life: improvements in the provision of education; parenting roles within the family; improved conditions at work.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'improvements in the provision of education', 5, 1, 5,
          semis(h_ed, 'improvements in the provision of education')[:CAP],
          'One point, 5 marks, graded 5:3:0. The named schemes are the marks — SUSI, HEAR, DARE, VTOS, PLC and SOLAS courses. Say what each opened up for families who could not afford it before.'),
     anyN('r-2', 'parenting roles within the family', 5, 1, 5,
          semis(h_pr, 'parenting roles within the family')[:CAP],
          'One point, 5 marks, graded 5:3:0 — the longest list. The change is the point: both parents working, fathers at home, women as breadwinners, an egalitarian split of childcare, and the role conflict and overload that came with it.'),
     anyN('r-3', 'improved conditions at work', 5, 1, 5,
          semis(h_wk, 'improved conditions at work')[:CAP],
          'One point, 5 marks, graded 5:3:0. Shorter hours, better pay, more disposable income, safer workplaces — and the scheme explicitly credits the knock-on that happier workers make for better family life.')],
    'Fixed: three named changes, priced identically.',
    stem='Social and economic changes have impacted on family life in Ireland today.',
    tariff_kind='fixed'))

ch = block(E3c, '3 points @ 5 marks (graded 5:3:0) literacy skills')
cards.append(C(
    PFX+'q3cii', Y, LV, 'home-economics-2-2', 'second-level-education-and-the-workplace',
    '2024 OL Section C E3 Q3(c)(ii)',
    'Describe how second-level education prepares students for participation in the workplace.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'How second-level education prepares students for the workplace', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three points at 5 marks, graded 5:3:0. The list splits into skills (literacy, numeracy, computer) and qualities (punctuality, responsibility, respect for authority, self-discipline). Take from both, and say how school builds each one.')],
    'One flat list, taken in order to the cap.',
    stem='Social and economic changes have impacted on family life in Ireland today.'))

# ------------------------------------------------------- Question 4 (Core)
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) ‘Your body needs lots', 'and 4.(b)')
ch = block(Q4a, 'nutritive value HBV protein', '(ii) Describe one heat treatment')
h_n, h_d = heads(ch, ['nutritive value HBV protein', 'dietetic value HBV protein'])
o_n, o_d = semis(h_n, 'nutritive value'), semis(h_d, 'dietetic value')
cards.append(C(
    PFX+'q4ai', Y, LV, 'home-economics-0-9', 'nutritive-and-dietetic-value-of-milk',
    '2024 OL Section C Q4(a)(i) - Core',
    'Give an account of the nutritive value and the dietetic value of milk.',
    '4 points @ 5 marks (graded 5:4:3:2:0)', 20,
    [anyN('r-1', 'Nutritive value', 5, 1, 5, o_n[:CAP],
          'One point, 5 marks, on a 5:4:3:2:0 ladder — partial credit is real, so write what you know. Nutritive value is which nutrients are present and how much: HBV protein, saturated fat, lactose, calcium, 87% water. The two deficiencies, vitamin C and iron, are marking points too.'),
     anyN('r-2', 'Dietetic value', 5, 1, 5, o_d[:CAP],
          'One point, 5 marks, 5:4:3:2:0. Dietetic value is who it suits and why — easy to digest, inexpensive, versatile in sweet and savoury dishes, important for children, adolescents, pregnant women and older people. This is the half students merge into the first and lose.'),
     anyN('r-3', 'Two further points, from either heading', 10, 2, 5, (o_n + o_d)[:CAP],
          'The scheme reads "1 reference to nutritive value, 1 reference to dietetic value, & 2 other points", so half the marks float.')],
    'Fixed: one point pinned to each named value and two floating. Nutritive is what is in it; dietetic is who it suits.',
    stem='‘Your body needs lots of different nutrients to stay healthy.’ (www.safefood.net)',
    tariff_kind='fixed'))

# (slug, display name, block anchor, prefix to strip off the first step)
PROC = [('pasteurisation', 'Pasteurisation', 'pasteurisation milk heated to 72', 'pasteurisation'),
        ('sterilisation', 'Sterilisation', 'sterilisation milk homogenised', 'sterilisation'),
        ('uht', 'Ultra-heat treatment (UHT)', 'ultra-heat treatment (UHT) milk heated',
         'ultra-heat treatment (UHT)'),
        ('condensed', 'Condensed milk', 'condensed milk milk homogenised', 'condensed milk'),
        ('evaporated', 'Evaporated milk', 'evaporated milk milk homogenised', 'evaporated milk')]
pb = heads(block(Q4a, 'pasteurisation milk heated to 72', 'labelling type of milk'), [a for _, _, a, _ in PROC])
o_names = ['pasteurisation', 'sterilisation', 'ultra-heat treatment (UHT)', 'condensed milk',
           'evaporated milk'] + semis(
    block(Q4a, 'Accept Spray Drying', '(iii) Outline three different ways'), 'Accept')
o_lab = semis(block(Q4a, 'labelling type of milk', 'Accept Spray Drying'), 'labelling')
for i, (slug, name, anchor, pfx) in enumerate(PROC):
    cards.append(C(
        PFX+'q4aii-'+slug, Y, LV, 'home-economics-0-9', f'milk-heat-treatment-{slug}',
        f'2024 OL Section C Q4(a)(ii) - Core - {name}',
        'Describe one heat treatment used by manufacturers to extend the shelf life of milk. Refer to: name of process; how the process is carried out; labelling.',
        'Name 1 @ 2 marks (graded 2:1:0); process 4 points @ 3 marks (graded 3:2:0); labelling 2 points @ 2 marks (graded 2:1:0)', 18,
        [anyN('r-1', 'Name of process', 2, 1, 2, o_names[:CAP],
              f'Name one, 2 marks, graded 2:1:0 — only 2 of the 18 marks. This card follows {name.lower()}; the scheme prints a parallel process for each of the others, marked the same way.'),
         anyN('r-2', f'How {name.lower()} is carried out', 12, 4, 3, semis(pb[i], pfx)[:CAP],
              'Four points at 3 marks, graded 3:2:0 — twelve of the eighteen marks. The temperature and the time are separate marking points, so quote both figures exactly; then the cooling and the packaging give you the other two.'),
         anyN('r-3', 'Labelling', 4, 2, 2, o_lab[:CAP],
              'Two points at 2 marks, graded 2:1:0. Short items straight off the carton — type of milk, brand, quantity, nutritional information, date stamp, storage instructions.')],
        'One of five parallel processes the scheme prints under Q4(a)(ii). A candidate describes a single heat treatment, so each is its own card with its own questionRef rather than pooling five sets of steps into one menu. The name and labelling rows are common to all five.',
        stem='‘Your body needs lots of different nutrients to stay healthy.’ (www.safefood.net)',
        tariff_kind='fixed'))

DAIRY = ['Milk, milk with cereal', 'Cheese, grilled cheese', 'Yoghurt, instead of milk', 'Cream, garnish for soups']
ch = block(Q4a, '3 ways @ 4 marks (graded 4:2:0)')
cards.append(C(
    PFX+'q4aiii', Y, LV, 'home-economics-0-10', 'including-dairy-foods-in-a-healthy-diet',
    '2024 OL Section C Q4(a)(iii) - Core',
    'Outline three different ways that dairy foods can be included as part of a healthy diet.',
    '3 ways @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Ways dairy foods can be included in a healthy diet', 12, 3, 4,
          [bundle(h, '', 5) for h in heads(ch, DAIRY)][:CAP],
          'Three ways at 4 marks, graded 4:2:0. The question says different, so take three different dairy foods rather than three uses of milk. Naming the food is 2 — the other 2 come from the dish you put it in.')],
    'One option per dairy food, each carrying that food\'s own uses, because the question asks for three different ways and the scheme groups its uses under four foods.',
    stem='‘Your body needs lots of different nutrients to stay healthy.’ (www.safefood.net)'))

Q4b = block(Q4, 'and 4.(b) ‘Choosing an electrical appliance', 'or 4.(c)')
ch = block(Q4b, '3 factors @ 5 marks (graded 5:3:0)', '(ii) Describe three guidelines')
cards.append(C(
    PFX+'q4bi', Y, LV, 'home-economics-1-3', 'choosing-a-kitchen-appliance',
    '2024 OL Section C Q4(b)(i) - Core',
    'Discuss three factors that should be considered when choosing a kitchen appliance.',
    '3 factors @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors to consider when choosing a kitchen appliance', 15, 3, 5,
          semis(ch, '3 factors @ 5 marks (graded 5:3:0)')[:CAP],
          'Three factors at 5 marks, graded 5:3:0 — no 4, so a factor named without a reason drops to 3. The list runs from the appliance itself (cost, energy rating, size, function, guarantee) to how you found out about it (consumer websites, leaflets, word of mouth), and both halves score.')],
    'One flat list, taken in order to the cap.',
    stem='‘Choosing an electrical appliance, less is usually best.’ (www.electricireland.com)'))

ch = block(Q4b, '3 guidelines @ 5 marks (graded 5:3:0)')
cards.append(C(
    PFX+'q4bii', Y, LV, 'home-economics-1-3', 'safe-use-of-electrical-kitchen-appliances',
    '2024 OL Section C Q4(b)(ii) - Core',
    'Describe three guidelines to follow for the safe use of electrical kitchen appliances.',
    '3 guidelines @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Guidelines for the safe use of electrical kitchen appliances', 15, 3, 5,
          semis(ch, '3 guidelines @ 5 marks (graded 5:3:0)')[:CAP],
          'Three guidelines at 5 marks, graded 5:3:0. Describe, so say what each one prevents — wet hands conduct electricity, a trailing flex over a hob can melt, an overloaded socket can catch fire. The danger is where the marks are.')],
    'One flat list, taken in order to the cap.',
    stem='‘Choosing an electrical appliance, less is usually best.’ (www.electricireland.com)'))

Q4c = block(Q4, '4.(c) ‘There was a total of 23,173 marriages')
ch = block(Q4c, '3 points @ 5 marks (graded 5:3:0) three months', '(ii) Discuss three responsibilities')
cards.append(C(
    PFX+'q4ci', Y, LV, 'home-economics-2-1', 'conditions-for-a-legally-valid-marriage',
    '2024 OL Section C Q4(c)(i) - Core',
    'Outline conditions necessary for a marriage to be legally valid in Ireland.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Conditions for a marriage to be legally valid in Ireland', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three conditions at 5 marks, graded 5:3:0. The two numbers are the reliable marks — three months\' notice to the registrar, and both parties over 18. Free to marry, not closely related, and two witnesses present are the other safe ones.')],
    'One flat list, taken in order to the cap.',
    stem='‘There was a total of 23,173 marriages celebrated in Ireland in 2022.’ (www.cso.ie)'))

ch = block(Q4c, '3 points @ 5 marks (graded 5:3:0) provide financial support')
cards.append(C(
    PFX+'q4cii', Y, LV, 'home-economics-2-1', 'responsibilities-within-a-marriage',
    '2024 OL Section C Q4(c)(ii) - Core',
    'Discuss three responsibilities of a couple within a marriage relationship.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Responsibilities of a couple within a marriage relationship', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Three responsibilities at 5 marks, graded 5:3:0 — the shortest list on the paper, so all five options are worth knowing. The legal duty to provide for the physical, emotional, social, moral and educational needs of the children is the one that develops most easily to a full 5.')],
    'One flat list, taken in order to the cap.',
    stem='‘There was a total of 23,173 marriages celebrated in Ireland in 2022.’ (www.cso.ie)'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2024ol_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
