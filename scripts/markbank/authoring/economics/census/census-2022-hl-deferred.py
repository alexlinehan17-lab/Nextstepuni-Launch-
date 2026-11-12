"""Write the independent 2022 HL deferred-sitting EV census draft from a full visual sweep (2026-11-04).

The deferred paper is its own sitting: the archive files it under
deferredexams/ and deferredmarkingschemes/ with the June file id, Paper Trail
indexes it as "LC034ALP000EV-deferred", and every card id carries "-deferred-".
All 40 paper pages and all 40 scheme pages were viewed (scheme PDF page =
printed page; PDF pages 37-40 are blank and the back cover). The hand count of
the printed asks is 70 (Section A 23, Section B 47), the reader's own count.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/deferredexams/2022/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/deferredmarkingschemes/2022/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2022-hl-deferred-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, extra=()):
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in extra]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

q(1, [3], [4, 5], [T('a', 6, 'sa-q1-a', '4-1'), T('b', 9, 'sa-q1-b', '4-1')],
  'a two positive consequences of FDI from six, 3 each; b reasons to invest abroad, three from five at 3 (1 + 2). The scheme prints "1 x 6 (3+3)" and "3 x 3 (1+2)" together beside (a) and nothing beside (b): (a) asks for two, so it takes the 6 and (b) the 3 x 3, the question\'s 15.',
  'Foreign direct investment and why firms invest abroad are Globalisation (4-1); the consequences the scheme names include economic growth (3-5) and exports (4-2).',
  extra=('3-5', '4-2'))
q(2, [4], [5, 6], [T('a', 10, 'sa-q2-a', '1-0'), T('b', 5, 'sa-q2-b', '0-1')],
  'a diagram 7 (seven labels at 1, hidden solution; the blank axes are the question figure) + explanation 3 x 1. b 5 scarcity, three wordings.',
  'A fall in supply on the market diagram is The Market Economy (1-0), the supply side The Firm (Supply) (1-2); scarcity is Scarcity & Choice (0-1).',
  extra=('1-2',))
q(3, [5], [6], [T('a', 10, 'sa-q3-a', '1-4'), T('b', 5, 'sa-q3-b', '1-4')],
  'a 5 x 2, the five figures of the YED working (+7.35). b 1 x 3 + 1 x 2 beside two headings, the sign 3 and the number 2.',
  'Income elasticity of demand is Elasticity (1-4).')
q(4, [6], [7], [T('a', 8, 'sa-q4-a', '1-3'), T('b', 7, 'sa-q4-b', '1-2')],
  'a 2 x 4 (2 + 2) two reasons from three. b printed Yes/No; the scheme answers No only: diagram 3 x 1 (hidden solution) + 2 x 2 explanation, one card.',
  'Banning ticket touting is Government Intervention (1-3); a supply fixed by capacity is The Firm (Supply) (1-2), on The Market Economy\'s diagram (1-0).',
  extra=('1-0',))
q(5, [7, 8], [8, 9], [T('a', 7, 'sa-q5-a', '4-2'), T('b', 8, 'sa-q5-b', '3-5'), T('c', 8, 'sa-q5-c', '3-5')],
  'a 1 x 4 (2 + 2), 1 x 3 (1 + 2) two sources from four. Answer (b) 2 x 4 (2 + 2) two benefits from six OR (c) 2 x 4 (2 + 2) two reasons from six; the alternatives count once.',
  'Comparative advantage is International Trade & Competitiveness (4-2); rural broadband and balanced regional development are Economic Growth (3-5).')
q(6, [9], [9, 10], [T('a', 9, 'sa-q6-a', '3-0'), T('b', 6, 'sa-q6-b', '3-0')],
  'a "Any 3 x 3" beside one definition with three parts in bold, 3 each. b ANY TWO of A, B or C at 3 (2 x 3), one card; the data table and answer grid are the figure.',
  'GNP, GNI and GNI* are National Income (3-0).')
q(7, [10, 11], [10, 11], [T('a', 7, 'sa-q7-a', '0-2'), T('b', 8, 'sa-q7-b', '4-0'), T('c', 8, 'sa-q7-c', '4-0')],
  'a 1 x 4 (2 + 2), 1 x 3 (1 + 2) two measures from four. Answer (b) 2 x 4 (2 + 2) two reasons from seven OR (c) 2 x 4 (2 + 2) two challenges from six; the alternatives count once.',
  'Protecting the environment is Sustainability (0-2) and the government\'s measures (a carbon tax, grants) Government Intervention (1-3); aid to less developed nations is Growth & Development (4-0).',
  extra=('1-3',))
q(8, [11], [11], [T('a', 7, 'sa-q8-a', '0-2'), T('b', 8, 'sa-q8-b', '2-2')],
  'a printed "Do you agree?"; the scheme answers Yes only, 7. b printed True/False; the scheme ticks True 2 + explanation 6.',
  'A world of 8 billion is Sustainability (0-2); electric cars as a market failure are Market Failure (2-2).')
q(9, [12, 13], [12], [T('a', 7, 'sa-q9-a', '1-5'), T('b', 8, 'sa-q9-b', '1-5'), T('c', 8, 'sa-q9-c', '1-5')],
  'a 7 x 1, four totals and three marginal revenues (hidden completed table; the blank table is the question figure). Answer (b) one benefit OR (c) one disadvantage, each priced "2 x 4 (2+2)", 8: the one response is assessed against the 8; the alternatives count once.',
  'Total and marginal revenue and specialisation are Costs of Production, Revenue & Profit (1-5).')
q(10, [14], [13], [T('a', 8, 'sa-q10-a', '3-3'), T('b', 7, 'sa-q10-b', '3-3')],
  'a 2 x 4 (2 + 2) two trends from four periods. b "7 (4+3)" one developed effect from five, as the same price is one response beside Q12(c)(ii) and (iii).',
  'The benchmark interest rate and its effect on borrowers are Monetary Policy & Inflation (3-3).')
q(11, [15, 16, 17, 18], [14, 15, 16],
  [T('a/i', 7, 'q11-a-i', '3-1'), T('a/ii', 12, 'q11-a-ii', '3-1'), T('a/iii', 6, 'q11-a-iii', '3-1'),
   T('b/i', 8, 'q11-b-i', '4-2'), T('b/ii', 12, 'q11-b-ii', '4-2'), T('c/i', 13, 'q11-c-i', '3-0'),
   T('c/ii', 12, 'q11-c-ii', '3-0'), T('c/iii', 5, 'q11-c-iii', '3-0')],
  'Eight tasks totalling 75. a(i) 2018 4 + 2019 3; a(ii) 4 x 3; a(iii) printed Expansionary/Contractionary, the scheme ticks Expansionary 1 + explanation 5, one card. b(i) US and GB 4 (2 x 2) each; b(ii) one benefit 6 (3 + 3) AND one challenge 6 (3 + 3), one card. c(i) 13 x 1 (hidden solution); c(ii) 2 + 2 x 2 + 2 + 2 x 2; c(iii) 5.',
  'The budget surplus, the 2020 deficit and expansionary policy are Fiscal Policy & the Budget (3-1); trade with the US and Great Britain and imports International Trade & Competitiveness (4-2); the circular flow, injections and leakages National Income (3-0).')
q(12, [19, 20, 21, 22], [17, 18, 19, 20],
  [T('a/i', 12, 'q12-a-i', '2-0'), T('a/ii', 7, 'q12-a-ii', '2-0'), T('b/i', 17, 'q12-b-i', '2-0'),
   T('b/ii', 10, 'q12-b-ii', '2-0'), T('b/iii', 8, 'q12-b-iii', '2-0'), T('c/i', 7, 'q12-c-i', '1-3'),
   T('c/ii', 7, 'q12-c-ii', '2-0'), T('c/iii', 7, 'q12-c-iii', '2-0')],
  'Eight tasks totalling 75. a(i) 2008 6 (3 + 3) + 2021 6 (3 + 3) (the scheme heads the second "2001"); a(ii) 1 x 4, 1 x 3. b(i) 9 labels + 8 marked points (hidden solution); b(ii) one advantage AND one disadvantage, "1 x 6 (3+3)" and "1 x 4 (2+2)", read in order, one card; b(iii) printed Agree/Disagree, the scheme ticks Agree only, 2 x 4 (2 + 2). c(i), c(ii), c(iii) 7 (4 + 3) each, one response.',
  'Market concentration, perfect competition and monopoly power are Market Structures (2-0); regulating markets is Government Intervention (1-3).')
q(13, [23, 24, 25, 26], [21, 22, 23, 24],
  [T('a/i', 10, 'q13-a-i', '3-2'), T('a/ii', 5, 'q13-a-ii', '2-1'), T('a/iii', 8, 'q13-a-iii', '3-2'),
   T('b/i', 7, 'q13-b-i', '2-1'), T('b/ii', 21, 'q13-b-ii', '2-1'), T('c/i', 6, 'q13-c-i', '3-3'),
   T('c/ii', 12, 'q13-c-ii', '3-1'), T('c/iii', 6, 'q13-c-iii', '3-3')],
  'Eight tasks totalling 75. a(i) 2020-2021 5 + 2022-2023 5; a(ii) 5 (3 + 2) one reason from five; a(iii) 2 x 4 (2 + 2) from six. b(i) 7; b(ii) one effect each on employees, businesses and the government, 7 (4 + 3) each, one card with three groups. c(i) the scheme answers No, 6 (3 + 3); c(ii) 2 x 6 (3 + 3) from eight; c(iii) 1 x 6 (3 + 3) from three.',
  'Unemployment and its effects are Employment & Unemployment (3-2); labour shortages and the living wage The Labour Market (2-1); pensioners and inflation and the ECB\'s measures Monetary Policy & Inflation (3-3); the government\'s measures against inflation Fiscal Policy & the Budget (3-1).')
q(14, [27, 28, 29, 30], [25, 26, 27, 28],
  [T('a/i', 8, 'q14-a-i', '3-1'), T('a/ii', 15, 'q14-a-ii', '3-1'), T('a/iii', 7, 'q14-a-iii', '3-1'),
   T('b/i', 8, 'q14-b-i', '0-1'), T('b/ii', 8, 'q14-b-ii', '0-1'), T('c/i', 12, 'q14-c-i', '1-5'),
   T('c/ii', 8, 'q14-c-ii', '1-5'), T('c/iii', 9, 'q14-c-iii', '1-5')],
  'Eight tasks totalling 75. a(i) 4 x 2 the parts of the working (0.6%); a(ii) 3 x 5 (2 + 3) from eight; a(iii) printed progressive or regressive, the scheme answers regressive, 7. b(i) diagram 4 + explanation 4; b(ii) diagram 4 + 2 x 2 (hidden solutions; the printed PPFs are question figures). c(i) 4 x 3 diagram (hidden solution); c(ii) downward 4 (2 + 2) + upward 4 (2 x 2); c(iii) 3 x 3.',
  'Revenue\'s costs, the principles of taxation and LPT are Fiscal Policy & the Budget (3-1); the PPF and opportunity cost Scarcity & Choice (0-1); SRAC and MC Costs of Production, Revenue & Profit (1-5).')
q(15, [31, 32, 33, 34], [29, 30, 31, 32],
  [T('a/i', 16, 'q15-a-i', '1-0'), T('a/ii', 8, 'q15-a-ii', '1-2'), T('b/i', 14, 'q15-b-i', '1-0'),
   T('b/ii', 14, 'q15-b-ii', '1-0'), T('c/i', 5, 'q15-c-i', '1-3'), T('c/ii', 10, 'q15-c-ii', '1-3'),
   T('c/iii', 8, 'q15-c-iii', '1-3')],
  'Seven tasks totalling 75. a(i) diagram 8 (four labels at 2, hidden solution) + 2 x 2 + 2 x 2; a(ii) 2 x 4 (2 + 2) from six (two bare headings). b(i) and b(ii) diagram 3 x 2 (hidden solution) + 4 x 2, one card each. c(i) 5; c(ii) one argument for 5 (2 + 3) AND one against 5 (2 + 3), one card; c(iii) 2 x 4 (2 + 2) from four.',
  'The market for electric vehicles and shifts in its equilibrium are The Market Economy (1-0); the cost of producing them The Firm (Supply) (1-2); subsidies and intervention Government Intervention (1-3).')
q(16, [35, 36, 37, 38], [33, 34, 35, 36],
  [T('a/i', 8, 'q16-a-i', '3-1'), T('a/ii', 12, 'q16-a-ii', '3-1'), T('b/i', 15, 'q16-b-i', '1-3'),
   T('b/ii', 10, 'q16-b-ii', '1-3'), T('b/iii', 8, 'q16-b-iii', '2-2'), T('c/i', 4, 'q16-c-i', '1-1'),
   T('c/ii', 10, 'q16-c-ii', '1-2'), T('c/iii', 8, 'q16-c-iii', '1-0')],
  'Eight tasks totalling 75. a(i) 2 x 4 (2 + 2) from three periods; a(ii) one positive AND one negative effect, "1 x 8 (4+4)" and "1 x 4 (2+2)", read in order, one card. b(i) diagram 9 (hidden solution) + "6 (2 x 3)" any two of three effects; b(ii) 2 x 5 (2 + 3) from five; b(iii) 2 x 4 (2 + 2) from four. c(i) 4; c(ii) 2 x 5 (3 + 2) from four; c(iii) diagram 4 x 1 (hidden solution) + 2 + 2.',
  'Corporation tax receipts and the 15% rate are Fiscal Policy & the Budget (3-1); minimum pricing and other strategies against alcohol Government Intervention (1-3); its social costs Market Failure (2-2); derived demand The Consumer (1-1), the characteristics of land The Firm (Supply) (1-2) and the market for land The Market Economy (1-0), land a factor of production as earlier reviews file them under Scarcity & Choice (0-1).',
  extra=('0-1',))

SEL = {
 'Answer 3 out of 6 questions.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 3 out of 6 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions from this section.': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Answer 5 out of 10 questions': ('exam-question-selection', 'Whole-exam selection; every independently practicable task stays in the census.'),
 'Write your answers in blue or black pen.': ('not-a-task-selection', 'Administrative instruction.'),
 'end of the booklet. Label any such extra work clearly with the question number and part.': ('not-a-task-selection', 'Administrative instruction about extra pages.'),
 'Answer (b) or (c)': ('finite-route', 'Printed alternative pair; (b) and (c) are separate carded tasks, counted once in the question total.'),
 'OR': ('finite-route', 'Separator between the printed (b)/(c) alternatives.'),
}
PAGE_SEL = {
 (6, 'Yes: No:'): ('answer-classification', 'Q4(b) the scheme answers No only; one card.'),
 (7, 'Ireland has one of the fastest growing data centre markets in Europe. Currently, most data centres'): ('not-a-task-selection', 'Stem wording ("most data centres"), not a selection.'),
 (9, 'use the information above to calculate ANY TWO of the following terms A, B, OR C.'): ('finite-route', 'Q6(b) any two of A, B or C: one card claimed twice at 3.'),
 (11, 'In your opinion, is the statement above true or false? Explain your choice.'): ('answer-classification', 'Q8(b) the scheme ticks True only; one card.'),
 (11, 'unsustainable. Do you agree with this statement? Explain your answer.'): ('answer-classification', 'Q8(a) the scheme answers Yes only and prints no case for disagreeing; one card.'),
 (15, 'Explain your choice using a relevant example to illustrate your understanding.'): ('answer-classification', 'Q11(a)(iii) tail of the tick instruction; Expansionary only.'),
 (15, 'Tick () your choice: Expansionary: Contractionary:'): ('answer-classification', 'Q11(a)(iii) the scheme ticks Expansionary only; one card.'),
 (21, 'Agree: Disagree:'): ('answer-classification', 'Q12(b)(iii) the scheme ticks Agree and prints no disagree answer; one card.'),
 (21, 'Do you agree or disagree with this statement?'): ('answer-classification', 'Q12(b)(iii) Agree only in the scheme.'),
 (27, 'Is LPT a progressive tax or a regressive tax? Justify your answer.'): ('answer-classification', 'Q14(a)(iii) the scheme answers regressive only; one card.'),
 (37, 'Outline two of these possible social costs.'): ('not-a-task-selection', 'Q16(b)(iii) "two of these" is an open count of social costs, not a printed pool.'),
}
sels = []
for (page, text), n in sorted(directives(paper).items()):
    if (page, text) in PAGE_SEL: c, r = PAGE_SEL[(page, text)]
    elif text in SEL: c, r = SEL[text]
    elif page == 40: c, r = ('not-a-task-selection', 'Copyright notice on the back cover.')
    else: raise SystemExit(f'UNCLASSIFIED {page} {text!r}')
    for _ in range(n): sels.append({'page': page, 'text': text, 'classification': c, 'reason': r})

tasks = [t for x in Q for t in x['tasks']]
assert len(tasks) == 70 and len({t['cardId'] for t in tasks}) == 70
for x in Q:
    n = int(x['n'])
    total = sum(t['marks'] for t in x['tasks'])
    # Section A answers (b) or (c) in Q5, Q7 and Q9: the alternatives count once.
    alt = next((t['marks'] for t in x['tasks'] if t['key'] == 'c'), 0) if n in (5, 7, 9) else 0
    assert total - alt == (15 if n <= 10 else 75), (n, total, alt)
draft = {
 'subjectId': 'economics', 'year': 2022, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV-deferred',
 'sitting': 'deferred',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 41)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'The 2022 deferred Higher sitting, read 2026-11-04 from a paired visual sweep of all 40 paper and 40 scheme pages (scheme PDF page = printed page; PDF pages 37-40 blank and the back cover). The hand count of the printed asks is 70 (Section A 23, Section B 47), equal to the reader\'s. {len(tasks)} routes ({sum(len(x["tasks"]) for x in Q if int(x["n"]) <= 10)} Section A + {sum(len(x["tasks"]) for x in Q if int(x["n"]) > 10)} Section B), one per printed ask: every printed choice the scheme answers on one side only is one card on that side, and each two-sided ask with one priced response per side ("one advantage and one disadvantage") is one card. {len(sels)} raw directive lines classified. Stems and asks are sliced from the deferred paper and every marking point from the deferred scheme (econ_2022_hl_deferred.py). Choose-N rule checked: Q6(b) ANY TWO of A, B or C is one card claimed twice.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2022-hl-deferred-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
for x in Q:
    print('Q', x['n'], sum(t['marks'] for t in x['tasks']), x['canonicalNodeIds'])
