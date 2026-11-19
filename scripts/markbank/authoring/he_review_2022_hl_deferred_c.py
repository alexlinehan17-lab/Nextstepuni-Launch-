#!/usr/bin/env python3
"""All 26 deferred 2022 Section C tasks, checked at published mark boundaries."""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred import deferred_card, BASE
from he_review_2023_hl_deferred_c1 import after, named_sections
from he_review_2022_hl_deferred import documents, SOURCES

FIGURE = 'home-economics-2022-hl-deferred-sc-q1ai-fuels'
BOUNDS = [111, 217, 541, 351]
CROP_SHA256 = 'cd5a5da7f898ef21bf29f5a5d2d0f0e1ede97a588619cf622bd5c927e3e0be5b'
CLARIFICATIONS = {
    'solar': dict(sources=['https://www.eia.gov/energyexplained/solar/solar-thermal-collectors.php'], note='The scheme labels collectors, pumps and fans as passive solar. This describes active solar heating; passive design uses the building to collect and distribute solar heat.'),
    'insulation': dict(sources=['https://www.planningportal.nsw.gov.au/basix-thermal-comfort/design-principles/insulation'], note='Bulk insulation reduces heat transfer; it does not stop all heat or necessarily reflect heat back into the room.'),
    'emissions': dict(sources=['https://www.epa.gov/acidrain/what-acid-rain', 'https://www.data.jma.go.jp/ghg/kanshi/ghgp/co_e.html'], note='CO has indirect climate effects, unlike direct greenhouse gas CO2. Acid deposition is mainly driven by SO2 and NOx; CO2 explains normal rain’s mild acidity, not the scheme’s fixed pH 4.1 acid-rain claim.'),
    'social-policy': dict(sources=['https://www.gov.ie/en/department-of-social-protection/services/working-family-payment-wfp/', 'https://www.gov.ie/en/department-of-social-protection/publications/operational-guidelines-back-to-work-family-dividend/'], note='The scheme’s benefit-trap examples are not universal: in-work and transition supports exist, including the Back to Work Family Dividend introduced in 2015. No current eligibility advice is supplied.'),
    'osteoporosis': dict(sources=['https://www.niams.nih.gov/health-topics/osteoporosis', 'https://www.nidcr.nih.gov/health-info/tooth-decay'], note='Fractures, fragile bones and vertebral changes are appropriate osteoporosis effects; tooth decay is a distinct acid-driven process, not a general direct effect of osteoporosis.'),
    'bacteria': dict(sources=['https://www.canada.ca/en/health-canada/programs/consultation-e-coli-drinking-water/document.html', 'https://ask.fsis.usda.gov/article/How-do-bacteria-spoil-food', 'https://www.cdc.gov/infection-control/hcp/disinfection-sterilization/steam-sterilization.html', 'https://guidelines.nhmrc.gov.au/australian-drinking-water-guidelines/part-4/disinfection/1.7-disinfection-with-ultraviolet-light'], note='E. coli is facultatively anaerobic; growth time varies; heat/UV effectiveness depends on conditions and exposure. Darkness is not a universal bacterial requirement.'),
}
MARKS = {1: dict(ai=16,aii=24,aiii=10,bi=18,bii=12,ci=18,cii=12), 2: dict(ai=10,aii=15,b=15,ci=6,cii=9), 3: dict(ai=24,aii=16,aiii=10,bi=18,bii=12,ci=12,cii=18), 4: dict(ai=20,aii=18,aiii=12,bi=20,bii=10,ci=12,cii=18)}
SELECTION = {1: dict(ai=[],aii=['one'],aiii=['one'],bi=['three'],bii=['one'],ci=[],cii=[]), 2: dict(ai=[],aii=['three'],b=['one'],ci=[],cii=[]), 3: dict(ai=[],aii=[],aiii=['one'],bi=['two'],bii=['each','following'],ci=[],cii=['two']), 4: dict(ai=[],aii=[],aiii=[],bi=['four'],bii=['two'],ci=[],cii=['four'])}


def paper_tasks(docs):
    tasks = {}
    for n in range(1, 5):
        text = tidy(docs['bc'][n + 3].get_text(clip=fitz.Rect(0, 0, 595, 760)))
        groups = list(re.finditer(rf'{n}\.\(([abc])\)', text))
        assert len(groups) == 3
        for i, group in enumerate(groups):
            body = text[group.end():groups[i+1].start() if i+1<len(groups) else len(text)].strip()
            body = re.sub(r'\s+(?:and|or)$', '', body)
            parts = list(re.finditer(r'\((i{1,3})\)', body))
            for j, part in enumerate(parts or [None]):
                key = group[1] + (part[1] if part else '')
                question = body[part.end():parts[j+1].start() if j+1<len(parts) else len(body)].strip() if part else body
                assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', question, re.I) == SELECTION[n][key], (n, key, question)
                mark_text = f'({MARKS[n][key]} marks)'; assert question.count(mark_text) == 1
                # Q3(b)(i) prints its marks in the middle of the extracted sentence.
                # Remove the mark annotation only; never discard the remaining ask.
                question = ' '.join(question.replace(mark_text, '').split()).replace(' \uf0b7 ', '\n• ')
                stem = body[:parts[0].start()].strip() if parts else ''
                if not parts and n == 2:
                    stem, question = question.split('Write a profile', 1); question = 'Write a profile' + question; stem = stem.strip()
                tasks[n, key] = (question, stem)
    assert len(tasks) == 26
    return tasks


def build():
    docs = documents(); tasks = paper_tasks(docs)
    s = {n: tidy(docs['scheme'][n-1].get_text(clip=fitz.Rect(0, 0, 595, 788))) for n in range(16, 26)}
    cards = []
    def add(n, part, topic, concept, rows, notation):
        question, stem = tasks[n, part]
        if n == 1 and part[0] == 'a': stem = ''
        roman = f'({part[1:]})' if len(part)>1 else ''
        ref = (f'E{n} ' if n<4 else '') + f'Q{n}({part[0]}){roman}'
        c = deferred_card(f'sc-q{n}{part}', 'C', ref, topic, concept, question, stem, MARKS[n][part], notation, rows, n+4)
        c['id']=c['id'].replace('2023','2022');c['year']=2022;c['questionRef']=c['questionRef'].replace('2023','2022')
        c['sourceMaterial']['attribution']=c['sourceMaterial']['attribution'].replace('2023','2022')
        c['notes']='2022 deferred source pages independently reviewed; complete boundaries, choices and factual clarifications recorded in he_review_2022_hl_deferred_c.py and home-economics/2022-hl-deferred-review.json.'
        cards.append(c);return c
    def guidance(text, marker): return after(text, marker)
    fuel = after(between(s[16], '(i)', '(ii)'), '(graded: 4:2:0)')
    for label in ['Oil:', 'Gas:', 'Electricity:', 'Electricity – night rate:']: fuel=fuel.replace(' '+label,'\n\n'+label)
    c=add(1,'ai','3-6','fuel-cost-efficiency-comparison',[criterion(f'merit-{i}','merits',1,[0,2,4],f'Merit {i} of four, graded 4:2:0. Use the table and give a distinct relevant point; the scheme does not require one point from every fuel. '+('Source correction: the paper table gives the night rate as 9.60 cent/kWh; the 15.21c in the prose below is inconsistent. All figures refer to 2020, not current prices. Complete published examples:\n\n'+fuel if i==1 else 'Use the complete source guidance and corrected table value above.')) for i in range(1,5)],'4 merits × 4 (4:2:0)')
    c['stem']='The table below shows a comparison of energy costs and efficiency ratings for a variety of fuel used to heat a room in 2020. (www.seai.ie)'
    c.update(questionFigureKey=FIGURE,questionFigureIncludesPrompt=False)
    type_names=after(s[16],'Type of heating system: 6 marks (graded: 6:3:0)')
    heat=between(s[17],'Underlying principle 3 points @ 3 marks (graded: 3:2:0)','Reasons for choice:')
    labels=['Wet central heating:', 'Dry central heating/under floor/storage heating:', 'Passive solar heating:', 'Air source heat pump:', 'Ground source heat pump:']
    bodies=named_sections(heat,labels)
    reasons=between(s[17],'3 reasons @ 3 marks (graded: 3:2:0)','(iii)')
    variants=[]
    for key,label,body in zip(['wet','dry','active-solar','air-source','ground-source'],['Wet central heating','Dry central / underfloor / storage heating','Active solar heating','Air source heat pump','Ground source heat pump'],bodies):
        clarification='Source correction: this collector/pump/fan description is printed under “Passive solar heating”, but describes active solar heating. ' if key=='active-solar' else ''
        variants.append(dict(id=key,label=label,rows=[criterion('type','Type of heating system',1,[0,3,6],'One system, graded 6:3:0. Published type examples: '+type_names), criterion('principle','Underlying principle',3,[0,2,3],'Three points for the same system, each graded 3:2:0. '+clarification+'Complete published principle: '+body), criterion('reasons','Reasons for choice',3,[0,2,3],'Three reasons appropriate to your chosen system, each graded 3:2:0. Published examples: '+reasons)]))
    for key,label,note in [('passive-solar','Passive solar heating','Source correction: passive design collects and distributes heat through the building’s orientation, glazing and thermal mass, without the powered collectors/pumps/fans described under this name in the scheme. The source prints no accurate passive model.'),('another','Another valid heating system','The named systems are examples, not a finite choice pool. The source prints no model principle for this alternative; explain your chosen system accurately.')]:
        variants.append(dict(id=key,label=label,rows=[criterion('type','Type of heating system',1,[0,3,6],'One system, graded 6:3:0. Published examples: '+type_names),criterion('principle','Underlying principle',3,[0,2,3],'Three points for the same system, each graded 3:2:0. '+note),criterion('reasons','Reasons for choice',3,[0,2,3],'Three reasons for the same system, each graded 3:2:0. Published examples: '+reasons)]))
    c=add(1,'aii','3-5','central-heating-profile',deepcopy(variants[0]['rows']),'Type 6 (6:3:0); principle 3 × 3; reasons 3 × 3 (3:2:0)');c['answerVariants']=variants
    insulation=after(s[17],'Name: Bonded beads;');insulation='Bonded beads;'+insulation
    name,principle=insulation.split('Underling principle:',1)
    add(1,'aiii','3-6','wall-insulation',[criterion('name','Name of insulation',1,[0,2],'Name one method, graded 2:0. Published examples: '+name),criterion('principle','underlying principle',2,[0,2,4],'Two points for that method, each graded 4:2:0. Source clarification: bulk insulation slows heat transfer; it does not completely stop heat or necessarily reflect it. Published wording: '+principle.strip())],'Name 2 (2:0); principle 2 × 4 (4:2:0)')
    housing=after(between(s[18],'1.(b)','(ii)'),'(graded: 6:3:0)')
    add(1,'bi','3-3','housing-design-changes',[criterion('changes','changes',3,[0,3,6],'Three changes, each graded 6:3:0. “Recent” refers to this 2022 examination. Published guidance: '+housing)],'3 changes × 6 (6:3:0)')
    grants=after(after(between(s[18],'1.(b)','1.(c)'),'(ii)'), 'Details 2 points @ 4 marks (graded: 4:2:0)').removesuffix(' or').strip()
    add(1,'bii','3-3','housing-grant-profile',[criterion('name','Name',1,[0,2,4],'Name one grant, graded 4:2:0. These are historical 2022 examples, not current eligibility advice: '+grants),criterion('details','Details',2,[0,2,4],'Two accurate details of the same grant, each graded 4:2:0. The scheme lists names only; no model grant details are printed.')],'Name 4; details 2 × 4 (all 4:2:0)')
    c1=after(s[18],'1.(c)');inefficient=after(between(c1,'(i)','(ii)'),'Strategies: 3 @ 3 marks (graded: 3:2:0)')
    rows=[]
    for i in range(1,4):
        row=criterion(f'pair-{i}','Energy inefficiencies',2,[0,2,3],f'Pair {i}: one inefficiency and a matching improvement strategy, each graded 3:2:0. '+('The scheme lists inefficient uses but no model strategies. Complete examples: '+inefficient if i==1 else 'Use the examples above and give an accurate matching strategy.'))
        for part,label in zip(row['parts'],['Energy inefficiency','Improvement strategy']):part['verbatim']=label
        rows.append(row)
    add(1,'ci','3-6','home-energy-efficiency',rows,'3 pairs × (inefficiency 3 + strategy 3), all 3:2:0')
    emissions=after(c1,'3 effect @ 2 marks (graded 2:0)').replace(' Emissions:','\n\nEmissions:').replace(' Smog and smoke:','\n\nSmog and smoke:')
    rows=[]
    for i in range(1,4):
        row=criterion(f'pair-{i}','emissions',2,[0,2],f'Pair {i}: a distinct emission and matching environmental effect, each graded 2:0. '+('Source clarification: CO2 directly contributes to warming; CO affects climate indirectly. SO2 and nitrogen oxides drive acid deposition; CO2 causes normal rain’s mild acidity. Acid rain does not have one fixed pH. Published examples and wording:\n\n'+emissions if i==1 else 'Use the source examples and factual clarifications above; match each effect to its emission.'))
        for part,label in zip(row['parts'],['Emission','Environmental effect']):part['verbatim']=label
        rows.append(row)
    add(1,'cii','3-6','fuel-emissions-effects',rows,'3 pairs × (emission 2 + effect 2), all 2:0')

    add(2,'ai','3-8','smart-casual-workwear',[criterion('sketch','Sketch',1,list(range(5)),'Sketch the outfit asked for; graded 4:3:2:1:0. The source prints no model drawing.'),criterion('description','Description',1,[0,2,4,6],'Describe the same smart casual work outfit; graded 6:4:2:0. The source prints no model description.')],'Sketch 4 (4:3:2:1:0); description 6 (6:4:2:0)')
    principles=after(between(s[19],'(ii)','• how the outfit'),'(graded: 3:2:0)')
    suitable=after(after(s[19].split('2.(b)',1)[0],'2 points @ 3 marks'),'(graded: 3:2:0)').removesuffix(' and').strip()
    c=add(2,'aii','3-8','workwear-design-evaluation',[criterion('principles','principles of design',3,[0,2,3],'Apply three principles to your own outfit; each graded 3:2:0. Source examples (names only, no model applications): '+principles),criterion('purpose','suitable for purpose',2,[0,2,3],'Two points about the same outfit’s suitability, each graded 3:2:0. Source examples (no model evaluations): '+suitable)],'Principles 3 × 3; suitability 2 × 3 (3:2:0)')
    c['stem']+='\n\nUse your outfit from part (a)(i): “Sketch and describe a smart casual outfit suitable for work wear.”'
    fabric=after(s[19],'Name – polyester cotton (polycotton)');production,properties,uses=named_sections(fabric,['Fibre production –','Fabric properties –','Uses –'])
    routes=[dict(id='polycotton',label='Polyester cotton (polycotton)',rows=[criterion('name','name',1,[0,1],'Name one blend, graded 1:0. Published example: polyester cotton (polycotton).'),criterion('production','fibre production',2,[0,2,3],'Two points, each graded 3:2:0. Published guidance: '+production),criterion('properties','fabric properties',2,[0,2],'Two properties, each graded 2:0. Both positive and negative examples are retained: '+properties),criterion('uses','uses',2,[0,2],'Two suitable uses, each graded 2:0. Published guidance: '+uses)])]
    routes.append(dict(id='another-blend',label='Another valid blended fabric',rows=[criterion('name','name',1,[0,1],'Name one blended fabric, graded 1:0. The paper leaves the choice open.'),criterion('production','fibre production',2,[0,2,3],'Two accurate production points for the chosen blend, each graded 3:2:0. No alternative model is printed.'),criterion('properties','fabric properties',2,[0,2],'Two accurate properties of the chosen blend, each graded 2:0. No alternative model is printed.'),criterion('uses','uses',2,[0,2],'Two appropriate uses of the chosen blend, each graded 2:0. No alternative model is printed.')]))
    c=add(2,'b','3-7','blended-fabric-profile',deepcopy(routes[0]['rows']),'Name 1; production 2 × 3 (3:2:0); properties 2 × 2; uses 2 × 2 (2:0)');c['answerVariants']=routes
    sectors=after(between(s[20],'(i)','(ii)'),'(graded: 3:2:0)')
    add(2,'ci','3-8','irish-clothing-sectors',[criterion('sectors','sectors',2,[0,2,3],'Describe two sectors, each graded 3:2:0. The source lists names only, not model descriptions: '+sectors)],'2 sectors × 3 (3:2:0)')
    tech=after(s[20].split('(ii)',1)[1],'(graded: 3:2:0)')
    add(2,'cii','3-8','technology-clothing-design',[criterion('technology','technology',3,[0,2,3],'Three discussed points, each graded 3:2:0. The source names example areas but prints no model discussions: '+tech)],'3 points × 3 (3:2:0)')

    education=between(s[21].split('3.(b)',1)[0],'(i)','(ii)');names=['Physical','Emotional','Moral','Intellectual'];bodies=named_sections(education,[name+':' for name in names])
    add(3,'ai','3-10','purpose-education',[criterion(name.lower(),name,1,[0,3,6],'Required development heading, graded 6:3:0. Published examples: '+body) for name,body in zip(names,bodies)],'4 required headings × 6 (6:3:0)')
    opportunity=after(between(s[21],'(ii)','(iii)'),'(graded: 4:2:0)')
    add(3,'aii','3-10','education-equality',[criterion('opportunity','equality of opportunity',4,[0,2,4],'Four points, each graded 4:2:0. The source describes group-level inequalities, not inevitable outcomes for individual students. Published 2022 guidance: '+opportunity)],'4 points × 4 (4:2:0)')
    initiatives=after(between(s[21],'(iii)','3.(b)'), 'Details: 2 points @ 3 marks (graded: 3:2:0)').removesuffix(' and').strip()
    add(3,'aiii','3-10','education-access-initiative',[criterion('name','Name',1,[0,2,4],'Name one initiative, graded 4:2:0. “Contemporary” refers to 2022. Source examples, not current eligibility guidance: '+initiatives),criterion('details','Details',2,[0,2,3],'Two accurate details of that initiative, each graded 3:2:0. The source gives examples only, with no model details.')],'Name 4 (4:2:0); details 2 × 3 (3:2:0)')
    assert '2 groups @ 3 marks (graded: 3:2:0)' in s[21]
    poverty=s[22].split('(ii)',1)[0];groups=between(poverty,'Groups at risk:','Impact:');impact=after(poverty,'Impact:')
    add(3,'bi','3-9','poverty-groups-impact',[criterion('groups','groups',2,[0,2,3],'Two groups at risk, each graded 3:2:0. Published examples: '+groups),criterion('family','family',1,[0,2,4],'One required family impact, graded 4:2:0. Published impact examples: '+impact),criterion('society','society',1,[0,2,4],'One required societal impact, graded 4:2:0. Apply the source examples above at society level.'),criterion('other','one other',1,[0,2,4],'One further distinct family or societal impact, graded 4:2:0. Use the complete impact examples above.')],'Groups 2 × 3 (3:2:0); family 4 + society 4 + other 4 (4:2:0)')
    policy=after(s[22].split('3.(c)',1)[0],'(ii)');cycle=between(policy,'Cycle of poverty:','Social policy on poverty:');social=after(policy,'Social policy on poverty:').removesuffix(' and').strip()
    add(3,'bii','3-9','poverty-cycle-policy',[criterion('cycle','cycle of poverty',1,[0,3,6],'Required heading, graded 6:3:0. The paper asks how it has affected poverty rates. Intergenerational disadvantage is a risk, not an inevitable outcome for a family. Published example: '+cycle),criterion('policy','social policy on poverty',1,[0,3,6],'Required heading, graded 6:3:0. Source clarification: the benefit-trap example is not universal. In-work and transition supports exist, including Working Family Payment and Back to Work Family Dividend. The historical guidance is not current benefits advice: '+social)],'2 required headings × 6 (6:3:0)')
    family=after(s[22],'3.(c)');dual=after(between(family,'(i)','(ii)'),'(graded: 4:2:0)').replace(' Negative:','\n\nNegative:')
    add(3,'ci','3-11','dual-earner-families',[criterion('impact','family life',3,[0,2,4],'Three analysed points, each graded 4:2:0. These are possible positive/negative effects, not universal outcomes or a required positive/negative quota. Complete published examples: '+dual)],'3 points × 4 (4:2:0)')
    childcare=after(family,'(graded 2:1:0)) x 2');rows=[]
    for i in range(1,3):
        rows.extend([criterion(f'name-{i}','Name',1,[0,1],f'Childcare option {i}: name, graded 1:0. Choose two different options. '+('Published examples: '+childcare if i==1 else 'Use the example list above or another valid option.')),criterion(f'evaluation-{i}','Evaluate',4,[0,1,2],f'Four evaluation points for option {i}, each graded 2:1:0. The scheme lists names only, not model evaluations.')])
    add(3,'cii','3-11','childcare-options',rows,'2 options × (name 1 + evaluation 4 × 2), evaluation 2:1:0')

    milk=after(between(s[23],'(i)','(ii)'),'(graded: 4:3:2:1:0)')
    add(4,'ai','0-9','milk-dietary-significance',[criterion('nutrition','nutritional significance',5,list(range(5)),'Five points, each graded 4:3:2:1:0. No fixed quota per nutrient is printed. Full published guidance: '+milk)],'5 points × 4 (4:3:2:1:0)')
    osteoporosis=between(s[23],'(ii)','(iii)');risk=between(osteoporosis,'(graded 4:2:0)','• the effects');effects=after(osteoporosis,'(graded 2:0)')
    add(4,'aii','0-1','osteoporosis-risk-effects',[criterion('risk','main factors',3,[0,2,4],'Three risk factors, each graded 4:2:0. Published examples: '+risk),criterion('effects','effects of osteoporosis',3,[0,2],'Three effects, each graded 2:0. Source clarification: tooth decay is a separate process involving bacterial acids acting on enamel; it is not a general direct effect of osteoporosis. Use the bone/fracture effects. Complete historical wording: '+effects)],'Risk factors 3 × 4 (4:2:0); effects 3 × 2 (2:0)')
    exports=after(s[23].split('(iii)',1)[1],'(graded 4:2:0)')
    add(4,'aiii','0-11','dairy-exports',[criterion('reasons','reasons',3,[0,2,4],'Three reasons, each graded 4:2:0. Published 2022 guidance: '+exports)],'3 reasons × 4 (4:2:0)')
    bacteria=after(between(s[24],'(i)','(ii)'),'(graded 5:4:3:2:0)')
    for label in ['Warmth:', 'Moisture:', 'Oxygen:', 'pH level:', 'Time:', 'Light:']:bacteria=bacteria.replace(' '+label,'\n\n'+label)
    rows=[]
    for i in range(1,5):
        rows.append(criterion(f'condition-{i}','conditions',1,[0,2,3,4,5],f'Condition {i} of four, graded 5:4:3:2:0. Choose four different conditions. '+('Source clarifications: E. coli is facultatively anaerobic; bacterial growth rates vary, so 20 minutes is an example, not a universal rate. Heat and UV inactivation depend on exposure conditions and time/dose; darkness is not a universal requirement. The printed temperatures alone are not a sterilisation procedure. Complete published guidance:\n\n'+bacteria if i==1 else 'Use the complete seven-heading source guidance and factual clarifications above.')))
    add(4,'bi','0-4','bacterial-growth',rows,'4 conditions × 5 (5:4:3:2:0)')
    microbes=after(s[24].split('(ii)',1)[1],'(graded 5:4:3:2:1:0)')
    add(4,'bii','0-4','microorganisms-food-production',[criterion('uses','uses',2,list(range(6)),'Two distinct uses, each graded 5:4:3:2:1:0. Complete published examples: '+microbes)],'2 uses × 5 (5:4:3:2:1:0)')
    economy=after(between(s[25],'(i)','(ii)'),'(graded 4:2:0)')
    add(4,'ci','1-0','family-financial-unit',[criterion('role','financial unit',3,[0,2,4],'Three points, each graded 4:2:0. Economic commentary refers to this 2022 examination. Published guidance: '+economy)],'3 points × 4 (4:2:0)')
    spending=after(s[25].split('(ii)',1)[1],'(graded 4:2:0)')
    add(4,'cii','1-0','household-expenditure-factors',[criterion(f'factor-{i}','factors',1,[0,3,5] if i<3 else [0,2,4],f'Distinct factor {i}: '+('graded 5:3:0. ' if i<3 else 'graded 4:2:0. ')+('The scheme allocates two 5-mark factors and two 4-mark factors; it does not assign particular factor names to either tariff. Use the two 5-mark slots for your strongest distinct explanations. Historical 2022 guidance: '+spending if i==1 else 'Use the complete source guidance above; do not score the same factor twice.')) for i in range(1,5)],'2 factors × 5 (5:3:0) + 2 factors × 4 (4:2:0)')
    assert len(cards)==26 and sum(c['totalMarks'] for c in cards)==385
    return cards


def write():
    cards=build();path=ROOT/'scripts/markbank/authored/home-economics.json';authored=json.loads(path.read_text())
    for c in cards:
        i=next((i for i,old in enumerate(authored) if old['id']==c['id']),None)
        if i is None:authored.append(c)
        else:authored[i]=c
    path.write_text(json.dumps(authored,ensure_ascii=False,indent=1)+'\n')
    target=ROOT/f'public/exam-figures/home-economics/{FIGURE}.png';documents()['bc'][4].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(BOUNDS)).save(target)
    sha=hashlib.sha256(target.read_bytes()).hexdigest(); assert sha == CROP_SHA256
    path=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(path.read_text());manifest[FIGURE]=dict(src=f'/exam-figures/home-economics/{FIGURE}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt='2020 fuel costs (cent/kWh) and efficiency: standard coal 5.66, 60%; kerosene oil 8.60, 80%; natural gas Band D2 6.86, 90%; electricity Band DE 17.77, 100%; electricity night rate 9.60, 100% (shared electricity cell).',attribution='SEC Home Economics 2022 Higher Level deferred examination paper, page 5; source SEAI — © State Examinations Commission.',sourceNote=f'Original table, bounds {BOUNDS}, rendered at 2×. Source SHA256 {SOURCES["bc"]["sha256"]}. Shared electricity efficiency cell retained.');path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    path=ROOT/BASE/'2022-hl-deferred-review.json';review=json.loads(path.read_text());review['tasks']=[t for t in review['tasks'] if t['section']!='C']+[dict(id=c['id'],status='carded',section='C',questionRef=c['questionRef'],marks=c['totalMarks'],topicId=c['topicId']) for c in cards]
    assert len(review['tasks'])==61 and sum(t['marks'] for t in review['tasks'])==749
    review['status']='source-complete; all-source-pages-visually-reviewed; browser-QA-pending';review['sectionStatus']['C']='All 26 tasks carded; 385 offered marks.'
    review['sectionCReview']=dict(paperPages=list(range(5,9)),schemePages=list(range(16,26)),tasks=26,offeredMarks=385,clarificationsChecked='2026-11-01',sourceClarifications=CLARIFICATIONS,figure=dict(key=FIGURE,bounds=BOUNDS,scale=2,sha256=sha),decisions=['C1(a)(i): one comparison with four merit slots, original five-fuel table and corrected 9.60 night-rate value.', 'C1(a)(ii): one open heating profile; all source principles and reasons retained as routes, with active/passive correction.', 'C1(a)(iii) and C1(b)(ii): open insulation/grant profiles remain one task each.', 'C1(c): three dependent pairs per task at the published element tariffs.', 'C2(a)(ii) carries the earlier outfit prompt; blended-fabric profile stays open.', 'C3(a)(i): four required development headings; education initiatives and childcare options remain open.', 'C3 scheme page 21: retain the final scoring line ending at y=782; the footer starts at y=788.8.', 'C3(b)(i): the full question continues after the extracted 18-mark annotation; retain the family/society ask and its one-family/one-society/one-other quota.', 'C3(b)(ii) and C3(c)(i): original paper verbs and dual-earner wording retained despite scheme paraphrases.', 'C4(a): no invented milk nutrient quota; osteoporosis risk/effects remain one account.', 'C4(b)(i): one choose-four response, all seven source headings, exact 5:4:3:2:0 ladder.', 'C4(c)(ii): two 5-mark factors plus two 4-mark factors; no equal division or predetermined factor assignments.'])
    review['resolvedDecisions']=review.get('resolvedDecisions', review['pendingDecisions']);review['pendingDecisions']=[]
    review['completion']=dict(sourceReviewedTasks=61,offeredPracticeMarks=749,candidateMarks=review['candidateMarks'],note='Full independent sweep of all 79 source pages. Candidate elective/section choices are not additive. Main sitting and Irish editions are separate. Browser QA remains pending.')
    path.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n');print('2022 Higher deferred C: 26 tasks, 385 offered marks; full sitting 61 tasks / 749 offered marks.')


if __name__=='__main__':
    if '--write' in sys.argv:write()
    else:print(json.dumps(build(),ensure_ascii=False,indent=2))
