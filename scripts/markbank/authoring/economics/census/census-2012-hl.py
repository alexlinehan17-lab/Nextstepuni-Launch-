"""Write the independent 2012 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2012 Higher
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2012/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2012/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2012-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once. Section A Q8 (Yes / No) and Section B
# Q5(c)(ii) (Yes / No) and Q8(a)(i) (two push OR two pull factors) are printed
# choices whose scheme credits each side with its own answer: one route each,
# the first counted. Section B Q7(a)(ii) is answered by any of the scheme's
# three options, each credited with its own points: one route each, the first
# counted.
ALT = ('-no', '-pull', '-option-2', '-option-3')

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '1-1')],
  'Three reasons from six: 6 + 5 + 5.',
  'Shifts in the demand curve for bottled water are The Consumer (Demand) (1-1).')
q(2, [2], [5], [T('all', 16, 'sa-q2', '3-3')],
  'Three areas of responsibility from five: 6 + 5 + 5.',
  'The ECB is Monetary Policy & Inflation (3-3).')
q(3, [2], [6], [T('all', 16, 'sa-q3', '3-0')],
  'Two reasons at 4 from four + two effects for the Exchequer at 4 from five: one card, two rows.',
  'The black economy is National Income (3-0); its effects for the Exchequer are also Fiscal Policy & the Budget (3-1).', also=['3-1'])
q(4, [2], [6], [T('all', 16, 'sa-q4', '1-5')],
  'The four ticks at 4: one card. The paper’s “(a) economy of scale or (b) diseconomy of scale” labels the table’s two column groups and is not two parts.',
  'Internal and external economies and diseconomies of scale are Costs of Production, Revenue & Profit (1-5).')
q(5, [2], [6], [T('a', 10, 'sa-q5-a', '1-4'), T('b', 6, 'sa-q5-b', '1-4')],
  'a 10; b 6 for the example and its reason, which the scheme does not divide: questionTotal, unpriced rows.',
  'Income elasticity of demand and inferior goods are Elasticity (1-4).')
q(6, [3], [7], [T('i', 9, 'sa-q6-i', '3-0'), T('ii', 8, 'sa-q6-ii', '3-0')],
  'i 9 and ii 8, each claimed with its answer beside the hidden working (the paper’s table beside the ask).',
  'The marginal propensity to save and the multiplier are National Income (3-0).')
q(7, [3], [8], [T('all', 17, 'sa-q7', '3-4')],
  'Three factors from five: 6 + 6 + 5.',
  'The rate of savings and the factors affecting it are Financial Sector (3-4).')
q(8, [3], [8], [T('all', 17, 'sa-q8-yes', '2-0'), T('all', 17, 'sa-q8-no', '2-0')],
  'Yes / No is a printed choice and the scheme credits each side with its own answer: one route each, counted once. Each 1 + 8 + 8: the answer 1, then the explanation’s two points at 8.',
  'Imperfect competition and the waste of resources are Market Structures (2-0).')
q(9, [3], [9], [T('a', 8, 'sa-q9-a', '3-1'), T('b', 9, 'sa-q9-b', '3-1')],
  'a 2 advantages at 4 from six; b 9 for the answer and its explanation, which the scheme does not divide: questionTotal, unpriced rows.',
  'The household charge, its advantages for the Exchequer and progressive and regressive taxes are Fiscal Policy & the Budget (3-1).')

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [4], [10, 11, 12],
  [T('a/i', 10, 'sb-q1-a-i', '1-1'), T('a/ii', 15, 'sb-q1-a-ii', '1-1'), T('b', 30, 'sb-q1-b', '1-4'),
   T('c/i', 10, 'sb-q1-c-i', '1-4'), T('c/ii', 10, 'sb-q1-c-ii', '1-4')],
  'Five tasks totalling 75. a(i) 10; a(ii) 3 at 5 from three. b 10 a product, which the scheme does not divide between the price change, the type of good, the reason, the effect on total revenue and the demand curve (hidden solution table). c(i) and c(ii) each 10 (4 + 6): the answer 4 and the explanation 6.',
  'The equi-marginal principle and the assumptions of consumer behaviour are The Consumer (Demand) (1-1); price and cross elasticity of demand are Elasticity (1-4).')
q('B2', [4], [13, 14, 15, 16],
  [T('a/i', 10, 'sb-q2-a-i', '2-0'), T('a/ii', 10, 'sb-q2-a-ii', '2-0'), T('b/i', 17, 'sb-q2-b-i', '2-0'),
   T('b/ii', 18, 'sb-q2-b-ii', '2-0'), T('c', 20, 'sb-q2-c', '2-0')],
  'Five tasks totalling 75. a(i) 6 + 4 (the price taker 6, then either explanation 4); a(ii) 2 at 5 from four. b(i) the diagram 7 (its seven elements at 1) + the explanation 5 at 2 (hidden solution diagram); b(ii) the market diagram 4 + the firm diagram 4 (their elements at 1) + the explanation 5 at 2 (hidden solution diagrams). c the four headings 6 + 6 + 4 + 4.',
  'Perfect competition, its short-run equilibrium, the entry of new firms and the contrast with monopoly are Market Structures (2-0).')
q('B3', [5], [17, 18, 19, 20],
  [T('a/i', 10, 'sb-q3-a-i', '2-1'), T('a/ii', 15, 'sb-q3-a-ii', '2-1'), T('b/i', 15, 'sb-q3-b-i', '0-1'),
   T('b/ii', 15, 'sb-q3-b-ii', '0-1'), T('c', 20, 'sb-q3-c', '2-0')],
  'Five tasks totalling 75. a(i) the two terms at 5; a(ii) economic rent 5 + 2 circumstances at 5 from four. b(i) 3 at 5 from nine; b(ii) 3 at 5 from nine. c 4 at 5 from eight.',
  'Supply price, transfer earnings and economic rent are factor incomes, The Labour Market (2-1); the entrepreneur and entrepreneurship are Scarcity & Choice (0-1); the survival of small firms is Market Structures (2-0), as 2016 HL files it.')
q('B4', [5], [21, 22, 23],
  [T('a/i', 13, 'sb-q4-a-i', '1-5'), T('a/ii', 12, 'sb-q4-a-ii', '1-5'), T('b', 25, 'sb-q4-b', '1-2'),
   T('c/i', 15, 'sb-q4-c-i', '1-5'), T('c/ii', 10, 'sb-q4-c-ii', '1-5')],
  'Five tasks totalling 75. a(i) 13 (6 + 3 + 4): the diagram 6, SRAC 3, LRAC 4 (hidden solution diagram); a(ii) 12 (6 + 6): the diagram 6, the relationship 6 (hidden solution diagram). b 5 at 5 from nineteen, within and across countries. c(i) 15 (9 + 6): the minimum price 9, its explanation 6; c(ii) 10 (6 + 4): the minimum price 6, its explanation 4. The paper prints (c)(ii) inside the line of (c)(i).',
  'Short- and long-run average cost, marginal cost and the minimum price in the short and long run are Costs of Production, Revenue & Profit (1-5); where a firm locates is The Firm (Supply) (1-2), as 2014 HL files it.')
q('B5', [6], [24, 25, 26, 27],
  [T('a/i', 10, 'sb-q5-a-i', '3-5'), T('a/ii', 20, 'sb-q5-a-ii', '3-5'), T('b/i', 15, 'sb-q5-b-i', '4-0'),
   T('b/ii', 10, 'sb-q5-b-ii', '4-0'), T('c/i', 10, 'sb-q5-c-i', '0-0'), T('c/ii', 10, 'sb-q5-c-ii-yes', '0-0'),
   T('c/ii', 10, 'sb-q5-c-ii-no', '0-0')],
  'Six tasks totalling 75. a(i) 2 at 5 from six; a(ii) 4 at 5 from six. b(i) 3 at 5 from seven; b(ii) one advantage 5 from six + one disadvantage 5 from four. c(i) 10 (4 + 4 + 2); c(ii) Yes / No is a printed choice and the scheme credits each side with its own column, 2 points at 5: one route each, counted once.',
  'World population growth and its effects on the Irish economy are Economic Growth (3-5); economic growth in developing countries is Growth & Development (4-0); Malthus’s theory of population is Economics as a Way of Thinking (0-0) and also Economic Growth (3-5).')
q('B6', [6], [28, 29, 30],
  [T('a', 20, 'sb-q6-a', '3-1'), T('b/i', 8, 'sb-q6-b-i', '3-1'), T('b/ii', 20, 'sb-q6-b-ii', '3-1'),
   T('b/iii', 7, 'sb-q6-b-iii', '1-3'), T('c', 20, 'sb-q6-c', '1-3')],
  'Five tasks totalling 75. a 4 at 5 from twelve, each with a current statistic. b(i) 8 for the explanations and examples, which the scheme does not divide: questionTotal, unpriced rows; b(ii) 2 advantages at 5 from six + 2 disadvantages at 5 from six; b(iii) the 1st correct point 4 and the 2nd 3, from four. c 2 arguments in favour at 5 from four + 2 against at 5 from five.',
  'The government’s economic aims and direct and indirect taxes are Fiscal Policy & the Budget (3-1); a tax on sugary foods is Government Intervention (1-3), as 2013 OL files a sugar tax; students contributing to the cost of third-level education is Government Intervention (1-3) and also Fiscal Policy & the Budget (3-1).')
q('B7', [7], [31, 32, 33, 34],
  [T('a/i', 10, 'sb-q7-a-i', '4-2'), T('a/ii', 8, 'sb-q7-a-ii-option-1', '4-2'), T('a/ii', 8, 'sb-q7-a-ii-option-2', '4-2'),
   T('a/ii', 8, 'sb-q7-a-ii-option-3', '4-2'), T('a/iii', 12, 'sb-q7-a-iii', '4-2'), T('b/i', 15, 'sb-q7-b-i', '4-2'),
   T('b/ii', 10, 'sb-q7-b-ii', '4-2'), T('c', 20, 'sb-q7-c', '4-2')],
  'Six tasks totalling 75. a(i) 10 (6 + 4); a(ii) 8 by any of the scheme’s three options, each credited with its own points: option 1 3 + 3 + 2, options 2 and 3 8 undivided (questionTotal): one route each, counted once; a(iii) 4 at 3. b(i) 3 at 5 from six; b(ii) 2 at 5 from three. c 4 at 5 from eight.',
  'Comparative advantage, the terms of trade, competitiveness and the gains from trade are International Trade & Competitiveness (4-2); the effects of slower euro-area growth on the Irish economy are also Economic Growth (3-5).', also=['3-5'])
q('B8', [7], [35, 36, 37, 38],
  [T('a/i', 10, 'sb-q8-a-i-push', '3-2'), T('a/i', 10, 'sb-q8-a-i-pull', '3-2'), T('a/ii', 20, 'sb-q8-a-ii', '3-2'),
   T('b/i', 5, 'sb-q8-b-i', '3-2'), T('b/ii', 15, 'sb-q8-b-ii', '3-2'), T('c/i', 13, 'sb-q8-c-i', '3-1'),
   T('c/ii', 12, 'sb-q8-c-ii', '0-0')],
  'Six tasks totalling 75. a(i) two push OR two pull factors is a printed choice and the scheme credits each with its own column, 2 at 5: one route each, counted once; a(ii) 2 negative at 5 from five + 2 positive at 5 from four. b(i) 5; b(ii) 3 at 5 from five. c(i) 13 (9 + 4); c(ii) 2 at 6 from seven.',
  'Emigration, its push and pull factors and consequences and the Live Register are Employment & Unemployment (3-2); Keynes’s use of fiscal policy for full employment is Fiscal Policy & the Budget (3-1), and his other concepts Economics as a Way of Thinking (0-0).')

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 8': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 9)},
}
PAGE_SEL = {
 (3, '(b) Is this a progressive tax or a regressive tax? Explain your answer.'): ('answer-classification', 'Section A Q9(b) progressive or regressive is the answer (regressive); one card.'),
 (3, '8. ‘Imperfect Competition is wasteful of resources’. Do you agree with this statement? Yes /No'): ('finite-route', 'Section A Q8 Yes or No: the scheme credits each side with its own explanation, so one route per side, counted once.'),
 (6, '6. (a) One of the economic aims of the Irish Government at present is to decrease government current'): ('not-a-task-selection', 'Section B Q6(a) stem wording, read on "One"; not a selection.'),
 (6, 'justify your choice. (20)'): ('not-a-task-selection', 'Section B Q6(a) ask wording ("use relevant statistics/information to justify your choice"), read on "choice"; the four aims are the ask, not a selection.'),
 (7, '(i) Describe two economic ‘push’ factors OR two economic ‘pull’ factors currently affecting'): ('finite-route', 'Section B Q8(a)(i) two push OR two pull factors: the scheme credits each with its own column, so one route each, counted once.'),
 (2, '4. In relation to each statement listed below, indicate whether it is an internal or external'): ('answer-classification', 'Section A Q4 internal or external is the answer for each statement; one card, four answers.'),
 (2, '(a) economy of scale or (b) diseconomy of scale. (Place a tick (√) for each correct answer.)'): ('answer-classification', 'Section A Q4 internal or external economy or diseconomy of scale is the answer for each statement; one card, four answers.'),
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
 'subjectId': 'economics', 'year': 2012, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 9)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 8 paper and 40 scheme pages (paper page 8 is blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the support notes with the index, and pages 39-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 55 printed asks (12 Section A + 43 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2012_hl.py). Section A Q8 and Section B Q5(c)(ii) (Yes / No) and Q8(a)(i) (push OR pull) are one route for each side the scheme credits, and Section B Q7(a)(ii) one route for each of the scheme’s three options, each counted once.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2012-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
