"""Write the independent 2025 HL EV census draft from the full visual sweep."""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2025/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2025/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2025-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(t['topicId'] for t in tasks))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})
q(1, [3], [5], [T('a', 12, 'sa-q1-a-for', '3-5'), T('b', 6, 'sa-q1-b', '0-1')],
  'a required headings Argument for 6 + Argument against 6 in one response (the old against-only card resolves by alias). b 6 one definition. The scheme prints 6 for each heading, so Q1 totals 18 against 12 for most Section A questions; recorded as printed.',
  'Benefits and costs of hosting a major event to the host economy are growth outcomes (NCCA 4.6 economic growth). Cost benefit analysis weighs opportunity cost (NCCA 1.2).')
q(2, [4], [6, 7, 8], [T('a', 6, 'seca-q2-a', '3-0'), T('b', 6, 'sa-q2-b', '3-0'),
                      T('c/agree', 6, 'sa-q2-c-agree', '3-0'), T('c/disagree', 6, 'sa-q2-c-disagree', '3-0')],
  'a 6 savings rate 15% (fraction working, hidden solution crop). Answer either b 2@3 OR c: c printed Agree/Disagree tick with both lists in the scheme, two routes 6 each.',
  'Household savings, the savings ratio and its macro effects are national income/circular flow (NCCA 4.1).')
q(3, [5], [9, 10, 11], [T('a', 6, 'sa-q3-a', '4-2'), T('b', 6, 'sa-q3-b', '4-2'), T('c', 6, 'sa-q3-c', '4-2')],
  'a 6 one reason from seven. Answer either b 6 (one alternative measure to tariffs) OR c 6 (one reason protectionism is rising): both carded.',
  'Import patterns, protectionist measures and their causes are international trade (NCCA 5.3).')
q(4, [6, 7], [12, 13, 14, 15], [T('a', 6, 'sa-q4-a-good', '3-3'), T('b', 12, 'sa-q4-b-gov', '3-1'), T('c', 6, 'sa-q4-c', '3-3')],
  'a one 6 cell for the trend comment AND whether it is beneficial; the scheme lists beneficial and not-beneficial examples under one cell, the paper prints no tick, so one card (the old not-beneficial card resolves by alias). Answer either b required headings government 6 + consumers 6 (one card; the old consumers card resolves by alias) OR c 6: objective tick, the scheme answer is cost-push only, one card. Q4 via (b) totals 18; recorded as printed.',
  'Disinflation and cost-push inflation are NCCA 4.4 (price level). Government cost-of-living measures are fiscal policy (NCCA 4.2).')
q(5, [7], [16], [T('a', 6, 'sa-q5-a', '0-0'), T('b', 6, 'seca-q5-b', '0-0')],
  'a 2@3 positive and normative explanations, both required. b 2@3 two objective classifications (1 normative, 2 positive).',
  'Positive and normative economics is economics as a way of thinking (NCCA 1.1).')
q(6, [8], [17], [T('a', 6, 'sa-q6-a', '1-3'), T('b', 6, 'seca-q6-b', '2-1')],
  'a 6 price floor definition. b one 6 cell for the completed labour-market diagram and its explanation together; the diagram solution is hidden until reveal and the full printed question is shown.',
  'A price floor is government intervention (NCCA 2.4). A minimum wage above equilibrium is the labour market (NCCA 3.2).')
q(7, [9], [18], [T('a', 6, 'seca-q7-a', '1-4'), T('b', 6, 'sa-q7-b', '2-2')],
  'a one 6 cell for necessity (electricity, noodles accepted) and luxury (premium clothing) with justifications, no published split. b 6 merit good explanation.',
  'YED classification is elasticity (NCCA 2.2, deck 2.5). Merit goods are market failure (NCCA 3.3).')
q(8, [10], [19, 20], [T('a', 6, 'sa-q8-a', '0-2'), T('b', 6, 'sa-q8-b', '2-2')],
  'a one 6 cell for the concept and one recent initiative together. b 2@3 two ways greenwashing causes market failure.',
  'Environmental sustainability is NCCA 1.3. Greenwashing as information failure is market failure (NCCA 3.3).')
q(9, [11], [21], [T('a', 6, 'q9-a', '2-0'), T('b', 6, 'sa-q9-b', '2-0')],
  'a one 6 cell for three labels (MC, AR = Demand, MR), no per-label split. b one 6 cell explaining the kinked curve above and below the kink.',
  'The kinked demand curve of oligopoly is market structures (NCCA 3.1).')
q(10, [12], [22, 23], [T('a', 6, 'seca-q10-a', '3-5'), T('b', 6, 'sa-q10-b', '3-5')],
  'a 2@3 boom A and recession B each with a justification (objective identifications). b 6 one factor 2008-2011.',
  'The business cycle and the 2008-2011 downturn are economic growth (NCCA 4.6).')
q(11, [13, 14, 15, 16], [24, 25, 26, 27, 28, 29, 30],
  [T('a/i', 8, 'q11-a-i', '2-0'), T('a/ii', 14, 'q11-a-ii', '2-0'),
   T('b/i/diagram', 12, 'q11-b-i', '2-0'), T('b/i/explanation', 9, 'q11-b-i-explanation', '2-0'),
   T('b/ii', 4, 'q11-b-ii', '2-0'), T('b/iii', 8, 'q11-b-iii-adv', '2-0'),
   T('c/i', 8, 'q11-c-i', '2-1'), T('c/ii', 4, 'q11-c-ii', '2-1'), T('c/iii', 8, 'q11-c-iii', '1-0')],
  'Nine tasks totalling 75. a(i) one 8 cell: tick highly concentrated, HHI 3,594, justify (>2,500). a(ii) 2@7. b(i) diagram 12 and explanation 9 separately priced, split (the old combined card keeps its ID as the diagram). b(ii) 4. b(iii) required advantage 4 + disadvantage 4 (old disadvantage card resolves by alias). c(i) 2@4; c(ii) 4; c(iii) one 8 cell for meaning and example.',
  'HHI, entry, patent monopoly, barriers and monopoly power are market structures (NCCA 3.1). GP shortages are a labour-market supply question (NCCA 3.2). A mixed economy is the market economy and the role of government (NCCA 2.1).')
q(12, [17, 18, 19, 20], [31, 32, 33, 34, 35, 36, 37, 38],
  [T('a/i/gni', 6, 'q12-a-i', '3-1'), T('a/i/gdp', 6, 'q12-a-i-gdp', '3-1'),
   T('a/ii', 14, 'q12-a-ii-tax', '3-1'), T('a/iii', 6, 'q12-a-iii', '3-0'),
   T('b/i', 12, 'q12-b-i', '3-1'), T('b/ii', 8, 'q12-b-ii', '3-1'),
   T('b/iii/agree', 8, 'q12-b-iii-agree', '3-1'), T('b/iii/disagree', 8, 'q12-b-iii-disagree', '3-1'),
   T('c/i', 14, 'q12-c-i-employee', '2-1'), T('c/ii', 7, 'q12-c-ii', '3-0')],
  'Ten routes; 75 with one route per choice. a(i) printed GNI*/GDP tick, the scheme writes both trends: two routes 6 each (the GDP route is new). a(ii) required taxpayers 7 + government 7 (old government card resolves by alias). a(iii) objective tick GNI* + justify 6. b(i) most significant change 6 + reason 6. b(ii) objective tick regressive + justify 8. b(iii) Agree 8 OR Disagree 8. c(i) required employee advantage 7 + employer disadvantage 7 (old employer card resolves by alias). c(ii) 7.',
  'Government debt, the tax mix, VAT and income tax rates are fiscal policy (NCCA 4.2). GNI* against GDP and the multiplier are national income (NCCA 4.1). Auto-enrolment pensions for employees and employers are the labour market (NCCA 3.2).')
q(13, [21, 22, 23, 24], [39, 40, 41, 42, 43, 44, 45, 46],
  [T('a/i', 8, 'q13-a-i', '4-2'), T('a/ii', 14, 'q13-a-ii-benefit', '4-2'), T('a/iii', 7, 'q13-a-iii', '4-1'),
   T('b/i', 7, 'q13-b-i', '4-2'), T('b/ii', 12, 'q13-b-ii', '4-2'), T('b/iii', 6, 'q13-b-iii', '4-2'),
   T('c/i', 7, 'q13-c-i', '4-0'), T('c/ii', 7, 'q13-c-ii', '4-0'), T('c/iii', 7, 'q13-c-iii', '4-0')],
  'Nine tasks totalling 75. a(i) 8 = 31.48% / 32% (fraction working, hidden solution crop). a(ii) required benefit 7 + challenge 7 (old challenge card resolves by alias). a(iii) 7. b(i) 7; b(ii) 2@6; b(iii) 6. c(i)-(iii) 7 each.',
  'Exports, comparative advantage and the WTO are international trade (NCCA 5.3). Outward FDI is globalisation (NCCA 5.2). Overseas development assistance and aid dependence are growth and development (NCCA 5.1).')
q(14, [25, 26, 27, 28], [47, 48, 49, 50, 51, 52, 53, 54, 55],
  [T('a/i', 10, 'q14-a-i', '1-1'), T('a/ii', 10, 'q14-a-ii', '2-0'),
   T('a/iii/agriculture', 5, 'q14-a-iii-agri', '1-2'), T('a/iii/sport', 5, 'q14-a-iii-sport', '1-2'),
   T('b/i', 17, 'q14-b-i', '1-0'), T('b/ii/calculation', 9, 'q14-b-ii', '1-4'), T('b/ii/meaning', 5, 'q14-b-ii-meaning', '1-4'),
   T('c/i/agree', 7, 'q15-a-i-agree', '2-1'), T('c/i/disagree', 7, 'q15-a-i-disagree', '2-1'),
   T('c/ii', 12, 'q14-c-ii-positive', '3-2')],
  'Ten routes; 75 with one route per choice. a(i) 2@5; a(ii) 2@5. a(iii) printed sector tick, the scheme lists both sectors: two routes 5 each. b(i) 17 x 1 with the margin split axes 2, D 6, S 6, E, Pe, Qe 1 each. b(ii) workings 9 (-1.8) and economic meaning 5 separately priced, split (the calculation card is new). c(i) Agree 7 OR Disagree 7 (IDs carry a q15 prefix from the earlier extractor; citation is Q14(c)(i)). c(ii) required positive 6 + negative 6 (the negative half was missing).',
  'Online shopping benefits are the consumer (NCCA 2.2). Amazon and small retailers is market structure (NCCA 3.1). Technology in a sector is the firm (NCCA 2.3). Demand and supply equilibrium is the market (NCCA 2.1); PED is elasticity (NCCA 2.2). Gig-economy regulation is the labour market (NCCA 3.2). Full employment is employment and unemployment (NCCA 4.3).')
q(15, [29, 30, 31, 32], [56, 57, 58, 59, 60, 61, 62, 63, 64],
  [T('a/i/agree', 6, 'q15-a-i-cash-agree', '3-4'), T('a/i/disagree', 6, 'q15-a-i-cash-disagree', '3-4'),
   T('a/ii', 12, 'q15-a-ii', '3-4'), T('a/iii', 6, 'q15-a-iii-aib', '3-4'),
   T('b/i', 8, 'q15-b-i', '3-3'), T('b/ii', 12, 'q15-b-ii', '2-1'),
   T('b/iii/agree', 5, 'q15-b-iii-agree', '1-3'), T('b/iii/disagree', 5, 'q15-b-iii-disagree', '1-3'),
   T('c/i', 6, 'q15-c-i', '3-1'), T('c/ii', 10, 'q15-c-ii', '3-1'), T('c/iii', 10, 'q15-c-iii', '3-1')],
  'Eleven routes; 75 with one route per choice. a(i) Agree 6 OR Disagree 6. a(ii) 2@6; a(iii) 6. b(i) 8 = 36.48% (fraction working, hidden solution crop; the chart plots annual growth rates). b(ii) 2@6. b(iii) Agree 5 OR Disagree 5. c(i) one 6 cell for meaning and example. c(ii) 2@5; c(iii) 2@5 reasons other than infrastructure.',
  'Access to cash, credit creation and bank branches are the financial sector (NCCA 4.5). The RPPI growth rate is the price level (NCCA 4.4). Property prices and labour are the labour market (NCCA 3.2). Mortgage interest relief is government intervention (NCCA 2.4). Infrastructure and government expenditure are fiscal policy (NCCA 4.2).')
q(16, [33, 34, 35, 36], [65, 66, 67, 68, 69, 70, 71],
  [T('a/i', 6, 'q16-a-i', '1-5'), T('a/ii', 5, 'q16-a-ii', '1-5'), T('a/iii', 14, 'q16-a-iii', '1-5'),
   T('b/i', 9, 'q16-b-i-diseconomies', '1-5'), T('b/ii/diagram', 8, 'q16-b-ii', '1-5'),
   T('b/ii/explanation', 8, 'q16-b-ii-explanation', '1-5'),
   T('c/i', 12, 'q16-b-i', '1-3'), T('c/ii', 5, 'q16-c-ii', '1-5'), T('c/iii', 8, 'q16-c', '0-0')],
  'Nine tasks totalling 75. a(i) one 6 cell for A = 10 and B = 1.92. a(ii) 5 = 70. a(iii) 2@7. b(i) one 9 cell for meaning and example (new card). b(ii) diagram 8 (SRAC x3, labels x3, LRAC x1, label x1) and explanation 8 separately priced, split (the old combined card keeps its ID as the diagram). c(i) 2@6 (ID carries a q16-b-i suffix from the earlier extractor; citation is Q16(c)(i)). c(ii) 5 short-run loss (new card). c(iii) 2@4.',
  'Costs, revenue, profit, firm objectives, diseconomies of scale, the LRAC and the short-run shutdown rule are NCCA 2.3 (deck 2.6). Supports for hospitality firms are government intervention (NCCA 2.4). Entrepreneurship as a factor of production is economics as a way of thinking (NCCA 1.1).')

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
}
PAGE_SEL = {
 (4, 'Do you agree or disagree with this statement?'): ('finite-route', 'Q2(c) agree/disagree routes.'),
 (7, '(b) Determine whether each of the economic statements below is a positive statement or a'): ('answer-classification', 'Q5(b) each statement has one correct box; one card with both classifications.'),
 (7, 'normative statement. Indicate your choice below by ticking () the relevant box.'): ('answer-classification', 'Q5(b) tick boxes with one correct answer each.'),
 (7, 'Do you regard the above situation to be an example of demand-pull inflation or cost-push'): ('answer-classification', 'Q4(c) the scheme answer is cost-push only; one card.'),
 (7, 'inflation? Indicate your choice below by ticking () the relevant box and justify your choice.'): ('answer-classification', 'Q4(c) tick box with one correct answer.'),
 (8, 'Clearly label any changes you make. Explain your answer.'): ('not-a-task-selection', 'Drawing instruction ("any changes"), not a selection.'),
 (10, '(Greenwashing is a marketing measure / practice where some companies make false or'): ('not-a-task-selection', 'Stem definition ("or"), not a selection.'),
 (12, '(a) Identify from the diagram above which option (A or B) represents:'): ('answer-classification', 'Q10(a) boom A and recession B are fixed answers; one card.'),
 (12, 'Indicate your choice below by inserting A or B in the appropriate box and justify your choice'): ('answer-classification', 'Q10(a) answer boxes with fixed answers.'),
 (13, 'determine whether the market is competitive or highly concentrated. Indicate your'): ('answer-classification', 'Q11(a)(i) the HHI decides the box (highly concentrated); one card.'),
 (17, 'Government debt as a % of GNI* or Government debt as a % of GDP'): ('finite-route', 'Q12(a)(i) GNI* or GDP trend tick; the scheme writes both trends, two routes.'),
 (18, 'Indicate your choice below by ticking () the relevant box and justify your choice.'): ('answer-classification', 'Q12(a)(iii) tick box; the scheme answer is GNI* only.'),
 (18, 'debt as a percentage of GNI* or debt as a percentage of GDP?'): ('answer-classification', 'Q12(a)(iii) the scheme ticks GNI* only; one card.'),
 (19, '(ii) Do you regard Ireland’s value added tax system to be a progressive tax or a'): ('answer-classification', 'Q12(b)(ii) the scheme ticks regressive only; one card.'),
 (19, 'Do you agree or disagree with the statement, that individuals who earn above'): ('finite-route', 'Q12(b)(iii) agree/disagree routes.'),
 (19, 'Indicate your choice below by ticking () the relevant box and justify your choice.'): ('finite-route', 'Q12(b)(iii) stance tick boxes.'),
 (19, 'your choice.'): ('answer-classification', 'Q12(b)(ii) tail of the regressive/progressive tick instruction.'),
 (25, 'able to choose from a wider selection of products.'): ('not-a-task-selection', 'Exclusion ("other than being able to choose from a wider selection"), not a selection.'),
 (26, 'economy. Outline one other way that changes in technology may affect how either of'): ('finite-route', 'Q14(a)(iii) either Agriculture or Sports and fitness; the scheme lists both sectors, two routes.'),
 (27, '(Note: the gig economy is a labour market where short-term contracts or freelance'): ('not-a-task-selection', 'Stem definition ("or"), not a selection.'),
 (27, 'Do you agree or disagree with the statement above?'): ('finite-route', 'Q14(c)(i) agree/disagree routes.'),
 (27, 'Indicate your choice below by ticking () the relevant box and justify your choice.'): ('finite-route', 'Q14(c)(i) stance tick boxes.'),
 (29, '(a) (i) Do you agree or disagree with The Finance (Provision of Access to Cash Infrastructure)'): ('finite-route', 'Q15(a)(i) agree/disagree routes.'),
 (29, 'Indicate your choice below by ticking () the relevant box and justify your choice.'): ('finite-route', 'Q15(a)(i) stance tick boxes.'),
 (31, 'Do you agree or disagree with this government decision?'): ('finite-route', 'Q15(b)(iii) agree/disagree routes.'),
 (31, 'Indicate your choice below by ticking () the relevant box and justify your choice.'): ('finite-route', 'Q15(b)(iii) stance tick boxes.'),
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
 'subjectId': 'economics', 'year': 2025, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-11',
 'visuallyInspectedPaperPages': list(range(1, 41)), 'visuallyInspectedSchemePages': list(range(1, 78)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Census from the paired visual sweep of all 40 paper and 77 scheme pages, checked against the 83 cards the earlier extractors shipped. {len(tasks)} routes ({sum(1 for t in tasks if "-sa-" in t["cardId"] or "-seca-" in t["cardId"] or t["cardId"].endswith("q9-a"))} Section A + rest Section B), {len(sels)} raw directive lines classified. Seven split required-heading cards consolidate with progress aliases; six missing tasks are added (Q11(b)(i) explanation, Q12(a)(i) GDP route, Q14(b)(ii) calculation, Q16(b)(i), Q16(b)(ii) explanation, Q16(c)(ii)). Scheme PDF pp72-77 student research project descriptors and back cover: no written-paper asks. Scheme header says Section A 75 marks against the paper\'s 100; Q1 and Q4(b) carry 6 per required heading (18 in total), recorded as printed.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2025-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']))
