#!/usr/bin/env python3
"""Independent, incrementally reviewed task denominator for Agricultural Science.

Read from the SEC paper/scheme boundary review, not from authored cards. The
generic leaf parser loses Q1 and the two Q3 options in legacy Higher papers;
it also splits pooled marking scales. Every unaudited edition stays OPEN.
This module must not import the authoring modules, reviewed-task output or deck.
"""
import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / 'scripts/markbank/authored/agricultural-science-census.json'

# ref | marks | paper PDF page | scheme PDF page | distinctive scheme wording
# A marks field describes one practice response, never all choice routes added.
HIGHER_2010 = '''
Q1(a)|10|2|5|It is a species which shows the conditions in the habitat.
Q1(b)|10|2|5|Crown/root/enamel/
Q1(c)|10|2|5|High dry matter /high dmd
Q1(d)(i)|4|2|5|acid-alkali scale
Q1(d)(ii)|6|2|5|sour milk 4-5, rumen 7, abomasum 2
Q1(e)|10|2|5|Refractometer= estimate sugar%
Q1(f)|10|2|5|Asteraceae/Compositae
Q1(g)|10|2|5|114 DAYS
Q1(h)|10|2|5|Food store
Q1(i)|10|2|5|Not as high in N as urea or CAN
Q1(j)|10|2|5|leaves have holes
Q2(a)|16|2|6|Activity of soil animals
Q2(b)|16|2|6|Blanket =caused by high local rainfall
Q2(c)|16|2|6|Loss in wt divided by wt of sample
Q3 Option One (a)(i)|4|3|7|because it’s a good dairy
Q3 Option One (a)(ii)|4|3|7|beef calves for sale
Q3 Option One (a)(iii)|4|3|7|easy calving
Q3 Option One (a)(iv)|4|3|7|15-20%
Q3 Option One (b)|16|3|7|MILK LET-DOWN
Q3 Option One (c)|16|3|7|WITHDRAWAL
Q3 Option Two (a)(i)|4|3|8|Lime(stone)
Q3 Option Two (a)(ii)|8|3|8|Weathering of limestone
Q3 Option Two (b) — parasitic disease|6|3|8|parasitic means caused by a parasite
Q3 Option Two (b) — deficiency disease|6|3|8|deficiency disease caused by a lack
Q3 Option Two (b)|12|3|8|Grass-Tetany
Q3 Option Two (c)|12|3|8|not certified seed
Q4(a)|24|3|9|SOIL TEXTURE
Q4(b)|24|3|9|EARTHWORMS
Q4(c)|24|3|9|TRANSPIRATION RATE
Q4(d)|24|3|9|BARLEY DIGESTIBILITY
Q5(a)(i)|8|4|9|RADDLING HARNESS
Q5(a)(ii)|8|4|9|FOOTROT
Q5(b)(i)|16|4|9|RESEEDING WHY?
Q5(b)(ii)|8|4|9|perennial ryegrass
Q5(c)|8|4|9|LEAF:STEM
Q6(a)|12|4|10|BLIGHT
Q6(b)|12|4|10|SCUTCH
Q6(c)(i)|6|4|10|PLOUGH PAN
Q6(c)(ii)|6|4|10|First point compulsory in (ii)
Q6(d)|12|4|10|1000 grain weight
Q7(a)|12|4|11|ANY THREE
Q7(b)(i)|4|4|11|Parents phenotypes
Q7(b)(ii)|9|4|11|Punnett square:
Q7(b)(iii)|3|4|11|Test cross or back cross
Q7(c)(i)|6|4|11|occurs when cell division goes wrong
Q7(c)(ii)|6|4|11|Name of ploidy
Q7(d)|8|4|11|CALVING DIFFICULTY INDEX
Q8(a)|24|5|12|At least one point from either
Q8(b)|24|5|12|Photosynthesis:
Q8(c)|24|5|12|Two points from each alternative
Q9(a)|12|5|13|At least one reference each to fasting and hanging
Q9(b)|12|5|13|oxygen is more soluble in cold
Q9(c)|12|5|13|highest yielding breed
Q9(d)|12|5|13|protein rich
Q9(e)|12|5|13|conifers do well
'''

ORDINARY_2010 = '''
Q1(a)|4|2|5|A: Air
Q1(b)|12|2|5|Accept “sand” alone for 3 marks
Q1(c)|4|2|5|Earthworm, fungus, bacteria
Q2 — activity 2|4|3|5|2. Harvesting barley
Q2 — activity 3|4|3|5|3. Making hay
Q2 — activity 4|4|3|5|4. Harvesting potatoes
Q2 — activity 5|4|3|5|5. Sowing seed
Q2 — activity 6|4|3|5|6. Breaking up compacted soil
Q3(a)|2|3|5|Accept “Simmental”.
Q3(b)|6|3|5|Wedge(triangular) shaped
Q3(c) — lactation|3|3|5|Lactation – production of milk
Q3(c) — colostrum|3|3|5|Colostrum – first milk
Q3(d)|6|3|5|305 days
Q4 — Mastitis|4|4|6|Mastitis
Q4 — Swine fever|4|4|6|Swine fever
Q4 — Brucellosis|4|4|6|Brucellosis
Q4 — Liverfluke|4|4|6|Liverfluke
Q4 — Tuberculosis (TB)|4|4|6|Tuberculosis (TB)
Q5|20|4|6|6(3) + 2
Q6(a)|12|5|6|A: Cell Wall B: Vacuole
Q6(b)|4|5|6|Chlorophyll
Q6(c)|4|5|6|Photosynthesis or to make food
Q7|20|5|6|The first five correct answers 5(1); the next five correct answers 5(3)
Q8(a)(i)|6|6|7|A: Strip Grazing / B: Paddock Grazing
Q8(a)(ii) — strip|6|6|7|Strip Grazing: Land divided into strips
Q8(a)(ii) — paddock|6|6|7|Paddock Grazing: Land divided into paddocks
Q8(a)(iii) — strip advantage|3|6|7|Fresh grass always available
Q8(a)(iii) — strip disadvantage|3|6|7|High labour or hard to contain stock
Q8(a)(iii) — paddock advantage|3|6|7|Fresh grass every day
Q8(a)(iii) — paddock disadvantage|3|6|7|Expensive or need to create roads
Q8(a)(iv)|3|6|7|Set stocking or block grazing
Q8(b)(i)|6|6|7|Perennial ryegrass (PRG)
Q8(b)(ii)|6|6|7|PRG – good productivity
Q8(c)|9|6|8|Description: Three points.
Q8(d) — tillering|3|6|8|Tillering – the growth of side shoots
Q8(d) — topping|3|6|8|Topping – cutting the grass
Q9(a)|4|7|9|Liming
Q9(b)|6|7|9|Any two correct elements
Q9(c)|2|7|9|Crop named
Q9(d)|4|7|9|Correct Fertilizer
Q9(e)(i)|6|7|9|Preparation of seedbed
Q9(e)(ii)|2|7|9|Spring sowing
Q9(e)(iii)|6|7|9|Blight/potato cyst nematode
Q9(e)(iv)|4|7|9|Spray (fungicide)
Q9(e)(v)|2|7|9|First earlies: May-June
Q9(e)(vi)|6|7|9|First and second earlies - 7-10 tonnes/Ha.
Q9(f)|18|7|9|Any four relevant points
Q10(a)(i)|9|8|10|A: (Right) atrium
Q10(a)(ii)|9|8|10|White blood cells/Red blood cells
Q10(a)(iii)|9|8|10|Fight infection
Q10(a)(iv)|3|8|10|Iron deficiency
Q10(a)(v)|3|8|10|Iron injection
Q10(b)(i)|9|8|10|A: Ovary/B: Vagina
Q10(b)(ii)|3|8|10|Stock ewes on poor quality pasture
Q10(b)(iii)|9|8|10|More eggs released
Q10(b)(iv)|3|8|10|Artificial insemination
Q10(b)(v)|3|8|10|Better choice of sire
Q11(a)(i)|4|9|11|Shape of an animal
Q11(a)(ii)|8|9|11|Beef animals have muscular shoulders
Q11(a)(iii)|4|9|11|2 - 2 ½ years
Q11(a)(iv)|4|9|11|After this age fat is put on
Q11(b)(i)|8|9|11|Texel/Wicklow
Q11(b)(ii)|4|9|11|3-6 kg
Q11(b)(iii) — feeding|4|9|11|Feeding: Colostrum
Q11(b)(iii) — management|8|9|11|Management: Any two
Q11(c)(i)|4|9|11|Only young animal has access to food
Q11(c)(ii)|12|9|11|Supplements milk from mother
Q12(a)(i)|8|9|12|Any two weeds
Q12(a)(ii)|4|9|12|One piece of equipment
Q12(a)(iii)|18|9|12|Any three points:
Q12(b)(i)|4|9|12|20oC
Q12(b)(ii)|8|9|12|To prevent sow from crushing her bonhams
Q12(b)(iii)|4|9|12|Dry sow house
Q12(b)(iv)|14|9|12|Any three criteria
Q12(c)(i)|14|9|12|Any three advantages
Q12(c)(ii)|10|9|12|Any two ways
Q12(c)(iii)|6|9|12|Organic farming:
Q12(d)(i) — germination|4|9|12|Germination: Seed begins to grow
Q12(d)(i) — establishment|6|9|12|Establishment: new plant puts down roots
Q12(d)(ii)|18|9|12|one tube has all three suitable conditions
Q13(a)|18|10|13|1. dominant
Q13(b)(i)|12|10|13|Gametes E x e
Q13(b)(ii)|21|11|13|Genotype of second parent Ee
Q13(c)(i)|3|11|13|Meiosis
Q13(c)(ii)|6|11|13|L: Spindle (fibre)
'''

HIGHER_2011 = '''
Q1(a)|10|2|5|Rosaceae-large flowers
Q1(b)(i)|4|2|5|Condition scoring
Q1(b)(ii)|6|2|5|Calving 2.5-3.5, service 2-3
Q1(c)|10|2|5|Active = body manufactures antibodies
Q1(d)|10|2|5|Earthworms; adding lime
Q1(e)|10|2|5|Germination; use certified seed
Q1(f)|10|2|5|Mono: glucose
Q1(g)(i)|4|2|5|Platys: liverfluke/tapeworm
Q1(g)(ii)|6|2|5|Platy: liver damage/not thriving
Q1(h)(i)|4|2|5|Symbiosis; accept biology def
Q1(h)(ii)|6|2|5|Examples; Rhizobium
Q1(i)|10|2|5|Add acid to sample
Q1(j)|10|2|5|Stolon; above ground horizontal stem
Q2(a)(i)|4|2|6|Name: plough/iron/compaction
Q2(a)(ii)|4|2|6|Formed; continuous tillage
Q2(a)(iii)|4|2|6|Problem: hard/impervious layer
Q2(a)(iv)|4|2|6|Removal: deep ploughing
Q2(b)(i)|8|2|6|Gleisation: high rainfall
Q2(b)(ii)|8|2|6|Check field colour differences
Q2(c)|16|2|6|Place a sample of soil in flask
Q3 Option One (a)|16|3|7|Summer grazing; involves
Q3 Option One (b)|16|3|7|Replacement heifers;
Q3 Option One (c)(i)|8|3|7|FCE; how efficiently
Q3 Option One (c)(ii)|4|3|7|Body tissues develop in order
Q3 Option One (c)(iii)|4|3|7|Improve FCE;
Q3 Option Two (a)|16|3|7|Grassland management;
Q3 Option Two (b)(i)|2|3|7|Colostrum; /intestine changes
Q3 Option Two (b)(ii)|14|3|7|Nutritious/laxative/good start in life/
Q3 Option Two (c)(i)|4|3|7|Strip grazing;a moveable electric fence
Q3 Option Two (c)(ii) — advantages|6|3|7|Adv; cheap/get fresh material
Q3 Option Two (c)(ii) — disadvantages|6|3|7|Disadv; damage to soil structure
Q4(a)|24|3|8|Take 2 or more different varieties
Q4(b)|24|3|8|Place in sterile test tubes
Q4(c)|24|3|8|Get 2 suitable vessels
Q4(d)|24|3|8|Block off area
Q5(a)(i)|4|4|8|Anaemia
Q5(a)(ii)|4|4|8|Haemoglobin molecule
Q5(a)(iii)|4|4|8|Balanced diet (containing iron)
Q5(b)(i)|16|4|8|A= septum, B= right ventricle
Q5(b)(ii)|8|4|8|X= body(or named part), Y=lungs
Q5(b)(iii)|8|4|8|Blood in X= oxyhaemoglobin
Q5(c)|4|4|8|Haemoglobin in urine
Q6(a)|16|4|9|Crop is bleached
Q6(b)(i)|6|4|9|Soil type:malting
Q6(b)(ii)|6|4|9|Rotation: malting needs low N
Q6(b)(iii)|6|4|9|Fertiliser: Malting needs low N
Q6(b)(iv)|6|4|9|End use: Malting for brewing
Q6(c)|8|4|9|Diagram = 4,2,0 plus 4x1 labels
Q7(a)(i)|4|5|10|Interphase: before prophase
Q7(a)(ii)|4|5|10|Haploid; condition
Q7(a)(iii)|4|5|10|Inbreeding: allowing related
Q7(b) — cross|12|5|10|4 gametes each side
Q7(b)(i)|4|5|10|Hairy = 12/16
Q7(b)(ii)|4|5|10|Short = 4/16
Q7(b)(iii)|4|5|10|Hairy and short = 3/16
Q7(c)|12|5|10|RR = red WW(rr) = white RW(Rr) = roan
Q8(a)|24|5|11|One week before farrowing date
Q8(b)(i)|4|5|11|BOD: Biological
Q8(b)(ii)|4|5|11|Milk/slurry(FYM)/silage effluent
Q8(b)(iii)|8|5|11|Bacteria use up oxygen
Q8(b)(iv)|8|5|11|Strategies; ensure dairy waste
Q8(c)|24|5|11|Non essential; can be made
Q9(a)|12|5|12|Equation may cover all points
Q9(b)|12|5|12|Calves or offspring are tested
Q9(c)|12|5|12|Systemic; chemicals are absorbed
Q9(d)|12|5|12|Caused by wrong soil type
Q9(e)|12|5|12|To attract bonhams away from sow
'''

SOURCES = [
    (2010, 'higher', 'A', HIGHER_2010,
               'fa917bba0b9350bb15cfe355789fa3002515bb6b28561f46ac47acfc1e7fa408',
               '120a5729e8e4d01ea5411df25c54e509c95ea099fb55cb52466f045c72909174'),
    (2010, 'ordinary', 'G', ORDINARY_2010,
                 '4ee8be5bf23d55308b3d08007dad8c0a181c2e7a6cad0e501c4385272fa7e6f0',
                 '42dbd3ca25728ba373226b63a9c1224137705d62fd62a8516faf261a76879ef6'),
    (2011, 'higher', 'A', HIGHER_2011,
     '19975eb5d04e868becd63819eb5a3325929f6c774cff8e6abd4b72a1d3fb4ed9',
     '9979d05e915b789dd55e9ac742066987f4b26c75820485b15b1436ed5d06e9ba'),
]


def source_tasks():
    papers = []
    for year,level,letter,table,paper_hash,scheme_hash in SOURCES:
        fileid = f'LC024{letter}LP000EV.pdf'
        pages = {}
        for kind,digest in [('exampapers',paper_hash),('markingschemes',scheme_hash)]:
            path = ROOT / f'paper-trail-corpus/{kind}/{year}/{fileid}'
            assert hashlib.sha256(path.read_bytes()).hexdigest()==digest, f'Source changed: {path}'
            with fitz.open(path) as pdf:
                pages[kind] = [' '.join(page.get_text().split()) for page in pdf]
        tasks = []
        for line in table.strip().splitlines():
            ref,marks,paper_page,scheme_page,cue = line.split('|')
            paper_page,scheme_page = int(paper_page),int(scheme_page)
            # The seedbed heading is on the paper; its scheme says plough,
            # remove stones, harrow, drills and separately prices it 2 + 4.
            kind,page = ('exampapers',paper_page) if cue=='Preparation of seedbed' else ('markingschemes',scheme_page)
            assert cue in pages[kind][page-1], f'Stale source cue: {level} {ref}: {cue}'
            routes = [ref]
            selection = {'kind':'none'}
            if year==2010 and level=='higher' and ref=='Q3 Option Two (b)':
                routes = [ref+' — Hoose',ref+' — grass-tetany']
                selection = {'kind':'closed','choose':1,'options':['Hoose','grass-tetany']}
            elif level=='higher' and (ref=='Q8(c)' or year==2010 and ref=='Q7(a)'):
                choices = ['i','ii','iii','iv']
                routes = [ref+' — '+', '.join(parts) for parts in itertools.combinations(choices,3)]
                selection = {'kind':'closed','choose':3,'options':choices}
            tag = 'HL' if level=='higher' else 'OL'
            tasks.append({'ref':f'{year} {tag} {ref}','marksPerResponse':int(marks),
                          'paperPage':paper_page,'schemePage':scheme_page,
                          'sourceCue':{'kind':kind,'page':page,'text':cue},
                          'selection':selection,
                          'routes':[f'{year} {tag} {route}' for route in routes]})
        assert len(tasks)=={(2010,'higher'):55,(2010,'ordinary'):85,(2011,'higher'):67}[(year,level)]
        papers.append({'year':year,'level':level,'lang':'ev','paperFileid':fileid,
                       'sourceHashes':{'exampapers':paper_hash,'markingschemes':scheme_hash},
                       'status':'boundary-reviewed','baseTasks':tasks})
    return papers


def build():
    papers = source_tasks()
    inventory = json.loads((ROOT / 'scripts/markbank/authored/agricultural-science-inventory.json').read_text())
    # All indexed editions remain visible; a reviewed English denominator does
    # not silently declare the Irish edition or another sitting complete.
    return {'subjectId':'agricultural-science','status':'in-progress',
            'method':'Independent 2010 Higher/Ordinary and 2011 Higher paper/scheme boundary review with exact option and semantic-subtask addresses. Finite internal choices are expanded mechanically. Authored cards and their review ledger are not inputs.',
            'papers':papers,
            'boundaryRules':[
                'A diagram labelling exercise stays one task with all required labels and its figure; labels are answer fields, not printed alternative routes.',
                'A matching table can split into complete activity or disease tasks when each row has a published fixed award. Completed examples are not tasks.',
                'Pooled first-correct tariffs stay together: Higher Q1(e/f/g/j), Ordinary Q5 and Q7 must not allocate fixed marks to individual answer positions.',
                'Higher Q3 Option One and Option Two are distinct addresses. Q3 Option Two (b) has two common definitions and two alternative disease responses.',
                'Higher Q7(a) and Q8(c) each print a closed three-of-four pool. Each complete three-item response is one route.',
                'Exam choices between independently priced questions/parts do not combine unrelated tasks into extra practice identities.',
                'Ordinary Q3(a) identifies correct dairy breeds rather than choosing arbitrary pairs. Ordinary Q8(c) and Q9(c/e) are open methods/crops; accepted scheme examples are not a finite paper choice.',
                'Ordinary Q12(a)(iii) has inconsistent point-count wording: retain 18 marks and a non-automatic part-score. Q12(d) totals 28 in English versus 30 printed; disclose the discrepancy, never add fictitious marks.',
                '2011 Higher Q7(b): the shared cross receives 2+2 for parents and 8x1 for gametes; three separate offspring proportions receive four marks each. Never duplicate the shared 12 marks into each ratio task.',
                '2011 Higher Q7(a) requires each of three definitions, individually marked at four. Q8(c) alone has a closed three-of-four pool. Q6(c) preserves the 4/2/0 diagram band and four one-mark labels through manual total scoring.',
            ],
            'inventoryEditionCount':len(inventory['papers']),
            'editionStatus':[
                {'year':p['year'],'level':p['level'],'lang':p['lang'],
                 'paperFileid':p['doc']['fileid'],
                 'independentCensus':'boundary-reviewed' if (p['year'],p['level'],p['lang']) in {(q['year'],q['level'],q['lang']) for q in papers} else 'open'}
                for p in inventory['papers']],
            'questionMarkChecks':question_mark_checks(papers)}


def question_mark_checks(papers):
    """Candidate budgets collapse routes, then apply the printed outer choice.

    These totals use the independently transcribed boundaries above. They do
    not sum every alternative card as though one candidate answered them all.
    """
    checks = []
    for paper in papers:
        groups = {}
        higher = paper['level']=='higher'
        for task in paper['baseTasks']:
            address = task['ref'].split(' ',2)[2]
            question = re.match(r'Q\d+(?: Option (?:One|Two))?',address).group()
            groups.setdefault(question,[]).append(task)
        for question,tasks in groups.items():
            units = {}
            choose = None
            if higher and question in ['Q1','Q4','Q8','Q9']:
                choose = {'Q1':6,'Q4':2,'Q8':2,'Q9':4}[question]
            elif not higher and question=='Q12':
                choose = 2
            for task in tasks:
                unit = re.search(r'Q\d+(\([a-z]\))',task['ref']).group(1) if choose else 'all'
                units[unit] = units.get(unit,0)+task['marksPerResponse']
            totals = sorted({sum(values) for values in itertools.combinations(units.values(),choose or 1)})
            expected = (60 if question=='Q1' else 48) if higher else (20 if int(question[1:])<=7 else 60)
            discrepancy = not higher and question=='Q12'
            assert totals==([58,60] if discrepancy else [expected]), (paper['level'],question,totals)
            checks.append({'year':paper['year'],'level':paper['level'],'lang':paper['lang'],
                           'question':question,'units':units,'choose':choose or 1,
                           'candidateTotalsFromScheme':totals,'printedQuestionMarks':expected,
                           'sourceException':'English Q12(d) totals 28, not the printed 30; selecting it gives 58. Preserve the scheme and disclose the difference.' if discrepancy else None})
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        OUTPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    elif args.check:
        assert json.loads(OUTPUT.read_text())==data, 'Independent census stale'
    print('Source census: 2010 Higher 55 base tasks / 62 routes; 2010 Ordinary 85; 2011 Higher 67 / 70. Remaining editions stay open.')


if __name__=='__main__':
    main()
