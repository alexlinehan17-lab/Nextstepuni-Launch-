"""2011 Ordinary tasks transcribed after the complete paper/scheme visual sweep.

The independent census is maintained separately. Q1–Q4 have pooled tariffs;
Q10(d) has independent sample cases; Q13 awards follow the printed asterisks.
"""
from itertools import combinations
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers':'b7b85bb61a0e55572f8d576f7ad7cdc45d7311496297cf37b8c4b146b5fba748',
          'markingschemes':'3b7c1edf3a79a4862bf8fdb65d017c5b770c1b0d25c10df0bb8a22453280834f'}
SELECTIONS = {
    'e071cf9679a673b6':('exam-selection','Section One selects six independent 20-mark questions; all seven are retained.'),
    '730586d08013e726':('exam-selection','Section Two selects three independent 60-mark questions; all six are retained.'),
    'e778e922af95b4e0':('open','Q10(c) asks for three weathering processes but prints no finite list. The scheme is an accepted-answer menu.'),
    'd9bd22c89ac31be4':('independent-task-selection','Q12 selects two separately priced 30-mark parts. Each published internal task is retained; bundles of unrelated responses are not new practice identities.'),
}
SCIENTIFIC = {
    'q7c':('https://www.apsnet.org/edcenter/Pages/IntroOomycetes.aspx',
            'The 2011 scheme accepts “fungus” for potato blight. Phytophthora infestans is classified as an oomycete, a fungus-like organism. The historical wording and four-mark tariff are preserved.'),
    'q9di':('https://teagasc.ie/news--events/daily/taking-advantage-of-growth-rates/',
             'The historical scheme describes dry matter as retained or assimilated. DMD measures the percentage of consumed dry matter digested by the animal; it is not the percentage ultimately retained as body tissue.'),
    'q10biii':('https://gsi.geodata.gov.ie/downloads/Geoheritage/Reports/KK007_Archersgrove_Quarry.pdf',
                'The historical scheme lists Kilkenny for marble. Kilkenny Black Marble is a commercial name for limestone, a sedimentary rock. Connemara marble is a suitable metamorphic example. The original scheme remains visible.'),
}


def paper_review():
    observed, supplementary = scan(2011,FILE,HASHES,SELECTIONS,[
        (1,'Six questions must be answered.','exam-selection','Cover repeats the six-of-seven Section One selection.'),
        (1,'Three questions must be answered.','exam-selection','Cover repeats the three-of-six Section Two selection.'),
        (7,'match the words from the list below','answer-identification','Q10(a) requires six correct matches in one paragraph, not arbitrary choices or permutations.'),
        (8,'a cereal or a root crop','open','Q11(c) names open crop categories. Barley and potato are scheme examples, not a closed pool of named crops.'),
        (8,'under the following headings:','required-headings','Q11(c) requires all headings. Date and method split only where the scheme prices them separately.'),
        (8,'a named insect','open','Q11(b) permits any suitable named insect; the two scheme lifecycle types are marking examples.'),
        (8,'one named digestive enzyme','open','Q12(a) permits a suitable digestive enzyme and matching experiment, not a finite list.'),
        (8,'one named component','open','Q12(c)(ii) permits a suitable milk component and matching investigation, not a finite list.'),
    ])
    return dict(year=2011,level='ordinary',lang='ev',paperFileid=FILE,hashes=HASHES,
                wholePaperVisualReview='reviewed',schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1,13)),schemePagesInspected=list(range(1,17)),
                selectionDirectives=observed,supplementarySelections=supplementary,
                sourceNotes=[dict(questionN={'q7c':'7','q9di':'9','q10biii':'10'}[key],
                                  questionRef={'q7c':'Q7(c)','q9di':'Q9(d)(i)','q10biii':'Q10(b)(iii)'}[key],
                                  note=note,source=url) for key,(url,note) in SCIENTIFIC.items()],
                independentBoundaryReview='All paper and scheme pages inspected. Four shared descending scales remain whole. Separately priced definitions, scenarios, crop headings and genetic-cross fields split without duplicating marks. No internal closed optional pool is printed.',
                cropVisualReview='All 65 distinct paper/scheme crop pairs rendered and inspected. Clipped continuation lines, shared crop-name headings, genetic stems and the biodiversity crop corrected and re-rendered. All five original figure assets inspected.',
                remaining=['Irish edition comparison','Phone/desktop runtime review','Corpus-wide reconciliation'])


def reviewed_tasks():
    paper_review()
    cards,tasks=[],[]
    def add(key,ref,topic,old,atlas,concept,question,rows,pp,sp,stem=None,marks=None,selection=None,illustrated=False):
        cid='agsci-2011-ol-'+key
        rows=[dict(row,id=f'r-{i+1}') for i,row in enumerate(rows)]
        card=dict(id=cid,subjectId='agricultural-science',year=2011,level='ordinary',
                  section='A' if int(ref.split('(')[0].split(' ')[0][1:])<=7 else 'B',
                  questionRef='2011 OL '+ref,topicId='agsci-'+topic,
                  curriculumNodeIds=['agricultural-science-'+t for t in old.split('|')],conceptId=concept,
                  questionText=question,rows=rows,totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                  tariffModel={'kind':'questionTotal' if marks is not None else 'fixed'},
                  sourceMaterial=dict(kind='source-illustration' if illustrated else 'source-text',label='OFFICIAL QUESTION PAGE',
                      title='Agricultural Science 2011 Ordinary — '+ref,pages=sorted({r['p'] for r in pp}),
                      attribution='SEC Agricultural Science 2011 Ordinary Level examination paper — © State Examinations Commission.',
                      presentationNote='Open the original page for the published diagrams, wording and answer spaces.'))
        if stem: card['stem']=stem
        task=dict(questionRef=card['questionRef'],paperPage=pp[0]['p'],schemePage=sp[0]['p'],paperRegions=pp,schemeRegions=sp,
                  atlasNumbers={cid:str(1001+len(cards))},cardIds=[cid],marksPerRoute=card['totalMarks'],
                  examTopicIds=['agricultural-science-ordinary-'+t for t in atlas.split('|')],
                  selection=selection or {'kind':'none','reason':'Required response. Open examples and scheme alternatives are marking menus, not finite printed choice routes.'},
                  evidence='All 12 paper and 16 scheme pages visually inspected. Task boundaries and tariffs transcribed from the original sources independently of the legacy parser.')
        if key in SCIENTIFIC:
            url,note=SCIENTIFIC[key]
            task['schemeNote']=note
            task['scientificContext']={'source':url,'checkedAt':'2026-10-07','treatment':'Retain historical scheme and explain the scientific distinction.'}
            rows[0]['contextNote']=(rows[0].get('contextNote','')+' '+note).strip()
        cards.append(card);tasks.append(task)
        return card

    def variants(card,items):
        card['answerVariants']=[dict(id=k,label=label,rows=[dict(row,id=f'r-{i+1}') for i,row in enumerate(rows)]) for k,label,rows in items]

    section_one='Section One uses the published first-correct scale across the whole question. Surplus wrong answers cancel correct answers under the scheme’s general instructions; account for any such deduction when recording your mark.'
    c=add('q1','Q1','3-1','2-0','plant-physiology','bean-germination-and-dispersal',
        '(a) The diagram shows a germinating broad bean seed. Identify the parts labelled A and B. (b) List the three conditions necessary for seed germination. (c) State two ways in which plants disperse their seeds.',
        [menu(['A: Plumule','B: Radicle','Suitable temperature or warmth','Water or moisture','Oxygen or air',
               'Wind','water'],
              [7,7,2,1,1,1,1],section_one+' Claim no more than two distinct dispersal ways; a relevant description is accepted.')],
        [region(2,.27,.886)],[region(5,.187,.386)],illustrated=True)
    variants(c,[(f'dispersal-{i}', ' + '.join(pair), [menu(['A: Plumule','B: Radicle','Suitable temperature or warmth','Water or moisture','Oxygen or air',*pair],
        [7,7,2,1,1,1,1],section_one+' Select the pair of distinct dispersal ways you answered. Relevant descriptions are accepted; a germination condition and a dispersal method answer separate fields.')])
        for i,pair in enumerate(combinations(['Wind','water','animal','self dispersal'],2),1)])
    c['figureKey']='agsci-2011-ol-paper-bean'
    c['labelKey']=[dict(letter=l,meaning=m,askedInThisQuestion=True) for l,m in [('A','Plumule'),('B','Radicle')]]
    c=add('q2','Q2','2-3','1-6','fertilisers-pollution-the-environment','compound-fertiliser-and-manure',
        '(a) State one difference between a compound fertilizer and manure. In your answer mention one point about each. (b) The photograph shows a bag of compound fertilizer. The numbers on the front represent the major elements in the fertilizer. Name these three elements. (c) Other than the fertilizer shown, name another fertilizer used in agriculture.',
        [menu(['Manure: plant waste / animal waste / organic material / improves soil structure',
               'Fertilizer: artificial material / manmade / inorganic material / does not improve soil structure',
               'Nitrogen','Phosphorus','Potassium',
               '10:10:20 / 18:6:12 / CAN / Urea / Ground Rock Phosphate / Sulphate of Ammonia / any other fertilizer'],
              [7,7,2,2,1,1],section_one+' N, P and K may be given in any order; each appears at most once.')],
        [region(3,.038,.628)],[region(5,.418,.639)],'The illustrated compound fertilizer is 16-4-8.',illustrated=True)
    c['figureKey']='agsci-2011-ol-paper-fertiliser'
    add('q3','Q3','4-1','3-0','animal-physiology','mammalian-body-part-locations',
        'State the location of each of the following in the body of a mammal: (i) Left ventricle, (ii) Femur, (iii) Bronchiole, (iv) Testis, (v) Cerebrum. The completed example is villi: small intestine.',
        [menu(['Left ventricle: Heart','Femur: Thigh or (hind) leg','Bronchiole: Lung','Testis: Scrotum','Cerebrum: Brain or head or skull'],[7,7,2,2,2],section_one+' The completed villi example earns no marks.')],
        [region(3,.646,.955)],[region(5,.671,.925)])
    c=add('q4','Q4','4-2','3-1','classification-of-organisms|animal-diseases','liverfluke-and-snail-classification',
        'Complete the table in relation to the organisms shown in the photographs. For each organism give (i) its name, (ii) its phylum, (iii) one characteristic of a member of the phylum, and (iv) its importance in agriculture.',
        [menu(['Liverfluke / fluke / Fasciola (hepatica)','Snail / mudsnail / watersnail / garden snail / Lymnaea',
               'Platyhelminthes','Mollusca',
               'Triploblastic / bilaterally symmetrical / hermaphrodite / dorsoventrally flattened or flat bodied [Accept characteristic(s) of liverfluke if given e.g. cuticle / (oral) sucker]',
               'Shell / radula / muscular foot / soft bodied / produces slime',
               '(Internal) parasite of cattle (and sheep) / unsaleable livers / reduced weight gains / depressed milk yields / loss of wool / weight loss',
               'Host of liverfluke / eats or causes damage to plant (foliage)'],[6,6,2,2,1,1,1,1],section_one+' Options follow the table in pairs: left/right organism names, left/right phyla, left/right characteristics, left/right agricultural importance. Claim one answer per field; alternatives within a field cannot earn additional awards.')],
        [region(4,.038,.479)],[region(6,.08,.492)],illustrated=True)
    c['figureKey']='agsci-2011-ol-paper-organisms'
    c['additionalTopicIds']=['agsci-4-3-3']
    definitions=[('bullock','Bullock (or steer)','A male calf that has been castrated'),('gilt','Gilt','A female pig that has not had a litter'),
                 ('draft ewe','Draft or cast ewe','A ewe that is culled from the flock and sold'),('broiler','Broiler','A chicken that is reared for slaughter or reared for meat'),
                 ('suckler calf','Suckler calf','A calf (in the beef herd) that sucks milk from its mother')]
    for key,label,answer in definitions:
        add('q5-'+key.replace(' ','-'),'Q5 — '+key,'4-3-1','3-3','animal-production','livestock-term-'+key.replace(' ','-'),
            'Give a definition for the following term used in animal production: '+label+'.',[point(answer,4)],
            [region(4,.51,.811)],[region(6,.499,.704)])
    for letter,label,answer,sy in [
        ('a','Crop rotation','Prevents pests / prevents diseases / more balanced uptake of nutrients / weed control / improves organic matter content in soil',(.109,.153)),
        ('b','Sowing certified seed','high percentage purity / high germination rate / lower disease risk / potentially lower seeding rates / no weeds or wild oat / doesn’t have to be dressed / traceability / virus free potato seed / access to new varieties / tubers are graded for size / higher yields / treated for diseases',(.156,.235)),
        ('c','Applying selective herbicide','removal of weeds without killing crop',(.237,.263)),
        ('d','Planting winter varieties of cereals','Survive winter frosts / longer growing season / greater yield capacity / earlier harvesting / lessens labour load in spring on mixed farms / allows earlier sowing of catch crops on mixed farms / better weather at sowing time / better weather at harvest time',(.266,.344)),
    ]:
        add('q6'+letter,f'Q6({letter})','3-3-1' if letter in 'bd' else '3-3-2','2-3' if letter in 'bd' else '2-4','crop-production',
            'tillage-practice-'+letter,'Give a scientific explanation for the following practice carried out on tillage farms: '+label+'.',
            [point(answer,5,'Any one point.')],[region(5,.039,.57)],[region(7,*sy)])
    add('q7a','Q7(a)','4-3-3','3-5','animal-diseases','bacterial-livestock-diseases',
        'Name two diseases of livestock that are caused by bacteria.',
        [menu('TB|pneumonia|mastitis|brucellosis|scour|navel-ill|Clostridial disease(s) or named clostridial disease e.g. blackleg|footrot|farrowing fever|any other disease',[4,4],
              'Two distinct bacterial diseases; the generic scheme names refer to bacterial forms.')],[region(5,.591,.692)],[region(7,.391,.464)])
    add('q7b','Q7(b)','2-2-3','1-4','soil-science|animal-physiology','beneficial-agricultural-bacteria',
        'Give two benefits of bacteria in agriculture.',
        [menu('Silage production|production of dairy products (cheese, yoghurt)|digestion in ruminant|nitrogen fixation|breakdown of organic material in soil|any other benefits',[4,4])],
        [region(5,.705,.799)],[region(7,.467,.51)])
    add('q7c','Q7(c)','3-3-2','2-4','crop-production','potato-blight-pathogen',
        'Which type of organism is the cause of potato blight?',[point('Fungus / Phytophthora infestans / parasite',4)],
        [region(5,.82,.85)],[region(7,.513,.54)])

    sheep=[
        ('i','Tail docking','removal of tails in new born lambs|use of ring or knife|reduces risk of maggot infestation or flystrike|facilitates mating|keeps fleece clean',(.196,.241)),
        ('ii','Shearing','Removal of fleece or wool from sheep|keeps sheep cool in summer|sale of wool|reduced risk of maggots or flystrike|increase mobility of sheep|more space at housing|heavier lambs',(.243,.305)),
        ('iii','Raddling a ram','Raddle (harness) attached to ram’s chest|raddle contains dye|dye left on ewe’s wool when mounted by ram|shows which ewes have been served by ram|changed every 14 days|shows repeats|shows ram infertility|allows lambing dates to be predicted',(.307,.369)),
        ('iv','Dipping','Sheep immersed in tank containing insecticide|Summer dip insecticide prevents flystrike|Winter dip prevents infection by parasites|7-14 weeks protection|immerse sheep for 1 minute',(.37,.432)),
        ('v','Walking the flock through a footbath','prevents bacterial infection|foot rot|prevents spread of foot and mouth disease|solution of copper sulphate or formalin or zinc sulphate|repeated throughout year if necessary|carried out after feet are pared',(.434,.496)),
    ]
    for roman,label,pool,sy in sheep:
        add('q8a'+roman,f'Q8(a)({roman})','4-3-3','3-5','animal-production|animal-diseases','sheep-management-'+roman,
            'Write a note on the following practice carried out in sheep production: '+label+'.',
            [menu(pool,[3,3],'Two distinct points from the 2011 scheme. Synonymous descriptions of the same benefit count once.')],
            [region(6,.193,.337)],[region(8,*sy)])
    for roman,label,pool,sy in [
        ('i','Isolation pen','Housing sick animals|disease can be treated|prevent spread of disease to other animals|used to house bulls|important if buying in animals',(.556,.602)),
        ('ii','Infrared lamp','Keeps new born lambs or piglets (bonhams) warm|located in lambing pen or farrowing crate|used to treat lambs suffering from chill|temperature of 27°C - 30°C',(.603,.711)),
        ('iii','Creep feeder','Allows lambs or calves to feed but prevents older animals from feeding|creep feeder described|lamb or calf gets used to eating solid food|higher weight gains|higher weights at weaning',(.603,.711)),
        ('iv','Crush','Pen for holding livestock|restricts movement of animal|treated or examined by farmer or vet|prevents injury to animal or farmer|used at calving time',(.712,.758)),
        ('v','Farrowing crate','Located in farrowing house|20°C|sow gives birth to bonhams|crate allows bonhams to suck without being crushed',(.758,.803)),
    ]:
        add('q8b'+roman,f'Q8(b)({roman})','4-3-1','3-3','animal-production','livestock-equipment-'+roman,
            'Several pieces of equipment and housing units are used to ensure good farm management. Explain the use of the following on farms involved in livestock production: '+label+'.',
            [menu(pool,[3,3],'Two distinct points; expand a description where required by the scheme.')],
            [region(6,.356,.503)],[region(8,*sy)])
    pasture='Clover and perennial ryegrass are often used in seed mixtures for grazing.'
    add('q9ai','Q9(a)(i)','3-3-2','2-6','grassland','clover-seed-mixture-benefits','State three advantages of using clover in seed mixtures.',
        [menu('Nitrogen fixation|rich in protein|weed control|palatable|high productivity|cheaper than fertilizer|reduced need for N fertilizer|rich in minerals',[4,3,3])],
        [region(6,.505,.601)],[region(9,.108,.183)],pasture)
    add('q9aii','Q9(a)(ii)','3-3-2','2-6','grassland','perennial-ryegrass-benefits','Give two reasons why perennial ryegrass is considered to be a superior grass.',
        [menu('More palatable|higher yield or more productive|high DMD or high digestibility|persistent|aggressive',[5,5])],
        [region(6,.537,.601)],[region(9,.184,.229)],pasture)
    for key,label,answer,sy in [
        ('ley','Ley','Grassland sown by farmer / high production level / usually only one or two grasses present or fewer weeds / temporary grassland / grassland that is used as part of a rotation system or used as a “grass break”',(.26,.346)),
        ('establishment','Establishment','Becoming a totally independent plant / plants form a thick sward / grass tillers / new plant puts down roots / new plant begins to photosynthesise',(.342,.383)),
        ('heading out','Heading out','Stage when grass flowers / stage when 50% of grass plants begin to show their seed heads / carbohydrates begin to turn to fibre / stage of growth that is ideal for cutting for silage',(.379,.443)),
    ]:
        add('q9b-'+key.replace(' ','-'),'Q9(b) — '+key,'3-1' if key!='ley' else '3-3-2','2-6','grassland','grassland-term-'+key.replace(' ','-'),
            'Explain the underlined term: '+label+'.',[point(answer,5,'Any one point.')],
            [region(6,.604,.659)],[region(9,*sy)],'Farmers often sow a mixture of seed varieties in their leys. The seeds germinate and undergo establishment even though the varieties have different heading out dates.')
    for roman,scenario,answer in [('i','A farmer wants to plant barley but also to have grass available for grazing when the barley is harvested.','Undersowing'),
                                 ('ii','A farmer wants to sow grass seed on land which is shallow or not easily ploughed.','Direct drilling / stitching-in (slit-seeding)')]:
        add('q9c'+roman,f'Q9(c)({roman})','3-3-1','2-3|2-6','grassland','grass-sowing-scenario-'+roman,
            'Different methods may be used when sowing grass seed. State the most suitable method in this situation: '+scenario,
            [point(answer,5)],[region(6,.669,.765)],[region(9,.467,.553)])
    for roman,question,answer,sy in [
        ('i','What does the term Dry Matter Digestibility (DMD) mean?','The proportion (expressed as a %) of the dry matter of a feedstuff which is retained in the animal’s system following digestion / degree to which the dry matter is retained and assimilated by the animal’s body / the % of the food that is kept and used by the animal',(.584,.675)),
        ('ii','What approximate DMD value should high quality silage be?','70% - 80%',(.677,.704)),
        ('iii','Explain why old, poorly managed grassland is unsuitable for the production of good-quality silage.','Less productivity or low yield / low DMD or low digestibility / stemmy / more weeds or named grassland weed(s) / grass is less palatable',(.706,.751)),
    ]:
        add('q9d'+roman,f'Q9(d)({roman})','3-3-3','2-5|2-6','grassland','silage-quality-'+roman,question,[point(answer,5,'Any one point.')],
            [region(6,.768,.846)],[region(9,*sy)])

    add('q10a','Q10(a)','2-1','1-1','soil-science','peat-formation-passage',
        'Read the paragraph on the formation of peat bogs and match the words from the list with the numbered spaces. Write your answers in your answer book.',
        [point(answer,4,'Space '+str(i)) for i,answer in enumerate(['rainfall (accept waterlogging)','evaporation','1-2m','Acidity (accept waterlogging)','8-10m','waterlogging (accept rainfall)'],1)],
        [region(7,.038,.287)],[region(10,.079,.26)],
        'Word list: waterlogging; 1-2m; 8-10m; evaporation; rainfall; acidity. Blanket peats are formed in areas of high ___1___ and low ___2___. They are normally ___3___ in depth. ___4___ is a common characteristic of blanket peat. Basin peats are normally ___5___ in depth. They are formed in valleys and depressions as a result of ___6___.',
        selection={'kind':'answer-identification','reason':'All six numbered spaces have correct answers; permuting the word list is not a set of permitted examination routes.'})
    rocks=[
        ('i','igneous',[('granite','Granite','Wicklow / Donegal'),('basalt','Basalt','Antrim / Giant’s Causeway')]),
        ('ii','sedimentary',[('limestone','Limestone','Central plain of Ireland (or named county in central plain) / midlands / Burren / (N.) Clare / (S.W.) Wexford'),('sandstone','Sandstone','Cork / Kerry / Waterford'),('shale','Shale','Kerry / Limerick / Clare / Leitrim / Fermanagh / Kilkenny')]),
        ('iii','metamorphic',[('marble','Marble','Kilkenny / Galway / Connemara'),('schist','Schist','Galway / Mayo / Donegal / Tyrone / Derry'),('gneiss','Gneiss','Galway / Mayo / Donegal / Tyrone / Derry'),('quartzite','Quartzite','Galway / Mayo / Donegal / Tyrone / Derry'),('slate','Slate','Down / Armagh / Monaghan / Cavan / Meath / Louth / Wicklow / Wexford / Kildare')]),
    ]
    for roman,label,examples in rocks:
        menus=[(key,name,[point(name,3,'Rock example'),point(counties,2,'County/region must match this rock.')]) for key,name,counties in examples]
        c=add('q10b'+roman,f'Q10(b)({roman})','2-1','1-0','soil-science','rock-type-'+label,
            f'Give an example of an {label} rock. Mention an area or county on the island of Ireland where it is commonly found.' if roman=='i' else f'Give an example of a {label} rock. Mention an area or county on the island of Ireland where it is commonly found.',
            menus[0][2],[region(7,.299,.388)],[region(10,.261,.663)],
            selection={'kind':'open','reason':'Rock class is required; the paper does not print a closed list of rock examples. Menus preserve matched scheme examples.'})
        variants(c,menus)
        if 'q10b'+roman in SCIENTIFIC:
            for v in c['answerVariants']: v['rows'][0]['contextNote']+=' '+SCIENTIFIC['q10b'+roman][1]
    add('q10c','Q10(c)','2-1','1-0','soil-science','rock-weathering-processes',
        'Parent rock material may be weathered by physical or chemical means. Weathering breaks rock into soil particles. Give details of any three ways in which rock can be weathered.',
        [menu('Frost action or freezing and thawing|heating and cooling or onion weathering|plant action or example of plant action described|animal action or example of animal action described|wind erosion|water erosion|gravity|pressure due to moving ice or glaciers|solution|carbonation or acid rain|hydrolysis|hydration|oxidation-reduction',[3,3,3])],
        [region(7,.398,.437)],[region(10,.677,.785)],selection={'kind':'open','reason':'No finite list of weathering methods is printed in the question.'})
    for letter,answer in [('A','Clay'),('B','Loam'),('C','Sandy Loam')]:
        c=add('q10d-'+letter.lower(),'Q10(d) — soil '+letter,'2-2-2','1-3','soil-science','soil-texture-sample-'+letter.lower(),
            'Use the soil texture triangle to identify the texture of soil sample '+letter+'. Write your answer in your answer book.',[point(answer,4)],
            [region(7,.447,.939)],[region(10,.787,.888)],
            'The table lists sand, silt and clay respectively: Soil A: 10%, 35%, 55%; Soil B: 40%, 45%, 15%; Soil C: 60%, 25%, 15%. Use the original triangle shown with the table.',illustrated=True)
        c['figureKey']='agsci-2011-ol-paper-soil-triangle'

    parasite='Parasites are a common occurrence in agriculture.'
    add('q11ai','Q11(a)(i)','4-3-3','3-5','animal-diseases','parasite-definition','What is a parasite?',
        [point('An organism that lives in or on or off another (living) organism (host)',3),point('causing it harm',3)],
        [region(8,.038,.145)],[region(11,.079,.137)],parasite)
    add('q11aii','Q11(a)(ii)','4-3-3','3-5','animal-diseases|crop-production','parasite-host-example',
        'Give an example of a parasite of a named crop or livestock that you have studied.',
        [point('Liverfluke - sheep / lice - cattle / aphid - barley / any other parasite',3,'Award only if the named parasite and named host match.')],
        [region(8,.071,.145)],[region(11,.138,.203)],parasite)
    add('q11aiii','Q11(a)(iii)','4-3-3','3-5','animal-diseases|crop-production','parasite-control-matching',
        'State one way to get rid of the parasite you have named.',
        [point('Dosing / spray / fungicide / pesticide / insecticide / antibiotics / drainage / biological control',3,'Method of removal must match your named parasite; the options are not interchangeable.')],
        [region(8,.071,.145)],[region(11,.2,.254)],parasite+' Name a parasite and its crop or livestock host before giving a suitable control; naming marks belong to part (ii).')
    c=add('q11b','Q11(b)','4-2','3-1','classification-of-organisms','insect-life-cycle',
        'With the aid of a labelled diagram, describe the life cycle of a named insect.',
        [point('(Cabbage white) butterfly / clickbeetle / cranefly / (house)fly',3,'Name an insect appropriate to the cycle.'),
         point('Diagram',3,'Award 3 or 0; the lifecycle stages must be in an acceptable sequence.','criterion'),
         menu('Egg|larva or named larva|pupa or chrysalis or cocoon|adult or imago',[2,2,2],'Any three correct labels.')],
        [region(8,.151,.183)],[region(11,.255,.581)],selection={'kind':'open','reason':'A named insect is an open choice. The scheme’s two lifecycle types are accepted examples, not two finite examination routes.'})
    variants(c,[('complete','Complete metamorphosis',c['rows']),('incomplete','Incomplete metamorphosis',
        [point('Greenfly or aphid / locust',3,'Name an insect appropriate to this cycle.'),point('Diagram',3,'Award 3 or 0 only if all stages are in an acceptable sequence.','criterion'),
         point('Egg',2,'Label'),point('nymph',2,'Label'),point('adult',2,'Label')])])
    cultivation=[
        ('i','i','Soil suitability','3-3-1','2-3',8,
         menu('(Sandy) loam soil|brown earth or grey-brown podzolic|good drainage|good aeration|pH 6.0-6.5|crumb structure|fertile',[4,4]),
         menu('Deep soil|(medium) loam|well drained|good aeration|free from stones|pH 5.0-5.5|brown earth or grey-brown podzolic|fertile|grow in wide range of soils',[4,4]),(11,.611,.697),(12,.251,.333)),
        ('ii-date','ii) — date','Sowing date','3-3-1','2-3',4,
         point('September - November (Winter barley) or February - April (Spring barley)',4),point('Jan - May',4),(11,.699,.755),(12,.335,.356)),
        ('ii-method','ii) — method','Sowing method','3-3-1','2-3',4,
         point('sown with a combine drill / seed drill / one pass',4),point('Potato planter / sow (plant) in drills or ridges / grow-bags / plant with spade',4),(11,.757,.784),(12,.335,.393)),
        ('iii','iii','Fertilizer used','2-3','1-6',4,
         point('10:10:20 / N,P,K / apply N fertilizer in spring / split application of N',4,'Accept farmyard manure, slurry or relevant organic fertiliser if method and time of incorporation are given, e.g. ploughed into soil in autumn.'),
         point('10-10-20 / 7-6-17 / N,P,K / (farmyard) manure',4,'Other relevant organic fertiliser accepted if method of incorporation into soil is given.'),(11,.786,.862),(12,.395,.453)),
        ('iv','iv','Control of pests','3-3-2','2-4',4,
         point('Certified seed / seed treatment / spray / fungicide / pesticide / resistant varieties / biological control / Autumn ploughing / rotation',4),
         point('(1 in 4) rotation / spray / pesticide / fungicide / slug pellets / earthing up / resistant varieties / certified seed',4),(11,.864,.909),(12,.457,.514)),
        ('v-method','v) — method','Harvesting method','3-3-3','2-5',4,
         point('Combine harvester',4),point('Kill off haulms (with herbicide) / elevator digger / complete potato harvester / dig up with spade (and gather by hand)',4),(12,.079,.107),(12,.517,.575)),
        ('v-time','v) — time','Harvesting time','3-3-3','2-5',4,
         point('Winter barley: July or Spring barley: August - September',4,'Accept signs of ripeness, e.g. grain gets hard or stems turn yellow.'),
         point('First earlies: May - June / Second earlies: July / Maincrop: August - November',4),(12,.109,.168),(12,.577,.635)),
        ('vi','vi','Yield per hectare','3-3-3','2-5',4,
         point('Winter barley: 7-9 tonnes/ha or Spring barley: 5-7 tonnes/ha',4),point('Earlies: 7-10 tonnes/ha or Maincrop: 30-40 tonnes/ha',4),(12,.17,.21),(12,.637,.68)),
    ]
    for key,address,heading,topic,old,total,barley,potato,br,pr in cultivation:
        ref='Q11(c)('+address+(')' if '—' not in address else '')
        for row in [barley,potato]: row['contextNote']=(row.get('contextNote','')+' Match the named crop and its type. Barley and potatoes are scheme examples; other appropriate cereal or root crops remain permitted.').strip()
        c=add('q11c'+key,ref,topic,old,'crop-production','crop-'+key,
            'Describe the cultivation of a cereal or a root crop under this heading: '+heading+'.',[barley],
            [region(8,.185,.313)],[region(*br),region(*pr)],'Name the cereal or root crop whose cultivation you are describing.',
            selection={'kind':'open','reason':'The paper permits open crop categories. Published barley and potato examples are matched marking menus on one task.'})
        assert c['totalMarks']==total
        variants(c,[('barley','Barley',[barley]),('potatoes','Potatoes',[potato])])

    add('q12a-system','Q12(a) — digestive system','4-1','3-0','animal-physiology','monogastric-digestive-system',
        'Draw a labelled diagram of the digestive system of a named monogastric animal.',
        [point('Name of monogastric animal',None,'3 marks for an appropriate named animal.','criterion'),
         point('Diagram',None,'4, 2 or 0 marks. Judge the drawing against the original scheme.','criterion'),
         point('Labels',None,'Four correct labels at 2 marks each. Judge all three criteria and record a total out of 15.','criterion')],
        [region(8,.448,.493)],[region(13,.108,.137)],marks=15)
    add('q12a-enzyme','Q12(a) — enzyme experiment','1-2','0-1|3-0','scientific-practices-experiments-investigations|animal-physiology','digestive-enzyme-experiment',
        'Describe an experiment to investigate the action of one named digestive enzyme.',
        [point('Named enzyme / matching substrate / suitable temperature / water-bath / named product / test for product / mention of control / control explained / result / conclusion',None,
               'Name of enzyme: 3 marks, plus four other relevant points at 3 marks each. All points must form a valid matching experiment. An unlabelled relevant diagram earns at most 3 marks. Use the source criteria to judge the response and record the total.','criterion')],
        [region(8,.448,.493)],[region(13,.139,.234)],marks=15)
    for roman,prompt,pool,sy,topic,old,atlas in [
        ('i','The appearance of earthworms on the surface of a soil following heavy rain.','Waterlogging|gas exchange or explained|respiration or explained',(.257,.284),'2-2-3','1-4','soil-science'),
        ('ii','The feeding of colostrum to a calf in the hours immediately after birth.','Rich in antibodies|highly digestible nutrients or rich in protein and minerals|laxative effect|disease resistance|warms calf',(.286,.331),'4-3-3','3-5','animal-production'),
        ('iii','The conservation of hedgerows.','Habitat for wildlife|shelter for farm animals|food source for wildlife|microclimate for crops|absorb carbon dioxide|produce oxygen|biodiversity|wildlife corridors|boundaries or fences|reduces spread of diseases (in livestock)|REPs|noise reduction',(.331,.391),'3-3-2','1-6','fertilisers-pollution-the-environment'),
        ('iv','The proper storage of hay immediately after drying.','Optimum conditions for storage explained|prevents overheating|prevents rotting',(.391,.436),'3-3-3','2-5','grassland'),
        ('v','The thinning of trees in forest tree production.','Poorest trees removed leaving better trees|remaining trees grow at increased rate|remaining trees grow straighter|remaining trees of better quality e.g. fewer knots in timber|less competition for water or for nutrients or for light|improved access|thinnings used to make useful product(s) or named product',(.436,.511),'3-3-2','2-4','crop-production'),
    ]:
        add('q12b'+roman,f'Q12(b)({roman})',topic,old,atlas,'scientific-explanation-'+roman,
            'Give a scientific explanation for the following: '+prompt,[menu(pool,[3,3],'Two distinct points; equivalent descriptions count once.')],
            [region(8,.497,.608)],[region(13,*sy)])
    milk='Milk is considered to be a basic food requirement for young calves.'
    add('q12ci','Q12(c)(i)','4-1','3-0','animal-physiology','fresh-milk-composition','State the average composition of fresh milk.',
        [menu(['Water 87.5% (87–88%)','total solids 12.5% (12–13%)','butterfat or fat 3.8% (3.5–4%)','SNF 8.7%','Protein 3.1% (3.0–3.5%)','lactose 4.6% (4–5%)','minerals + vitamins 0.8% (0.7–1.0%)'],[3,3,3],'Any three composition points, each with its percentage.')],
        [region(8,.612,.6827)],[region(13,.511,.572)],milk)
    add('q12cii','Q12(c)(ii)','1-2','0-1|3-0','scientific-practices-experiments-investigations|animal-physiology','milk-component-investigation',
        'Describe a laboratory investigation to show the presence of one named component of fresh milk.',
        [point('Named component',None,'3 marks for the component investigated.','criterion'),
         point('Named reagent / procedural point one / procedural point two / mention of control / control explained / result / conclusion',None,
               'Named component: 3 marks, plus any three matching investigation points at 3 marks each. These are assessment criteria, not a model experimental answer. Judge a valid investigation for the named component and record its total.','criterion')],
        [region(8,.612,.6998)],[region(13,.571,.631)],milk,marks=12)
    add('q12ciii','Q12(c)(iii)','4-3-3','3-5','animal-production','milking-parlour-hygiene',
        'How can the dairy farmer prevent contamination of milk in the milking parlour?',
        [menu('Wash udders and teats before milking|parlour hygiene|milker hygiene|check teats for mastitis (using strip cup)|iodine teat dip or spray|wash clusters and milk line|use of filter to remove dirt particles|wash bulk tank|keep milk at a suitable temperature|milk cows with mastitis separately to rest of herd|fly screens',[3,3,3])],
        [region(8,.612,.6998)],[region(13,.631,.707)],milk)
    add('q12di','Q12(d)(i)','3-2','2-1','classification-of-organisms','farm-food-chain',
        'Describe, with the aid of a labelled diagram, a simple food chain as it occurs on a farm.',
        [point('Named producer',3,'A correctly named producer in your farm chain.','criterion'),
         point('named primary consumer',3,'Must feed on the named producer.','criterion'),
         point('named secondary consumer',3,'Must feed on the named primary consumer.','criterion'),
         point('arrows',3,'Arrows must show the direction of transfer along the valid chain.','criterion')],
        [region(8,.71,.82)],[region(13,.706,.78)])
    add('q12dii','Q12(d)(ii)','1-2','0-1|2-6','scientific-practices-experiments-investigations|grassland','pasture-botanical-composition',
        'Describe a field investigation to determine the botanical composition of an old permanent pasture.',
        [menu('Quadrat|throw at random|how random|identification of plant species|how identified|repeat|record plants found|graph|conclusion',[3,3,3,3,3],
              'The quadrat is the scheme example. Explain the procedural details and appropriate results; headings such as “graph” or “conclusion” alone are not a described investigation.')],
        [region(8,.71,.82)],[region(13,.706,.78)])
    add('q12diii','Q12(d)(iii)','3-2','2-1','classification-of-organisms','biodiversity-definition','Explain the term biodiversity.',
        [point('The variety of organisms found in a habitat',3)],[region(8,.71,.82)],[region(13,.783,.809)],
        '2010 was designated by the United Nations as the International Year of Biodiversity.')

    for roman,label,answer,sy in [
        ('i','Alleles','Different forms of the same gene',(.109,.139)),
        ('ii','Clone','A clone is a group of cells or organisms that are genetically identical / individual member of such a group / identical genotype / exact copy of cell or organism',(.139,.198)),
        ('iii','Hybrid vigour','Characteristic shown in the superior offspring of a cross between two (dissimilar) parents',(.199,.244)),
    ]:
        add('q13a'+roman,f'Q13(a)({roman})','4-3-2','3-6','genetics','genetics-term-'+roman,
            'Explain the following term: '+label+'.',[point(answer,3)],[region(9,.039,.102)],[region(14,*sy)])
    barley='In barley, six-row ear type (S) is dominant over two-row ear type (s). A homozygous six-row plant (SS) is crossed with a homozygous two-row plant (ss). The F1 offspring are heterozygous. These offspring are crossed by self pollination to produce F2. Use genotypes in brackets and phenotypes on lines.'
    add('q13b-f1','Q13(b) — F1','4-3-2','3-6','genetics','barley-f1-cross',
        'Copy and complete the first cross: gametes produced by each original parent, genotype of F1 offspring and phenotype of F1 offspring.',
        [point('S',2,'Gamete from SS'),point('s',2,'Gamete from ss'),point('Ss',2,'F1 genotype'),point('six-row ear type',2,'F1 phenotype')],
        [region(9,.103,.323)],[region(14,.274,.362)],barley)
    c=add('q13b-f2','Q13(b) — F2','4-3-2','3-6','genetics','barley-f2-cross',
        'Copy and complete the second cross: genotypes of the second-generation parents, gametes produced by each parent, F2 genotypes and F2 phenotypes.',
        [menu(['Ss','Ss'],[2,2],'First checkbox: first parent. Second checkbox: second parent. Both genotypes are required.'),
         menu(['S','s'],[2,2],'First parent’s two gametes. Complete the second parent’s gametes too; they are unstarred and carry no separate marks.'),
         menu(['SS','Ss','Ss','ss'],[2,2,2,2],'The four checkboxes correspond to the four F2 genotype spaces, in printed order. Both separate Ss entries are starred.'),
         menu(['Six-row','Six-row','Two-row'],[2,2,2],'The three starred phenotype entries correspond to SS, Ss and ss. Complete both repeated Ss phenotype spaces, but only one is starred and paid.')],
        [region(9,.103,.21),region(9,.329,.455)],[region(14,.37,.5)],barley,
        illustrated=True)
    c['rows'][0]['contextNote']+=' Complete both parents’ S and s gametes, but the scheme stars and pays only one parent’s two gamete entries. Total: eleven starred entries at two marks each.'
    cross='Show a cross between a two-row barley parent (ss) and an F1 individual (Ss) from SS × ss. Six-row ear type (S) is dominant over two-row ear type (s).'
    for roman,label,rows in [
        ('i','the genotypes of the parents',[point('ss',1,'Two-row parent'),point('Ss',1,'F1 individual')]),
        ('ii','the genotypes of the gametes',[point('s',1,'Gamete from ss parent'),point('S',1,'One gamete from Ss parent'),point('s',1,'Other gamete from Ss parent')]),
        ('iii','the genotypes and the phenotypes of the offspring of the cross',[point('Ss',1,'First offspring genotype'),point('ss',1,'Second offspring genotype'),point('Six-row',1,'Ss phenotype'),point('Two-row',1,'ss phenotype')]),
    ]:
        add('q13c'+roman,f'Q13(c)({roman})','4-3-2','3-6','genetics','barley-testcross-'+roman,
            'In your cross show '+label+'.',rows,[region(9,.103,.21),region(9,.463,.574)],[region(14,.53,.663)],cross)
    for roman,question,answer in [
        ('i','Which diagram, A or B, represents meiosis?','B'),('ii','Which diagram has haploid cells?','B'),
        ('iii','What is the main difference between a haploid cell and a diploid cell?','Haploid: half the number of chromosomes / n / chromosomes that exist singly; Diploid: pairs of chromosomes / 2n'),
        ('iv','Where in an animal’s body would you expect to find haploid cells?','Ovary / testis / sex organs / gonads'),
    ]:
        c=add('q13d'+roman,f'Q13(d)({roman})','4-3-2','3-6','genetics','cell-division-'+roman,question,[point(answer,3)],
            [region(9,.578,.942)],[region(14,.695,.815)],'Mitosis and meiosis are two types of cell division presented in diagrams A and B on the official page.',illustrated=True)
        c['figureKey']='agsci-2011-ol-paper-cell-division'
    for task in tasks:
        key=task['cardIds'][0].removeprefix('agsci-2011-ol-')
        if key.startswith('q11c') and key!='q11ci':
            br,pr=task['schemeRegions']
            task['schemeRegions']=[region(11,.611,.638),br,region(12,.25,.277),pr]
            task['schemePage']=task['schemeRegions'][0]['p']
    bacteria=next(c for c in cards if c['id']=='agsci-2011-ol-q7b')
    bacteria['curriculumNodeIds']=['agricultural-science-1-4','agricultural-science-2-5','agricultural-science-3-0']
    bacteria['additionalTopicIds']=['agsci-3-3-3','agsci-4-1']
    assert len(cards)==81
    assert len({c['id'] for c in cards})==81
    return cards,tasks
