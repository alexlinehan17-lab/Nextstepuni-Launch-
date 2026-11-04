"""Write the independent 2026 HL EV census draft (before authoring)."""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2026/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2026/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2026-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(t['topicId'] for t in tasks))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes,
              'topicReason': topic_reason})
q(1, [3], [5, 6], [T('a', 6, 'sa-q1-a', '0-1'), T('b', 6, 'sa-q1-b', '4-2')],
  'a 2@3 two benefits of specialisation from seven open examples. b one 6 cell: one 1950s characteristic compared with one present-day characteristic; six headed pairs are open examples, both periods required, no published split between the periods.',
  'NCCA 1.2 names the principle of specialisation and how firms use it to increase efficiency, so Q1(a) is Scarcity & Choice. Comparing Irish trade then and now is NCCA 5.3 patterns in Irish trade over time.')
q(2, [4], [7, 8], [T('a/events', 6, 'sa-q2-a-events', '1-4'), T('a/streaming', 6, 'sa-q2-a-streaming', '1-4'),
                   T('b', 6, 'sa-q2-b', '1-5'), T('c', 6, 'sa-q2-c', '1-5')],
  'a 6: printed two-box choice; scheme ticks music events and separately credits a streaming answer, so both stances are routes (6 each, counted once). Answer either b 2@3 OR c 6: both alternatives carded.',
  'PED comparison is NCCA 2.2 elasticity (deck 2.5). Objectives other than profit maximisation and near-zero marginal cost are firm cost/revenue topics (NCCA 2.3, deck 2.6).')
q(3, [5, 6], [9, 10, 11, 12], [T('a/agree', 6, 'sa-q3-a-agree', '1-3'), T('a/disagree', 6, 'sa-q3-a-disagree', '1-3'),
                              T('b', 6, 'sa-q3-b', '2-2'), T('c', 6, 'sa-q3-c', '0-2')],
  'a single 6 cell with AGREE and DISAGREE lists: two stance routes, counted once. Answer either b 6 (one reason) OR c 2@3: both carded.',
  'A public-transport subsidy is government intervention (NCCA 2.4). Noise externality is market failure (NCCA 3.3). Reducing urban-rural inequality is social sustainability/inequality (NCCA 1.3).')
q(4, [6, 7], [13, 14, 15], [T('a', 6, 'sa-q4-a', '2-1'), T('b', 6, 'sa-q4-b', '1-3'), T('c', 6, 'sa-q4-c', '1-1')],
  'a 6 one reason from seven. Answer either b 2@3 OR c 2@3: both carded. Open example pools, no finite selection.',
  'Lower LDC wages are wage differentials (NCCA 3.2). Measures to raise demand are government intervention (NCCA 2.4). App benefits for consumers are consumer outcomes (NCCA 2.2).')
q(5, [8], [15, 16, 17], [T('a/rational', 6, 'sa-q5-a-rational', '1-1'), T('a/irrational', 6, 'sa-q5-a-irrational', '1-1'), T('b', 6, 'sa-q5-b', '1-1')],
  'a single 6 cell, scheme gives Rational and Irrational justification lists: two stance routes counted once. b 2@3 two other assumptions from three open headings.',
  'Rational behaviour and consumer assumptions are NCCA 2.2 (critique the rationality assumption).')
q(6, [9], [17, 18, 19], [T('a', 6, 'sa-q6-a', '4-1'), T('b', 6, 'sa-q6-b', '3-5')],
  'a two separately priced asks in one lettered part: explain globalisation 3 + one benefit to a company 3, kept as one card with fixed 3+3 rows. b 2@3 benefits of theme parks within a country.',
  'Globalisation and investing abroad is NCCA 5.2. Benefits of theme parks to a country (employment, invisible exports, multiplier, regional development) are growth outcomes (deck 4.6).')
q(7, [10], [20, 21, 22], [T('a/subsidy', 6, 'sa-q7-a-subsidy', '1-3'), T('a/tax', 6, 'sa-q7-a-tax', '1-3'),
                          T('b/yes', 6, 'sa-q7-b-yes', '0-2'), T('b/no', 6, 'sa-q7-b-no', '0-2')],
  'a printed subsidy/tax tick boxes, scheme justifies both: two routes 6 each (not caught by the directive scan; recorded here). b EKC Yes (relevant)/No (not relevant): two routes 6 each.',
  'Fiscal tools to change packaging behaviour are government intervention (NCCA 2.4). The EKC growth-environment relationship is sustainability (NCCA 1.3).')
q(8, [11], [23, 24], [T('a', 6, 'sa-q8-a', '2-1'), T('b', 6, 'sa-q8-b', '1-0')],
  'a 2@3 two discouraging factors from eleven open examples. b 2@3 two effects on other local businesses from six.',
  'Factors affecting entry to farming work are labour supply (NCCA 3.2). Input-cost effects passing through local markets are market economy effects (NCCA 2.1).')
q(9, [12], [25, 26], [T('a', 6, 'sa-q9-a', '3-5'), T('b', 6, 'sa-q9-b', '3-5')],
  'a one 6 cell for calculation and comment together (97.3%), no published split. b 2@3 two concerns from seven.',
  'Comparing GDP growth between regions and its concerns is economic growth (deck 4.6, NCCA 4.1 data patterns).')
q(10, [13], [26, 27, 28], [T('a', 6, 'sa-q10-a', '3-3'), T('b', 6, 'sa-q10-b', '3-3')],
  'a 2@3 effects of higher prices from thirteen. b 2@3 unequal effects of food price rises from eight.',
  'Consequences of a higher price level are NCCA 4.4 (consequences of changes in the price level).')
q(11, [14, 15, 16, 17], [29, 30, 31, 32, 33, 34, 35, 36],
  [T('a/i', 6, 'q11-a-i', '1-3'), T('a/ii', 12, 'q11-a-ii', '2-2'),
   T('b/i/diagram', 12, 'q11-b-i', '2-0'), T('b/i/explanation', 9, 'q11-b-i-explanation', '2-0'),
   T('b/ii', 8, 'q11-b-ii', '2-0'), T('c/i/calculation', 7, 'q11-c-i', '1-4'), T('c/i/meaning', 5, 'q11-c-i-meaning', '1-4'),
   T('c/ii/agree', 6, 'q11-c-ii-agree', '1-3'), T('c/ii/disagree', 6, 'q11-c-ii-disagree', '1-3'), T('c/iii', 10, 'q11-c-iii', '1-4')],
  'Ten tasks; 75 with one stance. a(i) 6 one measure; a(ii) 2@6. b(i) diagram 12 (eleven labels, no per-label tariff) and explanation 9 are separately priced, split as in 2024 Q14(b)(i). b(ii) required headings Choice of gyms 4 + Cost of membership 4. c(i) workings 7 (+1.8) and explanation 5 separately priced, split. c(ii) AGREE 6 OR DISAGREE 6 stance routes. c(iii) one 10 cell for PED meaning and measure, no published split.',
  'Measures to raise participation and society-wide benefits are intervention and positive externalities (NCCA 2.4, 3.3). Monopolistic competition and oligopoly comparisons are NCCA 3.1. YED and PED are NCCA 2.2 (deck 2.5). Tax relief to change a market outcome is NCCA 2.4.')
q(12, [18, 19, 20, 21], [37, 38, 39, 40, 41, 42, 43, 44, 45, 46],
  [T('a/i/imports', 4, 'q12-a-i-imports', '4-2'), T('a/i/exports', 4, 'q12-a-i-exports', '4-2'),
   T('a/ii/benefit', 8, 'q12-a-ii-benefit', '4-2'), T('a/ii/challenge', 8, 'q12-a-ii-challenge', '4-2'),
   T('a/iii', 6, 'q12-a-iii', '4-2'), T('b/i', 6, 'q12-b-i', '4-2'), T('b/ii', 12, 'q12-b-ii', '4-2'),
   T('b/iii', 12, 'q12-b-iii', '4-2'), T('c/i/calculation', 7, 'q12-c-i', '2-0'), T('c/i/influence', 4, 'q12-c-i-influence', '2-0'),
   T('c/ii/option-a', 6, 'q12-c-ii-option-a', '1-3'), T('c/ii/option-b', 6, 'q12-c-ii-option-b', '1-3'),
   T('c/iii', 10, 'q12-c-iii', '2-0')],
  'Thirteen routes; 75 with one route per choice. a(i) imports OR exports trend 4 each (both scheme trends printed). a(ii) benefit or challenge stance 8 each (one 8 cell, two lists). a(iii) dumping 6; b(i) tariff 6; b(ii) 2@6; b(iii) required benefit 6 + challenge 6. c(i) workings 7 (42.7%) and influence 4 separately priced, split. c(ii) Option A 6 OR Option B 6 (not caught by the directive scan; recorded here). c(iii) required employment 5 + prices 5.',
  'Trade values, dumping, tariffs and protectionism are NCCA 5.3. Top-three concentration and price influence are NCCA 3.1 (concentration of market power). Carbon tax versus subsidies are government intervention (NCCA 2.4). Ending ESB Networks monopoly is market structure/competition (NCCA 3.1).')
q(13, [22, 23, 24, 25], [47, 48, 49, 50, 51, 52, 53, 54, 55],
  [T('a/i', 6, 'q13-a-i', '3-3'), T('a/ii', 12, 'q13-a-ii', '3-4'), T('b/i', 12, 'q13-b-i', '1-5'),
   T('b/ii', 16, 'q13-b-ii', '1-5'), T('b/iii', 4, 'q13-b-iii', '1-5'), T('c/i', 10, 'q13-c-i', '0-1'),
   T('c/ii', 10, 'q13-c-ii', '2-1'), T('c/iii/agree', 5, 'q13-c-iii-agree', '1-3'), T('c/iii/disagree', 5, 'q13-c-iii-disagree', '1-3')],
  'Nine routes; 75 with one stance. a(i) 6; a(ii) 2@6. b(i) 2@6: fixed costs (meaning+example) 6 and variable costs (meaning+example) 6, both required; no published meaning/example split. b(ii) one 16 cell for the TFC/TVC/TC diagram. b(iii) 4 = EUR25. c(i) required benefit 5 + challenge 5. c(ii) 2@5. c(iii) Agree 5 OR Disagree 5.',
  'ECB rate decisions are NCCA 4.4; demand for credit is NCCA 4.5. Fixed/variable/total cost curves and price for target profit are NCCA 2.3 (deck 2.6). Benefit/challenge evaluation of town-centre revitalisation is a cost-benefit judgement (NCCA 1.2). EU free movement and construction labour supply is NCCA 3.2. Compulsory purchase is government intervention (NCCA 2.4).')
q(14, [26, 27, 28, 29], [56, 57, 58, 59, 60, 61, 62, 63, 64, 65],
  [T('a/i', 6, 'q14-a-i', '3-0'), T('a/ii', 10, 'q14-a-ii', '3-0'), T('a/iii', 10, 'q14-a-iii', '3-0'),
   T('b/i', 8, 'q14-b-i', '3-0'), T('b/ii', 12, 'q14-b-ii', '4-2'),
   T('b/iii/agree', 5, 'q14-b-iii-agree', '3-1'), T('b/iii/disagree', 5, 'q14-b-iii-disagree', '3-1'),
   T('c/i', 8, 'q14-c-i', '1-0'), T('c/ii', 8, 'q14-c-ii', '1-0'), T('c/iii', 8, 'q14-c-iii', '1-0')],
  'Ten routes; 75 with one stance. a(i) 6 NFIA = -46.4bn; a(ii) 2@5; a(iii) required economic 5 + social 5. b(i) one 8 cell for four circular-flow terms, no per-term split. b(ii) imports meaning 4 + 2@4 factors in one card. b(iii) Agree 5 OR Disagree 5. c(i)-(iii) one 8 cell each for diagram and explanation together, so each event is one complete card.',
  'NFIA, GDP limitations, hidden economy and circular flow are NCCA 4.1. Factors influencing imports are NCCA 5.3. Paying household arrears from public funds is fiscal (NCCA 4.2). Equilibrium changes from demand/supply shifts are NCCA 2.1.')
q(15, [30, 31, 32, 33], [66, 67, 68, 69, 70, 71, 72, 73, 74, 75],
  [T('a/i', 12, 'q15-a-i', '3-1'), T('a/ii', 6, 'q15-a-ii', '3-1'), T('a/iii', 6, 'q15-a-iii', '3-1'),
   T('b/i', 6, 'q15-b-i', '3-1'), T('b/ii', 12, 'q15-b-ii', '3-1'),
   T('b/iii/agree', 6, 'q15-b-iii-agree', '3-1'), T('b/iii/disagree', 6, 'q15-b-iii-disagree', '3-1'),
   T('c/i', 9, 'q15-c-i', '3-5'), T('c/ii', 12, 'q15-c-ii', '3-5'),
   T('c/iii/narrow', 6, 'q15-c-iii-narrow', '3-5'), T('c/iii/widen', 6, 'q15-c-iii-widen', '3-5')],
  'Eleven routes; 75 with one route per choice. a(i) 2@6 current (meaning+example) and capital (meaning+example), both required, no meaning/example split. a(ii) 6; a(iii) 6; b(i) 6; b(ii) 2@6; b(iii) Agree 6 OR Disagree 6. c(i) labour productivity 5 + foreign example 2 + domestic example 2. c(ii) required reason 6 + strategy 6. c(iii) narrow/widen routes 6 each.',
  'Current/capital spending, targeted supports, tax base and VAT are NCCA 4.2. Labour productivity and AI effects on productivity gaps are growth determinants (deck 4.6, NCCA 5.1).')
q(16, [34, 35, 36, 37], [76, 77, 78, 79, 80, 81, 82],
  [T('a/i', 4, 'q16-a-i', '1-0'), T('a/ii', 7, 'q16-a-ii', '1-0'), T('a/iii', 14, 'q16-a-iii', '3-1'),
   T('b/i', 5, 'q16-b-i', '4-2'), T('b/ii', 7, 'q16-b-ii', '4-2'), T('b/iii', 14, 'q16-b-iii', '3-5'),
   T('c/i', 6, 'q16-c-i', '0-1'), T('c/ii', 6, 'q16-c-ii', '0-1'), T('c/iii', 12, 'q16-c-iii', '4-0')],
  'Nine tasks totalling 75. a(i) diagram 4; a(ii) 7; a(iii) 2@7. b(i) 5 France share; b(ii) 7; b(iii) 2@7. c(i) 6; c(ii) 6 PPF inward shift with explanation; c(iii) required economic 6 + social 6.',
  'Hotel-room equilibrium with fixed short-run supply is NCCA 2.1. Tourist-tax revenue use is fiscal (NCCA 4.2). Visitor shares and exchange-rate effects are NCCA 5.3. Airports and balanced regional development are growth (deck 4.6). PPF is scarcity and choice (NCCA 1.2). Effects of aid cuts on an LDC are NCCA 5.1.')

SEL = {
 'Answer 4 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 4 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 8 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 8 out of 10 questions.': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Questions 2, 3 and 4 contain an internal choice.': ('finite-route', 'Q2, Q3 and Q4 each offer (b) OR (c); every alternative is its own carded task.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer either (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (b)/(c) alternatives.'),
 'Agree Disagree': ('finite-route', 'Printed two-box stance; the scheme lists both sides, so each stance is its own route at the full tariff.'),
 'Do you agree or disagree with this proposal?': ('finite-route', 'Printed agree/disagree stance; both sides are carded routes.'),
 'Yes (relevant) No (not relevant)': ('finite-route', 'Q7(b) printed Yes/No; scheme justifies both, two routes.'),
 'Choice of gyms:': ('required-headings', 'Q11(b)(ii) answer box heading; both printed headings are required in one response.'),
 ' Choice of gyms': ('required-headings', 'Q11(b)(ii) bullet heading; both printed headings are required in one response.'),
}
PAGE_SEL = {
 (4, 'demand? Indicate your choice below by ticking () the relevant box and justify your choice.'): ('finite-route', 'Q2(a) two boxes; the scheme ticks music events but separately credits a streaming answer, so both are routes.'),
 (5, '(b) Irish Rail has imposed €100 fines for passengers who play videos or music without'): ('not-a-task-selection', 'Stem wording ("or"), not a selection.'),
 (8, 'FIND THE ITEMS YOU SELECT KLARNA PAY IN 30 DAYS'): ('not-a-task-selection', 'Text inside the Klarna graphic.'),
 (8, 'LIKE, ADD THEM PAYMENT METHOD OR 3 INTEREST'): ('not-a-task-selection', 'Text inside the Klarna graphic.'),
 (8, 'online purchases in Ireland. These agreements allow consumers to either pay upfront or to spread'): ('not-a-task-selection', 'Stem description of BNPL, not a selection.'),
 (8, 'or irrational consumer behaviour?'): ('finite-route', 'Q5(a) rational/irrational stance; the scheme justifies both, two routes.'),
 (10, 'Ireland generates more plastic packaging waste per person than any other EU country.'): ('not-a-task-selection', 'Stem statistic ("any other"), not a selection.'),
 (11, '(a) Farming may be seen as an unattractive career choice for many younger people in Ireland'): ('not-a-task-selection', 'Stem wording ("choice"), not a selection.'),
 (17, 'Do you agree or disagree, that gym memberships should receive tax relief?'): ('finite-route', 'Q11(c)(ii) agree/disagree routes.'),
 (17, 'Indicate your opinion below by ticking () the relevant box and justify your choice.'): ('finite-route', 'Q11(c)(ii) stance tick boxes.'),
 (18, '(i) Outline the overall trend in the value of Ireland’s total goods imports or total goods'): ('finite-route', 'Q12(a)(i) imports OR exports trend; both printed in the scheme, two routes.'),
 (18, '(ii) In your opinion, do the changes, shown in the chart above, bring benefits or'): ('finite-route', 'Q12(a)(ii) benefit or challenge stance; scheme lists both, two routes.'),
 (25, 'Do you agree or disagree with local authorities being allowed to compulsorily buy derelict'): ('finite-route', 'Q13(c)(iii) agree/disagree routes.'),
 (28, 'Do you agree or disagree with this proposal?'): ('finite-route', 'Q14(b)(iii) agree/disagree routes.'),
 (31, 'Do you agree or disagree with this VAT reduction for some of the hospitality sector?'): ('finite-route', 'Q15(b)(iii) agree/disagree routes.'),
 (33, 'In your opinion, will AI narrow or widen the productivity gap between the domestic'): ('finite-route', 'Q15(c)(iii) narrow/widen routes; the scheme lists both.'),
 (33, 'Indicate your choice below by ticking () the relevant box and justify your choice.'): ('finite-route', 'Q15(c)(iii) stance tick boxes.'),
 (37, 'Clearly label any changes you make. Explain your answer.'): ('not-a-task-selection', 'Drawing instruction ("any changes"), not a selection.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 40: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2026, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-11',
 'visuallyInspectedPaperPages': list(range(1, 41)), 'visuallyInspectedSchemePages': list(range(1, 89)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Census drafted from the paired visual sweep before any 2026 card existed: all 40 paper and 88 scheme pages viewed. {len(tasks)} routes ({sum(1 for t in tasks if "-sa-" in t["cardId"])} Section A + {sum(1 for t in tasks if "-sa-" not in t["cardId"])} Section B), {len(sels)} raw directive lines classified. Scheme PDF pp83-86 research rubric/brief, p87 blank, p88 back cover: no written-paper asks.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2026-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    if int(x['n']) > 10:
        print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
