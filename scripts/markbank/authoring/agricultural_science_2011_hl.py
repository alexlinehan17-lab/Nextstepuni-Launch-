"""2011 Higher: original-paper and marking-scheme review, not parser output.

All 8 paper and 16 scheme PDF pages visually inspected on 7 October 2026.
The shared dihybrid-cross award is separate from its three ratio answers.
Question 8(c)'s three-of-four comparisons expand to four complete routes.
"""
import hashlib
from itertools import combinations
import fitz
from agricultural_science_2010_hl import ROOT, point, menu, region

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers':'19975eb5d04e868becd63819eb5a3325929f6c774cff8e6abd4b72a1d3fb4ed9',
          'markingschemes':'9979d05e915b789dd55e9ac742066987f4b26c75820485b15b1436ed5d06e9ba'}
SELECTIONS = {
    'ec78d4ad8f7de622':('independent-task-selection','Q1 selects six of ten independently marked lettered parts. Every part is retained; (b), (g) and (h) split at fixed roman-part awards. No exam-submission bundles.'),
    '07570960ab2faac4':('independent-task-selection','Q4 selects two independently priced 24-mark experiments. All four are separate practice tasks; open methods are marking menus, not a finite printed pool.'),
    '2843749efe6a5ae7':('independent-task-selection','Q8 selects two 24-mark parts. All are retained, including the internal closed pool in (c).'),
    '91da40e393d25b3c':('closed','Q8(c) prints four comparison pairs and asks for three. All four combinations retain three complete eight-mark comparisons.'),
    '29f5b0a7725b0396':('independent-task-selection','Q9 selects four independently marked twelve-mark explanations. All five are retained.'),
}


def paper_review():
    from agricultural_science_inventory import DIRECTIVE
    pages = {}
    for kind,digest in HASHES.items():
        path = ROOT / f'paper-trail-corpus/{kind}/2011/{FILE}'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest, f'Source changed: {path}'
        with fitz.open(path) as pdf:
            pages[kind] = [' '.join(p.get_text().split()) for p in pdf]
    observed = []
    for i,text in enumerate(pages['exampapers']):
        for match in DIRECTIVE.finditer(text):
            context = text[max(0,match.start()-90):match.end()+230]
            key = hashlib.sha256(f'{HASHES["exampapers"]}|{i+1}|{match.start()}|{context}'.encode()).hexdigest()[:16]
            assert key in SELECTIONS, f'Unclassified selection: {key} {context}'
            kind,reason = SELECTIONS[key]
            observed.append(dict(id=key,page=i+1,cue=match.group(),context=context,classification=kind,reason=reason))
    assert {c['id'] for c in observed}==set(SELECTIONS), 'Stale selection classification'
    supplementary = [
        (1,'SIX QUESTIONS TO BE ANSWERED','exam-selection','Outer exam selection; do not combine unrelated tasks into new cards.'),
        (3,'OR Option Two','closed','Both Q3 options are retained with distinct addresses and their own task boundaries.'),
        (3,'laboratory or field experiment','open','An experimental setting, not a finite list of experiments beyond the four separately priced parts.'),
        (5,'Explain each of the following terms:','required-headings','Q7(a) requires all three terms, each separately awarded four marks; no choose-three route.'),
    ]
    for page,text,_,_ in supplementary:
        assert pages['exampapers'][page-1].count(text)==1, f'Stale supplementary cue: {text}'
    return dict(year=2011,level='higher',lang='ev',paperFileid=FILE,hashes=HASHES,
                wholePaperVisualReview='reviewed',schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1,9)),schemePagesInspected=list(range(1,17)),
                selectionDirectives=observed,
                supplementarySelections=[dict(page=p,wording=w,classification=c,reason=r) for p,w,c,r in supplementary],
                taskCountsByQuestion={'Q1':13,'Q2':7,'Q3 Option One':5,'Q3 Option Two':6,'Q4':4,'Q5':7,'Q6':6,'Q7':8,'Q8':9,'Q9':5},
                independentBoundaryReview='67 base tasks, 70 finite routes. Q7(b) has 12 marks for the shared cross and three separate 4-mark ratios. Diagram labels remain one exercise. Q3 Option Two (c)(ii) has separately priced advantages and disadvantages.',
                remaining=['Full application navigation review','Corpus-wide reconciliation'])


def variants(card,choices):
    card['answerVariants'] = [dict(id=k,label=label,rows=[dict(r,id=f'r-{i+1}') for i,r in enumerate(rows)]) for k,label,rows in choices]
    card['rows'] = card['answerVariants'][0]['rows']


def reviewed_tasks():
    paper_review()
    cards,tasks = [],[]

    def add(key,ref,topic,old,atlas,concept,question,rows,paper,scheme,stem=None,selection=None):
        cid = 'agsci-2011-hl-'+key
        card = dict(id=cid,subjectId='agricultural-science',year=2011,level='higher',
                    section='A' if key.startswith('q1') else 'B',questionRef='2011 HL '+ref,
                    topicId='agsci-'+topic,curriculumNodeIds=['agricultural-science-'+old],conceptId=concept,
                    questionText=question,tariffModel={'kind':'fixed'},totalMarks=sum(r['marks'] for r in rows),
                    rows=[dict(r,id=f'r-{i+1}') for i,r in enumerate(rows)],
                    sourceMaterial=dict(kind='source-text',label='OFFICIAL QUESTION PAGE',
                        title='Agricultural Science 2011 Higher — '+ref,pages=sorted({r['p'] for r in paper}),
                        attribution='SEC Agricultural Science 2011 Higher Level examination paper — © State Examinations Commission.',
                        presentationNote='Open the original page for the published wording, diagrams and examination context.'))
        if stem: card['stem'] = stem
        cards.append(card)
        tasks.append(dict(questionRef=card['questionRef'],paperPage=paper[0]['p'],schemePage=scheme[0]['p'],
                          paperRegions=paper,schemeRegions=scheme,atlasNumbers={cid:str(1000+len(cards))},
                          selection=selection or {'kind':'none','reason':'No finite response choice. Open named examples and scheme alternatives remain marking menus.'},
                          cardIds=[cid],marksPerRoute=card['totalMarks'],
                          examTopicIds=['agricultural-science-higher-'+t for t in atlas.split('|')],
                          evidence='All 8 paper and 16 scheme pages visually inspected. Published boundaries and tariffs checked; no automatic question-parser denominator.'))
        return card

    rosacea='large flowers|parts in 5s|Rose/apple etc.'
    crucifer='parts in 4s|cross shaped|cabbage, kale, oilseed rape etc.'
    c=add('q1a','Q1(a)','3-2','2-1','classification-of-animals-plants','flower-family-comparison',
        'Compare the structure of the flowers of named examples from the Rosaceae and the Cruciferae families.',
        [menu(rosacea,[3,2],'Rosaceae: allow a labelled diagram.'),menu(crucifer,[3,2],'Cruciferae: allow a labelled diagram.')],
        [region(2,.082,.12)],[region(5,.114,.209)])
    variants(c,[(k,label,[menu(rosacea+('|insect pollinated' if family=='rosaceae' else ''),[3,2],'Rosaceae: two points; a labelled diagram is accepted.'),
                         menu(crucifer+('|insect pollinated' if family=='cruciferae' else ''),[3,2],'Cruciferae: two points. Insect pollination can be credited for only one family.')])
                for k,label,family in [('structure','Structural points and examples','none'),('rosaceae-pollination','Pollination credited for Rosaceae','rosaceae'),('cruciferae-pollination','Pollination credited for Cruciferae','cruciferae')]])
    add('q1bi','Q1(b)(i)','4-3-1','3-3','dairy-cattle','cow-condition-scoring',
        'What is meant by condition scoring in cows?', [point('(ratio of) lean to fat on animals body / correct scale / feeling (by hand) along back',4)],
        [region(2,.131,.15)],[region(5,.208,.282)])
    add('q1bii','Q1(b)(ii)','4-3-1','3-3','dairy-cattle','cow-condition-score-targets',
        'Give the recommended condition scores for a dairy cow at service and at calving.',[point('Service 2–3',3),point('Calving 2.5–3.5',3)],
        [region(2,.146,.165)],[region(5,.208,.282)])
    add('q1c','Q1(c)','4-3-3','3-5','animal-diseases','active-passive-immunity',
        'Explain the difference between active and passive immunity and give one example of each from agriculture.',
        [menu(['Active = body manufactures antibodies to particular antigen','through contact e.g. virus/bacterium/exposure to vaccine/TB test'],[3,2],'Active immunity: explanation and example. The first correct point earns three marks.'),
         menu(['Passive = immunity is passed on','e.g. colostrum/or across placenta'],[3,2],'Passive immunity: explanation and example. The first correct point earns three marks.')],
        [region(2,.176,.21)],[region(5,.282,.361)])
    add('q1d','Q1(d)','2-2-3','1-4','soil-science','increasing-earthworm-populations',
        'List three practices that would increase the population of earthworms in farmland.',
        [menu('adding lime/suitable pH|adding organic matter|draining wet land|aerating soil (by cultivations)',[8,1,1])],
        [region(2,.222,.241)],[region(5,.361,.409)])
    germ='use certified seed|warm conditions|good seed bed|moisture'
    establish='don’t sow too deep|pest control|weed control|fertilising|crop rotation|rolling'
    c=add('q1e','Q1(e)','3-3-1','2-3','crop-production','germination-and-establishment',
        'Describe how a farmer provides for optimal seed germination and crop establishment.',
        [menu(germ,[8],'Germination: at least one point.'),menu(establish,[1,1],'Establishment: at least one point.')],
        [region(2,.25,.27)],[region(5,.409,.519)])
    variants(c,[(f'g{g}-first-{first}',f'{g} germination + {3-g} establishment; first point from {first}',
                 [menu(germ,([8]+[1]*(g-1)) if first=='germination' else [1]*g,'Germination points.'),
                  menu(establish,([8]+[1]*(2-g)) if first=='establishment' else [1]*(3-g),'Establishment points.')])
                for g in [1,2] for first in ['germination','establishment']])
    add('q1f','Q1(f)','3-1','2-0','plant-physiology','grass-carbohydrates',
        'Name one monosaccharide and one polysaccharide found in grass and list the three main elements found in these compounds.',
        [menu(['Mono: glucose (or named mono.)','Poly: starch/cellulose'],[4,3],'One answer from each carbohydrate class; the first correct name earns four marks.'),
         point('Carbon',1),point('Hydrogen',1),point('Oxygen',1)],
        [region(2,.28,.316)],[region(5,.518,.56)])
    add('q1gi','Q1(g)(i)','4-2','3-1','classification-of-animals-plants|animal-diseases','parasite-phyla-examples',
        'Name one member of each of the phyla Platyhelminthes and Arthropoda.',
        [point('Platys: liverfluke/tapeworm',2),point('Arthropoda: ticks/lice/warble fly',2)],
        [region(2,.324,.344)],[region(5,.56,.607)])
    add('q1gii','Q1(g)(ii)','4-3-3','3-5','animal-diseases','parasite-disease-matching',
        'Identify one disease of cattle caused by each member of the phyla you have named.',
        [point('Platy: liver damage/not thriving',3,'Must match the named member.'),point('Arthropoda: infection/ eating flesh/ irritation (disease must match named example), accept redwater disease for tick',3,'Must match the named member.')],
        [region(2,.324,.363)],[region(5,.607,.68)],'Name one member of Platyhelminthes and one of Arthropoda, then match a cattle disease to each. The naming marks belong to part (i).')
    add('q1hi','Q1(h)(i)','4-2','3-1','classification-of-animals-plants','symbiosis-definition',
        'Explain the term symbiosis.',[point('accept biology def /2 organisms living together each benefits',4)],
        [region(2,.371,.389)],[region(5,.68,.799)])
    add('q1hii','Q1(h)(ii)','4-2','3-1','classification-of-animals-plants|soil-science','agricultural-symbiosis-examples',
        'Give two examples of symbiosis from agriculture.',
        [menu('Rhizobium (or N-fixing bacteria) in clover|birds eating lice and ticks on cattle|microbes in rumen|any parasite example',[3,3],
              'The historical scheme accepts parasitism under the broader meaning of symbiosis. Mutualism is the form in which both organisms benefit.')],
        [region(2,.386,.404)],[region(5,.68,.799)])
    add('q1i','Q1(i)','2-1','1-0','soil-science|scientific-practices-experiments-investigations','limestone-parent-material-test',
        'Describe how you would identify limestone as a parent material in a soil.',
        [menu('Add acid to sample|bubbles|CO2|test for CO2|indicate carbonates',[4,3,3])],
        [region(2,.414,.435)],[region(5,.799,.828)])
    add('q1j','Q1(j)','3-1','2-0','plant-physiology','stolon-rhizome-comparison',
        'Distinguish between a stolon (runner) and a rhizome and give one example of each from agriculture.',
        [menu(['Stolon: above ground horizontal stem/with buds for new plants','Strawberries/clover/buttercup etc.'],[3,2],'Stolon: explanation and example. The first correct point earns three marks.'),
         menu(['Rhizome: underground modified stem/stores food/pieces with buds can reproduce','scutch/iris/…'],[3,2],'Rhizome: explanation and example. The first correct point earns three marks.')],
        [region(2,.444,.479)],[region(5,.828,.907)])

    for key,question,pool,py,sy in [
        ('i','Name one type of soil pan.','plough/iron/compaction (hard pan)',(.565,.584),(.085,.114)),
        ('ii','Outline how the named soil pan is formed.','continuous tillage ploughing same depth/iron (oxides) washed down/leached from A to B horizon/using heavy machinery/not using low ground pressure tyres',(.58,.6),(.114,.18)),
        ('iii','State one problem associated with the named soil pan.','hard/impervious layer/poor drainage/poor growth/poor germination/restrict root penetration',(.595,.616),(.18,.227)),
        ('iv','Say how the named soil pan could be removed.','deep ploughing/not ploughing at the same depth in successive years/subsoiling/ripping/forestry plough',(.61,.631),(.226,.275)),
    ]:
        add('q2a'+key,f'Q2(a)({key})','2-2-2','1-3','soil-science','soil-pan-'+key,question,[point(pool,4,'The answer must be appropriate to the soil pan you name.')],
            [region(2,*py)],[region(6,*sy)],None if key=='i' else 'Name a soil pan (for example a plough pan, iron pan or compaction pan) and answer for that same pan. Naming marks are allocated in part (i).')
    add('q2bi','Q2(b)(i)','2-1','1-0','soil-science','gleisation-and-soil-profile',
        'Describe gleisation and its role in the development of a soil profile.',
        [point('high rainfall/low lying area/waterlogged/acid reacts with iron/low bacterial activity/low level decomposition',4,'Gleisation conditions/process.'),
         point('Peat accumulates on top/streaks mottling in B horizon/subsoil blue grey colour or grey',4,'Effect on the soil profile.')],
        [region(2,.641,.662)],[region(6,.275,.386)])
    add('q2bii','Q2(b)(ii)','2-3','1-6','soil-science|scientific-practices-experiments-investigations','soil-sampling-factors',
        'Explain the factors to be considered when collecting soil samples for analysis.',
        [menu('Check field colour differences|old hedges etc.|W-shaped pattern in collecting|avoid headlands/gateways/under trees/beside watercourses|collect from top 7.5–15 cm|repeated sampling|field history|topography',[4,2,2])],
        [region(2,.656,.678)],[region(6,.386,.477)])
    nitrogen_common='Place a sample of soil in flask|add distilled water|shake|filter|collect filtrate'
    c=add('q2c','Q2(c)','2-3','1-6','soil-science|scientific-practices-experiments-investigations','soil-nitrogen-experiment',
        'Describe an experiment to investigate the presence of nitrogen in a soil sample.',
        [menu(nitrogen_common+'|add diphenylamine soln|blue ppt is (positive for N)',[4]*4)],
        [region(2,.686,.712)],[region(6,.477,.56)])
    variants(c,[(k,label,[menu(nitrogen_common+'|'+pool,[4]*4,'Credit four points from one coherent method; accept reference to a colour chart.')]) for k,label,pool in [
        ('diphenylamine','Diphenylamine test','add diphenylamine soln|blue ppt is (positive for N)'),
        ('brown-ring','Brown-ring test','add iron sulphate|add sulphuric acid|brown ring formed')]])

    summer='involves using all the grazing to finish cattle|no hay or silage saved|little labour required|no housing|little or no concentrates|low cost'
    winter='most of grass is made into silage|housing required|meal feeding needed|high labour requirement'
    c=add('q3o1a','Q3 Option One (a)','4-3-1','3-3','beef-cattle','beef-finishing-systems',
        'Compare summer grazing and winter fattening as systems for finishing beef animals.',
        [menu(summer,[4]),menu(winter,[4]*3)], [region(3,.031,.08)],[region(7,.085,.244)])
    variants(c,[(f'summer-{n}',f'{n} summer + {4-n} winter points',[menu(summer,[4]*n,'At least one summer point; only one cost comparison.'),menu(winter,[4]*(4-n),'At least one winter point.')]) for n in [1,2,3]])
    add('q3o1b','Q3 Option One (b)','4-3-2','3-6','dairy-cattle','selecting-dairy-replacements',
        'Describe four qualities a farmer would look for when selecting replacement heifers for a dairy herd.',
        [menu('good teeth|feet|udder 4 teats|fertility|high milk yield|good conformation|comes from good EBI bull|come from good mother that is prolific/good milker|docile|disease free (or healthy)|correct condition score|dairy breed or named|easy calving',[4]*4)],
        [region(3,.091,.111)],[region(7,.244,.343)])
    fce_stem='Food Conversion Efficiency (FCE) decreases with age in farm animals.'
    add('q3o1ci','Q3 Option One (c)(i)','4-1','3-0','animal-physiology-digestive-system','food-conversion-efficiency',
        'Explain Food Conversion Efficiency (FCE) and give an example of FCE for a named farm animal.',
        [point('how efficiently an animal converts food consumed into weight gained/food to flesh/can be expressed as ratio',4),
         point('pigs 1.75–3.25:1; cattle/sheep 8:1; poultry 2:1 (accept first number)',4,'Name an animal and give its matching ratio.')],
        [region(3,.123,.17)],[region(7,.343,.423)],fce_stem)
    add('q3o1cii','Q3 Option One (c)(ii)','4-1','3-0','animal-physiology-digestive-system','age-and-food-conversion',
        'Explain why FCE decreases with age in an animal.',
        [point('Body tissues develop in order/nerve-bone-muscle-fat/fat deposition increases with age/e.g. 24 months in cattle/depends on breed/the younger the animal the less fat it forms and more lean/fat less efficiently produced',4)],
        [region(3,.123,.143),region(3,.165,.188)],[region(7,.423,.488)],fce_stem)
    add('q3o1ciii','Q3 Option One (c)(iii)','4-1','3-0','animal-physiology-digestive-system','improving-food-conversion',
        'Explain how a farmer might improve the FCE of his herd.',
        [point('changing high quality diet/increase concentrates/less roughage/buy in new animals/breeding/disease control/housing/high temperature for pigs',4)],
        [region(3,.123,.143),region(3,.183,.205)],[region(7,.488,.555)],fce_stem)
    add('q3o2a','Q3 Option Two (a)','3-3-2','2-6','grassland','high-quality-silage-management',
        'Describe four grassland management practices used to achieve high quality silage.',
        [menu('use high quality species of ryegrass or clover|fertilise|close for min.6 weeks|cut at leafy stage or high DMD or heading-out (stage)|reseed frequently|remove weeds|lime|drain|named grazing system',[6,4,3,3])],
        [region(3,.267,.314)],[region(7,.582,.695)])
    add('q3o2bi','Q3 Option Two (b)(i)','4-1','3-0','animal-physiology-digestive-system|animal-diseases','colostrum-first-day',
        'Explain why a young animal should receive colostrum in the first day of life.',
        [point('intestine changes after 24 hours/antibodies absorbed',2)],
        [region(3,.332,.353)],[region(7,.695,.782)])
    add('q3o2bii','Q3 Option Two (b)(ii)','4-1','3-0','animal-physiology-digestive-system|animal-diseases','colostrum-benefits',
        'List three benefits of colostrum to the young animal.',
        [menu('Nutritious|laxative|good start in life|antibodies/immunity|warming|easily digested',[8,3,3])],
        [region(3,.349,.367)],[region(7,.695,.782)])
    add('q3o2ci','Q3 Option Two (c)(i)','3-3-2','2-6','grassland','strip-grazing-features',
        'Outline the main features of strip-grazing.',[menu('a moveable electric fence|advanced each day|back fence|moveable water supply',[3,1])],
        [region(3,.379,.397)],[region(7,.782,.822)])
    for key,label,pool,sy in [
        ('advantages','advantages','cheap|get fresh material each day|better utilisation of crop|avoids frost damage|better L.W.G.',(.819,.858)),
        ('disadvantages','disadvantages','damage to soil structure|pollution|dirty|runback for animals|footrot/disease|teeth damage from stones|labour intensive',(.856,.904)),
    ]:
        add('q3o2cii-'+key,'Q3 Option Two (c)(ii) — '+key,'3-3-2','2-6','grassland|sheep','strip-grazing-'+key,
            f'Give two {label} of strip grazing in the feeding of fodder roots to sheep.',[menu(pool,[4,2])],
            [region(3,.394,.424)],[region(7,*sy)],'Part (c)(ii) asks for two advantages and two disadvantages; this practice task covers the separately marked '+label+'.')

    experiments = [
        ('a','3-3-2','2-4','crop-production','potato-dry-matter','to determine the dry matter content of different potato varieties',
         'Take 2 or more different varieties or named|chop into small pieces|weigh crucibles|weigh wet potato samples in crucibles|place in drying oven|@100 degrees|leave|reweigh at intervals|when no further weight loss|calculate % dry matter|new weight divided by old weight x100=% d.m.',(.502,.521),(.11,.212)),
        ('b','4-3-1','3-3','dairy-cattle','milk-hygienic-quality','to determine the hygienic quality of milk',
         'Place in sterile test tubes|add 1 ml resazurin soln (methylene blue)|stopper|shake|incubate|at 37 degrees|for 10 mins|note colour change|blue (best)|pink (poor)|white (worst)',(.529,.549),(.212,.327)),
        ('c','2-2-2','1-3','soil-science','soil-flocculation','to demonstrate soil flocculation',
         'Get 2 suitable vessels|put soil and water in each|equal amounts|add lime to one or correct flocculant|shake both|allow to settle|control remains muddy|limed sample settles quickly|demonstrating flocculation',(.559,.578),(.327,.409)),
        ('d','3-3-2','2-6','grassland','grazing-botanical-composition','to demonstrate the effects of grazing on the botanical composition of grassland',
         'Block off area|with cage or similar|to let rain and light in|keep stock out|allow rest of field to be grazed normally|observe over period|note composition inside and outside wire|use a line transect/quadrat|a number of times|at random|use identification key|weeds flourish inside (correct conclusion)',(.588,.609),(.409,.508)),
    ]
    for key,topic,old,atlas,concept,question,pool,py,sy in experiments:
        c=add('q4'+key,f'Q4({key})',topic,old,atlas+'|scientific-practices-experiments-investigations',concept,
            'Describe a laboratory or field experiment '+question+'.',[menu(pool,[4]*6)],
            [region(3,.473,.493),region(3,*py)],[region(8,*sy)],'Q4 asks for two experiments. This task practises part ('+key+'), worth 24 marks.')
        if key=='b':
            agar='two sterile agar plates|one inoculated with milk|using a sterile loop|control|seal|incubate|inverted position|at 37 degrees|24 hours or more|colonies in one, none in control'
            variants(c,[('dye','Dye test',[menu(pool,[4]*6)]),('agar','Agar plates',[menu(agar,[4]*6)])])
    for key,question,pool,py,sy in [
        ('i','Name the disease caused by a lack of iron in the diet of an animal.','Anaemia',(.047,.065),(.535,.566)),
        ('ii','Discuss the role of iron in the blood.','Haemoglobin molecule/haem group has iron at its centre/transports oxygen',(.062,.081),(.566,.614)),
        ('iii','Mention one way of preventing iron deficiency in livestock.','Balanced diet containing iron/inject/as part of ration (pigs and poultry)/iron dextrose injection of pigs/allowing pigs access to soil/lick/animals on grass (greens)',(.077,.096),(.614,.678)),
    ]:
        add('q5a'+key,f'Q5(a)({key})','4-1','3-0','animal-physiology-digestive-system|animal-diseases','iron-'+key,question,[point(pool,4)],
            [region(4,*py)],[region(8,*sy)])
    heart=[region(4,.108,.388)]
    for key,question,answers,py,sy in [
        ('i','Name the parts labelled A, B, C, D.',[('A','septum'),('B','right ventricle'),('C','bicuspid valve'),('D','Vena cava')],(.468,.487),(.678,.733)),
        ('ii','State the destination of the blood flowing 1. in X 2. in Y.',[('X','body (or named part)'),('Y','lungs')],(.484,.532),(.733,.764)),
        ('iii','State the key characteristic of the blood 1. in X 2. in Y.',[('X','oxyhaemoglobin/bright/oxygenated'),('Y','deoxyhaemoglobin/dark/deoxygenated')],(.53,.578),(.764,.823)),
    ]:
        c=add('q5b'+key,f'Q5(b)({key})','4-1','3-0','animal-physiology-circulatory-system','heart-'+key,question,
            [point(answer,4,'Label '+label+'.') for label,answer in answers],heart+[region(4,*py)],[region(8,*sy)],'The original diagram shows a dissected mammalian heart.')
        c['figureKey']='agsci-2011-hl-paper-heart'
        c['labelKey']=[dict(letter=l,meaning=m,askedInThisQuestion=True) for l,m in answers]
    add('q5c','Q5(c)','4-3-3','3-5','animal-diseases','redwater-urine-colour',
        'Explain the reason for the red colour of the urine.',[point('Haemoglobin in urine/cell or red cell bursts/blood in urine',4)],
        [region(4,.6,.649)],[region(8,.823,.855)],'Red water fever in cattle is caused by a parasite. One symptom is that an affected animal’s urine turns red.')
    add('q6a','Q6(a)','3-3-2','2-4','crop-production','cereal-ripeness',
        'Describe four signs of ripeness in a cereal.',
        [menu('Crop is bleached (yellow)|seed (grain) is hard|ear is drooped parallel to stem|flag leaves at top are dead|grain is easily dislodged|moisture % is low (about 15 or less) or dry',[4]*4)],
        [region(4,.742,.763)],[region(9,.085,.15)])
    for key,label,pool,py,sy in [
        ('i','Soil type','Malting: light/medium/sandy loam (less moisture retention), grey brown podzol|Feeding: heavy loam (more moisture retention), brown earth',(.788,.808),(.15,.2)),
        ('ii','Rotation','Malting: needs low N in soil|no grass or other green crop in previous years|pest control (allow once only)|Feeding: no rotation necessary/continuous sowing possible',(.803,.822),(.226,.28)),
        ('iii','Fertilizer regime','Malting: needs low N|for low protein|high sugar in grain|Feed barley needs high N in soil|for high protein in grain',(.818,.836),(.28,.314)),
        ('iv','End use','Malting for brewing/distilling|Feed; for ration manufacture/animal feed',(.832,.852),(.314,.357)),
    ]:
        add('q6b'+key,f'Q6(b)({key})','3-3-2','2-4','crop-production','barley-'+key,
            'Compare the growing of malting barley and feeding barley under the heading: '+label+'.',
            [menu(pool,[4,2],'Two correct points for this heading. Keep the crop association explicit; the first correct point earns four marks.')],
            [region(4,.766,.786),region(4,*py)],[region(9,*sy)])
    c=add('q6c','Q6(c)','3-1','2-0','plant-physiology|crop-production','cereal-grain-longitudinal-section',
        'Draw a labelled diagram to show the main structures of a cereal grain in longitudinal section.',
        [point('Diagram: 4, 2 or 0',4,'Use the published diagram bands. The scheme does not define the intermediate band in words.', 'criterion'),
         menu('Testa (pericarp)|endosperm|cotyledon (one)|coleoptile|plumule|radicle|coleorhiza|aleurone layer',[1]*4,'Four correctly placed labels.')],
        [region(4,.858,.881)],[region(9,.387,.467)])
    # The point renderer has no quality-band control. Keep the drawing's
    # 4/2/0 award and four label marks visible in a manual total instead of
    # turning a four-mark checkbox into an all-or-nothing drawing score.
    c['tariffModel']={'kind':'questionTotal'}
    c['rows']=[dict(id='drawing',kind='criterion',verbatim='Testa(pericarp)/endosperm/cotyledon (one)/coleoptile/plumule/radicle/coleorhiza/aleurone layer. Diagram = 4,2,0 plus 4x1 labels',marks=None,
                   contextNote='The scheme awards 4, 2 or 0 for the diagram. It does not define the intermediate quality band in words. Combine this award with up to four label marks, for a maximum of 8.'),
               dict(id='labels',kind='criterion',verbatim='Testa (pericarp) / endosperm / cotyledon (one) / coleoptile / plumule / radicle / coleorhiza / aleurone layer',marks=None,
                    contextNote='Award one mark per correctly placed label, up to four marks.')]

    terms=[('i','Interphase','before prophase/a resting stage before or after cell divisions/between meiosis 1 and meiosis 2/between meioses (cell divisions)/cell organelles duplicate',(.099,.15)),
           ('ii','Haploid','condition where cell contain half the usual no of chromosomes/1 copy of each chromosome/1 set of chromosomes/23 chromosomes in man/n',(.178,.227)),
           ('iii','Inbreeding','allowing related animals to breed',(.225,.256))]
    for key,term,answer,sy in terms:
        add('q7a'+key,f'Q7(a)({key})','4-3-2','3-6','genetics',term.lower()+'-definition','Explain the term '+term+'.',
            [point(answer,4,'Interphase includes growth and DNA replication before division. There is no second round of DNA replication between meiosis I and II.' if key=='i' else None)],
            [region(5,.029,.101)],[region(10,*sy)])
    maize='A maize plant, heterozygous for the recessive alleles hairless tassel (h) and short anther (l), is self-fertilised and the seeds are collected. The genes for tassel type and anther length are not linked.'
    c=add('q7b-cross','Q7(b) — cross','4-3-2','3-6','genetics','maize-dihybrid-cross',
        'Use a cross to illustrate the self-fertilisation of this maize plant. Show the parental genotypes and the four gametes from each parent.',
        [point('HhLl',2,'First parent.'),point('HhLl',2,'Second parent.'),
         menu('HL|Hl|hL|hl',[1]*4,'Four gametes from the first parent.'),menu('HL|Hl|hL|hl',[1]*4,'Four gametes from the second parent.')],
        [region(5,.121,.226)],[region(10,.246,.458)],maize+' This task covers the shared cross award. The three offspring proportions are separately marked tasks.')
    c['figureKey']='agsci-2011-hl-scheme-p10-punnett'
    for key,trait,answer,sy in [('i','hairy tassel','12/16',(.449,.474)),('ii','short anther','4/16',(.47,.49)),('iii','hairy tassel and short anther','3/16',(.486,.518))]:
        add('q7b'+key,f'Q7(b)({key})','4-3-2','3-6','genetics','maize-'+trait.replace(' ','-'),
            'What proportion of the offspring would you expect to show '+trait+'?',
            [point(answer,4,'Accept an equivalent fraction or percentage. The scheme accepts the numerator alone when the candidate shows all 16 boxes.')],
            [region(5,.121,.226)],[region(10,*sy)],maize+' Use a cross to obtain the proportion. Its shared construction marks are practised separately.')
    add('q7c','Q7(c)','4-3-2','3-6','genetics','roan-cattle-cross',
        'Use a cross to show how roan coat colour arises from homozygous parents.',
        [point('RR = red',4),point('WW(rr) = white',4),point('RRxWW = RW or RR x rr = Rr',4)],
        [region(5,.241,.279)],[region(10,.54,.591)],'The 2011 paper describes roan coat colour in Shorthorn cattle as incomplete dominance. Use the original paper’s parental colours and show the cross.')
    add('q8a','Q8(a)','4-3-1','3-3','pigs','preparing-sow-for-farrowing',
        'Describe the husbandry practices involved in preparing a sow at the end of gestation for transfer from the dry-sow house to the farrowing house.',
        [menu('One week before farrowing date/around day 108|wash sow|delouse|dose for endoparasites (worms)|vaccinate sow|against erysipelas|clean out farrowing pen area|put sow in farrowing crate|adequate food or water|temp 20 degrees',[4]*6)],
        [region(5,.34,.39)],[region(11,.11,.197)])
    pollution='Name one agricultural pollutant with a high B.O.D., such as milk, slurry, silage effluent or dirty yard water. Use that same pollutant throughout your answer.'
    for key,concept,question,rows,py,sy in [
        ('i','bod-definition','Explain the meaning of the term B.O.D.',[point('Biological (biochemical) oxygen demand/is a measure of the amount of oxygen required by 1 litre of pollutant/bacteria use up oxygen when breaking pollutants down',4)],(.405,.425),(.197,.28)),
        ('ii','high-bod-pollutants','Name one agricultural pollutant with a high B.O.D.',[point('Milk/slurry (FYM)/silage effluent/dirty yard (tank) water',4)],(.42,.441),(.28,.308)),
        ('iii','pollutant-water-quality','Explain how the named pollutant affects water quality.',[menu('Bacteria use up oxygen|decomposition|oxygen levels drop|fish die|eutrophication|algal bloom|toxicity',[4,4])],(.435,.458),(.308,.356)),
        ('iv','pollutant-waste-management','Suggest two key elements of a waste management strategy for the named pollutant.',[menu('ensure dairy waste goes into enclosed waterproof tank|collect dairy washings in a tank with sufficient capacity|ensure rain does not wash slurry onto or off land/off concrete area|which should have a fall towards centre of yard and sump|don’t apply slurry on frozen/wet soils/when rain is expected|have sufficient capacity for slurry tank|wilt silage to reduce effluent|collect effluent in a tank from pit|spread on land in correct conditions',[4,4],'Choose points appropriate to your named pollutant.')],(.451,.476),(.356,.507)),
    ]:
        add('q8b'+key,f'Q8(b)({key})','2-3','1-6','fertilisers-pollution-environment-cycles',concept,question,rows,
            [region(5,*py)],[region(11,*sy)],pollution if key in ['iii','iv'] else None)
    pairs={
        'i':[('Essential amino acids','must be in animal diet/cannot be manufactured by an animal/ruminants don’t need essential amino acids can make their own'),('Non-essential amino acids','can be made by the body/from other nutrients/not needed for growth/in abundant supply')],
        'ii':[('Annual plants','plant grows flowers seeds and dies in 1 growing season/completes lifecycle in one year'),('Biennial plants','plant grows year 1 stores food regrows year 2/flowers seeds and dies in two years/completes lifecycle in two years')],
        'iii':[('Drainage','the removal of excess water (when soil is saturated, flooded)/stops poaching'),('Irrigation','adding water to soil/in times of moisture stress/soil moisture deficit/drought/to stop plants drying up or wilting')],
        'iv':[('Eelworms','nematodes/no legs/non-segmented/roundworms'),('Wireworms','larvae/of clickbeetle/arthropod/legs/segmented or any insect characteristic')],
    }
    pair_topics={'i':('4-1','3-0','animal-physiology-digestive-system'),'ii':('3-2','2-1','classification-of-animals-plants'),'iii':('2-2-2','1-3','soil-science'),'iv':('3-3-2','2-4','crop-production')}
    for selected in combinations(pairs,3):
        topic,old,_=pair_topics[selected[0]]
        c=add('q8c-route-'+'-'.join(selected),'Q8(c) — '+', '.join(selected),topic,old,'|'.join(pair_topics[k][2] for k in selected),'agricultural-comparisons',
            'Highlight the main differences between the members of any three of the following pairs: (i) Essential and non-essential amino acids (ii) Annual and biennial plants (iii) Drainage and irrigation (iv) Eelworms and wireworms.',
            [point(answer,4,label+'.') for k in selected for label,answer in pairs[k]],
            [region(5,.49,.587)],[region(11,.506,.898)],'Practice choice: '+', '.join(selected)+'.',
            {'kind':'closed','choose':3,'options':list(pairs),'route':list(selected)})
        c['additionalTopicIds']=['agsci-'+pair_topics[k][0] for k in selected[1:]]
        c['curriculumNodeIds']=['agricultural-science-'+pair_topics[k][1] for k in selected]
    # The scheme permits three points with at least one from each application;
    # it does not prescribe a fermentation + brewing + baking allocation.
    # A manual total preserves that judgement without manufacturing fixed rows.
    c=add('q9a','Q9(a)','3-1','2-0','plant-physiology','yeast-brewing-baking',
        'Give a scientific explanation for the action of yeast in brewing and baking.',
        [point('anaerobic respiration (fermentation)/production of alcohol/production of CO2',4,'A correct equation may cover the points.'),
         point('alcolhol and CO2 used in brewing',4,'At least one brewing point.'),point('CO2 used to raise bread',4,'At least one baking point.')],
        [region(5,.623,.671)],[region(12,.111,.266)])
    c['tariffModel']={'kind':'questionTotal'}
    c['rows']=[dict(id='explanation',kind='criterion',marks=None,
                   verbatim='Equation may cover all points/anaerobic respiration (fermentation)/production of alcohol/production of CO2/alcolhol and CO2 used in brewing/CO2 used to raise bread',
                   contextNote='Award four marks per correct point, up to three points (12 marks). At least one point must concern brewing and at least one must concern baking. A correct equation may cover multiple points; count each distinct scientific point once.')]
    for key,topic,old,atlas,concept,question,pool,py,sy in [
        ('b','4-3-2','3-6','genetics|dairy-cattle|beef-cattle','progeny-testing','Progeny testing of A.I. bulls.',
         'Calves or offspring are tested|growth rate|FCR|compared with progeny of other bulls|kept under the same conditions|records kept|large statistical sample|very reliable in predicting results of a mating with a particular bull|more reliable than performance test|can predict lift in milk yield/fat or protein increase in a herd',(.678,.7),(.266,.382)),
        ('c','3-3-2','2-4','crop-production','systemic-aphid-control','The use of systemic chemicals to control aphids.',
         'chemicals are absorbed by plants|through stoma|up xylem|down phloem (translocated)|aphids suck sap|ingest chemical|longterm control',(.706,.728),(.382,.458)),
        ('d','2-3','1-6','fertilisers-pollution-environment-cycles|crop-production','crop-trace-element-deficiencies','Trace element deficiencies in crop production.',
         'wrong soil type|deficiency in soil or parent rock|over cultivation|over liming|pH too high|pH too low|soil exhaustion|named example e.g. boron deficiency causes crown rot in beet|incorrect rotation/monoculture|leaching|reclaimed land',(.735,.757),(.458,.573)),
        ('e','4-3-1','3-3','pigs','piglet-creep-temperature','The fact that the creep area for bonhams is kept at a higher temperature than the rest of the farrowing house.',
         'attract bonhams away from sow|avoid being crushed|higher temp too hot for sow|bonhams small lose heat easily|farrowing house 20°C for sows|up to 30* in creep area|attract them to feed',(.764,.798),(.573,.675)),
    ]:
        add('q9'+key,f'Q9({key})',topic,old,atlas,concept,'Give a scientific explanation for: '+question,[menu(pool,[4]*3,
            '“Vascular system” is accepted instead of either xylem or phloem, not as an extra point.' if key=='c' else None)],
            [region(5,.623,.645),region(5,*py)],[region(12,*sy)])
    # Corrections from the rendered crop review. Keep shared award columns and
    # instructions alongside every independently marked task they govern.
    scheme_fixes = {
        'q1f':(5,.515,.571),'q1gi':(5,.573,.618),'q1gii':(5,.62,.683),
        'q1hi':(5,.685,.765),'q1hii':(5,.685,.765),'q1i':(5,.766,.795),'q1j':(5,.796,.9),
        'q2bi':(6,.27,.362),'q2bii':(6,.363,.444),'q2c':(6,.445,.526),
        'q3o1ci':(7,.34,.4),'q3o1cii':(7,.403,.483),'q3o1ciii':(7,.485,.548),
        'q3o2ci':(7,.778,.9),'q3o2cii-advantages':(7,.778,.9),'q3o2cii-disadvantages':(7,.778,.9),
        'q5bi':(8,.675,.818),'q5bii':(8,.675,.818),'q5biii':(8,.675,.818),
        'q6bi':(9,.147,.382),'q6bii':(9,.147,.382),'q6biii':(9,.147,.382),'q6biv':(9,.147,.382),
        'q7ai':(10,.083,.236),'q7aii':(10,.083,.236),'q7aiii':(10,.083,.236),
        'q7b-cross':(10,.24,.441),'q7bi':(10,.444,.526),'q7bii':(10,.444,.526),'q7biii':(10,.444,.526),
        'q9a':(12,.111,.204),'q9b':(12,.234,.347),'q9c':(12,.35,.429),'q9d':(12,.431,.528),'q9e':(12,.53,.61),
    }
    paper_fixes = {
        'q1bi':(2,.131,.165),'q1bii':(2,.131,.165),'q1hi':(2,.371,.404),'q1hii':(2,.371,.404),
        'q2ai':(2,.565,.631),'q2aii':(2,.565,.631),'q2aiii':(2,.565,.631),'q2aiv':(2,.565,.631),
        'q2bi':(2,.639,.678),'q2bii':(2,.639,.678),
        'q2c':(2,.686,.721),
        'q3o1ci':(3,.12,.218),'q3o1cii':(3,.12,.218),'q3o1ciii':(3,.12,.218),
        'q3o2a':(3,.27,.325),'q3o2bi':(3,.33,.37),'q3o2bii':(3,.33,.37),
        'q3o2ci':(3,.375,.443),'q3o2cii-advantages':(3,.375,.443),'q3o2cii-disadvantages':(3,.375,.443),
        'q5ai':(4,.045,.101),'q5aii':(4,.045,.101),'q5aiii':(4,.045,.101),
        'q6bi':(4,.766,.852),'q6bii':(4,.766,.852),'q6biii':(4,.766,.852),'q6biv':(4,.766,.852),
        'q6c':(4,.856,.893),
        'q7ai':(5,.03,.114),'q7aii':(5,.03,.114),'q7aiii':(5,.03,.114),
        'q7b-cross':(5,.12,.235),'q7bi':(5,.12,.235),'q7bii':(5,.12,.235),'q7biii':(5,.12,.235),
        'q7c':(5,.24,.295),'q8a':(5,.36,.431),
        'q8bi':(5,.435,.505),'q8bii':(5,.435,.505),'q8biii':(5,.435,.505),'q8biv':(5,.435,.505),
    }
    for task in tasks:
        key=task['cardIds'][0].removeprefix('agsci-2011-hl-')
        if key in scheme_fixes: task['schemeRegions']=[region(*scheme_fixes[key])]
        if key in paper_fixes: task['paperRegions']=[region(*paper_fixes[key])]
        if key in ['q4a','q4b','q4c','q4d']:
            y={'q4a':(.525,.55),'q4b':(.555,.581),'q4c':(.585,.611),'q4d':(.615,.655)}[key]
            task['paperRegions']=[region(3,.495,.52),region(3,*y)]
        if key.startswith('q8c-route-'): task['paperRegions']=[region(5,.51,.611)]
        if key in ['q9a','q9b','q9c','q9d','q9e']:
            y={'q9a':(.675,.701),'q9b':(.705,.731),'q9c':(.735,.761),'q9d':(.765,.791),'q9e':(.795,.851)}[key]
            task['paperRegions']=[region(5,.645,.672),region(5,*y)]
        if key in ['q4b','q4c','q4d']:
            task['schemeRegions'].append(region(8,.109,.135,.77,.95))
        if key in ['q9b','q9c','q9d','q9e']:
            task['schemeRegions'].append(region(12,.111,.137,.75,.96))
    scientific = {
        'q7ai':('https://openstax.org/books/biology/pages/11-1-the-process-of-meiosis',
                 'The historical scheme calls interphase a resting stage and includes the interval between meiotic divisions. Interphase is active: cells grow and replicate DNA before division. DNA does not replicate again between meiosis I and meiosis II.'),
        'q7c':('https://extension.okstate.edu/fact-sheets/color-patterns-in-crossbred-beef-cattle',
                'The original paper calls roan coat colour incomplete dominance. Red and white hairs in roan cattle are described as codominance. The printed cross and its 12-mark tariff are retained.'),
        'q8c':('https://www.ncbi.nlm.nih.gov/books/NBK234922/',
               'The historical scheme includes “not needed for growth” for non-essential amino acids. These amino acids are needed to make proteins; non-essential means the body can synthesise them. The original scheme remains visible for this examination.'),
    }
    for task,card in zip(tasks,cards):
        key=card['id'].removeprefix('agsci-2011-hl-')
        source_key='q8c' if key.startswith('q8c-route-') and 'i' in task['selection']['route'] else key
        if source_key in scientific:
            url,note=scientific[source_key]
            task['schemeNote']=note
            task['scientificContext']={'source':url,'checkedAt':'2026-10-07','treatment':'Retain the historical quotation and tariff; explain the scientific distinction.'}
            card['rows'][0]['contextNote']=(card['rows'][0].get('contextNote','')+' '+note).strip()
    assert len(cards)==70
    assert len({c['id'] for c in cards})==70
    return cards,tasks
