"""Write the independent 2012 OL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2012 Ordinary
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2012/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2012/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2012-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: none on this paper (no printed stance or
# either-or choice is credited with a list for each side).
ALT = ()

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('a', 2, 'sa-q1-a', '3-1'), T('b', 14, 'sa-q1-b', '3-1')],
  'a 2 (Adam Smith); b the four matches, the first two correct 4 each and the 3rd and 4th 3 each: one card, the canons table beside the typed lists.',
  'Adam Smith’s canons of taxation are Fiscal Policy & the Budget (3-1).')
q(2, [2], [5], [T('all', 16, 'sa-q2', '1-3')],
  'Two advantages from ten: the 1st correct 12, the 2nd 4.',
  'The cycle-to-work scheme, a government tax incentive to change behaviour, is Government Intervention (1-3); its congestion and emissions benefits are also Market Failure (2-2).', also=['2-2'])
q(3, [2], [6], [T('all', 16, 'sa-q3', '2-1')],
  'The three blanks (human; goods; wages / salary): the 1st correct 8, the 2nd and 3rd 4 each: one card.',
  'Labour as a factor of production and its payment, wages, are The Labour Market (2-1); the factors of production are also Scarcity & Choice (0-1).', also=['0-1'])
q(4, [2], [6], [T('all', 16, 'sa-q4', '3-1')],
  'Two effects from seven: the 1st correct 12, the 2nd 4.',
  'Austerity and reducing the government budget deficit are Fiscal Policy & the Budget (3-1).')
q(5, [2], [6], [T('all', 16, 'sa-q5', '1-3')],
  'The explanation 6 + the five words of EU and IMF in full at 2 each (EU 4, IMF 6): one card, three rows.',
  'Privatisation is Government Intervention (1-3); using its revenue to reduce the national debt is also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q(6, [3], [7], [T('all', 17, 'sa-q6', '1-4')],
  'The four blank rows of the table (∆P, P1, P2, Q2): the 1st correct 8, the 2nd, 3rd and 4th 3 each: one card, the formula and table as the crop.',
  'The price elasticity of demand formula is Elasticity (1-4).')
q(7, [3], [7], [T('all', 17, 'sa-q7', '1-3')],
  'One action from nine and one advantage from five: the 1st correct 12, the 2nd 5, one of each: one card.',
  'Measures against alcohol consumption are Government Intervention (1-3); the benefits for society are also Market Failure (2-2).', also=['2-2'])
q(8, [3], [8], [T('all', 17, 'sa-q8', '3-2')],
  'The explanation and one other effect from eight: the 1st correct 11, the 2nd 6, one of each: one card.',
  'Emigration and its effects are Employment & Unemployment (3-2).')
q(9, [3], [8], [T('all', 17, 'sa-q9', '3-1')],
  'One effect for each of the three groups: the 1st correct 9, the 2nd and 3rd 4 each: one card.',
  'The VAT increase and the budget deficit are Fiscal Policy & the Budget (3-1); cross-border shopping is also International Trade & Competitiveness (4-2), and its effect on employment levels Employment & Unemployment (3-2).', also=['4-2', '3-2'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [9, 10, 11],
  [T('a/i', 20, 'sb-q1-a-i', '2-0'), T('a/ii', 10, 'sb-q1-a-ii', '2-0'), T('b/i', 7, 'sb-q1-b-i', '2-0'),
   T('b/ii-iii', 14, 'sb-q1-b-ii', '2-0'), T('c/i', 8, 'sb-q1-c-i', '2-0'), T('c/ii', 16, 'sb-q1-c-ii', '1-0')],
  'Six cards for seven asks, totalling 75. a(i) the five lines at 4; a(ii) Q1, P1 and C1, the 1st and 2nd correct 4 each and the 3rd 2 (hidden solution diagram). b(i) 7, either explanation; b(ii) and (iii) share one 2 at 7 (4 + 3), a characteristic with its note: one card covers both. c(i) 8 one competitor from two; c(ii) one effect per group, the 1st correct 8 (4 + 4) and the 2nd and 3rd 4 (2 + 2).',
  'Imperfect competition, its long-run equilibrium, close substitutes and competitors are Market Structures (2-0); the effects of higher electricity prices on consumers, other suppliers and the economy are The Market Economy (1-0), as 2013 OL files higher fuel prices.')
q('B2', [5], [12, 13, 14],
  [T('a/i', 9, 'sb-q2-a-i', '1-0'), T('a/ii', 6, 'sb-q2-a-ii', '1-0'), T('a/iii', 6, 'sb-q2-a-iii', '1-0'),
   T('b/i', 14, 'sb-q2-b-i', '1-1'), T('b/ii', 8, 'sb-q2-b-ii', '1-0'), T('b/iii', 8, 'sb-q2-b-iii', '1-1'),
   T('c/i', 12, 'sb-q2-c-i', '1-3'), T('c/ii', 12, 'sb-q2-c-ii', '1-3')],
  'Eight tasks totalling 75. a(i) the three lines at 3 (the scheme’s reprint reads “lines 1 and 3” and answers all three); a(ii) P1 3 + Q1 3 (hidden solution diagram); a(iii) 6. b(i) two factors at 7, each the factor 4 (“2 at 4 marks each”) and how it shifts the curve 3 (“2 at 3 marks each”), from six; b(ii) 8; b(iii) the good 4 + its effect 2 + the reason 2. c(i) one advantage 6 (3 + 3) from four + one disadvantage 6 from three; c(ii) one effect each on hauliers 6 and the current budget deficit 6.',
  'Demand, supply and equilibrium for match tickets are The Market Economy (1-0); the reasons demand shifts and complementary goods are The Consumer (Demand) (1-1); motorway tolls are Government Intervention (1-3), and their effect on the current budget deficit also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q('B3', [6], [15, 16, 17, 18, 19],
  [T('a/i', 3, 'sb-q3-a-i', '1-5'), T('a/ii', 12, 'sb-q3-a-ii', '1-5'), T('a/iii', 10, 'sb-q3-a-iii', '1-5'),
   T('b/i', 12, 'sb-q3-b-i', '0-1'), T('b/ii', 10, 'sb-q3-b-ii', '0-1'), T('b/iii', 8, 'sb-q3-b-iii', '0-1'),
   T('c/i', 6, 'sb-q3-c-i', '1-3'), T('c/ii', 14, 'sb-q3-c-ii', '1-0')],
  'Eight tasks totalling 75. a(i) 3, any of three; a(ii) each cost 6: the definition 3 + 1 (the scheme prints 3 marks beside “costs which do not change” and 1 beside “as output changes”) and one example 2, which the scheme does not name; a(iii) 2 at 5 (2 + 3) from four. b(i) Land, Labour and Capital 4 + 4 + 4; b(ii) 2 at 5 (2 + 3) from nine; b(iii) one action each for the government 4 (2 + 2) from nine and schools / colleges 4 (2 + 2) from four. c(i) 2 at 3 (2 + 1) from four; c(ii) 2 at 7 (4 + 3) from seven.',
  'Normal profit, fixed and variable costs and why profit matters are Costs of Production, Revenue & Profit (1-5); the factors of production, the entrepreneur and encouraging enterprise are Scarcity & Choice (0-1); a local authority’s measures to encourage shopping local are Government Intervention (1-3), and the benefits to the local economy The Market Economy (1-0).')
q('B4', [6], [20, 21, 22],
  [T('a/i', 10, 'sb-q4-a-i', '3-4'), T('a/ii', 5, 'sb-q4-a-ii', '3-4'), T('a/iii', 10, 'sb-q4-a-iii', '3-4'),
   T('b/i', 6, 'sb-q4-b-i', '3-5'), T('b/ii', 7, 'sb-q4-b-ii', '3-3'), T('b/iii', 12, 'sb-q4-b-iii', '3-5'),
   T('c/i', 4, 'sb-q4-c-i', '3-3'), T('c/ii', 6, 'sb-q4-c-ii', '3-3'), T('c/iii', 15, 'sb-q4-c-iii', '3-3')],
  'Nine tasks totalling 75. a(i) any two of the three terms at 5; a(ii) 5 (2 + 3), either difficulty; a(iii) 2 at 5 (2 + 3) from three functions. b(i) 6; b(ii) 7; b(iii) 2 at 6 (3 + 3) from eight. c(i) 4, either explanation; c(ii) 6; c(iii) one effect per group, the 1st correct 7 (4 + 3) and the 2nd and 3rd 4 (2 + 2).',
  'Money, its characteristics and functions and barter are Financial Sector (3-4); economic growth and its effects are Economic Growth (3-5); the ECB, price inflation, the CPI and a falling rate of inflation are Monetary Policy & Inflation (3-3).')
q('B5', [7], [23, 24],
  [T('a/i', 6, 'sb-q5-a-i', '3-0'), T('a/ii', 5, 'sb-q5-a-ii', '3-0'), T('a/iii', 14, 'sb-q5-a-iii', '3-0'),
   T('b/i', 12, 'sb-q5-b-i', '3-0'), T('b/ii', 8, 'sb-q5-b-ii', '3-0'), T('c/i', 6, 'sb-q5-c-i', '3-0'),
   T('c/ii', 12, 'sb-q5-c-ii', '3-0'), T('c/iii', 12, 'sb-q5-c-iii', '3-1')],
  'Eight tasks totalling 75. a(i) 6; a(ii) 5, any of three explanations; a(iii) 2 at 7 (4 + 3) from six. b(i) the multiplier 6 + an open economy 6; b(ii) 8 (hidden solution working; the paper’s formula beside the ask). c(i) 6; c(ii) 2 at 6, the scheme’s two examples; c(iii) 2 at 6 (3 + 3) from five.',
  'Transfer payments, national income statistics, the open-economy multiplier and the black economy are National Income (3-0), as earlier reviews file the black economy; the government’s actions against it (taxation, enforcement) are Fiscal Policy & the Budget (3-1).')
q('B6', [7], [25, 26, 27, 28],
  [T('a/i', 5, 'sb-q6-a-i', '3-2'), T('a/ii', 10, 'sb-q6-a-ii', '3-2'), T('a/iii', 15, 'sb-q6-a-iii', '3-1'),
   T('b/i', 5, 'sb-q6-b-i', '3-1'), T('b/ii', 15, 'sb-q6-b-ii', '3-1'), T('c/i', 7, 'sb-q6-c-i', '0-1'),
   T('c/ii', 18, 'sb-q6-c-ii', '1-3')],
  'Seven tasks totalling 75. a(i) 5; a(ii) 2 at 5 (2 + 3) from five; a(iii) 3 at 5 (2 + 3) from twelve. b(i) 5, any of three; b(ii) 3 at 5 (2 + 3) from four. c(i) 7, either explanation; c(ii) one effect each for households, businesses and the Irish economy at 6 (3 + 3): three heading rows.',
  'The Live Register and the advantages of reducing it are Employment & Unemployment (3-2); the government’s economic aims, infrastructure and capital spending are Fiscal Policy & the Budget (3-1); opportunity cost is Scarcity & Choice (0-1); government energy grants are Government Intervention (1-3), as earlier reviews file grants, and their environmental effect is also Sustainability (0-2).', also=['0-2'])
q('B7', [8], [29, 30, 31, 32],
  [T('a/i', 7, 'sb-q7-a-i', '4-2'), T('a/ii', 5, 'sb-q7-a-ii', '4-2'), T('a/iii', 8, 'sb-q7-a-iii', '4-2'),
   T('b/i', 10, 'sb-q7-b-i', '4-2'), T('b/ii', 15, 'sb-q7-b-ii', '4-2'), T('c/i', 10, 'sb-q7-c-i', '4-1'),
   T('c/ii', 10, 'sb-q7-c-ii', '4-1'), T('c/iii', 10, 'sb-q7-c-iii', '4-1')],
  'Eight tasks totalling 75. a(i) Cars 4 + why 3; a(ii) Wine 4 + why 1; a(iii) the eight starred workings at 1 (hidden solution table; the paper’s table beside the ask). b(i) the explanation 6 + one other example 4 from three; b(ii) 3 at 5 (2 + 3) from six (the scheme heads it “(i)”). c(i) any 2 companies at 5 from eleven; c(ii) 2 at 5 (2 + 3) from six; c(iii) 2 at 5 (2 + 3) from six.',
  'Comparative advantage, invisible imports and the benefits of exports are International Trade & Competitiveness (4-2); multinational companies are Globalisation (4-1).')
q('B8', [9], [33, 34, 35],
  [T('a', 21, 'sb-q8-a', '3-1'), T('b/i', 15, 'sb-q8-b-i', '3-1'), T('b/ii', 15, 'sb-q8-b-ii', '3-1'),
   T('c/i', 8, 'sb-q8-c-i', '3-1'), T('c/ii', 6, 'sb-q8-c-ii', '3-1'), T('c/iii', 10, 'sb-q8-c-iii', '3-1')],
  'Six tasks totalling 75. a any three of the four terms at 7: one card. b(i) the three taxes at 5; b(ii) one effect each for households, retailers and the current budget deficit at 5 (2 + 3): three heading rows. c(i) 8; c(ii) 6; c(iii) 2 at 5 (2 + 3) from seven.',
  'The current budget deficit, progressive tax, VAT, carbon taxes, the household charge, the NTMA and the national debt are Fiscal Policy & the Budget (3-1); nationalisation is also Government Intervention (1-3), and economic recession Economic Growth (3-5).', also=['1-3', '3-5'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 9': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 10)},
}
PAGE_SEL = {
 (2, 'Outline any two effects which government ‘austerity’ measures may have on Irish citizens.'): ('finite-route', 'Section A Q4 any two effects: one card, a menu of seven claimed at 12 then 4.'),
 (3, 'This is one of the effects of the current emigration of Irish citizens. Explain the underlined term and state'): ('not-a-task-selection', 'Section A Q8 stimulus, read on "one"; not a selection.'),
 (6, '(i) Explain any two of the underlined terms.'): ('finite-route', 'Section B Q4(a)(i) any two of three characteristics: one card claimed twice at 5.'),
 (7, '6. (a) One of the main economic aims of the Irish Government is to reduce the number on the'): ('not-a-task-selection', 'Section B Q6(a) stimulus, read on "One"; not a selection.'),
 (9, '(c) One of the functions of the NTMA is to manage Ireland’s National Debt on behalf of the'): ('not-a-task-selection', 'Section B Q8(c) stimulus, read on "One"; not a selection.'),
 (9, '8. (a) Explain any three of the following:'): ('finite-route', 'Section B Q8(a) any three of four terms: one card claimed three times at 7.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

tasks = [t for x in Q for t in x['tasks']]
for x in Q:
    total = sum(t['marks'] for t in x['tasks'] if not t['cardId'].endswith(ALT))
    want = 75 if x['n'].startswith('B') else (16 if int(x['n']) <= 5 else 17)
    assert total == want, (x['n'], total, want)
draft = {
 'subjectId': 'economics', 'year': 2012, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 40 scheme pages (paper pages 10-12 are blank; scheme pages 1-4 are the SEC cover, a blank page, the title page and the support notes with the index, page 36 is blank but for its page number, and pages 37-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 71 printed asks (10 Section A + 61 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2012_ol.py). One card covers two printed asks because the scheme prices them together: Section B Q1(b)(ii)-(iii). No printed choice is credited with a list for each side.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2012-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
