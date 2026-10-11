"""Draft the 2015 Ordinary Level Construction Studies theory paper (LC029GLP000EV), Q1-Q9.

Every question text and stem is lifted from the SEC paper (a narrowed task only
deletes the other printed items); every row's verbatim is a phrase printed in the
SEC marking scheme; tariffs follow the scheme's mark tables (pages 17-25), checked
against rendered pages. Figures are exact crops of the original PDFs at 2x.

Run from anywhere; writes ordinary-draft.json and the figure PNGs beside this file.
Q1 keeps the validated checkpoint-589 draft's ids, rows and shared 8-mark drawing
allowance (applied once, on the complete question only).
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
P = 'paper-trail-corpus/exampapers/2015/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2015/LC029GLP000EV.pdf'
HASHES = {P: '6a5e6c2c39fcfc5d7d3d4eebae139ed927eaaaa16fb429d0eab333c3f0d7e99f',
          S: 'ca21a4dccfd47aea12de99758ce82058a9b33138a0ab9742dba1197b47364e07'}
ATTRIBUTION = 'SEC Leaving Certificate Construction Studies 2015 Ordinary Level — © State Examinations Commission.'
FP = 'construction-studies-2015-OL-'
PREFIX = 'cons-2015-ol-'
BAND8 = [0, 4, 6, 8]
BAND4 = [0, 2, 3, 4]

for f, h in HASHES.items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f

# ---------------------------------------------------------------- figures
FIGURES = {
    # key: (file, page, rect, solution)
    'q1-original': (P, 2, [38, 34, 580, 221], False),
    'q1-roof-section': (S, 4, [54, 54, 568, 752], True),
    'q2-original': (P, 2, [38, 236, 580, 398], False),
    'q2-cavity-fill': (S, 5, [408, 56, 544, 343], True),
    'q2-external-insulation': (S, 5, [382, 343, 556, 495], True),
    'q2-insulated-wall': (S, 5, [315, 540, 565, 699], True),
    'q2-scheme': (S, 5, [50, 52, 566, 765], True),
    'q3-original': (P, 2, [38, 398, 580, 588], False),
    'q3-system': (S, 6, [333, 97, 547, 350], True),
    'q3-scheme': (S, 6, [50, 52, 566, 765], True),
    'q4-original': (P, 2, [38, 588, 580, 790], False),
    'q4-site-plans': (S, 7, [43, 124, 549, 359], True),
    'q5-original': (P, 3, [38, 34, 580, 220], False),
    'q5-section': (S, 9, [50, 52, 566, 716], True),
    'q6-original': (P, 3, [38, 220, 580, 381], False),
    'q6-hand-sign': (S, 10, [52, 76, 169, 212], True),
    'q6-ear-sign': (S, 10, [222, 76, 340, 212], True),
    'q6-eye-sign': (S, 10, [408, 76, 523, 212], True),
    'q6-signs': (S, 10, [52, 76, 523, 212], True),
    'q7-original': (P, 3, [38, 381, 580, 528], False),
    'q7-water-butt': (S, 11, [397, 457, 548, 654], True),
    'q8-original': (P, 3, [38, 528, 580, 622], False),
    'q8-box-dovetail-joint': (S, 12, [384, 381, 542, 543], True),
    'q8-triple-glazing': (S, 12, [426, 555, 544, 705], True),
    'q8-solar-panel': (S, 13, [402, 44, 556, 304], True),
    'q8-cordless-drill': (S, 13, [410, 325, 532, 448], True),
    'q8-skirting-board': (S, 13, [422, 542, 558, 701], True),
    'q8-compression-fitting': (S, 14, [413, 67, 561, 186], True),
    'q8-natural-seasoning': (S, 14, [50, 226, 572, 541], True),
    'q8-concrete-lintel': (S, 14, [358, 568, 532, 725], True),
    'q8-radon-barrier': (S, 15, [309, 71, 543, 243], True),
    'q9-original': (P, 3, [38, 622, 580, 790], False),
    'q9-joint': (S, 15, [50, 388, 560, 779], True),
    'q9-table-features': (S, 16, [375, 89, 538, 214], True),
    'q9-finish': (S, 16, [408, 400, 546, 745], True),
}
question_figures = []
for key, (f, page, rect, solution) in FIGURES.items():
    with fitz.open(R / f) as pdf:
        px = pdf[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(rect), alpha=False)
    path = HERE / f'{FP}{key}.png'
    px.save(path)
    question_figures.append(dict(key=FP + key, source=f, page=page, rect=rect, renderScale=2,
                                 solution=solution, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                 visuallyInspected=True))


def page_hash(f, page):
    with fitz.open(R / f) as pdf:
        return hashlib.sha256(' '.join(pdf[page - 1].get_text().split()).encode()).hexdigest()


def checks(paper_page, scheme_pages):
    return ([dict(file=P, page=p, textSha256=page_hash(P, p)) for p in (1, paper_page)]
            + [dict(file=S, page=p, textSha256=page_hash(S, p)) for p in [2, *scheme_pages]])


def row(rid, verbatim, marks, note, steps):
    assert steps[0] == 0 and steps[-1] == marks
    return dict(id=rid, kind='criterion', verbatim=verbatim, marks=marks, contextNote=note, permittedMarks=steps)


# ---------------------------------------------------------------- questions
QUESTIONS = {
    '1': dict(page=2, title='Insulated porch roof and wallplate fixing', concept='porch-roof-section',
              stem='A front porch with a tiled roof is shown in the sketch. The porch has an internal width of 2.0 metres. The roof of the porch, which is insulated, is a traditional cut roof and has a pitch of 30°. The roof is supported on a 400 mm concrete block wall with a 200 mm full-fill insulated cavity. The rafters and ceiling joists are 200 mm × 40 mm. Insulated plasterboard is also fixed to the underside of the ceiling joists.',
              note='The original specified section and complete model drawing are retained. Detail/dimension marks and wallplate-fixing marks are separated from the one shared whole-drawing quality allowance. Historical model specifications do not assert current building regulations.'),
    '2': dict(page=2, title='Insulating an existing external wall', concept='external-wall-insulation',
              stem='The sketch shows a dwelling house which was built over 40 years ago. The external wall is a 300 mm concrete block wall with a 100 mm cavity. There is no insulation in the cavity. It is proposed to insulate the external wall by: filling the cavity with insulation and adding an external system of insulation to the wall.',
              note='Both insulation systems are required: each keeps its own published notes and sketch marks. The scheme procedures are typical model answers, not the only acceptable sequence.'),
    '3': dict(page=2, title='Hot and cold water to a mixer-shower and toilet', concept='bathroom-water-supply',
              stem='',
              note='The listed components are required content, not a choice. The scheme diagram is one acceptable layout; any alternative that complies with current Building Regulations is acceptable.'),
    '4': dict(page=2, title='Site layout: entrance, driveway, septic tank and trees', concept='site-layout',
              stem='The shaded portion of the map shows a site A for a house. Also shown is the location of the house B and a roadway C-C.',
              note='The original site map is retained. The scheme shows two acceptable layouts; preferred locations, reasons and tree species are open, well-reasoned responses. Distances quoted in the 2015 scheme are historical model guidance, not current regulations.'),
    '5': dict(page=3, title='Strip foundation, timber-frame wall and ground floor', concept='foundation-wall-floor-section',
              stem='A traditional strip foundation supports the external wall of a dwelling house, as shown in the sketch. The external wall is of timber-frame construction, with a 100 mm concrete block outer leaf, a 50 mm cavity and a 200 mm insulated timber-frame inner leaf. The ground floor is an insulated concrete floor with a 20 mm quarry tile finish.',
              note='Detail/dimension marks and the insulation-position marks are separated from the one shared whole-drawing quality allowance. Any alternative detailing that complies with current Building Regulations is acceptable.'),
    '6': dict(page=3, title='Personal protective equipment', concept='ppe-safety',
              stem='',
              note='The three named PPE types are all required. The scheme activities are examples; any other valid, specific activity is acceptable.'),
    '7': dict(page=3, title='Collecting rainwater in a water butt', concept='water-butt',
              stem='A water butt is used to collect rainwater from the pitched roof of a house, as shown.',
              note='Original sketch retained. Stored rainwater is for tasks that do not need potable water; the scheme does not present a water butt as a drinking-water supply.'),
    '8': dict(page=3, title='Construction terms', concept='construction-terms',
              stem='',
              note='Explain any five of the nine printed terms. Each term is marked separately at 10 marks; the scheme illustrations are examples of suitable sketches.'),
    '9': dict(page=3, title='Wooden table for outdoor use', concept='outdoor-table',
              stem='The sketch shows portion of a wooden table. The table is designed for outdoor use.',
              note='Original sketch retained. The joint, design features and finish are open choices; the scheme shows one suitable joint (haunched mortise and tenon) and accepts any other suitable joint or finish.'),
}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 8, 20], '5': [9, 21], '6': [10, 11, 22],
                '7': [11, 12, 23], '8': [12, 13, 14, 15, 24], '9': [15, 16, 25]}

tasks, bindings = [], []
cards = {}
CROSS = 'construction-studies-ordinary-'


def add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, scheme_pages=None,
        groups=None, bonus=None, total=None):
    meta = QUESTIONS[q]
    card = dict(id=f'{PREFIX}q{q}-{key}', subjectId='construction-studies', year=2015, level='ordinary', section='B',
                topicId=nodes[0], conceptId=f"{meta['concept']}-{key}", questionRef=f'2015 OL Q{q}{ref}',
                stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                totalMarks=total if total is not None else sum(r['marks'] for r in rows), rows=rows,
                questionFigureKey=f'{FP}q{q}-original', questionFigureIncludesPrompt=True)
    if figure:
        card['figureKey'] = FP + figure
    card['sourceMaterial'] = dict(kind='source-illustration', label=f'ORIGINAL QUESTION {q}', title=meta['title'],
                                  pages=[1, meta['page']], attribution=ATTRIBUTION, presentationNote=meta['note'])
    if groups:
        card['taskGroups'] = groups
    if bonus:
        card['questionBonus'] = bonus
    tasks.append(dict(questionNumber=q, card=card,
                      sourceChecks=checks(meta['page'], scheme_pages or SCHEME_PAGES[q]),
                      boundaryReview=boundary, selectionReview=selection,
                      requiredQuestionFigures=[f'{FP}q{q}-original'],
                      requiredSolutionFigures=[FP + figure] if figure else []))
    bindings.append(dict(cardId=card['id'], markBankTopicId=nodes[0], canonicalTopicIds=nodes,
                         canonicalTopicReview=review, questionNumber=q,
                         atlasTopicIds=[CROSS + t for t in topics]))
    cards[card['id']] = card
    return card


def compose(q, key, ref, children, figure, review, boundary, selection, text=None, labels=None, bonus=None,
            scheme_pages=None, total=None):
    """A complete route or composite part: every child row kept, prefixed by its group label."""
    rows, groups = [], []
    for i, child in enumerate(children):
        label = labels[i] if labels else child['id'].removeprefix(f'{PREFIX}q{q}-')
        prefix = child['id'].removeprefix(f'{PREFIX}q{q}-')
        rs = copy.deepcopy(child['rows'])
        for r in rs:
            r['id'] = f"{prefix}-{r['id']}"
        rows += rs
        groups.append(dict(sourceCardId=child['id'], label=label, marks=child['totalMarks'], rowIds=[r['id'] for r in rs]))
    child_bindings = [next(b for b in bindings if b['cardId'] == c['id']) for c in children]
    nodes = list(dict.fromkeys(n for b in child_bindings for n in b['canonicalTopicIds']))
    topics = list(dict.fromkeys(t.removeprefix(CROSS) for b in child_bindings for t in b['atlasTopicIds']))
    text = text or '\n\n'.join(c['questionText'] for c in children)
    return add(q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection,
               scheme_pages=scheme_pages, groups=groups, bonus=bonus,
               total=total if total is not None else sum(c['totalMarks'] for c in children) + (bonus['marks'] if bonus else 0))


# ---------------------------------------------------------------- Q1 (validated checkpoint-589 draft rows)
q1_draft = json.loads((HERE.parent / 'construction-2015-ordinary-q1-draft/q1-draft.json').read_text())
q1_rows = {t['card']['id']: t['card'] for t in q1_draft['tasks']}
B1 = 'a details36 (best 9 × 4) plus four dimensions 4 = 40; b wallplate fixing 2. The whole drawing has ONE shared draughting/accuracy/scale allowance of 8 (excellent 8, good 6, fair 4), printed after (b): it is applied once on the complete question and never attached to either part. Complete 50.'
S1 = 'One required half-roof section and one open wallplate-securing method. The scheme best-nine detail list is an indicative marking menu, not a printed choose-nine task. The front door is expressly excluded. The whole-exam rubric (Q1 plus three others) adds no single-question variants.'
A1 = add('1', 'a', '(a) — construction and dimensions',
         'To a scale of 1:5, draw a vertical section through one half of the roof of the porch, to show one rafter length. Show the typical construction details from a level 400 mm below the wallplate, through the wall and eaves up to the ridge. Show three courses of tiles at eaves. Include four typical dimensions. Note: It is not necessary to show the front door.',
         copy.deepcopy(q1_rows[PREFIX + 'q1-a']['rows']), ['cons-3-8', 'cons-3-9', 'cons-3-3', 'cons-6-2', 'cons-1-5'],
         ['roofs', 'foundations-floors-walls', 'heat-loss-insulation', 'question-one-drawing-questions'], 'q1-roof-section',
         '2015 outgoing syllabus: traditional cut roof form (3.8), tiled covering and roof insulation (3.9), the supporting cavity wall (3.3), thermal insulation (6.2) and the 1:5 scaled drawing of Question 1 (1.5). Ordinary Atlas files the wall under its combined Foundations/Floors/Walls heading.',
         B1, S1)
B1b = add('1', 'b', '(b) — wallplate fixing',
          'On your drawing, show clearly one method of securing the wallplate to the external wall.',
          copy.deepcopy(q1_rows[PREFIX + 'q1-b']['rows']), ['cons-3-8', 'cons-3-3'], ['roofs', 'foundations-floors-walls'],
          'q1-roof-section', 'Securing the wallplate is the roof-to-wall junction: roof structure (3.8) restrained to the external wall (3.3).', B1, S1)
bonus1 = copy.deepcopy(q1_rows[PREFIX + 'q1-complete']['questionBonus'])
compose('1', 'complete', ' — complete', [A1, B1b], 'q1-roof-section',
        'Complete Question 1 keeps the union of its separately reviewed parts.', B1, S1,
        text='(a) ' + A1['questionText'] + '\n\n(b) ' + B1b['questionText'], bonus=bonus1)

# ---------------------------------------------------------------- Q2
B2 = 'Scheme p18: filling the cavity notes 3 × 4 = 12 plus sketch quality 8 (8/6/4) = 20; external insulation notes 3 × 4 = 12 plus sketch quality 8 = 20; (a) 40. (b) two advantages × 5 = 10. Complete 50.'
S2 = 'The stem names two systems joined by AND and part (a) asks for EACH: both are required, not alternatives, so each system is a separately marked task and (a) is their sum. Part (b) two open advantages, not a finite list.'
WALL = ['cons-6-2', 'cons-3-3']
WALL_T = ['heat-loss-insulation', 'foundations-floors-walls']
A2c = add('2', 'a-cavity-fill', '(a) — filling the cavity with insulation',
          'It is proposed to insulate the external wall by: filling the cavity with insulation. Using notes and freehand sketches, show the steps to be followed in applying each system of insulation to the wall.',
          [row('notes', 'Filling the cavity with insulation – Notes', 12,
               'Three valid steps, 4 marks each. Typical procedure (carried out by specialist firms): 22 mm diameter holes are drilled through the external leaf, usually spaced about 800 mm horizontally and 1350 mm vertically; special care is taken at damp proof courses and at heads of windows and doors, with extra holes drilled around openings so the cavity fills properly; polystyrene beads are pumped into the cavity while a light coating of glue is applied, setting into a solid structure; when pumping is complete the holes are filled. Other valid steps are acceptable.',
               [0, 4, 8, 12]),
           row('sketches', 'Filling the cavity with insulation – Sketches', 8,
               'Quality of sketches for the cavity-fill steps: excellent 8, good 6, fair 4. The scheme sketches show the drill entering the outer leaf and the hole spacing on the wall.',
               BAND8)],
          WALL, WALL_T, 'q2-cavity-fill',
          'Retrofitting insulation material (6.2) into the existing cavity wall (3.3).', B2, S2)
A2e = add('2', 'a-external-insulation', '(a) — adding an external system of insulation',
          'It is proposed to insulate the external wall by: adding an external system of insulation to the wall. Using notes and freehand sketches, show the steps to be followed in applying each system of insulation to the wall.',
          [row('notes', 'Adding an external system of insulation to the wall – Notes', 12,
               'Three valid steps, 4 marks each. Typical procedure: the first row of insulation boards is fixed in place resting on a stainless steel track; boards are fixed in position with a special adhesive, and all rows are fixed and the adhesive allowed to set; mechanical fixings (typically about seven per square metre, longer for thicker boards) are installed by drilling through the insulation into the wall and then hammered into place. Typical insulation materials: polystyrene, mineral fibre board, wood fibre board. Other valid steps are acceptable.',
               [0, 4, 8, 12]),
           row('sketches', 'Adding an external system of insulation to the wall – Sketches', 8,
               'Quality of sketches for the external-insulation steps: excellent 8, good 6, fair 4. The scheme sketch shows the wall, adhesive, insulation board and mechanical fixing.',
               BAND8)],
          WALL, WALL_T, 'q2-external-insulation',
          'External insulation system (6.2) applied to the existing external wall (3.3).', B2, S2)
A2 = compose('2', 'a', '(a)', [A2c, A2e], 'q2-scheme',
             'Part (a) keeps the union of both required insulation systems.', B2, S2,
             text='Using notes and freehand sketches, show the steps to be followed in applying each system of insulation to the wall.',
             labels=['filling the cavity with insulation', 'adding an external system of insulation to the wall'])
B2b = add('2', 'b', '(b)', 'Discuss two advantages of insulating the external walls of the house.',
          [row('advantages', 'Two advantages of insulating the external walls of the house', 10,
               'Two distinct advantages, 5 marks each, discussed rather than just named. Such as: reduced heat loss and a warmer house; improved thermal comfort with no extremes of heat or cold; lower energy bills; less fossil fuel burned to heat the house, which is better for the environment; improved U-value and Building Energy Rating (BER); reduced condensation and mould; the wall retains heat and acts as a heat store. Do not credit the same advantage twice.',
               [0, 5, 10])],
          ['cons-6-2', 'cons-6-3'], ['heat-loss-insulation'], 'q2-insulated-wall',
          'Benefits of insulating materials (6.2) through reduced heat loss and running costs (6.3).', B2, S2)
compose('2', 'complete', ' — complete', [A2, B2b], 'q2-scheme',
        'Complete Question 2 keeps the union of its separately reviewed parts.', B2, S2,
        text='(a) ' + A2['questionText'] + '\n\n(b) ' + B2b['questionText'])

# ---------------------------------------------------------------- Q3
B3 = 'Scheme p19: (a) best 8 of 12 listed details × 4 = 32 plus sketch quality 8 (8/6/4) = 40, printed before part (b). (b) two methods × 5 (notes and sketches) = 10. Complete 50.'
S3 = 'The four bullets and the insulation instruction are required diagram content, not a choice. Part (b) asks for two open methods; the scheme groups examples by shower, basin, toilet and bath without making them a closed pool.'
A3 = add('3', 'a', '(a)',
         'Using a single-line labelled diagram, show the pipework required to provide hot and cold water to a mixer-shower and to provide cold water to a toilet, as shown in the sketch. Include the following on your diagram: rising main and water storage tank; hot water cylinder; typical pipework to mixer-shower and toilet; all necessary valves. On your diagram, show the insulation to the water storage tank in the attic and to all the pipework.',
         [row('details', 'Any 8 of the above details (4 marks each)', 32,
              'Credit the best EIGHT correct details at 4 marks each, capped at 32. Marked details: rising main (typically 15 mm with stop valve); cold water storage tank; overflow (22 mm minimum); cold supply from the storage tank to the hot water cylinder (22 mm); hot water cylinder (pre-insulated); expansion pipe from the cylinder (22 mm); hot water supply to the mixer-shower (22 mm); cold water supply to the mixer-shower (22 mm); cold water supply to the toilet cistern (15 mm); valves; insulation to the storage tank and pipework; labelling. Hot and cold supplies to the shower and a cold supply to the toilet are all required.',
              list(range(0, 33, 4))),
          row('sketch', 'Quality of sketch', 8, 'Quality of the single-line diagram: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-5-2', 'cons-5-1'], ['services-water-gas-electrical', 'hot-water-space-heating'], 'q3-system',
         'Hot and cold water system with storage tank and cylinder (5.2) and protection of the installation by insulating tank and pipework (5.1).',
         B3, S3)
B3b = add('3', 'b', '(b)', 'Using notes and sketches, show two methods of reducing the use of water in a bathroom.',
          [row('methods', 'Two methods to reduce the use of water in a bathroom', 10,
               'Two distinct methods, 5 marks each for notes and sketches. Such as: a low-flow eco or aerated shower head; shorter showers and no power shower; a tap aerator, push-button or infra-red sensor taps, or an inline regulating valve on the wash hand basin; not running the tap while brushing teeth; a low-flush or dual-flush cistern, or a water-saver bag in the cistern; checking the cistern for leaks; showering rather than bathing.',
               [0, 5, 10])],
          ['cons-5-6', 'cons-5-2'], ['drainage', 'services-water-gas-electrical'], 'q3-scheme',
          'Water-saving sanitary fitments (5.6) and the cold/hot water supply to them (5.2).', B3, S3)
compose('3', 'complete', ' — complete', [A3, B3b], 'q3-scheme',
        'Complete Question 3 keeps the union of its separately reviewed parts.', B3, S3,
        text='(a) ' + A3['questionText'] + '\n\n(b) ' + B3b['questionText'])

# ---------------------------------------------------------------- Q4
B4 = 'Scheme p20: (a) site outline and house 3, entrance 3, driveway 3, septic tank and percolation area 3, sketch quality 8 = 20. (b) one reason for each of the three locations × 4 = 12. (c) two tree types × 2, planting sketch quality 8, two advantages × 3 = 18. Complete 50.'
S4 = 'Part (a) is one integrated site sketch with one quality mark, so it stays whole. Part (b) asks for one reason for EACH of the three printed items (entrance, driveway, septic tank and percolation area), each separately marked at 4: three required tasks, not a choice. Tree species and advantages in (c) are open.'
SITE = ['cons-1-3', 'cons-5-5']
A4 = add('4', 'a', '(a)',
         'Draw a large freehand sketch of the given site. Show on your sketch a preferred location for each of following: the entrance to the site at the roadway; the driveway to the house from the entrance; the septic tank and percolation area.',
         [row('site', 'Site outline and house', 3, 'Sketch the given site outline with house B in its position.', [0, 3]),
          row('entrance', 'Entrance', 3, 'Show a preferred location for the entrance at roadway C-C.', [0, 3]),
          row('driveway', 'Driveway', 3, 'Show the driveway from the entrance to the house.', [0, 3]),
          row('septic', 'Septic tank and percolation area', 3, 'Show a preferred location for the septic tank and its percolation area.', [0, 3]),
          row('sketch', 'Quality of sketch', 8, 'Quality of the site sketch: excellent 8, good 6, fair 4.', BAND8)],
         SITE, ['planning-sustainability-environment', 'drainage'], 'q4-site-plans',
         'Site layout for a house on a chosen site (1.3) including the septic tank and percolation area (5.5).', B4, S4)
REASONS = [
    ('entrance', 'the entrance to the site at the roadway', 'Entrance', ['cons-1-3'], ['planning-sustainability-environment'],
     'One discussed reason, 4 marks. Such as: on a straight stretch of road with an unobstructed view in both directions for safety (sight lines measured back from the road edge); splayed so vehicles can enter and leave safely; gates set back and opening inward so a car can pull in off the road; retaining as much existing hedgerow as possible; a simple entrance in keeping with local style.',
     'Entrance location: a site-planning decision (1.3).'),
    ('driveway', 'the driveway to the house from the entrance', 'Driveway', ['cons-1-3'], ['planning-sustainability-environment'],
     'One discussed reason, 4 marks. Such as: following the contours of the site; curving to reduce speed within the site and avoid a long straight visible drive; a shale or gravel surface that lets ground water drain and reduces visual and environmental impact, rather than hard tarmacadam.',
     'Driveway location: a site-planning decision (1.3).'),
    ('septic-tank', 'the septic tank and percolation area', 'Septic tank and percolation area', ['cons-5-5', 'cons-1-3'],
     ['drainage', 'planning-sustainability-environment'],
     'One discussed reason, 4 marks. Such as: the location keeps the required separation from the house, the site boundary and the road; downhill of the house so effluent flows by gravity; ground suitable for a percolation area. The 2015 scheme quotes historical model distances (for example 7 m from the house); learn the distances in current regulations rather than treating these as current law.',
     'Septic tank and percolation area (5.5) located as part of the site layout (1.3).'),
]
b4 = []
for slug, item, verbatim, nodes, topics, note, review in REASONS:
    b4.append(add('4', f'b-{slug}', f'(b) — {item}',
                  f'{item[0].upper()}{item[1:]}: discuss one reason why you selected the preferred location.',
                  [row('reason', verbatim, 4, note, [0, 4])], nodes, topics, 'q4-site-plans', review, B4, S4))
B4b = compose('4', 'b', '(b)', b4, 'q4-site-plans', 'Part (b) keeps the union of its three required reasons.', B4, S4,
              text='For each of the above, discuss one reason why you selected the preferred location.',
              labels=[r[1] for r in REASONS])
C4 = add('4', 'c', '(c)',
         'It is proposed to plant more trees on the site. Recommend two suitable types of tree and show on your sketch where you would plant the trees on the site. Discuss two advantages of planting the recommended trees on the site.',
         [row('types', 'Two suitable types of tree', 4,
              'Two suitable tree types, 2 marks each. Such as native or naturalised species: silver birch, rowan (mountain ash), beech, hazel, cherry, ash, wild crab apple, oak, holly, hornbeam; or a mixed native hedgerow (whitethorn, blackthorn, beech, field maple, hazel). The scheme also favours retaining existing trees and hedgerows and avoiding exotic evergreens along boundaries. Species choice should suit the site and soil.',
              [0, 2, 4]),
          row('sketch', 'Show where you would plant the trees on the site', 8,
              'Show the planting positions on your site sketch: quality excellent 8, good 6, fair 4. The scheme plans show trees along the boundaries and beside the driveway.', BAND8),
          row('advantages', 'Two advantages of the recommended trees on the site', 6,
              'Two distinct advantages, 3 marks each. Such as: shelter from prevailing winds; habitat and food for wildlife and biodiversity; absorbing CO2 and releasing oxygen; screening noise and giving privacy from the road and neighbours; deciduous trees shade the house in summer and let in light in winter; helping the house blend into the countryside and softening its visual impact.',
              [0, 3, 6])],
         ['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'], 'q4-site-plans',
         'Landscaping and its effect on the built environment (1.2) within the site plan (1.3).', B4, S4)
compose('4', 'complete', ' — complete', [A4, B4b, C4], 'q4-site-plans',
        'Complete Question 4 keeps the union of its separately reviewed parts.', B4, S4,
        text='(a) ' + A4['questionText'] + '\n\n(b) ' + B4b['questionText'] + '\n\n(c) ' + C4['questionText'])

# ---------------------------------------------------------------- Q5
B5 = 'Scheme p21: (a) best 7 of 14 listed details × 5 = 35 plus four dimensions 4 = 39; (b) wall and floor insulation 3 (one shared mark, not 3 each). One shared draughting/accuracy/scale allowance of 8 (8/6/4) printed after (b): applied once on the complete question. Complete 50.'
S5 = 'One required section and one required insulation-position detail covering BOTH wall and floor. The best-seven detail list is a marking menu, not a printed choose-seven task. The radon barrier is required content.'
A5 = add('5', 'a', '(a) — construction and dimensions',
         'To a scale of 1:5, draw a vertical section through the foundation, external wall and ground floor. Show the typical construction details from the bottom of the foundation, through the wall and ground floor to a level 400 mm above finished floor. Include the radon barrier and show four typical dimensions.',
         [row('details', 'Any 7 of the above details ( 5 marks each)', 35,
              'Credit the best SEVEN acceptable details at 5 marks each, capped at 35. Marked details: external render (19 mm); concrete block outer leaf (100 mm); 50 mm ventilated cavity; breather membrane and racking board (OSB/plywood); 200 mm timber stud; 12.5 mm plasterboard; skirting board; concrete slab and 20 mm quarry tiles; floor insulation (200–300 mm) with vertical edge insulation; radon barrier/DPM and damp proof course (DPC); hardcore and sand blinding; cavity fill and concrete insulation blocks; reinforced concrete foundation; footpath and hardcore. Keep the printed 100 mm outer leaf, 50 mm cavity, 200 mm timber-frame inner leaf and 20 mm quarry tiles.',
              list(range(0, 36, 5))),
          row('dimensions', 'Four typical dimensions', 4,
              'Include four appropriate dimensions on the section. One published 4-mark allowance; the shared whole-drawing quality allowance is not included again here.', [0, 4])],
         ['cons-2-4', 'cons-3-3', 'cons-4-2', 'cons-3-4', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation'],
         'q5-section',
         'Strip foundation (2.4), external wall (3.3), insulated solid ground floor (4.2), DPC and radon barrier (3.4) and insulation (6.2) are all explicit in the printed section.',
         B5, S5)
B5b = add('5', 'b', '(b) — insulation position',
          'On your drawing, show clearly the position of the insulation in the wall and in the floor.',
          [row('insulation', 'Wall and floor insulation', 3,
               'Show BOTH positions; one shared 3-mark allowance, not 3 for each. Wall: about 200 mm rigid, blown, board or quilt insulation between the timber studs. Floor: 200–300 mm rigid insulation fitted above the radon barrier and below the concrete slab, thickness depending on the insulation material.',
               [0, 3])],
          ['cons-6-2', 'cons-3-3', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls'], 'q5-section',
          'Insulation position (6.2) in the external wall (3.3) and ground floor (4.2).', B5, S5)
compose('5', 'complete', ' — complete', [A5, B5b], 'q5-section',
        'Complete Question 5 keeps the union of its separately reviewed parts.', B5, S5,
        text='(a) ' + A5['questionText'] + '\n\n(b) ' + B5b['questionText'],
        bonus=row('drawing-quality', 'Draughting, accuracy and scale', 8,
                  'One shared assessment of the COMPLETE drawing: excellent 8, good 6, fair 4; zero if no credit. Apply once to the integrated 1:5 section including the insulation positions. The scheme does not award it separately to each part.',
                  BAND8))

# ---------------------------------------------------------------- Q6
B6 = 'Scheme p22: (a) three sign sketches, each quality 8 (8/6/4) = 24; (b) one activity for each of the three PPE types × 4 = 12; (c) two activities × 7 = 14. Complete 50.'
S6 = 'Parts (a) and (b) name three PPE types and require EACH: three required, separately marked tasks per part, not a choice. Part (c) two open activities; the scheme examples are not a closed pool.'
PPE = [('hand', 'hand protection', 'Hand protection', ['cons-1-8'], ['site-safety'],
        'Hand protection sign: blue circular mandatory sign with white gloves. Quality of sketch: excellent 8, good 6, fair 4.',
        'One specific construction-site activity, 4 marks. Such as: laying blocks or bricks; moving roof tiles or slates; handling sharp materials; building or working with stone; fixing or removing scaffolding; working with corrosive or toxic substances; any other valid activity.',
        'Hand protection on site: safety precautions on site (1.8).'),
       ('ear', 'ear protection', 'Ear protection', ['cons-1-8', 'cons-8-4'], ['site-safety', 'sound'],
        'Ear protection sign: blue circular mandatory sign showing a head wearing ear defenders. Quality of sketch: excellent 8, good 6, fair 4.',
        'One specific construction-site activity, 4 marks. Such as: using a hammer-action or percussion drill; using a compressor; cutting concrete lintels or cills with a con saw; using a mechanical woodworking saw; any work where noise is continuously at about 85–90 decibels or more; any other valid activity.',
        'Ear protection: site safety (1.8) and noise levels and hearing-protection devices (8.4).'),
       ('eye', 'eye protection', 'Eye protection', ['cons-1-8'], ['site-safety'],
        'Eye protection sign: blue circular mandatory sign showing a face wearing safety goggles. Quality of sketch: excellent 8, good 6, fair 4.',
        'One specific construction-site activity, 4 marks. Such as: mechanically cutting or drilling concrete or steel; using a hammer, angle grinder or nail gun; welding steel; painting ceilings or chipping loose paintwork; any other valid activity.',
        'Eye protection on site: safety precautions on site (1.8).')]
a6, b6 = [], []
for slug, item, verbatim, nodes, topics, sign_note, activity_note, review in PPE:
    a6.append(add('6', f'a-{slug}', f'(a) — {item}',
                  f'Draw the particular safety signs to show the personal protective equipment (PPE) for {item}.',
                  [row('sign', verbatim, 8, sign_note, BAND8)], nodes, topics, f'q6-{slug}-sign', review, B6, S6))
for slug, item, verbatim, nodes, topics, sign_note, activity_note, review in PPE:
    b6.append(add('6', f'b-{slug}', f'(b) — {item}',
                  f'{item[0].upper()}{item[1:]}: state one specific activity where the personal protective equipment you have shown should be worn on a construction site.',
                  [row('activity', verbatim, 4, activity_note, [0, 4])], nodes, topics, None, review, B6, S6))
A6 = compose('6', 'a', '(a)', a6, 'q6-signs', 'Part (a) keeps the union of its three required signs.', B6, S6,
             text='Draw the particular safety signs to show the personal protective equipment (PPE) for each of the following: hand protection; ear protection; eye protection.',
             labels=[p[1] for p in PPE])
B6b = compose('6', 'b', '(b)', b6, None, 'Part (b) keeps the union of its three required activities.', B6, S6,
              text='For each of the above, state one specific activity where the personal protective equipment you have shown should be worn on a construction site.',
              labels=[p[1] for p in PPE])
C6 = add('6', 'c', '(c)',
         'Outline two activities in the Construction Studies room where it is recommended that personal protective equipment should be worn.',
         [row('activities', 'Two activities in the Construction Studies room where it is recommended that the personal protective equipment should be worn', 14,
              'Two distinct activities, 7 marks each, outlining the PPE and why it is worn. Such as: drilling wood, metal or acrylic (eye protection against small particles, ear protection, gloves for sharp edges); cutting wood with a jig saw or band saw (eye and ear protection; a dust mask when cutting plywood or MDF); using a woodturning lathe (visor against flying chips, dust mask, ear muffs); using mechanical or belt sanders (dust mask, eye and ear protection); painting or varnishing (gloves; respiratory mask in confined areas).',
              [0, 7, 14])],
         ['cons-9-4'], ['site-safety'], None, 'Safe use of tools and machines in the Construction Studies room (9.4).', B6, S6)
compose('6', 'complete', ' — complete', [A6, B6b, C6], 'q6-signs',
        'Complete Question 6 keeps the union of its separately reviewed parts.', B6, S6,
        text='(a) ' + A6['questionText'] + '\n\n(b) ' + B6b['questionText'] + '\n\n(c) ' + C6['questionText'])

# ---------------------------------------------------------------- Q7
B7 = 'Scheme p23: (a) two notes details × 6 = 12 plus sketch quality 8 (8/6/4) = 20; (b) two advantages × 5 = 10 AND two disadvantages × 5 = 10 = 20; (c) two reasons × 5 = 10. Complete 50.'
S7 = 'Part (b) requires both two advantages AND two disadvantages, separately marked: two required tasks, not a choice. All other responses are open.'
RAIN = ['cons-5-4']
A7 = add('7', 'a', '(a)',
         'Using notes and freehand sketches, show the pipework necessary to collect the rainwater from the roof and to store it in the water butt.',
         [row('notes', 'pipework necessary to collect and store rainwater from the roof', 12,
              'Two valid details, 6 marks each. Rainwater from the sloping roof flows into the eaves gutter and down the downpipe; a diverter on the downpipe sends it through a connecting hose into the water butt; when the butt is full the diverter returns the water to the downpipe and the gully; the butt usually sits on a stand with a tap near the bottom.',
              [0, 6, 12]),
          row('sketch', 'pipework necessary to collect rainwater from the roof and store it', 8,
              'Quality of sketches showing gutter, downpipe, diverter, hose and butt: excellent 8, good 6, fair 4.', BAND8)],
         RAIN, ['drainage'], 'q7-water-butt', 'Eaves gutters and rainwater pipes (5.4).', B7, S7)
B7a = add('7', 'b-advantages', '(b) — advantages',
          'Discuss two advantages of using a water butt to store rainwater.',
          [row('advantages', 'Two advantages of using a water butt to store rainwater', 10,
               'Two distinct advantages, 5 marks each. Such as: environmentally friendly, reducing the amount of treated water used; lower water bills where meters are installed; rainwater is satisfactory for watering gardens and washing cars; butts are inexpensive, easy to fit and maintain, and can be linked in series for more storage.',
               [0, 5, 10])],
          RAIN, ['drainage'], None, 'Rainwater collected from gutters and downpipes (5.4).', B7, S7)
B7d = add('7', 'b-disadvantages', '(b) — disadvantages',
          'Discuss two disadvantages of using a water butt to store rainwater.',
          [row('disadvantages', 'Two disadvantages of using a water butt to store rainwater', 10,
               'Two distinct disadvantages, 5 marks each. Such as: storage is limited to the size of the butt, so supply runs out; the water is not pressurised; rainwater may be contaminated by dirt or other contaminants from the roof, so it is not drinking water.',
               [0, 5, 10])],
          RAIN, ['drainage'], None, 'Rainwater collected from gutters and downpipes (5.4).', B7, S7)
B7b = compose('7', 'b', '(b)', [B7a, B7d], None, 'Part (b) keeps the union of both required lists.', B7, S7,
              text='Discuss two advantages and two disadvantages of using a water butt to store rainwater.',
              labels=['advantages', 'disadvantages'])
C7 = add('7', 'c', '(c)', 'Discuss two reasons why it is advisable to harvest rainwater.',
         [row('reasons', 'Two reasons why it is advisable to harvest rainwater', 10,
              'Two distinct reasons, 5 marks each. Such as: it encourages water conservation and supplements the mains supply; most sloped roofs already act as collectors; it can be used for tasks that do not need potable water; storage can be sized to demand and provides water in drought; it reduces demand on wells and helps maintain ground water levels; large storage units can reduce flooding in low-lying areas.',
              [0, 5, 10])],
         RAIN, ['drainage'], None, 'Harvesting surface water from roofs (5.4).', B7, S7)
compose('7', 'complete', ' — complete', [A7, B7b, C7], 'q7-water-butt',
        'Complete Question 7 keeps the union of its separately reviewed parts.', B7, S7,
        text='(a) ' + A7['questionText'] + '\n\n(b) ' + B7b['questionText'] + '\n\n(c) ' + C7['questionText'])

# ---------------------------------------------------------------- Q8
B8 = 'Scheme p24: five items, each primary communication of relevant information 6 plus other communication 4 = 10; complete 50. The scheme does not split each item into fixed notes/sketch marks.'
S8 = 'Closed choose-five pool of nine printed terms: nine separately practicable 10-mark term tasks plus all C(9,5) = 126 complete 50-mark routes. Route marks are never added across unchosen terms.'
TERMS = [
    ('box-dovetail-joint', 'box dovetail joint', 12, ['cons-10-2', 'cons-10-4'], ['wood-rot-ventilation'],
     'Such as: a joint for box shapes and a common joint in high-quality furniture, made by hand or with special jigs; the slope of the dovetails matters for strength, usually 1:6 in softwood and 1:8 in hardwood; it gives a decorative appearance, sometimes highlighted with contrasting woods. A sketch should show the interlocking tails and pins at the corner.',
     'Box construction (10.2) and choice of joint for strength and decorative effect (10.4). The Ordinary reference taxonomy has no joinery heading; the original question is browsed under its existing Wood, Rot & Ventilation association, and 10.2/10.4 are declared outside that heading\'s crosswalk.'),
    ('triple-glazing', 'triple glazing', 12, ['cons-3-6', 'cons-6-2', 'cons-6-6'],
     ['windows-doors', 'heat-loss-insulation', 'air-tightness-condensation'],
     'Such as: three panes of glass with a cavity between each; a better insulator and better acoustic performance than double glazing; low-e coatings reflect heat back into the house; cavities filled with argon or krypton reduce heat loss; an improved window U-value, a more comfortable indoor temperature and reduced condensation. A sketch should show the three panes, spacers and cavities.',
     'Glass and glazing (3.6), insulating performance (6.2) and reduced surface condensation (6.6).'),
    ('solar-panel', 'solar panel', 13, ['cons-6-4', 'cons-5-3'], ['planning-sustainability-environment', 'hot-water-space-heating'],
     'Such as: a solar collector absorbs solar radiation and converts it to heat, usually on a south-facing roof or secure ground-level fixing, working with other forms of heating and reducing CO2 emissions; types include flat-plate and evacuated-tube collectors, and tubes can be mounted to follow the sun. The scheme also lists photovoltaic panels: a coherent explanation of either is acceptable, but a photovoltaic panel produces electricity, not heat.',
     'Solar heat gain (6.4) used by a heating/hot-water system (5.3).'),
    ('cordless-drill', 'cordless drill', 13, ['cons-9-2', 'cons-9-4'], ['site-safety'],
     'Such as: battery operated with rechargeable batteries, so not directly connected to AC mains power in use; features similar to a mains drill, including hammer action; used for driving screws, with a clutch to prevent damage to screw heads; right-angle versions for tight spaces; several power and speed settings, light low-voltage drills for DIY and heavier higher-voltage drills for robust work. A sketch should show the drill body, chuck and battery.',
     'Power tools and their uses (9.2) and safety with electricity (9.4). The Ordinary reference taxonomy has no tools heading; 9.2 is declared outside the Site Safety crosswalk, which covers 9.4.'),
    ('skirting-board', 'skirting board', 13, ['cons-4-5'], ['windows-doors'],
     'Such as: a decorative board fitted at the junction of a wall and floor, giving a neat finish; hardwood, softwood or MDF in various lengths and profiles; typical sections from 100 mm × 15 mm to 200 mm × 20 mm; mitred at internal and external corners. A sketch should show the board fixed at the wall–floor junction.',
     'Second-fixing joinery (4.5).'),
    ('compression-fitting', 'compression fitting', 14, ['cons-5-2', 'cons-5-1'], ['services-water-gas-electrical'],
     'Such as: a plumbing joint for copper or PVC pipes, made of brass or PVC in a range of sizes; the pipe ends are cut square, the nut and olive are fitted over the pipe, the pipe is pushed into the fitting and the nut is tightened to compress the olive into a watertight joint; PTFE tape may be used. A sketch should show the body, nut, olive and pipe.',
     'Water supply pipework (5.2) and service installation materials (5.1).'),
    ('natural-seasoning', 'natural seasoning', 14, ['cons-10-3'], ['wood-rot-ventilation'],
     'Such as: a traditional method of reducing the moisture content of timber; planks are stacked parallel with spaces between, separated by stickers (usually about 25 mm × 15 mm), in an open shed on a clean, dry, level base such as brick piers, and dried by the prevailing weather; plank ends are painted to prevent splitting; one species per stack; moisture content falls to about 18–22%, in equilibrium with the surrounding air; cheap because it uses no electrical energy, but slow and the rate cannot be controlled. A sketch should show the stacked planks, stickers and cover.',
     'Timber as a construction material (10.3). The outgoing registry has no separate timber-seasoning node; the reviewed Ordinary Wood, Rot & Ventilation crosswalk node for timber boards is used, matching the question\'s existing Atlas association.'),
    ('concrete-lintel', 'concrete lintel', 14, ['cons-3-4'], ['foundations-floors-walls'],
     'Such as: a reinforced concrete beam spanning a door or window opening, carrying the blockwork or brickwork above and transferring the load to the wall at either side; cast in situ or, more commonly, pre-stressed; the length depends on the opening width and the imposed loads, and pre-stressed lintels come in a range of lengths and widths. A sketch should show the lintel bearing on the wall either side of the opening.',
     'Lintels over openings (3.4).'),
    ('radon-barrier', 'radon barrier', 15, ['cons-3-4', 'cons-4-2'], ['foundations-floors-walls'],
     'Such as: a flexible membrane placed under the floor and extended through the external walls to prevent radon gas entering the building; fitted over the whole floor area as one complete, unbroken layer with all joints taped and sealed, including around service pipes; usually laid over sand blinding (which protects it) and beneath the insulation; it replaces the damp proof membrane; installed with care by trained personnel so it is not damaged. Only a membrane rated and detailed as a radon barrier does this job.',
     'Membranes (3.4) within the solid ground floor (4.2).'),
]
assert [t[0] for t in TERMS] == ['box-dovetail-joint', 'triple-glazing', 'solar-panel', 'cordless-drill', 'skirting-board',
                                 'compression-fitting', 'natural-seasoning', 'concrete-lintel', 'radon-barrier']
term_cards = []
for slug, item, page, nodes, topics, content, review in TERMS:
    term_cards.append(add('8', slug, f' — {item}',
                          f'Explain, with the aid of notes and freehand sketches: {item}.',
                          [row('primary', 'Primary communication of relevant information', 6,
                               f'Explain the {item} with notes and freehand sketches; the main relevant explanation earns up to 6. ' + content,
                               list(range(7))),
                           row('other', 'Other communication of relevant information', 4,
                               f'Further relevant information about the {item}, in notes or sketches, earns up to 4. The scheme does not reserve fixed marks for notes versus sketches.',
                               list(range(5)))],
                          nodes, topics, f'q8-{slug}', review, B8, S8, scheme_pages=[page, 24]))
routes = []
for combo in itertools.combinations(range(9), 5):
    chosen = [term_cards[i] for i in combo]
    names = [TERMS[i][1] for i in combo]
    slugs = [TERMS[i][0] for i in combo]
    pages = sorted({TERMS[i][2] for i in combo}) + [24]
    routes.append(compose('8', 'complete-' + '--'.join(slugs), ' — complete: ' + ', '.join(names), chosen, None,
                          'This complete route keeps the union of its five separately reviewed terms.', B8, S8,
                          text='Explain, with the aid of notes and freehand sketches, any five of the following: ' + '; '.join(names) + '.',
                          labels=names, scheme_pages=pages))
assert len(routes) == 126

# ---------------------------------------------------------------- Q9
B9 = 'Scheme p25: (a) suitable joint 4, valid reason 4, sketch quality 8 (8/6/4) = 16; (b) two design features × 4 = 8 plus sketch quality 8 = 16; (c) recommended finish 4, two preparation/application details × 5 = 10, sketch quality 4 (4/3/2) = 18. Complete 50.'
S9 = '"One of the rail" is any one identical rail-to-leg junction and the joint is an open choice; design features and finish are open. No finite printed option pool.'
A9 = add('9', 'a', '(a)',
         'Using notes and freehand sketches, show a suitable joint for attaching one of the rail to the leg of the table. Give one reason for choosing this joint.',
         [row('joint', 'Suitable joint', 4,
              'Name and describe a suitable joint, 4 marks. The scheme model is a haunched mortise and tenon: a mortise is removed from the top of the leg, the end of the rail is cut and shaped as a tenon to fit it, and a haunch formed on the tenon fits a matching recess, preventing the rail twisting and increasing the gluing surface. Any other suitable joint is acceptable.',
              [0, 4]),
          row('reason', 'Valid reason', 4,
              'One valid reason, 4 marks. Such as: the joint is strong and sturdy with a large glue contact area; it suits outdoor use when assembled with waterproof glue.', [0, 4]),
          row('sketch', 'Suitable joint for attaching a rail to a leg of the table - Sketches', 8,
              'Quality of sketches of the joint: excellent 8, good 6, fair 4.', BAND8)],
         ['cons-10-4', 'cons-10-6'], ['wood-rot-ventilation'], 'q9-joint',
         'Choice of joint (10.4) and waterproof glue (10.6). The Ordinary reference taxonomy has no joinery heading; the original question keeps its existing Wood, Rot & Ventilation association and 10.4/10.6 are declared outside that heading\'s crosswalk.',
         B9, S9)
B9b = add('9', 'b', '(b)',
          'Using notes and freehand sketches, discuss two design features that make the table suitable for outdoor use.',
          [row('features', 'Two design features that make the table suitable for outside use - Notes', 8,
               'Two distinct design features, 4 marks each. Such as: gaps between the top boards let water drip off and allow the boards to expand and contract; solid wood that, with maintenance, withstands the elements; sturdy, strong members; the top boards cover the end grain of the legs so it cannot absorb moisture; spacing that makes future maintenance easy.',
               [0, 4, 8]),
           row('sketch', 'Two design features that make the table suitable for outside use - Sketches', 8,
               'Quality of sketches of the features: excellent 8, good 6, fair 4.', BAND8)],
          ['cons-10-3'], ['wood-rot-ventilation'], 'q9-table-features',
          'Solid timber boards spaced for movement and protected from moisture (10.3). Exposure to the elements (1.7) is not a reviewed canonical library node, so it is not claimed.',
          B9, S9)
C9 = add('9', 'c', '(c)',
         'Recommend a suitable finish for the table. Describe, using notes and freehand sketches, the steps involved in preparing the wood and in applying the recommended finish to the tabletop.',
         [row('finish', 'Recommended finish', 4,
              'A suitable outdoor finish, 4 marks. Such as: paint; Danish, tung, teak or other oils; water-based varnishes, paints and preservatives; any other suitable finish.', [0, 4]),
          row('steps', 'Preparing the wood and applying the recommended finish to tabletop - Notes', 10,
              'Two valid preparation/application details, 5 marks each. Such as, for paint: clean and sand, remove dust with white spirit, prime, sand with fine glasspaper, undercoat, sand and clean, then two top coats. For varnish or stain: sand and clean, apply by brush, cloth or spray gun, two or three coats, sanding between coats. For oil: clean and sand, apply with a brush or lint-free cloth, several coats sanded between, re-oiled over the years.',
              [0, 5, 10]),
          row('sketch', 'Preparing the wood and applying the recommended finish to tabletop - Sketches', 4,
              'Quality of sketches: excellent 4, good 3, fair 2.', BAND4)],
         ['cons-10-7'], ['wood-rot-ventilation'], 'q9-finish', 'Surface preparation and finishing (10.7).', B9, S9)
compose('9', 'complete', ' — complete', [A9, B9b, C9], 'q9-joint',
        'Complete Question 9 keeps the union of its separately reviewed parts.', B9, S9,
        text='(a) ' + A9['questionText'] + '\n\n(b) ' + B9b['questionText'] + '\n\n(c) ' + C9['questionText'])

# ---------------------------------------------------------------- ledgers
intake = json.loads((HERE.parent / 'construction-2015-ordinary-intake/source-intake.json').read_text())
ledger = json.loads((HERE.parent / 'construction-2015-ordinary-intake/selection-ledger.json').read_text())
whole = {q: [c['id'] for c in cards.values() if c['id'].startswith(f'{PREFIX}q{q}-complete')] for q in QUESTIONS}
route_ledgers = {
    '1': dict(wholeRoutes=[dict(id=PREFIX + 'q1-complete', parts=['a', 'b'], componentMarks=[40, 2], sharedQualityMarks=8, marks=50)],
              nonChoices=['Best-nine scheme detail menu is not a printed finite option pool.', 'One suitable wallplate securing method is an open response.']),
    '2': dict(wholeRoutes=[dict(id=PREFIX + 'q2-complete', parts=['a', 'b'], componentMarks=[40, 10], marks=50)],
              requiredSystems=['filling the cavity with insulation', 'adding an external system of insulation to the wall'],
              nonChoices=['The two insulation systems are joined by AND and (a) asks for each: both required.', 'Advantages in (b) are open.']),
    '3': dict(wholeRoutes=[dict(id=PREFIX + 'q3-complete', parts=['a', 'b'], componentMarks=[40, 10], marks=50)],
              nonChoices=['The four bulleted diagram contents are required, not a choice.', 'Best-eight detail list is a marking menu.', 'Water-saving methods in (b) are open.']),
    '4': dict(wholeRoutes=[dict(id=PREFIX + 'q4-complete', parts=['a', 'b', 'c'], componentMarks=[20, 12, 18], marks=50)],
              requiredLocations=['entrance', 'driveway', 'septic tank and percolation area'],
              nonChoices=['Each of the three printed locations is required in (a) and (b).', 'Tree types and advantages in (c) are open.']),
    '5': dict(wholeRoutes=[dict(id=PREFIX + 'q5-complete', parts=['a', 'b'], componentMarks=[39, 3], sharedQualityMarks=8, marks=50)],
              nonChoices=['Best-seven scheme detail menu is not a printed finite option pool.', 'Wall AND floor insulation share one 3-mark allowance.']),
    '6': dict(wholeRoutes=[dict(id=PREFIX + 'q6-complete', parts=['a', 'b', 'c'], componentMarks=[24, 12, 14], marks=50)],
              requiredPpe=['hand protection', 'ear protection', 'eye protection'],
              nonChoices=['Each of the three PPE types is required in (a) and (b).', 'Classroom activities in (c) are open.']),
    '7': dict(wholeRoutes=[dict(id=PREFIX + 'q7-complete', parts=['a', 'b', 'c'], componentMarks=[20, 20, 10], marks=50)],
              nonChoices=['Two advantages AND two disadvantages are both required in (b).', 'Reasons in (c) are open.']),
    '8': dict(choose=5, options=[t[1] for t in TERMS], termTasks=[c['id'] for c in term_cards],
              wholeRoutes=[dict(id=r['id'], parts=[g['label'] for g in r['taskGroups']], marks=50) for r in routes],
              figurePolicy='Each term card carries its own scheme illustration; a route card carries the original question crop and every constituent row, because one card holds one solution figure.'),
    '9': dict(wholeRoutes=[dict(id=PREFIX + 'q9-complete', parts=['a', 'b', 'c'], componentMarks=[16, 16, 18], marks=50)],
              nonChoices=['"One of the rail" names any one identical rail-to-leg junction; the joint is an open choice.', 'Design features and finish are open.']),
}
taxonomy_gaps = [
    dict(cardId=PREFIX + 'q8-box-dovetail-joint', canonicalTopicIds=['cons-10-2', 'cons-10-4'], atlasTopicId=CROSS + 'wood-rot-ventilation',
         reason='No Ordinary outgoing reference heading covers joinery (10.x joints).'),
    dict(cardId=PREFIX + 'q8-cordless-drill', canonicalTopicIds=['cons-9-2'], atlasTopicId=CROSS + 'site-safety',
         reason='No Ordinary outgoing reference heading covers tools (9.2).'),
    dict(cardId=PREFIX + 'q9-a', canonicalTopicIds=['cons-10-4', 'cons-10-6'], atlasTopicId=CROSS + 'wood-rot-ventilation',
         reason='No Ordinary outgoing reference heading covers joinery and glues (10.4, 10.6).'),
]
out = dict(schemaVersion=1, subjectId='construction-studies', year=2015, level='ordinary', lang='ev', sitting='main',
           paperKey='single', fileid='LC029GLP000EV.pdf', component='theory',
           status='Q1–Q9 source-reviewed draft; integration pending.', sourceHashes=HASHES,
           tasks=tasks, bindings=bindings, questionFigures=question_figures,
           addedIds=[t['card']['id'] for t in tasks], selectionLedger=ledger, questionRouteLedgers=route_ledgers,
           taxonomyGaps=taxonomy_gaps, questionsReviewed=list(QUESTIONS), unreviewedQuestions=[],
           sourceIntake='docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-intake/source-intake.json',
           q1DraftBasis='docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-q1-draft/q1-draft.json')
(HERE / 'ordinary-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(tasks=len(tasks), figures=len(question_figures), q8Routes=len(routes),
                      perQuestion={q: sum(1 for t in tasks if t['questionNumber'] == q) for q in QUESTIONS})))
