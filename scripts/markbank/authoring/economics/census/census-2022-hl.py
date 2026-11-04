"""Write the independent 2022 HL EV census draft from the full visual sweep (re-review 2026-10-12).

The route set is the one the 2022 Higher Irish review mirrors task for task
(econ_review.validate_equivalences), so every (key, card, marks, topic) tuple
must equal the earlier review's; the sweep confirmed each one. Boundary and
topic reasons are re-written from this sweep.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2022/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2022/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2022-hl-'
old = json.loads((W / 'scripts/markbank/authoring/reviews/economics-2022-hl-ev.json').read_text())
atlas = json.loads((W / 'data/examTopics/economics-sec-topic-reviews.json').read_text())
OLD_NODES = {q['n']: q['canonicalNodeIds'] for q in atlas['questions']
             if q['year'] == 2022 and q['level'] == 'higher' and q['lang'] == 'ev'}
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(OLD_NODES.get(str(n), []) + [t['topicId'] for t in tasks]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

q(1, [3], [5], [T('a', 10, 'sa-q1-a', '1-4'), T('b', 5, 'sa-q1-b', '1-1')],
  'a 10 PED = −3 off the face-mask graph (hidden working, whole printed question shown). b 5 the law of demand from the graph.',
  'Price elasticity is Elasticity (1-4); the law of demand is The Consumer (1-1).')
q(2, [4], [5], [T('a', 9, 'seca-q2-a', '4-2'), T('b', 6, 'sa-q2-b', '1-1')],
  'a 9 objective EXPANSIONARY with the export and import figures. b 6 (3 + 3) one factor behind the rise in personal consumption, four bullets.',
  'Exports, imports and the balance of payments are International Trade & Competitiveness (4-2), the national accounts National Income (3-0); personal consumption is The Consumer (1-1).')
q(3, [5], [6], [T('a/agree', 9, 'sa-q3-a-agree', '1-3'), T('a/disagree', 9, 'sa-q3-a-disagree', '1-3'), T('b', 6, 'sa-q3-b', '2-2')],
  'a printed Agree/Disagree; the scheme lists both sides, two routes at 9 (5 + 4). b 6 (3 + 3) market failure explained and illustrated.',
  'Minimum unit pricing is Government Intervention (1-3); alcohol as a market failure is Market Failure (2-2).')
q(4, [6], [7], [T('a', 8, 'seca-q4-a-ticks', '3-0'), T('b', 7, 'sa-q4-b', '3-0'), T('c', 7, 'sa-q4-c', '4-1')],
  'a 3 + 3 + 2 three objective classifications (hidden completed table, whole printed question shown). Answer (b) 7 (3 + 2 + 2) justify all three OR (c) 7 two FDI reasons; the scheme prints one 3 + 2 + 2 beside the choice and no per-reason value for (c).',
  'Injections and leakages are National Income (3-0); foreign direct investment is Globalisation (4-1).')
q(5, [7], [8, 9], [T('a', 7, 'sa-q5-a', '3-5'), T('b', 8, 'sa-q5-b', '2-1'), T('c', 7, 'sa-q5-c', '3-1')],
  'a 1 x 4, 1 x 3 two factors (the fourth bullet prints after the (b) marker). Answer (b) 4 + 4 OR (c) 7 (4 + 3): the printed asymmetry is kept.',
  'Population ageing is Economic Growth (3-5); its labour-market advantages The Labour Market (2-1); its policy impacts Fiscal Policy & the Budget (3-1).')
q(6, [8, 9], [10], [T('a+b', 15, 'sa-q6-a-b', '2-0'), T('a+c', 15, 'sa-q6-a-c', '2-0')],
  'The scheme prints 4, 2 and 2 beside (a) and nothing beside (b) or (c); two complete 15-mark routes, (a) with (b) and (a) with (c), unpriced rows (hidden completed diagrams). The old per-diagram cards resolve by alias.',
  'Perfect competition, entry and the price-taking firm are Market Structures (2-0).')
q(7, [10], [11], [T('a/i', 1, 'sa-q7-a-i', '3-3'), T('a/ii', 8, 'seca-q7-a-ii', '3-3'), T('b', 6, 'sa-q7-b', '3-4')],
  'a(i) 1 objective Figure B (the scheme writes 2021, the paper 2020); a(ii) 2 x 4 justify; b 2 x 3 two other ECB roles.',
  'The ECB rate is Monetary Policy & Inflation (3-3); the ECB’s roles are Financial Sector (3-4).')
q(8, [11], [12], [T('a', 5, 'sa-q8-a', '3-0'), T('b', 10, 'sa-q8-b', '4-2')],
  'a 5 the hidden economy (three wordings). b 2 x 5 (3 + 2) two supply-chain reasons from four.',
  'The hidden economy is National Income (3-0); supply-chain disruption to trade is International Trade & Competitiveness (4-2).')
q(9, [12], [12], [T('a', 10, 'sa-q9-a', '2-2'), T('b', 5, 'sa-q9-b', '2-2')],
  'a 5 + 5 private cost and private benefit, one card. b 5 social benefits.',
  'Private and social costs and benefits are Market Failure (2-2).')
q(10, [13], [13], [T('a', 6, 'seca-q10-a', '0-1'), T('b', 9, 'sa-q10-b', '0-1')],
  'a 6 opportunity cost D to H = 62 million litres of Tropicana. b 9 objective NO, X lies inside the frontier. The schedule and the PPF chart are one data crop.',
  'Opportunity cost and the production possibility frontier are Scarcity & Choice (0-1).')
q(11, [14, 15, 16, 17], [14, 15, 16],
  [T('a/i', 12, 'q11-a-i', '1-1'), T('a/ii', 12, 'q11-a-ii', '3-5'), T('b/i', 11, 'q11-b-i', '1-0'),
   T('b/ii', 10, 'q11-b-ii', '1-2'), T('b/iii', 5, 'q11-b-iii', '1-1'), T('c/i', 8, 'q11-c-i', '0-1'),
   T('c/ii', 5, 'q11-c-ii', '0-1'), T('c/iii', 12, 'q11-c-iii-for', '1-3')],
  'Eight tasks totalling 75. a(i) and a(ii) 1 x 8, 1 x 4. b(i) diagram 6 + explanation 5 (hidden solution); b(ii) 2 x 5; b(iii) 5. c(i) 8; c(ii) 5 (the example must be capital spending); c(iii) 2 x 6 (3 + 3), one argument for AND one against, one card (the old against card resolves by alias).',
  'Rent demand is The Consumer (1-1); balanced regional development Economic Growth (3-5); the land market The Market Economy (1-0) with the characteristics of land The Firm (Supply) (1-2) and derived demand The Consumer (1-1); opportunity cost Scarcity & Choice (0-1); support for regional airports Government Intervention (1-3).')
q(12, [18, 19, 20, 21], [17, 18, 19, 20, 21, 22],
  [T('a/i', 9, 'q12-a-i', '2-0'), T('a/ii', 6, 'q12-a-ii', '2-0'), T('a/iii', 4, 'q12-a-iii', '1-3'),
   T('a/iv', 5, 'q12-a-iv', '1-3'), T('b/i/monopoly', 5, 'q12-b-i-monopoly', '2-0'),
   T('b/i/oligopoly', 5, 'q12-b-i-oligopoly', '2-0'), T('b/ii', 19, 'q12-b-ii', '2-0'),
   T('b/iii', 6, 'q12-b-iii', '2-0'), T('c/i', 8, 'q12-c-i', '0-2'),
   T('c/ii/for', 4, 'q12-c-ii-for', '1-3'), T('c/ii/against', 4, 'q12-c-ii-against', '1-3')],
  'Eleven tasks totalling 75. a(i) 3 x 3 (three bullets, one each); a(ii) 2 x 3; a(iii) 4; a(iv) 5 (2 + 3). b(i) one advantage of each structure, separate 5 (2 + 3) cells, so two cards; b(ii) 11 labels + 8 (hidden solution); b(iii) 2 x 3. c(i) 2 x 4 (2 + 2); c(ii) one reason for and one against, separate 4 (2 + 2) cells, two cards.',
  'Concentration, deregulation and the market structures are Market Structures (2-0); privatisation and planning decisions are Government Intervention (1-3); a carbon-neutral motor industry is Sustainability (0-2).')
q(13, [22, 23, 24, 25], [23, 24, 25, 26],
  [T('a/i', 9, 'q13-a-i', '3-1'), T('a/ii', 16, 'q13-a-ii', '3-1'), T('b/i/incentive', 7, 'q13-b-i-incentive', '1-3'),
   T('b/i/tax', 7, 'q13-b-i-tax', '1-3'), T('b/ii', 12, 'q13-b-ii', '1-3'), T('c/i', 16, 'q13-c-i', '3-1'),
   T('c/ii/yes', 8, 'q13-c-ii-yes', '3-1'), T('c/ii/no', 8, 'q13-c-ii-no', '3-1')],
  'Eight routes; 75 with one route for c(ii). a(i) explanation 5 + example 4; a(ii) (6 + 2) + (6 + 2). b(i) one incentive AND one tax measure, separate 7 (4 + 3) cells, two cards; b(ii) 2 x 6 (3 + 3). c(i) 2 x 8 (4 + 4); c(ii) printed Yes/No, the scheme writes both sides: two routes at 8 (4 + 4).',
  'Government spending and taxation are Fiscal Policy & the Budget (3-1); incentives, taxes and interventions on behaviour are Government Intervention (1-3).')
q(14, [26, 27, 28, 29], [27, 28, 29, 30],
  [T('a/i', 6, 'q14-a-i', '3-3'), T('a/ii', 18, 'q14-a-ii-ticks', '1-5'), T('b/i', 9, 'q14-b-i', '1-5'),
   T('b/ii', 16, 'q14-b-ii', '1-5'), T('b/iii', 5, 'q14-b-iii', '1-5'), T('c/i', 8, 'q14-c-i', '2-1'),
   T('c/ii', 5, 'q14-c-ii', '2-1'), T('c/iii', 8, 'q14-c-iii', '2-1')],
  'Eight tasks totalling 75. a(i) 6 (3 + 3); a(ii) (2 + 4) x 3 objective classifications (hidden completed table, whole printed question shown). b(i) 9 €360,000, €200,000, €50,000 (the scheme labels B average variable cost; the paper says average total cost) and b(ii) TC 5, VC 5, FC 2, axes 4 (hidden solutions, the table shown as the whole printed (b)); b(iii) 5 four houses. c(i) 8 average 13.5; c(ii) 5 (2 + 3); c(iii) one argument for 4 (2 + 2) AND one against 4 (2 + 2), one card.',
  'Cost-push inflation is Monetary Policy & Inflation (3-3); costs, revenue and profit-maximising output are Costs of Production, Revenue & Profit (1-5); the gender pay gap and the living wage are The Labour Market (2-1).')
q(15, [30, 31, 32, 33, 34], [31, 32, 33, 34, 35, 36],
  [T('a/i', 8, 'q15-a-i', '1-2'), T('a/ii', 8, 'q15-a-ii', '1-3'), T('a/iii', 14, 'q15-a-iii', '1-0'),
   T('b/i', 8, 'q15-b-i', '4-2'), T('b/ii', 14, 'q15-b-ii', '4-2'), T('b/iii', 6, 'q15-b-iii', '1-4'),
   T('c/i', 7, 'q15-c-i', '4-2'), T('c/ii', 10, 'q15-c-ii', '4-1')],
  'Eight tasks totalling 75. a(i) 2 x 4 (2 + 2) two trends; a(ii) 2 x 4 subsidy AND quota; a(iii) diagram 9 + explanation 5 (hidden solution, whole printed question shown). b(i) 4 + 4 one period, three scheme examples (the scheme writes pence for pounds); b(ii) 2 x 7 (4 + 3); b(iii) 6. c(i) 4 + 3 Germany and Poland, unpriced pair; c(ii) 2 x 5 (2 + 3).',
  'Milk supply is The Firm (Supply) (1-2); subsidies and quotas Government Intervention (1-3); grant aid and the milk market The Market Economy (1-0); exchange rates, Brexit and the EU budget International Trade & Competitiveness (4-2); PED Elasticity (1-4); staying in the EU Globalisation (4-1).')
q(16, [35, 36, 37, 38], [37, 38, 39, 40, 41],
  [T('a/i', 12, 'q16-a-i', '0-2'), T('a/ii', 12, 'q16-a-ii', '1-3'), T('b/i', 7, 'q16-b-i', '0-2'),
   T('b/ii/government', 7, 'q16-b-ii', '0-2'), T('b/ii/citizens', 7, 'q16-b-ii-citizens', '0-2'),
   T('c/i', 15, 'q16-c-i', '1-3'), T('c/ii', 10, 'q16-c-ii', '0-2'), T('c/iii', 5, 'q16-c-iii', '0-2')],
  'Eight tasks totalling 75. a(i) and a(ii) 1 x 8, 1 x 4. b(i) 7 (4 + 3); b(ii) one strategy for the government AND one for citizens, separate 1 x 7 (4 + 3) cells, two cards. c(i) diagram 10 + explanation 5 (hidden solution); c(ii) 2 x 5 (2 + 3); c(iii) 5 (2 + 3).',
  'Social and environmental sustainability and fast fashion are Sustainability (0-2); housing interventions and minimum pricing are Government Intervention (1-3).')

SEL = {
 'Answer 3 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 3 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer either (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'Answer (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (b)/(c) alternatives.'),
}
PAGE_SEL = {
 (4, 'expansionary or contractionary effect. Refer to relevant figures in the diagram above to'): ('answer-classification', 'Q2(a) the figures decide the answer (expansionary); one card.'),
 (4, 'explain your answer. Indicate by means of a tick ( ) whether it is expansionary or'): ('answer-classification', 'Q2(a) tail of the tick instruction; expansionary only.'),
 (5, '(a) Do you agree with this new MUP for alcohol?'): ('finite-route', 'Q3(a) Agree/Disagree; the scheme lists both sides, two routes at 9.'),
 (5, 'Agree: Disagree:'): ('finite-route', 'Q3(a) printed stance boxes.'),
 (6, '(a) Categorise each of the following as either an injection, or a leakage from the circular flow of'): ('answer-classification', 'Q4(a) each item has one correct box (injection, injection, leakage); one card.'),
 (6, '(b) In the box below justify each of your choices in part (a) above.'): ('answer-classification', 'Q4(b) justify all three classifications; not a choice.'),
 (10, '(ii) Justify your choice in (i) above.'): ('answer-classification', 'Q7(a)(ii) justify the objective Figure B.'),
 (10, '2020. Choose by means of a tick ( ) one of the boxes below.'): ('answer-classification', 'Q7(a)(i) the scheme ticks Figure B only; one card.'),
 (10, 'Only one of the charts below accurately displays the trend in the European Central Bank (ECB)'): ('answer-classification', 'Q7 stem: one chart is correct (Figure B).'),
 (13, 'Cork based firm PepsiCo have 23 brands in total. Doritos and Tropicana are two of their most'): ('not-a-task-selection', 'Stem wording ("two of their most popular products"), not a selection.'),
 (17, 'Discuss the arguments for and against this statement.'): ('required-headings', 'Q11(c)(iii) both sides required, 2 x 6; one card.'),
 (19, '(iv) A government could choose privatisation of a semi-state body over deregulation.'): ('not-a-task-selection', 'Q12(a)(iv) the government’s choice in the scenario; the candidate explains privatisation, not a route.'),
 (19, 'Outline one reason why a government may choose to privatise a semi-state body'): ('not-a-task-selection', 'Q12(a)(iv) "one reason" is an open response.'),
 (24, 'that have an annual revenue of €750 million or more will be charged corporation tax at the'): ('not-a-task-selection', 'Stem threshold wording ("or more"), not a selection.'),
 (25, 'Yes: No:'): ('finite-route', 'Q13(c)(ii) Yes/No; the scheme lists both sides, two routes at 8.'),
 (26, '(ii) Choose by means of a tick () which type of cost best describes each of the following.'): ('answer-classification', 'Q14(a)(ii) each expense has one correct box (variable, variable, fixed); one card.'),
 (26, 'Explain your choice.'): ('answer-classification', 'Q14(a)(ii) tail of the tick instruction.'),
 (31, '(iii) Grant aid of €395m was provided to Irish farmers to improve and/or build a specific'): ('not-a-task-selection', 'Stem wording ("and/or"), not a selection.'),
 (31, 'range of farm buildings or purchase equipment that may benefit their farm business'): ('not-a-task-selection', 'Stem wording ("or"), not a selection.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 40: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

# The route tuples must equal the earlier review's, which the Irish review mirrors.
tup = lambda qs: sorted((x['n'], t['key'], t['cardId'], t['marks'], t['topicId']) for x in qs for t in x['tasks'])
if tup(Q) != tup(old['questions']):
    raise SystemExit(f'route tuples differ: +{set(tup(Q)) - set(tup(old["questions"]))} -{set(tup(old["questions"])) - set(tup(Q))}')
for x, o in zip(Q, old['questions']):
    assert x['paperPages'] == o['paperPages'], x['n']
    assert x['schemePages'] == o['schemePages'], x['n']
    assert sorted(x['canonicalNodeIds']) == sorted(o['canonicalNodeIds']), (x['n'], x['canonicalNodeIds'], o['canonicalNodeIds'])
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2022, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-12',
 'visuallyInspectedPaperPages': list(range(1, 41)), 'visuallyInspectedSchemePages': list(range(1, 49)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Re-review 2026-10-12 from a fresh paired visual sweep of all 40 paper and 48 scheme pages (scheme PDF page = printed page + 1; PDF pages 42-45 are the student research project rubric and 46-48 blank and back cover). {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), {len(sels)} raw directive lines classified; the route set equals the earlier review and the Irish review that mirrors it. Every stem and ask is now sliced from the paper and every menu from the scheme (econ_2022_hl.py; the Section A script is retired, and the twelve card-corrections that patched topics, wording and rows are folded into the authoring). Two consolidations stay with progress aliases (Q6 per-diagram cards, Q11(c)(iii) against). Choose-N rule checked: no printed choose-N-of-M item pool on this paper.',
 'externalClarifications': old.get('externalClarifications', []),
 'curriculumSource': old.get('curriculumSource', 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf'),
}
for k in ('targetedIrishEvidence',):
    if k in old: draft[k] = old[k]
out = W / 'scripts/markbank/authoring/drafts/economics-2022-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']), x['canonicalNodeIds'])
