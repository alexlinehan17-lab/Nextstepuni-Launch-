"""Write the independent 2024 HL EV census draft from the full visual sweep.

The route set is the one the 2024 Higher Irish review mirrors task for task
(econ_review.validate_equivalences), so every (key, card, marks, topic) tuple
must equal the earlier review's; the sweep confirmed each one against the paper
and scheme. Boundary and topic reasons are re-written from this sweep.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2024/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2024/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2024-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
# Atlas nodes beyond the task topics, kept from the reviewed Atlas mapping: a
# required heading of a combined card that belongs to a second topic.
EXTRA = {'9': ['economics-1-3'], '14': ['economics-3-1'], '16': ['economics-2-2']}
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + EXTRA.get(str(n), [])))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})
q(1, [3], [5], [T('a', 6, 'seca-q1-a', '4-2'), T('b', 6, 'sa-q1-b', '4-2')],
  'a one 6 cell for the current-account calculation and the surplus verdict: (76 + 91) - (38 + 83) = 46bn, surplus. b 6 one advantage from five headed examples.',
  'The balance of payments current account and a surplus are International Trade & Competitiveness (4-2).')
q(2, [4], [6], [T('a', 6, 'sa-q2-a', '3-2'), T('b', 6, 'sa-q2-b', '3-2'), T('c', 6, 'sa-q2-c', '3-1')],
  'a 6 full employment. Answer either b 2@3 (two reasons, four examples) OR c 2@3 (two conflicting aims, four examples): both alternatives carded.',
  'Full employment is Employment & Unemployment (3-2); conflicts between government aims are Fiscal Policy & the Budget (3-1).')
q(3, [5], [7], [T('a', 6, 'sa-q3-a', '1-3'), T('b', 6, 'sa-q3-b', '1-3'), T('c', 6, 'sa-q3-c', '1-3')],
  'a one 6 cell for the altered diagram: a €200 ceiling below Pe with excess demand S1 to D1 (hidden solution diagram, whole printed question shown). Answer b 2@3 price ceiling (three explanation points) OR c 2@3 reasons for the €450 credit (four headed examples).',
  'A price ceiling and an energy credit are Government Intervention (1-3).')
q(4, [6], [8], [T('a', 6, 'seca-q4-a-ticks', '1-5'), T('b', 6, 'sa-q4-b', '2-1'), T('c', 6, 'sa-q4-c', '1-5')],
  'a one 6 cell for the objective tick (capital deepening, 1:1 to 2:1) and its explanation (hidden solution, whole printed question shown). Answer b 2@3 demand-for-labour factors (eight headed examples) OR c 6 MEC.',
  'Capital deepening and the MEC sit with Costs of Production, Revenue & Profit (1-5); the demand for labour is The Labour Market (2-1).')
q(5, [7], [9], [T('a', 8, 'sa-q5-a', '1-0'), T('b', 4, 'sa-q5-b', '1-0')],
  'a 8 diagram: vertical supply at 80,000, €97.10 below equilibrium, excess demand (hidden solution diagram). b 4 explanation.',
  'A fixed-capacity shortage is demand, supply and equilibrium in The Market Economy (1-0).')
q(6, [8], [10], [T('a/diagram', 5, 'sa-q6-a-diagram', '1-5'), T('a/explanation', 3, 'sa-q6-a', '1-5'), T('b', 4, 'sa-q6-b-down', '1-5')],
  'a diagram 5 and explanation 3 in separate cells, two cards. b 2@2 required headings Downward sloping part (specialisation OR spread of fixed costs) and Upward sloping part (diminishing returns) in one card; the old upward-only card resolves by alias.',
  'Short-run average and marginal cost are Costs of Production, Revenue & Profit (1-5).')
q(7, [9], [11], [T('a', 6, 'sa-q7-a', '2-2'), T('b', 6, 'sa-q7-b', '1-3')],
  'a 6 one explanation from four statements. b 2@3 two interventions from five headed examples.',
  'Vaping as a demerit good is Market Failure (2-2); intervening in the market is Government Intervention (1-3).')
q(8, [10], [12], [T('a', 6, 'sa-q8-a', '2-0'), T('b', 6, 'sa-q8-b', '2-0')],
  'a explanation 4 + example 2 (four example bullets). b 2@3 two consumer characteristics from three.',
  'Price discrimination is Market Structures (2-0).')
q(9, [11], [13], [T('a', 6, 'sa-q9-a-cost', '0-1'), T('b', 6, 'sa-q9-b', '2-2')],
  'a required headings opportunity cost 3 + social benefit 3 in one card; the old benefit-only card resolves by alias. b 6 positive externality, one of three statements.',
  'Opportunity cost is Scarcity & Choice (0-1); a positive externality is Market Failure (2-2); a state forestry pledge and a public university are Government Intervention (1-3).')
q(10, [12], [14], [T('a/ii', 6, 'sa-q10-a-ii', '3-0'), T('b', 6, 'sa-q10-b', '3-0')],
  'a(i) GDP to GNP is completed on the paper and is not a task (the only exclusion). a(ii) 6: GNI = 325 + 2 - 0.5 = 326.5bn (hidden solution ladder, whole printed question shown). b 6 NFIA.',
  'GDP, GNP, GNI and NFIA are National Income (3-0).')
q(11, [13, 14, 15, 16], [15, 16, 17, 18, 19, 20],
  [T('a/i', 8, 'q11-a-i', '4-2'), T('a/ii', 6, 'q11-a-ii', '3-0'), T('a/iii', 6, 'q11-a-iii', '4-2'),
   T('b/i/calculation', 12, 'q11-b-i', '3-0'), T('b/i/meaning', 4, 'q11-b-i-meaning', '3-0'),
   T('b/ii', 4, 'q11-b-ii', '3-0'), T('b/iii', 8, 'q11-b-iii', '3-0'),
   T('c/i/diagram', 5, 'q11-c-i-diagram', '1-0'), T('c/i/explanation', 4, 'q11-c-i', '1-0'),
   T('c/ii/diagram', 5, 'q11-c-ii-diagram', '1-0'), T('c/ii/explanation', 4, 'q11-c-ii', '1-0'),
   T('c/iii/diagram', 5, 'q11-c-iii-diagram', '1-0'), T('c/iii/explanation', 4, 'q11-c-iii', '1-0')],
  'Thirteen tasks totalling 75. a(i) 8 = 94.11% / 94% (-1 if % omitted); a(ii) 6; a(iii) 1 @ 6 from five. b(i) calculation 12 (1.08; Method 1 and Method 2 are equivalent workings, not routes) and meaning 4 in separate cells; b(ii) 4; b(iii) 2 @ 4 from six. c(i)-(iii) each a diagram 5 @ 1 (hidden solution) and an explanation 4 @ 1 (shift, price, quantity, cause) in separate cells.',
  'Tourist numbers and their costs are International Trade & Competitiveness (4-2); the circular flow, the multiplier and national income statistics are National Income (3-0); shifts in demand and supply are The Market Economy (1-0).')
q(12, [17, 18, 19, 20], [21, 22, 23, 24, 25, 26],
  [T('a/i', 10, 'q12-a-i', '3-1'), T('a/ii', 10, 'q12-a-ii', '3-0'),
   T('a/iii/taxpayer', 4, 'q12-a-iii-tax', '3-1'), T('a/iii/government', 4, 'q12-a-iii-gov', '3-1'),
   T('b/i', 6, 'q12-b-i', '3-3'), T('b/ii', 19, 'q12-b-ii', '3-3'), T('b/iii', 6, 'q12-b-iii', '3-3'),
   T('c/i', 6, 'q12-c-i', '1-3'), T('c/ii', 4, 'q12-c-ii', '2-2'), T('c/iii', 10, 'q12-c-iii', '1-1')],
  'Ten routes; 75 with one route for a(iii). a(i) 2 @ 5 canons other than certainty (eight); a(ii) 2 @ 5 (six). a(iii) printed Tax payer / Government tick at 1 @ 4, the scheme lists both sides: two routes 4 each. b(i) 6 trend of the inflation rate; b(ii) 19 for the whole composite-index table, 119.5, no per-row split (hidden solution worksheet, whole printed question shown); b(iii) 2 @ 3 (six). c(i) 1 @ 4 then 1 @ 2; c(ii) 1 @ 4 (five); c(iii) 2 @ 5 assumptions other than limited incomes (three).',
  'Canons of taxation and a middle tax rate are Fiscal Policy & the Budget (3-1); the hidden economy is National Income (3-0); the CPI and inflation are Monetary Policy & Inflation (3-3); gambling regulation is Government Intervention (1-3); demerit goods are Market Failure (2-2); assumptions of consumer behaviour are The Consumer (1-1).')
q(13, [21, 22, 23, 24], [27, 28, 29, 30, 31, 32, 33],
  [T('a/i', 8, 'q13-a-i', '3-5'), T('a/ii', 10, 'q13-a-ii', '3-5'), T('a/iii', 10, 'q13-a-iii', '1-3'),
   T('b/i', 6, 'q13-b-i', '4-1'), T('b/ii', 10, 'q13-b-ii', '4-1'), T('b/iii', 10, 'q13-b-iii-pos', '4-1'),
   T('c/i', 8, 'q13-c-i', '3-1'), T('c/ii', 7, 'q13-c-ii', '3-1'), T('c/iii', 6, 'q13-c-iii-pos', '3-1')],
  'Nine tasks totalling 75. a(i) 8 = 52.63% (-1 for %); a(ii) and a(iii) 1 @ 6 then 1 @ 4. b(i) 6 one of four formulations; b(ii) 1 @ 6 then 1 @ 4; b(iii) required Positive AND Negative priced 1 @ 6 then 1 @ 4 across the pair (no fixed share per heading), one card; the old negative card resolves by alias. c(i) 2 @ 4 trend with data + reason; c(ii) 7; c(iii) required positive 1 @ 3 + negative 1 @ 3, one card; the old negative card resolves by alias.',
  'Population and migration are Economic Growth (3-5); the Vacant Home Tax is Government Intervention (1-3); globalisation is Globalisation (4-1); corporation tax and a budget surplus are Fiscal Policy & the Budget (3-1).')
q(14, [25, 26, 27, 28], [34, 35, 36, 37],
  [T('a/i', 15, 'q14-a-i', '2-0'), T('a/ii/agree', 6, 'q14-a-ii-agree', '2-0'), T('a/ii/disagree', 6, 'q14-a-ii-disagree', '2-0'),
   T('b/i/diagram', 12, 'q14-b-i', '2-0'), T('b/i/explanation', 9, 'q14-b-i-explanation', '2-0'), T('b/ii', 5, 'q14-b-ii', '2-0'),
   T('c/i', 8, 'q14-c-i-spending', '3-3'), T('c/ii', 8, 'q14-c-ii', '3-3'), T('c/iii', 12, 'q14-c-iii', '3-4')],
  'Nine routes; 75 with one route for a(ii). a(i) 3 @ 5 other than many sellers (five). a(ii) printed Agree/Disagree tick, 1 @ 6, the scheme lists both: two routes 6 each. b(i) diagram 12 (12 x 1 labels) and explanation 9 in separate cells (hidden solution diagram); b(ii) 1 @ 5 (four). c(i) required headings consumer spending 4 + cost of servicing the national debt 4 (2 @ 4), one card; the old debt card resolves by alias. c(ii) 8 = -3.25%; c(iii) 2 @ 6 (five).',
  'Monopolistic competition is Market Structures (2-0); ECB rate rises and the real rate of interest are Monetary Policy & Inflation (3-3); neobanks are the Financial Sector (3-4); the cost of servicing the national debt is Fiscal Policy & the Budget (3-1).')
q(15, [29, 30, 31, 32], [38, 39, 40, 41, 42],
  [T('a/i', 8, 'q15-a-i', '4-0'), T('a/ii', 5, 'q15-a-ii', '4-0'), T('a/iii', 10, 'q15-a-iii', '4-0'),
   T('b/i', 8, 'q15-b-i', '4-2'), T('b/ii', 10, 'q15-b-ii', '4-2'), T('b/iii', 4, 'q15-b-iii', '3-5'),
   T('c/i', 10, 'q15-c-i', '4-1'), T('c/ii', 10, 'q15-c-ii-economic', '1-3'), T('c/iii', 10, 'q15-c-iii', '2-2')],
  'Nine tasks totalling 75. a(i) 8 = 95.45% (-1 for %); a(ii) 5 one step (four headed); a(iii) 1 @ 6 then 1 @ 4. b(i) 2 @ 4 (six); b(ii) required headings exports AND imports 2 @ 5, one answer each; b(iii) 4 recession. c(i) 1 @ 6 then 1 @ 4; c(ii) required Economic AND Social measures priced 1 @ 6 then 1 @ 4 across the pair, one card; the old social card resolves by alias; c(iii) 1 @ 6 then 1 @ 4.',
  'LDC debt and aid are Growth & Development (4-0); competitiveness and the exchange rate are International Trade & Competitiveness (4-2); a recession is Economic Growth (3-5); EU membership is Globalisation (4-1); obesity measures are Government Intervention (1-3); the costs of data centres are Market Failure (2-2).')
q(16, [33, 34, 35, 36], [43, 44, 45, 46, 47],
  [T('a/i', 10, 'q16-a-i', '1-3'), T('a/ii', 10, 'q16-a-ii', '1-3'),
   T('b/i', 8, 'q16-b-i', '1-4'), T('b/ii/calculation', 9, 'q16-b-ii', '1-4'), T('b/ii/meaning', 4, 'q16-b-ii-meaning', '1-4'),
   T('b/iii', 6, 'q16-b-iii', '1-4'), T('c/i', 6, 'q16-c-i', '3-1'), T('c/ii', 10, 'q16-c-ii-cost', '0-1'),
   T('c/iii', 12, 'q16-c-iii-advantage', '3-1')],
  'Nine tasks totalling 75. a(i) and a(ii) 1 @ 6 then 1 @ 4. b(i) 8; b(ii) workings 9 (+0.8; the scheme table labels the paper\'s 2022/2023 rows 2021/2022) and meaning 4 in separate cells; b(iii) 6 = 7,400 units (the scheme labels the paper\'s 2023/2024 as 2022/2023). c(i) explain 4 + example other than transport 2; c(ii) required social cost 5 + social benefit 5 (2 @ 5), one card; the old benefit card resolves by alias; c(iii) 2 @ 6 with a MINIMUM of ONE advantage and one disadvantage, one card; the old disadvantage card resolves by alias.',
  'Homelessness and social housing are Government Intervention (1-3); income elasticity is Elasticity (1-4); capital expenditure and indirect taxation are Fiscal Policy & the Budget (3-1); social cost and benefit is Scarcity & Choice (0-1), and the DART+ social costs and benefits are externalities, Market Failure (2-2).')

SEL = {
 'Answer 4 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 4 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 8 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Questions 2, 3 and 4 contain an internal choice.': ('finite-route', 'Q2, Q3 and Q4 each offer (b) OR (c); every alternative is its own carded task.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer either (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'Answer (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (b)/(c) alternatives.'),
}
PAGE_SEL = {
 (3, 'State whether it is a surplus or a deficit. Show all your workings.'): ('answer-classification', 'Q1(a) the current account is objectively a surplus; one card.'),
 (3, 'Surplus or Deficit?'): ('answer-classification', 'Q1(a) answer box for the objective surplus verdict.'),
 (4, 'Explain how any other two current economic aims of the government may conflict with this'): ('not-a-task-selection', 'Q2(c) "any other two" aims is an open response, not a printed pool.'),
 (6, 'From the information given above, tick () one of the boxes below to indicate whether the firm'): ('answer-classification', 'Q4(a) the ratio decides the box (capital deepening); one card.'),
 (6, 'has engaged in capital widening or capital deepening and explain your answer.'): ('answer-classification', 'Q4(a) tick with one correct answer.'),
 (6, 'No. of machines 5 10'): ('not-a-task-selection', 'Table row ("No." abbreviates number), not a selection.'),
 (6, 'No. of workers 5 5'): ('not-a-task-selection', 'Table row ("No." abbreviates number), not a selection.'),
 (17, '(a) (i) The principle of certainty is one of the canons of taxation, i.e. tax payers should be'): ('not-a-task-selection', 'The certainty canon is given as an example and excluded ("two other canons"); not a selection.'),
 (17, 'Outline one economic consequence for either the tax payer or the government if this'): ('finite-route', 'Q12(a)(iii) tax payer OR government tick; the scheme lists both sides, two routes.'),
 (25, '(ii) Firms operating under monopolistic competition waste resources. Do you agree or'): ('finite-route', 'Q14(a)(ii) agree/disagree routes; the scheme lists both.'),
 (25, 'disagree with this statement? Indicate your choice below by ticking () the relevant'): ('finite-route', 'Q14(a)(ii) stance tick boxes.'),
 (25, 'box and justify your choice.'): ('finite-route', 'Q14(a)(ii) tail of the stance instruction.'),
 (25, 'Agree: Disagree:'): ('finite-route', 'Q14(a)(ii) printed stance boxes.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 40: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# The route tuples must equal the earlier review's, which the Irish review mirrors.
old = json.loads((W / 'scripts/markbank/authoring/reviews/economics-2024-hl-ev.json').read_text())
tup = lambda qs: sorted((x['n'], t['key'], t['cardId'], t['marks'], t['topicId']) for x in qs for t in x['tasks'])
if tup(Q) != tup(old['questions']):
    raise SystemExit('route tuples differ from the reviewed (Irish-mirrored) set')
for x, o in zip(Q, old['questions']):
    assert x['paperPages'] == o['paperPages'], x['n']
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2024, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 41)), 'visuallyInspectedSchemePages': list(range(1, 53)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Re-review 2026-10-12 from a fresh paired visual sweep of all 40 paper and 52 scheme pages (scheme PDF page = printed page). {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified; the route set equals the earlier review and the Irish review that mirrors it. Every stem and ask is now sliced from the paper and every menu from the scheme\'s own headings (econ_2024_hl.py; the Section A script and the correction module are retired). Eight split required-heading cards stay consolidated with progress aliases. Q10(a)(i) is completed on the paper and excluded. Scheme pp48-51 student research project descriptors and p52 back cover: no written-paper asks. Choose-N rule checked: no printed choose-N-of-M item pool on this paper.',
 'externalClarifications': old.get('externalClarifications', []),
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2024-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
