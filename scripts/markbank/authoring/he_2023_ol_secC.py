"""2023 Ordinary Level, Section C."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2023, 'ordinary')
SEC = tidy(T[22298:43193])
Y, LV, PFX, CAP = 2023, 'ordinary', 'he-2023-ol-sc-', 14
cards, held = [], []
def C(*a, **k):
    k.setdefault('section', 'C'); return card(*a, **k)
def bundle(h, prefix='', n=None):
    seg = semis(h, prefix); return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 –', 'Elective 2 –')
E1a = block(E1, '1.(a) A contemporary bathroom', 'and 1.(b)')
ch = block(E1a, '4 points @ 5 marks (graded 5:3:0) large space', '(ii) Discuss three factors')
held.append(dict(C(
    PFX+'q1ai', Y, LV, 'home-economics-3-4', 'evaluating-a-bathroom-design',
    '2023 OL Section C E1 Q1(a)(i)',
    'Evaluate the suitability of the bathroom space shown above for a couple with children.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Suitability of the bathroom space', 20, 4, 5,
          semis(ch, '4 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Four points at 5 marks, graded 5:3:0.')],
    'Held - see heldReason.',
    stem='A contemporary bathroom design is shown below.'),
    heldReason='Marks a bathroom photograph printed on the paper. Every option describes that image ("large walk-in shower", "roman blind for privacy", "shelves may be a hazard for small child"), so the card is unanswerable without the figure and the markdown extraction does not carry it.'))

HEAT = ['cost: installation', 'energy efficiency: is the source', 'convenience: automatic timer',
        'comfort: constant temperature', 'safety: priority for family', 'water heating: immersion',
        'aesthetic appeal: underfloor', 'impact on the environment: gas']
ch = block(E1a, 'cost: installation', '(iii) Describe three guidelines')
cards.append(C(
    PFX+'q1aii', Y, LV, 'home-economics-3-5', 'choosing-a-home-heating-system',
    '2023 OL Section C E1 Q1(a)(ii)',
    'Discuss three factors which should be considered when choosing a heating system for the home.',
    '3 factors @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Factors to consider when choosing a heating system', 15, 3, 5,
          [bundle(h, a.split(':')[0] + ':') for h, a in zip(heads(ch, HEAT), HEAT)][:CAP],
          'Three factors at 5 marks, graded 5:3:0 - no 4, so a factor named without a reason drops to 3. The scheme prints eight factors, so take three genuinely different ones: cost, how it is controlled, and what it does to the environment.')],
    'One option per named factor, each carrying that factor\'s own detail, because the scheme groups its marking points under eight headings and prices three.',
    stem='A contemporary bathroom design is shown below.'))

ch = block(E1a, '3 guidelines @ 5 marks (graded 5:3:0) never mix electricity')
cards.append(C(
    PFX+'q1aiii', Y, LV, 'home-economics-1-3', 'safe-use-of-electricity-in-the-home',
    '2023 OL Section C E1 Q1(a)(iii)',
    'Describe three guidelines to follow for the safe use of electricity in the home.',
    '3 guidelines @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Guidelines for the safe use of electricity in the home', 15, 3, 5,
          semis(ch, '3 guidelines @ 5 marks (graded 5:3:0)')[:CAP],
          'Three guidelines at 5 marks, graded 5:3:0. Describe, so say what each one prevents - water conducts electricity, a flex across a hob can melt, an overloaded adaptor can catch fire. The danger is where the extra marks are.')],
    'One flat list, taken in order to the cap.'))

E1b = block(E1, 'and 1.(b) ‘A quarter of all energy', 'or 1.(c)')
ch = block(E1b, '3 strategies @ 5 marks (graded 5:3:0)', '(ii) Name one renewable energy source')
cards.append(C(
    PFX+'q1bi', Y, LV, 'home-economics-3-6', 'improving-home-energy-efficiency',
    '2023 OL Section C E1 Q1(b)(i)',
    'Describe three strategies that could be used to improve energy efficiency in the home.',
    '3 strategies @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Strategies to improve energy efficiency in the home', 15, 3, 5,
          semis(ch, '3 strategies @ 5 marks (graded 5:3:0)')[:CAP],
          'Three strategies at 5 marks, graded 5:3:0. Spread them - one on keeping heat in, one on heating water, one on appliances - so they cannot be read as the same strategy three times. Say how each saves the energy.')],
    'One flat list, taken in order to the cap.',
    stem='‘A quarter of all energy used in Ireland is consumed directly in homes.’ (www.seai.ie)'))

REN = ['solar saves up to', 'wood contributes to biomass', 'wind unlimited', 'hydropower very viable',
       'bio energy suitable for heating', 'geothermal cost effective']
rb = heads(block(E1b, 'solar saves up to'), REN)
cards.append(C(
    PFX+'q1bii', Y, LV, 'home-economics-3-6', 'renewable-energy-sources-and-advantages',
    '2023 OL Section C E1 Q1(b)(ii)',
    'Name one renewable energy source and outline the advantages of the energy source named.',
    'Name 5 marks (graded 5:3:0); 2 advantages @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Renewable energy sources', 5, 1, 5,
          ['solar', 'wood', 'wind', 'hydropower', 'bio energy', 'geothermal'],
          'Name one, 5 marks, graded 5:3:0. Six are accepted, but solar has by far the most detailed list of advantages in the scheme - name that one unless you know another well, because the other 10 marks depend on it.'),
     anyN('r-2', 'Advantages of the energy source named', 10, 2, 5,
          [x for h, a in zip(rb, REN) for x in semis(h, a.split()[0])][:CAP],
          'Two advantages at 5 marks, graded 5:3:0 - ten of the fifteen marks. The strongest answers pair a money advantage with an environmental one: solar saves up to 68% on heating bills and raises the BER, and it produces no carbon dioxide. Grants are a marking point in their own right.')],
    'Fixed: naming is priced at 5 and the advantages at 10. The advantages row pools all six sources, because the two points are awarded for whichever was named.',
    stem='‘A quarter of all energy used in Ireland is consumed directly in homes.’ (www.seai.ie)',
    tariff_kind='fixed'))

E1c = block(E1, 'or 1.(c) (i) Describe the function')
ch = block(E1c, 'stopcock: special valve', '(ii) Outline three guidelines')
h_sc, h_st, h_op = heads(ch, ['stopcock: special valve', 'storage tank: located', 'overflow pipe: attic storage'])
cards.append(C(
    PFX+'q1ci', Y, LV, 'home-economics-3-5', 'cold-water-supply-parts-ol',
    '2023 OL Section C E1 Q1(c)(i)',
    'Describe the function of the following parts of a cold-water supply to a house: stop cock; storage tank; overflow pipe.',
    '1 function @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'stop cock', 5, 1, 5, semis(h_sc, 'stopcock:')[:CAP],
          'One function, 5 marks, graded 5:3:0. Say where it is as well as what it does - on the service pipe outside or under the kitchen sink - and that it shuts the supply off if there is a problem.'),
     anyN('r-2', 'storage tank', 5, 1, 5, semis(h_st, 'storage tank:')[:CAP],
          'One function, 5 marks, graded 5:3:0. The height is the point: it sits in the attic so gravity gives the pressure to feed the toilet, shower and hot press below.'),
     anyN('r-3', 'overflow pipe', 5, 1, 5, semis(h_op, 'overflow pipe:')[:CAP],
          'One function, 5 marks, graded 5:3:0. It carries excess water outside, and the scheme wants the reason it is needed - if the ball valve fails, it stops the house flooding.')],
    'Fixed: three named parts, priced identically. All three are short and factual.',
    tariff_kind='fixed'))

WAT = ['toilet: install a dual flush', 'taps: repair leaking', 'appliances: fill kettle', 'water: use a shower']
ch = block(E1c, 'toilet: install a dual flush')
cards.append(C(
    PFX+'q1cii', Y, LV, 'home-economics-3-6', 'reducing-water-usage-in-the-home',
    '2023 OL Section C E1 Q1(c)(ii)',
    'Outline three guidelines to follow to reduce water usage in the home.',
    '3 guidelines @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Guidelines to reduce water usage in the home', 15, 3, 5,
          [bundle(h, a.split(':')[0] + ':') for h, a in zip(heads(ch, WAT), WAT)][:CAP],
          'Three guidelines at 5 marks, graded 5:3:0. The scheme groups its tips by where the water is used - toilet, taps, appliances, washing - so taking one from different groups gives three that are genuinely different. Say how much each saves or why it works.')],
    'One option per place water is used, each carrying that group\'s own tips, because three guidelines drawn from one group would read as one guideline restated.'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 –', 'Elective 3 –')
E2a = block(E2, '2.(a) ‘Music festivals', 'and 2.(b)')
ch = block(E2a, 'comfort: fabric allows', '(ii) Describe one method of applying')
h_c, h_f, h_a = heads(ch, ['comfort: fabric allows', 'function: waterproof boots', 'aesthetic appeal: relaxed'])
held.append(dict(C(
    PFX+'q2ai', Y, LV, 'home-economics-3-8', 'suitability-of-festival-fashion',
    '2023 OL Section C E2 Q2(a)(i)',
    'Comment on the suitability of the festival fashion shown above. Refer to: comfort; function; aesthetic appeal.',
    '2 points @ 3 marks (graded 3:2:0) x 3', 18,
    [anyN('r-1', 'comfort', 6, 2, 3, semis(h_c, 'comfort:')[:CAP], 'Two points at 3 marks, graded 3:2:0.'),
     anyN('r-2', 'function', 6, 2, 3, semis(h_f, 'function:')[:CAP], 'Two points at 3 marks, graded 3:2:0.'),
     anyN('r-3', 'aesthetic appeal', 6, 2, 3, semis(h_a, 'aesthetic appeal:')[:CAP], 'Two points at 3 marks, graded 3:2:0.')],
    'Fixed: three headings named in the question, priced equally.',
    stem='‘Music festivals bring new trends and a boost to the fashion industry.’ (www.guardian.com)',
    tariff_kind='fixed'),
    heldReason='Marks festival outfits printed on the paper. Every option describes that image ("easy to remove shirt, jackets, sweatshirt", "waterproof boots", "layered look"), so the card is unanswerable without the figure.'))

ch = block(E2a, '1 points @ 4 marks (graded 4:2:0), 1 points @ 3 marks (graded 3:2:0)')
o_meth = semis(ch, '1 points @ 4 marks (graded 4:2:0), 1 points @ 3 marks (graded 3:2:0)')
cards.append(C(
    PFX+'q2aii', Y, LV, 'home-economics-3-8', 'methods-of-applying-a-design-to-a-garment',
    '2023 OL Section C E2 Q2(a)(ii)',
    'Describe one method of applying a design to a garment.',
    '1 point @ 4 marks (graded 4:2:0); 1 point @ 3 marks (graded 3:2:0)', 7,
    [anyN('r-1', 'Methods of applying a design to a garment', 4, 1, 4, o_meth[:CAP],
          'First point, 4 marks, graded 4:2:0. Naming the method is 2 - the other 2 come from saying how it puts the design onto the cloth.'),
     anyN('r-2', 'A second point on the method described', 3, 1, 3, o_meth[:CAP],
          'Second point, 3 marks, graded 3:2:0. The scheme prints a single list of seven methods and prices two points off it, the first at 4 and the second at 3, so the second point continues the description of the same method rather than naming a new one.')],
    'Fixed: the scheme prints one list of methods and two point-values, 4 then 3, so both rows draw on that same list. Only seven marks in total - this is a short part, not a discussion.',
    stem='‘Music festivals bring new trends and a boost to the fashion industry.’ (www.guardian.com)',
    tariff_kind='fixed'))

E2b = block(E2, 'and 2.(b) Textiles can be treated', 'or 2.(c)')
ch = block(E2b, '2 reasons @ 3 marks (graded 3:2:0)', '(ii) Name and describe one fabric finish')
cards.append(C(
    PFX+'q2bi', Y, LV, 'home-economics-3-7', 'why-fabric-finishes-are-used-2023',
    '2023 OL Section C E2 Q2(b)(i)',
    'Explain why fabric finishes are used on fabric.',
    '2 reasons @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Why fabric finishes are used on fabric', 6, 2, 3,
          semis(ch, '2 reasons @ 3 marks (graded 3:2:0)')[:CAP],
          'Only two reasons at 3 marks - a six-mark part, so keep it short. Each reason is a problem the finish removes: creasing, shrinking, staining, catching fire.')],
    'One flat list, taken in order to the cap.',
    stem='Textiles can be treated with a variety of fabric finishes.'))

FIN = ['waterproofing:', 'anti-static:', 'stain resistant:', 'crease resistant:', 'mercerising:', 'flame retardant:']
fb = heads(block(E2b, 'waterproofing: makes fabric'), FIN)
descs, exs = [], []
for h, f in zip(fb, FIN):
    t = tidy(h)[len(f):].strip()
    left, right = t.split('e.g.', 1)
    descs.append(tidy(left).rstrip(' ,;'))
    exs.append('e.g.' + right.split(';')[0].rstrip(' ,.'))
cards.append(C(
    PFX+'q2bii', Y, LV, 'home-economics-3-7', 'fabric-finishes-2023-ol',
    '2023 OL Section C E2 Q2(b)(ii)',
    'Name and describe one fabric finish. Give an example of its use in clothing.',
    'Name 4 marks (graded 4:2:0); description 1 point @ 3 marks (graded 3:2:0); example 1 point @ 2 marks (graded 2:0)', 9,
    [anyN('r-1', 'Fabric finishes', 4, 1, 4, [f[:-1] for f in FIN][:CAP],
          'Name one, 4 marks, graded 4:2:0 - the biggest single row here, and six finishes are accepted. Pick the one whose effect and use you can state, because the other 5 marks follow from it.'),
     anyN('r-2', 'What the finish does', 3, 1, 3, descs[:CAP],
          'One description, 3 marks, graded 3:2:0, matching the finish you named. Each of the scheme\'s descriptions is a single clause about what the fabric can now do - that is the whole answer.'),
     anyN('r-3', 'Example of its use in clothing', 2, 1, 2, exs[:CAP],
          'One example, 2 marks, graded 2:0 - all-or-nothing. It must be a garment, not a fabric: raincoats for waterproofing, children\'s night wear for flame retardant, jeans for mercerising.')],
    'Fixed, three rows: the scheme prints its six finishes as name, effect and example, so the rows are the three columns of that list and the option picked in one row fixes the answer in the other two.',
    stem='Textiles can be treated with a variety of fabric finishes.',
    tariff_kind='fixed'))

E2c = block(E2, 'or 2.(c) The future of fashion')
ch = block(E2c, '3 points @ 3 marks (graded 3:2:0) creates employment', '(ii) Describe two fashion accessories')
cards.append(C(
    PFX+'q2ci', Y, LV, 'home-economics-3-8', 'irish-designers-contribution-to-industry',
    '2023 OL Section C E2 Q2(c)(i)',
    'Describe the contribution of Irish fashion designers to the clothing and textile industry.',
    '3 points @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Contribution of Irish fashion designers', 9, 3, 3,
          semis(ch, '3 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Three points at 3 marks, graded 3:2:0 - and the scheme prints only three options, so all three are needed. Employment across manufacture, distribution and sales; the range of goods exported; and promoting Irish designers abroad.')],
    'One flat list. The scheme prints exactly three marking points for three required points, so there is no choice here.',
    stem='The future of fashion is in the hands of the designers.'))

ch = block(E2c, '2 points @ 3 marks (graded 3:2:0) bright coloured handbags')
cards.append(C(
    PFX+'q2cii', Y, LV, 'home-economics-3-8', 'popular-fashion-accessories',
    '2023 OL Section C E2 Q2(c)(ii)',
    'Describe two fashion accessories currently popular with trendsetters.',
    '2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'Fashion accessories currently popular', 6, 2, 3,
          semis(ch, '2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Only two points at 3 marks - a six-mark part. Describe, so name the accessory and add the detail that makes it current: the colour, the size, or how it is worn.')],
    'One flat list, taken in order to the cap.',
    stem='The future of fashion is in the hands of the designers.'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2023ol_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
