"""Write the independent 2015 HL EV census draft from the full visual sweep (lane 2026-11-04).

First review of this paper and its first cards: the old-syllabus paper, nine
short questions in Section A (answer six) and eight long questions in Section B
(answer four), Section B numbered 1-8 again and keyed B1-B8 as the Atlas numbers
it. Every tariff is the scheme's printed cell; this scheme prints no Summary of
Mark Allocations, so each is read beside its part. There is no 2015 Higher
Irish review, so nothing is mirrored.
"""
import hashlib, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
from econ_review import directives
paper = W / 'paper-trail-corpus/exampapers/2015/LC034ALP000EV.pdf'
scheme = W / 'paper-trail-corpus/markingschemes/2015/LC034ALP000EV.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
P = 'econ-2015-hl-'
def T(key, marks, suffix, topic): return {'key': key, 'marks': marks, 'cardId': P + suffix, 'topicId': 'economics-' + topic}
Q = []
def q(n, pp, sp, tasks, boundary, topic_reason, also=()):
    # `also`: a further Atlas topic the question's content belongs to beyond its cards' own.
    nodes = list(dict.fromkeys([t['topicId'] for t in tasks] + ['economics-' + x for x in also]))
    Q.append({'n': str(n), 'paperPages': pp, 'schemePages': sp, 'tasks': tasks,
              'boundaryReason': boundary, 'canonicalNodeIds': nodes, 'topicReason': topic_reason})

# Routes the census counts once: a printed choice the scheme credits with a list
# for each side (the first route of each set is the one counted).
ALT = ('-disagree',)

# ── Section A: nine short questions, 16 or 17 marks each ──────────────────────
q(1, [2], [5], [T('all', 16, 'sa-q1', '0-1')],
  '3 points of information at 8 + 4 + 4, from the scheme’s one answer: one card, the three points claimed at the printed steps.',
  'Scarcity, alternative uses, unlimited wants and choice are Scarcity & Choice (0-1).')
q(2, [2], [5], [T('a', 6, 'sa-q2-a', '1-1'), T('b', 10, 'sa-q2-b', '1-1')],
  'a 6; b 7 the working + 3 the answer (hidden working crop).',
  'The equi-marginal principle of consumer behaviour is The Consumer (1-1).')
q(3, [2], [5], [T('a', 8, 'sa-q3-a', '3-1'), T('b', 8, 'sa-q3-b', '3-1')],
  'a 8; b 2 the answer (good) + 6 one explanation from three.',
  'The NTMA and government borrowing are Fiscal Policy & the Budget (3-1), as 2018 HL files them; bonds and their yield are also Financial Sector (3-4).', also=['3-4'])
q(4, [3], [6], [T('a', 8, 'sa-q4-a', '2-0'), T('b', 8, 'sa-q4-b', '2-0')],
  'a 6 the explanation + 2 one example from four; b 2 @ 4 from three.',
  'Oligopoly and the concentration ratio are Market Structures (2-0).')
q(5, [3], [6], [T('a', 8, 'sa-q5-a', '3-1'), T('b', 8, 'sa-q5-b', '3-1')],
  'a 8; b 2 @ 4 from five.',
  'Regressive and indirect taxation are Fiscal Policy & the Budget (3-1).')
q(6, [3], [7], [T('all', 17, 'sa-q6', '0-0')],
  '9 (4 + 5) + 8 (4 + 4), two contributions from five, the first correct 9.',
  'The Classical economists’ contributions are Economics as a Way of Thinking (0-0).')
q(7, [4], [7], [T('all', 17, 'sa-q7', '1-4')],
  'The four ticks: the 1st correct response 5, then 4 + 4 + 4.',
  'Income, cross-price and price elasticity of demand are Elasticity (1-4).')
q(8, [4], [8], [T('a', 7, 'sa-q8-a', '4-2'), T('b', 10, 'sa-q8-b', '4-2')],
  'a 7; b 2 @ 5 from six, positive or negative.',
  'The euro’s exchange rate against the dollar is International Trade & Competitiveness (4-2).')
q(9, [4], [8], [T('all', 17, 'sa-q9', '3-5')],
  '2 implications @ 6 from seven + one policy measure 5 from five: one card, two rows.',
  'Population ageing is Economic Growth (3-5), as 2019 HL files it; its policy responses (pensions, retirement age) are Fiscal Policy & the Budget (3-1) and The Labour Market (2-1).', also=['3-1', '2-1'])

# ── Section B: eight long questions, 75 marks each, numbered 1-8 again ────────
q('B1', [5], [9, 10, 11, 12],
  [T('a/i', 16, 'sb-q1-a-i', '1-0'), T('a/ii', 14, 'sb-q1-a-ii', '1-0'),
   T('b/i', 10, 'sb-q1-b-i', '1-0'), T('b/ii', 10, 'sb-q1-b-ii', '1-0'), T('b/iii', 10, 'sb-q1-b-iii', '1-0'),
   T('c', 15, 'sb-q1-c', '1-3')],
  'Six tasks totalling 75. a(i) the graph: D/C 6 (5 points + label), S/C 6, the axes 2 and the equilibrium price and quantity 2 (hidden solution graph); a(ii) 10 (6 + 4) the definition + 4 the explanation, by excess demand or excess supply. b each 10: the diagram 5 (D, S1, S2 and the price and quantity indications at 1) + the explanation 5 (shift, price, quantity at 1 and the reason 2) (hidden solution diagrams). c 3 @ 5 (2 + 3) from seven.',
  'Demand, supply, equilibrium and their shifts are The Market Economy (1-0); a rent ceiling is Government Intervention (1-3).')
q('B2', [6], [13, 14, 15, 16],
  [T('a/i', 10, 'sb-q2-a-i', '2-0'), T('a/ii', 25, 'sb-q2-a-ii', '2-0'),
   T('b/i', 10, 'sb-q2-b-i', '2-0'), T('b/ii', 15, 'sb-q2-b-ii', '2-0'), T('c', 15, 'sb-q2-c', '1-3')],
  'Five tasks totalling 75. a(i) 2 @ 5 (2 + 3) from nine; a(ii) the diagram 11 points at 1 + the explanation 14 under the scheme’s five numbered heads (equilibrium 1 + 2, price and output 2 + 1, cost 2, SNP 1 + 2, inefficiency 1 + 2) (hidden solution diagram). b(i) 8 the explanation + 2 one example from four; b(ii) 3 @ 5 (2 + 3), the three conditions. c 3 @ 5 (2 + 3) from seven, for or against regulation.',
  'Monopoly, barriers to entry and price discrimination are Market Structures (2-0); regulating Irish Water is Government Intervention (1-3).', also=['2-0'])
q('B3', [6], [17, 18, 19],
  [T('a', 20, 'sb-q3-a', '1-5'), T('b/i', 12, 'sb-q3-b-i', '1-5'), T('b/ii', 20, 'sb-q3-b-ii', '1-5'),
   T('b/iii', 3, 'sb-q3-b-iii', '1-5'), T('c', 20, 'sb-q3-c', '1-5')],
  'Five tasks totalling 75. a any two of three pairs: 4 explanations @ 5 from six, one card. b(i) fixed costs 6 + variable costs 3 + average cost 3; b(ii) the graph: labels 2, FC 4, TC 7 (2 + 2 + 3), VC 7 (2 + 2 + 3) (hidden solution graph); b(iii) 3 the short run with its reason, printed as one 3: questionTotal, unpriced rows. c 4 @ 5 (2 + 3), at least one economy and one diseconomy.',
  'Marginal, average, explicit and implicit costs, normal and supernormal profit, short-run costs and economies of scale are Costs of Production, Revenue & Profit (1-5).')
q('B4', [7], [20, 21, 22],
  [T('a/i', 10, 'sb-q4-a-i', '0-1'), T('a/ii', 20, 'sb-q4-a-ii', '1-5'),
   T('b/i', 10, 'sb-q4-b-i', '0-1'), T('b/ii', 20, 'sb-q4-b-ii', '3-1'),
   T('c/i', 9, 'sb-q4-c-i', '3-4'), T('c/ii', 6, 'sb-q4-c-ii', '3-4')],
  'Six tasks totalling 75. a(i) 2 @ 5 (2 + 3) from three; a(ii) 4 @ 5 (2 + 3) from six. b(i) 2 @ 5, capital and investment; b(ii) 4 @ 5 (2 + 3), at least one for and one against. c 3 at 5 (1 + 2 + 2) over the scheme’s Statement / Explanation / One main influence columns: (i) each motive 3 (1 + 2); (ii) each influence 2.',
  'Enterprise and capital as factors of production are Scarcity & Choice (0-1); profit is Costs of Production, Revenue & Profit (1-5); investing in the railways is government capital spending, Fiscal Policy & the Budget (3-1); Keynes’s motives for holding money are Financial Sector (3-4) and, as an economist’s contribution, Economics as a Way of Thinking (0-0).', also=['0-0'])
q('B5', [7], [23, 24, 25],
  [T('a/i', 18, 'sb-q5-a-i', '3-4'), T('a/ii', 12, 'sb-q5-a-ii', '3-4'), T('b', 20, 'sb-q5-b', '3-4'),
   T('c', 25, 'sb-q5-c', '3-4')],
  'Four tasks totalling 75. a(i) 3 @ 6 (3 + 3) from five; a(ii) 2 @ 6 (3 + 3) from four. b 3 impacts at 7 (4 + 3) + 7 (4 + 3) + 6 (3 + 3) from six. c 4 benefits at 7 (4 + 3) + 3 @ 6 (3 + 3) from seven.',
  'Credit creation, financial regulation, the Central Bank’s mortgage rules and SME funding are Financial Sector (3-4); the property market is also Government Intervention (1-3).', also=['1-3'])
q('B6', [8], [26, 27, 28, 29],
  [T('a/i', 17, 'sb-q6-a-i', '3-3'), T('a/ii', 8, 'sb-q6-a-ii', '3-3'),
   T('b/i', 15, 'sb-q6-b-i', '3-2'), T('b/ii', 10, 'sb-q6-b-ii', '3-2'),
   T('c/i', 5, 'sb-q6-c-i', '3-2'), T('c/ii', 10, 'sb-q6-c-ii', '3-2'), T('c/iii', 10, 'sb-q6-c-iii', '3-1')],
  'Seven tasks totalling 75. a(i) No 2 + 3 reasons @ 5 (2 + 3) from eight (the scheme credits No only); a(ii) 2 @ 4 (2 + 2) from six. b(i) 3 @ 5 (2 + 3) from five types; b(ii) 2 @ 5 (2 + 3) from five. c(i) 5 the Live Register; c(ii) 2 @ 5 from four; c(iii) 2 @ 5 (2 + 3), revenue and expenditure.',
  'The CPI and deflation are Monetary Policy & Inflation (3-3); types of unemployment, policies and the sources of unemployment statistics are Employment & Unemployment (3-2); the current finances are Fiscal Policy & the Budget (3-1).')
q('B7', [8], [30, 31, 32],
  [T('a/i', 23, 'sb-q7-a-i', '3-0'), T('a/ii', 12, 'sb-q7-a-ii', '3-0'), T('b', 20, 'sb-q7-b', '3-0'),
   T('c/i', 4, 'sb-q7-c-i', '3-5'), T('c/ii', 16, 'sb-q7-c-ii', '3-5')],
  'Five tasks totalling 75. a(i) the diagram 13 (hidden solution diagram) + households 5 + firms 5; a(ii) 6 (3 + 3) for each of exports and savings. b 4 @ 5 (2 + 3) from eight. c(i) 4; c(ii) 4 @ 4 (2 + 2), at least one cost and one benefit.',
  'The circular flow of income and comparing national income statistics are National Income (3-0); economic growth and its costs and benefits are Economic Growth (3-5).')
q('B8', [9], [33, 34, 35, 36],
  [T('a', 20, 'sb-q8-a-agree', '3-1'), T('a', 20, 'sb-q8-a-disagree', '3-1'),
   T('b/i', 15, 'sb-q8-b-i', '3-5'), T('b/ii', 10, 'sb-q8-b-ii', '3-5'),
   T('c/i', 20, 'sb-q8-c-i', '3-2'), T('c/ii', 10, 'sb-q8-c-ii', '3-2')],
  'Five tasks totalling 75. a the reference to the Irish economy 6 (3 + 3) + 2 points at 7 (4 + 3): agree or disagree, each with its own list, so one route per side, counted once. b(i) 3 @ 5 (2 + 3) from five; b(ii) 2 @ 5 (2 + 3) from five. c(i) 4 @ 5 (2 + 3) from the negative and positive columns; c(ii) 2 @ 5 (2 + 3) from six.',
  'The budget deficit is Fiscal Policy & the Budget (3-1); balanced regional development is Economic Growth (3-5), as 2019 OL files it, and its policies Government Intervention (1-3); emigration and returning emigrants are Employment & Unemployment (3-2).', also=['1-3'])

SEL = {
 'Answer four questions.': ('exam-question-selection', 'Whole-exam selection (Section B); every printed task stays in the census.'),
 'Answer six of the nine short response type questions in the spaces provided.': ('exam-question-selection', 'Whole-exam selection (Section A); every printed task stays in the census.'),
 'Answer six questions from Section A and four questions from Section B.': ('exam-question-selection', 'Whole-exam selection; every printed task stays in the census.'),
 **{f'Page {n} of 9': ('not-a-task-selection', 'Page footer, read on "of"; not a selection.') for n in range(1, 10)},
}
PAGE_SEL = {
 (2, '(b) Is selling bonds at a low yield good or bad for the Irish Government? Explain your answer.'): ('answer-classification', 'Section A Q3(b) good or bad is the answer (good); the scheme credits only good: one card.'),
 (2, '1. Outline why ‘choice’ is fundamental to the study of economics.'): ('not-a-task-selection', 'Section A Q1 ask wording, read on "or"; not a selection.'),
 (4, '7. Read each statement below and indicate if the statement is true or false. [Tick () the appropriate box.]'): ('answer-classification', 'Section A Q7 four true/false ticks; one card claimed at 5, 4, 4, 4.'),
 (4, 'one of them should be highly elastic.'): ('not-a-task-selection', 'Section A Q7 statement text, read on "one"; not a selection.'),
 (6, '3. (a) In the case of any two of the following three pairs distinguish between the two concepts:'): ('finite-route', 'Section B Q3(a) any two of three pairs: one card, four explanations claimed at 5.'),
 (6, 'Discuss whether or not Irish Water (Uisce Éireann), Ireland’s new water utility company, should'): ('not-a-task-selection', 'Section B Q2(c) "whether or not" names both sides of one discussion; one menu of both columns.'),
 (6, 'run or the long run? Outline a reason for your answer. (35)'): ('answer-classification', 'Section B Q3(b)(iii) short run or long run is the answer (the short run); one card.'),
 (7, '(ii) Discuss the case for and against the Government investing in Ireland’s railways. (30)'): ('not-a-task-selection', 'Section B Q4(b)(ii) "for and against" names both sides of one discussion; one menu.'),
 (9, 'Discuss this statement with reference to the Irish economy. You may agree or disagree. (20)'): ('answer-classification', 'Section B Q8(a) agree or disagree: the scheme credits each side with its own list, so two stance routes.'),
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
 'subjectId': 'economics', 'year': 2015, 'level': 'higher', 'lang': 'ev', 'fileid': 'LC034ALP000EV',
 'status': 'independent-census-before-authoring', 'completeSubject': False, 'reviewedAt': '2026-11-04',
 'visuallyInspectedPaperPages': list(range(1, 13)), 'visuallyInspectedSchemePages': list(range(1, 41)),
 'unreviewedPaperPages': [], 'unreviewedSchemePages': [],
 'paperSha256': sha(paper), 'schemeSha256': sha(scheme), 'questions': Q, 'selections': sels,
 'reviewNote': f'Review 2026-11-04 from a paired visual sweep of all 12 paper and 40 scheme pages (paper pages 10-12 are blank; scheme pages 1-4 are the SEC cover, the note on published schemes, the title page and the notes and index, and pages 37-40 blank or the back cover; scheme page numbers here are the PDF’s, two ahead of the printed ones; this scheme prints no Summary of Mark Allocations, so every tariff is read beside its part). The old-syllabus paper: Section A nine short questions (answer six), Section B eight long questions (answer four) numbered 1-8 again, keyed B1-B8 as the Atlas numbers them. {len(tasks)} routes for 57 printed asks (14 Section A + 43 Section B), {len(sels)} raw directive lines classified. Every stem and ask is sliced from the paper and every marking point from the scheme (econ_2015_hl.py). The stance route is Section B Q8(a), agree or disagree, each credited with its own list. Section B Q3(a) any two of three pairs is one card.',
 'externalClarifications': [],
 'curriculumSource': 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
 'curriculumNote': 'Sat on the outgoing syllabus. Its questions are filed under the Economics Topic Atlas taxonomy the Atlas uses for every sitting 2010-2026, whose canonical nodes are those of the 2019 specification; no Syllabus X-Ray link is claimed.',
}
out = W / 'scripts/markbank/authoring/drafts/economics-2015-hl-ev.json'
out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
print(len(tasks), 'routes;', len(sels), 'directives ->', out)
