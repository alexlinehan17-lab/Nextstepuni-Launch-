"""2022 Higher Level, Section C."""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = load(2022, 'higher')
SEC = tidy(T[27206:51408])
Y, LV, PFX, CAP = 2022, 'higher', 'he-2022-hl-sc-', 14
cards, held = [], []
def C(*a, **k):
    k.setdefault('section', 'C'); return card(*a, **k)
def bundle(h, prefix='', n=None):
    seg = semis(h, prefix); return '; '.join(seg[:n] if n else seg)

# ---------------------------------------------------------------- Elective 1
E1 = block(SEC, 'Elective 1 – Home Design', 'Elective 2 – Textiles')
E1a = block(E1, '1.(a) ‘Working from home', 'and 1.(b)')

# (match anchor, label, prefix to strip). The anchor has to be long enough to be
# unambiguous, but stripping the whole anchor would eat the first few words of
# the description -- "Architect - , house design" instead of "advises on site".
SERV = [('Architect advises on site', 'Architect', 'Architect'),
        ('Structural/Site engineer:', 'Structural/site engineer', 'Structural/Site engineer:'),
        ('Surveyor survey site', 'Surveyor', 'Surveyor'),
        ('Solicitor contracts', 'Solicitor', 'Solicitor'),
        ('Builder draws up building contract', 'Builder', 'Builder')]
ch = block(E1a, 'Architect advises on site', '(ii) Recommend a suitable floor covering')
# 'Interior Designer' is included as a heading so Builder's chunk STOPS there.
# Without it Builder swallowed the bare-name list, and the "etc." between them is
# stripped by semis() -- which broke contiguity and failed the provenance gate.
chunks = heads(ch, [a for a, _, _ in SERV] + ['Interior Designer'])
named = [f'{label} - {bundle(h, strip)}' for h, (_, label, strip) in zip(chunks, SERV)]
bare = semis(chunks[-1])
cards.append(C(
    PFX+'q1ai', Y, LV, 'home-economics-3-3', 'professional-services-for-a-home-office',
    '2022 HL Section C E1 Q1(a)(i)',
    'Identify and describe three professional services that could assist individuals when modifying their home to include a home office space.',
    '3 points @ 5 marks (graded 5:4:2:0)', 15,
    [anyN('r-1', 'Professional services assisting a home modification', 15, 3, 5,
          (named + bare)[:CAP],
          'Three services at 5 marks, graded 5:4:2:0 - the 4 is the give-away that naming plus a thin description still scores well. Identify AND describe, so pair the title with what they actually do. The first five carry the scheme’s own detail; the rest are named only, so you supply the role.')],
    'One option per named service, each carrying that service’s own detail. The five the scheme details are listed first; the ones it only names follow.',
    stem='‘Working from home in separate home offices can improve work-life balance.’ (The Irish Times, 2021)'))

ch = block(E1a, '4 points @ 3 marks (graded 3:2:0) cost', '• properties')
cards.append(C(
    PFX+'q1aii', Y, LV, 'home-economics-3-4', 'choosing-a-floor-covering-factors',
    '2022 HL Section C E1 Q1(a)(ii) - factors to consider',
    'Set out the factors to consider when selecting a floor covering for a home office.',
    '4 points @ 3 marks (graded 3:2:0)', 12,
    [anyN('r-1', 'Factors to consider when selecting a floor covering', 12, 4, 3,
          semis(ch, '4 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Four factors at 3 marks, graded 3:2:0, and the scheme prints only six - so name the factor and tie it to a home office. Function is the one that earns most here: a room you sit and work in wants warmth and quiet, not a hard cold floor.')],
    'The factors strand at its own 12 marks. The 2-mark naming strand and the 6-mark properties strand are held - see the held file.',
    stem='‘Working from home in separate home offices can improve work-life balance.’ (The Irish Times, 2021)'))
held.append(dict(C(
    PFX+'q1aii-properties', Y, LV, 'home-economics-3-4', 'floor-covering-name-and-properties',
    '2022 HL Section C E1 Q1(a)(ii) - name and properties',
    'Name a suitable floor covering for a home office and give its properties.',
    'name 2 marks (graded 2:1:0); properties 3 points @ 2 marks (graded 2:0)', 8,
    [anyN('r-1', 'Floor covering and its properties', 8, 3, 2, [], 'Held - see heldReason.')],
    'Held - see heldReason.',
    stem='‘Working from home in separate home offices can improve work-life balance.’ (The Irish Times, 2021)'),
    heldReason='The scheme prints these as a two-column table (covering | properties) and the PDF extraction interleaves the columns: "chips easily; etc. stone carpeting Tiles slate tiles", "chinese slate easy to clean", "low limestone tiles/slabs; maintenance". Slicing it would ship name-column fragments as student-facing marking points, so both the naming and properties strands are held rather than guessed. Accounts for 8 of the 20 marks; the 12-mark factors strand ships as he-2022-hl-sc-q1aii.'))

CPT = ['Colour primary, secondary', 'Pattern add variety', 'Texture adds interest']
h_col, h_pat, h_tex = heads(block(E1a, 'Colour primary, secondary'), CPT)
cards.append(C(
    PFX+'q1aiii', Y, LV, 'home-economics-3-4', 'colour-pattern-and-texture-in-interior-design',
    '2022 HL Section C E1 Q1(a)(iii)',
    'Outline how colour, pattern and texture can be used to enhance the interior design of a room.',
    '1 point @ 5 marks (graded 5:3:0) x 3', 15,
    [anyN('r-1', 'Colour', 5, 1, 5, semis(h_col, 'Colour')[:CAP],
          'One point, 5 marks, graded 5:3:0. Much the longest list. The strongest answers use colour to change the room rather than just naming schemes: bright reflects light and enlarges, dark absorbs and makes it cosier.'),
     anyN('r-2', 'Pattern', 5, 1, 5, semis(h_pat, 'Pattern')[:CAP],
          'One point, 5 marks, graded 5:3:0. A short list - variety, interest, and the scale of the pattern. Say what the scale does to the room, since that is the only real development available.'),
     anyN('r-3', 'Texture', 5, 1, 5, semis(h_tex, 'Texture')[:CAP],
          'One point, 5 marks, graded 5:3:0. The thinnest of the three. Contrast is the idea worth writing: smooth against rough, matt against shiny.')],
    'Fixed: the question names all three elements, so all three must be answered. Priced identically at 5 marks each.',
    stem='‘Working from home in separate home offices can improve work-life balance.’ (The Irish Times, 2021)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 1.(b)
E1b = block(E1, 'and 1.(b) ‘Proper ventilation', '1.(c) ‘25%')
ch = block(E1b, '3 points @ 4 marks (graded 4:2:0) Stale air', '(ii) Recommend one artificial method')
cards.append(C(
    PFX+'q1bi', Y, LV, 'home-economics-3-5', 'effects-of-poor-ventilation',
    '2022 HL Section C E1 Q1(b)(i)',
    'Describe the effects of poor ventilation in the home.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Effects of poor ventilation in the home', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three effects at 4 marks, graded 4:2:0. The scheme runs three ways - the air itself (stale, humid, low oxygen), the people in it (asthma, bronchitis, carbon monoxide), and the building (condensation, damp, mould). One from each shows range, and carbon monoxide is the one worth naming outright.')],
    'One flat list, taken in order to the cap.',
    stem='‘Proper ventilation is very important.’ (seai.ie)'))

VENT = ['Extractor fan the shutters open', 'Cooker hood an electric motor',
        'Modified heat recovery ventilation system']
ch = block(E1b, 'Artificial methods Extractor fan')
h_ef, h_ch, h_hrv = heads(ch, VENT)
cards.append(C(
    PFX+'q1bii', Y, LV, 'home-economics-3-5', 'artificial-kitchen-ventilation-and-its-principle',
    '2022 HL Section C E1 Q1(b)(ii)',
    'Recommend one artificial method of ventilation suitable for a kitchen and explain the underlying principle of this method.',
    'Name 2 marks (graded 2:1:0); underlying principle 4 points @ 4 marks (graded 4:2:0)', 18,
    [anyN('r-1', 'Artificial method of ventilation suitable for a kitchen', 2, 1, 2,
          ['Extractor fan', 'Cooker hood', 'Modified heat recovery ventilation system'],
          'Name one, 2 marks. Only 2 of the 18 marks - the naming is almost free, and everything rests on being able to explain whichever one you name. The cooker hood has the longest explanation in the scheme, so it is the safest choice for a kitchen.'),
     anyN('r-2', 'Underlying principle of the method named', 16, 4, 4,
          (semis(h_ef, 'Extractor fan') + semis(h_ch, 'Cooker hood')
           + semis(h_hrv, 'Modified heat recovery ventilation system -'))[:CAP],
          'Four points at 4 marks - 16 of the 18 marks, so this row is the question. For the fan and the hood the principle is suction: a motor spins the blades, that creates suction, stale or grease-laden air is drawn out and fresh air replaces it. Work through it as a sequence rather than listing parts.')],
    'Fixed: naming is priced at 2 and the principle at 16. The principle row pools the scheme’s three explained methods, because the four points are awarded for whichever method the candidate named.',
    stem='‘Proper ventilation is very important.’ (seai.ie)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 1.(c)
E1c = block(E1, '1.(c) ‘25%')
SOL = ['Solar photovoltaic systems', 'Passive solar architecture', 'Active solar heating/solar panels']
ch_sys = block(E1c, 'Solar photovoltaic systems', '• merits of using solar energy')
ch_mer = block(E1c, 'Merits - hot water is always available')
ch_sus = block(E1c, 'Sustainability – the sun is a renewable', '(ii) Explain, giving an example')
cards.append(C(
    PFX+'q1ci', Y, LV, 'home-economics-3-6', 'solar-energy-as-a-home-energy-source',
    '2022 HL Section C E1 Q1(c)(i)',
    'Set out details of solar energy as an energy supply source to the home. Refer to: a system used in the home to utilise solar energy; merits of using solar energy; sustainability.',
    'system 2 points @ 3 marks; merits 3 points @ 3 marks; sustainability 1 point @ 3 marks', 18,
    [anyN('r-1', 'A system used in the home to utilise solar energy', 6, 2, 3,
          [f'{a} - {bundle(h, a)}' for h, a in zip(heads(ch_sys, SOL), SOL)][:CAP],
          'Two points at 3 marks. Three systems, and they are genuinely different: PV makes electricity, active solar heats water, passive solar is the house design itself. Naming one and saying what it converts is the 3.'),
     anyN('r-2', 'Merits of using solar energy', 9, 3, 3, semis(ch_mer, 'Merits -')[:CAP],
          'Three merits at 3 marks. Split between money (lower heating and electricity bills, little servicing) and environment (no smoke or carbon dioxide). Take from both rather than writing the same saving three ways.'),
     anyN('r-3', 'Sustainability', 3, 1, 3, semis(ch_sus, 'Sustainability –')[:CAP],
          'One point at 3 marks. The scheme prints only two, and both say the same thing: the sun is renewable and effectively infinite. Say renewable and say why that matters - it cannot be used up the way a fossil fuel is.')],
    'Fixed: the question names three strands and prices them separately at 6, 9 and 3.',
    stem='‘25% of the energy used in Ireland is used in our homes.’ (seai.ie)',
    tariff_kind='fixed'))

ch_pr = block(E1c, 'Underlying Principle Air, polystyrene')
ch_ex = block(E1c, 'Examples fibreglass')
cards.append(C(
    PFX+'q1cii', Y, LV, 'home-economics-3-6', 'principle-of-home-insulation',
    '2022 HL Section C E1 Q1(c)(ii)',
    'Explain, giving an example, the underlying principle of a method of insulation used in the home.',
    'Underlying principle 2 points @ 4 marks (graded 4:2:0); example @ 4 marks (graded 4:0)', 12,
    [anyN('r-1', 'Underlying principle of insulation', 8, 2, 4,
          semis(ch_pr, 'Underlying Principle')[:CAP],
          'Two points at 4 marks. The whole principle is one idea: these materials are poor conductors, and trapped air is what makes them poor conductors. Say that heat cannot pass through easily so it is held inside the house.'),
     anyN('r-2', 'Example of a method of insulation', 4, 1, 4, semis(ch_ex, 'Examples')[:CAP],
          'One example at 4 marks, graded 4:0 - all or nothing, so name a real method. The scheme accepts the full range, from cavity wall and attic materials to double glazing, a lagging jacket and heavy lined curtains.')],
    'Fixed: the principle is priced at 8 and the example at 4. Graded 4:0 on the example means a vague answer scores nothing.',
    stem='‘25% of the energy used in Ireland is used in our homes.’ (seai.ie)',
    tariff_kind='fixed'))

# ---------------------------------------------------------------- Elective 2
E2 = block(SEC, 'Elective 2 – Textiles', 'Elective 3 – Social Studies')
E2a = block(E2, '2.(a) ‘Smart casual', 'and 2.(b)')

OUT = ['Comfort – loose fitting trousers', 'Aesthetic appeal – appeals to professionals',
       'Lifestyle - smart casual can be worn']
ch = block(E2a, 'Comfort – loose fitting trousers', '(ii) Discuss how colour')
held.append(dict(C(
    PFX+'q2ai', Y, LV, 'home-economics-3-8', 'evaluating-a-smart-casual-outfit',
    '2022 HL Section C E2 Q2(a)(i)',
    'Evaluate the design of the outfits shown in the image above. Refer to: comfort; aesthetic appeal; lifestyle.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Evaluation of the outfits shown', 15, 3, 5,
          [f'{a.split(chr(8211))[0].split(" - ")[0].strip()} - {bundle(h, a)}'
           for h, a in zip(heads(ch, OUT), OUT)][:CAP],
          'Held - see heldReason.')],
    'Held - see heldReason.',
    stem='‘Smart casual is a fusion of two contrasting dress codes.’ (Louis Copeland)'),
    heldReason='Marks a photograph of two outfits printed on the paper. Every marking point describes that image ("loose fitting trousers", "soft fabric in t-shirt", "casual blazer", "comfortable trainers"), so the card is unanswerable without the figure and the markdown extraction does not carry it.'))

ch = block(E2a, 'Colour – Tonal dressing')
cards.append(C(
    PFX+'q2aii', Y, LV, 'home-economics-3-8', 'using-colour-to-flatter-body-size-and-shape',
    '2022 HL Section C E2 Q2(a)(ii)',
    'Discuss how colour can be used to flatter body size and shape.',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'How colour can be used to flatter body size and shape', 10, 2, 5,
          semis(ch, 'Colour –')[:CAP],
          'Two points at 5 marks, graded 5:3:0. Each point needs the effect, not just the colour: dark shades absorb light and outline the silhouette, a single colour head to toe creates an illusion of height. "Black is slimming" on its own is the 3.')],
    'One flat list, taken in order to the cap.',
    stem='‘Smart casual is a fusion of two contrasting dress codes.’ (Louis Copeland)'))

# ------------------------------------------------------------------- 2.(b)
E2b = block(E2, 'and 2.(b) (i) Differentiate', 'or 2.(c)')
h_reg, h_syn = heads(block(E2b, 'Regenerated created by dissolving', '(ii) Explain, filament modification'),
                     ['Regenerated created by dissolving', 'Synthetic polymer'])
cards.append(C(
    PFX+'q2bi', Y, LV, 'home-economics-3-7', 'regenerated-versus-synthetic-fibres',
    '2022 HL Section C E2 Q2(b)(i)',
    'Differentiate between regenerated and synthetic fibres.',
    '1 point @ 3 marks (graded 3:2:0) x 2', 6,
    [anyN('r-1', 'Regenerated fibres', 3, 1, 3, semis(h_reg, 'Regenerated')[:CAP],
          'One point, 3 marks. The word that earns it is cellulose: a plant fibre dissolved in chemicals and re-formed as fibre. So it starts natural and is chemically treated.'),
     anyN('r-2', 'Synthetic fibres', 3, 1, 3, semis(h_syn, 'Synthetic')[:CAP],
          'One point, 3 marks. The contrast is the origin: 100% chemical, a polymer made from oil or coal, with no plant or animal source at all.')],
    'Fixed: differentiate means both sides are required, priced identically at 3 marks each.',
    tariff_kind='fixed'))

ch = block(E2b, 'Techniques used to change or improve')
ch_ex = block(E2b, 'Examples blending')
cards.append(C(
    PFX+'q2bii', Y, LV, 'home-economics-3-7', 'filament-modification',
    '2022 HL Section C E2 Q2(b)(ii)',
    'Explain filament modification, giving two examples.',
    'Explain 1 point @ 3 marks (graded 3:0); examples 2 @ 3 marks (graded 3:0)', 9,
    [anyN('r-1', 'What filament modification is', 3, 1, 3, semis(ch)[:CAP],
          'One point at 3 marks, graded 3:0 - all or nothing. The scheme prints a single line: techniques used to change or improve the properties of a fabric. Say what is being changed and you have it.'),
     anyN('r-2', 'Examples of filament modification', 6, 2, 3, semis(ch_ex, 'Examples')[:CAP],
          'Two examples at 3 marks each, graded 3:0. Two thirds of the marks, and they are single words - blending, crimping, twisting, mercerisation. Learn four and you can never lose this row.')],
    'Fixed: the explanation is priced at 3 and the two examples at 6. Both rows are graded 3:0, so each point is all or nothing.',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 2.(c)
E2c = block(E2, 'or 2.(c) The functionality')
ch = block(E2c, '3 points @ 3 marks (graded 3:2:0) lengthen', '(ii) Discuss how traditional crafts')
cards.append(C(
    PFX+'q2ci', Y, LV, 'home-economics-3-8', 'modifying-a-commercial-pattern',
    '2022 HL Section C E2 Q2(c)(i)',
    'Describe one method of modifying a commercial pattern to tailor it to the specific needs of an individual.',
    '3 points @ 3 marks (graded 3:2:0)', 9,
    [anyN('r-1', 'Method of modifying a commercial pattern', 9, 3, 3,
          semis(ch, '3 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Three points at 3 marks, graded 3:2:0. One method, described in three steps - the scheme works through lengthening (cut along the alteration lines, insert tissue, redraw the fitting lines) and shortening (fold along an alteration line by half the amount). Pick one and give all three steps.')],
    'One flat list, taken in order to the cap. The scheme runs the lengthen and shorten methods together, so the method names sit inside the options.',
    stem='The functionality and aesthetic appeal of a garment has a strong influence on its design.'))

ch = block(E2c, '2 points @ 3 marks (graded 3:2:0) hand-weaving')
cards.append(C(
    PFX+'q2cii', Y, LV, 'home-economics-3-8', 'traditional-crafts-in-irish-design',
    '2022 HL Section C E2 Q2(c)(ii)',
    'Discuss how traditional crafts have influenced Irish design and fashion industry.',
    '2 points @ 3 marks (graded 3:2:0)', 6,
    [anyN('r-1', 'How traditional crafts have influenced Irish design and fashion', 6, 2, 3,
          semis(ch, '2 points @ 3 marks (graded 3:2:0)')[:CAP],
          'Two points at 3 marks, graded 3:2:0. Name the craft and say where it shows up in modern clothing - Aran stitches in coatigans, Irish linen from summer skirts to heavy jackets, lace and crochet in wedding dresses. The garment is what turns a 2 into a 3.')],
    'One flat list, taken in order to the cap.',
    stem='The functionality and aesthetic appeal of a garment has a strong influence on its design.'))

# ---------------------------------------------------------------- Elective 3
E3 = block(SEC, 'Elective 3 – Social Studies', 'Question 4 – Core')
E3a = block(E3, '3.(a) According to CSO', '3.(b) ‘Everyone has a right')

ch = block(E3a, 'Unemployment occurs when a person of working age', '(ii) Discuss the following')
cards.append(C(
    PFX+'q3ai', Y, LV, 'home-economics-3-9', 'defining-unemployment-hl',
    '2022 HL Section C E3 Q3(a)(i)',
    'Define unemployment.',
    '1 point @ 6 marks (graded 6:3:0)', 6,
    [anyN('r-1', 'Definition of unemployment', 6, 1, 6, [bundle(ch)],
          'One point at 6 marks, graded 6:3:0 - so this is 6 or 3, nothing between. The scheme prints the definition in three parts and all three are needed for the 6: of working age, without work, and both available for and seeking work. Leave out the seeking-work half and it is a 3.')],
    'A single option carrying the whole definition, because the scheme prices it as one point and grades it 6:3:0 on how complete that one definition is.',
    stem='According to CSO data, 216 959 people were estimated to be either out of work or in receipt of the government’s pandemic unemployment payment in November 2021. (www.cso.ie)'))

FACT = ['changing requirements of industry increased automation',
        'geographical location variations in employment',
        'level of consumer demand for products and services.']
h_ind, h_geo, h_dem = heads(block(E3a, 'changing requirements of industry increased automation',
                                  '(iii) Describe the effects'), FACT)
o_ind = semis(h_ind, 'changing requirements of industry')
o_geo = semis(h_geo, 'geographical location')
o_dem = semis(h_dem, 'level of consumer demand for products and services.')
cards.append(C(
    PFX+'q3aii', Y, LV, 'home-economics-3-9', 'contributory-factors-to-unemployment',
    '2022 HL Section C E3 Q3(a)(ii)',
    'Discuss the following as contributory factors to unemployment in Ireland: changing requirements of industry; geographical location; level of consumer demand for products and services.',
    '5 points @ 4 marks (graded 4:2:0) - 1 point on each and 2 other points', 20,
    [anyN('r-1', 'changing requirements of industry', 4, 1, 4, o_ind[:CAP],
          'One point at 4 marks. The idea is that the jobs themselves changed: automation and new technology removed some roles and demanded a different skillset for the ones that remain.'),
     anyN('r-2', 'geographical location', 4, 1, 4, o_geo[:CAP],
          'One point at 4 marks. The scheme wants the spiral, not just "some areas have fewer jobs" - people leave to find work, so shops and services close, so there are fewer jobs again.'),
     anyN('r-3', 'level of consumer demand for products and services', 4, 1, 4, o_dem[:CAP],
          'One point at 4 marks. Demand falls and jobs follow: cheaper imports and online shopping pull spending away from Irish producers and local shops, and people with less income spend less again.'),
     anyN('r-4', 'Two further points, from any of the three factors', 8, 2, 4,
          (o_ind + o_geo + o_dem)[:CAP],
          'Two further points at 4 marks each - the scheme says "1 point on each and 2 other points", so these eight marks can come from any of the three factors. Develop the one you know best rather than reaching for a fourth idea.')],
    'Fixed: the scheme requires one point on each named factor, then floats the remaining 8 marks across all three. Modelled as four rows so the three compulsory points cannot be lost.',
    stem='According to CSO data, 216 959 people were estimated to be either out of work or in receipt of the government’s pandemic unemployment payment in November 2021. (www.cso.ie)',
    tariff_kind='fixed'))

ch = block(E3a, '3 points @ 4 marks (graded 4:2:0) Children lack role models', '(iv) Name one statutory initiative')
cards.append(C(
    PFX+'q3aiii', Y, LV, 'home-economics-3-9', 'effects-of-unemployment-on-society-hl',
    '2022 HL Section C E3 Q3(a)(iii)',
    'Describe the effects of unemployment on society.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Effects of unemployment on society', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three effects at 4 marks, graded 4:2:0. Keep them at society level - the generational pattern where children grow up without a working role model, anti-social behaviour from boredom, unemployment blackspots, and the cost to the State. An effect on one person is not what this asks.')],
    'One flat list, taken in order to the cap.',
    stem='According to CSO data, 216 959 people were estimated to be either out of work or in receipt of the government’s pandemic unemployment payment in November 2021. (www.cso.ie)'))

INIT = ['Action Plan for Jobs:', 'Industrial Development Authority (IDA) –', 'SOLAS:',
        'National Further Education and Training Authority;', 'JobsPlus /Revenue Job Assist',
        'Enterprise Ireland responsible', 'Údarás na Gaeltachta provides',
        'Work Placement Experience Programme gives', 'Local Enterprise Offices supports']
ch = block(E3a, 'Action Plan for Jobs: government agencies')
# 3.(a) ends "...provide mentoring service; etc. and", the connector into 3.(b).
# semis() strips the "etc." and keeps a bare "and", which the last initiative's
# bundle then swallowed -- failing the provenance gate.
if ch.rstrip().endswith(' and'):
    ch = ch.rstrip()[:-4]
init_chunks = heads(ch, INIT)
cards.append(C(
    PFX+'q3aiv', Y, LV, 'home-economics-3-9', 'statutory-initiatives-creating-employment',
    '2022 HL Section C E3 Q3(a)(iv)',
    'Name one statutory initiative aimed at creating employment and outline how it helps to enhance employment options.',
    'Name 4 marks (graded 4:2:0); outline 2 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Name of the statutory initiative', 4, 1, 4,
          ['Action Plan for Jobs', 'Industrial Development Authority (IDA)', 'SOLAS',
           'National Further Education and Training Authority', 'JobsPlus', 'Enterprise Ireland',
           'Údarás na Gaeltachta', 'Work Placement Experience Programme',
           'Local Enterprise Offices'],
          'Name one, 4 marks. Nine are accepted, so the difficulty is not naming one but naming one you can then explain for the other 8 marks. SOLAS and the IDA are the two most students can develop.'),
     anyN('r-2', 'How the initiative enhances employment options', 8, 2, 4,
          [f'{a.rstrip(": –;").strip()} - {bundle(h, a)}' for h, a in zip(init_chunks, INIT)][:CAP],
          'Two points at 4 marks - two thirds of the marks, and they must be about the initiative you named. Each option here carries that body’s own detail, so read the one you chose: the IDA is about attracting foreign investment, SOLAS about upskilling and apprenticeships, JobsPlus about paying employers to hire off the live register.')],
    'Fixed: naming is priced at 4 and the outline at 8. The outline row carries one option per initiative, each with that initiative’s own detail, because the two points must match whichever was named.',
    stem='According to CSO data, 216 959 people were estimated to be either out of work or in receipt of the government’s pandemic unemployment payment in November 2021. (www.cso.ie)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 3.(b)
E3b = block(E3, '3.(b) ‘Everyone has a right', 'or 3.(c)')
ch = block(E3b, '3 points @ 4 marks (graded 4:2:0) Allows young people', '(ii) Name and evaluate')
cards.append(C(
    PFX+'q3bi', Y, LV, 'home-economics-3-11', 'benefits-of-leisure-for-young-people',
    '2022 HL Section C E3 Q3(b)(i)',
    'Analyse how young people benefit from participating in leisure activities.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'How young people benefit from leisure activities', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three benefits at 4 marks, graded 4:2:0. Analyse, so each needs a consequence: not "they make friends" but that leisure brings young people together and keeps them from isolation. The scheme runs physical, social and personal - one from each is the widest answer.')],
    'One flat list, taken in order to the cap.',
    stem='‘Everyone has a right to rest and leisure.’ (UN, Universal Declaration of Human Rights)'))

LEI = ['Name – sports clubs', 'Cost – initial costs', 'Value for money – amount of use',
       'Facilities – classes/tuition']
h_nm, h_cost, h_val, h_fac = heads(block(E3b, 'Name – sports clubs'), LEI)
cards.append(C(
    PFX+'q3bii', Y, LV, 'home-economics-3-11', 'evaluating-two-leisure-facilities',
    '2022 HL Section C E3 Q3(b)(ii)',
    'Name and evaluate two popular leisure facilities you have studied. Refer to: cost and value for money; range of facilities offered.',
    '(Name 1 mark; cost 1 point @ 2 marks; value for money 1 point @ 2 marks; facilities 2 points @ 2 marks) x 2', 18,
    [anyN('r-1', 'Name of the leisure facility', 2, 2, 1, semis(h_nm, 'Name –')[:CAP],
          'Two facilities at 1 mark each - the cheapest marks on the paper, and the rest of the question depends on them. Pick two you can actually cost, like a GAA club and a gym.'),
     anyN('r-2', 'Cost', 4, 2, 2, semis(h_cost, 'Cost –')[:CAP],
          'One cost point per facility at 2 marks. The scheme splits cost in two - the initial membership fee and the ongoing cost of equipment and clothes. Naming both halves for one facility is the safest 2.'),
     anyN('r-3', 'Value for money', 4, 2, 2, semis(h_val, 'Value for money –')[:CAP],
          'One value point per facility at 2 marks. Value is not price - it is what you get for the price: how much you use it, family rates, discounts, free entry to tournaments.'),
     anyN('r-4', 'Range of facilities offered', 8, 4, 2, semis(h_fac, 'Facilities –')[:CAP],
          'Two facilities points each, at 2 marks - eight of the eighteen marks, the biggest row. List what is physically there: pitches, floodlighting, changing rooms, a canteen, tuition and equipment.')],
    'Fixed: the scheme prices four strands and doubles the whole thing for two facilities, so each row here carries both facilities at once - 1x2, 2x2, 2x2 and 4x2.',
    stem='‘Everyone has a right to rest and leisure.’ (UN, Universal Declaration of Human Rights)',
    tariff_kind='fixed'))

# ------------------------------------------------------------------- 3.(c)
E3c = block(E3, 'or 3.(c) The Irish education system')
ch = block(E3c, '4 points @ 4 marks (graded 4:2:0) Parental attitude', '(ii) Evaluate two initiatives')
cards.append(C(
    PFX+'q3ci', Y, LV, 'home-economics-3-10', 'factors-influencing-educational-achievement-hl',
    '2022 HL Section C E3 Q3(c)(i)',
    'Analyse the factors that influence the educational achievement of school children.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Factors influencing educational achievement', 16, 4, 4,
          semis(ch, '4 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Four factors at 4 marks, graded 4:2:0. The scheme prints eight bare factors and no detail, so every one of the 16 marks is in your explanation. Say how the factor acts - a large family means less one-to-one attention and nowhere quiet to study.')],
    'One flat list, taken in order to the cap. The scheme names the factors only, so the development is entirely the candidate’s.',
    stem='The Irish education system provides a holistic education for children.'))

EQ = ['Delivering Equality of Opportunity in Schools (DEIS)', 'Learning Support withdrawal',
      'Special Needs Assistants/Inclusion Support Assistants', 'Extra Resources e.g. laptop',
      'Tusla encourages', 'Social welfare benefits back to school',
      'Variety of educational programmes offered']
eq_chunks = heads(block(E3c, 'Delivering Equality of Opportunity in Schools (DEIS)'), EQ)
cards.append(C(
    PFX+'q3cii', Y, LV, 'home-economics-3-10', 'initiatives-for-equality-of-opportunity-in-education',
    '2022 HL Section C E3 Q3(c)(ii)',
    'Evaluate two initiatives aimed at providing equality of opportunity in education with reference to early school leavers.',
    '(name 3 marks (graded 3:2:0); description 1 point @ 4 marks (graded 4:2:0)) x 2', 14,
    [anyN('r-1', 'Name of the initiative', 6, 2, 3,
          ['Delivering Equality of Opportunity in Schools (DEIS)', 'Learning Support',
           'Special Needs Assistants/Inclusion Support Assistants', 'Extra Resources',
           'Tusla', 'Social welfare benefits', 'Variety of educational programmes offered'],
          'Two initiatives at 3 marks each. DEIS is the one to name first - it is the only initiative the scheme describes at length, and it is aimed squarely at early school leavers, which is what the question asks about.'),
     anyN('r-2', 'Description of the initiative', 8, 2, 4,
          # Strip only the LABEL, not the whole anchor: 'Extra Resources e.g. laptop'
          # would otherwise drop "e.g. laptop" out of the middle and break
          # contiguity with the scheme.
          [f'{lbl} - {bundle(h, lbl)}'
           for h, lbl in zip(eq_chunks, [a.split(' e.g.')[0].rstrip(';').strip() for a in EQ])][:CAP],
          'One description per initiative at 4 marks - eight of the fourteen marks. Tie it back to early school leaving: DEIS runs a school completion programme with homework clubs, after-school support, school meals and book grants, all aimed at keeping a child in school.')],
    'Fixed: the scheme prices naming at 3 and description at 4, doubled for two initiatives. Each description option carries that initiative’s own detail, because the description must match whichever was named.',
    stem='The Irish education system provides a holistic education for children.',
    tariff_kind='fixed'))

# ------------------------------------------------------------- Question 4 Core
Q4 = block(SEC, 'Question 4 – Core')
Q4a = block(Q4, '4.(a) ‘Food waste', '4.(b) ‘Being on a restrictive')

NUT = ['Protein 1-8%', 'Fat 0%', 'Carbohydrate 3-20%', 'Vitamins vitamin A', 'Minerals - calcium', 'Water 70-95%']
ch = block(Q4a, 'Protein 1-8%', '(ii) Give an account of a method of home preservation')
cards.append(C(
    PFX+'q4ai', Y, LV, 'home-economics-0-9', 'nutritional-significance-of-vegetables',
    '2022 HL Section C Q4(a)(i) - Core',
    'Discuss the nutritional significance of vegetables in the diet.',
    '5 points @ 4 marks (graded 4:3:2:1:0)', 20,
    [anyN('r-1', 'Nutritional significance of vegetables', 20, 5, 4,
          [f'{lbl} - {bundle(h, lbl)}' for h, lbl in zip(heads(ch, NUT), NUT)][:CAP],
          'Five points at 4 marks, graded 4:3:2:1:0 - the long grading ladder means a partial answer still scores, so write something for all five. Each nutrient needs the figure, the type, and what it does in the body: vitamins and minerals carry the most detail and are where vegetables genuinely matter.')],
    'One option per nutrient, each carrying that nutrient’s own detail, because the scheme groups its marking points under six nutrient headings and prices five points.',
    stem='‘Food waste is bad for the environment and bad for our pockets.’ (www.safefood.net)'))

PRES = ['Freezing blanching', 'Bottling sterilisation', 'Dehydration heated to remove',
        'Chutney/Relish chemical preservatives', 'Pickling boiling vegetables']
pres_chunks = heads(block(Q4a, 'Freezing blanching', 'Packaging strong'), PRES)
ch_pack = block(Q4a, 'Packaging strong', '(iii) Evaluate irradiation')
cards.append(C(
    PFX+'q4aii', Y, LV, 'home-economics-0-4', 'home-preservation-of-vegetables',
    '2022 HL Section C Q4(a)(ii) - Core',
    'Give an account of a method of home preservation suitable for vegetables. Refer to: name of preservation method; underlying principle; suitable packaging.',
    'name 3 marks (graded 3:0); underlying principle 3 points @ 4 marks; packaging 1 point @ 3 marks', 18,
    [anyN('r-1', 'Name of the preservation method', 3, 1, 3,
          ['Freezing', 'Bottling', 'Dehydration', 'Chutney/Relish', 'Pickling'],
          'Name one, 3 marks, graded 3:0 - all or nothing, but it is one word. Freezing has the fullest explanation in the scheme and is the most natural fit for vegetables.'),
     anyN('r-2', 'Underlying principle of the method named', 12, 3, 4,
          [f'{lbl.split(" ")[0]} - {bundle(h, lbl.split(" ")[0])}'
           for h, lbl in zip(pres_chunks, PRES)][:CAP],
          'Three points at 4 marks - 12 of the 18 marks, and they must match the method you named. Every method comes down to the same two ideas: stop the enzymes and stop the micro-organisms. Say HOW your method does each - blanching inactivates enzymes, freezing removes the warmth and locks water into ice crystals so bacteria cannot use it.'),
     anyN('r-3', 'Suitable packaging', 3, 1, 3, semis(ch_pack, 'Packaging')[:CAP],
          'One point at 3 marks. Match the packaging to the method - freezer bags and plastic containers for freezing, glass jars for bottling or pickling. The scheme accepts the correct packaging for whichever method was chosen.')],
    'Fixed: the question names three strands and prices them at 3, 12 and 3. The principle row carries one option per method, because the three points must match whichever was named.',
    stem='‘Food waste is bad for the environment and bad for our pockets.’ (www.safefood.net)',
    tariff_kind='fixed'))

ch_adv = block(Q4a, 'Advantages destroys food poisoning', 'Disadvantages causes rancidity')
ch_dis = block(Q4a, 'Disadvantages causes rancidity')
cards.append(C(
    PFX+'q4aiii', Y, LV, 'home-economics-0-4', 'evaluating-irradiation',
    '2022 HL Section C Q4(a)(iii) - Core',
    'Evaluate irradiation as a commercial method of food preservation.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Evaluation of irradiation', 12, 3, 4,
          (semis(ch_adv, 'Advantages') + semis(ch_dis, 'Disadvantages'))[:CAP],
          'Three points at 4 marks, graded 4:2:0. Evaluate means both sides - the scheme prints advantages and disadvantages together and prices them as one pool, so a candidate who writes only the good things is answering half the question. Two advantages and one disadvantage is the safe shape.')],
    'One flat list pooling the advantages and disadvantages, because the scheme prices three points across both rather than pricing each side separately.',
    stem='‘Food waste is bad for the environment and bad for our pockets.’ (www.safefood.net)'))

# ------------------------------------------------------------------- 4.(b)
Q4b = block(Q4, '4.(b) ‘Being on a restrictive', 'or 4.(c) Household technology')
ch = block(Q4b, '3 points @ 5 marks (graded 5:3:0) (15 marks) Exclude all foods')
cards.append(C(
    PFX+'q4bi', Y, LV, 'home-economics-0-1', 'dietary-guidelines-for-coeliac-disease',
    '2022 HL Section C Q4(b)(i) - Core',
    'Outline the dietary guidelines that should be followed by a person with coeliac disease.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Dietary guidelines for a person with coeliac disease', 15, 3, 5,
          semis(ch, '3 points @ 5 marks (graded 5:3:0) (15 marks)')[:CAP],
          'Three guidelines at 5 marks, graded 5:3:0. "Avoid gluten" is one point, not three - the other two come from how you actually do it: read the ingredient list, look for the gluten-free symbol, and build meals around foods that are naturally gluten free like rice, corn and potatoes.')],
    'One flat list, taken in order to the cap.',
    stem='‘Being on a restrictive diet should not mean a restricted food experience.’ (www.delicious.ie)'))

ch = block(Q4b, 'Use of sustainable practices')
cards.append(C(
    PFX+'q4bii', Y, LV, 'home-economics-0-11', 'popularity-of-irish-speciality-foods',
    '2022 HL Section C Q4(b)(ii) - Core',
    'Analyse the growing popularity of speciality foods produced by small businesses in Ireland.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Reasons for the growing popularity of speciality foods', 15, 3, 5,
          semis(ch)[:CAP],
          'Three points at 5 marks, graded 5:3:0. The scheme runs three threads - the environment (sustainable practices, fewer food miles), the local economy (employment, supporting local producers), and quality (traditional skills, small batches, Ireland’s food reputation). One from each is the strongest answer.')],
    'One flat list, taken in order to the cap.',
    stem='‘Being on a restrictive diet should not mean a restricted food experience.’ (www.delicious.ie)'))

# ------------------------------------------------------------------- 4.(c)
Q4c = block(Q4, 'or 4.(c) Household technology')
ch_con = block(Q4c, 'Kettle Construction – Made from stainless steel', 'Working principle -')
ch_wp = block(Q4c, 'Working principle - electricity flows', 'Guidelines for use –')
ch_gl = block(Q4c, 'Guidelines for use – switch on with dry hands', '(ii) Discuss the factors')
ch_acc = block(Q4c, 'Accept deep fat fryer', '(ii) Discuss the factors')
cards.append(C(
    PFX+'q4ci', Y, LV, 'home-economics-1-3', 'study-of-an-appliance-with-a-heating-element',
    '2022 HL Section C Q4(c)(i) - Core',
    'Set out details of a study you have undertaken on an appliance with a heating element. Refer to: name of appliance; construction; working principle; guidelines for use.',
    'name 2 marks (graded 2:0); construction 3 points @ 2 marks; working principle 3 points @ 2 marks; guidelines 2 points @ 2 marks', 18,
    [anyN('r-1', 'Name of the appliance', 2, 1, 2, (['Kettle'] + semis(ch_acc, 'Accept'))[:CAP],
          'Name one, 2 marks, graded 2:0. The kettle is the only appliance the scheme works through in full, so it is the safe answer - but a deep fat fryer, air fryer, toaster or iron is equally accepted if you know its parts.'),
     anyN('r-2', 'Construction', 6, 3, 2, semis(ch_con, 'Kettle Construction –')[:CAP],
          'Three points at 2 marks. Construction is the parts list - materials, then the components: element, thermostat, water level indicator, filter, heat-resistant handle. Easy marks if you have looked at the appliance.'),
     anyN('r-3', 'Working principle', 6, 3, 2, semis(ch_wp, 'Working principle -')[:CAP],
          'Three points at 2 marks. This is the row that separates candidates, and it is a chain: electricity meets resistance in the element, the element heats by conduction, convection currents carry that heat through the water, and the thermostat cuts the supply at temperature. Name the method of heat transfer at each step.'),
     anyN('r-4', 'Guidelines for use', 4, 2, 2, semis(ch_gl, 'Guidelines for use –')[:CAP],
          'Two points at 2 marks. Safety first - dry hands, unplug before filling - then the efficiency ones: use the level guides and boil only what you need.')],
    'Fixed: the question names four strands and prices them at 2, 6, 6 and 4.',
    stem='Household technology has become an integral part of our lives.',
    tariff_kind='fixed'))

ch = block(Q4c, '3 points @ 4 marks (graded 4:2:0) Initial cost')
cards.append(C(
    PFX+'q4cii', Y, LV, 'home-economics-1-2', 'factors-influencing-appliance-purchase',
    '2022 HL Section C Q4(c)(ii) - Core',
    'Discuss the factors that influence consumers’ decision making when purchasing large household appliances.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Factors influencing the purchase of a large household appliance', 12, 3, 4,
          semis(ch, '3 points @ 4 marks (graded 4:2:0)')[:CAP],
          'Three factors at 4 marks, graded 4:2:0. The scheme prints over twenty, so choice is not the problem - development is. Cost splits three ways (initial, running, maintenance), and energy efficiency is worth naming because it connects the two.')],
    'One flat list, taken in order to the cap.',
    stem='Household technology has become an integral part of our lives.'))

emit(cards)
json.dump(held, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'held_2022hl_secC.json'),'w'), ensure_ascii=False, indent=1)
print(f'held: {len(held)}', file=sys.stderr)
