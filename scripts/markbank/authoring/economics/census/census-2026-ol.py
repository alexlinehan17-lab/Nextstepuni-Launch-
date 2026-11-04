"""Write the independent 2026 OL EV census draft (made before authoring)."""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2026/LC034GLP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2026/LC034GLP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2026-ol-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason):
    nodes = list(dict.fromkeys(t['topicId'] for t in tasks))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})
q(1, [3], [5], [T('i', 6, 'sa-q1-i', '0-0'), T('ii', 6, 'sa-q1-ii', '4-2')],
  'i 6: Statistics and Office (Central given), 1st 4 / 2nd 2. ii 6: one example of an export AND one reason, 1st 4 / 2nd 2 shared, not a fixed side split.',
  'The CSO is the source of official economic data (NCCA 1.1 data for decisions). Why Ireland exports is NCCA 5.3 trade.')
q(2, [4], [6, 7], [T('a/private', 12, 'sa-q2-a-private', '2-2'), T('a/social', 12, 'sa-q2-a-social', '2-2'),
                   T('b/government', 12, 'sa-q2-b-government', '1-3'), T('b/retailers', 12, 'sa-q2-b-retailers', '1-3')],
  'Answer (a) or (b). a: printed private/social tick, the scheme lists both at 12 (OR): two routes. b: printed Government/Car retailers tick, scheme lists both under one 12: two routes. Each alternative counted once.',
  'Private versus social benefits of electric cars are externalities (NCCA 3.3). Encouraging EV purchase by subsidies, taxes and incentives is intervention in a market (NCCA 2.4).')
q(3, [5], [7, 8], [T('a', 12, 'sa-q3-a', '0-2'), T('b', 12, 'sa-q3-b', '0-2')],
  'Answer (a) or (b): one advantage 12 OR one disadvantage 12 of charging for paper bags; both carded.',
  'Charging for bags to change consumption habits and its trade-offs is sustainability in business decisions (NCCA 1.3).')
q(4, [6], [9], [T('a', 12, 'sa-q4-a', '3-1'), T('b/advantage', 12, 'sa-q4-b-advantage', '3-1'), T('b/disadvantage', 12, 'sa-q4-b-disadvantage', '3-1')],
  'Answer (a) or (b). a 12: the scheme ticks Capital only, so the tick is an objective classification and one card. b: advantage OR disadvantage tick, scheme lists both: two routes at 12.',
  'Current versus capital government spending and the effects of a public capital project are NCCA 4.2.')
q(5, [7], [10], [T('advantage', 12, 'sa-q5-advantage', '4-0'), T('disadvantage', 12, 'sa-q5-disadvantage', '4-0')],
  'Advantage OR disadvantage tick; scheme lists both under one 12: two routes.',
  'Aid to developing countries is NCCA 5.1 (overseas development).')
q(6, [7], [11], [T('-', 12, 'sa-q6', '3-1')],
  'One advantage AND one disadvantage, 12 with 1st 8 / 2nd 4: one whole response, no fixed side split.',
  'A Budget fee reduction and its costs is fiscal policy (NCCA 4.2).')
q(7, [8], [12], [T('-', 12, 'sa-q7', '3-1')],
  'Match B, C, D (A given): 1st 8, 2nd 2, 3rd 2 = 12; one task.',
  'Canons of taxation are NCCA 4.2 taxation.')
q(8, [8], [13], [T('agree', 12, 'sa-q8-agree', '0-1'), T('disagree', 12, 'sa-q8-disagree', '0-1')],
  'Agree/Disagree tick; scheme lists Agree 12 OR Disagree 12: two routes.',
  'Whether the spending was waste is an opportunity-cost judgement on a government decision (NCCA 1.2).')
q(9, [9], [14], [T('-', 12, 'sa-q9', '3-2')],
  'Economic advantage AND disadvantage of rising employment, 12 with 1st 8 / 2nd 4: one whole response.',
  'Effects of rising employment are NCCA 4.3.')
q(10, [10], [15], [T('i', 6, 'sa-q10-i', '3-1'), T('ii', 6, 'sa-q10-ii', '3-1')],
  'i 6: highest (Social Protection) and one lowest (Transport/Justice), 1st 4 / 2nd 2. ii 6: one example for Social Protection AND Health, 1st 4 / 2nd 2. Separately priced, two tasks.',
  'Areas of government expenditure are NCCA 4.2.')
q(11, [11, 12, 13], [16, 17, 18, 19],
  [T('a/i', 9, 'q11-a-i', '2-0'), T('a/ii', 12, 'q11-a-ii', '2-0'), T('b/i', 24, 'q11-b-i', '2-0'),
   T('b/ii', 4, 'q11-b-ii', '2-0'), T('b/iii', 4, 'q11-b-iii', '2-0'), T('c/i', 16, 'q11-c-i', '2-0'),
   T('c/ii/agree', 6, 'q11-c-ii-agree', '2-0'), T('c/ii/disagree', 6, 'q11-c-ii-disagree', '2-0')],
  'Eight routes; 75 with one stance. a(i) YES ticked 4 + justify 5 = 9: the scheme credits YES only, an objective classification, one card. a(ii) disadvantage AND advantage 12, 1st 8 / 2nd 4. b(i) MC, AR, MR 3 x 8. b(ii) P1 and AC1 on the diagram 4. b(iii) one barrier 4. c(i) Dunnes Stores and Tesco 2 x 8. c(ii) Agree 6 OR Disagree 6.',
  'Monopoly, its equilibrium, barriers to entry and oligopoly shares are market structures (NCCA 3.1).')
q(12, [14, 15, 16], [20, 21, 22, 23],
  [T('a/i', 10, 'q12-a-i', '1-1'), T('a/ii', 10, 'q12-a-ii', '2-0'), T('b/i', 7, 'q12-b-i', '3-1'),
   T('b/ii', 20, 'q12-b-ii', '3-1'), T('c/i', 8, 'q12-c-i', '3-4'), T('c/ii', 16, 'q12-c-ii', '3-4'), T('c/iii', 4, 'q12-c-iii', '3-4')],
  'Seven tasks totalling 75: a(i) 10; a(ii) 10; b(i) 7; b(ii) two aims each justified 2 x 10; c(i) 8; c(ii) two institutions 2 x 8; c(iii) 4.',
  'Determinants of demand for flights are NCCA 2.2. A new entrant increasing competition is NCCA 3.1. Water investment and government economic aims are fiscal (NCCA 4.2). Revolut, financial institutions and regulation are NCCA 4.5.')
q(13, [17, 18, 19], [24, 25, 26, 27, 28],
  [T('a/i', 6, 'q13-a-i', '3-1'), T('a/ii/trend', 12, 'q13-a-ii', '3-1'),
   T('a/ii/positive', 3, 'q13-a-ii-positive', '3-1'), T('a/ii/negative', 3, 'q13-a-ii-negative', '3-1'),
   T('a/iii', 6, 'q13-a-iii', '3-1'), T('b/i/households', 8, 'q13-b-i-households', '3-1'), T('b/i/economy', 8, 'q13-b-i-economy', '3-1'),
   T('b/ii', 8, 'q13-b-ii', '3-1'), T('b/iii/agree', 8, 'q13-b-iii-agree', '3-1'), T('b/iii/disagree', 8, 'q13-b-iii-disagree', '3-1'),
   T('c/i', 8, 'q13-c-i', '4-1'), T('c/ii', 16, 'q13-c-ii', '4-1')],
  'Twelve routes; 75 with one route per choice. a(i) 6. a(ii) trend with figures 12 and the positive/negative opinion 3 are separately priced: the trend is one task and the opinion has two routes. a(iii) 6. b(i) households OR economy 8 each. b(ii) 8. b(iii) Agree OR Disagree 8 each. c(i) 8. c(ii) 2 x 8.',
  'Corporation tax, tax cuts, budget surpluses and welfare increases are fiscal policy (NCCA 4.2). MNC hiring and relocation are globalisation and MNCs (NCCA 5.2).')
q(14, [20, 21, 22], [29, 30, 31, 32],
  [T('a/i', 10, 'q14-a-i', '3-3'), T('a/ii/yes', 10, 'q14-a-ii-yes', '3-3'), T('a/ii/no', 10, 'q14-a-ii-no', '3-3'),
   T('b/i/employee', 12, 'q14-b-i-employee', '1-3'), T('b/i/employer', 12, 'q14-b-i-employer', '1-3'),
   T('b/ii', 12, 'q14-b-ii', '3-1'), T('b/iii', 6, 'q14-b-iii', '3-0'),
   T('c/i', 5, 'q14-c-i', '1-4'), T('c/ii', 8, 'q14-c-ii', '1-0'), T('c/iii', 12, 'q14-c-iii', '1-1')],
  'Ten routes; 75 with one route per choice. a(i) 10. a(ii) YES OR NO 10 each (scheme lists both). b(i) advantage to the employee OR disadvantage to the employer 1 x 12 each. b(ii) 12. b(iii) 6. c(i) 5. c(ii) 8. c(iii) 12.',
  'Price inflation is NCCA 4.4. A compulsory-enrolment pension scheme is government intervention (NCCA 2.4). Investing for an ageing population is fiscal (NCCA 4.2). Modified Domestic Demand is a national-income measure (NCCA 4.1). PED is NCCA 2.2 (deck 2.5); electricity price causes are market supply and demand (NCCA 2.1); household responses are consumer behaviour (NCCA 2.2).')
q(15, [23, 24, 25], [33, 34, 35, 36],
  [T('a/i', 16, 'q15-a-i', '2-2'), T('a/ii/agree', 8, 'q15-a-ii-agree', '1-3'), T('a/ii/disagree', 8, 'q15-a-ii-disagree', '1-3'),
   T('b/i', 8, 'q15-b-i', '1-2'), T('b/ii', 4, 'q15-b-ii', '1-2'), T('b/iii', 16, 'q15-b-iii', '1-5'),
   T('c/i', 11, 'q15-c-i', '3-0'), T('c/ii', 12, 'q15-c-ii', '3-0')],
  'Eight routes; 75 with one stance. a(i) private 8 + social 8, both required. a(ii) Agree OR Disagree 8 each. b(i) 8. b(ii) 4. b(iii) total cost and profit 16 with no published split. c(i) explanation 7 + example 4. c(ii) businesses 6 + government 6.',
  'Private and social benefits of sport spending are externalities (NCCA 3.3). Subsidising gyms is intervention (NCCA 2.4). The firm and its sole-supplier contract are NCCA 2.3; cost and profit are NCCA 2.3 (deck 2.6). The hidden economy is NCCA 4.1.')
q(16, [26, 27, 28], [37, 38, 39, 40, 41],
  [T('a/i', 8, 'q16-a-i', '4-2'), T('a/ii', 8, 'q16-a-ii', '4-2'), T('a/iii', 9, 'q16-a-iii', '4-2'),
   T('b/i', 6, 'q16-b-i', '2-1'), T('b/ii', 7, 'q16-b-ii', '2-1'), T('b/iii', 12, 'q16-b-iii', '1-3'),
   T('c/i', 8, 'q16-c-i', '2-1'), T('c/ii', 8, 'q16-c-ii', '2-1'), T('c/iii', 9, 'q16-c-iii', '2-1')],
  'Nine tasks totalling 75. a 8 + 8 + 9. b(i) any two of land, labour, capital 2 x 3 (no printed pool: an answer list, one card). b(ii) explain one of them 7. b(iii) 12. c 8 + 8 + 9.',
  'Tariffs and trade policy are NCCA 5.3. Factors of production are NCCA 3.2; encouraging entrepreneurship is government intervention (NCCA 2.4). The minimum wage and rewarding employees are the labour market (NCCA 3.2).')
SEL = {
 'Answer 4 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 4 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 8 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Answer 8 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; all independently practicable tasks remain in census.'),
 'Questions 2, 3 and 4 contain an internal choice.': ('finite-route', 'Q2, Q3 and Q4 each offer (a) OR (b); every alternative is carded.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer (a) or (b)': ('finite-route', 'Printed alternative pair; (a) and (b) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between printed alternatives.'),
}
PAGE_SEL = {
 (4, '(a) Discuss one private benefit or one social benefit for the Irish economy if more people'): ('finite-route', 'Q2(a) private OR social tick; scheme lists both at 12, two routes.'),
 (4, '(b) Outline one way in which the Irish Government or car retailers could further encourage the'): ('finite-route', 'Q2(b) Government OR car retailers tick; scheme lists both, two routes.'),
 (4, 'Indicate your choice by placing a tick () in the relevant box below and justify your choice.'): ('finite-route', 'Q2(a)/(b) tick boxes for the two printed routes of each part.'),
 (6, '(a) Do you consider this proposed spending on the light rail system in Cork current or capital'): ('answer-classification', 'Q4(a): the scheme ticks Capital only; an objective classification, one card.'),
 (6, '(b) Outline one possible economic advantage or one possible economic disadvantage to the Irish'): ('finite-route', 'Q4(b) advantage OR disadvantage; scheme lists both, two routes.'),
 (6, 'Indicate your choice by placing a tick () in the relevant box below and explain your answer.'): ('finite-route', 'Q4(a) classification tick and Q4(b) route tick.'),
 (7, 'Discuss one possible advantage or one possible disadvantage of aid for developing countries.'): ('finite-route', 'Q5 advantage OR disadvantage; scheme lists both, two routes.'),
 (8, 'Agree: Disagree:'): ('finite-route', 'Q8 agree/disagree routes.'),
 (8, 'Indicate with a tick () if you agree or disagree with this statement. Justify your answer.'): ('finite-route', 'Q8 agree/disagree routes.'),
 (10, 'State one of the areas in which government expenditure'): ('answer-classification', 'Q10(i) lowest area: Transport and Justice tie at €4bn; either is correct, one answer slot.'),
 (11, '(i) Is Irish Rail an example of a monopoly? YES: NO:'): ('answer-classification', 'Q11(a)(i): the scheme ticks YES only; one card.'),
 (11, 'monopoly market structure to Irish consumers and/or the Irish economy.'): ('not-a-task-selection', 'Flexible and/or scope wording; the disadvantage and advantage are both required.'),
 (13, 'Do you agree or disagree with this statement? Agree: Disagree:'): ('finite-route', 'Q11(c)(ii) agree/disagree routes.'),
 (17, 'Is this trend a positive development: OR a negative development:'): ('finite-route', 'Q13(a)(ii) positive OR negative opinion; scheme lists both at 3, two routes.'),
 (17, 'the graph above. In your opinion, is this trend a positive development or a negative'): ('finite-route', 'Q13(a)(ii) positive OR negative opinion routes.'),
 (18, '(i) Discuss one benefit to either households or the economy if the government reduce'): ('finite-route', 'Q13(b)(i) households OR economy; scheme lists both, two routes.'),
 (18, 'Agree Disagree'): ('finite-route', 'Q13(b)(iii) agree/disagree routes.'),
 (18, 'Do you agree or disagree with this increase?'): ('finite-route', 'Q13(b)(iii) agree/disagree routes.'),
 (18, 'Indicate your choice with a tick () in the relevant box below. Justify your answer.'): ('finite-route', 'Q13(b)(iii) stance tick boxes.'),
 (20, 'In your opinion does this benefit consumers in Ireland? YES: NO:'): ('finite-route', 'Q14(a)(ii) YES OR NO; scheme lists both, two routes.'),
 (21, '(i) Outline one possible economic advantage to the employee or one possible economic'): ('finite-route', 'Q14(b)(i) employee advantage OR employer disadvantage; two routes.'),
 (23, '(ii) Do you agree or disagree with this statement?'): ('finite-route', 'Q15(a)(ii) agree/disagree routes.'),
 (23, 'Agree Disagree'): ('finite-route', 'Q15(a)(ii) agree/disagree routes.'),
 (27, '(b) Entrepreneurs take a risk in organising the other factors of production to produce a good or a'): ('not-a-task-selection', 'Stem wording ("other factors"), not a selection.'),
 (27, '(i) Name any two factors of production other than enterprise.'): ('answer-classification', 'Q16(b)(i): no options are printed; the scheme accepts any two of land, labour and capital, so it is one card with an answer list, not a printed route pool.'),
 (27, '(ii) Explain one of the factors of production you named above in part (i).'): ('answer-classification', 'Q16(b)(ii) explains one factor the candidate already named; one card listing the three accepted definitions.'),
 (28, '(ii) Outline one economic argument against any further increase in the minimum wage in'): ('not-a-task-selection', 'Wording ("any further increase"), not a selection.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 32: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})
tasks = [t for x in Q for t in x['tasks']]
draft = {
 'subjectId': 'economics', 'year': 2026, 'level': 'ordinary', 'lang': 'ev', 'fileid': 'LC034GLP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-10-11',
 'visuallyInspectedPaperPages': list(range(1, 33)), 'visuallyInspectedSchemePages': list(range(1, 48)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Census drafted from the paired visual sweep before any 2026 Ordinary card existed: all 32 paper and 47 scheme pages viewed. {len(tasks)} routes ({sum(1 for t in tasks if "-sa-" in t["cardId"])} Section A + {sum(1 for t in tasks if "-sa-" not in t["cardId"])} Section B), {len(sels)} raw directive lines classified. Scheme PDF pp42-45 research brief/rubric and p46-47 back pages add no written-paper asks. The scheme heads Section A "75 marks" where the paper prints 100; every task tariff is unaffected.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2026-ol-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
alt = ('/social', '/retailers', '/disadvantage', 'disadvantage', '/disagree', '/negative', '/economy', '/no', '/employer')
for x in Q:
    once = sum(t['marks'] for t in x['tasks'] if not any(t['key'].endswith(a) for a in alt)
               and not (x['n'] in '234' and t['key'] == 'b' and int(x['n']) == 3))
    print('Q', x['n'], once)
