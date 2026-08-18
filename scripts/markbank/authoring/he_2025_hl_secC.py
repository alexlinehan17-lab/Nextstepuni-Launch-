"""2025 Higher Level, Section C — electives 1/2/3 and Question 4 (Core).

Every option list is sliced out of the scheme markdown, never retyped.
"""
import os, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, point, card, emit

T = load(2025, 'higher')
SEC = tidy(T[35119:60366])   # tidy once: block() anchors must not straddle the PDF's line wraps
Y, LV, PFX = 2025, 'higher', 'he-2025-hl-sc-'
CAP = 14

def C(*a, **k):
    k.setdefault('section', 'C')
    return card(*a, **k)

def bundle(head_text, prefix, n=None):
    """A whole scheme heading as ONE option.

    The segments under a heading are adjacent in the scheme, so re-joining the
    first n of them with "; " still normalises to a contiguous scheme substring
    and clears the provenance gate. Used where the examiner prices one point per
    heading rather than one point per segment.
    """
    seg = semis(head_text, prefix)
    return '; '.join(seg[:n] if n else seg)


cards = []

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, '1.(a) The kitchen', 'Elective 2 –')

# 1(a)(i) — kitchen/dining design factors, 16 marks, 1 point per heading + 1 other
ch = block(E1, '1 point on each heading and 1 other point', '(ii) Outline the principles')
h_fam, h_erg, h_env = heads(ch, ['family size and circumstances',
                                 'ergonomics', 'environmental awareness'])
o_fam = semis(h_fam, 'family size and circumstances')
o_erg = semis(h_erg, 'ergonomics')
o_env = semis(h_env, 'environmental awareness')
cards.append(C(
    PFX + 'q1ai', Y, LV, 'home-economics-3-4', 'kitchen-dining-room-design-factors',
    '2025 HL Section C E1 Q1(a)(i)',
    'Discuss the factors that influence the design of a kitchen/dining room. Refer to: family size and circumstances; ergonomics; environmental awareness.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'family size and circumstances', 4, 1, 4, o_fam[:CAP],
          'One point from this heading, 4 marks, graded 4:2:0 — a bare mention is 2, a developed point is 4. The scheme requires a point on each of the three headings, so you cannot bank all four marks here.'),
     anyN('r-2', 'ergonomics', 4, 1, 4, o_erg[:CAP],
          'One point from this heading, 4 marks, graded 4:2:0. Ergonomics is about fitting the room to the body and the work done in it — the work triangle and correct worktop heights are the two most reliably creditable ideas.'),
     anyN('r-3', 'environmental awareness', 4, 1, 4, o_env[:CAP],
          'One point from this heading, 4 marks, graded 4:2:0. The scheme runs the whole product life cycle — materials, making, using, disposing — so the reuse/recycle/repurpose cluster is the easiest to develop to full marks.'),
     anyN('r-4', 'One further point, from any of the three headings', 4, 1, 4,
          (o_fam + o_erg + o_env)[:CAP],
          'The fourth point is free: the scheme reads "1 point on each heading and 1 other point", so after covering all three headings you add one more from whichever heading you know best. Graded 4:2:0 like the rest.')],
    'Fixed rather than best-of: the scheme pins one point to each of the three named headings and lets the fourth float, so the rows are not interchangeable. Ignoring a heading caps you at 12 no matter how much you write on the other two.',
    tariff_kind='fixed'))

# 1(a)(ii) — lighting principles, 16 marks
ch = block(E1, '4 points @ 4 marks (graded 4:2:0) incorporate natural light',
           '(iii) Explain the underlying principle')
o = semis(ch, '4 points @ 4 marks (graded 4:2:0)')
cards.append(C(
    PFX + 'q1aii', Y, LV, 'home-economics-3-5', 'lighting-system-planning-principles',
    '2025 HL Section C E1 Q1(a)(ii)',
    'Outline the principles that should be considered when planning a lighting system for a kitchen/dining room.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Principles of planning a lighting system', 16, 4, 4, o[:CAP],
          'Four points at 4 marks, graded 4:2:0 — naming a principle is 2, outlining it is 4, so four bare names score only 8. The three lighting types (task, general, accent) are three separate points, which is the quickest route to full marks.')],
    'One flat list, taken in order to the cap.'))

# 1(a)(iii) — ventilation principle + effects of inadequate ventilation, 18 marks
ch = block(E1, '3 points re underlying principle of ventilation', 'and 1.(b) Good housing')
p1 = block(ch, '3 points re underlying principle', '3 effects of inadequate ventilation')
p2 = block(ch, '3 effects of inadequate ventilation')
o1 = semis(p1, '3 points re underlying principle of ventilation @ 3 marks (graded 3:2:0)')
o2 = semis(p2, '3 effects of inadequate ventilation @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX + 'q1aiii', Y, LV, 'home-economics-3-5', 'ventilation-principle-and-effects',
    '2025 HL Section C E1 Q1(a)(iii)',
    'Explain the underlying principle of ventilation and outline the effects of inadequate ventilation in a kitchen/dining room.',
    '3 points @ 3 marks (graded 3:2:0) x 2', 18,
    [anyN('r-1', 'Underlying principle of ventilation', 9, 3, 3, o1[:CAP],
          'Three points at 3 marks, graded 3:2:0. This half is pure physics and the scheme wants the chain, not the word: warm air expands and rises, leaves high up, and cold fresh air is drawn in lower down, creating a convection current. Writing "thermal expansion" alone is one point, not three.'),
     anyN('r-2', 'Effects of inadequate ventilation', 9, 3, 3, o2[:CAP],
          'Three points at 3 marks, graded 3:2:0. Condensation, mould and dampness are one causal chain but the scheme lists them separately, so each earns its own 3 marks. The two carbon build-ups are the safety points and are always safe to include.')],
    'Two equally weighted halves, so this is fixed with a row each. The question verb differs by half — explain for the principle, outline for the effects — and the principle half is where the marks are lost.',
    tariff_kind='fixed'))

# 1(b)(i) — housing requirements for two groups, 18 marks
E1b = block(E1, '1.(b) Good housing', 'or 1.(c)')
ch = block(E1b, '2 points on each and any 2 others', '(ii) Discuss social housing')
h_kids, h_dis = heads(ch, ['families with school going children', 'people with disabilities'])
o_kids = semis(h_kids, 'families with school going children')
o_dis = semis(h_dis, 'people with disabilities')
cards.append(C(
    PFX + 'q1bi', Y, LV, 'home-economics-3-3', 'housing-requirements-specific-groups',
    '2025 HL Section C E1 Q1(b)(i)',
    'Outline the housing requirements necessary to meet the needs of each of the following groups of people: families with school going children; people with disabilities.',
    '6 points @ 3 marks (graded 3:2:0)', 18,
    [anyN('r-1', 'Families with school going children', 6, 2, 3, o_kids[:CAP],
          'Two points at 3 marks, graded 3:2:0. Requirements only — do not drift into why the family needs them. Proximity to school, shops and transport is one point, not several, however many amenities you list.'),
     anyN('r-2', 'People with disabilities', 6, 2, 3, o_dis[:CAP],
          'Two points at 3 marks, graded 3:2:0. The strongest answers name a specific adaptation (ramp, wide doorway, lowered worktop, chairlift) rather than saying the house should be accessible.'),
     anyN('r-3', 'Two further points, from either group', 6, 2, 3, (o_kids + o_dis)[:CAP],
          'The scheme reads "2 points on each and any 2 others", so after two points per group you add two more from whichever group you know better. Same 3 marks and same 3:2:0 grading.')],
    'Fixed: two points are pinned to each named group and two float. Answering only one group caps you at 6 of 18. The floating pair is drawn from either list, so this row pools both.',
    tariff_kind='fixed'))

# 1(b)(ii) — social housing provision, 12 marks
ch = block(E1b, '3 points @ 4 marks (graded 4:2:0) local authorities')
o = semis(ch, '3 points @ 4 marks (graded 4:2:0)')
cards.append(C(
    PFX + 'q1bii', Y, LV, 'home-economics-3-3', 'social-housing-provision-ireland',
    '2025 HL Section C E1 Q1(b)(ii)',
    'Discuss social housing provision in Ireland.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Social housing provision in Ireland', 12, 3, 4, o[:CAP],
          'Three points at 4 marks, graded 4:2:0 — discuss, so a named scheme on its own is 2 and 4 needs a sentence saying what it does. Naming HAP or RAS and explaining it is the most efficient way to reach 4.')],
    'One flat list, taken in order to the cap.'))

# 1(c)(i) — cold-water system, 15 marks
E1c = block(E1, 'or 1.(c)')
ch = block(E1c, '5 points @ 3 marks (graded 3:2:0) mains pipe', '(ii) Devise a set')
o = semis(ch, '5 points @ 3 marks (graded 3:2:0)')
o = [x for x in o if 'Accept a well labelled diagram' not in x]
cards.append(C(
    PFX + 'q1ci', Y, LV, 'home-economics-3-5', 'cold-water-system-in-the-home',
    '2025 HL Section C E1 Q1(c)(i)',
    'Describe the cold-water system in a house.',
    '5 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'The cold-water system in a house', 15, 5, 3, o[:CAP],
          'Five points at 3 marks, graded 3:2:0. Follow the water in order — mains, service pipe, stopcock, rising main, storage tank, distribution — and the five points write themselves. The scheme adds "Accept a well labelled diagram", so a labelled drawing earns these marks in place of prose.')],
    'One flat list, taken in order to the cap. The scheme\'s "Accept a well labelled diagram" line is carried in the row note rather than as an option, because it is a marking instruction and not a marking point.'))

# 1(c)(ii) — sustainable household water management, 15 marks
ch = block(E1c, '5 points @ 3 marks (graded 3:2:0) install a timer')
o = semis(ch, '5 points @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX + 'q1cii', Y, LV, 'home-economics-3-6', 'sustainable-household-water-management',
    '2025 HL Section C E1 Q1(c)(ii)',
    'Devise a set of different strategies to ensure that household water is managed in an energy efficient and sustainable way in the home.',
    '5 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'Strategies for energy efficient and sustainable water use', 15, 5, 3, o[:CAP],
          'Five points at 3 marks, graded 3:2:0. The question asks for different strategies, so five variations on "use less water" will not score five times — spread across heating the water, fixing losses, and reusing water.')],
    'One flat list, taken in order to the cap.'))


# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 –', 'Elective 3 –')
held = []

# 2(a)(i) and 2(a)(ii) both mark an image of two outfits that the markdown does
# not carry, so they are held rather than shipped blind.
E2a = block(E2, '2.(a) A blazer', 'and 2.(b) Performance tests')
ch = block(E2a, 'one reference to each outfit and one other', '(ii) Name one design principle')
h_des, h_com, h_aes = heads(ch, ['design contrasting colour scheme', 'comfort soft', 'aesthetic appeal appeals'])
held.append(dict(C(
    PFX + 'q2ai', Y, LV, 'home-economics-3-8', 'evaluating-outfit-design',
    '2025 HL Section C E2 Q2(a)(i)',
    'Evaluate the design of the outfits shown above. Refer to: design; comfort; aesthetic appeal.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'design', 5, 1, 5, semis(h_des, 'design')[:CAP], 'One point, 5 marks, graded 5:3:0.'),
     anyN('r-2', 'comfort', 5, 1, 5, semis(h_com, 'comfort')[:CAP], 'One point, 5 marks, graded 5:3:0.'),
     anyN('r-3', 'aesthetic appeal', 5, 1, 5, semis(h_aes, 'aesthetic appeal')[:CAP], 'One point, 5 marks, graded 5:3:0.')],
    'Fixed: one point pinned to each of the three named headings.',
    stem='A blazer is a wardrobe staple.', tariff_kind='fixed'),
    heldReason='Marks an image of two outfits printed on the paper. Every option in the scheme describes that image ("wide-leg jeans can make legs look shorter", "bag adds emphasis"), so the card is unanswerable without the figure and the markdown extraction does not carry it.'))

ch = block(E2a, 'How it is demonstrated in either outfit 2 points @ 3 marks (graded 3:2:0)')
h_bal, h_emp, h_pro, h_rhy = heads(ch, ['Balance colours', 'Emphasis different', 'Proportion blazer', 'Rhythm colour'])
held.append(dict(C(
    PFX + 'q2aii', Y, LV, 'home-economics-3-8', 'design-principles-demonstrated',
    '2025 HL Section C E2 Q2(a)(ii)',
    'Name one design principle and explain how it is demonstrated in either outfit above.',
    'Name 1 @ 4 marks (graded 4:0); demonstration 2 points @ 3 marks (graded 3:2:0)', 10,
    [anyN('r-1', 'Name of design principle', 4, 1, 4, ['Balance', 'Emphasis', 'Proportion', 'Rhythm'],
          'Name one principle, 4 marks, graded 4:0 — all-or-nothing.'),
     anyN('r-2', 'How it is demonstrated in either outfit', 6, 2, 3,
          (semis(h_bal, 'Balance') + semis(h_emp, 'Emphasis'))[:CAP],
          'Two points at 3 marks, graded 3:2:0, tied to the principle you named.')],
    'Fixed: the name is priced separately from the two demonstration points.',
    stem='A blazer is a wardrobe staple.', tariff_kind='fixed'),
    heldReason='The demonstration half can only be marked against the outfits printed on the paper, and the scheme prints a separate demonstration list for each of the four principles — a single card can show only one pair of them. Needs the figure and a per-principle card split.'))

# 2(b)(i) — performance tests, 15 marks
E2b = block(E2, 'and 2.(b) Performance tests', 'or 2.(c)')
TESTS = ['abrasion resistance test', 'insulating properties test', 'stretch and elasticity test',
         'crease resistance test', 'washability test', 'colourfast test', 'absorbency test',
         'pilling and snagging test', 'tearing resistance test', 'resistance to water test',
         'flame resistance test']
tblocks = heads(block(E2b, 'abrasion resistance test'), TESTS)
cards.append(C(
    PFX + 'q2bi', Y, LV, 'home-economics-3-7', 'fabric-performance-tests',
    '2025 HL Section C E2 Q2(b)(i)',
    'Name two performance tests that can be carried out on fabrics and explain the procedure involved in conducting one of the tests you have identified.',
    '2 tests named @ 3 marks (graded 3:2:0); procedure 3 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'Performance tests that can be carried out on fabrics', 6, 2, 3, TESTS[:CAP],
          'Two tests named, 3 marks each, graded 3:2:0. Naming is cheap marks — the scheme accepts eleven different tests, so this half should never be lost. Name the two you can actually describe, because the second half is tied to one of them.'),
     anyN('r-2', 'Procedure — abrasion resistance test', 9, 3, 3, semis(tblocks[0], 'abrasion resistance test')[:CAP],
          'Three points at 3 marks, graded 3:2:0, describing the procedure for ONE of the tests you named. The steps shown here are the scheme\'s own for the abrasion resistance test, the first of the eleven it lists; the scheme prints an equivalent step list for each of the other ten, so if you named a different test the same three-at-3-marks structure applies to its steps. Every list is written as equipment, action, then how the result is judged — that ordering is the easiest way to reach three distinct points.')],
    'Fixed: naming and describing are priced separately. The procedure row carries one test\'s steps because the scheme prints eleven parallel step lists and a card may show at most 14 options — the row note says which test is shown and that the others are marked the same way.',
    stem='Performance tests measure a fabric’s unique set of characteristics.', tariff_kind='fixed'))

# 2(c)(i) — factors influencing fashion trends, 9 marks
E2c = block(E2, 'or 2.(c)')
ch = block(E2c, '3 influences @ 3 marks (graded 3:2:0)', '(ii) Give examples')
o = semis(ch, '3 influences @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX + 'q2ci', Y, LV, 'home-economics-3-8', 'factors-influencing-fashion-trends',
    '2025 HL Section C E2 Q2(c)(i)',
    'Outline three factors that influence current fashion trends.',
    '3 influences @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Factors that influence current fashion trends', 9, 3, 3, o[:CAP],
          'Three influences at 3 marks, graded 3:2:0 — naming is 2, outlining is 3, so the extra mark costs one sentence. Public figures, celebrities and influencers are three separate options in the scheme, so all three can come from the same cluster.')],
    'One flat list, taken in order to the cap.'))

# 2(c)(ii) — restyling a garment, 6 marks
ch = block(E2c, '2 points @ 3 marks (graded 3:2:0) addition of belts')
o = semis(ch, '2 points @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX + 'q2cii', Y, LV, 'home-economics-3-8', 'restyling-a-garment',
    '2025 HL Section C E2 Q2(c)(ii)',
    'Give examples of how a garment can be restyled to reflect a current trend.',
    '2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Ways a garment can be restyled', 6, 2, 3, o[:CAP],
          'Only two points at 3 marks — a six-mark part, so do not over-write it. The question says examples, so name the change and the garment it is made to.')],
    'One flat list, taken in order to the cap.'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 –', 'Question 4 – Core')
E3a = block(E3, '3.(a) Work is recognised', 'and 3.(b) Lifelong learning')

# 3(a)(i) — impact on work in Ireland, 20 marks
ch = block(E3a, 'and 1 other increased educational requirements', '(ii) Analyse how intrinsic')
h_edu, h_flex = heads(ch, ['increased educational requirements', 'increased flexibility in working hours'])
o_edu = semis(h_edu, 'increased educational requirements')
o_flex = semis(h_flex, 'increased flexibility in working hours')
cards.append(C(
    PFX + 'q3ai', Y, LV, 'home-economics-2-2', 'education-and-flexible-hours-impact-on-work',
    '2025 HL Section C E3 Q3(a)(i)',
    'Discuss how increased educational requirements and flexibility in working hours have impacted work in Ireland.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'increased educational requirements', 8, 2, 4, o_edu[:CAP],
          'Two points at 4 marks, graded 4:2:0. Discuss means the impact, not the fact — "third level qualifications needed for many jobs" is 2, adding what that has done to early school leavers takes it to 4.'),
     anyN('r-2', 'increased flexibility in working hours', 8, 2, 4, o_flex[:CAP],
          'Two points at 4 marks, graded 4:2:0. The named arrangements (flexi time, job sharing, remote working) are the 2-mark half; the 4-mark half says who it lets work who otherwise could not.'),
     anyN('r-3', 'One further point, from either heading', 4, 1, 4, (o_edu + o_flex)[:CAP],
          'The scheme reads "2 points to refer to increased educational requirements, 2 points to refer to flexibility in working hours and 1 other", so the fifth point comes from whichever heading you know better.')],
    'Fixed: two points are pinned to each named strand and the fifth floats. Writing only about education caps you at 12 of 20.',
    stem='Work is recognised as an important part of people’s lives.', tariff_kind='fixed'))

# 3(a)(ii) — intrinsic and extrinsic factors, 15 marks
ch = block(E3a, '1 point on each + 1 other point', '(iii) Name and evaluate')
h_in, h_ex = heads(ch, ['intrinsic work satisfaction', 'extrinsic work satisfaction'])
o_in = semis(h_in, 'intrinsic work satisfaction')
o_ex = semis(h_ex, 'extrinsic work satisfaction')
cards.append(C(
    PFX + 'q3aii', Y, LV, 'home-economics-2-2', 'intrinsic-and-extrinsic-attitudes-to-work',
    '2025 HL Section C E3 Q3(a)(ii)',
    'Analyse how intrinsic and extrinsic factors affect a person’s attitude to work.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'intrinsic work satisfaction', 5, 1, 5, o_in[:CAP],
          'One point, 5 marks, graded 5:3:0 — there is no 4, so a half-developed point drops straight to 3. Intrinsic means the satisfaction comes from the work itself, not from what the work pays.'),
     anyN('r-2', 'extrinsic work satisfaction', 5, 1, 5, o_ex[:CAP],
          'One point, 5 marks, graded 5:3:0. Extrinsic means the reward sits outside the job — pay, car, bonus, health insurance — and the scheme links that to lower self-esteem and less pride in the work.'),
     anyN('r-3', 'One further point, from either heading', 5, 1, 5, (o_in + o_ex)[:CAP],
          'The scheme reads "1 point on each + 1 other point", so the third point comes from whichever of the two you can develop furthest. Same 5:3:0 grading.')],
    'Fixed: one point pinned to each named factor and one floating. The two lists are deliberate mirror images — self-esteem, pride and positive feelings appear in both, in opposite directions.',
    stem='Work is recognised as an important part of people’s lives.', tariff_kind='fixed'))

# 3(a)(iii) — childcare option, 15 marks
ch = block(E3a, 'name of childcare option @ 3 marks (graded 3:0)')
o_name = semis(block(ch, 'name of childcare option', 'evaluation of childcare option'),
               'name of childcare option @ 3 marks (graded 3:0)')
o_eval = semis(block(ch, 'evaluation of childcare option'),
               'evaluation of childcare option 4 points @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX + 'q3aiii', Y, LV, 'home-economics-3-11', 'evaluating-a-childcare-option',
    '2025 HL Section C E3 Q3(a)(iii)',
    'Name and evaluate one childcare option available to working parents.',
    'Name 1 @ 3 marks (graded 3:0); evaluation 4 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'Childcare options available to working parents', 3, 1, 3, o_name[:CAP],
          'Name one option, 3 marks, graded 3:0 — all-or-nothing, and naming a second adds nothing. Pick the one you can evaluate on four separate criteria, because the other 12 marks all hang off it.'),
     anyN('r-2', 'Evaluation of the named childcare option', 12, 4, 3, o_eval[:CAP],
          'Four points at 3 marks, graded 3:2:0. Evaluate, so each criterion needs a judgement about the option you named, not a definition of the criterion. Staff qualifications and staff-to-child ratio are separate points in the scheme.')],
    'Fixed: the name is priced separately from the four evaluation points. Twelve of the fifteen marks are in the evaluation, so the choice of option matters less than having four criteria ready.',
    stem='Work is recognised as an important part of people’s lives.', tariff_kind='fixed'))

# 3(b)(i) — reasons adults return to education, 18 marks
E3b = block(E3, 'and 3.(b) Lifelong learning', 'or 3.(c)')
ch = block(E3b, '3 points @ 6 marks (graded 6:4:2:0)', '(ii) Describe how improvements')
o = semis(ch, '3 points @ 6 marks (graded 6:4:2:0)')
cards.append(C(
    PFX + 'q3bi', Y, LV, 'home-economics-3-10', 'reasons-adults-return-to-education',
    '2025 HL Section C E3 Q3(b)(i)',
    'Analyse the reasons why adults return to education.',
    '3 points @ 6 marks (graded 6:4:2:0)', 18,
    [anyN('r-1', 'Reasons why adults return to education', 18, 3, 6, o[:CAP],
          'Three points at 6 marks, graded 6:4:2:0 — the widest ladder on the paper. A bare reason is 2; 6 needs the reason, who it applies to, and what it changes for them. Three reasons written to full depth beat six written flat.')],
    'One flat list, taken in order to the cap.',
    stem='Lifelong learning benefits both the individual and the family.'))

# 3(b)(ii) — education provision and family life, 12 marks
ch = block(E3b, '3 points @ 4 marks (graded 4:2:0) increased resources')
o = semis(ch, '3 points @ 4 marks (graded 4:2:0)')
cards.append(C(
    PFX + 'q3bii', Y, LV, 'home-economics-3-10', 'education-provision-impact-on-family-life',
    '2025 HL Section C E3 Q3(b)(ii)',
    'Describe how improvements in the provision of education have impacted on family life.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'How improvements in education provision have impacted family life', 12, 3, 4, o[:CAP],
          'Three points at 4 marks, graded 4:2:0. Every option in this list is written as improvement then consequence for the family, joined by a dash — copy that shape and the 4 marks follow. The named schemes at the end (HEAR, DARE, SUSI, Youthreach, VTOS) score only if you say what they do for the family.')],
    'One flat list, taken in order to the cap.',
    stem='Lifelong learning benefits both the individual and the family.'))

# 3(c)(i) — causes of poverty, 18 marks
E3c = block(E3, 'or 3.(c)')
ch = block(E3c, 'cycle of poverty poverty exists', '(ii) Differentiate')
o = semis(ch, 'cycle of poverty')
cards.append(C(
    PFX + 'q3ci', Y, LV, 'home-economics-3-9', 'causes-of-poverty-and-the-cycle-of-poverty',
    '2025 HL Section C E3 Q3(c)(i)',
    'Discuss the causes of poverty. In your answer refer to the cycle of poverty.',
    '3 points @ 6 marks (graded 6:4:2:0)', 18,
    [anyN('r-1', 'Causes of poverty, including the cycle of poverty', 18, 3, 6, o[:CAP],
          'Three points at 6 marks, graded 6:4:2:0. The question names the cycle of poverty, so the first option is effectively compulsory — poverty persisting across generations through limited access to resources and opportunities. A bare cause is 2; 6 needs the cause and how it keeps a household poor.')],
    'One flat list, taken in order to the cap. The cycle-of-poverty statement heads the scheme’s list because the question asks for it by name.',
    stem='In 2023, 559,850 people were living in poverty in Ireland. Over 176,900 of those were children. (Social Justice Ireland, November 2024)'))

# 3(c)(ii) — absolute and relative poverty, 12 marks
ch = block(E3c, 'absolute poverty insufficient income')
h_abs, h_rel = heads(ch, ['absolute poverty insufficient income', 'relative poverty people living below'])
cards.append(C(
    PFX + 'q3cii', Y, LV, 'home-economics-3-9', 'absolute-and-relative-poverty',
    '2025 HL Section C E3 Q3(c)(ii)',
    'Differentiate between each of the following types of poverty: absolute poverty; relative poverty.',
    '2 points @ 3 marks (graded 3:2:0) x 2', 12,
    [anyN('r-1', 'absolute poverty', 6, 2, 3, semis(h_abs, 'absolute poverty')[:CAP],
          'Two points at 3 marks, graded 3:2:0. Absolute poverty is about physical survival — not enough income for food, shelter or clothing. Homelessness is the scheme’s worked example.'),
     anyN('r-2', 'relative poverty', 6, 2, 3, semis(h_rel, 'relative poverty')[:CAP],
          'Two points at 3 marks, graded 3:2:0. Relative poverty is measured against the society you live in, and the scheme gives the hard number: income below 60% of the median household income. Quote it.')],
    'Fixed, two equal halves. Differentiate, so the marks come from the contrast: absolute is survival, relative is exclusion from the normal standard of living.',
    tariff_kind='fixed'))

# ------------------------------------------------------- Question 4 (Core)
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) Consumers in Ireland', 'and 4.(b) If you are buying')

# 4(a)(i) — nutritional significance of meat, 20 marks
ch = block(Q4a, '5 points @ 4 marks (4:3:2:1:0)', '(ii) Outline two causes')
NUTR = ['protein 20-30%', 'fat 10-30%', 'carbohydrates 0%', 'vitamins good source',
        'minerals good source', 'water 50-60%']
hb = heads(ch, NUTR)
o = [bundle(h, '', 4) for h in hb]
cards.append(C(
    PFX + 'q4ai', Y, LV, 'home-economics-0-9', 'nutritional-significance-of-meat',
    '2025 HL Section C Q4(a)(i) - Core',
    'Discuss the nutritional significance of meat in the diet.',
    '5 points @ 4 marks (4:3:2:1:0)', 20,
    [anyN('r-1', 'Nutritional significance of meat', 20, 5, 4, o[:CAP],
          'Five points at 4 marks on a 4:3:2:1:0 ladder — the finest grading on the paper, so partial credit is real and a thin point still scores. The scheme groups its marking points under six nutrients and you need five, so take one nutrient per point: give the percentage present and what it does in the body. Carbohydrate at 0% still scores, because saying meat supplies none and should be served with a starchy food is the scheme’s own point.')],
    'One option per nutrient heading rather than one per fragment: the scheme prints six nutrient blocks and prices five points, so a student picks nutrients, not sentences. Each option is that heading’s own opening run of marking points, kept contiguous.'))

# 4(a)(ii) — toughness and tenderising, 18 marks
ch = block(Q4a, '2 outlined causes of toughness', '(iii) Describe how the Bord Bia')
o_c = semis(block(ch, '2 outlined causes', '4 described methods'), '2 outlined causes of toughness @ 3 marks (graded 3:2:0)')
o_m = semis(block(ch, '4 described methods'), '4 described methods of tenderising meat @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX + 'q4aii', Y, LV, 'home-economics-0-9', 'meat-toughness-causes-and-tenderising',
    '2025 HL Section C Q4(a)(ii) - Core',
    'Outline two causes of toughness in meat. Describe four methods of tenderising meat.',
    '2 causes @ 3 marks (graded 3:2:0); 4 methods @ 3 marks (graded 3:2:0)', 18,
    [anyN('r-1', 'Causes of toughness in meat', 6, 2, 3, o_c[:CAP],
          'Two causes at 3 marks, graded 3:2:0. The scheme splits the carcass handling into three separate causes — not resting before slaughter, wrong hanging time, wrong hanging conditions — so two of the six can come from that one area.'),
     anyN('r-2', 'Methods of tenderising meat', 12, 4, 3, o_m[:CAP],
          'Four methods at 3 marks, graded 3:2:0. Describe, so name the method and say what it does to the fibres or connective tissue. Twelve of the eighteen marks sit here, so do not spend the time on the causes half.')],
    'Fixed: the question sets two counts and the scheme prices them separately. The tenderising half is worth twice the toughness half.',
    stem='Consumers in Ireland have access to high quality meat and meat products at price points that suit their budgets.',
    tariff_kind='fixed'))

# 4(a)(iii) — Bord Bia Quality Assurance, 12 marks
ch = block(Q4a, '3 points @ 4 marks (graded 4:2:0) informs the consumer')
o = semis(ch, '3 points @ 4 marks (graded 4:2:0)')
cards.append(C(
    PFX + 'q4aiii', Y, LV, 'home-economics-0-11', 'bord-bia-quality-assurance-scheme',
    '2025 HL Section C Q4(a)(iii) - Core',
    'Describe how the Bord Bia Quality Assurance Scheme ensures meat quality and safety.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'How the Bord Bia Quality Assurance Scheme ensures meat quality and safety', 12, 3, 4, o[:CAP],
          'Three points at 4 marks, graded 4:2:0. The scheme rewards the mechanism, not the logo — traceable veterinary treatments, regulated feedstuffs, kept records, farm and plant inspections. Saying the mark reassures the consumer is one point only.')],
    'One flat list, taken in order to the cap.',
    stem='Consumers in Ireland have access to high quality meat and meat products at price points that suit their budgets.'))

# 4(b)(i) — mortgage approval conditions, 16 marks
Q4b = block(Q4, 'and 4.(b) If you are buying', 'or 4.(c)')
# Anchors long enough to be unique: a bare 'age' matches inside 'mortgage'.
COND = ['borrowing limit', 'deposit 10%', 'good financial record/credit history',
        'savings: steady', 'employment must be secure', 'proof of income',
        'term of loan repaid over', 'age applicant must be over 18',
        'proof of identity', 'proof of address', 'property must be in good condition',
        'mortgage protection policy must be in place', 'house insurance must be in place',
        'house buyer must have an Irish bank account']
ch = block(Q4b, '4 points @ 4 marks (graded 4:2:0) borrowing limit', '(ii) Name and describe')
o = [bundle(h, '', 3) for h in heads(ch, COND)]
cards.append(C(
    PFX + 'q4bi', Y, LV, 'home-economics-1-1', 'mortgage-approval-conditions',
    '2025 HL Section C Q4(b)(i) - Core',
    'Outline the conditions that must be met in order to qualify for mortgage approval.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Conditions that must be met to qualify for mortgage approval', 16, 4, 4, o[:CAP],
          'Four conditions at 4 marks, graded 4:2:0 — naming the condition is 2, and the figure attached to it is what earns the other 2. The numbers are the marks here: 3.5 times gross income (4 for first-time buyers), 10% deposit, 90% ceiling on a first-time buyer’s home, a 20-40 year term. Learn those four and the part is done.')],
    'One option per condition heading: the scheme prints fourteen named conditions, each with its own detail, and prices four points — so a student picks conditions, not fragments. Exactly at the fourteen-option ceiling.',
    stem='If you are buying a home, you will probably have to take out a mortgage. (www.citizensinformation.ie)'))

# 4(b)(ii) — type of mortgage, 14 marks
MORT = ['Annuity/Repayment mortgage:', 'Endowment:', 'Pension linked:', 'Local authority mortgage/Home Choice Loan:']
ch = block(Q4b, 'Name: 1 @ 2 marks (graded 2:1:0)')
mb = heads(block(ch, 'Annuity/Repayment mortgage:'), MORT)
o_name = ['Annuity/Repayment mortgage', 'Endowment', 'Pension linked',
          'Local authority mortgage/Home Choice Loan'] + \
         semis(block(ch, 'Tracker; current account/offset mortgage'), '')
cards.append(C(
    PFX + 'q4bii', Y, LV, 'home-economics-1-1', 'types-of-mortgage-named-and-described',
    '2025 HL Section C Q4(b)(ii) - Core',
    'Name and describe one type of mortgage available to house purchasers.',
    'Name 1 @ 2 marks (graded 2:1:0); description 3 points @ 4 marks (graded 4:2:0)', 14,
    [anyN('r-1', 'Types of mortgage available to house purchasers', 2, 1, 2, o_name[:CAP],
          'Name one, 2 marks, graded 2:1:0. Only 2 of the 14 marks — name the one you can describe in three separate points, because the other 12 all depend on it.'),
     anyN('r-2', 'Description — Annuity/Repayment mortgage', 12, 3, 4, semis(mb[0], 'Annuity/Repayment mortgage:')[:CAP],
          'Three points at 4 marks, graded 4:2:0 — twelve of the fourteen marks. The steps shown are the scheme’s own for the annuity/repayment mortgage, the first of the four it describes in full; it prints an equivalent description for the endowment, pension-linked and local authority mortgages, marked the same way. For any of them the three points are: how the repayment splits, what happens to the debt over time, and what protection policy is required.')],
    'Fixed: naming is priced at 2 and describing at 12. The description row carries one type’s detail because the scheme prints four parallel descriptions; the row note says which is shown and that the others are marked identically.',
    stem='If you are buying a home, you will probably have to take out a mortgage. (www.citizensinformation.ie)',
    tariff_kind='fixed'))

# 4(c)(i) — meal planning for an older person, 15 marks
Q4c = block(Q4, 'or 4.(c)')
ch = block(Q4c, '3 points @ 5 marks (graded 5:3:0) ensure meals', '(ii) Evaluate steaming')
o = semis(ch, '3 points @ 5 marks (graded 5:3:0)')
cards.append(C(
    PFX + 'q4ci', Y, LV, 'home-economics-0-10', 'meal-planning-guidelines-older-person',
    '2025 HL Section C Q4(c)(i) - Core',
    'Outline three meal planning guidelines that an older person should follow to maximise nutritional intake.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Meal planning guidelines for an older person', 15, 3, 5, o[:CAP],
          'Three guidelines at 5 marks, graded 5:3:0 — no 4, so a guideline without a reason drops to 3. The scheme writes its own options as guideline, nutrient, then why that nutrient matters at this age: fruit and veg for vitamin C for the immune system, calcium for bone health, iron to prevent anaemia. Copy that three-part shape.')],
    'One flat list, taken in order to the cap.',
    stem='As people get older, they may cook less for themselves and may be more at risk of nutritional deficiencies.'))

# 4(c)(ii) — evaluating steaming, 15 marks
ch = block(Q4c, '• ease of use 2 points @ 3 marks')
h_ease, h_nut, h_pal = heads(ch, ['ease of use', 'effect on nutritive value of food',
                                  'palatability of food cooked by this method'])
cards.append(C(
    PFX + 'q4cii', Y, LV, 'home-economics-0-3', 'evaluating-steaming-for-an-older-person',
    '2025 HL Section C Q4(c)(ii) - Core',
    'Evaluate steaming as a method of cooking for an older person. Refer to: ease of use; effect on nutritive value of food; palatability of food cooked by this method.',
    '2 points @ 3 marks; 1 @ 3 marks; 2 points @ 3 marks (graded 3:2:0)', 15,
    [anyN('r-1', 'ease of use', 6, 2, 3, semis(h_ease, 'ease of use 2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Two points at 3 marks, graded 3:2:0. Tie each to the older person: little attention needed, hard to overcook, one unit cooks the whole meal, and it suits single portions.'),
     anyN('r-2', 'effect on nutritive value of food', 3, 1, 3, semis(h_nut, 'effect on nutritive value of food 1 @ 3 marks (graded 3:2:0)')[:CAP],
          'Only ONE point here, 3 marks — the smallest row on the question, so do not write a paragraph. Name the nutrient that survives: little loss of B group vitamins or vitamin C, and no added fat.'),
     anyN('r-3', 'palatability of food cooked by this method', 6, 2, 3, semis(h_pal, 'palatability of food cooked by this method 2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Two points at 3 marks, graded 3:2:0. Evaluate means both directions are creditable — food stays moist and keeps its colour, but steamed food can lack flavour and go soft if overcooked. A negative point scores as well as a positive one.')],
    'Fixed: the question prints three headings and the scheme prices them unequally — 2 points, then 1, then 2. The middle heading is worth half the others, which is the easiest place to waste time.',
    stem='As people get older, they may cook less for themselves and may be more at risk of nutritional deficiencies.',
    tariff_kind='fixed'))

emit(cards)
import json as _j, sys as _s
_j.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2025hl_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=_s.stderr)

